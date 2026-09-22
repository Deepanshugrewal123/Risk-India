"""
RISK // INDIA — PHASE 30C VERIFICATION SUITE
=============================================
Dynamic Catchment Telemetry Stream & Hydrological Sensor Ingestion.
30 test cases validating schemas, deterministic hierarchical mapping,
unit conversions, 13 quality rejection rules, deduplication, out-of-order handling,
decoupled freshness, provider circuit breakers, REST API endpoints, and scientific invariants.
"""

import unittest
import hashlib
import time
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from starlette.testclient import TestClient
from app.main import app
from app.services.telemetry import (
    dynamic_telemetry_service,
    catchment_gauge_registry,
    unit_normalization_engine,
    telemetry_quality_engine,
    temporal_telemetry_manager,
    hydrological_provider_client,
    VariableType,
    QualityRejectionReason,
    ObservationQualityStatus,
    DataFreshness,
    GaugeStatus,
    generate_observation_id
)
from app.services.future_risk import (
    future_risk_service,
    future_risk_engine,
    assemble_region_forecast_dataset
)
from app.services.disaster_provider import CircuitState


class TestPhase30CDynamicTelemetry(unittest.TestCase):
    """30-dimension verification suite for Phase 30C dynamic telemetry."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        # Clear temporal store for clean test environment
        temporal_telemetry_manager.clear()

    def setUp(self):
        # Ensure clean state before each test
        for p in hydrological_provider_client.PROVIDERS:
            hydrological_provider_client.reset_circuit(p)

    # -------------------------------------------------------------------------
    # 1. Deterministic Catchment Gauge Normalization
    # -------------------------------------------------------------------------
    def test_01_canonical_gauge_mapping(self):
        """Verifies GAUGE -> RIVER -> CATCHMENT -> MAJOR BASIN -> STATE/UT routing."""
        # Bhadrachalam
        bhadra = catchment_gauge_registry.get_gauge("CWC-GD-001")
        self.assertIsNotNone(bhadra)
        self.assertEqual(bhadra.river_name, "Godavari")
        self.assertEqual(bhadra.sub_basin, "pranhita_catchment")
        self.assertEqual(bhadra.basin_id, "godavari")
        self.assertEqual(bhadra.state, "Telangana")
        self.assertEqual(bhadra.status, GaugeStatus.ACTIVE_CALIBRATED.value)

        # Hirakud
        hirakud = catchment_gauge_registry.get_gauge("CWC-MH-001")
        self.assertIsNotNone(hirakud)
        self.assertEqual(hirakud.river_name, "Mahanadi")
        self.assertEqual(hirakud.basin_id, "mahanadi")
        self.assertEqual(hirakud.state, "Odisha")

        # Dhansirighat
        dhansiri = catchment_gauge_registry.get_gauge("CWC-BP-001")
        self.assertIsNotNone(dhansiri)
        self.assertEqual(dhansiri.basin_id, "brahmaputra")
        self.assertEqual(dhansiri.state, "Assam")

        # Haridwar
        haridwar = catchment_gauge_registry.get_gauge("CWC-GG-001")
        self.assertIsNotNone(haridwar)
        self.assertEqual(haridwar.basin_id, "ganga")
        self.assertEqual(haridwar.state, "Uttarakhand")

        # Almatti
        almatti = catchment_gauge_registry.get_gauge("CWC-KR-001")
        self.assertIsNotNone(almatti)
        self.assertEqual(almatti.basin_id, "krishna")
        self.assertEqual(almatti.state, "Karnataka")

    def test_02_unmapped_gauge_handling(self):
        """Verifies unknown gauges receive status UNMAPPED and are never guessed."""
        gauge = catchment_gauge_registry.normalize_or_unmapped("UNKNOWN-GAUGE-999")
        self.assertEqual(gauge.status, GaugeStatus.UNMAPPED.value)
        self.assertEqual(gauge.basin_id, "unmapped")
        self.assertEqual(gauge.sub_basin, "unmapped")
        self.assertEqual(gauge.river_name, "unmapped")
        self.assertEqual(gauge.state, "unmapped")

    # -------------------------------------------------------------------------
    # 2. Normalized Observation Schema & Fields
    # -------------------------------------------------------------------------
    def test_03_normalized_observation_schema(self):
        """Verifies HydrologicalObservation schema compliance and zero synthetic records."""
        now_utc = datetime.now(timezone.utc)
        ts_str = (now_utc - timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
        obs, reason = dynamic_telemetry_service.ingest_observation({
            "gauge_id": "CWC-GD-001",
            "variable_type": "WATER_LEVEL",
            "value": 15.2,
            "unit": "m",
            "observed_at": ts_str,
            "source_provider": "Central Water Commission"
        }, now=now_utc)

        self.assertIsNotNone(obs)
        self.assertIsNone(reason)
        self.assertEqual(obs.gauge_id, "CWC-GD-001")
        self.assertEqual(obs.river_name, "Godavari")
        self.assertEqual(obs.major_basin, "godavari")
        self.assertEqual(obs.state, "Telangana")
        self.assertEqual(obs.variable_type, "WATER_LEVEL")
        self.assertEqual(obs.normalized_unit, "m")
        self.assertEqual(obs.normalized_value, 15.2)
        self.assertEqual(obs.synthetic_records, 0)
        self.assertEqual(obs.freshness, DataFreshness.LIVE.value)
        self.assertIn("warning_level_m", obs.provenance)

    # -------------------------------------------------------------------------
    # 3. Unit Normalizations
    # -------------------------------------------------------------------------
    def test_04_water_level_unit_conversion(self):
        """Tests mathematical conversion of water level (ft -> m, cm -> m, m -> m)."""
        # Feet to meters: 50 ft -> 15.24 m
        rec_ft = unit_normalization_engine.normalize("WATER_LEVEL", 50.0, "ft")
        self.assertEqual(rec_ft.normalized_unit, "m")
        self.assertEqual(rec_ft.normalized_value, 15.24)

        # Centimeters to meters: 1500 cm -> 15.0 m
        rec_cm = unit_normalization_engine.normalize("WATER_LEVEL", 1500.0, "cm")
        self.assertEqual(rec_cm.normalized_unit, "m")
        self.assertEqual(rec_cm.normalized_value, 15.0)

        # Meters identity
        rec_m = unit_normalization_engine.normalize("WATER_LEVEL", 14.5, "m")
        self.assertEqual(rec_m.normalized_unit, "m")
        self.assertEqual(rec_m.normalized_value, 14.5)

    def test_05_rainfall_unit_conversion(self):
        """Tests mathematical conversion of rainfall (inches -> mm, cm -> mm, mm -> mm)."""
        # Inches to mm: 2.0 inches -> 50.8 mm
        rec_in = unit_normalization_engine.normalize("RAINFALL", 2.0, "in")
        self.assertEqual(rec_in.normalized_unit, "mm")
        self.assertEqual(rec_in.normalized_value, 50.8)

        # Centimeters to mm: 7.5 cm -> 75.0 mm
        rec_cm = unit_normalization_engine.normalize("RAINFALL", 7.5, "cm")
        self.assertEqual(rec_cm.normalized_unit, "mm")
        self.assertEqual(rec_cm.normalized_value, 75.0)

        # Millimeters identity
        rec_mm = unit_normalization_engine.normalize("RAINFALL", 85.0, "mm")
        self.assertEqual(rec_mm.normalized_unit, "mm")
        self.assertEqual(rec_mm.normalized_value, 85.0)

    def test_06_discharge_unit_conversion(self):
        """Tests mathematical conversion of discharge (cusec -> m3_s, cumec -> m3_s)."""
        # Cusec (ft3/s) to m3_s: 1000 cusec -> 28.3168 m3_s
        rec_cusec = unit_normalization_engine.normalize("DISCHARGE", 1000.0, "cusec")
        self.assertEqual(rec_cusec.normalized_unit, "m3_s")
        self.assertEqual(rec_cusec.normalized_value, 28.3168)

        # Cumec identity
        rec_cumec = unit_normalization_engine.normalize("DISCHARGE", 500.0, "cumec")
        self.assertEqual(rec_cumec.normalized_unit, "m3_s")
        self.assertEqual(rec_cumec.normalized_value, 500.0)

    def test_07_unknown_unit_rejection(self):
        """Verifies unknown units are strictly rejected without guessing."""
        with self.assertRaises(ValueError) as ctx:
            unit_normalization_engine.normalize("WATER_LEVEL", 10.0, "knots")
        self.assertIn(QualityRejectionReason.UNKNOWN_UNIT.value, str(ctx.exception))

        now_utc = datetime.now(timezone.utc)
        obs, reason = dynamic_telemetry_service.ingest_observation({
            "gauge_id": "CWC-GD-001",
            "variable_type": "WATER_LEVEL",
            "value": 10.0,
            "unit": "unknown_random_unit",
            "observed_at": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_provider": "Central Water Commission"
        }, now=now_utc)
        self.assertIsNone(obs)
        self.assertEqual(reason, QualityRejectionReason.UNKNOWN_UNIT.value)

    # -------------------------------------------------------------------------
    # 4. Data Quality Engine & Rejection Rules
    # -------------------------------------------------------------------------
    def test_08_missing_gauge_id_rejection(self):
        """Gate 1: Missing or blank gauge ID rejected."""
        now_utc = datetime.now(timezone.utc)
        obs, reason = dynamic_telemetry_service.ingest_observation({
            "gauge_id": "   ",
            "variable_type": "WATER_LEVEL",
            "value": 12.0,
            "unit": "m",
            "observed_at": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
        }, now=now_utc)
        self.assertIsNone(obs)
        self.assertEqual(reason, QualityRejectionReason.MISSING_GAUGE_ID.value)

    def test_09_invalid_timestamp_rejection(self):
        """Gate 2: Malformed timestamp rejected."""
        now_utc = datetime.now(timezone.utc)
        obs, reason = dynamic_telemetry_service.ingest_observation({
            "gauge_id": "CWC-GD-001",
            "variable_type": "WATER_LEVEL",
            "value": 12.0,
            "unit": "m",
            "observed_at": "invalid-timestamp-string"
        }, now=now_utc)
        self.assertIsNone(obs)
        self.assertEqual(reason, QualityRejectionReason.INVALID_TIMESTAMP.value)

    def test_10_non_numeric_value_rejection(self):
        """Gate 3: Non-numeric measurements (string, None, bool) rejected."""
        now_utc = datetime.now(timezone.utc)
        for bad_val in ["twelve", None, True, float("nan")]:
            obs, reason = dynamic_telemetry_service.ingest_observation({
                "gauge_id": "CWC-GD-001",
                "variable_type": "WATER_LEVEL",
                "value": bad_val,
                "unit": "m",
                "observed_at": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
            }, now=now_utc)
            self.assertIsNone(obs)
            self.assertEqual(reason, QualityRejectionReason.NON_NUMERIC_VALUE.value)

    def test_11_future_dated_observation_rejection(self):
        """Gate 10: Future dated observation rejected."""
        now_utc = datetime.now(timezone.utc)
        future_ts = (now_utc + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
        obs, reason = dynamic_telemetry_service.ingest_observation({
            "gauge_id": "CWC-GD-001",
            "variable_type": "WATER_LEVEL",
            "value": 12.0,
            "unit": "m",
            "observed_at": future_ts
        }, now=now_utc)
        self.assertIsNone(obs)
        self.assertEqual(reason, QualityRejectionReason.FUTURE_DATED_OBSERVATION.value)

    def test_12_physically_impossible_rainfall_rejection(self):
        """Gate 5: Physically impossible rainfall (< 0 or > 1500mm) rejected."""
        now_utc = datetime.now(timezone.utc)
        # Negative rain
        obs_neg, reason_neg = dynamic_telemetry_service.ingest_observation({
            "gauge_id": "CWC-GD-001",
            "variable_type": "RAINFALL",
            "value": -10.0,
            "unit": "mm",
            "observed_at": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
        }, now=now_utc)
        self.assertIsNone(obs_neg)
        self.assertEqual(reason_neg, QualityRejectionReason.PHYSICALLY_IMPOSSIBLE_VALUE.value)

        # Excessive rain
        obs_hi, reason_hi = dynamic_telemetry_service.ingest_observation({
            "gauge_id": "CWC-GD-001",
            "variable_type": "RAINFALL",
            "value": 2500.0,
            "unit": "mm",
            "observed_at": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
        }, now=now_utc)
        self.assertIsNone(obs_hi)
        self.assertEqual(reason_hi, QualityRejectionReason.PHYSICALLY_IMPOSSIBLE_VALUE.value)

    def test_13_physically_impossible_level_and_discharge_rejection(self):
        """Gate 5: Impossible water levels and discharge rejected."""
        now_utc = datetime.now(timezone.utc)
        # Extreme water level (> 1000m)
        obs, reason = dynamic_telemetry_service.ingest_observation({
            "gauge_id": "CWC-GD-001",
            "variable_type": "WATER_LEVEL",
            "value": 2000.0,
            "unit": "m",
            "observed_at": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
        }, now=now_utc)
        self.assertIsNone(obs)
        self.assertEqual(reason, QualityRejectionReason.PHYSICALLY_IMPOSSIBLE_VALUE.value)

        # Negative discharge
        obs_d, reason_d = dynamic_telemetry_service.ingest_observation({
            "gauge_id": "CWC-GD-001",
            "variable_type": "DISCHARGE",
            "value": -50.0,
            "unit": "cumec",
            "observed_at": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
        }, now=now_utc)
        self.assertIsNone(obs_d)
        self.assertEqual(reason_d, QualityRejectionReason.PHYSICALLY_IMPOSSIBLE_VALUE.value)

    def test_14_out_of_bounds_coordinates_rejection(self):
        """Gate 6: Coordinates outside Indian territory rejected."""
        now_utc = datetime.now(timezone.utc)
        obs, reason = dynamic_telemetry_service.ingest_observation({
            "gauge_id": "CWC-GD-001",
            "variable_type": "WATER_LEVEL",
            "value": 12.0,
            "unit": "m",
            "observed_at": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "latitude": 51.5074,   # London coordinates
            "longitude": -0.1278
        }, now=now_utc)
        self.assertIsNone(obs)
        self.assertEqual(reason, QualityRejectionReason.OUT_OF_BOUNDS_COORDINATES.value)

    def test_15_unverified_geographic_mapping_rejection(self):
        """Gate 7: Observation on unmapped station rejected from ingestion."""
        now_utc = datetime.now(timezone.utc)
        obs, reason = dynamic_telemetry_service.ingest_observation({
            "gauge_id": "UNVERIFIED-GAUGE-X",
            "variable_type": "WATER_LEVEL",
            "value": 12.0,
            "unit": "m",
            "observed_at": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
        }, now=now_utc)
        self.assertIsNone(obs)
        self.assertEqual(reason, QualityRejectionReason.UNVERIFIED_GEOGRAPHIC_MAPPING.value)

    def test_16_synthetic_data_rejection(self):
        """Gate 11: Synthetic records and markers strictly rejected (synthetic_records = 0)."""
        now_utc = datetime.now(timezone.utc)
        ts = (now_utc - timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ")

        # 1. explicit is_synthetic
        obs1, r1 = dynamic_telemetry_service.ingest_observation({
            "gauge_id": "CWC-GD-001",
            "variable_type": "WATER_LEVEL",
            "value": 12.0,
            "unit": "m",
            "observed_at": ts,
            "is_synthetic": True
        }, now=now_utc)
        self.assertIsNone(obs1)
        self.assertEqual(r1, QualityRejectionReason.SYNTHETIC_DATA_REJECTED.value)

        # 2. explicit synthetic_records > 0
        obs2, r2 = dynamic_telemetry_service.ingest_observation({
            "gauge_id": "CWC-GD-001",
            "variable_type": "WATER_LEVEL",
            "value": 12.0,
            "unit": "m",
            "observed_at": ts,
            "synthetic_records": 1
        }, now=now_utc)
        self.assertIsNone(obs2)
        self.assertEqual(r2, QualityRejectionReason.SYNTHETIC_DATA_REJECTED.value)

        # 3. keyword in provider
        obs3, r3 = dynamic_telemetry_service.ingest_observation({
            "gauge_id": "CWC-GD-001",
            "variable_type": "WATER_LEVEL",
            "value": 12.0,
            "unit": "m",
            "observed_at": ts,
            "source_provider": "Mock Synthetic Ingestor"
        }, now=now_utc)
        self.assertIsNone(obs3)
        self.assertEqual(r3, QualityRejectionReason.SYNTHETIC_DATA_REJECTED.value)

    def test_17_all_13_rejection_reasons_covered(self):
        """Verifies that all 13 machine-readable rejection reasons are fully defined in the enum."""
        expected_reasons = {
            "MISSING_GAUGE_ID",
            "INVALID_TIMESTAMP",
            "NON_NUMERIC_VALUE",
            "UNKNOWN_UNIT",
            "PHYSICALLY_IMPOSSIBLE_VALUE",
            "OUT_OF_BOUNDS_COORDINATES",
            "UNVERIFIED_GEOGRAPHIC_MAPPING",
            "DUPLICATE_OBSERVATION",
            "CORRUPTED_PAYLOAD",
            "FUTURE_DATED_OBSERVATION",
            "SYNTHETIC_DATA_REJECTED",
            "STALE_THRESHOLD_EXCEEDED",
            "UNSUPPORTED_VARIABLE"
        }
        enum_values = {e.value for e in QualityRejectionReason}
        self.assertEqual(expected_reasons, enum_values)

    # -------------------------------------------------------------------------
    # 5. Temporal Integrity & Deduplication
    # -------------------------------------------------------------------------
    def test_18_deduplication_via_deterministic_hash(self):
        """Gate 8: Identical observation rejected as duplicate."""
        now_utc = datetime.now(timezone.utc)
        ts = (now_utc - timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ")

        payload = {
            "gauge_id": "CWC-GD-002",
            "variable_type": "WATER_LEVEL",
            "value": 3.2,
            "unit": "m",
            "observed_at": ts,
            "source_provider": "Central Water Commission"
        }
        obs1, r1 = dynamic_telemetry_service.ingest_observation(payload, now=now_utc)
        self.assertIsNotNone(obs1)

        # Immediate repeat
        obs2, r2 = dynamic_telemetry_service.ingest_observation(payload, now=now_utc)
        self.assertIsNone(obs2)
        self.assertEqual(r2, QualityRejectionReason.DUPLICATE_OBSERVATION.value)

    def test_19_out_of_order_and_late_arriving_handling(self):
        """Verifies late-arriving packets are slotted into chronological sequence."""
        now_utc = datetime.now(timezone.utc)
        t1 = (now_utc - timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%SZ")
        t2 = (now_utc - timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
        t_late = (now_utc - timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Ingest t1, then t2
        dynamic_telemetry_service.ingest_observation({
            "gauge_id": "CWC-GD-003",
            "variable_type": "WATER_LEVEL",
            "value": 25.0,
            "unit": "m",
            "observed_at": t1
        }, now=now_utc)

        dynamic_telemetry_service.ingest_observation({
            "gauge_id": "CWC-GD-003",
            "variable_type": "WATER_LEVEL",
            "value": 27.0,
            "unit": "m",
            "observed_at": t2
        }, now=now_utc)

        # Ingest t_late (arrived late, between t1 and t2)
        dynamic_telemetry_service.ingest_observation({
            "gauge_id": "CWC-GD-003",
            "variable_type": "WATER_LEVEL",
            "value": 26.0,
            "unit": "m",
            "observed_at": t_late
        }, now=now_utc)

        # Query series: must be sorted t1, t_late, t2
        series = dynamic_telemetry_service.get_observations(gauge_id="CWC-GD-003", variable_type="WATER_LEVEL")
        self.assertGreaterEqual(len(series), 3)
        timestamps = [s.observed_at for s in series]
        self.assertEqual(timestamps, sorted(timestamps))

    def test_20_separation_of_observed_at_and_ingested_at(self):
        """Verifies observed_at (sensor) and ingested_at (system) are distinct."""
        now_utc = datetime.now(timezone.utc)
        past_ts = (now_utc - timedelta(hours=10)).strftime("%Y-%m-%dT%H:%M:%SZ")

        obs, _ = dynamic_telemetry_service.ingest_observation({
            "gauge_id": "CWC-GD-004",
            "variable_type": "WATER_LEVEL",
            "value": 72.5,
            "unit": "m",
            "observed_at": past_ts
        }, now=now_utc)

        self.assertIsNotNone(obs)
        self.assertEqual(obs.observed_at, past_ts)
        self.assertNotEqual(obs.observed_at, obs.ingested_at)
        self.assertEqual(obs.ingested_at, now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"))

    # -------------------------------------------------------------------------
    # 6. Freshness Decoupling & Severity
    # -------------------------------------------------------------------------
    def test_21_decoupled_freshness_and_severity(self):
        """
        Danger Level exceeded with stale telemetry remains STALE freshness.
        Severity and freshness are strictly orthogonal; high risk never converts STALE to LIVE.
        """
        now_utc = datetime.now(timezone.utc)
        # 30 hours old (stale)
        stale_ts = (now_utc - timedelta(hours=30)).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Ingest water level above Danger Level (Bhadrachalam DL = 16.15m)
        obs, _ = dynamic_telemetry_service.ingest_observation({
            "gauge_id": "CWC-GD-001",
            "variable_type": "WATER_LEVEL",
            "value": 17.50,  # CRITICAL (above DL 16.15m)
            "unit": "m",
            "observed_at": stale_ts
        }, now=now_utc)

        self.assertIsNotNone(obs)
        self.assertGreater(obs.normalized_value, obs.provenance["danger_level_m"])
        # Invariant: Freshness must be STALE, not LIVE!
        self.assertEqual(obs.freshness, DataFreshness.STALE.value)

    # -------------------------------------------------------------------------
    # 7. Provider Resilience & Circuit Breakers
    # -------------------------------------------------------------------------
    def test_22_provider_circuit_breaker_isolation(self):
        """Tripping CWC circuit breaker does not degrade IMD, NRSC, or ASDMA."""
        client = hydrological_provider_client
        # Force trip CWC
        client.force_trip_circuit("CWC")

        status_cwc = client.get_circuit_status("CWC")
        self.assertEqual(status_cwc["state"], CircuitState.OPEN.value)

        # Verify other circuits remain CLOSED
        status_imd = client.get_circuit_status("IMD")
        status_nrsc = client.get_circuit_status("NRSC_BHUVAN")
        status_asdma = client.get_circuit_status("ASDMA")

        self.assertEqual(status_imd["state"], CircuitState.CLOSED.value)
        self.assertEqual(status_nrsc["state"], CircuitState.CLOSED.value)
        self.assertEqual(status_asdma["state"], CircuitState.CLOSED.value)

    def test_23_provider_circuit_breaker_recovery(self):
        """Tests circuit breaker recovery transitions: CLOSED -> OPEN -> HALF_OPEN -> CLOSED."""
        client = hydrological_provider_client
        cb = client._circuit_breakers["IMD"]
        self.assertEqual(cb.state, CircuitState.CLOSED)

        # Trigger failures
        cb.record_failure()
        cb.record_failure()
        cb.record_failure()
        cb.record_failure()
        self.assertEqual(cb.state, CircuitState.OPEN)

        # Simulate cooldown passage
        cb.last_failure_time = datetime.now(timezone.utc) - timedelta(seconds=cb.cooldown_seconds + 5)
        self.assertTrue(cb.can_execute())
        self.assertEqual(cb.state, CircuitState.HALF_OPEN)

        # Successful attempt closes the circuit
        cb.record_success()
        self.assertEqual(cb.state, CircuitState.CLOSED)

    def test_24_in_memory_fallback_resilience(self):
        """Verifies in-memory fallback operates seamlessly without HTTP 500."""
        status = dynamic_telemetry_service.get_status()
        self.assertEqual(status["status"], "OPERATIONAL")
        self.assertEqual(status["backend_storage"], "IN_MEMORY_RESILIENT")

    def test_25_batch_ingestion_summary(self):
        """Tests ingest_batch with mixed valid, duplicate, and invalid payloads."""
        now_utc = datetime.now(timezone.utc)
        t_valid = (now_utc - timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%SZ")

        batch_payload = [
            # Valid 1
            {"gauge_id": "CWC-GD-005", "variable_type": "WATER_LEVEL", "value": 352.0, "unit": "m", "observed_at": t_valid},
            # Valid 2
            {"gauge_id": "CWC-GD-006", "variable_type": "WATER_LEVEL", "value": 98.0, "unit": "m", "observed_at": t_valid},
            # Duplicate of Valid 1
            {"gauge_id": "CWC-GD-005", "variable_type": "WATER_LEVEL", "value": 352.0, "unit": "m", "observed_at": t_valid},
            # Invalid (unknown unit)
            {"gauge_id": "CWC-GD-007", "variable_type": "WATER_LEVEL", "value": 130.0, "unit": "furlongs", "observed_at": t_valid},
            # Invalid (future dated)
            {"gauge_id": "CWC-GD-008", "variable_type": "WATER_LEVEL", "value": 550.0, "unit": "m", "observed_at": "2099-01-01T00:00:00Z"}
        ]

        batch_res = dynamic_telemetry_service.ingest_batch(batch_payload, now=now_utc)
        self.assertEqual(batch_res.total_submitted, 5)
        self.assertEqual(batch_res.accepted_count, 2)
        self.assertEqual(batch_res.deduplicated_count, 1)
        self.assertEqual(batch_res.rejected_count, 2)
        self.assertEqual(len(batch_res.rejections), 3)

    # -------------------------------------------------------------------------
    # 8. REST API Endpoints
    # -------------------------------------------------------------------------
    def test_26_api_telemetry_status(self):
        """GET /api/telemetry/status returns operational metrics and circuit states."""
        res = self.client.get("/api/telemetry/status")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "OPERATIONAL")
        self.assertIn("total_gauges_registered", data)
        self.assertIn("provider_circuits", data)
        self.assertEqual(data["synthetic_records_total"], 0)

    def test_27_api_telemetry_gauges(self):
        """GET /api/telemetry/gauges returns canonical gauge list with filtering."""
        res = self.client.get("/api/telemetry/gauges?basin=godavari")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(data["count"], 8)
        for g in data["gauges"]:
            self.assertEqual(g["basin_id"], "godavari")

    def test_28_api_telemetry_observations(self):
        """GET /api/telemetry/observations returns chronological telemetry stream."""
        res = self.client.get("/api/telemetry/observations?limit=50")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("observations", data)
        self.assertIsInstance(data["observations"], list)

    def test_29_api_telemetry_readiness(self):
        """GET /api/telemetry/readiness returns basin-by-basin telemetry readiness."""
        res = self.client.get("/api/telemetry/readiness")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["probe_name"], "NATIONAL_BASIN_TELEMETRY_READINESS")
        self.assertEqual(data["basins_audited"], 5)
        basin_ids = [b["basin_id"] for b in data["basin_readiness"]]
        self.assertIn("brahmaputra", basin_ids)
        self.assertIn("godavari", basin_ids)
        self.assertIn("mahanadi", basin_ids)
        self.assertIn("krishna", basin_ids)
        self.assertIn("ganga", basin_ids)

    # -------------------------------------------------------------------------
    # 9. Future-Risk Engine Boundary & Scientific Invariants
    # -------------------------------------------------------------------------
    def test_30_future_risk_integration_and_invariants(self):
        """
        Verifies:
        1. Dynamic telemetry stream integrates into HydrologicalVariable.
        2. Non-Assam ML guard is strictly preserved (ml_available = False).
        3. Model and dataset SHA-256 byte invariance is strictly preserved.
        """
        # Test future risk assessment for Telangana (Godavari basin)
        assessments = future_risk_engine.evaluate_future_risk(state_identifier="Telangana", hazard="FLOOD")
        self.assertTrue(len(assessments) > 0)
        telangana_rec = assessments[0]
        # Telangana must not claim ML prediction
        self.assertIn("not currently validated", telangana_rec.ml_scope_note.lower())
        self.assertNotEqual(telangana_rec.methodology, "EMPIRICAL_ML")

        # Ingest telemetry for Godavari station
        now_utc = datetime.now(timezone.utc)
        dynamic_telemetry_service.ingest_observation({
            "gauge_id": "CWC-GD-001",
            "variable_type": "WATER_LEVEL",
            "value": 15.5,
            "unit": "m",
            "observed_at": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
        }, now=now_utc)

        # Verify forecast contracts ingest this dynamic telemetry
        dataset = assemble_region_forecast_dataset("Telangana")
        self.assertIsNotNone(dataset.hydrology.river_level_m)
        self.assertEqual(dataset.hydrology.river_level_m, 15.5)
        self.assertEqual(dataset.hydrology.metadata.provider, "CWC_DYNAMIC_TELEMETRY")

        # Byte-for-byte model invariant
        with open("ml/flood/artifacts/model.joblib", "rb") as f:
            model_hash = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(
            model_hash,
            "0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf",
            "Model artifact SHA-256 hash was altered!"
        )

        # Byte-for-byte dataset invariant
        with open("datasets/processed/flood_assam/flood_features.csv", "rb") as f:
            data_hash = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(
            data_hash,
            "88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080",
            "Assam training dataset SHA-256 hash was altered!"
        )


if __name__ == "__main__":
    unittest.main()
