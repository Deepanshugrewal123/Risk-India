"""
RISK // INDIA — Dynamic Catchment Telemetry Schema & Contracts
==============================================================
Canonical contracts, enums, and dataclasses for real-time hydrological sensor ingestion.
Enforces zero synthetic data (synthetic_records = 0 strictly).
"""

from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
import hashlib
from datetime import datetime, timezone


class VariableType(str, Enum):
    WATER_LEVEL = "WATER_LEVEL"
    RAINFALL = "RAINFALL"
    DISCHARGE = "DISCHARGE"


class ObservationQualityStatus(str, Enum):
    VALIDATED = "VALIDATED"
    FLAGGED = "FLAGGED"
    REJECTED = "REJECTED"
    UNVERIFIED = "UNVERIFIED"


class DataFreshness(str, Enum):
    LIVE = "LIVE"          # < 1 hour old
    RECENT = "RECENT"      # < 24 hours old
    STALE = "STALE"        # >= 24 hours old
    UNAVAILABLE = "UNAVAILABLE"


class GaugeStatus(str, Enum):
    ACTIVE_CALIBRATED = "ACTIVE_CALIBRATED"
    UNMAPPED = "UNMAPPED"
    INACTIVE = "INACTIVE"


class QualityRejectionReason(str, Enum):
    MISSING_GAUGE_ID = "MISSING_GAUGE_ID"
    INVALID_TIMESTAMP = "INVALID_TIMESTAMP"
    NON_NUMERIC_VALUE = "NON_NUMERIC_VALUE"
    UNKNOWN_UNIT = "UNKNOWN_UNIT"
    PHYSICALLY_IMPOSSIBLE_VALUE = "PHYSICALLY_IMPOSSIBLE_VALUE"
    OUT_OF_BOUNDS_COORDINATES = "OUT_OF_BOUNDS_COORDINATES"
    UNVERIFIED_GEOGRAPHIC_MAPPING = "UNVERIFIED_GEOGRAPHIC_MAPPING"
    DUPLICATE_OBSERVATION = "DUPLICATE_OBSERVATION"
    CORRUPTED_PAYLOAD = "CORRUPTED_PAYLOAD"
    FUTURE_DATED_OBSERVATION = "FUTURE_DATED_OBSERVATION"
    SYNTHETIC_DATA_REJECTED = "SYNTHETIC_DATA_REJECTED"
    STALE_THRESHOLD_EXCEEDED = "STALE_THRESHOLD_EXCEEDED"
    UNSUPPORTED_VARIABLE = "UNSUPPORTED_VARIABLE"


@dataclass
class CanonicalGauge:
    """Authoritative hydrological monitoring station representation."""
    station_id: str
    station_name: str
    basin_id: str
    sub_basin: str
    river_name: str
    state: str
    district: str
    latitude: float
    longitude: float
    elevation_msl_m: Optional[float] = None
    warning_level_m: Optional[float] = None
    danger_level_m: Optional[float] = None
    hfl_m: Optional[float] = None
    zero_datum_m: Optional[float] = None
    agency: str = "Central Water Commission (CWC)"
    status: str = GaugeStatus.ACTIVE_CALIBRATED.value

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class UnitConversionRecord:
    """Audit trail of mathematical unit conversion."""
    original_value: float
    original_unit: str
    normalized_value: float
    normalized_unit: str
    conversion_rule: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HydrologicalObservation:
    """
    Canonical normalized hydrological observation with complete provenance.
    Zero synthetic records allowed (synthetic_records = 0 strictly).
    """
    observation_id: str
    gauge_id: str
    gauge_name: str
    river_name: str
    catchment: str
    major_basin: str
    state: str
    district: str
    latitude: float
    longitude: float
    observed_at: str                        # UTC ISO 8601 recorded by sensor
    ingested_at: str                        # UTC ISO 8601 recorded by ingestion engine
    variable_type: str                      # WATER_LEVEL, RAINFALL, DISCHARGE
    original_value: float
    original_unit: str
    normalized_value: float
    normalized_unit: str                    # m, mm, m3_s
    conversion_rule: str
    source_provider: str
    source_identifier: str
    quality_status: str                     # VALIDATED, FLAGGED, REJECTED, UNVERIFIED
    rejection_reasons: List[str] = field(default_factory=list)
    freshness: str = DataFreshness.LIVE.value
    synthetic_records: int = 0              # Invariant: strictly 0
    provenance: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TelemetryIngestionBatch:
    """Batch summary resulting from dynamic sensor telemetry ingestion."""
    batch_id: str
    total_submitted: int
    accepted_count: int
    rejected_count: int
    deduplicated_count: int
    rejections: List[Dict[str, Any]] = field(default_factory=list)
    ingested_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def generate_observation_id(source_provider: str, gauge_id: str, variable_type: str, observed_at: str) -> str:
    """Deterministically creates a 16-character SHA-256 observation identifier."""
    raw = f"{source_provider.strip().lower()}:{gauge_id.strip().upper()}:{variable_type.strip().upper()}:{observed_at.strip()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
