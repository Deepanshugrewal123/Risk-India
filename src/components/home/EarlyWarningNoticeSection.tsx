import React, { useState, useEffect } from 'react';
import { EarlyWarningAssessment, EarlyWarningStatus } from '../../types/predictiveRisk';
import predictiveRiskService from '../../services/predictiveRiskService';
import {
  BellRing,
  AlertTriangle,
  ShieldCheck,
  LifeBuoy,
  FileCheck2,
  Clock,
  ExternalLink,
  Info,
  MapPin
} from 'lucide-react';

interface EarlyWarningNoticeSectionProps {
  onSelectRegion?: (regionId: string) => void;
  onViewAllWarnings?: () => void;
}

export const EarlyWarningNoticeSection: React.FC<EarlyWarningNoticeSectionProps> = ({
  onSelectRegion,
  onViewAllWarnings
}) => {
  const [readinessData, setReadinessData] = useState<{
    actionable_count: number;
    entities: any[];
    synthetic_records: number;
  } | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const loadReadiness = async () => {
      try {
        setLoading(true);
        const data = await predictiveRiskService.getReadiness();
        setReadinessData(data);
      } catch (err) {
        console.error('Failed to load readiness data', err);
      } finally {
        setLoading(false);
      }
    };
    loadReadiness();
  }, []);

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'EMERGENCY':
        return 'bg-rose-600 text-white border-rose-700 font-bold';
      case 'EVACUATION_READINESS':
        return 'bg-rose-500/15 text-rose-700 dark:text-rose-300 border-rose-500/30 font-bold';
      case 'GET_READY':
        return 'bg-amber-500/15 text-amber-700 dark:text-amber-300 border-amber-500/30 font-bold';
      case 'PREPARE':
        return 'bg-indigo-500/15 text-indigo-700 dark:text-indigo-300 border-indigo-500/30 font-bold';
      case 'WATCH':
        return 'bg-blue-500/15 text-blue-700 dark:text-blue-300 border-blue-500/30 font-bold';
      case 'NO_ACTIVE_SIGNAL':
      default:
        return 'bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border-emerald-500/30 font-bold';
    }
  };

  return (
    <section id="early-warnings" className="py-10 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div className="rounded-3xl border border-paper-300 bg-white dark:bg-slate-900 p-6 sm:p-8 shadow-lg space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-paper-200 dark:border-slate-800">
          <div className="space-y-1">
            <div className="inline-flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-amber-600 dark:text-amber-400">
              <BellRing className="w-4 h-4" />
              <span>EARLY WARNING & PUBLIC DECISION SUPPORT</span>
            </div>
            <h2 className="text-xl sm:text-3xl font-extrabold text-charcoal-950 dark:text-white">
              NATIONAL EARLY WARNING POSTURE
            </h2>
            <p className="text-xs sm:text-sm text-charcoal-600 dark:text-slate-400 max-w-2xl font-normal">
              Progressive decision guidance distinguishing preparation from evacuation directives.
              Statutory warnings are formally issued by IMD, CWC, and NDMA.
            </p>
          </div>

          <div className="flex items-center gap-2 font-mono text-xs">
            <span className="px-3 py-1.5 rounded-xl bg-paper-100 dark:bg-slate-800 text-charcoal-700 dark:text-slate-300 border border-paper-200 dark:border-slate-700">
              Actionable Entities: {readinessData?.actionable_count ?? 0}
            </span>
          </div>
        </div>

        {/* Actionable Entity Cards Grid */}
        {loading ? (
          <div className="p-8 text-center text-xs text-slate-500 font-mono">
            Evaluating statutory early warning feeds...
          </div>
        ) : readinessData && readinessData.entities.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {readinessData.entities.map((item) => {
              const isEvacAdvised = item.is_evacuation_advised;

              return (
                <div
                  key={item.region_id}
                  className={`p-4 rounded-2xl border transition-all ${
                    isEvacAdvised
                      ? 'border-rose-500/40 bg-rose-50/50 dark:bg-rose-950/20'
                      : 'border-paper-200 dark:border-slate-800 bg-paper-50/50 dark:bg-slate-850/50'
                  }`}
                >
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <div>
                      <span className="text-xs font-bold font-mono text-charcoal-500 dark:text-slate-400">
                        {item.hazard}
                      </span>
                      <h4 className="text-base font-bold text-charcoal-950 dark:text-white flex items-center gap-1.5">
                        <MapPin className="w-4 h-4 text-indigo-500 shrink-0" />
                        <span>{item.region_name}</span>
                      </h4>
                    </div>

                    <span
                      className={`px-2 py-0.5 rounded-lg text-[10px] font-mono border ${getStatusBadge(
                        item.early_warning_status
                      )}`}
                    >
                      {item.early_warning_status}
                    </span>
                  </div>

                  <div className="text-[11px] font-mono text-charcoal-500 mb-2">
                    Window: {item.lead_time_window}
                  </div>

                  {/* Evacuation Notice vs Preparation Guidance */}
                  {isEvacAdvised && item.evacuation_guidance ? (
                    <div className="p-2.5 rounded-xl border border-rose-500 bg-rose-100/70 dark:bg-rose-900/40 text-xs text-rose-900 dark:text-rose-100 font-medium mb-2 space-y-1">
                      <div className="flex items-center gap-1 font-bold text-rose-700 dark:text-rose-300 uppercase text-[10px]">
                        <AlertTriangle className="w-3.5 h-3.5" />
                        <span>Evacuation Directive Active</span>
                      </div>
                      <p className="text-[11px] leading-relaxed">{item.evacuation_guidance}</p>
                    </div>
                  ) : (
                    <div className="space-y-1.5 mb-2">
                      <span className="text-[11px] font-bold text-charcoal-800 dark:text-slate-200 block">
                        Preparation Actions:
                      </span>
                      <ul className="space-y-1 text-[11px] text-charcoal-600 dark:text-slate-300">
                        {item.preparation_guidance?.map((prep: string, idx: number) => (
                          <li key={idx} className="flex items-start gap-1">
                            <ShieldCheck className="w-3.5 h-3.5 text-indigo-500 shrink-0 mt-0.5" />
                            <span>{prep}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {onSelectRegion && (
                    <button
                      onClick={() => onSelectRegion(item.region_id)}
                      className="w-full mt-2 py-1.5 rounded-xl text-xs font-mono font-bold text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-950/40 hover:bg-indigo-100 dark:hover:bg-indigo-900/50 transition-colors text-center"
                    >
                      Inspect Location Details →
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        ) : (
          <div className="p-6 rounded-2xl bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-800/40 flex items-center gap-3 text-emerald-800 dark:text-emerald-200 text-xs sm:text-sm">
            <ShieldCheck className="w-5 h-5 text-emerald-600 shrink-0" />
            <div>
              <span className="font-bold block">No Urgent Evacuation Directives Active Nationwide</span>
              <p className="text-xs opacity-90 leading-relaxed mt-0.5">
                Baseline seasonal weather and hydrological monitoring continue. Maintain household
                72-hour emergency preparedness supplies.
              </p>
            </div>
          </div>
        )}

        {/* Strict Disclaimers & Provenance Note */}
        <div className="p-3.5 rounded-xl bg-paper-100 dark:bg-slate-800/60 border border-paper-200 dark:border-slate-800 text-[11px] text-charcoal-600 dark:text-slate-400 flex items-start gap-2">
          <Info className="w-4 h-4 text-indigo-500 shrink-0 mt-0.5" />
          <p className="leading-relaxed">
            <strong>Preparation vs Evacuation Authority Notice: </strong>
            Evacuation directives are legally issued by District Magistrates, State Disaster Management
            Authorities (SDMA), and NDMA under the Disaster Management Act, 2005. Internally derived
            forecast signals are for early preparation only and are never presented as statutory evacuation orders.
          </p>
        </div>
      </div>
    </section>
  );
};

export default EarlyWarningNoticeSection;
