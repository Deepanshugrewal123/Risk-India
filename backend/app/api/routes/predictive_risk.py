"""
RISK // INDIA — National Predictive Risk Fusion REST Endpoints (Phase 30F)
==========================================================================
Exposes unified predictive risk fusion, 5-horizon timelines, scenarios,
early warning decision support, and 12-question citizen safety intelligence
across all 36 States and Union Territories.
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Query, Path, HTTPException

from app.services.predictive_risk import (
    national_predictive_risk_service,
    PredictiveRiskAssessment,
    NationalPredictiveOverview,
    PredictiveTimelinePoint,
    PredictionExplanation,
    PredictiveScenario,
    EarlyWarningAssessment
)

router = APIRouter(prefix="/predictive-risk", tags=["National Predictive Risk Fusion"])


@router.get("/national", response_model=NationalPredictiveOverview)
def get_national_overview() -> NationalPredictiveOverview:
    """Returns comprehensive national predictive posture covering all 36 Indian entities."""
    return national_predictive_risk_service.get_national_overview()


@router.get("/trends")
def get_national_trends() -> Dict[str, Any]:
    """Returns directional risk momentum (RISING, STABLE, DECLINING, VOLATILE) for all 36 entities."""
    return national_predictive_risk_service.get_trends()


@router.get("/readiness")
def get_national_readiness() -> Dict[str, Any]:
    """Returns entities requiring active preparation or evacuation readiness."""
    return national_predictive_risk_service.get_readiness()


@router.get("/providers")
def get_authoritative_providers() -> List[Dict[str, Any]]:
    """Returns status and catalogs of authoritative upstream scientific providers."""
    return national_predictive_risk_service.get_providers()


@router.get("/{region}/timeline", response_model=List[PredictiveTimelinePoint])
def get_region_timeline(
    region: str = Path(..., description="State or Union Territory identifier or name"),
    hazard: Optional[str] = Query(None, description="FLOOD, CYCLONE, HEATWAVE, SEVERE_WEATHER, LANDSLIDE, EARTHQUAKE")
) -> List[PredictiveTimelinePoint]:
    """Returns 5-horizon predictive timeline points across NOW, 0-6h, 6-24h, 1-3d, and 3-7d."""
    return national_predictive_risk_service.get_timeline(region, hazard)


@router.get("/{region}/explanation", response_model=PredictionExplanation)
def get_region_explanation(
    region: str = Path(..., description="State or Union Territory identifier or name"),
    hazard: Optional[str] = Query(None, description="FLOOD, CYCLONE, HEATWAVE, SEVERE_WEATHER, LANDSLIDE, EARTHQUAKE")
) -> PredictionExplanation:
    """Returns transparent explanation dimensions and direct answers to all 12 citizen safety questions."""
    return national_predictive_risk_service.get_explanation(region, hazard)


@router.get("/{region}/scenarios", response_model=List[PredictiveScenario])
def get_region_scenarios(
    region: str = Path(..., description="State or Union Territory identifier or name"),
    hazard: Optional[str] = Query(None, description="FLOOD, CYCLONE, HEATWAVE, SEVERE_WEATHER, LANDSLIDE, EARTHQUAKE")
) -> List[PredictiveScenario]:
    """Returns Baseline, Likely, and Escalation forward-looking scenarios."""
    return national_predictive_risk_service.get_scenarios(region, hazard)


@router.get("/{region}/early-warning", response_model=EarlyWarningAssessment)
def get_region_early_warning(
    region: str = Path(..., description="State or Union Territory identifier or name"),
    hazard: Optional[str] = Query(None, description="FLOOD, CYCLONE, HEATWAVE, SEVERE_WEATHER, LANDSLIDE, EARTHQUAKE")
) -> EarlyWarningAssessment:
    """Returns progressive early-warning posture, strictly separating preparation from evacuation."""
    return national_predictive_risk_service.get_early_warning(region, hazard)


@router.get("/{region}/{hazard}", response_model=PredictiveRiskAssessment)
def get_region_hazard_assessment(
    region: str = Path(..., description="State or Union Territory identifier or name"),
    hazard: str = Path(..., description="Specific hazard: FLOOD, CYCLONE, HEATWAVE, SEVERE_WEATHER, LANDSLIDE, EARTHQUAKE")
) -> PredictiveRiskAssessment:
    """Returns complete multi-signal predictive risk assessment for a specific hazard in a region."""
    return national_predictive_risk_service.get_hazard_assessment(region, hazard)


@router.get("/{region}", response_model=PredictiveRiskAssessment)
def get_region_assessment(
    region: str = Path(..., description="State or Union Territory identifier or name"),
    hazard: Optional[str] = Query(None, description="Optional hazard override. If omitted, uses baseline primary hazard.")
) -> PredictiveRiskAssessment:
    """Returns complete multi-signal predictive risk assessment for a region."""
    return national_predictive_risk_service.get_regional_assessment(region, hazard)
