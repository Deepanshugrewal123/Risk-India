from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database.database import get_db
from app.schemas.risk import RiskResponse, RiskAnalyzeRequest, RiskAnalyzeResponse
from app.services.risk_service import risk_service

router = APIRouter(prefix="/risk", tags=["Risk Intelligence"])

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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Risk analysis engine error: {str(e)}"
        )
