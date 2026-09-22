import React from 'react';
import {
  RiskState,
  TrendState,
  ConfidenceLevel,
  UncertaintyLevel
} from '../../types/predictiveRisk';
import { RiskTrendIndicator } from './RiskTrendIndicator';
import { UncertaintyBadge } from './UncertaintyBadge';
import {
  Droplets,
  Wind,
  Sun,
  CloudLightning,
  Mountain,
  Activity
} from 'lucide-react';

interface HazardForecastCardProps {
  currentHazard: string;
  onSelectHazard: (hazard: string) => void;
  currentRiskState: RiskState;
  currentScore: number;
  futureRiskState: RiskState;
  peakScore: number;
  peakWindow: string;
  trend: TrendState;
  confidence: ConfidenceLevel;
  uncertainty: UncertaintyLevel;
}

export const HazardForecastCard: React.FC<HazardForecastCardProps> = ({
  currentHazard,
  onSelectHazard,
  currentRiskState,
  currentScore,
  futureRiskState,
  peakScore,
  peakWindow,
  trend,
  confidence,
  uncertainty
}) => {
  const hazards = [
    { id: 'FLOOD', name: 'Flood', icon: Droplets, color: 'text-blue-500' },
    { id: 'CYCLONE', name: 'Cyclone', icon: Wind, color: 'text-teal-500' },
    { id: 'HEATWAVE', name: 'Heatwave', icon: Sun, color: 'text-amber-500' },
    { id: 'SEVERE_WEATHER', name: 'Severe Weather', icon: CloudLightning, color: 'text-purple-500' },
    { id: 'LANDSLIDE', name: 'Landslide', icon: Mountain, color: 'text-emerald-500' },
    { id: 'EARTHQUAKE', name: 'Earthquake', icon: Activity, color: 'text-rose-500' }
  ];

  const getRiskColor = (state: RiskState) => {
    switch (state) {
      case 'CRITICAL':
        return 'text-rose-600 dark:text-rose-400';
      case 'HIGH':
        return 'text-orange-600 dark:text-orange-400';
      case 'ELEVATED':
        return 'text-amber-600 dark:text-amber-400';
      case 'WATCH':
        return 'text-blue-600 dark:text-blue-400';
      case 'NORMAL':
      default:
        return 'text-emerald-600 dark:text-emerald-400';
    }
  };

  return (
    <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 shadow-sm space-y-4">
      <div className="flex items-center justify-between flex-wrap gap-2 pb-2 border-b border-slate-100 dark:border-slate-800">
        <h4 className="text-sm font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100">
          Multi-Hazard Forecasting (6 Hazards)
        </h4>
        <span className="text-xs text-slate-500 font-mono">
          Integrated Early Warning Matrix
        </span>
      </div>

      {/* Hazard Selector Pills */}
      <div className="grid grid-cols-3 sm:grid-cols-6 gap-2">
        {hazards.map((h) => {
          const isSelected = h.id === currentHazard.toUpperCase();
          const IconComp = h.icon;

          return (
            <button
              key={h.id}
              onClick={() => onSelectHazard(h.id)}
              className={`flex flex-col items-center gap-1.5 p-2.5 rounded-xl border transition-all ${
                isSelected
                  ? 'border-indigo-500 ring-2 ring-indigo-500/20 bg-indigo-50/40 dark:bg-indigo-950/30'
                  : 'border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-slate-50/50 dark:bg-slate-900/50'
              }`}
            >
              <IconComp className={`w-5 h-5 ${h.color}`} />
              <span
                className={`text-xs font-semibold truncate ${
                  isSelected
                    ? 'text-indigo-600 dark:text-indigo-400 font-bold'
                    : 'text-slate-700 dark:text-slate-300'
                }`}
              >
                {h.name}
              </span>
            </button>
          );
        })}
      </div>

      {/* Summary Metrics for Selected Hazard */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/60 dark:border-slate-700/60 text-xs">
        <div>
          <span className="text-slate-500 block mb-0.5">Current Status</span>
          <span className={`text-base font-bold font-mono ${getRiskColor(currentRiskState)}`}>
            {currentRiskState}
          </span>
          <span className="text-[11px] text-slate-400 block font-mono">
            Score: {currentScore}
          </span>
        </div>

        <div>
          <span className="text-slate-500 block mb-0.5">Projected Peak Risk</span>
          <span className={`text-base font-bold font-mono ${getRiskColor(futureRiskState)}`}>
            {futureRiskState}
          </span>
          <span className="text-[11px] text-slate-400 block font-mono">
            Score: {peakScore} ({peakWindow})
          </span>
        </div>

        <div>
          <span className="text-slate-500 block mb-1">Directional Trend</span>
          <RiskTrendIndicator trend={trend} size="sm" />
        </div>

        <div>
          <span className="text-slate-500 block mb-1">Confidence & Uncertainty</span>
          <UncertaintyBadge
            confidence={confidence}
            uncertainty={uncertainty}
            showLabels={false}
          />
        </div>
      </div>
    </div>
  );
};

export default HazardForecastCard;
