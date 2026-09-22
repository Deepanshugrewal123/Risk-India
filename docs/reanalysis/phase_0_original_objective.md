# RISK // INDIA — Phase 0 Forensic Re-Audit
## Original Product Mission & Evolutionary Foundation

**Document:** `phase_0_original_objective.md`  
**Classification:** Forensic System Re-Analysis  
**Target:** RISK // INDIA Disaster Risk Intelligence  
**Authoritative Workspace:** `C:\Users\HP\Desktop\Risk Analyser`  

---

### 1. Foundational Mission & The Problem RISK // INDIA Was Created to Solve

RISK // INDIA was conceived as an intelligent, evidence-based disaster risk intelligence platform for India. Its original charter was formulated around an acute operational problem:
> **During disasters in India, information is fragmented across disparate bureaucratic silos (IMD bulletins, CWC hydrographs, NDMA advisories, local news, and social channels). Citizens either receive uncalibrated panic warnings or delayed alerts after floodwaters or storms have already caused catastrophic damage.**

The platform was intended to solve this problem by providing:
1. **Unified, honest public disaster intelligence**: Synthesizing environmental, geographical, and historical signals into actionable situational awareness.
2. **Citizen-centric answers to fundamental survival questions**:
   - *What is happening right now?*
   - *What could happen next?*
   - *How serious is the situation?*
   - *Where is the risk?*
   - *Why is the risk changing?*
   - *When could conditions worsen?*
   - *What should I do now?*
   - *What should I prepare?*
   - *What should I do before, during, and after?*
   - *Where can I get verified help?*
   - *When should I check again?*
3. **Strict scientific integrity**: Preventing deceptive pseudo-probabilities (e.g. "87% chance" when no calibrated model supports it), banning synthetic data fabrication, and respecting physical predictability limits (e.g. acknowledging that earthquakes cannot be forecasted deterministically).

---

### 2. Dual User Archetypes

The original vision explicitly bifurcated users into two operational personas:
1. **User Archetype A — Preparedness Citizen (Peacetime / Early Advisory)**:
   - Needs regional baseline risk understanding.
   - Needs seasonal preparedness guidance (72-hour family grab-bag, home proofing).
   - Needs multi-day forecast awareness (1–3 days and 3–7 days) to plan travel, agriculture, and livestock safety.
2. **User Archetype B — Crisis Citizen (Impending / Active Hazard)**:
   - Needs immediate life-safety answers in seconds on mobile devices.
   - Needs high-contrast, distraction-free emergency actions ("Do this now").
   - Needs authoritative evacuation notices separated clearly from routine preparation.
   - Needs direct speed-dial access to verified emergency response helplines (112, NDMA 1078, NDRF, SDMA).

---

### 3. The Core Conceptual Hierarchy

To prevent confusion between physical observations, models, and statutory alerts, the platform was founded on five distinct conceptual layers:

| Layer | Question Answered | Authority & Source | Key Citizen Presentation |
| :--- | :--- | :--- | :--- |
| **1. CURRENT RISK** | *What is observed right now?* | Live ground telemetry (IMD, CWC, USGS) | Real-time hazard state, water levels, temperatures |
| **2. FUTURE RISK** | *What could happen next?* | NWP models & multi-source evidence fusion | 5-horizon trajectory (NOW to 7 days), directional trend |
| **3. REGIONAL BASELINE** | *What is the long-term vulnerability?* | BIS IS 1893:2016, CWC basin monographs | Inherent seismic, flood, and terrain susceptibility |
| **4. OFFICIAL WARNING** | *What has government formally warned?* | IMD, CWC, NDMA statutory alerts | RED, ORANGE, YELLOW color-coded administrative directives |
| **5. EMPIRICAL ML** | *What does the machine learning model predict?* | Frozen Assam prototype (`assam_flood_prototype_v1`) | Statistically validated flood inference in Assam ONLY |

---

### 4. Initial Forensic Audit Finding

While the backend successfully grew from an offline Assam prototype into an advanced 36-entity multi-hazard predictive fusion engine across 30 phases, **the public-facing website experienced a growing product-level divergence**. 

Key technical modules—specifically multi-horizon future risk forecasting, transparent uncertainty expansion, and 12-question citizen safety answers—remained largely hidden behind REST APIs or buried in nested map tabs. Meanwhile, the homepage continued displaying older demo mock objects (`isDemoData: true`, `isSimulated: true`, `confidenceScore: 92`) in the "Analyze Your Area" section.

Phase 2 Website Betterment addresses this exact root cause: restoring the original product mission and making future risk a prominent, discoverable, first-class citizen experience.
