# Forensic Data Verification & Audit Report — RISK // INDIA (Assam Flood Pilot)

**Phase**: 5B — Authoritative Dataset Forensic Verification & Correction  
**Date**: September 12, 2026  
**Auditor**: Lead Data Forensics & Geospatial ML Engineer  
**Status**: COMPLETE — ALL RAW DATASETS VERIFIED & AUDITED  

---

## 1. Executive Summary & Forensic Verdict

Following the initial acquisition of open-government hydrology and meteorology datasets for Assam under Phase 5, this forensic audit performed byte-level, line-level, and schema-level verification directly on the physical CSV files stored under `datasets/raw/`. 

### Key Findings:
1. **Source of Truth Established**: All analysis in this document is derived directly from raw files without fabrication, synthetic generation, or unverified assumptions.
2. **CWC Telemetry Rainfall (`rainfall_tel_hr_cwc_as_2021_2025.csv`)**:
   - Contains **137,659 total rows** across **40 stations** spanning 1,824 days (2021-01-01 to 2025-12-30).
   - **Critical Forensic Insight**: Exactly **31 active telemetry stations** contain **35,309 valid, non-null hourly rainfall records**. Exactly **9 stations** (e.g. Nematighat, Goalpara, Tezpur, Guwahati) have **100% NULL rainfall (102,350 rows)** because they are river stage gauge stations included in the portal export that do not have automated rain gauges.
   - **Quality Notice**: 1,097 records exhibit extreme values (> 100 mm/hr, up to 1,005 mm/hr), representing transmission corruptions that require quality control clipping/filtering.
3. **CWC Telemetry River Water Level (`rwl_tel_hr_assam_999_2021_2025.csv`)**:
   - Contains **78,212 total rows** across **3 highway bridge crossing telemetry gauges** (`NH15 Crossing Fakirpara Tangni`, `NH17 Crossing Boko`, `NH15 Crossing Dhansirighat`) spanning 1,355 days (2022-01-01 to 2025-09-17).
   - **Critical Forensic Insight**: Danger levels and warning levels are **NOT present** in the raw CSV (RL_of_zeroGauge and MeanSeaLevel are uniformly 0). 
   - **Sensor Transition Detected**: In 2022–2023, stations reported local river stage (medians 1.2–3.1m); in 2024–2025, telemetry shifted to bridge benchmark elevation / MSL (medians jumping to 30.4m, 32.7m, 50.2m, and 80.2m). 32 extreme glitch spikes (> 100m, max 1,018.6m) were detected.
4. **IMD District-wise Daily Rainfall (`rainfall_districtwise_daily_imd.csv`)**:
   - Contains **18,184 structured rows** (NOT 36,371 rows; previous count was artificially inflated by unescaped newlines inside CSV cells).
   - Covers **Pan-India across 39 States and UTs**; Assam accounts for **825 rows** (4.54%) across 33 districts.
   - **Critical Forensic Insight**: The date range is **2026-08-19 to 2026-09-12 (25 calendar days)**. It is an operational monsoon bulletin snapshot, NOT a historical 2021–2025 time-series. It has **0 days overlap** with the 2021–2025 CWC records and **CANNOT be used as historical training data**.
5. **Flood Ground Truth Status**:
   - `FLOOD LABEL = NOT YET AVAILABLE`. ISRO/NRSC Bhuvan satellite inundation vectors require manual GIS export. Water level threshold proxy cannot be directly applied without official CWC Danger Levels or datum-shift baseline normalization.

---

## 2. Raw File Inventory (Verified)

| File Name | Physical Size (Bytes) | Size (MB) | Parsed Row Count | Column Count | Verified Date Range | Temporal Span | Spatial Coverage | Verified Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `cwc/rainfall/rainfall_tel_hr_cwc_as_2021_2025.csv` | 19,171,861 | 18.28 MB | 137,659 | 20 | 2021-01-01 04:00 to 2025-12-30 01:00 | 1,824 Days (~5.0 Years) | Assam (40 stations; 31 active rain stations) | **Primary Predictor (Meteorological)** |
| `cwc/river_level/rwl_tel_hr_assam_999_2021_2025.csv` | 10,558,346 | 10.07 MB | 78,212 | 23 | 2022-01-01 20:00 to 2025-09-17 05:00 | 1,355 Days (~3.7 Years) | Assam (3 NH river crossing gauges) | **Primary Hydrological Predictor & Target** |
| `imd/rainfall_districtwise_daily_imd.csv` | 3,023,860 | 2.88 MB | 18,184 | 22 | 2026-08-19 to 2026-09-12 | 25 Days | National (39 States/UTs; 33 Assam districts, 825 rows) | **Operational Validation Benchmark Only** |

---

## 3. CWC Hourly Rainfall Forensic Analysis

### 3.1 Metadata & Schema
- **File**: `datasets/raw/cwc/rainfall/rainfall_tel_hr_cwc_as_2021_2025.csv`
- **Columns (20)**: `SlNo` (int64), `Station` (str), `Agency` (str), `State LGD Code` (int64), `State` (str), `District LGD Code` (int64), `District` (str), `Tehsil` (str), `Block` (str), `Village` (str), `River` (str), `Basin` (str), `Tributary` (str), `Subtributary` (str), `SubSubtributary` (str), `Local River` (str), `Latitude` (float64), `Longitude` (float64), `Data Acquisition Time` (str), `Telemetry Hourly Rainfall (mm)` (float64).
- **Missing Values**:
  - `Telemetry Hourly Rainfall (mm)`: 102,350 missing (74.35%).
  - All geospatial & administrative coordinates: 0 missing. (Placeholders `-` used for unpopulated sub-basin fields).

### 3.2 The 40 Stations Breakdown (31 Valid vs 9 Non-Telemetry)
Forensic auditing revealed why 74.35% of the rainfall records are null. CWC's export database queried stations across Assam, including 9 major river gauge sites that lack automated precipitation sensors:

#### Active Reporting Rainfall Stations (31 Stations, 35,309 Valid Records, 0% Nulls):
1. **AP Ghat** (Cachar): 2,833 valid rows (100% valid)
2. **BAHALPUR** (Dhubri): 457 valid rows (100% valid)
3. **Basudevthan** (Lakhimpur): 1,793 valid rows (100% valid)
4. **Beki Road bridge** (Barpeta): 2,692 valid rows (100% valid)
5. **Bokajan** (Karbi Anglong): 171 valid rows (100% valid)
6. **Chenimari (Khowang)** (Dibrugarh): 234 valid rows (100% valid)
7. **Chouldhowaghat** (Lakhimpur): 1,991 valid rows (100% valid)
8. **DRF** (Baksa): 1,094 valid rows (100% valid)
9. **Desangpani** (Sivasagar): 727 valid rows (100% valid)
10. **Dharamtul** (Marigaon): 167 valid rows (100% valid)
11. **Dholabazar** (Cachar): 2,012 valid rows (100% valid)
12. **Dholai** (Cachar): 30 valid rows (100% valid)
13. **Dillighat** (Dibrugarh): 62 valid rows (100% valid)
14. **Gelabil** (Golaghat): 1,043 valid rows (100% valid)
15. **Gharmura** (Hailakandi): 57 valid rows (100% valid)
16. **Golaghat** (Golaghat): 347 valid rows (100% valid)
17. **KANGKUBASTI** (Dhemaji): 108 valid rows (100% valid)
18. **Kampur** (Nagaon): 404 valid rows (100% valid)
19. **Karimganj** (Karimganj): 5,362 valid rows (100% valid)
20. **Kheronighat** (Karbi Anglong): 41 valid rows (100% valid)
21. **Kokrajhar** (Kokrajhar): 3,378 valid rows (100% valid)
22. **Lakhipur** (Cachar): 149 valid rows (100% valid)
23. **Manas N H Crossing** (Bongaigaon): 972 valid rows (100% valid)
24. **Margherita** (Tinsukia): 1,159 valid rows (100% valid)
25. **Mathanguri** (Baksa): 358 valid rows (100% valid)
26. **NT Road Crossing Jia-Bharali** (Sonitpur): 1,033 valid rows (100% valid)
27. **NT Road Crossing(Jiabharali)** (Sonitpur): 1,771 valid rows (100% valid)
28. **Neharkatia** (Dibrugarh): 186 valid rows (100% valid)
29. **Numaligarh** (Golaghat): 2,557 valid rows (100% valid)
30. **Sivasagar** (Sivasagar): 1,629 valid rows (100% valid)
31. **ghilamora** (Lakhimpur): 492 valid rows (100% valid)

#### Non-Telemetry Hydrological Stations (9 Stations, 102,350 Records, 100% Nulls):
- **Nematighat**: 24,274 rows (100% null)
- **Goalpara**: 21,162 rows (100% null)
- **Melabazar**: 14,722 rows (100% null)
- **Golokganj**: 12,325 rows (100% null)
- **Tezpur**: 9,486 rows (100% null)
- **Guwahati(D.C.Court)**: 7,157 rows (100% null)
- **Dhubri**: 4,961 rows (100% null)
- **Dibrugarh**: 4,168 rows (100% null)
- **NH RD Xing(Puthimari)**: 4,095 rows (100% null)

*Cleaning Rule*: Drop rows from the 9 inactive stations during ingestion. Retain the 31 active telemetry stations (35,309 records).

### 3.3 Statistical Distribution & Telemetry Characteristics
- **Valid Observations**: 35,309
- **Minimum**: 0.50 mm (Sensor tipping bucket activation threshold)
- **25th Percentile**: 0.50 mm
- **Median (50th)**: 1.50 mm
- **75th Percentile**: 6.00 mm
- **90th Percentile**: 21.00 mm
- **95th Percentile**: 48.00 mm
- **99th Percentile**: 305.96 mm
- **Maximum**: 1,005.00 mm
- **Negative Values**: 0
- **Zero Values**: 0 (CWC telemetry logs only when precipitation is detected)
- **Anomalies (> 100 mm/hr)**: 1,097 observations (e.g. Neharkatia logging 1,005 mm, Lakhipur logging 989 mm). In Indian climatology, single-hour rainfall exceeding 100–150 mm represents extreme cloudburst or sensor packet error. An automated threshold rule of `rainfall <= 150 mm/hr` must be enforced.

---

## 4. CWC Hourly River Water Level Forensic Analysis

### 4.1 Metadata & Schema
- **File**: `datasets/raw/cwc/river_level/rwl_tel_hr_assam_999_2021_2025.csv`
- **Columns (23)**: `SlNo` (int64), `Station` (str), `Agency` (str), `State LGD Code` (int64), `State` (str), `District LGD Code` (int64), `District` (str), `Tehsil` (str), `Block` (str), `Village` (str), `River` (str), `Basin` (str), `Tributary` (str), `Subtributary` (str), `SubSubtributary` (str), `Local River` (str), `Latitude` (float64), `Longitude` (float64), `Is_DischargeDataAvailable` (str), `RL_of_zeroGauge` (int64), `MeanSeaLevel` (int64), `Data Acquisition Time` (str), `River Water Level Telemetry Hourly (meter)` (float64).
- **Missing Values**:
  - `River Water Level Telemetry Hourly (meter)`: 1,844 missing (2.36%).
  - All other columns: 0 missing.
- **Danger & Warning Levels**: Not present in the raw data. `RL_of_zeroGauge` and `MeanSeaLevel` are uniformly recorded as `0`.

### 4.2 Gauge Breakdown & Sensor Drift / Datum Transition

| Gauge Name | District | Coordinates (Lat, Lon) | Total Records | Valid Records | Null Records (Pct) | Temporal Coverage |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **NH15 Crossing Fakirpara Tangni** | Darrang | 26.5083, 92.1164 | 36,460 | 34,920 | 1,540 (4.22%) | 2022-01-01 20:00 to 2025-09-17 05:00 |
| **NH17 Crossing Boko** | Kamrup Metro | 25.9775, 91.2342 | 25,254 | 24,951 | 303 (1.20%) | 2022-02-25 18:00 to 2025-05-07 09:30 |
| **NH15 Crossing Dhansirighat** | Udalguri | 26.6958, 92.2578 | 16,498 | 16,497 | 1 (0.01%) | 2022-02-26 17:00 to 2025-06-28 03:00 |

#### Annual Telemetry Transition (Stage vs MSL Datum Shift):
- **2022**: Fakirpara median 1.22m, Boko median 2.30m, Dhansirighat median 2.31m. (Gauges measuring local relative water stage).
- **2023**: Fakirpara median 1.56m, Boko median 6.66m, Dhansirighat median 3.15m. (Monsoon flood stage cresting).
- **2024**: Fakirpara median jumps to 32.70m, Boko median jumps to 7.90m–30.00m, Dhansirighat jumps to 30.38m. (System datum shifted to bridge benchmark or MSL).
- **2025**: Fakirpara median 32.70m (max 63.47m), Boko median 50.24m (max 694.28m), Dhansirighat median 80.22m (max 80.61m).
- **Sensor Spikes**: 32 observations exceed 100 meters (e.g., 624.67m, 871.86m, 1,018.65m). These are physical impossibilities indicating digital telemetry transmission bit corruption.

---

## 5. IMD District Rainfall Forensic Analysis

### 5.1 Verification of Row Count Discrepancy
- **Previous Report Claim**: 36,371 rows.
- **Actual Verified CSV Rows**: **18,184 rows**.
- **Root Cause**: The raw file contains literal carriage returns (`\r`) and newline (`\n`) characters within quoted string cells (notably in headers `Weekly \nActual`, `Cumulative \nCategory`, and cells like `From 01-08-2026 To 19-08-2026\r`). Line counting utilities (`wc -l` or basic file line readers) count these embedded newlines as separate rows. Standard RFC 4180 CSV parsers correctly recognize exactly 18,184 structured rows.

### 5.2 Climatological & Geographical Scope
- **States & UTs**: 39 across India (Pan-India dataset).
- **Assam Records**: Exactly **825 rows** (4.54% of dataset) across **33 districts** (Baksa, Barpeta, Biswanath, Bongaigaon, Cachar, Charaideo, Chirang, Darrang, Dhemaji, Dhubri, Dibrugarh, Dima Hasao, Goalpara, Golaghat, Hailakandi, Hojai, Jorhat, Kamrup, Kamrup Metro, Karbi Anglong, Karimganj, Kokrajhar, Lakhimpur, Majuli, Morigaon, Nagaon, Nalbari, Sivasagar, Sonitpur, South Salmara Mancachar, Tinsukia, Udalguri, West Karbi Anglong).
- **Date Range**: **2026-08-19 to 2026-09-12 (25 calendar days)** for all states and Assam.
- **Dataset Classification**: Operational daily monsoon bulletin snapshot, NOT historical data.

### 5.3 Historical ML Training Viability: **NO**
- **Mathematical Reason**: Temporal overlap with the historical CWC river level dataset (2022-01-01 to 2025-09-17) is **0 calendar days (0.00% overlap)**.
- **Role Reclassification**: Reclassified to **OPERATIONAL MONITORING VALIDATION ONLY**. It cannot be joined to the 2021–2025 training dataset.

---

## 6. Cross-Dataset Alignment & Compatibility Matrix

| Feature Dimension | CWC Telemetry Rainfall | CWC Telemetry River Water Level | IMD District-wise Daily Rainfall | Compatibility Status |
| :--- | :--- | :--- | :--- | :--- |
| **Temporal Coverage** | 2021-01-01 to 2025-12-30 | 2022-01-01 to 2025-09-17 | 2026-08-19 to 2026-09-12 | CWC Rain & RWL: **COMPATIBLE** (1,355 days overlap) <br> IMD vs CWC: **INCOMPATIBLE** (0 days overlap) |
| **Temporal Granularity** | Hourly (event-based tips) | Hourly (sub-hourly regular) | Daily aggregate | CWC files align directly at hourly resolution. |
| **Spatial Unit** | Point telemetry coordinates | Point bridge crossing coordinates | District administrative polygon | Direct station join yields 0 rows. Requires spatial proximity linkage. |
| **Spatial Matching** | 31 active stations | 3 highway bridge gauges | 33 Assam districts | Gauges located in Darrang, Kamrup Metro, Udalguri. Rainfall stations located in neighboring districts at 44–65 km. |

### Proximity Linkage (Nearest Rainfall Stations to River Gauges):
1. **NH15 Crossing Dhansirighat (Udalguri)**:
   - Tezpur (54.3 km), DRF Baksa (56.8 km), Dharamtul Marigaon (59.5 km), NT Road Crossing Jia-Bharali (63.0 km).
2. **NH15 Crossing Fakirpara Tangni (Darrang)**:
   - Dharamtul Marigaon (44.8 km), NH RD Xing Puthimari Kamrup (49.9 km), Guwahati DC Court (51.0 km), DRF Baksa (51.5 km).
3. **NH17 Crossing Boko (Kamrup Metropolitan)**:
   - Guwahati DC Court (56.3 km), NH RD Xing Puthimari (58.3 km), Goalpara (64.2 km), Beki Road Bridge (65.5 km).

---

## 7. Flood Label Feasibility & Hydrological Proxy Assessment

### 7.1 Status of Authoritative Satellite Polygons
- **Current Status**: `FLOOD LABEL = NOT YET AVAILABLE`
- ISRO/NRSC Bhuvan inundation shapefiles and hazard zonation layers require manual GIS download. No satellite labels currently exist in `datasets/raw/isro/`.

### 7.2 Feasibility of Hydrological Water Level Proxy
- **Exceedance Check (`water_level >= danger_level`)**:
  - Raw CWC CSV files omit `danger_level` and `warning_level`.
  - Applying a fixed numerical threshold across the entire time-series is **statistically invalid** due to the sensor datum transition from 2022–2023 (relative stage ~1–5m) to 2024–2025 (elevation ~30–80m).
- **Requirements for Defensible Hydrological Proxy**:
  1. Retrieve official CWC Danger Levels (DL) and High Flood Levels (HFL) published by Central Water Commission for these highway crossing bridges.
  2. Implement segmented normalization (separate z-score or min-max normalization for 2022–2023 stage vs 2024–2025 MSL).
  3. Define proxy flood label as `rate_of_rise > threshold` AND `normalized_level > 95th_percentile`.

---

## 8. Discrepancy Register (Previous Claims vs Verified Facts)

| # | Item | Previous Report Claim | Actual File Forensic Result | Impact & Correction Required |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **D1** | **IMD Row Count** | 36,371 rows | **18,184 parsed rows** | Correct all reports and metadata; discrepancy caused by unescaped newlines within CSV cells. |
| **D2** | **IMD Temporal Span** | 2021–2025 historical dataset | **2026-08-19 to 2026-09-12 (25 days)** | Reclassify IMD from historical predictor to operational validation benchmark. 0% overlap with CWC. |
| **D3** | **CWC Rainfall Nulls** | Not detailed / assumed uniform | **74.35% nulls (102,350 rows)** | Filter out the 9 non-telemetry river gauge stations; retain the 31 active rain stations (35,309 valid rows). |
| **D4** | **CWC RWL Date Range** | 2022-02-26 to 2025-01-31 | **2022-01-01 20:00 to 2025-09-17 05:00** | Extend verified time-series bounds by 8 months (1,355 total days). |
| **D5** | **CWC Danger Levels** | Implied available for thresholding | **Completely missing from CSV (0/null)** | Do not use hardcoded water level threshold without external CWC DL/HFL lookup or datum normalization. |
| **D6** | **CWC RWL Datum** | Assumed uniform stage | **Significant Datum Shift (Stage to MSL)** | Segment data: 2022–2023 (relative stage) vs 2024–2025 (MSL). Remove 32 transmission spikes > 100m. |
| **D7** | **CWC Rainfall Max** | Not audited | **1,005.0 mm/hr (1,097 rows > 100mm)** | Enforce quality control rule: clip or flag hourly rainfall exceeding 150 mm/hr. |

---

## 9. Data Quality & Cleaning Rules Required

1. **CWC Rainfall Filtering**:
   - Filter `Station` in 31 active stations list; drop 9 null stations.
   - Filter `Telemetry Hourly Rainfall (mm) <= 150.0 mm/hr`. Flag higher values as sensor errors.
2. **CWC River Water Level Cleaning**:
   - Filter `River Water Level Telemetry Hourly (meter) <= 100.0 m`. Drop the 32 transmission spikes.
   - Drop rows with null water level (1,844 rows, 2.36%).
   - Apply segmented normalization to account for the 2022–2023 vs 2024–2025 datum shift.
3. **Resampling & Regularization**:
   - Resample both datasets to strict hourly intervals (`1H`), filling dry hours with `0.0 mm` for active rain stations.
4. **Spatial Aggregation**:
   - Construct a catchment precipitation feature for each river gauge using Inverse Distance Weighting (IDW) of the nearest active rainfall stations.

---

## 10. Recommended Feature Engineering Strategy Given Actual Data

Given the 1,355 days of temporal overlap between CWC rainfall and river water levels:
1. **Antecedent Precipitation Index (API)**:
   - \(API_t = \sum_{k=1}^{n} \frac{P_{t-k}}{k}\) across 24h, 72h, and 168h windows.
2. **Lagged Cumulative Rainfall**:
   - Rolling sums: `rain_cum_6h`, `rain_cum_24h`, `rain_cum_72h`.
3. **River Stage Dynamics**:
   - Rate of rise: \(\Delta H = H_t - H_{t-1}\).
   - Relative stage deviation from 14-day rolling baseline: \(H_t - \mu_{14d}\).
4. **Seasonal Sinusoidal Features**:
   - Day of year cyclical encodings: \(\sin(2\pi \cdot \text{DOY} / 365)\), \(\cos(2\pi \cdot \text{DOY} / 365)\) to capture monsoon seasonality.

---

## 11. ML Readiness Verdict

### **CONDITIONAL GO (HYDROLOGICAL LEVEL PREDICTION ONLY)**
- **Hydrological Stage / Rate-of-Rise Modeling**: **GO**. With 76,368 valid water level records and 35,309 valid rainfall records overlapping for 1,355 days, training a river stage dynamics regression or rate-of-rise alert model is mathematically defensible and feasible.
- **Binary Flood Inundation Classification**: **NO-GO**. Because `FLOOD LABEL = NOT YET AVAILABLE` (ISRO satellite inundation masks pending export, and CWC Danger Levels missing from telemetry files), training a spatial inundation classifier would require fabricating labels, which violates project integrity principles.

---

## 12. Concrete Next Steps for Phase 6

1. Implement the preprocessing pipeline in `ml/data/` implementing the cleaning rules and station filters.
2. Acquire official CWC published Danger Levels / High Flood Levels for the 3 highway crossing gauges from the CWC Flood Forecasting portal.
3. Build the Inverse Distance Weighting (IDW) geospatial alignment module linking the 31 active rain stations to the 3 river gauges.
4. If satellite labels are obtained from ISRO Bhuvan, ingest vector polygons into `datasets/raw/isro/` to form spatial ground truth.
