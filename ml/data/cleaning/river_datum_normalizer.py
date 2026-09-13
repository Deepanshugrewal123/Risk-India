"""
RISK // INDIA — River Water Level Datum Normalization Engine

Resolves the documented telemetry datum transition in CWC river crossing gauges:
- 2022–2023: Relative river stage above zero gauge (medians 1.2–3.1 m)
- 2024–2025: Geodetic bridge benchmark / MSL elevation (medians 30.4–80.2 m)

Provides 4 mathematically sound normalizations invariant to datum shifts:
1. Rate of Rise (Delta H): first difference is invariant to vertical datum translation.
2. Rolling Baseline Deviation: H_t - median_14d(H) removes slow baseline elevation changes.
3. Segmented Standardization: Era-specific z-score normalization (Pre-2024 vs Post-2024).
4. Percentile-Based Relative Stage: Empirical cumulative probability ranking within each era.

Includes despiking for digital bit corruption (32 transmission spikes > 100 m).
Preserves raw values untouched.
"""

from typing import Optional, Dict, Any, List
import pandas as pd
import numpy as np

MAX_PLAUSIBLE_WATER_STAGE_M = 100.0
DATUM_TRANSITION_DATE = pd.Timestamp("2024-01-01")


def filter_river_transmission_spikes(
    df: pd.DataFrame,
    water_level_col: str = "River Water Level Telemetry Hourly (meter)",
    max_threshold_m: float = MAX_PLAUSIBLE_WATER_STAGE_M
) -> pd.DataFrame:
    """
    Identifies and flags digital transmission spikes (> 100m, up to 1,018m).
    """
    df_out = df.copy()
    spike_mask = df_out[water_level_col] > max_threshold_m
    df_out["is_rwl_spike_flag"] = spike_mask.astype(int)
    # Capped / despiked representation
    df_out["despiked_water_level_m"] = df_out[water_level_col].where(~spike_mask, np.nan)
    return df_out


def compute_rate_of_rise(
    df: pd.DataFrame,
    water_level_col: str = "River Water Level Telemetry Hourly (meter)",
    time_col: str = "Data Acquisition Time",
    station_col: str = "Station",
    lag_hours: int = 1
) -> pd.Series:
    """
    Computes rate of rise: Delta H = H(t) - H(t - lag).
    First-order differencing is mathematically invariant to constant vertical datum translation.
    """
    df_sorted = df.sort_values([station_col, time_col]).copy()
    diff_series = df_sorted.groupby(station_col)[water_level_col].diff(periods=lag_hours)
    return diff_series.round(4)


def compute_rolling_baseline_deviation(
    df: pd.DataFrame,
    water_level_col: str = "River Water Level Telemetry Hourly (meter)",
    time_col: str = "parsed_datetime",
    station_col: str = "Station",
    window_hours: int = 336 # 14 days
) -> pd.Series:
    """
    Calculates deviation from a 14-day rolling baseline:
    Dev_t = H_t - median_14d(H).
    Removes elevation datum shift while isolating acute storm hydrograph crests.
    """
    df_sorted = df.sort_values([station_col, time_col]).copy()

    def _calc_station_deviation(group: pd.DataFrame) -> pd.Series:
        # Rolling median over window
        rolling_median = group[water_level_col].rolling(window=window_hours, min_periods=24).median()
        return (group[water_level_col] - rolling_median).round(3)

    deviation = df_sorted.groupby(station_col, group_keys=False).apply(_calc_station_deviation)
    return deviation


def compute_segmented_standardization(
    df: pd.DataFrame,
    water_level_col: str = "River Water Level Telemetry Hourly (meter)",
    time_col: str = "parsed_datetime",
    station_col: str = "Station",
    transition_date: pd.Timestamp = DATUM_TRANSITION_DATE
) -> pd.Series:
    """
    Standardizes water levels separately for Era 1 (2022–2023: Stage) and Era 2 (2024–2025: MSL):
    z = (H - mu_era) / sigma_era per station.
    """
    df_work = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df_work[time_col]):
        df_work["_dt"] = pd.to_datetime(df_work[time_col])
    else:
        df_work["_dt"] = df_work[time_col]

    df_work["_era"] = np.where(df_work["_dt"] < transition_date, "ERA_1_STAGE", "ERA_2_MSL")

    def _standardize_era(group: pd.DataFrame) -> pd.Series:
        mu = group[water_level_col].mean()
        sigma = group[water_level_col].std()
        if pd.isna(sigma) or sigma == 0:
            return pd.Series(0.0, index=group.index)
        return ((group[water_level_col] - mu) / sigma).round(3)

    z_scores = df_work.groupby([station_col, "_era"], group_keys=False).apply(_standardize_era)
    return z_scores


def compute_percentile_relative_stage(
    df: pd.DataFrame,
    water_level_col: str = "River Water Level Telemetry Hourly (meter)",
    time_col: str = "parsed_datetime",
    station_col: str = "Station",
    transition_date: pd.Timestamp = DATUM_TRANSITION_DATE
) -> pd.Series:
    """
    Computes empirical cumulative distribution percentile (0.0 to 1.0) within each station and era.
    """
    df_work = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df_work[time_col]):
        df_work["_dt"] = pd.to_datetime(df_work[time_col])
    else:
        df_work["_dt"] = df_work[time_col]

    df_work["_era"] = np.where(df_work["_dt"] < transition_date, "ERA_1_STAGE", "ERA_2_MSL")

    def _rank_era(group: pd.DataFrame) -> pd.Series:
        return (group[water_level_col].rank(pct=True)).round(4)

    ranks = df_work.groupby([station_col, "_era"], group_keys=False).apply(_rank_era)
    return ranks
