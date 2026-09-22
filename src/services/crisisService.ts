/**
 * RISK // INDIA — National Crisis Intelligence API Client (Phase 30E)
 * ====================================================================
 */

import { apiClient } from './api';
import {
  CrisisAssessment,
  NationalCrisisOverview,
  CrisisActionItem,
  CrisisResourceItem,
  CrisisTimelinePoint,
  CrisisExplanation,
  FamilyChecklistItem
} from '../types/crisis';

export interface CrisisStatusResponse {
  status: string;
  system: string;
  timestamp: string;
  operational_state_distribution: Record<string, number>;
  crisis_recommended_count: number;
  crisis_recommended_regions: Array<{
    region_id: string;
    region_name: string;
    operational_state: string;
    primary_hazard: string;
    activation_reason: string;
  }>;
  national_emergency_helplines: Record<string, string>;
  synthetic_records: number;
}

export interface RegionActionsResponse {
  region_id: string;
  region_name: string;
  primary_hazard: string;
  operational_state: string;
  what_to_do_now: CrisisActionItem[];
  action_protocols: {
    BEFORE?: CrisisActionItem[];
    DURING?: CrisisActionItem[];
    AFTER?: CrisisActionItem[];
  };
  family_prep_checklist: FamilyChecklistItem[];
  synthetic_records: number;
}

export interface RegionResourcesResponse {
  region_id: string;
  region_name: string;
  primary_hazard: string;
  emergency_resources: CrisisResourceItem[];
  resource_availability_note?: string;
  synthetic_records: number;
}

export const crisisService = {
  getStatus: async (): Promise<CrisisStatusResponse> => {
    return apiClient.get<CrisisStatusResponse>('/api/crisis/status');
  },

  getNationalOverview: async (): Promise<NationalCrisisOverview> => {
    return apiClient.get<NationalCrisisOverview>('/api/crisis/national');
  },

  getRegionAssessment: async (
    region: string,
    hazard?: string,
    manual: boolean = false,
    lat?: number,
    lon?: number
  ): Promise<CrisisAssessment> => {
    const params = new URLSearchParams();
    if (hazard) params.append('hazard', hazard);
    if (manual) params.append('manual', 'true');
    if (lat !== undefined && lon !== undefined) {
      params.append('lat', lat.toString());
      params.append('lon', lon.toString());
    }
    const query = params.toString() ? `?${params.toString()}` : '';
    return apiClient.get<CrisisAssessment>(`/api/crisis/${encodeURIComponent(region)}${query}`);
  },

  getRegionActions: async (region: string, hazard?: string): Promise<RegionActionsResponse> => {
    const params = new URLSearchParams();
    if (hazard) params.append('hazard', hazard);
    const query = params.toString() ? `?${params.toString()}` : '';
    return apiClient.get<RegionActionsResponse>(`/api/crisis/${encodeURIComponent(region)}/actions${query}`);
  },

  getRegionResources: async (
    region: string,
    hazard?: string,
    lat?: number,
    lon?: number
  ): Promise<RegionResourcesResponse> => {
    const params = new URLSearchParams();
    if (hazard) params.append('hazard', hazard);
    if (lat !== undefined && lon !== undefined) {
      params.append('lat', lat.toString());
      params.append('lon', lon.toString());
    }
    const query = params.toString() ? `?${params.toString()}` : '';
    return apiClient.get<RegionResourcesResponse>(`/api/crisis/${encodeURIComponent(region)}/resources${query}`);
  },

  getRegionTimeline: async (
    region: string,
    hazard?: string
  ): Promise<{ region_id: string; region_name: string; primary_hazard: string; timeline: CrisisTimelinePoint[]; synthetic_records: number }> => {
    const params = new URLSearchParams();
    if (hazard) params.append('hazard', hazard);
    const query = params.toString() ? `?${params.toString()}` : '';
    return apiClient.get(`/api/crisis/${encodeURIComponent(region)}/timeline${query}`);
  },

  getRegionExplanation: async (
    region: string,
    hazard?: string
  ): Promise<{ region_id: string; region_name: string; primary_hazard: string; explanation: CrisisExplanation; synthetic_records: number }> => {
    const params = new URLSearchParams();
    if (hazard) params.append('hazard', hazard);
    const query = params.toString() ? `?${params.toString()}` : '';
    return apiClient.get(`/api/crisis/${encodeURIComponent(region)}/explanation${query}`);
  }
};

export default crisisService;
