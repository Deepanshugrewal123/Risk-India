# Model Card — Assam Flood Tabular ML Prototype
**Model Identifier:** `assam_flood_prototype_v1`  
**Model Family:** Regularized Logistic Regression  
**Framework:** scikit-learn 975 bytes (`Pipeline` + `StandardScaler`)  
**Release Date:** 2026-09-13  
**Development Phase:** Phase 8 Prototype  

---

## 1. Model Overview & Purpose

### Model Purpose
A proof-of-concept tabular classification prototype designed to evaluate whether contemporaneous and antecedent telemetry from the **Central Water Commission (CWC)** (hourly rainfall and river stage) can predict riverine flood inundation detected in **ISRO/NRSC Bhuvan** historical satellite flood GeoTIFF rasters.

### Intended Use
- **Research & Development:** Testing tabular feature representations, event-group cross-validation, and hydrometric signal correlation.
- **Proof-of-Concept Benchmarking:** Establishing a rigorous quantitative baseline before scaling data collection.

### Explicit Non-Intended Uses
> [!CAUTION]
> - **NOT FOR OPERATIONAL EMERGENCY WARNING:** This model is an early research prototype and MUST NOT be used for life-critical evacuation decisions, disaster management commands, or public warning sirens.
> - **NOT A NATIONWIDE MODEL:** This model is strictly calibrated on 3 gauge catchments in Assam and has NOT been tested on other Indian river basins (e.g. Ganges, Mahanadi, Godavari, Krishna).

---

## 2. Training Data & Provenance

- **Geographic Scope:** Assam, India (Brahmaputra River Valley).
- **Monitoring Gauges:**
  1. `NH15 Crossing Dhansirighat` (Udalguri District; $26.6958^\circ\text{N}, 92.2578^\circ\text{E}$)
  2. `NH15 Crossing Fakirpara Tangni` (Darrang District; $26.5083^\circ\text{N}, 92.1164^\circ\text{E}$)
  3. `NH17 Crossing Boko` (Kamrup District; $25.9775^\circ\text{N}, 91.2342^\circ\text{E}$)
- **Total Observations ($N$):** **32**
- **Target Distribution:**
  - Positive Inundation ($y=1$): **18** (56.25%)
  - Negative Non-Flood Baseline ($y=0$): **14** (43.75%)
- **Independent Hydrological Event Groups:** **18**
- **Temporal Span:** 2022-05-23 to 2025-07-08 (1,141.5 days across 4 monsoon seasons).
- **Data Leakage Check:** ZERO future data leakage ($t \le T_{event}$ strictly enforced).

---

## 3. Features & Inputs

The model ingests **13 continuous numerical predictors**:
1. `rainfall_6h`: 6-hour antecedent precipitation sum (mm)
2. `rainfall_24h`: 24-hour antecedent precipitation sum (mm)
3. `rainfall_72h`: 72-hour antecedent precipitation sum (mm)
4. `rainfall_168h`: 168-hour (7-day) antecedent precipitation sum (mm)
5. `river_rise_6h`: 6-hour water level difference (m)
6. `river_rise_24h`: 24-hour water level difference (m)
7. `river_level_relative`: Stage relative to operational season minimum (m)
8. `river_percentile_level`: Empirical percentile of stage within season ($[0.0, 1.0]$)
9. `month`: Observation calendar month ($5 - 8$)
10. `day_of_year_sin`: Cyclical sine of day of year
11. `day_of_year_cos`: Cyclical cosine of day of year
12. `latitude`: Decimal latitude of gauge ($^\circ\text{N}$)
13. `longitude`: Decimal longitude of gauge ($^\circ\text{E}$)

*Excluded/Documented Unavailable:* `elevation`, `slope`, `distance_to_river` (100% missing in raw telemetry; strictly retained as NaN without fabrication).

---

## 4. Evaluation Strategy & Performance

### Cross-Validation Strategy
- **5-Fold `GroupKFold` grouped by `event_group_id`**.
- Multi-pass snapshots of the same flood wave are strictly sequestered into the same fold, completely preventing data leakage across train and validation partitions.

### Quantitative Performance Metrics

| Evaluation Metric | 5-Fold OOF Overall | 5-Fold Mean $\pm$ Std | Random Forest Baseline | Gradient Boosting Baseline |
| :--- | :---: | :---: | :---: | :---: |
| **Accuracy** | **0.5000** | $0.5067 \pm 0.165$ | 0.3750 | 0.3750 |
| **Recall (Sensitivity)** | **0.5556** | $0.5333 \pm 0.403$ | 0.4444 | 0.5556 |
| **Precision** | **0.5556** | $0.5476 \pm 0.334$ | 0.4444 | 0.4545 |
| **F1-Score** | **0.5556** | $0.4633 \pm 0.309$ | 0.4444 | 0.5000 |
| **ROC-AUC** | **0.4286** | $0.4750 \pm 0.316$ | 0.2937 | 0.2619 |
| **PR-AUC** | **0.5476** | $0.5583 \pm 0.287$ | 0.4757 | 0.4544 |
| **False Negative Rate (Miss Rate)** | **0.4444** | — | 0.5556 | 0.4444 |
| **False Positive Rate (False Alarm)**| **0.5714** | — | 0.7143 | 0.8571 |

### Confusion Matrix (Out-of-Fold, $N=32$):
- **True Positives (TP):** 10
- **True Negatives (TN):** 6
- **False Positives (FP):** 8
- **False Negatives (FN):** 8

---

## 5. Known Limitations & Biases

1. **Extremely Small Sample Size ($N=32$ across 18 events):**
   - High fold-to-fold variance in metrics. Tree-based ensembles overfit on training folds ($N \approx 25$).
2. **Spatial Concentration:**
   - 25 of 32 observations originate from a single gauge basin (`NH15 Crossing Dhansirighat`). Spatial coordinates act partly as station identifiers.
3. **Monsoon-Only Domain:**
   - All samples originate between May and August. The model has zero exposure to post-monsoon or dry season conditions.
4. **CWC River Datum Complexity:**
   - Although $\Delta_{24h}$ and percentile normalization mitigate datum shifts, uncalibrated absolute river gauge height cannot be directly utilized.

---
*Model Card compliant with standard ML Governance & Quality Guidelines.*
