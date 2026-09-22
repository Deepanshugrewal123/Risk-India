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
          ? 'bg-rose-600 text-white shadow-2xs'
          : 'text-rose-700 hover:bg-rose-50';
      case 'LIKELY':
        return activeTab === 'LIKELY'
          ? 'bg-blue-700 text-white shadow-2xs'
          : 'text-blue-700 hover:bg-blue-50';
      case 'BASELINE':
      default:
        return activeTab === 'BASELINE'
          ? 'bg-slate-900 text-white shadow-2xs'
          : 'text-slate-700 hover:bg-slate-200';
    }
  };

  return (
    <div className="space-y-4 rounded-2xl border border-slate-200 bg-white p-4 sm:p-5 shadow-xs">
      <div className="flex items-center justify-between flex-wrap gap-2 pb-2 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <Compass className="w-4 h-4 text-blue-700" />
          <h4 className="text-sm font-bold uppercase tracking-wider text-slate-900">
            Forward Predictive Scenarios
          </h4>
        </div>
        <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-100 text-xs">
          {scenarios.map((sc) => (
            <button
              key={sc.scenario_type}
              onClick={() => setActiveTab(sc.scenario_type)}
              className={`px-3 py-1 rounded-lg font-bold text-xs transition-colors ${getTabColor(
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
              <span className="text-xs font-mono font-bold uppercase text-blue-700">
                Scenario: {activeScenario.scenario_type}
              </span>
              <h5 className="text-base font-bold text-slate-900 mt-0.5">
                {activeScenario.title}
              </h5>
            </div>
            <div className="flex items-center gap-2 flex-wrap">
              <RiskTrendIndicator trend={activeScenario.expected_direction} size="sm" />
              <UncertaintyBadge uncertainty={activeScenario.uncertainty} showLabels={true} />
            </div>
          </div>

          <p className="text-xs text-slate-600 leading-relaxed font-normal">
            {activeScenario.description}
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs pt-1">
            <div className="space-y-1.5 p-3.5 rounded-xl bg-slate-50 border border-slate-200">
              <span className="font-semibold text-slate-800 block">
                Triggering Factors & Evidence:
              </span>
              <ul className="space-y-1">
                {activeScenario.triggering_evidence.map((trig, i) => (
                  <li key={i} className="flex items-start gap-1.5 text-slate-600">
                    <ChevronRight className="w-3.5 h-3.5 text-blue-600 shrink-0 mt-0.5" />
                    <span>{trig}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="space-y-1.5 p-3.5 rounded-xl bg-slate-50 border border-slate-200">
              <span className="font-semibold text-slate-800 block">
                Preparedness Implications:
              </span>
              <p className="text-slate-600 leading-relaxed mb-2 font-normal">
                {activeScenario.preparedness_implications}
              </p>
              <div className="space-y-1">
                {activeScenario.safety_actions.slice(0, 2).map((act, i) => (
                  <div key={i} className="flex items-start gap-1.5 text-slate-700">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
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
