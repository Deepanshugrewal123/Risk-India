# RISK // INDIA — Phase 30D Technical Report
## National Weather Intelligence, Forecast Ingestion & Multi-Hazard Early Warning Engine

---

## Executive Summary

Phase 30D establishes the production-grade **National Weather Intelligence, Forecast Ingestion & Multi-Hazard Early Warning Engine** for **RISK // INDIA**. Prior to Phase 30D, future-risk forecasting relied on Phase 30A/30B/30C baseline contracts and dynamic catchment river telemetry.

With Phase 30D, the platform introduces a nationwide meteorological evidence layer covering all **28 States and 8 Union Territories (36 administrative entities)**, river basins, and supported districts. The engine systematically ingests and validates synoptic surface observations, numerical weather predictions across multiple lead-time horizons (NOW, 0–6H, 6–24H, 1–3D, 3–7D), and official meteorological bulletins and warnings from authoritative agencies (India Meteorological Department, Central Water Commission, NDMA, NRSC/Bhuvan).

Crucially, Phase 30D establishes that **weather data serves as an empirical evidence layer** feeding downstream multi-hazard assessments. It strictly bars pseudo-scientific deterministic earthquake predictions from meteorological signals, and preserves the Assam prototype ML boundary without expanding speculative ML to other regions.

---

## Non-Negotiable Scientific Invariants

1. **Byte-for-Byte Assam ML Model Preservation:**
   - Artifact: `ml/flood/artifacts/model.joblib`
   - Expected & Verified SHA-256: `0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf`
   - Status: **IDENTICAL / UNMODIFIED**

2. **Byte-for-Byte Assam Flood Training Dataset Preservation:**
   - Dataset: `datasets/processed/flood_assam/flood_features.csv`
   - Expected & Verified SHA-256: `88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080`
   - Status: **IDENTICAL / UNMODIFIED**

3. **Assam ML Model Scope Boundary:**
   - Machine learning inference is strictly restricted to the Assam Brahmaputra basin prototype (`assam_flood_prototype_v1`).
   - For all other 35 administrative entities, the system transparently utilizes `REGIONAL_BASELINE + OFFICIAL_INTELLIGENCE + VALIDATED_EVIDENCE_SIGNALS` with `ml_available = False`.

4. **Strict Earthquake Non-Prediction Invariant:**
   - Earthquakes are tectonic phenomena and are fundamentally unpredictable from atmospheric weather observations or forecasts.
   - Atmospheric signals are strictly decoupled from earthquake risk evaluation; forward horizons for earthquakes return `UNAVAILABLE` confidence with explicit non-predictive scientific disclaimers.

5. **Zero Synthetic Data Invariant (`synthetic_records = 0`):**
   - No mock, synthetic, simulated, or randomized weather records are tolerated in the production pipeline.
   - Any payload containing synthetic flags, mock keywords, or simulated fields is unconditionally rejected at the quality engine gate.

6. **Decoupled Freshness and Severity:**
   - Stale observations degrade data confidence and uncertainty metrics, but never artificially modify or inflate hazard severity indices.

---

## The 14-Gate Meteorological Quality Engine

Every raw meteorological record passes through a 14-gate verification pipeline before acceptance into temporal storage:

| Gate # | Code | Description | Enforcement Action |
|---|---|---|---|
| **1** | `MISSING_LOCATION` | Region or station identifier missing, empty, or whitespace | Reject packet |
| **2** | `INVALID_TIMESTAMP` | Unparseable or non-ISO-8601 UTC timestamp | Reject packet |
| **3** | `NON_NUMERIC_VALUE` | Measurement is NaN, Inf, string, boolean, or None | Reject packet |
| **4** | `UNKNOWN_UNIT` | Unit not recognized in canonical SI conversion table | Reject packet |
| **5** | `PHYSICALLY_IMPOSSIBLE_VALUE` | Temperature < -50°C or > 60°C, rainfall < 0 or > 2000mm, wind > 150 m/s, pressure < 850 or > 1085 hPa | Reject packet |
| **6** | `OUT_OF_BOUNDS_COORDINATES` | Coordinates outside India WGS84 bounding box ([6–38°N, 68–98°E]) | Reject packet |
| **7** | `UNVERIFIED_GEOGRAPHIC_MAPPING` | Entity unresolved or returned `UNMAPPED` | Reject packet |
| **8** | `DUPLICATE_RECORD` | Observation or forecast ID already ingested (deterministic hash match) | Reject packet |
| **9** | `CORRUPTED_PAYLOAD` | Non-dictionary structure or missing critical metadata | Reject packet |
| **10** | `FUTURE_OBSERVATION` | Observation timestamp > now + 5 minutes tolerance | Reject packet |
| **11** | `INVALID_FORECAST_WINDOW` | Forecast valid until <= valid from, or invalid horizon | Reject packet |
| **12** | `STALE_DATA` | Age exceeds operational threshold (> 90 days) | Reject packet |
| **13** | `UNSUPPORTED_VARIABLE` | Variable not in canonical meteorological variable registry | Reject packet |
| **14** | `MISSING_PROVIDER_PROVENANCE` | Provider identity missing or unaccredited | Reject packet |

*Synthetic data is rejected immediately via Gate `SYNTHETIC_DATA_REJECTED` whenever synthetic indicators or mock sources are detected.*

---

## Subsystem Architecture & Modules

```
backend/app/services/weather/
├── __init__.py                # Package exports, facades, and public API symbols
├── schema.py                  # Canonical schemas (CanonicalWeatherObservation, CanonicalWeatherForecast, WeatherWarning)
├── normalizer.py              # Mathematical unit normalizer (°C, mm, m/s, hPa, km)
├── geographic_mapper.py       # Deterministic router for 28 States, 8 UTs, and basins
├── quality_engine.py          # 14-gate quality validation & range enforcement
├── temporal_manager.py        # Chronological indexing, deduplication, and out-of-order handling
├── provider_client.py         # Multi-agency client with isolated circuit breakers (IMD, CWC, NDMA, NRSC)
├── freshness_engine.py        # Decoupled SLA freshness classification (LIVE, RECENT, STALE)
├── evidence_engine.py         # Multi-hazard evidence synthesis (Flood, Heatwave, Cyclone, Severe Weather, Landslide)
└── weather_service.py         # Central coordinator, thread-safe resilient storage, and national readiness probe
```

---

## REST API Endpoints

The subsystem exposes nine production-grade endpoints mounted under `/api/weather`:

1. `GET /api/weather/status`
   Operational subsystem metrics, backend storage status (`IN_MEMORY_RESILIENT`), 36 entities monitored, total observation/forecast/warning tallies, `synthetic_records_total: 0`, and live provider circuit states.

2. `GET /api/weather/current?region=...&limit=...`
   Latest validated synoptic surface weather observations with full provenance.

3. `GET /api/weather/forecast?region=...&horizon=...&limit=...`
   Multi-horizon numerical weather predictions (NOW, 0_6H, 6_24H, 1_3D, 3_7D) with uncertainty indicators.

4. `GET /api/weather/warnings?region=...&hazard=...&severity=...`
   Official meteorological alerts and bulletins with severity levels (RED, ORANGE, YELLOW, GREEN).

5. `GET /api/weather/regions/{region}`
   Comprehensive dossier for an administrative entity combining current weather, multi-horizon forecasts, active warnings, and synthesized hazard evidence.

6. `GET /api/weather/regions/{region}/forecast`
   Dedicated multi-horizon timeline for a specific administrative entity.

7. `GET /api/weather/freshness`
   Meteorological freshness standards, SLAs, decay parameters, and strict severity decoupling policy.

8. `GET /api/weather/providers`
   Live circuit breaker states, latencies, and resilience policies for IMD, CWC, NDMA, and NRSC_BHUVAN.

9. `GET /api/weather/readiness`
   National readiness probe reporting 36 monitored entities, 100% coverage, and `READY_FOR_EVIDENCE_FEEDS`.

---

## Frontend Components

Located in `src/components/weather/`:

1. `WeatherStatusCard.tsx`: Operational health, 36 monitored entities, observations/forecast counts, provider circuit states, and zero-synthetic badges.
2. `WeatherForecastTimeline.tsx`: Multi-horizon forecast cards across 0h → 7d with physical variables and uncertainty progression badges.
3. `WeatherWarningCard.tsx`: Official bulletins with color-coded severity tiers (RED, ORANGE, YELLOW, GREEN), issued timestamps, and authoritative bulletin links with `rel="noopener noreferrer"`.
4. `WeatherEvidencePanel.tsx`: Multi-hazard early-warning evidence signals, decoupled freshness notices, and the strict Earthquake Non-Prediction Scientific Guard banner.
5. `index.ts`: Package exports.

---

## Verification & Test Results

### 1. Dedicated Verification Suite
- File: `tests/test_phase30d_national_weather_intelligence.py`
- Test Dimensions: **40 distinct dimensions**
- Results: **40 / 40 PASS (0 failures, 0 errors)** in 0.901s

### 2. Full System Regression Suite
- Command: `python -m unittest discover tests`
- Baseline: 398 tests
- Phase 30D: 40 tests
- Total Tests: **438 / 438 PASS (0 failures, 0 errors, 0 regressions)** in 13.595s

### 3. Frontend Production Build
- Command: `npm run build` (`tsc && vite build`)
- Transformed Modules: 1976 modules
- Build Time: 3.08s
- Exit Code: **0 (CLEAN)**

---

## Next Steps

**PHASE 30E NOT STARTED.**
Phase 30D is fully complete, hardened, and verified.
