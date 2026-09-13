"""
RISK // INDIA — CWC Telemetry Rainfall Ingestion Loader

Parses sub-daily/hourly automated rain gauge (ARG) telemetry from the
Central Water Commission (CWC) hydro-meteorological network.

Canonical Output Schema:
- timestamp: ISO 8601 string
- station_id: str
- river_basin: str
- rainfall_hourly_mm: float
- latitude: float
- longitude: float
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
import pandas as pd

from ml.data.validation.schema_validation import inspect_dataframe_schema
from ml.data.validation.quality_report import DataQualityReporter

DEFAULT_CWC_RAW_DIR = Path(__file__).resolve().parents[3] / "datasets" / "raw" / "cwc"


class CWCRainfallLoader:
    """
    Ingestion parser for CWC telemetry rainfall datasets.
    """

    def __init__(self, raw_dir: Path = DEFAULT_CWC_RAW_DIR):
        self.raw_dir = raw_dir
        self.reporter = DataQualityReporter()

    def discover_raw_files(self) -> List[Path]:
        if not self.raw_dir.exists():
            return []
        return sorted([
            f for f in self.raw_dir.rglob("*rainfall*.*")
            if f.suffix.lower() in [".csv", ".parquet"]
        ])

    def load_file(self, file_path: Path) -> Dict[str, Any]:
        if not file_path.exists():
            return {"status": "FILE_NOT_FOUND", "data": None, "report": {"error": f"File {file_path} not found."}}

        try:
            df_raw = pd.read_parquet(file_path) if file_path.suffix == ".parquet" else pd.read_csv(file_path)
        except Exception as e:
            return {"status": "LOAD_ERROR", "data": None, "report": {"error": str(e)}}

        schema_audit = inspect_dataframe_schema(df_raw, required_concepts=["rainfall", "date"])
        if not schema_audit["is_schema_valid"]:
            return {"status": "INVALID_SCHEMA", "data": None, "report": schema_audit}

        col_mappings = schema_audit["detected_mappings"]
        rename_dict = {}
        for canonical, orig in col_mappings.items():
            if canonical == "rainfall":
                rename_dict[orig] = "rainfall_hourly_mm"
            elif canonical == "date":
                rename_dict[orig] = "timestamp"
            elif canonical == "station_id":
                rename_dict[orig] = "station_id"
            elif canonical == "latitude":
                rename_dict[orig] = "latitude"
            elif canonical == "longitude":
                rename_dict[orig] = "longitude"

        df_std = df_raw.rename(columns=rename_dict).copy()
        df_std["timestamp"] = pd.to_datetime(df_std["timestamp"], dayfirst=True).dt.strftime("%Y-%m-%d %H:%M:%S")
        df_std["rainfall_hourly_mm"] = pd.to_numeric(df_std["rainfall_hourly_mm"], errors="coerce")

        audit_report = self.reporter.audit_rainfall_dataset(
            df_std, rainfall_col="rainfall_hourly_mm", date_col="timestamp", station_col="station_id" if "station_id" in df_std.columns else None
        )

        return {
            "status": "SUCCESS",
            "file_path": str(file_path),
            "rows_loaded": len(df_std),
            "data": df_std,
            "quality_report": audit_report
        }

    def status(self) -> Dict[str, Any]:
        files = self.discover_raw_files()
        if not files:
            return {
                "status": "AWAITING_SOURCE_DATA",
                "raw_dir": str(self.raw_dir),
                "files_found": 0,
                "message": "No raw CWC telemetry rainfall files found in datasets/raw/cwc/."
            }
        return {
            "status": "RAW_DATA_PRESENT",
            "files_found": len(files),
            "files": [f.name for f in files]
        }
