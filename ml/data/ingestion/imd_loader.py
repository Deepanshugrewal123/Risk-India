"""
RISK // INDIA — IMD Precipitation Ingestion Loader

Parses daily gridded or station/district precipitation records from the
India Meteorological Department (IMD).

Canonical Output Schema:
- date: YYYY-MM-DD
- location_id: str (normalized lowercase state/district code)
- latitude: float (optional/if available)
- longitude: float (optional/if available)
- rainfall_mm: float (daily total mm)
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
import pandas as pd
import numpy as np

from ml.data.validation.schema_validation import inspect_dataframe_schema, resolve_canonical_column
from ml.data.validation.spatial_validation import validate_coordinates
from ml.data.validation.quality_report import DataQualityReporter

DEFAULT_IMD_RAW_DIR = Path(__file__).resolve().parents[3] / "datasets" / "raw" / "imd"


class IMDRainfallLoader:
    """
    Ingestion parser for IMD daily rainfall datasets.
    """

    def __init__(self, raw_dir: Path = DEFAULT_IMD_RAW_DIR):
        self.raw_dir = raw_dir
        self.reporter = DataQualityReporter()

    def discover_raw_files(self) -> List[Path]:
        """Discovers any CSV, TXT, or Parquet files placed in datasets/raw/imd."""
        if not self.raw_dir.exists():
            return []
        return sorted([
            f for f in self.raw_dir.glob("*.*")
            if f.suffix.lower() in [".csv", ".txt", ".parquet"]
        ])

    def load_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Loads and parses a single raw IMD file into a standardized intermediate dataframe.
        """
        if not file_path.exists():
            return {
                "status": "FILE_NOT_FOUND",
                "file_path": str(file_path),
                "data": None,
                "report": {"error": f"File {file_path} does not exist."}
            }

        try:
            if file_path.suffix.lower() == ".parquet":
                df_raw = pd.read_parquet(file_path)
            else:
                df_raw = pd.read_csv(file_path)
        except Exception as e:
            return {
                "status": "LOAD_ERROR",
                "file_path": str(file_path),
                "data": None,
                "report": {"error": f"Failed reading raw file: {e}"}
            }

        schema_audit = inspect_dataframe_schema(df_raw, required_concepts=["rainfall", "date"])
        if not schema_audit["is_schema_valid"]:
            return {
                "status": "INVALID_SCHEMA",
                "file_path": str(file_path),
                "data": None,
                "report": schema_audit
            }

        # Standardize columns to canonical names
        col_mappings = schema_audit["detected_mappings"]
        rename_dict = {}
        for canonical, orig in col_mappings.items():
            if canonical == "rainfall":
                rename_dict[orig] = "rainfall_mm"
            elif canonical == "date":
                rename_dict[orig] = "date"
            elif canonical == "latitude":
                rename_dict[orig] = "latitude"
            elif canonical == "longitude":
                rename_dict[orig] = "longitude"
            elif canonical in ["district", "station_id", "state"]:
                if "location_id" not in rename_dict.values():
                    rename_dict[orig] = "location_id"

        df_std = df_raw.rename(columns=rename_dict).copy()

        # Date normalization
        df_std["date"] = pd.to_datetime(df_std["date"]).dt.strftime("%Y-%m-%d")

        # Location ID normalization
        if "location_id" not in df_std.columns:
            df_std["location_id"] = "imd-station-unknown"
        else:
            df_std["location_id"] = df_std["location_id"].astype(str).str.strip().str.lower()

        # Ensure numeric rainfall
        df_std["rainfall_mm"] = pd.to_numeric(df_std["rainfall_mm"], errors="coerce")

        # Run non-destructive quality audit
        audit_report = self.reporter.audit_rainfall_dataset(df_std, rainfall_col="rainfall_mm", date_col="date")

        return {
            "status": "SUCCESS",
            "file_path": str(file_path),
            "rows_loaded": len(df_std),
            "data": df_std,
            "quality_report": audit_report,
            "schema_audit": schema_audit
        }

    def status(self) -> Dict[str, Any]:
        files = self.discover_raw_files()
        if not files:
            return {
                "status": "AWAITING_SOURCE_DATA",
                "raw_dir": str(self.raw_dir),
                "files_found": 0,
                "message": "No raw IMD precipitation files found in datasets/raw/imd/."
            }
        return {
            "status": "RAW_DATA_PRESENT",
            "raw_dir": str(self.raw_dir),
            "files_found": len(files),
            "files": [f.name for f in files]
        }
