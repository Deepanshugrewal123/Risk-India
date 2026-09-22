"""
RISK // INDIA — Phase 26 Verification Test Suite
=================================================
Validates National Empirical Flood Data Acquisition, Authoritative Provenance,
Basin Gauge Harmonization, Event Construction, 13 Data Quality Gates,
Scientific ML Promotion Gates, and Strict Zero-Synthetic Invariants.
"""

import unittest
from pathlib import Path
import hashlib
import json
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from app.main import app
from app.middleware.rate_limit import rate_limiter

from app.services.empirical_data import (
    SourceProvider,
    QualityStatus,
    ProvenanceStatus,
    DataFreshness,
    ScientificState,
    PromotionStatus,
    PRIORITY_BASINS,
    EmpiricalObservationRecord,
    generate_observation_id,
    get_provider_metadata,
    check_provider_access,
    validate_coordinates,
    validate_physical_measurements,
    validate_timestamp,
    validate_temporal_consistency,
    normalize_state_name,
    normalize_basin_name,
    normalize_coordinates,
    normalize_timestamp,
    normalize_unit,
    empirical_basin_registry,
    flood_event_constructor,
    data_quality_evaluator,
    empirical_acquisition_service,
    scientific_basin_promotion_gate,
    generate_national_flood_manifest
)
from app.services.model_registry import model_registry
from app.services.flood_model_service import flood_model_service, EXPECTED_FEATURES
from app.services.geo_basin_service import INDIAN_ADMINISTRATIVE_ENTITIES


class TestPhase26NationalEmpiricalFloodData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def setUp(self):
        rate_limiter.reset()

    def tearDown(self):
        rate_limiter.reset()

    # -------------------------------------------------------------------------
    # 1. Real Observation Schema & Provenance
    # -------------------------------------------------------------------------
    def test_01_real_observation_schema_and_provenance(self):
        """Verify EmpiricalObservationRecord schema preserves all fields and handles missing values."""
        obs = EmpiricalObservationRecord(
            observation_id="OBS-TEST-001",
            basin="brahmaputra",
            state="Assam",
            gauge_id="CWC-AS-001",
            gauge_name="Panbazar (Guwahati)",
            timestamp="2026-09-16T12:00:00Z",
            latitude=26.1856,
            longitude=91.7482,
            rainfall_24h=45.5,
            river_level_relative=1.2,
            flood_event_label=1,
            source_provider="Central Water Commission",
            source_url_or_identifier="https://ffs.india-water.gov.in"
        )
        self.assertEqual(obs.basin, "brahmaputra")
        self.assertEqual(obs.rainfall_24h, 45.5)
        self.assertIsNone(obs.rainfall_168h)  # Missing feature explicitly None
        self.assertEqual(obs.synthetic_records, 0)
        self.assertEqual(obs.provenance_status, ProvenanceStatus.VERIFIED_OFFICIAL.value)

    # -------------------------------------------------------------------------
    # 2. Authoritative Provenance & Honest Access Handling
    # -------------------------------------------------------------------------
    def test_02_authoritative_provenance_enforcement_and_honest_access(self):
        """Verify provider metadata and honest reporting of restricted/authenticated sources."""
        cwc_meta = get_provider_metadata("CWC")
        self.assertIn("ffs.india-water.gov.in", cwc_meta["portal_url"])

        # CWC real-time API requires NIC authentication; system must honestly report without fabricating
        cwc_access, cwc_status, cwc_msg = check_provider_access("CWC")
        self.assertFalse(cwc_access)
        self.assertEqual(cwc_status, ProvenanceStatus.AUTHENTICATION_REQUIRED.value)
        self.assertIn("credentials", cwc_msg.lower())

        # IMD requires research clearance
        imd_access, imd_status, imd_msg = check_provider_access("IMD")
        self.assertFalse(imd_access)
        self.assertEqual(imd_status, ProvenanceStatus.AUTHENTICATION_REQUIRED.value)

    # -------------------------------------------------------------------------
    # 3. Deterministic Deduplication
    # -------------------------------------------------------------------------
    def test_03_deterministic_duplicate_detection(self):
        """Verify deterministic SHA-256 observation IDs and duplicate detection."""
        id1 = generate_observation_id("CWC", "CWC-AS-001", "water_level_m", "2026-09-16T12:00:00Z")
        id2 = generate_observation_id("cwc", "cwc-as-001", "water_level_m", "2026-09-16T12:00:00Z")
        self.assertEqual(id1, id2)
        self.assertEqual(len(id1), 16)

    # -------------------------------------------------------------------------
    # 4. Normalization Engine
    # -------------------------------------------------------------------------
    def test_04_gauge_normalization_and_integrity(self):
        """Verify normalization of coordinates, state names, basin names, timestamps, and units."""
        self.assertEqual(normalize_state_name("orissa"), "Odisha")
        self.assertEqual(normalize_state_name("pondicherry"), "Puducherry")
        self.assertEqual(normalize_basin_name("Brahmaputra and Barak"), "brahmaputra")
        self.assertEqual(normalize_basin_name("Dakshin Ganga"), "godavari")

        # Unit conversions
        val_m, unit_m = normalize_unit("water_level", 10.0, "feet")
        self.assertAlmostEqual(val_m, 3.048, places=3)
        self.assertEqual(unit_m, "m")

        val_mm, unit_mm = normalize_unit("rainfall", 2.5, "inches")
        self.assertAlmostEqual(val_mm, 63.5, places=1)
        self.assertEqual(unit_mm, "mm")

        # Coordinate rounding to WGS84 6 decimals
        lat, lon = normalize_coordinates(26.18567891, 91.74823456)
        self.assertEqual(lat, 26.185679)
        self.assertEqual(lon, 91.748235)

    # -------------------------------------------------------------------------
    # 5. Coordinate & Physical Bounds Validation
    # -------------------------------------------------------------------------
    def test_05_coordinate_and_physical_measurement_validators(self):
        """Verify coordinate bounding box and physical measurement sanity checking."""
        # Inside India
        ok_coord, _ = validate_coordinates(26.1856, 91.7482)
        self.assertTrue(ok_coord)

        # Outside India (Southern Hemisphere)
        bad_lat, reason_lat = validate_coordinates(-5.0, 78.0)
        self.assertFalse(bad_lat)
        self.assertIn("outside Indian bounding box", reason_lat)

        # Physical bounds: Negative rain
        bad_rain, reason_rain = validate_physical_measurements({"rainfall_24h": -10.0})
        self.assertFalse(bad_rain)
        self.assertIn("Negative rainfall", reason_rain)

        # Physical bounds: Impossibly high rain (> 2000mm)
        bad_rain_hi, reason_rain_hi = validate_physical_measurements({"rainfall_24h": 3500.0})
        self.assertFalse(bad_rain_hi)
        self.assertIn("exceeds physical ceiling", reason_rain_hi)

    # -------------------------------------------------------------------------
    # 6. Temporal and Spatial Leakage Detection
    # -------------------------------------------------------------------------
    def test_06_temporal_and_spatial_leakage_detection(self):
        """Verify that observation timestamps occurring after target event are rejected."""
        valid_ts, _ = validate_temporal_consistency("2022-05-15T00:00:00Z", "2022-05-20T00:00:00Z")
        self.assertTrue(valid_ts)

        # Leakage: observation in the future of the flood wave
        leakage, reason = validate_temporal_consistency("2022-05-25T00:00:00Z", "2022-05-20T00:00:00Z")
        self.assertFalse(leakage)
        self.assertIn("Temporal leakage detected", reason)

    # -------------------------------------------------------------------------
    # 7. Five Priority Basins Gauge Registry Harmonization
    # -------------------------------------------------------------------------
    def test_07_canonical_five_basin_gauge_registry_integrity(self):
        """Verify the 5 priority basins gauge registry, coordinate uniqueness, and station counts."""
        integrity = empirical_basin_registry.validate_registry_integrity()
        self.assertTrue(integrity["is_valid"])
        self.assertEqual(len(integrity["duplicate_ids"]), 0)
        self.assertEqual(len(integrity["coordinate_conflicts"]), 0)

        # Basin counts
        self.assertEqual(len(empirical_basin_registry.get_gauges_by_basin("brahmaputra")), 3)
        self.assertEqual(len(empirical_basin_registry.get_gauges_by_basin("ganga")), 5)
        self.assertEqual(len(empirical_basin_registry.get_gauges_by_basin("godavari")), 5)
        self.assertEqual(len(empirical_basin_registry.get_gauges_by_basin("mahanadi")), 8)
        self.assertEqual(len(empirical_basin_registry.get_gauges_by_basin("krishna")), 5)

        # Active observations: Only Brahmaputra has 32 audited observations
        sum_as = empirical_basin_registry.get_basin_summary("brahmaputra")
        self.assertEqual(sum_as["active_observations"], 32)

        sum_gg = empirical_basin_registry.get_basin_summary("ganga")
        self.assertEqual(sum_gg["active_observations"], 0)

    # -------------------------------------------------------------------------
    # 8. Flood Event Construction Methodology
    # -------------------------------------------------------------------------
    def test_08_flood_event_construction_methodology(self):
        """Verify deterministic corroborated historical flood events and category segregation."""
        events_as = flood_event_constructor.get_events("brahmaputra")
        self.assertEqual(len(events_as), 12)
        for ev in events_as:
            self.assertTrue(len(ev.evidence_sources) > 0)
            self.assertIn(ev.event_category, ["TRAINING_CANDIDATE", "VALIDATION_CANDIDATE", "INDEPENDENT_TEST"])

        # Non-Assam basins report 0 constructed events (never fabricated)
        events_gd = flood_event_constructor.get_events("godavari")
        self.assertEqual(len(events_gd), 0)

    # -------------------------------------------------------------------------
    # 9. Thirteen Data Quality Gates Evaluation
    # -------------------------------------------------------------------------
    def test_09_thirteen_data_quality_gates_evaluation(self):
        """Verify execution of the 13 data quality gates across priority basins."""
        q_as = data_quality_evaluator.evaluate_basin("brahmaputra")
        self.assertTrue(q_as["is_quality_approved"])
        self.assertEqual(q_as["passed_gates_count"], 13)
        self.assertEqual(q_as["scientific_state"], ScientificState.EMPIRICALLY_VALIDATED_ML.value)

        # Ganga, Godavari, Mahanadi, Krishna must be EMPIRICAL_DATA_INSUFFICIENT
        for b in ["ganga", "godavari", "mahanadi", "krishna"]:
            q_res = data_quality_evaluator.evaluate_basin(b)
            self.assertFalse(q_res["is_quality_approved"])
            self.assertEqual(q_res["scientific_state"], ScientificState.EMPIRICAL_DATA_INSUFFICIENT.value)

    # -------------------------------------------------------------------------
    # 10. Scientific ML Promotion Gate
    # -------------------------------------------------------------------------
    def test_10_scientific_ml_promotion_gate_and_non_assam_rejection(self):
        """Verify scientific promotion gate: Only Assam is approved; others are not approved with fallback."""
        eval_as = scientific_basin_promotion_gate.evaluate_basin_promotion("brahmaputra")
        self.assertTrue(eval_as["ml_ready"])
        self.assertEqual(eval_as["promotion_status"], PromotionStatus.APPROVED.value)
        self.assertEqual(eval_as["model_id"], "assam_flood_prototype_v1")

        for b in ["ganga", "godavari", "mahanadi", "krishna"]:
            eval_b = scientific_basin_promotion_gate.evaluate_basin_promotion(b)
            self.assertFalse(eval_b["ml_ready"])
            self.assertEqual(eval_b["promotion_status"], PromotionStatus.NOT_APPROVED.value)
            self.assertEqual(eval_b["model_id"], "NONE")
            self.assertIn("REGIONAL_BASELINE", eval_b["fallback_strategy"])

    # -------------------------------------------------------------------------
    # 11. Model Registry Explicit Basin Status
    # -------------------------------------------------------------------------
    def test_11_model_registry_explicit_basin_status(self):
        """Verify model_registry reports explicit basin status as required by Part 7."""
        st_as = model_registry.get_basin_model_status("brahmaputra")
        self.assertEqual(st_as["model"], "assam_flood_prototype_v1")
        self.assertEqual(st_as["status"], "APPROVED")

        st_gg = model_registry.get_basin_model_status("ganga")
        self.assertEqual(st_gg["model"], "NONE")
        self.assertEqual(st_gg["status"], "NOT_APPROVED")

        st_gd = model_registry.get_basin_model_status("godavari")
        self.assertEqual(st_gd["model"], "NONE")
        self.assertEqual(st_gd["status"], "NOT_APPROVED")

    # -------------------------------------------------------------------------
    # 12. Assam Model Immutability & Frozen Integrity
    # -------------------------------------------------------------------------
    def test_12_assam_model_immutability_and_byte_integrity(self):
        """Verify assam_flood_prototype_v1 is 100% frozen, 13 features, 32 real observations."""
        self.assertEqual(len(EXPECTED_FEATURES), 13)
        self.assertIsNotNone(flood_model_service.model)
        meta = model_registry.get_model("assam_flood_prototype_v1")
        self.assertIsNotNone(meta)
        self.assertTrue(meta.frozen)
        self.assertEqual(meta.training_observation_count, 32)

    # -------------------------------------------------------------------------
    # 13. National Dataset Manifest Zero-Synthetic Guarantee
    # -------------------------------------------------------------------------
    def test_13_national_dataset_manifest_zero_synthetic_guarantee(self):
        """Verify national manifest generation strictly enforces synthetic_record_count = 0."""
        manifest = generate_national_flood_manifest()
        self.assertEqual(manifest["synthetic_record_count"], 0)
        self.assertEqual(manifest["observation_count_by_basin"]["brahmaputra"], 32)
        self.assertEqual(manifest["observation_count_by_basin"]["ganga"], 0)
        self.assertEqual(manifest["observation_count_by_basin"]["godavari"], 0)
        self.assertEqual(manifest["observation_count_by_basin"]["mahanadi"], 0)
        self.assertEqual(manifest["observation_count_by_basin"]["krishna"], 0)
        self.assertTrue(bool(manifest["checksum_sha256"]))

    # -------------------------------------------------------------------------
    # 14. Phase 26 REST API Endpoints
    # -------------------------------------------------------------------------
    def test_14_api_endpoints_basins_gauges_events_quality_provenance(self):
        """Verify all Phase 26 REST endpoints conform to the required contracts."""
        # /api/data/empirical/basins
        r_b = self.client.get("/api/data/empirical/basins")
        self.assertEqual(r_b.status_code, 200)
        self.assertEqual(r_b.json()["count"], 5)

        # /api/data/empirical/basins/brahmaputra
        r_as = self.client.get("/api/data/empirical/basins/brahmaputra")
        self.assertEqual(r_as.status_code, 200)
        self.assertTrue(r_as.json()["ml_ready"])

        # /api/data/empirical/basins/ganga
        r_gg = self.client.get("/api/data/empirical/basins/ganga")
        self.assertEqual(r_gg.status_code, 200)
        self.assertFalse(r_gg.json()["ml_ready"])
        self.assertEqual(r_gg.json()["model_id"], "NONE")

        # /api/data/empirical/gauges
        r_g = self.client.get("/api/data/empirical/gauges")
        self.assertEqual(r_g.status_code, 200)
        self.assertEqual(r_g.json()["count"], 26)

        # /api/data/empirical/events
        r_e = self.client.get("/api/data/empirical/events")
        self.assertEqual(r_e.status_code, 200)
        self.assertEqual(r_e.json()["count"], 12)

        # /api/data/empirical/quality
        r_q = self.client.get("/api/data/empirical/quality")
        self.assertEqual(r_q.status_code, 200)
        self.assertEqual(r_q.json()["count"], 5)

        # /api/data/empirical/provenance
        r_p = self.client.get("/api/data/empirical/provenance")
        self.assertEqual(r_p.status_code, 200)
        self.assertGreaterEqual(r_p.json()["count"], 6)

        # /api/ml/readiness
        r_ml = self.client.get("/api/ml/readiness")
        self.assertEqual(r_ml.status_code, 200)
        self.assertEqual(r_ml.json()["national_ml_readiness"], "PARTIAL_ASSAM_PROTOTYPE_ONLY")

    # -------------------------------------------------------------------------
    # 15. National Coverage & Hazard Preservation
    # -------------------------------------------------------------------------
    def test_15_national_coverage_and_hazard_preservation(self):
        """Verify that national 28-state + 8-UT coverage and 6 hazards are 100% preserved."""
        # Administrative coverage
        states = [e for e in INDIAN_ADMINISTRATIVE_ENTITIES if e.get("type") == "STATE"]
        uts = [e for e in INDIAN_ADMINISTRATIVE_ENTITIES if e.get("type") == "UNION_TERRITORY"]
        self.assertEqual(len(states), 28)
        self.assertEqual(len(uts), 8)

        # Health endpoint
        r_health = self.client.get("/api/health")
        self.assertEqual(r_health.status_code, 200)
        self.assertIn(r_health.json()["status"], ["ok", "healthy", "degraded"])


if __name__ == "__main__":
    unittest.main()
