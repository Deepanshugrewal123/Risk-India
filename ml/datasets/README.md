# RISK // INDIA — Flood Dataset Specification & Provenance Guide

This document outlines the strict dataset schema, verification criteria, and institutional data sources required to assemble a scientifically valid training and evaluation dataset for the **RISK // INDIA Flood Risk ML Pipeline**.

---

## 1. Zero Synthetic Data Policy

> [!IMPORTANT]
> **Strict Machine Learning Integrity**:
> The RISK // INDIA platform enforces a zero-tolerance policy against using randomly generated synthetic datasets or fabricating model performance benchmarks. Models must only be trained on verified historical hydrological and meteorological observations.

---

## 2. Target Variable Formulation

| Field Name | Type | Allowed Values | Definition |
| :--- | :--- | :--- | :--- |
| `flood_occurred` | Integer / Binary | `0` or `1` | Binary ground-truth indicator of extreme flood occurrence or bank overtopping during the observation window. |

### Scientific Rationale
In raw hydrological and disaster records, floods are recorded as discrete inundation events exceeding threshold river gauge heights (CWC Danger Level) or documented structural inundation (NDMA/SDMA damage reports). Predicting binary occurrence and calibrating the posterior probability $P(\text{Flood} = 1 \mid X)$ allows smooth, defensible transformation to continuous risk scores ($0–100$) and standardized risk tiers without inventing arbitrary multi-class boundaries.

---

## 3. Mandatory Feature Schema & Units

Datasets placed in this directory (e.g. `flood_training_data.csv`) must provide the following columns:

### Tier 1: Core Features (Mandatory)
| Column Name | Type | Unit | Range / Constraints | Recommended Indian Source |
| :--- | :--- | :--- | :--- | :--- |
| `date` | String | ISO Date (`YYYY-MM-DD`) | Chronological sequence | Observation record timestamp |
| `location_id` | String | Identifier | Unique state/district ID | Sovereign Indian administrative code |
| `latitude` | Float | Decimal Degrees | `6.5` to `37.5` | Indian Sovereign Geography |
| `longitude` | Float | Decimal Degrees | `68.0` to `97.5` | Indian Sovereign Geography |
| `rainfall_24h` | Float | mm | $\ge 0.0$ | IMD Automated Weather Stations (AWS) |
| `rainfall_72h_cumulative` | Float | mm | $\ge 0.0$ | IMD 3-day antecedent accumulation |
| `elevation` | Float | meters (a.s.l.) | $-50$ to $9,000$ | ISRO Bhuvan CartoDEM (30m) / SRTM |
| `slope` | Float | degrees | $0.0^\circ$ to $90.0^\circ$ | Topographic gradient from DEM |
| `flood_occurred` | Integer | Binary | `0` or `1` | Ground-truth event label |

### Tier 2: Hydrological & Catchment Features (Optional / Recommended)
| Column Name | Type | Unit | Range / Constraints | Recommended Indian Source |
| :--- | :--- | :--- | :--- | :--- |
| `rainfall_anomaly` | Float | % departure | Typically $-100\%$ to $+500\%$ | IMD Long Period Average (LPA) Departure |
| `soil_moisture_index` | Float | % saturation | $0.0$ to $100.0$ | NASA SMAP / Sentinel-1 / NRSC |
| `river_gauge_above_danger` | Float | meters | Relative to danger mark | Central Water Commission (CWC) |
| `distance_to_river_km` | Float | kilometers | $\ge 0.0$ | Survey of India / HydroSHEDS |
| `historical_flood_frequency`| Integer| count | $\ge 0$ | NDMA / SDMA historical archives |

---

## 4. Institutional Indian Data Sources & Provenance

1. **India Meteorological Department (IMD)**:
   - High-resolution gridded daily rainfall data ($0.25^\circ \times 0.25^\circ$).
   - Automated Weather Stations (AWS) and Automated Rain Gauges (ARG) network.
   - Portal: `https://www.imdpune.gov.in/` / `https://mausam.imd.gov.in/`
2. **Central Water Commission (CWC)**:
   - Daily river stage levels, flood forecast hydrographs, and discharge measurements across major river basins (Ganga, Brahmaputra, Godavari, Krishna, Mahanadi, etc.).
   - Portal: `https://ffs.india-water.gov.in/`
3. **National Remote Sensing Centre (NRSC / ISRO)**:
   - Bhuvan Disaster Services: Flood Inundation Hazard Zonation maps.
   - CartoDEM: High-resolution Indian digital elevation models.
   - Portal: `https://bhuvan-app1.nrsc.gov.in/disaster/disaster.php`
4. **National Disaster Management Authority (NDMA)**:
   - Official post-disaster damage and loss assessments, relief deployment registries.
   - Portal: `https://ndma.gov.in/`

---

## 5. Pre-Training Data Quality Assurance

Before training, every CSV file must pass the `TabularDataValidator` suite in `ml/common/validation.py`, which enforces:
- Zero out-of-bounds coordinates (must fall within sovereign Indian bounds).
- Zero negative rainfall or soil moisture outside $0–100\%$.
- Chronological consistency for temporal splits without future-data leakage.
- Absence of duplicate spatio-temporal observations.
