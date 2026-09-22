"""
RISK // INDIA — National Live Disaster Intelligence & Unified Risk Presentation Endpoints
========================================================================================
Provides unified, transparent, provenance-aware risk intelligence for all 28 States and 8 Union Territories
across all 6 core hazards (FLOOD, EARTHQUAKE, CYCLONE, HEATWAVE, LANDSLIDE, SEVERE_WEATHER).

Endpoints:
- GET /api/national-risk              - Complete nationwide summary across 36 entities
- GET /api/national-risk/freshness    - Audit of data freshness and distribution
- GET /api/national-risk/providers    - Provider operational status & circuit breakers
- GET /api/national-risk/{region}     - Unified single-region profile with all 6 hazards
- GET /api/national-risk/{region}/{hazard} - Hazard-specific profile for a region
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any

from app.services.national_risk import (
    unified_national_risk_service,
    freshness_engine,
    regional_baseline_engine,
    SUPPORTED_HAZARDS
)

router = APIRouter(prefix="/national-risk", tags=["National Live Risk Intelligence"])


@router.get("", summary="Get unified national risk intelligence across all 36 States & UTs")
def get_national_risk_overview(
    hazard: Optional[str] = Query(None, description="Filter primary hazard (e.g. 'FLOOD', 'CYCLONE')"),
    level: Optional[str] = Query(None, description="Filter by risk level (e.g. 'HIGH', 'CRITICAL', 'MODERATE', 'LOW')"),
    status: Optional[str] = Query(None, description="Filter by overall status (e.g. 'OFFICIAL_LIVE_WARNING')")
) -> Dict[str, Any]:
    """
    Returns the comprehensive national disaster risk summary across all 28 States
    and 8 Union Territories, integrating official feeds, regional baselines, and Assam ML.
    """
    summary = unified_national_risk_service.get_national_risk_summary()
    regions = summary["regions"]

    if hazard:
        h_clean = hazard.upper().strip()
        regions = [r for r in regions if r.get("overall_risk", {}).get("primary_hazard") == h_clean]

    if level:
        lvl_clean = level.upper().strip()
        regions = [r for r in regions if r.get("overall_risk", {}).get("level") == lvl_clean]

    if status:
        st_clean = status.upper().strip()
        regions = [r for r in regions if r.get("overall_status") == st_clean]

    return {
        "count": len(regions),
        "states_covered": sum(1 for r in regions if r["region"]["type"] == "STATE"),
        "union_territories_covered": sum(1 for r in regions if r["region"]["type"] == "UNION_TERRITORY"),
        "total_administrative_entities": len(regions),
        "supported_hazards": SUPPORTED_HAZARDS,
        "synthetic_records": 0,
        "freshness_policy": "Freshness is evaluated independently from risk severity; zero synthetic data",
        "national_ml_scope": summary["national_ml_scope"],
        "regions": regions
    }


@router.get("/freshness", summary="Get nationwide data freshness and distribution audit")
def get_national_freshness_audit() -> Dict[str, Any]:
    """
    Returns nationwide audit of data freshness across live feeds, baselines, and ML models.
    Freshness is classified independently from risk severity.
    """
    return unified_national_risk_service.get_freshness_report()


@router.get("/providers", summary="Get live upstream disaster data providers health and circuit breaker status")
def get_providers_health() -> Dict[str, Any]:
    """
    Returns real-time health, response status, and circuit breaker states for all upstream providers
    (USGS, CWC, IMD, GSI). Enforces independent provider fault isolation.
    """
    return unified_national_risk_service.get_providers_health_report()


@router.get("/{region}", summary="Get unified risk profile for a specific State or Union Territory")
def get_region_risk_profile(region: str) -> Dict[str, Any]:
    """
    Returns normalized intelligence for a specific Indian State or UT:
    - All 6 hazard profiles
    - Active official warnings
    - Regional baseline vulnerability
    - Empirical ML status (Assam prototype only; transparent limitation for other states)
    - Verified emergency resources
    - Deterministic freshness and provenance
    - Upstream provider health
    """
    profile = unified_national_risk_service.get_state_risk(region)
    if not profile:
        raise HTTPException(
            status_code=404,
            detail=f"Region '{region}' not found in official Indian administrative catalog (28 States + 8 UTs)."
        )
    return profile


@router.get("/{region}/{hazard}", summary="Get hazard-specific intelligence for a State or UT")
def get_region_hazard_profile(region: str, hazard: str) -> Dict[str, Any]:
    """
    Returns hazard-specific intelligence for a single state and hazard type.
    """
    h_clean = hazard.upper().strip()
    if h_clean not in SUPPORTED_HAZARDS:
        raise HTTPException(
            status_code=400,
            detail=f"Hazard '{hazard}' is not supported. Supported hazards: {', '.join(SUPPORTED_HAZARDS)}"
        )

    profile = unified_national_risk_service.get_state_hazard_risk(region, h_clean)
    if not profile:
        raise HTTPException(
            status_code=404,
            detail=f"Region '{region}' not found in official Indian administrative catalog."
        )
    return profile
