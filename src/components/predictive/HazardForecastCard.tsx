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
        return 'text-rose-700 font-bold';
      case 'HIGH':
        return 'text-orange-700 font-bold';
      case 'ELEVATED':
        return 'text-amber-700 font-bold';
      case 'WATCH':
        return 'text-blue-700 font-bold';
      case 'NORMAL':
      default:
        return 'text-emerald-700 font-bold';
    }
  };

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4 sm:p-5 shadow-xs space-y-4">
      <div className="flex items-center justify-between flex-wrap gap-2 pb-2 border-b border-slate-100">
        <h4 className="text-sm font-bold uppercase tracking-wider text-slate-900">
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
                  ? 'border-blue-600 ring-2 ring-blue-500/20 bg-blue-50/50 shadow-xs'
                  : 'border-slate-200 hover:border-slate-300 bg-slate-50/50 hover:bg-white'
              }`}
            >
              <IconComp className={`w-5 h-5 ${h.color}`} />
              <span
                className={`text-xs truncate ${
                  isSelected
                    ? 'text-blue-700 font-bold'
                    : 'text-slate-700 font-medium'
                }`}
              >
                {h.name}
              </span>
            </button>
          );
        })}
      </div>

      {/* Summary Metrics for Selected Hazard */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs">
        <div>
          <span className="text-slate-500 block mb-0.5 font-medium">Current Status</span>
          <span className={`text-base font-bold font-mono ${getRiskColor(currentRiskState)}`}>
            {currentRiskState}
          </span>
          <span className="text-[11px] text-slate-500 block font-mono">
            Score: {currentScore}
          </span>
        </div>

        <div>
          <span className="text-slate-500 block mb-0.5 font-medium">Projected Peak Risk</span>
          <span className={`text-base font-bold font-mono ${getRiskColor(futureRiskState)}`}>
            {futureRiskState}
          </span>
          <span className="text-[11px] text-slate-500 block font-mono">
            Score: {peakScore} ({peakWindow})
          </span>
        </div>

        <div>
          <span className="text-slate-500 block mb-1 font-medium">Directional Trend</span>
          <RiskTrendIndicator trend={trend} size="sm" />
        </div>

        <div>
          <span className="text-slate-500 block mb-1 font-medium">Confidence & Uncertainty</span>
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
