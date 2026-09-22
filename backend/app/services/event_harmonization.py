"""
RISK // INDIA — Deterministic Event Harmonization & Negative Label Policy
==========================================================================
Enforces rigorous scientific separation between:
1. OBSERVATION: Raw / normalized sensor telemetry readings at a given gauge and timestamp.
2. EVENT: Spatio-temporal hazard manifestation aggregated across gauge corridors and confirmed by authorities.
3. GROUND_TRUTH: Verified inundation masks (ISRO/NRSC satellite rasters) or official state disaster bulletins.

SCIENTIFIC LABELING PRINCIPLES:
- Only 'CONFIRMED' events may be utilized as positive training labels for empirical ML.
- Heavy rainfall is NEVER converted to a flood label without confirmed inundation.
- River level exceeding danger level is recorded as hydrological danger, NOT confirmed flood,
  unless satellite inundation or official CWC flood bulletin confirms out-of-bank inundation.
- Negative samples require positive proof of non-flood conditions:
  "Adequate telemetry observations during the period AND zero official flood/inundation confirmation."
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import logging

logger = logging.getLogger("event-harmonization")


class EventConfidence:
    CONFIRMED = "CONFIRMED"      # Verified by satellite inundation or official government bulletin
    PROBABLE = "PROBABLE"        # Hydrological thresholds exceeded but awaiting satellite verification
    UNCONFIRMED = "UNCONFIRMED"  # Media report or unverified crowd alert


class LabelType:
    POSITIVE_FLOOD = "POSITIVE_FLOOD"
    NEGATIVE_NON_FLOOD = "NEGATIVE_NON_FLOOD"
    UNCERTAIN_EXCLUDED = "UNCERTAIN_EXCLUDED"


@dataclass
class DisasterEventEntity:
    event_id: str
    basin: str
    state: str
    district: str
    station_ids: List[str]
    start_time: str
    peak_time: Optional[str]
    end_time: Optional[str]
    hazard_type: str = "FLOOD"
    severity: str = "HIGH"  # MODERATE, HIGH, EXTREME
    official_confirmation: bool = True
    ground_truth_source: str = "ISRO Bhuvan Inundation Rasters / CWC Bulletins"
    source_url: str = "https://bhuvan-app1.nrsc.gov.in/disaster/disaster.php"
    confidence: str = EventConfidence.CONFIRMED
    inundation_area_sqkm: Optional[float] = None
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HarmonizedObservationLabel:
    observation_id: str
    station_id: str
    timestamp: str
    basin: str
    label: str  # POSITIVE_FLOOD, NEGATIVE_NON_FLOOD, UNCERTAIN_EXCLUDED
    confidence: str  # CONFIRMED, PROBABLE, UNCONFIRMED
    associated_event_id: Optional[str]
    ground_truth_source: str
    label_methodology: str
    is_valid_ml_sample: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class NegativeSamplePolicy:
    """
    Enforces scientifically defensible negative (non-flood) labeling.
    Prevents false negatives caused by reporting gaps.
    """
    @staticmethod
    def evaluate_negative_sample(
        has_adequate_telemetry: bool,
        water_level_below_warning: bool,
        official_inundation_absent: bool,
        station_id: str,
        timestamp: str
    ) -> HarmonizedObservationLabel:
        """
        Rule: An observation is labeled NEGATIVE_NON_FLOOD IF AND ONLY IF:
        1. Gauge had adequate continuous telemetry during the observation window.
        2. Water level remained safely below warning level.
        3. Official ground truth confirmed NO inundation occurred in the gauge catchment.
        """
        if not has_adequate_telemetry:
            return HarmonizedObservationLabel(
                observation_id=f"{station_id}@{timestamp}",
                station_id=station_id,
                timestamp=timestamp,
                basin="",
                label=LabelType.UNCERTAIN_EXCLUDED,
                confidence=EventConfidence.UNCONFIRMED,
                associated_event_id=None,
                ground_truth_source="NONE",
                label_methodology="EXCLUDED: Telemetry gaps during observation window preclude definitive negative label.",
                is_valid_ml_sample=False
            )

        if water_level_below_warning and official_inundation_absent:
            return HarmonizedObservationLabel(
                observation_id=f"{station_id}@{timestamp}",
                station_id=station_id,
                timestamp=timestamp,
                basin="",
                label=LabelType.NEGATIVE_NON_FLOOD,
                confidence=EventConfidence.CONFIRMED,
                associated_event_id=None,
                ground_truth_source="CWC Daily Bulletin + ISRO Bhuvan Non-Inundated Baseline",
                label_methodology="CONFIRMED_NEGATIVE: Continuous telemetry verified water level below warning level with zero satellite inundation.",
                is_valid_ml_sample=True
            )

        # Ambiguous case: elevated river level but no confirmed inundation
        return HarmonizedObservationLabel(
            observation_id=f"{station_id}@{timestamp}",
            station_id=station_id,
            timestamp=timestamp,
            basin="",
            label=LabelType.UNCERTAIN_EXCLUDED,
            confidence=EventConfidence.PROBABLE,
            associated_event_id=None,
            ground_truth_source="CWC Gauge Alert",
            label_methodology="EXCLUDED: High river level without confirmed satellite inundation raster cannot be definitively labeled.",
            is_valid_ml_sample=False
        )


class EventHarmonizer:
    """
    Harmonizes independent flood events across river basins.
    """
    def __init__(self):
        self._events: Dict[str, DisasterEventEntity] = {}
        self._register_canonical_events()

    def _register_canonical_events(self):
        # Canonical verified flood events from Assam empirical baseline
        self._events["EV-AS-2022-01"] = DisasterEventEntity(
            event_id="EV-AS-2022-01",
            basin="brahmaputra",
            state="Assam",
            district="Kamrup",
            station_ids=["CWC-BP-003"],
            start_time="2022-05-18T00:00:00+00:00",
            peak_time="2022-05-24T12:00:00+00:00",
            end_time="2022-05-28T00:00:00+00:00",
            hazard_type="FLOOD",
            severity="EXTREME",
            official_confirmation=True,
            ground_truth_source="ISRO Bhuvan Satellite Inundation Raster + ASDMA Bulletin",
            confidence=EventConfidence.CONFIRMED,
            inundation_area_sqkm=450.0,
            notes="Assam pre-monsoon severe deluge wave 1."
        )
        self._events["EV-AS-2024-01"] = DisasterEventEntity(
            event_id="EV-AS-2024-01",
            basin="brahmaputra",
            state="Assam",
            district="Darrang",
            station_ids=["CWC-BP-002"],
            start_time="2024-07-01T00:00:00+00:00",
            peak_time="2024-07-04T18:00:00+00:00",
            end_time="2024-07-08T00:00:00+00:00",
            hazard_type="FLOOD",
            severity="HIGH",
            official_confirmation=True,
            ground_truth_source="ISRO Bhuvan Satellite Inundation Raster + CWC Bulletin",
            confidence=EventConfidence.CONFIRMED,
            inundation_area_sqkm=320.0,
            notes="Assam monsoon flood wave 2."
        )

        # Historical benchmark flood events for Godavari & Mahanadi (Cataloged for benchmark verification only)
        self._events["EV-GD-2022-01"] = DisasterEventEntity(
            event_id="EV-GD-2022-01",
            basin="godavari",
            state="Telangana",
            district="Bhadradri Kothagudem",
            station_ids=["CWC-GD-001", "CWC-GD-003"],
            start_time="2022-07-12T00:00:00+00:00",
            peak_time="2022-07-16T14:00:00+00:00",
            end_time="2022-07-20T00:00:00+00:00",
            hazard_type="FLOOD",
            severity="EXTREME",
            official_confirmation=True,
            ground_truth_source="CWC Godavari Flood Bulletin (71.3 ft crest at Bhadrachalam) + NRSC",
            confidence=EventConfidence.CONFIRMED,
            notes="Historic Godavari flood wave; second highest recorded since 1986."
        )
        self._events["EV-MH-2020-01"] = DisasterEventEntity(
            event_id="EV-MH-2020-01",
            basin="mahanadi",
            state="Odisha",
            district="Cuttack",
            station_ids=["CWC-MH-001", "CWC-MH-002"],
            start_time="2020-08-27T00:00:00+00:00",
            peak_time="2020-08-30T10:00:00+00:00",
            end_time="2020-09-03T00:00:00+00:00",
            hazard_type="FLOOD",
            severity="HIGH",
            official_confirmation=True,
            ground_truth_source="SRC Odisha Official Flood Report + CWC Hirakud Discharge",
            confidence=EventConfidence.CONFIRMED,
            notes="Mahanadi basin high flood wave; peak discharge 10.2 lakh cusec at Mundali/Naraj."
        )

    def get_event(self, event_id: str) -> Optional[DisasterEventEntity]:
        return self._events.get(event_id)

    def list_events(self, basin: Optional[str] = None, confirmed_only: bool = False) -> List[Dict[str, Any]]:
        evs = list(self._events.values())
        if basin:
            evs = [e for e in evs if e.basin.lower() == basin.lower().strip()]
        if confirmed_only:
            evs = [e for e in evs if e.confidence == EventConfidence.CONFIRMED]
        return [e.to_dict() for e in evs]


event_harmonizer = EventHarmonizer()
