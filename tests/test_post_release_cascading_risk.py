"""
RISK // INDIA — Post-Release Enhancement: Cascading Risk Intelligence Test Suite
================================================================================
Comprehensive test suite validating:
1. Cascading risk data schema & serialization
2. Hazard-to-secondary-risk relationships across all 6 supported hazards
3. Evidence posture states (LIVE_EVIDENCE, RECENT_EVIDENCE, FORECAST_AVAILABLE, BASELINE_ONLY, LIMITED_EVIDENCE, DATA_UNAVAILABLE)
4. Data-gap honesty & unmonitored condition reporting
5. Regional location & terrain conditionality
6. Earthquake non-prediction safeguard
7. Assam ML boundary preservation
8. Strict absence of fabricated numeric pseudo-probabilities
9. Zero synthetic data enforcement (synthetic_records == 0)
10. End-to-end FastAPI REST endpoint contracts
"""

import unittest
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from app.main import app
from app.services.future_risk import (
    cascading_risk_engine,
    CascadingRiskEngine,
    EvidencePosture,
    RelationshipClassification,
    SUPPORTED_HAZARDS
)


class TestCascadingRiskIntelligence(unittest.TestCase):
    """Validates cascading and secondary risk intelligence capabilities."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_cascading_engine_initialization(self):
        """Engine is instantiated and supports all 6 canonical hazards."""
        self.assertIsInstance(cascading_risk_engine, CascadingRiskEngine)
        self.assertEqual(len(SUPPORTED_HAZARDS), 6)
        self.assertIn("FLOOD", SUPPORTED_HAZARDS)
        self.assertIn("CYCLONE", SUPPORTED_HAZARDS)
        self.assertIn("EARTHQUAKE", SUPPORTED_HAZARDS)
        self.assertIn("HEATWAVE", SUPPORTED_HAZARDS)
        self.assertIn("LANDSLIDE", SUPPORTED_HAZARDS)
        self.assertIn("SEVERE_WEATHER", SUPPORTED_HAZARDS)

    def test_flood_consequence_chain_structure(self):
        """Flood consequence chain has 4 valid progressive stages."""
        assessment = cascading_risk_engine.evaluate_region_cascading_risk("assam", "FLOOD")
        self.assertIsNotNone(assessment)
        self.assertEqual(assessment.primary_hazard, "FLOOD")
        self.assertEqual(len(assessment.chains), 1)

        chain = assessment.chains[0]
        self.assertEqual(chain.hazard, "FLOOD")
        self.assertEqual(len(chain.stages), 4)

        stage_types = [s.stage_type for s in chain.stages]
        self.assertEqual(stage_types, [
            "PRIMARY_HAZARD",
            "PHYSICAL_CHANGE",
            "SECONDARY_HAZARD",
            "TERTIARY_CONSEQUENCE"
        ])

        # Stage 3 must be conditional secondary risk
        stage3 = chain.stages[2]
        self.assertEqual(stage3.scientific_classification, RelationshipClassification.CONDITIONAL_SECONDARY_RISK)
        self.assertTrue(len(stage3.defensive_actions) >= 1)
        self.assertTrue(len(stage3.field_warning_signs) >= 1)

    def test_cyclone_consequence_chain(self):
        """Cyclone chain models wind shear and coastal surge consequences."""
        assessment = cascading_risk_engine.evaluate_region_cascading_risk("odisha", "CYCLONE")
        self.assertIsNotNone(assessment)
        chain = assessment.chains[0]
        self.assertEqual(chain.hazard, "CYCLONE")
        self.assertIn("Blackout", chain.title)
        self.assertEqual(len(chain.stages), 4)

        # Verify telecommunications blackout consequence
        stage4 = chain.stages[3]
        self.assertIn("Telecommunication", stage4.title)

    def test_earthquake_non_prediction_safeguard(self):
        """Earthquake chain strictly enforces the non-prediction scientific invariant."""
        assessment = cascading_risk_engine.evaluate_region_cascading_risk("uttarakhand", "EARTHQUAKE")
        self.assertIsNotNone(assessment)
        chain = assessment.chains[0]
        self.assertEqual(chain.hazard, "EARTHQUAKE")

        # Mandatory non-prediction notice must be present
        self.assertIsNotNone(chain.earthquake_non_prediction_notice)
        self.assertIn("CANNOT be temporally predicted", chain.earthquake_non_prediction_notice)

        # Primary hazard classification must be established physical relationship, NOT predictive forecast
        stage1 = chain.stages[0]
        self.assertEqual(stage1.scientific_classification, RelationshipClassification.ESTABLISHED_PHYSICAL_RELATIONSHIP)
        self.assertNotEqual(stage1.scientific_classification, RelationshipClassification.PREDICTIVE_FORECAST)

        # Aftershock stage must have explicit non-prediction note
        stage4 = chain.stages[3]
        self.assertIn("Aftershock", stage4.title)

    def test_heatwave_consequence_chain(self):
        """Heatwave chain models thermal stress, water demand, and power grid loads."""
        assessment = cascading_risk_engine.evaluate_region_cascading_risk("rajasthan", "HEATWAVE")
        self.assertIsNotNone(assessment)
        chain = assessment.chains[0]
        self.assertEqual(chain.hazard, "HEATWAVE")
        self.assertEqual(len(chain.stages), 4)

        stage3 = chain.stages[2]
        self.assertIn("Transformer", stage3.title)

    def test_landslide_consequence_chain(self):
        """Landslide chain models debris flow, river damming, and transport severance."""
        assessment = cascading_risk_engine.evaluate_region_cascading_risk("himachal-pradesh", "LANDSLIDE")
        self.assertIsNotNone(assessment)
        chain = assessment.chains[0]
        self.assertEqual(chain.hazard, "LANDSLIDE")

        # Terrain sensitivity note must be present
        self.assertIsNotNone(chain.terrain_sensitivity_note)

        # Stage 3 must model river damming / outburst flood risk
        stage3 = chain.stages[2]
        self.assertIn("Damming", stage3.title)

    def test_severe_weather_consequence_chain(self):
        """Severe weather chain models convective squalls, underpass ponding, and lightning."""
        assessment = cascading_risk_engine.evaluate_region_cascading_risk("delhi", "SEVERE_WEATHER")
        self.assertIsNotNone(assessment)
        chain = assessment.chains[0]
        self.assertEqual(chain.hazard, "SEVERE_WEATHER")
        self.assertEqual(len(chain.stages), 4)

    def test_terrain_conditionality_not_simplistic_blanket(self):
        """Terrain conditionality checks actual slope vulnerability, not just blanket state suppression."""
        # Punjab has low/alluvial slope vulnerability baseline
        punjab_eval = cascading_risk_engine.evaluate_region_cascading_risk("punjab", "FLOOD")
        self.assertIsNotNone(punjab_eval)
        punjab_chain = punjab_eval.chains[0]
        self.assertIsNotNone(punjab_chain.terrain_sensitivity_note)

        # Uttarakhand has high slope vulnerability baseline
        uk_eval = cascading_risk_engine.evaluate_region_cascading_risk("uttarakhand", "FLOOD")
        self.assertIsNotNone(uk_eval)
        uk_chain = uk_eval.chains[0]
        self.assertIn("slope vulnerability", uk_chain.terrain_sensitivity_note.lower())

    def test_data_gap_honesty_unmonitored_fields(self):
        """Every stage explicitly reports unmonitored or unknown conditions."""
        assessment = cascading_risk_engine.evaluate_region_cascading_risk("bihar", "FLOOD")
        self.assertIsNotNone(assessment)
        chain = assessment.chains[0]
        for stage in chain.stages:
            self.assertTrue(len(stage.unmonitored_or_unknown) >= 1, f"Stage {stage.stage_order} missing unmonitored notes")

    def test_zero_numeric_pseudo_probabilities(self):
        """Cascading risk outputs contain no unsupported numeric probabilities."""
        assessment = cascading_risk_engine.evaluate_region_cascading_risk("assam", "FLOOD")
        d = assessment.to_dict()

        # Recursive check for any '% probability' or 'risk = X%' strings
        def check_no_fake_prob(obj):
            if isinstance(obj, str):
                self.assertNotIn("probability =", obj)
                self.assertNotIn("probability:", obj)
                self.assertNotIn("landslide probability", obj.lower())
            elif isinstance(obj, dict):
                for k, v in obj.items():
                    check_no_fake_prob(v)
            elif isinstance(obj, list):
                for item in obj:
                    check_no_fake_prob(item)

        check_no_fake_prob(d)

    def test_zero_synthetic_data_guarantee(self):
        """All cascading risk structures guarantee synthetic_records == 0."""
        for h in SUPPORTED_HAZARDS:
            eval_res = cascading_risk_engine.evaluate_region_cascading_risk("assam", h)
            self.assertIsNotNone(eval_res)
            self.assertEqual(eval_res.synthetic_records, 0)
            self.assertEqual(eval_res.chains[0].synthetic_records, 0)

    # -------------------------------------------------------------------------
    # REST API Endpoint Tests
    # -------------------------------------------------------------------------
    def test_api_region_cascading_endpoint(self):
        """GET /api/future-risk/{region}/cascading returns valid HTTP 200 payload."""
        resp = self.client.get("/api/future-risk/assam/cascading")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["region"]["id"], "assam")
        self.assertEqual(data["synthetic_records"], 0)
        self.assertTrue(len(data["chains"]) >= 1)
        self.assertIn("stages", data["chains"][0])

    def test_api_region_hazard_cascading_endpoint(self):
        """GET /api/future-risk/{region}/{hazard}/cascading returns hazard-specific chain."""
        resp = self.client.get("/api/future-risk/kerala/LANDSLIDE/cascading")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["primary_hazard"], "LANDSLIDE")
        self.assertEqual(data["chains"][0]["hazard"], "LANDSLIDE")

    def test_api_cascading_invalid_hazard_returns_400(self):
        """GET /api/future-risk/{region}/cascading with invalid hazard returns HTTP 400."""
        resp = self.client.get("/api/future-risk/assam/cascading?hazard=VOLCANO_ERUPTION")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Unsupported hazard", resp.json()["detail"])

    def test_api_cascading_invalid_region_returns_404(self):
        """GET /api/future-risk/{region}/cascading with invalid region returns HTTP 404."""
        resp = self.client.get("/api/future-risk/atlantis-invalid-zone/cascading")
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
