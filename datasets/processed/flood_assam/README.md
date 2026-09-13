# Assam Flood Pilot — Research Dataset

## Overview
This directory contains the machine-learning-ready ground-truth flood label dataset for the **RISK // INDIA** disaster risk analysis platform (Assam Flood ML Pilot).

- **Dataset Name**: `Assam Flood Pilot — Research Dataset`
- **Version**: `1.0.0-research`
- **Total Observations**: `12`
- **Unit of Analysis**: One observation per event-gauge time window (Catchment tile 20 km × 20 km around active CWC telemetry gauge).

---

## Label Summary

| Metric | Value | Description |
| :--- | :---: | :--- |
| **Total Samples** | `12` | Census of 2022–2025 Tier-1 dual-sensor overlap events |
| **Positive Labels (`1`)** | `8` | Ground-truth flood inundation observed by satellite (6 to 21,610 flood px) |
| **Negative Labels (`0`)** | `4` | Ground-truth non-inundated baseline flow observed by satellite (0 flood px) |
| **High Confidence** | `11` | Fully verified across satellite, gauge, and telemetry |
| **Review Required** | `1` | `BHUVAN_ASSAM_20250628_1100_DHANSIRIGHAT` (Telemetry gap at event hour + backwater 15km east) |
| **Synthetic Records** | `0` | Strictly 0.0% synthetic / fabricated records |
| **Data Leakage** | `NONE` | Strictly `acquisition_time <= event_timestamp` |

---

## File Contents

1. **`labels.csv`**:
   The tabular training label file containing all 12 observation units, labels, bounding box quality, pixel semantics flags, and preceding temporal window counts.
2. **`label_metadata.json`**:
   Full forensic provenance, GeoTIFF checksums, spatial bounds, and detailed temporal availability.

---

## Known Scientific Limitations

> [!WARNING]
> This dataset is designated as a **Research Dataset** for pilot model prototyping. It is **NOT** production-ready or nationally generalizable.
> 
> 1. **Sample Size**: Contains 12 discrete satellite observation windows (8 positive, 4 negative).
> 2. **Regional Pilot**: Restricted to 3 CWC telemetry crossing gauges in Assam (`NH15 Crossing Fakirpara Tangni`, `NH15 Crossing Dhansirighat`, `NH17 Crossing Boko`).
> 3. **Datum Shifts**: CWC gauge datum shifted between 2023, 2024, and 2025. Absolute river stage values must NOT be directly compared across years. Use relative changes (`river_level_change_24h`).
> 4. **Negative Labels**: Negative labels denote confirmed absence of out-of-bank inundation *within the local 20km gauge catchment tile*, not statewide absence of flood.
