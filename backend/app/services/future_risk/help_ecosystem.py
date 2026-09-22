"""
RISK // INDIA — Help Ecosystem (I Need Help & I Want To Help Framework)
======================================================================
Unified assistance architecture connecting citizens with verified government dispatch,
relief camps, statutory disaster relief funds, and anti-fraud volunteer networks.
"""

from typing import Dict, List, Any, Optional
from app.services.resource_service import ResourceService


VERIFIED_STATUTORY_FUNDS = [
    {
        "name": "Prime Minister's National Relief Fund (PMNRF)",
        "entity": "Prime Minister's Office, Government of India",
        "portal_url": "https://pmnrf.gov.in",
        "tax_exemption": "100% Tax Exempt under Section 80G of Income Tax Act",
        "verification_status": "STATUTORY_CENTRAL_GOVERNMENT",
        "scope": "Pan-India Natural Calamities & Bereaved Relief"
    },
    {
        "name": "Chief Minister's Relief Fund — Assam (CMRF Assam)",
        "entity": "Government of Assam Secretariat",
        "portal_url": "https://cm.assam.gov.in",
        "tax_exemption": "100% Tax Exempt under Section 80G",
        "verification_status": "STATUTORY_STATE_GOVERNMENT",
        "scope": "Brahmaputra Flood Relief & Rehabilitation"
    },
    {
        "name": "State Disaster Response Funds (SDRF)",
        "entity": "Respective State Disaster Management Authorities",
        "portal_url": "https://ndma.gov.in/Governance/SDRF",
        "tax_exemption": "Statutory Treasury Accounts",
        "verification_status": "STATUTORY_STATE_GOVERNMENT",
        "scope": "Immediate Search, Rescue, and Relief Operations"
    }
]

VERIFIED_VOLUNTEER_NETWORKS = [
    {
        "name": "NDMA Aapda Mitra Community Volunteer Scheme",
        "entity": "National Disaster Management Authority (NDMA)",
        "portal_url": "https://ndma.gov.in/Governance/Aapda-Mitra",
        "role": "Certified Community First Responder Training (Flood Rescue, Evacuation Logistics, First Aid)",
        "verification_status": "STATUTORY_CENTRAL_GOVERNMENT"
    },
    {
        "name": "Indian Red Cross Society (IRCS) Disaster Response Team",
        "entity": "Indian Red Cross Society Statutory Body",
        "portal_url": "https://indianredcross.org",
        "role": "Emergency First Aid, Community Blood Banks, and Relief Camp Logistics",
        "verification_status": "VERIFIED_STATUTORY_HUMANITARIAN"
    },
    {
        "name": "Civil Defence Corps India",
        "entity": "Ministry of Home Affairs, Directorate General of Fire Services, Civil Defence & Home Guards",
        "portal_url": "https://dgfscdhg.gov.in",
        "role": "Community Siren Warning, Evacuation Marshaling, Shelter Management",
        "verification_status": "STATUTORY_GOVERNMENT"
    }
]

NATIONAL_EMERGENCY_DISPATCH = [
    {"service": "National Emergency Unified Response Support System (ERSS)", "number": "112", "toll_free": True, "coverage": "Pan-India 24/7/365"},
    {"service": "NDMA National Disaster Control Room", "number": "1078", "toll_free": True, "coverage": "National Multi-Agency Coordination"},
    {"service": "State Disaster Emergency Operations Centre (SEOC)", "number": "1070", "toll_free": True, "coverage": "State Relief Commissioners"},
    {"service": "District Disaster Emergency Operations Centre (DEOC)", "number": "1077", "toll_free": True, "coverage": "District Collectors & DDMAs"},
    {"service": "National Emergency Ambulance & Paramedic Transit", "number": "108", "toll_free": True, "coverage": "Pan-India Emergency Health Dispatch"},
    {"service": "Fire & Rescue Service Command", "number": "101", "toll_free": True, "coverage": "Urban and Rural Fire / Collapsed Structure Search"},
    {"service": "Police Emergency Dispatch", "number": "100", "toll_free": True, "coverage": "Immediate Law Enforcement & Traffic Evacuation"}
]


class HelpEcosystem:
    """Manages verified emergency assistance routing and community contribution channels."""

    def get_assistance_directory(self, state: Optional[str] = None) -> Dict[str, Any]:
        """Returns verified resources for both victims ('I Need Help') and helpers ('I Want To Help')."""
        state_resources = []
        if state:
            state_resources = ResourceService.get_resources(state=state)
        else:
            state_resources = ResourceService.get_resources(state="Pan-India")

        return {
            "title": "RISK // INDIA National Verified Help Ecosystem",
            "anti_fraud_notice": "Only statutory government trusts (.gov.in) and verified disaster authorities are listed. Never transfer relief funds to unverified personal UPI handles.",
            "i_need_help": {
                "headline": "Emergency Response, Rescue & Medical Dispatch",
                "emergency_numbers": NATIONAL_EMERGENCY_DISPATCH,
                "verified_facilities_count": len(state_resources),
                "verified_facilities": state_resources[:10]
            },
            "i_want_to_help": {
                "headline": "Statutory Donation Channels & Certified Volunteer Networks",
                "statutory_relief_funds": VERIFIED_STATUTORY_FUNDS,
                "certified_volunteer_schemes": VERIFIED_VOLUNTEER_NETWORKS
            }
        }


help_ecosystem = HelpEcosystem()
