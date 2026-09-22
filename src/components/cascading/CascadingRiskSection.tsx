import React, { useState, useEffect } from 'react';
import {
  GitBranch,
  ArrowRight,
  ShieldCheck,
  Eye,
  AlertTriangle,
  AlertOctagon,
  ChevronDown,
  ChevronUp,
  Activity,
  Compass,
  Info,
  Layers,
  Sparkles,
  HelpCircle,
  ExternalLink,
  BookOpen
} from 'lucide-react';
import { CascadingRiskAssessment, CascadingStage, EvidencePosture } from '../../types/cascadingRisk';
import { cascadingRiskService } from '../../services/cascadingRiskService';
import { NavigationPage } from '../common/Navbar';

interface CascadingRiskSectionProps {
  regionId?: string;
  regionName?: string;
  hazard?: string;
  onNavigate?: (page: NavigationPage) => void;
  onExploreSafetyGuide?: (hazard: string) => void;
}

export const CascadingRiskSection: React.FC<CascadingRiskSectionProps> = ({
  regionId = 'assam',
  regionName = 'Assam',
  hazard = 'FLOOD',
  onNavigate,
  onExploreSafetyGuide
}) => {
  const [assessment, setAssessment] = useState<CascadingRiskAssessment | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [expandedStage, setExpandedStage] = useState<number | null>(3); // Default expand stage 3 (Secondary Hazard)

  useEffect(() => {
    let isMounted = true;
    const loadCascadingRisk = async () => {
      try {
        setLoading(true);
        const data = await cascadingRiskService.getRegionCascadingRisk(regionId, hazard);
        if (isMounted) {
          setAssessment(data);
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

  const getStageTitle = (order: number, type: string) => {
    switch (order) {
      case 1:
        return { subtitle: 'STEP 1 OF 4 // PRIMARY HAZARD', question: 'What is happening?' };
      case 2:
        return { subtitle: 'STEP 2 OF 4 // PHYSICAL CHANGE', question: 'What changes because of it?' };
      case 3:
        return { subtitle: 'STEP 3 OF 4 // SECONDARY HAZARD', question: 'What additional hazard could emerge?' };
      case 4:
      default:
        return { subtitle: 'STEP 4 OF 4 // SYSTEMIC IMPACT', question: 'What does this mean for people & services?' };
    }
  };

  const toggleStage = (order: number) => {
    setExpandedStage((prev) => (prev === order ? null : order));
  };

  if (loading) {
    return (
      <div className="rounded-3xl border border-paper-300 dark:border-slate-800 bg-white dark:bg-slate-900 p-8 text-center space-y-3">
        <div className="w-8 h-8 mx-auto border-2 border-indigo-600 border-t-transparent rounded-full animate-spin" />
        <p className="text-xs font-mono text-charcoal-500 dark:text-slate-400 uppercase">
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
      <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-4 pb-6 border-b border-paper-200 dark:border-slate-800">
        <div className="space-y-1.5 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200 dark:border-indigo-800 text-indigo-800 dark:text-indigo-300 text-xs font-mono font-bold uppercase tracking-wider">
            <GitBranch className="w-3.5 h-3.5" />
            <span>SYSTEMIC RISK INTELLIGENCE // FIRST-CLASS CITIZEN EXPERIENCE</span>
          </div>
          <h2
            id="cascading-risk-heading"
            className="text-2xl sm:text-4xl font-extrabold text-charcoal-950 dark:text-white tracking-tight"
          >
            Cascading Risk: What Could Happen Next?
          </h2>
          <p className="text-xs sm:text-sm text-charcoal-600 dark:text-slate-300 leading-relaxed">
            One hazard can trigger a chain of secondary hazards and systemic breakdowns. 
            Ground-failure relationships, infrastructure impacts, and health consequences are evaluated using verified physical laws—never fabricated percentages.
          </p>
        </div>

        {/* Global Evidence Posture Badge */}
        <div className="flex flex-col sm:flex-row lg:flex-col items-start lg:items-end gap-2 shrink-0">
          <div className={`px-3 py-1.5 rounded-xl border text-xs font-mono font-bold flex items-center gap-2 ${overallBadge.bg}`}>
            <span className={`w-2 h-2 rounded-full ${overallBadge.dot}`} />
            <span>{overallBadge.label}</span>
          </div>
          <span className="text-[10px] font-mono text-charcoal-400 dark:text-slate-500">
            Region: {regionName} • Target: {hazard}
          </span>
        </div>
      </div>

      {/* 2. Conceptual Clarification: CURRENT vs FUTURE vs CASCADING */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 p-4 rounded-2xl bg-paper-50 dark:bg-slate-850 border border-paper-200 dark:border-slate-800 text-xs leading-relaxed">
        <div className="space-y-1 p-2 rounded-xl">
          <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-charcoal-500 dark:text-slate-400 block">
            1. CURRENT RISK
          </span>
          <strong className="text-charcoal-900 dark:text-white block">What is happening right now</strong>
          <p className="text-charcoal-600 dark:text-slate-400 text-[11px]">
            Real-time telemetry from CWC river gauges, IMD rain radars, and USGS seismometers.
          </p>
        </div>

        <div className="space-y-1 p-2 rounded-xl border-t md:border-t-0 md:border-l border-paper-200 dark:border-slate-800">
          <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-indigo-600 dark:text-indigo-400 block">
            2. FUTURE RISK
          </span>
          <strong className="text-charcoal-900 dark:text-white block">What the hazard may do next</strong>
          <p className="text-charcoal-600 dark:text-slate-400 text-[11px]">
            Forward projections across 5 forecast horizons (NOW, 6h, 24h, 3d, 7d).
          </p>
        </div>

        <div className="space-y-1 p-2 rounded-xl border-t md:border-t-0 md:border-l border-paper-200 dark:border-slate-800 bg-indigo-100/50 dark:bg-indigo-950/30">
          <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-indigo-700 dark:text-indigo-300 block">
            3. CASCADING RISK
          </span>
          <strong className="text-indigo-950 dark:text-indigo-200 block">What could follow because of it</strong>
          <p className="text-indigo-900/80 dark:text-indigo-300/80 text-[11px]">
            Secondary hazards (e.g. landslides, contamination) and systemic impacts triggered downstream.
          </p>
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

      {/* 3. Visual 4-Stage Consequence Progression Chain */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-mono uppercase text-charcoal-500 dark:text-slate-400 font-bold block">
            FOUR-STAGE CAUSAL CHAIN // CLICK ANY STAGE TO INSPECT
          </span>
          <span className="text-[11px] font-mono text-indigo-600 dark:text-indigo-400">
            Progressive physical mechanism
          </span>
        </div>

        {/* Step Progression Bar with Directional Connectors */}
        <div className="hidden md:flex items-center justify-between px-4 py-2 rounded-xl bg-paper-50 dark:bg-slate-850 text-[10px] font-mono font-bold text-charcoal-600 dark:text-slate-400 border border-paper-200 dark:border-slate-800">
          <span className="text-indigo-700 dark:text-indigo-300">STEP 1: PRIMARY TRIGGER</span>
          <ArrowRight className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
          <span className="text-indigo-700 dark:text-indigo-300">STEP 2: PHYSICAL CHANGE</span>
          <ArrowRight className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
          <span className="text-indigo-700 dark:text-indigo-300">STEP 3: SECONDARY HAZARD</span>
          <ArrowRight className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
          <span className="text-indigo-700 dark:text-indigo-300">STEP 4: SYSTEMIC IMPACT</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
          {activeChain.stages.map((stage) => {
            const isExpanded = expandedStage === stage.stage_order;
            const stageBadge = getEvidenceBadge(stage.evidence_posture);
            const stageMeta = getStageTitle(stage.stage_order, stage.stage_type);

            return (
              <button
                key={stage.stage_order}
                onClick={() => toggleStage(stage.stage_order)}
                className={`text-left p-4 rounded-2xl border transition-all relative flex flex-col justify-between min-h-[140px] focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-600 ${
                  isExpanded
                    ? 'bg-paper-50 dark:bg-slate-850 border-charcoal-900 dark:border-white shadow-md'
                    : 'bg-white dark:bg-slate-900 border-paper-200 dark:border-slate-800 hover:border-paper-400 dark:hover:border-slate-700'
                }`}
                aria-expanded={isExpanded}
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-1.5">
                    <span className="text-[10px] font-mono uppercase font-bold text-indigo-600 dark:text-indigo-400">
                      {stageMeta.subtitle}
                    </span>
                    <span className={`w-2 h-2 rounded-full ${stageBadge.dot}`} />
                  </div>

                  <span className="text-[11px] font-medium text-charcoal-500 dark:text-slate-400 italic block mb-1">
                    &quot;{stageMeta.question}&quot;
                  </span>

                  <h3 className="text-sm font-bold text-charcoal-900 dark:text-white line-clamp-2">
                    {stage.title.split('//')[1] || stage.title}
                  </h3>

                  <p className="text-xs text-charcoal-600 dark:text-slate-400 mt-1 line-clamp-2">
                    {stage.description}
                  </p>
                </div>

                <div className="mt-3 flex items-center justify-between text-[11px] font-mono text-indigo-600 dark:text-indigo-400 font-bold pt-2 border-t border-paper-200 dark:border-slate-800">
                  <span>{isExpanded ? '[ HIDE PATHWAY DETAILS ▴ ]' : '[ EXAMINE THIS RISK PATHWAY ▾ ]'}</span>
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

      {/* 4. Detailed Expanded Inspector Panel with "WHAT CAN I DO?" */}
      {expandedStage !== null && (
        <div className="p-6 rounded-3xl bg-paper-50 dark:bg-slate-850 border border-paper-300 dark:border-slate-700 space-y-6 animate-in fade-in duration-200">
          {(() => {
            const currentStage = activeChain.stages.find((s) => s.stage_order === expandedStage);
            if (!currentStage) return null;
            const stageBadge = getEvidenceBadge(currentStage.evidence_posture);
            const stageMeta = getStageTitle(currentStage.stage_order, currentStage.stage_type);

            return (
              <div className="space-y-6">
                {/* Inspector Header */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-paper-200 dark:border-slate-700">
                  <div>
                    <span className="text-xs font-mono uppercase font-bold text-indigo-600 dark:text-indigo-400">
                      {stageMeta.subtitle} • {stageMeta.question}
                    </span>
                    <h3 className="text-xl font-bold text-charcoal-950 dark:text-white mt-0.5">
                      {currentStage.title}
                    </h3>
                  </div>

                  <div className={`px-3 py-1 rounded-xl border text-xs font-mono font-bold flex items-center gap-2 self-start sm:self-auto ${stageBadge.bg}`}>
                    <span className={`w-2 h-2 rounded-full ${stageBadge.dot}`} />
                    <span>{stageBadge.label}</span>
                  </div>
                </div>

                {/* Explanation */}
                <div className="space-y-2">
                  <h4 className="text-xs font-mono uppercase font-bold text-charcoal-500 dark:text-slate-400">
                    Physical & Causal Mechanism
                  </h4>
                  <p className="text-sm text-charcoal-800 dark:text-slate-200 leading-relaxed pl-4 border-l-2 border-indigo-600">
                    {currentStage.description}
                  </p>
                </div>

                {/* Grid: Supporting Evidence & Escalation Conditions */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                  {/* Supporting Evidence */}
                  <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-paper-200 dark:border-slate-800 space-y-2">
                    <div className="flex items-center gap-2 text-indigo-700 dark:text-indigo-400 font-bold uppercase font-mono text-[11px]">
                      <Eye className="w-3.5 h-3.5" />
                      <span>Supporting Evidence & Observations</span>
                    </div>
                    {currentStage.supporting_evidence.length > 0 ? (
                      <ul className="space-y-1.5 pl-4 list-disc text-charcoal-700 dark:text-slate-300">
                        {currentStage.supporting_evidence.map((ev, i) => (
                          <li key={i}>{ev}</li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-charcoal-500 dark:text-slate-400 italic">
                        Derived from established geotechnical and hydrometeorological baseline studies.
                      </p>
                    )}
                  </div>

                  {/* Conditions for Escalation */}
                  <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-paper-200 dark:border-slate-800 space-y-2">
                    <div className="flex items-center gap-2 text-amber-700 dark:text-amber-400 font-bold uppercase font-mono text-[11px]">
                      <AlertTriangle className="w-3.5 h-3.5" />
                      <span>Conditions That Accelerate Escalation</span>
                    </div>
                    {currentStage.conditions_for_escalation.length > 0 ? (
                      <ul className="space-y-1.5 pl-4 list-disc text-charcoal-700 dark:text-slate-300">
                        {currentStage.conditions_for_escalation.map((cond, i) => (
                          <li key={i}>{cond}</li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-charcoal-500 dark:text-slate-400 italic">
                        Escalation is governed by continuous rainfall thresholds and terrain saturation.
                      </p>
                    )}
                  </div>
                </div>

                {/* Grid: Warning Signs & Data Gaps */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                  {/* Field Warning Signs */}
                  {currentStage.field_warning_signs && currentStage.field_warning_signs.length > 0 && (
                    <div className="p-4 rounded-2xl bg-amber-50/60 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900 space-y-2">
                      <div className="flex items-center gap-2 text-amber-800 dark:text-amber-300 font-bold uppercase font-mono text-[11px]">
                        <Compass className="w-3.5 h-3.5" />
                        <span>Observable Field Signs on the Ground</span>
                      </div>
                      <ul className="space-y-1.5 pl-4 list-disc text-amber-950 dark:text-amber-200">
                        {currentStage.field_warning_signs.map((sign, i) => (
                          <li key={i}>{sign}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* What Remains Unknown / Unmonitored */}
                  {currentStage.unmonitored_or_unknown && currentStage.unmonitored_or_unknown.length > 0 && (
                    <div className="p-4 rounded-2xl bg-zinc-100/70 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700 space-y-2">
                      <div className="flex items-center gap-2 text-zinc-700 dark:text-zinc-300 font-bold uppercase font-mono text-[11px]">
                        <HelpCircle className="w-3.5 h-3.5" />
                        <span>Honest Data Gaps & Unmonitored Factors</span>
                      </div>
                      <ul className="space-y-1.5 pl-4 list-disc text-zinc-700 dark:text-zinc-300">
                        {currentStage.unmonitored_or_unknown.map((gap, i) => (
                          <li key={i}>{gap}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                {/* 5. Direct Citizen Action Linkage: "WHAT CAN I DO?" */}
                <div className="p-5 rounded-2xl bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800 space-y-3">
                  <div className="flex items-center justify-between gap-3">
                    <div className="flex items-center gap-2 text-emerald-800 dark:text-emerald-300 font-bold uppercase font-mono text-xs">
                      <ShieldCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                      <span>WHAT CAN I DO? // DEFENSIVE CITIZEN ACTIONS</span>
                    </div>

                    <button
                      onClick={() => {
                        if (onExploreSafetyGuide) {
                          onExploreSafetyGuide(hazard);
                        } else if (onNavigate) {
                          onNavigate('safety-guide');
                        }
                      }}
                      className="text-[11px] font-mono font-bold text-emerald-700 dark:text-emerald-300 hover:underline flex items-center gap-1 shrink-0"
                    >
                      <span>Explore Full Safety Guide</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  </div>

                  {currentStage.defensive_actions.length > 0 ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-emerald-950 dark:text-emerald-200">
                      {currentStage.defensive_actions.map((act, i) => (
                        <div key={i} className="flex items-start justify-between gap-2 p-2.5 rounded-lg bg-white/80 dark:bg-slate-900/70 border border-emerald-100 dark:border-emerald-900/60">
                          <div className="flex items-start gap-2">
                            <span className="font-mono font-bold text-emerald-700 dark:text-emerald-400 shrink-0">
                              ✓
                            </span>
                            <span className="leading-relaxed">{act}</span>
                          </div>
                          <button
                            onClick={() => {
                              if (onExploreSafetyGuide) {
                                onExploreSafetyGuide(hazard);
                              } else if (onNavigate) {
                                onNavigate('safety-guide');
                              }
                            }}
                            className="min-h-[28px] px-2 py-0.5 rounded-md bg-emerald-100 hover:bg-emerald-200 dark:bg-emerald-900/60 dark:hover:bg-emerald-850 text-emerald-900 dark:text-emerald-200 text-[10px] font-mono font-bold shrink-0 self-start transition-colors"
                          >
                            <span>GUIDE</span>
                          </button>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-emerald-900 dark:text-emerald-300 italic">
                      Follow standard household preparedness protocols in the Complete Safety Guide.
                    </p>
                  )}
                </div>
              </div>
            );
          })()}
        </div>
      )}
    </section>
  );
};
