/**
 * RISK // INDIA — Cascading / Secondary / Systemic Risk Intelligence Types
 * =========================================================================
 * Authoritative TypeScript definitions for consequence chains, evidence postures,
 * and scientific classification guards.
 */

export type EvidencePosture =
  | 'LIVE_EVIDENCE'         // Active telemetry confirms contributing condition
  | 'RECENT_EVIDENCE'       // Recent observation confirms contributing condition
  | 'FORECAST_AVAILABLE'   // Official numerical forecast model indicates threshold
  | 'BASELINE_ONLY'         // Established physical relationship/baseline only; no active trigger
  | 'LIMITED_EVIDENCE'     // Sparse telemetry in basin / region
  | 'DATA_UNAVAILABLE';     // Uninstrumented or offline telemetry

export type RelationshipClassification =
  | 'ESTABLISHED_PHYSICAL_RELATIONSHIP'
  | 'LOCAL_OBSERVED_EVIDENCE'
  | 'CONDITIONAL_SECONDARY_RISK'
  | 'PREDICTIVE_FORECAST';

export interface CascadingStage {
  stage_order: number;
  stage_type: 'PRIMARY_HAZARD' | 'PHYSICAL_CHANGE' | 'SECONDARY_HAZARD' | 'TERTIARY_CONSEQUENCE';
  title: string;
  description: string;
  scientific_classification: RelationshipClassification;
  evidence_posture: EvidencePosture;
  supporting_evidence: string[];
  conditions_for_escalation: string[];
  unmonitored_or_unknown: string[];
  field_warning_signs: string[];
  defensive_actions: string[];
}

export interface CascadingRiskChain {
  hazard: string;
  title: string;
  primary_hazard_summary: string;
  environmental_change_summary: string;
  secondary_hazard_summary: string;
  tertiary_consequences_summary: string;
  overall_evidence_posture: EvidencePosture;
  stages: CascadingStage[];
  scientific_rationale: string;
  earthquake_non_prediction_notice?: string | null;
  terrain_sensitivity_note?: string | null;
  synthetic_records: number;
}

export interface CascadingRiskAssessment {
  region: {
    id: string;
    name: string;
    type: string;
  };
  primary_hazard: string;
  evaluated_at: string;
  evidence_posture: EvidencePosture;
  chains: CascadingRiskChain[];
  context_indicators: {
    terrain_slope_vulnerability?: string;
    basin_condition?: string;
    river_level_trend?: string;
    accumulated_rainfall_72h_mm?: number | null;
    coastal_exposure?: string;
    active_cyclone_systems?: number;
    forecast_rainfall_mm?: number | null;
    is_hilly_or_mountainous?: boolean;
    [key: string]: any;
  };
  synthetic_records: number;
}
