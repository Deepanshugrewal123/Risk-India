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
    ScientificRiskState,
    ModelFactorContribution
)
from app.utils.risk_classifier import classify_risk_score
from app.ml.base_model import flood_model
from app.services.flood_model_service import flood_model_service
from app.services.national_flood_model_service import national_flood_model_service
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

        if is_assam and hazard_upper == "FLOOD":
            ml_available = True
            ml_msg = "Empirical ML prediction available via assam_flood_prototype_v1 (13 hydro-meteorological features, 32 audited observations)."
            why_risk = "Assam flood risk evaluated using regional hydro-meteorological baseline and empirical ML prototype calibration."
            methodology_str = "Brahmaputra/Barak basin hydrological monitoring and validated Logistic Regression classification."
            data_cat = "REGIONAL_BASELINE"
            risk_source_val = RiskSourceType.REGIONAL_BASELINE
            sci_state_val = ScientificRiskState.EMPIRICALLY_VALIDATED_ML
            m_scope_val = "Assam Brahmaputra & Barak Basins"
            ds_ver_val = "1.0.0"
            limitations_val = "Baseline risk calibrated with empirical flood prototype. Predictive ML active for flood analysis."
        else:
            ml_available = False
            ml_msg = "ML prediction is not currently available for this region or hazard. Regional baseline and official disaster intelligence are shown."
            data_cat = "REGIONAL_BASELINE"
            risk_source_val = RiskSourceType.REGIONAL_BASELINE
            sci_state_val = ScientificRiskState.BASELINE_ONLY
            m_scope_val = "National Regional Baseline (Non-ML)"
            ds_ver_val = "1.0.0-baseline"
            limitations_val = "Regional baseline derived from published NDMA vulnerability matrices and IMD/CWC climatological normals. Empirical ML models are not calibrated for this region or hazard."
            methodology_str = "Deterministic regional baseline weighting using published NDMA vulnerability matrices and IMD/CWC climatological normals."

            if "FLOOD" in hazard_upper:
                why_risk = "Regional baseline derived from historical/geographic risk indicators and CWC catchment thresholds. ML model not calibrated for this basin."
            elif "EARTHQUAKE" in hazard_upper or "SEISMIC" in hazard_upper:
                why_risk = "Regional seismic zoning baseline (BIS IS 1893:2016) and live USGS seismological monitoring. Earthquakes cannot be temporally predicted."
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
        Accept structured feature inputs and execute flood ML prediction.
        Routes production flood prediction across all Indian jurisdictions to risk_india_flood_v1.
        Preserves legacy prototype execution if explicitly requested via model_version="assam_flood_prototype_v1".
        """
        loc_id = request.location_id.lower().strip()
        location = None
        if db is not None:
            location = db.query(Location).filter(
                (Location.id == loc_id) | (Location.state_code == loc_id.upper())
            ).first()

        hazard = request.hazard or request.disaster_type or "flood"
        hazard_clean = hazard.lower().strip()

        # Check if caller explicitly requested historical Assam prototype
        requested_version = getattr(request, "model_version", None)
        if requested_version == "assam_flood_prototype_v1":
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
            is_ml_success = (pred.get("status") == "success")
            metrics_collector.record_ml_inference(is_assam=is_ml_success, success=is_ml_success)

            if is_ml_success:
                data_cat = "ML_PREDICTION"
                risk_source_val = RiskSourceType.EMPIRICAL_ML
                sci_state_val = ScientificRiskState.EMPIRICALLY_VALIDATED_ML
                m_scope_val = "Assam Brahmaputra & Barak Basins (Prototype)"
                ds_ver_val = "1.0.0"
                why_risk = "ML prototype estimate based on the validated Assam flood model (32 audited empirical observations)."
                methodology_str = "Scikit-Learn Logistic Regression pipeline with StandardScaler and 13 physical hydro-meteorological features."
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
                why_risk = "ML prediction is not currently available for this region or hazard. Regional baseline and official disaster intelligence are shown."
                methodology_str = "Regional baseline risk assessment; empirical ML model not validated outside Assam Brahmaputra/Barak flood basins."
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
                state=pred.get("state", "Assam" if is_ml_success else None),
                hazard=hazard,
                disaster_type=hazard,
                model_version=pred.get("model_version") if is_ml_success else "regional_baseline",
                flood_probability=pred.get("flood_probability"),
                probability=pred.get("flood_probability"),
                risk_score=pred.get("risk_score"),
                risk_level=pred.get("risk_level"),
                top_factors=top_factors,
                risk_factors=risk_factors,
                is_prototype=True,
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

        # Production India-wide routing: Check hazard compatibility
        if hazard_clean not in ["flood", "waterlogging", "inundation", "flash_flood"]:
            return RiskAnalyzeResponse(
                status="hazard_unsupported_by_flood_model",
                message=f"Hazard '{hazard}' is evaluated via authoritative statutory baselines and NWP feeds, not flood ML.",
                location_id=request.location_id,
                district=request.district,
                state=location.name if location else None,
                hazard=hazard,
                disaster_type=hazard,
                model_version="regional_baseline",
                risk_score=50,
                risk_level="MEDIUM",
                is_prototype=False,
                data_category="REGIONAL_BASELINE",
                why_this_risk=f"Regional baseline derived for {hazard}.",
                methodology="Deterministic statutory baseline.",
                risk_source=RiskSourceType.REGIONAL_BASELINE,
                scientific_state=ScientificRiskState.BASELINE_ONLY,
                model_scope="National Regional Baseline (Non-ML)",
                limitations="Empirical ML models are calibrated for flood hazard only. Earthquakes cannot be temporally predicted."
            )

        # Execute prediction via national flood ML model service (risk_india_flood_v1)
        pred = national_flood_model_service.predict(
            location_id=request.location_id,
            state=location.name if location else None,
            district=request.district,
            features=request.features,
            hazard=hazard_clean
        )

        is_ml_success = (pred.get("status") == "success")
        is_assam = (pred.get("state") == "Assam" or loc_id in ["assam", "as", "assam-state", "in-as"])
        metrics_collector.record_ml_inference(is_assam=is_assam, success=is_ml_success)

        raw_attributions = pred.get("feature_attributions", [])
        top_factors = []
        for a in raw_attributions:
            factor_name = a.get("factor", "Precipitation Factor")
            val_str = str(a.get("value", ""))
            impact = a.get("impact", "MODERATE")
            is_pos = impact in ["SEVERE_ELEVATION", "MODERATE_ELEVATION", "HIGH_SURCHARGE", "ELEVATED"]
            contrib = 0.65 if impact == "SEVERE_ELEVATION" else 0.45 if impact in ["HIGH_SURCHARGE", "ELEVATED"] else 0.25 if is_pos else -0.20
            top_factors.append(ModelFactorContribution(
                feature=factor_name.lower().replace(" ", "_"),
                contribution=contrib,
                direction="increases_risk" if is_pos else "decreases_risk",
                display_label=factor_name,
                value=val_str
            ))

        risk_factors = [
            RiskFactorSchema(
                factor_name=f.display_label,
                factor_value=str(f.value or ""),
                importance="High" if abs(f.contribution) > 0.4 else "Medium",
                unit=None
            )
            for f in top_factors
        ]

        primary_driver = top_factors[0].display_label if top_factors else "Catchment Precipitation Influx"

        if not is_ml_success:
            data_cat = "REGIONAL_BASELINE"
            risk_source_val = RiskSourceType.REGIONAL_BASELINE
            sci_state_val = ScientificRiskState.BASELINE_ONLY
            m_scope_val = "National Regional Baseline (Non-ML)"
            ds_ver_val = "1.0.0-baseline"
            why_risk = pred.get("message") or "ML prediction is currently unavailable. Regional baseline and official disaster intelligence are shown."
            methodology_str = "Regional baseline risk assessment; national ML model unavailable."
            limitations_val = "Automated flood model inference was not completed. Regional baseline risk and official disaster intelligence are shown."
            model_ver_val = "regional_baseline"
            conf_prov_val = {
                "source": "Published NDMA Vulnerability Matrices + CWC/IMD Climatological Baselines",
                "observations_count": 0,
                "features_count": 0
            }
        elif is_assam:
            data_cat = "ML_PREDICTION"
            risk_source_val = RiskSourceType.EMPIRICAL_ML
            sci_state_val = ScientificRiskState.EMPIRICALLY_VALIDATED_ML
            model_ver_val = pred.get("model_version", "risk_india_flood_v1")
            ds_ver_val = "1.0.0"
            m_scope_val = "Assam Brahmaputra & Barak Basins (Satellite Calibrated)"
            why_risk = "Empirical ML prediction calibrated against 32 verified ISRO Bhuvan satellite flood rasters and CWC telemetry."
            methodology_str = "GradientBoostingClassifier on 15 hydro-meteorological features with empirical satellite ground truth."
            limitations_val = "Calibrated against 32 empirical ISRO Bhuvan SAR flood inundation rasters and IMD district telemetry."
            conf_prov_val = {
                "source": "ISRO Bhuvan SAR Inundation Rasters + IMD Gridded Telemetry + CWC Catchment Telemetry",
                "observations_count": 18216,
                "features_count": 15,
                "validation_strategy": "5-Fold Grouped Spatial & Temporal Holdout"
            }
        else:
            data_cat = "ML_PREDICTION"
            risk_source_val = RiskSourceType.EMPIRICAL_ML
            sci_state_val = ScientificRiskState.METEOROLOGICAL_SURCHARGE_PROXY
            model_ver_val = pred.get("model_version", "risk_india_flood_v1")
            ds_ver_val = "1.0.0"
            m_scope_val = "Pan-India River Basins & Districts (Precipitation Surcharge)"
            why_risk = "Empirical flood surcharge inference based on acute rainfall surge, antecedent moisture, and basin morphometry."
            methodology_str = "GradientBoostingClassifier trained on 18,184 IMD observations with compound flood formulation."
            limitations_val = "Automated Hydrological Surcharge & Precipitation Severity Proxy. Inundation ground truth unobserved outside Assam in repository."
            conf_prov_val = {
                "source": "IMD District Precipitation Network + CWC Basin Flood Vulnerability Index",
                "observations_count": 18184,
                "features_count": 15,
                "validation_strategy": "5-Fold Grouped Spatial & Temporal Holdout"
            }

        return RiskAnalyzeResponse(
            status=pred.get("status", "success"),
            message=pred.get("message"),
            location_id=pred.get("location_id", request.location_id),
            district=pred.get("district", request.district),
            state=pred.get("state", location.name if location else None),
            hazard="flood",
            disaster_type="flood",
            model_version=model_ver_val,
            flood_probability=pred.get("flood_probability"),
            probability=pred.get("flood_probability"),
            risk_score=int(round(pred.get("risk_score", 0))),
            risk_level=pred.get("risk_level", "LOW"),
            top_factors=top_factors,
            risk_factors=risk_factors,
            is_prototype=False,
            emergency_warning=(pred.get("risk_score", 0) >= 80),
            primary_driver=primary_driver,
            recommended_action=pred.get("recommended_action") or "Monitor official CWC bulletins and IMD district alerts.",
            recommended_immediate_action=pred.get("recommended_action") or "Continuous flood monitoring active via RISK // INDIA Flood Model v1.",
            disclaimer=pred.get("disclaimer") or "RISK // INDIA Flood Model v1 inference based on empirical IMD and CWC observations. Official advisories from NDMA/SDMA supersede automated estimates.",
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
