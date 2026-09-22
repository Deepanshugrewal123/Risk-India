import React, { useState } from 'react';
import { PredictiveScenario, ScenarioType } from '../../types/predictiveRisk';
import { UncertaintyBadge } from './UncertaintyBadge';
import { RiskTrendIndicator } from './RiskTrendIndicator';
import { Compass, ShieldAlert, CheckCircle2, ChevronRight } from 'lucide-react';

interface ScenarioPanelProps {
  scenarios: PredictiveScenario[];
}

export const ScenarioPanel: React.FC<ScenarioPanelProps> = ({ scenarios }) => {
  const [activeTab, setActiveTab] = useState<ScenarioType>('LIKELY');

  if (!scenarios || scenarios.length === 0) {
    return null;
  }

  const activeScenario =
    scenarios.find((s) => s.scenario_type === activeTab) || scenarios[0];

  const getTabColor = (type: ScenarioType) => {
    switch (type) {
      case 'ESCALATION':
        return activeTab === 'ESCALATION'
          ? 'bg-rose-600 text-white'
          : 'text-rose-600 dark:text-rose-400 hover:bg-rose-500/10';
      case 'LIKELY':
        return activeTab === 'LIKELY'
          ? 'bg-indigo-600 text-white'
          : 'text-indigo-600 dark:text-indigo-400 hover:bg-indigo-500/10';
      case 'BASELINE':
      default:
        return activeTab === 'BASELINE'
          ? 'bg-slate-700 dark:bg-slate-300 text-white dark:text-slate-900'
          : 'text-slate-600 dark:text-slate-400 hover:bg-slate-500/10';
    }
  };

  return (
    <div className="space-y-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 shadow-sm">
      <div className="flex items-center justify-between flex-wrap gap-2 pb-2 border-b border-slate-100 dark:border-slate-800">
        <div className="flex items-center gap-2">
          <Compass className="w-4 h-4 text-indigo-500" />
          <h4 className="text-sm font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100">
            Forward Predictive Scenarios
          </h4>
        </div>
        <div className="flex items-center gap-1.5 p-1 rounded-lg bg-slate-100 dark:bg-slate-800 text-xs">
          {scenarios.map((sc) => (
            <button
              key={sc.scenario_type}
              onClick={() => setActiveTab(sc.scenario_type)}
              className={`px-3 py-1 rounded-md font-semibold text-xs transition-colors ${getTabColor(
                sc.scenario_type
              )}`}
            >
              {sc.scenario_type}
            </button>
          ))}
        </div>
      </div>

      {activeScenario && (
        <div className="space-y-3.5">
          <div className="flex items-start justify-between flex-wrap gap-2">
            <div>
              <span className="text-xs font-mono font-bold uppercase text-indigo-600 dark:text-indigo-400">
                Scenario: {activeScenario.scenario_type}
              </span>
              <h5 className="text-base font-bold text-slate-900 dark:text-slate-100 mt-0.5">
                {activeScenario.title}
              </h5>
            </div>
            <div className="flex items-center gap-2 flex-wrap">
              <RiskTrendIndicator trend={activeScenario.expected_direction} size="sm" />
              <UncertaintyBadge uncertainty={activeScenario.uncertainty} showLabels={true} />
            </div>
          </div>

          <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
            {activeScenario.description}
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs pt-1">
            <div className="space-y-1.5 p-3 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/60 dark:border-slate-700/60">
              <span className="font-semibold text-slate-700 dark:text-slate-300 block">
                Triggering Factors & Evidence:
              </span>
              <ul className="space-y-1">
                {activeScenario.triggering_evidence.map((trig, i) => (
                  <li key={i} className="flex items-start gap-1.5 text-slate-600 dark:text-slate-400">
                    <ChevronRight className="w-3.5 h-3.5 text-indigo-500 shrink-0 mt-0.5" />
                    <span>{trig}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="space-y-1.5 p-3 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/60 dark:border-slate-700/60">
              <span className="font-semibold text-slate-700 dark:text-slate-300 block">
                Preparedness Implications:
              </span>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed mb-2">
                {activeScenario.preparedness_implications}
              </p>
              <div className="space-y-1">
                {activeScenario.safety_actions.slice(0, 2).map((act, i) => (
                  <div key={i} className="flex items-start gap-1.5 text-slate-700 dark:text-slate-300">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" />
                    <span>{act}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ScenarioPanel;
