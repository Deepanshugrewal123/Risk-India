# Geospatial & Temporal Alignment — RISK // INDIA

This package provides temporal and spatial alignment utilities linking disparate environmental observation feeds:
- CWC Telemetry Hourly Rainfall (31 active stations)
- CWC Telemetry Hourly River Water Level (3 highway crossing gauges)
- ISRO/NRSC Satellite Flood Inundation Observations

---

## 1. Modules

1. `temporal_alignment.py` (`TemporalEventAligner`):
   - Computes antecedent rainfall windows (24h, 72h, 168h).
   - Computes concurrent river stage and 24h rate of rise (\(\Delta H\)).
   - **Zero Future Leakage**: Strictly ensures that no telemetry logged after the target event timestamp is utilized.
2. `spatial_alignment.py` (`GeospatialAligner`):
   - Vector Haversine distance calculations.
   - Inverse Distance Weighting (IDW) interpolation:
     \[
     P_{\text{gauge}} = \frac{\sum_{i=1}^k w_i P_i}{\sum_{i=1}^k w_i}, \quad w_i = \frac{1}{d_i^p} \quad (p=2.0)
     \]
   - Matches highway crossing river gauges (located in Darrang, Kamrup Metro, Udalguri) to their nearest active precipitation stations in surrounding catchments (44–65 km).

---

## 2. Leakage Prevention Protocol

When evaluating an event on date \(T\):
- **Allowed Predictors**: Observations recorded in \([T - 168\text{h}, T]\).
- **Forbidden Predictors**: Any observation logged after \(T\).
- Every feature extraction checks `temporal_leakage_prevented == True` and verifies `max_predictor_timestamp <= event_timestamp`.
