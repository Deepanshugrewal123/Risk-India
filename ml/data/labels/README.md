# Flood Ground-Truth Label Architecture — RISK // INDIA

This package manages the ingestion, forensic validation, event grouping, spatial/temporal alignment, and negative sampling of authoritative satellite flood inundation observations from ISRO, NRSC, and Bhuvan.

---

## 1. Directory Structure

```
ml/data/labels/
├── __init__.py                 # Package exports
├── label_schema.py             # Canonical Pydantic schemas (FloodEventLabel, QualityReport)
├── isro_flood_loader.py        # Machine-readable parser & CRS/geometry validator
├── event_builder.py            # Multi-swath event grouping & duplicate detection
├── spatial_labeling.py         # Catchment buffer intersection engine
├── negative_sampler.py         # Defensible negative sampler with +/- 7-day exclusion buffer
├── check_label_readiness.py    # Automated 10-criteria readiness gate
├── run_label_pipeline.py       # Single-command end-to-end pipeline runner
└── README.md                   # This specification document

tests/
└── test_flood_label_pipeline.py # 11-case test suite verifying integrity guards
```

---

## 2. Standard Label Schema (`FloodEventLabel`)

```json
{
  "event_id": "FE_BHUVAN_2022_06_18_001",
  "event_date": "2022-06-18",
  "location_id": "NH15 Crossing Fakirpara Tangni",
  "location_type": "GAUGE_CATCHMENT",
  "geometry_source": "ISRO_NRSC_BHUVAN",
  "flood_observed": 1,
  "source_product": "Sentinel-1A SAR Inundation Layer",
  "source_url": "https://bhuvan-app1.nrsc.gov.in/disaster/usrtasks/flood/flood.php",
  "spatial_resolution": "10m-30m SAR",
  "confidence": "OBSERVED_SATELLITE",
  "inundated_area_sqkm": 28.45
}
```

---

## 3. Acceptable Formats vs. Rejected Visual Maps

| Category | File Extensions | Handling Protocol |
| :--- | :--- | :--- |
| **Machine-Readable Vectors** | `.geojson`, `.json`, `.shp`, `.gpkg` | **ACCEPTED**. Ingested directly into spatial intersection engine after CRS validation (EPSG:4326). |
| **Machine-Readable Rasters** | `.tif`, `.tiff` (GeoTIFF) | **ACCEPTED**. Georeferenced raster extraction supported. |
| **Visual Maps / Documents** | `.jpg`, `.jpeg`, `.png`, `.pdf`, `.bmp` | **STRICTLY REJECTED**. Flagged as `MANUAL GIS EXTRACTION REQUIRED`. Vectorization via QGIS required. |

---

## 4. Defensible Negative Sampling Protocol

- **Zero Contamination**: Rejects negative samples within \(\pm 7\text{ days}\) and \(\ge 30\text{ km}\) of any verified positive flood event.
- **Readiness Guard**: If 0 positive flood events exist, negative sampling safely halts with `NEGATIVE_LABELS_NOT_READY = True` rather than generating fabricated non-flood labels.

---

## 5. Execution Commands

### Run Automated Unit Test Suite:
```bash
python -m unittest tests/test_flood_label_pipeline.py
```

### Check Label Readiness Gate:
```bash
python ml/data/labels/check_label_readiness.py
```

### Run End-to-End Pipeline:
```bash
python ml/data/labels/run_label_pipeline.py
```
*(Fails loudly with clear guidance if raw ISRO files are missing from `datasets/raw/isro/`).*
