# Assam Flood Training Dataset Expansion Audit

**Project**: RISK // INDIA — AI-Powered Disaster Risk Analysis Platform  
**Phase**: Phase 7G — Training Dataset Expansion Audit & Capacity Feasibility  
**Audit Date**: `2026-09-12 23:42:46`  
**Primary Question**: Can the current 12-observation dataset be safely and authoritatively expanded using real official data before machine learning model development?  

---

## 1. Executive Summary & Audit Recommendation

Phase 7F successfully established the **Assam Flood Pilot — Research Dataset** consisting of **12 fully verified observation windows** (8 positive flood inundations, 4 empirical negative baselines across 11 distinct event groups). While this dataset successfully validated the pipeline architecture, georeferencing, and strict leakage prevention, **12 observations are statistically insufficient for meaningful machine learning training or generalization**.

- **Current Census**: `12` observations (Degrees of freedom $N \approx p$; single-sample metric shift = 8.33%).
- **Total Bhuvan Archive Census**: `156` catalogued satellite flood inundation layers across 2021–2025.
- **Additional Proven Candidates**: **`38` layers** have verified Bhuvan flood rasters and active CWC hourly rainfall telemetry (17 from 2021 + 21 river sensor outages from 2022–2025).
- **Additional Conditional Candidates**: **`59` layers** have active river and rainfall telemetry but declare statewide bounding boxes, requiring individual raster swath verification.
- **Definitely Excluded / Unusable**: **`47` layers** (37 spatial mismatch outside pilot gauges, 7 rainfall telemetry data gaps, 3 multi-day composite layers).

> [!IMPORTANT]
> **FINAL AUDIT RECOMMENDATION**: **`EXPAND_DATASET_FIRST`**  
> Before initiating ML model training, the dataset must be expanded to either **Option B (50 samples, Rainfall-Only Inundation Model)** or **Option A Expanded (up to ~30–40 samples, Dual-Sensor Model)** to achieve statistical stability and meaningful cross-validation.

---

## 2. Current Dataset Status (Baseline Core)

- **Total Current Observations**: `12`
- **Positive Inundation Observations (`1`)**: `8` (Inundation swaths ranging from 6 to 21,610 flood pixels)
- **Negative Baseline Observations (`0`)**: `4` (Empirical non-inundated riverbed within natural banks; confirmed via 50km diagnostic rasters)
- **Unresolved Labels**: `0`
- **High Confidence Labels**: `11`
- **Review Required Labels**: `1` (`BHUVAN_ASSAM_20250628_1100_DHANSIRIGHAT`)
- **Unique Event Groups**: `11` (Only Observations 8 and 9 share an ongoing flood episode)
- **Data Leakage Check**: `PASS` (Monotonic cumulative windows, $t \le T_{event}$ strictly enforced)
- **Synthetic Records**: `0 (0.0%)`

---

## 3. Comprehensive Layer Taxonomy Audit (All 156 Bhuvan Layers)

Every catalogued layer from the 2021–2025 ISRO/NRSC Bhuvan archive was classified according to strict scientific criteria:

| Taxonomy Category | Count | Usable for ML? | Model Applicability | Forensic Reason |
| :--- | :---: | :---: | :--- | :--- |
| **`CURRENT_TIER1_ACQUIRED`** | **12** | **YES** | Option A & Option B | Verified dual sensor overlap; focused swath; active river & rain telemetry. |
| **`B) VALID_FOR_RAINFALL_ONLY_MODEL` (2021)** | **17** | **YES** | **Option B Only** | Valid Bhuvan flood raster + active CWC rainfall telemetry (1 to 151 records). River telemetry did not exist in 2021. |
| **`F) SENSOR_OUTAGE` (2022–2025)** | **21** | **YES (for Rain)** | **Option B Only** | Valid Bhuvan flood raster + active CWC rainfall telemetry. River sensor knocked offline during severe flood peak. |
| **`G) UNSAFE_OR_AMBIGUOUS` (Statewide BBox)** | **59** | **CONDITIONAL** | **Potential Option A** | Broad state bounding box ($\ge 4.5^\circ$ span); river & rain active, but true swath coverage over gauge unverified without downloading tiles. |
| **`D) INVALID_SPATIAL_MATCH`** | **37** | **NO** | Excluded | Swath restricted to Upper Assam (Lakhimpur/Dibrugarh) or Barak Valley outside the 3 river gauges. |
| **`C) VALID_LABEL_BUT_MISSING_PREDICTOR`** | **7** | **NO** | Excluded | CWC rainfall telemetry reported 0 valid records in 24h window (2 in 2021, 5 in 2022–2025). |
| **`E) INVALID_TEMPORAL_MATCH`** | **3** | **NO** | Excluded | Multi-week composite layers (e.g. `16-28`) with non-discrete observation timestamps. |
| **TOTAL ARCHIVE** | **156** | — | — | Complete census of official Bhuvan Assam flood archive (2021–2025). |

---

## 4. Event Diversity & Meteorological Grouping

In disaster ML, raw sample count is deceptive: 20 satellite passes during a single 10-day flood wave share the same soil saturation, antecedent runoff, and catchment state. Generalization requires sampling diverse meteorological regimes across seasons and years.

### Current 12-Observation Event Groups (11 Unique Groups):

| Event Group ID | Episode Description | Observations | Date Range | River Gauges Covered |
| :--- | :--- | :---: | :--- | :--- |
| `ASSAM_FLOOD_2022_05_FAKIRPARA` | May 2022 Pre-Monsoon Flood Wave | 1 | 2022-05-23 | NH15 Crossing Fakirpara Tangni |
| `ASSAM_FLOOD_2022_07_BOKO` | July 2022 Historic Flood Wave | 1 | 2022-07-06 | NH17 Crossing Boko |
| `ASSAM_FLOOD_2023_06_DHANSIRI` | June 2023 Peak Flood Wave | 1 | 2023-06-23 | NH15 Crossing Dhansirighat |
| `ASSAM_FLOOD_2023_07_DHANSIRI` | July 2023 Secondary Ponding | 1 | 2023-07-20 | NH15 Crossing Dhansirighat |
| `ASSAM_FLOOD_2023_08_BOKO` | August 2023 Late Monsoon Flood | 1 | 2023-08-31 | NH17 Crossing Boko |
| `ASSAM_FLOOD_2024_05_PREMONSOON` | May 2024 Pre-Monsoon Baseline (0 px) | 1 | 2024-05-31 | NH15 Crossing Dhansirighat |
| `ASSAM_FLOOD_2024_06_DHANSIRI_BASELINE` | June 2024 Basin Baseline (0 px) | 1 | 2024-06-07 | NH15 Crossing Dhansirighat |
| **`ASSAM_FLOOD_2024_07_DHANSIRI`** | **July 2024 Major Flood Wave (Rising + Peak)** | **2** | **2024-07-08 to 2024-07-16** | **NH15 Crossing Dhansirighat (613 px -> 3,756 px)** |
| `ASSAM_FLOOD_2024_07_BOKO` | July 2024 Severe Kamrup Flood | 1 | 2024-07-20 | NH17 Crossing Boko |
| `ASSAM_FLOOD_2025_06_DHANSIRI_EARLY` | June 2025 Early Monsoon Baseline (0 px) | 1 | 2025-06-11 | NH15 Crossing Dhansirighat |
| `ASSAM_FLOOD_2025_06_DHANSIRI_LATE` | June 2025 Regional Inundation Baseline (0 px) | 1 | 2025-06-28 | NH15 Crossing Dhansirighat |

Across the entire 156-layer archive, **28 distinct multi-day flood waves / periods** were identified from 2021 to 2025, confirming rich potential for expanded event diversity.

---

## 5. Sample Size Assessment & Statistical Feasibility

A scientifically rigorous assessment of sample size requirements for flood risk ML models:

### A. Current Sample Size Evaluation ($N = 12$)
- **Degrees of Freedom**: In a model with 5 input features (e.g., rainfall 24h, rainfall 72h, river stage change 24h, rate of rise, rolling baseline), degrees of freedom is $12 - 5 - 1 = 6$.
- **Sensitivity**: 1 misclassified sample changes accuracy by **8.33%** and F1-score by **~0.12**.
- **Evaluation Limits**: In 5-fold GroupKFold, test folds have only 1 to 2 samples, resulting in massive metric variance.
- **Verdict**: The current 12 samples are sufficient for **pipeline verification and schema validation**, but **insufficient for statistically meaningful model comparison or generalization**.

### B. Target Sample Size Thresholds
1. **Pipeline & Architectural Smoke Testing**: `10 – 15 samples` *(Current Status: Fully Met with 12 samples)*.
2. **Baseline Model Prototyping & Preliminary Feature Selection**: `40 – 60 samples` across `15 – 25 independent event episodes` *(Can be achieved by implementing Option B or screening Option A)*.
3. **Defensible Operational / Regional Generalization**: `100+ samples` across multiple hydrologic basins and seasons.

---

## 6. Model Dataset Architecture Options

Two distinct, scientifically valid model architectures are available for expansion:

### OPTION A: Dual-Sensor Model (CWC Rainfall + CWC River Stage + Flood Inundation Label)
- **Predictors**: Antecedent rainfall (6h, 24h, 72h, 168h) + River stage dynamics (relative change 24h, rate of rise).
- **Target Label**: Inundation presence ($0/1$) at gauge catchment tile.
- **Current Verified Samples**: `12` (Census of Tier-1 focused swaths).
- **Expansion Potential**: **Up to 59 additional candidate layers** (`STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE`).
- **Required Action to Expand**: Must systematically probe Bhuvan WCS for each of the 59 layers with gauge-centered 0.2° tiles to verify if the satellite swath actually covered the gauge and whether valid flood pixels exist.
- **Advantages**: Highest physical fidelity. River stage directly reflects basin routing and upstream tributary integration.
- **Limitations**: Limited by river gauge sensor outages during catastrophic flood peaks (21 layers lost) and datum shift complexities.

### OPTION B: Rainfall-Only Model (CWC Hourly Rainfall + Flood Inundation Label)
- **Predictors**: Multi-horizon antecedent rainfall accumulation (6h, 24h, 72h, 168h) across reporting telemetry stations.
- **Target Label**: Inundation presence ($0/1$) in river subcatchment.
- **Current Verified Samples**: `12`.
- **Expansion Potential**: **`38` proven additional layers** immediately available without ambiguity:
  - `17` layers from 2021 (valid Bhuvan rasters + active CWC rainfall telemetry; river telemetry starts in 2022).
  - `21` layers from 2022–2025 where river sensors failed during peak floods, but CWC rainfall stations were active.
- **Total Expanded Dataset**: **`50` verified empirical observations** across 2021–2025.
- **Advantages**: Robust to river sensor knockouts; enables 4 full monsoon seasons of training (2021–2025); statistical stability for 5-fold GroupKFold cross-validation.
- **Limitations**: Does not model upstream river channel stage or backwater hydraulic effects.

---

## 7. Comparative Model Option Matrix

| Feature / Metric | Option A (Dual-Sensor) | Option B (Rainfall-Only) |
| :--- | :---: | :---: |
| **Input Predictors** | Rainfall + River Stage Dynamics | Cumulative Rainfall Multi-Horizons |
| **Target Ground Truth** | ISRO Bhuvan GeoTIFF Inundation | ISRO Bhuvan GeoTIFF Inundation |
| **Current Usable Rows** | `12` | `12` |
| **Immediately Proven Additions**| `0` (Requires tile screening) | **`38`** (17 from 2021 + 21 river outages) |
| **Expanded Dataset Size** | `~25 – 35` (Estimated after screening 59) | **`50`** (Immediate verified census) |
| **Seasons Covered** | 2022 – 2025 (3.5 seasons) | 2021 – 2025 (5 full seasons) |
| **Vulnerability to Sensor Loss**| HIGH (Lost 21 peak flood events) | LOW (Rainfall network has redundancy) |
| **Recommended Role** | Gauge-specific hydraulic regression | Sub-basin catchment inundation classifier |

---

## 8. Final Safety Gate & Recommendation

```
CURRENT_OBSERVATIONS: 12
CURRENT_POSITIVE: 8
CURRENT_NEGATIVE: 4
UNIQUE_EVENT_GROUPS: 11
ADDITIONAL_VALID_CANDIDATES: 38 (Option B Proven) / up to 59 (Option A Conditional)
DUAL_SENSOR_CANDIDATES: 12 current (+ up to 59 conditional upon tile verification)
RAINFALL_ONLY_CANDIDATES: 50 total (12 current + 38 additional proven)
INVALID_OR_UNUSABLE: 47
SYNTHETIC_DATA: 0
FINAL_RECOMMENDATION: EXPAND_DATASET_FIRST
ML_TRAINING: NOT_STARTED
```
