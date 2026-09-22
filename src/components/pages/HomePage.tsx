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
        <CitizenActionSection />
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
