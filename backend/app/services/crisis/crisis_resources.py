"""
RISK // INDIA — Crisis Emergency Resources Engine (Phase 30E)
============================================================
Retrieves verified emergency services, helplines, NDRF/SDRF battalions,
and medical rescue nodes with strict provenance preservation.

CRITICAL INVARIANT:
Zero synthetic or invented emergency resources.
If a verified nearby resource is absent, the system explicitly returns:
"Verified nearby resource location is currently unavailable."
"""

import math
from typing import List, Optional, Tuple, Dict, Any
from app.services.crisis.crisis_schema import CrisisResourceItem
from app.services.resource_service import VERIFIED_RESOURCES_REGISTRY


class CrisisResourceEngine:
    """Manages verified emergency assistance resources and proximity sorting."""

    @staticmethod
    def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculates great-circle distance in kilometers between two points."""
        r = 6371.0  # Earth radius in kilometers
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2.0) ** 2 + \
            math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return round(r * c, 2)

    @classmethod
    def get_emergency_resources(
        cls,
        state_or_ut: str,
        hazard: str = "ALL",
        coordinates: Optional[Tuple[float, float]] = None,
        max_results: int = 10
    ) -> Tuple[List[CrisisResourceItem], Optional[str]]:
        """
        Retrieves verified emergency resources for the specified state/UT and hazard.
        
        Returns:
            (resources_list, availability_note)
        """
        norm_state = str(state_or_ut).strip().lower()
        norm_hazard = str(hazard).strip().upper()
        
        matched_items: List[CrisisResourceItem] = []
        has_local_resource = False

        for r in VERIFIED_RESOURCES_REGISTRY:
            res_state = str(r.get("state", "")).strip().lower()
            res_hazard = str(r.get("disaster_type", "ALL")).strip().upper()
            
            # Match state or pan-India
            is_state_match = (
                norm_state in res_state or
                res_state in norm_state or
                res_state == "pan-india" or
                norm_state == "india"
            )
            
            if not is_state_match:
                continue

            # Check hazard relevance
            if norm_hazard != "ALL" and res_hazard not in ["ALL", norm_hazard]:
                continue

            if res_state != "pan-india":
                has_local_resource = True

            # Distance calculation if coordinates are present
            dist_km: Optional[float] = None
            lat = r.get("latitude")
            lon = r.get("longitude")
            if coordinates and lat is not None and lon is not None:
                dist_km = cls._haversine_km(coordinates[0], coordinates[1], float(lat), float(lon))

            phone = r.get("phone") or r.get("contact_number")
            item = CrisisResourceItem(
                id=str(r.get("id")),
                name=str(r.get("name")),
                resource_type=str(r.get("resource_type", "GOVERNMENT")),
                category=str(r.get("category", "Emergency Response")),
                phone=phone,
                contact_number=phone,
                website_url=r.get("website_url") or r.get("website"),
                address=r.get("address"),
                state=str(r.get("state")),
                district=r.get("district"),
                disaster_type=str(r.get("disaster_type", "ALL")),
                verification_status="VERIFIED",
                distance_km=dist_km,
                services=r.get("services") or [],
                source=str(r.get("source", "Official Statutory Entity")),
                provenance=f"Statutory authority: {r.get('source', 'Official Govt Registry')} (Verified)"
            )
            matched_items.append(item)

        # Sort: items with distance first (ascending), then local state, then Pan-India
        if coordinates:
            matched_items.sort(
                key=lambda x: (
                    0 if x.distance_km is not None else 1,
                    x.distance_km if x.distance_km is not None else 99999.0
                )
            )
        else:
            matched_items.sort(
                key=lambda x: (
                    0 if x.state.lower() != "pan-india" else 1,
                    x.name
                )
            )

        final_items = matched_items[:max_results]
        
        # Invariant check: if no local resources are present in registry
        availability_note = None
        if not has_local_resource:
            availability_note = (
                "Verified nearby resource location is currently unavailable. "
                "Pan-India statutory emergency response helplines (NDMA 1078, NDRF 011-24363260, Emergency 112) "
                "remain operational 24/7."
            )

        return final_items, availability_note
