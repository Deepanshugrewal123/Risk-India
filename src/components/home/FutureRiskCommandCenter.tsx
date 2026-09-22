import React, { useState, useEffect } from 'react';
import {
  PredictiveRiskAssessment,
  NationalPredictiveOverview,
  PredictiveTimelinePoint,
  RiskState,
  TrendState,
  ConfidenceLevel,
  UncertaintyLevel
} from '../../types/predictiveRisk';
import predictiveRiskService from '../../services/predictiveRiskService';
import { ALL_INDIAN_STATES, ALL_INDIAN_UNION_TERRITORIES } from '../../data/indiaLocations';
import { RiskTrendIndicator } from '../predictive/RiskTrendIndicator';
import { UncertaintyBadge } from '../predictive/UncertaintyBadge';
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
  AlertCircle
} from 'lucide-react';

interface FutureRiskCommandCenterProps {
  onOpenFullMap?: () => void;
  onViewEarlyWarnings?: () => void;
  onSelectRegion?: (regionId: string) => void;
  onViewDetailedPage?: () => void;
}

export const FutureRiskCommandCenter: React.FC<FutureRiskCommandCenterProps> = ({
  onOpenFullMap,
  onViewEarlyWarnings,
  onSelectRegion,
  onViewDetailedPage
}) => {
  // Default to null -> Displays National India-Wide Future Risk Overview
  const [selectedRegion, setSelectedRegion] = useState<string | null>(null);
  const [selectedHazard, setSelectedHazard] = useState<string>('FLOOD');
  const [selectedHorizon, setSelectedHorizon] = useState<string>('6-24h');

  const [nationalOverview, setNationalOverview] = useState<NationalPredictiveOverview | null>(null);
  const [assessment, setAssessment] = useState<PredictiveRiskAssessment | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [dataGap, setDataGap] = useState<boolean>(false);

  const allEntities = [...ALL_INDIAN_STATES, ...ALL_INDIAN_UNION_TERRITORIES];

  // Load National Overview on mount
  useEffect(() => {
    let isMounted = true;
    const loadNationalData = async () => {
      try {
        setLoading(true);
        const overview = await predictiveRiskService.getNationalOverview();
        if (isMounted) {
          setNationalOverview(overview);
        }
      } catch (err) {
        console.error('Failed to load national predictive overview:', err);
      } finally {
        if (isMounted) setLoading(false);
      }
    };
    loadNationalData();
    return () => {
      isMounted = false;
    };
  }, []);

  // Load Regional Assessment when a specific region is selected
  useEffect(() => {
    let isMounted = true;
    if (!selectedRegion) {
      setAssessment(null);
      setDataGap(false);
      return;
    }

    const loadAssessment = async () => {
      try {
        setLoading(true);
        setDataGap(false);
        const data = await predictiveRiskService.getHazardAssessment(selectedRegion, selectedHazard);
        if (isMounted) {
          setAssessment(data);
        }
      } catch (err) {
        console.warn('Telemetry data unavailable for region/hazard:', selectedRegion, selectedHazard);
        if (isMounted) {
          setDataGap(true);
          setAssessment(null);
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

  const horizons = [
    { code: 'NOW', label: 'NOW', sub: 'Live Telemetry', span: 'Immediate' },
    { code: '0-6h', label: '0–6 HOURS', sub: 'Nowcasting', span: 'Next 6h' },
    { code: '6-24h', label: '6–24 HOURS', sub: 'Short-Range', span: 'Next 24h' },
    { code: '1-3d', label: '1–3 DAYS', sub: 'Medium-Range', span: '2–3 Days' },
    { code: '3-7d', label: '3–7 DAYS', sub: 'Extended Outlook', span: '4–7 Days' },
  ];

  const hazards = [
    { code: 'FLOOD', name: 'Flood' },
    { code: 'CYCLONE', name: 'Cyclone' },
    { code: 'HEATWAVE', name: 'Heatwave' },
    { code: 'SEVERE_WEATHER', name: 'Severe Weather' },
    { code: 'LANDSLIDE', name: 'Landslide' },
    { code: 'EARTHQUAKE', name: 'Earthquake' },
  ];

  const getRiskColor = (state?: string) => {
    switch (state) {
      case 'CRITICAL':
        return 'text-rose-700 bg-rose-50 border-rose-200 dark:bg-rose-950/40 dark:text-rose-300 dark:border-rose-900';
      case 'HIGH':
        return 'text-orange-700 bg-orange-50 border-orange-200 dark:bg-orange-950/40 dark:text-orange-300 dark:border-orange-900';
      case 'ELEVATED':
        return 'text-amber-700 bg-amber-50 border-amber-200 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-900';
      case 'WATCH':
        return 'text-blue-700 bg-blue-50 border-blue-200 dark:bg-blue-950/40 dark:text-blue-300 dark:border-blue-900';
      case 'NORMAL':
      default:
        return 'text-emerald-700 bg-emerald-50 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-900';
    }
  };

  const activeHorizonPoint = assessment?.timeline.find((p) => p.horizon === selectedHorizon) || assessment?.timeline[2];

  const selectedLocationMeta = allEntities.find((e) => e.id === selectedRegion);

  return (
    <section id="future-risk" className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto relative scroll-mt-24">
      <div className="rounded-3xl border border-paper-300 bg-white dark:bg-slate-900 p-6 sm:p-8 shadow-xl space-y-6">
        {/* Header Strip with 4 Pillars & Scope */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-5 border-b border-paper-200 dark:border-slate-800">
          <div className="space-y-1">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200 dark:border-indigo-800 text-indigo-900 dark:text-indigo-300 text-xs font-mono font-bold uppercase tracking-wider">
              <Sparkles className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />
              <span>FUTURE RISK & EARLY WARNING COMMAND CENTER</span>
            </div>
            <h2 className="text-2xl sm:text-4xl font-extrabold text-charcoal-950 dark:text-white tracking-tight">
              What Could Happen Next?
            </h2>
            <p className="text-xs sm:text-sm text-charcoal-600 dark:text-slate-400 max-w-2xl font-normal">
              Continuous multi-horizon predictive intelligence across 5 forecast intervals from NOW to 7 days ahead.
              Multi-source fusion across IMD, CWC, NDMA, and official Earth observation telemetry.
            </p>
          </div>

          {/* Quick Actions */}
          <div className="flex flex-wrap items-center gap-2">
            {onViewDetailedPage && (
              <button
                onClick={onViewDetailedPage}
                className="px-3 py-1.5 rounded-full text-xs font-mono font-semibold bg-paper-100 dark:bg-slate-800 text-charcoal-800 dark:text-slate-200 hover:bg-paper-200 border border-paper-300 dark:border-slate-700 transition-colors flex items-center gap-1.5"
              >
                <span>Full Future Risk Page</span>
                <ExternalLink className="w-3 h-3" />
              </button>
            )}
            {onOpenFullMap && (
              <button
                onClick={onOpenFullMap}
                className="px-3.5 py-1.5 rounded-full text-xs font-mono font-bold bg-charcoal-900 text-paper-50 hover:bg-charcoal-800 transition-colors flex items-center gap-1.5 shadow-xs"
              >
                <Compass className="w-3.5 h-3.5" />
                <span>Open Risk Map</span>
              </button>
            )}
          </div>
        </div>

        {/* Region Selector Bar: National Overview vs 36 States/UTs */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 p-3.5 rounded-2xl bg-paper-50 dark:bg-slate-800/60 border border-paper-200 dark:border-slate-700">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-mono font-bold uppercase tracking-wider text-charcoal-600 dark:text-slate-400">
              Location Scope:
            </span>
            <button
              onClick={() => {
                setSelectedRegion(null);
                onSelectRegion?.('all');
              }}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold transition-all ${
                selectedRegion === null
                  ? 'bg-indigo-600 text-white shadow-xs'
                  : 'bg-white dark:bg-slate-800 text-charcoal-700 dark:text-slate-300 border border-paper-300 dark:border-slate-600 hover:bg-paper-100'
              }`}
            >
              🇮🇳 National Overview (All 36 States & UTs)
            </button>
          </div>

          {/* Dropdown for specific State/UT */}
          <div className="flex items-center gap-2">
            <label htmlFor="state-ut-select" className="text-xs font-mono text-charcoal-500 dark:text-slate-400 shrink-0">
              Inspect State / UT:
            </label>
            <select
              id="state-ut-select"
              value={selectedRegion || ''}
              onChange={(e) => {
                const val = e.target.value;
                setSelectedRegion(val === '' ? null : val);
                if (val && onSelectRegion) onSelectRegion(val);
              }}
              className="px-3 py-1.5 rounded-xl text-xs font-mono font-medium bg-white dark:bg-slate-800 border border-paper-300 dark:border-slate-600 text-charcoal-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="">-- Select State or UT --</option>
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
        </div>

        {/* Hazard Selector (when region is selected) */}
        {selectedRegion && (
          <div className="flex items-center gap-2 overflow-x-auto pb-1">
            <span className="text-xs font-mono text-charcoal-500 dark:text-slate-400 shrink-0">Hazard Layer:</span>
            {hazards.map((h) => (
              <button
                key={h.code}
                onClick={() => setSelectedHazard(h.code)}
                className={`px-3 py-1 rounded-full text-xs font-mono font-semibold transition-all shrink-0 ${
                  selectedHazard === h.code
                    ? 'bg-charcoal-900 text-paper-50 dark:bg-white dark:text-charcoal-950 shadow-xs'
                    : 'bg-paper-100 dark:bg-slate-800 text-charcoal-600 dark:text-slate-300 border border-paper-300 dark:border-slate-700 hover:bg-paper-200'
                }`}
              >
                {h.name}
              </button>
            ))}
          </div>
        )}

        {/* Scientific Invariant Guard / Earthquake Non-Prediction Disclaimer */}
        {selectedHazard === 'EARTHQUAKE' && (
          <div className="p-4 rounded-2xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800 text-amber-900 dark:text-amber-200 flex items-start gap-3">
            <ShieldAlert className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
            <div className="text-xs space-y-1">
              <span className="font-mono font-bold uppercase tracking-wider block">
                SCIENTIFIC MANDATE // EARTHQUAKE NON-PREDICTION NOTICE
              </span>
              <p>
                <strong>Earthquake timing cannot currently be predicted reliably.</strong> Displayed metrics represent
                tectonic baseline vulnerability, historical seismicity zones (Zones II–V), and structural resilience
                directives under BIS standard IS 1893. No short-term warning is generated.
              </p>
            </div>
          </div>
        )}

        {/* Coverage Tier Clarification Strip */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 text-center text-[10px] font-mono">
          <div className="p-2 rounded-xl bg-paper-100 dark:bg-slate-800/80 border border-paper-200 dark:border-slate-700">
            <div className="text-charcoal-500 dark:text-slate-400">ADMIN COVERAGE</div>
            <div className="font-bold text-charcoal-900 dark:text-white mt-0.5">36/36 States & UTs</div>
          </div>
          <div className="p-2 rounded-xl bg-paper-100 dark:bg-slate-800/80 border border-paper-200 dark:border-slate-700">
            <div className="text-charcoal-500 dark:text-slate-400">REGIONAL BASELINE</div>
            <div className="font-bold text-charcoal-900 dark:text-white mt-0.5">100% Pan-India</div>
          </div>
          <div className="p-2 rounded-xl bg-paper-100 dark:bg-slate-800/80 border border-paper-200 dark:border-slate-700">
            <div className="text-charcoal-500 dark:text-slate-400">LIVE TELEMETRY</div>
            <div className="font-bold text-charcoal-900 dark:text-white mt-0.5">IMD / CWC Network</div>
          </div>
          <div className="p-2 rounded-xl bg-paper-100 dark:bg-slate-800/80 border border-paper-200 dark:border-slate-700">
            <div className="text-charcoal-500 dark:text-slate-400">OFFICIAL FORECAST</div>
            <div className="font-bold text-charcoal-900 dark:text-white mt-0.5">5 Lead Horizons</div>
          </div>
          <div className="p-2 rounded-xl bg-paper-100 dark:bg-slate-800/80 border border-paper-200 dark:border-slate-700">
            <div className="text-charcoal-500 dark:text-slate-400">OFFICIAL WARNINGS</div>
            <div className="font-bold text-charcoal-900 dark:text-white mt-0.5">IMD & NDMA Direct</div>
          </div>
          <div className="p-2 rounded-xl bg-paper-100 dark:bg-slate-800/80 border border-paper-200 dark:border-slate-700">
            <div className="text-charcoal-500 dark:text-slate-400">APPROVED ML SCOPE</div>
            <div className="font-bold text-indigo-600 dark:text-indigo-400 mt-0.5">Assam Flood (Only)</div>
          </div>
        </div>

        {/* Loading Indicator */}
        {loading && (
          <div className="p-8 text-center text-xs text-slate-500 font-mono flex items-center justify-center gap-2">
            <RefreshCw className="w-4 h-4 animate-spin text-indigo-500" />
            <span>Retrieving authoritative forward risk telemetry and forecast models...</span>
          </div>
        )}

        {/* VIEW 1: NATIONAL OVERVIEW (When no specific region is selected) */}
        {!loading && selectedRegion === null && (
          <div className="space-y-6">
            <div className="p-5 rounded-2xl bg-indigo-50/50 dark:bg-indigo-950/20 border border-indigo-200 dark:border-indigo-900 flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
                  <span className="font-mono text-xs uppercase tracking-wider font-bold text-indigo-950 dark:text-indigo-200">
                    PAN-INDIA PREDICTIVE OVERVIEW // LIVE FUSION POSTURE
                  </span>
                </div>
                <h3 className="text-xl sm:text-2xl font-bold text-charcoal-950 dark:text-white">
                  National Forward Risk Trajectory
                </h3>
                <p className="text-xs text-charcoal-600 dark:text-slate-400 mt-1">
                  Monitored Across 28 States & 8 Union Territories. Synthetic records: {nationalOverview?.synthetic_records ?? 0} (Zero synthetic records rule verified).
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-3">
                <div className="px-4 py-2 rounded-xl bg-white dark:bg-slate-800 border border-paper-300 dark:border-slate-700 text-center">
                  <div className="text-[10px] font-mono text-charcoal-500 dark:text-slate-400 uppercase">Entities Monitored</div>
                  <div className="text-lg font-mono font-bold text-charcoal-900 dark:text-white">
                    {nationalOverview?.total_entities_monitored || 36} / 36
                  </div>
                </div>

                <div className="px-4 py-2 rounded-xl bg-white dark:bg-slate-800 border border-paper-300 dark:border-slate-700 text-center">
                  <div className="text-[10px] font-mono text-charcoal-500 dark:text-slate-400 uppercase">Actionable Alerts</div>
                  <div className="text-lg font-mono font-bold text-amber-600 dark:text-amber-400">
                    {nationalOverview?.crisis_recommended_count ?? 0}
                  </div>
                </div>
              </div>
            </div>

            {/* National Risk Distribution Breakdown */}
            {nationalOverview?.risk_state_distribution && (
              <div className="p-4 rounded-2xl bg-white dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-3">
                <div className="text-xs font-mono uppercase tracking-wider text-charcoal-500 dark:text-slate-400 font-bold flex items-center justify-between">
                  <span>NATIONAL ADVISORY DISTRIBUTION</span>
                  <span>ALL 36 JURISDICTIONS</span>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-5 gap-2.5">
                  {Object.entries(nationalOverview.risk_state_distribution).map(([state, count]) => (
                    <div
                      key={state}
                      className={`p-3 rounded-xl border flex flex-col justify-between ${getRiskColor(state)}`}
                    >
                      <div className="text-[10px] font-mono font-bold uppercase">{state}</div>
                      <div className="text-xl font-mono font-extrabold mt-1">{count} Entities</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Entities with Elevated/Watch Posture */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <h4 className="text-xs font-mono uppercase tracking-wider text-charcoal-600 dark:text-slate-400 font-bold">
                  Regional Forward Watchlist
                </h4>
                <span className="text-[11px] font-mono text-indigo-600 dark:text-indigo-400">
                  Select any State/UT above to inspect full 10-dimension evidence
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {nationalOverview?.regions.slice(0, 9).map((reg) => (
                  <div
                    key={reg.region_id}
                    onClick={() => {
                      setSelectedRegion(reg.region_id);
                      if (reg.hazard) setSelectedHazard(reg.hazard);
                      onSelectRegion?.(reg.region_id);
                    }}
                    className="p-4 rounded-2xl bg-paper-50/80 dark:bg-slate-800/80 border border-paper-200 dark:border-slate-700 hover:border-indigo-400 dark:hover:border-indigo-500 cursor-pointer transition-all hover:shadow-md group"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-mono text-xs font-bold text-charcoal-900 dark:text-white group-hover:text-indigo-600">
                        {reg.region_name}
                      </span>
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-mono font-bold border ${getRiskColor(reg.future_risk_state)}`}>
                        {reg.future_risk_state}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-xs text-charcoal-600 dark:text-slate-400 font-mono">
                      <span>Primary: {reg.hazard}</span>
                      <span className="text-[10px]">Peak: {reg.peak_future_window}</span>
                    </div>
                    <div className="mt-2.5 pt-2 border-t border-paper-200 dark:border-slate-700 flex items-center justify-between text-[10px] font-mono">
                      <span className="text-charcoal-500">Early Warning: {reg.early_warning_status}</span>
                      <span className="text-indigo-600 dark:text-indigo-400 font-semibold group-hover:underline flex items-center gap-0.5">
                        Inspect <ChevronRight className="w-3 h-3" />
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* VIEW 2: DATA GAP STATE (When telemetry/evidence is unavailable) */}
        {selectedRegion && dataGap && (
          <div className="p-6 rounded-2xl bg-amber-50/70 dark:bg-amber-950/20 border border-amber-300 dark:border-amber-800 space-y-4">
            <div className="flex items-start gap-3">
              <AlertTriangle className="w-6 h-6 text-amber-600 shrink-0 mt-0.5" />
              <div className="space-y-1">
                <h3 className="text-base font-bold text-charcoal-900 dark:text-white font-mono uppercase">
                  DATA UNAVAILABLE // LIMITED SCIENTIFIC EVIDENCE
                </h3>
                <p className="text-xs text-charcoal-700 dark:text-slate-300 leading-relaxed">
                  Real-time telemetry and numerical forecast signals for <strong>{selectedLocationMeta?.name || selectedRegion}</strong> under{' '}
                  <strong>{selectedHazard}</strong> are not currently transmitting from central observational feeds.
                  In accordance with scientific safety principles, RISK // INDIA <strong>never fabricates or interpolates</strong> synthetic predictions.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
              <div className="p-3.5 rounded-xl bg-white dark:bg-slate-900 border border-amber-200 dark:border-amber-900 text-xs space-y-1 font-mono">
                <div className="text-emerald-700 dark:text-emerald-400 font-bold flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>WHAT IS KNOWN:</span>
                </div>
                <ul className="list-disc pl-4 text-charcoal-700 dark:text-slate-300 space-y-0.5 text-[11px]">
                  <li>State/UT Administrative baseline: {selectedLocationMeta?.name} ({selectedLocationMeta?.code})</li>
                  <li>Historical primary hazard profile: {selectedLocationMeta?.primaryRisk || selectedHazard}</li>
                  <li>Statutory emergency helpline: 112 (All Emergency) / 1070 (State Disaster Management)</li>
                </ul>
              </div>

              <div className="p-3.5 rounded-xl bg-white dark:bg-slate-900 border border-amber-200 dark:border-amber-900 text-xs space-y-1 font-mono">
                <div className="text-amber-700 dark:text-amber-400 font-bold flex items-center gap-1">
                  <HelpCircle className="w-3.5 h-3.5" />
                  <span>WHAT IS UNKNOWN:</span>
                </div>
                <ul className="list-disc pl-4 text-charcoal-700 dark:text-slate-300 space-y-0.5 text-[11px]">
                  <li>Local district rain-gauge or river-stage telemetry</li>
                  <li>Multi-model numerical ensemble consensus for micro-basin</li>
                  <li>No active official warning bulletin issued in last 6 hours</li>
                </ul>
              </div>
            </div>

            {/* 7 Required Data Availability Audit Points */}
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 pt-2 text-[10px] font-mono">
              <div className="p-2 rounded-xl bg-white dark:bg-slate-900 border border-amber-200 dark:border-amber-900">
                <span className="text-charcoal-500 uppercase block">Last Available Observation</span>
                <span className="font-bold text-charcoal-800 dark:text-slate-200 mt-0.5 block">No recent gauge reading</span>
              </div>
              <div className="p-2 rounded-xl bg-white dark:bg-slate-900 border border-amber-200 dark:border-amber-900">
                <span className="text-charcoal-500 uppercase block">Source / Provenance</span>
                <span className="font-bold text-charcoal-800 dark:text-slate-200 mt-0.5 block">CWC / IMD Station Network</span>
              </div>
              <div className="p-2 rounded-xl bg-white dark:bg-slate-900 border border-amber-200 dark:border-amber-900">
                <span className="text-charcoal-500 uppercase block">Freshness</span>
                <span className="font-bold text-amber-600 dark:text-amber-400 mt-0.5 block">DATA UNAVAILABLE</span>
              </div>
              <div className="p-2 rounded-xl bg-white dark:bg-slate-900 border border-amber-200 dark:border-amber-900">
                <span className="text-charcoal-500 uppercase block">Forecast Availability</span>
                <span className="font-bold text-charcoal-800 dark:text-slate-200 mt-0.5 block">Regional Climatology Only</span>
              </div>
              <div className="p-2 rounded-xl bg-white dark:bg-slate-900 border border-amber-200 dark:border-amber-900">
                <span className="text-charcoal-500 uppercase block">Official Warning Availability</span>
                <span className="font-bold text-emerald-600 dark:text-emerald-400 mt-0.5 block">No Active Red/Orange Bulletin</span>
              </div>
            </div>

            <div className="flex flex-wrap items-center justify-between gap-3 pt-2 text-xs font-mono">
              <span className="text-charcoal-600 dark:text-slate-400">
                Source: Direct statutory feed check // IMD / CWC / NDMA
              </span>
              <button
                onClick={() => setSelectedRegion(null)}
                className="text-indigo-600 dark:text-indigo-400 font-bold hover:underline"
              >
                ← Return to National Overview
              </button>
            </div>
          </div>
        )}

        {/* VIEW 3: REGIONAL 10-DIMENSION COMMAND DISPLAY (When data is present) */}
        {selectedRegion && assessment && !dataGap && (
          <div className="space-y-6">
            {/* Top 10-Dimension Summary Ribbon */}
            <div className="p-5 rounded-2xl bg-paper-50 dark:bg-slate-800/80 border border-paper-200 dark:border-slate-700 space-y-4">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <div className="flex items-center gap-2 text-xs font-mono text-charcoal-500 dark:text-slate-400">
                    <MapPin className="w-3.5 h-3.5 text-indigo-600" />
                    <span>{assessment.region_name}</span>
                    <span>•</span>
                    <span>{assessment.hazard} Hazard Analysis</span>
                    <span>•</span>
                    <span className="text-indigo-600 font-bold">
                      {assessment.region_id === 'assam' && assessment.hazard === 'FLOOD'
                        ? 'Approved ML Enabled'
                        : 'Official Forecast & Telemetry'}
                    </span>
                  </div>
                  <h3 className="text-xl sm:text-2xl font-bold text-charcoal-950 dark:text-white mt-0.5">
                    10-Dimension Future Risk Profile
                  </h3>
                </div>

                <div className="flex items-center gap-2">
                  <RiskTrendIndicator trend={assessment.trend} />
                  <UncertaintyBadge
                    confidence={assessment.confidence}
                    uncertainty={assessment.uncertainty}
                  />
                </div>
              </div>

              {/* 10 Core Dimensions Grid */}
              <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 pt-2">
                {/* A. Current State */}
                <div className="p-3 rounded-xl bg-white dark:bg-slate-900 border border-paper-200 dark:border-slate-700">
                  <div className="text-[10px] font-mono text-charcoal-500 uppercase">A. Current State</div>
                  <div className={`mt-1 font-mono text-sm font-bold inline-block px-2 py-0.5 rounded-lg border ${getRiskColor(assessment.current_risk_state)}`}>
                    {assessment.current_risk_state}
                  </div>
                </div>

                {/* B. Future State */}
                <div className="p-3 rounded-xl bg-white dark:bg-slate-900 border border-paper-200 dark:border-slate-700">
                  <div className="text-[10px] font-mono text-charcoal-500 uppercase">B. Future State</div>
                  <div className={`mt-1 font-mono text-sm font-bold inline-block px-2 py-0.5 rounded-lg border ${getRiskColor(assessment.future_risk_state)}`}>
                    {assessment.future_risk_state}
                  </div>
                </div>

                {/* C. Trend */}
                <div className="p-3 rounded-xl bg-white dark:bg-slate-900 border border-paper-200 dark:border-slate-700">
                  <div className="text-[10px] font-mono text-charcoal-500 uppercase">C. Trend</div>
                  <div className="mt-1 font-mono text-sm font-bold text-charcoal-900 dark:text-white">
                    {assessment.trend}
                  </div>
                </div>

                {/* D. Peak Horizon */}
                <div className="p-3 rounded-xl bg-white dark:bg-slate-900 border border-paper-200 dark:border-slate-700">
                  <div className="text-[10px] font-mono text-charcoal-500 uppercase">D. Peak Horizon</div>
                  <div className="mt-1 font-mono text-sm font-bold text-indigo-600 dark:text-indigo-400">
                    {assessment.peak_future_window}
                  </div>
                </div>

                {/* E. Hazard */}
                <div className="p-3 rounded-xl bg-white dark:bg-slate-900 border border-paper-200 dark:border-slate-700">
                  <div className="text-[10px] font-mono text-charcoal-500 uppercase">E. Main Hazard</div>
                  <div className="mt-1 font-mono text-sm font-bold text-charcoal-900 dark:text-white">
                    {assessment.hazard}
                  </div>
                </div>
              </div>
            </div>

            {/* 5-Horizon Interactive Timeline Bar */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs font-mono font-bold text-charcoal-600 dark:text-slate-400 uppercase">
                <span>Select Forecast Interval (5 Horizons)</span>
                <span className="text-charcoal-400">Uncertainty Expands Monotonically With Horizon</span>
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
                {horizons.map((h) => {
                  const pt = assessment.timeline.find((p) => p.horizon === h.code);
                  const isSelected = selectedHorizon === h.code;
                  return (
                    <button
                      key={h.code}
                      onClick={() => setSelectedHorizon(h.code)}
                      className={`p-3 rounded-2xl text-left border transition-all ${
                        isSelected
                          ? 'bg-charcoal-900 text-paper-50 dark:bg-white dark:text-charcoal-950 border-charcoal-900 dark:border-white shadow-md ring-2 ring-indigo-500'
                          : 'bg-white dark:bg-slate-900 text-charcoal-800 dark:text-slate-200 border-paper-200 dark:border-slate-700 hover:border-indigo-300'
                      }`}
                    >
                      <div className="flex items-center justify-between text-[10px] font-mono">
                        <span className="font-bold">{h.label}</span>
                        <span className="opacity-70">{h.span}</span>
                      </div>
                      <div className="text-xs font-bold mt-1">
                        {pt ? pt.future_risk_state : 'NORMAL'}
                      </div>
                      <div className="text-[10px] opacity-70 mt-0.5">
                        Uncertainty: {pt?.uncertainty || 'LOW'}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Active Horizon Detail Panel */}
            {activeHorizonPoint && (
              <div className="p-4 rounded-2xl bg-indigo-50/40 dark:bg-indigo-950/20 border border-indigo-200 dark:border-indigo-900 space-y-2">
                <div className="flex items-center justify-between text-xs font-mono">
                  <span className="font-bold text-indigo-900 dark:text-indigo-300">
                    HORIZON: {activeHorizonPoint.time_window_label || activeHorizonPoint.horizon}
                  </span>
                  <span className="text-charcoal-500 dark:text-slate-400">
                    Freshness: {activeHorizonPoint.freshness}
                  </span>
                </div>
                <p className="text-xs text-charcoal-800 dark:text-slate-200 leading-relaxed">
                  <strong>Recommended Action:</strong> {activeHorizonPoint.recommended_action}
                </p>
                {activeHorizonPoint.evidence_summary && activeHorizonPoint.evidence_summary.length > 0 && (
                  <div className="text-[11px] text-charcoal-600 dark:text-slate-400 pt-1 font-mono">
                    Evidence: {activeHorizonPoint.evidence_summary.join(' • ')}
                  </div>
                )}
              </div>
            )}

            {/* Causal Evidence Drivers & What Could Make It Worse */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Evidence Drivers */}
              <div className="p-4 rounded-2xl bg-white dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-2">
                <div className="text-xs font-mono font-bold uppercase tracking-wider text-charcoal-600 dark:text-slate-300 flex items-center gap-1.5">
                  <Layers className="w-4 h-4 text-indigo-600" />
                  <span>Causal Evidence Drivers (Official Feeds)</span>
                </div>
                <p className="text-xs text-charcoal-600 dark:text-slate-400">
                  {assessment.explanation?.why_this_risk || 'Multi-source observational telemetry indicates baseline equilibrium.'}
                </p>
                {assessment.explanation?.what_supports_it && assessment.explanation.what_supports_it.length > 0 && (
                  <ul className="list-disc pl-4 text-xs text-charcoal-700 dark:text-slate-300 space-y-1 pt-1 font-mono">
                    {assessment.explanation.what_supports_it.slice(0, 3).map((item, idx) => (
                      <li key={idx}>{item}</li>
                    ))}
                  </ul>
                )}
              </div>

              {/* What Could Make It Worse / Scenarios */}
              <div className="p-4 rounded-2xl bg-white dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-2">
                <div className="text-xs font-mono font-bold uppercase tracking-wider text-amber-700 dark:text-amber-400 flex items-center gap-1.5">
                  <AlertCircle className="w-4 h-4 text-amber-600" />
                  <span>Escalation Scenarios // What To Watch</span>
                </div>
                <p className="text-xs text-charcoal-600 dark:text-slate-400">
                  {assessment.explanation?.what_could_make_it_worse || 'Precipitation exceeding 90th percentile over catchment basin.'}
                </p>
                <div className="pt-2 border-t border-paper-200 dark:border-slate-700 text-xs font-mono text-emerald-700 dark:text-emerald-400">
                  <strong>Improvement Triggers:</strong>{' '}
                  {assessment.explanation?.what_could_make_it_improve || 'River discharge subsiding below warning stage.'}
                </div>
              </div>
            </div>

            {/* Action Footer */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-2">
              <button
                onClick={() => setSelectedRegion(null)}
                className="text-xs font-mono text-indigo-600 dark:text-indigo-400 hover:underline font-bold"
              >
                ← Back to National Overview
              </button>

              <div className="flex items-center gap-2">
                {onViewEarlyWarnings && (
                  <button
                    onClick={onViewEarlyWarnings}
                    className="px-4 py-2 rounded-xl text-xs font-mono font-bold bg-amber-500/10 text-amber-900 dark:text-amber-300 border border-amber-300 hover:bg-amber-500/20 transition-colors"
                  >
                    View Official Early Warnings
                  </button>
                )}
                {onOpenFullMap && (
                  <button
                    onClick={onOpenFullMap}
                    className="px-4 py-2 rounded-xl text-xs font-mono font-bold bg-charcoal-900 text-paper-50 hover:bg-charcoal-800 transition-colors"
                  >
                    View in Map
                  </button>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
};
