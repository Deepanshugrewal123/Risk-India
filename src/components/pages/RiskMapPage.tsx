import React, { useState, useEffect } from 'react';
import { IndiaRiskMap } from '../map/IndiaRiskMap';
import { RegionRiskData, DisasterType, RiskLevel } from '../../types/risk';
import { DisasterEvent } from '../../types/disaster';
import { AdministrativeType } from '../../types/location';
import { ALL_INDIAN_LOCATIONS } from '../../data/indiaLocations';
import { riskService } from '../../services/riskService';
import { RiskBadge } from '../common/RiskBadge';
import { DemoBadge } from '../common/DemoBadge';
import { LoadingState } from '../common/LoadingState';
import { ErrorState } from '../common/ErrorState';
import { EmptyState } from '../common/EmptyState';
import { Search, ShieldCheck, MapPin, Phone, AlertCircle, Clock, Globe } from 'lucide-react';
import { NationalFutureRisk } from '../predictive/NationalFutureRisk';

interface RiskMapPageProps {
  onSelectIncident?: (incident: DisasterEvent) => void;
}

export const RiskMapPage: React.FC<RiskMapPageProps> = ({ onSelectIncident }) => {
  const [viewMode, setViewMode] = useState<'current' | 'future'>('future');
  const [allRegions, setAllRegions] = useState<RegionRiskData[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [selectedLocationType, setSelectedLocationType] = useState<'ALL' | AdministrativeType>('ALL');
  const [selectedHazard, setSelectedHazard] = useState<string>('All');
  const [selectedSeverity, setSelectedSeverity] = useState<RiskLevel | 'All'>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedRegion, setSelectedRegion] = useState<RegionRiskData | null>(null);

  const fetchRegions = async () => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      const data = await riskService.getAllRegions();
      setAllRegions(data);
      if (data.length > 0) {
        setSelectedRegion(data[0]);
      }
    } catch (err) {
      console.error('Failed to load regions:', err);
      setErrorMessage('Unable to load geospatial risk dataset from the risk service.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchRegions();
  }, []);

  const hazards: (DisasterType | 'All')[] = ['All', 'Flood', 'Landslide', 'Cyclone', 'Earthquake', 'Heatwave', 'Drought'];
  const severities: (RiskLevel | 'All')[] = ['All', 'LOW', 'MODERATE', 'HIGH', 'CRITICAL'];

  // Filter regions by search query and filters
  const filteredRegions = allRegions.filter((r) => {
    const locMeta = ALL_INDIAN_LOCATIONS.find((l) => l.id === r.id || l.code === r.code);
    const matchesType = selectedLocationType === 'ALL' || locMeta?.type === selectedLocationType;
    const matchesSearch =
      r.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      r.code.toLowerCase().includes(searchQuery.toLowerCase()) ||
      r.primaryRisk.toLowerCase().includes(searchQuery.toLowerCase()) ||
      r.capital.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesHazard = selectedHazard === 'All' || r.primaryRisk.toLowerCase() === selectedHazard.toLowerCase();
    const matchesSeverity = selectedSeverity === 'All' || r.riskLevel === selectedSeverity;
    return matchesType && matchesSearch && matchesHazard && matchesSeverity;
  });

  return (
    <div className="pt-28 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto min-h-screen">
      {/* Page Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold">
                Geospatial Intelligence Explorer
              </span>
              <DemoBadge label="36 REGIONS MONITORED" />
            </div>
            <h1 className="text-3xl sm:text-5xl font-bold tracking-tight text-charcoal-950">
              {viewMode === 'future' ? 'Predictive Risk & Early Warning' : 'India Disaster Risk Map'}
            </h1>
            <p className="text-sm sm:text-base text-charcoal-600 mt-2 max-w-2xl">
              {viewMode === 'future'
                ? 'Authoritative national predictive risk fusion, 5-horizon NWP forecasting, qualitative uncertainty, scenarios, and citizen safety action intelligence.'
                : 'Multi-hazard vulnerability modeling across all 28 States and 8 Union Territories, synthesizing topography, river discharge, and satellite moisture indices.'}
            </p>
          </div>

          <div className="flex items-center p-1 rounded-2xl bg-paper-200 border border-paper-300 font-mono text-xs">
            <button
              onClick={() => setViewMode('future')}
              className={`flex items-center gap-1.5 px-4 py-2 rounded-xl font-bold transition-all ${
                viewMode === 'future'
                  ? 'bg-charcoal-900 text-white shadow-sm'
                  : 'text-charcoal-600 hover:text-charcoal-950'
              }`}
            >
              <Clock className="w-4 h-4 text-indigo-400" />
              <span>FUTURE RISK & EARLY WARNING</span>
            </button>
            <button
              onClick={() => setViewMode('current')}
              className={`flex items-center gap-1.5 px-4 py-2 rounded-xl font-bold transition-all ${
                viewMode === 'current'
                  ? 'bg-charcoal-900 text-white shadow-sm'
                  : 'text-charcoal-600 hover:text-charcoal-950'
              }`}
            >
              <Globe className="w-4 h-4" />
              <span>CURRENT RISK</span>
            </button>
          </div>
        </div>
      </div>

      {viewMode === 'future' ? (
        <NationalFutureRisk />
      ) : (
        <>
          {/* Filter and Search Bar */}
          <div className="p-4 sm:p-5 rounded-3xl bg-white border border-paper-300 shadow-subtle mb-8 space-y-4">
            <div className="flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-4">
          {/* Search box */}
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-charcoal-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search state, UT, code (e.g. Assam, Delhi, Ladakh, KL), or hazard..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-paper-50 border border-paper-300 text-xs font-mono text-charcoal-900 focus:outline-none focus:ring-2 focus:ring-charcoal-900 transition-shadow"
            />
          </div>

          <div className="flex flex-wrap items-center gap-3">
            {/* Location Type Filter */}
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono text-charcoal-500 shrink-0">Scope:</span>
              <select
                value={selectedLocationType}
                onChange={(e) => setSelectedLocationType(e.target.value as 'ALL' | AdministrativeType)}
                className="px-3 py-2 rounded-xl bg-paper-50 border border-paper-300 text-xs font-mono text-charcoal-800 font-medium focus:outline-none focus:ring-2 focus:ring-charcoal-900"
              >
                <option value="ALL">All India (37)</option>
                <option value="STATE">States Only (28)</option>
                <option value="UNION_TERRITORY">Union Territories (9)</option>
              </select>
            </div>

            {/* Hazard Dropdown */}
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono text-charcoal-500 shrink-0">Hazard:</span>
              <select
                value={selectedHazard}
                onChange={(e) => setSelectedHazard(e.target.value)}
                className="px-3 py-2 rounded-xl bg-paper-50 border border-paper-300 text-xs font-mono text-charcoal-800 font-medium focus:outline-none focus:ring-2 focus:ring-charcoal-900"
              >
                {hazards.map((h) => (
                  <option key={h} value={h}>
                    {h === 'All' ? 'All Hazards' : `${h} Only`}
                  </option>
                ))}
              </select>
            </div>

            {/* Severity Dropdown */}
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono text-charcoal-500 shrink-0">Severity:</span>
              <select
                value={selectedSeverity}
                onChange={(e) => setSelectedSeverity(e.target.value as RiskLevel | 'All')}
                className="px-3 py-2 rounded-xl bg-paper-50 border border-paper-300 text-xs font-mono text-charcoal-800 font-medium focus:outline-none focus:ring-2 focus:ring-charcoal-900"
              >
                {severities.map((s) => (
                  <option key={s} value={s}>
                    {s === 'All' ? 'All Severities' : `${s} Risk`}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>

      {isLoading ? (
        <LoadingState
          message="Loading Geospatial Risk Matrix..."
          description="Fetching regional hazard evaluations and historical exposure trends for all 37 locations..."
          heightClass="min-h-[480px]"
        />
      ) : errorMessage ? (
        <ErrorState
          title="Unable to Load Map Data"
          message={errorMessage}
          onRetry={fetchRegions}
          retryLabel="Reload Dataset"
        />
      ) : (
        /* Main Layout: Interactive Map + Side Inspector */
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Map Column */}
          <div className="lg:col-span-8">
            <IndiaRiskMap
              onSelectRegion={(reg) => setSelectedRegion(reg)}
              onSelectIncident={onSelectIncident}
              selectedRegionId={selectedRegion?.id}
              filterHazard={selectedHazard === 'All' ? undefined : selectedHazard}
              filterRiskLevel={selectedSeverity}
              filterLocationType={selectedLocationType}
            />
          </div>

          {/* Side Inspector Column */}
          <div className="lg:col-span-4 space-y-6">
            {selectedRegion ? (
              <div className="rounded-3xl bg-white border border-paper-300 p-6 shadow-subtle space-y-6 sticky top-28">
                {/* Region Header */}
                <div className="border-b border-paper-200 pb-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-mono text-charcoal-400">
                      {ALL_INDIAN_LOCATIONS.find((l) => l.id === selectedRegion.id)?.type === 'UNION_TERRITORY'
                        ? 'UNION TERRITORY'
                        : 'STATE'}{' '}
                      INSPECTOR // {selectedRegion.code}
                    </span>
                    <RiskBadge level={selectedRegion.riskLevel} size="sm" score={selectedRegion.riskScore} />
                  </div>
                  <h2 className="text-2xl font-bold text-charcoal-950">{selectedRegion.name}</h2>
                  <p className="text-xs text-charcoal-500 font-mono mt-0.5">
                    Capital: {selectedRegion.capital} • {selectedRegion.monitoredDistricts} Districts Monitored
                  </p>
                </div>

                {/* Summary */}
                <p className="text-xs text-charcoal-600 leading-relaxed">{selectedRegion.summary}</p>

                {/* Primary & Secondary Hazards */}
                <div className="grid grid-cols-2 gap-3">
                  <div className="p-3.5 rounded-2xl bg-paper-50 border border-paper-200">
                    <span className="text-[10px] font-mono text-charcoal-400 uppercase tracking-wider block">Primary Hazard</span>
                    <span className="text-sm font-bold text-charcoal-900 mt-0.5 block">{selectedRegion.primaryRisk}</span>
                  </div>
                  <div className="p-3.5 rounded-2xl bg-paper-50 border border-paper-200">
                    <span className="text-[10px] font-mono text-charcoal-400 uppercase tracking-wider block">Secondary Hazard</span>
                    <span className="text-sm font-bold text-charcoal-900 mt-0.5 block">{selectedRegion.secondaryRisk || 'None'}</span>
                  </div>
                </div>

                {/* Key Risk Factors */}
                <div className="space-y-2.5">
                  <span className="text-xs font-mono text-charcoal-400 uppercase tracking-wider block">
                    Telemetry Factors
                  </span>
                  {selectedRegion.factors.map((f, i) => (
                    <div key={i} className="p-3 rounded-xl bg-paper-50 border border-paper-200 space-y-1">
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-semibold text-charcoal-900">{f.name}</span>
                        <span className="font-mono text-[10px] text-charcoal-500">{f.weight}%</span>
                      </div>
                      <p className="text-[11px] text-charcoal-500 leading-snug">{f.description}</p>
                    </div>
                  ))}
                </div>

                {/* SDMA Helpline */}
                <div className="p-3.5 rounded-2xl bg-paper-100 border border-paper-200 flex items-center gap-3">
                  <Phone className="w-4 h-4 text-charcoal-600 shrink-0" />
                  <div>
                    <span className="text-[10px] font-mono uppercase text-charcoal-400 block">Emergency SDMA Contact</span>
                    <span className="text-xs font-bold text-charcoal-900 font-mono">{selectedRegion.emergencyHelpline}</span>
                  </div>
                </div>
              </div>
            ) : (
              <EmptyState
                title="No Region Selected"
                description="Click on any state, UT, or marker on the map to inspect its multi-hazard telemetry factors."
                icon={<MapPin className="w-5 h-5 text-charcoal-400" />}
              />
            )}
          </div>
        </div>
      )}
        </>
      )}
    </div>
  );
};
