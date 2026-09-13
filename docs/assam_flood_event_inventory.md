# Assam Historical Flood Event Inventory (2021–2025)

**Source**: National Remote Sensing Centre (NRSC), ISRO / Bhuvan Historical Floods Service  
**Service Base URL**: `https://bhuvan-gp1.nrsc.gov.in/bhuvan/wcs`  
**Web Viewer Reference**: `https://bhuvan-app1.nrsc.gov.in/disaster/usrtasks/flood/flood.php`  
**Inventory Date**: September 12, 2026  
**Total Discovered Assam Observations (2021–2025)**: **156 layers**  

---

## 1. Executive Prioritization Summary (Audited & Corrected in Phase 7C-A)

> [!IMPORTANT]
> **PHASE 7C-A INDEPENDENT AUDIT CORRECTION**:
> The previous preliminary categorization naively marked 100 candidate layers as "Priority 1" based solely on whether Bhuvan's layer zoom bounding box encompassed the coordinates of the 3 CWC river gauges.
> A strict forensic cross-source audit conducted in [`docs/assam_flood_overlap_audit.md`](docs/assam_flood_overlap_audit.md) against raw CWC hourly CSV files revealed that:
> 1. **59 candidate layers** declare generic state-level bounding boxes (\(\ge 4.5^\circ\) span), where catchment-scale swath coverage is unconfirmed.
> 2. **21 candidate layers** intersect river gauges but experienced **river telemetry sensor knockouts** (0 valid stage readings, such as during the peak disaster wave of June 16–17, 2022).
> 3. **37 candidate layers** are regional swaths covering Eastern Assam / Barak Valley that do not intersect any river gauges.
> 4. Exactly **12 layers** possess **`VERIFIED_DUAL_OVERLAP`** (focused satellite footprint \(\le 3^\circ\) span + active river-stage telemetry + active rainfall telemetry).

| Priority Tier | Description & Audited Overlap Criteria | Preliminary Layer Count | Verified Focused Swaths (Audit) | Candidate Acquisition Actions |
| :---: | :--- | :---: | :---: | :--- |
| **Priority 1 (Verified Core)** | **2022–2025 Focused Swaths**: Genuine focused satellite footprint overlapping a verified CWC river gauge with non-null river-stage AND active CWC rainfall telemetry. | 100 *(preliminary)* | **12 layers** | **TIER-1 PRIMARY ML GROUND TRUTH** — Scientifically defensible dual-sensor ground truth. |
| **Priority 1 (Statewide Envelope)** | Broad state-level bounding box (\(\ge 4.5^\circ\) span); river telemetry was active, but true satellite swath extent is unconfirmed at gauge level. | — | **59 layers** | **TIER-2 CONDITIONAL CANDIDATES** — Requires raster boundary verification before training. |
| **Priority 1 (Sensor Outage)** | Layer footprint intersects gauge, but river sensor reported 0 valid readings during event peak. | — | **21 layers** | **EXCLUDED FROM STAGE REGRESSION** — Usable only for rainfall-inundation classification. |
| **Priority 2** | **2021 Events**: CWC hourly rainfall telemetry exists (2021–2025), but CWC river-level telemetry does not yet exist (begins 2022-01-01). | **56 layers** | **56 layers** | **METEOROLOGICAL RUNOFF MODELING** — Usable for rainfall-inundation relationship. |
| **TOTAL** | **All cataloged 2021–2025 Assam satellite observations** | **156 layers** | **156 layers** | Complete multi-year satellite flood archive on Bhuvan. |

### Annual Breakdown by Year (Audited)

| Year | Total Discovered Layers | Verified Dual Overlap (Tier-1 Core) | Statewide BBox (Tier-2 Conditional) | River Outage During Flood | Rainfall Overlap Only (Priority 2) | Primary River Gauges Verified |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **2021** | 19 | 0 | 0 | 0 | 19 | None (River telemetry begins 2022) |
| **2022** | 41 | 3 | 25 | 6 | 7 | NH15 Crossing Fakirpara Tangni, NH17 Crossing Boko |
| **2023** | 22 | 4 | 9 | 1 | 8 | NH15 Crossing Fakirpara Tangni, NH15 Crossing Dhansirighat |
| **2024** | 35 | 3 | 11 | 6 | 15 | NH15 Crossing Fakirpara Tangni |
| **2025** | 39 | 2 | 14 | 8 | 15 | NH15 Crossing Fakirpara Tangni |

---

## 2. Priority 1 Layers (2022–2025: Dual CWC Rainfall & River-Level Overlap)

These layers represent the highest-value ground truth for RISK // INDIA because they coincide temporally and spatially with active CWC hourly rainfall telemetry AND CWC hourly river water-level telemetry gauges (`NH15 Crossing Fakirpara Tangni`, `NH15 Crossing Dhansirighat`, and `NH17 Crossing Boko`):

| # | Year | Event Date | Obs Time | Coverage Layer Name | Overlapping CWC River Gauges | Bounding Box (WGS 84: MinX, MinY, MaxX, MaxY) | Availability |
| :---: | :---: | :---: | :---: | :--- | :--- | :--- | :---: |
| 1 | 2022 | 2022-05-18 | 18:00 | `flood:as_2022_18_05_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.701, 23.964, 96.014, 28.994` | **ONLINE (WCS)** |
| 2 | 2022 | 2022-05-19 | 18:00 | `flood:as_2022_19_05_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.701, 24.134, 92.382, 27.973` | **ONLINE (WCS)** |
| 3 | 2022 | 2022-05-20 | 10:00 | `flood:as_2022_20_05_10` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat | `91.769, 24.134, 93.466, 27.532` | **ONLINE (WCS)** |
| 4 | 2022 | 2022-05-21 | 06:00 | `flood:as_2022_21_05_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.701, 24.134, 96.215, 28.415` | **ONLINE (WCS)** |
| 5 | 2022 | 2022-05-22 | 06:00 | `flood:as_2022_22_05_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.701, 24.134, 96.014, 27.973` | **ONLINE (WCS)** |
| 6 | 2022 | 2022-05-22 | 18:00 | `flood:as_2022_22_05_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.701, 23.243, 96.014, 27.973` | **ONLINE (WCS)** |
| 7 | 2022 | 2022-05-23 | 18:00 | `flood:as_2022_23_05_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `90.571, 24.134, 93.659, 26.988` | **ONLINE (WCS)** |
| 8 | 2022 | 2022-05-24 | 16:00 | `flood:as_2022_24_05_16` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.702, 24.135, 96.013, 27.972` | **ONLINE (WCS)** |
| 9 | 2022 | 2022-05-25 | 11:00 | `flood:as_2022_25_05_11` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.701, 23.598, 96.387, 27.973` | **ONLINE (WCS)** |
| 10 | 2022 | 2022-05-26 | 06:00 | `flood:as_2022_25-26_05_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `90.739, 24.134, 96.014, 27.973` | **ONLINE (WCS)** |
| 11 | 2022 | 2022-05-26 | 11:00 | `flood:as_2022_26_05_11` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.699, 24.134, 96.015, 27.973` | **ONLINE (WCS)** |
| 12 | 2022 | 2022-06-16 | 06:00 | `flood:as_2022_16_06_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.517, 24.134, 96.014, 27.973` | **ONLINE (WCS)** |
| 13 | 2022 | 2022-06-16 | 18:00 | `flood:as_2022_16_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.701, 23.562, 96.014, 27.973` | **ONLINE (WCS)** |
| 14 | 2022 | 2022-06-17 | 18:00 | `flood:as_2022_17_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.701, 24.134, 96.014, 27.973` | **ONLINE (WCS)** |
| 15 | 2022 | 2022-06-19 | 06:00 | `flood:as_2022_18-19_06_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.701, 24.133, 96.332, 28.661` | **ONLINE (WCS)** |
| 16 | 2022 | 2022-06-19 | 18:00 | `flood:as_2022_19_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `87.308, 23.103, 96.014, 28.467` | **ONLINE (WCS)** |
| 17 | 2022 | 2022-06-20 | 18:00 | `flood:as_2022_20_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.691, 24.111, 96.014, 27.977` | **ONLINE (WCS)** |
| 18 | 2022 | 2022-06-21 | 09:00 | `flood:as_2022_21_06_09` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.691, 24.111, 96.014, 27.977` | **ONLINE (WCS)** |
| 19 | 2022 | 2022-06-21 | 18:00 | `flood:as_2022_21_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.691, 24.111, 96.014, 28.412` | **ONLINE (WCS)** |
| 20 | 2022 | 2022-06-22 | 11:00 | `flood:as_2022_22_06_11` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.691, 23.575, 96.388, 27.977` | **ONLINE (WCS)** |
| 21 | 2022 | 2022-06-24 | 06:00 | `flood:as_2022_23-24_06_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.691, 23.956, 96.014, 28.888` | **ONLINE (WCS)** |
| 22 | 2022 | 2022-06-24 | 18:00 | `flood:as_2022_24_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat | `91.593, 25.425, 93.472, 27.112` | **ONLINE (WCS)** |
| 23 | 2022 | 2022-06-25 | 18:00 | `flood:as_2022_25_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.859, 24.175, 92.574, 27.240` | **ONLINE (WCS)** |
| 24 | 2022 | 2022-06-26 | 18:00 | `flood:as_2022_26_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat | `91.742, 24.111, 94.776, 27.977` | **ONLINE (WCS)** |
| 25 | 2022 | 2022-06-28 | 18:00 | `flood:as_2022_28_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `90.076, 24.111, 93.713, 27.000` | **ONLINE (WCS)** |
| 26 | 2022 | 2022-07-01 | 06:00 | `flood:as_2022_01_07_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `91.185, 24.304, 93.881, 26.953` | **ONLINE (WCS)** |
| 27 | 2022 | 2022-07-03 | 18:00 | `flood:as_2022_03_07_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `88.473, 24.111, 96.014, 27.977` | **ONLINE (WCS)** |
| 28 | 2022 | 2022-07-05 | 18:00 | `flood:as_2022_05_07_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.691, 24.111, 96.014, 28.913` | **ONLINE (WCS)** |
| 29 | 2022 | 2022-07-06 | 18:00 | `flood:as_2022_06_07_18` | NH17 Crossing Boko | `89.691, 25.016, 91.790, 26.944` | **ONLINE (WCS)** |
| 30 | 2022 | 2022-07-08 | 06:00 | `flood:as_2022_07-08_07_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.691, 23.107, 96.211, 28.385` | **ONLINE (WCS)** |
| 31 | 2022 | 2022-07-13 | 06:00 | `flood:as_2022_12-13_07` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.691, 23.733, 97.145, 29.005` | **ONLINE (WCS)** |
| 32 | 2022 | 2022-07-14 | 06:00 | `flood:as_2022_14_07` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.691, 24.111, 96.014, 27.977` | **ONLINE (WCS)** |
| 33 | 2022 | 2022-07-17 | 18:00 | `flood:as_2022_17_07_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.691, 24.111, 96.014, 27.977` | **ONLINE (WCS)** |
| 34 | 2022 | 2022-18-28 | 06:00 | `flood:as_2022_16-28_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `87.038, 22.999, 96.511, 28.987` | **ONLINE (WCS)** |
| 35 | 2023 | 2023-06-16 | 06:00 | `flood:as_2023_16_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.701, 24.136, 96.013, 27.973` | **ONLINE (WCS)** |
| 36 | 2023 | 2023-06-17 | 06:00 | `flood:as_2023_17_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.701, 24.136, 96.013, 27.973` | **ONLINE (WCS)** |
| 37 | 2023 | 2023-06-18 | 06:00 | `flood:as_2023_18_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.701, 24.136, 96.013, 27.973` | **ONLINE (WCS)** |
| 38 | 2023 | 2023-06-20 | 18:00 | `flood:as_2023_20_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `90.251, 24.136, 93.504, 27.599` | **ONLINE (WCS)** |
| 39 | 2023 | 2023-06-21 | 18:00 | `flood:as_2023_21_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat | `91.277, 24.136, 94.281, 27.242` | **ONLINE (WCS)** |
| 40 | 2023 | 2023-06-23 | 18:00 | `flood:as_2023_23_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `90.561, 24.133, 93.714, 27.000` | **ONLINE (WCS)** |
| 41 | 2023 | 2023-06-26 | 06:00 | `flood:as_2023_26_06_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.700, 24.133, 96.014, 27.972` | **ONLINE (WCS)** |
| 42 | 2023 | 2023-06-29 | 18:00 | `flood:as_2023_29_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.699, 24.132, 96.021, 27.972` | **ONLINE (WCS)** |
| 43 | 2023 | 2023-07-07 | 18:00 | `flood:as_2023_07_07_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.701, 25.507, 96.013, 27.971` | **ONLINE (WCS)** |
| 44 | 2023 | 2023-07-15 | 18:00 | `flood:as_2023_15_07_18` | NH15 Crossing Fakirpara Tangni<br>NH17 Crossing Boko | `89.885, 24.649, 92.132, 27.675` | **ONLINE (WCS)** |
| 45 | 2023 | 2023-07-20 | 06:00 | `flood:as_2023_20_07_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat | `91.587, 25.415, 93.495, 27.128` | **ONLINE (WCS)** |
| 46 | 2023 | 2023-08-31 | 18:00 | `flood:as_2023_31_08_18` | NH17 Crossing Boko | `90.172, 25.411, 92.091, 27.141` | **ONLINE (WCS)** |
| 47 | 2023 | 2023-17-16 | 08:00 | `flood:as_2023_16_17_08` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat | `91.709, 24.435, 94.336, 27.973` | **ONLINE (WCS)** |
| 48 | 2023 | 2023-18-16 | 06:00 | `flood:as_2023_16-18_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.701, 24.136, 96.013, 27.973` | **ONLINE (WCS)** |
| 49 | 2024 | 2024-05-31 | 18:00 | `flood:as_2024_31_05_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat | `91.895, 25.563, 93.659, 27.225` | **ONLINE (WCS)** |
| 50 | 2024 | 2024-06-03 | 18:00 | `flood:as_2024_03_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat | `91.329, 24.359, 93.544, 27.388` | **ONLINE (WCS)** |
| 51 | 2024 | 2024-06-07 | 11:00 | `flood:as_2024_07_06_11` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `90.765, 25.712, 93.502, 27.021` | **ONLINE (WCS)** |
| 52 | 2024 | 2024-06-08 | 06:00 | `flood:as_2024_08_06_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `90.766, 24.136, 93.896, 27.164` | **ONLINE (WCS)** |
| 53 | 2024 | 2024-06-12 | 18:00 | `flood:as_2024_12_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat | `91.515, 24.084, 93.795, 27.128` | **ONLINE (WCS)** |
| 54 | 2024 | 2024-06-17 | 18:00 | `flood:as_2024_17_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.700, 24.133, 96.021, 27.972` | **ONLINE (WCS)** |
| 55 | 2024 | 2024-06-20 | 06:00 | `flood:as_2024_20_06_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `90.765, 24.136, 93.895, 27.164` | **ONLINE (WCS)** |
| 56 | 2024 | 2024-06-23 | 11:00 | `flood:as_2024_23_06_11` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `90.310, 25.543, 92.788, 27.069` | **ONLINE (WCS)** |
| 57 | 2024 | 2024-07-03 | 06:00 | `flood:as_2024_03_07_06` | NH17 Crossing Boko | `90.172, 25.411, 92.073, 27.125` | **ONLINE (WCS)** |
| 58 | 2024 | 2024-07-04 | 06:00 | `flood:as_2024_03-04_07_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `90.039, 24.145, 95.135, 28.395` | **ONLINE (WCS)** |
| 59 | 2024 | 2024-07-04 | 18:00 | `flood:as_2024_04_07_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.700, 24.133, 96.021, 27.972` | **ONLINE (WCS)** |
| 60 | 2024 | 2024-07-08 | 10:00 | `flood:as_2024_08_07_10` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat | `91.847, 25.784, 93.433, 26.709` | **ONLINE (WCS)** |
| 61 | 2024 | 2024-07-08 | 18:00 | `flood:as_2024_08_07_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.700, 24.133, 96.021, 27.972` | **ONLINE (WCS)** |
| 62 | 2024 | 2024-07-11 | 06:00 | `flood:as_2024_11_07_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.700, 24.128, 96.021, 27.968` | **ONLINE (WCS)** |
| 63 | 2024 | 2024-07-11 | 18:00 | `flood:as_2024_11_07_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `90.522, 23.542, 93.736, 27.019` | **ONLINE (WCS)** |
| 64 | 2024 | 2024-07-16 | 18:00 | `flood:as_2024_16_07_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat | `91.244, 24.161, 93.525, 27.063` | **ONLINE (WCS)** |
| 65 | 2024 | 2024-07-20 | 06:00 | `flood:as_2024_20_07_06` | NH17 Crossing Boko | `90.190, 25.411, 92.091, 27.125` | **ONLINE (WCS)** |
| 66 | 2024 | 2024-08-09 | 06:00 | `flood:as_2024_09_08` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.700, 24.133, 96.021, 27.972` | **ONLINE (WCS)** |
| 67 | 2024 | 2024-08-09 | 18:00 | `flood:as_2024_09_08_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.699, 24.136, 96.018, 27.971` | **ONLINE (WCS)** |
| 68 | 2024 | 2024-08-10 | 18:00 | `flood:as_2024_10_08_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.700, 24.133, 96.021, 27.972` | **ONLINE (WCS)** |
| 69 | 2025 | 2025-04-07 | 10:00 | `flood:as_2025_07_04_10` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.532, 23.494, 96.093, 28.460` | **ONLINE (WCS)** |
| 70 | 2025 | 2025-06-03 | 06:00 | `flood:as_2025_03_06_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.700, 24.133, 96.018, 27.971` | **ONLINE (WCS)** |
| 71 | 2025 | 2025-06-03 | 10:00 | `flood:as_2025_03_06_10` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.532, 23.494, 96.093, 28.460` | **ONLINE (WCS)** |
| 72 | 2025 | 2025-06-06 | 06:00 | `flood:as_2025_06_06_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.700, 24.133, 96.021, 27.972` | **ONLINE (WCS)** |
| 73 | 2025 | 2025-06-07 | 18:00 | `flood:as_2025_07_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.532, 23.494, 96.093, 28.460` | **ONLINE (WCS)** |
| 74 | 2025 | 2025-06-08 | 06:00 | `flood:as_2025_08_06_06` | NH17 Crossing Boko | `90.172, 25.411, 92.073, 27.141` | **ONLINE (WCS)** |
| 75 | 2025 | 2025-06-09 | 06:00 | `flood:as_2025_09_06_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.701, 24.136, 96.013, 27.973` | **ONLINE (WCS)** |
| 76 | 2025 | 2025-06-09 | 10:00 | `flood:as_2025_09_06_10` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.700, 24.133, 96.021, 27.972` | **ONLINE (WCS)** |
| 77 | 2025 | 2025-06-09 | 18:00 | `flood:as_2025_09_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.700, 24.133, 96.021, 27.972` | **ONLINE (WCS)** |
| 78 | 2025 | 2025-06-11 | 10:00 | `flood:as_2025_11_06_10` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `90.681, 25.441, 92.574, 26.992` | **ONLINE (WCS)** |
| 79 | 2025 | 2025-06-12 | 06:00 | `flood:as_2025_31_05-12_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.903, 24.191, 95.941, 27.937` | **ONLINE (WCS)** |
| 80 | 2025 | 2025-06-12 | 10:00 | `flood:as_2025_12_06_10` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.301, 23.373, 96.098, 28.563` | **ONLINE (WCS)** |
| 81 | 2025 | 2025-06-12 | 18:00 | `flood:as_2025_12_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.700, 24.133, 96.021, 27.972` | **ONLINE (WCS)** |
| 82 | 2025 | 2025-06-17 | 18:00 | `flood:as_2025_17_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.600, 24.096, 96.128, 28.008` | **ONLINE (WCS)** |
| 83 | 2025 | 2025-06-19 | 18:00 | `flood:as_2025_19_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.532, 23.494, 96.093, 28.460` | **ONLINE (WCS)** |
| 84 | 2025 | 2025-06-24 | 18:00 | `flood:as_2025_24_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.700, 24.133, 96.021, 27.972` | **ONLINE (WCS)** |
| 85 | 2025 | 2025-06-26 | 06:00 | `flood:as_2025_26_06_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.532, 23.493, 96.093, 28.460` | **ONLINE (WCS)** |
| 86 | 2025 | 2025-06-27 | 18:00 | `flood:as_2025_27_06_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.701, 24.136, 96.013, 27.973` | **ONLINE (WCS)** |
| 87 | 2025 | 2025-06-28 | 11:00 | `flood:as_2025_28_06_11` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat | `91.973, 24.523, 93.107, 26.824` | **ONLINE (WCS)** |
| 88 | 2025 | 2025-07-03 | 10:00 | `flood:as_2025_03_07_10` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.532, 23.494, 96.093, 28.460` | **ONLINE (WCS)** |
| 89 | 2025 | 2025-07-05 | 18:00 | `flood:as_2025_05_07_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.532, 23.494, 96.093, 28.460` | **ONLINE (WCS)** |
| 90 | 2025 | 2025-07-06 | 18:00 | `flood:as_2025_06_07_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.701, 24.136, 96.013, 28.167` | **ONLINE (WCS)** |
| 91 | 2025 | 2025-07-08 | 06:00 | `flood:as_2025_08_07_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.700, 24.133, 96.021, 27.972` | **ONLINE (WCS)** |
| 92 | 2025 | 2025-07-11 | 10:00 | `flood:as_2025_11_07_10` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.701, 24.136, 96.013, 27.973` | **ONLINE (WCS)** |
| 93 | 2025 | 2025-08-13 | 18:00 | `flood:as_2025_13_08_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.532, 23.494, 96.093, 28.460` | **ONLINE (WCS)** |
| 94 | 2025 | 2025-09-16 | 18:00 | `flood:as_2025_16_09_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `90.115, 23.763, 94.629, 27.521` | **ONLINE (WCS)** |
| 95 | 2025 | 2025-09-19 | 06:00 | `flood:as_2025_19_09_06` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `90.115, 23.763, 94.629, 27.521` | **ONLINE (WCS)** |
| 96 | 2025 | 2025-09-20 | 10:00 | `flood:as_2025_20_09_10` | NH15 Crossing Fakirpara Tangni<br>NH17 Crossing Boko | `89.905, 24.905, 92.247, 27.064` | **ONLINE (WCS)** |
| 97 | 2025 | 2025-09-21 | 18:00 | `flood:as_2025_21_09_18` | NH17 Crossing Boko | `89.699, 25.466, 91.823, 26.905` | **ONLINE (WCS)** |
| 98 | 2025 | 2025-09-22 | 10:00 | `flood:as_2025_22_09_10` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `90.443, 25.687, 94.811, 27.814` | **ONLINE (WCS)** |
| 99 | 2025 | 2025-09-22 | 18:00 | `flood:as_2025_22_09_18` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `90.115, 24.970, 93.895, 27.032` | **ONLINE (WCS)** |
| 100 | 2025 | 2025-09-25 | 10:00 | `flood:as_2025_25_09_10` | NH15 Crossing Fakirpara Tangni<br>NH15 Crossing Dhansirighat<br>NH17 Crossing Boko | `89.631, 24.069, 96.161, 28.034` | **ONLINE (WCS)** |

---

## 3. Priority 2 Layers (2021: CWC Rainfall Overlap Only)

These layers possess active CWC hourly rainfall telemetry across Assam (31 active reporting stations), but predate the CWC river-level telemetry records (which begin January 1, 2022):

| # | Year | Event Date | Obs Time | Coverage Layer Name | Overlapping CWC Rain Stations | Bounding Box (WGS 84: MinX, MinY, MaxX, MaxY) | Availability |
| :---: | :---: | :---: | :---: | :--- | :--- | :--- | :---: |
| 1 | 2021 | 2021-06-07 | 06:00 | `flood:as_2021_07_06_06` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `93.030, 24.911, 96.014, 27.973` | **ONLINE (WCS)** |
| 2 | 2021 | 2021-06-09 | 06:00 | `flood:as_2021_09_06_06` | Numaligarh | `90.539, 24.134, 93.737, 27.002` | **ONLINE (WCS)** |
| 3 | 2021 | 2021-06-28 | 18:00 | `flood:as_2021_28_06_18` | Dibrugarh<br>Basudevthan | `94.314, 26.840, 95.153, 27.832` | **ONLINE (WCS)** |
| 4 | 2021 | 2021-07-01 | 06:00 | `flood:as_2021_01_07_06` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `89.701, 24.134, 96.176, 28.380` | **ONLINE (WCS)** |
| 5 | 2021 | 2021-07-03 | 18:00 | `flood:as_2021_03_07_18` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `89.701, 24.134, 96.014, 27.973` | **ONLINE (WCS)** |
| 6 | 2021 | 2021-07-10 | 18:00 | `flood:as_2021_10_07_18` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `92.549, 25.710, 95.180, 27.792` | **ONLINE (WCS)** |
| 7 | 2021 | 2021-07-13 | 06:00 | `flood:as_2021_13_07_06` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `93.038, 24.917, 96.014, 27.973` | **ONLINE (WCS)** |
| 8 | 2021 | 2021-07-13 | 21:00 | `flood:as_2021_13_07_21` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `89.701, 24.134, 96.014, 27.973` | **ONLINE (WCS)** |
| 9 | 2021 | 2021-07-15 | 18:00 | `flood:as_2021_15_07_18` | Regional catchments | `90.434, 25.575, 93.543, 27.174` | **ONLINE (WCS)** |
| 10 | 2021 | 2021-07-22 | 18:00 | `flood:as_2021_22_07_18` | Nematighat<br>Numaligarh<br>Golaghat<br>*(+1 more)* | `92.532, 25.465, 95.378, 27.395` | **ONLINE (WCS)** |
| 11 | 2021 | 2021-08-27 | 06:00 | `flood:as_2021_27_08_06` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `89.964, 24.903, 96.014, 27.973` | **ONLINE (WCS)** |
| 12 | 2021 | 2021-08-27 | 18:00 | `flood:as_2021_27_08_18` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `92.193, 25.464, 95.421, 27.973` | **ONLINE (WCS)** |
| 13 | 2021 | 2021-08-28 | 06:00 | `flood:as_2021_28_08_06` | Regional catchments | `89.701, 25.022, 91.792, 26.935` | **ONLINE (WCS)** |
| 14 | 2021 | 2021-08-30 | 06:00 | `flood:as_2021_30_08_06` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `89.701, 24.134, 96.500, 28.389` | **ONLINE (WCS)** |
| 15 | 2021 | 2021-08-31 | 14:00 | `flood:as_2021_31_08_14` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `89.702, 24.135, 96.013, 27.972` | **ONLINE (WCS)** |
| 16 | 2021 | 2021-09-01 | 18:00 | `flood:as_2021_01_09_18` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `90.217, 24.134, 96.014, 27.973` | **ONLINE (WCS)** |
| 17 | 2021 | 2021-09-03 | 18:00 | `flood:as_2021_03_09_18` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `89.701, 23.712, 96.014, 28.671` | **ONLINE (WCS)** |
| 18 | 2021 | 2021-09-05 | 14:00 | `flood:as_2021_05_09_14` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `89.702, 24.135, 96.013, 27.972` | **ONLINE (WCS)** |
| 19 | 2021 | 2021-09-06 | 18:00 | `flood:as_2021_06_09_18` | Regional catchments | `89.701, 25.264, 91.316, 27.159` | **ONLINE (WCS)** |
| 20 | 2022 | 2022-05-19 | 06:00 | `flood:as_2022_19_05_06` | Regional catchments | `92.675, 24.452, 93.046, 25.000` | **ONLINE (WCS)** |
| 21 | 2022 | 2022-05-19 | 06:00 | `flood:as_2022_19_05` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+1 more)* | `92.506, 24.134, 94.493, 27.821` | **ONLINE (WCS)** |
| 22 | 2022 | 2022-05-19 | 09:00 | `flood:as_2022_19_05_09` | Numaligarh<br>Golaghat | `92.671, 26.043, 93.957, 27.041` | **ONLINE (WCS)** |
| 23 | 2022 | 2022-06-21 | 17:00 | `flood:as_2022_21_06_17` | Regional catchments | `89.691, 25.278, 91.188, 26.830` | **ONLINE (WCS)** |
| 24 | 2022 | 2022-06-27 | 18:00 | `flood:as_2022_27_06_18` | Regional catchments | `89.691, 24.542, 91.162, 27.977` | **ONLINE (WCS)** |
| 25 | 2022 | 2022-06-29 | 18:00 | `flood:as_2022_29_06_18` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `92.570, 25.648, 95.541, 27.977` | **ONLINE (WCS)** |
| 26 | 2022 | 2022-07-08 | 18:00 | `flood:as_2022_08_07_18` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `93.643, 25.563, 96.014, 27.977` | **ONLINE (WCS)** |
| 27 | 2023 | 2023-06-19 | 18:00 | `flood:as_2023_19_06_18` | Nematighat<br>Chouldhowaghat<br>Dibrugarh<br>*(+1 more)* | `94.106, 26.513, 96.658, 28.391` | **ONLINE (WCS)** |
| 28 | 2023 | 2023-06-22 | 18:00 | `flood:as_2023_22_06_18` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `93.612, 25.276, 96.115, 28.016` | **ONLINE (WCS)** |
| 29 | 2023 | 2023-06-25 | 18:00 | `flood:as_2023_25_06_18` | Dibrugarh<br>Basudevthan | `94.286, 25.571, 96.021, 27.972` | **ONLINE (WCS)** |
| 30 | 2023 | 2023-06-26 | 18:00 | `flood:as_2023_26_06_18` | Nematighat<br>Numaligarh<br>Golaghat<br>*(+1 more)* | `92.476, 25.635, 95.007, 27.420` | **ONLINE (WCS)** |
| 31 | 2023 | 2023-06-27 | 18:00 | `flood:as_2023_27_06_18` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `93.456, 25.369, 96.293, 28.492` | **ONLINE (WCS)** |
| 32 | 2023 | 2023-07-09 | 18:00 | `flood:as_2023_09_07_18` | Nematighat<br>Chouldhowaghat<br>Dibrugarh<br>*(+1 more)* | `93.836, 26.581, 96.013, 27.973` | **ONLINE (WCS)** |
| 33 | 2023 | 2023-07-12 | 06:00 | `flood:as_2023_12_07_06` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `93.022, 25.425, 95.135, 28.395` | **ONLINE (WCS)** |
| 34 | 2023 | 2023-08-29 | 18:00 | `flood:as_2023_29_08_18` | Nematighat<br>Numaligarh<br>Golaghat<br>*(+1 more)* | `92.543, 25.464, 95.411, 27.393` | **ONLINE (WCS)** |
| 35 | 2024 | 2024-06-02 | 11:00 | `flood:as_2024_02_06_11` | Regional catchments | `92.537, 24.573, 93.009, 24.908` | **ONLINE (WCS)** |
| 36 | 2024 | 2024-06-02 | 18:00 | `flood:as_2024_02_06_18` | Regional catchments | `90.932, 24.112, 92.740, 25.193` | **ONLINE (WCS)** |
| 37 | 2024 | 2024-06-03 | 06:00 | `flood:as_2024_03_06_06` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `93.348, 26.461, 96.013, 27.971` | **ONLINE (WCS)** |
| 38 | 2024 | 2024-06-06 | 11:00 | `flood:as_2024_06_06_11` | Regional catchments | `92.050, 26.022, 92.910, 26.343` | **ONLINE (WCS)** |
| 39 | 2024 | 2024-06-11 | 18:00 | `flood:as_2024_11_06_18` | Regional catchments | `91.783, 24.136, 93.825, 25.828` | **ONLINE (WCS)** |
| 40 | 2024 | 2024-06-26 | 11:00 | `flood:as_2024_26_06_11` | Regional catchments | `92.036, 24.251, 93.066, 25.109` | **ONLINE (WCS)** |
| 41 | 2024 | 2024-07-01 | 18:00 | `flood:as_2024_01_07_18` | Dibrugarh<br>Basudevthan | `94.290, 25.571, 97.434, 27.977` | **ONLINE (WCS)** |
| 42 | 2024 | 2024-07-07 | 18:00 | `flood:as_2024_07_07_18` | Basudevthan | `94.266, 26.705, 94.757, 27.581` | **ONLINE (WCS)** |
| 43 | 2024 | 2024-07-13 | 10:00 | `flood:as_2024_13_07_10` | Nematighat<br>Basudevthan | `94.245, 26.803, 95.004, 27.418` | **ONLINE (WCS)** |
| 44 | 2024 | 2024-07-16 | 06:00 | `flood:as_2024_16_07` | Regional catchments | `92.060, 24.184, 93.298, 25.107` | **ONLINE (WCS)** |
| 45 | 2024 | 2024-07-18 | 18:00 | `flood:as_2024_18_07_18` | Nematighat<br>Numaligarh<br>Golaghat<br>*(+1 more)* | `92.546, 25.464, 95.368, 27.385` | **ONLINE (WCS)** |
| 46 | 2024 | 2024-07-25 | 10:00 | `flood:as_2024_25_07_10` | Regional catchments | `94.295, 26.765, 94.880, 27.086` | **ONLINE (WCS)** |
| 47 | 2024 | 2024-07-25 | 18:00 | `flood:as_2024_25_07_18` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+3 more)* | `93.511, 25.558, 95.806, 27.971` | **ONLINE (WCS)** |
| 48 | 2024 | 2024-07-30 | 18:00 | `flood:as_2024_30_07_18` | Nematighat<br>Numaligarh<br>Golaghat<br>*(+1 more)* | `92.545, 25.464, 95.367, 27.385` | **ONLINE (WCS)** |
| 49 | 2024 | 2024-08-11 | 18:00 | `flood:as_2024_11_08_18` | Nematighat<br>Numaligarh<br>Golaghat<br>*(+1 more)* | `92.901, 26.463, 95.106, 27.382` | **ONLINE (WCS)** |
| 50 | 2025 | 2025-06-01 | 06:00 | `flood:as_2025_01_06_06` | Dibrugarh | `94.710, 27.014, 95.941, 27.937` | **ONLINE (WCS)** |
| 51 | 2025 | 2025-06-04 | 18:00 | `flood:as_2025_04_06_18` | Nematighat<br>Chouldhowaghat<br>Dibrugarh<br>*(+1 more)* | `93.991, 26.793, 95.540, 27.845` | **ONLINE (WCS)** |
| 52 | 2025 | 2025-06-10 | 11:00 | `flood:as_2025_10_06_11` | Nematighat<br>Numaligarh<br>Chouldhowaghat<br>*(+2 more)* | `93.422, 26.514, 95.639, 28.186` | **ONLINE (WCS)** |
| 53 | 2025 | 2025-06-17 | 10:00 | `flood:as_2025_17_06_10` | Regional catchments | `92.330, 24.369, 93.172, 24.999` | **ONLINE (WCS)** |
| 54 | 2025 | 2025-07-13 | 18:00 | `flood:as_2025_13_07_18` | Nematighat<br>Numaligarh<br>Golaghat<br>*(+1 more)* | `92.546, 25.464, 95.414, 27.392` | **ONLINE (WCS)** |
| 55 | 2025 | 2025-08-09 | 06:00 | `flood:as_2025_09_08_06` | Nematighat<br>Chouldhowaghat<br>Dibrugarh<br>*(+1 more)* | `94.113, 26.636, 95.563, 27.998` | **ONLINE (WCS)** |
| 56 | 2025 | 2025-09-19 | 10:00 | `flood:as_2025_19_09_10` | Regional catchments | `92.213, 23.763, 93.474, 25.827` | **ONLINE (WCS)** |

---

## 4. Technical Guidelines for Automated WCS Extraction

1. **Service Endpoint**: `https://bhuvan-gp1.nrsc.gov.in/bhuvan/wcs`
2. **Protocol Parameters**:
   - `service=WCS`
   - `version=1.0.0`
   - `request=GetCoverage`
   - `coverage=<coverage_name>`
   - `crs=EPSG:4326`
   - `format=GeoTIFF`
   - `width=512&height=512`
3. **Spatial Window Configuration**: Always query a focused catchment-scale window (\(0.20^\circ 	imes 0.20^\circ\), approx. \(20\times 22\text{ km}\)) centered on the CWC gauge. Do NOT query full-state extents in a single request to avoid server-side gateway timeouts.
4. **Storage Convention**: Save downloaded rasters to `datasets/raw/isro/flood_inundation/` with naming convention `assam_<year>_<month>_<day>_<hour>hr_<gauge>.tif`.