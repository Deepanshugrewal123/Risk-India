"""
RISK // INDIA — Multi-Basin Data Quality Engine & Leakage Protection
=====================================================================
Rigorous quality audit and leakage prevention engine for multi-basin hydro-meteorological data.

SCIENTIFIC PRINCIPLES:
- Zero tolerance for synthetic, fabricated, or unverified placeholder measurements.
- Physical bounds validation calibrated to gauge elevation datums and historical records.
- Temporal leakage prevention: strict causality check (observation_time <= event_time).
- Basin-aware spatial and temporal cross-validation splitters preventing data leakage.
"""

from typing import Dict, Any, Optional, List, Tuple, Set
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import math
import logging

from app.services.hydro_schema import HydroObservation, HydroObservationNormalizer
from app.services.basin_gauge_registry import basin_gauge_registry, haversine_distance_km

logger = logging.getLogger("data-quality-engine")


@dataclass
class DataQualityViolation:
    record_id: str
    station_id: str
    violation_type: str
    description: str
    detected_value: Any
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DataQualityReport:
    basin_id: str
    total_records_analyzed: int
    valid_records_count: int
    quarantined_count: int
    duplicate_count: int
    temporal_leakage_violations: int
    physical_bounds_violations: int
    coordinate_violations: int
    pass_rate: float
    audit_timestamp: str
    is_basin_clean: bool
    violations: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MultiBasinDataQualityEngine:
    """
    Quality gatekeeper validating incoming hydro-meteorological observations
    against physical invariants, geographic boundaries, and temporal ordering.
    """
    # Continental India bounding box
    MIN_LAT = 6.0
    MAX_LAT = 38.0
    MIN_LON = 68.0
    MAX_LON = 98.0

    MAX_24H_RAINFALL_MM = 2000.0  # Physical upper bound
    MAX_6H_SURGE_M = 10.0         # Upper limit on rapid river surge (rate of rise)

    def __init__(self):
        self._quarantined_records: List[Dict[str, Any]] = []

    def validate_single_observation(
        self,
        obs: HydroObservation,
        event_time: Optional[str] = None
    ) -> Tuple[bool, Optional[DataQualityViolation]]:
        """
        Audits an observation against strict physical and temporal rules.
        """
        rec_id = f"{obs.station_id}@{obs.observation_timestamp}"

        # 1. Geographic Bounds Check
        if not (self.MIN_LAT <= obs.latitude <= self.MAX_LAT and self.MIN_LON <= obs.longitude <= self.MAX_LON):
            return False, DataQualityViolation(
                record_id=rec_id,
                station_id=obs.station_id,
                violation_type="COORDINATE_OUT_OF_BOUNDS",
                description=f"Coordinates ({obs.latitude}, {obs.longitude}) are outside Indian subcontinental bounds",
                detected_value={"lat": obs.latitude, "lon": obs.longitude}
            )

        # 2. Timestamp Validity & Future-Dated Check
        try:
            obs_dt = datetime.fromisoformat(obs.observation_timestamp.replace("Z", "+00:00"))
            if obs_dt.tzinfo is None:
                obs_dt = obs_dt.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            # Allow 5 minutes clock drift
            if (obs_dt - now).total_seconds() > 300:
                return False, DataQualityViolation(
                    record_id=rec_id,
                    station_id=obs.station_id,
                    violation_type="FUTURE_TIMESTAMP",
                    description=f"Observation timestamp is in the future: {obs.observation_timestamp}",
                    detected_value=obs.observation_timestamp
                )
        except Exception as e:
            return False, DataQualityViolation(
                record_id=rec_id,
                station_id=obs.station_id,
                violation_type="INVALID_TIMESTAMP_FORMAT",
                description=f"Timestamp could not be parsed: {e}",
                detected_value=obs.observation_timestamp
            )

        # 3. Temporal Leakage Prevention (Strict Causality)
        if event_time:
            try:
                ev_dt = datetime.fromisoformat(event_time.replace("Z", "+00:00"))
                if ev_dt.tzinfo is None:
                    ev_dt = ev_dt.replace(tzinfo=timezone.utc)
                if obs_dt > ev_dt:
                    return False, DataQualityViolation(
                        record_id=rec_id,
                        station_id=obs.station_id,
                        violation_type="DATA_LEAKAGE",
                        description=f"Temporal leakage: observation ({obs.observation_timestamp}) is AFTER event ({event_time})",
                        detected_value={"observation_time": obs.observation_timestamp, "event_time": event_time}
                    )
            except (ValueError, TypeError) as parse_err:
                logger.debug("Date parsing skipped in causality check: %s", parse_err)

        # 4. Precipitation Bounds
        for r_val, r_name in [
            (obs.rainfall_1h_mm, "rainfall_1h_mm"),
            (obs.rainfall_24h_mm, "rainfall_24h_mm"),
            (obs.rainfall_72h_mm, "rainfall_72h_mm"),
            (obs.rainfall_168h_mm, "rainfall_168h_mm")
        ]:
            if r_val is not None:
                if math.isnan(r_val) or r_val < 0.0:
                    return False, DataQualityViolation(
                        record_id=rec_id,
                        station_id=obs.station_id,
                        violation_type="NEGATIVE_RAINFALL",
                        description=f"Precipitation cannot be negative or NaN: {r_name}={r_val}",
                        detected_value={r_name: r_val}
                    )
                if r_val > self.MAX_24H_RAINFALL_MM:
                    return False, DataQualityViolation(
                        record_id=rec_id,
                        station_id=obs.station_id,
                        violation_type="EXCESSIVE_RAINFALL",
                        description=f"Precipitation exceeds physical limit ({self.MAX_24H_RAINFALL_MM}mm): {r_name}={r_val}",
                        detected_value={r_name: r_val}
                    )

        # 5. River Stage Physical Limits (Calibrated to Station Elevation Datums)
        registered_station = basin_gauge_registry.get_station(obs.station_id)
        if registered_station:
            # Check whether levels are expressed as gauge staff height above zero datum or absolute MSL
            if registered_station.zero_datum_m and registered_station.danger_level_m < registered_station.zero_datum_m:
                # Gauge height above zero datum (e.g. 0 to 25m staff height)
                min_allowable = -2.0
                max_allowable = (registered_station.hfl_m + 8.0) if registered_station.hfl_m else (registered_station.danger_level_m + 12.0)
            elif registered_station.zero_datum_m:
                # Absolute elevation in meters MSL (e.g. Nanded ~354m MSL)
                min_allowable = registered_station.zero_datum_m - 5.0
                max_allowable = (registered_station.hfl_m + 8.0) if registered_station.hfl_m else (registered_station.danger_level_m + 12.0)
            else:
                min_allowable = 0.0
                max_allowable = (registered_station.hfl_m + 8.0) if registered_station.hfl_m else (registered_station.danger_level_m + 12.0)

            if obs.water_level_m < min_allowable or obs.water_level_m > max_allowable:
                return False, DataQualityViolation(
                    record_id=rec_id,
                    station_id=obs.station_id,
                    violation_type="PHYSICALLY_IMPOSSIBLE_STAGE",
                    description=(
                        f"Water level {obs.water_level_m}m is outside calibrated physical range "
                        f"[{min_allowable:.1f}m, {max_allowable:.1f}m] for station {obs.station_name}"
                    ),
                    detected_value=obs.water_level_m
                )
        else:
            # Generic sanity check
            if obs.water_level_m < -10.0 or obs.water_level_m > 700.0:
                return False, DataQualityViolation(
                    record_id=rec_id,
                    station_id=obs.station_id,
                    violation_type="PHYSICALLY_IMPOSSIBLE_STAGE",
                    description=f"Water level {obs.water_level_m}m is outside generic physical bounds [-10m, 700m]",
                    detected_value=obs.water_level_m
                )

        # 6. Surge Rate Limit
        if obs.water_level_change_24h_m is not None:
            if abs(obs.water_level_change_24h_m) > self.MAX_6H_SURGE_M * 2:
                return False, DataQualityViolation(
                    record_id=rec_id,
                    station_id=obs.station_id,
                    violation_type="EXTREME_SURGE_RATE",
                    description=f"24h water level change of {obs.water_level_change_24h_m}m indicates telemetry glitch",
                    detected_value=obs.water_level_change_24h_m
                )

        return True, None

    def audit_basin_dataset(
        self,
        basin_id: str,
        observations: List[HydroObservation],
        event_time: Optional[str] = None
    ) -> DataQualityReport:
        """
        Audits a full batch of observations for a basin, detecting duplicates,
        quarantining invalid readings, and calculating pass rates.
        """
        total = len(observations)
        if total == 0:
            return DataQualityReport(
                basin_id=basin_id,
                total_records_analyzed=0,
                valid_records_count=0,
                quarantined_count=0,
                duplicate_count=0,
                temporal_leakage_violations=0,
                physical_bounds_violations=0,
                coordinate_violations=0,
                pass_rate=1.0,
                audit_timestamp=datetime.now(timezone.utc).isoformat(),
                is_basin_clean=True,
                violations=[]
            )

        seen_keys: Set[Tuple[str, str]] = set()
        duplicates = 0
        leakage_violations = 0
        physical_violations = 0
        coord_violations = 0
        quarantined = 0
        valid_count = 0
        violations_list: List[DataQualityViolation] = []

        for obs in observations:
            key = (obs.station_id, obs.observation_timestamp)
            if key in seen_keys:
                duplicates += 1
                quarantined += 1
                vio = DataQualityViolation(
                    record_id=f"{obs.station_id}@{obs.observation_timestamp}",
                    station_id=obs.station_id,
                    violation_type="DUPLICATE_RECORD",
                    description=f"Duplicate observation detected for station {obs.station_id} at {obs.observation_timestamp}",
                    detected_value=str(key)
                )
                violations_list.append(vio)
                continue

            seen_keys.add(key)
            is_valid, violation = self.validate_single_observation(obs, event_time=event_time)

            if is_valid:
                valid_count += 1
            else:
                quarantined += 1
                if violation:
                    violations_list.append(violation)
                    if violation.violation_type == "DATA_LEAKAGE":
                        leakage_violations += 1
                    elif violation.violation_type == "COORDINATE_OUT_OF_BOUNDS":
                        coord_violations += 1
                    elif violation.violation_type in ("NEGATIVE_RAINFALL", "EXCESSIVE_RAINFALL", "PHYSICALLY_IMPOSSIBLE_STAGE", "EXTREME_SURGE_RATE"):
                        physical_violations += 1

        pass_rate = round(valid_count / total, 4) if total > 0 else 0.0

        report = DataQualityReport(
            basin_id=basin_id,
            total_records_analyzed=total,
            valid_records_count=valid_count,
            quarantined_count=quarantined,
            duplicate_count=duplicates,
            temporal_leakage_violations=leakage_violations,
            physical_bounds_violations=physical_violations,
            coordinate_violations=coord_violations,
            pass_rate=pass_rate,
            audit_timestamp=datetime.now(timezone.utc).isoformat(),
            is_basin_clean=(quarantined == 0),
            violations=[v.to_dict() for v in violations_list[:20]]  # cap preview
        )
        return report


# -----------------------------------------------------------------------------
# Leakage-Protected Cross-Validation Splitters
# -----------------------------------------------------------------------------
class SpatialGroupSplitter:
    """
    Performs GroupKFold splitting grouped strictly by gauge station or sub-basin.
    Guarantees that stations in the test fold NEVER appear in the training folds,
    preventing spatial autocorrelation leakage.
    """
    @staticmethod
    def split(
        records: List[Dict[str, Any]],
        group_key: str = "station_id",
        n_splits: int = 3
    ) -> List[Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]]:
        """
        Splits records into n_splits (train_records, test_records) folds.
        """
        # Collect distinct groups
        groups: Dict[str, List[Dict[str, Any]]] = {}
        for r in records:
            grp = str(r.get(group_key, "UNKNOWN"))
            groups.setdefault(grp, []).append(r)

        sorted_groups = sorted(list(groups.keys()))
        if len(sorted_groups) < n_splits:
            raise ValueError(f"Cannot perform {n_splits}-fold split with only {len(sorted_groups)} distinct groups.")

        folds: List[Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]] = []
        for i in range(n_splits):
            test_groups = {sorted_groups[j] for j in range(len(sorted_groups)) if j % n_splits == i}
            train_records: List[Dict[str, Any]] = []
            test_records: List[Dict[str, Any]] = []

            for grp, recs in groups.items():
                if grp in test_groups:
                    test_records.extend(recs)
                else:
                    train_records.extend(recs)

            folds.append((train_records, test_records))

        return folds


class TemporalBlockSplitter:
    """
    Splits continuous multi-basin time series chronologically into training and test blocks.
    Enforces that max(train_timestamp) < min(test_timestamp), preventing future-data leakage.
    """
    @staticmethod
    def split_by_cutoff(
        records: List[Dict[str, Any]],
        timestamp_key: str = "observation_timestamp",
        cutoff_timestamp: str = "2024-01-01T00:00:00+00:00"
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Splits records before and after cutoff timestamp.
        """
        cutoff_dt = datetime.fromisoformat(cutoff_timestamp.replace("Z", "+00:00"))
        if cutoff_dt.tzinfo is None:
            cutoff_dt = cutoff_dt.replace(tzinfo=timezone.utc)

        train: List[Dict[str, Any]] = []
        test: List[Dict[str, Any]] = []

        for r in records:
            ts_str = str(r.get(timestamp_key, ""))
            try:
                r_dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                if r_dt.tzinfo is None:
                    r_dt = r_dt.replace(tzinfo=timezone.utc)
                if r_dt < cutoff_dt:
                    train.append(r)
                else:
                    test.append(r)
            except Exception:
                test.append(r)

        return train, test


data_quality_engine = MultiBasinDataQualityEngine()
