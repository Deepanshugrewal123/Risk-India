import React, { useState, useEffect } from 'react';
import { CrisisProvider, useCrisis } from './context/CrisisContext';
import { Navbar, NavigationPage } from './components/common/Navbar';
import { Footer } from './components/common/Footer';
import { OfflineIndicator } from './components/common/OfflineIndicator';
import { HomePage } from './components/pages/HomePage';
import { FutureRiskPage } from './components/pages/FutureRiskPage';
import { CascadingRiskPage } from './components/pages/CascadingRiskPage';
import { SafetyGuidePage } from './components/pages/SafetyGuidePage';
import { RiskMapPage } from './components/pages/RiskMapPage';
import { DisastersPage } from './components/pages/DisastersPage';
import { GetHelpPage } from './components/pages/GetHelpPage';
import { HelpOthersPage } from './components/pages/HelpOthersPage';
import { HowItWorksPage } from './components/pages/HowItWorksPage';
import { DisasterDetailModal } from './components/modals/DisasterDetailModal';
import { EmergencyAccessHub } from './components/emergency/EmergencyAccessHub';
import { disasterService } from './services/disasterService';
import { RegionRiskData } from './types/risk';
import { DisasterEvent } from './types/disaster';
import { CrisisDashboard, CrisisRecommendedBanner } from './components/crisis';
import { PhoneCall, ShieldAlert, X } from 'lucide-react';

const getInitialPage = (): NavigationPage => {
  if (typeof window !== 'undefined') {
    // 1. Check URL pathname: /risk-map, /future-risk, etc.
    const pathname = window.location.pathname.replace(/^\/+|\/+$/g, '').toLowerCase();
    if (pathname === 'risk-map' || pathname === 'map') return 'risk-map';
    if (pathname === 'future-risk' || pathname === 'future' || pathname === 'predictive') return 'future-risk';
    if (pathname === 'cascading-risk' || pathname === 'cascading') return 'cascading-risk';
    if (pathname === 'safety-guide' || pathname === 'safety' || pathname === 'guide') return 'safety-guide';
    if (pathname === 'disasters' || pathname === 'incidents') return 'disasters';
    if (pathname === 'get-help' || pathname === 'help') return 'get-help';
    if (pathname === 'help-others' || pathname === 'volunteer') return 'help-others';
    if (pathname === 'how-it-works' || pathname === 'about') return 'how-it-works';

    // 2. Check URL query param: ?page=... or ?view=...
    const params = new URLSearchParams(window.location.search);
    const pageParam = params.get('page') || params.get('view');
    
    if (pageParam === 'future-risk' || pageParam === 'future' || pageParam === 'predictive') return 'future-risk';
    if (pageParam === 'cascading-risk' || pageParam === 'cascading') return 'cascading-risk';
    if (pageParam === 'safety-guide' || pageParam === 'safety' || pageParam === 'guide') return 'safety-guide';
    if (pageParam === 'map' || pageParam === 'risk-map') return 'risk-map';
    if (pageParam === 'disasters' || pageParam === 'incidents') return 'disasters';
    if (pageParam === 'get-help' || pageParam === 'help') return 'get-help';
    if (pageParam === 'help-others' || pageParam === 'volunteer') return 'help-others';
    if (pageParam === 'how-it-works' || pageParam === 'about') return 'how-it-works';

    // 3. Check hash: #...
    if (window.location.hash) {
      const hash = window.location.hash.replace('#', '') as NavigationPage;
      const validPages: NavigationPage[] = ['home', 'future-risk', 'cascading-risk', 'safety-guide', 'risk-map', 'disasters', 'get-help', 'help-others', 'how-it-works'];
      if (validPages.includes(hash)) return hash;
    }
  }
  return 'home';
};

export const AppContent: React.FC = () => {
  const { isCrisisMode } = useCrisis();
  const [currentPage, setCurrentPage] = useState<NavigationPage>(getInitialPage);
  const [selectedIncident, setSelectedIncident] = useState<DisasterEvent | null>(null);
  const [showEmergencyHub, setShowEmergencyHub] = useState<boolean>(() => {
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      return params.get('emergency') === 'true' || params.get('sos') === 'true';
    }
    return false;
  });
  const [showQuickSOS, setShowQuickSOS] = useState<boolean>(false);

  const [safetyGuideHazard, setSafetyGuideHazard] = useState<string>(() => {
    if (typeof window !== 'undefined') {
      const p = new URLSearchParams(window.location.search).get('hazard');
      if (p) return p.toUpperCase().trim();
    }
    return 'FLOOD';
  });
  const [safetyGuideCategory, setSafetyGuideCategory] = useState<string>(() => {
    if (typeof window !== 'undefined') {
      const p = new URLSearchParams(window.location.search).get('category');
      if (p) return p.trim();
    }
    return 'ALL';
  });
  const [cascadingHazard, setCascadingHazard] = useState<string>(() => {
    if (typeof window !== 'undefined') {
      const p = new URLSearchParams(window.location.search).get('hazard');
      if (p) return p.toUpperCase().trim();
    }
    return 'FLOOD';
  });
  const [cascadingRegionId, setCascadingRegionId] = useState<string>(() => {
    if (typeof window !== 'undefined') {
      const p = new URLSearchParams(window.location.search).get('region');
      if (p) return p.toLowerCase().trim();
    }
    return 'assam';
  });

  // Sync back/forward browser history and query parameters
  useEffect(() => {
    const handlePopState = () => {
      setCurrentPage(getInitialPage());
      if (typeof window !== 'undefined') {
        const params = new URLSearchParams(window.location.search);
        const h = params.get('hazard');
        if (h) {
          setSafetyGuideHazard(h.toUpperCase().trim());
          setCascadingHazard(h.toUpperCase().trim());
        }
        const c = params.get('category');
        if (c) setSafetyGuideCategory(c);
        const r = params.get('region');
        if (r) setCascadingRegionId(r);
      }
    };

    window.addEventListener('popstate', handlePopState);
    window.addEventListener('hashchange', handlePopState);
    return () => {
      window.removeEventListener('popstate', handlePopState);
      window.removeEventListener('hashchange', handlePopState);
    };
  }, []);

  // Handle deep-linked incident (?incident=<id>)
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      const incidentId = params.get('incident');
      if (incidentId) {
        disasterService.getActiveDisasters().then((list) => {
          const found = list.find((inc) => inc.id === incidentId || inc.id.includes(incidentId));
          if (found) {
            setSelectedIncident(found);
          }
        }).catch(() => {});
      }
    }
  }, []);

  const handleNavigate = (
    page: NavigationPage,
    context?: { hazard?: string; category?: string; regionId?: string; phase?: string }
  ) => {
    setCurrentPage(page);
    if (context?.hazard) {
      setSafetyGuideHazard(context.hazard.toUpperCase().trim());
      setCascadingHazard(context.hazard.toUpperCase().trim());
    }
    if (context?.category) {
      setSafetyGuideCategory(context.category);
    }
    if (context?.regionId) {
      setCascadingRegionId(context.regionId);
    }

    const params = new URLSearchParams();
    if (page !== 'home') params.set('page', page);
    if (context?.hazard) params.set('hazard', context.hazard);
    if (context?.category) params.set('category', context.category);
    if (context?.regionId) params.set('region', context.regionId);
    if (context?.phase) params.set('phase', context.phase);

    const queryString = params.toString();
    const basePath = page === 'home' ? '/' : `/${page}`;
    const newUrl = queryString ? `${basePath}?${queryString}` : basePath;
    window.history.pushState(null, '', newUrl);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSelectRegionFromHome = (region: RegionRiskData) => {
    handleNavigate('risk-map');
  };

  return (
    <div className="min-h-screen flex flex-col bg-paper-100 text-charcoal-900 font-sans selection:bg-charcoal-900 selection:text-paper-100 overflow-x-hidden">
      {/* Offline Connectivity Indicator */}
      <OfflineIndicator onOpenEmergencyHub={() => setShowEmergencyHub(true)} />

      {/* Global Minimal Navigation */}
      <Navbar
        currentPage={currentPage}
        onNavigate={handleNavigate}
        onOpenEmergencyHub={() => setShowEmergencyHub(true)}
        onOpenAnalyzeModal={() => {
          if (currentPage !== 'home') {
            handleNavigate('home');
          }
          setTimeout(() => {
            document.getElementById('analyze-section')?.scrollIntoView({ behavior: 'smooth' });
          }, 150);
        }}
      />

      {/* Crisis Mode Recommended Advisory Banner */}
      {!isCrisisMode && (
        <div className="pt-16 sm:pt-20">
          <CrisisRecommendedBanner />
        </div>
      )}

      {/* Main Routed Page Content or Dedicated Crisis Dashboard */}
      <div className="flex-1">
        {isCrisisMode ? (
          <CrisisDashboard />
        ) : (
          <>
            {currentPage === 'home' && (
              <HomePage
                onNavigate={handleNavigate}
                onSelectRegion={handleSelectRegionFromHome}
                onSelectIncident={(incident) => setSelectedIncident(incident)}
              />
            )}

            {currentPage === 'future-risk' && (
              <FutureRiskPage
                onNavigate={handleNavigate}
              />
            )}

            {currentPage === 'cascading-risk' && (
              <CascadingRiskPage
                onNavigate={handleNavigate}
                initialRegionId={cascadingRegionId}
                initialHazard={cascadingHazard}
              />
            )}

            {currentPage === 'safety-guide' && (
              <SafetyGuidePage
                onNavigate={handleNavigate}
                initialHazard={safetyGuideHazard}
                initialCategory={safetyGuideCategory}
              />
            )}

            {currentPage === 'risk-map' && (
              <RiskMapPage
                onSelectIncident={(incident) => setSelectedIncident(incident)}
                onNavigate={handleNavigate}
              />
            )}

            {currentPage === 'disasters' && (
              <DisastersPage
                onSelectIncident={(incident) => setSelectedIncident(incident)}
                onNavigate={handleNavigate}
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
          </>
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

      {/* Emergency Access Hub Modal (Offline-ready speed dial & safety protocols) */}
      <EmergencyAccessHub
        isOpen={showEmergencyHub}
        onClose={() => setShowEmergencyHub(false)}
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

            <div className="mt-2.5 pt-2 border-t border-paper-200">
              <button
                onClick={() => {
                  setShowQuickSOS(false);
                  setShowEmergencyHub(true);
                }}
                className="w-full py-1.5 px-2.5 rounded-lg bg-charcoal-900 hover:bg-charcoal-800 text-white font-mono text-[11px] font-bold text-center transition-colors"
              >
                Open Full Emergency Hub →
              </button>
            </div>
          </div>
        ) : null}

        <button
          onClick={() => setShowEmergencyHub(true)}
          className="flex items-center gap-2 px-4 py-3 rounded-full bg-rose-600 text-white shadow-floating hover:bg-rose-700 transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-rose-500 font-bold"
          aria-label="Quick Emergency Helplines & Protocols"
          title="Open Emergency Helpline Directory (112, 1078, 1070) & Offline Safety Guides"
        >
          <PhoneCall className="w-4 h-4 text-white animate-pulse" />
          <span className="text-xs font-mono font-bold tracking-tight">SOS Lines</span>
        </button>
      </div>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <CrisisProvider>
      <AppContent />
    </CrisisProvider>
  );
};

export default App;
