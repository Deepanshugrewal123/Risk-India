/**
 * RISK // INDIA — Extended Citizen Disaster Safety Guidance Master Dataset
 * =========================================================================
 * Comprehensive Before / During / After life-safety guidelines across all 6 hazards:
 * FLOOD, CYCLONE, HEATWAVE, SEVERE_WEATHER, LANDSLIDE, EARTHQUAKE.
 *
 * Aligned with NDMA Standard Operating Procedures, IMD Guidelines, and the Disaster Management Act 2005.
 * Features progressive disclosure:
 * Level 1: Action title
 * Level 2: Short 1-2 sentence instruction
 * Level 3/4: Detailed on-demand guidance:
 *   - Why this matters (life-safety rationale)
 *   - What to do / How to do it (practical steps)
 *   - Warning signs / When to act (field signs on the ground)
 *   - What not to do (dangerous actions)
 *   - Who needs extra attention (vulnerable demographics)
 *   - Related cascading risk (links primary hazard consequence to secondary hazards)
 *   - Action checklist (interactive subtasks)
 *
 * Guarantees:
 * - Zero artificial 4-item slicing (6 items per phase, 18 items per hazard, 108 total).
 * - Prioritized: CRITICAL first, then IMPORTANT (HIGH), then HELPFUL (RECOMMENDED).
 * - Zero synthetic records (synthetic_records == 0).
 */

import { SafetyInstructionItem } from '../types/safetyGuide';

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
    title: 'Store Potable Drinking Water in Elevated Sealed Containers',
    instruction: 'Store at least 3 to 4 litres of clean drinking water per person per day for a minimum 72-hour period in elevated, food-grade vessels.',
    priority: 'CRITICAL',
    reason: 'Floodwaters submerge municipal distribution pipes and open wells, introducing pathogenic sewage and industrial effluent into the drinking supply.',
    source: 'NDMA National Disaster Management Guidelines: Management of Floods (Section 4.3)',
    warning: 'Do not rely on municipal tap water or domestic borewells once floodwaters approach residential sectors.',
    related_cascading_risk: 'Water supply contamination and enteric waterborne epidemics (Cholera, Typhoid).',
    practical_steps: [
      'Thoroughly wash and sanitize food-grade drums or jerrycans with mild chlorinated boiled water.',
      'Fill vessels to the brim to minimize air headspace and seal lids tightly with food-safe wrap.',
      'Keep stored containers on upper floors or tables elevated at least 1 metre above ground slab.',
      'Store 100 chlorine halogen water purification tablets (Halazone / NaDCC) for emergency point-of-use.'
    ],
    warning_signs: [
      'Municipal tap water appears cloudy, silty, or carries an earthy sewage odor.',
      'Local storm culverts begin backing up onto neighborhood road surfaces.',
      'CWC hydrological bulletin indicates upstream river level crossing Warning Stage.'
    ],
    what_not_to_do: [
      'Do NOT use chemical drums or oil carboys to store drinking water.',
      'Do NOT leave water storage containers uncovered or resting directly on flood-prone mud ground.',
      'Do NOT wait until municipal water pressure drops to begin emergency water storage.'
    ],
    vulnerable_groups: 'Infants needing reconstituted milk formula, pregnant mothers, dialysis patients, and bedridden elders who require uninterrupted oral hydration.',
    checklist: [
      'Sanitize food-grade water containers',
      'Fill 4 litres per family member per day for 3 days',
      'Store containers on upper level or raised tables',
      'Pack chlorine halogen tablets and water dropper in emergency kit'
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
    related_cascading_risk: 'Severe recovery delays and relief bottlenecks caused by lost statutory identification.',
    practical_steps: [
      'Scan all essential identity cards, land records, and insurance certificates; save encrypted digital copies on secure cloud storage.',
      'Pack physical original documents inside two concentric heavy-duty ziplock pouches.',
      'Keep the waterproof pouch inside your primary 72-hour emergency grab bag near the main exit door.',
      'Write down emergency phone contacts on a laminated physical card inside the pouch.'
    ],
    warning_signs: [
      'Local administration issues an Orange or Red hydrological alert for your river basin.',
      'Low-lying approach roads to your neighborhood start showing surface runoff pooling.'
    ],
    what_not_to_do: [
      'Do NOT leave original paper documents inside ground-floor wooden drawers or metal almirahs.',
      'Do NOT pack documents at the bottom of heavy suitcases that cannot be carried rapidly on foot.'
    ],
    vulnerable_groups: 'Elderly pensioners and daily-wage laborers who depend entirely on physical Aadhaar/ration cards for monthly statutory entitlements.',
    checklist: [
      'Photograph all Aadhaar, PAN, ration cards & land records',
      'Seal physical documents in double waterproof zipbags',
      'Place pouch inside top compartment of emergency grab bag'
    ]
  },
  {
    id: 'fld-bef-03',
    hazard: 'FLOOD',
    phase: 'BEFORE',
    category: 'SAFE_ROUTES_EVACUATION',
    title: 'Map Multiple High-Ground Evacuation Paths to Designated Shelters',
    instruction: 'Identify at least two high-ground evacuation paths to designated community multi-purpose flood shelters, elevated school buildings, or reinforced concrete structures.',
    priority: 'CRITICAL',
    reason: 'Low-lying culverts, railway underpasses, and river bridges inundate rapidly, cutting off exit routes hours before peak river crest.',
    source: 'CWC Flood Forecasting & Inundation Mapping Handbook',
    warning: 'Never plan an evacuation route that crosses low-water bridges, earthen causeways, or culvert dips.',
    related_cascading_risk: 'Road washouts, transportation paralysis, and community isolation.',
    practical_steps: [
      'Walk your planned evacuation route in advance to locate elevated terrain landmarks.',
      'Identify alternate routes in case primary low-lying arterial bridges become inundated.',
      'Locate designated government cyclone/flood shelters or reinforced community buildings.',
      'Agree on a family meeting assembly point outside the flood basin.'
    ],
    warning_signs: [
      'Roadside culverts overflowing with muddy water.',
      'Police or civic authorities closing low-lying causeways.',
      'District Disaster Management Authority (DDMA) issuing advisory alerts.'
    ],
    what_not_to_do: [
      'Do NOT attempt to cross causeways once water covers the road markers.',
      'Do NOT wait until water enters ground-floor rooms before beginning evacuation.'
    ],
    vulnerable_groups: 'Families with mobility-impaired elders, infants, and pregnant mothers who require extra transit time.',
    checklist: [
      'Walk primary and secondary evacuation routes with family',
      'Note phone number of designated shelter warden',
      'Confirm vehicle has full fuel tank and is parked on high ground'
    ]
  },
  {
    id: 'fld-bef-04',
    hazard: 'FLOOD',
    phase: 'BEFORE',
    category: 'VULNERABLE_MEMBERS',
    title: 'Prioritize Transport Plan for Elderly, Children & Medically Fragile Members',
    instruction: 'Arrange early transport for elderly family members, infants, pregnant women, and persons with disabilities to elevated relatives’ homes before road access degrades.',
    priority: 'CRITICAL',
    reason: 'Mobility-impaired and medically vulnerable individuals cannot navigate sudden moving floodwaters or swift evacuations once water enters streets.',
    source: 'NDMA Guidelines on Disability Inclusive Disaster Risk Reduction (DiDRR)',
    related_cascading_risk: 'Emergency rescue bottlenecks and hypothermia during rapid inundation.',
    practical_steps: [
      'Identify family or friends residing on elevated terrain outside the flood zone.',
      'Pack a 7-day supply of daily prescription medications, inhalers, insulin, and medical reports.',
      'Transfer medically fragile relatives during daylight hours well before water approaches roads.',
      'Notify the local Asha worker, ward councillor, or DDMA helpline of any bedridden individuals.'
    ],
    warning_signs: [
      'Continuous monsoon downpour forecast for more than 24 hours.',
      'River basin upstream gauge registering rapid rise rate (>10 cm/hr).'
    ],
    what_not_to_do: [
      'Do NOT delay vulnerable member relocation until night-time emergency boat rescue is required.',
      'Do NOT leave elderly family members alone in ground-floor houses.'
    ],
    vulnerable_groups: 'Bedridden elders, dialysis patients, wheelchair users, and infants under 1 year.',
    checklist: [
      'Pack 7-day medication kit with written doctor prescriptions',
      'Arrange high-ground vehicle transport 12-24h before peak water',
      'Inform local emergency disaster cell of medical vulnerability'
    ]
  },
  {
    id: 'fld-bef-05',
    hazard: 'FLOOD',
    phase: 'BEFORE',
    category: 'PETS_AND_LIVESTOCK',
    title: 'Untie Livestock & Move Animals to Elevated Embankments',
    instruction: 'Untie domestic cattle, goats, and working animals; move them to elevated community highlands or embankments. Stock dry fodder on raised bamboo platforms.',
    priority: 'HIGH',
    reason: 'Tethered animals drown when floodwaters rise rapidly. Untying allows natural survival instincts and prevents massive post-disaster carcass contamination.',
    source: 'Department of Animal Husbandry and Dairying Disaster Management Plan',
    warning: 'Never leave cattle or pets tied to sheds in low-lying flood-prone areas.',
    related_cascading_risk: 'Mass livestock mortality causing post-flood biological contamination and anthrax/blackquarter outbreaks.',
    practical_steps: [
      'Identify elevated flood platforms (high grounds/chapories) built by local animal husbandry departments.',
      'Untie all halters and tethers so animals can swim or walk to elevated knolls if waters rise.',
      'Stock dry paddy straw and feed concentrates on bamboo lofts above expected flood level.',
      'Vaccinate cattle against hemorrhagic septicemia and blackquarter prior to monsoon onset.'
    ],
    warning_signs: [
      'River overflow water entering lower agricultural fields and pasture lands.',
      'Drainage ditches surrounding animal sheds filling up rapidly.'
    ],
    what_not_to_do: [
      'Do NOT padlock or rope animal sheds in vulnerable floodplains.',
      'Do NOT force cattle to drink floodwater carrying dead silt and sewage runoff.'
    ],
    vulnerable_groups: 'Milch cows, calves, and small goats unable to swim against strong currents.',
    checklist: [
      'Untie all animal tethers before water reaches barn floor',
      'Move livestock to designated village high mound',
      'Protect dry fodder bales on raised timber platforms'
    ]
  },
  {
    id: 'fld-bef-06',
    hazard: 'FLOOD',
    phase: 'BEFORE',
    category: 'PROPERTY_PREPARATION',
    title: 'Install Sewer Backflow Valves & Sandbag Ground-Floor Drains',
    instruction: 'Install check valves or plug ground-floor toilet drains with sandbags to prevent sewage backflow; clear neighborhood runoff culverts of plastic blockages.',
    priority: 'RECOMMENDED',
    reason: 'Rising stormwater exerts back-pressure into municipal sewer mains, driving contaminated blackwater into ground-floor habitations.',
    source: 'CPHEEO Urban Drainage Manual',
    related_cascading_risk: 'Urban waterlogging, indoor sanitation failure, and vector proliferation.',
    practical_steps: [
      'Place heavy sandbags over ground-floor toilet floor drains, inspection chambers, and sink outlets.',
      'Inspect roof downspouts to ensure rainwater discharges freely away from building foundations.',
      'Remove accumulated plastic debris from neighborhood roadside gutters.',
      'Move valuable household furniture and carpets to upper floors.'
    ],
    warning_signs: [
      'Gurgling sounds from ground-floor toilet bowls.',
      'Water rising back up through floor drainage grates.'
    ],
    what_not_to_do: [
      'Do NOT open municipal sewer manholes on flooded streets; open manholes create lethal submerged whirlpools.',
      'Do NOT use chemical drain cleaners during active flood back-pressure.'
    ],
    vulnerable_groups: 'Ground-floor apartment dwellers and basement shopkeepers.',
    checklist: [
      'Fill and place sandbags over ground-floor drain holes',
      'Clear perimeter yard drains of debris and sediment',
      'Move electronics and carpets to first floor'
    ]
  },

  // --- FLOOD: DURING ---
  {
    id: 'fld-dur-01',
    hazard: 'FLOOD',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Never Walk, Swim, or Drive Through Moving Floodwater (6-Inch Rule)',
    instruction: 'Adhere strictly to the Six-Inch / Two-Foot Rule: Just 15 cm (6 inches) of moving water can knock down an adult; 30 cm can float a small car; 60 cm can sweep away an SUV.',
    priority: 'CRITICAL',
    reason: 'Moving water exerts immense hydrodynamic pressure, and submerged road surfaces may have been entirely washed away beneath the murky water.',
    source: 'NDMA Standard Operating Procedure for Flood Response',
    warning: 'Turn Around, Don’t Drown! Over 50% of flood fatalities occur in vehicles attempting to cross submerged roads.',
    related_cascading_risk: 'Culvert scour, road subsidence, and vehicular drowning.',
    practical_steps: [
      'If driving and encountering water of unknown depth over the road, stop immediately, reverse safely, and seek alternate high routes.',
      'If your vehicle stalls in rapidly rising water, abandon it immediately and scramble to higher ground.',
      'If compelled to wade through shallow, standing water, probe every footstep ahead using a sturdy wooden stick.',
      'Wear sturdy closed-toe shoes or gumboots to protect feet from submerged rusty iron, sharp debris, and venomous snakes.'
    ],
    warning_signs: [
      'Water flowing rapidly across road dips with visible surface ripples or eddies.',
      'Roadside markers, culvert railings, or median curbs disappear under murky water.',
      'Vehicle floating sensation, loss of steering traction, or water entering vehicle door floorboards.'
    ],
    what_not_to_do: [
      'Do NOT drive around police barricades or road-closed warning signs on flooded causeways.',
      'Do NOT walk near open storm drains, drainage catch basins, or manholes with dislodged covers.',
      'Do NOT allow curious children or youth to swim or take selfies near swollen rivers or flood culverts.'
    ],
    vulnerable_groups: 'Schoolchildren, elderly citizens with walking aids, motorcycle commuters, and auto-rickshaw drivers.',
    checklist: [
      'Turn vehicle around upon spotting submerged roadway',
      'Abandon vehicle immediately if water reaches door frame',
      'Use a wooden probe stick when wading through necessary shallow water',
      'Keep hands free and children secured in life vests or carry pouches'
    ]
  },
  {
    id: 'fld-dur-02',
    hazard: 'FLOOD',
    phase: 'DURING',
    category: 'UTILITY_SAFETY',
    title: 'Shut Off Main Electrical Breaker & LPG Gas Cylinders',
    instruction: 'Turn off your home’s main electrical breaker switch and close the regulator valves of all domestic cooking gas (LPG) cylinders before evacuating.',
    priority: 'CRITICAL',
    reason: 'Water submerged electrical outlets cause lethal electrocution; displaced buoyant gas cylinders can rupture pipes and trigger explosions.',
    source: 'Central Electricity Authority (CEA) Safety Regulations',
    warning: 'Do not touch the electrical switch panel if you are already standing in water.',
    related_cascading_risk: 'Electrical short-circuit fires and underwater electrification.',
    practical_steps: [
      'Switch off individual appliance switches first, then pull the main knife switch or trip the MCB.',
      'Ensure you are standing on dry wooden board or rubber mat; wear dry rubber-soled shoes.',
      'Turn LPG regulator knob to closed (horizontal/off) position; disconnect pipe and store cylinder upright on high table.',
      'Unplug all television, refrigerator, and inverter chargers from wall sockets.'
    ],
    warning_signs: [
      'Water level approaching bottom of ground-floor electrical switch sockets (approx 30 cm from floor).',
      'Sparks, buzzing noises, or faint burnt smell from electrical distribution board.'
    ],
    what_not_to_do: [
      'Do NOT touch electrical switchboards with wet hands or while standing in puddle water.',
      'Do NOT light matches or candles if you detect sulfur or LPG odor.'
    ],
    vulnerable_groups: 'Elderly residents unfamiliar with miniature circuit breaker (MCB) panels.',
    checklist: [
      'Trip the main building electrical circuit breaker',
      'Close LPG cylinder regulator valve tightly',
      'Disconnect power inverter backup batteries'
    ]
  },
  {
    id: 'fld-dur-03',
    hazard: 'FLOOD',
    phase: 'DURING',
    category: 'SAFE_ROUTES_EVACUATION',
    title: 'Comply Instantly with Statutory Evacuation Directives',
    instruction: 'Evacuate immediately upon announcement of official directives by the District Magistrate / SDMA / NDRF. Do not delay waiting for water to enter the house.',
    priority: 'CRITICAL',
    reason: 'Under Section 30 of the Disaster Management Act 2005, district authorities order evacuations based on upstream dam discharge and hydrological crest models.',
    source: 'Disaster Management Act 2005 (Statutory Framework)',
    warning: 'Self-evacuation during the day is far safer than dangerous night-time boat rescue operations.',
    related_cascading_risk: 'Stranded populations requiring emergency helicopter or boat rescue.',
    practical_steps: [
      'Lock house doors and windows; secure upper floor latches.',
      'Carry your 72-hour emergency grab bag, waterproof document pouch, and essential medications.',
      'Follow routes designated by traffic police and civil defense volunteers.',
      'Check in at the official registration desk at the relief camp so family tracing can occur.'
    ],
    warning_signs: [
      'Loudspeaker announcements from police patrol vans or siren signals.',
      'SDRF / NDRF personnel arriving with inflatable rescue boats.'
    ],
    what_not_to_do: [
      'Do NOT resist statutory evacuation directives to protect material possessions.',
      'Do NOT take bulky steel trunks or heavy furniture onto rescue boats.'
    ],
    vulnerable_groups: 'Elderly homeowners reluctant to leave ancestral property.',
    checklist: [
      'Carry emergency grab bag and waterproof document pack',
      'Lock all doors and windows securely',
      'Report immediately to designated government relief shelter'
    ]
  },
  {
    id: 'fld-dur-04',
    hazard: 'FLOOD',
    phase: 'DURING',
    category: 'EMERGENCY_CONTACTS',
    title: 'Signal Distress from Rooftop if Trapped by Sudden Inundation',
    instruction: 'Move to the highest accessible roof level. Signal distress using a whistle, flashlight, or brightly colored cloth. Dial 112 (National Emergency) or 1078 (NDMA).',
    priority: 'HIGH',
    reason: 'Blowing a whistle preserves vocal energy and carries sound significantly farther than shouting over the roar of floodwaters.',
    source: 'NDRF Search and Rescue Operational Protocol',
    warning: 'Do not climb into an enclosed attic without an exterior roof hatch; rising waters can trap you against the ceiling.',
    related_cascading_risk: 'Hypothermia and acute exposure.',
    practical_steps: [
      'Scramble to the highest accessible terrace or reinforced roof slab.',
      'Tie a bright red or orange cloth to a pole or television antenna.',
      'Blow three sharp whistle blasts repeatedly (universal distress signal).',
      'Conserve phone battery: send GPS coordinates via SMS to 112 before battery drains.'
    ],
    warning_signs: [
      'Water rapidly rising past window sill level on ground floor.',
      'Internal staircases becoming submerged by brown, turbulent current.'
    ],
    what_not_to_do: [
      'Do NOT hide inside closed crawlspaces or attics with no roof exit.',
      'Do NOT jump into swift flood currents expecting to swim across.'
    ],
    vulnerable_groups: 'Children and seniors prone to hypothermia from wind and rain on open roofs.',
    checklist: [
      'Move family and warm blankets to roof slab',
      'Tie bright cloth signal to rooftop pole',
      'Send SMS with address and headcount to 112'
    ]
  },
  {
    id: 'fld-dur-05',
    hazard: 'FLOOD',
    phase: 'DURING',
    category: 'MEDICAL_AND_HEALTH',
    title: 'Beware of Displaced Venomous Snakes & Submerged Sharp Debris',
    instruction: 'Watch for snakes (cobras, kraits, vipers) seeking refuge on elevated furniture, verandas, and trees; use a torch and walking stick when moving in darkness.',
    priority: 'HIGH',
    reason: 'Floodwaters inundate subterranean snake burrows, forcing venomous snakes into human dwellings; snakebite incidence spikes sharply during active floods.',
    source: 'National Snakebite Management Protocol (Ministry of Health & Family Welfare)',
    warning: 'Do not reach blindly into floating vegetation, thatch piles, or elevated shelves.',
    related_cascading_risk: 'Secondary envenomation crises overwhelming flood rescue personnel.',
    practical_steps: [
      'Always shine a flashlight ahead before stepping onto stairs or furniture.',
      'Tap a wooden pole against doorframes and walls before sitting down.',
      'If bitten, keep victim calm and immobilize the limb with a broad crepe bandage (pressure immobilization).',
      'Do NOT cut, suck, or apply tight tourniquets to the bite site; call 108 immediately for Anti-Snake Venom (ASV).'
    ],
    warning_signs: [
      'Floating clumps of water hyacinth or debris rafts approaching verandas.',
      'Hissing sounds from ceiling lofts, fuel wood stacks, or window sills.'
    ],
    what_not_to_do: [
      'Do NOT try to handle or kill a swimming snake.',
      'Do NOT reach blindly under beds or into submerged storage boxes.'
    ],
    vulnerable_groups: 'Children playing near floodwaters and farmers wading through inundated courtyards.',
    checklist: [
      'Keep torch batteries fresh and accessible on top shelf',
      'Use walking stick to probe before stepping',
      'Note nearest community health centre stocking ASV vials'
    ]
  },
  {
    id: 'fld-dur-06',
    hazard: 'FLOOD',
    phase: 'DURING',
    category: 'TRANSPORTATION',
    title: 'Avoid Low-Water Bridges, Culverts & Subway Underpasses',
    instruction: 'Never enter pedestrian underpasses, vehicular subways, or low-water causeways during heavy downpours.',
    priority: 'CRITICAL',
    reason: 'Urban subways and railway underpasses act as natural drainage sumps, filling with 3 to 5 metres of water in under 15 minutes with no escape path.',
    source: 'NDMA Urban Flooding Standard Operating Procedures',
    related_cascading_risk: 'Submerged vehicular drowning and urban transit gridlock.',
    practical_steps: [
      'Take elevated bypass roads or arterial flyovers even if route is 5 km longer.',
      'Follow civic traffic police diversions strictly.',
      'If trapped inside subway, unbuckle seatbelt, roll down window immediately before electrical power cuts, and escape.'
    ],
    warning_signs: [
      'Water accumulation visible at dip entry point.',
      'Stormwater gushing out of manhole grates inside underpass.'
    ],
    what_not_to_do: [
      'Do NOT follow buses or heavy trucks into flooded underpasses thinking the road is passable.',
      'Do NOT hesitate to smash window if doors cannot open due to water pressure.'
    ],
    vulnerable_groups: 'Two-wheeler and auto-rickshaw commuters.',
    checklist: [
      'Check traffic police real-time diversion alerts',
      'Avoid subway dips during heavy rainfall',
      'Keep emergency glass breaker in vehicle glove box'
    ]
  },

  // --- FLOOD: AFTER ---
  {
    id: 'fld-aft-01',
    hazard: 'FLOOD',
    phase: 'AFTER',
    category: 'RECOVERY_AND_HEALTH',
    title: 'Boil All Water Vigorously for 1 Full Minute Before Consumption',
    instruction: 'Boil all tap water, open well water, and tube-well water vigorously for at least 1 full minute (or use certified chlorine halogen tablets) before drinking, cooking, or brushing teeth.',
    priority: 'CRITICAL',
    reason: 'Floodwaters carry sewage pathogens, Escherichia coli, Vibrio cholerae, and Leptospira interrogans bacteria, causing cholera, acute gastroenteritis, and leptospirosis.',
    source: 'National Centre for Disease Control (NCDC) Post-Disaster Health Advisory',
    warning: 'Water filters alone may not eliminate viral contaminants if backflow pressure damaged the membrane.',
    related_cascading_risk: 'Leptospirosis and waterborne diarrheal epidemics.',
    practical_steps: [
      'Bring water to a full rolling boil for a minimum of 60 seconds (or 3 minutes at altitudes above 2000 m).',
      'Allow water to cool naturally in clean, covered glass or stainless steel vessels.',
      'If fuel is unavailable, add 1 certified chlorine purification tablet per 20 litres of clear water; wait 30 minutes before drinking.',
      'Disinfect open well sources using bleaching powder at 2.5 grams per 1,000 litres under PHED supervision.'
    ],
    warning_signs: [
      'Family members report sudden vomiting, watery diarrhea, or high fever with muscle cramps.',
      'Well water appears turbid, foul-smelling, or shows visible surface scum post-flood.',
      'Local community PHC reports sudden spike in gastrointestinal infections.'
    ],
    what_not_to_do: [
      'Do NOT drink unboiled tap water or ice made from untreated water even if it looks visually clear.',
      'Do NOT use untreated water to wash cooking utensils, vegetables, or baby feeding bottles.',
      'Do NOT swallow water while taking bucket baths.'
    ],
    vulnerable_groups: 'Children under 5 years, elderly grandparents, chemotherapy patients, and anyone with compromised immunity.',
    checklist: [
      'Bring all drinking and cooking water to a 60-second rolling boil',
      'Store boiled water in covered stainless steel vessels with taps',
      'Disinfect water storage tanks and household filters before reuse',
      'Prepare Oral Rehydration Salts (ORS) solution at the first sign of loose stools'
    ]
  },
  {
    id: 'fld-aft-02',
    hazard: 'FLOOD',
    phase: 'AFTER',
    category: 'STRUCTURAL_SAFETY',
    title: 'Inspect Building Foundations & Walls for Structural Settlement Cracks',
    instruction: 'Inspect perimeter walls, pillars, and foundations for new structural cracks, soil settlement, or scouring before allowing family members to re-enter premises.',
    priority: 'CRITICAL',
    reason: 'Prolonged waterlogging softens sub-surface foundation soil, leading to differential settlement and sudden structural collapse hours after water recedes.',
    source: 'NDMA Post-Flood Structural Safety Audit Manual',
    warning: 'Do not enter if walls are bowed, plaster is falling heavily, or doors are jammed in frames.',
    related_cascading_risk: 'Structural building collapse and secondary entrapment.',
    practical_steps: [
      'Walk around exterior perimeter first; inspect foundation grade beams for diagonal shear cracks.',
      'Check if doors and windows open smoothly; jammed frames indicate structural racking.',
      'Probe foundation perimeter soil with a stick to check for hidden washout voids or sinkholes.',
      'Have an authorized civil engineer or municipal surveyor inspect before undertaking major repairs.'
    ],
    warning_signs: [
      'Horizontal or diagonal cracks wider than 5 mm in brick masonry or reinforced concrete pillars.',
      'Visible tilt in porch columns, boundary walls, or external balconies.'
    ],
    what_not_to_do: [
      'Do NOT allow children or family to sleep inside building with severe foundation settlement.',
      'Do NOT remove supporting props or jacks without professional engineering guidance.'
    ],
    vulnerable_groups: 'Inhabitants of old unreinforced brick or mud-mortar homes.',
    checklist: [
      'Conduct 360-degree perimeter walk inspection',
      'Check doors and window frames for jamming',
      'Mark any foundation cracks with chalk and monitor widening'
    ]
  },
  {
    id: 'fld-aft-03',
    hazard: 'FLOOD',
    phase: 'AFTER',
    category: 'SANITATION',
    title: 'Disinfect Submerged Living Quarters Wearing Protective Boots & Gloves',
    instruction: 'Scrub all flood-silted surfaces using clean water mixed with domestic disinfectant or bleaching powder; wear heavy rubber gloves and gumboots.',
    priority: 'HIGH',
    reason: 'Flood silt contains decaying sewage, animal carcasses, industrial heavy metals, and tetanus spores.',
    source: 'CPHEEO Post-Calamity Environmental Sanitation Manual',
    related_cascading_risk: 'Tetanus infections, skin dermatoses, and mould proliferation.',
    practical_steps: [
      'Shovel out mud and silt while still wet before it hardens into concrete-like crust.',
      'Scrub hard floors and masonry walls with solution of 1 cup chlorine bleach per 5 litres clean water.',
      'Open all doors and windows to facilitate rapid cross-ventilation and moisture evaporation.',
      'Ensure family members have active tetanus toxoid (TT) vaccination within past 5 years.'
    ],
    warning_signs: [
      'Foul sour stench from damp walls.',
      'Black or dark green mould patches spreading on damp plasterboards.'
    ],
    what_not_to_do: [
      'Do NOT handle flood silt with bare hands or walk barefoot in sludge.',
      'Do NOT mix chlorine bleach with ammonia or acid toilet cleaners (generates lethal chlorine gas).'
    ],
    vulnerable_groups: 'Persons with open cuts, skin abrasions, or chronic asthma/bronchitis.',
    checklist: [
      'Wear rubber gumboots, heavy-duty gloves, and face mask',
      'Scrub walls and floors with chlorine bleach solution',
      'Verify household tetanus vaccination currency'
    ]
  },
  {
    id: 'fld-aft-04',
    hazard: 'FLOOD',
    phase: 'AFTER',
    category: 'WATER_AND_FOOD',
    title: 'Discard Submerged Perishable Food, Grains & Wet Medications',
    instruction: 'Discard all fresh vegetables, open grain sacks, and bottled medicines that have come into contact with floodwater.',
    priority: 'HIGH',
    reason: 'Floodwater penetrates plastic screw caps and porous packaging; consuming contaminated grains causes fatal toxic enteritis.',
    source: 'Food Safety and Standards Authority of India (FSSAI) Post-Flood Advisory',
    related_cascading_risk: 'Mass foodborne poisoning and acute gastroenteritis outbreaks.',
    practical_steps: [
      'Throw away canned goods with bulging lids, dents, or rusted seams.',
      'Discard all cardboard packaged cereals, flour bags, and spices submerged in water.',
      'Throw out prescription medicines, insulin vials, or syrups submerged in floodwater.',
      'Disinfect undamaged commercial metal cans with bleach solution before opening.'
    ],
    warning_signs: [
      'Unusual odor or discoloration on dried food items.',
      'Slimy feel on exterior of packaged food items.'
    ],
    what_not_to_do: [
      'Do NOT attempt to sun-dry and consume flood-submerged rice, dal, or wheat.',
      'Do NOT feed contaminated food scraps to household pets or cattle.'
    ],
    vulnerable_groups: 'Young children and elders susceptible to acute foodborne intoxication.',
    checklist: [
      'Dispose of submerged open grain sacks safely',
      'Discard contaminated medicines and request fresh prescription from PHC',
      'Clean food prep surfaces with boiling water and disinfectant'
    ]
  },
  {
    id: 'fld-aft-05',
    hazard: 'FLOOD',
    phase: 'AFTER',
    category: 'UTILITY_SAFETY',
    title: 'Have Electrician Certify Wiring Before Restoring Power Breakers',
    instruction: 'Do not turn on electrical circuit breakers until wiring, wall sockets, and distribution panels have completely dried out and been tested by a licensed electrician.',
    priority: 'CRITICAL',
    reason: 'Moisture trapped behind switchboards causes severe phase-to-ground arcing, lethal electrocution, and devastating post-flood electrical fires.',
    source: 'Central Electricity Authority (CEA) Post-Inundation Safety Norms',
    related_cascading_risk: 'Secondary electrical fires and electrocution fatalities.',
    practical_steps: [
      'Keep main breaker in the OFF position until floodwaters have fully receded for at least 48 hours.',
      'Have electrician test insulation resistance (Megger test) between phase, neutral, and ground.',
      'Replace all switches and sockets that were submerged in muddy water.',
      'Ensure home appliances (refrigerator, washing machine) are dried and tested before plugging in.'
    ],
    warning_signs: [
      'Moisture condensation visible inside electrical meter glass.',
      'Tripping of circuit breaker immediately upon switching on.'
    ],
    what_not_to_do: [
      'Do NOT plug in wet appliances to test if they work.',
      'Do NOT touch electrical appliances while standing on damp floors.'
    ],
    vulnerable_groups: 'Homeowners eager to restore lights without electrical knowledge.',
    checklist: [
      'Keep main circuit breaker switched off',
      'Schedule licensed electrician insulation test',
      'Replace water-submerged ground-level switches'
    ]
  },
  {
    id: 'fld-aft-06',
    hazard: 'FLOOD',
    phase: 'AFTER',
    category: 'MEDICAL_AND_HEALTH',
    title: 'Eliminate Stagnant Water Pools to Suppress Vector Epidemics',
    instruction: 'Drain stagnant puddles in discarded tires, coconut shells, and water tanks within 72 hours; sleep under insecticide-treated mosquito nets.',
    priority: 'HIGH',
    reason: 'Receding floodwaters create millions of stagnant shallow pools, driving explosive breeding of Aedes and Anopheles mosquitoes within 7 to 10 days.',
    source: 'National Vector Borne Disease Control Programme (NVBDCP)',
    related_cascading_risk: 'Dengue, Malaria, and Chikungunya post-flood epidemic spikes.',
    practical_steps: [
      'Invert or discard broken pottery, plastic cups, and used tires in the yard.',
      'Pour a thin film of domestic kerosene or temephos larvicide onto stagnant roadside ditches.',
      'Sleep under long-lasting insecticide-treated bed nets (LLINs).',
      'Report large stagnant water bodies to municipal vector control teams for fogging.'
    ],
    warning_signs: [
      'Sharp increase in mosquito swarms at dusk and dawn.',
      'Family members developing high fever with retro-orbital pain and joint aches.'
    ],
    what_not_to_do: [
      'Do NOT store water in open drums without tight mesh covers.',
      'Do NOT ignore high fever accompanied by shivering or petechial skin rashes.'
    ],
    vulnerable_groups: 'Infants, pregnant mothers, and elderly citizens prone to severe dengue shock.',
    checklist: [
      'Empty all standing water containers around house',
      'Set up insecticide-treated mosquito nets over beds',
      'Report fever cases immediately to local Primary Health Centre (PHC)'
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
    category: 'PROPERTY_PREPARATION',
    title: 'Reinforce Roof Trusses, Secure Tin Sheets & Install Storm Shutters',
    instruction: 'Inspect and fasten roof sheets with metal U-bolts; install plywood storm shutters or tape glass panes diagonally to prevent explosive wind suction.',
    priority: 'CRITICAL',
    reason: 'Cyclonic winds exceeding 120 km/h create massive aerodynamic uplift, ripping unfastened corrugated sheets and transforming them into lethal flying guillotines.',
    source: 'NDMA Cyclone Management Guidelines (Section 3.4)',
    related_cascading_risk: 'Roof blow-off, wall collapse, and severe airborne projectile trauma.',
    practical_steps: [
      'Tighten J-bolts on asbestos and galvanized iron sheets; replace rusted washers with rubber gaskets.',
      'Board up external glass windows with 12 mm exterior plywood or install storm shutters.',
      'Apply diagonal masking tape strips across large glass panes to prevent shattering shards.',
      'Anchor rooftop solar panels and satellite dish antennas with high-tensile steel cables.'
    ],
    warning_signs: [
      'IMD issues Cyclone Alert (Yellow bulletin 48h prior) or Cyclone Warning (Orange bulletin 24h prior).',
      'Barometric pressure dropping sharply accompanied by gusty oceanic swell.'
    ],
    what_not_to_do: [
      'Do NOT place heavy loose bricks on tin roofs expecting weight to hold them down; wind will turn them into flying projectiles.',
      'Do NOT leave windows cracked open on windward side during cyclonic landfall.'
    ],
    vulnerable_groups: 'Residents of semi-pucca houses with tin or asbestos roofing sheets.',
    checklist: [
      'Inspect roof J-bolts and secure with rubber washers',
      'Board up or tape external glass windows',
      'Secure solar panels and satellite antennas'
    ]
  },
  {
    id: 'cyc-bef-02',
    hazard: 'CYCLONE',
    phase: 'BEFORE',
    category: 'PROPERTY_PREPARATION',
    title: 'Trim Dead Tree Branches & Clear Yard Projectiles',
    instruction: 'Trim dying branches overhanging electric cables, roofs, and driveways; secure or bring indoors all loose outdoor pots, ladders, and metal scrap.',
    priority: 'HIGH',
    reason: 'Gale-force gusts snap heavy tree limbs, crushing house roofs and tearing down overhead high-voltage power lines.',
    source: 'IMD Coastal Cyclone Preparedness Manual',
    related_cascading_risk: 'Grid power blackouts, road blockages, and electrocution hazards.',
    practical_steps: [
      'Prune branches within 3 metres of overhead electrical service cables with utility assistance.',
      'Bring indoor potted plants, outdoor furniture, zinc buckets, and trash bins.',
      'Secure temporary construction materials and wooden planks in shed.',
      'Park vehicles inside garage or clear of tall trees and utility poles.'
    ],
    warning_signs: [
      'Fierce gusts making mature trees bend and groan.',
      'Local power transmission lines swinging violently.'
    ],
    what_not_to_do: [
      'Do NOT climb tall trees to prune branches during active cyclonic gale warnings.',
      'Do NOT park vehicles under large banyan, eucalyptus, or gulmohar trees.'
    ],
    vulnerable_groups: 'Residents living in heavily wooded coastal settlements.',
    checklist: [
      'Prune dead overhanging tree limbs',
      'Move all loose patio and yard items inside house',
      'Park car away from tall trees and utility poles'
    ]
  },
  {
    id: 'cyc-bef-03',
    hazard: 'CYCLONE',
    phase: 'BEFORE',
    category: 'SAFE_ROUTES_EVACUATION',
    title: 'Identify Nearest Multi-Purpose Cyclone Shelter (MPCS) & Evacuation Route',
    instruction: 'Know the location of your designated reinforced concrete Multi-Purpose Cyclone Shelter; identify safe inland route away from tidal rivers.',
    priority: 'CRITICAL',
    reason: 'Storm surge inundation can penetrate 5 to 10 km inland, raising seawater levels by 3 to 6 metres within minutes and wiping out coastal thatch settlements.',
    source: 'National Cyclone Risk Mitigation Project (NCRMP) Operational Guidelines',
    related_cascading_risk: 'Catastrophic coastal storm surge drowning and saline land inundation.',
    practical_steps: [
      'Identify the nearest government MPCS building or reinforced school in your revenue village.',
      'Pack your 72-hour family survival kit with dry food, water, ID papers, and warm clothing.',
      'Note the contact phone number of the shelter management committee or village head.',
      'Evacuate immediately upon announcement of Red alert by administration.'
    ],
    warning_signs: [
      'IMD Post-Landfall Warning Bulletin forecasting storm surge of 3+ metres above astronomical tide.',
      'Local police and civil defense blowing sirens in coastal fishing villages.'
    ],
    what_not_to_do: [
      'Do NOT stay in coastal huts within 2 km of high tide line hoping the storm will shift.',
      'Do NOT delay evacuation until storm surge water enters the street.'
    ],
    vulnerable_groups: 'Coastal fishing communities, salt pan workers, and residents living in katcha huts.',
    checklist: [
      'Locate nearest reinforced cyclone shelter',
      'Pack 72-hour survival kit with dry rations and IDs',
      'Coordinate evacuation transport with village disaster committee'
    ]
  },
  {
    id: 'cyc-bef-04',
    hazard: 'CYCLONE',
    phase: 'BEFORE',
    category: 'PETS_AND_LIVESTOCK',
    title: 'Secure Coastal Fishing Boats & Move Marine Equipment Inland',
    instruction: 'Haul fishing trawlers, fiber boats, and catamarans beyond high storm surge line; secure them with steel chains to concrete anchors.',
    priority: 'HIGH',
    reason: 'Storm surges and 5-metre ocean waves smash unmoored boats against jetties, destroying fishing livelihoods and generating heavy floating wreckage.',
    source: 'Department of Fisheries Cyclone Standard Operating Procedure',
    related_cascading_risk: 'Loss of maritime livelihoods and floating harbor wreckage.',
    practical_steps: [
      'Haul mechanized boats and catamarans at least 500 metres inland or into protected creek shelters.',
      'Lash hulls with heavy marine-grade synthetic ropes or galvanized chains to reinforced mooring bollards.',
      'Remove boat engines, communication radios, and nylon nets to elevated lockups.',
      'Never venture into deep sea once Distant Warning Signal No. 2 is hoisted at port.'
    ],
    warning_signs: [
      'Port hoisting Great Danger Signal No. 8, 9, or 10.',
      'Ocean waves showing white foam crests and roaring surf sound.'
    ],
    what_not_to_do: [
      'Do NOT attempt to ride out the cyclone aboard anchored fishing trawlers.',
      'Do NOT defy port fishing prohibition orders.'
    ],
    vulnerable_groups: 'Traditional coastal fishermen and boat owners.',
    checklist: [
      'Haul boats to high inland ground',
      'Remove and store outboard engines in dry storage',
      'Lash hulls securely to fixed ground anchors'
    ]
  },
  {
    id: 'cyc-bef-05',
    hazard: 'CYCLONE',
    phase: 'BEFORE',
    category: 'EMERGENCY_KIT',
    title: 'Stock 7 Days of Non-Perishable Food, Medical Supplies & Clean Water',
    instruction: 'Stock dry high-calorie rations (puffed rice, flattened rice, jaggery, biscuits, nuts) that require zero cooking; pack first aid kit and 7 days of daily medications.',
    priority: 'HIGH',
    reason: 'Cyclones sever road access, flood markets, and knock out power grids for 5 to 10 days, cutting off fresh supplies.',
    source: 'NDMA Household Emergency Preparedness Guide',
    related_cascading_risk: 'Severe food scarcity and medical emergency isolation.',
    practical_steps: [
      'Store 20 litres of drinking water per person in sealed containers.',
      'Stock non-perishable high-protein foods: roasted chana, sattu, dates, biscuits, glucose.',
      'Pack first aid supplies: sterile gauze, band-aids, betadine, paracetamol, ORS packets.',
      'Keep waterproof matches, candles, heavy-duty torch, and extra dry batteries in ziplock bag.'
    ],
    warning_signs: [
      'Market shops running low on basic groceries due to panic buying.',
      'District collector announcing closure of schools and commercial markets.'
    ],
    what_not_to_do: [
      'Do NOT stock food that requires refrigeration or elaborate cooking fuel.',
      'Do NOT forget daily blood pressure, cardiac, and asthma medications.'
    ],
    vulnerable_groups: 'Diabetic individuals requiring insulin storage and families with infants.',
    checklist: [
      'Pack 7-day non-perishable dry ration stock',
      'Refill chronic prescription medicines',
      'Store torch, radio, and spare alkaline batteries'
    ]
  },
  {
    id: 'cyc-bef-06',
    hazard: 'CYCLONE',
    phase: 'BEFORE',
    category: 'POWER_AND_LIGHTING',
    title: 'Pre-Charge Power Banks & Tune Battery Radio to All India Radio',
    instruction: 'Fully charge all mobile phones and power banks; keep a battery-powered transistor radio tuned to local All India Radio station for official bulletins.',
    priority: 'RECOMMENDED',
    reason: 'Cellular towers and power grids collapse during landfall; terrestrial AM radio remains the sole operational broadcast channel during severe cyclonic blackouts.',
    source: 'Ministry of Information & Broadcasting Emergency Communication SOP',
    related_cascading_risk: 'Total telecommunication blackout and panic from misinformation.',
    practical_steps: [
      'Charge all emergency power banks to 100% capacity; pack in waterproof plastic bags.',
      'Note the frequency of your local All India Radio (AIR) station (e.g., Cuttack, Chennai, Kolkata, Visakhapatnam).',
      'Enable low battery mode on mobile phones and turn off background data sync.',
      'Keep one manual hand-crank or battery-powered radio with fresh spare batteries.'
    ],
    warning_signs: [
      'Cellular data speeds slowing down as transmission towers lose grid power.',
      'Local power discom announcing preventive grid shutdown.'
    ],
    what_not_to_do: [
      'Do NOT waste mobile phone battery playing games or streaming videos during pre-landfall hours.',
      'Do NOT rely on home Wi-Fi routers that will die the moment grid power fails.'
    ],
    vulnerable_groups: 'Residents in remote coastal islands and tidal delta villages.',
    checklist: [
      'Charge all mobile phones and portable power banks',
      'Test battery transistor radio on All India Radio frequency',
      'Pack phones in waterproof sealable bags'
    ]
  },

  // --- CYCLONE: DURING ---
  {
    id: 'cyc-dur-01',
    hazard: 'CYCLONE',
    phase: 'DURING',
    category: 'SHELTER',
    title: 'Remain in Interior Central Room; Beware the Deceptive "Eye of Cyclone"',
    instruction: 'Shelter in the strongest interior windowless room (hallway, bathroom). When winds suddenly cease, DO NOT go outside—this is the calm Eye; destructive winds will resume instantly from the opposite direction.',
    priority: 'CRITICAL',
    reason: 'The Eye of a cyclone brings brief deceptive calm (15-45 mins) as barometric center passes, followed immediately by violent maximum winds from the reverse direction.',
    source: 'IMD Cyclone Warning Protocol & NDMA SOP',
    warning: 'Dozens of cyclone fatalities occur when people step out during the Eye to inspect damage and are crushed when reverse gale winds resume abruptly.',
    related_cascading_risk: 'Severe blunt force trauma and decapitation from sudden reverse gale projectiles.',
    practical_steps: [
      'Stay away from all glass windows, exterior doors, and exterior brick walls.',
      'Sit under a sturdy dining table or doorframe with a mattress or thick blanket over head.',
      'Keep shoes on at all times in case sudden evacuation is forced by structural breach.',
      'If the wind suddenly drops to dead calm, remain inside; the rear eyewall is approaching.'
    ],
    warning_signs: [
      'Ears popping due to intense barometric pressure drop.',
      'Roaring sound like a low-flying jet engine outside.',
      'Sudden eerie silence and cessation of rain in the middle of the storm.'
    ],
    what_not_to_do: [
      'Do NOT step outdoors to inspect roof damage or take videos during the calm Eye of the storm.',
      'Do NOT stand near glass french windows or glass balcony doors.'
    ],
    vulnerable_groups: 'Children and curious family members eager to see outdoor damage.',
    checklist: [
      'Gather entire family in central interior room',
      'Cover heads with thick blankets or mattresses',
      'Remain inside until radio announces storm has completely moved inland'
    ]
  },
  {
    id: 'cyc-dur-02',
    hazard: 'CYCLONE',
    phase: 'DURING',
    category: 'UTILITY_SAFETY',
    title: 'Unplug All Electrical Appliances & Turn Off Domestic LPG Cylinder',
    instruction: 'Switch off main electrical circuit breaker and close gas cylinder regulators to prevent short circuits and catastrophic gas explosions.',
    priority: 'CRITICAL',
    reason: 'Power grid line swings and lightning strikes cause sudden 440V high-voltage surges that destroy household appliances and spark attic fires.',
    source: 'Central Electricity Authority (CEA) Storm Safety Regulations',
    related_cascading_risk: 'Electrical arc fires and household gas explosion emergencies.',
    practical_steps: [
      'Trip the main building MCB breaker at the start of heavy gale gusts.',
      'Unplug TV, computer, inverter, and refrigerator cords completely from wall sockets.',
      'Shut off the LPG regulator valve on cooking gas cylinders.',
      'Use battery flashlights exclusively; do not light candles during high winds.'
    ],
    warning_signs: [
      'Flickering ceiling lights and severe voltage fluctuation.',
      'Sparks seen from utility poles outside window.'
    ],
    what_not_to_do: [
      'Do NOT use open flame candles in rooms where wind gusts can knock them into curtains.',
      'Do NOT touch electrical switchboards during active thunderstorm strikes.'
    ],
    vulnerable_groups: 'Elderly residents and children left unsupervised in kitchens.',
    checklist: [
      'Trip main electrical breaker',
      'Unplug all wall cords',
      'Turn off and disconnect LPG cooking cylinder'
    ]
  },
  {
    id: 'cyc-dur-03',
    hazard: 'CYCLONE',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Do Not Venture Outdoors Under Any Circumstance',
    instruction: 'Remain strictly indoors until the local district administration or IMD officially declares that the cyclonic storm has completely passed.',
    priority: 'CRITICAL',
    reason: 'Over 80% of cyclonic casualties are caused by flying tin sheets, falling trees, snapping high-voltage wires, and collapsing boundary walls outdoors.',
    source: 'NDMA Cyclone Guidelines',
    warning: 'A tin roof sheet flying at 130 km/h has the kinetic cutting energy of an industrial guillotine.',
    related_cascading_risk: 'Fatal projectile decapitation, crush trauma, and electrocution.',
    practical_steps: [
      'Keep exterior doors bolted from the inside with heavy latches.',
      'If roof sheets begin to lift, move immediately into an interior reinforced bathroom or under concrete lintel.',
      'Listen to official radio broadcast updates on battery transistor.',
      'Keep family members together; do not allow anyone to search for missing pets outdoors during peak storm.'
    ],
    warning_signs: [
      'Sound of roofing sheets rattling and shearing bolts.',
      'Debris hitting exterior walls like artillery shrapnel.'
    ],
    what_not_to_do: [
      'Do NOT open doors to see how strong the wind is.',
      'Do NOT go outdoors to hold down roofs or rescue outdoor goods.'
    ],
    vulnerable_groups: 'Young adults tempted to record social media reels during landfall.',
    checklist: [
      'Bolt all exterior doors securely',
      'Keep all family members inside designated interior room',
      'Monitor All India Radio bulletins for official all-clear signal'
    ]
  },
  {
    id: 'cyc-dur-04',
    hazard: 'CYCLONE',
    phase: 'DURING',
    category: 'SAFE_ROUTES_EVACUATION',
    title: 'If Caught in Open Terrain, Seek Low Ditch Away from Trees & Power Lines',
    instruction: 'If caught outdoors unable to reach shelter, lie flat in a low roadside depression or ditch; cover your head with hands and clothing.',
    priority: 'HIGH',
    reason: 'Lying in a depression keeps you below the aerodynamic trajectory of high-speed airborne projectiles and reduces your lightning profile.',
    source: 'Civil Defense Manual on Tropical Storm Survival',
    related_cascading_risk: 'Severe airborne debris impact and lightning strikes.',
    practical_steps: [
      'Quickly scan terrain for a drainage culvert, ditch, or depression away from trees and utility poles.',
      'Lie face down and protect the back of your neck with interlocked fingers.',
      'Keep your mouth covered with cloth to prevent inhaling blinding torrential spray and dirt.',
      'Scramble to a reinforced concrete building as soon as a brief lull occurs.'
    ],
    warning_signs: [
      'Wind gusts exceeding 100 km/h making forward walking impossible.',
      'Branches breaking and tin sheets hurtling overhead.'
    ],
    what_not_to_do: [
      'Do NOT cling to metal transmission poles or take shelter under tall trees.',
      'Do NOT run blindly through standing water where fallen live wires may lie submerged.'
    ],
    vulnerable_groups: 'Pedestrians and farm laborers caught mid-transit between villages.',
    checklist: [
      'Drop into lowest nearby ditch or terrain depression',
      'Cover head and back of neck with hands',
      'Wait for storm intensity to abate before moving to pucca shelter'
    ]
  },
  {
    id: 'cyc-dur-05',
    hazard: 'CYCLONE',
    phase: 'DURING',
    category: 'WATER_AND_FOOD',
    title: 'Ration Drinking Water & Consume High-Energy Dry Food',
    instruction: 'Consume small, regular sips of clean water and eat energy-dense dry foods; do not open refrigerators repeatedly.',
    priority: 'RECOMMENDED',
    reason: 'Conserving hydration and stamina is essential; opening refrigerators lets cold air escape and spoils perishables within hours of power loss.',
    source: 'NDMA Food and Water Survival Guidance',
    related_cascading_risk: 'Food spoilage and acute dehydration.',
    practical_steps: [
      'Allocate drinking water strictly: 2 litres per adult per 24 hours.',
      'Eat puffed rice, biscuits, jaggery, and dry fruits that do not induce excessive thirst.',
      'Keep refrigerator door closed tightly to maintain internal cool temperature for 24 hours.',
      'Use pre-packed sterile baby formula for infants.'
    ],
    warning_signs: [
      'Dry mouth, headache, and dark concentrated urine indicating early dehydration.'
    ],
    what_not_to_do: [
      'Do NOT eat salty or excessively spicy foods that increase thirst.',
      'Do NOT open the refrigerator door unless absolutely necessary.'
    ],
    vulnerable_groups: 'Infants, pregnant mothers, and elderly persons.',
    checklist: [
      'Ration clean water bottles among family',
      'Distribute dry energy snacks at regular 4-hour intervals',
      'Keep refrigerator door sealed shut'
    ]
  },
  {
    id: 'cyc-dur-06',
    hazard: 'CYCLONE',
    phase: 'DURING',
    category: 'VULNERABLE_MEMBERS',
    title: 'Keep Children, Elders & Household Pets Calm in Interior Room',
    instruction: 'Reassure frightened children and elderly family members; keep pets leashed or in pet carriers beside you to prevent panic-induced bolting.',
    priority: 'RECOMMENDED',
    reason: 'The terrifying roar of cyclonic winds causes acute panic attacks, disorientation in dementia patients, and frantic bolting in domestic pets.',
    source: 'NDMA Psychological First Aid in Disasters Guidelines',
    related_cascading_risk: 'Loss of pets and acute cardiac/anxiety medical emergencies.',
    practical_steps: [
      'Engage children with storytelling, oral games, or simple puzzles to divert focus from wind noise.',
      'Keep soothing physical contact with anxious elders; ensure hearing aids are in place.',
      'Place pets inside secure plastic carriers or keep dogs on short leash beside family.',
      'Keep prescribed anti-anxiety or cardiac medications immediately at hand.'
    ],
    warning_signs: [
      'Hyperventilation, extreme trembling, or chest tightness in elderly family members.',
      'Pets whining, scratching walls, and attempting to force open doors.'
    ],
    what_not_to_do: [
      'Do NOT shout or display visible panic in front of children.',
      'Do NOT let pets loose outdoors during the storm.'
    ],
    vulnerable_groups: 'Young children under 8 years, elderly individuals with heart conditions, and domestic pets.',
    checklist: [
      'Keep children engaged with quiet games',
      'Ensure elder cardiac medications are beside bed',
      'Secure domestic pets inside crate or on leash'
    ]
  },

  // --- CYCLONE: AFTER ---
  {
    id: 'cyc-aft-01',
    hazard: 'CYCLONE',
    phase: 'AFTER',
    category: 'UTILITY_SAFETY',
    title: 'Watch for Fallen Live Electrical Wires & Snapped High-Tension Cables',
    instruction: 'Treat every fallen wire as LIVE and deadly; maintain a minimum 10-metre clearance and report immediately to electricity department helpline or 112.',
    priority: 'CRITICAL',
    reason: 'Snapping branches drag down 11 kV and 33 kV distribution lines onto roads, fences, and standing puddles; stepping within the voltage gradient field causes instant fatal electrocution.',
    source: 'Central Electricity Authority (CEA) Post-Cyclone Public Safety Alert',
    warning: 'Never touch a fallen wire, puddle near a wire, or metal chain-link fence in contact with power cables.',
    related_cascading_risk: 'Fatal step-potential electrocution and secondary substation explosions.',
    practical_steps: [
      'If you see a downed power cable, stop immediately and warn others to stay at least 10 metres (33 feet) away.',
      'If a power line falls on your vehicle, remain inside; honk horn for rescue. If compelled to exit due to fire, jump clear with feet together—never touch car and ground simultaneously.',
      'Do not walk through standing rainwater pools near fallen utility poles.',
      'Dial 112 or local power discom emergency cell to report the exact pole location.'
    ],
    warning_signs: [
      'Buzzing or hissing sound from wet ground or bushes.',
      'Arcing blue sparks or charred grass near fallen wire.'
    ],
    what_not_to_do: [
      'Do NOT attempt to move a fallen electrical cable using a dry stick, broom, or bamboo pole.',
      'Do NOT touch metal fences, gates, or street signposts near snapped utility wires.'
    ],
    vulnerable_groups: 'Curious children walking outdoors post-storm, cattle, and relief volunteers.',
    checklist: [
      'Maintain 10-metre buffer from all fallen utility wires',
      'Alert neighbors and place physical warning markers',
      'Call power department emergency number (1912 / 112)'
    ]
  },
  {
    id: 'cyc-aft-02',
    hazard: 'CYCLONE',
    phase: 'AFTER',
    category: 'DAMAGE_DOCUMENTATION',
    title: 'Photograph Roof & Structural Damage Before Moving Any Debris',
    instruction: 'Take clear date-stamped photographs and videos of all damaged roof sheets, collapsed walls, broken windows, and damaged property before cleanup.',
    priority: 'HIGH',
    reason: 'Under State Disaster Response Fund (SDRF) norms, revenue inspectors require visual photographic evidence to process house damage ex-gratia compensation.',
    source: 'Ministry of Home Affairs SDRF/NDRF Compensation Operational Guidelines',
    related_cascading_risk: 'Relief disbursement rejections and protracted compensation disputes.',
    practical_steps: [
      'Photograph wide-angle views showing house number and full facade.',
      'Take detailed close-up pictures of cracked load-bearing walls, sheared roof trusses, and destroyed water tanks.',
      'Photograph serial numbers and damage to motorized farm equipment or commercial stock.',
      'Preserve damaged receipts, tax bills, and repair estimates in your waterproof document pouch.'
    ],
    warning_signs: [
      'Local revenue patwari or village administrative officer (VAO) announcing door-to-door damage enumeration.'
    ],
    what_not_to_do: [
      'Do NOT dispose of damaged roofing sheets or timber before revenue inspection without photos.',
      'Do NOT falsify damage claims.'
    ],
    vulnerable_groups: 'Marginalized families unfamiliar with government relief documentation processes.',
    checklist: [
      'Take 10+ clear photos of all exterior and interior damage',
      'Record 2-minute video walkthrough showing house number',
      'Submit formal damage claim form to local Gram Panchayat / Tahsildar'
    ]
  },
  {
    id: 'cyc-aft-03',
    hazard: 'CYCLONE',
    phase: 'AFTER',
    category: 'WATER_AND_FOOD',
    title: 'Boil Tap Water or Use Chlorine Tablets; Discard Rain-Exposed Food',
    instruction: 'Boil all drinking water vigorously for 1 minute; discard cooked food left unrefrigerated for over 4 hours or exposed to cyclonic spray.',
    priority: 'CRITICAL',
    reason: 'Storm surge inundation and broken municipal water mains allow contaminated runoff to infiltrate drinking water lines, triggering post-cyclone cholera outbreaks.',
    source: 'NCDC Post-Disaster Health Protocol',
    related_cascading_risk: 'Post-cyclone cholera, acute diarrheal disease, and hepatitis A epidemics.',
    practical_steps: [
      'Boil all water used for drinking, cooking, and brushing teeth for at least 60 seconds.',
      'Use 1 chlorine tablet (33 mg) per 10 litres of water; let stand for 30 minutes before use.',
      'Discard any food that has a strange odor, color, or texture.',
      'Wash canned foods thoroughly before opening.'
    ],
    warning_signs: [
      'Tap water coming out muddy, brown, or with salty brackish taste.',
      'Diarrhea or vomiting symptoms in family members.'
    ],
    what_not_to_do: [
      'Do NOT drink water from open coastal wells contaminated by seawater surge.',
      'Do NOT consume unrefrigerated meat or dairy products post-blackout.'
    ],
    vulnerable_groups: 'Infants, young children, and elderly citizens.',
    checklist: [
      'Boil all household drinking water for 60 seconds',
      'Add chlorine tablets to stored domestic water tanks',
      'Discard spoiled perishable food from refrigerator'
    ]
  },
  {
    id: 'cyc-aft-04',
    hazard: 'CYCLONE',
    phase: 'AFTER',
    category: 'TRANSPORTATION',
    title: 'Avoid Entering Waterlogged Coastal Arterials with Uprooted Trees',
    instruction: 'Do not travel on coastal highways until local road administration (PWD / NHAI) has cleared uprooted trees and verified bridge safety.',
    priority: 'HIGH',
    reason: 'Heavy banyan trees and snapped power poles block rural roads; submerged bridge culverts may have suffered scouring and sudden collapse under vehicle weight.',
    source: 'National Highways Authority of India (NHAI) Disaster Protocol',
    related_cascading_risk: 'Vehicle entrapment, secondary road collisions, and blocking NDRF convoys.',
    practical_steps: [
      'Check local traffic police radio advisories before embarking on any essential journey.',
      'Give right-of-way immediately to NDRF, SDRF, electricity board, and ambulance convoys.',
      'Carry a small hand-saw, tow rope, and flashlight in car boot for emergency clearance.',
      'Do not attempt to cross bridges with turbulent water touching the girder level.'
    ],
    warning_signs: [
      'PWD road barrier signs or tree trunks blocking lanes.',
      'Bridge approaches showing erosion gullies on shoulders.'
    ],
    what_not_to_do: [
      'Do NOT drive on closed highways to go sight-seeing or take photos of coastal devastation.',
      'Do NOT move road-closed barriers placed by emergency teams.'
    ],
    vulnerable_groups: 'Long-distance truckers and motorcycle delivery riders.',
    checklist: [
      'Verify road clearance status on local administration portal',
      'Yield right-of-way to emergency repair vehicles',
      'Keep travel limited strictly to medical emergencies'
    ]
  },
  {
    id: 'cyc-aft-05',
    hazard: 'CYCLONE',
    phase: 'AFTER',
    category: 'MEDICAL_AND_HEALTH',
    title: 'Check Neighbors, Elders & Infants for Hypothermia or Trauma Injuries',
    instruction: 'Visit neighboring homes, especially elderly residents living alone; inspect family members for puncture wounds, hypothermia, or shock.',
    priority: 'RECOMMENDED',
    reason: 'Prolonged exposure to drenching cyclonic rains and freezing winds induces severe hypothermia in infants and bedridden elders; rusted metal cuts cause tetanus.',
    source: 'Indian Red Cross Society First Aid Manual',
    related_cascading_risk: 'Hypothermia fatalities and untreated infected wound complications.',
    practical_steps: [
      'Provide dry woollen blankets, warm tea, and dry clothes to shivering elders and children.',
      'Clean all minor cuts and abrasions with antiseptic liquid (Savlon/Dettol); apply sterile dressing.',
      'Take any person with deep punctures or rust cuts to the nearest PHC for a Tetanus Toxoid injection within 24 hours.',
      'Provide emotional reassurance to shocked or distressed neighbors.'
    ],
    warning_signs: [
      'Shivering, slurred speech, cold pale skin, or confusion indicating hypothermia.',
      'Redness, throbbing pain, or pus from puncture wounds.'
    ],
    what_not_to_do: [
      'Do NOT ignore small cuts sustained while handling rusted corrugated tin sheets.',
      'Do NOT leave solitary elders unchecked in damaged coastal homes.'
    ],
    vulnerable_groups: 'Elderly citizens living alone, infants, and destitute families.',
    checklist: [
      'Conduct neighborhood check on elderly residents',
      'Administer first aid and clean wounds with antiseptic',
      'Visit PHC for tetanus injection within 24 hours of cut'
    ]
  },
  {
    id: 'cyc-aft-06',
    hazard: 'CYCLONE',
    phase: 'AFTER',
    category: 'SANITATION',
    title: 'Register Damage Claim with Gram Panchayat / Revenue Inspector',
    instruction: 'Submit your formal calamity relief application along with photo evidence, Aadhaar copy, and bank account passbook to the local Tahsildar / Block Development Officer.',
    priority: 'RECOMMENDED',
    reason: 'Statutory ex-gratia assistance under SDRF guidelines is disbursed directly into verified Aadhaar-linked bank accounts through DBT following field survey verification.',
    source: 'State Disaster Management Authority Relief Administration SOP',
    related_cascading_risk: 'Exclusion from government relief packages due to missed filing deadlines.',
    practical_steps: [
      'Collect the official Calamity Damage Enumeration Form from village administrative officer or online portal.',
      'Attach printed damage photos, Aadhaar photocopy, ration card copy, and bank passbook with IFSC code.',
      'Obtain a dated receipt or acknowledgment slip with reference number from the receiving official.',
      'Track enumeration team visits to your ward for on-site physical verification.'
    ],
    warning_signs: [
      'Panchayat announcement of last date for submitting cyclone damage claims.'
    ],
    what_not_to_do: [
      'Do NOT pay bribes or deal with unauthorized middlemen promising inflated relief.',
      'Do NOT miss the statutory filing window (usually 15-30 days post-calamity).'
    ],
    vulnerable_groups: 'Illiterate households requiring assistance filling administrative forms.',
    checklist: [
      'Fill government calamity relief application form',
      'Attach photo proof, Aadhaar, and bank passbook copies',
      'Retain official dated acknowledgment receipt'
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
    category: 'PROPERTY_PREPARATION',
    title: 'Insulate Roofs with Reflective White Paint & Install Bamboo Screens',
    instruction: 'Apply solar-reflective cool-roof white paint or lime wash on terrace roofs; hang wet khus-khus or bamboo mats (chicks) over sun-facing windows.',
    priority: 'HIGH',
    reason: 'Uninsulated concrete roofs absorb intense solar radiation, radiating temperatures of 55°C+ into living quarters and trapping indoor heat overnight.',
    source: 'NDMA National Heat Wave Action Plan Guidelines',
    related_cascading_risk: 'Indoor heat trap syndrome, nocturnal heat stroke, and urban heat island amplification.',
    practical_steps: [
      'Apply two coats of solar-reflective lime wash or elastomeric high-albedo white paint on exposed terrace roofs.',
      'Hang wet vetiver (khus-khus) or bamboo chick blinds on western and southern windows.',
      'Keep curtains and dark blinds drawn closed during daylight hours (09:00 to 18:00) to block radiant solar flux.',
      'Open windows at night to establish cross-ventilation once ambient outdoor air cools.'
    ],
    warning_signs: [
      'Ceiling fan blowing searing hot air even at midnight.',
      'Terrace floor slab burning hot to the touch well after sunset.'
    ],
    what_not_to_do: [
      'Do NOT sleep directly beneath an uninsulated concrete roof on top-floor rooms during peak heatwave.',
      'Do NOT leave south-facing windows unshaded during midday solar peak.'
    ],
    vulnerable_groups: 'Residents of top-floor apartments, tin-shed houses, and informal settlements.',
    checklist: [
      'Apply white reflective coating on terrace slab',
      'Install shade blinds on south and west windows',
      'Ensure cross-ventilation pathways are open for night cooling'
    ]
  },
  {
    id: 'htw-bef-02',
    hazard: 'HEATWAVE',
    phase: 'BEFORE',
    category: 'WATER_AND_FOOD',
    title: 'Hydrate Actively with Oral Electrolytes, Chaas & Lemon Water',
    instruction: 'Drink 3 to 4 litres of fluids daily even before feeling thirsty; consume buttermilk (chaas), lemon water with salt, coconut water, and aam panna.',
    priority: 'CRITICAL',
    reason: 'Profuse sweating rapidly depletes essential sodium and potassium ions; plain water alone cannot prevent heat exhaustion without electrolyte replenishment.',
    source: 'Ministry of Health & Family Welfare Heatwave Health Advisory',
    warning: 'Thirst is a delayed symptom of dehydration; by the time you feel thirsty, body water deficit has already reached 2%.',
    related_cascading_risk: 'Acute electrolyte imbalance, heat cramps, and acute renal failure.',
    practical_steps: [
      'Drink a glass of water every 30 to 45 minutes even without thirst sensation.',
      'Prepare traditional cooling electrolyte drinks: buttermilk with roasted cumin and salt, aam panna, or lemon-sugar-salt solution.',
      'Carry a reusable insulated water bottle whenever stepping out of the house.',
      'Keep ORS (Oral Rehydration Salts) sachets readily accessible in household medicine drawer.'
    ],
    warning_signs: [
      'Dark amber urine indicating severe fluid deficit.',
      'Dry mouth, headache, lightheadedness, and lethargy.'
    ],
    what_not_to_do: [
      'Do NOT consume alcohol, carbonated soft drinks, or excessive caffeinated tea/coffee; they act as diuretics and accelerate dehydration.',
      'Do NOT consume chilled ice water immediately after coming in from scorching sun.'
    ],
    vulnerable_groups: 'Elderly persons who have diminished biological thirst sensation, infants, and pregnant women.',
    checklist: [
      'Drink 3-4 litres of water and oral electrolytes daily',
      'Prepare salted buttermilk or lemon water jug in kitchen',
      'Monitor urine color (aim for clear or pale yellow)'
    ]
  },
  {
    id: 'htw-bef-03',
    hazard: 'HEATWAVE',
    phase: 'BEFORE',
    category: 'TRANSPORTATION',
    title: 'Reschedule Outdoor Labor & Farming to Early Morning & Late Evening',
    instruction: 'Shift strenuous outdoor construction work, agricultural harvesting, and sports training to 06:00–10:00 and post-17:00; avoid midday solar peak.',
    priority: 'CRITICAL',
    reason: 'Heavy physical exertion during peak wet-bulb temperatures overwhelms the human thermoregulatory mechanism, causing body temperature to spike past 40°C in under 30 minutes.',
    source: 'Ministry of Labour & Employment Heat Advisory & NDMA Guidelines',
    related_cascading_risk: 'Exertional heat stroke, worker collapse, and loss of livelihood.',
    practical_steps: [
      'Commence farming, harvesting, and masonry work at dawn (05:30 to 09:30).',
      'Enforce mandatory 20-minute shaded rest breaks every hour during hot hours.',
      'Wear wide-brimmed straw hats, damp towels (gamchas) over neck, and loose cotton clothing.',
      'Provide cold potable water and ORS at all active work sites under shade.'
    ],
    warning_signs: [
      'IMD issuing Yellow or Orange Heatwave bulletin with maximum temperatures exceeding 42°C (40°C in coastal areas).',
      'Muscle cramps in calves and abdomen during physical work.'
    ],
    what_not_to_do: [
      'Do NOT work continuously in direct midday sunlight between 11:00 and 16:00.',
      'Do NOT allow school children to conduct outdoor physical sports training during heatwave alerts.'
    ],
    vulnerable_groups: 'Daily wage construction laborers, MNREGA workers, farmers, traffic police, and rickshaw pullers.',
    checklist: [
      'Shift work schedule to early morning hours',
      'Wear wide-brimmed hat and damp cotton head cloth',
      'Set up shaded hydration station at work site'
    ]
  },
  {
    id: 'htw-bef-04',
    hazard: 'HEATWAVE',
    phase: 'BEFORE',
    category: 'PETS_AND_LIVESTOCK',
    title: 'Provide Shaded Enclosures & Abundant Water for Domestic Livestock & Pets',
    instruction: 'Ensure cattle, goats, and domestic pets have unlimited access to cool drinking water and shaded tree groves; wash cattle twice daily with cool water.',
    priority: 'HIGH',
    reason: 'Dairy cattle suffer acute heat stress at Temperature-Humidity Index (THI) > 72, leading to sudden drop in milk yield, panting, and fatal heat stroke.',
    source: 'Department of Animal Husbandry Advisory on Summer Heat Stress Management',
    related_cascading_risk: 'Livestock mortality and severe rural dairy economic loss.',
    practical_steps: [
      'Provide continuous fresh water in large earthen or cement troughs under thatched tree shade.',
      'Sprinkle or splash cool water on dairy cattle during peak afternoon hours (12:00 to 14:00).',
      'Feed cattle green fodder and mineral supplements during cool early morning and evening hours.',
      'Keep domestic dogs and cats indoors in well-ventilated tiled rooms; never leave them tied in sunny yards.'
    ],
    warning_signs: [
      'Cattle panting with tongues protruding and drooling thick saliva.',
      'Domestic dogs panting rapidly with glassy eyes and inability to stand.'
    ],
    what_not_to_do: [
      'Do NOT graze cattle in open pasture fields between 11:00 and 16:00 during heatwave alerts.',
      'Do NOT tie pets in unshaded metal sheds or on hot asphalt driveways.'
    ],
    vulnerable_groups: 'Cross-bred jersey cows, pregnant livestock, and brachycephalic dog breeds (pugs, bulldogs).',
    checklist: [
      'Keep water troughs filled with clean water under shade',
      'Splash cattle with water twice daily during afternoon',
      'Keep domestic pets indoors in cool rooms'
    ]
  },
  {
    id: 'htw-bef-05',
    hazard: 'HEATWAVE',
    phase: 'BEFORE',
    category: 'VULNERABLE_MEMBERS',
    title: 'Check on Solitary Elders, Chronic Patients & Children Daily',
    instruction: 'Establish daily check-ins with elderly neighbors living alone, bedridden patients, and households with newborns; ensure fans and cooling water are operating.',
    priority: 'HIGH',
    reason: 'Seniors have impaired thermoregulation, reduced sweating response, and frequently take cardiovascular medications (diuretics, beta-blockers) that worsen dehydration.',
    source: 'NDMA Heat Action Plan Community Outreach Module',
    related_cascading_risk: 'Silent indoor heat stroke fatalities among isolated elderly citizens.',
    practical_steps: [
      'Visit or call elderly relatives and neighbors at least twice daily (midday and evening).',
      'Ensure their living space has working ceiling fans or coolers and adequate drinking water within arm’s reach.',
      'Check if they are taking diuretic or antihypertensive medications; consult doctor about dosage adjustments during severe heat.',
      'Encourage elders to take cool sponge baths twice daily.'
    ],
    warning_signs: [
      'Elderly relative appearing unusually drowsy, confused, or unresponsive.',
      'Dry tongue, sunken eyes, and absence of urination for over 8 hours.'
    ],
    what_not_to_do: [
      'Do NOT leave elderly persons confined in closed, unventilated top-floor rooms without fans.',
      'Do NOT assume that because they do not ask for water, they are not thirsty.'
    ],
    vulnerable_groups: 'Seniors over 65 years, Alzheimer’s/dementia patients, and bedridden individuals.',
    checklist: [
      'Schedule 2x daily check-ins with elderly relatives',
      'Verify ceiling fan or desert cooler is operating',
      'Place water pitcher and ORS bottle beside their bed'
    ]
  },
  {
    id: 'htw-bef-06',
    hazard: 'HEATWAVE',
    phase: 'BEFORE',
    category: 'POWER_AND_LIGHTING',
    title: 'Conserve Electricity Peak Load & Maintain Backup Cooling Fans',
    instruction: 'Avoid running high-wattage appliances (washing machines, geysers) during peak grid hours (14:00–18:00); keep hand fans and battery emergency fans charged.',
    priority: 'RECOMMENDED',
    reason: 'Extreme widespread air conditioner usage overloads distribution transformers, causing localized substation trips and blackouts during the hottest hours.',
    source: 'Central Electricity Authority (CEA) Peak Load Management Advisory',
    related_cascading_risk: 'Power grid tripping, localized blackouts, and loss of refrigeration.',
    practical_steps: [
      'Set air conditioners to 24°C–26°C with ceiling fan on; this saves up to 25% power while maintaining thermal comfort.',
      'Run heavy electrical appliances during early morning or late night hours.',
      'Keep rechargeable portable fans and traditional palm-leaf hand fans ready for power cuts.',
      'Keep mobile phones charged and maintain backup ice packs in freezer.'
    ],
    warning_signs: [
      'Frequent voltage drops and dimming lights during hot afternoons.',
      'Power discom issuing advisory on high grid demand.'
    ],
    what_not_to_do: [
      'Do NOT set AC thermostat to 16°C or 18°C; it does not cool faster and drastically overloads the compressor.',
      'Do NOT leave appliances running in empty rooms.'
    ],
    vulnerable_groups: 'Urban populations dependent entirely on mechanical cooling during heatwaves.',
    checklist: [
      'Set AC temperature to 24°C–26°C with ceiling fan',
      'Charge portable emergency battery fans',
      'Keep traditional hand fans accessible in all rooms'
    ]
  },

  // --- HEATWAVE: DURING ---
  {
    id: 'htw-dur-01',
    hazard: 'HEATWAVE',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Avoid Direct Sun Exposure from 11:00 to 16:00 (Peak UV Hours)',
    instruction: 'Remain indoors in shaded, cool rooms during the peak solar radiation window between 11:00 and 16:00; wear broad-brimmed hats and cotton clothing if stepping out.',
    priority: 'CRITICAL',
    reason: 'Solar radiation and UV indices peak sharply between 11:00 and 16:00, causing rapid skin erythema, core temperature escalation, and heat cramps.',
    source: 'IMD & NDMA Public Safety Advisory',
    related_cascading_risk: 'Acute heat exhaustion, sun stroke, and severe sunburns.',
    practical_steps: [
      'Schedule all grocery shopping, banking, and errands before 10:00 or after 17:30.',
      'If compelled to venture out, cover head, face, and neck with a damp cotton cloth (gamcha) or umbrella.',
      'Wear loose, lightweight, light-colored cotton garments to facilitate sweat evaporation.',
      'Apply broad-spectrum sunscreen (SPF 30+) on exposed face, ears, and hands.'
    ],
    warning_signs: [
      'Heat index (feels-like temperature) exceeding 45°C.',
      'Blistering heat waves shimmering above asphalt road surfaces.'
    ],
    what_not_to_do: [
      'Do NOT go for afternoon jogs, cycling, or recreational outdoor walks between 11:00 and 16:00.',
      'Do NOT wear tight, dark, or synthetic polyester clothes that trap metabolic body heat.'
    ],
    vulnerable_groups: 'Couriers, food delivery executives, construction workers, and street vendors.',
    checklist: [
      'Stay indoors between 11:00 and 16:00',
      'Carry umbrella and water bottle if outdoors',
      'Wear light-colored loose cotton clothing'
    ]
  },
  {
    id: 'htw-dur-02',
    hazard: 'HEATWAVE',
    phase: 'DURING',
    category: 'MEDICAL_AND_HEALTH',
    title: 'Recognize Heat Stroke Warning Signs (Medical Emergency)',
    instruction: 'Recognize critical heat stroke symptoms: body temperature >40°C (104°F), cessation of sweating, hot red dry skin, confusion, vomiting, or seizures. Call 108 immediately.',
    priority: 'CRITICAL',
    reason: 'Heat stroke is a life-threatening medical emergency with up to 50% mortality if core body temperature is not reduced within 30 minutes; it causes permanent brain and kidney damage.',
    source: 'National Centre for Disease Control (NCDC) Heat Stroke Management Protocol',
    warning: 'Unlike heat exhaustion (where victim sweats heavily), heat stroke causes thermoregulatory failure where sweating completely STOPS and skin becomes hot and bone-dry.',
    related_cascading_risk: 'Multi-organ failure, coma, and emergency hospital ICU overload.',
    practical_steps: [
      'Call emergency ambulance (108) immediately; state that victim is suffering from suspected heat stroke.',
      'Move patient immediately to cool shaded room or air-conditioned vehicle.',
      'Remove excess clothing; spray or sponge victim with cool (not freezing) water.',
      'Apply ice packs or cold wet towels to armpits, groin, neck, and back where major blood vessels lie close to skin.',
      'Fan victim vigorously to maximize evaporative heat loss; do NOT force-feed fluids if victim is unconscious.'
    ],
    warning_signs: [
      'High core body temperature above 40°C (104°F).',
      'Confusion, agitation, slurred speech, delirium, or loss of consciousness.',
      'Hot, dry, flushed skin with complete absence of sweat.'
    ],
    what_not_to_do: [
      'Do NOT give oral fluids, ORS, or aspirin/paracetamol to an unconscious or vomiting victim.',
      'Do NOT submerge victim in ice water tub (causes peripheral vasoconstriction and shivering, trapping core heat).'
    ],
    vulnerable_groups: 'Elderly persons, outdoor manual laborers, athletes, and young children.',
    checklist: [
      'Dial 108 ambulance immediately',
      'Move victim to shade and remove outer clothing',
      'Apply cold packs to neck, armpits, and groin',
      'Fan vigorously and monitor breathing'
    ]
  },
  {
    id: 'htw-dur-03',
    hazard: 'HEATWAVE',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Never Leave Children, Elders, or Pets Locked Inside Parked Vehicles',
    instruction: 'Never leave children, elderly family members, or pets unattended in parked cars even for 5 minutes, even with windows cracked open.',
    priority: 'CRITICAL',
    reason: 'Greenhouse effect inside an enclosed parked car causes internal cabin temperature to skyrocket from 35°C to over 55°C in under 15 minutes, causing fatal pediatric heat stroke.',
    source: 'National Highway Traffic Safety & NDMA Child Safety Advisory',
    warning: 'Cracking windows open reduces interior vehicle heating by less than 2°C; car interiors become death traps.',
    related_cascading_risk: 'Fatal vehicular hyperthermia and pediatric cardiac arrest.',
    practical_steps: [
      'Always check the rear seat before locking your car (Look Before You Lock protocol).',
      'Keep a teddy bear or shoe in the passenger seat as a visual reminder that a child is in the back.',
      'Keep car doors locked when parked at home so young children cannot climb inside during play.',
      'If you see an unattended child or pet in a locked car on a hot day, seek owner or alert police immediately.'
    ],
    warning_signs: [
      'Child or pet panting, flushed, sweating profusely or unresponsive inside vehicle.'
    ],
    what_not_to_do: [
      'Do NOT leave child or pet in car while running a "quick" errand inside a shop.',
      'Do NOT rely on open sunroofs or cracked windows to keep car interior cool.'
    ],
    vulnerable_groups: 'Infants and toddlers who cannot unbuckle child seats, and domestic pets.',
    checklist: [
      'Adopt "Look Before You Lock" routine every time',
      'Place essential bag/phone in rear seat as reminder',
      'Keep parked vehicle locked to prevent children entering'
    ]
  },
  {
    id: 'htw-dur-04',
    hazard: 'HEATWAVE',
    phase: 'DURING',
    category: 'WATER_AND_FOOD',
    title: 'Emergency First Aid for Heat Exhaustion (Heavy Sweating, Dizziness)',
    instruction: 'For heat exhaustion (heavy sweating, paleness, muscle cramps, dizziness, nausea): move victim to shade, loosen clothing, and administer sips of cool salted water or ORS.',
    priority: 'HIGH',
    reason: 'Prompt first aid prevents heat exhaustion from escalating into life-threatening heat stroke.',
    source: 'Indian Red Cross Society First Aid Protocol for Heat Casualties',
    related_cascading_risk: 'Progression to full heat stroke if untreated within 30 minutes.',
    practical_steps: [
      'Lead or carry victim into an air-conditioned room, shaded porch, or under dense tree canopy.',
      'Have victim lie down flat with legs slightly elevated (30 cm) to facilitate blood return to brain.',
      'Loosen tight belts, collars, and shoes; unbutton shirt.',
      'Administer half a glass of cool water mixed with pinch of salt or ORS every 15 minutes for 1 hour.',
      'If vomiting persists or condition fails to improve within 45 minutes, transport to hospital.'
    ],
    warning_signs: [
      'Pale, cool, clammy skin with profuse perspiration.',
      'Fast weak pulse, dizziness upon standing, and muscle cramps.'
    ],
    what_not_to_do: [
      'Do NOT allow victim to resume strenuous outdoor work on the same day.',
      'Do NOT force large gulps of water that induce vomiting.'
    ],
    vulnerable_groups: 'Traffic constables, security guards, delivery couriers, and outdoor sports persons.',
    checklist: [
      'Move victim to shaded, cool environment',
      'Elevate legs 30 cm and loosen tight clothing',
      'Give slow sips of ORS or salted lemon water'
    ]
  },
  {
    id: 'htw-dur-05',
    hazard: 'HEATWAVE',
    phase: 'DURING',
    category: 'SHELTER',
    title: 'Utilize Public Cooling Centers, Temples & Shaded Community Hubs',
    instruction: 'If household lacks fans or air conditioning, spend the hottest afternoon hours (12:00–16:00) in public cooling shelters, shaded temples, libraries, or shopping complexes.',
    priority: 'RECOMMENDED',
    reason: 'Spending just 2 to 3 hours in an air-conditioned or well-ventilated public building significantly lowers core body temperature and prevents cumulative heat stress.',
    source: 'Ahmedabad Heat Action Plan & NDMA Guidelines',
    related_cascading_risk: 'Cumulative nocturnal heat strain and household heat traps.',
    practical_steps: [
      'Identify designated civic cooling centers or air-conditioned public facilities in your ward.',
      'Community halls, libraries, religious institutions, and shopping malls offer shaded thermal relief.',
      'Carry your own water bottle and medication kit when visiting public cooling centers.',
      'Help transport elderly neighbors from top-floor tin-roof rooms to shaded ground-floor community centers.'
    ],
    warning_signs: [
      'Indoor room temperature exceeding 38°C with stagnant air.'
    ],
    what_not_to_do: [
      'Do NOT stay isolated in sweltering top-floor rooms out of hesitation to use public cooling shelters.',
      'Do NOT leave bedridden elders unattended in stifling rooms.'
    ],
    vulnerable_groups: 'Slum dwellers, tin-roof occupants, and unhoused citizens.',
    checklist: [
      'Locate nearest free public cooling space in ward',
      'Spend 12:00-16:00 in shaded or cooled facility',
      'Bring hydration bottle and prescription medicines'
    ]
  },
  {
    id: 'htw-dur-06',
    hazard: 'HEATWAVE',
    phase: 'DURING',
    category: 'WATER_AND_FOOD',
    title: 'Prepare Fresh Food & Avoid Heavy, Oily, Protein-Dense Meals',
    instruction: 'Eat small, frequent meals consisting of fresh fruits (watermelon, cucumber, muskmelon), curd, and light lentils; avoid stale food and heavy fried meats.',
    priority: 'RECOMMENDED',
    reason: 'Digesting heavy protein and fat-dense meals significantly increases metabolic heat production (diet-induced thermogenesis), raising body temperature internally.',
    source: 'FSSAI Summer Nutrition Guidelines',
    related_cascading_risk: 'Acute gastroenteritis and metabolic heat overload.',
    practical_steps: [
      'Consume seasonal high-water fruits: watermelon, cucumber, muskmelon, oranges, gourds.',
      'Eat freshly cooked light khichdi, rice, curd, and moong dal.',
      'Do not eat food left out at room temperature for more than 2 hours; summer bacterial growth is exponential.',
      'Store cooked food in refrigerator or clean cool pantry.'
    ],
    warning_signs: [
      'Food showing sour smell, curdling, or surface bubbles.',
      'Abdominal bloating and sluggishness after heavy meals.'
    ],
    what_not_to_do: [
      'Do NOT consume heavy deep-fried pakoras, samosas, or high-fat street food during heatwaves.',
      'Do NOT consume cut fruits sold open to flies on roadside carts.'
    ],
    vulnerable_groups: 'Children and seniors with sensitive digestive systems.',
    checklist: [
      'Include fresh watermelon, cucumber, and curd in diet',
      'Eat light meals and avoid deep-fried foods',
      'Refrigerate or consume cooked food within 2 hours'
    ]
  },

  // --- HEATWAVE: AFTER ---
  {
    id: 'htw-aft-01',
    hazard: 'HEATWAVE',
    phase: 'AFTER',
    category: 'RECOVERY_AND_HEALTH',
    title: 'Continue Active Electrolyte Hydration Even After Temperatures Drop',
    instruction: 'Continue drinking 2.5 to 3 litres of water and oral electrolytes daily for at least 48 hours following a heatwave; full physiological recovery takes several days.',
    priority: 'HIGH',
    reason: 'Cellular dehydration and sub-clinical electrolyte deficits persist for several days after ambient temperature falls; resuming normal activity too quickly can trigger secondary collapse.',
    source: 'NCDC Post-Heatwave Clinical Guidelines',
    related_cascading_risk: 'Secondary heat exhaustion relapse and persistent muscular fatigue.',
    practical_steps: [
      'Keep consuming ORS, salted buttermilk, and coconut water for 2 days post-heatwave.',
      'Get 8 hours of restful sleep in a well-ventilated cool room to allow cellular rehydration.',
      'Avoid immediately engaging in extreme physical workouts or long marathons.',
      'Monitor urine color until it remains consistently pale yellow.'
    ],
    warning_signs: [
      'Lingering headache, muscle cramps, and profound physical exhaustion post-event.'
    ],
    what_not_to_do: [
      'Do NOT abruptly halt extra hydration the moment daytime temperatures dip slightly.',
      'Do NOT consume dehydrating alcoholic drinks to celebrate the end of a heatwave.'
    ],
    vulnerable_groups: 'Outdoor workers recovering from heat exhaustion.',
    checklist: [
      'Continue drinking 3 litres of water + electrolytes daily',
      'Allow 48 hours of physical rest before heavy exertion',
      'Verify urine color has normalized to pale straw yellow'
    ]
  },
  {
    id: 'htw-aft-02',
    hazard: 'HEATWAVE',
    phase: 'AFTER',
    category: 'PROPERTY_PREPARATION',
    title: 'Inspect & Clean Earthen Coolers, AC Filters & Water Storage Tanks',
    instruction: 'Drain, scrub, and dry desert coolers to prevent mosquito breeding; wash air-conditioner mesh filters to restore cooling airflow and energy efficiency.',
    priority: 'HIGH',
    reason: 'Stagnant water in desert coolers and overhead tanks becomes a primary breeding ground for Aedes aegypti mosquitoes, sparking dengue outbreaks immediately following summer heat.',
    source: 'NVBDCP National Dengue Prevention Advisory',
    related_cascading_risk: 'Post-summer dengue and chikungunya epidemics.',
    practical_steps: [
      'Empty the water sump of all desert coolers completely once a week (Dry Day routine).',
      'Scrub cooler tank with brush and bleach to kill mosquito eggs clinging to sides.',
      'Clean dust and lint from air-conditioner indoor filters under running tap water.',
      'Inspect domestic overhead Sintex tanks; ensure airtight lids are locked.'
    ],
    warning_signs: [
      'Wriggling mosquito larvae visible in desert cooler tank water.',
      'Air conditioner blowing weak airflow with musty odor.'
    ],
    what_not_to_do: [
      'Do NOT leave water sitting in unused desert coolers when heatwave ends.',
      'Do NOT leave overhead water tanks uncovered.'
    ],
    vulnerable_groups: 'Residents of urban residential colonies using evaporative desert coolers.',
    checklist: [
      'Empty and scrub desert cooler water tanks',
      'Wash AC filters under running tap water',
      'Verify overhead water tank lids are sealed tight'
    ]
  },
  {
    id: 'htw-aft-03',
    hazard: 'HEATWAVE',
    phase: 'AFTER',
    category: 'WATER_AND_FOOD',
    title: 'Inspect Refrigerator Food Stored During Power Brownouts',
    instruction: 'Inspect refrigerated meats, milk, cooked gravies, and eggs that may have thawed during summer power outages; discard any items showing spoilage.',
    priority: 'RECOMMENDED',
    reason: 'Frequent transformer brownouts cause refrigerator temperatures to rise above 8°C, accelerating rapid bacterial growth in dairy and meat products.',
    source: 'FSSAI Food Safety in Emergencies Advisory',
    related_cascading_risk: 'Food poisoning outbreaks and acute salmonellosis.',
    practical_steps: [
      'Check temperature of dairy milk and cooked curries; if sour, curdled, or smelling abnormal, discard immediately.',
      'Do not refreeze thawed raw poultry or fish that has reached room temperature.',
      'Sanitize refrigerator shelves with warm water and baking soda or mild bleach.',
      'Restock with fresh groceries once power supply has fully stabilized.'
    ],
    warning_signs: [
      'Sour odor, slimy film, or off-color on dairy and cooked meat products.'
    ],
    what_not_to_do: [
      'Do NOT taste food to test if it has spoiled; foodborne toxins can be odorless and tasteless.',
      'Do NOT feed spoiled refrigerated food to household pets.'
    ],
    vulnerable_groups: 'Families with young children and elderly grandparents.',
    checklist: [
      'Inspect refrigerated dairy and cooked items',
      'Discard thawed meats left above 8°C for over 4 hours',
      'Clean interior refrigerator shelves with mild sanitizer'
    ]
  },
  {
    id: 'htw-aft-04',
    hazard: 'HEATWAVE',
    phase: 'AFTER',
    category: 'PETS_AND_LIVESTOCK',
    title: 'Monitor Livestock for Delayed Heat Stress & Replenish Fodder Salts',
    instruction: 'Provide mineral licks and salt supplements to dairy cattle; watch for delayed respiratory infections or sharp drops in milk yield.',
    priority: 'RECOMMENDED',
    reason: 'Sustained heat stress suppresses bovine immunity, leading to post-heatwave mastitis, pneumonia, and prolonged reproductive anestrus.',
    source: 'National Dairy Development Board (NDDB) Advisory',
    related_cascading_risk: 'Secondary livestock bacterial infections and dairy economic losses.',
    practical_steps: [
      'Add mineral mixture and salt (50 grams/animal/day) to cattle drinking water and feed.',
      'Inspect cow udders for heat swelling or early signs of mastitis.',
      'Provide clean green fodder to stimulate rumination and restore electrolyte balance.',
      'Consult local veterinary assistant surgeon if cattle show persistent fever or loss of appetite.'
    ],
    warning_signs: [
      'Cow milk yield remaining more than 20% below pre-heatwave baseline.',
      'Cattle coughing or showing nasal discharge.'
    ],
    what_not_to_do: [
      'Do NOT force dairy cows into long walking journeys under direct sun immediately following a heatwave.',
      'Do NOT neglect mineral supplementation in livestock feed.'
    ],
    vulnerable_groups: 'Dairy farmers and rural livestock owners.',
    checklist: [
      'Add mineral mixture and salt to cattle feed',
      'Check dairy cows for normal milk production',
      'Consult local veterinary doctor for persistent lethargy'
    ]
  },
  {
    id: 'htw-aft-05',
    hazard: 'HEATWAVE',
    phase: 'AFTER',
    category: 'RECOVERY_AND_HEALTH',
    title: 'Seek Medical Evaluation for Persistent Dizziness or Dark Urine',
    instruction: 'Visit a physician or Primary Health Centre if you experience persistent muscle weakness, nausea, confusion, or dark brown urine post-heatwave.',
    priority: 'HIGH',
    reason: 'Severe heat stress can induce rhabdomyolysis (breakdown of damaged skeletal muscle releasing myoglobin into blood), causing acute kidney injury if untreated.',
    source: 'Ministry of Health & Family Welfare Clinical Protocol',
    related_cascading_risk: 'Acute renal failure and chronic kidney damage.',
    practical_steps: [
      'Visit nearest PHC or hospital outpatient clinic.',
      'Request routine blood urea, serum creatinine, and urine analysis.',
      'Inform the doctor of your heatwave exposure duration and outdoor exertion level.',
      'Continue aggressive oral hydration with plain water and electrolyte solutions under medical advice.'
    ],
    warning_signs: [
      'Tea-colored or cola-colored dark urine.',
      'Profound muscle soreness in thighs and back with inability to walk.'
    ],
    what_not_to_do: [
      'Do NOT take over-the-counter NSAID painkillers (ibuprofen, diclofenac) without medical advice; they severely worsen heat-induced kidney damage.',
      'Do NOT ignore reduced urine volume.'
    ],
    vulnerable_groups: 'Marathon runners, construction laborers, and military recruits.',
    checklist: [
      'Monitor urine color and daily output volume',
      'Avoid NSAID painkiller self-medication',
      'Get serum creatinine test if dark urine persists'
    ]
  },
  {
    id: 'htw-aft-06',
    hazard: 'HEATWAVE',
    phase: 'AFTER',
    category: 'PROPERTY_PREPARATION',
    title: 'Report Water Supply Shortages to Municipal Authorities / Ward Office',
    instruction: 'Report depleted borewells, damaged municipal supply pipelines, or contaminated tanker deliveries to your local municipal corporation or gram panchayat.',
    priority: 'RECOMMENDED',
    reason: 'Summer heatwaves sharply deplete groundwater tables, causing water scarcity that requires emergency municipal tanker mobilization.',
    source: 'Central Ground Water Board (CGWB) Advisory',
    related_cascading_risk: 'Neighborhood water distress, commercial water tanker gouging, and sanitation failure.',
    practical_steps: [
      'Call the municipal water supply grievance helpline or log ticket on civic citizen app.',
      'Coordinate with resident welfare association (RWA) for collective community tanker scheduling.',
      'Test tanker water quality with chlorine test kit before pumping into household overhead tanks.',
      'Adopt strict water conservation measures: reuse greywater for gardening and toilet flushing.'
    ],
    warning_signs: [
      'Borewell pumping muddy air and sand.',
      'Municipal tap pressure dropping to zero across neighborhood.'
    ],
    what_not_to_do: [
      'Do NOT buy uncertified tanker water from unknown private operators without testing or boiling.',
      'Do NOT waste municipal water hosing down driveways or washing cars.'
    ],
    vulnerable_groups: 'Slum settlements and urban peri-urban peripheral communities.',
    checklist: [
      'Log water shortage complaint with municipal ward office',
      'Test private tanker water before domestic use',
      'Implement household greywater conservation practices'
    ]
  },

  // =========================================================================
  // 4. SEVERE WEATHER (Thunderstorms, Squalls, Lightning & Hail)
  // =========================================================================
  // --- SEVERE WEATHER: BEFORE ---
  {
    id: 'swx-bef-01',
    hazard: 'SEVERE_WEATHER',
    phase: 'BEFORE',
    category: 'UTILITY_SAFETY',
    title: 'Unplug Sensitive Electronics & Disconnect External TV Dish Cables',
    instruction: 'Unplug computers, televisions, microwave ovens, and inverters from wall sockets; disconnect external dish antenna coaxial cables.',
    priority: 'HIGH',
    reason: 'Lightning strike ground-currents and power line surges travel through utility lines and coaxial cables, causing instant component burnout and electrical fires.',
    source: 'Bureau of Indian Standards (BIS) Lightning Protection Guidelines & NDMA SOP',
    related_cascading_risk: 'Electrical surge fires, destroyed home appliances, and telecommunications loss.',
    practical_steps: [
      'Unplug power cords completely from wall sockets (merely turning switch off does NOT protect against 100,000V lightning arcs).',
      'Unscrew the metal coaxial cable connecting external dish antenna to your TV set-top box.',
      'Disconnect desktop computer LAN cables connected to exterior optical fiber/broadband boxes.',
      'Charge mobile phones and power banks prior to storm arrival; avoid charging during active lightning.'
    ],
    warning_signs: [
      'Damini app / IMD Nowcast warning for active convective lightning clusters within 20 km.',
      'Distant rolling thunder audible and sky turning dark greenish-black.'
    ],
    what_not_to_do: [
      'Do NOT leave expensive electronics plugged into wall sockets during severe lightning alerts.',
      'Do NOT touch metal cable connectors while lightning is active outside.'
    ],
    vulnerable_groups: 'Households in rural and semi-urban sectors with overhead power and cable wiring.',
    checklist: [
      'Unplug TV, computer, and refrigerator power cords',
      'Disconnect TV dish antenna coaxial cable',
      'Unplug broadband router and Wi-Fi modem'
    ]
  },
  {
    id: 'swx-bef-02',
    hazard: 'SEVERE_WEATHER',
    phase: 'BEFORE',
    category: 'PROPERTY_PREPARATION',
    title: 'Secure Metal Roofing Sheets, Solar Panels & Balcony Furniture',
    instruction: 'Fasten corrugated tin/asbestos sheets, solar water heater panels, and outdoor balcony chairs; clear loose clay tiles from sloping roofs.',
    priority: 'HIGH',
    reason: 'Thunderstorm squalls (Kalbaishakhi/Nor’westers) produce sudden microburst wind gusts exceeding 90 to 110 km/h that rip unanchored structures.',
    source: 'IMD Severe Convective Storm Warning Handbook',
    related_cascading_risk: 'Flying metal projectile hazards and roof collapse.',
    practical_steps: [
      'Check screws and J-bolts on tin roofing sheets; tighten loose fasteners.',
      'Bring indoor lightweight balcony chairs, clothes drying racks, and flower pots.',
      'Anchor rooftop solar panels with steel brackets bolted into reinforced concrete slab.',
      'Inspect roof drainage gutters and downspout grates; remove dead leaves and plastic waste.'
    ],
    warning_signs: [
      'Rapidly rising anvil-shaped cumulonimbus thunderclouds on horizon.',
      'Sudden drop in ambient air temperature and abrupt wind gust pick-up.'
    ],
    what_not_to_do: [
      'Do NOT climb onto roofs to secure sheets once strong winds and lightning have commenced.',
      'Do NOT leave glass flower pots on high balcony ledges.'
    ],
    vulnerable_groups: 'Residents living in homes with corrugated tin or asbestos roofing.',
    checklist: [
      'Move balcony furniture and potted plants inside',
      'Check rooftop solar panel mounting bolts',
      'Clear roof gutters of leaves and plastic debris'
    ]
  },
  {
    id: 'swx-bef-03',
    hazard: 'SEVERE_WEATHER',
    phase: 'BEFORE',
    category: 'EMERGENCY_CONTACTS',
    title: 'Check Damini App & IMD Nowcast Radar for Lightning Proximity',
    instruction: 'Check the Ministry of Earth Sciences Damini lightning app or IMD regional Doppler radar nowcast for real-time lightning strike movement within 40 km.',
    priority: 'RECOMMENDED',
    reason: 'Lightning strikes in India kill over 2,500 citizens annually; the Damini app provides a 15-to-30 minute advance warning of impending strikes in your exact GPS grid.',
    source: 'Ministry of Earth Sciences (MoES) & IITM Pune Damini Protocol',
    related_cascading_risk: 'Fatal lightning strikes among outdoor rural workers.',
    practical_steps: [
      'Download and install the Damini app (IITM Pune / MoES) on your smartphone.',
      'Enable GPS location permissions so automated proximity alerts trigger when thunderclouds approach within 20 km.',
      'Share lightning warning alerts with field farm laborers and open-air construction teams.',
      'Recall family members from open fields or sports grounds upon receiving Yellow/Orange lightning alert.'
    ],
    warning_signs: [
      'Damini app displaying Red zone warning for your district.',
      'Rapid darkening of southwestern sky with frequent cloud-to-ground lightning flashes.'
    ],
    what_not_to_do: [
      'Do NOT ignore mobile lightning alerts when working in agricultural paddy fields.',
      'Do NOT wait until rain starts before seeking lightning-safe shelter.'
    ],
    vulnerable_groups: 'Farmers transplanting paddy, cattle herders, and open-ground sports players.',
    checklist: [
      'Install Damini Lightning app on smartphone',
      'Check IMD Doppler Weather Radar nowcast',
      'Alert outdoor workers to seek pucca shelter'
    ]
  },
  {
    id: 'swx-bef-04',
    hazard: 'SEVERE_WEATHER',
    phase: 'BEFORE',
    category: 'TRANSPORTATION',
    title: 'Park Vehicles Away from Decaying Trees, Billboard Hoardings & Walls',
    instruction: 'Park cars, auto-rickshaws, and motorcycles inside covered garages or clear of old gulmohar/eucalyptus trees, roadside advertising hoardings, and loose brick walls.',
    priority: 'HIGH',
    reason: 'Squalls and thunderstorm downdrafts routinely collapse illegal advertising hoardings and uproot shallow-rooted trees onto parked vehicles.',
    source: 'NDMA Thunderstorm Guidelines & Municipal Safety By-Laws',
    related_cascading_risk: 'Crush trauma fatalities, vehicle destruction, and blocked emergency lanes.',
    practical_steps: [
      'Park vehicles inside a concrete garage or well away from mature trees with heavy overhangs.',
      'Avoid parking alongside commercial billboard hoardings or unreinforced compound walls.',
      'Cover vehicle windshield with a thick blanket or rubber mat if severe hail is forecast.',
      'Ensure vehicle wiper blades and hazard lights are in working order.'
    ],
    warning_signs: [
      'Commercial advertising hoardings flapping violently in wind.',
      'Creaking sounds from old roadside trees with exposed root systems.'
    ],
    what_not_to_do: [
      'Do NOT park underneath large eucalyptus or gulmohar trees with dead branches.',
      'Do NOT leave two-wheelers parked on steep road shoulders vulnerable to flash runoff.'
    ],
    vulnerable_groups: 'Two-wheeler commuters and commercial vehicle operators.',
    checklist: [
      'Move vehicle away from mature trees and hoardings',
      'Park inside covered garage or open space',
      'Secure car with handbrake and cover windshield if hail expected'
    ]
  },
  {
    id: 'swx-bef-05',
    hazard: 'SEVERE_WEATHER',
    phase: 'BEFORE',
    category: 'PROPERTY_PREPARATION',
    title: 'Clear Stormwater Runoff Culverts & Downspouts of Plastic Trash',
    instruction: 'Clear neighborhood road culverts, yard drains, and roof downspout grates of leaves, mud, and plastic bags before storm clouds burst.',
    priority: 'RECOMMENDED',
    reason: 'Intense convective thunderstorms deposit 50 to 80 mm of rain in under an hour; clogged drains cause immediate street flooding and vehicle submersion.',
    source: 'CPHEEO Urban Stormwater Guidelines',
    related_cascading_risk: 'Flash urban waterlogging and basement flooding.',
    practical_steps: [
      'Inspect roof drainage downspouts and remove bird nests, silt, and fallen leaves.',
      'Clear plastic debris from roadside storm drains fronting your residence.',
      'Ensure basement sump pumps have working float switches and backup power.',
      'Position sandbags near low-lying basement garage entry ramps.'
    ],
    warning_signs: [
      'Street gutters already filled with uncollected municipal garbage.',
      'Water pooling around compound gates during initial drizzle.'
    ],
    what_not_to_do: [
      'Do NOT dump garden waste or construction debris into open storm drains.',
      'Do NOT leave basement ramp flood gates unlatched.'
    ],
    vulnerable_groups: 'Basement shop owners and ground-floor residents.',
    checklist: [
      'Clean roof downspouts and yard drainage grates',
      'Verify basement sump pump operation',
      'Place sandbags at basement driveway entry ramp'
    ]
  },
  {
    id: 'swx-bef-06',
    hazard: 'SEVERE_WEATHER',
    phase: 'BEFORE',
    category: 'PETS_AND_LIVESTOCK',
    title: 'Move Outdoor Farm Laborers & Livestock into Covered Pucca Enclosures',
    instruction: 'Recall all farm laborers, open-air construction workers, and grazing cattle into reinforced pucca buildings before lightning begins.',
    priority: 'CRITICAL',
    reason: 'Open agricultural fields and pastures account for over 70% of lightning deaths in India; cattle tied to metal fences or under trees are electrocuted by ground current.',
    source: 'NDMA Lightning Guidelines & Animal Husbandry SOP',
    related_cascading_risk: 'Mass casualties among agricultural workers and herd mortality.',
    practical_steps: [
      'Blow a whistle or sound community siren to alert farm workers in open fields.',
      'Bring all grazing cattle and goats inside a pucca shed with concrete or tiled roof.',
      'Ensure animal sheds do not have ungrounded metal sheet roofs or wire fences.',
      'Ensure workers do not gather under open tin sheds in the middle of fields.'
    ],
    warning_signs: [
      'Cattle exhibiting nervous behavior and gathering together.',
      'Distant thunder audible (less than 30 seconds after lightning flash).'
    ],
    what_not_to_do: [
      'Do NOT leave farm workers transplanting paddy in standing water during lightning storms.',
      'Do NOT tether cattle to metal barbed wire fences or electrical transmission poles.'
    ],
    vulnerable_groups: 'Agricultural farm workers, MNREGA laborers, and domestic livestock.',
    checklist: [
      'Recall all field workers into pucca buildings',
      'Untie and shelter livestock inside reinforced sheds',
      'Ensure all outdoor work is halted immediately'
    ]
  },

  // --- SEVERE WEATHER: DURING ---
  {
    id: 'swx-dur-01',
    hazard: 'SEVERE_WEATHER',
    phase: 'DURING',
    category: 'SHELTER',
    title: 'Apply 30-30 Lightning Rule: If Thunder Heard Within 30s, Stay Indoors',
    instruction: 'Follow the 30-30 Rule: If time between lightning flash and thunder clap is less than 30 seconds, you are in immediate strike zone. Seek shelter immediately; remain inside 30 minutes after last thunder.',
    priority: 'CRITICAL',
    reason: 'Sound travels at ~340 m/s (~1 km every 3 seconds). Thunder heard within 30 seconds means the lightning strike is less than 10 km away and can strike your exact location.',
    source: 'National Weather Service & NDMA Lightning Safety Standard',
    warning: 'Lightning can strike up to 15 km away from rain clouds ("a bolt from the blue"). Do not wait for rain to start.',
    related_cascading_risk: 'Instant cardiac arrest and fatal neuro-electrical shock.',
    practical_steps: [
      'Seek shelter inside a substantial pucca building with plumbing and wiring (which acts as a Faraday cage).',
      'If no building is nearby, shelter inside a hard-topped metal enclosed vehicle with windows fully closed.',
      'Stay away from open porches, verandas, carports, and balconies.',
      'Remain inside the safe structure for a full 30 minutes after the very last roll of thunder is heard.'
    ],
    warning_signs: [
      'Time between lightning flash and thunder clap decreasing below 15 seconds.',
      'Hair on your arms standing on end, skin tingling, or hearing buzzing noises from metal fences.'
    ],
    what_not_to_do: [
      'Do NOT step outside as soon as the rain stops if thunder is still rumbling in the distance.',
      'Do NOT take shelter inside small tin shacks, bus stops, or open pavilions.'
    ],
    vulnerable_groups: 'Outdoor sportsmen, construction workers, and agricultural laborers.',
    checklist: [
      'Count seconds between lightning flash and thunder clap',
      'Seek pucca building or metal hardtop vehicle if under 30s',
      'Wait full 30 minutes after last thunder before exiting'
    ]
  },
  {
    id: 'swx-dur-02',
    hazard: 'SEVERE_WEATHER',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Never Shelter Beneath Tall Solitary Trees, Tin Sheds, or Metal Towers',
    instruction: 'Never seek shelter under tall solitary trees, tin sheds, power transmission pylons, or mobile towers during a thunderstorm.',
    priority: 'CRITICAL',
    reason: 'Tall isolated trees act as natural lightning rods. When struck, explosive side-flashes jump from the trunk into nearby humans, and ground currents electrocute anyone standing within 15 metres.',
    source: 'NDMA Lightning Safety Manual (Do’s and Don’ts)',
    warning: 'Sheltering under trees causes over 50% of all lightning fatalities in India.',
    related_cascading_risk: 'Explosive trunk splintering, secondary side-flash electrocution, and falling heavy limbs.',
    practical_steps: [
      'Move completely away from tall trees, grove edges, and metal transmission towers.',
      'If caught in a forest, seek shelter in an area of smaller, uniform-height trees on lower ground.',
      'Stay at least 15 metres away from barbed wire fences, clotheslines, and railroad tracks.',
      'Drop any metal umbrellas, golf clubs, iron rods, or fishing rods immediately.'
    ],
    warning_signs: [
      'Lightning flashing continuously overhead with immediate concussive thunderclaps.',
      'Ozone smell (clean, sharp pungent chlorine-like odor) in the air.'
    ],
    what_not_to_do: [
      'Do NOT huddle with cattle or people under a banyan or mango tree during rain.',
      'Do NOT hold an umbrella with a metal tip or metal shaft in open fields.'
    ],
    vulnerable_groups: 'Shepherds, farmers caught in sudden rain, and rural school children.',
    checklist: [
      'Move 15+ metres away from solitary trees and poles',
      'Discard metal-tipped umbrellas and metal tools',
      'Head towards enclosed concrete building or low terrain'
    ]
  },
  {
    id: 'swx-dur-03',
    hazard: 'SEVERE_WEATHER',
    phase: 'DURING',
    category: 'SAFE_ROUTES_EVACUATION',
    title: 'Assume Lightning Crouch Position If Trapped in Open Field',
    instruction: 'If caught in an open field with no shelter and hair standing on end: squat low on the balls of your feet with heels touching, head tucked between knees, and hands over ears. DO NOT lie flat.',
    priority: 'CRITICAL',
    reason: 'Squatting on balls of feet minimizes contact area with ground; touching heels together provides a closed loop for ground current to pass through feet rather than heart/brain. Lying flat makes you 10x more vulnerable to lethal ground current.',
    source: 'National Disaster Management Authority (NDMA) Lightning Protocol',
    warning: 'Never lie flat on the ground during a lightning strike.',
    related_cascading_risk: 'Lethal step-potential cardiac arrest from ground current dispersion.',
    practical_steps: [
      'Squat as low as possible on the balls of your feet (make yourself the smallest target).',
      'Ensure your heels are pressed firmly together.',
      'Tuck your head low between your knees; cover your ears with hands to prevent eardrum rupture from acoustic shockwave.',
      'If in a group, disperse immediately; keep at least 5 metres separation between individuals.'
    ],
    warning_signs: [
      'Static electricity making hair on head or arms stand straight up.',
      'Faint crackling or clicking sound from metal belt buckles or eyeglasses.'
    ],
    what_not_to_do: [
      'Do NOT lie flat on the ground; ground current dispersion kills more people than direct strikes.',
      'Do NOT huddle together in a tight group; dispersion prevents multiple simultaneous casualties.'
    ],
    vulnerable_groups: 'Farmers and laborers in vast open agricultural fields.',
    checklist: [
      'Squat low on balls of feet with heels touching',
      'Tuck head between knees and cover ears with hands',
      'Maintain 5-metre distance from other individuals'
    ]
  },
  {
    id: 'swx-dur-04',
    hazard: 'SEVERE_WEATHER',
    phase: 'DURING',
    category: 'UTILITY_SAFETY',
    title: 'Stay Away from Corded Phones, Plumbing Pipes & Metal Window Frames',
    instruction: 'Do not use corded landline telephones; avoid washing hands, taking showers, or leaning against metal plumbing pipes and metal window grills.',
    priority: 'HIGH',
    reason: 'Lightning strikes on building exteriors conduct lethal electrical current through metal plumbing pipes, gas lines, and copper telephone wires.',
    source: 'BIS National Electrical Code (NEC) Lightning Safety Section',
    related_cascading_risk: 'Indoor indoor electrocution and ear acoustic trauma.',
    practical_steps: [
      'Use mobile phones or cordless phones exclusively during thunderstorms (they are safe to use indoors).',
      'Postpone taking baths, showers, or washing dishes until lightning storm passes.',
      'Stay at least 1 metre away from metal window frames, concrete walls with internal rebar, and exterior doors.',
      'Stay away from metallic sinks, faucets, and radiator pipes.'
    ],
    warning_signs: [
      'Bright flashes illuminating window frames with immediate loud thunder.',
      'Static crackle audible over telephone or radio speakers.'
    ],
    what_not_to_do: [
      'Do NOT wash hands or dishes in kitchen sink during active lightning.',
      'Do NOT talk on corded landline telephone receivers.'
    ],
    vulnerable_groups: 'Homemakers working in kitchens and bathrooms during thunderstorms.',
    checklist: [
      'Avoid touching water faucets, showers, and plumbing',
      'Use mobile phone rather than corded landline phone',
      'Maintain 1-metre clearance from metal window frames'
    ]
  },
  {
    id: 'swx-dur-05',
    hazard: 'SEVERE_WEATHER',
    phase: 'DURING',
    category: 'TRANSPORTATION',
    title: 'Pull Vehicle Off Road Away from Trees & Stay Inside Hardtop Car',
    instruction: 'If driving during severe squalls, pull safely off road away from trees and power lines; turn on hazard flashers, keep windows closed, and stay inside.',
    priority: 'HIGH',
    reason: 'An enclosed hard-topped metal vehicle acts as a Faraday cage; lightning current flows over the exterior metal skin into the ground without harming occupants inside.',
    source: 'National Safety Council & NDMA Transportation Advisory',
    warning: 'Convertibles, fiberglass vehicles, auto-rickshaws, and motorcycles offer ZERO lightning protection.',
    related_cascading_risk: 'Loss of vehicular control, tree crush accidents, and blinding torrential spray collisions.',
    practical_steps: [
      'Slow down gradually and pull vehicle safely onto wide shoulder away from trees, poles, and flyovers.',
      'Turn on hazard warning flashers and engage parking brake.',
      'Keep all glass windows rolled completely shut.',
      'Place hands in your lap; do NOT touch metal door handles, steering wheel metal spokes, or plugged car chargers.'
    ],
    warning_signs: [
      'Severe hail cracking windshield glass.',
      'Crosswinds rocking the car and blowing rain horizontally.'
    ],
    what_not_to_do: [
      'Do NOT step out of car to take shelter under an overpass or nearby tree.',
      'Do NOT touch metal parts of the vehicle frame during active strikes.'
    ],
    vulnerable_groups: 'Highway drivers and interstate travelers.',
    checklist: [
      'Pull car safely onto road shoulder away from trees',
      'Turn on hazard flashers and keep windows rolled up',
      'Keep hands off metal door handles and stay inside vehicle'
    ]
  },
  {
    id: 'swx-dur-06',
    hazard: 'SEVERE_WEATHER',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Avoid Water Bodies, Swimming, Fishing & Flooded Paddy Fields',
    instruction: 'Get out of ponds, lakes, rivers, and flooded paddy fields immediately; move at least 50 metres inland away from water edges.',
    priority: 'CRITICAL',
    reason: 'Water is a superb conductor of electrical current. A lightning strike hitting water travels hundreds of metres across the surface, delivering lethal shock to swimmers or waders.',
    source: 'NDMA Lightning Safety Manual',
    related_cascading_risk: 'Mass electrocution and drowning in water bodies.',
    practical_steps: [
      'If swimming, bathing, or boating, exit the water immediately at the very first rumble of thunder.',
      'Leave wet fishing nets, rods, and metal buckets on bank and move inland.',
      'Seek shelter in a dry pucca building or metal enclosed vehicle.',
      'Do not walk along elevated canal bunds or narrow earthen dikes.'
    ],
    warning_signs: [
      'Water surface rippling violently under squall wind.',
      'Fish jumping erratically or distant lightning reflecting on water surface.'
    ],
    what_not_to_do: [
      'Do NOT continue fishing or boating hoping the storm will stay on the other side of the river.',
      'Do NOT stand holding a graphite or carbon-fiber fishing rod.'
    ],
    vulnerable_groups: 'Fishermen, rural bathers, and children playing in village ponds.',
    checklist: [
      'Exit water body immediately upon hearing thunder',
      'Drop fishing rods and metal equipment on bank',
      'Move 50+ metres inland to dry pucca shelter'
    ]
  },

  // --- SEVERE WEATHER: AFTER ---
  {
    id: 'swx-aft-01',
    hazard: 'SEVERE_WEATHER',
    phase: 'AFTER',
    category: 'MEDICAL_AND_HEALTH',
    title: 'Administer Immediate CPR to Lightning Victims (They Carry No Charge)',
    instruction: 'Lightning strike victims DO NOT carry any residual electrical charge; administer CPR (cardiopulmonary resuscitation) immediately and dial 108.',
    priority: 'CRITICAL',
    reason: 'Lightning causes sudden cardiac arrest and temporary paralysis of the brain’s respiratory center. Immediate chest compressions and rescue breaths can revive up to 70% of victims who appear clinically dead.',
    source: 'American Heart Association / Indian Red Cross Lightning Resuscitation Protocol',
    warning: 'Never delay touching a lightning strike victim; they are completely safe to touch and will die of anoxia without instant CPR.',
    related_cascading_risk: 'Irreversible brain anoxia and death from delayed resuscitation.',
    practical_steps: [
      'Check victim for responsiveness and normal breathing.',
      'If unresponsive and not breathing normally, begin CPR immediately: 30 hard and fast chest compressions (100-120 bpm, center of chest) followed by 2 rescue breaths.',
      'Have someone call 108 ambulance immediately, stating "cardiac arrest following lightning strike".',
      'Check for burns, broken bones, and spinal trauma; keep victim warm with a blanket once breathing resumes.'
    ],
    warning_signs: [
      'Victim lying unconscious on ground with singed clothing or feather-like red branching marks (Lichtenberg figures) on skin.',
      'Absence of carotid pulse and no chest rise.'
    ],
    what_not_to_do: [
      'Do NOT hesitate to touch the victim out of fear of electric shock; they hold zero charge.',
      'Do NOT bury the victim in mud or cow dung (lethal folk superstition that suffocates the patient).'
    ],
    vulnerable_groups: 'Coworkers and family members of outdoor lightning strike victims.',
    checklist: [
      'Verify victim is safe to touch (zero residual charge)',
      'Call 108 ambulance immediately',
      'Begin 30:2 chest compressions and rescue breathing without delay'
    ]
  },
  {
    id: 'swx-aft-02',
    hazard: 'SEVERE_WEATHER',
    phase: 'AFTER',
    category: 'STRUCTURAL_SAFETY',
    title: 'Inspect Roof Tiles, Corrugated Sheets & Chimneys for Displacement',
    instruction: 'Inspect roofing tiles, corrugated sheets, chimney pots, and solar brackets for wind dislocation from ground level before climbing.',
    priority: 'HIGH',
    reason: 'Squall winds loosen fasteners and crack clay tiles; loose sheets can slide off during subsequent wind gusts, injuring pedestrians below.',
    source: 'NDMA Structural Safety Protocol',
    related_cascading_risk: 'Falling roof tiles injuring pedestrians and rainwater ceiling leaks.',
    practical_steps: [
      'Perform visual inspection from ground using binoculars; check for displaced tiles or loose sheets.',
      'Cordon off area below loose parapets or hanging tin sheets with caution tape.',
      'Fasten loose sheets only when winds have completely died down and surfaces are dry.',
      'Check internal ceiling plaster for damp spots indicating hidden roof leaks.'
    ],
    warning_signs: [
      'Corrugated sheets vibrating or rattling in light breeze.',
      'Pieces of clay tiles or broken mortar lying in yard.'
    ],
    what_not_to_do: [
      'Do NOT climb wet sloping roofs immediately following a storm; slipping hazard is extreme.',
      'Do NOT walk beneath loose hanging tin sheets.'
    ],
    vulnerable_groups: 'Homeowners attempting immediate roof repairs.',
    checklist: [
      'Inspect roof from ground level with binoculars',
      'Barricade walkway beneath damaged roof eaves',
      'Hire professional roofer for high elevation repairs'
    ]
  },
  {
    id: 'swx-aft-03',
    hazard: 'SEVERE_WEATHER',
    phase: 'AFTER',
    category: 'UTILITY_SAFETY',
    title: 'Watch for Severed Power Lines Sparking in Wet Bushes or Roads',
    instruction: 'Beware of snapped overhead distribution lines tangled in wet branches or submerged in roadside puddles; maintain 10-metre distance and dial 112.',
    priority: 'CRITICAL',
    reason: 'Thunderstorm microbursts frequently snap tree branches across live power cables, leaving high-voltage wires hidden beneath foliage.',
    source: 'Central Electricity Authority Public Hazard Guidelines',
    related_cascading_risk: 'Secondary electrocution and bushfires.',
    practical_steps: [
      'Look up and scan for hanging wires before walking under trees or clearing brush.',
      'Warn neighbors, children, and passing motorists away from any fallen cable.',
      'Dial 1912 (power helpline) or 112 with exact pole location.',
      'Do not attempt to move branches resting across electrical lines.'
    ],
    warning_signs: [
      'Sparks, buzzing sounds, or smoke rising from fallen branches.'
    ],
    what_not_to_do: [
      'Do NOT touch fallen wires or branches in contact with power lines.',
      'Do NOT drive over fallen cables; wires can become entangled in car axles.'
    ],
    vulnerable_groups: 'Community cleanup volunteers and children playing in puddles.',
    checklist: [
      'Scan path for fallen wires before starting cleanup',
      'Keep 10-metre buffer from all hanging cables',
      'Report downed power lines to 1912 / 112'
    ]
  },
  {
    id: 'swx-aft-04',
    hazard: 'SEVERE_WEATHER',
    phase: 'AFTER',
    category: 'PROPERTY_PREPARATION',
    title: 'Check for Smoldering Lightning Fires in Attics, Thatch & Haystacks',
    instruction: 'Inspect attic crawlspaces, thatched eaves, and agricultural haystacks for hidden smoldering fires ignited by lightning strikes.',
    priority: 'HIGH',
    reason: 'Lightning strikes inject intense heat into wooden framing and dry thatch, which can smolder undetected for 2 to 6 hours before bursting into open flame.',
    source: 'Fire and Rescue Services Post-Storm Safety Guide',
    related_cascading_risk: 'Delayed structural house fires and haystack infernos.',
    practical_steps: [
      'Inspect attic and upper lofts with a flashlight; check for smoke odor or warm wall surfaces.',
      'Probe agricultural haystacks and thatch eaves with a wooden stick to detect internal heat.',
      'Keep fire extinguisher or bucket of water readily accessible.',
      'If smoke or sparks are detected, dial 101 (Fire Service) immediately and evacuate building.'
    ],
    warning_signs: [
      'Faint burning wood odor or haze in upper floor rooms.',
      'Discolored charred wood near roof lightning arrestor path.'
    ],
    what_not_to_do: [
      'Do NOT ignore burnt electrical smells assuming they will dissipate naturally.',
      'Do NOT sleep in building before inspecting attics following a direct strike nearby.'
    ],
    vulnerable_groups: 'Rural households with thatched roofs and agricultural hay lofts.',
    checklist: [
      'Inspect attic and thatched eaves for smoldering embers',
      'Probe agricultural haystacks for internal heat',
      'Keep water bucket and fire extinguisher ready'
    ]
  },
  {
    id: 'swx-aft-05',
    hazard: 'SEVERE_WEATHER',
    phase: 'AFTER',
    category: 'PROPERTY_PREPARATION',
    title: 'Clear Hail Accumulation from Roof Drains to Prevent Ceiling Collapse',
    instruction: 'Shovel accumulated hail stone drifts from flat roofs, terrace drains, and gutters to prevent sudden ceiling water leaks and overload collapse.',
    priority: 'RECOMMENDED',
    reason: 'Dense hail accumulations block terrace downspout grates, damming heavy meltwater that exerts immense structural load and causes sudden ceiling collapse.',
    source: 'NDMA Hailstorm Mitigation Manual',
    related_cascading_risk: 'Roof structural overload collapse and extensive ceiling water damage.',
    practical_steps: [
      'Use a plastic shovel or broom to clear hail drifts blocking terrace drainage outlets.',
      'Check flat roof terrace drains; break up compacted ice dams over drain grates.',
      'Wear sturdy non-slip boots when clearing hail from flat terraces.',
      'Check internal ceilings below flat roofs for sagging plaster.'
    ],
    warning_signs: [
      'Meltwater pooling 10 cm deep on terrace roof behind hail dam.',
      'Water dripping through ceiling light fixtures.'
    ],
    what_not_to_do: [
      'Do NOT walk on sloping tin or asbestos roofs covered in slippery hail ice.',
      'Do NOT use sharp metal pickaxes that puncture terrace waterproofing membranes.'
    ],
    vulnerable_groups: 'Residents of flat concrete roof houses in hailstorm prone regions.',
    checklist: [
      'Clear hail blockage from terrace drain outlets',
      'Wear non-slip footwear while clearing terrace ice',
      'Inspect ceilings for water leakage or sagging plaster'
    ]
  },
  {
    id: 'swx-aft-06',
    hazard: 'SEVERE_WEATHER',
    phase: 'AFTER',
    category: 'TRANSPORTATION',
    title: 'Exercise Caution on Roads Covered with Hail Slick or Fallen Leaves',
    instruction: 'Drive at reduced speeds on roads covered with hail slush or wet shredded leaves; maintain triple following distance to prevent skidding.',
    priority: 'RECOMMENDED',
    reason: 'Hail slush and wet mashed leaves create extreme loss of tire friction equivalent to driving on black ice, causing sudden vehicle spinouts.',
    source: 'Ministry of Road Transport & Highways Wet Weather Safety',
    related_cascading_risk: 'Multi-vehicle highway pileups and skidding accidents.',
    practical_steps: [
      'Reduce vehicle speed by at least 50% on hail-covered or leaf-slick roadways.',
      'Apply brakes gently and avoid sudden sharp steering maneuvers.',
      'Maintain at least 6 car lengths following distance behind preceding vehicles.',
      'Two-wheeler riders should dismount and walk bike across deep hail accumulations.'
    ],
    warning_signs: [
      'ABS anti-lock braking pulsation vibrating through brake pedal.',
      'Vehicle tail fishtailing when cornering on wet leaves.'
    ],
    what_not_to_do: [
      'Do NOT slam hard on brakes on hail-covered roads.',
      'Do NOT attempt high-speed overtaking on narrow hill roads post-storm.'
    ],
    vulnerable_groups: 'Two-wheeler and auto-rickshaw riders.',
    checklist: [
      'Reduce driving speed by half on wet roads',
      'Maintain 6-car following distance',
      'Brake gently in straight line to prevent skidding'
    ]
  },

  // =========================================================================
  // 5. LANDSLIDE & SLOPE INSTABILITY
  // =========================================================================
  // --- LANDSLIDE: BEFORE ---
  {
    id: 'lsd-bef-01',
    hazard: 'LANDSLIDE',
    phase: 'BEFORE',
    category: 'PROPERTY_PREPARATION',
    title: 'Monitor Slopes for New Ground Tension Cracks & Tilting Trees',
    instruction: 'Inspect hillside slopes for widening ground tension cracks, tilting trees, utility poles, jammed doors/windows, or sudden muddy spring water seepage.',
    priority: 'CRITICAL',
    reason: 'Sustained monsoon rain increases pore-water pressure inside hillside soil; tension cracks and tilting vegetation are the primary geotechnical precursors of catastrophic slope failure.',
    source: 'Geological Survey of India (GSI) Landslide Early Warning Guidelines',
    warning: 'New diagonal cracks appearing in building walls or compound pavements on hill slopes indicate active creeping shear plane failure.',
    related_cascading_risk: 'Massive slope failure, rockfall, and building structural shearing.',
    practical_steps: [
      'Walk your hillside property perimeter weekly during monsoon; check for ground fissures.',
      'Drive wooden pegs across visible cracks to monitor widening rate daily.',
      'Check if trees, fence posts, or telephone poles have tilted downhill.',
      'Observe natural hillside water springs; if clear water suddenly turns dark brown or muddy, slope is shearing internally.'
    ],
    warning_signs: [
      'Ground cracks wider than 10 mm on slopes or retaining walls.',
      'Doors and windows suddenly sticking or jamming in their frames.',
      'Underground utility pipes leaking or breaking without apparent cause.'
    ],
    what_not_to_do: [
      'Do NOT ignore widening cracks on slopes or patch them with cosmetic cement without reporting.',
      'Do NOT dig into toe of slope to expand garden or parking space during monsoon.'
    ],
    vulnerable_groups: 'Residents of hillside settlements, terraced hill roads, and river valley flanks.',
    checklist: [
      'Inspect hillside slopes for ground tension cracks',
      'Monitor retaining walls for bulging or tilting',
      'Report muddy spring water discharges to district authorities'
    ]
  },
  {
    id: 'lsd-bef-02',
    hazard: 'LANDSLIDE',
    phase: 'BEFORE',
    category: 'PROPERTY_PREPARATION',
    title: 'Direct Surface Storm Runoff Away from Steep Hillside Slopes',
    instruction: 'Install and maintain lined catch-water drains to divert roof and road runoff safely away from vulnerable slope crests into natural masonry channels.',
    priority: 'HIGH',
    reason: 'Uncontrolled surface stormwater infiltration saturates vulnerable soil mantles, drastically reducing shear strength and triggering debris flows.',
    source: 'National Institute of Disaster Management (NIDM) Slope Stabilization SOP',
    related_cascading_risk: 'Debris flow mobilization and toe scouring.',
    practical_steps: [
      'Ensure roof gutters discharge into sealed downspouts directed into roadside drainage masonry channels.',
      'Keep perimeter interceptor catch-water drains clear of fallen rocks, leaves, and mud.',
      'Pave or line drainage ditches with stone masonry or cement to prevent seepage into slope soil.',
      'Never allow septic tank overflow or household greywater to discharge freely onto hillside slope.'
    ],
    warning_signs: [
      'Stormwater pooling on slope terraces instead of draining away.',
      'Water gushing over road shoulders and cutting deep erosion gullies into hillside.'
    ],
    what_not_to_do: [
      'Do NOT allow unchanneled water from your roof or driveway to pour directly down slopes.',
      'Do NOT block existing hill drains with construction spoil or garbage.'
    ],
    vulnerable_groups: 'Hill town residents living on steep valley slopes.',
    checklist: [
      'Clear perimeter catch-water hillside drains',
      'Direct roof runoff into sealed masonry drainage gullies',
      'Inspect slope for erosion gullies after heavy rain'
    ]
  },
  {
    id: 'lsd-bef-03',
    hazard: 'LANDSLIDE',
    phase: 'BEFORE',
    category: 'SAFE_ROUTES_EVACUATION',
    title: 'Map Transverse Hill Evacuation Paths Away from Debris Chutes',
    instruction: 'Identify multiple horizontal (transverse) evacuation routes across the slope onto stable bedrock ridges; avoid paths along drainage gullies or ravines.',
    priority: 'CRITICAL',
    reason: 'Debris flows travel down existing stream channels and gullies at speeds of 30 to 60 km/h; running downhill along the gully guarantees getting engulfed.',
    source: 'GSI Landslide Evacuation Protocol',
    warning: 'Always evacuate sideways (transverse) to the slope onto stable rocky ridges, NEVER straight downhill.',
    related_cascading_risk: 'High-speed debris flow engulfment and road severed isolation.',
    practical_steps: [
      'Map lateral paths that lead across the hill towards stable rock ridges or designated shelter sites.',
      'Identify designated village evacuation centers located on confirmed bedrock geology.',
      'Walk paths in daytime with family members; ensure route does not cross natural debris chutes.',
      'Keep heavy-duty battery torches and walking sticks near front door.'
    ],
    warning_signs: [
      'Cumulative 48-hour rainfall crossing regional landslide threshold (e.g. >150 mm in Western Ghats / Himalayas).',
      'GSI Landslide Early Warning System issuing Orange/Red bulletin for your sub-basin.'
    ],
    what_not_to_do: [
      'Do NOT choose an evacuation route along stream gullies, dry seasonal nallahs, or ravine bottoms.',
      'Do NOT hesitate to evacuate when local administration issues slope advisory.'
    ],
    vulnerable_groups: 'Elderly residents and children in isolated hillside hamlets.',
    checklist: [
      'Map horizontal evacuation route to stable bedrock ridge',
      'Ensure route avoids stream channels and seasonal gullies',
      'Pack emergency grab bag with headlamps and whistle'
    ]
  },
  {
    id: 'lsd-bef-04',
    hazard: 'LANDSLIDE',
    phase: 'BEFORE',
    category: 'PROPERTY_PREPARATION',
    title: 'Avoid Cutting Slope Toes & Protect Deep-Rooted Native Vegetation',
    instruction: 'Never cut into the base (toe) of steep slopes for building or road widening; plant and preserve native deep-rooted trees and vetiver grass.',
    priority: 'HIGH',
    reason: 'Cutting the toe of a slope removes natural mechanical support, destabilizing the entire soil mass above; tree roots act as natural bio-structural soil anchors.',
    source: 'Indian Road Congress (IRC) Hill Road Stabilization Guidelines',
    related_cascading_risk: 'Toe failure, rotational slumping, and chronic road subsidence.',
    practical_steps: [
      'Construct reinforced masonry or gabion retaining walls with weepholes before making any slope cuts.',
      'Plant deep-rooted native tree species (e.g., oak, alder, bamboo) and vetiver grass across bare slope faces.',
      'Ensure retaining walls have clear weep holes to discharge accumulated hydrostatic pressure.',
      'Consult a certified geotechnical engineer before undertaking any hillside terracing or construction.'
    ],
    warning_signs: [
      'Bulging or cracking in stone retaining walls.',
      'Weep holes in retaining walls blocked with dried mud and discharging zero water during rain.'
    ],
    what_not_to_do: [
      'Do NOT excavate slope toes using heavy earthmoving JCB equipment during monsoon season.',
      'Do NOT clear hillside forest cover for short-term agriculture or firewood.'
    ],
    vulnerable_groups: 'Homeowners building additions on steep hill plots.',
    checklist: [
      'Inspect retaining wall weep holes and clear sediment',
      'Plant native deep-root vegetation across bare slope faces',
      'Avoid unengineered excavation of slope toe'
    ]
  },
  {
    id: 'lsd-bef-05',
    hazard: 'LANDSLIDE',
    phase: 'BEFORE',
    category: 'FAMILY_COMMUNICATION',
    title: 'Establish Neighborhood Slope Monitoring & Whistle Alert System',
    instruction: 'Organize a community slope-watch committee; establish a distinct whistle/drum alarm system to warn sleeping neighbors of slope movement at night.',
    priority: 'RECOMMENDED',
    reason: 'Over 65% of fatal landslide disasters strike between midnight and 05:00 AM while families are asleep and oblivious to slope deformation.',
    source: 'NDMA Community-Based Disaster Risk Reduction (CBDRR) Manual',
    related_cascading_risk: 'Mass nighttime casualty entrapment beneath collapsed debris.',
    practical_steps: [
      'Agree on an audible emergency signal: three sustained whistle blasts or temple bell ringing.',
      'Designate rotational volunteers to monitor hillside streams and cracks during heavy continuous night downpours.',
      'Establish a WhatsApp/SMS alert group for all households along vulnerable slope corridor.',
      'Identify elderly and disabled neighbors who require physical evacuation assistance.'
    ],
    warning_signs: [
      'Continuous heavy monsoon downpour persisting past 22:00.',
      'Small stones and soil pebbles trickling down cut slopes onto roadway.'
    ],
    what_not_to_do: [
      'Do NOT sleep in ground-floor rooms facing directly towards an unstable cut slope during intense cloudbursts.',
      'Do NOT ignore small pebble roll-outs; they precede major debris slides by minutes.'
    ],
    vulnerable_groups: 'Families living in homes directly abutted against steep excavated hill faces.',
    checklist: [
      'Establish community whistle alarm protocol with neighbors',
      'Sleep in interior rooms away from uphill slope wall during heavy rain',
      'Verify emergency contact numbers of ward disaster committee'
    ]
  },
  {
    id: 'lsd-bef-06',
    hazard: 'LANDSLIDE',
    phase: 'BEFORE',
    category: 'EMERGENCY_KIT',
    title: 'Pack Emergency Grab Bag with Sturdy Boots, Rope & Whistle',
    instruction: 'Keep a portable emergency backpack containing sturdy hiking boots, 15-metre nylon climbing rope, work gloves, torch, whistle, and 3-day rations near exit.',
    priority: 'RECOMMENDED',
    reason: 'Navigating rough landslide debris fields and mud flows requires sturdy footwear and hands-free lighting; ordinary slippers or barefoot travel leads to severe injury.',
    source: 'NDRF Hill Search & Rescue Manual',
    related_cascading_risk: 'Inability to evacuate across mud debris and foot puncture injuries.',
    practical_steps: [
      'Pack sturdy ankle-high hiking boots or gumboots with deep tread soles.',
      'Include a 10–15 mm thick nylon utility rope for emergency steep slope descent.',
      'Pack high-intensity LED headlamp (keeps hands free for balance) and extra batteries.',
      'Include emergency foil survival blanket, whistle, first aid kit, and high-energy dry rations.'
    ],
    warning_signs: [
      'Rainfall intensity exceeding 20 mm/hour on mountain slopes.'
    ],
    what_not_to_do: [
      'Do NOT attempt to scramble across wet mud debris in flip-flops, sandals, or high heels.',
      'Do NOT overload grab bag with heavy non-essential items.'
    ],
    vulnerable_groups: 'Hill hamlets located far from motorable roads.',
    checklist: [
      'Pack ankle-high boots and utility rope in backpack',
      'Include LED headlamp, whistle, and survival blanket',
      'Place grab bag near main exit door'
    ]
  },

  // --- LANDSLIDE: DURING ---
  {
    id: 'lsd-dur-01',
    hazard: 'LANDSLIDE',
    phase: 'DURING',
    category: 'SAFE_ROUTES_EVACUATION',
    title: 'Evacuate Laterally Across Slope Away from Debris Path (Never Downhill)',
    instruction: 'Move quickly sideways (laterally/transversely) across the slope away from the path of descending debris; never run straight downhill ahead of a slide.',
    priority: 'CRITICAL',
    reason: 'Landslides and debris flows accelerate downhill at 30 to 60 km/h, easily outrunning human sprinters; moving laterally takes you out of the narrow debris chute.',
    source: 'GSI & NDMA Landslide Survival Protocol',
    warning: 'Never run straight downhill in the direction the mud and boulders are traveling.',
    related_cascading_risk: 'High-velocity boulder impact and burial under mud debris.',
    practical_steps: [
      'Identify the central axis of the descending slide and move immediately at right angles to it.',
      'Scramble across slope towards stable rock outcrops, mature ridge crests, or high ground.',
      'Warn others shouting "LANDSLIDE!" while moving sideways.',
      'Hold onto sturdy bedrock or fixed structures if knocked down; protect your head.'
    ],
    warning_signs: [
      'Trembling ground, roaring sound like an oncoming freight train, snapping tree trunks.',
      'Shower of pebbles, soil spatter, and snapping branches rushing down slope.'
    ],
    what_not_to_do: [
      'Do NOT try to outrun a debris flow by running straight downhill along the valley.',
      'Do NOT stop to collect heavy personal belongings.'
    ],
    vulnerable_groups: 'Children, elders, and persons unfamiliar with mountain terrain.',
    checklist: [
      'Move sideways at right angles to descending debris flow',
      'Scramble towards bedrock ridge or elevated spur',
      'Keep head covered with arms or helmet'
    ]
  },
  {
    id: 'lsd-dur-02',
    hazard: 'LANDSLIDE',
    phase: 'DURING',
    category: 'SHELTER',
    title: 'If Trapped Indoors, Curl into Tight Ball Under Sturdy Furniture',
    instruction: 'If trapped indoors with slide imminent, curl into a tight ball under a sturdy table, bed, or interior doorframe; protect your head and neck with your arms.',
    priority: 'CRITICAL',
    reason: 'Curling under sturdy furniture provides a protective void against collapsing ceiling beams, falling masonry, and tumbling hillside rocks.',
    source: 'FEMA & NDMA Indoor Landslide Protection Standard',
    related_cascading_risk: 'Crush asphyxiation and traumatic brain injury.',
    practical_steps: [
      'Drop to floor under a heavy wooden dining table, bed, or reinforced interior door lintel.',
      'Curl into a tight fetal ball on your side; cover your head and back of neck with hands and arms.',
      'Tuck face into chest to protect airway from inhaled dust and mud slurry.',
      'Remain in protective posture until all grinding movement and rumbling ceases completely.'
    ],
    warning_signs: [
      'Uphill wall of house cracking violently or bulging inward with mud slurry leaking through floorboards.',
      'Loud roaring sound outside with flying debris hitting roof.'
    ],
    what_not_to_do: [
      'Do NOT stand near exterior uphill walls or glass windows.',
      'Do NOT attempt to escape across open slope once mudflow has struck house perimeter.'
    ],
    vulnerable_groups: 'Bedridden individuals, young children, and elderly persons unable to flee.',
    checklist: [
      'Drop under heavy wooden table or reinforced lintel',
      'Curl into tight ball and cover head with arms',
      'Protect airway with cloth against fine mud dust'
    ]
  },
  {
    id: 'lsd-dur-03',
    hazard: 'LANDSLIDE',
    phase: 'DURING',
    category: 'EMERGENCY_CONTACTS',
    title: 'Listen for Roaring Sound & Watch Downstream River Level Drops',
    instruction: 'Listen for rumbling sounds of crashing boulders; if a mountain river suddenly drops to a trickle, evacuate uphill immediately—an upstream landslide dam has formed.',
    priority: 'CRITICAL',
    reason: 'Landslides into river gorges dam the river, causing water levels downstream to drop abruptly; the temporary dam will breach within hours, unleashing a devastating flash flood.',
    source: 'CWC & GSI Landslide Dam Hazard Advisory',
    warning: 'A sudden drop in river flow during intense mountain rainfall is the single most critical warning of a Landslide Dam Outburst Flood (LDOF).',
    related_cascading_risk: 'Catastrophic Landslide Dam Outburst Flood (LDOF) and downstream river valley inundation.',
    practical_steps: [
      'If you observe mountain stream water suddenly turn into dry bed or trickle during rain, evacuate immediately to high ground (at least 30 metres above river level).',
      'Alert all downstream villages and police checkpoints immediately via phone.',
      'Do not return to river banks until authorities confirm upstream gorge is clear.'
    ],
    warning_signs: [
      'Mountain river water dropping by more than 1 metre in 15 minutes during heavy rainfall.',
      'Sudden cessation of river roar accompanied by distant booming sound in upper gorge.'
    ],
    what_not_to_do: [
      'Do NOT walk onto dry riverbed to inspect exposed rocks or fish.',
      'Do NOT stay in riverside homes or camping sites.'
    ],
    vulnerable_groups: 'Downstream riverbank communities, bridge toll booths, and riverside pilgrims.',
    checklist: [
      'Monitor river water level from elevated vantage point',
      'Evacuate 30+ metres above river level if flow suddenly drops',
      'Alert downstream police and disaster control room'
    ]
  },
  {
    id: 'lsd-dur-04',
    hazard: 'LANDSLIDE',
    phase: 'DURING',
    category: 'TRANSPORTATION',
    title: 'Stop Vehicle Immediately If Encountering Fresh Rocks on Mountain Road',
    instruction: 'If driving on hill roads and encountering small falling stones or fresh mud across tarmac, stop immediately, reverse safely, and do not attempt crossing.',
    priority: 'HIGH',
    reason: 'Trickling pebbles and small rocks are immediate precursors of a major rockfall or debris slide about to release from the cut slope above.',
    source: 'Border Roads Organisation (BRO) Hill Highway Safety Protocol',
    warning: 'Never stop your vehicle directly beneath a steep cut slope or overhang during rainfall.',
    related_cascading_risk: 'Vehicle crushed by falling boulders and swept down gorge.',
    practical_steps: [
      'Reverse vehicle to a wide, stable section of roadway away from steep cut slopes.',
      'Do not step out of vehicle directly under an active rockfall zone.',
      'Turn on hazard flashers and warn oncoming traffic to stop.',
      'Wait in safe turnout zone or return to nearest hill town.'
    ],
    warning_signs: [
      'Small stones (pebbles/gravel) pinging against road surface or car hood.',
      'Cloud of dust rising from slope above road curve.'
    ],
    what_not_to_do: [
      'Do NOT accelerate to try and "beat" the falling stones across the hazard zone.',
      'Do NOT stop to clear rocks from road with your hands during active rockfall.'
    ],
    vulnerable_groups: 'Tourists and commercial taxi drivers unfamiliar with mountain roads.',
    checklist: [
      'Reverse car to safe turnout away from cut slope',
      'Turn on hazard flashers to alert following traffic',
      'Wait in safe zone until BRO / PWD inspects slope'
    ]
  },
  {
    id: 'lsd-dur-05',
    hazard: 'LANDSLIDE',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Stay Away from River Gorges & Narrow Mountain Valley Bottoms',
    instruction: 'Avoid river valley bottoms, canyon bridges, and low-lying gorge floors during cloudbursts; seek elevated ridges.',
    priority: 'HIGH',
    reason: 'Debris flows funnel through narrow mountain gorges, gaining speed and depth; valley floors offer zero lateral escape routes.',
    source: 'NIDM Mountain Hazard Safety Standard',
    related_cascading_risk: 'Flash flood entrapment and debris burial.',
    practical_steps: [
      'Climb uphill onto stable bedrock shoulders at least 20 to 30 metres above valley floor.',
      'Avoid camping or parking near confluences of mountain streams.',
      'Stay on designated highway alignment; do not take shortcuts down steep valley trails.'
    ],
    warning_signs: [
      'Muddy water surging down seasonal hillside dry beds.',
      'Loud clacking sound of underwater boulders grinding against riverbed.'
    ],
    what_not_to_do: [
      'Do NOT camp or park near riverbanks during monsoon season.',
      'Do NOT cross footbridges submerged in turbulent mountain runoff.'
    ],
    vulnerable_groups: 'Pilgrims, trekkers, and riverside dhaba operators.',
    checklist: [
      'Climb 30+ metres above gorge floor',
      'Stay clear of mountain stream confluences',
      'Follow main road alignment onto stable bedrock'
    ]
  },
  {
    id: 'lsd-dur-06',
    hazard: 'LANDSLIDE',
    phase: 'DURING',
    category: 'VULNERABLE_MEMBERS',
    title: 'Assist Elderly & Mobility-Impaired Members to Uphill Stable Spur',
    instruction: 'Provide physical walking support or carry mobility-impaired relatives uphill to confirmed stable bedrock spurs; do not leave anyone behind in valley homes.',
    priority: 'HIGH',
    reason: 'Landslide evacuation requires rapid vertical and lateral scramble across rough terrain; elderly individuals cannot negotiate muddy slopes unassisted.',
    source: 'NDMA Disability Inclusive Disaster Risk Reduction Manual',
    related_cascading_risk: 'Fatal entrapment of mobility-impaired citizens.',
    practical_steps: [
      'Pair able-bodied family members with elderly or child relatives (buddy system).',
      'Use walking poles, bamboo staffs, or climbing ropes for balance on slick mud.',
      'Carry infants securely in chest carry pouches, keeping both hands free for balance.',
      'Move steadily towards pre-identified stable bedrock structures.'
    ],
    warning_signs: [
      'Cracking sounds from uphill hillside retaining walls.'
    ],
    what_not_to_do: [
      'Do NOT allow mobility-impaired members to attempt slippery steep paths unassisted.',
      'Do NOT leave disabled relatives in ground-floor rooms hoping slide will bypass home.'
    ],
    vulnerable_groups: 'Bedridden elders, pregnant mothers, and young children.',
    checklist: [
      'Implement family buddy system for elderly support',
      'Use walking sticks and ropes on slippery mud trails',
      'Secure infants in chest carrier pouches'
    ]
  },

  // --- LANDSLIDE: AFTER ---
  {
    id: 'lsd-aft-01',
    hazard: 'LANDSLIDE',
    phase: 'AFTER',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Stay Away from Slide Perimeter; Secondary Slides Follow Within Hours',
    instruction: 'Do not approach or walk across the landslide scar or debris deposit; secondary slides, rockfalls, and slumping frequently occur hours after the initial failure.',
    priority: 'CRITICAL',
    reason: 'The steep scarp left behind by a landslide is severely fractured and destabilized; additional saturated soil will release without warning, burying onlookers.',
    source: 'GSI Post-Disaster Field Safety Protocol',
    warning: 'Secondary slides and scarp collapses kill dozens of curious onlookers and rescue volunteers every monsoon season.',
    related_cascading_risk: 'Secondary slide burial, unstable scarp collapse, and rescuer casualties.',
    practical_steps: [
      'Maintain a minimum safety perimeter of at least 50 metres from the top scarp and lateral margins of the slide.',
      'Keep crowds and curious onlookers away from the debris edge.',
      'Wait for official clearance from Geological Survey of India (GSI) or PWD engineers before entering area.',
      'Direct rescue efforts from stable bedrock ground only.'
    ],
    warning_signs: [
      'Small stones, dirt clods, and dust continuing to fall from the top scarp face.',
      'New tension cracks opening in the soil above the landslide crown.'
    ],
    what_not_to_do: [
      'Do NOT walk across the muddy debris fan to search for personal belongings.',
      'Do NOT stand directly beneath exposed overhangs on the slide scarp.'
    ],
    vulnerable_groups: 'Curious local crowds, village volunteers, and photo-taking onlookers.',
    checklist: [
      'Maintain 50-metre exclusion perimeter from slide scar',
      'Prevent crowds and children from entering debris zone',
      'Wait for geotechnical engineering clearance before re-entry'
    ]
  },
  {
    id: 'lsd-aft-02',
    hazard: 'LANDSLIDE',
    phase: 'AFTER',
    category: 'EMERGENCY_CONTACTS',
    title: 'Check for Trapped Survivors Without Entering Unstable Debris Zone',
    instruction: 'Scan debris field visually and listen for cries or tapping sounds from stable vantage points; direct arriving NDRF / SDRF teams with accurate headcount.',
    priority: 'CRITICAL',
    reason: 'Stepping onto saturated debris can trigger liquefaction and sink rescue personnel; specialized NDRF teams use search cameras and acoustic sensors to locate voids.',
    source: 'NDRF Urban Search and Rescue (USAR) Protocol',
    related_cascading_risk: 'Rescuer entrapment and structural collapse during recovery operations.',
    practical_steps: [
      'Listen quietly for shouting, whistling, or tapping sounds from buried structures.',
      'Note exact locations of bedrooms, living rooms, or collapsed vehicles before the slide.',
      'Provide arriving NDRF/SDRF commanders with precise household headcount and known victim locations.',
      'Do not operate heavy JCB excavators directly over suspected victim void spaces.'
    ],
    warning_signs: [
      'Voice calls, tapping on pipes, or waving hand visible from collapsed void.'
    ],
    what_not_to_do: [
      'Do NOT send unequipped crowds walking onto wet mud debris.',
      'Do NOT bring heavy bulldozers over suspected survivor locations without hand-probing.'
    ],
    vulnerable_groups: 'Trapped survivors beneath collapsed building voids.',
    checklist: [
      'Listen for vocal or tapping distress signals from safe perimeter',
      'Provide exact headcount and room layout to NDRF teams',
      'Keep heavy machinery away from suspected survivor voids'
    ]
  },
  {
    id: 'lsd-aft-03',
    hazard: 'LANDSLIDE',
    phase: 'AFTER',
    category: 'UTILITY_SAFETY',
    title: 'Report Broken Gas Pipes, Severed Electric Cables & Damaged Walls',
    instruction: 'Check for severed underground electrical cables, broken LPG gas lines, and ruptured water pipes around perimeter; report immediately to emergency services (112).',
    priority: 'HIGH',
    reason: 'Differential ground movement rips apart buried utility lines; escaping gas ignites readily from sparking snapped cables, sparking secondary hillside infernos.',
    source: 'NDMA Post-Disaster Infrastructure Assessment Protocol',
    related_cascading_risk: 'Secondary gas explosions, utility fires, and potable water contamination.',
    practical_steps: [
      'Smell for LPG or sulfur odor around property perimeter; if detected, evacuate uphill immediately.',
      'Report downed electric poles and tangled high-voltage cables to local electricity board.',
      'Shut off main water supply valves if pipes are sheared to conserve municipal reservoir storage.',
      'Do not light matches, lighters, or use electrical appliances in the vicinity.'
    ],
    warning_signs: [
      'Hissing sounds or bubbling mud indicating high-pressure gas/water pipeline rupture.',
      'Sparks from severed utility cables lying in mud.'
    ],
    what_not_to_do: [
      'Do NOT turn on electrical switches or light candles near landslide damage.',
      'Do NOT drink water from ruptured supply lines exposed to landslide mud.'
    ],
    vulnerable_groups: 'Homeowners inspecting perimeter utility connections.',
    checklist: [
      'Check perimeter for gas odor or sparking cables',
      'Report utility breaches immediately to 112 / fire department',
      'Shut off main domestic water valve'
    ]
  },
  {
    id: 'lsd-aft-04',
    hazard: 'LANDSLIDE',
    phase: 'AFTER',
    category: 'STRUCTURAL_SAFETY',
    title: 'Have Geotechnical Engineer Certify Slope Stability Before Rebuilding',
    instruction: 'Do not reoccupy or rebuild damaged hillside dwellings until a certified geotechnical engineer or GSI team certifies slope stability and foundation integrity.',
    priority: 'HIGH',
    reason: 'Post-slide hillside slopes retain high internal moisture and active shear planes; rebuilding without slope stabilization results in re-burial in subsequent monsoons.',
    source: 'National Building Code of India (NBC) Hill Construction Code',
    related_cascading_risk: 'Recurrent slope failure and repetitive capital infrastructure loss.',
    practical_steps: [
      'Commission a slope stability assessment (factor of safety analysis) from qualified geotechnical engineers.',
      'Install recommended engineering mitigations: micropiles, soil nails, gabion retaining walls, and subsurface perforated drainage pipes.',
      'Observe recommended municipal building setback distances from steep slope crests.',
      'Obtain formal structural fitness certificate before re-inhabiting premises.'
    ],
    warning_signs: [
      'New fine cracks appearing in fresh repair plaster within weeks.',
      'Retaining walls showing persistent outward tilt.'
    ],
    what_not_to_do: [
      'Do NOT rebuild on the exact same debris footprint without geotechnical anchoring.',
      'Do NOT construct additional upper floors on buildings on unstable slopes.'
    ],
    vulnerable_groups: 'Hill community homeowners planning reconstruction.',
    checklist: [
      'Request geotechnical slope fitness assessment',
      'Install engineered gabion walls and drainage weep holes',
      'Comply with municipal hill building setback codes'
    ]
  },
  {
    id: 'lsd-aft-05',
    hazard: 'LANDSLIDE',
    phase: 'AFTER',
    category: 'PROPERTY_PREPARATION',
    title: 'Replant Native Deep-Rooted Grasses & Trees on Exposed Scar Faces',
    instruction: 'Plant fast-growing vetiver grass (Chrysopogon zizanioides) and native deep-rooted pioneer trees on exposed landslide scars to bind topsoil and prevent rill erosion.',
    priority: 'RECOMMENDED',
    reason: 'Bare landslide scars suffer severe sheet and rill erosion in subsequent rains; bio-engineering with vetiver grass creates a living underground anchor network 3 metres deep.',
    source: 'Central Soil and Water Conservation Research and Training Institute (CSWCRTI)',
    related_cascading_risk: 'Chronic slope rill erosion and recurring debris washouts.',
    practical_steps: [
      'Plant vetiver grass slips along contour lines spaced 1 metre apart across the slope face.',
      'Inter-plant with native pioneer trees (alder, oak, bamboo) that tolerate rocky subsoil.',
      'Install coir geotextile netting over exposed soil to hold seeds and prevent rain wash.',
      'Maintain surface drainage channels above the planted zone to prevent gully formation.'
    ],
    warning_signs: [
      'Rills and small gullies carving into exposed red/yellow landslide clay.',
      'Rainwater washing muddy sediment into lower road drains.'
    ],
    what_not_to_do: [
      'Do NOT plant shallow-rooted ornamental trees (e.g. eucalyptus, pine) on steep unstable slopes.',
      'Do NOT allow grazing animals onto newly planted bio-engineering slopes.'
    ],
    vulnerable_groups: 'Village panchayats and community forestry committees.',
    checklist: [
      'Lay biodegradable coir geotextile netting on exposed scar',
      'Plant vetiver grass along horizontal contour lines',
      'Fence off revegetated slope from grazing livestock'
    ]
  },
  {
    id: 'lsd-aft-06',
    hazard: 'LANDSLIDE',
    phase: 'AFTER',
    category: 'DAMAGE_DOCUMENTATION',
    title: 'Register Land Loss & House Damage with District Revenue Authorities',
    instruction: 'File formal loss enumeration documents with local Revenue Inspector / Tahsildar for relief grants and resettlement assistance under the DM Act 2005.',
    priority: 'RECOMMENDED',
    reason: 'Landslide damage frequently involves total loss of land parcel; revenue documentation is necessary for statutory land reallocation and SDRF ex-gratia assistance.',
    source: 'Ministry of Home Affairs Calamity Compensation Guidelines',
    related_cascading_risk: 'Loss of land titles, landlessness, and protracted resettlement disputes.',
    practical_steps: [
      'Photograph all damaged buildings, cracked compound walls, and lost agricultural land.',
      'Collect land survey patta documents, Aadhaar cards, and bank passbooks.',
      'Submit written claim form to the Tahsildar / Sub-Divisional Magistrate (SDM) office.',
      'Ensure revenue survey team visits and records your GPS boundary coordinates in the official calamity register.'
    ],
    warning_signs: [
      'District administration announcing cutoff dates for landslide relief enumeration.'
    ],
    what_not_to_do: [
      'Do NOT miss the statutory filing window for government calamity enumeration.',
      'Do NOT alter boundary markers before the revenue survey is completed.'
    ],
    vulnerable_groups: 'Marginal farmers who have lost their entire terraced crop land.',
    checklist: [
      'Photograph destroyed property and land parcel scars',
      'Submit formal compensation claim to Tahsildar office',
      'Retain official stamped acknowledgment slip'
    ]
  },

  // =========================================================================
  // 6. EARTHQUAKE (Tectonic Baseline Awareness & Structural Safety)
  // =========================================================================
  // --- EARTHQUAKE: BEFORE ---
  {
    id: 'eqk-bef-01',
    hazard: 'EARTHQUAKE',
    phase: 'BEFORE',
    category: 'PROPERTY_PREPARATION',
    title: 'Fasten Tall Furniture, Heavy Bookcases & Water Heaters to Wall Studs',
    instruction: 'Anchor tall almirahs, heavy wardrobes, refrigerators, and wall-mounted geysers to masonry wall studs using heavy-duty metal L-brackets and expansion bolts.',
    priority: 'CRITICAL',
    reason: 'Over 55% of earthquake injuries are non-structural—caused by falling wardrobes, toppling refrigerators, and dislodged ceiling fans crushing sleeping occupants.',
    source: 'Bureau of Indian Standards (BIS) Non-Structural Earthquake Mitigation Guidelines',
    related_cascading_risk: 'Severe blunt force crush trauma, broken limbs, and internal bleeding.',
    practical_steps: [
      'Secure tall wooden and steel wardrobes to solid masonry walls using 50 mm steel L-brackets and anchor bolts.',
      'Install safety latches on upper kitchen cabinets so glass jars and crockery cannot fly open during shaking.',
      'Fasten heavy water geysers and domestic gas cylinders with metal straps bolted to walls.',
      'Place heavy books and metal objects on lower shelves rather than top shelves.'
    ],
    warning_signs: [
      'Heavy furniture wobbling freely when pushed by hand.',
      'Tall wardrobes leaning slightly forward away from wall.'
    ],
    what_not_to_do: [
      'Do NOT leave heavy metal storage trunks or heavy boxes on top of tall bedroom cupboards.',
      'Do NOT hang heavy glass-framed paintings, mirrors, or clocks directly over beds.'
    ],
    vulnerable_groups: 'Young children sleeping in bedrooms with tall unanchored furniture.',
    checklist: [
      'Anchor all wardrobes and bookcases to walls with L-brackets',
      'Install positive latches on upper kitchen cabinets',
      'Strap water geysers and LPG cylinders to solid walls'
    ]
  },
  {
    id: 'eqk-bef-02',
    hazard: 'EARTHQUAKE',
    phase: 'BEFORE',
    category: 'PROPERTY_PREPARATION',
    title: 'Identify Safe Interior Cover Spots in Every Room (Drop, Cover & Hold On)',
    instruction: 'Identify safe cover locations in advance: beneath sturdy wooden dining tables, desks, or interior doorframes; practice family earthquake drills.',
    priority: 'CRITICAL',
    reason: 'When intense seismic shaking strikes, you have under 3 seconds to take cover before being knocked to the ground; pre-identified safe spots save lives.',
    source: 'NDMA National Earthquake Guidelines & BIS IS 1893',
    related_cascading_risk: 'Crush trauma from falling ceiling plaster and concrete spall.',
    practical_steps: [
      'Identify sturdy furniture in every room (heavy wooden tables, sturdy desks).',
      'Practice the "Drop, Cover, and Hold On" drill with children: Drop to knees, Cover head under table, Hold on to table legs.',
      'Ensure hallways and exit paths are kept clear of clutter, shoes, and loose boxes.',
      'Designate an outside family reunion location in an open park or ground away from buildings.'
    ],
    warning_signs: [
      'Home situated in seismic Zone IV or Zone V (e.g. Northeast India, Delhi-NCR, Jammu & Kashmir, Uttarakhand, Kutch).'
    ],
    what_not_to_do: [
      'Do NOT plan to run outdoors during shaking; running during ground motion causes severe falls and exposes you to falling facade bricks.',
      'Do NOT choose doorway arches unless you know they are load-bearing reinforced concrete.'
    ],
    vulnerable_groups: 'Schoolchildren and elderly family members with limited mobility.',
    checklist: [
      'Identify sturdy desk/table cover spots in all rooms',
      'Conduct family "Drop, Cover, Hold On" practice drill',
      'Designate open ground family assembly point'
    ]
  },
  {
    id: 'eqk-bef-03',
    hazard: 'EARTHQUAKE',
    phase: 'BEFORE',
    category: 'UTILITY_SAFETY',
    title: 'Locate & Learn How to Shut Off Main Gas, Water & Electricity Supply',
    instruction: 'Ensure all adult family members know the exact location of the main electrical breaker, domestic LPG cylinder regulator, and main water valve.',
    priority: 'HIGH',
    reason: 'Ruptured gas pipes and severed electrical wiring cause catastrophic secondary fires that frequently destroy more property than the seismic ground shaking itself.',
    source: 'National Building Code (NBC) Fire & Life Safety Section',
    related_cascading_risk: 'Secondary urban conflagrations and water pipeline flooding.',
    practical_steps: [
      'Clearly label the main circuit breaker (MCB) and main water valve with reflective tags.',
      'Keep a suitable wrench or tool near gas valves and water meters.',
      'Show teenagers and family members how to turn off the LPG regulator valve smoothly.',
      'Inspect domestic flexible gas tubing; replace with BIS-certified steel-braided hose.'
    ],
    warning_signs: [
      'Corroded or stuck main water valves that cannot be turned by hand.',
      'Electrical breaker box located in dark, cluttered inaccessible corner.'
    ],
    what_not_to_do: [
      'Do NOT padlock the main electrical breaker panel in an inaccessible state.',
      'Do NOT store flammable paints or thinners near domestic gas cylinders.'
    ],
    vulnerable_groups: 'Teenagers or family members left alone at home.',
    checklist: [
      'Tag main electrical breaker and water shutoff valves',
      'Train all adult family members on gas shutoff procedure',
      'Replace aging rubber gas hose with wire-braided Suraksha hose'
    ]
  },
  {
    id: 'eqk-bef-04',
    hazard: 'EARTHQUAKE',
    phase: 'BEFORE',
    category: 'STRUCTURAL_SAFETY',
    title: 'Assess Building for Seismic Vulnerabilities (BIS IS 1893 Compliance)',
    instruction: 'Have a licensed structural engineer assess your building for soft-storey (open ground-floor stilt parking), floating columns, or unreinforced masonry.',
    priority: 'HIGH',
    reason: 'Over 80% of urban apartment collapses in Indian earthquakes (e.g. 2001 Bhuj) occur due to open ground-floor stilt parking (soft storeys) lacking shear walls.',
    source: 'Bureau of Indian Standards (BIS IS 1893: Criteria for Earthquake Resistant Design)',
    related_cascading_risk: 'Total pancake building collapse and mass structural entrapment.',
    practical_steps: [
      'Hire a chartered structural engineer to inspect building blueprints and column dimensions.',
      'Retrofit open stilt parking columns with steel jacketing, concrete encasement, or cross-bracing.',
      'Do not demolish load-bearing interior walls to create open-plan living rooms without engineering signoff.',
      'Check terrace overhead water tanks; ensure concrete supporting columns are seismically braced.'
    ],
    warning_signs: [
      'Building resting on open ground-floor stilt parking with no shear walls.',
      'Diagonal cracks visible at the corners of doors and windows in ground-floor pillars.'
    ],
    what_not_to_do: [
      'Do NOT remove ground-floor pillars or load-bearing walls for shop expansion.',
      'Do NOT add extra upper floors without structural foundation capacity verification.'
    ],
    vulnerable_groups: 'Residents of multi-storey apartment buildings with open stilt parking.',
    checklist: [
      'Request structural engineer seismic vulnerability audit',
      'Check building compliance with BIS IS 1893 seismic standards',
      'Brace overhead concrete water tank supporting pillars'
    ]
  },
  {
    id: 'eqk-bef-05',
    hazard: 'EARTHQUAKE',
    phase: 'BEFORE',
    category: 'PROPERTY_PREPARATION',
    title: 'Do Not Place Heavy Mirrors, Glass Cabinets or Clocks Over Beds',
    instruction: 'Keep beds away from large glass windows, heavy wall mirrors, and suspended lighting fixtures; secure picture frames with closed screw-hooks.',
    priority: 'RECOMMENDED',
    reason: 'Earthquake vibrations dislodge hanging glass objects, dropping heavy shards directly onto sleeping family members.',
    source: 'NDMA Non-Structural Earthquake Safety Guidelines',
    related_cascading_risk: 'Severe facial lacerations, arterial bleeding, and eye trauma.',
    practical_steps: [
      'Reposition beds away from windows and heavy glass-fronted bookcases.',
      'Hang framed artwork and mirrors using heavy-duty closed screw-eye hooks instead of open nails.',
      'Apply clear safety film on glass windows near beds to prevent shattering.',
      'Avoid placing heavy brass idols or metal artifacts on high bedroom shelves.'
    ],
    warning_signs: [
      'Heavy framed pictures hung on simple open nails above headboards.'
    ],
    what_not_to_do: [
      'Do NOT hang chandeliers or heavy ceiling fans directly above sleeping pillows.',
      'Do NOT place glass water carafes on bedside tables where they can shatter onto bare feet.'
    ],
    vulnerable_groups: 'Infants sleeping in cribs and elderly bedridden individuals.',
    checklist: [
      'Move beds away from windows and heavy wall hangings',
      'Use closed screw-eye hooks for wall-mounted frames',
      'Apply anti-shatter safety film to bedroom window panes'
    ]
  },
  {
    id: 'eqk-bef-06',
    hazard: 'EARTHQUAKE',
    phase: 'BEFORE',
    category: 'EMERGENCY_KIT',
    title: 'Prepare 72-Hour Survival Kit with Sturdy Shoes, Whistle & Dust Masks',
    instruction: 'Keep a portable emergency backpack with thick-soled shoes, dust masks (N95), heavy-duty torch, whistle, first aid kit, crowbar, and 3-day water supply.',
    priority: 'RECOMMENDED',
    reason: 'Following an earthquake, floors are covered with shattered glass, airborne pulverized concrete dust fills the air, and power/water grids fail completely.',
    source: 'NDMA Disaster Kit Guidelines',
    related_cascading_risk: 'Foot puncture wounds, dust inhalation respiratory distress, and dehydration.',
    practical_steps: [
      'Keep a pair of sturdy closed-toe shoes and a flashlight tied to every family member’s bedpost.',
      'Pack N95 dust masks to protect lungs from pulverized concrete and asbestos dust.',
      'Include a high-decibel whistle in the kit for signaling if trapped beneath rubble.',
      'Store minimum 3 litres drinking water per person and high-calorie non-perishable food.'
    ],
    warning_signs: [
      'Household completely unprepared with zero emergency supplies or stored water.'
    ],
    what_not_to_do: [
      'Do NOT keep the emergency grab bag locked in deep storage cupboards.',
      'Do NOT forget daily prescription medications and spare eyeglasses.'
    ],
    vulnerable_groups: 'All household members.',
    checklist: [
      'Tie sturdy shoes and flashlight to bedpost',
      'Pack N95 particulate respirators and emergency whistles',
      'Store 3-day water and food supply in grab bag'
    ]
  },

  // --- EARTHQUAKE: DURING ---
  {
    id: 'eqk-dur-01',
    hazard: 'EARTHQUAKE',
    phase: 'DURING',
    category: 'SHELTER',
    title: 'DROP, COVER, AND HOLD ON Immediately at First Sign of Shaking',
    instruction: 'DROP to your hands and knees; COVER your head and neck under a sturdy table or desk; HOLD ON to your shelter until shaking stops. If no table nearby, cover head against interior wall.',
    priority: 'CRITICAL',
    reason: 'Ground motion during severe earthquakes knocks standing humans off their feet, causing severe hip and head fractures; sheltering beneath furniture protects against falling concrete chunks.',
    source: 'NDMA National Earthquake Safety Standard & International ShakeOut Protocol',
    warning: 'Do NOT run outdoors during shaking! Parapets, signboards, and falling glass shards cause over 70% of casualties outside.',
    related_cascading_risk: 'Traumatic brain injury, skull fractures, and fatal crush injuries.',
    practical_steps: [
      'DROP immediately to hands and knees before the violent shaking knocks you down.',
      'COVER your head and neck under a sturdy wooden table, desk, or reinforced bench.',
      'HOLD ON to the table leg with one hand; be prepared to move with the table as it shifts across the floor.',
      'If in bed, stay in bed; curl face down and cover head and neck with a thick pillow.'
    ],
    warning_signs: [
      'Sudden deep rumbling noise followed by sharp vertical jolt and violent swaying.',
      'Hanging lamps swinging wildly and glassware rattling off shelves.'
    ],
    what_not_to_do: [
      'Do NOT run outside while the ground is actively shaking.',
      'Do NOT stand under unreinforced doorways; modern doors often swing violently and crush fingers.',
      'Do NOT dive down stairwells or attempt to jump from balconies.'
    ],
    vulnerable_groups: 'Elderly persons who cannot drop quickly; they should sit low in an interior corner and cover head with pillow.',
    checklist: [
      'Drop immediately to hands and knees',
      'Cover head and neck beneath sturdy table or desk',
      'Hold on firmly to table leg until shaking ceases'
    ]
  },
  {
    id: 'eqk-dur-02',
    hazard: 'EARTHQUAKE',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Never Use Elevators; Avoid Rushing Down Crowded Stairwells',
    instruction: 'Never use elevators during an earthquake; do not rush down crowded stairwells during active shaking. Wait for shaking to stop, then take stairs.',
    priority: 'CRITICAL',
    reason: 'Elevator counterweights jump track guides during seismic sway, severing cables and trapping occupants between floors; building power cuts out immediately.',
    source: 'Bureau of Indian Standards Elevator Safety Code & NDMA Guidelines',
    related_cascading_risk: 'Elevator shaft entrapment, panic stampedes, and stairwell collapse.',
    practical_steps: [
      'If inside an elevator when shaking begins, press buttons for all upcoming floors immediately; exit as soon as doors open and take cover.',
      'If inside an apartment building, remain inside under sturdy cover until the ground stops moving completely.',
      'When shaking ceases, use reinforced concrete stairwells calmly; hold handrail.',
      'Watch for cracked stair treads and dislodged handrails as you descend.'
    ],
    warning_signs: [
      'Alarm bells ringing in elevator shafts.',
      'Stairwell lights flickering out and emergency lights activating.'
    ],
    what_not_to_do: [
      'Do NOT enter an elevator during or immediately following an earthquake.',
      'Do NOT push or stampede on staircases; panic stampedes cause fatal crushing.'
    ],
    vulnerable_groups: 'Residents of high-rise apartment towers (Zone IV and V).',
    checklist: [
      'Never step into an elevator during or after shaking',
      'Wait for shaking to stop before taking stairs',
      'Descend stairwell calmly holding the handrail'
    ]
  },
  {
    id: 'eqk-dur-03',
    hazard: 'EARTHQUAKE',
    phase: 'DURING',
    category: 'SAFE_ROUTES_EVACUATION',
    title: 'If Outdoors, Move to Open Ground Away from Buildings & Cables',
    instruction: 'If outdoors, move immediately to open ground away from high-rise buildings, brick boundary walls, glass facades, and overhead electrical power lines.',
    priority: 'HIGH',
    reason: 'Falling masonry, window glass, air-conditioner compressors, and shattered parapets peel off building facades, falling into the 5-metre "kill zone" around building bases.',
    source: 'NDMA Outdoor Earthquake Guidelines',
    related_cascading_risk: 'Direct impact from falling facade bricks, glass rain, and electrocution.',
    practical_steps: [
      'Move quickly to an open park, sports ground, or wide road away from tall structures.',
      'Drop to hands and knees in the open ground until shaking stops to prevent being thrown.',
      'Cover your head with a bag, briefcase, or your arms.',
      'Stay away from tall brick boundary walls, chimneys, and overhead electrical distribution poles.'
    ],
    warning_signs: [
      'Glass shards showering down onto pavements from high-rise windows.',
      'Brick parapets cracking and peeling off building roof edges.'
    ],
    what_not_to_do: [
      'Do NOT stand under building awnings, porticos, or overhangs for shelter.',
      'Do NOT touch fallen utility lines or metal lampposts.'
    ],
    vulnerable_groups: 'Pedestrians on crowded city footpaths and market streets.',
    checklist: [
      'Move immediately to open park or wide roadway',
      'Maintain 10+ metres distance from building exterior walls',
      'Drop low and protect head until shaking ceases'
    ]
  },
  {
    id: 'eqk-dur-04',
    hazard: 'EARTHQUAKE',
    phase: 'DURING',
    category: 'TRANSPORTATION',
    title: 'If Driving, Pull Over Safely Away from Flyovers & Bridges; Stay Inside',
    instruction: 'Slow down smoothly and pull vehicle to the road shoulder away from flyovers, bridges, cut slopes, and overhead cables; stay inside vehicle with parking brake on.',
    priority: 'HIGH',
    reason: 'Violent shaking feels like driving on flat tires and can cause total loss of steering control; flyovers and bridges experience severe dynamic displacement.',
    source: 'Ministry of Road Transport & Highways Seismic Safety Advisory',
    related_cascading_risk: 'Flyover joint collapse, vehicle rollovers, and multi-car highway collisions.',
    practical_steps: [
      'Avoid stopping directly underneath or on top of overpasses, bridges, or flyovers.',
      'Turn on hazard warning flashers and pull safely to the left road shoulder.',
      'Set parking brake firmly and keep seatbelt fastened.',
      'Stay inside vehicle until shaking stops completely; the vehicle’s suspension acts as a shock absorber.'
    ],
    warning_signs: [
      'Car swaying violently and steering pulling hard to one side.',
      'Expansion joints on bridges opening and clattering loudly.'
    ],
    what_not_to_do: [
      'Do NOT stop your car underneath a highway flyover or pedestrian footbridge.',
      'Do NOT exit vehicle while electrical cables are falling onto the road.'
    ],
    vulnerable_groups: 'Highway drivers and bridge commuters.',
    checklist: [
      'Pull car safely onto road shoulder away from flyovers',
      'Engage parking brake and turn on hazard flashers',
      'Remain inside vehicle with seatbelt fastened until shaking stops'
    ]
  },
  {
    id: 'eqk-dur-05',
    hazard: 'EARTHQUAKE',
    phase: 'DURING',
    category: 'EMERGENCY_CONTACTS',
    title: 'If Trapped in Rubble, Tap on Pipes & Blow Whistle; Avoid Shouting',
    instruction: 'If trapped under collapsed debris: protect mouth with cloth, do not light matches, tap on metal pipes or masonry walls with a stone, and blow a whistle for search teams.',
    priority: 'CRITICAL',
    reason: 'Shouting exhausts vital oxygen and causes inhalation of lethal toxic concrete dust; tapping on metal pipes carries acoustic vibrations hundreds of metres to rescue geophones.',
    source: 'NDRF Search and Rescue Operational Standard',
    warning: 'Do not light matches or cigarette lighters beneath rubble; escaping natural gas will trigger instant explosion.',
    related_cascading_risk: 'Dust inhalation asphyxiation, dehydration, and secondary explosion.',
    practical_steps: [
      'Cover your nose and mouth with a piece of clothing or handkerchief to filter out thick dust.',
      'Look for an exit or void space; do not kick violently, which can trigger secondary collapses.',
      'Find a rock, brick, or piece of metal; tap rhythmically in sets of three (tap-tap-tap) on a metal pipe or concrete beam.',
      'Shout only as a last resort when you hear human voices directly overhead.'
    ],
    warning_signs: [
      'Thick concrete dust cloud settling in void space.',
      'Sound of search dogs barking or acoustic probe sensors tapping overhead.'
    ],
    what_not_to_do: [
      'Do NOT light a match or lighter under rubble under any circumstance.',
      'Do NOT shout continuously and waste your energy and oxygen.'
    ],
    vulnerable_groups: 'Entrapped victims in collapsed building voids.',
    checklist: [
      'Cover nose and mouth with cloth against concrete dust',
      'Tap rhythmically on metal pipe or concrete wall with stone',
      'Blow whistle in sets of three bursts when hearing rescuers'
    ]
  },
  {
    id: 'eqk-dur-06',
    hazard: 'EARTHQUAKE',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'If in Crowded Public Place (Cinema, Mall), Do Not Rush for Exits',
    instruction: 'If inside a crowded mall, auditorium, or stadium, do not rush for exit doors; drop between seat rows, cover your head, and protect yourself from stampedes.',
    priority: 'HIGH',
    reason: 'Panic stampedes at narrow theater or stadium exit doors cause massive crush fatalities far exceeding the direct structural damage of the earthquake.',
    source: 'NDMA Crowd Management Guidelines in Disasters',
    related_cascading_risk: 'Human stampedes, crushing, and doorway blockages.',
    practical_steps: [
      'Drop between seat rows or alongside interior counter bases.',
      'Cover your head and neck with your arms, coat, or backpack.',
      'Stay calm and shout "Stay Calm! Protect Your Heads!" to deter stampedes.',
      'When shaking stops, exit in an orderly line following illuminated emergency exit signs.'
    ],
    warning_signs: [
      'Crowds shouting and surging en masse towards exit doors.',
      'Ceiling acoustic panels and track lighting crashing down.'
    ],
    what_not_to_do: [
      'Do NOT join a frantic rushing crowd heading towards a narrow doorway.',
      'Do NOT push, shove, or jump over seated patrons.'
    ],
    vulnerable_groups: 'Cinema-goers, mall shoppers, and sports stadium attendees.',
    checklist: [
      'Drop low between seat rows and cover head with bag',
      'Wait for ground shaking to cease completely',
      'Follow emergency exit signs calmly without running'
    ]
  },

  // --- EARTHQUAKE: AFTER ---
  {
    id: 'eqk-aft-01',
    hazard: 'EARTHQUAKE',
    phase: 'AFTER',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Expect Severe Aftershocks; Evacuate Damaged Buildings Carefully',
    instruction: 'Expect powerful aftershocks within minutes, hours, and days; carefully evacuate structurally compromised buildings taking stairs and wearing sturdy shoes.',
    priority: 'CRITICAL',
    reason: 'Aftershocks frequently register magnitude 5.0 to 6.5+, causing total collapse of structures already weakened or sheared by the main shock.',
    source: 'National Centre for Seismology (NCS) & NDMA Guidelines',
    warning: 'Never re-enter a building that has visible diagonal shear cracks or leaning pillars to retrieve possessions.',
    related_cascading_risk: 'Secondary structural collapse from aftershock tremors.',
    practical_steps: [
      'Put on sturdy shoes before stepping onto debris-covered floors.',
      'Grab your 72-hour emergency backpack and waterproof document pouch.',
      'Descend via exterior or reinforced stairwells; do NOT touch damaged railings.',
      'Move to pre-designated open assembly park or ground at least building-height distance away.'
    ],
    warning_signs: [
      'Secondary tremors and shaking felt within minutes of main shock.',
      'Plaster continuing to fall and creaking sounds from building joints.'
    ],
    what_not_to_do: [
      'Do NOT return inside a damaged building to retrieve jewelry, laptops, or pets.',
      'Do NOT stand directly beneath overhanging balconies or parapets while exiting.'
    ],
    vulnerable_groups: 'Residents of multi-storey apartment buildings.',
    checklist: [
      'Put on sturdy shoes immediately post-shaking',
      'Evacuate via stairs carrying emergency grab bag',
      'Assemble in open ground away from building facades'
    ]
  },
  {
    id: 'eqk-aft-02',
    hazard: 'EARTHQUAKE',
    phase: 'AFTER',
    category: 'UTILITY_SAFETY',
    title: 'Check for Gas Leaks; If Smelling Gas, Evacuate & Dial 1906',
    instruction: 'Check for gas leaks immediately; if you smell gas (sulfur/rotten eggs) or hear hissing, open windows, evacuate immediately, and dial 1906 (Gas Leak Emergency).',
    priority: 'CRITICAL',
    reason: 'Ruptured domestic cooking gas cylinders and municipal piped natural gas (PNG) mains cause catastrophic post-earthquake infernos.',
    source: 'Petroleum and Natural Gas Regulatory Board (PNGRB) Emergency Protocol',
    warning: 'Do not flip any electrical switch on or off; the tiny electrical spark inside the switch can trigger an instant gas explosion.',
    related_cascading_risk: 'Massive residential gas explosions and urban firestorms.',
    practical_steps: [
      'Smell for gas odor as you move through rooms.',
      'If gas odor is detected, turn off the cylinder regulator knob or PNG meter valve if safe to reach.',
      'Do NOT touch any electrical switches, do NOT use landline phones, and do NOT light matches.',
      'Evacuate all occupants outdoors immediately; call 1906 from a safe distance.'
    ],
    warning_signs: [
      'Rotten egg / sulfur odor of mercaptan gas odorant.',
      'Hissing sounds near kitchen gas pipeline or cylinder.'
    ],
    what_not_to_do: [
      'Do NOT switch lights on or off (the spark inside the switch is an ignition source).',
      'Do NOT use lighters or matches to inspect dark rooms; use only battery torches.'
    ],
    vulnerable_groups: 'Households using piped natural gas (PNG) or multiple domestic LPG cylinders.',
    checklist: [
      'Check kitchen for gas odor or hissing sounds',
      'Shut off gas cylinder regulator if safely accessible',
      'Evacuate building immediately and call 1906 from outside'
    ]
  },
  {
    id: 'eqk-aft-03',
    hazard: 'EARTHQUAKE',
    phase: 'AFTER',
    category: 'PROPERTY_PREPARATION',
    title: 'Wear Thick-Soled Shoes & Gloves to Avoid Glass Lacerations',
    instruction: 'Put on thick-soled boots and heavy work gloves before walking across rooms or beginning debris clearance; avoid walking barefoot.',
    priority: 'HIGH',
    reason: 'Shattered window glass, broken mirrors, and jagged masonry fragments cover floors; foot lacerations paralyze victims and cause severe blood loss.',
    source: 'NDMA First Aid & Evacuation Safety Guide',
    related_cascading_risk: 'Severe plantar lacerations, severed tendons, and tetanus infections.',
    practical_steps: [
      'Keep boots right beside your bed at all times so they can be slipped on in seconds.',
      'Put on heavy leather or rubber work gloves before touching door handles or clearing rubble.',
      'Sweep a narrow clear path through broken glass if family members lack footwear.',
      'Do not allow children to step onto floor until their shoes are secured.'
    ],
    warning_signs: [
      'Floor covered in shattered window panes and broken crockery.'
    ],
    what_not_to_do: [
      'Do NOT walk barefoot or in thin socks across earthquake-damaged rooms.',
      'Do NOT handle sharp glass shards without protective gloves.'
    ],
    vulnerable_groups: 'Children and seniors who walk barefoot inside Indian homes.',
    checklist: [
      'Slip on thick-soled shoes before taking a single step',
      'Wear leather work gloves before moving debris',
      'Verify children have closed-toe shoes secured'
    ]
  },
  {
    id: 'eqk-aft-04',
    hazard: 'EARTHQUAKE',
    phase: 'AFTER',
    category: 'UTILITY_SAFETY',
    title: 'Extinguish Small Household Fires Immediately (Before Water Pressure Fails)',
    instruction: 'Extinguish small localized kitchen or electrical fires immediately using a fire extinguisher, sand, or water bucket before municipal water mains fail.',
    priority: 'HIGH',
    reason: 'Post-earthquake fires expand exponentially; once municipal water mains rupture, fire brigade hydrants have zero water pressure and cannot control conflagrations.',
    source: 'Fire Protection Association & NDMA Fire Safety Norms',
    related_cascading_risk: 'Uncontrolled urban block firestorms consuming entire neighborhoods.',
    practical_steps: [
      'Operate domestic ABC dry chemical fire extinguisher (PASS technique: Pull pin, Aim nozzle, Squeeze handle, Sweep base of fire).',
      'Smother small kitchen grease fires with a metal lid or damp blanket; NEVER pour water on oil fires.',
      'If fire cannot be extinguished within 30 seconds, evacuate the building immediately and alert neighbors.',
      'Close doors behind you as you exit to slow the fire’s oxygen supply.'
    ],
    warning_signs: [
      'Smoke rising from kitchen or behind electrical distribution board.',
      'Small flames licking up curtains from toppled decorative lamps.'
    ],
    what_not_to_do: [
      'Do NOT attempt to fight a fire that has reached the ceiling or blocked your exit path.',
      'Do NOT pour water on electrical or cooking oil fires.'
    ],
    vulnerable_groups: 'Residents in high-density urban residential colonies.',
    checklist: [
      'Discharge fire extinguisher at base of small fires',
      'Smother small grease fires with heavy damp blanket',
      'Evacuate immediately if fire cannot be contained in 30s'
    ]
  },
  {
    id: 'eqk-aft-05',
    hazard: 'EARTHQUAKE',
    phase: 'AFTER',
    category: 'STRUCTURAL_SAFETY',
    title: 'Inspect Load-Bearing Pillars & Roof Joints for Diagonal Shear Cracks',
    instruction: 'Inspect concrete columns, load-bearing brick walls, and beam-column joints for X-shaped diagonal shear cracks before considering re-entry.',
    priority: 'CRITICAL',
    reason: 'X-shaped diagonal shear cracking in reinforced concrete columns indicates near-total loss of vertical load-bearing capacity; collapse is imminent during aftershocks.',
    source: 'NDMA Post-Earthquake Rapid Structural Safety Assessment Guidelines',
    warning: 'Never enter a building exhibiting X-shaped diagonal shear cracks in columns or crushed concrete at pillar bases.',
    related_cascading_risk: 'Sudden building collapse during aftershocks.',
    practical_steps: [
      'Examine ground-floor columns for vertical spalling, exposed rebar, or X-shaped cracks.',
      'Check if building is visibly tilting or separated from neighboring structures.',
      'Look for horizontal cracks at beam-column junctions.',
      'Tag building RED (Unsafe - Do Not Enter) until municipal structural engineers complete audit.'
    ],
    warning_signs: [
      'X-shaped diagonal cracks wider than 3 mm in concrete columns.',
      'Concrete crumbled and crushed at top or bottom of structural pillars.'
    ],
    what_not_to_do: [
      'Do NOT enter a building tagged with red X-marks or yellow warning tape.',
      'Do NOT attempt temporary amateur patching of cracked structural columns.'
    ],
    vulnerable_groups: 'Homeowners anxious to inspect belongings.',
    checklist: [
      'Inspect columns for X-shaped diagonal shear cracks',
      'Check for exposed or buckled steel reinforcement bars',
      'Do not re-enter premises without certified structural clearance'
    ]
  },
  {
    id: 'eqk-aft-06',
    hazard: 'EARTHQUAKE',
    phase: 'AFTER',
    category: 'FAMILY_COMMUNICATION',
    title: 'Tune to Official Radio & Keep Telephone Lines Free for SOS Calls',
    instruction: 'Listen to All India Radio or official DDMA emergency broadcasts; use SMS or text messaging instead of voice calls to keep cellular channels open for 112 SOS calls.',
    priority: 'RECOMMENDED',
    reason: 'Cellular networks experience extreme network congestion post-earthquake; SMS texts consume 1% of the bandwidth of voice calls and successfully queue through congested towers.',
    source: 'National Disaster Response Force (NDRF) Communication SOP',
    related_cascading_risk: 'Cellular network crash blocking life-saving 112 and 108 emergency calls.',
    practical_steps: [
      'Send a single brief SMS to family: "I AM SAFE. ASSEMBLED AT [LOCATION]".',
      'Do not make non-urgent phone calls; leave network capacity open for disaster rescue coordination.',
      'Listen to your battery-operated transistor radio for official updates from the District Collector.',
      'Do not forward unverified WhatsApp rumors regarding earthquake predictions or dam failures.'
    ],
    warning_signs: [
      'Phone displaying "Network Busy" or "Call Failed" due to severe tower congestion.',
      'Viral rumors on social media claiming "next earthquake at 4 PM" (scientifically impossible).'
    ],
    what_not_to_do: [
      'Do NOT spread unverified panic messages on social media; earthquake timing cannot be predicted.',
      'Do NOT tie up emergency lines (112 / 108) with non-emergency inquiries.'
    ],
    vulnerable_groups: 'Citizens separated from family members in different parts of the city.',
    checklist: [
      'Send single "I AM SAFE" SMS to family contacts',
      'Tune battery radio to All India Radio disaster broadcast',
      'Avoid circulating unverified social media earthquake rumors'
    ]
  }
];
