"""
RISK // INDIA — ISRO / NRSC Bhuvan Flood GeoTIFF Raster Validator

Forensic validation module for OGC WCS raster coverages downloaded from Bhuvan.
Performs header parsing, georeferencing inspection, coordinate reference verification,
pixel distribution accounting, and spatial overlap validation against CWC telemetry gauges.
"""

from typing import Dict, Any, Optional, Tuple, Union
from pathlib import Path
import os
import json
import logging
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

# Official Bhuvan GeoServer SLD ColorMap Mapping for recentfloods:
# Quantity <= 0.1: #000000 (0.0 opacity, Background / No Inundation)
# Quantity 0.1 to 1.1: #00FFFF (1.0 opacity, Cyan Inundation / Active Flood Water)
SLD_VALUE_MAP = {
    0: "BACKGROUND_OR_NO_INUNDATION",
    1: "ACTIVE_FLOOD_INUNDATION"
}

# Regional bounding box for Assam State
ASSAM_EXTENT = {
    "min_lon": 89.5,
    "max_lon": 96.5,
    "min_lat": 24.0,
    "max_lat": 28.5
}


def inspect_isro_geotiff(
    file_path: Union[str, Path],
    gauge_coords: Optional[Tuple[float, float]] = None,
    gauge_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Forensically inspects an ISRO Bhuvan GeoTIFF flood raster.

    Args:
        file_path: Path to the .tif file.
        gauge_coords: Optional tuple (latitude, longitude) of the associated CWC gauge.
        gauge_name: Optional name of the CWC gauge.

    Returns:
        Structured dictionary containing all raster properties, spatial checks, and final verdict.
    """
    p = Path(file_path)
    if not p.exists():
        return {
            "status": "ERROR",
            "file": str(p),
            "file_exists": False,
            "error": f"File '{p}' does not exist.",
            "final_verdict": "DOWNLOAD_FAILED"
        }

    file_size = p.stat().st_size
    if file_size == 0:
        return {
            "status": "ERROR",
            "file": str(p),
            "file_exists": True,
            "file_size_bytes": 0,
            "error": "File exists but has 0 bytes.",
            "final_verdict": "DOWNLOAD_FAILED"
        }

    try:
        img = Image.open(p)
    except Exception as e:
        return {
            "status": "ERROR",
            "file": str(p),
            "file_exists": True,
            "file_size_bytes": file_size,
            "error": f"Failed to open TIFF: {str(e)}",
            "final_verdict": "INVALID_RASTER"
        }

    # Basic Raster Dimensions
    width, height = img.size
    mode = img.mode
    format_name = img.format

    tags = getattr(img, "tag_v2", {})
    band_count = tags.get(277, 1)  # Tag 277: SamplesPerPixel
    nodata_tag = tags.get(42113)   # Tag 42113: GDAL_NODATA
    nodata_value = float(nodata_tag) if nodata_tag is not None else 0.0

    # CRS Inspection (Tag 34735: GeoKeyDirectoryTag)
    geokey_dir = tags.get(34735)
    crs = "UNKNOWN"
    is_epsg_4326 = False
    if geokey_dir:
        # Check for Key 2048 (GeographicTypeGeoKey) == 4326
        # GeoKeyDirectory structure: [wKeyDirectoryVersion, wKeyRevision, wMinorRevision, wNumberOfKeys, ...]
        # Followed by 4-tuples: [wKeyID, wTIFFTagLocation, wCount, wValue_Offset]
        for i in range(4, len(geokey_dir), 4):
            if i + 3 < len(geokey_dir):
                key_id = geokey_dir[i]
                val = geokey_dir[i + 3]
                if key_id == 2048 and val == 4326:
                    crs = "EPSG:4326"
                    is_epsg_4326 = True
                    break
        if not is_epsg_4326 and any(x == 4326 for x in geokey_dir):
            crs = "EPSG:4326"
            is_epsg_4326 = True

    # Geotransform & Bounds Inspection
    # Tag 34264: ModelTransformationTag (4x4 matrix)
    # Tag 33922: ModelTiepointTag + Tag 33550: ModelPixelScaleTag
    bounds = None
    geotransform = None
    if 34264 in tags:
        m = tags[34264]
        dx, dy = m[0], m[5]
        ox, oy = m[3], m[7]
        geotransform = {
            "origin_x": ox,
            "pixel_scale_x": dx,
            "origin_y": oy,
            "pixel_scale_y": dy
        }
        min_x = ox
        max_x = ox + dx * width
        max_y = oy
        min_y = oy + dy * height  # dy is typically negative
        bounds = {
            "min_lon": round(min(min_x, max_x), 6),
            "min_lat": round(min(min_y, max_y), 6),
            "max_lon": round(max(min_x, max_x), 6),
            "max_lat": round(max(min_y, max_y), 6)
        }
    elif 33922 in tags and 33550 in tags:
        tie = tags[33922]
        scale = tags[33550]
        ox, oy = tie[3], tie[4]
        dx, dy = scale[0], -scale[1]
        geotransform = {
            "origin_x": ox,
            "pixel_scale_x": dx,
            "origin_y": oy,
            "pixel_scale_y": dy
        }
        min_x = ox
        max_x = ox + dx * width
        max_y = oy
        min_y = oy + dy * height
        bounds = {
            "min_lon": round(min(min_x, max_x), 6),
            "min_lat": round(min(min_y, max_y), 6),
            "max_lon": round(max(min_x, max_x), 6),
            "max_lat": round(max(min_y, max_y), 6)
        }

    # ColorMap / Palette Inspection
    # Tag 320: ColorMap
    colormap_tag = tags.get(320)
    has_colormap = colormap_tag is not None

    # Pixel Array Statistics
    arr = np.array(img)
    total_pixels = int(arr.size)
    unique_vals, counts = np.unique(arr, return_counts=True)
    hist = {int(k): int(v) for k, v in zip(unique_vals, counts)}
    min_val = int(unique_vals.min()) if len(unique_vals) > 0 else None
    max_val = int(unique_vals.max()) if len(unique_vals) > 0 else None

    flood_pixels = hist.get(1, 0)
    background_pixels = hist.get(0, 0)
    other_pixels = total_pixels - flood_pixels - background_pixels

    # Spatial Validation: In Assam
    in_assam = False
    if bounds:
        in_assam = (
            bounds["min_lon"] >= ASSAM_EXTENT["min_lon"] - 0.5 and
            bounds["max_lon"] <= ASSAM_EXTENT["max_lon"] + 0.5 and
            bounds["min_lat"] >= ASSAM_EXTENT["min_lat"] - 0.5 and
            bounds["max_lat"] <= ASSAM_EXTENT["max_lat"] + 0.5
        )

    # Gauge Spatial Overlap Check
    gauge_overlap = None
    gauge_inside = False
    gauge_dist_flood_m = None
    if gauge_coords and bounds and geotransform:
        g_lat, g_lon = gauge_coords
        gauge_inside = (
            bounds["min_lon"] <= g_lon <= bounds["max_lon"] and
            bounds["min_lat"] <= g_lat <= bounds["max_lat"]
        )
        gauge_overlap = {
            "gauge_name": gauge_name or "Unknown Gauge",
            "gauge_latitude": g_lat,
            "gauge_longitude": g_lon,
            "is_inside_raster_bounds": gauge_inside
        }
        if gauge_inside and flood_pixels > 0:
            dx = abs(geotransform["pixel_scale_x"])
            dy = abs(geotransform["pixel_scale_y"])
            gx = int((g_lon - bounds["min_lon"]) / dx)
            gy = int((bounds["max_lat"] - g_lat) / dy)
            gx = max(0, min(gx, width - 1))
            gy = max(0, min(gy, height - 1))
            y_pts, x_pts = np.where(arr == 1)
            if len(x_pts) > 0:
                dists_px = np.sqrt((x_pts - gx)**2 + (y_pts - gy)**2)
                min_dist_px = dists_px.min()
                # Approximate 1 degree ~ 111 km
                gauge_dist_flood_m = round(float(min_dist_px * dx * 111000), 1)
                gauge_overlap["nearest_flood_pixel_meters"] = gauge_dist_flood_m
                gauge_overlap["value_at_gauge_pixel"] = int(arr[gy, gx])

    # Final Verdict Determination
    if not is_epsg_4326 or not bounds:
        final_verdict = "INVALID_RASTER"
    elif not in_assam:
        final_verdict = "INVALID_RASTER"
    elif total_pixels == 0:
        final_verdict = "EMPTY_RASTER"
    elif flood_pixels > 0:
        final_verdict = "VALID_REAL_FLOOD_RASTER"
    elif background_pixels == total_pixels:
        final_verdict = "EMPTY_RASTER"
    else:
        final_verdict = "METADATA_AMBIGUOUS"

    return {
        "status": "SUCCESS",
        "file": str(p),
        "file_name": p.name,
        "file_size_bytes": file_size,
        "format": format_name,
        "mode": mode,
        "width": width,
        "height": height,
        "total_pixels": total_pixels,
        "band_count": band_count,
        "crs": crs,
        "geotransform": geotransform,
        "bounds": bounds,
        "nodata_value": nodata_value,
        "min_value": min_val,
        "max_value": max_val,
        "pixel_distribution": hist,
        "flood_pixel_count": flood_pixels,
        "flood_pixel_percentage": round((flood_pixels / total_pixels) * 100, 4) if total_pixels > 0 else 0.0,
        "background_pixel_count": background_pixels,
        "other_pixel_count": other_pixels,
        "in_assam_boundary": in_assam,
        "gauge_spatial_overlap": gauge_overlap,
        "has_official_colormap": has_colormap,
        "flood_value_interpretation": (
            "Verified from official ISRO GeoServer SLD UserStyle (recentfloods): "
            "Value 0 = Background / No Flood; Value 1 = Cyan (#00FFFF) Inundated Flood Water."
        ),
        "final_verdict": final_verdict
    }


if __name__ == "__main__":
    import sys
    files_to_check = [
        (
            "datasets/raw/isro/flood_inundation/assam_2021_07_06_06hr_nematighat.tif",
            (26.860300, 94.252200),
            "Nematighat (CWC Station, Jorhat)"
        ),
        (
            "datasets/raw/isro/flood_inundation/assam_2021_07_06_06hr_fakirpara.tif",
            (26.508333, 92.116389),
            "NH15 Crossing Fakirpara Tangni (CWC Gauge, Darrang)"
        )
    ]
    if len(sys.argv) > 1:
        files_to_check = [(sys.argv[1], None, None)]

    for fpath, coords, name in files_to_check:
        print(f"\n{'='*70}\nINSPECTING: {fpath}\n{'='*70}")
        res = inspect_isro_geotiff(fpath, coords, name)
        print(json.dumps(res, indent=2))
