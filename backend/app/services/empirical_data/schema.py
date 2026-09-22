"""
RISK // INDIA — Canonical Empirical Flood Observation Schema
============================================================
Defines the strict schema for real hydrological observations with full provenance.
Missing data remains explicitly missing and is never artificially imputed.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import hashlib

from .base import QualityStatus, ProvenanceStatus, DataFreshness, ScientificState


@dataclass
class EmpiricalObservationRecord:
    """
    Standardized empirical flood observation record with complete provenance metadata.
    """
    observation_id: str
    basin: str
    state: str
    gauge_id: str
    gauge_name: str
    timestamp: str                                    # UTC ISO 8601
    latitude: Optional[float] = None                  # WGS84 EPSG:4326
    longitude: Optional[float] = None                 # WGS84 EPSG:4326
    rainfall_6h: Optional[float] = None               # mm
    rainfall_24h: Optional[float] = None              # mm
    rainfall_72h: Optional[float] = None              # mm
    rainfall_168h: Optional[float] = None             # mm
    river_level_relative: Optional[float] = None      # meters relative to danger level / datum
    river_rise_6h: Optional[float] = None             # meters
    river_rise_24h: Optional[float] = None            # meters
    river_percentile_level: Optional[float] = None    # 0.0 to 1.0
    flood_event_label: Optional[int] = None           # 0 (non-flood), 1 (flood), None (unlabeled)
    source_provider: str = "Central Water Commission"
    source_url_or_identifier: str = "https://ffs.india-water.gov.in"
    acquisition_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    original_units: Dict[str, str] = field(default_factory=lambda: {"rainfall": "mm", "water_level": "m"})
    normalized_units: Dict[str, str] = field(default_factory=lambda: {"rainfall": "mm", "water_level": "m"})
    quality_status: str = QualityStatus.VALIDATED.value
    provenance_status: str = ProvenanceStatus.VERIFIED_OFFICIAL.value
    quarantine_reasons: List[str] = field(default_factory=list)
    synthetic_records: int = 0                        # Strictly 0 across all authentic data

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def generate_observation_id(source_provider: str, gauge_id: str, parameter: str, timestamp_utc: str) -> str:
    """Generates deterministic 16-character SHA-256 identifier for an observation."""
    raw = f"{source_provider.strip().lower()}:{gauge_id.strip().upper()}:{parameter.strip().lower()}:{timestamp_utc.strip()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
