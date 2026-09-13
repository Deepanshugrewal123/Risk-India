import React, { useState, useEffect } from 'react';
import { resourceService } from '../../services/resourceService';
import { disasterService } from '../../services/disasterService';
import { Resource, ResourceCategory } from '../../types/resource';
import { DisasterEvent } from '../../types/disaster';
import { LoadingState } from '../common/LoadingState';
import { ErrorState } from '../common/ErrorState';
import { EmptyState } from '../common/EmptyState';
import {
  Heart,
  ShieldCheck,
  CheckCircle2,
  AlertOctagon,
  Building2,
  Users,
  MapPin,
  Calendar,
  LifeBuoy,
  X,
  Info,
  ArrowUpRight,
  Sparkles,
  Phone,
  Globe
} from 'lucide-react';

export const HelpOthersPage: React.FC = () => {
  const [selectedState, setSelectedState] = useState<string>('All');
  const [selectedCategory, setSelectedCategory] = useState<ResourceCategory | 'All'>('All');
  const [resources, setResources] = useState<Resource[]>([]);
  const [disasters, setDisasters] = useState<DisasterEvent[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [selectedResource, setSelectedResource] = useState<Resource | null>(null);

  const states = ['All', 'Assam', 'Himachal Pradesh', 'Odisha', 'Delhi', 'West Bengal', 'Karnataka'];
  const categories: (ResourceCategory | 'All')[] = [
    'All',
    'Government Relief',
    'Donations / Volunteering',
    'NGO / Relief Organization',
    'Food & Water',
    'Medical Assistance',
    'Disaster Management'
  ];

  const loadData = async () => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      const [resData, disData] = await Promise.all([
        resourceService.getResources({
          state: selectedState === 'All' ? undefined : selectedState,
          category: selectedCategory === 'All' ? undefined : selectedCategory,
          verificationStatus: 'VERIFIED'
        }),
        disasterService.getActiveDisasters()
      ]);
      setResources(resData);
      setDisasters(disData.slice(0, 3)); // Top 3 observed feeds
    } catch (err) {
      console.error('Failed to load help-others data:', err);
      setErrorMessage('Help resources are temporarily unavailable.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [selectedState, selectedCategory]);

  const getActionLabel = (r: Resource): string => {
    if (r.name.includes('Fund') || r.category === 'Donations / Volunteering') {
      return 'Donate via official organization';
    }
    if (r.name.includes('Aapda Mitra') || r.name.includes('Volunteer')) {
      return 'View Official Volunteer Enrollment';
    }
    return 'Visit Official Portal';
  };

  return (
    <div className="pt-28 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto min-h-screen">
      {/* Hero Section */}
      <div className="text-center max-w-3xl mx-auto mb-10">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-risk-low-soft text-xs font-mono font-semibold mb-6">
          <Heart className="w-3.5 h-3.5 fill-emerald-500" />
          <span>VERIFIED RELIEF & SOLIDARITY DIRECTORY</span>
          <span className="text-emerald-300">•</span>
          <span>STATUTORY CHANNELS ONLY</span>
        </div>

        <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-charcoal-950 mb-4 leading-tight">
          Verified Pathways to Help.{' '}
          <span className="block text-charcoal-600 font-light text-3xl sm:text-4xl mt-1">
            Direct Support via Official Organizations
          </span>
        </h1>

        <p className="text-sm sm:text-base text-charcoal-600 leading-relaxed max-w-2xl mx-auto">
          Direct your solidarity responsibly. Connect exclusively with audited statutory agencies, recognized relief funds, and institutional volunteer frameworks.
        </p>
      </div>

      {/* Semantic Distinction Banner */}
      <div className="mb-10 p-5 sm:p-6 rounded-3xl bg-paper-100/90 border border-paper-300 shadow-subtle">
        <div className="flex items-center gap-2 text-xs font-mono font-bold text-charcoal-700 uppercase tracking-wider mb-3">
          <Info className="w-4 h-4 text-blue-600" />
          <span>Operational Guidance // Understanding Risk Signals vs Relief Needs</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-3">
          <div className="p-3.5 rounded-2xl bg-white border border-rose-200 text-xs">
            <div className="flex items-center gap-1.5 font-bold text-rose-700 mb-1">
              <span className="w-2 h-2 rounded-full bg-rose-600 animate-pulse" />
              <span>Observed Disaster</span>
            </div>
            <p className="text-charcoal-600 text-[11px] leading-relaxed">
              Verified physical incident logged by official government bulletins or seismic monitoring networks.
            </p>
          </div>

          <div className="p-3.5 rounded-2xl bg-white border border-amber-200 text-xs">
            <div className="flex items-center gap-1.5 font-bold text-amber-700 mb-1">
              <span className="w-2 h-2 rounded-full bg-amber-500" />
              <span>Potential Risk (AI Baseline)</span>
            </div>
            <p className="text-charcoal-600 text-[11px] leading-relaxed">
              Regional statistical vulnerability. <strong>Does not mean active emergency or that relief funds are currently requested.</strong>
            </p>
          </div>

          <div className="p-3.5 rounded-2xl bg-white border border-emerald-200 text-xs">
            <div className="flex items-center gap-1.5 font-bold text-emerald-700 mb-1">
              <span className="w-2 h-2 rounded-full bg-emerald-600" />
              <span>Assistance Opportunity</span>
            </div>
            <p className="text-charcoal-600 text-[11px] leading-relaxed">
              Audited statutory relief channel, direct CM/PM relief fund, or accredited NGO program currently accepting support.
            </p>
          </div>
        </div>

        <div className="text-[11px] font-mono text-charcoal-500 bg-white/60 p-2.5 rounded-xl border border-paper-200">
          <strong>Safety Commitment:</strong> RISK // INDIA does not collect payments or process volunteer signups. All links direct exclusively to official .gov.in or statutory NGO web portals.
        </div>
      </div>

      {/* Observed Disaster Context Cards (If Any) */}
      {disasters.length > 0 && (
        <div className="mb-10">
          <div className="flex items-center justify-between mb-4">
            <div>
              <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-bold">
                Current Monitored Feeds
              </span>
              <h2 className="text-xl font-bold text-charcoal-950 mt-0.5">
                Recent Verified Disasters (Official Feeds)
              </h2>
            </div>
            <span className="text-xs font-mono text-charcoal-400">
              {disasters.length} Monitored Reports
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {disasters.map((d) => (
              <div
                key={d.id}
                className="rounded-2xl bg-white border border-paper-300 p-4 shadow-subtle flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-50 text-rose-700 border border-rose-200">
                      <span className="w-1.5 h-1.5 rounded-full bg-rose-600 animate-pulse" />
                      OBSERVED DISASTER
                    </span>
                    <span className="text-[10px] font-mono text-charcoal-400">
                      {d.type}
                    </span>
                  </div>
                  <h3 className="text-sm font-bold text-charcoal-950 mb-1 line-clamp-2">
                    {d.title}
                  </h3>
                  <div className="flex items-center gap-1 text-xs text-charcoal-500 font-mono mb-2">
                    <MapPin className="w-3 h-3 text-charcoal-400 shrink-0" />
                    <span className="truncate">{d.location}</span>
                  </div>
                  <p className="text-xs text-charcoal-600 line-clamp-2 mb-3">
                    {d.description}
                  </p>
                </div>

                <div className="pt-3 border-t border-paper-200 flex items-center justify-between text-[11px] font-mono">
                  <span className="text-charcoal-500 truncate max-w-[130px]">
                    Source: {d.source || 'Authorized Feed'}
                  </span>
                  {d.state && d.state !== 'India' && (
                    <button
                      onClick={() => setSelectedState(d.state)}
                      className="text-blue-700 hover:text-blue-900 font-bold underline"
                    >
                      Filter for {d.state}
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Filter Toolbar */}
      <div className="mb-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-4">
          <div>
            <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-bold">
              Verified Assistance Directory
            </span>
            <h2 className="text-2xl font-bold text-charcoal-950 mt-0.5">
              Official Relief Funds & Organizations
            </h2>
            <p className="text-xs text-charcoal-600 mt-1">
              Contribute directly through official portals. Every listed agency is verified against government records.
            </p>
          </div>
          <span className="text-xs font-mono text-charcoal-400">
            Showing {resources.length} Verified Channels
          </span>
        </div>

        {/* Filter Controls */}
        <div className="p-4 rounded-2xl bg-paper-50/90 border border-paper-300 space-y-3">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-mono uppercase text-charcoal-600 font-semibold mb-1">
                Filter By State / Region
              </label>
              <select
                value={selectedState}
                onChange={(e) => setSelectedState(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-white border border-paper-300 text-xs font-mono text-charcoal-900 focus:outline-none"
              >
                {states.map((st) => (
                  <option key={st} value={st}>
                    {st === 'All' ? 'All States (Pan-India)' : st}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-mono uppercase text-charcoal-600 font-semibold mb-1">
                Filter By Assistance Type
              </label>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value as any)}
                className="w-full px-3 py-2 rounded-xl bg-white border border-paper-300 text-xs font-mono text-charcoal-900 focus:outline-none"
              >
                {categories.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-paper-200 text-xs font-mono">
            <span className="text-charcoal-400">Active:</span>
            <span className="px-2 py-0.5 rounded-full bg-white border border-paper-200 text-charcoal-700">
              Region: <strong>{selectedState}</strong>
            </span>
            <span className="px-2 py-0.5 rounded-full bg-white border border-paper-200 text-charcoal-700">
              Category: <strong>{selectedCategory}</strong>
            </span>
            {(selectedState !== 'All' || selectedCategory !== 'All') && (
              <button
                onClick={() => {
                  setSelectedState('All');
                  setSelectedCategory('All');
                }}
                className="text-xs text-charcoal-500 hover:text-charcoal-900 underline ml-2"
              >
                Reset Filters
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Resources Grid */}
      {isLoading ? (
        <LoadingState
          message="Loading Relief Opportunities..."
          description="Connecting to verified statutory organizations and emergency funds..."
          heightClass="min-h-[260px]"
        />
      ) : errorMessage ? (
        <ErrorState
          title="Help Resources Temporarily Unavailable"
          message={errorMessage}
          onRetry={loadData}
          retryLabel="Reload Directory"
        />
      ) : resources.length === 0 ? (
        <EmptyState
          title="No Verified Resources Found"
          description="No verified assistance opportunities match your selected filters. Try broadening the state or category filter."
          icon={<LifeBuoy className="w-6 h-6 text-stone-400" />}
          action={{
            label: 'Reset Filters',
            onClick: () => {
              setSelectedState('All');
              setSelectedCategory('All');
            }
          }}
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
          {resources.map((res) => {
            const isFund = res.name.includes('Fund') || res.category === 'Donations / Volunteering';
            const isVolunteer = res.name.includes('Aapda Mitra') || res.name.includes('Volunteer');
            const portalUrl = res.website_url || res.website || res.source_url || 'https://ndma.gov.in';

            return (
              <div
                key={res.id}
                className="rounded-3xl bg-white border border-paper-300 p-6 shadow-subtle hover:shadow-elevated transition-shadow flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-3">
                    <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-mono font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                      <span>SOURCE VERIFIED</span>
                    </span>
                    <span className="text-[10px] font-mono text-charcoal-400 uppercase">
                      {res.type}
                    </span>
                  </div>

                  <h3 className="text-lg font-bold text-charcoal-950 mb-1">
                    {res.name}
                  </h3>

                  <div className="flex items-center gap-1.5 text-xs text-charcoal-500 font-mono mb-3">
                    <MapPin className="w-3.5 h-3.5 text-charcoal-400 shrink-0" />
                    <span>{res.district ? `${res.district}, ${res.state || 'India'}` : res.location}</span>
                  </div>

                  <p className="text-xs text-charcoal-600 leading-relaxed mb-4">
                    {res.description}
                  </p>

                  {res.services && res.services.length > 0 && (
                    <div className="mb-4">
                      <span className="text-[10px] font-mono uppercase text-charcoal-400 block mb-1.5">
                        Authorized Operations:
                      </span>
                      <div className="flex flex-wrap gap-1">
                        {res.services.map((svc, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-0.5 rounded-lg bg-paper-100 text-charcoal-700 text-[10px] font-mono"
                          >
                            {svc}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                <div className="pt-4 border-t border-paper-200 space-y-3">
                  <div className="flex items-center justify-between text-[11px] font-mono text-charcoal-500">
                    <span>Source: <strong>{res.source || 'Official Registry'}</strong></span>
                    <span className="text-[10px] text-charcoal-400">
                      {res.freshness || 'CURRENT'}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <a
                      href={portalUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className={`flex-1 inline-flex items-center justify-center gap-1.5 py-2.5 px-3 rounded-xl text-xs font-mono font-bold transition-colors ${
                        isFund
                          ? 'bg-amber-600 hover:bg-amber-700 text-white'
                          : isVolunteer
                          ? 'bg-blue-600 hover:bg-blue-700 text-white'
                          : 'bg-charcoal-900 hover:bg-charcoal-800 text-paper-50'
                      }`}
                    >
                      <span>{getActionLabel(res)}</span>
                      <ArrowUpRight className="w-3.5 h-3.5" />
                    </a>

                    <button
                      onClick={() => setSelectedResource(res)}
                      className="px-3 py-2.5 rounded-xl border border-paper-300 text-charcoal-700 hover:bg-paper-100 text-xs font-mono transition-colors"
                      title="View full details"
                    >
                      Details
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Statutory Guidelines Box */}
      <div className="rounded-3xl bg-paper-100 border border-paper-300 p-6 sm:p-8">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-start gap-3.5">
            <ShieldCheck className="w-6 h-6 text-emerald-600 shrink-0 mt-0.5" />
            <div>
              <h3 className="text-base font-bold text-charcoal-950 mb-1">
                Direct Statutory Transparency Standards
              </h3>
              <p className="text-xs text-charcoal-600 leading-relaxed max-w-2xl">
                All donations are routed directly to official government bank accounts or accredited 80G tax-exempt charitable trusts. RISK // INDIA holds no escrow accounts and levies zero intermediary transaction fees.
              </p>
            </div>
          </div>
          <div className="shrink-0 flex items-center gap-2">
            <span className="px-3 py-1.5 rounded-xl bg-white border border-paper-200 text-xs font-mono text-charcoal-700">
              FCRA / 80G Regulated
            </span>
          </div>
        </div>
      </div>

      {/* Resource Detail Modal */}
      {selectedResource && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-charcoal-950/60 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="relative w-full max-w-xl rounded-3xl bg-white border border-paper-300 shadow-floating p-6 sm:p-8 max-h-[90vh] overflow-y-auto">
            <button
              onClick={() => setSelectedResource(null)}
              className="absolute top-6 right-6 p-2 rounded-xl text-charcoal-400 hover:text-charcoal-900 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="mb-4">
              <div className="flex items-center gap-2 mb-2">
                <span className="px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                  ✓ SOURCE VERIFIED
                </span>
                <span className="text-xs font-mono text-charcoal-400">
                  {selectedResource.type}
                </span>
              </div>
              <h3 className="text-2xl font-bold text-charcoal-950">
                {selectedResource.name}
              </h3>
              <p className="text-xs font-mono text-charcoal-500 mt-1 flex items-center gap-1">
                <MapPin className="w-3.5 h-3.5" />
                <span>{selectedResource.district ? `${selectedResource.district}, ${selectedResource.state || 'India'}` : selectedResource.location}</span>
              </p>
            </div>

            <div className="space-y-4 text-xs">
              <div className="p-4 rounded-2xl bg-paper-50 border border-paper-200">
                <span className="font-mono uppercase text-[10px] text-charcoal-400 block mb-1 font-semibold">
                  Scope of Support & Mandate
                </span>
                <p className="text-charcoal-700 leading-relaxed text-sm">
                  {selectedResource.description}
                </p>
              </div>

              {selectedResource.services && (
                <div>
                  <span className="font-mono uppercase text-[10px] text-charcoal-400 block mb-1.5 font-semibold">
                    Services & Relief Activities:
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {selectedResource.services.map((s, idx) => (
                      <span
                        key={idx}
                        className="px-2.5 py-1 rounded-xl bg-paper-100 text-charcoal-800 font-mono text-xs"
                      >
                        ✓ {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                <div className="p-3 rounded-xl bg-paper-50 border border-paper-200">
                  <span className="font-mono uppercase text-[10px] text-charcoal-400 block mb-1">
                    Official Contact
                  </span>
                  <span className="font-mono font-semibold text-charcoal-900">
                    {selectedResource.contactNumber || selectedResource.phone || 'Available via portal'}
                  </span>
                </div>

                <div className="p-3 rounded-xl bg-paper-50 border border-paper-200">
                  <span className="font-mono uppercase text-[10px] text-charcoal-400 block mb-1">
                    Verification Source
                  </span>
                  <span className="font-mono font-semibold text-charcoal-900">
                    {selectedResource.source || 'Authorized Registry'}
                  </span>
                </div>
              </div>

              {selectedResource.accessibilityNotes && (
                <div className="p-3 rounded-xl bg-blue-50/60 border border-blue-200 text-blue-900 font-mono text-[11px]">
                  <strong>Notes:</strong> {selectedResource.accessibilityNotes}
                </div>
              )}

              <div className="pt-4 flex items-center justify-end gap-3 border-t border-paper-200">
                <button
                  onClick={() => setSelectedResource(null)}
                  className="px-4 py-2 rounded-xl text-charcoal-600 hover:text-charcoal-900 text-xs font-mono font-medium"
                >
                  Close
                </button>
                <a
                  href={selectedResource.website_url || selectedResource.website || selectedResource.source_url || 'https://ndma.gov.in'}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 px-5 py-2.5 rounded-xl bg-charcoal-900 text-white font-mono text-xs font-bold hover:bg-charcoal-800 transition-colors shadow-sm"
                >
                  <span>{getActionLabel(selectedResource)}</span>
                  <ArrowUpRight className="w-3.5 h-3.5" />
                </a>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
