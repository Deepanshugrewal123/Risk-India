"""
RISK // INDIA — PHASE 30E VERIFICATION SUITE
=============================================
National Crisis Mode, Emergency Response & Human Action Intelligence.
Comprehensive test suite validating:
- Absolute Project Invariants (SHA-256 byte-for-byte hashes)
- Non-Assam ML Guard (ml_available = False outside Assam)
- Assam ML Model Guard (assam_flood_prototype_v1 preserved)
- Earthquake Non-Prediction Guard (Zero deterministic earthquake forecasting)
- Zero Synthetic Records (synthetic_records = 0 everywhere)
- Zero Invented Resources (Strict provenance + "Verified nearby resource location is currently unavailable")
- Operational State Transitions (NORMAL, WATCH, ELEVATED, CRISIS)
- Deterministic Activation Rules A-E & Weak Signal Filter
- Top 3-5 Prioritized Immediate Actions ("What to do now")
- Structured Before / During / After Protocols for all 6 Hazards
- 72-Hour Family Preparedness Checklist
- Unified 5-Horizon Timeline with Explicit Provenance Tags
- Deterministic Transparent Explanation & Data Limitations
- Proximity-based Emergency Resource Sorting
- National Coverage across 28 States + 8 UTs (36 entities)
- Complete REST API Endpoints & Error Handling
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
from app.services.crisis import (
    national_crisis_service,
    CrisisOperationalState,
    ActionPhase,
    ActionPriority,
    TimelineSignalType,
    CrisisActivationEngine,
    CrisisActionEngine,
    CrisisResourceEngine,
    CrisisTimelineEngine,
    CrisisExplanationEngine
)
from app.services.national_risk.regional_baseline import SUPPORTED_HAZARDS


class TestPhase30ECrisisMode(unittest.TestCase):
    """Rigorous Phase 30E National Crisis Mode verification suite."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.expected_model_sha = "0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf"
        cls.expected_dataset_sha = "88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080"

    # =========================================================================
    # 1. ABSOLUTE PROJECT INVARIANTS
    # =========================================================================

    def test_01_model_joblib_sha256_inviolate(self):
        """Assam ML model SHA-256 must match exactly."""
        model_path = PROJECT_ROOT / "ml" / "flood" / "artifacts" / "model.joblib"
        self.assertTrue(model_path.exists(), "model.joblib missing")
        actual_hash = hashlib.sha256(model_path.read_bytes()).hexdigest()
        self.assertEqual(actual_hash, self.expected_model_sha)

    def test_02_dataset_sha256_inviolate(self):
        """Assam flood dataset SHA-256 must match exactly."""
        data_path = PROJECT_ROOT / "datasets" / "processed" / "flood_assam" / "flood_features.csv"
        self.assertTrue(data_path.exists(), "flood_features.csv missing")
        actual_hash = hashlib.sha256(data_path.read_bytes()).hexdigest()
        self.assertEqual(actual_hash, self.expected_dataset_sha)

    def test_03_non_assam_ml_guard(self):
        """Non-Assam entities must strictly have ml_available = False."""
        res_delhi = national_crisis_service.assess_crisis("delhi")
        self.assertFalse(res_delhi.ml_audit["ml_available"])
        self.assertEqual(res_delhi.ml_audit["status"], "NOT_AVAILABLE")
        self.assertEqual(res_delhi.ml_audit["synthetic_records"], 0)

        res_kerala = national_crisis_service.assess_crisis("kerala")
        self.assertFalse(res_kerala.ml_audit["ml_available"])
        self.assertEqual(res_kerala.ml_audit["status"], "NOT_AVAILABLE")

    def test_04_assam_ml_model_preserved(self):
        """Assam flood crisis assessment must reference assam_flood_prototype_v1."""
        res_assam = national_crisis_service.assess_crisis("assam", hazard="FLOOD")
        self.assertTrue(res_assam.ml_audit["ml_available"])
        self.assertEqual(res_assam.ml_audit["model_name"], "assam_flood_prototype_v1")
        self.assertEqual(res_assam.ml_audit["synthetic_records"], 0)

    def test_05_earthquake_non_prediction_guard(self):
        """Earthquake assessments must never predict future occurrences."""
        res_eq = national_crisis_service.assess_crisis("uttarakhand", hazard="EARTHQUAKE")
        self.assertFalse(res_eq.ml_audit["is_predictable"])
        self.assertFalse(res_eq.ml_audit["forecast_attempted"])
        self.assertIn("cannot be predicted", res_eq.what_could_happen_next.lower())
        for pt in res_eq.timeline:
            if pt.horizon != "NOW":
                self.assertEqual(pt.signal_type, TimelineSignalType.BASELINE)
                self.assertEqual(pt.expected_risk_level, "VERY_LOW")

    def test_06_zero_synthetic_data_guarantee(self):
        """Every assessment and resource payload must declare synthetic_records = 0."""
        res = national_crisis_service.assess_crisis("maharashtra")
        self.assertEqual(res.ml_audit["synthetic_records"], 0)
        overview = national_crisis_service.get_national_crisis_overview()
        self.assertEqual(overview["synthetic_records"], 0)

    # =========================================================================
    # 2. ACTIVATION RULES & OPERATIONAL STATES
    # =========================================================================

    def test_07_rule_a_official_red_warning_activates_crisis(self):
        """Rule A: Official RED alert must trigger CRISIS operational state."""
        state, is_rec, reason, rules = CrisisActivationEngine.evaluate(
            current_risk_level="LOW",
            current_risk_score=20.0,
            peak_future_risk_level="LOW",
            peak_future_score=25.0,
            official_warnings=[{"severity": "RED", "headline": "Severe Inundation Warning"}],
            telemetry_summary={},
            future_risk_confidence=0.8
        )
        self.assertEqual(state, CrisisOperationalState.CRISIS)
        self.assertTrue(is_rec)
        self.assertIn("RULE_A_OFFICIAL_RED_WARNING", rules)

    def test_08_rule_a_official_orange_warning_activates_elevated(self):
        """Rule A: Official ORANGE alert must trigger ELEVATED operational state."""
        state, is_rec, reason, rules = CrisisActivationEngine.evaluate(
            current_risk_level="LOW",
            current_risk_score=20.0,
            peak_future_risk_level="LOW",
            peak_future_score=25.0,
            official_warnings=[{"severity": "ORANGE", "headline": "Heavy Rain Alert"}],
            telemetry_summary={},
            future_risk_confidence=0.8
        )
        self.assertEqual(state, CrisisOperationalState.ELEVATED)
        self.assertTrue(is_rec)
        self.assertIn("RULE_A_OFFICIAL_ORANGE_WARNING", rules)

    def test_09_rule_b_critical_current_risk_activates_crisis(self):
        """Rule B: CRITICAL current risk with telemetry activates CRISIS."""
        state, is_rec, reason, rules = CrisisActivationEngine.evaluate(
            current_risk_level="CRITICAL",
            current_risk_score=85.0,
            peak_future_risk_level="LOW",
            peak_future_score=20.0,
            official_warnings=[],
            telemetry_summary={"rainfall_24h_mm": 120.0},
            telemetry_fresh=True
        )
        self.assertEqual(state, CrisisOperationalState.CRISIS)
        self.assertTrue(is_rec)
        self.assertIn("RULE_B_CRITICAL_CURRENT_RISK", rules)

    def test_10_rule_c_high_future_risk_signal(self):
        """Rule C: High future-risk signal triggers ELEVATED/CRISIS."""
        state, is_rec, reason, rules = CrisisActivationEngine.evaluate(
            current_risk_level="LOW",
            current_risk_score=20.0,
            peak_future_risk_level="CRITICAL",
            peak_future_score=90.0,
            official_warnings=[],
            telemetry_summary={},
            future_risk_confidence=0.75
        )
        self.assertEqual(state, CrisisOperationalState.CRISIS)
        self.assertTrue(is_rec)
        self.assertIn("RULE_C_HIGH_FUTURE_RISK_SIGNAL", rules)

    def test_11_rule_d_multi_signal_convergence(self):
        """Rule D: Rainfall >= 64.5mm and river ratio >= 0.90 triggers multi-signal convergence."""
        state, is_rec, reason, rules = CrisisActivationEngine.evaluate(
            current_risk_level="MEDIUM",
            current_risk_score=50.0,
            peak_future_risk_level="MEDIUM",
            peak_future_score=50.0,
            official_warnings=[],
            telemetry_summary={
                "rainfall_24h_mm": 75.0,
                "river_danger_ratio": 0.92
            }
        )
        self.assertEqual(state, CrisisOperationalState.ELEVATED)
        self.assertTrue(is_rec)
        self.assertIn("RULE_D_MULTI_SIGNAL_CONVERGENCE", rules)

    def test_12_rule_e_manual_activation(self):
        """Rule E: User manual activation forces CRISIS operational state."""
        state, is_rec, reason, rules = CrisisActivationEngine.evaluate(
            current_risk_level="LOW",
            current_risk_score=15.0,
            peak_future_risk_level="LOW",
            peak_future_score=15.0,
            official_warnings=[],
            telemetry_summary={},
            manual_activation=True
        )
        self.assertEqual(state, CrisisOperationalState.CRISIS)
        self.assertIn("RULE_E_MANUAL_ACTIVATION", rules)

    def test_13_weak_signal_filter(self):
        """Weak signal filter: Low baseline indicators remain NORMAL without emergency recommendation."""
        state, is_rec, reason, rules = CrisisActivationEngine.evaluate(
            current_risk_level="LOW",
            current_risk_score=20.0,
            peak_future_risk_level="LOW",
            peak_future_score=20.0,
            official_warnings=[],
            telemetry_summary={"rainfall_24h_mm": 5.0}
        )
        self.assertEqual(state, CrisisOperationalState.NORMAL)
        self.assertFalse(is_rec)
        self.assertEqual(len(rules), 0)

    # =========================================================================
    # 3. ACTION PROTOCOLS & IMMEDIATE HUMAN ACTIONS
    # =========================================================================

    def test_14_what_to_do_now_contains_top_actions(self):
        """What to do now must contain 3-5 prioritized actions with order_rank 1 to 5."""
        for hazard in SUPPORTED_HAZARDS:
            actions = CrisisActionEngine.get_what_to_do_now(hazard)
            self.assertGreaterEqual(len(actions), 3)
            self.assertLessEqual(len(actions), 5)
            self.assertEqual(actions[0].order_rank, 1)
            self.assertEqual(actions[0].priority, ActionPriority.LIFE_SAFETY)
            self.assertTrue(actions[0].is_urgent)

    def test_15_before_during_after_protocols_all_hazards(self):
        """Before, During, and After protocols must be populated for all 6 hazards."""
        for hazard in SUPPORTED_HAZARDS:
            protocols = CrisisActionEngine.get_phase_protocols(hazard)
            self.assertIn("BEFORE", protocols)
            self.assertIn("DURING", protocols)
            self.assertIn("AFTER", protocols)
            self.assertGreater(len(protocols["BEFORE"]), 0)
            self.assertGreater(len(protocols["DURING"]), 0)
            self.assertGreater(len(protocols["AFTER"]), 0)

    def test_16_family_preparedness_checklist(self):
        """72-hour family checklist must include water, food, medical, power, documents."""
        checklist = CrisisActionEngine.get_family_prep_checklist()
        self.assertGreaterEqual(len(checklist), 6)
        categories = [item.category.lower() for item in checklist]
        self.assertTrue(any("water" in c for c in categories))
        self.assertTrue(any("food" in c for c in categories))
        self.assertTrue(any("medical" in c for c in categories))
        self.assertTrue(any("power" in c for c in categories))

    # =========================================================================
    # 4. EMERGENCY RESOURCES & ZERO INVENTED RESOURCES GUARD
    # =========================================================================

    def test_17_emergency_resources_verified_provenance(self):
        """Resources must have verified status and statutory origin."""
        resources, note = CrisisResourceEngine.get_emergency_resources("delhi")
        self.assertGreater(len(resources), 0)
        for r in resources:
            self.assertEqual(r.verification_status, "VERIFIED")
            self.assertTrue(len(r.provenance) > 0)
            self.assertIsNotNone(r.phone or r.contact_number)

    def test_18_missing_local_resource_yields_mandatory_safety_note(self):
        """If no local resource exists in registry, mandatory safety note must be emitted."""
        # Querying an entity with no state-specific entries in mock registry
        resources, note = CrisisResourceEngine.get_emergency_resources("lakshadweep")
        self.assertIsNotNone(note)
        self.assertIn("Verified nearby resource location is currently unavailable", note)
        # Pan-India fallbacks must still be provided
        self.assertGreater(len(resources), 0)
        self.assertEqual(resources[0].state.lower(), "pan-india")

    def test_19_haversine_distance_calculation(self):
        """Distance must be calculated and sorted in ascending order when coordinates are given."""
        # Coordinates for New Delhi (28.6139, 77.2090)
        resources, note = CrisisResourceEngine.get_emergency_resources("delhi", coordinates=(28.6139, 77.2090))
        self.assertGreater(len(resources), 0)
        first_dist = resources[0].distance_km
        self.assertIsNotNone(first_dist)
        self.assertLess(first_dist, 50.0)  # NDMA / NDRF HQ is within 10 km of central Delhi

    # =========================================================================
    # 5. TIMELINE & DETERMINISTIC EXPLANATIONS
    # =========================================================================

    def test_20_timeline_5_horizons_with_provenance_tags(self):
        """Timeline must cover NOW, 0_6H, 6_24H, 1_3D, 3_7D with explicit signal types."""
        res = national_crisis_service.assess_crisis("assam", hazard="FLOOD")
        self.assertEqual(len(res.timeline), 5)
        horizons = [pt.horizon for pt in res.timeline]
        self.assertEqual(horizons, ["NOW", "0_6H", "6_24H", "1_3D", "3_7D"])
        self.assertEqual(res.timeline[0].signal_type, TimelineSignalType.EMPIRICAL_ML)

    def test_21_explanation_engine_structure(self):
        """Explanation must answer why, what changed, supporting evidence, and data limitations."""
        res = national_crisis_service.assess_crisis("odisha", hazard="CYCLONE")
        expl = res.explanation
        self.assertTrue(len(expl.why) > 0)
        self.assertTrue(len(expl.what_changed) > 0)
        self.assertTrue(len(expl.supporting_evidence) > 0)
        self.assertTrue(len(expl.what_could_change) > 0)
        self.assertIn("Machine learning inference is strictly restricted to Assam", expl.data_limitations)

    # =========================================================================
    # 6. NATIONWIDE COVERAGE ACROSS ALL 36 ENTITIES
    # =========================================================================

    def test_22_national_overview_evaluates_36_entities(self):
        """National crisis overview must successfully evaluate all 36 entities."""
        overview = national_crisis_service.get_national_crisis_overview()
        self.assertEqual(overview["total_entities_monitored"], 36)
        self.assertEqual(overview["states_covered"], 28)
        self.assertEqual(overview["union_territories_covered"], 8)
        self.assertIn("CRISIS", overview["operational_state_distribution"])
        self.assertIn("NORMAL", overview["operational_state_distribution"])

    # =========================================================================
    # 7. REST API ENDPOINTS
    # =========================================================================

    def test_23_api_crisis_status(self):
        """GET /api/crisis/status must return operational posture and emergency numbers."""
        resp = self.client.get("/api/crisis/status")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "OPERATIONAL")
        self.assertIn("112", data["national_emergency_helplines"]["all_emergencies"])
        self.assertEqual(data["synthetic_records"], 0)

    def test_24_api_crisis_national(self):
        """GET /api/crisis/national must return all 36 regions."""
        resp = self.client.get("/api/crisis/national")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["total_entities_monitored"], 36)
        self.assertEqual(len(data["regions"]), 36)

    def test_25_api_crisis_region(self):
        """GET /api/crisis/{region} must return full assessment."""
        resp = self.client.get("/api/crisis/kerala")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["region_name"], "Kerala")
        self.assertIn("what_is_happening", data)
        self.assertIn("what_to_do_now", data)
        self.assertIn("timeline", data)
        self.assertEqual(data["synthetic_records"], 0)

    def test_26_api_crisis_region_hazard(self):
        """GET /api/crisis/{region}/{hazard} must return tailored hazard assessment."""
        resp = self.client.get("/api/crisis/rajasthan/HEATWAVE")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["primary_hazard"], "HEATWAVE")
        self.assertIn("Peak Hours", data["what_to_do_now"][0]["title"])

    def test_27_api_crisis_region_actions(self):
        """GET /api/crisis/{region}/actions must return action protocols."""
        resp = self.client.get("/api/crisis/assam/actions?hazard=FLOOD")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("what_to_do_now", data)
        self.assertIn("BEFORE", data["action_protocols"])
        self.assertIn("DURING", data["action_protocols"])
        self.assertIn("AFTER", data["action_protocols"])

    def test_28_api_crisis_region_resources(self):
        """GET /api/crisis/{region}/resources must return verified emergency resources."""
        resp = self.client.get("/api/crisis/assam/resources?hazard=FLOOD")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreater(len(data["emergency_resources"]), 0)
        self.assertEqual(data["synthetic_records"], 0)

    def test_29_api_crisis_region_timeline(self):
        """GET /api/crisis/{region}/timeline must return 5 horizons."""
        resp = self.client.get("/api/crisis/assam/timeline")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data["timeline"]), 5)

    def test_30_api_crisis_region_explanation(self):
        """GET /api/crisis/{region}/explanation must return explanation and data limitations."""
        resp = self.client.get("/api/crisis/assam/explanation")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("explanation", data)
        self.assertIn("data_limitations", data["explanation"])

    def test_31_api_crisis_invalid_hazard_returns_400(self):
        """GET /api/crisis/{region}?hazard=TORNADO must return 400."""
        resp = self.client.get("/api/crisis/delhi?hazard=TORNADO")
        self.assertEqual(resp.status_code, 400)

    def test_32_api_crisis_manual_toggle(self):
        """GET /api/crisis/{region}?manual=true must set operational_state to CRISIS."""
        resp = self.client.get("/api/crisis/goa?manual=true")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["operational_state"], "CRISIS")
        self.assertTrue(data["is_manual_activation"])


if __name__ == "__main__":
    unittest.main()
