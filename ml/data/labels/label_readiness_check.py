"""
RISK // INDIA — Flood Label Readiness Inspection CLI

Inspects datasets/raw/isro/ to determine if authoritative machine-readable
flood inundation layers are locally present for training label creation.

Outputs one of three official statuses:
1. NO_LABEL_DATA: datasets/raw/isro is empty or contains only gitkeeps/placeholders.
2. PARTIAL_LABEL_DATA: only visual raster maps (.jpg/.pdf) or incomplete extracts exist.
3. READY_FOR_LABEL_ALIGNMENT: machine-readable vector polygons (.geojson/.shp/.gpkg) are verified present.
"""

from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[3]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ml.data.labels.isro_flood_loader import (
    ISROFloodInundationLoader,
    MACHINE_READABLE_EXTENSIONS,
    VISUAL_REJECTED_EXTENSIONS
)

BASE_DIR = Path(__file__).resolve().parents[3]
ISRO_RAW_DIR = BASE_DIR / "datasets" / "raw" / "isro"


def check_flood_label_readiness() -> Dict[str, Any]:
    """
    Forensically inspects datasets/raw/isro/ and returns structured readiness status.
    """
    loader = ISROFloodInundationLoader(ISRO_RAW_DIR)
    scan_result = loader.scan_directory()

    machine_readable = scan_result.get("machine_readable_files", [])
    visual_files = scan_result.get("visual_files_requiring_manual_extraction", [])

    if len(machine_readable) > 0:
        status = "READY_FOR_LABEL_ALIGNMENT"
        message = f"Found {len(machine_readable)} machine-readable geospatial layer(s). Ready for spatial labeling join."
    elif len(visual_files) > 0:
        status = "PARTIAL_LABEL_DATA"
        message = (
            f"Found {len(visual_files)} visual map file(s), but NO machine-readable vector layers. "
            "STATUS: MANUAL GIS EXTRACTION REQUIRED. Export GeoJSON/Shapefiles using QGIS before alignment."
        )
    else:
        status = "NO_LABEL_DATA"
        message = (
            "No satellite flood inundation layers found in datasets/raw/isro/. "
            "Official Bhuvan disaster polygons are pending manual download/export. "
            "Ground truth status remains: NOT_READY — FLOOD LABEL DATA REQUIRED."
        )

    return {
        "status": status,
        "isro_raw_dir": str(ISRO_RAW_DIR),
        "machine_readable_count": len(machine_readable),
        "machine_readable_files": machine_readable,
        "visual_files_count": len(visual_files),
        "visual_files": [v["file"] for v in visual_files],
        "message": message
    }


def main():
    print("=" * 80)
    print("RISK // INDIA — FLOOD GROUND TRUTH LABEL READINESS AUDIT")
    print("=" * 80)

    report = check_flood_label_readiness()

    print(f"\nTARGET DIRECTORY: {report['isro_raw_dir']}")
    print(f"MACHINE-READABLE FILES DETECTED: {report['machine_readable_count']}")
    if report['machine_readable_files']:
        for f in report['machine_readable_files']:
            print(f"  [+] {f}")

    print(f"VISUAL MAP FILES DETECTED: {report['visual_files_count']}")
    if report['visual_files']:
        for f in report['visual_files']:
            print(f"  [!] {f} -> MANUAL GIS EXTRACTION REQUIRED")

    print("\n" + "-" * 80)
    print(f"FLOOD LABEL STATUS: {report['status']}")
    print("-" * 80)
    print(f"VERDICT: {report['message']}\n")

    if report["status"] != "READY_FOR_LABEL_ALIGNMENT":
        print("ACTION REQUIRED: Follow instructions in docs/flood_label_manual_acquisition.md")
        print("to acquire machine-readable GeoJSON/Shapefiles from ISRO/NRSC Bhuvan portal.\n")


if __name__ == "__main__":
    main()
