"""
RISK // INDIA — Multi-Agency Weather Ingestion Client & Circuit Breakers
========================================================================
Maintains isolated circuit breakers for IMD, CWC, NDMA, and NRSC/Bhuvan.
Outages in one agency never cascade to or degrade peer providers.
"""

from typing import Dict, List, Any, Optional
import time
import logging
from datetime import datetime, timezone

from app.services.disaster_provider import CircuitBreaker, CircuitState

logger = logging.getLogger("weather-providers")


class WeatherProviderClient:
    """
    Authoritative meteorological provider integration client.
    Enforces circuit breakers and fault containment.
    """

    PROVIDERS = ["IMD", "CWC", "NDMA", "NRSC_BHUVAN"]

    def __init__(self):
        self._circuit_breakers: Dict[str, CircuitBreaker] = {}
        for p in self.PROVIDERS:
            self._circuit_breakers[p] = CircuitBreaker(
                failure_threshold=3,
                cooldown_seconds=30.0
            )
        self._cached_payloads: Dict[str, Any] = {p: [] for p in self.PROVIDERS}

    def get_circuit_status(self, provider: str) -> Dict[str, Any]:
        p_clean = provider.strip().upper()
        cb = self._circuit_breakers.get(p_clean)
        if not cb:
            return {"provider": provider, "status": "UNKNOWN"}
        return {
            "provider": p_clean,
            "state": cb.state.value if hasattr(cb.state, "value") else str(cb.state),
            "failure_count": cb.failure_count,
            "threshold": cb.failure_threshold,
            "last_failure_time": cb.last_failure_time.isoformat() if cb.last_failure_time else None
        }

    def get_all_circuit_statuses(self) -> Dict[str, Any]:
        return {p: self.get_circuit_status(p) for p in self.PROVIDERS}

    def execute_with_circuit_breaker(
        self,
        provider: str,
        fetch_func,
        fallback_data: Optional[Any] = None
    ) -> Any:
        p_clean = provider.strip().upper()
        cb = self._circuit_breakers.get(p_clean)
        if not cb:
            raise ValueError(f"Unknown provider '{provider}'")

        if not cb.can_execute():
            logger.warning(f"Weather circuit OPEN for {p_clean}. Using cached fallback data.")
            cached = self._cached_payloads.get(p_clean)
            return cached if cached else fallback_data

        try:
            data = fetch_func()
            cb.record_success()
            self._cached_payloads[p_clean] = data
            return data
        except Exception as exc:
            cb.record_failure(str(exc))
            logger.error(f"Weather provider failure [{p_clean}]: {exc}. Circuit failures: {cb.failure_count}")
            cached = self._cached_payloads.get(p_clean)
            return cached if cached else fallback_data

    def is_provider_healthy(self, provider: str) -> bool:
        p_clean = provider.strip().upper()
        cb = self._circuit_breakers.get(p_clean)
        return cb.state == CircuitState.CLOSED if cb else False

    def record_failure(self, provider: str, error: str = "Provider failure"):
        p_clean = provider.strip().upper()
        if p_clean in self._circuit_breakers:
            self._circuit_breakers[p_clean].record_failure(error)

    def force_trip_circuit(self, provider: str):
        p_clean = provider.strip().upper()
        if p_clean in self._circuit_breakers:
            cb = self._circuit_breakers[p_clean]
            for _ in range(cb.failure_threshold + 1):
                cb.record_failure("Forced test trip")

    def reset_circuit(self, provider: str):
        p_clean = provider.strip().upper()
        if p_clean in self._circuit_breakers:
            cb = self._circuit_breakers[p_clean]
            cb.state = CircuitState.CLOSED
            cb.failure_count = 0
            cb.last_failure_time = None


weather_provider_client = WeatherProviderClient()
