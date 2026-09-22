import React from 'react';
import { Wifi, Clock, Database, AlertCircle, Sparkles, HelpCircle, TrendingUp, Shield, AlertTriangle } from 'lucide-react';

export type FreshnessStatus =
  | 'LIVE'
  | 'OFFICIAL_LIVE'
  | 'LIVE_EVIDENCE'
  | 'RECENT'
  | 'OFFICIAL_RECENT'
  | 'RECENT_EVIDENCE'
  | 'FORECAST'
  | 'FORECAST_AVAILABLE'
  | 'CACHED'
  | 'STALE'
  | 'BASELINE'
  | 'REGIONAL_BASELINE'
  | 'BASELINE_ONLY'
  | 'LIMITED_EVIDENCE'
  | 'EMPIRICAL_ML'
  | 'DATA_UNAVAILABLE'
  | 'UNAVAILABLE'
  | 'PROVIDER_DEGRADED'
  | 'DEGRADED';

interface FreshnessBadgeProps {
  status: FreshnessStatus | string;
  observedAt?: string | null;
  ageMinutes?: number | null;
  className?: string;
  size?: 'xs' | 'sm' | 'md';
  showPulse?: boolean;
}

export const FreshnessBadge: React.FC<FreshnessBadgeProps> = ({
  status,
  observedAt,
  ageMinutes,
  className = '',
  size = 'sm',
  showPulse = true,
}) => {
  const normalized = (status || 'REGIONAL_BASELINE').toUpperCase().trim().replace(/[\s-]+/g, '_');

  let label = 'REGIONAL BASELINE';
  let badgeColor = 'bg-slate-100 text-slate-800 border-slate-300';
  let dotColor = 'bg-slate-500';
  let Icon: React.ComponentType<{ className?: string }> = Shield;

  if (normalized === 'LIVE_EVIDENCE' || normalized === 'LIVE' || normalized === 'OFFICIAL_LIVE' || normalized.includes('LIVE')) {
    label = 'LIVE EVIDENCE';
    badgeColor = 'bg-emerald-50 text-emerald-800 border-emerald-300';
    dotColor = 'bg-emerald-500';
    Icon = Wifi;
  } else if (normalized === 'RECENT_EVIDENCE' || normalized === 'RECENT' || normalized === 'OFFICIAL_RECENT' || normalized.includes('RECENT')) {
    label = 'RECENT EVIDENCE';
    badgeColor = 'bg-sky-50 text-sky-800 border-sky-300';
    dotColor = 'bg-sky-500';
    Icon = Clock;
  } else if (normalized === 'FORECAST_AVAILABLE' || normalized === 'FORECAST' || normalized.includes('FORECAST') || normalized.includes('PROJECTION')) {
    label = 'FORECAST AVAILABLE';
    badgeColor = 'bg-indigo-50 text-indigo-800 border-indigo-300';
    dotColor = 'bg-indigo-500';
    Icon = TrendingUp;
  } else if (normalized === 'LIMITED_EVIDENCE' || normalized.includes('LIMITED')) {
    label = 'LIMITED EVIDENCE';
    badgeColor = 'bg-amber-50 text-amber-800 border-amber-300';
    dotColor = 'bg-amber-500';
    Icon = HelpCircle;
  } else if (normalized === 'BASELINE_ONLY' || normalized === 'BASELINE' || normalized === 'REGIONAL_BASELINE' || normalized.includes('BASELINE')) {
    label = 'BASELINE ONLY';
    badgeColor = 'bg-slate-100 text-slate-800 border-slate-300';
    dotColor = 'bg-slate-500';
    Icon = Shield;
  } else if (normalized === 'CACHED' || normalized.includes('CACHE')) {
    label = 'CACHED';
    badgeColor = 'bg-amber-50 text-amber-800 border-amber-300';
    dotColor = 'bg-amber-500';
    Icon = Database;
  } else if (normalized === 'STALE' || normalized.includes('STALE')) {
    label = 'STALE (>24H)';
    badgeColor = 'bg-rose-50 text-rose-800 border-rose-300';
    dotColor = 'bg-rose-500';
    Icon = AlertCircle;
  } else if (normalized === 'EMPIRICAL_ML' || normalized.includes('ML')) {
    label = 'EMPIRICAL ML';
    badgeColor = 'bg-purple-50 text-purple-800 border-purple-300';
    dotColor = 'bg-purple-500';
    Icon = Sparkles;
  } else if (
    normalized === 'PROVIDER_DEGRADED' ||
    normalized === 'DEGRADED' ||
    normalized.includes('DEGRADED')
  ) {
    label = 'PROVIDER DEGRADED';
    badgeColor = 'bg-orange-50 text-orange-800 border-orange-300';
    dotColor = 'bg-orange-500';
    Icon = AlertTriangle;
  } else if (
    normalized === 'DATA_UNAVAILABLE' ||
    normalized === 'UNAVAILABLE' ||
    normalized.includes('UNAVAILABLE')
  ) {
    label = 'DATA UNAVAILABLE';
    badgeColor = 'bg-zinc-100 text-zinc-700 border-zinc-300';
    dotColor = 'bg-zinc-400';
    Icon = HelpCircle;
  } else {
    // Default: BASELINE ONLY
    label = 'BASELINE ONLY';
    badgeColor = 'bg-slate-100 text-slate-800 border-slate-300';
    dotColor = 'bg-slate-500';
    Icon = Shield;
  }

  const sizeClasses = {
    xs: 'text-[9px] px-1.5 py-0.5 gap-1',
    sm: 'text-[10px] px-2 py-0.5 gap-1.5',
    md: 'text-xs px-2.5 py-1 gap-1.5',
  };

  const titleText = ageMinutes !== undefined && ageMinutes !== null
    ? `Data Freshness: ${label} (Observed ${ageMinutes}m ago)`
    : `Data Freshness: ${label}`;

  return (
    <span
      className={`inline-flex items-center rounded-full border font-mono tracking-tight font-medium select-none ${badgeColor} ${sizeClasses[size]} ${className}`}
      title={titleText}
      aria-label={titleText}
    >
      <span
        className={`w-1.5 h-1.5 rounded-full ${dotColor} ${
          showPulse && (normalized.includes('LIVE') || normalized.includes('ML')) ? 'animate-pulse' : ''
        }`}
        aria-hidden="true"
      />
      <Icon className="w-2.5 h-2.5 opacity-80" aria-hidden="true" />
      <span>{label}</span>
      {ageMinutes !== undefined && ageMinutes !== null && ageMinutes > 0 && ageMinutes < 1440 && (
        <span className="opacity-75 font-normal">({ageMinutes}m)</span>
      )}
    </span>
  );
};
