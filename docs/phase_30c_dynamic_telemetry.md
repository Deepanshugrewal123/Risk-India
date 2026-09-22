# RISK // INDIA — Phase 30C Technical Report
## Dynamic Catchment Telemetry Stream & Hydrological Sensor Ingestion

---

## Executive Summary

Phase 30C establishes the production-grade empirical hydrological telemetry stream and sensor ingestion architecture for **RISK // INDIA**. Prior to Phase 30C, hydrological gauges were registered as static metadata records in the basin registry, and forward risk forecasting relied on synoptic weather advisories or regional climatological baselines.

With Phase 30C, the platform ingests authentic, real-time catchment sensor measurements across India's major river basins, enforcing deterministic unit normalization, hierarchical catchment routing, a 13-gate machine-readable data quality engine, isolated upstream circuit breakers, chronological ordering with late-packet handling, orthogonal freshness computation, and seamless in-memory fallback.

---

## Key Architectural Principles & Invariants

1. **Zero Synthetic Data Invariant (`synthetic_records = 0`):**
   Synthetic observations, simulations, or fabricated data points are rejected at ingestion via Gate 11 (`SYNTHETIC_DATA_REJECTED`).

2. **Byte-for-Byte Scientific Invariants:**
   - Model artifact: `ml/flood/artifacts/model.joblib`
     SHA-256: `0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf`
   - Training dataset: `datasets/processed/flood_assam/flood_features.csv`
     SHA-256: `88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080`
   - Assam model weights are frozen; ML inference is strictly restricted to Assam (`ml_available = False` for all non-Assam basins).

3. **Deterministic Hierarchical Spatial Routing:**
   Every incoming telemetry packet is resolved via:
   $$\\text{GAUGE} \\longrightarrow \\text{RIVER} \\longrightarrow \\text{CATCHMENT/SUB-BASIN} \\longrightarrow \\text{MAJOR BASIN} \\longrightarrow \\text{STATE/UT}$$
   Unrecognized or unverified gauges are marked with `status = "UNMAPPED"` and rejected from ingestion. Guessing or hallucinating catchment memberships is strictly prohibited.

4. **Mathematical Unit Normalization:**
   - Water level: `m` (canonical metric relative to MSL/datum). Converts `ft` ($\\times 0.3048$), `cm` ($\\times 0.01$).
   - Rainfall: `mm` (canonical metric). Converts `in` ($\\times 25.4$), `cm` ($\\times 10.0$).
   - Discharge: `m3_s` (canonical cubic meters per second). Converts `cusec` ($\\times 0.0283168$).
   - Any unknown/ambiguous unit triggers Gate 4 (`UNKNOWN_UNIT`) rejection. Guessing is strictly prohibited.

5. **Decoupled Freshness and Severity:**
   Freshness is derived solely from the elapsed observation delta:
   - `LIVE`: $< 1$ hour ($< 3600\\text{s}$)
   - `RECENT`: $< 24$ hours ($< 86400\\text{s}$)
   - `STALE`: $\\ge 24$ hours
   Severity and freshness are orthogonal: a river stage exceeding Danger Level with 30-hour-old data is classified as `CRITICAL` severity and `STALE` freshness (never promoted to `LIVE` because of elevated risk).

6. **Provider Isolation & Circuit Breakers:**
   Independent circuit breakers protect each upstream data source:
   - Central Water Commission (CWC)
   - India Meteorological Department (IMD)
   - NRSC / ISRO Bhuvan
   - Assam State Disaster Management Authority (ASDMA)
   Failure in one agency never degrades, blocks, or trips peer providers.

---

## The 13 Machine-Readable Data Quality Gates

| Gate # | Code | Description | Action on Failure |
|---|---|---|---|
| **1** | `MISSING_GAUGE_ID` | Station identifier missing, empty, or whitespace | Reject packet |
| **2** | `INVALID_TIMESTAMP` | Unparseable or non-ISO-8601 UTC timestamp | Reject packet |
| **3** | `NON_NUMERIC_VALUE` | Measurement is NaN, Inf, string, boolean, or None | Reject packet |
| **4** | `UNKNOWN_UNIT` | Unit not recognized in canonical conversion tables | Reject packet |
| **5** | `PHYSICALLY_IMPOSSIBLE_VALUE` | Negative rain, water level outside [-10, 1000]m, discharge > 150k m³/s | Reject packet |
| **6** | `OUT_OF_BOUNDS_COORDINATES` | Coordinates outside India WGS84 bounding box ([6-38°N, 68-98°E]) | Reject packet |
| **7** | `UNVERIFIED_GEOGRAPHIC_MAPPING` | Station has `status = "UNMAPPED"` or unverified catchment | Reject packet |
| **8** | `DUPLICATE_OBSERVATION` | Observation ID already exists in series (deterministic hash match) | Reject packet |
| **9** | `CORRUPTED_PAYLOAD` | Payload is not a valid dictionary or missing structural keys | Reject packet |
| **10** | `FUTURE_DATED_OBSERVATION` | Timestamp > now + 5 minutes tolerance | Reject packet |
| **11** | `SYNTHETIC_DATA_REJECTED` | Synthetic flag true, synthetic records > 0, or synthetic keywords detected | Reject packet |
| **12** | `STALE_THRESHOLD_EXCEEDED` | Observation older than operational max age threshold (> 90 days) | Reject packet |
| **13** | `UNSUPPORTED_VARIABLE` | Variable type not in (`WATER_LEVEL`, `RAINFALL`, `DISCHARGE`) | Reject packet |

---

## Subsystem Architecture & Modules

```
backend/app/services/telemetry/
├── __init__.py                # Package facade exporting services and dataclasses
├── schema.py                  # Canonical observation, gauge, and batch schemas
├── gauge_registry.py          # Spatial routing & 26 canonical CWC stations
├── unit_normalizer.py         # Deterministic SI unit conversion engine
├── quality_engine.py          # 13 machine-readable quality gates
├── temporal_manager.py        # Chronological sorting, deduplication, late packets
├── provider_client.py         # Multi-provider client with isolated circuit breakers
└── telemetry_service.py       # Thread-safe central facade & readiness evaluator
```

---

## REST API Endpoints

The subsystem exposes four production endpoints mounted under `/api/telemetry`:

1. `GET /api/telemetry/status`
   Returns subsystem health, active backend storage (`IN_MEMORY_RESILIENT`), gauge counts, freshness breakdown (`live_gauges`, `recent_gauges`, `stale_gauges`), and live circuit states across all four providers.

2. `GET /api/telemetry/gauges?basin=...&state=...&status=...`
   Returns canonical gauge stations filtered by basin, state, or status (`ACTIVE_CALIBRATED`, `UNMAPPED`).

3. `GET /api/telemetry/observations?gauge_id=...&basin=...&state=...&variable_type=...&limit=...`
   Returns chronological observation streams with complete provenance and normalized SI units.

4. `GET /api/telemetry/readiness`
   Basin-by-basin telemetry readiness assessment across the 5 priority basins (Brahmaputra, Ganga, Godavari, Mahanadi, Krishna).

---

## Verification & Audit Results

- **Automated Verification:** 398 / 398 tests passing (0 failures, 0 errors, 0 regressions).
- **Dedicated Suite:** `tests/test_phase30c_dynamic_telemetry.py` (30 test cases).
- **Frontend Production Build:** `tsc && vite build` built in 3.02s without errors.
- **Model Invariance:** `0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf` (Exact match).
- **Dataset Invariance:** `88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080` (Exact match).
- **Synthetic Records:** 0 across all production schemas and databases.
- **PHASE 30D STATUS:** NOT STARTED.
