from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
import logging

from app.models.resource import Resource
from app.models.location import Location

logger = logging.getLogger("resource-service")

# Authoritative, verified Indian emergency and disaster relief entities
VERIFIED_RESOURCES_REGISTRY: List[Dict[str, Any]] = [
    {
        "id": "gov-ndma-hq",
        "name": "National Disaster Management Authority (NDMA HQ)",
        "resource_type": "GOVERNMENT",
        "category": "Disaster Management",
        "description": "Apex statutory body for disaster management in India providing national guidelines, NDRF deployment oversight, and multi-state coordination.",
        "state": "Pan-India",
        "district": "New Delhi",
        "location_id": "delhi",
        "disaster_type": "ALL",
        "phone": "1078",
        "contact_number": "1078",
        "website": "https://ndma.gov.in",
        "website_url": "https://ndma.gov.in",
        "address": "NDMA Bhawan, A-1, Safdarjung Enclave, New Delhi - 110029",
        "latitude": 28.5672,
        "longitude": 77.1950,
        "source": "National Disaster Management Authority Official Portal",
        "source_url": "https://ndma.gov.in",
        "verification_status": "VERIFIED",
        "freshness": "CURRENT",
        "accessibility_notes": "24/7 central emergency operations room, toll-free accessible, bilingual Hindi/English dispatch.",
        "last_verified_at": "2026-09-12T00:00:00Z",
        "is_demo": False,
        "services": ["National Early Warnings", "SDRF/NDRF Coordination", "Disaster Guidelines"]
    },
    {
        "id": "gov-ndrf-hq",
        "name": "National Disaster Response Force (NDRF HQ)",
        "resource_type": "GOVERNMENT",
        "category": "Rescue",
        "description": "Specialized multi-disciplinary rapid disaster response force dedicated to search, rescue, flood water evacuation, and CBRN emergencies.",
        "state": "Pan-India",
        "district": "New Delhi",
        "location_id": "delhi",
        "disaster_type": "ALL",
        "phone": "011-24363260",
        "contact_number": "011-24363260 / 9711077372",
        "website": "https://www.ndrf.gov.in",
        "website_url": "https://www.ndrf.gov.in",
        "address": "6th Floor, NDCC-II Building, Jai Singh Road, New Delhi - 110001",
        "latitude": 28.6289,
        "longitude": 77.2144,
        "source": "NDRF Directorate General, Ministry of Home Affairs",
        "source_url": "https://www.ndrf.gov.in",
        "verification_status": "VERIFIED",
        "freshness": "CURRENT",
        "accessibility_notes": "16 operational battalions stationed across vulnerable regions with motorized boats and collapsed structure search equipment.",
        "last_verified_at": "2026-09-12T00:00:00Z",
        "is_demo": False,
        "services": ["Flood Water Rescue", "Earthquake Extraction", "Triage & First Aid"]
    },
    {
        "id": "gov-asdma-hq",
        "name": "Assam State Disaster Management Authority (ASDMA)",
        "resource_type": "GOVERNMENT",
        "category": "Government Relief",
        "description": "Nodal Assam state agency coordinating disaster preparedness, daily flood situation bulletins, search and rescue operations, and relief camps.",
        "state": "Assam",
        "district": "Kamrup Metro",
        "location_id": "assam",
        "disaster_type": "FLOOD",
        "phone": "1070",
        "contact_number": "1070 (Toll-Free) / 1079 / 0361-2237221",
        "website": "https://asdma.assam.gov.in",
        "website_url": "https://asdma.assam.gov.in",
        "address": "Janata Bhawan, Secretariat Complex, Dispur, Guwahati, Assam - 781006",
        "latitude": 26.1445,
        "longitude": 91.7900,
        "source": "Assam State Disaster Management Authority Official Portal",
        "source_url": "https://asdma.assam.gov.in",
        "verification_status": "VERIFIED",
        "freshness": "CURRENT",
        "accessibility_notes": "State Emergency Operations Center (SEOC) 24/7. Assamese, Bodo, Bengali, English dispatch.",
        "last_verified_at": "2026-09-12T00:00:00Z",
        "is_demo": False,
        "services": ["Flood SitRep Issuance", "Ex-Gratia Claims", "Relief Shelter Administration"]
    },
    {
        "id": "gov-hpsdma-hq",
        "name": "HP State Disaster Management Authority (HPSDMA)",
        "resource_type": "GOVERNMENT",
        "category": "Government Relief",
        "description": "Nodal agency for disaster risk reduction, hill slope geotechnical warnings, and road clearance coordination in Himachal Pradesh.",
        "state": "Himachal Pradesh",
        "district": "Shimla",
        "location_id": "himachal-pradesh",
        "disaster_type": "LANDSLIDE",
        "phone": "1070",
        "contact_number": "1070 (Toll-Free) / 0177-2629683",
        "website": "https://hpsdma.nic.in",
        "website_url": "https://hpsdma.nic.in",
        "address": "Armsdale Building, HP Secretariat, Chotta Shimla, HP - 171002",
        "latitude": 31.0991,
        "longitude": 77.1812,
        "source": "HP State Disaster Management Authority Official Portal",
        "source_url": "https://hpsdma.nic.in",
        "verification_status": "VERIFIED",
        "freshness": "CURRENT",
        "accessibility_notes": "SEOC Shimla operates round the clock with satellite backup link.",
        "last_verified_at": "2026-09-12T00:00:00Z",
        "is_demo": False,
        "services": ["Landslide Slope Early Warning", "Highway Transit Advisories", "Mountain Search Coordination"]
    },
    {
        "id": "gov-osdma-hq",
        "name": "Odisha State Disaster Management Authority (OSDMA)",
        "resource_type": "GOVERNMENT",
        "category": "Government Relief",
        "description": "Apex Odisha government authority pioneering community-based cyclone preparedness, multi-purpose cyclone shelter networks, and early warning dissemination.",
        "state": "Odisha",
        "district": "Khordha",
        "location_id": "odisha",
        "disaster_type": "CYCLONE",
        "phone": "1070",
        "contact_number": "1070 (Toll-Free) / 0674-2395398",
        "website": "https://www.osdma.org",
        "website_url": "https://www.osdma.org",
        "address": "Rajiv Bhawan, Unit-5, Bhubaneswar, Odisha - 751001",
        "latitude": 20.2706,
        "longitude": 85.8334,
        "source": "Odisha State Disaster Management Authority Official Portal",
        "source_url": "https://www.osdma.org",
        "verification_status": "VERIFIED",
        "freshness": "CURRENT",
        "accessibility_notes": "Coastal Siren Towers, Early Warning Dissemination System (EWDS) in Odia and English.",
        "last_verified_at": "2026-09-12T00:00:00Z",
        "is_demo": False,
        "services": ["Cyclone Shelter Coordination", "Mass Evacuation Protocols", "Disaster Resilient Infrastructure"]
    },
    {
        "id": "gov-cwc-ffs",
        "name": "Central Water Commission (CWC Flood Forecast Division)",
        "resource_type": "GOVERNMENT",
        "category": "Disaster Management",
        "description": "Authoritative national river hydrological telemetry agency monitoring river water levels, gauge discharge rates, and basin-wide flood warnings across India.",
        "state": "Pan-India",
        "district": "New Delhi",
        "location_id": "delhi",
        "disaster_type": "FLOOD",
        "phone": "011-26106523",
        "contact_number": "011-26106523",
        "website": "https://ffs.india-water.gov.in",
        "website_url": "https://ffs.india-water.gov.in",
        "address": "Sewa Bhawan, R.K. Puram, New Delhi - 110066",
        "latitude": 28.5665,
        "longitude": 77.1852,
        "source": "Central Water Commission Hydrological Network",
        "source_url": "https://ffs.india-water.gov.in",
        "verification_status": "VERIFIED",
        "freshness": "CURRENT",
        "accessibility_notes": "Live public hydrological river gauge telemetry covering 332 forecasting stations nationwide.",
        "last_verified_at": "2026-09-12T00:00:00Z",
        "is_demo": False,
        "services": ["River Level Monitoring", "Inundation Forecasts", "Catchment Hydrographs"]
    },
    {
        "id": "gov-imd-hq",
        "name": "India Meteorological Department (IMD Cyclone Warning Division)",
        "resource_type": "GOVERNMENT",
        "category": "Disaster Management",
        "description": "National meteorological agency providing real-time severe weather bulletins, tropical cyclone tracks, Doppler weather radar surveillance, and heavy rainfall nowcasts.",
        "state": "Pan-India",
        "district": "New Delhi",
        "location_id": "delhi",
        "disaster_type": "CYCLONE",
        "phone": "011-24631913",
        "contact_number": "011-24631913",
        "website": "https://mausam.imd.gov.in",
        "website_url": "https://mausam.imd.gov.in",
        "address": "Mausam Bhawan, Lodhi Road, New Delhi - 110003",
        "latitude": 28.5898,
        "longitude": 77.2223,
        "source": "India Meteorological Department, Ministry of Earth Sciences",
        "source_url": "https://mausam.imd.gov.in",
        "verification_status": "VERIFIED",
        "freshness": "CURRENT",
        "accessibility_notes": "Colour-coded weather warning bulletins (Green, Yellow, Orange, Red) published every 3-6 hours.",
        "last_verified_at": "2026-09-12T00:00:00Z",
        "is_demo": False,
        "services": ["Tropical Cyclone Bulletins", "Heavy Rain Warnings", "Radar Imagery"]
    },
    {
        "id": "hl-emergency-112",
        "name": "Unified National Emergency Response System (112 India)",
        "resource_type": "HELPLINE",
        "category": "Emergency Services",
        "description": "Unified pan-India single emergency number for immediate police, fire, medical ambulance, and SDRF disaster dispatch.",
        "state": "Pan-India",
        "district": "All Districts",
        "location_id": "delhi",
        "disaster_type": "ALL",
        "phone": "112",
        "contact_number": "112",
        "website": "https://112.gov.in",
        "website_url": "https://112.gov.in",
        "address": "National Emergency Operations, Ministry of Home Affairs",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "source": "Ministry of Home Affairs Emergency Response Support System (ERSS)",
        "source_url": "https://112.gov.in",
        "verification_status": "VERIFIED",
        "freshness": "CURRENT",
        "accessibility_notes": "Toll-free 24/7/365, supports mobile SOS panic button and automated GPS caller location dispatch.",
        "last_verified_at": "2026-09-12T00:00:00Z",
        "is_demo": False,
        "services": ["Police Emergency", "Fire Emergency", "Medical Dispatch", "Disaster Rescue Request"]
    },
    {
        "id": "hl-ndma-1078",
        "name": "NDMA National Disaster Helpline (1078)",
        "resource_type": "HELPLINE",
        "category": "Emergency Services",
        "description": "Official 24/7 national disaster emergency helpline managed by the National Disaster Management Authority for emergency assistance, situation reports, and rescue coordination.",
        "state": "Pan-India",
        "district": "New Delhi",
        "location_id": "delhi",
        "disaster_type": "ALL",
        "phone": "1078",
        "contact_number": "1078",
        "website": "https://ndma.gov.in",
        "website_url": "https://ndma.gov.in",
        "address": "NDMA Bhawan, A-1 Safdarjung Enclave, New Delhi - 110029",
        "latitude": 28.5672,
        "longitude": 77.1950,
        "source": "NDMA 24/7 National Emergency Control Room",
        "source_url": "https://ndma.gov.in",
        "verification_status": "VERIFIED",
        "freshness": "CURRENT",
        "accessibility_notes": "Toll-free 24/7 accessible across all telecom networks in India.",
        "last_verified_at": "2026-09-12T00:00:00Z",
        "is_demo": False,
        "services": ["Emergency SOS", "Disaster Reporting", "NDRF Dispatch Coordination"]
    },
    {
        "id": "hl-ambulance-108",
        "name": "National Emergency Medical & Ambulance Service (108)",
        "resource_type": "HELPLINE",
        "category": "Medical Assistance",
        "description": "Rapid emergency ambulance dispatch service providing basic and advanced life support (BLS/ALS) transit during health crises and disaster trauma.",
        "state": "Pan-India",
        "district": "All Districts",
        "location_id": "delhi",
        "disaster_type": "ALL",
        "phone": "108",
        "contact_number": "108",
        "website": "https://nhm.gov.in",
        "website_url": "https://nhm.gov.in",
        "address": "National Health Mission, Ministry of Health and Family Welfare",
        "latitude": 28.6119,
        "longitude": 77.2195,
        "source": "National Health Mission Emergency Medical Service",
        "source_url": "https://nhm.gov.in",
        "verification_status": "VERIFIED",
        "freshness": "CURRENT",
        "accessibility_notes": "Toll-free 24/7 ambulance dispatch across participating Indian states.",
        "last_verified_at": "2026-09-12T00:00:00Z",
        "is_demo": False,
        "services": ["Emergency Paramedic Dispatch", "Trauma Stabilization", "Hospital Patient Transit"]
    },
    {
        "id": "ngo-ircs-hq",
        "name": "Indian Red Cross Society (Disaster Management Division)",
        "resource_type": "NGO",
        "category": "Medical Assistance",
        "description": "Statutory voluntary humanitarian organization providing emergency first aid, disaster relief kits, mobile water purification units, and blood bank coordination across 36 state branches.",
        "state": "Pan-India",
        "district": "New Delhi",
        "location_id": "delhi",
        "disaster_type": "ALL",
        "phone": "011-23716441",
        "contact_number": "011-23716441 / 011-23716442",
        "website": "https://indianredcross.org",
        "website_url": "https://indianredcross.org",
        "address": "1, Red Cross Road, New Delhi - 110001",
        "latitude": 28.6186,
        "longitude": 77.2090,
        "source": "Indian Red Cross Society Act of Parliament Charter",
        "source_url": "https://indianredcross.org",
        "verification_status": "VERIFIED",
        "freshness": "CURRENT",
        "accessibility_notes": "Operates state and district branches across Assam, Odisha, Himachal Pradesh, Kerala, Bihar, and all territories.",
        "last_verified_at": "2026-09-12T00:00:00Z",
        "is_demo": False,
        "services": ["Emergency First Aid", "Relief Kit Distribution", "Mobile Water Treatment", "Volunteer Corps"]
    },
    {
        "id": "ngo-rkm-relief",
        "name": "Ramakrishna Mission Relief and Rehabilitation Services",
        "resource_type": "NGO",
        "category": "Food & Water",
        "description": "Historic humanitarian relief organization delivering cooked meals, dry rations, drinking water pouches, medical triage camps, and temporary shelter rehabilitation in disaster areas.",
        "state": "Pan-India",
        "district": "Howrah",
        "location_id": "west-bengal",
        "disaster_type": "FLOOD",
        "phone": "033-26545700",
        "contact_number": "033-26545700",
        "website": "https://belurmath.org/relief-services",
        "website_url": "https://belurmath.org/relief-services",
        "address": "Belur Math, Howrah, West Bengal - 711202",
        "latitude": 22.6322,
        "longitude": 88.3564,
        "source": "Ramakrishna Math and Ramakrishna Mission Official Relief Wing",
        "source_url": "https://belurmath.org/relief-services",
        "verification_status": "VERIFIED",
        "freshness": "CURRENT",
        "accessibility_notes": "Active field relief operations deployed through branch centers across eastern, north-eastern, and southern flood corridors.",
        "last_verified_at": "2026-09-12T00:00:00Z",
        "is_demo": False,
        "services": ["Community Kitchen Rations", "Water Tanker Trucking", "Tarpaulin Shelter Packs"]
    },
    {
        "id": "ngo-goonj-rahat",
        "name": "Goonj (Rahat Disaster Relief Initiative)",
        "resource_type": "NGO",
        "category": "Donations / Volunteering",
        "description": "Audited non-profit mobilising material resources, dignified clothing kits, sanitary hygiene packs, and community infrastructure rehabilitation following disaster impact.",
        "state": "Pan-India",
        "district": "New Delhi",
        "location_id": "delhi",
        "disaster_type": "ALL",
        "phone": "011-26972351",
        "contact_number": "011-26972351 / 011-41401216",
        "website": "https://goonj.org",
        "website_url": "https://goonj.org",
        "address": "J-93, Sarita Vihar, New Delhi - 110076",
        "latitude": 28.5292,
        "longitude": 77.2974,
        "source": "Goonj Rahat Disaster Initiative Official Portal",
        "source_url": "https://goonj.org",
        "verification_status": "VERIFIED",
        "freshness": "CURRENT",
        "accessibility_notes": "Material collection centers in major urban hubs; verified rural community distribution network.",
        "last_verified_at": "2026-09-12T00:00:00Z",
        "is_demo": False,
        "services": ["Family Relief Kits", "Sanitary Cloth Pads", "Rural Infrastructure Rebuilding", "Material Mobilization"]
    },
    {
        "id": "ngo-akshaya-patra",
        "name": "The Akshaya Patra Foundation (Disaster Relief Feeding)",
        "resource_type": "NGO",
        "category": "Food & Water",
        "description": "Large-scale humanitarian feeding foundation deploying centralized mega-kitchens and mobile food vans to provide nutritious cooked meals and emergency ration kits to flood and cyclone evacuees.",
        "state": "Pan-India",
        "district": "Bengaluru",
        "location_id": "karnataka",
        "disaster_type": "FLOOD",
        "phone": "1800-425-8622",
        "contact_number": "1800-425-8622 (Toll-Free)",
        "website": "https://www.akshayapatra.org",
        "website_url": "https://www.akshayapatra.org",
        "address": "Hare Krishna Hill, Chord Road, Rajajinagar, Bengaluru - 560010",
        "latitude": 13.0098,
        "longitude": 77.5511,
        "source": "The Akshaya Patra Foundation Official Relief Wing",
        "source_url": "https://www.akshayapatra.org",
        "verification_status": "VERIFIED",
        "freshness": "CURRENT",
        "accessibility_notes": "Capable of preparing 50,000+ freshly cooked meals per day in disaster response zones in coordination with state administrations.",
        "last_verified_at": "2026-09-12T00:00:00Z",
        "is_demo": False,
        "services": ["Fresh Cooked Meals", "Dry Grocery Kits", "Safe Drinking Water"]
    },
    {
        "id": "gov-fund-pmnrf",
        "name": "Prime Minister's National Relief Fund (PMNRF)",
        "resource_type": "GOVERNMENT",
        "category": "Donations / Volunteering",
        "description": "Authoritative national government relief trust providing financial assistance to victims of major natural calamities and bereaved families across India.",
        "state": "Pan-India",
        "district": "New Delhi",
        "location_id": "delhi",
        "disaster_type": "ALL",
        "phone": "011-23012312",
        "contact_number": "011-23012312",
        "website": "https://pmnrf.gov.in",
        "website_url": "https://pmnrf.gov.in",
        "address": "Prime Minister's Office, South Block, New Delhi - 110011",
        "latitude": 28.6143,
        "longitude": 77.2023,
        "source": "Prime Minister's Office Official Portal",
        "source_url": "https://pmnrf.gov.in",
        "verification_status": "VERIFIED",
        "freshness": "CURRENT",
        "accessibility_notes": "Donate via official organization: 100% tax exempt under Section 80G. Direct government payment gateway only.",
        "last_verified_at": "2026-09-12T00:00:00Z",
        "is_demo": False,
        "services": ["Ex-Gratia Relief Grants", "Calamity Relief Financial Aid"]
    },
    {
        "id": "gov-fund-cmrf-assam",
        "name": "Chief Minister's Relief Fund - Assam (CMRF Assam)",
        "resource_type": "GOVERNMENT",
        "category": "Donations / Volunteering",
        "description": "Official Assam state government relief fund dedicated to mitigating distress caused by monsoonal floods, river erosion, and landslides in Assam.",
        "state": "Assam",
        "district": "Kamrup Metro",
        "location_id": "assam",
        "disaster_type": "FLOOD",
        "phone": "0361-2237054",
        "contact_number": "0361-2237054",
        "website": "https://cm.assam.gov.in",
        "website_url": "https://cm.assam.gov.in",
        "address": "Chief Minister's Secretariat, Dispur, Guwahati - 781006",
        "latitude": 26.1445,
        "longitude": 91.7900,
        "source": "Government of Assam Official Secretariat Portal",
        "source_url": "https://cm.assam.gov.in",
        "verification_status": "VERIFIED",
        "freshness": "CURRENT",
        "accessibility_notes": "Donate via official organization: Direct state treasury portal for Assam flood victims. Verified bank account IFSC listed on official .gov.in domain.",
        "last_verified_at": "2026-09-12T00:00:00Z",
        "is_demo": False,
        "services": ["State Flood Relief Ex-Gratia", "Rehabilitation Housing Aid"]
    },
    {
        "id": "gov-vol-aapda-mitra",
        "name": "NDMA Aapda Mitra Community Volunteer Scheme",
        "resource_type": "GOVERNMENT",
        "category": "Donations / Volunteering",
        "description": "Central government scheme training 100,000 community volunteers in disaster-prone districts with basic skills in search, flood rescue, first aid, and evacuation logistics.",
        "state": "Pan-India",
        "district": "New Delhi",
        "location_id": "delhi",
        "disaster_type": "ALL",
        "phone": "1078",
        "contact_number": "1078",
        "website": "https://ndma.gov.in/Governance/Aapda-Mitra",
        "website_url": "https://ndma.gov.in/Governance/Aapda-Mitra",
        "address": "NDMA Bhawan, Safdarjung Enclave, New Delhi - 110029",
        "latitude": 28.5672,
        "longitude": 77.1950,
        "source": "NDMA Community Volunteer Training Initiative",
        "source_url": "https://ndma.gov.in",
        "verification_status": "VERIFIED",
        "freshness": "CURRENT",
        "accessibility_notes": "Official citizen volunteer enrollment through District Disaster Management Authorities (DDMAs).",
        "last_verified_at": "2026-09-12T00:00:00Z",
        "is_demo": False,
        "services": ["Community First Responder Training", "Flood Evacuation Support", "Shelter Line Marshals"]
    }
]



VALID_INDIAN_STATES = {
    "andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh", "goa", "gujarat",
    "haryana", "himachal pradesh", "jharkhand", "karnataka", "kerala", "madhya pradesh",
    "maharashtra", "manipur", "meghalaya", "mizoram", "nagaland", "odisha", "punjab",
    "rajasthan", "sikkim", "tamil nadu", "telangana", "tripura", "uttar pradesh", "uttarakhand",
    "west bengal", "delhi", "jammu and kashmir", "ladakh", "puducherry", "chandigarh",
    "andaman and nicobar", "dadra and nagar haveli", "daman and diu", "lakshadweep", "pan-india", "india"
}

VALID_HAZARDS = {"flood", "cyclone", "landslide", "earthquake", "heatwave", "all", "all hazards", "waterlogging / flood", "cyclone / flood"}

class ResourceService:
    @staticmethod
    def get_resources(
        db: Optional[Session] = None,
        location: Optional[str] = None,
        state: Optional[str] = None,
        district: Optional[str] = None,
        resource_type: Optional[str] = None,
        category: Optional[str] = None,
        disaster_type: Optional[str] = None,
        verification_status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves verified disaster relief resources with robust multi-parameter filtering.
        Returns strictly verified authoritative entities.
        """
        results = list(VERIFIED_RESOURCES_REGISTRY)

        # Location / State filter
        loc_filter = (state or location or "").lower().strip()
        if loc_filter and loc_filter != "all":
            is_valid_loc = (
                loc_filter in VALID_INDIAN_STATES or
                any(loc_filter in r["state"].lower() or (r.get("district") and loc_filter in r["district"].lower()) for r in VERIFIED_RESOURCES_REGISTRY)
            )
            if not is_valid_loc:
                return []

            results = [
                r for r in results
                if loc_filter in r["state"].lower() or 
                   r["state"].lower() == "pan-india" or 
                   (r.get("district") and loc_filter in r["district"].lower()) or
                   (r.get("location_id") and loc_filter == r["location_id"].lower())
            ]

        # District filter
        if district and district.lower().strip() != "all":
            d_clean = district.lower().strip()
            results = [
                r for r in results
                if (r.get("district") and d_clean in r["district"].lower()) or
                   r["state"].lower() == "pan-india" or
                   r.get("district") == "All Districts"
            ]

        # Resource Type filter (e.g. GOVERNMENT, NGO, HELPLINE)
        if resource_type and resource_type.upper().strip() != "ALL":
            rt_clean = resource_type.upper().strip()
            results = [r for r in results if r["resource_type"].upper() == rt_clean]

        # Category filter (e.g. "Medical Assistance", "Food & Water", "Rescue")
        if category and category.upper().strip() != "ALL":
            cat_clean = category.lower().strip()
            results = [
                r for r in results
                if cat_clean in r.get("category", "").lower() or
                   any(cat_clean in s.lower() for s in r.get("services", []))
            ]

        # Disaster Type filter (e.g. FLOOD, CYCLONE, LANDSLIDE, ALL)
        if disaster_type and disaster_type.upper().strip() != "ALL":
            dt_clean = disaster_type.lower().strip()
            if dt_clean not in VALID_HAZARDS:
                return []
            results = [
                r for r in results
                if r.get("disaster_type", "ALL").lower() in ["all", "all hazards", dt_clean]
            ]

        # Verification Status filter
        if verification_status and verification_status.upper().strip() != "ALL":
            vs_clean = verification_status.upper().strip()
            results = [r for r in results if r.get("verification_status", "").upper() == vs_clean]

        return results

    @staticmethod
    def get_resource_by_id(resource_id: str) -> Optional[Dict[str, Any]]:
        for r in VERIFIED_RESOURCES_REGISTRY:
            if r["id"] == resource_id:
                return r
        return None

resource_service = ResourceService()
