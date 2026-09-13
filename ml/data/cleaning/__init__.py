"""
RISK // INDIA — Data Cleaning & Normalization Package

Provides rigorous preprocessing pipelines:
- CWC Rainfall Cleaner: Filters inactive stations, flags bit errors, generates datasets/interim/
- River Datum Normalizer: Robust mathematical transformations invariant to telemetry datum transitions
"""

from ml.data.cleaning.cwc_rainfall_cleaner import clean_cwc_rainfall_dataset
from ml.data.cleaning.river_datum_normalizer import (
    compute_rate_of_rise,
    compute_rolling_baseline_deviation,
    compute_segmented_standardization,
    compute_percentile_relative_stage
)

__all__ = [
    "clean_cwc_rainfall_dataset",
    "compute_rate_of_rise",
    "compute_rolling_baseline_deviation",
    "compute_segmented_standardization",
    "compute_percentile_relative_stage"
]
