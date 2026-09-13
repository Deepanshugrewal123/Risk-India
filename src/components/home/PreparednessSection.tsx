import React, { useState, useEffect } from 'react';
import { preparednessService, PreparednessGuide } from '../../services/preparednessService';
import { Waves, Mountain, Wind, Activity, Sun, CheckCircle, ShieldAlert, ArrowRight } from 'lucide-react';

export const PreparednessSection: React.FC = () => {
  const [guides, setGuides] = useState<PreparednessGuide[]>([]);
  const [selectedDisaster, setSelectedDisaster] = useState<string>('Flood');
  const [activePhase, setActivePhase] = useState<'Before' | 'During' | 'After'>('Before');

  useEffect(() => {
    preparednessService.getGuides().then((data) => {
      setGuides(data);
    });
  }, []);

  const currentGuide = guides.find((g) => g.disaster === selectedDisaster) || guides[0] || {
    disaster: 'Flood',
    iconName: 'Waves',
    tagline: 'Rapid inundation precautions',
    overview: 'Flood safety guidelines',
    phases: [{ phase: 'Before' as const, title: 'Preparation', instructions: [] }]
  };
  const currentPhaseData = currentGuide.phases.find((p) => p.phase === activePhase) || currentGuide.phases[0] || {
    phase: 'Before' as const,
    title: 'Preparation',
    instructions: []
  };

  const getHazardIcon = (name: string) => {
    switch (name) {
      case 'Flood':
        return <Waves className="w-4 h-4" />;
      case 'Landslide':
        return <Mountain className="w-4 h-4" />;
      case 'Cyclone':
        return <Wind className="w-4 h-4" />;
      case 'Earthquake':
        return <Activity className="w-4 h-4" />;
      case 'Heatwave':
      default:
        return <Sun className="w-4 h-4" />;
    }
  };

  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div className="max-w-3xl mb-12">
        <div className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold mb-2">
          Citizen Preparedness Protocols
        </div>
        <h2 className="text-3xl sm:text-5xl font-bold tracking-tight text-charcoal-950">
          Prepare Before It Happens.
        </h2>
        <p className="text-sm sm:text-base text-charcoal-600 mt-3">
          Concise, actionable lifecycle guidelines developed for Indian families, residential societies, and village panchayats.
        </p>
      </div>

      {/* Hazard Selector Pills */}
      <div className="flex flex-wrap items-center gap-2 mb-8">
        {guides.map((guide) => {
          const isSelected = selectedDisaster === guide.disaster;
          return (
            <button
              key={guide.disaster}
              onClick={() => setSelectedDisaster(guide.disaster)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-full text-xs font-medium transition-all ${
                isSelected
                  ? 'bg-charcoal-900 text-paper-50 shadow-sm'
                  : 'bg-white text-charcoal-700 border border-paper-300 hover:bg-paper-50'
              }`}
            >
              {getHazardIcon(guide.disaster)}
              <span>{guide.disaster}</span>
            </button>
          );
        })}
      </div>

      {/* Main Preparedness Card with Before / During / After Tabs */}
      <div className="rounded-3xl bg-white border border-paper-300 shadow-floating overflow-hidden">
        {/* Top Hazard Summary Bar */}
        <div className="p-6 sm:p-8 bg-paper-50/80 border-b border-paper-200 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="font-mono text-xs uppercase tracking-wider text-charcoal-500 font-bold">
                Safety Playbook
              </span>
              <span className="text-charcoal-300">•</span>
              <span className="text-xs font-semibold text-charcoal-900">{currentGuide.disaster} Protocol</span>
            </div>
            <p className="text-sm text-charcoal-700 italic">
              "{currentGuide.tagline}"
            </p>
          </div>

          {/* Phase Segmented Buttons: BEFORE, DURING, AFTER */}
          <div className="flex items-center gap-1 bg-paper-200/80 p-1 rounded-2xl border border-paper-300/80 self-start md:self-auto">
            {(['Before', 'During', 'After'] as const).map((phase) => (
              <button
                key={phase}
                onClick={() => setActivePhase(phase)}
                className={`px-4 py-2 rounded-xl text-xs font-mono font-bold uppercase tracking-wider transition-all ${
                  activePhase === phase
                    ? 'bg-white text-charcoal-950 shadow-subtle border border-paper-300'
                    : 'text-charcoal-600 hover:text-charcoal-900'
                }`}
              >
                {phase}
              </button>
            ))}
          </div>
        </div>

        {/* Phase Action Details */}
        <div className="p-6 sm:p-10 space-y-8">
          {/* Critical Highlight Banner */}
          {currentPhaseData.criticalItem && (
            <div className="p-4 rounded-2xl bg-paper-100 border border-paper-300 flex items-start gap-3">
              <div className="p-1.5 rounded-lg bg-charcoal-900 text-paper-50 shrink-0 mt-0.5">
                <ShieldAlert className="w-4 h-4" />
              </div>
              <div>
                <span className="text-[10px] font-mono uppercase tracking-wider text-charcoal-500 font-bold block">
                  Non-Negotiable Rule // {activePhase.toUpperCase()}
                </span>
                <span className="text-xs sm:text-sm font-semibold text-charcoal-900">
                  {currentPhaseData.criticalItem}
                </span>
              </div>
            </div>
          )}

          {/* Checklist of steps */}
          <div>
            <h4 className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold mb-4">
              Action Steps ({activePhase.toUpperCase()})
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {currentPhaseData.instructions.map((step, index) => (
                <div
                  key={index}
                  className="p-4 rounded-2xl bg-paper-50/70 border border-paper-200 flex items-start gap-3"
                >
                  <div className="w-6 h-6 rounded-full bg-white border border-paper-300 flex items-center justify-center font-mono text-xs font-bold text-charcoal-700 shrink-0 mt-0.5">
                    0{index + 1}
                  </div>
                  <p className="text-xs sm:text-sm text-charcoal-800 leading-relaxed">
                    {step}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
