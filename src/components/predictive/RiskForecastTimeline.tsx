import React, { useState } from 'react';
import { PredictiveTimelinePoint, RiskState } from '../../types/predictiveRisk';
import { UncertaintyBadge } from './UncertaintyBadge';
import { RiskTrendIndicator } from './RiskTrendIndicator';
import { Clock, ShieldAlert, CheckCircle2, ChevronRight } from 'lucide-react';

interface RiskForecastTimelineProps {
  timeline: PredictiveTimelinePoint[];
  hazard: string;
}

export const RiskForecastTimeline: React.FC<RiskForecastTimelineProps> = ({
  timeline,
  hazard
}) => {
  const [selectedHorizon, setSelectedHorizon] = useState<string>(
    timeline[0]?.horizon || 'NOW'
  );

  if (!timeline || timeline.length === 0) {
    return (
      <div className="p-4 text-center text-slate-500 text-sm">
        No predictive timeline data available for {hazard}.
      </div>
    );
  }

  const selectedPoint =
    timeline.find((tp) => tp.horizon === selectedHorizon) || timeline[0];

  const getRiskStateStyle = (state: RiskState) => {
    switch (state) {
      case 'CRITICAL':
        return {
          bg: 'bg-rose-500/10 border-rose-500/30 text-rose-600 dark:text-rose-400',
          bar: 'bg-rose-500',
          pill: 'bg-rose-600 text-white'
        };
      case 'HIGH':
        return {
          bg: 'bg-orange-500/10 border-orange-500/30 text-orange-600 dark:text-orange-400',
          bar: 'bg-orange-500',
          pill: 'bg-orange-600 text-white'
        };
      case 'ELEVATED':
        return {
          bg: 'bg-amber-500/10 border-amber-500/30 text-amber-600 dark:text-amber-400',
          bar: 'bg-amber-500',
          pill: 'bg-amber-600 text-white'
        };
      case 'WATCH':
        return {
          bg: 'bg-blue-500/10 border-blue-500/30 text-blue-600 dark:text-blue-400',
          bar: 'bg-blue-500',
          pill: 'bg-blue-600 text-white'
        };
      case 'NORMAL':
      default:
        return {
          bg: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-600 dark:text-emerald-400',
          bar: 'bg-emerald-500',
          pill: 'bg-emerald-600 text-white'
        };
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-900 flex items-center gap-2">
          <Clock className="w-4 h-4 text-blue-700" />
          5-Horizon Predictive Timeline ({hazard})
        </h3>
        <span className="text-xs text-slate-500 font-mono">
          NWP Ensemble + Ground Telemetry
        </span>
      </div>

      {/* Horizon Selector Tabs */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
        {timeline.map((tp) => {
          const isSelected = tp.horizon === selectedHorizon;
          const style = getRiskStateStyle(tp.future_risk_state);

          return (
            <button
              key={tp.horizon}
              onClick={() => setSelectedHorizon(tp.horizon)}
              className={`flex flex-col items-center justify-between p-3 rounded-2xl border transition-all text-left ${
                isSelected
                  ? 'border-blue-600 ring-2 ring-blue-500/20 shadow-sm bg-white'
                  : 'border-slate-200 hover:border-slate-300 bg-slate-50/50 hover:bg-white'
              }`}
            >
              <div className="w-full flex items-center justify-between mb-1.5">
                <span className="text-xs font-bold font-mono text-slate-800">
                  {tp.horizon}
                </span>
                <span
                  className={`px-1.5 py-0.5 rounded text-[10px] font-bold font-mono ${style.pill}`}
                >
                  {tp.future_risk_state}
                </span>
              </div>

              <div className="w-full space-y-1">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-500 text-[11px] font-medium">Score</span>
                  <span className="font-mono font-bold text-slate-900">
                    {tp.risk_score}
                  </span>
                </div>
                <div className="w-full h-1.5 rounded-full bg-slate-200 overflow-hidden">
                  <div
                    className={`h-full ${style.bar}`}
                    style={{ width: `${Math.min(100, Math.max(5, tp.risk_score))}%` }}
                  />
                </div>
              </div>
            </button>
          );
        })}
      </div>

      {/* Selected Horizon Card */}
      {selectedPoint && (
        <div className="p-4 sm:p-5 rounded-2xl border border-slate-200 bg-white shadow-xs space-y-3">
          <div className="flex items-center justify-between flex-wrap gap-2 pb-2 border-b border-slate-100">
            <div>
              <span className="text-xs font-mono text-blue-700 font-bold uppercase">
                Horizon: {selectedPoint.time_window_label}
              </span>
              <h4 className="text-base font-bold text-slate-900 flex items-center gap-2 mt-0.5">
                <span>
                  {hazard} Projected Risk: {selectedPoint.future_risk_state}
                </span>
                <span className="text-xs font-mono font-normal text-slate-500">
                  (Score: {selectedPoint.risk_score}/100)
                </span>
              </h4>
            </div>

            <div className="flex items-center gap-2 flex-wrap">
              <RiskTrendIndicator trend={selectedPoint.trend} size="sm" />
              <UncertaintyBadge
                uncertainty={selectedPoint.uncertainty}
                confidence={selectedPoint.confidence}
                showLabels={false}
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            <div className="space-y-1.5">
              <span className="font-semibold text-slate-700 block">
                Evidence Convergence:
              </span>
              <ul className="space-y-1">
                {selectedPoint.evidence_summary.map((ev, i) => (
                  <li key={i} className="flex items-start gap-1.5 text-slate-600">
                    <ChevronRight className="w-3.5 h-3.5 text-blue-600 shrink-0 mt-0.5" />
                    <span>{ev}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="space-y-1.5">
              <span className="font-semibold text-slate-700 block">
                Recommended Action:
              </span>
              <div className="flex items-start gap-2 p-2.5 rounded-xl bg-slate-50 border border-slate-200">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span className="text-slate-800 leading-relaxed font-medium">
                  {selectedPoint.recommended_action}
                </span>
              </div>
            </div>
          </div>

          {selectedPoint.official_warning && (
            <div className="flex items-start gap-2 p-2.5 rounded-xl bg-amber-50 border border-amber-200 text-xs text-amber-900">
              <ShieldAlert className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
              <span>
                <strong>Official Warning Active:</strong> {selectedPoint.official_warning}
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RiskForecastTimeline;
