"""
RISK // INDIA — National Flood ML Configuration & Feature Schemas
=================================================================
Defines configuration constants, features, candidate model specifications,
and serialization paths for 'risk_india_flood_v1'.
"""

import os

# Project root path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Dataset Paths
RAW_IMD_DATASET = os.path.join(BASE_DIR, "datasets", "raw", "imd", "rainfall_districtwise_daily_imd.csv")
PROCESSED_DATASET = os.path.join(BASE_DIR, "datasets", "processed", "national_flood", "national_flood_features.csv")

# Artifact Paths
ARTIFACTS_DIR = os.path.join(BASE_DIR, "ml", "national_flood", "artifacts")
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "model.joblib")
METADATA_PATH = os.path.join(ARTIFACTS_DIR, "metadata.json")

# Model Metadata
MODEL_NAME = "risk_india_flood_v1"
MODEL_DISPLAY_NAME = "RISK // INDIA Flood Model v1"
PUBLIC_DESCRIPTION = "India-Wide Empirical Flood Intelligence"
MODEL_VERSION = "1.0.0"

# Target & Feature Schema
TARGET_COLUMN = "flood_risk_event"

FEATURE_COLUMNS = [
    "actual_rainfall_24h_mm",
    "normal_rainfall_24h_mm",
    "rainfall_departure_pct",
    "weekly_rainfall_actual_mm",
    "weekly_rainfall_normal_mm",
    "weekly_departure_pct",
    "cumulative_monsoon_rainfall_mm",
    "monthly_rainfall_actual_mm",
    "monthly_departure_pct",
    "antecedent_saturation_index",
    "basin_flood_vulnerability",
    "latitude",
    "longitude",
    "day_of_year_sin",
    "day_of_year_cos"
]

FEATURE_DESCRIPTIONS = {
    "actual_rainfall_24h_mm": "Observed 24-hour daily precipitation (mm) from IMD district network",
    "normal_rainfall_24h_mm": "Climatological normal daily rainfall (mm) for the district",
    "rainfall_departure_pct": "Daily precipitation departure from normal percentage",
    "weekly_rainfall_actual_mm": "7-day antecedent cumulative precipitation (mm)",
    "weekly_rainfall_normal_mm": "Climatological 7-day normal precipitation (mm)",
    "weekly_departure_pct": "7-day precipitation departure from normal percentage",
    "cumulative_monsoon_rainfall_mm": "Season-to-date cumulative monsoon precipitation (mm)",
    "monthly_rainfall_actual_mm": "Month-to-date cumulative precipitation (mm)",
    "monthly_departure_pct": "Month-to-date precipitation departure from normal percentage",
    "antecedent_saturation_index": "Compound soil saturation & catchment moisture index [0.0 - 1.0]",
    "basin_flood_vulnerability": "River basin morphometric & chronic flood susceptibility index [0.0 - 1.0]",
    "latitude": "District centroid latitude (WGS84 EPSG:4326)",
    "longitude": "District centroid longitude (WGS84 EPSG:4326)",
    "day_of_year_sin": "Cyclical seasonal monsoon phase (sine transform)",
    "day_of_year_cos": "Cyclical seasonal monsoon phase (cosine transform)"
}

# Regional Zones Mapping for Holdout Evaluation
REGIONAL_ZONES = {
    "North": [
        "Uttar Pradesh", "Himachal Pradesh", "Punjab", "Haryana",
        "Jammu and Kashmir", "Ladakh", "Delhi", "Chandigarh", "Uttarakhand"
    ],
    "Central": [
        "Madhya Pradesh", "Chhattisgarh"
    ],
    "East": [
        "Bihar", "Jharkhand", "Odisha", "West Bengal"
    ],
    "Northeast": [
        "Assam", "Arunachal Pradesh", "Meghalaya", "Mizoram",
        "Nagaland", "Tripura", "Sikkim", "Manipur"
    ],
    "West": [
        "Maharashtra", "Gujarat", "Goa", "Rajasthan",
        "Dadra and Nagar Haveli and Daman and Diu"
    ],
    "South": [
        "Andhra Pradesh", "Telangana", "Karnataka", "Kerala",
        "Tamil Nadu", "Puducherry", "Lakshadweep", "Andaman and Nicobar Islands"
    ]
}
