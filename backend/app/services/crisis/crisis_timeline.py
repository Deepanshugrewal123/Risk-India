"""
RISK // INDIA — Crisis Timeline Engine (Phase 30E)
==================================================
Builds a unified 5-horizon progression from empirical telemetry, statutory bulletins,
and forecast models, with strict signal provenance and scientific invariants.
"""

from typing import Dict, List, Any, Optional
from app.services.crisis.crisis_schema import (
    CrisisTimelinePoint,
    TimelineSignalType
)


class CrisisTimelineEngine:
    """
    Constructs an authoritative 5-horizon progression for crisis projection:
    - NOW: Observed empirical telemetry & current active bulletins
    - 0_6H: Immediate flash window / nowcast
    - 6_24H: Day 1 high-resolution forecast & warning
    - 1_3D: Multi-day synoptic outlook
    - 3_7D: Extended probabilistic outlook
    """

    @staticmethod
    def build_timeline(
        region_id: str,
        hazard: str,
        current_level: str,
        current_score: float,
        future_windows: Dict[str, Dict[str, Any]],
        official_warnings: List[Dict[str, Any]],
        telemetry_summary: Dict[str, Any],
        is_flood_ml: bool = False,
        is_assam_flood: bool = False
    ) -> List[CrisisTimelinePoint]:
        """
        Constructs the 5 timeline points with explicit provenance and hazard guards.
        """
        norm_hazard = str(hazard).upper()
        timeline: List[CrisisTimelinePoint] = []

        # 1. NOW (Observed Empirical Telemetry & Active Bulletins)
        now_factors = []
        if telemetry_summary.get("rainfall_24h_mm"):
            now_factors.append(f"Recorded rainfall: {telemetry_summary['rainfall_24h_mm']:.1f} mm")
        if telemetry_summary.get("river_danger_ratio"):
            ratio_pct = telemetry_summary['river_danger_ratio'] * 100
            now_factors.append(f"Hydrological gauge at {ratio_pct:.1f}% of danger level")
        if telemetry_summary.get("temperature_c"):
            now_factors.append(f"Ambient temperature: {telemetry_summary['temperature_c']:.1f}°C")
        if official_warnings:
            now_factors.append(f"Active statutory warning: {official_warnings[0].get('headline', 'Advisory')}")
        if not now_factors:
            now_factors.append("Baseline environmental monitoring active")

        if is_assam_flood:
            now_signal = TimelineSignalType.EMPIRICAL_ML
            now_prov = "Assam ML Prototype (Validated) + Live CWC Telemetry"
        elif is_flood_ml:
            now_signal = TimelineSignalType.EMPIRICAL_ML
            now_prov = "India-Wide Flood ML Model v1 (risk_india_flood_v1) + Live Telemetry"
        else:
            now_signal = TimelineSignalType.OBSERVED
            now_prov = "Empirical Hydromet Sensor Telemetry + Official Warning Bulletin"

        timeline.append(
            CrisisTimelinePoint(
                horizon="NOW",
                window_label="Current Situation (Live)",
                expected_risk_level=current_level,
                expected_risk_score=current_score,
                confidence=0.92 if (is_flood_ml or is_assam_flood) else 0.85,
                primary_hazard=norm_hazard,
                signal_type=now_signal,
                key_factors=now_factors,
                provenance=now_prov
            )
        )

        # Map for future horizons
        horizon_specs = [
            ("0_6H", "0-6h", "Immediate Window (0–6 Hours)", TimelineSignalType.OFFICIAL_WARNING if official_warnings else TimelineSignalType.FORECAST),
            ("6_24H", "6-24h", "Near-Term Forecast (6–24 Hours)", TimelineSignalType.FORECAST_DERIVED_RISK),
            ("1_3D", "1-3d", "Extended Synoptic Outlook (1–3 Days)", TimelineSignalType.FORECAST),
            ("3_7D", "3-7d", "Medium-Range Outlook (3–7 Days)", TimelineSignalType.BASELINE)
        ]

        # Guard: Earthquake future prediction is strictly prohibited
        is_earthquake = (norm_hazard == "EARTHQUAKE")

        for horizon_key, win_key, win_label, default_signal in horizon_specs:
            win_data = future_windows.get(win_key, {})
            
            if is_earthquake:
                # Invariant: Never predict future earthquakes
                timeline.append(
                    CrisisTimelinePoint(
                        horizon=horizon_key,
                        window_label=win_label,
                        expected_risk_level="VERY_LOW",
                        expected_risk_score=0.05,
                        confidence=0.1,
                        primary_hazard=norm_hazard,
                        signal_type=TimelineSignalType.BASELINE,
                        key_factors=["Earthquake events cannot be forecast deterministically.", "Displaying regional seismic zone tectonic baseline only."],
                        provenance="BIS IS 1893 Seismic Zonation & NCS Historical Catalog"
                    )
                )
                continue

            exp_level = str(win_data.get("risk_level", current_level)).upper()
            exp_score = float(win_data.get("risk_score", current_score))
            conf = float(win_data.get("confidence", 0.70))
            factors = win_data.get("key_factors", [])
            
            if not factors:
                if horizon_key == "0_6H":
                    factors = ["IMD Nowcast radar echoes", "Flash run-off convergence assessment"]
                elif horizon_key == "6_24H":
                    factors = ["Numerical weather prediction (NWP) 24-hr cumulative precipitation"]
                elif horizon_key == "1_3D":
                    factors = ["Synoptic multi-model ensemble precipitation trajectories"]
                else:
                    factors = ["Climatological teleconnection & medium-range global forecasts"]

            signal_type = default_signal
            prov = win_data.get("provenance", f"IMD NWP + CWC Hydrological Ensemble ({horizon_key})")

            timeline.append(
                CrisisTimelinePoint(
                    horizon=horizon_key,
                    window_label=win_label,
                    expected_risk_level=exp_level,
                    expected_risk_score=round(exp_score, 3),
                    confidence=round(conf, 2),
                    primary_hazard=norm_hazard,
                    signal_type=signal_type,
                    key_factors=factors[:3],
                    provenance=prov
                )
            )

        return timeline
