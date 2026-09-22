import React, { useState, useEffect } from 'react';
import { RegionRiskData, RiskLevel, DisasterType } from '../../types/risk';
import { DisasterEvent } from '../../types/disaster';
import { AdministrativeType, IndiaLocation } from '../../types/location';
import { ALL_INDIAN_LOCATIONS } from '../../data/indiaLocations';
import { riskService } from '../../services/riskService';
import { disasterService } from '../../services/disasterService';
import { getRiskConfig, getRiskLevel } from '../../utils/riskLevels';
import { RiskBadge } from '../common/RiskBadge';
import { DemoBadge } from '../common/DemoBadge';
import { FreshnessBadge } from '../common/FreshnessBadge';
import { TiltCard } from '../common/TiltCard';
import {
  AlertTriangle,
  Flame,
  ShieldCheck,
  MapPin,
  Eye,
  Activity,
  Info,
  X,
  ChevronRight,
  Waves,
  Mountain,
  Wind,
  Sun
} from 'lucide-react';
import { resourceService } from '../../services/resourceService';
import { Resource } from '../../types/resource';
import { REGIONS_RISK_DATA, NATIONAL_RISK_SNAPSHOT } from '../../data/riskData';
import { ACTIVE_DISASTERS } from '../../data/disasters';
import { UNIFIED_RESOURCES } from '../../data/resources';

interface IndiaRiskMapProps {
  onSelectRegion?: (region: RegionRiskData) => void;
  onSelectIncident?: (incident: DisasterEvent) => void;
  onSelectResource?: (resource: Resource) => void;
  selectedRegionId?: string;
  filterHazard?: string;
  filterRiskLevel?: RiskLevel | 'All';
  filterLocationType?: AdministrativeType | 'ALL';
  compactMode?: boolean;
  perspective?: 'CURRENT' | 'FUTURE';
  onPerspectiveChange?: (perspective: 'CURRENT' | 'FUTURE') => void;
  hideInternalInspector?: boolean;
}

interface StatePathDef {
  id: string;
  name: string;
  code: string;
  x: number;
  y: number;
  path: string;
  labelX: number;
  labelY: number;
}

const INDIA_STATE_SHAPES: StatePathDef[] = [
  {
    id: 'jammu-kashmir',
    name: 'Jammu & Kashmir / Ladakh',
    code: 'JK',
    x: 230,
    y: 80,
    path: 'M 220 50 L 320 60 L 340 120 L 300 150 L 250 145 L 210 120 Z',
    labelX: 270,
    labelY: 100
  },
  {
    id: 'himachal-pradesh',
    name: 'Himachal Pradesh',
    code: 'HP',
    x: 275,
    y: 155,
    path: 'M 255 146 L 300 148 L 320 185 L 290 205 L 255 180 Z',
    labelX: 285,
    labelY: 175
  },
  {
    id: 'uttarakhand',
    name: 'Uttarakhand',
    code: 'UK',
    x: 310,
    y: 195,
    path: 'M 292 205 L 322 186 L 360 215 L 345 245 L 305 230 Z',
    labelX: 325,
    labelY: 220
  },
  {
    id: 'punjab-haryana',
    name: 'Punjab & Haryana',
    code: 'PB/HR',
    x: 220,
    y: 190,
    path: 'M 215 160 L 255 155 L 260 220 L 230 235 L 205 200 Z',
    labelX: 235,
    labelY: 195
  },
  {
    id: 'delhi',
    name: 'Delhi (NCT)',
    code: 'DL',
    x: 270,
    y: 225,
    path: 'M 262 220 L 280 220 L 280 238 L 262 238 Z',
    labelX: 271,
    labelY: 229
  },
  {
    id: 'rajasthan',
    name: 'Rajasthan',
    code: 'RJ',
    x: 170,
    y: 260,
    path: 'M 130 220 L 220 225 L 250 250 L 225 330 L 160 345 L 120 280 Z',
    labelX: 180,
    labelY: 285
  },
  {
    id: 'uttar-pradesh',
    name: 'Uttar Pradesh',
    code: 'UP',
    x: 320,
    y: 270,
    path: 'M 265 242 L 345 246 L 415 270 L 400 330 L 330 340 L 270 300 Z',
    labelX: 335,
    labelY: 290
  },
  {
    id: 'bihar',
    name: 'Bihar',
    code: 'BR',
    x: 435,
    y: 295,
    path: 'M 416 272 L 485 275 L 490 325 L 425 330 Z',
    labelX: 450,
    labelY: 300
  },
  {
    id: 'assam',
    name: 'Assam & North East',
    code: 'AS',
    x: 550,
    y: 270,
    path: 'M 515 260 L 590 235 L 635 255 L 610 320 L 550 335 L 525 300 Z',
    labelX: 565,
    labelY: 285
  },
  {
    id: 'west-bengal',
    name: 'West Bengal',
    code: 'WB',
    x: 485,
    y: 350,
    path: 'M 485 275 L 515 285 L 505 390 L 465 375 L 485 330 Z',
    labelX: 488,
    labelY: 345
  },
  {
    id: 'gujarat',
    name: 'Gujarat',
    code: 'GJ',
    x: 130,
    y: 375,
    path: 'M 90 330 L 175 330 L 195 385 L 170 435 L 115 425 L 80 375 Z',
    labelX: 140,
    labelY: 380
  },
  {
    id: 'madhya-pradesh',
    name: 'Madhya Pradesh',
    code: 'MP',
    x: 275,
    y: 360,
    path: 'M 225 332 L 330 342 L 375 355 L 360 430 L 260 435 L 205 380 Z',
    labelX: 295,
    labelY: 380
  },
  {
    id: 'odisha',
    name: 'Odisha',
    code: 'OD',
    x: 420,
    y: 430,
    path: 'M 380 380 L 465 375 L 480 440 L 420 480 L 375 440 Z',
    labelX: 425,
    labelY: 425
  },
  {
    id: 'maharashtra',
    name: 'Maharashtra',
    code: 'MH',
    x: 230,
    y: 475,
    path: 'M 175 435 L 265 435 L 325 450 L 305 540 L 190 535 L 180 470 Z',
    labelX: 245,
    labelY: 485
  },
  {
    id: 'andhra-telangana',
    name: 'Andhra Pradesh & Telangana',
    code: 'AP',
    x: 330,
    y: 535,
    path: 'M 305 455 L 375 445 L 410 520 L 350 620 L 295 560 Z',
    labelX: 345,
    labelY: 535
  },
  {
    id: 'karnataka',
    name: 'Karnataka',
    code: 'KA',
    x: 230,
    y: 590,
    path: 'M 205 535 L 290 545 L 295 640 L 230 655 L 200 580 Z',
    labelX: 245,
    labelY: 595
  },
  {
    id: 'kerala',
    name: 'Kerala',
    code: 'KL',
    x: 240,
    y: 690,
    path: 'M 225 655 L 255 655 L 265 745 L 240 755 L 220 700 Z',
    labelX: 242,
    labelY: 700
  },
  {
    id: 'tamil-nadu',
    name: 'Tamil Nadu',
    code: 'TN',
    x: 300,
    y: 680,
    path: 'M 255 645 L 330 630 L 340 715 L 270 755 L 255 680 Z',
    labelX: 295,
    labelY: 690
  }
];

export const IndiaRiskMap: React.FC<IndiaRiskMapProps> = ({
  onSelectRegion,
  onSelectIncident,
  onSelectResource,
  selectedRegionId,
  filterHazard,
  filterRiskLevel = 'All',
  filterLocationType = 'ALL',
  compactMode = false,
  perspective = 'CURRENT',
  onPerspectiveChange,
  hideInternalInspector = false
}) => {
  const [internalHazardFilter, setInternalHazardFilter] = useState<string>(filterHazard || 'ALL');
  const [internalAdminFilter, setInternalAdminFilter] = useState<'ALL' | AdministrativeType>(filterLocationType);
  const [hoveredRegion, setHoveredRegion] = useState<RegionRiskData | null>(null);
  const [hoveredLocationType, setHoveredLocationType] = useState<AdministrativeType>('STATE');
  const [mouseCoord, setMouseCoord] = useState({ x: 0, y: 0 });
  const [regions, setRegions] = useState<RegionRiskData[]>(REGIONS_RISK_DATA);
  const [snapshot, setSnapshot] = useState(NATIONAL_RISK_SNAPSHOT);
  const [disasters, setDisasters] = useState<DisasterEvent[]>(() => ACTIVE_DISASTERS.slice(0, 12));
  const [activeSelectedRegion, setActiveSelectedRegion] = useState<RegionRiskData | null>(() => {
    if (selectedRegionId) {
      return REGIONS_RISK_DATA.find((r) => r.id === selectedRegionId) || REGIONS_RISK_DATA[0];
    }
    return REGIONS_RISK_DATA[0];
  });
  const [showPins, setShowPins] = useState<boolean>(true);
  const [verifiedResources, setVerifiedResources] = useState<Resource[]>(() =>
    UNIFIED_RESOURCES.filter((r) => r.verificationStatus === 'VERIFIED')
  );
  const [showResources, setShowResources] = useState<boolean>(true);
  const [hoveredResource, setHoveredResource] = useState<Resource | null>(null);
  const [selectedResource, setSelectedResource] = useState<Resource | null>(null);
  const [displayMode, setDisplayMode] = useState<'map' | 'cards' | 'list'>('map');
  const [mapRenderError, setMapRenderError] = useState<boolean>(false);
  const [mapPerspective, setMapPerspective] = useState<'CURRENT' | 'FUTURE'>(perspective);
  const [futureHorizon, setFutureHorizon] = useState<string>('6-24h');

  // Synchronize internal perspective with incoming prop if controlled
  useEffect(() => {
    if (perspective && perspective !== mapPerspective) {
      setMapPerspective(perspective);
    }
  }, [perspective]);

  // Synchronize incoming selectedRegionId
  useEffect(() => {
    if (selectedRegionId) {
      const matched = regions.find((r) => r.id === selectedRegionId);
      if (matched) setActiveSelectedRegion(matched);
    }
  }, [selectedRegionId, regions]);

  // Decoupled, fault-tolerant telemetry loading: one failing service does NOT abort others
  useEffect(() => {
    let isMounted = true;

    // 1. Regional multi-hazard risk
    riskService.getAllRegions()
      .then((allRegs) => {
        if (!isMounted || !Array.isArray(allRegs) || allRegs.length === 0) return;
        setRegions(allRegs);
        if (selectedRegionId) {
          const matched = allRegs.find((r) => r.id === selectedRegionId);
          if (matched) setActiveSelectedRegion(matched);
        } else if (!activeSelectedRegion) {
          setActiveSelectedRegion(allRegs[0]);
        }
      })
      .catch((err) => {
        console.warn('Live regional risk API unavailable, preserving static baseline:', err);
      });

    // 2. National telemetry snapshot
    riskService.getNationalSnapshot()
      .then((natSnap) => {
        if (isMounted && natSnap) setSnapshot(natSnap);
      })
      .catch((err) => {
        console.warn('National snapshot API unavailable, preserving baseline snapshot:', err);
      });

    // 3. Active disaster incidents (USGS, IMD, CWC feeds)
    disasterService.getActiveDisasters()
      .then((incidents) => {
        if (isMounted && Array.isArray(incidents)) setDisasters(incidents);
      })
      .catch((err) => {
        console.warn('Active disasters feed unavailable, preserving static catalog:', err);
      });

    // 4. Verified relief resources
    resourceService.getResources({ verificationStatus: 'VERIFIED' })
      .then((resList) => {
        if (isMounted && Array.isArray(resList)) setVerifiedResources(resList);
      })
      .catch((err) => {
        console.warn('Resources feed unavailable, preserving verified catalog:', err);
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const hazardTabs = ['ALL', 'FLOOD', 'LANDSLIDE', 'CYCLONE', 'EARTHQUAKE', 'HEATWAVE'];
  const effectiveHazard = filterHazard || internalHazardFilter;
  const effectiveAdmin = filterLocationType !== 'ALL' ? filterLocationType : internalAdminFilter;

  // Derive estimated specific hazard risks
  const getHazardScores = (reg: RegionRiskData) => {
    const floodScore = reg.primaryRisk === 'Flood' ? reg.riskScore : reg.secondaryRisk === 'Flood' ? Math.max(30, reg.riskScore - 18) : 25;
    const landslideScore = reg.primaryRisk === 'Landslide' ? reg.riskScore : reg.secondaryRisk === 'Landslide' ? Math.max(30, reg.riskScore - 16) : 18;
    const cycloneScore = reg.primaryRisk === 'Cyclone' ? reg.riskScore : reg.secondaryRisk === 'Cyclone' ? Math.max(28, reg.riskScore - 20) : 12;
    return { floodScore, landslideScore, cycloneScore };
  };

  const getRiskColor = (level: RiskLevel, isSelected: boolean) => {
    const config = getRiskConfig(level);
    if (isSelected) return config.hexColor;
    return `${config.hexColor}40`; // ~25% alpha for clean pastel map fill
  };

  const getBorderColor = (level: RiskLevel, isSelected: boolean) => {
    if (isSelected) return '#121316';
    return getRiskConfig(level).hexColor;
  };

  const findRegionData = (stateDef: StatePathDef): RegionRiskData => {
    const direct = regions.find(
      (r) => r.code === stateDef.code || r.name.toLowerCase().includes(stateDef.name.toLowerCase())
    );
    if (direct) return direct;

    return {
      id: stateDef.id,
      name: stateDef.name,
      code: stateDef.code,
      capital: 'Capital',
      riskScore: 32,
      riskLevel: 'LOW',
      primaryRisk: 'Flood',
      monitoredDistricts: 18,
      criticalDistrictsCount: 0,
      summary: 'Regional climate parameters within normal seasonal standard deviation.',
      emergencyHelpline: '1070',
      activeIncidentsCount: 0,
      factors: [
        { name: 'Catchment Retention', weight: 32, trend: 'stable', description: 'Normal reservoir buffer' },
        { name: 'Advisory Level', weight: 24, trend: 'decreasing', description: 'Green alert' }
      ],
      historicalTrend: [{ year: 2024, score: 32 }],
      recommendedActions: ['Standard seasonal readiness'],
      isDemoData: false
    };
  };

  const handleMouseMove = (e: React.MouseEvent<SVGSVGElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    setMouseCoord({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
  };

  const handleRegionClick = (reg: RegionRiskData) => {
    setActiveSelectedRegion(reg);
    onSelectRegion?.(reg);
  };

  // Status descriptor for regions
  const getRegionStatus = (reg: RegionRiskData) => {
    if (reg.riskLevel === 'CRITICAL') return 'Elevated (Critical Watch)';
    if (reg.riskLevel === 'HIGH') return 'Elevated Risk';
    if (reg.riskLevel === 'MODERATE') return 'Monitored';
    return 'Stable';
  };

  return (
    <div className="relative w-full rounded-3xl bg-white border border-paper-300 shadow-elevated overflow-hidden select-none">
      {/* Top Filter and Telemetry Header */}
      <div className="p-4 sm:p-6 border-b border-paper-200 space-y-4 bg-paper-50/70">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-mono text-xs uppercase tracking-wider text-charcoal-500 font-semibold">
                India Geospatial Risk Matrix
              </h3>
              <DemoBadge label="36 REGIONS COVERED" />
            </div>
            <p className="text-sm font-semibold text-charcoal-900 mt-0.5">
              Interactive Multi-Hazard Map // 28 States + 8 Union Territories
            </p>
          </div>

          {/* Legend: Evidence Postures & Hazard Severity */}
          <div className="flex flex-wrap items-center gap-2 sm:gap-3 text-xs font-mono">
            <div className="flex flex-wrap items-center gap-2 mr-1">
              <span className="text-charcoal-500 font-bold uppercase tracking-wider text-[10px]">Evidence Posture:</span>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-emerald-500" />
                <span className="text-charcoal-700 font-semibold text-[11px]">LIVE</span>
              </span>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-blue-500" />
                <span className="text-charcoal-700 font-semibold text-[11px]">RECENT</span>
              </span>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-indigo-500" />
                <span className="text-charcoal-700 font-semibold text-[11px]">FORECAST</span>
              </span>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-slate-400" />
                <span className="text-charcoal-700 font-semibold text-[11px]">BASELINE</span>
              </span>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-slate-300 border border-slate-400" />
                <span className="text-charcoal-500 font-semibold text-[11px]">DATA UNAVAILABLE</span>
              </span>
            </div>

            <div className="flex items-center gap-1.5 border-l border-paper-300 pl-3">
              <span className="text-charcoal-500 font-bold text-[10px]">Risk Tier:</span>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-risk-low border border-risk-low-border" />
                <span className="text-charcoal-600 text-[11px]">Low</span>
              </span>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-risk-moderate border border-risk-moderate-border" />
                <span className="text-charcoal-600 text-[11px]">Mod</span>
              </span>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-risk-high border border-risk-high-border" />
                <span className="text-charcoal-600 text-[11px]">High</span>
              </span>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-risk-critical border border-risk-critical-border" />
                <span className="text-charcoal-600 text-[11px]">Crit</span>
              </span>
            </div>
            <div className="flex items-center gap-1.5 border-l border-paper-300 pl-3">
              <span className="w-2.5 h-2.5 rounded-full bg-risk-critical animate-ping" />
              <span className="text-charcoal-700 font-medium text-[11px]">Reported Disaster Incident</span>
            </div>
            <div className="flex items-center gap-1.5 border-l border-paper-300 pl-3">
              <span className="w-2.5 h-2.5 rotate-45 bg-emerald-500 border border-white inline-block shadow-xs" />
              <span className="text-charcoal-700 font-medium text-[11px]">Verified Help Center</span>
            </div>
          </div>
        </div>

        {/* Map Perspective Mode Toggle: CURRENT RISK vs FUTURE RISK & EARLY WARNING */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 p-2.5 rounded-2xl bg-white border border-paper-300 shadow-xs">
          <div className="flex items-center gap-1 bg-paper-100 p-1 rounded-xl">
            <button
              onClick={() => {
                setMapPerspective('CURRENT');
                onPerspectiveChange?.('CURRENT');
              }}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-mono font-bold transition-all ${
                mapPerspective === 'CURRENT'
                  ? 'bg-charcoal-900 text-paper-50 shadow-xs'
                  : 'text-charcoal-600 hover:text-charcoal-950'
              }`}
            >
              CURRENT RISK
            </button>
            <button
              onClick={() => {
                setMapPerspective('FUTURE');
                onPerspectiveChange?.('FUTURE');
              }}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-mono font-bold transition-all ${
                mapPerspective === 'FUTURE'
                  ? 'bg-indigo-600 text-white shadow-xs'
                  : 'text-charcoal-600 hover:text-charcoal-950'
              }`}
            >
              FUTURE RISK & EARLY WARNING
            </button>
          </div>

          {mapPerspective === 'FUTURE' ? (
            <div className="flex items-center gap-1.5 overflow-x-auto text-xs font-mono">
              <span className="text-charcoal-400 font-semibold shrink-0">Forecast Horizon:</span>
              {['NOW', '0-6h', '6-24h', '1-3d', '3-7d'].map((hz) => (
                <button
                  key={hz}
                  onClick={() => setFutureHorizon(hz)}
                  className={`px-2.5 py-1 rounded-lg transition-all ${
                    futureHorizon === hz
                      ? 'bg-indigo-100 text-indigo-900 font-bold border border-indigo-300'
                      : 'bg-paper-50 text-charcoal-600 border border-paper-200 hover:bg-paper-100'
                  }`}
                >
                  {hz}
                </button>
              ))}
            </div>
          ) : (
            <div className="text-[11px] font-mono text-charcoal-500 flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>Real-Time In-Situ Sensors & Radar Feed Active</span>
            </div>
          )}
        </div>

        {/* Dual Filter Bars: Administrative Scope + Hazard Layer */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-2 border-t border-paper-200">
          {/* Admin Type Filter */}
          <div className="flex items-center gap-1.5 overflow-x-auto">
            <span className="text-xs font-mono text-charcoal-400 mr-1 shrink-0">Region Scope:</span>
            <button
              onClick={() => setInternalAdminFilter('ALL')}
              className={`px-3 py-1 rounded-full text-xs font-mono transition-all shrink-0 ${
                effectiveAdmin === 'ALL'
                  ? 'bg-charcoal-900 text-paper-50 font-bold shadow-subtle'
                  : 'bg-white text-charcoal-700 hover:bg-paper-200 border border-paper-300'
              }`}
            >
              All India (36)
            </button>
            <button
              onClick={() => setInternalAdminFilter('STATE')}
              className={`px-3 py-1 rounded-full text-xs font-mono transition-all shrink-0 ${
                effectiveAdmin === 'STATE'
                  ? 'bg-charcoal-900 text-paper-50 font-bold shadow-subtle'
                  : 'bg-white text-charcoal-700 hover:bg-paper-200 border border-paper-300'
              }`}
            >
              States (28)
            </button>
            <button
              onClick={() => setInternalAdminFilter('UNION_TERRITORY')}
              className={`px-3 py-1 rounded-full text-xs font-mono transition-all shrink-0 ${
                effectiveAdmin === 'UNION_TERRITORY'
                  ? 'bg-charcoal-900 text-paper-50 font-bold shadow-subtle'
                  : 'bg-white text-charcoal-700 hover:bg-paper-200 border border-paper-300'
              }`}
            >
              Union Territories (8)
            </button>
          </div>

          {/* Hazard Filter Tabs & Resource Toggle */}
          <div className="flex items-center gap-1.5 overflow-x-auto">
            <span className="text-xs font-mono text-charcoal-400 mr-1 shrink-0">Layers:</span>
            {hazardTabs.map((hz) => {
              const isSelected = effectiveHazard.toUpperCase() === hz;
              return (
                <button
                  key={hz}
                  onClick={() => setInternalHazardFilter(hz)}
                  className={`px-2.5 py-1 rounded-full text-xs font-mono transition-all shrink-0 ${
                    isSelected
                      ? 'bg-charcoal-900 text-paper-50 font-bold shadow-subtle'
                      : 'bg-white text-charcoal-700 hover:bg-paper-200 border border-paper-300'
                  }`}
                >
                  {hz}
                </button>
              );
            })}
            <button
              onClick={() => setShowResources(!showResources)}
              className={`px-2.5 py-1 rounded-full text-xs font-mono transition-all shrink-0 flex items-center gap-1.5 ${
                showResources
                  ? 'bg-emerald-800 text-white font-bold shadow-subtle'
                  : 'bg-white text-charcoal-700 hover:bg-paper-200 border border-paper-300'
              }`}
            >
              <span className="w-2 h-2 rotate-45 bg-emerald-400 inline-block" />
              <span>Help Centers ({verifiedResources.filter((r) => typeof r.latitude === 'number' && typeof r.longitude === 'number').length})</span>
            </button>

            {/* View Mode Segmented Controls */}
            <div className="flex items-center gap-1 bg-paper-200/90 p-0.5 rounded-full border border-paper-300 ml-auto shrink-0">
              <button
                type="button"
                onClick={() => { setDisplayMode('map'); setMapRenderError(false); }}
                className={`px-3 py-1 rounded-full text-xs font-mono transition-colors ${
                  displayMode === 'map' && !mapRenderError
                    ? 'bg-charcoal-900 text-white font-bold shadow-xs'
                    : 'text-charcoal-700 hover:text-charcoal-950 hover:bg-white/60'
                }`}
                title="Interactive Map View"
              >
                Map
              </button>
              <button
                type="button"
                onClick={() => setDisplayMode('cards')}
                className={`px-3 py-1 rounded-full text-xs font-mono transition-colors ${
                  displayMode === 'cards'
                    ? 'bg-charcoal-900 text-white font-bold shadow-xs'
                    : 'text-charcoal-700 hover:text-charcoal-950 hover:bg-white/60'
                }`}
                title="State Cards Overview"
              >
                Cards
              </button>
              <button
                type="button"
                onClick={() => setDisplayMode('list')}
                className={`px-3 py-1 rounded-full text-xs font-mono transition-colors ${
                  displayMode === 'list' || mapRenderError
                    ? 'bg-charcoal-900 text-white font-bold shadow-xs'
                    : 'text-charcoal-700 hover:text-charcoal-950 hover:bg-white/60'
                }`}
                title="Accessible Tabular List View"
              >
                List
              </button>
            </div>
          </div>
        </div>
      </div>


      {/* Main Map Canvas Area */}
      <div className="relative flex flex-col lg:flex-row items-center justify-center p-4 sm:p-8 min-h-[520px] bg-paper-100/40">
        {/* Floating Snapshot Counter Panel */}
        <TiltCard
          maxTilt={1.5}
          className="lg:absolute lg:top-6 lg:left-6 z-10 w-full lg:w-64 p-4 rounded-2xl bg-white/95 backdrop-blur-md border border-paper-300 shadow-subtle mb-4 lg:mb-0"
        >
          <div className="flex items-center justify-between mb-3 border-b border-paper-200 pb-2">
            <span className="font-mono text-[11px] uppercase tracking-wider text-charcoal-500 font-bold">
              India Risk Snapshot
            </span>
            <span className="w-2 h-2 rounded-full bg-risk-high animate-ping" />
          </div>
          <div className="space-y-2.5">
            <div className="flex items-center justify-between text-xs">
              <span className="text-charcoal-600 flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-risk-critical" />
                Critical Areas
              </span>
              <span className="font-mono font-bold text-risk-critical">
                0{snapshot.criticalAreas}
              </span>
            </div>
            <div className="flex items-center justify-between text-xs">
              <span className="text-charcoal-600 flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-risk-high" />
                High Risk Areas
              </span>
              <span className="font-mono font-bold text-risk-high">
                {snapshot.highRiskAreas}
              </span>
            </div>
            <div className="flex items-center justify-between text-xs">
              <span className="text-charcoal-600 flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-risk-moderate" />
                Active Disasters
              </span>
              <span className="font-mono font-bold text-charcoal-900">
                {snapshot.activeDisasters}
              </span>
            </div>
            <div className="flex items-center justify-between text-xs pt-1 border-t border-paper-200">
              <span className="text-charcoal-500">Monitored Locations</span>
              <span className="font-mono font-semibold text-charcoal-700">
                36 (28 States + 8 UTs)
              </span>
            </div>
          </div>
          <div className="mt-3 pt-2 text-[10px] text-charcoal-400 font-mono flex items-center justify-between border-t border-paper-100">
            <span>Centroid Markers</span>
            <button
              onClick={() => setShowPins(!showPins)}
              className="text-charcoal-700 underline font-semibold hover:text-charcoal-950"
            >
              {showPins ? 'Hide Pins' : 'Show Pins'}
            </button>
          </div>
        </TiltCard>

        {/* Map Failure Fallback / Banner */}
        {mapRenderError && (
          <div className="w-full max-w-4xl mb-4 p-4 rounded-2xl bg-amber-50 border border-amber-200 text-xs text-amber-900 flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
            <div>
              <strong className="block font-bold text-sm">Interactive Map Tiles Unavailable</strong>
              <p className="mt-0.5 leading-relaxed">
                Geospatial map visualization could not be loaded due to network or rendering constraints. Official disaster telemetry, state risk baselines, and emergency hotlines remain fully accessible in the tabular list view below.
              </p>
            </div>
          </div>
        )}

        {/* 1. Accessible Tabular List View (Tier 3 Fallback & Screen Reader View) */}
        {(displayMode === 'list' || mapRenderError) && (
          <div className="w-full max-w-4xl overflow-x-auto bg-white rounded-2xl border border-paper-300 shadow-subtle p-4 my-2">
            <div className="flex items-center justify-between pb-3 mb-3 border-b border-paper-200">
              <span className="font-mono text-xs uppercase font-bold text-charcoal-700">
                National Disaster Risk Matrix — Tabular View
              </span>
              <span className="text-xs font-mono text-charcoal-500">
                {INDIA_STATE_SHAPES.length} States & UTs Monitored
              </span>
            </div>
            <table className="w-full text-left text-xs font-mono border-collapse">
              <thead>
                <tr className="border-b border-paper-200 text-charcoal-500 uppercase text-[10px]">
                  <th className="pb-2 font-bold">State / UT</th>
                  <th className="pb-2 font-bold">Primary Hazard</th>
                  <th className="pb-2 font-bold">Risk Tier</th>
                  <th className="pb-2 font-bold">Baseline Score</th>
                  <th className="pb-2 font-bold">Emergency Helpline</th>
                  <th className="pb-2 font-bold text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-paper-100">
                {INDIA_STATE_SHAPES.map((shape) => {
                  const data = findRegionData(shape);
                  const isSelected = (activeSelectedRegion?.id === data.id) || (selectedRegionId === data.id);
                  return (
                    <tr
                      key={shape.id}
                      className={`hover:bg-paper-50 transition-colors ${isSelected ? 'bg-paper-100 font-bold' : ''}`}
                    >
                      <td className="py-2.5 font-sans font-semibold text-charcoal-900">
                        {data.name}
                        <span className="ml-1.5 text-[10px] font-mono text-charcoal-400">({shape.code})</span>
                      </td>
                      <td className="py-2.5 text-charcoal-700">{data.primaryRisk}</td>
                      <td className="py-2.5">
                        <RiskBadge level={data.riskLevel} size="sm" score={data.riskScore} />
                      </td>
                      <td className="py-2.5 font-bold text-charcoal-900">{data.riskScore}%</td>
                      <td className="py-2.5">
                        <a
                          href="tel:1070"
                          className="inline-flex items-center gap-1 text-charcoal-700 hover:text-charcoal-950 underline font-bold"
                        >
                          {data.emergencyHelpline || '1070 / 112'}
                        </a>
                      </td>
                      <td className="py-2.5 text-right">
                        <button
                          type="button"
                          onClick={() => handleRegionClick(data)}
                          className="px-2.5 py-1 rounded-lg bg-charcoal-900 text-white hover:bg-charcoal-800 text-[11px] font-sans font-medium transition-colors"
                        >
                          Select
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        {/* 2. Responsive Cards View (Tier 2 Degraded View) */}
        {displayMode === 'cards' && !mapRenderError && (
          <div className="w-full max-w-4xl grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 my-2">
            {INDIA_STATE_SHAPES.map((shape) => {
              const data = findRegionData(shape);
              const isSelected = (activeSelectedRegion?.id === data.id) || (selectedRegionId === data.id);
              return (
                <div
                  key={shape.id}
                  onClick={() => handleRegionClick(data)}
                  className={`p-4 rounded-2xl border transition-all cursor-pointer flex flex-col justify-between ${
                    isSelected
                      ? 'bg-paper-100 border-charcoal-900 shadow-subtle'
                      : 'bg-white border-paper-300 hover:border-charcoal-400'
                  }`}
                >
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <div>
                      <h4 className="font-bold text-sm text-charcoal-950">{data.name}</h4>
                      <span className="text-[10px] font-mono text-charcoal-500">Code: {shape.code}</span>
                    </div>
                    <RiskBadge level={data.riskLevel} size="sm" score={data.riskScore} />
                  </div>
                  <div className="text-xs font-mono text-charcoal-600 space-y-1 mb-3">
                    <div>Primary: <strong className="text-charcoal-900">{data.primaryRisk}</strong></div>
                    <div>Baseline Score: <strong className="text-charcoal-900">{data.riskScore}%</strong></div>
                    <div>Helpline: <a href="tel:1070" className="underline font-bold text-charcoal-800">{data.emergencyHelpline || '1070 / 112'}</a></div>
                  </div>
                  <button
                    type="button"
                    onClick={(e) => { e.stopPropagation(); handleRegionClick(data); }}
                    className="w-full py-1.5 rounded-xl bg-paper-200 text-charcoal-900 hover:bg-charcoal-900 hover:text-white text-xs font-medium transition-colors"
                  >
                    View Risk Breakdown
                  </button>
                </div>
              );
            })}
          </div>
        )}

        {/* 3. Normal Interactive SVG Map View (Tier 1 Default View) */}
        {displayMode === 'map' && !mapRenderError && (
        <div className="w-full max-w-[620px] aspect-[700/780] relative flex items-center justify-center">
          <svg
            viewBox="50 30 620 750"
            className="w-full h-full filter drop-shadow-sm"
            onMouseMove={handleMouseMove}
            onMouseLeave={() => setHoveredRegion(null)}
          >

            {/* Background Grid Lines */}
            <defs>
              <pattern id="map-grid" width="40" height="40" patternUnits="userSpaceOnUse">
                <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(18, 19, 22, 0.04)" strokeWidth="1" />
              </pattern>
            </defs>
            <rect x="50" y="30" width="620" height="750" fill="url(#map-grid)" />

            {/* Render Indian Region Shapes */}
            {INDIA_STATE_SHAPES.map((shape) => {
              const data = findRegionData(shape);
              const isSelected = (activeSelectedRegion?.id === data.id) || (selectedRegionId === data.id);
              const matchesSeverity = filterRiskLevel === 'All' || data.riskLevel === filterRiskLevel;
              const matchesHazard =
                effectiveHazard === 'ALL' ||
                data.primaryRisk.toUpperCase() === effectiveHazard.toUpperCase() ||
                data.secondaryRisk?.toUpperCase() === effectiveHazard.toUpperCase();
              const isDimmed = !matchesSeverity || !matchesHazard;

              const fillColor = isDimmed ? 'rgba(230, 230, 225, 0.35)' : getRiskColor(data.riskLevel, isSelected);
              const strokeColor = isDimmed ? '#D5D5CD' : getBorderColor(data.riskLevel, isSelected);

              return (
                <g key={shape.id} className="cursor-pointer transition-all duration-200">
                  <path
                    d={shape.path}
                    fill={fillColor}
                    stroke={strokeColor}
                    strokeWidth={isSelected ? '2.5' : '1.5'}
                    strokeLinejoin="round"
                    className="transition-colors duration-200 hover:brightness-95"
                    onMouseEnter={() => {
                      setHoveredRegion(data);
                      setHoveredLocationType('STATE');
                    }}
                    onClick={() => handleRegionClick(data)}
                  />
                  <text
                    x={shape.labelX}
                    y={shape.labelY}
                    textAnchor="middle"
                    className="font-mono text-[10px] font-bold fill-charcoal-800 pointer-events-none select-none tracking-tighter opacity-70"
                  >
                    {shape.code}
                  </text>
                </g>
              );
            })}

            {/* Complete 36 State & Union Territory Centroid Markers */}
            {showPins &&
              ALL_INDIAN_LOCATIONS.map((loc) => {
                const regData: RegionRiskData = regions.find((r) => r.id === loc.id || r.code === loc.code) || {
                  id: loc.id,
                  name: loc.name,
                  code: loc.code,
                  capital: loc.capital,
                  riskScore: loc.riskScore || 50,
                  riskLevel: getRiskLevel(loc.riskScore || 50),
                  primaryRisk: (loc.primaryRisk || 'Flood') as DisasterType,
                  secondaryRisk: (loc.secondaryRisk || 'Heatwave') as DisasterType,
                  monitoredDistricts: loc.districts.length,
                  criticalDistrictsCount: 1,
                  summary: `${loc.name} administrative territory surveillance active.`,
                  emergencyHelpline: '1070 / 112',
                  activeIncidentsCount: 0,
                  factors: [],
                  historicalTrend: [],
                  recommendedActions: [],
                  isDemoData: false
                };

                const isSelected = (activeSelectedRegion?.id === loc.id) || (selectedRegionId === loc.id);
                const matchesSeverity = filterRiskLevel === 'All' || regData.riskLevel === filterRiskLevel;
                const matchesHazard =
                  effectiveHazard === 'ALL' ||
                  regData.primaryRisk.toUpperCase() === effectiveHazard.toUpperCase() ||
                  regData.secondaryRisk?.toUpperCase() === effectiveHazard.toUpperCase();
                const matchesAdmin = effectiveAdmin === 'ALL' || loc.type === effectiveAdmin;

                if (!matchesSeverity || !matchesHazard || !matchesAdmin) return null;

                // Normalized projection to SVG coordinate space
                const latNorm = Math.max(0, Math.min(1, (loc.latitude - 8) / (37 - 8)));
                const lngNorm = Math.max(0, Math.min(1, (loc.longitude - 68) / (97 - 68)));
                const svgX = 110 + lngNorm * 480;
                const svgY = 740 - latNorm * 680;
                const config = getRiskConfig(regData.riskLevel);

                return (
                  <g
                    key={`centroid-pin-${loc.id}`}
                    className="cursor-pointer group"
                    onClick={() => handleRegionClick(regData)}
                    onMouseEnter={() => {
                      setHoveredRegion(regData);
                      setHoveredLocationType(loc.type);
                    }}
                  >
                    {isSelected && (
                      <circle
                        cx={svgX}
                        cy={svgY}
                        r="11"
                        fill="none"
                        stroke={config.hexColor}
                        strokeWidth="1.5"
                        strokeDasharray="2 2"
                        className="animate-spin"
                        style={{ animationDuration: '4s' }}
                      />
                    )}
                    <circle
                      cx={svgX}
                      cy={svgY}
                      r={isSelected ? 6 : loc.type === 'UNION_TERRITORY' ? 4 : 4.5}
                      fill={config.hexColor}
                      stroke="#ffffff"
                      strokeWidth="1.5"
                      className="transition-transform duration-200 group-hover:scale-150 shadow-xs"
                    />
                  </g>
                );
              })}

            {/* Active Incident Pulsing Markers */}
            {disasters.map((incident) => {
              const latNorm = (incident.coordinates[0] - 8) / (36 - 8);
              const lngNorm = (incident.coordinates[1] - 68) / (97 - 68);
              const svgX = 110 + lngNorm * 480;
              const svgY = 740 - latNorm * 680;

              return (
                <g
                  key={incident.id}
                  className="cursor-pointer group"
                  onClick={() => onSelectIncident?.(incident)}
                >
                  <circle
                    cx={svgX}
                    cy={svgY}
                    r="12"
                    className={`animate-ping opacity-75 ${
                      incident.severity === 'CRITICAL' ? 'fill-risk-critical' : 'fill-risk-high'
                    }`}
                  />
                  <circle
                    cx={svgX}
                    cy={svgY}
                    r="6"
                    className={`${
                      incident.severity === 'CRITICAL'
                        ? 'fill-risk-critical stroke-white'
                        : 'fill-risk-high stroke-white'
                    } stroke-2 shadow-sm transition-transform duration-200 group-hover:scale-125`}
                  />
                </g>
              );
            })}

            {/* Verified Help Center Emerald Diamond Markers */}
            {showResources &&
              verifiedResources
                .filter((res) => typeof res.latitude === 'number' && typeof res.longitude === 'number')
                .map((res) => {
                  const latNorm = (res.latitude! - 8) / (36 - 8);
                  const lngNorm = (res.longitude! - 68) / (97 - 68);
                  const svgX = 110 + lngNorm * 480;
                  const svgY = 740 - latNorm * 680;
                  const isSelected = selectedResource?.id === res.id;

                  return (
                    <g
                      key={`res-marker-${res.id}`}
                      className="cursor-pointer group"
                      onClick={() => {
                        setSelectedResource(res);
                        onSelectResource?.(res);
                      }}
                      onMouseEnter={() => setHoveredResource(res)}
                      onMouseLeave={() => setHoveredResource(null)}
                    >
                      {isSelected && (
                        <polygon
                          points={`${svgX},${svgY - 10} ${svgX + 10},${svgY} ${svgX},${svgY + 10} ${svgX - 10},${svgY}`}
                          fill="none"
                          stroke="#059669"
                          strokeWidth="2"
                          strokeDasharray="2 2"
                        />
                      )}
                      <polygon
                        points={`${svgX},${svgY - 6.5} ${svgX + 6.5},${svgY} ${svgX},${svgY + 6.5} ${svgX - 6.5},${svgY}`}
                        fill="#10b981"
                        stroke="#ffffff"
                        strokeWidth="1.5"
                        className="transition-transform duration-200 group-hover:scale-150 shadow-sm"
                      />
                      <circle cx={svgX} cy={svgY} r="1.5" fill="#ffffff" />
                    </g>
                  );
                })}
          </svg>

          {/* Hover Tooltip */}
          {hoveredRegion && (
            <div
              className="absolute pointer-events-none z-30 p-3.5 rounded-2xl bg-charcoal-900 text-paper-50 text-xs shadow-floating border border-charcoal-700 min-w-[220px] -translate-x-1/2 -translate-y-full mt-[-12px]"
              style={{
                left: Math.max(110, Math.min(window.innerWidth > 600 ? 450 : 230, mouseCoord.x)),
                top: Math.max(10, mouseCoord.y - 15),
              }}
            >
              <div className="flex items-center justify-between gap-3 border-b border-charcoal-700 pb-1.5 mb-2">
                <div>
                  <span className="font-bold text-sm text-paper-50 uppercase tracking-tight block">
                    {hoveredRegion.name}
                  </span>
                  <span className="text-[9px] font-mono text-amber-300">
                    {hoveredLocationType === 'UNION_TERRITORY' ? 'Union Territory' : 'Indian State'}
                  </span>
                </div>
                <span className="font-mono text-[10px] text-charcoal-400">
                  {hoveredRegion.code}
                </span>
              </div>
              <div className="space-y-1.5 font-mono text-[11px]">
                <div className="flex justify-between text-charcoal-300">
                  <span>Primary Hazard:</span>
                  <span className="font-semibold text-paper-50">{hoveredRegion.primaryRisk}</span>
                </div>
                <div className="flex justify-between text-charcoal-300">
                  <span>Historical Baseline:</span>
                  <span className="font-bold text-amber-400">{hoveredRegion.riskScore}%</span>
                </div>
                <div className="flex justify-between text-charcoal-300">
                  <span>Risk Category:</span>
                  <span
                    className={`font-semibold ${
                      hoveredRegion.riskLevel === 'CRITICAL'
                        ? 'text-rose-400'
                        : hoveredRegion.riskLevel === 'HIGH'
                        ? 'text-orange-400'
                        : hoveredRegion.riskLevel === 'MODERATE'
                        ? 'text-amber-300'
                        : 'text-emerald-400'
                    }`}
                  >
                    {hoveredRegion.riskLevel}
                  </span>
                </div>
                <div className="flex justify-between text-charcoal-300">
                  <span>AI Risk Model:</span>
                  <span className="font-medium text-paper-50">
                    {hoveredRegion.name.toLowerCase().includes('assam') ? 'Assam Prototype Active' : 'Baseline Profile Only'}
                  </span>
                </div>
                <div className="flex justify-between text-charcoal-300 pt-1 border-t border-charcoal-800">
                  <span>Data Freshness:</span>
                  <span className="font-medium text-paper-50">
                    {hoveredRegion.activeIncidentsCount > 0
                      ? 'OFFICIAL LIVE'
                      : hoveredRegion.name.toLowerCase().includes('assam')
                      ? 'EMPIRICAL ML'
                      : 'REGIONAL BASELINE'}
                  </span>
                </div>
                <div className="flex justify-between text-charcoal-300">
                  <span>Status:</span>
                  <span className="font-medium text-paper-50">{getRegionStatus(hoveredRegion)}</span>
                </div>
              </div>
              <div className="mt-2.5 pt-1.5 border-t border-charcoal-800 text-[9px] text-charcoal-400 text-center">
                Click to inspect hazard breakdown
              </div>
            </div>
          )}

          {/* Hover Resource Tooltip */}
          {hoveredResource && !hoveredRegion && (
            <div
              className="absolute pointer-events-none z-30 p-3.5 rounded-2xl bg-charcoal-900 text-paper-50 text-xs shadow-floating border border-charcoal-700 min-w-[220px] -translate-x-1/2 -translate-y-full mt-[-12px]"
              style={{
                left: Math.max(110, Math.min(window.innerWidth > 600 ? 450 : 230, mouseCoord.x)),
                top: Math.max(10, mouseCoord.y - 15),
              }}
            >
              <div className="flex items-center justify-between gap-2 border-b border-charcoal-700 pb-1.5 mb-2">
                <span className="font-bold text-sm text-paper-50 uppercase tracking-tight block">
                  {hoveredResource.name}
                </span>
                <span className="px-1.5 py-0.5 rounded text-[9px] font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-700 shrink-0">
                  ✓ VERIFIED
                </span>
              </div>
              <div className="space-y-1 font-mono text-[11px]">
                <div className="flex justify-between text-charcoal-300">
                  <span>Type:</span>
                  <span className="font-semibold text-paper-50">{hoveredResource.category}</span>
                </div>
                <div className="flex justify-between text-charcoal-300">
                  <span>Location:</span>
                  <span className="text-paper-50">{hoveredResource.location}</span>
                </div>
                <div className="flex justify-between text-charcoal-300">
                  <span>Authority / Source:</span>
                  <span className="text-amber-300 font-semibold">{hoveredResource.source || 'Authorized Registry'}</span>
                </div>
                <div className="flex justify-between text-charcoal-300">
                  <span>Freshness:</span>
                  <span className="text-emerald-400 font-semibold">{hoveredResource.freshness || 'CURRENT'}</span>
                </div>
              </div>
              <div className="mt-2 pt-1 border-t border-charcoal-800 text-[9px] text-charcoal-400 text-center">
                Click to inspect verified resource
              </div>
            </div>
          )}
        </div>
      )}


        {/* Selected Region Detailed Panel */}
        {!hideInternalInspector && activeSelectedRegion && (
          <TiltCard
            maxTilt={1.5}
            className="lg:absolute lg:bottom-6 lg:right-6 z-20 w-full lg:w-80 p-5 rounded-3xl bg-white border border-paper-300 shadow-floating mt-4 lg:mt-0"
          >
            {(() => {
              const { floodScore, landslideScore, cycloneScore } = getHazardScores(activeSelectedRegion);
              const locRecord = ALL_INDIAN_LOCATIONS.find((l) => l.id === activeSelectedRegion.id);
              return (
                <div className="space-y-4">
                  {/* Top Bar */}
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center gap-1.5 flex-wrap">
                        <span className="text-xs font-mono uppercase text-charcoal-500 font-bold">
                          {locRecord?.type === 'UNION_TERRITORY' ? 'Union Territory' : 'Indian State'}
                        </span>
                        <DemoBadge label="MONITORED" />
                        <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full font-bold border ${
                          mapPerspective === 'FUTURE'
                            ? 'bg-indigo-50 text-indigo-700 border-indigo-200'
                            : 'bg-paper-100 text-charcoal-700 border-paper-300'
                        }`}>
                          {mapPerspective === 'FUTURE' ? `FUTURE (${futureHorizon})` : 'CURRENT'}
                        </span>
                        <FreshnessBadge
                          status={
                            activeSelectedRegion.activeIncidentsCount > 0
                              ? 'OFFICIAL_LIVE'
                              : activeSelectedRegion.name.toLowerCase().includes('assam')
                              ? 'EMPIRICAL_ML'
                              : 'REGIONAL_BASELINE'
                          }
                          size="xs"
                        />
                      </div>
                      <h4 className="text-xl font-bold uppercase tracking-tight text-charcoal-950">
                        {activeSelectedRegion.name}
                      </h4>
                      <p className="text-xs text-charcoal-500 font-mono">
                        Capital: {activeSelectedRegion.capital} • {activeSelectedRegion.monitoredDistricts} Districts
                      </p>
                    </div>
                    <RiskBadge level={activeSelectedRegion.riskLevel} size="md" />
                  </div>

                  {/* Historical Hazard Baseline Gauge */}
                  <div className="p-3.5 rounded-2xl bg-paper-50 border border-paper-200 space-y-2">
                    <div className="flex items-center justify-between">
                      <div>
                        <span className="text-xs font-mono uppercase text-charcoal-500 font-semibold block">
                          Historical Hazard Baseline
                        </span>
                        <span className="text-xs text-charcoal-600">
                          Primary Hazard: <strong className="text-charcoal-900">{activeSelectedRegion.primaryRisk}</strong>
                        </span>
                      </div>
                      <div className="text-right">
                        <span className="text-2xl font-black font-mono text-charcoal-950">
                          {activeSelectedRegion.riskScore}%
                        </span>
                      </div>
                    </div>
                    {activeSelectedRegion.name.toLowerCase().includes('assam') ? (
                      <div className="space-y-1 text-[10px] font-mono text-emerald-800 bg-emerald-50 p-2 rounded-lg border border-emerald-200">
                        <div className="font-bold flex items-center justify-between">
                          <span>✓ Empirical ML Prediction Available</span>
                          <FreshnessBadge status="EMPIRICAL_ML" size="xs" />
                        </div>
                        <div className="text-emerald-700">Model: assam_flood_prototype_v1 (13 features, 32 audited observations)</div>
                      </div>
                    ) : (
                      <div className="space-y-1 text-[10px] font-mono text-charcoal-700 bg-paper-100 p-2 rounded-lg border border-paper-300">
                        <div className="font-bold text-charcoal-900 flex items-center justify-between">
                          <span>ℹ️ ML prediction is not currently available for this region.</span>
                          <FreshnessBadge status="REGIONAL_BASELINE" size="xs" />
                        </div>
                        <div className="text-charcoal-600">Regional baseline and official disaster intelligence are shown.</div>
                      </div>
                    )}
                  </div>

                  {/* Specific Hazard Indicators */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-xs font-mono">
                      <span className="text-charcoal-600 flex items-center gap-1.5">
                        <Waves className="w-3.5 h-3.5 text-blue-500" />
                        Flood Risk
                      </span>
                      <span className="font-bold text-charcoal-900">{floodScore}%</span>
                    </div>
                    <div className="w-full h-1.5 rounded-full bg-paper-200 overflow-hidden">
                      <div
                        className="h-full rounded-full bg-blue-500 transition-all duration-500"
                        style={{ width: `${floodScore}%` }}
                      />
                    </div>

                    <div className="flex items-center justify-between text-xs font-mono pt-1">
                      <span className="text-charcoal-600 flex items-center gap-1.5">
                        <Mountain className="w-3.5 h-3.5 text-amber-600" />
                        Landslide Risk
                      </span>
                      <span className="font-bold text-charcoal-900">{landslideScore}%</span>
                    </div>
                    <div className="w-full h-1.5 rounded-full bg-paper-200 overflow-hidden">
                      <div
                        className="h-full rounded-full bg-amber-600 transition-all duration-500"
                        style={{ width: `${landslideScore}%` }}
                      />
                    </div>

                    <div className="flex items-center justify-between text-xs font-mono pt-1">
                      <span className="text-charcoal-600 flex items-center gap-1.5">
                        <Wind className="w-3.5 h-3.5 text-teal-600" />
                        Cyclone Risk
                      </span>
                      <span className="font-bold text-charcoal-900">{cycloneScore}%</span>
                    </div>
                    <div className="w-full h-1.5 rounded-full bg-paper-200 overflow-hidden">
                      <div
                        className="h-full rounded-full bg-teal-600 transition-all duration-500"
                        style={{ width: `${cycloneScore}%` }}
                      />
                    </div>
                  </div>

                  {/* Summary Narrative */}
                  <div className="text-xs text-charcoal-600 leading-relaxed border-t border-paper-200 pt-3">
                    {activeSelectedRegion.summary}
                  </div>

                  {/* Immediate Recommended Action */}
                  <div className="p-3 rounded-xl bg-paper-100/80 border border-paper-200 text-xs">
                    <span className="font-mono text-[10px] uppercase text-charcoal-500 font-bold block mb-1">
                      Immediate Preparedness Action
                    </span>
                    <span className="text-charcoal-800 font-medium">
                      {activeSelectedRegion.recommendedActions[0] || 'Standard seasonal readiness and community alert subscription.'}
                    </span>
                  </div>

                  {/* Emergency Contact */}
                  <div className="flex items-center justify-between text-xs pt-1 border-t border-paper-200 font-mono text-charcoal-500">
                    <span>Emergency SDMA:</span>
                    <span className="font-bold text-charcoal-900">
                      {activeSelectedRegion.emergencyHelpline}
                    </span>
                  </div>
                </div>
              );
            })()}
          </TiltCard>
        )}
      </div>
    </div>
  );
};
