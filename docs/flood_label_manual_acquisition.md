# Manual Acquisition Protocol & Checklist: ISRO / NRSC Flood Products

**Project**: RISK // INDIA  
**Sub-Region**: Assam River Basin System (Brahmaputra & Barak corridors)  
**Document**: Standard Operating Procedure & Executable Acquisition Checklist  

---

## 1. Directory Structure

Place all acquired data in the designated subfolders:

```
datasets/raw/isro/
├── flood_inundation/          # Event-specific satellite inundation layers (GeoJSON / Shapefiles)
├── flood_hazard/              # Multi-year flood hazard frequency zones
└── metadata/                  # Mission activation bulletins, sensor logs, calibration profiles
```

---

## 2. Executable Manual Acquisition Checklist

Use this checklist when retrieving real flood data from official portals:

- [ ] **Step 1: Access the Bhuvan Disaster Services Portal**  
  URL: `https://bhuvan-app1.nrsc.gov.in/disaster/usrtasks/flood/flood.php`  
  Alternative Hazard Portal: `https://bhuvan-app1.nrsc.gov.in/disaster/usrtasks/flood_hz/flood_hz.php`
- [ ] **Step 2: Select Pilot Target State & Historical Disaster Years**  
  - State: **Assam**  
  - Priority Historical Events:
    - **June–July 2022 Brahmaputra Mega-Flood** (peak inundation across 32 districts)
    - **June–July 2024 Assam Monsoon Flood**
- [ ] **Step 3: Export in Preferred Machine-Readable Vector Format**  
  - **Preferred Format**: **GeoJSON (`.geojson`)** in WGS 84 (EPSG:4326).  
  - Alternative Format: ESRI Shapefile (`.shp`, `.shx`, `.dbf`, `.prj` kept together).
- [ ] **Step 4: Verify Coordinate Reference System (CRS)**  
  Coordinates must be decimal degrees longitude/latitude:  
  - Longitude: `89.5°E to 96.5°E`  
  - Latitude: `24.0°N to 28.5°N`  
  *(Projected UTM meters without projection files are rejected by the pipeline).*
- [ ] **Step 5: Deposit Files with Standard Naming Convention**  
  - Event Inundation: `datasets/raw/isro/flood_inundation/assam_flood_inundation_YYYYMMDD.geojson`  
  - Hazard Zonation: `datasets/raw/isro/flood_hazard/assam_flood_hazard_zones_1998_2023.geojson`  
  - Calibration Bulletin: `datasets/raw/isro/metadata/bhuvan_activation_report_YYYYMMDD.pdf`
- [ ] **Step 6: Run Automated Validation & Readiness Gate**  
  Execute in terminal:
  ```bash
  python ml/data/labels/check_label_readiness.py
  ```
  And verify full pipeline ingestion:
  ```bash
  python ml/data/labels/run_label_pipeline.py
  ```

---

## 3. What to Do if Only a Visual Map Is Available

If the portal offers only a visual map image (`.jpg`, `.png`) or PDF bulletin:

1. **Do NOT feed images directly into the ML pipeline** (they are flagged as `MANUAL GIS EXTRACTION REQUIRED`).
2. **QGIS Vectorization Procedure**:
   - Open **QGIS** (v3.22+).
   - Use `Raster` -> `Georeferencer` to load the map image.
   - Set coordinate system to **EPSG:4326 (WGS 84)**.
   - Reference control points against base OpenStreetMap (river confluences, district boundaries).
   - Trace or polygonize the blue inundation extent.
   - Add attributes: `event_id`, `observation_date` (YYYY-MM-DD), `district_name`, `inundated_area_sqkm`, `confidence: MANUAL_GIS_DIGITIZED`.
   - Export as `GeoJSON` into `datasets/raw/isro/flood_inundation/`.

---

## 4. Dataset Versioning Policy

- Raw downloaded files remain **strictly immutable**.
- When new vector layers are added, the ingestion engine increments the version metadata record (e.g. `assam_flood_labels_v0.1` -> `assam_flood_labels_v1.0`).
- Processed outputs are saved to `datasets/processed/` with explicit version stamps.
