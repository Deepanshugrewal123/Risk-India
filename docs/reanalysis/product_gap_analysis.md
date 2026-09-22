# RISK // INDIA — Product Gap Analysis
## Critical Analysis of Future-Risk Discoverability, Citizen Usability & UX Roadblocks

**Document:** `product_gap_analysis.md`  
**Classification:** Forensic System Re-Analysis  
**Authoritative Workspace:** `C:\Users\HP\Desktop\Risk Analyser`  

---

### 1. The Core Product Problem

The fundamental gap identified in the user's directive is:
> **The backend contains future-risk / predictive-risk infrastructure, but the citizen-facing website does not make FUTURE RISK clearly visible, discoverable, understandable, and actionable.**

This section breaks down the specific reasons why this occurred and how each is systematically resolved.

---

### 2. Forensic Gap Breakdown

#### Gap 1: Future Risk Was Buried in an Alternate Sub-Tab
- **Current Reality**: Future risk capabilities were implemented as a nested view mode (`viewMode === 'future'`) inside `RiskMapPage.tsx`.
- **User Experience Failure**: A citizen arriving at the homepage sees "Explore Risk Map" or "Analyze My Area". If they do not visit the Map page and notice the small mode button, **they never discover that RISK // INDIA has multi-horizon forecast capabilities**.
- **Correction**: Future Risk ("WHAT COULD HAPPEN NEXT?") must be a **first-class hero section on the homepage itself**, complemented by primary navigation links.

#### Gap 2: Simulated Mocks & Fake Probabilities in "Analyze Your Area"
- **Current Reality**: `AnalyzeAreaSection.tsx` had an initial state containing:
  ```ts
  isDemoData: true,
  isSimulated: true,
  confidenceScore: 92,
  modelVersion: 'v1.4.0-demo'
  ```
- **User Experience Failure**: This violated the zero-synthetic data guarantee and presented a numeric pseudo-probability ("92% confidence") that contradicted the scientific invariant of qualitative confidence (`LOW`, `MODERATE`, `HIGH`).
- **Correction**: Purge `isDemoData` and `isSimulated`. Rewrite `AnalyzeAreaSection` into a live **Location Risk Checker** powered directly by `predictiveRiskService.getRegionalAssessment()` and qualitative metrics.

#### Gap 3: Confusing Navigation & Button Nomenclature
- **Current Reality**: Various buttons said "Dedicated Risk Map", "Analyze My Area", or "Explore Risk Map".
- **User Experience Failure**: "Dedicated Risk Map" sounds like an internal developer view. The user doesn't know where to click.
- **Correction**: Standardize on **"Open Risk Map"** and clear descriptive labels:
  - "Check Risk for My Location"
  - "What Could Happen Next?"
  - "Early Warnings"
  - "What Should I Do?"

#### Gap 4: Conflation of Preparation vs Evacuation
- **Current Reality**: In early UI iterations, alert badges did not clearly separate a precautionary watch from an urgent evacuation order.
- **User Experience Failure**: Either causes premature panic or complacency.
- **Correction**: Strictly decouple **Preparation Guidance** (e.g. charging batteries, storing 72h water, elevating goods) from **Evacuation Orders** (e.g. moving immediately to pucca flood/cyclone shelters). Evacuation guidance is rendered **ONLY** when statutory criteria or `EVACUATION_READINESS` / `EMERGENCY` status are active.

#### Gap 5: Absence of 6-Hazard Future Risk Cards on Homepage
- **Current Reality**: Citizens could not glance at the homepage and see how each hazard (`FLOOD`, `CYCLONE`, `HEATWAVE`, `SEVERE_WEATHER`, `LANDSLIDE`, `EARTHQUAKE`) was trending over the next 24 hours.
- **Correction**: Provide a clean, citizen-readable **6-Hazard Future Risk Grid** on the homepage showing Current State, Future State, Directional Trend, Expected Horizon, and Life-Safety Action.

#### Gap 6: Mobile Experience Density
- **Current Reality**: Technical dashboards with multi-column layouts were heavy on small smartphone screens.
- **Correction**: Prioritize mobile-first vertical card stacking, clear touch targets ($\ge 44 \times 44$ px), high-contrast badges, and quick-tap emergency dial buttons.
