/**
 * RISK // INDIA — National Weather Intelligence Frontend Interfaces
 */

export interface WeatherObservation {
  observation_id: string;
  region_id: string;
  region_name: string;
  region_type: string;
  latitude: number;
  longitude: number;
  observed_at: string;
  ingested_at: string;
  temperature_celsius?: number;
  feels_like_celsius?: number;
  relative_humidity_percent?: number;
  rainfall_mm?: number;
  wind_speed_mps?: number;
  surface_pressure_hpa?: number;
  visibility_km?: number;
  weather_condition: string;
  thunderstorm_indicator: boolean;
  lightning_indicator: boolean;
  source_provider: string;
  source_url: string;
  freshness: string;
  synthetic_records: number;
  provenance: Record<string, any>;
}

export interface WeatherForecast {
  forecast_id: string;
  region_id: string;
  region_name: string;
  forecasted_at: string;
  forecast_valid_from: string;
  forecast_valid_until: string;
  forecast_horizon: string;
  temperature_celsius?: number;
  rainfall_mm?: number;
  wind_speed_mps?: number;
  relative_humidity_percent?: number;
  surface_pressure_hpa?: number;
  weather_condition: string;
  forecast_source: string;
  uncertainty: 'LOW' | 'MODERATE' | 'HIGH' | 'VERY_HIGH';
  freshness: string;
  synthetic_records: number;
  provenance: Record<string, any>;
}

export interface WeatherWarning {
  warning_id: string;
  provider: string;
  hazard: string;
  severity: 'RED' | 'ORANGE' | 'YELLOW' | 'GREEN';
  headline: string;
  description: string;
  issued_at: string;
  valid_from: string;
  valid_until: string;
  affected_region: string;
  source_record_id: string;
  source_url: string;
  freshness: string;
  synthetic_records: number;
  provenance: Record<string, any>;
}

export interface WeatherEvidenceSignal {
  hazard: string;
  signal_type: string;
  metric: string;
  value: any;
  lead_time: string;
  implication: string;
  confidence: string;
  uncertainty: string;
  source: string;
  synthetic_records: number;
}

export interface WeatherSubsystemStatus {
  status: string;
  subsystem: string;
  backend_storage: string;
  entities_monitored: number;
  total_observations_ingested: number;
  total_forecasts_managed: number;
  total_active_warnings: number;
  synthetic_records_total: number;
  provider_circuits: Record<string, {
    state: string;
    failures: number;
    latency_ms: number;
    healthy: boolean;
  }>;
  timestamp_utc: string;
}

export interface WeatherRegionOverview {
  region: string;
  region_type: string;
  region_id: string;
  current_weather: WeatherObservation;
  forecast_timeline: WeatherForecast[];
  active_warnings: WeatherWarning[];
  hazard_evidence: {
    region: string;
    evaluated_at: string;
    signals_count: number;
    evidence_signals: WeatherEvidenceSignal[];
    earthquake_boundary: string;
    synthetic_records: number;
  };
  synthetic_records: number;
}
