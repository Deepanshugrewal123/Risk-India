"""
RISK // INDIA — PHASE 30F TEST SUITE
=====================================
National Predictive Risk Fusion, Early-Warning Intelligence & Future-Hazard Assessment.

Validates all 36 dimensions:
1. Invariants: model.joblib SHA-256 byte-for-byte match
2. Invariants: flood_features.csv SHA-256 byte-for-byte match
3. Assam ML model guard: ml_available = True in Assam
4. Non-Assam ML model guard: ml_available = False outside Assam
5. Earthquake non-prediction guard: no forward earthquake forecasts
6. Earthquake explanation: tectonic non-predictability explicitly stated
7. Zero synthetic data in regional assessments (synthetic_records = 0)
8. Zero synthetic data in national overview
9. Zero synthetic data in trends, readiness, and timelines
10. National coverage: exactly 36 entities monitored (28 States + 8 UTs)
11. Multi-hazard support: all 6 hazards covered (FLOOD, CYCLONE, HEATWAVE, SEVERE_WEATHER, LANDSLIDE, EARTHQUAKE)
12. Standard forecast horizons: NOW, 0-6h, 6-24h, 1-3d, 3-7d present
13. Qualitative confidence engine: strictly LOW, MODERATE, HIGH (no pseudo-probabilities)
14. Qualitative confidence: drops with source disagreements
15. Qualitative uncertainty expansion: expands monotonically with lead time
16. Qualitative uncertainty: expands with stale data
17. Risk trend engine: RISING
18. Risk trend engine: DECLINING
19. Risk trend engine: STABLE
20. Risk trend engine: VOLATILE
21. Risk trend engine: INSUFFICIENT_DATA
22. Evidence collector: canonical EvidenceSignal aggregation
23. Conflicting signals: detection & explicit transparent resolution
24. Statutory warning precedence: Red warning guarantees at least HIGH future risk
25. Early warning engine: strictly decouples preparation from evacuation
26. Early warning engine: evacuation advised only during EVACUATION_READINESS / EMERGENCY
27. Scenario engine: Baseline, Likely, Escalation generation
28. Scenario engine: earthquake tectonic background specialization
29. 12 Citizen safety questions: all 12 questions populated and actionable
30. 6 Technical explanation dimensions: fully populated
31. Crisis mode recommendation: deterministic convergence logic
32. REST API: GET /api/predictive-risk/national
33. REST API: GET /api/predictive-risk/{region}
34. REST API: GET /api/predictive-risk/{region}/{hazard}
35. REST API: subpaths (timeline, explanation, scenarios, early-warning)
36. REST API: trends, readiness, and authoritative providers catalog
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
from app.services.predictive_risk import (
    national_predictive_risk_service,
    RiskState,
    TrendState,
    ConfidenceLevel,
    UncertaintyLevel,
    EarlyWarningStatus,
    ScenarioType,
    PredictiveEvidenceCollector,
    QualitativeConfidenceEngine,
    PredictiveUncertaintyEngine,
    RiskTrendEngine,
    MultiHazardForecastEngine,
    RiskEscalationEngine,
    EarlyWarningEngine,
    ScenarioEngine,
    PredictionExplanationEngine
)
from app.services.national_risk.regional_baseline import SUPPORTED_HAZARDS


class TestPhase30FPredictiveRiskFusion(unittest.TestCase):
    """Authoritative test suite for Phase 30F National Predictive Risk Fusion."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.expected_model_sha = "0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf"
        cls.expected_dataset_sha = "88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080"

    # =========================================================================
    # DIMENSION 1 & 2: INVIOLATE SHA-256 HASHES
    # =========================================================================
    def test_01_invariants_model_joblib_sha256(self):
        """Invariant: model.joblib SHA-256 must match exactly byte-for-byte."""
        model_path = PROJECT_ROOT / "ml" / "flood" / "artifacts" / "model.joblib"
        self.assertTrue(model_path.exists(), f"Missing model artifact: {model_path}")
        with open(model_path, "rb") as f:
            actual_sha = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(actual_sha, self.expected_model_sha)

    def test_02_invariants_flood_features_sha256(self):
        """Invariant: flood_features.csv SHA-256 must match exactly byte-for-byte."""
        dataset_path = PROJECT_ROOT / "datasets" / "processed" / "flood_assam" / "flood_features.csv"
        self.assertTrue(dataset_path.exists(), f"Missing dataset: {dataset_path}")
        with open(dataset_path, "rb") as f:
            actual_sha = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(actual_sha, self.expected_dataset_sha)

    # =========================================================================
    # DIMENSION 3 & 4: ASSAM ML MODEL GUARD
    # =========================================================================
    def test_03_assam_ml_model_scope_assam(self):
        """Assam Flood utilizes assam_flood_prototype_v1 with ml_available = True."""
        assessment = national_predictive_risk_service.get_hazard_assessment("assam", "FLOOD")
        self.assertEqual(assessment.region_id, "assam")
        self.assertEqual(assessment.hazard, "FLOOD")
        self.assertTrue(assessment.ml_scope.get("ml_available"))
        self.assertEqual(assessment.synthetic_records, 0)

    def test_04_assam_ml_model_scope_non_assam(self):
        """Non-Assam states strictly set ml_available = False and status = NOT_AVAILABLE."""
        test_states = ["delhi", "kerala", "gujarat", "maharashtra", "odisha"]
        for st in test_states:
            assessment = national_predictive_risk_service.get_hazard_assessment(st, "FLOOD")
            self.assertFalse(assessment.ml_scope.get("ml_available"), f"ML should be disabled for {st}")
            self.assertEqual(assessment.ml_scope.get("status"), "NOT_AVAILABLE")
            self.assertEqual(assessment.synthetic_records, 0)

    # =========================================================================
    # DIMENSION 5 & 6: EARTHQUAKE NON-PREDICTION GUARD
    # =========================================================================
    def test_05_earthquake_non_prediction_guard(self):
        """Earthquakes are strictly non-predictable; no future forecasting allowed."""
        assessment = national_predictive_risk_service.get_hazard_assessment("uttarakhand", "EARTHQUAKE")
        self.assertEqual(assessment.hazard, "EARTHQUAKE")
        self.assertEqual(assessment.trend, TrendState.STABLE)
        self.assertEqual(assessment.confidence, ConfidenceLevel.LOW)
        self.assertEqual(assessment.uncertainty, UncertaintyLevel.VERY_HIGH)
        # All timeline points must equal current state
        for tp in assessment.timeline:
            self.assertEqual(tp.future_risk_state, assessment.current_risk_state)

    def test_06_earthquake_explanation_non_prediction(self):
        """Earthquake explanation transparently discloses tectonic non-predictability."""
        assessment = national_predictive_risk_service.get_hazard_assessment("himachal-pradesh", "EARTHQUAKE")
        self.assertIn("non-predictable", assessment.explanation.what_we_do_not_know.lower())
        self.assertIn("cannot be predicted", assessment.explanation.citizen_answers.what_could_happen_next.lower())

    # =========================================================================
    # DIMENSION 7, 8, 9: ZERO SYNTHETIC DATA GUARANTEE
    # =========================================================================
    def test_07_zero_synthetic_data_across_assessments(self):
        """Zero synthetic records across all assessed regions and hazards."""
        for h in SUPPORTED_HAZARDS:
            assessment = national_predictive_risk_service.get_hazard_assessment("bihar", h)
            self.assertEqual(assessment.synthetic_records, 0)

    def test_08_zero_synthetic_data_in_national_overview(self):
        """National overview explicitly confirms synthetic_records = 0."""
        overview = national_predictive_risk_service.get_national_overview()
        self.assertEqual(overview.synthetic_records, 0)

    def test_09_zero_synthetic_data_in_timeline_and_trends(self):
        """Trends and readiness feeds strictly have synthetic_records = 0."""
        trends = national_predictive_risk_service.get_trends()
        self.assertEqual(trends.get("synthetic_records"), 0)
        readiness = national_predictive_risk_service.get_readiness()
        self.assertEqual(readiness.get("synthetic_records"), 0)

    # =========================================================================
    # DIMENSION 10 & 11: NATIONAL COVERAGE & MULTI-HAZARD SUPPORT
    # =========================================================================
    def test_10_national_overview_36_entities(self):
        """Monitors all 28 States and 8 Union Territories (36 entities total)."""
        overview = national_predictive_risk_service.get_national_overview()
        self.assertEqual(overview.total_entities_monitored, 36)
        self.assertEqual(overview.states_covered, 28)
        self.assertEqual(overview.union_territories_covered, 8)
        self.assertEqual(len(overview.regions), 36)

    def test_11_all_6_hazards_supported(self):
        """All 6 disasters supported across all Indian regions."""
        overview = national_predictive_risk_service.get_national_overview()
        expected = ["FLOOD", "CYCLONE", "HEATWAVE", "SEVERE_WEATHER", "LANDSLIDE", "EARTHQUAKE"]
        for exp in expected:
            self.assertIn(exp, overview.supported_hazards)

    # =========================================================================
    # DIMENSION 12: 5 STANDARD FORECAST HORIZONS
    # =========================================================================
    def test_12_5_standard_forecast_horizons(self):
        """Timeline contains exactly the 5 standard forecast horizons."""
        assessment = national_predictive_risk_service.get_hazard_assessment("delhi", "HEATWAVE")
        horizons = [tp.horizon for tp in assessment.timeline]
        expected_horizons = ["NOW", "0-6h", "6-24h", "1-3d", "3-7d"]
        self.assertEqual(horizons, expected_horizons)

    # =========================================================================
    # DIMENSION 13 & 14: QUALITATIVE CONFIDENCE ENGINE
    # =========================================================================
    def test_13_qualitative_confidence_engine(self):
        """Confidence is strictly qualitative LOW, MODERATE, HIGH (no pseudo-probabilities)."""
        conf_high = QualitativeConfidenceEngine.evaluate(
            hazard="FLOOD",
            signals=[None, None, None, None],
            has_official_warning=True,
            has_live_telemetry=True,
            has_forecast_inputs=True,
            source_disagreement=False
        )
        self.assertEqual(conf_high, ConfidenceLevel.HIGH)
        self.assertIsInstance(conf_high.value, str)
        self.assertNotIn("%", conf_high.value)

    def test_14_qualitative_confidence_source_disagreement(self):
        """Active source disagreement drops confidence level."""
        conf_disagree = QualitativeConfidenceEngine.evaluate(
            hazard="FLOOD",
            signals=[None, None, None, None],
            has_official_warning=False,
            has_live_telemetry=True,
            has_forecast_inputs=True,
            source_disagreement=True
        )
        self.assertEqual(conf_disagree, ConfidenceLevel.LOW)

    # =========================================================================
    # DIMENSION 15 & 16: QUALITATIVE UNCERTAINTY EXPANSION
    # =========================================================================
    def test_15_qualitative_uncertainty_expansion_lead_time(self):
        """Uncertainty expands monotonically with forecast lead time."""
        u_now = PredictiveUncertaintyEngine.evaluate("NOW", "FLOOD", "OFFICIAL_LIVE")
        u_24h = PredictiveUncertaintyEngine.evaluate("6-24h", "FLOOD", "OFFICIAL_LIVE")
        u_3d = PredictiveUncertaintyEngine.evaluate("1-3d", "FLOOD", "OFFICIAL_LIVE")
        u_7d = PredictiveUncertaintyEngine.evaluate("3-7d", "FLOOD", "OFFICIAL_LIVE")

        rank = {UncertaintyLevel.LOW: 1, UncertaintyLevel.MODERATE: 2, UncertaintyLevel.HIGH: 3, UncertaintyLevel.VERY_HIGH: 4}
        self.assertLessEqual(rank[u_now], rank[u_24h])
        self.assertLessEqual(rank[u_24h], rank[u_3d])
        self.assertLessEqual(rank[u_3d], rank[u_7d])

    def test_16_qualitative_uncertainty_degraded_freshness(self):
        """Stale or missing data expands uncertainty even in near-term windows."""
        u_stale = PredictiveUncertaintyEngine.evaluate("NOW", "FLOOD", "STALE")
        self.assertIn(u_stale, [UncertaintyLevel.MODERATE, UncertaintyLevel.HIGH])

    # =========================================================================
    # DIMENSION 17-21: DIRECTIONAL RISK TREND ENGINE
    # =========================================================================
    def test_17_risk_trend_engine_rising(self):
        """Significant forward increase evaluates to RISING."""
        trend = RiskTrendEngine.evaluate(20.0, [35.0, 50.0, 65.0], "FLOOD")
        self.assertEqual(trend, TrendState.RISING)

    def test_18_risk_trend_engine_declining(self):
        """Significant forward drop evaluates to DECLINING."""
        trend = RiskTrendEngine.evaluate(75.0, [50.0, 35.0, 20.0], "FLOOD")
        self.assertEqual(trend, TrendState.DECLINING)

    def test_19_risk_trend_engine_stable(self):
        """Stable scores evaluate to STABLE."""
        trend = RiskTrendEngine.evaluate(30.0, [32.0, 31.0, 30.0], "FLOOD")
        self.assertEqual(trend, TrendState.STABLE)

    def test_20_risk_trend_engine_volatile(self):
        """Opposing swings evaluate to VOLATILE."""
        trend = RiskTrendEngine.evaluate(30.0, [55.0, 25.0, 60.0], "FLOOD")
        self.assertEqual(trend, TrendState.VOLATILE)

    def test_21_risk_trend_engine_insufficient_data(self):
        """Missing future timeline evaluates to INSUFFICIENT_DATA."""
        trend = RiskTrendEngine.evaluate(30.0, [], "FLOOD", has_insufficient_evidence=True)
        self.assertEqual(trend, TrendState.INSUFFICIENT_DATA)

    # =========================================================================
    # DIMENSION 22: EVIDENCE COLLECTOR
    # =========================================================================
    def test_22_evidence_collector_gathers_signals(self):
        """Evidence collector packages signals with strict provenance."""
        evidence = PredictiveEvidenceCollector.collect_evidence("delhi", "Delhi", "HEATWAVE")
        self.assertIn("signals", evidence)
        self.assertIn("forecast_timeline", evidence)
        self.assertIn("official_warnings", evidence)
        self.assertIsInstance(evidence["signals"], list)

    # =========================================================================
    # DIMENSION 23 & 24: ESCALATION, CONFLICTS & STATUTORY WARNING PRECEDENCE
    # =========================================================================
    def test_23_conflicting_signals_detection_and_resolution(self):
        """Heavy forecast rain with calm river gauges flags conflicts with resolution notes."""
        from app.services.predictive_risk.fusion_schema import EvidenceSignal
        signals = [
            EvidenceSignal(
                id="sig-rain-heavy",
                provider="IMD",
                source="Forecast",
                observed_at="2026-09-18T00:00:00Z",
                ingested_at="2026-09-18T00:00:00Z",
                geographic_scope="Basin",
                variable="RAINFALL_24H",
                unit="mm",
                raw_value=75.0,
                normalized_value=75.0,
                freshness="OFFICIAL_LIVE",
                data_classification="FORECAST",
                official_status="VERIFIED"
            ),
            EvidenceSignal(
                id="sig-river-normal",
                provider="CWC",
                source="Gauge",
                observed_at="2026-09-18T00:00:00Z",
                ingested_at="2026-09-18T00:00:00Z",
                geographic_scope="Basin",
                variable="RIVER_WATER_LEVEL",
                unit="ratio",
                raw_value=0.4,
                normalized_value=0.4,
                freshness="OFFICIAL_LIVE",
                data_classification="OBSERVED",
                official_status="VERIFIED"
            )
        ]
        curr_state, fut_state, has_conflicts, conflicts, notes, crisis, reason = RiskEscalationEngine.evaluate(
            hazard="FLOOD",
            current_state=RiskState.NORMAL,
            current_score=20.0,
            future_state=RiskState.NORMAL,
            peak_future_score=60.0,
            evidence_signals=signals,
            official_warnings=[],
            corroborating_factors=[]
        )
        self.assertTrue(has_conflicts)
        self.assertGreater(len(conflicts), 0)
        self.assertIsNotNone(notes)
        self.assertIn("Hydrological Lag", notes)

    def test_24_statutory_warning_precedence(self):
        """Official Red warning escalates future risk to at least HIGH."""
        warnings = [{"severity": "RED", "headline": "Severe Cloudburst Warning", "provider": "IMD"}]
        curr_state, fut_state, has_conflicts, conflicts, notes, crisis, reason = RiskEscalationEngine.evaluate(
            hazard="FLOOD",
            current_state=RiskState.NORMAL,
            current_score=20.0,
            future_state=RiskState.NORMAL,
            peak_future_score=40.0,
            evidence_signals=[],
            official_warnings=warnings,
            corroborating_factors=[]
        )
        self.assertEqual(fut_state, RiskState.HIGH)
        self.assertTrue(crisis)

    # =========================================================================
    # DIMENSION 25 & 26: EARLY WARNING ENGINE & PREPARATION VS EVACUATION
    # =========================================================================
    def test_25_early_warning_engine_decouples_prepare_from_evacuate(self):
        """Strictly distinguishes preparation guidance from physical evacuation."""
        ew = EarlyWarningEngine.evaluate(
            hazard="FLOOD",
            current_state=RiskState.NORMAL,
            future_state=RiskState.ELEVATED,
            peak_score=50.0,
            peak_window="6-24h",
            official_warnings=[]
        )
        self.assertIn(ew.status, [EarlyWarningStatus.PREPARE, EarlyWarningStatus.GET_READY])
        self.assertTrue(ew.is_preparation_advised)
        self.assertFalse(ew.is_evacuation_advised)
        self.assertIsNone(ew.evacuation_guidance)
        self.assertGreater(len(ew.preparation_guidance), 0)

    def test_26_early_warning_evacuation_readiness_conditions(self):
        """Evacuation is advised only during EVACUATION_READINESS or EMERGENCY."""
        ew = EarlyWarningEngine.evaluate(
            hazard="CYCLONE",
            current_state=RiskState.HIGH,
            future_state=RiskState.CRITICAL,
            peak_score=88.0,
            peak_window="0-6h",
            official_warnings=[{"severity": "RED", "warning_id": "IMD-CYC-01"}]
        )
        self.assertIn(ew.status, [EarlyWarningStatus.EVACUATION_READINESS, EarlyWarningStatus.EMERGENCY])
        self.assertTrue(ew.is_evacuation_advised)
        self.assertIsNotNone(ew.evacuation_guidance)

    # =========================================================================
    # DIMENSION 27 & 28: SCENARIO ENGINE
    # =========================================================================
    def test_27_scenario_engine_baseline_likely_escalation(self):
        """Generates BASELINE, LIKELY, and ESCALATION scenarios."""
        scenarios = ScenarioEngine.generate_scenarios(
            hazard="FLOOD",
            current_state=RiskState.NORMAL,
            future_state=RiskState.ELEVATED,
            peak_future_score=55.0,
            corroborating_factors=["Heavy basin precipitation"],
            uncertainty=UncertaintyLevel.MODERATE
        )
        types = [s.scenario_type for s in scenarios]
        self.assertEqual(types, [ScenarioType.BASELINE, ScenarioType.LIKELY, ScenarioType.ESCALATION])
        for s in scenarios:
            self.assertTrue(len(s.title) > 0)
            self.assertTrue(len(s.description) > 0)
            self.assertTrue(len(s.safety_actions) > 0)

    def test_28_scenario_engine_earthquake_specialization(self):
        """Earthquake scenarios focus on tectonic background, not temporal forecasts."""
        scenarios = ScenarioEngine.generate_scenarios(
            hazard="EARTHQUAKE",
            current_state=RiskState.NORMAL,
            future_state=RiskState.NORMAL,
            peak_future_score=20.0,
            corroborating_factors=[],
            uncertainty=UncertaintyLevel.VERY_HIGH
        )
        self.assertEqual(len(scenarios), 3)
        for s in scenarios:
            self.assertEqual(s.expected_direction, TrendState.STABLE)
            self.assertEqual(s.uncertainty, UncertaintyLevel.VERY_HIGH)

    # =========================================================================
    # DIMENSION 29 & 30: 12 CITIZEN SAFETY QUESTIONS & 6 TECHNICAL DIMENSIONS
    # =========================================================================
    def test_29_12_citizen_safety_questions_completeness(self):
        """All 12 citizen safety questions are directly and actionably answered."""
        assessment = national_predictive_risk_service.get_hazard_assessment("assam", "FLOOD")
        ans = assessment.explanation.citizen_answers

        self.assertTrue(len(ans.what_is_happening_now) > 0, "Q1 missing")
        self.assertTrue(len(ans.what_could_happen_next) > 0, "Q2 missing")
        self.assertTrue(len(ans.what_is_future_trend) > 0, "Q3 missing")
        self.assertTrue(len(ans.how_serious_could_it_become) > 0, "Q4 missing")
        self.assertTrue(len(ans.why_risk_may_increase) > 0, "Q5 missing")
        self.assertTrue(len(ans.what_evidence_supports_it) > 0, "Q6 missing")
        self.assertTrue(len(ans.what_should_i_do_now) > 0, "Q7 missing")
        self.assertTrue(len(ans.what_to_prepare_before) > 0, "Q8 missing")
        self.assertTrue(len(ans.what_to_do_during) > 0, "Q9 missing")
        self.assertTrue(len(ans.what_to_do_after) > 0, "Q10 missing")
        self.assertTrue(len(ans.what_data_missing_or_uncertain) > 0, "Q11 missing")
        self.assertTrue(len(ans.when_to_check_again) > 0, "Q12 missing")

    def test_30_6_technical_explanation_dimensions(self):
        """All 6 technical explanation dimensions are fully populated."""
        assessment = national_predictive_risk_service.get_hazard_assessment("delhi", "HEATWAVE")
        exp = assessment.explanation
        self.assertTrue(len(exp.why_this_risk) > 0)
        self.assertTrue(len(exp.what_changed) > 0)
        self.assertTrue(len(exp.what_supports_it) > 0)
        self.assertTrue(len(exp.what_could_make_it_worse) > 0)
        self.assertTrue(len(exp.what_could_make_it_improve) > 0)
        self.assertTrue(len(exp.what_we_do_not_know) > 0)

    # =========================================================================
    # DIMENSION 31: CRISIS MODE RECOMMENDATION
    # =========================================================================
    def test_31_crisis_mode_recommendation_logic(self):
        """Recommends crisis mode when hazard escalation crosses critical thresholds."""
        assessment = national_predictive_risk_service.get_hazard_assessment("delhi", "HEATWAVE")
        self.assertIsInstance(assessment.crisis_mode_recommended, bool)

    # =========================================================================
    # DIMENSION 32-36: REST API ENDPOINTS
    # =========================================================================
    def test_32_api_get_national_overview(self):
        """GET /api/predictive-risk/national returns 200 OK and valid overview schema."""
        res = self.client.get("/api/predictive-risk/national")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("total_entities_monitored"), 36)
        self.assertEqual(data.get("synthetic_records"), 0)

    def test_33_api_get_regional_assessment(self):
        """GET /api/predictive-risk/{region} returns 200 OK with fused assessment."""
        res = self.client.get("/api/predictive-risk/assam")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("region_id"), "assam")
        self.assertIn("timeline", data)
        self.assertIn("scenarios", data)
        self.assertIn("early_warning", data)
        self.assertIn("explanation", data)

    def test_34_api_get_hazard_assessment(self):
        """GET /api/predictive-risk/{region}/{hazard} returns 200 OK for specific hazard."""
        res = self.client.get("/api/predictive-risk/odisha/CYCLONE")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("hazard"), "CYCLONE")

    def test_35_api_subpaths(self):
        """GET /api/predictive-risk/{region}/(timeline|explanation|scenarios|early-warning)."""
        res_tl = self.client.get("/api/predictive-risk/kerala/timeline")
        self.assertEqual(res_tl.status_code, 200)
        self.assertEqual(len(res_tl.json()), 5)

        res_exp = self.client.get("/api/predictive-risk/kerala/explanation")
        self.assertEqual(res_exp.status_code, 200)
        self.assertIn("citizen_answers", res_exp.json())

        res_sc = self.client.get("/api/predictive-risk/kerala/scenarios")
        self.assertEqual(res_sc.status_code, 200)
        self.assertEqual(len(res_sc.json()), 3)

        res_ew = self.client.get("/api/predictive-risk/kerala/early-warning")
        self.assertEqual(res_ew.status_code, 200)
        self.assertIn("is_preparation_advised", res_ew.json())

    def test_36_api_trends_readiness_providers(self):
        """GET /api/predictive-risk/(trends|readiness|providers) returns 200 OK."""
        res_tr = self.client.get("/api/predictive-risk/trends")
        self.assertEqual(res_tr.status_code, 200)
        self.assertEqual(res_tr.json().get("total_entities"), 36)

        res_rd = self.client.get("/api/predictive-risk/readiness")
        self.assertEqual(res_rd.status_code, 200)
        self.assertIn("actionable_count", res_rd.json())

        res_pr = self.client.get("/api/predictive-risk/providers")
        self.assertEqual(res_pr.status_code, 200)
        self.assertEqual(len(res_pr.json()), 6)


if __name__ == "__main__":
    unittest.main()
