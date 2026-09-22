import React, { useEffect, useState } from 'react';
import { AlertTriangle, ArrowRight, ShieldAlert, X } from 'lucide-react';
import { useCrisis } from '../../context/CrisisContext';
import { crisisService, CrisisStatusResponse } from '../../services/crisisService';

interface CrisisRecommendedBannerProps {
  currentRegion?: string;
  onSelectRegion?: (regionId: string) => void;
}

export const CrisisRecommendedBanner: React.FC<CrisisRecommendedBannerProps> = ({
  currentRegion,
  onSelectRegion
}) => {
  const { isCrisisMode, setCrisisMode } = useCrisis();
  const [statusData, setStatusData] = useState<CrisisStatusResponse | null>(null);
  const [dismissed, setDismissed] = useState<boolean>(false);

  useEffect(() => {
    let isMounted = true;
    crisisService.getStatus().then((data) => {
      if (isMounted) setStatusData(data);
    }).catch(() => {});

    return () => {
      isMounted = false;
    };
  }, []);

  if (isCrisisMode || dismissed || !statusData || statusData.crisis_recommended_count === 0) {
    return null;
  }

  const activeRegions = statusData.crisis_recommended_regions;
  const targetRegion = currentRegion
    ? activeRegions.find(r => r.region_id.toLowerCase() === currentRegion.toLowerCase()) || activeRegions[0]
    : activeRegions[0];

  return (
    <div className="bg-gradient-to-r from-red-600 via-rose-600 to-amber-600 text-white shadow-md border-b border-red-700/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-2.5 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs sm:text-sm font-sans">
        <div className="flex items-center gap-2.5">
          <div className="p-1 rounded bg-white/20 text-white shrink-0">
            <ShieldAlert className="w-4 h-4 animate-pulse" />
          </div>
          <div>
            <span className="font-bold tracking-wide uppercase bg-black/30 px-2.5 py-0.5 rounded text-[11px] mr-2 border border-white/20">
              ⚠️ CONDITIONS MAY BE DANGEROUS
            </span>
            <span>
              <strong>Crisis Mode Recommended for {targetRegion.region_name}:</strong>{' '}
              <span className="opacity-90">{targetRegion.activation_reason}</span>
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <button
            onClick={() => {
              if (onSelectRegion && targetRegion) {
                onSelectRegion(targetRegion.region_id);
              }
              setCrisisMode(true);
            }}
            className="px-3.5 py-1.5 rounded-lg bg-white text-red-700 font-bold hover:bg-red-50 transition-colors shadow-sm flex items-center gap-1.5 text-xs font-mono tracking-tight"
          >
            <span>See What You Should Do Now</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => setDismissed(true)}
            className="p-1.5 rounded hover:bg-white/10 text-white/80 hover:text-white transition-colors"
            title="Dismiss notification"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
