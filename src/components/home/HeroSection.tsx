import React from 'react';
import { ParticleFieldCanvas } from '../common/ParticleFieldCanvas';
import { MagneticButton } from '../common/MagneticButton';
import {
  ArrowDown,
  ArrowUpRight,
  Shield,
  Activity,
  Compass,
  Sparkles,
  TrendingUp,
  Clock,
  CheckCircle2,
  PhoneCall,
  BellRing
} from 'lucide-react';

interface HeroSectionProps {
  onExploreMap: () => void;
  onAnalyzeArea: () => void;
  onHowItWorks: () => void;
  onCheckFutureRisk?: () => void;
  onSeeEarlyWarnings?: () => void;
}

export const HeroSection: React.FC<HeroSectionProps> = ({
  onExploreMap,
  onAnalyzeArea,
  onHowItWorks,
  onCheckFutureRisk,
  onSeeEarlyWarnings,
}) => {
  const handleFutureRiskClick = () => {
    if (onCheckFutureRisk) {
      onCheckFutureRisk();
    } else {
      const el = document.getElementById('future-risk');
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  const handleEarlyWarningsClick = () => {
    if (onSeeEarlyWarnings) {
      onSeeEarlyWarnings();
    } else {
      const el = document.getElementById('early-warnings');
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  return (
    <section className="relative min-h-[92vh] flex items-center justify-center pt-28 pb-16 px-4 sm:px-6 lg:px-8 overflow-hidden">
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
          <span className="font-mono text-xs uppercase tracking-wider text-charcoal-800 font-semibold">
            CURRENT RISK • FUTURE RISK • EARLY WARNING • ACTION
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
          An authoritative disaster intelligence platform for India. Track active hazard events, inspect multi-horizon future risk forecasts, heed official early warnings, and execute verified family safety protocols.
        </p>

        {/* Primary CTA Buttons (Open Risk Map + Check Future Risk + See Early Warnings + Check Risk for My Location) */}
        <div className="flex flex-col sm:flex-row flex-wrap items-center justify-center gap-3 w-full sm:w-auto mb-10">
          <MagneticButton
            size="lg"
            variant="primary"
            onClick={onExploreMap}
            className="w-full sm:w-auto shadow-md"
          >
            <span>Open Risk Map</span>
            <Compass className="w-4 h-4 opacity-70" />
          </MagneticButton>

          <MagneticButton
            size="lg"
            variant="secondary"
            onClick={handleFutureRiskClick}
            className="w-full sm:w-auto border-indigo-300 text-indigo-950 bg-indigo-50/80 hover:bg-indigo-100 hover:border-indigo-400 shadow-sm"
          >
            <Sparkles className="w-4 h-4 text-indigo-600" />
            <span>Check Future Risk</span>
            <TrendingUp className="w-4 h-4 text-indigo-600 opacity-70" />
          </MagneticButton>

          <MagneticButton
            size="lg"
            variant="secondary"
            onClick={handleEarlyWarningsClick}
            className="w-full sm:w-auto border-amber-300 text-amber-950 bg-amber-50/80 hover:bg-amber-100 hover:border-amber-400 shadow-sm"
          >
            <BellRing className="w-4 h-4 text-amber-600" />
            <span>See Early Warnings</span>
          </MagneticButton>

          <MagneticButton
            size="lg"
            variant="secondary"
            onClick={onAnalyzeArea}
            className="w-full sm:w-auto shadow-sm"
          >
            <span>Check Risk for My Location</span>
            <ArrowUpRight className="w-4 h-4 opacity-70" />
          </MagneticButton>
        </div>

        {/* Secondary Sub-action Link */}
        <button
          onClick={onHowItWorks}
          className="group inline-flex items-center gap-1.5 text-xs font-mono uppercase tracking-wider text-charcoal-500 hover:text-charcoal-950 transition-colors focus:outline-none mb-12"
        >
          <span>How it works</span>
          <ArrowDown className="w-3.5 h-3.5 transition-transform group-hover:translate-y-0.5" />
        </button>

        {/* First-Viewport Citizen Disaster Intelligence Strip (Answers the 6 Plain-Language Questions) */}
        <div className="pt-6 border-t border-paper-300/80 w-full max-w-4xl">
          <div className="text-[10px] font-mono uppercase tracking-widest text-charcoal-500 font-bold mb-3 text-center sm:text-left flex items-center justify-center sm:justify-between">
            <span>CITIZEN INTELLIGENCE // 6 CORE QUESTIONS AT A GLANCE</span>
            <span className="hidden sm:inline-block text-indigo-600 font-semibold">ALL 36 STATES & UTs COVERED</span>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5 text-left">
            {/* 1. What is happening now? */}
            <div className="p-3 rounded-xl bg-white/80 border border-paper-200 backdrop-blur-xs flex flex-col justify-between hover:border-paper-400 transition-colors">
              <div>
                <div className="flex items-center gap-1 text-charcoal-400 text-[10px] font-mono mb-1">
                  <Activity className="w-3 h-3 text-emerald-600" />
                  <span>1. Happening Now</span>
                </div>
                <div className="font-mono text-xs font-bold text-charcoal-900 leading-tight">Live Telemetry</div>
              </div>
              <div className="text-[10px] text-charcoal-500 mt-1">36 States & UTs Monitored</div>
            </div>

            {/* 2. What could happen next? */}
            <div className="p-3 rounded-xl bg-white/80 border border-paper-200 backdrop-blur-xs flex flex-col justify-between hover:border-paper-400 transition-colors">
              <div>
                <div className="flex items-center gap-1 text-charcoal-400 text-[10px] font-mono mb-1">
                  <Sparkles className="w-3 h-3 text-indigo-600" />
                  <span>2. Happening Next</span>
                </div>
                <div className="font-mono text-xs font-bold text-charcoal-900 leading-tight">5 Horizons</div>
              </div>
              <div className="text-[10px] text-charcoal-500 mt-1">NOW to 7 Days Ahead</div>
            </div>

            {/* 3. Is risk increasing or decreasing? */}
            <div className="p-3 rounded-xl bg-white/80 border border-paper-200 backdrop-blur-xs flex flex-col justify-between hover:border-paper-400 transition-colors">
              <div>
                <div className="flex items-center gap-1 text-charcoal-400 text-[10px] font-mono mb-1">
                  <TrendingUp className="w-3 h-3 text-amber-600" />
                  <span>3. Risk Trend</span>
                </div>
                <div className="font-mono text-xs font-bold text-charcoal-900 leading-tight">Trajectory</div>
              </div>
              <div className="text-[10px] text-charcoal-500 mt-1">Increasing / Receding</div>
            </div>

            {/* 4. How soon could conditions change? */}
            <div className="p-3 rounded-xl bg-white/80 border border-paper-200 backdrop-blur-xs flex flex-col justify-between hover:border-paper-400 transition-colors">
              <div>
                <div className="flex items-center gap-1 text-charcoal-400 text-[10px] font-mono mb-1">
                  <Clock className="w-3 h-3 text-blue-600" />
                  <span>4. Timing</span>
                </div>
                <div className="font-mono text-xs font-bold text-charcoal-900 leading-tight">0–6h to 72h</div>
              </div>
              <div className="text-[10px] text-charcoal-500 mt-1">Rapid Lead Windows</div>
            </div>

            {/* 5. What should I do? */}
            <div className="p-3 rounded-xl bg-white/80 border border-paper-200 backdrop-blur-xs flex flex-col justify-between hover:border-paper-400 transition-colors">
              <div>
                <div className="flex items-center gap-1 text-charcoal-400 text-[10px] font-mono mb-1">
                  <CheckCircle2 className="w-3 h-3 text-indigo-600" />
                  <span>5. What To Do</span>
                </div>
                <div className="font-mono text-xs font-bold text-charcoal-900 leading-tight">Action Steps</div>
              </div>
              <div className="text-[10px] text-charcoal-500 mt-1">Do Now & 72h Kit</div>
            </div>

            {/* 6. Where can I get verified help? */}
            <div className="p-3 rounded-xl bg-white/80 border border-paper-200 backdrop-blur-xs flex flex-col justify-between hover:border-paper-400 transition-colors">
              <div>
                <div className="flex items-center gap-1 text-charcoal-400 text-[10px] font-mono mb-1">
                  <PhoneCall className="w-3 h-3 text-rose-600" />
                  <span>6. Verified Help</span>
                </div>
                <div className="font-mono text-xs font-bold text-charcoal-900 leading-tight">112 / 1078</div>
              </div>
              <div className="text-[10px] text-charcoal-500 mt-1">24/7 Pan-India Direct</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
