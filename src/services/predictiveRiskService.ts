/**
 * RISK // INDIA — National Predictive Risk Fusion Service API Client (Phase 30F)
 * ===============================================================================
 * Client for fetching national predictive posture, regional fused assessments,
 * 5-horizon timelines, scenarios, early-warning guidance, and 12 citizen safety answers.
 */

import { apiClient } from './api';
import {
  PredictiveRiskAssessment,
  NationalPredictiveOverview,
  PredictiveTimelinePoint,
  PredictionExplanation,
  PredictiveScenario,
  EarlyWarningAssessment,
  AuthoritativeProviderInfo
} from '../types/predictiveRisk';

export const predictiveRiskService = {
  /**
   * Retrieves the comprehensive national overview covering all 36 Indian States & UTs.
   */
  getNationalOverview: async (): Promise<NationalPredictiveOverview> => {
    return apiClient.get<NationalPredictiveOverview>('/api/predictive-risk/national');
  },

  /**
   * Retrieves full fused predictive risk assessment for an entity and hazard.
   */
  getRegionalAssessment: async (
    region: string,
    hazard?: string
  ): Promise<PredictiveRiskAssessment> => {
    const query = hazard ? `?hazard=${encodeURIComponent(hazard)}` : '';
    return apiClient.get<PredictiveRiskAssessment>(
      `/api/predictive-risk/${encodeURIComponent(region)}${query}`
    );
  },

  /**
   * Retrieves assessment for a specific hazard in a region.
   */
  getHazardAssessment: async (
    region: string,
    hazard: string
  ): Promise<PredictiveRiskAssessment> => {
    return apiClient.get<PredictiveRiskAssessment>(
      `/api/predictive-risk/${encodeURIComponent(region)}/${encodeURIComponent(hazard)}`
    );
  },

  /**
   * Retrieves 5-horizon predictive timeline points across NOW, 0-6h, 6-24h, 1-3d, and 3-7d.
   */
  getTimeline: async (
    region: string,
    hazard?: string
  ): Promise<PredictiveTimelinePoint[]> => {
    const query = hazard ? `?hazard=${encodeURIComponent(hazard)}` : '';
    return apiClient.get<PredictiveTimelinePoint[]>(
      `/api/predictive-risk/${encodeURIComponent(region)}/timeline${query}`
    );
  },

  /**
   * Retrieves transparent explanations and direct answers to all 12 citizen questions.
   */
  getExplanation: async (
    region: string,
    hazard?: string
  ): Promise<PredictionExplanation> => {
    const query = hazard ? `?hazard=${encodeURIComponent(hazard)}` : '';
    return apiClient.get<PredictionExplanation>(
      `/api/predictive-risk/${encodeURIComponent(region)}/explanation${query}`
    );
  },

  /**
   * Retrieves Baseline, Likely, and Escalation forward-looking scenarios.
   */
  getScenarios: async (
    region: string,
    hazard?: string
  ): Promise<PredictiveScenario[]> => {
    const query = hazard ? `?hazard=${encodeURIComponent(hazard)}` : '';
    return apiClient.get<PredictiveScenario[]>(
      `/api/predictive-risk/${encodeURIComponent(region)}/scenarios${query}`
    );
  },

  /**
   * Retrieves progressive early warning posture and action guidance.
   */
  getEarlyWarning: async (
    region: string,
    hazard?: string
  ): Promise<EarlyWarningAssessment> => {
    const query = hazard ? `?hazard=${encodeURIComponent(hazard)}` : '';
    return apiClient.get<EarlyWarningAssessment>(
      `/api/predictive-risk/${encodeURIComponent(region)}/early-warning${query}`
    );
  },

  /**
   * Retrieves directional momentum mapping across all 36 entities.
   */
  getTrends: async (): Promise<{
    total_entities: number;
    trends: Record<string, any>;
    synthetic_records: number;
  }> => {
    return apiClient.get('/api/predictive-risk/trends');
  },

  /**
   * Retrieves regions requiring active preparation or evacuation readiness.
   */
  getReadiness: async (): Promise<{
    actionable_count: number;
    entities: Array<any>;
    synthetic_records: number;
  }> => {
    return apiClient.get('/api/predictive-risk/readiness');
  },

  /**
   * Retrieves authoritative upstream providers and their operational status.
   */
  getProviders: async (): Promise<AuthoritativeProviderInfo[]> => {
    return apiClient.get<AuthoritativeProviderInfo[]>('/api/predictive-risk/providers');
  }
};

export default predictiveRiskService;
