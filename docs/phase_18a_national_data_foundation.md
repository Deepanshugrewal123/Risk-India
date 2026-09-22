# RISK // INDIA — Phase 18A: National Data Foundation & Multi-Hazard Intelligence

## Executive Summary
**RISK // INDIA** Phase 18A establishes the **National Data Foundation** required to expand disaster intelligence and future basin-level ML across India while preserving strict scientific honesty and zero synthetic fabrication.

All operations were executed under non-negotiable scientific boundaries:
- **ML Scope Honesty**: The existing Assam flood model (`assam_flood_prototype_v1`) remains strictly **Assam-only** (`status: PROTOTYPE`). No unverified nationwide prediction is claimed or rendered.
- **Dataset Preservation**: The 32 empirical ISRO/CWC observations are preserved verbatim with a reproducible cryptographic manifest declaring `synthetic_records = 0`.
- **Administrative Integrity**: Geographic normalization strictly enforces India's official **28 States and 8 Union Territories** (36 entities), resolving legacy post-merger aliases seamlessly.
- **Hydrological Abstraction**: India's 12 major river systems are cataloged for spatial and basin indexing without claiming ML inference coverage outside Assam.
- **Zero Regressions**: All 107 existing tests pass; 18 new automated tests added (**125 total passing tests, 0 failures, 0 regressions**).
- **No Live Deployment or Push**: Changes executed locally without Git commits, pushes, or deployments.

---

## 1. Authoritative Disaster Data Provider Audit

The platform conducts an honest accounting of upstream disaster data sources across India:

| Provider | Agency | Source Tier | Hazard Scope | Integration Status |
| :--- | :--- | :--- | :--- | :--- |
| **USGS Seismic** | United States Geological Survey | `LIVE_API` | Earthquake | Operational (Subcontinental Bounding Box [6°N–38°N, 68°E–98°E], Circuit Breaker enabled) |
| **IMD Mausam** | India Meteorological Department | `PUBLIC_WEB_DATA` | Cyclone, Heavy Rainfall, Heatwave | Operational (Official Synoptic Bulletins & Advisories) |
| **CWC FFS** | Central Water Commission | `PUBLIC_WEB_DATA` | Flood | Operational (Daily Hydrological Gauge Bulletins) |
| **ASDMA Assam** | Assam State Disaster Management Authority | `PUBLIC_WEB_DATA` | Flood, Landslide | Operational (Assam Monsoon Situation Reports) |
| **NDMA India** | National Disaster Management Authority | `PUBLIC_WEB_DATA` | Multi-Hazard, Heatwave | Operational (National Action Guidelines & Protocols) |
| **NDMA Sachet CAP** | NDMA / C-DOT | `AUTHENTICATED_API` | Multi-Hazard CAP Alerts | Documented Contract Only (No synthetic credentials fabricated) |
| **INCOIS** | Indian National Centre for Ocean Info Services | `PUBLIC_WEB_DATA` | Tsunami, Coastal Surge | Operational (Ocean State & Tsunami Bulletins) |
| **GSI** | Geological Survey of India | `PUBLIC_WEB_DATA` | Landslide | Operational (Monsoon Landslide Bulletins) |
| **India-WRIS** | Ministry of Jal Shakti | `DOWNLOADABLE_DATA` | Basin Telemetry | Historical Archive Synchronization |
| **ISRO/NRSC Bhuvan** | National Remote Sensing Centre | `DOWNLOADABLE_DATA` | Satellite Flood Inundation | Empirical Raster Ground Truth Integrated |

---

## 2. Normalized Multi-Hazard Event Schema

The canonical internal representation (`NormalizedDisasterEvent`) standardizes incidents across all hazards while maintaining 100% backward compatibility:
- **Canonical Hazard Types**: `EARTHQUAKE`, `FLOOD`, `CYCLONE`, `LANDSLIDE`, `HEATWAVE`, `LIGHTNING`, `TSUNAMI`, `HEAVY_RAINFALL`, `DROUGHT`, `OTHER`.
- **Extended Fields**: `event_id`, `event_subtype`, `basin`, `source_event_id`, `confidence`, `official_alert`, `geometry` (GeoJSON Point), `created_at`, `updated_at`.
- **Deterministic Freshness**:
  - `LIVE`: < 1 hour elapsed since observation
  - `RECENT`: < 24 hours elapsed
  - `STALE`: >= 24 hours elapsed
  - `UNAVAILABLE`: observation timestamp missing

---

## 3. Spatio-Temporal Event Deduplication Engine

Located in `backend/app/services/event_deduplication.py`:
- **Stage 1 (Exact Match)**: Deduplicates exact matches on `source` + `source_event_id` or `id`.
- **Stage 2 (Spatio-Temporal Fingerprinting)**:
  - Hazard type strict matching.
  - Great-circle distance check within 25 km via Haversine formulation.
  - Dynamic hazard-specific temporal tolerance: Earthquakes (1.5h), Weather/Cyclones (6.0h), Floods (12.0h), Drought (72.0h).
- **Stage 3 (Attribution Preservation)**: Combines secondary reports into composite attribution (e.g. `CWC / ASDMA`) while preserving the highest verified confidence.

---

## 4. Geographic Normalization & River Basin Foundation

Located in `backend/app/services/geo_basin_service.py`:
- **Administrative Normalization**:
  - Strict catalog of **28 States and 8 Union Territories** (36 entities).
  - Merged Dadra & Nagar Haveli and Daman & Diu (`code: "DN"`, capital `"Daman"`).
  - Aliasing engine resolving alternative spellings and legacy state codes.
- **River Basin Catalog**:
  - Major Indian River Basins cataloged: `Brahmaputra`, `Ganga`, `Indus`, `Godavari`, `Krishna`, `Mahanadi`, `Narmada`, `Tapi`, `Cauvery`, `Barak and Others`, `Coastal / Island`.
  - Maps state and district to hydrological sub-basins (e.g., Udalguri -> Dhansiri Catchment; Cachar -> Barak Valley).
  - Explicit disclaimer: *Hydrological normalization only. Does NOT claim or imply trained ML coverage outside the Assam prototype.*

---

## 5. Future Flood ML Data Pipeline & Quality Gates

Located in `backend/app/services/ml_data_pipeline.py`:
- **Seven Pipeline Stages**:
  `RAW` → `VALIDATED` → `NORMALIZED` → `EVENT_LABELED` → `FEATURE_ENGINEERED` → `LEAKAGE_AUDITED` → `MODEL_READY`
- **Quality Gates Enforcement**:
  - Coordinate validity: Subcontinental bounding box [6.0°N–38.0°N, 68.0°E–98.0°E].
  - Physical consistency: Negative rainfall rejection (`rainfall >= 0`), physically impossible river stages (`-10m <= stage <= 35m`).
  - Strict temporal ordering: Observation timestamp cannot be in the future, and cannot exceed event timestamp (`obs_time <= event_time`).
  - Quarantine mechanism: Malformed records isolated with explicit rule violation logs; never silently altered.

---

## 6. Cryptographic Dataset Manifest System

Located in `backend/app/services/dataset_manifest.py`:
- Canonical manifest created for `datasets/processed/flood_assam/flood_features.csv`:
  - `dataset_id`: `assam_flood_features_v1`
  - `version`: `1.0.0`
  - `row_count`: `32` (verified empirical observations)
  - `station_count`: `3`
  - `event_count`: `12`
  - `time_range`: `2022-05-23` to `2025-07-08`
  - `sha256`: Cryptographically computed and verified
  - **`synthetic_records = 0`** (MANDATORY non-synthetic declaration)

---

## 7. Versioned Hazard Model Registry

Located in `backend/app/services/model_registry.py`:
- Registered models:
  - `assam_flood_prototype_v1`: `status = PROTOTYPE`, `is_active = True`, `hazard = FLOOD`, `geographic_scope = ["Assam", "Brahmaputra Basin", "Barak Basin"]`.
  - Future models (`flood_godavari_v1`, `flood_mahanadi_v1`, `flood_ganga_v1`): `status = NOT_TRAINED`, `is_active = False`, clearly labeled as architecture placeholders.

---

## 8. Public ML Honesty & Emergency UX Enhancements

- **Public ML Honesty**:
  - In `AnalyzeAreaSection.tsx`, selecting an unsupported non-Assam region displays:
    **"ML flood prediction is currently unavailable for this region."**
  - Accompanied by three distinct information panels:
    1. **Regional Baseline Risk**: Baseline terrain and seasonal susceptibility score.
    2. **Official Intelligence**: Direct links to IMD Weather, CWC Flood, and NDMA alerts.
    3. **Verified Emergency Resources**: 24x7 National and State helplines.
- **Multi-Hazard Filtering**:
  - Added filter pills in `CurrentDisastersSection.tsx` for Hazard Type (`Earthquake`, `Flood`, `Cyclone`, `Landslide`, `Heatwave`), Severity, and Freshness.
  - Displays observation timestamp in IST and river basin where available.
- **Emergency Safety**:
  - All helpline numbers formatted with mobile-friendly `tel:` tap-to-call links.
  - Added prominent banner emphasizing that official evacuation directives from DDMA/SDMA/NDRF take precedence over statistical model predictions.

---

## 9. REST API Architecture Expansion

New endpoints integrated under `/api`:
- `GET /api/basins`: River basin catalog and state mappings.
- `GET /api/models`: Model Registry list of versioned hazard models.
- `GET /api/models/{id}`: Detailed model metadata and limitations.
- `GET /api/datasets/manifests`: Audited dataset manifests (`synthetic_records: 0`).
- `GET /api/disasters/providers`: Provider catalog, operational tiers, and circuit breaker health.
- `GET /api/disasters/status`: Operational feed status, freshness breakdown, and deduplication statistics.

---

## 10. Verification & Measured Benchmarks

### Automated Test Suite
- **Command**: `python -m unittest discover tests`
- **Total Test Count**: **125 tests** (107 existing + 18 Phase 18A)
- **Results**: **125 Passed, 0 Failed, 0 Errors (100% Pass Rate)**
- **Execution Time**: **11.661s**
- **Regressions**: **0**

### Frontend Production Build
- **Command**: `npm run build`
- **Status**: **SUCCESS in 2.23s (0 errors)**

### Measured Query Latencies
- Geographic normalization: **0.001 ms** (~1.4 microseconds)
- Quality gate validation: **0.001 ms** (~1.2 microseconds)
- `/api/basins` response time: **26.32 ms**
- `/api/models` response time: **4.05 ms**
- `/api/datasets/manifests` response time: **3.59 ms**
- `/api/disasters/providers` response time: **3.82 ms**
