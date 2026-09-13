"""
RISK // INDIA — ISRO / NRSC / Bhuvan Flood Inundation Ingestion Loader

Parses satellite flood inundation observation bulletins, hazard zones,
and event extents from ISRO/NRSC Bhuvan Disaster Services.

Canonical Output Schema:
- event_id: str
- observation_date: YYYY-MM-DD
- state_name: str
- district_name: str
- inundated_area_sqkm: float
- hazard_severity: str (Low, Moderate, High, Very High)
- sensor: str (e.g. Sentinel-1A SAR, RISAT-1A)
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
import json
import pandas as pd

DEFAULT_ISRO_RAW_DIR = Path(__file__).resolve().parents[3] / "datasets" / "raw" / "isro"


class ISROFloodInundationLoader:
    """
    Ingestion parser for ISRO/NRSC Bhuvan flood inundation datasets.
    """

    def __init__(self, raw_dir: Path = DEFAULT_ISRO_RAW_DIR):
        self.raw_dir = raw_dir

    def discover_raw_files(self) -> List[Path]:
        if not self.raw_dir.exists():
            return []
        return sorted([
            f for f in self.raw_dir.glob("*.*")
            if f.suffix.lower() in [".csv", ".json", ".geojson"]
        ])

    def load_file(self, file_path: Path) -> Dict[str, Any]:
        if not file_path.exists():
            return {"status": "FILE_NOT_FOUND", "data": None, "report": {"error": f"File {file_path} not found."}}

        try:
            if file_path.suffix.lower() in [".json", ".geojson"]:
                with open(file_path, "r", encoding="utf-8") as f:
                    geo_json = json.load(f)
                features = geo_json.get("features", [])
                records = [feat.get("properties", {}) for feat in features]
                df_raw = pd.DataFrame(records)
            else:
                df_raw = pd.read_csv(file_path)
        except Exception as e:
            return {"status": "LOAD_ERROR", "data": None, "report": {"error": str(e)}}

        if df_raw.empty:
            return {"status": "EMPTY_DATASET", "data": None, "report": {"error": "Dataset contains 0 rows."}}

        # Normalize column names
        df_std = df_raw.copy()
        clean_cols = {c: str(c).strip().lower().replace(" ", "_") for c in df_std.columns}
        df_std = df_std.rename(columns=clean_cols)

        return {
            "status": "SUCCESS",
            "file_path": str(file_path),
            "rows_loaded": len(df_std),
            "data": df_std,
            "columns": list(df_std.columns)
        }

    def status(self) -> Dict[str, Any]:
        files = self.discover_raw_files()
        if not files:
            return {
                "status": "AWAITING_SOURCE_DATA",
                "raw_dir": str(self.raw_dir),
                "files_found": 0,
                "message": "No raw ISRO/NRSC flood inundation layers found in datasets/raw/isro/."
            }
        return {
            "status": "RAW_DATA_PRESENT",
            "files_found": len(files),
            "files": [f.name for f in files]
        }
