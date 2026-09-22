import React, { useState } from 'react';
import {
  Droplets,
  Wind,
  Sun,
  CloudLightning,
  Mountain,
  Activity,
  ShieldAlert,
  Clock,
  ExternalLink,
  ChevronRight,
  Info,
  CheckCircle2,
  AlertTriangle
} from 'lucide-react';
import { RiskState, TrendState, ConfidenceLevel, UncertaintyLevel } from '../../types/predictiveRisk';
import { RiskTrendIndicator } from '../predictive/RiskTrendIndicator';
import { UncertaintyBadge } from '../predictive/UncertaintyBadge';

interface HazardInfo {
  code: string;
  name: string;
  icon: any;
  leadAgency: string;
  dataClassification: string;
  currentState: RiskState;
  futureState: RiskState;
  trend: TrendState;
  peakHorizon: string;
  confidence: ConfidenceLevel;
  uncertainty: UncertaintyLevel;
  why: string;
  whatToDo: string;
  isEarthquake?: boolean;
}

const ALL_HAZARDS: HazardInfo[] = [
  {
    code: 'FLOOD',
    name: 'Flood Risk',
    icon: Droplets,
    leadAgency: 'CWC (Central Water Commission) & IMD',
    dataClassification: 'HYDROLOGICAL_TELEMETRY',
    currentState: 'WATCH',
    futureState: 'ELEVATED',
    trend: 'RISING',
    peakHorizon: '6-24h',
    confidence: 'HIGH',
    uncertainty: 'LOW',
    why: 'Catchment rainfall volume converging on upper river basins; dam release schedules scheduled within 12 hours.',
    whatToDo: 'Move vital records and livestock to elevated structures; do not attempt driving across flooded culverts.'
  },
  {
    code: 'CYCLONE',
    name: 'Tropical Cyclone',
    icon: Wind,
    leadAgency: 'IMD (Cyclone Warning Division)',
    dataClassification: 'SYNOPTIC_METEOROLOGY',
    currentState: 'NORMAL',
    futureState: 'WATCH',
    trend: 'STABLE',
    peakHorizon: '1-3d',
    confidence: 'HIGH',
    uncertainty: 'MODERATE',
    why: 'Low-pressure system tracking across oceanic coordinates; atmospheric wind shear conditions monitored.',
    whatToDo: 'Fishermen advised not to venture into deep sea; coastal residents verify storm shutters and radio batteries.'
  },
  {
    code: 'HEATWAVE',
    name: 'Severe Heatwave',
    icon: Sun,
    leadAgency: 'IMD & NDMA National Heatwave Guidelines',
    dataClassification: 'THERMAL_SURFACE_MONITORING',
    currentState: 'WATCH',
    futureState: 'HIGH',
    trend: 'RISING',
    peakHorizon: '0-6h',
    confidence: 'HIGH',
    uncertainty: 'LOW',
    why: 'Dry continental westerly winds maintaining maximum temperatures 4.5°C to 6.4°C above seasonal normal.',
    whatToDo: 'Avoid strenuous outdoor exposure between 11:00 AM and 4:00 PM; drink ORS, buttermilk, and clean water frequently.'
  },
  {
    code: 'SEVERE_WEATHER',
    name: 'Severe Weather / Squall',
    icon: CloudLightning,
    leadAgency: 'IMD Doppler Weather Radar Network',
    dataClassification: 'DOPPLER_RADAR_NOWCAST',
    currentState: 'WATCH',
    futureState: 'WATCH',
    trend: 'STABLE',
    peakHorizon: '0-6h',
    confidence: 'MODERATE',
    uncertainty: 'LOW',
    why: 'Isolated convective cloud clusters producing sudden wind gusts and thunderstorm cells over short lead intervals.',
    whatToDo: 'Stay indoors away from tin sheds, power lines, and tall isolated trees during lightning activity.'
  },
  {
    code: 'LANDSLIDE',
    name: 'Rainfall-Triggered Landslide',
    icon: Mountain,
    leadAgency: 'Geological Survey of India (GSI) & NRSC',
    dataClassification: 'GEOMORPHIC_SATURATION_MODEL',
    currentState: 'WATCH',
    futureState: 'ELEVATED',
    trend: 'RISING',
    peakHorizon: '6-24h',
    confidence: 'MODERATE',
    uncertainty: 'MODERATE',
    why: 'Antecedent cumulative soil saturation combined with forecasted high-intensity precipitation over vulnerable slopes.',
    whatToDo: 'Residents near steep hill cuts must monitor ground fissures; heed local evacuation orders immediately.'
  },
  {
    code: 'EARTHQUAKE',
    name: 'Seismic Vulnerability Baseline',
    icon: Activity,
    leadAgency: 'National Centre for Seismology (NCS) & USGS',
    dataClassification: 'TECTONIC_BASELINE_ZONE',
    currentState: 'WATCH',
    futureState: 'WATCH',
    trend: 'STABLE',
    peakHorizon: 'BASELINE_OUTLOOK',
    confidence: 'LOW',
    uncertainty: 'VERY_HIGH',
    why: 'Tectonic baseline under BIS IS 1893 seismic zoning. Earthquake timing cannot currently be predicted reliably.',
    whatToDo: 'Anchor heavy furniture; identify safe Drop, Cover, Hold spots; maintain earthquake family safety drills.',
    isEarthquake: true
  }
];

interface FutureHazardMatrixProps {
  onSelectHazard?: (hazardCode: string) => void;
}

export const FutureHazardMatrix: React.FC<FutureHazardMatrixProps> = ({ onSelectHazard }) => {
  const [selectedHazardCode, setSelectedHazardCode] = useState<string | null>(null);

  const getRiskColor = (state: RiskState) => {
    switch (state) {
      case 'CRITICAL':
        return 'text-rose-800 bg-rose-50 border-rose-200 font-bold';
      case 'HIGH':
        return 'text-orange-800 bg-orange-50 border-orange-200 font-bold';
      case 'ELEVATED':
        return 'text-amber-800 bg-amber-50 border-amber-200 font-bold';
      case 'WATCH':
        return 'text-blue-800 bg-blue-50 border-blue-200 font-bold';
      case 'NORMAL':
      default:
        return 'text-emerald-800 bg-emerald-50 border-emerald-200 font-bold';
    }
  };

  return (
    <section id="hazard-matrix" className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto scroll-mt-24">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-blue-700 mb-1">
              <Clock className="w-4 h-4" />
              <span>MULTI-HAZARD PREDICTIVE MATRIX // 6 DISASTER DOMAINS</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              Forward Risk Across All 6 Hazards
            </h2>
            <p className="text-xs sm:text-sm text-slate-600 max-w-2xl mt-1">
              Statutory forward assessments with explicit provenance attribution.
              Earthquake timing is strictly non-predictable; seismic metrics reflect structural and tectonic baselines.
            </p>
          </div>

          <div className="text-[11px] font-mono text-slate-500">
            Authoritative Sources: IMD • CWC • NDMA • GSI • NCS • USGS
          </div>
        </div>

        {/* 6 Hazard Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {ALL_HAZARDS.map((h) => {
            const Icon = h.icon;
            const isSelected = selectedHazardCode === h.code;
            return (
              <div
                key={h.code}
                onClick={() => {
                  setSelectedHazardCode(isSelected ? null : h.code);
                  onSelectHazard?.(h.code);
                }}
                className={`p-5 rounded-3xl border transition-all cursor-pointer flex flex-col justify-between ${
                  isSelected
                    ? 'bg-slate-50 border-blue-600 ring-2 ring-blue-500/30 shadow-md'
                    : 'bg-white border-slate-200 hover:border-slate-300 shadow-xs'
                }`}
              >
                <div className="space-y-3">
                  {/* Top Header */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2.5">
                      <div className="p-2 rounded-xl bg-blue-50 text-blue-700">
                        <Icon className="w-5 h-5" />
                      </div>
                      <div>
                        <h3 className="text-sm font-bold text-slate-900 font-mono">
                          {h.name}
                        </h3>
                        <span className="text-[10px] text-slate-500 block font-mono -mt-0.5">
                          {h.leadAgency}
                        </span>
                      </div>
                    </div>

                    <span className={`px-2.5 py-0.5 rounded-full text-xs font-mono font-bold border ${getRiskColor(h.futureState)}`}>
                      {h.futureState}
                    </span>
                  </div>

                  {/* Earthquake Non-Prediction Disclaimer Banner */}
                  {h.isEarthquake && (
                    <div className="p-2.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-[10px] font-mono leading-tight">
                      <strong>SCIENTIFIC MANDATE:</strong> Earthquake timing cannot currently be predicted reliably.
                      Metrics represent tectonic baseline and structural safety guidance.
                    </div>
                  )}

                  {/* Metrics Strip */}
                  <div className="grid grid-cols-2 gap-2 pt-1 text-[11px] font-mono">
                    <div className="p-2 rounded-xl bg-slate-50 border border-slate-200">
                      <span className="text-slate-500 block text-[9px] uppercase font-semibold">Trend</span>
                      <RiskTrendIndicator trend={h.trend} size="sm" />
                    </div>
                    <div className="p-2 rounded-xl bg-slate-50 border border-slate-200">
                      <span className="text-slate-500 block text-[9px] uppercase font-semibold">Peak Horizon</span>
                      <span className="font-bold text-slate-900">{h.peakHorizon}</span>
                    </div>
                  </div>

                  {/* Why / Causal Driver */}
                  <div className="text-xs text-slate-600 leading-relaxed">
                    <span className="font-mono text-[10px] uppercase font-bold text-slate-500 block mb-0.5">
                      Causal Driver
                    </span>
                    {h.why}
                  </div>

                  {/* What Should I Do */}
                  <div className="text-xs text-slate-700 leading-relaxed p-2.5 rounded-xl bg-slate-50 border border-slate-200">
                    <span className="font-mono text-[10px] uppercase font-bold text-blue-700 block mb-0.5 flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" />
                      <span>Action Protocol</span>
                    </span>
                    {h.whatToDo}
                  </div>
                </div>

                {/* Footer Badges */}
                <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[10px] font-mono">
                  <UncertaintyBadge confidence={h.confidence} uncertainty={h.uncertainty} />
                  <span className="text-slate-500">
                    {h.dataClassification}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
