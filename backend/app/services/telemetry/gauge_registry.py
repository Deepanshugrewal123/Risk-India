"""
RISK // INDIA — Dynamic Catchment Gauge Registry & Hierarchical Normalizer
==========================================================================
Maintains authoritative gauge stations and executes deterministic routing:
GAUGE -> RIVER -> CATCHMENT/SUB-BASIN -> MAJOR BASIN -> STATE/UT

Unmapped gauges are explicitly assigned status UNMAPPED; never guessed.
"""

from typing import Dict, List, Optional, Any
import logging
from app.services.basin_gauge_registry import CANONICAL_BASIN_GAUGES, BasinGaugeStation
from .schema import CanonicalGauge, GaugeStatus

logger = logging.getLogger("telemetry-gauge-registry")


class CatchmentGaugeRegistry:
    """
    Catalog of canonical Indian river basin gauging stations and spatial normalizer.
    Pre-seeded with official CWC calibrated stations across major basins.
    """

    def __init__(self):
        self._gauges: Dict[str, CanonicalGauge] = {}
        self._aliases: Dict[str, str] = {}
        self._load_canonical_gauges()

    def _load_canonical_gauges(self):
        """Loads canonical gauges from basin_gauge_registry."""
        for bg in CANONICAL_BASIN_GAUGES:
            cg = CanonicalGauge(
                station_id=bg.station_id,
                station_name=bg.station_name,
                basin_id=bg.basin_id.lower(),
                sub_basin=bg.sub_basin,
                river_name=bg.river_name,
                state=bg.state,
                district=bg.district,
                latitude=bg.latitude,
                longitude=bg.longitude,
                elevation_msl_m=bg.elevation_msl_m,
                warning_level_m=bg.warning_level_m,
                danger_level_m=bg.danger_level_m,
                hfl_m=bg.hfl_m,
                zero_datum_m=bg.zero_datum_m,
                agency=bg.agency,
                status=GaugeStatus.ACTIVE_CALIBRATED.value
            )
            self.register_gauge(cg)

    def register_gauge(self, gauge: CanonicalGauge):
        """Registers a canonical gauge and indexes normalized aliases."""
        clean_id = gauge.station_id.strip().upper()
        self._gauges[clean_id] = gauge
        # Index aliases
        self._aliases[clean_id.lower()] = clean_id
        self._aliases[clean_id.replace("-", "").lower()] = clean_id
        self._aliases[gauge.station_name.strip().lower()] = clean_id

    def get_gauge(self, gauge_id: str) -> Optional[CanonicalGauge]:
        """Direct lookup by station ID or normalized alias."""
        if not gauge_id:
            return None
        clean = gauge_id.strip().upper()
        if clean in self._gauges:
            return self._gauges[clean]
        alias_key = gauge_id.strip().lower()
        if alias_key in self._aliases:
            return self._gauges[self._aliases[alias_key]]
        return None

    def normalize_or_unmapped(self, gauge_id: str, raw_metadata: Optional[Dict[str, Any]] = None) -> CanonicalGauge:
        """
        Resolves gauge ID to CanonicalGauge.
        If unknown, returns an explicit UNMAPPED CanonicalGauge without guessing.
        """
        existing = self.get_gauge(gauge_id)
        if existing:
            return existing

        meta = raw_metadata or {}
        # Unmapped: do not invent basin or catchment
        return CanonicalGauge(
            station_id=gauge_id.strip().upper(),
            station_name=meta.get("station_name", f"Unmapped Station ({gauge_id})"),
            basin_id="unmapped",
            sub_basin="unmapped",
            river_name=meta.get("river_name", "unmapped"),
            state=meta.get("state", "unmapped"),
            district=meta.get("district", "unmapped"),
            latitude=float(meta.get("latitude", 0.0)) if meta.get("latitude") is not None else 0.0,
            longitude=float(meta.get("longitude", 0.0)) if meta.get("longitude") is not None else 0.0,
            status=GaugeStatus.UNMAPPED.value,
            agency=meta.get("agency", "UNVERIFIED_SOURCE")
        )

    def get_all_gauges(self) -> List[CanonicalGauge]:
        return list(self._gauges.values())

    def get_gauges_by_basin(self, basin_id: str) -> List[CanonicalGauge]:
        b_clean = basin_id.strip().lower()
        return [g for g in self._gauges.values() if g.basin_id == b_clean]

    def get_gauges_by_state(self, state: str) -> List[CanonicalGauge]:
        s_clean = state.strip().lower()
        return [g for g in self._gauges.values() if s_clean in g.state.lower()]


catchment_gauge_registry = CatchmentGaugeRegistry()
