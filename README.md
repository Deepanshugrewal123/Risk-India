# RISK // INDIA

> **AI-Assisted Disaster Risk Intelligence & Community Resilience Platform for India**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)]()
[![React](https://img.shields.io/badge/React-18.3-61DAFB.svg)]()
[![TypeScript](https://img.shields.io/badge/TypeScript-5.5-3178C6.svg)]()
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4-38B2AC.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

---

## 📌 Overview

**RISK // INDIA** is a full-stack disaster risk intelligence and preparedness platform designed to synthesize environmental observations, geographical indicators, official telemetry, and verified relief registries into a single, cohesive interface.

The project combines:
1. **Multi-Hazard Risk Analysis**: Baseline assessments and explainability metrics across all 28 States and 9 Union Territories of India.
2. **ML Flood Prototype**: An empirical, audited machine learning model trained on real-world Central Water Commission (CWC) and ISRO/NRSC satellite observations for the Assam Brahmaputra river basin.
3. **Live Disaster Intelligence**: Operational seismic tracking integrated with the USGS Real-Time Earthquake feed and official meteorological alerts.
4. **Verified Relief & Assistance Directory**: Curated government emergency numbers, state disaster management authorities (SDMAs), verified relief camps, and official donation channels (CMRF / PMNRF).
5. **Community Preparedness**: Actionable survival checklists, evacuation guidelines, and first-aid kits tailored for floods, cyclones, earthquakes, and landslides.

> [!IMPORTANT]
> **PROTOTYPE SCOPE NOTICE**:
> The integrated Machine Learning flood model (ssam_flood_prototype_v1) is an **academic research prototype** strictly calibrated to 3 CWC hydrological monitoring stations in Assam. It is **NOT** a nationwide prediction system and must **NOT** be used as a replacement for official operational alerts issued by the India Meteorological Department (IMD) or Central Water Commission (CWC).

---

## 🌟 Core Features

- **AI Risk Analysis**: On-demand risk assessment evaluating cumulative rainfall (6h–168h), river gauge levels, and seasonal factors.
- **Explainable Predictions ("Why This Risk?")**: Transparent breakdown showing top contributing environmental signals and feature coefficients.
- **Geospatial Risk Map**: Interactive SVG-based map covering all 37 Indian States and Union Territories with categorized risk levels (Low, Moderate, High, Critical).
- **Live Disaster Feed**: Real-time seismic event tracking with magnitude, depth, timestamp, and epicentral distance filtering.
- **Get Help (Emergency Relief)**: Immediate single-tap access to national emergency helplines (112, NDRF, SDRF), district hospital directories, and active relief camps.
- **Help Others (Verified Donations & Volunteering)**: Direct links to official Chief Minister Relief Funds (Assam, Kerala, HP, Odisha) and vetted volunteer organizations.
- **Disaster Preparedness Hub**: Phase-specific safety guides (Before, During, and After) for major disaster vectors.
- **Responsive Mobile Experience**: Engineered with hardware-accelerated scroll reveal transitions and zero horizontal layout overflow across all viewports (320px–1440px+).

---

## 🏗️ System Architecture

The application adheres to a decoupled architecture separating real-time telemetry, offline-trained machine learning inference, and verified resource catalogs:

`
┌────────────────────────────────────────────────────────┐
│             React + TypeScript Frontend                │
│   (Vite, TailwindCSS, Framer Motion, Lucide Icons)     │
└───────────────────────────┬────────────────────────────┘
                            │ REST / JSON (HTTP)
                            ▼
┌────────────────────────────────────────────────────────┐
│                   FastAPI Backend                      │
│   (Uvicorn, Pydantic v2, SQLAlchemy, SQLite/Postgres)  │
├───────────────────────────┬────────────────────────────┤
│                           │                            │
│  ┌─────────────────────┐  │  ┌──────────────────────┐  │
│  │   Risk / ML Service │  │  │ Live Disaster Service│  │
│  │   (Flood Prototype) │  │  │ (USGS & Bulletins)   │  │
│  └──────────┬──────────┘  │  └──────────┬───────────┘  │
│             │             │             │              │
│  ┌──────────▼──────────┐  │  ┌──────────▼───────────┐  │
│  │ Scikit-Learn Model  │  │  │ External Feeds       │  │
│  │ assam_flood_v1      │  │  │ (USGS Seismic API)   │  │
│  └─────────────────────┘  │  └──────────────────────┘  │
│                           │                            │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Database Layer: Location, Assessment & Resources │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
`

### Architectural Separation
- **ML Inference vs. Live Feeds**: Predictive risk scoring is generated via local model evaluation of hydrological parameters. Live disaster monitoring runs independently through real-time external providers.
- **Offline Reliability**: The frontend provides a configurable offline mock fallback (VITE_USE_MOCK_DATA=true) to demonstrate full UI workflows even when disconnected from the backend.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React 18, TypeScript, Vite | Single-page application framework |
| **Styling & UI** | Tailwind CSS, Lucide React, Framer Motion | Editorial design system, responsive typography, micro-interactions |
| **Backend** | FastAPI, Uvicorn, Python 3.10+ | High-performance asynchronous REST API |
| **Data Validation** | Pydantic v2, Pydantic Settings | Strict schema definition and request/response typing |
| **Database** | SQLAlchemy 2.0, SQLite (local) / PostgreSQL (prod) | Relational storage for locations, risk records, and relief directory |
| **Machine Learning** | Scikit-Learn, NumPy, Pandas, Joblib | Tabular model serialization, preprocessing, and inference |
| **External Telemetry** | USGS Earthquake Hazards Program | Real-time global seismic feeds with India region bounding |

---

## 📊 Official Data Sources & Provenance

All model training features and risk indicators originate strictly from authentic public government platforms:

1. **Central Water Commission (CWC) / NWDP**:
   - Hourly river water level telemetry (Gauge: Nematighat, Fakirpara, Dhansirighat).
   - Hourly rainfall telemetry from basin automatic weather stations (2021–2025).
   - Source: [NWDP Open Data Portal](https://www.nwdp.nwic.gov.in/)
2. **India Meteorological Department (IMD)**:
   - District-wise daily observed rainfall matrices across monsoon seasons.
   - Source: [IMD / NWDP Open Data](https://www.nwdp.nwic.gov.in/en/dataset/rainfall-daily-imd)
3. **ISRO / NRSC Bhuvan Disaster Management Support**:
   - Georeferenced satellite flood inundation raster masks (RISAT-1A, Sentinel-1 SAR).
   - Source: [Bhuvan DMSP Flood Portal](https://bhuvan-app1.nrsc.gov.in/disaster/usrtasks/flood/flood.php)
4. **United States Geological Survey (USGS)**:
   - Real-time global seismic event feeds (M2.5+ earthquakes).
   - Source: [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)

---

## 🤖 Machine Learning Model Card

| Attribute | Details |
| :--- | :--- |
| **Model Identifier** | ssam_flood_prototype_v1 |
| **Model Type** | Regularized Logistic Regression (L2, =0.5$, balanced class weights) |
| **Serialized Artifact** | ml/flood/artifacts/model.joblib (975 bytes) |
| **Preprocessor Artifact**| ml/flood/artifacts/preprocessor.joblib (2.9 KB) |
| **Training Dataset** | 32 verified observations (18 Flood / 14 Non-Flood) |
| **Independence Groups** | 18 distinct hydrological events across 2021–2024 monsoons |
| **Validation Strategy** | 5-Fold GroupKFold partitioned strictly by event_group_id |
| **OOF Performance** | Accuracy: 50.0% \| Precision: 55.6% \| Recall: 55.6% \| ROC-AUC: 0.43 |
| **Input Features (13)** | Cumulative rain (6h, 24h, 72h, 168h), river level, 6h/24h rise, percentile, month, DOY sine/cosine, coordinates |
| **Temporal Leakage** | **Zero detected** (All predictors strictly precede observation timestamp) |

### Ethical & Scientific Honesty
Given the limited sample size (32 audited events across 3 gauge basins), the model's out-of-fold ROC-AUC is modest (~0.43), reflecting real-world validation difficulty on small hydrological event samples without synthetic data generation. The model is presented transparently as an educational and research prototype.

---

## 🚀 Getting Started

### Prerequisites
- **Node.js**: v18.0.0 or higher
- **Python**: v3.10 or higher
- **npm** or **yarn**

### 1. Repository Setup
`ash
git clone https://github.com/your-username/risk-india.git
cd risk-india
`

### 2. Frontend Setup
`ash
# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Run development server (runs on http://localhost:5173)
npm run dev
`

### 3. Backend Setup
`ash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Initialize database schema and seed baseline Indian location telemetry
python -m app.database.init_db

# Start FastAPI development server (runs on http://127.0.0.1:8000)
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
`

---

## 🧪 Testing & Verification

The repository contains automated unit, integration, and browser tests:

`ash
# Run full backend and ML test suite (55 tests)
python -m unittest discover tests

# Run frontend TypeScript type checking and production build
npm run build
`

---

## ⚠️ Limitations & Disclaimers

1. **Non-Operational Status**: RISK // INDIA is an academic prototype developed for college demonstration and research exploration. It does not replace official meteorological advisories.
2. **Geographical ML Scope**: Machine learning inference is strictly calibrated for Assam gauge basins. Locations outside Assam return baseline multi-hazard indicators without activating local gauge models.
3. **Emergency Situations**: In case of active emergencies, citizens must immediately dial **112** (National Emergency Helpline) or refer to the **NDMA / SDMA** portals.

---

## 🔮 Future Roadmap

- **Hydrological Basin Expansion**: Scaling the tabular ML pipeline across the Godavari, Krishna, Mahanadi, and Ganga river networks.
- **Deep Learning Vision Pipeline**: Incorporating SAR satellite imagery with automated inundation segmentation models (U-Net / SegNet).
- **Multi-Hazard Extensions**: Dedicated predictive models for coastal cyclone surges and Western Himalayan landslide susceptibility.
- **Native Mobile App**: Offline-first mobile distribution built with React Native for low-connectivity disaster zones.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.