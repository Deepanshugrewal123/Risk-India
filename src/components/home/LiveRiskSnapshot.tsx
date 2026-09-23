import React from 'react';
import { IndiaRiskMap } from '../map/IndiaRiskMap';
import { RegionRiskData } from '../../types/risk';
import { DisasterEvent } from '../../types/disaster';
import { ArrowUpRight, ShieldCheck, AlertCircle, TrendingUp, Clock } from 'lucide-react';
import { MagneticButton } from '../common/MagneticButton';
import { DemoBadge } from '../common/DemoBadge';

interface LiveRiskSnapshotProps {
  onOpenFullMap: () => void;
  onSelectRegion: (region: RegionRiskData) => void;
  onSelectIncident: (incident: DisasterEvent) => void;
}

export const LiveRiskSnapshot: React.FC<LiveRiskSnapshotProps> = ({
  onOpenFullMap,
  onSelectRegion,
  onSelectIncident,
}) => {
  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold">
              National Geospatial Risk Matrix
            </span>
            <DemoBadge label="GEO-INTELLIGENCE MATRIX" />
          </div>
          <h2 className="text-3xl sm:text-5xl font-bold tracking-tight text-charcoal-950">
            India, Seen Through Risk.
          </h2>
          <p className="text-sm sm:text-base text-charcoal-600 max-w-2xl mt-3 leading-relaxed">
            An authoritative view of multi-hazard vulnerability across India, combining official public incident markers with multi-year regional hazard baselines and multi-horizon predictive risk projections (NOW to 7 Days). Automated flood risk is evaluated nationwide by RISK // INDIA Flood Model v1 (risk_india_flood_v1), calibrated with satellite observations in the Assam corridor and empirical hydrometeorological proxies nationwide.
          </p>
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <div className="inline-flex items-center gap-2 text-xs text-charcoal-600 bg-paper-200/60 px-3 py-1.5 rounded-xl border border-paper-300/80">
              <TrendingUp className="w-3.5 h-3.5 text-blue-600 shrink-0" />
              <span>Future Risk Forecast: 5 Horizons (NOW, 0-6h, 6-24h, 1-3d, 3-7d)</span>
            </div>
            <div className="inline-flex items-center gap-2 text-xs text-charcoal-500 bg-paper-200/60 px-3 py-1.5 rounded-xl border border-paper-300/80">
              <AlertCircle className="w-3.5 h-3.5 text-amber-600 shrink-0" />
              <span>Regional indices reflect historical baseline climatology and reported feeds.</span>
            </div>
          </div>
        </div>

        <div className="shrink-0">
          <MagneticButton
            variant="secondary"
            size="md"
            onClick={onOpenFullMap}
            className="gap-2"
          >
            <span>Open Risk Map</span>
            <ArrowUpRight className="w-4 h-4 opacity-70" />
          </MagneticButton>
        </div>
      </div>

      {/* Interactive Map Component with Built-In Hazard Filter */}
      <IndiaRiskMap
        onSelectRegion={onSelectRegion}
        onSelectIncident={onSelectIncident}
      />
    </section>
  );
};
