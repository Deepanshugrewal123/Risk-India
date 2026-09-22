import React, { useState, useEffect } from 'react';
import { WifiOff, Wifi, X, PhoneCall, AlertTriangle } from 'lucide-react';

interface OfflineIndicatorProps {
  onOpenEmergencyHub?: () => void;
}

export const OfflineIndicator: React.FC<OfflineIndicatorProps> = ({ onOpenEmergencyHub }) => {
  const [isOnline, setIsOnline] = useState<boolean>(() => {
    return typeof navigator !== 'undefined' ? navigator.onLine : true;
  });
  const [justReconnected, setJustReconnected] = useState<boolean>(false);
  const [isDismissed, setIsDismissed] = useState<boolean>(false);
  const [showDetails, setShowDetails] = useState<boolean>(false);


  useEffect(() => {
    if (typeof window === 'undefined') return;

    const handleOnline = () => {
      setIsOnline(true);
      setIsDismissed(false);
      setJustReconnected(true);
      const timer = setTimeout(() => {
        setJustReconnected(false);
      }, 3500);
      return () => clearTimeout(timer);
    };

    const handleOffline = () => {
      setIsOnline(false);
      setJustReconnected(false);
      setIsDismissed(false);
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // When fully online and not just reconnected, do not render anything
  if (isOnline && !justReconnected) {
    return null;
  }

  // If user dismissed while offline, show only a tiny non-intrusive floating badge
  if (!isOnline && isDismissed) {
    return (
      <aside aria-label="Offline status" className="fixed top-20 right-4 z-40">
        <button
          type="button"
          onClick={() => setIsDismissed(false)}
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-amber-500 text-white text-[10px] font-mono font-bold shadow-md hover:bg-amber-600 transition-all active:scale-95 motion-reduce:active:scale-100"
          title="Browser is offline. Click to view offline capabilities."
        >
          <WifiOff className="w-3 h-3" />
          <span>OFFLINE</span>
        </button>
      </aside>
    );
  }

  // Reconnection success banner
  if (isOnline && justReconnected) {
    return (
      <aside aria-label="Connection restored notice" className="fixed top-16 sm:top-20 left-1/2 -translate-x-1/2 z-40 w-[94%] max-w-md pointer-events-auto">
        <div className="flex items-center justify-between px-3.5 py-2 rounded-2xl bg-emerald-700 text-white shadow-elevated border border-emerald-600 text-xs font-medium animate-in fade-in slide-in-from-top-2 duration-200 motion-reduce:animate-none">
          <div className="flex items-center gap-2">
            <Wifi className="w-4 h-4 text-emerald-200 shrink-0" />
            <span>Connection restored. Disaster intelligence re-synced.</span>
          </div>
          <button
            type="button"
            onClick={() => setJustReconnected(false)}
            className="p-1 text-emerald-200 hover:text-white rounded-lg transition-colors"
            aria-label="Dismiss notification"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      </aside>
    );
  }

  // Active offline banner
  return (
    <aside aria-label="Offline mode status" className="fixed top-16 sm:top-20 left-1/2 -translate-x-1/2 z-40 w-[94%] max-w-lg pointer-events-auto">
      <div className="bg-charcoal-900/95 backdrop-blur-md text-paper-50 rounded-2xl p-3 sm:p-3.5 border border-charcoal-700 shadow-floating text-xs transition-all duration-200 motion-reduce:transition-none">
        <div className="flex items-start justify-between gap-2.5">
          <div className="flex items-start gap-2.5">
            <div className="w-7 h-7 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center shrink-0 mt-0.5">
              <WifiOff className="w-3.5 h-3.5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-paper-50 tracking-tight">Offline Mode</span>
                <span className="px-1.5 py-0.5 rounded bg-amber-400/20 text-amber-300 font-mono text-[10px] font-semibold">
                  LIVE SYNC PAUSED
                </span>
              </div>
              <p className="text-charcoal-300 text-[11px] leading-relaxed mt-0.5">
                Displaying locally cached risk data and emergency hotlines. Live telemetry feeds will resume once connectivity returns.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-1 shrink-0">
            <button
              type="button"
              onClick={() => setShowDetails(!showDetails)}
              className="px-2 py-1 rounded-lg text-[10px] font-mono text-charcoal-300 hover:text-white bg-charcoal-800 hover:bg-charcoal-700 transition-colors"
            >
              {showDetails ? 'Hide' : 'SOS'}
            </button>
            <button
              type="button"
              onClick={() => setIsDismissed(true)}
              className="p-1 rounded-lg text-charcoal-400 hover:text-white transition-colors"
              aria-label="Dismiss offline banner"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {showDetails && (
          <div className="mt-3 pt-2.5 border-t border-charcoal-800 flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-1 text-[11px] text-charcoal-300">
              <AlertTriangle className="w-3.5 h-3.5 text-amber-400 shrink-0" />
              <span>Offline telephone helplines remain active via cellular voice:</span>
            </div>
            <div className="flex items-center gap-2 font-mono text-[11px]">
              <a
                href="tel:112"
                className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-rose-600 text-white hover:bg-rose-700 font-bold"
              >
                <PhoneCall className="w-3 h-3" />
                <span>Call 112</span>
              </a>
              <a
                href="tel:1078"
                className="px-2 py-1 rounded bg-charcoal-800 text-charcoal-200 hover:bg-charcoal-700"
              >
                1078 (NDMA)
              </a>
              {onOpenEmergencyHub && (
                <button
                  type="button"
                  onClick={onOpenEmergencyHub}
                  className="px-2 py-1 rounded bg-amber-500/30 text-amber-200 hover:bg-amber-500/50 underline font-sans"
                >
                  All Helplines & Safety Guide →
                </button>
              )}
            </div>
          </div>
        )}

      </div>
    </aside>
  );
};

export default OfflineIndicator;
