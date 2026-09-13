# Assam Flood Pilot — ML Label Construction & Quality Report

**Project**: RISK // INDIA — AI-Powered Disaster Risk Analysis Platform  
**Phase**: Phase 7F — Construct Real Assam Flood ML Label Dataset  
**Report Generated**: `2026-09-12 23:38:30 IST`  
**Dataset Path**: [`datasets/processed/flood_assam/labels.csv`](datasets/processed/flood_assam/labels.csv)  
**Metadata Path**: [`datasets/processed/flood_assam/label_metadata.json`](datasets/processed/flood_assam/label_metadata.json)  
**Quality Gate Validator**: [`ml/data/validate_flood_labels.py`](ml/data/validate_flood_labels.py)  
**Status**: **`READY_FOR_MODEL_DEVELOPMENT`**  
**ML Training**: **`NOT STARTED`**

---

## 1. Dataset Summary

The first real, machine-learning-ready flood ground-truth label dataset for the RISK // INDIA Assam flood pilot has been constructed and forensically validated.

- **Total Label Observations**: `12`
- **Positive Flood Labels (`1`)**: `8`
- **Negative Baseline Labels (`0`)**: `4`
- **Unresolved Labels**: `0`
- **High Confidence Labels**: `11`
- **Review Required Labels**: `1` (`BHUVAN_ASSAM_20250628_1100_DHANSIRIGHAT`)
- **Unit of Analysis**: `ONE_SAMPLE_PER_EVENT_GAUGE_WINDOW` (Catchment tile 20 km × 20 km around active CWC telemetry crossing gauge). Individual pixels are strictly **not** treated as independent observations to prevent artificial sample inflation.
- **Synthetic / Fabricated Data**: `0 (0.0%)`

---

## 2. Complete Training Label Table (`labels.csv`)

| # | Observation ID | Event Group | Event Timestamp | Gauge Name | Flood Label | Flood Pixels | Pixel % | Rain (24h) | River (24h) | River Datum | River Flag | Quality Status |
| :-: | :--- | :--- | :--- | :--- | :-: | :-: | :-: | :-: | :-: | :--- | :--- | :--- |
| 01 | `BHUVAN_ASSAM_20220523_1800_FAKIRPARA` | `ASSAM_FLOOD_2022_05_FAKIRPARA` | `2022-05-23 18:00` | NH15 Crossing Fakirpara Tangni | **`1`** | 744 | 0.28% | 2 rows | 8h | `RELATIVE_GAUGE_ZERO` | `CONTINUOUS` | `HIGH_CONFIDENCE` |
| 02 | `BHUVAN_ASSAM_20220706_1800_BOKO` | `ASSAM_FLOOD_2022_07_BOKO` | `2022-07-06 18:00` | NH17 Crossing Boko | **`1`** | 4,261 | 1.63% | 8 rows | 19h | `RELATIVE_GAUGE_ZERO` | `CONTINUOUS` | `HIGH_CONFIDENCE` |
| 03 | `BHUVAN_ASSAM_20230623_1800_DHANSIRIGHAT` | `ASSAM_FLOOD_2023_06_DHANSIRI` | `2023-06-23 18:00` | NH15 Crossing Dhansirighat | **`1`** | 21,610 | 8.24% | 1 rows | 25h | `RELATIVE_GAUGE_ZERO` | `CONTINUOUS` | `HIGH_CONFIDENCE` |
| 04 | `BHUVAN_ASSAM_20230720_0600_DHANSIRIGHAT` | `ASSAM_FLOOD_2023_07_DHANSIRI` | `2023-07-20 06:00` | NH15 Crossing Dhansirighat | **`1`** | 6 | 0.002% | 1 rows | 25h | `RELATIVE_GAUGE_ZERO` | `CONTINUOUS` | `HIGH_CONFIDENCE` |
| 05 | `BHUVAN_ASSAM_20230831_1800_BOKO` | `ASSAM_FLOOD_2023_08_BOKO` | `2023-08-31 18:00` | NH17 Crossing Boko | **`1`** | 4,449 | 1.70% | 11 rows | 23h | `RELATIVE_GAUGE_ZERO` | `CONTINUOUS` | `HIGH_CONFIDENCE` |
| 06 | `BHUVAN_ASSAM_20240531_1800_DHANSIRIGHAT` | `ASSAM_FLOOD_2024_05_PREMONSOON` | `2024-05-31 18:00` | NH15 Crossing Dhansirighat | **`0`** | 0 | 0.0% | 3 rows | 25h | `DATUM_RECLASSIFIED_LOCAL` | `CONTINUOUS` | `HIGH_CONFIDENCE` |
| 07 | `BHUVAN_ASSAM_20240607_1100_DHANSIRIGHAT` | `ASSAM_FLOOD_2024_06_DHANSIRI_BASELINE` | `2024-06-07 11:00` | NH15 Crossing Dhansirighat | **`0`** | 0 | 0.0% | 9 rows | 25h | `DATUM_RECLASSIFIED_LOCAL` | `CONTINUOUS` | `HIGH_CONFIDENCE` |
| 08 | `BHUVAN_ASSAM_20240708_1000_DHANSIRIGHAT` | `ASSAM_FLOOD_2024_07_DHANSIRI` | `2024-07-08 10:00` | NH15 Crossing Dhansirighat | **`1`** | 613 | 0.23% | 1 rows | 25h | `DATUM_RECLASSIFIED_LOCAL` | `CONTINUOUS` | `HIGH_CONFIDENCE` |
| 09 | `BHUVAN_ASSAM_20240716_1800_DHANSIRIGHAT` | `ASSAM_FLOOD_2024_07_DHANSIRI` | `2024-07-16 18:00` | NH15 Crossing Dhansirighat | **`1`** | 3,756 | 1.43% | 1 rows | 25h | `DATUM_RECLASSIFIED_LOCAL` | `CONTINUOUS` | `HIGH_CONFIDENCE` |
| 10 | `BHUVAN_ASSAM_20240720_0600_BOKO` | `ASSAM_FLOOD_2024_07_BOKO` | `2024-07-20 06:00` | NH17 Crossing Boko | **`1`** | 4,275 | 1.63% | 6 rows | 25h | `DATUM_RECLASSIFIED_LOCAL` | `CONTINUOUS` | `HIGH_CONFIDENCE` |
| 11 | `BHUVAN_ASSAM_20250611_1000_DHANSIRIGHAT` | `ASSAM_FLOOD_2025_06_DHANSIRI_EARLY` | `2025-06-11 10:00` | NH15 Crossing Dhansirighat | **`0`** | 0 | 0.0% | 1 rows | 25h | `MSL_NORMALIZED` | `CONTINUOUS` | `HIGH_CONFIDENCE` |
| 12 | `BHUVAN_ASSAM_20250628_1100_DHANSIRIGHAT` | `ASSAM_FLOOD_2025_06_DHANSIRI_LATE` | `2025-06-28 11:00` | NH15 Crossing Dhansirighat | **`0`** | 0 | 0.0% | 2 rows | 17h | `MSL_NORMALIZED` | `GAP_AT_EVENT_HR` | `REVIEW_REQUIRED` |

---

## 3. Label Provenance & Assignment Definitions

### A. Label Provenance
All ground-truth labels originate directly from the official **National Remote Sensing Centre (NRSC) / Indian Space Research Organisation (ISRO) Bhuvan Historical Flood Inundation service**.
- OGC WCS Endpoint: `https://bhuvan-gp1.nrsc.gov.in/bhuvan/wcs`
- Spatial format: Little-Endian single-band GeoTIFF in EPSG:4326.
- Raw file preservation: Stored immutably under [`datasets/raw/isro/flood_inundation/`](datasets/raw/isro/flood_inundation/).

### B. Positive Label Definition (`flood_label = 1`)
A sample is assigned `flood_label = 1` if and only if:
1. The raster was acquired during an active ISRO Bhuvan historical flood observation layer.
2. Binary pixel value `1` is present within the 20km gauge catchment tile (`flood_pixel_count > 0`), which according to official Bhuvan GeoServer SLD Style (`recentfloods`) strictly represents active flood water inundation (Cyan `#00FFFF`).
3. The observation has verified simultaneous CWC river stage uptime and active CWC rainfall telemetry.
4. The spatial footprint overlaps the verified gauge catchment.

### C. Negative Label Definition (`flood_label = 0`)
Negative labels were **not** synthetically generated or arbitrarily inferred. A sample is assigned `flood_label = 0` if and only if:
1. The official satellite raster for that observation timestamp contains exactly **`0` flood pixels** (`flood_pixel_count == 0`) across all 262,144 pixels in the 20km tile.
2. The raster has valid georeferencing, single-band format, and confirmed zero-inundation SLD semantics (`value 0` = background/within-bank land).
3. A controlled diagnostic query with a wider **50 km × 50 km** window verified that:
   - For **June 7, 2024** and **June 11, 2025**: `0` flood pixels exist across the entire 50km Dhansiri basin.
   - For **May 31, 2024**: River was within natural channel banks (3.258m stage); the 42 flood pixels in the 50km tile were >22 km away in the lower Brahmaputra plain.
   - For **June 28, 2025**: River channel was within banks at the gauge; 1,014 flood pixels were ~15 km east in the neighboring Pachnoi/Rowta river reach.
4. The sample provides crucial empirical negative contrast (within-bank normal/baseline river conditions) without synthetic fabrication.

---

## 4. Event Grouping & Collinearity Controls

Treating multiple satellite observations from the same ongoing flood wave as independent training samples would introduce severe collinearity and data leakage during cross-validation. Therefore, `event_group_id` is maintained alongside `observation_id`:

| Event Group ID | Episode Description | Observations Included | Temporal Span |
| :--- | :--- | :-: | :--- |
| `ASSAM_FLOOD_2022_05_FAKIRPARA` | May 2022 Pre-Monsoon Flood Wave | 1 (Obs 1) | May 23, 2022 |
| `ASSAM_FLOOD_2022_07_BOKO` | July 2022 Major Brahmaputra Flood | 1 (Obs 2) | July 6, 2022 |
| `ASSAM_FLOOD_2023_06_DHANSIRI` | June 2023 Peak Inundation Wave | 1 (Obs 3) | June 23, 2023 |
| `ASSAM_FLOOD_2023_07_DHANSIRI` | July 2023 Secondary Recession Ponding | 1 (Obs 4) | July 20, 2023 |
| `ASSAM_FLOOD_2023_08_BOKO` | August 2023 Boko Flood Swath | 1 (Obs 5) | August 31, 2023 |
| `ASSAM_FLOOD_2024_05_PREMONSOON` | May 2024 Pre-Monsoon Transition Baseline | 1 (Obs 6) | May 31, 2024 |
| `ASSAM_FLOOD_2024_06_DHANSIRI_BASELINE` | June 2024 Regional Baseline | 1 (Obs 7) | June 7, 2024 |
| **`ASSAM_FLOOD_2024_07_DHANSIRI`** | **July 2024 Major Flood Wave (Multi-Pass)** | **2 (Obs 8 & 9)** | **July 8 to July 16, 2024 (Rising limb to peak limb)** |
| `ASSAM_FLOOD_2024_07_BOKO` | July 2024 Boko Inundation Wave | 1 (Obs 10) | July 20, 2024 |
| `ASSAM_FLOOD_2025_06_DHANSIRI_EARLY` | June 2025 Early Monsoon Baseline | 1 (Obs 11) | June 11, 2025 |
| `ASSAM_FLOOD_2025_06_DHANSIRI_LATE` | June 2025 Regional Inundation Baseline | 1 (Obs 12) | June 28, 2025 |

> [!IMPORTANT]
> When splitting this dataset into training and evaluation sets, **GroupKFold** or **Leave-One-Group-Out** on `event_group_id` must be used rather than random K-Fold to prevent test data leakage.

---

## 5. Temporal Predictor Windows & Strict Leakage Controls

### A. Preceding Observation Availability

| Observation ID | River 6h | River 24h | River 72h | River 168h | Rain Near (24h) | Rain Network (24h) |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: |
| `BHUVAN_ASSAM_20220523_1800_FAKIRPARA` | 1h | 8h | 15h | 44h | 2 rows | 35 rows |
| `BHUVAN_ASSAM_20220706_1800_BOKO` | 7h | 19h | 19h | 19h | 8 rows | 121 rows |
| `BHUVAN_ASSAM_20230623_1800_DHANSIRIGHAT` | 7h | 25h | 73h | 153h | 1 rows | 12 rows |
| `BHUVAN_ASSAM_20230720_0600_DHANSIRIGHAT` | 7h | 25h | 73h | 161h | 1 rows | 11 rows |
| `BHUVAN_ASSAM_20230831_1800_BOKO` | 7h | 23h | 46h | 122h | 11 rows | 13 rows |
| `BHUVAN_ASSAM_20240531_1800_DHANSIRIGHAT` | 7h | 25h | 70h | 165h | 3 rows | 75 rows |
| `BHUVAN_ASSAM_20240607_1100_DHANSIRIGHAT` | 7h | 25h | 73h | 167h | 9 rows | 29 rows |
| `BHUVAN_ASSAM_20240708_1000_DHANSIRIGHAT` | 7h | 25h | 71h | 163h | 1 rows | 20 rows |
| `BHUVAN_ASSAM_20240716_1800_DHANSIRIGHAT` | 7h | 25h | 73h | 153h | 1 rows | 47 rows |
| `BHUVAN_ASSAM_20240720_0600_BOKO` | 7h | 25h | 73h | 168h | 6 rows | 10 rows |
| `BHUVAN_ASSAM_20250611_1000_DHANSIRIGHAT` | 7h | 25h | 73h | 169h | 1 rows | 2 rows |
| `BHUVAN_ASSAM_20250628_1100_DHANSIRIGHAT` | 0h | 17h | 66h | 83h | 2 rows | 3 rows |

### B. Leakage Controls
- All predictor queries enforce `acquisition_time <= event_timestamp`.
- Absolutely no future observation (`T + 1h`, `T + 24h`) is accessible to predictor windows.
- In `ml/data/validate_flood_labels.py`, monotonicity across cumulative windows (`records(6h) <= records(24h) <= records(72h) <= records(168h)`) is strictly enforced and verified.

---

## 6. Spatial Association & River Datum Architecture

### A. Rainfall Spatial Association
- **Deterministic Nearest Station**:
  - `NH15 Crossing Fakirpara Tangni` -> `Kampur` (71 km)
  - `NH17 Crossing Boko` -> `Beki Road bridge` (67 km)
  - `NH15 Crossing Dhansirighat` -> `DRF` (63 km) / `NT Road Crossing(Jiabharali)` (70 km)
- **Secondary Network Context**: Total valid active rainfall telemetry rows across the Assam reporting network in the 24h window are stored to provide regional meteorological context.

### B. River Datum Shift Preservation
- In 2022–2023: CWC stages reported relative to local gauge zero (`~0.29m - 2.55m`).
- In 2024: Gauge datum shifted locally (`~30m - 31m`).
- In 2025: Gauge datum normalized to Mean Sea Level (MSL) (`~79m - 80m`).
- **Standard Modeling Rule**: Raw river water level must **never** be used directly across years. Instead, relative change features (e.g. `stage_delta_24h = stage(T) - stage(T-24h)` or `rate_of_rise`) must be computed within each datum regime.

---

## 7. Known Scientific Limitations

> [!WARNING]
> This dataset is formally designated as the **"Assam Flood Pilot — Research Dataset"**. Its limitations are explicitly documented:
> 
> 1. **Sample Size**: Contains 12 discrete satellite observation windows (8 positive, 4 negative). It is suited for benchmark formulation and preliminary feature testing, not nationwide deep learning.
> 2. **Regional Pilot Scope**: Restricted strictly to 3 verified crossing gauges in Assam.
> 3. **Satellite Pass Intermittency**: Satellite observations represent discrete temporal snapshots, not continuous inundation hydrographs.
> 4. **CWC Station Sparsity**: Nearest active rainfall telemetry stations are 63 km to 71 km from the river gauges due to the exclusion of 9 non-reporting CWC rainfall stations.
> 5. **Local Non-Inundation**: The 4 negative labels confirm that the river was within banks *inside the 20km gauge catchment window*. They do not imply that other remote districts of Assam were flood-free on those dates.
> 6. **Datum Shifts**: Features must be trained on relative level dynamics rather than absolute river stage meters.

---

## 8. Final Quality Gate

```
TOTAL_LABEL_OBSERVATIONS: 12
POSITIVE_LABELS: 8
NEGATIVE_LABELS: 4
UNRESOLVED: 0
HIGH_CONFIDENCE_LABELS: 11
DUPLICATE_OBSERVATIONS: 0
SYNTHETIC_RECORDS: 0
LEAKAGE_CHECK: PASS
LABEL_VALIDATION: PASS
DATASET_STATUS: READY_FOR_MODEL_DEVELOPMENT
ML_TRAINING: NOT_STARTED
```
