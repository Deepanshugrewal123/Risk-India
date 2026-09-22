import React, { useState } from 'react';
import { PredictiveTimelinePoint, RiskState, UncertaintyLevel } from '../../types/predictiveRisk';
import { Clock, ShieldAlert, ArrowRight, CheckCircle2, AlertTriangle, Layers } from 'lucide-react';
import { UncertaintyBadge } from '../predictive/UncertaintyBadge';

interface FutureRiskTimelineProps {
  timeline?: PredictiveTimelinePoint[];
  regionName?: string;
  hazardName?: string;
  onSelectHorizon?: (horizonCode: string) => void;
}

const DEFAULT_TIMELINE: PredictiveTimelinePoint[] = [
  {
    horizon: 'NOW',
    time_window_label: 'Immediate Observation (NOW)',
    hazard: 'MULTI_HAZARD',
    current_risk_state: 'WATCH',
    future_risk_state: 'WATCH',
    risk_score: 35,
    trend: 'STABLE',
    confidence: 'HIGH',
    uncertainty: 'LOW',
    freshness: '3 mins ago',
    evidence_summary: ['Central hydrometeorological radar operational', 'In-situ telemetry reporting nominal'],
    recommended_action: 'Monitor local weather alerts and keep emergency communications charged.',
    data_classification: 'OFFICIAL_TELEMETRY'
  },
  {
    horizon: '0-6h',
    time_window_label: 'Nowcasting (0–6 Hours)',
    hazard: 'MULTI_HAZARD',
    current_risk_state: 'WATCH',
    future_risk_state: 'WATCH',
    risk_score: 40,
    trend: 'STABLE',
    confidence: 'HIGH',
    uncertainty: 'LOW',
    freshness: '12 mins ago',
    evidence_summary: ['Doppler radar convective precipitation tracking', 'Automatic weather station trend consensus'],
    recommended_action: 'Secure loose outdoor items; review household evacuation route.',
    data_classification: 'RADAR_NOWCAST'
  },
  {
    horizon: '6-24h',
    time_window_label: 'Short-Range (6–24 Hours)',
    hazard: 'MULTI_HAZARD',
    current_risk_state: 'WATCH',
    future_risk_state: 'ELEVATED',
    risk_score: 55,
    trend: 'RISING',
    confidence: 'MODERATE',
    uncertainty: 'MODERATE',
    freshness: '25 mins ago',
    evidence_summary: ['Numerical weather prediction high-resolution forecast', 'Catchment inflow upstream trajectory'],
    recommended_action: 'Prepare 72h disaster supply kit; store 3-day drinking water; avoid low-lying underpasses.',
    data_classification: 'NUMERICAL_FORECAST'
  },
  {
    horizon: '1-3d',
    time_window_label: 'Medium-Range (1–3 Days)',
    hazard: 'MULTI_HAZARD',
    current_risk_state: 'WATCH',
    future_risk_state: 'ELEVATED',
    risk_score: 58,
    trend: 'RISING',
    confidence: 'MODERATE',
    uncertainty: 'HIGH',
    freshness: '1 hour ago',
    evidence_summary: ['Multi-model ensemble synoptic depression propagation', 'Reservoir buffer stage assessment'],
    recommended_action: 'Vulnerable residents and elderly should prepare for potential relocation; heed block-level advisories.',
    data_classification: 'ENSEMBLE_PROJECTION'
  },
  {
    horizon: '3-7d',
    time_window_label: 'Extended Outlook (3–7 Days)',
    hazard: 'MULTI_HAZARD',
    current_risk_state: 'WATCH',
    future_risk_state: 'WATCH',
    risk_score: 45,
    trend: 'DECLINING',
    confidence: 'LOW',
    uncertainty: 'VERY_HIGH',
    freshness: '2 hours ago',
    evidence_summary: ['Extended range atmospheric teleconnection outlook', 'Seasonal climatological boundary conditions'],
    recommended_action: 'Track daily IMD bulletins; maintain general disaster preparedness posture.',
    data_classification: 'EXTENDED_OUTLOOK'
  }
];

export const FutureRiskTimeline: React.FC<FutureRiskTimelineProps> = ({
  timeline = DEFAULT_TIMELINE,
  regionName = 'National Outlook',
  hazardName = 'Multi-Hazard',
  onSelectHorizon
}) => {
  const [activeCode, setActiveCode] = useState<string>('6-24h');

  const points = timeline.length > 0 ? timeline : DEFAULT_TIMELINE;
  const activePoint = points.find((p) => p.horizon === activeCode) || points[2] || points[0];

  const getRiskBorder = (state: RiskState) => {
    switch (state) {
      case 'CRITICAL':
        return 'border-rose-500 bg-rose-500/10 text-rose-700 dark:text-rose-300';
      case 'HIGH':
        return 'border-orange-500 bg-orange-500/10 text-orange-700 dark:text-orange-300';
      case 'ELEVATED':
        return 'border-amber-500 bg-amber-500/10 text-amber-700 dark:text-amber-300';
      case 'WATCH':
        return 'border-blue-500 bg-blue-500/10 text-blue-700 dark:text-blue-300';
      case 'NORMAL':
      default:
        return 'border-emerald-500 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300';
    }
  };

  return (
    <div className="rounded-3xl border border-paper-300 bg-white dark:bg-slate-900 p-6 sm:p-8 shadow-md space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-paper-200 dark:border-slate-800">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono text-indigo-600 dark:text-indigo-400 uppercase font-bold">
            <Clock className="w-4 h-4" />
            <span>5-HORIZON PREDICTIVE TIMELINE</span>
          </div>
          <h3 className="text-xl sm:text-2xl font-bold text-charcoal-950 dark:text-white mt-0.5">
            Forward Risk Evolution // {regionName}
          </h3>
          <p className="text-xs text-charcoal-600 dark:text-slate-400 mt-0.5">
            Multi-horizon trajectory under {hazardName}. Qualitative classification; uncertainty expands with lead time.
          </p>
        </div>

        <div className="text-xs font-mono px-3 py-1.5 rounded-xl bg-paper-100 dark:bg-slate-800 border border-paper-300 dark:border-slate-700 text-charcoal-700 dark:text-slate-300 self-start sm:self-auto">
          Monotonic Uncertainty: LOW → VERY HIGH
        </div>
      </div>

      {/* Horizontal Horizon Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-5 gap-3">
        {points.map((pt, idx) => {
          const isSelected = activeCode === pt.horizon;
          return (
            <button
              key={pt.horizon}
              onClick={() => {
                setActiveCode(pt.horizon);
                onSelectHorizon?.(pt.horizon);
              }}
              className={`p-4 rounded-2xl text-left border transition-all relative ${
                isSelected
                  ? 'bg-charcoal-950 text-paper-50 dark:bg-white dark:text-charcoal-950 border-charcoal-950 dark:border-white shadow-lg ring-2 ring-indigo-500'
                  : 'bg-paper-50 dark:bg-slate-800/80 text-charcoal-800 dark:text-slate-200 border-paper-200 dark:border-slate-700 hover:border-indigo-300'
              }`}
            >
              <div className="flex items-center justify-between text-[11px] font-mono">
                <span className="font-bold">H0{idx + 1}</span>
                <span className="opacity-70 font-semibold">{pt.horizon}</span>
              </div>
              <div className="text-sm font-extrabold mt-1.5">
                {pt.future_risk_state}
              </div>
              <div className="text-[10px] opacity-75 mt-1 font-mono">
                Trend: {pt.trend}
              </div>
              <div className="mt-2 pt-2 border-t border-current/10 text-[10px] font-mono flex items-center justify-between">
                <span>Uncertainty:</span>
                <span className="font-bold">{pt.uncertainty}</span>
              </div>
            </button>
          );
        })}
      </div>

      {/* Selected Horizon Detail Inspection */}
      {activePoint && (
        <div className="p-5 rounded-2xl bg-paper-50/80 dark:bg-slate-800/60 border border-paper-300 dark:border-slate-700 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-paper-200 dark:border-slate-700">
            <div>
              <span className="text-[10px] font-mono uppercase tracking-wider text-charcoal-500 dark:text-slate-400 font-bold block">
                INSPECTED HORIZON
              </span>
              <h4 className="text-base font-bold text-charcoal-950 dark:text-white font-mono">
                {activePoint.time_window_label}
              </h4>
            </div>

            <div className="flex items-center gap-2">
              <span className={`px-2.5 py-1 rounded-full text-xs font-mono font-bold border ${getRiskBorder(activePoint.future_risk_state)}`}>
                State: {activePoint.future_risk_state}
              </span>
              <UncertaintyBadge
                confidence={activePoint.confidence}
                uncertainty={activePoint.uncertainty}
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Recommended Action */}
            <div className="p-4 rounded-xl bg-white dark:bg-slate-900 border border-paper-200 dark:border-slate-700 space-y-1.5">
              <div className="text-xs font-mono font-bold uppercase tracking-wider text-indigo-700 dark:text-indigo-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                <span>Action For This Horizon</span>
              </div>
              <p className="text-xs text-charcoal-800 dark:text-slate-200 leading-relaxed font-sans">
                {activePoint.recommended_action}
              </p>
            </div>

            {/* Evidence & Provenance */}
            <div className="p-4 rounded-xl bg-white dark:bg-slate-900 border border-paper-200 dark:border-slate-700 space-y-1.5">
              <div className="text-xs font-mono font-bold uppercase tracking-wider text-charcoal-600 dark:text-slate-400 flex items-center justify-between">
                <span className="flex items-center gap-1.5">
                  <Layers className="w-4 h-4 text-charcoal-500" />
                  <span>Observational Basis</span>
                </span>
                <span className="text-[10px] text-charcoal-400">Freshness: {activePoint.freshness}</span>
              </div>
              {activePoint.evidence_summary && activePoint.evidence_summary.length > 0 ? (
                <ul className="list-disc pl-4 text-xs text-charcoal-700 dark:text-slate-300 space-y-0.5 font-mono text-[11px]">
                  {activePoint.evidence_summary.map((ev, i) => (
                    <li key={i}>{ev}</li>
                  ))}
                </ul>
              ) : (
                <p className="text-xs text-charcoal-500 font-mono">Central observation network baseline</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
