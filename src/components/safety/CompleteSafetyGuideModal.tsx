import React, { useState, useEffect } from 'react';
import {
  X,
  ShieldCheck,
  Search,
  CheckSquare,
  Square,
  AlertTriangle,
  AlertOctagon,
  PhoneCall,
  Flame,
  Clock,
  HeartHandshake,
  Package,
  Layers,
  Filter,
  FileCheck2,
  ExternalLink,
  BookOpen
} from 'lucide-react';
import { SafetyPhase, SafetyPriority, SafetyCategory, SafetyInstructionItem } from '../../types/safetyGuide';
import { EXTENDED_SAFETY_ITEMS } from '../../data/extendedSafetyData';

interface CompleteSafetyGuideModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialHazard?: string;
}

const ALL_HAZARDS = [
  { id: 'FLOOD', label: 'Flood' },
  { id: 'CYCLONE', label: 'Cyclone' },
  { id: 'EARTHQUAKE', label: 'Earthquake' },
  { id: 'HEATWAVE', label: 'Heatwave' },
  { id: 'LANDSLIDE', label: 'Landslide' },
  { id: 'SEVERE_WEATHER', label: 'Severe Weather' }
];

export const CompleteSafetyGuideModal: React.FC<CompleteSafetyGuideModalProps> = ({
  isOpen,
  onClose,
  initialHazard = 'FLOOD'
}) => {
  const [selectedHazard, setSelectedHazard] = useState<string>(initialHazard);
  const [selectedPhase, setSelectedPhase] = useState<SafetyPhase | 'ALL'>('ALL');
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [checkedItems, setCheckedItems] = useState<Record<string, boolean>>({});

  // Sync initial hazard when opened
  useEffect(() => {
    if (initialHazard) {
      setSelectedHazard(initialHazard.toUpperCase().trim());
    }
  }, [initialHazard, isOpen]);

  // Handle escape key to close
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    if (isOpen) {
      window.addEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'hidden';
    }
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  // Filter instructions
  const hazardItems = EXTENDED_SAFETY_ITEMS.filter((item) => item.hazard === selectedHazard);

  const availableCategories = Array.from(new Set(hazardItems.map((i) => i.category)));

  const filteredItems = hazardItems.filter((item) => {
    const matchPhase = selectedPhase === 'ALL' || item.phase === selectedPhase;
    const matchCategory = selectedCategory === 'ALL' || item.category === selectedCategory;
    const matchSearch =
      searchQuery.trim() === '' ||
      item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.instruction.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.reason.toLowerCase().includes(searchQuery.toLowerCase());
    return matchPhase && matchCategory && matchSearch;
  });

  const toggleCheck = (id: string) => {
    setCheckedItems((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const getPriorityBadge = (priority: SafetyPriority) => {
    switch (priority) {
      case 'CRITICAL':
        return 'bg-rose-100 dark:bg-rose-950/60 text-rose-800 dark:text-rose-300 border-rose-300 dark:border-rose-800';
      case 'HIGH':
        return 'bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 border-amber-300 dark:border-amber-800';
      case 'RECOMMENDED':
      default:
        return 'bg-blue-100 dark:bg-blue-950/60 text-blue-800 dark:text-blue-300 border-blue-300 dark:border-blue-800';
    }
  };

  const getPhaseColor = (phase: SafetyPhase) => {
    switch (phase) {
      case 'BEFORE':
        return 'text-charcoal-900 bg-paper-200 dark:bg-slate-700';
      case 'DURING':
        return 'text-amber-900 bg-amber-100 dark:bg-amber-950/70';
      case 'AFTER':
        return 'text-teal-900 bg-teal-100 dark:bg-teal-950/70';
    }
  };

  const completedForHazard = hazardItems.filter((i) => checkedItems[i.id]).length;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-charcoal-950/80 backdrop-blur-sm animate-in fade-in duration-200"
      role="dialog"
      aria-modal="true"
      aria-labelledby="safety-guide-title"
    >
      <div
        className="bg-white dark:bg-slate-900 border border-paper-300 dark:border-slate-700 rounded-3xl shadow-2xl max-w-5xl w-full max-h-[92vh] flex flex-col overflow-hidden text-charcoal-900 dark:text-slate-100"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header */}
        <div className="p-5 sm:p-6 border-b border-paper-200 dark:border-slate-800 flex items-center justify-between gap-4 bg-paper-50/80 dark:bg-slate-850">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-emerald-600 text-white flex items-center justify-center shrink-0 shadow-sm">
              <BookOpen className="w-5 h-5" />
            </div>
            <div>
              <div className="text-[11px] font-mono uppercase tracking-wider text-emerald-700 dark:text-emerald-400 font-bold">
                COMPREHENSIVE NDMA CITIZEN DIRECTORY
              </div>
              <h2 id="safety-guide-title" className="text-xl sm:text-2xl font-black tracking-tight">
                Complete Citizen Disaster Safety Guide
              </h2>
            </div>
          </div>

          <button
            onClick={onClose}
            className="w-11 h-11 rounded-2xl border border-paper-300 dark:border-slate-700 hover:bg-paper-100 dark:hover:bg-slate-800 flex items-center justify-center text-charcoal-600 dark:text-slate-400 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-emerald-600 shrink-0"
            aria-label="Close safety guide modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Statutory Legal Demarcation Alert */}
        <div className="px-6 py-3 bg-amber-50 dark:bg-amber-950/40 border-b border-amber-200 dark:border-amber-900/60 text-amber-950 dark:text-amber-200 text-xs flex items-center gap-2.5">
          <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
          <p className="leading-tight">
            <strong>Operational Boundary:</strong> Household preparation can be executed independently at any time.
            <strong> Mandatory evacuation orders</strong> are issued exclusively by civil authorities (District Magistrate / SDMA / NDRF).
          </p>
        </div>

        {/* Hazard Selector Ribbon */}
        <div className="px-6 pt-4 pb-2 border-b border-paper-200 dark:border-slate-800 flex items-center gap-2 overflow-x-auto">
          {ALL_HAZARDS.map((h) => (
            <button
              key={h.id}
              onClick={() => {
                setSelectedHazard(h.id);
                setSelectedCategory('ALL');
              }}
              className={`min-h-[44px] px-4 py-2 rounded-xl text-xs sm:text-sm font-mono font-bold transition-all shrink-0 border ${
                selectedHazard === h.id
                  ? 'bg-charcoal-950 text-white dark:bg-white dark:text-charcoal-950 border-charcoal-950 dark:border-white shadow-xs'
                  : 'bg-paper-50 dark:bg-slate-800 text-charcoal-700 dark:text-slate-300 border-paper-200 dark:border-slate-700 hover:bg-paper-100'
              }`}
            >
              {h.label}
            </button>
          ))}
        </div>

        {/* Phase Tabs & Search Filter Controls */}
        <div className="p-4 sm:px-6 border-b border-paper-200 dark:border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-paper-50/40 dark:bg-slate-850/40">
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
            {[
              { id: 'ALL', label: 'All Lifecycle Phases' },
              { id: 'BEFORE', label: '1. Before (Prepare)' },
              { id: 'DURING', label: '2. During (Survive)' },
              { id: 'AFTER', label: '3. After (Recover)' }
            ].map((p) => (
              <button
                key={p.id}
                onClick={() => setSelectedPhase(p.id as any)}
                className={`min-h-[44px] px-3 py-1.5 rounded-lg text-xs font-bold transition-all shrink-0 border ${
                  selectedPhase === p.id
                    ? 'bg-emerald-600 text-white border-emerald-600 shadow-xs'
                    : 'bg-white dark:bg-slate-800 text-charcoal-700 dark:text-slate-300 border-paper-200 dark:border-slate-700 hover:bg-paper-100'
                }`}
              >
                {p.label}
              </button>
            ))}
          </div>

          {/* Search bar */}
          <div className="relative min-w-[220px]">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-charcoal-400" />
            <input
              type="text"
              placeholder="Search instructions..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-paper-300 dark:border-slate-700 bg-white dark:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-600"
            />
          </div>
        </div>

        {/* Category Pills */}
        <div className="px-6 py-2.5 border-b border-paper-200 dark:border-slate-800 flex items-center gap-1.5 overflow-x-auto text-[11px] font-mono">
          <span className="text-charcoal-400 dark:text-slate-500 mr-1 flex items-center gap-1">
            <Filter className="w-3 h-3" />
            Filter:
          </span>
          <button
            onClick={() => setSelectedCategory('ALL')}
            className={`min-h-[36px] px-2.5 py-1 rounded-md transition-colors ${
              selectedCategory === 'ALL'
                ? 'bg-charcoal-800 text-white dark:bg-slate-200 dark:text-charcoal-900 font-bold'
                : 'bg-paper-100 dark:bg-slate-800 text-charcoal-600 dark:text-slate-400 hover:bg-paper-200'
            }`}
          >
            All Categories ({hazardItems.length})
          </button>
          {availableCategories.map((cat) => {
            const count = hazardItems.filter((i) => i.category === cat).length;
            return (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`min-h-[36px] px-2.5 py-1 rounded-md transition-colors shrink-0 ${
                  selectedCategory === cat
                    ? 'bg-charcoal-800 text-white dark:bg-slate-200 dark:text-charcoal-900 font-bold'
                    : 'bg-paper-100 dark:bg-slate-800 text-charcoal-600 dark:text-slate-400 hover:bg-paper-200'
                }`}
              >
                {cat.replace(/_/g, ' ')} ({count})
              </button>
            );
          })}
        </div>

        {/* Scrollable Instruction Cards List */}
        <div className="flex-1 overflow-y-auto p-5 sm:p-6 space-y-4">
          {filteredItems.length === 0 ? (
            <div className="py-12 text-center text-charcoal-500 dark:text-slate-400 text-xs font-mono">
              No safety instructions match your selected filter criteria.
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between text-xs font-mono text-charcoal-500 dark:text-slate-400 pb-1">
                <span>Showing {filteredItems.length} actionable protocols</span>
                <span>
                  Tracked: <strong>{completedForHazard}</strong> / {hazardItems.length}
                </span>
              </div>

              {filteredItems.map((item) => {
                const isChecked = !!checkedItems[item.id];

                return (
                  <div
                    key={item.id}
                    className={`p-5 rounded-2xl border transition-all ${
                      isChecked
                        ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-300 dark:border-emerald-800'
                        : 'bg-white dark:bg-slate-850 border-paper-200 dark:border-slate-800 shadow-xs'
                    }`}
                  >
                    {/* Item Top Bar */}
                    <div className="flex flex-wrap items-center justify-between gap-2 pb-2 mb-2 border-b border-paper-100 dark:border-slate-800">
                      <div className="flex items-center gap-2">
                        <span
                          className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold uppercase tracking-wider ${getPhaseColor(
                            item.phase
                          )}`}
                        >
                          {item.phase}
                        </span>
                        <span className="text-[10px] font-mono text-charcoal-400 dark:text-slate-500 uppercase">
                          {item.category.replace(/_/g, ' ')}
                        </span>
                      </div>

                      <div className="flex items-center gap-2">
                        <span
                          className={`text-[10px] font-mono px-2 py-0.5 rounded-full border font-bold uppercase ${getPriorityBadge(
                            item.priority
                          )}`}
                        >
                          {item.priority}
                        </span>
                        <button
                          onClick={() => toggleCheck(item.id)}
                          className="min-h-[44px] min-w-[44px] -my-2 -mr-2 px-2 flex items-center justify-center text-charcoal-600 dark:text-slate-400 hover:text-emerald-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-emerald-600 rounded-lg"
                          aria-label={isChecked ? `Mark ${item.title} as incomplete` : `Mark ${item.title} as completed`}
                        >
                          {isChecked ? (
                            <CheckSquare className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
                          ) : (
                            <Square className="w-5 h-5" />
                          )}
                        </button>
                      </div>
                    </div>

                    {/* Title & Instruction */}
                    <div className="space-y-1.5">
                      <h3
                        className={`text-base font-bold ${
                          isChecked ? 'line-through text-charcoal-500 dark:text-slate-400' : 'text-charcoal-950 dark:text-white'
                        }`}
                      >
                        {item.title}
                      </h3>
                      <p className="text-xs sm:text-sm text-charcoal-700 dark:text-slate-300 leading-relaxed">
                        {item.instruction}
                      </p>
                    </div>

                    {/* Scientific Rationale */}
                    <div className="mt-3 p-3 rounded-xl bg-paper-50 dark:bg-slate-800/60 border border-paper-200 dark:border-slate-800 text-xs text-charcoal-600 dark:text-slate-400 space-y-1">
                      <div className="font-mono text-[10px] uppercase font-bold text-charcoal-500 dark:text-slate-400">
                        Scientific / Medical Rationale:
                      </div>
                      <p className="leading-relaxed">{item.reason}</p>
                    </div>

                    {/* Warning Box if present */}
                    {item.warning && (
                      <div className="mt-2.5 p-2.5 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900 text-rose-900 dark:text-rose-200 text-xs flex items-start gap-2">
                        <AlertOctagon className="w-4 h-4 text-rose-600 dark:text-rose-400 shrink-0 mt-0.5" />
                        <div>
                          <strong>What NOT To Do: </strong>
                          <span>{item.warning}</span>
                        </div>
                      </div>
                    )}

                    {/* Related Cascading Secondary Risk */}
                    {item.related_cascading_risk && (
                      <div className="mt-2 text-[11px] font-mono text-indigo-700 dark:text-indigo-400 flex items-center gap-1.5">
                        <span className="font-bold">→ Related Cascading Secondary Hazard:</span>
                        <span>{item.related_cascading_risk}</span>
                      </div>
                    )}

                    {/* Source Citation */}
                    <div className="mt-2 text-[10px] font-mono text-charcoal-400 dark:text-slate-500">
                      Authoritative Standard: {item.source}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Modal Bottom Emergency Bar */}
        <div className="p-4 sm:p-5 border-t border-paper-200 dark:border-slate-800 bg-charcoal-950 text-white flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="text-xs">
            <span className="font-mono text-rose-400 uppercase font-bold block">
              Official 24/7 Life Threat Helplines:
            </span>
            <span className="text-charcoal-300">Free call from any landline or mobile, even without balance.</span>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <a
              href="tel:112"
              className="min-h-[44px] px-3.5 py-2 rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-mono text-xs font-bold flex items-center gap-1.5 transition-colors"
            >
              <PhoneCall className="w-3.5 h-3.5" />
              <span>112 (National Emergency)</span>
            </a>
            <a
              href="tel:1078"
              className="min-h-[44px] px-3.5 py-2 rounded-xl bg-charcoal-800 hover:bg-charcoal-700 text-white font-mono text-xs font-bold flex items-center gap-1.5 transition-colors border border-charcoal-700"
            >
              <span>1078 (NDMA)</span>
            </a>
            <a
              href="tel:108"
              className="min-h-[44px] px-3.5 py-2 rounded-xl bg-charcoal-800 hover:bg-charcoal-700 text-white font-mono text-xs font-bold flex items-center gap-1.5 transition-colors border border-charcoal-700"
            >
              <span>108 (Ambulance)</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CompleteSafetyGuideModal;
