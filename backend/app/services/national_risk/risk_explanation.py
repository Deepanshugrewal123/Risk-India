"""
RISK // INDIA — Scientific Risk Explanation Engine
=================================================
Produces plain-language, transparent, and scientifically honest explanations
for multi-hazard assessments across all Indian administrative entities.
Clearly distinguishes official active alerts, regional baselines, and empirical ML.
"""

from typing import Dict, Any, Optional, List


class RiskExplanationEngine:
    """Generates transparent explanations and disclosures."""

    def explain_state_risk(
        self,
        state_name: str,
        primary_hazard: str,
        overall_risk_level: str,
        has_active_alert: bool,
        is_assam: bool,
        active_alert_count: int
    ) -> str:
        """Formulates primary explanation of current risk posture."""
        if has_active_alert:
            return (
                f"{state_name} has {active_alert_count} active official warning(s) currently monitored. "
                f"Primary hazard is {primary_hazard} with {overall_risk_level} severity. "
                f"Follow official instructions issued by State and District Disaster Management Authorities."
            )
        elif is_assam:
            return (
                f"Assam risk evaluated via regional hydro-meteorological baseline and verified "
                f"empirical ML prototype calibration (assam_flood_prototype_v1). "
                f"Currently reporting {overall_risk_level} regional risk posture."
            )
        else:
            return (
                f"Regional baseline risk derived from published NDMA vulnerability matrices, "
                f"BIS seismic zonation, and CWC/IMD climatological normals. "
                f"No active official warning is currently triggered for {state_name}."
            )

    def explain_ml_availability(self, state_name: str) -> Dict[str, Any]:
        """
        Explains ML model availability.
        Assam: EMPIRICAL_ML available.
        Non-Assam: ML_STATUS = NOT_AVAILABLE, with clean scientific explanation.
        """
        s_clean = state_name.lower().strip()
        is_assam = ("assam" in s_clean or s_clean == "as" or s_clean == "in-as")

        if is_assam:
            return {
                "available": True,
                "status": "APPROVED",
                "ml_status": "AVAILABLE",
                "model_id": "assam_flood_prototype_v1",
                "message": (
                    "Empirical ML flood prediction is active via assam_flood_prototype_v1 "
                    "(13 hydro-meteorological features, 32 audited empirical observations, 12 corroborated events)."
                ),
                "scope_guard": "Assam Brahmaputra Corridor only. 13 features mandatory. Zero synthetic data."
            }
        else:
            return {
                "available": False,
                "status": "NOT_AVAILABLE",
                "ml_status": "NOT_AVAILABLE",
                "model_id": "NONE",
                "message": (
                    "Empirical ML prediction is not currently validated for this region. "
                    "Regional baseline risk and official disaster intelligence are shown."
                ),
                "scope_guard": "Trained ML is strictly prohibited outside the approved Assam corridor."
            }

    def explain_limitations(
        self,
        state_name: str,
        is_assam: bool,
        unreachable_providers: Optional[List[str]] = None
    ) -> str:
        """Explicitly discloses boundaries, sensor density, and upstream provider health."""
        limitations = [
            f"Regional risk reflects published government vulnerability frameworks and live official telemetry."
        ]
        if not is_assam:
            limitations.append(
                "Predictive machine learning is not calibrated for this state; regional baseline and official advisories apply."
            )
        if unreachable_providers:
            limitations.append(
                f"Live feeds from {', '.join(unreachable_providers)} are currently experiencing upstream degradation; cached fallbacks active."
            )
        limitations.append(
            "Official evacuation directives and public safety broadcasts from District Administration always take precedence."
        )
        return " ".join(limitations)


risk_explanation_engine = RiskExplanationEngine()
