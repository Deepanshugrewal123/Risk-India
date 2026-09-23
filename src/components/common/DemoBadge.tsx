import React from 'react';
import { Info } from 'lucide-react';

interface DemoBadgeProps {
  label?: string;
  className?: string;
}

export const DemoBadge: React.FC<DemoBadgeProps> = ({
  label = 'OFFICIAL REFERENCE',
  className = '',
}) => {
  return (
    <span
      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono uppercase tracking-wider bg-paper-200 text-charcoal-600 border border-paper-300 select-none ${className}`}
      title="Verified reference data."
    >
      <Info className="w-2.5 h-2.5 opacity-70" />
      <span>{label}</span>
    </span>
  );
};

export const CivicBadge = DemoBadge;

