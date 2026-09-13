# RISK // INDIA — Raw Data Ingestion & Manual Download Protocols

This document outlines the exact access instructions, source URLs, and destinations for official Indian flood data.

---

## Data Acquisition Status Summary

| Dataset Identifier | Source Agency | Status | Local Directory |
| :--- | :--- | :--- | :--- |
| `cwc_rainfall_assam_hourly` | Central Water Commission (CWC) / NWDP | DOWNLOADED (In Progress) | `datasets/raw/cwc/rainfall/` |
| `cwc_river_level_assam_hourly` | Central Water Commission (CWC) / NWDP | DOWNLOADED (In Progress) | `datasets/raw/cwc/river_level/` |
| `imd_rainfall_districtwise_daily` | India Meteorological Department (IMD) / NWDP | DOWNLOADED (In Progress) | `datasets/raw/imd/` |
| `isro_bhuvan_flood_inundation` | ISRO / NRSC / Bhuvan Disaster Services | **AWAITING MANUAL DOWNLOAD** | `datasets/raw/isro/flood_inundation/` |
| `isro_bhuvan_flood_hazard` | ISRO / NRSC / Bhuvan Disaster Services | **AWAITING MANUAL DOWNLOAD** | `datasets/raw/isro/flood_hazard/` |

---

## 1. ISRO / NRSC Bhuvan Flood Inundation Layers

- **DATASET**: Historical Flood Inundation Layers (Assam)
- **SOURCE**: National Remote Sensing Centre (NRSC) / Indian Space Research Organisation (ISRO)
- **STATUS**: **AWAITING MANUAL DOWNLOAD**
- **REQUIRED FILE**: Flood Inundation Extent Vector / Raster (GeoJSON, ESRI Shapefile, or GeoTIFF) for major Assam flood events (e.g. 2022, 2023, 2024 monsoon seasons).
- **DOWNLOAD PAGE**: `https://bhuvan-app1.nrsc.gov.in/disaster/usrtasks/flood/flood.php?uname=empty`
- **MANUAL ACTION REQUIRED**:
  1. Open the Bhuvan Disaster Management Support Programme (DMSP) portal at the link above.
  2. In the Left Navigation Tree, navigate to **State-wise Flood Layers** -> **Assam**.
  3. Select the target flood event year (e.g. `2022`, `2023`, `2024`).
  4. Select the specific satellite observation date (e.g. peak monsoon flood wave).
  5. In the map toolbar, click **Download Layer / Export GIS** or download the official inundation bulletin GeoJSON/Shapefile.
  6. Place the extracted archive into the destination folder below.
- **EXPECTED FILE FORMAT**: `.geojson`, `.shp` (with `.dbf`, `.shx`, `.prj`), or `.tif`
- **DESTINATION FOLDER**: `datasets/raw/isro/flood_inundation/`

---

## 2. ISRO / NRSC Flood Hazard Zonation Layers

- **DATASET**: Flood Hazard Zonation Atlas (Assam)
- **SOURCE**: National Remote Sensing Centre (NRSC) / Indian Space Research Organisation (ISRO)
- **STATUS**: **AWAITING MANUAL DOWNLOAD**
- **REQUIRED FILE**: Flood Hazard Zonation Layer (categorized into Very High, High, Moderate, Low flood frequency zones).
- **DOWNLOAD PAGE**: `https://bhuvan-app1.nrsc.gov.in/disaster/usrtasks/flood_hz/flood_hz.php?uname=empty`
- **MANUAL ACTION REQUIRED**:
  1. Open the Bhuvan Flood Hazard application at the link above.
  2. In the layer control, select **Assam State**.
  3. Under Hazard Maps, locate the district or state composite hazard layer.
  4. If user login is prompted, authenticate with ISRO Bhuvan credentials.
  5. Export the GIS vector layer or georeferenced GeoTIFF layer.
  6. Place the uncompressed files into the destination folder below.
- **EXPECTED FILE FORMAT**: `.geojson`, `.shp`, or `.tif`
- **DESTINATION FOLDER**: `datasets/raw/isro/flood_hazard/`

---

## 3. CWC Telemetry Hourly Rainfall (Assam)

- **DATASET**: CWC Telemetry Hourly Rainfall (Assam, 2021–2025)
- **SOURCE**: Central Water Commission (CWC), Ministry of Jal Shakti
- **STATUS**: **DOWNLOADED** via NWDP Open Data
- **SOURCE URL**: `https://www.nwdp.nwic.gov.in/en/dataset/rainfall-cwc-telemetry-hourly`
- **DIRECT RESOURCE**: `https://nwdp.nwic.gov.in/dataset/792f0818-bedf-42ab-a119-dc7002ceb312/resource/1f77001d-77b2-4d2d-a5af-b20168b9d517/download/rainfall_tel_hr_cwc_as_2021_2025.csv`
- **FORMAT**: CSV
- **DESTINATION FOLDER**: `datasets/raw/cwc/rainfall/rainfall_tel_hr_cwc_as_2021_2025.csv`

---

## 4. CWC Telemetry Hourly River Water Level (Assam)

- **DATASET**: CWC River Water Level Telemetry Hourly (Assam, 2021–2025)
- **SOURCE**: Central Water Commission (CWC), Ministry of Jal Shakti
- **STATUS**: **DOWNLOADED** via NWDP Open Data
- **SOURCE URL**: `https://nwdp.nwic.gov.in/dataset/river-water-level-telemetry-hourly-assam-department`
- **DIRECT RESOURCE**: `https://nwdp.nwic.gov.in/dataset/6273c426-32f9-4fdf-b67f-e4e7a46d8554/resource/51640870-5961-4696-b986-b744231f1c9f/download/rwl_tel_hr_assam_999_2021_2025.csv`
- **FORMAT**: CSV
- **DESTINATION FOLDER**: `datasets/raw/cwc/river_level/rwl_tel_hr_assam_999_2021_2025.csv`

---

## 5. IMD District-wise Daily Rainfall

- **DATASET**: IMD District-wise Daily Observed Rainfall
- **SOURCE**: India Meteorological Department (IMD) / NWDP
- **STATUS**: **DOWNLOADED** via NWDP Open Data
- **SOURCE URL**: `https://www.nwdp.nwic.gov.in/en/dataset/rainfall-daily-imd`
- **DIRECT RESOURCE**: `https://nwdp.nwic.gov.in/dataset/9380580f-9bf0-4708-9773-0cea3cbc595a/resource/8752174f-1d17-4aaf-8058-2eb396f50157/download/rainfall_districtwise_daily_imd.csv`
- **FORMAT**: CSV
- **DESTINATION FOLDER**: `datasets/raw/imd/rainfall_districtwise_daily_imd.csv`
