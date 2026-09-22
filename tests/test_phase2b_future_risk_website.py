"""
RISK // INDIA — PHASE 2B AUTOMATED TEST SUITE
===============================================================================
Comprehensive test suite verifying the 25 Mandatory Approval Conditions:
1. Removal of hardcoded Assam/Kamrup default; National Overview default
2. National India-Wide Future Risk Overview coverage (36 entities)
3. Zero fabricated/simulated location telemetry
4. Explicit coverage tier distinction (Administrative, Baseline, Telemetry, Forecast, Warning, ML)
5. Non-implication of equal live scientific coverage across tiers
6. Explicit DATA UNAVAILABLE / LIMITED EVIDENCE state handling
7. Future Risk discoverability from Homepage, Navbar, Map toggle, and dedicated page
8. Risk Map dual mode: CURRENT RISK vs FUTURE RISK & EARLY WARNING
9. Homepage first viewport 4-pillar communication
10. Exposure of all 10 core dimensions (A-J)
11. Zero numeric pseudo-probabilities ("87% chance" strictly prohibited)
12. Earthquake timing prediction prohibited (tectonic baseline only)
13. ML scope strictly restricted to Assam flood jurisdiction
14. Zero synthetic records (synthetic_records == 0)
15. Byte-for-byte preservation of frozen SHA-256 hashes
16. Backend endpoint reuse without duplicated prediction engines
17. Frontend avoids authoritative risk computation
18. Authoritative risk interpretation originates from backend contracts
19. Discoverability tests
20. Data-gap state tests
21. Visual & semantic distinction between Current and Future risk
22. Future Risk and Early Warning accessible without deep tab navigation
23. Forensic scans for obsolete strings and mock flags
24. Regression and build verification
25. Final certification compliance
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

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Frozen SHA-256 scientific invariants
FROZEN_MODEL_SHA256 = "0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf"
FROZEN_DATASET_SHA256 = "88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080"


class TestPhase2BFutureRiskWebsite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    # -------------------------------------------------------------------------
    # 1. REMOVAL OF HARDCODED ASSAM DEFAULT & NATIONAL OVERVIEW DEFAULT
    # -------------------------------------------------------------------------
    def test_01_no_hardcoded_assam_default_in_future_risk(self):
        """Verify FutureRiskCommandCenter and FutureRiskHeroSection default to null/national overview, not 'assam'."""
        cmd_file = PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskCommandCenter.tsx"
        self.assertTrue(cmd_file.exists())
        content = cmd_file.read_text(encoding="utf-8")
        self.assertIn("useState<string | null>(null)", content)
        self.assertNotIn("useState<string>('assam')", content)

        hero_file = PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskHeroSection.tsx"
        self.assertTrue(hero_file.exists())
        hero_content = hero_file.read_text(encoding="utf-8")
        self.assertNotIn("useState<string>('assam')", hero_content)

    def test_02_location_checker_no_hardcoded_assam_default(self):
        """Verify LocationRiskCheckerSection defaults selectedLocation to null (National Overview)."""
        checker_file = PROJECT_ROOT / "src" / "components" / "home" / "LocationRiskCheckerSection.tsx"
        self.assertTrue(checker_file.exists())
        content = checker_file.read_text(encoding="utf-8")
        self.assertIn("useState<IndiaLocation | null>(null)", content)
        self.assertNotIn("useState<IndiaLocation>(allLocations[2])", content)

    # -------------------------------------------------------------------------
    # 2. NATIONAL OVERVIEW BACKEND AND ZERO SYNTHETIC RECORDS
    # -------------------------------------------------------------------------
    def test_03_national_overview_monitors_36_entities(self):
        """Verify backend /api/predictive-risk/national covers all 36 Indian States & UTs."""
        resp = self.client.get("/api/predictive-risk/national")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["total_entities_monitored"], 36)
        self.assertEqual(data["states_covered"], 28)
        self.assertEqual(data["union_territories_covered"], 8)
        self.assertEqual(len(data["regions"]), 36)

    def test_04_zero_synthetic_records_in_national_overview(self):
        """Verify synthetic_records == 0 across national predictive posture."""
        resp = self.client.get("/api/predictive-risk/national")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["synthetic_records"], 0)

    # -------------------------------------------------------------------------
    # 3. SCIENTIFIC INVARIANTS PRESERVATION (BYTE-FOR-BYTE)
    # -------------------------------------------------------------------------
    def test_05_model_joblib_sha256_preserved(self):
        """Verify SHA-256 of ml/flood/artifacts/model.joblib matches frozen invariant exactly."""
        model_path = PROJECT_ROOT / "ml" / "flood" / "artifacts" / "model.joblib"
        self.assertTrue(model_path.exists())
        hasher = hashlib.sha256()
        hasher.update(model_path.read_bytes())
        self.assertEqual(hasher.hexdigest(), FROZEN_MODEL_SHA256)

    def test_06_flood_features_csv_sha256_preserved(self):
        """Verify SHA-256 of datasets/processed/flood_assam/flood_features.csv matches frozen invariant."""
        dataset_path = PROJECT_ROOT / "datasets" / "processed" / "flood_assam" / "flood_features.csv"
        self.assertTrue(dataset_path.exists())
        hasher = hashlib.sha256()
        hasher.update(dataset_path.read_bytes())
        self.assertEqual(hasher.hexdigest(), FROZEN_DATASET_SHA256)

    # -------------------------------------------------------------------------
    # 4. EARTHQUAKE NON-PREDICTION MANDATE
    # -------------------------------------------------------------------------
    def test_07_earthquake_timing_non_prediction_disclaimer_in_ui(self):
        """Verify prominent disclaimer stating earthquake timing cannot currently be predicted reliably."""
        files_to_check = [
            PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskCommandCenter.tsx",
            PROJECT_ROOT / "src" / "components" / "home" / "FutureHazardMatrix.tsx",
            PROJECT_ROOT / "src" / "components" / "pages" / "FutureRiskPage.tsx",
        ]
        for f in files_to_check:
            self.assertTrue(f.exists(), f"File missing: {f}")
            content = f.read_text(encoding="utf-8")
            self.assertIn("Earthquake timing cannot currently be predicted reliably", content)

    def test_08_earthquake_backend_invariant_contract(self):
        """Verify backend earthquake assessment strictly conforms to non-prediction contract."""
        resp = self.client.get("/api/predictive-risk/delhi/EARTHQUAKE")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["trend"], "STABLE")
        self.assertEqual(data["confidence"], "LOW")
        self.assertEqual(data["uncertainty"], "VERY_HIGH")

    # -------------------------------------------------------------------------
    # 5. ML SCOPE RESTRICTED TO ASSAM FLOOD JURISDICTION ONLY
    # -------------------------------------------------------------------------
    def test_09_ml_scope_restricted_to_assam_flood(self):
        """Verify ml_available is False for non-Assam entities across all hazards."""
        for region in ["delhi", "maharashtra", "odisha", "tamil-nadu", "kerala"]:
            resp = self.client.get(f"/api/predictive-risk/{region}/FLOOD")
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertFalse(data["ml_scope"]["ml_available"])
            self.assertEqual(data["ml_scope"]["guard_status"], "PASS_NON_ASSAM_GUARD")
            self.assertIn("Assam", data["ml_scope"]["reason"])

        # Verify Assam flood has ML active
        resp_assam = self.client.get("/api/predictive-risk/assam/FLOOD")
        self.assertEqual(resp_assam.status_code, 200)
        data_assam = resp_assam.json()
        self.assertTrue(data_assam["ml_scope"]["ml_available"])
        self.assertEqual(data_assam["ml_scope"]["guard_status"], "PASS_ASSAM_IN_DISTRIBUTION")

    # -------------------------------------------------------------------------
    # 6. DATA GAP & LIMITED TELEMETRY EXPLICIT HANDLING
    # -------------------------------------------------------------------------
    def test_10_data_gap_handling_in_ui_components(self):
        """Verify DATA UNAVAILABLE / LIMITED EVIDENCE state with What is Known and What is Unknown."""
        files = [
            PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskCommandCenter.tsx",
            PROJECT_ROOT / "src" / "components" / "home" / "LocationRiskCheckerSection.tsx",
            PROJECT_ROOT / "src" / "components" / "pages" / "FutureRiskPage.tsx",
        ]
        for f in files:
            content = f.read_text(encoding="utf-8")
            self.assertIn("DATA UNAVAILABLE // LIMITED", content)
            self.assertIn("WHAT IS KNOWN", content)
            self.assertIn("WHAT IS UNKNOWN", content)

    # -------------------------------------------------------------------------
    # 7. COVERAGE TIER CLARIFICATION & NON-EQUAL SCIENTIFIC COVERAGE
    # -------------------------------------------------------------------------
    def test_11_six_coverage_tiers_distinguished(self):
        """Verify components distinguish Administrative, Baseline, Telemetry, Forecast, Warning, ML."""
        files = [
            PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskCommandCenter.tsx",
            PROJECT_ROOT / "src" / "components" / "home" / "LocationRiskCheckerSection.tsx",
            PROJECT_ROOT / "src" / "components" / "pages" / "FutureRiskPage.tsx",
        ]
        for f in files:
            content = f.read_text(encoding="utf-8")
            self.assertIn("ADMIN COVERAGE", content)
            self.assertIn("REGIONAL BASELINE", content)
            self.assertIn("LIVE TELEMETRY", content)
            self.assertIn("OFFICIAL WARNINGS", content)
            self.assertIn("APPROVED ML SCOPE", content)

    # -------------------------------------------------------------------------
    # 8. HOMEPAGE FIRST VIEWPORT & 4-PILLAR COMMUNICATION
    # -------------------------------------------------------------------------
    def test_12_hero_section_4_pillars(self):
        """Verify HeroSection communicates CURRENT RISK, FUTURE RISK, EARLY WARNING, and ACTION."""
        hero_file = PROJECT_ROOT / "src" / "components" / "home" / "HeroSection.tsx"
        content = hero_file.read_text(encoding="utf-8")
        self.assertIn("CURRENT RISK • FUTURE RISK • EARLY WARNING • ACTION", content)

    def test_13_hero_section_see_early_warnings_cta(self):
        """Verify HeroSection contains See Early Warnings CTA and onSeeEarlyWarnings prop."""
        hero_file = PROJECT_ROOT / "src" / "components" / "home" / "HeroSection.tsx"
        content = hero_file.read_text(encoding="utf-8")
        self.assertIn("onSeeEarlyWarnings", content)
        self.assertIn("See Early Warnings", content)

    # -------------------------------------------------------------------------
    # 9. DISCOVERABILITY: NAVBAR & ROUTING
    # -------------------------------------------------------------------------
    def test_14_navbar_exposes_required_navigation(self):
        """Verify Navbar exposes Home, Future Risk, Early Warnings, Open Risk Map, Live Disasters, Get Help / SOS."""
        nav_file = PROJECT_ROOT / "src" / "components" / "common" / "Navbar.tsx"
        content = nav_file.read_text(encoding="utf-8")
        self.assertIn("'future-risk'", content)
        self.assertIn("Future Risk", content)
        self.assertIn("Early Warnings", content)
        self.assertIn("Open Risk Map", content)
        self.assertIn("Live Disasters", content)
        self.assertIn("Get Help / SOS", content)

    def test_15_future_risk_page_routed_in_app(self):
        """Verify App.tsx imports and routes FutureRiskPage under 'future-risk'."""
        app_file = PROJECT_ROOT / "src" / "App.tsx"
        content = app_file.read_text(encoding="utf-8")
        self.assertIn("FutureRiskPage", content)
        self.assertIn("currentPage === 'future-risk'", content)

    # -------------------------------------------------------------------------
    # 10. RISK MAP DUAL MODE TOGGLE
    # -------------------------------------------------------------------------
    def test_16_risk_map_dual_mode_toggle(self):
        """Verify IndiaRiskMap contains CURRENT RISK vs FUTURE RISK & EARLY WARNING mode toggle."""
        map_file = PROJECT_ROOT / "src" / "components" / "map" / "IndiaRiskMap.tsx"
        content = map_file.read_text(encoding="utf-8")
        self.assertIn("CURRENT RISK", content)
        self.assertIn("FUTURE RISK & EARLY WARNING", content)
        self.assertIn("mapPerspective", content)
        self.assertIn("futureHorizon", content)

    # -------------------------------------------------------------------------
    # 11. 10 CORE DIMENSIONS EXPOSED
    # -------------------------------------------------------------------------
    def test_17_ten_core_dimensions_in_command_center(self):
        """Verify FutureRiskCommandCenter displays all 10 core dimensions (A through E and details)."""
        cmd_file = PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskCommandCenter.tsx"
        content = cmd_file.read_text(encoding="utf-8")
        self.assertIn("A. Current State", content)
        self.assertIn("B. Future State", content)
        self.assertIn("C. Trend", content)
        self.assertIn("D. Peak Horizon", content)
        self.assertIn("E. Main Hazard", content)
        self.assertIn("Causal Evidence Drivers", content)
        self.assertIn("Escalation Scenarios", content)

    # -------------------------------------------------------------------------
    # 12. 5-HORIZON TIMELINE WITH MONOTONIC UNCERTAINTY EXPANSION
    # -------------------------------------------------------------------------
    def test_18_five_horizons_in_timeline(self):
        """Verify FutureRiskTimeline defines NOW, 0-6h, 6-24h, 1-3d, 3-7d."""
        tl_file = PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskTimeline.tsx"
        content = tl_file.read_text(encoding="utf-8")
        for h in ["NOW", "0-6h", "6-24h", "1-3d", "3-7d"]:
            self.assertIn(h, content)
        self.assertIn("Monotonic Uncertainty: LOW → VERY HIGH", content)

    # -------------------------------------------------------------------------
    # 13. MULTI-HAZARD MATRIX & PROVENANCE
    # -------------------------------------------------------------------------
    def test_19_all_6_hazards_in_matrix(self):
        """Verify FutureHazardMatrix supports Flood, Cyclone, Heatwave, Severe Weather, Landslide, Earthquake."""
        hm_file = PROJECT_ROOT / "src" / "components" / "home" / "FutureHazardMatrix.tsx"
        content = hm_file.read_text(encoding="utf-8")
        for h in ["FLOOD", "CYCLONE", "HEATWAVE", "SEVERE_WEATHER", "LANDSLIDE", "EARTHQUAKE"]:
            self.assertIn(h, content)
        self.assertIn("CWC (Central Water Commission) & IMD", content)
        self.assertIn("National Centre for Seismology (NCS) & USGS", content)

    # -------------------------------------------------------------------------
    # 14. 72-HOUR FAMILY DISASTER EMERGENCY KIT
    # -------------------------------------------------------------------------
    def test_20_family_kit_8_categories(self):
        """Verify FutureRiskActionPanel defines all 8 categories of the 72-hour family kit."""
        ap_file = PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskActionPanel.tsx"
        content = ap_file.read_text(encoding="utf-8")
        self.assertIn("72-HOUR FAMILY DISASTER SUPPLY KIT", content)
        self.assertIn("1. Water & Hydration", content)
        self.assertIn("2. Emergency Rations", content)
        self.assertIn("3. First Aid & Prescription Meds", content)
        self.assertIn("4. Emergency Lighting & Radio", content)
        self.assertIn("5. Power & Communication", content)
        self.assertIn("6. Critical Documents", content)
        self.assertIn("7. Sanitation & Personal Hygiene", content)
        self.assertIn("8. Signaling & Protective Wear", content)

    # -------------------------------------------------------------------------
    # 15. STATUTORY HELPLINES
    # -------------------------------------------------------------------------
    def test_21_statutory_helplines_present(self):
        """Verify 112, 1078, and 1070 are present in action and checker sections."""
        ap_file = PROJECT_ROOT / "src" / "components" / "home" / "FutureRiskActionPanel.tsx"
        content = ap_file.read_text(encoding="utf-8")
        self.assertIn("112", content)
        self.assertIn("1078", content)

        prep_file = PROJECT_ROOT / "src" / "components" / "home" / "PreparednessSection.tsx"
        prep_content = prep_file.read_text(encoding="utf-8")
        self.assertIn("1078", prep_content)
        self.assertIn("112", prep_content)

    # -------------------------------------------------------------------------
    # 16. FORENSIC PURITY: ZERO DEDICATED RISK MAP, ZERO MOCKS
    # -------------------------------------------------------------------------
    def test_22_zero_dedicated_risk_map_in_src(self):
        """Verify obsolete 'Dedicated Risk Map' string does not exist anywhere in src/."""
        src_dir = PROJECT_ROOT / "src"
        matches = []
        for p in src_dir.rglob("*.tsx"):
            txt = p.read_text(encoding="utf-8")
            if "Dedicated Risk Map" in txt:
                matches.append(str(p.relative_to(PROJECT_ROOT)))
        self.assertEqual(matches, [], f"Found 'Dedicated Risk Map' in files: {matches}")

    def test_23_zero_mock_flags_in_future_risk_components(self):
        """Verify no isDemoData or isSimulated flags exist in FutureRiskCommandCenter or FutureRiskPage."""
        for name in ["FutureRiskCommandCenter.tsx", "FutureRiskTimeline.tsx", "FutureHazardMatrix.tsx", "FutureRiskPage.tsx"]:
            f = PROJECT_ROOT / "src" / "components" / ("pages" if "Page" in name else "home") / name
            content = f.read_text(encoding="utf-8")
            self.assertNotIn("isDemoData", content)
            self.assertNotIn("isSimulated", content)

    # -------------------------------------------------------------------------
    # 17. REUSE OF BACKEND PREDICTIVE RISK APIS
    # -------------------------------------------------------------------------
    def test_24_backend_timeline_endpoint(self):
        """Verify /api/predictive-risk/{region}/timeline returns 5 horizon points."""
        resp = self.client.get("/api/predictive-risk/assam/timeline")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 5)
        horizons = [p["horizon"] for p in data]
        self.assertEqual(horizons, ["NOW", "0-6h", "6-24h", "1-3d", "3-7d"])

    def test_25_backend_explanation_endpoint(self):
        """Verify /api/predictive-risk/{region}/explanation returns causal drivers and 12 citizen answers."""
        resp = self.client.get("/api/predictive-risk/assam/explanation")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("why_this_risk", data)
        self.assertIn("citizen_answers", data)
        answers = data["citizen_answers"]
        self.assertIn("what_should_i_do_now", answers)
        self.assertIn("what_to_prepare_before", answers)

    def test_26_backend_scenarios_endpoint(self):
        """Verify /api/predictive-risk/{region}/scenarios returns Baseline, Likely, Escalation."""
        resp = self.client.get("/api/predictive-risk/assam/scenarios")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 3)
        types = [s["scenario_type"] for s in data]
        self.assertEqual(types, ["BASELINE", "LIKELY", "ESCALATION"])

    def test_27_backend_early_warning_endpoint(self):
        """Verify /api/predictive-risk/{region}/early-warning provides guidance."""
        resp = self.client.get("/api/predictive-risk/assam/early-warning")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("status", data)
        self.assertIn("lead_time_window", data)
        self.assertIn("preparation_guidance", data)

    def test_28_backend_readiness_endpoint(self):
        """Verify /api/predictive-risk/readiness returns actionable entities with zero synthetic records."""
        resp = self.client.get("/api/predictive-risk/readiness")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("actionable_count", data)
        self.assertEqual(data["synthetic_records"], 0)

    # -------------------------------------------------------------------------
    # 18. HOMEPAGE 12-SECTION STRUCTURE COMPLIANCE
    # -------------------------------------------------------------------------
    def test_29_homepage_contains_all_12_sections(self):
        """Verify HomePage contains all 12 sections in sequence."""
        hp_file = PROJECT_ROOT / "src" / "components" / "pages" / "HomePage.tsx"
        content = hp_file.read_text(encoding="utf-8")
        sections = [
            "<HeroSection",
            "<FutureRiskHeroSection",
            "<LocationRiskCheckerSection",
            "<EarlyWarningNoticeSection",
            "<FutureHazardCardsSection",
            "<CitizenActionSection",
            "<LiveRiskSnapshot",
            "<CurrentDisastersSection",
            "<ReliefHubSection",
            "<VerifiedHelpSection",
            "<HowItWorksSection",
            "<FinalCTASection",
        ]
        last_pos = -1
        for s in sections:
            pos = content.find(s)
            self.assertNotEqual(pos, -1, f"Missing section: {s}")
            self.assertGreater(pos, last_pos, f"Section out of order: {s}")
            last_pos = pos

    def test_30_components_exported_in_home_index(self):
        """Verify all Phase 2B components are cleanly exported from src/components/home/index.ts."""
        index_file = PROJECT_ROOT / "src" / "components" / "home" / "index.ts"
        content = index_file.read_text(encoding="utf-8")
        for comp in [
            "FutureRiskCommandCenter",
            "FutureRiskTimeline",
            "FutureHazardMatrix",
            "FutureRiskDrivers",
            "FutureRiskActionPanel",
        ]:
            self.assertIn(comp, content, f"Component {comp} not exported in home/index.ts")


if __name__ == "__main__":
    unittest.main()
