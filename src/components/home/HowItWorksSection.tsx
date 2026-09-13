import React from 'react';
import { Database, Cpu, Compass, HeartHandshake, ArrowRight, ArrowDown } from 'lucide-react';

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
      title: 'AI ANALYSIS',
      subtitle: 'Predictive Risk Estimation',
      description: 'Machine learning heuristics process compound risk factors to forecast probability, impact footprint, and vulnerable district clusters 24 to 72 hours in advance.',
      icon: Cpu,
      highlight: 'Spatial ML Risk Engine'
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

  return (
    <section id="how-it-works" className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div className="text-center max-w-3xl mx-auto mb-16">
        <div className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold mb-2">
          System Architecture & Pipelines
        </div>
        <h2 className="text-3xl sm:text-5xl font-bold tracking-tight text-charcoal-950 mb-4">
          How RISK//INDIA Operates.
        </h2>
        <p className="text-sm sm:text-base text-charcoal-600">
          A seamless intelligence continuum transforming raw planetary signals into community resilience and verified relief.
        </p>
      </div>

      {/* 4-Step Process Timeline */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 relative">
        {steps.map((step, index) => {
          const IconComponent = step.icon;
          return (
            <div
              key={step.num}
              className="rounded-3xl bg-white border border-paper-300 p-6 sm:p-8 shadow-subtle hover:shadow-elevated hover:border-charcoal-400 transition-all duration-300 flex flex-col justify-between group"
            >
              <div>
                {/* Step Number & Icon */}
                <div className="flex items-center justify-between mb-6">
                  <span className="font-mono text-3xl font-extrabold text-charcoal-300 group-hover:text-charcoal-900 transition-colors">
                    {step.num}
                  </span>
                  <div className="w-10 h-10 rounded-2xl bg-paper-100 border border-paper-300 flex items-center justify-center text-charcoal-800 group-hover:bg-charcoal-900 group-hover:text-paper-50 transition-colors">
                    <IconComponent className="w-5 h-5" />
                  </div>
                </div>

                {/* Step Titles */}
                <h3 className="text-lg font-bold text-charcoal-950 mb-1">
                  {step.title}
                </h3>
                <div className="text-xs font-mono text-charcoal-500 mb-4">
                  {step.subtitle}
                </div>

                {/* Description */}
                <p className="text-xs text-charcoal-600 leading-relaxed">
                  {step.description}
                </p>
              </div>

              {/* Bottom Tag */}
              <div className="mt-8 pt-4 border-t border-paper-200">
                <span className="inline-flex items-center gap-1 text-[11px] font-mono text-charcoal-500 bg-paper-50 px-2.5 py-1 rounded-md border border-paper-200">
                  {step.highlight}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};
