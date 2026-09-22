import React, { useState, useEffect } from 'react';
import {
  NationalPredictiveOverview,
  PredictiveRiskAssessment
} from '../../types/predictiveRisk';
import predictiveRiskService from '../../services/predictiveRiskService';
import UncertaintyBadge from './UncertaintyBadge';
import RiskTrendIndicator from './RiskTrendIndicator';
import PredictionScopeNotice from './PredictionScopeNotice';
import RiskForecastTimeline from './RiskForecastTimeline';
import EvidenceConvergencePanel from './EvidenceConvergencePanel';
import ScenarioPanel from './ScenarioPanel';
import EarlyWarningPanel from './EarlyWarningPanel';
import RiskExplanationCard from './RiskExplanationCard';
import HazardForecastCard from './HazardForecastCard';
import {
  Globe,
  AlertTriangle,
  Search,
  ShieldCheck,
  Radio,
  Layers,
  Sparkles,
  RefreshCw,
  ChevronRight
} from 'lucide-react';

export const NationalFutureRisk: React.FC = () => {
  const [overview, setOverview] = useState<NationalPredictiveOverview | null>(null);
  const [selectedRegion, setSelectedRegion] = useState<string>('delhi');
  const [selectedHazard, setSelectedHazard] = useState<string>('HEATWAVE');
  const [assessment, setAssessment] = useState<PredictiveRiskAssessment | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const [assessmentLoading, setAssessmentLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Load National Overview
  const fetchOverview = async () => {
    try {
      setLoading(true);
      const data = await predictiveRiskService.getNationalOverview();
      setOverview(data);
      if (data.regions.length > 0 && !selectedRegion) {
        setSelectedRegion(data.regions[0].region_id);
        setSelectedHazard(data.regions[0].hazard);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load national predictive risk overview');
    } finally {
      setLoading(false);
    }
  };

  // Load Regional Hazard Assessment
  const fetchAssessment = async (regionId: string, hazard: string) => {
    try {
      setAssessmentLoading(true);
      const data = await predictiveRiskService.getHazardAssessment(regionId, hazard);
      setAssessment(data);
    } catch (err: any) {
      console.error('Error fetching hazard assessment:', err);
    } finally {
      setAssessmentLoading(false);
    }
  };

  useEffect(() => {
    fetchOverview();
  }, []);

  useEffect(() => {
    if (selectedRegion) {
      fetchAssessment(selectedRegion, selectedHazard);
    }
  }, [selectedRegion, selectedHazard]);

  const handleSelectRegion = (regionId: string, defaultHazard?: string) => {
    setSelectedRegion(regionId);
    if (defaultHazard) {
      setSelectedHazard(defaultHazard);
    }
  };

  const filteredRegions =
    overview?.regions.filter((r) =>
      r.region_name.toLowerCase().includes(searchQuery.toLowerCase())
    ) || [];

  if (loading && !overview) {
    return (
      <div className="flex flex-col items-center justify-center p-12 space-y-3">
        <RefreshCw className="w-8 h-8 text-indigo-500 animate-spin" />
        <span className="text-sm font-semibold text-slate-600 dark:text-slate-400">
          Fusing national multi-hazard predictive models across 36 entities...
        </span>
      </div>
    );
  }

  if (error && !overview) {
    return (
      <div className="p-6 rounded-xl border border-rose-500/30 bg-rose-500/10 text-rose-800 dark:text-rose-200 space-y-2">
        <div className="flex items-center gap-2 font-bold">
          <AlertTriangle className="w-5 h-5" />
          <span>Error Loading National Predictive Risk Engine</span>
        </div>
        <p className="text-xs">{error}</p>
        <button
          onClick={fetchOverview}
          className="px-3 py-1.5 rounded-lg bg-rose-600 text-white text-xs font-semibold hover:bg-rose-700 transition-colors"
        >
          Retry Connection
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-sm space-y-4">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="p-2 rounded-xl bg-indigo-500/10 text-indigo-600 dark:text-indigo-400">
                <Globe className="w-5 h-5" />
              </span>
              <div>
                <h2 className="text-lg font-black tracking-tight text-slate-900 dark:text-slate-100 flex items-center gap-2">
                  <span>NATIONAL PREDICTIVE RISK FUSION ENGINE</span>
                  <span className="text-xs px-2 py-0.5 rounded font-mono font-bold bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/20">
                    PHASE 30F
                  </span>
                </h2>
                <p className="text-xs text-slate-500">
                  Authoritative multi-hazard forecast convergence across 28 States & 8 Union
                  Territories
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2 flex-wrap">
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-mono font-semibold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
              <ShieldCheck className="w-3.5 h-3.5" />
              Synthetic Records: {overview?.synthetic_records ?? 0}
            </span>
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-mono font-semibold bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
              <Layers className="w-3.5 h-3.5 text-indigo-500" />
              Entities: {overview?.total_entities_monitored} (28S + 8UT)
            </span>
            <button
              onClick={fetchOverview}
              className="p-1.5 rounded-lg border border-slate-200 dark:border-slate-800 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-400 transition-colors"
              title="Refresh national overview"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* National Risk & Trend Distribution */}
        {overview && (
          <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 gap-2 pt-2 border-t border-slate-100 dark:border-slate-800 text-xs">
            <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200/60 dark:border-slate-800">
              <span className="text-[11px] text-slate-400 block font-mono">NORMAL</span>
              <span className="text-base font-bold text-emerald-600">
                {overview.risk_state_distribution['NORMAL'] || 0}
              </span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200/60 dark:border-slate-800">
              <span className="text-[11px] text-slate-400 block font-mono">WATCH</span>
              <span className="text-base font-bold text-blue-600">
                {overview.risk_state_distribution['WATCH'] || 0}
              </span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200/60 dark:border-slate-800">
              <span className="text-[11px] text-slate-400 block font-mono">ELEVATED</span>
              <span className="text-base font-bold text-amber-600">
                {overview.risk_state_distribution['ELEVATED'] || 0}
              </span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200/60 dark:border-slate-800">
              <span className="text-[11px] text-slate-400 block font-mono">HIGH</span>
              <span className="text-base font-bold text-orange-600">
                {overview.risk_state_distribution['HIGH'] || 0}
              </span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200/60 dark:border-slate-800">
              <span className="text-[11px] text-slate-400 block font-mono">CRITICAL</span>
              <span className="text-base font-bold text-rose-600">
                {overview.risk_state_distribution['CRITICAL'] || 0}
              </span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200/60 dark:border-slate-800">
              <span className="text-[11px] text-slate-400 block font-mono">RISING TREND</span>
              <span className="text-base font-bold text-indigo-600">
                {overview.trend_distribution['RISING'] || 0}
              </span>
            </div>
          </div>
        )}

        {/* Crisis Mode Recommendation Banner */}
        {overview && overview.crisis_recommended_count > 0 && (
          <div className="p-3.5 rounded-xl border border-rose-500 bg-rose-50 dark:bg-rose-950/40 text-rose-900 dark:text-rose-100 text-xs flex items-center justify-between flex-wrap gap-2">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-rose-600 dark:text-rose-400 shrink-0" />
              <span>
                <strong>CRISIS MODE RECOMMENDED:</strong> {overview.crisis_recommended_count} entities
                demonstrate severe multi-hazard convergence requiring heightened public assistance.
              </span>
            </div>
            <div className="flex items-center gap-1.5 flex-wrap">
              {overview.crisis_recommended_entities.map((cr) => (
                <button
                  key={cr.region_id}
                  onClick={() => handleSelectRegion(cr.region_id, cr.hazard)}
                  className="px-2 py-0.5 rounded font-mono text-[11px] bg-rose-600 text-white hover:bg-rose-700"
                >
                  {cr.region_name} ({cr.hazard})
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Main Two-Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: 36 Entity Browser */}
        <div className="lg:col-span-4 space-y-3">
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100">
                Monitored Entities (36)
              </h3>
              <span className="text-xs text-slate-500 font-mono">Live Fusion</span>
            </div>

            {/* Search Input */}
            <div className="relative">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Filter state or UT..."
                className="w-full pl-9 pr-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-850 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            {/* Entity List */}
            <div className="space-y-1.5 max-h-[560px] overflow-y-auto pr-1">
              {filteredRegions.map((reg) => {
                const isSelected = reg.region_id === selectedRegion;

                return (
                  <button
                    key={reg.region_id}
                    onClick={() => handleSelectRegion(reg.region_id, reg.hazard)}
                    className={`w-full flex items-center justify-between p-2.5 rounded-xl border text-left transition-all ${
                      isSelected
                        ? 'border-indigo-500 ring-2 ring-indigo-500/20 bg-indigo-50/50 dark:bg-indigo-950/40 shadow-xs'
                        : 'border-slate-100 dark:border-slate-800/80 hover:border-slate-200 dark:hover:border-slate-700 bg-slate-50/40 dark:bg-slate-850/40'
                    }`}
                  >
                    <div className="min-w-0 pr-2">
                      <div className="flex items-center gap-1.5">
                        <span className="text-xs font-bold text-slate-900 dark:text-slate-100 truncate">
                          {reg.region_name}
                        </span>
                        <span className="text-[10px] font-mono text-slate-400">
                          ({reg.region_type === 'UNION_TERRITORY' ? 'UT' : 'ST'})
                        </span>
                      </div>
                      <div className="flex items-center gap-1.5 text-[11px] text-slate-500 mt-0.5">
                        <span>{reg.hazard}</span>
                        <span>•</span>
                        <span>Peak: {reg.peak_future_score}</span>
                      </div>
                    </div>

                    <div className="flex items-center gap-1.5 shrink-0">
                      <RiskTrendIndicator trend={reg.trend as any} showText={false} size="sm" />
                      <span
                        className={`px-1.5 py-0.5 rounded text-[10px] font-bold font-mono ${
                          reg.future_risk_state === 'CRITICAL'
                            ? 'bg-rose-600 text-white'
                            : reg.future_risk_state === 'HIGH'
                            ? 'bg-orange-600 text-white'
                            : reg.future_risk_state === 'ELEVATED'
                            ? 'bg-amber-600 text-white'
                            : reg.future_risk_state === 'WATCH'
                            ? 'bg-blue-600 text-white'
                            : 'bg-emerald-600 text-white'
                        }`}
                      >
                        {reg.future_risk_state}
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Right Column: Detailed Regional Predictive Risk Intelligence */}
        <div className="lg:col-span-8 space-y-4">
          {assessmentLoading && (
            <div className="p-8 text-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-500 text-xs flex items-center justify-center gap-2">
              <RefreshCw className="w-4 h-4 animate-spin text-indigo-500" />
              <span>Updating predictive multi-hazard projection...</span>
            </div>
          )}

          {assessment && !assessmentLoading && (
            <>
              {/* Scope Notice (Assam ML & Earthquake Guards) */}
              <PredictionScopeNotice
                isAssam={assessment.region_id === 'assam'}
                hazard={assessment.hazard}
                mlScope={assessment.ml_scope}
                syntheticRecords={assessment.synthetic_records}
              />

              {/* Multi-Hazard Selector & Score Overview */}
              <HazardForecastCard
                currentHazard={assessment.hazard}
                onSelectHazard={(h) => setSelectedHazard(h)}
                currentRiskState={assessment.current_risk_state}
                currentScore={assessment.current_risk_score}
                futureRiskState={assessment.future_risk_state}
                peakScore={assessment.peak_future_score}
                peakWindow={assessment.peak_future_window}
                trend={assessment.trend}
                confidence={assessment.confidence}
                uncertainty={assessment.uncertainty}
              />

              {/* 5-Horizon Predictive Timeline */}
              <RiskForecastTimeline
                timeline={assessment.timeline}
                hazard={assessment.hazard}
              />

              {/* Early Warning Panel (Separates Prepare from Evacuate) */}
              <EarlyWarningPanel
                earlyWarning={assessment.early_warning}
                hazard={assessment.hazard}
              />

              {/* Forward Scenarios (Baseline, Likely, Escalation) */}
              <ScenarioPanel scenarios={assessment.scenarios} />

              {/* Evidence Convergence & Conflicting Signals */}
              <EvidenceConvergencePanel
                signals={assessment.evidence_signals}
                hasConflictingEvidence={assessment.has_conflicting_evidence}
                conflictingSignals={assessment.conflicting_signals}
                conflictResolutionNotes={assessment.conflict_resolution_notes}
                overallFreshness={assessment.overall_freshness}
              />

              {/* 12 Citizen Safety Questions & Scientific Reasoning */}
              <RiskExplanationCard
                explanation={assessment.explanation}
                regionName={assessment.region_name}
                hazard={assessment.hazard}
              />
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default NationalFutureRisk;
