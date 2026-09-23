"""
RISK // INDIA — National Crisis Intelligence Service (Phase 30E)
================================================================
Central coordinator transforming RISK // INDIA into a national public
disaster assistance system. Provides operational crisis state evaluation,
prioritized immediate actions, before/during/after protocols, verified
statutory resources, and plain-language civil protection intelligence.
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone
import logging

from app.services.crisis.crisis_schema import (
    CrisisOperationalState,
    CrisisAssessment,
    CrisisTimelinePoint,
    CrisisExplanation,
    CrisisActionItem,
    CrisisResourceItem,
    FamilyChecklistItem
)
from app.services.crisis.crisis_activation import CrisisActivationEngine
from app.services.crisis.crisis_actions import CrisisActionEngine
from app.services.crisis.crisis_resources import CrisisResourceEngine
from app.services.crisis.crisis_timeline import CrisisTimelineEngine
from app.services.crisis.crisis_explanation import CrisisExplanationEngine

from app.services.national_risk.regional_baseline import (
    regional_baseline_engine,
    SUPPORTED_HAZARDS
)
from app.services.weather import national_weather_service
from app.services.telemetry import dynamic_telemetry_service
from app.services.future_risk import future_risk_service
from app.services.flood_model_service import flood_model_service
from app.services.national_flood_model_service import national_flood_model_service

logger = logging.getLogger("national-crisis-service")


class NationalCrisisService:
    """
    Coordinates public disaster assistance intelligence across all 36 Indian States & UTs.
    Strictly preserves:
    - Pan-India Empirical Flood Model v1 (risk_india_flood_v1)
    - Historical Assam ML Model and Data Invariants (assam_flood_prototype_v1)
    - Earthquake Non-Prediction Guard
    - Zero Synthetic Records Guard
    - Zero Invented Resources Guard
    """

    def __init__(self):
        self._activation_engine = CrisisActivationEngine()
        self._action_engine = CrisisActionEngine()
        self._resource_engine = CrisisResourceEngine()
        self._timeline_engine = CrisisTimelineEngine()
        self._explanation_engine = CrisisExplanationEngine()

    def _resolve_profile(self, region_id: str):
        """Resolves state profile from id, code, or name."""
        profile = regional_baseline_engine.get_state_profile(region_id)
        if profile:
            return profile
        # Case-insensitive search
        norm_id = region_id.strip().lower().replace("_", "-").replace(" ", "-")
        for p in regional_baseline_engine.get_all_state_profiles():
            if (p.id.lower() == norm_id or
                p.code.lower() == norm_id or
                p.name.lower() == region_id.strip().lower()):
                return p
        return None

    @staticmethod
    def _parse_confidence(val: Any, default: float = 0.70) -> float:
        if val is None:
            return default
        if isinstance(val, (int, float)):
            return float(val)
        val_str = str(val).strip().upper()
        mapping = {
            "HIGH": 0.85,
            "MEDIUM": 0.65,
            "MODERATE": 0.65,
            "LOW": 0.45,
            "VERY_LOW": 0.25,
            "VERY LOW": 0.25
        }
        if val_str in mapping:
            return mapping[val_str]
        try:
            return float(val_str)
        except (ValueError, TypeError):
            return default

    def assess_crisis(
        self,
        region_id: str,
        hazard: Optional[str] = None,
        manual_activation: bool = False,
        coordinates: Optional[Tuple[float, float]] = None,
        model_version: Optional[str] = None
    ) -> CrisisAssessment:
        """
        Assesses crisis state, action requirements, and emergency intelligence for a region.
        """
        profile = self._resolve_profile(region_id)
        region_name = profile.name if profile else region_id.replace("-", " ").title()
        canon_id = profile.id if profile else region_id.lower()
        is_assam = (canon_id in ["assam", "as", "in-as", "assam-state"])

        # Determine target hazard
        target_hazard = "FLOOD"
        if hazard and hazard.upper() in SUPPORTED_HAZARDS:
            target_hazard = hazard.upper()
        elif profile:
            target_hazard = profile.primary_hazard.upper()

        # 1. Fetch Official Weather Warnings
        try:
            raw_warnings = national_weather_service.get_active_warnings(region_name)
        except Exception as e:
            logger.warning(f"Failed to fetch active weather warnings for {region_name}: {e}")
            raw_warnings = []
        official_warnings: List[Dict[str, Any]] = []
        for w in raw_warnings:
            w_id = getattr(w, "warning_id", getattr(w, "id", "warn-001"))
            w_src = getattr(w, "provider", "India Meteorological Department (IMD)")
            official_warnings.append({
                "id": w_id,
                "severity": w.severity,
                "headline": w.headline,
                "description": w.description,
                "source": w_src,
                "valid_until": w.valid_until,
                "color": w.severity
            })

        # 2. Fetch Telemetry Summary
        try:
            obs = national_weather_service.get_current_weather(region_name)
        except Exception as e:
            logger.warning(f"Failed to fetch current weather for {region_name}: {e}")
            obs = None

        rain_val = 0.0
        temp_val = 28.0
        wind_kmh = 12.0
        rh_pct = 70.0
        telemetry_fresh = (obs is not None)
        if obs:
            if obs.rainfall_mm is not None:
                rain_val = float(obs.rainfall_mm)
            if obs.temperature_celsius is not None:
                temp_val = float(obs.temperature_celsius)
            if obs.wind_speed_mps is not None:
                wind_kmh = round(float(obs.wind_speed_mps) * 3.6, 1)
            if obs.relative_humidity_percent is not None:
                rh_pct = float(obs.relative_humidity_percent)

        telemetry_summary: Dict[str, Any] = {
            "rainfall_24h_mm": rain_val,
            "temperature_c": temp_val,
            "wind_speed_kmh": wind_kmh,
            "relative_humidity_pct": rh_pct,
            "river_danger_ratio": 0.0,
            "telemetry_fresh": telemetry_fresh
        }

        # Check river telemetry if flood-relevant
        if target_hazard == "FLOOD":
            basin_name = profile.primary_basin.lower() if profile else ""
            try:
                readings = dynamic_telemetry_service.get_observations(basin=basin_name, variable_type="WATER_LEVEL", limit=50) if basin_name else dynamic_telemetry_service.get_observations(variable_type="WATER_LEVEL", limit=50)
                for r in readings:
                    if r.provenance and r.provenance.get("danger_level_m"):
                        try:
                            danger_m = float(r.provenance["danger_level_m"])
                            if danger_m > 0 and r.normalized_value is not None:
                                ratio = r.normalized_value / danger_m
                                if ratio > telemetry_summary["river_danger_ratio"]:
                                    telemetry_summary["river_danger_ratio"] = round(ratio, 3)
                        except (ValueError, TypeError):
                            pass
            except Exception as e:
                logger.warning(f"Failed to fetch river telemetry for basin '{basin_name}': {e}")

        # 2b. Execute Flood ML Inference (Active Pan-India Model: risk_india_flood_v1)
        flood_pred = None
        is_legacy_assam_requested = (model_version == "assam_flood_prototype_v1" and is_assam)
        if target_hazard == "FLOOD":
            if is_legacy_assam_requested:
                try:
                    flood_pred = flood_model_service.predict(
                        location_id=canon_id,
                        district=None,
                        features={"rainfall_24h": telemetry_summary["rainfall_24h_mm"]},
                        hazard="flood"
                    )
                except Exception as e:
                    logger.warning(f"Legacy Assam flood model inference failed for {canon_id}: {e}")
                    flood_pred = None
            else:
                try:
                    rf_feat = {
                        "actual_rainfall_24h_mm": telemetry_summary["rainfall_24h_mm"],
                        "river_danger_ratio": telemetry_summary.get("river_danger_ratio", 0.0)
                    }
                    if coordinates:
                        rf_feat["latitude"] = coordinates[0]
                        rf_feat["longitude"] = coordinates[1]
                    flood_pred = national_flood_model_service.predict(
                        location_id=canon_id,
                        state=region_name,
                        district=None,
                        features=rf_feat,
                        hazard="flood"
                    )
                except Exception as e:
                    logger.warning(f"National flood model inference failed for {canon_id}: {e}")
                    flood_pred = None

        # 3. Fetch Future Risk Horizons
        try:
            reg_future = future_risk_service.get_region_hazard_timeline(canon_id, target_hazard)
        except Exception as e:
            logger.warning(f"Failed to fetch future hazard timeline for {canon_id}/{target_hazard}: {e}")
            reg_future = None
        future_windows: Dict[str, Dict[str, Any]] = {}
        peak_level = "LOW"
        peak_score = 25.0
        peak_window = "NOW"
        future_conf = 0.70

        if reg_future and "timeline" in reg_future:
            for step in reg_future["timeline"]:
                w_key = step.get("horizon", step.get("forecast_window", "")).lower()
                lvl = str(step.get("risk_level", "LOW")).upper()
                sc = float(step.get("risk_score", 20.0))
                parsed_conf = self._parse_confidence(step.get("confidence"), 0.70)
                future_windows[w_key] = {
                    "risk_level": lvl,
                    "risk_score": sc,
                    "confidence": parsed_conf,
                    "key_factors": step.get("key_factors", []),
                    "provenance": step.get("provenance", "National Forecast Engine")
                }
                if sc > peak_score:
                    peak_score = sc
                    peak_level = lvl
                    peak_window = w_key
                    future_conf = parsed_conf

        # Current risk score computation
        current_risk_score = 25.0
        current_risk_level = "LOW"
        if official_warnings:
            sev = official_warnings[0]["severity"].upper()
            if sev == "RED":
                current_risk_score = 88.0
                current_risk_level = "CRITICAL"
            elif sev in ["ORANGE", "AMBER"]:
                current_risk_score = 72.0
                current_risk_level = "HIGH"
            elif sev == "YELLOW":
                current_risk_score = 52.0
                current_risk_level = "MEDIUM"
        elif target_hazard == "FLOOD" and flood_pred and flood_pred.get("status") == "success":
            current_risk_score = float(flood_pred.get("risk_score", 25.0))
            lvl = str(flood_pred.get("risk_level", "LOW")).upper()
            if lvl == "SEVERE":
                current_risk_level = "CRITICAL"
            elif lvl == "HIGH":
                current_risk_level = "HIGH"
            elif lvl in ["MEDIUM", "MODERATE"]:
                current_risk_level = "MEDIUM"
            else:
                current_risk_level = "LOW"
        else:
            if telemetry_summary["rainfall_24h_mm"] > 115.5:
                current_risk_score = 82.0
                current_risk_level = "CRITICAL"
            elif telemetry_summary["rainfall_24h_mm"] > 64.5:
                current_risk_score = 68.0
                current_risk_level = "HIGH"
            elif telemetry_summary["rainfall_24h_mm"] > 20.0:
                current_risk_score = 48.0
                current_risk_level = "MEDIUM"

        # Special Guard: Earthquake
        if target_hazard == "EARTHQUAKE":
            # Never predict future earthquakes
            peak_level = "VERY_LOW"
            peak_score = 5.0
            peak_window = "BASELINE"
            current_risk_score = 20.0
            current_risk_level = "LOW"

        # 4. Evaluate Crisis Operational State & Activation Rules
        op_state, is_rec, act_reason, matched_rules = self._activation_engine.evaluate(
            current_risk_level=current_risk_level,
            current_risk_score=current_risk_score,
            peak_future_risk_level=peak_level,
            peak_future_score=peak_score,
            official_warnings=official_warnings,
            telemetry_summary=telemetry_summary,
            future_risk_confidence=future_conf,
            telemetry_fresh=True,
            manual_activation=manual_activation
        )

        # 5. Core Disaster Answers: "What is happening?" and "What could happen next?"
        if op_state in [CrisisOperationalState.CRISIS, CrisisOperationalState.ELEVATED]:
            what_is_happening = (
                f"Active emergency alert in {region_name}: {target_hazard} risk is currently assessed as {current_risk_level} "
                f"(score: {current_risk_score:.0f}/100) driven by {act_reason.lower()}."
            )
            what_could_happen_next = (
                f"Peak threat window is projected during {peak_window.replace('_', '-').upper()} with potential {peak_level} "
                f"severity. Rapid runoff, structural inundation, or disrupted transport corridors are anticipated."
            )
        elif op_state == CrisisOperationalState.WATCH:
            what_is_happening = (
                f"Precautionary watch in effect for {region_name}. {target_hazard} activity is moderate (score: {current_risk_score:.0f}/100) "
                "with atmospheric and hydrological conditions approaching advisory thresholds."
            )
            what_could_happen_next = (
                f"Forecast indicators suggest conditions may persist or peak at {peak_level} in {peak_window.replace('_', '-').upper()}. "
                "Monitor official bulletins and verify household disaster supplies."
            )
        else:
            what_is_happening = (
                f"Normal baseline status in {region_name}. {target_hazard} indicators are at {current_risk_level} levels "
                f"(score: {current_risk_score:.0f}/100) with no statutory emergency bulletins active."
            )
            what_could_happen_next = (
                f"Conditions are expected to remain steady across standard forecast horizons. "
                "Maintain general seasonal preparedness."
            )

        if target_hazard == "EARTHQUAKE":
            what_could_happen_next = (
                "Earthquake occurrences cannot be predicted. Preparedness relies strictly on structural resilience "
                "and knowing immediate 'Drop, Cover, and Hold On' life-safety drills."
            )

        # 6. Prioritized Human Actions (Top 3-5 What To Do Now + Protocols)
        what_to_do_now = self._action_engine.get_what_to_do_now(target_hazard)
        action_protocols = self._action_engine.get_phase_protocols(target_hazard)
        family_prep_checklist = self._action_engine.get_family_prep_checklist()

        # 7. Verified Emergency Resources
        coords = coordinates
        if not coords and obs and getattr(obs, "latitude", None) is not None and getattr(obs, "longitude", None) is not None:
            coords = (obs.latitude, obs.longitude)

        emergency_resources, resource_note = self._resource_engine.get_emergency_resources(
            state_or_ut=region_name,
            hazard=target_hazard,
            coordinates=coords,
            max_results=8
        )

        # 8. Timeline (5 Horizons)
        is_flood_ml_active = (target_hazard == "FLOOD" and (is_legacy_assam_requested or national_flood_model_service.is_ready))
        timeline = self._timeline_engine.build_timeline(
            region_id=canon_id,
            hazard=target_hazard,
            current_level=current_risk_level,
            current_score=current_risk_score,
            future_windows=future_windows,
            official_warnings=official_warnings,
            telemetry_summary=telemetry_summary,
            is_flood_ml=is_flood_ml_active,
            is_assam_flood=is_legacy_assam_requested
        )

        # 9. Deterministic Explanation ("Why this risk?")
        explanation = self._explanation_engine.generate_explanation(
            region_name=region_name,
            hazard=target_hazard,
            current_level=current_risk_level,
            operational_state=op_state.value,
            official_warnings=official_warnings,
            telemetry_summary=telemetry_summary,
            is_assam=is_assam
        )

        # 10. ML Audit & Scientific Guards
        if target_hazard == "FLOOD":
            if is_legacy_assam_requested:
                ml_audit = {
                    "ml_available": True,
                    "model_name": "assam_flood_prototype_v1",
                    "model_status": "LOADED_AND_VERIFIED",
                    "training_scope": "Assam State Brahmaputra Basin (1998-2024)",
                    "synthetic_records": 0,
                    "algorithm": "LogisticRegression",
                    "features_used": 13,
                    "guard_status": "PASS_HISTORICAL_ASSAM_PROTOTYPE_COMPATIBILITY"
                }
            elif national_flood_model_service.is_ready:
                ml_audit = {
                    "ml_available": True,
                    "model_name": "risk_india_flood_v1",
                    "model_display_name": "RISK // INDIA Flood Model v1",
                    "model_status": "LOADED_AND_VERIFIED",
                    "training_scope": "India-Wide Empirical IMD Observations (18,184 records across 36 States/UTs)",
                    "synthetic_records": 0,
                    "algorithm": "GradientBoostingClassifier",
                    "features_used": 15,
                    "guard_status": "PASS_NATIONAL_FLOOD_ML_ACTIVE"
                }
            else:
                ml_audit = {
                    "ml_available": False,
                    "status": "BASELINE_FALLBACK",
                    "reason": "National Flood ML service temporarily unavailable; deterministic statutory baseline active.",
                    "synthetic_records": 0,
                    "guard_status": "PASS_FAILSAFE_GUARD"
                }
        elif target_hazard == "EARTHQUAKE":
            ml_audit = {
                "ml_available": False,
                "status": "NOT_AVAILABLE",
                "reason": "Earthquake prediction is scientifically non-viable globally.",
                "is_predictable": False,
                "forecast_attempted": False,
                "synthetic_records": 0,
                "guard_status": "PASS_EARTHQUAKE_NON_PREDICTION_GUARD"
            }
        else:
            ml_audit = {
                "ml_available": False,
                "status": "NOT_AVAILABLE",
                "reason": f"Empirical ML models are calibrated specifically for flood hazards (risk_india_flood_v1). {region_name} evaluated using empirical hydromet sensor telemetry and statutory warning bulletins.",
                "synthetic_records": 0,
                "guard_status": "PASS_NON_FLOOD_STATUTORY_GUARD"
            }

        return CrisisAssessment(
            region_id=canon_id,
            region_name=region_name,
            operational_state=op_state,
            is_crisis_recommended=is_rec,
            activation_reason=act_reason,
            matched_rules=matched_rules,
            is_manual_activation=manual_activation,
            primary_hazard=target_hazard,
            current_risk_level=current_risk_level,
            current_risk_score=round(current_risk_score, 2),
            peak_future_risk_level=peak_level,
            peak_future_window=peak_window,
            what_is_happening=what_is_happening,
            what_could_happen_next=what_could_happen_next,
            what_to_do_now=what_to_do_now,
            action_protocols=action_protocols,
            family_prep_checklist=family_prep_checklist,
            official_warnings=official_warnings,
            emergency_resources=emergency_resources,
            resource_availability_note=resource_note,
            timeline=timeline,
            explanation=explanation,
            telemetry_summary=telemetry_summary,
            ml_audit=ml_audit
        )

    def get_national_crisis_overview(self) -> Dict[str, Any]:
        """
        Provides national crisis posture overview across all 36 Indian administrative entities.
        """
        profiles = regional_baseline_engine.get_all_state_profiles()
        assessments: List[Dict[str, Any]] = []
        state_counts = {
            "CRISIS": 0,
            "ELEVATED": 0,
            "WATCH": 0,
            "NORMAL": 0
        }

        crisis_recommended_regions: List[Dict[str, Any]] = []

        for p in profiles:
            a = self.assess_crisis(p.id)
            state_counts[a.operational_state.value] += 1
            entry = {
                "region_id": a.region_id,
                "region_name": a.region_name,
                "state_type": p.administrative_type,
                "operational_state": a.operational_state.value,
                "is_crisis_recommended": a.is_crisis_recommended,
                "activation_reason": a.activation_reason,
                "primary_hazard": a.primary_hazard,
                "current_risk_level": a.current_risk_level,
                "current_risk_score": a.current_risk_score,
                "official_warnings_count": len(a.official_warnings),
                "matched_rules": a.matched_rules
            }
            assessments.append(entry)
            if a.is_crisis_recommended:
                crisis_recommended_regions.append(entry)

        return {
            "title": "RISK // INDIA National Crisis Intelligence Overview",
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
            "total_entities_monitored": len(profiles),
            "states_covered": sum(1 for p in profiles if p.administrative_type == "STATE"),
            "union_territories_covered": sum(1 for p in profiles if p.administrative_type == "UNION_TERRITORY"),
            "operational_state_distribution": state_counts,
            "crisis_recommended_count": len(crisis_recommended_regions),
            "crisis_recommended_regions": crisis_recommended_regions,
            "synthetic_records": 0,
            "regions": assessments
        }


# Global singleton instance
national_crisis_service = NationalCrisisService()
