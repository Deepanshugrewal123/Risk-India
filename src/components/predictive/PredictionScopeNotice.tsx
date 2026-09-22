import React from 'react';
import { ShieldCheck, AlertCircle, Info, Database } from 'lucide-react';

interface PredictionScopeNoticeProps {
  isAssam: boolean;
  hazard: string;
  mlScope?: Record<string, any>;
  syntheticRecords?: number;
}

export const PredictionScopeNotice: React.FC<PredictionScopeNoticeProps> = ({
  isAssam,
  hazard,
  mlScope,
  syntheticRecords = 0
}) => {
  const normHazard = hazard.toUpperCase().trim();
  const isEarthquake = normHazard === 'EARTHQUAKE';
  const isFlood = normHazard === 'FLOOD';

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4 space-y-2.5 text-xs shadow-xs">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <div className="flex items-center gap-1.5 font-bold text-slate-800">
          <Database className="w-4 h-4 text-blue-700" />
          <span>Scientific Governance & Model Scope</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-mono bg-emerald-50 text-emerald-800 border border-emerald-200 font-bold">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
            Zero Synthetic Data ({syntheticRecords})
          </span>
        </div>
      </div>

      {isEarthquake && (
        <div className="flex items-start gap-2 text-amber-900 bg-amber-50 border border-amber-200 rounded-xl p-3">
          <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-amber-600" />
          <div className="space-y-0.5">
            <span className="font-bold block">Earthquake Non-Prediction Guard Active</span>
            <p className="text-[11px] leading-relaxed text-amber-800">
              Earthquakes cannot be predicted deterministically. Projections represent ambient
              lithospheric baselines (BIS IS 1893:2016) and observed USGS/NCS seismic catalog
              records. Future temporal forecasts are strictly disabled for seismic hazards.
            </p>
          </div>
        </div>
      )}

      {isFlood && isAssam && (
        <div className="flex items-start gap-2 text-blue-900 bg-blue-50 border border-blue-200 rounded-xl p-3">
          <ShieldCheck className="w-4 h-4 shrink-0 mt-0.5 text-blue-700" />
          <div className="space-y-0.5">
            <span className="font-bold block">Assam Empirical ML Model Active</span>
            <p className="text-[11px] leading-relaxed text-blue-800">
              Model: <code className="font-mono font-bold bg-white px-1 py-0.5 rounded border border-blue-200">assam_flood_prototype_v1</code> (RandomForest
              Classifier). Trained exclusively on empirical historical Brahmaputra gauge and
              precipitation records.
            </p>
          </div>
        </div>
      )}

      {!isEarthquake && !(isFlood && isAssam) && (
        <div className="flex items-start gap-2 text-slate-700 bg-slate-50 border border-slate-200 rounded-xl p-3">
          <Info className="w-4 h-4 shrink-0 mt-0.5 text-blue-700" />
          <div className="space-y-0.5">
            <span className="font-bold text-slate-900 block">
              Deterministic Multi-Signal Early Warning Fusion
            </span>
            <p className="text-[11px] leading-relaxed text-slate-600">
              Assessment is derived from real-time IMD numerical weather predictions, CWC river
              telemetry, and statutory vulnerability baselines. Assam ML is strictly scoped to Assam
              jurisdiction (ml_available = false).
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default PredictionScopeNotice;
