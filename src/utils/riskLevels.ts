import { RiskLevel } from '../types/risk';

export interface RiskLevelConfig {
  level: RiskLevel;
  label: string;
  minScore: number;
  maxScore: number;
  hexColor: string;
  badgeBg: string;
  badgeText: string;
  badgeBorder: string;
  badgeClass: string;
  dotClass: string;
  ringClass: string;
  borderClass: string;
  description: string;
}

export const RISK_LEVEL_CONFIG: Record<RiskLevel, RiskLevelConfig> = {
  LOW: {
    level: 'LOW',
    label: 'Low',
    minScore: 0,
    maxScore: 44,
    hexColor: '#10B981',
    badgeBg: 'bg-emerald-50',
    badgeText: 'text-emerald-700',
    badgeBorder: 'border-emerald-200',
    badgeClass: 'bg-emerald-50/90 text-emerald-700 border-emerald-200',
    dotClass: 'bg-emerald-500',
    ringClass: 'ring-emerald-400/30',
    borderClass: 'border-emerald-200',
    description: 'Baseline monitoring. Conditions within normal seasonal thresholds.'
  },
  MODERATE: {
    level: 'MODERATE',
    label: 'Moderate',
    minScore: 45,
    maxScore: 69,
    hexColor: '#F59E0B',
    badgeBg: 'bg-amber-50',
    badgeText: 'text-amber-700',
    badgeBorder: 'border-amber-200',
    badgeClass: 'bg-amber-50/90 text-amber-700 border-amber-200',
    dotClass: 'bg-amber-500',
    ringClass: 'ring-amber-400/30',
    borderClass: 'border-amber-200',
    description: 'Heightened surveillance warranted. Localized vulnerability anomalies observed.'
  },
  HIGH: {
    level: 'HIGH',
    label: 'High',
    minScore: 70,
    maxScore: 84,
    hexColor: '#F97316',
    badgeBg: 'bg-orange-50',
    badgeText: 'text-orange-700',
    badgeBorder: 'border-orange-200',
    badgeClass: 'bg-orange-50/90 text-orange-700 border-orange-200',
    dotClass: 'bg-orange-500',
    ringClass: 'ring-orange-400/30',
    borderClass: 'border-orange-200',
    description: 'Elevated hazard probability. Preparedness protocols and alerts active.'
  },
  CRITICAL: {
    level: 'CRITICAL',
    label: 'Critical',
    minScore: 85,
    maxScore: 100,
    hexColor: '#EF4444',
    badgeBg: 'bg-red-50',
    badgeText: 'text-red-700',
    badgeBorder: 'border-red-200',
    badgeClass: 'bg-red-50/90 text-red-700 border-red-200',
    dotClass: 'bg-red-500',
    ringClass: 'ring-red-400/30',
    borderClass: 'border-red-200',
    description: 'Severe impact threshold imminent or ongoing. Preemptive emergency response required.'
  }
};

/**
 * Determine the conceptual RiskLevel from a numeric score (0 - 100)
 */
export function getRiskLevel(score: number): RiskLevel {
  const cleanScore = Math.max(0, Math.min(100, Math.round(score)));
  if (cleanScore >= 85) return 'CRITICAL';
  if (cleanScore >= 70) return 'HIGH';
  if (cleanScore >= 45) return 'MODERATE';
  return 'LOW';
}

/**
 * Normalize and retrieve the configuration for any risk level (case-insensitive)
 */
export function getRiskConfig(level?: string | null): RiskLevelConfig {
  if (!level) return RISK_LEVEL_CONFIG.LOW;
  const normalized = level.toUpperCase() as RiskLevel;
  return RISK_LEVEL_CONFIG[normalized] || RISK_LEVEL_CONFIG.LOW;
}

/**
 * Get the full configuration and level directly from a score
 */
export function formatRiskScore(score: number): { level: RiskLevel; config: RiskLevelConfig } {
  const level = getRiskLevel(score);
  return {
    level,
    config: RISK_LEVEL_CONFIG[level]
  };
}

/**
 * Returns hex color code for map paths and charts
 */
export function getRiskHexColor(levelOrScore: RiskLevel | number): string {
  if (typeof levelOrScore === 'number') {
    return formatRiskScore(levelOrScore).config.hexColor;
  }
  return getRiskConfig(levelOrScore).hexColor;
}
