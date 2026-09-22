"""
RISK // INDIA — PHASE 2A CITIZEN-FIRST WEBSITE EXPERIENCE HARDENING TEST SUITE
=============================================================================
Authoritative automated verification for Phase 2A:
1. Model & Dataset SHA-256 scientific preservation
2. Zero synthetic records guarantee across all predictive & crisis endpoints
3. Scientific scope restrictions (ML confined to Assam, zero ML outside Assam)
4. Earthquake non-prediction scientific invariant
5. Preparation vs Civil Evacuation demarcation under DM Act 2005
6. Complete legacy mock purge (0 isDemoData: true, 0 isSimulated: true, no AnalyzeAreaSection)
7. Terminology standardization (0 Dedicated Risk Map, 100% Open Risk Map)
8. Hero Section first-viewport 6-question intelligence & Check Future Risk CTA
9. Location Risk Checker 4-tier cascade & 11-point citizen intelligence matrix
10. How It Works 6 plain-language explainability questions
11. Crisis Recommended Banner warning headline & action CTA
12. FreshnessBadge 9-state degradation & provenance support
"""

import unittest
import hashlib
import re
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


class TestPhase2ACitizenWebsiteHardening(unittest.TestCase):
    """Rigorous verification of Phase 2A Citizen-First Website Experience Hardening."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.expected_model_sha256 = (
            "0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf"
        )
        cls.expected_dataset_sha256 = (
            "88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080"
        )

    # -------------------------------------------------------------------------
    # 1. SCIENTIFIC & DATA INVARIANTS PRESERVATION
    # -------------------------------------------------------------------------
    def test_01_model_joblib_sha256_preservation(self):
        """Verify model.joblib has not been retrained, modified, or altered."""
        model_path = PROJECT_ROOT / "ml" / "flood" / "artifacts" / "model.joblib"
        self.assertTrue(model_path.exists(), f"Model file missing at: {model_path}")
        computed = hashlib.sha256(model_path.read_bytes()).hexdigest()
        self.assertEqual(
            computed,
            self.expected_model_sha256,
            f"model.joblib SHA-256 altered: got {computed}, expected {self.expected_model_sha256}"
        )

    def test_02_flood_features_dataset_sha256_preservation(self):
        """Verify flood_features.csv has not been altered or modified."""
        dataset_path = (
            PROJECT_ROOT / "datasets" / "processed" / "flood_assam" / "flood_features.csv"
        )
        self.assertTrue(dataset_path.exists(), f"Dataset missing at: {dataset_path}")
        computed = hashlib.sha256(dataset_path.read_bytes()).hexdigest()
        self.assertEqual(
            computed,
            self.expected_dataset_sha256,
            f"flood_features.csv SHA-256 altered: got {computed}, expected {self.expected_dataset_sha256}"
        )

    # -------------------------------------------------------------------------
    # 2. ZERO-SYNTHETIC DATA GUARANTEE ACROSS PREDICTIVE ENDPOINTS
    # -------------------------------------------------------------------------
    def test_03_zero_synthetic_data_guarantee(self):
        """Verify synthetic_records == 0 across all predictive risk endpoints."""
        endpoints = [
            "/api/predictive-risk/national",
            "/api/predictive-risk/assam/FLOOD",
            "/api/predictive-risk/bihar/FLOOD",
            "/api/predictive-risk/kerala/LANDSLIDE",
            "/api/predictive-risk/odisha/CYCLONE",
            "/api/predictive-risk/readiness",
            "/api/crisis/status",
        ]
        for ep in endpoints:
            resp = self.client.get(ep)
            self.assertEqual(resp.status_code, 200, f"Endpoint failed: {ep}")
            data = resp.json()
            if "synthetic_records" in data:
                self.assertEqual(
                    data["synthetic_records"],
                    0,
                    f"Synthetic data detected in {ep}: {data['synthetic_records']}"
                )

    # -------------------------------------------------------------------------
    # 3. SCIENTIFIC SCOPE & EARTHQUAKE NON-PREDICTION SAFEGUARDS
    # -------------------------------------------------------------------------
    def test_04_ml_scope_restriction_outside_assam(self):
        """Verify ML is active ONLY for Assam and strictly disabled for other 35 entities."""
        # Assam Flood -> ML active
        resp_assam = self.client.get("/api/predictive-risk/assam/FLOOD")
        self.assertEqual(resp_assam.status_code, 200)
        data_assam = resp_assam.json()
        ml_scope_assam = data_assam.get("ml_scope", {})
        self.assertTrue(ml_scope_assam.get("ml_available", False))
        self.assertEqual(ml_scope_assam.get("guard_status"), "PASS_ASSAM_IN_DISTRIBUTION")

        # Non-Assam regions -> ML disabled
        non_assam_regions = ["bihar", "kerala", "odisha", "delhi", "gujarat"]
        for r in non_assam_regions:
            resp = self.client.get(f"/api/predictive-risk/{r}/FLOOD")
            self.assertEqual(resp.status_code, 200)
            d = resp.json()
            ml_scope_r = d.get("ml_scope", {})
            self.assertFalse(ml_scope_r.get("ml_available", True), f"ML incorrectly enabled for non-Assam region: {r}")
            self.assertEqual(ml_scope_r.get("guard_status"), "PASS_NON_ASSAM_GUARD")

    def test_05_earthquake_scientific_guard(self):
        """Verify earthquakes are never predicted; trend is stable and uncertainty is very high."""
        resp = self.client.get("/api/predictive-risk/assam/EARTHQUAKE")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["trend"], "STABLE")
        self.assertEqual(data["confidence"], "LOW")
        self.assertEqual(data["uncertainty"], "VERY_HIGH")
        # Citizen explanation must clearly disclaim prediction capability
        exp_str = str(data.get("explanation", {})).lower()
        self.assertTrue(
            "cannot be predicted" in exp_str or "not predictable" in exp_str or "non-predictable" in exp_str or "cannot be forecasted" in exp_str,
            f"Missing earthquake non-prediction disclaimer in explanation: {exp_str}"
        )

    # -------------------------------------------------------------------------
    # 4. PREPARATION VS CIVIL EVACUATION DEMARCATION (DM ACT 2005)
    # -------------------------------------------------------------------------
    def test_06_evacuation_statutory_demarcation(self):
        """Verify early warning readiness strictly decouples preparation from statutory evacuation."""
        resp = self.client.get("/api/predictive-risk/readiness")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("entities", data)
        for ent in data["entities"]:
            self.assertIn("early_warning_status", ent)
            self.assertIn("is_evacuation_advised", ent)
            self.assertIn("preparation_guidance", ent)
            self.assertIsInstance(ent["preparation_guidance"], list)

    # -------------------------------------------------------------------------
    # 5. FRONTEND LEGACY MOCK PURGE AUDIT
    # -------------------------------------------------------------------------
    def test_07_no_legacy_analyze_area_component(self):
        """Verify AnalyzeAreaSection.tsx is completely purged from the repository."""
        legacy_file = PROJECT_ROOT / "src" / "components" / "home" / "AnalyzeAreaSection.tsx"
        self.assertFalse(legacy_file.exists(), "Obsolete AnalyzeAreaSection.tsx still exists!")

    def test_08_zero_is_demo_data_in_frontend(self):
        """Verify zero occurrences of 'isDemoData: true' in src/ codebase."""
        src_dir = PROJECT_ROOT / "src"
        matches = []
        for file in src_dir.rglob("*.ts*"):
            content = file.read_text(encoding="utf-8", errors="ignore")
            if "isDemoData: true" in content:
                matches.append(str(file.relative_to(PROJECT_ROOT)))
        self.assertEqual(matches, [], f"Found 'isDemoData: true' in files: {matches}")

    def test_09_zero_is_simulated_in_frontend(self):
        """Verify zero occurrences of 'isSimulated: true' in src/ codebase."""
        src_dir = PROJECT_ROOT / "src"
        matches = []
        for file in src_dir.rglob("*.ts*"):
            content = file.read_text(encoding="utf-8", errors="ignore")
            if "isSimulated: true" in content:
                matches.append(str(file.relative_to(PROJECT_ROOT)))
        self.assertEqual(matches, [], f"Found 'isSimulated: true' in files: {matches}")

    def test_10_terminology_open_risk_map(self):
        """Verify zero occurrences of 'Dedicated Risk Map' and correct use of 'Open Risk Map'."""
        src_dir = PROJECT_ROOT / "src"
        matches = []
        for file in src_dir.rglob("*.ts*"):
            content = file.read_text(encoding="utf-8", errors="ignore")
            if "Dedicated Risk Map" in content:
                matches.append(str(file.relative_to(PROJECT_ROOT)))
        self.assertEqual(matches, [], f"Found 'Dedicated Risk Map' in files: {matches}")

        navbar_file = PROJECT_ROOT / "src" / "components" / "common" / "Navbar.tsx"
        self.assertIn("Open Risk Map", navbar_file.read_text(encoding="utf-8"))

    # -------------------------------------------------------------------------
    # 6. HERO SECTION CITIZEN EXPERIENCE HARDENING
    # -------------------------------------------------------------------------
    def test_11_hero_section_future_risk_cta_and_6_questions(self):
        """Verify HeroSection contains 'Check Future Risk' CTA and first-viewport 6 questions."""
        hero_file = PROJECT_ROOT / "src" / "components" / "home" / "HeroSection.tsx"
        self.assertTrue(hero_file.exists())
        content = hero_file.read_text(encoding="utf-8")

        # CTA buttons
        self.assertIn("Open Risk Map", content)
        self.assertIn("Check Future Risk", content)
        self.assertIn("Check Risk for My Location", content)

        # First-viewport 6 questions
        self.assertIn("1. Happening Now", content)
        self.assertIn("2. Happening Next", content)
        self.assertIn("3. Risk Trend", content)
        self.assertIn("4. Timing", content)
        self.assertIn("5. What To Do", content)
        self.assertIn("6. Verified Help", content)

    # -------------------------------------------------------------------------
    # 7. LOCATION RISK CHECKER 4-TIER CASCADE & 11 REQUIRED FIELDS
    # -------------------------------------------------------------------------
    def test_12_location_checker_section_ids(self):
        """Verify LocationRiskCheckerSection provides location-checker, analyze-section, check-location."""
        checker_file = PROJECT_ROOT / "src" / "components" / "home" / "LocationRiskCheckerSection.tsx"
        self.assertTrue(checker_file.exists())
        content = checker_file.read_text(encoding="utf-8")

        self.assertIn('id="location-checker"', content)
        self.assertIn('id="analyze-section"', content)
        self.assertIn('id="check-location"', content)

    def test_13_location_checker_4_tier_cascade(self):
        """Verify 4-tier geospatial cascade: India -> State/UT -> District -> Locality."""
        checker_file = PROJECT_ROOT / "src" / "components" / "home" / "LocationRiskCheckerSection.tsx"
        content = checker_file.read_text(encoding="utf-8")

        self.assertIn("4-TIER GEOSPATIAL CASCADE", content)
        self.assertIn("1. Country (Tier 1)", content)
        self.assertIn("India (National)", content)
        self.assertIn("2. State / UT (Tier 2)", content)
        self.assertIn("3. District (Tier 3)", content)
        self.assertIn("4. City / Locality (Tier 4)", content)

    def test_14_location_checker_11_required_fields(self):
        """Verify all 11 required citizen intelligence fields are explicitly rendered."""
        checker_file = PROJECT_ROOT / "src" / "components" / "home" / "LocationRiskCheckerSection.tsx"
        content = checker_file.read_text(encoding="utf-8")

        required_fields = [
            "1. CURRENT RISK",
            "2. FUTURE RISK",
            "3. MAIN HAZARD",
            "4. RISK TREND",
            "5. TIME HORIZON",
            "6. CONFIDENCE",
            "7. UNCERTAINTY",
            "8. WHY?",
            "9. WHAT TO DO?",
            "10. OFFICIAL WARNING",
            "11. VERIFIED HELP"
        ]
        for field in required_fields:
            self.assertIn(field, content, f"Required field missing in LocationRiskCheckerSection: {field}")

    # -------------------------------------------------------------------------
    # 8. HOW IT WORKS 6 PLAIN-LANGUAGE EXPLANATION QUESTIONS
    # -------------------------------------------------------------------------
    def test_15_how_it_works_6_plain_language_questions(self):
        """Verify HowItWorksSection answers the 6 plain-language questions."""
        how_file = PROJECT_ROOT / "src" / "components" / "home" / "HowItWorksSection.tsx"
        self.assertTrue(how_file.exists())
        content = how_file.read_text(encoding="utf-8")

        questions = [
            "1. Why is this risk showing?",
            "2. What changed?",
            "3. What evidence supports it?",
            "4. What could make it worse?",
            "5. What do we not know?",
            "6. When should I check again?"
        ]
        for q in questions:
            self.assertIn(q, content, f"Missing plain-language question in HowItWorksSection: {q}")

    # -------------------------------------------------------------------------
    # 9. CRISIS RECOMMENDED BANNER CITIZEN ACTIONS
    # -------------------------------------------------------------------------
    def test_16_crisis_recommended_banner_headline_and_cta(self):
        """Verify CrisisRecommendedBanner displays warning headline and actionable CTA."""
        banner_file = PROJECT_ROOT / "src" / "components" / "crisis" / "CrisisRecommendedBanner.tsx"
        self.assertTrue(banner_file.exists())
        content = banner_file.read_text(encoding="utf-8")

        self.assertIn("⚠️ CONDITIONS MAY BE DANGEROUS", content)
        self.assertIn("See What You Should Do Now", content)

    # -------------------------------------------------------------------------
    # 10. FRESHNESS BADGE 9-STATE PROVENANCE
    # -------------------------------------------------------------------------
    def test_17_freshness_badge_all_9_states(self):
        """Verify FreshnessBadge explicitly supports all 9 provenance & degradation states."""
        badge_file = PROJECT_ROOT / "src" / "components" / "common" / "FreshnessBadge.tsx"
        self.assertTrue(badge_file.exists())
        content = badge_file.read_text(encoding="utf-8")

        states = [
            "LIVE",
            "RECENT",
            "FORECAST",
            "CACHED",
            "STALE",
            "BASELINE",
            "EMPIRICAL_ML",
            "DATA_UNAVAILABLE",
            "PROVIDER_DEGRADED"
        ]
        for s in states:
            self.assertIn(s, content, f"FreshnessBadge missing support for state: {s}")

    # -------------------------------------------------------------------------
    # 11. HOMEPAGE 12-SECTION HIERARCHY
    # -------------------------------------------------------------------------
    def test_18_homepage_12_section_order(self):
        """Verify HomePage maintains the exact 12-section hierarchy."""
        hp_file = PROJECT_ROOT / "src" / "components" / "pages" / "HomePage.tsx"
        self.assertTrue(hp_file.exists())
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
            "<FinalCTASection"
        ]
        last_pos = -1
        for s in sections:
            pos = content.find(s)
            self.assertNotEqual(pos, -1, f"Section missing in HomePage: {s}")
            self.assertGreater(pos, last_pos, f"Section out of order: {s}")
            last_pos = pos

    # -------------------------------------------------------------------------
    # 12. STATUTORY PROTOCOL DEMARCATION
    # -------------------------------------------------------------------------
    def test_19_statutory_protocol_demarcation_notice(self):
        """Verify explicit Disaster Management Act 2005 notices in UI components."""
        ew_file = PROJECT_ROOT / "src" / "components" / "home" / "EarlyWarningNoticeSection.tsx"
        content = ew_file.read_text(encoding="utf-8")
        self.assertIn("Disaster Management Act, 2005", content)
        self.assertIn("District Magistrates", content)

    # -------------------------------------------------------------------------
    # 13. PAN-INDIA COVERAGE (36/36 ENTITIES)
    # -------------------------------------------------------------------------
    def test_20_national_36_entities_coverage(self):
        """Verify national overview returns exactly 36 entities with non-synthetic data."""
        resp = self.client.get("/api/predictive-risk/national")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["total_entities_monitored"], 36)
        self.assertEqual(data["states_covered"], 28)
        self.assertEqual(data["union_territories_covered"], 8)
        self.assertEqual(len(data["regions"]), 36)
        self.assertEqual(data["synthetic_records"], 0)


if __name__ == "__main__":
    unittest.main()
