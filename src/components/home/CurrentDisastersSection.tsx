import React, { useState, useEffect } from 'react';
import { DisasterEvent } from '../../types/disaster';
import { disasterService } from '../../services/disasterService';
import { RiskBadge } from '../common/RiskBadge';
import { TiltCard } from '../common/TiltCard';
import { LoadingState } from '../common/LoadingState';
import { ErrorState } from '../common/ErrorState';
import { EmptyState } from '../common/EmptyState';
import { Clock, MapPin, ArrowUpRight, AlertTriangle, CheckCircle2, Radio, ExternalLink } from 'lucide-react';

interface CurrentDisastersSectionProps {
  onSelectIncident: (incident: DisasterEvent) => void;
  onViewAllDisasters: () => void;
}

export const CurrentDisastersSection: React.FC<CurrentDisastersSectionProps> = ({
  onSelectIncident,
  onViewAllDisasters,
}) => {
  const [incidents, setIncidents] = useState<DisasterEvent[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const fetchDisasters = async () => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      const data = await disasterService.getActiveDisasters();
      setIncidents(data);
    } catch (err) {
      console.error('Failed to load active disasters:', err);
      setErrorMessage('Unable to load current disaster incidents from the service.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDisasters();
  }, []);

  const hasLiveEvents = incidents.some((i) => i.verified && !i.isDemoData);

  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold">
              Active Incidents & Sitreps
            </span>
            {hasLiveEvents ? (
              <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 text-[10px] font-mono font-bold">
                <Radio className="w-3 h-3 text-emerald-600 animate-pulse" />
                <span>OPERATIONAL DATA FEED</span>
              </span>
            ) : (
              <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-paper-200 text-charcoal-700 border border-paper-300 text-[10px] font-mono font-bold">
                <span className="w-1.5 h-1.5 rounded-full bg-risk-high" />
                <span>REFERENCE ARCHIVE</span>
              </span>
            )}
            <span className="text-[10px] font-mono text-charcoal-500">
              USGS & Official Bulletins
            </span>
          </div>
          <h2 className="text-3xl sm:text-5xl font-bold tracking-tight text-charcoal-950">
            What Is Happening Now?
          </h2>
          <p className="text-sm sm:text-base text-charcoal-600 max-w-xl mt-3">
            Real-time incident monitoring aggregating public subcontinental seismic telemetry (USGS) and authoritative government bulletins (IMD, CWC, ASDMA).
          </p>
        </div>

        <button
          onClick={onViewAllDisasters}
          className="inline-flex items-center gap-1.5 text-xs font-mono font-medium text-charcoal-700 hover:text-charcoal-950 transition-colors shrink-0"
        >
          <span>View All Monitored Incidents</span>
          <ArrowUpRight className="w-4 h-4" />
        </button>
      </div>

      {/* Dynamic Content: Loading, Error, Empty, or Grid */}
      {isLoading ? (
        <LoadingState
          message="Loading Monitored Disasters..."
          description="Connecting to disaster service feed..."
          heightClass="min-h-[280px]"
        />
      ) : errorMessage ? (
        <ErrorState
          title="Incident Feed Unavailable"
          message={errorMessage}
          onRetry={fetchDisasters}
          retryLabel="Reload Incidents"
        />
      ) : incidents.length === 0 ? (
        <div className="rounded-3xl bg-paper-100 border border-paper-300 p-8 sm:p-12 text-center max-w-2xl mx-auto">
          <AlertTriangle className="w-8 h-8 text-amber-600 mx-auto mb-3" />
          <h3 className="text-lg font-bold text-charcoal-950 mb-2">
            No Verified Live Disaster Data Currently Available
          </h3>
          <p className="text-xs sm:text-sm text-charcoal-600 mb-6 leading-relaxed">
            All upstream seismic and bulletin feeds indicate no critical incidents within the active watch window. For official national alerts, consult government portals directly.
          </p>
          <div className="flex flex-wrap justify-center gap-3 text-xs font-mono">
            <a
              href="https://ndma.gov.in"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1 px-3 py-1.5 rounded-full bg-white border border-paper-300 text-charcoal-800 hover:text-charcoal-950"
            >
              <span>NDMA Portal</span>
              <ExternalLink className="w-3 h-3" />
            </a>
            <a
              href="https://mausam.imd.gov.in"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1 px-3 py-1.5 rounded-full bg-white border border-paper-300 text-charcoal-800 hover:text-charcoal-950"
            >
              <span>IMD Weather</span>
              <ExternalLink className="w-3 h-3" />
            </a>
            <a
              href="https://ffs.india-water.gov.in"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1 px-3 py-1.5 rounded-full bg-white border border-paper-300 text-charcoal-800 hover:text-charcoal-950"
            >
              <span>CWC Flood Telemetry</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>
      ) : (
        /* Grid of Disasters with Subtle Cursor Tilt Cards */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {incidents.slice(0, 6).map((incident) => {
            const isFresh = incident.freshness === 'LIVE';
            const isRecent = incident.freshness === 'RECENT';

            return (
              <TiltCard
                key={incident.id}
                maxTilt={1.5}
                onClick={() => onSelectIncident(incident)}
                className="group cursor-pointer rounded-3xl bg-white border border-paper-300 p-6 shadow-subtle hover:shadow-elevated transition-all duration-300 hover:border-charcoal-400 flex flex-col justify-between"
              >
                <div>
                  {/* Top Meta Line: Severity + Freshness/Status */}
                  <div className="flex items-center justify-between gap-2 mb-4">
                    <RiskBadge level={incident.severity} size="sm" score={incident.riskScore} />
                    
                    <div className="flex items-center gap-1.5">
                      {incident.verified && !incident.isDemoData ? (
                        <span
                          className={`inline-flex items-center gap-1 text-[10px] font-mono px-2 py-0.5 rounded-full border ${
                            isFresh
                              ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                              : isRecent
                              ? 'bg-blue-50 text-blue-700 border-blue-200'
                              : 'bg-paper-100 text-charcoal-600 border-paper-200'
                          }`}
                        >
                          <span
                            className={`w-1.5 h-1.5 rounded-full ${
                              isFresh ? 'bg-emerald-500 animate-ping' : isRecent ? 'bg-blue-500' : 'bg-charcoal-400'
                            }`}
                          />
                          <span>{incident.freshness || 'RECENT'}</span>
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-[10px] font-mono text-charcoal-500 bg-paper-100 px-2 py-0.5 rounded-full border border-paper-200">
                          <span>REFERENCE ARCHIVE</span>
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Title & Location */}
                  <h3 className="text-lg font-bold text-charcoal-950 group-hover:text-charcoal-800 transition-colors leading-snug mb-2">
                    {incident.title}
                  </h3>

                  <div className="flex items-center gap-1.5 text-xs text-charcoal-500 font-mono mb-4">
                    <MapPin className="w-3.5 h-3.5 text-charcoal-400 shrink-0" />
                    <span className="truncate">{incident.location || incident.state}</span>
                  </div>

                  {/* Brief Description */}
                  <p className="text-xs text-charcoal-600 line-clamp-3 leading-relaxed mb-6">
                    {incident.description}
                  </p>
                </div>

                {/* Bottom Details Footer with Transparent Attribution */}
                <div className="pt-4 border-t border-paper-200 flex items-center justify-between text-xs font-mono text-charcoal-500">
                  <div className="flex items-center gap-1 truncate max-w-[190px]" title={incident.source || 'Authorized Feed'}>
                    <CheckCircle2 className="w-3 h-3 text-emerald-600 shrink-0" />
                    <span className="truncate">{incident.source || 'Official Feed'}</span>
                  </div>
                  <div className="inline-flex items-center gap-1 text-charcoal-900 font-medium group-hover:translate-x-0.5 transition-transform shrink-0">
                    <span>Examine</span>
                    <ArrowUpRight className="w-3.5 h-3.5" />
                  </div>
                </div>
              </TiltCard>
            );
          })}
        </div>
      )}
    </section>
  );
};
