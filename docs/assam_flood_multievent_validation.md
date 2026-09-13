# Assam Multi-Event Flood Ground-Truth Validation & Alignment Report

**Project**: RISK // INDIA — AI-Powered Disaster Risk Analyzer & Management System  
**Phase**: 7C — Multi-Event Real Flood Ground-Truth Acquisition & Alignment  
**Investigation Date**: September 12, 2026  
**Investigator**: Lead Data Forensics & Geospatial ML Engineer  
**Status**: COMPLETE — 10 REAL RASTERS ACQUIRED & ALIGNED  
**Flood Ground-Truth Acquisition Status**: **`READY`**  
**Multi-Event Dataset Status**: **`READY`**  
**Rainfall Alignment Status**: **`PARTIAL`** *(Intermittent telemetry transmission requiring multi-station catchment aggregation)*  
**River Alignment Status**: **`PARTIAL`** *(Datum shift across 2023/2024/2025 requires segment normalization; sensor outage in June 2022)*  
**Negative Labels Status**: **`NOT_STARTED`**  
**ML Training Status**: **`NOT_STARTED`**  
**Training Readiness**: `TRAINING_READY = False`

---

## 1. Executive Summary

In Phase 7C, the RISK // INDIA project successfully transitioned from the single-raster pilot of Phase 7B to a **multi-event, multi-year empirical ground-truth dataset** acquired directly from the official **ISRO / NRSC Bhuvan OGC Web Coverage Service (WCS)**.

### Key Forensic Achievements:
1. **Resolved Gauge Mismatch**:
   - Addressed the Phase 7B observation constraint. For 2021 observation `07/06/2021-06Hr`, `NH15 Crossing Fakirpara Tangni` was outside the satellite swath, triggering the fallback to `Nematighat`.
   - In Phase 7C, identified satellite layers directly covering `NH15 Crossing Fakirpara Tangni` across 2021, 2022, 2023, 2024, and 2025, restoring primary focus to the requested river-crossing gauge.
2. **Complete 5-Year Bhuvan Inventory**:
   - Discovered and indexed **156 discrete Assam flood observation layers** across 2021–2025 in the official Bhuvan GeoServer catalog.
   - Categorized into **100 Priority 1 layers** (dual CWC rainfall and river-stage overlap in 2022–2025) and **56 Priority 2 layers** (CWC rainfall overlap in 2021).
3. **Acquired 10 Distinct Real Flood Observations**:
   - Downloaded 10 genuine GeoTIFF coverages spanning all 5 years (2021 to 2025).
   - **9 Valid Real Flood Rasters** containing between **1,245 and 29,877 positive flood inundation pixels** per catchment grid.
   - **1 Valid Non-Inundated Baseline Raster** (`0` flood pixels on 2023-06-16 prior to flood surge), providing genuine negative training contrast.
4. **Deduplicated Event Architecture**:
   - Formulated **7 distinct disaster event groups** (`ASSAM_2021_EVENT_01` to `ASSAM_2025_EVENT_01`) linking multi-swath satellite passes to cohesive flood episodes.
5. **Rigorous Temporal & Spatial Matching**:
   - Evaluated 6h, 24h, 72h, and 168h antecedent precipitation and river-stage windows against actual CWC hourly CSV telemetry.

---

## 2. Event Discovery & Inventory Metrics

- **Total Historical Flood Observations Discovered (2021–2025)**: **156 layers**
  - **Year 2021**: 19 layers (Priority 2: CWC Rainfall available; River Level records begin 2022)
  - **Year 2022**: 41 layers (34 Priority 1: Dual Rain + River Overlap; 7 Priority 2)
  - **Year 2023**: 22 layers (14 Priority 1: Dual Rain + River Overlap; 8 Priority 2)
  - **Year 2024**: 35 layers (20 Priority 1: Dual Rain + River Overlap; 15 Priority 2)
  - **Year 2025**: 39 layers (32 Priority 1: Dual Rain + River Overlap; 7 Priority 2)
- **Total Rasters Acquired**: **10 distinct target rasters** *(plus 1 diagnostic border file from Phase 7B)*.
- **Failed Acquisitions**: **0 failed downloads** *(1 candidate layer was outside coverage envelope during initial probe and excluded)*.
- **Valid Flood Rasters**: **9 rasters** (flood pixels > 0).
- **Empty / Baseline Rasters**: **1 raster** (genuine non-flood observation: `assam_2023_06_16_18hr_fakirpara.tif`).
- **Years Represented**: **5 years** (2021, 2022, 2023, 2024, 2025).

---

## 3. Acquired Flood Rasters Master Table

All rasters are georeferenced in **EPSG:4326**, formatted as **512 \(\times\) 512** single-band 8-bit GeoTIFFs, and stored in [`datasets/raw/isro/flood_inundation/`](datasets/raw/isro/flood_inundation/):

| # | Event Group ID | Observation ID | Event Date & Time | Target Gauge | Inundation Pixels | Inundation Pct | Nearest Flood (m) | Validation Status | Overlap Priority |
| :---: | :--- | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | `ASSAM_2021_EVENT_01` | `OBS_2021_06_09_06HR` | 2021-06-09 06:00 | NH15 Crossing Fakirpara Tangni | **1,245** | 0.47% | 893.9 m | `VALID_REAL_FLOOD_RASTER` | Priority 2 |
| 2 | `ASSAM_2021_EVENT_02` | `OBS_2021_07_06_06HR` | 2021-07-06 06:00 | Nematighat | **2,349** | 0.90% | 806.5 m | `VALID_REAL_FLOOD_RASTER` | Priority 2 |
| 3 | `ASSAM_2022_EVENT_01` | `OBS_2022_05_19_18HR` | 2022-05-19 18:00 | NH17 Crossing Boko | **10,739** | 4.10% | 1,217.2 m | `VALID_REAL_FLOOD_RASTER` | Priority 1 |
| 4 | `ASSAM_2022_EVENT_02` | `OBS_2022_06_16_18HR` | 2022-06-16 18:00 | NH15 Crossing Fakirpara Tangni | **29,877** | 11.40% | 1,015.9 m | `VALID_REAL_FLOOD_RASTER` | Priority 1 |
| 5 | `ASSAM_2022_EVENT_02` | `OBS_2022_06_17_18HR` | 2022-06-17 18:00 | NH15 Crossing Fakirpara Tangni | **14,727** | 5.62% | 156.3 m | `VALID_REAL_FLOOD_RASTER` | Priority 1 |
| 6 | `ASSAM_2023_EVENT_01` | `OBS_2023_06_16_18HR` | 2023-06-16 18:00 | NH15 Crossing Fakirpara Tangni | **0** | 0.00% | *N/A (Dry)* | `EMPTY_RASTER` *(Baseline)* | Priority 1 |
| 7 | `ASSAM_2023_EVENT_01` | `OBS_2023_06_18_18HR` | 2023-06-18 18:00 | NH15 Crossing Fakirpara Tangni | **2,643** | 1.01% | 260.2 m | `VALID_REAL_FLOOD_RASTER` | Priority 1 |
| 8 | `ASSAM_2024_EVENT_01` | `OBS_2024_06_17_18HR` | 2024-06-17 18:00 | NH15 Crossing Fakirpara Tangni | **6,116** | 2.33% | 1,916.7 m | `VALID_REAL_FLOOD_RASTER` | Priority 1 |
| 9 | `ASSAM_2024_EVENT_01` | `OBS_2024_06_20_06HR` | 2024-06-20 06:00 | NH15 Crossing Fakirpara Tangni | **12,014** | 4.58% | 2,621.7 m | `VALID_REAL_FLOOD_RASTER` | Priority 1 |
| 10 | `ASSAM_2025_EVENT_01` | `OBS_2025_06_03_06HR` | 2025-06-03 06:00 | NH15 Crossing Fakirpara Tangni | **8,593** | 3.28% | 1,012.2 m | `VALID_REAL_FLOOD_RASTER` | Priority 1 |

---

## 4. Flood Event Deduplication & Grouping

Multiple satellite overpasses often capture consecutive stages of the same hydrometeorological event. Treating each overpass as an independent flood creates data leakage during ML cross-validation. Events were grouped based on spatial catchment contiguity and a temporal window of \(\le 72\text{ hours}\):

1. **`ASSAM_2021_EVENT_01`**: Early monsoon flood wave (June 9, 2021). Single pass over Darrang/Tangni basin.
2. **`ASSAM_2021_EVENT_02`**: Upper Brahmaputra flood surge (July 6, 2021) at Nematighat/Jorhat.
3. **`ASSAM_2022_EVENT_01`**: Severe pre-monsoon convective flood surge (May 19, 2022) affecting the Boko/Kamrup south bank corridor.
4. **`ASSAM_2022_EVENT_02`**: **Catastrophic June 2022 Assam Floods**. Multi-temporal satellite tracking:
   - Pass 1: `2022-06-16 18:00` (29,877 flood pixels — 11.4% catchment inundation peak).
   - Pass 2: `2022-06-17 18:00` (14,727 flood pixels — inundation recedes slightly, floodwater approaches within 156 meters of gauge structure).
5. **`ASSAM_2023_EVENT_01`**: June 2023 Flood Evolution:
   - Stage 1: `2023-06-16 18:00` (0 flood pixels — non-inundated pre-flood baseline).
   - Stage 2: `2023-06-18 18:00` (2,643 flood pixels — sudden flood wave arrival following heavy upstream rainfall).
6. **`ASSAM_2024_EVENT_01`**: June 2024 Flood Wave:
   - Stage 1: `2024-06-17 18:00` (6,116 flood pixels).
   - Stage 2: `2024-06-20 06:00` (12,014 flood pixels — cresting event).
7. **`ASSAM_2025_EVENT_01`**: Early monsoon inundation (June 3, 2025) with 8,593 inundated pixels around Fakirpara Tangni.

---

## 5. Temporal Alignment Analysis (CWC Datasets)

For each acquired observation, actual raw CWC telemetry records were analyzed across 4 standard antecedent accumulation windows: **6 hours, 24 hours, 72 hours, and 168 hours (7 days)**.

### 5.1 CWC River Stage Telemetry Overlap (`rwl_tel_hr_assam_999_2021_2025.csv`)

| Observation ID | Gauge | 6h Cov (%) | 24h Cov (%) | 72h Cov (%) | 168h Cov (%) | Mean Stage (m) | Forensic River Stage Finding |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `OBS_2021_06_09_06HR` | Fakirpara | 0.0% | 0.0% | 0.0% | 0.0% | *N/A* | Pre-dates dataset (telemetry began Jan 1, 2022). |
| `OBS_2021_07_06_06HR` | Nematighat | 0.0% | 0.0% | 0.0% | 0.0% | *N/A* | Pre-dates dataset; Nematighat is rain telemetry only. |
| `OBS_2022_05_19_18HR` | Boko | 0.0% | 0.0% | 0.0% | 0.0% | *N/A* | Telemetry transmission gap at Boko during May 2022. |
| `OBS_2022_06_16_18HR` | Fakirpara | 0.0% | 0.0% | 0.0% | 0.0% | *N/A* | **Sensor Outage**: Extreme flood submerged/knocked out gauge transmission. |
| `OBS_2022_06_17_18HR` | Fakirpara | 0.0% | 0.0% | 0.0% | 0.0% | *N/A* | Sensor outage continued during peak inundation. |
| `OBS_2023_06_16_18HR` | Fakirpara | 16.7% | 41.7% | 47.2% | 76.8% | 5.76 m | Relative stage datum (~5.76 m). |
| `OBS_2023_06_18_18HR` | Fakirpara | **100.0%** | **100.0%** | 80.6% | 70.8% | 5.76 m | 100% complete hourly records during flood onset. |
| `OBS_2024_06_17_18HR` | Fakirpara | **100.0%** | 75.0% | 84.7% | **92.3%** | 32.70 m | Local benchmark datum shift (~32.70 m). |
| `OBS_2024_06_20_06HR` | Fakirpara | **100.0%** | **100.0%** | **94.4%** | **92.9%** | 32.70 m | Exceptional data continuity (>92% across all windows). |
| `OBS_2025_06_03_06HR` | Fakirpara | **100.0%** | **100.0%** | **98.6%** | **99.4%** | 61.18 m | MSL datum shift (~61.18 m; range: 60.90–61.46 m). |

### 5.2 CWC Rainfall Telemetry Overlap (`rainfall_tel_hr_cwc_as_2021_2025.csv`)

Forensic analysis of the 31 active reporting CWC rain telemetry stations revealed:
1. **Station Proximity**: The nearest active reporting rain station to Fakirpara Tangni is `Dharamtul` (44.9 km south) and `DRF` (51.5 km northwest in Baksa).
2. **Transmission Reliability**: Telemetry transmission at individual remote rain stations exhibits intermittent gaps. While seasonal coverage is continuous, hourly record completeness varies by station:
   - For `OBS_2022_05_19_18HR` (Boko): Nearest rain station `Beki Road bridge` recorded **114.0 mm** in 16 active hourly readings within the 24h antecedent window.
   - For `OBS_2022_06_16_18HR` (Fakirpara): Catchment station `Kampur` recorded continuous rainfall totaling **53.5 mm** over the 72h window preceding the peak flood.
   - For `OBS_2021_06_09_06HR` (Fakirpara): 35.0 mm cumulative rain recorded over the 168h window.

---

## 6. Spatial Matching & Proximity Analysis

- **Target Geometries**: All downloaded rasters were acquired as \(0.20^\circ \times 0.20^\circ\) bounding boxes centered directly on the CWC gauge.
- **In-Grid Gauge Coordinates**:
  - `NH15 Crossing Fakirpara Tangni`: Lat `26.508333°N`, Lon `92.116389°E` \(\rightarrow\) Grid Pixel \((X=257, Y=255)\).
  - `NH17 Crossing Boko`: Lat `25.977500°N`, Lon `91.234167°E` \(\rightarrow\) Grid Pixel \((X=257, Y=257)\).
  - `Nematighat`: Lat `26.860300°N`, Lon `94.252200°E` \(\rightarrow\) Grid Pixel \((X=261, Y=255)\).
- **Proximity to Inundated Pixels**:
  - `OBS_2022_06_17_18HR`: Nearest flood pixel was only **156.3 meters** from the Fakirpara Tangni bridge structure.
  - `OBS_2023_06_18_18HR`: Nearest flood pixel was **260.2 meters** away.
  - `OBS_2021_06_09_06HR`: Nearest flood pixel was **893.9 meters** away.
  - `OBS_2025_06_03_06HR`: Nearest flood pixel was **1,012.2 meters** away.
- **Spatial Quality Assessment**: **HIGH**. In every positive observation, floodwaters lie within 0.15 to 2.6 km of the gauging structure, representing true riverine floodplain inundation without submerging the elevated bridge deck.

---

## 7. Data Quality & Forensic Obstacles

1. **CWC River Stage Datum Inconsistency (CRITICAL)**:
   - The raw telemetry for `NH15 Crossing Fakirpara Tangni` transitions between three completely distinct vertical datums:
     - 2022–2023: Relative zero-gauge staff stage (\(\approx 5.76\text{ m}\)).
     - 2024: Local survey bridge datum (\(\approx 32.70\text{ m}\)).
     - 2025: Geodetic Mean Sea Level (MSL) benchmark (\(\approx 61.18\text{ m}\)).
   - **Resolution Required Before ML**: Raw river level must NEVER be used as an unnormalized training predictor. Segment z-score normalization or relative anomaly difference \(\Delta H = H_t - \bar{H}_{\text{season}}\) must be applied.
2. **Sensor Knockouts During Catastrophic Peaks**:
   - During the June 16–17, 2022 flood, river gauge telemetry ceased reporting (0 valid readings), despite Bhuvan confirming 29,877 inundated pixels (11.4% of catchment). Severe floods frequently disable solar telemetry units or submerge transmitter enclosures.
3. **Rainfall Spatial Representativeness**:
   - The nearest reporting CWC rain gauge is 44.9 km from Fakirpara Tangni. Point-based rainfall at 45 km distance cannot capture localized convective cloudbursts without multi-station inverse distance weighting (IDW) or gridded IMD reanalysis augmentation.

---

## 8. Unresolved Issues & Critical Blockers

1. **Polygonization / Vectorization Not Performed**: In strict compliance with Phase 7C instructions, rasters remain as GeoTIFFs; vector polygon extraction (`gdal_polygonize`) has not yet been executed.
2. **Negative Label Sampling Not Performed**: `NEGATIVE_LABELS = NOT_STARTED`. Buffer zones of \(\pm 7\text{ days}\) and \(\ge 30\text{ km}\) must be applied before non-flood training samples are generated.
3. **ML Training Barred**: `TRAINING_READY = False`. Models must not be trained until feature tables with normalized river anomalies and gridded rainfall aggregates are formally constructed.

---

## 9. Final Phase 7C Status

- **`FLOOD_GROUND_TRUTH_ACQUISITION`**: **`READY`**
- **`MULTI_EVENT_DATASET`**: **`READY`**
- **`RAINFALL_ALIGNMENT`**: **`PARTIAL`** *(Intermittent single-station transmission requiring multi-station catchment weighting)*
- **`RIVER_ALIGNMENT`**: **`PARTIAL`** *(Multi-year datum shifts require segment normalization)*
- **`NEGATIVE_LABELS`**: **`NOT_STARTED`**
- **`ML_TRAINING`**: **`NOT_STARTED`**
- **`TRAINING_READY`**: **`FALSE`**
