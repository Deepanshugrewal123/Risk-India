"""
RISK // INDIA — Weather Freshness Engine (Decoupled from Severity)
===================================================================
Calculates meteorological freshness strictly from temporal timestamps.
A severe warning or extreme rainfall observation with stale data remains STALE.
"""

from typing import Optional
from datetime import datetime, timezone
from .schema import WeatherFreshness


class WeatherFreshnessEngine:
    """
    Computes time-based freshness tags:
    - Observations:
      < 1h: OFFICIAL_LIVE
      < 24h: OFFICIAL_RECENT
      >= 24h: STALE
    - Forecasts:
      valid window includes current time: FORECAST_CURRENT
      valid within next 24h: FORECAST_NEAR_TERM
      expired: STALE
    """

    def evaluate_observation_freshness(
        self,
        observed_at_iso: Optional[str],
        now: Optional[datetime] = None
    ) -> str:
        if not observed_at_iso:
            return WeatherFreshness.UNAVAILABLE.value
        try:
            dt = datetime.fromisoformat(observed_at_iso.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)
        except Exception:
            return WeatherFreshness.UNAVAILABLE.value

        current = now or datetime.now(timezone.utc)
        delta_seconds = (current - dt).total_seconds()

        if delta_seconds < 3600:
            return WeatherFreshness.OFFICIAL_LIVE.value
        elif delta_seconds < 86400:
            return WeatherFreshness.OFFICIAL_RECENT.value
        else:
            return WeatherFreshness.STALE.value

    def evaluate_forecast_freshness(
        self,
        valid_from_iso: Optional[str],
        valid_until_iso: Optional[str],
        now: Optional[datetime] = None
    ) -> str:
        if not valid_from_iso or not valid_until_iso:
            return WeatherFreshness.UNAVAILABLE.value
        try:
            dt_from = datetime.fromisoformat(valid_from_iso.replace("Z", "+00:00"))
            dt_until = datetime.fromisoformat(valid_until_iso.replace("Z", "+00:00"))
            current = now or datetime.now(timezone.utc)
            if dt_from.tzinfo is None:
                dt_from = dt_from.replace(tzinfo=timezone.utc)
            if dt_until.tzinfo is None:
                dt_until = dt_until.replace(tzinfo=timezone.utc)
        except Exception:
            return WeatherFreshness.UNAVAILABLE.value

        if dt_until < current:
            return WeatherFreshness.STALE.value
        elif dt_from <= current <= dt_until:
            return WeatherFreshness.FORECAST_CURRENT.value
        elif (dt_from - current).total_seconds() <= 86400:
            return WeatherFreshness.FORECAST_NEAR_TERM.value
        else:
            return WeatherFreshness.FORECAST_NEAR_TERM.value


weather_freshness_engine = WeatherFreshnessEngine()
