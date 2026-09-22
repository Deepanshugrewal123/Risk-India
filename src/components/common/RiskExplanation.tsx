import React, { useState } from 'react';
import { TrendingUp, Info, Sparkles, HelpCircle, ShieldAlert, ChevronDown, ChevronUp, BookOpen } from 'lucide-react';
import { DemoBadge } from './DemoBadge';

export interface ExplanationFactor {
  name: string;
  weight: number; // 0 to 100
  category?: 'Environmental' | 'Topographical' | 'Historical' | 'Hydrological';
  description: string;
}

interface RiskExplanationProps {
  locationName: string;
  disasterType: string;
  riskScore: number;
  factors: ExplanationFactor[];
  explanationNarrative?: string;
  className?: string;
  isAssamPrototype?: boolean;
  isMLScopeLimited?: boolean;
}

// Plain-Language Interpretations for Ordinary Citizens
const TECHNICAL_GLOSSARY: Record<string, { term: string; plainMeaning: string; practicalTip: string }> = {
  'antecedent rainfall': {
    term: 'Antecedent Rainfall',
    plainMeaning: 'Rain that fell over the past 24 to 72 hours. Because the ground is already soaked, new rain cannot soak in and runs off quickly, causing flash floods.',
    practicalTip: 'Keep storm drains clear and move vehicles away from low-lying culverts.'
  },
  'rainfall': {
    term: 'Catchment Rainfall',
    plainMeaning: 'Precipitation falling upstream that will flow down into nearby rivers over the next 12–48 hours.',
    practicalTip: 'River levels may rise even if it stops raining in your immediate neighborhood.'
  },
  'river stage': {
    term: 'River Stage & High Flood Level (HFL)',
    plainMeaning: 'River water height compared to the official Danger Level and historical High Flood Level mark.',
    practicalTip: 'Check local CWC gauges or district flood bulletins before crossing causeways.'
  },
  'probability': {
    term: 'Model Probability & Likelihood',
    plainMeaning: 'A scientific statistical estimate based on past flood patterns. It is not an official evacuation order.',
    practicalTip: 'Always follow instructions issued by your District Disaster Management Authority (DDMA).'
  },
  'focal depth': {
    term: 'Focal Depth (Earthquake)',
    plainMeaning: 'How deep underground the earthquake started. Shallow quakes (under 25 km) cause much stronger surface shaking.',
    practicalTip: 'During shaking: Drop, Cover, and Hold On. Avoid tall furniture and glass.'
  },
  'retention': {
    term: 'Valley Drainage Retention',
    plainMeaning: 'How slowly water drains out of a valley due to flat terrain, silted riverbeds, or high water tables.',
    practicalTip: 'Water will recede slowly; prepare drinking water and power banks for multi-day waterlogging.'
  },
};

export const RiskExplanation: React.FC<RiskExplanationProps> = ({
  locationName,
  disasterType,
  riskScore,
  factors,
  explanationNarrative,
  className = '',
  isAssamPrototype = false,
  isMLScopeLimited = false,
}) => {
  const [showGlossary, setShowGlossary] = useState<boolean>(false);
  const [showWhyModal, setShowWhyModal] = useState<boolean>(false);

  // Detect whether this is Assam prototype scope
  const isAssam = isAssamPrototype || locationName.toLowerCase().includes('assam') || locationName.toLowerCase().includes('udalguri') || locationName.toLowerCase().includes('kamrup');
  // Sort factors by weight descending to highlight top drivers
  const sortedFactors = [...factors].sort((a, b) => b.weight - a.weight);

  const defaultExplanation =
    explanationNarrative ||
    `Model prototype attributes the ${riskScore}% estimated ${disasterType.toLowerCase()} risk in ${locationName} primarily to ${
      sortedFactors[0]?.name.toLowerCase() || 'elevated environmental thresholds'
    } compounded by ${
      sortedFactors[1]?.name.toLowerCase() || 'regional vulnerability factors'
    }. Historical recurrence and local contour drainage inertia further elevate baseline exposure.`;

  return (
    <div
      className={`p-6 sm:p-7 rounded-3xl bg-white border border-paper-300 shadow-subtle ${className}`}
    >
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 mb-5 border-b border-paper-200">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="font-mono text-xs uppercase tracking-wider text-charcoal-500 font-bold flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-amber-500" />
              <span>WHY THIS RISK?</span>
            </span>
            <span className="text-charcoal-300">•</span>
            <span className="text-[10px] font-mono text-charcoal-400">
              FACTOR CONTRIBUTION BREAKDOWN
            </span>
          </div>
          <p className="text-xs text-charcoal-600">
            Explainable AI breakdown of contributing environmental and terrain signals
          </p>
        </div>
        
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowWhyModal(!showWhyModal)}
            className="px-2.5 py-1 rounded-xl bg-paper-100 hover:bg-paper-200 text-charcoal-800 text-xs font-mono font-semibold transition-colors flex items-center gap-1 border border-paper-200"
            title="Understand scientific boundaries and methodology"
          >
            <HelpCircle className="w-3.5 h-3.5 text-charcoal-600" />
            <span>Why am I seeing this?</span>
          </button>
          <DemoBadge label="FACTOR ATTRIBUTION" />
        </div>
      </div>

      {/* Scope Honesty Banner */}
      {isAssam ? (
        <div className="mb-5 p-3.5 rounded-2xl bg-amber-50/90 border border-amber-200 text-xs text-amber-950 flex items-start gap-2.5">
          <Sparkles className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
          <div className="space-y-0.5">
            <strong className="font-bold block">Empirical ML Risk — Assam Prototype</strong>
            <p className="text-[11px] leading-relaxed">
              ML Prototype Estimate — Validated only for the Assam Brahmaputra and Barak basin prototype scope (13 empirical features, 32 historical flood observations).
            </p>
          </div>
        </div>
      ) : (
        <div className="mb-5 p-3.5 rounded-2xl bg-blue-50/90 border border-blue-200 text-xs text-blue-950 flex items-start gap-2.5">
          <Info className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
          <div className="space-y-0.5">
            <strong className="font-bold block">Regional Baseline — ML unavailable for this region</strong>
            <p className="text-[11px] leading-relaxed">
              ML prediction unavailable for this region. Regional baseline risk and official disaster intelligence are shown. Empirical data is insufficient for machine learning in this region.
            </p>
          </div>
        </div>
      )}

      {/* Expandable "Why am I seeing this?" Scientific Explanation */}
      {showWhyModal && (
        <div className="mb-6 p-4 rounded-2xl bg-charcoal-900 text-paper-50 space-y-3 animate-in fade-in duration-200 text-xs">
          <div className="flex items-center justify-between pb-2 border-b border-charcoal-700">
            <span className="font-mono font-bold flex items-center gap-1.5 text-amber-300">
              <ShieldAlert className="w-4 h-4" />
              <span>Scientific Foundation & Verification Boundaries</span>
            </span>
            <button
              onClick={() => setShowWhyModal(false)}
              className="text-paper-300 hover:text-white text-xs font-mono"
            >
              Close [×]
            </button>
          </div>
          <p className="text-[11px] text-paper-200 leading-relaxed">
            RISK // INDIA strictly adheres to the principle of scientific honesty. The mathematical predictions displayed here are bounded by verified observation data:
          </p>
          <ul className="space-y-1.5 text-[11px] text-paper-300 list-disc list-inside">
            <li><strong>Assam Basin:</strong> Derived from 13 empirical features across 32 audited historical flood events (Udalguri, Darrang, Kamrup) using official CWC gauge telemetry.</li>
            <li><strong>Non-Assam States & UTs:</strong> Evaluated using multi-hazard baseline indices (seismic microzonation, IMD monsoon normal, terrain slope) without fabricated machine-learning weights.</li>
            <li><strong>Life-Safety Precaution:</strong> This automated breakdown does not supersede active evacuation orders or warnings from NDMA, SDMA, or district collectors.</li>
          </ul>
        </div>
      )}

      {/* Visual Factor Importance Bars (SHAP-Ready) */}
      <div className="space-y-4 mb-6">
        {sortedFactors.map((factor, index) => {
          // Bar styling based on relative contribution
          const isPrimary = index === 0;
          return (
            <div key={factor.name} className="space-y-1.5">
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <span
                    className={`w-1.5 h-1.5 rounded-full ${
                      factor.weight > 80
                        ? 'bg-risk-critical'
                        : factor.weight > 65
                        ? 'bg-risk-high'
                        : factor.weight > 45
                        ? 'bg-risk-moderate'
                        : 'bg-risk-low'
                    }`}
                  />
                  <span className="font-semibold text-charcoal-900">
                    {factor.name}
                  </span>
                  {isPrimary && (
                    <span className="text-[9px] font-mono uppercase px-1.5 py-0.5 rounded bg-amber-50 text-amber-800 border border-amber-200 font-bold">
                      Primary Driver
                    </span>
                  )}
                </div>
                <span className="font-mono font-bold text-charcoal-700">
                  {factor.weight}%
                </span>
              </div>

              {/* Graphical block segment progress bar */}
              <div className="w-full h-2.5 bg-paper-100 rounded-full overflow-hidden flex p-0.5 border border-paper-200">
                <div
                  className={`h-full rounded-full transition-all duration-700 ${
                    factor.weight > 80
                      ? 'bg-risk-critical'
                      : factor.weight > 65
                      ? 'bg-risk-high'
                      : factor.weight > 45
                      ? 'bg-risk-moderate'
                      : 'bg-risk-low'
                  }`}
                  style={{ width: `${factor.weight}%` }}
                />
              </div>

              <div className="flex items-center justify-between text-[11px] text-charcoal-500">
                <span>{factor.description}</span>
                {factor.category && (
                  <span className="font-mono text-[10px] text-charcoal-400">
                    {factor.category}
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Narrative Synthesis */}
      <div className="p-4 rounded-2xl bg-paper-50/80 border border-paper-200 mb-4">
        <div className="flex items-center gap-1.5 text-[11px] font-mono text-charcoal-500 uppercase tracking-wider mb-1.5">
          <Info className="w-3.5 h-3.5 text-charcoal-400" />
          <span>Synthesis Summary</span>
        </div>
        <p className="text-xs sm:text-sm text-charcoal-800 leading-relaxed font-normal">
          {defaultExplanation}
        </p>
      </div>

      {/* Plain-Language Citizen Glossary (Collapsible) */}
      <div className="rounded-2xl border border-paper-200 overflow-hidden bg-paper-50/50">
        <button
          onClick={() => setShowGlossary(!showGlossary)}
          className="w-full p-3.5 flex items-center justify-between text-left hover:bg-paper-100/70 transition-colors"
        >
          <div className="flex items-center gap-2 text-xs font-mono text-charcoal-700 font-semibold">
            <BookOpen className="w-3.5 h-3.5 text-charcoal-500" />
            <span>Plain-Language Terminology Guide for Citizens</span>
          </div>
          {showGlossary ? (
            <ChevronUp className="w-4 h-4 text-charcoal-500" />
          ) : (
            <ChevronDown className="w-4 h-4 text-charcoal-500" />
          )}
        </button>

        {showGlossary && (
          <div className="p-4 pt-1 space-y-3 text-xs border-t border-paper-200">
            {Object.entries(TECHNICAL_GLOSSARY).map(([key, item]) => (
              <div key={key} className="p-2.5 rounded-xl bg-white border border-paper-200">
                <div className="font-bold text-charcoal-900 mb-0.5">{item.term}</div>
                <p className="text-[11px] text-charcoal-600 mb-1 leading-relaxed">{item.plainMeaning}</p>
                <div className="text-[10px] font-mono text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded inline-block">
                  Tip: {item.practicalTip}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Disclaimers & Future ML Notice */}
      <div className="mt-4 pt-3 border-t border-paper-200 flex items-center justify-between text-[10px] font-mono text-charcoal-400">
        <span>Architected for future SHAP / TreeExplainer weights</span>
        <span>Informational estimate only • Follow DDMA/SDMA alerts</span>
      </div>
    </div>
  );
};
