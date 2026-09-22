"""
RISK // INDIA — Multi-Hazard Disaster Intelligence Provider Framework
=====================================================================
Abstract base classes, circuit breaker specifications, and standardized
event normalization schemas for authoritative Indian disaster telemetry.

Enforces:
- Strict provider isolation (fault in one provider never impacts others)
- Circuit breaker resilience (CLOSED -> OPEN -> HALF_OPEN recovery)
- Explicit freshness classification (LIVE, RECENT, STALE, UNAVAILABLE)
- Provenance tracking (source agency, official bulletin URL, retrieval timestamps)
- Zero synthetic data generation
"""

import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any

from app.services.disaster_provider import (
    NormalizedDisasterEvent,
    CircuitBreaker,
    CircuitState,
    calculate_freshness,
    INDIAN_PLACE_TO_STATE
)
from app.services.metrics_service import metrics_collector

logger = logging.getLogger("hazard-providers")

class BaseHazardProvider(ABC):
    """
    Abstract interface for single-hazard operational data providers.
    Every hazard provider encapsulates its own timeouts, retry policy,
    circuit breaker, and schema validation.
    """

    def __init__(
        self,
        name: str,
        hazard_type: str,
        is_live: bool,
        timeout_sec: int = 10,
        failure_threshold: int = 5,
        cooldown_sec: float = 60.0
    ):
        self._name = name
        self._hazard_type = hazard_type
        self._is_live = is_live
        self.timeout_sec = timeout_sec
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=failure_threshold,
            cooldown_seconds=cooldown_sec
        )
        self.last_status = "initialized"
        self.last_error: Optional[str] = None
        self.last_retrieved: Optional[datetime] = None
        self._last_good_events: List[NormalizedDisasterEvent] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def hazard_type(self) -> str:
        return self._hazard_type

    @property
    def is_live(self) -> bool:
        return self._is_live

    @abstractmethod
    def fetch_events(self) -> List[NormalizedDisasterEvent]:
        """Ingests, validates, and normalizes events for this hazard."""
        pass

    def safe_fetch_events(self) -> List[NormalizedDisasterEvent]:
        """
        Executes fetch_events with circuit breaker gating and fault isolation.
        Returns empty list or cached events with updated STALE freshness on failure.
        """
        now = datetime.now(timezone.utc)

        # 1. Check Circuit Breaker
        if not self.circuit_breaker.can_execute():
            self.last_status = "circuit_open"
            self.last_error = (
                f"Circuit breaker is OPEN ({self.circuit_breaker.failure_count} failures). "
                f"Queries halted for {self.circuit_breaker.cooldown_seconds}s cooldown."
            )
            logger.warning(f"Provider '{self.name}' query suppressed: {self.last_error}")
            metrics_collector.record_provider_event(self.name, "circuit_trip")
            return self._get_stale_fallback(now)

        # 2. Execute fetch with safe error handling
        metrics_collector.record_provider_event(self.name, "request")
        try:
            events = self.fetch_events()
            self.circuit_breaker.record_success()
            self.last_status = "healthy"
            self.last_error = None
            self.last_retrieved = now
            self._last_good_events = events
            metrics_collector.record_provider_event(self.name, "success")
            return events
        except Exception as e:
            self.circuit_breaker.record_failure(str(e))
            if self.circuit_breaker.state == CircuitState.OPEN:
                self.last_status = "circuit_open"
            else:
                self.last_status = "error"
            self.last_error = str(e)
            logger.warning(f"Provider '{self.name}' fetch failed: {e}")
            metrics_collector.record_provider_event(self.name, "failure")
            return self._get_stale_fallback(now)

    def _get_stale_fallback(self, now: datetime) -> List[NormalizedDisasterEvent]:
        """Returns cached events marked as STALE when upstream is unreachable."""
        if not self._last_good_events:
            return []
        metrics_collector.record_cache_event("stale_served")
        refreshed = []
        for ev in self._last_good_events:
            tag = calculate_freshness(ev.observed_at, now=now)
            if tag == "LIVE":
                tag = "RECENT"
            refreshed.append(NormalizedDisasterEvent(
                id=ev.id,
                hazard_type=ev.hazard_type,
                title=ev.title,
                state=ev.state,
                district=ev.district,
                latitude=ev.latitude,
                longitude=ev.longitude,
                severity=ev.severity,
                status=ev.status,
                description=ev.description,
                source=ev.source,
                source_url=ev.source_url,
                verified=ev.verified,
                is_demo=ev.is_demo,
                observed_at=ev.observed_at,
                retrieved_at=now,
                freshness=tag,
                risk_score=ev.risk_score,
                event_subtype=ev.event_subtype,
                basin=ev.basin,
                source_event_id=ev.source_event_id,
                confidence=ev.confidence,
                official_alert=ev.official_alert,
                geometry=ev.geometry
            ))
        return refreshed

    def get_health(self) -> Dict[str, Any]:
        """Returns standardized health report for this provider."""
        return {
            "name": self.name,
            "hazard_type": self.hazard_type,
            "is_live": self.is_live,
            "status": "circuit_open" if self.circuit_breaker.state == CircuitState.OPEN else self.last_status,
            "last_retrieved": self.last_retrieved.isoformat() if self.last_retrieved else None,
            "error": self.last_error,
            "cached_events_count": len(self._last_good_events),
            "circuit_breaker": {
                "state": self.circuit_breaker.state.value,
                "failure_count": self.circuit_breaker.failure_count,
                "failure_threshold": self.circuit_breaker.failure_threshold,
                "cooldown_seconds": self.circuit_breaker.cooldown_seconds
            }
        }
