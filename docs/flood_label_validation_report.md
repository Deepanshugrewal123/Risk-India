# Flood Ground-Truth Validation & Quality Report — RISK // INDIA (Assam Pilot)

**Phase**: 7 — Real Flood Ground-Truth Acquisition & Label Alignment  
**Evaluation Date**: September 12, 2026  
**Status**: AUDITED — NO REAL ISRO LABELS PRESENT LOCALLY  
**Readiness Verdict**: **NOT_READY — FLOOD LABEL DATA REQUIRED**  
**Training Readiness**: `TRAINING_READY = False`  

---

## 1. Dataset Inventory

A physical filesystem audit of [`datasets/raw/isro/`](datasets/raw/isro/) was conducted across all designated subdirectories:

| Subdirectory | Expected Product Category | Files Discovered | Machine-Readable Files | Visual Files | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `datasets/raw/isro/flood_inundation/` | Event-specific satellite SAR inundation vectors | 1 (`.gitkeep`) | 0 | 0 | **AWAITING DATA** |
| `datasets/raw/isro/flood_hazard/` | Multi-temporal flood hazard zonation layers | 1 (`.gitkeep`) | 0 | 0 | **AWAITING DATA** |
| `datasets/raw/isro/metadata/` | Sensor calibration & activation bulletins | 1 (`.gitkeep`) | 0 | 0 | **AWAITING DATA** |

**Summary**: Exactly **0 machine-readable vector or raster flood observation files** are currently available in the project workspace.

---

## 2. Source Provenance

- **Intended Agency**: National Remote Sensing Centre (NRSC), Indian Space Research Organisation (ISRO).
- **Target Products**:
  1. Bhuvan Disaster Management Support Program (DMSP) Flood Inundation Layers.
  2. NRSC Flood Hazard Zonation Atlas of Assam State.
- **Sensors**: Sentinel-1A/1B (C-band SAR), RISAT-1A (C-band SAR), Resourcesat-2 (AWiFS/LISS-III).
- **Current Acquisition State**: External manual GIS vector export from Bhuvan portal is pending. Provenance cannot be verified until physical files are deposited.

---

## 3. Spatial Coverage

- **Target Pilot Region**: Assam, India.
- **Geographic Bounding Box**: Latitude 24.0°N to 28.5°N, Longitude 89.5°E to 96.5°E.
- **Monitored River Corridors**: Brahmaputra and Barak river floodplains.
- **Current Verified Extent**: 0 sq km (no spatial geometries deposited).

---

## 4. Temporal Coverage

- **Target Historical Pilot Period**: 2021 to 2025 (matching CWC rainfall and river stage observations).
- **Discovered Date Range**: `NONE` (no satellite event dates recorded in raw directory).

---

## 5. Number of Flood Observations & Events

- **Discovered Polygons**: 0
- **Identified Flood Events**: 0
- **Positive Labels Generated**: 0
- **Integrity Compliance**: Zero fake event IDs or synthetic labels were created.

---

## 6. CRS Validation

- **Pipeline CRS Standard**: **EPSG:4326 (WGS 84)** longitude/latitude coordinates.
- **Automated Validation Rule**: The ingestion engine (`ISROFloodInundationLoader`) verifies that coordinates fall within `[-180, 180]` and `[-90, 90]` and intersect Assam's bounding box. Projected Cartesian coordinates (e.g. UTM meters) without explicit CRS declarations are rejected automatically.
- **Current Dataset Result**: N/A (0 files to validate).

---

## 7. Geometry Validity

- **Topological Integrity Rules**:
  - Minimum 4 points per polygon coordinate ring.
  - Closed coordinate rings (first coordinate == last coordinate).
  - Valid boundary orientations and non-degenerate geometries.
- **Current Dataset Result**: N/A (0 geometries).

---

## 8. Duplicate Analysis

- **Deduplication Engine**: `FloodEventBuilder.detect_duplicates()` eliminates identical coordinate strings occurring on the same date and district.
- **Duplicate Observations Detected**: 0 (no data).

---

## 9. Event Grouping

- **Grouping Strategy**: Multi-swath observations sharing the same date and administrative district / river corridor are consolidated into unified disaster event envelopes.
- **Grouped Disaster Events**: 0

---

## 10. Spatial Matching Results

- **Hierarchy Established**:
  1. Exact spatial intersection
  2. Station catchment buffer intersection (15–25 km)
  3. Documented nearest-station matching with distance & quality metrics
  4. Inverse Distance Weighting (IDW) catchment precipitation interpolation
- **Matched Predictor Stations**: 0 (awaiting event polygons).

---

## 11. Temporal Matching Results

- **Candidate Predictor Windows**: 6 hours, 24 hours, 72 hours, 168 hours.
- **Zero Temporal Leakage Enforcement**: Every extraction enforces \(t_{\text{predictor}} \le t_{\text{event}}\).
- **Matched Temporal Events**: 0

---

## 12. Predictor Coverage

The available predictor datasets in [`datasets/interim/`](datasets/interim/) and [`datasets/raw/`](datasets/raw/) were forensically evaluated for eventual alignment:

| Predictor Dataset | Source | Time Period | Usable Records | Active Stations / Gauges | Quality Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cleaned Hourly Rainfall** | CWC | 2021-01-01 to 2025-12-30 | **35,309 rows** | 31 active stations | Cleaned, 0 nulls, 861 spikes flagged (>150mm/hr) |
| **Hourly River Water Level** | CWC | 2022-01-01 to 2025-09-17 | **76,368 valid rows** | 3 highway bridge gauges | Despiked, datum-invariant transformations ready |
| **District-wise Daily Rainfall** | IMD | 2026-08-19 to 2026-09-12 | 825 Assam rows | 33 districts | Incompatible with 2021–2025 historical events (0 days overlap) |

---

## 13. Missingness & Sufficiency

- **Feature Window Sufficiency Rule**: Antecedent rainfall windows require \(\ge 70\%\) data completeness over the evaluated duration. Windows with sparse observations are flagged as `INSUFFICIENT_COVERAGE` and set to `None`.
- **Current Label Missingness**: **100% of ground-truth labels are currently missing locally**.

---

## 14. Negative Sampling Status

- **Strategy Protocol**: Non-flood negative examples (`flood_presence = 0`) must **never** be generated naively for all non-flood days.
- **Contamination Buffer**: Negative samples require a temporal buffer of \(\pm 7\text{ days}\) and spatial buffer of \(\ge 30\text{ km}\) around known flood events.
- **Operational Verdict**:
  - `POSITIVE_LABELS_AVAILABLE`: **`False`** (0 positive events exist)
  - `NEGATIVE_LABELS_NOT_READY`: **`True`** (Defensible exclusion zones cannot be drawn without knowing positive flood boundaries)
  - **Negative labels generated**: 0

---

## 15. Known Satellite Observation Limitations

When real ISRO data is ingested, the following physical remote sensing limitations will be documented:
1. **Satellite Revisit Latency**: Synthetic Aperture Radar (SAR) constellations revisit the same orbital ground track every 2 to 6 days. Fast flash floods peaking and receding within 12–24 hours may not be recorded at peak crest.
2. **Post-Peak Water Ponding**: Observations acquired 48–72 hours after heavy storms may depict standing floodwater rather than dynamic channel overflow.
3. **Radar Backscatter Attenuation**: Dense forest canopies and dense urban infrastructure impede C-band microwave backscatter, leading to potential under-detection in forested riverbanks.
4. **Cloud Cover**: Optical sensors (e.g., AWiFS, LISS-III) are blinded by dense monsoon convective cloud decks.

Labels must be classified as:
> **"Satellite-observed flood inundation" — NOT "perfect ground truth"**

---

## 16. Final Readiness Decision

```
================================================================================
FINAL READINESS GATE EVALUATION:
================================================================================
TRAINING_READY: False
STATUS: NOT_READY — FLOOD LABEL DATA REQUIRED
CRITICAL BLOCKERS:
1. Zero machine-readable ISRO/NRSC flood inundation files exist in datasets/raw/isro/.
2. Positive flood event labels are not available.
3. Defensible negative samples cannot be generated without positive flood exclusion zones.
================================================================================
```

**Next Action**: Execute manual acquisition as specified in [`docs/flood_label_manual_acquisition.md`](docs/flood_label_manual_acquisition.md).
