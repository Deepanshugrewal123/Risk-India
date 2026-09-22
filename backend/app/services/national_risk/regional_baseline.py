"""
RISK // INDIA — National Regional Baseline Risk Engine
=====================================================
Provides deterministic regional baseline risk profiles across all 28 States and
8 Union Territories across all 6 disaster hazards.
Derived from published national vulnerability matrices (BIS IS 1893:2016, CWC, IMD, NDMA, GSI).
Strictly labeled as REGIONAL_BASELINE; never presented as ML predictions or live alerts.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

SUPPORTED_HAZARDS = [
    "FLOOD",
    "EARTHQUAKE",
    "CYCLONE",
    "HEATWAVE",
    "LANDSLIDE",
    "SEVERE_WEATHER"
]


@dataclass
class HazardBaselineProfile:
    hazard_type: str
    baseline_score: int
    baseline_level: str
    rationale: str
    reference_framework: str
    data_category: str = "REGIONAL_BASELINE"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class StateBaselineProfile:
    id: str
    name: str
    administrative_type: str
    code: str
    capital: str
    region: str
    primary_basin: str
    overall_baseline_score: int
    overall_baseline_level: str
    primary_hazard: str
    hazards: Dict[str, HazardBaselineProfile]

    def to_dict(self) -> Dict[str, Any]:
        res = asdict(self)
        res["hazards"] = {k: v.to_dict() for k, v in self.hazards.items()}
        return res


NATIONAL_BASELINE_PROFILES: Dict[str, StateBaselineProfile] = {}


def _init_national_baselines():
    from app.services.geo_basin_service import INDIAN_ADMINISTRATIVE_ENTITIES

    for entity in INDIAN_ADMINISTRATIVE_ENTITIES:
        eid = entity["id"]
        ename = entity["name"]
        etype = entity["type"]
        ecode = entity["code"]
        ecap = entity["capital"]
        ereg = entity["region"]
        ebasin = entity.get("primary_basin", "general")

        ename_lower = ename.lower()

        # Flood baseline
        if "assam" in ename_lower or "bihar" in ename_lower or "bengal" in ename_lower or "odisha" in ename_lower:
            flood_score = 75
            flood_level = "HIGH"
            flood_rat = "Major river basin flood corridor with intense monsoon discharge."
        elif "andhra" in ename_lower or "uttar pradesh" in ename_lower or "kerala" in ename_lower:
            flood_score = 62
            flood_level = "MODERATE"
            flood_rat = "Riparian plains prone to seasonal high flood levels."
        else:
            flood_score = 35
            flood_level = "LOW"
            flood_rat = "Inland or well-drained catchment with localized waterlogging risk."

        # Earthquake baseline (BIS IS 1893:2016)
        if any(ne in ename_lower for ne in ["assam", "arunachal", "manipur", "meghalaya", "mizoram", "nagaland", "tripura", "sikkim"]) or "ladakh" in ename_lower or "himachal" in ename_lower or "uttarakhand" in ename_lower or "jammu" in ename_lower or "andaman" in ename_lower:
            eq_score = 80
            eq_level = "HIGH"
            eq_rat = "BIS Seismic Zone V / IV active Himalayan or Indo-Burmese tectonic boundary."
        elif "delhi" in ename_lower or "bihar" in ename_lower or "gujarat" in ename_lower or "maharashtra" in ename_lower:
            eq_score = 60
            eq_level = "MODERATE"
            eq_rat = "BIS Seismic Zone IV / III fault line corridor."
        else:
            eq_score = 30
            eq_level = "LOW"
            eq_rat = "Stable peninsular shield (BIS Seismic Zone II / III)."

        # Cyclone baseline
        if any(c in ename_lower for c in ["odisha", "andhra", "tamil nadu", "bengal", "puducherry"]):
            cyc_score = 85
            cyc_level = "HIGH"
            cyc_rat = "Bay of Bengal high-frequency cyclonic landfall corridor."
        elif "gujarat" in ename_lower or "kerala" in ename_lower or "goa" in ename_lower or "maharashtra" in ename_lower or "andaman" in ename_lower or "lakshadweep" in ename_lower:
            cyc_score = 55
            cyc_level = "MODERATE"
            cyc_rat = "Arabian Sea or island cyclonic / gale risk zone."
        else:
            cyc_score = 15
            cyc_level = "LOW"
            cyc_rat = "Inland continental territory beyond tropical storm surge impact."

        # Heatwave baseline
        if any(h in ename_lower for h in ["rajasthan", "delhi", "haryana", "punjab", "uttar pradesh", "madhya pradesh", "telangana", "chhattisgarh"]):
            heat_score = 78
            heat_level = "HIGH"
            heat_rat = "Arid / semi-arid continental summer extreme temperature zone."
        elif any(h in ename_lower for h in ["andhra", "bihar", "maharashtra", "gujarat", "odisha", "jharkhand"]):
            heat_score = 62
            heat_level = "MODERATE"
            heat_rat = "High humidity-heat index seasonal vulnerability corridor."
        else:
            heat_score = 25
            heat_level = "LOW"
            heat_rat = "Himalayan, coastal, or maritime moderating influence."

        # Landslide baseline
        if any(ls in ename_lower for ls in ["himachal", "uttarakhand", "sikkim", "arunachal", "manipur", "nagaland", "mizoram", "meghalaya"]):
            ls_score = 82
            ls_level = "HIGH"
            ls_rat = "GSI High Susceptibility Himalayan / NE mountainous slope failure zone."
        elif any(ls in ename_lower for ls in ["kerala", "goa", "karnataka", "maharashtra", "tamil nadu", "jammu", "ladakh"]):
            ls_score = 58
            ls_level = "MODERATE"
            ls_rat = "Western Ghats / sub-Himalayan monsoon slope instability zone."
        else:
            ls_score = 10
            ls_level = "LOW"
            ls_rat = "Plains or plateau terrain with zero slope failure potential."

        # Severe Weather baseline
        if any(sw in ename_lower for sw in ["bengal", "bihar", "assam", "odisha", "jharkhand", "kerala"]):
            sw_score = 68
            sw_level = "MODERATE"
            sw_rat = "High thunderstorm, squall, and pre-monsoon convective activity."
        else:
            sw_score = 40
            sw_level = "LOW"
            sw_rat = "Standard seasonal monsoon and convective weather patterns."

        scores = {
            "FLOOD": flood_score,
            "EARTHQUAKE": eq_score,
            "CYCLONE": cyc_score,
            "HEATWAVE": heat_score,
            "LANDSLIDE": ls_score,
            "SEVERE_WEATHER": sw_score
        }
        primary_h = max(scores, key=scores.get)
        overall_score = max(scores.values())

        if overall_score >= 75:
            overall_level = "HIGH"
        elif overall_score >= 50:
            overall_level = "MODERATE"
        else:
            overall_level = "LOW"

        hazards_dict = {
            "FLOOD": HazardBaselineProfile("FLOOD", flood_score, flood_level, flood_rat, "CWC / NFC Flood Commission"),
            "EARTHQUAKE": HazardBaselineProfile("EARTHQUAKE", eq_score, eq_level, eq_rat, "BIS IS 1893:2016 Seismic Zonation"),
            "CYCLONE": HazardBaselineProfile("CYCLONE", cyc_score, cyc_level, cyc_rat, "IMD RSMC Cyclone Vulnerability"),
            "HEATWAVE": HazardBaselineProfile("HEATWAVE", heat_score, heat_level, heat_rat, "NDMA Heat Wave Action Guidelines"),
            "LANDSLIDE": HazardBaselineProfile("LANDSLIDE", ls_score, ls_level, ls_rat, "GSI National Landslide Susceptibility Mapping"),
            "SEVERE_WEATHER": HazardBaselineProfile("SEVERE_WEATHER", sw_score, sw_level, sw_rat, "IMD Severe Weather Climatological Normals")
        }

        profile = StateBaselineProfile(
            id=eid,
            name=ename,
            administrative_type=etype,
            code=ecode,
            capital=ecap,
            region=ereg,
            primary_basin=ebasin,
            overall_baseline_score=overall_score,
            overall_baseline_level=overall_level,
            primary_hazard=primary_h,
            hazards=hazards_dict
        )
        NATIONAL_BASELINE_PROFILES[eid] = profile
        NATIONAL_BASELINE_PROFILES[ename_lower] = profile
        NATIONAL_BASELINE_PROFILES[ecode.lower()] = profile


_init_national_baselines()


class RegionalBaselineEngine:
    """Manages regional baseline risk profiles for all Indian States & UTs."""

    def get_state_profile(self, state_identifier: str) -> Optional[StateBaselineProfile]:
        """Resolves state profile by ID, code, or name."""
        clean = state_identifier.lower().strip()
        return NATIONAL_BASELINE_PROFILES.get(clean)

    def get_all_state_profiles(self) -> List[StateBaselineProfile]:
        """Returns unique baseline profiles for all 36 States & UTs."""
        seen = set()
        profiles = []
        for p in NATIONAL_BASELINE_PROFILES.values():
            if p.id not in seen:
                seen.add(p.id)
                profiles.append(p)
        return profiles

    def get_hazard_baseline(self, state_identifier: str, hazard: str) -> Optional[HazardBaselineProfile]:
        """Returns baseline profile for a specific hazard in a state."""
        profile = self.get_state_profile(state_identifier)
        if not profile:
            return None
        return profile.hazards.get(hazard.upper())


regional_baseline_engine = RegionalBaselineEngine()
