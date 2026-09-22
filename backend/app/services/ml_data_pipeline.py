"""
RISK // INDIA — Future Flood ML Data Pipeline & Data Quality Gates
==================================================================
Auditable data pipeline architecture for future river basin expansion.

Pipeline Stages:
1. RAW: Ingested telemetry and satellite readings from CWC, IMD, ISRO/Bhuvan.
2. VALIDATED: Strict quality gate validation; bad data quarantined with audit reasons.
3. NORMALIZED: Coordinates, physical units, and timestamps standardized.
4. EVENT_LABELED: Inundation truth labels aligned from verified flood rasters.
5. FEATURE_ENGINEERED: Antecedent rainfall, surge deltas, and seasonal harmonics computed.
6. LEAKAGE_AUDITED: Verified strict temporal ordering (observation_time <= event_time).
7. MODEL_READY: Clean feature matrix for audited basin model training.

SCIENTIFIC PRINCIPLE:
Never silently alter suspect data. Quarantined records are isolated with clear failure reasons.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone
import math
import logging

logger = logging.getLogger("ml-data-pipeline")


class PipelineStage:
    RAW = "RAW"
    VALIDATED = "VALIDATED"
    NORMALIZED = "NORMALIZED"
    EVENT_LABELED = "EVENT_LABELED"
    FEATURE_ENGINEERED = "FEATURE_ENGINEERED"
    LEAKAGE_AUDITED = "LEAKAGE_AUDITED"
    MODEL_READY = "MODEL_READY"


@dataclass
class RawObservation:
    source: str
    station_id: str
    station_name: str
    basin: str
    latitude: float
    longitude: float
    observation_time: str
    parameter: str  # rainfall, river_stage, discharge
    value: float
    unit: str  # mm, meters, cumec
    retrieval_time: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    quality_flag: str = "RAW_UNAUDITED"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QuarantinedRecord:
    raw_observation: RawObservation
    quarantine_reason: str
    violated_rule: str
    quarantined_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DataQualityGate:
    """
    Automated gatekeeper validating incoming hydrological and meteorological observations.
    """
    # Physical subcontinental bounding box [6.0°N–38.0°N, 68.0°E–98.0°E]
    MIN_LAT = 6.0
    MAX_LAT = 38.0
    MIN_LON = 68.0
    MAX_LON = 98.0

    # Physical thresholds
    MAX_24H_RAINFALL_MM = 2000.0  # Cherrapunji world record reference ~1563 mm/24h
    MIN_RIVER_STAGE_M = -10.0      # Estuarine datum offset
    MAX_RIVER_STAGE_M = 35.0       # Maximum extreme Brahmaputra/Ganga crest
    MAX_6H_SURGE_M = 10.0          # Flash flood surge upper bound

    @classmethod
    def validate_record(
        cls,
        obs: RawObservation,
        event_time: Optional[str] = None
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validates an individual observation against physical, temporal, and spatial rules.
        Returns:
            (is_valid, failure_reason, violated_rule)
        """
        # 1. Source Provenance
        if not obs.source or not obs.source.strip():
            return False, "Missing authoritative source provenance", "SOURCE_PROVENANCE"

        # 2. Station Identity
        if not obs.station_id or not obs.station_id.strip():
            return False, "Missing unique station identifier", "STATION_IDENTITY"

        # 3. Coordinate Validity
        if obs.latitude is None or obs.longitude is None:
            return False, "Missing geographic coordinates", "COORDINATE_VALIDITY"
        if not (cls.MIN_LAT <= obs.latitude <= cls.MAX_LAT and cls.MIN_LON <= obs.longitude <= cls.MAX_LON):
            return False, f"Coordinates ({obs.latitude}, {obs.longitude}) out of Indian subcontinent bounds", "COORDINATE_BOUNDS"

        # 4. Timestamp Validity
        if not obs.observation_time:
            return False, "Missing observation timestamp", "TIMESTAMP_VALIDITY"
        try:
            obs_dt = datetime.fromisoformat(obs.observation_time.replace("Z", "+00:00"))
            if obs_dt.tzinfo is None:
                obs_dt = obs_dt.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            if obs_dt > now:
                return False, f"Observation timestamp is in the future: {obs.observation_time}", "FUTURE_TIMESTAMP"
        except ValueError:
            return False, f"Invalid ISO observation timestamp: {obs.observation_time}", "TIMESTAMP_FORMAT"

        # 5. Future-Data Leakage Prevention (Crucial for ML Integrity)
        if event_time:
            try:
                ev_dt = datetime.fromisoformat(event_time.replace("Z", "+00:00"))
                if ev_dt.tzinfo is None:
                    ev_dt = ev_dt.replace(tzinfo=timezone.utc)
                if obs_dt > ev_dt:
                    return False, f"Temporal leakage detected: obs_time ({obs.observation_time}) > event_time ({event_time})", "DATA_LEAKAGE"
            except ValueError:
                pass

        # 6. Parameter-Specific Physical Bounds
        param_clean = (obs.parameter or "").lower().strip()

        # Rainfall rules
        if "rain" in param_clean or "precip" in param_clean:
            if obs.value is None or math.isnan(obs.value):
                return False, "Null rainfall observation value", "MISSING_VALUE"
            if obs.value < 0.0:
                return False, f"Negative rainfall value physically impossible: {obs.value} mm", "NEGATIVE_RAINFALL"
            if obs.value > cls.MAX_24H_RAINFALL_MM:
                return False, f"Rainfall exceeds physical limit: {obs.value} mm > {cls.MAX_24H_RAINFALL_MM} mm", "EXCESSIVE_RAINFALL"

        # River stage rules
        elif "river" in param_clean or "stage" in param_clean or "level" in param_clean:
            if obs.value is None or math.isnan(obs.value):
                return False, "Null river stage observation value", "MISSING_VALUE"
            if obs.value < cls.MIN_RIVER_STAGE_M or obs.value > cls.MAX_RIVER_STAGE_M:
                return False, f"River stage outside physical range [{cls.MIN_RIVER_STAGE_M}m, {cls.MAX_RIVER_STAGE_M}m]: {obs.value}m", "PHYSICALLY_IMPOSSIBLE_STAGE"

        return True, None, None


class MLDataPipelineManager:
    """
    Orchestrates ingestion, gate validation, quarantine isolation, and dataset progression.
    """
    def __init__(self):
        self.raw_count = 0
        self.validated_records: List[RawObservation] = []
        self.quarantined_records: List[QuarantinedRecord] = []

    def process_observations(
        self,
        observations: List[RawObservation],
        event_time: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes Quality Gate filtering over incoming observations.
        """
        initial_count = len(observations)
        self.raw_count += initial_count
        accepted: List[RawObservation] = []

        for obs in observations:
            is_valid, reason, rule = DataQualityGate.validate_record(obs, event_time=event_time)
            if is_valid:
                obs.quality_flag = "VALIDATED_EMPIRICAL"
                accepted.append(obs)
                self.validated_records.append(obs)
            else:
                quarantine = QuarantinedRecord(
                    raw_observation=obs,
                    quarantine_reason=reason or "Failed quality check",
                    violated_rule=rule or "UNKNOWN_RULE"
                )
                self.quarantined_records.append(quarantine)
                logger.warning(f"Record quarantined [Station {obs.station_id}]: {reason}")

        return {
            "initial_count": initial_count,
            "accepted_count": len(accepted),
            "quarantined_count": initial_count - len(accepted),
            "pass_rate": (len(accepted) / initial_count) if initial_count > 0 else 0.0,
            "current_stage": PipelineStage.VALIDATED
        }

    def get_pipeline_telemetry(self) -> Dict[str, Any]:
        return {
            "total_ingested": self.raw_count,
            "total_validated": len(self.validated_records),
            "total_quarantined": len(self.quarantined_records),
            "quarantine_reasons": [q.quarantine_reason for q in self.quarantined_records[-10:]]
        }


ml_data_pipeline_manager = MLDataPipelineManager()
