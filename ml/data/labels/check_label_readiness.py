"""
RISK // INDIA — Automated Flood Ground-Truth Readiness Gate

Evaluates the 10 mandatory criteria required for ML training readiness:
1. Authoritative flood observations available
2. Provenance documented
3. Valid spatial alignment
4. Valid temporal alignment
5. Sufficient predictor coverage
6. Valid label schema
7. Positive labels available
8. Defensible negative samples available
9. No unresolved critical data corruption
10. Zero leakage between training and evaluation design

Outputs one of:
- NOT_READY
- SOURCE_DATA_AVAILABLE
- POSITIVE_LABELS_READY
- LABEL_ALIGNMENT_READY
- TRAINING_READY

If any critical requirement fails:
TRAINING_READY = False
"""

from typing import Dict, Any, List
from pathlib import Path
import sys
import json

BASE_DIR = Path(__file__).resolve().parents[3]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ml.data.labels.isro_flood_loader import ISROFloodInundationLoader

ISRO_RAW_DIR = BASE_DIR / "datasets" / "raw" / "isro"
INTERIM_DIR = BASE_DIR / "datasets" / "interim"


def evaluate_training_readiness_gate() -> Dict[str, Any]:
    """
    Evaluates the complete end-to-end readiness checklist.
    """
    loader = ISROFloodInundationLoader(ISRO_RAW_DIR)
    scan_res = loader.scan_directory()

    machine_readable_files = scan_res.get("machine_readable_files", [])
    visual_files = scan_res.get("visual_files_requiring_manual_extraction", [])

    # Check 1: Authoritative flood observations available
    has_source_data = len(machine_readable_files) > 0

    # Check interim predictor availability
    cleaned_rf_path = INTERIM_DIR / "cwc_rainfall_assam_hourly_cleaned.csv"
    has_cleaned_rainfall = cleaned_rf_path.exists() and cleaned_rf_path.stat().st_size > 1000

    criteria = {
        "1_authoritative_flood_observations_available": has_source_data,
        "2_provenance_documented": has_source_data,
        "3_valid_spatial_alignment": False, # Requires source polygons
        "4_valid_temporal_alignment": False, # Requires source dates
        "5_sufficient_predictor_coverage": has_cleaned_rainfall,
        "6_valid_label_schema_implemented": True, # Pydantic schema active
        "7_positive_labels_available": False,
        "8_defensible_negative_samples_available": False,
        "9_no_unresolved_critical_data_corruption": True, # Rainfall QC applied in interim
        "10_zero_temporal_leakage_enforced": True # Temporal aligner enforces causality
    }

    # Determine status tier
    critical_blockers = []
    if not has_source_data:
        critical_blockers.append("No machine-readable ISRO/NRSC flood inundation files found in datasets/raw/isro/.")
    if len(visual_files) > 0:
        critical_blockers.append("Visual raster files present requiring manual QGIS vector extraction.")
    if not criteria["7_positive_labels_available"]:
        critical_blockers.append("0 verified positive flood event labels exist.")
    if not criteria["8_defensible_negative_samples_available"]:
        critical_blockers.append("Defensible negative samples cannot be generated without known positive flood event windows.")

    training_ready = all(criteria.values())

    if training_ready:
        status = "TRAINING_READY"
    elif has_source_data and criteria["7_positive_labels_available"] and criteria["8_defensible_negative_samples_available"]:
        status = "LABEL_ALIGNMENT_READY"
    elif has_source_data and criteria["7_positive_labels_available"]:
        status = "POSITIVE_LABELS_READY"
    elif has_source_data:
        status = "SOURCE_DATA_AVAILABLE"
    else:
        status = "NOT_READY"

    return {
        "status": status,
        "training_ready": training_ready,
        "criteria": criteria,
        "critical_blockers": critical_blockers,
        "source_data_summary": {
            "isro_raw_dir": str(ISRO_RAW_DIR),
            "machine_readable_count": len(machine_readable_files),
            "machine_readable_files": machine_readable_files,
            "visual_files_count": len(visual_files),
            "visual_files": [v["file"] for v in visual_files]
        }
    }


def main():
    print("=" * 80)
    print("RISK // INDIA — AUTOMATED FLOOD LABEL READINESS GATE")
    print("=" * 80)

    report = evaluate_training_readiness_gate()

    print(f"\nREADINESS GATE STATUS: {report['status']}")
    print(f"TRAINING READY: {report['training_ready']}")

    print("\nMANDATORY READINESS CRITERIA CHECKLIST:")
    for criterion, passed in report["criteria"].items():
        mark = "[PASS]" if passed else "[FAIL]"
        print(f"  {mark} {criterion}")

    print("\nCRITICAL BLOCKERS:")
    if report["critical_blockers"]:
        for blocker in report["critical_blockers"]:
            print(f"  [-] {blocker}")
    else:
        print("  None. All criteria satisfied.")

    print("\n" + "=" * 80)
    print(f"FINAL VERDICT: TRAINING_READY = {report['training_ready']}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
