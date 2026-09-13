import { PreparednessGuide } from '../types/chat';

export const PREPAREDNESS_GUIDES: PreparednessGuide[] = [
  {
    disaster: 'Flood',
    iconName: 'Waves',
    tagline: 'Rising waters give warning signals. Early action saves lives and property.',
    overview: 'Floods are India’s most frequent natural calamity, affecting plains, river valleys, and urban watersheds during the monsoons.',
    phases: [
      {
        phase: 'Before',
        title: 'Preparation & Mitigation',
        criticalItem: 'Prepare a 72-hour waterproof grab-and-go emergency kit',
        instructions: [
          'Know your local flood plain elevation and identify high ground evacuation routes.',
          'Store drinking water in sealed containers; floodwaters quickly contaminate ground sources.',
          'Keep important identity cards, land deeds, and medical prescriptions in a watertight bag.',
          'Install check valves in home sewer drains to prevent floodwater backflow into sinks and toilets.'
        ]
      },
      {
        phase: 'During',
        title: 'Immediate Protective Action',
        criticalItem: 'Never drive, walk, or wade through moving water',
        instructions: [
          'Move immediately to the highest accessible level or official multi-purpose shelter.',
          'Turn off main electrical breaker and gas connections before evacuating.',
          'Avoid downed power lines, electrical substations, and submerged transformers.',
          'Listen continuously to local disaster authority radio bulletins for crest time estimates.'
        ]
      },
      {
        phase: 'After',
        title: 'Recovery & Health Safety',
        criticalItem: 'Boil or chemically treat all water before drinking',
        instructions: [
          'Return home only after local authorities declare the area safe and structurally sound.',
          'Inspect foundation walls, electrical conduits, and gas lines for damage before entering.',
          'Discard all food, perishables, and medicines that came in contact with flood water.',
          'Disinfect living areas with chlorine solution to prevent leptospirosis and waterborne infections.'
        ]
      }
    ]
  },
  {
    disaster: 'Landslide',
    iconName: 'Mountain',
    tagline: 'Slope stability can change rapidly during prolonged downpours.',
    overview: 'Landslides are prevalent across the Himalayas, Western Ghats, and North-Eastern hill states, triggered by heavy precipitation, slope cuts, or seismic tremors.',
    phases: [
      {
        phase: 'Before',
        title: 'Geological Hazard Awareness',
        criticalItem: 'Monitor hillside retaining walls for new cracks or tilting',
        instructions: [
          'Observe drainage slopes behind your house; watch for sudden changes in runoff turbidity.',
          'Plant native deep-rooted vegetation on slopes to bind topsoil cohesion.',
          'Consult local administration before building near steep slopes, ravine edges, or fault tracks.',
          'Keep an emergency vehicle parked facing uphill or in an unobstructed evacuation direction.'
        ]
      },
      {
        phase: 'During',
        title: 'Evasion & Immediate Shelter',
        criticalItem: 'Move quickly away from the path of debris flow',
        instructions: [
          'If you notice trees cracking, boulders clattering, or rumbling sounds, evacuate immediately.',
          'Run to higher, stable ground perpendicular to the direction of the landslide slide.',
          'If escape is impossible, curl into a tight protective ball and shield your head with your arms.',
          'Stay alert for secondary slides, which often follow initial debris failure.'
        ]
      },
      {
        phase: 'After',
        title: 'Inspection & Cautious Re-entry',
        criticalItem: 'Stay clear of the slide zone; sudden re-activation is common',
        instructions: [
          'Check for trapped or injured persons near the slide perimeter without entering unstable mud.',
          'Report broken utility lines (power, water, telecom) immediately to district control 1077.',
          'Check building foundations, chimneys, and surrounding ground for structural fissures.',
          'Replant damaged soil surfaces promptly to prevent subsequent erosion.'
        ]
      }
    ]
  },
  {
    disaster: 'Cyclone',
    iconName: 'Wind',
    tagline: 'Modern early warnings provide crucial hours to secure shelters and assets.',
    overview: 'Tropical cyclones strike both the East and West coasts of India, bringing destructive gale-force winds, torrential rains, and dangerous marine storm surges.',
    phases: [
      {
        phase: 'Before',
        title: 'Structural Reinforcement & Stocking',
        criticalItem: 'Board up or tape glass windows; trim tree branches near power lines',
        instructions: [
          'Clear roofs of loose asbestos sheets, corrugated metal, or construction debris.',
          'Charge power banks, mobile phones, emergency lamps, and maintain a radio transceiver.',
          'Locate your nearest fortified cyclone shelter and map the safest path to it.',
          'Anchor livestock securely in designated concrete livestock enclosures.'
        ]
      },
      {
        phase: 'During',
        title: 'Gale & Surge Survival',
        criticalItem: 'Stay indoors away from windows; do not venture out during the eye of the storm',
        instructions: [
          'Remain in the strongest interior room of the house or within an official cyclone shelter.',
          'Keep electrical mains switched off to prevent fire hazards from line short-circuits.',
          'The calm "eye" of the cyclone is deceptive—winds will resume suddenly from the opposite direction.',
          'Do not go outside to inspect roof damage until the all-clear is officially broadcast.'
        ]
      },
      {
        phase: 'After',
        title: 'Post-Storm Hazard Avoidance',
        criticalItem: 'Beware of snapped live electric wires dangling in puddles',
        instructions: [
          'Do not touch damp electric appliances or poles until inspected by electricity board staff.',
          'Report gas leaks or petroleum odor to fire emergency services immediately.',
          'Use chlorinated or boiled water to prevent cholera and diarrhea outbreaks.',
          'Help neighbors, especially the elderly, infants, and persons with disabilities.'
        ]
      }
    ]
  },
  {
    disaster: 'Earthquake',
    iconName: 'Activity',
    tagline: 'Earthquakes occur without warning. Instinctive Drop, Cover, and Hold saves lives.',
    overview: 'Over 59% of India’s landmass is vulnerable to moderate to severe seismic shocks across Zones II to V.',
    phases: [
      {
        phase: 'Before',
        title: 'Structural Safety & Drills',
        criticalItem: 'Fasten tall heavy furniture, water heaters, and mirrors securely to wall studs',
        instructions: [
          'Identify safe spots in every room: under sturdy desks, against interior walls, away from glass.',
          'Teach all family members how to shut off the gas meter, main water valve, and electrical fuse.',
          'Conduct regular "Drop, Cover, and Hold On" practice drills with family members.',
          'Keep heavy hanging pots, photo frames, and ceiling fans tightly anchored.'
        ]
      },
      {
        phase: 'During',
        title: 'Drop, Cover, and Hold On',
        criticalItem: 'Do not rush outside during tremors or use elevators',
        instructions: [
          'DROP down onto your hands and knees to prevent being thrown down.',
          'COVER your head and neck beneath a sturdy table or desk. If no shelter, cover head with arms against an inside wall.',
          'HOLD ON to your shelter until shaking completely ceases.',
          'If outdoors: Move to an open area away from high buildings, glass facades, power poles, and trees.'
        ]
      },
      {
        phase: 'After',
        title: 'Aftershock Readiness & Evacuation',
        criticalItem: 'Expect aftershocks. Use stairs only; never use elevators',
        instructions: [
          'Check yourself and family for injuries; apply first aid before helping others.',
          'Sniff for gas leaks. If smelled, open windows, evacuate immediately, and do not switch any lights on/off.',
          'Wear sturdy shoes to protect feet from broken glass and debris.',
          'Tune in to emergency radio announcements for damage assessments and open shelters.'
        ]
      }
    ]
  },
  {
    disaster: 'Heatwave',
    iconName: 'Sun',
    tagline: 'Extreme temperatures can cause life-threatening hyperthermia without precautions.',
    overview: 'Severe heatwave conditions affect northern, central, and peninsular India during summer months, exacerbated by urban heat island effects.',
    phases: [
      {
        phase: 'Before',
        title: 'Hydration & Home Thermal Shielding',
        criticalItem: 'Keep oral rehydration salts (ORS), buttermilk, and lemon water readily accessible',
        instructions: [
          'Install dark curtains, reflective blinds, or white lime-wash on roofs to reduce heat ingress.',
          'Plan outdoor work strictly for early mornings (before 10 AM) or evenings (after 5 PM).',
          'Ensure continuous access to shaded resting quarters for domestic workers and delivery personnel.',
          'Equip vehicles with window sunshades and drinking water flasks.'
        ]
      },
      {
        phase: 'During',
        title: 'Peak Sun Protection & Cooling',
        criticalItem: 'Never leave children or pets inside a parked vehicle, even for a few minutes',
        instructions: [
          'Drink water frequently throughout the day, even if not feeling thirsty.',
          'Wear loose, lightweight, light-colored, full-sleeve cotton clothing and wide-brim hats.',
          'Recognize heat exhaustion symptoms: dizziness, excessive sweating, headache, nausea, and pale skin.',
          'If someone suffers heatstroke (high body temp, cessation of sweating, confusion), move to shade and sponge with cool water immediately.'
        ]
      },
      {
        phase: 'After',
        title: 'Recovery & Community Care',
        criticalItem: 'Replenish electrolytes and maintain cool environment during sleep',
        instructions: [
          'Rest in ventilated, cooled rooms to allow core body temperature to reset.',
          'Offer hydration support and shade to stray animals, birds, and neighborhood workers.',
          'Continue adequate electrolyte hydration for 24-48 hours post-exposure.',
          'Seek medical consultation if weakness, vomiting, or muscle cramps persist.'
        ]
      }
    ]
  }
];
