"""
RISK // INDIA — Cascading / Secondary / Systemic Risk Intelligence Engine
==========================================================================
Evaluates scientifically grounded causal and consequence chains:
    Primary Hazard -> Environmental/Physical Change -> Secondary Hazard -> Tertiary Consequences

Scientific Guardrails & Verification Guarantees:
1. Strict distinction between:
   - Established physical relationship (theoretical/empirical physics)
   - Local observed evidence (real-time telemetry from IMD, CWC, NRSC, etc.)
   - Conditional secondary risk (secondary hazard contingent on terrain/soil/vulnerability)
   - Actual predictive forecast (only when an authoritative numerical model supports it)
2. Zero numeric pseudo-probabilities (no fabricated "78% landslide risk").
3. Honest evidence postures: LIVE_EVIDENCE, RECENT_EVIDENCE, FORECAST_AVAILABLE, BASELINE_ONLY, LIMITED_EVIDENCE, DATA_UNAVAILABLE.
4. Earthquake non-prediction invariant: Physical structural consequences only; temporal prediction strictly prohibited.
5. Assam ML model boundary: ML predictions strictly scoped to Assam flood; cascading chains are physical risk evaluations.
6. Zero synthetic data fabrication: synthetic_records = 0.
"""

from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone

from app.services.national_risk.regional_baseline import regional_baseline_engine, SUPPORTED_HAZARDS
from app.services.future_risk.forecast_contracts import (
    assemble_region_forecast_dataset,
    ForecastEnvironmentDataset,
    InputAvailabilityStatus
)


class EvidencePosture(str, Enum):
    """Authoritative evidence states for cascading risk relationships."""
    LIVE_EVIDENCE = "LIVE_EVIDENCE"               # Active telemetry indicates threshold reached
    RECENT_EVIDENCE = "RECENT_EVIDENCE"           # Recent observation confirms contributing condition
    FORECAST_AVAILABLE = "FORECAST_AVAILABLE"     # Official numerical weather prediction indicates threshold
    BASELINE_ONLY = "BASELINE_ONLY"               # Known physical relationship / historical baseline, no active trigger
    LIMITED_EVIDENCE = "LIMITED_EVIDENCE"         # Sparse telemetry in basin / region
    DATA_UNAVAILABLE = "DATA_UNAVAILABLE"         # Uninstrumented or offline telemetry


class RelationshipClassification(str, Enum):
    """Scientific classification of the causal link."""
    ESTABLISHED_PHYSICAL_RELATIONSHIP = "ESTABLISHED_PHYSICAL_RELATIONSHIP"
    LOCAL_OBSERVED_EVIDENCE = "LOCAL_OBSERVED_EVIDENCE"
    CONDITIONAL_SECONDARY_RISK = "CONDITIONAL_SECONDARY_RISK"
    PREDICTIVE_FORECAST = "PREDICTIVE_FORECAST"


@dataclass
class CascadingStage:
    """Individual node in the cascading risk consequence chain."""
    stage_order: int
    stage_type: str                                # PRIMARY_HAZARD, PHYSICAL_CHANGE, SECONDARY_HAZARD, TERTIARY_CONSEQUENCE
    title: str
    description: str
    scientific_classification: RelationshipClassification
    evidence_posture: EvidencePosture
    supporting_evidence: List[str] = field(default_factory=list)
    conditions_for_escalation: List[str] = field(default_factory=list)
    unmonitored_or_unknown: List[str] = field(default_factory=list)
    field_warning_signs: List[str] = field(default_factory=list)
    defensive_actions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stage_order": self.stage_order,
            "stage_type": self.stage_type,
            "title": self.title,
            "description": self.description,
            "scientific_classification": self.scientific_classification.value,
            "evidence_posture": self.evidence_posture.value,
            "supporting_evidence": self.supporting_evidence,
            "conditions_for_escalation": self.conditions_for_escalation,
            "unmonitored_or_unknown": self.unmonitored_or_unknown,
            "field_warning_signs": self.field_warning_signs,
            "defensive_actions": self.defensive_actions
        }


@dataclass
class CascadingRiskChain:
    """Complete causal consequence chain for a primary hazard."""
    hazard: str
    title: str
    primary_hazard_summary: str
    environmental_change_summary: str
    secondary_hazard_summary: str
    tertiary_consequences_summary: str
    overall_evidence_posture: EvidencePosture
    stages: List[CascadingStage]
    scientific_rationale: str
    earthquake_non_prediction_notice: Optional[str] = None
    terrain_sensitivity_note: Optional[str] = None
    synthetic_records: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hazard": self.hazard,
            "title": self.title,
            "primary_hazard_summary": self.primary_hazard_summary,
            "environmental_change_summary": self.environmental_change_summary,
            "secondary_hazard_summary": self.secondary_hazard_summary,
            "tertiary_consequences_summary": self.tertiary_consequences_summary,
            "overall_evidence_posture": self.overall_evidence_posture.value,
            "stages": [s.to_dict() for s in self.stages],
            "scientific_rationale": self.scientific_rationale,
            "earthquake_non_prediction_notice": self.earthquake_non_prediction_notice,
            "terrain_sensitivity_note": self.terrain_sensitivity_note,
            "synthetic_records": self.synthetic_records
        }


@dataclass
class CascadingRiskAssessment:
    """Full regional cascading risk evaluation."""
    region_id: str
    region_name: str
    region_type: str
    primary_hazard: str
    evaluated_at: str
    evidence_posture: EvidencePosture
    chains: List[CascadingRiskChain]
    context_indicators: Dict[str, Any]
    synthetic_records: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "region": {
                "id": self.region_id,
                "name": self.region_name,
                "type": self.region_type
            },
            "primary_hazard": self.primary_hazard,
            "evaluated_at": self.evaluated_at,
            "evidence_posture": self.evidence_posture.value,
            "chains": [c.to_dict() for c in self.chains],
            "context_indicators": self.context_indicators,
            "synthetic_records": self.synthetic_records
        }


class CascadingRiskEngine:
    """
    Authoritative engine for evaluating cascading and secondary hazard risks.
    Combines established geomechanical/hydrometeorological physical relationships
    with real-time regional environmental telemetry.
    """

    def evaluate_region_cascading_risk(
        self,
        state_identifier: str,
        hazard: Optional[str] = None
    ) -> Optional[CascadingRiskAssessment]:
        """
        Evaluates cascading risks for a specific state/UT, incorporating environmental
        variables (terrain slope vulnerability, hydrological telemetry, weather forecast).
        """
        profile = regional_baseline_engine.get_state_profile(state_identifier)
        if not profile:
            return None

        dataset = assemble_region_forecast_dataset(profile.name)
        active_hazard = hazard.upper().strip() if hazard else profile.primary_hazard
        if active_hazard not in SUPPORTED_HAZARDS:
            active_hazard = "FLOOD"

        chain = self._build_hazard_chain(active_hazard, profile, dataset)
        overall_posture = chain.overall_evidence_posture

        context_indicators = {
            "terrain_slope_vulnerability": dataset.environment.terrain_slope_vulnerability if dataset else "UNAVAILABLE",
            "basin_condition": dataset.hydrology.basin_condition if dataset else "NORMAL",
            "river_level_trend": dataset.hydrology.river_level_trend if dataset else "UNAVAILABLE",
            "accumulated_rainfall_72h_mm": dataset.hydrology.accumulated_rainfall_72h_mm if dataset else None,
            "coastal_exposure": dataset.cyclone.coastal_exposure if dataset else "NONE",
            "active_cyclone_systems": len(dataset.cyclone.active_cyclone_systems) if dataset else 0,
            "forecast_rainfall_mm": dataset.weather_forecast.forecast_rainfall_mm if dataset else None,
            "is_hilly_or_mountainous": profile.primary_hazard == "LANDSLIDE" or (dataset and dataset.environment.terrain_slope_vulnerability in ("HIGH", "MODERATE"))
        }

        return CascadingRiskAssessment(
            region_id=profile.id,
            region_name=profile.name,
            region_type=profile.administrative_type,
            primary_hazard=active_hazard,
            evaluated_at=datetime.now(timezone.utc).isoformat(),
            evidence_posture=overall_posture,
            chains=[chain],
            context_indicators=context_indicators,
            synthetic_records=0
        )

    def _build_hazard_chain(
        self,
        hazard: str,
        profile: Any,
        dataset: Optional[ForecastEnvironmentDataset]
    ) -> CascadingRiskChain:
        """Constructs a scientifically defensible consequence chain for the given hazard."""
        if hazard == "FLOOD":
            return self._build_flood_chain(profile, dataset)
        elif hazard == "CYCLONE":
            return self._build_cyclone_chain(profile, dataset)
        elif hazard == "EARTHQUAKE":
            return self._build_earthquake_chain(profile, dataset)
        elif hazard == "HEATWAVE":
            return self._build_heatwave_chain(profile, dataset)
        elif hazard == "LANDSLIDE":
            return self._build_landslide_chain(profile, dataset)
        else:  # SEVERE_WEATHER
            return self._build_severe_weather_chain(profile, dataset)

    # -------------------------------------------------------------------------
    # 1. FLOOD
    # -------------------------------------------------------------------------
    def _build_flood_chain(
        self,
        profile: Any,
        dataset: Optional[ForecastEnvironmentDataset]
    ) -> CascadingRiskChain:
        # Determine evidence posture from actual hydrological and terrain telemetry
        terrain_vuln = dataset.environment.terrain_slope_vulnerability if dataset else "UNAVAILABLE"
        hydrology_avail = dataset.hydrology.metadata.availability if dataset else "UNAVAILABLE"
        rain_72h = dataset.hydrology.accumulated_rainfall_72h_mm if dataset else None
        river_trend = dataset.hydrology.river_level_trend if dataset else "UNAVAILABLE"

        if hydrology_avail == InputAvailabilityStatus.AVAILABLE.value and rain_72h is not None and rain_72h > 70.0:
            posture = EvidencePosture.LIVE_EVIDENCE
            ev_desc = f"Observed 72h accumulated rainfall ({rain_72h:.1f} mm) and river stage trend '{river_trend}'."
        elif hydrology_avail == InputAvailabilityStatus.AVAILABLE.value and rain_72h is not None and rain_72h > 25.0:
            posture = EvidencePosture.RECENT_EVIDENCE
            ev_desc = f"Recent hydrological observation shows moderate accumulated rainfall ({rain_72h:.1f} mm)."
        elif hydrology_avail == InputAvailabilityStatus.UNAVAILABLE.value:
            posture = EvidencePosture.DATA_UNAVAILABLE
            ev_desc = "Local hydrological telemetry unavailable for this basin; relationship grounded in baseline physical hydrology."
        else:
            posture = EvidencePosture.BASELINE_ONLY
            ev_desc = "Regional baseline hydrology; no active anomalous precipitation threshold exceeded."

        # Terrain slope conditionality: Flood-induced landslides occur where slopes are susceptible
        if terrain_vuln in ("HIGH", "MODERATE"):
            slope_risk_desc = (
                f"Flood-related soil saturation and riverbank toe erosion MAY increase slope instability and "
                f"landslide susceptibility in this region's terrain (terrain vulnerability: {terrain_vuln})."
            )
            terrain_note = f"Region exhibits {terrain_vuln} slope vulnerability; elevated hydrostatic pore pressure can trigger secondary mass wasting."
        elif terrain_vuln == "LOW":
            slope_risk_desc = (
                "Terrain slope vulnerability is assessed as LOW. Primary secondary risk is localized embankment "
                "scour and drainage breach rather than mass hill-slope failure."
            )
            terrain_note = "Predominantly flat/alluvial terrain; risk is primarily embankment destabilization rather than hill-slope landslides."
        else:
            slope_risk_desc = (
                "Flood-related saturation can increase soil erosion and embankment stress. "
                "Local slope telemetry and geological geotechnical monitoring are currently UNAVAILABLE for this location."
            )
            terrain_note = "Local slope telemetry is unavailable; unmonitored geotechnical conditions must be treated with caution."

        stages = [
            CascadingStage(
                stage_order=1,
                stage_type="PRIMARY_HAZARD",
                title="Primary Hazard // Riverine / Pluvial Flood",
                description="Heavy precipitation runoff or high upstream discharge causes river stages or drainage basins to exceed carrying capacity.",
                scientific_classification=RelationshipClassification.ESTABLISHED_PHYSICAL_RELATIONSHIP,
                evidence_posture=posture,
                supporting_evidence=[ev_desc],
                conditions_for_escalation=["Intense rainfall exceeding 50 mm in 24 hours", "Upstream dam release or catchment runoff surge"],
                unmonitored_or_unknown=["Sub-catchment micro-basin gauge coverage", "Unmonitored rural tributary stage heights"],
                field_warning_signs=["Water turning turbid and carrying debris", "Rapidly rising water marks on bridge piers"],
                defensive_actions=["Move valuables and documents to higher elevation", "Monitor official CWC / DDMA bulletins"]
            ),
            CascadingStage(
                stage_order=2,
                stage_type="PHYSICAL_CHANGE",
                title="Environmental Change // Soil Saturation & Bank Erosion",
                description="Prolonged inundation increases soil pore-water pressure, reducing effective shear strength along riverbanks and unreinforced earthen embankments.",
                scientific_classification=RelationshipClassification.ESTABLISHED_PHYSICAL_RELATIONSHIP,
                evidence_posture=posture,
                supporting_evidence=[
                    f"Basin soil condition: {dataset.hydrology.basin_condition if dataset else 'UNAVAILABLE'}",
                    "Geotechnical principle: Terzaghi effective stress decrease during complete hydraulic saturation"
                ],
                conditions_for_escalation=["Continuous waterlogging exceeding 48 hours", "High flow velocity scouring embankment toes"],
                unmonitored_or_unknown=["Pore-water piezometer data along rural bunds", "Sub-surface soil compaction metrics"],
                field_warning_signs=["New tension cracks parallel to riverbanks or bunds", "Seepage or sand-boils appearing behind flood embankments"],
                defensive_actions=["Stay off earthen river embankments and flood-protection dykes", "Report embankment seepage immediately to local revenue/irrigation officials"]
            ),
            CascadingStage(
                stage_order=3,
                stage_type="SECONDARY_HAZARD",
                title="Secondary Hazard // Embankment Breach & Slope Failure",
                description=slope_risk_desc,
                scientific_classification=RelationshipClassification.CONDITIONAL_SECONDARY_RISK,
                evidence_posture=posture if terrain_vuln != "UNAVAILABLE" else EvidencePosture.DATA_UNAVAILABLE,
                supporting_evidence=[
                    f"Terrain slope vulnerability: {terrain_vuln}",
                    "Conditionality: Soil saturation reduces bank resisting forces proportionally to slope angle"
                ],
                conditions_for_escalation=["High water head differential across earthen dykes", "Sustained torrential downpour on saturated hill slopes"],
                unmonitored_or_unknown=["Real-time inclinometer telemetry on road cuttings", "Local earthen bund structural health ratings"],
                field_warning_signs=["Slumping of road edges or berms", "Mud plumes appearing in previously clear hillside streams"],
                defensive_actions=["Evacuate low-lying areas behind aging earthen bunds", "Avoid driving through mountain cuttings during prolonged rainfall"]
            ),
            CascadingStage(
                stage_order=4,
                stage_type="TERTIARY_CONSEQUENCE",
                title="Tertiary Consequences // Lifeline Disruption & Public Health Risk",
                description="Secondary failures threaten transportation corridors, submerge drinking water tube-wells, and disrupt basic sanitation.",
                scientific_classification=RelationshipClassification.CONDITIONAL_SECONDARY_RISK,
                evidence_posture=posture,
                supporting_evidence=["Public health epidemiology: Inundation of municipal water mains and open wells creates acute waterborne contamination risk."],
                conditions_for_escalation=["Submersion of electrical distribution substations", "Isolation of habitations with road access cut"],
                unmonitored_or_unknown=["Village-level drinking well contamination status", "Real-time road culvert structural integrity"],
                field_warning_signs=["Discolored or foul-smelling tap/well water", "Ponding around electrical transformer poles"],
                defensive_actions=["Boil all drinking water vigorously for at least 1 minute or use chlorine tablets", "Treat all downed or submerged wires as live and dangerous"]
            )
        ]

        return CascadingRiskChain(
            hazard="FLOOD",
            title="Flood Cascading Chain: Hydraulic Saturation -> Structural Bank Erosion -> Infrastructure & Health Impacts",
            primary_hazard_summary="Riverine inundation and pluvial drainage overflow",
            environmental_change_summary="Soil saturation, pore pressure escalation, and hydraulic shear along riverbanks",
            secondary_hazard_summary="Embankment breach, toe erosion, and conditional slope instability in steep terrain",
            tertiary_consequences_summary="Culvert washouts, drinking water contamination, and community road access cut-offs",
            overall_evidence_posture=posture,
            stages=stages,
            scientific_rationale="Hydraulic pore pressure mechanics govern embankment and slope stability during prolonged inundation.",
            terrain_sensitivity_note=terrain_note,
            synthetic_records=0
        )

    # -------------------------------------------------------------------------
    # 2. CYCLONE
    # -------------------------------------------------------------------------
    def _build_cyclone_chain(
        self,
        profile: Any,
        dataset: Optional[ForecastEnvironmentDataset]
    ) -> CascadingRiskChain:
        coastal_exp = dataset.cyclone.coastal_exposure if dataset else "NONE"
        wind_knots = dataset.cyclone.wind_intensity_knots if dataset else None
        active_systems = dataset.cyclone.active_cyclone_systems if dataset else []

        if len(active_systems) > 0 and wind_knots and wind_knots >= 34.0:
            posture = EvidencePosture.LIVE_EVIDENCE
            ev_desc = f"Active cyclonic disturbance detected with sustained wind intensity of {wind_knots:.1f} knots."
        elif dataset and dataset.weather_forecast.forecast_wind_kmh and dataset.weather_forecast.forecast_wind_kmh > 60.0:
            posture = EvidencePosture.FORECAST_AVAILABLE
            ev_desc = f"Forecast model indicates gale winds exceeding {dataset.weather_forecast.forecast_wind_kmh:.0f} km/h."
        elif coastal_exp in ("HIGH", "MODERATE"):
            posture = EvidencePosture.BASELINE_ONLY
            ev_desc = f"Region has {coastal_exp} coastal exposure to maritime cyclonic systems; no active cyclone currently tracked."
        else:
            posture = EvidencePosture.BASELINE_ONLY
            ev_desc = "Inland or low-coastal exposure baseline; cyclonic risk is limited to dissipated convective depressions."

        stages = [
            CascadingStage(
                stage_order=1,
                stage_type="PRIMARY_HAZARD",
                title="Primary Hazard // Tropical Cyclone & Storm Surge",
                description="Intense low-pressure marine vortex brings destructive gale-force winds, torrential squall bands, and coastal storm surges.",
                scientific_classification=RelationshipClassification.ESTABLISHED_PHYSICAL_RELATIONSHIP,
                evidence_posture=posture,
                supporting_evidence=[ev_desc],
                conditions_for_escalation=["Central pressure deepening below 980 hPa", "Landfall timing coinciding with astronomical high tide"],
                unmonitored_or_unknown=["Micro-scale coastal bathymetry variations affecting local surge height"],
                field_warning_signs=["Rapid atmospheric pressure drop on aneroid barometers", "Sudden ocean swell and receding shoreline prior to surge"],
                defensive_actions=["Evacuate to designated pucca Cyclone Shelters well before gale arrival", "Tie down loose exterior assets and board up glass windows"]
            ),
            CascadingStage(
                stage_order=2,
                stage_type="PHYSICAL_CHANGE",
                title="Environmental Change // Wind Shear & Marine Saline Inundation",
                description="Extreme aerodynamic drag exerts severe lateral loads on structures; storm surge forces seawater kilometers inland along estuaries.",
                scientific_classification=RelationshipClassification.ESTABLISHED_PHYSICAL_RELATIONSHIP,
                evidence_posture=posture,
                supporting_evidence=[
                    f"Coastal Exposure: {coastal_exp}",
                    "Atmospheric physics: Wind force scales with the square of velocity (Dynamic Pressure = 0.5 * rho * v^2)"
                ],
                conditions_for_escalation=["Squalls exceeding 100 km/h (54 knots)", "Surge height exceeding 2.0 meters above astronomical tide"],
                unmonitored_or_unknown=["Local saline intrusion depth into freshwater aquifers"],
                field_warning_signs=["Salt spray traveling far inland", "Severe bending or uprooting of shallow-rooted coastal trees"],
                defensive_actions=["Disconnect household electrical appliances to protect against surge spikes", "Store drinking water in sealed containers before saline contamination"]
            ),
            CascadingStage(
                stage_order=3,
                stage_type="SECONDARY_HAZARD",
                title="Secondary Hazard // Coastal Inundation & Structural Up-rooting",
                description="Saline floodwaters submerge agricultural tracts and coastal roads, while high winds topple power transmission towers and telecommunication masts.",
                scientific_classification=RelationshipClassification.CONDITIONAL_SECONDARY_RISK,
                evidence_posture=posture,
                supporting_evidence=["Empirical damage assessments from historical cyclonic landfalls across the Bay of Bengal and Arabian Sea."],
                conditions_for_escalation=["Unreinforced masonry or tin-roof construction", "Prolonged exposure during the eye-wall transit"],
                unmonitored_or_unknown=["Condition of telecom backup diesel generators in coastal towers"],
                field_warning_signs=["Snapping sounds from overhead power lines", "Corrugated tin sheets peeling from roofs"],
                defensive_actions=["Remain inside the strongest interior room away from exterior windows", "Do not venture out during the calm 'eye' of the storm"]
            ),
            CascadingStage(
                stage_order=4,
                stage_type="TERTIARY_CONSEQUENCE",
                title="Tertiary Consequences // Telecommunication Blackout & Salinization",
                description="Destruction of utility poles and mobile towers creates widespread communications blackout; coastal drinking wells suffer long-term salinization.",
                scientific_classification=RelationshipClassification.CONDITIONAL_SECONDARY_RISK,
                evidence_posture=posture,
                supporting_evidence=["Post-cyclone disaster recovery evidence: Telecom towers lose grid power and backup fuel within 24-48 hours."],
                conditions_for_escalation=["Damage to regional electrical grid sub-stations", "Saltwater remaining trapped in agricultural fields"],
                unmonitored_or_unknown=["Restoration timelines for high-voltage transmission lines"],
                field_warning_signs=["Loss of cellular signal bars across multiple carriers", "Brackish taste in municipal or tube-well water"],
                defensive_actions=["Rely on battery-powered All India Radio transceivers for official civil bulletins", "Use only verified fresh water sources; do not consume brackish well water"]
            )
        ]

        return CascadingRiskChain(
            hazard="CYCLONE",
            title="Cyclone Cascading Chain: Extreme Wind & Surge -> Infrastructure Collapse -> Utility Blackout",
            primary_hazard_summary="Tropical storm vortex with high wind and heavy squalls",
            environmental_change_summary="Aerodynamic pressure load, marine storm surge, and saline inland inundation",
            secondary_hazard_summary="Power transmission collapse, coastal flooding, and fallen tree blockages",
            tertiary_consequences_summary="Telecommunications blackout, drinking well salinization, and prolonged access isolation",
            overall_evidence_posture=posture,
            stages=stages,
            scientific_rationale="Wind load increases quadratically with speed; coastal surge follows shallow-water hydrodynamic wave mechanics.",
            synthetic_records=0
        )

    # -------------------------------------------------------------------------
    # 3. EARTHQUAKE
    # -------------------------------------------------------------------------
    def _build_earthquake_chain(
        self,
        profile: Any,
        dataset: Optional[ForecastEnvironmentDataset]
    ) -> CascadingRiskChain:
        seismic_zone = getattr(profile, "seismic_zone", None) or "Zone IV / V"
        posture = EvidencePosture.BASELINE_ONLY

        stages = [
            CascadingStage(
                stage_order=1,
                stage_type="PRIMARY_HAZARD",
                title="Primary Hazard // Seismic Ground Motion (Non-Predictable)",
                description="Tectonic fault slip radiates transient elastodynamic body and surface seismic waves through the earth's crust.",
                scientific_classification=RelationshipClassification.ESTABLISHED_PHYSICAL_RELATIONSHIP,
                evidence_posture=posture,
                supporting_evidence=[
                    f"Seismic Zonation: {seismic_zone} according to BIS IS 1893:2016.",
                    "Strict Scientific Guardrail: Earthquakes CANNOT be temporally predicted by science."
                ],
                conditions_for_escalation=["High peak ground acceleration (PGA) in shallow hypocentral events"],
                unmonitored_or_unknown=["Micro-level sub-surface fault stress accumulation state"],
                field_warning_signs=["Tremor, rattling of loose fixtures, sudden low rumbling sound"],
                defensive_actions=["Instinctive DROP, COVER, and HOLD ON under sturdy furniture", "Do NOT run outside during active shaking; falling facade masonry causes high casualties"]
            ),
            CascadingStage(
                stage_order=2,
                stage_type="PHYSICAL_CHANGE",
                title="Environmental Change // Ground Acceleration & Dynamic Structural Strain",
                description="Transient horizontal and vertical accelerations exert dynamic shear stresses on building foundations, non-ductile columns, and unreinforced masonry.",
                scientific_classification=RelationshipClassification.ESTABLISHED_PHYSICAL_RELATIONSHIP,
                evidence_posture=posture,
                supporting_evidence=[
                    "Structural mechanics: Unreinforced masonry (URM) and non-ductile frame structures suffer brittle shear cracking under cyclical lateral loads."
                ],
                conditions_for_escalation=["Presence of soft-story ground parking", "Saturated alluvial soil susceptible to liquefaction"],
                unmonitored_or_unknown=["Exact structural ductility compliance of private un-engineered buildings"],
                field_warning_signs=["Visible hairline diagonal shear cracks along masonry walls or beam-column joints"],
                defensive_actions=["Move away from exterior glass facades, brick parapets, and heavy bookcases", "Do NOT use elevators under any circumstances"]
            ),
            CascadingStage(
                stage_order=3,
                stage_type="SECONDARY_HAZARD",
                title="Secondary Hazard // Structural Cracking, Liquefaction & Secondary Fire",
                description="Compromised structures may experience partial collapse; fractured domestic LPG pipelines and severed electrical lines create acute secondary fire risks.",
                scientific_classification=RelationshipClassification.CONDITIONAL_SECONDARY_RISK,
                evidence_posture=posture,
                supporting_evidence=["Historical post-earthquake damage forensics: Secondary fires from severed gas/power lines are major sources of post-tremor casualties."],
                conditions_for_escalation=["Severe initial ground shaking causing structural yielding", "Dense urban settlements with narrow lane egress"],
                unmonitored_or_unknown=["Gas pipeline valve shut-off automation status"],
                field_warning_signs=["Odor of unburned LPG gas in corridors", "Sparks from damaged electrical conduits"],
                defensive_actions=["Shut off main household gas cylinder valve and electrical breaker switch immediately upon evacuation", "If gas smell is detected, do NOT operate electrical switches or open flames"]
            ),
            CascadingStage(
                stage_order=4,
                stage_type="TERTIARY_CONSEQUENCE",
                title="Tertiary Consequences // Aftershock Risk to Weakened Buildings & Lifeline Damage",
                description="Naturally occurring aftershock sequences pose severe collapse hazards to structures already stressed by the main tremor. Lifelines (water, power, transport) experience localized fractures.",
                scientific_classification=RelationshipClassification.ESTABLISHED_PHYSICAL_RELATIONSHIP,
                evidence_posture=posture,
                supporting_evidence=[
                    "Seismological invariant: Aftershock sequences follow Omori-Utsu decay laws; while individual timings cannot be predicted, their occurrence is a recognized physical certainty."
                ],
                conditions_for_escalation=["Re-entering severely cracked buildings prior to official structural audit", "Blocked road access hindering fire tenders"],
                unmonitored_or_unknown=["Individual structural residual load capacity without engineering inspection"],
                field_warning_signs=["Widening of existing structural cracks", "Creaking or groaning sounds in compromised buildings"],
                defensive_actions=["Do NOT re-enter cracked or tilted buildings until inspected by licensed structural engineers / municipal authorities", "Keep emergency survival kit and sturdy shoes ready near the safe open assembly area"]
            )
        ]

        return CascadingRiskChain(
            hazard="EARTHQUAKE",
            title="Earthquake Physical Consequence Chain: Ground Shaking -> Structural Strain -> Fire & Aftershock Hazards",
            primary_hazard_summary="Seismic ground motion radiated from fault rupture",
            environmental_change_summary="Ground acceleration, cyclical dynamic shear strain, and potential soil liquefaction",
            secondary_hazard_summary="Structural masonry cracking, gas line rupture, and electrical short-circuit fire risks",
            tertiary_consequences_summary="Elevated aftershock collapse vulnerability for compromised structures and transport blockages",
            overall_evidence_posture=posture,
            stages=stages,
            scientific_rationale="Elastodynamic ground motion imposes cyclical lateral forces on structures; aftershocks stress compromised components.",
            earthquake_non_prediction_notice="MANDATORY SCIENTIFIC INVARIANT: Earthquakes and aftershocks CANNOT be temporally predicted. This assessment outlines established structural engineering relationships, NOT an event forecast.",
            synthetic_records=0
        )

    # -------------------------------------------------------------------------
    # 4. HEATWAVE
    # -------------------------------------------------------------------------
    def _build_heatwave_chain(
        self,
        profile: Any,
        dataset: Optional[ForecastEnvironmentDataset]
    ) -> CascadingRiskChain:
        obs_temp = dataset.weather_observation.temperature_celsius if dataset else None
        fc_temp = dataset.weather_forecast.forecast_temperature_celsius if dataset else None

        if obs_temp and obs_temp >= 42.0:
            posture = EvidencePosture.LIVE_EVIDENCE
            ev_desc = f"Observed local ambient temperature ({obs_temp:.1f}°C) exceeds official IMD heatwave threshold."
        elif fc_temp and fc_temp >= 40.0:
            posture = EvidencePosture.FORECAST_AVAILABLE
            ev_desc = f"Numerical weather forecast projects maximum temperatures reaching {fc_temp:.1f}°C."
        else:
            posture = EvidencePosture.BASELINE_ONLY
            ev_desc = "Regional climatic baseline; current seasonal temperatures remain within normal thermal tolerance."

        stages = [
            CascadingStage(
                stage_order=1,
                stage_type="PRIMARY_HAZARD",
                title="Primary Hazard // Extreme Thermal Heatwave",
                description="Persistent high atmospheric pressure blocks convective cooling, leading to prolonged severe surface temperatures.",
                scientific_classification=RelationshipClassification.ESTABLISHED_PHYSICAL_RELATIONSHIP,
                evidence_posture=posture,
                supporting_evidence=[ev_desc],
                conditions_for_escalation=["Daytime maximum temperatures exceeding 45°C (or departure > 4.5°C from normal)", "High nighttime minimum temperatures preventing physiological cooling"],
                unmonitored_or_unknown=["Micro-climate variations in dense informal settlements lacking weather stations"],
                field_warning_signs=["Elevated dry-bulb temperatures above 40°C by 11:00 AM", "Intense shimmering heat mirages over asphalt surfaces"],
                defensive_actions=["Schedule all strenuous outdoor physical activity before 9:00 AM or after 5:00 PM", "Consume oral rehydration solution (ORS) and clean water frequently"]
            ),
            CascadingStage(
                stage_order=2,
                stage_type="PHYSICAL_CHANGE",
                title="Environmental Change // Elevated Thermal Radiation & Atmospheric Evaporative Deficit",
                description="High solar irradiation and vapor-pressure deficits trigger intense evapotranspiration, rapidly depleting shallow soil moisture and escalating urban heat retention.",
                scientific_classification=RelationshipClassification.ESTABLISHED_PHYSICAL_RELATIONSHIP,
                evidence_posture=posture,
                supporting_evidence=[
                    "Thermodynamics: Urban concrete and bitumen absorb high solar radiation, creating pronounced nighttime Urban Heat Island (UHI) effects."
                ],
                conditions_for_escalation=["Dry hot westerly winds (Loo)", "Relative humidity below 20% accelerating dehydration"],
                unmonitored_or_unknown=["Urban canopy surface temperature differentials"],
                field_warning_signs=["Rapid withering of roadside vegetation and shallow-rooted garden plants"],
                defensive_actions=["Keep sun-facing windows covered with reflective films, bamboo blinds, or dark curtains", "Provide shaded, ventilated resting quarters for elderly relatives and domestic animals"]
            ),
            CascadingStage(
                stage_order=3,
                stage_type="SECONDARY_HAZARD",
                title="Secondary Hazard // Acute Water Demand & Electrical Grid Transformer Strain",
                description="Municipal water demand surges while distribution transformers operate under continuous extreme thermal and electrical loads.",
                scientific_classification=RelationshipClassification.CONDITIONAL_SECONDARY_RISK,
                evidence_posture=posture,
                supporting_evidence=["Public utility operational records: Peak electrical loads for cooling coincide with reduced transformer cooling efficiency, increasing risk of localized transformer trips."],
                conditions_for_escalation=["Uninterrupted air-conditioning load during peak daytime hours", "Drawdown of municipal storage reservoirs"],
                unmonitored_or_unknown=["Real-time transformer oil temperature sensor coverage in distribution grids"],
                field_warning_signs=["Voltage fluctuations or dimming lights during peak afternoon hours", "Low municipal tap water pressure in tail-end distribution zones"],
                defensive_actions=["Conserve municipal water for essential hydration and hygiene", "Avoid running high-wattage appliances simultaneously during peak hours"]
            ),
            CascadingStage(
                stage_order=4,
                stage_type="TERTIARY_CONSEQUENCE",
                title="Tertiary Consequences // Exertional Heat Stroke & Agricultural Labor Stress",
                description="Human core body temperatures reach critical thresholds when wet-bulb temperatures inhibit evaporative sweating, leading to life-threatening heat stroke.",
                scientific_classification=RelationshipClassification.CONDITIONAL_SECONDARY_RISK,
                evidence_posture=posture,
                supporting_evidence=["Occupational health epidemiology: Outdoor agricultural and construction workers face exponential hyperthermia risk under sustained wet-bulb globe temperatures (WBGT) > 30°C."],
                conditions_for_escalation=["Direct outdoor sun exposure between 12:00 PM and 3:30 PM", "Pre-existing cardiovascular conditions, advanced age, or infancy"],
                unmonitored_or_unknown=["Hospital emergency room real-time thermal exhaustion admissions"],
                field_warning_signs=["Cessation of sweating, hot dry skin, confusion, staggering, or nausea (medical emergency: Heat Stroke)", "Severe muscle cramps and dizziness"],
                defensive_actions=["If heat stroke is suspected (confusion, ceased sweating): Move victim to shade, apply ice/wet cloth, and call 108 immediately", "Never leave children, elderly persons, or pets inside parked vehicles"]
            )
        ]

        return CascadingRiskChain(
            hazard="HEATWAVE",
            title="Heatwave Cascading Chain: Extreme Thermal Exposure -> Water/Grid Strain -> Physiological Heat Stroke",
            primary_hazard_summary="Severe meteorological heatwave with sustained high ambient temperatures",
            environmental_change_summary="Intense solar radiation, urban heat retention, and severe evaporative moisture deficit",
            secondary_hazard_summary="Spike in drinking water demand and severe electrical transformer thermal load",
            tertiary_consequences_summary="Life-threatening exertional heat stroke, occupational labor shutdown, and livestock thermal stress",
            overall_evidence_posture=posture,
            stages=stages,
            scientific_rationale="Atmospheric thermal trapping degrades human physiological heat dissipation and stresses urban utility lifelines.",
            synthetic_records=0
        )

    # -------------------------------------------------------------------------
    # 5. LANDSLIDE
    # -------------------------------------------------------------------------
    def _build_landslide_chain(
        self,
        profile: Any,
        dataset: Optional[ForecastEnvironmentDataset]
    ) -> CascadingRiskChain:
        terrain_vuln = dataset.environment.terrain_slope_vulnerability if dataset else "UNAVAILABLE"
        rain_24h = dataset.weather_observation.rainfall_mm_24h if dataset else None
        rain_72h = dataset.hydrology.accumulated_rainfall_72h_mm if dataset else None

        if terrain_vuln in ("HIGH", "MODERATE") and rain_72h and rain_72h > 60.0:
            posture = EvidencePosture.LIVE_EVIDENCE
            ev_desc = f"Terrain slope vulnerability is {terrain_vuln} with high 72h accumulated precipitation ({rain_72h:.1f} mm)."
        elif terrain_vuln in ("HIGH", "MODERATE") and rain_24h and rain_24h > 20.0:
            posture = EvidencePosture.RECENT_EVIDENCE
            ev_desc = f"Terrain slope vulnerability is {terrain_vuln} with active 24h precipitation ({rain_24h:.1f} mm)."
        elif terrain_vuln in ("HIGH", "MODERATE"):
            posture = EvidencePosture.BASELINE_ONLY
            ev_desc = f"Region has {terrain_vuln} slope vulnerability baseline; no active heavy precipitation trigger currently observed."
        elif terrain_vuln == "LOW":
            posture = EvidencePosture.BASELINE_ONLY
            ev_desc = "Topographical baseline indicates predominantly flat terrain; mass wasting susceptibility is low."
        else:
            posture = EvidencePosture.DATA_UNAVAILABLE
            ev_desc = "Local slope telemetry and geological geotechnical sensors are unavailable for this region."

        stages = [
            CascadingStage(
                stage_order=1,
                stage_type="PRIMARY_HAZARD",
                title="Primary Hazard // Slope Instability & Mass Debris Flow",
                description="Gravity-driven shear stress along a failure surface exceeds the shear strength of unconsolidated soil or weathered bedrock.",
                scientific_classification=RelationshipClassification.ESTABLISHED_PHYSICAL_RELATIONSHIP,
                evidence_posture=posture,
                supporting_evidence=[ev_desc],
                conditions_for_escalation=["Rainfall intensity exceeding 15 mm/hour on saturated slopes", "Recent road cutting or toe excavation without retaining walls"],
                unmonitored_or_unknown=["Sub-surface geotechnical joint orientation in hill cuttings"],
                field_warning_signs=["New cracks appearing in hillside soil, retaining walls, or foundations", "Sudden tilting of trees, utility poles, or fences on hill slopes"],
                defensive_actions=["Evacuate slope terrain immediately if you hear crackling trees or rumbling sounds", "Move laterally away from gullies and natural drainage ravines"]
            ),
            CascadingStage(
                stage_order=2,
                stage_type="PHYSICAL_CHANGE",
                title="Environmental Change // Slope Failure & Channel Debris Accumulation",
                description="Dislodged debris, boulders, and saturated mud descend into stream valleys, blocking natural drainage culverts and road alignments.",
                scientific_classification=RelationshipClassification.ESTABLISHED_PHYSICAL_RELATIONSHIP,
                evidence_posture=posture,
                supporting_evidence=[
                    f"Terrain vulnerability classification: {terrain_vuln}",
                    "Mohr-Coulomb shear strength criterion: Pore-water pressure reduces effective normal stress."
                ],
                conditions_for_escalation=["Debris volume exceeding road culvert clearance", "Blockage of narrow mountain river defiles"],
                unmonitored_or_unknown=["Upstream tributary blockage status in remote valleys"],
                field_warning_signs=["Sudden drop in mountain stream flow (indicating an upstream blockage/landslide dam)", "Sudden emergence of muddy, turbid water where clear water flowed minutes before"],
                defensive_actions=["Never attempt to drive through active mountain talus slides", "Alert downstream communities if a river channel appears abruptly blocked"]
            ),
            CascadingStage(
                stage_order=3,
                stage_type="SECONDARY_HAZARD",
                title="Secondary Hazard // Valley River Damming & Landslide Lake Outburst Risk",
                description="Debris blocking a river can form a temporary natural dam; water accumulates behind the dam until sudden breaching triggers a flash flood wave.",
                scientific_classification=RelationshipClassification.CONDITIONAL_SECONDARY_RISK,
                evidence_posture=posture,
                supporting_evidence=["Historical Himalayan and Western Ghats disaster records: Landslide-dam breach floods cause severe downstream damage hours or days after the initial slide."],
                conditions_for_escalation=["Rapidly rising water levels behind the debris blockage", "Overtopping of uncompacted sediment dam"],
                unmonitored_or_unknown=["Volume of impounded water behind remote landslide blockages"],
                field_warning_signs=["River water completely stopping or drying up downstream of a slide", "A loud roaring sound from upstream signaling dam breach"],
                defensive_actions=["Move to high ground (> 20 meters above river bed) immediately if stream water suddenly recedes", "Do NOT linger near mountain riverbanks after heavy downpours"]
            ),
            CascadingStage(
                stage_order=4,
                stage_type="TERTIARY_CONSEQUENCE",
                title="Tertiary Consequences // Highway Cut-Off, Power Grid Severance & Isolation",
                description="Damage to national highways and bridges isolates remote mountain communities, severing power lines and healthcare supply chains.",
                scientific_classification=RelationshipClassification.CONDITIONAL_SECONDARY_RISK,
                evidence_posture=posture,
                supporting_evidence=["Transport lifeline vulnerability: Mountain state arterial highways (e.g. NH-10, NH-58, NH-44) frequently experience multi-day closures during monsoon slides."],
                conditions_for_escalation=["Multiple concurrent slides along the same transport corridor", "Inclement weather preventing rescue helicopter operations"],
                unmonitored_or_unknown=["Local heavy earthmoving machinery availability near slide locations"],
                field_warning_signs=["Fallen transmission poles tangled in roadside landslide debris", "Long queues of stationary transport vehicles halted before hill sections"],
                defensive_actions=["Maintain 7-day reserve of dry food, drinking water, and chronic medicines in hill habitations", "Report blocked state/national highways to district control desks (1077 / 112)"]
            )
        ]

        return CascadingRiskChain(
            hazard="LANDSLIDE",
            title="Landslide Cascading Chain: Slope Failure -> Valley Damming -> Outburst Flood & Lifeline Severance",
            primary_hazard_summary="Gravitational mass movement and slope debris failure",
            environmental_change_summary="Soil shear strength loss, mass displacement, and valley drainage channel blockage",
            secondary_hazard_summary="Natural landslide-dam impoundment and conditional breach flash flooding",
            tertiary_consequences_summary="Highway corridor severance, remote settlement isolation, and severed utility conduits",
            overall_evidence_posture=posture,
            stages=stages,
            scientific_rationale="Geotechnical shear failure drives slope movement; impounded valley drainage creates secondary outburst hazards.",
            terrain_sensitivity_note=f"Terrain slope vulnerability is assessed as {terrain_vuln}. Slopes > 25° with weathered overburden carry elevated susceptibility.",
            synthetic_records=0
        )

    # -------------------------------------------------------------------------
    # 6. SEVERE_WEATHER
    # -------------------------------------------------------------------------
    def _build_severe_weather_chain(
        self,
        profile: Any,
        dataset: Optional[ForecastEnvironmentDataset]
    ) -> CascadingRiskChain:
        obs_rain = dataset.weather_observation.rainfall_mm_24h if dataset else None
        obs_wind = dataset.weather_observation.wind_speed_kmh if dataset else None
        flags = dataset.weather_forecast.severe_weather_flags if dataset else []

        if len(flags) > 0 or (obs_rain and obs_rain > 50.0) or (obs_wind and obs_wind > 50.0):
            posture = EvidencePosture.LIVE_EVIDENCE
            ev_desc = f"Active severe convective storm alerts: {', '.join(flags) if flags else 'Intense squalls/rain observed'}."
        elif dataset and dataset.weather_forecast.forecast_rainfall_mm and dataset.weather_forecast.forecast_rainfall_mm > 35.0:
            posture = EvidencePosture.FORECAST_AVAILABLE
            ev_desc = f"Numerical model forecasts convective rainfall exceeding {dataset.weather_forecast.forecast_rainfall_mm:.1f} mm."
        else:
            posture = EvidencePosture.BASELINE_ONLY
            ev_desc = "Regional baseline weather; standard atmospheric convective variability without active threshold breach."

        stages = [
            CascadingStage(
                stage_order=1,
                stage_type="PRIMARY_HAZARD",
                title="Primary Hazard // Severe Convective Thunderstorm & Lightning",
                description="Intense convective updrafts generate deep cumulonimbus cells with cloud-to-ground lightning discharges, localized microbursts, and intense downpours.",
                scientific_classification=RelationshipClassification.ESTABLISHED_PHYSICAL_RELATIONSHIP,
                evidence_posture=posture,
                supporting_evidence=[ev_desc],
                conditions_for_escalation=["Severe convective available potential energy (CAPE > 2000 J/kg)", "Strong vertical wind shear producing supercell structures"],
                unmonitored_or_unknown=["Micro-scale Doppler weather radar coverage in remote terrain gaps"],
                field_warning_signs=["Rapid darkening of the sky with towering anvil clouds", "Sudden sharp drop in temperature accompanied by gusty winds"],
                defensive_actions=["Adhere to the 30-30 Rule: If thunder is heard within 30 seconds of lightning, seek shelter immediately indoors", "Never shelter under tall isolated trees, tin sheds, or near metal fences"]
            ),
            CascadingStage(
                stage_order=2,
                stage_type="PHYSICAL_CHANGE",
                title="Environmental Change // Flash Precipitation & High Kinetic Wind Gusts",
                description="Extremely high instantaneous rainfall rates overwhelm local storm drains within minutes, while localized downburst gusts exert sudden lateral pressure.",
                scientific_classification=RelationshipClassification.ESTABLISHED_PHYSICAL_RELATIONSHIP,
                evidence_posture=posture,
                supporting_evidence=["Atmospheric thermodynamics: Downbursts occur when rain-cooled dense air plunges rapidly, spreading radially at ground level."],
                conditions_for_escalation=["Rainfall rates exceeding 30 mm/hour", "Microburst wind gusts exceeding 75 km/h"],
                unmonitored_or_unknown=["Urban stormwater sewer carrying capacity and blockage status"],
                field_warning_signs=["Water swirling over manhole covers and backflowing from street curbs", "Loose branches and plastic debris flying horizontally"],
                defensive_actions=["Pull vehicles safely over away from tall trees and overhead wires; stay inside the metal vehicle", "Unplug sensitive household electronics and disconnect computer modems"]
            ),
            CascadingStage(
                stage_order=3,
                stage_type="SECONDARY_HAZARD",
                title="Secondary Hazard // Urban Flash Waterlogging & Tree/Pylon Falls",
                description="Submerged underpasses and roads create acute drowning and vehicle stalling hazards; falling branches tear down power service cables.",
                scientific_classification=RelationshipClassification.CONDITIONAL_SECONDARY_RISK,
                evidence_posture=posture,
                supporting_evidence=["Urban hydrology: Impervious asphalt/concrete surfaces generate near 100% surface runoff, causing rapid street ponding."],
                conditions_for_escalation=["Blocked drainage culverts", "Un-pruned roadside trees with hollow trunks"],
                unmonitored_or_unknown=["Water depth telemetry in railway and road underpasses"],
                field_warning_signs=["Submerged vehicle tires exceeding rim depth (30 cm)", "Sparking electrical wires touching puddles"],
                defensive_actions=["Never drive or walk into water-filled underpasses; submerged water depths are deceptive and can trap vehicles", "Treat all standing water near electrical poles as potentially electrified"]
            ),
            CascadingStage(
                stage_order=4,
                stage_type="TERTIARY_CONSEQUENCE",
                title="Tertiary Consequences // Localized Grid Disruption & Traffic Gridlock",
                description="Localized transformer trips and fallen poles cause short-term neighborhood blackouts; traffic halts across key urban arteries.",
                scientific_classification=RelationshipClassification.CONDITIONAL_SECONDARY_RISK,
                evidence_posture=posture,
                supporting_evidence=["Municipal emergency logs: Thunderstorm squalls cause extensive localized power outages and emergency service delays."],
                conditions_for_escalation=["Peak rush-hour timing during storm onset", "Multiple feeder line trips in distribution substations"],
                unmonitored_or_unknown=["Local electricity distribution repair crew dispatch times"],
                field_warning_signs=["Loss of streetlights and neighborhood power", "Audible siren alerts from stalled emergency vehicles"],
                defensive_actions=["Wait at least 30 minutes after the last thunderclap before resuming outdoor activities", "Report fallen live wires to the local electricity board emergency desk or 112"]
            )
        ]

        return CascadingRiskChain(
            hazard="SEVERE_WEATHER",
            title="Severe Weather Cascading Chain: Convective Storm -> Urban Waterlogging & Lightning -> Utility Disruption",
            primary_hazard_summary="Intense convective thunderstorm with lightning and gust fronts",
            environmental_change_summary="Instantaneous high-rate precipitation and localized microburst gusts",
            secondary_hazard_summary="Rapid street flash waterlogging, underpass inundation, and fallen tree branches",
            tertiary_consequences_summary="Neighborhood power trips, traffic paralysis, and acute outdoor lightning hazards",
            overall_evidence_posture=posture,
            stages=stages,
            scientific_rationale="Deep convective updrafts release high kinetic and electrical energy; high rainfall rates exceed urban infiltration rates.",
            synthetic_records=0
        )


cascading_risk_engine = CascadingRiskEngine()
