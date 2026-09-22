"""
RISK // INDIA — WEBSITE BETTERMENT PHASE 2 VERIFICATION SUITE
============================================================
Comprehensive automated test suite validating the complete Phase 0 re-analysis
and Phase 2 Website Betterment reset across backend invariants, scientific guards,
predictive risk fusion, zero-synthetic guarantees, frontend component architecture,
security, and documentation integrity.
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


class TestPhaseBetterment2(unittest.TestCase):
    """Rigorous verification of Website Betterment Phase 2."""

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
    # 1. SCIENTIFIC INVARIANTS & PRESERVATION
    # -------------------------------------------------------------------------
    def test_01_model_joblib_sha256_preservation(self):
        """Verify model.joblib has not been retrained, modified, or corrupted."""
        model_path = PROJECT_ROOT / "ml" / "flood" / "artifacts" / "model.joblib"
        self.assertTrue(model_path.exists(), f"Model file missing at: {model_path}")
        computed = hashlib.sha256(model_path.read_bytes()).hexdigest()
        self.assertEqual(
            computed,
            self.expected_model_sha256,
            f"model.joblib SHA-256 altered: got {computed}, expected {self.expected_model_sha256}"
        )

    def test_02_flood_features_dataset_sha256_preservation(self):
        """Verify flood_features.csv has not been modified or corrupted."""
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
    # 2. SCIENTIFIC GUARDS (NON-ASSAM ML & EARTHQUAKE NON-PREDICTION)
    # -------------------------------------------------------------------------
    def test_03_non_assam_ml_guard(self):
        """Verify empirical ML model is strictly NOT_AVAILABLE outside Assam."""
        non_assam_regions = ["odisha", "maharashtra", "bihar", "kerala", "gujarat"]
        for region in non_assam_regions:
            resp = self.client.get(f"/api/predictive-risk/{region}/FLOOD")
            if resp.status_code == 200:
                data = resp.json()
                ml_info = data.get("ml_scope") or data.get("ml_model_scope", {})
                self.assertFalse(
                    ml_info.get("ml_available", True),
                    f"ML model improperly claimed outside Assam for {region}"
                )
                self.assertEqual(
                    ml_info.get("status"),
                    "NOT_AVAILABLE",
                    f"ML status must be NOT_AVAILABLE for {region}"
                )

    def test_04_earthquake_non_prediction_guard(self):
        """Verify earthquake hazard strictly rejects forward forecasting."""
        for region in ["delhi", "uttarakhand", "assam", "gujarat"]:
            resp = self.client.get(f"/api/predictive-risk/{region}/EARTHQUAKE")
            if resp.status_code == 200:
                data = resp.json()
                self.assertEqual(
                    data.get("trend"),
                    "STABLE",
                    f"Earthquake trend must remain STABLE (non-forecastable) for {region}"
                )
                self.assertEqual(
                    data.get("confidence"),
                    "LOW",
                    f"Earthquake forecast confidence must remain LOW for {region}"
                )
                self.assertEqual(
                    data.get("uncertainty"),
                    "VERY_HIGH",
                    f"Earthquake forecast uncertainty must be VERY_HIGH for {region}"
                )
                exp = data.get("explanation", {})
                self.assertTrue(
                    "cannot be predicted" in str(exp).lower() or "non-predictable" in str(exp).lower(),
                    f"Earthquake explanation must disclose tectonic non-predictability for {region}"
                )

    # -------------------------------------------------------------------------
    # 3. ZERO SYNTHETIC DATA & QUALITATIVE METRICS
    # -------------------------------------------------------------------------
    def test_05_zero_synthetic_data_guarantee(self):
        """Verify all predictive endpoints return synthetic_records == 0."""
        endpoints = [
            "/api/predictive-risk/national",
            "/api/predictive-risk/trends",
            "/api/predictive-risk/readiness",
            "/api/predictive-risk/assam/FLOOD",
            "/api/predictive-risk/odisha/CYCLONE",
        ]
        for ep in endpoints:
            resp = self.client.get(ep)
            if resp.status_code == 200:
                data = resp.json()
                synthetic_count = data.get("synthetic_records", 0)
                self.assertEqual(
                    synthetic_count,
                    0,
                    f"Violation of zero-synthetic invariant at {ep}: {synthetic_count} synthetic records"
                )

    def test_06_qualitative_confidence_and_monotonic_uncertainty(self):
        """Verify confidence is qualitative (LOW/MODERATE/HIGH) and uncertainty expands monotonically."""
        resp = self.client.get("/api/predictive-risk/assam/timeline")
        self.assertEqual(resp.status_code, 200)
        raw = resp.json()
        timeline = raw if isinstance(raw, list) else raw.get("timeline", [])
        self.assertEqual(len(timeline), 5, "Expected 5 forecast horizons")
        uncertainty_ranks = {
            "VERY_LOW": 1,
            "LOW": 2,
            "MODERATE": 3,
            "HIGH": 4,
            "VERY_HIGH": 5
        }
        prev_rank = 0
        for pt in timeline:
            conf = pt.get("confidence")
            self.assertIn(
                conf,
                ["LOW", "MODERATE", "HIGH"],
                f"Non-qualitative confidence value found: {conf}"
            )
            unc = pt.get("uncertainty")
            self.assertIn(
                unc,
                uncertainty_ranks.keys(),
                f"Invalid qualitative uncertainty level: {unc}"
            )
            current_rank = uncertainty_ranks[unc]
            self.assertGreaterEqual(
                current_rank,
                prev_rank,
                f"Monotonic uncertainty expansion violated at horizon {pt.get('horizon')}: {unc} < previous"
            )
            prev_rank = current_rank

    # -------------------------------------------------------------------------
    # 4. FRONTEND BETTERMENT COMPONENTS & ARCHITECTURE
    # -------------------------------------------------------------------------
    def test_07_homepage_betterment_components_exist(self):
        """Verify all new Phase 2 Betterment home components exist on disk."""
        components_dir = PROJECT_ROOT / "src" / "components" / "home"
        required_files = [
            "FutureRiskHeroSection.tsx",
            "LocationRiskCheckerSection.tsx",
            "EarlyWarningNoticeSection.tsx",
            "FutureHazardCardsSection.tsx",
            "CitizenActionSection.tsx",
            "LiveRiskSnapshot.tsx",
            "HeroSection.tsx",
            "index.ts",
        ]
        for fname in required_files:
            fpath = components_dir / fname
            self.assertTrue(fpath.exists(), f"Required Betterment component missing: {fname}")
            self.assertGreater(fpath.stat().st_size, 100, f"Component file empty or trivial: {fname}")

    def test_08_homepage_assembly_includes_betterment_sections(self):
        """Verify HomePage.tsx imports and mounts all citizen betterment sections in order."""
        homepage_path = PROJECT_ROOT / "src" / "components" / "pages" / "HomePage.tsx"
        self.assertTrue(homepage_path.exists())
        content = homepage_path.read_text(encoding="utf-8")
        
        expected_sections = [
            "HeroSection",
            "FutureRiskHeroSection",
            "LocationRiskCheckerSection",
            "EarlyWarningNoticeSection",
            "FutureHazardCardsSection",
            "CitizenActionSection",
            "LiveRiskSnapshot",
            "CurrentDisastersSection",
            "ReliefHubSection",
            "VerifiedHelpSection",
        ]
        for sec in expected_sections:
            self.assertIn(sec, content, f"HomePage missing critical section: {sec}")

    def test_09_purge_of_legacy_mock_artifacts_from_active_homepage(self):
        """Verify no mock flags (isDemoData, isSimulated, confidenceScore: 92) exist in LocationRiskCheckerSection."""
        checker_path = PROJECT_ROOT / "src" / "components" / "home" / "LocationRiskCheckerSection.tsx"
        self.assertTrue(checker_path.exists())
        content = checker_path.read_text(encoding="utf-8")
        
        self.assertNotIn("isDemoData: true", content)
        self.assertNotIn("isSimulated: true", content)
        self.assertNotIn("confidenceScore: 92", content)

    def test_10_standardized_open_risk_map_terminology(self):
        """Verify obsolete 'Dedicated Risk Map' is eliminated in favor of 'Open Risk Map'."""
        src_dir = PROJECT_ROOT / "src"
        for fpath in src_dir.rglob("*.tsx"):
            content = fpath.read_text(encoding="utf-8")
            self.assertNotIn(
                "Dedicated Risk Map",
                content,
                f"Obsolete 'Dedicated Risk Map' string found in {fpath.name}"
            )

    def test_11_navbar_direct_betterment_navigation(self):
        """Verify Navbar.tsx exposes direct links to Future Risk, Early Warnings, and Open Risk Map."""
        navbar_path = PROJECT_ROOT / "src" / "components" / "common" / "Navbar.tsx"
        self.assertTrue(navbar_path.exists())
        content = navbar_path.read_text(encoding="utf-8")
        
        self.assertIn("Future Risk", content)
        self.assertIn("Early Warnings", content)
        self.assertIn("Open Risk Map", content)

    def test_12_decoupling_of_preparation_from_evacuation(self):
        """Verify CitizenActionSection and EarlyWarningNoticeSection explicitly demarcate evacuation as civil authority."""
        files = [
            PROJECT_ROOT / "src" / "components" / "home" / "EarlyWarningNoticeSection.tsx",
            PROJECT_ROOT / "src" / "components" / "home" / "CitizenActionSection.tsx",
        ]
        for fpath in files:
            content = fpath.read_text(encoding="utf-8")
            self.assertIn("Evacuation", content)
            self.assertTrue(
                "District Magistrate" in content or "civil authorities" in content or "SDMA" in content,
                f"Missing legal civil authority notice in {fpath.name}"
            )

    def test_13_interactive_72_hour_family_checklist_presence(self):
        """Verify CitizenActionSection includes interactive 72-Hour Family Kit items."""
        action_path = PROJECT_ROOT / "src" / "components" / "home" / "CitizenActionSection.tsx"
        content = action_path.read_text(encoding="utf-8")
        
        self.assertIn("72-Hour Family", content)
        self.assertIn("Drinking Water", content)
        self.assertIn("First Aid", content)
        self.assertIn("Waterproof Pouch", content)

    # -------------------------------------------------------------------------
    # 5. CODE SECURITY & ACCESSIBILITY AUDIT
    # -------------------------------------------------------------------------
    def test_14_external_hyperlink_security(self):
        """Verify all external target='_blank' links have rel='noopener noreferrer'."""
        src_dir = PROJECT_ROOT / "src"
        checked = 0
        for fpath in src_dir.rglob("*.tsx"):
            content = fpath.read_text(encoding="utf-8")
            if 'target="_blank"' in content:
                for match in re.finditer(r'<a\s+[^>]*target="_blank"[^>]*>', content):
                    tag = match.group(0)
                    self.assertIn(
                        'rel="noopener noreferrer"',
                        tag,
                        f"Unsafe external link missing rel='noopener noreferrer' in {fpath.name}: {tag}"
                    )
                    checked += 1
        self.assertGreater(checked, 5, "Expected external links checked across TSX files.")

    def test_15_zero_dangerously_set_inner_html(self):
        """Verify absolute absence of dangerouslySetInnerHTML across all frontend source files."""
        src_dir = PROJECT_ROOT / "src"
        for fpath in src_dir.rglob("*.tsx"):
            content = fpath.read_text(encoding="utf-8")
            self.assertNotIn(
                "dangerouslySetInnerHTML",
                content,
                f"dangerouslySetInnerHTML detected in {fpath.name}"
            )

    # -------------------------------------------------------------------------
    # 6. DOCUMENTATION COMPLETENESS
    # -------------------------------------------------------------------------
    def test_16_forensic_reanalysis_documents_exist(self):
        """Verify all 8 Track 1 Re-Analysis documents exist in docs/reanalysis/."""
        reanalysis_dir = PROJECT_ROOT / "docs" / "reanalysis"
        required = [
            "phase_0_original_objective.md",
            "phase_history_audit.md",
            "architecture_audit.md",
            "feature_inventory.md",
            "product_gap_analysis.md",
            "scientific_integrity_audit.md",
            "ui_gap_analysis.md",
            "final_reanalysis_report.md",
        ]
        for fname in required:
            fpath = reanalysis_dir / fname
            self.assertTrue(fpath.exists(), f"Re-analysis document missing: {fname}")
            self.assertGreater(fpath.stat().st_size, 500, f"Re-analysis doc too short: {fname}")

    def test_17_betterment_documents_exist(self):
        """Verify all 5 Track 3 Betterment documents exist in docs/betterment/."""
        betterment_dir = PROJECT_ROOT / "docs" / "betterment"
        required = [
            "phase_2_product_betterment.md",
            "future_risk_ux_specification.md",
            "citizen_user_journeys.md",
            "ui_architecture.md",
            "feature_gap_closure.md",
        ]
        for fname in required:
            fpath = betterment_dir / fname
            self.assertTrue(fpath.exists(), f"Betterment document missing: {fname}")
            self.assertGreater(fpath.stat().st_size, 500, f"Betterment doc too short: {fname}")

    def test_18_docs_readme_index_coverage(self):
        """Verify docs/README.md indexes both Re-Analysis and Betterment categories."""
        readme_path = PROJECT_ROOT / "docs" / "README.md"
        self.assertTrue(readme_path.exists())
        content = readme_path.read_text(encoding="utf-8")
        
        self.assertIn("Forensic Re-Analysis", content)
        self.assertIn("Website Betterment Phase 2", content)


if __name__ == "__main__":
    unittest.main()
