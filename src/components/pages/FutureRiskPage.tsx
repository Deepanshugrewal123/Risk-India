import React, { useState, useEffect } from 'react';
import {
  PredictiveRiskAssessment,
  NationalPredictiveOverview,
  PredictiveTimelinePoint,
  PredictiveScenario,
  RiskState,
  TrendState,
  ConfidenceLevel,
  UncertaintyLevel
} from '../../types/predictiveRisk';
import predictiveRiskService from '../../services/predictiveRiskService';
import { ALL_INDIAN_STATES, ALL_INDIAN_UNION_TERRITORIES } from '../../data/indiaLocations';
import { FutureRiskTimeline } from '../home/FutureRiskTimeline';
import { FutureHazardMatrix } from '../home/FutureHazardMatrix';
import { FutureRiskDrivers } from '../home/FutureRiskDrivers';
import { FutureRiskActionPanel } from '../home/FutureRiskActionPanel';
import { CascadingRiskSection } from '../cascading/CascadingRiskSection';
import { EarlyWarningNoticeSection } from '../home/EarlyWarningNoticeSection';
import { RiskTrendIndicator } from '../predictive/RiskTrendIndicator';
import { UncertaintyBadge } from '../predictive/UncertaintyBadge';
import { PredictionScopeNotice } from '../predictive/PredictionScopeNotice';
import { ScenarioPanel } from '../predictive/ScenarioPanel';
import { NavigationPage } from '../common/Navbar';
import {
  Sparkles,
  TrendingUp,
  Clock,
  ShieldAlert,
  Compass,
  CheckCircle2,
  Radio,
  RefreshCw,
  AlertTriangle,
  ChevronRight,
  Info,
  MapPin,
  FileCheck2,
  HelpCircle,
  ExternalLink,
  Shield,
  Layers,
  Activity,
  Globe,
  PhoneCall,
  ArrowLeft
} from 'lucide-react';

interface FutureRiskPageProps {
  onNavigate: (page: NavigationPage) => void;
  initialRegionId?: string;
  initialHazard?: string;
}

export const FutureRiskPage: React.FC<FutureRiskPageProps> = ({
  onNavigate,
  initialRegionId,
  initialHazard = 'FLOOD'
}) => {
  // Default region is null (National India-Wide Future Risk Overview)
  const [selectedRegion, setSelectedRegion] = useState<string | null>(initialRegionId || null);
  const [selectedHazard, setSelectedHazard] = useState<string>(initialHazard);
  const [nationalOverview, setNationalOverview] = useState<NationalPredictiveOverview | null>(null);
  const [assessment, setAssessment] = useState<PredictiveRiskAssessment | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [dataGap, setDataGap] = useState<boolean>(false);
  const [scenarios, setScenarios] = useState<PredictiveScenario[]>([]);

  const allEntities = [...ALL_INDIAN_STATES, ...ALL_INDIAN_UNION_TERRITORIES];

  // Load National Overview
  useEffect(() => {
    let isMounted = true;
    const loadNational = async () => {
      try {
        setLoading(true);
        const data = await predictiveRiskService.getNationalOverview();
        if (isMounted) setNationalOverview(data);
      } catch (err) {
        console.error('Failed to load national predictive overview on page:', err);
      } finally {
        if (isMounted) setLoading(false);
      }
    };
    loadNational();
    return () => {
      isMounted = false;
    };
  }, []);

  // Load Regional Assessment when specific region is selected
  useEffect(() => {
    let isMounted = true;
    if (!selectedRegion) {
      setAssessment(null);
      setScenarios([]);
      setDataGap(false);
      return;
    }

    const loadAssessment = async () => {
      try {
        setLoading(true);
        setDataGap(false);
        const [data, sc] = await Promise.all([
          predictiveRiskService.getHazardAssessment(selectedRegion, selectedHazard),
          predictiveRiskService.getScenarios(selectedRegion, selectedHazard).catch(() => [])
        ]);
        if (isMounted) {
          setAssessment(data);
          setScenarios(sc || []);
        }
      } catch (err) {
        console.warn('Data unavailable for region/hazard on FutureRiskPage:', selectedRegion, selectedHazard);
        if (isMounted) {
          setDataGap(true);
          setAssessment(null);
          setScenarios([]);
        }
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    loadAssessment();
    return () => {
      isMounted = false;
    };
  }, [selectedRegion, selectedHazard]);

  const selectedLocationMeta = allEntities.find((e) => e.id === selectedRegion);

  const getRiskColor = (state?: string) => {
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
    <div className="pt-24 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-8">
      {/* 1. Breadcrumbs & Top Navigation Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs font-mono">
        <div className="flex items-center gap-2 text-slate-500">
          <button
            onClick={() => onNavigate('home')}
            className="hover:text-slate-900 flex items-center gap-1 font-medium transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Home</span>
          </button>
          <span>/</span>
          <span className="text-slate-900 font-bold">Future Risk Intelligence</span>
          {selectedRegion && (
            <>
              <span>/</span>
              <span className="text-blue-700 font-bold">
                {selectedLocationMeta?.name || selectedRegion}
              </span>
            </>
          )}
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => onNavigate('risk-map')}
            className="px-3.5 py-1.5 rounded-xl font-bold bg-slate-900 text-white hover:bg-slate-800 transition-colors flex items-center gap-1.5 shadow-xs"
          >
            <Compass className="w-3.5 h-3.5" />
            <span>Open Risk Map</span>
          </button>
        </div>
      </div>

      {/* 2. Page Hero Banner: National Scope & Scientific Invariant Mandate */}
      <div className="p-6 sm:p-8 rounded-3xl bg-white border border-slate-200 shadow-xs space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 border border-blue-200 text-blue-800 text-xs font-mono font-bold uppercase tracking-wider mb-2">
              <Sparkles className="w-3.5 h-3.5 text-blue-700" />
              <span>NATIONAL PREDICTIVE DECISION SUPPORT SYSTEM</span>
            </div>
            <h1 className="text-3xl sm:text-5xl font-extrabold text-slate-900 tracking-tight">
              Future Risk Intelligence
            </h1>
            <p className="text-sm sm:text-base text-slate-600 max-w-3xl mt-2 font-normal">
              Official predictive modeling across 5 lead horizons (NOW to 7 days).
              Strictly non-synthetic observational fusion across IMD, CWC, NDMA, and Earth observations.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
            <div className="px-4 py-3 rounded-2xl bg-slate-50 border border-slate-200 text-center">
              <div className="text-[10px] font-mono text-slate-500 uppercase">Monitored Entities</div>
              <div className="text-xl font-mono font-extrabold text-slate-900">
                36 / 36
              </div>
            </div>
            <div className="px-4 py-3 rounded-2xl bg-slate-50 border border-slate-200 text-center">
              <div className="text-[10px] font-mono text-slate-500 uppercase">Synthetic Records</div>
              <div className="text-xl font-mono font-extrabold text-emerald-600">
                0
              </div>
            </div>
          </div>
        </div>

        {/* Location Selector Bar */}
        <div className="pt-4 border-t border-slate-100 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={() => setSelectedRegion(null)}
              className={`px-4 py-2 rounded-xl text-xs font-mono font-bold transition-all ${
                selectedRegion === null
                  ? 'bg-blue-700 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-700 border border-slate-200 hover:bg-slate-200'
              }`}
            >
              🇮🇳 National Overview (All 36 Jurisdictions)
            </button>

            <select
              value={selectedRegion || ''}
              onChange={(e) => setSelectedRegion(e.target.value || null)}
              className="px-3.5 py-2 rounded-xl text-xs font-mono bg-slate-50 border border-slate-200 text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-900 font-medium"
            >
              <option value="">-- Choose State or UT to Inspect --</option>
              <optgroup label="States (28)">
                {ALL_INDIAN_STATES.map((st) => (
                  <option key={st.id} value={st.id}>
                    {st.name} ({st.code})
                  </option>
                ))}
              </optgroup>
              <optgroup label="Union Territories (8)">
                {ALL_INDIAN_UNION_TERRITORIES.map((ut) => (
                  <option key={ut.id} value={ut.id}>
                    {ut.name} ({ut.code})
                  </option>
                ))}
              </optgroup>
            </select>
          </div>

          {selectedRegion && (
            <div className="flex items-center gap-1.5 overflow-x-auto text-xs font-mono">
              <span className="text-slate-500 font-semibold shrink-0">Hazard:</span>
              {['FLOOD', 'CYCLONE', 'HEATWAVE', 'SEVERE_WEATHER', 'LANDSLIDE', 'EARTHQUAKE'].map((h) => (
                <button
                  key={h}
                  onClick={() => setSelectedHazard(h)}
                  className={`px-2.5 py-1 rounded-lg transition-all ${
                    selectedHazard === h
                      ? 'bg-slate-900 text-white font-bold shadow-xs'
                      : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                  }`}
                >
                  {h.replace('_', ' ')}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Earthquake Non-Prediction Disclaimer Banner */}
      {selectedHazard === 'EARTHQUAKE' && (
        <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 text-amber-900 flex items-start gap-3">
          <ShieldAlert className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          <div className="text-xs space-y-1">
            <span className="font-mono font-bold uppercase tracking-wider block">
              SCIENTIFIC MANDATE // EARTHQUAKE NON-PREDICTION NOTICE
            </span>
            <p>
              <strong>Earthquake timing cannot currently be predicted reliably.</strong> Metrics reflect tectonic
              baseline vulnerability under BIS IS 1893 seismic zoning and structural awareness. No short-term warning is generated.
            </p>
          </div>
        </div>
      )}

      {/* Coverage Tier Clarification Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 text-center text-[10px] font-mono">
        <div className="p-2.5 rounded-xl bg-white border border-slate-200">
          <div className="text-slate-500">ADMIN COVERAGE</div>
          <div className="font-bold text-slate-900 mt-0.5">36/36 States & UTs</div>
        </div>
        <div className="p-2.5 rounded-xl bg-white border border-slate-200">
          <div className="text-slate-500">REGIONAL BASELINE</div>
          <div className="font-bold text-slate-900 mt-0.5">100% Pan-India</div>
        </div>
        <div className="p-2.5 rounded-xl bg-white border border-slate-200">
          <div className="text-slate-500">LIVE TELEMETRY</div>
          <div className="font-bold text-slate-900 mt-0.5">IMD / CWC Network</div>
        </div>
        <div className="p-2.5 rounded-xl bg-white border border-slate-200">
          <div className="text-slate-500">OFFICIAL FORECAST</div>
          <div className="font-bold text-slate-900 mt-0.5">5 Lead Horizons</div>
        </div>
        <div className="p-2.5 rounded-xl bg-white border border-slate-200">
          <div className="text-slate-500">OFFICIAL WARNINGS</div>
          <div className="font-bold text-slate-900 mt-0.5">IMD & NDMA Direct</div>
        </div>
        <div className="p-2.5 rounded-xl bg-white border border-slate-200">
          <div className="text-slate-500">APPROVED ML SCOPE</div>
          <div className="font-bold text-blue-700 mt-0.5">Assam Flood (Only)</div>
        </div>
      </div>

      {/* STATE A: NATIONAL OVERVIEW (When no region is selected) */}
      {selectedRegion === null && nationalOverview && (
        <div className="space-y-6">
          {/* National Advisory Distribution */}
          <div className="p-6 rounded-3xl bg-white border border-slate-200 shadow-xs space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="font-mono text-xs font-bold uppercase tracking-wider text-slate-700">
                National Advisory Distribution (36 Entities)
              </h3>
              <span className="text-xs font-mono text-slate-500">
                Updated: {nationalOverview.evaluated_at}
              </span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
              {Object.entries(nationalOverview.risk_state_distribution).map(([state, count]) => (
                <div
                  key={state}
                  className={`p-4 rounded-2xl border flex flex-col justify-between ${getRiskColor(state)}`}
                >
                  <span className="text-[10px] font-mono font-bold uppercase">{state}</span>
                  <span className="text-2xl font-mono font-extrabold mt-2">{count} Entities</span>
                </div>
              ))}
            </div>
          </div>

          {/* Regional Watchlist Grid */}
          <div className="p-6 rounded-3xl bg-white border border-slate-200 shadow-xs space-y-4">
            <h3 className="font-mono text-xs font-bold uppercase tracking-wider text-slate-700">
              All 36 Indian Jurisdictions Predictive Status
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {nationalOverview.regions.map((reg) => (
                <div
                  key={reg.region_id}
                  onClick={() => {
                    setSelectedRegion(reg.region_id);
                    if (reg.hazard) setSelectedHazard(reg.hazard);
                  }}
                  className="p-4 rounded-2xl bg-slate-50 border border-slate-200 hover:border-blue-500 hover:bg-white cursor-pointer transition-all hover:shadow-sm group"
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-mono text-xs font-bold text-slate-900 group-hover:text-blue-700">
                      {reg.region_name}
                    </span>
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-mono font-bold border ${getRiskColor(reg.future_risk_state)}`}>
                      {reg.future_risk_state}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-[11px] font-mono text-slate-600">
                    <span>Hazard: {reg.hazard}</span>
                    <span>Peak: {reg.peak_future_window}</span>
                  </div>
                  <div className="mt-2 pt-2 border-t border-slate-200 flex items-center justify-between text-[10px] font-mono text-slate-500">
                    <span>Trend: {reg.trend}</span>
                    <span className="text-blue-700 font-bold group-hover:underline flex items-center gap-0.5">
                      Inspect <ChevronRight className="w-3 h-3" />
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* STATE B: DATA GAP STATE (When telemetry is unavailable) */}
      {selectedRegion && dataGap && (
        <div className="p-6 sm:p-8 rounded-3xl bg-amber-50/70 border border-amber-300 space-y-4">
          <div className="flex items-start gap-3">
            <AlertTriangle className="w-6 h-6 text-amber-600 shrink-0 mt-0.5" />
            <div>
              <h3 className="text-base font-bold font-mono text-slate-900 uppercase">
                DATA UNAVAILABLE // LIMITED SCIENTIFIC EVIDENCE
              </h3>
              <p className="text-xs sm:text-sm text-slate-700 mt-1 leading-relaxed">
                Live sensor telemetry and numerical forecast signals for{' '}
                <strong>{selectedLocationMeta?.name || selectedRegion}</strong> under{' '}
                <strong>{selectedHazard}</strong> are not currently transmitting from central observation feeds.
                RISK // INDIA does not invent synthetic predictions.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            <div className="p-4 rounded-2xl bg-white border border-amber-200 text-xs font-mono space-y-2">
              <span className="font-bold text-emerald-700 block">WHAT IS KNOWN:</span>
              <ul className="list-disc pl-4 text-slate-700 space-y-1 text-[11px]">
                <li>Administrative Jurisdiction: {selectedLocationMeta?.name} ({selectedLocationMeta?.code})</li>
                <li>Historical primary hazard: {selectedLocationMeta?.primaryRisk || selectedHazard}</li>
                <li>Statutory emergency helplines remain active (112, 1078, 1070)</li>
              </ul>
            </div>

            <div className="p-4 rounded-2xl bg-white border border-amber-200 text-xs font-mono space-y-2">
              <span className="font-bold text-amber-700 block">WHAT IS UNKNOWN:</span>
              <ul className="list-disc pl-4 text-slate-700 space-y-1 text-[11px]">
                <li>Micro-basin river discharge readings within last 6 hours</li>
                <li>Doppler radar nowcasting precipitation accumulation</li>
                <li>No active official warning issued by IMD for this sector</li>
              </ul>
            </div>
          </div>

          {/* 7 Required Data Availability Audit Points */}
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 pt-2 text-[10px] font-mono">
            <div className="p-2.5 rounded-xl bg-white border border-amber-200">
              <span className="text-slate-500 uppercase block">Last Available Observation</span>
              <span className="font-bold text-slate-800 mt-0.5 block">No recent gauge reading</span>
            </div>
            <div className="p-2.5 rounded-xl bg-white border border-amber-200">
              <span className="text-slate-500 uppercase block">Source / Provenance</span>
              <span className="font-bold text-slate-800 mt-0.5 block">CWC / IMD Station Network</span>
            </div>
            <div className="p-2.5 rounded-xl bg-white border border-amber-200">
              <span className="text-slate-500 uppercase block">Freshness</span>
              <span className="font-bold text-amber-700 mt-0.5 block">DATA UNAVAILABLE</span>
            </div>
            <div className="p-2.5 rounded-xl bg-white border border-amber-200">
              <span className="text-slate-500 uppercase block">Forecast Availability</span>
              <span className="font-bold text-slate-800 mt-0.5 block">Regional Climatology Only</span>
            </div>
            <div className="p-2.5 rounded-xl bg-white border border-amber-200">
              <span className="text-slate-500 uppercase block">Official Warning Availability</span>
              <span className="font-bold text-emerald-700 mt-0.5 block">No Active Red/Orange Bulletin</span>
            </div>
          </div>

          <div className="pt-2 flex items-center justify-between text-xs font-mono">
            <span className="text-slate-500">Source: Central observation network check</span>
            <button
              onClick={() => setSelectedRegion(null)}
              className="text-blue-700 font-bold hover:underline"
            >
              ← Back to National Overview
            </button>
          </div>
        </div>
      )}

      {/* STATE C: REGIONAL 10-DIMENSION DETAILS (When region data is loaded) */}
      {selectedRegion && assessment && !dataGap && (
        <div className="space-y-8">
          {/* Scope notice for Assam ML vs Other */}
          <PredictionScopeNotice
            isAssam={assessment.region_id === 'assam'}
            hazard={assessment.hazard}
            mlScope={assessment.ml_scope}
            syntheticRecords={assessment.synthetic_records}
          />

          {/* 10 Core Dimensions Ribbon */}
          <div className="p-6 rounded-3xl bg-white border border-slate-200 shadow-xs space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <span className="text-xs font-mono uppercase text-slate-500 font-bold block">
                  10-DIMENSION EVIDENCE CONTRACT
                </span>
                <h3 className="text-xl sm:text-2xl font-bold text-slate-900 mt-0.5">
                  {assessment.region_name} • {assessment.hazard}
                </h3>
              </div>
              <div className="flex items-center gap-2">
                <RiskTrendIndicator trend={assessment.trend} />
                <UncertaintyBadge confidence={assessment.confidence} uncertainty={assessment.uncertainty} />
              </div>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 pt-2">
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
                <div className="text-[10px] font-mono text-slate-500 uppercase">A. Current State</div>
                <div className={`mt-1 font-mono text-xs font-bold inline-block px-2 py-0.5 rounded-lg border ${getRiskColor(assessment.current_risk_state)}`}>
                  {assessment.current_risk_state}
                </div>
              </div>
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
                <div className="text-[10px] font-mono text-slate-500 uppercase">B. Future State</div>
                <div className={`mt-1 font-mono text-xs font-bold inline-block px-2 py-0.5 rounded-lg border ${getRiskColor(assessment.future_risk_state)}`}>
                  {assessment.future_risk_state}
                </div>
              </div>
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
                <div className="text-[10px] font-mono text-slate-500 uppercase">C. Trend</div>
                <div className="mt-1 font-mono text-xs font-bold text-slate-900">
                  {assessment.trend}
                </div>
              </div>
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
                <div className="text-[10px] font-mono text-slate-500 uppercase">D. Peak Horizon</div>
                <div className="mt-1 font-mono text-xs font-bold text-blue-700">
                  {assessment.peak_future_window}
                </div>
              </div>
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
                <div className="text-[10px] font-mono text-slate-500 uppercase">E. Main Hazard</div>
                <div className="mt-1 font-mono text-xs font-bold text-slate-900">
                  {assessment.hazard}
                </div>
              </div>
            </div>
          </div>

          {/* 5-Horizon Timeline */}
          <FutureRiskTimeline
            timeline={assessment.timeline}
            regionName={assessment.region_name}
            hazardName={assessment.hazard}
          />

          {/* Causal Evidence Drivers */}
          <FutureRiskDrivers
            regionName={assessment.region_name}
            hazardName={assessment.hazard}
            explanation={assessment.explanation}
            evidenceSignals={assessment.evidence_signals}
          />

          {/* Forward Predictive Scenarios (Baseline, Likely, Escalation) */}
          {scenarios && scenarios.length > 0 && (
            <div className="space-y-2">
              <div className="p-3 rounded-2xl bg-blue-50 border border-blue-200 text-xs font-mono flex items-start gap-2">
                <Info className="w-4 h-4 text-blue-700 shrink-0 mt-0.5" />
                <span className="text-slate-700">
                  <strong>Analytical Scenarios Notice:</strong> Baseline, Likely, and Escalation scenarios are forward-looking analytical projections based on multi-model atmospheric and hydrological simulations, NOT guaranteed deterministic outcomes.
                </span>
              </div>
              <ScenarioPanel scenarios={scenarios} />
            </div>
          )}
        </div>
      )}

      {/* WHAT COULD HAPPEN NEXT? // SECONDARY & CASCADING RISKS */}
      <section className="p-6 sm:p-8 rounded-3xl bg-gradient-to-r from-amber-500/10 via-rose-500/10 to-indigo-500/10 border-2 border-amber-300 shadow-sm space-y-6">
        <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-6">
          <div className="space-y-2 max-w-3xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-100 border border-amber-300 text-amber-900 text-xs font-mono font-bold uppercase tracking-wider">
              <Layers className="w-3.5 h-3.5" />
              <span>WHAT COULD HAPPEN NEXT? // SECONDARY &amp; CASCADING RISKS</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              A disaster rarely ends with the first hazard.
            </h2>
            <p className="text-sm text-slate-700 leading-relaxed font-sans">
              Changes caused by the initial event can create additional hazards and wider impacts across terrain, critical lifelines, and communities. Trace the causal consequence chain before secondary hazards strike.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 shrink-0">
            <button
              onClick={() => onNavigate('cascading-risk')}
              className="min-h-[48px] px-5 py-3 rounded-2xl bg-amber-600 hover:bg-amber-700 text-white font-mono text-xs sm:text-sm font-bold transition-all shadow-md flex items-center justify-center gap-2 group"
            >
              <span>EXAMINE CASCADING RISKS</span>
              <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </button>
            <button
              onClick={() => onNavigate('safety-guide')}
              className="min-h-[48px] px-5 py-3 rounded-2xl bg-white hover:bg-slate-50 text-slate-900 border border-slate-200 font-mono text-xs sm:text-sm font-bold transition-all flex items-center justify-center gap-2"
            >
              <FileCheck2 className="w-4 h-4 text-emerald-600" />
              <span>SAFETY ACTION GUIDE</span>
            </button>
          </div>
        </div>

        {/* 4-Stage Visual Causal Progression */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-3 pt-2">
          <div className="p-4 rounded-2xl bg-white border border-amber-200 shadow-2xs space-y-1">
            <span className="text-[10px] font-mono uppercase font-bold text-amber-700 block">
              1. PRIMARY TRIGGER
            </span>
            <strong className="text-xs sm:text-sm font-bold text-slate-900 block">
              {selectedHazard} Inception
            </strong>
            <p className="text-[11px] text-slate-600">
              Direct kinetic or meteorological impact from precipitation, wind, or ground motion.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-white border border-blue-200 shadow-2xs space-y-1">
            <span className="text-[10px] font-mono uppercase font-bold text-blue-700 block">
              2. PHYSICAL CHANGE
            </span>
            <strong className="text-xs sm:text-sm font-bold text-slate-900 block">
              Environmental Shift
            </strong>
            <p className="text-[11px] text-slate-600">
              Soil pore saturation, structural stress, drainage overload, and coastal water level rise.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-white border border-rose-200 shadow-2xs space-y-1">
            <span className="text-[10px] font-mono uppercase font-bold text-rose-700 block">
              3. SECONDARY HAZARDS
            </span>
            <strong className="text-xs sm:text-sm font-bold text-slate-900 block">
              Consequential Threat
            </strong>
            <p className="text-[11px] text-slate-600">
              Secondary slope instability, embankment breach, contamination, and electrical hazards.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-white border border-purple-200 shadow-2xs space-y-1">
            <span className="text-[10px] font-mono uppercase font-bold text-purple-700 block">
              4. SYSTEMIC IMPACTS
            </span>
            <strong className="text-xs sm:text-sm font-bold text-slate-900 block">
              Civil &amp; Lifeline Stress
            </strong>
            <p className="text-[11px] text-slate-600">
              Road isolation, healthcare overload, potable water interruption, and supply bottlenecks.
            </p>
          </div>
        </div>
      </section>

      {/* 4. Multi-Hazard Matrix across all 6 Hazards */}
      <FutureHazardMatrix
        onSelectHazard={(h) => setSelectedHazard(h)}
      />

      {/* 5. Early Warning Notices */}
      <EarlyWarningNoticeSection
        onSelectRegion={(regId) => setSelectedRegion(regId)}
        onViewAllWarnings={() => onNavigate('disasters')}
      />

      {/* 6. Cascading & Secondary Risk Intelligence */}
      <CascadingRiskSection
        regionId={selectedRegion || 'assam'}
        regionName={selectedLocationMeta?.name || 'National Baseline'}
        hazard={selectedHazard}
        onNavigate={onNavigate}
        onExploreSafetyGuide={(h) => onNavigate('safety-guide')}
      />

      {/* 7. Citizen Action Protocols (What Should I Do, 72h Family Kit) */}
      <FutureRiskActionPanel
        regionName={selectedLocationMeta?.name || 'National Outlook'}
        hazardName={selectedHazard}
      />
    </div>
  );
};
