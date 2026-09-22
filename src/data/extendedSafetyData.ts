/**
 * RISK // INDIA — Extended Citizen Disaster Safety Guidance Static Dataset
 * =========================================================================
 * Comprehensive Before / During / After life-safety guidelines across all 6 hazards.
 * Aligned with NDMA Standard Operating Procedures, IMD Guidelines, and the Disaster Management Act 2005.
 * Enables zero-latency searching, filtering, and offline resilience for citizen safety.
 */

import { SafetyInstructionItem, HazardSafetyGuide } from '../types/safetyGuide';

export const EXTENDED_SAFETY_ITEMS: SafetyInstructionItem[] = [
  // =========================================================================
  // FLOOD
  // =========================================================================
  {
    id: 'fld-bef-01',
    hazard: 'FLOOD',
    phase: 'BEFORE',
    category: 'WATER_AND_FOOD',
    title: 'Store Potable Drinking Water in Sealed Containers',
    instruction: 'Store a minimum of 3 to 4 litres of clean drinking water per person per day for at least 3 days in clean, food-grade containers.',
    priority: 'CRITICAL',
    reason: 'Floodwaters submerge municipal distribution pipes and open wells, introducing toxic bacteria, sewage, and chemical runoff into the drinking supply.',
    source: 'NDMA National Disaster Management Guidelines: Management of Floods (Section 4.3)',
    warning: 'Do not rely on municipal taps once floodwaters approach your street.',
    related_cascading_risk: 'Water supply contamination and enteric waterborne epidemics.'
  },
  {
    id: 'fld-bef-02',
    hazard: 'FLOOD',
    phase: 'BEFORE',
    category: 'CRITICAL_DOCUMENTS',
    title: 'Secure Important Documents in Watertight Pouches',
    instruction: 'Place Aadhaar cards, voter IDs, ration cards, property deeds, birth certificates, and insurance policies into sealed waterproof ziplock pouches near your exit.',
    priority: 'HIGH',
    reason: 'Identity proof and property records are required for statutory calamity relief disbursement, ex-gratia claims, and insurance verification under the DM Act 2005.',
    source: 'Ministry of Home Affairs / NDMA Calamity Relief Documentation SOP',
    related_cascading_risk: 'Prolonged recovery delays due to loss of statutory identification.'
  },
  {
    id: 'fld-bef-03',
    hazard: 'FLOOD',
    phase: 'BEFORE',
    category: 'SAFE_ROUTES_EVACUATION',
    title: 'Map High Ground & Designated Community Shelters',
    instruction: 'Identify multiple high-ground evacuation paths to designated community multi-purpose flood shelters, elevated school buildings, or reinforced concrete structures.',
    priority: 'CRITICAL',
    reason: 'Low-lying roads and culverts flood rapidly and may become impassable hours before peak river crest.',
    source: 'CWC Flood Forecasting & Inundation Mapping Handbook',
    warning: 'Never plan an evacuation route that crosses low-water bridges or earthen causeways.',
    related_cascading_risk: 'Road washouts and community isolation.'
  },
  {
    id: 'fld-bef-04',
    hazard: 'FLOOD',
    phase: 'BEFORE',
    category: 'VULNERABLE_MEMBERS',
    title: 'Prioritize Support Plan for Elderly, Children & Persons with Disabilities',
    instruction: 'Arrange early transport for elderly family members, infants, pregnant women, and persons with disabilities to elevated relatives\' homes before road access degrades.',
    priority: 'CRITICAL',
    reason: 'Mobility-impaired and medically vulnerable individuals cannot navigate sudden moving floodwaters or swift evacuations.',
    source: 'NDMA Guidelines on Disability Inclusive Disaster Risk Reduction (DiDRR)',
    related_cascading_risk: 'Emergency rescue bottlenecks during rapid inundation.'
  },
  {
    id: 'fld-bef-05',
    hazard: 'FLOOD',
    phase: 'BEFORE',
    category: 'PETS_AND_LIVESTOCK',
    title: 'Move Livestock & Working Animals to Elevated Embankments',
    instruction: 'Untie domestic cattle and livestock; move them to elevated community highlands or embankments. Stock dry fodder on raised bamboo platforms.',
    priority: 'HIGH',
    reason: 'Tethered animals drown when floodwaters rise rapidly. Untying allows natural survival instincts.',
    source: 'Department of Animal Husbandry and Dairying Disaster Management Plan',
    warning: 'Never leave cattle tied to sheds in low-lying flood-prone areas.',
    related_cascading_risk: 'Livestock mortality causing post-flood biological contamination.'
  },
  {
    id: 'fld-bef-06',
    hazard: 'FLOOD',
    phase: 'BEFORE',
    category: 'PROPERTY_PREPARATION',
    title: 'Install Sewer Backflow Valves & Clear Storm Drains',
    instruction: 'Install simple check valves or plug ground-floor toilet drains with sandbags to prevent sewage backflow; clear neighborhood runoff culverts of plastic blockages.',
    priority: 'RECOMMENDED',
    reason: 'Rising stormwater exerts back-pressure into municipal sewer mains, driving contaminated blackwater into ground-floor habitations.',
    source: 'CPHEEO Urban Drainage Manual',
    related_cascading_risk: 'Urban waterlogging and indoor sanitation failure.'
  },
  {
    id: 'fld-dur-01',
    hazard: 'FLOOD',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Never Walk, Swim, or Drive Through Moving Floodwater',
    instruction: 'Adhere strictly to the Six-Inch / Two-Foot Rule: Just 15 cm (6 inches) of moving water can knock down an adult; 30 cm can float a small car; 60 cm can sweep away an SUV.',
    priority: 'CRITICAL',
    reason: 'Moving water exerts immense hydrodynamic pressure, and submerged road surfaces may have been entirely washed away beneath murky water.',
    source: 'NDMA Standard Operating Procedure for Flood Response',
    warning: 'Turn Around, Don\'t Drown! Over 50% of flood fatalities occur in vehicles attempting to cross submerged roads.',
    related_cascading_risk: 'Culvert scour and vehicular drowning.'
  },
  {
    id: 'fld-dur-02',
    hazard: 'FLOOD',
    phase: 'DURING',
    category: 'UTILITY_SAFETY',
    title: 'Shut Off Main Electrical Breaker & LPG Gas Cylinders',
    instruction: 'Turn off your home\'s main electrical breaker switch and close the regulator valves of all domestic cooking gas (LPG) cylinders before evacuating.',
    priority: 'CRITICAL',
    reason: 'Water submerged electrical outlets cause lethal electrocution; displaced buoyant gas cylinders can rupture pipes and trigger explosions.',
    source: 'Central Electricity Authority (CEA) Safety Regulations',
    warning: 'Do not touch the electrical switch panel if you are already standing in water.',
    related_cascading_risk: 'Electrical short-circuit fires and underwater electrification.'
  },
  {
    id: 'fld-dur-03',
    hazard: 'FLOOD',
    phase: 'DURING',
    category: 'SAFE_ROUTES_EVACUATION',
    title: 'Comply Instantly with Statutory Evacuation Orders',
    instruction: 'Evacuate immediately upon announcement of official directives by the District Magistrate / SDMA / NDRF. Do not delay waiting for water to enter the house.',
    priority: 'CRITICAL',
    reason: 'Under Section 30 of the Disaster Management Act 2005, district authorities order evacuations based on upstream dam discharge and hydrological crest models.',
    source: 'Disaster Management Act 2005 (Statutory Framework)',
    warning: 'Self-evacuation during the day is far safer than dangerous night-time boat rescue operations.',
    related_cascading_risk: 'Stranded populations requiring aerial or boat rescue.'
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
    related_cascading_risk: 'Hypothermia and acute exposure.'
  },
  {
    id: 'fld-aft-01',
    hazard: 'FLOOD',
    phase: 'AFTER',
    category: 'RECOVERY_AND_HEALTH',
    title: 'Boil All Water Vigorously for 1 Minute Before Consumption',
    instruction: 'Boil all tap water, open well water, and tube-well water vigorously for at least 1 full minute (or use certified chlorine halogen tablets) before drinking, cooking, or brushing teeth.',
    priority: 'CRITICAL',
    reason: 'Floodwaters carry sewage pathogens, Escherichia coli, Vibrio cholerae, and Leptospira interrogans bacteria, causing cholera, acute gastroenteritis, and leptospirosis.',
    source: 'National Centre for Disease Control (NCDC) Post-Disaster Health Advisory',
    warning: 'Water filters alone may not eliminate viral contaminants if backflow pressure damaged the membrane.',
    related_cascading_risk: 'Leptospirosis and waterborne diarrheal epidemics.'
  },
  {
    id: 'fld-aft-02',
    hazard: 'FLOOD',
    phase: 'AFTER',
    category: 'PROPERTY_PREPARATION',
    title: 'Inspect Building Foundation Walls for Structural Cracks',
    instruction: 'Inspect perimeter walls, pillars, and foundations for new structural cracks, soil settlement, or scouring before allowing family members to re-enter premises.',
    priority: 'CRITICAL',
    reason: 'Prolonged waterlogging softens sub-surface foundation soil, leading to differential settlement and sudden structural collapse hours after water recedes.',
    source: 'NDMA Post-Flood Structural Safety Audit Manual',
    warning: 'Do not enter if walls are bowed, plaster is falling heavily, or doors are jammed.',
    related_cascading_risk: 'Secondary structural building collapse.'
  },
  {
    id: 'fld-aft-03',
    hazard: 'FLOOD',
    phase: 'AFTER',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Beware of Displaced Venomous Snakes, Scorpions & Rodents',
    instruction: 'Use a long stick to poke into shoes, bedding, cupboards, and ceiling crevices before reaching with bare hands. Wear sturdy boots while cleaning sludge.',
    priority: 'HIGH',
    reason: 'Displaced venomous snakes (Cobra, Russell\'s viper, Krait) seek dry refuge inside homes, furniture, and vehicles during and after floods.',
    source: 'State Health Departments Anti-Snake Venom (ASV) Protocol',
    warning: 'Never reach into dark corners or under debris with unprotected hands.',
    related_cascading_risk: 'Post-flood snakebite morbidity spikes.'
  },
  {
    id: 'fld-aft-04',
    hazard: 'FLOOD',
    phase: 'AFTER',
    category: 'DAMAGE_DOCUMENTATION',
    title: 'Photograph and Document All Damage Before Cleaning',
    instruction: 'Take clear date-stamped photographs and videos of flood waterline marks on walls, damaged furniture, appliances, crops, and structures before discarding items.',
    priority: 'RECOMMENDED',
    reason: 'Visual evidence is mandatory for revenue department damage assessment surveys (Girdawari), State Disaster Response Fund (SDRF) relief, and insurance claims.',
    source: 'Disaster Management Division, Ministry of Home Affairs SDRF Guidelines',
    related_cascading_risk: 'Delayed statutory financial relief disbursement.'
  },

  // =========================================================================
  // CYCLONE
  // =========================================================================
  {
    id: 'cyc-bef-01',
    hazard: 'CYCLONE',
    phase: 'BEFORE',
    category: 'PROPERTY_PREPARATION',
    title: 'Board Up Glass Windows & Anchor Corrugated Roofing',
    instruction: 'Board up large glass windows or apply heavy-duty criss-cross tape to prevent shattering; securely anchor or remove loose tin sheets, solar panels, and asbestos roofing.',
    priority: 'CRITICAL',
    reason: 'High gale winds transform loose corrugated roofing sheets into lethal airborne projectiles traveling at over 120 km/h.',
    source: 'IMD Cyclone Warning Services SOP',
    related_cascading_risk: 'Flying debris trauma and structural roof shearing.'
  },
  {
    id: 'cyc-bef-02',
    hazard: 'CYCLONE',
    phase: 'BEFORE',
    category: 'POWER_AND_LIGHTING',
    title: 'Fully Charge All Phones, Solar Lanterns & Power Banks',
    instruction: 'Charge mobile phones, rechargeable lanterns, and auxiliary power banks to 100%. Write essential family contact numbers on paper in case of battery depletion.',
    priority: 'HIGH',
    reason: 'Power grids are preemptively shut down during cyclones to prevent electrocution and fires from fallen lines, often resulting in 3 to 7 days of blackout.',
    source: 'State Disaster Management Authorities Coastal SOP',
    related_cascading_risk: 'Prolonged power grid failure and telecommunications blackout.'
  },
  {
    id: 'cyc-bef-03',
    hazard: 'CYCLONE',
    phase: 'BEFORE',
    category: 'SAFE_ROUTES_EVACUATION',
    title: 'Evacuate Kutcha / Thatched Houses to Pucca Cyclone Shelters',
    instruction: 'If residing in a kutcha, asbestos, or mud-brick house within 5 km of the coast, evacuate to a dedicated multi-purpose cyclone shelter before winds reach gale force.',
    priority: 'CRITICAL',
    reason: 'Kutcha structures cannot withstand sustained cyclonic wind pressures (> 90 km/h) or storm surge inundation exceeding 1.5 meters.',
    source: 'National Cyclone Risk Mitigation Project (NCRMP) Guidelines',
    warning: 'Never stay inside a thatched or tin-roof house once an Orange or Red cyclone alert is issued.',
    related_cascading_risk: 'Catastrophic structural collapse under aerodynamic wind load.'
  },
  {
    id: 'cyc-dur-01',
    hazard: 'CYCLONE',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Do NOT Venture Outdoors During the Calm \'Eye\' of the Cyclone',
    instruction: 'If winds suddenly stop and the sky clears, stay indoors! The \'eye\' of the cyclone is passing; violent gale winds will resume abruptly from the opposite direction.',
    priority: 'CRITICAL',
    reason: 'The central eye of a tropical cyclone features deceptive calm; reverse winds on the back-side of the eyewall strike with maximum destructive fury without warning.',
    source: 'IMD Forecasters Manual for Tropical Cyclones',
    warning: 'Many casualties occur when people venture out during the eye to inspect damage.',
    related_cascading_risk: 'Violent wind reversals catching citizens exposed outdoors.'
  },
  {
    id: 'cyc-dur-02',
    hazard: 'CYCLONE',
    phase: 'DURING',
    category: 'SAFE_ROUTES_EVACUATION',
    title: 'Shelter in the Strongest Interior Room Away from Windows',
    instruction: 'Stay in the central reinforced room or hallway of the house. Keep blankets and mattresses nearby to shield against falling plaster or flying glass shards.',
    priority: 'CRITICAL',
    reason: 'Internal partition walls provide the highest structural rigidity and are protected from direct exterior aerodynamic wind blast.',
    source: 'NDMA Cyclone Management Guidelines',
    related_cascading_risk: 'Flying glass splinter lacerations.'
  },
  {
    id: 'cyc-aft-01',
    hazard: 'CYCLONE',
    phase: 'AFTER',
    category: 'UTILITY_SAFETY',
    title: 'Treat All Downed Electrical Cables as Live and Lethal',
    instruction: 'Do not touch or approach fallen electrical poles, dangling service wires, or corrugated metal fences touching wet ground. Keep a minimum 10-meter clearance.',
    priority: 'CRITICAL',
    reason: 'Snapped conductors can remain energized by back-feeding from residential inverters or delayed sub-station trips, carrying fatal voltages across wet soil.',
    source: 'Central Electricity Authority Safety Handbook',
    warning: 'Never drive over downed power lines entangled in tree branches.',
    related_cascading_risk: 'Electrocution from grounded electrical lines.'
  },
  {
    id: 'cyc-aft-02',
    hazard: 'CYCLONE',
    phase: 'AFTER',
    category: 'WATER_AND_FOOD',
    title: 'Avoid Brackish Drinking Wells Contaminated by Storm Surge',
    instruction: 'Do not drink from open wells or shallow handpumps in coastal flood zones until salinity testing and hyper-chlorination are completed by health authorities.',
    priority: 'HIGH',
    reason: 'Marine storm surge forces seawater into coastal freshwater aquifers, rendering groundwater non-potable and causing severe electrolyte imbalance if ingested.',
    source: 'Central Ground Water Board (CGWB) Coastal Salinity Advisory',
    related_cascading_risk: 'Long-term drinking water salinization.'
  },

  // =========================================================================
  // EARTHQUAKE
  // =========================================================================
  {
    id: 'eqk-bef-01',
    hazard: 'EARTHQUAKE',
    phase: 'BEFORE',
    category: 'PROPERTY_PREPARATION',
    title: 'Secure Tall Furniture & Heavy Wall Hangings with L-Brackets',
    instruction: 'Fasten tall cupboards, refrigerators, heavy mirrors, water geysers, and bookshelves securely to wall studs using metal L-brackets.',
    priority: 'CRITICAL',
    reason: 'Toppling furniture and falling geysers account for over 60% of non-fatal injuries and trap egress routes during moderate to severe seismic shocks.',
    source: 'BIS IS 13935: Indian Standard for Seismic Evaluation and Strengthening of Buildings',
    related_cascading_risk: 'Toppling furniture blocking primary evacuation hallways.'
  },
  {
    id: 'eqk-bef-02',
    hazard: 'EARTHQUAKE',
    phase: 'BEFORE',
    category: 'FAMILY_COMMUNICATION',
    title: 'Practice \'Drop, Cover, and Hold On\' Drills Biannually',
    instruction: 'Ensure every family member knows the safe spots in each room: under sturdy wooden desks/tables or against interior load-bearing walls away from glass windows.',
    priority: 'HIGH',
    reason: 'Seismic shaking induces panic; instinctive muscle memory developed through drills allows survival actions within the first 3 seconds of ground acceleration.',
    source: 'NDMA Earthquake Management Guidelines',
    related_cascading_risk: 'Panic-induced stampedes in stairwells.'
  },
  {
    id: 'eqk-dur-01',
    hazard: 'EARTHQUAKE',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'DROP, COVER, and HOLD ON — Do NOT Run Outside During Shaking',
    instruction: 'DROP down onto hands and knees; COVER your head and neck beneath a sturdy desk or table; HOLD ON until shaking stops completely. Do NOT rush outdoors.',
    priority: 'CRITICAL',
    reason: 'Running outside exposes individuals to falling exterior brick parapets, shattered window glass, architectural cornices, and falling electrical wires, which cause the vast majority of seismic deaths.',
    source: 'National Disaster Management Guidelines: Management of Earthquakes',
    warning: 'Never use elevators during or immediately following ground tremors.',
    related_cascading_risk: 'Falling facade masonry and glass showers.'
  },
  {
    id: 'eqk-dur-02',
    hazard: 'EARTHQUAKE',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'If in an Open Field or Vehicle: Stay Clear of Structures',
    instruction: 'If outdoors, move into an open area away from high-rise buildings, flyovers, billboards, and high-voltage transmission lines. If driving, pull over smoothly away from overpasses.',
    priority: 'HIGH',
    reason: 'Non-engineered parapets and utility poles readily collapse outward into street corridors during horizontal ground accelerations.',
    source: 'NDMA Earthquake SOP',
    related_cascading_risk: 'Pylon collapse and vehicle crushing.'
  },
  {
    id: 'eqk-aft-01',
    hazard: 'EARTHQUAKE',
    phase: 'AFTER',
    category: 'UTILITY_SAFETY',
    title: 'Sniff for LPG Gas Leaks Before Operating Any Electrical Switches',
    instruction: 'Check for gas smell immediately upon evacuation. If gas odor is present, open windows, extinguish any open flames, evacuate outdoors, and do NOT turn light switches ON or OFF.',
    priority: 'CRITICAL',
    reason: 'Operating electrical switches generates micro-sparks that can ignite gas-air mixtures released from seismic ruptures in domestic LPG cylinder pipes.',
    source: 'Petroleum and Explosives Safety Organisation (PESO) Safety Bulletin',
    warning: 'Do not light matches, candles, or lighters; use battery-powered flashlights only.',
    related_cascading_risk: 'Post-earthquake urban conflagrations and gas explosions.'
  },
  {
    id: 'eqk-aft-02',
    hazard: 'EARTHQUAKE',
    phase: 'AFTER',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Expect Aftershocks — Do NOT Re-Enter Visibly Cracked Buildings',
    instruction: 'Remain in open ground. Do not re-enter structures with visible diagonal shear cracks, bowed pillars, or damaged stairwells until cleared by licensed structural engineers.',
    priority: 'CRITICAL',
    reason: 'Aftershocks can trigger the complete pancake collapse of buildings already weakened by the main shock.',
    source: 'Geological Survey of India (GSI) Post-Earthquake Safety Protocol',
    warning: 'Earthquake aftershocks cannot be temporally predicted; treat damaged buildings with utmost caution.',
    related_cascading_risk: 'Secondary progressive structural collapse during aftershocks.'
  },

  // =========================================================================
  // HEATWAVE
  // =========================================================================
  {
    id: 'htw-bef-01',
    hazard: 'HEATWAVE',
    phase: 'BEFORE',
    category: 'MEDICAL_AND_HEALTH',
    title: 'Stock Oral Rehydration Salts (ORS) & Maintain Home Hydration',
    instruction: 'Keep packets of ORS, glucose, electoral powders, and clean water containers stocked at home. Prepare natural coolers like buttermilk, aam panna, and lemon water.',
    priority: 'CRITICAL',
    reason: 'Severe sweating depletes essential sodium and potassium electrolytes rapidly, leading to hypokalemia, painful muscle cramps, and heat exhaustion.',
    source: 'NDMA National Guidelines for Prevention and Management of Heat Wave',
    related_cascading_risk: 'Acute fluid deficit and circulatory heat collapse.'
  },
  {
    id: 'htw-bef-02',
    hazard: 'HEATWAVE',
    phase: 'BEFORE',
    category: 'PROPERTY_PREPARATION',
    title: 'Install Window Shades, Bamboo Blinds & Lime-Wash Roofs',
    instruction: 'Cover sun-facing windows with reflective film, dark curtains, or bamboo chiks. Applying reflective white lime-wash on flat roofs can reduce indoor temperatures by up to 5°C.',
    priority: 'HIGH',
    reason: 'Thermal radiant ingress through unshaded masonry and single-pane glass elevates indoor temperatures far above outdoor ambient levels.',
    source: 'Bureau of Energy Efficiency (BEE) Cool Roofs Guidelines',
    related_cascading_risk: 'Indoor thermal trapping and nighttime heat stress.'
  },
  {
    id: 'htw-dur-01',
    hazard: 'HEATWAVE',
    phase: 'DURING',
    category: 'WATER_AND_FOOD',
    title: 'Drink Plenty of Water Frequently, Even Without Feeling Thirsty',
    instruction: 'Drink clean water every 20 to 30 minutes throughout the day. Avoid alcohol, excessive tea, coffee, and carbonated soft drinks, which dehydrate the body.',
    priority: 'CRITICAL',
    reason: 'Thirst is a delayed physiological indicator of dehydration; drinking regularly maintains blood volume and core thermal regulation.',
    source: 'Ministry of Health and Family Welfare (MoHFW) National Heat Health Advisory',
    related_cascading_risk: 'Exertional dehydration and kidney stress.'
  },
  {
    id: 'htw-dur-02',
    hazard: 'HEATWAVE',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Avoid Direct Sun Exposure Between 12:00 PM and 3:30 PM',
    instruction: 'Reschedule heavy agricultural work, construction, outdoor labor, and sports to early morning (before 9 AM) or late evening (after 5 PM).',
    priority: 'CRITICAL',
    reason: 'Solar ultraviolet irradiation and ambient dry-bulb temperatures peak during this midday window, dramatically escalating the risk of acute Heat Stroke.',
    source: 'Ministry of Labour and Employment Occupational Heat Stress Advisories',
    warning: 'Never leave young children, elderly persons, or pets inside a parked vehicle.',
    related_cascading_risk: 'Occupational heat stroke emergencies.'
  },
  {
    id: 'htw-dur-03',
    hazard: 'HEATWAVE',
    phase: 'DURING',
    category: 'MEDICAL_AND_HEALTH',
    title: 'Recognize Heat Stroke Symptoms & Administer Rapid Cooling',
    instruction: 'If someone develops high body temperature (> 40°C), ceases sweating, exhibits confusion or loss of consciousness: Move to shade, apply ice packs to neck/armpits/groin, and call 108 immediately.',
    priority: 'CRITICAL',
    reason: 'Heat stroke is a medical emergency with up to 50% mortality if core body cooling is delayed beyond 30 minutes.',
    source: 'MoHFW Emergency Clinical Protocol for Heat-Related Illnesses',
    warning: 'Heat stroke requires immediate aggressive external water cooling; do not administer oral fluids to an unconscious person.',
    related_cascading_risk: 'Multi-organ failure from extreme hyperthermia.'
  },
  {
    id: 'htw-aft-01',
    hazard: 'HEATWAVE',
    phase: 'AFTER',
    category: 'VULNERABLE_MEMBERS',
    title: 'Monitor Elderly & Vulnerable Relatives for Delayed Thermal Stress',
    instruction: 'Continue monitoring hydration and mental alertness of elderly individuals, pregnant women, and infants for 48 hours following a severe heatwave episode.',
    priority: 'HIGH',
    reason: 'Elderly individuals have diminished thirst sensation and reduced cardiovascular reserve, often presenting with delayed electrolyte collapse days after heat waves.',
    source: 'National Health Mission Elderly Care Protocols',
    related_cascading_risk: 'Delayed geriatric cardiovascular decompensation.'
  },

  // =========================================================================
  // LANDSLIDE
  // =========================================================================
  {
    id: 'lnd-bef-01',
    hazard: 'LANDSLIDE',
    phase: 'BEFORE',
    category: 'PROPERTY_PREPARATION',
    title: 'Recognize Precursor Geological Warning Signs on Slopes',
    instruction: 'Regularly inspect retaining walls, slopes behind your house, and paved paths for new tension fissures, tilting utility poles/trees, sticking windows, or bulging masonry.',
    priority: 'CRITICAL',
    reason: 'Slope failure surfaces develop tensile deformation cracks and creep displacement days or weeks before catastrophic sudden shear failure.',
    source: 'Geological Survey of India (GSI) Landslide Awareness Guidelines',
    related_cascading_risk: 'Toe slumping and sudden slope failure.'
  },
  {
    id: 'lnd-bef-02',
    hazard: 'LANDSLIDE',
    phase: 'BEFORE',
    category: 'SAFE_ROUTES_EVACUATION',
    title: 'Map Evacuation Routes That Avoid Gullies & Narrow Hill Defiles',
    instruction: 'Identify secondary escape routes that stay on stable bedrock ridges. Never choose paths along mountain stream gullies, ravine floors, or directly beneath steep talus cones.',
    priority: 'CRITICAL',
    reason: 'Debris flows channel high-velocity mud, boulders, and uprooted trees directly into natural stream gullies and ravines at speeds exceeding 40 km/h.',
    source: 'NDMA National Landslide Risk Management Strategy',
    warning: 'Never build or pitch tents near the base of steep slopes or dry mountain channels.',
    related_cascading_risk: 'Rapid channeled debris avalanche.'
  },
  {
    id: 'lnd-dur-01',
    hazard: 'LANDSLIDE',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Move Laterally Away from Debris Path — Never Outrun Downhill',
    instruction: 'If you hear rumbling, trees snapping, or notice sudden mudflow, move laterally (perpendicular) to the slide path. Never attempt to run straight downhill ahead of the debris flow.',
    priority: 'CRITICAL',
    reason: 'Debris flows accelerate down-gradient and spread laterally; escaping sideways to higher stable ridges is the only viable physical evasion strategy.',
    source: 'Border Roads Organisation (BRO) Hill Road Safety Manual',
    warning: 'If escape is impossible, curl into a tight ball beneath a reinforced pillar and protect your head with your arms.',
    related_cascading_risk: 'Crushing trauma from high-velocity boulder flows.'
  },
  {
    id: 'lnd-aft-01',
    hazard: 'LANDSLIDE',
    phase: 'AFTER',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Stay Clear of Slide Perimeter — Expect Delayed Secondary Failures',
    instruction: 'Do not approach the perimeter of a fresh landslide. Secondary slides frequently occur hours or days after the primary failure as unsupported scarp slopes collapse.',
    priority: 'CRITICAL',
    reason: 'The head scarp and lateral margins of a fresh slide remain in an unstable critical state of equilibrium (Factor of Safety < 1.0).',
    source: 'NDMA Landslide Post-Event Safety Guidelines',
    warning: 'Never walk over unconsolidated slide debris; mud crusts can conceal deep water pockets or unstable voids.',
    related_cascading_risk: 'Secondary progressive head-scarp collapse.'
  },
  {
    id: 'lnd-aft-02',
    hazard: 'LANDSLIDE',
    phase: 'AFTER',
    category: 'SAFE_ROUTES_EVACUATION',
    title: 'Alert Downstream Communities if River Flow Stoppage is Observed',
    instruction: 'If a mountain river downstream of a slide suddenly dries up or drops dramatically, evacuate downstream riverbanks immediately and notify district authorities (112 / 1077).',
    priority: 'CRITICAL',
    reason: 'Sudden river stoppage indicates a natural landslide dam has formed upstream; when the debris dam breaches, a catastrophic flash flood wave is released.',
    source: 'Central Water Commission Landslide Dam Outburst Flood (LDOF) Advisory',
    related_cascading_risk: 'Landslide lake outburst floods (LDOF).'
  },

  // =========================================================================
  // SEVERE WEATHER
  // =========================================================================
  {
    id: 'swx-bef-01',
    hazard: 'SEVERE_WEATHER',
    phase: 'BEFORE',
    category: 'UTILITY_SAFETY',
    title: 'Unplug Sensitive Electronic Equipment & Computer Modems',
    instruction: 'Disconnect computers, televisions, air-conditioners, and internet modems from electrical wall outlets before severe thunderstorms begin.',
    priority: 'HIGH',
    reason: 'Lightning strikes induce massive high-voltage transient surges along overhead power and telecom cables, destroying internal transformer circuits.',
    source: 'Bureau of Indian Standards IS 2309: Protection of Buildings and Allied Structures Against Lightning',
    related_cascading_risk: 'Electrical short-circuit fires and appliance destruction.'
  },
  {
    id: 'swx-dur-01',
    hazard: 'SEVERE_WEATHER',
    phase: 'DURING',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Apply the 30-30 Rule & Never Shelter Under Tall Isolated Trees',
    instruction: 'If the delay between lightning flash and thunderclap is under 30 seconds, seek indoor shelter immediately. Never shelter under tall isolated trees, open metal tin sheds, or mobile towers.',
    priority: 'CRITICAL',
    reason: 'Tall isolated trees attract step-leader lightning strikes, causing fatal ground surface currents (step voltage) and side-flash discharges to nearby persons.',
    source: 'NDMA National Guidelines on Lightning Risk Management',
    warning: 'If trapped in an open field, crouch low on the balls of your feet with heels touching; minimize contact with the ground.',
    related_cascading_risk: 'Direct lightning strike and step-voltage electrocution.'
  },
  {
    id: 'swx-dur-02',
    hazard: 'SEVERE_WEATHER',
    phase: 'DURING',
    category: 'SAFE_ROUTES_EVACUATION',
    title: 'Never Drive Into Submerged Railway or Road Underpasses',
    instruction: 'Avoid low-lying underpasses during heavy downpours. If water covers the curb or approaches tire rim height, turn around immediately.',
    priority: 'CRITICAL',
    reason: 'Urban underpasses act as natural drainage sumps, rapidly accumulating 2 to 3 meters of runoff within 15 minutes, which stalls vehicle engines and traps occupants.',
    source: 'Ministry of Road Transport and Highways (MoRTH) Monsoon Traffic Advisory',
    warning: 'Electric windows and door locks fail once a vehicle\'s battery is submerged.',
    related_cascading_risk: 'Urban underpass drowning and vehicular entrapment.'
  },
  {
    id: 'swx-aft-01',
    hazard: 'SEVERE_WEATHER',
    phase: 'AFTER',
    category: 'AVOIDANCE_WHAT_NOT_TO_DO',
    title: 'Wait At Least 30 Minutes After the Last Thunderclap Before Resuming Outdoors',
    instruction: 'Remain inside a safe pucca structure for at least 30 minutes following the last audible sound of thunder, even if rain has stopped and blue skies appear.',
    priority: 'HIGH',
    reason: 'Lightning can strike up to 15 kilometers away from the parent storm cloud, originating from the anvil overhang of departing thunderstorm cells.',
    source: 'IMD Lightning Early Warning and Safety Manual',
    related_cascading_risk: 'Delayed bolt-from-the-blue lightning fatalities.'
  }
];

export const getStaticHazardGuide = (hazard: string): HazardSafetyGuide => {
  const hClean = hazard.toUpperCase().trim();
  const items = EXTENDED_SAFETY_ITEMS.filter((i) => i.hazard === hClean);
  
  const beforeItems = items.filter((i) => i.phase === 'BEFORE');
  const duringItems = items.filter((i) => i.phase === 'DURING');
  const afterItems = items.filter((i) => i.phase === 'AFTER');

  return {
    hazard: hClean,
    statutory_notice: 'Preparation actions may be undertaken independently at any time. Mandatory evacuation directives are ordered exclusively by civil authorities (District Magistrate / SDMA / NDRF) under the Disaster Management Act 2005.',
    emergency_contacts: {
      national_emergency: '112',
      ndma_disaster_helpline: '1078',
      state_emergency_operation_center: '1070',
      ambulance: '108'
    },
    total_action_items: items.length,
    categories_covered: Array.from(new Set(items.map((i) => i.category))),
    phases: {
      BEFORE: {
        phase_title: 'Before Event // Preparedness & Household Mitigation',
        item_count: beforeItems.length,
        items: beforeItems
      },
      DURING: {
        phase_title: 'During Event // Immediate Life Safety & Defensive Action',
        item_count: duringItems.length,
        items: duringItems
      },
      AFTER: {
        phase_title: 'After Event // Safe Recovery, Health Protection & Relief Claims',
        item_count: afterItems.length,
        items: afterItems
      }
    },
    synthetic_records: 0
  };
};
