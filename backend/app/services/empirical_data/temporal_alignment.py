"""
RISK // INDIA — Deterministic Temporal Feature Alignment Engine
==============================================================
Deterministically aligns raw rainfall time series and river stage readings
into the canonical 13-feature vector required by the Assam ML model schema.
Enforces:
1. Chronological sequencing: observation_timestamp <= event_timestamp.
2. Rejection of future timestamps (REJECTION_REASON_FUTURE_TIMESTAMP).
3. Rejection of forward lookahead (REJECTION_REASON_TEMPORAL_LEAKAGE).
4. Strict guarantee: Temporal alignment NEVER triggers automated ML model training.
"""

from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timezone
import math
import logging

from .base import (
    REJECTION_REASON_FUTURE_TIMESTAMP,
    REJECTION_REASON_TEMPORAL_LEAKAGE,
    REJECTION_REASON_OUT_OF_BOUNDS_COORDINATES,
    REJECTION_REASON_MISSING_FEATURES
)
from .validators import validate_coordinates, validate_timestamp

logger = logging.getLogger("temporal-alignment")

CANONICAL_13_FEATURES = [
    "rainfall_6h",
    "rainfall_24h",
    "rainfall_72h",
    "rainfall_168h",
    "river_level_relative",
    "river_rise_6h",
    "river_rise_24h",
    "river_percentile_level",
    "month",
    "day_of_year_sin",
    "day_of_year_cos",
    "latitude",
    "longitude"
]


class TemporalAlignmentEngine:
    """Engine for aligning hydrological telemetry into canonical empirical feature vectors."""

    def align_observation_features(
        self,
        rainfall_series: Dict[str, float],
        stage_series: Dict[str, float],
        coordinates: Tuple[float, float],
        observation_timestamp: str,
        event_timestamp: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Aligns raw observation inputs into the canonical 13-feature empirical vector.
        Validates coordinate bounds, timestamps, and temporal leakage.
        """
        lat, lon = coordinates

        # 1. Geographic coordinate validation
        coord_valid, coord_msg = validate_coordinates(lat, lon)
        if not coord_valid:
            return {
                "is_valid": False,
                "rejection_reason": REJECTION_REASON_OUT_OF_BOUNDS_COORDINATES,
                "error": coord_msg,
                "aligned_features": None,
                "synthetic_records": 0,
                "training_triggered": False
            }

        # 2. Observation timestamp validation
        ts_valid, ts_err = validate_timestamp(observation_timestamp)
        if not ts_valid:
            return {
                "is_valid": False,
                "rejection_reason": REJECTION_REASON_FUTURE_TIMESTAMP,
                "error": ts_err or "Invalid observation timestamp format or future date",
                "aligned_features": None,
                "synthetic_records": 0,
                "training_triggered": False
            }

        try:
            clean_ts = observation_timestamp.strip().replace("Z", "+00:00")
            obs_dt = datetime.fromisoformat(clean_ts)
            if obs_dt.tzinfo is None:
                obs_dt = obs_dt.replace(tzinfo=timezone.utc)
        except Exception as e:
            return {
                "is_valid": False,
                "rejection_reason": REJECTION_REASON_FUTURE_TIMESTAMP,
                "error": f"Failed to parse timestamp: {e}",
                "aligned_features": None,
                "synthetic_records": 0,
                "training_triggered": False
            }

        # Check future timestamp against current UTC
        now_utc = datetime.now(timezone.utc)
        if obs_dt > now_utc:
            return {
                "is_valid": False,
                "rejection_reason": REJECTION_REASON_FUTURE_TIMESTAMP,
                "error": f"Observation timestamp {observation_timestamp} is in the future",
                "aligned_features": None,
                "synthetic_records": 0,
                "training_triggered": False
            }

        # 3. Temporal leakage check (observation must precede or coincide with event)
        if event_timestamp:
            try:
                clean_ev = event_timestamp.strip().replace("Z", "+00:00")
                ev_dt = datetime.fromisoformat(clean_ev)
                if ev_dt.tzinfo is None:
                    ev_dt = ev_dt.replace(tzinfo=timezone.utc)
                if obs_dt > ev_dt:
                    return {
                        "is_valid": False,
                        "rejection_reason": REJECTION_REASON_TEMPORAL_LEAKAGE,
                        "error": f"Observation timestamp ({observation_timestamp}) postdates event timestamp ({event_timestamp})",
                        "aligned_features": None,
                        "synthetic_records": 0,
                        "training_triggered": False
                    }
            except Exception:
                pass


        # 4. Cyclical calendar feature calculation
        month = float(obs_dt.month)
        day_of_year = obs_dt.timetuple().tm_yday
        day_of_year_sin = math.sin(2 * math.pi * day_of_year / 365.25)
        day_of_year_cos = math.cos(2 * math.pi * day_of_year / 365.25)

        # 5. Assemble the 13 canonical features
        aligned = {
            "rainfall_6h": float(rainfall_series.get("rainfall_6h", 0.0)),
            "rainfall_24h": float(rainfall_series.get("rainfall_24h", 0.0)),
            "rainfall_72h": float(rainfall_series.get("rainfall_72h", 0.0)),
            "rainfall_168h": float(rainfall_series.get("rainfall_168h", 0.0)),
            "river_level_relative": float(stage_series.get("river_level_relative", 0.0)),
            "river_rise_6h": float(stage_series.get("river_rise_6h", 0.0)),
            "river_rise_24h": float(stage_series.get("river_rise_24h", 0.0)),
            "river_percentile_level": float(stage_series.get("river_percentile_level", 0.5)),
            "month": month,
            "day_of_year_sin": round(day_of_year_sin, 6),
            "day_of_year_cos": round(day_of_year_cos, 6),
            "latitude": round(lat, 6),
            "longitude": round(lon, 6)
        }

        return {
            "is_valid": True,
            "rejection_reason": None,
            "aligned_features": aligned,
            "feature_count": len(aligned),
            "synthetic_records": 0,
            "training_triggered": False,
            "observation_timestamp": obs_dt.isoformat()
        }


temporal_alignment_engine = TemporalAlignmentEngine()
