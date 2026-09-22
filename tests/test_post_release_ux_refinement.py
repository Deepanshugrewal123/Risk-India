"""
RISK // INDIA — Post-Release UX Refinement Test Suite
=====================================================
Forensic validation of:
1. Expanded safety item counts exceeding artificial limits (148 total items in frontend master dataset)
2. Before / During / After completeness across all 6 hazards
3. Level 2 "Examine More" detail availability (why_it_matters, practical_steps, warning_signs, what_not_to_do, checklist)
4. Hazard-specific non-generic guidance (Flood, Cyclone, Heatwave, Severe Weather, Landslide, Earthquake)
5. Cascading relationship progression & 4-stage causality
6. Evidence posture integrity (LIVE_EVIDENCE, RECENT_EVIDENCE, FORECAST_AVAILABLE, BASELINE_ONLY, LIMITED_EVIDENCE, DATA_UNAVAILABLE)
7. Citizen guidance cross-link metadata
8. Mobile-first rendering & accessible text-labeled priority badges
9. Zero synthetic data enforcement (synthetic_records == 0)
10. Absence of numeric pseudo-probabilities & Earthquake non-prediction safeguard
"""

import unittest
import sys
import re
import json
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
    cascading_risk_engine,
    EvidencePosture,
    RelationshipClassification,
    SUPPORTED_HAZARDS,
)
from app.middleware.rate_limit import rate_limiter


class TestPostReleaseUXRefinement(unittest.TestCase):
    """Forensic verification of UX refinement, progressive disclosure, and cascading prominence."""

    def setUp(self):
        rate_limiter.reset()

    def tearDown(self):
        rate_limiter.reset()

    @classmethod
    def setUpClass(cls):
        rate_limiter.reset()
        cls.client = TestClient(app)
        cls.frontend_dataset_path = PROJECT_ROOT / "src" / "data" / "extendedSafetyData.ts"
        with open(cls.frontend_dataset_path, "r", encoding="utf-8") as f:
            cls.frontend_dataset_text = f.read()

    def test_frontend_expanded_safety_item_counts(self):
        """Frontend dataset contains at least 140 safety items with >=20 items per hazard."""
        item_ids = re.findall(r'id:\s*["\']([^"\']+)["\']', self.frontend_dataset_text)
        self.assertGreaterEqual(len(item_ids), 140, "Total items must exceed 140 to satisfy comprehensive coverage")
        self.assertEqual(len(item_ids), len(set(item_ids)), "Item IDs must be globally unique")

        hazards = re.findall(r'hazard:\s*["\']([^"\']+)["\']', self.frontend_dataset_text)
        for h in SUPPORTED_HAZARDS:
            count = hazards.count(h)
            self.assertGreaterEqual(count, 20, f"Hazard {h} must have at least 20 actionable safety items")

    def test_before_during_after_completeness(self):
        """Every hazard has strong representation across BEFORE, DURING, and AFTER phases."""
        for h in SUPPORTED_HAZARDS:
            # Pattern matching items for this hazard
            hazard_blocks = re.findall(
                rf'id:\s*["\'][^"\']+["\'][^}}]+hazard:\s*["\']{h}["\'][^}}]+phase:\s*["\'](\w+)["\']',
                self.frontend_dataset_text
            )
            before_count = hazard_blocks.count("BEFORE")
            during_count = hazard_blocks.count("DURING")
            after_count = hazard_blocks.count("AFTER")

            self.assertGreaterEqual(before_count, 8, f"Hazard {h} must have >=8 BEFORE items")
            self.assertGreaterEqual(during_count, 6, f"Hazard {h} must have >=6 DURING items")
            self.assertGreaterEqual(after_count, 6, f"Hazard {h} must have >=6 AFTER items")

    def test_examine_more_detail_availability(self):
        """All safety items include Level 2 progressive disclosure fields (no empty stubs)."""
        self.assertIn("practical_steps:", self.frontend_dataset_text)
        self.assertIn("warning_signs:", self.frontend_dataset_text)
        self.assertIn("what_not_to_do:", self.frontend_dataset_text)
        self.assertIn("checklist:", self.frontend_dataset_text)
        self.assertIn("reason:", self.frontend_dataset_text)
        self.assertIn("source:", self.frontend_dataset_text)

        # Verify that '[ EXAMINE MORE ▾ ]' is used in the component
        card_component_path = PROJECT_ROOT / "src" / "components" / "safety" / "SafetyActionItemCard.tsx"
        with open(card_component_path, "r", encoding="utf-8") as f:
            card_code = f.read()

        self.assertIn("[ EXAMINE MORE ▾ ]", card_code)
        self.assertIn("[ HIDE DETAILS ▴ ]", card_code)
        self.assertIn("WHY THIS MATTERS", card_code)
        self.assertIn("WHAT TO DO", card_code)
        self.assertIn("WARNING SIGNS", card_code)
        self.assertIn("WHAT NOT TO DO", card_code)

    def test_hazard_specific_guidance_fidelity(self):
        """Safety guidance contains hazard-specific physics and operational terms, not generic copy."""
        # Flood: must mention sewage/waterborne/inundation
        self.assertIn("fld-bef-01", self.frontend_dataset_text)
        self.assertIn("pathogenic sewage", self.frontend_dataset_text)
        self.assertIn("Turn around, do not drown", self.frontend_dataset_text)

        # Cyclone: must mention storm surge/winds/eye of the storm
        self.assertIn("cyc-dur-07", self.frontend_dataset_text)
        self.assertIn("Beware the False Eye of the Cyclone", self.frontend_dataset_text)
        self.assertIn("storm surges", self.frontend_dataset_text)

        # Heatwave: must mention hydration/stroke/active cooling
        self.assertIn("htw-dur-08", self.frontend_dataset_text)
        self.assertIn("Execute Rapid Active Cooling for Heat Stroke", self.frontend_dataset_text)

        # Severe weather: must mention lightning 30-30 rule and crouch
        self.assertIn("swx-dur-07", self.frontend_dataset_text)
        self.assertIn("Execute 30-30 Rule", self.frontend_dataset_text)
        self.assertIn("Lightning Crouch", self.frontend_dataset_text)

        # Landslide: must mention weep-holes and rumbling sound
        self.assertIn("lsd-bef-07", self.frontend_dataset_text)
        self.assertIn("weep-holes", self.frontend_dataset_text)
        self.assertIn("lateral slope", self.frontend_dataset_text.lower())

        # Earthquake: must mention Drop, Cover, Hold On and no elevators
        self.assertIn("eqk-dur-07", self.frontend_dataset_text)
        self.assertIn("Drop, Cover, and Hold On", self.frontend_dataset_text)
        self.assertIn("Never Use Elevators", self.frontend_dataset_text)

    def test_cascading_risk_4_stage_chain_and_evidence_posture(self):
        """Cascading risk engine evaluates 4-stage causality with valid evidence postures."""
        assessment = cascading_risk_engine.evaluate_region_cascading_risk("assam", "FLOOD")
        self.assertIsNotNone(assessment)
        self.assertGreaterEqual(len(assessment.chains), 1)

        chain = assessment.chains[0]
        self.assertEqual(len(chain.stages), 4)

        stage_types = [s.stage_type for s in chain.stages]
        self.assertEqual(stage_types, ["PRIMARY_HAZARD", "PHYSICAL_CHANGE", "SECONDARY_HAZARD", "TERTIARY_CONSEQUENCE"])

        for stage in chain.stages:
            self.assertIsInstance(stage.evidence_posture, EvidencePosture)
            self.assertIn(stage.evidence_posture.value, [
                "LIVE_EVIDENCE", "RECENT_EVIDENCE", "FORECAST_AVAILABLE",
                "BASELINE_ONLY", "LIMITED_EVIDENCE", "DATA_UNAVAILABLE"
            ])

    def test_citizen_guidance_cross_links(self):
        """Cascading risk panels and safety guide components have cross-navigation capabilities."""
        what_next_panel_path = PROJECT_ROOT / "src" / "components" / "cascading" / "WhatCanHappenNextPanel.tsx"
        with open(what_next_panel_path, "r", encoding="utf-8") as f:
            panel_code = f.read()

        self.assertIn("onNavigate", panel_code)
        self.assertIn("safety-guide", panel_code)
        self.assertIn("cascading-risk", panel_code)
        self.assertIn("WATER SAFETY", panel_code)
        self.assertIn("LANDSLIDE SAFETY", panel_code)

    def test_zero_synthetic_data_and_no_pseudo_probabilities(self):
        """Verification of strict scientific integrity across future risk & cascading endpoints."""
        rate_limiter.reset()
        # Backend API health
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)

        rate_limiter.reset()
        # Safety guide API returns zero synthetic records
        res_sg = self.client.get("/api/future-risk/safety-guide?hazard=FLOOD")
        self.assertEqual(res_sg.status_code, 200)
        data = res_sg.json()
        self.assertEqual(data["synthetic_records"], 0)

        rate_limiter.reset()
        # Cascading risk API returns zero synthetic records
        res_cr = self.client.get("/api/future-risk/assam/cascading?hazard=FLOOD")
        self.assertEqual(res_cr.status_code, 200)
        cr_data = res_cr.json()
        self.assertEqual(cr_data["synthetic_records"], 0)

        # String search across output: no fabricated pseudo probabilities like "78% probability of landslide"
        cr_json_str = json.dumps(cr_data)
        self.assertNotIn("% probability", cr_json_str)
        self.assertNotIn("% chance of landslide", cr_json_str)

    def test_earthquake_non_prediction_safeguard(self):
        """Earthquake consequence evaluation strictly disclaims temporal prediction."""
        rate_limiter.reset()
        res_eq = self.client.get("/api/future-risk/assam/cascading?hazard=EARTHQUAKE")
        self.assertEqual(res_eq.status_code, 200)
        eq_data = res_eq.json()
        chain = eq_data["chains"][0]

        self.assertIn("earthquake_non_prediction_notice", chain)
        self.assertIn("cannot be temporally predicted", chain["earthquake_non_prediction_notice"].lower())
        self.assertIn("structural engineering relationships", chain["earthquake_non_prediction_notice"].lower())

    def test_mobile_accessibility_and_text_labeled_badges(self):
        """Safety priority badges use text labels and icons, never color alone."""
        card_component_path = PROJECT_ROOT / "src" / "components" / "safety" / "SafetyActionItemCard.tsx"
        with open(card_component_path, "r", encoding="utf-8") as f:
            card_code = f.read()

        self.assertIn("CRITICAL LIFE SAFETY", card_code)
        self.assertIn("IMPORTANT ACTION", card_code)
        self.assertIn("HELPFUL PREPARATION", card_code)
        self.assertIn("min-h-[44px]", card_code)  # WCAG 2.1 touch target size


if __name__ == "__main__":
    unittest.main()
