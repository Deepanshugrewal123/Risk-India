"""
RISK // INDIA — Hydrological Telemetry Data Quality Engine (13 Rules)
=====================================================================
Evaluates incoming hydrological sensor feeds against 13 machine-readable criteria.
Rejects synthetic data, future timestamps, out-of-bound coordinates, impossible physics.
"""

from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime, timezone, timedelta
import math

from .schema import (
    VariableType,
    QualityRejectionReason,
    GaugeStatus,
    CanonicalGauge
)


class TelemetryQualityEngine:
    """
    Production-grade validation engine enforcing the 13 machine-readable quality gates.
    """

    INDIA_BOUNDS = {
        "min_lat": 6.0,
        "max_lat": 38.0,
        "min_lon": 68.0,
        "max_lon": 98.0
    }

    PHYSICAL_RANGES = {
        VariableType.WATER_LEVEL.value: (-10.0, 1000.0),    # -10m (datum) to 1000m MSL
        VariableType.RAINFALL.value: (0.0, 1500.0),          # 0mm to 1500mm in 24h
        VariableType.DISCHARGE.value: (0.0, 150000.0)        # 0 to 150k m3/s (Brahmaputra peak)
    }

    MAX_OPERATIONAL_AGE_DAYS = 90.0

    def validate_payload_structure(self, payload: Any) -> Tuple[bool, Optional[str]]:
        """Gate 9: Payload corruption / structural integrity."""
        if not isinstance(payload, dict):
            return False, QualityRejectionReason.CORRUPTED_PAYLOAD.value
        return True, None

    def validate_gauge_id(self, gauge_id: Any) -> Tuple[bool, Optional[str]]:
        """Gate 1: Gauge identifier presence."""
        if not gauge_id or not isinstance(gauge_id, str) or not gauge_id.strip():
            return False, QualityRejectionReason.MISSING_GAUGE_ID.value
        return True, None

    def validate_variable_type(self, variable_type: Any) -> Tuple[bool, Optional[str]]:
        """Gate 13: Unsupported variable."""
        if not variable_type or not isinstance(variable_type, str):
            return False, QualityRejectionReason.UNSUPPORTED_VARIABLE.value
        v_clean = variable_type.strip().upper()
        if v_clean not in [e.value for e in VariableType]:
            return False, QualityRejectionReason.UNSUPPORTED_VARIABLE.value
        return True, None

    def validate_numeric_value(self, value: Any) -> Tuple[bool, Optional[float], Optional[str]]:
        """Gate 3: Non-numeric value."""
        if value is None or isinstance(value, bool):
            return False, None, QualityRejectionReason.NON_NUMERIC_VALUE.value
        try:
            val = float(value)
            if math.isnan(val) or math.isinf(val):
                return False, None, QualityRejectionReason.NON_NUMERIC_VALUE.value
            return True, val, None
        except (ValueError, TypeError):
            return False, None, QualityRejectionReason.NON_NUMERIC_VALUE.value

    def validate_timestamp(self, ts_raw: Any, now: Optional[datetime] = None) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Gate 2: Invalid timestamp.
        Gate 10: Future dated observation.
        Gate 12: Stale threshold exceeded.
        """
        if not ts_raw or not isinstance(ts_raw, str):
            return False, None, QualityRejectionReason.INVALID_TIMESTAMP.value

        clean_ts = ts_raw.strip().replace("Z", "+00:00")
        try:
            dt = datetime.fromisoformat(clean_ts)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)
        except Exception:
            return False, None, QualityRejectionReason.INVALID_TIMESTAMP.value

        current_time = now or datetime.now(timezone.utc)

        # Gate 10: Future dated (> 5 min tolerance)
        if dt > current_time + timedelta(minutes=5):
            return False, None, QualityRejectionReason.FUTURE_DATED_OBSERVATION.value

        # Gate 12: Stale threshold (> 90 days)
        if (current_time - dt).total_seconds() > (self.MAX_OPERATIONAL_AGE_DAYS * 86400):
            return False, None, QualityRejectionReason.STALE_THRESHOLD_EXCEEDED.value

        return True, dt.strftime("%Y-%m-%dT%H:%M:%SZ"), None

    def validate_physical_limits(self, variable_type: str, normalized_value: float) -> Tuple[bool, Optional[str]]:
        """Gate 5: Physically impossible value."""
        v_clean = variable_type.strip().upper()
        if v_clean in self.PHYSICAL_RANGES:
            min_val, max_val = self.PHYSICAL_RANGES[v_clean]
            if normalized_value < min_val or normalized_value > max_val:
                return False, QualityRejectionReason.PHYSICALLY_IMPOSSIBLE_VALUE.value
        return True, None

    def validate_coordinates(self, lat: float, lon: float) -> Tuple[bool, Optional[str]]:
        """Gate 6: Out of bounds coordinates (WGS84 India)."""
        if not (self.INDIA_BOUNDS["min_lat"] <= lat <= self.INDIA_BOUNDS["max_lat"]) or            not (self.INDIA_BOUNDS["min_lon"] <= lon <= self.INDIA_BOUNDS["max_lon"]):
            return False, QualityRejectionReason.OUT_OF_BOUNDS_COORDINATES.value
        return True, None

    def validate_geographic_mapping(self, gauge: CanonicalGauge) -> Tuple[bool, Optional[str]]:
        """Gate 7: Unverified geographic mapping."""
        if gauge.status == GaugeStatus.UNMAPPED.value or gauge.basin_id == "unmapped":
            return False, QualityRejectionReason.UNVERIFIED_GEOGRAPHIC_MAPPING.value
        return True, None

    def validate_synthetic_data(self, payload: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Gate 11: Zero synthetic data check."""
        # 1. explicit synthetic_records > 0
        if payload.get("synthetic_records", 0) > 0:
            return False, QualityRejectionReason.SYNTHETIC_DATA_REJECTED.value
        # 2. explicit boolean flags
        if payload.get("is_synthetic") is True or payload.get("is_simulated") is True:
            return False, QualityRejectionReason.SYNTHETIC_DATA_REJECTED.value
        # 3. keywords in identifiers or provider
        text_fields = [
            str(payload.get("source_provider", "")),
            str(payload.get("source_identifier", "")),
            str(payload.get("gauge_id", "")),
            str(payload.get("gauge_name", ""))
        ]
        for t in text_fields:
            tl = t.lower()
            if "synthetic" in tl or "simulated" in tl or "mock_gauge" in tl:
                return False, QualityRejectionReason.SYNTHETIC_DATA_REJECTED.value
        return True, None


telemetry_quality_engine = TelemetryQualityEngine()
