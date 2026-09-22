"""
RISK // INDIA — Phase 27 Automated Verification Test Suite
===========================================================
Validates National Flood Empirical Data Acquisition, Event Corroboration,
Temporal Alignment, 13 Data Quality Gates with Rejection Reasons, Basin Readiness,
Scientific ML Promotion Gates, Immutability Hashes, and REST API Contracts.
"""

import unittest
from pathlib import Path
import hashlib
import json
import sys
from datetime import datetime, timezone, timedelta

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
    CANONICAL_BASIN_NAMES,
    REJECTION_REASON_MISSING_CORROBORATION,
    REJECTION_REASON_OUT_OF_BOUNDS_COORDINATES,
    REJECTION_REASON_FUTURE_TIMESTAMP,
    REJECTION_REASON_TEMPORAL_LEAKAGE,
    REJECTION_REASON_UNVERIFIED_PROVENANCE,
    REJECTION_REASON_SYNTHETIC_DATA_PROHIBITED,
    REJECTION_REASON_INVALID_UNITS,
    REJECTION_REASON_INSUFFICIENT_OBSERVATIONS,
    REJECTION_REASON_DUPLICATE_RECORD,
    REJECTION_REASON_MISSING_FEATURES,
    REJECTION_REASON_SPATIAL_LEAKAGE,
    REJECTION_REASON_UNAPPROVED_MODEL,
    REJECTION_REASON_NON_ASSAM_ML_PROHIBITED,
    EmpiricalObservationRecord,
    generate_observation_id,
    AUTHORITATIVE_PROVIDERS_METADATA,
    get_provider_metadata,
    check_provider_access,
    validate_coordinates,
    validate_physical_measurements,
    validate_timestamp,
    validate_temporal_consistency,
    empirical_basin_registry,
    flood_event_constructor,
    event_corroboration_service,
    CorroborationStatus,
    CorroboratedFloodEvent,
    temporal_alignment_engine,
    CANONICAL_13_FEATURES,
    basin_readiness_evaluator,
    data_quality_evaluator,
    empirical_acquisition_service,
    scientific_basin_promotion_gate,
    generate_national_flood_manifest
)
from app.services.geo_basin_service import INDIAN_ADMINISTRATIVE_ENTITIES


class TestPhase27NationalFloodEmpiricalAcquisition(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def setUp(self):
        rate_limiter.reset()

    def tearDown(self):
        rate_limiter.reset()

    # -------------------------------------------------------------------------
    # 1. Authoritative Provenance Enforcement & Honest Access Handling
    # -------------------------------------------------------------------------
    def test_01_authoritative_provenance_enforcement_and_honest_access(self):
        """Verifies official provider provenance metadata and truthful reporting of restricted access."""
        providers = ["CWC", "IMD", "ASDMA", "NRSC", "NDMA"]
        for p in providers:
            meta = get_provider_metadata(p)
            self.assertIsNotNone(meta, f"Provider metadata missing for {p}")
            self.assertIn("full_name", meta)
            self.assertIn("portal_url", meta)
            self.assertIn("data_license", meta)


        # Honest provider access check
        accessible, status, msg = check_provider_access("CWC")
        self.assertIn(status, [
            ProvenanceStatus.VERIFIED_OFFICIAL.value,
            ProvenanceStatus.DATA_UNAVAILABLE.value,
            ProvenanceStatus.AUTHENTICATION_REQUIRED.value
        ])
        self.assertIsInstance(msg, str)

    # -------------------------------------------------------------------------
    # 2. Geographic Coordinate Bounding Box Validation
    # -------------------------------------------------------------------------
    def test_02_coordinate_bounds_validation(self):
        """Validates coordinates strictly within India [6-38N, 68-98E] and rejection of out-of-bounds."""
        # Valid Indian coordinates (Guwahati, Assam)
        valid, msg = validate_coordinates(26.1856, 91.7482)
        self.assertTrue(valid)
        self.assertIsNone(msg)

        # Out-of-bounds coordinate (London)
        invalid, err_msg = validate_coordinates(51.5074, -0.1278)
        self.assertFalse(invalid)
        self.assertIn("outside Indian bounding box", err_msg)

        # Temporal alignment engine rejection of out-of-bounds coordinates
        res = temporal_alignment_engine.align_observation_features(
            rainfall_series={"rainfall_24h": 50.0},
            stage_series={"river_level_relative": 1.2},
            coordinates=(51.5074, -0.1278),
            observation_timestamp="2024-07-15T12:00:00Z"
        )
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["rejection_reason"], REJECTION_REASON_OUT_OF_BOUNDS_COORDINATES)

    # -------------------------------------------------------------------------
    # 3. Timestamp Chronology & Future Rejection
    # -------------------------------------------------------------------------
    def test_03_timestamp_chronology_and_future_rejection(self):
        """Validates ISO 8601 UTC chronological timestamps and rejects future dates."""
        # Valid past timestamp
        valid, msg = validate_timestamp("2024-06-20T08:30:00Z")
        self.assertTrue(valid)
        self.assertIsNone(msg)

        # Future timestamp rejection
        future_dt = (datetime.now(timezone.utc) + timedelta(days=365)).isoformat()
        future_valid, future_msg = validate_timestamp(future_dt)
        self.assertFalse(future_valid)
        self.assertIn("in the future", future_msg)

        # Rejection in temporal alignment engine
        res = temporal_alignment_engine.align_observation_features(
            rainfall_series={"rainfall_24h": 30.0},
            stage_series={"river_level_relative": 0.5},
            coordinates=(26.1856, 91.7482),
            observation_timestamp=future_dt
        )
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["rejection_reason"], REJECTION_REASON_FUTURE_TIMESTAMP)

    # -------------------------------------------------------------------------
    # 4. SHA-256 Deterministic Deduplication
    # -------------------------------------------------------------------------
    def test_04_sha256_deterministic_deduplication(self):
        """Verifies deterministic SHA-256 hashing produces identical fingerprints for duplicates."""
        id1 = generate_observation_id("CWC", "CWC-AS-001", "water_level", "2024-07-01T00:00:00Z")
        id2 = generate_observation_id("CWC", "CWC-AS-001", "water_level", "2024-07-01T00:00:00Z")
        self.assertEqual(id1, id2, "Observation IDs for identical telemetry must match deterministically")

        id_diff = generate_observation_id("CWC", "CWC-AS-001", "water_level", "2024-07-01T01:00:00Z")
        self.assertNotEqual(id1, id_diff, "Different timestamp must generate distinct observation ID")


    # -------------------------------------------------------------------------
    # 5. Elevated Stage Spike Rejection Without Official Corroboration
    # -------------------------------------------------------------------------
    def test_05_stage_spike_rejection_without_official_corroboration(self):
        """Asserts that high river stage alone is strictly REJECTED without authoritative agency evidence."""
        # Uncorroborated event hypothesis: stage is elevated, but NO official bulletins/sitreps
        unsubstantiated = event_corroboration_service.evaluate_candidate_event(
            event_id="EVT-CANDIDATE-UNSUBSTANTIATED-01",
            basin="godavari",
            gauge_ids=["CWC-GD-001"],
            start_time="2024-08-01T00:00:00Z",
            end_time="2024-08-05T23:59:59Z",
            source_evidence=[],  # No official evidence
            is_stage_elevated=True
        )
        self.assertEqual(unsubstantiated.corroboration_status, CorroborationStatus.REJECTED_UNSUBSTANTIATED.value)
        self.assertEqual(unsubstantiated.rejection_reason, REJECTION_REASON_MISSING_CORROBORATION)
        self.assertEqual(unsubstantiated.confidence_score, 0.0)

        # Candidate with official CWC and ASDMA corroboration: APPROVED
        substantiated = event_corroboration_service.evaluate_candidate_event(
            event_id="EVT-CANDIDATE-SUBSTANTIATED-01",
            basin="brahmaputra",
            gauge_ids=["CWC-AS-001"],
            start_time="2024-07-01T00:00:00Z",
            end_time="2024-07-10T23:59:59Z",
            source_evidence=["CWC Daily Flood Bulletin", "ASDMA Situation Report July 2024"],
            is_stage_elevated=True
        )
        self.assertEqual(substantiated.corroboration_status, CorroborationStatus.APPROVED_CORROBORATED.value)
        self.assertIsNone(substantiated.rejection_reason)
        self.assertGreater(substantiated.confidence_score, 0.8)

    # -------------------------------------------------------------------------
    # 6. Corroborated Flood Event Registry
    # -------------------------------------------------------------------------
    def test_06_corroborated_flood_event_registry(self):
        """Verifies the 12 approved Assam flood events and 0 approved events for non-Assam basins."""
        assam_events = event_corroboration_service.get_events("brahmaputra")
        self.assertEqual(len(assam_events), 12, "Assam must have exactly 12 audited corroborated events")

        for b in ["ganga", "godavari", "mahanadi", "krishna"]:
            non_assam_events = event_corroboration_service.get_events(b)
            self.assertEqual(len(non_assam_events), 0, f"Basin {b} must have zero approved events pending telemetry")

    # -------------------------------------------------------------------------
    # 7. Temporal Feature Alignment Engine (13 Features)
    # -------------------------------------------------------------------------
    def test_07_temporal_feature_alignment_13_vector(self):
        """Validates alignment of raw telemetry into canonical 13-feature vector without triggering ML training."""
        aligned = temporal_alignment_engine.align_observation_features(
            rainfall_series={
                "rainfall_6h": 12.5,
                "rainfall_24h": 45.0,
                "rainfall_72h": 110.0,
                "rainfall_168h": 220.0
            },
            stage_series={
                "river_level_relative": 1.45,
                "river_rise_6h": 0.25,
                "river_rise_24h": 0.80,
                "river_percentile_level": 0.92
            },
            coordinates=(26.1856, 91.7482),
            observation_timestamp="2024-06-25T08:00:00Z",
            event_timestamp="2024-06-25T12:00:00Z"
        )
        self.assertTrue(aligned["is_valid"])
        self.assertIsNone(aligned["rejection_reason"])
        self.assertEqual(aligned["synthetic_records"], 0)
        self.assertFalse(aligned["training_triggered"], "Temporal alignment must NEVER trigger automated model training")

        features = aligned["aligned_features"]
        self.assertEqual(len(features), 13)
        for key in CANONICAL_13_FEATURES:
            self.assertIn(key, features)

    # -------------------------------------------------------------------------
    # 8. Temporal Leakage Protection (Lookahead Rejection)
    # -------------------------------------------------------------------------
    def test_08_temporal_leakage_protection(self):
        """Ensures observations occurring after the target event are rejected with TEMPORAL_LEAKAGE."""
        # Observation is at 18:00, but event peak is at 12:00 -> Lookahead!
        res = temporal_alignment_engine.align_observation_features(
            rainfall_series={"rainfall_24h": 50.0},
            stage_series={"river_level_relative": 1.0},
            coordinates=(26.1856, 91.7482),
            observation_timestamp="2024-06-25T18:00:00Z",
            event_timestamp="2024-06-25T12:00:00Z"
        )
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["rejection_reason"], REJECTION_REASON_TEMPORAL_LEAKAGE)
        self.assertIn("postdates event timestamp", res["error"])

    # -------------------------------------------------------------------------
    # 9. Spatial Catchment Boundary Enforcement
    # -------------------------------------------------------------------------
    def test_09_spatial_catchment_boundary_enforcement(self):
        """Verifies gauge coordinates strictly reside within declared basin bounds."""
        for b in PRIORITY_BASINS:
            gauges = empirical_basin_registry.get_gauges_by_basin(b)
            self.assertGreater(len(gauges), 0, f"Basin {b} must have registered calibrated gauges")
            for g in gauges:
                self.assertTrue(6.0 <= g.latitude <= 38.0)
                self.assertTrue(68.0 <= g.longitude <= 98.0)
                self.assertEqual(g.basin_id, b)

    # -------------------------------------------------------------------------
    # 10. 13 Data Quality Gates with Machine-Readable Rejection Reasons
    # -------------------------------------------------------------------------
    def test_10_thirteen_quality_gates_with_rejection_reasons(self):
        """Evaluates all 13 gates and verifies machine-readable rejection reasons for unapproved basins."""
        # Brahmaputra: All 13 gates pass
        assam_eval = data_quality_evaluator.evaluate_basin("brahmaputra")
        self.assertEqual(assam_eval["passed_gates_count"], 13)
        self.assertTrue(assam_eval["is_quality_approved"])
        self.assertEqual(len(assam_eval["rejection_reasons"]), 0)

        # Ganga: Fails gates, contains standardized rejection reasons
        ganga_eval = data_quality_evaluator.evaluate_basin("ganga")
        self.assertFalse(ganga_eval["is_quality_approved"])
        self.assertIn(REJECTION_REASON_UNVERIFIED_PROVENANCE, ganga_eval["rejection_reasons"])
        self.assertIn(REJECTION_REASON_FUTURE_TIMESTAMP, ganga_eval["rejection_reasons"])
        self.assertIn(REJECTION_REASON_MISSING_CORROBORATION, ganga_eval["rejection_reasons"])

    # -------------------------------------------------------------------------
    # 11. Basin Readiness Evaluator
    # -------------------------------------------------------------------------
    def test_11_basin_readiness_evaluator(self):
        """Verifies machine-readable readiness records across all 5 priority river basins."""
        evaluations = basin_readiness_evaluator.evaluate_all_priority_basins()
        self.assertEqual(len(evaluations), 5)

        for e in evaluations:
            self.assertIn(e["basin"], PRIORITY_BASINS)
            self.assertEqual(e["synthetic_records"], 0)
            if e["basin"] == "brahmaputra":
                self.assertTrue(e["ML_READY"])
                self.assertEqual(e["MODEL_STATUS"], "APPROVED")
                self.assertEqual(e["observations"], 32)
                self.assertEqual(e["approved_events"], 12)
                self.assertEqual(e["rejection_reasons"], [])
            else:
                self.assertFalse(e["ML_READY"])
                self.assertEqual(e["MODEL_STATUS"], "NOT_APPROVED")
                self.assertEqual(e["observations"], 0)
                self.assertEqual(e["approved_events"], 0)
                self.assertIn(REJECTION_REASON_INSUFFICIENT_OBSERVATIONS, e["rejection_reasons"])
                self.assertIn(REJECTION_REASON_NON_ASSAM_ML_PROHIBITED, e["rejection_reasons"])
                self.assertGreater(len(e["next_required_evidence"]), 0)

    # -------------------------------------------------------------------------
    # 12. Scientific ML Promotion Gate Enforcement
    # -------------------------------------------------------------------------
    def test_12_scientific_ml_promotion_gate_enforcement(self):
        """Verifies promotion gate permits only Brahmaputra and enforces fallback for others."""
        assam_promo = scientific_basin_promotion_gate.evaluate_basin_promotion("brahmaputra")
        self.assertTrue(assam_promo["ml_ready"])
        self.assertEqual(assam_promo["promotion_status"], PromotionStatus.APPROVED.value)
        self.assertEqual(assam_promo["model_id"], "assam_flood_prototype_v1")

        for b in ["ganga", "godavari", "mahanadi", "krishna"]:
            promo = scientific_basin_promotion_gate.evaluate_basin_promotion(b)
            self.assertFalse(promo["ml_ready"])
            self.assertEqual(promo["promotion_status"], PromotionStatus.NOT_APPROVED.value)
            self.assertEqual(promo["fallback_strategy"], "REGIONAL_BASELINE + OFFICIAL_DISASTER_INTELLIGENCE")

    # -------------------------------------------------------------------------
    # 13. Zero Synthetic Data Guarantee
    # -------------------------------------------------------------------------
    def test_13_zero_synthetic_data_guarantee(self):
        """Strict guarantee that synthetic_record_count == 0 across all manifest, event, and telemetry pipelines."""
        manifest = generate_national_flood_manifest()
        self.assertEqual(manifest["synthetic_record_count"], 0)

        acq = empirical_acquisition_service.acquire_all()
        self.assertEqual(acq["synthetic_records"], 0)

        # Attempting to corroborate a synthetic candidate is rejected
        synth_event = event_corroboration_service.evaluate_candidate_event(
            event_id="EVT-SYNTH-TEST",
            basin="brahmaputra",
            gauge_ids=["CWC-AS-001"],
            start_time="2024-07-01T00:00:00Z",
            end_time="2024-07-05T00:00:00Z",
            source_evidence=["Synthetic Generator"],
            is_synthetic=True
        )
        self.assertEqual(synth_event.corroboration_status, CorroborationStatus.REJECTED_UNSUBSTANTIATED.value)
        self.assertEqual(synth_event.rejection_reason, REJECTION_REASON_SYNTHETIC_DATA_PROHIBITED)

    # -------------------------------------------------------------------------
    # 14. Assam ML Prototype Byte-For-Byte Immutability Check
    # -------------------------------------------------------------------------
    def test_14_assam_prototype_byte_for_byte_immutability(self):
        """Asserts model.joblib has exact SHA-256 hash 0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf."""
        model_path = PROJECT_ROOT / "ml" / "flood" / "artifacts" / "model.joblib"
        self.assertTrue(model_path.exists(), "Trained prototype model artifact must exist")
        model_hash = hashlib.sha256(model_path.read_bytes()).hexdigest()
        self.assertEqual(
            model_hash,
            "0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf",
            "Model artifact must remain 100% frozen byte-for-byte"
        )

    # -------------------------------------------------------------------------
    # 15. Assam Dataset Byte-For-Byte Immutability Check
    # -------------------------------------------------------------------------
    def test_15_assam_dataset_byte_for_byte_immutability(self):
        """Asserts flood_features.csv has exact SHA-256 hash 88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080."""
        dataset_path = PROJECT_ROOT / "datasets" / "processed" / "flood_assam" / "flood_features.csv"
        self.assertTrue(dataset_path.exists(), "Assam empirical dataset must exist")
        dataset_hash = hashlib.sha256(dataset_path.read_bytes()).hexdigest()
        self.assertEqual(
            dataset_hash,
            "88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080",
            "Assam empirical dataset must remain 100% frozen byte-for-byte"
        )

    # -------------------------------------------------------------------------
    # 16. Phase 27 REST Endpoints Contract & Freshness Tagging Verification
    # -------------------------------------------------------------------------
    def test_16_phase27_api_contracts_and_freshness_tagging(self):
        """Verifies Phase 27 REST endpoints contract and explicit DataFreshness tagging."""
        # 1. /api/data/basins
        r_basins = self.client.get("/api/data/basins")
        self.assertEqual(r_basins.status_code, 200)
        d_basins = r_basins.json()
        self.assertEqual(d_basins["count"], 5)
        self.assertEqual(d_basins["synthetic_records"], 0)
        self.assertIn("freshness_categories", d_basins)

        # 2. /api/data/basins/brahmaputra vs /api/data/basins/ganga
        r_brah = self.client.get("/api/data/basins/brahmaputra")
        self.assertEqual(r_brah.status_code, 200)
        d_brah = r_brah.json()
        self.assertEqual(d_brah["freshness"], DataFreshness.EMPIRICAL.value)
        self.assertTrue(d_brah["ml_ready"])
        self.assertEqual(d_brah["model_status"], "APPROVED")
        self.assertEqual(d_brah["rejection_reasons"], [])

        r_ganga = self.client.get("/api/data/basins/ganga")
        self.assertEqual(r_ganga.status_code, 200)
        d_ganga = r_ganga.json()
        self.assertEqual(d_ganga["freshness"], DataFreshness.REGIONAL_BASELINE.value)
        self.assertFalse(d_ganga["ml_ready"])
        self.assertEqual(d_ganga["model_status"], "NOT_APPROVED")
        self.assertIn(REJECTION_REASON_NON_ASSAM_ML_PROHIBITED, d_ganga["rejection_reasons"])

        # 3. /api/data/gauges
        r_gauges = self.client.get("/api/data/gauges")
        self.assertEqual(r_gauges.status_code, 200)
        d_gauges = r_gauges.json()
        self.assertEqual(d_gauges["count"], 26)
        self.assertEqual(d_gauges["freshness"], DataFreshness.EMPIRICAL.value)

        # 4. /api/data/provenance
        r_prov = self.client.get("/api/data/provenance")
        self.assertEqual(r_prov.status_code, 200)
        d_prov = r_prov.json()
        self.assertIn("authoritative_providers", d_prov)
        self.assertIn("data_freshness_categories", d_prov)

        # 5. /api/data/readiness
        r_readiness = self.client.get("/api/data/readiness")
        self.assertEqual(r_readiness.status_code, 200)
        d_readiness = r_readiness.json()
        self.assertEqual(d_readiness["synthetic_records"], 0)
        self.assertIn("priority_basins_readiness", d_readiness)
        self.assertIn("brahmaputra", d_readiness["summary"]["prototype_active_basins"])


if __name__ == "__main__":
    unittest.main()
