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
    RiskAnalyzeResponse,
    RiskSourceType,
    ScientificRiskState
)
from app.utils.risk_classifier import classify_risk_score
from app.ml.base_model import flood_model
from app.services.flood_model_service import flood_model_service
from app.services.metrics_service import metrics_collector

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

        # Phase 19: 'Why This Risk?' & Scientific Rationale Engine
        is_assam = location.id.lower() in ["assam", "as", "assam-state", "in-as"] or "assam" in location.name.lower()
        hazard_upper = (assessment.disaster_type or "FLOOD").upper()

        if is_assam:
            ml_available = True
            ml_msg = "Empirical ML prediction available via assam_flood_prototype_v1 (13 hydro-meteorological features, 32 audited observations)."
            why_risk = "Assam flood risk evaluated using regional hydro-meteorological baseline and empirical ML prototype calibration."
            methodology_str = "Brahmaputra/Barak basin hydrological monitoring and validated Random Forest classification."
            data_cat = "REGIONAL_BASELINE"
            risk_source_val = RiskSourceType.REGIONAL_BASELINE
            sci_state_val = ScientificRiskState.EMPIRICALLY_VALIDATED_ML
            m_scope_val = "Assam Brahmaputra & Barak Basins"
            ds_ver_val = "1.0.0"
            limitations_val = "Baseline risk calibrated with empirical flood prototype. Predictive ML active for flood analysis."
        else:
            ml_available = False
            ml_msg = "ML prediction is not currently available for this region. Regional baseline and official disaster intelligence are shown."
            data_cat = "REGIONAL_BASELINE"
            risk_source_val = RiskSourceType.REGIONAL_BASELINE
            sci_state_val = ScientificRiskState.BASELINE_ONLY
            m_scope_val = "National Regional Baseline (Non-ML)"
            ds_ver_val = "1.0.0-baseline"
            limitations_val = "Regional baseline derived from published NDMA vulnerability matrices and IMD/CWC climatological normals. Empirical ML models are not calibrated for this region."
            methodology_str = "Deterministic regional baseline weighting using published NDMA vulnerability matrices and IMD/CWC climatological normals."

            if "FLOOD" in hazard_upper:
                why_risk = "Regional baseline derived from historical/geographic risk indicators and CWC catchment thresholds. ML model not yet calibrated for this basin."
            elif "EARTHQUAKE" in hazard_upper or "SEISMIC" in hazard_upper:
                why_risk = "Regional seismic zoning baseline (BIS IS 1893:2016) and live USGS seismological monitoring."
            elif "CYCLONE" in hazard_upper:
                why_risk = "Coastal vulnerability index and official IMD/RSMC tropical cyclone warnings."
            elif "HEATWAVE" in hazard_upper:
                why_risk = "Regional climatological summer anomaly index and NDMA Heat Wave Action Protocol."
            elif "LANDSLIDE" in hazard_upper:
                why_risk = "Geological slope susceptibility index and official GSI LEWS / SDMA advisories."
            else:
                why_risk = "Regional baseline derived from historical and geographical risk indicators."

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
            ],
            data_category=data_cat,
            why_this_risk=why_risk,
            methodology=methodology_str,
            ml_available=ml_available,
            ml_message=ml_msg,
            hazard_scope=["FLOOD", "EARTHQUAKE", "CYCLONE", "HEATWAVE", "LANDSLIDE"],
            risk_source=risk_source_val,
            scientific_state=sci_state_val,
            model_scope=m_scope_val,
            dataset_version=ds_ver_val,
            data_freshness="LIVE",
            limitations=limitations_val
        )

    @staticmethod
    def get_all_baselines(db: Session) -> List[RiskResponse]:
        """
        Returns regional baseline risk evaluations for all monitored States and Union Territories.
        """
        locations = db.query(Location).all()
        results = []
        for loc in locations:
            resp = RiskService.get_location_risk(db, loc.id)
            if resp:
                results.append(resp)
        return results

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

        # Phase 19 & 25: Explicit classification between ML prediction and Regional Baseline fallback
        is_ml_success = (pred.get("status") == "success")
        metrics_collector.record_ml_inference(is_assam=is_ml_success, success=is_ml_success)

        if is_ml_success:
            data_cat = "ML_PREDICTION"
            risk_source_val = RiskSourceType.EMPIRICAL_ML
            sci_state_val = ScientificRiskState.EMPIRICALLY_VALIDATED_ML
            m_scope_val = "Assam Brahmaputra & Barak Basins (Prototype)"
            ds_ver_val = "1.0.0"
            why_risk = "ML prototype estimate based on the validated Assam flood model (32 audited empirical observations)."
            methodology_str = "Pre-computed Random Forest pipeline with StandardScaler and 13 physical hydro-meteorological features."
            limitations_val = "Experimental Assam flood-risk prototype based on 32 empirical observations across 3 gauge corridors. Not valid for nationwide inference."
            conf_prov_val = {
                "source": "ISRO Bhuvan Inundation Rasters + CWC Gauge Telemetry + IMD Gridded Rainfall",
                "observations_count": 32,
                "features_count": 13,
                "validation_strategy": "Leave-One-Event-Out Multievent Cross-Validation"
            }
        else:
            data_cat = "REGIONAL_BASELINE"
            risk_source_val = RiskSourceType.REGIONAL_BASELINE
            sci_state_val = ScientificRiskState.EMPIRICAL_DATA_INSUFFICIENT
            m_scope_val = "National Regional Baseline (Non-ML)"
            ds_ver_val = "1.0.0-baseline"
            why_risk = "ML prediction is not currently available for this region. Regional baseline and official disaster intelligence are shown."
            methodology_str = "Regional baseline risk assessment; empirical ML model not validated outside Assam."
            limitations_val = "AI risk analysis is currently available only for the Assam flood prototype. Regional baseline risk and official disaster intelligence are shown."
            conf_prov_val = {
                "source": "Published NDMA Vulnerability Matrices + CWC/IMD Climatological Baselines",
                "observations_count": 0,
                "features_count": 0
            }

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
            timestamp=datetime.now(timezone.utc),
            data_category=data_cat,
            why_this_risk=why_risk,
            methodology=methodology_str,
            risk_source=risk_source_val,
            scientific_state=sci_state_val,
            model_scope=m_scope_val,
            dataset_version=ds_ver_val,
            data_freshness="LIVE",
            confidence_provenance=conf_prov_val,
            limitations=limitations_val
        )

risk_service = RiskService()
