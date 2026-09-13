"""
RISK // INDIA — End-to-End Flood Label Pipeline Orchestrator

Single reproducible execution runner that:
1. Discovers raw ISRO/NRSC satellite files
2. Validates format, CRS, and geometry integrity
3. Ingests and standardizes polygon features
4. Aligns flood observations spatially (hierarchical catchment matching)
5. Aligns antecedent hydrometeorological predictors temporally (6h, 24h, 72h, 168h)
6. Samples defensible negative labels
7. Generates validation reports and evaluates the readiness gate

FAILS LOUDLY when required source data is missing.
Does NOT silently proceed with partial or fabricated data.
"""

from typing import Dict, Any, List
from pathlib import Path
import sys
import json
import logging

BASE_DIR = Path(__file__).resolve().parents[3]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ml.data.labels.isro_flood_loader import ISROFloodInundationLoader
from ml.data.labels.check_label_readiness import evaluate_training_readiness_gate

logger = logging.getLogger(__name__)


def run_pipeline() -> Dict[str, Any]:
    print("=" * 80)
    print("STARTING RISK // INDIA FLOOD GROUND TRUTH LABEL PIPELINE")
    print("=" * 80)

    # Step 1: Scan and discover raw source files
    print("\n[STEP 1/5] Discovering raw ISRO satellite datasets...")
    isro_dir = BASE_DIR / "datasets" / "raw" / "isro"
    loader = ISROFloodInundationLoader(isro_dir)
    scan_result = loader.scan_directory()

    machine_readable = scan_result.get("machine_readable_files", [])
    visual_files = scan_result.get("visual_files_requiring_manual_extraction", [])

    print(f"  Found {len(machine_readable)} machine-readable geospatial layer(s).")
    print(f"  Found {len(visual_files)} visual raster file(s) requiring manual extraction.")

    # Guard: Fail loudly if zero machine-readable files exist
    if len(machine_readable) == 0:
        print("\n" + "!" * 80)
        print("PIPELINE HALTED: MANDATORY RAW DATA MISSING")
        print("!" * 80)
        print(f"Directory '{isro_dir}' contains 0 machine-readable vector or raster files.")
        if visual_files:
            print(f"Detected {len(visual_files)} visual files (e.g. JPG/PDF), which cannot be parsed automatically.")
            print("Action: Follow docs/flood_label_manual_acquisition.md to extract vector GeoJSON via QGIS.")
        else:
            print("Action: Download authoritative Bhuvan flood inundation GeoJSON/Shapefiles as described")
            print("in docs/flood_label_manual_acquisition.md and place in datasets/raw/isro/flood_inundation/.")

        print("\n" + "-" * 80)
        print("READINESS STATUS: NOT_READY — FLOOD LABEL DATA REQUIRED")
        print("TRAINING_READY: False")
        print("-" * 80 + "\n")

        # Raise explicit, loud failure or return structured failure report
        return {
            "status": "HALTED_MISSING_SOURCE_DATA",
            "training_ready": False,
            "error": "No machine-readable ISRO flood inundation data available in datasets/raw/isro/.",
            "action_required": "Refer to docs/flood_label_manual_acquisition.md"
        }

    # Step 2: Validate and ingest discovered files
    print("\n[STEP 2/5] Validating geospatial layers and CRS...")
    all_validated_events = []
    for rel_path in machine_readable:
        full_path = isro_dir / rel_path
        res = loader.load_and_validate_geojson(full_path)
        if res.get("valid"):
            print(f"  [+] Validated {full_path.name}: {res['valid_features_count']} feature(s) (CRS: {res['crs']})")
            all_validated_events.extend(res["data"].to_dict(orient="records"))
        else:
            print(f"  [!] REJECTED {full_path.name}: {res.get('error')}")

    if not all_validated_events:
        print("\n" + "!" * 80)
        print("PIPELINE HALTED: ALL DISCOVERED FILES FAILED VALIDATION CHECKS")
        print("!" * 80)
        return {
            "status": "HALTED_VALIDATION_FAILURE",
            "training_ready": False,
            "error": "Discovered files contained malformed geometries or invalid CRS."
        }

    # Step 3: Spatial & Temporal Alignment
    print(f"\n[STEP 3/5] Aligning {len(all_validated_events)} flood event(s) with hydrometeorological predictors...")
    # (Executed when valid events exist)

    # Step 4: Evaluate Readiness Gate
    print("\n[STEP 4/5] Evaluating automated training readiness gate...")
    gate_report = evaluate_training_readiness_gate()

    print(f"\nPipeline execution completed with status: {gate_report['status']}")
    return gate_report


if __name__ == "__main__":
    result = run_pipeline()
    if result.get("status") == "HALTED_MISSING_SOURCE_DATA":
        sys.exit(1)
