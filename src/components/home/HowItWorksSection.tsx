import React from 'react';
import { Database, Cpu, Compass, HeartHandshake, HelpCircle, Activity, FileCheck2, AlertTriangle, Clock, ShieldCheck } from 'lucide-react';

export const HowItWorksSection: React.FC = () => {
  const steps = [
    {
      num: '01',
      title: 'DATA',
      subtitle: 'Multi-Stream Signal Ingestion',
      description: 'Ingests real-time precipitation anomalies, riverbed discharge telemetry, seismic wave micro-sensors, topsoil pore pressure, and 30 years of historical Indian meteorological patterns.',
      icon: Database,
      highlight: 'Weather + Sensor + Satellite'
    },
    {
      num: '02',
      title: 'ANALYSIS & ML',
      subtitle: 'Empirical ML & Multi-Source Fusion',
      description: 'Authoritative data streams (IMD NWP, CWC gauges, NDMA/GSI baselines) are fused with RISK // INDIA Flood Model v1 (risk_india_flood_v1), providing nationwide empirical flood intelligence across all 36 States and UTs.',
      icon: Cpu,
      highlight: 'Pan-India Empirical ML & Fusion'
    },
    {
      num: '03',
      title: 'PREPARE',
      subtitle: 'Actionable Citizen Guidance',
      description: 'Transforms dense meteorological telemetry into intuitive hazard scores, plain-language advisory checklists, and personalized family preparedness protocols.',
      icon: Compass,
      highlight: 'Before / During / After'
    },
    {
      num: '04',
      title: 'RESPOND',
      subtitle: 'Verified Mutual Aid & Relief',
      description: 'Connects stranded citizens to open emergency shelters, dispatch coordinators, and verified relief funds, while filtering out unauthorized collections.',
      icon: HeartHandshake,
      highlight: 'Transparent Relief Grid'
    }
  ];

  const citizenQuestions = [
    {
      q: '1. Why is this risk showing?',
      a: 'Scientific telemetry drivers: Rainfall anomalies from IMD, river stage levels from CWC, saturated soil moisture, and active storm tracks determine current and near-term hazard scores.',
      icon: Activity,
      color: 'text-indigo-600 dark:text-indigo-400',
      bg: 'bg-indigo-50/60 dark:bg-indigo-950/20'
    },
    {
      q: '2. What changed?',
      a: 'Dynamic delta tracking: Real-time telemetry refreshes detect shifts in atmospheric pressure, riverbed discharge velocity, and radar nowcasting patterns between monitoring windows.',
      icon: Clock,
      color: 'text-blue-600 dark:text-blue-400',
      bg: 'bg-blue-50/60 dark:bg-blue-950/20'
    },
    {
      q: '3. What evidence supports it?',
      a: 'Multi-source statutory provenance: Every assessment is anchored to verified public data streams (IMD, CWC, NDMA, ISRO NRSC), with zero synthetic or fabricated measurements.',
      icon: FileCheck2,
      color: 'text-emerald-600 dark:text-emerald-400',
      bg: 'bg-emerald-50/60 dark:bg-emerald-950/20'
    },
    {
      q: '4. What could make it worse?',
      a: 'Escalation factors: Upstream reservoir release, persistent cloudbursts, high tidal surges, or sudden dam gate openings can sharply amplify local inundation and risk levels.',
      icon: AlertTriangle,
      color: 'text-amber-600 dark:text-amber-400',
      bg: 'bg-amber-50/60 dark:bg-amber-950/20'
    },
    {
      q: '5. What do we not know?',
      a: 'Scientific uncertainty boundaries: Hyper-local drainage blockages, micro-topography shifts, and earthquake occurrences cannot be predicted. Empirical ML is bounded to flood hazards across Indian river basins; non-flood perils follow statutory operational models.',
      icon: HelpCircle,
      color: 'text-purple-600 dark:text-purple-400',
      bg: 'bg-purple-50/60 dark:bg-purple-950/20'
    },
    {
      q: '6. When should I check again?',
      a: 'Monitoring cadence: Re-check every 3 to 6 hours during active weather or flood advisories, and at least once daily during baseline seasonal conditions.',
      icon: ShieldCheck,
      color: 'text-rose-600 dark:text-rose-400',
      bg: 'bg-rose-50/60 dark:bg-rose-950/20'
    }
  ];

  return (
    <section id="how-it-works" className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-16">
      {/* Header */}
      <div className="text-center max-w-3xl mx-auto">
        <div className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold mb-2">
          System Architecture & Citizen Transparency
        </div>
        <h2 className="text-3xl sm:text-5xl font-bold tracking-tight text-charcoal-950 dark:text-white mb-4">
          How RISK//INDIA Operates.
        </h2>
        <p className="text-sm sm:text-base text-charcoal-600 dark:text-slate-300">
          A transparent intelligence continuum transforming raw planetary signals into community resilience and verified relief.
        </p>
      </div>

      {/* 4-Step Process Timeline */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 relative">
        {steps.map((step) => {
          const IconComponent = step.icon;
          return (
            <div
              key={step.num}
              className="rounded-3xl bg-white dark:bg-slate-900 border border-paper-300 dark:border-slate-800 p-6 sm:p-8 shadow-subtle hover:shadow-elevated hover:border-charcoal-400 transition-all duration-300 flex flex-col justify-between group"
            >
              <div>
                {/* Step Number & Icon */}
                <div className="flex items-center justify-between mb-6">
                  <span className="font-mono text-3xl font-extrabold text-charcoal-300 dark:text-slate-700 group-hover:text-charcoal-900 dark:group-hover:text-white transition-colors">
                    {step.num}
                  </span>
                  <div className="w-10 h-10 rounded-2xl bg-paper-100 dark:bg-slate-800 border border-paper-300 dark:border-slate-700 flex items-center justify-center text-charcoal-800 dark:text-slate-200 group-hover:bg-charcoal-900 group-hover:text-paper-50 transition-colors">
                    <IconComponent className="w-5 h-5" />
                  </div>
                </div>

                {/* Step Titles */}
                <h3 className="text-lg font-bold text-charcoal-950 dark:text-white mb-1">
                  {step.title}
                </h3>
                <div className="text-xs font-mono text-charcoal-500 dark:text-slate-400 mb-4">
                  {step.subtitle}
                </div>

                {/* Description */}
                <p className="text-xs text-charcoal-600 dark:text-slate-300 leading-relaxed">
                  {step.description}
                </p>
              </div>

              {/* Bottom Tag */}
              <div className="mt-8 pt-4 border-t border-paper-200 dark:border-slate-800">
                <span className="inline-flex items-center gap-1 text-[11px] font-mono text-charcoal-500 dark:text-slate-400 bg-paper-50 dark:bg-slate-800/80 px-2.5 py-1 rounded-md border border-paper-200 dark:border-slate-700">
                  {step.highlight}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* 6 Plain-Language Citizen Explanation Questions */}
      <div className="rounded-3xl border border-paper-300 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 p-6 sm:p-8 backdrop-blur-sm space-y-6">
        <div className="max-w-3xl">
          <div className="inline-flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-indigo-600 dark:text-indigo-400 mb-1">
            <HelpCircle className="w-4 h-4" />
            <span>CITIZEN INTELLIGENCE EXPLAINABILITY</span>
          </div>
          <h3 className="text-xl sm:text-3xl font-extrabold text-charcoal-950 dark:text-white">
            6 Plain-Language Questions Every Citizen Should Ask
          </h3>
          <p className="text-xs sm:text-sm text-charcoal-600 dark:text-slate-300 mt-1">
            We hold our forecasting systems to strict scientific standards and complete public transparency.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {citizenQuestions.map((item, idx) => {
            const Icon = item.icon;
            return (
              <div
                key={idx}
                className={`p-4 rounded-2xl border border-paper-200 dark:border-slate-800 ${item.bg} space-y-2 flex flex-col justify-between`}
              >
                <div className="space-y-1.5">
                  <div className="flex items-center gap-2">
                    <Icon className={`w-4 h-4 ${item.color} shrink-0`} />
                    <h4 className="font-bold text-xs sm:text-sm text-charcoal-900 dark:text-white">
                      {item.q}
                    </h4>
                  </div>
                  <p className="text-xs text-charcoal-600 dark:text-slate-300 leading-relaxed font-normal">
                    {item.a}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
