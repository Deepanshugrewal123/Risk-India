"""
RISK // INDIA — Central Dynamic Catchment Telemetry Service
===========================================================
Unified facade for real-time hydrological sensor ingestion, caching,
orthogonal freshness computation, and downstream risk engine feeds.
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone
import logging
import threading
import uuid

from .schema import (
    HydrologicalObservation,
    TelemetryIngestionBatch,
    CanonicalGauge,
    QualityRejectionReason,
    ObservationQualityStatus,
    DataFreshness,
    GaugeStatus,
    generate_observation_id
)
from .gauge_registry import catchment_gauge_registry
from .unit_normalizer import unit_normalization_engine
from .quality_engine import telemetry_quality_engine
from .temporal_manager import temporal_telemetry_manager
from .provider_client import hydrological_provider_client

logger = logging.getLogger("dynamic-telemetry-service")


class DynamicCatchmentTelemetryService:
    """
    Coordinates ingestion, quality gating, storage, and retrieval of hydrological telemetry.
    Maintains complete isolation between Freshness and Severity.
    """

    def __init__(self):
        self._lock = threading.RLock()
        self._registry = catchment_gauge_registry
        self._unit_normalizer = unit_normalization_engine
        self._quality_engine = telemetry_quality_engine
        self._temporal = temporal_telemetry_manager
        self._providers = hydrological_provider_client
        self._backend_storage = "IN_MEMORY_RESILIENT"

    def calculate_freshness(self, observed_at_iso: str, now: Optional[datetime] = None) -> str:
        """
        Computes freshness strictly from observation timestamp:
        - LIVE: < 1 hour (< 3600s)
        - RECENT: < 24 hours (< 86400s)
        - STALE: >= 24 hours
        Orthogonal to severity: extreme river stage with old timestamp remains STALE.
        """
        if not observed_at_iso:
            return DataFreshness.UNAVAILABLE.value
        try:
            dt = datetime.fromisoformat(observed_at_iso.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)
        except Exception:
            return DataFreshness.UNAVAILABLE.value

        current = now or datetime.now(timezone.utc)
        delta_seconds = (current - dt).total_seconds()

        if delta_seconds < 3600:
            return DataFreshness.LIVE.value
        elif delta_seconds < 86400:
            return DataFreshness.RECENT.value
        else:
            return DataFreshness.STALE.value

    def ingest_observation(
        self,
        raw_payload: Dict[str, Any],
        now: Optional[datetime] = None
    ) -> Tuple[Optional[HydrologicalObservation], Optional[str]]:
        """
        Ingests a single hydrological observation through the 13 quality gates.
        Returns (observation, rejection_reason).
        """
        current_time = now or datetime.now(timezone.utc)
        ingested_at = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Gate 9: Payload structure
        ok, reason = self._quality_engine.validate_payload_structure(raw_payload)
        if not ok:
            return None, reason

        # Gate 11: Synthetic data rejection
        ok, reason = self._quality_engine.validate_synthetic_data(raw_payload)
        if not ok:
            return None, reason

        # Gate 1: Gauge ID
        gauge_id = raw_payload.get("gauge_id")
        ok, reason = self._quality_engine.validate_gauge_id(gauge_id)
        if not ok:
            return None, reason

        # Gate 13: Variable type
        var_type = raw_payload.get("variable_type")
        ok, reason = self._quality_engine.validate_variable_type(var_type)
        if not ok:
            return None, reason
        var_type = var_type.strip().upper()

        # Gate 3: Numeric value
        raw_val = raw_payload.get("value")
        ok, num_val, reason = self._quality_engine.validate_numeric_value(raw_val)
        if not ok:
            return None, reason

        # Gate 4: Unit & Conversion
        unit_str = raw_payload.get("unit")
        try:
            conversion = self._unit_normalizer.normalize(var_type, num_val, unit_str)
        except ValueError as ve:
            err_msg = str(ve)
            if QualityRejectionReason.UNKNOWN_UNIT.value in err_msg:
                return None, QualityRejectionReason.UNKNOWN_UNIT.value
            elif QualityRejectionReason.UNSUPPORTED_VARIABLE.value in err_msg:
                return None, QualityRejectionReason.UNSUPPORTED_VARIABLE.value
            return None, QualityRejectionReason.UNKNOWN_UNIT.value

        # Gate 5: Physical limits
        ok, reason = self._quality_engine.validate_physical_limits(var_type, conversion.normalized_value)
        if not ok:
            return None, reason

        # Gate 2, 10, 12: Timestamp validity, future date, staleness
        raw_ts = raw_payload.get("observed_at")
        ok, valid_ts, reason = self._quality_engine.validate_timestamp(raw_ts, current_time)
        if not ok:
            return None, reason

        # Gauge Resolution & Gate 7: Geographic mapping
        gauge = self._registry.normalize_or_unmapped(gauge_id, raw_payload)
        ok, reason = self._quality_engine.validate_geographic_mapping(gauge)
        if not ok:
            return None, reason

        # Gate 6: Coordinate bounds
        lat = raw_payload.get("latitude", gauge.latitude)
        lon = raw_payload.get("longitude", gauge.longitude)
        ok, reason = self._quality_engine.validate_coordinates(lat, lon)
        if not ok:
            return None, reason

        # Provenance and Metadata
        provider = raw_payload.get("source_provider", gauge.agency or "Central Water Commission")
        source_id = raw_payload.get("source_identifier", f"{provider}:{gauge.station_id}")
        freshness_val = self.calculate_freshness(valid_ts, current_time)
        obs_id = generate_observation_id(provider, gauge.station_id, var_type, valid_ts)

        obs = HydrologicalObservation(
            observation_id=obs_id,
            gauge_id=gauge.station_id,
            gauge_name=gauge.station_name,
            river_name=gauge.river_name,
            catchment=gauge.sub_basin,
            major_basin=gauge.basin_id,
            state=gauge.state,
            district=gauge.district,
            latitude=round(float(lat), 6),
            longitude=round(float(lon), 6),
            observed_at=valid_ts,
            ingested_at=ingested_at,
            variable_type=var_type,
            original_value=conversion.original_value,
            original_unit=conversion.original_unit,
            normalized_value=conversion.normalized_value,
            normalized_unit=conversion.normalized_unit,
            conversion_rule=conversion.conversion_rule,
            source_provider=provider,
            source_identifier=source_id,
            quality_status=ObservationQualityStatus.VALIDATED.value,
            rejection_reasons=[],
            freshness=freshness_val,
            synthetic_records=0,    # Strictly 0
            provenance={
                "ingestion_method": "DYNAMIC_TELEMETRY_STREAM",
                "authority": gauge.agency,
                "warning_level_m": gauge.warning_level_m,
                "danger_level_m": gauge.danger_level_m,
                "zero_datum_m": gauge.zero_datum_m,
                "status": gauge.status
            }
        )

        # Gate 8 & Temporal Ordering
        ok, reason = self._temporal.add_observation(obs)
        if not ok:
            return None, reason

        return obs, None

    def ingest_batch(
        self,
        records: List[Dict[str, Any]],
        now: Optional[datetime] = None
    ) -> TelemetryIngestionBatch:
        """Processes an array of observation dictionaries, tracking statistics."""
        batch_id = str(uuid.uuid4())[:8]
        current_time = now or datetime.now(timezone.utc)
        accepted = 0
        rejected = 0
        deduped = 0
        rejections_list: List[Dict[str, Any]] = []

        for item in records:
            obs, reason = self.ingest_observation(item, current_time)
            if obs:
                accepted += 1
            else:
                if reason == QualityRejectionReason.DUPLICATE_OBSERVATION.value:
                    deduped += 1
                else:
                    rejected += 1
                rejections_list.append({
                    "gauge_id": item.get("gauge_id") if isinstance(item, dict) else "unknown",
                    "reason": reason
                })

        return TelemetryIngestionBatch(
            batch_id=batch_id,
            total_submitted=len(records),
            accepted_count=accepted,
            rejected_count=rejected,
            deduplicated_count=deduped,
            rejections=rejections_list,
            ingested_at=current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        )

    def get_observations(
        self,
        gauge_id: Optional[str] = None,
        basin: Optional[str] = None,
        state: Optional[str] = None,
        variable_type: Optional[str] = None,
        limit: int = 100
    ) -> List[HydrologicalObservation]:
        """Queries observations filtered by station, basin, state, and variable."""
        with self._lock:
            all_gauges = self._registry.get_all_gauges()
            target_gauge_ids = set()

            if gauge_id:
                target_gauge_ids.add(gauge_id.strip().upper())
            else:
                for g in all_gauges:
                    if basin and g.basin_id.lower() != basin.strip().lower():
                        continue
                    if state and state.strip().lower() not in g.state.lower():
                        continue
                    target_gauge_ids.add(g.station_id)

            results: List[HydrologicalObservation] = []
            for gid in target_gauge_ids:
                series = self._temporal.get_series(gid, variable_type, limit=limit)
                results.extend(series)

            results.sort(key=lambda x: x.observed_at)
            return results[-limit:] if limit else results

    def get_latest_observation(
        self,
        gauge_id: str,
        variable_type: Optional[str] = None
    ) -> Optional[HydrologicalObservation]:
        return self._temporal.get_latest(gauge_id, variable_type)

    def get_gauges(
        self,
        basin: Optional[str] = None,
        state: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Returns registered canonical gauges with filtering."""
        gauges = self._registry.get_all_gauges()
        if basin:
            gauges = [g for g in gauges if g.basin_id.lower() == basin.strip().lower()]
        if state:
            gauges = [g for g in gauges if state.strip().lower() in g.state.lower()]
        if status:
            gauges = [g for g in gauges if g.status.lower() == status.strip().lower()]
        return [g.to_dict() for g in gauges]

    def get_status(self) -> Dict[str, Any]:
        """Provides operational metrics for the telemetry ingestion subsystem."""
        with self._lock:
            total_obs = self._temporal.get_total_count()
            circuits = self._providers.get_all_circuit_statuses()
            gauges = self._registry.get_all_gauges()

            # Freshness breakdown across latest observations
            live_count = 0
            recent_count = 0
            stale_count = 0
            for g in gauges:
                latest = self._temporal.get_latest(g.station_id)
                if latest:
                    f = self.calculate_freshness(latest.observed_at)
                    if f == DataFreshness.LIVE.value:
                        live_count += 1
                    elif f == DataFreshness.RECENT.value:
                        recent_count += 1
                    else:
                        stale_count += 1

            return {
                "status": "OPERATIONAL",
                "subsystem": "DYNAMIC_CATCHMENT_TELEMETRY",
                "backend_storage": self._backend_storage,
                "total_gauges_registered": len(gauges),
                "total_observations_ingested": total_obs,
                "synthetic_records_total": 0,    # Invariant: 0
                "active_feed_freshness": {
                    "live_gauges": live_count,
                    "recent_gauges": recent_count,
                    "stale_gauges": stale_count
                },
                "provider_circuits": circuits,
                "timestamp_utc": datetime.now(timezone.utc).isoformat()
            }

    def get_readiness(self) -> Dict[str, Any]:
        """
        Basin-by-basin empirical telemetry readiness probe.
        Evaluates observational density, verified gauge count, and freshness.
        """
        basins = ["brahmaputra", "ganga", "godavari", "mahanadi", "krishna"]
        basin_reports = []

        for b in basins:
            gauges = self._registry.get_gauges_by_basin(b)
            total_g = len(gauges)
            obs = self.get_observations(basin=b, limit=500)
            active_g = len({o.gauge_id for o in obs})

            # Assam/Brahmaputra has active approved empirical model; others are telemetry-ready
            is_assam = (b == "brahmaputra")
            status = "EMPIRICAL_TELEMETRY_STREAMING" if active_g > 0 else "REGISTERED_STATIONS_AWAITING_INGESTION"

            basin_reports.append({
                "basin_id": b,
                "registered_gauges": total_g,
                "active_streaming_gauges": active_g,
                "total_observations": len(obs),
                "sub_basins_monitored": sorted(list({g.sub_basin for g in gauges})),
                "states_covered": sorted(list({g.state for g in gauges})),
                "telemetry_readiness_status": status,
                "ml_model_status": "APPROVED_PROTOTYPE_v1" if is_assam else "ML_NOT_APPROVED_INSUFFICIENT_EVENTS",
                "synthetic_records": 0
            })

        return {
            "probe_name": "NATIONAL_BASIN_TELEMETRY_READINESS",
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
            "basins_audited": len(basins),
            "basin_readiness": basin_reports
        }


dynamic_telemetry_service = DynamicCatchmentTelemetryService()
