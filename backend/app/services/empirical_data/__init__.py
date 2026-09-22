"""
RISK // INDIA — National Empirical Disaster Data Foundation
===========================================================
Package exports for the empirical flood data acquisition, normalization,
quality evaluation, and scientific model promotion layer.
"""

from .base import (
    SourceProvider,
    QualityStatus,
    ProvenanceStatus,
    DataFreshness,
    ScientificState,
    EventCategory,
    PromotionStatus,
    PRIORITY_BASINS,
    CANONICAL_BASIN_NAMES,
    REJECTION_REASON_MISSING_CORROBORATION,
    REJECTION_REASON_OUT_OF_BOUNDS_COORDINATES,
    REJECTION_REASON_FUTURE_TIMESTAMP,
    REJECTION_REASON_TEMPORAL_LEAKAGE,
    REJECTION_REASON_UNVERIFIED_PROVENANCE,
    REJECTION_REASON_SYNTHETIC_DATA_PROHIBITED,
    REJECTION_REASON_INVALID_UNITS,
    REJECTION_REASON_INSUFFICIENT_OBSERVATIONS,
    REJECTION_REASON_DUPLICATE_RECORD,
    REJECTION_REASON_MISSING_FEATURES,
    REJECTION_REASON_SPATIAL_LEAKAGE,
    REJECTION_REASON_UNAPPROVED_MODEL,
    REJECTION_REASON_NON_ASSAM_ML_PROHIBITED
)

from .schema import (
    EmpiricalObservationRecord,
    generate_observation_id
)

from .provenance import (
    AUTHORITATIVE_PROVIDERS_METADATA,
    get_provider_metadata,
    check_provider_access
)

from .validators import (
    validate_coordinates,
    validate_physical_measurements,
    validate_timestamp,
    validate_temporal_consistency,
    INDIAN_BOUNDING_BOX,
    PHYSICAL_MEASUREMENT_BOUNDS
)

from .normalization import (
    normalize_state_name,
    normalize_basin_name,
    normalize_coordinates,
    normalize_timestamp,
    normalize_unit,
    normalize_observation_record
)

from .basin_registry import (
    CalibratedRiverGauge,
    empirical_basin_registry
)

from .event_construction import (
    FloodEvent,
    flood_event_constructor,
    ASSAM_AUDITED_FLOOD_EVENTS
)

from .event_corroboration import (
    CorroborationStatus,
    CorroboratedFloodEvent,
    EventCorroborationService,
    event_corroboration_service
)

from .temporal_alignment import (
    TemporalAlignmentEngine,
    temporal_alignment_engine,
    CANONICAL_13_FEATURES
)

from .basin_readiness import (
    BasinReadinessEvaluator,
    basin_readiness_evaluator
)

from .quality import (
    QualityGateResult,
    DataQualityGateEvaluator,
    data_quality_evaluator
)

from .acquisition import (
    BaseProviderAdapter,
    AssamEmpiricalAdapter,
    CWCProviderAdapter,
    IMDProviderAdapter,
    GaugeTelemetryIngestionService,
    RainfallTelemetryIngestionService,
    FloodEventIngestionService,
    EmpiricalDataAcquisitionService,
    empirical_acquisition_service
)

from .promotion_gate import (
    ScientificBasinPromotionGate,
    scientific_basin_promotion_gate
)

from .manifest import (
    generate_national_flood_manifest,
    NATIONAL_DATA_MANIFEST_V1
)

__all__ = [
    "SourceProvider",
    "QualityStatus",
    "ProvenanceStatus",
    "DataFreshness",
    "ScientificState",
    "EventCategory",
    "PromotionStatus",
    "PRIORITY_BASINS",
    "CANONICAL_BASIN_NAMES",
    "REJECTION_REASON_MISSING_CORROBORATION",
    "REJECTION_REASON_OUT_OF_BOUNDS_COORDINATES",
    "REJECTION_REASON_FUTURE_TIMESTAMP",
    "REJECTION_REASON_TEMPORAL_LEAKAGE",
    "REJECTION_REASON_UNVERIFIED_PROVENANCE",
    "REJECTION_REASON_SYNTHETIC_DATA_PROHIBITED",
    "REJECTION_REASON_INVALID_UNITS",
    "REJECTION_REASON_INSUFFICIENT_OBSERVATIONS",
    "REJECTION_REASON_DUPLICATE_RECORD",
    "REJECTION_REASON_MISSING_FEATURES",
    "REJECTION_REASON_SPATIAL_LEAKAGE",
    "REJECTION_REASON_UNAPPROVED_MODEL",
    "REJECTION_REASON_NON_ASSAM_ML_PROHIBITED",
    "EmpiricalObservationRecord",
    "generate_observation_id",
    "AUTHORITATIVE_PROVIDERS_METADATA",
    "get_provider_metadata",
    "check_provider_access",
    "validate_coordinates",
    "validate_physical_measurements",
    "validate_timestamp",
    "validate_temporal_consistency",
    "INDIAN_BOUNDING_BOX",
    "PHYSICAL_MEASUREMENT_BOUNDS",
    "normalize_state_name",
    "normalize_basin_name",
    "normalize_coordinates",
    "normalize_timestamp",
    "normalize_unit",
    "normalize_observation_record",
    "CalibratedRiverGauge",
    "empirical_basin_registry",
    "FloodEvent",
    "flood_event_constructor",
    "ASSAM_AUDITED_FLOOD_EVENTS",
    "CorroborationStatus",
    "CorroboratedFloodEvent",
    "EventCorroborationService",
    "event_corroboration_service",
    "TemporalAlignmentEngine",
    "temporal_alignment_engine",
    "CANONICAL_13_FEATURES",
    "BasinReadinessEvaluator",
    "basin_readiness_evaluator",
    "QualityGateResult",
    "DataQualityGateEvaluator",
    "data_quality_evaluator",
    "BaseProviderAdapter",
    "AssamEmpiricalAdapter",
    "CWCProviderAdapter",
    "IMDProviderAdapter",
    "GaugeTelemetryIngestionService",
    "RainfallTelemetryIngestionService",
    "FloodEventIngestionService",
    "EmpiricalDataAcquisitionService",
    "empirical_acquisition_service",
    "ScientificBasinPromotionGate",
    "scientific_basin_promotion_gate",
    "generate_national_flood_manifest",
    "NATIONAL_DATA_MANIFEST_V1"
]
