"""
RISK // INDIA — Automated Test Suite: Assam Flood ML Prototype Integration
End-to-end verification of trained model integration with FastAPI and frontend contracts.

10 Required Test Conditions:
1. test_model_loading: Model and preprocessor loaded successfully from disk
2. test_valid_inference: Clean prediction generated for valid Assam telemetry
3. test_probability_range: Probability is strictly float between 0.0 and 1.0
4. test_score_range: UI risk score is strictly integer between 0 and 100
5. test_risk_level_mapping: Risk level is one of ["Low", "Moderate", "High", "Critical"]
6. test_model_version_string: Model version matches "assam_flood_prototype_v1"
7. test_unsupported_location: Non-Assam locations return "model_scope_limited" without fake scores
8. test_missing_features: Missing telemetry returns "insufficient_data" without fake scores
9. test_explanation_generation: Top factors generated using exact linear feature contributions
10. test_no_future_data_leakage: Model strictly relies on antecedent and static spatial features
"""

import sys
from pathlib import Path
import unittest
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from backend.app.services.flood_model_service import (
    flood_model_service,
    EXPECTED_FEATURES,
    SUPPORTED_ASSAM_LOCATIONS
)
from backend.app.services.risk_service import risk_service
from backend.app.schemas.risk import RiskAnalyzeRequest, RiskAnalyzeResponse


class TestMLIntegration(unittest.TestCase):

    def setUp(self):
        self.service = flood_model_service
        self.sample_features = {
            "rainfall_6h": 1.5,
            "rainfall_24h": 56.0,
            "rainfall_72h": 73.0,
            "rainfall_168h": 196.5,
            "river_level_relative": 0.819,
            "river_rise_6h": 0.024,
            "river_rise_24h": 0.172,
            "river_percentile_level": 0.0218,
            "month": 6,
            "day_of_year_sin": 0.23224,
            "day_of_year_cos": -0.97266,
            "latitude": 26.6958,
            "longitude": 92.2577
        }

    # 1. Model Loading
    def test_01_model_loading(self):
        self.assertTrue(self.service.is_ready, "Flood ML service model and preprocessor must be ready.")
        self.assertIsNotNone(self.service.model, "Model instance must not be None.")
        self.assertIsNotNone(self.service.preprocessor, "Preprocessor instance must not be None.")
        self.assertEqual(self.service.model_version, "assam_flood_prototype_v1")

    # 2. Valid Inference
    def test_02_valid_inference(self):
        res = self.service.predict(
            location_id="assam",
            district="Udalguri",
            features=self.sample_features
        )
        self.assertEqual(res["status"], "success")
        self.assertTrue(res["is_prototype"])
        self.assertFalse(res["emergency_warning"])
        self.assertIn("Experimental Assam flood-risk prototype", res["disclaimer"])

    # 3. Probability Range [0.0, 1.0]
    def test_03_probability_range(self):
        res = self.service.predict(
            location_id="assam",
            district="Udalguri",
            features=self.sample_features
        )
        prob = res.get("flood_probability")
        self.assertIsInstance(prob, float)
        self.assertGreaterEqual(prob, 0.0)
        self.assertLessEqual(prob, 1.0)

    # 4. Score Range [0, 100]
    def test_04_score_range(self):
        res = self.service.predict(
            location_id="assam",
            district="Udalguri",
            features=self.sample_features
        )
        score = res.get("risk_score")
        self.assertIsInstance(score, int)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    # 5. Risk Level Mapping
    def test_05_risk_level_mapping(self):
        res = self.service.predict(
            location_id="assam",
            district="Udalguri",
            features=self.sample_features
        )
        level = res.get("risk_level")
        self.assertIn(level, ["Low", "Moderate", "High", "Critical"])

    # 6. Model Version String
    def test_06_model_version_string(self):
        res = self.service.predict(
            location_id="assam",
            district="Udalguri",
            features=self.sample_features
        )
        self.assertEqual(res["model_version"], "assam_flood_prototype_v1")

    # 7. Unsupported Location Scope Guard
    def test_07_unsupported_location(self):
        unsupported_cases = [
            ("kerala", "Ernakulam"),
            ("maharashtra", "Mumbai"),
            ("delhi", "New Delhi"),
            ("rajasthan", "Jaipur")
        ]
        for loc, dist in unsupported_cases:
            res = self.service.predict(
                location_id=loc,
                district=dist,
                features=self.sample_features
            )
            self.assertEqual(res["status"], "model_scope_limited")
            self.assertIn("limited to selected Assam monitoring areas", res["message"])
            self.assertIsNone(res.get("flood_probability"))
            self.assertIsNone(res.get("risk_score"))

    # 8. Missing Environmental Features Guard
    def test_08_missing_features(self):
        res = self.service.predict(
            location_id="assam",
            district="Udalguri",
            features={}
        )
        self.assertEqual(res["status"], "insufficient_data")
        self.assertIn("Insufficient environmental data", res["message"])
        self.assertIsNone(res.get("flood_probability"))
        self.assertIsNone(res.get("risk_score"))

    # 9. Explanation Generation
    def test_09_explanation_generation(self):
        res = self.service.predict(
            location_id="assam",
            district="Udalguri",
            features=self.sample_features
        )
        factors = res.get("top_factors", [])
        self.assertIsInstance(factors, list)
        self.assertGreater(len(factors), 0)
        self.assertLessEqual(len(factors), 4)

        for factor in factors:
            self.assertIn("feature", factor)
            self.assertIn("contribution", factor)
            self.assertIn("direction", factor)
            self.assertIn("display_label", factor)
            self.assertIn(factor["direction"], ["increases_risk", "decreases_risk"])
            self.assertIsInstance(factor["contribution"], float)

    # 10. No Future Data Leakage
    def test_10_no_future_data_leakage(self):
        forbidden_substrings = ["future", "post", "target", "occurrence", "lead_", "_ahead", "after"]
        for feat in EXPECTED_FEATURES:
            for forbidden in forbidden_substrings:
                self.assertNotIn(
                    forbidden,
                    feat.lower(),
                    f"Feature '{feat}' appears to contain future information or target leakage."
                )

        expected_set = {
            "rainfall_6h", "rainfall_24h", "rainfall_72h", "rainfall_168h",
            "river_level_relative", "river_rise_6h", "river_rise_24h",
            "river_percentile_level", "month", "day_of_year_sin", "day_of_year_cos",
            "latitude", "longitude"
        }
        self.assertEqual(set(EXPECTED_FEATURES), expected_set)


if __name__ == "__main__":
    unittest.main()
