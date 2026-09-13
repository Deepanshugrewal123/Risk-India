import { DisasterType } from './risk';

export type AdministrativeType = 'STATE' | 'UNION_TERRITORY';

export interface IndiaLocation {
  id: string;
  name: string;
  type: AdministrativeType;
  code: string;
  capital: string;
  region: string; // e.g. 'North India', 'South India', 'East India', 'West India', 'Central India', 'Northeast India', 'Islands'
  latitude: number;
  longitude: number;
  districts: string[];
  primaryRisk?: DisasterType;
  secondaryRisk?: DisasterType;
  riskScore?: number;
  isDemoData?: boolean;
}

export interface Location {
  id: string;
  state: string;
  district: string;
  city?: string;
  latitude: number;
  longitude: number;
  isDemoData?: boolean;
}

export interface StateDistrictMap {
  state: string;
  code: string;
  districts: string[];
}
