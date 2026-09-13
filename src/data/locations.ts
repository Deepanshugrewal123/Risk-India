import { Location } from '../types/location';
import { ALL_INDIAN_LOCATIONS, ALL_INDIAN_STATES, ALL_INDIAN_UNION_TERRITORIES } from './indiaLocations';

export interface StateDistrictOption {
  state: string;
  code: string;
  districts: string[];
  type?: 'STATE' | 'UNION_TERRITORY';
  region?: string;
  latitude?: number;
  longitude?: number;
}

/**
 * Backward-compatible full list of all 37 Indian States and Union Territories with districts
 */
export const INDIAN_LOCATIONS: StateDistrictOption[] = ALL_INDIAN_LOCATIONS.map((loc) => ({
  state: loc.name,
  code: loc.code,
  districts: loc.districts,
  type: loc.type,
  region: loc.region,
  latitude: loc.latitude,
  longitude: loc.longitude
}));

/**
 * Structured locations for map markers and backward-compatible services
 */
export const STRUCTURED_LOCATIONS: Location[] = ALL_INDIAN_LOCATIONS.map((loc) => ({
  id: `loc-${loc.code.toLowerCase()}-${loc.id}`,
  state: loc.name,
  district: loc.districts[0] || loc.capital,
  city: loc.capital,
  latitude: loc.latitude,
  longitude: loc.longitude,
  isDemoData: true
}));

export { ALL_INDIAN_STATES, ALL_INDIAN_UNION_TERRITORIES, ALL_INDIAN_LOCATIONS };
