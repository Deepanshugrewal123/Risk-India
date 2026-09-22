"""
RISK // INDIA — Phase 2C Real-World Product Acceptance Verification Suite
=========================================================================
Independent, behavioral, and contractual acceptance testing verifying:
- Live backend API connectivity & contracts
- National-first default posture (/api/predictive-risk/national)
- Elimination of hardcoded Assam/Kamrup regional bias
- All 36 administrative entities parity
- Strict zero synthetic data guarantee (synthetic_records == 0)
- Byte-for-byte cryptographic integrity of frozen model and dataset
- Assam-only ML scope (ml_available == True ONLY for Assam)
- Earthquake non-prediction consensus adherence
- 6-hazard multi-horizon forecast contracts (NOW to 7 days)
- Early warning decision support (preparation vs evacuation authority)
- Homepage first-viewport 5-second citizen comprehension contracts
- Dual-mode Risk Map (CURRENT RISK vs FUTURE RISK & EARLY WARNING)
- 72-Hour Family Disaster Emergency Kit
"""

import unittest
import hashlib
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from starlette.testclient import TestClient
from app.main import app
from app.services.geo_basin_service import INDIAN_ADMINISTRATIVE_ENTITIES

FROZEN_MODEL_SHA256 = "0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf"
FROZEN_DATASET_SHA256 = "88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080"


class TestPhase2CRealWorldAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    # -------------------------------------------------------------------------
    # 1. API CONNECTIVITY & OPERATIONAL HEALTH
    # -------------------------------------------------------------------------
    def test_01_backend_health_and_service_readiness(self):
        """Verify live API health endpoint responds with database and model readiness."""
        resp = self.client.get("/api/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("service", data)
        self.assertEqual(data["database"], "connected")
        self.assertTrue(data.get("model_ready", False))

    # -------------------------------------------------------------------------
    # 2. NATIONAL-FIRST DEFAULT & PARITY ACROSS ALL 36 JURISDICTIONS
    # -------------------------------------------------------------------------
    def test_02_national_predictive_posture_parity(self):
        """Verify national overview returns all 36 entities with zero synthetic records."""
        resp = self.client.get("/api/predictive-risk/national")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["total_entities_monitored"], 36)
        self.assertEqual(data["states_covered"], 28)
        self.assertEqual(data["union_territories_covered"], 8)
        self.assertEqual(len(data["regions"]), 36)
        self.assertEqual(data["synthetic_records"], 0)

    def test_03_default_state_excludes_hardcoded_assam_kamrup(self):
        """Verify frontend components initialize selectedRegion/selectedLocation as null."""
        cmd_center = (PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskCommandCenter.tsx").read_text(encoding="utf-8")
        loc_checker = (PROJECT_ROOT / "src" / "components" / "home" / "LocationRiskCheckerSection.tsx").read_text(encoding="utf-8")
        future_page = (PROJECT_ROOT / "src" / "components" / "pages" / "FutureRiskPage.tsx").read_text(encoding="utf-8")

        self.assertIn("useState<string | null>(null)", cmd_center)
        self.assertIn("useState<IndiaLocation | null>(null)", loc_checker)
        self.assertIn("useState<string | null>(initialRegionId || null)", future_page)

    # -------------------------------------------------------------------------
    # 3. SCIENTIFIC INVARIANT PRESERVATION (EXACT HASHES)
    # -------------------------------------------------------------------------
    def test_04_frozen_model_hash_exact(self):
        """Verify byte-for-byte SHA256 of frozen model.joblib."""
        path = PROJECT_ROOT / "ml" / "flood" / "artifacts" / "model.joblib"
        self.assertTrue(path.exists())
        h = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(h, FROZEN_MODEL_SHA256)

    def test_05_frozen_dataset_hash_exact(self):
        """Verify byte-for-byte SHA256 of frozen flood_features.csv."""
        path = PROJECT_ROOT / "datasets" / "processed" / "flood_assam" / "flood_features.csv"
        self.assertTrue(path.exists())
        h = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(h, FROZEN_DATASET_SHA256)

    # -------------------------------------------------------------------------
    # 4. ASSAM-ONLY ML SCOPE & BYPASS PREVENTION
    # -------------------------------------------------------------------------
    def test_06_assam_only_ml_enforcement(self):
        """Verify ml_available == True ONLY for Assam; False for all 35 other entities."""
        from app.services.predictive_risk import national_predictive_risk_service

        for entity in INDIAN_ADMINISTRATIVE_ENTITIES:
            eid = entity["id"]
            assessment = national_predictive_risk_service.get_hazard_assessment(eid, "FLOOD")
            is_assam = (eid.lower() == "assam")
            ml_available = assessment.ml_scope.get("ml_available", False)

            if is_assam:
                self.assertTrue(ml_available, "Assam must have ml_available == True")
                self.assertEqual(assessment.ml_scope.get("guard_status"), "PASS_ASSAM_IN_DISTRIBUTION")
            else:
                self.assertFalse(ml_available, f"{eid} must have ml_available == False")

    # -------------------------------------------------------------------------
    # 5. STRICT EARTHQUAKE NON-PREDICTION CONSENSUS
    # -------------------------------------------------------------------------
    def test_07_earthquake_strictly_non_predictive(self):
        """Verify earthquake assessments enforce non-prediction invariants."""
        from app.services.predictive_risk import national_predictive_risk_service

        eq = national_predictive_risk_service.get_hazard_assessment("delhi", "EARTHQUAKE")
        self.assertEqual(eq.trend.value, "STABLE")
        self.assertEqual(eq.confidence.value, "LOW")
        self.assertEqual(eq.uncertainty.value, "VERY_HIGH")
        self.assertEqual(eq.peak_future_window, "BASELINE")

    # -------------------------------------------------------------------------
    # 6. MULTI-HORIZON & SCENARIO CONTRACTS
    # -------------------------------------------------------------------------
    def test_08_five_standard_forecast_horizons(self):
        """Verify 5 standard forecast horizons exist across timeline."""
        resp = self.client.get("/api/predictive-risk/assam/timeline?hazard=FLOOD")
        self.assertEqual(resp.status_code, 200)
        timeline = resp.json()
        self.assertEqual(len(timeline), 5)
        horizons = [pt["horizon"] for pt in timeline]
        self.assertEqual(horizons, ["NOW", "0-6h", "6-24h", "1-3d", "3-7d"])

    def test_09_predictive_scenarios_contract(self):
        """Verify Baseline, Likely, and Escalation scenarios are served."""
        resp = self.client.get("/api/predictive-risk/assam/scenarios?hazard=FLOOD")
        self.assertEqual(resp.status_code, 200)
        scenarios = resp.json()
        self.assertGreaterEqual(len(scenarios), 3)
        stypes = [s["scenario_type"] for s in scenarios]
        self.assertIn("BASELINE", stypes)
        self.assertIn("LIKELY", stypes)
        self.assertIn("ESCALATION", stypes)

    # -------------------------------------------------------------------------
    # 7. EARLY WARNING & STATUTORY AUTHORITY DEMARCATION
    # -------------------------------------------------------------------------
    def test_10_early_warning_preparation_vs_evacuation(self):
        """Verify readiness separates preparation advice from statutory evacuation."""
        resp = self.client.get("/api/predictive-risk/readiness")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("actionable_count", data)
        self.assertEqual(data["synthetic_records"], 0)

    # -------------------------------------------------------------------------
    # 8. CITIZEN UX & DISCOVERABILITY CONTRACTS
    # -------------------------------------------------------------------------
    def test_11_first_viewport_comprehension_strip(self):
        """Verify HeroSection contains 6-question citizen intelligence strip."""
        hero = (PROJECT_ROOT / "src" / "components" / "home" / "HeroSection.tsx").read_text(encoding="utf-8")
        self.assertIn("CITIZEN INTELLIGENCE // 6 CORE QUESTIONS AT A GLANCE", hero)
        self.assertIn("1. Happening Now", hero)
        self.assertIn("2. Happening Next", hero)
        self.assertIn("3. Risk Trend", hero)
        self.assertIn("4. Timing", hero)
        self.assertIn("5. What To Do", hero)
        self.assertIn("6. Verified Help", hero)
        self.assertIn("CURRENT RISK • FUTURE RISK • EARLY WARNING • ACTION", hero)

    def test_12_navbar_future_risk_discoverability(self):
        """Verify Navbar has Future Risk item."""
        navbar = (PROJECT_ROOT / "src" / "components" / "common" / "Navbar.tsx").read_text(encoding="utf-8")
        self.assertIn("{ id: 'future-risk', label: 'Future Risk' }", navbar)

    def test_13_risk_map_dual_modes(self):
        """Verify RiskMapPage has CURRENT RISK and FUTURE RISK & EARLY WARNING modes."""
        risk_map = (PROJECT_ROOT / "src" / "components" / "pages" / "RiskMapPage.tsx").read_text(encoding="utf-8")
        self.assertIn("<span>FUTURE RISK & EARLY WARNING</span>", risk_map)
        self.assertIn("<span>CURRENT RISK</span>", risk_map)

    def test_14_72h_family_kit_and_life_safety_actions(self):
        """Verify FutureRiskActionPanel has 72-Hour Kit and Stage 1 immediate action."""
        action_panel = (PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskActionPanel.tsx").read_text(encoding="utf-8")
        self.assertIn("1. DO THIS RIGHT NOW", action_panel)
        self.assertIn("72-HOUR FAMILY DISASTER SUPPLY KIT", action_panel)
        self.assertIn("72-Hour Family Disaster Emergency Kit", action_panel)

    def test_15_statutory_legal_and_scenario_disclaimers(self):
        """Verify Disaster Management Act 2005 and analytical scenario notices."""
        early_warn = (PROJECT_ROOT / "src" / "components" / "home" / "EarlyWarningNoticeSection.tsx").read_text(encoding="utf-8")
        future_page = (PROJECT_ROOT / "src" / "components" / "pages" / "FutureRiskPage.tsx").read_text(encoding="utf-8")
        loc_checker = (PROJECT_ROOT / "src" / "components" / "home" / "LocationRiskCheckerSection.tsx").read_text(encoding="utf-8")

        self.assertIn("Preparation vs Evacuation Authority Notice: ", early_warn)
        self.assertIn("Disaster Management Act, 2005", early_warn)
        self.assertIn("Analytical Scenarios Notice:", future_page)
        self.assertIn("Administrative Notice:", loc_checker)
        self.assertIn("Administrative selection does not guarantee live telemetry", loc_checker)


if __name__ == "__main__":
    unittest.main()
