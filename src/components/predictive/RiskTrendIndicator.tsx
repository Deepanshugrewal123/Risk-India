import React from 'react';
import { TrendState } from '../../types/predictiveRisk';
import { TrendingUp, TrendingDown, Minus, Activity, AlertTriangle } from 'lucide-react';

interface RiskTrendIndicatorProps {
  trend: TrendState;
  showText?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

export const RiskTrendIndicator: React.FC<RiskTrendIndicatorProps> = ({
  trend,
  showText = true,
  size = 'md'
}) => {
  const getConfig = () => {
    switch (trend) {
      case 'RISING':
        return {
          icon: TrendingUp,
          color: 'text-rose-600 dark:text-rose-400 bg-rose-500/10 border-rose-500/20',
          label: 'RISING',
          desc: 'Risk trajectory is escalating over the projection window'
        };
      case 'DECLINING':
        return {
          icon: TrendingDown,
          color: 'text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
          label: 'DECLINING',
          desc: 'Hazard intensity is subsiding'
        };
      case 'VOLATILE':
        return {
          icon: Activity,
          color: 'text-purple-600 dark:text-purple-400 bg-purple-500/10 border-purple-500/20',
          label: 'VOLATILE',
          desc: 'Unstable multi-model swing across forecast intervals'
        };
      case 'INSUFFICIENT_DATA':
        return {
          icon: AlertTriangle,
          color: 'text-slate-500 dark:text-slate-400 bg-slate-500/10 border-slate-500/20',
          label: 'INSUFFICIENT DATA',
          desc: 'Telemetry or numerical forecast density is below threshold'
        };
      case 'STABLE':
      default:
        return {
          icon: Minus,
          color: 'text-sky-600 dark:text-sky-400 bg-sky-500/10 border-sky-500/20',
          label: 'STABLE',
          desc: 'Conditions remain near current baseline thresholds'
        };
    }
  };

  const cfg = getConfig();
  const IconComponent = cfg.icon;

  const iconSizes = {
    sm: 'w-3 h-3',
    md: 'w-4 h-4',
    lg: 'w-5 h-5'
  };

  const textSizes = {
    sm: 'text-xs px-2 py-0.5',
    md: 'text-xs px-2.5 py-1',
    lg: 'text-sm px-3 py-1.5'
  };

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full font-semibold border ${cfg.color} ${textSizes[size]}`}
      title={cfg.desc}
    >
      <IconComponent className={iconSizes[size]} />
      {showText && <span>{cfg.label}</span>}
    </span>
  );
};

export default RiskTrendIndicator;
