# RISK // INDIA — Phase History Forensic Audit
## Chronological Progression, Technical Milestones & Evolutionary Drift

**Document:** `phase_history_audit.md`  
**Classification:** Forensic System Re-Analysis  
**Authoritative Workspace:** `C:\Users\HP\Desktop\Risk Analyser`  

---

### 1. Chronological Phase Audit Table (Phases 1 to 30F)

| Phase Sequence | Primary Objectives | Key Technical Deliverables | Product Impact & Identified Gaps |
| :--- | :--- | :--- | :--- |
| **Phases 1–8** | Assam Flood ML Prototype | `ml/flood/artifacts/model.joblib` (Random Forest Classifier), `flood_features.csv`, GroupKFold cross-validation, 13 canonical features. | Solid offline machine learning foundation established for the Brahmaputra corridor. Byte-for-byte SHA-256 frozen. |
| **Phases 9–13** | ML Serving & Initial Product Pilot | FastAPI model serving, initial React dashboard, verified help contact directory, basic incident feed. | Connected frontend to ML inference; however, frontend relied on small demo mock payloads for areas outside Assam. |
| **Phases 14–17** | Production Architecture & Reliability Hardening | Circuit breakers for upstream providers, dual-mode SQLite/PostgreSQL storage, sliding-window rate limiting, security headers, Alembic migrations. | Massive production stability upgrade; backend hardened against thundering herds and malicious inputs. |
| **Phases 18A–19** | National Multi-Basin & Multi-Hazard Expansion | Canonical CWC gauge registries (Godavari, Mahanadi, Brahmaputra), normalized disaster schemas, 6-hazard baseline engine across all 28 States + 8 UTs. | System expanded nationwide for baseline risk, but ML was strictly gated (`ml_available = False`) outside Assam. |
| **Phases 20–24** | Containerization, Public UX & Staging Resilience | Docker Compose topology (Postgres 16 + Redis 7), global Crisis Mode context, Emergency Access Hub, offline-ready speed dial, staging health probes. | Provided offline resilience and container topologies; UI established emergency high-contrast modes. |
| **Phases 25–29** | Empirical Data Acquisition & Release Candidate RC1 | 14-gate model promotion framework, deterministic event corroboration, orthogonal freshness taxonomy (`OFFICIAL_LIVE`, `STALE`, etc.), 322 automated tests. | Enforced zero synthetic data guarantee across empirical storage; rigorous telemetry audit trail. |
| **Phase 30A** | Future Risk Forecasting Architecture | Conceptual separation of 6 risk modes; 5 temporal horizons (`NOW`, `0_6H`, `6_24H`, `1_3D`, `3_7D`); Before/During/After protocols; Earthquake non-prediction guard. | Established the 12 citizen question architecture and hazard predictability limits. |
| **Phase 30B** | National Weather & Environmental Future Risk | Multi-hazard future risk sub-engines; normalized environmental telemetry; qualitative confidence (`LOW`, `MODERATE`, `HIGH`) and uncertainty. | Transformed multi-agency forecasts into forward risk indices; backend-heavy milestone. |
| **Phase 30C** | Dynamic Catchment Telemetry Stream | Real-time CWC hydrological sensor ingestion; 13 machine-readable quality gates; SI unit normalization; hierarchical basin-to-state mapping. | Live hydrological sensor streams operational; provided live river danger ratio evidence. |
| **Phase 30D** | National Weather Intelligence & Forecast Ingestion | Multi-horizon NWP timeline ingestion; IMD official warning color coding (RED, ORANGE, YELLOW); provider circuit breakers; 40 dedicated tests. | Live synoptic weather and official IMD warnings active across all 36 entities. |
| **Phase 30E** | National Crisis Mode & Emergency Response | Rules A–E deterministic activation; 3–5 prioritized immediate actions; 72h family checklist; proximity-based verified resource engine; 32 dedicated tests. | Active crisis assistance engine and high-contrast dashboard deployed. |
| **Phase 30F** | National Predictive Risk Fusion Engine | Unified multi-source evidence fusion; directional risk trends (`RISING`, `STABLE`, etc.); forward scenarios (`BASELINE`, `LIKELY`, `ESCALATION`); 12 citizen safety answers. | Created full predictive risk backend & components; **GAP: Future risk was nested under RiskMapPage rather than exposed as the centerpiece on HomePage.** |

---

### 2. Diagnosis of Evolutionary Drift

1. **The "Backend-First" Skew**: As the backend matured with high-frequency telemetry, rigorous 14-gate promotion engines, SI conversions, and multi-source evidence fusion, the frontend lagged in translating these capabilities to the citizen.
2. **The "Analyze Area" Demo Relic**: While `predictive_service.py` was generating multi-signal assessments, `AnalyzeAreaSection.tsx` on the homepage was still using a static fallback object containing `isDemoData: true`, `isSimulated: true`, and a fake `confidenceScore: 92`.
3. **Hidden Discoverability**: In Phase 30F, rich predictive components (`NationalFutureRisk`, `RiskForecastTimeline`, `HazardForecastCard`, `ScenarioPanel`, `RiskExplanationCard`) were created, but they were placed behind an alternate button in `RiskMapPage.tsx`. A visitor landing on the homepage had no clear way to immediately see: *"What could happen next?"*
4. **The Remedy**: Website Betterment Phase 2 places Future Risk, Early Warning, and Action Intelligence directly on the homepage, location-first and mobile-optimized.
