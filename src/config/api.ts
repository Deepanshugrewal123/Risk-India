/// <reference types="vite/client" />

/**
 * API and Environment Configuration
 * 
 * Supports local offline mode or direct FastAPI backend at API_BASE_URL.
 */

export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/+$/, '');

export const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA !== 'false';

export const API_ENDPOINTS = {
  risk: {
    analyze: `${API_BASE_URL}/api/risk/analyze`,
    byLocation: (location: string) => `${API_BASE_URL}/api/risk/${encodeURIComponent(location)}`,
    nationalSnapshot: `${API_BASE_URL}/api/risk/national-snapshot`,
    regions: `${API_BASE_URL}/api/risk/regions`,
  },
  disasters: {
    list: `${API_BASE_URL}/api/disasters`,
    live: `${API_BASE_URL}/api/disasters/live`,
    refresh: `${API_BASE_URL}/api/disasters/refresh`,
    byId: (id: string) => `${API_BASE_URL}/api/disasters/${encodeURIComponent(id)}`,
  },
  resources: {
    list: (params?: { location?: string; type?: string }) => {
      const query = new URLSearchParams();
      if (params?.location) query.set('location', params.location);
      if (params?.type) query.set('type', params.type);
      const queryString = query.toString();
      return `${API_BASE_URL}/api/resources${queryString ? `?${queryString}` : ''}`;
    },
    shelters: `${API_BASE_URL}/api/resources/shelters`,
    helplines: `${API_BASE_URL}/api/resources/helplines`,
    agencies: `${API_BASE_URL}/api/resources/agencies`,
    requirements: `${API_BASE_URL}/api/resources/requirements`,
    pledgeVolunteer: `${API_BASE_URL}/api/resources/volunteer-pledge`,
    pledgeDonation: `${API_BASE_URL}/api/resources/donation-pledge`,
  },
  assistant: {
    chat: `${API_BASE_URL}/api/assistant/chat`,
  }
} as const;
