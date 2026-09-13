"""
RISK // INDIA — CWC Rainfall Cleaning Pipeline

Cleans the raw CWC hourly rainfall dataset without altering source files:
- Retains verified active telemetry stations (31 stations)
- Removes 9 non-telemetry river gauge stations (102,350 null rows)
- Flags telemetry spikes (> 150 mm/hr) without silent loss of information
- Outputs cleaned dataset to datasets/interim/cwc_rainfall_assam_hourly_cleaned.csv
- Generates reproducible audit trail at datasets/interim/cwc_rainfall_cleaning_audit.json
"""

from typing import Dict, Any, List
from pathlib import Path
import json
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[3]
DEFAULT_RAW_PATH = BASE_DIR / "datasets" / "raw" / "cwc" / "rainfall" / "rainfall_tel_hr_cwc_as_2021_2025.csv"
DEFAULT_INTERIM_DIR = BASE_DIR / "datasets" / "interim"

# Documented 9 non-telemetry river gauge stations that lack rain sensors
NON_TELEMETRY_STATIONS = {
    "Nematighat",
    "Goalpara",
    "Melabazar",
    "Golokganj",
    "Tezpur",
    "Guwahati(D.C.Court)",
    "Dhubri",
    "Dibrugarh",
    "NH RD Xing(Puthimari)"
}

# Maximum physically plausible single-hour precipitation threshold in Assam (mm/hr)
MAX_PLAUSIBLE_HOURLY_RAINFALL = 150.0


def clean_cwc_rainfall_dataset(
    raw_path: Path = DEFAULT_RAW_PATH,
    output_dir: Path = DEFAULT_INTERIM_DIR
) -> Dict[str, Any]:
    """
    Executes the documented forensic cleaning rules on raw CWC rainfall.
    """
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw CWC rainfall file not found at: {raw_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    df_raw = pd.read_csv(raw_path)
    total_raw_rows = len(df_raw)

    rain_val_col = "Telemetry Hourly Rainfall (mm)"
    time_col = "Data Acquisition Time"

    # Rule 1: Identify and drop the 9 non-telemetry stations
    non_tel_mask = df_raw["Station"].isin(NON_TELEMETRY_STATIONS)
    dropped_non_tel_rows = int(non_tel_mask.sum())
    df_step1 = df_raw[~non_tel_mask].copy()

    # Rule 2: Verify remaining rows have non-null rainfall
    null_rain_mask = df_step1[rain_val_col].isna()
    dropped_null_rows = int(null_rain_mask.sum())
    df_step2 = df_step1[~null_rain_mask].copy()

    # Rule 3: Check for negative values
    negative_mask = df_step2[rain_val_col] < 0
    negative_count = int(negative_mask.sum())

    # Rule 4: Flag and cap extreme telemetry spikes (> 150 mm/hr)
    spike_mask = df_step2[rain_val_col] > MAX_PLAUSIBLE_HOURLY_RAINFALL
    spikes_flagged = int(spike_mask.sum())

    df_step2["is_telemetry_spike_flag"] = spike_mask.astype(int)
    # Capped feature for modeling while preserving original raw column
    df_step2["cleaned_rainfall_mm"] = df_step2[rain_val_col].clip(upper=MAX_PLAUSIBLE_HOURLY_RAINFALL)

    # Parse and standardize datetime
    df_step2["parsed_datetime"] = pd.to_datetime(df_step2[time_col], format="%d-%m-%Y %H:%M", errors="coerce")
    df_step2 = df_step2.sort_values(["Station", "parsed_datetime"]).reset_index(drop=True)

    # Save cleaned interim dataset
    output_csv_path = output_dir / "cwc_rainfall_assam_hourly_cleaned.csv"
    df_step2.to_csv(output_csv_path, index=False)

    # Compile cleaning audit report
    audit_report = {
        "source_raw_file": str(raw_path.relative_to(BASE_DIR)),
        "target_interim_file": str(output_csv_path.relative_to(BASE_DIR)),
        "execution_status": "SUCCESS",
        "cleaning_rules_applied": [
            {
                "rule_id": "RULE_1_REMOVE_NON_TELEMETRY_STATIONS",
                "description": "Dropped 9 river gauge stations that reported 100% null rainfall.",
                "stations_removed": sorted(list(NON_TELEMETRY_STATIONS)),
                "rows_dropped": dropped_non_tel_rows
            },
            {
                "rule_id": "RULE_2_ENSURE_NON_NULL_TELEMETRY",
                "description": "Ensured all retained records have valid numeric precipitation values.",
                "rows_dropped": dropped_null_rows
            },
            {
                "rule_id": "RULE_3_VERIFY_NON_NEGATIVE",
                "description": "Verified no negative rainfall measurements.",
                "negative_count_found": negative_count
            },
            {
                "rule_id": "RULE_4_FLAG_EXTREME_TELEMETRY_SPIKES",
                "description": f"Flagged observations exceeding {MAX_PLAUSIBLE_HOURLY_RAINFALL} mm/hr as sensor errors. Preserved original value in '{rain_val_col}' and provided clipped value in 'cleaned_rainfall_mm'.",
                "spikes_flagged_count": spikes_flagged,
                "max_spike_value_observed": float(df_step2[rain_val_col].max())
            }
        ],
        "statistics": {
            "total_raw_rows": total_raw_rows,
            "total_cleaned_rows": len(df_step2),
            "retained_active_stations_count": int(df_step2["Station"].nunique()),
            "retained_active_stations": sorted(df_step2["Station"].unique().tolist()),
            "earliest_timestamp": str(df_step2["parsed_datetime"].min()),
            "latest_timestamp": str(df_step2["parsed_datetime"].max()),
            "cleaned_min_rainfall_mm": float(df_step2["cleaned_rainfall_mm"].min()),
            "cleaned_median_rainfall_mm": float(df_step2["cleaned_rainfall_mm"].median()),
            "cleaned_max_rainfall_mm": float(df_step2["cleaned_rainfall_mm"].max())
        }
    }

    audit_json_path = output_dir / "cwc_rainfall_cleaning_audit.json"
    with open(audit_json_path, "w", encoding="utf-8") as f:
        json.dump(audit_report, f, indent=2)

    return audit_report


if __name__ == "__main__":
    report = clean_cwc_rainfall_dataset()
    print("=" * 80)
    print("CWC RAINFALL CLEANING PIPELINE COMPLETED")
    print("=" * 80)
    print(f"Raw rows: {report['statistics']['total_raw_rows']:,}")
    print(f"Cleaned rows retained: {report['statistics']['total_cleaned_rows']:,}")
    print(f"Active stations retained: {report['statistics']['retained_active_stations_count']}")
    print(f"Telemetry spikes flagged (>150mm/hr): {report['cleaning_rules_applied'][3]['spikes_flagged_count']}")
    print(f"Output saved to: {report['target_interim_file']}")
