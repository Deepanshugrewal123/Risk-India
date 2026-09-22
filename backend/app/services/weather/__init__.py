"""
RISK // INDIA — National Weather Intelligence, Forecast Ingestion & Multi-Hazard Early Warning Package
======================================================================================================
"""

from .schema import (
    DataClassification,
    ForecastHorizon,
    ForecastUncertainty,
    WeatherFreshness,
    QualityRejectionReason,
    WeatherUnitConversionRecord,
    CanonicalWeatherObservation,
    CanonicalWeatherForecast,
    WeatherWarning,
    generate_weather_id
)
from .normalizer import weather_unit_normalizer, WeatherUnitNormalizer
from .geographic_mapper import weather_geographic_mapper, WeatherGeographicMapper
from .quality_engine import weather_quality_engine, WeatherQualityEngine
from .temporal_manager import weather_temporal_manager, WeatherTemporalManager
from .provider_client import weather_provider_client, WeatherProviderClient
from .freshness_engine import weather_freshness_engine, WeatherFreshnessEngine
from .evidence_engine import weather_evidence_engine, WeatherEvidenceEngine
from .weather_service import national_weather_service, NationalWeatherIntelligenceService

__all__ = [
    "DataClassification",
    "ForecastHorizon",
    "ForecastUncertainty",
    "WeatherFreshness",
    "QualityRejectionReason",
    "WeatherUnitConversionRecord",
    "CanonicalWeatherObservation",
    "CanonicalWeatherForecast",
    "WeatherWarning",
    "generate_weather_id",
    "weather_unit_normalizer",
    "WeatherUnitNormalizer",
    "weather_geographic_mapper",
    "WeatherGeographicMapper",
    "weather_quality_engine",
    "WeatherQualityEngine",
    "weather_temporal_manager",
    "WeatherTemporalManager",
    "weather_provider_client",
    "WeatherProviderClient",
    "weather_freshness_engine",
    "WeatherFreshnessEngine",
    "weather_evidence_engine",
    "WeatherEvidenceEngine",
    "national_weather_service",
    "NationalWeatherIntelligenceService"
]
