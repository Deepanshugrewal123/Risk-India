import React from 'react';
import { MagneticButton } from '../common/MagneticButton';
import { Compass, ArrowUpRight, ShieldCheck } from 'lucide-react';

interface FinalCTASectionProps {
  onAnalyzeArea: () => void;
  onExploreMap: () => void;
}

export const FinalCTASection: React.FC<FinalCTASectionProps> = ({
  onAnalyzeArea,
  onExploreMap,
}) => {
  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto text-center">
      <div className="rounded-3xl bg-white border border-paper-300 p-8 sm:p-16 shadow-floating relative overflow-hidden">
        {/* Subtle grid pattern background */}
        <div className="absolute inset-0 bg-grid-subtle opacity-60 pointer-events-none" />

        <div className="relative z-10 max-w-2xl mx-auto">
          <div className="inline-flex items-center gap-2 p-2 rounded-2xl bg-paper-100 border border-paper-200 mb-6 text-charcoal-700">
            <ShieldCheck className="w-5 h-5 text-risk-low-soft" />
            <span className="text-xs font-mono font-semibold uppercase tracking-wider">
              National Disaster Resilience Network
            </span>
          </div>

          <h2 className="text-3xl sm:text-5xl font-bold tracking-tight text-charcoal-950 mb-4 leading-tight">
            Preparedness Starts Before the Warning.
          </h2>

          <p className="text-sm sm:text-base text-charcoal-600 mb-10 leading-relaxed">
            Understand your risk. Know what to do. Help where it matters.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <MagneticButton
              size="lg"
              variant="primary"
              onClick={onAnalyzeArea}
              className="w-full sm:w-auto"
            >
              <span>Analyze My Area</span>
              <ArrowUpRight className="w-4 h-4 opacity-70" />
            </MagneticButton>

            <MagneticButton
              size="lg"
              variant="secondary"
              onClick={onExploreMap}
              className="w-full sm:w-auto"
            >
              <span>Explore Risk Map</span>
              <Compass className="w-4 h-4 opacity-70" />
            </MagneticButton>
          </div>
        </div>
      </div>
    </section>
  );
};
