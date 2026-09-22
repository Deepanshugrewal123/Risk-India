import React, { useState } from 'react';
import { PredictionExplanation } from '../../types/predictiveRisk';
import {
  HelpCircle,
  ShieldCheck,
  ChevronDown,
  ChevronUp,
  AlertCircle,
  Compass,
  CheckCircle2,
  Clock,
  Search,
  Sparkles
} from 'lucide-react';

interface RiskExplanationCardProps {
  explanation: PredictionExplanation;
  regionName: string;
  hazard: string;
}

export const RiskExplanationCard: React.FC<RiskExplanationCardProps> = ({
  explanation,
  regionName,
  hazard
}) => {
  const [activeTab, setActiveTab] = useState<'CITIZEN_ANSWERS' | 'TECHNICAL_EXPLANATION'>(
    'CITIZEN_ANSWERS'
  );
  const [expandedQuestion, setExpandedQuestion] = useState<number | null>(null);

  const { citizen_answers: ans } = explanation;

  const toggleQuestion = (idx: number) => {
    setExpandedQuestion(expandedQuestion === idx ? null : idx);
  };

  const citizenQuestions = [
    {
      num: 1,
      q: 'What is happening right now?',
      a: ans.what_is_happening_now,
      icon: Clock
    },
    {
      num: 2,
      q: 'What could happen next?',
      a: ans.what_could_happen_next,
      icon: Compass
    },
    {
      num: 3,
      q: 'What is the future risk trend?',
      a: ans.what_is_future_trend,
      icon: Sparkles
    },
    {
      num: 4,
      q: 'How serious could it become?',
      a: ans.how_serious_could_it_become,
      icon: AlertCircle
    },
    {
      num: 5,
      q: 'Why does the system think the risk may increase?',
      a: ans.why_risk_may_increase,
      icon: Search
    },
    {
      num: 6,
      q: 'What evidence supports that assessment?',
      a: ans.what_evidence_supports_it,
      isList: true,
      icon: ShieldCheck
    },
    {
      num: 7,
      q: 'What should I do now?',
      a: ans.what_should_i_do_now,
      isList: true,
      icon: CheckCircle2
    },
    {
      num: 8,
      q: 'What should I prepare before the disaster?',
      a: ans.what_to_prepare_before,
      isList: true,
      icon: CheckCircle2
    },
    {
      num: 9,
      q: 'What should I do during the disaster?',
      a: ans.what_to_do_during,
      isList: true,
      icon: CheckCircle2
    },
    {
      num: 10,
      q: 'What should I do after the disaster?',
      a: ans.what_to_do_after,
      isList: true,
      icon: CheckCircle2
    },
    {
      num: 11,
      q: 'What data is missing or uncertain?',
      a: ans.what_data_missing_or_uncertain,
      icon: HelpCircle
    },
    {
      num: 12,
      q: 'When should I check again?',
      a: ans.when_to_check_again,
      icon: Clock
    }
  ];

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-xs space-y-4">
      <div className="flex items-center justify-between flex-wrap gap-2 pb-2 border-b border-slate-200/80">
        <div className="flex items-center gap-2">
          <HelpCircle className="w-4 h-4 text-blue-600" />
          <h4 className="text-sm font-bold uppercase tracking-wider text-slate-900">
            Transparent Reasoning & Citizen Safety Intelligence
          </h4>
        </div>

        <div className="flex items-center gap-1 p-1 rounded-lg bg-slate-100 border border-slate-200/60 text-xs">
          <button
            onClick={() => setActiveTab('CITIZEN_ANSWERS')}
            className={`px-3 py-1 rounded-md font-semibold transition-colors ${
              activeTab === 'CITIZEN_ANSWERS'
                ? 'bg-blue-600 text-white shadow-2xs'
                : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
            }`}
          >
            12 Citizen Questions
          </button>
          <button
            onClick={() => setActiveTab('TECHNICAL_EXPLANATION')}
            className={`px-3 py-1 rounded-md font-semibold transition-colors ${
              activeTab === 'TECHNICAL_EXPLANATION'
                ? 'bg-blue-600 text-white shadow-2xs'
                : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
            }`}
          >
            Scientific Factors
          </button>
        </div>
      </div>

      {activeTab === 'CITIZEN_ANSWERS' && (
        <div className="space-y-2">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {citizenQuestions.map((item) => {
              const isExpanded = expandedQuestion === item.num;
              const IconComp = item.icon;

              return (
                <div
                  key={item.num}
                  className="rounded-xl border border-slate-200/80 bg-slate-50/70 hover:border-slate-300 transition-colors overflow-hidden"
                >
                  <button
                    onClick={() => toggleQuestion(item.num)}
                    className="w-full flex items-center justify-between p-3 text-left hover:bg-slate-100/70 transition-colors"
                  >
                    <div className="flex items-center gap-2.5 min-w-0 pr-2">
                      <span className="w-5 h-5 rounded-full bg-blue-100 text-blue-800 flex items-center justify-center text-[10px] font-bold shrink-0 font-mono">
                        {item.num}
                      </span>
                      <span className="text-xs font-semibold text-slate-900 truncate">
                        {item.q}
                      </span>
                    </div>
                    {isExpanded ? (
                      <ChevronUp className="w-4 h-4 text-slate-500 shrink-0" />
                    ) : (
                      <ChevronDown className="w-4 h-4 text-slate-500 shrink-0" />
                    )}
                  </button>

                  {isExpanded && (
                    <div className="p-3 pt-0 text-xs border-t border-slate-200/70 mt-1">
                      {item.isList && Array.isArray(item.a) ? (
                        <ul className="space-y-1 mt-1.5">
                          {item.a.map((line: string, i: number) => (
                            <li
                              key={i}
                              className="flex items-start gap-1.5 text-slate-700 leading-relaxed"
                            >
                              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                              <span>{line}</span>
                            </li>
                          ))}
                        </ul>
                      ) : (
                        <p className="text-slate-700 leading-relaxed mt-1">
                          {typeof item.a === 'string' ? item.a : JSON.stringify(item.a)}
                        </p>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {activeTab === 'TECHNICAL_EXPLANATION' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <div className="space-y-1.5 p-3 rounded-xl bg-slate-50/80 border border-slate-200/80">
            <span className="font-semibold text-slate-900 flex items-center gap-1.5">
              <Compass className="w-3.5 h-3.5 text-blue-600" />
              Why This Risk Level:
            </span>
            <p className="text-slate-700 leading-relaxed">
              {explanation.why_this_risk}
            </p>
          </div>

          <div className="space-y-1.5 p-3 rounded-xl bg-slate-50/80 border border-slate-200/80">
            <span className="font-semibold text-slate-900 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-blue-600" />
              What Changed:
            </span>
            <p className="text-slate-700 leading-relaxed">
              {explanation.what_changed}
            </p>
          </div>

          <div className="space-y-1.5 p-3 rounded-xl bg-rose-50/60 border border-rose-200/80">
            <span className="font-semibold text-rose-900 flex items-center gap-1.5">
              <AlertCircle className="w-3.5 h-3.5 text-rose-600" />
              What Could Make It Worse:
            </span>
            <p className="text-rose-800 leading-relaxed">
              {explanation.what_could_make_it_worse}
            </p>
          </div>

          <div className="space-y-1.5 p-3 rounded-xl bg-emerald-50/60 border border-emerald-200/80">
            <span className="font-semibold text-emerald-900 flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
              What Could Make It Improve:
            </span>
            <p className="text-emerald-800 leading-relaxed">
              {explanation.what_could_make_it_improve}
            </p>
          </div>

          <div className="col-span-1 md:col-span-2 space-y-1.5 p-3 rounded-xl bg-amber-50/40 border border-amber-200/70">
            <span className="font-semibold text-amber-950 flex items-center gap-1.5">
              <HelpCircle className="w-3.5 h-3.5 text-amber-600" />
              What We Do Not Know (Uncertainty & Data Gaps):
            </span>
            <p className="text-slate-700 leading-relaxed">
              {explanation.what_we_do_not_know}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default RiskExplanationCard;
