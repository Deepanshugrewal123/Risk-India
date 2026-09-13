"""
RISK // INDIA — Automated End-to-End User Journey Test Suite
Comprehensive verification of all 8 primary application stages across the API,
data providers, machine learning inference engine, explainability drivers,
and verified disaster resource registry.
"""

import sys
from pathlib import Path
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi.testclient import TestClient
from backend.app.main import app


class TestEndToEndJourney(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_stage_1_system_health(self):
        """Stage 1: System Telemetry and Health Checks"""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn(data.get("status"), ["ok", "healthy", "degraded"])
        self.assertIn("providers", data)

    def test_stage_2_geospatial_locations(self):
        """Stage 2: Inspect Administrative Regions and Map Telemetry"""
        response = self.client.get("/api/locations")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(len(data), 36)

        # Inspect Assam region baseline
        assam_resp = self.client.get("/api/risk/assam")
        self.assertEqual(assam_resp.status_code, 200)
        assam_data = assam_resp.json()
        self.assertEqual(assam_data["location"]["name"], "Assam")
        self.assertIn("risk_score", assam_data["assessment"])

    def test_stage_3_live_disaster_feed(self):
        """Stage 3: Live Incident Telemetry and Freshness"""
        response = self.client.get("/api/disasters/live")
        self.assertEqual(response.status_code, 200)
        events = response.json()
        self.assertGreater(len(events), 0)
        first = events[0]
        self.assertIn("title", first)
        self.assertIn("hazard_type", first)
        self.assertIn("source", first)

    def test_stage_4_verified_help_directory(self):
        """Stage 4: Verified Help Directory and Category Filtering"""
        response = self.client.get("/api/resources?category=Medical%20Assistance")
        self.assertEqual(response.status_code, 200)
        resources = response.json()
        self.assertGreater(len(resources), 0)
        for r in resources:
            self.assertEqual(r["verification_status"], "VERIFIED")
            self.assertTrue(r["source_url"].startswith("http"))

    def test_stage_5_help_others_solidarity(self):
        """Stage 5: Official Relief Funds and Contribution Portals"""
        response = self.client.get("/api/resources?category=Donations%20%2F%20Volunteering")
        self.assertEqual(response.status_code, 200)
        resources = response.json()
        self.assertGreater(len(resources), 0)
        for r in resources:
            portal = r.get("website_url") or r.get("source_url")
            self.assertFalse(portal.startswith("javascript:"))
            self.assertTrue(any(dom in portal for dom in [".gov.in", "indianredcross.org", "goonj.org", "akshayapatra.org"]))

    def test_stage_6_ml_flood_inference(self):
        """Stage 6: ML Flood Prototype Inference on Supported Basin"""
        payload = {
            "location_id": "assam",
            "district": "Udalguri",
            "hazard": "flood",
            "features": {
                "rainfall_24h": 68.5,
                "rainfall_72h": 142.0,
                "river_level_relative": 1.58,
                "latitude": 26.69,
                "longitude": 92.25
            }
        }
        response = self.client.post("/api/risk/analyze", json=payload)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result.get("status"), "success")
        self.assertEqual(result.get("model_version"), "assam_flood_prototype_v1")
        self.assertIsInstance(result.get("risk_score"), int)
        self.assertGreaterEqual(result.get("risk_score"), 0)
        self.assertLessEqual(result.get("risk_score"), 100)

    def test_stage_7_explainability_attribution(self):
        """Stage 7: Explainable AI Attribution Drivers and Disclaimers"""
        payload = {
            "location_id": "assam",
            "district": "Udalguri",
            "hazard": "flood",
            "features": {
                "rainfall_24h": 75.0,
                "rainfall_72h": 160.0,
                "river_level_relative": 1.9,
                "latitude": 26.69,
                "longitude": 92.25
            }
        }
        response = self.client.post("/api/risk/analyze", json=payload)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("top_factors", result)
        self.assertGreater(len(result["top_factors"]), 0)
        for f in result["top_factors"]:
            self.assertIn("contribution", f)
            self.assertIn("direction", f)
            self.assertIn("display_label", f)
        self.assertIn("disclaimer", result)

    def test_stage_8_scope_guard(self):
        """Stage 8: Geographic and Hazard Scope Guard Protection"""
        payload = {
            "location_id": "delhi",
            "hazard": "flood",
            "features": {"rainfall_24h": 40.0}
        }
        response = self.client.post("/api/risk/analyze", json=payload)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result.get("status"), "model_scope_limited")
        self.assertIn("Assam flood prototype", result.get("message", ""))


if __name__ == "__main__":
    unittest.main()
