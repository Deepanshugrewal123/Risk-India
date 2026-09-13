import { DisasterEvent, DisasterStatus } from '../types/disaster';
import { DisasterType, RiskLevel } from '../types/risk';
import { ACTIVE_DISASTERS } from '../data/disasters';
import { API_ENDPOINTS } from '../config/api';

function normalizeDisaster(item: any): DisasterEvent {
  const hazardType = item.hazard_type || item.disaster_type || 'Flood';
  const lat = item.latitude ?? (item.coordinates ? item.coordinates[0] : 26.1445);
  const lng = item.longitude ?? (item.coordinates ? item.coordinates[1] : 91.7362);
  const state = item.state || 'India';
  const district = item.district || '';
  const location = item.location || (district ? `${district}, ${state}` : state);

  return {
    id: item.id,
    title: item.title,
    location,
    state,
    district,
    coordinates: [lat, lng],
    type: hazardType as DisasterType,
    disasterType: hazardType as DisasterType,
    severity: (item.severity || 'MODERATE') as RiskLevel,
    status: (item.status || 'Active') as DisasterStatus,
    riskScore: item.risk_score || 60,
    description: item.description || '',
    source: item.source,
    officialSource: item.source,
    source_url: item.source_url,
    sourceUrl: item.source_url,
    verified: Boolean(item.verified),
    isDemoData: Boolean(item.is_demo),
    freshness: item.freshness || 'RECENT',
    observed_at: item.observed_at,
    retrieved_at: item.retrieved_at,
    timestamp: item.freshness ? `${item.freshness} • ${item.source || 'Official Source'}` : 'Monitored Report',
    lastUpdated: item.retrieved_at || 'Recently',
    affectedPopulationEstimate: item.affectedPopulationEstimate,
    reportedEvacuations: item.reportedEvacuations,
    activeSheltersCount: item.activeSheltersCount,
    reliefTeamsDeployed: item.reliefTeamsDeployed,
    keyFactors: item.keyFactors || [
      `Official Source: ${item.source || 'Authorized Feed'}`,
      `Verification: ${item.verified ? 'Verified Official Source' : 'Reference Archive'}`,
      `Freshness State: ${item.freshness || 'RECENT'}`
    ],
    safetyAdvisories: item.safetyAdvisories || [
      'Heed regional alerts broadcast by district administration and state disaster management authority.',
      'Check official portal for localized evacuation instructions and relief camp allotments.'
    ]
  };
}

export const disasterService = {
  /**
   * Fetch all currently active or monitored disaster incidents from live backend
   */
  getActiveDisasters: async (): Promise<DisasterEvent[]> => {
    try {
      const res = await fetch(API_ENDPOINTS.disasters.list);
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          return data.map(normalizeDisaster);
        }
      }
    } catch (err) {
      console.warn('Disasters API fetch failed, falling back to reference dataset:', err);
    }
    return ACTIVE_DISASTERS;
  },

  /**
   * Specifically fetch verified live & recent disaster events
   */
  getLiveDisasters: async (): Promise<DisasterEvent[]> => {
    try {
      const res = await fetch(API_ENDPOINTS.disasters.live);
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data)) {
          return data.map(normalizeDisaster);
        }
      }
    } catch (err) {
      console.warn('Live disasters API fetch failed:', err);
    }
    return [];
  },

  /**
   * Fetch all recorded disaster incidents including resolved
   */
  getAllDisasters: async (): Promise<DisasterEvent[]> => {
    return disasterService.getActiveDisasters();
  },

  /**
   * Filter disasters by hazard type, severity level, status, or state
   */
  filterDisasters: async (
    type?: DisasterType | 'All',
    severity?: RiskLevel | string | 'All',
    status?: DisasterStatus | string | 'All',
    state?: string
  ): Promise<DisasterEvent[]> => {
    try {
      const params = new URLSearchParams();
      if (type && type !== 'All') params.set('type', type);
      if (status && status !== 'All') params.set('status', status);
      if (state) params.set('state', state);

      const url = `${API_ENDPOINTS.disasters.list}?${params.toString()}`;
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          let list = data.map(normalizeDisaster);
          if (severity && severity !== 'All') {
            list = list.filter((i) => i.severity.toLowerCase() === severity.toLowerCase());
          }
          return list;
        }
      }
    } catch (err) {
      console.warn('Filtered disasters API fetch failed, falling back to local filter:', err);
    }

    const all = await disasterService.getActiveDisasters();
    return all.filter((incident) => {
      const matchType = !type || type === 'All' || incident.type.toLowerCase() === type.toLowerCase();
      const matchSeverity = !severity || severity === 'All' || incident.severity.toLowerCase() === severity.toLowerCase();
      const matchState = !state || incident.state.toLowerCase().includes(state.toLowerCase());
      
      let matchStatus = true;
      if (status && status !== 'All') {
        const queryStatus = status.toLowerCase();
        const itemStatus = incident.status.toLowerCase();
        if (queryStatus === 'active') {
          matchStatus = itemStatus.includes('active') || itemStatus.includes('relief');
        } else if (queryStatus === 'monitoring') {
          matchStatus = itemStatus.includes('monitoring');
        } else if (queryStatus === 'resolved') {
          matchStatus = itemStatus.includes('resolved') || itemStatus.includes('contained');
        } else {
          matchStatus = itemStatus === queryStatus;
        }
      }

      return matchType && matchSeverity && matchStatus && matchState;
    });
  },

  /**
   * Trigger cache refresh from upstream disaster feeds
   */
  refreshDisasters: async (): Promise<boolean> => {
    try {
      const res = await fetch(API_ENDPOINTS.disasters.refresh);
      return res.ok;
    } catch (err) {
      console.error('Error refreshing disasters:', err);
      return false;
    }
  },

  /**
   * Get disaster incident detail by unique ID
   */
  getDisasterById: async (id: string): Promise<DisasterEvent | undefined> => {
    try {
      const res = await fetch(API_ENDPOINTS.disasters.byId(id));
      if (res.ok) {
        const item = await res.json();
        return normalizeDisaster(item);
      }
    } catch (err) {
      console.warn(`Disaster ID ${id} API fetch failed:`, err);
    }
    const all = await disasterService.getActiveDisasters();
    return all.find((d) => d.id === id);
  },

  /**
   * Get disasters in a specific state or district
   */
  getDisastersByLocation: async (locationQuery: string): Promise<DisasterEvent[]> => {
    return disasterService.filterDisasters(undefined, undefined, undefined, locationQuery);
  }
};
