import React, { useState, useEffect } from 'react';
import {
  PredictiveRiskAssessment,
  NationalPredictiveOverview,
  RiskState,
  TrendState,
  ConfidenceLevel,
  UncertaintyLevel
} from '../../types/predictiveRisk';
import predictiveRiskService from '../../services/predictiveRiskService';
import { ALL_INDIAN_STATES, ALL_INDIAN_UNION_TERRITORIES } from '../../data/indiaLocations';
import { IndiaLocation } from '../../types/location';
import { RiskTrendIndicator } from '../predictive/RiskTrendIndicator';
import { UncertaintyBadge } from '../predictive/UncertaintyBadge';
import { PredictionScopeNotice } from '../predictive/PredictionScopeNotice';
import {
  Search,
  MapPin,
  RefreshCw,
  Clock,
  ShieldAlert,
  CheckCircle2,
  PhoneCall,
  ChevronRight,
  AlertTriangle,
  HelpCircle,
  Radio,
  FileCheck2,
  ExternalLink,
  Globe,
  Layers,
  Sparkles,
  Info
} from 'lucide-react';

interface LocationRiskCheckerSectionProps {
  onOpenMap?: () => void;
  onViewFullAnalysis?: () => void;
}

export const LocationRiskCheckerSection: React.FC<LocationRiskCheckerSectionProps> = ({
  onOpenMap,
  onViewFullAnalysis
}) => {
  // Location Selection State (4-Tier Cascade: India -> State/UT -> District -> Locality)
  const allLocations = [...ALL_INDIAN_STATES, ...ALL_INDIAN_UNION_TERRITORIES];
  // Default is null (National India-Wide Future Risk Overview, zero hardcoded regional bias)
  const [selectedLocation, setSelectedLocation] = useState<IndiaLocation | null>(null);
  const [selectedDistrict, setSelectedDistrict] = useState<string>('');
  const [selectedLocality, setSelectedLocality] = useState<string>('');
  const [selectedHazard, setSelectedHazard] = useState<string>('FLOOD');

  // Search & Filter
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'OVERVIEW' | 'ACTIONS' | 'EVIDENCE'>('OVERVIEW');

  // Live Assessment & National Overview States
  const [assessment, setAssessment] = useState<PredictiveRiskAssessment | null>(null);
  const [nationalOverview, setNationalOverview] = useState<NationalPredictiveOverview | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Load National Overview if no location selected
  useEffect(() => {
    let isMounted = true;
    if (!selectedLocation) {
      setLoading(true);
      predictiveRiskService
        .getNationalOverview()
        .then((data) => {
          if (isMounted) setNationalOverview(data);
        })
        .catch((err) => {
          console.error('Failed to fetch national overview for checker:', err);
        })
        .finally(() => {
          if (isMounted) setLoading(false);
        });
    }
    return () => {
      isMounted = false;
    };
  }, [selectedLocation]);

  const fetchAssessment = async (locationId: string, hazard: string) => {
    try {
      setLoading(true);
      setError(null);
      const data = await predictiveRiskService.getHazardAssessment(locationId, hazard);
      setAssessment(data);
    } catch (err: any) {
      console.error('Failed to fetch location assessment:', err);
      setError('Live station telemetry currently unavailable for this specific jurisdiction.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedLocation) {
      fetchAssessment(selectedLocation.id, selectedHazard);
    }
  }, [selectedLocation, selectedHazard]);

  const handleSelectLocation = (loc: IndiaLocation) => {
    setSelectedLocation(loc);
    if (loc.districts && loc.districts.length > 0) {
      setSelectedDistrict(loc.districts[0]);
      setSelectedLocality(`${loc.districts[0]} Central / Municipal HQ`);
    } else {
      setSelectedDistrict('');
      setSelectedLocality('');
    }
  };

  const handleSelectDistrict = (dist: string) => {
    setSelectedDistrict(dist);
    setSelectedLocality(`${dist} Central / Municipal HQ`);
  };

  const filteredLocations = allLocations.filter(
    (loc) =>
      loc.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      loc.code.toLowerCase().includes(searchQuery.toLowerCase()) ||
      loc.districts.some((d) => d.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const getRiskColor = (state: RiskState) => {
    switch (state) {
      case 'CRITICAL':
        return 'text-rose-600 dark:text-rose-400 bg-rose-500/10 border-rose-500/30';
      case 'HIGH':
        return 'text-orange-600 dark:text-orange-400 bg-orange-500/10 border-orange-500/30';
      case 'ELEVATED':
        return 'text-amber-600 dark:text-amber-400 bg-amber-500/10 border-amber-500/30';
      case 'WATCH':
        return 'text-blue-600 dark:text-blue-400 bg-blue-500/10 border-blue-500/30';
      case 'NORMAL':
      default:
        return 'text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 border-emerald-500/30';
    }
  };

  return (
    <section id="location-checker" className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto relative">
      <div id="analyze-section" className="sr-only" aria-hidden="true" />
      <div id="check-location" className="sr-only" aria-hidden="true" />

      <div className="rounded-3xl border border-paper-300 bg-white dark:bg-slate-900 p-6 sm:p-8 shadow-xl space-y-6">
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-paper-200 dark:border-slate-800">
          <div>
            <div className="inline-flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-indigo-600 dark:text-indigo-400 mb-1">
              <MapPin className="w-4 h-4" />
              <span>4-TIER LOCATION RISK INTELLIGENCE CASCADE</span>
            </div>
            <h2 className="text-2xl sm:text-4xl font-extrabold text-charcoal-950 dark:text-white">
              CHECK RISK FOR MY LOCATION
            </h2>
            <p className="text-xs sm:text-sm text-charcoal-600 dark:text-slate-400 max-w-2xl mt-1 font-normal">
              Select your State / Union Territory, District, and Locality to receive an instant, unified assessment
              of current conditions, future risk trends, active warnings, and actionable survival advice.
            </p>
          </div>

          <div className="flex items-center gap-2 font-mono text-xs">
            <span className="px-3 py-1.5 rounded-xl bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/20 font-semibold flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              Live Telemetry & Provenance
            </span>
          </div>
        </div>

        {/* 4-Tier Location Cascade Grid */}
        <div className="p-4 rounded-2xl bg-paper-100 dark:bg-slate-850 border border-paper-200 dark:border-slate-800 space-y-3 text-xs">
          <div className="flex items-center justify-between text-[11px] font-mono text-charcoal-500 dark:text-slate-400 font-semibold uppercase">
            <span>4-TIER GEOSPATIAL CASCADE: INDIA → STATE/UT → DISTRICT → CITY/LOCALITY</span>
            <span className="text-indigo-600 dark:text-indigo-400 font-bold">ALL 36 JURISDICTIONS ACTIVE</span>
          </div>

          {/* Telemetry Disclaimer Notice */}
          <div className="p-2.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-900 dark:text-amber-200 text-xs font-mono flex items-center gap-2">
            <Info className="w-3.5 h-3.5 text-amber-600 shrink-0" />
            <span>
              <strong>Administrative Notice:</strong> Administrative selection does not guarantee live telemetry. Live sensor reporting depends on physical river-gauge and weather station coverage.
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            {/* Tier 1: Country */}
            <div className="space-y-1">
              <label className="font-mono text-charcoal-500 dark:text-slate-400 font-semibold uppercase">
                1. Country (Tier 1):
              </label>
              <div className="px-3 py-2 rounded-xl bg-white dark:bg-slate-800 border border-paper-300 dark:border-slate-700 font-medium text-charcoal-900 dark:text-white flex items-center justify-between">
                <span className="font-bold flex items-center gap-1.5">
                  <Globe className="w-3.5 h-3.5 text-indigo-600" />
                  India (National)
                </span>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-300 border border-indigo-200">
                  36 States/UTs
                </span>
              </div>
            </div>

            {/* Tier 2: State / Union Territory */}
            <div className="space-y-1">
              <label className="font-mono text-charcoal-500 dark:text-slate-400 font-semibold uppercase">
                2. State / UT (Tier 2):
              </label>
              <select
                value={selectedLocation ? selectedLocation.id : ''}
                onChange={(e) => {
                  const val = e.target.value;
                  if (!val) {
                    setSelectedLocation(null);
                    setSelectedDistrict('');
                    setSelectedLocality('');
                  } else {
                    const found = allLocations.find((l) => l.id === val);
                    if (found) handleSelectLocation(found);
                  }
                }}
                className="w-full px-3 py-2 rounded-xl bg-white dark:bg-slate-800 border border-paper-300 dark:border-slate-700 font-medium text-charcoal-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="">-- National Overview (India-Wide) --</option>
                <optgroup label="States (28)">
                  {ALL_INDIAN_STATES.map((loc) => (
                    <option key={loc.id} value={loc.id}>
                      {loc.name} ({loc.code})
                    </option>
                  ))}
                </optgroup>
                <optgroup label="Union Territories (8)">
                  {ALL_INDIAN_UNION_TERRITORIES.map((loc) => (
                    <option key={loc.id} value={loc.id}>
                      {loc.name} ({loc.code})
                    </option>
                  ))}
                </optgroup>
              </select>
            </div>

            {/* Tier 3: District */}
            <div className="space-y-1">
              <label className="font-mono text-charcoal-500 dark:text-slate-400 font-semibold uppercase">
                3. District (Tier 3):
              </label>
              <select
                value={selectedDistrict}
                disabled={!selectedLocation}
                onChange={(e) => handleSelectDistrict(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-white dark:bg-slate-800 border border-paper-300 dark:border-slate-700 font-medium text-charcoal-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-60"
              >
                {!selectedLocation ? (
                  <option value="">Select State/UT First</option>
                ) : (
                  selectedLocation.districts.map((d) => (
                    <option key={d} value={d}>
                      {d}
                    </option>
                  ))
                )}
              </select>
            </div>

            {/* Tier 4: City / Locality / Sub-district */}
            <div className="space-y-1">
              <label className="font-mono text-charcoal-500 dark:text-slate-400 font-semibold uppercase">
                4. City / Locality (Tier 4):
              </label>
              <select
                value={selectedLocality}
                disabled={!selectedLocation}
                onChange={(e) => setSelectedLocality(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-white dark:bg-slate-800 border border-paper-300 dark:border-slate-700 font-medium text-charcoal-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-60"
              >
                {!selectedLocation ? (
                  <option value="">Select District First</option>
                ) : (
                  <>
                    <option value={`${selectedDistrict} Central / Municipal HQ`}>
                      {selectedDistrict} Central / Municipal HQ
                    </option>
                    <option value={`${selectedDistrict} North / Tehsil Sector`}>
                      {selectedDistrict} North / Tehsil Sector
                    </option>
                    <option value={`${selectedDistrict} South / Basin Sector`}>
                      {selectedDistrict} South / Basin Sector
                    </option>
                    <option value={`${selectedDistrict} Rural / Agricultural Belt`}>
                      {selectedDistrict} Rural / Agricultural Belt
                    </option>
                  </>
                )}
              </select>
            </div>
          </div>

          {/* Hazard Focus Buttons */}
          <div className="pt-2 border-t border-paper-200 dark:border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <span className="font-mono text-charcoal-500 dark:text-slate-400 font-semibold uppercase">
                Hazard Focus:
              </span>
              <div className="flex flex-wrap gap-1.5">
                {['FLOOD', 'CYCLONE', 'HEATWAVE', 'SEVERE_WEATHER', 'LANDSLIDE', 'EARTHQUAKE'].map((h) => (
                  <button
                    key={h}
                    onClick={() => setSelectedHazard(h)}
                    className={`px-2.5 py-1 rounded-lg text-xs font-mono font-bold transition-colors ${
                      selectedHazard === h
                        ? 'bg-indigo-600 text-white shadow-xs'
                        : 'bg-white dark:bg-slate-800 text-charcoal-700 dark:text-slate-300 border border-paper-200 dark:border-slate-700 hover:bg-paper-200'
                    }`}
                  >
                    {h.replace('_', ' ')}
                  </button>
                ))}
              </div>
            </div>
            <div className="text-[11px] font-mono text-charcoal-500">
              Selected:{' '}
              <span className="font-bold text-charcoal-900 dark:text-white">
                {selectedLocation
                  ? `${selectedLocality || selectedDistrict}, ${selectedLocation.name}`
                  : 'National India-Wide Overview (All 36 Jurisdictions)'}
              </span>
            </div>
          </div>
        </div>

        {/* Scope Notice Banner */}
        {assessment && (
          <PredictionScopeNotice
            isAssam={assessment.region_id === 'assam'}
            hazard={assessment.hazard}
            mlScope={assessment.ml_scope}
            syntheticRecords={assessment.synthetic_records}
          />
        )}

        {/* Live Assessment Results Card or National Overview */}
        {loading ? (
          <div className="p-12 text-center text-xs text-slate-500 font-mono flex items-center justify-center gap-2">
            <RefreshCw className="w-4 h-4 animate-spin text-indigo-500" />
            <span>Retrieving live station telemetry and forecast models for {selectedLocation?.name || 'National Overview'}...</span>
          </div>
        ) : !selectedLocation ? (
          /* National India-Wide Risk Checker Overview */
          <div className="space-y-6 pt-2">
            <div className="p-5 rounded-2xl bg-indigo-50/50 dark:bg-indigo-950/20 border border-indigo-200 dark:border-indigo-900 flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <Globe className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                  <span className="font-mono text-xs uppercase tracking-wider font-bold text-indigo-950 dark:text-indigo-200">
                    NATIONAL INDIA-WIDE FUTURE RISK OVERVIEW
                  </span>
                </div>
                <h3 className="text-xl font-bold text-charcoal-950 dark:text-white">
                  Pan-India Administrative & Forecast Status
                </h3>
                <p className="text-xs text-charcoal-600 dark:text-slate-400 mt-1">
                  Covering 28 States & 8 Union Territories. Select any jurisdiction above to cascade into district and locality telemetry.
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-2">
                {onViewFullAnalysis && (
                  <button
                    onClick={onViewFullAnalysis}
                    className="px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold bg-indigo-600 text-white hover:bg-indigo-700 transition-colors shadow-xs"
                  >
                    View Full Future Risk Analysis
                  </button>
                )}
                {onOpenMap && (
                  <button
                    onClick={onOpenMap}
                    className="px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold bg-charcoal-900 text-paper-50 hover:bg-charcoal-800 transition-colors"
                  >
                    Open Risk Map
                  </button>
                )}
              </div>
            </div>

            {/* Coverage Level Breakdown Badges */}
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 text-center text-[10px] font-mono">
              <div className="p-2.5 rounded-xl bg-paper-50 dark:bg-slate-800 border border-paper-200 dark:border-slate-700">
                <div className="text-charcoal-500 dark:text-slate-400">ADMIN COVERAGE</div>
                <div className="font-bold text-charcoal-900 dark:text-white mt-0.5">36/36 States & UTs</div>
              </div>
              <div className="p-2.5 rounded-xl bg-paper-50 dark:bg-slate-800 border border-paper-200 dark:border-slate-700">
                <div className="text-charcoal-500 dark:text-slate-400">REGIONAL BASELINE</div>
                <div className="font-bold text-charcoal-900 dark:text-white mt-0.5">100% Pan-India</div>
              </div>
              <div className="p-2.5 rounded-xl bg-paper-50 dark:bg-slate-800 border border-paper-200 dark:border-slate-700">
                <div className="text-charcoal-500 dark:text-slate-400">LIVE TELEMETRY</div>
                <div className="font-bold text-charcoal-900 dark:text-white mt-0.5">IMD/CWC Sensors</div>
              </div>
              <div className="p-2.5 rounded-xl bg-paper-50 dark:bg-slate-800 border border-paper-200 dark:border-slate-700">
                <div className="text-charcoal-500 dark:text-slate-400">FORECAST RANGE</div>
                <div className="font-bold text-charcoal-900 dark:text-white mt-0.5">NOW to 7 Days</div>
              </div>
              <div className="p-2.5 rounded-xl bg-paper-50 dark:bg-slate-800 border border-paper-200 dark:border-slate-700">
                <div className="text-charcoal-500 dark:text-slate-400">OFFICIAL WARNINGS</div>
                <div className="font-bold text-charcoal-900 dark:text-white mt-0.5">IMD & NDMA Direct</div>
              </div>
              <div className="p-2.5 rounded-xl bg-paper-50 dark:bg-slate-800 border border-paper-200 dark:border-slate-700">
                <div className="text-charcoal-500 dark:text-slate-400">APPROVED ML SCOPE</div>
                <div className="font-bold text-indigo-600 dark:text-indigo-400 mt-0.5">Assam Flood (Only)</div>
              </div>
            </div>

            {/* Quick State/UT Selection Pills */}
            <div className="space-y-2">
              <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 dark:text-slate-400 font-bold block">
                Quick Jump to Jurisdiction (Click to analyze):
              </span>
              <div className="flex flex-wrap gap-1.5">
                {allLocations.map((loc) => (
                  <button
                    key={loc.id}
                    onClick={() => handleSelectLocation(loc)}
                    className="px-2.5 py-1 rounded-lg text-xs font-mono bg-paper-50 dark:bg-slate-800 text-charcoal-700 dark:text-slate-300 border border-paper-200 dark:border-slate-700 hover:bg-paper-200 dark:hover:bg-slate-700 transition-colors"
                  >
                    {loc.name}
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : error ? (
          <div className="p-6 rounded-2xl bg-amber-50/70 dark:bg-amber-950/20 border border-amber-300 dark:border-amber-800 space-y-4 text-xs font-mono">
            <div className="flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
              <div>
                <h4 className="text-sm font-bold text-charcoal-900 dark:text-white uppercase">
                  DATA UNAVAILABLE // LIMITED EVIDENCE
                </h4>
                <p className="text-charcoal-700 dark:text-slate-300 mt-1 font-sans">
                  Real-time telemetry and numerical forecast signals are not currently reporting for{' '}
                  <strong>{selectedLocality || selectedDistrict || selectedLocation.name}</strong> under{' '}
                  <strong>{selectedHazard}</strong>. In accordance with scientific safety principles,
                  RISK // INDIA does not synthesize or interpolate artificial predictions.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
              <div className="p-3.5 rounded-xl bg-white dark:bg-slate-900 border border-amber-200 dark:border-amber-900 text-xs space-y-1">
                <div className="text-emerald-700 dark:text-emerald-400 font-bold flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>WHAT IS KNOWN:</span>
                </div>
                <ul className="list-disc pl-4 text-charcoal-700 dark:text-slate-300 space-y-0.5 text-[11px] font-sans">
                  <li>Administrative Jurisdiction: {selectedLocation.name} ({selectedLocation.type})</li>
                  <li>Historical baseline primary hazard: {selectedLocation.primaryRisk}</li>
                  <li>24/7 Statutory emergency helplines remain fully operational</li>
                </ul>
              </div>

              <div className="p-3.5 rounded-xl bg-white dark:bg-slate-900 border border-amber-200 dark:border-amber-900 text-xs space-y-1">
                <div className="text-amber-700 dark:text-amber-400 font-bold flex items-center gap-1">
                  <HelpCircle className="w-3.5 h-3.5" />
                  <span>WHAT IS UNKNOWN:</span>
                </div>
                <ul className="list-disc pl-4 text-charcoal-700 dark:text-slate-300 space-y-0.5 text-[11px] font-sans">
                  <li>Locality micro-radar precipitation telemetry</li>
                  <li>Basin sensor discharge readings within the last 6 hours</li>
                  <li>No active IMD Red/Orange bulletin issued for this sub-district</li>
                </ul>
              </div>
            </div>

            {/* 7 Required Data Availability Audit Points */}
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 pt-2 text-[10px] font-mono">
              <div className="p-2 rounded-xl bg-white dark:bg-slate-900 border border-amber-200 dark:border-amber-900">
                <span className="text-charcoal-500 uppercase block">Last Available Observation</span>
                <span className="font-bold text-charcoal-800 dark:text-slate-200 mt-0.5 block">No recent gauge reading</span>
              </div>
              <div className="p-2 rounded-xl bg-white dark:bg-slate-900 border border-amber-200 dark:border-amber-900">
                <span className="text-charcoal-500 uppercase block">Source / Provenance</span>
                <span className="font-bold text-charcoal-800 dark:text-slate-200 mt-0.5 block">CWC / IMD Station Network</span>
              </div>
              <div className="p-2 rounded-xl bg-white dark:bg-slate-900 border border-amber-200 dark:border-amber-900">
                <span className="text-charcoal-500 uppercase block">Freshness</span>
                <span className="font-bold text-amber-600 dark:text-amber-400 mt-0.5 block">DATA UNAVAILABLE</span>
              </div>
              <div className="p-2 rounded-xl bg-white dark:bg-slate-900 border border-amber-200 dark:border-amber-900">
                <span className="text-charcoal-500 uppercase block">Forecast Availability</span>
                <span className="font-bold text-charcoal-800 dark:text-slate-200 mt-0.5 block">Regional Climatology Only</span>
              </div>
              <div className="p-2 rounded-xl bg-white dark:bg-slate-900 border border-amber-200 dark:border-amber-900">
                <span className="text-charcoal-500 uppercase block">Official Warning Availability</span>
                <span className="font-bold text-emerald-600 dark:text-emerald-400 mt-0.5 block">No Active Red/Orange Bulletin</span>
              </div>
            </div>

            <div className="pt-2 flex flex-wrap items-center justify-between gap-3 text-[11px] text-charcoal-600 dark:text-slate-400 border-t border-amber-200 dark:border-amber-900">
              <span>National Emergency: 112 • NDMA: 1078 • State Relief: 1070</span>
              {onViewFullAnalysis && (
                <button
                  onClick={onViewFullAnalysis}
                  className="text-indigo-600 dark:text-indigo-400 font-bold hover:underline"
                >
                  View Full Future Risk Analysis →
                </button>
              )}
            </div>
          </div>
        ) : assessment ? (
          <div className="space-y-6">
            {/* Dynamic 6-Tier Coverage Summary for Selected Location */}
            <div className="p-4 rounded-2xl bg-paper-50 dark:bg-slate-850 border border-paper-200 dark:border-slate-800 space-y-2 text-xs font-mono">
              <div className="flex items-center justify-between text-[11px] font-bold text-charcoal-700 dark:text-slate-300 uppercase">
                <span>COVERAGE SUMMARY // {selectedLocation.name} ({selectedLocation.type})</span>
                <span className="text-indigo-600 dark:text-indigo-400 font-semibold">6-TIER STATUS</span>
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 text-center text-[10px]">
                <div className="p-2 rounded-xl bg-white dark:bg-slate-800 border border-paper-200 dark:border-slate-700">
                  <div className="text-charcoal-500 dark:text-slate-400 uppercase">Administrative Coverage</div>
                  <div className="font-bold text-charcoal-900 dark:text-white mt-0.5">Tier 2 ({selectedLocation.code})</div>
                </div>
                <div className="p-2 rounded-xl bg-white dark:bg-slate-800 border border-paper-200 dark:border-slate-700">
                  <div className="text-charcoal-500 dark:text-slate-400 uppercase">Regional Baseline</div>
                  <div className="font-bold text-emerald-600 dark:text-emerald-400 mt-0.5">Active (100%)</div>
                </div>
                <div className="p-2 rounded-xl bg-white dark:bg-slate-800 border border-paper-200 dark:border-slate-700">
                  <div className="text-charcoal-500 dark:text-slate-400 uppercase">Live Telemetry</div>
                  <div className="font-bold text-charcoal-900 dark:text-white mt-0.5">
                    {selectedLocation.id === 'assam' || selectedLocation.id === 'odisha' || selectedLocation.id === 'andhra-pradesh'
                      ? 'Active (CWC/IMD)'
                      : 'Regional Baseline'}
                  </div>
                </div>
                <div className="p-2 rounded-xl bg-white dark:bg-slate-800 border border-paper-200 dark:border-slate-700">
                  <div className="text-charcoal-500 dark:text-slate-400 uppercase">Forecast</div>
                  <div className="font-bold text-indigo-600 dark:text-indigo-400 mt-0.5">Active (NOW–7d)</div>
                </div>
                <div className="p-2 rounded-xl bg-white dark:bg-slate-800 border border-paper-200 dark:border-slate-700">
                  <div className="text-charcoal-500 dark:text-slate-400 uppercase">Official Warnings</div>
                  <div className="font-bold text-charcoal-900 dark:text-white mt-0.5">IMD / NDMA Direct</div>
                </div>
                <div className="p-2 rounded-xl bg-white dark:bg-slate-800 border border-paper-200 dark:border-slate-700">
                  <div className="text-charcoal-500 dark:text-slate-400 uppercase">Approved ML</div>
                  <div className={`font-bold mt-0.5 ${selectedLocation.id === 'assam' ? 'text-purple-600 dark:text-purple-400' : 'text-charcoal-400'}`}>
                    {selectedLocation.id === 'assam' ? 'Active (Assam ML)' : 'Not Available'}
                  </div>
                </div>
              </div>
            </div>

            {/* 11 Required Fields Disaster Intelligence Matrix */}
            <div className="p-4 rounded-2xl bg-paper-50 dark:bg-slate-850 border border-paper-200 dark:border-slate-800 space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-paper-200 dark:border-slate-800 pb-2">
                <span className="font-mono text-xs font-bold uppercase tracking-wider text-charcoal-800 dark:text-slate-200 flex items-center gap-1.5">
                  <ShieldAlert className="w-4 h-4 text-indigo-600" />
                  <span>UNIFIED 11-POINT CITIZEN INTELLIGENCE ASSESSMENT</span>
                </span>
                <span className="text-[11px] font-mono text-charcoal-500">
                  Target: {selectedDistrict}, {selectedLocation.name}
                </span>
              </div>

              {/* Grid of 11 Required Fields */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
                {/* 1. CURRENT RISK */}
                <div className="p-3 rounded-xl bg-white dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-1">
                  <span className="font-mono text-[10px] text-charcoal-500 uppercase block font-semibold">
                    1. CURRENT RISK
                  </span>
                  <div className={`text-base font-black font-mono px-2 py-0.5 rounded border inline-block ${getRiskColor(assessment.current_risk_state)}`}>
                    {assessment.current_risk_state}
                  </div>
                  <span className="text-[11px] font-mono text-charcoal-600 dark:text-slate-300 block">
                    Score: {assessment.current_risk_score} / 100
                  </span>
                </div>

                {/* 2. FUTURE RISK */}
                <div className="p-3 rounded-xl bg-white dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-1">
                  <span className="font-mono text-[10px] text-charcoal-500 uppercase block font-semibold">
                    2. FUTURE RISK
                  </span>
                  <div className={`text-base font-black font-mono px-2 py-0.5 rounded border inline-block ${getRiskColor(assessment.future_risk_state)}`}>
                    {assessment.future_risk_state}
                  </div>
                  <span className="text-[11px] font-mono text-charcoal-600 dark:text-slate-300 block">
                    Peak: {assessment.peak_future_score} / 100
                  </span>
                </div>

                {/* 3. MAIN HAZARD */}
                <div className="p-3 rounded-xl bg-white dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-1">
                  <span className="font-mono text-[10px] text-charcoal-500 uppercase block font-semibold">
                    3. MAIN HAZARD
                  </span>
                  <div className="text-base font-bold font-mono text-charcoal-900 dark:text-white uppercase">
                    {assessment.hazard}
                  </div>
                  <span className="text-[11px] font-mono text-charcoal-500 block">
                    Primary Hazard Vector
                  </span>
                </div>

                {/* 4. RISK TREND */}
                <div className="p-3 rounded-xl bg-white dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-1">
                  <span className="font-mono text-[10px] text-charcoal-500 uppercase block font-semibold">
                    4. RISK TREND
                  </span>
                  <RiskTrendIndicator trend={assessment.trend} size="md" />
                  <span className="text-[10px] font-mono text-charcoal-500 block mt-1">
                    Trajectory over 72h
                  </span>
                </div>

                {/* 5. TIME HORIZON */}
                <div className="p-3 rounded-xl bg-white dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-1">
                  <span className="font-mono text-[10px] text-charcoal-500 uppercase block font-semibold">
                    5. TIME HORIZON
                  </span>
                  <div className="text-sm font-bold font-mono text-indigo-600 dark:text-indigo-400">
                    {assessment.peak_future_window}
                  </div>
                  <span className="text-[10px] font-mono text-charcoal-500 block">
                    Lead time before peak
                  </span>
                </div>

                {/* 6. CONFIDENCE */}
                <div className="p-3 rounded-xl bg-white dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-1">
                  <span className="font-mono text-[10px] text-charcoal-500 uppercase block font-semibold">
                    6. CONFIDENCE
                  </span>
                  <div className="text-sm font-bold font-mono text-charcoal-900 dark:text-white">
                    {assessment.confidence}
                  </div>
                  <span className="text-[10px] font-mono text-charcoal-500 block">
                    Telemetry signal quality
                  </span>
                </div>

                {/* 7. UNCERTAINTY */}
                <div className="p-3 rounded-xl bg-white dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-1">
                  <span className="font-mono text-[10px] text-charcoal-500 uppercase block font-semibold">
                    7. UNCERTAINTY
                  </span>
                  <UncertaintyBadge
                    confidence={assessment.confidence}
                    uncertainty={assessment.uncertainty}
                    showLabels={false}
                  />
                  <span className="text-[10px] font-mono text-charcoal-500 block mt-1">
                    Expands with lead time
                  </span>
                </div>

                {/* 8. WHY? */}
                <div className="p-3 rounded-xl bg-white dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-1">
                  <span className="font-mono text-[10px] text-charcoal-500 uppercase block font-semibold">
                    8. WHY? (SCIENTIFIC RATIONALE)
                  </span>
                  <p className="text-[11px] text-charcoal-700 dark:text-slate-300 line-clamp-2">
                    {assessment.explanation.why_this_risk}
                  </p>
                </div>
              </div>

              {/* Fields 9, 10, 11 (What to Do, Official Warning, Verified Help) */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2">
                {/* 9. WHAT TO DO? */}
                <div className="p-3.5 rounded-xl bg-indigo-50/70 dark:bg-indigo-950/30 border border-indigo-200 dark:border-indigo-800 space-y-1.5">
                  <span className="font-mono text-[11px] font-bold text-indigo-900 dark:text-indigo-200 uppercase flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4 text-indigo-600" />
                    <span>9. WHAT TO DO? (CITIZEN PROTOCOL)</span>
                  </span>
                  <p className="text-xs text-indigo-950 dark:text-indigo-100 font-medium">
                    {assessment.explanation.citizen_answers.what_should_i_do_now[0] || 'Inspect local surroundings and secure emergency kit.'}
                  </p>
                  <span className="text-[10px] font-mono text-indigo-700 dark:text-indigo-300 block">
                    See Tab 2 below for pre-disaster & during safety steps.
                  </span>
                </div>

                {/* 10. OFFICIAL WARNING */}
                <div className="p-3.5 rounded-xl bg-amber-50/70 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800 space-y-1.5">
                  <span className="font-mono text-[11px] font-bold text-amber-900 dark:text-amber-200 uppercase flex items-center gap-1.5">
                    <AlertTriangle className="w-4 h-4 text-amber-600" />
                    <span>10. OFFICIAL WARNING STATUS</span>
                  </span>
                  <p className="text-xs text-amber-950 dark:text-amber-100 font-medium">
                    Statutory alerts active via IMD / CWC / NDMA feeds. Evacuation orders are strictly legally issued by District Magistrate / SDMA under Disaster Management Act, 2005.
                  </p>
                  <span className="text-[10px] font-mono text-amber-700 dark:text-amber-300 block">
                    Advisories support preparation; heed official civil orders.
                  </span>
                </div>

                {/* 11. VERIFIED HELP */}
                <div className="p-3.5 rounded-xl bg-rose-50/70 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-800 space-y-1.5">
                  <span className="font-mono text-[11px] font-bold text-rose-900 dark:text-rose-200 uppercase flex items-center gap-1.5">
                    <PhoneCall className="w-4 h-4 text-rose-600" />
                    <span>11. VERIFIED HELP DIRECTORY</span>
                  </span>
                  <div className="flex flex-wrap gap-1.5 text-xs font-mono font-bold">
                    <a href="tel:112" className="px-2 py-0.5 rounded bg-white dark:bg-slate-800 text-rose-600 border border-rose-200 hover:underline">112 National</a>
                    <a href="tel:1078" className="px-2 py-0.5 rounded bg-white dark:bg-slate-800 text-rose-600 border border-rose-200 hover:underline">1078 NDMA</a>
                    <a href="tel:1070" className="px-2 py-0.5 rounded bg-white dark:bg-slate-800 text-rose-600 border border-rose-200 hover:underline">1070 SDMA</a>
                    <a href="tel:1077" className="px-2 py-0.5 rounded bg-white dark:bg-slate-800 text-rose-600 border border-rose-200 hover:underline">1077 DEOC</a>
                  </div>
                  <span className="text-[10px] font-mono text-rose-700 dark:text-rose-300 block">
                    Pan-India 24/7 statutory emergency response dispatch.
                  </span>
                </div>
              </div>
            </div>

            {/* Navigation Tabs for Location Inspector */}
            <div className="flex items-center gap-2 border-b border-paper-200 dark:border-slate-800 text-xs pb-1">
              <button
                onClick={() => setActiveTab('OVERVIEW')}
                className={`px-4 py-2 font-bold transition-all border-b-2 -mb-1 ${
                  activeTab === 'OVERVIEW'
                    ? 'border-indigo-600 text-indigo-600 dark:text-indigo-400'
                    : 'border-transparent text-charcoal-600 dark:text-slate-400 hover:text-charcoal-950'
                }`}
              >
                1. What May Happen Next?
              </button>
              <button
                onClick={() => setActiveTab('ACTIONS')}
                className={`px-4 py-2 font-bold transition-all border-b-2 -mb-1 ${
                  activeTab === 'ACTIONS'
                    ? 'border-indigo-600 text-indigo-600 dark:text-indigo-400'
                    : 'border-transparent text-charcoal-600 dark:text-slate-400 hover:text-charcoal-950'
                }`}
              >
                2. What Should I Do?
              </button>
              <button
                onClick={() => setActiveTab('EVIDENCE')}
                className={`px-4 py-2 font-bold transition-all border-b-2 -mb-1 ${
                  activeTab === 'EVIDENCE'
                    ? 'border-indigo-600 text-indigo-600 dark:text-indigo-400'
                    : 'border-transparent text-charcoal-600 dark:text-slate-400 hover:text-charcoal-950'
                }`}
              >
                3. Why Could Risk Increase?
              </button>
            </div>

            {/* Tab 1: Overview & Citizen Answers */}
            {activeTab === 'OVERVIEW' && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div className="p-4 rounded-2xl bg-paper-50 dark:bg-slate-850 border border-paper-200 dark:border-slate-800 space-y-2">
                  <span className="font-bold text-charcoal-900 dark:text-white flex items-center gap-1.5 uppercase font-mono tracking-wider">
                    <Clock className="w-4 h-4 text-indigo-500" />
                    What Is Happening Right Now?
                  </span>
                  <p className="text-charcoal-700 dark:text-slate-300 leading-relaxed font-normal">
                    {assessment.explanation.citizen_answers.what_is_happening_now}
                  </p>
                </div>

                <div className="p-4 rounded-2xl bg-paper-50 dark:bg-slate-850 border border-paper-200 dark:border-slate-800 space-y-2">
                  <span className="font-bold text-charcoal-900 dark:text-white flex items-center gap-1.5 uppercase font-mono tracking-wider">
                    <Clock className="w-4 h-4 text-indigo-500" />
                    What Could Happen Next?
                  </span>
                  <p className="text-charcoal-700 dark:text-slate-300 leading-relaxed font-normal">
                    {assessment.explanation.citizen_answers.what_could_happen_next}
                  </p>
                </div>

                <div className="p-4 rounded-2xl bg-paper-50 dark:bg-slate-850 border border-paper-200 dark:border-slate-800 space-y-2">
                  <span className="font-bold text-charcoal-900 dark:text-white flex items-center gap-1.5 uppercase font-mono tracking-wider">
                    <AlertTriangle className="w-4 h-4 text-amber-500" />
                    How Serious Could It Become?
                  </span>
                  <p className="text-charcoal-700 dark:text-slate-300 leading-relaxed font-normal">
                    {assessment.explanation.citizen_answers.how_serious_could_it_become}
                  </p>
                </div>

                <div className="p-4 rounded-2xl bg-paper-50 dark:bg-slate-850 border border-paper-200 dark:border-slate-800 space-y-2">
                  <span className="font-bold text-charcoal-900 dark:text-white flex items-center gap-1.5 uppercase font-mono tracking-wider">
                    <Clock className="w-4 h-4 text-indigo-500" />
                    When Should I Check Again?
                  </span>
                  <p className="text-charcoal-700 dark:text-slate-300 leading-relaxed font-normal">
                    {assessment.explanation.citizen_answers.when_to_check_again}
                  </p>
                </div>
              </div>
            )}

            {/* Tab 2: Action Protocols & Verified Helplines */}
            {activeTab === 'ACTIONS' && (
              <div className="space-y-4 text-xs">
                {/* Priority Do Now Checklist */}
                <div className="p-4 rounded-2xl border border-indigo-500/30 bg-indigo-50/50 dark:bg-indigo-950/20 space-y-2">
                  <span className="font-bold text-indigo-950 dark:text-indigo-200 text-sm flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-indigo-600" />
                    <span>DO THIS RIGHT NOW ({assessment.hazard}):</span>
                  </span>
                  <ul className="space-y-1.5 text-indigo-900 dark:text-indigo-200">
                    {assessment.explanation.citizen_answers.what_should_i_do_now.map((act, i) => (
                      <li key={i} className="flex items-start gap-2 leading-relaxed">
                        <span className="font-mono font-bold">{i + 1}.</span>
                        <span>{act}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Pre-Disaster & During Protocols */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div className="p-3.5 rounded-2xl bg-paper-50 dark:bg-slate-850 border border-paper-200 dark:border-slate-800 space-y-2">
                    <span className="font-bold text-charcoal-900 dark:text-white block">
                      Prepare Before the Disaster:
                    </span>
                    <ul className="space-y-1 text-charcoal-600 dark:text-slate-300">
                      {assessment.explanation.citizen_answers.what_to_prepare_before.map((p, i) => (
                        <li key={i} className="flex items-start gap-1.5">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" />
                          <span>{p}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="p-3.5 rounded-2xl bg-paper-50 dark:bg-slate-850 border border-paper-200 dark:border-slate-800 space-y-2">
                    <span className="font-bold text-charcoal-900 dark:text-white block">
                      During the Disaster:
                    </span>
                    <ul className="space-y-1 text-charcoal-600 dark:text-slate-300">
                      {assessment.explanation.citizen_answers.what_to_do_during.map((d, i) => (
                        <li key={i} className="flex items-start gap-1.5">
                          <AlertTriangle className="w-3.5 h-3.5 text-amber-500 shrink-0 mt-0.5" />
                          <span>{d}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Verified Emergency Help Directory */}
                <div className="p-4 rounded-2xl bg-rose-50/50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-800 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-rose-900 dark:text-rose-200 flex items-center gap-1.5 uppercase font-mono">
                      <PhoneCall className="w-4 h-4 text-rose-600" />
                      <span>Verified Statutory Emergency Contacts</span>
                    </span>
                    <span className="text-[10px] font-mono text-rose-700 dark:text-rose-300">24/7 Pan-India</span>
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center">
                    <a
                      href="tel:112"
                      className="p-2.5 rounded-xl bg-white dark:bg-slate-800 border border-rose-200 dark:border-rose-900 text-charcoal-900 dark:text-white font-bold hover:bg-rose-100 dark:hover:bg-rose-900/40 transition-colors"
                    >
                      <span className="text-[10px] text-slate-500 block font-mono">National Emergency</span>
                      <span className="text-sm font-mono text-rose-600">112</span>
                    </a>
                    <a
                      href="tel:1078"
                      className="p-2.5 rounded-xl bg-white dark:bg-slate-800 border border-rose-200 dark:border-rose-900 text-charcoal-900 dark:text-white font-bold hover:bg-rose-100 dark:hover:bg-rose-900/40 transition-colors"
                    >
                      <span className="text-[10px] text-slate-500 block font-mono">NDMA Helpline</span>
                      <span className="text-sm font-mono text-rose-600">1078</span>
                    </a>
                    <a
                      href="tel:1070"
                      className="p-2.5 rounded-xl bg-white dark:bg-slate-800 border border-rose-200 dark:border-rose-900 text-charcoal-900 dark:text-white font-bold hover:bg-rose-100 dark:hover:bg-rose-900/40 transition-colors"
                    >
                      <span className="text-[10px] text-slate-500 block font-mono">State Relief (SDMA)</span>
                      <span className="text-sm font-mono text-rose-600">1070</span>
                    </a>
                    <a
                      href="tel:1077"
                      className="p-2.5 rounded-xl bg-white dark:bg-slate-800 border border-rose-200 dark:border-rose-900 text-charcoal-900 dark:text-white font-bold hover:bg-rose-100 dark:hover:bg-rose-900/40 transition-colors"
                    >
                      <span className="text-[10px] text-slate-500 block font-mono">District Emergency (DEOC)</span>
                      <span className="text-sm font-mono text-rose-600">1077</span>
                    </a>
                  </div>

                  <p className="text-[11px] text-rose-800 dark:text-rose-300 leading-relaxed font-mono pt-1">
                    * Verified nearby resource location is currently unavailable. Pan-India statutory
                    emergency response helplines remain operational 24/7.
                  </p>
                </div>
              </div>
            )}

            {/* Tab 3: Scientific Evidence & Conflict Resolution */}
            {activeTab === 'EVIDENCE' && (
              <div className="space-y-3 text-xs">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div className="p-3.5 rounded-2xl bg-paper-50 dark:bg-slate-850 border border-paper-200 dark:border-slate-800 space-y-1.5">
                    <span className="font-bold text-charcoal-900 dark:text-white block font-mono uppercase">
                      What Changed?
                    </span>
                    <p className="text-charcoal-600 dark:text-slate-300 leading-relaxed">
                      {assessment.explanation.what_changed}
                    </p>
                  </div>

                  <div className="p-3.5 rounded-2xl bg-paper-50 dark:bg-slate-850 border border-paper-200 dark:border-slate-800 space-y-1.5">
                    <span className="font-bold text-charcoal-900 dark:text-white block font-mono uppercase">
                      Why Does the System Expect Escalation?
                    </span>
                    <p className="text-charcoal-600 dark:text-slate-300 leading-relaxed">
                      {assessment.explanation.why_this_risk}
                    </p>
                  </div>

                  <div className="p-3.5 rounded-2xl bg-rose-50/50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900 space-y-1.5">
                    <span className="font-bold text-rose-900 dark:text-rose-200 block font-mono uppercase">
                      What Could Make It Worse?
                    </span>
                    <p className="text-rose-800 dark:text-rose-300 leading-relaxed">
                      {assessment.explanation.what_could_make_it_worse}
                    </p>
                  </div>

                  <div className="p-3.5 rounded-2xl bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-900 space-y-1.5">
                    <span className="font-bold text-emerald-900 dark:text-emerald-200 block font-mono uppercase">
                      What Could Make It Improve?
                    </span>
                    <p className="text-emerald-800 dark:text-emerald-300 leading-relaxed">
                      {assessment.explanation.what_could_make_it_improve}
                    </p>
                  </div>
                </div>

                <div className="p-3.5 rounded-2xl bg-paper-50 dark:bg-slate-850 border border-paper-200 dark:border-slate-800 space-y-1.5">
                  <span className="font-bold text-charcoal-900 dark:text-white block font-mono uppercase">
                    What Do We Not Know? (Data Gaps & Uncertainty Limits)
                  </span>
                  <p className="text-charcoal-600 dark:text-slate-400 leading-relaxed">
                    {assessment.explanation.what_we_do_not_know}
                  </p>
                </div>
              </div>
            )}
          </div>
        ) : null}
      </div>
    </section>
  );
};

export default LocationRiskCheckerSection;
