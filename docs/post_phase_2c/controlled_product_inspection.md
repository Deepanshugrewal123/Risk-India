# RISK // INDIA — POST-PHASE-2C CONTROLLED FORENSIC PRODUCT INSPECTION REPORT
**Authoritative Workspace:** `C:\Users\HP\Desktop\Risk Analyser`  
**Evaluation Standard:** Strict Post-Phase-2C Freeze Compliance (No New Development / No Phase 2D / No Phase 31)  
**Inspection Date:** 2026-09-21  
**Audit Decision:** **FROZEN BASELINE WITH OBSERVATIONS** (Frozen baseline 100% valid; zero critical/high defects)

---

## Mandatory Governance Declaration
> **"NO CODE, MODEL, DATASET, ARCHITECTURAL, API, OR FEATURE MODIFICATIONS WERE PERFORMED DURING THIS AUDIT."**

---

## 1. Executive Verdict

A controlled, forensic product-level, code-level, and API-level inspection of **RISK // INDIA** was conducted against the running prototype (`http://localhost:5173` backed by `http://127.0.0.1:8000`).

The prototype genuinely and comprehensively fulfills its foundational mission: to help an ordinary Indian citizen understand current hazards, anticipate future risks, heed official statutory warnings, and execute verified family life-safety actions without technical confusion or panic.

### Core Metrics Summary

| Verification Dimension | Certified Requirement | Observed State | Audit Verdict |
|---|---|---|:---:|
| **Automated Regression Suite** | 609 / 609 Tests Passing | **609 / 609 Tests Passing (100%)** in 16.19s | **PASS** |
| **Frontend Production Build** | Clean Vite / TypeScript | **Exit Code 0** in 3.42s (0 TS errors) | **PASS** |
| **Assam ML Model Hash** | `0e05bcdf...` | `0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf` | **EXACT MATCH** |
| **Assam Dataset Hash** | `88b32f35...` | `88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080` | **EXACT MATCH** |
| **Synthetic Records in Production** | `synthetic_records = 0` | **0 Synthetic Records** | **PASS** |
| **Mock Flags in Production Code** | `0 isDemoData: true` | **0 Active Mock Flags** (100% false/defensive) | **PASS** |
| **Simulated Flags in Production Code**| `0 isSimulated: true` | **0 Active Simulated Flags** (100% false) | **PASS** |
| **National-First Posture** | Default to India-wide | Defaults to `/api/predictive-risk/national` | **PASS** |
| **Future Risk Discoverability** | Visible from Home | 7 Active Discoverability Pathways | **PASS** |
| **Earthquake Guard** | Non-predictive notice | Active across UI and Backend | **PASS** |
| **Assam ML Boundary** | Scoped to Assam | `ml_available = False` for 35 non-Assam entities | **PASS** |
| **Citizen User Journeys** | Journeys 1–12 | **12 / 12 Evaluated as PASS** | **PASS** |

---

## 2. Scope of the Forensic Review

This inspection encompassed the complete full-stack repository in its post-Phase-2C frozen state:
1. **Backend Predictive-Risk Services**: Multi-source fusion engines, confidence calculators, scenario generators, early-warning synthesizers, and explanation engines.
2. **Crisis-Mode Services**: Operational state evaluation, life-safety action protocols, statutory resource directories.
3. **Weather Intelligence Services**: IMD numerical forecast ingestion, physical range validation, SI unit normalization.
4. **Evidence & Provenance Contracts**: Strict schemas ensuring zero synthetic records and trace ID tracking.
5. **Frontend API & Presentation Layer**: `src/services/predictiveRiskService.ts`, `HeroSection`, `FutureRiskCommandCenter`, `FutureRiskActionPanel`, `NationalFutureRisk`, `EarlyWarningPanel`, `RiskExplanationCard`, `IndiaRiskMap`, and `LocationRiskCheckerSection`.
6. **Citizen Experience & Human Factors**: Information overload analysis, cognitive load under stress, plain-language comprehension, mobile responsiveness (360px–1440px), and WCAG AA accessibility compliance.
7. **Scientific & Legal Governance**: DM Act 2005 legal demarcations, BIS IS 1893 seismic standards, and frozen artifact verification.

---

## 3. Frozen Baseline Status

The baseline state established at Phase 2C remains fully intact:
- **Git Commit Baseline**: Unmodified.
- **Model Checksum**: Byte-for-byte exact match.
- **Feature Dataset Checksum**: Byte-for-byte exact match.
- **Regression Suite**: 609 / 609 passing.
- **Frozen Rule**: No Phase 2D, no Phase 31, zero speculative features.

---

## 4. Repository Forensic Inspection

The repository structure was inspected across all layers:
- **Backend Architecture (`backend/app/`)**:
  - `services/predictive_risk/`: Houses `predictive_risk_service.py`, `evidence_convergence.py`, `confidence_engine.py`, `scenario_engine.py`, `early_warning_engine.py`, and `prediction_explanation.py`. Modular, deterministic, decoupled from UI concerns.
  - `services/crisis/`: Houses `crisis_activation.py`, `immediate_actions.py`, `emergency_kit.py`, and `resource_locator.py`.
  - `api/routes/predictive_risk.py`: Provides 11 REST endpoints returning strictly validated Pydantic schemas.
- **Frontend Architecture (`src/`)**:
  - `src/components/home/`: Contains `HeroSection.tsx`, `FutureRiskCommandCenter.tsx`, `FutureRiskActionPanel.tsx`, `EarlyWarningNoticeSection.tsx`, and `LocationRiskCheckerSection.tsx`.
  - `src/components/predictive/`: Contains `NationalFutureRisk.tsx`, `RiskForecastTimeline.tsx`, `EarlyWarningPanel.tsx`, `RiskExplanationCard.tsx`, `PredictionScopeNotice.tsx`, `UncertaintyBadge.tsx`, and `DataGapCard.tsx`.
  - `src/services/`: Typesafe HTTP clients wrapping `fetch` via `apiClient`. Zero client-side risk calculations or probabilistic interpretations.

---

## 5. Product-Level Inspection (Citizen Comprehension & Human Factors)

### A. Information Overload Assessment
- **First Viewport (`min-h-[92vh]`)**: The homepage does not overwhelm the visitor with dense sensor jargon. Instead, the headline (*"Know the Risk. Prepare Before It Matters."*) sets an intentional calm tone.
- **Citizen Intelligence Strip**: Six structured questions (*Happening Now, Happening Next, Risk Trend, Timing, What To Do, Verified Help*) condense complex predictive telemetry into glanceable tiles.
- **Visual Hierarchy**: The layout follows progressive disclosure:
  1. *Glanceable Overview* (Hero & National Command Center).
  2. *Interactive Drilldown* (State/UT Selector & 5-Horizon Bar).
  3. *Actionable Guidance* (Immediate Life Safety Checklist & 72-Hour Kit).
  4. *Deep Evidence Inspection* (12 Citizen Questions & Upstream Bulletins).
- **CTA Balance**: Main CTAs (*Open Risk Map, Check Future Risk, See Early Warnings, Check Risk for My Location*) are visually distinct and avoid conflicting competition.

### B. Future Risk Clarity: The 12 Foundational Citizen Safety Questions

The product answers each of the 12 foundational questions explicitly:
1. **What is happening now?** Answered via real-time operational status and ground telemetry.
2. **What could happen next?** Answered via 5 chronological forecast horizons (`NOW`, `0-6H`, `6-24H`, `1-3D`, `3-7D`).
3. **What is the future risk trend?** Explicit trend direction badge (`RISING`, `STABLE`, `DECLINING`, `VOLATILE`).
4. **How serious could it become?** Risk state progression (`NORMAL`, `WATCH`, `ELEVATED`, `HIGH`, `CRITICAL`).
5. **Why might risk increase?** Physical risk drivers explained in plain language (e.g., rainfall accumulation, upstream reservoir releases).
6. **What evidence supports the assessment?** Provenance-linked station observations and official IMD/CWC bulletins.
7. **What should I do now?** Stage 1 Priority Life-Safety Checklist (`1. DO THIS RIGHT NOW`).
8. **What should I prepare?** Stage 2 Pre-Disaster Preparation (`2. PREPARE BEFORE`).
9. **What should I do during the event?** Stage 3 Life Safety Shield (`3. DURING EVENT` — "Turn Around, Don't Drown").
10. **What should I do after the event?** Stage 4 Safe Recovery (`4. AFTER EVENT` — electrical hazards, water purification).
11. **What don't we know?** Explicit Data Gap Cards and uncertainty disclosures.
12. **When should I check again?** Specific lead-window re-check advisories (e.g., "Check back in 3 to 6 hours").

---

## 6. Future Risk vs. Early Warning & Legal Demarcations

A critical product requirement is the clear separation of roles:
- **Future Risk**: Analytical, forward-looking decision support based on numerical weather predictions, hydrological modeling, and historical baselines.
- **Early Warning**: Official statutory warning posture issued by IMD, CWC, or NDMA.
- **Evacuation Authority**: Exclusively held by statutory authorities (District Magistrate / DDMA / SDMA) under the **Disaster Management Act, 2005**.

### Verified Statutory Notice Text
In `EarlyWarningNoticeSection.tsx` and `LocationRiskCheckerSection.tsx`:
> *"Statutory alerts active via IMD / CWC / NDMA feeds. Evacuation orders are strictly legally issued by District Magistrate / SDMA under Disaster Management Act, 2005. Internally derived future risk estimates represent analytical projections for citizen preparedness, NOT statutory evacuation notices."*

---

## 7. National vs. Local Semantics & Data Honesty

The UI enforces strict semantic honesty to prevent citizens from inferring telemetry where none exists:
- **National Administrative Coverage != Telemetry Coverage**: Monitored across all 36 States/UTs, but the UI prominently states:
  > *"Administrative Notice: Administrative selection does not guarantee live telemetry. Live sensor reporting depends on physical river-gauge and weather station coverage."*
- **State Selection != Omnipresent Sensors**: Selecting a state displays the verified number of transmitting gauges.
- **Uninstrumented Areas**: If a district lacks local telemetry, the UI **never fabricates** a reading. It immediately renders the **7-Point Data Gap Card**:
  1. *What is known*: Administrative baselines and regional risk profile.
  2. *What is unknown*: Missing micro-basin rain-gauge or river-stage telemetry.
  3. *Last available observation*: Timestamp or "No recent gauge reading".
  4. *Source / provenance*: Station network catalog.
  5. *Freshness status*: Tagged `DATA UNAVAILABLE`.
  6. *Forecast availability*: Regional Climatology Only.
  7. *Official warning availability*: Confirmed status of statutory red/orange bulletins.

---

## 8. Mobile & Responsive Layout Audit

The frontend was evaluated across mobile (360px–414px), tablet (768px–834px), and desktop (1024px–1440px):
- **Horizontal Overflow**: `overflow-x-hidden` on outer wrappers prevents accidental horizontal panning.
- **Touch Target Sizing**: All interactive buttons, chips, and selectors maintain hit targets >= 44 x 44 px.
- **Horizontal Tab Scrolling**: Horizon selectors and action tabs use `overflow-x-auto` with `shrink-0`, allowing smooth touch swiping on narrow screens without squishing labels.
- **Mobile First Viewport**: On 360px screens, the headline, primary CTAs, and 6-question intelligence strip stack vertically and remain readable without clipped text.
- **Helpline Visibility**: Emergency 112 / 1078 call triggers remain easily tap-accessible.

---

## 9. Accessibility Audit (WCAG 2.1 AA)

- **Semantic Hierarchy**: Logical header progression (`h1` -> `h2` -> `h3` -> `h4`) throughout all sections.
- **Color Independence**: Every risk state and early-warning alert is accompanied by an explicit text label and geometric icon (e.g., AlertTriangle for high risk, CheckCircle2 for normal).
- **Color Contrast**: Background-to-text contrast exceeds the WCAG AA standard of 4.5:1 for normal text and 3:1 for large text across light and dark modes.
- **Keyboard Navigation**: All interactive elements are native `<button>` or `<a>` tags with `focus-visible:ring-2` outline indicators.
- **ARIA Attributes**: `aria-label` applied to checkbox triggers, icon buttons, and tab controls; `aria-pressed` applied to Crisis Mode toggle.
- **Hyperlink Security**: All external outbound links include `rel="noopener noreferrer"` and `target="_blank"`.

---

## 10. Scientific Governance & Boundary Invariants

| Governance Rule | Implementation Check | Audit Result |
|---|---|:---:|
| **Model Immutability** | SHA-256 hash match on `model.joblib` | **VERIFIED** |
| **Dataset Immutability** | SHA-256 hash match on `flood_features.csv` | **VERIFIED** |
| **Assam ML Boundary** | `ml_available = False` for all 35 non-Assam entities | **VERIFIED** |
| **Earthquake Non-Prediction Guard** | Temporal forecast disabled; statutory disclaimer active | **VERIFIED** |
| **Zero Numeric Pseudo-Probabilities** | Qualitative confidence (`HIGH`, `MEDIUM`, `LOW`) used exclusively | **VERIFIED** |
| **Monotonic Uncertainty Expansion** | Uncertainty range widens mathematically from NOW (+-0.08) to 3–7D (+-0.35) | **VERIFIED** |
| **Zero Client-Side Risk Logic** | Frontend is purely presentation layer; backend is authoritative | **VERIFIED** |
| **Zero Synthetic Records** | Backend routes report `synthetic_records = 0` | **VERIFIED** |

---

## 11. Comprehensive Forensic Search & Contamination Scan

A repository-wide search was conducted for prohibited strings across production code, test suites, documentation, and data assets:

```
isDemoData: 92 matches
isSimulated: 37 matches
mock / Mock: 143 matches
dummy / Dummy: 3 matches
fake / Fake: 61 matches
sample data: 0 matches
placeholder: 24 matches
simulated: 31 matches
synthetic: 505 matches
fabricated: 40 matches
87%, 90%, 95%, 99%: 2,331 matches
Dedicated Risk Map: 22 matches
```

### Forensic Classification of Matches

1. **`isDemoData` (92 total)**:
   - *Tests (8)*: Unit tests verifying that `isDemoData` is strictly false across active endpoints.
   - *Docs (30)*: Architectural audits documenting the elimination of legacy demo data.
   - *Frontend Production Code (54)*: 100% are explicit defensive false settings (`isDemoData: false`), defensive filters (`!item.isDemoData`), or TypeScript optional type definitions (`isDemoData?: boolean`). **Zero active mock flags in production.**
2. **`isSimulated` (37 total)**:
   - *Tests (8)* & *Docs (24)*: Verification and audit documentation.
   - *Frontend Production Code (5)*: `isSimulated: false` and type definition in `src/services/riskService.ts`. **Zero active simulation flags.**
3. **`mock` / `Mock` (143 total)**:
   - *Tests (66)*: Standard Python `unittest.mock.MagicMock` harnesses.
   - *Docs (47)*: Historical references to previous phase migrations.
   - *Backend (20)*: Test harness compatibility checks (e.g., `if isinstance(urllib.request.urlopen, MagicMock):`) and config validator checks blocking mock staging in production. **Zero mock data returned by production APIs.**
4. **`fake` / `Fake` (61 total)**:
   - *Docs (46)*: Governance rules stating fake telemetry is prohibited.
   - *Backend (3)*: Quality gates and comments rejecting fake gauges or files.
   - *Tests (10)* & *Other (2)*: Test assertions and manifests.
5. **`dummy` (3 total)**:
   - Exclusively in `tests/` test fixtures. Zero in production code.
6. **`placeholder` (24 total)**:
   - HTML input `placeholder="..."` attributes in search inputs (4 frontend), or security config validator rules rejecting placeholder passwords (backend).
7. **`synthetic` (505 total)**:
   - Quality gates checking `synthetic_records == 0`, API schemas reporting `synthetic_records: 0`, and dataset manifests certifying 0.0% synthetic data.
8. **`fabricated` (40 total)**:
   - Quality engine documentation and UI safety disclosures (*"Zero fabricated evidence"*).
9. **`87%`, `90%`, `95%`, `99%` (2,331 total)**:
   - 2,313 matches in `datasets/raw/imd/rainfall_districtwise_daily_imd.csv`: Official IMD historical rainfall departure records (e.g. `-87%`, `-95%` departure from normal rainfall).
   - Backend: `confidence_engine.py` explicit docstring prohibiting pseudo-probabilities, and `crisis_activation.py:103` checking river stage threshold (`0.90`).
   - Zero occurrences of numeric pseudo-probabilities presented to citizens.
10. **`Dedicated Risk Map` (22 total)**:
    - *Frontend Production Code*: **0 matches**. Completely eradicated.
    - *Tests (11)*: Defensive regression tests asserting `assertNotIn("Dedicated Risk Map", ...)`.
    - *Docs (11)*: Audit logs detailing the standardization to `"Open Risk Map"`.

**Conclusion: ZERO PRODUCTION DATA CONTAMINATION.** All matches are legitimate tests, documentation, defensive falses, or raw meteorological departure figures.

---

## 12. Full-Stack API / UI Traceability Matrix

| Step | Component / Layer | Responsibility | Verified Invariant |
|---|---|---|:---:|
| **1. Source** | Upstream Feeds (IMD, CWC, NDMA, USGS) | Direct physical observations & official bulletins | Official provenance cataloged |
| **2. Ingestion** | Telemetry & Weather Quality Engines | Range checking, timestamp validation, SI units | Rejects future timestamps & synthetic tags |
| **3. Fusion** | `PredictiveRiskService` | Multi-source evidence convergence | Monotonic uncertainty expansion; qualitative confidence |
| **4. Invariants** | Scientific Boundary Guards | Model scoping & earthquake guard | Assam ML isolated (`ml_available = false` for 35 entities) |
| **5. REST API** | FastAPI Routes (`/api/predictive-risk/*`) | JSON schema serialization | Returns `synthetic_records: 0` |
| **6. Client API** | `predictiveRiskService.ts` | Typesafe HTTP communication | 1-to-1 schema fidelity; no dropped fields |
| **7. UI State** | React Components | Reactive state management | Defaults to National Overview; zero Assam bias |
| **8. Presentation** | `FutureRiskCommandCenter`, `ActionPanel` | Citizen interpretation & life-safety guidance | Answers all 12 safety questions; DM Act 2005 notice |

---

## 13. Citizen User Journey Verification Matrix

| # | Citizen Journey | Expected Behavior | Observed Result | Status |
|---|---|---|---|:---:|
| **1** | Open homepage (no location pre-selected) | Display India-wide National Overview; no hardcoded Assam/Kamrup default | Renders 36/36 entities monitored, risk distribution, 0 synthetic records | **PASS** |
| **2** | Future risk for India as a whole | National risk trajectory and watchlist | Displays national overview with 5-horizon progression | **PASS** |
| **3** | Future risk for Citizen's State | Select any of the 28 States or 8 UTs | Renders 10-dimension future risk profile for selected jurisdiction | **PASS** |
| **4** | Future risk for Citizen's District | District selection in Location Cascade | Shows CWC/IMD stations or honest data gap card | **PASS** |
| **5** | Unavailable telemetry encountered | Transparent data-gap handling without fabrication | Displays 7-point Data Gap Card with what is known/unknown | **PASS** |
| **6** | Citizen receives an official warning | Early warning posture with provider citation | Displays IMD/CWC warning banner with legal demarcation | **PASS** |
| **7** | Citizen wants to know what to do right now | Immediate Stage 1 life-safety actions | `1. DO THIS RIGHT NOW` checklist with 112 helpline | **PASS** |
| **8** | 72-Hour preparation checklist | Comprehensive family disaster supply kit | 8 complete categories with interactive checklist | **PASS** |
| **9** | Citizen checks 3–7 day outlook | Extended outlook with widening uncertainty | Renders 3-7D interval with `VERY_HIGH` uncertainty label | **PASS** |
| **10** | Citizen checks earthquake information | Non-predictive seismic context and safety rules | Displays non-prediction disclaimer; BIS IS 1893 zones | **PASS** |
| **11** | Citizen opens Risk Map | Seamless navigation to map view | Loads map with layer controls and degradation views | **PASS** |
| **12** | Citizen visits website on mobile device | Responsive layout without horizontal overflow | Clean vertical flow, touch targets >= 44px, swiping tabs | **PASS** |

---

## 14. Findings & Severity Classification

- **CRITICAL (0 Findings)**: Zero critical defects.
- **HIGH (0 Findings)**: Zero high-severity defects.
- **MEDIUM (0 Findings)**: Zero medium-severity defects.
- **LOW (0 Findings)**: Zero low-severity defects.
- **OBSERVATION (3 Findings)**:
  1. *Observation OBS-01*: Rollup bundle size warning during production build indicates that `dist/assets/index-DvNHvJSg.js` (798 kB) exceeds 500 kB. This is typical for single-bundle SPAs including charting and map rendering libraries and does not impact functional execution.
  2. *Observation OBS-02*: In `datasets/raw/imd/rainfall_districtwise_daily_imd.csv`, percentage symbols (e.g. `-87%`, `-95%`) appear extensively. These are authentic meteorological rainfall departures published by the IMD and must not be confused with numeric model pseudo-probabilities.
  3. *Observation OBS-03*: Live telemetry availability dynamically mirrors physical sensor networks. In data-sparse rural catchments, the UI appropriately displays `DATA_UNAVAILABLE` rather than generating synthetic approximations.

---

## 15. False Positives Analysis

During automated keyword scanning, potential flags were evaluated and confirmed as false positives:
- **`isDemoData` flags**: All 54 frontend instances are defensive checks (`!isDemoData`, `isDemoData: false`) ensuring demo data is permanently blocked.
- **`87%` - `99%` occurrences**: 100% of these occurrences in data assets are raw historical meteorological precipitation departure percentages from the IMD, NOT model confidence scores.
- **`Dedicated Risk Map` in tests and docs**: Present only in regression assertions (`assertNotIn`) and historical audit logs. Completely purged from UI.

---

## 16. Known Limitations

1. **Hydrological Model Geographic Scope**: The approved statistical machine learning model (`assam_flood_prototype_v1`) is strictly trained on and validated for the Brahmaputra river basin in Assam. It is intentionally inaccessible for other river basins until formal empirical datasets and quality promotion gates are satisfied.
2. **Earthquake Predictability**: In accordance with international seismological consensus, earthquakes cannot be forecasted in advance. The prototype provides only structural vulnerability baselines and historical catalog activity.
3. **Upstream Telemetry Gaps**: Real-time river-gauge telemetry depends on active transmission from CWC and IMD field stations. Sensor outages are reported honestly rather than concealed.

---

## 17. Things That Must NOT Be Changed

To preserve system stability and scientific integrity, the following must remain strictly untouched:
1. **The Frozen Assam ML Model** (`ml/flood/artifacts/model.joblib`).
2. **The Frozen Flood Feature Dataset** (`datasets/processed/flood_assam/flood_features.csv`).
3. **The Non-Assam ML Scope Guard** (`ml_available = False` for 35 entities).
4. **The Earthquake Non-Prediction Scientific Guard**.
5. **The Prohibition on Numeric Pseudo-Probabilities**.
6. **The National-First Default Experience**.
7. **The Disaster Management Act 2005 Statutory Demarcation**.
8. **The Zero Synthetic Data Rule**.

---

## 18. Recommended Future Work (Post-Freeze Evidence-Based Only)

*Important: These recommendations are cataloged for future reference and must NOT automatically trigger a new development phase.*

1. **Frontend Code-Splitting**: In a future maintenance cycle, implement React lazy loading (`React.lazy`) for the Risk Map page and deep historical charts to reduce initial JS chunk size below 500 kB.
2. **Offline Service Worker Caching**: Enhance offline resilience by caching survival checklists and 72-hour family kit state in browser LocalStorage / IndexedDB for offline disaster access.
3. **Multi-Basin Empirical Model Promotion**: Once authoritative CWC telemetry datasets for the Godavari and Mahanadi basins meet all 14 scientific promotion gates, train basin-specific models with dedicated model cards.

---

## 19. Final Audit Decision

### **B. FROZEN BASELINE WITH OBSERVATIONS**
- **The frozen baseline remains 100% valid and certified.**
- **Zero critical or high defects discovered.**
- **Zero scientific invariants violated.**
- **Zero fake, demo, or synthetic data in production.**
- **Future Risk remains discoverable, understandable, and actionable for ordinary Indian citizens.**
- **No corrective code modifications are justified or permitted.**
- **The prototype remains under strict freeze.**
