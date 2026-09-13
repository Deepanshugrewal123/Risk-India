"""
RISK // INDIA — Flood Event Ground-Truth Label Architecture

Provides standard schemas, ISRO/NRSC Bhuvan satellite ingestion loaders,
and spatial labeling intersection utilities.
"""

from ml.data.labels.label_schema import (
    FloodEventLabel,
    FloodLabelConfidence,
    LocationType,
    GeometrySource,
    FloodDatasetQualityReport
)
from ml.data.labels.isro_flood_loader import ISROFloodInundationLoader
from ml.data.labels.spatial_labeling import SpatialLabeler

__all__ = [
    "FloodEventLabel",
    "FloodLabelConfidence",
    "LocationType",
    "GeometrySource",
    "FloodDatasetQualityReport",
    "ISROFloodInundationLoader",
    "SpatialLabeler"
]
