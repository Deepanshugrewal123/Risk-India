"""
RISK // INDIA — Phase 21 Verification Suite
===========================================
Validates Public UX Hardening, Emergency Accessibility & Crisis Resilience:
1. Emergency Helplines (112, 1078, 1070, 108, 101, 100, 1077, 1098, 1091) and direct tel: protocol.
2. Offline Emergency Access Hub with step-by-step life safety guides for all 6 hazards.
3. Crisis Mode context management, localStorage persistence, URL query synchronization (?crisis=true), and animation suppression.
4. ParticleFieldCanvas and TiltCard performance bypass during crisis mode.
5. Freshness honesty in disasterService: cached snapshot data is NEVER marked as LIVE.
6. Three-tier Map Degradation in IndiaRiskMap (Interactive Map -> State Cards Grid -> Accessible Tabular List).
7. Plain-language citizen interpretations (Antecedent rainfall, River stage/HFL, Probability, Focal depth).
8. Scientific honesty and ML scope demarcation (Assam prototype vs non-Assam regional baseline).
9. Help Hub explicit verification tags (OFFICIAL GOVERNMENT, VERIFIED NGO / AGENCY, COMMUNITY AID) and direct tap-to-call.
10. Deep-linking query parameter routing (?page, ?view, ?crisis, ?emergency, ?incident).
11. Frozen Assam flood prototype preservation (13 features, 32 historical events, zero synthetic data).
"""

import os
import sys
import re
import json
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.dataset_manifest import dataset_manifest_registry
from app.services.model_registry import model_registry, ModelStatus


class TestPhase21PublicUXAndCrisisResilience(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_root = str(PROJECT_ROOT)
        cls.src_dir = os.path.join(cls.project_root, "src")
        cls.backend_dir = os.path.join(cls.project_root, "backend")

    # -------------------------------------------------------------------------
    # 1. Emergency Helplines & Direct Calling Tests
    # -------------------------------------------------------------------------
    def test_emergency_access_hub_exists_and_contains_all_core_helplines(self):
        hub_path = os.path.join(self.src_dir, "components", "emergency", "EmergencyAccessHub.tsx")
        self.assertTrue(os.path.exists(hub_path), "EmergencyAccessHub.tsx must exist.")

        with open(hub_path, "r", encoding="utf-8") as f:
            content = f.read()

        core_numbers = ["112", "1078", "1070", "108", "101", "100"]
        for num in core_numbers:
            self.assertIn(f"'{num}'", content, f"Helpline number {num} must be registered in EmergencyAccessHub.")
            self.assertIn(f"tel:${{", content, "Must use tel: protocol for direct mobile calling.")

        # Check additional critical citizen services
        self.assertIn("1077", content, "District EOC 1077 must be present.")
        self.assertIn("1098", content, "Childline 1098 must be present.")
        self.assertIn("1091", content, "Women Helpline 1091 must be present.")

    def test_emergency_hub_one_click_copy_and_dial_attributes(self):
        hub_path = os.path.join(self.src_dir, "components", "emergency", "EmergencyAccessHub.tsx")
        with open(hub_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("navigator.clipboard.writeText", content, "Must provide one-click clipboard copy for desktop.")
        self.assertIn("Copied", content, "Must provide copied confirmation feedback.")
        self.assertIn("tel:", content, "Must provide direct tel: anchor links.")

    # -------------------------------------------------------------------------
    # 2. Offline Static Safety Protocols for All Hazards
    # -------------------------------------------------------------------------
    def test_emergency_hub_offline_safety_protocols(self):
        hub_path = os.path.join(self.src_dir, "components", "emergency", "EmergencyAccessHub.tsx")
        with open(hub_path, "r", encoding="utf-8") as f:
            content = f.read()

        required_hazards = ["Flood", "Earthquake", "Cyclone", "Heatwave", "Landslide", "Severe Weather"]
        for hazard in required_hazards:
            self.assertIn(hazard, content, f"Offline safety protocol must cover {hazard}.")

        # Check life preservation instructions
        self.assertIn("Do not walk or drive through moving water", content)
        self.assertIn("DROP to your hands and knees", content)
        self.assertIn("Stay securely indoors in the strongest", content)
        self.assertIn("Drink water frequently (ORS", content)
        self.assertIn("trees cracking", content)
        self.assertIn("metal vehicle immediately upon hearing thunder", content)

    # -------------------------------------------------------------------------
    # 3. Crisis Mode State & Context Management
    # -------------------------------------------------------------------------
    def test_crisis_context_implementation(self):
        context_path = os.path.join(self.src_dir, "context", "CrisisContext.tsx")
        self.assertTrue(os.path.exists(context_path), "CrisisContext.tsx must exist.")

        with open(context_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("risk_india_crisis_mode", content, "Must persist crisis mode in localStorage.")
        self.assertIn("params.get('crisis')", content, "Must detect crisis mode from URL query parameters (?crisis=true).")
        self.assertIn("classList.add('crisis-mode')", content, "Must add .crisis-mode class to document root.")
        self.assertIn("classList.remove('crisis-mode')", content, "Must remove .crisis-mode class when deactivated.")
        self.assertIn("export const CrisisProvider", content, "Must export CrisisProvider.")
        self.assertIn("export const useCrisis", content, "Must export useCrisis hook.")

    def test_particle_canvas_suppression_in_crisis_mode(self):
        canvas_path = os.path.join(self.src_dir, "components", "common", "ParticleFieldCanvas.tsx")
        with open(canvas_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("useCrisis", content, "ParticleFieldCanvas must hook into CrisisContext.")
        self.assertIn("if (isCrisisMode) return", content, "Must abort animation loop if isCrisisMode is active.")
        self.assertIn("if (isCrisisMode)", content, "Must check crisis mode before rendering canvas.")

    def test_tilt_card_bypass_in_crisis_mode(self):
        tilt_path = os.path.join(self.src_dir, "components", "common", "TiltCard.tsx")
        with open(tilt_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("useCrisis", content, "TiltCard must hook into CrisisContext.")
        self.assertIn("if (isCrisisMode)", content, "TiltCard must bypass motion calculations in crisis mode.")

    # -------------------------------------------------------------------------
    # 4. Freshness Honesty & Cache Transparency
    # -------------------------------------------------------------------------
    def test_disaster_service_cache_honesty(self):
        service_path = os.path.join(self.src_dir, "services", "disasterService.ts")
        with open(service_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("risk_india_disasters_cache", content, "Must have offline cache key in localStorage.")
        self.assertIn("freshness: 'CACHED'", content, "Cached snapshots must be explicitly marked as CACHED.")
        self.assertIn("is_cached: true", content, "Must set is_cached flag.")

    def test_disaster_page_freshness_and_four_pillars_badges(self):
        page_path = os.path.join(self.src_dir, "components", "pages", "DisastersPage.tsx")
        with open(page_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Four Pillars badges
        self.assertIn("LIVE OFFICIAL DATA", content)
        self.assertIn("ML PROTOTYPE ESTIMATE", content)
        self.assertIn("OFFICIAL BULLETIN", content)
        self.assertIn("REGIONAL BASELINE", content)

        # Freshness honesty
        self.assertIn("CACHED", content)
        self.assertIn("LIVE", content)
        self.assertIn("RECENT", content)
        self.assertIn("STALE / ARCHIVE", content)

    # -------------------------------------------------------------------------
    # 5. Three-Tier Map Degradation Fallback
    # -------------------------------------------------------------------------
    def test_india_risk_map_three_tier_fallback(self):
        map_path = os.path.join(self.src_dir, "components", "map", "IndiaRiskMap.tsx")
        with open(map_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Three display modes
        self.assertIn("'map' | 'cards' | 'list'", content, "Must support map, cards, and list display modes.")
        self.assertIn("Map View", content, "Must provide map view option.")
        self.assertIn("State Cards", content, "Must provide state cards option.")
        self.assertIn("List View", content, "Must provide accessible list view option.")
        self.assertIn("mapRenderError", content, "Must track map render errors.")
        self.assertIn("Interactive Map Tiles Unavailable", content, "Must render fallback banner on map error.")

    # -------------------------------------------------------------------------
    # 6. Plain-Language Interpretations & Scientific Boundaries
    # -------------------------------------------------------------------------
    def test_risk_explanation_plain_language_glossary(self):
        explanation_path = os.path.join(self.src_dir, "components", "common", "RiskExplanation.tsx")
        with open(explanation_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Technical terms
        self.assertIn("Antecedent Rainfall", content)
        self.assertIn("River Stage & High Flood Level", content)
        self.assertIn("Model Probability & Likelihood", content)
        self.assertIn("Focal Depth", content)

        # Interactive controls
        self.assertIn("Why am I seeing this?", content)
        self.assertIn("Plain-Language Terminology Guide for Citizens", content)
        self.assertIn("Scientific Foundation & Verification Boundaries", content)

    def test_ml_scope_messaging_honesty(self):
        explanation_path = os.path.join(self.src_dir, "components", "common", "RiskExplanation.tsx")
        with open(explanation_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Assam prototype message
        self.assertIn("ML Prototype Estimate — Validated only for the Assam Brahmaputra and Barak basin prototype scope", content)
        # Non-Assam message
        self.assertIn("ML prediction unavailable for this region. Regional baseline risk and official disaster intelligence are shown.", content)

    # -------------------------------------------------------------------------
    # 7. Help Hub Explicit Verification & Direct Calling
    # -------------------------------------------------------------------------
    def test_get_help_page_verification_tags_and_tap_to_call(self):
        page_path = os.path.join(self.src_dir, "components", "pages", "GetHelpPage.tsx")
        with open(page_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("OFFICIAL GOVERNMENT", content)
        self.assertIn("VERIFIED NGO / AGENCY", content)
        self.assertIn("COMMUNITY AID", content)
        self.assertIn("Tap to Call:", content)
        self.assertIn("tel:${resource.phone}", content)
        self.assertIn("LIFE-SAFETY NOTICE", content)

    def test_help_others_page_verification_tags(self):
        page_path = os.path.join(self.src_dir, "components", "pages", "HelpOthersPage.tsx")
        with open(page_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("OFFICIAL GOVERNMENT", content)
        self.assertIn("VERIFIED NGO / AGENCY", content)
        self.assertIn("COMMUNITY AID", content)
        self.assertIn("tel:${res.phone}", content)

    # -------------------------------------------------------------------------
    # 8. Deep Linking & Routing Synchronization
    # -------------------------------------------------------------------------
    def test_app_deep_linking_and_routing_parameters(self):
        app_path = os.path.join(self.src_dir, "App.tsx")
        with open(app_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("params.get('page') || params.get('view')", content, "Must parse ?page and ?view query parameters.")
        self.assertIn("params.get('emergency')", content, "Must support ?emergency=true to auto-open EmergencyAccessHub.")
        self.assertIn("params.get('sos')", content, "Must support ?sos=true.")
        self.assertIn("params.get('incident')", content, "Must support ?incident=<id> deep linking.")
        self.assertIn("<CrisisProvider>", content, "App must be wrapped in CrisisProvider.")
        self.assertIn("<EmergencyAccessHub", content, "EmergencyAccessHub must be mounted globally in App.")

    # -------------------------------------------------------------------------
    # 9. Accessibility & Mobile Optimization (WCAG 2.1 AA)
    # -------------------------------------------------------------------------
    def test_accessibility_touch_targets_and_aria_attributes(self):
        navbar_path = os.path.join(self.src_dir, "components", "common", "Navbar.tsx")
        with open(navbar_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("min-h-[44px]", content, "Touch targets must satisfy minimum 44px WCAG touch criterion.")
        self.assertIn("aria-pressed", content, "Crisis mode toggle must have aria-pressed attribute.")
        self.assertIn("aria-label", content, "Interactive buttons must provide accessible aria-labels.")

    # -------------------------------------------------------------------------
    # 10. Frozen Model Artifact & Zero Nationwide ML Extrapolation
    # -------------------------------------------------------------------------
    def test_frozen_assam_prototype_artifact_integrity(self):
        # 1. Check Dataset Manifest
        manifest = dataset_manifest_registry.get_manifest("assam_flood_features_v1")
        self.assertIsNotNone(manifest, "Assam dataset manifest must be registered")
        self.assertEqual(manifest.synthetic_records, 0, "MANDATORY: synthetic_records must strictly equal 0")
        self.assertEqual(manifest.row_count, 32, "Audited row count must be exactly 32")

        # 2. Check Model Registry
        model = model_registry.get_model("assam_flood_prototype_v1")
        self.assertIsNotNone(model, "Assam flood model must be registered in model registry")
        self.assertEqual(model.status, ModelStatus.PROTOTYPE)
        self.assertIn("Assam", model.geographic_scope)
        self.assertEqual(len(model.feature_schema), 13, "Must strictly preserve 13 empirical features.")
        self.assertTrue(model.is_active)
        self.assertIn("not applicable outside assam", model.limitations.lower())

        # 3. Model joblib file must exist
        artifact_path = os.path.join(self.project_root, "ml", "flood", "artifacts", "model.joblib")
        self.assertTrue(os.path.exists(artifact_path), "Model artifact file model.joblib must exist.")


if __name__ == "__main__":
    unittest.main()
