import React from 'react';
import { 
  HeroSection, 
  FutureRiskHeroSection, 
  LocationRiskCheckerSection, 
  EarlyWarningNoticeSection, 
  FutureHazardCardsSection, 
  CitizenActionSection, 
  LiveRiskSnapshot, 
  CurrentDisastersSection, 
  ReliefHubSection, 
  VerifiedHelpSection, 
  HowItWorksSection, 
  FinalCTASection 
} from '../home';
import { ScrollReveal } from '../common/ScrollReveal';
import { RegionRiskData } from '../../types/risk';
import { DisasterEvent } from '../../types/disaster';
import { NavigationPage } from '../common/Navbar';

interface HomePageProps {
  onNavigate: (page: NavigationPage) => void;
  onSelectRegion: (region: RegionRiskData) => void;
  onSelectIncident: (incident: DisasterEvent) => void;
}

export const HomePage: React.FC<HomePageProps> = ({
  onNavigate,
  onSelectRegion,
  onSelectIncident,
}) => {
  const scrollToChecker = () => {
    const el = document.getElementById('location-checker') || document.getElementById('analyze-section') || document.getElementById('check-location');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const scrollToFutureRisk = () => {
    const el = document.getElementById('future-risk');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const scrollToEarlyWarnings = () => {
    const el = document.getElementById('early-warnings');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const scrollToHowItWorks = () => {
    const el = document.getElementById('how-it-works');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <main className="space-y-6">
      {/* 1. Hero Section: CURRENT RISK + FUTURE RISK + EARLY WARNING + ACTION */}
      <HeroSection
        onExploreMap={() => onNavigate('risk-map')}
        onAnalyzeArea={scrollToChecker}
        onCheckFutureRisk={scrollToFutureRisk}
        onSeeEarlyWarnings={scrollToEarlyWarnings}
        onHowItWorks={scrollToHowItWorks}
      />

      {/* 2. Future Risk Hero: WHAT COULD HAPPEN NEXT? (5 Horizons: NOW to 7 Days, Defaults to National Overview) */}
      <ScrollReveal>
        <FutureRiskHeroSection 
          onOpenFullMap={() => onNavigate('risk-map')}
          onSelectLocation={scrollToChecker}
          onViewDetailedPage={() => onNavigate('future-risk')}
          onViewEarlyWarnings={scrollToEarlyWarnings}
        />
      </ScrollReveal>

      {/* 3. Location Risk Checker: Live State -> District -> City Analysis (Zero Demo Mocks) */}
      <ScrollReveal>
        <LocationRiskCheckerSection 
          onOpenMap={() => onNavigate('risk-map')}
          onViewFullAnalysis={() => onNavigate('future-risk')}
        />
      </ScrollReveal>

      {/* 4. Early Warning Notices: Official Bulletins & Strict Preparation vs Evacuation Demarcation */}
      <ScrollReveal>
        <EarlyWarningNoticeSection 
          onViewAllWarnings={() => onNavigate('disasters')}
        />
      </ScrollReveal>

      {/* 5. 6-Hazard Predictive Risk Cards (Flood, Cyclone, Heatwave, Weather, Landslide, Earthquake) */}
      <ScrollReveal>
        <FutureHazardCardsSection 
          onSelectHazard={() => {
            const el = document.getElementById('future-risk');
            el?.scrollIntoView({ behavior: 'smooth' });
          }}
        />
      </ScrollReveal>

      {/* 6. Citizen Action Protocols: WHAT SHOULD I DO? (Do Now, Before, During, After, 72h Family Kit) */}
      <ScrollReveal>
        <CitizenActionSection onNavigate={onNavigate} />
      </ScrollReveal>

      {/* Deep Citizen Exploration Hub */}
      <ScrollReveal>
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto py-6">
          <div className="p-6 sm:p-8 rounded-3xl bg-slate-50 border border-slate-200 space-y-4 shadow-xs">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <span className="text-[11px] font-mono uppercase tracking-wider text-blue-700 font-bold block">
                  CITIZEN INTELLIGENCE PORTAL // DEEPER PERSPECTIVES
                </span>
                <h3 className="text-xl sm:text-2xl font-black text-slate-900">
                  Explore Specialized Disaster Intelligence
                </h3>
                <p className="text-xs sm:text-sm text-slate-600 mt-1">
                  Move beyond surface headlines into forward modeling, secondary causality, and verified citizen defense.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-2">
              <button
                onClick={() => onNavigate('future-risk')}
                className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-blue-500 hover:shadow-xs text-left transition-all group min-h-[44px] flex flex-col justify-between"
              >
                <div>
                  <div className="text-[10px] font-mono font-bold uppercase text-blue-700 mb-1.5 flex items-center justify-between">
                    <span>01 // FORWARD OUTLOOK</span>
                    <span className="text-blue-500 group-hover:translate-x-0.5 transition-transform">→</span>
                  </div>
                  <h4 className="font-bold text-slate-900 text-base group-hover:text-blue-700 transition-colors">
                    Future Risk Projections
                  </h4>
                  <p className="text-xs text-slate-600 mt-1.5 leading-relaxed font-sans">
                    5 forecast horizons from NOW to 7 days across all 36 monitored States &amp; UTs.
                  </p>
                </div>
                <div className="mt-3 text-[10px] font-mono text-slate-500 font-semibold pt-2 border-t border-slate-100">
                  NWP Forecast Fusion
                </div>
              </button>

              <button
                onClick={() => onNavigate('cascading-risk')}
                className="p-5 rounded-2xl bg-amber-50/50 border border-amber-300 hover:border-amber-500 hover:shadow-xs text-left transition-all group min-h-[44px] flex flex-col justify-between relative overflow-hidden"
              >
                <div>
                  <div className="text-[10px] font-mono font-bold uppercase text-amber-800 mb-1.5 flex items-center justify-between">
                    <span className="font-extrabold">02 // WHAT HAPPENS NEXT?</span>
                    <span className="text-amber-700 group-hover:translate-x-0.5 transition-transform">→</span>
                  </div>
                  <h4 className="font-bold text-slate-900 text-base group-hover:text-amber-800 transition-colors">
                    Cascading Risk Intelligence
                  </h4>
                  <p className="text-xs text-slate-700 mt-1.5 leading-relaxed font-sans font-medium">
                    &ldquo;A disaster happens — what could happen NEXT?&rdquo; Trace the 5-stage causal consequence sequence.
                  </p>
                </div>
                <div className="mt-3 text-[10px] font-mono text-amber-800 font-bold pt-2 border-t border-amber-200">
                  Secondary Hazards &amp; Lifelines →
                </div>
              </button>

              <button
                onClick={() => onNavigate('safety-guide')}
                className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-emerald-500 hover:shadow-xs text-left transition-all group min-h-[44px] flex flex-col justify-between"
              >
                <div>
                  <div className="text-[10px] font-mono font-bold uppercase text-emerald-700 mb-1.5 flex items-center justify-between">
                    <span>03 // LIFE SAFETY</span>
                    <span className="text-emerald-500 group-hover:translate-x-0.5 transition-transform">→</span>
                  </div>
                  <h4 className="font-bold text-slate-900 text-base group-hover:text-emerald-700 transition-colors">
                    Complete Safety Guide
                  </h4>
                  <p className="text-xs text-slate-600 mt-1.5 leading-relaxed font-sans">
                    148 Before, During, and After actionable guidance protocols across all 6 disaster types.
                  </p>
                </div>
                <div className="mt-3 text-[10px] font-mono text-slate-500 font-semibold pt-2 border-t border-slate-100">
                  NDMA Verified Protocols
                </div>
              </button>

              <button
                onClick={() => onNavigate('risk-map')}
                className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-slate-400 hover:shadow-xs text-left transition-all group min-h-[44px] flex flex-col justify-between"
              >
                <div>
                  <div className="text-[10px] font-mono font-bold uppercase text-slate-600 mb-1.5 flex items-center justify-between">
                    <span>04 // GEOSPATIAL</span>
                    <span className="text-slate-500 group-hover:translate-x-0.5 transition-transform">→</span>
                  </div>
                  <h4 className="font-bold text-slate-900 text-base group-hover:text-slate-700 transition-colors">
                    Open Risk Map
                  </h4>
                  <p className="text-xs text-slate-600 mt-1.5 leading-relaxed font-sans">
                    Interactive multi-hazard geospatial map with live district telemetry across all 36 entities.
                  </p>
                </div>
                <div className="mt-3 text-[10px] font-mono text-slate-500 font-semibold pt-2 border-t border-slate-100">
                  28 States + 8 UTs Covered
                </div>
              </button>
            </div>
          </div>
        </section>
      </ScrollReveal>

      {/* 7. Live Geospatial Risk Matrix: Open Risk Map */}
      <ScrollReveal>
        <LiveRiskSnapshot
          onOpenFullMap={() => onNavigate('risk-map')}
          onSelectRegion={onSelectRegion}
          onSelectIncident={onSelectIncident}
        />
      </ScrollReveal>

      {/* 8. Active Disasters Feed */}
      <ScrollReveal>
        <CurrentDisastersSection
          onSelectIncident={onSelectIncident}
          onViewAllDisasters={() => onNavigate('disasters')}
        />
      </ScrollReveal>

      {/* 9. Disaster Relief Hub */}
      <ScrollReveal>
        <ReliefHubSection
          onNeedHelpClick={() => onNavigate('get-help')}
          onWantToHelpClick={() => onNavigate('help-others')}
        />
      </ScrollReveal>

      {/* 10. Verified Help Sources */}
      <ScrollReveal>
        <VerifiedHelpSection />
      </ScrollReveal>

      {/* 11. How It Works */}
      <ScrollReveal>
        <HowItWorksSection />
      </ScrollReveal>

      {/* 12. Final Editorial CTA */}
      <ScrollReveal>
        <FinalCTASection
          onAnalyzeArea={scrollToChecker}
          onExploreMap={() => onNavigate('risk-map')}
        />
      </ScrollReveal>
    </main>
  );
};
