"""
RISK // INDIA — Statistical Data Profiler & Inspector

Generates rigorous statistical and structural inspection profiles for any tabular dataset:
- Row and column cardinality
- Column datatypes and memory footprint
- Missing value counts and percentages
- Duplicate row counts
- Temporal boundaries and date coverage
- Station and geographical footprint
- Complete numerical percentiles (25th, 50th, 75th, 90th, 95th, 99th, min, max, mean, std)
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np


class DatasetInspector:
    """
    Automated statistical profiler for disaster telemetry datasets.
    """

    def inspect(
        self,
        df: pd.DataFrame,
        dataset_name: str = "Dataset",
        date_col: Optional[str] = "date",
        station_col: Optional[str] = "station_id"
    ) -> Dict[str, Any]:
        """
        Executes a comprehensive structural and statistical audit.
        """
        if df is None or df.empty:
            return {
                "dataset_name": dataset_name,
                "is_empty": True,
                "total_rows": 0,
                "total_columns": 0,
                "message": "Dataset is empty."
            }

        total_rows = len(df)
        total_cols = len(df.columns)

        # 1. Missing values and data types
        col_profile = {}
        for col in df.columns:
            null_count = int(df[col].isna().sum())
            col_profile[col] = {
                "dtype": str(df[col].dtype),
                "null_count": null_count,
                "null_percentage": round(null_count / total_rows * 100, 2),
                "unique_values": int(df[col].nunique(dropna=True))
            }

        # 2. Numerical variable percentiles
        num_cols = df.select_dtypes(include=[np.number]).columns
        numerical_summary = {}
        for col in num_cols:
            series = df[col].dropna()
            if series.empty:
                continue
            numerical_summary[col] = {
                "count": int(len(series)),
                "mean": round(float(series.mean()), 3),
                "std": round(float(series.std()), 3) if len(series) > 1 else 0.0,
                "min": round(float(series.min()), 3),
                "p25": round(float(np.percentile(series, 25)), 3),
                "median_p50": round(float(series.median()), 3),
                "p75": round(float(np.percentile(series, 75)), 3),
                "p90": round(float(np.percentile(series, 90)), 3),
                "p95": round(float(np.percentile(series, 95)), 3),
                "p99": round(float(np.percentile(series, 99)), 3),
                "max": round(float(series.max()), 3),
            }

        # 3. Temporal coverage
        temporal_info = {}
        target_date_col = None
        for c in ["date", "timestamp", "datetime", "obs_date"]:
            if c in df.columns:
                target_date_col = c
                break

        if target_date_col:
            try:
                dt_series = pd.to_datetime(df[target_date_col].dropna())
                if not dt_series.empty:
                    temporal_info = {
                        "date_column_used": target_date_col,
                        "earliest_date": str(dt_series.min()),
                        "latest_date": str(dt_series.max()),
                        "total_days_span": int((dt_series.max() - dt_series.min()).days),
                        "distinct_dates_count": int(dt_series.dt.date.nunique())
                    }
            except Exception as e:
                temporal_info = {"error": f"Failed parsing dates: {e}"}

        # 4. Spatial coverage
        spatial_info = {}
        for s_col in ["station_id", "location_id", "district", "state"]:
            if s_col in df.columns:
                spatial_info[s_col] = {
                    "unique_count": int(df[s_col].nunique(dropna=True)),
                    "sample_entities": df[s_col].dropna().unique()[:8].tolist()
                }

        # 5. Duplicates
        duplicates_count = int(df.duplicated().sum())

        return {
            "dataset_name": dataset_name,
            "is_empty": False,
            "total_rows": total_rows,
            "total_columns": total_cols,
            "duplicate_rows_count": duplicates_count,
            "column_profiles": col_profile,
            "numerical_summary": numerical_summary,
            "temporal_coverage": temporal_info,
            "spatial_coverage": spatial_info
        }

    def print_report(self, profile: Dict[str, Any]):
        """Prints formatted inspection report to stdout."""
        print("\n" + "=" * 76)
        print(f"  DATASET INSPECTION REPORT: {profile.get('dataset_name', 'Unknown')}")
        print("=" * 76)
        print(f"Total Rows    : {profile.get('total_rows', 0)}")
        print(f"Total Columns : {profile.get('total_columns', 0)}")
        print(f"Duplicate Rows: {profile.get('duplicate_rows_count', 0)}")

        if profile.get("temporal_coverage"):
            t = profile["temporal_coverage"]
            print(f"Date Span     : {t.get('earliest_date')} to {t.get('latest_date')} ({t.get('total_days_span')} days)")

        if profile.get("spatial_coverage"):
            print("Spatial Units :")
            for k, v in profile["spatial_coverage"].items():
                print(f"  - {k}: {v.get('unique_count')} unique entities")

        if profile.get("numerical_summary"):
            print("\nNumerical Variables Summary:")
            print(f"{'Variable':<22} {'Mean':<10} {'Median':<10} {'Min':<10} {'P95':<10} {'Max':<10}")
            print("-" * 76)
            for var, stats in profile["numerical_summary"].items():
                print(f"{var:<22} {stats.get('mean', 0):<10.2f} {stats.get('median_p50', 0):<10.2f} "
                      f"{stats.get('min', 0):<10.2f} {stats.get('p95', 0):<10.2f} {stats.get('max', 0):<10.2f}")
        print("=" * 76 + "\n")
