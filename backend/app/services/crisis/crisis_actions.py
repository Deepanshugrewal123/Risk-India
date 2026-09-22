"""
RISK // INDIA — Crisis Action Engine (Phase 30E)
================================================
Generates prioritized, life-safety-ranked emergency human actions,
hazard-specific BEFORE/DURING/AFTER protocols, and 72-hour family preparedness checklists.
"""

from typing import Dict, List, Any
from app.services.crisis.crisis_schema import (
    CrisisActionItem,
    ActionPhase,
    ActionPriority,
    FamilyChecklistItem
)


# Hazard-specific prioritized immediate actions ("WHAT TO DO NOW")
HAZARD_IMMEDIATE_ACTIONS: Dict[str, List[Dict[str, Any]]] = {
    "FLOOD": [
        {
            "priority": ActionPriority.LIFE_SAFETY,
            "title": "Move to High Ground or Designated Elevated Shelter",
            "instruction": "Immediately move yourself, family, and vulnerable individuals to designated multi-story concrete structures or higher terrain away from riverbanks and low-lying nullahs.",
            "rationale": "Rapidly rising water levels can submerge escape paths within minutes.",
            "is_urgent": True
        },
        {
            "priority": ActionPriority.EVACUATION,
            "title": "Comply Immediately with Official Evacuation Orders",
            "instruction": "Follow instructions from District Disaster Management Authority (DDMA), SDRF, or Police. Do not delay evacuation to protect personal property.",
            "rationale": "Delayed evacuation risks stranding families and imperils emergency rescue teams.",
            "is_urgent": True
        },
        {
            "priority": ActionPriority.AVOID_DANGER,
            "title": "Turn Off Electricity & Do Not Enter Moving Water",
            "instruction": "Shut off main circuit breaker and gas cylinder valves before leaving. Never walk, cycle, or drive into flood water—just 15 cm of flowing water can sweep an adult off balance.",
            "rationale": "Electrocution and vehicular sweep are leading causes of preventable flood mortality.",
            "is_urgent": True
        },
        {
            "priority": ActionPriority.COMMUNICATION,
            "title": "Maintain Phone Charge & Keep Emergency Numbers Ready",
            "instruction": "Switch phones to battery saver mode. Keep nationwide emergency number 112 and Disaster Helpline 1078 or 1070 ready. If stranded on rooftop, signal with bright cloth, torch, or whistle.",
            "rationale": "Cellular network congestion and power outages require conserving phone batteries for rescue coordination.",
            "is_urgent": False
        },
        {
            "priority": ActionPriority.EMERGENCY_RESOURCES,
            "title": "Secure Waterproof Go-Bag & Clean Drinking Water",
            "instruction": "Carry your waterproof bag containing identity documents, essential prescription medication, torch, and sealed drinking water.",
            "rationale": "Water supply contamination is ubiquitous during flood inundation; safe drinking water prevents acute waterborne illness.",
            "is_urgent": False
        }
    ],
    "EARTHQUAKE": [
        {
            "priority": ActionPriority.LIFE_SAFETY,
            "title": "DROP, COVER, and HOLD ON",
            "instruction": "If inside, DROP to the floor, take COVER under a sturdy desk or table, and HOLD ON until tremors cease completely. Protect head and neck with your arms.",
            "rationale": "Overhead falling objects and dislodged ceiling fixtures cause the majority of earthquake trauma.",
            "is_urgent": True
        },
        {
            "priority": ActionPriority.AVOID_DANGER,
            "title": "Stay Away from Glass Windows, Parapets & Exterior Walls",
            "instruction": "Do not attempt to run out of multi-story buildings during active shaking. Never use elevators. If outdoors, move to an open clearing away from electrical cables, facades, and billboards.",
            "rationale": "Shattering glass facades and falling masonry along building exteriors cause severe exterior casualties.",
            "is_urgent": True
        },
        {
            "priority": ActionPriority.EVACUATION,
            "title": "Evacuate Calmly Once Tremors Stop",
            "instruction": "Once shaking halts, inspect immediate surroundings for fire or structural collapse. Use stairwells calmly to reach open community ground.",
            "rationale": "Stairwell stampedes cause severe injuries; structural evaluation is critical before re-entry.",
            "is_urgent": True
        },
        {
            "priority": ActionPriority.AVOID_DANGER,
            "title": "Check for Gas Leaks & Fire Hazards",
            "instruction": "Turn off cooking gas cylinders immediately. If you smell gas, do not operate any electrical switch or flame; open windows and leave immediately.",
            "rationale": "Post-earthquake fires ignited by gas ruptures can surpass direct structural damage.",
            "is_urgent": False
        },
        {
            "priority": ActionPriority.COMMUNICATION,
            "title": "Prepare for Strong Aftershocks & Monitor Official Radio",
            "instruction": "Be prepared for subsequent aftershocks which can collapse pre-damaged structures. Keep telephone calls limited to life-threatening emergencies to unblock lines.",
            "rationale": "Aftershocks frequently occur in the hours following moderate to strong earthquakes.",
            "is_urgent": False
        }
    ],
    "CYCLONE": [
        {
            "priority": ActionPriority.LIFE_SAFETY,
            "title": "Take Shelter in Sturdy Pucca or Cyclone Shelter",
            "instruction": "Move to the strongest interior room on the ground or reinforced floor of a pucca concrete building, or reach designated cyclone shelters before gale winds arrive.",
            "rationale": "Kutcha houses, tin roofs, and asbestos sheets are readily dislodged by gale-force cyclone winds.",
            "is_urgent": True
        },
        {
            "priority": ActionPriority.AVOID_DANGER,
            "title": "Stay Indoors Even During Temporary Calm (Eye of the Cyclone)",
            "instruction": "Do not venture outside when winds subside temporarily. The calm center (eye) will quickly be followed by ferocious winds blowing from the opposite direction.",
            "rationale": "Wind reversal in the trailing eye-wall is sudden, violent, and highly hazardous.",
            "is_urgent": True
        },
        {
            "priority": ActionPriority.EVACUATION,
            "title": "Heed Inundation & Coastal Evacuation Directives",
            "instruction": "Residents within 5 km of coastlines or tidal estuaries must evacuate immediately when ordered due to storm surge risks.",
            "rationale": "Storm surges driven by tropical cyclones can submerge coastal plains under 2–5 meters of seawater.",
            "is_urgent": True
        },
        {
            "priority": ActionPriority.COMMUNICATION,
            "title": "Secure Windows & Listen to IMD Cyclone Bulletins",
            "instruction": "Fasten storm shutters or criss-cross tape on large glass panes. Keep a battery transistor radio tuned to All India Radio for official cyclone updates.",
            "rationale": "Power and cellular towers frequently collapse; terrestrial radio remains the most resilient broadcast channel.",
            "is_urgent": False
        },
        {
            "priority": ActionPriority.EMERGENCY_RESOURCES,
            "title": "Store Emergency Potable Water & Food Provisions",
            "instruction": "Fill buckets, clean containers, and bottles with drinking water before municipal water pressure fails. Stock non-perishable food for at least 72 hours.",
            "rationale": "Post-cyclone utility restoration in affected districts typically takes several days.",
            "is_urgent": False
        }
    ],
    "HEATWAVE": [
        {
            "priority": ActionPriority.LIFE_SAFETY,
            "title": "Avoid Direct Sun Exposure During Peak Hours (11:00 AM – 4:00 PM)",
            "instruction": "Remain indoors in well-ventilated or cooled spaces during peak solar irradiance. Postpone intense manual labor and outdoor activities.",
            "rationale": "Prolonged exposure during extreme heat spells triggers heat stroke, organ stress, and hyperthermia.",
            "is_urgent": True
        },
        {
            "priority": ActionPriority.AVOID_DANGER,
            "title": "Continuous Hydration with Electrolytes & ORS",
            "instruction": "Drink water frequently even if not thirsty. Consume Oral Rehydration Salts (ORS), coconut water, lemon water (nimbu pani), or buttermilk (chaas). Avoid alcohol and caffeinated drinks.",
            "rationale": "Electrolyte depletion leads rapidly to muscle cramps, heat exhaustion, and cardiovascular collapse.",
            "is_urgent": True
        },
        {
            "priority": ActionPriority.LIFE_SAFETY,
            "title": "Protect Infants, Elderly & Chronic Patients",
            "instruction": "Never leave children, elderly family members, or pets inside parked vehicles even with cracked windows. Check frequently on vulnerable neighbors living alone.",
            "rationale": "Internal vehicle temperatures can exceed fatal 50°C levels in less than 15 minutes.",
            "is_urgent": True
        },
        {
            "priority": ActionPriority.PREPARATION,
            "title": "Wear Light-Colored, Loose Cotton Clothing",
            "instruction": "Wear loose, light-colored cotton attire. Use umbrellas, wide-brimmed hats, and damp towels to cover head and neck when stepping out is unavoidable.",
            "rationale": "Light fabrics reflect solar radiation and facilitate natural sweat evaporation.",
            "is_urgent": False
        },
        {
            "priority": ActionPriority.COMMUNICATION,
            "title": "Recognize Heatstroke Symptoms & Seek Immediate Medical Help",
            "instruction": "If someone exhibits high body temperature, cessation of sweating, confusion, nausea, or fainting, move them to shade immediately, apply ice packs to neck/armpits, and call 108/112.",
            "rationale": "Heatstroke is an emergency requiring rapid evaporative and physical cooling to avert brain injury.",
            "is_urgent": False
        }
    ],
    "LANDSLIDE": [
        {
            "priority": ActionPriority.LIFE_SAFETY,
            "title": "Evacuate Slope Footing & Steep Valley Zones Immediately",
            "instruction": "Move away from known landslide paths, steep escarpments, steep drainage channels, and valley bottoms during or immediately following intense rainfall.",
            "rationale": "Saturated debris flows travel at speeds exceeding 30–50 km/h with little audible advance notice.",
            "is_urgent": True
        },
        {
            "priority": ActionPriority.AVOID_DANGER,
            "title": "Watch for Early Physical Warning Signs",
            "instruction": "Look and listen for tilting utility poles, leaning trees, fresh soil cracks, jammed doors/windows, or sudden muddy discoloration in nearby streams.",
            "rationale": "Creep and subsurface soil slippage precede catastrophic slope shear failures.",
            "is_urgent": True
        },
        {
            "priority": ActionPriority.EVACUATION,
            "title": "Do Not Cross Fresh Mudslides or Debris on Hill Roads",
            "instruction": "Halt vehicles well clear of road debris or rock falls. Secondary slides frequently strike within minutes of the initial detachment.",
            "rationale": "Vehicles halted adjacent to active landslide zones are vulnerable to recurrent rockfall.",
            "is_urgent": True
        },
        {
            "priority": ActionPriority.COMMUNICATION,
            "title": "Alert Downslope Neighbors & Notify District Emergency Operations",
            "instruction": "Warn downstream and downslope households immediately. Report slope cracking or river damming to District Emergency Operations Centre (1077).",
            "rationale": "River damming by debris can breach rapidly, creating devastating downstream flash floods.",
            "is_urgent": False
        },
        {
            "priority": ActionPriority.PREPARATION,
            "title": "Seek Shelter in Sturdy Structures Away from Slopes",
            "instruction": "If unable to evacuate the region, shelter on the upper floor of a reinforced structure on the side furthest from the slope.",
            "rationale": "Upper-floor rooms on the protected side provide the greatest survival margin against low-volume earth movement.",
            "is_urgent": False
        }
    ],
    "SEVERE_WEATHER": [
        {
            "priority": ActionPriority.LIFE_SAFETY,
            "title": "Seek Enclosed Shelter & Avoid Open Fields",
            "instruction": "Immediately go inside a substantial building or fully enclosed metal vehicle when thunder roars. Avoid open grounds, golf courses, bus shelters, and tractors.",
            "rationale": "'When Thunder Roars, Go Indoors'. Lightning can strike 10–15 km ahead of the active precipitation core.",
            "is_urgent": True
        },
        {
            "priority": ActionPriority.AVOID_DANGER,
            "title": "Stay Away from Isolated Trees & Tall Conductive Objects",
            "instruction": "Never take shelter beneath isolated trees, metal fences, light towers, or high mast poles. Maintain at least 15 meters distance.",
            "rationale": "Side flashes and ground current radiating from struck trees are major causes of lightning fatalities in India.",
            "is_urgent": True
        },
        {
            "priority": ActionPriority.AVOID_DANGER,
            "title": "Unplug Electrical Appliances & Avoid Plumbing",
            "instruction": "Disconnect expensive electronics and computers. Refrain from showering or washing hands during heavy cloud-to-ground lightning storms.",
            "rationale": "Lightning surges conduct readily through electrical wiring, internet cables, and metal plumbing lines.",
            "is_urgent": False
        },
        {
            "priority": ActionPriority.COMMUNICATION,
            "title": "Wait 30 Minutes After Last Thunder Before Resuming Outdoors",
            "instruction": "Remain in safe shelter until 30 minutes after hearing the last clap of thunder. Follow IMD nowcast updates on Damini lightning alert app.",
            "rationale": "Trailing storm cells routinely generate delayed lightning discharges.",
            "is_urgent": False
        },
        {
            "priority": ActionPriority.PREPARATION,
            "title": "Secure Loose Outdoor Items Against Squall Winds",
            "instruction": "Fasten or bring indoors sheet roofs, flowerpots, tarpaulins, and temporary signboards before severe convective winds arrive.",
            "rationale": "Severe convective squalls (Kalbaishakhi/Andhi) generate microbursts exceeding 80 km/h.",
            "is_urgent": False
        }
    ]
}


# Hazard-specific comprehensive BEFORE / DURING / AFTER life-safety protocols
COMPREHENSIVE_PROTOCOLS: Dict[str, Dict[str, List[Dict[str, str]]]] = {
    "FLOOD": {
        "BEFORE": [
            {"title": "72-Hour Disaster Kit", "instruction": "Prepare 3L drinking water per person/day, dry rations, torch, spare batteries, first aid, and power banks."},
            {"title": "Protect Vital Documents", "instruction": "Seal Aadhaar cards, voter IDs, land deeds, insurance policies, and medications in waterproof ziplock bags."},
            {"title": "Identify High-Ground Shelters", "instruction": "Map out nearest designated elevated flood evacuation shelters and high-ground routes with family members."},
            {"title": "Clear Drains & Elevate Valuables", "instruction": "Clear local culverts; move livestock, motorbikes, and heavy appliances to upper floors or elevated platforms."},
            {"title": "Monitor CWC/DDMA Bulletins", "instruction": "Keep track of Central Water Commission gauge levels and District Disaster Management bulletins."}
        ],
        "DURING": [
            {"title": "Evacuate on Official Notice", "instruction": "Evacuate immediately upon DDMA orders; do not wait until water enters rooms."},
            {"title": "Disconnect Mains Electricity & Gas", "instruction": "Turn off main circuit breaker and cooking gas cylinders before leaving premises."},
            {"title": "Avoid Moving Water", "instruction": "Never walk, swim, or drive through flowing water. 15 cm floats a person; 30 cm sweeps a car."},
            {"title": "Steer Clear of Downed Wires", "instruction": "Stay at least 10 meters away from submerged transformers, utility poles, and downed electric lines."},
            {"title": "Signal Distress from Rooftops", "instruction": "If trapped on upper floors, signal distress using a whistle, flashlight, or bright cloth. Dial 112 / 1078."}
        ],
        "AFTER": [
            {"title": "Boil Drinking Water", "instruction": "Do not drink municipal or well water until boiled vigorously for 1 minute or treated with chlorine."},
            {"title": "Inspect Structural Integrity", "instruction": "Examine building walls, foundations, and ceilings for cracks or sagging before entering."},
            {"title": "Discard Contaminated Food", "instruction": "Throw away all perishable food, unsealed grains, and medicines that came in contact with flood water."},
            {"title": "Beware of Displaced Reptiles", "instruction": "Check shoes, furniture, and dark corners for displaced snakes, scorpions, or rodents."},
            {"title": "Report Damaged Infrastructure", "instruction": "Notify panchayat or municipal authorities of breached embankments, blocked culverts, or severed power."}
        ]
    },
    "EARTHQUAKE": {
        "BEFORE": [
            {"title": "Anchor Heavy Furniture", "instruction": "Secure wardrobes, bookcases, refrigerators, and heavy wall hangings to wall studs with steel brackets."},
            {"title": "Identify Safe Indoor Spots", "instruction": "Identify sturdy tables or interior load-bearing corners away from glass windows in each room."},
            {"title": "Bedside Emergency Kit", "instruction": "Keep sturdy shoes, flashlight, whistle, and basic eyeglasses beside your bed at all times."},
            {"title": "Learn Utility Shut-Offs", "instruction": "Ensure every adult in the household knows how to shut off main gas, water, and electrical supply."},
            {"title": "Conduct Drop & Cover Drills", "instruction": "Practice Drop, Cover, and Hold On drills with household members twice a year."}
        ],
        "DURING": [
            {"title": "Drop, Cover, and Hold On", "instruction": "Drop to hands and knees, take cover under a sturdy table, and hold on until shaking stops entirely."},
            {"title": "Stay Away from Windows", "instruction": "Move away from external windows, glass doors, mirrors, and unanchored tall furniture."},
            {"title": "Do Not Run Outside During Shaking", "instruction": "Falling masonry, signboards, and facade glass cause most injuries. Stay inside until shaking ends."},
            {"title": "Never Use Elevators", "instruction": "Use only stairwells once shaking stops; elevators can lose power or misalign in shafts."},
            {"title": "Outdoor Safety Clearing", "instruction": "If outdoors, move into an open area away from electrical cables, tall buildings, trees, and overpasses."}
        ],
        "AFTER": [
            {"title": "Check Injuries & Administer First Aid", "instruction": "Treat bleeding and severe injuries immediately; do not move seriously injured persons unless in danger."},
            {"title": "Sniff for Gas Leaks", "instruction": "If gas odor is present, open windows, shut main cylinder valve, and leave without using electrical switches."},
            {"title": "Anticipate Aftershocks", "instruction": "Expect aftershocks. Avoid entering visibly cracked or compromised concrete structures."},
            {"title": "Keep Phone Lines Open", "instruction": "Use phones only for urgent life-threatening rescue calls to keep cellular bands clear."},
            {"title": "Tune to Official Radio", "instruction": "Listen to All India Radio or official DDMA broadcasts for building re-entry and relief directives."}
        ]
    },
    "CYCLONE": {
        "BEFORE": [
            {"title": "Board Windows / Secure Roofs", "instruction": "Secure loose tin sheets and board windows or paste criss-cross heavy tape across large glass panes."},
            {"title": "Trim Overhanging Branches", "instruction": "Prune weak or dead tree branches near roofs, overhead power cables, and driveways."},
            {"title": "Stock 72h Non-Perishable Food", "instruction": "Store roasted chana, dry biscuits, jaggery, baby food, and 15 liters of drinking water per person."},
            {"title": "Charge Communication Devices", "instruction": "Fully charge smartphones, emergency power banks, rechargeable torches, and battery radios."},
            {"title": "Secure Fishing Boats & Livestock", "instruction": "Move livestock to reinforced cattle shelters; haul small fishing craft high above the tidal reach line."}
        ],
        "DURING": [
            {"title": "Remain in Strongest Interior Room", "instruction": "Stay inside the central reinforced room away from exterior windows and tin roof sections."},
            {"title": "Beware of the Eye of the Storm", "instruction": "Do not go outside if wind stops abruptly. The reverse eye-wall will hit suddenly with equal fury."},
            {"title": "Disconnect Non-Essential Electricals", "instruction": "Unplug home electronics and turn off the main breaker switch to avoid surges from downed power lines."},
            {"title": "Coastal Inundation Precaution", "instruction": "Move to higher floor levels if storm surge begins encroaching on coastal property."},
            {"title": "Keep Emergency Radio Tuned", "instruction": "Listen continuously to IMD track updates and coastal police broadcasts."}
        ],
        "AFTER": [
            {"title": "Do Not Touch Loose / Downed Wires", "instruction": "Assume every fallen electrical cable is live; report immediately to local power utility and police."},
            {"title": "Clear Debris Safely", "instruction": "Wear thick gloves and heavy shoes when clearing storm debris, broken glass, and fallen branches."},
            {"title": "Drink Only Boiled / Chlorinated Water", "instruction": "Municipal water distribution may be contaminated by storm surge or pipe breaches."},
            {"title": "Check Foundation Scour", "instruction": "Inspect building foundations and compound walls for soil scouring or undermining from surge water."},
            {"title": "Follow SDMA Relief Directives", "instruction": "Collect relief supplies only at designated government distribution points; avoid spreading rumors."}
        ]
    },
    "HEATWAVE": {
        "BEFORE": [
            {"title": "Prepare Cool Hydration Drinks", "instruction": "Keep earthen pots (matkas), ORS sachets, glucose, and electrolyte powders stocked at home."},
            {"title": "Insulate Living Quarters", "instruction": "Hang dark curtains, bamboo blinds (chicks), or sunshades on west and south facing windows."},
            {"title": "Schedule Outdoor Chores Early", "instruction": "Plan marketing, agricultural work, and transit before 10:00 AM or after 5:00 PM."},
            {"title": "Set Up Water Bowls for Animals", "instruction": "Keep shallow water bowls in shaded areas for stray animals and urban birds."},
            {"title": "Stock Emergency Heat Medicines", "instruction": "Ensure paracetamol, anti-diarrheals, and ORS are available in your home first-aid cabinet."}
        ],
        "DURING": [
            {"title": "Remain Indoors During Peak Heat", "instruction": "Stay inside shaded, well-ventilated rooms between 11:00 AM and 4:00 PM."},
            {"title": "Hydrate Systematically", "instruction": "Drink a glass of water every 30 minutes. Supplement with salted buttermilk, nimbu pani, and coconut water."},
            {"title": "Never Leave Children in Parked Vehicles", "instruction": "Never leave infants, kids, or pets in stationary cars, even with air conditioning running."},
            {"title": "Cover Head & Eyes When Stepping Out", "instruction": "Use a white umbrella, cotton gamcha/scarf to cover head and ears, and UV sunglasses."},
            {"title": "Apply Cooling Compresses on Heat Exhaustion", "instruction": "If experiencing dizziness or heavy sweat, sit in AC/shade, loosen collar, and apply cold wet towels."}
        ],
        "AFTER": [
            {"title": "Rehydrate Slowly After Sun Exposure", "instruction": "Drink lukewarm or room-temperature fluids; avoid chugging chilled water immediately upon entering."},
            {"title": "Monitor Urine Color", "instruction": "Ensure urine remains pale clear to light straw; dark amber urine indicates severe dehydration."},
            {"title": "Maintain High-Fluid Light Diet", "instruction": "Eat water-rich foods like watermelon, cucumber, gourds, and curd; avoid heavy, spicy, fried meals."},
            {"title": "Review Community Vulnerabilities", "instruction": "Confirm that elderly relatives and outdoor workers in your circle have recovered from daytime heat."},
            {"title": "Prepare for Prolonged Spells", "instruction": "Restock ORS and clean water reserves as heatwaves typically persist for 4 to 7 consecutive days."}
        ]
    },
    "LANDSLIDE": {
        "BEFORE": [
            {"title": "Map Slope Drainage & Cracks", "instruction": "Inspect hillside drainage ditches and retaining walls for new cracks, bulging, or water seepage."},
            {"title": "Establish Community Whistle Alerts", "instruction": "Agree with hillside neighbors on emergency whistle, drum, or siren codes for rapid evacuation."},
            {"title": "Keep Go-Bags Packed", "instruction": "Store critical documents, torch, warm clothes, rain gear, and first aid in portable backpacks."},
            {"title": "Plant Deep-Rooting Vegetation", "instruction": "Preserve hillside trees and plant vetiver grass to bind topsoil on vulnerable terraced embankments."},
            {"title": "Monitor Heavy Rainfall Alerts", "instruction": "Track Geological Survey of India (GSI) landslide bulletins and IMD heavy precipitation nowcasts."}
        ],
        "DURING": [
            {"title": "Evacuate Slope Zone Instantly", "instruction": "Leave immediate hillside area if you hear rumbling earth, cracking trees, or see sudden mudflow."},
            {"title": "Curl into Tight Ball If Trapped", "instruction": "If escape is impossible, curl into a tight fetal ball and protect your head and neck with your arms."},
            {"title": "Avoid Ravines & Drainage Channels", "instruction": "Never seek shelter inside natural gullies, stream beds, or roadside drainage culverts."},
            {"title": "Stop Vehicles at Safe Distance", "instruction": "If driving on hill highways, stop well back from falling boulders; never park beneath sheer rock cuts."},
            {"title": "Call 1077 / 112", "instruction": "Inform District Emergency Operations Centre and notify mountain rescue units immediately."}
        ],
        "AFTER": [
            {"title": "Stay Clear of Slide Area", "instruction": "Do not enter fresh debris zones. Secondary sliding and unstable boulders frequently fall hours later."},
            {"title": "Check for Dammed Rivers", "instruction": "Look for rivers blocked by slide debris upstream; breach waves can trigger catastrophic flash floods."},
            {"title": "Report Broken Gas, Water & Power Lines", "instruction": "Alert municipal utility boards immediately to severed conduits to prevent fires and road washouts."},
            {"title": "Assist Rescue Teams from Safe Perimeter", "instruction": "Guide SDRF/NDRF teams with local terrain knowledge without venturing onto loose scree."},
            {"title": "Re-Enter Only After Geologist Clearance", "instruction": "Have local engineering authorities or GSI experts inspect foundations before reoccupying hillside homes."}
        ]
    },
    "SEVERE_WEATHER": {
        "BEFORE": [
            {"title": "Secure Outdoor Objects", "instruction": "Tie down roofing sheets, awnings, potted plants, and outdoor furniture before storm arrival."},
            {"title": "Check Lightning Protection Conductors", "instruction": "Verify that building lightning arresters and earth grounding rods are in sound working order."},
            {"title": "Unplug Sensitive Electronics", "instruction": "Disconnect TVs, desktop computers, Wi-Fi routers, and charging bricks from wall outlets."},
            {"title": "Keep Flashlight & Spare Batteries Ready", "instruction": "Have emergency lights and battery-operated lanterns ready in accessible spots."},
            {"title": "Track Damini / IMD Nowcasts", "instruction": "Monitor lightning strikes in your 20 km radius using IMD Damini mobile portal or weather radar."}
        ],
        "DURING": [
            {"title": "Get Inside Sturdy Building", "instruction": "Adhere to the '30-30 Rule': If thunder follows lightning in less than 30 seconds, seek indoor shelter."},
            {"title": "Avoid Plumbing & Landline Phones", "instruction": "Do not use corded phones, wash dishes, or take showers; metal pipes conduct lightning strikes."},
            {"title": "Avoid Isolated High Points", "instruction": "Never stand beneath tall trees, watchtowers, or metal fences. Squat low in a depression if caught in open."},
            {"title": "Stay in Enclosed Metal Vehicles", "instruction": "If in a car, pull over away from trees/power lines, turn on hazards, and avoid touching exterior metal."},
            {"title": "Wait 30 Minutes After Last Thunder", "instruction": "Do not venture out until at least 30 minutes after hearing the last thunderclap."}
        ],
        "AFTER": [
            {"title": "Administer CPR If Lightning Strike Occurs", "instruction": "Lightning victims carry no electrical charge; immediately check breathing and perform CPR if needed."},
            {"title": "Inspect Roof & Chimney Damage", "instruction": "Examine tiles, solar panels, and sheet metal for loose fasteners or puncture damage from squalls/hail."},
            {"title": "Avoid Downed Power Lines", "instruction": "Report fallen lines to the power board; assume fallen wires and puddles surrounding them are energized."},
            {"title": "Clear Blocked Gutter Inlets", "instruction": "Remove leaves and hail accumulation from rooftop gutters to avert ponding and ceiling seepage."},
            {"title": "Resume Outdoor Work Carefully", "instruction": "Verify from radar that the convective thunderstorm cell has fully moved out of your district."}
        ]
    }
}


# 72-Hour Family Disaster Preparedness Checklist
FAMILY_PREPAREDNESS_CHECKLIST: List[FamilyChecklistItem] = [
    FamilyChecklistItem(
        category="Water & Hydration",
        item="Safe Drinking Water (12 Liters per person)",
        description="Calculate 3 to 4 liters per person per day for drinking and basic sanitation for 72 hours.",
        is_critical=True
    ),
    FamilyChecklistItem(
        category="Food & Nutrition",
        item="Non-Perishable Ready-to-Eat Food",
        description="Roasted grams (chana), dates, energy bars, biscuits, sattu, jaggery, canned food, and baby formula if required.",
        is_critical=True
    ),
    FamilyChecklistItem(
        category="Medical & First Aid",
        item="Family First Aid & Prescription Medicines",
        description="7-day supply of personal prescription drugs, ORS packets, bandages, antiseptic liquid, paracetamol, and pain relief.",
        is_critical=True
    ),
    FamilyChecklistItem(
        category="Power & Light",
        item="High-Capacity Power Bank & LED Torch",
        description="Charged 20,000mAh power bank, USB charging cords, heavy-duty LED torch, and spare AA/AAA batteries.",
        is_critical=True
    ),
    FamilyChecklistItem(
        category="Emergency Documents",
        item="Waterproof Document Pouch",
        description="Waterproof pouch containing Aadhaar cards, voter IDs, property papers, insurance, bank passbooks, and passport copies.",
        is_critical=True
    ),
    FamilyChecklistItem(
        category="Safety Gear",
        item="Emergency Whistle & Heavy-Duty Gloves",
        description="Pealess high-decibel whistle for distress signaling and leather/canvas work gloves for navigating storm debris.",
        is_critical=False
    ),
    FamilyChecklistItem(
        category="Cash & Finance",
        item="Physical Currency in Small Denominations",
        description="Small-denomination banknotes (₹50, ₹100, ₹500) as ATMs, POS machines, and digital UPI networks fail during power cuts.",
        is_critical=False
    ),
    FamilyChecklistItem(
        category="Communication",
        item="Battery-Powered AM/FM Transistor Radio",
        description="Portable radio receiver to hear official All India Radio / DDMA civil protection emergency bulletins during network collapse.",
        is_critical=False
    )
]


class CrisisActionEngine:
    """Produces prioritized immediate life safety actions and phase protocols."""

    @staticmethod
    def get_what_to_do_now(hazard: str) -> List[CrisisActionItem]:
        """Returns top 3-5 prioritized immediate life-safety actions ranked 1 to 5."""
        norm_hazard = str(hazard).upper()
        raw_items = HAZARD_IMMEDIATE_ACTIONS.get(norm_hazard, HAZARD_IMMEDIATE_ACTIONS["FLOOD"])
        
        actions: List[CrisisActionItem] = []
        for idx, item in enumerate(raw_items[:5], start=1):
            action_id = f"act-{norm_hazard.lower()}-now-{idx}"
            actions.append(
                CrisisActionItem(
                    id=action_id,
                    priority=item["priority"],
                    phase=ActionPhase.DURING,
                    order_rank=idx,
                    title=item["title"],
                    instruction=item["instruction"],
                    rationale=item["rationale"],
                    target_hazard=norm_hazard,
                    is_urgent=item.get("is_urgent", False)
                )
            )
        return actions

    @staticmethod
    def get_phase_protocols(hazard: str) -> Dict[str, List[CrisisActionItem]]:
        """Returns structured BEFORE, DURING, and AFTER protocols."""
        norm_hazard = str(hazard).upper()
        hazard_data = COMPREHENSIVE_PROTOCOLS.get(norm_hazard, COMPREHENSIVE_PROTOCOLS["FLOOD"])
        
        result: Dict[str, List[CrisisActionItem]] = {}
        for phase_key in ["BEFORE", "DURING", "AFTER"]:
            phase_enum = getattr(ActionPhase, phase_key)
            items = hazard_data.get(phase_key, [])
            action_items: List[CrisisActionItem] = []
            for idx, p in enumerate(items, start=1):
                action_items.append(
                    CrisisActionItem(
                        id=f"proto-{norm_hazard.lower()}-{phase_key.lower()}-{idx}",
                        priority=ActionPriority.LIFE_SAFETY if phase_key == "DURING" else ActionPriority.PREPARATION,
                        phase=phase_enum,
                        order_rank=idx,
                        title=p["title"],
                        instruction=p["instruction"],
                        rationale="Evidence-based civil disaster protection protocol.",
                        target_hazard=norm_hazard,
                        is_urgent=(phase_key == "DURING")
                    )
                )
            result[phase_key] = action_items
        return result

    @staticmethod
    def get_family_prep_checklist() -> List[FamilyChecklistItem]:
        """Returns standard 72-hour family disaster preparedness checklist."""
        return FAMILY_PREPAREDNESS_CHECKLIST
