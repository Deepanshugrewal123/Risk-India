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
        return 'bg-blue-50 text-blue-700 border-blue-200';
      case 'CWC':
        return 'bg-teal-50 text-teal-700 border-teal-200';
      case 'NDMA':
        return 'bg-rose-50 text-rose-700 border-rose-200';
      case 'USGS':
      case 'USGS / NCS':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'GSI':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      default:
        return 'bg-purple-50 text-purple-700 border-purple-200';
    }
  };

  return (
    <div className="space-y-4 rounded-2xl border border-slate-200 bg-white p-4 sm:p-5 shadow-xs">
      <div className="flex items-center justify-between flex-wrap gap-2 pb-2 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-blue-700" />
          <h4 className="text-sm font-bold uppercase tracking-wider text-slate-900">
            Authoritative Evidence Convergence ({signals.length})
          </h4>
        </div>
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1 text-xs font-mono text-slate-500">
            <Radio className="w-3 h-3 text-emerald-600 animate-pulse" />
            Freshness: {overallFreshness}
          </span>
        </div>
      </div>

      {/* Conflicting Evidence Alert & Resolution */}
      {hasConflictingEvidence && (
        <div className="p-3.5 rounded-xl border border-amber-200 bg-amber-50 space-y-2 text-xs text-amber-900">
          <div className="flex items-center gap-2 font-bold text-amber-800">
            <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
            <span>Multi-Source Signal Disagreement Detected</span>
          </div>
          <ul className="space-y-1 list-disc list-inside text-[11px] opacity-90 pl-1">
            {conflictingSignals.map((cs, i) => (
              <li key={i}>{cs}</li>
            ))}
          </ul>
          {conflictResolutionNotes && (
            <div className="mt-2 pt-2 border-t border-amber-200 text-[11px]">
              <strong className="text-amber-950 font-bold">Scientific Resolution: </strong>
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
            className={`px-3 py-1 rounded-lg font-bold transition-colors ${
              filter === tab
                ? 'bg-blue-700 text-white shadow-2xs'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
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
            className="flex items-center justify-between p-2.5 rounded-xl border border-slate-200 bg-slate-50 text-xs gap-3"
          >
            <div className="space-y-0.5 min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${getProviderBadge(
                    sig.provider
                  )}`}
                >
                  {sig.provider}
                </span>
                <span className="font-bold text-slate-900 truncate">
                  {sig.variable}
                </span>
                <span className="text-[10px] font-mono text-slate-500">
                  [{sig.data_classification}]
                </span>
              </div>
              <p className="text-[11px] text-slate-500 truncate font-normal">{sig.geographic_scope}</p>
            </div>

            <div className="flex items-center gap-3 shrink-0">
              {sig.raw_value !== null && sig.raw_value !== undefined && (
                <span className="font-mono font-bold text-slate-900">
                  {sig.raw_value} {sig.unit}
                </span>
              )}
              {sig.url && (
                <a
                  href={sig.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-700 hover:text-blue-900 p-1 font-bold"
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
