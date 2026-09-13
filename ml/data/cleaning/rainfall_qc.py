"""
RISK // INDIA — Granular Rainfall Quality Control (QC) Flagging Engine

Implements principled, non-destructive quality control based on forensic audit findings:
- Categorizes every observation into explicit, auditable QC flags:
  1. VALID: 0.0 <= value <= extreme_threshold_mm_hr
  2. SUSPICIOUS_EXTREME: value > extreme_threshold_mm_hr (e.g. 150.0 mm/hr)
  3. INVALID: negative values or unparseable formats
  4. MISSING: null readings from active stations
  5. STATION_INACTIVE: readings from the 9 non-telemetry river gauge stations

Thresholds are configurable parameters rather than hardcoded physical dogmas.
Preserves raw data immutability while producing a transparent QC audit trail.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import pandas as pd
import numpy as np

# Configurable default physical threshold for single-hour precipitation in Assam
DEFAULT_EXTREME_THRESHOLD_MM_HR = 150.0

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


class RainfallQCProcessor:
    """
    Applies configurable quality control rules and tags each hourly observation with a QC flag.
    """

    def __init__(
        self,
        extreme_threshold_mm_hr: float = DEFAULT_EXTREME_THRESHOLD_MM_HR,
        inactive_stations: Optional[set] = None
    ):
        self.extreme_threshold = float(extreme_threshold_mm_hr)
        self.inactive_stations = inactive_stations or NON_TELEMETRY_STATIONS

    def process_dataframe(
        self,
        df: pd.DataFrame,
        station_col: str = "Station",
        rainfall_col: str = "Telemetry Hourly Rainfall (mm)"
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Processes dataframe and appends qc_flag and qc_notes columns without deleting rows.
        """
        df_qc = df.copy()

        def _assign_qc_flag(row) -> Tuple[str, str]:
            st = str(row.get(station_col, ""))
            val = row.get(rainfall_col)

            # Check station activity
            if st in self.inactive_stations:
                return "STATION_INACTIVE", "Station is a river gauge station without rain sensors."

            # Check missingness
            if pd.isna(val):
                return "MISSING", "Null observation recorded for active station."

            try:
                num_val = float(val)
            except (ValueError, TypeError):
                return "INVALID", f"Unparseable numeric value: {val}"

            if num_val < 0.0:
                return "INVALID", f"Physically impossible negative rainfall: {num_val}"

            if num_val > self.extreme_threshold:
                return "SUSPICIOUS_EXTREME", (
                    f"Observation {num_val} mm/hr exceeds configurable threshold "
                    f"({self.extreme_threshold} mm/hr). Likely telemetry bit corruption or cumulative logging."
                )

            return "VALID", "Observation within normal plausible operating bounds."

        qc_results = [_assign_qc_flag(row) for _, row in df_qc.iterrows()]
        df_qc["qc_flag"] = [r[0] for r in qc_results]
        df_qc["qc_notes"] = [r[1] for r in qc_results]

        # Flag summary
        counts = df_qc["qc_flag"].value_counts().to_dict()
        summary = {
            "total_rows_processed": len(df_qc),
            "extreme_threshold_applied_mm_hr": self.extreme_threshold,
            "qc_flag_distribution": counts,
            "valid_percentage": round((counts.get("VALID", 0) / len(df_qc)) * 100.0, 2),
            "suspicious_extreme_count": counts.get("SUSPICIOUS_EXTREME", 0),
            "inactive_station_rows": counts.get("STATION_INACTIVE", 0),
            "missing_count": counts.get("MISSING", 0),
            "invalid_count": counts.get("INVALID", 0)
        }

        return df_qc, summary
