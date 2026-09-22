import React from 'react';
import { UncertaintyLevel, ConfidenceLevel } from '../../types/predictiveRisk';
import { HelpCircle, ShieldCheck, AlertCircle } from 'lucide-react';

interface UncertaintyBadgeProps {
  uncertainty?: UncertaintyLevel;
  confidence?: ConfidenceLevel;
  showLabels?: boolean;
}

export const UncertaintyBadge: React.FC<UncertaintyBadgeProps> = ({
  uncertainty,
  confidence,
  showLabels = true
}) => {
  const getUncertaintyColor = (lvl?: UncertaintyLevel) => {
    switch (lvl) {
      case 'LOW':
        return 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20';
      case 'MODERATE':
        return 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20';
      case 'HIGH':
        return 'bg-orange-500/10 text-orange-600 dark:text-orange-400 border-orange-500/20';
      case 'VERY_HIGH':
        return 'bg-red-500/10 text-red-600 dark:text-red-400 border-red-500/20';
      default:
        return 'bg-slate-500/10 text-slate-600 dark:text-slate-400 border-slate-500/20';
    }
  };

  const getConfidenceColor = (lvl?: ConfidenceLevel) => {
    switch (lvl) {
      case 'HIGH':
        return 'bg-sky-500/10 text-sky-600 dark:text-sky-400 border-sky-500/20';
      case 'MODERATE':
        return 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20';
      case 'LOW':
        return 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/20';
      default:
        return 'bg-slate-500/10 text-slate-600 dark:text-slate-400 border-slate-500/20';
    }
  };

  return (
    <div className="inline-flex items-center gap-1.5 flex-wrap">
      {confidence && (
        <span
          className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium border ${getConfidenceColor(
            confidence
          )}`}
          title={`Confidence: ${confidence} (Empirical corroboration & source convergence)`}
        >
          <ShieldCheck className="w-3 h-3" />
          {showLabels ? `Confidence: ${confidence}` : confidence}
        </span>
      )}

      {uncertainty && (
        <span
          className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium border ${getUncertaintyColor(
            uncertainty
          )}`}
          title={`Uncertainty: ${uncertainty} (Expands with lead time and sensor latency)`}
        >
          {uncertainty === 'LOW' || uncertainty === 'MODERATE' ? (
            <HelpCircle className="w-3 h-3" />
          ) : (
            <AlertCircle className="w-3 h-3" />
          )}
          {showLabels ? `Uncertainty: ${uncertainty}` : uncertainty}
        </span>
      )}
    </div>
  );
};

export default UncertaintyBadge;
