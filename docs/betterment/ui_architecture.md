# UI ARCHITECTURE & DATA FLOW
## Component Hierarchy, Service Layer & Scientific Invariant Enforcement

**Document Version**: 2.0.0  
**Status**: APPROVED  
**Date**: September 2026  
**Scope**: Frontend Architecture (React 18 + TypeScript + Vite + Tailwind CSS)  

---

### 1. System Topology & Component Hierarchy

The citizen-facing application follows a unidirectional data flow and strict modular hierarchy:

```
App.tsx
 ├── CrisisProvider (Global State: isCrisisMode, highContrast, networkQuality)
 │    ├── Navbar (Desktop/Mobile Nav, SOS Trigger, Crisis Toggle, Deep Links)
 │    ├── OfflineIndicator (Offline Detection, Emergency Access Hub trigger)
 │    ├── CrisisRecommendedBanner (Auto-recommends Crisis Mode if active severe alerts)
 │    │
 │    ├── [Main Content Router]
 │    │    │
 │    │    ├── HomePage.tsx (Default View)
 │    │    │    ├── HeroSection (Declare CURRENT + FUTURE + EARLY WARNING + ACTION)
 │    │    │    ├── FutureRiskHeroSection (5 Horizons, Qualitative Trend & Evidence)
 │    │    │    ├── LocationRiskCheckerSection (Cascade Selector, Live Telemetry)
 │    │    │    ├── EarlyWarningNoticeSection (Official Bulletins, Prepare vs Evacuate)
 │    │    │    ├── FutureHazardCardsSection (6 Multi-Hazard Predictive Cards)
 │    │    │    ├── CitizenActionSection (Do Now, Prepare Before, During, After, 72h Kit)
 │    │    │    ├── LiveRiskSnapshot (Geospatial Matrix preview, "Open Risk Map")
 │    │    │    ├── CurrentDisastersSection (Active official incident feed)
 │    │    │    ├── ReliefHubSection (Help Requests & Volunteer matching)
 │    │    │    ├── VerifiedHelpSection (Government Helplines & NGO resources)
 │    │    │    ├── HowItWorksSection (Methodology & Scientific Transparency)
 │    │    │    └── FinalCTASection (Direct path to Location Checker & Risk Map)
 │    │    │
 │    │    ├── RiskMapPage.tsx (Interactive Map, Vector Layers, Multi-Horizon Overlays)
 │    │    ├── DisastersPage.tsx (National Disaster Inventory)
 │    │    ├── GetHelpPage.tsx (Emergency Resource Dispatch)
 │    │    ├── HelpOthersPage.tsx (Community Volunteer Deployment)
 │    │    └── HowItWorksPage.tsx (Full Scientific Documentation)
 │    │
 │    ├── Footer (Institutional provenance, data sources, disclaimers)
 │    ├── DisasterDetailModal (Contextual incident deep-dive)
 │    └── EmergencyAccessHub (Offline-cached speed dial & survival guides)
```

---

### 2. Service Layer Integration

Frontend components do not make ad-hoc fetch requests. All telemetry and predictive risk data pass through strictly typed service singletons:

```
+-------------------------------------------------------------+
|                     FastAPI Backend                         |
|  /api/predictive/national-overview                          |
|  /api/predictive/assessment?region_id=...&hazard=...        |
|  /api/predictive/readiness                                  |
|  /api/disasters                                             |
+------------------------------+------------------------------+
                               | (JSON over HTTP/REST)
                               v
+-------------------------------------------------------------+
|                 Frontend Service Layer                      |
|  src/services/predictiveRiskService.ts                      |
|  src/services/disasterService.ts                            |
|  src/services/preparednessService.ts                        |
+------------------------------+------------------------------+
                               | (Strongly-typed TS Interfaces)
                               v
+-------------------------------------------------------------+
|                 UI Components & Hooks                       |
|  FutureRiskHeroSection, LocationRiskCheckerSection,         |
|  EarlyWarningNoticeSection, FutureHazardCardsSection        |
+-------------------------------------------------------------+
```

#### Key API Methods
- `predictiveRiskService.getNationalOverview()`: Retrieves national hazard counts, dominant risk drivers, and system-wide synthetic record verification (`synthetic_records === 0`).
- `predictiveRiskService.getAssessment(regionId, hazard)`: Retrieves the 5-horizon timeline points (`NOW`, `0-6h`, `6-24h`, `1-3d`, `3-7d`), driving factors, evidence sources, and qualitative confidence/uncertainty.
- `predictiveRiskService.getReadiness()`: Fetches actionable official early warnings and readiness notices across all 36 States and Union Territories.

---

### 3. Scientific Safeguard Enforcements in UI

The UI architecture implements programmatic guards to prevent misleading claims:

#### A. Non-Assam ML Guard
```tsx
// LocationRiskCheckerSection.tsx & FutureHazardCardsSection.tsx
if (regionId.toLowerCase() !== 'assam') {
  // ml_available is guaranteed FALSE
  // UI renders: "Empirical ML flood model is strictly localized to Assam Brahmaputra monitoring gauges."
  // Displays baseline index derived from IMD/CWC climatological telemetry.
}
```

#### B. Earthquake Non-Prediction Guard
```tsx
// FutureHazardCardsSection.tsx & predictiveRiskService.ts
if (hazard === 'EARTHQUAKE') {
  // is_predictable: false
  // trend: "STABLE"
  // confidence: "LOW"
  // uncertainty: "VERY_HIGH"
  // UI renders: "Earthquake occurrence cannot be forecast in advance. Protocols emphasize structural preparedness and Drop, Cover, Hold On response."
}
```

#### C. Zero Synthetic Data Validation
```tsx
// Evaluated on every service response
if (response.synthetic_records !== 0) {
  console.warn("Scientific Integrity Alert: Non-zero synthetic records detected.");
}
```

#### D. Monotonic Uncertainty Validator
The UI component verifies that for any horizon sequence, uncertainty steps non-decreasingly:
$$\text{Level}(t_1) \le \text{Level}(t_2) \quad \text{for } t_1 < t_2$$

---

### 4. Offline Resilience & Low-Bandwidth Optimizations

1. **Emergency Access Hub (`EmergencyAccessHub.tsx`)**:
   - Stores emergency phone numbers (`112`, `1078`, `1070`, `1077`, `1091`) in local application bundle.
   - Operates 100% offline without backend API connectivity.
   - One-tap `tel:` protocol links launch device phone dialer directly.

2. **Crisis Mode Rendering**:
   - `CrisisDashboard.tsx` replaces complex DOM trees with high-contrast, linear, zero-canvas markup.
   - Network polling intervals drop to zero; all user actions prioritize battery and cellular preservation.

3. **SVG & CSS Optimization**:
   - National map preview uses vector SVG path geometries with pure CSS fills rather than raster tiles, reducing payload from megabytes to under 45 kB.
