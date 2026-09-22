import React, { useState } from 'react';
import { 
  ShieldCheck, 
  Clock, 
  CheckSquare, 
  Square, 
  AlertTriangle, 
  PhoneCall, 
  HeartHandshake, 
  Package, 
  Radio, 
  FileText, 
  Zap, 
  Droplet, 
  Flame, 
  ExternalLink,
  BookOpen
} from 'lucide-react';
import { CompleteSafetyGuideModal } from '../safety/CompleteSafetyGuideModal';

interface ChecklistItem {
  id: string;
  category: 'water_food' | 'medical' | 'tools' | 'docs' | 'safety';
  label: string;
  detail: string;
}

const DEFAULT_KIT_ITEMS: ChecklistItem[] = [
  {
    id: 'kit-1',
    category: 'water_food',
    label: 'Drinking Water (3-Day Supply)',
    detail: 'Minimum 3–4 litres per person per day for drinking and basic sanitation.',
  },
  {
    id: 'kit-2',
    category: 'water_food',
    label: 'Non-Perishable Food Ration',
    detail: 'Dry rations, ready-to-eat grains, biscuits, nuts, energy bars, manual can opener.',
  },
  {
    id: 'kit-3',
    category: 'medical',
    label: 'First Aid Kit & 7-Day Prescription Meds',
    detail: 'Antiseptic, bandages, ORS sachets, chronic medications (insulin, BP, asthma).',
  },
  {
    id: 'kit-4',
    category: 'tools',
    label: 'Battery / Hand-Crank Radio & Flashlight',
    detail: 'All-band radio for official All India Radio / IMD bulletins; spare alkaline batteries.',
  },
  {
    id: 'kit-5',
    category: 'tools',
    label: 'Charged Power Bank & Heavy-Duty Cables',
    detail: 'Store in airtight waterproof zip bag; keep emergency contacts written on paper.',
  },
  {
    id: 'kit-6',
    category: 'docs',
    label: 'Waterproof Pouch with Essential Documents',
    detail: 'Aadhaar cards, ration card, insurance policies, property deeds, hospital records.',
  },
  {
    id: 'kit-7',
    category: 'tools',
    label: 'Whistle & High-Visibility Marker',
    detail: 'Signaling tool to alert search and rescue personnel without exhausting your voice.',
  },
  {
    id: 'kit-8',
    category: 'safety',
    label: 'Emergency Cash in Small Denominations',
    detail: '₹500 / ₹100 / ₹50 notes. ATMs, POS machines, and UPI fail during grid blackout.',
  },
];

type ActionTab = 'now' | 'before' | 'during' | 'after' | 'checklist';

export const CitizenActionSection: React.FC = () => {
  const [activeTab, setActiveTab] = useState<ActionTab>('now');
  const [checkedItems, setCheckedItems] = useState<Record<string, boolean>>({});
  const [showCompleteGuide, setShowCompleteGuide] = useState<boolean>(false);

  const toggleCheck = (id: string) => {
    setCheckedItems((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const completedCount = Object.values(checkedItems).filter(Boolean).length;
  const totalCount = DEFAULT_KIT_ITEMS.length;

  return (
    <section id="citizen-actions" className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6 mb-10">
        <div className="max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-mono uppercase tracking-wider font-semibold mb-3">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>CITIZEN ACTION PROTOCOLS // LIFE SAFETY</span>
          </div>
          <h2 className="text-3xl sm:text-5xl font-bold tracking-tight text-charcoal-950">
            What Should I Do?
          </h2>
          <p className="text-base sm:text-lg text-charcoal-600 mt-3 leading-relaxed">
            Clear, authoritative actions for every stage of disaster response. Preparedness saves lives before disaster strikes; following verified protocols protects your family during and after.
          </p>
        </div>

        {/* Extended Citizen Safety Guide CTA Button */}
        <button
          onClick={() => setShowCompleteGuide(true)}
          className="min-h-[48px] px-5 py-3 rounded-2xl bg-charcoal-950 hover:bg-charcoal-850 text-white font-mono text-xs sm:text-sm font-bold flex items-center justify-center gap-2.5 transition-all shadow-subtle shrink-0 border border-charcoal-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-emerald-600 self-start lg:self-end"
          aria-label="Explore Complete Citizen Disaster Safety Guide"
        >
          <BookOpen className="w-4.5 h-4.5 text-emerald-400" />
          <span>EXPLORE COMPLETE SAFETY GUIDE</span>
        </button>
      </div>

      {/* Critical Legal & Operational Distinction Callout */}
      <div className="mb-8 p-4 sm:p-5 rounded-2xl bg-amber-50/90 border border-amber-200/90 text-amber-950 flex items-start gap-3.5">
        <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
        <div className="text-xs sm:text-sm space-y-1">
          <div className="font-bold uppercase tracking-wider text-[11px] text-amber-800">
            Official Guidance Separation // Preparation vs Evacuation
          </div>
          <p className="text-amber-900 leading-relaxed">
            <strong>Preparation actions</strong> can and should be taken independently at any time. 
            <strong> Mandatory evacuation directives</strong> are ordered exclusively by civil authorities (District Magistrate / SDMA / NDRF). 
            Never delay evacuation if an official order is issued for your area.
          </p>
        </div>
      </div>

      {/* Main Tabs Navigation */}
      <div className="flex flex-wrap items-center gap-2 mb-8 border-b border-paper-300 pb-4">
        <button
          onClick={() => setActiveTab('now')}
          className={`min-h-[44px] px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all flex items-center gap-2 ${
            activeTab === 'now'
              ? 'bg-rose-600 text-white shadow-subtle font-bold'
              : 'bg-white text-charcoal-700 border border-paper-300 hover:bg-paper-100'
          }`}
        >
          <Clock className="w-4 h-4" />
          <span>Do Right Now</span>
        </button>

        <button
          onClick={() => setActiveTab('before')}
          className={`min-h-[44px] px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all flex items-center gap-2 ${
            activeTab === 'before'
              ? 'bg-charcoal-900 text-white shadow-subtle font-bold'
              : 'bg-white text-charcoal-700 border border-paper-300 hover:bg-paper-100'
          }`}
        >
          <ShieldCheck className="w-4 h-4" />
          <span>Prepare Before</span>
        </button>

        <button
          onClick={() => setActiveTab('during')}
          className={`min-h-[44px] px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all flex items-center gap-2 ${
            activeTab === 'during'
              ? 'bg-amber-600 text-white shadow-subtle font-bold'
              : 'bg-white text-charcoal-700 border border-paper-300 hover:bg-paper-100'
          }`}
        >
          <Flame className="w-4 h-4" />
          <span>During Disaster</span>
        </button>

        <button
          onClick={() => setActiveTab('after')}
          className={`min-h-[44px] px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all flex items-center gap-2 ${
            activeTab === 'after'
              ? 'bg-teal-700 text-white shadow-subtle font-bold'
              : 'bg-white text-charcoal-700 border border-paper-300 hover:bg-paper-100'
          }`}
        >
          <HeartHandshake className="w-4 h-4" />
          <span>After & Recovery</span>
        </button>

        <button
          onClick={() => setActiveTab('checklist')}
          className={`min-h-[44px] px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all flex items-center gap-2 ${
            activeTab === 'checklist'
              ? 'bg-blue-600 text-white shadow-subtle font-bold'
              : 'bg-white text-charcoal-700 border border-paper-300 hover:bg-paper-100'
          }`}
        >
          <Package className="w-4 h-4" />
          <span>72-Hour Family Kit ({completedCount}/{totalCount})</span>
        </button>
      </div>

      {/* Tab Panel Content */}
      <div className="rounded-3xl bg-white border border-paper-300 shadow-floating p-6 sm:p-10">
        {/* TAB: DO RIGHT NOW */}
        {activeTab === 'now' && (
          <div className="space-y-6">
            <div className="border-b border-paper-200 pb-4">
              <span className="font-mono text-xs uppercase tracking-wider text-rose-600 font-bold block mb-1">
                Immediate Action Phase // Next 1 to 2 Hours
              </span>
              <h3 className="text-2xl font-bold text-charcoal-950">
                Five Steps to Take Right Now
              </h3>
              <p className="text-sm text-charcoal-600 mt-1">
                If adverse weather or flood warnings are active in your region, do not wait. Perform these five basic actions immediately.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
              <div className="p-5 rounded-2xl bg-rose-50/50 border border-rose-200 flex items-start gap-4">
                <div className="w-8 h-8 rounded-full bg-rose-600 text-white flex items-center justify-center font-mono font-bold text-sm shrink-0">
                  1
                </div>
                <div>
                  <h4 className="font-bold text-charcoal-900 text-base mb-1">Charge Devices & Power Banks</h4>
                  <p className="text-xs sm:text-sm text-charcoal-700 leading-relaxed">
                    Charge mobile phones, backup batteries, and flashlights to 100%. Switch phones to battery-saver mode. Download offline offline maps if cellular service is vulnerable.
                  </p>
                </div>
              </div>

              <div className="p-5 rounded-2xl bg-paper-50 border border-paper-200 flex items-start gap-4">
                <div className="w-8 h-8 rounded-full bg-charcoal-900 text-white flex items-center justify-center font-mono font-bold text-sm shrink-0">
                  2
                </div>
                <div>
                  <h4 className="font-bold text-charcoal-900 text-base mb-1">Store Clean Drinking Water</h4>
                  <p className="text-xs sm:text-sm text-charcoal-700 leading-relaxed">
                    Fill clean containers and bottles with potable water. In floods or storms, municipal water supply lines may become contaminated or lose pumping pressure.
                  </p>
                </div>
              </div>

              <div className="p-5 rounded-2xl bg-paper-50 border border-paper-200 flex items-start gap-4">
                <div className="w-8 h-8 rounded-full bg-charcoal-900 text-white flex items-center justify-center font-mono font-bold text-sm shrink-0">
                  3
                </div>
                <div>
                  <h4 className="font-bold text-charcoal-900 text-base mb-1">Gather Critical Documents & Meds</h4>
                  <p className="text-xs sm:text-sm text-charcoal-700 leading-relaxed">
                    Place ID cards (Aadhaar), property/insurance records, cash, and ongoing prescription medicines into a sealed waterproof plastic bag near your exit.
                  </p>
                </div>
              </div>

              <div className="p-5 rounded-2xl bg-paper-50 border border-paper-200 flex items-start gap-4">
                <div className="w-8 h-8 rounded-full bg-charcoal-900 text-white flex items-center justify-center font-mono font-bold text-sm shrink-0">
                  4
                </div>
                <div>
                  <h4 className="font-bold text-charcoal-900 text-base mb-1">Agree on Family Rendezvous Point</h4>
                  <p className="text-xs sm:text-sm text-charcoal-700 leading-relaxed">
                    Ensure all family members know an agreed meeting location outside your neighborhood if separated, and memorize one out-of-district relative's phone number.
                  </p>
                </div>
              </div>

              <div className="p-5 rounded-2xl bg-paper-50 border border-paper-200 flex items-start gap-4 md:col-span-2">
                <div className="w-8 h-8 rounded-full bg-charcoal-900 text-white flex items-center justify-center font-mono font-bold text-sm shrink-0">
                  5
                </div>
                <div>
                  <h4 className="font-bold text-charcoal-900 text-base mb-1">Tune to Official Government Broadcasts Only</h4>
                  <p className="text-xs sm:text-sm text-charcoal-700 leading-relaxed">
                    Rely on All India Radio, Doordarshan, IMD Mausam, and official District Disaster Management Authority (DDMA) announcements. Do not forward unverified viral WhatsApp messages.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB: PREPARE BEFORE */}
        {activeTab === 'before' && (
          <div className="space-y-6">
            <div className="border-b border-paper-200 pb-4">
              <span className="font-mono text-xs uppercase tracking-wider text-charcoal-500 font-bold block mb-1">
                Advance Mitigation // Days to Weeks Before
              </span>
              <h3 className="text-2xl font-bold text-charcoal-950">
                Structural & Community Preparedness
              </h3>
              <p className="text-sm text-charcoal-600 mt-1">
                Proactive measures that dramatically reduce property damage and protect family members before severe weather arrives.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
              <div className="p-5 rounded-2xl bg-paper-50 border border-paper-200">
                <div className="p-2 w-fit rounded-xl bg-charcoal-900 text-white mb-3">
                  <Droplet className="w-5 h-5" />
                </div>
                <h4 className="font-bold text-charcoal-900 text-base mb-2">Drainage & Roof Inspection</h4>
                <ul className="text-xs sm:text-sm text-charcoal-700 space-y-2 list-disc pl-4">
                  <li>Clear rooftop rainwater outlets and storm gutters of debris.</li>
                  <li>Secure loose asbestos, tin, or plastic roof sheets with ties.</li>
                  <li>Trim weak or overhanging tree branches near power lines.</li>
                </ul>
              </div>

              <div className="p-5 rounded-2xl bg-paper-50 border border-paper-200">
                <div className="p-2 w-fit rounded-xl bg-charcoal-900 text-white mb-3">
                  <Zap className="w-5 h-5" />
                </div>
                <h4 className="font-bold text-charcoal-900 text-base mb-2">Electrical & Gas Safeties</h4>
                <ul className="text-xs sm:text-sm text-charcoal-700 space-y-2 list-disc pl-4">
                  <li>Know the exact location of your main electrical circuit breaker.</li>
                  <li>Inspect LPG regulator and ensure cylinder shut-off valves work smoothly.</li>
                  <li>Elevate major appliances (refrigerators, inverters) on wooden pedestals.</li>
                </ul>
              </div>

              <div className="p-5 rounded-2xl bg-paper-50 border border-paper-200">
                <div className="p-2 w-fit rounded-xl bg-charcoal-900 text-white mb-3">
                  <FileText className="w-5 h-5" />
                </div>
                <h4 className="font-bold text-charcoal-900 text-base mb-2">Vulnerable Care & Community</h4>
                <ul className="text-xs sm:text-sm text-charcoal-700 space-y-2 list-disc pl-4">
                  <li>Pre-arrange care for elderly relatives, infants, and people with disabilities.</li>
                  <li>Identify the nearest designated cyclone shelter, school, or community hall.</li>
                  <li>Save local ward councillor and panchayat representative contact numbers.</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* TAB: DURING DISASTER */}
        {activeTab === 'during' && (
          <div className="space-y-6">
            <div className="border-b border-paper-200 pb-4">
              <span className="font-mono text-xs uppercase tracking-wider text-amber-600 font-bold block mb-1">
                Active Hazard Phase // Survival & Containment
              </span>
              <h3 className="text-2xl font-bold text-charcoal-950">
                Non-Negotiable Life Safety Rules
              </h3>
              <p className="text-sm text-charcoal-600 mt-1">
                Actions to protect yourself when cyclonic winds, sudden flash floods, or earthquake tremors strike.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
              <div className="p-5 rounded-2xl bg-amber-50/70 border border-amber-200">
                <div className="font-bold text-amber-950 text-base mb-2 flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-amber-600" />
                  <span>Flash Floods & Waterlogging</span>
                </div>
                <ul className="text-xs sm:text-sm text-charcoal-800 space-y-2 list-disc pl-4 leading-relaxed">
                  <li><strong>Never walk or drive through moving floodwaters.</strong> Just 15 cm of moving water can knock an adult down; 30 cm can sweep away a car.</li>
                  <li>Disconnect main electrical breaker if water enters your home.</li>
                  <li>Move immediately to an upper floor or reinforced roof. Carry only your emergency pouch.</li>
                </ul>
              </div>

              <div className="p-5 rounded-2xl bg-amber-50/70 border border-amber-200">
                <div className="font-bold text-amber-950 text-base mb-2 flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-amber-600" />
                  <span>Cyclonic Gale Winds</span>
                </div>
                <ul className="text-xs sm:text-sm text-charcoal-800 space-y-2 list-disc pl-4 leading-relaxed">
                  <li>Stay inside the strongest central room away from windows and glass doors.</li>
                  <li>Beware of the "Eye of the Cyclone": sudden calm is temporary, destructive winds will resume from opposite direction.</li>
                  <li>Do not venture outside until authorities declare "All Clear".</li>
                </ul>
              </div>

              <div className="p-5 rounded-2xl bg-amber-50/70 border border-amber-200">
                <div className="font-bold text-amber-950 text-base mb-2 flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-amber-600" />
                  <span>Earthquake Tremors</span>
                </div>
                <ul className="text-xs sm:text-sm text-charcoal-800 space-y-2 list-disc pl-4 leading-relaxed">
                  <li><strong>DROP, COVER, AND HOLD ON.</strong> Take shelter under a sturdy table or desk.</li>
                  <li>Do not rush to elevators or staircases during shaking.</li>
                  <li>If outdoors, move into an open area away from buildings, utility wires, and flyovers.</li>
                </ul>
              </div>

              <div className="p-5 rounded-2xl bg-amber-50/70 border border-amber-200">
                <div className="font-bold text-amber-950 text-base mb-2 flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-amber-600" />
                  <span>Extreme Heatwave</span>
                </div>
                <ul className="text-xs sm:text-sm text-charcoal-800 space-y-2 list-disc pl-4 leading-relaxed">
                  <li>Avoid outdoor exposure between 11:00 AM and 4:00 PM.</li>
                  <li>Drink ORS, lemon water, buttermilk, or plain water even before feeling thirsty.</li>
                  <li>If someone exhibits high body temperature without sweating, apply cool wet cloth and seek immediate medical help.</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* TAB: AFTER & RECOVERY */}
        {activeTab === 'after' && (
          <div className="space-y-6">
            <div className="border-b border-paper-200 pb-4">
              <span className="font-mono text-xs uppercase tracking-wider text-teal-700 font-bold block mb-1">
                Post-Event Recovery // Safe Re-Entry & Health
              </span>
              <h3 className="text-2xl font-bold text-charcoal-950">
                Safe Return & Infection Prevention
              </h3>
              <p className="text-sm text-charcoal-600 mt-1">
                More casualties often occur after a disaster than during the event due to electrocution, contaminated water, and structural collapse.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
              <div className="p-5 rounded-2xl bg-teal-50/50 border border-teal-200">
                <h4 className="font-bold text-charcoal-900 text-base mb-2">1. Structural & Electrical Re-Entry Check</h4>
                <ul className="text-xs sm:text-sm text-charcoal-700 space-y-2 list-disc pl-4">
                  <li>Inspect foundation, walls, and ceiling for cracks before stepping inside.</li>
                  <li>Do not turn on electrical switches until an electrician certifies wiring is dry.</li>
                  <li>Watch out for displaced wildlife, stray venomous snakes, and sharp metal debris.</li>
                </ul>
              </div>

              <div className="p-5 rounded-2xl bg-teal-50/50 border border-teal-200">
                <h4 className="font-bold text-charcoal-900 text-base mb-2">2. Water Sanitation & Food Hygiene</h4>
                <ul className="text-xs sm:text-sm text-charcoal-700 space-y-2 list-disc pl-4">
                  <li>Boil all tap or well water vigorously for at least 1 minute before consuming.</li>
                  <li>Discard any food item that touched floodwater or spoiled during blackout.</li>
                  <li>Use chlorine tablets as directed by municipal public health teams.</li>
                </ul>
              </div>

              <div className="p-5 rounded-2xl bg-teal-50/50 border border-teal-200">
                <h4 className="font-bold text-charcoal-900 text-base mb-2">3. Damage Documentation for Relief Claims</h4>
                <ul className="text-xs sm:text-sm text-charcoal-700 space-y-2 list-disc pl-4">
                  <li>Photograph and video document structural damages and damaged assets before cleaning.</li>
                  <li>Keep copies of police DDR (Daily Diary Report) if vehicles or livestock were lost.</li>
                  <li>Submit claims through the state disaster relief portal or district revenue office.</li>
                </ul>
              </div>

              <div className="p-5 rounded-2xl bg-teal-50/50 border border-teal-200">
                <h4 className="font-bold text-charcoal-900 text-base mb-2">4. Helping Vulnerable Neighbors</h4>
                <ul className="text-xs sm:text-sm text-charcoal-700 space-y-2 list-disc pl-4">
                  <li>Check on elderly, infants, and lone residents in your immediate neighborhood.</li>
                  <li>Report unaddressed hazards or stranded citizens to National Emergency (112).</li>
                  <li>Coordinate with authorized local relief distribution centres.</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* TAB: 72-HOUR FAMILY CHECKLIST */}
        {activeTab === 'checklist' && (
          <div className="space-y-6">
            <div className="border-b border-paper-200 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <span className="font-mono text-xs uppercase tracking-wider text-blue-600 font-bold block mb-1">
                  Interactive Survival Readiness
                </span>
                <h3 className="text-2xl font-bold text-charcoal-950">
                  72-Hour Family Disaster Kit
                </h3>
                <p className="text-sm text-charcoal-600 mt-1">
                  Keep these essentials assembled in an easy-to-carry backpack or duffel bag near your front door.
                </p>
              </div>

              <div className="p-3 bg-blue-50 border border-blue-200 rounded-2xl text-center sm:text-right shrink-0">
                <div className="text-xs font-mono uppercase text-blue-700 font-semibold">Progress</div>
                <div className="text-xl font-bold font-mono text-blue-950">
                  {completedCount} / {totalCount} <span className="text-xs font-normal text-charcoal-500">packed</span>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
              {DEFAULT_KIT_ITEMS.map((item) => {
                const isChecked = !!checkedItems[item.id];
                return (
                  <button
                    key={item.id}
                    onClick={() => toggleCheck(item.id)}
                    className={`min-h-[56px] text-left p-4 rounded-2xl border transition-all flex items-start gap-3.5 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 ${
                      isChecked
                        ? 'bg-blue-50/80 border-blue-300 text-blue-950'
                        : 'bg-paper-50/70 border-paper-200 text-charcoal-900 hover:bg-white'
                    }`}
                  >
                    <div className="mt-0.5 shrink-0 text-blue-600">
                      {isChecked ? (
                        <CheckSquare className="w-5 h-5 text-blue-700" />
                      ) : (
                        <Square className="w-5 h-5 text-charcoal-400" />
                      )}
                    </div>
                    <div>
                      <div className={`text-sm font-bold ${isChecked ? 'line-through text-blue-900' : 'text-charcoal-900'}`}>
                        {item.label}
                      </div>
                      <div className="text-xs text-charcoal-600 mt-0.5 leading-relaxed">
                        {item.detail}
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* Verified Government Emergency Help Bar */}
      <div className="mt-8 p-6 rounded-3xl bg-charcoal-950 text-paper-50 border border-charcoal-900 flex flex-col md:flex-row items-center justify-between gap-6">
        <div>
          <div className="font-mono text-xs uppercase tracking-wider text-charcoal-400 font-semibold mb-1">
            VERIFIED OFFICIAL EMERGENCY NUMBERS
          </div>
          <div className="text-lg font-bold">
            If You Are in Immediate Life Threat, Call Directly
          </div>
          <p className="text-xs text-charcoal-400 mt-1">
            Free of charge from any mobile carrier or landline in India, even with zero balance or locked SIM.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3 shrink-0">
          <a
            href="tel:112"
            className="min-h-[44px] px-4 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-mono font-bold text-sm flex items-center gap-2 transition-colors"
          >
            <PhoneCall className="w-4 h-4" />
            <span>112 (National Emergency)</span>
          </a>

          <a
            href="tel:1078"
            className="min-h-[44px] px-4 py-2.5 rounded-xl bg-charcoal-800 hover:bg-charcoal-700 text-white font-mono font-bold text-sm flex items-center gap-2 transition-colors border border-charcoal-700"
          >
            <PhoneCall className="w-4 h-4" />
            <span>1078 (NDMA Disaster)</span>
          </a>

          <a
            href="tel:1070"
            className="min-h-[44px] px-4 py-2.5 rounded-xl bg-charcoal-800 hover:bg-charcoal-700 text-white font-mono font-bold text-sm flex items-center gap-2 transition-colors border border-charcoal-700"
          >
            <PhoneCall className="w-4 h-4" />
            <span>1070 (State Relief)</span>
          </a>
        </div>
      </div>

      {/* Complete Citizen Disaster Safety Guide Modal */}
      <CompleteSafetyGuideModal
        isOpen={showCompleteGuide}
        onClose={() => setShowCompleteGuide(false)}
      />
    </section>
  );
};

