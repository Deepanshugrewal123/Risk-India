import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database.database import get_db
from app.schemas.risk import RiskResponse, RiskAnalyzeRequest, RiskAnalyzeResponse
from app.services.risk_service import risk_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/risk", tags=["Risk Intelligence"])

@router.get("/basins", summary="Get major Indian river basins catalog")
def get_risk_basins(state: Optional[str] = None):
    from app.services.geo_basin_service import geo_basin_service
    basins = geo_basin_service.get_all_basins()
    if state:
        s_clean = state.lower().strip()
        basins = [b for b in basins if any(s_clean in st.lower() for st in b.get("riparian_states", []))]
    return {
        "count": len(basins),
        "disclaimer": "Hydrological normalization only. RISK // INDIA Flood Model v1 evaluates empirical flood surcharge across basins; direct satellite ground truth is validated in the Assam corridor.",
        "basins": basins
    }

@router.get("/models", summary="List versioned hazard models")
def get_risk_models(hazard: Optional[str] = None, active_only: bool = False):
    from app.services.model_registry import model_registry
    models = model_registry.list_models(hazard=hazard, active_only=active_only)
    return {
        "count": len(models),
        "registry_status": "OPERATIONAL",
        "models": models
    }

@router.get("", summary="Get all nationwide regional baseline risk assessments")
def get_all_risk_baselines(db: Session = Depends(get_db)):
    """
    Returns nationwide baseline risk evaluations covering all monitored States and Union Territories.
    Clearly categorized as Regional Baseline Risk (distinct from ML predictions and live telemetry).
    """
    baselines = risk_service.get_all_baselines(db)
    return {
        "count": len(baselines),
        "data_category": "REGIONAL_BASELINE",
        "description": "Deterministic regional baseline weighting across Indian States and Union Territories.",
        "baselines": baselines
    }

@router.get("/{location_id}", response_model=RiskResponse, summary="Get latest risk assessment for location")
def get_risk_assessment(location_id: str, db: Session = Depends(get_db)):
    """
    Return the latest available risk assessment, risk score (0-100), provisional level,
    and associated telemetry factors for any Indian state or union territory.
    """
    result = risk_service.get_location_risk(db, location_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Risk assessment not available for location '{location_id}'"
        )
    return result

@router.post("/analyze", response_model=RiskAnalyzeResponse, summary="Execute predictive risk analysis")
def analyze_risk(request: RiskAnalyzeRequest, db: Session = Depends(get_db)):
    """
    Accept structured feature inputs (rainfall, antecedent precipitation, river water level, coordinates)
    and compute an estimated risk breakdown through the ML model service.
    """
    try:
        return risk_service.analyze_risk(db, request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid risk input: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Risk analysis engine error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during risk computation. Please retry or contact support."
        )

@router.post("/national-flood/predict", summary="Execute India-wide empirical flood ML inference (risk_india_flood_v1)")
def predict_national_flood(request: RiskAnalyzeRequest):
    """
    Executes India-Wide Flood Model v1 (risk_india_flood_v1) inference for any Indian State or Union Territory.
    Trained on 18,184 empirical IMD district observations with zero synthetic records.
    """
    from app.services.national_flood_model_service import national_flood_model_service
    return national_flood_model_service.predict(
        location_id=request.location_id,
        district=request.district,
        features=request.features,
        hazard=request.hazard or request.disaster_type or "flood"
    )

