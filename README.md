# RISK // INDIA

> **National Multi-Hazard Predictive Risk Intelligence & Citizen Resilience Platform for India**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)]()
[![React](https://img.shields.io/badge/React-18.3-61DAFB.svg)]()
[![TypeScript](https://img.shields.io/badge/TypeScript-5.5-3178C6.svg)]()
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4-38B2AC.svg)]()
[![Release](https://img.shields.io/badge/release-POST__PHASE2C__FINAL-brightgreen.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

---

> [!IMPORTANT]
> **Certified Release Reference:** [`RISK_INDIA_2026_POST_PHASE2C_FINAL_RELEASE`](docs/release/release_manifest.md)  
> **Baseline Ancestry:** Commit `b10175a6abab8f82a3035fc99440ef4352a34efc` | **Governance:** Strict Project Freeze  
> For complete technical architecture, operations runbooks, and scientific governance, consult the **[Final Project Knowledge Pack](docs/release/final_project_knowledge_pack.md)** and **[Operator Handover Guide](docs/release/operator_handover.md)**.

---

## 📌 Overview

**RISK // INDIA** is a nationwide, multi-hazard disaster intelligence and public safety platform designed to transform complex hydrometeorological and seismic telemetry from official statutory agencies into clear, actionable, and life-saving decision support for Indian citizens.

The platform provides an immediate, plain-language answer to four foundational questions above the fold:
1. **Current Risk:** What is happening right now across India?
2. **Future Risk:** What could happen next across five standard forecast horizons (NOW, 0–6h, 6–24h, 1–3d, 3–7d)?
3. **Early Warning:** What official government advisories, bulletins, and weather color alerts are in effect?
4. **What Should I Do?:** What prioritized, evidence-based life-safety actions should I take immediately?

---

## 🌟 Core System Capabilities

- **National-First Experience:** Defaults to an India-wide multi-hazard overview across all 28 States and 8 Union Territories (36 administrative entities), eliminating regional bias.
- **Future Disaster Risk Forecasting:** Multi-horizon outlooks synthesizing meteorological models, hydrological routing, and empirical historical baselines across 5 forward windows: `NOW`, `0–6 HOURS`, `6–24 HOURS`, `1–3 DAYS`, and `3–7 DAYS`.
- **Six Supported Natural Hazards:**
  1. *Flood:* Riverine stage gauges, catchment runoff, and urban inundation.
  2. *Cyclone:* Coastal track monitoring, gale-force winds, and storm surge.
  3. *Heatwave:* Severe maximum temperature departures and persistence tracking.
  4. *Severe Weather:* Thunderstorms, lightning, cloudbursts, and squall events.
  5. *Landslide:* Rainfall-triggered slope susceptibility in vulnerable mountain terrains.
  6. *Earthquake:* Near real-time seismic event notification (post-event) and BIS tectonic hazard context.
- **Open Risk Map:** Interactive nationwide geospatial risk map supporting three-tier accessible degradation:
  1. *Interactive Map:* Full vector and tile canvas with administrative drill-downs.
  2. *Accessible Cards:* Responsive card deck for touchscreens and lower-bandwidth devices.
  3. *Semantic Text List:* High-contrast, screen-reader optimized plain-text view.
- **Directional Trend Momentum:** Transparent risk momentum classification (`RISING`, `STABLE`, `DECLINING`, `VOLATILE`).
- **Forward Analytical Scenarios:** Deterministic scenario modeling (Baseline, Likely, Escalation) explaining physical driving factors without sensationalism.
- **Emergency Resilience Hub:** Immediate single-tap access to national emergency helplines (`112`, NDMA `1078`, SEOC `1070`), 72-Hour Family Emergency Preparedness checklists, and codified Before / During / After hazard survival protocols.

---

## 🛡️ Scientific Safeguards & Operational Invariants

RISK // INDIA operates under twelve non-negotiable scientific invariants to ensure public trust and prevent misinformation:

1. **India-Wide Empirical Flood Model:** Automated flood risk inference is powered by RISK // INDIA Flood Model v1 (`risk_india_flood_v1`), trained on 18,216 empirical records across 38 States and Union Territories with zero synthetic observations.
2. **Ground-Truth Boundary Transparency:** Direct satellite flood inundation observations (ISRO Bhuvan SAR) are validated within the Assam corridor. Across other Indian river basins, positive training events are truthfully documented as empirical meteorological-hydrological surcharge proxies rather than simulated satellite pixels. The historical Assam prototype (`assam_flood_prototype_v1`) remains preserved as an immutable baseline.
3. **Earthquake Temporal Prediction Prohibited:** Under NO circumstances does the platform attempt to predict the timing, location, or magnitude of future earthquakes (`EARTHQUAKE_NOT_PREDICTABLE`). Only historical seismic zonation (BIS Zones II–V) and post-event USGS/NCS notifications are presented.
4. **No Numeric Pseudo-Probabilities:** The platform strictly rejects misleading percentage forecasts (e.g. "87% probability"). Risk confidence is classified qualitatively (`VERY_HIGH`, `HIGH`, `MEDIUM`, `LOW`, `VERY_LOW`).
5. **Monotonic Uncertainty Expansion:** Forecast uncertainty mathematically expands as lead time increases ($Uncertainty_{3-7D} > Uncertainty_{1-3D} > Uncertainty_{6-24H} > Uncertainty_{0-6H} > Uncertainty_{NOW}$).
6. **Statutory Evacuation Demarcation:** 
   > *"Under the Disaster Management Act 2005, mandatory evacuation orders and official relief operations are authorized exclusively by the National Disaster Management Authority (NDMA), State Disaster Management Authorities (SDMA / ASDMA), and District Magistrates (DDMA). RISK // INDIA provides informational situational intelligence and preparedness guidance only."*
7. **National Coverage vs. Telemetry Coverage:** Administrative mapping across all 36 States/UTs does NOT imply universal live physical sensor coverage.
8. **Explicit Data Gaps:** Unmonitored catchments or offline stations honestly report `DATA_UNAVAILABLE` or `LIMITED_EVIDENCE`. Zero spatial interpolation or fake readings are generated.
9. **Zero Synthetic Data Guarantee:** `synthetic_records == 0`. Production feeds strictly prohibit mock, simulated, or fabricated disaster records.
10. **Authoritative Backend Interpretation:** All risk classifications, scores, and life-safety actions are computed solely by backend engines; the frontend never invents independent risk metrics.
11. **Frontend Presentation Only:** The frontend acts as an accessible presentation layer with global error boundary resilience and offline detection.
12. **Cryptographic Release Immutability:** Pre-trained ML model artifacts and empirical datasets are frozen with permanent SHA-256 digests.

---

## 📊 Official Data Provenance

All telemetry and indicators originate strictly from authentic public government platforms:
- **India Meteorological Department (IMD):** Multi-day synoptic weather forecasts, rainfall departure matrices, cyclone bulletins, and heatwave alerts.
- **Central Water Commission (CWC):** River water level telemetry, warning levels, danger marks, and historical flood waves.
- **National Disaster Management Authority (NDMA):** Statutory alerts, safety guidelines, and national emergency contacts.
- **ISRO / NRSC Bhuvan:** Historical satellite flood inundation extents and geospatial datasets.
- **USGS & NCS:** Real-time seismic feed data and Indian tectonic epicentral records.
- **Geological Survey of India (GSI):** Baseline landslide susceptibility zonation.

---

## 🏗️ Architecture & Technology Stack

```
+-------------------------------------------------------------------------+
|                         CITIZEN BROWSER CLIENT                          |
|  React 18 + TypeScript + Vite + TailwindCSS + Lucide Icons + Leaflet    |
|  - 4 Core Life-Safety Question Cards & Immediate Guidance Strip         |
|  - 5-Horizon Future-Risk Forecast Timeline & 6-Hazard Risk Matrix       |
|  - Open Risk Map with 3-Tier Accessible Degradation (Map/Cards/List)    |
|  - Global React Error Boundary & Offline Connectivity Indicator         |
+-------------------------------------------------------------------------+
                                    |  HTTP REST / JSON (Port 8000)
                                    v
+-------------------------------------------------------------------------+
|                        BACKEND INFERENCE & API                          |
|  FastAPI + Uvicorn + Pydantic v2 + Scikit-Learn Runtime                |
|  - Upstream Provider Circuit Breakers (IMD, CWC, NDMA, USGS, NRSC)      |
|  - Scientific Guard Layer (Assam ML Boundary, Earthquake Non-Predict)  |
|  - Predictive Risk Fusion Engine (Multi-Source Convergence)             |
|  - Qualitative Confidence & Monotonic Uncertainty Expansion Engine      |
+-------------------------------------------------------------------------+
                                    |
          +-------------------------+-------------------------+
          |                                                   |
          v                                                   v
+-----------------------------------+       +-------------------+
|  EMPIRICAL SCIENTIFIC ML          |       | DATABASE / CACHE  |
|  - National Flood v1 (Active)     |       | Dual SQLite / PG  |
|  - Assam Prototype (Immutable)    |       | Redis / In-Memory |
+-----------------------------------+       +-------------------+
```

---

## 🚀 Installation & Quick Start

### Prerequisites
- **Python:** 3.10 to 3.14 (Verified: Python 3.14.7)
- **Node.js:** v18 to v24 (Verified: Node v24.21.0, npm 11.19.0)
- **Git**

### 1. Clone & Set Up Environment
```powershell
# Clone the repository
git clone https://github.com/Deepanshugrewal123/Risk-India.git
cd "Risk-India"

# Set up Python virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install Python backend dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies
npm install
```

### 2. Start Backend Service
```powershell
# Export PYTHONPATH
$env:PYTHONPATH = "backend;."

# Start FastAPI Uvicorn ASGI server on port 8000
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
- API Documentation: `http://127.0.0.1:8000/docs`
- Health Probe: `http://127.0.0.1:8000/api/health`

### 3. Start Frontend Client
```powershell
# Start Vite development server
npm run dev
```
- Web Application: `http://localhost:5173`

---

## 🧪 Verification & Testing

### Automated Regression Test Suite (658 Tests)
```powershell
$env:PYTHONPATH = "backend;."
python -m unittest discover tests
```
*Expected Result:* `Ran 658 tests in ~12-20s. OK (0 failures, 0 errors)`.

### Production Frontend Build
```powershell
npm run build
```
*Expected Result:* `tsc && vite build` completes with **0 TypeScript errors**.

---

## 🔒 Cryptographic Integrity & Release Manifest

| Artifact | File Path | Verified SHA-256 Digest | Status |
|---|---|---|:---:|
| **Historical Assam ML Model** | `ml/flood/artifacts/model.joblib` | `0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf` | **FROZEN** |
| **Historical Assam Dataset** | `datasets/processed/flood_assam/flood_features.csv` | `88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080` | **FROZEN** |
| **National Flood Model v1** | `ml/national_flood/artifacts/model.joblib` | `8ec5f4e0c4ec54a3ed5b97bfa10aba9e0717de5215ff0c10ebc525e26a5a1fd4` | **VERIFIED** |
| **National Feature Dataset** | `datasets/processed/national_flood/national_flood_features.csv` | `d731147cd961d725426ae9b9b5dd5838f6463fe915f03b46415fb60d8c55d1d0` | **VERIFIED** |

---

## ⚠️ Known Limitations & Non-Blocking Observations

1. **National Model Scope & Satellite Validation:** Automated empirical flood inference is operational nationwide via `risk_india_flood_v1` (18,216 validated empirical observations across 38 States/UTs). Direct radar satellite event validation (ISRO Bhuvan SAR) is concentrated in the Assam corridor, with official IMD precipitation and CWC river stage telemetry providing empirical surcharge ground truth across other basins.
2. **Earthquake Unpredictability:** Earthquakes cannot be forecast in advance; only post-event alerts and historical BIS tectonic risk zones are provided.
3. **Sparse Rural Sensors:** Certain rural catchments lack digital CWC river stage telemetry. These areas explicitly display `DATA_UNAVAILABLE` rather than unverified synthetic interpolations.
4. **Rainfall Departures:** Negative percentage values in IMD rainfall matrices (e.g., `-87%`, `-95%`) are physical precipitation departures from historical seasonal normals, NOT forecast probabilities.
5. **Frontend Bundle Size:** The production JavaScript bundle is ~1.2 MB due to integrated GIS geospatial coordinates and iconography libraries; this triggers a non-blocking informational Rollup warning (> 500 kB).

---

## 📚 Technical Documentation Index

- **[Final Project Knowledge Pack](docs/release/final_project_knowledge_pack.md)** — Complete 34-section operational and architectural handover manual.
- **[Operator Handover Guide](docs/release/operator_handover.md)** — Daily operations checklist, health probes, and incident recovery runbooks.
- **[Cryptographic Release Manifest](docs/release/release_manifest.md)** — System snapshot, runtime specifications, and quality gate metrics.
- **[Production Deployment Runbook](docs/DEPLOYMENT.md)** — 19-section container, reverse proxy, and staging deployment guide.
- **[Full Technical Documentation Index](docs/README.md)** — Complete index of all 27 canonical architectural, forensic, and scientific audit reports.

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
