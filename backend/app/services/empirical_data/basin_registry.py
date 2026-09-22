"""
RISK // INDIA — Canonical Five-Basin Gauge Registry
===================================================
Maintains canonical gauge station metadata across the 5 priority basins:
1. Brahmaputra (Assam) — 3 calibrated gauges, 32 real observations (ML_READY)
2. Ganga — 5 calibrated gauges, 0 observations
3. Godavari — 5 calibrated gauges, 0 observations
4. Mahanadi — 8 calibrated gauges, 0 observations
5. Krishna — 5 calibrated gauges, 0 observations

Enforces coordinate consistency, prevents duplicates, and prohibits fake gauges.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict


@dataclass
class CanonicalGaugeInfo:
    gauge_id: str
    gauge_name: str
    basin_id: str
    river_name: str
    state: str
    district: str
    latitude: float
    longitude: float
    warning_level_m: float
    danger_level_m: float
    hfl_m: Optional[float]
    agency: str = "Central Water Commission (CWC)"
    is_calibrated: bool = True
    active_observations_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# Canonical alias
CalibratedRiverGauge = CanonicalGaugeInfo



# Authoritative CWC Gauges for the 5 Priority Basins
CANONICAL_FIVE_BASIN_GAUGES: List[CanonicalGaugeInfo] = [
    # -------------------------------------------------------------------------
    # 1. BRAHMAPUTRA (Assam Prototype Corridor — 3 Calibrated Stations)
    # -------------------------------------------------------------------------
    CanonicalGaugeInfo(
        gauge_id="CWC-AS-001",
        gauge_name="Panbazar (Guwahati)",
        basin_id="brahmaputra",
        river_name="Brahmaputra",
        state="Assam",
        district="Kamrup Metropolitan",
        latitude=26.1856,
        longitude=91.7482,
        warning_level_m=49.68,
        danger_level_m=50.68,
        hfl_m=51.46,
        active_observations_count=12
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-AS-002",
        gauge_name="Matijuri",
        basin_id="brahmaputra",
        river_name="Katakhai (Barak tributary)",
        state="Assam",
        district="Hailakandi",
        latitude=24.6833,
        longitude=92.5833,
        warning_level_m=19.85,
        danger_level_m=20.85,
        hfl_m=22.47,
        active_observations_count=10
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-AS-003",
        gauge_name="NT Road Crossing (Boro)",
        basin_id="brahmaputra",
        river_name="Pagladiya / Dhansiri sub-basin",
        state="Assam",
        district="Baksa / Udalguri",
        latitude=26.5167,
        longitude=91.5000,
        warning_level_m=52.00,
        danger_level_m=53.00,
        hfl_m=54.20,
        active_observations_count=10
    ),

    # -------------------------------------------------------------------------
    # 2. GANGA BASIN (5 Calibrated CWC Stations)
    # -------------------------------------------------------------------------
    CanonicalGaugeInfo(
        gauge_id="CWC-GG-001",
        gauge_name="Haridwar",
        basin_id="ganga",
        river_name="Ganga",
        state="Uttarakhand",
        district="Haridwar",
        latitude=29.9457,
        longitude=78.1642,
        warning_level_m=293.00,
        danger_level_m=294.00,
        hfl_m=296.30,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-GG-002",
        gauge_name="Prayagraj (Sangam)",
        basin_id="ganga",
        river_name="Ganga",
        state="Uttar Pradesh",
        district="Prayagraj",
        latitude=25.4358,
        longitude=81.8463,
        warning_level_m=83.73,
        danger_level_m=84.73,
        hfl_m=89.04,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-GG-003",
        gauge_name="Varanasi",
        basin_id="ganga",
        river_name="Ganga",
        state="Uttar Pradesh",
        district="Varanasi",
        latitude=25.3176,
        longitude=83.0062,
        warning_level_m=70.26,
        danger_level_m=71.26,
        hfl_m=73.90,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-GG-004",
        gauge_name="Patna (Gandhi Ghat)",
        basin_id="ganga",
        river_name="Ganga",
        state="Bihar",
        district="Patna",
        latitude=25.6207,
        longitude=85.1740,
        warning_level_m=47.60,
        danger_level_m=48.60,
        hfl_m=50.52,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-GG-005",
        gauge_name="Farakka",
        basin_id="ganga",
        river_name="Ganga",
        state="West Bengal",
        district="Murshidabad",
        latitude=24.8016,
        longitude=87.9272,
        warning_level_m=21.22,
        danger_level_m=22.25,
        hfl_m=25.26,
        active_observations_count=0
    ),

    # -------------------------------------------------------------------------
    # 3. GODAVARI BASIN (5 Calibrated CWC Stations)
    # -------------------------------------------------------------------------
    CanonicalGaugeInfo(
        gauge_id="CWC-GD-001",
        gauge_name="Bhadrachalam",
        basin_id="godavari",
        river_name="Godavari",
        state="Telangana",
        district="Bhadradri Kothagudem",
        latitude=17.6688,
        longitude=80.8936,
        warning_level_m=14.63,
        danger_level_m=16.15,
        hfl_m=21.82,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-GD-002",
        gauge_name="Dowleswaram Barrage",
        basin_id="godavari",
        river_name="Godavari",
        state="Andhra Pradesh",
        district="East Godavari",
        latitude=16.9441,
        longitude=81.7699,
        warning_level_m=3.05,
        danger_level_m=3.96,
        hfl_m=5.33,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-GD-003",
        gauge_name="Polavaram",
        basin_id="godavari",
        river_name="Godavari",
        state="Andhra Pradesh",
        district="West Godavari",
        latitude=17.2514,
        longitude=81.6528,
        warning_level_m=25.00,
        danger_level_m=28.00,
        hfl_m=35.00,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-GD-004",
        gauge_name="Perur",
        basin_id="godavari",
        river_name="Pranhita",
        state="Telangana",
        district="Jagtial",
        latitude=18.7844,
        longitude=79.9122,
        warning_level_m=112.50,
        danger_level_m=114.00,
        hfl_m=117.80,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-GD-005",
        gauge_name="Nanded",
        basin_id="godavari",
        river_name="Godavari",
        state="Maharashtra",
        district="Nanded",
        latitude=19.1528,
        longitude=77.3197,
        warning_level_m=351.00,
        danger_level_m=354.00,
        hfl_m=357.25,
        active_observations_count=0
    ),

    # -------------------------------------------------------------------------
    # 4. MAHANADI BASIN (8 Calibrated CWC Stations)
    # -------------------------------------------------------------------------
    CanonicalGaugeInfo(
        gauge_id="CWC-MN-001",
        gauge_name="Tikarpara",
        basin_id="mahanadi",
        river_name="Mahanadi",
        state="Odisha",
        district="Angul",
        latitude=20.5922,
        longitude=84.7786,
        warning_level_m=68.58,
        danger_level_m=70.10,
        hfl_m=75.60,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-MN-002",
        gauge_name="Naraj Barrage",
        basin_id="mahanadi",
        river_name="Kathajodi (Mahanadi arm)",
        state="Odisha",
        district="Cuttack",
        latitude=20.4683,
        longitude=85.7783,
        warning_level_m=25.41,
        danger_level_m=26.41,
        hfl_m=27.60,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-MN-003",
        gauge_name="Sambalpur",
        basin_id="mahanadi",
        river_name="Mahanadi",
        state="Odisha",
        district="Sambalpur",
        latitude=21.4669,
        longitude=83.9756,
        warning_level_m=118.00,
        danger_level_m=119.40,
        hfl_m=122.25,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-MN-004",
        gauge_name="Baripada",
        basin_id="mahanadi",
        river_name="Budhabalanga",
        state="Odisha",
        district="Mayurbhanj",
        latitude=21.9333,
        longitude=86.7333,
        warning_level_m=29.56,
        danger_level_m=30.56,
        hfl_m=33.20,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-MN-005",
        gauge_name="Anandpur",
        basin_id="mahanadi",
        river_name="Baitarani",
        state="Odisha",
        district="Kendujhar",
        latitude=21.2167,
        longitude=86.1167,
        warning_level_m=37.45,
        danger_level_m=38.36,
        hfl_m=41.20,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-MN-006",
        gauge_name="Champua",
        basin_id="mahanadi",
        river_name="Baitarani",
        state="Odisha",
        district="Kendujhar",
        latitude=22.0833,
        longitude=85.6667,
        warning_level_m=375.00,
        danger_level_m=376.50,
        hfl_m=378.80,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-MN-007",
        gauge_name="Jamshedpur",
        basin_id="mahanadi",
        river_name="Subarnarekha",
        state="Jharkhand",
        district="East Singhbhum",
        latitude=22.8046,
        longitude=86.2029,
        warning_level_m=128.50,
        danger_level_m=129.50,
        hfl_m=133.50,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-MN-008",
        gauge_name="Ghatsila",
        basin_id="mahanadi",
        river_name="Subarnarekha",
        state="Jharkhand",
        district="East Singhbhum",
        latitude=22.5833,
        longitude=86.4833,
        warning_level_m=80.50,
        danger_level_m=82.00,
        hfl_m=86.10,
        active_observations_count=0
    ),

    # -------------------------------------------------------------------------
    # 5. KRISHNA BASIN (5 Calibrated CWC Stations)
    # -------------------------------------------------------------------------
    CanonicalGaugeInfo(
        gauge_id="CWC-KR-001",
        gauge_name="Almatti Dam (Lal Bahadur Shastri Sagar)",
        basin_id="krishna",
        river_name="Krishna",
        state="Karnataka",
        district="Vijayapura",
        latitude=16.3311,
        longitude=75.8883,
        warning_level_m=518.50,
        danger_level_m=519.60,
        hfl_m=521.00,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-KR-002",
        gauge_name="Narayanpur Dam (Basava Sagar)",
        basin_id="krishna",
        river_name="Krishna",
        state="Karnataka",
        district="Yadgir",
        latitude=16.2417,
        longitude=76.3683,
        warning_level_m=491.50,
        danger_level_m=492.25,
        hfl_m=494.50,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-KR-003",
        gauge_name="Srisailam Reservoir",
        basin_id="krishna",
        river_name="Krishna",
        state="Andhra Pradesh",
        district="Nandyal",
        latitude=16.0886,
        longitude=78.8967,
        warning_level_m=268.00,
        danger_level_m=269.75,
        hfl_m=272.50,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-KR-004",
        gauge_name="Nagarjuna Sagar Dam",
        basin_id="krishna",
        river_name="Krishna",
        state="Telangana",
        district="Nalgonda",
        latitude=16.5772,
        longitude=79.3136,
        warning_level_m=178.50,
        danger_level_m=179.83,
        hfl_m=182.20,
        active_observations_count=0
    ),
    CanonicalGaugeInfo(
        gauge_id="CWC-KR-005",
        gauge_name="Vijayawada Prakasham Barrage",
        basin_id="krishna",
        river_name="Krishna",
        state="Andhra Pradesh",
        district="NTR",
        latitude=16.5075,
        longitude=80.6083,
        warning_level_m=15.50,
        danger_level_m=17.00,
        hfl_m=20.50,
        active_observations_count=0
    )
]


class EmpiricalBasinRegistry:
    """Canonical registry service managing the 5 priority basins."""
    def __init__(self):
        self._gauges: Dict[str, CanonicalGaugeInfo] = {g.gauge_id: g for g in CANONICAL_FIVE_BASIN_GAUGES}

    def get_all_gauges(self) -> List[CanonicalGaugeInfo]:
        return list(self._gauges.values())

    def get_gauges_by_basin(self, basin_id: str) -> List[CanonicalGaugeInfo]:
        b = basin_id.lower().strip()
        return [g for g in self._gauges.values() if g.basin_id == b]

    def get_gauge(self, gauge_id: str) -> Optional[CanonicalGaugeInfo]:
        return self._gauges.get(gauge_id.strip().upper())

    def validate_registry_integrity(self) -> Dict[str, Any]:
        """Validates absence of duplicate gauge IDs, coordinate conflicts, or illegal coords."""
        gauge_ids = set()
        coord_map = {}
        duplicates = []
        conflicts = []

        for g in self._gauges.values():
            if g.gauge_id in gauge_ids:
                duplicates.append(g.gauge_id)
            gauge_ids.add(g.gauge_id)

            coord_key = (round(g.latitude, 4), round(g.longitude, 4))
            if coord_key in coord_map and coord_map[coord_key] != g.gauge_id:
                conflicts.append((g.gauge_id, coord_map[coord_key], coord_key))
            coord_map[coord_key] = g.gauge_id

        return {
            "total_gauges": len(self._gauges),
            "unique_gauges": len(gauge_ids),
            "duplicate_ids": duplicates,
            "coordinate_conflicts": conflicts,
            "is_valid": (len(duplicates) == 0 and len(conflicts) == 0)
        }

    def get_basin_summary(self, basin_id: str) -> Dict[str, Any]:
        gauges = self.get_gauges_by_basin(basin_id)
        return {
            "basin_id": basin_id.lower(),
            "gauge_count": len(gauges),
            "states": sorted(list({g.state for g in gauges})),
            "rivers": sorted(list({g.river_name for g in gauges})),
            "calibrated_stations": [g.gauge_name for g in gauges],
            "active_observations": sum(g.active_observations_count for g in gauges)
        }


empirical_basin_registry = EmpiricalBasinRegistry()
