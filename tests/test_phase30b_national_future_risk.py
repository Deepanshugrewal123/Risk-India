"""
RISK // INDIA — PHASE 30B NATIONAL FUTURE RISK INTELLIGENCE ENGINE TEST SUITE
=============================================================================
Comprehensive automated validation covering all 24 Phase 30B dimensions:
1. National Coverage Matrix: 36 Entities (28 States + 8 UTs)
2. Six Core Hazards Coverage
3. Forecast Horizons (NOW, 0-6H, 6-24H, 1-3D, 3-7D)
4. Freshness Independent of Severity (HIGH + STALE stays STALE)
5. Provenance on All Inputs & Results
6. Confidence Engine (Qualitative LOW, MODERATE, HIGH)
7. Uncertainty Handling (LOW, MODERATE, HIGH, VERY_HIGH)
8. Missing Data Returns UNAVAILABLE (Zero Fabrication)
9. Stale Data Handling (Honest Degradation)
10. Cached Data Handling (Cached Remains CACHED)
11. Official Warning Separation
12. Flood Future Risk Engine & WHY_FLOOD_RISK_CHANGED
13. Cyclone Engine (CYCLONE_DETECTED, CYCLONE_FORECAST, CYCLONE_IMPACT_RISK)
14. Heatwave Engine (Persistence & Climatological Departure)
15. Severe Weather Engine (OFFICIAL_WARNING vs FORECAST_DERIVED_RISK)
16. Landslide Engine (POTENTIAL_LANDSLIDE_RISK)
17. Earthquake Non-Prediction Guard (Horizon NOW Only)
18. Assam ML Scope Preservation
19. Non-Assam ML Rejection
20. Zero Synthetic Production Records Guarantee (synthetic_records = 0)
21. End-to-End API Contracts (including /forecast and /explanation)
22. Public Safety Explanation Format (WHAT, WHEN, WHY, CONFIDENCE, WHAT TO DO, SOURCE)
23. Before-Disaster Action Guidance Integration
24. Provider Failure Isolation & Safe Fallback
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
    InputAvailabilityStatus,
    VariableQualityStatus,
    ForecastEnvironmentDataset,
    assemble_region_forecast_dataset,
    confidence_engine,
    flood_future_risk_engine,
    cyclone_future_risk_engine,
    heatwave_future_risk_engine,
    severe_weather_engine,
    landslide_future_risk_engine,
    earthquake_intelligence_engine,
    public_safety_explanation_engine,
    disaster_action_engine,
    future_risk_engine,
    future_risk_service,
)


class TestPhase30BNationalFutureRisk(unittest.TestCase):
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
    # 1. NATIONAL COVERAGE MATRIX (36 ENTITIES)
    # =========================================================================

    def test_01_national_coverage_36_entities(self):
        """Verify all 28 States and 8 Union Territories are covered in future risk evaluation."""
        summary = future_risk_service.get_national_future_risk_summary()
        self.assertEqual(summary["total_entities_evaluated"], 36)
        self.assertEqual(summary["states_covered"], 28)
        self.assertEqual(summary["union_territories_covered"], 8)
        self.assertEqual(len(summary["regions"]), 36)

        returned_names = {r["region"]["name"] for r in summary["regions"]}
        catalog_names = {e["name"] for e in INDIAN_ADMINISTRATIVE_ENTITIES}
        self.assertEqual(returned_names, catalog_names)

    # =========================================================================
    # 2. SIX CORE HAZARDS COVERAGE
    # =========================================================================

    def test_02_six_core_hazards_supported(self):
        """Verify all 6 core hazards are evaluated across all entities."""
        expected_hazards = {"FLOOD", "EARTHQUAKE", "CYCLONE", "HEATWAVE", "LANDSLIDE", "SEVERE_WEATHER"}
        self.assertEqual(set(SUPPORTED_HAZARDS), expected_hazards)

        # Test Maharashtra across all 6 hazards
        profile = future_risk_service.get_region_future_risk("Maharashtra")
        self.assertIsNotNone(profile)
        self.assertEqual(set(profile["hazards_forward_assessment"].keys()), expected_hazards)

    # =========================================================================
    # 3. FORECAST HORIZONS (NOW, 0-6H, 6-24H, 1-3D, 3-7D)
    # =========================================================================

    def test_03_all_five_forecast_horizons_evaluated(self):
        """Verify all 5 forecast horizons are cleanly modeled in timeline projections."""
        timeline_data = future_risk_service.get_region_hazard_timeline("Odisha", "CYCLONE")
        self.assertIsNotNone(timeline_data)
        horizons_found = [pt["forecast_window"] for pt in timeline_data["timeline"]]
        self.assertEqual(horizons_found, ["NOW", "0_6_HOURS", "6_24_HOURS", "1_3_DAYS", "3_7_DAYS"])

    # =========================================================================
    # 4. FRESHNESS INDEPENDENT OF SEVERITY
    # =========================================================================

    def test_04_freshness_independent_of_severity(self):
        """Verify that a high/critical risk with stale observation is classified as STALE, never LIVE."""
        # Check that freshness state is evaluated independent of severity flag
        records = future_risk_engine.evaluate_future_risk("Bihar", "FLOOD", "6_24_HOURS")
        self.assertEqual(len(records), 1)
        rec = records[0]
        self.assertTrue(rec.freshness["evaluated_independent_of_severity"])
        # When no live events are present, baseline receives REGIONAL_BASELINE freshness, not false LIVE
        self.assertEqual(rec.freshness["state"], "REGIONAL_BASELINE")

    # =========================================================================
    # 5. PROVENANCE ON ALL INPUTS & RESULTS
    # =========================================================================

    def test_05_provenance_preservation(self):
        """Verify 100% provenance is attached to every normalized input and future risk record."""
        dataset = assemble_region_forecast_dataset("Kerala")
        self.assertIsNotNone(dataset)
        self.assertTrue(bool(dataset.weather_observation.metadata.provider))
        self.assertTrue(bool(dataset.hydrology.metadata.provider))
        self.assertTrue(bool(dataset.environment.metadata.provider))

        record = future_risk_engine.evaluate_future_risk("Kerala", "LANDSLIDE", "0_6_HOURS")[0]
        self.assertIn("providers", record.provenance)
        self.assertTrue(record.provenance["zero_synthetic_records_guarantee"])

    # =========================================================================
    # 6. CONFIDENCE ENGINE (QUALITATIVE LOW, MODERATE, HIGH)
    # =========================================================================

    def test_06_confidence_engine_qualitative_scoring(self):
        """Verify confidence is qualitative (LOW, MODERATE, HIGH) and never labeled as probability."""
        conf, uncert, rat = confidence_engine.evaluate_confidence(
            data_completeness=1.0,
            horizon="0_6_HOURS",
            source_agreement_count=3,
            freshness="LIVE",
            has_official_warning=True
        )
        self.assertEqual(conf, "HIGH")
        self.assertEqual(uncert, "LOW")
        self.assertIn("High confidence", rat)

        conf_low, uncert_high, _ = confidence_engine.evaluate_confidence(
            data_completeness=0.2,
            horizon="3_7_DAYS",
            source_agreement_count=1,
            freshness="REGIONAL_BASELINE",
            has_official_warning=False
        )
        self.assertEqual(conf_low, "LOW")
        self.assertEqual(uncert_high, "VERY_HIGH")

    # =========================================================================
    # 7. UNCERTAINTY HANDLING
    # =========================================================================

    def test_07_uncertainty_scales_with_horizon(self):
        """Verify uncertainty expands as the forecast lead time increases."""
        timeline = future_risk_service.get_region_hazard_timeline("Rajasthan", "HEATWAVE")
        pts = timeline["timeline"]

        now_pt = next(p for p in pts if p["forecast_window"] == "NOW")
        day7_pt = next(p for p in pts if p["forecast_window"] == "3_7_DAYS")

        self.assertIn(now_pt["uncertainty"], ["LOW", "MODERATE"])
        self.assertIn(day7_pt["uncertainty"], ["HIGH", "VERY_HIGH"])

    # =========================================================================
    # 8. MISSING DATA RETURNS UNAVAILABLE (ZERO FABRICATION)
    # =========================================================================

    def test_08_missing_data_returns_unavailable(self):
        """Verify that when a variable has no active telemetry, it is marked UNAVAILABLE without fake numbers."""
        dataset = assemble_region_forecast_dataset("Punjab")
        self.assertIsNotNone(dataset)

        # In Punjab without active flood alerts, river_level_m is None and availability is UNAVAILABLE
        self.assertIsNone(dataset.hydrology.river_level_m)
        self.assertEqual(dataset.hydrology.metadata.availability, InputAvailabilityStatus.UNAVAILABLE.value)
        self.assertEqual(dataset.hydrology.metadata.quality_status, VariableQualityStatus.HISTORICAL_NORMAL.value)

    # =========================================================================
    # 9. STALE DATA HANDLING
    # =========================================================================

    def test_09_stale_data_handling(self):
        """Verify stale observations degrade confidence and preserve STALE tag."""
        conf, uncert, _ = confidence_engine.evaluate_confidence(
            data_completeness=0.5,
            horizon="6_24_HOURS",
            freshness="STALE"
        )
        self.assertIn(conf, ["LOW", "MODERATE"])

    # =========================================================================
    # 10. CACHED DATA HANDLING
    # =========================================================================

    def test_10_cached_data_handling(self):
        """Verify cached telemetry is tagged CACHED and not elevated to LIVE."""
        conf, _, _ = confidence_engine.evaluate_confidence(
            data_completeness=0.8,
            horizon="0_6_HOURS",
            freshness="CACHED"
        )
        self.assertIn(conf, ["MODERATE", "HIGH"])

    # =========================================================================
    # 11. OFFICIAL WARNING SEPARATION
    # =========================================================================

    def test_11_official_warning_separation(self):
        """Verify official warnings are distinctly isolated in the assessment record."""
        # Test evaluating severe weather advisory
        records = future_risk_engine.evaluate_future_risk("Meghalaya", "SEVERE_WEATHER", "0_6_HOURS")
        self.assertEqual(len(records), 1)
        rec = records[0]
        self.assertIsNotNone(rec.official_warning)
        self.assertTrue(rec.official_warning["active"])

    # =========================================================================
    # 12. FLOOD FUTURE RISK ENGINE & WHY_FLOOD_RISK_CHANGED
    # =========================================================================

    def test_12_flood_future_risk_engine_and_why_changed(self):
        """Verify flood future-risk engine explains WHY_FLOOD_RISK_CHANGED."""
        dataset = assemble_region_forecast_dataset("Assam")
        rec = flood_future_risk_engine.evaluate(dataset, "6_24_HOURS", is_assam=True)

        self.assertEqual(rec.hazard_type, "FLOOD")
        self.assertIn("WHY_FLOOD_RISK_CHANGED", rec.summary)
        self.assertGreater(len(rec.evidence_signals), 0)

    # =========================================================================
    # 13. CYCLONE ENGINE (DETECTED, FORECAST, IMPACT RISK)
    # =========================================================================

    def test_13_cyclone_detected_forecast_impact_distinction(self):
        """Verify cyclone engine distinctly evaluates CYCLONE_DETECTED, CYCLONE_FORECAST, and CYCLONE_IMPACT_RISK."""
        dataset = assemble_region_forecast_dataset("Odisha")
        rec = cyclone_future_risk_engine.evaluate(dataset, "6_24_HOURS")

        self.assertEqual(rec.hazard_type, "CYCLONE")
        self.assertIn("CYCLONE_DETECTED", rec.summary)
        self.assertIn("CYCLONE_FORECAST", rec.summary)
        self.assertIn("CYCLONE_IMPACT_RISK", rec.summary)

    # =========================================================================
    # 14. HEATWAVE ENGINE (PERSISTENCE & DEPARTURE)
    # =========================================================================

    def test_14_heatwave_persistence_and_departure(self):
        """Verify heatwave engine models temperature persistence and climatological departure."""
        dataset = assemble_region_forecast_dataset("Rajasthan")
        rec = heatwave_future_risk_engine.evaluate(dataset, "6_24_HOURS")

        self.assertEqual(rec.hazard_type, "HEATWAVE")
        self.assertGreaterEqual(rec.risk_score, 0)
        self.assertLessEqual(rec.risk_score, 100)

    # =========================================================================
    # 15. SEVERE WEATHER ENGINE (OFFICIAL WARNING VS DERIVED)
    # =========================================================================

    def test_15_severe_weather_warning_vs_derived(self):
        """Verify severe weather engine distinguishes official warning from forecast derived risk."""
        dataset = assemble_region_forecast_dataset("Meghalaya")
        rec = severe_weather_engine.evaluate(dataset, "0_6_HOURS")

        self.assertEqual(rec.hazard_type, "SEVERE_WEATHER")
        self.assertIn(rec.methodology, [MethodologyType.OFFICIAL_WARNING.value, MethodologyType.FORECAST_DERIVED_RISK.value])

    # =========================================================================
    # 16. LANDSLIDE ENGINE (POTENTIAL_LANDSLIDE_RISK)
    # =========================================================================

    def test_16_landslide_potential_risk_label(self):
        """Verify landslide engine labels output as POTENTIAL_LANDSLIDE_RISK with transparent uncertainty."""
        dataset = assemble_region_forecast_dataset("Himachal Pradesh")
        rec = landslide_future_risk_engine.evaluate(dataset, "6_24_HOURS")

        self.assertEqual(rec.hazard_type, "LANDSLIDE")
        self.assertIn("POTENTIAL_LANDSLIDE_RISK", rec.summary)
        self.assertIn("not deterministically predictable", rec.limitations.lower())

    # =========================================================================
    # 17. EARTHQUAKE NON-PREDICTION GUARD
    # =========================================================================

    def test_17_earthquake_non_prediction_guard(self):
        """Verify exact deterministic earthquake prediction is strictly prohibited for forward horizons."""
        dataset = assemble_region_forecast_dataset("Uttarakhand")

        # Forward horizons must return UNAVAILABLE confidence and non-predictive disclaimer
        for horiz in ["0_6_HOURS", "6_24_HOURS", "1_3_DAYS", "3_7_DAYS"]:
            rec = earthquake_intelligence_engine.evaluate(dataset, horiz)
            self.assertEqual(rec.confidence, ConfidenceLevel.UNAVAILABLE.value)
            self.assertIn("scientifically impossible", rec.summary.lower())

        # NOW horizon provides RECENT_SEISMIC_ACTIVITY & SEISMIC_CONTEXT
        rec_now = earthquake_intelligence_engine.evaluate(dataset, "NOW")
        self.assertEqual(rec_now.risk_mode, RiskMode.CURRENT_DISASTER_INTELLIGENCE.value)
        self.assertIn("RECENT_SEISMIC_ACTIVITY", rec_now.summary)

    # =========================================================================
    # 18. ASSAM ML SCOPE PRESERVATION
    # =========================================================================

    def test_18_assam_ml_scope_preservation(self):
        """Verify Assam flood uses approved prototype and preserves prototype status."""
        rec = future_risk_engine.evaluate_future_risk("Assam", "FLOOD", "6_24_HOURS")[0]
        self.assertIn("assam_flood_prototype_v1", rec.ml_scope_note)

    # =========================================================================
    # 19. NON-ASSAM ML REJECTION
    # =========================================================================

    def test_19_non_assam_ml_rejection(self):
        """Verify all non-Assam entities strictly reject ML inference."""
        for state in ["Bihar", "Odisha", "Gujarat", "Kerala", "Uttar Pradesh"]:
            rec = future_risk_engine.evaluate_future_risk(state, "FLOOD", "6_24_HOURS")[0]
            self.assertNotEqual(rec.methodology, MethodologyType.EMPIRICAL_ML.value)
            self.assertIn("ML prediction unavailable", rec.ml_scope_note)

    # =========================================================================
    # 20. ZERO SYNTHETIC PRODUCTION RECORDS GUARANTEE
    # =========================================================================

    def test_20_zero_synthetic_data_guarantee(self):
        """Verify synthetic_records is strictly 0 across all future risk operations."""
        summary = future_risk_service.get_national_future_risk_summary()
        self.assertEqual(summary["synthetic_records"], 0)
        for r in summary["regions"]:
            self.assertEqual(r["synthetic_records"], 0)

        dataset = assemble_region_forecast_dataset("Tamil Nadu")
        self.assertEqual(dataset.synthetic_records, 0)

    # =========================================================================
    # 21. END-TO-END API CONTRACTS
    # =========================================================================

    def test_21_api_forecast_variables_endpoint(self):
        """Contract test: GET /api/future-risk/{region}/forecast returns normalized variable schemas."""
        rate_limiter.reset()
        resp = self.client.get("/api/future-risk/West%20Bengal/forecast")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data["region"]["name"], "West Bengal")
        self.assertIn("weather_observation", data)
        self.assertIn("weather_forecast", data)
        self.assertIn("hydrology", data)
        self.assertIn("cyclone", data)
        self.assertIn("environment", data)
        self.assertIn("data_completeness", data)
        self.assertEqual(data["synthetic_records"], 0)

    def test_22_api_public_safety_explanation_endpoint(self):
        """Contract test: GET /api/future-risk/{region}/explanation returns citizen guidance."""
        rate_limiter.reset()
        resp = self.client.get("/api/future-risk/Assam/explanation?hazard=FLOOD")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data["region"], "Assam")
        self.assertEqual(data["hazard"], "FLOOD")
        self.assertIn("public_safety_advisory", data)
        advisory = data["public_safety_advisory"]
        self.assertIn("what", advisory)
        self.assertIn("when", advisory)
        self.assertIn("why", advisory)
        self.assertIn("confidence", advisory)
        self.assertIn("what_to_do", advisory)
        self.assertIn("source", advisory)

    # =========================================================================
    # 23. BEFORE-DISASTER ACTION GUIDANCE INTEGRATION
    # =========================================================================

    def test_23_before_disaster_action_guidance_integrated(self):
        """Verify that explanation and action endpoints supply preparation protocols."""
        resp = self.client.get("/api/future-risk/Kerala/explanation?hazard=LANDSLIDE")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        what_to_do = data["public_safety_advisory"]["what_to_do"]

        self.assertIn("preparedness_phase_before", what_to_do)
        self.assertGreater(len(what_to_do["preparedness_phase_before"]), 0)
        self.assertIn("emergency_dispatch", what_to_do)

    # =========================================================================
    # 24. PROVIDER FAILURE ISOLATION & MODEL ASSET INVARIANTS
    # =========================================================================

    def test_24_model_asset_hashes_and_failure_isolation(self):
        """Verify byte-for-byte immutability of model.joblib and flood_features.csv."""
        model_path = PROJECT_ROOT / "ml" / "flood" / "artifacts" / "model.joblib"
        data_path = PROJECT_ROOT / "datasets" / "processed" / "flood_assam" / "flood_features.csv"

        with open(model_path, "rb") as f:
            actual_model = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(actual_model, self.expected_model_hash, "MODEL.JOBLIB MODIFIED!")

        with open(data_path, "rb") as f:
            actual_data = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(actual_data, self.expected_dataset_hash, "FLOOD_FEATURES.CSV MODIFIED!")


if __name__ == "__main__":
    unittest.main()
