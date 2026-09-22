# RISK // INDIA — Phase 30B: National Weather & Environmental Future-Risk Intelligence Engine

**Phase:** Phase 30B  
**Scope:** Nationwide Weather and Environmental Future-Risk Intelligence Engine across all 28 States and 8 Union Territories (36 Administrative Entities), Major River Basins, and District-Level Early Warning Extensions  
**Status:** **PASS — PRODUCTION-VERIFIED & CERTIFIED**  
**Date:** September 2026  

---

## 1. Executive Summary & Core Public Life-Safety Directives

Phase 30B transitions RISK // INDIA from the foundational architecture established in Phase 30A into an operational **National Weather & Environmental Future-Risk Intelligence Engine**. The platform directly answers the five critical life-safety questions for citizens and disaster managers during crisis and pre-crisis periods:

| Citizen Question | Subsystem | Methodology | Output Representation |
|:---|:---|:---|:---|
| **1. What disaster risk may develop next?** | Normalized Future-Risk Engine | Multi-Hazard Forward Evaluation | `hazard`, `risk_level` (`LOW`, `MODERATE`, `HIGH`, `VERY_HIGH`, `CRITICAL`) |
| **2. What evidence indicates that risk?** | Multi-Source Corroboration Engine | Hydro-Meteorological Ingestion | Evidence signals from IMD, CWC, USGS, GSI, and published baselines |
| **3. When could the risk increase?** | Multi-Horizon Forecasting | Temporal Windowing | 5 horizons (`NOW`, `0_6_HOURS`, `6_24_HOURS`, `1_3_DAYS`, `3_7_DAYS`) |
| **4. How confident is the assessment?** | Confidence & Uncertainty Engine | Deterministic Multi-Factor Scoring | Qualitative confidence (`LOW`, `MODERATE`, `HIGH`) and uncertainty bounds |
| **5. What should people do before it worsens?** | Disaster Action Engine & Public UX | Before/During Action Checklists | Plain-language advisory answering WHAT, WHEN, WHY, WHAT TO DO, SOURCE |

---

## 2. Inviolate Scientific Invariants & Supply-Chain Security

The machine-learning foundation remains frozen byte-for-byte:

| Scientific Asset | Expected SHA-256 | Verified SHA-256 | Status |
|:---|:---|:---|:---:|
| `ml/flood/artifacts/model.joblib` | `0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf` | `0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf` | **PASS (UNMODIFIED)** |
| `datasets/processed/flood_assam/flood_features.csv` | `88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080` | `88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080` | **PASS (UNMODIFIED)** |
| `assam_flood_prototype_v1` | 13 features, 32 observations | 13 features, 32 observations | **PASS (FROZEN)** |
| Synthetic Records Guarantee | Strictly 0 | Strictly 0 | **PASS (ZERO SYNTHETIC)** |

### Strict Non-Assam ML Boundary
- **Assam Corridor:** `assam_flood_prototype_v1` operational for riverine flood modeling.
- **Non-Assam Administrative Entities (35 Entities):** Machine-learning prediction is strictly blocked (`ml_available = False`). Transparent citizen disclosure enforced:
  > *"Empirical ML prediction is not currently validated for this region. ML prediction unavailable for this region. Regional baseline and official disaster intelligence are shown."*

---

## 3. Normalized Forecast Variable Contracts

Phase 30B introduces comprehensive internal dataclass contracts under `forecast_contracts.py`:

### 3.1 Contract Dimensions
1. **Weather Observation (`WeatherObservationVariable`):** Ambient temperature (°C), 24h precipitation (mm), relative humidity (%), wind speed (km/h) & direction (°), atmospheric pressure (hPa), synoptic condition descriptor.
2. **Weather Forecast (`WeatherForecastVariable`):** Forward 24h precipitation forecast (mm), projected temperature (°C), projected wind velocity (km/h), forecast humidity (%), barometric pressure trend (hPa), severe weather warning flags.
3. **Hydrological Telemetry (`HydrologicalVariable`):** Gauge river stage (m), stage trend (`RISING`, `FALLING`, `STEADY`, `UNAVAILABLE`), 72h accumulated catchment precipitation (mm), basin saturation condition (`SATURATED`, `MODERATE`, `NORMAL`, `DRY`), official CWC flood stage alert.
4. **Cyclone Dynamics (`CycloneVariable`):** Active cyclonic disturbances, forecast track coordinate projections, directional movement vector, sustained surface wind intensity (knots), coastal vulnerability tier, official IMD RSMC advisories.
5. **Environmental Baseline (`EnvironmentalVariable`):** Terrain slope vulnerability (GSI NLSM index), historical hazard susceptibility rating, statutory regional baseline scores across all 6 hazards.

### 3.2 Metadata & Ingestion Invariants
Every input variable encapsulates a `NormalizedInputMetadata` header with:
- Authoritative Source & Provider Identification
- Observation & Forecast Timestamps (UTC ISO-8601)
- Geographic Scope (Administrative Entity / District / River Basin)
- Physical Unit of Measurement
- Freshness Classification (`LIVE`, `RECENT`, `CACHED`, `STALE`, `REGIONAL_BASELINE`)
- Provenance Identifiers (linking to official bulletin IDs and portals)
- Availability State (`AVAILABLE`, `UNAVAILABLE`, `DEGRADED`)
- Data Quality Status (`VALIDATED`, `ESTIMATED`, `HISTORICAL_NORMAL`, `UNAVAILABLE`)

**Scientific Honesty Rule:** When external telemetry is unavailable, the engine returns `UNAVAILABLE` and historical normal bounds. It **never** manufactures synthetic values.

---

## 4. Specialized Multi-Hazard Future-Risk Sub-Engines

### 4.1 Flood Future-Risk Engine
- **Evaluation Logic:** Evaluates 24h forecast precipitation, 72h antecedent saturation, gauge stage trend, and CWC warning thresholds.
- **Causal Transparency:** Produces an explicit `WHY_FLOOD_RISK_CHANGED` rationale explaining the physical mechanisms:
  > Example: *"WHY_FLOOD_RISK_CHANGED: forecast rainfall elevated (110.0 mm/24h) + recent rainfall accumulation elevated (142.5 mm) + river level rising + official CWC warning detected."*

### 4.2 Cyclone Future-Risk Engine
- **Three-Tier Separation:** Strictly separates:
  - `CYCLONE_DETECTED`: Binary state tracking real disturbances.
  - `CYCLONE_FORECAST`: Official IMD forecast track, landfall window, and movement vector.
  - `CYCLONE_IMPACT_RISK`: Coastal exposure index combined with maximum sustained wind speed.
- Prohibits claiming independent cyclogenesis prediction when no official disturbance exists.

### 4.3 Heatwave Future-Risk Engine
- **Evaluation Logic:** Assesses ambient temperature, departure from climatological normal (>4.5°C for heatwave, >6.4°C for severe heatwave), and multi-day persistence across 6–24h, 1–3d, and 3–7d windows.
- **Microclimate Disclaimer:** Explicitly notes urban heat island (UHI) temperature elevations.

### 4.4 Severe Weather Engine
- **Evaluation Logic:** Monitors convective mesoscale storm indicators, squalls, gale-force winds, lightning nowcasts, and heavy precipitation alerts.
- **Methodology Honesty:** Tagged as `OFFICIAL_WARNING` when official IMD red/orange alerts exist, and `FORECAST_DERIVED_RISK` when derived from numerical indicator thresholds.

### 4.5 Landslide Future-Risk Engine
- **Evaluation Logic:** Combines GSI National Landslide Susceptibility Mapping (NLSM) slope data with orographic precipitation and 72h antecedent saturation thresholds.
- **Label Honesty:** Strictly designated as `POTENTIAL_LANDSLIDE_RISK` with an explicit disclaimer that exact slip timing is not deterministically predictable.

### 4.6 Earthquake Intelligence Engine
- **STRICT NON-PREDICTION INVARIANT:**
  - Exact deterministic earthquake prediction (time, location, magnitude) is **SCIENTIFICALLY IMPOSSIBLE**.
  - All forward horizons (`0_6_HOURS`, `6_24_HOURS`, `1_3_DAYS`, `3_7_DAYS`) return `confidence = UNAVAILABLE`, methodology `REGIONAL_BASELINE`, and the mandatory scientific disclaimer.
  - The `NOW` horizon provides `RECENT_SEISMIC_ACTIVITY` from official USGS and NCS telemetry, combined with `SEISMIC_CONTEXT` and `SEISMIC_BASELINE_RISK` under BIS IS 1893:2016 zonation.

---

## 5. Confidence Engine & Multi-Source Corroboration

### 5.1 Deterministic Qualitative Scoring
Qualitative confidence (`LOW`, `MODERATE`, `HIGH`) is deterministically calculated across 6 weighted factors:
1. **Data Completeness (30%):** Ratio of verified observation and forecast signals available.
2. **Multi-Source Corroboration (25%):** Evidence agreement between independent providers (e.g., IMD precipitation forecast + CWC gauge stage trend + NDMA administrative alert).
3. **Official Warning Presence (20%):** Validates whether statutory authorities have declared active disaster stages.
4. **Observation Freshness (15%):** Penalizes stale or cached telemetry.
5. **Forecast Lead Time (10%):** Incorporates synoptic horizon degradation.
6. **ML Validation Bonus (Assam only):** Confirms validated empirical prototype status.

### 5.2 Uncertainty Scaling
Uncertainty is categorized as `LOW`, `MODERATE`, `HIGH`, or `VERY_HIGH`:
- Nowcasting (`NOW`, `0_6_HOURS`) with comprehensive data $	o$ `LOW` uncertainty.
- Medium-range (`1_3_DAYS`) $	o$ `MODERATE` to `HIGH` uncertainty.
- Extended synoptic outlooks (`3_7_DAYS`) $	o$ `HIGH` or `VERY_HIGH` uncertainty.

**Public Safety Rule:** Qualitative confidence is explicitly communicated as an evidence-completeness and agreement metric—**never** as a mathematical or statistical probability.

---

## 6. Public Safety UX & Citizen Explanation Format

Technical parameters are converted into accessible citizen advisories via `GET /api/future-risk/{region}/explanation`:

```json
{
  "hazard": "FLOOD",
  "region": "Assam",
  "district": "All vulnerable districts",
  "risk_level": "VERY_HIGH",
  "forecast_window": "6_24_HOURS",
  "methodology": "EMPIRICAL_ML",
  "public_safety_advisory": {
    "what": "VERY_HIGH flood risk developing in riverine catchments of Assam.",
    "when": "Next 24 hours (Diurnal runoff and forecast cycle).",
    "why": "forecast rainfall elevated (110.0 mm/24h) + recent rainfall accumulation elevated (142.5 mm) + river level rising + official CWC warning detected.",
    "confidence": "HIGH (Uncertainty: LOW, Data Completeness: 80%). Note: Qualitative confidence reflects evidence completeness and lead-time certainty, not statistical probability.",
    "what_to_do": {
      "preparedness_phase_before": [
        "Prepare a 72-hour Disaster Kit: 3L drinking water per person/day, dry rations, torch, spare batteries, first aid, and power banks.",
        "Seal identity documents, land records, insurance, and prescription medicines in waterproof ziplock bags.",
        "Identify nearest designated high-ground flood evacuation centers and community elevated shelters."
      ],
      "immediate_safety_phase_during": [
        "Evacuate immediately upon receipt of official DDMA evacuation orders; do not wait until water enters premises.",
        "Turn off main electrical breaker switch and cooking gas cylinders before leaving premises.",
        "Never walk, swim, or drive through moving floodwaters. Just 15 cm (6 inches) of moving water can knock an adult down; 30 cm can float a vehicle."
      ],
      "emergency_dispatch": "Call 112 (National Unified Emergency Response) or 1078 (NDMA National Control Room)."
    },
    "source": "Authoritative Government Sources: CWC, IMD"
  },
  "scientific_limitations": "Localized embankment breaches and reservoir emergency releases can cause localized surges exceeding gauge trend forecasts.",
  "ml_scope_note": "Validated empirical ML active via assam_flood_prototype_v1 (13 hydro-meteorological features, 32 historical observations).",
  "synthetic_records": 0
}
```

---

## 7. REST API Endpoints Specification

| Endpoint | Method | Description |
|:---|:---:|:---|
| `/api/future-risk` | `GET` | National multi-hazard forward risk summary across 36 entities (supports `?hazard=` and `?horizon=`). |
| `/api/future-risk/{region}` | `GET` | Multi-hazard multi-horizon future risk profile for a State or UT. |
| `/api/future-risk/{region}/forecast` | `GET` | Normalized weather observations, forecasts, hydrological telemetry, cyclone indicators, and environmental baseline variables. |
| `/api/future-risk/{region}/explanation` | `GET` | Plain-language citizen explanation answering WHAT, WHEN, WHY, CONFIDENCE, WHAT TO DO, and SOURCE. Supports `?hazard=` and `?district=`. |
| `/api/future-risk/{region}/actions` | `GET` | Structured Before / During / After action checklists. |
| `/api/future-risk/{region}/{hazard}` | `GET` | Detailed forward risk evaluation for a specific region and hazard. |
| `/api/future-risk/{region}/{hazard}/timeline` | `GET` | Step-by-step projection across all 5 horizons (`NOW`, `0_6H`, `6_24H`, `1_3D`, `3_7D`). |
| `/api/future-risk/help` | `GET` | Verified emergency dispatch numbers and statutory relief funds directory. |
| `/api/future-risk/ml-expansion` | `GET` | 14-gate scientific promotion audit across the 5 priority river basins. |

---

## 8. Automated Verification & Certification Evidence

- **Phase 30B Test Suite (`tests/test_phase30b_national_future_risk.py`):** 24 / 24 Tests Passing (1.01s).
- **Phase 30A Test Suite (`tests/test_phase30a_future_risk_forecasting.py`):** 22 / 22 Tests Passing (0.64s).
- **Full Repository Test Suite (`python -m unittest discover tests`):** **368 / 368 Tests Passing (0 failures, 0 errors, 0 regressions)**.
- **Frontend Production Build:** PASS (`tsc && vite build` completed in 3.03s with 0 errors).
- **Supply Chain Integrity:**
  - `ml/flood/artifacts/model.joblib`: `0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf` (**EXACT MATCH**)
  - `datasets/processed/flood_assam/flood_features.csv`: `88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080` (**EXACT MATCH**)
- **Zero Synthetic Data:** `synthetic_records = 0` verified across all endpoints and data models.
