/**
 * RISK // INDIA — Cascading & Secondary Risk API Service
 * =======================================================
 * Fetches authoritative multi-stage consequence chains from the backend.
 * 
 * MANDATORY AMENDMENT ENFORCEMENT:
 * - Offline fallback data NEVER appears as live local evidence, forecast, telemetry, or prediction.
 * - Static fallback relationships represent ONLY scientifically established baseline physical relationships.
 * - Always marked with evidence posture BASELINE_ONLY.
 * - Zero fabricated local observations, telemetry, forecasts, or pseudo-probabilities.
 */

import { apiClient } from './api';
import { CascadingRiskAssessment, CascadingRiskChain, EvidencePosture } from '../types/cascadingRisk';

// Scientifically established baseline physical chains (strictly BASELINE_ONLY, zero fabricated local telemetry)
const BASELINE_FALLBACK_CHAINS: Record<string, CascadingRiskChain> = {
  FLOOD: {
    hazard: 'FLOOD',
    title: 'Flood Cascading Chain: Hydraulic Saturation -> Bank Scour -> Lifeline Interruption',
    primary_hazard_summary: 'Riverine overflow and pluvial stormwater accumulation',
    environmental_change_summary: 'Prolonged inundation increases soil pore-water pressure along earthen dykes and riverbanks',
    secondary_hazard_summary: 'Embankment breach, toe erosion, and conditional slope instability in steep terrain',
    tertiary_consequences_summary: 'Culvert damage, drinking water tube-well contamination, and localized access cuts',
    overall_evidence_posture: 'BASELINE_ONLY',
    scientific_rationale: 'Established physical relationship: Terzaghi effective stress reduction in hydraulically saturated soils.',
    terrain_sensitivity_note: 'Secondary hill-slope landslides require vulnerable sloping terrain. Flat alluvial plains primarily experience embankment toe erosion.',
    stages: [
      {
        stage_order: 1,
        stage_type: 'PRIMARY_HAZARD',
        title: 'Primary Hazard // Riverine / Pluvial Flood',
        description: 'Excess runoff exceeds natural channel drainage capacity.',
        scientific_classification: 'ESTABLISHED_PHYSICAL_RELATIONSHIP',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Hydrological baseline: Runoff generation exceeds channel conveyance capacity.'],
        conditions_for_escalation: ['Intense 24h precipitation', 'Upstream catchment discharge'],
        unmonitored_or_unknown: ['Offline mode: Live river gauge telemetry not accessible.'],
        field_warning_signs: ['Rapidly rising water marks on bridge piers', 'Water turning muddy and debris-laden'],
        defensive_actions: ['Elevate household electronics and medicines', 'Monitor official emergency radio broadcasts']
      },
      {
        stage_order: 2,
        stage_type: 'PHYSICAL_CHANGE',
        title: 'Environmental Change // Soil Saturation & Bank Stress',
        description: 'Saturation weakens cohesive soil strength along unreinforced earthen riverbanks.',
        scientific_classification: 'ESTABLISHED_PHYSICAL_RELATIONSHIP',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Geotechnical physics: Pore-water pressure reduces soil shear strength.'],
        conditions_for_escalation: ['Continuous submersion exceeding 48 hours'],
        unmonitored_or_unknown: ['Sub-surface piezometer pore-water pressure metrics'],
        field_warning_signs: ['Tension cracks parallel to riverbanks or bunds', 'Seepage or sand boils behind embankments'],
        defensive_actions: ['Stay clear of earthen dykes and river edges', 'Report seepage to local revenue/irrigation officials']
      },
      {
        stage_order: 3,
        stage_type: 'SECONDARY_HAZARD',
        title: 'Secondary Hazard // Embankment Breach & Conditional Slope Failure',
        description: 'Weakened banks may breach under hydraulic head; steep slopes MAY experience secondary instability if terrain is vulnerable.',
        scientific_classification: 'CONDITIONAL_SECONDARY_RISK',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Conditionality: Soil saturation reduces slope factor of safety in steep topography.'],
        conditions_for_escalation: ['Water level overtopping unpaved dykes', 'High rainfall on steep overburden'],
        unmonitored_or_unknown: ['Live slope inclinometer telemetry'],
        field_warning_signs: ['Slumping of road edges or embankments'],
        defensive_actions: ['Evacuate low-lying tracts behind aging bunds', 'Avoid driving through mountain cuttings during prolonged downpours']
      },
      {
        stage_order: 4,
        stage_type: 'TERTIARY_CONSEQUENCE',
        title: 'Tertiary Consequences // Water Contamination & Lifeline Disruption',
        description: 'Inundation submerges drinking water wells and municipal pipes, creating acute public health contamination risks.',
        scientific_classification: 'CONDITIONAL_SECONDARY_RISK',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Epidemiological baseline: Surface floodwaters introduce enteric pathogens into open wells.'],
        conditions_for_escalation: ['Submergence of community drinking water tube-wells'],
        unmonitored_or_unknown: ['Local bacterial contamination testing in drinking wells'],
        field_warning_signs: ['Discolored or odorous tap/well water'],
        defensive_actions: ['Boil drinking water vigorously for at least 1 minute', 'Never touch submerged electrical transformers']
      }
    ],
    synthetic_records: 0
  },
  CYCLONE: {
    hazard: 'CYCLONE',
    title: 'Cyclone Cascading Chain: Gale Winds & Surge -> Transmission Collapse -> Blackout',
    primary_hazard_summary: 'Tropical cyclonic vortex with high wind shear and squall bands',
    environmental_change_summary: 'Aerodynamic pressure load, marine storm surge, and saline inland inundation',
    secondary_hazard_summary: 'Power transmission collapse, coastal flooding, and fallen tree blockages',
    tertiary_consequences_summary: 'Telecommunications blackout, drinking well salinization, and prolonged access isolation',
    overall_evidence_posture: 'BASELINE_ONLY',
    scientific_rationale: 'Established physical relationship: Aerodynamic drag increases quadratically with wind velocity; storm surge follows coastal shallow-water hydrodynamic wave physics.',
    stages: [
      {
        stage_order: 1,
        stage_type: 'PRIMARY_HAZARD',
        title: 'Primary Hazard // Tropical Cyclone & Storm Surge',
        description: 'Intense marine low-pressure system generating gale-force squalls and sea surges.',
        scientific_classification: 'ESTABLISHED_PHYSICAL_RELATIONSHIP',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Meteorological baseline: Coastal maritime vulnerability to tropical cyclonic systems.'],
        conditions_for_escalation: ['Central pressure deepening', 'Landfall coinciding with astronomical high tide'],
        unmonitored_or_unknown: ['Offline mode: Live Doppler radar telemetry not connected.'],
        field_warning_signs: ['Rapid atmospheric pressure drop', 'Sudden sea swell along coastlines'],
        defensive_actions: ['Evacuate to designated Cyclone Shelters', 'Secure loose exterior sheets and board up glass windows']
      },
      {
        stage_order: 2,
        stage_type: 'PHYSICAL_CHANGE',
        title: 'Environmental Change // Wind Shear & Surge Ingress',
        description: 'High wind pressure topples shallow-rooted vegetation; storm surge penetrates inland along tidal estuaries.',
        scientific_classification: 'ESTABLISHED_PHYSICAL_RELATIONSHIP',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Physical mechanics: Aerodynamic drag = 0.5 * rho * v^2 * Cd.'],
        conditions_for_escalation: ['Squalls exceeding 100 km/h', 'Surge exceeding 2 meters above tide'],
        unmonitored_or_unknown: ['Micro-scale estuary surge wave propagation depth'],
        field_warning_signs: ['Salt spray traveling kilometers inland', 'Severe bending or uprooting of coastal palms'],
        defensive_actions: ['Disconnect household appliances to avoid surge spikes', 'Store fresh water before saline contamination']
      },
      {
        stage_order: 3,
        stage_type: 'SECONDARY_HAZARD',
        title: 'Secondary Hazard // Power Grid & Tree Collapse',
        description: 'High winds topple overhead power lines, utility poles, and roadside trees, severing transportation corridors.',
        scientific_classification: 'CONDITIONAL_SECONDARY_RISK',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Empirical infrastructure records: Overhead distribution lines fail under sustained gusts > 75 km/h.'],
        conditions_for_escalation: ['Unreinforced masonry or tin-roof dwellings', 'Overgrown tree branches near power cables'],
        unmonitored_or_unknown: ['Sub-station emergency backup fuel status'],
        field_warning_signs: ['Snapping sounds from overhead power lines', 'Tin roofing sheets peeling'],
        defensive_actions: ['Stay indoors in a central reinforced room', 'Do not venture out during the deceptive calm eye of the storm']
      },
      {
        stage_order: 4,
        stage_type: 'TERTIARY_CONSEQUENCE',
        title: 'Tertiary Consequences // Telecommunication & Water Blackout',
        description: 'Grid collapse exhausts cell tower batteries within 24 hours; storm surges contaminate coastal tube-wells with saltwater.',
        scientific_classification: 'CONDITIONAL_SECONDARY_RISK',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Public health records: Saline contamination of shallow aquifers causes severe potable water shortages.'],
        conditions_for_escalation: ['Damage to regional electrical transmission substations'],
        unmonitored_or_unknown: ['Cellular tower generator fuel replenishment access'],
        field_warning_signs: ['Loss of mobile phone network signal', 'Brackish taste in drinking water'],
        defensive_actions: ['Rely on battery-powered All India Radio transceivers for official civil bulletins', 'Drink only verified freshwater sources']
      }
    ],
    synthetic_records: 0
  },
  EARTHQUAKE: {
    hazard: 'EARTHQUAKE',
    title: 'Earthquake Consequence Chain: Ground Shaking -> Structural Strain -> Fire & Aftershock Hazards',
    primary_hazard_summary: 'Seismic ground motion radiated from crustal fault slip',
    environmental_change_summary: 'Ground acceleration, dynamic cyclical shear strain, and potential soil liquefaction',
    secondary_hazard_summary: 'Structural masonry cracking, domestic gas pipeline rupture, and electrical short-circuit fires',
    tertiary_consequences_summary: 'Elevated aftershock collapse vulnerability for compromised buildings and transport blockages',
    overall_evidence_posture: 'BASELINE_ONLY',
    scientific_rationale: 'Established physical relationship: Elastodynamic ground motion imposes cyclical lateral forces on structures.',
    earthquake_non_prediction_notice: 'MANDATORY SCIENTIFIC INVARIANT: Earthquakes and aftershocks CANNOT be temporally predicted. This assessment outlines established structural engineering relationships, NOT an event forecast.',
    stages: [
      {
        stage_order: 1,
        stage_type: 'PRIMARY_HAZARD',
        title: 'Primary Hazard // Seismic Ground Motion (Non-Predictable)',
        description: 'Fault slip releases accumulated elastic strain energy as elastodynamic seismic waves.',
        scientific_classification: 'ESTABLISHED_PHYSICAL_RELATIONSHIP',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Seismological invariant: Earthquakes CANNOT be temporally predicted by science.'],
        conditions_for_escalation: ['High peak ground acceleration (PGA) in shallow hypocentral events'],
        unmonitored_or_unknown: ['Micro-level sub-surface fault stress accumulation state'],
        field_warning_signs: ['Tremor, rattling of light fixtures, sudden low rumbling sound'],
        defensive_actions: ['Instinctive DROP, COVER, and HOLD ON under sturdy furniture', 'Do NOT run outside during active shaking; falling facade masonry causes high casualties']
      },
      {
        stage_order: 2,
        stage_type: 'PHYSICAL_CHANGE',
        title: 'Environmental Change // Dynamic Structural Shear Strain',
        description: 'Cyclical lateral forces induce tensile and shear deformation in building foundations and load-bearing walls.',
        scientific_classification: 'ESTABLISHED_PHYSICAL_RELATIONSHIP',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Structural mechanics: Unreinforced masonry (URM) suffers brittle shear cracking under cyclical lateral loads.'],
        conditions_for_escalation: ['Presence of soft-story ground parking', 'Saturated alluvial soil susceptible to liquefaction'],
        unmonitored_or_unknown: ['Individual structural ductility compliance of private un-engineered buildings'],
        field_warning_signs: ['Diagonal shear cracks along masonry walls or beam-column joints'],
        defensive_actions: ['Move away from exterior glass windows, brick parapets, and heavy shelves', 'Never use elevators under any circumstances']
      },
      {
        stage_order: 3,
        stage_type: 'SECONDARY_HAZARD',
        title: 'Secondary Hazard // Structural Damage & Secondary Fire',
        description: 'Structural cracking compromises load capacity; severed electrical lines and fractured LPG gas lines create acute fire hazards.',
        scientific_classification: 'CONDITIONAL_SECONDARY_RISK',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Damage forensics: Secondary fires from severed gas/power lines are major sources of post-tremor casualties.'],
        conditions_for_escalation: ['Severe initial ground shaking', 'Dense urban settlements with narrow lane egress'],
        unmonitored_or_unknown: ['Domestic gas pipeline automatic shut-off valve deployment rate'],
        field_warning_signs: ['Odor of unburned LPG cooking gas in corridors', 'Sparks from damaged electrical conduits'],
        defensive_actions: ['Shut off main household gas cylinder valve and electrical breaker switch immediately upon evacuation', 'If gas smell is detected, do NOT operate electrical switches or open flames']
      },
      {
        stage_order: 4,
        stage_type: 'TERTIARY_CONSEQUENCE',
        title: 'Tertiary Consequences // Aftershock Vulnerability & Lifeline Fractures',
        description: 'Aftershocks pose severe collapse hazards to already compromised structures. Water mains and access corridors suffer fractures.',
        scientific_classification: 'ESTABLISHED_PHYSICAL_RELATIONSHIP',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Seismological invariant: Aftershock sequences follow Omori-Utsu decay laws; their physical occurrence is established, though exact timing is unpredictable.'],
        conditions_for_escalation: ['Re-entering severely cracked buildings prior to official structural audit'],
        unmonitored_or_unknown: ['Residual load capacity of cracked structures without engineering inspection'],
        field_warning_signs: ['Widening of existing structural cracks', 'Creaking or groaning sounds in compromised buildings'],
        defensive_actions: ['Do NOT re-enter cracked buildings until inspected by licensed structural engineers', 'Stay in open ground away from overhead structures']
      }
    ],
    synthetic_records: 0
  },
  HEATWAVE: {
    hazard: 'HEATWAVE',
    title: 'Heatwave Cascading Chain: Extreme Thermal Exposure -> Water/Grid Strain -> Heat Stroke',
    primary_hazard_summary: 'Severe meteorological heatwave with sustained high ambient temperatures',
    environmental_change_summary: 'Intense solar radiation, urban heat retention, and severe evaporative moisture deficit',
    secondary_hazard_summary: 'Spike in drinking water demand and severe electrical transformer thermal load',
    tertiary_consequences_summary: 'Life-threatening exertional heat stroke, occupational labor shutdown, and livestock thermal stress',
    overall_evidence_posture: 'BASELINE_ONLY',
    scientific_rationale: 'Established physical relationship: Atmospheric thermal trapping degrades human physiological heat dissipation and stresses urban utility lifelines.',
    stages: [
      {
        stage_order: 1,
        stage_type: 'PRIMARY_HAZARD',
        title: 'Primary Hazard // Extreme Thermal Heatwave',
        description: 'Persistent high atmospheric pressure blocks convective cooling, leading to prolonged surface heating.',
        scientific_classification: 'ESTABLISHED_PHYSICAL_RELATIONSHIP',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Climatological baseline: High insolation during pre-monsoon summer across northern and peninsular India.'],
        conditions_for_escalation: ['Daytime temperatures exceeding 45°C', 'High nighttime temperatures preventing cooling'],
        unmonitored_or_unknown: ['Offline mode: Live station thermometer telemetry not connected.'],
        field_warning_signs: ['Dry-bulb temperatures above 40°C by 11:00 AM', 'Intense shimmering heat mirages over roads'],
        defensive_actions: ['Schedule outdoor labor before 9:00 AM or after 5:00 PM', 'Drink oral rehydration solution (ORS) and clean water frequently']
      },
      {
        stage_order: 2,
        stage_type: 'PHYSICAL_CHANGE',
        title: 'Environmental Change // Urban Heat Retention & Evaporative Deficit',
        description: 'Concrete and asphalt absorb solar radiation, releasing heat slowly at night and exacerbating Urban Heat Island (UHI) effects.',
        scientific_classification: 'ESTABLISHED_PHYSICAL_RELATIONSHIP',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Thermodynamics: High thermal mass of concrete maintains elevated nighttime ambient temperatures.'],
        conditions_for_escalation: ['Dry hot westerly winds (Loo)', 'Relative humidity below 20%'],
        unmonitored_or_unknown: ['Micro-canopy surface temperature differentials across urban wards'],
        field_warning_signs: ['Rapid wilting of garden plants and roadside foliage'],
        defensive_actions: ['Cover sun-facing windows with reflective blinds or curtains', 'Provide shaded resting quarters for elderly relatives and domestic animals']
      },
      {
        stage_order: 3,
        stage_type: 'SECONDARY_HAZARD',
        title: 'Secondary Hazard // Water Demand Surge & Transformer Overload',
        description: 'Municipal water consumption spikes while electrical distribution transformers operate under peak cooling loads.',
        scientific_classification: 'CONDITIONAL_SECONDARY_RISK',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Utility operations: High ambient temperatures diminish transformer cooling efficiency, raising trip frequencies.'],
        conditions_for_escalation: ['Simultaneous peak air-conditioning load', 'Depletion of local overhead water reservoirs'],
        unmonitored_or_unknown: ['Transformer oil temperature sensor coverage'],
        field_warning_signs: ['Voltage fluctuations or dimming lights during afternoon hours', 'Low municipal water pressure'],
        defensive_actions: ['Conserve water for essential hydration and hygiene', 'Avoid operating non-essential high-wattage appliances simultaneously']
      },
      {
        stage_order: 4,
        stage_type: 'TERTIARY_CONSEQUENCE',
        title: 'Tertiary Consequences // Exertional Heat Stroke & Medical Emergencies',
        description: 'High wet-bulb temperatures inhibit human sweat evaporation, causing rapid core body temperature escalation.',
        scientific_classification: 'CONDITIONAL_SECONDARY_RISK',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Occupational health: Sustained wet-bulb temperatures > 30°C cause severe exertional heat illnesses.'],
        conditions_for_escalation: ['Direct midday sun exposure', 'Pre-existing cardiovascular conditions, advanced age, or infancy'],
        unmonitored_or_unknown: ['Hospital emergency heatstroke admission rates'],
        field_warning_signs: ['Cessation of sweating, hot dry skin, confusion, staggering (Heat Stroke emergency)'],
        defensive_actions: ['If heat stroke is suspected: Move victim to shade, apply wet cloths/ice, call 108 immediately', 'Never leave children or pets inside parked vehicles']
      }
    ],
    synthetic_records: 0
  },
  LANDSLIDE: {
    hazard: 'LANDSLIDE',
    title: 'Landslide Cascading Chain: Slope Failure -> Valley Damming -> Outburst Flood & Isolation',
    primary_hazard_summary: 'Gravitational mass movement and slope debris failure',
    environmental_change_summary: 'Soil shear strength loss, mass displacement, and valley drainage channel blockage',
    secondary_hazard_summary: 'Natural landslide-dam impoundment and conditional breach flash flooding',
    tertiary_consequences_summary: 'Highway corridor severance, remote settlement isolation, and severed utility conduits',
    overall_evidence_posture: 'BASELINE_ONLY',
    scientific_rationale: 'Established physical relationship: Mohr-Coulomb shear failure occurs when gravitational shear exceeds soil shear strength.',
    terrain_sensitivity_note: 'Hilly and mountainous terrain with slopes > 25° and weathered overburden exhibits elevated landslide susceptibility.',
    stages: [
      {
        stage_order: 1,
        stage_type: 'PRIMARY_HAZARD',
        title: 'Primary Hazard // Slope Instability & Mass Debris Flow',
        description: 'Gravitational shear stress exceeds resisting shear strength along a failure plane in weathered rock or soil.',
        scientific_classification: 'ESTABLISHED_PHYSICAL_RELATIONSHIP',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Geotechnical physics: Pore-water pressure reduces effective normal stress on hill slopes.'],
        conditions_for_escalation: ['Rainfall intensity exceeding 15 mm/h on saturated slopes', 'Un-engineered toe cuts for hill roads'],
        unmonitored_or_unknown: ['Offline mode: Live sub-surface slope inclinometers not connected.'],
        field_warning_signs: ['New tension cracks appearing in soil or retaining walls', 'Tilting trees or utility poles on slopes'],
        defensive_actions: ['Evacuate slope terrain immediately if you hear crackling trees or rumblings', 'Move laterally away from stream gullies']
      },
      {
        stage_order: 2,
        stage_type: 'PHYSICAL_CHANGE',
        title: 'Environmental Change // Debris Displacement & Channel Infill',
        description: 'Dislodged mud, boulders, and trees descend rapidly into valley drainage channels and road alignments.',
        scientific_classification: 'ESTABLISHED_PHYSICAL_RELATIONSHIP',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Physical mechanics: Debris flows accelerate down-gradient, channeling into natural stream gullies.'],
        conditions_for_escalation: ['Debris volume exceeding river channel width'],
        unmonitored_or_unknown: ['Upstream tributary debris damming status'],
        field_warning_signs: ['Mountain stream flow dropping abruptly (signaling upstream debris blockage)', 'Water turning muddy'],
        defensive_actions: ['Never attempt to drive through active talus slides', 'Alert downstream communities if a river appears abruptly blocked']
      },
      {
        stage_order: 3,
        stage_type: 'SECONDARY_HAZARD',
        title: 'Secondary Hazard // Landslide Damming & Outburst Flooding',
        description: 'Debris forming a temporary dam impounds river water; sudden overtopping or breach releases a flash flood wave downstream.',
        scientific_classification: 'CONDITIONAL_SECONDARY_RISK',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Historical disaster records: Landslide Dam Outburst Floods (LDOF) cause high downstream damage.'],
        conditions_for_escalation: ['Rapid rise of impounded lake water', 'Overtopping of uncompacted debris dam'],
        unmonitored_or_unknown: ['Impounded lake water volume in remote gorges'],
        field_warning_signs: ['River water stopping or drying up downstream of a slide', 'Loud roaring sound from upstream'],
        defensive_actions: ['Move to high ground (> 20 meters above river bed) immediately if stream water suddenly recedes', 'Do NOT linger near mountain riverbanks after heavy rains']
      },
      {
        stage_order: 4,
        stage_type: 'TERTIARY_CONSEQUENCE',
        title: 'Tertiary Consequences // Lifeline Severance & Community Isolation',
        description: 'Highway blockages isolate mountain settlements, severing food supply chains, power lines, and emergency healthcare access.',
        scientific_classification: 'CONDITIONAL_SECONDARY_RISK',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Transport vulnerability: Mountain arterial highways frequently experience multi-day closures during monsoon slides.'],
        conditions_for_escalation: ['Multiple concurrent slides along the same transport corridor'],
        unmonitored_or_unknown: ['Heavy machinery clearing response timelines'],
        field_warning_signs: ['Fallen utility poles entangled in roadside slide debris', 'Stationary queues of supply trucks before hill passes'],
        defensive_actions: ['Maintain a 7-day reserve of food, water, and medicines in hill settlements', 'Report blocked highways to district control (112 / 1077)']
      }
    ],
    synthetic_records: 0
  },
  SEVERE_WEATHER: {
    hazard: 'SEVERE_WEATHER',
    title: 'Severe Weather Cascading Chain: Convective Storm -> Urban Waterlogging & Lightning -> Grid Disruption',
    primary_hazard_summary: 'Severe convective thunderstorm with lightning, microbursts, and intense downpours',
    environmental_change_summary: 'Instantaneous high-rate precipitation and localized microburst wind gusts',
    secondary_hazard_summary: 'Rapid street flash waterlogging, underpass inundation, and fallen tree branches',
    tertiary_consequences_summary: 'Neighborhood power trips, traffic paralysis, and acute outdoor lightning hazards',
    overall_evidence_posture: 'BASELINE_ONLY',
    scientific_rationale: 'Established physical relationship: High instantaneous precipitation exceeds urban infiltration and sewer capacity; gust fronts generate high kinetic shear.',
    stages: [
      {
        stage_order: 1,
        stage_type: 'PRIMARY_HAZARD',
        title: 'Primary Hazard // Convective Thunderstorm & Lightning',
        description: 'Deep cumulonimbus development with cloud-to-ground lightning discharges and squall gusts.',
        scientific_classification: 'ESTABLISHED_PHYSICAL_RELATIONSHIP',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Atmospheric physics: Convective instability releases high kinetic and electrostatic energy.'],
        conditions_for_escalation: ['High Convective Available Potential Energy (CAPE)', 'Strong vertical wind shear'],
        unmonitored_or_unknown: ['Offline mode: Real-time lightning detector network not connected.'],
        field_warning_signs: ['Rapid darkening of sky with towering anvil clouds', 'Sudden sharp drop in temperature with gusty winds'],
        defensive_actions: ['Apply 30-30 Rule: If thunder follows lightning within 30s, seek indoor shelter', 'Never shelter under tall isolated trees or tin sheds']
      },
      {
        stage_order: 2,
        stage_type: 'PHYSICAL_CHANGE',
        title: 'Environmental Change // Flash Precipitation & Kinetic Gusts',
        description: 'Rainfall rates overwhelm stormwater drains; microburst gusts exert sudden lateral pressure on trees and signage.',
        scientific_classification: 'ESTABLISHED_PHYSICAL_RELATIONSHIP',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Urban hydrology: High percentage of impervious surfaces generates immediate 100% surface runoff.'],
        conditions_for_escalation: ['Rainfall rate exceeding 30 mm/hour', 'Microburst gusts exceeding 70 km/h'],
        unmonitored_or_unknown: ['Local storm sewer debris blockage status'],
        field_warning_signs: ['Water swirling over road manholes', 'Tree branches snapping'],
        defensive_actions: ['Pull vehicles over away from tall trees and power cables', 'Unplug computers and modems to prevent lightning surge damage']
      },
      {
        stage_order: 3,
        stage_type: 'SECONDARY_HAZARD',
        title: 'Secondary Hazard // Underpass Inundation & Pylon Falls',
        description: 'Railway and road underpasses rapidly fill with water; snapped tree branches tear down local distribution service lines.',
        scientific_classification: 'CONDITIONAL_SECONDARY_RISK',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Civil engineering: Depressed underpasses collect runoff from surrounding elevated roads.'],
        conditions_for_escalation: ['Un-cleared drainage sumps in railway underpasses'],
        unmonitored_or_unknown: ['Underpass water depth sensor coverage'],
        field_warning_signs: ['Water covering road curbs or tires past rim depth'],
        defensive_actions: ['Never drive or walk into submerged underpasses', 'Treat all standing water near electrical poles as potentially electrified']
      },
      {
        stage_order: 4,
        stage_type: 'TERTIARY_CONSEQUENCE',
        title: 'Tertiary Consequences // Localized Grid Trips & Traffic Gridlock',
        description: 'Localized transformer trips cause neighborhood blackouts; traffic halts across key urban arterial routes.',
        scientific_classification: 'CONDITIONAL_SECONDARY_RISK',
        evidence_posture: 'BASELINE_ONLY',
        supporting_evidence: ['Municipal emergency logs: Thunderstorm squalls cause extensive localized power outages.'],
        conditions_for_escalation: ['Onset coinciding with evening rush hour'],
        unmonitored_or_unknown: ['Power utility emergency restoration crew dispatch status'],
        field_warning_signs: ['Loss of streetlights and neighborhood power', 'Audible sirens from stalled emergency vehicles'],
        defensive_actions: ['Wait at least 30 minutes after the last thunderclap before resuming outdoor activities', 'Report fallen wires to local electricity board or 112']
      }
    ],
    synthetic_records: 0
  }
};

export const cascadingRiskService = {
  /**
   * Retrieves cascading consequence chain for a region and hazard from the backend.
   * If offline or API fails, returns scientifically verified BASELINE_ONLY physical relationship chain.
   */
  getRegionCascadingRisk: async (
    region: string,
    hazard?: string
  ): Promise<CascadingRiskAssessment> => {
    try {
      const query = hazard ? `?hazard=${encodeURIComponent(hazard)}` : '';
      return await apiClient.get<CascadingRiskAssessment>(
        `/api/future-risk/${encodeURIComponent(region)}/cascading${query}`
      );
    } catch (err) {
      console.warn('Cascading risk API unavailable. Falling back to scientifically established BASELINE_ONLY chain:', err);
      
      const targetHazard = (hazard || 'FLOOD').toUpperCase().trim();
      const chain = BASELINE_FALLBACK_CHAINS[targetHazard] || BASELINE_FALLBACK_CHAINS.FLOOD;

      return {
        region: {
          id: region.toLowerCase().replace(/\s+/g, '-'),
          name: region,
          type: 'STATE'
        },
        primary_hazard: targetHazard,
        evaluated_at: new Date().toISOString(),
        evidence_posture: 'BASELINE_ONLY',
        chains: [chain],
        context_indicators: {
          terrain_slope_vulnerability: 'UNAVAILABLE',
          basin_condition: 'NORMAL',
          river_level_trend: 'UNAVAILABLE',
          is_offline_baseline: true
        },
        synthetic_records: 0
      };
    }
  }
};

export default cascadingRiskService;
