import React from 'react';
import { Inbox } from 'lucide-react';

interface EmptyStateProps {
  title: string;
  description?: string;
  icon?: React.ReactNode;
  action?: {
    label: string;
    onClick: () => void;
  };
  className?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title,
  description,
  icon,
  action,
  className = ''
}) => {
  return (
    <div
      className={`w-full min-h-[220px] flex flex-col items-center justify-center p-8 bg-stone-50/60 border border-dashed border-stone-300/80 rounded-2xl text-center ${className}`}
    >
      <div className="w-11 h-11 rounded-full bg-white text-stone-400 border border-stone-200/80 flex items-center justify-center mb-3 shadow-xs">
        {icon || <Inbox className="w-5 h-5" />}
      </div>
      <h4 className="text-sm font-semibold text-stone-800 mb-1">{title}</h4>
      {description && (
        <p className="text-xs text-stone-500 max-w-sm leading-relaxed mb-4">{description}</p>
      )}
      {action && (
        <button
          onClick={action.onClick}
          className="inline-flex items-center px-4 py-1.5 bg-white hover:bg-stone-100 border border-stone-300 text-stone-800 rounded-lg text-xs font-medium tracking-wide transition-all shadow-xs"
        >
          {action.label}
        </button>
      )}
    </div>
  );
};
