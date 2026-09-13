import React from 'react';
import { HeroSection } from '../home/HeroSection';
import { LiveRiskSnapshot } from '../home/LiveRiskSnapshot';
import { AnalyzeAreaSection } from '../home/AnalyzeAreaSection';
import { CurrentDisastersSection } from '../home/CurrentDisastersSection';
import { PreparednessSection } from '../home/PreparednessSection';
import { AIAssistantSection } from '../home/AIAssistantSection';
import { ReliefHubSection } from '../home/ReliefHubSection';
import { VerifiedHelpSection } from '../home/VerifiedHelpSection';
import { HowItWorksSection } from '../home/HowItWorksSection';
import { FinalCTASection } from '../home/FinalCTASection';
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
  const scrollToAnalyze = () => {
    const el = document.getElementById('analyze-section');
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
    <main className="space-y-4">
      {/* 1. Hero Section (Immediate display, zero delay) */}
      <HeroSection
        onExploreMap={() => onNavigate('risk-map')}
        onAnalyzeArea={scrollToAnalyze}
        onHowItWorks={scrollToHowItWorks}
      />

      {/* 2. Section A: Live India Risk Snapshot */}
      <ScrollReveal>
        <LiveRiskSnapshot
          onOpenFullMap={() => onNavigate('risk-map')}
          onSelectRegion={onSelectRegion}
          onSelectIncident={onSelectIncident}
        />
      </ScrollReveal>

      {/* 3. Section B: Analyze Your Area */}
      <ScrollReveal>
        <AnalyzeAreaSection />
      </ScrollReveal>

      {/* 4. Section C: Current Disasters */}
      <ScrollReveal>
        <CurrentDisastersSection
          onSelectIncident={onSelectIncident}
          onViewAllDisasters={() => onNavigate('disasters')}
        />
      </ScrollReveal>

      {/* 5. Section D: Prepare Before It Happens */}
      <ScrollReveal>
        <PreparednessSection />
      </ScrollReveal>

      {/* 6. Section E: AI Disaster Assistant */}
      <ScrollReveal>
        <AIAssistantSection />
      </ScrollReveal>

      {/* 7. Section F: Disaster Relief Hub */}
      <ScrollReveal>
        <ReliefHubSection
          onNeedHelpClick={() => onNavigate('get-help')}
          onWantToHelpClick={() => onNavigate('help-others')}
        />
      </ScrollReveal>

      {/* 8. Section G: Verified Help Sources */}
      <ScrollReveal>
        <VerifiedHelpSection />
      </ScrollReveal>

      {/* 9. Section H: How It Works */}
      <ScrollReveal>
        <HowItWorksSection />
      </ScrollReveal>

      {/* 10. Section I: Final Editorial CTA */}
      <ScrollReveal>
        <FinalCTASection
          onAnalyzeArea={scrollToAnalyze}
          onExploreMap={() => onNavigate('risk-map')}
        />
      </ScrollReveal>
    </main>
  );
};
