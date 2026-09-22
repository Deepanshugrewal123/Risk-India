import React from 'react';
import { WeatherEvidenceSignal } from '../../types/weather';
import { ShieldCheck, ShieldAlert, Cpu, Activity, Compass, Layers } from 'lucide-react';

interface WeatherEvidencePanelProps {
  signals: WeatherEvidenceSignal[];
  regionName: string;
  earthquakeBoundaryNotice?: string;
}

export const WeatherEvidencePanel: React.FC<WeatherEvidencePanelProps> = ({
  signals,
  regionName,
  earthquakeBoundaryNotice
}) => {
  return (
    <div className="p-6 bg-white border border-gray-200 rounded-2xl shadow-sm space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-100 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <Layers className="w-5 h-5 text-blue-600" />
            <h3 className="text-base font-bold text-gray-900 tracking-tight">
              Multi-Hazard Early-Warning Evidence Feeds — {regionName}
            </h3>
          </div>
          <p className="text-xs text-gray-500 mt-1">
            Empirical weather evidence feeding downstream multi-hazard early warning assessments.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 font-mono">
            <Cpu className="w-3.5 h-3.5" />
            ASSAM ML MODEL PROTECTED
          </span>
        </div>
      </div>

      {/* Strict Earthquake Non-Prediction Scientific Guard */}
      <div className="p-3.5 bg-purple-50/70 border border-purple-200 rounded-xl text-xs space-y-1">
        <div className="flex items-center gap-2 font-bold text-purple-900">
          <ShieldCheck className="w-4 h-4 text-purple-700 shrink-0" />
          <span>Scientific Invariant: Earthquake Non-Prediction Boundary</span>
        </div>
        <p className="text-purple-800 leading-relaxed">
          {earthquakeBoundaryNotice ||
            'Earthquakes are tectonically driven and cannot be deterministically predicted from atmospheric weather signals. Weather feeds are strictly decoupled from seismic intelligence.'}
        </p>
      </div>

      {/* Signals Grid */}
      {signals && signals.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {signals.map((sig, idx) => (
            <div
              key={idx}
              className="p-3.5 bg-gray-50/80 rounded-xl border border-gray-200 space-y-2 hover:border-gray-300 transition-colors"
            >
              <div className="flex items-center justify-between">
                <span className="px-2 py-0.5 text-[11px] font-bold font-mono uppercase bg-blue-100/70 text-blue-800 rounded">
                  {sig.hazard}
                </span>
                <span className="text-[11px] font-mono text-gray-500">
                  Lead: {sig.lead_time}
                </span>
              </div>

              <div className="space-y-1">
                <div className="text-xs font-semibold text-gray-900">
                  {sig.signal_type.replace(/_/g, ' ')}
                </div>
                <div className="text-xs text-gray-600">
                  Metric: <strong className="font-medium text-gray-800">{sig.metric}</strong> = {String(sig.value)}
                </div>
                <p className="text-xs text-gray-700 leading-relaxed">
                  {sig.implication}
                </p>
              </div>

              <div className="pt-2 border-t border-gray-200/60 flex items-center justify-between text-[10px] text-gray-500 font-mono">
                <span>Confidence: <strong>{sig.confidence}</strong></span>
                <span>Uncertainty: <strong>{sig.uncertainty}</strong></span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="p-4 bg-gray-50 rounded-xl border border-gray-100 text-center text-xs text-gray-500">
          No anomalous weather-derived evidence signals active for {regionName}. Synoptic conditions are within climatological baseline ranges.
        </div>
      )}

      {/* Footer Notes */}
      <div className="text-[11px] text-gray-500 border-t border-gray-100 pt-3 flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-1.5">
          <Activity className="w-3.5 h-3.5 text-emerald-600" />
          <span>Freshness decoupled from severity: Stale observations degrade confidence without distorting hazard indices.</span>
        </div>
        <div className="font-mono text-gray-400">
          Zero Synthetic Records Guarantee
        </div>
      </div>
    </div>
  );
};
