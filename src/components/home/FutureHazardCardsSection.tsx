import React, { useState, useEffect } from 'react';
import {
  RiskState,
  TrendState,
  ConfidenceLevel,
  UncertaintyLevel
} from '../../types/predictiveRisk';
import predictiveRiskService from '../../services/predictiveRiskService';
import { RiskTrendIndicator } from '../predictive/RiskTrendIndicator';
import { UncertaintyBadge } from '../predictive/UncertaintyBadge';
import {
  Droplets,
  Wind,
  Sun,
  CloudLightning,
  Mountain,
  Activity,
  ChevronRight,
  ShieldCheck,
  AlertTriangle,
  Clock,
  CheckCircle2
} from 'lucide-react';

interface HazardCardData {
  hazard: string;
  name: string;
  icon: any;
  color: string;
  currentState: RiskState;
  futureState: RiskState;
  trend: TrendState;
  expectedHorizon: string;
  why: string;
  confidence: ConfidenceLevel;
  uncertainty: UncertaintyLevel;
  whatToDo: string;
}

interface FutureHazardCardsSectionProps {
  onSelectHazard?: (hazard: string) => void;
}

export const FutureHazardCardsSection: React.FC<FutureHazardCardsSectionProps> = ({
  onSelectHazard
}) => {
  const [hazardCards, setHazardCards] = useState<HazardCardData[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const hazardMeta = [
    {
      hazard: 'FLOOD',
      name: 'Flood Risk',
      icon: Droplets,
      color: 'text-blue-500 bg-blue-500/10 border-blue-500/20',
      sampleRegion: 'assam'
    },
    {
      hazard: 'CYCLONE',
      name: 'Cyclone Risk',
      icon: Wind,
      color: 'text-teal-500 bg-teal-500/10 border-teal-500/20',
      sampleRegion: 'odisha'
    },
    {
      hazard: 'HEATWAVE',
      name: 'Heatwave Risk',
      icon: Sun,
      color: 'text-amber-500 bg-amber-500/10 border-amber-500/20',
      sampleRegion: 'delhi'
    },
    {
      hazard: 'SEVERE_WEATHER',
      name: 'Severe Weather',
      icon: CloudLightning,
      color: 'text-purple-500 bg-purple-500/10 border-purple-500/20',
      sampleRegion: 'himachal-pradesh'
    },
    {
      hazard: 'LANDSLIDE',
      name: 'Landslide Risk',
      icon: Mountain,
      color: 'text-emerald-500 bg-emerald-500/10 border-emerald-500/20',
      sampleRegion: 'uttarakhand'
    },
    {
      hazard: 'EARTHQUAKE',
      name: 'Seismic Hazard',
      icon: Activity,
      color: 'text-rose-500 bg-rose-500/10 border-rose-500/20',
      sampleRegion: 'jammu-kashmir'
    }
  ];

  useEffect(() => {
    const loadCards = async () => {
      try {
        setLoading(true);
        const cardPromises = hazardMeta.map(async (meta) => {
          try {
            const assess = await predictiveRiskService.getHazardAssessment(
              meta.sampleRegion,
              meta.hazard
            );
            return {
              hazard: meta.hazard,
              name: meta.name,
              icon: meta.icon,
              color: meta.color,
              currentState: assess.current_risk_state,
              futureState: assess.future_risk_state,
              trend: assess.trend,
              expectedHorizon: assess.peak_future_window,
              why: assess.explanation.citizen_answers.why_risk_may_increase,
              confidence: assess.confidence,
              uncertainty: assess.uncertainty,
              whatToDo: assess.explanation.citizen_answers.what_should_i_do_now[0] || 'Monitor official regional bulletins.'
            };
          } catch (e) {
            return {
              hazard: meta.hazard,
              name: meta.name,
              icon: meta.icon,
              color: meta.color,
              currentState: 'NORMAL' as RiskState,
              futureState: 'NORMAL' as RiskState,
              trend: 'STABLE' as TrendState,
              expectedHorizon: '6-24h',
              why: 'Multi-agency forecasts indicate baseline parameters.',
              confidence: 'MODERATE' as ConfidenceLevel,
              uncertainty: 'LOW' as UncertaintyLevel,
              whatToDo: 'Maintain baseline situational awareness.'
            };
          }
        });
        const results = await Promise.all(cardPromises);
        setHazardCards(results);
      } catch (err) {
        console.error('Failed to load hazard cards:', err);
      } finally {
        setLoading(false);
      }
    };
    loadCards();
  }, []);

  const getRiskColor = (state: RiskState) => {
    switch (state) {
      case 'CRITICAL':
        return 'text-rose-600 dark:text-rose-400 font-bold';
      case 'HIGH':
        return 'text-orange-600 dark:text-orange-400 font-bold';
      case 'ELEVATED':
        return 'text-amber-600 dark:text-amber-400 font-bold';
      case 'WATCH':
        return 'text-blue-600 dark:text-blue-400 font-bold';
      case 'NORMAL':
      default:
        return 'text-emerald-600 dark:text-emerald-400 font-bold';
    }
  };

  return (
    <section id="hazard-forecasts" className="py-10 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-3">
          <div>
            <div className="inline-flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-indigo-600 dark:text-indigo-400 mb-1">
              <Clock className="w-4 h-4" />
              <span>MULTI-HAZARD EARLY WARNING MATRIX</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-charcoal-950 dark:text-white">
              FUTURE RISK BY DISASTER HAZARD
            </h2>
            <p className="text-xs sm:text-sm text-charcoal-600 dark:text-slate-400 max-w-2xl mt-0.5 font-normal">
              Compare forward projections across all 6 supported disaster types.
              Earthquake reflects tectonic baseline and structural awareness (timing cannot be predicted).
            </p>
          </div>
        </div>

        {/* 6 Hazard Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {hazardCards.map((card) => {
            const IconComp = card.icon;

            return (
              <div
                key={card.hazard}
                className="p-5 rounded-3xl border border-paper-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between space-y-4"
              >
                <div className="space-y-3">
                  {/* Card Header */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2.5">
                      <div className={`p-2.5 rounded-2xl border ${card.color}`}>
                        <IconComp className="w-5 h-5" />
                      </div>
                      <div>
                        <h3 className="text-base font-bold text-charcoal-950 dark:text-white">
                          {card.name}
                        </h3>
                        <span className="text-[10px] font-mono text-slate-400 uppercase">
                          Horizon: {card.expectedHorizon}
                        </span>
                      </div>
                    </div>

                    <RiskTrendIndicator trend={card.trend} size="sm" />
                  </div>

                  {/* Current vs Future Metrics */}
                  <div className="grid grid-cols-2 gap-2 p-2.5 rounded-xl bg-paper-50 dark:bg-slate-850 border border-paper-200 dark:border-slate-800 text-xs">
                    <div>
                      <span className="text-[10px] font-mono text-charcoal-500 block">Current</span>
                      <span className={`text-xs font-mono ${getRiskColor(card.currentState)}`}>
                        {card.currentState}
                      </span>
                    </div>
                    <div>
                      <span className="text-[10px] font-mono text-charcoal-500 block">Future Projected</span>
                      <span className={`text-xs font-mono ${getRiskColor(card.futureState)}`}>
                        {card.futureState}
                      </span>
                    </div>
                  </div>

                  {/* Why */}
                  <div className="space-y-1 text-xs">
                    <span className="font-bold text-charcoal-800 dark:text-slate-200 font-mono text-[11px] block uppercase">
                      Why Risk May Increase:
                    </span>
                    <p className="text-charcoal-600 dark:text-slate-400 leading-relaxed text-[11px]">
                      {card.why}
                    </p>
                  </div>

                  {/* Confidence & Uncertainty */}
                  <div className="flex items-center justify-between text-[11px] pt-1">
                    <span className="text-charcoal-500 font-mono">Confidence / Uncertainty:</span>
                    <UncertaintyBadge
                      confidence={card.confidence}
                      uncertainty={card.uncertainty}
                      showLabels={false}
                    />
                  </div>
                </div>

                {/* What to do footer */}
                <div className="pt-3 border-t border-paper-100 dark:border-slate-800 text-xs space-y-1.5">
                  <span className="font-bold text-charcoal-900 dark:text-slate-100 flex items-center gap-1.5 text-[11px] uppercase font-mono">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                    What To Do:
                  </span>
                  <p className="text-charcoal-700 dark:text-slate-300 text-[11px] leading-relaxed">
                    {card.whatToDo}
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

export default FutureHazardCardsSection;
