import React from 'react';
import { ParticleFieldCanvas } from '../common/ParticleFieldCanvas';
import { MagneticButton } from '../common/MagneticButton';
import { ArrowDown, ArrowUpRight, Shield, Activity, Compass, Cpu } from 'lucide-react';

interface HeroSectionProps {
  onExploreMap: () => void;
  onAnalyzeArea: () => void;
  onHowItWorks: () => void;
}

export const HeroSection: React.FC<HeroSectionProps> = ({
  onExploreMap,
  onAnalyzeArea,
  onHowItWorks,
}) => {
  return (
    <section className="relative min-h-[92vh] flex items-center justify-center pt-28 pb-20 px-4 sm:px-6 lg:px-8 overflow-hidden">
      {/* Background Interactive Particle Field Canvas */}
      <ParticleFieldCanvas className="opacity-95" particleCount={62} isHero={true} />

      {/* Subtle India Geographic Latitude & Longitude Axis Backdrop */}
      <div className="absolute inset-0 pointer-events-none flex items-center justify-center -z-0 opacity-40">
        <div className="w-[820px] h-[580px] rounded-[48px] border border-dashed border-charcoal-300/40 relative">
          <div className="absolute top-4 left-6 text-[10px] font-mono text-charcoal-400">
            LAT 8.4°N — 37.6°N // LONG 68.7°E — 97.2°E
          </div>
          <div className="absolute bottom-4 right-6 text-[10px] font-mono text-charcoal-400">
            GEOSPATIAL REFERENCE GRID // INDIA
          </div>
          {/* Subtle crosshair intersections */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 flex items-center justify-center text-charcoal-300">
            +
          </div>
        </div>
      </div>

      {/* Radial ambient background lighting */}
      <div className="absolute inset-0 bg-gradient-to-b from-paper-100/10 via-transparent to-paper-100 pointer-events-none" />

      {/* Main Container */}
      <div className="relative max-w-5xl mx-auto text-center z-10 flex flex-col items-center">
        {/* Subtle Top Metadata Pill */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/95 border border-paper-300 shadow-subtle mb-8 backdrop-blur-sm">
          <span className="w-2 h-2 rounded-full bg-risk-low animate-pulse" />
          <span className="font-mono text-xs uppercase tracking-wider text-charcoal-700 font-semibold">
            AI-POWERED DISASTER INTELLIGENCE
          </span>
          <span className="text-charcoal-300">•</span>
          <span className="font-mono text-[9px] uppercase tracking-wider text-charcoal-500 font-semibold">
            RESEARCH PROTOTYPE
          </span>
        </div>

        {/* Editorial Headline with Intentional 2-Line Composition */}
        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-charcoal-950 max-w-4xl leading-[1.12] mb-6">
          <span className="block">Know the Risk.</span>
          <span className="block font-light text-charcoal-600 mt-1 sm:mt-2">
            Prepare Before It Matters.
          </span>
        </h1>

        {/* Supporting Line */}
        <p className="text-base sm:text-xl text-charcoal-600 max-w-2xl font-normal leading-relaxed mb-10">
          An intelligent view of disaster risk across India, designed to combine environmental, geographical, and historical signals for early community resilience.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 w-full sm:w-auto mb-12">
          <MagneticButton
            size="lg"
            variant="primary"
            onClick={onExploreMap}
            className="w-full sm:w-auto"
          >
            <span>Explore Risk Map</span>
            <Compass className="w-4 h-4 opacity-70" />
          </MagneticButton>

          <MagneticButton
            size="lg"
            variant="secondary"
            onClick={onAnalyzeArea}
            className="w-full sm:w-auto"
          >
            <span>Analyze My Area</span>
            <ArrowUpRight className="w-4 h-4 opacity-70" />
          </MagneticButton>
        </div>

        {/* Secondary Sub-action Link */}
        <button
          onClick={onHowItWorks}
          className="group inline-flex items-center gap-1.5 text-xs font-mono uppercase tracking-wider text-charcoal-500 hover:text-charcoal-950 transition-colors focus:outline-none"
        >
          <span>How it works</span>
          <ArrowDown className="w-3.5 h-3.5 transition-transform group-hover:translate-y-0.5" />
        </button>

        {/* Micro Telemetry Badges Strip */}
        <div className="mt-16 pt-8 border-t border-paper-300/80 w-full max-w-3xl grid grid-cols-2 sm:grid-cols-4 gap-4 text-left">
          <div className="p-3 rounded-xl bg-white/70 border border-paper-200 backdrop-blur-xs">
            <div className="flex items-center gap-1.5 text-charcoal-400 text-xs font-mono mb-0.5">
              <Shield className="w-3.5 h-3.5" />
              <span>Regions</span>
            </div>
            <div className="font-mono text-base font-bold text-charcoal-900">724 Evaluated</div>
          </div>

          <div className="p-3 rounded-xl bg-white/70 border border-paper-200 backdrop-blur-xs">
            <div className="flex items-center gap-1.5 text-charcoal-400 text-xs font-mono mb-0.5">
              <Activity className="w-3.5 h-3.5" />
              <span>Hazards</span>
            </div>
            <div className="font-mono text-base font-bold text-charcoal-900">Multi-Vector</div>
          </div>

          <div className="p-3 rounded-xl bg-white/70 border border-paper-200 backdrop-blur-xs">
            <div className="flex items-center gap-1.5 text-charcoal-400 text-xs font-mono mb-0.5">
              <Cpu className="w-3.5 h-3.5" />
              <span>Prediction</span>
            </div>
            <div className="font-mono text-base font-bold text-charcoal-900">AI Risk Engine</div>
          </div>

          <div className="p-3 rounded-xl bg-white/70 border border-paper-200 backdrop-blur-xs">
            <div className="flex items-center gap-1.5 text-charcoal-400 text-xs font-mono mb-0.5">
              <Compass className="w-3.5 h-3.5" />
              <span>Relief</span>
            </div>
            <div className="font-mono text-base font-bold text-charcoal-900">Verified Portals</div>
          </div>
        </div>
      </div>
    </section>
  );
};
