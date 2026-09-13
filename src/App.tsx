import React, { useState, useEffect } from 'react';
import { Navbar, NavigationPage } from './components/common/Navbar';
import { Footer } from './components/common/Footer';
import { HomePage } from './components/pages/HomePage';
import { RiskMapPage } from './components/pages/RiskMapPage';
import { DisastersPage } from './components/pages/DisastersPage';
import { GetHelpPage } from './components/pages/GetHelpPage';
import { HelpOthersPage } from './components/pages/HelpOthersPage';
import { HowItWorksPage } from './components/pages/HowItWorksPage';
import { DisasterDetailModal } from './components/modals/DisasterDetailModal';
import { RegionRiskData } from './types/risk';
import { DisasterEvent } from './types/disaster';
import { PhoneCall, ShieldAlert, X } from 'lucide-react';

const getInitialPage = (): NavigationPage => {
  if (typeof window !== 'undefined') {
    // Check URL query param: ?page=...
    const params = new URLSearchParams(window.location.search);
    const pageParam = params.get('page') as NavigationPage;
    const validPages: NavigationPage[] = ['home', 'risk-map', 'disasters', 'get-help', 'help-others', 'how-it-works'];
    if (pageParam && validPages.includes(pageParam)) return pageParam;

    // Check hash: #...
    if (window.location.hash) {
      const hash = window.location.hash.replace('#', '') as NavigationPage;
      if (validPages.includes(hash)) return hash;
    }
  }
  return 'home';
};

export const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<NavigationPage>(getInitialPage);
  const [selectedIncident, setSelectedIncident] = useState<DisasterEvent | null>(null);
  const [showQuickSOS, setShowQuickSOS] = useState<boolean>(false);

  // Sync back/forward browser history and hash changes
  useEffect(() => {
    const handlePopState = () => {
      setCurrentPage(getInitialPage());
    };

    window.addEventListener('popstate', handlePopState);
    window.addEventListener('hashchange', handlePopState);
    return () => {
      window.removeEventListener('popstate', handlePopState);
      window.removeEventListener('hashchange', handlePopState);
    };
  }, []);

  const handleNavigate = (page: NavigationPage) => {
    setCurrentPage(page);
    const newUrl = page === 'home' ? '/' : `?page=${page}`;
    window.history.pushState(null, '', newUrl);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSelectRegionFromHome = (region: RegionRiskData) => {
    handleNavigate('risk-map');
  };

  return (
    <div className="min-h-screen flex flex-col bg-paper-100 text-charcoal-900 font-sans selection:bg-charcoal-900 selection:text-paper-100 overflow-x-hidden">
      {/* Global Minimal Navigation */}
      <Navbar
        currentPage={currentPage}
        onNavigate={handleNavigate}
        onOpenAnalyzeModal={() => {
          if (currentPage !== 'home') {
            handleNavigate('home');
          }
          setTimeout(() => {
            document.getElementById('analyze-section')?.scrollIntoView({ behavior: 'smooth' });
          }, 150);
        }}
      />

      {/* Main Routed Page Content */}
      <div className="flex-1">
        {currentPage === 'home' && (
          <HomePage
            onNavigate={handleNavigate}
            onSelectRegion={handleSelectRegionFromHome}
            onSelectIncident={(incident) => setSelectedIncident(incident)}
          />
        )}

        {currentPage === 'risk-map' && (
          <RiskMapPage
            onSelectIncident={(incident) => setSelectedIncident(incident)}
          />
        )}

        {currentPage === 'disasters' && (
          <DisastersPage
            onSelectIncident={(incident) => setSelectedIncident(incident)}
          />
        )}

        {currentPage === 'get-help' && <GetHelpPage />}

        {currentPage === 'help-others' && <HelpOthersPage />}

        {currentPage === 'how-it-works' && (
          <HowItWorksPage
            onAnalyzeArea={() => {
              handleNavigate('home');
              setTimeout(() => {
                document.getElementById('analyze-section')?.scrollIntoView({ behavior: 'smooth' });
              }, 150);
            }}
            onExploreMap={() => handleNavigate('risk-map')}
          />
        )}
      </div>

      {/* Global Footer */}
      <Footer onNavigate={handleNavigate} />

      {/* Disaster Incident Detail Modal */}
      <DisasterDetailModal
        incident={selectedIncident}
        onClose={() => setSelectedIncident(null)}
        onHelpAction={() => {
          setSelectedIncident(null);
          handleNavigate('help-others');
        }}
      />

      {/* Floating Quick SOS Emergency Dial Button (Bottom Right) */}
      <div className="fixed bottom-6 right-6 z-40">
        {showQuickSOS ? (
          <div className="p-4 rounded-3xl bg-white border border-paper-300 shadow-floating text-xs font-mono w-72 mb-3 animate-in fade-in slide-in-from-bottom-2 duration-200">
            <div className="flex items-center justify-between pb-2 mb-2 border-b border-paper-200">
              <span className="font-bold text-red-600 flex items-center gap-1.5">
                <ShieldAlert className="w-4 h-4" />
                <span>Emergency Helplines</span>
              </span>
              <button
                onClick={() => setShowQuickSOS(false)}
                className="p-1 rounded-lg text-charcoal-400 hover:text-charcoal-700"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </div>
            <div className="space-y-2">
              <a
                href="tel:112"
                className="flex items-center justify-between p-2 rounded-xl bg-red-50 text-red-700 hover:bg-red-100 transition-colors"
              >
                <span>National Emergency</span>
                <strong className="font-bold">112</strong>
              </a>
              <a
                href="tel:1078"
                className="flex items-center justify-between p-2 rounded-xl bg-paper-100 text-charcoal-800 hover:bg-paper-200 transition-colors"
              >
                <span>NDMA Helpline</span>
                <strong className="font-bold">1078</strong>
              </a>
              <a
                href="tel:1070"
                className="flex items-center justify-between p-2 rounded-xl bg-paper-100 text-charcoal-800 hover:bg-paper-200 transition-colors"
              >
                <span>State Relief Control</span>
                <strong className="font-bold">1070</strong>
              </a>
            </div>
          </div>
        ) : null}

        <button
          onClick={() => setShowQuickSOS(!showQuickSOS)}
          className="flex items-center gap-2 px-4 py-3 rounded-full bg-charcoal-900 text-paper-50 shadow-floating hover:bg-charcoal-800 transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-charcoal-900"
          aria-label="Quick Emergency Helplines"
        >
          <PhoneCall className="w-4 h-4 text-rose-400 animate-pulse" />
          <span className="text-xs font-mono font-bold tracking-tight">SOS Lines</span>
        </button>
      </div>
    </div>
  );
};

export default App;
