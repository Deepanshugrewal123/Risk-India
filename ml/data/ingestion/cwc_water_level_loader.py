"""
RISK // INDIA — CWC River Stage & Water Level Telemetry Ingestion Loader

Parses hourly river water levels, danger levels, and warning thresholds from
the Central Water Commission (CWC) hydrometric stations.

Canonical Output Schema:
- timestamp: ISO 8601 (YYYY-MM-DD HH:MM:SS)
- station_id: str
- river_name: str
- water_level_m: float
- danger_level_m: float
- warning_level_m: float
- level_above_danger_m: float (derived: water_level - danger_level)
- latitude: float
- longitude: float
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
import pandas as pd

from ml.data.validation.schema_validation import inspect_dataframe_schema
from ml.data.validation.quality_report import DataQualityReporter

DEFAULT_CWC_RAW_DIR = Path(__file__).resolve().parents[3] / "datasets" / "raw" / "cwc"


class CWCWaterLevelLoader:
    """
    Ingestion parser for CWC river stage water level datasets.
    """

    def __init__(self, raw_dir: Path = DEFAULT_CWC_RAW_DIR):
        self.raw_dir = raw_dir
        self.reporter = DataQualityReporter()

    def discover_raw_files(self) -> List[Path]:
        if not self.raw_dir.exists():
            return []
        files = list(self.raw_dir.rglob("*level*.*")) + list(self.raw_dir.rglob("*rwl*.*"))
        return sorted(list({
            f for f in files
            if f.suffix.lower() in [".csv", ".parquet"]
        }))

    def load_file(self, file_path: Path) -> Dict[str, Any]:
        if not file_path.exists():
            return {"status": "FILE_NOT_FOUND", "data": None, "report": {"error": f"File {file_path} not found."}}

        try:
            df_raw = pd.read_parquet(file_path) if file_path.suffix == ".parquet" else pd.read_csv(file_path)
        except Exception as e:
            return {"status": "LOAD_ERROR", "data": None, "report": {"error": str(e)}}

        schema_audit = inspect_dataframe_schema(df_raw, required_concepts=["water_level", "date"])
        if not schema_audit["is_schema_valid"]:
            return {"status": "INVALID_SCHEMA", "data": None, "report": schema_audit}

        col_mappings = schema_audit["detected_mappings"]
        rename_dict = {}
        for canonical, orig in col_mappings.items():
            if canonical == "water_level":
                rename_dict[orig] = "water_level_m"
            elif canonical == "date":
                rename_dict[orig] = "timestamp"
            elif canonical == "danger_level":
                rename_dict[orig] = "danger_level_m"
            elif canonical == "station_id":
                rename_dict[orig] = "station_id"
            elif canonical == "latitude":
                rename_dict[orig] = "latitude"
            elif canonical == "longitude":
                rename_dict[orig] = "longitude"

        df_std = df_raw.rename(columns=rename_dict).copy()
        df_std["timestamp"] = pd.to_datetime(df_std["timestamp"], dayfirst=True).dt.strftime("%Y-%m-%d %H:%M:%S")
        df_std["water_level_m"] = pd.to_numeric(df_std["water_level_m"], errors="coerce")

        if "danger_level_m" in df_std.columns:
            df_std["danger_level_m"] = pd.to_numeric(df_std["danger_level_m"], errors="coerce")
            df_std["level_above_danger_m"] = df_std["water_level_m"] - df_std["danger_level_m"]
        else:
            df_std["danger_level_m"] = None
            df_std["level_above_danger_m"] = None

        if "station_id" not in df_std.columns:
            df_std["station_id"] = "cwc-station-unknown"

        audit_report = self.reporter.audit_river_level_dataset(
            df_std,
            water_level_col="water_level_m",
            timestamp_col="timestamp",
            station_col="station_id"
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
                "message": "No raw CWC river stage telemetry files found in datasets/raw/cwc/."
            }
        return {
            "status": "RAW_DATA_PRESENT",
            "files_found": len(files),
            "files": [f.name for f in files]
        }
