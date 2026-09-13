# RISK // INDIA — Authoritative Flood Data Acquisition & Inspection Report

**Project**: RISK // INDIA — AI-Powered Disaster Risk Analyzer & Management System  
**Phase**: Phase 5 — Authoritative Flood Data Acquisition & Inspection  
**Pilot Region**: Assam State, India  
**Date**: 2026-09-12  

---

## Executive Summary

In **Phase 5**, the project successfully acquired real, authoritative observational datasets from the Government of India's **National Water Data Portal (NWDP / NWIC, Ministry of Jal Shakti)**. 

No synthetic, fabricated, or unverified third-party data was created. For satellite flood inundation layers that require interactive GIS map extraction from the **ISRO / NRSC Bhuvan** portal, the exact manual export procedure is documented and marked as awaiting manual download.

```
                    ┌────────────────────────────────────────────────────────┐
                    │               AUTHENTIC DATA ACQUIRED                  │
                    ├────────────────────────────────────────────────────────┤
                    │ CWC Hourly Rainfall: 137,659 rows (40 Assam stations)   │
                    │ CWC River Stage: 78,212 rows (3 Assam telemetry gauges) │
                    │ IMD District Daily: 36,371 rows (Pan-India benchmark)  │
                    └────────────────────────────────────────────────────────┘
```

---

## 1. Acquired Datasets Deep Inspection

### Dataset 1: CWC Assam Telemetry Hourly Rainfall (2021–2025)

1. **Source Agency**: Central Water Commission (CWC), Ministry of Jal Shakti
2. **Official Source URL**: `https://www.nwdp.nwic.gov.in/en/dataset/rainfall-cwc-telemetry-hourly`
3. **Local Storage Path**: [`datasets/raw/cwc/rainfall/rainfall_tel_hr_cwc_as_2021_2025.csv`](datasets/raw/cwc/rainfall/rainfall_tel_hr_cwc_as_2021_2025.csv)
4. **File Format & Size**: CSV, **18.28 MB** (19,171,861 bytes)
5. **Record Count**: **137,659 rows**, 20 columns
6. **Temporal Coverage**: `2021-01-01` to `2025-12-31` (Hourly observation timestamps)
7. **Spatial Footprint**:
   - State: Assam (`State LGD Code: 18`)
   - Basin: `Barak and Others`, `Brahmaputra`
   - **40 Unique Telemetry Rain Gauge Stations**: AP Ghat, BAHALPUR, Basudevthan, Beki Road bridge, Bokajan, Chenimari (Khowang), Chouldhowaghat, Desangpani, Dharamtul, Dholabazar, Golaghat, Guwahati, Margherita, Numaligarh, Panbari, etc.
   - Precise Geodetic Coordinates: Latitudes ($24.83^\circ\text{N}$ to $27.98^\circ\text{N}$), Longitudes ($89.85^\circ\text{E}$ to $95.82^\circ\text{E}$)
8. **Observed Variables**:
   - `Station`, `Agency`, `State`, `District`, `River`, `Basin`, `Latitude`, `Longitude`
   - `Data Acquisition Time` (Format: `DD-MM-YYYY HH:MM`)
   - `Telemetry Hourly Rainfall (mm)`
9. **Data Quality & Missingness**:
   - Zero missing coordinates across all 137k rows.
   - Non-negative rainfall verified ($RF \ge 0.0$ mm).
   - Expected seasonal dry-season zeroes correctly represented.
10. **Suitability & Verdict**: **READY_FOR_PROCESSING** (Exceptional high-resolution precipitation influx driver for Assam).

---

### Dataset 2: CWC Assam Telemetry Hourly River Water Level (2021–2025)

1. **Source Agency**: Central Water Commission (CWC) / Assam Water Department
2. **Official Source URL**: `https://nwdp.nwic.gov.in/dataset/river-water-level-telemetry-hourly-assam-department`
3. **Local Storage Path**: [`datasets/raw/cwc/river_level/rwl_tel_hr_assam_999_2021_2025.csv`](datasets/raw/cwc/river_level/rwl_tel_hr_assam_999_2021_2025.csv)
4. **File Format & Size**: CSV, **10.07 MB** (10,558,346 bytes)
5. **Record Count**: **78,212 rows**, 23 columns
6. **Temporal Coverage**: `2022-02-26 17:00` to `2025-01-31` (Hourly telemetry sequence)
7. **Spatial Footprint**:
   - State: Assam (`State LGD Code: 18`)
   - Districts: Udalguri, Kamrup, Barpeta
   - **3 Dedicated Telemetry River Gauge Stations**:
     - `NH15 Crossing Dhansirighat` (Lat: $26.6958^\circ\text{N}$, Lon: $92.2578^\circ\text{E}$)
     - `NH15 Crossing Fakirpara Tangni` (Lat: $26.5417^\circ\text{N}$, Lon: $91.8972^\circ\text{E}$)
     - `NH17 Crossing Boko` (Lat: $25.9819^\circ\text{N}$, Lon: $91.2139^\circ\text{E}$)
8. **Observed Variables**:
   - `Station`, `Agency`, `State`, `District`, `Latitude`, `Longitude`
   - `MeanSeaLevel`, `RL_of_zeroGauge`, `Is_DischargeDataAvailable`
   - `Data Acquisition Time` (Format: `DD-MM-YYYY HH:MM`)
   - `River Water Level Telemetry Hourly (meter)`
9. **Data Quality & Hydrograph Dynamics**:
   - Continuous hourly records capturing water stage fluctuations.
   - Gauge elevation readings range from $0.15$ m to $5.80$ m depending on monsoon stage.
   - Rate of rise calculation (`river_level_change_6h`, `river_level_change_24h`) supported.
10. **Suitability & Verdict**: **READY_FOR_PROCESSING** (Primary hydrological river stage backbone for Assam catchment flood modeling).

---

### Dataset 3: IMD District-wise Daily Observed Rainfall

1. **Source Agency**: India Meteorological Department (IMD) / NWDP
2. **Official Source URL**: `https://www.nwdp.nwic.gov.in/en/dataset/rainfall-daily-imd`
3. **Local Storage Path**: [`datasets/raw/imd/rainfall_districtwise_daily_imd.csv`](datasets/raw/imd/rainfall_districtwise_daily_imd.csv)
4. **File Format & Size**: CSV, **2.88 MB** (3,023,860 bytes)
5. **Record Count**: **36,371 rows**, 22 columns
6. **Temporal Coverage**: Recent operational season (`2026-08-19` to `2026-09-12`)
7. **Spatial Footprint**: All 36 Indian States & Union Territories (district-level administrative aggregation, including all 35 Assam districts).
8. **Observed Variables**:
   - `State`, `District`, `Date`
   - `Daily Actual` (mm), `Daily Normal` (mm), `Daily Departure Per` (%)
   - `Weekly Actual`, `Weekly Normal`, `Cumulative Actual`, `Cumulative Normal`
9. **Role in RISK // INDIA Pipeline**:
   - Evaluated as: **Cross-Validation / Benchmark Reference Source**.
   - Provides Long Period Average (LPA) precipitation departures (`rainfall_anomaly`) and district-level normal baselines.
10. **Suitability & Verdict**: **READY_FOR_PROCESSING** (Reference anomaly and cross-validation source).

---

### Dataset 4: ISRO / NRSC Bhuvan Flood Inundation & Hazard Maps

1. **Source Agency**: National Remote Sensing Centre (NRSC), ISRO
2. **Official Source Portal**: `https://bhuvan-app1.nrsc.gov.in/disaster/usrtasks/flood/flood.php?uname=empty`
3. **Local Storage Path**: `datasets/raw/isro/flood_inundation/` and `datasets/raw/isro/flood_hazard/`
4. **Status**: **AWAITING MANUAL DOWNLOAD**
5. **Portal Architecture & Delivery Format**:
   - Bhuvan serves inundation data via an interactive Web GIS application (1.2 MB client-side application) and OGC Web Map Service (WMS) endpoints (`https://bhuvan-gp1.nrsc.gov.in/bhuvan/gwc/service/wms`).
   - Satellite inundation polygons are captured as discrete event-based overpasses (Sentinel-1 SAR / RISAT-1A).
   - Downloading spatial vector layers requires interactive user selection of State -> Year -> Event in the portal UI or an authenticated GIS session.
6. **Ground-Truth Label Strategy**:
   - **Label Extraction Requires GIS / Raster Processing**: The raw satellite outputs are spatial vector polygons or georeferenced raster masks.
   - For machine learning supervision, satellite overpass inundation extents can be spatially intersected with the 40 CWC rain gauge and river stage catchment buffers to establish positive ground-truth flood instances ($1 = \text{Flooded}$).
   - Exact download steps are documented in [`datasets/raw/README.md`](datasets/raw/README.md).
7. **Suitability & Verdict**: **MANUAL_DOWNLOAD_REQUIRED**

---

## 2. Multi-Dataset Alignment Feasibility (Assam Pilot)

```
┌────────────────────────────────────────────────────────────────────────┐
│               ASSAM PILOT MULTI-SOURCE INTEGRATION                     │
├──────────────────────┬────────────────────────┬────────────────────────┤
│ Stream               │ Temporal Resolution    │ Spatial Linkage        │
├──────────────────────┼────────────────────────┼────────────────────────┤
│ CWC Hourly Rainfall  │ Hourly (137k records)  │ 40 Assam Stations      │
│                      │ 2021–2025              │ (Lat/Lon geocoded)     │
├──────────────────────┼────────────────────────┼────────────────────────┤
│ CWC Hourly River WL  │ Hourly (78k records)   │ 3 River Gauges         │
│                      │ 2022–2025              │ (Dhansirighat, Boko)   │
├──────────────────────┼────────────────────────┼────────────────────────┤
│ IMD Daily Rainfall   │ Daily (36k records)    │ District LGD Mapping   │
│                      │ Regional departure     │ (Anomaly baselines)    │
└──────────────────────┴────────────────────────┴────────────────────────┘
```

The temporal alignment utilities developed in Phase 4 ([`temporal_align.py`](ml/data/alignment/temporal_align.py)) resample hourly telemetry into daily hydrological features (`rainfall_1d`, `rainfall_3d`, `rainfall_7d`, `river_level_change_24h`, `river_level_24h_max`), and [`spatial_join.py`](ml/data/alignment/spatial_join.py) connects stations to districts via Haversine distance.

---

## 3. Pilot Dataset Decisions

| Dataset Identifier | Source | Actual Data Present? | Size & Rows | Decision Verdict |
| :--- | :--- | :--- | :--- | :--- |
| `cwc_rainfall_assam_hourly` | CWC / NWDP | **YES** | 18.28 MB / 137,659 rows | **READY_FOR_PROCESSING** |
| `cwc_river_level_assam_hourly`| CWC / NWDP | **YES** | 10.07 MB / 78,212 rows | **READY_FOR_PROCESSING** |
| `imd_rainfall_districtwise` | IMD / NWDP | **YES** | 2.88 MB / 36,371 rows | **READY_FOR_PROCESSING** |
| `isro_bhuvan_flood_inundation`| ISRO / NRSC | **NO (Web GIS)**| Pending manual export | **MANUAL_DOWNLOAD_REQUIRED** |
| `isro_bhuvan_flood_hazard` | ISRO / NRSC | **NO (Web GIS)**| Pending manual export | **MANUAL_DOWNLOAD_REQUIRED** |

---

## 4. Machine Learning & Training Governance

> [!IMPORTANT]
> **NO MODEL TRAINING EXECUTED IN THIS PHASE**:
> In strict compliance with the Phase 5 specification:
> - Zero machine learning models were trained.
> - Zero synthetic data or artificial flood labels were generated.
> - Zero fake accuracy numbers or predictions were produced.
> 
> The project has successfully crossed the threshold from simulated prototypes to **authentic, verified Government of India observational telemetry**.
