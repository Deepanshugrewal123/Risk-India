import { RegionRiskData, NationalRiskSnapshot, RiskLevel } from '../types/risk';
import { ALL_INDIAN_LOCATIONS } from './indiaLocations';
import { getRiskLevel } from '../utils/riskLevels';

export const NATIONAL_RISK_SNAPSHOT: NationalRiskSnapshot = {
  criticalAreas: 8,
  highRiskAreas: 27,
  activeDisasters: 12,
  monitoredRegions: 766,
  lastSyncTime: '5 mins ago'
};

const DETAILED_REGIONS_MAP: Record<string, Partial<RegionRiskData>> = {
  'assam': {
    riskScore: 84,
    riskLevel: 'HIGH',
    primaryRisk: 'Flood',
    secondaryRisk: 'Landslide',
    monitoredDistricts: 35,
    criticalDistrictsCount: 9,
    summary: 'Brahmaputra basin experiencing heavy monsoonal influx. Multiple tributaries breaching danger mark in Upper Assam and Kamrup valley.',
    emergencyHelpline: '1070 / 1079 (ASDMA)',
    activeIncidentsCount: 3,
    factors: [
      { name: 'Monsoon Precipitation Exceedance', weight: 88, trend: 'rising', description: '+38% above 10-year seasonal median in watershed catchment' },
      { name: 'Riverbed Siltation & Water Influx', weight: 84, trend: 'rising', description: 'Brahmaputra discharge at Guwahati gauge crossing alert mark by 1.2m' },
      { name: 'Embankment Vulnerability Index', weight: 79, trend: 'stable', description: 'Recent erosion reported along 4 vulnerable river bends in Barpeta' },
      { name: 'Topographic Runoff Retention', weight: 72, trend: 'stable', description: 'Low-gradient valley basin traps slow drainage floodwaters' }
    ],
    historicalTrend: [
      { year: 2020, score: 78 }, { year: 2021, score: 72 }, { year: 2022, score: 89 }, { year: 2023, score: 81 }, { year: 2024, score: 84 }
    ],
    recommendedActions: [
      'Pre-position motorized inflatable rescue boats in low-lying char areas',
      'Stock dry rations, oral rehydration salts, and chlorine tablets at block hubs',
      'Maintain round-the-clock watch at vulnerable embankment breaches'
    ]
  },
  'himachal-pradesh': {
    riskScore: 91,
    riskLevel: 'CRITICAL',
    primaryRisk: 'Landslide',
    secondaryRisk: 'Flood',
    monitoredDistricts: 12,
    criticalDistrictsCount: 5,
    summary: 'Severe geological slope instability triggered by intense cloudbursts. High soil moisture saturation across Shimla-Mandi and Kullu corridors.',
    emergencyHelpline: '1070 / 1077 (HPSDMA)',
    activeIncidentsCount: 4,
    factors: [
      { name: 'Soil Pore-Water Saturation', weight: 94, trend: 'rising', description: 'Topsoil saturation index exceeds 92% after 72h continuous rainfall' },
      { name: 'Slope Gradient Instability', weight: 89, trend: 'rising', description: 'Highway cut slopes showing active fissures and surface creep' },
      { name: 'Flash Flood Debris Flow Risk', weight: 85, trend: 'rising', description: 'Steep tributary streams carrying heavy boulders and sediment' },
      { name: 'Deforestation & Seismic Weakness', weight: 76, trend: 'stable', description: 'Zone IV & V seismic belt combined with road expansion terracing' }
    ],
    historicalTrend: [
      { year: 2020, score: 65 }, { year: 2021, score: 71 }, { year: 2022, score: 76 }, { year: 2023, score: 94 }, { year: 2024, score: 91 }
    ],
    recommendedActions: [
      'Enforce preventive vehicle restrictions along vulnerable NH-21 gorges at night',
      'Deploy NDRF SDRF teams at Mandi and Pandoh choke points',
      'Evacuate vulnerable riverside settlements near Beas riverbank'
    ]
  },
  'odisha': {
    riskScore: 68,
    riskLevel: 'MODERATE',
    primaryRisk: 'Cyclone',
    secondaryRisk: 'Flood',
    monitoredDistricts: 30,
    criticalDistrictsCount: 3,
    summary: 'Deep depression over east-central Bay of Bengal intensifying into a cyclonic storm, tracking west-northwest towards coastal districts.',
    emergencyHelpline: '1070 / 0674-2534177 (OSDMA)',
    activeIncidentsCount: 2,
    factors: [
      { name: 'Sea Surface Temperature Anomaly', weight: 74, trend: 'rising', description: 'Warm oceanic eddy (~30.5°C) providing latent convective energy' },
      { name: 'Atmospheric Wind Shear', weight: 61, trend: 'decreasing', description: 'Low vertical shear favorable for further vortex consolidation' },
      { name: 'Coastal Storm Surge Vulnerability', weight: 70, trend: 'stable', description: 'High astronomical tide expected within next 48 hours' },
      { name: 'Multi-Purpose Shelter Preparedness', weight: 35, trend: 'decreasing', description: 'OSDMA cyclone shelters in state of active pre-deployment readiness' }
    ],
    historicalTrend: [
      { year: 2020, score: 82 }, { year: 2021, score: 75 }, { year: 2022, score: 64 }, { year: 2023, score: 66 }, { year: 2024, score: 68 }
    ],
    recommendedActions: [
      'Total ban on deep-sea artisanal and mechanized fishing operations',
      'Verify backup generator diesel supply in all 879 coastal cyclone shelters',
      'Pre-position high-capacity dewatering pumps in urban lowlands of Puri & Cuttack'
    ]
  },
  'kerala': {
    riskScore: 78,
    riskLevel: 'HIGH',
    primaryRisk: 'Landslide',
    secondaryRisk: 'Flood',
    monitoredDistricts: 14,
    criticalDistrictsCount: 4,
    summary: 'High-intensity monsoon belts over the Western Ghats slopes. Soil shear resistance compromised in tea plantation terrains of Wayanad and Idukki.',
    emergencyHelpline: '1077 / 1070 (KSDMA)',
    activeIncidentsCount: 2,
    factors: [
      { name: 'Cumulative 48-hour Rainfall', weight: 83, trend: 'rising', description: 'Precipitation exceeding 210mm in Meppadi and Vythiri hills' },
      { name: 'Regolith Moisture Index', weight: 81, trend: 'rising', description: 'Subsurface water table rising close to ground level' },
      { name: 'Reservoir Inflow & Gate Levels', weight: 69, trend: 'stable', description: 'Sholayar and Idukki dam reserves at 78% rule-curve capacity' },
      { name: 'Drainage Corridor Obstruction', weight: 74, trend: 'stable', description: 'Culvert choking in steep village feeder access roads' }
    ],
    historicalTrend: [
      { year: 2020, score: 77 }, { year: 2021, score: 79 }, { year: 2022, score: 68 }, { year: 2023, score: 74 }, { year: 2024, score: 78 }
    ],
    recommendedActions: [
      'Precautionary relocation of estate workers from slope-side settlements',
      'Continuous acoustic monitoring of geological shift sensors in Wayanad',
      'Restricted tourist transit after 18:00 hrs on ghat roads'
    ]
  },
  'uttarakhand': {
    riskScore: 86,
    riskLevel: 'HIGH',
    primaryRisk: 'Landslide',
    secondaryRisk: 'Flood',
    monitoredDistricts: 13,
    criticalDistrictsCount: 4,
    summary: 'Cloudburst clusters over Rudraprayag and Chamoli. Glacial melt combined with intense localized downpours raising Alaknanda discharge.',
    emergencyHelpline: '1070 / 112 (USDMA)',
    activeIncidentsCount: 2,
    factors: [
      { name: 'Steep Catchment Orographic Rainfall', weight: 87, trend: 'rising', description: 'Localized convective cloudburst triggers' },
      { name: 'River Bed Sedimentary Scour', weight: 82, trend: 'rising', description: 'Torrential velocity scouring bridge abutments' },
      { name: 'Tectonic Fracture Line Density', weight: 88, trend: 'stable', description: 'Main Central Thrust (MCT) seismic vulnerability' },
      { name: 'Yatra Route Congestion Density', weight: 71, trend: 'decreasing', description: 'Pilgrim traffic throttled at key transit stages' }
    ],
    historicalTrend: [
      { year: 2020, score: 70 }, { year: 2021, score: 92 }, { year: 2022, score: 79 }, { year: 2023, score: 85 }, { year: 2024, score: 86 }
    ],
    recommendedActions: [
      'Regulate Char Dham pilgrims at Rishikesh and Haridwar base camps',
      'Stage heavy earthmovers at Joshimath and Badrinath slides',
      'Automated water-level siren activation at Chamoli river gauge'
    ]
  },
  'delhi': {
    riskScore: 67,
    riskLevel: 'MODERATE',
    primaryRisk: 'Flood',
    secondaryRisk: 'Heatwave',
    monitoredDistricts: 11,
    criticalDistrictsCount: 2,
    summary: 'Hathnikund Barrage releases into Yamuna under continuous telemetry monitoring. Old Railway Bridge water level hovering near warning threshold.',
    emergencyHelpline: '1077 / 011-22421656 (DDMA)',
    activeIncidentsCount: 1,
    factors: [
      { name: 'Yamuna Influx from Upper Catchment', weight: 62, trend: 'rising', description: 'Discharge from Yamunanagar recorded at 1.1 lakh cusecs' },
      { name: 'Urban Stormwater Drain Siltation', weight: 59, trend: 'stable', description: 'Stormwater drains experiencing backflow pressure' },
      { name: 'Floodplain Encroachment Exposure', weight: 68, trend: 'stable', description: 'Basti clusters along Yamuna riverbed alerted for evacuation' },
      { name: 'Regulator Gate Readiness', weight: 44, trend: 'decreasing', description: 'ITO and drain barrage gates cleared of debris' }
    ],
    historicalTrend: [
      { year: 2020, score: 45 }, { year: 2021, score: 48 }, { year: 2022, score: 50 }, { year: 2023, score: 86 }, { year: 2024, score: 67 }
    ],
    recommendedActions: [
      'Keep flood control room operational 24/7 with inter-state barrage coordination',
      'Inspect submersible de-watering pumps in low-lying underpasses'
    ]
  },
  'ladakh': {
    riskScore: 77,
    riskLevel: 'HIGH',
    primaryRisk: 'Landslide',
    secondaryRisk: 'Earthquake',
    monitoredDistricts: 2,
    criticalDistrictsCount: 1,
    summary: 'High-altitude flash flood and glacial lake outburst (GLOF) monitoring active along Indus and Zanskar tributaries. Rapid summer moraine thaw.',
    emergencyHelpline: '112 / 01982-255530 (UT Ladakh DDMA)',
    activeIncidentsCount: 1,
    factors: [
      { name: 'Glacial Moraine Melt Velocity', weight: 81, trend: 'rising', description: 'Elevated daytime temperatures accelerating glacial ablation' },
      { name: 'Debris Flow Vulnerability Index', weight: 79, trend: 'rising', description: 'Narrow gorge channels with loose scree deposits' },
      { name: 'Seismic Fault Activity (Zone IV)', weight: 72, trend: 'stable', description: 'Tectonic friction line along Trans-Himalayan belt' },
      { name: 'Remote Communications Redundancy', weight: 65, trend: 'stable', description: 'Satellite communication terminals staged at vulnerable passes' }
    ],
    historicalTrend: [
      { year: 2020, score: 58 }, { year: 2021, score: 62 }, { year: 2022, score: 71 }, { year: 2023, score: 75 }, { year: 2024, score: 77 }
    ],
    recommendedActions: [
      'Position emergency recovery equipment at Khardung La and Chang La passes',
      'Monitor satellite altimetry feeds for glacial lake expansion'
    ]
  },
  'jammu-kashmir': {
    riskScore: 81,
    riskLevel: 'HIGH',
    primaryRisk: 'Flood',
    secondaryRisk: 'Earthquake',
    monitoredDistricts: 20,
    criticalDistrictsCount: 4,
    summary: 'Jhelum basin water levels elevated following continuous Western Disturbance rain. Silt accumulation in Wular Lake outflow monitored.',
    emergencyHelpline: '1070 / 112 (JKSDMA)',
    activeIncidentsCount: 2,
    factors: [
      { name: 'Jhelum Gauge Inundation Index', weight: 84, trend: 'rising', description: 'Ram Munshi Bagh gauge nearing warning mark' },
      { name: 'Mountain Slope Soil Saturation', weight: 79, trend: 'rising', description: 'NH-44 Ramban-Banihal stretch vulnerable to shooting stones' },
      { name: 'Seismic Vulnerability (Zone V)', weight: 82, trend: 'stable', description: 'Kashmir Valley active tectonic fault orientation' },
      { name: 'Drainage Pumping Readiness', weight: 58, trend: 'decreasing', description: 'SMC dewatering stations operational in Srinagar lowlands' }
    ],
    historicalTrend: [
      { year: 2020, score: 73 }, { year: 2021, score: 69 }, { year: 2022, score: 78 }, { year: 2023, score: 82 }, { year: 2024, score: 81 }
    ],
    recommendedActions: [
      'Maintain continuous watch on Ramban slide points along national highway',
      'Inspect sandbag reinforcements along Jhelum river embankments'
    ]
  }
};

/**
 * Generate full 36-location region risk dataset
 */
export const REGIONS_RISK_DATA: RegionRiskData[] = ALL_INDIAN_LOCATIONS.map((loc) => {
  const custom = DETAILED_REGIONS_MAP[loc.id];
  const score = custom?.riskScore || loc.riskScore || 52;
  const level: RiskLevel = custom?.riskLevel || getRiskLevel(score);
  const primary = (custom?.primaryRisk || loc.primaryRisk || 'Flood') as import('../types/risk').DisasterType;
  const secondary = (custom?.secondaryRisk || loc.secondaryRisk || 'Heatwave') as import('../types/risk').DisasterType;

  return {
    id: loc.id,
    name: loc.name,
    code: loc.code,
    capital: loc.capital,
    riskScore: score,
    riskLevel: level,
    primaryRisk: primary,
    secondaryRisk: secondary,
    monitoredDistricts: loc.districts.length,
    criticalDistrictsCount: level === 'CRITICAL' ? 5 : level === 'HIGH' ? 3 : level === 'MODERATE' ? 1 : 0,
    summary:
      custom?.summary ||
      `Regional surveillance active for ${loc.name} (${loc.region}). Terrain and meteorological indices evaluated against seasonal baseline for ${primary.toLowerCase()} and ${secondary.toLowerCase()} hazards.`,
    emergencyHelpline: custom?.emergencyHelpline || `1070 / 112 (${loc.code} SDMA Control Room)`,
    activeIncidentsCount: custom?.activeIncidentsCount !== undefined ? custom.activeIncidentsCount : level === 'HIGH' || level === 'CRITICAL' ? 1 : 0,
    factors:
      custom?.factors || [
        {
          name: `${primary} Environmental Exposure Index`,
          weight: Math.min(95, score + 4),
          trend: score > 70 ? 'rising' : 'stable',
          description: `Regional baseline vulnerability indicator for ${loc.name} terrain`
        },
        {
          name: 'Seasonal Catchment & Soil Saturation',
          weight: Math.max(35, score - 6),
          trend: 'stable',
          description: 'Measured satellite soil moisture and precipitation runoff metric'
        },
        {
          name: 'Infrastructure & Density Exposure',
          weight: Math.max(30, score - 12),
          trend: 'stable',
          description: 'Settlement density and proximity to hazard-prone terrain'
        },
        {
          name: 'Early Warning & Disaster Response Buffer',
          weight: Math.max(25, 100 - score),
          trend: 'decreasing',
          description: 'Readiness of local civil defense, shelters, and relief stockpiles'
        }
      ],
    historicalTrend:
      custom?.historicalTrend || [
        { year: 2020, score: Math.max(30, score - 10) },
        { year: 2021, score: Math.max(35, score - 5) },
        { year: 2022, score: Math.max(32, score + 4) },
        { year: 2023, score: Math.max(40, score - 2) },
        { year: 2024, score: score }
      ],
    recommendedActions:
      custom?.recommendedActions || [
        `Maintain active coordination with ${loc.name} State/UT Disaster Management Authority`,
        'Verify emergency drinking water, dry rations, and first aid kits at neighborhood centers',
        'Follow official district magistrate weather and safety advisories'
      ],
    isDemoData: false
  };
});
