import React, { useState } from 'react';
import {
  PhoneCall,
  ShieldAlert,
  X,
  Copy,
  Check,
  LifeBuoy,
  AlertTriangle,
  Info,
  Waves,
  Mountain,
  Wind,
  Sun,
  Activity,
  FileText,
  CloudLightning
} from 'lucide-react';

export interface HelplineInfo {
  number: string;
  name: string;
  agency: string;
  usage: string;
  priority: 'CRITICAL' | 'HIGH' | 'SUPPORT';
}

export const EMERGENCY_NUMBERS: HelplineInfo[] = [
  {
    number: '112',
    name: 'National Emergency Number',
    agency: 'Emergency Response Support System (ERSS)',
    usage: 'Unified all-in-one emergency response for Police, Fire, and Ambulance dispatch across India.',
    priority: 'CRITICAL'
  },
  {
    number: '1078',
    name: 'National Disaster Helpline',
    agency: 'National Disaster Management Authority (NDMA)',
    usage: '24x7 central emergency operations control room for flood, cyclone, earthquake, and major disaster emergencies.',
    priority: 'CRITICAL'
  },
  {
    number: '1070',
    name: 'State Disaster Emergency Desk',
    agency: 'State Disaster Management Authority (SDMA SEOC)',
    usage: 'State-level disaster coordination, relief center allocations, and district rescue deployments.',
    priority: 'CRITICAL'
  },
  {
    number: '108',
    name: 'Emergency Medical & Ambulance',
    agency: 'National Health Mission / State EMS',
    usage: 'Immediate medical trauma, critical injury transport, and urgent hospital transfer.',
    priority: 'HIGH'
  },
  {
    number: '101',
    name: 'Fire Services',
    agency: 'State Fire & Rescue Services',
    usage: 'Building fire, industrial hazards, urban search & rescue, and collapsed structures.',
    priority: 'HIGH'
  },
  {
    number: '100',
    name: 'Police Assistance',
    agency: 'State Police Departments',
    usage: 'Law and order, crowd control, public safety, and emergency cordon enforcement.',
    priority: 'HIGH'
  },
  {
    number: '1077',
    name: 'District Disaster Operations Center',
    agency: 'District Collectorate / Magistrate DDMA',
    usage: 'District-specific relief camp queries, local road passability, and ration distribution info.',
    priority: 'SUPPORT'
  },
  {
    number: '1098',
    name: 'National Childline',
    agency: 'Ministry of Women and Child Development',
    usage: 'Emergency protection and assistance for displaced or unaccompanied children during crisis.',
    priority: 'SUPPORT'
  },
  {
    number: '1091',
    name: 'Women Emergency Helpline',
    agency: 'National Commission for Women / Police',
    usage: 'Dedicated 24/7 protection and assistance for women facing crisis or distress.',
    priority: 'SUPPORT'
  }
];

export interface SafetyProtocol {
  hazard: string;
  icon: typeof Waves;
  dos: string[];
  donts: string[];
}

export const BASIC_SAFETY_PROTOCOLS: SafetyProtocol[] = [
  {
    hazard: 'Flood & Inundation',
    icon: Waves,
    dos: [
      'Move immediately to designated higher ground or elevated multi-story relief centers.',
      'Turn off main electricity switch and cooking gas valve before evacuating.',
      'Drink only boiled or chemically disinfected bottled water.'
    ],
    donts: [
      'Do not walk or drive through moving water (15 cm of moving water can sweep an adult).',
      'Do not touch submerged electrical appliances or downed wiring.',
      'Do not consume food that has come into contact with flood waters.'
    ]
  },
  {
    hazard: 'Earthquake',
    icon: Activity,
    dos: [
      'DROP to your hands and knees, COVER your head and neck under sturdy furniture, and HOLD ON.',
      'If outdoors, move to an open area away from electrical cables, facades, and tall trees.',
      'Expect aftershocks and use stairs (never elevators) when evacuating.'
    ],
    donts: [
      'Do not panic or rush toward building exits during ground shaking.',
      'Do not stand near heavy wall hangings, mirrors, or unanchored glass windows.',
      'Do not light matches or candles due to potential gas line leaks.'
    ]
  },
  {
    hazard: 'Cyclone & High Winds',
    icon: Wind,
    dos: [
      'Stay securely indoors in the strongest, windowless part of the house until official all-clear is given.',
      'Keep battery-powered transistor radios tuned to All India Radio / IMD weather bulletins.',
      'Secure loose roof sheets, solar panels, and outdoor equipment before wind speeds peak.'
    ],
    donts: [
      'Do not go outside during the calm "eye" of the cyclone; violent winds will resume from the opposite direction.',
      'Do not venture out to sea or nearby beaches until authorized ports issue clearance.',
      'Do not spread unverified social media rumors regarding landfall timings.'
    ]
  },
  {
    hazard: 'Heatwave',
    icon: Sun,
    dos: [
      'Drink water frequently (ORS, lemon water, buttermilk), even if not feeling thirsty.',
      'Wear lightweight, loose-fitting, light-colored cotton clothing.',
      'Schedule strenuous outdoor labor strictly during cooler dawn and late evening hours.'
    ],
    donts: [
      'Do not step outside during peak solar radiation hours (11:00 AM to 4:00 PM).',
      'Do not leave children, elderly, or pets inside parked vehicles with closed windows.',
      'Do not consume alcohol, carbonated soft drinks, or heavy caffeine which accelerates dehydration.'
    ]
  },
  {
    hazard: 'Landslide & Hill Slope Failure',
    icon: Mountain,
    dos: [
      'Evacuate immediately if you observe new slope fissures, tilted trees, or muddy spring discharge.',
      'Stay alert during prolonged heavy rainfall; listen for unusual sounds like trees cracking.',
      'Heed state highway police closures on ghat and mountain roads.'
    ],
    donts: [
      'Do not camp, park, or build along steep cut-slopes or natural drainage ravines.',
      'Do not attempt to drive through recent debris deposits on mountain corridors.',
      'Do not cross swollen mountain torrents during cloudburst events.'
    ]
  },
  {
    hazard: 'Severe Weather & Lightning',
    icon: CloudLightning,
    dos: [
      'Seek shelter inside a substantial, enclosed building or metal vehicle immediately upon hearing thunder.',
      'Unplug sensitive electronic devices and avoid using corded landline phones during active electrical storms.',
      'Stay away from tall isolated trees, open fields, metal fences, and water bodies until 30 minutes after last thunder.'
    ],
    donts: [
      'Do not take shelter under solitary tall trees or tin sheds in open grounds.',
      'Do not touch electrical conduit, plumbing pipes, or wired equipment while lightning is active.',
      'Do not lie flat on open ground; crouch low on the balls of your feet with hands over ears if caught outdoors.'
    ]
  }
];

interface EmergencyAccessHubProps {
  isOpen: boolean;
  onClose: () => void;
  defaultTab?: 'numbers' | 'safety' | 'limitations';
}

export const EmergencyAccessHub: React.FC<EmergencyAccessHubProps> = ({
  isOpen,
  onClose,
  defaultTab = 'numbers'
}) => {
  const [activeTab, setActiveTab] = useState<'numbers' | 'safety' | 'limitations'>(defaultTab);
  const [copiedNumber, setCopiedNumber] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleCopy = (num: string) => {
    try {
      navigator.clipboard.writeText(num);
      setCopiedNumber(num);
      setTimeout(() => setCopiedNumber(null), 2000);
    } catch {
      // Fallback
    }
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="emergency-hub-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-charcoal-950/70 backdrop-blur-sm animate-in fade-in duration-150"
    >
      <div className="relative w-full max-w-2xl max-h-[90vh] flex flex-col rounded-3xl bg-white border border-paper-300 shadow-floating overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-paper-200 bg-rose-50/50">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-rose-600 text-white flex items-center justify-center shadow-xs">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <h2 id="emergency-hub-title" className="text-base font-bold text-charcoal-950 flex items-center gap-2">
                Emergency Access Hub
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-rose-100 text-rose-800 font-semibold border border-rose-200">
                  OFFLINE READY
                </span>
              </h2>
              <p className="text-xs text-charcoal-600">
                Official Indian helplines and immediate crisis safety guidance
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-xl text-charcoal-400 hover:text-charcoal-800 hover:bg-paper-200/60 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-charcoal-900"
            aria-label="Close emergency modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Switcher */}
        <div className="flex border-b border-paper-200 px-5 pt-2 bg-paper-50/60 gap-2">
          <button
            onClick={() => setActiveTab('numbers')}
            className={`pb-2.5 px-3 text-xs font-semibold border-b-2 transition-colors flex items-center gap-1.5 ${
              activeTab === 'numbers'
                ? 'border-rose-600 text-rose-700'
                : 'border-transparent text-charcoal-600 hover:text-charcoal-900'
            }`}
          >
            <PhoneCall className="w-3.5 h-3.5" />
            <span>Helplines (112, 1078...)</span>
          </button>
          <button
            onClick={() => setActiveTab('safety')}
            className={`pb-2.5 px-3 text-xs font-semibold border-b-2 transition-colors flex items-center gap-1.5 ${
              activeTab === 'safety'
                ? 'border-rose-600 text-rose-700'
                : 'border-transparent text-charcoal-600 hover:text-charcoal-900'
            }`}
          >
            <LifeBuoy className="w-3.5 h-3.5" />
            <span>Crisis Safety Protocols</span>
          </button>
          <button
            onClick={() => setActiveTab('limitations')}
            className={`pb-2.5 px-3 text-xs font-semibold border-b-2 transition-colors flex items-center gap-1.5 ${
              activeTab === 'limitations'
                ? 'border-rose-600 text-rose-700'
                : 'border-transparent text-charcoal-600 hover:text-charcoal-900'
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Safety Limitations</span>
          </button>
        </div>

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto p-5 space-y-4">
          {/* TAB 1: NUMBERS */}
          {activeTab === 'numbers' && (
            <div className="space-y-3">
              <div className="p-3 rounded-2xl bg-amber-50 border border-amber-200 text-xs text-amber-900 flex items-start gap-2.5">
                <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                <div className="space-y-1 leading-relaxed">
                  <span className="font-bold">Life-Safety Notice:</span> Helpline availability depends on telecom connectivity and state/district dispatch networks. In immediate danger, contact local emergency services directly. Official local district administration orders supersede all app indicators.
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                {EMERGENCY_NUMBERS.map((item) => (
                  <div
                    key={item.number}
                    className={`p-3.5 rounded-2xl border transition-all flex flex-col justify-between ${
                      item.priority === 'CRITICAL'
                        ? 'bg-rose-50/40 border-rose-200 hover:border-rose-300'
                        : 'bg-white border-paper-300 hover:border-paper-400'
                    }`}
                  >
                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs font-bold text-charcoal-900">{item.name}</span>
                        <span className="text-[10px] font-mono uppercase px-1.5 py-0.2 rounded bg-paper-200 text-charcoal-700 font-semibold">
                          {item.priority}
                        </span>
                      </div>
                      <p className="text-[11px] text-charcoal-500 font-mono mb-2">{item.agency}</p>
                      <p className="text-xs text-charcoal-600 leading-relaxed mb-3">{item.usage}</p>
                    </div>

                    <div className="flex items-center gap-2 pt-2 border-t border-paper-200/80">
                      <a
                        href={`tel:${item.number}`}
                        className="flex-1 min-h-[44px] py-2 px-3 rounded-xl bg-charcoal-900 text-white hover:bg-charcoal-800 transition-colors flex items-center justify-center gap-2 text-sm font-mono font-bold focus:outline-none focus-visible:ring-2 focus-visible:ring-charcoal-900"
                        title={`Tap to call ${item.name} at ${item.number}`}
                      >
                        <PhoneCall className="w-3.5 h-3.5 text-rose-400" />
                        <span>Call {item.number}</span>
                      </a>
                      <button
                        type="button"
                        onClick={() => handleCopy(item.number)}
                        className="min-h-[44px] min-w-[44px] p-2 rounded-xl border border-paper-300 hover:bg-paper-100 text-charcoal-700 transition-colors flex items-center justify-center"
                        title={`Copy number ${item.number} to clipboard`}
                        aria-label={`Copy number ${item.number}`}
                      >
                        {copiedNumber === item.number ? (
                          <Check className="w-4 h-4 text-emerald-600" />
                        ) : (
                          <Copy className="w-4 h-4" />
                        )}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 2: CRISIS SAFETY PROTOCOLS */}
          {activeTab === 'safety' && (
            <div className="space-y-4">
              <p className="text-xs text-charcoal-600">
                Actionable life-safety instructions for common natural hazards in India. Accessible 100% offline without cellular data.
              </p>
              <div className="space-y-3">
                {BASIC_SAFETY_PROTOCOLS.map((protocol) => {
                  const Icon = protocol.icon;
                  return (
                    <div key={protocol.hazard} className="p-4 rounded-2xl bg-paper-50 border border-paper-300">
                      <div className="flex items-center gap-2 mb-2.5">
                        <div className="w-7 h-7 rounded-lg bg-charcoal-900 text-paper-50 flex items-center justify-center">
                          <Icon className="w-4 h-4" />
                        </div>
                        <h3 className="text-sm font-bold text-charcoal-950">{protocol.hazard}</h3>
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                        <div className="p-3 rounded-xl bg-emerald-50/70 border border-emerald-200">
                          <span className="font-mono text-[10px] uppercase font-bold text-emerald-800 block mb-1">
                            DO THIS IMMEDIATELY
                          </span>
                          <ul className="space-y-1.5 text-emerald-950 list-disc list-inside">
                            {protocol.dos.map((item, idx) => (
                              <li key={idx} className="leading-snug">{item}</li>
                            ))}
                          </ul>
                        </div>
                        <div className="p-3 rounded-xl bg-rose-50/70 border border-rose-200">
                          <span className="font-mono text-[10px] uppercase font-bold text-rose-800 block mb-1">
                            DO NOT DO THIS
                          </span>
                          <ul className="space-y-1.5 text-rose-950 list-disc list-inside">
                            {protocol.donts.map((item, idx) => (
                              <li key={idx} className="leading-snug">{item}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* TAB 3: SAFETY LIMITATIONS & DISCLOSURE */}
          {activeTab === 'limitations' && (
            <div className="space-y-3 text-xs leading-relaxed text-charcoal-700">
              <div className="p-4 rounded-2xl bg-white border border-paper-300 space-y-3">
                <h3 className="text-sm font-bold text-charcoal-950 flex items-center gap-2">
                  <Info className="w-4 h-4 text-blue-600" />
                  <span>Public Decision-Support Information Scope</span>
                </h3>
                <p>
                  <strong>1. Decision-Support Platform Only:</strong> RISK // INDIA aggregates public disaster telemetry, baseline hazard indices, and verified relief registries. It is intended to assist citizen awareness and preparedness. It does NOT replace statutory early warning broadcasts or emergency sirens.
                </p>
                <p>
                  <strong>2. Official Evacuation Orders Take Precedence:</strong> In all disaster situations, evacuation instructions, curfew advisories, and shelter allocations issued by the local District Collector, Superintendent of Police, or SDMA are legally binding and paramount.
                </p>
                <p>
                  <strong>3. Upstream Telemetry Latency:</strong> Live sensor feeds (USGS seismographs, CWC river level gauges, IMD radar stations) are subject to network transmission delays and physical gauge disruption during extreme catastrophic events.
                </p>
                <p>
                  <strong>4. Machine Learning Model Boundaries:</strong> The empirical flood prediction prototype (<code>assam_flood_prototype_v1</code>) was calibrated exclusively on historical flood observations in the Brahmaputra and Barak river basins of Assam. It is not calibrated for nationwide flood prediction, cyclones, or seismic events. Outside Assam, only regional baseline susceptibility and verified live alerts are displayed.
                </p>
                <p>
                  <strong>5. Immediate Threat to Life:</strong> Do not rely on mobile web applications when immediate physical evacuation or rescue is required. Contact first responders immediately at <strong>112</strong> or your local district control room at <strong>1077</strong>.
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-5 py-3 border-t border-paper-200 bg-paper-50 flex items-center justify-between text-xs font-mono text-charcoal-500">
          <span>Pan-India Emergency Response</span>
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-charcoal-900 text-white text-xs font-bold hover:bg-charcoal-800 transition-colors"
          >
            Close Hub
          </button>
        </div>
      </div>
    </div>
  );
};
