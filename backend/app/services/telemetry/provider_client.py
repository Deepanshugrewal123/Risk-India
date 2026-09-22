"""
RISK // INDIA — Hydrological Provider Ingestion Clients & Fault Isolation
=========================================================================
Encapsulates external agency connections (CWC, IMD, NRSC/Bhuvan, ASDMA)
with dedicated, isolated Circuit Breakers. Failure in one agency never degrades others.
"""

from typing import Dict, List, Any, Optional
import time
import logging
from app.services.disaster_provider import CircuitBreaker, CircuitState

logger = logging.getLogger("telemetry-providers")


class HydrologicalProviderClient:
    """
    Multi-agency telemetry integration client.
    Maintains isolated circuit breakers for each upstream source.
    """

    PROVIDERS = ["CWC", "IMD", "NRSC_BHUVAN", "ASDMA"]

    def __init__(self):
        self._circuit_breakers: Dict[str, CircuitBreaker] = {}
        for p in self.PROVIDERS:
            self._circuit_breakers[p] = CircuitBreaker(
                failure_threshold=3,
                cooldown_seconds=30.0
            )
        self._cached_provider_data: Dict[str, List[Dict[str, Any]]] = {p: [] for p in self.PROVIDERS}
        self._last_successful_fetch: Dict[str, float] = {p: 0.0 for p in self.PROVIDERS}

    def get_circuit_status(self, provider: str) -> Dict[str, Any]:
        """Returns the live circuit breaker state for a specific provider."""
        p_clean = provider.strip().upper()
        cb = self._circuit_breakers.get(p_clean)
        if not cb:
            return {"provider": provider, "status": "UNKNOWN"}
        return {
            "provider": p_clean,
            "state": cb.state.value,
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
        fallback_data: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Executes an upstream ingestion call protected by provider's circuit breaker.
        Faults are isolated: exceptions do not escape or affect peers.
        """
        p_clean = provider.strip().upper()
        cb = self._circuit_breakers.get(p_clean)
        if not cb:
            raise ValueError(f"Unknown provider '{provider}'")

        if not cb.can_execute():
            logger.warning(f"Telemetry circuit OPEN for {p_clean}. Using cached fallback data.")
            cached = self._cached_provider_data.get(p_clean, [])
            return cached if cached else (fallback_data or [])

        try:
            data = fetch_func()
            cb.record_success()
            self._cached_provider_data[p_clean] = data
            self._last_successful_fetch[p_clean] = time.time()
            return data
        except Exception as exc:
            cb.record_failure(str(exc))
            logger.error(f"Upstream provider failure [{p_clean}]: {exc}. Circuit failure count: {cb.failure_count}")
            cached = self._cached_provider_data.get(p_clean, [])
            return cached if cached else (fallback_data or [])

    def force_trip_circuit(self, provider: str):
        """Forces a circuit breaker into OPEN state (for testing/fault injection)."""
        p_clean = provider.strip().upper()
        if p_clean in self._circuit_breakers:
            cb = self._circuit_breakers[p_clean]
            for _ in range(cb.failure_threshold + 1):
                cb.record_failure("Forced test trip")

    def reset_circuit(self, provider: str):
        """Resets a provider circuit to CLOSED state."""
        p_clean = provider.strip().upper()
        if p_clean in self._circuit_breakers:
            cb = self._circuit_breakers[p_clean]
            cb.state = CircuitState.CLOSED
            cb.failure_count = 0
            cb.last_failure_time = None


hydrological_provider_client = HydrologicalProviderClient()
