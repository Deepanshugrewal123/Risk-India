import React, { useState, useEffect } from 'react';
import {
  GitBranch,
  MapPin,
  Flame,
  ArrowRight,
  BookOpen,
  Compass,
  Layers,
  ChevronRight,
  ShieldAlert,
  Info,
  CheckCircle2,
  HelpCircle
} from 'lucide-react';
import { CascadingRiskSection } from '../cascading/CascadingRiskSection';
import { WhatCanHappenNextPanel } from '../cascading/WhatCanHappenNextPanel';
import { PublicSafetyWorkflowBar } from '../common/PublicSafetyWorkflowBar';
import { NavigationPage } from '../common/Navbar';
import { ALL_INDIAN_STATES, ALL_INDIAN_UNION_TERRITORIES } from '../../data/indiaLocations';

interface CascadingRiskPageProps {
  onNavigate?: (page: NavigationPage, context?: { hazard?: string; category?: string; regionId?: string }) => void;
  initialRegionId?: string;
  initialRegionName?: string;
  initialHazard?: string;
}

export interface JurisdictionOption {
  id: string;
  name: string;
  type: 'STATE' | 'UNION_TERRITORY';
  defaultHazard: string;
}

const mapHazard = (risk?: string): string => {
  if (!risk) return 'FLOOD';
  const clean = risk.toUpperCase().replace(/\s+/g, '_');
  if (['FLOOD', 'CYCLONE', 'EARTHQUAKE', 'HEATWAVE', 'LANDSLIDE', 'SEVERE_WEATHER'].includes(clean)) {
    return clean;
  }
  return 'FLOOD';
};

const ALL_JURISDICTIONS: JurisdictionOption[] = [
  ...ALL_INDIAN_STATES.map((s) => ({
    id: s.id,
    name: s.name,
    type: 'STATE' as const,
    defaultHazard: mapHazard(s.primaryRisk)
  })),
  ...ALL_INDIAN_UNION_TERRITORIES.map((ut) => ({
    id: ut.id,
    name: ut.name,
    type: 'UNION_TERRITORY' as const,
    defaultHazard: mapHazard(ut.primaryRisk)
  }))
].sort((a, b) => a.name.localeCompare(b.name));

const HAZARDS = [
  { id: 'FLOOD', label: 'Flood', icon: '🌊' },
  { id: 'CYCLONE', label: 'Cyclone', icon: '🌀' },
  { id: 'EARTHQUAKE', label: 'Earthquake', icon: '⚡' },
  { id: 'HEATWAVE', label: 'Heatwave', icon: '☀️' },
  { id: 'LANDSLIDE', label: 'Landslide', icon: '⛰️' },
  { id: 'SEVERE_WEATHER', label: 'Severe Weather', icon: '⛈️' }
];

export const CascadingRiskPage: React.FC<CascadingRiskPageProps> = ({
  onNavigate,
  initialRegionId = 'assam',
  initialRegionName = 'Assam',
  initialHazard = 'FLOOD'
}) => {
  const [selectedRegionId, setSelectedRegionId] = useState<string>(initialRegionId);
  const [selectedHazard, setSelectedHazard] = useState<string>(initialHazard);

  useEffect(() => {
    if (initialRegionId) setSelectedRegionId(initialRegionId);
  }, [initialRegionId]);

  useEffect(() => {
    if (initialHazard) setSelectedHazard(initialHazard);
  }, [initialHazard]);

  const currentRegion = ALL_JURISDICTIONS.find((r) => r.id === selectedRegionId) || {
    id: selectedRegionId,
    name: initialRegionName,
    type: 'STATE' as const,
    defaultHazard: 'FLOOD'
  };

  return (
    <main className="py-10 sm:py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-8 animate-in fade-in duration-200">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-xs font-mono text-charcoal-500 dark:text-slate-400">
        <button
          onClick={() => onNavigate && onNavigate('home')}
          className="hover:underline hover:text-charcoal-800 dark:hover:text-slate-200"
        >
          Home
        </button>
        <span>/</span>
        <button
          onClick={() => onNavigate && onNavigate('future-risk')}
          className="hover:underline hover:text-charcoal-800 dark:hover:text-slate-200"
        >
          Future Risk
        </button>
        <span>/</span>
        <span className="text-charcoal-900 dark:text-slate-100 font-bold">Cascading Risk</span>
      </div>

      {/* Hero Header */}
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6 pb-6 border-b border-slate-200">
        <div className="max-w-3xl space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 border border-blue-200 text-blue-800 text-xs font-mono uppercase tracking-wider font-bold">
            <GitBranch className="w-3.5 h-3.5 text-blue-700" />
            <span>DISASTER CONSEQUENCE INTELLIGENCE // ALL 36 STATES &amp; UNION TERRITORIES</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-extrabold text-slate-900 tracking-tight">
            Cascading Risk Intelligence
          </h1>
          <p className="text-base sm:text-lg text-slate-600 leading-relaxed font-normal">
            Answers the vital citizen question: <strong className="text-slate-900 font-semibold">&quot;A disaster happens — what could happen NEXT?&quot;</strong>
          </p>
        </div>

        {/* Action Link to Safety Guide */}
        <button
          onClick={() => onNavigate && onNavigate('safety-guide')}
          className="min-h-[48px] px-5 py-3 rounded-2xl bg-slate-900 text-white hover:bg-slate-800 font-mono text-xs sm:text-sm font-bold flex items-center justify-center gap-2.5 transition-all shadow-xs shrink-0 self-start lg:self-end"
        >
          <BookOpen className="w-4 h-4 text-emerald-400" />
          <span>VIEW COMPLETE SAFETY GUIDE</span>
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>

      {/* Flagship Concept Card: “A disaster happens — what could happen NEXT?” */}
      <div className="p-6 sm:p-8 rounded-3xl bg-white border border-slate-200 shadow-xs space-y-6">
        <div className="space-y-1.5 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-amber-50 border border-amber-200 text-amber-900 text-[11px] font-mono font-bold uppercase tracking-wider">
            <Layers className="w-3 h-3 text-amber-700" />
            <span>PRIMARY DIFFERENTIATING ARCHITECTURE</span>
          </div>
          <h2 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
            “A disaster happens — what could happen NEXT?”
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
            Disaster impact rarely stops at the initial shock. A cyclone breaches coastal sea dykes; saline flooding poisons freshwater borewells; submerged transformers plunge hospitals into blackout. RISK // INDIA models the physical cascade across five progressive stages:
          </p>
        </div>

        {/* 5-Stage Consequence Progression Chain */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 pt-2">
          {/* Stage 1 */}
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 flex flex-col justify-between space-y-2">
            <div>
              <div className="flex items-center justify-between mb-1">
                <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-800 text-xs font-mono font-bold flex items-center justify-center">1</span>
                <span className="text-[10px] font-mono text-slate-500 uppercase font-bold">Inception</span>
              </div>
              <h3 className="text-xs font-mono font-bold uppercase text-blue-900">
                PRIMARY HAZARD
              </h3>
              <p className="text-[11px] text-slate-600 mt-1 leading-relaxed">
                The primary event: torrential rainfall, cyclonic winds, seismic shaking, or heat dome.
              </p>
            </div>
            <div className="text-[10px] font-mono text-blue-700 font-semibold pt-2 border-t border-slate-200">
              Triggers initial shock
            </div>
          </div>

          {/* Stage 2 */}
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 flex flex-col justify-between space-y-2">
            <div>
              <div className="flex items-center justify-between mb-1">
                <span className="w-6 h-6 rounded-full bg-amber-100 text-amber-800 text-xs font-mono font-bold flex items-center justify-center">2</span>
                <span className="text-[10px] font-mono text-slate-500 uppercase font-bold">Terrain Shift</span>
              </div>
              <h3 className="text-xs font-mono font-bold uppercase text-amber-900">
                PHYSICAL CHANGE
              </h3>
              <p className="text-[11px] text-slate-600 mt-1 leading-relaxed">
                Environmental shifts: soil pore-water saturation, embankment scour, drainage backflow.
              </p>
            </div>
            <div className="text-[10px] font-mono text-amber-700 font-semibold pt-2 border-t border-slate-200">
              Alters physical system
            </div>
          </div>

          {/* Stage 3 */}
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 flex flex-col justify-between space-y-2">
            <div>
              <div className="flex items-center justify-between mb-1">
                <span className="w-6 h-6 rounded-full bg-orange-100 text-orange-800 text-xs font-mono font-bold flex items-center justify-center">3</span>
                <span className="text-[10px] font-mono text-slate-500 uppercase font-bold">Emergent Threat</span>
              </div>
              <h3 className="text-xs font-mono font-bold uppercase text-orange-900">
                SECONDARY HAZARD
              </h3>
              <p className="text-[11px] text-slate-600 mt-1 leading-relaxed">
                Consequential perils: slope failures/landslides, water table contamination, electrical fire.
              </p>
            </div>
            <div className="text-[10px] font-mono text-orange-700 font-semibold pt-2 border-t border-slate-200">
              Spawns subsequent hazard
            </div>
          </div>

          {/* Stage 4 */}
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 flex flex-col justify-between space-y-2">
            <div>
              <div className="flex items-center justify-between mb-1">
                <span className="w-6 h-6 rounded-full bg-indigo-100 text-indigo-800 text-xs font-mono font-bold flex items-center justify-center">4</span>
                <span className="text-[10px] font-mono text-slate-500 uppercase font-bold">Lifeline Stress</span>
              </div>
              <h3 className="text-xs font-mono font-bold uppercase text-indigo-900">
                SYSTEMIC CONSEQUENCE
              </h3>
              <p className="text-[11px] text-slate-600 mt-1 leading-relaxed">
                Critical lifeline breakdown: grid blackout, severed highway access, waterborne epidemic.
              </p>
            </div>
            <div className="text-[10px] font-mono text-indigo-700 font-semibold pt-2 border-t border-slate-200">
              Disrupts human society
            </div>
          </div>

          {/* Stage 5 */}
          <div className="p-4 rounded-2xl bg-emerald-50/70 border border-emerald-300 flex flex-col justify-between space-y-2">
            <div>
              <div className="flex items-center justify-between mb-1">
                <span className="w-6 h-6 rounded-full bg-emerald-600 text-white text-xs font-mono font-bold flex items-center justify-center">5</span>
                <span className="text-[10px] font-mono text-emerald-800 uppercase font-bold">Action Directive</span>
              </div>
              <h3 className="text-xs font-mono font-bold uppercase text-emerald-950">
                WHAT CITIZENS SHOULD DO
              </h3>
              <p className="text-[11px] text-emerald-900 mt-1 leading-relaxed">
                Immediate defensive countermeasures: isolate utilities, boil water, evacuate via vetted routes.
              </p>
            </div>
            <div className="text-[10px] font-mono text-emerald-800 font-bold pt-2 border-t border-emerald-200 flex items-center gap-1">
              <span>Direct Safety Action</span>
              <span>→</span>
            </div>
          </div>
        </div>

        {/* Evidence Posture Reference Key: Explicit Distinction of All 6 Postures */}
        <div className="pt-4 border-t border-slate-200 space-y-2.5">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-mono uppercase font-bold text-slate-700 block">
              SCIENTIFIC HONESTY // 6 STANDARDIZED EVIDENCE POSTURES
            </span>
            <span className="text-[10px] font-mono text-slate-500">
              Zero fabricated percentages • Explicit data posture transparency
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 text-xs">
            <div className="p-2.5 rounded-xl bg-rose-50 border border-rose-200 space-y-1">
              <div className="flex items-center gap-1.5 font-mono font-bold text-[10px] text-rose-900">
                <span className="w-2 h-2 rounded-full bg-rose-600 animate-pulse" />
                <span>LIVE EVIDENCE</span>
              </div>
              <p className="text-[10px] text-rose-950 leading-tight">
                Confirmed by real-time sensor, river gauge, or IMD radar.
              </p>
            </div>

            <div className="p-2.5 rounded-xl bg-orange-50 border border-orange-200 space-y-1">
              <div className="flex items-center gap-1.5 font-mono font-bold text-[10px] text-orange-900">
                <span className="w-2 h-2 rounded-full bg-orange-600" />
                <span>RECENT EVIDENCE</span>
              </div>
              <p className="text-[10px] text-orange-950 leading-tight">
                Satellite or field report recorded in past 24–48 hours.
              </p>
            </div>

            <div className="p-2.5 rounded-xl bg-blue-50 border border-blue-200 space-y-1">
              <div className="flex items-center gap-1.5 font-mono font-bold text-[10px] text-blue-900">
                <span className="w-2 h-2 rounded-full bg-blue-600" />
                <span>FORECAST AVAILABLE</span>
              </div>
              <p className="text-[10px] text-blue-950 leading-tight">
                Projected by official IMD NWP or CWC basin model.
              </p>
            </div>

            <div className="p-2.5 rounded-xl bg-slate-100 border border-slate-200 space-y-1">
              <div className="flex items-center gap-1.5 font-mono font-bold text-[10px] text-slate-900">
                <span className="w-2 h-2 rounded-full bg-slate-500" />
                <span>BASELINE ONLY</span>
              </div>
              <p className="text-[10px] text-slate-700 leading-tight">
                Physical/geotechnical correlation without live sensors.
              </p>
            </div>

            <div className="p-2.5 rounded-xl bg-amber-50 border border-amber-200 space-y-1">
              <div className="flex items-center gap-1.5 font-mono font-bold text-[10px] text-amber-900">
                <span className="w-2 h-2 rounded-full bg-amber-600" />
                <span>LIMITED EVIDENCE</span>
              </div>
              <p className="text-[10px] text-amber-950 leading-tight">
                Sparse telemetry; baseline physical correlations applied.
              </p>
            </div>

            <div className="p-2.5 rounded-xl bg-slate-100 border border-slate-200 space-y-1">
              <div className="flex items-center gap-1.5 font-mono font-bold text-[10px] text-slate-700">
                <span className="w-2 h-2 rounded-full bg-slate-400" />
                <span>DATA UNAVAILABLE</span>
              </div>
              <p className="text-[10px] text-slate-600 leading-tight">
                Honest reporting of data gap; zero synthetic assumptions.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Statutory & Scientific Guardrail Disclaimers */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 rounded-2xl bg-blue-50/70 border border-blue-200 text-xs text-slate-800 flex items-start gap-3">
          <Info className="w-4.5 h-4.5 text-blue-700 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <strong className="font-mono uppercase font-bold block text-blue-900">
              Physically Established Consequence Pathways
            </strong>
            <p className="leading-relaxed text-slate-700">
              Cascading risk relationships reflect physically established and empirical vulnerability pathways.
              They do <strong>NOT</strong> represent predictive forecasts or synthetic probability models.
            </p>
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-amber-50/70 border border-amber-200 text-xs text-amber-950 flex items-start gap-3">
          <ShieldAlert className="w-4.5 h-4.5 text-amber-600 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <strong className="font-mono uppercase font-bold block text-amber-900">
              Seismic Non-Prediction Guarantee
            </strong>
            <p className="leading-relaxed text-amber-900">
              Earthquakes are fundamentally non-predictable: ground shaking triggers structural and geotechnical failures,
              not scheduled calendar events. Temporal earthquake prediction is scientifically prohibited.
            </p>
          </div>
        </div>
      </div>

      {/* Region & Hazard Selector Bar (All 36 Jurisdictions) */}
      <div className="p-5 sm:p-6 rounded-3xl bg-white dark:bg-slate-900 border border-paper-300 dark:border-slate-800 space-y-4 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          {/* Region Dropdown with Optgroups */}
          <div className="flex items-center gap-3">
            <MapPin className="w-4 h-4 text-indigo-600 dark:text-indigo-400 shrink-0" />
            <div className="space-y-0.5">
              <span className="text-[10px] font-mono uppercase font-bold text-charcoal-500 dark:text-slate-400 block">
                Target State / Union Territory (36 Total):
              </span>
              <select
                value={selectedRegionId}
                onChange={(e) => {
                  setSelectedRegionId(e.target.value);
                  const found = ALL_JURISDICTIONS.find((r) => r.id === e.target.value);
                  if (found) setSelectedHazard(found.defaultHazard);
                }}
                className="min-h-[44px] px-3.5 py-1.5 rounded-xl bg-paper-100 dark:bg-slate-800 border border-paper-300 dark:border-slate-700 text-sm font-bold text-charcoal-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-600"
              >
                <optgroup label="States (28)">
                  {ALL_JURISDICTIONS.filter((j) => j.type === 'STATE').map((r) => (
                    <option key={r.id} value={r.id}>
                      {r.name}
                    </option>
                  ))}
                </optgroup>
                <optgroup label="Union Territories (8)">
                  {ALL_JURISDICTIONS.filter((j) => j.type === 'UNION_TERRITORY').map((r) => (
                    <option key={r.id} value={r.id}>
                      {r.name}
                    </option>
                  ))}
                </optgroup>
              </select>
            </div>
          </div>

          <div className="text-xs font-mono text-charcoal-500 dark:text-slate-400">
            Selected: <strong className="text-charcoal-900 dark:text-white">{currentRegion.name}</strong> • Hazard:{' '}
            <strong className="text-charcoal-900 dark:text-white">{selectedHazard}</strong>
          </div>
        </div>

        {/* Hazard Selector Pills */}
        <div className="space-y-1.5 pt-2 border-t border-paper-200 dark:border-slate-800">
          <span className="text-[10px] font-mono uppercase font-bold text-charcoal-500 dark:text-slate-400 block">
            Select Primary Trigger Hazard:
          </span>
          <div className="flex flex-wrap items-center gap-2">
            {HAZARDS.map((h) => {
              const isSelected = selectedHazard === h.id;
              return (
                <button
                  key={h.id}
                  onClick={() => setSelectedHazard(h.id)}
                  className={`min-h-[44px] px-3.5 py-2 rounded-xl text-xs font-mono font-bold uppercase transition-all flex items-center gap-2 ${
                    isSelected
                      ? 'bg-indigo-600 text-white shadow-sm'
                      : 'bg-paper-100 dark:bg-slate-800 text-charcoal-700 dark:text-slate-300 hover:bg-paper-200 dark:hover:bg-slate-700'
                  }`}
                >
                  <span>{h.icon}</span>
                  <span>{h.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Main 4-Stage Cascading Risk Section Component */}
      <CascadingRiskSection
        regionId={selectedRegionId}
        regionName={currentRegion.name}
        hazard={selectedHazard}
        onNavigate={onNavigate}
        onExploreSafetyGuide={(h) => {
          if (onNavigate) {
            onNavigate('safety-guide');
          }
        }}
      />

      {/* What Can Happen Next? Multi-Stage Consequence & Observable Signs Panel */}
      <div className="pt-6 border-t border-slate-200">
        <WhatCanHappenNextPanel
          initialHazard={selectedHazard}
          onNavigate={onNavigate}
        />
      </div>

      {/* Connected Public Safety Workflow Navigation Bar */}
      <PublicSafetyWorkflowBar
        currentPage="cascading-risk"
        onNavigate={onNavigate}
        className="mt-8"
      />
    </main>
  );
};
