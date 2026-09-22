/**
 * RISK // INDIA — Extended Citizen Disaster Safety Guidance Types
 * ================================================================
 * Authoritative TypeScript definitions for structured Before/During/After life-safety protocols.
 */

export type SafetyPhase = 'BEFORE' | 'DURING' | 'AFTER';

export type SafetyPriority = 'CRITICAL' | 'HIGH' | 'RECOMMENDED';

export type SafetyCategory =
  | 'EMERGENCY_CONTACTS'
  | 'FAMILY_COMMUNICATION'
  | 'EMERGENCY_KIT'
  | 'WATER_AND_FOOD'
  | 'MEDICAL_AND_HEALTH'
  | 'CRITICAL_DOCUMENTS'
  | 'POWER_AND_LIGHTING'
  | 'SAFE_ROUTES_EVACUATION'
  | 'VULNERABLE_MEMBERS'
  | 'PETS_AND_LIVESTOCK'
  | 'PROPERTY_PREPARATION'
  | 'UTILITY_SAFETY'
  | 'AVOIDANCE_WHAT_NOT_TO_DO'
  | 'RECOVERY_AND_HEALTH'
  | 'DAMAGE_DOCUMENTATION'
  | 'SHELTER'
  | 'TRANSPORTATION'
  | 'SANITATION'
  | 'STRUCTURAL_SAFETY';

export interface SafetyInstructionItem {
  id: string;
  hazard: string;
  phase: SafetyPhase;
  category: SafetyCategory;
  title: string;
  instruction: string;
  priority: SafetyPriority;
  reason: string;
  source: string;
  warning?: string | null;
  related_cascading_risk?: string | null;
  // Progressive disclosure detailed guidance:
  practical_steps?: string[];
  warning_signs?: string[];
  what_not_to_do?: string[];
  vulnerable_groups?: string;
  checklist?: string[];
}

export interface PhaseGroup {
  phase_title: string;
  item_count: number;
  items: SafetyInstructionItem[];
}

export interface HazardSafetyGuide {
  hazard: string;
  statutory_notice: string;
  emergency_contacts: {
    national_emergency: string;
    ndma_disaster_helpline: string;
    state_emergency_operation_center: string;
    ambulance: string;
    [key: string]: string;
  };
  total_action_items: number;
  categories_covered: string[];
  phases: {
    BEFORE: PhaseGroup;
    DURING: PhaseGroup;
    AFTER: PhaseGroup;
  };
  region?: {
    id: string;
    name: string;
    type: string;
    primary_hazard: string;
    secondary_hazard: string;
  };
  synthetic_records: number;
}
