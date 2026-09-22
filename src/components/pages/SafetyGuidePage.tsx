import React, { useState, useEffect, useMemo } from 'react';
import {
  BookOpen,
  Search,
  Filter,
  ShieldCheck,
  Flame,
  HeartHandshake,
  PhoneCall,
  AlertTriangle,
  Layers,
  GitBranch,
  RotateCcw,
  CheckCircle2,
  X,
  ArrowRight
} from 'lucide-react';
import { SafetyPhase, SafetyPriority, SafetyInstructionItem } from '../../types/safetyGuide';
import { EXTENDED_SAFETY_ITEMS } from '../../data/extendedSafetyData';
import { SafetyActionItemCard } from '../safety/SafetyActionItemCard';
import { NavigationPage } from '../common/Navbar';

interface SafetyGuidePageProps {
  onNavigate?: (page: NavigationPage) => void;
  initialHazard?: string;
}

const HAZARD_OPTIONS = [
  { id: 'FLOOD', label: 'Flood', icon: '🌊' },
  { id: 'CYCLONE', label: 'Cyclone', icon: '🌀' },
  { id: 'EARTHQUAKE', label: 'Earthquake', icon: '⚡' },
  { id: 'HEATWAVE', label: 'Heatwave', icon: '☀️' },
  { id: 'LANDSLIDE', label: 'Landslide', icon: '⛰️' },
  { id: 'SEVERE_WEATHER', label: 'Severe Weather', icon: '⛈️' }
];

export const SafetyGuidePage: React.FC<SafetyGuidePageProps> = ({
  onNavigate,
  initialHazard = 'FLOOD'
}) => {
  const [selectedHazard, setSelectedHazard] = useState<string>(initialHazard);
  const [selectedPhase, setSelectedPhase] = useState<SafetyPhase | 'ALL'>('ALL');
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [completedItems, setCompletedItems] = useState<Record<string, boolean>>({});

  // Sync initial hazard from props or query string
  useEffect(() => {
    if (initialHazard) {
      setSelectedHazard(initialHazard.toUpperCase().trim());
    }
  }, [initialHazard]);

  // Extract items for selected hazard
  const hazardItems = useMemo(() => {
    return EXTENDED_SAFETY_ITEMS.filter((i) => i.hazard === selectedHazard);
  }, [selectedHazard]);

  // Categories available for selected hazard
  const availableCategories = useMemo(() => {
    return Array.from(new Set(hazardItems.map((i) => i.category)));
  }, [hazardItems]);

  // Filtered items without ANY artificial slicing
  const filteredItems = useMemo(() => {
    return hazardItems.filter((item) => {
      const matchPhase = selectedPhase === 'ALL' || item.phase === selectedPhase;
      const matchCategory = selectedCategory === 'ALL' || item.category === selectedCategory;
      const q = searchQuery.toLowerCase().trim();
      const matchSearch =
        q === '' ||
        item.title.toLowerCase().includes(q) ||
        item.instruction.toLowerCase().includes(q) ||
        item.reason.toLowerCase().includes(q) ||
        (item.practical_steps && item.practical_steps.some((s) => s.toLowerCase().includes(q))) ||
        (item.warning && item.warning.toLowerCase().includes(q));

      return matchPhase && matchCategory && matchSearch;
    });
  }, [hazardItems, selectedPhase, selectedCategory, searchQuery]);

  const toggleItemComplete = (id: string) => {
    setCompletedItems((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const completedCountForHazard = hazardItems.filter((i) => completedItems[i.id]).length;
  const totalCountForHazard = hazardItems.length;

  return (
    <main className="py-10 sm:py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-8 animate-in fade-in duration-200">
      {/* 1. Header & Breadcrumb */}
      <div className="space-y-4">
        <div className="flex items-center gap-2 text-xs font-mono text-charcoal-500 dark:text-slate-400">
          <button
            onClick={() => onNavigate && onNavigate('home')}
            className="hover:underline hover:text-charcoal-800 dark:hover:text-slate-200"
          >
            Home
          </button>
          <span>/</span>
          <span className="text-charcoal-900 dark:text-slate-100 font-bold">Complete Safety Guide</span>
        </div>

        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-6 border-b border-paper-300 dark:border-slate-800">
          <div className="max-w-3xl space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-300 text-xs font-mono uppercase tracking-wider font-bold">
              <BookOpen className="w-3.5 h-3.5" />
              <span>NATIONAL CITIZEN SAFETY KNOWLEDGE BASE // NDMA SOP</span>
            </div>
            <h1 className="text-3xl sm:text-5xl font-black text-charcoal-950 dark:text-white tracking-tight">
              Complete Citizen Disaster Safety Guide
            </h1>
            <p className="text-sm sm:text-base text-charcoal-600 dark:text-slate-300 leading-relaxed">
              Comprehensive Before, During, and After life-safety action protocols across all 6 national hazards. 
              Designed with progressive disclosure: concise summaries upfront, deep practical steps and warning signs on demand.
            </p>
          </div>

          {/* Quick Helplines Box */}
          <div className="p-4 rounded-2xl bg-paper-50 dark:bg-slate-850 border border-paper-300 dark:border-slate-800 shrink-0 space-y-2">
            <div className="text-[11px] font-mono uppercase font-bold text-charcoal-600 dark:text-slate-400 flex items-center gap-1.5">
              <PhoneCall className="w-3.5 h-3.5 text-rose-600 dark:text-rose-400" />
              <span>24/7 Verified Emergency Numbers</span>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              <a
                href="tel:112"
                className="min-h-[44px] px-3.5 py-2 rounded-xl bg-rose-600 text-white font-mono text-xs font-bold hover:bg-rose-700 transition-colors flex items-center gap-1.5 shadow-sm"
              >
                <span>112 (National Emergency)</span>
              </a>
              <a
                href="tel:1078"
                className="min-h-[44px] px-3.5 py-2 rounded-xl bg-white dark:bg-slate-800 text-charcoal-800 dark:text-slate-200 font-mono text-xs font-bold border border-paper-300 dark:border-slate-700 hover:bg-paper-100 dark:hover:bg-slate-700 transition-colors flex items-center gap-1.5"
              >
                <span>1078 (NDMA)</span>
              </a>
              <a
                href="tel:1070"
                className="min-h-[44px] px-3.5 py-2 rounded-xl bg-white dark:bg-slate-800 text-charcoal-800 dark:text-slate-200 font-mono text-xs font-bold border border-paper-300 dark:border-slate-700 hover:bg-paper-100 dark:hover:bg-slate-700 transition-colors flex items-center gap-1.5"
              >
                <span>1070 (State EOC)</span>
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* 2. Statutory Distinction Callout */}
      <div className="p-4 sm:p-5 rounded-2xl bg-amber-50/90 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-900 text-amber-950 dark:text-amber-200 text-xs sm:text-sm flex items-start gap-3.5">
        <AlertTriangle className="w-5 h-5 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <strong className="font-mono uppercase tracking-wider text-[11px] block">
            Statutory Framework Notice // Preparation vs Evacuation
          </strong>
          <p className="leading-relaxed">
            <strong>Preparation actions</strong> can and should be executed independently by households at any time. 
            <strong> Mandatory evacuation directives</strong> are statutory orders issued exclusively by civil authorities 
            (District Magistrate / DDMA / SDMA / NDRF under DM Act 2005). Never delay evacuation once an official order is declared.
          </p>
        </div>
      </div>

      {/* 3. First-Class Cascading Risk Discovery Banner */}
      <div className="p-5 rounded-3xl bg-indigo-50/70 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-900 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-start gap-3">
          <div className="w-10 h-10 rounded-2xl bg-indigo-600 text-white flex items-center justify-center shrink-0 shadow-sm mt-0.5">
            <GitBranch className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-indigo-950 dark:text-indigo-200">
              One Hazard Triggers Secondary Consequences
            </h2>
            <p className="text-xs sm:text-sm text-indigo-900/80 dark:text-indigo-300/80 mt-0.5">
              Disasters rarely strike in isolation. Explore the 4-stage causal consequence chain for {selectedHazard.toLowerCase()}.
            </p>
          </div>
        </div>

        <button
          onClick={() => onNavigate && onNavigate('cascading-risk')}
          className="min-h-[44px] px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-mono text-xs font-bold transition-all shadow-sm flex items-center justify-center gap-2 shrink-0 self-start sm:self-center"
        >
          <span>EXPLORE CASCADING RISK</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

      {/* 4. Hazard Selection Tabs */}
      <div className="space-y-2">
        <label className="text-[11px] font-mono font-bold uppercase tracking-wider text-charcoal-500 dark:text-slate-400 block">
          SELECT DISASTER HAZARD:
        </label>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5">
          {HAZARD_OPTIONS.map((h) => {
            const isSelected = selectedHazard === h.id;
            const count = EXTENDED_SAFETY_ITEMS.filter((i) => i.hazard === h.id).length;
            return (
              <button
                key={h.id}
                onClick={() => {
                  setSelectedHazard(h.id);
                  setSelectedCategory('ALL');
                }}
                className={`min-h-[52px] p-3 rounded-2xl border text-left transition-all flex items-center justify-between gap-2 focus:outline-none focus-visible:ring-2 focus-visible:ring-emerald-600 ${
                  isSelected
                    ? 'bg-charcoal-950 dark:bg-white text-white dark:text-charcoal-950 border-charcoal-950 dark:border-white shadow-md font-bold'
                    : 'bg-white dark:bg-slate-900 text-charcoal-800 dark:text-slate-200 border-paper-300 dark:border-slate-800 hover:border-paper-400 dark:hover:border-slate-700'
                }`}
              >
                <div className="flex items-center gap-2 min-w-0">
                  <span className="text-lg">{h.icon}</span>
                  <span className="text-xs font-semibold truncate">{h.label}</span>
                </div>
                <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded-full ${
                  isSelected ? 'bg-white/20 dark:bg-black/20 text-white dark:text-charcoal-950' : 'bg-paper-100 dark:bg-slate-800 text-charcoal-500'
                }`}>
                  {count}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* 5. Phase & Category Controls + Search */}
      <div className="rounded-3xl bg-white dark:bg-slate-900 border border-paper-300 dark:border-slate-800 p-5 sm:p-6 space-y-4 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          {/* Phase Filter Tabs */}
          <div className="flex flex-wrap items-center gap-2">
            {(['ALL', 'BEFORE', 'DURING', 'AFTER'] as const).map((phase) => {
              const isSelected = selectedPhase === phase;
              return (
                <button
                  key={phase}
                  onClick={() => setSelectedPhase(phase)}
                  className={`min-h-[44px] px-4 py-2 rounded-xl text-xs font-mono font-bold uppercase transition-all flex items-center gap-1.5 ${
                    isSelected
                      ? 'bg-emerald-600 text-white shadow-sm'
                      : 'bg-paper-100 dark:bg-slate-800 text-charcoal-700 dark:text-slate-300 hover:bg-paper-200 dark:hover:bg-slate-700'
                  }`}
                >
                  {phase === 'BEFORE' && <ShieldCheck className="w-3.5 h-3.5" />}
                  {phase === 'DURING' && <Flame className="w-3.5 h-3.5 text-amber-400" />}
                  {phase === 'AFTER' && <HeartHandshake className="w-3.5 h-3.5 text-teal-300" />}
                  <span>{phase === 'ALL' ? 'ALL PHASES' : phase}</span>
                </button>
              );
            })}
          </div>

          {/* Checklist Progress Indicator */}
          <div className="flex items-center gap-2.5 text-xs font-mono text-charcoal-600 dark:text-slate-400">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            <span>Preparedness: <strong>{completedCountForHazard}</strong> / {totalCountForHazard} Actions Checked</span>
          </div>
        </div>

        {/* Search & Category Filter Row */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 pt-3 border-t border-paper-200 dark:border-slate-800">
          {/* Search Input */}
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-charcoal-400 dark:text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search safety actions (e.g., 'drinking water', 'LPG gas', 'CPR', 'livestock')..."
              className="w-full min-h-[44px] pl-10 pr-10 py-2.5 rounded-xl bg-paper-50 dark:bg-slate-800 border border-paper-300 dark:border-slate-700 text-xs sm:text-sm text-charcoal-900 dark:text-white placeholder:text-charcoal-400 dark:placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-600"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="w-8 h-8 rounded-lg hover:bg-paper-200 dark:hover:bg-slate-700 flex items-center justify-center text-charcoal-500 absolute right-2 top-1/2 -translate-y-1/2"
                aria-label="Clear search"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

          {/* Category Dropdown */}
          <div className="flex items-center gap-2 shrink-0">
            <Filter className="w-4 h-4 text-charcoal-400 dark:text-slate-500" />
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="min-h-[44px] px-3 py-2 rounded-xl bg-paper-50 dark:bg-slate-800 border border-paper-300 dark:border-slate-700 text-xs font-mono font-semibold text-charcoal-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-emerald-600"
            >
              <option value="ALL">All Categories ({availableCategories.length})</option>
              {availableCategories.map((c) => (
                <option key={c} value={c}>
                  {c.replace(/_/g, ' ')}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* 6. Active Actions Grid (Zero 4-Item Limit) */}
      <div className="space-y-4">
        <div className="flex items-center justify-between text-xs font-mono text-charcoal-500 dark:text-slate-400">
          <span>
            SHOWING <strong>{filteredItems.length}</strong> ACTION PROTOCOLS FOR {selectedHazard}
          </span>
          {searchQuery && (
            <span>Filtered by keyword: &quot;{searchQuery}&quot;</span>
          )}
        </div>

        {filteredItems.length === 0 ? (
          <div className="text-center py-16 px-4 rounded-3xl bg-white dark:bg-slate-900 border border-paper-300 dark:border-slate-800 space-y-3">
            <BookOpen className="w-10 h-10 text-charcoal-300 dark:text-slate-600 mx-auto" />
            <h3 className="text-lg font-bold text-charcoal-800 dark:text-slate-200">
              No matching safety protocols found
            </h3>
            <p className="text-xs sm:text-sm text-charcoal-500 dark:text-slate-400 max-w-md mx-auto">
              Try clearing your search query or selecting &quot;ALL PHASES&quot; to explore the complete catalog.
            </p>
            <button
              onClick={() => {
                setSearchQuery('');
                setSelectedPhase('ALL');
                setSelectedCategory('ALL');
              }}
              className="min-h-[44px] px-4 py-2 rounded-xl bg-charcoal-900 text-white font-mono text-xs font-bold hover:bg-charcoal-800 transition-colors"
            >
              Reset Filters
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredItems.map((item) => (
              <SafetyActionItemCard
                key={item.id}
                item={item}
                isCompleted={!!completedItems[item.id]}
                onToggleComplete={toggleItemComplete}
              />
            ))}
          </div>
        )}
      </div>
    </main>
  );
};
