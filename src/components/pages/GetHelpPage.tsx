import React, { useState, useEffect } from 'react';
import { resourceService } from '../../services/resourceService';
import { Resource, ResourceCategory } from '../../types/resource';
import { LoadingState } from '../common/LoadingState';
import { ErrorState } from '../common/ErrorState';
import { EmptyState } from '../common/EmptyState';
import {
  PhoneCall,
  AlertOctagon,
  CheckCircle2,
  MapPin,
  ExternalLink,
  ShieldCheck,
  Filter,
  LifeBuoy,
  X,
  Info,
  Clock,
  Printer
} from 'lucide-react';

export const GetHelpPage: React.FC = () => {
  const [selectedState, setSelectedState] = useState<string>('All');
  const [selectedDisaster, setSelectedDisaster] = useState<string>('All');
  const [selectedCategory, setSelectedCategory] = useState<ResourceCategory | 'All'>('All');
  const [resources, setResources] = useState<Resource[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [selectedResource, setSelectedResource] = useState<Resource | null>(null);

  const helplines = resourceService.getHelplines();
  const states = ['All', 'Assam', 'Himachal Pradesh', 'Odisha', 'Delhi', 'West Bengal', 'Karnataka'];
  const disasters = ['All', 'Flood', 'Cyclone', 'Landslide', 'Earthquake', 'All Hazards'];
  const categories: (ResourceCategory | 'All')[] = [
    'All',
    'Emergency Services',
    'Government Relief',
    'Medical Assistance',
    'Rescue',
    'Food & Water',
    'Disaster Management',
    'NGO / Relief Organization'
  ];

  const fetchResources = async () => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      const data = await resourceService.getResources({
        state: selectedState === 'All' ? undefined : selectedState,
        category: selectedCategory === 'All' ? undefined : selectedCategory,
        disaster_type: selectedDisaster === 'All' || selectedDisaster === 'All Hazards' ? undefined : selectedDisaster,
        verificationStatus: 'VERIFIED'
      });
      setResources(data);
    } catch (err) {
      console.error('Failed to load verified resources:', err);
      setErrorMessage('Help resources are temporarily unavailable.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchResources();
  }, [selectedState, selectedDisaster, selectedCategory]);

  const getVerificationTag = (resource: Resource) => {
    const text = `${resource.category} ${resource.source} ${resource.name}`.toLowerCase();
    if (
      resource.category === 'Government Relief' ||
      resource.category === 'Disaster Management' ||
      resource.category === 'Emergency Services' ||
      text.includes('government') ||
      text.includes('ndma') ||
      text.includes('sdma') ||
      text.includes('ddma') ||
      text.includes('police') ||
      text.includes('cwc') ||
      text.includes('ministry') ||
      text.includes('statutory')
    ) {
      return {
        label: 'OFFICIAL GOVERNMENT',
        style: 'bg-emerald-50 text-emerald-800 border-emerald-300',
      };
    }
    if (
      resource.category === 'NGO / Relief Organization' ||
      resource.category === 'Donations / Volunteering' ||
      text.includes('red cross') ||
      text.includes('unicef') ||
      text.includes('ngo') ||
      text.includes('foundation')
    ) {
      return {
        label: 'VERIFIED NGO / AGENCY',
        style: 'bg-blue-50 text-blue-800 border-blue-300',
      };
    }
    return {
      label: 'COMMUNITY AID',
      style: 'bg-paper-100 text-charcoal-700 border-paper-300',
    };
  };

  return (
    <div className="pt-28 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto min-h-screen">
      {/* Emergency Disclaimer Banner */}
      <div className="mb-6 p-4 rounded-2xl bg-amber-50 border border-amber-300 text-amber-950 text-xs font-mono flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-xs">
        <div className="flex items-start sm:items-center gap-2.5">
          <AlertOctagon className="w-4 h-4 text-amber-700 shrink-0 mt-0.5 sm:mt-0" />
          <span>
            <strong>LIFE-SAFETY NOTICE:</strong> For immediate emergencies, contact local emergency services and follow official government instructions. Always follow local civil protection, NDMA, SDMA, and District Collector evacuation instructions. Platform resource directories and sensor telemetry do not replace statutory emergency orders.
          </span>
        </div>
        <span className="shrink-0 text-[10px] text-amber-900 bg-amber-200/80 px-2 py-0.5 rounded border border-amber-300 font-bold uppercase">
          OFFICIAL PROTOCOL
        </span>
      </div>

      {/* Critical Emergency Speed-Dial Card */}
      <div className="mb-10 p-6 sm:p-8 rounded-3xl bg-red-50/80 border-2 border-red-200 shadow-elevated flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="flex items-start gap-4">
          <div className="p-3 rounded-2xl bg-risk-critical text-white shrink-0 mt-1">
            <AlertOctagon className="w-7 h-7" />
          </div>
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-mono uppercase tracking-wider text-risk-critical font-bold">
                Immediate Crisis Dispatch
              </span>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-risk-critical/10 text-risk-critical border border-risk-critical/30">
                24/7 TOLL-FREE
              </span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-charcoal-950">
              National Emergency Hotlines
            </h2>
            <p className="text-xs sm:text-sm text-charcoal-700 mt-1">
              Connect directly with official first-responders for search, flood extraction, fire, or trauma:
            </p>
          </div>
        </div>

        {/* Big Dial Buttons */}
        <div className="flex flex-wrap items-center gap-3 shrink-0 w-full md:w-auto">
          <a
            href="tel:112"
            className="flex-1 sm:flex-initial inline-flex items-center justify-center gap-2 px-5 py-3 rounded-2xl bg-charcoal-900 text-paper-50 font-mono text-sm font-bold shadow-md hover:bg-charcoal-800 transition-colors"
          >
            <PhoneCall className="w-4 h-4 text-rose-400" />
            <span>DIAL 112 (Police / Rescue)</span>
          </a>
          <a
            href="tel:1078"
            className="flex-1 sm:flex-initial inline-flex items-center justify-center gap-2 px-5 py-3 rounded-2xl bg-white text-charcoal-900 border border-paper-300 font-mono text-sm font-bold shadow-subtle hover:bg-paper-50 transition-colors"
          >
            <PhoneCall className="w-4 h-4 text-amber-600" />
            <span>DIAL 1078 (NDMA Helpline)</span>
          </a>
        </div>
      </div>

      {/* 2-Column Grid: Central Helplines Directory + Offline Self-Preservation */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-14">
        {/* Helplines Directory */}
        <div className="lg:col-span-7 rounded-3xl bg-white border border-paper-300 p-6 sm:p-8 shadow-subtle">
          <div className="flex items-center justify-between mb-6">
            <div>
              <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold">
                Verified Hotlines
              </span>
              <h3 className="text-xl font-bold text-charcoal-950 mt-0.5">
                Central & State Disaster Lines
              </h3>
            </div>
            <span className="px-2.5 py-1 rounded-full text-xs font-mono font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
              ✓ GOVT VERIFIED
            </span>
          </div>

          <div className="space-y-3">
            {helplines.map((hl, i) => (
              <div
                key={i}
                className="p-3.5 sm:p-4 rounded-2xl bg-paper-50/80 border border-paper-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 hover:border-paper-400 transition-colors"
              >
                <div>
                  <h4 className="text-sm font-bold text-charcoal-900">{hl.service}</h4>
                  <p className="text-xs text-charcoal-500 mt-0.5">{hl.description}</p>
                </div>
                <a
                  href={`tel:${hl.number}`}
                  className="px-3.5 py-1.5 rounded-xl bg-white hover:bg-paper-100 border border-paper-300 font-mono text-xs font-bold text-charcoal-900 flex items-center gap-1.5 shrink-0 shadow-xs"
                >
                  <PhoneCall className="w-3.5 h-3.5 text-emerald-600" />
                  <span>Call {hl.number}</span>
                </a>
              </div>
            ))}
          </div>
        </div>

        {/* Offline Action Card */}
        <div className="lg:col-span-5 rounded-3xl bg-white border border-paper-300 p-6 sm:p-8 shadow-subtle flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold">
                Offline Action Guide
              </span>
              <span className="text-xs font-mono text-charcoal-400">NO INTERNET READY</span>
            </div>
            <h3 className="text-xl font-bold text-charcoal-950 mb-3">
              If Telecommunications Fail
            </h3>
            <ul className="space-y-2.5 text-xs text-charcoal-700">
              <li className="flex items-start gap-2 bg-paper-50 p-2.5 rounded-xl border border-paper-200">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>Conserve battery: Switch phone to Ultra Power Saver; use SMS rather than voice calls.</span>
              </li>
              <li className="flex items-start gap-2 bg-paper-50 p-2.5 rounded-xl border border-paper-200">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>Keep transistor radio tuned to All India Radio AM frequencies for district announcements.</span>
              </li>
              <li className="flex items-start gap-2 bg-paper-50 p-2.5 rounded-xl border border-paper-200">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>Signal for help: Bright fabric on roof during daytime; 3 flashes torch signal at night.</span>
              </li>
              <li className="flex items-start gap-2 bg-paper-50 p-2.5 rounded-xl border border-paper-200">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>Do not enter standing floodwaters near submerged transformers or fallen electrical cables.</span>
              </li>
            </ul>
          </div>

          <div className="pt-6 border-t border-paper-200 mt-6">
            <button
              onClick={() => window.print()}
              className="w-full py-2.5 px-4 rounded-xl bg-paper-100 hover:bg-paper-200 text-charcoal-800 text-xs font-mono font-semibold flex items-center justify-center gap-2 border border-paper-300 transition-colors"
            >
              <Printer className="w-4 h-4" />
              <span>Print Offline Emergency Card</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Get Help Interactive Multi-Filter Directory */}
      <div className="mb-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-6">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-bold">
                Verified Assistance Directory
              </span>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-blue-50 text-blue-700 border border-blue-200">
                MULTI-PARAMETER FILTER
              </span>
            </div>
            <h3 className="text-2xl sm:text-3xl font-bold text-charcoal-950">
              Find Verified Help in Your Area
            </h3>
            <p className="text-xs sm:text-sm text-charcoal-600 mt-1">
              Filter by location, disaster type, and need. Displays only official government agencies and statutory verified organizations.
            </p>
          </div>
        </div>

        {/* 3-Filter Interactive Bar */}
        <div className="p-5 rounded-3xl bg-paper-50/90 border border-paper-300 space-y-4 shadow-subtle mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Filter 1: State / Region */}
            <div>
              <label className="block text-xs font-mono uppercase tracking-wider text-charcoal-600 font-semibold mb-1.5">
                01 // State / Region
              </label>
              <select
                value={selectedState}
                onChange={(e) => setSelectedState(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl bg-white border border-paper-300 text-xs font-mono text-charcoal-900 focus:outline-none focus:ring-2 focus:ring-charcoal-900"
              >
                {states.map((st) => (
                  <option key={st} value={st}>
                    {st === 'All' ? 'All States (Pan-India)' : st}
                  </option>
                ))}
              </select>
            </div>

            {/* Filter 2: Disaster Hazard Type */}
            <div>
              <label className="block text-xs font-mono uppercase tracking-wider text-charcoal-600 font-semibold mb-1.5">
                02 // Disaster Type
              </label>
              <select
                value={selectedDisaster}
                onChange={(e) => setSelectedDisaster(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl bg-white border border-paper-300 text-xs font-mono text-charcoal-900 focus:outline-none focus:ring-2 focus:ring-charcoal-900"
              >
                {disasters.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </select>
            </div>

            {/* Filter 3: Assistance Need Category */}
            <div>
              <label className="block text-xs font-mono uppercase tracking-wider text-charcoal-600 font-semibold mb-1.5">
                03 // Assistance Category
              </label>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value as any)}
                className="w-full px-3.5 py-2.5 rounded-xl bg-white border border-paper-300 text-xs font-mono text-charcoal-900 focus:outline-none focus:ring-2 focus:ring-charcoal-900"
              >
                {categories.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Active Filter Chips */}
          <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-paper-200 text-xs font-mono">
            <span className="text-charcoal-400">Active Filters:</span>
            <span className="px-2.5 py-0.5 rounded-full bg-white border border-paper-300 text-charcoal-700">
              Location: <strong>{selectedState}</strong>
            </span>
            <span className="px-2.5 py-0.5 rounded-full bg-white border border-paper-300 text-charcoal-700">
              Disaster: <strong>{selectedDisaster}</strong>
            </span>
            <span className="px-2.5 py-0.5 rounded-full bg-white border border-paper-300 text-charcoal-700">
              Category: <strong>{selectedCategory}</strong>
            </span>
            {(selectedState !== 'All' || selectedDisaster !== 'All' || selectedCategory !== 'All') && (
              <button
                onClick={() => {
                  setSelectedState('All');
                  setSelectedDisaster('All');
                  setSelectedCategory('All');
                }}
                className="text-xs text-charcoal-500 hover:text-charcoal-900 underline ml-2"
              >
                Reset All Filters
              </button>
            )}
          </div>
        </div>

        {/* Resources Dynamic Grid */}
        {isLoading ? (
          <LoadingState
            message="Loading Verified Resources..."
            description="Querying verified disaster authorities and relief networks..."
            heightClass="min-h-[280px]"
          />
        ) : errorMessage ? (
          <ErrorState
            title="Help Resources Temporarily Unavailable"
            message={errorMessage}
            onRetry={fetchResources}
            retryLabel="Retry Directory"
          />
        ) : resources.length === 0 ? (
          <EmptyState
            title="No Verified Resources Found"
            description="No verified resource is currently available for this filter combination. Contact the 24/7 State Emergency Operations Center at 1070 or National Emergency at 112."
            icon={<LifeBuoy className="w-6 h-6 text-stone-400" />}
            action={{
              label: 'Reset Filters',
              onClick: () => {
                setSelectedState('All');
                setSelectedDisaster('All');
                setSelectedCategory('All');
              }
            }}
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {resources.map((resource) => {
              const vTag = getVerificationTag(resource);

              return (
                <div
                  key={resource.id}
                  onClick={() => setSelectedResource(resource)}
                  className="group cursor-pointer rounded-3xl bg-white border border-paper-300 p-6 shadow-subtle hover:shadow-elevated transition-all duration-200 hover:border-charcoal-400 flex flex-col justify-between"
                >
                  <div>
                    {/* Category & Explicit Verification Badge */}
                    <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
                      <span className="text-[11px] font-mono font-semibold uppercase tracking-wider text-charcoal-500">
                        {resource.category}
                      </span>
                      <span className={`inline-flex items-center gap-1 text-[10px] font-mono px-2 py-0.5 rounded-full border font-bold ${vTag.style}`}>
                        <CheckCircle2 className="w-3 h-3" />
                        <span>{vTag.label}</span>
                      </span>
                    </div>

                    {/* Organization / Resource Name */}
                    <h4 className="text-lg font-bold text-charcoal-950 group-hover:text-charcoal-800 transition-colors mb-2">
                      {resource.name}
                    </h4>

                    {/* Location Info */}
                    <div className="flex items-center gap-1.5 text-xs text-charcoal-500 font-mono mb-3">
                      <MapPin className="w-3.5 h-3.5 text-charcoal-400 shrink-0" />
                      <span>{resource.location}</span>
                    </div>

                    {/* Description */}
                    <p className="text-xs text-charcoal-600 line-clamp-3 leading-relaxed mb-4">
                      {resource.description}
                    </p>

                    {/* Direct Tap-to-Call Button on Card */}
                    {resource.phone && (
                      <div className="mb-4">
                        <a
                          href={`tel:${resource.phone}`}
                          onClick={(e) => e.stopPropagation()}
                          className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-700 font-mono text-xs font-bold border border-rose-200 transition-colors w-full justify-center shadow-xs"
                          title={`Emergency call to ${resource.phone}`}
                        >
                          <PhoneCall className="w-3.5 h-3.5 text-rose-600" />
                          <span>Tap to Call: {resource.phone}</span>
                        </a>
                      </div>
                    )}

                    {/* Services Pills */}
                    {resource.services && resource.services.length > 0 && (
                      <div className="flex flex-wrap gap-1 mb-4">
                        {resource.services.slice(0, 3).map((srv, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-0.5 rounded bg-paper-100 text-[10px] font-mono text-charcoal-700"
                          >
                            {srv}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Card Footer */}
                  <div className="pt-3.5 border-t border-paper-200 flex items-center justify-between text-xs font-mono">
                    <div className="truncate max-w-[170px] text-charcoal-500" title={resource.source}>
                      <span>{resource.source || 'Authorized Agency'}</span>
                    </div>

                    <div className="inline-flex items-center gap-1 text-charcoal-900 font-medium group-hover:translate-x-0.5 transition-transform shrink-0">
                      <span>Inspect</span>
                      <ExternalLink className="w-3.5 h-3.5" />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Resource Detail Modal */}
      {selectedResource && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-charcoal-950/50 backdrop-blur-xs">
          <div className="relative w-full max-w-2xl rounded-3xl bg-white border border-paper-300 p-6 sm:p-8 shadow-floating max-h-[90vh] overflow-y-auto">
            {/* Modal Header */}
            <div className="flex items-start justify-between gap-4 mb-4">
              <div>
                <div className="flex items-center gap-2 mb-1.5">
                  <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold">
                    {selectedResource.category} // {selectedResource.type}
                  </span>
                  <span className="inline-flex items-center gap-1 text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 font-bold">
                    <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                    <span>✓ Source Verified</span>
                  </span>
                </div>
                <h3 className="text-2xl font-bold text-charcoal-950">
                  {selectedResource.name}
                </h3>
              </div>
              <button
                onClick={() => setSelectedResource(null)}
                className="p-2 rounded-full hover:bg-paper-100 text-charcoal-500 hover:text-charcoal-950 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Body */}
            <div className="space-y-4 text-xs font-mono text-charcoal-700">
              <p className="text-sm font-sans text-charcoal-700 leading-relaxed">
                {selectedResource.description}
              </p>

              <div className="p-4 rounded-2xl bg-paper-50 border border-paper-200 space-y-2">
                <div className="flex justify-between">
                  <span className="text-charcoal-500">Jurisdiction / State:</span>
                  <strong className="text-charcoal-900">{selectedResource.state}</strong>
                </div>
                {selectedResource.district && (
                  <div className="flex justify-between">
                    <span className="text-charcoal-500">District:</span>
                    <strong className="text-charcoal-900">{selectedResource.district}</strong>
                  </div>
                )}
                {selectedResource.address && (
                  <div className="flex justify-between">
                    <span className="text-charcoal-500">Address:</span>
                    <span className="text-right text-charcoal-900 max-w-[280px]">{selectedResource.address}</span>
                  </div>
                )}
                {selectedResource.phone && (
                  <div className="flex justify-between items-center pt-1 border-t border-paper-200">
                    <span className="text-charcoal-500">Emergency Helpline:</span>
                    <a
                      href={`tel:${selectedResource.phone}`}
                      className="font-bold text-rose-600 hover:underline flex items-center gap-1"
                    >
                      <PhoneCall className="w-3 h-3" />
                      <span>{selectedResource.phone}</span>
                    </a>
                  </div>
                )}
              </div>

              {/* Services Offered */}
              {selectedResource.services && selectedResource.services.length > 0 && (
                <div>
                  <span className="font-bold text-charcoal-900 block mb-1.5">What They Provide:</span>
                  <div className="flex flex-wrap gap-1.5">
                    {selectedResource.services.map((srv, idx) => (
                      <span
                        key={idx}
                        className="px-2.5 py-1 rounded-lg bg-paper-100 text-charcoal-800 text-xs"
                      >
                        ✓ {srv}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Accessibility Notes */}
              {selectedResource.accessibilityNotes && (
                <div className="p-3 rounded-xl bg-blue-50/70 border border-blue-200 text-blue-950 flex items-start gap-2">
                  <Info className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
                  <span>{selectedResource.accessibilityNotes}</span>
                </div>
              )}

              {/* Attribution & Verification Meta */}
              <div className="pt-4 border-t border-paper-200 space-y-1.5 text-[11px] text-charcoal-500">
                <div className="flex justify-between">
                  <span>Authoritative Source:</span>
                  <strong className="text-charcoal-800">{selectedResource.source || 'Authorized Government Agency'}</strong>
                </div>
                <div className="flex justify-between">
                  <span>Verification Status:</span>
                  <span className="text-emerald-700 font-bold">{selectedResource.verificationStatus}</span>
                </div>
                <div className="flex justify-between">
                  <span>Freshness / Recency:</span>
                  <span>{selectedResource.freshness || 'Verified recently'} • {selectedResource.lastVerified || 'Current'}</span>
                </div>
              </div>
            </div>

            {/* Modal Actions */}
            <div className="mt-6 pt-4 border-t border-paper-200 flex flex-col sm:flex-row items-center justify-between gap-3">
              {selectedResource.website && (
                <a
                  href={selectedResource.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full sm:w-auto px-5 py-2.5 rounded-xl bg-charcoal-900 text-paper-50 text-xs font-mono font-bold hover:bg-charcoal-800 transition-colors flex items-center justify-center gap-1.5"
                >
                  <span>Open Official Organization Portal</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              )}
              <button
                onClick={() => setSelectedResource(null)}
                className="w-full sm:w-auto px-4 py-2.5 rounded-xl border border-paper-300 text-xs font-mono font-semibold text-charcoal-700 hover:bg-paper-100 transition-colors"
              >
                Close Details
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
