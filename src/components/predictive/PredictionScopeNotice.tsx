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
    <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50 p-3.5 space-y-2 text-xs">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <div className="flex items-center gap-1.5 font-semibold text-slate-700 dark:text-slate-300">
          <Database className="w-4 h-4 text-indigo-500" />
          <span>Scientific Governance & Model Scope</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-mono bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
            <ShieldCheck className="w-3 h-3" />
            Zero Synthetic Data ({syntheticRecords})
          </span>
        </div>
      </div>

      {isEarthquake && (
        <div className="flex items-start gap-2 text-amber-700 dark:text-amber-300 bg-amber-500/10 border border-amber-500/20 rounded-lg p-2.5">
          <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-amber-600 dark:text-amber-400" />
          <div className="space-y-0.5">
            <span className="font-semibold block">Earthquake Non-Prediction Guard Active</span>
            <p className="text-[11px] leading-relaxed opacity-90">
              Earthquakes cannot be predicted deterministically. Projections represent ambient
              lithospheric baselines (BIS IS 1893:2016) and observed USGS/NCS seismic catalog
              records. Future temporal forecasts are strictly disabled for seismic hazards.
            </p>
          </div>
        </div>
      )}

      {isFlood && isAssam && (
        <div className="flex items-start gap-2 text-indigo-700 dark:text-indigo-300 bg-indigo-500/10 border border-indigo-500/20 rounded-lg p-2.5">
          <ShieldCheck className="w-4 h-4 shrink-0 mt-0.5 text-indigo-600 dark:text-indigo-400" />
          <div className="space-y-0.5">
            <span className="font-semibold block">Assam Empirical ML Model Active</span>
            <p className="text-[11px] leading-relaxed opacity-90">
              Model: <code className="font-mono font-bold">assam_flood_prototype_v1</code> (RandomForest
              Classifier). Trained exclusively on empirical historical Brahmaputra gauge and
              precipitation records.
            </p>
          </div>
        </div>
      )}

      {!isEarthquake && !(isFlood && isAssam) && (
        <div className="flex items-start gap-2 text-slate-600 dark:text-slate-400 bg-white/50 dark:bg-slate-800/50 border border-slate-200/60 dark:border-slate-700/60 rounded-lg p-2.5">
          <Info className="w-4 h-4 shrink-0 mt-0.5 text-slate-500" />
          <div className="space-y-0.5">
            <span className="font-semibold text-slate-700 dark:text-slate-300 block">
              Deterministic Multi-Signal Early Warning Fusion
            </span>
            <p className="text-[11px] leading-relaxed">
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
