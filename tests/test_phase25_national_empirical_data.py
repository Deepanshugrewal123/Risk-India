"""
RISK // INDIA — Phase 25 Verification Test Suite
=================================================
Validates National Empirical Data Foundation, Scientific ML Expansion,
Model Promotion Gates, Multi-Basin Readiness Assessments, and Strict Zero-Synthetic Invariants.
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta
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
from app.services.empirical_data_pipeline import (
    empirical_data_pipeline,
    CanonicalEmpiricalRecord,
    generate_deterministic_record_id,
    AUTHORITATIVE_AGENCIES
)
from app.services.model_promotion_gate import model_promotion_gate
from app.services.ml_readiness_gate import ml_readiness_gate
from app.services.model_registry import model_registry, ModelStatus
from app.services.basin_gauge_registry import basin_gauge_registry
from app.services.dataset_manifest import dataset_manifest_registry
from app.services.flood_model_service import flood_model_service, EXPECTED_FEATURES
from app.schemas.risk import RiskSourceType, ScientificRiskState


class TestPhase25NationalEmpiricalData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def setUp(self):
        rate_limiter.reset()

    def tearDown(self):
        rate_limiter.reset()

    # -------------------------------------------------------------------------
    # 1. Canonical Empirical Schema & Normalization
    # -------------------------------------------------------------------------
    def test_01_canonical_empirical_schema_normalization(self):
        """Verify empirical observation normalization across fields and data types."""
        raw = {
            "source": "CWC",
            "source_url": "https://ffs.india-water.gov.in",
            "observation_timestamp": "2026-09-16T10:00:00Z",
            "state": "orissa",  # Should normalize to 'Odisha'
            "district": "Cuttack",
            "latitude": 20.46,
            "longitude": 85.78,
            "hazard_type": "flood",
            "station_id": "CWC-MH-002",
            "measurements": {
                "water_level_m": 26.5,
                "rainfall_24h_mm": 45.2
            },
            "measurement_units": {
                "water_level_m": "m",
                "rainfall_24h_mm": "mm"
            },
            "original_identifier": "CWC-RAW-9921"
        }
        rec = empirical_data_pipeline.normalize_record(raw)
        self.assertIsInstance(rec, CanonicalEmpiricalRecord)
        self.assertEqual(rec.state, "Odisha")
        self.assertEqual(rec.hazard_type, "FLOOD")
        self.assertEqual(rec.data_quality_status, "VALIDATED")
        self.assertEqual(rec.confidence_score, 1.0)
        self.assertEqual(rec.measurements["water_level_m"], 26.5)

    def test_02_provenance_metadata_completeness(self):
        """Verify full provenance metadata is preserved and audit-ready."""
        records = empirical_data_pipeline.get_records(status="VALIDATED")
        self.assertGreaterEqual(len(records), 5)
        for r in records:
            self.assertTrue(bool(r.source))
            self.assertTrue(r.source_url.startswith("http"))
            self.assertTrue(bool(r.observation_timestamp))
            self.assertIn(r.hazard_type, ["FLOOD", "EARTHQUAKE", "CYCLONE", "HEATWAVE", "LANDSLIDE", "SEVERE_WEATHER"])
            self.assertGreater(r.confidence_score, 0.5)
            self.assertIn("zero_synthetic_verified", r.provenance_metadata)
            self.assertTrue(r.provenance_metadata["zero_synthetic_verified"])

    # -------------------------------------------------------------------------
    # 2. Deterministic Deduplication
    # -------------------------------------------------------------------------
    def test_03_deterministic_deduplication(self):
        """Verify duplicate empirical records are deterministically identified and suppressed."""
        record_payload = {
            "source": "India Meteorological Department (IMD)",
            "source_url": "https://mausam.imd.gov.in",
            "observation_timestamp": "2026-08-15T08:30:00Z",
            "state": "Maharashtra",
            "district": "Pune",
            "latitude": 18.52,
            "longitude": 73.85,
            "hazard_type": "SEVERE_WEATHER",
            "station_id": "IMD-PUNE-01",
            "measurements": {"rainfall_24h_mm": 62.0}
        }
        # First ingestion
        success1, rec1, msg1 = empirical_data_pipeline.ingest(record_payload)
        self.assertTrue(success1)
        self.assertEqual(rec1.data_quality_status, "VALIDATED")

        # Second ingestion of the exact same observation
        success2, rec2, msg2 = empirical_data_pipeline.ingest(record_payload)
        self.assertFalse(success2)
        self.assertIn("Duplicate", msg2)
        self.assertEqual(rec1.record_id, rec2.record_id)

    # -------------------------------------------------------------------------
    # 3. Coordinate & Physical Bounds Validation (Quarantine Engine)
    # -------------------------------------------------------------------------
    def test_04_coordinate_bounding_box_quarantine(self):
        """Verify out-of-bounds coordinates (outside India 6-38N, 68-98E) are quarantined."""
        bad_coord_payload = {
            "source": "USGS",
            "source_url": "https://earthquake.usgs.gov",
            "observation_timestamp": "2026-09-16T12:00:00Z",
            "state": "Pacific Ocean",
            "latitude": -12.5,  # South of equator
            "longitude": 120.0, # Outside Indian bounding box
            "hazard_type": "EARTHQUAKE",
            "station_id": "USGS-PACIFIC-01",
            "measurements": {"magnitude": 5.5}
        }
        rec = empirical_data_pipeline.normalize_record(bad_coord_payload)
        self.assertEqual(rec.data_quality_status, "QUARANTINED")
        self.assertIn("outside Indian subcontinental bounding box", rec.quarantine_reason)
        self.assertEqual(rec.confidence_score, 0.20)

    def test_05_physical_measurement_bounds_quarantine(self):
        """Verify physically impossible values (e.g. negative or >2000mm rain) are quarantined."""
        impossible_payload = {
            "source": "CWC",
            "source_url": "https://ffs.india-water.gov.in",
            "observation_timestamp": "2026-09-16T12:00:00Z",
            "state": "Assam",
            "latitude": 26.5,
            "longitude": 92.5,
            "hazard_type": "FLOOD",
            "station_id": "CWC-AS-999",
            "measurements": {
                "rainfall_24h_mm": 5400.0  # Physically impossible single-day reading
            }
        }
        rec = empirical_data_pipeline.normalize_record(impossible_payload)
        self.assertEqual(rec.data_quality_status, "QUARANTINED")
        self.assertIn("Excessive physical rainfall", rec.quarantine_reason)

    # -------------------------------------------------------------------------
    # 4. Dataset Manifest & Strict Zero-Synthetic Invariant
    # -------------------------------------------------------------------------
    def test_06_dataset_manifests_zero_synthetic_guarantee(self):
        """Verify all manifests strictly declare synthetic_records = 0."""
        manifests = dataset_manifest_registry.list_manifests()
        self.assertGreaterEqual(len(manifests), 5)

        m_ids = [m["dataset_id"] for m in manifests]
        self.assertIn("assam_flood_features_v1", m_ids)
        self.assertIn("godavari_gauge_registry_v1", m_ids)
        self.assertIn("mahanadi_gauge_registry_v1", m_ids)
        self.assertIn("ganga_gauge_registry_v1", m_ids)
        self.assertIn("krishna_gauge_registry_v1", m_ids)

        for m in manifests:
            self.assertEqual(m["synthetic_records"], 0, f"Manifest {m['dataset_id']} violated zero-synthetic rule!")
            self.assertTrue(bool(m["sha256"]))

    # -------------------------------------------------------------------------
    # 5. Model Registry Expansion & Frozen Assam Model Integrity
    # -------------------------------------------------------------------------
    def test_07_frozen_assam_model_byte_level_integrity(self):
        """Verify assam_flood_prototype_v1 is 100% frozen with 13 features and 32 observations."""
        assam = model_registry.get_model("assam_flood_prototype_v1")
        self.assertIsNotNone(assam)
        self.assertEqual(assam.status, ModelStatus.PROTOTYPE)
        self.assertEqual(assam.status, ModelStatus.FROZEN)
        self.assertTrue(assam.is_frozen)
        self.assertTrue(assam.is_active)
        self.assertEqual(assam.training_observation_count, 32)
        self.assertEqual(assam.validation_observation_count, 32)
        self.assertEqual(assam.scientific_status, "EMPIRICALLY_VALIDATED_ML")
        self.assertEqual(len(EXPECTED_FEATURES), 13)

        # Artifact must exist and match SHA256
        model_path = PROJECT_ROOT / "ml" / "flood" / "artifacts" / "model.joblib"
        self.assertTrue(model_path.exists())
        self.assertNotEqual(assam.artifact_hash, "ARTIFACT_NOT_FOUND")

    def test_08_future_models_data_collection_required(self):
        """Verify Godavari, Mahanadi, Ganga, Krishna models are NOT trained and require empirical data."""
        for m_id in ["flood_godavari_v1", "flood_mahanadi_v1", "flood_ganga_v1", "flood_krishna_v1"]:
            model = model_registry.get_model(m_id)
            self.assertIsNotNone(model, f"Model {m_id} missing from registry")
            self.assertFalse(model.is_active)
            self.assertFalse(model.is_predictive)
            self.assertEqual(model.training_observation_count, 0)
            self.assertEqual(model.status, ModelStatus.NOT_TRAINED)
            self.assertEqual(model.scientific_status, "EMPIRICAL_DATA_INSUFFICIENT")

    # -------------------------------------------------------------------------
    # 6. Basin Readiness Assessment: 5 Prioritized Basins
    # -------------------------------------------------------------------------
    def test_09_prioritized_basins_readiness_assessment(self):
        """Verify scientific readiness assessment for Brahmaputra, Ganga, Godavari, Mahanadi, Krishna."""
        # 1. Brahmaputra (Assam) -> Ready Prototype
        bp = ml_readiness_gate.evaluate_basin("brahmaputra")
        self.assertTrue(bp.ml_ready)
        self.assertEqual(bp.observation_count, 32)
        self.assertEqual(bp.positive_events_count, 18)
        self.assertEqual(bp.negative_observations_count, 14)
        self.assertEqual(bp.missing_data_ratio, 0.0)
        self.assertEqual(bp.scientific_state, ScientificRiskState.EMPIRICALLY_VALIDATED_ML)

        # 2. Ganga -> Data Insufficient
        gg = ml_readiness_gate.evaluate_basin("ganga")
        self.assertFalse(gg.ml_ready)
        self.assertEqual(gg.observation_count, 0)
        self.assertEqual(gg.scientific_state, ScientificRiskState.EMPIRICAL_DATA_INSUFFICIENT)
        self.assertGreaterEqual(gg.station_gauge_coverage, 5)

        # 3. Godavari -> Data Insufficient
        gd = ml_readiness_gate.evaluate_basin("godavari")
        self.assertFalse(gd.ml_ready)
        self.assertEqual(gd.observation_count, 0)
        self.assertEqual(gd.scientific_state, ScientificRiskState.EMPIRICAL_DATA_INSUFFICIENT)
        self.assertGreaterEqual(gd.station_gauge_coverage, 8)

        # 4. Mahanadi -> Data Insufficient
        mh = ml_readiness_gate.evaluate_basin("mahanadi")
        self.assertFalse(mh.ml_ready)
        self.assertEqual(mh.observation_count, 0)
        self.assertEqual(mh.scientific_state, ScientificRiskState.EMPIRICAL_DATA_INSUFFICIENT)
        self.assertGreaterEqual(mh.station_gauge_coverage, 8)

        # 5. Krishna -> Data Insufficient
        kr = ml_readiness_gate.evaluate_basin("krishna")
        self.assertFalse(kr.ml_ready)
        self.assertEqual(kr.observation_count, 0)
        self.assertEqual(kr.scientific_state, ScientificRiskState.EMPIRICAL_DATA_INSUFFICIENT)
        self.assertGreaterEqual(kr.station_gauge_coverage, 5)

    # -------------------------------------------------------------------------
    # 7. Model Promotion Gate: 11 Scientific Validation Gates
    # -------------------------------------------------------------------------
    def test_10_model_promotion_gate_assam_approved(self):
        """Verify assam_flood_prototype_v1 passes all 11 scientific validation gates."""
        assam_meta = model_registry.get_model("assam_flood_prototype_v1").to_dict()
        assam_meta["positive_events_count"] = 18
        res = model_promotion_gate.evaluate_model("assam_flood_prototype_v1", assam_meta)
        self.assertTrue(res.is_approved)
        self.assertEqual(res.promotion_status, "APPROVED")
        self.assertEqual(res.passed_count, 11)

    def test_11_model_promotion_gate_rejects_insufficient_data_or_leakage(self):
        """Verify candidate with < 100 observations or temporal leakage is rejected."""
        bad_candidate = {
            "training_observation_count": 45,  # Insufficient (< 100)
            "temporal_leakage_detected": True,  # Critical violation
            "spatial_validity": True,
            "positive_events_count": 22,
            "missing_feature_ratio": 0.02,
            "provenance_completeness": 0.95,
            "artifact_hash": "dummyhash123",
            "metrics": {"accuracy": 0.85, "f1_score": 0.82, "roc_auc": 0.84},
            "geographic_scope": ["Godavari Basin"]
        }
        res = model_promotion_gate.evaluate_model("flood_godavari_candidate_bad", bad_candidate)
        self.assertFalse(res.is_approved)
        self.assertEqual(res.promotion_status, "NOT_APPROVED")
        self.assertIn("REGIONAL_BASELINE", res.fallback_strategy)
        failed_checks = [c.check_name for c in res.checks if not c.passed]
        self.assertIn("sufficient_observations", failed_checks)
        self.assertIn("temporal_separation_no_leakage", failed_checks)

    # -------------------------------------------------------------------------
    # 8. REST API: Scientific State & Risk Source Classification
    # -------------------------------------------------------------------------
    def test_12_api_risk_classification_assam_ml_vs_non_assam(self):
        """Verify API response clearly classifies EMPIRICAL_ML vs REGIONAL_BASELINE."""
        # 1. Assam ML Query
        resp_assam = self.client.post("/api/risk/analyze", json={
            "location_id": "assam",
            "district": "Kamrup",
            "hazard": "flood",
            "features": {
                "rainfall_24h": 45.0,
                "rainfall_72h": 120.0,
                "river_level_relative": 1.2
            }
        })
        self.assertEqual(resp_assam.status_code, 200)
        data_assam = resp_assam.json()
        self.assertEqual(data_assam["status"], "success")
        self.assertEqual(data_assam["risk_source"], RiskSourceType.EMPIRICAL_ML)
        self.assertEqual(data_assam["scientific_state"], ScientificRiskState.EMPIRICALLY_VALIDATED_ML)
        self.assertIn("Assam Brahmaputra", data_assam["model_scope"])

        # 2. Non-Assam Query (e.g. Maharashtra) -> Spatial Guard Active
        resp_mh = self.client.post("/api/risk/analyze", json={
            "location_id": "maharashtra",
            "district": "Pune",
            "hazard": "flood"
        })
        self.assertEqual(resp_mh.status_code, 200)
        data_mh = resp_mh.json()
        self.assertEqual(data_mh["status"], "model_scope_limited")
        self.assertEqual(data_mh["risk_source"], RiskSourceType.REGIONAL_BASELINE)
        self.assertEqual(data_mh["scientific_state"], ScientificRiskState.EMPIRICAL_DATA_INSUFFICIENT)

    def test_13_api_empirical_catalog_and_schema_endpoints(self):
        """Verify /api/data/empirical/catalog and schema endpoints."""
        # Schema
        resp_schema = self.client.get("/api/data/empirical/schema")
        self.assertEqual(resp_schema.status_code, 200)
        s_data = resp_schema.json()
        self.assertTrue(s_data["zero_synthetic_guarantee"])
        self.assertIn("record_id", s_data["mandatory_fields"])

        # Catalog
        resp_catalog = self.client.get("/api/data/empirical/catalog")
        self.assertEqual(resp_catalog.status_code, 200)
        c_data = resp_catalog.json()
        self.assertEqual(c_data["synthetic_records"], 0)
        self.assertGreaterEqual(c_data["count"], 5)

    def test_14_api_priority_basins_readiness_endpoint(self):
        """Verify /api/basins/readiness/priority returns the 5 core basins."""
        resp = self.client.get("/api/basins/readiness/priority")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["count"], 5)
        self.assertEqual(data["priority_basins"], ["brahmaputra", "ganga", "godavari", "mahanadi", "krishna"])
        assam_eval = next(a for a in data["assessments"] if a["basin_id"] == "brahmaputra")
        self.assertTrue(assam_eval["ml_ready"])
        ganga_eval = next(a for a in data["assessments"] if a["basin_id"] == "ganga")
        self.assertFalse(ganga_eval["ml_ready"])

    def test_15_api_model_promotion_gate_endpoint(self):
        """Verify /api/models/{model_id}/promotion-gate endpoint."""
        resp_assam = self.client.get("/api/models/assam_flood_prototype_v1/promotion-gate")
        self.assertEqual(resp_assam.status_code, 200)
        self.assertTrue(resp_assam.json()["is_approved"])

        resp_gd = self.client.get("/api/models/flood_godavari_v1/promotion-gate")
        self.assertEqual(resp_gd.status_code, 200)
        self.assertFalse(resp_gd.json()["is_approved"])
        self.assertEqual(resp_gd.json()["promotion_status"], "NOT_APPROVED")


if __name__ == "__main__":
    unittest.main()
