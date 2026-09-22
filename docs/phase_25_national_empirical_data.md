# RISK // INDIA — PHASE 25
# NATIONAL EMPIRICAL DATA FOUNDATION & SCIENTIFIC ML EXPANSION
**Comprehensive Architecture, Scientific Governance & Audit Report**
**Date:** September 2026  
**Status:** COMPLETE & VERIFIED  

---

## 1. Executive Summary

Phase 25 of **RISK // INDIA** establishes a canonical, scientifically defensible national empirical data foundation for disaster risk intelligence across the Republic of India. Rather than proliferating uncalibrated or synthetic predictive models, this phase introduces an auditable, reproducible empirical pipeline, expands basin-level hydrometric monitoring across five core river basins, and establishes an authoritative 11-gate Model Promotion Gate that prevents any speculative machine learning model from reaching public production.

### Core Guarantees & Non-Negotiable Invariants Preserved
1. **100% Frozen Prototype Integrity:** `assam_flood_prototype_v1` remains byte-for-byte identical, utilizing strictly its 13 empirical features and 32 real observations. Zero retraining, zero reweighting, and zero synthetic augmentation.
2. **Strict Zero Synthetic Guarantee:** Across all datasets, manifests, and ingestion pipelines, `synthetic_records = 0` is strictly enforced. No synthetic, extrapolated, or hallucinated disaster events are generated.
3. **Absolute Scientific Honesty:** Non-Assam river basins and regions are strictly classified as `REGIONAL_BASELINE` and `EMPIRICAL_DATA_INSUFFICIENT`. ML predictions are served exclusively for the validated Assam prototype corridor.
4. **Zero UI Redesign:** Layouts, color palettes, visual hierarchies, and responsive interactions are preserved without regression.
5. **No Unauthorized Deployments:** Zero git commits, zero git pushes, and zero live external deployments performed.

---

## 2. Canonical Empirical Data Ingestion Pipeline & Schema

Implemented in `backend/app/services/empirical_data_pipeline.py`, the ingestion framework standardizes hydrometeorological, seismic, and geophysical observations into a canonical record format (`CanonicalEmpiricalRecord`).

### 2.1 Canonical Record Schema
Every incoming observation is normalized with strict field typing:
- `record_id`: Deterministic SHA256 hex string derived from `(source_agency, station_id, parameter, timestamp_utc)`.
- `source_agency`: Authoritative provenance provider (`CWC`, `IMD`, `GSI`, `NDMA`, `NCS`, `NRSC`).
- `station_id`: Unique identifier registered with the authoritative agency.
- `station_name`: Canonical name of the gauging/monitoring station.
- `basin_id`: River basin or seismic zone identifier.
- `state_ut`: Standardized Indian administrative entity name.
- `latitude` / `longitude`: High-precision WGS-84 coordinates.
- `timestamp_utc`: Standardized ISO 8601 UTC timestamp.
- `parameter`: Standardized measurement parameter (`water_level_m`, `discharge_cumec`, `rainfall_mm`, `magnitude_mw`, etc.).
- `value`: Raw observed scalar value.
- `unit`: SI or standard Indian meteorological unit.
- `quality_flag`: Audit status (`VALIDATED`, `SUSPECT`, `CALIBRATION_REQUIRED`, `QUARANTINED`).
- `synthetic_flag`: Guaranteed `False`.
- `provenance_url`: Official bulletin or portal URL documenting origin.

### 2.2 Physical Measurement & Coordinate Bounds
Physical validation bounds are strictly enforced to quarantine corrupted sensor readings or transcription errors:
- **India Coordinate Bounding Box:** Latitude [6.0°N, 38.0°N], Longitude [68.0°E, 98.0°E]. Any reading outside these coordinates is quarantined with reason `COORDINATES_OUT_OF_BOUNDS_INDIA`.
- **Rainfall:** [0.0, 2000.0 mm/day] (quarantining negative rainfall or values exceeding the Cherrapunji world record).
- **Water Level:** [0.0, 1500.0 m MSL].
- **Discharge:** [0.0, 120000.0 cumec].
- **Seismic Magnitude:** [0.0, 10.0 Mw].
- **Wind Speed:** [0.0, 350.0 km/h].
- **Ambient Temperature:** [-40.0°C, 60.0°C].

### 2.3 Deterministic Deduplication
Duplicate submissions of identical station readings are identified and suppressed via deterministic SHA256 hashing. The deduplication engine guarantees idempotency across continuous ETL cycles.

---

## 3. Five Prioritized River Basins & Readiness Assessment

In accordance with Phase 25 objectives, the platform expands hydrological gauge registries and assesses machine learning readiness across 5 major Indian river systems (`backend/app/services/ml_readiness_gate.py` and `basin_gauge_registry.py`):

| Priority Basin | Major River / Sub-Basins | Calibrated CWC Gauges | Empirical Observations | ML Readiness Status | Scientific State | Operational Strategy |
|:---|:---|:---:|:---:|:---:|:---|:---|
| **1. Brahmaputra** | Brahmaputra, Barak, Jiabharali | 3 | 32 | **READY (Prototype)** | `EMPIRICALLY_VALIDATED_ML` | Active ML Prototype Ingestion & Serving |
| **2. Ganga** | Ganga, Yamuna, Ghaghara, Gandak | 5 | 0 | **NOT READY** | `EMPIRICAL_DATA_INSUFFICIENT` | Regional Baseline + CWC Gauge Telemetry |
| **3. Godavari** | Godavari, Pranhita, Indravati | 5 | 0 | **NOT READY** | `EMPIRICAL_DATA_INSUFFICIENT` | Regional Baseline + CWC Gauge Telemetry |
| **4. Mahanadi** | Mahanadi, Seonath, Tel, Ib | 8 | 0 | **NOT READY** | `EMPIRICAL_DATA_INSUFFICIENT` | Regional Baseline + CWC Gauge Telemetry |
| **5. Krishna** | Krishna, Tungabhadra, Bhima | 5 | 0 | **NOT READY** | `EMPIRICAL_DATA_INSUFFICIENT` | Regional Baseline + CWC Gauge Telemetry |

### 3.1 Calibrated River Gauges
- **Brahmaputra:** Panbazar (Guwahati), Matijuri, NT Road Crossing.
- **Ganga:** Haridwar, Prayagraj, Varanasi, Patna, Farakka.
- **Godavari:** Bhadrachalam, Dowleswaram, Polavaram, Perur, Nanded.
- **Mahanadi:** Tikarpara, Naraj, Sambalpur, Baripada, Anandpur, Champua, Jamshedpur, Ghatsila.
- **Krishna:** Almatti Dam, Narayanpur, Srisailam, Nagarjuna Sagar, Vijayawada Prakasham Barrage.

---

## 4. Eleven-Gate Model Promotion Gate

The Model Promotion Gate (`backend/app/services/model_promotion_gate.py`) establishes an unyielding scientific validation barrier before any hazard predictive model can be promoted to public inference:

1. **Sufficient Empirical Observations:** Minimum audited empirical observation count (>= 100 for new regional models; >= 32 for audited Assam prototype).
2. **Temporal Separation (Zero Leakage):** Cross-validation must strictly enforce chronological partitioning (e.g. Leave-One-Event-Out or Purged Time-Series Split) without forward leakage.
3. **Spatial Validity:** All gauge and sensor coordinates must fall within the verified hydrological catchment.
4. **Class Balance:** Positive event ratio must remain between [15%, 85%] to prevent artificial synthetic imbalance or severe target distortion.
5. **Feature Completeness:** Missing feature ratio must not exceed 5% across the training dataset.
6. **Target Leakage Detection:** Upstream features must not incorporate downstream flood rasters or future proxy metrics.
7. **Provenance Completeness:** >= 90% of observations must trace directly to official government agencies (CWC, IMD, ISRO) with verifiable URLs.
8. **Reproducibility & Hash Integrity:** The model artifact must match the SHA256 checksum recorded in the official release manifest.
9. **Performance Metrics:** Rigorous thresholds must be satisfied across cross-validation folds:
   - Accuracy >= 0.80
   - F1-Score >= 0.75
   - ROC-AUC >= 0.80
10. **Probability Calibration:** Risk output probabilities must align with empirical event frequency (Brier score <= 0.20).
11. **Geographic Scope Boundary Enforcement:** Models must declare explicit, bounded geographic scopes. Any claim of nationwide or all-India flood ML without comprehensive all-basin empirical training is rejected immediately.

**Fallback Guarantee:** Any candidate model that fails even a single gate is flagged as `NOT_APPROVED`, and the system automatically enforces fallback to `REGIONAL_BASELINE + OFFICIAL_DISASTER_INTELLIGENCE`.

---

## 5. Dataset Manifests & Provenance Tracking

All dataset manifests registered in `backend/app/services/dataset_manifest.py` enforce `synthetic_records = 0` as an immutable attribute:
- `assam_flood_features_v1`: 32 empirical observations, 13 features, 100% frozen.
- `godavari_gauge_registry_v1`: 5 calibrated CWC stations, 0 synthetic records.
- `mahanadi_gauge_registry_v1`: 8 calibrated CWC stations, 0 synthetic records.
- `ganga_gauge_registry_v1`: 5 calibrated CWC stations, 0 synthetic records.
- `krishna_gauge_registry_v1`: 5 calibrated CWC stations, 0 synthetic records.
- `national_empirical_catalog_v1`: Multi-hazard canonical catalog spanning 28 States and 8 UTs, 0 synthetic records.

---

## 6. Extended API Contracts & REST Endpoints

### 6.1 Extended Risk API Schema
Responses from `/api/risk/point`, `/api/risk/analyze`, and `/api/risk/locations` now explicitly report:
- `risk_source`:
  - `EMPIRICAL_ML`: Served exclusively for locations within the audited Assam corridor.
  - `REGIONAL_BASELINE`: Served for all other Indian states and non-Assam basins.
  - `OFFICIAL_INTELLIGENCE`: Live warnings and telemetry from IMD, CWC, or NCS.
  - `CACHED_OFFICIAL_INTELLIGENCE`: Cached bulletin data when upstream providers are degraded.
- `scientific_state`:
  - `EMPIRICALLY_VALIDATED_ML`
  - `EMPIRICAL_DATA_INSUFFICIENT`
  - `BASELINE_ONLY`
  - `OFFICIAL_INTELLIGENCE_ONLY`
- `model_scope`: Explicit geographic boundary description.
- `dataset_version`: Reference version of the underlying empirical dataset.
- `data_freshness`: Telemetry latency and synchronization status.
- `confidence_provenance`: Methodology description of the confidence estimate.
- `limitations`: Plain-language operational caveats.

### 6.2 New Foundation REST Endpoints
- `GET /api/data/empirical/catalog`: Returns registered datasets, record counts, and zero-synthetic verification.
- `GET /api/data/empirical/schema`: Returns canonical observation field definitions, units, and physical bounds.
- `POST /api/data/empirical/ingest`: Ingests and validates batches of empirical observations with quarantine reporting.
- `GET /api/models/{model_id}/promotion-gate`: Evaluates a model against all 11 scientific validation gates.
- `GET /api/basins/readiness/priority`: Returns detailed empirical readiness evaluations for the 5 prioritized basins.

---

## 7. Frontend User Experience & Scientific Honesty

The frontend interface maintains scientific honesty through clear attribution banners:
- **Assam Corridor:** Displays `"Empirical ML Risk — Assam Prototype"` with explicit reference to the 13 empirical features and 32 historical flood events.
- **Non-Assam Regions:** Displays `"Regional Baseline — ML unavailable for this region"`, explaining:
  > *"ML prediction unavailable for this region. Regional baseline risk and official disaster intelligence are shown. Empirical data is insufficient for machine learning in this region."*
- **Explainability:** Fully preserves plain-language citizen glossaries for hydrological terms (Antecedent Rainfall, River Stage, HFL) while suppressing animations during active Crisis Mode.

---

## 8. Verification & Test Coverage Summary

- **Total Backend Tests:** 253 passing (0 failed, 0 errors, 0 regressions).
- **Phase 25 Dedicated Suite:** 15 passing tests (`test_phase25_national_empirical_data.py`).
- **Regression Suites:** Phase 18A (25 tests), Phase 18B (21 tests), Phase 21 (16 tests), Phase 24 (16 tests) all 100% passing.
- **Frontend Production Build:** Vite v5.4.21 TypeScript build succeeded in 3.04s with 0 errors.
- **Model Byte Hash:** Verified immutable at `a1b02fa1...` matching frozen release baseline.
