# RISK // INDIA — PHASE 30E ARCHITECTURE SPECIFICATION
## National Crisis Mode, Emergency Response & Human Action Intelligence

### 1. Executive Summary

Phase 30E marks the definitive transformation of **RISK // INDIA** from a predictive and analytical risk platform into a **National Public Disaster Assistance System**. In life-threatening emergencies, citizens do not simply need raw probabilities or numerical scores; they require unambiguous, immediate answers to four fundamental questions:

1. **What is happening?**
2. **What could happen next?**
3. **What should I do right now?**
4. **What should I do before, during, and after the disaster?**

Phase 30E delivers this human-first disaster assistance architecture across all **28 States and 8 Union Territories (36 administrative entities)** for all six core disaster hazards: **FLOOD**, **CYCLONE**, **HEATWAVE**, **LANDSLIDE**, **SEVERE_WEATHER**, and **EARTHQUAKE**.

---

### 2. Operational State Model & Deterministic Activation Rules

The system establishes four operational posture states: `CRISIS`, `ELEVATED`, `WATCH`, and `NORMAL`. These are operational and presentation states, maintaining separation from scientific ML risk scores and decoupled freshness indicators.

#### Deterministic Activation Engine (`CrisisActivationEngine`)

The engine evaluates five deterministic rules combined with a weak-signal filter:

- **Rule A (Verified Statutory Warning):**
  - An active **RED** bulletin issued by statutory nodal agencies (IMD, CWC, INCOIS) deterministically escalates the operational state to `CRISIS` and triggers `is_crisis_recommended = True`.
  - An active **ORANGE/AMBER** alert elevates the state to `ELEVATED` with `is_crisis_recommended = True`.
- **Rule B (High / Critical Current Risk with Valid Telemetry):**
  - Current risk evaluated as `CRITICAL` supported by fresh empirical sensor telemetry sets state to `CRISIS`.
  - Current risk evaluated as `HIGH` sets state to `ELEVATED`.
- **Rule C (High Future-Risk Signal with Evidence):**
  - Projections showing `CRITICAL` or `HIGH` risk in near-term forecast horizons (0–6h, 6–24h) with confidence $\ge 0.40$ set state to `CRISIS` or `ELEVATED`.
- **Rule D (Multi-Signal Convergence):**
  - Convergence of multiple critical thresholds (e.g. 24h rainfall $\ge 64.5\text{ mm}$ + river gauge stage $\ge 90\%$ of danger level) elevates state to `ELEVATED`.
- **Rule E (User Manual Activation):**
  - Citizen or emergency manager explicitly activating the Crisis Mode toggle forces `CRISIS` operational state with `is_manual_activation = True`.
- **Weak-Signal Filter:**
  - An isolated, low-confidence or stale forecast without corroborating warning or empirical telemetry does NOT trigger an automated emergency state. Baseline conditions remain `NORMAL` or `WATCH`.

---

### 3. Human Action Intelligence Architecture (`CrisisActionEngine`)

#### Top 3–5 "What Should I Do Right Now?" Actions
For every hazard, immediate actions are ranked strictly in order of survival and life safety:
1. **Immediate Life Safety** (`LIFE_SAFETY`): Seek high ground, move indoors, drop/cover/hold on.
2. **Official Evacuation Compliance** (`EVACUATION`): Comply with DDMA/SDRF orders; leave prior to rising floodwaters or squall arrival.
3. **Hazard Danger Avoidance** (`AVOID_DANGER`): Turn off mains electricity/gas; never walk or drive through moving water; avoid downed cables, exterior glass, or steep slopes.
4. **Emergency Communication & Signaling** (`COMMUNICATION`): Battery preservation; signaling distress via whistle/torch/bright cloth; dialing 112 / 1078.
5. **Emergency Resources & Go-Bag** (`EMERGENCY_RESOURCES`): Waterproof identity documents, prescription medicines, sealed potable water.

#### Before / During / After Protocols
Comprehensive life-safety action protocols partitioned across the three disaster lifecycle phases are codified for all six supported hazards:
- `FLOOD`: 72h go-bag, drain clearing, moving valuables $\rightarrow$ Evacuation compliance, power cut-off, avoiding flowing water $\rightarrow$ Water boiling, building foundation checks, snakebite precautions.
- `CYCLONE`: Storm shutters, branch trimming, boat securing $\rightarrow$ Sturdy interior sheltering, eye-of-storm calm warning $\rightarrow$ Fallen live wire avoidance, foundation scour inspection.
- `HEATWAVE`: ORS/hydration preparation, daytime window shading $\rightarrow$ Peak hours indoor shelter (11am-4pm), frequent electrolyte intake, checking vulnerable elders $\rightarrow$ Slow cooling, rehydration monitoring.
- `LANDSLIDE`: Hillside crack mapping, community whistle codes $\rightarrow$ Immediate slope zone evacuation, ravine avoidance $\rightarrow$ Secondary slide avoidance, river damming reporting.
- `SEVERE_WEATHER`: Roof tie-downs, lightning rod inspection $\rightarrow$ 30-30 Rule indoor sheltering, avoiding plumbing/trees $\rightarrow$ CPR on lightning victims, downed line avoidance.
- `EARTHQUAKE`: Furniture anchoring, bedside torch $\rightarrow$ Drop, Cover, and Hold On drills, stay away from glass $\rightarrow$ Injury treatment, sniffing for gas leaks, expecting aftershocks.

#### 72-Hour Family Disaster Preparedness Checklist
Standard checklist detailing critical items:
- **Water & Hydration**: 12 Liters potable water per person (3-4 L/person/day for 3 days).
- **Food & Nutrition**: Non-perishable ready-to-eat rations (chana, dates, sattu, biscuits, baby formula).
- **Medical & First Aid**: 7-day prescription drugs, ORS, bandages, antiseptics, paracetamol.
- **Power & Light**: 20,000mAh charged power bank, heavy-duty LED torch, spare batteries.
- **Emergency Documents**: Waterproof sealed pouch for Aadhaar, property deeds, insurance.
- **Safety Gear**: Pealess whistle for distress signaling, heavy-duty work gloves.
- **Cash & Finance**: Physical banknotes in small denominations for POS/ATM network blackouts.
- **Communication**: Battery-powered AM/FM transistor radio for civil protection broadcasts.

---

### 4. Verified Statutory Emergency Resources (`CrisisResourceEngine`)

#### Absolute Zero Invented Resources Guard
- Zero synthetic or mock emergency resources are generated.
- All entries originate from the verified statutory registry (`VERIFIED_RESOURCES_REGISTRY`): NDMA HQ, NDRF Battalions, SDRF Units, State Disaster Operations Centres, and official 24/7 helplines.
- **Mandatory Safety Fallback**: If a verified local resource is absent in a specific remote district or union territory, the system explicitly returns:
  > *"Verified nearby resource location is currently unavailable. Pan-India statutory emergency response helplines (NDMA 1078, NDRF 011-24363260, Emergency 112) remain operational 24/7."*
- Proximity-based distance calculations (Haversine formula in km) are computed when user geolocation coordinates are provided.

---

### 5. 5-Horizon Unified Timeline Progression (`CrisisTimelineEngine`)

Provides a coherent, chronological multi-horizon view:
1. `NOW`: Current situation from live empirical telemetry and active IMD/CWC warnings (`OBSERVED` or `EMPIRICAL_ML`).
2. `0_6H`: Immediate flash / nowcast window (`OFFICIAL_WARNING` or `FORECAST`).
3. `6_24H`: Near-term NWP forecast window (`FORECAST_DERIVED_RISK`).
4. `1_3D`: Extended synoptic multi-model outlook (`FORECAST`).
5. `3_7D`: Medium-range climatological baseline (`BASELINE`).

Every milestone explicitly retains its signal type (`TimelineSignalType`) and data provenance.

---

### 6. Transparent Deterministic Explanation (`CrisisExplanationEngine`)

Plain-language explanations answering five questions:
1. **Why this risk was assessed:** Primary physical drivers (e.g. active red alert, intense rainfall, river stage surcharge).
2. **What changed recently:** Anomalies compared to historical seasonal baselines.
3. **Supporting tangible evidence:** Exact numerical records and official bulletins.
4. **What could change this risk:** Plausible meteorological escalation and mitigation scenarios.
5. **What we do NOT know (Data limitations):** Honest declarations regarding micro-scale cloudburst limits, unmonitored rural drainage choke points, and building-specific resonance.

---

### 7. Absolute Project Invariants & Scientific Guards

1. **Assam ML Prototype Model Invariant**:
   `ml/flood/artifacts/model.joblib`
   SHA-256: `0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf` (PRESERVED BYTE-FOR-BYTE)
2. **Assam Flood Features Dataset Invariant**:
   `datasets/processed/flood_assam/flood_features.csv`
   SHA-256: `88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080` (PRESERVED BYTE-FOR-BYTE)
3. **Non-Assam ML Guard**:
   Machine learning inference is strictly restricted to Assam (`ml_available = False`, `status = NOT_AVAILABLE` outside Assam). All other entities use empirical hydromet sensor telemetry, NWP, and statutory IMD/CWC bulletins.
4. **Earthquake Non-Prediction Guard**:
   Earthquakes cannot be deterministically predicted. Future projections for earthquake hazards are clamped to tectonic baselines with explicit disclaimers; no future earthquake predictions are attempted (`is_predictable = False`).
5. **Zero Synthetic Records Guard**:
   `synthetic_records = 0` is strictly audited and maintained across all backend endpoints and frontend data structures.
6. **Freshness Orthogonality**:
   Freshness remains orthogonal to severity: high risk with old telemetry remains `STALE`.

---

### 8. API Endpoint Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/crisis/status` | Global crisis posture, active recommendations count, emergency numbers |
| `GET` | `/api/crisis/national` | Comprehensive 36-entity national crisis overview and state distribution |
| `GET` | `/api/crisis/{region}` | Full regional assessment: what is happening, what to do now, Before/During/After |
| `GET` | `/api/crisis/{region}/{hazard}` | Tailored hazard-specific assessment for an entity |
| `GET` | `/api/crisis/{region}/actions` | Top 3–5 prioritized actions, Before/During/After protocols, 72h checklist |
| `GET` | `/api/crisis/{region}/resources` | Verified emergency helplines, rescue battalions, proximity sorting |
| `GET` | `/api/crisis/{region}/timeline` | 5-horizon progression with explicit provenance tags |
| `GET` | `/api/crisis/{region}/explanation` | Deterministic plain-language explanation and data limitations |
