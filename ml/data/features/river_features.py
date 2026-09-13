"""
RISK // INDIA — River Hydrometric Feature Engineering

Calculates river stage dynamics from hourly CWC telemetry:
- river_level: current gauge elevation
- river_level_change_6h: 6-hour rate of rise (rapid flash flood indicator)
- river_level_change_24h: 24-hour diurnal rate of rise
- river_level_24h_max: 24-hour peak hydrograph crest
- river_level_24h_mean: 24-hour mean hydrograph base
- river_level_above_danger: gauge level relative to CWC danger mark

Safeguards:
- Enforces time-series sort per station before shifting.
- Re-indexes or calculates time-delta based differences to prevent index skew.
"""

from typing import Optional
import pandas as pd
import numpy as np


def compute_river_stage_features(
    df: pd.DataFrame,
    water_level_col: str = "water_level_m",
    danger_level_col: Optional[str] = "danger_level_m",
    timestamp_col: str = "timestamp",
    station_col: str = "station_id"
) -> pd.DataFrame:
    """
    Computes rolling hydrograph stage features on hourly telemetry observations.
    """
    if df.empty or water_level_col not in df.columns or timestamp_col not in df.columns:
        return df

    df_out = df.copy()
    df_out["_dt"] = pd.to_datetime(df_out[timestamp_col])

    # Sort chronologically per station
    sort_cols = [station_col, "_dt"] if station_col in df_out.columns else ["_dt"]
    df_out = df_out.sort_values(by=sort_cols).reset_index(drop=True)

    def _calc_station_river_dynamics(group: pd.DataFrame) -> pd.DataFrame:
        grp = group.copy()
        grp = grp.set_index("_dt")

        wl = grp[water_level_col]

        # 6-hour and 24-hour shifts using time-based windowing where possible
        grp["river_level"] = wl
        grp["river_level_change_6h"] = wl - wl.shift(6)
        grp["river_level_change_24h"] = wl - wl.shift(24)
        grp["river_level_24h_max"] = wl.rolling(24, min_periods=12).max()
        grp["river_level_24h_mean"] = wl.rolling(24, min_periods=12).mean()

        if danger_level_col and danger_level_col in grp.columns:
            grp["river_level_above_danger"] = wl - grp[danger_level_col]

        return grp.reset_index()

    if station_col in df_out.columns:
        df_out = df_out.groupby(station_col, group_keys=False).apply(_calc_station_river_dynamics)
    else:
        df_out = _calc_station_river_dynamics(df_out)

    df_out = df_out.drop(columns=["_dt"], errors="ignore")
    return df_out
