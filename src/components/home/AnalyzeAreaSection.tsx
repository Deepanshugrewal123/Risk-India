import React, { useState, useRef, useEffect } from 'react';
import { DisasterType } from '../../types/risk';
import { riskService, AreaAnalysisResult } from '../../services/riskService';
import { ALL_INDIAN_STATES, ALL_INDIAN_UNION_TERRITORIES } from '../../data/indiaLocations';
import { AdministrativeType, IndiaLocation } from '../../types/location';
import { RiskBadge } from '../common/RiskBadge';
import { DemoBadge } from '../common/DemoBadge';
import { MagneticButton } from '../common/MagneticButton';
import { RiskExplanation } from '../common/RiskExplanation';
import { LoadingState } from '../common/LoadingState';
import { ErrorState } from '../common/ErrorState';
import { EmptyState } from '../common/EmptyState';
import {
  Search,
  Loader2,
  Sparkles,
  AlertCircle,
  ShieldCheck,
  ChevronDown,
  X,
  MapPin,
  Check
} from 'lucide-react';

export const AnalyzeAreaSection: React.FC = () => {
  // Master Location Selection State
  const [selectedLocation, setSelectedLocation] = useState<IndiaLocation>(() => ALL_INDIAN_STATES[2]); // Default Assam
  const [selectedDistrict, setSelectedDistrict] = useState<string>('Udalguri');
  const [selectedDisaster, setSelectedDisaster] = useState<DisasterType>('Flood');

  // Search & Filter State for Location Dropdown
  const [isDropdownOpen, setIsDropdownOpen] = useState<boolean>(false);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [typeFilter, setTypeFilter] = useState<'ALL' | AdministrativeType>('ALL');
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Analysis Result State
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AreaAnalysisResult | null>(() => ({
    id: 'assessment-assam-initial',
    location: { state: 'Assam', district: 'Guwahati (Kamrup Metro)' },
    state: 'Assam',
    district: 'Guwahati (Kamrup Metro)',
    locationType: 'STATE',
    disasterType: 'Flood',
    riskScore: 84,
    riskLevel: 'HIGH',
    confidenceScore: 92,
    factors: [
      { name: 'Heavy Catchment Rainfall', impact: 'High', value: 88, importance: 0.35, description: 'Heavy monsoon precipitation in upper watershed catchment (+38% above median)' },
      { name: 'Riverbed Siltation & Water Influx', impact: 'High', value: 84, importance: 0.28, description: 'Brahmaputra discharge benchmark crossing alert mark by +1.2m' },
      { name: 'Historical Flood Exposure', impact: 'High', value: 80, importance: 0.22, description: 'Recurrent seasonal inundation documented across lower valley' },
      { name: 'Low-Lying Valley Retention', impact: 'Medium', value: 74, importance: 0.15, description: 'Basin topography with prolonged natural drainage retention' },
    ],
    primaryDriver: 'Heavy Catchment Rainfall',
    recommendedActions: ['Pre-position motorized inflatable rescue boats in low-lying char areas', 'Stock 72-hour dry rations and oral rehydration salts'],
    recommendedImmediateAction: 'Pre-position motorized inflatable rescue boats in low-lying char areas and monitor ASDMA river stage updates.',
    historicalIncidentFrequency: '4 major flood occurrences in past 10 years',
    predictedPeakTimeWindow: 'Next 24 to 48 Hours',
    modelVersion: 'v1.4.0-demo',
    timestamp: new Date().toISOString(),
    isDemoData: true,
    isSimulated: true,
  }));

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Filtered States and UTs according to search query and type filter
  const cleanQuery = searchQuery.toLowerCase().trim();

  const filteredStates = ALL_INDIAN_STATES.filter((s) => {
    if (typeFilter === 'UNION_TERRITORY') return false;
    if (!cleanQuery) return true;
    return (
      s.name.toLowerCase().includes(cleanQuery) ||
      s.code.toLowerCase().includes(cleanQuery) ||
      s.capital.toLowerCase().includes(cleanQuery) ||
      s.districts.some((d) => d.toLowerCase().includes(cleanQuery))
    );
  });

  const filteredUTs = ALL_INDIAN_UNION_TERRITORIES.filter((u) => {
    if (typeFilter === 'STATE') return false;
    if (!cleanQuery) return true;
    return (
      u.name.toLowerCase().includes(cleanQuery) ||
      u.code.toLowerCase().includes(cleanQuery) ||
      u.capital.toLowerCase().includes(cleanQuery) ||
      u.districts.some((d) => d.toLowerCase().includes(cleanQuery)) ||
      (cleanQuery.includes('dadra') && u.id.includes('dadra')) ||
      (cleanQuery.includes('daman') && u.id.includes('daman'))
    );
  });

  const totalFilteredCount = filteredStates.length + filteredUTs.length;

  // Handle Location Selection
  const handleSelectLocation = (loc: IndiaLocation) => {
    setSelectedLocation(loc);
    setIsDropdownOpen(false);
    setSearchQuery('');
    // Reset district to first available district of selected location
    if (loc.districts.length > 0) {
      setSelectedDistrict(loc.districts[0]);
    }
  };

  // Perform Analysis
  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    setAnalysisError(null);
    try {
      const result = await riskService.analyzeAreaRisk(
        selectedLocation.name,
        selectedDistrict,
        selectedDisaster
      );
      setAnalysisResult(result);
    } catch (err) {
      console.error('Risk analysis failed:', err);
      setAnalysisError('Unable to calculate estimated risk for the selected location. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const disasterOptions: DisasterType[] = ['Flood', 'Landslide', 'Cyclone', 'Earthquake', 'Heatwave', 'Drought'];

  return (
    <section id="analyze-section" className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      {/* Section Header */}
      <div className="text-center max-w-3xl mx-auto mb-12">
        <div className="inline-flex items-center gap-2 mb-3">
          <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold">
            Predictive Risk Assessment
          </span>
          <DemoBadge label="AI RISK ENGINE" />
        </div>
        <h2 className="text-3xl sm:text-5xl font-bold tracking-tight text-charcoal-950 mb-4">
          What Is Your Area's Risk?
        </h2>
        <p className="text-sm sm:text-base text-charcoal-600 max-w-xl mx-auto leading-relaxed">
          Comprehensive multi-hazard intelligence covering all 28 States and 9 Union Territories. Explore localized terrain vulnerability, precipitation anomalies, and historical recurrence benchmarks.
        </p>
      </div>

      {/* Main Analysis Card Container with Editorial Styling */}
      <div className="rounded-3xl bg-white border border-paper-300 shadow-floating overflow-visible">
        {/* Form Inputs Header */}
        <div className="p-6 sm:p-8 bg-paper-50/70 border-b border-paper-200 rounded-t-3xl">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
            {/* 01 // Searchable State / UT Selector */}
            <div className="relative" ref={dropdownRef}>
              <div className="flex items-center justify-between mb-2">
                <label className="block text-xs font-mono uppercase tracking-wider text-charcoal-600 font-semibold">
                  01 // State / Union Territory
                </label>
                <span className="text-[10px] font-mono text-charcoal-500">
                  {selectedLocation.type === 'UNION_TERRITORY' ? 'Union Territory' : 'State'} ({selectedLocation.code})
                </span>
              </div>

              {/* Selector Trigger Button */}
              <button
                type="button"
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                className="w-full px-4 py-3 rounded-xl bg-white border border-paper-300 text-charcoal-900 text-sm flex items-center justify-between hover:border-charcoal-400 focus:outline-none focus:ring-2 focus:ring-charcoal-900 transition-all font-medium text-left shadow-xs"
              >
                <div className="flex items-center gap-2.5 truncate">
                  <MapPin className="w-4 h-4 text-charcoal-500 shrink-0" />
                  <span className="truncate font-semibold text-charcoal-950">{selectedLocation.name}</span>
                  <span className="text-[10px] font-mono uppercase px-1.5 py-0.5 rounded bg-paper-100 text-charcoal-600 shrink-0">
                    {selectedLocation.type === 'UNION_TERRITORY' ? 'UT' : 'State'}
                  </span>
                </div>
                <ChevronDown className={`w-4 h-4 text-charcoal-500 transition-transform shrink-0 ${isDropdownOpen ? 'rotate-180' : ''}`} />
              </button>

              {/* Dropdown Menu Modal */}
              {isDropdownOpen && (
                <div className="absolute z-50 left-0 right-0 mt-2 rounded-2xl bg-white border border-paper-300 shadow-floating overflow-hidden animate-in fade-in zoom-in-95 duration-150">
                  {/* Search and Filter Header */}
                  <div className="p-3 bg-paper-50 border-b border-paper-200 space-y-2.5">
                    <div className="relative">
                      <Search className="w-4 h-4 text-charcoal-400 absolute left-3 top-1/2 -translate-y-1/2" />
                      <input
                        type="text"
                        placeholder="Type to search (e.g. ass, del, ladakh)..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        autoFocus
                        className="w-full pl-9 pr-8 py-2 rounded-lg bg-white border border-paper-300 text-xs font-mono text-charcoal-900 focus:outline-none focus:ring-2 focus:ring-charcoal-900 transition-all placeholder:text-charcoal-400"
                      />
                      {searchQuery && (
                        <button
                          onClick={() => setSearchQuery('')}
                          className="absolute right-2.5 top-1/2 -translate-y-1/2 text-charcoal-400 hover:text-charcoal-700"
                        >
                          <X className="w-3.5 h-3.5" />
                        </button>
                      )}
                    </div>

                    {/* Filter Type Pills */}
                    <div className="flex items-center gap-1.5 text-[11px] font-mono">
                      <button
                        type="button"
                        onClick={() => setTypeFilter('ALL')}
                        className={`px-2.5 py-1 rounded-full transition-all ${
                          typeFilter === 'ALL'
                            ? 'bg-charcoal-900 text-white font-bold'
                            : 'bg-white text-charcoal-600 hover:bg-paper-200 border border-paper-300'
                        }`}
                      >
                        All (37)
                      </button>
                      <button
                        type="button"
                        onClick={() => setTypeFilter('STATE')}
                        className={`px-2.5 py-1 rounded-full transition-all ${
                          typeFilter === 'STATE'
                            ? 'bg-charcoal-900 text-white font-bold'
                            : 'bg-white text-charcoal-600 hover:bg-paper-200 border border-paper-300'
                        }`}
                      >
                        States (28)
                      </button>
                      <button
                        type="button"
                        onClick={() => setTypeFilter('UNION_TERRITORY')}
                        className={`px-2.5 py-1 rounded-full transition-all ${
                          typeFilter === 'UNION_TERRITORY'
                            ? 'bg-charcoal-900 text-white font-bold'
                            : 'bg-white text-charcoal-600 hover:bg-paper-200 border border-paper-300'
                        }`}
                      >
                        Union Territories (9)
                      </button>
                    </div>
                  </div>

                  {/* List of Locations (Grouped) */}
                  <div className="max-h-64 overflow-y-auto divide-y divide-paper-100">
                    {totalFilteredCount === 0 ? (
                      <div className="p-6 text-center text-xs font-mono text-charcoal-500">
                        No matching location found.
                      </div>
                    ) : (
                      <>
                        {/* Group: STATES */}
                        {filteredStates.length > 0 && (
                          <div>
                            <div className="px-3.5 py-1.5 bg-paper-100/60 text-[10px] font-mono uppercase tracking-wider text-charcoal-600 font-bold sticky top-0 z-10 flex items-center justify-between">
                              <span>States ({filteredStates.length})</span>
                              <span className="text-charcoal-400">28 Total</span>
                            </div>
                            <div className="p-1">
                              {filteredStates.map((s) => {
                                const isSelected = selectedLocation.id === s.id;
                                return (
                                  <button
                                    key={s.id}
                                    type="button"
                                    onClick={() => handleSelectLocation(s)}
                                    className={`w-full px-3 py-2 rounded-lg text-left text-xs flex items-center justify-between transition-colors ${
                                      isSelected
                                        ? 'bg-paper-200/80 text-charcoal-950 font-bold'
                                        : 'hover:bg-paper-100 text-charcoal-800'
                                    }`}
                                  >
                                    <span className="truncate">{s.name}</span>
                                    <div className="flex items-center gap-2">
                                      <span className="font-mono text-[10px] text-charcoal-400">{s.code}</span>
                                      {isSelected && <Check className="w-3.5 h-3.5 text-charcoal-900" />}
                                    </div>
                                  </button>
                                );
                              })}
                            </div>
                          </div>
                        )}

                        {/* Group: UNION TERRITORIES */}
                        {filteredUTs.length > 0 && (
                          <div>
                            <div className="px-3.5 py-1.5 bg-paper-100/60 text-[10px] font-mono uppercase tracking-wider text-charcoal-600 font-bold sticky top-0 z-10 flex items-center justify-between">
                              <span>Union Territories ({filteredUTs.length})</span>
                              <span className="text-charcoal-400">9 Total</span>
                            </div>
                            <div className="p-1">
                              {filteredUTs.map((u) => {
                                const isSelected = selectedLocation.id === u.id;
                                return (
                                  <button
                                    key={u.id}
                                    type="button"
                                    onClick={() => handleSelectLocation(u)}
                                    className={`w-full px-3 py-2 rounded-lg text-left text-xs flex items-center justify-between transition-colors ${
                                      isSelected
                                        ? 'bg-paper-200/80 text-charcoal-950 font-bold'
                                        : 'hover:bg-paper-100 text-charcoal-800'
                                    }`}
                                  >
                                    <span className="truncate">{u.name}</span>
                                    <div className="flex items-center gap-2">
                                      <span className="font-mono text-[10px] text-charcoal-400">{u.code}</span>
                                      {isSelected && <Check className="w-3.5 h-3.5 text-charcoal-900" />}
                                    </div>
                                  </button>
                                );
                              })}
                            </div>
                          </div>
                        )}
                      </>
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* 02 // District / City Select */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="block text-xs font-mono uppercase tracking-wider text-charcoal-600 font-semibold">
                  02 // District / City
                </label>
                <span className="text-[10px] font-mono text-charcoal-500">
                  {selectedLocation.districts.length} Options
                </span>
              </div>
              <select
                value={selectedDistrict}
                onChange={(e) => setSelectedDistrict(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-white border border-paper-300 text-charcoal-900 text-sm focus:outline-none focus:ring-2 focus:ring-charcoal-900 transition-shadow font-medium"
              >
                {selectedLocation.districts.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </select>
            </div>

            {/* 03 // Hazard Category Select */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="block text-xs font-mono uppercase tracking-wider text-charcoal-600 font-semibold">
                  03 // Hazard Category
                </label>
                <span className="text-[10px] font-mono text-charcoal-500">
                  Primary: {selectedLocation.primaryRisk || 'Flood'}
                </span>
              </div>
              <select
                value={selectedDisaster}
                onChange={(e) => setSelectedDisaster(e.target.value as DisasterType)}
                className="w-full px-4 py-3 rounded-xl bg-white border border-paper-300 text-charcoal-900 text-sm focus:outline-none focus:ring-2 focus:ring-charcoal-900 transition-shadow font-medium"
              >
                {disasterOptions.map((type) => (
                  <option key={type} value={type}>
                    {type} Risk
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Action Button & Disclaimer Bar */}
          <div className="mt-6 flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-paper-200">
            <div className="flex items-center gap-2 text-xs text-charcoal-500 font-mono">
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
              <span>Full India Coverage // 28 States + 9 Union Territories Active</span>
            </div>
            <MagneticButton
              variant="primary"
              size="md"
              onClick={handleAnalyze}
              disabled={isAnalyzing}
              className="w-full sm:w-auto"
            >
              {isAnalyzing ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Calculating Estimated Risk...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4 text-amber-300" />
                  <span>Analyze Risk</span>
                </>
              )}
            </MagneticButton>
          </div>
        </div>

        {/* Results Area */}
        <div className="p-6 sm:p-10">
          {isAnalyzing ? (
            <LoadingState
              message="Calculating Estimated Risk..."
              description="Synthesizing regional terrain models, precipitation anomalies, and historical recurrence benchmarks..."
              heightClass="min-h-[300px]"
            />
          ) : analysisError ? (
            <ErrorState
              title="Unable to Calculate Risk"
              message={analysisError}
              onRetry={handleAnalyze}
              retryLabel="Recalculate Risk"
            />
          ) : analysisResult ? (
            <div className="space-y-8 animate-in fade-in duration-300">
              {/* Scope Boundary Alert */}
              {analysisResult.status === 'model_scope_limited' ? (
                <div className="p-8 rounded-3xl bg-amber-50/70 border border-amber-200/90 shadow-xs space-y-5">
                  <div className="flex items-start gap-4">
                    <div className="p-3 rounded-2xl bg-amber-100 text-amber-900 shrink-0 mt-1">
                      <AlertCircle className="w-6 h-6 text-amber-700" />
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="font-mono text-xs font-bold uppercase tracking-wider text-amber-900">
                          Geographic Scope Boundary
                        </span>
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-200/80 text-amber-950 border border-amber-300">
                          ASSAM PROTOTYPE ONLY
                        </span>
                      </div>
                      <h3 className="text-xl sm:text-2xl font-bold tracking-tight text-amber-950">
                        The current flood ML prototype is limited to selected Assam monitoring areas.
                      </h3>
                      <p className="text-sm text-amber-900/90 leading-relaxed max-w-2xl">
                        This research prototype was trained and audited strictly on Central Water Commission (CWC) telemetry and ISRO/NRSC Bhuvan flood rasters for Assam river monitoring gauges (Udalguri, Darrang, Kamrup). In compliance with scientific integrity and safety guidelines, unverified predictions are not generated for non-Assam regions.
                      </p>
                    </div>
                  </div>

                  <div className="p-4 rounded-2xl bg-white/80 border border-amber-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                    <div className="text-xs text-amber-950">
                      <span className="font-bold">Audited Basins:</span> Udalguri (Dhansirighat), Darrang (Tangni), Kamrup (Boko)
                    </div>
                    <button
                      type="button"
                      onClick={() => {
                        const assamLoc = ALL_INDIAN_STATES.find((s) => s.name.toLowerCase() === 'assam') || ALL_INDIAN_STATES[2];
                        setSelectedLocation(assamLoc);
                        setSelectedDistrict('Udalguri');
                        setSelectedDisaster('Flood');
                        setIsAnalyzing(true);
                        riskService.analyzeAreaRisk('Assam', 'Udalguri', 'Flood').then((res) => {
                          setAnalysisResult(res);
                          setIsAnalyzing(false);
                        });
                      }}
                      className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-charcoal-900 hover:bg-charcoal-950 text-white text-xs font-medium transition-colors shadow-xs"
                    >
                      <Sparkles className="w-3.5 h-3.5 text-amber-300" />
                      <span>Switch to Assam Basin (Udalguri)</span>
                    </button>
                  </div>
                </div>
              ) : analysisResult.status === 'insufficient_data' ? (
                <div className="p-8 rounded-3xl bg-amber-50/70 border border-amber-200/90 shadow-xs space-y-4">
                  <div className="flex items-start gap-4">
                    <div className="p-3 rounded-2xl bg-amber-100 text-amber-900 shrink-0 mt-1">
                      <AlertCircle className="w-6 h-6 text-amber-700" />
                    </div>
                    <div className="space-y-2">
                      <span className="font-mono text-xs font-bold uppercase tracking-wider text-amber-900">
                        Data Integrity Requirement
                      </span>
                      <h3 className="text-xl sm:text-2xl font-bold tracking-tight text-amber-950">
                        Insufficient environmental data available for this prototype analysis.
                      </h3>
                      <p className="text-sm text-amber-900/90 leading-relaxed max-w-2xl">
                        The prototype model requires antecedent rainfall and river stage observations from official CWC monitoring gauges. Predictions are disabled when telemetry is absent to prevent fabricated outputs.
                      </p>
                    </div>
                  </div>
                </div>
              ) : (
                <>
                  {/* Header result row */}
                  <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-6 border-b border-paper-200">
                    <div>
                      <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                        <span className="font-mono text-xs uppercase tracking-wider text-charcoal-500">
                          {analysisResult.isPrototype ? 'ML Prototype Assessment' : 'Estimated Risk Evaluation'}
                        </span>
                        {analysisResult.isPrototype && (
                          <span className="px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold bg-amber-100 text-amber-900 border border-amber-300">
                            ASSAM FLOOD PROTOTYPE V1 // RESEARCH ONLY
                          </span>
                        )}
                      </div>
                      <h3 className="text-2xl sm:text-3xl font-bold uppercase tracking-tight text-charcoal-950">
                        {analysisResult.district}, {analysisResult.state}
                      </h3>
                      <p className="text-sm text-charcoal-600 mt-0.5 flex items-center gap-2">
                        <span>
                          Target Hazard: <span className="font-semibold text-charcoal-900">{analysisResult.disasterType} Risk</span>
                        </span>
                        <span className="text-charcoal-300">•</span>
                        <span className="font-mono text-xs text-charcoal-500">
                          {selectedLocation.type === 'UNION_TERRITORY' ? 'Union Territory' : 'State'} of {selectedLocation.region || 'India'}
                        </span>
                      </p>
                    </div>

                    <div className="flex items-center gap-6">
                      {analysisResult.floodProbability !== undefined && (
                        <div className="text-right hidden sm:block">
                          <div className="text-[11px] font-mono text-charcoal-500">Model Probability</div>
                          <div className="text-2xl font-bold font-mono text-charcoal-700">
                            {(analysisResult.floodProbability * 100).toFixed(1)}%
                          </div>
                        </div>
                      )}
                      <div className="text-right">
                        <div className="text-xs font-mono text-charcoal-500">UI Risk Score</div>
                        <div className="text-4xl font-extrabold font-mono text-charcoal-950">
                          {analysisResult.riskScore}%
                        </div>
                      </div>
                      <RiskBadge level={analysisResult.riskLevel} size="lg" />
                    </div>
                  </div>

                  {/* Mandatory Experimental Prototype Disclaimer Banner */}
                  <div className="p-4 rounded-2xl bg-amber-50/80 border border-amber-200/90 flex items-center gap-3 text-xs text-amber-950 leading-relaxed shadow-xs">
                    <AlertCircle className="w-5 h-5 text-amber-600 shrink-0" />
                    <p className="font-medium">
                      {analysisResult.disclaimer ||
                        'Experimental Assam flood-risk prototype based on a limited event dataset. Results are for research and awareness only and should not replace official emergency warnings.'}
                    </p>
                  </div>

                  {/* Dynamic Top Factors ("Why this risk?") */}
                  {analysisResult.topFactors && analysisResult.topFactors.length > 0 && (
                    <div className="p-6 sm:p-7 rounded-3xl bg-paper-50/80 border border-paper-200 space-y-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <span className="font-mono text-[11px] font-bold uppercase tracking-wider text-charcoal-500 block">
                            Model Explainability // Feature Contribution
                          </span>
                          <h4 className="text-base sm:text-lg font-bold text-charcoal-950">
                            Why this risk score?
                          </h4>
                        </div>
                        <span className="text-xs font-mono text-charcoal-500 bg-white px-2.5 py-1 rounded-lg border border-paper-200">
                          Top 4 Linear Drivers
                        </span>
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                        {analysisResult.topFactors.map((factor, idx) => {
                          const isIncrease = factor.direction === 'increases_risk';
                          return (
                            <div
                              key={idx}
                              className="p-4 rounded-2xl bg-white border border-paper-200 shadow-xs flex items-center justify-between gap-3"
                            >
                              <div className="space-y-1 truncate">
                                <div className="text-xs font-bold text-charcoal-900 truncate">
                                  {factor.display_label}
                                </div>
                                <div className="flex items-center gap-2">
                                  <span className="text-[11px] font-mono text-charcoal-600 bg-paper-100 px-2 py-0.5 rounded">
                                    {factor.value || 'Telemetry Input'}
                                  </span>
                                </div>
                              </div>
                              <div className="text-right shrink-0">
                                <span
                                  className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-mono font-bold ${
                                    isIncrease
                                      ? 'bg-rose-50 text-rose-700 border border-rose-200'
                                      : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                                  }`}
                                >
                                  {isIncrease ? 'Increases Risk' : 'Decreases Risk'}
                                </span>
                                <div className="text-[10px] font-mono text-charcoal-500 mt-1">
                                  weight {factor.contribution > 0 ? '+' : ''}
                                  {factor.contribution.toFixed(2)}
                                </div>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  )}

                  {/* Standard RiskExplanation Component (Preserved) */}
                  <RiskExplanation
                    locationName={`${analysisResult.district}, ${analysisResult.state}`}
                    disasterType={analysisResult.disasterType}
                    riskScore={analysisResult.riskScore}
                    factors={analysisResult.factors.map((f) => ({
                      name: f.name,
                      weight: typeof f.value === 'number' ? f.value : f.weight || 70,
                      category: f.impact === 'High' ? 'Environmental' : 'Topographical',
                      description: f.description || '',
                    }))}
                    explanationNarrative={`The estimated ${analysisResult.riskScore}% ${analysisResult.disasterType.toLowerCase()} risk for ${analysisResult.district} (${analysisResult.state}) is primarily driven by ${(analysisResult.primaryDriver || 'regional environmental anomalies').toLowerCase()}. Model signals indicate compound saturation factors and historical recurrence patterns (${analysisResult.historicalIncidentFrequency || 'regional exposure index'}).`}
                  />

                  {/* Recommended Actionable Guidance */}
                  <div className="p-5 rounded-2xl bg-paper-100/70 border border-paper-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                    <div className="flex items-start gap-3">
                      <div className="p-2 rounded-xl bg-white border border-paper-200 text-charcoal-800 shrink-0 mt-0.5">
                        <ShieldCheck className="w-5 h-5 text-risk-low-soft" />
                      </div>
                      <div>
                        <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-bold block">
                          Recommended Preparedness Action
                        </span>
                        <p className="text-xs text-charcoal-800 font-medium mt-0.5">
                          {analysisResult.recommendedImmediateAction}
                        </p>
                      </div>
                    </div>
                    <div className="text-xs font-mono text-charcoal-500 shrink-0">
                      Forecast Window: <span className="font-semibold text-charcoal-800">{analysisResult.predictedPeakTimeWindow}</span>
                    </div>
                  </div>
                </>
              )}
            </div>
          ) : (
            <EmptyState
              title="No Area Selected"
              description="Select your State or Union Territory, District, and Hazard category above and click 'Analyze Risk' to generate an estimated risk breakdown."
              icon={<Search className="w-5 h-5 text-charcoal-400" />}
            />
          )}
        </div>
      </div>
    </section>
  );
};
