"""
RISK // INDIA — Standard Flood-Event Label Schema & Quality Specifications

Defines canonical Pydantic models for authoritative satellite ground-truth labels.
Strictly adheres to project integrity standards:
- Explicit geometry and product provenance
- No invented dates or fabricated event IDs
- Distinction between observed satellite inundation and hydrological proxies
- Formal documentation of satellite observation limits (clouds, revisit cycle)
"""

from typing import Optional, List, Dict, Any, Literal
from datetime import date
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class FloodLabelConfidence(str, Enum):
    """
    Quality and confidence classification of the flood ground truth.
    """
    OBSERVED_SATELLITE = "OBSERVED_SATELLITE"
    HYDROLOGICAL_PROXY_VERIFIED = "HYDROLOGICAL_PROXY_VERIFIED"
    HYDROLOGICAL_PROXY_UNVERIFIED = "HYDROLOGICAL_PROXY_UNVERIFIED"
    NEGATIVE_VERIFIED_PASS = "NEGATIVE_VERIFIED_PASS"
    UNVERIFIED = "UNVERIFIED"


class LocationType(str, Enum):
    """
    Spatial resolution / aggregation type for the location identifier.
    """
    STATION_CATCHMENT = "STATION_CATCHMENT"
    GAUGE_CATCHMENT = "GAUGE_CATCHMENT"
    DISTRICT = "DISTRICT"
    GRID_PIXEL = "GRID_PIXEL"


class GeometrySource(str, Enum):
    """
    Authoritative geospatial source provider.
    """
    ISRO_NRSC_BHUVAN = "ISRO_NRSC_BHUVAN"
    CWC_HYDROLOGY_NETWORK = "CWC_HYDROLOGY_NETWORK"
    MANUAL_GIS_DIGITIZED = "MANUAL_GIS_DIGITIZED"


class FloodEventLabel(BaseModel):
    """
    Canonical standardized flood ground-truth observation record.
    """
    event_id: str = Field(
        ...,
        description="Authoritative event identifier from ISRO/NRSC Bhuvan activation or official bulletin."
    )
    event_date: date = Field(
        ...,
        description="Date of satellite observation or confirmed inundation (YYYY-MM-DD)."
    )
    location_id: str = Field(
        ...,
        description="Identifier of the monitored location (Station ID, Gauge ID, or LGD District Code)."
    )
    location_type: LocationType = Field(
        default=LocationType.GAUGE_CATCHMENT,
        description="Spatial aggregation scale of the location."
    )
    geometry_source: GeometrySource = Field(
        default=GeometrySource.ISRO_NRSC_BHUVAN,
        description="Geospatial agency providing the observation polygons or rasters."
    )
    flood_observed: Literal[0, 1] = Field(
        ...,
        description="Binary indicator: 1 = Inundation confirmed within catchment; 0 = Confirmed clear/dry during valid satellite pass."
    )
    source_product: str = Field(
        ...,
        description="Specific satellite product name (e.g., Sentinel-1A SAR Inundation Map, Bhuvan Flood Hazard Layer)."
    )
    source_url: str = Field(
        ...,
        description="Direct official URL or portal endpoint documenting the acquisition."
    )
    spatial_resolution: str = Field(
        ...,
        description="Spatial resolution of sensor or vector product (e.g., '10m SAR', '30m Multi-spectral', 'District Polygon')."
    )
    confidence: FloodLabelConfidence = Field(
        default=FloodLabelConfidence.OBSERVED_SATELLITE,
        description="Verification level. Labeled strictly as 'Satellite-observed flood inundation', never 'perfect ground truth'."
    )
    inundated_area_sqkm: Optional[float] = Field(
        default=None,
        description="Estimated inundated surface area in square kilometers within the location bounds, if available."
    )
    intersection_fraction: Optional[float] = Field(
        default=None,
        description="Fraction of the catchment area inundated (0.0 to 1.0)."
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional satellite metadata (sensor, orbit, polarization, cloud cover estimate)."
    )

    @field_validator("event_id")
    def validate_event_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("event_id must not be empty or whitespace.")
        return v.strip()

    @field_validator("location_id")
    def validate_location_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("location_id must not be empty or whitespace.")
        return v.strip()


class FloodDatasetQualityReport(BaseModel):
    """
    Comprehensive quality and limitation assessment for an acquired flood label set.
    """
    source_provider: str = "ISRO / NRSC Bhuvan Disaster Services"
    ground_truth_nature: str = "Satellite-observed flood inundation (NOT perfect ground truth)"
    total_events: int = 0
    date_range_start: Optional[date] = None
    date_range_end: Optional[date] = None
    positive_labels_count: int = 0
    negative_labels_count: int = 0
    spatial_coverage_districts: List[str] = Field(default_factory=list)
    sensors_used: List[str] = Field(default_factory=list)
    observation_limitations: List[str] = Field(
        default_factory=lambda: [
            "Optical imagery is obscured by heavy cloud cover during peak monsoon storm events.",
            "Synthetic Aperture Radar (SAR) revisit intervals range between 2 and 6 days, potentially missing short-duration flash crests.",
            "Narrow riverine flood pulses lasting < 24 hours may recede before subsequent orbital passes.",
            "Dense vegetation canopies and urban structures induce radar backscatter attenuation.",
            "Satellite observations register standing surface water at the instant of pass, which may reflect post-peak ponding rather than maximum flood stage."
        ]
    )
    missed_flood_risk_factors: List[str] = Field(
        default_factory=lambda: [
            "Flash floods occurring between satellite overpasses.",
            "Sub-canopy embankment breaches undetected by C-band SAR."
        ]
    )
