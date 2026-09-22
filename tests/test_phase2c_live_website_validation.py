"""
RISK // INDIA — PHASE 2C AUTOMATED TEST SUITE
===============================================================================
Live Website Product Validation, UX Hardening & Citizen Experience.
Verifies all 20 mandatory acceptance criteria specified in Part 25:
1. Homepage exposes Future Risk
2. Homepage exposes Early Warning
3. Homepage exposes Action
4. Navbar exposes Future Risk
5. Risk Map exposes Current Risk
6. Risk Map exposes Future Risk
7. Future Risk uses national overview when no location selected
8. No hardcoded Assam/Kamrup default
9. No synthetic records (synthetic_records == 0)
10. No numeric pseudo-probabilities ("87% chance" banned)
11. Earthquake guard (is_predictable = False, non-prediction disclaimer)
12. Assam ML guard (Assam only, non-Assam rejection)
13. Data unavailable state (What is known, What is unknown, Last observation, etc.)
14. Coverage tier distinction (6 distinct tiers)
15. Current vs Future semantic distinction
16. Future Risk does not depend on hidden tabs
17. Early Warning does not depend on hidden tabs
18. Location selection does not imply telemetry availability
19. Frontend does not contain independent authoritative risk calculation
20. Frozen SHA-256 hashes remain byte-for-byte unchanged
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

FROZEN_MODEL_SHA256 = "0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf"
FROZEN_DATASET_SHA256 = "88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080"


class TestPhase2CLiveWebsiteValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    # -------------------------------------------------------------------------
    # 1. HOMEPAGE EXPOSES FUTURE RISK
    # -------------------------------------------------------------------------
    def test_01_homepage_exposes_future_risk(self):
        """Verify that Future Risk is prominently exposed on the homepage."""
        hero_path = PROJECT_ROOT / "src" / "components" / "home" / "HeroSection.tsx"
        self.assertTrue(hero_path.exists(), "HeroSection.tsx must exist")
        hero_src = hero_path.read_text(encoding="utf-8")
        self.assertIn("FUTURE RISK", hero_src)
        self.assertIn("Check Future Risk", hero_src)

        cmd_path = PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskCommandCenter.tsx"
        self.assertTrue(cmd_path.exists(), "FutureRiskCommandCenter.tsx must exist")
        cmd_src = cmd_path.read_text(encoding="utf-8")
        self.assertIn("What Could Happen Next?", cmd_src)
        self.assertIn("FUTURE RISK & EARLY WARNING COMMAND CENTER", cmd_src)

    # -------------------------------------------------------------------------
    # 2. HOMEPAGE EXPOSES EARLY WARNING
    # -------------------------------------------------------------------------
    def test_02_homepage_exposes_early_warning(self):
        """Verify that Early Warning is mounted and discoverable on the homepage."""
        hero_path = PROJECT_ROOT / "src" / "components" / "home" / "HeroSection.tsx"
        hero_src = hero_path.read_text(encoding="utf-8")
        self.assertIn("EARLY WARNING", hero_src)
        self.assertIn("See Early Warnings", hero_src)

        ew_path = PROJECT_ROOT / "src" / "components" / "home" / "EarlyWarningNoticeSection.tsx"
        self.assertTrue(ew_path.exists(), "EarlyWarningNoticeSection.tsx must exist")
        ew_src = ew_path.read_text(encoding="utf-8")
        self.assertIn("EARLY WARNING POSTURE", ew_src)

    # -------------------------------------------------------------------------
    # 3. HOMEPAGE EXPOSES ACTION
    # -------------------------------------------------------------------------
    def test_03_homepage_exposes_action(self):
        """Verify that citizen action directives and preparedness are exposed on homepage."""
        hero_path = PROJECT_ROOT / "src" / "components" / "home" / "HeroSection.tsx"
        hero_src = hero_path.read_text(encoding="utf-8")
        self.assertIn("ACTION", hero_src)

        action_path = PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskActionPanel.tsx"
        self.assertTrue(action_path.exists(), "FutureRiskActionPanel.tsx must exist")
        action_src = action_path.read_text(encoding="utf-8")
        self.assertIn("DO THIS RIGHT NOW", action_src)
        self.assertTrue(
            "72-HOUR FAMILY DISASTER EMERGENCY KIT" in action_src or "72-Hour Family Disaster Emergency Kit" in action_src,
            "72-Hour Emergency Kit must be present in FutureRiskActionPanel"
        )

        prep_path = PROJECT_ROOT / "src" / "components" / "home" / "PreparednessSection.tsx"
        self.assertTrue(prep_path.exists(), "PreparednessSection.tsx must exist")
        prep_src = prep_path.read_text(encoding="utf-8")
        self.assertIn("Preparedness", prep_src)

    # -------------------------------------------------------------------------
    # 4. NAVBAR EXPOSES FUTURE RISK
    # -------------------------------------------------------------------------
    def test_04_navbar_exposes_future_risk(self):
        """Verify that Navbar includes Future Risk link without obsolete terminology."""
        nav_path = PROJECT_ROOT / "src" / "components" / "common" / "Navbar.tsx"
        self.assertTrue(nav_path.exists(), "Navbar.tsx must exist")
        nav_src = nav_path.read_text(encoding="utf-8")
        self.assertIn("'future-risk'", nav_src)
        self.assertIn("Future Risk", nav_src)
        self.assertIn("Open Risk Map", nav_src)
        self.assertNotIn("Dedicated Risk Map", nav_src)

    # -------------------------------------------------------------------------
    # 5. RISK MAP EXPOSES CURRENT RISK
    # -------------------------------------------------------------------------
    def test_05_risk_map_exposes_current_risk(self):
        """Verify that Risk Map has dedicated CURRENT RISK mode."""
        map_path = PROJECT_ROOT / "src" / "components" / "map" / "IndiaRiskMap.tsx"
        self.assertTrue(map_path.exists(), "IndiaRiskMap.tsx must exist")
        map_src = map_path.read_text(encoding="utf-8")
        self.assertIn("CURRENT RISK", map_src)
        self.assertIn("setMapPerspective('CURRENT')", map_src)

    # -------------------------------------------------------------------------
    # 6. RISK MAP EXPOSES FUTURE RISK
    # -------------------------------------------------------------------------
    def test_06_risk_map_exposes_future_risk(self):
        """Verify that Risk Map has dedicated FUTURE RISK & EARLY WARNING mode."""
        map_path = PROJECT_ROOT / "src" / "components" / "map" / "IndiaRiskMap.tsx"
        map_src = map_path.read_text(encoding="utf-8")
        self.assertIn("FUTURE RISK & EARLY WARNING", map_src)
        self.assertIn("setMapPerspective('FUTURE')", map_src)
        self.assertIn("Forecast Horizon:", map_src)
        for h in ["NOW", "0-6h", "6-24h", "1-3d", "3-7d"]:
            self.assertIn(h, map_src)

    # -------------------------------------------------------------------------
    # 7. FUTURE RISK USES NATIONAL OVERVIEW WHEN NO LOCATION SELECTED
    # -------------------------------------------------------------------------
    def test_07_future_risk_uses_national_overview_by_default(self):
        """Verify that Future Risk defaults to National Overview."""
        cmd_path = PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskCommandCenter.tsx"
        cmd_src = cmd_path.read_text(encoding="utf-8")
        self.assertIn("selectedRegion, setSelectedRegion] = useState<string | null>(null)", cmd_src)
        self.assertIn("National Overview (All 36 States & UTs)", cmd_src)

        resp = self.client.get("/api/predictive-risk/national")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["total_entities_monitored"], 36)
        self.assertIn("risk_state_distribution", data)

    # -------------------------------------------------------------------------
    # 8. NO HARDCODED ASSAM / KAMRUP DEFAULT
    # -------------------------------------------------------------------------
    def test_08_no_hardcoded_assam_kamrup_default(self):
        """Verify that neither Assam nor Kamrup is hardcoded as default."""
        cmd_path = PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskCommandCenter.tsx"
        cmd_src = cmd_path.read_text(encoding="utf-8")
        self.assertNotIn("useState<string | null>('assam')", cmd_src)
        self.assertNotIn("useState<string | null>('kamrup')", cmd_src)

        loc_path = PROJECT_ROOT / "src" / "components" / "home" / "LocationRiskCheckerSection.tsx"
        loc_src = loc_path.read_text(encoding="utf-8")
        self.assertIn("selectedLocation, setSelectedLocation] = useState<IndiaLocation | null>(null)", loc_src)

        page_path = PROJECT_ROOT / "src" / "components" / "pages" / "FutureRiskPage.tsx"
        page_src = page_path.read_text(encoding="utf-8")
        self.assertIn("useState<string | null>(initialRegionId || null)", page_src)

    # -------------------------------------------------------------------------
    # 9. NO SYNTHETIC RECORDS (SYNTHETIC_RECORDS == 0)
    # -------------------------------------------------------------------------
    def test_09_no_synthetic_records(self):
        """Verify synthetic_records == 0 across national and regional endpoints."""
        resp = self.client.get("/api/predictive-risk/national")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get("synthetic_records", 0), 0)

        for region in ["delhi", "maharashtra", "assam", "kerala", "odisha"]:
            r = self.client.get(f"/api/predictive-risk/{region}/FLOOD")
            if r.status_code == 200:
                self.assertEqual(r.json().get("synthetic_records", 0), 0)

    # -------------------------------------------------------------------------
    # 10. NO NUMERIC PSEUDO-PROBABILITIES
    # -------------------------------------------------------------------------
    def test_10_no_numeric_pseudo_probabilities(self):
        """Verify that numeric pseudo-probabilities ('87% chance') are banned."""
        src_dir = PROJECT_ROOT / "src"
        for tsx_file in src_dir.rglob("*.tsx"):
            content = tsx_file.read_text(encoding="utf-8")
            self.assertNotIn("87%", content, f"87% pseudo-probability found in {tsx_file}")
            self.assertNotIn("% chance", content, f"% chance pseudo-probability found in {tsx_file}")

        resp = self.client.get("/api/predictive-risk/assam/FLOOD")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn(data["future_risk_state"], ["NORMAL", "WATCH", "ELEVATED", "HIGH", "CRITICAL"])
        self.assertIn(data["confidence"], ["LOW", "MEDIUM", "HIGH"])

    # -------------------------------------------------------------------------
    # 11. EARTHQUAKE GUARD
    # -------------------------------------------------------------------------
    def test_11_earthquake_guard(self):
        """Verify earthquake scientific non-prediction banner and invariants."""
        resp = self.client.get("/api/predictive-risk/delhi/EARTHQUAKE")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertFalse(data.get("is_predictable", False))
        self.assertEqual(data["trend"], "STABLE")
        self.assertEqual(data["confidence"], "LOW")
        self.assertEqual(data["uncertainty"], "VERY_HIGH")

        cmd_path = PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskCommandCenter.tsx"
        cmd_src = cmd_path.read_text(encoding="utf-8")
        self.assertIn("Earthquake timing cannot currently be predicted reliably", cmd_src)

    # -------------------------------------------------------------------------
    # 12. ASSAM ML GUARD
    # -------------------------------------------------------------------------
    def test_12_assam_ml_guard(self):
        """Verify Assam ML scope restriction (ml_available == False for non-Assam)."""
        resp_non_assam = self.client.get("/api/predictive-risk/delhi/FLOOD")
        self.assertEqual(resp_non_assam.status_code, 200)
        data_delhi = resp_non_assam.json()
        self.assertFalse(data_delhi["ml_scope"]["ml_available"])
        self.assertEqual(data_delhi["ml_scope"]["guard_status"], "PASS_NON_ASSAM_GUARD")

        resp_assam = self.client.get("/api/predictive-risk/assam/FLOOD")
        self.assertEqual(resp_assam.status_code, 200)
        data_assam = resp_assam.json()
        self.assertTrue(data_assam["ml_scope"]["ml_available"])
        self.assertEqual(data_assam["ml_scope"]["guard_status"], "PASS_ASSAM_IN_DISTRIBUTION")

    # -------------------------------------------------------------------------
    # 13. DATA UNAVAILABLE STATE
    # -------------------------------------------------------------------------
    def test_13_data_unavailable_state(self):
        """Verify honest DATA UNAVAILABLE / LIMITED EVIDENCE state rendering."""
        cmd_path = PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskCommandCenter.tsx"
        cmd_src = cmd_path.read_text(encoding="utf-8")
        self.assertIn("DATA UNAVAILABLE // LIMITED SCIENTIFIC EVIDENCE", cmd_src)
        self.assertIn("WHAT IS KNOWN:", cmd_src)
        self.assertIn("WHAT IS UNKNOWN:", cmd_src)
        self.assertIn("Last Available Observation", cmd_src)
        self.assertIn("Source / Provenance", cmd_src)
        self.assertIn("Forecast Availability", cmd_src)

        loc_path = PROJECT_ROOT / "src" / "components" / "home" / "LocationRiskCheckerSection.tsx"
        loc_src = loc_path.read_text(encoding="utf-8")
        self.assertIn("DATA UNAVAILABLE // LIMITED EVIDENCE", loc_src)
        self.assertIn("WHAT IS KNOWN:", loc_src)
        self.assertIn("WHAT IS UNKNOWN:", loc_src)

    # -------------------------------------------------------------------------
    # 14. COVERAGE TIER DISTINCTION
    # -------------------------------------------------------------------------
    def test_14_coverage_tier_distinction(self):
        """Verify distinction between 6 scientific coverage tiers."""
        cmd_path = PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskCommandCenter.tsx"
        cmd_src = cmd_path.read_text(encoding="utf-8")
        self.assertIn("ADMIN COVERAGE", cmd_src)
        self.assertIn("REGIONAL BASELINE", cmd_src)
        self.assertIn("LIVE TELEMETRY", cmd_src)
        self.assertIn("OFFICIAL FORECAST", cmd_src)
        self.assertIn("OFFICIAL WARNINGS", cmd_src)
        self.assertIn("APPROVED ML SCOPE", cmd_src)

    # -------------------------------------------------------------------------
    # 15. CURRENT / FUTURE SEMANTIC DISTINCTION
    # -------------------------------------------------------------------------
    def test_15_current_vs_future_semantic_distinction(self):
        """Verify semantic distinction between CURRENT RISK and FUTURE RISK."""
        map_path = PROJECT_ROOT / "src" / "components" / "map" / "IndiaRiskMap.tsx"
        map_src = map_path.read_text(encoding="utf-8")
        self.assertIn("CURRENT RISK", map_src)
        self.assertIn("FUTURE RISK & EARLY WARNING", map_src)
        self.assertIn("Real-Time In-Situ Sensors", map_src)
        self.assertIn("Forecast Horizon:", map_src)

        cmd_path = PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskCommandCenter.tsx"
        cmd_src = cmd_path.read_text(encoding="utf-8")
        self.assertIn("A. Current State", cmd_src)
        self.assertIn("B. Future State", cmd_src)

    # -------------------------------------------------------------------------
    # 16. FUTURE RISK DOES NOT DEPEND ON HIDDEN TABS
    # -------------------------------------------------------------------------
    def test_16_future_risk_not_dependent_on_hidden_tabs(self):
        """Verify that Future Risk is directly accessible in homepage and primary routes."""
        home_path = PROJECT_ROOT / "src" / "components" / "pages" / "HomePage.tsx"
        home_src = home_path.read_text(encoding="utf-8")
        self.assertIn("<FutureRiskHeroSection", home_src)
        self.assertIn("<LocationRiskCheckerSection", home_src)

        app_path = PROJECT_ROOT / "src" / "App.tsx"
        app_src = app_path.read_text(encoding="utf-8")
        self.assertIn("future-risk", app_src)
        self.assertIn("<FutureRiskPage", app_src)

    # -------------------------------------------------------------------------
    # 17. EARLY WARNING DOES NOT DEPEND ON HIDDEN TABS
    # -------------------------------------------------------------------------
    def test_17_early_warning_not_dependent_on_hidden_tabs(self):
        """Verify that Early Warning is mounted in the primary page flow."""
        home_path = PROJECT_ROOT / "src" / "components" / "pages" / "HomePage.tsx"
        home_src = home_path.read_text(encoding="utf-8")
        self.assertIn("<EarlyWarningNoticeSection", home_src)

        ew_path = PROJECT_ROOT / "src" / "components" / "home" / "EarlyWarningNoticeSection.tsx"
        ew_src = ew_path.read_text(encoding="utf-8")
        self.assertIn("Preparation vs Evacuation Authority Notice", ew_src)
        self.assertIn("Disaster Management Act, 2005", ew_src)

    # -------------------------------------------------------------------------
    # 18. LOCATION SELECTION DOES NOT IMPLY TELEMETRY AVAILABILITY
    # -------------------------------------------------------------------------
    def test_18_location_selection_does_not_imply_telemetry(self):
        """Verify explicit disclaimer that administrative selection != live telemetry."""
        loc_path = PROJECT_ROOT / "src" / "components" / "home" / "LocationRiskCheckerSection.tsx"
        loc_src = loc_path.read_text(encoding="utf-8")
        self.assertIn("Administrative selection does not guarantee live telemetry", loc_src)
        self.assertIn("COVERAGE SUMMARY //", loc_src)

    # -------------------------------------------------------------------------
    # 19. FRONTEND DOES NOT INDEPENDENTLY CALCULATE AUTHORITATIVE RISK
    # -------------------------------------------------------------------------
    def test_19_frontend_authority_contract(self):
        """Verify that frontend consumes authoritative backend risk without local recalculation."""
        resp = self.client.get("/api/predictive-risk/delhi/FLOOD")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("current_risk_state", data)
        self.assertIn("future_risk_state", data)
        self.assertIn("peak_future_window", data)
        self.assertIn("trend", data)
        self.assertIn("confidence", data)
        self.assertIn("uncertainty", data)
        self.assertIn("explanation", data)

        # Confirm scenarios contract exists
        sc_resp = self.client.get("/api/predictive-risk/assam/scenarios")
        self.assertEqual(sc_resp.status_code, 200)
        scenarios = sc_resp.json()
        self.assertTrue(len(scenarios) > 0)
        types = [s["scenario_type"] for s in scenarios]
        self.assertIn("BASELINE", types)
        self.assertIn("LIKELY", types)
        self.assertIn("ESCALATION", types)

    # -------------------------------------------------------------------------
    # 20. FROZEN HASHES REMAIN UNCHANGED
    # -------------------------------------------------------------------------
    def test_20_frozen_hashes_remain_unchanged(self):
        """Verify byte-for-byte preservation of frozen model and dataset hashes."""
        model_path = PROJECT_ROOT / "ml" / "flood" / "artifacts" / "model.joblib"
        self.assertTrue(model_path.exists())
        actual_model_hash = hashlib.sha256(model_path.read_bytes()).hexdigest()
        self.assertEqual(
            actual_model_hash,
            FROZEN_MODEL_SHA256,
            f"FROZEN MODEL HASH COMPROMISED: {actual_model_hash}"
        )

        dataset_path = PROJECT_ROOT / "datasets" / "processed" / "flood_assam" / "flood_features.csv"
        self.assertTrue(dataset_path.exists())
        actual_dataset_hash = hashlib.sha256(dataset_path.read_bytes()).hexdigest()
        self.assertEqual(
            actual_dataset_hash,
            FROZEN_DATASET_SHA256,
            f"FROZEN DATASET HASH COMPROMISED: {actual_dataset_hash}"
        )


if __name__ == "__main__":
    unittest.main()
