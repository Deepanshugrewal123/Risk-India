/**
 * RISK // INDIA — Crisis Subsystem Types (Phase 30E)
 * ===================================================
 * Types for National Crisis Mode, Emergency Response & Human Action Intelligence.
 */

export type CrisisOperationalState = 'NORMAL' | 'WATCH' | 'ELEVATED' | 'CRISIS';

export type ActionPhase = 'BEFORE' | 'DURING' | 'AFTER';

export type ActionPriority =
  | 'LIFE_SAFETY'
  | 'EVACUATION'
  | 'AVOID_DANGER'
  | 'COMMUNICATION'
  | 'EMERGENCY_RESOURCES'
  | 'PREPARATION';

export type TimelineSignalType =
  | 'OBSERVED'
  | 'OFFICIAL_WARNING'
  | 'FORECAST'
  | 'FORECAST_DERIVED_RISK'
  | 'BASELINE'
  | 'EMPIRICAL_ML';

export interface CrisisActionItem {
  id: string;
  priority: ActionPriority;
  phase: ActionPhase;
  order_rank: number;
  title: string;
  instruction: string;
  rationale: string;
  target_hazard: string;
  is_urgent: boolean;
}

export interface CrisisTimelinePoint {
  horizon: string;
  window_label: string;
  expected_risk_level: string;
  expected_risk_score: number;
  confidence: number;
  primary_hazard: string;
  signal_type: TimelineSignalType;
  key_factors: string[];
  provenance: string;
}

export interface CrisisExplanation {
  why: string;
  what_changed: string;
  supporting_evidence: string[];
  what_could_change: string;
  data_limitations: string;
}

export interface CrisisResourceItem {
  id: string;
  name: string;
  resource_type: string;
  category: string;
  phone?: string;
  contact_number?: string;
  website_url?: string;
  address?: string;
  state: string;
  district?: string;
  disaster_type: string;
  verification_status: string;
  distance_km?: number;
  services: string[];
  source: string;
  provenance: string;
}

export interface FamilyChecklistItem {
  category: string;
  item: string;
  description: string;
  is_critical: boolean;
}

export interface OfficialWarningItem {
  id: string;
  severity: string;
  headline: string;
  description: string;
  source: string;
  valid_until: string;
  color: string;
}

export interface CrisisAssessment {
  region_id: string;
  region_name: string;
  operational_state: CrisisOperationalState;
  is_crisis_recommended: boolean;
  activation_reason: string;
  matched_rules: string[];
  is_manual_activation: boolean;
  primary_hazard: string;
  current_risk_level: string;
  current_risk_score: number;
  peak_future_risk_level: string;
  peak_future_window: string;
  what_is_happening: string;
  what_could_happen_next: string;
  what_to_do_now: CrisisActionItem[];
  action_protocols: {
    BEFORE?: CrisisActionItem[];
    DURING?: CrisisActionItem[];
    AFTER?: CrisisActionItem[];
  };
  family_prep_checklist: FamilyChecklistItem[];
  official_warnings: OfficialWarningItem[];
  emergency_resources: CrisisResourceItem[];
  resource_availability_note?: string;
  timeline: CrisisTimelinePoint[];
  explanation: CrisisExplanation;
  telemetry_summary: Record<string, any>;
  ml_audit: Record<string, any>;
  evaluated_at: string;
  synthetic_records: number;
}

export interface CrisisRegionSummary {
  region_id: string;
  region_name: string;
  state_type: string;
  operational_state: CrisisOperationalState;
  is_crisis_recommended: boolean;
  activation_reason: string;
  primary_hazard: string;
  current_risk_level: string;
  current_risk_score: number;
  official_warnings_count: number;
  matched_rules: string[];
}

export interface NationalCrisisOverview {
  title: string;
  evaluated_at: string;
  total_entities_monitored: number;
  states_covered: number;
  union_territories_covered: number;
  operational_state_distribution: Record<string, number>;
  crisis_recommended_count: number;
  crisis_recommended_regions: CrisisRegionSummary[];
  synthetic_records: number;
  regions: CrisisRegionSummary[];
}
