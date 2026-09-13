"""
RISK // INDIA — Assam Flood Tabular ML Prototype Configuration
Central configuration of paths, feature sets, risk thresholds, and validation settings.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ML_DIR = BASE_DIR / "ml"
PROCESSED_DATA_DIR = BASE_DIR / "datasets" / "processed" / "flood_assam"
DEFAULT_DATASET_PATH = PROCESSED_DATA_DIR / "flood_features.csv"

ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"
DEFAULT_MODEL_PATH = ARTIFACTS_DIR / "model.joblib"
DEFAULT_PREPROCESSOR_PATH = ARTIFACTS_DIR / "preprocessor.joblib"
DEFAULT_METADATA_PATH = ARTIFACTS_DIR / "metadata.json"

# Version identifier
MODEL_VERSION = "assam_flood_prototype_v1"

# Target & Group variables
TARGET_COLUMN = "flood_occurrence"
GROUP_COLUMN = "event_group_id"

# 13 verified backward-looking empirical features
NUMERICAL_FEATURES = [
    "rainfall_6h",
    "rainfall_24h",
    "rainfall_72h",
    "rainfall_168h",
    "river_level_relative",
    "river_rise_6h",
    "river_rise_24h",
    "river_percentile_level",
    "month",
    "day_of_year_sin",
    "day_of_year_cos",
    "latitude",
    "longitude",
]

# Documented unavailable features (strictly excluded from training)
UNAVAILABLE_FEATURES = [
    "elevation",
    "slope",
    "distance_to_river",
]

RISK_THRESHOLDS = {
    "Low": (0.00, 0.25),
    "Moderate": (0.26, 0.50),
    "High": (0.51, 0.75),
    "Critical": (0.76, 1.00),
}

# Alias for backwards compatibility
PROVISIONAL_RISK_THRESHOLDS = RISK_THRESHOLDS
