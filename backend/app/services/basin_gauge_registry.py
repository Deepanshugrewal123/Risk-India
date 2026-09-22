"""
RISK // INDIA — Canonical River Basin Gauge Registry
=====================================================
Maintains authoritative metadata for Central Water Commission (CWC) and India-WRIS
river monitoring stations across major Indian river basins.

SCIENTIFIC PRINCIPLES:
- All station metadata reflects official CWC Flood Forecasting Network designations.
- Warning Levels (WL), Danger Levels (DL), and High Flood Levels (HFL) are recorded in meters
  above Mean Sea Level (MSL) or relative to gauge zero datum.
- Gauge registries establish the spatial and observational foundation for future empirical modeling.
- Merely having a gauge registered does NOT imply ML prediction capability.
  ML readiness is determined solely by the MLReadinessGate.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import math
import logging

logger = logging.getLogger("basin-gauge-registry")


@dataclass
class BasinGaugeStation:
    station_id: str
    station_name: str
    basin_id: str
    sub_basin: str
    river_name: str
    state: str
    district: str
    latitude: float
    longitude: float
    elevation_msl_m: Optional[float]
    warning_level_m: float
    danger_level_m: float
    hfl_m: Optional[float]
    hfl_date: Optional[str]
    zero_datum_m: Optional[float]
    agency: str = "Central Water Commission (CWC) / India-WRIS"
    source_url: str = "https://ffs.india-water.gov.in"
    historical_period: str = "1986–Present"
    availability_status: str = "CALIBRATED_ACTIVE"
    station_type: str = "LEVEL_AND_RAINFALL"  # LEVEL, LEVEL_AND_RAINFALL, DISCHARGE
    status: str = "ACTIVE_CALIBRATED"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# Canonical CWC Monitoring Stations for Godavari, Mahanadi, and Brahmaputra Basins
CANONICAL_BASIN_GAUGES: List[BasinGaugeStation] = [
    # -------------------------------------------------------------------------
    # GODAVARI BASIN (Drainage Area: 312,812 sq km)
    # Riparian States: Maharashtra, Telangana, Andhra Pradesh, Chhattisgarh,
    #                  Madhya Pradesh, Odisha, Karnataka, Puducherry
    # -------------------------------------------------------------------------
    BasinGaugeStation(
        station_id="CWC-GD-001",
        station_name="Bhadrachalam",
        basin_id="godavari",
        sub_basin="pranhita_catchment",
        river_name="Godavari",
        state="Telangana",
        district="Bhadradri Kothagudem",
        latitude=17.6688,
        longitude=80.8936,
        elevation_msl_m=42.0,
        warning_level_m=14.63,  # 48.0 feet
        danger_level_m=16.15,   # 53.0 feet
        hfl_m=21.82,            # 71.6 feet (Record 1986 flood)
        hfl_date="1986-08-16",
        zero_datum_m=33.53,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-GD-002",
        station_name="Dowleswaram Barrage (Rajahmundry)",
        basin_id="godavari",
        sub_basin="lower_godavari_delta",
        river_name="Godavari",
        state="Andhra Pradesh",
        district="East Godavari",
        latitude=16.9441,
        longitude=81.7699,
        elevation_msl_m=12.5,
        warning_level_m=3.05,   # 10.0 feet (1st warning)
        danger_level_m=3.96,    # 13.0 feet (2nd warning)
        hfl_m=5.33,             # 17.5 feet (3rd warning / extreme)
        hfl_date="2006-08-08",
        zero_datum_m=9.45,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-GD-003",
        station_name="Polavaram",
        basin_id="godavari",
        sub_basin="lower_godavari_delta",
        river_name="Godavari",
        state="Andhra Pradesh",
        district="Eluru",
        latitude=17.2589,
        longitude=81.6508,
        elevation_msl_m=22.0,
        warning_level_m=27.50,
        danger_level_m=28.00,
        hfl_m=29.20,
        hfl_date="2022-07-16",
        zero_datum_m=15.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-GD-004",
        station_name="Perur",
        basin_id="godavari",
        sub_basin="pranhita_catchment",
        river_name="Godavari",
        state="Telangana",
        district="Bhadradri Kothagudem",
        latitude=18.5500,
        longitude=80.4000,
        elevation_msl_m=71.0,
        warning_level_m=74.00,
        danger_level_m=75.00,
        hfl_m=77.85,
        hfl_date="2013-08-03",
        zero_datum_m=65.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-GD-005",
        station_name="Nanded",
        basin_id="godavari",
        sub_basin="upper_godavari",
        river_name="Godavari",
        state="Maharashtra",
        district="Nanded",
        latitude=19.1500,
        longitude=77.3167,
        elevation_msl_m=351.0,
        warning_level_m=353.00,
        danger_level_m=354.00,
        hfl_m=356.10,
        hfl_date="2006-08-07",
        zero_datum_m=345.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-GD-006",
        station_name="Kaleshwaram (Medigadda Confluence)",
        basin_id="godavari",
        sub_basin="pranhita_catchment",
        river_name="Godavari",
        state="Telangana",
        district="Jayashankar Bhupalpally",
        latitude=18.8167,
        longitude=79.9000,
        elevation_msl_m=96.0,
        warning_level_m=99.00,
        danger_level_m=100.00,
        hfl_m=102.50,
        hfl_date="2022-07-14",
        zero_datum_m=90.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-GD-007",
        station_name="Mancherial",
        basin_id="godavari",
        sub_basin="upper_godavari",
        river_name="Godavari",
        state="Telangana",
        district="Mancherial",
        latitude=18.8679,
        longitude=79.4639,
        elevation_msl_m=129.0,
        warning_level_m=132.50,
        danger_level_m=134.00,
        hfl_m=136.20,
        hfl_date="2020-08-18",
        zero_datum_m=125.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-GD-008",
        station_name="Jagdalpur",
        basin_id="godavari",
        sub_basin="indravati_catchment",
        river_name="Indravati",
        state="Chhattisgarh",
        district="Bastar",
        latitude=19.0733,
        longitude=82.0167,
        elevation_msl_m=548.0,
        warning_level_m=552.00,
        danger_level_m=554.00,
        hfl_m=556.80,
        hfl_date="2010-09-12",
        zero_datum_m=540.00,
        station_type="LEVEL_AND_RAINFALL"
    ),

    # -------------------------------------------------------------------------
    # MAHANADI BASIN (Drainage Area: 141,589 sq km)
    # Riparian States: Chhattisgarh, Odisha, Madhya Pradesh, Jharkhand, Maharashtra
    # -------------------------------------------------------------------------
    BasinGaugeStation(
        station_id="CWC-MH-001",
        station_name="Hirakud Dam (Sambalpur)",
        basin_id="mahanadi",
        sub_basin="hasdeo_catchment",
        river_name="Mahanadi",
        state="Odisha",
        district="Sambalpur",
        latitude=21.5700,
        longitude=83.8700,
        elevation_msl_m=190.0,
        warning_level_m=191.00,
        danger_level_m=192.02,  # Full Reservoir Level 630.0 ft
        hfl_m=192.33,
        hfl_date="2011-09-10",
        zero_datum_m=175.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-MH-002",
        station_name="Naraj Barrage",
        basin_id="mahanadi",
        sub_basin="mahanadi_delta",
        river_name="Mahanadi / Kathajodi",
        state="Odisha",
        district="Cuttack",
        latitude=20.4639,
        longitude=85.7761,
        elevation_msl_m=23.0,
        warning_level_m=25.41,
        danger_level_m=26.41,
        hfl_m=27.60,
        hfl_date="2008-09-22",
        zero_datum_m=18.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-MH-003",
        station_name="Tikarpara",
        basin_id="mahanadi",
        sub_basin="hasdeo_catchment",
        river_name="Mahanadi",
        state="Odisha",
        district="Angul",
        latitude=20.6000,
        longitude=84.7833,
        elevation_msl_m=65.0,
        warning_level_m=69.50,
        danger_level_m=70.50,
        hfl_m=72.80,
        hfl_date="2011-09-11",
        zero_datum_m=60.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-MH-004",
        station_name="Khairmal",
        basin_id="mahanadi",
        sub_basin="tel_catchment",
        river_name="Mahanadi",
        state="Odisha",
        district="Boudh",
        latitude=20.8000,
        longitude=84.1500,
        elevation_msl_m=102.0,
        warning_level_m=106.00,
        danger_level_m=107.00,
        hfl_m=108.95,
        hfl_date="2008-09-21",
        zero_datum_m=98.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-MH-005",
        station_name="Rajim",
        basin_id="mahanadi",
        sub_basin="seonath_catchment",
        river_name="Mahanadi",
        state="Chhattisgarh",
        district="Gariaband",
        latitude=20.9667,
        longitude=81.8833,
        elevation_msl_m=276.0,
        warning_level_m=280.00,
        danger_level_m=281.50,
        hfl_m=283.40,
        hfl_date="2014-08-04",
        zero_datum_m=270.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-MH-006",
        station_name="Sheorinarayan",
        basin_id="mahanadi",
        sub_basin="seonath_catchment",
        river_name="Mahanadi / Seonath Confluence",
        state="Chhattisgarh",
        district="Janjgir-Champa",
        latitude=21.7167,
        longitude=82.6000,
        elevation_msl_m=224.0,
        warning_level_m=228.00,
        danger_level_m=229.50,
        hfl_m=231.20,
        hfl_date="2018-09-06",
        zero_datum_m=218.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-MH-007",
        station_name="Barmul",
        basin_id="mahanadi",
        sub_basin="mahanadi_delta",
        river_name="Mahanadi",
        state="Odisha",
        district="Nayagarh",
        latitude=20.4500,
        longitude=85.1833,
        elevation_msl_m=38.0,
        warning_level_m=41.50,
        danger_level_m=42.50,
        hfl_m=44.10,
        hfl_date="2008-09-22",
        zero_datum_m=34.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-MH-008",
        station_name="Simga",
        basin_id="mahanadi",
        sub_basin="seonath_catchment",
        river_name="Seonath",
        state="Chhattisgarh",
        district="Baloda Bazar",
        latitude=21.6333,
        longitude=81.7000,
        elevation_msl_m=258.0,
        warning_level_m=262.50,
        danger_level_m=264.00,
        hfl_m=266.30,
        hfl_date="2016-08-10",
        zero_datum_m=250.00,
        station_type="LEVEL_AND_RAINFALL"
    ),

    # -------------------------------------------------------------------------
    # BRAHMAPUTRA BASIN (Assam Empirical Reference Corridors)
    # -------------------------------------------------------------------------
    BasinGaugeStation(
        station_id="CWC-BP-001",
        station_name="Dhansirighat",
        basin_id="brahmaputra",
        sub_basin="dhansiri_catchment",
        river_name="Dhansiri",
        state="Assam",
        district="Udalguri",
        latitude=26.7380,
        longitude=92.1280,
        elevation_msl_m=68.0,
        warning_level_m=72.00,
        danger_level_m=73.50,
        hfl_m=75.20,
        hfl_date="2022-06-18",
        zero_datum_m=65.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-BP-002",
        station_name="Tangni",
        basin_id="brahmaputra",
        sub_basin="tangni_catchment",
        river_name="Tangni",
        state="Assam",
        district="Darrang",
        latitude=26.5410,
        longitude=91.9830,
        elevation_msl_m=52.0,
        warning_level_m=54.50,
        danger_level_m=56.00,
        hfl_m=57.80,
        hfl_date="2024-07-04",
        zero_datum_m=48.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-BP-003",
        station_name="Boko",
        basin_id="brahmaputra",
        sub_basin="boko_catchment",
        river_name="Boko",
        state="Assam",
        district="Kamrup",
        latitude=26.0120,
        longitude=91.2340,
        elevation_msl_m=44.0,
        warning_level_m=46.50,
        danger_level_m=48.00,
        hfl_m=49.90,
        hfl_date="2022-05-24",
        zero_datum_m=40.00,
        station_type="LEVEL_AND_RAINFALL"
    ),

    # -------------------------------------------------------------------------
    # GANGA BASIN (Drainage Area: 861,452 sq km)
    # Riparian States: Uttarakhand, Uttar Pradesh, Bihar, West Bengal,
    #                  Haryana, Himachal Pradesh, Rajasthan, MP, Chhattisgarh, Jharkhand, Delhi
    # -------------------------------------------------------------------------
    BasinGaugeStation(
        station_id="CWC-GG-001",
        station_name="Haridwar (Upper Ganga)",
        basin_id="ganga",
        sub_basin="upper_ganga_plains",
        river_name="Ganga",
        state="Uttarakhand",
        district="Haridwar",
        latitude=29.9457,
        longitude=78.1642,
        elevation_msl_m=289.0,
        warning_level_m=293.00,
        danger_level_m=294.00,
        hfl_m=296.30,
        hfl_date="2013-06-18",
        zero_datum_m=280.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-GG-002",
        station_name="Prayagraj / Phaphamau",
        basin_id="ganga",
        sub_basin="middle_ganga_plains",
        river_name="Ganga",
        state="Uttar Pradesh",
        district="Prayagraj",
        latitude=25.4358,
        longitude=81.8463,
        elevation_msl_m=76.0,
        warning_level_m=83.73,
        danger_level_m=84.73,
        hfl_m=88.03,
        hfl_date="2019-09-20",
        zero_datum_m=70.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-GG-003",
        station_name="Varanasi",
        basin_id="ganga",
        sub_basin="middle_ganga_plains",
        river_name="Ganga",
        state="Uttar Pradesh",
        district="Varanasi",
        latitude=25.3176,
        longitude=83.0062,
        elevation_msl_m=64.0,
        warning_level_m=70.26,
        danger_level_m=71.26,
        hfl_m=73.90,
        hfl_date="2016-08-25",
        zero_datum_m=58.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-GG-004",
        station_name="Patna / Digha Ghat",
        basin_id="ganga",
        sub_basin="lower_ganga_plains",
        river_name="Ganga",
        state="Bihar",
        district="Patna",
        latitude=25.6320,
        longitude=85.1010,
        elevation_msl_m=45.0,
        warning_level_m=49.52,
        danger_level_m=50.52,
        hfl_m=52.52,
        hfl_date="2016-08-27",
        zero_datum_m=40.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-GG-005",
        station_name="Farakka Barrage",
        basin_id="ganga",
        sub_basin="lower_ganga_plains",
        river_name="Ganga",
        state="West Bengal",
        district="Murshidabad",
        latitude=24.8020,
        longitude=87.9290,
        elevation_msl_m=16.0,
        warning_level_m=21.20,
        danger_level_m=22.25,
        hfl_m=25.00,
        hfl_date="1998-09-12",
        zero_datum_m=10.00,
        station_type="LEVEL_AND_RAINFALL"
    ),

    # -------------------------------------------------------------------------
    # KRISHNA BASIN (Drainage Area: 258,948 sq km)
    # Riparian States: Maharashtra, Karnataka, Telangana, Andhra Pradesh
    # -------------------------------------------------------------------------
    BasinGaugeStation(
        station_id="CWC-KR-001",
        station_name="Almatti Dam",
        basin_id="krishna",
        sub_basin="upper_krishna",
        river_name="Krishna",
        state="Karnataka",
        district="Bagalkot",
        latitude=16.3297,
        longitude=75.8887,
        elevation_msl_m=515.0,
        warning_level_m=518.50,
        danger_level_m=519.60,
        hfl_m=520.00,
        hfl_date="2019-08-10",
        zero_datum_m=500.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-KR-002",
        station_name="Narayanpur Dam",
        basin_id="krishna",
        sub_basin="upper_krishna",
        river_name="Krishna",
        state="Karnataka",
        district="Yadgir",
        latitude=16.2425,
        longitude=76.5867,
        elevation_msl_m=488.0,
        warning_level_m=491.00,
        danger_level_m=492.25,
        hfl_m=493.00,
        hfl_date="2019-08-12",
        zero_datum_m=475.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-KR-003",
        station_name="Srisailam Dam",
        basin_id="krishna",
        sub_basin="middle_krishna",
        river_name="Krishna",
        state="Andhra Pradesh",
        district="Kurnool",
        latitude=16.0883,
        longitude=78.8970,
        elevation_msl_m=260.0,
        warning_level_m=268.00,
        danger_level_m=269.80,
        hfl_m=272.50,
        hfl_date="2009-10-02",
        zero_datum_m=245.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-KR-004",
        station_name="Nagarjuna Sagar Dam",
        basin_id="krishna",
        sub_basin="middle_krishna",
        river_name="Krishna",
        state="Telangana",
        district="Nalgonda",
        latitude=16.5780,
        longitude=79.3130,
        elevation_msl_m=170.0,
        warning_level_m=178.50,
        danger_level_m=179.80,
        hfl_m=181.00,
        hfl_date="2009-10-04",
        zero_datum_m=155.00,
        station_type="LEVEL_AND_RAINFALL"
    ),
    BasinGaugeStation(
        station_id="CWC-KR-005",
        station_name="Vijayawada Prakasham Barrage",
        basin_id="krishna",
        sub_basin="krishna_delta",
        river_name="Krishna",
        state="Andhra Pradesh",
        district="Krishna",
        latitude=16.5062,
        longitude=80.6050,
        elevation_msl_m=1.5,
        warning_level_m=3.66,
        danger_level_m=4.88,
        hfl_m=6.90,
        hfl_date="2009-10-05",
        zero_datum_m=0.00,
        station_type="LEVEL_AND_RAINFALL"
    )
]


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two points in kilometers."""
    r = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


class BasinGaugeRegistry:
    """
    Service for querying, cataloging, and spatially searching CWC river monitoring gauges.
    """
    def __init__(self):
        self._stations: Dict[str, BasinGaugeStation] = {}
        for s in CANONICAL_BASIN_GAUGES:
            self._stations[s.station_id] = s

    def get_all_stations(self) -> List[BasinGaugeStation]:
        return list(self._stations.values())

    def get_station(self, station_id: str) -> Optional[BasinGaugeStation]:
        return self._stations.get(station_id)

    def get_stations_by_basin(self, basin_id: str) -> List[BasinGaugeStation]:
        b_clean = basin_id.lower().strip()
        return [s for s in self._stations.values() if s.basin_id.lower() == b_clean]

    def get_stations_by_state(self, state: str) -> List[BasinGaugeStation]:
        s_clean = state.lower().strip()
        return [s for s in self._stations.values() if s_clean in s.state.lower()]

    def normalize_station(self, query: str) -> Optional[BasinGaugeStation]:
        """
        Normalizes station name variations, identifiers, and aliases to canonical BasinGaugeStation.
        Example: 'Bhadrachalam Gauge', 'BHADRACHALAM', 'CWC_GD_001' -> CWC-GD-001
        """
        if not query:
            return None
        q = query.lower().strip().replace("_", "-").replace(" gauge", "").replace(" station", "").replace(" barrage", "")
        # Exact ID match
        for s in self._stations.values():
            if s.station_id.lower() == q or s.station_id.lower().replace("-", "") == q:
                return s
        # Name match or substring
        for s in self._stations.values():
            s_clean = s.station_name.lower().replace(" barrage", "").replace(" dam", "")
            if q in s_clean or s_clean in q:
                return s
        return None

    def find_nearest_station(
        self,
        lat: float,
        lon: float,
        basin_id: Optional[str] = None,
        max_distance_km: float = 150.0
    ) -> Optional[Dict[str, Any]]:
        """
        Finds the nearest calibrated river gauge within max_distance_km.
        """
        candidates = self.get_stations_by_basin(basin_id) if basin_id else self.get_all_stations()
        if not candidates:
            return None

        best_station: Optional[BasinGaugeStation] = None
        min_dist = float("inf")

        for s in candidates:
            d = haversine_distance_km(lat, lon, s.latitude, s.longitude)
            if d < min_dist and d <= max_distance_km:
                min_dist = d
                best_station = s

        if best_station:
            result = best_station.to_dict()
            result["distance_km"] = round(min_dist, 2)
            return result
        return None

    def get_basin_summary(self, basin_id: str) -> Dict[str, Any]:
        """Returns hydrological station summary for a given basin."""
        stations = self.get_stations_by_basin(basin_id)
        if not stations:
            return {
                "basin_id": basin_id,
                "station_count": 0,
                "stations": [],
                "sub_basins_monitored": []
            }

        sub_basins = sorted(list({s.sub_basin for s in stations}))
        states = sorted(list({s.state for s in stations}))
        rivers = sorted(list({s.river_name for s in stations}))

        return {
            "basin_id": basin_id,
            "station_count": len(stations),
            "states_covered": states,
            "rivers_monitored": rivers,
            "sub_basins_monitored": sub_basins,
            "stations": [s.to_dict() for s in stations]
        }


basin_gauge_registry = BasinGaugeRegistry()
