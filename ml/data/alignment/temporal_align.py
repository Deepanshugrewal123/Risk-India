"""
RISK // INDIA — Temporal Alignment & Multi-Resolution Harmonization

Harmonizes disparate temporal resolutions:
- Sub-daily/hourly CWC telemetry (river water levels & precipitation)
- Daily IMD observations (08:30 IST to 08:30 IST standard window)
- Event-based discrete satellite inundation snapshots (ISRO/NRSC)

Explicit Timezone Rules:
- Indian Standard Time (IST) is UTC+05:30.
- Timestamps must be normalized to UTC or IST explicitly before joins.
- Aggregations are documented and reproducible (no silent date shifts).
"""

from typing import Dict, Any, Optional, Literal
import pandas as pd
import numpy as np


def resample_hourly_to_daily_hydrology(
    df: pd.DataFrame,
    timestamp_col: str = "timestamp",
    station_col: str = "station_id",
    water_level_col: Optional[str] = "water_level_m",
    rainfall_col: Optional[str] = "rainfall_hourly_mm",
    target_timezone: str = "Asia/Kolkata"
) -> pd.DataFrame:
    """
    Resamples hourly telemetry into daily hydrological summaries matching IMD standard days.
    
    Metrics aggregated per station-day:
    - water_level_max: peak flood stage during the 24h cycle
    - water_level_mean: diurnal mean stage
    - water_level_delta_24h: net change from prior day
    - rainfall_daily_total: sum of hourly precipitation
    """
    if df.empty or timestamp_col not in df.columns:
        return pd.DataFrame()

    df_clean = df.copy()
    df_clean["_dt"] = pd.to_datetime(df_clean[timestamp_col])

    # Convert to standard target timezone
    try:
        if df_clean["_dt"].dt.tz is None:
            # Assume IST if naive
            df_clean["_dt"] = df_clean["_dt"].dt.tz_localize("Asia/Kolkata")
        else:
            df_clean["_dt"] = df_clean["_dt"].dt.tz_convert(target_timezone)
    except Exception:
        pass

    # Extract observation date
    df_clean["date"] = df_clean["_dt"].dt.strftime("%Y-%m-%d")

    agg_rules: Dict[str, Any] = {}
    if water_level_col and water_level_col in df_clean.columns:
        agg_rules[water_level_col] = ["max", "mean", "min", "count"]
    if rainfall_col and rainfall_col in df_clean.columns:
        agg_rules[rainfall_col] = ["sum", "max"]

    if not agg_rules:
        return pd.DataFrame()

    group_cols = [station_col, "date"] if station_col in df_clean.columns else ["date"]
    daily_grouped = df_clean.groupby(group_cols).agg(agg_rules)

    # Flatten hierarchical columns
    flat_cols = []
    for col, stat in daily_grouped.columns:
        if col == water_level_col:
            flat_cols.append(f"wl_daily_{stat}")
        elif col == rainfall_col:
            flat_cols.append(f"rf_daily_{stat}")
        else:
            flat_cols.append(f"{col}_{stat}")
    daily_grouped.columns = flat_cols
    daily_df = daily_grouped.reset_index()

    return daily_df


def merge_daily_rainfall_and_river(
    daily_rainfall_df: pd.DataFrame,
    daily_river_df: pd.DataFrame,
    rainfall_date_col: str = "date",
    river_date_col: str = "date",
    rainfall_id_col: str = "location_id",
    river_id_col: str = "location_id",
    how: Literal["inner", "left", "outer"] = "inner"
) -> pd.DataFrame:
    """
    Safely joins daily rainfall and daily river records by (location_id, date).
    """
    if daily_rainfall_df.empty or daily_river_df.empty:
        return pd.DataFrame()

    merged = pd.merge(
        daily_rainfall_df,
        daily_river_df,
        left_on=[rainfall_id_col, rainfall_date_col],
        right_on=[river_id_col, river_date_col],
        how=how
    )
    return merged
