import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingStateProps {
  message?: string;
  description?: string;
  variant?: 'card' | 'inline' | 'skeleton';
  heightClass?: string;
  className?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({
  message = 'Loading data...',
  description,
  variant = 'card',
  heightClass = 'min-h-[220px]',
  className = ''
}) => {
  if (variant === 'inline') {
    return (
      <div className={`flex items-center space-x-2 text-stone-500 py-3 ${className}`}>
        <Loader2 className="w-4 h-4 animate-spin text-stone-700" />
        <span className="text-xs tracking-wide uppercase font-medium">{message}</span>
      </div>
    );
  }

  if (variant === 'skeleton') {
    return (
      <div className={`bg-white rounded-xl border border-stone-200/80 p-6 space-y-4 animate-pulse ${className}`}>
        <div className="h-4 bg-stone-100 rounded w-1/3"></div>
        <div className="space-y-2.5">
          <div className="h-3 bg-stone-100/80 rounded w-5/6"></div>
          <div className="h-3 bg-stone-100/60 rounded w-4/6"></div>
          <div className="h-3 bg-stone-100/40 rounded w-2/3"></div>
        </div>
        <div className="pt-2 flex items-center justify-between">
          <div className="h-8 bg-stone-100 rounded-lg w-24"></div>
          <div className="h-8 bg-stone-100 rounded-lg w-32"></div>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`w-full ${heightClass} flex flex-col items-center justify-center p-8 bg-white/70 backdrop-blur-sm border border-stone-200/80 rounded-2xl text-center ${className}`}
    >
      <div className="relative mb-4">
        <div className="w-10 h-10 rounded-full border-2 border-stone-200 border-t-stone-800 animate-spin" />
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="w-2 h-2 rounded-full bg-orange-500 animate-pulse" />
        </div>
      </div>
      <p className="text-sm font-semibold text-stone-800 tracking-tight">{message}</p>
      {description && (
        <p className="text-xs text-stone-500 mt-1 max-w-sm leading-relaxed">{description}</p>
      )}
    </div>
  );
};
