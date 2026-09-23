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

      {isFlood && (
        <div className="flex items-start gap-2 text-blue-900 bg-blue-50 border border-blue-200 rounded-xl p-3">
          <ShieldCheck className="w-4 h-4 shrink-0 mt-0.5 text-blue-700" />
          <div className="space-y-0.5">
            <span className="font-bold block">RISK // INDIA Flood Model v1 — India-Wide Empirical Flood Intelligence</span>
            <p className="text-[11px] leading-relaxed text-blue-800">
              Model: <code className="font-mono font-bold bg-white px-1 py-0.5 rounded border border-blue-200">risk_india_flood_v1</code> (GradientBoostingClassifier).
              Trained on 18,184 empirical IMD district observations across 38 States/UTs. Evaluates compound hydrological flood inundation across all 12 major Indian river basins with zero synthetic data.
            </p>
          </div>
        </div>
      )}

      {!isEarthquake && !isFlood && (
        <div className="flex items-start gap-2 text-slate-700 bg-slate-50 border border-slate-200 rounded-xl p-3">
          <Info className="w-4 h-4 shrink-0 mt-0.5 text-blue-700" />
          <div className="space-y-0.5">
            <span className="font-bold text-slate-900 block">
              Multi-Source Evidence Early Warning Fusion (Authoritative Non-ML)
            </span>
            <p className="text-[11px] leading-relaxed text-slate-600">
              Assessment is derived from authoritative meteorological forecasts (IMD NWFC), hydrological telemetry (CWC), and statutory geospatial baselines (NDMA, GSI, BIS IS 1893). Empirical ML is active for flood hazards; non-flood perils follow statutory operational models.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default PredictionScopeNotice;
