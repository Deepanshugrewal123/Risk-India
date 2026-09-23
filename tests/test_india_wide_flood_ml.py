"""
RISK // INDIA — Automated Test Suite: India-Wide Flood ML Expansion (risk_india_flood_v1)
========================================================================================
Validates the nationwide empirical machine learning flood intelligence pipeline,
compound flood target scientific formulation, model serialization, model registry,
and strict immutability of historical certified baseline artifacts.
"""

import os
import sys
import json
import hashlib
from pathlib import Path
import unittest
import pandas as pd
import numpy as np

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.services.national_flood_model_service import national_flood_model_service
from app.services.model_registry import model_registry, ModelStatus
from fastapi.testclient import TestClient
from app.main import app

CERTIFIED_ASSAM_MODEL_HASH = "0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf"
CERTIFIED_ASSAM_DATASET_HASH = "88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080"


class TestIndiaWideFloodML(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.dataset_path = PROJECT_ROOT / "datasets" / "processed" / "national_flood" / "national_flood_features.csv"
        cls.model_path = PROJECT_ROOT / "ml" / "national_flood" / "artifacts" / "model.joblib"
        cls.metadata_path = PROJECT_ROOT / "ml" / "national_flood" / "artifacts" / "metadata.json"

    # 1. Empirical Dataset Integrity & Zero Synthetic Records
    def test_01_processed_dataset_integrity(self):
        """Verifies 18,216 empirical observations, nationwide coverage, zero synthetic records."""
        self.assertTrue(self.dataset_path.exists(), f"Processed dataset missing at {self.dataset_path}")
        df = pd.read_csv(self.dataset_path)

        self.assertEqual(len(df), 18216, "Total dataset rows must be exactly 18,216 (18,184 IMD + 32 ISRO Bhuvan).")
        self.assertGreaterEqual(df["state"].nunique(), 36, "Must cover at least 36 Indian States/UTs.")
        self.assertGreaterEqual(df["district"].nunique(), 700, "Must cover over 700 districts.")

        # Zero synthetic records
        self.assertEqual((df["synthetic_record"] != 0).sum(), 0, "Synthetic records must be strictly zero.")
        self.assertEqual(df["synthetic_record"].sum(), 0, "No synthetic records allowed.")

        # Target column exists and has positive/negative balance
        self.assertIn("flood_risk_event", df.columns)
        pos_count = (df["flood_risk_event"] == 1).sum()
        neg_count = (df["flood_risk_event"] == 0).sum()
        self.assertGreater(pos_count, 50, "Must contain empirical positive compound flood events.")
        self.assertGreater(neg_count, 15000, "Must contain empirical control/negative observations.")

    # 2. Compound Target Formulation (Distinguishing Rain Only from Inundation)
    def test_02_compound_flood_target_science(self):
        """Verifies scientific formulation distinguishes rain-only from compound inundation."""
        df = pd.read_csv(self.dataset_path)
        self.assertIn("is_heavy_rain_only", df.columns)

        # Isolated heavy rain without saturation must be flagged
        rain_only_events = df[df["is_heavy_rain_only"] == 1]
        self.assertGreater(len(rain_only_events), 0, "Must identify dry catchment heavy rain events.")

        # Inundation requires compound response
        compound_events = df[df["flood_risk_event"] == 1]
        for _, row in compound_events.head(20).iterrows():
            acute = (row["actual_rainfall_24h_mm"] >= 64.5) or (row["actual_rainfall_24h_mm"] >= 50.0) or (row["primary_basin"] == "brahmaputra")
            self.assertTrue(acute, "Compound flood event must have acute rainfall influx or basin vulnerability.")

    # 3. Model Artifact and Metadata Integrity
    def test_03_model_artifact_and_metadata(self):
        """Verifies model serialization, metadata, algorithm, and metrics."""
        self.assertTrue(self.model_path.exists(), "Trained model artifact missing.")
        self.assertTrue(self.metadata_path.exists(), "Model metadata JSON missing.")

        with open(self.metadata_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        self.assertEqual(meta["model_name"], "risk_india_flood_v1")
        self.assertEqual(meta["algorithm"], "GradientBoostingClassifier")
        self.assertEqual(meta["library"], "scikit-learn")
        self.assertEqual(meta["training_data"]["observation_count"], 18216)
        self.assertEqual(meta["training_data"]["imd_observations"], 18184)
        self.assertEqual(meta["training_data"]["bhuvan_satellite_observations"], 32)
        self.assertEqual(meta["training_data"]["synthetic_records"], 0)

        # Preprocessor check
        preproc_path = self.model_path.parent / "preprocessor.joblib"
        self.assertTrue(preproc_path.exists(), "Preprocessor artifact missing.")

        # Metrics verification
        cv_metrics = meta["cross_validation_5fold_grouped"]
        self.assertGreaterEqual(cv_metrics["roc_auc"], 0.90, "5-Fold CV ROC-AUC must be >= 0.90")
        self.assertGreaterEqual(cv_metrics["f1_score"], 0.85, "5-Fold CV F1-Score must be >= 0.85")
        self.assertLessEqual(cv_metrics["brier_score"], 0.05, "Brier score must indicate well-calibrated probabilities.")

    # 4. Temporal and Regional Holdout Validation
    def test_04_temporal_and_regional_holdout_validation(self):
        """Verifies temporal out-of-time generalizability and regional zone transferability."""
        with open(self.metadata_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        temp = meta["temporal_holdout_evaluation"]
        self.assertGreaterEqual(temp["roc_auc"], 0.90, "Temporal holdout ROC-AUC must be >= 0.90")
        self.assertGreaterEqual(temp["f1_score"], 0.85, "Temporal holdout F1-Score must be >= 0.85")

        reg = meta["regional_holdout_evaluation"]
        for zone in ["North", "Central", "East", "Northeast", "West", "South"]:
            self.assertIn(zone, reg, f"Zone {zone} must be evaluated in regional holdout.")
            if reg[zone]["positive_events"] > 0:
                self.assertGreaterEqual(reg[zone]["roc_auc"], 0.80, f"Zone {zone} ROC-AUC must be >= 0.80")

    # 5. National Flood Model Service Inference
    def test_05_national_flood_model_service_inference(self):
        """Verifies real-time inference on risk_india_flood_v1 across diverse Indian jurisdictions."""
        self.assertTrue(national_flood_model_service.is_ready)
        self.assertEqual(national_flood_model_service.model_version, "risk_india_flood_v1")

        # Case A: Heavy compound rain in Uttar Pradesh (Ganga Basin)
        res_up = national_flood_model_service.predict(
            location_id="uttar-pradesh",
            features={"actual_rainfall_24h_mm": 95.0, "weekly_rainfall_actual_mm": 160.0}
        )
        self.assertEqual(res_up["status"], "success")
        self.assertEqual(res_up["risk_level"], "SEVERE")
        self.assertGreater(res_up["flood_probability"], 0.80)
        self.assertEqual(res_up["model_version"], "risk_india_flood_v1")
        self.assertEqual(res_up["synthetic_records"], 0)
        self.assertFalse(res_up["is_prototype"])
        self.assertGreater(len(res_up["feature_attributions"]), 0)

        # Case B: Benign conditions in Maharashtra
        res_mh = national_flood_model_service.predict(
            location_id="maharashtra",
            features={"actual_rainfall_24h_mm": 5.0, "weekly_rainfall_actual_mm": 20.0}
        )
        self.assertEqual(res_mh["status"], "success")
        self.assertEqual(res_mh["risk_level"], "LOW")
        self.assertLess(res_mh["flood_probability"], 0.20)

        # Case C: Rain-only on dry soil in Rajasthan (differentiated from flood)
        res_rj = national_flood_model_service.predict(
            location_id="rajasthan",
            features={"actual_rainfall_24h_mm": 65.0, "weekly_rainfall_actual_mm": 10.0, "normal_rainfall_24h_mm": 15.0}
        )
        self.assertEqual(res_rj["status"], "success")
        self.assertEqual(res_rj["risk_level"], "LOW")
        self.assertLess(res_rj["flood_probability"], 0.25)

    # 6. Model Registry Integration
    def test_06_model_registry_integration(self):
        """Verifies risk_india_flood_v1 is active in model registry alongside historical prototype."""
        nat = model_registry.get_model("risk_india_flood_v1")
        self.assertIsNotNone(nat, "risk_india_flood_v1 must be registered.")
        self.assertEqual(nat.status, ModelStatus.VALIDATED)
        self.assertTrue(nat.is_active)
        self.assertTrue(nat.is_predictive)
        self.assertEqual(nat.training_observation_count, 18216)

        # Assam prototype remains registered
        assam = model_registry.get_model("assam_flood_prototype_v1")
        self.assertIsNotNone(assam)
        self.assertEqual(assam.status, ModelStatus.PROTOTYPE)
        self.assertTrue(assam.is_active)

    # 7. REST API Endpoint (/api/risk/national-flood/predict)
    def test_07_rest_api_endpoint(self):
        """Verifies FastAPI REST API endpoint returns valid predictions and attribution factors."""
        payload = {
            "location_id": "bihar",
            "district": "Patna",
            "hazard": "flood",
            "features": {
                "actual_rainfall_24h_mm": 80.0,
                "weekly_rainfall_actual_mm": 140.0
            }
        }
        response = self.client.post("/api/risk/national-flood/predict", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["model_version"], "risk_india_flood_v1")
        self.assertEqual(data["synthetic_records"], 0)
        self.assertIn("feature_attributions", data)
        self.assertIn("corroborating_evidence", data)

    # 8. Strict Byte-for-Byte Assam Legacy Preservation
    def test_08_assam_legacy_immutability_and_hashes(self):
        """Verifies certified historical Assam model and dataset are strictly unchanged."""
        assam_model_path = PROJECT_ROOT / "ml" / "flood" / "artifacts" / "model.joblib"
        assam_dataset_path = PROJECT_ROOT / "datasets" / "processed" / "flood_assam" / "flood_features.csv"

        with open(assam_model_path, "rb") as f:
            model_hash = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(model_hash.lower(), CERTIFIED_ASSAM_MODEL_HASH.lower(), "Certified Assam model modified!")

        with open(assam_dataset_path, "rb") as f:
            ds_hash = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(ds_hash.lower(), CERTIFIED_ASSAM_DATASET_HASH.lower(), "Certified Assam dataset modified!")

    # 9. Earthquake Non-Prediction Invariant
    def test_09_earthquake_non_prediction_preserved(self):
        """Verifies earthquake assessments strictly forbid deterministic temporal prediction."""
        res = national_flood_model_service.predict("delhi", hazard="earthquake")
        self.assertEqual(res["status"], "hazard_unsupported_by_flood_model")
        self.assertIn("statutory baselines", res["message"])


if __name__ == "__main__":
    unittest.main()
