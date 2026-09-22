"""
RISK // INDIA — Disaster Action Engine (Before / During / After Life-Safety Protocols)
=====================================================================================
Provides evidence-based, medically responsible, and actionable emergency guidance
partitioned into BEFORE (preparedness), DURING (immediate safety), and AFTER (recovery).
"""

from typing import Dict, List, Any


ACTION_PROTOCOLS: Dict[str, Dict[str, List[str]]] = {
    "FLOOD": {
        "BEFORE": [
            "Prepare a 72-hour Disaster Kit: 3L drinking water per person/day, dry rations, torch, spare batteries, first aid, and power banks.",
            "Seal identity documents, land records, insurance, and prescription medicines in waterproof ziplock bags.",
            "Identify nearest designated high-ground flood evacuation centers and community elevated shelters.",
            "Clear neighborhood storm culverts; move livestock, farm machinery, and vehicles to elevated embankments.",
            "Monitor CWC river stage bulletins and District Disaster Management Authority (DDMA) early warnings on VHF/FM."
        ],
        "DURING": [
            "Evacuate immediately upon receipt of official DDMA evacuation orders; do not wait until water enters premises.",
            "Turn off main electrical breaker switch and cooking gas cylinders before leaving premises.",
            "Never walk, swim, or drive through moving floodwaters. Just 15 cm (6 inches) of moving water can knock an adult down; 30 cm can float a vehicle.",
            "Stay clear of submerged electrical transformers, downed power cables, and open drains.",
            "Signal distress using a whistle, torch, or brightly colored cloth from the rooftop if trapped; call 112 or 1078."
        ],
        "AFTER": [
            "Do not drink flood-affected tap water or open well water until boiled vigorously for at least 1 minute or chlorinated.",
            "Inspect building walls and foundations for structural cracking before re-entering premises.",
            "Discard all perishable food, open medicines, and grains that came into contact with floodwaters.",
            "Beware of displaced snakes, scorpions, and rodents sheltering in furniture, shoes, or ceiling crevices.",
            "Report damaged embankments, severed electrical lines, or contaminated community wells to local revenue / panchayat officers."
        ]
    },
    "EARTHQUAKE": {
        "BEFORE": [
            "Fasten heavy furniture, cupboards, water heaters, and overhead shelves securely to wall studs with L-brackets.",
            "Identify safe spots in each room: under sturdy wooden tables or desks, and against interior load-bearing walls.",
            "Keep an emergency battery-powered radio, whistle, torch, and sturdy shoes beside your bed.",
            "Know how and where to shut off household main electricity, water, and gas valves.",
            "Conduct biannual Drop, Cover, and Hold On drills with family members."
        ],
        "DURING": [
            "DROP to your hands and knees; COVER your head and neck under a sturdy table or desk; HOLD ON until shaking stops.",
            "If in bed, stay there and protect your head with a firm pillow unless under a heavy ceiling fixture.",
            "Do NOT run outside while shaking is active; falling masonry, glass facade shards, and parapets cause the majority of casualties.",
            "If outdoors, move to an open area clear of overhead power lines, high-rise buildings, billboards, and flyovers.",
            "Do NOT use elevators under any circumstances during or immediately after ground shaking."
        ],
        "AFTER": [
            "Check yourself and household members for injuries; apply immediate first aid before assisting neighbors.",
            "Smell for gas leaks; if gas odor is detected, turn off main cylinder valve, open windows, and evacuate immediately without operating electrical switches.",
            "Expect aftershocks; each aftershock can trigger the collapse of buildings already weakened by the main shock.",
            "Use telephone networks strictly for life-threatening emergencies to prevent cellular network congestion.",
            "Listen to All India Radio or official State Disaster Management Authority broadcasts for structural re-entry notices."
        ]
    },
    "CYCLONE": {
        "BEFORE": [
            "Board up glass windows or apply criss-cross heavy masking tape to minimize flying glass splinters.",
            "Trim overgrown tree branches near roofs and overhead power service lines.",
            "Anchor loose outdoor objects (tin roofing sheets, trash bins, antennas, solar panels) or move them indoors.",
            "Keep emergency vehicles fueled and mobile phones, solar lanterns, and power banks fully charged.",
            "If living in a kutcha house or low-lying coastal zone, evacuate to a pucca Cyclone Shelter well before gale winds begin."
        ],
        "DURING": [
            "Remain indoors in the strongest central room of the house, away from external windows and glass doors.",
            "Do NOT go outside when the eye of the cyclone passes; calm conditions are temporary and violent reverse winds will strike suddenly.",
            "Disconnect electrical appliances to protect against extreme lightning surges and power grid voltage swings.",
            "Keep livestock untied so they can seek natural shelter in extreme flooding scenarios.",
            "Follow official IMD cyclone bulletins broadcast on radio and television."
        ],
        "AFTER": [
            "Remain in the cyclone shelter or reinforced structure until official 'All Clear' is broadcast by the district administration.",
            "Beware of snapped electric cables lying on wet ground or touching corrugated iron fences; treat all wires as live.",
            "Drive only if urgent; coastal and rural roads may be blocked by fallen banyan trees, electric poles, and storm surge silt.",
            "Boil drinking water or use water purification tablets to prevent cholera and water-borne enteric outbreaks.",
            "Help clear neighborhood drainage paths and assist community first-response volunteers."
        ]
    },
    "HEATWAVE": {
        "BEFORE": [
            "Stock oral rehydration salts (ORS), glucose, lemon water, and clean drinking water containers at home.",
            "Install light-colored curtains, bamboo blinds, or reflective films on sun-facing west and south windows.",
            "Schedule outdoor labor, heavy agricultural work, and travel for early morning (before 9 AM) or late evening (after 5 PM).",
            "Ensure elderly family members, young children, and pets have shaded, well-ventilated resting quarters."
        ],
        "DURING": [
            "Drink plenty of water frequently, even if you do not feel thirsty. Carry water whenever stepping outdoors.",
            "Avoid direct sun exposure between 12:00 PM and 3:30 PM, the peak ultraviolet and thermal irradiation window.",
            "Wear loose, light-colored, breathable cotton clothing and wide-brimmed hats or carry an umbrella.",
            "Never leave children or pets inside parked vehicles, where cabin temperatures can reach 60°C within 10 minutes.",
            "If someone experiences high body temperature, confusion, or ceases sweating, move them to shade, apply wet cloths, and call 108 immediately for heat stroke."
        ],
        "AFTER": [
            "Continue hydration therapy and monitor vulnerable family members for delayed thermal exhaustion or electrolyte imbalance.",
            "Replenish animal water troughs in community spaces and ensure farm livestock have shaded recovery paddocks.",
            "Report community drinking water supply breakdowns or tube-well failures to local municipal/panchayat desks."
        ]
    },
    "LANDSLIDE": {
        "BEFORE": [
            "Recognize precursor signs: sudden tilting of utility poles/trees, sticking doors/windows, and new cracks in plaster or soil.",
            "Plant deep-rooted native grass and shrubs on slopes to retard surface runoff erosion.",
            "Ensure slope retaining walls have clear weep holes to release hydrostatic water pressure behind the wall.",
            "Identify secondary evacuation routes avoiding narrow hill defiles, stream gullies, and steep talus slopes."
        ],
        "DURING": [
            "Evacuate slope terrain immediately if you hear a rumbling sound, crackling trees, or see sudden muddy water flow.",
            "If escape is impossible, curl into a tight ball and protect your head with your arms beneath a sturdy table or behind a reinforced pillar.",
            "Move laterally away from the path of debris flow; never attempt to outrun a mudflow downhill along its direct course.",
            "Stay alert while driving in hilly terrain; road embankments frequently collapse without prior warning."
        ],
        "AFTER": [
            "Stay away from slide areas; secondary collapses and delayed slope failures frequently occur hours after the initial slide.",
            "Check for ruptured underground LPG gas lines, municipal water mains, and snapped electric lines.",
            "Report trapped individuals or blocked state highways to local police control room (112) or BRO/PWD teams.",
            "Help elderly neighbors and children safely navigate uneven mud and talus debris."
        ]
    },
    "SEVERE_WEATHER": {
        "BEFORE": [
            "Unplug sensitive electronic devices and home computers to prevent lightning surge damage.",
            "Secure livestock inside reinforced sheds away from tall isolated trees and metal fences.",
            "Inspect rooftop water tanks, solar panels, and asbestos/tin sheets to ensure secure anchorage against high convective winds."
        ],
        "DURING": [
            "Adhere to the 30-30 Rule: If time between lightning flash and thunder is under 30 seconds, seek shelter indoors immediately.",
            "Never shelter under tall, isolated trees, open metal tin sheds, mobile towers, or near high-tension electrical pylons.",
            "If caught in an open field with no shelter nearby, crouch low on the balls of your feet with heels touching; minimize contact with the ground.",
            "Avoid contact with plumbing fixtures and corded electrical equipment during intense electrical thunderstorms.",
            "Pull vehicles over to the shoulder away from trees and overhead wires; stay inside the metal vehicle cabin."
        ],
        "AFTER": [
            "Wait at least 30 minutes after hearing the last thunderclap before resuming outdoor activities.",
            "Check roofs, solar installations, and vehicle glass for hail impact fractures.",
            "Watch out for fallen branches and dangling wires entangled in roadside vegetation."
        ]
    }
}


class DisasterActionEngine:
    """Provides structured life-safety guidance across all 6 disaster hazards."""

    def get_actions_for_hazard(self, hazard: str) -> Dict[str, List[str]]:
        h_clean = hazard.upper().strip()
        return ACTION_PROTOCOLS.get(h_clean, {
            "BEFORE": ["Monitor local district administration advisories.", "Prepare household emergency kit."],
            "DURING": ["Follow instructions from emergency first responders.", "Call 112 for emergency rescue."],
            "AFTER": ["Inspect premises safely.", "Report damaged infrastructure to local authorities."]
        })

    def get_actions_for_region(self, region_name: str, primary_hazard: str) -> Dict[str, Any]:
        h_clean = primary_hazard.upper().strip()
        actions = self.get_actions_for_hazard(h_clean)
        return {
            "region": region_name,
            "hazard_type": h_clean,
            "action_framework": "NDMA Life-Safety Standard Operating Procedures",
            "before_event": actions.get("BEFORE", []),
            "during_event": actions.get("DURING", []),
            "after_event": actions.get("AFTER", []),
            "emergency_dispatch": "112 (Unified Pan-India Emergency Service)"
        }


disaster_action_engine = DisasterActionEngine()
