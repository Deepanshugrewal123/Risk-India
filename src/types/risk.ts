import { Location } from './location';

export type DisasterType = 
  | 'Flood'
  | 'Landslide'
  | 'Cyclone'
  | 'Earthquake'
  | 'Heatwave'
  | 'Drought'
  | 'flood'
  | 'landslide'
  | 'cyclone'
  | 'earthquake'
  | 'heatwave'
  | 'drought';

export type RiskLevel = 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL';

export interface RiskFactor {
  name: string;
  value?: string | number; // e.g. "High" or 84
  importance?: number; // 0.0 to 1.0 (SHAP / Feature Importance ready)
  weight?: number; // 0 to 100
  trend?: 'rising' | 'stable' | 'decreasing';
  impact?: 'High' | 'Medium' | 'Low';
  description?: string;
}

export interface RiskAssessment {
  id?: string;
  location: Location | { state: string; district: string; city?: string };
  disasterType: DisasterType;
  riskScore: number; // 0 - 100
  riskLevel: RiskLevel;
  confidenceScore?: number; // 0 - 100
  factors: RiskFactor[];
  primaryDriver?: string;
  recommendedActions: string[];
  recommendedImmediateAction?: string;
  historicalIncidentFrequency?: string;
  predictedPeakTimeWindow?: string;
  modelVersion: string;
  timestamp: string;
  isDemoData: boolean;
}

export interface RegionRiskData {
  id: string;
  name: string; // State or Major Region
  code: string; // 2-letter state code e.g. AS, HP, OD
  capital: string;
  riskScore: number; // 0 - 100
  riskLevel: RiskLevel;
  primaryRisk: DisasterType;
  secondaryRisk?: DisasterType;
  monitoredDistricts: number;
  criticalDistrictsCount: number;
  summary: string;
  factors: RiskFactor[];
  historicalTrend: { year: number; score: number }[];
  emergencyHelpline: string;
  activeIncidentsCount: number;
  recommendedActions: string[];
  isDemoData?: boolean;
}

export interface NationalRiskSnapshot {
  criticalAreas: number;
  highRiskAreas: number;
  activeDisasters: number;
  monitoredRegions: number;
  lastSyncTime: string;
  isDemoData?: boolean;
}

export * from './disaster';
