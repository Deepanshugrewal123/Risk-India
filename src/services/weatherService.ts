/**
 * RISK // INDIA — National Weather Intelligence Service API Client
 */

import { apiClient } from './api';
import {
  WeatherObservation,
  WeatherForecast,
  WeatherWarning,
  WeatherSubsystemStatus,
  WeatherRegionOverview
} from '../types/weather';

export const weatherService = {
  getStatus: async (): Promise<WeatherSubsystemStatus> => {
    return apiClient.get<WeatherSubsystemStatus>('/api/weather/status');
  },

  getCurrentWeather: async (region?: string, limit: number = 50): Promise<{ count: number; observations: WeatherObservation[] }> => {
    const params = new URLSearchParams();
    if (region) params.append('region', region);
    if (limit) params.append('limit', limit.toString());
    return apiClient.get<{ count: number; observations: WeatherObservation[] }>(`/api/weather/current?${params.toString()}`);
  },

  getForecasts: async (region?: string, horizon?: string, limit: number = 100): Promise<{ count: number; forecasts: WeatherForecast[] }> => {
    const params = new URLSearchParams();
    if (region) params.append('region', region);
    if (horizon) params.append('horizon', horizon);
    if (limit) params.append('limit', limit.toString());
    return apiClient.get<{ count: number; forecasts: WeatherForecast[] }>(`/api/weather/forecast?${params.toString()}`);
  },

  getWarnings: async (region?: string, hazard?: string, severity?: string): Promise<{ count: number; warnings: WeatherWarning[] }> => {
    const params = new URLSearchParams();
    if (region) params.append('region', region);
    if (hazard) params.append('hazard', hazard);
    if (severity) params.append('severity', severity);
    return apiClient.get<{ count: number; warnings: WeatherWarning[] }>(`/api/weather/warnings?${params.toString()}`);
  },

  getRegionOverview: async (region: string): Promise<WeatherRegionOverview> => {
    return apiClient.get<WeatherRegionOverview>(`/api/weather/regions/${encodeURIComponent(region)}`);
  },

  getReadiness: async (): Promise<{
    probe_name: string;
    evaluated_at: string;
    total_administrative_entities: number;
    entities_with_live_telemetry: number;
    coverage_percent: number;
    readiness_status: string;
    synthetic_records: number;
  }> => {
    return apiClient.get('/api/weather/readiness');
  }
};

export default weatherService;
