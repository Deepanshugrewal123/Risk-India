# RISK // INDIA — Architecture Forensic Audit
## Full-Stack Architecture, Data Flows & Boundary Security

**Document:** `architecture_audit.md`  
**Classification:** Forensic System Re-Analysis  
**Authoritative Workspace:** `C:\Users\HP\Desktop\Risk Analyser`  

---

### 1. Architectural Topology Overview

RISK // INDIA is constructed as a decoupled, resilient web architecture:

```
[Public Citizen / Mobile Browser]
              │ (HTTPS / REST)
              ▼
[Frontend: Vite / React / TypeScript / Tailwind CSS]
   ├── Home / Landing (Needs First-Class Future Risk & Early Warning)
   ├── Location Risk Checker (State -> District -> City)
   ├── Predictive 5-Horizon Timelines (NOW, 0-6h, 6-24h, 1-3d, 3-7d)
   ├── Risk Map Page (Current vs Future vs Early Warning)
   └── Universal Emergency Access Hub & Helplines (112, NDMA 1078)
              │
              ▼ (JSON API / Axios / Rate-Limited Client)
[FastAPI Backend Application Layer]
   ├── API Routers (/predictive-risk, /crisis, /weather, /telemetry, /risk)
   ├── National Predictive Risk Fusion Service
   │     ├── Predictive Evidence Collector
   │     ├── Qualitative Confidence Engine (LOW, MODERATE, HIGH)
   │     ├── Predictive Uncertainty Engine (Expands with Lead Time)
   │     ├── Risk Trend Engine (RISING, STABLE, DECLINING, VOLATILE)
   │     ├── Multi-Hazard Forecast Engine (6 Hazards)
   │     ├── Risk Escalation & Downgrade Engine (Conflict Resolution)
   │     ├── Early Warning Engine (Decouples Prepare from Evacuate)
   │     ├── Scenario Engine (Baseline, Likely, Escalation)
   │     └── Prediction Explanation Engine (12 Citizen Questions)
   ├── Regional Baseline Risk Engine (28 States + 8 UTs)
   ├── National Weather Intelligence Service
   ├── Dynamic Catchment Telemetry Stream (CWC Gauges)
   └── Disaster Feed Manager (Multi-Provider Circuit Breakers)
              │
              ├── [ML Runtime: scikit-learn / joblib]
              │      └── Frozen Prototype: assam_flood_prototype_v1 (Assam Only)
              │
              ├── [Relational / Geospatial Storage]
              │      └── SQLite (Local/Dev) / PostgreSQL 16 (Staging/Prod)
              │
              └── [Upstream Official Providers (Isolated Circuits)]
                     ├── IMD (Weather, NWP Forecasts, Warnings)
                     ├── CWC (River Water Levels & Danger Marks)
                     ├── NDMA (National Early Warning Directives)
                     ├── USGS / NCS (Earthquake Epicenter Catalog)
                     ├── NRSC / ISRO (Satellite Inundation & Soil Moisture)
                     └── GSI (Landslide Susceptibility Baselines)
```

---

### 2. Forensic Review by Architectural Subsystem

#### A. Backend Micro-Services & API Layer
- **Status**: Exceptionally robust. Built with FastAPI, Pydantic v2 schemas, and dependency injection.
- **Strengths**: 
  - Strict circuit breakers preventing upstream cascade failures.
  - Orthogonal freshness tagging preserving source honesty.
  - Comprehensive REST endpoints covering national, regional, hazard-specific, timeline, scenario, and early warning queries.
- **Identified Deficiency**: Frontend was not calling newer Phase 30F endpoints from the homepage; instead, homepage relied on older `riskService` endpoints or hardcoded initial states.

#### B. Machine Learning Engine & Governance
- **Frozen Artifacts**:
  - `ml/flood/artifacts/model.joblib` (SHA-256: `0e05bcdf...`)
  - `datasets/processed/flood_assam/flood_features.csv` (SHA-256: `88b32f35...`)
- **Scope Restriction**: Strictly bounded to Assam Brahmaputra corridor.
- **Non-Assam Behavior**: `ml_available = False`, `status = "NOT_AVAILABLE"`. Fallback is deterministic evidence fusion.
- **Earthquake Boundary**: No temporal ML prediction exists or is allowed.

#### C. Data Storage & Telemetry Processing
- **Dual-Mode Engine**: SQLite for zero-dependency local dev; PostgreSQL with connection pooling for production.
- **Dynamic Telemetry Stream**: 13 data quality gates ensuring physical plausibility (no negative rainfall, coordinates within India bounding box, timestamps not in the future, zero synthetic data).

#### D. Security & Resilience Posture
- Sliding-window rate limiter preventing API abuse.
- Strict Content Security Policy and HTTP security headers.
- Safe structured logging redacting sensitive headers and query tokens.
- AST hyperlink hygiene ensuring all external resource links have `rel="noopener noreferrer"`.
