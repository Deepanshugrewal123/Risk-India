import React, { useState } from 'react';
import {
  ShieldCheck,
  Clock,
  CheckCircle2,
  CheckSquare,
  Square,
  PhoneCall,
  AlertTriangle,
  FileCheck2,
  HeartHandshake,
  ExternalLink,
  Droplet,
  Package,
  Radio,
  FileText
} from 'lucide-react';

interface KitItem {
  id: string;
  category: string;
  name: string;
  detail: string;
}

const FAMILY_KIT_8_CATEGORIES: KitItem[] = [
  {
    id: 'kit-water',
    category: '1. Water & Hydration',
    name: 'Drinking Water (3 Litres/Person/Day)',
    detail: 'Minimum 3-day supply in clean, food-grade sealed containers for drinking and sanitation.'
  },
  {
    id: 'kit-food',
    category: '2. Emergency Rations',
    name: 'Non-Perishable Food Supply (3-Day)',
    detail: 'High-calorie dry grains, puffed rice, ready-to-eat meals, dry fruits, energy bars, manual can opener.'
  },
  {
    id: 'kit-medical',
    category: '3. First Aid & Prescription Meds',
    name: 'First Aid Kit & 7-Day Chronic Medication',
    detail: 'Sterile bandages, antiseptic liquid, ORS packets, thermal blanket, insulin, inhalers, blood pressure tablets.'
  },
  {
    id: 'kit-lighting',
    category: '4. Emergency Lighting & Radio',
    name: 'Battery / Hand-Crank Radio & Flashlights',
    detail: 'Essential for receiving All India Radio / IMD bulletins during grid power blackout; spare batteries.'
  },
  {
    id: 'kit-power',
    category: '5. Power & Communication',
    name: 'Heavy-Duty Power Banks & Backup Cables',
    detail: 'Store charged power banks in sealed waterproof zip bags; written paper sheet with family & emergency numbers.'
  },
  {
    id: 'kit-docs',
    category: '6. Critical Documents',
    name: 'Waterproof Pouch with Essential Documents',
    detail: 'Aadhaar cards, voter ID, bank passbook copies, property deeds, health insurance papers, ration card.'
  },
  {
    id: 'kit-sanitation',
    category: '7. Sanitation & Personal Hygiene',
    name: 'Sanitary Supplies, Disinfectant & Soap',
    detail: 'Chlorine water purification tablets, hand sanitizer, sanitary napkins, biohazard waste disposal bags.'
  },
  {
    id: 'kit-safety',
    category: '8. Signaling & Protective Wear',
    name: 'Emergency Whistle & Heavy-Duty Footwear',
    detail: 'Whistle to signal rescue personnel without exhausting voice; thick rubber boots and work gloves.'
  }
];

interface FutureRiskActionPanelProps {
  regionName?: string;
  hazardName?: string;
  leadTime?: string;
}

export const FutureRiskActionPanel: React.FC<FutureRiskActionPanelProps> = ({
  regionName = 'Your Area',
  hazardName = 'Disaster Hazard',
  leadTime = '6–24 Hours'
}) => {
  const [activeStage, setActiveStage] = useState<'now' | 'before' | 'during' | 'after' | 'kit'>('now');
  const [checkedKitItems, setCheckedKitItems] = useState<Record<string, boolean>>({});

  const toggleKitItem = (id: string) => {
    setCheckedKitItems((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const completedCount = Object.values(checkedKitItems).filter(Boolean).length;
  const totalCount = FAMILY_KIT_8_CATEGORIES.length;

  return (
    <section id="action-panel" className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto scroll-mt-24">
      <div className="rounded-3xl border border-paper-300 bg-white dark:bg-slate-900 p-6 sm:p-8 shadow-xl space-y-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-paper-200 dark:border-slate-800">
          <div className="space-y-1">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-300 text-xs font-mono font-bold uppercase tracking-wider">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>CITIZEN ACTION PROTOCOLS // LIFE SAFETY</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-charcoal-950 dark:text-white tracking-tight">
              What Should I Do?
            </h2>
            <p className="text-xs sm:text-sm text-charcoal-600 dark:text-slate-400 max-w-2xl">
              Lifecycle action guidelines aligned with NDMA standard operating procedures.
              Clear demarcation between immediate preparation and statutory evacuation directives.
            </p>
          </div>

          {/* Direct Helplines */}
          <div className="flex flex-wrap items-center gap-2 self-start md:self-auto">
            <a
              href="tel:112"
              className="px-3 py-1.5 rounded-xl bg-rose-600 text-white font-mono text-xs font-bold hover:bg-rose-700 transition-colors flex items-center gap-1.5 shadow-xs"
            >
              <PhoneCall className="w-3.5 h-3.5" />
              <span>112 (National Emergency)</span>
            </a>
            <a
              href="tel:1078"
              className="px-3 py-1.5 rounded-xl bg-paper-100 dark:bg-slate-800 text-charcoal-800 dark:text-slate-200 font-mono text-xs font-bold border border-paper-300 dark:border-slate-700 hover:bg-paper-200 transition-colors flex items-center gap-1.5"
            >
              <span>1078 (NDMA)</span>
            </a>
          </div>
        </div>

        {/* Stage Selector Tabs */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1">
          {[
            { id: 'now', label: '1. DO THIS RIGHT NOW', sub: 'Immediate (0–2h)' },
            { id: 'before', label: '2. PREPARE BEFORE', sub: 'Lead Window (6–24h)' },
            { id: 'during', label: '3. DURING EVENT', sub: 'Life Safety Shield' },
            { id: 'after', label: '4. AFTER EVENT', sub: 'Safe Recovery' },
            { id: 'kit', label: '5. 72H FAMILY KIT', sub: `${completedCount}/${totalCount} Packed` }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveStage(tab.id as any)}
              className={`px-4 py-2 rounded-2xl text-xs font-mono font-bold transition-all shrink-0 text-left border ${
                activeStage === tab.id
                  ? 'bg-charcoal-900 text-paper-50 dark:bg-white dark:text-charcoal-950 border-charcoal-900 dark:border-white shadow-sm'
                  : 'bg-paper-50 dark:bg-slate-800 text-charcoal-700 dark:text-slate-300 border-paper-200 dark:border-slate-700 hover:bg-paper-100'
              }`}
            >
              <div>{tab.label}</div>
              <div className="text-[10px] opacity-70 font-normal">{tab.sub}</div>
            </button>
          ))}
        </div>

        {/* STAGE 1: DO THIS RIGHT NOW */}
        {activeStage === 'now' && (
          <div className="space-y-4">
            <div className="p-4 rounded-2xl bg-rose-50/70 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900 text-rose-950 dark:text-rose-200 flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
              <div className="text-xs space-y-1">
                <span className="font-mono font-bold uppercase tracking-wider block">
                  PRIORITY LIFE-SAFETY ACTION CHECKLIST // LEAD TIME: {leadTime}
                </span>
                <p>
                  Perform these 4 immediate actions before weather deteriorates. Do not wait until floodwaters rise or winds become dangerous.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div className="p-4 rounded-2xl bg-paper-50 dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-1">
                <div className="font-mono text-xs font-bold text-charcoal-900 dark:text-white flex items-center gap-2">
                  <span className="w-5 h-5 rounded-full bg-rose-600 text-white flex items-center justify-center text-[10px]">1</span>
                  <span>Charge Communications & Fill Water Containers</span>
                </div>
                <p className="text-xs text-charcoal-600 dark:text-slate-400 pl-7">
                  Fully charge all mobile phones, power banks, and torches. Fill clean buckets and bottles with at least 15 litres of drinking water per person.
                </p>
              </div>

              <div className="p-4 rounded-2xl bg-paper-50 dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-1">
                <div className="font-mono text-xs font-bold text-charcoal-900 dark:text-white flex items-center gap-2">
                  <span className="w-5 h-5 rounded-full bg-rose-600 text-white flex items-center justify-center text-[10px]">2</span>
                  <span>Assemble Identity Documents & Prescription Medicines</span>
                </div>
                <p className="text-xs text-charcoal-600 dark:text-slate-400 pl-7">
                  Place Aadhaar cards, ration card, property deeds, and essential prescription tablets (insulin, BP) in a double-sealed waterproof plastic pouch.
                </p>
              </div>

              <div className="p-4 rounded-2xl bg-paper-50 dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-1">
                <div className="font-mono text-xs font-bold text-charcoal-900 dark:text-white flex items-center gap-2">
                  <span className="w-5 h-5 rounded-full bg-rose-600 text-white flex items-center justify-center text-[10px]">3</span>
                  <span>Locate Official Evacuation Shelter & Safe Route</span>
                </div>
                <p className="text-xs text-charcoal-600 dark:text-slate-400 pl-7">
                  Identify your nearest government school, cyclone shelter, or community hall on higher ground. Verify walking route avoids low-lying underpasses.
                </p>
              </div>

              <div className="p-4 rounded-2xl bg-paper-50 dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-1">
                <div className="font-mono text-xs font-bold text-charcoal-900 dark:text-white flex items-center gap-2">
                  <span className="w-5 h-5 rounded-full bg-rose-600 text-white flex items-center justify-center text-[10px]">4</span>
                  <span>Establish Family Emergency Meeting Protocol</span>
                </div>
                <p className="text-xs text-charcoal-600 dark:text-slate-400 pl-7">
                  Designate an out-of-district relative as the primary phone contact in case local mobile cellular networks become congested or non-operational.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* STAGE 2: PREPARE BEFORE */}
        {activeStage === 'before' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-5 rounded-2xl bg-paper-50 dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-2">
              <h4 className="font-mono text-xs font-bold uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                Residential & Structural Precautions
              </h4>
              <ul className="list-disc pl-4 text-xs text-charcoal-700 dark:text-slate-300 space-y-1.5 font-mono text-[11px]">
                <li>Clear roof gutters, terrace drainage spouts, and outdoor drainage channels to prevent waterlogging.</li>
                <li>Elevate valuable appliances, refrigerators, and gas cylinders onto raised masonry plinths or upper floors.</li>
                <li>Inspect overhead water storage tanks; anchor loose solar panels, tin sheets, and TV antennas securely.</li>
                <li>Turn off main gas pipeline regulator or LPG cylinder valves before leaving your dwelling.</li>
              </ul>
            </div>

            <div className="p-5 rounded-2xl bg-paper-50 dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-2">
              <h4 className="font-mono text-xs font-bold uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                Community & Vulnerable Person Support
              </h4>
              <ul className="list-disc pl-4 text-xs text-charcoal-700 dark:text-slate-300 space-y-1.5 font-mono text-[11px]">
                <li>Check on elderly neighbours, pregnant women, and persons with disabilities living alone in your lane.</li>
                <li>Untie domestic cattle and pets so they can reach higher ground in case of sudden water inundation.</li>
                <li>Verify local village panchayat or ward councillor helpline numbers are saved in your phone.</li>
                <li>Tune into All India Radio (AIR) station for hourly official district magistrate announcements.</li>
              </ul>
            </div>
          </div>
        )}

        {/* STAGE 3: DURING EVENT */}
        {activeStage === 'during' && (
          <div className="space-y-4">
            <div className="p-5 rounded-2xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800 space-y-3">
              <h4 className="font-mono text-xs font-bold uppercase tracking-wider text-amber-800 dark:text-amber-300">
                STRICT LIFE-SAFETY RULES DURING ACTIVE IMPACT
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs text-charcoal-800 dark:text-slate-200">
                <div className="p-3 rounded-xl bg-white dark:bg-slate-900 border border-amber-200 dark:border-amber-900">
                  <strong>DO NOT DRIVE THROUGH WATER:</strong> Just 15 cm of moving water can stall a car, and 30 cm can float most passenger vehicles.
                </div>
                <div className="p-3 rounded-xl bg-white dark:bg-slate-900 border border-amber-200 dark:border-amber-900">
                  <strong>AVOID DOWNED POWER WIRES:</strong> Assume all submerged wires are energized. Maintain a minimum 10-meter clearance distance.
                </div>
                <div className="p-3 rounded-xl bg-white dark:bg-slate-900 border border-amber-200 dark:border-amber-900">
                  <strong>HEED EVACUATION ORDERS:</strong> If local police or NDRF personnel order evacuation, move immediately without hesitation.
                </div>
              </div>
            </div>
          </div>
        )}

        {/* STAGE 4: AFTER EVENT */}
        {activeStage === 'after' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-5 rounded-2xl bg-paper-50 dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-2">
              <h4 className="font-mono text-xs font-bold uppercase tracking-wider text-emerald-700 dark:text-emerald-400">
                Safe Return & Sanitation
              </h4>
              <ul className="list-disc pl-4 text-xs text-charcoal-700 dark:text-slate-300 space-y-1.5 font-mono text-[11px]">
                <li>Do not enter flooded homes until local authorities confirm structural soundness.</li>
                <li>Boil all municipal or well water vigorously for at least 1 minute before drinking to prevent cholera and enteric infections.</li>
                <li>Watch for venomous snakes, scorpions, and rodents taking refuge in elevated dry indoor corners.</li>
                <li>Photograph structural damage and submerged assets for government disaster compensation claims (SDRF/NDRF).</li>
              </ul>
            </div>

            <div className="p-5 rounded-2xl bg-paper-50 dark:bg-slate-800 border border-paper-200 dark:border-slate-700 space-y-2">
              <h4 className="font-mono text-xs font-bold uppercase tracking-wider text-emerald-700 dark:text-emerald-400">
                Electrical & Gas Re-entry Check
              </h4>
              <ul className="list-disc pl-4 text-xs text-charcoal-700 dark:text-slate-300 space-y-1.5 font-mono text-[11px]">
                <li>Do NOT touch electrical switches, meters, or submerged circuit breakers with wet hands or bare feet.</li>
                <li>Have an authorized electrician inspect wiring before turning on the main circuit breaker.</li>
                <li>If you smell LPG or gas odor, open doors immediately, leave the house, and call 1906 (Gas Leak Emergency).</li>
                <li>Help municipal sanitation workers clear standing debris and stagnant water to prevent dengue and malaria outbreaks.</li>
              </ul>
            </div>
          </div>
        )}

        {/* STAGE 5: 72-HOUR FAMILY DISASTER KIT */}
        {activeStage === 'kit' && (
          <div className="space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-4 rounded-2xl bg-indigo-50 dark:bg-indigo-950/30 border border-indigo-200 dark:border-indigo-800">
              <div>
                <h4 className="font-mono text-xs font-bold uppercase tracking-wider text-indigo-900 dark:text-indigo-200">
                  72-HOUR FAMILY DISASTER SUPPLY KIT // 72-Hour Family Disaster Emergency Kit
                </h4>
                <p className="text-xs text-charcoal-600 dark:text-slate-400 mt-0.5">
                  Pack this 72-Hour Family Disaster Emergency Kit in a portable waterproof duffel bag or backpack kept near your main exit door.
                </p>
              </div>

              <div className="text-xs font-mono font-bold px-3 py-1.5 rounded-xl bg-white dark:bg-slate-800 border border-indigo-200 dark:border-indigo-700 text-indigo-700 dark:text-indigo-300 shrink-0">
                Progress: {completedCount} / {totalCount} Packed ({Math.round((completedCount / totalCount) * 100)}%)
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {FAMILY_KIT_8_CATEGORIES.map((item) => {
                const isChecked = Boolean(checkedKitItems[item.id]);
                return (
                  <div
                    key={item.id}
                    onClick={() => toggleKitItem(item.id)}
                    className={`p-4 rounded-2xl border transition-all cursor-pointer flex items-start gap-3 select-none ${
                      isChecked
                        ? 'bg-emerald-50/60 dark:bg-emerald-950/20 border-emerald-300 dark:border-emerald-800'
                        : 'bg-white dark:bg-slate-800 border-paper-200 dark:border-slate-700 hover:border-paper-300'
                    }`}
                  >
                    <button
                      type="button"
                      className="mt-0.5 text-charcoal-600 dark:text-slate-300 hover:text-emerald-600 shrink-0"
                      aria-label={`Toggle ${item.name}`}
                    >
                      {isChecked ? (
                        <CheckSquare className="w-5 h-5 text-emerald-600" />
                      ) : (
                        <Square className="w-5 h-5 text-charcoal-400" />
                      )}
                    </button>

                    <div className="space-y-0.5">
                      <span className="text-[10px] font-mono font-bold uppercase text-charcoal-500 dark:text-slate-400 block">
                        {item.category}
                      </span>
                      <div className={`text-xs font-bold ${isChecked ? 'text-emerald-900 dark:text-emerald-200 line-through opacity-80' : 'text-charcoal-900 dark:text-white'}`}>
                        {item.name}
                      </div>
                      <p className="text-[11px] text-charcoal-600 dark:text-slate-400 leading-relaxed font-sans">
                        {item.detail}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </section>
  );
};
