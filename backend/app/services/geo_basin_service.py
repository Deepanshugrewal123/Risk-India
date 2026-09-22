"""
RISK // INDIA — National Geographic Normalization & River Basin Foundation
==========================================================================
Provides authoritative normalization for India's 28 States, 8 Union Territories,
and 12 Major River Basins.

SCIENTIFIC & ARCHITECTURAL HONESTY:
- Administrative entities strictly reflect the official 28 States and 8 Union Territories
  (post-2020 merger of Dadra & Nagar Haveli and Daman & Diu).
- River basin mapping provides spatial/hydrological indexing across the subcontinent.
- Basin mapping does NOT claim or imply trained ML prediction capability.
- Empirical ML prediction remains strictly bounded to the Assam prototype (assam_flood_prototype_v1).
"""

from typing import Dict, Any, Optional, List, Tuple

# Exactly 28 States and 8 Union Territories = 36 Entities
INDIAN_ADMINISTRATIVE_ENTITIES: List[Dict[str, Any]] = [
    # 28 States
    {"id": "andhra-pradesh", "name": "Andhra Pradesh", "type": "STATE", "code": "AP", "capital": "Amaravati", "region": "South India", "primary_basin": "godavari"},
    {"id": "arunachal-pradesh", "name": "Arunachal Pradesh", "type": "STATE", "code": "AR", "capital": "Itanagar", "region": "Northeast India", "primary_basin": "brahmaputra"},
    {"id": "assam", "name": "Assam", "type": "STATE", "code": "AS", "capital": "Dispur", "region": "Northeast India", "primary_basin": "brahmaputra"},
    {"id": "bihar", "name": "Bihar", "type": "STATE", "code": "BR", "capital": "Patna", "region": "East India", "primary_basin": "ganga"},
    {"id": "chhattisgarh", "name": "Chhattisgarh", "type": "STATE", "code": "CG", "capital": "Raipur", "region": "Central India", "primary_basin": "mahanadi"},
    {"id": "goa", "name": "Goa", "type": "STATE", "code": "GA", "capital": "Panaji", "region": "West India", "primary_basin": "coastal"},
    {"id": "gujarat", "name": "Gujarat", "type": "STATE", "code": "GJ", "capital": "Gandhinagar", "region": "West India", "primary_basin": "narmada"},
    {"id": "haryana", "name": "Haryana", "type": "STATE", "code": "HR", "capital": "Chandigarh", "region": "North India", "primary_basin": "indus"},
    {"id": "himachal-pradesh", "name": "Himachal Pradesh", "type": "STATE", "code": "HP", "capital": "Shimla", "region": "North India", "primary_basin": "indus"},
    {"id": "jharkhand", "name": "Jharkhand", "type": "STATE", "code": "JH", "capital": "Ranchi", "region": "East India", "primary_basin": "ganga"},
    {"id": "karnataka", "name": "Karnataka", "type": "STATE", "code": "KA", "capital": "Bengaluru", "region": "South India", "primary_basin": "krishna"},
    {"id": "kerala", "name": "Kerala", "type": "STATE", "code": "KL", "capital": "Thiruvananthapuram", "region": "South India", "primary_basin": "coastal"},
    {"id": "madhya-pradesh", "name": "Madhya Pradesh", "type": "STATE", "code": "MP", "capital": "Bhopal", "region": "Central India", "primary_basin": "narmada"},
    {"id": "maharashtra", "name": "Maharashtra", "type": "STATE", "code": "MH", "capital": "Mumbai", "region": "West India", "primary_basin": "godavari"},
    {"id": "manipur", "name": "Manipur", "type": "STATE", "code": "MN", "capital": "Imphal", "region": "Northeast India", "primary_basin": "barak_others"},
    {"id": "meghalaya", "name": "Meghalaya", "type": "STATE", "code": "ML", "capital": "Shillong", "region": "Northeast India", "primary_basin": "brahmaputra"},
    {"id": "mizoram", "name": "Mizoram", "type": "STATE", "code": "MZ", "capital": "Aizawl", "region": "Northeast India", "primary_basin": "barak_others"},
    {"id": "nagaland", "name": "Nagaland", "type": "STATE", "code": "NL", "capital": "Kohima", "region": "Northeast India", "primary_basin": "brahmaputra"},
    {"id": "odisha", "name": "Odisha", "type": "STATE", "code": "OD", "capital": "Bhubaneswar", "region": "East India", "primary_basin": "mahanadi"},
    {"id": "punjab", "name": "Punjab", "type": "STATE", "code": "PB", "capital": "Chandigarh", "region": "North India", "primary_basin": "indus"},
    {"id": "rajasthan", "name": "Rajasthan", "type": "STATE", "code": "RJ", "capital": "Jaipur", "region": "Northwest India", "primary_basin": "indus"},
    {"id": "sikkim", "name": "Sikkim", "type": "STATE", "code": "SK", "capital": "Gangtok", "region": "Northeast India", "primary_basin": "brahmaputra"},
    {"id": "tamil-nadu", "name": "Tamil Nadu", "type": "STATE", "code": "TN", "capital": "Chennai", "region": "South India", "primary_basin": "cauvery"},
    {"id": "telangana", "name": "Telangana", "type": "STATE", "code": "TS", "capital": "Hyderabad", "region": "South India", "primary_basin": "godavari"},
    {"id": "tripura", "name": "Tripura", "type": "STATE", "code": "TR", "capital": "Agartala", "region": "Northeast India", "primary_basin": "barak_others"},
    {"id": "uttar-pradesh", "name": "Uttar Pradesh", "type": "STATE", "code": "UP", "capital": "Lucknow", "region": "North India", "primary_basin": "ganga"},
    {"id": "uttarakhand", "name": "Uttarakhand", "type": "STATE", "code": "UK", "capital": "Dehradun", "region": "North India", "primary_basin": "ganga"},
    {"id": "west-bengal", "name": "West Bengal", "type": "STATE", "code": "WB", "capital": "Kolkata", "region": "East India", "primary_basin": "ganga"},
    # 8 Union Territories
    {"id": "andaman-nicobar", "name": "Andaman and Nicobar Islands", "type": "UNION_TERRITORY", "code": "AN", "capital": "Port Blair", "region": "Bay of Bengal", "primary_basin": "coastal"},
    {"id": "chandigarh", "name": "Chandigarh", "type": "UNION_TERRITORY", "code": "CH", "capital": "Chandigarh", "region": "North India", "primary_basin": "indus"},
    {"id": "dadra-nagar-haveli-daman-diu", "name": "Dadra and Nagar Haveli and Daman and Diu", "type": "UNION_TERRITORY", "code": "DN", "capital": "Daman", "region": "West India", "primary_basin": "coastal"},
    {"id": "delhi", "name": "Delhi (NCT)", "type": "UNION_TERRITORY", "code": "DL", "capital": "New Delhi", "region": "North India", "primary_basin": "ganga"},
    {"id": "jammu-kashmir", "name": "Jammu and Kashmir", "type": "UNION_TERRITORY", "code": "JK", "capital": "Srinagar / Jammu", "region": "North India", "primary_basin": "indus"},
    {"id": "ladakh", "name": "Ladakh", "type": "UNION_TERRITORY", "code": "LA", "capital": "Leh", "region": "North India", "primary_basin": "indus"},
    {"id": "lakshadweep", "name": "Lakshadweep", "type": "UNION_TERRITORY", "code": "LD", "capital": "Kavaratti", "region": "Arabian Sea", "primary_basin": "coastal"},
    {"id": "puducherry", "name": "Puducherry", "type": "UNION_TERRITORY", "code": "PY", "capital": "Puducherry", "region": "South India", "primary_basin": "cauvery"}
]

# Major River Basins of India
RIVER_BASINS_CATALOG: Dict[str, Dict[str, Any]] = {
    "brahmaputra": {
        "basin_id": "brahmaputra",
        "basin_name": "Brahmaputra Basin",
        "major_river": "Brahmaputra",
        "drainage_area_sqkm": 194413,
        "riparian_states": ["Assam", "Arunachal Pradesh", "Meghalaya", "Nagaland", "Sikkim", "West Bengal"],
        "sub_basins": [
            {"id": "upper_brahmaputra", "name": "Upper Brahmaputra (Siang / Dihang)"},
            {"id": "dhansiri_catchment", "name": "Dhansiri Catchment"},
            {"id": "subansiri_catchment", "name": "Subansiri Catchment"},
            {"id": "jia_bharali_catchment", "name": "Jia-Bharali Catchment"},
            {"id": "manas_beki_catchment", "name": "Manas-Beki Catchment"},
            {"id": "tangni_catchment", "name": "Tangni Catchment"},
            {"id": "boko_catchment", "name": "Boko Catchment"}
        ],
        "ml_readiness": "PROTOTYPE_ACTIVE (Assam Gauge Corridors)",
        "active_models": ["assam_flood_prototype_v1"]
    },
    "ganga": {
        "basin_id": "ganga",
        "basin_name": "Ganga Basin",
        "major_river": "Ganga",
        "drainage_area_sqkm": 861452,
        "riparian_states": ["Uttarakhand", "Uttar Pradesh", "Bihar", "West Bengal", "Jharkhand", "Haryana", "Delhi", "Rajasthan", "Madhya Pradesh"],
        "sub_basins": [
            {"id": "upper_ganga", "name": "Upper Ganga (Bhagirathi / Alaknanda)"},
            {"id": "yamuna_sub_basin", "name": "Yamuna Sub-Basin"},
            {"id": "ghaghara_sub_basin", "name": "Ghaghara Sub-Basin"},
            {"id": "kosi_sub_basin", "name": "Kosi Sub-Basin"},
            {"id": "gandak_sub_basin", "name": "Gandak Sub-Basin"},
            {"id": "chambal_sub_basin", "name": "Chambal Sub-Basin"},
            {"id": "son_sub_basin", "name": "Son Sub-Basin"},
            {"id": "lower_ganga_hooghly", "name": "Lower Ganga / Hooghly"}
        ],
        "ml_readiness": "DATA_ACQUISITION_TARGET",
        "active_models": []
    },
    "indus": {
        "basin_id": "indus",
        "basin_name": "Indus Basin (India)",
        "major_river": "Indus",
        "drainage_area_sqkm": 321289,
        "riparian_states": ["Jammu and Kashmir", "Ladakh", "Himachal Pradesh", "Punjab", "Haryana", "Rajasthan", "Chandigarh"],
        "sub_basins": [
            {"id": "jhelum_catchment", "name": "Jhelum Catchment"},
            {"id": "chenab_catchment", "name": "Chenab Catchment"},
            {"id": "ravi_catchment", "name": "Ravi Catchment"},
            {"id": "beas_catchment", "name": "Beas Catchment"},
            {"id": "sutlej_catchment", "name": "Sutlej Catchment"},
            {"id": "upper_indus_leh", "name": "Upper Indus / Suru Catchment"}
        ],
        "ml_readiness": "DATA_ACQUISITION_TARGET",
        "active_models": []
    },
    "godavari": {
        "basin_id": "godavari",
        "basin_name": "Godavari Basin",
        "major_river": "Godavari",
        "drainage_area_sqkm": 312812,
        "riparian_states": ["Maharashtra", "Telangana", "Andhra Pradesh", "Chhattisgarh", "Madhya Pradesh", "Odisha", "Karnataka", "Puducherry"],
        "sub_basins": [
            {"id": "upper_godavari", "name": "Upper Godavari Catchment"},
            {"id": "pranhita_catchment", "name": "Pranhita Catchment"},
            {"id": "indravati_catchment", "name": "Indravati Catchment"},
            {"id": "lower_godavari_delta", "name": "Lower Godavari Delta"}
        ],
        "ml_readiness": "PLANNED_EXPANSION",
        "active_models": []
    },
    "krishna": {
        "basin_id": "krishna",
        "basin_name": "Krishna Basin",
        "major_river": "Krishna",
        "drainage_area_sqkm": 258948,
        "riparian_states": ["Maharashtra", "Karnataka", "Telangana", "Andhra Pradesh"],
        "sub_basins": [
            {"id": "upper_krishna", "name": "Upper Krishna"},
            {"id": "bhima_catchment", "name": "Bhima Catchment"},
            {"id": "tungabhadra_catchment", "name": "Tungabhadra Catchment"},
            {"id": "lower_krishna_delta", "name": "Lower Krishna Delta"}
        ],
        "ml_readiness": "PLANNED_EXPANSION",
        "active_models": []
    },
    "mahanadi": {
        "basin_id": "mahanadi",
        "basin_name": "Mahanadi Basin",
        "major_river": "Mahanadi",
        "drainage_area_sqkm": 141589,
        "riparian_states": ["Chhattisgarh", "Odisha", "Madhya Pradesh", "Jharkhand", "Maharashtra"],
        "sub_basins": [
            {"id": "seonath_catchment", "name": "Seonath Catchment"},
            {"id": "hasdeo_catchment", "name": "Hasdeo Catchment"},
            {"id": "tel_catchment", "name": "Tel Catchment"},
            {"id": "mahanadi_delta", "name": "Mahanadi Delta"}
        ],
        "ml_readiness": "PLANNED_EXPANSION",
        "active_models": []
    },
    "narmada": {
        "basin_id": "narmada",
        "basin_name": "Narmada Basin",
        "major_river": "Narmada",
        "drainage_area_sqkm": 98796,
        "riparian_states": ["Madhya Pradesh", "Gujarat", "Maharashtra", "Chhattisgarh"],
        "sub_basins": [
            {"id": "upper_narmada", "name": "Upper Narmada Catchment"},
            {"id": "middle_narmada", "name": "Middle Narmada Catchment"},
            {"id": "lower_narmada_estuary", "name": "Lower Narmada Estuary"}
        ],
        "ml_readiness": "PLANNED_EXPANSION",
        "active_models": []
    },
    "tapi": {
        "basin_id": "tapi",
        "basin_name": "Tapi Basin",
        "major_river": "Tapi",
        "drainage_area_sqkm": 65145,
        "riparian_states": ["Maharashtra", "Madhya Pradesh", "Gujarat"],
        "sub_basins": [
            {"id": "upper_tapi", "name": "Upper Tapi"},
            {"id": "purna_catchment", "name": "Purna Catchment"},
            {"id": "lower_tapi_surat", "name": "Lower Tapi (Surat)"}
        ],
        "ml_readiness": "PLANNED_EXPANSION",
        "active_models": []
    },
    "cauvery": {
        "basin_id": "cauvery",
        "basin_name": "Cauvery (Kaveri) Basin",
        "major_river": "Cauvery",
        "drainage_area_sqkm": 81155,
        "riparian_states": ["Karnataka", "Tamil Nadu", "Kerala", "Puducherry"],
        "sub_basins": [
            {"id": "kabini_catchment", "name": "Kabini Catchment"},
            {"id": "bhavani_catchment", "name": "Bhavani Catchment"},
            {"id": "cauvery_delta", "name": "Cauvery Delta"}
        ],
        "ml_readiness": "PLANNED_EXPANSION",
        "active_models": []
    },
    "barak_others": {
        "basin_id": "barak_others",
        "basin_name": "Barak and Others Basin",
        "major_river": "Barak",
        "drainage_area_sqkm": 41723,
        "riparian_states": ["Assam", "Manipur", "Mizoram", "Tripura", "Meghalaya", "Nagaland"],
        "sub_basins": [
            {"id": "barak_valley_cachar", "name": "Barak Valley (Cachar / Karimganj)"},
            {"id": "chindwin_tributaries", "name": "Chindwin Drainage System"}
        ],
        "ml_readiness": "PROTOTYPE_ASSOCIATED (Cachar / Karimganj gauges)",
        "active_models": ["assam_flood_prototype_v1"]
    },
    "coastal": {
        "basin_id": "coastal",
        "basin_name": "Coastal and Island Drainage Basins",
        "major_river": "Various Coastal Streams",
        "drainage_area_sqkm": 150000,
        "riparian_states": ["Kerala", "Goa", "Gujarat", "Andhra Pradesh", "Tamil Nadu", "Odisha", "West Bengal", "Andaman and Nicobar Islands", "Lakshadweep"],
        "sub_basins": [
            {"id": "west_flowing_western_ghats", "name": "West Flowing Rivers (Western Ghats)"},
            {"id": "east_flowing_coromandel", "name": "East Flowing Rivers (Coromandel / Bay of Bengal)"}
        ],
        "ml_readiness": "NOT_AVAILABLE",
        "active_models": []
    }
}


class GeoBasinService:
    """Service providing geographic normalization and river basin resolution across India."""

    @staticmethod
    def get_administrative_count() -> Dict[str, int]:
        """Returns verified count of Indian administrative entities."""
        states = [e for e in INDIAN_ADMINISTRATIVE_ENTITIES if e["type"] == "STATE"]
        uts = [e for e in INDIAN_ADMINISTRATIVE_ENTITIES if e["type"] == "UNION_TERRITORY"]
        return {
            "states": len(states),
            "union_territories": len(uts),
            "total": len(INDIAN_ADMINISTRATIVE_ENTITIES)
        }

    @staticmethod
    def normalize_location(query: str) -> Optional[Dict[str, Any]]:
        """
        Normalizes state or union territory name, code, or alias to canonical administrative record.
        Handles Dadra and Nagar Haveli and Daman and Diu legacy codes (DNH, DD, DN).
        """
        if not query:
            return None
        q = query.strip().lower()

        # Handle Dadra and Nagar Haveli / Daman and Diu merger aliases
        if "dadra" in q or "daman" in q or "diu" in q or q in ["dn", "dnh", "dd"]:
            return next((e for e in INDIAN_ADMINISTRATIVE_ENTITIES if e["id"] == "dadra-nagar-haveli-daman-diu"), None)

        for ent in INDIAN_ADMINISTRATIVE_ENTITIES:
            if (
                ent["id"] == q
                or ent["name"].lower() == q
                or ent["code"].lower() == q
                or ent["capital"].lower() == q
            ):
                return ent

        # Substring search
        for ent in INDIAN_ADMINISTRATIVE_ENTITIES:
            if q in ent["name"].lower() or ent["name"].lower() in q:
                return ent

        return None

    @staticmethod
    def get_basin_for_location(
        state: str,
        district: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Resolves the hydrological river basin context for a given Indian geographic location.
        """
        st_clean = (state or "").lower().strip()
        dist_clean = (district or "").lower().strip()

        # 1. District-level hydrological overrides
        # Assam Brahmaputra vs Barak Valley
        if "cachar" in dist_clean or "karimganj" in dist_clean or "hailakandi" in dist_clean:
            basin = RIVER_BASINS_CATALOG["barak_others"]
            return {
                "basin_id": basin["basin_id"],
                "basin_name": basin["basin_name"],
                "sub_basin": "Barak Valley (Cachar / Karimganj)",
                "ml_readiness": basin["ml_readiness"],
                "is_ml_supported": True
            }

        if "assam" in st_clean or st_clean == "as":
            basin = RIVER_BASINS_CATALOG["brahmaputra"]
            return {
                "basin_id": basin["basin_id"],
                "basin_name": basin["basin_name"],
                "sub_basin": f"{district.capitalize() if district else 'Assam Valley'} Catchment",
                "ml_readiness": basin["ml_readiness"],
                "is_ml_supported": True
            }

        # Delhi Yamuna Basin
        if "delhi" in st_clean or st_clean == "dl":
            basin = RIVER_BASINS_CATALOG["ganga"]
            return {
                "basin_id": basin["basin_id"],
                "basin_name": basin["basin_name"],
                "sub_basin": "Yamuna Sub-Basin",
                "ml_readiness": basin["ml_readiness"],
                "is_ml_supported": False
            }

        # 2. State-level administrative default
        norm = GeoBasinService.normalize_location(st_clean)
        if norm and norm.get("primary_basin") in RIVER_BASINS_CATALOG:
            b_key = norm["primary_basin"]
            basin = RIVER_BASINS_CATALOG[b_key]
            return {
                "basin_id": basin["basin_id"],
                "basin_name": basin["basin_name"],
                "sub_basin": basin["sub_basins"][0]["name"] if basin["sub_basins"] else "Main Catchment",
                "ml_readiness": basin["ml_readiness"],
                "is_ml_supported": False
            }

        # 3. Default fallback
        return {
            "basin_id": "subcontinental_drainage",
            "basin_name": "Indian Drainage System",
            "sub_basin": "Regional Watershed",
            "ml_readiness": "DATA_ACQUISITION_TARGET",
            "is_ml_supported": False
        }

    @staticmethod
    def get_all_basins() -> List[Dict[str, Any]]:
        """Returns the full river basin catalog."""
        return list(RIVER_BASINS_CATALOG.values())

    @staticmethod
    def get_basin(basin_id: str) -> Optional[Dict[str, Any]]:
        """Returns metadata for a specific river basin by id."""
        if not basin_id:
            return None
        return RIVER_BASINS_CATALOG.get(basin_id.lower().strip())


geo_basin_service = GeoBasinService()
