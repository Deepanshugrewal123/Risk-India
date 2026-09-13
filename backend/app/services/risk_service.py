from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timezone

from app.models.location import Location
from app.models.risk_assessment import RiskAssessment
from app.models.risk_factor import RiskFactor
from app.schemas.risk import (
    RiskResponse,
    RiskAssessmentData,
    RiskFactorSchema,
    LocationSummary,
    RiskAnalyzeRequest,
    RiskAnalyzeResponse
)
from app.utils.risk_classifier import classify_risk_score
from app.ml.base_model import flood_model
from app.services.flood_model_service import flood_model_service

class RiskService:
    @staticmethod
    def get_location_risk(db: Session, location_id: str) -> Optional[RiskResponse]:
        """
        Fetch latest available risk assessment and associated factors for a location.
        """
        loc_id = location_id.lower().strip()
        location = db.query(Location).filter(
            (Location.id == loc_id) | (Location.state_code == loc_id.upper())
        ).first()

        if not location:
            return None

        # Fetch latest risk assessment for this location
        assessment = db.query(RiskAssessment).filter(
            RiskAssessment.location_id == location.id
        ).order_by(RiskAssessment.created_at.desc()).first()

        if not assessment:
            # Generate a baseline demo assessment if none in DB
            assessment = RiskAssessment(
                location_id=location.id,
                disaster_type="FLOOD",
                risk_score=50,
                risk_level=classify_risk_score(50),
                model_version="demo-v1",
                assessment_status="DEMO"
            )
            db.add(assessment)
            db.commit()
            db.refresh(assessment)

        factors = db.query(RiskFactor).filter(
            RiskFactor.assessment_id == assessment.id
        ).all()

        return RiskResponse(
            location=LocationSummary(id=location.id, name=location.name),
            assessment=RiskAssessmentData(
                id=assessment.id,
                disaster_type=assessment.disaster_type,
                risk_score=assessment.risk_score,
                risk_level=assessment.risk_level,
                model_version=assessment.model_version,
                status=assessment.assessment_status,
                created_at=assessment.created_at
            ),
            risk_factors=[
                RiskFactorSchema(
                    id=f.id,
                    factor_name=f.factor_name,
                    factor_value=f.factor_value,
                    importance=f.importance,
                    unit=f.unit
                )
                for f in factors
            ]
        )

    @staticmethod
    def analyze_risk(db: Session, request: RiskAnalyzeRequest) -> RiskAnalyzeResponse:
        """
        Accept structured feature inputs and execute flood prototype ML prediction.
        Delegates prediction calculation directly to flood_model_service.
        """
        loc_id = request.location_id.lower().strip()
        location = None
        if db is not None:
            location = db.query(Location).filter(
                (Location.id == loc_id) | (Location.state_code == loc_id.upper())
            ).first()

        hazard = request.hazard or request.disaster_type or "flood"

        # Execute prediction via dedicated ML inference service
        pred = flood_model_service.predict(
            location_id=request.location_id,
            district=request.district,
            features=request.features,
            hazard=hazard
        )

        top_factors = pred.get("top_factors", [])
        risk_factors = [
            RiskFactorSchema(
                factor_name=f.get("display_label", f.get("feature")),
                factor_value=str(f.get("value", "")),
                importance="High" if abs(f.get("contribution", 0)) > 0.4 else "Medium",
                unit=None
            )
            for f in top_factors
        ]

        primary_driver = top_factors[0]["display_label"] if top_factors else "Antecedent Precipitation Influx"

        return RiskAnalyzeResponse(
            status=pred.get("status", "success"),
            message=pred.get("message"),
            location_id=pred.get("location_id", request.location_id),
            district=pred.get("district", request.district),
            state=pred.get("state", "Assam" if pred.get("status") == "success" else None),
            hazard=hazard,
            disaster_type=hazard,
            model_version=pred.get("model_version", "assam_flood_prototype_v1"),
            flood_probability=pred.get("flood_probability"),
            probability=pred.get("flood_probability"),
            risk_score=pred.get("risk_score"),
            risk_level=pred.get("risk_level"),
            top_factors=top_factors,
            risk_factors=risk_factors,
            is_prototype=pred.get("is_prototype", True),
            emergency_warning=pred.get("emergency_warning", False),
            primary_driver=primary_driver,
            recommended_action=pred.get("recommended_action"),
            recommended_immediate_action=pred.get("recommended_action"),
            disclaimer=pred.get(
                "disclaimer",
                "Experimental Assam flood-risk prototype based on a limited event dataset. "
                "Results are for research and awareness only and should not replace official emergency warnings."
            ),
            timestamp=datetime.now(timezone.utc)
        )

risk_service = RiskService()
