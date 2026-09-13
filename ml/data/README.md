# RISK // INDIA — Data Engineering & EDA Pipeline

This package implements the ingestion, schema validation, quality reporting, spatial/temporal alignment, and exploratory data analysis (EDA) pipeline for **RISK // INDIA**.

---

## 1. Directory Structure

```
ml/data/
├── __init__.py
├── README.md                      # Architecture documentation
├── ingestion/                     # Official Indian data loaders
│   ├── __init__.py
│   ├── imd_loader.py              # IMD gridded and station rainfall loader
│   ├── cwc_rainfall_loader.py     # CWC telemetry rainfall loader
│   ├── cwc_water_level_loader.py  # CWC hourly river gauge water level loader
│   └── isro_flood_loader.py       # ISRO/NRSC Bhuvan flood inundation loader
├── validation/                    # Validation & diagnostic audit suite
│   ├── __init__.py
│   ├── schema_validation.py       # Flexible concept mapping & type validation
│   ├── quality_report.py          # Non-destructive quality audit reporter
│   └── spatial_validation.py      # Sovereign Indian coordinate verification
├── alignment/                     # Spatial & temporal alignment engine
│   ├── __init__.py
│   ├── spatial_join.py            # Haversine nearest station matching
│   └── temporal_align.py          # IST/UTC normalization & multi-scale aggregation
├── features/                      # Domain hydrological feature engineering
│   ├── __init__.py
│   ├── rainfall_features.py       # Rolling accumulation (1d, 3d, 7d, 14d)
│   └── river_features.py          # River stage rate of rise (6h, 24h, 24h peak)
└── eda/                           # Statistical profiling & visualization
    ├── __init__.py
    ├── inspector.py               # Statistical profiler (rows, cols, percentiles)
    └── visual_eda.py              # Matplotlib visualizer (hydrographs, rain series)
```

---

## 2. Ingestion Loaders

Every loader conforms to a standard interface:
- `discover_raw_files()`: Scans the respective `datasets/raw/` subdirectory.
- `load_file(path)`: Ingests, normalizes column names, checks schema concepts, runs data quality reporting, and outputs standardized dataframes.
- `status()`: Reports whether raw source files are present or `"AWAITING_SOURCE_DATA"`.

Loaders do not hardcode assumptions about column naming; they use `schema_validation.py` to map synonyms (e.g. `rf_mm`, `rainfall`, `rain_mm` -> `rainfall_mm`).

---

## 3. Hydrological Feature Engineering

- **Rainfall Accumulations** (`ml/data/features/rainfall_features.py`):
  - `rainfall_1d`: 24h accumulation.
  - `rainfall_3d`: 72h antecedent saturation (critical soil pore water indicator).
  - `rainfall_7d`: Weekly basin infiltration.
  - `rainfall_14d`: Bi-weekly catchment soaking.
- **River Dynamics** (`ml/data/features/river_features.py`):
  - `river_level_change_6h`: 6-hour rate of rise (identifies rapid storm runoff).
  - `river_level_change_24h`: 24-hour diurnal rate of rise.
  - `river_level_24h_max`: 24-hour peak hydrograph stage.
  - `river_level_above_danger`: Gauge height relative to CWC danger level.

---

## 4. Multi-Source Alignment Engine

The pipeline prepares for uniting disparate data sources:
```
IMD Daily Rainfall  ──┐
                      ├─► Temporal Harmonization (IST Daily) ──► Unified Feature Matrix
CWC Hourly Telemetry ─┘                    ▲
                                           │
ISRO Inundation Layer ─────────────────────┴─► Spatial Haversine Matching / Grouping
```

---

## 5. Non-Destructive Quality Rule

> [!IMPORTANT]
> Raw observations containing suspicious jumps, extreme spikes, or gaps are cataloged in `quality_report.py` rather than silently purged. Silent deletion introduces survivorship bias and conceals telemetry failure modes.
