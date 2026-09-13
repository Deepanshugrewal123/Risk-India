"""
RISK // INDIA — ISRO / NRSC / Bhuvan Flood Inundation Ingestion & Validation Loader

Responsibilities:
- Discover supported machine-readable files (.geojson, .json, .shp, .gpkg, .tif, .tiff)
- Validate file format integrity and JSON syntax
- Validate Coordinate Reference System (CRS) & geographical extent
- Validate polygon geometry structure (closed rings, coordinate plausibility)
- Extract acquisition and event dates
- Normalize metadata and provenance records
- Reject malformed files and visual image formats (.jpg, .pdf, screenshots)
- Produce standardized internal representation without altering raw files
"""

from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import json
import logging
import pandas as pd

logger = logging.getLogger(__name__)

MACHINE_READABLE_EXTENSIONS = {".geojson", ".json", ".shp", ".gpkg", ".tif", ".tiff"}
VISUAL_REJECTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".pdf", ".gif", ".webp"}

# Regional geographical bounding box for Assam and immediate river basin catchments
ASSAM_BBOX = {
    "min_lon": 89.5,
    "max_lon": 96.5,
    "min_lat": 24.0,
    "max_lat": 28.5
}

DEFAULT_ISRO_DIR = Path(__file__).resolve().parents[3] / "datasets" / "raw" / "isro"


class ISROFloodInundationLoader:
    """
    Ingestion and forensic validation parser for ISRO/NRSC Bhuvan flood datasets.
    """

    def __init__(self, raw_isro_dir: Path = DEFAULT_ISRO_DIR):
        self.raw_dir = Path(raw_isro_dir)

    def discover_files(self) -> Dict[str, List[Path]]:
        """
        Discovers and categorizes all files in datasets/raw/isro/ subdirectories.
        """
        if not self.raw_dir.exists():
            return {"machine_readable": [], "visual_rejected": [], "unrecognized": []}

        all_files = [f for f in self.raw_dir.rglob("*") if f.is_file() and not f.name.startswith(".")]

        categorized: Dict[str, List[Path]] = {
            "machine_readable": [],
            "metadata": [],
            "visual_rejected": [],
            "unrecognized": []
        }

        for f in all_files:
            ext = f.suffix.lower()
            if "metadata" in f.parts:
                categorized["metadata"].append(f)
            elif ext in MACHINE_READABLE_EXTENSIONS:
                categorized["machine_readable"].append(f)
            elif ext in VISUAL_REJECTED_EXTENSIONS:
                categorized["visual_rejected"].append(f)
            else:
                categorized["unrecognized"].append(f)

        return categorized

    def scan_directory(self) -> Dict[str, Any]:
        """
        Scans datasets/raw/isro/ and produces a structured discovery summary.
        """
        discovered = self.discover_files()
        return {
            "status": "SCANNED",
            "directory": str(self.raw_dir),
            "total_files": sum(len(v) for v in discovered.values()),
            "machine_readable_files": [str(p.relative_to(self.raw_dir)) for p in discovered["machine_readable"]],
            "metadata_files": [str(p.relative_to(self.raw_dir)) for p in discovered["metadata"]],
            "visual_files_requiring_manual_extraction": [
                {
                    "file": str(p.relative_to(self.raw_dir)),
                    "status": "MANUAL GIS EXTRACTION REQUIRED",
                    "reason": f"Visual raster format '{p.suffix}' cannot be parsed as structured vector labels."
                }
                for p in discovered["visual_rejected"]
            ],
            "unrecognized_files": [str(p.relative_to(self.raw_dir)) for p in discovered["unrecognized"]]
        }

    def validate_crs_and_coordinates(
        self,
        coords: List[Any],
        geometry_type: str,
        declared_crs: Optional[str] = None
    ) -> Tuple[bool, str, Optional[Dict[str, float]]]:
        """
        Validates CRS and geographic coordinates:
        - Ensures coordinates fall within valid global latitude/longitude bounds
        - Detects whether coordinates fall within the Assam regional bounding box
        - Rejects unprojected Cartesian meter coordinates labeled as WGS 84
        """
        lons: List[float] = []
        lats: List[float] = []

        def _extract_points(c_list: Any):
            if isinstance(c_list, (list, tuple)) and len(c_list) >= 2 and isinstance(c_list[0], (int, float)):
                lons.append(float(c_list[0]))
                lats.append(float(c_list[1]))
            elif isinstance(c_list, (list, tuple)):
                for item in c_list:
                    _extract_points(item)

        _extract_points(coords)

        if not lons or not lats:
            return False, "EMPTY_COORDINATE_ARRAY", None

        min_lon, max_lon = min(lons), max(lons)
        min_lat, max_lat = min(lats), max(lats)

        # Check standard global geographic bounds
        if not (-180.0 <= min_lon <= 180.0 and -180.0 <= max_lon <= 180.0 and
                -90.0 <= min_lat <= 90.0 and -90.0 <= max_lat <= 90.0):
            return False, f"PROJECTED_OR_OUT_OF_BOUNDS_COORDINATES: Lon range [{min_lon}, {max_lon}], Lat range [{min_lat}, {max_lat}]", None

        # Regional check: Does the bounding box intersect Assam's region?
        is_in_assam_region = not (
            max_lon < ASSAM_BBOX["min_lon"] or
            min_lon > ASSAM_BBOX["max_lon"] or
            max_lat < ASSAM_BBOX["min_lat"] or
            min_lat > ASSAM_BBOX["max_lat"]
        )

        bbox_info = {
            "min_lon": round(min_lon, 4),
            "max_lon": round(max_lon, 4),
            "min_lat": round(min_lat, 4),
            "max_lat": round(max_lat, 4),
            "intersects_assam_region": is_in_assam_region
        }

        if declared_crs and declared_crs.upper() not in ["EPSG:4326", "WGS84", "CRS84", "OGC:CRS84"]:
            return False, f"NON_WGS84_CRS_DECLARED: {declared_crs}. Must be EPSG:4326.", bbox_info

        return True, "VALID_CRS_EPSG4326", bbox_info

    def validate_polygon_geometry(self, coords: List[Any], geometry_type: str) -> Tuple[bool, str]:
        """
        Verifies topological integrity of polygon coordinate rings:
        - Ring must have at least 4 points (start point repeated at end)
        - First and last coordinate pair must match (closed ring)
        """
        if geometry_type == "Polygon":
            rings = coords
        elif geometry_type == "MultiPolygon":
            rings = [r for poly in coords for r in poly]
        else:
            return True, "NON_POLYGON_GEOMETRY"

        for ring_idx, ring in enumerate(rings):
            if not isinstance(ring, list) or len(ring) < 4:
                return False, f"INVALID_RING_LENGTH: Ring {ring_idx} has {len(ring) if isinstance(ring, list) else 0} points (minimum 4 required)."
            p_start = ring[0]
            p_end = ring[-1]
            if len(p_start) < 2 or len(p_end) < 2:
                return False, f"MALFORMED_POINT: Ring {ring_idx} contains invalid point length."
            if p_start[0] != p_end[0] or p_start[1] != p_end[1]:
                return False, f"UNCLOSED_POLYGON_RING: Ring {ring_idx} start {p_start} does not match end {p_end}."

        return True, "VALID_POLYGON_GEOMETRY"

    def load_and_validate_geojson(self, file_path: Path) -> Dict[str, Any]:
        """
        Parses and strictly validates a GeoJSON flood observation layer.
        """
        if not file_path.exists():
            return {
                "status": "FILE_NOT_FOUND",
                "file": str(file_path),
                "error": f"Path '{file_path}' does not exist.",
                "valid": False
            }

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            return {
                "status": "MALFORMED_JSON",
                "file": str(file_path),
                "error": f"JSON syntax error: {str(e)}",
                "valid": False
            }

        if not isinstance(data, dict):
            return {
                "status": "INVALID_GEOJSON_STRUCTURE",
                "file": str(file_path),
                "error": "Root JSON element is not an object.",
                "valid": False
            }

        features = data.get("features")
        if features is None or not isinstance(features, list):
            return {
                "status": "MISSING_FEATURES_ARRAY",
                "file": str(file_path),
                "error": "GeoJSON document missing 'features' list.",
                "valid": False
            }

        if len(features) == 0:
            return {
                "status": "EMPTY_FEATURE_COLLECTION",
                "file": str(file_path),
                "error": "GeoJSON document contains 0 features.",
                "valid": False
            }

        # Declared CRS
        declared_crs = None
        crs_obj = data.get("crs")
        if isinstance(crs_obj, dict):
            props = crs_obj.get("properties", {})
            declared_crs = props.get("name")

        validated_records: List[Dict[str, Any]] = []
        validation_errors: List[str] = []

        all_lons: List[float] = []
        all_lats: List[float] = []

        for i, feat in enumerate(features):
            props = feat.get("properties", {}) or {}
            geom = feat.get("geometry", {}) or {}

            gtype = geom.get("type")
            coords = geom.get("coordinates")

            if not gtype or coords is None:
                validation_errors.append(f"Feature {i}: Missing geometry or coordinates.")
                continue

            # Validate CRS and point ranges
            crs_ok, crs_msg, bbox_info = self.validate_crs_and_coordinates(coords, gtype, declared_crs)
            if not crs_ok:
                validation_errors.append(f"Feature {i}: CRS error: {crs_msg}")
                continue

            # Validate polygon ring closure
            geom_ok, geom_msg = self.validate_polygon_geometry(coords, gtype)
            if not geom_ok:
                validation_errors.append(f"Feature {i}: Geometry error: {geom_msg}")
                continue

            # Extract provenance attributes
            event_id = props.get("event_id") or props.get("id") or f"FE_{file_path.stem}_{i:04d}"
            event_date = props.get("observation_date") or props.get("event_date") or props.get("date")
            district = props.get("district_name") or props.get("district") or props.get("DISTRICT")
            area_sqkm = props.get("inundated_area_sqkm") or props.get("area_sqkm")

            if not event_date:
                validation_errors.append(f"Feature {i}: Missing required event observation date.")
                continue

            validated_records.append({
                "source_organization": "ISRO / NRSC Bhuvan Disaster Management Support",
                "product_name": props.get("product_name", "Bhuvan Historical Flood Inundation Layer"),
                "original_filename": file_path.name,
                "source_reference": str(file_path),
                "event_id": str(event_id),
                "event_date": str(event_date),
                "district_name": str(district).strip().upper() if district else None,
                "inundated_area_sqkm": float(area_sqkm) if area_sqkm is not None else None,
                "geometry_type": gtype,
                "coordinates": coords,
                "crs": declared_crs or "EPSG:4326 (WGS84 assumed)",
                "bbox": bbox_info,
                "processing_status": "VALIDATED"
            })

        if not validated_records:
            return {
                "status": "VALIDATION_FAILED",
                "file": str(file_path),
                "error": f"All features failed validation: {'; '.join(validation_errors[:5])}",
                "validation_errors": validation_errors,
                "valid": False
            }

        df_validated = pd.DataFrame(validated_records)
        return {
            "status": "SUCCESS",
            "file": str(file_path),
            "valid": True,
            "total_features": len(features),
            "valid_features_count": len(validated_records),
            "rejected_features_count": len(validation_errors),
            "validation_errors": validation_errors,
            "data": df_validated,
            "crs": declared_crs or "EPSG:4326",
            "date_range": [str(df_validated["event_date"].min()), str(df_validated["event_date"].max())]
        }

    def inspect_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Inspects an arbitrary file, enforcing strict rejection of non-machine-readable formats.
        """
        ext = file_path.suffix.lower()
        if ext in VISUAL_REJECTED_EXTENSIONS:
            return {
                "status": "MANUAL GIS EXTRACTION REQUIRED",
                "file": file_path.name,
                "extension": ext,
                "valid": False,
                "message": (
                    f"Visual format '{ext}' is not machine-readable. "
                    "Cannot be automatically parsed into structured training ground truth. "
                    "Manual georeferencing and polygon vectorization via QGIS required."
                )
            }

        if ext in [".geojson", ".json"]:
            return self.load_and_validate_geojson(file_path)

        if ext in [".shp", ".gpkg"]:
            try:
                import geopandas as gpd
                gdf = gpd.read_file(file_path)
                return {
                    "status": "SUCCESS",
                    "file": file_path.name,
                    "valid": True,
                    "features_count": len(gdf),
                    "crs": str(gdf.crs),
                    "columns": list(gdf.columns)
                }
            except ImportError:
                return {
                    "status": "GEOPANDAS_REQUIRED_FOR_SHP_GPKG",
                    "file": file_path.name,
                    "valid": False,
                    "message": "geopandas is not installed. Convert .shp/.gpkg to .geojson using GDAL/ogr2ogr."
                }

        if ext in [".tif", ".tiff"]:
            from ml.data.labels.isro_raster_validator import inspect_isro_geotiff
            res = inspect_isro_geotiff(file_path)
            return {
                "status": "SUCCESS" if res.get("status") == "SUCCESS" else "FAILED",
                "file": file_path.name,
                "valid": res.get("final_verdict") in ["VALID_REAL_FLOOD_RASTER", "EMPTY_RASTER"],
                "raster_inspection": res
            }

        return {
            "status": "UNSUPPORTED_FORMAT",
            "file": file_path.name,
            "valid": False,
            "message": f"Unsupported format '{ext}'. Accepted: {sorted(list(MACHINE_READABLE_EXTENSIONS))}"
        }
