"""
RISK // INDIA — Weather Geographic Routing & Spatial Normalizer
===============================================================
Maps weather observations and forecast bulletins to the 28 States and
8 Union Territories (36 administrative entities), major river basins, and districts.
Unmapped locations receive status = UNMAPPED and are never guessed.
"""

from typing import Tuple, Optional, Dict, Any
from app.services.geo_basin_service import INDIAN_ADMINISTRATIVE_ENTITIES
from app.services.empirical_data.normalization import normalize_state_name, normalize_basin_name


class WeatherGeographicMapper:
    """
    Deterministic spatial router for Indian meteorological data.
    Ensures complete coverage of all 36 administrative entities without hallucinating mappings.
    """

    def __init__(self):
        self._entities_by_name: Dict[str, Dict[str, Any]] = {}
        self._entities_by_code: Dict[str, Dict[str, Any]] = {}
        self._load_entities()

    def _load_entities(self):
        for e in INDIAN_ADMINISTRATIVE_ENTITIES:
            name_key = e["name"].lower().strip()
            self._entities_by_name[name_key] = e
            id_key = e.get("id", "").lower().strip()
            if id_key:
                self._entities_by_name[id_key] = e
            if "(" in e["name"]:
                clean_no_paren = e["name"].split("(")[0].lower().strip()
                self._entities_by_name[clean_no_paren] = e
            code_key = e.get("code", "").lower().strip()
            if code_key:
                self._entities_by_code[code_key] = e

    def map_location(
        self,
        query: str,
        lat: Optional[float] = None,
        lon: Optional[float] = None
    ) -> Tuple[str, str, str, float, float]:
        """
        Resolves query to canonical administrative entity:
        Returns (canonical_name, region_type, region_id, latitude, longitude).
        If unmapped, returns ('Unmapped Location', 'UNMAPPED', 'unmapped', 0.0, 0.0).
        """
        if not query or not isinstance(query, str) or not query.strip():
            return "Unmapped Location", "UNMAPPED", "unmapped", 0.0, 0.0

        q = query.strip().lower()

        # Check direct canonical name or alias via normalize_state_name
        norm_name = normalize_state_name(query)
        norm_key = norm_name.lower().strip()

        if norm_key in self._entities_by_name:
            e = self._entities_by_name[norm_key]
            latitude = lat if lat is not None else e.get("lat", 20.5937)
            longitude = lon if lon is not None else e.get("lon", 78.9629)
            return e["name"], e.get("type", "STATE"), e.get("code", e["name"][:3].upper()), latitude, longitude

        # Check code
        if q in self._entities_by_code:
            e = self._entities_by_code[q]
            latitude = lat if lat is not None else e.get("lat", 20.5937)
            longitude = lon if lon is not None else e.get("lon", 78.9629)
            return e["name"], e.get("type", "STATE"), e.get("code", e["name"][:3].upper()), latitude, longitude

        # Check basin
        basin = normalize_basin_name(query)
        if basin in ["brahmaputra", "ganga", "godavari", "mahanadi", "krishna"]:
            return f"{basin.title()} Basin", "BASIN", f"BASIN_{basin.upper()}", lat or 22.0, lon or 80.0

        # Unverified / Unmapped
        return "Unmapped Location", "UNMAPPED", "unmapped", lat or 0.0, lon or 0.0

    def is_valid_entity(self, name: str) -> bool:
        """Returns True if the name corresponds to one of the 36 canonical entities."""
        norm_name = normalize_state_name(name)
        return norm_name.lower().strip() in self._entities_by_name

    def get_basin_for_entity(self, entity_name: str) -> str:
        """Returns canonical river basin identifier for an administrative entity."""
        norm = normalize_state_name(entity_name).lower().strip()
        e = self._entities_by_name.get(norm)
        if e and "primary_basin" in e:
            return e["primary_basin"]
        return "unknown"


weather_geographic_mapper = WeatherGeographicMapper()
