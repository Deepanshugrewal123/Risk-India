# RISK // INDIA — Datasets Directory Architecture

This directory houses raw, interim, processed datasets and source metadata for the **RISK // INDIA** disaster risk modeling platform.

---

## 1. Directory Structure

```
datasets/
├── raw/                           # IMMUTABLE raw files as obtained from source agencies
│   ├── imd/                       # India Meteorological Department precipitation records
│   ├── cwc/                       # Central Water Commission river stage & rainfall telemetry
│   └── isro/                      # ISRO / NRSC / Bhuvan flood inundation hazard layers
│
├── interim/                       # Cleaned, standardized, and type-validated intermediate datasets
├── processed/                     # Spatially and temporally joined matrices ready for modeling
│
├── metadata/                      # Machine-readable JSON metadata for every dataset source
│   ├── imd_rainfall_metadata.json
│   ├── cwc_telemetry_metadata.json
│   └── isro_bhuvan_flood_metadata.json
│
└── README.md                      # Architecture and data governance policy
```

---

## 2. Immutability Policy for Raw Data

> [!IMPORTANT]
> **STRICT IMMUTABILITY RULE**:
> Files placed in `datasets/raw/` must **NEVER** be modified, overwritten, or re-formatted in place.
> All data cleaning, timestamp standardization, unit conversions, and spatial joins must write their outputs to `datasets/interim/` or `datasets/processed/`.

---

## 3. Data Ingestion Standards

1. **No Synthetic Records**: Under no circumstances should randomly generated records be stored or substituted for real data.
2. **Metadata Requirement**: Every dataset ingested into `datasets/raw/` must have a corresponding `.json` metadata file in `datasets/metadata/` describing its source agency, collection window, spatial/temporal resolution, and access notes.
3. **Unknowns Explicitly Marked**: If a metadata field is unknown, specify `"UNKNOWN"`. Never guess or fabricate metadata attributes.
