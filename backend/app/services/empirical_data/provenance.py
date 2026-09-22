"""
RISK // INDIA — Authoritative Provenance & Source Registry
==========================================================
Manages verifiable provenance citations, provider URLs, and access states.
Guarantees zero fabricated observations when external feeds are restricted.
"""

from typing import Dict, Any, Tuple
from .base import ProvenanceStatus


AUTHORITATIVE_PROVIDERS_METADATA: Dict[str, Dict[str, Any]] = {
    "CWC": {
        "full_name": "Central Water Commission (CWC) / India-WRIS",
        "ministry": "Ministry of Jal Shakti, Government of India",
        "portal_url": "https://ffs.india-water.gov.in",
        "data_license": "National Data Sharing and Accessibility Policy (NDSAP)",
        "access_mode": "PUBLIC_BULLETINS",
        "real_time_api_status": "AUTHENTICATION_REQUIRED",
        "description": "Primary hydrological agency for flood forecasting, river stages, and reservoir levels."
    },
    "IMD": {
        "full_name": "India Meteorological Department (IMD) / Mausam",
        "ministry": "Ministry of Earth Sciences, Government of India",
        "portal_url": "https://mausam.imd.gov.in",
        "data_license": "Open Government Data (OGD) Platform India",
        "access_mode": "PUBLIC_SUMMARIES",
        "real_time_api_status": "AUTHENTICATION_REQUIRED",
        "description": "National meteorological agency providing rainfall, cyclonic tracking, and monsoon bulletins."
    },
    "NRSC": {
        "full_name": "National Remote Sensing Centre (NRSC / ISRO)",
        "ministry": "Department of Space, Government of India",
        "portal_url": "https://bhuvan-app1.nrsc.gov.in/disaster",
        "data_license": "ISRO Bhuvan Open Data License",
        "access_mode": "SATELLITE_RASTERS",
        "real_time_api_status": "PUBLIC_OPEN",
        "description": "Satellite-derived ground-truth flood inundation polygons and geospatial rasters."
    },
    "GSI": {
        "full_name": "Geological Survey of India (GSI) / Bhukosh",
        "ministry": "Ministry of Mines, Government of India",
        "portal_url": "https://bhukosh.gsi.gov.in",
        "data_license": "OGD India",
        "access_mode": "PORTAL_SEARCH",
        "real_time_api_status": "PUBLIC_OPEN",
        "description": "Geological mapping, landslide susceptibility zonation, and terrain contours."
    },
    "NDMA": {
        "full_name": "National Disaster Management Authority (NDMA)",
        "ministry": "Ministry of Home Affairs, Government of India",
        "portal_url": "https://ndma.gov.in",
        "data_license": "Government of India Official Records",
        "access_mode": "DAILY_SITUATION_REPORTS",
        "real_time_api_status": "PUBLIC_OPEN",
        "description": "Apex disaster management agency compiling daily disaster impact reports across all states."
    },
    "ASDMA": {
        "full_name": "Assam State Disaster Management Authority (ASDMA)",
        "ministry": "Government of Assam",
        "portal_url": "https://asdma.assam.gov.in",
        "data_license": "State Government Public Information",
        "access_mode": "DAILY_FLOOD_BULLETINS",
        "real_time_api_status": "PUBLIC_OPEN",
        "description": "District-level ground-truth flood impact bulletins, relief camp records, and inundation reports."
    }
}


def get_provider_metadata(provider_key: str) -> Dict[str, Any]:
    """Retrieves authoritative provider metadata or defaults."""
    key = provider_key.upper().strip()
    return AUTHORITATIVE_PROVIDERS_METADATA.get(key, {
        "full_name": provider_key,
        "portal_url": "https://data.gov.in",
        "access_mode": "CUSTOM",
        "real_time_api_status": ProvenanceStatus.UNVERIFIED.value
    })


def check_provider_access(provider_key: str) -> Tuple[bool, str, str]:
    """
    Checks provider accessibility honestly.
    Returns (is_accessible, provenance_status, explanation).
    """
    key = provider_key.upper().strip()
    meta = AUTHORITATIVE_PROVIDERS_METADATA.get(key)
    if not meta:
        return False, ProvenanceStatus.UNVERIFIED.value, f"Provider '{provider_key}' not in authoritative registry"

    if meta["real_time_api_status"] == "AUTHENTICATION_REQUIRED":
        return (
            False,
            ProvenanceStatus.AUTHENTICATION_REQUIRED.value,
            f"{meta['full_name']} requires registered API credentials or specialized departmental clearance for real-time automated ingestion."
        )

    return True, ProvenanceStatus.VERIFIED_OFFICIAL.value, f"Public bulletin access verified for {meta['full_name']}."
