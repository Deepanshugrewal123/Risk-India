import React from 'react';
import { RiskLevel } from '../../types/risk';
import { getRiskConfig, getRiskLevel } from '../../utils/riskLevels';
import { ShieldCheck, AlertCircle, AlertTriangle, Flame } from 'lucide-react';

interface RiskBadgeProps {
  level?: RiskLevel;
  size?: 'sm' | 'md' | 'lg';
  score?: number;
  className?: string;
  showIcon?: boolean;
}

const ICONS: Record<RiskLevel, React.ComponentType<{ className?: string }>> = {
  LOW: ShieldCheck,
  MODERATE: AlertCircle,
  HIGH: AlertTriangle,
  CRITICAL: Flame,
};

export const RiskBadge: React.FC<RiskBadgeProps> = ({
  level,
  size = 'md',
  score,
  className = '',
  showIcon = true,
}) => {
  const resolvedLevel = level || (score !== undefined ? getRiskLevel(score) : 'LOW');
  const config = getRiskConfig(resolvedLevel);
  const IconComponent = ICONS[config.level] || ShieldCheck;

  const sizeClasses = {
    sm: 'text-[11px] px-2 py-0.5 gap-1.5',
    md: 'text-xs px-2.5 py-1 gap-1.5',
    lg: 'text-sm px-3.5 py-1.5 gap-2 font-medium',
  };

  return (
    <span
      className={`inline-flex items-center rounded-full border font-mono tracking-tight font-medium ${config.badgeClass} ${sizeClasses[size]} ${className}`}
      aria-label={`Risk level: ${config.label}${score !== undefined ? `, Score: ${score}%` : ''}`}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${config.dotClass} animate-pulse`} aria-hidden="true" />
      {showIcon && <IconComponent className="w-3.5 h-3.5" aria-hidden="true" />}
      <span className="uppercase">{config.label} RISK</span>
      {score !== undefined && (
        <span className="opacity-80 font-normal">| {Math.round(score)}%</span>
      )}
    </span>
  );
};
