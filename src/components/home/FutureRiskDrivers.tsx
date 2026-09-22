import React from 'react';
import { Layers, AlertCircle, TrendingDown, HelpCircle, CheckCircle2, ShieldCheck, Radio } from 'lucide-react';
import { EvidenceSignal } from '../../types/predictiveRisk';

interface FutureRiskDriversProps {
  regionName?: string;
  hazardName?: string;
  explanation?: {
    why_this_risk?: string;
    what_changed?: string;
    what_supports_it?: string[];
    what_could_make_it_worse?: string;
    what_could_make_it_improve?: string;
    what_we_do_not_know?: string;
  };
  evidenceSignals?: EvidenceSignal[];
}

export const FutureRiskDrivers: React.FC<FutureRiskDriversProps> = ({
  regionName = 'National Multi-Hazard Outlook',
  hazardName = 'Multi-Hazard',
  explanation,
  evidenceSignals = []
}) => {
  const defaultDrivers = [
    'Upper catchment precipitation accumulation exceeding 5-day moving average (IMD Automatic Weather Station network)',
    'Upstream river gauge levels crossing designated warning thresholds at major hydrological monitoring stations (CWC)',
    'Soil saturation index approaching field capacity, reducing ground infiltration buffering potential (NRSC Earth Observation)',
    'Synoptic low-pressure circulation system sustaining persistent moisture influx from adjacent marine basins'
  ];

  const driversList = explanation?.what_supports_it && explanation.what_supports_it.length > 0
    ? explanation.what_supports_it
    : defaultDrivers;

  return (
    <section id="risk-drivers" className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto scroll-mt-24">
      <div className="rounded-3xl border border-paper-300 bg-white dark:bg-slate-900 p-6 sm:p-8 shadow-md space-y-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-4 border-b border-paper-200 dark:border-slate-800">
          <div>
            <div className="inline-flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
              <Layers className="w-4 h-4" />
              <span>CAUSAL EVIDENCE & UNCERTAINTY BOUNDARIES</span>
            </div>
            <h3 className="text-xl sm:text-2xl font-bold text-charcoal-950 dark:text-white mt-0.5">
              Why Is This Risk Projected? // {regionName}
            </h3>
            <p className="text-xs text-charcoal-600 dark:text-slate-400 mt-0.5">
              Transparent attribution to statutory data providers and physical telemetry observations.
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs font-mono text-charcoal-500 dark:text-slate-400">
            <Radio className="w-3.5 h-3.5 text-emerald-600 animate-pulse" />
            <span>Official Feeds: IMD • CWC • NDMA • NRSC</span>
          </div>
        </div>

        {/* Causal Explanation Main Narrative */}
        <div className="p-4 rounded-2xl bg-paper-50 dark:bg-slate-800/60 border border-paper-200 dark:border-slate-700">
          <span className="text-[10px] font-mono uppercase tracking-wider text-charcoal-500 dark:text-slate-400 font-bold block mb-1">
            CORE PHYSICAL MECHANISM
          </span>
          <p className="text-xs sm:text-sm text-charcoal-800 dark:text-slate-200 leading-relaxed font-sans">
            {explanation?.why_this_risk ||
              'Fused meteorological and hydrological indicators indicate that heavy antecedent precipitation over upper catchments will route downstream through the active river basin within the next 24 to 72 hours.'}
          </p>
        </div>

        {/* 3 Columns: Supporting Evidence, Escalation Triggers, Improvement Factors */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Supporting Evidence Signals */}
          <div className="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-3">
            <div className="flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-indigo-700 dark:text-indigo-400">
              <ShieldCheck className="w-4 h-4" />
              <span>Observable Telemetry Signals</span>
            </div>
            <ul className="space-y-2 text-xs text-charcoal-700 dark:text-slate-300 font-mono text-[11px]">
              {driversList.map((driver, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 shrink-0 mt-1.5" />
                  <span>{driver}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Escalation Factors (What Could Make It Worse) */}
          <div className="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-amber-200 dark:border-amber-900/60 space-y-3">
            <div className="flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-amber-700 dark:text-amber-400">
              <AlertCircle className="w-4 h-4 text-amber-600" />
              <span>What Could Make It Worse</span>
            </div>
            <p className="text-xs text-charcoal-700 dark:text-slate-300 leading-relaxed">
              {explanation?.what_could_make_it_worse ||
                'Consecutive high-intensity cloudburst events exceeding 65 mm/hr, unplanned reservoir emergency spillway discharge, or blockage of regional stormwater drainage outfalls.'}
            </p>
            <div className="pt-2 border-t border-paper-200 dark:border-slate-700 text-[11px] font-mono text-charcoal-500">
              Watch for: Sudden gauge spikes & Red advisory upgrades from IMD.
            </div>
          </div>

          {/* Improvement Factors (What Could Make It Improve) */}
          <div className="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-emerald-200 dark:border-emerald-900/60 space-y-3">
            <div className="flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-emerald-700 dark:text-emerald-400">
              <TrendingDown className="w-4 h-4 text-emerald-600" />
              <span>What Could Make It Improve</span>
            </div>
            <p className="text-xs text-charcoal-700 dark:text-slate-300 leading-relaxed">
              {explanation?.what_could_make_it_improve ||
                'Rapid eastward displacement of the monsoon trough, cessation of continuous rainfall, and natural drainage absorption as river discharges subside below danger marks.'}
            </p>
            <div className="pt-2 border-t border-paper-200 dark:border-slate-700 text-[11px] font-mono text-emerald-600 dark:text-emerald-400">
              Conditions transition to Green alert upon gauge stabilization.
            </div>
          </div>
        </div>

        {/* Data Gaps & Scientific Limitations Banner */}
        <div className="p-4 rounded-2xl bg-paper-100 dark:bg-slate-800/60 border border-paper-300 dark:border-slate-700 flex items-start gap-3">
          <HelpCircle className="w-5 h-5 text-charcoal-500 shrink-0 mt-0.5" />
          <div className="text-xs space-y-1">
            <span className="font-mono font-bold uppercase tracking-wider text-charcoal-700 dark:text-slate-300 block">
              DATA GAPS & UNCERTAINTY BOUNDARIES
            </span>
            <p className="text-charcoal-600 dark:text-slate-400 leading-relaxed">
              {explanation?.what_we_do_not_know ||
                'Micro-locality urban drainage blockages, individual basement pump operational status, and localized slope failure thresholds cannot be monitored in real time without in-situ IoT telemetry. Never make life safety decisions on predictions alone; always heed statutory SDMA orders.'}
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};
