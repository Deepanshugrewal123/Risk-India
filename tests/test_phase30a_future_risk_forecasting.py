"""
RISK // INDIA — PHASE 30A FUTURE RISK FORECASTING ARCHITECTURE TEST SUITE
==========================================================================
Comprehensive automated validation covering all Phase 30A dimensions:
1. 6 Core Risk Modes Conceptual Separation
2. Multi-Horizon Forecasting (NOW, 0-6H, 6-24H, 1-3D, 3-7D)
3. Strict Earthquake Non-Predictability Constraint
4. Prediction vs Forecast Methodology Tagging Honesty
5. Scientific Non-Assam ML Scope Guard Preservation
6. 14 Scientific Promotion Gates Across 5 Priority Basins
7. Disaster Action Protocols (Before / During / After)
8. Emergency Help Ecosystem ("I Need Help" & "I Want to Help")
9. End-to-End API Contracts (7 Endpoints Verified)
10. Forecast Freshness & Source Provenance Verification
11. Inviolate Scientific Asset Hashes & Zero Synthetic Data
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

from fastapi.testclient import TestClient
from app.main import app
from app.middleware.rate_limit import rate_limiter
from app.services.geo_basin_service import INDIAN_ADMINISTRATIVE_ENTITIES
from app.services.national_risk import SUPPORTED_HAZARDS

from app.services.future_risk import (
    RiskMode,
    MethodologyType,
    ConfidenceLevel,
    ForecastHorizon,
    ALL_FORECAST_HORIZONS,
    HAZARD_PREDICTABILITY_RULES,
    DisasterActionEngine,
    disaster_action_engine,
    HelpEcosystem,
    help_ecosystem,
    NationalMLExpansionGate,
    national_ml_expansion_gate,
    SCIENTIFIC_PROMOTION_GATES,
    FutureRiskEngine,
    future_risk_engine,
    FutureRiskService,
    future_risk_service,
)


class TestPhase30AFutureRiskForecasting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.expected_model_hash = "0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf"
        cls.expected_dataset_hash = "88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080"

    def setUp(self):
        rate_limiter.reset()

    def tearDown(self):
        rate_limiter.reset()

    # =========================================================================
    # 1. CORE RISK MODES SEPARATION
    # =========================================================================

    def test_01_core_risk_modes_defined_and_distinct(self):
        """Verify the 6 core risk modes exist, are distinct, and cannot be conflated."""
        expected_modes = {
            "CURRENT_DISASTER_INTELLIGENCE",
            "FUTURE_RISK_FORECAST",
            "REGIONAL_BASELINE_RISK",
            "EMPIRICAL_ML_PREDICTION",
            "OFFICIAL_WARNING",
            "EMERGENCY_RESOURCE_INTELLIGENCE",
        }
        actual_modes = {mode.value for mode in RiskMode}
        self.assertEqual(actual_modes, expected_modes)
        self.assertEqual(len(RiskMode), 6)

    def test_02_record_modes_never_conflated(self):
        """Verify future risk forecast records explicitly tag their mode as FUTURE_RISK_FORECAST."""
        records = future_risk_engine.evaluate_future_risk("Odisha", "CYCLONE", ForecastHorizon.HORIZON_6_24H.value)
        self.assertEqual(len(records), 1)
        assessment = records[0]
        self.assertEqual(assessment.risk_mode, RiskMode.FUTURE_RISK_FORECAST.value)
        self.assertNotEqual(assessment.risk_mode, RiskMode.CURRENT_DISASTER_INTELLIGENCE.value)
        self.assertNotEqual(assessment.risk_mode, RiskMode.EMPIRICAL_ML_PREDICTION.value)
        self.assertNotEqual(assessment.risk_mode, RiskMode.REGIONAL_BASELINE_RISK.value)

    # =========================================================================
    # 2. MULTI-HORIZON FORECASTING & EARTHQUAKE CONSTRAINT
    # =========================================================================

    def test_03_forecast_horizons_defined(self):
        """Verify all 5 forecast horizons are cleanly enumerated."""
        expected_horizons = ["NOW", "0_6_HOURS", "6_24_HOURS", "1_3_DAYS", "3_7_DAYS"]
        actual_horizons = [h for h in ALL_FORECAST_HORIZONS]
        self.assertEqual(actual_horizons, expected_horizons)

    def test_04_earthquake_non_predictability_enforced(self):
        """Verify earthquake is scientifically non-predictable for forward horizons."""
        rule = HAZARD_PREDICTABILITY_RULES["EARTHQUAKE"]
        self.assertEqual(rule["suitable_horizons"], [ForecastHorizon.NOW.value])
        self.assertIn("scientific_disclaimer", rule)
        self.assertIn("SCIENTIFICALLY IMPOSSIBLE", rule["predictability_basis"])

        # Test evaluating forward horizon for Earthquake: confidence must be UNAVAILABLE
        for horizon in [
            ForecastHorizon.HORIZON_0_6H.value,
            ForecastHorizon.HORIZON_6_24H.value,
            ForecastHorizon.HORIZON_1_3D.value,
            ForecastHorizon.HORIZON_3_7D.value
        ]:
            records = future_risk_engine.evaluate_future_risk("Uttarakhand", "EARTHQUAKE", horizon)
            self.assertEqual(len(records), 1)
            eq_assessment = records[0]
            self.assertEqual(eq_assessment.confidence, ConfidenceLevel.UNAVAILABLE.value)
            self.assertIn("scientifically impossible", eq_assessment.summary.lower())
            self.assertEqual(eq_assessment.methodology, MethodologyType.REGIONAL_BASELINE.value)

        # Test evaluating NOW horizon for Earthquake
        now_records = future_risk_engine.evaluate_future_risk("Uttarakhand", "EARTHQUAKE", ForecastHorizon.NOW.value)
        self.assertEqual(len(now_records), 1)
        eq_now = now_records[0]
        self.assertEqual(eq_now.risk_mode, RiskMode.CURRENT_DISASTER_INTELLIGENCE.value)
        self.assertEqual(eq_now.confidence, ConfidenceLevel.HIGH.value)

    def test_05_predictable_hazards_support_forward_horizons(self):
        """Verify flood, cyclone, and heatwave allow forward forecasting within their allowed horizons."""
        for hazard in ["FLOOD", "CYCLONE", "HEATWAVE"]:
            rule = HAZARD_PREDICTABILITY_RULES[hazard]
            self.assertIn(ForecastHorizon.HORIZON_1_3D.value, rule["suitable_horizons"])

            records = future_risk_engine.evaluate_future_risk("Gujarat", hazard, ForecastHorizon.HORIZON_1_3D.value)
            self.assertEqual(len(records), 1)
            assessment = records[0]
            self.assertNotEqual(assessment.confidence, ConfidenceLevel.UNAVAILABLE.value)
            self.assertGreaterEqual(assessment.risk_score, 0)
            self.assertLessEqual(assessment.risk_score, 100)

    # =========================================================================
    # 3. METHODOLOGY HONESTY & NON-ASSAM ML SCOPE GUARD
    # =========================================================================

    def test_06_prediction_vs_forecast_methodology_tagging(self):
        """Verify every forecast honestly indicates its methodology type."""
        # Non-Assam flood must NOT claim ML
        bihar_records = future_risk_engine.evaluate_future_risk("Bihar", "FLOOD", ForecastHorizon.HORIZON_6_24H.value)
        self.assertEqual(len(bihar_records), 1)
        bihar_flood = bihar_records[0]
        self.assertNotEqual(bihar_flood.methodology, MethodologyType.EMPIRICAL_ML.value)
        self.assertIn("ML prediction unavailable", bihar_flood.ml_scope_note)

        # Assam flood reports validated prototype note
        assam_records = future_risk_engine.evaluate_future_risk("Assam", "FLOOD", ForecastHorizon.HORIZON_6_24H.value)
        self.assertEqual(len(assam_records), 1)
        assam_flood = assam_records[0]
        self.assertIn("assam_flood_prototype_v1", assam_flood.ml_scope_note)

    def test_07_non_flood_assam_never_claims_flood_ml(self):
        """Verify that Assam for non-flood hazards (e.g. Earthquake, Cyclone) never claims flood ML."""
        assam_records = future_risk_engine.evaluate_future_risk("Assam", "EARTHQUAKE", ForecastHorizon.NOW.value)
        self.assertEqual(len(assam_records), 1)
        assam_eq = assam_records[0]
        self.assertIn("No ML prediction exists or is claimed for earthquakes", assam_eq.ml_scope_note)

    # =========================================================================
    # 4. 14 SCIENTIFIC ML EXPANSION GATES ACROSS 5 BASINS
    # =========================================================================

    def test_08_ml_expansion_14_scientific_gates(self):
        """Verify 14 scientific promotion gates are evaluated across all 5 priority basins."""
        evals = national_ml_expansion_gate.evaluate_all_priority_basins()
        self.assertEqual(len(evals), 5)
        self.assertEqual(len(SCIENTIFIC_PROMOTION_GATES), 14)

        basin_names = {b["basin"] for b in evals}
        self.assertEqual(basin_names, {"brahmaputra", "ganga", "godavari", "mahanadi", "krishna"})

        # Brahmaputra (Assam) should be APPROVED
        brahmaputra = next(b for b in evals if b["basin"] == "brahmaputra")
        self.assertTrue(brahmaputra["ml_ready"])
        self.assertEqual(brahmaputra["model_status"], "APPROVED")
        self.assertEqual(len(brahmaputra["failed_gates"]), 0)

        # Other 4 basins MUST be NOT_APPROVED
        for basin_id in ["ganga", "godavari", "mahanadi", "krishna"]:
            basin = next(b for b in evals if b["basin"] == basin_id)
            self.assertFalse(basin["ml_ready"])
            self.assertEqual(basin["model_status"], "NOT_APPROVED")
            self.assertGreater(len(basin["failed_gates"]), 0)

    # =========================================================================
    # 5. DISASTER ACTION PROTOCOLS (BEFORE / DURING / AFTER)
    # =========================================================================

    def test_09_action_engine_guidance_for_all_hazards(self):
        """Verify actionable Before / During / After protocols exist for all 6 hazards."""
        for hazard in SUPPORTED_HAZARDS:
            guidance = disaster_action_engine.get_actions_for_hazard(hazard)
            self.assertIn("BEFORE", guidance)
            self.assertIn("DURING", guidance)
            self.assertIn("AFTER", guidance)

            self.assertGreater(len(guidance["BEFORE"]), 0)
            self.assertGreater(len(guidance["DURING"]), 0)
            self.assertGreater(len(guidance["AFTER"]), 0)

    def test_10_action_engine_regional_context(self):
        """Verify region-specific action protocols partition into life-safety phases."""
        actions = disaster_action_engine.get_actions_for_region("Kerala", "FLOOD")
        self.assertEqual(actions["region"], "Kerala")
        self.assertEqual(actions["hazard_type"], "FLOOD")
        self.assertIn("before_event", actions)
        self.assertIn("during_event", actions)
        self.assertIn("after_event", actions)
        self.assertIn("emergency_dispatch", actions)

    # =========================================================================
    # 6. EMERGENCY HELP ECOSYSTEM ("I NEED HELP" & "I WANT TO HELP")
    # =========================================================================

    def test_11_emergency_dispatch_and_statutory_channels(self):
        """Verify emergency dispatch numbers and strictly verified statutory donation/volunteer channels."""
        help_package = help_ecosystem.get_assistance_directory(state="Odisha")

        self.assertIn("anti_fraud_notice", help_package)
        self.assertIn("i_need_help", help_package)
        self.assertIn("i_want_to_help", help_package)

        # "I Need Help" section
        need_help = help_package["i_need_help"]
        self.assertIn("emergency_numbers", need_help)
        numbers = [item["number"] for item in need_help["emergency_numbers"]]
        self.assertIn("112", numbers)
        self.assertIn("1078", numbers)
        self.assertIn("108", numbers)

        # "I Want to Help" section: strictly statutory
        want_help = help_package["i_want_to_help"]
        self.assertIn("statutory_relief_funds", want_help)
        funds = want_help["statutory_relief_funds"]
        fund_names = [f["name"] for f in funds]
        self.assertTrue(any("Prime Minister" in n for n in fund_names))
        for f in funds:
            self.assertIn("STATUTORY", f["verification_status"])

    # =========================================================================
    # 7. END-TO-END API CONTRACTS
    # =========================================================================

    def test_12_api_future_risk_national_summary(self):
        """Contract test: GET /api/future-risk returns national multi-hazard future risk summary."""
        rate_limiter.reset()
        resp = self.client.get("/api/future-risk")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data["total_entities_evaluated"], 36)
        self.assertEqual(data["states_covered"], 28)
        self.assertEqual(data["union_territories_covered"], 8)
        self.assertEqual(len(data["regions"]), 36)
        self.assertEqual(data["synthetic_records"], 0)

    def test_13_api_future_risk_help_ecosystem(self):
        """Contract test: GET /api/future-risk/help returns emergency and statutory help package."""
        rate_limiter.reset()
        resp = self.client.get("/api/future-risk/help?state=Tamil%20Nadu")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertIn("i_need_help", data)
        self.assertIn("i_want_to_help", data)

    def test_14_api_future_risk_ml_expansion(self):
        """Contract test: GET /api/future-risk/ml-expansion returns 14 scientific gate audit."""
        rate_limiter.reset()
        resp = self.client.get("/api/future-risk/ml-expansion")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertIn("priority_basins", data)
        self.assertEqual(len(data["priority_basins"]), 5)
        self.assertEqual(data["synthetic_records"], 0)

    def test_15_api_future_risk_regional_profile(self):
        """Contract test: GET /api/future-risk/{region} returns regional future risk profile."""
        rate_limiter.reset()
        resp = self.client.get("/api/future-risk/Maharashtra")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data["region"]["name"], "Maharashtra")
        self.assertIn("highest_future_risk", data)
        self.assertIn("hazards_forward_assessment", data)
        self.assertEqual(len(data["hazards_forward_assessment"]), 6)
        self.assertIn("action_checklist", data)
        self.assertEqual(data["synthetic_records"], 0)

    def test_16_api_future_risk_actions_endpoint(self):
        """Contract test: GET /api/future-risk/{region}/actions returns action checklists."""
        rate_limiter.reset()
        resp = self.client.get("/api/future-risk/Assam/actions?hazard=FLOOD")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data["region"], "Assam")
        self.assertEqual(data["hazard_type"], "FLOOD")
        self.assertIn("before_event", data)
        self.assertIn("during_event", data)
        self.assertIn("after_event", data)

    def test_17_api_future_risk_hazard_endpoint(self):
        """Contract test: GET /api/future-risk/{region}/{hazard} returns single hazard evaluation."""
        rate_limiter.reset()
        resp = self.client.get("/api/future-risk/West%20Bengal/CYCLONE")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data["region"]["name"], "West Bengal")
        self.assertEqual(data["hazard_type"], "CYCLONE")
        self.assertIn("timeline", data)

    def test_18_api_future_risk_timeline_endpoint(self):
        """Contract test: GET /api/future-risk/{region}/{hazard}/timeline returns all 5 horizons."""
        rate_limiter.reset()
        resp = self.client.get("/api/future-risk/Rajasthan/HEATWAVE/timeline")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data["region"]["name"], "Rajasthan")
        self.assertEqual(data["hazard_type"], "HEATWAVE")
        self.assertEqual(len(data["timeline"]), 5)

        horizons_returned = [pt["forecast_window"] for pt in data["timeline"]]
        self.assertEqual(horizons_returned, ["NOW", "0_6_HOURS", "6_24_HOURS", "1_3_DAYS", "3_7_DAYS"])

    def test_19_api_future_risk_invalid_region_and_hazard_error_handling(self):
        """Contract test: Invalid regions return 404, invalid hazards return 400."""
        rate_limiter.reset()
        resp_bad_region = self.client.get("/api/future-risk/Atlantis")
        self.assertEqual(resp_bad_region.status_code, 404)
        self.assertIn("not found", resp_bad_region.json()["detail"].lower())

        rate_limiter.reset()
        resp_bad_hazard = self.client.get("/api/future-risk/Assam/VOLCANO")
        self.assertEqual(resp_bad_hazard.status_code, 400)
        self.assertIn("not supported", resp_bad_hazard.json()["detail"].lower())

    # =========================================================================
    # 8. FRESHNESS & SOURCE PROVENANCE INTEGRITY
    # =========================================================================

    def test_20_forecast_freshness_and_provenance_audit(self):
        """Verify that every future risk record has independent freshness and valid-until tracking."""
        records = future_risk_engine.evaluate_future_risk("Assam", "FLOOD", ForecastHorizon.HORIZON_0_6H.value)
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertIn("freshness", record.to_dict())
        self.assertIn("provenance", record.to_dict())
        self.assertTrue(record.freshness["evaluated_independent_of_severity"])
        self.assertTrue(record.provenance["zero_synthetic_records_guarantee"])

    # =========================================================================
    # 9. INVIOLATE SCIENTIFIC ASSET HASHES & ZERO SYNTHETIC DATA
    # =========================================================================

    def test_21_model_and_dataset_sha256_invariance(self):
        """Verify that model.joblib and flood_features.csv remain byte-for-byte unmodified."""
        model_path = PROJECT_ROOT / "ml" / "flood" / "artifacts" / "model.joblib"
        data_path = PROJECT_ROOT / "datasets" / "processed" / "flood_assam" / "flood_features.csv"

        self.assertTrue(model_path.exists(), "model.joblib missing")
        self.assertTrue(data_path.exists(), "flood_features.csv missing")

        with open(model_path, "rb") as f:
            actual_model_hash = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(actual_model_hash, self.expected_model_hash, "MODEL.JOBLIB HASH MISMATCH")

        with open(data_path, "rb") as f:
            actual_data_hash = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(actual_data_hash, self.expected_dataset_hash, "FLOOD_FEATURES.CSV HASH MISMATCH")

    def test_22_zero_synthetic_data_contract(self):
        """Verify zero synthetic records exist in future risk architecture."""
        evals = national_ml_expansion_gate.evaluate_all_priority_basins()
        for basin in evals:
            if basin["basin"] == "brahmaputra":
                self.assertEqual(basin["empirical_observations"], 32)
                self.assertEqual(basin["corroborated_events"], 12)
            else:
                self.assertEqual(basin["empirical_observations"], 0)
                self.assertEqual(basin["corroborated_events"], 0)


if __name__ == "__main__":
    unittest.main()
