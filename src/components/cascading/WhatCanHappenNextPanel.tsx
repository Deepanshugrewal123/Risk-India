/**
 * RISK // INDIA — "What Can Happen Next?" Cascading Impact Panel
 * ===============================================================
 * Visualizes multi-stage disaster consequence progression:
 * Primary Trigger -> Secondary Physical Effects -> Downstream Systemic Impacts.
 * Provides observable warning signs and connects directly to citizen safety guidance.
 */

import React, { useState } from 'react';
import {
  GitBranch,
  ArrowRight,
  ShieldCheck,
  Compass,
  AlertTriangle,
  Layers,
  ChevronRight,
  BookOpen,
  Activity,
  Zap,
  Droplet,
  Flame,
  Wind
} from 'lucide-react';
import { NavigationPage } from '../common/Navbar';

export interface ConsequencePathway {
  hazardId: string;
  hazardName: string;
  icon: string;
  immediate: {
    title: string;
    description: string;
    items: string[];
  };
  secondary: {
    title: string;
    description: string;
    items: {
      name: string;
      explanation: string;
      watchFor: string;
    }[];
  };
  downstream: {
    title: string;
    description: string;
    items: {
      name: string;
      impact: string;
      defensiveAction: string;
    }[];
  };
  crossHazardNote: string;
}

export const CASCADING_PATHWAYS: Record<string, ConsequencePathway> = {
  FLOOD: {
    hazardId: 'FLOOD',
    hazardName: 'Flood / Heavy Inundation',
    icon: '🌊',
    immediate: {
      title: 'Immediate Onset (0–6 Hours)',
      description: 'Sudden surface runoff, river overbank spillage, and drainage network saturation.',
      items: [
        'Rapid water level rise submerging low-lying roads and bridge approaches.',
        'Stormwater culverts backing up into residential basements and ground floors.',
        'Surface transportation corridors severed at low-water crossings.'
      ]
    },
    secondary: {
      title: 'Possible Secondary Effects (6–24 Hours)',
      description: 'Physical and environmental disruptions developing as floodwaters linger.',
      items: [
        {
          name: 'Slope Instability & Hillside Landslides',
          explanation: 'Prolonged torrential rainfall saturates hillside soil, increasing pore-water pressure and weakening shear strength on vulnerable slopes.',
          watchFor: 'New ground cracks, tilted trees or telephone poles, and muddy hillside spring water.'
        },
        {
          name: 'Drinking Water Grid Contamination',
          explanation: 'Submerged municipal mains and open borewells suffer backflow from sewer lines and agricultural chemical runoff.',
          watchFor: 'Discolored tap water, foul earthy sewage odors, and sudden water turbidity.'
        },
        {
          name: 'Submerged Electrical Electrocution Hazards',
          explanation: 'Water enters ground-level transformer kiosks, street switchboards, and domestic distribution panels.',
          watchFor: 'Buzzing noises, sparking near utility poles, and surface ripples around electrical junction boxes.'
        },
        {
          name: 'Road Isolation & Culvert Scouring',
          explanation: 'Hydrodynamic water pressure scours road sub-bases beneath tarmac, creating invisible underwater collapse cavities.',
          watchFor: 'Washed-out road shoulders, tilting guardrails, and rapid turbulence over road dips.'
        }
      ]
    },
    downstream: {
      title: 'Possible Downstream Systemic Impacts (24–72+ Hours)',
      description: 'Critical infrastructure breakdowns and socio-economic consequences.',
      items: [
        {
          name: 'Enteric Waterborne Epidemics',
          impact: 'Spike in Cholera, Acute Gastroenteritis, and Leptospirosis from contact with contaminated water.',
          defensiveAction: 'Boil all drinking water for 60 seconds; take doxycycline prophylaxis under medical guidance.'
        },
        {
          name: 'Protracted Power Grid Blackouts',
          impact: 'Substations cannot be re-energized until underground transformers and conduits are pumped dry.',
          defensiveAction: 'Rely on battery transistor radio; preserve mobile battery with power-saving modes.'
        },
        {
          name: 'Healthcare & Hospital Supply Strain',
          impact: 'Flooded hospital ground floors compromise oxygen manifolds, ICUs, and vaccine cold chains.',
          defensiveAction: 'Keep 7 days of essential prescription medicines sealed in waterproof pouches.'
        },
        {
          name: 'Agricultural Inundation & Supply Disruption',
          impact: 'Submerged standing crops suffer root rot, causing vegetable shortages and market price spikes.',
          defensiveAction: 'Rely on stored non-perishable high-protein dry rations (puffed rice, pulses, jaggery).'
        }
      ]
    },
    crossHazardNote: 'In hilly and mountainous terrain (Himalayan states, Western Ghats), intense flooding directly triggers slope failures and debris flows.'
  },
  CYCLONE: {
    hazardId: 'CYCLONE',
    hazardName: 'Tropical Cyclone / Severe Storm',
    icon: '🌀',
    immediate: {
      title: 'Immediate Onset (Landfall: 0–6 Hours)',
      description: 'Destructive gale-force winds exceeding 120 km/h, torrential squalls, and coastal storm surge.',
      items: [
        'Aerodynamic uplift ripping unfastened corrugated tin sheets and solar panels.',
        'High-velocity projectile impacts from loose garden furniture and broken branches.',
        'Coastal seawater surge penetrating 3 to 10 km inland across low-lying estuaries.'
      ]
    },
    secondary: {
      title: 'Possible Secondary Effects (6–24 Hours)',
      description: 'Severe structural and environmental destruction in the wake of the eyewall.',
      items: [
        {
          name: 'Power & Telecommunication Blackout',
          explanation: 'High winds snap transmission towers, uproot electric poles, and tear down optical fiber cables.',
          watchFor: 'Sparks from damaged substations and sudden cellular network disconnection.'
        },
        {
          name: 'Inland River & Urban Flooding',
          explanation: 'Extensive spiral rainbands dump 200–300 mm of rain, triggering inland river crests well away from the coast.',
          watchFor: 'Rapid inundation of inland drainage channels hours after wind subsides.'
        },
        {
          name: 'Fallen Live High-Tension Cables',
          explanation: 'Fallen trees trap broken 11 kV/33 kV cables in wet foliage, creating lethal step-potential voltage zones.',
          watchFor: 'Buzzing sounds, smoking foliage, or severed black wires in puddles.'
        }
      ]
    },
    downstream: {
      title: 'Possible Downstream Systemic Impacts (24–72+ Hours)',
      description: 'Prolonged regional disruption to utilities, food, and public order.',
      items: [
        {
          name: 'Total Potable Water Distribution Breakdown',
          impact: 'Pumping stations lose grid power; storm surge saline water contaminates coastal freshwater aquifers.',
          defensiveAction: 'Disinfect water with chlorine tablets; access community water relief tankers.'
        },
        {
          name: 'Debris Gridlock Blocking Emergency Relief',
          impact: 'Thousands of uprooted banyan trees and metal debris block state highways, halting NDRF convoys.',
          defensiveAction: 'Stay off highways; clear neighborhood debris with community volunteers safely.'
        },
        {
          name: 'Saline Agricultural Soil Degradation',
          impact: 'Seawater inundation leaves salt deposits, destroying coastal paddy fields for multiple seasons.',
          defensiveAction: 'Flush soil with freshwater once monsoons resume; report crop damage to Tahsildar.'
        }
      ]
    },
    crossHazardNote: 'A coastal cyclone is a multi-hazard cascade: extreme wind triggers storm surge, which triggers inland river flooding, followed by grid failure.'
  },
  HEATWAVE: {
    hazardId: 'HEATWAVE',
    hazardName: 'Severe Heatwave / Thermal Stress',
    icon: '☀️',
    immediate: {
      title: 'Immediate Onset (Day 1–2)',
      description: 'Extreme ambient dry-bulb temperatures (>42°C) combined with high solar radiation flux.',
      items: [
        'Rapid body dehydration, electrolyte loss, and muscle heat cramps.',
        'Thermal expansion softening asphalt roads and elevating outdoor surface heat past 55°C.',
        'Peak urban air conditioner power demand surging past substation limits.'
      ]
    },
    secondary: {
      title: 'Possible Secondary Effects (Day 2–4)',
      description: 'Escalating physiological and infrastructural strain under sustained heat.',
      items: [
        {
          name: 'Power Grid Brownouts & Transformer Trips',
          explanation: 'Continuous thermal loading overheats distribution transformers, causing localized rolling blackouts.',
          watchFor: 'Dimming ceiling lights, frequent voltage drops, and buzzing electrical substations.'
        },
        {
          name: 'Water Distribution Shortages',
          explanation: 'Domestic water demand jumps 40% while reservoir evaporation accelerates and borewell water tables drop.',
          watchFor: 'Low municipal tap pressure and dry neighborhood water taps.'
        },
        {
          name: 'Urban Smog & Ozone Accumulation',
          explanation: 'Intense sunlight reacts with vehicular NOx and VOC emissions, forming high concentrations of ground-level ozone.',
          watchFor: 'Hazy yellowish horizon, eye stinging, and respiratory irritation.'
        }
      ]
    },
    downstream: {
      title: 'Possible Downstream Systemic Impacts (Day 4+)',
      description: 'Public health emergencies and regional economic slowdowns.',
      items: [
        {
          name: 'Hospital ICU & Emergency Ward Overload',
          impact: 'Wave of severe heat stroke, acute kidney injury, and cardiac arrests among seniors.',
          defensiveAction: 'Provide cooling first aid immediately; transport heat stroke victims to hospital.'
        },
        {
          name: 'Agricultural Desiccation & Forest Fires',
          impact: 'Bone-dry vegetation ignites easily from small sparks, triggering runaway scrub and forest fires.',
          defensiveAction: 'Do not light open fires or dispose of burning cigarette butts near dry brush.'
        },
        {
          name: 'Labor Productivity Loss & Economic Slowdown',
          impact: 'Outdoor daily wage laborers, rickshaw pullers, and delivery executives forced to halt daytime work.',
          defensiveAction: 'Shift outdoor labor strictly to 06:00–10:00 and post-17:00.'
        }
      ]
    },
    crossHazardNote: 'Severe heatwaves directly amplify subsequent drought risk, accelerate forest fire ignition, and heighten peak-hour electrical grid failure.'
  },
  SEVERE_WEATHER: {
    hazardId: 'SEVERE_WEATHER',
    hazardName: 'Severe Weather / Thunderstorms & Hail',
    icon: '⛈️',
    immediate: {
      title: 'Immediate Onset (0–2 Hours)',
      description: 'Violent convective downdrafts, rapid lightning discharges, and localized hail bombardment.',
      items: [
        'Cloud-to-ground lightning strikes hitting trees, structures, and open fields.',
        'Microburst wind gusts exceeding 90 km/h tearing unreinforced hoardings.',
        'Hailstones causing blunt trauma to pedestrians and damaging glass/crops.'
      ]
    },
    secondary: {
      title: 'Possible Secondary Effects (2–6 Hours)',
      description: 'Rapid localized hazards triggered by intense precipitation and lightning.',
      items: [
        {
          name: 'Flash Urban Street Inundation',
          explanation: 'Downpours depositing 60 mm in 45 minutes overwhelm storm culverts designed for 20 mm/hr capacity.',
          watchFor: 'Water gushing out of storm manholes and rapid ponding at road dips.'
        },
        {
          name: 'Structural Lightning Fires',
          explanation: 'Direct lightning strikes inject immense electrical thermal energy into attics, roof timber, and haystacks.',
          watchFor: 'Smell of burning wood or electrical insulation in attic crawlspaces.'
        },
        {
          name: 'Traffic Gridlock & Flying Debris Collisions',
          explanation: 'Fallen trees, hail slicks, and dislodged advertising hoardings block traffic lanes.',
          watchFor: 'Twisted metal sheets on road and broken glass scattered across intersections.'
        }
      ]
    },
    downstream: {
      title: 'Possible Downstream Systemic Impacts (6–24 Hours)',
      description: 'Regional disruption following localized severe storms.',
      items: [
        {
          name: 'Catastrophic Standing Crop Destruction',
          impact: 'Hailstorms shred standing wheat, mustard, and fruit orchards within minutes.',
          defensiveAction: 'Photograph field crop damage and register claim with PM Fasal Bima Yojana.'
        },
        {
          name: 'Substation Damage & Isolated Blackouts',
          impact: 'Lightning arrester burnouts trip local feeder lines, disabling residential colonies.',
          defensiveAction: 'Keep power banks charged; report damaged transformer kiosks to utility.'
        }
      ]
    },
    crossHazardNote: 'Severe convective thunderstorms are the primary trigger for sudden flash urban waterlogging and microburst structural blowouts.'
  },
  LANDSLIDE: {
    hazardId: 'LANDSLIDE',
    hazardName: 'Landslide / Slope Failure',
    icon: '⛰️',
    immediate: {
      title: 'Immediate Onset (0–1 Hour)',
      description: 'Sudden gravitational mass movement of rock, debris, and saturated soil downhill.',
      items: [
        'High-speed debris avalanche destroying buildings directly in its downslope path.',
        'Highways severed and buried beneath thousands of tonnes of crushed stone and mud.',
        'Telephone poles, electricity lines, and water distribution pipes ripped apart.'
      ]
    },
    secondary: {
      title: 'Possible Secondary Effects (1–12 Hours)',
      description: 'Critical secondary hazards emerging around the slide perimeter.',
      items: [
        {
          name: 'Landslide Dam Outburst Flood (LDOF)',
          explanation: 'Debris plunging into mountain river gorges creates a natural temporary dam; when it breaches under water pressure, a massive flash flood rushes downstream.',
          watchFor: 'Downstream river level suddenly dropping to a trickle during heavy rain.'
        },
        {
          name: 'Secondary Slope Failures & Scarp Collapses',
          explanation: 'The destabilized, fractured head scarp left behind loses supporting counterweight and collapses without warning.',
          watchFor: 'Pebbles and dust continually falling from the top scarp edge.'
        },
        {
          name: 'Highland Village Isolation',
          explanation: 'Both arterial approach roads blocked, stranding villages with limited food and medical access.',
          watchFor: 'All vehicle movement halted; communication lines down.'
        }
      ]
    },
    downstream: {
      title: 'Possible Downstream Systemic Impacts (12–72+ Hours)',
      description: 'Prolonged logistical and humanitarian isolation in mountain valleys.',
      items: [
        {
          name: 'Essential Fuel & Food Supply Cutoff',
          impact: 'Mountain hamlets face acute shortages of cooking gas (LPG), diesel, milk, and medical supplies.',
          defensiveAction: 'Ration local food grains; coordinate emergency airdrops with district magistrate.'
        },
        {
          name: 'Downstream Siltation & Hydroelectric Power Trip',
          impact: 'Millions of tonnes of fine silt choke hydroelectric turbine intakes, forcing complete dam shutdown.',
          defensiveAction: 'Prepare for regional electrical load shedding.'
        }
      ]
    },
    crossHazardNote: 'Landslides into mountain rivers directly cause catastrophic downstream flash floods (LDOFs), multiplying disaster impact across valley systems.'
  },
  EARTHQUAKE: {
    hazardId: 'EARTHQUAKE',
    hazardName: 'Earthquake / Ground Shaking',
    icon: '⚡',
    immediate: {
      title: 'Immediate Onset (0–2 Minutes)',
      description: 'Sudden seismic wave rupture causing violent horizontal and vertical ground accelerations.',
      items: [
        'Ground displacement and dynamic shaking of buildings, bridges, and flyovers.',
        'Non-structural hazards: falling ceiling fans, toppling wardrobes, and glass shards.',
        'Partial or total collapse of seismically vulnerable unreinforced masonry structures.'
      ]
    },
    secondary: {
      title: 'Possible Secondary Effects (2 Minutes–6 Hours)',
      description: 'Immediate secondary hazards that develop as direct aftermath of ground shaking.',
      items: [
        {
          name: 'Secondary Aftershock Tremors',
          explanation: 'Fault stress redistribution triggers hundreds of aftershocks, some registering magnitude 5.5+, bringing down already compromised structures.',
          watchFor: 'Secondary tremors and new cracks forming in masonry walls.'
        },
        {
          name: 'Gas Pipeline Ruptures & Urban Fires',
          explanation: 'Differential ground motion shears domestic gas connections and buried mains; tiny electrical sparks ignite raging block fires.',
          watchFor: 'Rotten egg / sulfur gas smell and smoke rising from building basements.'
        },
        {
          name: 'Soil Liquefaction in Saturated Alluvium',
          explanation: 'Seismic shaking increases pore-water pressure in loose, water-saturated sandy soil, causing ground to behave like liquid quicksand.',
          watchFor: 'Sand boils (water and silt erupting through ground cracks) and buildings sinking/tilting.'
        },
        {
          name: 'Mountain Rockfalls & Landslides',
          explanation: 'Seismic shaking dislodges jointed rock masses on steep slopes, blocking mountain passes and damming rivers.',
          watchFor: 'Dust clouds rising from hill slopes and boulders blocking roads.'
        }
      ]
    },
    downstream: {
      title: 'Possible Downstream Systemic Impacts (6–72+ Hours)',
      description: 'Widespread collapse of civic infrastructure and search-and-rescue mobilization.',
      items: [
        {
          name: 'Potable Water & Fire Hydrant Failure',
          impact: 'Sheared underground water pipes drain municipal reservoirs; fire brigades have zero water pressure to fight conflagrations.',
          defensiveAction: 'Use fire extinguishers or sand immediately on small fires before water fails.'
        },
        {
          name: 'Hospital Damage & Triage Bottleneck',
          impact: 'Hospitals overwhelmed with thousands of orthopedic and crush trauma patients while facilities suffer structural damage.',
          defensiveAction: 'Set up neighborhood first aid triage stations; reserve hospital beds for critical patients.'
        },
        {
          name: 'Communication Congestion & Transport Severance',
          impact: 'Millions attempting voice calls crash cellular networks; flyover damage isolates urban sectors.',
          defensiveAction: 'Use SMS instead of voice calls; travel on foot or bicycle to avoid bridge bottlenecks.'
        }
      ]
    },
    crossHazardNote: 'Earthquakes trigger secondary urban fires, soil liquefaction, mountain landslides, and tsunamis in coastal subduction zones.'
  }
};

interface WhatCanHappenNextPanelProps {
  initialHazard?: string;
  onNavigate?: (page: NavigationPage) => void;
  className?: string;
}

export const WhatCanHappenNextPanel: React.FC<WhatCanHappenNextPanelProps> = ({
  initialHazard = 'FLOOD',
  onNavigate,
  className = ''
}) => {
  const [activeHazard, setActiveHazard] = useState<string>(initialHazard);
  const [expandedSecondary, setExpandedSecondary] = useState<number | null>(0);

  const pathway = CASCADING_PATHWAYS[activeHazard] || CASCADING_PATHWAYS.FLOOD;

  return (
    <section
      id="what-can-happen-next"
      className={`p-6 sm:p-8 rounded-3xl bg-white dark:bg-slate-900 border border-paper-300 dark:border-slate-800 shadow-xl space-y-6 scroll-mt-24 ${className}`}
      aria-labelledby="what-can-happen-next-title"
    >
      {/* 1. Header & Concept Explainer */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-6 border-b border-paper-200 dark:border-slate-800">
        <div className="space-y-1.5 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-50 dark:bg-amber-950/60 border border-amber-300 dark:border-amber-800 text-amber-900 dark:text-amber-300 text-xs font-mono font-bold uppercase tracking-wider">
            <Layers className="w-3.5 h-3.5" />
            <span>DISASTER CONSEQUENCE INTELLIGENCE</span>
          </div>
          <h2
            id="what-can-happen-next-title"
            className="text-2xl sm:text-3xl font-black text-charcoal-950 dark:text-white tracking-tight"
          >
            What Can Happen Next?
          </h2>
          <p className="text-xs sm:text-sm text-charcoal-600 dark:text-slate-300 leading-relaxed font-sans">
            Disaster impact rarely stops at the primary event. A flood triggers slope failures, water supply contamination, and power outages. Understand the physical sequence of consequences so you can prepare for secondary hazards before they strike.
          </p>
        </div>

        {/* Quick Hazard Switcher */}
        <div className="flex flex-wrap items-center gap-1.5 self-start lg:self-center">
          {Object.keys(CASCADING_PATHWAYS).map((hKey) => {
            const isSelected = activeHazard === hKey;
            const p = CASCADING_PATHWAYS[hKey];
            return (
              <button
                key={hKey}
                onClick={() => {
                  setActiveHazard(hKey);
                  setExpandedSecondary(0);
                }}
                className={`min-h-[40px] px-3 py-1.5 rounded-xl text-xs font-mono font-bold transition-all flex items-center gap-1.5 ${
                  isSelected
                    ? 'bg-charcoal-950 dark:bg-white text-white dark:text-charcoal-950 shadow-xs'
                    : 'bg-paper-100 dark:bg-slate-800 text-charcoal-700 dark:text-slate-300 hover:bg-paper-200 dark:hover:bg-slate-700 border border-paper-200 dark:border-slate-700'
                }`}
                aria-pressed={isSelected}
              >
                <span>{p.icon}</span>
                <span>{hKey.replace('_', ' ')}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* 2. 3-Stage Consequence Pipeline */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* LEVEL 1: IMMEDIATE IMPACT */}
        <div className="p-5 rounded-2xl bg-paper-50 dark:bg-slate-850 border border-paper-200 dark:border-slate-800 space-y-3 flex flex-col justify-between">
          <div className="space-y-2">
            <div className="flex items-center justify-between gap-2">
              <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-charcoal-500 dark:text-slate-400">
                STAGE 1 // PRIMARY IMPACT
              </span>
              <span className="px-2 py-0.5 rounded-md bg-paper-200 dark:bg-slate-800 text-[10px] font-mono font-semibold text-charcoal-700 dark:text-slate-300">
                0–6 Hours
              </span>
            </div>
            <h3 className="text-base font-bold text-charcoal-950 dark:text-white">
              {pathway.immediate.title}
            </h3>
            <p className="text-xs text-charcoal-600 dark:text-slate-400 leading-relaxed">
              {pathway.immediate.description}
            </p>

            <ul className="space-y-2 pt-2 text-xs text-charcoal-800 dark:text-slate-200">
              {pathway.immediate.items.map((item, idx) => (
                <li key={idx} className="flex items-start gap-2 pl-1">
                  <span className="text-indigo-600 dark:text-indigo-400 font-bold shrink-0">•</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="pt-3 border-t border-paper-200 dark:border-slate-800 text-[10px] font-mono text-charcoal-500 dark:text-slate-400">
            Initial trigger phase
          </div>
        </div>

        {/* LEVEL 2: SECONDARY EFFECTS (INTERACTIVE) */}
        <div className="p-5 rounded-2xl bg-amber-50/50 dark:bg-amber-950/20 border-2 border-amber-300 dark:border-amber-800/80 space-y-3 flex flex-col justify-between shadow-sm">
          <div className="space-y-2">
            <div className="flex items-center justify-between gap-2">
              <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-amber-800 dark:text-amber-300">
                STAGE 2 // SECONDARY HAZARDS
              </span>
              <span className="px-2 py-0.5 rounded-md bg-amber-100 dark:bg-amber-900/60 text-[10px] font-mono font-bold text-amber-900 dark:text-amber-200">
                6–24 Hours
              </span>
            </div>
            <h3 className="text-base font-bold text-charcoal-950 dark:text-white">
              {pathway.secondary.title}
            </h3>
            <p className="text-xs text-charcoal-700 dark:text-slate-300 leading-relaxed">
              {pathway.secondary.description}
            </p>

            {/* Accordion / Selector for Secondary Effects */}
            <div className="space-y-2 pt-1">
              {pathway.secondary.items.map((sec, idx) => {
                const isItemExpanded = expandedSecondary === idx;
                return (
                  <div
                    key={idx}
                    className={`rounded-xl border transition-all ${
                      isItemExpanded
                        ? 'bg-white dark:bg-slate-900 border-amber-400 dark:border-amber-700 shadow-xs'
                        : 'bg-white/60 dark:bg-slate-900/60 border-paper-200 dark:border-slate-800'
                    }`}
                  >
                    <button
                      onClick={() => setExpandedSecondary(isItemExpanded ? null : idx)}
                      className="w-full text-left p-3 flex items-center justify-between gap-2 focus:outline-none focus-visible:ring-2 focus-visible:ring-amber-500 rounded-xl"
                      aria-expanded={isItemExpanded}
                    >
                      <span className="text-xs font-bold text-charcoal-900 dark:text-white">
                        {sec.name}
                      </span>
                      <span className="text-amber-700 dark:text-amber-400 font-mono text-xs shrink-0">
                        {isItemExpanded ? '▲' : '▼'}
                      </span>
                    </button>

                    {isItemExpanded && (
                      <div className="p-3 pt-0 text-xs space-y-2 text-charcoal-700 dark:text-slate-300 border-t border-paper-100 dark:border-slate-800/80 mt-1">
                        <p className="leading-relaxed">
                          <strong className="text-charcoal-900 dark:text-white font-mono text-[11px] uppercase">Why: </strong>
                          {sec.explanation}
                        </p>
                        <div className="p-2 rounded-lg bg-amber-50 dark:bg-amber-950/40 text-amber-950 dark:text-amber-200 text-[11px]">
                          <strong className="font-mono uppercase font-bold">Watch For: </strong>
                          <span>{sec.watchFor}</span>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          <div className="pt-3 border-t border-amber-200 dark:border-amber-900/60 text-[10px] font-mono text-amber-800 dark:text-amber-300 font-bold">
            Physically plausible consequence pathways
          </div>
        </div>

        {/* LEVEL 3: DOWNSTREAM SYSTEMIC CONSEQUENCES */}
        <div className="p-5 rounded-2xl bg-indigo-50/40 dark:bg-indigo-950/20 border border-indigo-200 dark:border-indigo-850 space-y-3 flex flex-col justify-between">
          <div className="space-y-2">
            <div className="flex items-center justify-between gap-2">
              <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-indigo-700 dark:text-indigo-300">
                STAGE 3 // SYSTEMIC IMPACTS
              </span>
              <span className="px-2 py-0.5 rounded-md bg-indigo-100 dark:bg-indigo-900/60 text-[10px] font-mono font-bold text-indigo-900 dark:text-indigo-200">
                24–72+ Hours
              </span>
            </div>
            <h3 className="text-base font-bold text-charcoal-950 dark:text-white">
              {pathway.downstream.title}
            </h3>
            <p className="text-xs text-charcoal-600 dark:text-slate-300 leading-relaxed">
              {pathway.downstream.description}
            </p>

            <div className="space-y-2 pt-1 text-xs">
              {pathway.downstream.items.map((down, idx) => (
                <div
                  key={idx}
                  className="p-2.5 rounded-xl bg-white dark:bg-slate-900 border border-indigo-100 dark:border-indigo-900/50 space-y-1"
                >
                  <div className="font-bold text-charcoal-900 dark:text-white text-xs">
                    {down.name}
                  </div>
                  <p className="text-[11px] text-charcoal-600 dark:text-slate-400 leading-relaxed">
                    {down.impact}
                  </p>
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1.5 pt-1.5 border-t border-indigo-50 dark:border-slate-800">
                    <div className="text-[11px] text-emerald-800 dark:text-emerald-300 font-medium flex items-start gap-1">
                      <ShieldCheck className="w-3.5 h-3.5 shrink-0 text-emerald-600 mt-0.5" />
                      <span>{down.defensiveAction}</span>
                    </div>
                    <button
                      onClick={() => onNavigate && onNavigate('safety-guide')}
                      className="min-h-[32px] px-2.5 py-1 rounded-lg bg-emerald-50 hover:bg-emerald-100 dark:bg-emerald-950/60 dark:hover:bg-emerald-900/80 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 text-[10px] font-mono font-bold flex items-center gap-1 self-start sm:self-auto shrink-0 transition-colors"
                    >
                      <span>
                        {down.name.toLowerCase().includes('water')
                          ? '💧 WATER SAFETY'
                          : down.name.toLowerCase().includes('power')
                          ? '⚡ POWER SAFETY'
                          : down.name.toLowerCase().includes('landslide')
                          ? '⛰️ LANDSLIDE SAFETY'
                          : '🛡️ DEFENSIVE ACTION'}
                      </span>
                      <ArrowRight className="w-3 h-3" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="pt-3 border-t border-indigo-200 dark:border-indigo-900 text-[10px] font-mono text-indigo-700 dark:text-indigo-300">
            Societal & infrastructural reverberations
          </div>
        </div>
      </div>

      {/* 3. Cross-Hazard Interaction Callout */}
      <div className="p-4 rounded-2xl bg-paper-50 dark:bg-slate-850 border border-paper-200 dark:border-slate-800 flex items-start gap-3 text-xs">
        <GitBranch className="w-4 h-4 text-indigo-600 dark:text-indigo-400 shrink-0 mt-0.5" />
        <div className="space-y-0.5">
          <strong className="font-mono text-charcoal-900 dark:text-white uppercase">
            Cross-Hazard Vulnerability Linkage:
          </strong>
          <p className="text-charcoal-700 dark:text-slate-300 font-sans leading-relaxed">
            {pathway.crossHazardNote}
          </p>
        </div>
      </div>

      {/* 4. Action CTAs */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 pt-4 border-t border-paper-200 dark:border-slate-800">
        <div className="text-xs font-mono text-charcoal-500 dark:text-slate-400">
          Source: Physically established relationships • Zero fabricated probabilities
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <button
            onClick={() => onNavigate && onNavigate('cascading-risk')}
            className="min-h-[44px] px-4 py-2 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-mono text-xs font-bold transition-all shadow-xs flex items-center gap-2"
          >
            <span>EXPLORE FULL CASCADING RISK CHAIN</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>

          <button
            onClick={() => onNavigate && onNavigate('safety-guide')}
            className="min-h-[44px] px-4 py-2 rounded-xl bg-paper-100 hover:bg-paper-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-charcoal-900 dark:text-white border border-paper-300 dark:border-slate-700 font-mono text-xs font-bold transition-all flex items-center gap-2"
          >
            <BookOpen className="w-3.5 h-3.5 text-emerald-600" />
            <span>VIEW COMPLETE SAFETY ACTION GUIDE</span>
          </button>
        </div>
      </div>
    </section>
  );
};
