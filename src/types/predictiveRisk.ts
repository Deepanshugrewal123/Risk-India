/**
 * RISK // INDIA — National Predictive Risk Fusion Types (Phase 30F)
 * =================================================================
 * Type definitions for multi-source risk fusion, multi-hazard forecasting,
 * 5-horizon predictive timelines, qualitative confidence & uncertainty,
 * forward scenarios, early warning, and 12-question citizen safety answers.
 */

export type RiskState = 'NORMAL' | 'WATCH' | 'ELEVATED' | 'HIGH' | 'CRITICAL';
export type TrendState = 'RISING' | 'STABLE' | 'DECLINING' | 'VOLATILE' | 'INSUFFICIENT_DATA';
export type ConfidenceLevel = 'LOW' | 'MODERATE' | 'HIGH';
export type UncertaintyLevel = 'LOW' | 'MODERATE' | 'HIGH' | 'VERY_HIGH';
export type EarlyWarningStatus =
  | 'NO_ACTIVE_SIGNAL'
  | 'WATCH'
  | 'PREPARE'
  | 'GET_READY'
  | 'EVACUATION_READINESS'
  | 'EMERGENCY';

export type ScenarioType = 'BASELINE' | 'LIKELY' | 'ESCALATION';

export interface EvidenceSignal {
  id: string;
  provider: string;
  source: string;
  source_record_id?: string | null;
  observed_at: string;
  ingested_at: string;
  geographic_scope: string;
  variable: string;
  unit: string;
  raw_value?: number | null;
  normalized_value?: number | null;
  freshness: string;
  data_classification: string;
  official_status: string;
  url?: string | null;
}

export interface PredictiveScenario {
  scenario_type: ScenarioType;
  title: string;
  description: string;
  triggering_evidence: string[];
  expected_direction: TrendState;
  uncertainty: UncertaintyLevel;
  preparedness_implications: string;
  safety_actions: string[];
}

export interface EarlyWarningAssessment {
  status: EarlyWarningStatus;
  lead_time_window: string;
  is_evacuation_advised: boolean;
  is_preparation_advised: boolean;
  preparation_guidance: string[];
  evacuation_guidance?: string | null;
  official_bulletin_reference?: string | null;
}

export interface CitizenSafetyAnswers {
  what_is_happening_now: string;
  what_could_happen_next: string;
  what_is_future_trend: string;
  how_serious_could_it_become: string;
  why_risk_may_increase: string;
  what_evidence_supports_it: string[];
  what_should_i_do_now: string[];
  what_to_prepare_before: string[];
  what_to_do_during: string[];
  what_to_do_after: string[];
  what_data_missing_or_uncertain: string;
  when_to_check_again: string;
}

export interface PredictionExplanation {
  why_this_risk: string;
  what_changed: string;
  what_supports_it: string[];
  what_could_make_it_worse: string;
  what_could_make_it_improve: string;
  what_we_do_not_know: string;
  citizen_answers: CitizenSafetyAnswers;
}

export interface PredictiveTimelinePoint {
  horizon: string;
  time_window_label: string;
  hazard: string;
  current_risk_state: RiskState;
  future_risk_state: RiskState;
  risk_score: number;
  trend: TrendState;
  confidence: ConfidenceLevel;
  uncertainty: UncertaintyLevel;
  freshness: string;
  evidence_summary: string[];
  official_warning?: string | null;
  recommended_action: string;
  data_classification: string;
}

export interface PredictiveRiskAssessment {
  region_id: string;
  region_name: string;
  region_type: string;
  hazard: string;
  current_risk_state: RiskState;
  current_risk_score: number;
  future_risk_state: RiskState;
  peak_future_score: number;
  peak_future_window: string;
  trend: TrendState;
  confidence: ConfidenceLevel;
  uncertainty: UncertaintyLevel;
  overall_freshness: string;
  evidence_signals: EvidenceSignal[];
  official_warnings: Record<string, any>[];
  conflicting_signals: string[];
  has_conflicting_evidence: boolean;
  conflict_resolution_notes?: string | null;
  scenarios: PredictiveScenario[];
  early_warning: EarlyWarningAssessment;
  crisis_mode_recommended: boolean;
  crisis_activation_reason?: string | null;
  timeline: PredictiveTimelinePoint[];
  explanation: PredictionExplanation;
  ml_scope: Record<string, any>;
  synthetic_records: number;
  evaluated_at: string;
}

export interface NationalPredictiveOverview {
  title: string;
  evaluated_at: string;
  total_entities_monitored: number;
  states_covered: number;
  union_territories_covered: number;
  supported_hazards: string[];
  forecast_horizons: string[];
  risk_state_distribution: Record<string, number>;
  trend_distribution: Record<string, number>;
  crisis_recommended_count: number;
  crisis_recommended_entities: Array<{
    region_id: string;
    region_name: string;
    hazard: string;
    future_risk_state: string;
    peak_future_score: number;
    reason?: string;
  }>;
  synthetic_records: number;
  regions: Array<{
    region_id: string;
    region_name: string;
    region_type: string;
    hazard: string;
    current_risk_state: string;
    current_risk_score: number;
    future_risk_state: string;
    peak_future_score: number;
    peak_future_window: string;
    trend: string;
    confidence: string;
    uncertainty: string;
    early_warning_status: string;
    crisis_mode_recommended: boolean;
    has_conflicting_evidence: boolean;
    freshness: string;
  }>;
}

export interface AuthoritativeProviderInfo {
  provider: string;
  full_name: string;
  role: string;
  status: string;
  data_types: string[];
}
