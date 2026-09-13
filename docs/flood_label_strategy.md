# Flood Ground-Truth Label Strategy — RISK // INDIA (Assam Pilot)

**Phase**: 6 — Flood Ground-Truth Label Pipeline Preparation  
**Status**: COMPLETE — PIPELINE ARCHITECTURE READY  
**Label Readiness Verdict**: **NOT_READY — FLOOD LABEL DATA REQUIRED**  
**Date**: September 12, 2026  

---

## 1. Selected Label Source

The primary candidate label source for RISK // INDIA is the **ISRO / NRSC / Bhuvan Disaster Management Support (DMS) Historical Flood Inundation & Hazard Mapping Service**, administered by the National Remote Sensing Centre (NRSC), Indian Space Research Organisation (ISRO).

Key source products identified:
- **Bhuvan Satellite Flood Inundation Layers** (Event-specific SAR activations from Sentinel-1A and RISAT-1A).
- **Flood Annual Layers & Cumulative Inundation Composites** (State-level seasonal inundation footprints).
- **Flood Hazard Zonation Atlas of Assam State** (Multi-decadal frequency zonation across all 35 Assam districts).

---

## 2. Why It Was Selected

1. **Authoritative National Standard**: ISRO/NRSC flood inundation products represent the official ground truth utilized by the National Disaster Management Authority (NDMA), Central Water Commission (CWC), and Assam State Disaster Management Authority (ASDMA).
2. **Physical Inundation Verification**: Hydrological river levels and meteorological rainfall alone cannot prove surface inundation. Ground truth requires independent observation that floodwaters overtopped natural banks or breached embankments.
3. **All-Weather Synthetic Aperture Radar (SAR)**: Active microwave C-band SAR sensors penetrate torrential monsoon cloud cover, providing dependable surface water delineation where optical satellites fail.
4. **Zero Fabrication**: Relying on official satellite observations prevents the dangerous pitfall of inventing arbitrary flood labels or fabricating training targets.

---

## 3. Label Format & Standard Schema

All ground-truth labels are standardized via the canonical Pydantic model `FloodEventLabel` defined in `ml/data/labels/label_schema.py`:

```json
{
  "event_id": "FE_BHUVAN_2022_06_18_001",
  "event_date": "2022-06-18",
  "location_id": "NH15 Crossing Fakirpara Tangni",
  "location_type": "GAUGE_CATCHMENT",
  "geometry_source": "ISRO_NRSC_BHUVAN",
  "flood_observed": 1,
  "source_product": "Sentinel-1A SAR Flood Inundation Layer",
  "source_url": "https://bhuvan-app1.nrsc.gov.in/disaster/usrtasks/flood/flood.php",
  "spatial_resolution": "10m-30m SAR",
  "confidence": "OBSERVED_SATELLITE",
  "inundated_area_sqkm": 28.45,
  "intersection_fraction": 0.142,
  "metadata": {
    "sensor": "Sentinel-1A C-SAR",
    "district": "DARRANG",
    "orbit": "Ascending"
  }
}
```

### Acceptable File Formats:
- **Machine-Readable Vectors**: GeoJSON (`.geojson`, `.json`), ESRI Shapefile (`.shp`), GeoPackage (`.gpkg`).
- **Machine-Readable Classified Rasters**: GeoTIFF (`.tif`, `.tiff`).
- **Rejected Visual Formats**: `.jpg`, `.png`, `.pdf` bulletins. Flagged strictly as `MANUAL GIS EXTRACTION REQUIRED`.

---

## 4. Spatial Labeling Strategy

Four spatial labeling strategies are supported by `SpatialLabeler` (`ml/data/labels/spatial_labeling.py`):

1. **`GAUGE_CATCHMENT` (Recommended Prototype)**:
   - Evaluates a 15–25 km circular/hydrological buffer around CWC river level telemetry bridge gauges (`NH15 Crossing Fakirpara Tangni`, `NH17 Crossing Boko`, `NH15 Crossing Dhansirighat`).
   - *Reasoning*: River gauges directly measure water stage. Associating inundation within their immediate catchment provides the cleanest physical cause-and-effect relationship between river cresting and overland flooding.
2. **`STATION_CATCHMENT`**:
   - 15–20 km buffer around the 31 active CWC rainfall telemetry stations.
3. **`DISTRICT`**:
   - Evaluates intersection across administrative district boundaries. Useful for macro-level warnings, but risks spatial dilation (treating an entire 3,000 sq km district as uniformly flooded when water is confined to a 50 sq km riparian zone).
4. **`GRID_PIXEL`**:
   - High-resolution (1 km x 1 km) regular spatial lattice reserved for future 2D hydrodynamic simulation.

---

## 5. Temporal Alignment Strategy

The `TemporalEventAligner` (`ml/data/alignment/temporal_alignment.py`) coordinates event dates with preceding environmental telemetry:

```
[ T - 168h ] ──────────► [ T - 72h ] ──────────► [ T - 24h ] ──────────► [ T (Event Date) ]
     │                        │                       │                         │
     └────── rainfall_168h ───┴───── rainfall_72h ────┴──── rainfall_24h ───────┤
                                                                                ├─ river_level(T)
                                                                                └─ rate_of_rise(24h)
```

For every target date \(T\):
- Cumulative rainfall is extracted over the preceding 24h, 72h, and 168h windows.
- Concurrent river stage at or immediately preceding \(T\) is captured.
- 24-hour rate of rise is computed: \(\Delta H_{24h} = H_T - H_{T-24h}\).

---

## 6. Negative Sampling Strategy

Naive negative sampling (labeling every unrecorded day or district as `flood_observed = 0`) is **scientifically invalid** in satellite remote sensing because satellite revisit cycles are intermittent (2–6 days), and cloud cover frequently obscures optical sensors.

### Defensible Negative Sampling Protocol:
1. **Confirmed Satellite Swath Pass**: A negative label (`flood_observed = 0`) is generated **only** for location catchments that fell directly within the confirmed swath footprint of an active satellite pass.
2. **Zero Inundation Verification**: The spatial intersection engine verifies that the catchment polygon has 0% overlap with observed surface water.
3. **Explicit Confidence Tag**: Tagged as `confidence: NEGATIVE_VERIFIED_PASS`.
4. **Unobserved Days Omitted**: Days without satellite passes (or passes with 100% cloud cover over the location) are left **unassigned / unobserved**, completely preventing false non-flood negatives from polluting the training set.

---

## 7. River Water Level Datum Normalization Strategy

The forensic audit revealed that CWC river crossing gauges experienced a datum shift from relative stage (~1–3m above zero gauge) in 2022–2023 to bridge benchmark / MSL elevation (~30–80m) in 2024–2025, alongside 32 digital bit-corruption spikes (> 100m, up to 1,018.6m).

To enable long-term multi-year modeling without altering raw source data, `river_datum_normalizer.py` implements four datum-invariant mathematical transformations:

1. **Rate of Rise (\(\Delta H\))**:
   \[
   \Delta H_t = H_t - H_{t - \text{lag}}
   \]
   First-order differencing is mathematically invariant to constant vertical datum translation.
2. **Rolling Baseline Deviation**:
   \[
   \text{Dev}_t = H_t - \text{median}_{14d}(H)
   \]
   Removes low-frequency elevation datum shifts while isolating acute storm hydrograph crests.
3. **Segmented Standardization (Era z-score)**:
   \[
   z = \frac{H - \mu_{\text{era}}}{\sigma_{\text{era}}}
   \]
   Standardizes separately for Era 1 (Pre-2024: relative stage) and Era 2 (Post-2024: MSL elevation).
4. **Percentile-Based Relative Stage**:
   Ranks hourly readings within their respective station and era on a continuous \([0.0, 1.0]\) scale.
5. **Despiking Rule**: Flags and excludes physical impossibilities (\(H > 100\text{ m}\)) from baseline computations.

---

## 8. Leakage Prevention Protocol

Temporal leakage occurs when information from the future (or during the event) leaks into predictors:
- **Strict Causality Rule**: Every feature extraction enforces \(t_{\text{predictor}} \le t_{\text{event}}\).
- **Post-Event Data Banned**: Precipitation or water level logged after the satellite observation timestamp is strictly prohibited from entering antecedent feature vectors.
- **Automated Verification**: `TemporalEventAligner` validates `temporal_leakage_prevented == True` on every extraction.

---

## 9. Label Limitations & Honest Quality Standards

Flood labels are explicitly classified as:
> **"Satellite-observed flood inundation" — NOT "perfect ground truth"**

Key physical limitations:
1. **Orbital Revisit Latency**: Satellites pass every 2 to 6 days. Fast-rising flash floods that peak and recede within 12–24 hours may not be captured at peak extent.
2. **Post-Peak Observation**: A satellite pass 48 hours after a storm may capture residual standing ponding rather than the maximum dynamic stage.
3. **Canopy & Urban Backscatter**: Dense tree canopies and built-up settlements impede microwave radar backscatter, occasionally causing underestimation of sub-canopy inundation.
4. **Cloud Obscurity**: Heavy cloud cover blinds optical sensors (e.g. Landsat, Sentinel-2), making SAR (Sentinel-1, RISAT-1A) the only reliable source during monsoon storms.

---

## 10. Manual Data Acquisition Requirement

Machine-readable flood polygons are not currently available via open REST API endpoints and must be manually retrieved or exported.

The complete standard operating procedure is documented in [`docs/flood_label_manual_acquisition.md`](docs/flood_label_manual_acquisition.md).

---

## 11. Exact Readiness Status

```
================================================================================
FLOOD GROUND TRUTH READINESS VERDICT:
NOT_READY — FLOOD LABEL DATA REQUIRED
================================================================================
```

- **Pipeline Architecture**: Fully designed, implemented, and verified in `ml/data/labels/`, `ml/data/alignment/`, and `ml/data/cleaning/`.
- **CWC Rainfall Cleaning**: Completed (`datasets/interim/cwc_rainfall_assam_hourly_cleaned.csv` generated with 35,309 valid rows across 31 stations).
- **Physical Ground Truth**: 0 machine-readable flood inundation files currently exist in `datasets/raw/isro/`.
- **Next Required Action**: Follow `docs/flood_label_manual_acquisition.md` to place verified Bhuvan GeoJSON/Shapefiles in `datasets/raw/isro/` before proceeding to model training.
