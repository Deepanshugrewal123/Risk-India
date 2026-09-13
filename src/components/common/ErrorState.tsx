import React from 'react';
import { AlertTriangle, RotateCcw } from 'lucide-react';

interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
  retryLabel?: string;
  className?: string;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = 'Unable to Load Information',
  message = 'An error occurred while fetching the requested data. Please verify your connection or try again.',
  onRetry,
  retryLabel = 'Try Again',
  className = ''
}) => {
  return (
    <div
      className={`w-full min-h-[200px] flex flex-col items-center justify-center p-8 bg-white border border-red-200/80 rounded-2xl text-center shadow-sm ${className}`}
    >
      <div className="w-10 h-10 rounded-full bg-red-50 text-red-600 flex items-center justify-center mb-3">
        <AlertTriangle className="w-5 h-5" />
      </div>
      <h4 className="text-base font-semibold text-stone-900 mb-1">{title}</h4>
      <p className="text-xs text-stone-500 max-w-md leading-relaxed mb-4">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center space-x-2 px-4 py-2 bg-stone-900 hover:bg-stone-800 text-white rounded-lg text-xs font-medium tracking-wide transition-all shadow-sm active:scale-95"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>{retryLabel}</span>
        </button>
      )}
    </div>
  );
};
