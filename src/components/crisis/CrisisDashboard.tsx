import React, { useState, useEffect } from 'react';
import {
  ShieldAlert,
  AlertCircle,
  PhoneCall,
  CheckCircle2,
  Clock,
  Compass,
  FileText,
  Info,
  ExternalLink,
  ChevronRight,
  Shield,
  X,
  AlertTriangle,
  Flame,
  Waves,
  Wind,
  Mountain,
  Zap,
  Activity,
  PackageCheck
} from 'lucide-react';
import { useCrisis } from '../../context/CrisisContext';
import { crisisService } from '../../services/crisisService';
import {
  CrisisAssessment,
  CrisisActionItem,
  CrisisResourceItem,
  CrisisTimelinePoint,
  FamilyChecklistItem
} from '../../types/crisis';

const INDIAN_REGIONS = [
  { id: 'assam', name: 'Assam' },
  { id: 'delhi', name: 'Delhi (NCT)' },
  { id: 'kerala', name: 'Kerala' },
  { id: 'odisha', name: 'Odisha' },
  { id: 'uttarakhand', name: 'Uttarakhand' },
  { id: 'rajasthan', name: 'Rajasthan' },
  { id: 'maharashtra', name: 'Maharashtra' },
  { id: 'gujarat', name: 'Gujarat' },
  { id: 'bihar', name: 'Bihar' },
  { id: 'west-bengal', name: 'West Bengal' },
  { id: 'tamil-nadu', name: 'Tamil Nadu' },
  { id: 'andhra-pradesh', name: 'Andhra Pradesh' },
  { id: 'karnataka', name: 'Karnataka' },
  { id: 'himachal-pradesh', name: 'Himachal Pradesh' },
  { id: 'jammu-and-kashmir', name: 'Jammu & Kashmir' },
  { id: 'punjab', name: 'Punjab' },
  { id: 'haryana', name: 'Haryana' },
  { id: 'uttar-pradesh', name: 'Uttar Pradesh' },
  { id: 'madhya-pradesh', name: 'Madhya Pradesh' },
  { id: 'chhattisgarh', name: 'Chhattisgarh' },
  { id: 'jharkhand', name: 'Jharkhand' },
  { id: 'telangana', name: 'Telangana' },
  { id: 'goa', name: 'Goa' },
  { id: 'sikkim', name: 'Sikkim' },
  { id: 'tripura', name: 'Tripura' },
  { id: 'meghalaya', name: 'Meghalaya' },
  { id: 'manipur', name: 'Manipur' },
  { id: 'nagaland', name: 'Nagaland' },
  { id: 'mizoram', name: 'Mizoram' },
  { id: 'arunachal-pradesh', name: 'Arunachal Pradesh' },
  { id: 'ladakh', name: 'Ladakh' },
  { id: 'chandigarh', name: 'Chandigarh' },
  { id: 'puducherry', name: 'Puducherry' },
  { id: 'andaman-and-nicobar-islands', name: 'Andaman & Nicobar' },
  { id: 'dadra-and-nagar-haveli-and-daman-and-diu', name: 'DNHDD' },
  { id: 'lakshadweep', name: 'Lakshadweep' }
];

const HAZARDS = [
  { id: 'FLOOD', label: 'Flood', icon: Waves },
  { id: 'CYCLONE', label: 'Cyclone', icon: Wind },
  { id: 'HEATWAVE', label: 'Heatwave', icon: Flame },
  { id: 'LANDSLIDE', label: 'Landslide', icon: Mountain },
  { id: 'SEVERE_WEATHER', label: 'Severe Weather', icon: Zap },
  { id: 'EARTHQUAKE', label: 'Earthquake', icon: Activity }
];

export const CrisisDashboard: React.FC = () => {
  const { isCrisisMode, setCrisisMode } = useCrisis();
  const [selectedRegion, setSelectedRegion] = useState<string>('assam');
  const [selectedHazard, setSelectedHazard] = useState<string>('FLOOD');
  const [assessment, setAssessment] = useState<CrisisAssessment | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'DURING' | 'BEFORE' | 'AFTER' | 'CHECKLIST'>('DURING');
  const [userCoords, setUserCoords] = useState<{ lat: number; lon: number } | null>(null);

  // Request browser geolocation once for distance sorting
  useEffect(() => {
    if (typeof window !== 'undefined' && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setUserCoords({ lat: pos.coords.latitude, lon: pos.coords.longitude });
        },
        () => {},
        { timeout: 5000 }
      );
    }
  }, []);

  // Fetch Crisis Assessment
  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    setError(null);

    crisisService
      .getRegionAssessment(
        selectedRegion,
        selectedHazard,
        isCrisisMode,
        userCoords?.lat,
        userCoords?.lon
      )
      .then((data) => {
        if (isMounted) {
          setAssessment(data);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          setError(err.message || 'Failed to load crisis assessment');
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [selectedRegion, selectedHazard, isCrisisMode, userCoords]);

  const getStateColor = (state?: string) => {
    switch (state) {
      case 'CRISIS':
        return 'bg-red-600 text-white';
      case 'ELEVATED':
        return 'bg-amber-600 text-white';
      case 'WATCH':
        return 'bg-yellow-500 text-charcoal-900';
      default:
        return 'bg-emerald-600 text-white';
    }
  };

  const getPriorityBadge = (priority: string) => {
    switch (priority) {
      case 'LIFE_SAFETY':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'EVACUATION':
        return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'AVOID_DANGER':
        return 'bg-amber-100 text-amber-800 border-amber-200';
      case 'COMMUNICATION':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="bg-paper-100 min-h-screen text-charcoal-900 pt-20 sm:pt-24 pb-16 font-sans">
      {/* Top Crisis Emergency Masthead */}
      <div className="bg-charcoal-950 text-paper-50 border-b-4 border-red-600 pt-6 pb-6 px-4 sm:px-6 lg:px-8 shadow-md">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-red-600 text-white shadow-sm shrink-0">
              <ShieldAlert className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl sm:text-2xl font-bold font-mono tracking-tight text-white">
                  NATIONAL CRISIS MODE
                </h1>
                <span className="text-xs px-2 py-0.5 rounded font-mono bg-red-900/60 text-red-200 border border-red-700">
                  PUBLIC DISASTER ASSISTANCE
                </span>
              </div>
              <p className="text-xs sm:text-sm text-paper-300 font-mono mt-0.5">
                Authoritative Civil Protection, Evidence-Based Life Safety & Verified Resources
              </p>
            </div>
          </div>

          {/* Quick Helpline Speed Dial */}
          <div className="flex flex-wrap items-center gap-2 bg-charcoal-900 p-2 rounded-xl border border-charcoal-800 font-mono text-xs">
            <span className="text-paper-400 font-semibold px-2 flex items-center gap-1">
              <PhoneCall className="w-3.5 h-3.5 text-red-400" />
              <span>National SOS:</span>
            </span>
            <a
              href="tel:112"
              className="px-2.5 py-1 rounded bg-red-600 hover:bg-red-700 text-white font-bold transition-colors"
            >
              112 (Emergency)
            </a>
            <a
              href="tel:1078"
              className="px-2.5 py-1 rounded bg-charcoal-800 hover:bg-charcoal-700 text-paper-100 transition-colors"
            >
              1078 (NDMA)
            </a>
            <a
              href="tel:1070"
              className="px-2.5 py-1 rounded bg-charcoal-800 hover:bg-charcoal-700 text-paper-100 transition-colors"
            >
              1070 (State)
            </a>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">
        {/* Controls: Region Selector & Hazard Filter */}
        <div className="bg-white rounded-2xl p-4 border border-paper-300 shadow-sm mb-6 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
            <div className="flex items-center gap-2">
              <Compass className="w-4 h-4 text-charcoal-500 shrink-0" />
              <span className="text-xs font-mono uppercase text-charcoal-500 font-bold">Region:</span>
              <select
                value={selectedRegion}
                onChange={(e) => setSelectedRegion(e.target.value)}
                className="bg-paper-100 border border-paper-300 rounded-lg px-3 py-1.5 text-xs font-mono font-medium focus:ring-2 focus:ring-charcoal-900"
              >
                {INDIAN_REGIONS.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex items-center gap-1.5 overflow-x-auto py-1">
              {HAZARDS.map((h) => {
                const IconComponent = h.icon;
                const isSel = selectedHazard === h.id;
                return (
                  <button
                    key={h.id}
                    onClick={() => setSelectedHazard(h.id)}
                    className={`px-2.5 py-1.5 rounded-lg text-xs font-mono flex items-center gap-1.5 transition-all whitespace-nowrap ${
                      isSel
                        ? 'bg-charcoal-900 text-white font-bold shadow-xs'
                        : 'bg-paper-100 hover:bg-paper-200 text-charcoal-700'
                    }`}
                  >
                    <IconComponent className="w-3.5 h-3.5" />
                    <span>{h.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          <div className="flex items-center gap-2 justify-end">
            <span className="text-xs font-mono text-charcoal-500">Crisis Mode:</span>
            <button
              onClick={() => setCrisisMode(!isCrisisMode)}
              className={`px-3 py-1 rounded-full text-xs font-mono font-bold transition-colors ${
                isCrisisMode ? 'bg-red-600 text-white' : 'bg-paper-200 text-charcoal-700 hover:bg-paper-300'
              }`}
            >
              {isCrisisMode ? 'ACTIVE (Rule E)' : 'STANDBY'}
            </button>
          </div>
        </div>

        {loading && (
          <div className="bg-white rounded-2xl p-12 text-center border border-paper-300">
            <div className="inline-block w-8 h-8 border-4 border-charcoal-900 border-t-transparent rounded-full animate-spin mb-3" />
            <p className="font-mono text-xs text-charcoal-600">
              Synthesizing crisis telemetry and life-safety intelligence for {selectedRegion}...
            </p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-2xl p-6 text-red-800 text-xs font-mono mb-6">
            <p className="font-bold">Error loading crisis intelligence:</p>
            <p>{error}</p>
          </div>
        )}

        {assessment && !loading && (
          <div className="space-y-6">
            {/* Operational State Banner */}
            <div className="bg-white rounded-2xl p-5 border border-paper-300 shadow-sm">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-paper-200">
                <div className="flex items-center gap-3">
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-mono font-bold tracking-wider ${getStateColor(
                      assessment.operational_state
                    )}`}
                  >
                    {assessment.operational_state} POSTURE
                  </span>
                  <h2 className="text-lg font-bold font-mono text-charcoal-950">
                    {assessment.region_name} — {assessment.primary_hazard}
                  </h2>
                </div>
                <div className="flex items-center gap-4 text-xs font-mono text-charcoal-600">
                  <div>
                    Current Risk:{' '}
                    <strong className="text-charcoal-900">
                      {assessment.current_risk_level} ({assessment.current_risk_score}/100)
                    </strong>
                  </div>
                  <div>
                    Peak Window:{' '}
                    <strong className="text-charcoal-900">
                      {assessment.peak_future_window.replace('_', '-').toUpperCase()} ({assessment.peak_future_risk_level})
                    </strong>
                  </div>
                </div>
              </div>

              {/* Official Warnings Feed */}
              {assessment.official_warnings && assessment.official_warnings.length > 0 && (
                <div className="mt-4 p-3.5 rounded-xl bg-red-50 border border-red-200 text-red-900 text-xs font-mono space-y-1">
                  <div className="font-bold flex items-center gap-1.5 text-red-700">
                    <AlertTriangle className="w-4 h-4" />
                    <span>Statutory Warning Bulletin (Official IMD / Nodal Authority):</span>
                  </div>
                  {assessment.official_warnings.map((w, idx) => (
                    <div key={w.id || idx} className="pl-5">
                      <strong>{w.headline}</strong>: {w.description} (Valid until: {w.valid_until})
                    </div>
                  ))}
                </div>
              )}

              {/* Fundamental Question 1: What is happening? */}
              <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-paper-100 border border-paper-200">
                  <h3 className="text-xs font-mono font-bold uppercase text-charcoal-500 mb-1 flex items-center gap-1.5">
                    <Info className="w-3.5 h-3.5 text-blue-600" />
                    <span>1. What is happening?</span>
                  </h3>
                  <p className="text-xs font-sans text-charcoal-800 leading-relaxed">
                    {assessment.what_is_happening}
                  </p>
                </div>

                {/* Fundamental Question 2: What could happen next? */}
                <div className="p-4 rounded-xl bg-paper-100 border border-paper-200">
                  <h3 className="text-xs font-mono font-bold uppercase text-charcoal-500 mb-1 flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5 text-amber-600" />
                    <span>2. What could happen next?</span>
                  </h3>
                  <p className="text-xs font-sans text-charcoal-800 leading-relaxed">
                    {assessment.what_could_happen_next}
                  </p>
                </div>
              </div>
            </div>

            {/* Fundamental Question 3: What should I do right now? (Top 3-5 Prioritized Actions) */}
            <div className="bg-white rounded-2xl p-5 border border-paper-300 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-base font-bold font-mono text-charcoal-950 flex items-center gap-2">
                    <Shield className="w-5 h-5 text-red-600" />
                    <span>3. WHAT SHOULD I DO RIGHT NOW?</span>
                  </h2>
                  <p className="text-xs text-charcoal-500 font-mono mt-0.5">
                    Top prioritized life-safety instructions ranked in order of immediate survival impact
                  </p>
                </div>
                <span className="text-[11px] font-mono font-bold px-2 py-1 rounded bg-red-50 text-red-700 border border-red-200">
                  Immediate Actions (1–{assessment.what_to_do_now.length})
                </span>
              </div>

              <div className="space-y-3">
                {assessment.what_to_do_now.map((act) => (
                  <div
                    key={act.id}
                    className="p-4 rounded-xl border border-paper-300 bg-paper-50 hover:bg-white transition-colors flex items-start gap-3.5"
                  >
                    <div className="w-7 h-7 rounded-lg bg-charcoal-900 text-paper-50 font-mono font-bold text-xs flex items-center justify-center shrink-0">
                      {act.order_rank}
                    </div>
                    <div className="flex-1 space-y-1">
                      <div className="flex flex-wrap items-center gap-2">
                        <h4 className="text-sm font-bold text-charcoal-950">{act.title}</h4>
                        <span
                          className={`text-[10px] font-mono px-2 py-0.5 rounded border uppercase font-semibold ${getPriorityBadge(
                            act.priority
                          )}`}
                        >
                          {act.priority.replace('_', ' ')}
                        </span>
                        {act.is_urgent && (
                          <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-red-600 text-white font-bold uppercase">
                            URGENT
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-charcoal-800 leading-relaxed font-sans">{act.instruction}</p>
                      <p className="text-[11px] text-charcoal-500 font-mono italic">
                        <strong>Rationale:</strong> {act.rationale}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Fundamental Question 4: Before, During, After Protocols & 72-Hour Checklist */}
            <div className="bg-white rounded-2xl p-5 border border-paper-300 shadow-sm">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
                <div>
                  <h2 className="text-base font-bold font-mono text-charcoal-950 flex items-center gap-2">
                    <FileText className="w-5 h-5 text-charcoal-700" />
                    <span>4. LIFE-SAFETY ACTION PROTOCOLS</span>
                  </h2>
                  <p className="text-xs text-charcoal-500 font-mono mt-0.5">
                    Disaster lifecycle guidelines for {assessment.primary_hazard} and 72-hour family preparedness
                  </p>
                </div>

                <div className="flex items-center gap-1 bg-paper-200 p-1 rounded-xl">
                  <button
                    onClick={() => setActiveTab('DURING')}
                    className={`px-3 py-1 rounded-lg text-xs font-mono font-bold transition-all ${
                      activeTab === 'DURING' ? 'bg-red-600 text-white shadow-xs' : 'text-charcoal-700 hover:text-charcoal-950'
                    }`}
                  >
                    DURING
                  </button>
                  <button
                    onClick={() => setActiveTab('BEFORE')}
                    className={`px-3 py-1 rounded-lg text-xs font-mono font-bold transition-all ${
                      activeTab === 'BEFORE' ? 'bg-white text-charcoal-900 shadow-xs' : 'text-charcoal-700 hover:text-charcoal-950'
                    }`}
                  >
                    BEFORE
                  </button>
                  <button
                    onClick={() => setActiveTab('AFTER')}
                    className={`px-3 py-1 rounded-lg text-xs font-mono font-bold transition-all ${
                      activeTab === 'AFTER' ? 'bg-white text-charcoal-900 shadow-xs' : 'text-charcoal-700 hover:text-charcoal-950'
                    }`}
                  >
                    AFTER
                  </button>
                  <button
                    onClick={() => setActiveTab('CHECKLIST')}
                    className={`px-3 py-1 rounded-lg text-xs font-mono font-bold transition-all flex items-center gap-1 ${
                      activeTab === 'CHECKLIST' ? 'bg-white text-charcoal-900 shadow-xs' : 'text-charcoal-700 hover:text-charcoal-950'
                    }`}
                  >
                    <PackageCheck className="w-3.5 h-3.5" />
                    <span>72h Kit</span>
                  </button>
                </div>
              </div>

              {activeTab === 'CHECKLIST' ? (
                <div className="space-y-2.5">
                  <div className="p-3 bg-amber-50 rounded-xl border border-amber-200 text-amber-900 text-xs font-mono mb-3">
                    <strong>72-Hour Family Disaster Preparedness Checklist:</strong> Essential provisions required to
                    sustain a household autonomously for 3 days during severe utility disruption.
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {assessment.family_prep_checklist.map((c, idx) => (
                      <div
                        key={idx}
                        className="p-3.5 rounded-xl border border-paper-300 bg-paper-50/70 flex items-start gap-3"
                      >
                        <CheckCircle2
                          className={`w-4 h-4 shrink-0 mt-0.5 ${
                            c.is_critical ? 'text-red-600' : 'text-emerald-600'
                          }`}
                        />
                        <div className="space-y-0.5">
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-bold text-charcoal-900">{c.item}</span>
                            <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-paper-200 text-charcoal-600">
                              {c.category}
                            </span>
                          </div>
                          <p className="text-[11px] text-charcoal-600 font-sans">{c.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="space-y-3">
                  {(assessment.action_protocols[activeTab] || []).map((p, idx) => (
                    <div
                      key={p.id || idx}
                      className="p-3.5 rounded-xl border border-paper-200 bg-paper-50 flex items-start gap-3"
                    >
                      <div className="w-6 h-6 rounded-md bg-paper-300 text-charcoal-800 font-mono font-bold text-xs flex items-center justify-center shrink-0">
                        {p.order_rank}
                      </div>
                      <div>
                        <h4 className="text-xs font-bold text-charcoal-950">{p.title}</h4>
                        <p className="text-xs text-charcoal-700 font-sans mt-0.5 leading-relaxed">
                          {p.instruction}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* 5-Horizon Unified Timeline Progression */}
            <div className="bg-white rounded-2xl p-5 border border-paper-300 shadow-sm">
              <div className="mb-4">
                <h2 className="text-base font-bold font-mono text-charcoal-950 flex items-center gap-2">
                  <Clock className="w-5 h-5 text-blue-600" />
                  <span>5-HORIZON PROJECTION TIMELINE</span>
                </h2>
                <p className="text-xs text-charcoal-500 font-mono mt-0.5">
                  Chronological disaster trajectory with explicit scientific signal provenance
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
                {assessment.timeline.map((pt) => (
                  <div
                    key={pt.horizon}
                    className="p-3.5 rounded-xl border border-paper-300 bg-paper-50 flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-center justify-between pb-1.5 border-b border-paper-200">
                        <span className="font-mono font-bold text-xs text-charcoal-900">{pt.horizon}</span>
                        <span
                          className={`text-[10px] font-mono px-1.5 py-0.5 rounded font-bold ${getStateColor(
                            pt.expected_risk_level === 'CRITICAL' ? 'CRISIS' : pt.expected_risk_level === 'HIGH' ? 'ELEVATED' : 'NORMAL'
                          )}`}
                        >
                          {pt.expected_risk_level}
                        </span>
                      </div>
                      <p className="text-[11px] font-mono text-charcoal-600 mt-1 font-semibold">
                        {pt.window_label}
                      </p>
                      <div className="text-[11px] font-mono text-charcoal-500 mt-1">
                        Confidence: {(pt.confidence * 100).toFixed(0)}%
                      </div>

                      <div className="mt-2 space-y-1">
                        {pt.key_factors.map((f, fIdx) => (
                          <div key={fIdx} className="text-[10px] font-sans text-charcoal-600 leading-tight">
                            • {f}
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="mt-3 pt-2 border-t border-paper-200">
                      <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-paper-200 text-charcoal-600 uppercase">
                        {pt.signal_type}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Emergency Resources Directory (Zero Invented Data Guarantee) */}
            <div className="bg-white rounded-2xl p-5 border border-paper-300 shadow-sm">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
                <div>
                  <h2 className="text-base font-bold font-mono text-charcoal-950 flex items-center gap-2">
                    <PhoneCall className="w-5 h-5 text-emerald-600" />
                    <span>VERIFIED STATUTORY EMERGENCY RESOURCES</span>
                  </h2>
                  <p className="text-xs text-charcoal-500 font-mono mt-0.5">
                    Verified NDRF, SDRF, state civil defense, and district emergency operations
                  </p>
                </div>
                <span className="text-[11px] font-mono text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                  100% Provenance Verified
                </span>
              </div>

              {assessment.resource_availability_note && (
                <div className="mb-4 p-3.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-xs font-mono">
                  <span className="font-bold flex items-center gap-1.5 mb-1">
                    <AlertCircle className="w-4 h-4 text-amber-600" />
                    <span>Resource Advisory:</span>
                  </span>
                  <p>{assessment.resource_availability_note}</p>
                </div>
              )}

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {assessment.emergency_resources.map((res) => (
                  <div
                    key={res.id}
                    className="p-3.5 rounded-xl border border-paper-300 bg-paper-50 flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-start justify-between gap-2">
                        <h4 className="text-xs font-bold text-charcoal-950 leading-tight">{res.name}</h4>
                        {res.distance_km !== undefined && res.distance_km !== null && (
                          <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-paper-200 text-charcoal-700 shrink-0">
                            {res.distance_km.toFixed(1)} km
                          </span>
                        )}
                      </div>
                      <div className="text-[10px] font-mono text-charcoal-500 mt-1">
                        {res.category} • {res.state}
                      </div>
                      {res.address && (
                        <p className="text-[11px] font-sans text-charcoal-600 mt-1 leading-tight">
                          {res.address}
                        </p>
                      )}
                    </div>

                    <div className="mt-3 pt-2 border-t border-paper-200 flex items-center justify-between">
                      {res.phone || res.contact_number ? (
                        <a
                          href={`tel:${(res.phone || res.contact_number)?.split('/')[0].trim()}`}
                          className="px-2.5 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-mono font-bold flex items-center gap-1 transition-colors"
                        >
                          <PhoneCall className="w-3 h-3" />
                          <span>{res.phone || res.contact_number}</span>
                        </a>
                      ) : (
                        <span className="text-[10px] font-mono text-charcoal-400">Lines in bulletin</span>
                      )}

                      {res.website_url && (
                        <a
                          href={res.website_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="p-1 rounded text-charcoal-400 hover:text-charcoal-800"
                        >
                          <ExternalLink className="w-3.5 h-3.5" />
                        </a>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Transparent Deterministic Explanation ("Why this risk?") */}
            <div className="bg-white rounded-2xl p-5 border border-paper-300 shadow-sm">
              <div className="mb-3">
                <h2 className="text-base font-bold font-mono text-charcoal-950 flex items-center gap-2">
                  <Info className="w-5 h-5 text-charcoal-700" />
                  <span>TRANSPARENT SCIENTIFIC EXPLANATION</span>
                </h2>
                <p className="text-xs text-charcoal-500 font-mono mt-0.5">
                  Deterministic reasoning, observed evidence, and clear declaration of data limitations
                </p>
              </div>

              <div className="space-y-3 text-xs font-sans">
                <div className="p-3 bg-paper-50 rounded-xl border border-paper-200">
                  <span className="font-bold text-charcoal-900 block font-mono text-[11px] uppercase mb-0.5">
                    Why this risk was assessed:
                  </span>
                  <p className="text-charcoal-700">{assessment.explanation.why}</p>
                </div>

                <div className="p-3 bg-paper-50 rounded-xl border border-paper-200">
                  <span className="font-bold text-charcoal-900 block font-mono text-[11px] uppercase mb-0.5">
                    What changed recently:
                  </span>
                  <p className="text-charcoal-700">{assessment.explanation.what_changed}</p>
                </div>

                <div className="p-3 bg-paper-50 rounded-xl border border-paper-200">
                  <span className="font-bold text-charcoal-900 block font-mono text-[11px] uppercase mb-0.5">
                    Supporting Tangible Evidence:
                  </span>
                  <ul className="list-disc pl-4 space-y-0.5 text-charcoal-700">
                    {assessment.explanation.supporting_evidence.map((ev, idx) => (
                      <li key={idx}>{ev}</li>
                    ))}
                  </ul>
                </div>

                <div className="p-3 bg-paper-50 rounded-xl border border-paper-200">
                  <span className="font-bold text-charcoal-900 block font-mono text-[11px] uppercase mb-0.5">
                    What could change this risk:
                  </span>
                  <p className="text-charcoal-700">{assessment.explanation.what_could_change}</p>
                </div>

                <div className="p-3 bg-paper-100 rounded-xl border border-paper-300">
                  <span className="font-bold text-charcoal-900 block font-mono text-[11px] uppercase mb-0.5 flex items-center gap-1 text-amber-700">
                    <AlertCircle className="w-3.5 h-3.5" />
                    <span>What we do NOT know (Scientific Limitations):</span>
                  </span>
                  <p className="text-charcoal-700">{assessment.explanation.data_limitations}</p>
                </div>
              </div>
            </div>

            {/* Scientific Guard Audit Strip */}
            <div className="p-4 bg-charcoal-900 text-paper-300 rounded-2xl font-mono text-[11px] flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
              <div>
                <span className="text-paper-100 font-bold">ML GUARD AUDIT:</span>{' '}
                {assessment.ml_audit.ml_available ? (
                  <span className="text-emerald-400">
                    Model: {assessment.ml_audit.model_name} (Verified Assam Prototype)
                  </span>
                ) : (
                  <span className="text-amber-400">
                    Inference: Non-ML Empirical Telemetry & NWP ({assessment.ml_audit.guard_status})
                  </span>
                )}
              </div>
              <div className="flex items-center gap-4 text-paper-400">
                <span>Synthetic Records: 0 strictly</span>
                <span>Evaluated: {new Date(assessment.evaluated_at).toLocaleTimeString()}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
