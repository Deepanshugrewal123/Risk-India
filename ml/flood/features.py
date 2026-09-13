"""
RISK // INDIA — Flood Feature Engineering & Registry

Provides:
- Feature metadata registry (units, sources, tiers)
- Feature extraction functions for raw telemetry records
- Domain-specific feature engineering (monsoon flags, topographic indicators)
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np

# Official feature registry documenting provenance & tiers
FEATURE_REGISTRY: Dict[str, Dict[str, Any]] = {
    "rainfall_24h": {
        "unit": "mm",
        "tier": "Tier 1 (Core)",
        "source": "IMD Automated Weather Stations (AWS) / GPM IMERG Gridded",
        "description": "Daily 24-hour total precipitation accumulation."
    },
    "rainfall_72h_cumulative": {
        "unit": "mm",
        "tier": "Tier 1 (Core)",
        "source": "IMD 3-day rolling accumulation",
        "description": "Antecedent 72-hour precipitation tracking soil pore saturation."
    },
    "elevation": {
        "unit": "meters",
        "tier": "Tier 1 (Core)",
        "source": "ISRO Bhuvan CartoDEM (30m) / SRTM",
        "description": "Digital Elevation Model mean topographic height."
    },
    "slope": {
        "unit": "degrees",
        "tier": "Tier 1 (Core)",
        "source": "Derived from DEM gradient vectors",
        "description": "Topographical slope angle. Flat low-slope terrain (< 3°) impedes runoff."
    },
    "monsoon_season_flag": {
        "unit": "binary (0/1)",
        "tier": "Tier 1 (Core)",
        "source": "IMD Climatological Calendar",
        "description": "Indicator variable for Southwest Monsoon (June 1 - September 30)."
    },
    "rainfall_anomaly": {
        "unit": "%",
        "tier": "Tier 2 (Optional)",
        "source": "IMD Long Period Average (LPA) Departure",
        "description": "Percentage deviation from normal historical precipitation."
    },
    "soil_moisture_index": {
        "unit": "%",
        "tier": "Tier 2 (Optional)",
        "source": "SMAP / Sentinel-1 / NRSC Hydrological Observatory",
        "description": "Root zone soil moisture saturation percentage."
    },
    "river_gauge_above_danger": {
        "unit": "meters",
        "tier": "Tier 2 (Optional)",
        "source": "Central Water Commission (CWC) River Hydrometry Network",
        "description": "Gauge level height above designated CWC river danger stage."
    },
    "distance_to_river_km": {
        "unit": "km",
        "tier": "Tier 2 (Optional)",
        "source": "Survey of India / HydroSHEDS hydrographic network",
        "description": "Euclidean distance to the nearest perennial river stream channel."
    },
    "historical_flood_frequency": {
        "unit": "count",
        "tier": "Tier 2 (Optional)",
        "source": "NDMA / State Disaster Management Authority (SDMA) Reports",
        "description": "Frequency of inundated occurrences recorded over prior decade."
    },
    "catchment_area_sqkm": {
        "unit": "km²",
        "tier": "Tier 3 (Future)",
        "source": "CWC / HydroBASINS watershed delineations",
        "description": "Total upstream drainage catchment collecting surface runoff."
    },
    "drainage_density": {
        "unit": "km/km²",
        "tier": "Tier 3 (Future)",
        "source": "GIS Stream Network Analysis",
        "description": "Total length of river channels per unit catchment area."
    }
}


def compute_monsoon_flag(date_val: Any) -> int:
    """
    Returns 1 if date falls within India's Southwest Monsoon window (June through September),
    otherwise 0.
    """
    try:
        dt = pd.to_datetime(date_val)
        return 1 if dt.month in [6, 7, 8, 9] else 0
    except Exception:
        return 1  # Default to conservative assumption


def engineer_flood_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches raw tabular dataframe with derived hydrological and geomorphic features.
    """
    df_out = df.copy()

    # 1. Date extraction & monsoon flag
    if "date" in df_out.columns:
        df_out["date"] = pd.to_datetime(df_out["date"])
        df_out["monsoon_season_flag"] = df_out["date"].dt.month.isin([6, 7, 8, 9]).astype(int)
    elif "monsoon_season_flag" not in df_out.columns:
        df_out["monsoon_season_flag"] = 1

    # 2. Estimate 72h cumulative rainfall if missing but 24h is available
    if "rainfall_72h_cumulative" not in df_out.columns or df_out["rainfall_72h_cumulative"].isnull().all():
        if "rainfall_24h" in df_out.columns:
            # Domain heuristic proxy: 72h cumulative is conservatively ~2.2x 24h if sustained
            df_out["rainfall_72h_cumulative"] = df_out["rainfall_24h"] * 2.2

    # 3. Topographic Wetness Index proxy (Rainfall / (tan(slope) + epsilon))
    if "rainfall_24h" in df_out.columns and "slope" in df_out.columns:
        slope_rad = np.radians(np.clip(df_out["slope"], 0.1, 89.9))
        df_out["wetness_runoff_index"] = df_out["rainfall_24h"] / (np.tan(slope_rad) + 0.05)

    return df_out
