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
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto py-4">
          <div className="p-6 sm:p-8 rounded-3xl bg-paper-50 dark:bg-slate-900 border border-paper-300 dark:border-slate-800 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <span className="text-[11px] font-mono uppercase tracking-wider text-indigo-700 dark:text-indigo-400 font-bold block">
                  CITIZEN INTELLIGENCE PORTAL // DEEPER PERSPECTIVES
                </span>
                <h3 className="text-xl sm:text-2xl font-bold text-charcoal-950 dark:text-white">
                  Explore Specialized Disaster Intelligence
                </h3>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-2">
              <button
                onClick={() => onNavigate('future-risk')}
                className="p-4 rounded-2xl bg-white dark:bg-slate-850 border border-paper-200 dark:border-slate-800 hover:border-indigo-400 dark:hover:border-indigo-600 text-left transition-all shadow-xs group min-h-[44px]"
              >
                <div className="text-xs font-mono font-bold uppercase text-indigo-600 dark:text-indigo-400 mb-1">
                  01 // FORWARD OUTLOOK
                </div>
                <h4 className="font-bold text-charcoal-900 dark:text-white text-base group-hover:text-indigo-600 transition-colors">
                  Future Risk Projections
                </h4>
                <p className="text-xs text-charcoal-600 dark:text-slate-400 mt-1">
                  5 forecast horizons from NOW to 7 days across all 36 States & UTs.
                </p>
              </button>

              <button
                onClick={() => onNavigate('cascading-risk')}
                className="p-4 rounded-2xl bg-white dark:bg-slate-850 border border-paper-200 dark:border-slate-800 hover:border-indigo-400 dark:hover:border-indigo-600 text-left transition-all shadow-xs group min-h-[44px]"
              >
                <div className="text-xs font-mono font-bold uppercase text-indigo-600 dark:text-indigo-400 mb-1">
                  02 // WHAT HAPPENS NEXT
                </div>
                <h4 className="font-bold text-charcoal-900 dark:text-white text-base group-hover:text-indigo-600 transition-colors">
                  Cascading Risk Intelligence
                </h4>
                <p className="text-xs text-charcoal-600 dark:text-slate-400 mt-1">
                  Trace secondary hazards and systemic breakdowns triggered by initial events.
                </p>
              </button>

              <button
                onClick={() => onNavigate('safety-guide')}
                className="p-4 rounded-2xl bg-white dark:bg-slate-850 border border-paper-200 dark:border-slate-800 hover:border-emerald-400 dark:hover:border-emerald-600 text-left transition-all shadow-xs group min-h-[44px]"
              >
                <div className="text-xs font-mono font-bold uppercase text-emerald-600 dark:text-emerald-400 mb-1">
                  03 // LIFE SAFETY
                </div>
                <h4 className="font-bold text-charcoal-900 dark:text-white text-base group-hover:text-emerald-600 transition-colors">
                  Complete Safety Guide
                </h4>
                <p className="text-xs text-charcoal-600 dark:text-slate-400 mt-1">
                  Before, During, and After actionable guidance across all 6 disaster types.
                </p>
              </button>

              <button
                onClick={() => onNavigate('risk-map')}
                className="p-4 rounded-2xl bg-white dark:bg-slate-850 border border-paper-200 dark:border-slate-800 hover:border-charcoal-500 text-left transition-all shadow-xs group min-h-[44px]"
              >
                <div className="text-xs font-mono font-bold uppercase text-charcoal-500 dark:text-slate-400 mb-1">
                  04 // GEOSPATIAL
                </div>
                <h4 className="font-bold text-charcoal-900 dark:text-white text-base group-hover:text-charcoal-700 transition-colors">
                  Open Risk Map
                </h4>
                <p className="text-xs text-charcoal-600 dark:text-slate-400 mt-1">
                  Interactive multi-hazard geospatial map with live district telemetry.
                </p>
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
