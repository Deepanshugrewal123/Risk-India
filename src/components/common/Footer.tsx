import React from 'react';
import { Shield, ExternalLink, Heart, AlertCircle } from 'lucide-react';
import { NavigationPage } from './Navbar';
import { DemoBadge } from './DemoBadge';

interface FooterProps {
  onNavigate: (page: NavigationPage) => void;
}

export const Footer: React.FC<FooterProps> = ({ onNavigate }) => {
  return (
    <footer className="bg-paper-200/50 border-t border-paper-300 pt-16 pb-12 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Top Disclaimer Banner */}
        <div className="mb-12 p-4 rounded-2xl bg-white border border-paper-300 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-subtle">
          <div className="flex items-start gap-3">
            <div className="p-2 rounded-lg bg-amber-50 text-amber-700 mt-0.5">
              <AlertCircle className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-semibold uppercase tracking-wider text-charcoal-900">
                  Disaster Risk Intelligence System
                </span>
                <DemoBadge label="ACADEMIC RESEARCH PROTOTYPE" />
              </div>
              <p className="text-xs text-charcoal-600 mt-0.5">
                RISK // INDIA integrates real-world disaster telemetry from USGS and official disaster bulletins, alongside an audited machine learning flood prototype for Assam river gauges. In an actual emergency, always follow official directives from NDMA and district authorities.
              </p>
            </div>
          </div>
          <div className="shrink-0 flex items-center gap-2">
            <span className="text-xs font-mono text-charcoal-500">In real emergency:</span>
            <span className="px-2.5 py-1 rounded-full bg-charcoal-900 text-paper-50 font-mono text-xs font-bold">
              Call 112 / 1070
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-10 pb-12 border-b border-paper-300">
          {/* Col 1 & 2: Brand and Philosophy */}
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-lg bg-charcoal-900 text-paper-50 flex items-center justify-center font-mono font-bold text-xs">
                <Shield className="w-3.5 h-3.5 text-paper-50" />
              </div>
              <span className="font-mono font-bold tracking-tight text-sm text-charcoal-950">
                RISK<span className="text-charcoal-400">//</span>INDIA
              </span>
            </div>
            <p className="text-xs text-charcoal-600 leading-relaxed max-w-sm">
              An AI-powered disaster intelligence and public safety platform prototype. Fostering proactive hazard forecasting, rapid citizen preparedness, and transparent relief coordination across India.
            </p>
            <div className="pt-2">
              <div className="text-[11px] font-mono uppercase tracking-wider text-charcoal-400 mb-1">
                Core Philosophy
              </div>
              <div className="inline-flex items-center gap-2 text-xs font-mono font-medium text-charcoal-800 bg-white px-3 py-1.5 rounded-lg border border-paper-300">
                <span>PREDICT</span>
                <span className="text-charcoal-300">→</span>
                <span>PREPARE</span>
                <span className="text-charcoal-300">→</span>
                <span>RESPOND</span>
                <span className="text-charcoal-300">→</span>
                <span>HELP</span>
              </div>
            </div>
          </div>

          {/* Col 3: Navigation */}
          <div className="space-y-3">
            <div className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold">
              Platform
            </div>
            <ul className="space-y-2 text-xs text-charcoal-600">
              <li>
                <button
                  onClick={() => { onNavigate('home'); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
                  className="hover:text-charcoal-950 transition-colors"
                >
                  Overview & Snapshot
                </button>
              </li>
              <li>
                <button
                  onClick={() => { onNavigate('risk-map'); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
                  className="hover:text-charcoal-950 transition-colors"
                >
                  Interactive Risk Map
                </button>
              </li>
              <li>
                <button
                  onClick={() => { onNavigate('disasters'); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
                  className="hover:text-charcoal-950 transition-colors"
                >
                  Live Monitored Disasters
                </button>
              </li>
              <li>
                <button
                  onClick={() => { onNavigate('how-it-works'); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
                  className="hover:text-charcoal-950 transition-colors"
                >
                  System Architecture & AI
                </button>
              </li>
            </ul>
          </div>

          {/* Col 4: Relief Hub */}
          <div className="space-y-3">
            <div className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold">
              Relief Ecosystem
            </div>
            <ul className="space-y-2 text-xs text-charcoal-600">
              <li>
                <button
                  onClick={() => { onNavigate('get-help'); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
                  className="hover:text-charcoal-950 transition-colors"
                >
                  I Need Help (Emergency)
                </button>
              </li>
              <li>
                <button
                  onClick={() => { onNavigate('help-others'); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
                  className="hover:text-charcoal-950 transition-colors"
                >
                  I Want To Help (Pledges)
                </button>
              </li>
              <li>
                <span className="text-charcoal-400">Emergency Shelter Network</span>
              </li>
              <li>
                <span className="text-charcoal-400">Verified NGO Audit Framework</span>
              </li>
            </ul>
          </div>

          {/* Col 5: Verified Portals */}
          <div className="space-y-3">
            <div className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold">
              Official Portals
            </div>
            <ul className="space-y-2 text-xs text-charcoal-600">
              <li>
                <a
                  href="https://ndma.gov.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 hover:text-charcoal-950 transition-colors"
                >
                  NDMA India <ExternalLink className="w-3 h-3 opacity-60" />
                </a>
              </li>
              <li>
                <a
                  href="https://mausam.imd.gov.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 hover:text-charcoal-950 transition-colors"
                >
                  IMD Weather <ExternalLink className="w-3 h-3 opacity-60" />
                </a>
              </li>
              <li>
                <a
                  href="https://ndrf.gov.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 hover:text-charcoal-950 transition-colors"
                >
                  NDRF Force <ExternalLink className="w-3 h-3 opacity-60" />
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom copyright */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-charcoal-500">
          <div className="flex items-center gap-1">
            <span>Designed for Public Safety Intelligence</span>
            <span className="mx-1.5">•</span>
            <span className="font-mono">RISK//INDIA 2026</span>
          </div>
          <div className="flex items-center gap-1">
            <span>Built with calm, human-centered motion & physics</span>
            <Heart className="w-3.5 h-3.5 text-charcoal-400 fill-charcoal-400 ml-1" />
          </div>
        </div>
      </div>
    </footer>
  );
};
