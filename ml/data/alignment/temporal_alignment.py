"""
RISK // INDIA — Temporal Alignment & Multi-Window Feature Extraction

Extracts antecedent hydrometeorological feature windows for target flood event timestamps:
- Candidate predictor windows: 6 hours, 24 hours, 72 hours, 168 hours
- Missingness & Sufficiency Guard: Enforces minimum coverage threshold (default >= 70%)
  before declaring a window valid
- Zero Temporal Leakage: Strictly verifies that max(t_predictor) <= t_event
- Records structured alignment audit metadata
"""

from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np

CANDIDATE_WINDOWS_HOURS = [6, 24, 72, 168]
MIN_DATA_SUFFICIENCY_PCT = 70.0


class TemporalEventAligner:
    """
    Constructs multi-window antecedent hydrometeorological feature vectors with strict causal isolation.
    """

    def __init__(
        self,
        rainfall_df: pd.DataFrame,
        river_df: Optional[pd.DataFrame] = None,
        rain_time_col: str = "Data Acquisition Time",
        rain_val_col: str = "Telemetry Hourly Rainfall (mm)",
        river_time_col: str = "Data Acquisition Time",
        river_val_col: str = "River Water Level Telemetry Hourly (meter)",
        date_format: str = "%d-%m-%Y %H:%M",
        min_sufficiency_pct: float = MIN_DATA_SUFFICIENCY_PCT
    ):
        self.min_sufficiency = min_sufficiency_pct

        # Prepare rainfall time-series
        self.rf = rainfall_df.copy()
        self.rf_val_col = rain_val_col
        if not self.rf.empty:
            if not pd.api.types.is_datetime64_any_dtype(self.rf[rain_time_col]):
                self.rf["_dt"] = pd.to_datetime(self.rf[rain_time_col], format=date_format, errors="coerce")
            else:
                self.rf["_dt"] = self.rf[rain_time_col]
            self.rf = self.rf.dropna(subset=["_dt"]).sort_values("_dt")
        else:
            self.rf["_dt"] = pd.Series(dtype="datetime64[ns]")

        # Prepare river time-series
        self.rwl_val_col = river_val_col
        if river_df is not None and not river_df.empty:
            self.rwl = river_df.copy()
            if not pd.api.types.is_datetime64_any_dtype(self.rwl[river_time_col]):
                self.rwl["_dt"] = pd.to_datetime(self.rwl[river_time_col], format=date_format, errors="coerce")
            else:
                self.rwl["_dt"] = self.rwl[river_time_col]
            self.rwl = self.rwl.dropna(subset=["_dt"]).sort_values("_dt")
        else:
            self.rwl = pd.DataFrame()
            self.rwl["_dt"] = pd.Series(dtype="datetime64[ns]")

    def extract_window_rainfall(
        self,
        event_dt: pd.Timestamp,
        window_hours: int,
        station_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculates cumulative precipitation in [event_dt - window_hours, event_dt] with sufficiency checks.
        """
        w_start = event_dt - pd.Timedelta(hours=window_hours)
        rf_sub = self.rf[(self.rf["_dt"] <= event_dt) & (self.rf["_dt"] >= w_start)]

        if station_id and "Station" in rf_sub.columns:
            rf_sub = rf_sub[rf_sub["Station"] == station_id]

        expected_obs = window_hours
        actual_obs = len(rf_sub)
        coverage_pct = round((actual_obs / expected_obs) * 100.0, 2) if expected_obs > 0 else 0.0

        is_sufficient = coverage_pct >= self.min_sufficiency
        cum_val = float(rf_sub[self.rf_val_col].sum()) if not rf_sub.empty else 0.0

        return {
            "window_hours": window_hours,
            "cumulative_rainfall_mm": round(cum_val, 2) if is_sufficient else None,
            "raw_sum_mm": round(cum_val, 2),
            "expected_observations": expected_obs,
            "actual_observations": actual_obs,
            "coverage_pct": coverage_pct,
            "is_sufficient": is_sufficient,
            "status": "VALID" if is_sufficient else f"INSUFFICIENT_COVERAGE_{coverage_pct:.1f}%"
        }

    def extract_antecedent_features_for_event(
        self,
        event_timestamp: pd.Timestamp,
        station_id: Optional[str] = None,
        gauge_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extracts multi-window antecedent hydrometeorological features strictly preceding event_timestamp.
        """
        event_dt = pd.to_datetime(event_timestamp)

        # 1. Rainfall windows
        windows_result = {}
        rf_leak_free = True
        rf_subset_all = self.rf[self.rf["_dt"] <= event_dt]
        if station_id and "Station" in rf_subset_all.columns:
            rf_subset_all = rf_subset_all[rf_subset_all["Station"] == station_id]

        max_rf_dt = rf_subset_all["_dt"].max() if not rf_subset_all.empty else None
        if max_rf_dt is not None and max_rf_dt > event_dt:
            rf_leak_free = False

        for w_h in CANDIDATE_WINDOWS_HOURS:
            w_res = self.extract_window_rainfall(event_dt, w_h, station_id=station_id)
            windows_result[f"rainfall_{w_h}h"] = w_res["cumulative_rainfall_mm"]
            windows_result[f"rainfall_{w_h}h_coverage_pct"] = w_res["coverage_pct"]
            windows_result[f"rainfall_{w_h}h_status"] = w_res["status"]

        # 2. River level readings
        river_level = None
        river_level_change_24h = None
        rwl_coverage_pct = 0.0
        rwl_leak_free = True

        if not self.rwl.empty:
            rwl_sub = self.rwl[self.rwl["_dt"] <= event_dt]
            if gauge_id and "Station" in rwl_sub.columns:
                rwl_sub = rwl_sub[rwl_sub["Station"] == gauge_id]

            if not rwl_sub.empty:
                max_rwl_dt = rwl_sub["_dt"].max()
                if max_rwl_dt > event_dt:
                    rwl_leak_free = False

                latest_row = rwl_sub.iloc[-1]
                river_level = float(latest_row[self.rwl_val_col])

                # 24h rate of rise
                sub_24h = rwl_sub[rwl_sub["_dt"] >= (event_dt - pd.Timedelta(hours=24))]
                rwl_coverage_pct = round((len(sub_24h) / 24.0) * 100.0, 2)

                prior_24h_sub = rwl_sub[rwl_sub["_dt"] <= (event_dt - pd.Timedelta(hours=24))]
                if not prior_24h_sub.empty:
                    prior_level = float(prior_24h_sub.iloc[-1][self.rwl_val_col])
                    river_level_change_24h = round(river_level - prior_level, 4)

        leakage_prevented = bool(rf_leak_free and rwl_leak_free)

        return {
            "event_timestamp": str(event_dt),
            "rainfall_windows": windows_result,
            "river_level": round(river_level, 3) if river_level is not None else None,
            "river_level_change_24h": river_level_change_24h,
            "river_level_24h_coverage_pct": rwl_coverage_pct,
            "temporal_leakage_prevented": leakage_prevented,
            "max_predictor_timestamp_used": str(max(filter(None, [max_rf_dt, rwl_sub["_dt"].max() if not self.rwl.empty and not rwl_sub.empty else None]))) if (max_rf_dt is not None or (not self.rwl.empty and not rwl_sub.empty)) else None,
            "alignment_status": "VALID_ALIGNMENT" if leakage_prevented else "LEAKAGE_DETECTED"
        }
