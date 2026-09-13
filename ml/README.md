# RISK // INDIA — Machine Learning Architecture & Multi-Hazard Roadmap

This directory contains the machine learning intelligence foundation for **RISK // INDIA: AI-Powered Disaster Risk Analyzer & Management System**.

---

## 1. Architectural Principles

1. **Defensible Science over Fake Intelligence**:
   - Zero fabricated models, random weights, or invented accuracy scores.
   - Transparent system states (`AVAILABLE`, `MODEL_PENDING`, `MODEL_NOT_AVAILABLE`).
2. **Decoupled Training & Inference**:
   - Training is an offline, asynchronous batch engineering pipeline (`train.py`).
   - Inference is a lightweight, stateless runtime service (`predict.py`) consumed by the FastAPI backend.
3. **Imbalance-Aware Formulation**:
   - Predict calibrated binary occurrence probabilities $P(\text{Disaster} = 1 \mid X)$.
   - Transform probabilities into standardized risk scores ($0–100$) and standardized risk tiers (LOW, MODERATE, HIGH, CRITICAL).
4. **Data Leakage & Generalization Safeguards**:
   - Strict chronological temporal validation (no future leakage).
   - Group-based spatial cross-validation (testing out-of-basin transferability).

---

## 2. Directory Layout

```
ml/
├── __init__.py
├── README.md                      # Architecture guide & multi-hazard roadmap
├── common/                        # Shared ML utilities across all hazards
│   ├── __init__.py
│   ├── metrics.py                 # Imbalance metrics (PR-AUC, ROC-AUC, Brier score, FPR/FNR)
│   ├── validation.py              # Tabular quality validation suite (bounds, gaps, coords)
│   └── utils.py                   # Central probability-to-risk mapping functions
├── flood/                         # Flood Risk ML Pipeline
│   ├── __init__.py
│   ├── README.md                  # Comprehensive scientific documentation
│   ├── config.py                  # Thresholds, paths, feature lists, temporal splits
│   ├── schema.py                  # Pydantic schemas (Core, Optional, Future, Output contract)
│   ├── features.py                # Feature extraction & engineering
│   ├── preprocessing.py           # Scikit-learn Pipeline & ColumnTransformer
│   ├── evaluate.py                # Candidate model benchmarking & spatial cross-validation
│   ├── train.py                   # Offline training runner (clean stop on absent dataset)
│   ├── predict.py                 # Runtime inference service (handles MODEL_PENDING)
│   └── artifacts/                 # Serialized pipelines & metadata (empty until trained)
│       └── .gitkeep
└── datasets/                      # Telemetry specifications & templates
    ├── README.md                  # Data specification & Indian provenance guide
    └── sample_flood_template.csv  # Verified CSV template with header documentation
```

---

## 3. Standardized Output Contract

All hazard models implement the standardized output contract defined in `ml/flood/schema.py`:

```json
{
  "location_id": "assam",
  "disaster_type": "FLOOD",
  "probability": 0.3849,
  "risk_score": 38,
  "risk_level": "MODERATE",
  "model_version": "heuristic-provisional-v1",
  "status": "MODEL_PENDING",
  "timestamp": "2026-09-12T08:14:28Z",
  "factors": [
    {
      "factor_name": "Antecedent Precipitation Influx",
      "factor_value": "310.0 mm (72h cumulative)",
      "impact": "INCREASES_RISK",
      "importance_rank": 1,
      "contribution_weight": 0.38,
      "unit": "mm"
    }
  ],
  "primary_driver": "Antecedent Precipitation Influx",
  "recommended_action": "Heighten routine hydrometric monitoring...",
  "disclaimer": "PROVISIONAL ASSESSMENT -- MODEL INTEGRATION PENDING. NOT A TRAINED ML INFERENCE."
}
```

---

## 4. Multi-Hazard Extensibility Roadmap

The ML architecture is designed so additional disaster hazard models can be plugged in without modifying the core system contracts:

| Disaster Hazard | Target Variable Formulation | Primary Meteorological / Physical Drivers | Planned Module |
| :--- | :--- | :--- | :--- |
| **Flood** *(Implemented)* | Binary flood occurrence in 24/48/72h | Antecedent rainfall, elevation, slope, river stage, soil saturation | `ml/flood/` |
| **Cyclone** *(Upcoming)* | Track landfall probability & wind speed class | Central pressure deficit, sea surface temperature (SST), vertical wind shear | `ml/cyclone/` |
| **Landslide** *(Upcoming)* | Slope failure occurrence probability | Rainfall intensity-duration, slope gradient, lithology, deforestation | `ml/landslide/` |
| **Heatwave** *(Upcoming)* | Temperature anomaly duration exceedance | Maximum daily temperature, humidity index, dry wind advection | `ml/heatwave/` |
| **Drought** *(Upcoming)* | Standardized Precipitation-Evapotranspiration Index (SPEI) | Precipitation deficit, potential evapotranspiration, vegetation health index | `ml/drought/` |

Each new hazard model will follow the identical structure (`config.py`, `schema.py`, `preprocessing.py`, `evaluate.py`, `train.py`, `predict.py`), re-using `ml/common/` for data validation, metric computation, and risk level mapping.
