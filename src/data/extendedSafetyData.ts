/**
 * RISK // INDIA — Extended Citizen Disaster Safety Guidance Master Dataset
 * =========================================================================
 * Comprehensive Before / During / After life-safety guidelines across all 6 hazards.
 * Aligned with NDMA Standard Operating Procedures, IMD Guidelines, and the Disaster Management Act 2005.
 * Features progressive disclosure: short summary default, rich on-demand details
 * (Why this matters, What to do, Warning signs, What not to do, Vulnerable groups, Action checklist).
 */

import { SafetyInstructionItem, HazardSafetyGuide } from '../types/safetyGuide';

export const EXTENDED_SAFETY_ITEMS: SafetyInstructionItem[] = [
  // =========================================================================
  // 1. FLOOD
  // =========================================================================
  // --- FLOOD: BEFORE ---
  {
    id: 'fld-bef-01',
    hazard: 'FLOOD',
    phase: 'BEFORE',
    category: 'WATER_AND_FOOD',
    title: 'Store Potable Drinking Water in Sealed Containers',
    instruction: 'Store at least 3 to 4 litres of clean drinking water per person per day for a minimum 72-hour period in elevated, food-grade vessels.',
    priority: 'CRITICAL',
    reason: 'Floodwaters submerge municipal distribution pipes and open wells, introducing pathogenic sewage and industrial effluent into the water table.',
    source: 'NDMA National Disaster Management Guidelines: Management of Floods (Section 4.3)',
    warning: 'Do not rely on municipal tap water or domestic borewells once floodwaters approach residential sectors.',
    related_cascading_risk: 'Water supply contamination and enteric waterborne epidemics (Cholera, Typhoid).',
    practical_steps: [
      'Thoroughly wash and sanitize jerrycans or large glass/food-grade plastic drums with mild chlorine bleach.',
      'Store at least 12 to 15 litres per person to cover drinking, infant formula, and basic oral hygiene.',
      'Keep water containers elevated on tables or shelves at least 1 meter above expected ground inundation level.',
      'Store water purification tablets (Halazone / Chlorine 33-50mg) and oral rehydration salts (ORS) nearby.'
    ],
    warning_signs: [
      'Municipal water coming out discolored, silty, or with an unusual odor.',
      'Local river basin telemetry crossing Warning Level upstream.',
      'Persistent heavy rainfall exceeding 65 mm in 24 hours in your catchment area.'
    ],
    what_not_to_do: [
      'Do not use untreated ground floodwater for brushing teeth or washing vegetables.',
      'Do not store water in open buckets or unsealed steel containers vulnerable to insect breeding and silt.'
    ],
    vulnerable_groups: 'Infants, dialysis patients, and nursing mothers need strictly sterile boiled water. Prepare pre-measured sealed bottles.',
    checklist: [
      'Fill minimum 15 litres clean drinking water per household member.',
      'Keep 20 water purification chlorine tablets in waterproof emergency pack.',
      'Elevate water containers to upper shelf or first floor.'
    ]
  },
  {
    id: 'fld-bef-02',
    hazard: 'FLOOD',
    phase: 'BEFORE',
    category: 'CRITICAL_DOCUMENTS',
    title: 'Secure Essential Identity & Property Records in Waterproof Pouches',
    instruction: 'Place Aadhaar cards, voter IDs, ration cards, property deeds, bank passbooks, and insurance policies into double-sealed waterproof zipbags.',
    priority: 'HIGH',
    reason: 'Identity proof and property records are required by revenue authorities for statutory calamity relief disbursement, ex-gratia compensation, and insurance claims under the DM Act 2005.',
    source: 'Ministry of Home Affairs / NDMA Calamity Relief Documentation SOP',
    warning: 'Loss of official identification severely delays access to emergency government relief funds and temporary shelter verification.',
    related_cascading_risk: 'Post-disaster bureaucratic recovery paralysis and displaced household identity loss.',
    practical_steps: [
      'Scan or photograph all key documents and save copies in DigiLocker or encrypted cloud storage.',
      'Place original documents inside laminated or heavy-duty zip bags with moisture-absorbing silica packets.',
      'Store the waterproof pouch in your grab-and-go emergency backpack near your primary exit.',
      'Include 4 passport-size photographs of every family member for relief identification cards.'
    ],
    warning_signs: [
      'Local administration issues Yellow or Orange alert for river cresting within 24 hours.'
    ],
    what_not_to_do: [
      'Do not leave legal documents inside ground-floor wooden drawers or floor-level metal cupboards.'
    ],
    vulnerable_groups: 'Ensure pension passbooks, disability certificates (UDID), and chronic prescription charts are bundled together.',
    checklist: [
      'Aadhaar / Voter ID / Ration cards sealed in ziplock bag.',
      'Property deeds, vehicle registrations, and insurance papers packed.',
      'Backup photographs and digital copies saved on mobile phone.'
    ]
  },
  {
    id: 'fld-bef-03',
    hazard: 'FLOOD',
    phase: 'BEFORE',
    category: 'SAFE_ROUTES_EVACUATION',
    title: 'Pre-Identify Elevated Evacuation Routes & Concrete Multi-Purpose Shelters',
    instruction: 'Map at least two elevated escape paths to designated community cyclone/flood shelters or reinforced public buildings.',
    priority: 'CRITICAL',
    reason: 'Low-lying culverts, railway underpasses, and earthen village causeways flood hours before main riverbanks breach.',
    source: 'CWC Flood Forecasting & Inundation Mapping Handbook',
    warning: 'Never plan an escape route that crosses earthen canal bunds, wooden bridges, or low-water causeways.',
    related_cascading_risk: 'Transportation corridor severance, stranded vehicles, and rapid isolation.',
    practical_steps: [
      'Contact local Gram Panchayat or Ward Councillor to confirm the designated municipal shelter location.',
      'Walk or drive the route in advance to identify low dips, open storm gutters, and culverts.',
      'Agree on an emergency family rendezvous point outside the inundation zone if separated during evacuation.',
      'Fuel vehicles and park them on highest available concrete ground facing outbound.'
    ],
    warning_signs: [
      'Local storm drains backing up and bubbling onto roadways during high tide or sustained rainfall.',
      'CWC flood bulletin indicates river gauge surging >0.2m per hour.'
    ],
    what_not_to_do: [
      'Do not wait until floodwater reaches your door to begin evacuation route planning.',
      'Do not attempt evacuation after nightfall through unlit rural paths without high-power torchlights.'
    ],
    vulnerable_groups: 'Persons using wheelchairs or walkers require pre-arranged transport with neighborhood volunteers before roads submerge.',
    checklist: [
      'Primary and secondary elevated escape routes mapped.',
      'Nearest government school/shelter confirmed open.',
      'Vehicle fuel tank at least half full.'
    ]
  },
  {
    id: 'fld-bef-04',
    hazard: 'FLOOD',
    phase: 'BEFORE',
    category: 'VULNERABLE_MEMBERS',
    title: 'Arrange Early Safe Relocation for High-Risk Household Members',
    instruction: 'Relocate elderly family members, pregnant women, infants, and medically dependent persons to elevated relatives\' homes before water levels surge.',
    priority: 'CRITICAL',
    reason: 'Mobility-impaired individuals and those requiring electricity for oxygen concentrators or insulin cannot navigate sudden flash flood rescues.',
    source: 'NDMA Guidelines on Disability Inclusive Disaster Risk Reduction (DiDRR)',
    related_cascading_risk: 'Emergency rescue bottlenecks during rapid inundation and hospital evacuation surges.',
    practical_steps: [
      'Assemble a 7-day reserve of essential daily medications, insulin ice-packs, and prescription copies.',
      'Arrange safe transport with relatives on elevated ground 24 hours prior to anticipated river crest.',
      'Register medically vulnerable household members with the local District Disaster Management Authority (DDMA) control room.'
    ],
    warning_signs: [
      'Civil administration issues evacuation advisory for low-lying or riverine wards.'
    ],
    what_not_to_do: [
      'Do not leave bedridden or elderly family members alone on ground floors while running errands.'
    ],
    vulnerable_groups: 'Check that assistive mobility devices (canes, wheelchairs, hearing aids with spare batteries) are immediately accessible.',
    checklist: [
      '7-day medicine reserve packed in waterproof bag.',
      'Doctor contact numbers and hospital record booklet gathered.',
      'Transportation to elevated relative home arranged.'
    ]
  },
  {
    id: 'fld-bef-05',
    hazard: 'FLOOD',
    phase: 'BEFORE',
    category: 'PETS_AND_LIVESTOCK',
    title: 'Untie Cattle & Relocate Domestic Livestock to Raised Highland Enclosures',
    instruction: 'Untie all domestic animals and move cattle, goats, and working animals to designated community highlands or elevated road embankments.',
    priority: 'HIGH',
    reason: 'Tethered cattle drown helplessly in sudden floodwater surges. Untying them allows natural swimming and survival instincts to take over.',
    source: 'Department of Animal Husbandry and Dairying Disaster Management Plan',
    warning: 'Never leave domestic animals tied to sheds, fences, or iron stakes in flood-prone floodplains.',
    related_cascading_risk: 'Mass livestock mortality causing post-flood biological contamination, carcass putrefaction, and anthrax outbreaks.',
    practical_steps: [
      'Move livestock to elevated community highlands, school compounds, or highway shoulders before roads are cut off.',
      'Stock dry paddy straw and feed bags on elevated bamboo machans (platforms) covered with tarpaulin.',
      'Attach identification tags or microchip records to cattle horns/collars.'
    ],
    warning_signs: [
      'Rising water in drainage channels adjacent to animal sheds.',
      'Animals displaying agitation and restlessness due to low-frequency ground vibrations of rushing water.'
    ],
    what_not_to_do: [
      'Do not keep animals tied inside low tin-roof stables where water levels can touch the ceiling.'
    ],
    vulnerable_groups: 'Young calves, pregnant cows, and poultry require immediate elevation inside protective bamboo crates.',
    checklist: [
      'Untie all cattle and livestock.',
      'Move herd to designated community highland embankment.',
      'Stage dry fodder and clean water troughs at elevated ground.'
    ]
  },
  // --- FLOOD: DURING ---
  {
    id: 'fld-dur-01',
    hazard: 'FLOOD',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Never Walk, Swim, or Drive Through Moving Floodwaters',
    instruction: 'Obey the universal 15 cm / 30 cm rule: Just 15 cm (6 in) of moving water knocks an adult down; 30 cm floats a car; 60 cm sweeps away an SUV.',
    priority: 'CRITICAL',
    reason: 'Moving floodwaters exert immense hydrodynamic drag, conceal washed-out roadbeds, submerged manholes, and live high-voltage electric cables.',
    source: 'NDMA Standard Operating Procedure for Flood Response',
    warning: 'Over 50% of flood fatalities occur in vehicles attempting to cross inundated roads or submerged causeways. Turn around, don\'t drown!',
    related_cascading_risk: 'Immediate drowning, vehicle entrapment, and electrocution from severed sub-station lines.',
    practical_steps: [
      'If caught on foot in rising water, turn around immediately and retreat to higher dry ground.',
      'If water rises around your vehicle, abandon the car immediately and move to higher ground if water is stationary.',
      'Use a long sturdy stick or pole to probe the ground ahead of you if walking through shallow water is strictly unavoidable.'
    ],
    warning_signs: [
      'Water rushing across asphalt with surface ripples or white foam.',
      'Floating debris (logs, oil slicks, corrugated metal sheets) moving rapidly.'
    ],
    what_not_to_do: [
      'Never drive past official police barricades or road-closed warning cones.',
      'Do not allow children to play, bathe, or wade in street floodwater.'
    ],
    vulnerable_groups: 'Hold children securely above chest level; never transport infants in low prams or strollers through water.',
    checklist: [
      'Turn vehicle around when approaching submerged road.',
      'Carry sturdy walking stick if walking through shallow standing water.'
    ]
  },
  {
    id: 'fld-dur-02',
    hazard: 'FLOOD',
    phase: 'DURING',
    category: 'UTILITY_SAFETY',
    title: 'Isolate Main Electrical Breakers & Shut Off LPG Gas Cylinders',
    instruction: 'Switch off main electrical fuse/MCB switchboard and tightly screw shut LPG regulator valves before floodwaters enter your dwelling.',
    priority: 'CRITICAL',
    reason: 'Submerged electrical wiring causes lethal water electrification and high-temperature arcing; buoyant gas cylinders rupture and cause explosion fires.',
    source: 'Central Electricity Authority (Safety Requirements) & NDMA Fire Safety SOP',
    warning: 'Never touch electrical switches, fuse boxes, or plugged-in appliances while standing in wet footwear or water.',
    related_cascading_risk: 'Secondary electrical fires, lethal electrocution, and residential LPG explosions.',
    practical_steps: [
      'Locate main distribution box; flip main switch to OFF using a dry wooden stick or wearing dry rubber slippers.',
      'Disconnect LPG cylinder regulator; screw safety plastic cap onto the valve and move cylinder to high shelf or roof.',
      'Unplug all electronics from floor-level wall sockets.'
    ],
    warning_signs: [
      'Flickering house lights or buzzing sound from walls/meter box.',
      'Smell of rotten eggs (ethyl mercaptan) signaling gas leak.'
    ],
    what_not_to_do: [
      'Do not use matches, lighters, or open kerosene lamps in flooded rooms where gas may be trapped.'
    ],
    vulnerable_groups: 'Ensure battery-powered medical equipment (e.g. oxygen monitors) is disconnected from wall chargers and running on internal cells.',
    checklist: [
      'Main MCB / fuse flipped to OFF.',
      'LPG regulator shut off and cylinder placed on raised platform.',
      'Appliances unplugged from lower sockets.'
    ]
  },
  {
    id: 'fld-dur-03',
    hazard: 'FLOOD',
    phase: 'DURING',
    category: 'SHELTER',
    title: 'Ascend to Highest Floor or Rooftop with Signaling Gear',
    instruction: 'If trapped indoors by sudden inundation, move immediately to the highest floor or accessible rooftop. Do NOT hide in enclosed attics.',
    priority: 'CRITICAL',
    reason: 'Rising waters can seal closed attics and low-clearance false ceilings against the roofline, creating a fatal drowning trap without an exterior escape hatch.',
    source: 'NDRF Life-Safety Protocol for Inundated Structural Extrication',
    warning: 'Only enter an attic or loft if it has an open skylight, roof hatch, or exterior window large enough for an adult exit.',
    related_cascading_risk: 'Ceiling space entrapment and delayed rescue by helicopter/boat crews.',
    practical_steps: [
      'Take emergency grab-bag, drinking water, whistle, mobile phone, and flashlight to the roof.',
      'Display a brightly colored cloth (red/orange dupatta or bedsheet) on the roof terrace to signal aerial reconnaissance helicopters.',
      'Use whistle (three short blasts) to attract passing NDRF/SDRF rescue boat crews.'
    ],
    warning_signs: [
      'Water rising more than 15 cm per hour inside ground-floor rooms.',
      'Structural vibrations or cracking sounds in ground-floor masonry walls.'
    ],
    what_not_to_do: [
      'Do not climb into an attic without an axe or heavy hammer to break through roof tiles if necessary.'
    ],
    vulnerable_groups: 'Assist children and elderly to upper floors first; wrap them in dry blankets or waterproof sheets to prevent hypothermia.',
    checklist: [
      'Household members assembled on highest floor or rooftop terrace.',
      'Emergency whistle and bright signaling cloth deployed.',
      'Phone battery preserved in ultra-power saver mode.'
    ]
  },
  // --- FLOOD: AFTER ---
  {
    id: 'fld-aft-01',
    hazard: 'FLOOD',
    phase: 'AFTER',
    category: 'STRUCTURAL_SAFETY',
    title: 'Inspect Foundation Walls & Load-Bearing Elements Before Re-Entering',
    instruction: 'Check exterior walls, foundation perimeters, and balconies for deep settlement cracks, tilting pillars, or eroded soil before stepping inside.',
    priority: 'CRITICAL',
    reason: 'Prolonged pore-water saturation reduces soil bearing capacity and washes out sub-base gravel, leading to sudden progressive structural collapse after floodwaters recede.',
    source: 'National Building Code of India (NBC 2016) / NDMA Structural Post-Flood SOP',
    warning: 'Do not enter any house showing diagonal wall cracks wider than 5 mm or doors jammed tightly in their doorframes.',
    related_cascading_risk: 'Secondary structural collapse, building pancake failures, and crushing injuries.',
    practical_steps: [
      'Walk completely around building perimeter during daylight; inspect plinth level for soil hollows.',
      'Check if porch pillars or exterior staircases have pulled away from the main building frame.',
      'Open windows and doors to cross-ventilate stagnant damp air before dwelling inside.'
    ],
    warning_signs: [
      'Fresh diagonal cracks in exterior brickwork or around lintels.',
      'Sagging ceiling plaster or damp-swollen roof slabs.'
    ],
    what_not_to_do: [
      'Do not rush into flooded basements or rooms while heavy water is still resting against exterior walls (differential hydrostatic pressure may cave walls inward).'
    ],
    vulnerable_groups: 'Do not allow children or elderly to enter the premises until an able-bodied adult has verified structural stability.',
    checklist: [
      'Perimeter foundation inspected for soil erosion.',
      'Doors and window alignments checked for structural racking.',
      'Rooms cross-ventilated before occupancy.'
    ]
  },
  {
    id: 'fld-aft-02',
    hazard: 'FLOOD',
    phase: 'AFTER',
    category: 'SANITATION',
    title: 'Disinfect All Living Surfaces with Sodium Hypochlorite / Bleach',
    instruction: 'Scrub all flooded floors, walls, and hard furniture with a 1:10 household bleach solution or sodium hypochlorite disinfectant.',
    priority: 'HIGH',
    reason: 'Receding flood mud carries high titers of sewage bacteria, Leptospira interrogans from rodent urine, and mold spores that cause deadly pulmonary and gastrointestinal infections.',
    source: 'National Centre for Disease Control (NCDC) Guidelines for Post-Flood Disease Prevention',
    warning: 'Wear thick rubber boots and nitrile gloves; never touch flood mud or sludge with bare hands or open cuts.',
    related_cascading_risk: 'Leptospirosis, Acute Diarrheal Disease (ADD), and fungal mold toxicities.',
    practical_steps: [
      'Shovel out all silt and mud before it dries into hardened concrete-like cakes.',
      'Wash surfaces with clean water and detergent, then apply diluted bleach solution (50ml bleach per 5L water).',
      'Leave disinfectant on surfaces for at least 15 minutes before rinsing with clean water.',
      'Dry mattresses and upholstered furniture thoroughly in direct sunlight for at least 3 consecutive days or discard.'
    ],
    warning_signs: [
      'Musty damp odor in living areas indicates rapid black mold colonization.',
      'Presence of dead rodents or frogs in receding silt.'
    ],
    what_not_to_do: [
      'Never mix chlorine bleach with ammonia or acid-based toilet cleaners (releases lethal toxic chlorine gas).'
    ],
    vulnerable_groups: 'Asthma and allergy sufferers should stay away during bleaching and mold scraping.',
    checklist: [
      'Wear rubber boots and heavy cleaning gloves.',
      'Disinfect hard surfaces with diluted bleaching solution.',
      'Discard flood-soaked mattresses and pillows.'
    ]
  },
  {
    id: 'fld-aft-03',
    hazard: 'FLOOD',
    phase: 'AFTER',
    category: 'DAMAGE_DOCUMENTATION',
    title: 'Capture Timestamped Geotagged Photographs for Calamity Relief Claims',
    instruction: 'Take clear photos and video of water-level tide marks on walls, collapsed structures, destroyed crops, and spoiled appliances before clearing debris.',
    priority: 'HIGH',
    reason: 'Revenue officers and insurance surveyors require verifiable photographic proof of high-water marks and loss inventory under State Disaster Response Fund (SDRF) norms.',
    source: 'Ministry of Home Affairs Calamity Compensation & SDRF Verification SOP',
    practical_steps: [
      'Photograph the high-water line on exterior and interior walls with a measuring tape or recognizable object for scale.',
      'Record serial numbers, brand plates, and purchase receipts of submerged pumps, refrigerators, and motor vehicles.',
      'Keep a written notebook of itemized destroyed goods, signed by local Ward Member or Sarpanch if possible.'
    ],
    warning_signs: [
      'Clean-up operations washing away high-water evidence before inspection.'
    ],
    what_not_to_do: [
      'Do not discard destroyed machinery or major assets until surveyed by official loss assessors.'
    ],
    vulnerable_groups: 'Ensure crop loss declarations for smallholder farmers list specific survey/khasra numbers.',
    checklist: [
      'High-water mark on walls photographed with scale.',
      'Damaged appliances, vehicles, and crops documented.',
      'Relief claim filed at local Tehsil / Taluk office.'
    ]
  },

  // =========================================================================
  // 2. CYCLONE
  // =========================================================================
  // --- CYCLONE: BEFORE ---
  {
    id: 'cyc-bef-01',
    hazard: 'CYCLONE',
    phase: 'BEFORE',
    category: 'STRUCTURAL_SAFETY',
    title: 'Secure Roof Sheets, Window Shutters & Exterior Overhangs',
    instruction: 'Fasten loose corrugated asbestos/tin roof sheets with galvanized U-bolts and batten straps; tape or board glass windows in a cross pattern.',
    priority: 'CRITICAL',
    reason: 'Gale-force cyclonic winds (>100 km/h) create aerodynamic low-pressure lift, ripping off unanchored tin roofs and turning loose glass into lethal high-speed projectiles.',
    source: 'NDMA National Disaster Management Guidelines: Management of Cyclones (Section 3.4)',
    warning: 'Never stand near large plate-glass windows during pre-cyclonic squalls.',
    related_cascading_risk: 'Structural roof blow-offs, building envelope breach, and flying debris fatalities.',
    practical_steps: [
      'Inspect roof sheet screws; reinforce rusted J-bolts with heavy wire ties or timber cross-battens.',
      'Tape window glass panes firmly with heavy adhesive tape in an X-pattern to prevent shattered fragments from scattering.',
      'Clear courtyards of loose plastic chairs, zinc sheets, corrugated pipes, and timber planks.'
    ],
    warning_signs: [
      'IMD issues Red Warning for Severe Cyclonic Storm landfall within 36 hours.',
      'Sudden drop in barometric pressure and high oceanic swell waves.'
    ],
    what_not_to_do: [
      'Do not wedge windows slightly open (this causes extreme internal pressurization that lifts the entire roof).'
    ],
    vulnerable_groups: 'Ensure families living in kutcha thatch huts evacuate to pucca concrete cyclone shelters immediately upon Orange Alert.',
    checklist: [
      'Loose roof sheets fastened with wire/straps.',
      'Windows taped or boarded.',
      'Loose yard items moved indoors.'
    ]
  },
  {
    id: 'cyc-bef-02',
    hazard: 'CYCLONE',
    phase: 'BEFORE',
    category: 'POWER_AND_LIGHTING',
    title: 'Fully Charge Phones, Power Banks & Emergency Lanterns',
    instruction: 'Charge all communication devices to 100%, charge secondary battery banks, and stock dry-cell LED lanterns before coastal grid isolation.',
    priority: 'HIGH',
    reason: 'Electricity distribution grids are preemptively shut down hours before landfall by state power corporations to prevent grid collapse and electrocution.',
    source: 'Central Electricity Authority / State DISCOM Cyclone Preparedness SOP',
    warning: 'Expect electricity power outages lasting 3 to 7 days following a severe cyclone landfall.',
    related_cascading_risk: 'Communication blackout, telemetry loss, and inability to call emergency services.',
    practical_steps: [
      'Charge all family mobile handsets, tablets, power banks, and rechargeable torches.',
      'Switch phones to battery-saver or airplane mode to conserve battery life during calm intervals.',
      'Stock spare AA/AAA dry-cell batteries for transistor radios to receive All India Radio storm bulletins.'
    ],
    warning_signs: [
      'DISCOM issues notification of scheduled coastal power shutdown.'
    ],
    what_not_to_do: [
      'Do not rely on candles as primary lighting (candles blow over in cyclonic drafts and cause catastrophic house fires).'
    ],
    vulnerable_groups: 'Pre-charge portable medical nebulizers and oxygen concentrators; arrange battery inverter backup.',
    checklist: [
      'Mobile phones and power banks at 100%.',
      'Battery-operated AM/FM radio tuned to AIR.',
      'LED torches and spare batteries staged.'
    ]
  },
  {
    id: 'cyc-bef-03',
    hazard: 'CYCLONE',
    phase: 'BEFORE',
    category: 'SAFE_ROUTES_EVACUATION',
    title: 'Evacuate Coastal Lowlands to Multi-Purpose Cyclone Shelters (MPCS)',
    instruction: 'If residing within 5 km of the coastline or in low-lying delta areas, move promptly to designated multi-purpose cyclone shelters upon official notice.',
    priority: 'CRITICAL',
    reason: 'Storm surges driven by cyclonic wind stress can elevate sea levels by 3 to 6 meters above astronomical tides, drowning coastal settlements within minutes.',
    source: 'National Cyclone Risk Mitigation Project (NCRMP) / NDMA Guidelines',
    warning: 'Storm surges travel at speeds exceeding 40 km/h; once surge water hits roads, foot evacuation becomes physically impossible.',
    related_cascading_risk: 'Coastal storm surge inundation, saltwater intrusion, and catastrophic village submersion.',
    practical_steps: [
      'Pack a compact emergency bag with 3 days of dry rations (chuda/gur/biscuits), water, IDs, and medications.',
      'Follow civil administration evacuation buses or walk to nearest elevated concrete cyclone shelter.',
      'Check in with shelter warden and register your family members for headcount.'
    ],
    warning_signs: [
      'IMD issues Storm Surge Warning indicating surge height >2 meters.',
      'Unusual ocean tide retreat exposing seabed followed by loud roaring breakers.'
    ],
    what_not_to_do: [
      'Do not stay back in kutcha huts to guard household property or cattle once evacuation orders are issued.'
    ],
    vulnerable_groups: 'Pregnant women in their third trimester should be shifted to district civil hospitals 48 hours before storm landfall.',
    checklist: [
      'Compact emergency bag packed.',
      'Follow designated route to Multi-Purpose Cyclone Shelter.',
      'Check in with shelter management committee.'
    ]
  },
  // --- CYCLONE: DURING ---
  {
    id: 'cyc-dur-01',
    hazard: 'CYCLONE',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'DO NOT Venture Outside During the False Calm of the "Eye"',
    instruction: 'If wind and rain suddenly stop completely, STAY INDOORS. You are in the eye of the cyclone; violent hurricane-force winds will resume abruptly from the reverse direction.',
    priority: 'CRITICAL',
    reason: 'The eye of a tropical cyclone is an area of deceptive calm (10-30 minutes). When the trailing eyewall hits, wind speeds instantaneously accelerate from 0 to over 150 km/h from the opposite direction.',
    source: 'IMD Cyclone Warning Dissemination Guidelines',
    warning: 'Dozens of cyclone fatalities occur when citizens step outside during the eye to inspect damage and are struck down by the violent eyewall reverse blast.',
    related_cascading_risk: 'Fatal blunt-force trauma from flying sheet metal, uprooted trees, and falling parapets.',
    practical_steps: [
      'Remain inside your shelter until local authorities or All India Radio confirm the cyclone has completely passed.',
      'Keep all doors and windows securely bolted on both sides of the building.',
      'Stay away from windows; take shelter in central hallway, bathroom, or under sturdy concrete lintels.'
    ],
    warning_signs: [
      'Sudden eerie silence, clearing sky, and calm winds following hours of extreme gale.',
      'Rapid barometric pressure dip.'
    ],
    what_not_to_do: [
      'Never step outside to inspect roof sheets or untie boats during the lull in winds.',
      'Do not open exterior doors to let pets out during the calm phase.'
    ],
    vulnerable_groups: 'Keep children close and engaged indoors to prevent them from slipping out open doors.',
    checklist: [
      'All family members remain indoors in central room.',
      'Windows and doors securely bolted.',
      'Listen to official radio broadcast confirming eyewall clearance.'
    ]
  },
  {
    id: 'cyc-dur-02',
    hazard: 'CYCLONE',
    phase: 'DURING',
    category: 'SHELTER',
    title: 'Shelter in Central Reinforced Rooms Away from External Glass & Tin',
    instruction: 'Gather all family members in an interior room with the fewest exterior walls (such as a ground-floor hallway or bathroom).',
    priority: 'CRITICAL',
    reason: 'Exterior walls and roof eaves receive the maximum aerodynamic pressure; interior load-bearing masonry partitions offer highest resistance against structural failure.',
    source: 'NDMA Cyclone Safety Manual',
    warning: 'Tin and corrugated asbestos roofs frequently shear off during Category 3+ cyclones, leaving upper floors exposed to torrential rains.',
    related_cascading_risk: 'Building envelope failure and blunt head trauma.',
    practical_steps: [
      'Sit on floor cushions under a sturdy wooden dining table or against an interior brick wall.',
      'Cover heads with mattresses or thick quilts to shield against flying plaster and glass shards.',
      'Keep your emergency flashlight and whistle in your pocket at all times.'
    ],
    warning_signs: [
      'Extreme whistling and howling sounds from door gaps.',
      'Vibration and bowing of exterior window glass panes.'
    ],
    what_not_to_do: [
      'Do not sleep on upper floors directly under tin or asbestos sheet roofing.'
    ],
    vulnerable_groups: 'Position elderly and bedridden persons on ground floor interior mattresses away from external walls.',
    checklist: [
      'Family situated in central interior hallway.',
      'Mattresses and pillows used for head protection.',
      'Emergency kit kept within arm\'s reach.'
    ]
  },
  // --- CYCLONE: AFTER ---
  {
    id: 'cyc-aft-01',
    hazard: 'CYCLONE',
    phase: 'AFTER',
    category: 'UTILITY_SAFETY',
    title: 'Beware of Fallen 11kV/33kV Power Lines & Submerged Electrical Conductors',
    instruction: 'Treat every dangling or fallen wire as energized and lethal. Maintain a minimum safe clearance distance of at least 10 meters (33 feet).',
    priority: 'CRITICAL',
    reason: 'Snapping cyclone winds pull down high-voltage distribution lines. Puddles and wet soil conduct lethal voltage over wide radius, causing instantaneous electrocution.',
    source: 'Central Electricity Authority / State Power Distribution Corporation Guidelines',
    warning: 'Never attempt to move a fallen tree or branch that is in contact with an electric cable, even if you believe power is off.',
    related_cascading_risk: 'Lethal electrocution, ground fault arcing, and municipal grid fire hazards.',
    practical_steps: [
      'Report downed lines immediately to DISCOM control room or dial 112.',
      'Warn neighbors and post makeshift warning sticks/caution tape around the puddle/wire area.',
      'If your car contacts a downed line while driving, stay inside the vehicle until rescue crews arrive.'
    ],
    warning_signs: [
      'Sparks, buzzing sounds, or smoking asphalt around a fallen wire.',
      'Dangling wires hanging near metal fences or waterlogged puddles.'
    ],
    what_not_to_do: [
      'Never drive or walk through puddles containing submerged wires.',
      'Do not use metal poles or wet wooden sticks to prod fallen lines.'
    ],
    vulnerable_groups: 'Children playing outdoors post-cyclone are at highest risk; supervise them strictly indoors until street clearance is confirmed.',
    checklist: [
      'Keep minimum 10m distance from fallen power cables.',
      'Report snapped transmission cables to local power authority.',
      'Keep children indoors until neighborhood wires are inspected.'
    ]
  },
  {
    id: 'cyc-aft-02',
    hazard: 'CYCLONE',
    phase: 'AFTER',
    category: 'WATER_AND_FOOD',
    title: 'Boil All Drinking Water & Disinfect Storage Tanks from Saline Storm Ingress',
    instruction: 'Bring all drinking water to a rolling boil for a full 2 to 3 minutes before consumption; test overhead tanks for saltwater contamination.',
    priority: 'HIGH',
    reason: 'Cyclonic storm surges and floodwaters inundate municipal underground reservoirs, carrying saline water, sewage, and decomposing organic debris into drinking supplies.',
    source: 'National Centre for Disease Control (NCDC) Guidelines',
    warning: 'Drinking saline or contaminated floodwater triggers rapid dehydration and severe bacterial gastroenteritis.',
    related_cascading_risk: 'Diarrheal outbreaks, dehydration, and long-term groundwater salinization.',
    practical_steps: [
      'Inspect underground water sumps for surface floodwater ingress; pump out and chlorinate if contaminated.',
      'Use 2 drops of chlorine solution or 1 chlorachek tablet per liter if boiling fuel is scarce.',
      'Eat only freshly cooked hot meals; discard open food packages that came into contact with storm surge.'
    ],
    warning_signs: [
      'Water tastes salty or has an earthy, brackish smell.'
    ],
    what_not_to_do: [
      'Do not consume food items from refrigerators that have been without power for more than 24 hours.'
    ],
    vulnerable_groups: 'Prepare ORS solution using boiled water for infants and elders recovering from storm stress.',
    checklist: [
      'Boil all drinking water for minimum 2-3 minutes.',
      'Inspect water sumps for saltwater ingress.',
      'Discard spoiled perishable foods.'
    ]
  },

  // =========================================================================
  // 3. HEATWAVE
  // =========================================================================
  // --- HEATWAVE: BEFORE ---
  {
    id: 'htw-bef-01',
    hazard: 'HEATWAVE',
    phase: 'BEFORE',
    category: 'WATER_AND_FOOD',
    title: 'Stock Oral Rehydration Salts (ORS) & Traditional Cooling Electrolytes',
    instruction: 'Stock adequate packets of WHO-formula ORS, raw mangoes (panna), lemons, coconut water, and unrefined salt at home before peak heat season.',
    priority: 'HIGH',
    reason: 'Extreme ambient heat causes profuse sweating, depleting sodium, potassium, and chloride ions faster than water replenishment alone can replace.',
    source: 'NDMA National Guidelines for Preparation of Action Plan - Prevention and Management of Heat Wave',
    warning: 'Plain water alone cannot prevent heat cramps or heat exhaustion when heavy electrolyte loss occurs.',
    related_cascading_risk: 'Electrolyte imbalance, hypovolemic shock, and heatstroke-induced acute kidney injury.',
    practical_steps: [
      'Dissolve one packet of standard WHO-ORS in 1 liter of clean drinking water.',
      'Prepare traditional remedies: boiled raw mango drink (aam panna), barley water, or buttermilk (chaas) with roasted cumin and salt.',
      'Keep traditional clay water pots (matkas) filled; evaporative clay cooling provides palatable cool water without electricity.'
    ],
    warning_signs: [
      'IMD issues Yellow/Orange Heatwave Alert with maximum temperatures exceeding 42°C in plains or 30°C in hills.',
      'Night-time minimum temperatures remaining above 30°C (warm nights increase cumulative physiological heat stress).'
    ],
    what_not_to_do: [
      'Do not consume high-sugar carbonated sodas or alcohol (they act as diuretics and accelerate dehydration).'
    ],
    vulnerable_groups: 'Older adults often lose their physiological thirst sensation; schedule hydration every 30 minutes regardless of thirst.',
    checklist: [
      'Stock 10 packets of WHO-ORS.',
      'Matkas (clay pots) cleaned and filled with clean water.',
      'Hydration schedule established for family elders.'
    ]
  },
  {
    id: 'htw-bef-02',
    hazard: 'HEATWAVE',
    phase: 'BEFORE',
    category: 'PROPERTY_PREPARATION',
    title: 'Block Direct Solar Radiation with Window Shades & Reflective Coatings',
    instruction: 'Hang dark curtains, bamboo reed blinds (khas), or reflective aluminum foil on south and west-facing windows; apply white lime wash to flat roofs.',
    priority: 'HIGH',
    reason: 'Solar radiation entering through unshaded glass and uninsulated concrete roof slabs creates intense indoor greenhouse heat trapping that persists throughout the night.',
    source: 'Ministry of Housing and Urban Affairs / Thermal Comfort Guidelines',
    related_cascading_risk: 'Urban heat island escalation and nocturnal physiological heat strain.',
    practical_steps: [
      'Install external bamboo blinds (chick/khas) and sprinkle them with water during hot afternoons for natural evaporative cooling.',
      'Apply high-albedo solar reflective white coating or slaked lime (chuna) to flat concrete roofs (reduces roof surface temp by 10-15°C).',
      'Keep windows closed during peak day hours (10 AM to 5 PM) and open them during cooler night hours to flush heat.'
    ],
    warning_signs: [
      'Indoor room temperature exceeding 35°C even with ceiling fans running.'
    ],
    what_not_to_do: [
      'Do not leave west-facing curtains open during afternoon peak solar hours.'
    ],
    vulnerable_groups: 'Shift elders and infants to ground floor or north-facing rooms away from uninsulated roof slabs.',
    checklist: [
      'South/west windows shaded with dark curtains or bamboo blinds.',
      'White reflective wash applied to roof terrace.',
      'Cross-ventilation planned for night hours.'
    ]
  },
  // --- HEATWAVE: DURING ---
  {
    id: 'htw-dur-01',
    hazard: 'HEATWAVE',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Avoid Direct Sun Exposure & Strenuous Physical Exertion (12 PM - 4 PM)',
    instruction: 'Stay indoors in shaded, ventilated rooms between 12:00 PM and 4:00 PM; reschedule heavy manual labor, sports, and outdoor errands to early morning.',
    priority: 'CRITICAL',
    reason: 'Peak solar zenith produces maximum ultraviolet irradiance and ambient temperatures, rapidly overloading the body\'s thermoregulatory cooling mechanism.',
    source: 'NDMA Heatwave Public Health Advisory / IMD Guidelines',
    warning: 'Exertional heatstroke can occur in less than 30 minutes of strenuous outdoor work under severe heatwave conditions.',
    related_cascading_risk: 'Exertional heatstroke, hyperthermia, and emergency hospital admissions.',
    practical_steps: [
      'Schedule agricultural harvesting or construction labor between 5:30 AM - 10:30 AM and after 5:00 PM.',
      'If outdoor travel is mandatory, wear loose-fitting, light-colored cotton clothing and cover head with a damp gamcha, towel, or umbrella.',
      'Carry a minimum 2-liter water bottle and sip frequently.'
    ],
    warning_signs: [
      'Dizziness, lightheadedness, throbbing headache, muscle cramps in calves, and excessive fatigue.'
    ],
    what_not_to_do: [
      'NEVER leave children, elders, or pets inside a parked vehicle, even for 5 minutes with windows cracked (cabin temperature can reach 60°C within 10 minutes).',
      'Do not engage in high-intensity gym workouts in non-air-conditioned spaces during peak afternoon.'
    ],
    vulnerable_groups: 'Outdoor gig-workers, delivery riders, and traffic police must take mandatory 15-minute breaks in shaded Cool Centers every hour.',
    checklist: [
      'Outdoor tasks rescheduled away from 12 PM - 4 PM window.',
      'Head covered with damp cotton cloth or wide-brimmed hat.',
      'Minimum 2L water flask carried when traveling.'
    ]
  },
  {
    id: 'htw-dur-02',
    hazard: 'HEATWAVE',
    phase: 'DURING',
    category: 'MEDICAL_AND_HEALTH',
    title: 'Recognize Heatstroke Red Flags & Initiate Immediate Emergency Cooling',
    instruction: 'Recognize the life-threatening triad: High body temperature (>40°C / 104°F), altered mental state/confusion, and hot dry or profusely sweating skin. Call 108 immediately!',
    priority: 'CRITICAL',
    reason: 'Heatstroke is a medical emergency with up to 50% mortality if core body temperature is not actively reduced within 30 minutes of onset.',
    source: 'National Disaster Management Authority (NDMA) Standard Operating Procedure for Heatstroke',
    warning: 'Do NOT give oral fluids to an unconscious or delirious patient (risk of lung aspiration and choking).',
    related_cascading_risk: 'Multi-organ failure, rhabdomyolysis, and cerebral edema.',
    practical_steps: [
      'Dial 108 for emergency ambulance immediately.',
      'Move patient to cool shade or air-conditioned room; remove excess tight clothing.',
      'Apply ice packs or cold wet towels to major arterial blood vessel areas: neck, armpits, and groin.',
      'Fan the patient vigorously while misting skin with cool water to facilitate rapid evaporative heat transfer.'
    ],
    warning_signs: [
      'Confusion, slurred speech, delirium, seizures, loss of consciousness, rapid shallow breathing, vomiting.'
    ],
    what_not_to_do: [
      'Do NOT administer antipyretics like paracetamol or aspirin (they do not work for environmental heat hyperthermia and increase liver/kidney strain).'
    ],
    vulnerable_groups: 'Bedridden elders and patients taking anticholinergics or diuretics are at extreme risk of silent non-exertional heatstroke.',
    checklist: [
      'Dial 108 immediately upon recognizing altered mental state.',
      'Apply cold compresses to neck, armpits, and groin.',
      'Fan patient vigorously with misted water.'
    ]
  },
  // --- HEATWAVE: AFTER ---
  {
    id: 'htw-aft-01',
    hazard: 'HEATWAVE',
    phase: 'AFTER',
    category: 'RECOVERY_AND_HEALTH',
    title: 'Gradual Post-Heat Rehydration & Monitored Electrolyte Recovery',
    instruction: 'Continue gradual rehydration with balanced fluids for 48 hours after heatwave subsides; monitor urine output and color (should be pale straw-colored).',
    priority: 'HIGH',
    reason: 'Subclinical cellular dehydration and renal micro-injury can persist for days after ambient temperatures moderate, triggering delayed acute tubular necrosis.',
    source: 'Indian Council of Medical Research (ICMR) Occupational Heat Stress Guidelines',
    practical_steps: [
      'Sip fluids slowly throughout the day; avoid chugging massive volumes of ice water at once (can trigger stomach cramps).',
      'Consume seasonal hydrating fruits: watermelon, musk melon, cucumber, oranges, and gourds.',
      'Monitor elderly family members for delayed confusion or muscle weakness.'
    ],
    warning_signs: [
      'Dark amber or brown urine (indicates concentrated urine or muscle protein breakdown / rhabdomyolysis).',
      'Persistent nausea or inability to retain fluids.'
    ],
    what_not_to_do: [
      'Do not abruptly resume heavy athletic training immediately after a severe heat exhaustion episode.'
    ],
    vulnerable_groups: 'Hypertensive and cardiac patients should consult their physician before resuming full diuretic dosages if fluid intake was restricted.',
    checklist: [
      'Fluid intake maintained at 3-4 liters daily.',
      'Hydrating fruits included in family diet.',
      'Urine color monitored for pale straw clarity.'
    ]
  },

  // =========================================================================
  // 4. SEVERE WEATHER (Thunderstorms, Squalls, Lightning, Hail)
  // =========================================================================
  // --- SEVERE WEATHER: BEFORE ---
  {
    id: 'swx-bef-01',
    hazard: 'SEVERE_WEATHER',
    phase: 'BEFORE',
    category: 'PROPERTY_PREPARATION',
    title: 'Inspect Overhanging Tree Boughs & Secure Outdoor Fixtures',
    instruction: 'Trim dead or rotting tree limbs overhanging your house or electrical service wires; secure satellite dishes, tin shades, and outdoor metal furniture.',
    priority: 'HIGH',
    reason: 'Convective storm microbursts and gust fronts produce sudden straight-line winds (>80 km/h) that snap compromised tree boughs, crushing roofs and severing lines.',
    source: 'CPWD Maintenance Manual / NDMA Severe Convective Storm Advisory',
    warning: 'Do not attempt tree trimming near power lines yourself; request municipal or power distribution authority assistance.',
    related_cascading_risk: 'Localized structural damage, fallen wire electrocutions, and road blockages.',
    practical_steps: [
      'Inspect roof terrace for unanchored water tanks, loose flowerpots, or building materials; move them indoors.',
      'Secure iron gates, window shutters, and corrugated car-shed tin sheets with strong locking latches.',
      'Unplug sensitive electronics (smart TVs, desktop computers, Wi-Fi routers) before storm line arrives.'
    ],
    warning_signs: [
      'IMD Nowcast radar bulletin warns of approaching squall line with wind gusts >60 km/h within 3 hours.',
      'Towering cumulonimbus anvil clouds darkening the western/northwestern horizon.'
    ],
    what_not_to_do: [
      'Do not leave vehicles parked directly underneath large eucalyptus, gulmohar, or ancient banyan trees during squalls.'
    ],
    vulnerable_groups: 'Ensure pets are brought inside the house well before thunder begins to prevent panicked bolting.',
    checklist: [
      'Overhanging dead branches cleared.',
      'Rooftop items and furniture moved indoors.',
      'Electronics unplugged from wall outlets.'
    ]
  },
  // --- SEVERE WEATHER: DURING ---
  {
    id: 'swx-dur-01',
    hazard: 'SEVERE_WEATHER',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Obey the 30-30 Lightning Rule: Never Shelter Under Tall Isolated Trees',
    instruction: 'When thunder roars, go indoors! If delay between lightning flash and thunder is under 30 seconds, you are in immediate strike range. Never shelter under tall trees!',
    priority: 'CRITICAL',
    reason: 'Tall isolated trees are natural lightning conductors. When struck, lethal side-flash and ground current radiate outward across ground surface, causing 80% of rural lightning deaths in India.',
    source: 'NDMA National Guidelines on Lightning / Lightning Resilient India Campaign (CROPC)',
    warning: 'Tents, open tin sheds, bus shelters, and tractors offer ZERO protection against lightning strikes.',
    related_cascading_risk: 'Instantaneous cardiac arrest, severe thermal burns, and ground current mass casualties.',
    practical_steps: [
      'Seek shelter inside a substantial enclosed building with plumbing/wiring (acts as a Faraday cage) or an all-metal enclosed vehicle.',
      'If trapped in open terrain with no shelter, assume the Lightning Safety Crouch: squat low on the balls of your feet, tuck head between knees, cover ears, minimize ground contact.',
      'Stay away from wire fences, railway tracks, metal pipes, and water bodies (ponds, irrigation channels).'
    ],
    warning_signs: [
      'Hair standing on end or skin tingling (indicates an electrostatic charge build-up; lightning strike is imminent within seconds!).',
      'Crackling sounds on car radio or metallic smell in the air.'
    ],
    what_not_to_do: [
      'DO NOT lie flat on the ground (this maximizes your contact area with lethal ground currents radiating through soil).',
      'Do not hold metal umbrellas, cricket bats, golf clubs, or fishing rods during an active thunderstorm.'
    ],
    vulnerable_groups: 'Farm laborers working in open paddy fields must immediately disperse and squat individually; do not huddle in groups.',
    checklist: [
      'Retreat indoors inside pucca concrete building.',
      'Maintain 30-minute stay inside after last heard thunderclap.',
      'Adopt Lightning Crouch if caught in open.'
    ]
  },
  {
    id: 'swx-dur-02',
    hazard: 'SEVERE_WEATHER',
    phase: 'DURING',
    category: 'UTILITY_SAFETY',
    title: 'Avoid Wired Landline Phones, Plumbing Fixtures & Electrical Sockets',
    instruction: 'Do not use corded landline telephones, avoid taking showers or washing dishes, and stay away from metal window frames during active lightning storms.',
    priority: 'HIGH',
    reason: 'Lightning strikes on utility poles or ground water tables travel through conductive metal plumbing pipes and copper telephone wires straight into homes.',
    source: 'Indian Standards Institute (IS/IEC 62305: Protection Against Lightning)',
    practical_steps: [
      'Use mobile phones or cordless phones instead of corded landlines.',
      'Postpone baths, showers, and laundry until the thunderstorm has moved at least 15 km away.',
      'Keep closed metal windows and balcony glass doors untouched.'
    ],
    warning_signs: [
      'Frequent cloud-to-ground lightning flashes within 5 km of home.'
    ],
    what_not_to_do: [
      'Do not stand near kitchen sinks, bathtubs, or metal bathroom faucets during lightning.'
    ],
    vulnerable_groups: 'Ensure infants in metallic cribs are moved away from exterior walls and metal window grilles.',
    checklist: [
      'Avoid plumbing and corded phones during active lightning.',
      'Stay at least 1 meter away from exterior windows and electrical outlets.'
    ]
  },
  // --- SEVERE WEATHER: AFTER ---
  {
    id: 'swx-aft-01',
    hazard: 'SEVERE_WEATHER',
    phase: 'AFTER',
    category: 'MEDICAL_AND_HEALTH',
    title: 'Provide Immediate CPR to Lightning Victims — They Carry NO Charge!',
    instruction: 'If a person is struck by lightning, render immediate first aid and chest compressions (CPR). Lightning victims carry ZERO residual electrical charge and are completely safe to touch.',
    priority: 'CRITICAL',
    reason: 'Lightning causes instantaneous cardiopulmonary arrest due to cardiac depolarisation. Immediate bystander CPR within 4 minutes can achieve survival rates over 70%.',
    source: 'Red Cross / NDMA Emergency First Aid Protocol for Lightning Casualties',
    warning: 'Never delay CPR out of fear of electric shock; the electrical charge dissipates instantly into the ground.',
    related_cascading_risk: 'Hypoxic brain death due to bystander delay in initiating chest compressions.',
    practical_steps: [
      'Check responsiveness and breathing; if victim is unresponsive and not breathing, call 108 immediately.',
      'Place victim on back on dry surface; place heel of hand on center of chest and deliver hard, fast compressions (100-120 per minute).',
      'Check for thermal burns around jewelry, belts, and zippers; apply clean dry dressing once breathing resumes.'
    ],
    warning_signs: [
      'Victim collapsed, unresponsive, with singed hair or feathering fern-like marks (Lichtenberg figures) on skin.'
    ],
    what_not_to_do: [
      'Do not bury the victim in cow dung or mud (a fatal traditional rural misconception that causes asphyxiation and severe bacterial sepsis).'
    ],
    vulnerable_groups: 'Check for temporary ruptured eardrums and severe confusion in nearby bystanders who survived the blast radius.',
    checklist: [
      'Verify area is safe from secondary lightning strikes.',
      'Call 108 ambulance immediately.',
      'Deliver continuous chest compressions until medical help arrives.'
    ]
  },

  // =========================================================================
  // 5. LANDSLIDE
  // =========================================================================
  // --- LANDSLIDE: BEFORE ---
  {
    id: 'lsd-bef-01',
    hazard: 'LANDSLIDE',
    phase: 'BEFORE',
    category: 'STRUCTURAL_SAFETY',
    title: 'Monitor Slopes for Ground Cracks, Leaning Trees & Sticking Doors',
    instruction: 'Regularly inspect hill slopes behind your home for tension fissures, new springs or seeps, leaning retaining walls, and tilted utility poles.',
    priority: 'CRITICAL',
    reason: 'Progressive slope failure begins with microscopic shear deformation, causing tell-tale ground cracking and building frame warping days before catastrophic mass release.',
    source: 'Geological Survey of India (GSI) / NDMA Landslide Risk Management Guidelines',
    warning: 'Any new ground crack on a slope steeper than 25° during monsoon indicates active shear displacement; evacuate immediately.',
    related_cascading_risk: 'Catastrophic debris flow, slope detachment, and sudden structural burial.',
    practical_steps: [
      'Walk the slope perimeter behind residential quarters before and during monsoon breaks.',
      'Check masonry retaining walls for bulging, displaced weep holes, or tilting.',
      'Ensure hill slope surface drains (jhoras) are free of garbage, plastic, and boulder debris.'
    ],
    warning_signs: [
      'Doors or windows suddenly sticking or jamming in their frames for the first time.',
      'New cracks appearing in plaster, tile floors, or retaining wall masonry.',
      'Sudden appearance of muddy water bubbling out of slope faces where drainage was dry.'
    ],
    what_not_to_do: [
      'Never cut the toe of a steep slope to create car parking or building extension without engineered retaining reinforcement.'
    ],
    vulnerable_groups: 'Families living in temporary roadside settlements or kutcha shacks below cut slopes must relocate during Orange Alert rainfall.',
    checklist: [
      'Slope inspected for fresh tension cracks.',
      'Weep holes in retaining walls cleared of silt.',
      'Report widening cracks to local District Disaster Management Officer.'
    ]
  },
  {
    id: 'lsd-bef-02',
    hazard: 'LANDSLIDE',
    phase: 'BEFORE',
    category: 'SAFE_ROUTES_EVACUATION',
    title: 'Identify Safe Valley Centers Away from Old Debris Cones & Gully Channels',
    instruction: 'Map evacuation paths to wide valley floors or broad flat ridges far away from historic scree chutes, steep gully channels, and stream banks.',
    priority: 'CRITICAL',
    reason: 'Debris flows follow existing drainage gullies like high-speed freight trains (30-50 km/h), jumping stream bends and burying everything within 100 meters of channel banks.',
    source: 'NDMA Standard Operating Procedure for Landslide Preparedness',
    practical_steps: [
      'Locate designated government relief camps established in wide valley clearings or stable bedrock plateaus.',
      'Ensure evacuation path does not cross steep scree slopes prone to rockfall.',
      'Keep vehicles parked facing downstream on safe reinforced highway stretches.'
    ],
    warning_signs: [
      'Continuous rainfall exceeding 100 mm in 24 hours in mountainous districts (Kerala Western Ghats, Uttarakhand, Himachal, Sikkim).'
    ],
    what_not_to_do: [
      'Do not shelter in tents or buildings located directly at the mouth of an alluvial drainage fan or mountain gorge.'
    ],
    vulnerable_groups: 'Elderly and mobility-impaired residents must be evacuated in daylight hours before mountain road links are compromised.',
    checklist: [
      'Evacuation destination located on stable bedrock plateau.',
      'Emergency grab-bag with torch and sturdy trekking boots staged.',
      'Local emergency control room number (1077 / 112) noted.'
    ]
  },
  // --- LANDSLIDE: DURING ---
  {
    id: 'lsd-dur-01',
    hazard: 'LANDSLIDE',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Evacuate Horizontally Out of Channel Path Upon Hearing Roaring Sounds',
    instruction: 'If you hear a low rumbling sound (like a freight train), snapping trees, or see sudden muddy torrents, RUN LATERALLY away from the gully path immediately!',
    priority: 'CRITICAL',
    reason: 'A debris flow moves faster than a sprinting human down a slope. Evacuating sideways (laterally) across the slope takes you out of the direct velocity path.',
    source: 'GSI Landslide Early Warning System Citizen Action Guide',
    warning: 'Never run straight downhill ahead of a landslide; debris flows gain speed as they descend and will overtake you.',
    related_cascading_risk: 'Burial under fluidized mud and boulder slurry traveling at 40 km/h.',
    practical_steps: [
      'Alert family with loud shout or whistle and move laterally (horizontally) away from the stream or gully channel.',
      'Climb to highest solid ground available out of the channel trench.',
      'If escape is physically impossible, curl into a tight fetal ball and shield your head and neck with arms, pillows, or heavy blankets.'
    ],
    warning_signs: [
      'Loud rumbling or roaring noise resembling an approaching freight train or low aircraft.',
      'Sounds of trees snapping or boulders grinding together underground.',
      'Sudden drop or complete drying up of river flow (indicates upstream damming that may burst!).'
    ],
    what_not_to_do: [
      'Do not attempt to salvage cattle or heavy possessions when rumbling is heard.',
      'Never drive across a mountain road where small stones and pebbles are actively tumbling down the hillside.'
    ],
    vulnerable_groups: 'Carry infants securely against your chest with both arms free for balance; assist elders to walk perpendicular to slope flow.',
    checklist: [
      'Run sideways (laterally) away from the gully or stream path.',
      'Move to higher elevated solid bedrock.',
      'Protect head and neck if caught.'
    ]
  },
  // --- LANDSLIDE: AFTER ---
  {
    id: 'lsd-aft-01',
    hazard: 'LANDSLIDE',
    phase: 'AFTER',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Stay Completely Clear of the Landslide Area — Beware Secondary Failures',
    instruction: 'Do not venture onto or below a fresh landslide scar. Saturated regolith and unbuttressed headwalls frequently collapse hours or days later.',
    priority: 'CRITICAL',
    reason: 'Initial slope movement leaves oversteepened, unsupported vertical headscarps and saturated debris toes that experience fatal secondary slope failures without warning.',
    source: 'NDMA Landslide Post-Disaster Operations Guidelines',
    warning: 'Rescue volunteers often become casualties by rushing onto unstable active slide zones before geotechnical stabilization.',
    related_cascading_risk: 'Secondary landslide triggers, burial of rescue teams, and delayed rockfalls.',
    practical_steps: [
      'Wait for SDRF/NDRF search and rescue teams equipped with specialized sniffer dogs and thermal imaging gear.',
      'Observe river channels below the landslide: report any sudden impoundment (natural landslide dam) to district authorities immediately.',
      'Check for injured or trapped neighbors around the periphery without entering the unstable slide mass.'
    ],
    warning_signs: [
      'Trickling soil, falling pebbles, or widening cracks at the top rim of the landslide scarp.'
    ],
    what_not_to_do: [
      'Do not allow crowds or onlookers to gather near the edge of a landslide scarp or bridge approach.'
    ],
    vulnerable_groups: 'Keep children far away from steep muddy slide edges and flooded riverbanks.',
    checklist: [
      'Maintain 200m safe perimeter from active slide zone.',
      'Report trapped persons and upstream river damming to authorities.',
      'Await official clearance from district administration before returning.'
    ]
  },

  // =========================================================================
  // 6. EARTHQUAKE
  // =========================================================================
  // --- EARTHQUAKE: BEFORE ---
  {
    id: 'eqk-bef-01',
    hazard: 'EARTHQUAKE',
    phase: 'BEFORE',
    category: 'STRUCTURAL_SAFETY',
    title: 'Fasten Tall Furniture, Heavy Appliances & Geysers to Wall Studs',
    instruction: 'Secure bookcases, almirahs, refrigerators, water heaters (geysers), and heavy wall mirrors to structural masonry walls using metal L-brackets.',
    priority: 'HIGH',
    reason: 'Over 60% of earthquake injuries in reinforced concrete buildings are caused by toppling heavy furniture, flying glass, and falling ceiling plaster rather than building collapse.',
    source: 'NDMA National Disaster Management Guidelines: Management of Earthquakes (Section 4.5)',
    practical_steps: [
      'Fasten heavy steel almirahs and wooden bookcases to walls with 2-inch steel anchor bolts.',
      'Place heavy, breakable items on lower shelves; install child-proof latches on upper kitchen cabinets.',
      'Ensure overhead water tanks (sintex) are firmly anchored to rooftop reinforced concrete columns.'
    ],
    warning_signs: [
      'Living in Seismic Zone IV or V (Himalayan belt, Northeast, Kutch, NCR Delhi) with unreinforced masonry structures.'
    ],
    what_not_to_do: [
      'Do not hang heavy mirrors, glass picture frames, or chandeliers directly over beds or sofas.'
    ],
    vulnerable_groups: 'Ensure pathways to exits for elderly and wheelchair users are completely clear of tall unbolted bookshelves.',
    checklist: [
      'Almirahs and bookcases anchored with L-brackets.',
      'Heavy items moved to lower shelves.',
      'Overhead water tank secured to rooftop column.'
    ]
  },
  {
    id: 'eqk-bef-02',
    hazard: 'EARTHQUAKE',
    phase: 'BEFORE',
    category: 'EMERGENCY_KIT',
    title: 'Prepare Under-Bed Earthquake Grab-Kit with Whistle & Heavy Shoes',
    instruction: 'Keep an emergency go-bag under or beside your bed containing a loud whistle, N95 dust mask, heavy leather-soled shoes, torch, and work gloves.',
    priority: 'HIGH',
    reason: 'Earthquakes striking at night leave survivors in pitch darkness surrounded by shattered glass and masonry rubble. Shoes protect feet and whistles signal search teams.',
    source: 'NDRF Earthquake Preparedness Handbook',
    practical_steps: [
      'Place heavy shoes and torch inside a tied canvas bag strapped to bed leg so it does not slide away during violent shaking.',
      'Include a bottle of water, essential daily pills, and a copy of identification papers in the pouch.',
      'Practice reaching for the bag blindly in the dark during family earthquake drills.'
    ],
    warning_signs: [
      'Structural non-prediction invariant: Earthquakes cannot be predicted. Preparedness must be permanent and continuous.'
    ],
    what_not_to_do: [
      'Do not store emergency kits in locked high cabinets that may jam during shaking.'
    ],
    vulnerable_groups: 'Keep extra pair of prescription spectacles and hearing aid batteries in the bedside kit.',
    checklist: [
      'Bedside bag contains heavy-soled shoes and flashlight.',
      'Loud emergency whistle attached to bag zipper.',
      'N95 dust mask packed to prevent concrete particulate inhalation.'
    ]
  },
  // --- EARTHQUAKE: DURING ---
  {
    id: 'eqk-dur-01',
    hazard: 'EARTHQUAKE',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'DROP, COVER, and HOLD ON! Never Run Outside During Active Shaking',
    instruction: 'DROP to your hands and knees, COVER your head and neck under a sturdy timber table or desk, and HOLD ON until shaking completely stops. Do NOT run outdoors!',
    priority: 'CRITICAL',
    reason: 'Running outside during violent shaking is the leading cause of earthquake death in urban areas. Shaking ground makes walking impossible, while falling brick parapets, window glass, and facade tiles rain down on street exits.',
    source: 'NDMA Standard Operating Procedure for Earthquake Life-Safety',
    warning: 'Never use elevators or rush toward crowded stairwells during tremors; stairs may buckle or jam doors.',
    related_cascading_risk: 'Blunt head trauma from falling exterior masonry and stairwell crush stampedes.',
    practical_steps: [
      'DROP down onto hands and knees before the violent shaking knocks you over.',
      'COVER head and neck with one arm; crawl under a sturdy dining table or desk for overhead protection.',
      'HOLD ON to your shelter with one hand; move with it if it shifts across the floor.',
      'If no table is nearby, drop against an interior load-bearing wall away from windows; shield head with both hands.'
    ],
    warning_signs: [
      'Sudden low-frequency rumbling followed by sharp vertical jolt (P-wave) and violent horizontal swaying (S-wave).'
    ],
    what_not_to_do: [
      'DO NOT run outside while building is actively shaking.',
      'DO NOT stand under doorways in modern construction (modern doorways are no stronger than the rest of the house and doors can slam shut on hands).',
      'Do not jump from balconies or first-floor windows.'
    ],
    vulnerable_groups: 'Persons using wheelchairs should lock wheels, cover head with a pillow or lap blanket, and shield neck until shaking stops.',
    checklist: [
      'DROP to hands and knees immediately.',
      'COVER head and neck under sturdy table.',
      'HOLD ON to table leg until shaking completely stops.'
    ]
  },
  {
    id: 'eqk-dur-02',
    hazard: 'EARTHQUAKE',
    phase: 'DURING',
    category: 'SHELTER',
    title: 'Actions if Outdoors or Driving When Shaking Begins',
    instruction: 'If outdoors, move into an open area away from high-rise buildings, utility poles, and flyovers. If driving, pull over safely to shoulder and set parking brake.',
    priority: 'HIGH',
    reason: 'Overhead glass curtain walls, neon signboards, high-voltage transformers, and masonry parapets fall into streets during seismic resonance.',
    source: 'National Disaster Management Authority Guidelines',
    practical_steps: [
      'Move to open parks, wide school grounds, or sports plazas.',
      'If in vehicle, stop clear of overpasses, bridges, and overhead utility cables; stay inside vehicle until shaking ceases.',
      'When driving resumes, watch for pavement cracks, road bumps, and bridge approach displacement.'
    ],
    warning_signs: [
      'Vehicles swaying violently as if four tires are suddenly punctured.'
    ],
    what_not_to_do: [
      'Do not stop car underneath highway flyovers, pedestrian overbridges, or next to steep hillsides.'
    ],
    vulnerable_groups: 'Instruct school children in outdoor playgrounds to sit down on open ground away from boundary walls.',
    checklist: [
      'Move to open plaza away from glass facades and utility poles.',
      'Pull car to road shoulder away from overhead flyovers.',
      'Remain inside parked car until shaking ceases.'
    ]
  },
  // --- EARTHQUAKE: AFTER ---
  {
    id: 'eqk-aft-01',
    hazard: 'EARTHQUAKE',
    phase: 'AFTER',
    category: 'UTILITY_SAFETY',
    title: 'Sniff for Gas Leaks Before Using Switches, Matches, or Lighters',
    instruction: 'Smell for LPG gas. If suspected, open windows, evacuate immediately, and do NOT flip electrical switches, light matches, or ring doorbells.',
    priority: 'CRITICAL',
    reason: 'Ruptured domestic LPG cylinder tubing and severed municipal gas lines create explosive air-gas mixtures; a single spark from an electrical light switch can detonate the entire building.',
    source: 'NDMA Post-Earthquake Life-Safety and Fire Prevention Protocol',
    warning: 'Secondary fires caused by fractured gas lines and shorted electrical circuits historically destroy more property than initial shaking.',
    related_cascading_risk: 'Secondary residential firestorms, gas explosions, and municipal water main failures.',
    practical_steps: [
      'Use flashlight or phone torch only; never strike matches or light candles.',
      'If you smell gas, shut off cylinder regulator, leave doors open, and evacuate everyone into open street.',
      'Shut off main electrical breaker only if you can do so safely without standing in water.'
    ],
    warning_signs: [
      'Hissing sounds near kitchen cylinders or strong smell of gas (rotten egg odor).'
    ],
    what_not_to_do: [
      'Do not turn on electrical switches, ceiling fans, or appliances if gas odor is present.'
    ],
    vulnerable_groups: 'Guide children and elderly outside immediately; put heavy footwear on them to prevent foot lacerations from shattered glass.',
    checklist: [
      'Check for gas odor without striking open flames.',
      'Evacuate building via stairs wearing sturdy footwear.',
      'Assemble in open area clear of building perimeter.'
    ]
  },
  {
    id: 'eqk-aft-02',
    hazard: 'EARTHQUAKE',
    phase: 'AFTER',
    category: 'STRUCTURAL_SAFETY',
    title: 'Expect Unpredictable Aftershocks — Stay Out of Compromised Buildings',
    instruction: 'Expect physical aftershocks over following hours and weeks. Do NOT re-enter damaged or visibly cracked buildings until cleared by structural engineers.',
    priority: 'CRITICAL',
    reason: 'Aftershocks are physical ground adjustments along fault lines. Buildings whose structural load-bearing columns have suffered micro-fracturing can collapse completely during moderate aftershocks.',
    source: 'GSI / NDMA Post-Earthquake Building Safety Assessment Protocol',
    warning: 'MANDATORY INVARIANT: Earthquakes and aftershocks CANNOT be predicted in time or magnitude. Treat every compromised building as hazardous.',
    related_cascading_risk: 'Secondary structural collapse of earthquake-weakened structures during aftershocks.',
    practical_steps: [
      'Remain in designated open community relief grounds or parks.',
      'Inspect exterior walls from safe distance for deep X-shaped shear cracks between windows.',
      'If trapped under rubble, protect airway from dust; tap rhythmically on metal pipes or masonry with stones (whistle if available) to signal NDRF search dogs.'
    ],
    warning_signs: [
      'Visible X-cracks on load-bearing masonry or crumbling concrete spalling off structural columns.'
    ],
    what_not_to_do: [
      'Never go back inside a cracked building to retrieve passports, jewelry, or cash.',
      'Do not shout continuously if trapped under rubble (shouting exhausts oxygen and fills lungs with fatal cement dust; tap on pipes instead).'
    ],
    vulnerable_groups: 'Provide emotional support and warm blankets to children and elderly traumatized by tremors in open relief camps.',
    checklist: [
      'Remain in open area away from cracked buildings.',
      'Signal rescue teams rhythmically by tapping on pipes if trapped.',
      'Wait for official structural clearance before entering homes.'
    ]
  }
];
