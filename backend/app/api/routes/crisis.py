"""
RISK // INDIA — National Crisis & Emergency Assistance Routes (Phase 30E)
========================================================================
REST endpoints delivering human-first disaster assistance:
- /api/crisis/status: High-level national crisis posture and statutory helplines
- /api/crisis/national: Comprehensive 36-entity crisis overview
- /api/crisis/{region}: Region crisis assessment with what is happening & what to do now
- /api/crisis/{region}/actions: Prioritized actions and Before/During/After life safety
- /api/crisis/{region}/resources: Verified statutory emergency contacts and rescue nodes
- /api/crisis/{region}/timeline: 5-horizon projection with explicit signal provenance
- /api/crisis/{region}/explanation: Deterministic transparent explanation & data limitations
- /api/crisis/{region}/{hazard}: Hazard-specific regional crisis assessment
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone

from app.services.crisis import (
    national_crisis_service,
    CrisisAssessment,
    CrisisOperationalState
)
from app.services.national_risk.regional_baseline import SUPPORTED_HAZARDS

router = APIRouter(prefix="/crisis", tags=["National Crisis & Emergency Assistance"])


@router.get("/status", summary="Global crisis mode posture and national emergency lines")
def get_crisis_status() -> Dict[str, Any]:
    """
    Returns global operational posture, national emergency helplines,
    and summary of active crisis recommendations.
    """
    overview = national_crisis_service.get_national_crisis_overview()
    return {
        "status": "OPERATIONAL",
        "system": "RISK // INDIA National Crisis Mode",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "operational_state_distribution": overview["operational_state_distribution"],
        "crisis_recommended_count": overview["crisis_recommended_count"],
        "crisis_recommended_regions": [
            {
                "region_id": r["region_id"],
                "region_name": r["region_name"],
                "operational_state": r["operational_state"],
                "primary_hazard": r["primary_hazard"],
                "activation_reason": r["activation_reason"]
            }
            for r in overview["crisis_recommended_regions"]
        ],
        "national_emergency_helplines": {
            "all_emergencies": "112",
            "disaster_management_ndma": "1078",
            "state_disaster_helpline": "1070",
            "district_emergency_cell": "1077",
            "ambulance_medical": "108",
            "fire_rescue": "101",
            "police": "100",
            "women_safety": "1090"
        },
        "synthetic_records": 0
    }


@router.get("/national", summary="Complete 36-entity national crisis overview")
def get_national_crisis_overview() -> Dict[str, Any]:
    """
    Returns national crisis evaluation across all 28 States and 8 Union Territories.
    """
    return national_crisis_service.get_national_crisis_overview()


@router.get("/{region}/actions", summary="Prioritized human actions and Before/During/After protocols")
def get_region_actions(
    region: str,
    hazard: Optional[str] = Query(None, description="Hazard filter: FLOOD, EARTHQUAKE, CYCLONE, HEATWAVE, LANDSLIDE, SEVERE_WEATHER")
) -> Dict[str, Any]:
    """
    Returns top 3-5 prioritized immediate life safety actions, structured
    Before/During/After protocols, and 72-hour family disaster preparedness checklist.
    """
    if hazard and hazard.upper().strip() not in SUPPORTED_HAZARDS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported hazard '{hazard}'. Supported: {', '.join(SUPPORTED_HAZARDS)}"
        )
    
    assessment = national_crisis_service.assess_crisis(region_id=region, hazard=hazard)
    return {
        "region_id": assessment.region_id,
        "region_name": assessment.region_name,
        "primary_hazard": assessment.primary_hazard,
        "operational_state": assessment.operational_state.value,
        "what_to_do_now": [a.model_dump() for a in assessment.what_to_do_now],
        "action_protocols": {
            phase: [a.model_dump() for a in items]
            for phase, items in assessment.action_protocols.items()
        },
        "family_prep_checklist": [c.model_dump() for c in assessment.family_prep_checklist],
        "synthetic_records": 0
    }


@router.get("/{region}/resources", summary="Verified nearby emergency resources and helplines")
def get_region_resources(
    region: str,
    hazard: Optional[str] = Query(None, description="Hazard filter: FLOOD, EARTHQUAKE, etc."),
    lat: Optional[float] = Query(None, description="User latitude for proximity sorting"),
    lon: Optional[float] = Query(None, description="User longitude for proximity sorting")
) -> Dict[str, Any]:
    """
    Returns verified statutory emergency relief nodes, helplines, and NDRF/SDRF units.
    Strictly preserves provenance; if no local verified resource exists, explicit disclaimer is returned.
    """
    coords = (lat, lon) if (lat is not None and lon is not None) else None
    assessment = national_crisis_service.assess_crisis(
        region_id=region,
        hazard=hazard,
        coordinates=coords
    )
    return {
        "region_id": assessment.region_id,
        "region_name": assessment.region_name,
        "primary_hazard": assessment.primary_hazard,
        "emergency_resources": [r.model_dump() for r in assessment.emergency_resources],
        "resource_availability_note": assessment.resource_availability_note,
        "synthetic_records": 0
    }


@router.get("/{region}/timeline", summary="5-horizon crisis progression with signal provenance")
def get_region_timeline(
    region: str,
    hazard: Optional[str] = Query(None, description="Hazard filter: FLOOD, EARTHQUAKE, etc.")
) -> Dict[str, Any]:
    """
    Returns unified 5-horizon progression (NOW, 0_6H, 6_24H, 1_3D, 3_7D) with explicit
    provenance tags (OBSERVED, OFFICIAL_WARNING, FORECAST, BASELINE, EMPIRICAL_ML).
    """
    if hazard and hazard.upper().strip() not in SUPPORTED_HAZARDS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported hazard '{hazard}'. Supported: {', '.join(SUPPORTED_HAZARDS)}"
        )
    assessment = national_crisis_service.assess_crisis(region_id=region, hazard=hazard)
    return {
        "region_id": assessment.region_id,
        "region_name": assessment.region_name,
        "primary_hazard": assessment.primary_hazard,
        "timeline": [t.model_dump() for t in assessment.timeline],
        "synthetic_records": 0
    }


@router.get("/{region}/explanation", summary="Deterministic 'Why this risk?' explanation")
def get_region_explanation(
    region: str,
    hazard: Optional[str] = Query(None, description="Hazard filter: FLOOD, EARTHQUAKE, etc.")
) -> Dict[str, Any]:
    """
    Answers: Why this risk? What changed? Supporting evidence? What could change? What we do not know?
    """
    assessment = national_crisis_service.assess_crisis(region_id=region, hazard=hazard)
    return {
        "region_id": assessment.region_id,
        "region_name": assessment.region_name,
        "primary_hazard": assessment.primary_hazard,
        "explanation": assessment.explanation.model_dump(),
        "synthetic_records": 0
    }


@router.get("/{region}", summary="Complete regional crisis assessment")
def get_region_crisis_assessment(
    region: str,
    hazard: Optional[str] = Query(None, description="Hazard filter: FLOOD, EARTHQUAKE, etc."),
    manual: bool = Query(False, description="Manual activation toggle (Rule E)"),
    lat: Optional[float] = Query(None, description="Latitude for proximity sorting"),
    lon: Optional[float] = Query(None, description="Longitude for proximity sorting")
) -> Dict[str, Any]:
    """
    Returns complete human-first disaster assessment for any Indian State or UT:
    - Answers: What is happening? What could happen next? What should I do now?
    - Before / During / After action protocols
    - Verified emergency resources with zero synthetic data
    - 5-horizon timeline
    - Deterministic explanation & data limitations
    - Assam ML guard & Earthquake non-prediction guard preservation
    """
    if hazard and hazard.upper().strip() not in SUPPORTED_HAZARDS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported hazard '{hazard}'. Supported: {', '.join(SUPPORTED_HAZARDS)}"
        )

    coords = (lat, lon) if (lat is not None and lon is not None) else None
    assessment = national_crisis_service.assess_crisis(
        region_id=region,
        hazard=hazard,
        manual_activation=manual,
        coordinates=coords
    )

    res_dict = assessment.model_dump()
    res_dict["synthetic_records"] = 0
    return res_dict


@router.get("/{region}/{hazard}", summary="Hazard-specific regional crisis assessment")
def get_region_hazard_crisis_assessment(
    region: str,
    hazard: str,
    manual: bool = Query(False, description="Manual activation toggle"),
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude")
) -> Dict[str, Any]:
    """
    Returns crisis assessment tailored to a specific hazard for an Indian State or UT.
    """
    h_clean = hazard.upper().strip()
    if h_clean not in SUPPORTED_HAZARDS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported hazard '{hazard}'. Supported: {', '.join(SUPPORTED_HAZARDS)}"
        )

    coords = (lat, lon) if (lat is not None and lon is not None) else None
    assessment = national_crisis_service.assess_crisis(
        region_id=region,
        hazard=h_clean,
        manual_activation=manual,
        coordinates=coords
    )

    res_dict = assessment.model_dump()
    res_dict["synthetic_records"] = 0
    return res_dict
