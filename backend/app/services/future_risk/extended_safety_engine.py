"""
RISK // INDIA — Extended Citizen Disaster Safety Guidance Engine
================================================================
Provides a scalable, structured content architecture for citizen disaster safety
across all 6 supported hazards (FLOOD, CYCLONE, HEATWAVE, SEVERE_WEATHER, LANDSLIDE, EARTHQUAKE).

Key Guarantees:
- Replaces artificial 4-item limit with a rich, multi-category actionable guidance architecture.
- Partitioned into BEFORE (Preparedness & Planning), DURING (Survival & Immediate Protection),
  and AFTER (Safe Recovery, Inspection, Disease Prevention & Assistance).
- Every item includes priority (CRITICAL, HIGH, RECOMMENDED), rationale, authoritative source (NDMA SOP,
  IMD Guidelines, Disaster Management Act 2005), and cross-references to cascading secondary risks.
- Clear legal and operational demarcation: Preparation actions can be undertaken autonomously;
  mandatory evacuation directives are ordered exclusively by civil authorities (District Magistrate / SDMA / NDRF).
"""

from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from app.services.national_risk.regional_baseline import regional_baseline_engine, SUPPORTED_HAZARDS


class SafetyPhase(str, Enum):
    BEFORE = "BEFORE"
    DURING = "DURING"
    AFTER = "AFTER"


class SafetyPriority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    RECOMMENDED = "RECOMMENDED"


class SafetyCategory(str, Enum):
    EMERGENCY_CONTACTS = "EMERGENCY_CONTACTS"
    FAMILY_COMMUNICATION = "FAMILY_COMMUNICATION"
    EMERGENCY_KIT = "EMERGENCY_KIT"
    WATER_AND_FOOD = "WATER_AND_FOOD"
    MEDICAL_AND_HEALTH = "MEDICAL_AND_HEALTH"
    CRITICAL_DOCUMENTS = "CRITICAL_DOCUMENTS"
    POWER_AND_LIGHTING = "POWER_AND_LIGHTING"
    SAFE_ROUTES_EVACUATION = "SAFE_ROUTES_EVACUATION"
    VULNERABLE_MEMBERS = "VULNERABLE_MEMBERS"
    PETS_AND_LIVESTOCK = "PETS_AND_LIVESTOCK"
    PROPERTY_PREPARATION = "PROPERTY_PREPARATION"
    UTILITY_SAFETY = "UTILITY_SAFETY"
    AVOIDANCE_WHAT_NOT_TO_DO = "AVOIDANCE_WHAT_NOT_TO_DO"
    RECOVERY_AND_HEALTH = "RECOVERY_AND_HEALTH"
    DAMAGE_DOCUMENTATION = "DAMAGE_DOCUMENTATION"
    SHELTER = "SHELTER"
    TRANSPORTATION = "TRANSPORTATION"
    SANITATION = "SANITATION"
    STRUCTURAL_SAFETY = "STRUCTURAL_SAFETY"


@dataclass
class SafetyInstructionItem:
    id: str
    hazard: str
    phase: SafetyPhase
    category: SafetyCategory
    title: str
    instruction: str
    priority: SafetyPriority
    reason: str
    source: str
    warning: Optional[str] = None
    related_cascading_risk: Optional[str] = None
    practical_steps: Optional[List[str]] = None
    warning_signs: Optional[List[str]] = None
    what_not_to_do: Optional[List[str]] = None
    vulnerable_groups: Optional[str] = None
    checklist: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "hazard": self.hazard,
            "phase": self.phase.value,
            "category": self.category.value,
            "title": self.title,
            "instruction": self.instruction,
            "priority": self.priority.value,
            "reason": self.reason,
            "source": self.source,
            "warning": self.warning,
            "related_cascading_risk": self.related_cascading_risk,
            "practical_steps": self.practical_steps or [],
            "warning_signs": self.warning_signs or [],
            "what_not_to_do": self.what_not_to_do or [],
            "vulnerable_groups": self.vulnerable_groups or "",
            "checklist": self.checklist or []
        }


# Master repository of structured safety protocols
RAW_SAFETY_INSTRUCTIONS: List[SafetyInstructionItem] = [
    # =========================================================================
    # FLOOD — BEFORE
    # =========================================================================
    SafetyInstructionItem(
        id="fld-bef-01",
        hazard="FLOOD",
        phase=SafetyPhase.BEFORE,
        category=SafetyCategory.WATER_AND_FOOD,
        title="Store Potable Drinking Water in Sealed Containers",
        instruction="Store a minimum of 3 to 4 litres of clean drinking water per person per day for at least 3 days in clean, food-grade containers.",
        priority=SafetyPriority.CRITICAL,
        reason="Floodwaters submerge municipal distribution pipes and open wells, introducing toxic bacteria, sewage, and chemical runoff into the drinking supply.",
        source="NDMA National Disaster Management Guidelines: Management of Floods (Section 4.3)",
        warning="Do not rely on municipal taps once floodwaters approach your street.",
        related_cascading_risk="Water supply contamination and enteric waterborne epidemics.",
        practical_steps=[
            "Thoroughly sanitize food-grade drums, jerrycans, or high-density food-safe polyethylene containers with clean boiled water.",
            "Fill containers to the brim to reduce air headspace and seal lids tightly with food-grade plastic wrap.",
            "Elevate stored containers at least 1 metre above ground floor slab onto sturdy tables, shelves, or upper floor lofts.",
            "Stock 100 chlorine halogen tablets (Halazone or NaDCC) for emergency point-of-use purification."
        ],
        warning_signs=[
            "Municipal tap water appears cloudy, yellowish, or carries an earthy/musty sewage smell.",
            "Local drains or stormwater culverts begin backing up into neighborhood road channels.",
            "CWC hydrological bulletin signals warning stage breach at upstream gauging station."
        ],
        what_not_to_do=[
            "Do NOT use chemical drums, oil carboys, or pesticide containers to store potable water.",
            "Do NOT leave water storage containers uncovered or resting directly on flood-prone mud ground.",
            "Do NOT wait until municipal water pressure drops to begin emergency filling."
        ],
        vulnerable_groups="Infants needing reconstituted milk formulas, pregnant mothers, dialysis patients, and bedridden elders who require uninterrupted oral hydration.",
        checklist=[
            "Sanitize food-grade water containers",
            "Fill 4 litres per family member per day for 3 days",
            "Store containers on upper level or raised tables",
            "Pack chlorine halogen tablets and water dropper in emergency kit"
        ]
    ),
    SafetyInstructionItem(
        id="fld-bef-02",
        hazard="FLOOD",
        phase=SafetyPhase.BEFORE,
        category=SafetyCategory.CRITICAL_DOCUMENTS,
        title="Secure Important Documents in Watertight Pouches",
        instruction="Place Aadhaar cards, voter IDs, ration cards, property deeds, birth certificates, and insurance policies into sealed waterproof ziplock pouches near your exit.",
        priority=SafetyPriority.HIGH,
        reason="Identity proof and property records are required for statutory calamity relief disbursement, ex-gratia claims, and insurance verification under the DM Act 2005.",
        source="Ministry of Home Affairs / NDMA Calamity Relief Documentation SOP",
        related_cascading_risk="Prolonged recovery delays due to loss of statutory identification."
    ),
    SafetyInstructionItem(
        id="fld-bef-03",
        hazard="FLOOD",
        phase=SafetyPhase.BEFORE,
        category=SafetyCategory.SAFE_ROUTES_EVACUATION,
        title="Map High Ground & Designated Community Shelters",
        instruction="Identify multiple high-ground evacuation paths to designated community multi-purpose flood shelters, elevated school buildings, or reinforced concrete structures.",
        priority=SafetyPriority.CRITICAL,
        reason="Low-lying roads and culverts flood rapidly and may become impassable hours before peak river crest.",
        source="CWC Flood Forecasting & Inundation Mapping Handbook",
        warning="Never plan an evacuation route that crosses low-water bridges or earthen causeways.",
        related_cascading_risk="Road washouts and community isolation."
    ),
    SafetyInstructionItem(
        id="fld-bef-04",
        hazard="FLOOD",
        phase=SafetyPhase.BEFORE,
        category=SafetyCategory.VULNERABLE_MEMBERS,
        title="Prioritize Support Plan for Elderly, Children & Persons with Disabilities",
        instruction="Arrange early transport for elderly family members, infants, pregnant women, and persons with disabilities to elevated relatives' homes before road access degrades.",
        priority=SafetyPriority.CRITICAL,
        reason="Mobility-impaired and medically vulnerable individuals cannot navigate sudden moving floodwaters or swift evacuations.",
        source="NDMA Guidelines on Disability Inclusive Disaster Risk Reduction (DiDRR)",
        related_cascading_risk="Emergency rescue bottlenecks during rapid inundation."
    ),
    SafetyInstructionItem(
        id="fld-bef-05",
        hazard="FLOOD",
        phase=SafetyPhase.BEFORE,
        category=SafetyCategory.PETS_AND_LIVESTOCK,
        title="Move Livestock & Working Animals to Elevated Embankments",
        instruction="Untie domestic cattle and livestock; move them to elevated community highlands or embankments. Stock dry fodder on raised bamboo platforms.",
        priority=SafetyPriority.HIGH,
        reason="Tethered animals drown when floodwaters rise rapidly. Untying allows natural survival instincts.",
        source="Department of Animal Husbandry and Dairying Disaster Management Plan",
        warning="Never leave cattle tied to sheds in low-lying flood-prone areas.",
        related_cascading_risk="Livestock mortality causing post-flood biological contamination."
    ),
    SafetyInstructionItem(
        id="fld-bef-06",
        hazard="FLOOD",
        phase=SafetyPhase.BEFORE,
        category=SafetyCategory.PROPERTY_PREPARATION,
        title="Install Sewer Backflow Valves & Clear Storm Drains",
        instruction="Install simple check valves or plug ground-floor toilet drains with sandbags to prevent sewage backflow; clear neighborhood runoff culverts of plastic blockages.",
        priority=SafetyPriority.RECOMMENDED,
        reason="Rising stormwater exerts back-pressure into municipal sewer mains, driving contaminated blackwater into ground-floor habitations.",
        source="CPHEEO Urban Drainage Manual",
        related_cascading_risk="Urban waterlogging and indoor sanitation failure."
    ),

    # =========================================================================
    # FLOOD — DURING
    # =========================================================================
    SafetyInstructionItem(
        id="fld-dur-01",
        hazard="FLOOD",
        phase=SafetyPhase.DURING,
        category=SafetyCategory.AVOIDANCE_WHAT_NOT_TO_DO,
        title="Never Walk, Swim, or Drive Through Moving Floodwater",
        instruction="Adhere strictly to the Six-Inch / Two-Foot Rule: Just 15 cm (6 inches) of moving water can knock down an adult; 30 cm can float a small car; 60 cm can sweep away an SUV.",
        priority=SafetyPriority.CRITICAL,
        reason="Moving water exerts immense hydrodynamic pressure, and submerged road surfaces may have been entirely washed away beneath the murky water.",
        source="NDMA Standard Operating Procedure for Flood Response",
        warning="Turn Around, Don't Drown! Over 50% of flood fatalities occur in vehicles attempting to cross submerged roads.",
        related_cascading_risk="Culvert scour and vehicular drowning.",
        practical_steps=[
            "If driving and encountering water of unknown depth over the road, stop immediately, reverse safely, and seek alternate high routes.",
            "If your vehicle stalls in rapidly rising water, abandon it immediately and scramble to higher ground.",
            "If compelled to wade through shallow, standing water, probe every footstep ahead using a sturdy wooden stick.",
            "Wear sturdy closed-toe shoes or gumboots to protect feet from submerged rusty iron, sharp debris, and venomous snakes."
        ],
        warning_signs=[
            "Water flowing rapidly across road dips with visible surface ripples or eddies.",
            "Roadside markers, culvert railings, or median curbs disappear under murky water.",
            "Vehicle floating sensation, loss of steering traction, or water entering vehicle door floorboards."
        ],
        what_not_to_do=[
            "Do NOT drive around police barricades or road-closed warning signs on flooded causeways.",
            "Do NOT walk near open storm drains, drainage catch basins, or manholes with dislodged covers.",
            "Do NOT allow curious children or youth to swim or take selfies near swollen rivers or flood culverts."
        ],
        vulnerable_groups="Schoolchildren, elderly citizens with walking aids, motorcycle commuters, and auto-rickshaw drivers.",
        checklist=[
            "Turn vehicle around upon spotting submerged roadway",
            "Abandon vehicle immediately if water reaches door frame",
            "Use a wooden probe stick when wading through necessary shallow water",
            "Keep hands free and children secured in life vests or carry pouches"
        ]
    ),
    SafetyInstructionItem(
        id="fld-dur-02",
        hazard="FLOOD",
        phase=SafetyPhase.DURING,
        category=SafetyCategory.UTILITY_SAFETY,
        title="Shut Off Main Electrical Breaker & LPG Gas Cylinders",
        instruction="Turn off your home's main electrical breaker switch and close the regulator valves of all domestic cooking gas (LPG) cylinders before evacuating.",
        priority=SafetyPriority.CRITICAL,
        reason="Water submerged electrical outlets cause lethal electrocution; displaced buoyant gas cylinders can rupture pipes and trigger explosions.",
        source="Central Electricity Authority (CEA) Safety Regulations",
        warning="Do not touch the electrical switch panel if you are already standing in water.",
        related_cascading_risk="Electrical short-circuit fires and underwater electrification."
    ),
    SafetyInstructionItem(
        id="fld-dur-03",
        hazard="FLOOD",
        phase=SafetyPhase.DURING,
        category=SafetyCategory.SAFE_ROUTES_EVACUATION,
        title="Comply Instantly with Statutory Evacuation Orders",
        instruction="Evacuate immediately upon announcement of official directives by the District Magistrate / SDMA / NDRF. Do not delay waiting for water to enter the house.",
        priority=SafetyPriority.CRITICAL,
        reason="Under Section 30 of the Disaster Management Act 2005, district authorities order evacuations based on upstream dam discharge and hydrological crest models.",
        source="Disaster Management Act 2005 (Statutory Framework)",
        warning="Self-evacuation during the day is far safer than dangerous night-time boat rescue operations.",
        related_cascading_risk="Stranded populations requiring aerial or boat rescue."
    ),
    SafetyInstructionItem(
        id="fld-dur-04",
        hazard="FLOOD",
        phase=SafetyPhase.DURING,
        category=SafetyCategory.EMERGENCY_CONTACTS,
        title="Signal Distress from Rooftop if Trapped by Sudden Inundation",
        instruction="Move to the highest accessible roof level. Signal distress using a whistle, flashlight, or brightly colored cloth. Dial 112 (National Emergency) or 1078 (NDMA).",
        priority=SafetyPriority.HIGH,
        reason="Blowing a whistle preserves vocal energy and carries sound significantly farther than shouting over the roar of floodwaters.",
        source="NDRF Search and Rescue Operational Protocol",
        warning="Do not climb into an enclosed attic without an exterior roof hatch; rising waters can trap you against the ceiling.",
        related_cascading_risk="Hypothermia and acute exposure."
    ),

    # =========================================================================
    # FLOOD — AFTER
    # =========================================================================
    SafetyInstructionItem(
        id="fld-aft-01",
        hazard="FLOOD",
        phase=SafetyPhase.AFTER,
        category=SafetyCategory.RECOVERY_AND_HEALTH,
        title="Boil All Water Vigorously for 1 Minute Before Consumption",
        instruction="Boil all tap water, open well water, and tube-well water vigorously for at least 1 full minute (or use certified chlorine halogen tablets) before drinking, cooking, or brushing teeth.",
        priority=SafetyPriority.CRITICAL,
        reason="Floodwaters carry sewage pathogens, Escherichia coli, Vibrio cholerae, and Leptospira interrogans bacteria, causing cholera, acute gastroenteritis, and leptospirosis.",
        source="National Centre for Disease Control (NCDC) Post-Disaster Health Advisory",
        warning="Water filters alone may not eliminate viral contaminants if backflow pressure damaged the membrane.",
        related_cascading_risk="Leptospirosis and waterborne diarrheal epidemics.",
        practical_steps=[
            "Bring water to a full rolling boil for a minimum of 60 seconds (or 3 minutes at altitudes above 2000 m).",
            "Allow water to cool naturally in clean, covered glass or stainless steel vessels.",
            "If fuel is unavailable, add 1 certified chlorine purification tablet per 20 litres of clear water; wait 30 minutes before drinking.",
            "Disinfect open well sources using bleaching powder at 2.5 grams per 1,000 litres under PHED supervision."
        ],
        warning_signs=[
            "Family members report sudden vomiting, watery diarrhea, or high fever with muscle cramps.",
            "Well water appears turbid, foul-smelling, or shows visible surface scum post-flood.",
            "Local community PHC reports sudden spike in gastrointestinal infections."
        ],
        what_not_to_do=[
            "Do NOT drink unboiled tap water or ice made from untreated water even if it looks visually clear.",
            "Do NOT use untreated water to wash cooking utensils, vegetables, or baby feeding bottles.",
            "Do NOT swallow water while taking bucket baths."
        ],
        vulnerable_groups="Children under 5 years, elderly grandparents, chemotherapy patients, and anyone with compromised immunity.",
        checklist=[
            "Bring all drinking and cooking water to a 60-second rolling boil",
            "Store boiled water in covered stainless steel vessels with taps",
            "Disinfect water storage tanks and household filters before reuse",
            "Prepare Oral Rehydration Salts (ORS) solution at the first sign of loose stools"
        ]
    ),
    SafetyInstructionItem(
        id="fld-aft-02",
        hazard="FLOOD",
        phase=SafetyPhase.AFTER,
        category=SafetyCategory.PROPERTY_PREPARATION,
        title="Inspect Building Foundation Walls for Structural Cracks",
        instruction="Inspect perimeter walls, pillars, and foundations for new structural cracks, soil settlement, or scouring before allowing family members to re-enter premises.",
        priority=SafetyPriority.CRITICAL,
        reason="Prolonged waterlogging softens sub-surface foundation soil, leading to differential settlement and sudden structural collapse hours after water recedes.",
        source="NDMA Post-Flood Structural Safety Audit Manual",
        warning="Do not enter if walls are bowed, plaster is falling heavily, or doors are jammed.",
        related_cascading_risk="Secondary structural building collapse."
    ),
    SafetyInstructionItem(
        id="fld-aft-03",
        hazard="FLOOD",
        phase=SafetyPhase.AFTER,
        category=SafetyCategory.AVOIDANCE_WHAT_NOT_TO_DO,
        title="Beware of Displaced Venomous Snakes, Scorpions & Rodents",
        instruction="Use a long stick to poke into shoes, bedding, cupboards, and ceiling crevices before reaching with bare hands. Wear sturdy boots while cleaning sludge.",
        priority=SafetyPriority.HIGH,
        reason="Displaced venomous snakes (Cobra, Russell's viper, Krait) seek dry refuge inside homes, furniture, and vehicles during and after floods.",
        source="State Health Departments Anti-Snake Venom (ASV) Protocol",
        warning="Never reach into dark corners or under debris with unprotected hands.",
        related_cascading_risk="Post-flood snakebite morbidity spikes."
    ),
    SafetyInstructionItem(
        id="fld-aft-04",
        hazard="FLOOD",
        phase=SafetyPhase.AFTER,
        category=SafetyCategory.DAMAGE_DOCUMENTATION,
        title="Photograph and Document All Damage Before Cleaning",
        instruction="Take clear date-stamped photographs and videos of flood waterline marks on walls, damaged furniture, appliances, crops, and structures before discarding items.",
        priority=SafetyPriority.RECOMMENDED,
        reason="Visual evidence is mandatory for revenue department damage assessment surveys (Girdawari), State Disaster Response Fund (SDRF) relief, and insurance claims.",
        source="Disaster Management Division, Ministry of Home Affairs SDRF Guidelines",
        related_cascading_risk="Delayed statutory financial relief disbursement."
    ),

    # =========================================================================
    # CYCLONE — BEFORE, DURING, AFTER
    # =========================================================================
    SafetyInstructionItem(
        id="cyc-bef-01",
        hazard="CYCLONE",
        phase=SafetyPhase.BEFORE,
        category=SafetyCategory.PROPERTY_PREPARATION,
        title="Board Up Glass Windows & Anchor Corrugated Roofing",
        instruction="Board up large glass windows or apply heavy-duty criss-cross tape to prevent shattering; securely anchor or remove loose tin sheets, solar panels, and asbestos roofing.",
        priority=SafetyPriority.CRITICAL,
        reason="High gale winds transform loose corrugated roofing sheets into lethal airborne projectiles traveling at over 120 km/h.",
        source="IMD Cyclone Warning Services SOP",
        related_cascading_risk="Flying debris trauma and structural roof shearing."
    ),
    SafetyInstructionItem(
        id="cyc-bef-02",
        hazard="CYCLONE",
        phase=SafetyPhase.BEFORE,
        category=SafetyCategory.POWER_AND_LIGHTING,
        title="Fully Charge All Phones, Solar Lanterns & Power Banks",
        instruction="Charge mobile phones, rechargeable lanterns, and auxiliary power banks to 100%. Write essential family contact numbers on paper in case of battery depletion.",
        priority=SafetyPriority.HIGH,
        reason="Power grids are preemptively shut down during cyclones to prevent electrocution and fires from fallen lines, often resulting in 3 to 7 days of blackout.",
        source="State Disaster Management Authorities Coastal SOP",
        related_cascading_risk="Prolonged power grid failure and telecommunications blackout."
    ),
    SafetyInstructionItem(
        id="cyc-bef-03",
        hazard="CYCLONE",
        phase=SafetyPhase.BEFORE,
        category=SafetyCategory.SAFE_ROUTES_EVACUATION,
        title="Evacuate Kutcha / Thatched Houses to Pucca Cyclone Shelters",
        instruction="If residing in a kutcha, asbestos, or mud-brick house within 5 km of the coast, evacuate to a dedicated multi-purpose cyclone shelter before winds reach gale force.",
        priority=SafetyPriority.CRITICAL,
        reason="Kutcha structures cannot withstand sustained cyclonic wind pressures (> 90 km/h) or storm surge inundation exceeding 1.5 meters.",
        source="National Cyclone Risk Mitigation Project (NCRMP) Guidelines",
        warning="Never stay inside a thatched or tin-roof house once an Orange or Red cyclone alert is issued.",
        related_cascading_risk="Catastrophic structural collapse under aerodynamic wind load."
    ),
    SafetyInstructionItem(
        id="cyc-dur-01",
        hazard="CYCLONE",
        phase=SafetyPhase.DURING,
        category=SafetyCategory.AVOIDANCE_WHAT_NOT_TO_DO,
        title="Do NOT Venture Outdoors During the Calm 'Eye' of the Cyclone",
        instruction="If winds suddenly stop and the sky clears, stay indoors! The 'eye' of the cyclone is passing; violent gale winds will resume abruptly from the opposite direction.",
        priority=SafetyPriority.CRITICAL,
        reason="The central eye of a tropical cyclone features deceptive calm; reverse winds on the back-side of the eyewall strike with maximum destructive fury without warning.",
        source="IMD Forecasters Manual for Tropical Cyclones",
        warning="Many casualties occur when people venture out during the eye to inspect damage.",
        related_cascading_risk="Violent wind reversals catching citizens exposed outdoors."
    ),
    SafetyInstructionItem(
        id="cyc-dur-02",
        hazard="CYCLONE",
        phase=SafetyPhase.DURING,
        category=SafetyCategory.SAFE_ROUTES_EVACUATION,
        title="Shelter in the Strongest Interior Room Away from Windows",
        instruction="Stay in the central reinforced room or hallway of the house. Keep blankets and mattresses nearby to shield against falling plaster or flying glass shards.",
        priority=SafetyPriority.CRITICAL,
        reason="Internal partition walls provide the highest structural rigidity and are protected from direct exterior aerodynamic wind blast.",
        source="NDMA Cyclone Management Guidelines",
        related_cascading_risk="Flying glass splinter lacerations."
    ),
    SafetyInstructionItem(
        id="cyc-aft-01",
        hazard="CYCLONE",
        phase=SafetyPhase.AFTER,
        category=SafetyCategory.UTILITY_SAFETY,
        title="Treat All Downed Electrical Cables as Live and Lethal",
        instruction="Do not touch or approach fallen electrical poles, dangling service wires, or corrugated metal fences touching wet ground. Keep a minimum 10-meter clearance.",
        priority=SafetyPriority.CRITICAL,
        reason="Snapped conductors can remain energized by back-feeding from residential inverters or delayed sub-station trips, carrying fatal voltages across wet soil.",
        source="Central Electricity Authority Safety Handbook",
        warning="Never drive over downed power lines entangled in tree branches.",
        related_cascading_risk="Electrocution from grounded electrical lines."
    ),
    SafetyInstructionItem(
        id="cyc-aft-02",
        hazard="CYCLONE",
        phase=SafetyPhase.AFTER,
        category=SafetyCategory.WATER_AND_FOOD,
        title="Avoid Brackish Drinking Wells Contaminated by Storm Surge",
        instruction="Do not drink from open wells or shallow handpumps in coastal flood zones until salinity testing and hyper-chlorination are completed by health authorities.",
        priority=SafetyPriority.HIGH,
        reason="Marine storm surge forces seawater into coastal freshwater aquifers, rendering groundwater non-potable and causing severe electrolyte imbalance if ingested.",
        source="Central Ground Water Board (CGWB) Coastal Salinity Advisory",
        related_cascading_risk="Long-term drinking water salinization."
    ),

    # =========================================================================
    # EARTHQUAKE — BEFORE, DURING, AFTER
    # =========================================================================
    SafetyInstructionItem(
        id="eqk-bef-01",
        hazard="EARTHQUAKE",
        phase=SafetyPhase.BEFORE,
        category=SafetyCategory.PROPERTY_PREPARATION,
        title="Secure Tall Furniture & Heavy Wall Hangings with L-Brackets",
        instruction="Fasten tall cupboards, refrigerators, heavy mirrors, water geysers, and bookshelves securely to wall studs using metal L-brackets.",
        priority=SafetyPriority.CRITICAL,
        reason="Toppling furniture and falling geysers account for over 60% of non-fatal injuries and trap egress routes during moderate to severe seismic shocks.",
        source="BIS IS 13935: Indian Standard for Seismic Evaluation and Strengthening of Buildings",
        related_cascading_risk="Toppling furniture blocking primary evacuation hallways."
    ),
    SafetyInstructionItem(
        id="eqk-bef-02",
        hazard="EARTHQUAKE",
        phase=SafetyPhase.BEFORE,
        category=SafetyCategory.FAMILY_COMMUNICATION,
        title="Practice 'Drop, Cover, and Hold On' Drills Biannually",
        instruction="Ensure every family member knows the safe spots in each room: under sturdy wooden desks/tables or against interior load-bearing walls away from glass windows.",
        priority=SafetyPriority.HIGH,
        reason="Seismic shaking induces panic; instinctive muscle memory developed through drills allows survival actions within the first 3 seconds of ground acceleration.",
        source="NDMA Earthquake Management Guidelines",
        related_cascading_risk="Panic-induced stampedes in stairwells."
    ),
    SafetyInstructionItem(
        id="eqk-dur-01",
        hazard="EARTHQUAKE",
        phase=SafetyPhase.DURING,
        category=SafetyCategory.AVOIDANCE_WHAT_NOT_TO_DO,
        title="DROP, COVER, and HOLD ON — Do NOT Run Outside During Shaking",
        instruction="DROP down onto hands and knees; COVER your head and neck beneath a sturdy desk or table; HOLD ON until shaking stops completely. Do NOT rush outdoors.",
        priority=SafetyPriority.CRITICAL,
        reason="Running outside exposes individuals to falling exterior brick parapets, shattered window glass, architectural cornices, and falling electrical wires, which cause the vast majority of seismic deaths.",
        source="National Disaster Management Guidelines: Management of Earthquakes",
        warning="Never use elevators during or immediately following ground tremors.",
        related_cascading_risk="Falling facade masonry and glass showers."
    ),
    SafetyInstructionItem(
        id="eqk-dur-02",
        hazard="EARTHQUAKE",
        phase=SafetyPhase.DURING,
        category=SafetyCategory.AVOIDANCE_WHAT_NOT_TO_DO,
        title="If in an Open Field or Vehicle: Stay Clear of Structures",
        instruction="If outdoors, move into an open area away from high-rise buildings, flyovers, billboards, and high-voltage transmission lines. If driving, pull over smoothly away from overpasses.",
        priority=SafetyPriority.HIGH,
        reason="Non-engineered parapets and utility poles readily collapse outward into street corridors during horizontal ground accelerations.",
        source="NDMA Earthquake SOP",
        related_cascading_risk="Pylon collapse and vehicle crushing."
    ),
    SafetyInstructionItem(
        id="eqk-aft-01",
        hazard="EARTHQUAKE",
        phase=SafetyPhase.AFTER,
        category=SafetyCategory.UTILITY_SAFETY,
        title="Sniff for LPG Gas Leaks Before Operating Any Electrical Switches",
        instruction="Check for gas smell immediately upon evacuation. If gas odor is present, open windows, extinguish any open flames, evacuate outdoors, and do NOT turn light switches ON or OFF.",
        priority=SafetyPriority.CRITICAL,
        reason="Operating electrical switches generates micro-sparks that can ignite gas-air mixtures released from seismic ruptures in domestic LPG cylinder pipes.",
        source="Petroleum and Explosives Safety Organisation (PESO) Safety Bulletin",
        warning="Do not light matches, candles, or lighters; use battery-powered flashlights only.",
        related_cascading_risk="Post-earthquake urban conflagrations and gas explosions."
    ),
    SafetyInstructionItem(
        id="eqk-aft-02",
        hazard="EARTHQUAKE",
        phase=SafetyPhase.AFTER,
        category=SafetyCategory.AVOIDANCE_WHAT_NOT_TO_DO,
        title="Expect Aftershocks — Do NOT Re-Enter Visibly Cracked Buildings",
        instruction="Remain in open ground. Do not re-enter structures with visible diagonal shear cracks, bowed pillars, or damaged stairwells until cleared by licensed structural engineers.",
        priority=SafetyPriority.CRITICAL,
        reason="Aftershocks can trigger the complete pancake collapse of buildings already weakened by the main shock.",
        source="Geological Survey of India (GSI) Post-Earthquake Safety Protocol",
        warning="Earthquake aftershocks cannot be temporally predicted; treat damaged buildings with utmost caution.",
        related_cascading_risk="Secondary progressive structural collapse during aftershocks."
    ),

    # =========================================================================
    # HEATWAVE — BEFORE, DURING, AFTER
    # =========================================================================
    SafetyInstructionItem(
        id="htw-bef-01",
        hazard="HEATWAVE",
        phase=SafetyPhase.BEFORE,
        category=SafetyCategory.MEDICAL_AND_HEALTH,
        title="Stock Oral Rehydration Salts (ORS) & Maintain Home Hydration",
        instruction="Keep packets of ORS, glucose, electoral powders, and clean water containers stocked at home. Prepare natural coolers like buttermilk, aam panna, and lemon water.",
        priority=SafetyPriority.CRITICAL,
        reason="Severe sweating depletes essential sodium and potassium electrolytes rapidly, leading to hypokalemia, painful muscle cramps, and heat exhaustion.",
        source="NDMA National Guidelines for Preparation of Action Plan for Prevention and Management of Heat Wave",
        related_cascading_risk="Acute fluid deficit and circulatory heat collapse."
    ),
    SafetyInstructionItem(
        id="htw-bef-02",
        hazard="HEATWAVE",
        phase=SafetyPhase.BEFORE,
        category=SafetyCategory.PROPERTY_PREPARATION,
        title="Install Window Shades, Bamboo Blinds & Lime-Wash Roofs",
        instruction="Cover sun-facing windows with reflective film, dark curtains, or bamboo chiks. Applying reflective white lime-wash on flat roofs can reduce indoor temperatures by up to 5°C.",
        priority=SafetyPriority.HIGH,
        reason="Thermal radiant ingress through unshaded masonry and single-pane glass elevates indoor temperatures far above outdoor ambient levels.",
        source="Bureau of Energy Efficiency (BEE) Cool Roofs Guidelines",
        related_cascading_risk="Indoor thermal trapping and nighttime heat stress."
    ),
    SafetyInstructionItem(
        id="htw-dur-01",
        hazard="HEATWAVE",
        phase=SafetyPhase.DURING,
        category=SafetyCategory.WATER_AND_FOOD,
        title="Drink Plenty of Water Frequently, Even Without Feeling Thirsty",
        instruction="Drink clean water every 20 to 30 minutes throughout the day. Avoid alcohol, excessive tea, coffee, and carbonated soft drinks, which dehydrate the body.",
        priority=SafetyPriority.CRITICAL,
        reason="Thirst is a delayed physiological indicator of dehydration; drinking regularly maintains blood volume and core thermal regulation.",
        source="Ministry of Health and Family Welfare (MoHFW) National Heat Health Advisory",
        related_cascading_risk="Exertional dehydration and kidney stress."
    ),
    SafetyInstructionItem(
        id="htw-dur-02",
        hazard="HEATWAVE",
        phase=SafetyPhase.DURING,
        category=SafetyCategory.AVOIDANCE_WHAT_NOT_TO_DO,
        title="Avoid Direct Sun Exposure Between 12:00 PM and 3:30 PM",
        instruction="Reschedule heavy agricultural work, construction, outdoor labor, and sports to early morning (before 9 AM) or late evening (after 5 PM).",
        priority=SafetyPriority.CRITICAL,
        reason="Solar ultraviolet irradiation and ambient dry-bulb temperatures peak during this midday window, dramatically escalating the risk of acute Heat Stroke.",
        source="Ministry of Labour and Employment Occupational Heat Stress Advisories",
        warning="Never leave young children, elderly persons, or pets inside a parked vehicle.",
        related_cascading_risk="Occupational heat stroke emergencies."
    ),
    SafetyInstructionItem(
        id="htw-dur-03",
        hazard="HEATWAVE",
        phase=SafetyPhase.DURING,
        category=SafetyCategory.MEDICAL_AND_HEALTH,
        title="Recognize Heat Stroke Symptoms & Administer Rapid Cooling",
        instruction="If someone develops high body temperature (> 40°C), ceases sweating, exhibits confusion or loss of consciousness: Move to shade, apply ice packs to neck/armpits/groin, and call 108 immediately.",
        priority=SafetyPriority.CRITICAL,
        reason="Heat stroke is a medical emergency with up to 50% mortality if core body cooling is delayed beyond 30 minutes.",
        source="MoHFW Emergency Clinical Protocol for Heat-Related Illnesses",
        warning="Heat stroke requires immediate aggressive external water cooling; do not administer oral fluids to an unconscious person.",
        related_cascading_risk="Multi-organ failure from extreme hyperthermia."
    ),
    SafetyInstructionItem(
        id="htw-aft-01",
        hazard="HEATWAVE",
        phase=SafetyPhase.AFTER,
        category=SafetyCategory.VULNERABLE_MEMBERS,
        title="Monitor Elderly & Vulnerable Relatives for Delayed Thermal Stress",
        instruction="Continue monitoring hydration and mental alertness of elderly individuals, pregnant women, and infants for 48 hours following a severe heatwave episode.",
        priority=SafetyPriority.HIGH,
        reason="Elderly individuals have diminished thirst sensation and reduced cardiovascular reserve, often presenting with delayed electrolyte collapse days after heat waves.",
        source="National Health Mission Elderly Care Protocols",
        related_cascading_risk="Delayed geriatric cardiovascular decompensation."
    ),

    # =========================================================================
    # LANDSLIDE — BEFORE, DURING, AFTER
    # =========================================================================
    SafetyInstructionItem(
        id="lnd-bef-01",
        hazard="LANDSLIDE",
        phase=SafetyPhase.BEFORE,
        category=SafetyCategory.PROPERTY_PREPARATION,
        title="Recognize Precursor Geological Warning Signs on Slopes",
        instruction="Regularly inspect retaining walls, slopes behind your house, and paved paths for new tension fissures, tilting utility poles/trees, sticking windows, or bulging masonry.",
        priority=SafetyPriority.CRITICAL,
        reason="Slope failure surfaces develop tensile deformation cracks and creep displacement days or weeks before catastrophic sudden shear failure.",
        source="Geological Survey of India (GSI) Landslide Awareness Guidelines",
        related_cascading_risk="Toe slumping and sudden slope failure."
    ),
    SafetyInstructionItem(
        id="lnd-bef-02",
        hazard="LANDSLIDE",
        phase=SafetyPhase.BEFORE,
        category=SafetyCategory.SAFE_ROUTES_EVACUATION,
        title="Map Evacuation Routes That Avoid Gullies & Narrow Hill Defiles",
        instruction="Identify secondary escape routes that stay on stable bedrock ridges. Never choose paths along mountain stream gullies, ravine floors, or directly beneath steep talus cones.",
        priority=SafetyPriority.CRITICAL,
        reason="Debris flows channel high-velocity mud, boulders, and uprooted trees directly into natural stream gullies and ravines at speeds exceeding 40 km/h.",
        source="NDMA National Landslide Risk Management Strategy",
        warning="Never build or pitch tents near the base of steep slopes or dry mountain channels.",
        related_cascading_risk="Rapid channeled debris avalanche."
    ),
    SafetyInstructionItem(
        id="lnd-dur-01",
        hazard="LANDSLIDE",
        phase=SafetyPhase.DURING,
        category=SafetyCategory.AVOIDANCE_WHAT_NOT_TO_DO,
        title="Move Laterally Away from Debris Path — Never Outrun Downhill",
        instruction="If you hear rumbling, trees snapping, or notice sudden mudflow, move laterally (perpendicular) to the slide path. Never attempt to run straight downhill ahead of the debris flow.",
        priority=SafetyPriority.CRITICAL,
        reason="Debris flows accelerate down-gradient and spread laterally; escaping sideways to higher stable ridges is the only viable physical evasion strategy.",
        source="Border Roads Organisation (BRO) Hill Road Safety Manual",
        warning="If escape is impossible, curl into a tight ball beneath a reinforced pillar and protect your head with your arms.",
        related_cascading_risk="Crushing trauma from high-velocity boulder flows."
    ),
    SafetyInstructionItem(
        id="lnd-aft-01",
        hazard="LANDSLIDE",
        phase=SafetyPhase.AFTER,
        category=SafetyCategory.AVOIDANCE_WHAT_NOT_TO_DO,
        title="Stay Clear of Slide Perimeter — Expect Delayed Secondary Failures",
        instruction="Do not approach the perimeter of a fresh landslide. Secondary slides frequently occur hours or days after the primary failure as unsupported scarp slopes collapse.",
        priority=SafetyPriority.CRITICAL,
        reason="The head scarp and lateral margins of a fresh slide remain in an unstable critical state of equilibrium (Factor of Safety < 1.0).",
        source="NDMA Landslide Post-Event Safety Guidelines",
        warning="Never walk over unconsolidated slide debris; mud crusts can conceal deep water pockets or unstable voids.",
        related_cascading_risk="Secondary progressive head-scarp collapse."
    ),
    SafetyInstructionItem(
        id="lnd-aft-02",
        hazard="LANDSLIDE",
        phase=SafetyPhase.AFTER,
        category=SafetyCategory.SAFE_ROUTES_EVACUATION,
        title="Alert Downstream Communities if River Flow Stoppage is Observed",
        instruction="If a mountain river downstream of a slide suddenly dries up or drops dramatically, evacuate downstream riverbanks immediately and notify district authorities (112 / 1077).",
        priority=SafetyPriority.CRITICAL,
        reason="Sudden river stoppage indicates a natural landslide dam has formed upstream; when the debris dam breaches, a catastrophic flash flood wave is released.",
        source="Central Water Commission Landslide Dam Outburst Flood (LDOF) Advisory",
        related_cascading_risk="Landslide lake outburst floods (LDOF)."
    ),

    # =========================================================================
    # SEVERE WEATHER — BEFORE, DURING, AFTER
    # =========================================================================
    SafetyInstructionItem(
        id="swx-bef-01",
        hazard="SEVERE_WEATHER",
        phase=SafetyPhase.BEFORE,
        category=SafetyCategory.UTILITY_SAFETY,
        title="Unplug Sensitive Electronic Equipment & Computer Modems",
        instruction="Disconnect computers, televisions, air-conditioners, and internet modems from electrical wall outlets before severe thunderstorms begin.",
        priority=SafetyPriority.HIGH,
        reason="Lightning strikes induce massive high-voltage transient surges along overhead power and telecom cables, destroying internal transformer circuits.",
        source="Bureau of Indian Standards IS 2309: Protection of Buildings and Allied Structures Against Lightning",
        related_cascading_risk="Electrical short-circuit fires and appliance destruction."
    ),
    SafetyInstructionItem(
        id="swx-dur-01",
        hazard="SEVERE_WEATHER",
        phase=SafetyPhase.DURING,
        category=SafetyCategory.AVOIDANCE_WHAT_NOT_TO_DO,
        title="Apply the 30-30 Rule & Never Shelter Under Tall Isolated Trees",
        instruction="If the delay between lightning flash and thunderclap is under 30 seconds, seek indoor shelter immediately. Never shelter under tall isolated trees, open metal tin sheds, or mobile towers.",
        priority=SafetyPriority.CRITICAL,
        reason="Tall isolated trees attract step-leader lightning strikes, causing fatal ground surface currents (step voltage) and side-flash discharges to nearby persons.",
        source="NDMA National Guidelines on Lightning Risk Management",
        warning="If trapped in an open field, crouch low on the balls of your feet with heels touching; minimize contact with the ground.",
        related_cascading_risk="Direct lightning strike and step-voltage electrocution."
    ),
    SafetyInstructionItem(
        id="swx-dur-02",
        hazard="SEVERE_WEATHER",
        phase=SafetyPhase.DURING,
        category=SafetyCategory.SAFE_ROUTES_EVACUATION,
        title="Never Drive Into Submerged Railway or Road Underpasses",
        instruction="Avoid low-lying underpasses during heavy downpours. If water covers the curb or approaches tire rim height, turn around immediately.",
        priority=SafetyPriority.CRITICAL,
        reason="Urban underpasses act as natural drainage sumps, rapidly accumulating 2 to 3 meters of runoff within 15 minutes, which stalls vehicle engines and traps occupants.",
        source="Ministry of Road Transport and Highways (MoRTH) Monsoon Traffic Advisory",
        warning="Electric windows and door locks fail once a vehicle's battery is submerged.",
        related_cascading_risk="Urban underpass drowning and vehicular entrapment."
    ),
    SafetyInstructionItem(
        id="swx-aft-01",
        hazard="SEVERE_WEATHER",
        phase=SafetyPhase.AFTER,
        category=SafetyCategory.AVOIDANCE_WHAT_NOT_TO_DO,
        title="Wait At Least 30 Minutes After the Last Thunderclap Before Resuming Outdoors",
        instruction="Remain inside a safe pucca structure for at least 30 minutes following the last audible sound of thunder, even if rain has stopped and blue skies appear.",
        priority=SafetyPriority.HIGH,
        reason="Lightning can strike up to 15 kilometers away from the parent storm cloud, originating from the anvil overhang of departing thunderstorm cells.",
        source="IMD Lightning Early Warning and Safety Manual",
        related_cascading_risk="Delayed bolt-from-the-blue lightning fatalities."
    )
]


class ExtendedCitizenSafetyEngine:
    """Provides structured, scalable citizen safety guidance across all 6 disaster hazards."""

    def __init__(self):
        self._items: List[SafetyInstructionItem] = RAW_SAFETY_INSTRUCTIONS

    def get_instructions(
        self,
        hazard: Optional[str] = None,
        phase: Optional[str] = None,
        category: Optional[str] = None,
        priority: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Filters safety guidance based on hazard, phase, category, or priority."""
        filtered = self._items

        if hazard:
            h_clean = hazard.upper().strip()
            filtered = [i for i in filtered if i.hazard == h_clean]

        if phase:
            p_clean = phase.upper().strip()
            filtered = [i for i in filtered if i.phase.value == p_clean]

        if category:
            c_clean = category.upper().strip()
            filtered = [i for i in filtered if i.category.value == c_clean]

        if priority:
            pr_clean = priority.upper().strip()
            filtered = [i for i in filtered if i.priority.value == pr_clean]

        return [i.to_dict() for i in filtered]

    def get_complete_hazard_guide(self, hazard: str) -> Dict[str, Any]:
        """Returns the full Before / During / After structured guide for a hazard."""
        h_clean = hazard.upper().strip()
        if h_clean not in SUPPORTED_HAZARDS:
            h_clean = "FLOOD"

        before_items = [i.to_dict() for i in self._items if i.hazard == h_clean and i.phase == SafetyPhase.BEFORE]
        during_items = [i.to_dict() for i in self._items if i.hazard == h_clean and i.phase == SafetyPhase.DURING]
        after_items = [i.to_dict() for i in self._items if i.hazard == h_clean and i.phase == SafetyPhase.AFTER]

        categories_represented = sorted(list(set(
            i.category.value for i in self._items if i.hazard == h_clean
        )))

        return {
            "hazard": h_clean,
            "statutory_notice": (
                "Preparation actions may be undertaken independently at any time. "
                "Mandatory evacuation directives are ordered exclusively by civil authorities "
                "(District Magistrate / SDMA / NDRF) under the Disaster Management Act 2005."
            ),
            "emergency_contacts": {
                "national_emergency": "112",
                "ndma_disaster_helpline": "1078",
                "state_emergency_operation_center": "1070",
                "ambulance": "108"
            },
            "total_action_items": len(before_items) + len(during_items) + len(after_items),
            "categories_covered": categories_represented,
            "phases": {
                "BEFORE": {
                    "phase_title": "Before Event // Preparedness & Household Mitigation",
                    "item_count": len(before_items),
                    "items": before_items
                },
                "DURING": {
                    "phase_title": "During Event // Immediate Life Safety & Defensive Action",
                    "item_count": len(during_items),
                    "items": during_items
                },
                "AFTER": {
                    "phase_title": "After Event // Safe Recovery, Health Protection & Relief Claims",
                    "item_count": len(after_items),
                    "items": after_items
                }
            },
            "synthetic_records": 0
        }

    def get_catalog_summary(self) -> Dict[str, Any]:
        """Provides an overview of all supported hazard guides."""
        hazards_summary = {}
        for h in SUPPORTED_HAZARDS:
            items = [i for i in self._items if i.hazard == h]
            hazards_summary[h] = {
                "total_items": len(items),
                "before_count": sum(1 for i in items if i.phase == SafetyPhase.BEFORE),
                "during_count": sum(1 for i in items if i.phase == SafetyPhase.DURING),
                "after_count": sum(1 for i in items if i.phase == SafetyPhase.AFTER),
                "critical_count": sum(1 for i in items if i.priority == SafetyPriority.CRITICAL)
            }

        return {
            "supported_hazards": SUPPORTED_HAZARDS,
            "total_catalog_items": len(self._items),
            "hazards": hazards_summary,
            "synthetic_records": 0
        }


extended_safety_engine = ExtendedCitizenSafetyEngine()
