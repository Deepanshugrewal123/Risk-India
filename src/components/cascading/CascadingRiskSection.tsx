import React, { useState, useEffect } from 'react';
import {
  GitBranch,
  ArrowRight,
  ArrowDown,
  AlertTriangle,
  ShieldCheck,
  Eye,
  HelpCircle,
  Activity,
  Layers,
  Sparkles,
  Info,
  CheckCircle2,
  AlertOctagon,
  ChevronDown,
  ChevronUp,
  ExternalLink
} from 'lucide-react';
import { CascadingRiskAssessment, CascadingStage, EvidencePosture } from '../../types/cascadingRisk';
import { cascadingRiskService } from '../../services/cascadingRiskService';

interface CascadingRiskSectionProps {
  regionId?: string;
  regionName?: string;
  hazard?: string;
}

export const CascadingRiskSection: React.FC<CascadingRiskSectionProps> = ({
  regionId = 'assam',
  regionName = 'Assam',
  hazard = 'FLOOD'
}) => {
  const [assessment, setAssessment] = useState<CascadingRiskAssessment | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [expandedStage, setExpandedStage] = useState<number | null>(null);

  useEffect(() => {
    let isMounted = true;
    const loadCascadingRisk = async () => {
      try {
        setLoading(true);
        const data = await cascadingRiskService.getRegionCascadingRisk(regionId, hazard);
        if (isMounted) {
          setAssessment(data);
          // Default expand secondary hazard stage (stage 3) or stage 1
          setExpandedStage(3);
        }
      } catch (err) {
        console.error('Failed to load cascading risk assessment:', err);
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    loadCascadingRisk();
    return () => {
      isMounted = false;
    };
  }, [regionId, hazard]);

  const activeChain = assessment?.chains?.[0];

  const getEvidenceBadge = (posture: EvidencePosture) => {
    switch (posture) {
      case 'LIVE_EVIDENCE':
        return {
          label: 'LIVE EVIDENCE ACTIVE',
          bg: 'bg-rose-50 text-rose-800 border-rose-200 dark:bg-rose-950/50 dark:text-rose-300 dark:border-rose-900',
          dot: 'bg-rose-500 animate-pulse'
        };
      case 'RECENT_EVIDENCE':
        return {
          label: 'RECENT OBSERVATION',
          bg: 'bg-orange-50 text-orange-800 border-orange-200 dark:bg-orange-950/50 dark:text-orange-300 dark:border-orange-900',
          dot: 'bg-orange-500'
        };
      case 'FORECAST_AVAILABLE':
        return {
          label: 'FORECAST INDICATION',
          bg: 'bg-indigo-50 text-indigo-800 border-indigo-200 dark:bg-indigo-950/50 dark:text-indigo-300 dark:border-indigo-900',
          dot: 'bg-indigo-500'
        };
      case 'BASELINE_ONLY':
        return {
          label: 'ESTABLISHED BASELINE RELATIONSHIP',
          bg: 'bg-slate-100 text-slate-800 border-slate-300 dark:bg-slate-800 dark:text-slate-300 dark:border-slate-700',
          dot: 'bg-slate-400'
        };
      case 'LIMITED_EVIDENCE':
        return {
          label: 'LIMITED REGIONAL TELEMETRY',
          bg: 'bg-amber-50 text-amber-800 border-amber-200 dark:bg-amber-950/50 dark:text-amber-300 dark:border-amber-900',
          dot: 'bg-amber-500'
        };
      case 'DATA_UNAVAILABLE':
      default:
        return {
          label: 'DATA UNAVAILABLE (HONEST GAP)',
          bg: 'bg-zinc-100 text-zinc-700 border-zinc-300 dark:bg-zinc-800 dark:text-zinc-400 dark:border-zinc-700',
          dot: 'bg-zinc-400'
        };
    }
  };

  const getStageHeaderColor = (type: string) => {
    switch (type) {
      case 'PRIMARY_HAZARD':
        return 'border-rose-500 bg-rose-50/70 dark:bg-rose-950/30 text-rose-900 dark:text-rose-200';
      case 'PHYSICAL_CHANGE':
        return 'border-amber-500 bg-amber-50/70 dark:bg-amber-950/30 text-amber-900 dark:text-amber-200';
      case 'SECONDARY_HAZARD':
        return 'border-orange-500 bg-orange-50/70 dark:bg-orange-950/30 text-orange-900 dark:text-orange-200';
      case 'TERTIARY_CONSEQUENCE':
      default:
        return 'border-purple-500 bg-purple-50/70 dark:bg-purple-950/30 text-purple-900 dark:text-purple-200';
    }
  };

  const toggleStage = (order: number) => {
    setExpandedStage((prev) => (prev === order ? null : order));
  };

  if (loading) {
    return (
      <div className="rounded-3xl border border-paper-300 bg-white dark:bg-slate-900 p-8 text-center space-y-3">
        <div className="w-8 h-8 mx-auto border-2 border-charcoal-400 border-t-transparent rounded-full animate-spin" />
        <p className="text-xs font-mono text-charcoal-500 uppercase">
          Evaluating Geomechanical & Hydrological Consequence Chains...
        </p>
      </div>
    );
  }

  if (!activeChain) {
    return null;
  }

  const overallBadge = getEvidenceBadge(activeChain.overall_evidence_posture);

  return (
    <section
      id="cascading-risks"
      className="rounded-3xl border border-paper-300 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 sm:p-8 shadow-xl space-y-6 scroll-mt-24"
      aria-labelledby="cascading-risk-heading"
    >
      {/* 1. Header & Evidence Posture */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-6 border-b border-paper-200 dark:border-slate-800">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200 dark:border-indigo-800 text-indigo-800 dark:text-indigo-300 text-xs font-mono font-bold uppercase tracking-wider">
            <GitBranch className="w-3.5 h-3.5" />
            <span>SYSTEMIC RISK INTELLIGENCE // CAUSAL CHAIN</span>
          </div>
          <h2
            id="cascading-risk-heading"
            className="text-2xl sm:text-3xl font-extrabold text-charcoal-950 dark:text-white tracking-tight"
          >
            Cascading & Secondary Risks
          </h2>
          <p className="text-xs sm:text-sm text-charcoal-600 dark:text-slate-400 max-w-3xl">
            Answers: <em>"If this disaster occurs, what physical changes, secondary hazards, and systemic impacts could follow?"</em> Grounded in verified physical relationships with strict scientific uncertainty demarcation.
          </p>
        </div>

        {/* Global Evidence Posture Badge */}
        <div className="flex flex-wrap items-center gap-2">
          <div className={`px-3 py-1.5 rounded-xl border text-xs font-mono font-bold flex items-center gap-2 ${overallBadge.bg}`}>
            <span className={`w-2 h-2 rounded-full ${overallBadge.dot}`} />
            <span>{overallBadge.label}</span>
          </div>
        </div>
      </div>

      {/* Mandatory Invariant / Earthquake Disclaimer */}
      {activeChain.earthquake_non_prediction_notice && (
        <div className="p-4 rounded-2xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-900 text-amber-950 dark:text-amber-200 text-xs font-mono flex items-start gap-3">
          <AlertOctagon className="w-5 h-5 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <span className="font-bold uppercase tracking-wider block">Seismic Non-Prediction Guarantee</span>
            <p className="leading-relaxed">
              {activeChain.earthquake_non_prediction_notice}
            </p>
          </div>
        </div>
      )}

      {/* Terrain Sensitivity / Geotechnical Conditionality Note */}
      {activeChain.terrain_sensitivity_note && (
        <div className="p-4 rounded-2xl bg-paper-50 dark:bg-slate-800 border border-paper-200 dark:border-slate-700 text-xs text-charcoal-700 dark:text-slate-300 flex items-start gap-3">
          <Info className="w-4.5 h-4.5 text-indigo-600 dark:text-indigo-400 shrink-0 mt-0.5" />
          <div>
            <strong className="font-mono text-charcoal-900 dark:text-white uppercase">Topographical Conditionality: </strong>
            <span>{activeChain.terrain_sensitivity_note}</span>
          </div>
        </div>
      )}

      {/* 2. Visual Consequence Chain Overview Bar (Horizontal on Desktop, Vertical on Mobile) */}
      <div className="space-y-3">
        <span className="text-[11px] font-mono uppercase text-charcoal-500 dark:text-slate-400 font-bold block">
          PHYSICAL PROGRESSION TIMELINE // 4-STAGE MECHANISM
        </span>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
          {activeChain.stages.map((stage, idx) => {
            const isExpanded = expandedStage === stage.stage_order;
            const stageBadge = getEvidenceBadge(stage.evidence_posture);

            return (
              <button
                key={stage.stage_order}
                onClick={() => toggleStage(stage.stage_order)}
                className={`text-left p-4 rounded-2xl border transition-all relative flex flex-col justify-between min-h-[140px] focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-600 ${
                  isExpanded
                    ? 'bg-paper-50 dark:bg-slate-800 border-charcoal-900 dark:border-white shadow-md'
                    : 'bg-white dark:bg-slate-900 border-paper-200 dark:border-slate-800 hover:border-paper-400 dark:hover:border-slate-700'
                }`}
                aria-expanded={isExpanded}
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <span className="text-[10px] font-mono uppercase font-bold text-charcoal-500 dark:text-slate-400">
                      STAGE {stage.stage_order} // {stage.stage_type.replace('_', ' ')}
                    </span>
                    <span className={`w-2 h-2 rounded-full ${stageBadge.dot}`} />
                  </div>

                  <h3 className="text-sm font-bold text-charcoal-900 dark:text-white line-clamp-2">
                    {stage.title.split('//')[1] || stage.title}
                  </h3>

                  <p className="text-xs text-charcoal-600 dark:text-slate-400 mt-1 line-clamp-2">
                    {stage.description}
                  </p>
                </div>

                <div className="mt-3 flex items-center justify-between text-[11px] font-mono text-indigo-600 dark:text-indigo-400 font-bold pt-2 border-t border-paper-200 dark:border-slate-800">
                  <span>{isExpanded ? 'Hide Details' : 'Inspect Evidence'}</span>
                  {isExpanded ? (
                    <ChevronUp className="w-3.5 h-3.5" />
                  ) : (
                    <ChevronDown className="w-3.5 h-3.5" />
                  )}
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* 3. Detailed Expanded Inspector Panel */}
      {expandedStage !== null && (
        <div className="p-6 rounded-3xl bg-paper-50 dark:bg-slate-800/70 border border-paper-300 dark:border-slate-700 space-y-6 animate-in fade-in duration-200">
          {(() => {
            const currentStage = activeChain.stages.find((s) => s.stage_order === expandedStage);
            if (!currentStage) return null;
            const stageBadge = getEvidenceBadge(currentStage.evidence_posture);

            return (
              <div className="space-y-6">
                {/* Stage Header */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-paper-200 dark:border-slate-700">
                  <div>
                    <span className="text-xs font-mono uppercase font-bold text-indigo-600 dark:text-indigo-400 block">
                      DEEP INSPECTOR // STAGE {currentStage.stage_order}
                    </span>
                    <h3 className="text-xl font-bold text-charcoal-950 dark:text-white mt-0.5">
                      {currentStage.title}
                    </h3>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="text-[11px] font-mono px-2.5 py-1 rounded-lg bg-charcoal-100 dark:bg-slate-700 text-charcoal-800 dark:text-slate-200 font-bold">
                      {currentStage.scientific_classification.replace(/_/g, ' ')}
                    </span>
                    <span className={`text-[11px] font-mono px-2.5 py-1 rounded-lg border font-bold ${stageBadge.bg}`}>
                      {stageBadge.label}
                    </span>
                  </div>
                </div>

                {/* Primary Physical Mechanism Description */}
                <div className="text-sm text-charcoal-800 dark:text-slate-200 leading-relaxed">
                  <strong className="text-charcoal-950 dark:text-white">Physical Mechanism: </strong>
                  {currentStage.description}
                </div>

                {/* 4 Core Dimensions Matrix */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Supporting Evidence */}
                  <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-paper-200 dark:border-slate-800 space-y-2">
                    <div className="text-xs font-mono uppercase font-bold text-charcoal-700 dark:text-slate-300 flex items-center gap-2">
                      <ShieldCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                      <span>1. What Evidence Supports This Relationship?</span>
                    </div>
                    <ul className="text-xs text-charcoal-600 dark:text-slate-400 space-y-1.5 list-disc list-inside">
                      {currentStage.supporting_evidence.map((ev, i) => (
                        <li key={i} className="leading-relaxed">{ev}</li>
                      ))}
                    </ul>
                  </div>

                  {/* Conditions for Escalation */}
                  <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-paper-200 dark:border-slate-800 space-y-2">
                    <div className="text-xs font-mono uppercase font-bold text-charcoal-700 dark:text-slate-300 flex items-center gap-2">
                      <AlertTriangle className="w-4 h-4 text-amber-600 dark:text-amber-400" />
                      <span>2. Conditions That Would Increase Concern</span>
                    </div>
                    <ul className="text-xs text-charcoal-600 dark:text-slate-400 space-y-1.5 list-disc list-inside">
                      {currentStage.conditions_for_escalation.map((cond, i) => (
                        <li key={i} className="leading-relaxed">{cond}</li>
                      ))}
                    </ul>
                  </div>

                  {/* What Remains Unknown (Data Gap Honesty) */}
                  <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-paper-200 dark:border-slate-800 space-y-2">
                    <div className="text-xs font-mono uppercase font-bold text-charcoal-700 dark:text-slate-300 flex items-center gap-2">
                      <HelpCircle className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                      <span>3. What Remains Unknown or Unmonitored?</span>
                    </div>
                    <ul className="text-xs text-charcoal-600 dark:text-slate-400 space-y-1.5 list-disc list-inside">
                      {currentStage.unmonitored_or_unknown.map((gap, i) => (
                        <li key={i} className="leading-relaxed text-blue-900 dark:text-blue-300 font-medium">
                          {gap}
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Field Signs to Watch For */}
                  <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-paper-200 dark:border-slate-800 space-y-2">
                    <div className="text-xs font-mono uppercase font-bold text-charcoal-700 dark:text-slate-300 flex items-center gap-2">
                      <Eye className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                      <span>4. Field Warning Signs for Citizens</span>
                    </div>
                    <ul className="text-xs text-charcoal-600 dark:text-slate-400 space-y-1.5 list-disc list-inside">
                      {currentStage.field_warning_signs.map((sign, i) => (
                        <li key={i} className="leading-relaxed">{sign}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Immediate Defensive Actions */}
                <div className="p-4 rounded-2xl bg-emerald-50/80 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800 space-y-2">
                  <div className="text-xs font-mono uppercase font-bold text-emerald-900 dark:text-emerald-300 flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                    <span>5. Defensive Citizen Actions for This Stage</span>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                    {currentStage.defensive_actions.map((act, i) => (
                      <div key={i} className="text-xs text-emerald-950 dark:text-emerald-200 flex items-start gap-2">
                        <span className="font-mono font-bold text-emerald-700 shrink-0">→</span>
                        <span>{act}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            );
          })()}
        </div>
      )}
    </section>
  );
};

export default CascadingRiskSection;
