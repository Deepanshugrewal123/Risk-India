import { DisasterType, RiskLevel } from './risk';
import { Location } from './location';

export type DisasterStatus = 
  | 'active'
  | 'monitoring'
  | 'resolved'
  | 'Active'
  | 'Monitoring'
  | 'Contained'
  | 'Relief Ongoing';

export interface DisasterEvent {
  id: string;
  title: string;
  location: string;
  state: string;
  district: string;
  coordinates: [number, number]; // [lat, lng]
  type: DisasterType;
  disasterType?: DisasterType;
  severity: RiskLevel;
  status: DisasterStatus;
  riskScore?: number;
  description: string;
  source?: string;
  officialSource?: string;
  source_url?: string;
  sourceUrl?: string;
  timestamp?: string;
  lastUpdated?: string;
  observed_at?: string;
  retrieved_at?: string;
  freshness?: 'LIVE' | 'RECENT' | 'STALE' | 'UNAVAILABLE';
  verified?: boolean;
  affectedPopulationEstimate?: string;
  reportedEvacuations?: string;
  activeSheltersCount?: number;
  reliefTeamsDeployed?: number;
  keyFactors?: string[];
  safetyAdvisories?: string[];
  isDemoData?: boolean;
  isMockData?: boolean;
}

// Backward-compatible alias
export type DisasterIncident = DisasterEvent;
