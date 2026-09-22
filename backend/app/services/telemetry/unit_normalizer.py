"""
RISK // INDIA — Mathematical Hydrological Unit Normalizer
==========================================================
Deterministic unit conversions for river stage, precipitation, and discharge.
Rejects unsupported or ambiguous units strictly (no guessing allowed).
"""

from typing import Tuple
from .schema import VariableType, QualityRejectionReason, UnitConversionRecord


class UnitNormalizationEngine:
    """
    Standardizes measurement units to national canonical scientific standards:
    - Water Level: meters (m) relative to MSL or gauge datum
    - Rainfall: millimeters (mm)
    - Discharge: cubic meters per second (m3_s / cumec)
    """

    SUPPORTED_LEVEL_UNITS = {
        "m": (1.0, "m", "val * 1.0 (m -> m)"),
        "meter": (1.0, "m", "val * 1.0 (m -> m)"),
        "meters": (1.0, "m", "val * 1.0 (m -> m)"),
        "ft": (0.3048, "m", "val * 0.3048 (ft -> m)"),
        "feet": (0.3048, "m", "val * 0.3048 (ft -> m)"),
        "foot": (0.3048, "m", "val * 0.3048 (ft -> m)"),
        "cm": (0.01, "m", "val * 0.01 (cm -> m)"),
        "centimeter": (0.01, "m", "val * 0.01 (cm -> m)"),
        "centimeters": (0.01, "m", "val * 0.01 (cm -> m)")
    }

    SUPPORTED_RAIN_UNITS = {
        "mm": (1.0, "mm", "val * 1.0 (mm -> mm)"),
        "millimeter": (1.0, "mm", "val * 1.0 (mm -> mm)"),
        "millimeters": (1.0, "mm", "val * 1.0 (mm -> mm)"),
        "cm": (10.0, "mm", "val * 10.0 (cm -> mm)"),
        "centimeter": (10.0, "mm", "val * 10.0 (cm -> mm)"),
        "centimeters": (10.0, "mm", "val * 10.0 (cm -> mm)"),
        "in": (25.4, "mm", "val * 25.4 (in -> mm)"),
        "inch": (25.4, "mm", "val * 25.4 (in -> mm)"),
        "inches": (25.4, "mm", "val * 25.4 (in -> mm)")
    }

    SUPPORTED_DISCHARGE_UNITS = {
        "cumec": (1.0, "m3_s", "val * 1.0 (cumec -> m3_s)"),
        "m3/s": (1.0, "m3_s", "val * 1.0 (m3/s -> m3_s)"),
        "m^3/s": (1.0, "m3_s", "val * 1.0 (m^3/s -> m3_s)"),
        "m3_s": (1.0, "m3_s", "val * 1.0 (m3_s -> m3_s)"),
        "cubic_meters_per_second": (1.0, "m3_s", "val * 1.0 (m3/s -> m3_s)"),
        "cusec": (0.0283168, "m3_s", "val * 0.0283168 (cusec -> m3_s)"),
        "ft3/s": (0.0283168, "m3_s", "val * 0.0283168 (cusec -> m3_s)"),
        "ft^3/s": (0.0283168, "m3_s", "val * 0.0283168 (cusec -> m3_s)"),
        "cfs": (0.0283168, "m3_s", "val * 0.0283168 (cfs -> m3_s)"),
        "cubic_feet_per_second": (0.0283168, "m3_s", "val * 0.0283168 (cfs -> m3_s)")
    }

    @classmethod
    def normalize(cls, variable_type: str, raw_value: float, unit_str: str) -> UnitConversionRecord:
        """
        Applies deterministic conversion.
        Raises ValueError with UNKNOWN_UNIT rejection reason if unit is unrecognized.
        """
        if not unit_str or not isinstance(unit_str, str):
            raise ValueError(QualityRejectionReason.UNKNOWN_UNIT.value)

        u_clean = unit_str.strip().lower().replace(" ", "_")
        v_clean = variable_type.strip().upper()

        if v_clean == VariableType.WATER_LEVEL.value:
            lookup = cls.SUPPORTED_LEVEL_UNITS
            precision = 4
        elif v_clean == VariableType.RAINFALL.value:
            lookup = cls.SUPPORTED_RAIN_UNITS
            precision = 2
        elif v_clean == VariableType.DISCHARGE.value:
            lookup = cls.SUPPORTED_DISCHARGE_UNITS
            precision = 4
        else:
            raise ValueError(QualityRejectionReason.UNSUPPORTED_VARIABLE.value)

        if u_clean not in lookup:
            raise ValueError(f"{QualityRejectionReason.UNKNOWN_UNIT.value}: Unsupported unit '{unit_str}' for {variable_type}")

        factor, norm_unit, rule = lookup[u_clean]
        norm_val = round(float(raw_value) * factor, precision)

        return UnitConversionRecord(
            original_value=float(raw_value),
            original_unit=unit_str,
            normalized_value=norm_val,
            normalized_unit=norm_unit,
            conversion_rule=rule
        )


unit_normalization_engine = UnitNormalizationEngine()
