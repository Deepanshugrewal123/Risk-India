# RISK // INDIA — PHASE 30F: NATIONAL PREDICTIVE RISK FUSION, EARLY-WARNING INTELLIGENCE & FUTURE-HAZARD ASSESSMENT

**Document Version:** 1.0.0  
**Status:** Certified & Verified  
**Date:** September 2026  
**System Classification:** Authoritative National Public Safety & Multi-Hazard Predictive Intelligence  

---

## 1. Executive Summary & Objective

Phase 30F establishes the authoritative **National Predictive Risk Fusion Engine** for RISK // INDIA. It transforms the platform from retrospective hazard logging into a predictive, multi-source, multi-hazard early warning intelligence system covering all 28 States and 8 Union Territories (36 entities total) across all 6 disaster hazards (`FLOOD`, `CYCLONE`, `HEATWAVE`, `SEVERE_WEATHER`, `LANDSLIDE`, `EARTHQUAKE`).

The primary purpose of Phase 30F is to answer the **12 foundational citizen safety questions**:
1. *What is happening right now?*
2. *What could happen next?*
3. *What is the future risk trend?*
4. *How serious could it become?*
5. *Why does the system think the risk may increase?*
6. *What evidence supports that assessment?*
7. *What should I do now?*
8. *What should I prepare before the disaster?*
9. *What should I do during the disaster?*
10. *What should I do after the disaster?*
11. *What data is missing or uncertain?*
12. *When should I check again?*

---

## 2. Absolute Scientific & Architectural Invariants

Phase 30F rigorously maintains all project safeguards without exception:

| Invariant | Authoritative Requirement | Verification Result |
| :--- | :--- | :--- |
| **Assam ML Model Artifact** | `ml/flood/artifacts/model.joblib`<br>SHA-256: `0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf` | **Verified byte-for-byte** |
| **Assam ML Features Dataset** | `datasets/processed/flood_assam/flood_features.csv`<br>SHA-256: `88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080` | **Verified byte-for-byte** |
| **Assam ML Model Scope** | Prototype model (`assam_flood_prototype_v1`) runs strictly for Assam Flood. | `ml_available = True` in Assam |
| **Non-Assam ML Guard** | For all 35 non-Assam entities, ML is strictly marked unavailable. | `ml_available = False`, `status = "NOT_AVAILABLE"` |
| **Earthquake Non-Prediction Guard** | Tectonic rupture timing cannot be predicted deterministically. Projections represent ambient lithospheric baselines (BIS IS 1893:2016) and observed USGS/NCS seismic catalog records. Future temporal forecasts are strictly disabled. | `trend = "STABLE"`, `confidence = "LOW"`, `uncertainty = "VERY_HIGH"` |
| **Zero Synthetic Data** | No synthetic, simulated, or fabricated telemetry records are generated under any circumstances. | `synthetic_records = 0` strictly everywhere |
| **Decoupled Prepare vs Evacuate** | Preparation advisories are never conflated with premature evacuation orders. | Evacuation is advised ONLY during `EVACUATION_READINESS` or `EMERGENCY` |
| **Qualitative Confidence** | Never output numeric pseudo-probabilities (e.g. "87% chance"). | Strictly `LOW`, `MODERATE`, or `HIGH` |
| **Uncertainty Expansion** | Uncertainty must monotonically expand with lead time and data gaps. | `NOW/0-6h <= 6-24h <= 1-3d <= 3-7d` |

---

## 3. National Coverage & Multi-Hazard Matrix

The system monitors **36 distinct administrative entities**:
- **28 States:** Andhra Pradesh, Arunachal Pradesh, Assam, Bihar, Chhattisgarh, Goa, Gujarat, Haryana, Himachal Pradesh, Jharkhand, Karnataka, Kerala, Madhya Pradesh, Maharashtra, Manipur, Meghalaya, Mizoram, Nagaland, Odisha, Punjab, Rajasthan, Sikkim, Tamil Nadu, Telangana, Tripura, Uttar Pradesh, Uttarakhand, West Bengal.
- **8 Union Territories:** Andaman and Nicobar Islands, Chandigarh, Dadra and Nagar Haveli and Daman and Diu, Delhi, Jammu and Kashmir, Ladakh, Lakshadweep, Puducherry.

### 6 Supported Disaster Hazards:
1. `FLOOD`: Multi-signal fusion of CWC catchment river gauges, IMD numerical precipitation forecasts, and basin soil baselines.
2. `CYCLONE`: IMD coastal storm tracks, maritime gale-force wind telemetry, and atmospheric pressure depressions.
3. `HEATWAVE`: Maximum surface temperature records, diurnal temperature cycles, and statutory IMD heat wave advisories.
4. `SEVERE_WEATHER`: Radar reflectivity, convective thunderstorm indicators, cloudburst signals, and lightning detection.
5. `LANDSLIDE`: GSI slope susceptibility ratings, antecedent precipitation saturation, and hilly terrain relief factors.
6. `EARTHQUAKE`: USGS/NCS seismic catalog observations, BIS IS 1893:2016 seismic zoning baselines, and tectonic fault line proximity.

---

## 4. 5 Standard Forecast Horizons

Predictive timelines are organized across 5 standardized forecast windows:
1. **`NOW` (Immediate Current Telemetry):** Ground station observations, current river water level ratios, and active alerts.
2. **`0-6h` (0 to 6 Hours - Nowcasting):** Rapid-update high-resolution convective projections and flash flood signals.
3. **`6-24h` (6 to 24 Hours - Short-Range):** Numerical weather prediction rainfall accumulation and diurnal temperature peaks.
4. **`1-3d` (1 to 3 Days - Medium-Range):** Synoptic system trajectory, depression tracking, and catchment inflow forecasts.
5. **`3-7d` (3 to 7 Days - Extended Outlook):** Medium-range atmospheric guidance and seasonal monsoon anomaly trends.

---

## 5. Qualitative Confidence & Uncertainty Engine

### Qualitative Confidence (`LOW`, `MODERATE`, `HIGH`):
- **`HIGH`:** Multi-source convergence (at least 4 corroborating signals across at least 3 distinct channels, including statutory official warnings, live telemetry, and NWP forecasts) with zero active source disagreements.
- **`MODERATE`:** At least 2 corroborating signals across at least 2 channels, or strong statutory alert with minor model latency.
- **`LOW`:** Limited sensor density, active source disagreement between models and telemetry, or non-predictable hazards (Earthquake).

### Qualitative Uncertainty (`LOW`, `MODERATE`, `HIGH`, `VERY_HIGH`):
- Monotonically expands with forecast lead time:
  - `NOW` / `0-6h`: `LOW` (with live data) or `MODERATE`
  - `6-24h`: `MODERATE`
  - `1-3d`: `HIGH`
  - `3-7d`: `VERY_HIGH`
- Stale data (`STALE` freshness) or sensor outages escalate uncertainty by one tier.
- Active signal disagreement escalates uncertainty to `HIGH` or `VERY_HIGH`.
- Earthquakes are permanently classified as `VERY_HIGH` uncertainty.

---

## 6. Directional Risk Trend Dynamics & Escalation

### Directional Trends:
- **`RISING`:** Forward projected risk score increases by $\ge 12.0$ points above current baseline.
- **`DECLINING`:** Projected risk score subsides by $\ge 12.0$ points below current elevated baseline.
- **`STABLE`:** Score fluctuations remain within $\pm 10.0$ points.
- **`VOLATILE`:** Alternating swings exceeding $\pm 15.0$ points across consecutive horizons.
- **`INSUFFICIENT_DATA`:** Insufficient empirical or forecast density. Never manufactured.

### Transparent Conflict Resolution:
When telemetry contradicts numerical forecasts (e.g. 75mm rain forecast while river gauge is calm):
- `has_conflicting_evidence = True`
- `conflicting_signals = ["Forecast models project heavy rainfall (>50mm), but river gauges currently report safe base-flow levels."]`
- `conflict_resolution_notes = "Hydrological Lag: Upstream runoff typically requires 6-18 hours to concentrate into river channels. Future risk is escalated to WATCH/ELEVATED while current telemetry remains bounded."`

---

## 7. Progressive Early Warning Decision Support

Strictly separates **Preparation Guidance** from **Evacuation Directives**:

| Status | Evacuation Advised? | Preparation Advised? | Primary Citizen Guidance |
| :--- | :---: | :---: | :--- |
| **`NO_ACTIVE_SIGNAL`** | No | No | Maintain standard baseline disaster supplies and situational awareness. |
| **`WATCH`** | No | Yes | Atmospheric conditions warrant routine monitoring; review household emergency battery kits. |
| **`PREPARE`** | No | Yes | Elevate electrical items, store 72h potable water and rations, check first aid kits. |
| **`GET_READY`** | No | Yes | Secure outdoor loose objects, assemble grab-and-go kits, avoid unnecessary travel. |
| **`EVACUATION_READINESS`** | **Yes** | Yes | Stand ready for orderly relocation; identify nearest designated public shelters. |
| **`EMERGENCY`** | **Yes** | Yes | Immediate sheltering or evacuation to pucca shelters; follow statutory routes. |

---

## 8. Forward Scenarios Engine

Each regional hazard evaluation constructs three transparent scenarios:
1. **`BASELINE` (Persistence):** Extrapolates current observations assuming weather patterns remain within current bounds.
2. **`LIKELY` (Expected Trajectory):** The most probable trajectory based on numerical weather prediction models and official advisories.
3. **`ESCALATION` (Severe Compounding):** Compounded worst-case conditions (e.g. stalled depression, cloudburst exceeding 20mm/hr, upstream reservoir releases, or high-tide convergence).

---

## 9. 12 Citizen Safety Questions

The engine directly and actionably answers all 12 foundational questions:
1. **What is happening right now?** Clear status of active ground conditions and current sensor readings.
2. **What could happen next?** Expected 24-72h trajectory and anticipated localized impacts.
3. **What is the future risk trend?** Directional momentum (`RISING`, `STABLE`, `DECLINING`) with confidence and uncertainty.
4. **How serious could it become?** Consequence benchmarks (minor disruption vs severe infrastructure damage).
5. **Why does the system think the risk may increase?** Physical drivers (e.g. heavy precipitation loading, river inflow rates).
6. **What evidence supports that assessment?** Authoritative evidence citations from IMD, CWC, NDMA, and USGS.
7. **What should I do now?** Immediate protective actions (charging phones, parking vehicles safely, staying indoors).
8. **What should I prepare before the disaster?** Pre-disaster checklist (72h water, medicine, emergency documents).
9. **What should I do during the disaster?** Survival actions during peak event (Turn Around Don't Drown, Drop Cover & Hold On).
10. **What should I do after the disaster?** Post-event recovery (boiling water, avoiding downed wires, checking on neighbors).
11. **What data is missing or uncertain?** Transparent disclosure of forecast horizon degradation and localized micro-climate gaps.
12. **When should I check again?** Explicit revisit timeframe (e.g. within 3-6 hours or next official IMD bulletin cycle).

---

## 10. REST API Specification

### Endpoints:
- `GET /api/predictive-risk/national`: National overview across all 36 entities, hazard counts, and crisis recommendations.
- `GET /api/predictive-risk/{region}`: Complete multi-signal predictive risk assessment for an entity.
- `GET /api/predictive-risk/{region}/{hazard}`: Complete assessment for a specific hazard in an entity.
- `GET /api/predictive-risk/{region}/timeline`: 5-horizon predictive timeline points.
- `GET /api/predictive-risk/{region}/explanation`: Transparent reasoning and all 12 citizen safety answers.
- `GET /api/predictive-risk/{region}/scenarios`: Baseline, Likely, and Escalation forward projections.
- `GET /api/predictive-risk/{region}/early-warning`: Decision support status and actionable guidance.
- `GET /api/predictive-risk/trends`: All 36 entities mapped to directional trends.
- `GET /api/predictive-risk/readiness`: Actionable entities in PREPARE, GET_READY, EVACUATION_READINESS, or EMERGENCY.
- `GET /api/predictive-risk/providers`: Status and catalog of authoritative upstream scientific providers (IMD, CWC, NDMA, USGS, NRSC, GSI).

---

## 11. Frontend Component Suite

Implemented in `src/components/predictive/`:
1. `NationalFutureRisk.tsx`: Unified Phase 30F dashboard with national overview cards, crisis recommendations, 36 entity search, and deep-dive analytics.
2. `RiskForecastTimeline.tsx`: Interactive 5-horizon slider and card inspector.
3. `HazardForecastCard.tsx`: Multi-hazard comparison selector across all 6 disaster types.
4. `EarlyWarningPanel.tsx`: Visual alert status separating preparation from evacuation.
5. `ScenarioPanel.tsx`: Interactive tabs for Baseline, Likely, and Escalation scenarios.
6. `EvidenceConvergencePanel.tsx`: Evidence signals list, provider attribution, and transparent conflict resolution.
7. `RiskExplanationCard.tsx`: Accordion for all 12 citizen safety questions and technical factor cards.
8. `RiskTrendIndicator.tsx`: Directional trend icon and styling.
9. `UncertaintyBadge.tsx`: Qualitative confidence and lead-time uncertainty pills.
10. `PredictionScopeNotice.tsx`: Scientific governance notice for Assam ML model and Earthquake non-prediction guard.

Integrated into `RiskMapPage.tsx` with a toggle allowing instant switching between **Current Risk Map** and **Future Risk & Early Warning (Phase 30F)**.

---

## 12. Verification & Test Results Certification

- **Phase 30F Dedicated Test Suite:** `tests/test_phase30f_predictive_risk_fusion.py` (36 tests passed, 0 failures, 0 errors).
- **Full Repository Regression:** 506 total tests passed, 0 failures, 0 errors.
- **Frontend Production Build:** Vite v5.4.21 built in 5.07s with zero TypeScript compilation errors.
- **Hash Invariants:** `model.joblib` and `flood_features.csv` confirmed identical byte-for-byte.
