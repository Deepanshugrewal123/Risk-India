"""
RISK // INDIA — Mathematical Weather SI Unit Normalizer
========================================================
Standardizes temperatures, precipitation, wind velocities, atmospheric pressures,
and optical visibilities to canonical SI / national meteorological standards.
Unknown units are strictly rejected without guessing.
"""

from typing import Tuple
from .schema import QualityRejectionReason, WeatherUnitConversionRecord


class WeatherUnitNormalizer:
    """
    Deterministic SI converter for meteorological variables:
    - Temperature: Celsius (°C)
    - Rainfall: millimeters (mm)
    - Wind: meters per second (m/s)
    - Pressure: hectopascals (hPa)
    - Visibility: kilometers (km)
    """

    SUPPORTED_TEMP_UNITS = {
        "c": (1.0, 0.0, "C", "identity (C -> C)"),
        "celsius": (1.0, 0.0, "C", "identity (C -> C)"),
        "degc": (1.0, 0.0, "C", "identity (C -> C)"),
        "f": (5.0 / 9.0, -32.0 * 5.0 / 9.0, "C", "(val - 32) * 5/9 (F -> C)"),
        "fahrenheit": (5.0 / 9.0, -32.0 * 5.0 / 9.0, "C", "(val - 32) * 5/9 (F -> C)"),
        "degf": (5.0 / 9.0, -32.0 * 5.0 / 9.0, "C", "(val - 32) * 5/9 (F -> C)"),
        "k": (1.0, -273.15, "C", "val - 273.15 (K -> C)"),
        "kelvin": (1.0, -273.15, "C", "val - 273.15 (K -> C)")
    }

    SUPPORTED_RAIN_UNITS = {
        "mm": (1.0, "mm", "identity (mm -> mm)"),
        "millimeter": (1.0, "mm", "identity (mm -> mm)"),
        "millimeters": (1.0, "mm", "identity (mm -> mm)"),
        "cm": (10.0, "mm", "val * 10.0 (cm -> mm)"),
        "centimeter": (10.0, "mm", "val * 10.0 (cm -> mm)"),
        "in": (25.4, "mm", "val * 25.4 (in -> mm)"),
        "inch": (25.4, "mm", "val * 25.4 (in -> mm)"),
        "inches": (25.4, "mm", "val * 25.4 (in -> mm)")
    }

    SUPPORTED_WIND_UNITS = {
        "m/s": (1.0, "m/s", "identity (m/s -> m/s)"),
        "mps": (1.0, "m/s", "identity (m/s -> m/s)"),
        "meter_per_second": (1.0, "m/s", "identity (m/s -> m/s)"),
        "km/h": (1.0 / 3.6, "m/s", "val / 3.6 (km/h -> m/s)"),
        "kmh": (1.0 / 3.6, "m/s", "val / 3.6 (km/h -> m/s)"),
        "kph": (1.0 / 3.6, "m/s", "val / 3.6 (km/h -> m/s)"),
        "knots": (0.514444, "m/s", "val * 0.514444 (knots -> m/s)"),
        "kt": (0.514444, "m/s", "val * 0.514444 (knots -> m/s)"),
        "mph": (0.44704, "m/s", "val * 0.44704 (mph -> m/s)")
    }

    SUPPORTED_PRESSURE_UNITS = {
        "hpa": (1.0, "hPa", "identity (hPa -> hPa)"),
        "hectopascal": (1.0, "hPa", "identity (hPa -> hPa)"),
        "mbar": (1.0, "hPa", "identity (mbar -> hPa)"),
        "millibar": (1.0, "hPa", "identity (mbar -> hPa)"),
        "atm": (1013.25, "hPa", "val * 1013.25 (atm -> hPa)"),
        "mmhg": (1.33322, "hPa", "val * 1.33322 (mmHg -> hPa)"),
        "inhg": (33.8639, "hPa", "val * 33.8639 (inHg -> hPa)")
    }

    SUPPORTED_VISIBILITY_UNITS = {
        "km": (1.0, "km", "identity (km -> km)"),
        "kilometer": (1.0, "km", "identity (km -> km)"),
        "kilometers": (1.0, "km", "identity (km -> km)"),
        "m": (0.001, "km", "val / 1000.0 (m -> km)"),
        "meter": (0.001, "km", "val / 1000.0 (m -> km)"),
        "meters": (0.001, "km", "val / 1000.0 (m -> km)"),
        "miles": (1.60934, "km", "val * 1.60934 (miles -> km)"),
        "mi": (1.60934, "km", "val * 1.60934 (miles -> km)")
    }

    def normalize(self, variable_name: str, raw_value: float, unit_str: str) -> WeatherUnitConversionRecord:
        """
        Normalizes a meteorological measurement to canonical SI unit.
        Raises ValueError with UNKNOWN_UNIT rejection reason if unit is unrecognized.
        """
        if not unit_str or not isinstance(unit_str, str):
            raise ValueError(QualityRejectionReason.UNKNOWN_UNIT.value)

        u = unit_str.strip().lower().replace("°", "").replace(" ", "_")
        v = variable_name.strip().lower()

        if "temp" in v or v == "dew_point":
            if u not in self.SUPPORTED_TEMP_UNITS:
                raise ValueError(f"{QualityRejectionReason.UNKNOWN_UNIT.value}: Unknown temperature unit '{unit_str}'")
            factor, offset, norm_u, rule = self.SUPPORTED_TEMP_UNITS[u]
            norm_val = round((float(raw_value) * factor) + offset, 2)
            return WeatherUnitConversionRecord(float(raw_value), unit_str, norm_val, norm_u, rule)

        elif "rain" in v or "precip" in v:
            if u not in self.SUPPORTED_RAIN_UNITS:
                raise ValueError(f"{QualityRejectionReason.UNKNOWN_UNIT.value}: Unknown rainfall unit '{unit_str}'")
            factor, norm_u, rule = self.SUPPORTED_RAIN_UNITS[u]
            norm_val = round(float(raw_value) * factor, 2)
            return WeatherUnitConversionRecord(float(raw_value), unit_str, norm_val, norm_u, rule)

        elif "wind" in v:
            if u not in self.SUPPORTED_WIND_UNITS:
                raise ValueError(f"{QualityRejectionReason.UNKNOWN_UNIT.value}: Unknown wind unit '{unit_str}'")
            factor, norm_u, rule = self.SUPPORTED_WIND_UNITS[u]
            norm_val = round(float(raw_value) * factor, 2)
            return WeatherUnitConversionRecord(float(raw_value), unit_str, norm_val, norm_u, rule)

        elif "pressure" in v:
            if u not in self.SUPPORTED_PRESSURE_UNITS:
                raise ValueError(f"{QualityRejectionReason.UNKNOWN_UNIT.value}: Unknown pressure unit '{unit_str}'")
            factor, norm_u, rule = self.SUPPORTED_PRESSURE_UNITS[u]
            norm_val = round(float(raw_value) * factor, 2)
            return WeatherUnitConversionRecord(float(raw_value), unit_str, norm_val, norm_u, rule)

        elif "visibility" in v:
            if u not in self.SUPPORTED_VISIBILITY_UNITS:
                raise ValueError(f"{QualityRejectionReason.UNKNOWN_UNIT.value}: Unknown visibility unit '{unit_str}'")
            factor, norm_u, rule = self.SUPPORTED_VISIBILITY_UNITS[u]
            norm_val = round(float(raw_value) * factor, 2)
            return WeatherUnitConversionRecord(float(raw_value), unit_str, norm_val, norm_u, rule)

        else:
            raise ValueError(f"{QualityRejectionReason.UNSUPPORTED_VARIABLE.value}: Unsupported weather variable '{variable_name}'")


weather_unit_normalizer = WeatherUnitNormalizer()
