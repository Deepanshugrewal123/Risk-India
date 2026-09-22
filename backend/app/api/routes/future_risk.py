"""
RISK // INDIA — Future Disaster Risk Forecasting & Early Warning Endpoints
==========================================================================
Provides REST endpoints for:
- National Future Risk Overview across 36 entities (/api/future-risk)
- Regional Multi-Horizon Forecasts (/api/future-risk/{region})
- Regional Forecast Variables (/api/future-risk/{region}/forecast)
- Plain-Language Public Safety Explanations (/api/future-risk/{region}/explanation)
- Hazard-Specific Timelines (/api/future-risk/{region}/{hazard}/timeline)
- Hazard-Specific Evaluation (/api/future-risk/{region}/{hazard})
- Before / During / After Action Protocols (/api/future-risk/{region}/actions)
- Verified Assistance Ecosystem (/api/future-risk/help)
- National ML Expansion Gates (/api/future-risk/ml-expansion)
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any

from app.services.future_risk import (
    future_risk_service,
    disaster_action_engine,
    help_ecosystem,
    national_ml_expansion_gate,
    ForecastHorizon,
    ALL_FORECAST_HORIZONS
)
from app.services.national_risk.regional_baseline import regional_baseline_engine, SUPPORTED_HAZARDS

router = APIRouter(prefix="/future-risk", tags=["National Future Risk Forecasting"])


@router.get("", summary="Get national future disaster risk overview across all 36 States & UTs")
def get_national_future_risk_overview(
    hazard: Optional[str] = Query(None, description="Filter by hazard (e.g. 'FLOOD', 'CYCLONE')"),
    horizon: Optional[str] = Query(None, description="Forecast horizon: 'NOW', '0_6_HOURS', '6_24_HOURS', '1_3_DAYS', '3_7_DAYS'")
) -> Dict[str, Any]:
    """
    Returns nationwide forward disaster risk projections across all 28 States and 8 Union Territories.
    """
    if horizon and horizon.upper().strip() not in ALL_FORECAST_HORIZONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid forecast horizon '{horizon}'. Supported horizons: {', '.join(ALL_FORECAST_HORIZONS)}"
        )

    if hazard and hazard.upper().strip() not in SUPPORTED_HAZARDS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported hazard '{hazard}'. Supported hazards: {', '.join(SUPPORTED_HAZARDS)}"
        )

    return future_risk_service.get_national_future_risk_summary(hazard=hazard, horizon=horizon)


@router.get("/help", summary="Access verified assistance directory (I Need Help & I Want To Help)")
def get_assistance_ecosystem(
    state: Optional[str] = Query(None, description="Filter assistance directory by state or UT name")
) -> Dict[str, Any]:
    """
    Returns verified emergency response numbers, NDRF/SDRF headquarters, statutory calamity relief funds,
    and accredited volunteer initiatives with strict anti-fraud verification notices.
    """
    return future_risk_service.get_help_directory(state=state)


@router.get("/ml-expansion", summary="Audit 14 scientific promotion gates for priority river basins")
def get_ml_expansion_status() -> Dict[str, Any]:
    """
    Returns 14-gate scientific promotion evaluation for Brahmaputra, Ganga, Godavari, Mahanadi, and Krishna.
    """
    return future_risk_service.get_ml_expansion_status()


@router.get("/safety-guide", summary="Access extended citizen disaster safety guidance catalog")
def get_citizen_safety_guide(
    hazard: Optional[str] = Query(None, description="FLOOD, CYCLONE, HEATWAVE, SEVERE_WEATHER, LANDSLIDE, EARTHQUAKE"),
    phase: Optional[str] = Query(None, description="BEFORE, DURING, AFTER"),
    category: Optional[str] = Query(None, description="Filter by safety category"),
    priority: Optional[str] = Query(None, description="CRITICAL, HIGH, RECOMMENDED")
) -> Dict[str, Any]:
    """
    Returns comprehensive Before/During/After citizen life-safety guidance across all 6 hazards.
    Eliminates artificial 4-item limits with detailed multi-category NDMA SOP guidance.
    """
    if hazard:
        h_clean = hazard.upper().strip()
        if h_clean not in SUPPORTED_HAZARDS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported hazard '{hazard}'. Supported hazards: {', '.join(SUPPORTED_HAZARDS)}"
            )
        return future_risk_service.get_safety_guide(hazard=h_clean)

    if phase or category or priority:
        instructions = future_risk_service.get_filtered_safety_instructions(
            hazard=hazard,
            phase=phase,
            category=category,
            priority=priority
        )
        return {
            "total_items": len(instructions),
            "items": instructions,
            "synthetic_records": 0
        }

    return future_risk_service.get_safety_catalog()


@router.get("/{region}", summary="Get comprehensive future risk forecast for a specific State or UT")
def get_region_future_risk(region: str) -> Dict[str, Any]:
    """
    Returns forward risk assessments across all 6 hazards and all forecast horizons for a specific region.
    """
    profile = future_risk_service.get_region_future_risk(region)
    if not profile:
        raise HTTPException(
            status_code=404,
            detail=f"Region '{region}' not found in official Indian administrative catalog (28 States + 8 UTs)."
        )
    return profile


@router.get("/{region}/forecast", summary="Get normalized weather, hydrology, and environmental forecast variables")
def get_region_forecast_variables(region: str) -> Dict[str, Any]:
    """
    Returns normalized weather observations, forward forecasts, hydrological telemetry,
    cyclone indicators, and environmental baseline metrics with 100% provenance and zero synthetic fabrication.
    """
    variables = future_risk_service.get_region_forecast_variables(region)
    if not variables:
        raise HTTPException(
            status_code=404,
            detail=f"Region '{region}' not found in official Indian administrative catalog."
        )
    return variables


@router.get("/{region}/explanation", summary="Get plain-language public safety explanation (WHAT, WHEN, WHY, CONFIDENCE, WHAT TO DO, SOURCE)")
def get_region_public_safety_explanation(
    region: str,
    hazard: Optional[str] = Query(None, description="Filter explanation by hazard (default: highest risk hazard)"),
    district: Optional[str] = Query(None, description="Specific district for targeted advisory")
) -> Dict[str, Any]:
    """
    Translates technical hydro-meteorological indicators into clear citizen guidance answering:
    - WHAT risk is developing
    - WHEN it could increase
    - WHY (physical & official evidence)
    - CONFIDENCE level
    - WHAT TO DO (immediate life-safety actions)
    - SOURCE citations
    """
    if hazard and hazard.upper().strip() not in SUPPORTED_HAZARDS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported hazard '{hazard}'. Supported hazards: {', '.join(SUPPORTED_HAZARDS)}"
        )

    explanation = future_risk_service.get_region_explanation(region, hazard=hazard, district=district)
    if not explanation:
        raise HTTPException(
            status_code=404,
            detail=f"Region '{region}' not found in official Indian administrative catalog."
        )
    return explanation


@router.get("/{region}/actions", summary="Get Before / During / After action protocols for a region")
def get_region_action_protocols(
    region: str,
    hazard: Optional[str] = Query(None, description="Filter action protocol by specific hazard")
) -> Dict[str, Any]:
    """
    Returns life-safety action checklists partitioned into BEFORE (preparedness), DURING (immediate safety),
    and AFTER (recovery and assistance access).
    """
    actions = future_risk_service.get_region_actions(region, hazard=hazard)
    if not actions:
        raise HTTPException(
            status_code=404,
            detail=f"Region '{region}' not found in official Indian administrative catalog."
        )
    return actions


@router.get("/{region}/{hazard}/timeline", summary="Get multi-horizon step-by-step projection timeline")
def get_hazard_timeline_projection(region: str, hazard: str) -> Dict[str, Any]:
    """
    Returns step-by-step projection across all 5 horizons (NOW, 0_6_HOURS, 6_24_HOURS, 1_3_DAYS, 3_7_DAYS).
    """
    h_clean = hazard.upper().strip()
    if h_clean not in SUPPORTED_HAZARDS:
        raise HTTPException(
            status_code=400,
            detail=f"Hazard '{hazard}' is not supported. Supported hazards: {', '.join(SUPPORTED_HAZARDS)}"
        )

    timeline_data = future_risk_service.get_region_hazard_timeline(region, h_clean)
    if not timeline_data:
        raise HTTPException(
            status_code=404,
            detail=f"Region '{region}' not found in official Indian administrative catalog."
        )
    return timeline_data


@router.get("/{region}/cascading", summary="Get cascading and secondary risk intelligence for a region")
def get_region_cascading_risk(
    region: str,
    hazard: Optional[str] = Query(None, description="FLOOD, CYCLONE, HEATWAVE, SEVERE_WEATHER, LANDSLIDE, EARTHQUAKE")
) -> Dict[str, Any]:
    """
    Evaluates multi-stage consequence chains: Primary Hazard -> Physical Change -> Secondary Hazard -> Tertiary Consequences.
    Enforces honest evidence postures (LIVE_EVIDENCE, RECENT_EVIDENCE, FORECAST_AVAILABLE, BASELINE_ONLY, LIMITED_EVIDENCE, DATA_UNAVAILABLE).
    """
    if hazard and hazard.upper().strip() not in SUPPORTED_HAZARDS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported hazard '{hazard}'. Supported hazards: {', '.join(SUPPORTED_HAZARDS)}"
        )

    cascading_data = future_risk_service.get_region_cascading_risk(region, hazard=hazard)
    if not cascading_data:
        raise HTTPException(
            status_code=404,
            detail=f"Region '{region}' not found in official Indian administrative catalog."
        )
    return cascading_data


@router.get("/{region}/{hazard}/cascading", summary="Get hazard-specific cascading risk intelligence for a region")
def get_region_hazard_cascading_risk(region: str, hazard: str) -> Dict[str, Any]:
    """
    Returns hazard-specific consequence chain evaluated with real-time regional environmental context.
    """
    h_clean = hazard.upper().strip()
    if h_clean not in SUPPORTED_HAZARDS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported hazard '{hazard}'. Supported hazards: {', '.join(SUPPORTED_HAZARDS)}"
        )

    cascading_data = future_risk_service.get_region_cascading_risk(region, hazard=h_clean)
    if not cascading_data:
        raise HTTPException(
            status_code=404,
            detail=f"Region '{region}' not found in official Indian administrative catalog."
        )
    return cascading_data


@router.get("/{region}/safety-guide", summary="Get extended safety guidance contextualized for a region")
def get_region_contextualized_safety_guide(
    region: str,
    hazard: Optional[str] = Query(None, description="Optional hazard override (default: region primary hazard)")
) -> Dict[str, Any]:
    """
    Returns extended Before/During/After citizen life-safety guidance contextualized for the region.
    """
    profile = regional_baseline_engine.get_state_profile(region)
    if not profile:
        raise HTTPException(
            status_code=404,
            detail=f"Region '{region}' not found in official Indian administrative catalog."
        )

    target_hazard = hazard.upper().strip() if hazard else profile.primary_hazard
    if target_hazard not in SUPPORTED_HAZARDS:
        target_hazard = profile.primary_hazard

    guide = future_risk_service.get_safety_guide(hazard=target_hazard)
    guide["region"] = {
        "id": profile.id,
        "name": profile.name,
        "type": profile.administrative_type,
        "primary_hazard": profile.primary_hazard,
        "secondary_hazard": getattr(profile, "secondary_hazard", None)
    }
    return guide


@router.get("/{region}/{hazard}", summary="Get hazard-specific future risk projection")
def get_region_hazard_future_risk(region: str, hazard: str) -> Dict[str, Any]:
    """
    Returns detailed forward assessment for a specific state and hazard.
    """
    h_clean = hazard.upper().strip()
    if h_clean not in SUPPORTED_HAZARDS:
        raise HTTPException(
            status_code=400,
            detail=f"Hazard '{hazard}' is not supported. Supported hazards: {', '.join(SUPPORTED_HAZARDS)}"
        )

    timeline_data = future_risk_service.get_region_hazard_timeline(region, h_clean)
    if not timeline_data:
        raise HTTPException(
            status_code=404,
            detail=f"Region '{region}' not found in official Indian administrative catalog."
        )
    return timeline_data


