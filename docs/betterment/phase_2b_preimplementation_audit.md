# RISK // INDIA — Phase 2B Pre-Implementation Audit & Forensic Architectural Check

**Authoritative Workspace**: `C:\Users\HP\Desktop\Risk Analyser`  
**Date**: 2026-09-21  
**Baseline**: Phase 30A–30G Complete | Phase 2 Forensic Re-Analysis Complete | Phase 2A Citizen Website Hardening Complete  

---

## 1. Executive Forensic Assessment

Prior to modifying any frontend code for Phase 2B, an exhaustive forensic pre-check was conducted across all backend routes, service abstractions, data stores, types, and UI components.

### Core Finding:
The backend architecture already possesses world-class predictive risk fusion, multi-horizon weather forecasting, early-warning classification, scenario modeling, and life-safety protocols across all 36 States and Union Territories. However, the homepage UX currently features several standalone cards and requires citizens to click through tabs or navigate to secondary pages to discover critical future risk intelligence.

Phase 2B bridges this divide by turning **Future Risk into the primary homepage product**, establishing the **Future Risk Command Center**, the **5-Horizon Timeline**, the **6-Hazard Matrix**, the **Why Risk May Increase Drivers**, the **Action Engine**, and a dedicated **Future Risk Detail Page**.

---

## 2. Existing Backend Routes Inventory

Every necessary data endpoint is already implemented, verified, and operational:

| Category | Endpoint | Method | Response / Purpose |
|---|---|---|---|
| **Predictive Risk** | `/api/predictive-risk/national` | GET | `NationalPredictiveOverview` covering all 36 States/UTs |
| | `/api/predictive-risk/trends` | GET | Directional momentum (`RISING`, `STABLE`, `DECLINING`, `VOLATILE`) |
| | `/api/predictive-risk/readiness` | GET | Actionable early warning & evacuation readiness posture |
| | `/api/predictive-risk/providers` | GET | Scientific upstream catalog (IMD, CWC, NDMA, USGS, NRSC, GSI) |
| | `/api/predictive-risk/{region}/timeline` | GET | 5 forecast horizons (`NOW`, `0-6h`, `6-24h`, `1-3d`, `3-7d`) |
| | `/api/predictive-risk/{region}/explanation` | GET | Transparent explanation & answers to 12 citizen safety questions |
| | `/api/predictive-risk/{region}/scenarios` | GET | Forward scenarios (`BASELINE`, `LIKELY`, `ESCALATION`) |
| | `/api/predictive-risk/{region}/early-warning` | GET | Progressive early warning posture decoupling preparation from evacuation |
| | `/api/predictive-risk/{region}/{hazard}` | GET | Complete fused predictive risk assessment for region + hazard |
| | `/api/predictive-risk/{region}` | GET | Assessment for dominant baseline hazard in region |
| **Crisis Mode** | `/api/crisis/status` | GET | Real-time crisis recommendations and activation triggers |
| | `/api/crisis/overview` | GET | National crisis response overview |
| | `/api/crisis/assessment/{region_id}` | GET | Detailed crisis assessment with life-safety actions |
| | `/api/crisis/checklist` | GET | 72-hour family disaster kit checklist across 8 categories |
| | `/api/crisis/helplines` | GET | 24/7 verified statutory emergency contact directory |
| **Weather & Forecasting**| `/api/weather/national` | GET | Meteorological overview across 36 entities |
| | `/api/weather/{region_id}` | GET | Station observations and numerical weather prediction |
| | `/api/weather/{region_id}/forecast` | GET | Multi-horizon forecast timeline |
| | `/api/weather/warnings` | GET | Active official meteorological bulletins (RED, ORANGE, YELLOW) |
| **Telemetry & Ingestion**| `/api/telemetry/status` | GET | Hydrological sensor telemetry ingestion status |
| | `/api/telemetry/gauges` | GET | Canonical CWC gauge stations catalog |
| | `/api/telemetry/observations` | GET | Real-time river stage, discharge, and rainfall observations |

---

## 3. Existing Frontend Service & Type Layer

### Typed API Clients:
1. `src/services/predictiveRiskService.ts`: Complete client for all `/api/predictive-risk/*` endpoints.
2. `src/services/crisisService.ts`: Complete client for `/api/crisis/*` endpoints.
3. `src/services/weatherService.ts`: Complete client for `/api/weather/*` endpoints.
4. `src/services/disasterService.ts`: Active incident feeds.

### Canonical Type Definitions:
1. `src/types/predictiveRisk.ts`:
   - `RiskState`: `NORMAL`, `WATCH`, `ELEVATED`, `HIGH`, `CRITICAL`
   - `TrendState`: `RISING`, `STABLE`, `DECLINING`, `VOLATILE`
   - `ConfidenceLevel`: `LOW`, `MODERATE`, `HIGH`
   - `UncertaintyLevel`: `LOW`, `MODERATE`, `HIGH`, `VERY_HIGH`
   - `EarlyWarningStatus`: `NO_ACTIVE_SIGNAL`, `WATCH`, `PREPARE`, `GET_READY`, `EVACUATION_READINESS`, `EMERGENCY`
   - `PredictiveTimelinePoint`, `PredictiveScenario`, `PredictionExplanation`, `PredictiveRiskAssessment`, `NationalPredictiveOverview`
2. `src/types/crisis.ts`:
   - `CrisisAction`, `DisasterKitItem`, `EmergencyHelpline`, `CrisisAssessment`
3. `src/types/location.ts`:
   - `IndiaLocation` with all 36 States/UTs, coordinates, and districts.

---

## 4. Existing UI Components & Current Gaps

| Component | Current State | Phase 2B Action |
|---|---|---|
| `HeroSection.tsx` | Has "Open Risk Map", "Check Future Risk", "Check Risk for My Location", 6-card intelligence strip | **Modify**: Add secondary CTA "See Early Warnings"; refine copy to maintain high urgency and clear hierarchy. |
| `FutureRiskHeroSection.tsx` | Basic interactive timeline card | **Replace / Upgrade**: Supersede with `FutureRiskCommandCenter.tsx` featuring the 10 core elements (A–J) and plain-language phrasing. |
| `LocationRiskCheckerSection.tsx`| 4-tier cascade (India $\rightarrow$ State $\rightarrow$ District $\rightarrow$ City), 11-point matrix | **Modify**: Elevate future risk results so they are prominent immediately without tab clicks; add "View Full Analysis" button linking to `FutureRiskPage.tsx`. |
| `EarlyWarningNoticeSection.tsx` | Actionable early warnings with DM Act 2005 demarcation | **Modify**: Add plain-language explanation of each warning status tier and what would trigger escalation. |
| `FutureHazardCardsSection.tsx` | 6 hazard cards with sample regions | **Replace / Upgrade**: Create `FutureHazardMatrix.tsx` with explicit earthquake non-prediction disclaimer, structural guidance, and evidence source attribution. |
| `CitizenActionSection.tsx` | Tabs for now/before/during/after + 72h checklist | **Decompose**: Split into `FutureRiskActionPanel.tsx` (top 3-5 prioritized life-safety actions, hazard-specific) and dedicated `PreparednessSection.tsx` (72h family kit across 8 categories). |
| `HowItWorksSection.tsx` | 4-step pipeline + 6 plain-language questions | **Preserve / Enhance**: Maintain transparent explainability. |
| `FreshnessBadge.tsx` | 9 states supported | **Preserve**: Standardized usage across all cards. |
| `FutureRiskPage.tsx` | Does not exist | **Create**: Comprehensive 20-element Future Risk detail page (`src/components/pages/FutureRiskPage.tsx`). |
| `FutureRiskDrivers.tsx` | Does not exist | **Create**: Plain-language causal evidence drivers with official source provenance (`src/components/home/FutureRiskDrivers.tsx`). |
| `FutureRiskTimeline.tsx` | Exists in `predictive/` as raw component | **Create / Upgrade**: Citizen-facing `FutureRiskTimeline.tsx` in `components/home/` with qualitative states and expanding uncertainty. |

---

## 5. Navigation & Routing Architecture

### Current Navigation:
- `Navbar.tsx` defines `NavigationPage`: `'home' | 'risk-map' | 'disasters' | 'get-help' | 'help-others' | 'how-it-works'`.
- `App.tsx` routes between these pages with URL query parameter support (`?page=...`).

### Phase 2B Upgrade:
- Add `'future-risk'` to `NavigationPage`.
- Update `Navbar.tsx` to expose:
  1. `Home`
  2. `Future Risk` (routes to `FutureRiskPage` or `#future-risk`)
  3. `Early Warnings` (scrolls to `#early-warnings`)
  4. `Open Risk Map` (routes to `RiskMapPage`)
  5. `Live Disasters` (routes to `DisastersPage`)
  6. `Get Help / SOS` (routes to `GetHelpPage` / opens Emergency Hub)
- Connect in `App.tsx`:
  - `currentPage === 'future-risk'` renders `<FutureRiskPage onNavigate={handleNavigate} />`.

---

## 6. Scientific & Operational Guard Invariants

1. **Model Immutability**:
   - `ml/flood/artifacts/model.joblib`: SHA-256 `0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf`
   - `datasets/processed/flood_assam/flood_features.csv`: SHA-256 `88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080`
2. **Zero-Synthetic Data Guarantee**:
   - Every endpoint must return `synthetic_records == 0`.
   - Never fabricate numeric chances ("87% chance of flood" strictly prohibited).
3. **ML Scope Restriction**:
   - Machine learning is certified and active **strictly for Assam Flood**.
   - All other 35 entities enforce `ml_available = False` and `guard_status = PASS_NON_ASSAM_GUARD`.
4. **Earthquake Non-Prediction Guard**:
   - Earthquakes must never be presented as forward forecasts.
   - Mandated output: `trend = STABLE`, `confidence = LOW`, `uncertainty = VERY_HIGH`, explicit non-prediction disclosure.
5. **Statutory Demarcation**:
   - Forecast preparation guidance $\ne$ statutory civil evacuation orders.
   - Evacuation orders are issued legally only by District Magistrates, SDMAs, and NDMA under the **Disaster Management Act, 2005**.
6. **National Coverage vs Live Telemetry Honesty**:
   - Administrative coverage is 36/36 States & UTs.
   - Live sensor availability is reported accurately without claiming all-India live sensor coverage where gaps exist.

---

## 7. Risks of Regression & Mitigation Strategy

1. **TypeScript Build Regressions**:
   - Strict typing across new components using types from `src/types/predictiveRisk.ts`.
   - Continuous verification using `npm run build` (`tsc && vite build`).
2. **Test Suite Integrity**:
   - Maintain all 544 currently passing tests.
   - Build a comprehensive `tests/test_phase2b_future_risk_website.py` suite covering all 30 validation criteria from Part 24.
3. **Cognitive Load & UI Bloat**:
   - Avoid duplicating content across sections.
   - Use progressive disclosure (high-level citizen plain-language takeaway upfront, technical metrics in expandable accordions/sub-labels).
4. **Mobile Responsiveness**:
   - Minimum 44x44px touch targets.
   - Zero horizontal scroll (`overflow-x-hidden`).
   - Text wrapped and readable on 360px width viewports.

---

## 8. Pre-Implementation Audit Verdict

**AUDIT COMPLETE & APPROVED FOR IMPLEMENTATION.**  
All required backend routes, data services, and types are verified and intact. The architecture is ready for the Phase 2B citizen-first website betterment pass.
