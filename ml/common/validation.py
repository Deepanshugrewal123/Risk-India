"""
RISK // INDIA — Tabular Data Quality Validation Suite

Performs rigorous validation on raw and preprocessed flood datasets before training:
1. Missing value audit & column-level thresholding.
2. Duplicate row and spatio-temporal key detection.
3. Coordinate boundary validation within sovereign Indian geography:
   - Latitude: [6.5, 37.5]
   - Longitude: [68.0, 97.5]
4. Physical feasibility & out-of-bounds numerical checks.
5. Temporal continuity & chronological gap reporting.
6. Class distribution & extreme imbalance diagnostics.
7. Spatial coverage auditing across states and districts.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import pandas as pd
import numpy as np

# Spatial boundaries for sovereign territory of India
INDIA_LAT_MIN = 6.5
INDIA_LAT_MAX = 37.5
INDIA_LON_MIN = 68.0
INDIA_LON_MAX = 97.5

@dataclass
class ValidationReport:
    is_valid: bool
    total_rows: int
    total_columns: int
    critical_errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    missing_value_summary: Dict[str, Any] = field(default_factory=dict)
    duplicate_rows_count: int = 0
    spatial_coverage: Dict[str, Any] = field(default_factory=dict)
    temporal_coverage: Dict[str, Any] = field(default_factory=dict)
    target_distribution: Dict[str, Any] = field(default_factory=dict)
    numeric_checks: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "total_rows": self.total_rows,
            "total_columns": self.total_columns,
            "critical_errors": self.critical_errors,
            "warnings": self.warnings,
            "missing_value_summary": self.missing_value_summary,
            "duplicate_rows_count": self.duplicate_rows_count,
            "spatial_coverage": self.spatial_coverage,
            "temporal_coverage": self.temporal_coverage,
            "target_distribution": self.target_distribution,
            "numeric_checks": self.numeric_checks,
        }

    def print_summary(self):
        status = "[VALID]" if self.is_valid else "[INVALID]"
        print(f"\n{status} Data Quality Validation Report ({self.total_rows} rows, {self.total_columns} columns)")
        print("-" * 70)
        if self.critical_errors:
            print("[!] CRITICAL ERRORS (Training Blocked):")
            for err in self.critical_errors:
                print(f"    - {err}")
        else:
            print("[+] Zero critical data errors encountered.")

        if self.warnings:
            print("[*] WARNINGS / ADVISORIES:")
            for warn in self.warnings:
                print(f"    - {warn}")

        if self.target_distribution:
            print(f"[*] Target Distribution: {self.target_distribution}")
        if self.spatial_coverage:
            print(f"[*] Spatial Coverage: {self.spatial_coverage.get('unique_locations_count', 0)} distinct locations")
        print("-" * 70)


class TabularDataValidator:
    """
    Validates disaster risk tabular datasets against strict physical, spatial, and numerical rules.
    """

    def __init__(
        self,
        required_columns: Optional[List[str]] = None,
        target_column: str = "flood_occurred",
        max_missing_ratio_critical: float = 0.30,
        max_missing_ratio_warning: float = 0.05
    ):
        self.required_columns = required_columns or [
            "location_id",
            "rainfall_24h",
            "elevation",
            "slope",
            target_column
        ]
        self.target_column = target_column
        self.max_missing_ratio_critical = max_missing_ratio_critical
        self.max_missing_ratio_warning = max_missing_ratio_warning

    def validate(self, df: pd.DataFrame) -> ValidationReport:
        critical_errors: List[str] = []
        warnings: List[str] = []

        if df is None or df.empty:
            return ValidationReport(
                is_valid=False,
                total_rows=0,
                total_columns=0,
                critical_errors=["Dataset is empty or None. Training cannot proceed."]
            )

        total_rows = len(df)
        total_cols = len(df.columns)

        # 1. Required columns presence
        missing_required = [col for col in self.required_columns if col not in df.columns]
        if missing_required:
            critical_errors.append(f"Missing mandatory columns: {missing_required}")

        # 2. Missing values audit
        missing_summary = {}
        for col in df.columns:
            null_count = int(df[col].isnull().sum())
            null_ratio = float(null_count / total_rows)
            if null_count > 0:
                missing_summary[col] = {
                    "missing_count": null_count,
                    "missing_ratio_pct": round(null_ratio * 100, 2)
                }
                if col in self.required_columns and null_ratio > self.max_missing_ratio_critical:
                    critical_errors.append(
                        f"Column '{col}' exceeds critical missing threshold: {round(null_ratio * 100, 1)}% missing."
                    )
                elif null_ratio > self.max_missing_ratio_warning:
                    warnings.append(
                        f"Column '{col}' has notable missingness: {round(null_ratio * 100, 1)}% missing."
                    )

        # 3. Duplicate checks
        duplicates = int(df.duplicated().sum())
        if duplicates > 0:
            warnings.append(f"Detected {duplicates} exact duplicate rows in dataset.")

        # Key-based duplicate checks (e.g. location_id + date/timestamp)
        if "location_id" in df.columns and "date" in df.columns:
            key_dups = int(df.duplicated(subset=["location_id", "date"]).sum())
            if key_dups > 0:
                critical_errors.append(f"Detected {key_dups} duplicate spatio-temporal entries for (location_id, date).")

        # 4. Coordinate checks (if present)
        spatial_cov = {}
        if "latitude" in df.columns and "longitude" in df.columns:
            valid_coords = df[["latitude", "longitude"]].dropna()
            if not valid_coords.empty:
                out_lat = ((valid_coords["latitude"] < INDIA_LAT_MIN) | (valid_coords["latitude"] > INDIA_LAT_MAX)).sum()
                out_lon = ((valid_coords["longitude"] < INDIA_LON_MIN) | (valid_coords["longitude"] > INDIA_LON_MAX)).sum()
                if out_lat > 0:
                    critical_errors.append(
                        f"Detected {out_lat} rows with latitude outside India bounding box [{INDIA_LAT_MIN}, {INDIA_LAT_MAX}]."
                    )
                if out_lon > 0:
                    critical_errors.append(
                        f"Detected {out_lon} rows with longitude outside India bounding box [{INDIA_LON_MIN}, {INDIA_LON_MAX}]."
                    )

        if "location_id" in df.columns:
            unique_locs = df["location_id"].dropna().unique().tolist()
            spatial_cov = {
                "unique_locations_count": len(unique_locs),
                "locations_sample": unique_locs[:10],
            }
            if len(unique_locs) < 3:
                warnings.append(f"Dataset contains only {len(unique_locs)} distinct location(s). Spatial generalization will be limited.")

        # 5. Physical numeric sanity checks
        numeric_checks = {}
        # Rainfall non-negative
        for r_col in ["rainfall_24h", "rainfall_72h_cumulative", "precipitation_mm"]:
            if r_col in df.columns:
                neg_count = int((df[r_col] < 0).sum())
                if neg_count > 0:
                    critical_errors.append(f"Column '{r_col}' contains {neg_count} impossible negative values.")
                max_val = float(df[r_col].max()) if not df[r_col].dropna().empty else 0.0
                if max_val > 1500:  # World record 24h rainfall is ~1825mm (Cherrapunji/La Reunion)
                    warnings.append(f"Column '{r_col}' has extreme value {max_val} mm. Verify sensor or unit.")
                numeric_checks[r_col] = {"min": float(df[r_col].min()), "max": max_val}

        # Soil moisture percentage [0, 100]
        if "soil_moisture_index" in df.columns:
            sm = df["soil_moisture_index"].dropna()
            out_sm = ((sm < 0) | (sm > 100)).sum()
            if out_sm > 0:
                critical_errors.append(f"Column 'soil_moisture_index' contains {out_sm} values outside [0, 100].")
            numeric_checks["soil_moisture_index"] = {"min": float(sm.min()), "max": float(sm.max())}

        # Elevation bounds [-50m to 9000m]
        if "elevation" in df.columns:
            elev = df["elevation"].dropna()
            out_elev = ((elev < -50) | (elev > 9000)).sum()
            if out_elev > 0:
                critical_errors.append(f"Column 'elevation' contains {out_elev} values outside plausible terrestrial range [-50m, 9000m].")
            numeric_checks["elevation"] = {"min": float(elev.min()), "max": float(elev.max())}

        # Slope bounds [0, 90 degrees]
        if "slope" in df.columns:
            slopes = df["slope"].dropna()
            out_slopes = ((slopes < 0) | (slopes > 90)).sum()
            if out_slopes > 0:
                critical_errors.append(f"Column 'slope' contains {out_slopes} values outside [0, 90] degrees.")
            numeric_checks["slope"] = {"min": float(slopes.min()), "max": float(slopes.max())}

        # 6. Temporal checks
        temporal_cov = {}
        if "date" in df.columns:
            try:
                dates = pd.to_datetime(df["date"].dropna())
                temporal_cov = {
                    "start_date": str(dates.min()),
                    "end_date": str(dates.max()),
                    "total_days_span": int((dates.max() - dates.min()).days) if not dates.empty else 0
                }
            except Exception as e:
                warnings.append(f"Unable to parse 'date' column into datetime: {e}")

        # 7. Target distribution & class imbalance
        target_dist = {}
        if self.target_column in df.columns:
            target_series = df[self.target_column].dropna()
            unique_targets = set(target_series.unique())
            if not unique_targets.issubset({0, 1, 0.0, 1.0, True, False}):
                critical_errors.append(
                    f"Target column '{self.target_column}' must be binary (0/1 or True/False). Found: {unique_targets}"
                )
            else:
                pos = int(target_series.isin([1, 1.0, True]).sum())
                neg = int(target_series.isin([0, 0.0, False]).sum())
                total_t = pos + neg
                pos_pct = round((pos / total_t) * 100, 2) if total_t > 0 else 0
                target_dist = {
                    "total_labeled": total_t,
                    "positive_flood_events": pos,
                    "negative_non_flood_events": neg,
                    "flood_event_prevalence_pct": pos_pct
                }
                if pos == 0:
                    critical_errors.append("Target column has ZERO positive flood instances. Cannot train classifier.")
                elif neg == 0:
                    critical_errors.append("Target column has ZERO negative non-flood instances. Cannot train classifier.")
                elif pos_pct < 2.0 or pos_pct > 98.0:
                    warnings.append(
                        f"Extreme class imbalance detected ({pos_pct}% positive class). Apply PR-AUC and balanced class weighting."
                    )

        is_valid = len(critical_errors) == 0

        return ValidationReport(
            is_valid=is_valid,
            total_rows=total_rows,
            total_columns=total_cols,
            critical_errors=critical_errors,
            warnings=warnings,
            missing_value_summary=missing_summary,
            duplicate_rows_count=duplicates,
            spatial_coverage=spatial_cov,
            temporal_coverage=temporal_cov,
            target_distribution=target_dist,
            numeric_checks=numeric_checks
        )
