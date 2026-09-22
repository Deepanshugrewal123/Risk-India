import React, { useState } from 'react';
import { EvidenceSignal } from '../../types/predictiveRisk';
import {
  Layers,
  AlertTriangle,
  ExternalLink,
  CheckCircle,
  HelpCircle,
  Clock,
  Radio
} from 'lucide-react';

interface EvidenceConvergencePanelProps {
  signals: EvidenceSignal[];
  hasConflictingEvidence: boolean;
  conflictingSignals: string[];
  conflictResolutionNotes?: string | null;
  overallFreshness: string;
}

export const EvidenceConvergencePanel: React.FC<EvidenceConvergencePanelProps> = ({
  signals,
  hasConflictingEvidence,
  conflictingSignals,
  conflictResolutionNotes,
  overallFreshness
}) => {
  const [filter, setFilter] = useState<'ALL' | 'OBSERVED' | 'FORECAST' | 'WARNING'>('ALL');

  const filteredSignals = signals.filter((s) => {
    if (filter === 'OBSERVED') return s.data_classification === 'OBSERVED';
    if (filter === 'FORECAST') return s.data_classification === 'FORECAST';
    if (filter === 'WARNING') return s.data_classification === 'OFFICIAL_WARNING';
    return true;
  });

  const getProviderBadge = (provider: string) => {
    switch (provider) {
      case 'IMD':
      case 'IMD_NWFC':
        return 'bg-blue-500/10 text-blue-600 dark:text-blue-400 border-blue-500/20';
      case 'CWC':
        return 'bg-teal-500/10 text-teal-600 dark:text-teal-400 border-teal-500/20';
      case 'NDMA':
        return 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/20';
      case 'USGS':
      case 'USGS / NCS':
        return 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20';
      case 'GSI':
        return 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20';
      default:
        return 'bg-purple-500/10 text-purple-600 dark:text-purple-400 border-purple-500/20';
    }
  };

  return (
    <div className="space-y-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 shadow-sm">
      <div className="flex items-center justify-between flex-wrap gap-2 pb-2 border-b border-slate-100 dark:border-slate-800">
        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-indigo-500" />
          <h4 className="text-sm font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100">
            Authoritative Evidence Convergence ({signals.length})
          </h4>
        </div>
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1 text-xs font-mono text-slate-500">
            <Radio className="w-3 h-3 text-emerald-500 animate-pulse" />
            Freshness: {overallFreshness}
          </span>
        </div>
      </div>

      {/* Conflicting Evidence Alert & Resolution */}
      {hasConflictingEvidence && (
        <div className="p-3.5 rounded-xl border border-amber-500/30 bg-amber-500/10 space-y-2 text-xs text-amber-800 dark:text-amber-200">
          <div className="flex items-center gap-2 font-bold text-amber-700 dark:text-amber-300">
            <AlertTriangle className="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0" />
            <span>Multi-Source Signal Disagreement Detected</span>
          </div>
          <ul className="space-y-1 list-disc list-inside text-[11px] opacity-90 pl-1">
            {conflictingSignals.map((cs, i) => (
              <li key={i}>{cs}</li>
            ))}
          </ul>
          {conflictResolutionNotes && (
            <div className="mt-2 pt-2 border-t border-amber-500/20 text-[11px]">
              <strong className="text-amber-900 dark:text-amber-100">Scientific Resolution: </strong>
              <span>{conflictResolutionNotes}</span>
            </div>
          )}
        </div>
      )}

      {/* Filter Tabs */}
      <div className="flex items-center gap-1.5 overflow-x-auto text-xs pb-1">
        {(['ALL', 'OBSERVED', 'FORECAST', 'WARNING'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setFilter(tab)}
            className={`px-2.5 py-1 rounded-lg font-medium transition-colors ${
              filter === tab
                ? 'bg-indigo-600 text-white shadow-2xs'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Signals List */}
      <div className="space-y-2 max-h-64 overflow-y-auto pr-1">
        {filteredSignals.map((sig) => (
          <div
            key={sig.id}
            className="flex items-center justify-between p-2.5 rounded-lg border border-slate-100 dark:border-slate-800/80 bg-slate-50/60 dark:bg-slate-800/40 text-xs gap-3"
          >
            <div className="space-y-0.5 min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <span
                  className={`px-1.5 py-0.5 rounded text-[10px] font-mono font-bold border ${getProviderBadge(
                    sig.provider
                  )}`}
                >
                  {sig.provider}
                </span>
                <span className="font-semibold text-slate-800 dark:text-slate-200 truncate">
                  {sig.variable}
                </span>
                <span className="text-[10px] font-mono text-slate-500">
                  [{sig.data_classification}]
                </span>
              </div>
              <p className="text-[11px] text-slate-500 truncate">{sig.geographic_scope}</p>
            </div>

            <div className="flex items-center gap-3 shrink-0">
              {sig.raw_value !== null && sig.raw_value !== undefined && (
                <span className="font-mono font-bold text-slate-800 dark:text-slate-200">
                  {sig.raw_value} {sig.unit}
                </span>
              )}
              {sig.url && (
                <a
                  href={sig.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 p-1"
                  title="View upstream source record"
                >
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EvidenceConvergencePanel;
