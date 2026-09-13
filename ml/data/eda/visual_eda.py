"""
RISK // INDIA — Visual EDA Generator

Generates publication-friendly diagnostic plots using Matplotlib:
1. Rainfall distribution & heavy precipitation tails
2. Chronological rainfall time series
3. Extreme rainfall events (95th/99th percentile exceedance)
4. River stage hydrograph with CWC danger level thresholds
5. Missingness matrix / missing data visualization
6. Station geographical spatial scatter

Uses non-interactive 'Agg' backend to avoid blocking processes or popups.
"""

from pathlib import Path
from typing import Optional, List
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

DEFAULT_FIG_DIR = Path(__file__).resolve().parents[3] / "docs" / "figures"


class VisualEDAGenerator:
    """
    Renders publication-grade diagnostic plots for disaster telemetry.
    """

    def __init__(self, output_dir: Path = DEFAULT_FIG_DIR):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        # Apply clean styling
        plt.rcParams["font.sans-serif"] = "DejaVu Sans"
        plt.rcParams["axes.edgecolor"] = "#CCCCCC"
        plt.rcParams["axes.linewidth"] = 0.8

    def plot_rainfall_distribution(
        self,
        df: pd.DataFrame,
        rainfall_col: str = "rainfall_mm",
        save_filename: str = "rainfall_distribution.png"
    ) -> Optional[Path]:
        """Plots distribution of precipitation with heavy tail log-scale inset."""
        if df.empty or rainfall_col not in df.columns:
            return None

        series = df[rainfall_col].dropna()
        if series.empty:
            return None

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5), dpi=150)

        # Plot 1: Standard histogram (linear)
        ax1.hist(series, bins=35, color="#1D5C96", edgecolor="white", alpha=0.85)
        ax1.set_title("Precipitation Distribution (Linear Scale)", fontsize=11, fontweight="bold")
        ax1.set_xlabel("Daily Rainfall (mm)")
        ax1.set_ylabel("Frequency (Count)")
        ax1.grid(True, linestyle="--", alpha=0.4)

        # Plot 2: Log-scale to inspect extreme right-tail events
        ax2.hist(series[series > 0], bins=35, color="#D9534F", edgecolor="white", alpha=0.85, log=True)
        p95 = np.percentile(series, 95)
        p99 = np.percentile(series, 99)
        ax2.axvline(p95, color="#F0AD4E", linestyle="--", linewidth=1.5, label=f"95th Pct ({p95:.1f} mm)")
        ax2.axvline(p99, color="#9C27B0", linestyle=":", linewidth=1.8, label=f"99th Pct ({p99:.1f} mm)")
        ax2.set_title("Positive Rainfall (Log Scale & Extremes)", fontsize=11, fontweight="bold")
        ax2.set_xlabel("Rainfall (mm > 0)")
        ax2.set_ylabel("Log Frequency")
        ax2.legend(frameon=True, facecolor="white")
        ax2.grid(True, linestyle="--", alpha=0.4)

        plt.tight_layout()
        out_path = self.output_dir / save_filename
        plt.savefig(out_path, bbox_inches="tight")
        plt.close(fig)
        return out_path

    def plot_rainfall_time_series(
        self,
        df: pd.DataFrame,
        date_col: str = "date",
        rainfall_col: str = "rainfall_mm",
        title: str = "Chronological Daily Precipitation",
        save_filename: str = "rainfall_time_series.png"
    ) -> Optional[Path]:
        """Plots time-series with IMD heavy rainfall alert thresholds."""
        if df.empty or date_col not in df.columns or rainfall_col not in df.columns:
            return None

        df_plot = df.dropna(subset=[date_col, rainfall_col]).copy()
        df_plot["_dt"] = pd.to_datetime(df_plot[date_col])
        df_plot = df_plot.sort_values(by="_dt")

        fig, ax = plt.subplots(figsize=(12, 4.5), dpi=150)
        ax.bar(df_plot["_dt"], df_plot[rainfall_col], color="#2B7A78", width=1.0, alpha=0.8, label="Rainfall (mm)")

        # IMD Thresholds: Heavy (64.5 mm), Very Heavy (115.5 mm)
        ax.axhline(64.5, color="#F0AD4E", linestyle="--", linewidth=1.2, label="IMD Heavy Alert (64.5 mm)")
        ax.axhline(115.5, color="#D9534F", linestyle="-.", linewidth=1.4, label="IMD Very Heavy Alert (115.5 mm)")

        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("Observation Date")
        ax.set_ylabel("Precipitation (mm/day)")
        ax.legend(loc="upper right", frameon=True, facecolor="white")
        ax.grid(True, linestyle="--", alpha=0.4)

        plt.tight_layout()
        out_path = self.output_dir / save_filename
        plt.savefig(out_path, bbox_inches="tight")
        plt.close(fig)
        return out_path

    def plot_river_hydrograph(
        self,
        df: pd.DataFrame,
        timestamp_col: str = "timestamp",
        water_level_col: str = "water_level_m",
        danger_level: Optional[float] = None,
        warning_level: Optional[float] = None,
        station_name: str = "CWC River Gauge",
        save_filename: str = "river_hydrograph.png"
    ) -> Optional[Path]:
        """Plots river hydrograph with danger stage threshold."""
        if df.empty or timestamp_col not in df.columns or water_level_col not in df.columns:
            return None

        df_plot = df.dropna(subset=[timestamp_col, water_level_col]).copy()
        df_plot["_dt"] = pd.to_datetime(df_plot[timestamp_col])
        df_plot = df_plot.sort_values(by="_dt")

        fig, ax = plt.subplots(figsize=(12, 4.5), dpi=150)
        ax.plot(df_plot["_dt"], df_plot[water_level_col], color="#0F4C81", linewidth=1.8, label="Observed Stage (m)")

        if warning_level is not None:
            ax.axhline(warning_level, color="#E67E22", linestyle="--", linewidth=1.5, label=f"Warning Stage ({warning_level} m)")
        if danger_level is not None:
            ax.axhline(danger_level, color="#C0392B", linestyle="-", linewidth=2.0, label=f"Danger Level ({danger_level} m)")

        ax.set_title(f"Hydrograph — {station_name}", fontsize=12, fontweight="bold")
        ax.set_xlabel("Telemetry Timestamp (IST)")
        ax.set_ylabel("Water Elevation (m a.s.l.)")
        ax.legend(loc="upper left", frameon=True, facecolor="white")
        ax.grid(True, linestyle="--", alpha=0.4)

        plt.tight_layout()
        out_path = self.output_dir / save_filename
        plt.savefig(out_path, bbox_inches="tight")
        plt.close(fig)
        return out_path

    def plot_missing_data_profile(
        self,
        df: pd.DataFrame,
        save_filename: str = "missing_data_profile.png"
    ) -> Optional[Path]:
        """Plots column missingness percentages."""
        if df.empty:
            return None

        null_pcts = (df.isna().sum() / len(df) * 100).sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(9, max(3.5, len(null_pcts) * 0.35)), dpi=150)

        colors = ["#2ECC71" if p < 5 else ("#F39C12" if p < 25 else "#E74C3C") for p in null_pcts]
        ax.barh(null_pcts.index, null_pcts.values, color=colors, edgecolor="none", height=0.6)

        for i, v in enumerate(null_pcts.values):
            ax.text(v + 0.5, i, f"{v:.1f}%", va="center", fontsize=9, color="#333333")

        ax.set_xlim(0, max(100, null_pcts.max() + 10))
        ax.set_title("Column Missingness Percentage Profile", fontsize=11, fontweight="bold")
        ax.set_xlabel("Missing Ratio (%)")
        ax.grid(True, linestyle="--", alpha=0.4, axis="x")

        plt.tight_layout()
        out_path = self.output_dir / save_filename
        plt.savefig(out_path, bbox_inches="tight")
        plt.close(fig)
        return out_path
