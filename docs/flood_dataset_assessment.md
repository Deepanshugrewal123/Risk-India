# RISK // INDIA — Authoritative Indian Flood Dataset Assessment Report

**System**: RISK // INDIA: AI-Powered Disaster Risk Analyzer & Management System  
**Phase**: Phase 4 — Real Flood Data Ingestion & Exploratory Data Analysis (EDA)  
**Evaluation Status**: `REAL DATA NOT YET AVAILABLE — MODEL TRAINING BLOCKED.`

---

## Executive Summary

To build a scientifically credible machine learning model for flood risk estimation across India, we have audited the three primary authoritative Indian government hydrological and remote sensing institutions:
1. **India Meteorological Department (IMD)** — Precipitation observations & gridded climatology
2. **Central Water Commission (CWC)** — River stage hydrometry & telemetry gauges
3. **National Remote Sensing Centre (NRSC / ISRO / Bhuvan)** — Satellite flood inundation hazard layers

This assessment documents their technical schemas, data quality considerations, spatio-temporal alignment feasibility, flood label viability, and machine learning suitability.

---

## 1. Candidate Dataset Source Profiles

| Source Agency | Primary Product | Temporal Resolution | Spatial Coverage | Access Regime |
| :--- | :--- | :--- | :--- | :--- |
| **IMD** | 0.25° Gridded Daily Rainfall & AWS Stations | Daily (08:30 IST standard) | Pan-India (6.5°N–37.5°N, 68°E–97.5°E) | Open Govt Data (OGD) / IMD Pune Archive |
| **CWC** | River Stage (m) & Hourly Discharge / ARG | Hourly telemetry / Sub-daily | ~1,600 Major River Basins / Stations | India-WRIS / CWC Flood Forecast Portal |
| **ISRO / NRSC** | Inundation Extent & Flood Hazard Zonation | Discrete event snapshots (2–6 day pass) | Basin-specific (Brahmaputra, Ganga, Mahanadi) | Bhuvan Disaster Services (WMS/GeoJSON) |

---

## 2. Institutional Credibility Assessment

- **India Meteorological Department (IMD)**:  
  **Credibility: Authoritative / Gold Standard**.  
  Operates under the Ministry of Earth Sciences. The 0.25° gridded daily rainfall dataset (Pai et al.) is the standard reference dataset used in Indian monsoon climatology, calibrated against hundreds of quality-controlled rain gauge stations.
- **Central Water Commission (CWC)**:  
  **Credibility: Authoritative / Primary Ground Truth**.  
  Operates under the Ministry of Jal Shakti. Manages national river hydrometry networks and officially designates Warning Level (WL), Danger Level (DL), and High Flood Level (HFL) for Indian river reaches.
- **ISRO / NRSC (National Remote Sensing Centre)**:  
  **Credibility: Authoritative / Space-Borne Ground Truth**.  
  Delineates active inundation using SAR (Sentinel-1, RISAT-1) and optical (Resourcesat-2) sensors under the Disaster Management Support Programme (DMSP).

---

## 3. Detailed Dataset Evaluation

### A. IMD Precipitation Dataset

1. **Variables**:
   - `rainfall_mm` (daily accumulation in mm, 08:30 IST to 08:30 IST)
   - `station_id` / `district` / `state`
   - `latitude`, `longitude`, `date`
2. **Data Quality & Physical Bounds**:
   - Non-negative constraint ($RF \ge 0.0$ mm).
   - Extreme events flagged above IMD criteria: Heavy ($>64.5$ mm), Very Heavy ($>115.5$ mm), Extremely Heavy ($>204.4$ mm).
3. **Strengths for ML**:
   - Unbroken continuous temporal sequence across decades.
   - Standardized 08:30 IST observation cadence avoids irregular sampling bias.
4. **Weaknesses & Gaps**:
   - 0.25° (~27 km) spatial resolution smooths localized convective cloudbursts in mountainous regions (e.g. Western Ghats, Himachal Pradesh, Uttarakhand).
5. **Verdict**: **SUITABLE** (Primary meteorological feature backbone).

---

### B. CWC River Stage Telemetry Dataset

1. **Variables**:
   - `water_level_m` (current gauge elevation in meters above MSL)
   - `danger_level_m` (basin-specific structural threshold)
   - `warning_level_m`
   - `discharge_cumec`
   - `rainfall_hourly_mm`
   - `station_id`, `river_name`, `basin`, `timestamp`
2. **Data Quality & Sensor Anomalies**:
   - Telemetry dropouts during extreme flood peaks (gauges submerged or solar battery drained).
   - Rapid stage jumps ($>5.0$ m/hr) indicating sensor datum shifts or backwater effects.
   - Classification restrictions on certain transboundary river stretches.
3. **Feature Candidates Derived**:
   - `river_level_change_6h`: Rate of river rise indicating flash flood onset.
   - `river_level_change_24h`: Diurnal hydrograph surge.
   - `river_level_above_danger`: Exceedance above river bankfull threshold ($WL - DL$).
   - `river_level_24h_max`: Peak wave crest over preceding 24 hours.
4. **Verdict**: **SUITABLE** (Primary hydrological feature backbone for riverine basins).

---

### C. ISRO / NRSC Bhuvan Flood Inundation & Hazard Maps

1. **Variables**:
   - `inundated_area_sqkm` (extent of surface water coverage)
   - `observation_date` (satellite pass acquisition date)
   - `hazard_severity` (Low, Moderate, High, Very High zonation)
   - `state_name`, `district_name`, vector inundation polygons
2. **Ground Truth Label Viability (`flood_occurred`)**:
   - **Critical Finding**: Satellite inundation masks provide valuable spatial delineations of major flood extents, but are **discrete temporal snapshots** (only captured during satellite overpasses every 2 to 6 days during active disaster activations).
   - Optical imagery is severely obstructed by monsoon cloud cover, necessitating Synthetic Aperture Radar (SAR).
   - Satellite passes often miss the peak crest of flash floods that occur between revisit cycles.
   - True negative labels ($0 = \text{No Flood}$) are ambiguous: non-observation during clear weather may represent either non-flooded conditions or an unmonitored area.
3. **Verdict**: **PARTIALLY SUITABLE** (Suitable as spatial validation and target ground-truth during major documented activations, but **not** as a continuous daily supervisory label without hydrological gauge confirmation).

---

## 4. Multi-Source Alignment Challenges

```
┌────────────────────────────────────────────────────────┐
│               ALIGNMENT BOTTLENECK ANALYSIS            │
├──────────────────────┬─────────────────────────────────┤
│ Challenge            │ Engineering Solution Implemented│
├──────────────────────┼─────────────────────────────────┤
│ Temporal Mismatch    │ Daily harmonization to standard │
│ (Hourly CWC vs       │ 08:30 IST window using          │
│ Daily IMD)           │ resample_hourly_to_daily()      │
├──────────────────────┼─────────────────────────────────┤
│ Spatial Discrepancy  │ Haversine nearest station       │
│ (Point gauges vs     │ matching constrained by maximum │
│ 0.25° grid cells)    │ catchment radius (max 75 km)    │
├──────────────────────┼─────────────────────────────────┤
│ Label Asynchrony     │ Inundation events aligned with  │
│ (Satellite snapshot  │ multi-day antecedent rainfall   │
│ vs continuous time)  │ windows (1d, 3d, 7d)            │
└──────────────────────┴─────────────────────────────────┘
```

---

## 5. Recommended Final Feature Set for Flood Risk Model

When real telemetry files are ingested into `datasets/raw/`, the aligned feature matrix should comprise:

1. `rainfall_1d` (mm) — 24-hour precipitation accumulation
2. `rainfall_3d` (mm) — 72-hour antecedent soil pore saturation
3. `rainfall_7d` (mm) — 7-day cumulative catchment soaking
4. `rainfall_14d` (mm) — 14-day seasonal baseflow influx
5. `river_level_above_danger` (m) — Gauge height relative to CWC danger level
6. `river_level_change_6h` (m) — 6-hour rate of rise (flash flood indicator)
7. `river_level_change_24h` (m) — 24-hour hydrograph trend
8. `elevation` (m) — ISRO CartoDEM digital elevation
9. `slope` (degrees) — Topographic gradient
10. `monsoon_season_flag` (0/1) — Indian Southwest Monsoon indicator (June–September)

---

## 6. Official Institutional Suitability Verdicts

| Dataset Source | Operational Role | Institutional Verdict | Notes |
| :--- | :--- | :--- | :--- |
| **IMD Gridded Daily Rainfall** | Feature Provider | **SUITABLE** | Cleanest national meteorological continuity. |
| **CWC Telemetry River Stage** | Feature Provider | **SUITABLE** | Indispensable for riverine flood warning. |
| **ISRO / NRSC Inundation Maps**| Target Label / Validation | **PARTIALLY SUITABLE**| Snapshot nature requires pairing with CWC danger level exceedance for reliable binary target. |

---

## 7. Machine Learning Readiness Statement

> [!WARNING]
> **REAL DATA NOT YET AVAILABLE — MODEL TRAINING BLOCKED.**
> 
> While the complete data ingestion architecture, schema validators, quality reporting suite, rolling feature calculators, and spatial/temporal alignment engines are verified and operational, **raw telemetry files have not yet been downloaded from government archives into `datasets/raw/`**.
> 
> Per our zero fake intelligence charter, no machine learning model will be trained until real, verified observational records from IMD and CWC are placed into `datasets/raw/` and processed through the pipeline.
