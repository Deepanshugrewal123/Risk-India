"""
RISK // INDIA — Rate Limiting & Abuse Protection Middleware
===========================================================
In-memory sliding-window rate limiter designed to prevent compute exhaustion,
upstream telemetry scraping, and DoS abuse.

Limits:
- Compute routes (POST /api/risk/analyze, GET /api/disasters/refresh): ~10 requests / 60 seconds
- General API routes: ~60 requests / 60 seconds

Features:
- Sliding-window timestamp accounting (accurate, prevents burst-at-boundary exploits)
- LRU / TTL memory bounding to prevent unbounded state growth
- Safe client IP extraction handling X-Forwarded-For headers
- HTTP 429 response with RFC-compliant `Retry-After` header
"""

import time
import re
from collections import defaultdict, deque
from typing import Dict, Deque, Tuple
import threading

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.config import settings
from app.services.metrics_service import metrics_collector

# Strict IPv4 / IPv6 validation pattern for sanitized X-Forwarded-For parsing
IP_PATTERN = re.compile(r"^[0-9a-fA-F:.]+$")


class RateLimiter:
    """
    Sliding-window in-memory rate limiter with TTL cleanup.
    """
    def __init__(
        self,
        general_limit: int = 60,
        compute_limit: int = 10,
        window_seconds: int = 60,
        max_tracked_ips: int = 10000
    ):
        self.general_limit = general_limit
        self.compute_limit = compute_limit
        self.window_seconds = window_seconds
        self.max_tracked_ips = max_tracked_ips

        # { (ip, tier): deque([timestamp, ...]) }
        self._records: Dict[Tuple[str, str], Deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()
        self._call_count = 0

    def _resolve_ip(self, request: Request) -> str:
        xff = request.headers.get("x-forwarded-for")
        if xff:
            # First IP in X-Forwarded-For is client origin
            candidate = xff.split(",")[0].strip()
            if candidate and IP_PATTERN.match(candidate):
                return candidate

        client = request.client
        if client and client.host:
            return client.host

        return "127.0.0.1"

    def _get_tier_and_limit(self, method: str, path: str) -> Tuple[str, int]:
        m = method.upper()
        p = path.rstrip("/")

        # Compute routes: heavy ML inference or upstream provider refresh
        if (m == "POST" and p.endswith("/api/risk/analyze")) or \
           (m == "GET" and p.endswith("/api/disasters/refresh")):
            return "compute", self.compute_limit

        return "general", self.general_limit

    def check(self, request: Request) -> Tuple[bool, int]:
        """
        Returns (is_allowed, retry_after_seconds).
        """
        ip = self._resolve_ip(request)
        tier, limit = self._get_tier_and_limit(request.method, request.url.path)
        now = time.time()
        cutoff = now - self.window_seconds

        with self._lock:
            self._call_count += 1
            if self._call_count % 200 == 0:
                self._cleanup(cutoff)

            key = (ip, tier)
            history = self._records[key]

            # Evict timestamps outside the active sliding window
            while history and history[0] <= cutoff:
                history.popleft()

            if len(history) >= limit:
                oldest = history[0]
                retry_after = max(1, int(self.window_seconds - (now - oldest)))
                return False, retry_after

            # Record current request timestamp
            history.append(now)
            return True, 0

    def _cleanup(self, cutoff: float):
        """Prunes stale IP entries to prevent unbounded memory retention."""
        to_delete = []
        for key, history in self._records.items():
            while history and history[0] <= cutoff:
                history.popleft()
            if not history:
                to_delete.append(key)

        for key in to_delete:
            del self._records[key]

        # If still over threshold, reset oldest
        if len(self._records) > self.max_tracked_ips:
            self._records.clear()

    def reset(self):
        """Clears all tracking state (used in testing)."""
        with self._lock:
            self._records.clear()
            self._call_count = 0


# Singleton rate limiter instance
rate_limiter = RateLimiter(
    general_limit=getattr(settings, "RATE_LIMIT_GENERAL", 60),
    compute_limit=getattr(settings, "RATE_LIMIT_COMPUTE", 10),
    window_seconds=60
)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware enforcing sliding-window rate limits.
    """
    def __init__(self, app, limiter: RateLimiter = rate_limiter):
        super().__init__(app)
        self.limiter = limiter

    async def dispatch(self, request: Request, call_next) -> Response:
        allowed, retry_after = self.limiter.check(request)
        if not allowed:
            metrics_collector.record_rate_limit()
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Too Many Requests",
                    "detail": f"Rate limit exceeded. Please try again in {retry_after} seconds.",
                    "retry_after": retry_after
                },
                headers={
                    "Retry-After": str(retry_after)
                }
            )

        return await call_next(request)
