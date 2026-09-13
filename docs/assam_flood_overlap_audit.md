# Assam Flood Observation Overlap Forensic Audit (2022–2025)

**Investigation**: Phase 7C-A — Critical Cross-Source Consistency & Overlap Verification  
**Audit Date**: September 12, 2026  
**Auditor**: Lead Data Forensics & Geospatial ML Engineer  
**Total Candidate Layers Audited (2022–2025)**: **137 layers**  

---

## 1. Executive Summary & Forensic Audit Finding

In Phase 7C, an initial automated spatial check suggested that approximately 100 layers had 'dual rainfall and river-level overlap'. In Phase 7C-A, a strict independent audit was executed to verify whether:
1. The layer actually intersects a **verified CWC river-level gauge** (`NH15 Crossing Fakirpara Tangni`, `NH15 Crossing Dhansirighat`, `NH17 Crossing Boko`), rather than an unverified state-wide bounding box.
2. The river gauge actually reported **valid, non-null water level data** during the event window (verifying sensor uptime vs outage).
3. An **active reporting CWC rain station** (out of the 31 verified active stations) had valid rainfall records in the preceding 24 hours.

### Key Audit Discovery:

| Audit Category | Description | Count | ML Training Implication |
| :--- | :--- | :---: | :--- |
| **`VERIFIED_DUAL_OVERLAP`** | **Genuine Focused Swaths**: Satellite footprint tightly bounds gauge (\(\le 3^\circ\) span); simultaneous non-null CWC river-stage AND active CWC rainfall telemetry verified. | **12 layers** | **TIER-1 PRIMARY ML CANDIDATES** — Scientifically defensible dual-sensor ground truth. |
| **`STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE`** | **Statewide Envelopes**: Layer declares broad state bounding box (\(\ge 4.5^\circ\) span); river telemetry was active, but true satellite swath extent is unconfirmed at gauge level. | **59 layers** | **TIER-2 CONDITIONAL CANDIDATES** — Requires manual raster boundary verification prior to training. |
| **`RIVER_TELEMETRY_OUTAGE`** | **Sensor Outages During Flood**: Layer footprint intersects gauge, but river sensor reported 0 valid records (e.g. submerged/damaged in historic June 16–17, 2022 flood). | **21 layers** | **EXCLUDED FROM STAGE REGRESSION** — Can only be used for rainfall-inundation classification, not stage modeling. |
| **`NO_RIVER_GAUGE_OVERLAP`** | **Regional Swath Mismatch**: Layer footprint is restricted to Upper Brahmaputra (Lakhimpur/Dibrugarh) or Barak Valley and does not cover the 3 river gauges. | **37 layers** | **EXCLUDED FROM GAUGE MODELING** — Usable only for regional rainfall-runoff research. |
| **`RAIN_DATA_GAP`** | River gauge was active, but nearby active rainfall stations reported 0 readings in the 24h window. | **5 layers** | **EXCLUDED DUE TO MISSING PREDICTOR**. |
| **`UNPARSEABLE_DATE_COMPOSITE`** | Multi-week composite layers with non-discrete observation dates (e.g. `16-28`). | **3 layers** | **EXCLUDED FROM EVENT MODELING**. |
| **TOTAL AUDITED** | **All 2022–2025 Assam Satellite Flood Coverages** | **137 layers** | Complete census of Bhuvan 2022–2025 archive. |

---

## 2. Verified Dual-Overlap Layers (Tier-1 Primary ML Ground Truth)

These **12 layers** represent the definitive, defensible empirical ground-truth core for RISK // INDIA:

| # | Event Timestamp | Flood Layer | River Gauge Matched | River Data (24h) | Nearest Active Rain Station | Spatial Footprint Status |
| :---: | :---: | :--- | :--- | :---: | :--- | :---: |
| 1 | `2022-05-23 18:00` | `flood:as_2022_23_05_18` | **NH15 Crossing Fakirpara Tangni** | YES (9h) | Kampur (71km) | `YES (NH15 Crossing Fakirpara Tangni)` |
| 2 | `2022-07-06 18:00` | `flood:as_2022_06_07_18` | **NH17 Crossing Boko** | YES (25h) | Beki Road bridge (67km) | `YES (NH17 Crossing Boko)` |
| 3 | `2023-06-23 18:00` | `flood:as_2023_23_06_18` | **NH15 Crossing Dhansirighat** | YES (31h) | NT Road Crossing(Jiabharali) (70km) | `YES (NH15 Crossing Dhansirighat)` |
| 4 | `2023-07-20 06:00` | `flood:as_2023_20_07_06` | **NH15 Crossing Dhansirighat** | YES (31h) | Gelabil (197km) | `YES (NH15 Crossing Dhansirighat)` |
| 5 | `2023-08-31 18:00` | `flood:as_2023_31_08_18` | **NH17 Crossing Boko** | YES (31h) | Karimganj (174km) | `YES (NH17 Crossing Boko)` |
| 6 | `2024-05-31 18:00` | `flood:as_2024_31_05_18` | **NH15 Crossing Dhansirighat** | YES (31h) | DRF (63km) | `YES (NH15 Crossing Dhansirighat)` |
| 7 | `2024-06-07 11:00` | `flood:as_2024_07_06_11` | **NH15 Crossing Dhansirighat** | YES (31h) | NT Road Crossing(Jiabharali) (70km) | `YES (NH15 Crossing Dhansirighat)` |
| 8 | `2024-07-08 10:00` | `flood:as_2024_08_07_10` | **NH15 Crossing Dhansirighat** | YES (31h) | DRF (63km) | `YES (NH15 Crossing Dhansirighat)` |
| 9 | `2024-07-16 18:00` | `flood:as_2024_16_07_18` | **NH15 Crossing Dhansirighat** | YES (31h) | DRF (63km) | `YES (NH15 Crossing Dhansirighat)` |
| 10 | `2024-07-20 06:00` | `flood:as_2024_20_07_06` | **NH17 Crossing Boko** | YES (30h) | Beki Road bridge (67km) | `YES (NH17 Crossing Boko)` |
| 11 | `2025-06-11 10:00` | `flood:as_2025_11_06_10` | **NH15 Crossing Dhansirighat** | YES (31h) | DRF (63km) | `YES (NH15 Crossing Dhansirighat)` |
| 12 | `2025-06-28 11:00` | `flood:as_2025_28_06_11` | **NH15 Crossing Dhansirighat** | YES (17h) | Karimganj (202km) | `YES (NH15 Crossing Dhansirighat)` |

---

## 3. Comprehensive Audit Table (All 137 Candidate Layers 2022–2025)

| Event | Flood Layer | Rainfall Available | Valid Rain Station | River Data Available | Valid River Gauge | Spatial Match | Final Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2022-05-18 18:00 | `flood:as_2022_18_05_18` | YES (216 rows) | Kampur (71km) | YES (9h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2022-05-19 06:00 | `flood:as_2022_19_05_06` | YES (224 rows) | Kampur (71km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2022-05-19 06:00 | `flood:as_2022_19_05` | YES (224 rows) | Kampur (71km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2022-05-19 09:00 | `flood:as_2022_19_05_09` | YES (230 rows) | Kampur (71km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2022-05-19 18:00 | `flood:as_2022_19_05_18` | YES (211 rows) | Kampur (71km) | YES (8h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2022-05-20 10:00 | `flood:as_2022_20_05_10` | YES (127 rows) | Kampur (71km) | YES (10h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2022-05-21 06:00 | `flood:as_2022_21_05_06` | YES (111 rows) | Kampur (71km) | YES (5h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2022-05-22 06:00 | `flood:as_2022_22_05_06` | YES (104 rows) | Kampur (71km) | YES (3h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2022-05-22 18:00 | `flood:as_2022_22_05_18` | YES (94 rows) | Kampur (71km) | YES (7h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2022-05-23 18:00 | `flood:as_2022_23_05_18` | YES (38 rows) | Kampur (71km) | YES (9h) | NH15 Crossing Fakirpara Tangni | YES (NH15 Crossing Fakirpara Tangni) | `VERIFIED_DUAL_OVERLAP` |
| 2022-05-24 16:00 | `flood:as_2022_24_05_16` | YES (32 rows) | Kampur (71km) | YES (5h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2022-05-25 11:00 | `flood:as_2022_25_05_11` | YES (58 rows) | Kampur (71km) | YES (8h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2022-05-26 06:00 | `flood:as_2022_25-26_05_06` | YES (77 rows) | Kampur (71km) | YES (8h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2022-05-26 11:00 | `flood:as_2022_26_05_11` | YES (79 rows) | Kampur (71km) | YES (7h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2022-06-16 06:00 | `flood:as_2022_16_06_06` | YES (106 rows) | Kampur (71km) | YES (1h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2022-06-16 18:00 | `flood:as_2022_16_06_18` | YES (131 rows) | Kampur (75km) | SENSOR_OUTAGE (0h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `RIVER_TELEMETRY_OUTAGE` |
| 2022-06-17 18:00 | `flood:as_2022_17_06_18` | YES (179 rows) | Kampur (75km) | SENSOR_OUTAGE (0h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `RIVER_TELEMETRY_OUTAGE` |
| 2022-06-19 06:00 | `flood:as_2022_18-19_06_06` | YES (108 rows) | NT Road Crossing(Jiabharali) (70km) | SENSOR_OUTAGE (0h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `RIVER_TELEMETRY_OUTAGE` |
| 2022-06-19 18:00 | `flood:as_2022_19_06_18` | YES (95 rows) | NT Road Crossing(Jiabharali) (70km) | SENSOR_OUTAGE (0h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `RIVER_TELEMETRY_OUTAGE` |
| 2022-06-20 18:00 | `flood:as_2022_20_06_18` | YES (75 rows) | NT Road Crossing(Jiabharali) (70km) | SENSOR_OUTAGE (0h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `RIVER_TELEMETRY_OUTAGE` |
| 2022-06-21 09:00 | `flood:as_2022_21_06_09` | YES (66 rows) | NT Road Crossing(Jiabharali) (70km) | SENSOR_OUTAGE (0h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `RIVER_TELEMETRY_OUTAGE` |
| 2022-06-21 17:00 | `flood:as_2022_21_06_17` | YES (81 rows) | NT Road Crossing(Jiabharali) (91km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2022-06-21 18:00 | `flood:as_2022_21_06_18` | YES (77 rows) | NT Road Crossing(Jiabharali) (70km) | SENSOR_OUTAGE (0h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `RIVER_TELEMETRY_OUTAGE` |
| 2022-06-22 11:00 | `flood:as_2022_22_06_11` | YES (65 rows) | Beki Road bridge (67km) | YES (1h) | NH17 Crossing Boko | CAUTION (Statewide BBox: NH17 Crossing Boko) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2022-06-24 06:00 | `flood:as_2022_23-24_06_06` | YES (54 rows) | Numaligarh (164km) | SENSOR_OUTAGE (0h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `RIVER_TELEMETRY_OUTAGE` |
| 2022-06-24 18:00 | `flood:as_2022_24_06_18` | YES (64 rows) | Numaligarh (164km) | SENSOR_OUTAGE (0h) | NH15 Crossing Dhansirighat | YES (NH15 Crossing Dhansirighat) | `RIVER_TELEMETRY_OUTAGE` |
| 2022-06-25 18:00 | `flood:as_2022_25_06_18` | YES (84 rows) | NT Road Crossing(Jiabharali) (70km) | SENSOR_OUTAGE (0h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `RIVER_TELEMETRY_OUTAGE` |
| 2022-06-26 18:00 | `flood:as_2022_26_06_18` | YES (88 rows) | NT Road Crossing(Jiabharali) (70km) | SENSOR_OUTAGE (0h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `RIVER_TELEMETRY_OUTAGE` |
| 2022-06-27 18:00 | `flood:as_2022_27_06_18` | YES (112 rows) | Kampur (71km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2022-06-28 18:00 | `flood:as_2022_28_06_18` | YES (119 rows) | NT Road Crossing(Jiabharali) (70km) | SENSOR_OUTAGE (0h) | NH15 Crossing Dhansirighat | YES (NH15 Crossing Dhansirighat) | `RIVER_TELEMETRY_OUTAGE` |
| 2022-06-29 18:00 | `flood:as_2022_29_06_18` | YES (91 rows) | NT Road Crossing(Jiabharali) (91km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2022-07-01 06:00 | `flood:as_2022_01_07_06` | YES (95 rows) | Kampur (75km) | SENSOR_OUTAGE (0h) | NH15 Crossing Dhansirighat | YES (NH15 Crossing Dhansirighat) | `RIVER_TELEMETRY_OUTAGE` |
| 2022-07-03 18:00 | `flood:as_2022_03_07_18` | YES (47 rows) | Gelabil (197km) | SENSOR_OUTAGE (0h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `RIVER_TELEMETRY_OUTAGE` |
| 2022-07-05 18:00 | `flood:as_2022_05_07_18` | YES (103 rows) | NT Road Crossing(Jiabharali) (70km) | YES (1h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2022-07-06 18:00 | `flood:as_2022_06_07_18` | YES (141 rows) | Beki Road bridge (67km) | YES (25h) | NH17 Crossing Boko | YES (NH17 Crossing Boko) | `VERIFIED_DUAL_OVERLAP` |
| 2022-07-08 06:00 | `flood:as_2022_07-08_07_06` | YES (66 rows) | NT Road Crossing Jia-Bharali (70km) | YES (28h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2022-07-08 18:00 | `flood:as_2022_08_07_18` | YES (83 rows) | NT Road Crossing(Jiabharali) (91km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2022-07-13 06:00 | `flood:as_2022_12-13_07` | YES (95 rows) | NT Road Crossing Jia-Bharali (70km) | YES (28h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2022-07-14 06:00 | `flood:as_2022_14_07` | YES (44 rows) | Karimganj (202km) | YES (26h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2022-07-17 18:00 | `flood:as_2022_17_07_18` | YES (97 rows) | Gelabil (197km) | YES (30h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 16-28/18/2022 | `flood:as_2022_16-28_18` | UNPARSEABLE_DATE | None | UNPARSEABLE_DATE | None | COMPOSITE_RANGE | `UNPARSEABLE_DATE_COMPOSITE` |
| 2023-06-16 06:00 | `flood:as_2023_16_06_18` | YES (122 rows) | DRF (63km) | YES (15h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2023-06-17 06:00 | `flood:as_2023_17_06_18` | YES (99 rows) | DRF (63km) | YES (6h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2023-06-18 06:00 | `flood:as_2023_18_06_18` | YES (130 rows) | DRF (63km) | YES (27h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2023-06-19 18:00 | `flood:as_2023_19_06_18` | YES (71 rows) | DRF (56km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2023-06-20 18:00 | `flood:as_2023_20_06_18` | YES (69 rows) | Beki Road bridge (150km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2023-06-21 18:00 | `flood:as_2023_21_06_18` | YES (23 rows) | Beki Road bridge (150km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2023-06-22 18:00 | `flood:as_2023_22_06_18` | YES (54 rows) | Beki Road bridge (133km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2023-06-23 18:00 | `flood:as_2023_23_06_18` | YES (19 rows) | NT Road Crossing(Jiabharali) (70km) | YES (31h) | NH15 Crossing Dhansirighat | YES (NH15 Crossing Dhansirighat) | `VERIFIED_DUAL_OVERLAP` |
| 2023-06-25 18:00 | `flood:as_2023_25_06_18` | YES (5 rows) | NT Road Crossing(Jiabharali) (91km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2023-06-26 06:00 | `flood:as_2023_26_06_06` | YES (2 rows) | Numaligarh (164km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2023-06-26 18:00 | `flood:as_2023_26_06_18` | YES (10 rows) | NT Road Crossing(Jiabharali) (91km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2023-06-27 18:00 | `flood:as_2023_27_06_18` | YES (22 rows) | NT Road Crossing(Jiabharali) (91km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2023-06-29 18:00 | `flood:as_2023_29_06_18` | YES (29 rows) | Karimganj (202km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2023-07-07 18:00 | `flood:as_2023_07_07_18` | YES (14 rows) | Basudevthan (266km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2023-07-09 18:00 | `flood:as_2023_09_07_18` | YES (1 rows) | Basudevthan (287km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2023-07-12 06:00 | `flood:as_2023_12_07_06` | YES (14 rows) | ghilamora (271km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2023-07-15 18:00 | `flood:as_2023_15_07_18` | YES (62 rows) | Kampur (71km) | YES (46h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2023-07-20 06:00 | `flood:as_2023_20_07_06` | YES (13 rows) | Gelabil (197km) | YES (31h) | NH15 Crossing Dhansirighat | YES (NH15 Crossing Dhansirighat) | `VERIFIED_DUAL_OVERLAP` |
| 2023-08-29 18:00 | `flood:as_2023_29_08_18` | YES (12 rows) | Beki Road bridge (133km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2023-08-31 18:00 | `flood:as_2023_31_08_18` | YES (17 rows) | Karimganj (174km) | YES (31h) | NH17 Crossing Boko | YES (NH17 Crossing Boko) | `VERIFIED_DUAL_OVERLAP` |
| 16/17/2023-08Hr | `flood:as_2023_16_17_08` | UNPARSEABLE_DATE | None | UNPARSEABLE_DATE | None | COMPOSITE_RANGE | `UNPARSEABLE_DATE_COMPOSITE` |
| 16-18/2023-06Hr | `flood:as_2023_16-18_06` | UNPARSEABLE_DATE | None | UNPARSEABLE_DATE | None | COMPOSITE_RANGE | `UNPARSEABLE_DATE_COMPOSITE` |
| 2024-05-31 18:00 | `flood:as_2024_31_05_18` | YES (80 rows) | DRF (63km) | YES (31h) | NH15 Crossing Dhansirighat | YES (NH15 Crossing Dhansirighat) | `VERIFIED_DUAL_OVERLAP` |
| 2024-06-02 11:00 | `flood:as_2024_02_06_11` | YES (57 rows) | DRF (56km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2024-06-02 18:00 | `flood:as_2024_02_06_18` | YES (52 rows) | DRF (56km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2024-06-03 06:00 | `flood:as_2024_03_06_06` | YES (56 rows) | DRF (56km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2024-06-03 18:00 | `flood:as_2024_03_06_18` | YES (74 rows) | DRF (63km) | YES (30h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2024-06-06 11:00 | `flood:as_2024_06_06_11` | YES (39 rows) | NT Road Crossing(Jiabharali) (91km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2024-06-07 11:00 | `flood:as_2024_07_06_11` | YES (34 rows) | NT Road Crossing(Jiabharali) (70km) | YES (31h) | NH15 Crossing Dhansirighat | YES (NH15 Crossing Dhansirighat) | `VERIFIED_DUAL_OVERLAP` |
| 2024-06-08 06:00 | `flood:as_2024_08_06_06` | YES (34 rows) | NT Road Crossing(Jiabharali) (70km) | YES (28h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2024-06-11 18:00 | `flood:as_2024_11_06_18` | YES (2 rows) | Basudevthan (287km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2024-06-12 18:00 | `flood:as_2024_12_06_18` | YES (11 rows) | NT Road Crossing(Jiabharali) (70km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2024-06-17 18:00 | `flood:as_2024_17_06_18` | YES (30 rows) | NT Road Crossing Jia-Bharali (70km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2024-06-20 06:00 | `flood:as_2024_20_06_06` | YES (6 rows) | Beki Road bridge (150km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2024-06-23 11:00 | `flood:as_2024_23_06_11` | NO | None | YES (30h) | NH15 Crossing Dhansirighat | YES (NH15 Crossing Dhansirighat) | `RAIN_DATA_GAP` |
| 2024-06-26 11:00 | `flood:as_2024_26_06_11` | NO | None | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2024-07-01 18:00 | `flood:as_2024_01_07_18` | NO | None | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2024-07-03 06:00 | `flood:as_2024_03_07_06` | NO | None | YES (31h) | NH17 Crossing Boko | YES (NH17 Crossing Boko) | `RAIN_DATA_GAP` |
| 2024-07-04 06:00 | `flood:as_2024_03-04_07_06` | YES (2 rows) | Beki Road bridge (150km) | YES (27h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2024-07-04 18:00 | `flood:as_2024_04_07_18` | YES (29 rows) | DRF (63km) | YES (27h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2024-07-07 18:00 | `flood:as_2024_07_07_18` | YES (28 rows) | Kampur (71km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2024-07-08 10:00 | `flood:as_2024_08_07_10` | YES (28 rows) | DRF (63km) | YES (31h) | NH15 Crossing Dhansirighat | YES (NH15 Crossing Dhansirighat) | `VERIFIED_DUAL_OVERLAP` |
| 2024-07-08 18:00 | `flood:as_2024_08_07_18` | YES (31 rows) | DRF (63km) | YES (30h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2024-07-11 06:00 | `flood:as_2024_11_07_06` | YES (44 rows) | DRF (63km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2024-07-11 18:00 | `flood:as_2024_11_07_18` | YES (40 rows) | DRF (63km) | YES (20h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2024-07-13 10:00 | `flood:as_2024_13_07_10` | YES (28 rows) | Beki Road bridge (133km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2024-07-16 06:00 | `flood:as_2024_16_07` | YES (54 rows) | DRF (56km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2024-07-16 18:00 | `flood:as_2024_16_07_18` | YES (49 rows) | DRF (63km) | YES (31h) | NH15 Crossing Dhansirighat | YES (NH15 Crossing Dhansirighat) | `VERIFIED_DUAL_OVERLAP` |
| 2024-07-18 18:00 | `flood:as_2024_18_07_18` | YES (22 rows) | DRF (56km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2024-07-20 06:00 | `flood:as_2024_20_07_06` | YES (12 rows) | Beki Road bridge (67km) | YES (30h) | NH17 Crossing Boko | YES (NH17 Crossing Boko) | `VERIFIED_DUAL_OVERLAP` |
| 2024-07-25 10:00 | `flood:as_2024_25_07_10` | YES (22 rows) | DRF (56km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2024-07-25 18:00 | `flood:as_2024_25_07_18` | YES (19 rows) | DRF (56km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2024-07-30 18:00 | `flood:as_2024_30_07_18` | YES (31 rows) | DRF (56km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2024-08-09 06:00 | `flood:as_2024_09_08` | YES (49 rows) | Beki Road bridge (150km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2024-08-09 18:00 | `flood:as_2024_09_08_18` | YES (23 rows) | Beki Road bridge (150km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2024-08-10 18:00 | `flood:as_2024_10_08_18` | YES (1 rows) | Basudevthan (266km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2024-08-11 18:00 | `flood:as_2024_11_08_18` | YES (2 rows) | Basudevthan (287km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2025-04-07 10:00 | `flood:as_2025_07_04_10` | NO | None | YES (31h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `RAIN_DATA_GAP` |
| 2025-06-01 06:00 | `flood:as_2025_01_06_06` | YES (19 rows) | DRF (56km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2025-06-03 06:00 | `flood:as_2025_03_06_06` | YES (13 rows) | DRF (63km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-06-03 10:00 | `flood:as_2025_03_06_10` | YES (13 rows) | DRF (63km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-06-04 18:00 | `flood:as_2025_04_06_18` | YES (9 rows) | DRF (56km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2025-06-06 06:00 | `flood:as_2025_06_06_06` | YES (10 rows) | DRF (63km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-06-07 18:00 | `flood:as_2025_07_06_18` | YES (7 rows) | Karimganj (202km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-06-08 06:00 | `flood:as_2025_08_06_06` | YES (2 rows) | Kampur (159km) | SENSOR_OUTAGE (0h) | NH17 Crossing Boko | YES (NH17 Crossing Boko) | `RIVER_TELEMETRY_OUTAGE` |
| 2025-06-09 06:00 | `flood:as_2025_09_06_06` | YES (3 rows) | Kampur (75km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-06-09 10:00 | `flood:as_2025_09_06_10` | YES (4 rows) | Kampur (75km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-06-09 18:00 | `flood:as_2025_09_06_18` | YES (4 rows) | AP Ghat (215km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-06-10 11:00 | `flood:as_2025_10_06_11` | YES (3 rows) | DRF (56km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2025-06-11 10:00 | `flood:as_2025_11_06_10` | YES (2 rows) | DRF (63km) | YES (31h) | NH15 Crossing Dhansirighat | YES (NH15 Crossing Dhansirighat) | `VERIFIED_DUAL_OVERLAP` |
| 2025-06-12 06:00 | `flood:as_2025_31_05-12_06` | YES (1 rows) | AP Ghat (215km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-06-12 10:00 | `flood:as_2025_12_06_10` | NO | None | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `RAIN_DATA_GAP` |
| 2025-06-12 18:00 | `flood:as_2025_12_06_18` | NO | None | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `RAIN_DATA_GAP` |
| 2025-06-17 10:00 | `flood:as_2025_17_06_10` | YES (10 rows) | DRF (56km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2025-06-17 18:00 | `flood:as_2025_17_06_18` | YES (11 rows) | Karimganj (202km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-06-19 18:00 | `flood:as_2025_19_06_18` | YES (20 rows) | DRF (63km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-06-24 18:00 | `flood:as_2025_24_06_18` | YES (13 rows) | DRF (56km) | YES (31h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-06-26 06:00 | `flood:as_2025_26_06_06` | YES (5 rows) | Kampur (75km) | YES (27h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-06-27 18:00 | `flood:as_2025_27_06_18` | YES (4 rows) | Karimganj (202km) | YES (31h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-06-28 11:00 | `flood:as_2025_28_06_11` | YES (3 rows) | Karimganj (202km) | YES (17h) | NH15 Crossing Dhansirighat | YES (NH15 Crossing Dhansirighat) | `VERIFIED_DUAL_OVERLAP` |
| 2025-07-03 10:00 | `flood:as_2025_03_07_10` | YES (5 rows) | DRF (56km) | YES (31h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-07-05 18:00 | `flood:as_2025_05_07_18` | YES (5 rows) | DRF (56km) | YES (31h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-07-06 18:00 | `flood:as_2025_06_07_18` | YES (3 rows) | AP Ghat (201km) | YES (31h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-07-08 06:00 | `flood:as_2025_08_07_06` | YES (13 rows) | DRF (56km) | YES (31h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-07-11 10:00 | `flood:as_2025_11_07_10` | YES (4 rows) | BAHALPUR (184km) | YES (31h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-07-13 18:00 | `flood:as_2025_13_07_18` | YES (3 rows) | DRF (56km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2025-08-09 06:00 | `flood:as_2025_09_08_06` | YES (6 rows) | Karimganj (183km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2025-08-13 18:00 | `flood:as_2025_13_08_18` | YES (8 rows) | Karimganj (183km) | YES (31h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-09-16 18:00 | `flood:as_2025_16_09_18` | YES (5 rows) | Karimganj (183km) | YES (31h) | NH15 Crossing Fakirpara Tangni | CAUTION (Statewide BBox: NH15 Crossing Fakirpara Tangni) | `STATE_LEVEL_ENVELOPE_RIVER_AVAILABLE` |
| 2025-09-19 06:00 | `flood:as_2025_19_09_06` | YES (6 rows) | Karimganj (202km) | SENSOR_OUTAGE (0h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `RIVER_TELEMETRY_OUTAGE` |
| 2025-09-19 10:00 | `flood:as_2025_19_09_10` | YES (6 rows) | Karimganj (183km) | NO | None | NO (Outside Footprint) | `NO_RIVER_GAUGE_OVERLAP` |
| 2025-09-20 10:00 | `flood:as_2025_20_09_10` | YES (1 rows) | Neharkatia (366km) | SENSOR_OUTAGE (0h) | NH15 Crossing Fakirpara Tangni | YES (NH15 Crossing Fakirpara Tangni) | `RIVER_TELEMETRY_OUTAGE` |
| 2025-09-21 18:00 | `flood:as_2025_21_09_18` | NO | None | SENSOR_OUTAGE (0h) | NH17 Crossing Boko | YES (NH17 Crossing Boko) | `RIVER_TELEMETRY_OUTAGE` |
| 2025-09-22 10:00 | `flood:as_2025_22_09_10` | YES (2 rows) | Karimganj (202km) | SENSOR_OUTAGE (0h) | NH15 Crossing Dhansirighat | YES (NH15 Crossing Dhansirighat) | `RIVER_TELEMETRY_OUTAGE` |
| 2025-09-22 18:00 | `flood:as_2025_22_09_18` | YES (2 rows) | Karimganj (202km) | SENSOR_OUTAGE (0h) | NH15 Crossing Dhansirighat | YES (NH15 Crossing Dhansirighat) | `RIVER_TELEMETRY_OUTAGE` |
| 2025-09-25 10:00 | `flood:as_2025_25_09_10` | NO | None | SENSOR_OUTAGE (0h) | NH15 Crossing Dhansirighat | CAUTION (Statewide BBox: NH15 Crossing Dhansirighat) | `RIVER_TELEMETRY_OUTAGE` |