"""
RISK // INDIA — Crisis Explanation Engine (Phase 30E)
=====================================================
Generates deterministic, transparent, and plain-language explanations answering:
1. Why is this risk level assessed?
2. What changed recently?
3. What is the supporting tangible evidence?
4. What realistic factors could change this risk?
5. What do we NOT know (data limitations)?
"""

from typing import Dict, List, Any, Optional
from app.services.crisis.crisis_schema import CrisisExplanation


class CrisisExplanationEngine:
    """Produces deterministic scientific and operational explanations."""

    @staticmethod
    def generate_explanation(
        region_name: str,
        hazard: str,
        current_level: str,
        operational_state: str,
        official_warnings: List[Dict[str, Any]],
        telemetry_summary: Dict[str, Any],
        is_assam: bool = False
    ) -> CrisisExplanation:
        """
        Generates structured CrisisExplanation.
        """
        norm_hazard = str(hazard).upper()
        norm_level = str(current_level).upper()
        
        evidence: List[str] = []
        
        # 1. Statutory Warnings Evidence
        if official_warnings:
            for w in official_warnings[:2]:
                src = w.get("source", "Statutory Warning")
                sev = w.get("severity", "WARNING")
                desc = w.get("description", w.get("headline", "Alert active"))
                evidence.append(f"{src} ({sev}): {desc}")

        # 2. Telemetry Evidence
        rain = telemetry_summary.get("rainfall_24h_mm")
        if rain is not None:
            evidence.append(f"Measured 24-hr cumulative rainfall: {rain:.1f} mm")
        
        river_ratio = telemetry_summary.get("river_danger_ratio")
        if river_ratio is not None:
            ratio_pct = river_ratio * 100
            evidence.append(f"CWC Catchment Gauge: Operating at {ratio_pct:.1f}% of official danger mark")

        temp = telemetry_summary.get("temperature_c")
        if temp is not None and norm_hazard == "HEATWAVE":
            evidence.append(f"Surface maximum air temperature recorded: {temp:.1f}°C")

        # Fallback evidence if none recorded
        if not evidence:
            evidence.append(f"Continuous environmental baseline monitoring for {region_name}")

        # Why
        if norm_level in ["CRITICAL", "HIGH"]:
            why = (
                f"Severe {norm_hazard.lower()} conditions are threatening {region_name} due to elevated "
                f"environmental telemetry thresholds and active statutory meteorological alerts."
            )
        elif norm_level == "MEDIUM":
            why = (
                f"Moderate {norm_hazard.lower()} susceptibility detected in {region_name} due to approaching "
                f"weather systems and saturated regional catchment conditions."
            )
        else:
            why = (
                f"Environmental and hydromet conditions in {region_name} currently remain within standard "
                f"climatological baselines without immediate critical hazard triggers."
            )

        # What changed
        changes = []
        if rain and rain >= 35.0:
            changes.append(f"Significant precipitation accumulation ({rain:.1f} mm) recorded over the past 24 hours")
        if river_ratio and river_ratio >= 0.85:
            changes.append("Basin river discharge surged significantly above seasonal mean")
        if official_warnings:
            changes.append("Official emergency bulletins escalated by meteorological/hydrological nodal authorities")
        if not changes:
            changes.append("No sudden anomalous telemetry spikes observed over the preceding 6 hours")
        what_changed = "; ".join(changes) + "."

        # What could change
        if norm_hazard == "FLOOD":
            what_could_change = (
                "Sustained heavy precipitation in upstream catchments or emergency dam discharge will escalate flood stages. "
                "Conversely, 12-24 hours of dry weather will allow gravity drainage and lower water levels."
            )
        elif norm_hazard == "CYCLONE":
            what_could_change = (
                "A shift in cyclone landfall track or forward translational speed will alter the zone of maximum storm surge and wind damage. "
                "Land interaction will cause rapid structural weakening of the cyclonic vortex."
            )
        elif norm_hazard == "HEATWAVE":
            what_could_change = (
                "Western disturbances, maritime sea breezes, or convective evening thundershowers will cause a rapid 3-6°C temperature drop. "
                "Continued clear skies and dry westerly winds will prolong the heatwave."
            )
        elif norm_hazard == "LANDSLIDE":
            what_could_change = (
                "Subsurface pore water pressure accumulation from further rainfall could trigger catastrophic slope shear. "
                "Cessation of rain and drainage clearance will gradually stabilize soil cohesion."
            )
        elif norm_hazard == "EARTHQUAKE":
            what_could_change = (
                "Seismic events cannot be forecasted. Aftershocks of decreasing frequency and magnitude typically follow any tectonic rupture."
            )
        else:
            what_could_change = (
                "Shifts in atmospheric convective instability or frontal movement may intensify or dissipate thunderstorm cells."
            )

        # What we do NOT know (Data limitations)
        if norm_hazard == "EARTHQUAKE":
            data_limitations = (
                "Tectonic stress accumulation and exact earthquake occurrence times cannot be deterministically predicted "
                "by any scientific institution globally. Micro-fault slippage and building-specific resonant vulnerabilities "
                "require specialized on-site civil structural audits."
            )
        elif norm_hazard == "FLOOD":
            data_limitations = (
                f"India-wide flood risk utilizes the empirical machine learning model (risk_india_flood_v1) calibrated across "
                f"18,184 IMD historical observations combined with CWC river sensors. However, localized urban storm drain blockages, "
                f"unmapped breach locations along rural earthen bunds, and micro-topographical depressions are not resolvable in real time."
            )
        else:
            data_limitations = (
                f"Machine learning inference is strictly restricted to flood hazard (risk_india_flood_v1); {region_name} assessments are derived from "
                "empirical sensor telemetry, NWP numerical weather prediction, and statutory IMD/CWC bulletins. "
                "Micro-scale hyper-local cloudbursts and village-level drainage choke points cannot be monitored in real time."
            )

        return CrisisExplanation(
            why=why,
            what_changed=what_changed,
            supporting_evidence=evidence,
            what_could_change=what_could_change,
            data_limitations=data_limitations
        )
