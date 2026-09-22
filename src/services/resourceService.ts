import {
  ReliefAgency,
  EmergencyShelter,
  ReliefRequirement,
  HelpCategory,
  Resource,
  ResourceType,
  ResourceCategory,
  ResourceVerificationStatus
} from '../types/resource';
import {
  VERIFIED_AGENCIES,
  EMERGENCY_SHELTERS,
  RELIEF_REQUIREMENTS,
  NATIONAL_HELPLINES,
  UNIFIED_RESOURCES,
  OFFICIAL_DISASTER_PORTALS
} from '../data/resources';
import { API_ENDPOINTS } from '../config/api';
import { apiClient } from './api';

function normalizeResource(item: any): Resource {
  return {
    id: item.id,
    name: item.name,
    type: (item.resource_type || item.type || 'GOVERNMENT') as ResourceType,
    resource_type: (item.resource_type || item.type || 'GOVERNMENT') as ResourceType,
    category: item.category || 'Disaster Management',
    location: item.location || (item.address ? `${item.district || ''}, ${item.state || ''}` : item.state || 'India'),
    state: item.state || 'Pan-India',
    district: item.district,
    disaster_type: item.disaster_type || 'ALL',
    description: item.description || '',
    website: item.website_url || item.website,
    website_url: item.website_url || item.website,
    contactNumber: item.contact_number || item.phone,
    phone: item.phone || item.contact_number,
    address: item.address,
    latitude: item.latitude,
    longitude: item.longitude,
    source: item.source,
    source_url: item.source_url,
    verificationStatus: (item.verification_status || 'VERIFIED') as ResourceVerificationStatus,
    verification_status: item.verification_status || 'VERIFIED',
    services: item.services || [],
    lastVerified: item.last_verified_at ? item.last_verified_at.slice(0, 10) : item.last_verified,
    last_verified_at: item.last_verified_at,
    freshness: item.freshness || 'CURRENT',
    accessibilityNotes: item.accessibility_notes || item.accessibilityNotes,
    accessibility_notes: item.accessibility_notes,
    isDemoData: Boolean(item.is_demo)
  };
}

export const resourceService = {
  /**
   * Return verified national emergency contacts and helplines
   */
  getHelplines: () => {
    return NATIONAL_HELPLINES;
  },

  /**
   * Return official national disaster management and warning portals
   */
  getOfficialPortals: () => {
    return OFFICIAL_DISASTER_PORTALS;
  },

  /**
   * Fetch verified resources matching optional location, category, type, and disaster filters
   */
  getResources: async (params?: {
    location?: string;
    state?: string;
    district?: string;
    category?: ResourceCategory | string;
    type?: ResourceType | 'ALL';
    resource_type?: string;
    disaster_type?: string;
    verificationStatus?: ResourceVerificationStatus | 'ALL';
  }): Promise<Resource[]> => {
    try {
      const query = new URLSearchParams();
      const loc = params?.state || params?.location;
      if (loc && loc !== 'All' && loc !== 'ALL') query.set('state', loc);
      if (params?.district && params.district !== 'All' && params.district !== 'ALL') query.set('district', params.district);
      if (params?.category && params.category !== 'All' && params.category !== 'ALL') query.set('category', params.category);
      const rType = params?.resource_type || params?.type;
      if (rType && rType !== 'ALL') query.set('resource_type', rType);
      if (params?.disaster_type && params.disaster_type !== 'All' && params.disaster_type !== 'ALL') query.set('disaster_type', params.disaster_type);
      if (params?.verificationStatus && params.verificationStatus !== 'ALL') query.set('verification_status', params.verificationStatus);

      const url = `${API_ENDPOINTS.resources.list()}?${query.toString()}`;
      const data = await apiClient.get<any[]>(url, { timeoutMs: 6000 });
      if (Array.isArray(data)) {
        return data.map(normalizeResource);
      }
    } catch (err) {
      console.warn('Backend resources API unavailable, falling back to verified static catalog:', err);
    }

    // Safe offline fallback with identical verified filtering rules
    return UNIFIED_RESOURCES.filter((item) => {
      let matchLocation = true;
      const filterLoc = (params?.state || params?.location || '').toLowerCase().trim();
      if (filterLoc && filterLoc !== 'all') {
        matchLocation = Boolean(
          item.state?.toLowerCase() === 'pan-india' ||
          item.state?.toLowerCase().includes(filterLoc) ||
          item.location.toLowerCase().includes(filterLoc) ||
          (item.district && item.district.toLowerCase().includes(filterLoc))
        );
      }

      let matchDistrict = true;
      if (params?.district && params.district !== 'All') {
        const dClean = params.district.toLowerCase().trim();
        matchDistrict = Boolean(
          item.district?.toLowerCase().includes(dClean) ||
          item.state?.toLowerCase() === 'pan-india' ||
          item.district === 'All Districts'
        );
      }

      let matchCategory = true;
      if (params?.category && params.category !== 'All') {
        const catClean = params.category.toLowerCase().trim();
        matchCategory = Boolean(
          item.category.toLowerCase().includes(catClean) ||
          item.services?.some((s) => s.toLowerCase().includes(catClean))
        );
      }

      const rType = params?.resource_type || params?.type;
      const matchType = !rType || rType === 'ALL' || item.type === rType;

      let matchDisaster = true;
      if (params?.disaster_type && params.disaster_type !== 'All') {
        const dtClean = params.disaster_type.toUpperCase().trim();
        matchDisaster = Boolean(
          !item.disaster_type ||
          item.disaster_type.toUpperCase() === 'ALL' ||
          item.disaster_type.toUpperCase() === dtClean
        );
      }

      const matchVerification =
        !params?.verificationStatus ||
        params.verificationStatus === 'ALL' ||
        item.verificationStatus === params.verificationStatus;

      return matchLocation && matchDistrict && matchCategory && matchType && matchDisaster && matchVerification;
    });
  },

  /**
   * Fetch resources specifically by location string
   */
  getResourcesByLocation: async (locationQuery: string): Promise<Resource[]> => {
    return resourceService.getResources({ location: locationQuery });
  },

  /**
   * Return verified relief agencies (Government & Statutory NGO)
   */
  getVerifiedAgencies: async (): Promise<ReliefAgency[]> => {
    return VERIFIED_AGENCIES;
  },

  /**
   * Fetch verified emergency shelters, optionally filtered by state
   */
  getEmergencyShelters: async (state?: string): Promise<EmergencyShelter[]> => {
    if (!state || state === 'All') return EMERGENCY_SHELTERS;
    return EMERGENCY_SHELTERS.filter((s) => s.state.toLowerCase() === state.toLowerCase());
  },

  /**
   * Fetch prioritized relief requirements by category
   */
  getReliefRequirements: async (category?: HelpCategory | 'All'): Promise<ReliefRequirement[]> => {
    if (!category || category === 'All') return RELIEF_REQUIREMENTS;
    return RELIEF_REQUIREMENTS.filter((r) => r.category === category);
  },

  /**
   * Get resource detail by ID
   */
  getResourceById: async (id: string): Promise<Resource | undefined> => {
    try {
      const res = await fetch(`${API_ENDPOINTS.resources.list()}/${encodeURIComponent(id)}`);
      if (res.ok) {
        const data = await res.json();
        return normalizeResource(data);
      }
    } catch (err) {
      console.warn(`Resource ID ${id} fetch error:`, err);
    }
    return UNIFIED_RESOURCES.find((r) => r.id === id);
  }
};
