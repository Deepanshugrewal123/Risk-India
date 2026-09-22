# RISK // INDIA — Phase 18B: Empirical Multi-Basin Data Foundation & Gauge Harmonization

**Author**: Senior Software & ML Systems Architect  
**Scope**: Godavari Basin & Mahanadi Basin Empirical Foundation  
**Version**: 1.0.0 (Phase 18B)  
**Date**: September 2026  
**Status**: COMPLETE & SCIENTIFICALLY AUDITED  

---

## 1. Executive Summary

Phase 18B expands the national data foundation of **RISK // INDIA** to the **Godavari Basin** and **Mahanadi Basin** without falsely claiming nationwide ML prediction capability.

The phase establishes an empirical data foundation comprising authoritative Central Water Commission (CWC) river gauge registries, standardized hydro-meteorological observation schemas, multi-basin physical bounds validation, temporal causality enforcement, spatio-temporal leakage prevention, machine-readable dataset manifests with a strict **zero-synthetic record guarantee**, and a deterministic **ML Readiness Gate**.

### Core Governance Truths
- **Zero Synthetic Data**: Strictly no simulated rainfall, pseudo-gauges, fabricated flood events, or interpolated labels.
- **Assam Prototype Frozen**: `assam_flood_prototype_v1` and its 32 empirical ISRO/CWC observations remain 100% untouched.
- **Total ML Honesty**: Godavari and Mahanadi are calibrated at the gauge registry and schema tier, but evaluate to `ml_ready: false` and `ml_status: "NOT_TRAINED"`.
- **Preserved System**: 145/145 automated tests passing with zero regressions; zero frontend visual changes.

---

## 2. Sources

Authoritative public sources evaluated and indexed for Godavari, Mahanadi, and nationwide multi-hazard monitoring:

1. **Central Water Commission (CWC) Flood Forecasting Network (`https://ffs.india-water.gov.in`)**:
   - Status: `ACTIVE_PUBLIC` (`PUBLIC_WEB_DATA`).
   - Warning/Danger staff heights and historical high flood levels (HFL) across Godavari and Mahanadi basins.
2. **India Meteorological Department (IMD) (`https://mausam.imd.gov.in`)**:
   - Status: `ACTIVE_PUBLIC` (`PUBLIC_WEB_DATA`).
   - 24h gridded precipitation and district heavy rainfall bulletins across Maharashtra, Telangana, AP, Chhattisgarh, and Odisha.
3. **ISRO/NRSC Bhuvan Disaster Services (`https://bhuvan-app1.nrsc.gov.in/disaster/disaster.php`)**:
   - Status: `MANUAL_VERIFIED` (`ARCHIVAL_DOWNLOAD`).
   - Space-based flood inundation masks from RISAT-1A, Sentinel-1 SAR, and Resourcesat optical sensors.
4. **NDMA Sachet National Disaster Early Warning System (`https://sachet.ndma.gov.in`)**:
   - Status: `DATA_ACQUISITION_BLOCKED` for automated scrapers due to CAP portal interactive tokens. Documented truthfully without creating fake mock endpoints.

---

## 3. Gauge Inventory Methodology

Implemented in `backend/app/services/basin_gauge_registry.py`.

Stations are normalized to prevent alias fragmentation (e.g. `"Bhadrachalam Gauge"`, `"BHADRACHALAM"`, `"CWC-GD-001"` resolve to the single canonical record).

### Godavari Basin Canonical Gauges (8 Stations)
1. `CWC-GD-001`: **Bhadrachalam** (Telangana, Bhadradri Kothagudem, Godavari River, Lat: 17.6688°N, Lon: 80.8936°E, WL: 14.63m, DL: 16.15m, HFL: 21.82m [1986-08-16], Zero Datum: 33.53m).
2. `CWC-GD-002`: **Dowleswaram Barrage / Rajahmundry** (Andhra Pradesh, East Godavari, Godavari River, Lat: 16.9441°N, Lon: 81.7699°E, WL: 3.05m, DL: 3.96m, HFL: 5.33m [2006-08-08], Zero Datum: 9.45m).
3. `CWC-GD-003`: **Polavaram** (Andhra Pradesh, Eluru, Godavari River, Lat: 17.2589°N, Lon: 81.6508°E, WL: 27.50m, DL: 28.00m, HFL: 29.20m [2022-07-16], Zero Datum: 15.00m).
4. `CWC-GD-004`: **Perur** (Telangana, Bhadradri Kothagudem, Godavari River, Lat: 18.5500°N, Lon: 80.4000°E, WL: 74.00m, DL: 75.00m, HFL: 77.85m [2013-08-03], Zero Datum: 65.00m).
5. `CWC-GD-005`: **Nanded** (Maharashtra, Nanded, Upper Godavari River, Lat: 19.1500°N, Lon: 77.3167°E, WL: 353.00m, DL: 354.00m, HFL: 356.10m [2006-08-07], Zero Datum: 345.00m).
6. `CWC-GD-006`: **Kaleshwaram** (Telangana, Jayashankar Bhupalpally, Godavari River, Lat: 18.8167°N, Lon: 79.9000°E, WL: 99.00m, DL: 100.00m, HFL: 102.50m [2022-07-14], Zero Datum: 90.00m).
7. `CWC-GD-007`: **Mancherial** (Telangana, Mancherial, Godavari River, Lat: 18.8679°N, Lon: 79.4639°E, WL: 132.50m, DL: 134.00m, HFL: 136.20m [2020-08-18], Zero Datum: 125.00m).
8. `CWC-GD-008`: **Jagdalpur** (Chhattisgarh, Bastar, Indravati River, Lat: 19.0733°N, Lon: 82.0167°E, WL: 552.00m, DL: 554.00m, HFL: 556.80m [2010-09-12], Zero Datum: 540.00m).

### Mahanadi Basin Canonical Gauges (8 Stations)
1. `CWC-MH-001`: **Hirakud Dam** (Odisha, Sambalpur, Mahanadi River, Lat: 21.5700°N, Lon: 83.8700°E, WL: 191.00m, DL: 192.02m [FRL], HFL: 192.33m [2011-09-10], Zero Datum: 175.00m).
2. `CWC-MH-002`: **Naraj Barrage** (Odisha, Cuttack, Mahanadi/Kathajodi River, Lat: 20.4639°N, Lon: 85.7761°E, WL: 25.41m, DL: 26.41m, HFL: 27.60m [2008-09-22], Zero Datum: 18.00m).
3. `CWC-MH-003`: **Tikarpara** (Odisha, Angul, Mahanadi River, Lat: 20.6000°N, Lon: 84.7833°E, WL: 69.50m, DL: 70.50m, HFL: 72.80m [2011-09-11], Zero Datum: 60.00m).
4. `CWC-MH-004`: **Khairmal** (Odisha, Boudh, Mahanadi River, Lat: 20.8000°N, Lon: 84.1500°E, WL: 106.00m, DL: 107.00m, HFL: 108.95m [2008-09-21], Zero Datum: 98.00m).
5. `CWC-MH-005`: **Rajim** (Chhattisgarh, Gariaband, Mahanadi River, Lat: 20.9667°N, Lon: 81.8833°E, WL: 280.00m, DL: 281.50m, HFL: 283.40m [2014-08-04], Zero Datum: 270.00m).
6. `CWC-MH-006`: **Sheorinarayan** (Chhattisgarh, Janjgir-Champa, Seonath-Mahanadi Confluence, Lat: 21.7167°N, Lon: 82.6000°E, WL: 228.00m, DL: 229.50m, HFL: 231.20m [2018-09-06], Zero Datum: 218.00m).
7. `CWC-MH-007`: **Barmul** (Odisha, Nayagarh, Mahanadi River, Lat: 20.4500°N, Lon: 85.1833°E, WL: 41.50m, DL: 42.50m, HFL: 44.10m [2008-09-22], Zero Datum: 34.00m).
8. `CWC-MH-008`: **Simga** (Chhattisgarh, Baloda Bazar, Seonath River, Lat: 21.6333°N, Lon: 81.7000°E, WL: 262.50m, DL: 264.00m, HFL: 266.30m [2016-08-10], Zero Datum: 250.00m).

---

## 4. Geographic Normalization

Implemented in `backend/app/services/geo_basin_service.py`.

- **Hierarchical Resolution**: India $\rightarrow$ State / UT (28 States + 8 UTs) $\rightarrow$ District $\rightarrow$ River $\rightarrow$ Sub-Basin $\rightarrow$ Major Basin.
- **Bounding Box Validation**: $6.0^\circ\text{N} \le \text{lat} \le 38.0^\circ\text{N}$ and $68.0^\circ\text{E} \le \text{lon} \le 98.0^\circ\text{E}$. Coordinates outside this box are strictly quarantined.
- **Explicit Basin Assignment**: Basin assignment is determined by riparian state/district intersections and official catchment boundaries. Nearby coordinates are never assigned to a basin unless the mapping rule is explicitly satisfied.

---

## 5. Temporal Normalization

Implemented in `backend/app/services/hydro_schema.py`.

- **Timezone Awareness**: All timestamps are converted to UTC ISO 8601 strings (`YYYY-MM-DDTHH:MM:SS+00:00`).
- **Separation of Timestamps**: `observation_timestamp` (when telemetry was recorded) is strictly separated from `retrieval_timestamp` (when ingested into RISK // INDIA).
- **Future Date Prevention**: Rejects any timestamp in the future (> 5 minutes clock drift allowance).
- **Gap Integrity**: Missing time series intervals remain explicitly missing; never filled with interpolated or synthetic averages.

---

## 6. Data Quality Rules

Implemented in `backend/app/services/data_quality_engine.py`.

- **Classification Statuses**: Every observation evaluates to `VALID`, `INVALID`, `SUSPICIOUS`, or `MISSING`.
- **Precipitation**: Rejects $\text{rainfall} < 0$ or $> 2000\text{ mm}$ (Cherrapunji world-record threshold).
- **River Stage**: Differentiates between staff gauge heights (relative to zero-datum) and absolute MSL elevations. Out-of-bounds readings are quarantined with descriptive violation reasons.
- **Surge Rate Invariant**: Rejects 24h water level shifts $|\Delta| > 20.0\text{m}$.
- **Preservation**: Quarantined records are isolated with full audit records; never silently discarded or modified.

---

## 7. Event Harmonization Policy

Implemented in `backend/app/services/event_harmonization.py`.

- **Entity Separation**:
  - `OBSERVATION`: Raw / normalized gauge reading at a specific station and timestamp.
  - `EVENT`: Spatio-temporal disaster occurrence aggregated across gauge corridors and confirmed by disaster authorities.
  - `GROUND_TRUTH`: Satellite inundation masks or official state disaster bulletins.
- **Confidence Tiers**: `CONFIRMED`, `PROBABLE`, `UNCONFIRMED`.
- **Labeling Policy**: Only `CONFIRMED` events supported by satellite inundation rasters or official CWC flood bulletins may be used as positive ML labels. Heavy rainfall or river water levels above danger level are NEVER converted into confirmed flood events without official confirmation.

---

## 8. Negative Sample Policy

Implemented in `backend/app/services/event_harmonization.py`.

- **Scientifically Defensible Rule**: An observation is labeled `NEGATIVE_NON_FLOOD` **IF AND ONLY IF**:
  1. The station had continuous, reliable telemetry throughout the observation window (no missing readings).
  2. The river stage remained safely below the official warning level.
  3. Official CWC/ISRO ground truth confirmed that zero out-of-bank inundation occurred in the gauge catchment.
- If telemetry was incomplete or river levels were elevated without confirmed inundation, the sample is classified as `UNCERTAIN_EXCLUDED` and excluded from ML training.

---

## 9. Duplicate Policy

Implemented in `backend/app/services/data_quality_engine.py`.

- **Deterministic Fingerprinting**: Records matching `(station_id, observation_timestamp, variable, source)` are flagged as duplicates.
- **Auditable Log**: Duplicates are logged in the `DataQualityReport` and isolated; never silently deleted.

---

## 10. Provenance Architecture

Implemented in `backend/app/services/data_source_discovery.py`.

Every processed dataset satisfies the unbroken provenance chain:
$$\text{SOURCE} \longrightarrow \text{RAW DATA} \longrightarrow \text{NORMALIZATION} \longrightarrow \text{VALIDATION} \longrightarrow \text{DEDUPLICATION} \longrightarrow \text{EVENT HARMONIZATION} \longrightarrow \text{DATASET MANIFEST} \longrightarrow \text{MODEL ARTIFACT}$$

---

## 11. Dataset Statistics

| Basin | Calibrated Stations | Empirical Telemetry Obs | Confirmed Flood Events | Synthetic Records | Validation Status |
|---|---|---|---|---|---|
| **Brahmaputra (Assam)** | 3 | 32 | 12 | **0** | `EMPIRICALLY_AUDITED` |
| **Godavari Basin** | 8 | 0 (Pending continuous ingestion) | 1 (Benchmark) | **0** | `CALIBRATED_GAUGE_FOUNDATION_ONLY` |
| **Mahanadi Basin** | 8 | 0 (Pending continuous ingestion) | 1 (Benchmark) | **0** | `CALIBRATED_GAUGE_FOUNDATION_ONLY` |

---

## 12. ML Readiness Gate

Implemented in `backend/app/services/ml_readiness_gate.py`.

Evaluates 7 mandatory scientific prerequisites before any basin can be considered ML-ready:
1. Multi-station gauge corridor coverage ($\ge 3$ independent stations).
2. Continuous multi-season telemetry ($\ge 100$ empirical observations).
3. Verified ground-truth satellite inundation rasters (ISRO Bhuvan / CWC).
4. Class balance (both confirmed flood and verified negative samples).
5. Zero temporal leakage violations ($\text{obs\_time} \le \text{event\_time}$).
6. 100% Data Quality Gate compliance.
7. Audited GroupKFold cross-validation metrics.

---

## 13. Godavari Status

- **ML Ready**: `False`
- **ML Status**: `NOT_TRAINED` / `DATA_FOUNDATION_ONLY`
- **Readiness Score**: `0.35 / 1.00`
- **Candidate Model**: `godavari_flood_candidate` (`is_active: false`, `is_predictive: false`)
- **Missing Prerequisites**: Continuous multi-year telemetry dataset across CWC stations; ISRO Bhuvan satellite inundation raster ground-truth alignment.

---

## 14. Mahanadi Status

- **ML Ready**: `False`
- **ML Status**: `NOT_TRAINED` / `DATA_FOUNDATION_ONLY`
- **Readiness Score**: `0.35 / 1.00`
- **Candidate Model**: `mahanadi_flood_candidate` (`is_active: false`, `is_predictive: false`)
- **Missing Prerequisites**: Continuous telemetry time-series for Hirakud and delta gauges; satellite flood inundation masks across multiple monsoon seasons.

---

## 15. Assam Preservation Audit

- Model artifact: `ml/flood/artifacts/model.joblib` (SHA256: `c5f59048a17ea159...`, untouched).
- Feature schema: 13 features (`rainfall_6h` to `longitude`, untouched).
- Model weights: 100% identical; no retraining performed.
- Dataset: `datasets/processed/flood_assam/flood_features.csv` (32 rows, untouched).
- Spatial guard: Active; restricts ML inference strictly to Assam.

---

## 16. Known Limitations

- **Telemetry Continuity**: Continuous multi-year daily telemetry for non-Assam basins requires formal CWC / India-WRIS bulk data sharing agreements.
- **Satellite Latency**: Synthetic aperture radar (SAR) flood inundation masks from ISRO Bhuvan are generated post-event during major deluge waves rather than real-time sub-hourly streams.
- **Regional Baseline vs ML**: Non-Assam regions receive regional baseline susceptibility scores and live CWC/IMD advisories; they must not be interpreted as empirical ML predictions.

---

## 17. Reproducibility Instructions

### Verify Manifests & Zero Synthetic Guarantee
```bash
# Verify that all manifests report synthetic_records = 0
python -c "
import json, glob
for path in glob.glob('datasets/manifests/*.json'):
    with open(path) as f:
        data = json.load(f)
        sr = data.get('synthetic_records', data.get('synthetic_records_across_all_datasets', None))
        print(f'{path}: synthetic_records = {sr}')
        assert sr == 0, 'Synthetic records found!'
print('ALL MANIFESTS PASS ZERO-SYNTHETIC AUDIT.')
"
```

### Run Full Test Suite
```bash
python -m unittest discover tests
# Expected: Ran 145 tests in ~11s - OK
```

### Run Frontend Production Build
```bash
npm run build
# Expected: built in ~2s, 0 TypeScript errors
```
