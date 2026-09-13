import React, { useState, useEffect } from 'react';
import { Menu, X, Shield, ArrowUpRight } from 'lucide-react';
import { MagneticButton } from './MagneticButton';

export type NavigationPage = 
  | 'home'
  | 'risk-map'
  | 'disasters'
  | 'get-help'
  | 'help-others'
  | 'how-it-works';

interface NavbarProps {
  currentPage: NavigationPage;
  onNavigate: (page: NavigationPage) => void;
  onOpenAnalyzeModal?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentPage,
  onNavigate,
  onOpenAnalyzeModal,
}) => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 24);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks: { id: NavigationPage; label: string }[] = [
    { id: 'home', label: 'Home' },
    { id: 'risk-map', label: 'Risk Map' },
    { id: 'disasters', label: 'Live Disasters' },
    { id: 'get-help', label: 'Get Help' },
    { id: 'help-others', label: 'Help Others' },
    { id: 'how-it-works', label: 'How It Works' },
  ];

  const handleLinkClick = (id: NavigationPage) => {
    onNavigate(id);
    setMobileMenuOpen(false);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled
          ? 'py-3 bg-paper-50/85 backdrop-blur-md border-b border-paper-300/80 shadow-subtle'
          : 'py-5 bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          {/* Logo & Identity */}
          <button
            onClick={() => handleLinkClick('home')}
            className="flex items-center gap-2.5 group focus:outline-none focus-visible:ring-2 focus-visible:ring-charcoal-900 rounded-lg p-1"
          >
            <div className="w-8 h-8 rounded-lg bg-charcoal-900 text-paper-50 flex items-center justify-center font-mono font-bold text-sm shadow-sm group-hover:bg-charcoal-800 transition-colors">
              <Shield className="w-4 h-4 text-paper-50" />
            </div>
            <div className="flex flex-col text-left">
              <span className="font-mono font-bold tracking-tight text-sm text-charcoal-950 flex items-center gap-1">
                RISK<span className="text-charcoal-400">//</span>INDIA
              </span>
              <span className="text-[10px] uppercase tracking-wider text-charcoal-500 font-mono -mt-0.5">
                Disaster Intelligence
              </span>
            </div>
          </button>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center gap-1 bg-paper-200/60 p-1 rounded-full border border-paper-300/70 backdrop-blur-sm">
            {navLinks.map((link) => {
              const isActive = currentPage === link.id;
              return (
                <button
                  key={link.id}
                  onClick={() => handleLinkClick(link.id)}
                  className={`px-3.5 py-1.5 rounded-full text-xs font-medium transition-all duration-200 ${
                    isActive
                      ? 'bg-white text-charcoal-950 shadow-subtle border border-paper-300/80'
                      : 'text-charcoal-600 hover:text-charcoal-950 hover:bg-white/40'
                  }`}
                >
                  {link.label}
                </button>
              );
            })}
          </nav>

          {/* Right Action */}
          <div className="hidden md:flex items-center gap-3">
            <MagneticButton
              size="sm"
              variant="primary"
              onClick={() => {
                if (onOpenAnalyzeModal) {
                  onOpenAnalyzeModal();
                } else {
                  handleLinkClick('home');
                  setTimeout(() => {
                    const el = document.getElementById('analyze-section');
                    el?.scrollIntoView({ behavior: 'smooth' });
                  }, 100);
                }
              }}
              className="gap-1.5"
            >
              <span>Analyze Area</span>
              <ArrowUpRight className="w-3.5 h-3.5 opacity-70" />
            </MagneticButton>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden min-w-[44px] min-h-[44px] p-2 rounded-lg text-charcoal-700 hover:bg-paper-200/80 flex items-center justify-center transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-charcoal-900"
            aria-label="Toggle navigation menu"
            aria-expanded={mobileMenuOpen}
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-paper-50/98 backdrop-blur-lg border-b border-paper-300 px-4 pt-3 pb-6 space-y-2 shadow-elevated animate-in fade-in slide-in-from-top-2 duration-200">
          <div className="flex flex-col space-y-1">
            {navLinks.map((link) => {
              const isActive = currentPage === link.id;
              return (
                <button
                  key={link.id}
                  onClick={() => handleLinkClick(link.id)}
                  className={`w-full min-h-[44px] text-left px-4 py-2.5 rounded-xl text-sm font-medium flex items-center transition-colors ${
                    isActive
                      ? 'bg-paper-200 text-charcoal-950 font-bold border border-paper-300/80 shadow-subtle'
                      : 'text-charcoal-700 hover:bg-paper-100/90 active:bg-paper-200'
                  }`}
                >
                  {link.label}
                </button>
              );
            })}
          </div>
          <div className="pt-3 border-t border-paper-200/80">
            <button
              onClick={() => {
                setMobileMenuOpen(false);
                if (onOpenAnalyzeModal) {
                  onOpenAnalyzeModal();
                } else {
                  handleLinkClick('home');
                  setTimeout(() => {
                    document.getElementById('analyze-section')?.scrollIntoView({ behavior: 'smooth' });
                  }, 100);
                }
              }}
              className="w-full min-h-[44px] py-2.5 px-4 rounded-xl bg-charcoal-900 text-paper-50 text-sm font-semibold flex items-center justify-center gap-2 shadow-sm hover:bg-charcoal-800 transition-colors"
            >
              <span>Analyze Area Risk</span>
              <ArrowUpRight className="w-4 h-4 opacity-80" />
            </button>
          </div>
        </div>
      )}
    </header>
  );
};
