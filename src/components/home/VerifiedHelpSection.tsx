import React, { useState, useEffect } from 'react';
import { ReliefAgency } from '../../types/resource';
import { resourceService } from '../../services/resourceService';
import { CheckCircle2, ExternalLink, MapPin, AlertCircle } from 'lucide-react';
import { DemoBadge } from '../common/DemoBadge';
import { LoadingState } from '../common/LoadingState';
import { ErrorState } from '../common/ErrorState';
import { EmptyState } from '../common/EmptyState';

export const VerifiedHelpSection: React.FC = () => {
  const [agencies, setAgencies] = useState<ReliefAgency[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const fetchAgencies = async () => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      const data = await resourceService.getVerifiedAgencies();
      setAgencies(data);
    } catch (err) {
      console.error('Failed to load verified agencies:', err);
      setErrorMessage('Unable to load verified agency registry.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAgencies();
  }, []);

  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div className="text-center max-w-3xl mx-auto mb-14">
        <div className="inline-flex items-center gap-2 mb-3">
          <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold">
            Trust & Verification Protocol
          </span>
          <DemoBadge label="VERIFIED DIRECTORY" />
        </div>
        <h2 className="text-3xl sm:text-5xl font-bold tracking-tight text-charcoal-950 mb-4">
          Help From Sources You Can Trust.
        </h2>
        <p className="text-sm sm:text-base text-charcoal-600 leading-relaxed">
          In emergency situations, misinformation and unauthorized fund collections cost critical time. All entities in our index undergo multi-point administrative verification.
        </p>
      </div>

      {/* Official Evacuation vs Scientific Estimation Protocol Notice */}
      <div className="mb-8 p-4 rounded-2xl bg-paper-100 border border-paper-300 flex items-start gap-3 text-xs">
        <AlertCircle className="w-4 h-4 text-charcoal-700 shrink-0 mt-0.5" />
        <div className="text-charcoal-700 leading-relaxed">
          <strong className="text-charcoal-950 font-bold">Official Safety Directive:</strong> In an active emergency, always prioritize official evacuation instructions and bulletins issued by your District Disaster Management Authority (DDMA), State Disaster Management Authority (SDMA), or the National Disaster Response Force (NDRF). Predictive risk scores and hydrological models are scientific intelligence tools and do not substitute for official administrative orders.
        </div>
      </div>

      {isLoading ? (
        <LoadingState
          message="Loading Verified Directory..."
          description="Connecting to verified agency repository..."
          heightClass="min-h-[280px]"
        />
      ) : errorMessage ? (
        <ErrorState
          title="Directory Unavailable"
          message={errorMessage}
          onRetry={fetchAgencies}
          retryLabel="Retry Connection"
        />
      ) : agencies.length === 0 ? (
        <EmptyState
          title="No Agencies Found"
          description="No registered or verified relief agencies are currently active in the database."
          icon={<AlertCircle className="w-5 h-5 text-stone-400" />}
        />
      ) : (
        /* Cards Grid */
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {agencies.map((agency) => (
            <div
              key={agency.id}
              className="rounded-3xl bg-white border border-paper-300 p-6 sm:p-8 shadow-subtle hover:shadow-elevated transition-shadow flex flex-col justify-between"
            >
              <div>
                {/* Header with Type & Verification Badge */}
                <div className="flex items-center justify-between gap-3 mb-4">
                  <span className="text-xs font-mono font-semibold uppercase tracking-wider text-charcoal-500">
                    {agency.type}
                  </span>

                    <div className="flex items-center gap-1.5">
                      <span
                        className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-mono font-medium ${
                          agency.verificationStatus === 'Government Verified'
                            ? 'bg-blue-50 text-blue-700 border border-blue-200'
                            : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                        }`}
                      >
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>✓ {agency.verificationStatus}</span>
                      </span>
                      {agency.isDemoData ? (
                        <DemoBadge label="VERIFIED DIRECTORY" />
                      ) : (
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-100 text-emerald-900 border border-emerald-300">
                          OFFICIAL
                        </span>
                      )}
                    </div>
                </div>

                {/* Organization Name */}
                <h3 className="text-xl font-bold text-charcoal-950 mb-2">
                  {agency.name}
                </h3>

                {/* Location & HQ */}
                <div className="flex items-center gap-2 text-xs text-charcoal-500 font-mono mb-4">
                  <MapPin className="w-3.5 h-3.5 text-charcoal-400 shrink-0" />
                  <span>HQ: {agency.headquarters}</span>
                </div>

                {/* Operational States */}
                <div className="mb-4">
                  <span className="text-[11px] font-mono text-charcoal-400 block mb-1">
                    Active Operational Theaters:
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {agency.operationalStates.map((st) => (
                      <span
                        key={st}
                        className="px-2 py-0.5 rounded-md bg-paper-100 border border-paper-200 text-[11px] text-charcoal-700 font-mono"
                      >
                        {st}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Services Offered */}
                <div className="mb-6">
                  <span className="text-[11px] font-mono text-charcoal-400 block mb-1">
                    Verified Services:
                  </span>
                  <ul className="space-y-1 text-xs text-charcoal-700">
                    {agency.servicesOffered.map((srv, i) => (
                      <li key={i} className="flex items-center gap-2">
                        <span className="w-1 h-1 rounded-full bg-charcoal-400" />
                        <span>{srv}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Bottom Contact & Link with Tap-Friendly tel: URL */}
              <div className="pt-4 border-t border-paper-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs font-mono">
                <span className="text-charcoal-500">
                  Helpline:{" "}
                  <a
                    href={`tel:${agency.contactNumber.replace(/[^0-9+]/g, '')}`}
                    className="text-charcoal-900 font-bold hover:underline inline-flex items-center gap-1"
                    title="Tap to call emergency helpline"
                  >
                    <span>{agency.contactNumber}</span>
                  </a>
                </span>

                <a
                  href={agency.officialPortalUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 text-charcoal-900 font-semibold hover:underline"
                >
                  <span>Official Portal</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};
