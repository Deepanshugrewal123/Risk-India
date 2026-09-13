export type ResourceType = 
  | 'GOVERNMENT'
  | 'NGO'
  | 'SHELTER'
  | 'HOSPITAL'
  | 'HELPLINE'
  | 'RELIEF_CENTER';

export type ResourceVerificationStatus = 'VERIFIED' | 'UNDER_AUDIT' | 'DEMO' | 'PENDING';

export type ResourceCategory =
  | 'Emergency Services'
  | 'Government Relief'
  | 'Medical Assistance'
  | 'Shelter'
  | 'Food & Water'
  | 'Rescue'
  | 'Disaster Management'
  | 'NGO / Relief Organization'
  | 'Donations / Volunteering'
  | 'All';

export type FreshnessStatus =
  | 'CURRENT'
  | 'RECENTLY_VERIFIED'
  | 'HISTORICAL'
  | 'AVAILABILITY_UNKNOWN';

export interface Resource {
  id: string;
  name: string;
  type: ResourceType;
  resource_type?: ResourceType;
  category: string;
  location: string;
  state?: string;
  district?: string;
  disaster_type?: string;
  description: string;
  website?: string;
  website_url?: string;
  contactNumber?: string;
  phone?: string;
  address?: string;
  latitude?: number;
  longitude?: number;
  source?: string;
  source_url?: string;
  verificationStatus: ResourceVerificationStatus;
  verification_status?: string;
  services?: string[];
  lastVerified?: string;
  last_verified_at?: string;
  freshness?: FreshnessStatus;
  accessibilityNotes?: string;
  accessibility_notes?: string;
  isDemoData: boolean;
}

// Relief and assistance domain types (preserved for compatibility)
export type ReliefAgencyType = 'Government Agency' | 'Grassroots NGO' | 'International Aid' | 'Community Kitchen';

export type VerificationStatus = 'Government Verified' | 'NGO Verified' | 'Under Audit';

export type HelpCategory = 'Donate' | 'Volunteer' | 'Supplies' | 'Medical Support' | 'Emergency Shelter';

export interface ReliefAgency {
  id: string;
  name: string;
  type: ReliefAgencyType;
  verificationStatus: VerificationStatus;
  headquarters: string;
  operationalStates: string[];
  activeOperations: string[];
  servicesOffered: string[];
  officialPortalUrl: string;
  contactNumber: string;
  transparencyScore: number; // 0 - 100
  urgentlyNeededSupplies: string[];
  volunteerRolesNeeded: string[];
  isDemoData: boolean;
}

export interface EmergencyShelter {
  id: string;
  name: string;
  location: string;
  district: string;
  state: string;
  capacity: number;
  currentOccupancy: number;
  amenities: string[];
  emergencyContact: string;
  status: 'Open & Accepting' | 'Near Capacity' | 'Full';
  isDemoData: boolean;
  latitude?: number;
  longitude?: number;
  source?: string;
  sourceUrl?: string;
}

export interface ReliefRequirement {
  id: string;
  category: HelpCategory;
  title: string;
  targetRegion: string;
  urgency: 'Immediate (24h)' | 'Urgent (3-5d)' | 'Ongoing Recovery';
  description: string;
  quantityOrGoal: string;
  currentFulfilled: string;
  verifiedPartner: string;
  partnerUrl?: string;
  isDemoData: boolean;
}
