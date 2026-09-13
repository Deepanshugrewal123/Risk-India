import React from 'react';
import { TrendingUp, Info, Sparkles, HelpCircle } from 'lucide-react';
import { DemoBadge } from './DemoBadge';

export interface ExplanationFactor {
  name: string;
  weight: number; // 0 to 100
  category?: 'Environmental' | 'Topographical' | 'Historical' | 'Hydrological';
  description: string;
}

interface RiskExplanationProps {
  locationName: string;
  disasterType: string;
  riskScore: number;
  factors: ExplanationFactor[];
  explanationNarrative?: string;
  className?: string;
}

export const RiskExplanation: React.FC<RiskExplanationProps> = ({
  locationName,
  disasterType,
  riskScore,
  factors,
  explanationNarrative,
  className = '',
}) => {
  // Sort factors by weight descending to highlight top drivers
  const sortedFactors = [...factors].sort((a, b) => b.weight - a.weight);

  const defaultExplanation =
    explanationNarrative ||
    `Model prototype attributes the ${riskScore}% estimated ${disasterType.toLowerCase()} risk in ${locationName} primarily to ${
      sortedFactors[0]?.name.toLowerCase() || 'elevated environmental thresholds'
    } compounded by ${
      sortedFactors[1]?.name.toLowerCase() || 'regional vulnerability factors'
    }. Historical recurrence and local contour drainage inertia further elevate baseline exposure.`;

  return (
    <div
      className={`p-6 sm:p-7 rounded-3xl bg-white border border-paper-300 shadow-subtle ${className}`}
    >
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 mb-5 border-b border-paper-200">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="font-mono text-xs uppercase tracking-wider text-charcoal-500 font-bold flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-amber-500" />
              <span>WHY THIS RISK?</span>
            </span>
            <span className="text-charcoal-300">•</span>
            <span className="text-[10px] font-mono text-charcoal-400">
              FACTOR CONTRIBUTION BREAKDOWN
            </span>
          </div>
          <p className="text-xs text-charcoal-600">
            Explainable AI breakdown of contributing environmental and terrain signals
          </p>
        </div>
        <DemoBadge label="FACTOR ATTRIBUTION" />
      </div>

      {/* Visual Factor Importance Bars (SHAP-Ready) */}
      <div className="space-y-4 mb-6">
        {sortedFactors.map((factor, index) => {
          // Bar styling based on relative contribution
          const isPrimary = index === 0;
          return (
            <div key={factor.name} className="space-y-1.5">
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <span
                    className={`w-1.5 h-1.5 rounded-full ${
                      factor.weight > 80
                        ? 'bg-risk-critical'
                        : factor.weight > 65
                        ? 'bg-risk-high'
                        : factor.weight > 45
                        ? 'bg-risk-moderate'
                        : 'bg-risk-low'
                    }`}
                  />
                  <span className="font-semibold text-charcoal-900">
                    {factor.name}
                  </span>
                  {isPrimary && (
                    <span className="text-[9px] font-mono uppercase px-1.5 py-0.5 rounded bg-amber-50 text-amber-800 border border-amber-200 font-bold">
                      Primary Driver
                    </span>
                  )}
                </div>
                <span className="font-mono font-bold text-charcoal-700">
                  {factor.weight}%
                </span>
              </div>

              {/* Graphical block segment progress bar */}
              <div className="w-full h-2.5 bg-paper-100 rounded-full overflow-hidden flex p-0.5 border border-paper-200">
                <div
                  className={`h-full rounded-full transition-all duration-700 ${
                    factor.weight > 80
                      ? 'bg-risk-critical'
                      : factor.weight > 65
                      ? 'bg-risk-high'
                      : factor.weight > 45
                      ? 'bg-risk-moderate'
                      : 'bg-risk-low'
                  }`}
                  style={{ width: `${factor.weight}%` }}
                />
              </div>

              <div className="flex items-center justify-between text-[11px] text-charcoal-500">
                <span>{factor.description}</span>
                {factor.category && (
                  <span className="font-mono text-[10px] text-charcoal-400">
                    {factor.category}
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Narrative Synthesis */}
      <div className="p-4 rounded-2xl bg-paper-50/80 border border-paper-200">
        <div className="flex items-center gap-1.5 text-[11px] font-mono text-charcoal-500 uppercase tracking-wider mb-1.5">
          <Info className="w-3.5 h-3.5 text-charcoal-400" />
          <span>Synthesis Summary</span>
        </div>
        <p className="text-xs sm:text-sm text-charcoal-800 leading-relaxed font-normal">
          {defaultExplanation}
        </p>
      </div>

      {/* Disclaimers & Future ML Notice */}
      <div className="mt-4 pt-3 border-t border-paper-200 flex items-center justify-between text-[10px] font-mono text-charcoal-400">
        <span>Architected for future SHAP / TreeExplainer weights</span>
        <span>Informational estimate only</span>
      </div>
    </div>
  );
};
