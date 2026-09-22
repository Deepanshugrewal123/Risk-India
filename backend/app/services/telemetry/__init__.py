"""
RISK // INDIA — Dynamic Catchment Telemetry Stream & Hydrological Sensor Ingestion
==================================================================================
Package exports for the production-grade empirical telemetry subsystem.
"""

from .schema import (
    VariableType,
    ObservationQualityStatus,
    DataFreshness,
    GaugeStatus,
    QualityRejectionReason,
    CanonicalGauge,
    UnitConversionRecord,
    HydrologicalObservation,
    TelemetryIngestionBatch,
    generate_observation_id
)
from .gauge_registry import catchment_gauge_registry, CatchmentGaugeRegistry
from .unit_normalizer import unit_normalization_engine, UnitNormalizationEngine
from .quality_engine import telemetry_quality_engine, TelemetryQualityEngine
from .temporal_manager import temporal_telemetry_manager, TemporalTelemetryManager
from .provider_client import hydrological_provider_client, HydrologicalProviderClient
from .telemetry_service import dynamic_telemetry_service, DynamicCatchmentTelemetryService

__all__ = [
    "VariableType",
    "ObservationQualityStatus",
    "DataFreshness",
    "GaugeStatus",
    "QualityRejectionReason",
    "CanonicalGauge",
    "UnitConversionRecord",
    "HydrologicalObservation",
    "TelemetryIngestionBatch",
    "generate_observation_id",
    "catchment_gauge_registry",
    "CatchmentGaugeRegistry",
    "unit_normalization_engine",
    "UnitNormalizationEngine",
    "telemetry_quality_engine",
    "TelemetryQualityEngine",
    "temporal_telemetry_manager",
    "TemporalTelemetryManager",
    "hydrological_provider_client",
    "HydrologicalProviderClient",
    "dynamic_telemetry_service",
    "DynamicCatchmentTelemetryService"
]
