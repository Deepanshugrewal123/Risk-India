import React, { useState, useEffect } from 'react';
import { disasterService } from '../../services/disasterService';
import { DisasterEvent } from '../../types/disaster';
import { RiskLevel } from '../../types/risk';
import { RiskBadge } from '../common/RiskBadge';
import { DemoBadge } from '../common/DemoBadge';
import { LoadingState } from '../common/LoadingState';
import { ErrorState } from '../common/ErrorState';
import { EmptyState } from '../common/EmptyState';
import { Search, MapPin, Clock, ArrowUpRight, AlertTriangle, X } from 'lucide-react';

interface DisastersPageProps {
  onSelectIncident: (incident: DisasterEvent) => void;
}

export const DisastersPage: React.FC<DisastersPageProps> = ({ onSelectIncident }) => {
  const [incidents, setIncidents] = useState<DisasterEvent[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [selectedType, setSelectedType] = useState<string>('All');
  const [selectedSeverity, setSelectedSeverity] = useState<RiskLevel | 'All'>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const fetchIncidents = async () => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      const data = await disasterService.getActiveDisasters();
      setIncidents(data);
    } catch (err) {
      console.error('Failed to load disasters:', err);
      setErrorMessage('Unable to load disaster incident stream.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchIncidents();
  }, []);

  const types = ['All', 'Flood', 'Earthquake', 'Cyclone', 'Heatwave', 'Landslide', 'Severe Weather'];
  const severities: (RiskLevel | 'All')[] = ['All', 'LOW', 'MODERATE', 'HIGH', 'CRITICAL'];
  const freshnessOptions = ['All', 'LIVE', 'RECENT', 'CACHED'];
  const [selectedFreshness, setSelectedFreshness] = useState<string>('All');

  const filtered = incidents.filter((incident) => {
    const matchesSearch =
      incident.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      incident.location.toLowerCase().includes(searchQuery.toLowerCase()) ||
      incident.state.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesType = selectedType === 'All' || incident.type.toLowerCase() === selectedType.toLowerCase();
    const matchesSeverity = selectedSeverity === 'All' || incident.severity === selectedSeverity;
    const matchesFreshness =
      selectedFreshness === 'All' ||
      (selectedFreshness === 'LIVE' && incident.freshness === 'LIVE') ||
      (selectedFreshness === 'RECENT' && incident.freshness === 'RECENT') ||
      (selectedFreshness === 'CACHED' && incident.freshness === 'CACHED');
    return matchesSearch && matchesType && matchesSeverity && matchesFreshness;
  });

  return (
    <div className="pt-28 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto min-h-screen">
      {/* Page Header */}
      <div className="mb-10">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold">
            Active Incident Command Stream
          </span>
          <DemoBadge label="INCIDENT INTELLIGENCE FEED" />
        </div>
        <h1 className="text-3xl sm:text-5xl font-bold tracking-tight text-charcoal-950">
          Monitored Disasters & Weather Emergencies
        </h1>
        <p className="text-sm sm:text-base text-charcoal-600 mt-2 max-w-2xl">
          Continuous situational telemetry from State Emergency Operations Centers (SEOC), regional radar networks, and district disaster management cells.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 sm:p-5 rounded-3xl bg-white border border-paper-300 shadow-subtle mb-10 space-y-4">
        <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-charcoal-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search by incident name, district, or state (e.g. Brahmaputra, Mandi)..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 rounded-2xl bg-paper-50 border border-paper-200 text-xs sm:text-sm text-charcoal-900 placeholder:text-charcoal-400 focus:outline-none focus:ring-2 focus:ring-charcoal-900"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-3.5 top-1/2 -translate-y-1/2 text-charcoal-400 hover:text-charcoal-600"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

          <div className="flex flex-wrap items-center gap-3">
            {/* Type Filter */}
            <div className="flex items-center gap-1.5">
              <span className="text-xs font-mono text-charcoal-500">Hazard:</span>
              <select
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
                className="px-3 py-2 rounded-xl bg-paper-50 border border-paper-200 text-xs font-mono text-charcoal-800 font-medium focus:outline-none focus:ring-2 focus:ring-charcoal-900"
              >
                {types.map((t) => (
                  <option key={t} value={t}>
                    {t === 'All' ? 'All Types' : t}
                  </option>
                ))}
              </select>
            </div>

            {/* Severity Filter */}
            <div className="flex items-center gap-1.5">
              <span className="text-xs font-mono text-charcoal-500">Severity:</span>
              <select
                value={selectedSeverity}
                onChange={(e) => setSelectedSeverity(e.target.value as RiskLevel | 'All')}
                className="px-3 py-2 rounded-xl bg-paper-50 border border-paper-200 text-xs font-mono text-charcoal-800 font-medium focus:outline-none focus:ring-2 focus:ring-charcoal-900"
              >
                {severities.map((s) => (
                  <option key={s} value={s}>
                    {s === 'All' ? 'All Severities' : `${s} Risk`}
                  </option>
                ))}
              </select>
            </div>

            {/* Freshness Filter */}
            <div className="flex items-center gap-1.5">
              <span className="text-xs font-mono text-charcoal-500">Recency:</span>
              <select
                value={selectedFreshness}
                onChange={(e) => setSelectedFreshness(e.target.value)}
                className="px-3 py-2 rounded-xl bg-paper-50 border border-paper-200 text-xs font-mono text-charcoal-800 font-medium focus:outline-none focus:ring-2 focus:ring-charcoal-900"
              >
                {freshnessOptions.map((f) => (
                  <option key={f} value={f}>
                    {f === 'All' ? 'All Data' : f}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>

      {isLoading ? (
        <LoadingState
          message="Loading Incident Stream..."
          description="Connecting to emergency incident stream..."
          heightClass="min-h-[350px]"
        />
      ) : errorMessage ? (
        <ErrorState
          title="Incident Stream Unavailable"
          message={errorMessage}
          onRetry={fetchIncidents}
          retryLabel="Reload Incidents"
        />
      ) : filtered.length === 0 ? (
        <EmptyState
          title="No Active Disasters Found"
          description="No incidents matched your current search and hazard filters. Try resetting the filters or searching a different region."
          icon={<AlertTriangle className="w-6 h-6 text-stone-400" />}
          action={{
            label: 'Clear Filters',
            onClick: () => {
              setSelectedType('All');
              setSelectedSeverity('All');
              setSelectedFreshness('All');
              setSearchQuery('');
            }
          }}
        />
      ) : (
        /* Incidents Grid */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((incident) => {
            const isFresh = incident.freshness === 'LIVE';
            const isRecent = incident.freshness === 'RECENT';

            return (
              <div
                key={incident.id}
                onClick={() => onSelectIncident(incident)}
                className="group cursor-pointer rounded-3xl bg-white border border-paper-300 p-6 shadow-subtle hover:shadow-elevated transition-all duration-300 hover:border-charcoal-400 flex flex-col justify-between"
              >
                <div>
                  {/* Top Meta: Severity + Four Pillars + Freshness */}
                  <div className="flex flex-wrap items-center justify-between gap-2 mb-3 pb-2 border-b border-paper-100">
                    <RiskBadge level={incident.severity} size="sm" score={incident.riskScore} />

                    <div className="flex flex-wrap items-center gap-1.5">
                      {/* Four Pillars Classification Tag */}
                      <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded-full border ${
                        incident.verified && !incident.isDemoData && isFresh
                          ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                          : incident.title.toLowerCase().includes('prototype') || (incident.data_category || '').includes('ML')
                          ? 'bg-purple-50 text-purple-800 border-purple-200'
                          : incident.verified
                          ? 'bg-blue-50 text-blue-800 border-blue-200'
                          : 'bg-paper-100 text-charcoal-700 border-paper-200'
                      }`}>
                        {incident.verified && !incident.isDemoData && isFresh
                          ? 'LIVE OFFICIAL DATA'
                          : incident.title.toLowerCase().includes('prototype') || (incident.data_category || '').includes('ML')
                          ? 'ML PROTOTYPE ESTIMATE'
                          : incident.verified
                          ? 'OFFICIAL BULLETIN'
                          : 'REGIONAL BASELINE'}
                      </span>

                      {/* Freshness Tag with Strict Honesty */}
                      {incident.freshness === 'CACHED' ? (
                        <span className="inline-flex items-center gap-1 text-[10px] font-mono px-2 py-0.5 rounded-full bg-amber-50 text-amber-800 border border-amber-200 font-bold" title="Cached snapshot — live feed currently unverified">
                          <span>CACHED</span>
                        </span>
                      ) : isFresh ? (
                        <span className="inline-flex items-center gap-1 text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 font-bold">
                          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping" />
                          <span>LIVE</span>
                        </span>
                      ) : isRecent ? (
                        <span className="inline-flex items-center gap-1 text-[10px] font-mono px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200 font-medium">
                          <span className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                          <span>RECENT</span>
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-[10px] font-mono text-charcoal-500 bg-paper-100 px-2 py-0.5 rounded-full border border-paper-200">
                          <span>STALE / ARCHIVE</span>
                        </span>
                      )}
                    </div>
                  </div>

                  <h3 className="text-xl font-bold text-charcoal-950 group-hover:text-charcoal-800 transition-colors leading-snug mb-2">
                    {incident.title}
                  </h3>

                  <div className="flex items-center gap-1.5 text-xs text-charcoal-500 font-mono mb-4">
                    <MapPin className="w-3.5 h-3.5 text-charcoal-400 shrink-0" />
                    <span>{incident.location}, {incident.state}</span>
                  </div>

                  <p className="text-xs text-charcoal-600 line-clamp-3 leading-relaxed mb-6">
                    {incident.description}
                  </p>
                </div>

                <div className="pt-4 border-t border-paper-200 flex items-center justify-between text-xs font-mono text-charcoal-500">
                  <div className="flex items-center gap-1">
                    <Clock className="w-3 h-3 text-charcoal-400" />
                    <span>{incident.lastUpdated || 'Recently updated'}</span>
                  </div>
                  <div className="inline-flex items-center gap-1 text-charcoal-900 font-medium group-hover:translate-x-0.5 transition-transform">
                    <span>Full SitRep</span>
                    <ArrowUpRight className="w-3.5 h-3.5" />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
