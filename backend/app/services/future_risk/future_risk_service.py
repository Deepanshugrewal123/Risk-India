"""
RISK // INDIA — Future Risk Service Facade
==========================================
Central coordinator for nationwide forward risk assessment, multi-horizon timelines,
disaster action protocols, verified help ecosystems, forecast variables, and
plain-language citizen explanations.
"""

from typing import Dict, List, Any, Optional
from .future_risk_engine import future_risk_engine
from .action_engine import disaster_action_engine
from .help_ecosystem import help_ecosystem
from .ml_expansion_gate import national_ml_expansion_gate
from .forecast_horizons import ALL_FORECAST_HORIZONS
from .forecast_contracts import assemble_region_forecast_dataset
from .explanation_engine import public_safety_explanation_engine
from .cascading_risk_engine import cascading_risk_engine
from .extended_safety_engine import extended_safety_engine
from app.services.national_risk.regional_baseline import regional_baseline_engine, SUPPORTED_HAZARDS


class FutureRiskService:
    """Central service facade for nationwide future disaster risk operations."""

    def get_national_future_risk_summary(
        self,
        hazard: Optional[str] = None,
        horizon: Optional[str] = None
    ) -> Dict[str, Any]:
        """Provides national forward risk overview across all 36 administrative entities."""
        profiles = regional_baseline_engine.get_all_state_profiles()
        target_horizon = horizon.upper().strip() if horizon else "6_24_HOURS"
        results = []

        for p in profiles:
            assessments = future_risk_engine.evaluate_future_risk(
                state_identifier=p.id,
                hazard=hazard,
                horizon=target_horizon
            )
            if assessments:
                # Find maximum forward risk for this region in the selected horizon
                top = max(assessments, key=lambda a: a.risk_score)
                results.append({
                    "region": {
                        "id": p.id,
                        "name": p.name,
                        "code": p.code,
                        "type": p.administrative_type,
                        "primary_basin": p.primary_basin
                    },
                    "forecast_window": target_horizon,
                    "primary_hazard": top.hazard_type,
                    "risk_score": top.risk_score,
                    "risk_level": top.risk_level,
                    "methodology": top.methodology,
                    "confidence": top.confidence,
                    "summary": top.summary,
                    "ml_scope_note": top.ml_scope_note,
                    "synthetic_records": 0
                })

        return {
            "title": "RISK // INDIA National Future Disaster Risk Overview",
            "forecast_window": target_horizon,
            "total_entities_evaluated": len(results),
            "states_covered": sum(1 for r in results if r["region"]["type"] == "STATE"),
            "union_territories_covered": sum(1 for r in results if r["region"]["type"] == "UNION_TERRITORY"),
            "supported_hazards": SUPPORTED_HAZARDS,
            "supported_horizons": ALL_FORECAST_HORIZONS,
            "synthetic_records": 0,
            "regions": results
        }

    def get_region_future_risk(self, state_identifier: str) -> Optional[Dict[str, Any]]:
        """Returns comprehensive future risk assessment for a specific State or UT across all horizons and hazards."""
        profile = regional_baseline_engine.get_state_profile(state_identifier)
        if not profile:
            return None

        assessments = future_risk_engine.evaluate_future_risk(state_identifier)
        by_hazard = {}
        for a in assessments:
            h = a.hazard_type
            if h not in by_hazard:
                by_hazard[h] = []
            by_hazard[h].append(a.to_dict())

        # Determine highest future hazard
        top_rec = max(assessments, key=lambda a: a.risk_score) if assessments else None
        primary_h = top_rec.hazard_type if top_rec else "FLOOD"

        actions = disaster_action_engine.get_actions_for_region(profile.name, primary_h)

        return {
            "region": {
                "id": profile.id,
                "name": profile.name,
                "code": profile.code,
                "type": profile.administrative_type,
                "primary_basin": profile.primary_basin
            },
            "highest_future_risk": {
                "hazard_type": primary_h,
                "score": top_rec.risk_score if top_rec else 30,
                "level": top_rec.risk_level if top_rec else "LOW",
                "forecast_window": top_rec.forecast_window if top_rec else "6_24_HOURS",
                "confidence": top_rec.confidence if top_rec else "HIGH"
            },
            "hazards_forward_assessment": by_hazard,
            "action_checklist": actions,
            "synthetic_records": 0
        }

    def get_region_hazard_timeline(self, state_identifier: str, hazard: str) -> Optional[Dict[str, Any]]:
        """Returns forward step-by-step projection across all horizons for a specific hazard."""
        profile = regional_baseline_engine.get_state_profile(state_identifier)
        if not profile:
            return None

        h_clean = hazard.upper().strip()
        if h_clean not in SUPPORTED_HAZARDS:
            return None

        assessments = future_risk_engine.evaluate_future_risk(state_identifier, hazard=h_clean)
        timeline = [a.to_dict() for a in assessments]

        return {
            "region": {
                "id": profile.id,
                "name": profile.name,
                "code": profile.code,
                "type": profile.administrative_type
            },
            "hazard_type": h_clean,
            "timeline_horizons": ALL_FORECAST_HORIZONS,
            "timeline": timeline,
            "synthetic_records": 0
        }

    def get_region_actions(self, state_identifier: str, hazard: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Returns structured Before / During / After action protocols."""
        profile = regional_baseline_engine.get_state_profile(state_identifier)
        if not profile:
            return None

        target_hazard = hazard.upper().strip() if hazard else profile.primary_hazard
        return disaster_action_engine.get_actions_for_region(profile.name, target_hazard)

    def get_region_forecast_variables(self, state_identifier: str) -> Optional[Dict[str, Any]]:
        """Returns normalized weather, hydrology, cyclone, and environmental forecast variables."""
        profile = regional_baseline_engine.get_state_profile(state_identifier)
        if not profile:
            return None

        dataset = assemble_region_forecast_dataset(profile.name)
        if not dataset:
            return None

        return dataset.to_dict()

    def get_region_explanation(
        self,
        state_identifier: str,
        hazard: Optional[str] = None,
        district: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Returns accessible public safety explanation answering WHAT, WHEN, WHY, CONFIDENCE, WHAT TO DO, SOURCE."""
        profile = regional_baseline_engine.get_state_profile(state_identifier)
        if not profile:
            return None

        target_hazard = hazard.upper().strip() if hazard else profile.primary_hazard
        assessments = future_risk_engine.evaluate_future_risk(
            state_identifier=state_identifier,
            hazard=target_hazard,
            horizon="6_24_HOURS"
        )
        if not assessments:
            return None

        top_assessment = assessments[0]
        return public_safety_explanation_engine.explain(top_assessment, district=district)

    def get_help_directory(self, state: Optional[str] = None) -> Dict[str, Any]:
        """Returns verified emergency dispatch and verified community assistance channels."""
        return help_ecosystem.get_assistance_directory(state=state)

    def get_ml_expansion_status(self) -> Dict[str, Any]:
        """Returns 14-gate scientific promotion evaluations across the 5 priority basins."""
        evals = national_ml_expansion_gate.evaluate_all_priority_basins()
        return {
            "expansion_policy": "Scientific promotion gates strictly enforced. Non-Assam ML is prohibited until 14 validation gates pass.",
            "priority_basins": evals,
            "synthetic_records": 0
        }

    def get_region_cascading_risk(
        self,
        state_identifier: str,
        hazard: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Evaluates regional cascading consequence chains with honest evidence postures."""
        assessment = cascading_risk_engine.evaluate_region_cascading_risk(
            state_identifier=state_identifier,
            hazard=hazard
        )
        if not assessment:
            return None
        return assessment.to_dict()

    def get_safety_guide(self, hazard: Optional[str] = None) -> Dict[str, Any]:
        """Returns comprehensive Before/During/After life-safety protocols for a hazard."""
        return extended_safety_engine.get_complete_hazard_guide(hazard or "FLOOD")

    def get_safety_catalog(self) -> Dict[str, Any]:
        """Returns catalog summary of extended citizen safety guidance."""
        return extended_safety_engine.get_catalog_summary()

    def get_filtered_safety_instructions(
        self,
        hazard: Optional[str] = None,
        phase: Optional[str] = None,
        category: Optional[str] = None,
        priority: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Returns filtered life-safety guidance items."""
        return extended_safety_engine.get_instructions(
            hazard=hazard,
            phase=phase,
            category=category,
            priority=priority
        )


future_risk_service = FutureRiskService()
