"""
RISK // INDIA — Post-Release Enhancement: Extended Citizen Safety Guidance Test Suite
====================================================================================
Comprehensive test suite validating:
1. Multi-hazard safety guidance coverage across all 6 hazards (Flood, Cyclone, Earthquake, Heatwave, Landslide, Severe Weather)
2. Lifecycle phases representation (BEFORE, DURING, AFTER)
3. Elimination of artificial 4-item limit
4. Priority distribution (CRITICAL, HIGH, RECOMMENDED)
5. Multi-category taxonomy (Water, Medical, Documents, Evacuation, Vulnerable Persons, Pets, Avoidance)
6. Disaster Management Act 2005 legal and operational demarcation notice
7. Emergency helpline integration (112, 1078, 1070, 108)
8. End-to-end FastAPI REST endpoint contracts
9. Zero synthetic data enforcement (synthetic_records == 0)
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
    extended_safety_engine,
    ExtendedCitizenSafetyEngine,
    SafetyPhase,
    SafetyPriority,
    SafetyCategory,
    SUPPORTED_HAZARDS
)


class TestExtendedCitizenSafetyGuidance(unittest.TestCase):
    """Validates extended citizen disaster safety guidance capabilities."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_extended_safety_engine_initialization(self):
        """Engine is initialized and holds guidance across all 6 hazards."""
        self.assertIsInstance(extended_safety_engine, ExtendedCitizenSafetyEngine)
        catalog = extended_safety_engine.get_catalog_summary()
        self.assertEqual(catalog["synthetic_records"], 0)
        self.assertTrue(catalog["total_catalog_items"] >= 20)

        for h in SUPPORTED_HAZARDS:
            self.assertIn(h, catalog["hazards"])
            h_data = catalog["hazards"][h]
            self.assertTrue(h_data["total_items"] >= 3, f"Hazard {h} has too few items")
            self.assertTrue(h_data["before_count"] >= 1, f"Hazard {h} missing BEFORE items")
            self.assertTrue(h_data["during_count"] >= 1, f"Hazard {h} missing DURING items")
            self.assertTrue(h_data["after_count"] >= 1, f"Hazard {h} missing AFTER items")

    def test_elimination_of_artificial_four_item_limit(self):
        """Extended catalog provides scalable multi-item architecture exceeding 4 items."""
        flood_guide = extended_safety_engine.get_complete_hazard_guide("FLOOD")
        self.assertGreater(flood_guide["total_action_items"], 4, "Flood guide must exceed artificial 4-item limit")
        self.assertTrue(len(flood_guide["phases"]["BEFORE"]["items"]) >= 4)
        self.assertTrue(len(flood_guide["phases"]["DURING"]["items"]) >= 3)
        self.assertTrue(len(flood_guide["phases"]["AFTER"]["items"]) >= 3)

    def test_multi_category_taxonomy_representation(self):
        """Safety items span essential life-safety categories."""
        all_items = extended_safety_engine.get_instructions()
        categories = set(i["category"] for i in all_items)

        self.assertIn(SafetyCategory.WATER_AND_FOOD.value, categories)
        self.assertIn(SafetyCategory.CRITICAL_DOCUMENTS.value, categories)
        self.assertIn(SafetyCategory.SAFE_ROUTES_EVACUATION.value, categories)
        self.assertIn(SafetyCategory.VULNERABLE_MEMBERS.value, categories)
        self.assertIn(SafetyCategory.UTILITY_SAFETY.value, categories)
        self.assertIn(SafetyCategory.AVOIDANCE_WHAT_NOT_TO_DO.value, categories)

    def test_priority_distribution(self):
        """Critical life-safety items are flagged with CRITICAL priority."""
        critical_items = extended_safety_engine.get_instructions(priority="CRITICAL")
        self.assertTrue(len(critical_items) >= 5)

        for item in critical_items:
            self.assertEqual(item["priority"], SafetyPriority.CRITICAL.value)
            self.assertTrue(len(item["reason"]) > 10, "Critical items must state a clear rationale")
            self.assertTrue(len(item["source"]) > 5, "Critical items must cite an authoritative standard")

    def test_statutory_demarcation_notice(self):
        """Hazard guides explicitly present Disaster Management Act 2005 demarcation."""
        for h in SUPPORTED_HAZARDS:
            guide = extended_safety_engine.get_complete_hazard_guide(h)
            self.assertIn("Disaster Management Act 2005", guide["statutory_notice"])
            self.assertIn("Mandatory evacuation directives are ordered exclusively by civil authorities", guide["statutory_notice"])

    def test_emergency_helpline_completeness(self):
        """Every guide provides verified pan-India emergency contact speed dials."""
        guide = extended_safety_engine.get_complete_hazard_guide("CYCLONE")
        contacts = guide["emergency_contacts"]
        self.assertEqual(contacts["national_emergency"], "112")
        self.assertEqual(contacts["ndma_disaster_helpline"], "1078")
        self.assertEqual(contacts["state_emergency_operation_center"], "1070")
        self.assertEqual(contacts["ambulance"], "108")

    def test_related_cascading_risk_cross_references(self):
        """Key instructions include cross-references to secondary cascading hazards."""
        flood_items = extended_safety_engine.get_instructions(hazard="FLOOD")
        items_with_cascading = [i for i in flood_items if i.get("related_cascading_risk")]
        self.assertTrue(len(items_with_cascading) >= 2)

    def test_zero_synthetic_data_guarantee(self):
        """Safety guides guarantee zero synthetic data."""
        for h in SUPPORTED_HAZARDS:
            guide = extended_safety_engine.get_complete_hazard_guide(h)
            self.assertEqual(guide["synthetic_records"], 0)

    # -------------------------------------------------------------------------
    # REST API Endpoint Tests
    # -------------------------------------------------------------------------
    def test_api_safety_guide_catalog_summary(self):
        """GET /api/future-risk/safety-guide returns catalog overview."""
        resp = self.client.get("/api/future-risk/safety-guide")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["synthetic_records"], 0)
        self.assertIn("supported_hazards", data)
        self.assertEqual(len(data["supported_hazards"]), 6)

    def test_api_safety_guide_hazard_filter(self):
        """GET /api/future-risk/safety-guide?hazard=HEATWAVE returns heatwave guide."""
        resp = self.client.get("/api/future-risk/safety-guide?hazard=HEATWAVE")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["hazard"], "HEATWAVE")
        self.assertIn("BEFORE", data["phases"])
        self.assertIn("DURING", data["phases"])
        self.assertIn("AFTER", data["phases"])
        self.assertEqual(data["synthetic_records"], 0)

    def test_api_safety_guide_priority_filter(self):
        """GET /api/future-risk/safety-guide?priority=CRITICAL returns filtered critical items."""
        resp = self.client.get("/api/future-risk/safety-guide?priority=CRITICAL")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["total_items"] >= 5)
        for item in data["items"]:
            self.assertEqual(item["priority"], "CRITICAL")

    def test_api_safety_guide_invalid_hazard_returns_400(self):
        """GET /api/future-risk/safety-guide?hazard=TORNADO returns HTTP 400."""
        resp = self.client.get("/api/future-risk/safety-guide?hazard=TORNADO")
        self.assertEqual(resp.status_code, 400)

    def test_api_region_safety_guide_endpoint(self):
        """GET /api/future-risk/{region}/safety-guide returns regional contextualized guide."""
        resp = self.client.get("/api/future-risk/assam/safety-guide")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["region"]["id"], "assam")
        self.assertEqual(data["hazard"], data["region"]["primary_hazard"])

    def test_api_region_safety_guide_invalid_region_returns_404(self):
        """GET /api/future-risk/{region}/safety-guide for invalid region returns HTTP 404."""
        resp = self.client.get("/api/future-risk/non-existent-state-123/safety-guide")
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
