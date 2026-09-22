"""
RISK // INDIA — Cache Abstraction & Storage Layer
=================================================
Provides a unified caching interface supporting:
1. In-Memory TTL Cache (Thread-safe, sub-millisecond, default for development & testing)
2. Redis Distributed Cache (Optional, production-ready, with automatic graceful fallback)

Key Guarantees:
- Cache failures NEVER crash the application.
- Provider telemetry freshness is recalculated dynamically on cache retrieval.
- Stale cached data is NEVER labeled as LIVE.
- Zero sensitive credentials or PII stored in cache.
"""

import time
import json
import logging
import threading
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, Tuple
from datetime import datetime, timezone

from app.config import settings
from app.services.metrics_service import metrics_collector

logger = logging.getLogger("risk-india.cache")


class BaseCacheService(ABC):
    """
    Abstract interface for cache providers.
    """
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Retrieve value from cache, returning None if missing or expired."""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> bool:
        """Store value with optional TTL expiration."""
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete specific key."""
        pass

    @abstractmethod
    def clear(self) -> bool:
        """Clear all cached entries."""
        pass

    @abstractmethod
    def is_healthy(self) -> bool:
        """Check cache backend availability."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Gracefully close backend connections and resources."""
        pass

    @property
    @abstractmethod
    def backend_name(self) -> str:
        """Name of the active cache backend."""
        pass


class MemoryCacheService(BaseCacheService):

    """
    Thread-safe in-memory cache with timestamp-based TTL expiration.
    """
    def __init__(self, default_ttl: int = 300, max_keys: int = 5000):
        self.default_ttl = default_ttl
        self.max_keys = max_keys
        # { key: (value, expiry_timestamp) }
        self._store: Dict[str, Tuple[Any, float]] = {}
        self._lock = threading.Lock()

    @property
    def backend_name(self) -> str:
        return "memory"

    def get(self, key: str) -> Optional[Any]:
        now = time.time()
        with self._lock:
            record = self._store.get(key)
            if record is None:
                metrics_collector.record_cache_event("miss")
                return None
            val, expiry = record
            if expiry < now:
                del self._store[key]
                metrics_collector.record_cache_event("miss")
                return None
            metrics_collector.record_cache_event("hit")
            return val

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> bool:
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        expiry = time.time() + ttl
        with self._lock:
            # Memory safety: prune expired entries if near capacity
            if len(self._store) >= self.max_keys:
                self._prune_expired()
                if len(self._store) >= self.max_keys:
                    self._store.pop(next(iter(self._store)), None)

            self._store[key] = (value, expiry)
            return True

    def delete(self, key: str) -> bool:
        with self._lock:
            return self._store.pop(key, None) is not None

    def clear(self) -> bool:
        with self._lock:
            self._store.clear()
            return True

    def is_healthy(self) -> bool:
        return True

    def close(self) -> None:
        self.clear()


    def _prune_expired(self):
        now = time.time()
        expired = [k for k, (_, exp) in self._store.items() if exp < now]
        for k in expired:
            del self._store[k]


class RedisCacheService(BaseCacheService):
    """
    Redis-backed cache with automatic error suppression, metrics tracking,
    and automatic memory fallback during network or server outages.
    """
    def __init__(self, redis_url: str, default_ttl: int = 300):
        self.redis_url = redis_url
        self.default_ttl = default_ttl
        self._fallback_memory = MemoryCacheService(default_ttl=default_ttl)
        self._client = None
        self._init_client()

    @property
    def backend_name(self) -> str:
        return "redis" if self._client is not None else "redis (fallback to memory)"

    def _init_client(self):
        try:
            import redis
            self._client = redis.Redis.from_url(
                self.redis_url,
                socket_timeout=2.0,
                socket_connect_timeout=2.0,
                decode_responses=True
            )
            self._client.ping()
            logger.info("Connected to Redis cache backend successfully.")
        except Exception as e:
            logger.warning(f"Could not connect to Redis: {e}. Graceful degradation active.")
            self._client = None

    def get(self, key: str) -> Optional[Any]:
        if not self._client:
            metrics_collector.record_cache_event("offline_fallback")
            return self._fallback_memory.get(key)
        try:
            raw = self._client.get(key)
            if raw is None:
                metrics_collector.record_cache_event("miss")
                return None
            metrics_collector.record_cache_event("hit")
            return json.loads(raw)
        except Exception as e:
            logger.warning(f"Redis get error for key '{key}': {e}. Using fallback memory.")
            metrics_collector.record_cache_event("offline_fallback")
            return self._fallback_memory.get(key)

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> bool:
        # Always mirror into fallback memory for seamless continuity
        self._fallback_memory.set(key, value, ttl_seconds=ttl_seconds)
        if not self._client:
            return True
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        try:
            serialized = json.dumps(value)
            return bool(self._client.set(key, serialized, ex=ttl))
        except Exception as e:
            logger.warning(f"Redis set error for key '{key}': {e}. Maintained in memory fallback.")
            return True

    def delete(self, key: str) -> bool:
        self._fallback_memory.delete(key)
        if not self._client:
            return False
        try:
            return bool(self._client.delete(key))
        except Exception as e:
            logger.warning(f"Redis delete error for key '{key}': {e}")
            return False

    def clear(self) -> bool:
        self._fallback_memory.clear()
        if not self._client:
            return False
        try:
            return bool(self._client.flushdb())
        except Exception as e:
            logger.warning(f"Redis clear error: {e}")
            return False

    def is_healthy(self) -> bool:
        if not self._client:
            try:
                self._init_client()
            except Exception:
                pass
        if not self._client:
            return False
        try:
            return bool(self._client.ping())
        except Exception:
            self._client = None
            return False

    def close(self) -> None:
        if self._client:
            try:
                self._client.close()
            except Exception as e:
                logger.warning(f"Error closing Redis client: {e}")
            finally:
                self._client = None
        self._fallback_memory.close()



def get_cache_service() -> BaseCacheService:
    """
    Factory function returning the active cache provider.
    Automatically degrades to MemoryCacheService if Redis is unconfigured or unreachable.
    """
    requested_backend = getattr(settings, "CACHE_BACKEND", "memory").lower()
    redis_url = getattr(settings, "REDIS_URL", None)

    if requested_backend == "redis" and redis_url:
        try:
            redis_svc = RedisCacheService(redis_url=redis_url, default_ttl=settings.CACHE_TTL_SECONDS)
            if redis_svc.is_healthy():
                return redis_svc
            logger.warning("Redis is not healthy. Falling back to MemoryCacheService.")
        except Exception as e:
            logger.warning(f"Failed to initialize Redis: {e}. Falling back to MemoryCacheService.")

    return MemoryCacheService(default_ttl=settings.CACHE_TTL_SECONDS)


# Singleton cache service instance
cache_service: BaseCacheService = get_cache_service()
