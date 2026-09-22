import React, { useState } from 'react';
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
import { NavigationPage } from '../common/Navbar';
import { ALL_INDIAN_STATES, ALL_INDIAN_UNION_TERRITORIES } from '../../data/indiaLocations';

interface CascadingRiskPageProps {
  onNavigate?: (page: NavigationPage) => void;
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
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6 pb-6 border-b border-paper-300 dark:border-slate-800">
        <div className="max-w-3xl space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200 dark:border-indigo-800 text-indigo-800 dark:text-indigo-300 text-xs font-mono uppercase tracking-wider font-bold">
            <GitBranch className="w-3.5 h-3.5" />
            <span>CAUSAL DISASTER SEQUENCE // ALL 36 STATES &amp; UNION TERRITORIES</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-black text-charcoal-950 dark:text-white tracking-tight">
            Cascading Risk Intelligence
          </h1>
          <p className="text-base sm:text-lg text-charcoal-600 dark:text-slate-300 leading-relaxed">
            Answers the vital citizen question: <em>&quot;If this disaster happens, what physical changes, secondary hazards, and systemic breakdowns could follow?&quot;</em>
          </p>
        </div>

        {/* Action Link to Safety Guide */}
        <button
          onClick={() => onNavigate && onNavigate('safety-guide')}
          className="min-h-[48px] px-5 py-3 rounded-2xl bg-charcoal-950 dark:bg-white text-white dark:text-charcoal-950 font-mono text-xs sm:text-sm font-bold flex items-center justify-center gap-2.5 transition-all shadow-subtle shrink-0 self-start lg:self-end hover:bg-charcoal-850 dark:hover:bg-slate-100"
        >
          <BookOpen className="w-4 h-4 text-emerald-400 dark:text-emerald-600" />
          <span>VIEW COMPLETE SAFETY GUIDE</span>
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>

      {/* Statutory & Scientific Guardrail Disclaimers */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 rounded-2xl bg-indigo-50/70 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-900 text-xs text-indigo-950 dark:text-indigo-200 flex items-start gap-3">
          <Info className="w-4.5 h-4.5 text-indigo-600 dark:text-indigo-400 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <strong className="font-mono uppercase font-bold block">
              Physically Established Consequence Pathways
            </strong>
            <p className="leading-relaxed">
              Cascading risk relationships reflect physically established and empirical vulnerability pathways.
              They do <strong>NOT</strong> represent predictive forecasts or synthetic probability models.
            </p>
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-amber-50/70 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-900 text-xs text-amber-950 dark:text-amber-200 flex items-start gap-3">
          <ShieldAlert className="w-4.5 h-4.5 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <strong className="font-mono uppercase font-bold block">
              Seismic Non-Prediction Guarantee
            </strong>
            <p className="leading-relaxed">
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
      <div className="pt-6 border-t border-paper-200 dark:border-slate-800">
        <WhatCanHappenNextPanel
          initialHazard={selectedHazard}
          onNavigate={onNavigate}
        />
      </div>
    </main>
  );
};
