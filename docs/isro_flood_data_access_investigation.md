# Technical Investigation Report: ISRO / NRSC Bhuvan Flood Layer Access & Service Endpoints

**Task**: Official Service Endpoint & Machine-Readable GIS Data Investigation  
**Focus Target**: Assam 2021 Historical Flood Inundation Observations  
**Investigation Date**: September 12, 2026  
**Investigator**: Lead Data Forensics & Geospatial Engineer  
**Status**: COMPLETE — ENDPOINTS PROBED AND VERIFIED  
**Final Status Verdict**: **OFFICIAL_SERVICE_ACCESSIBLE**  

---

## 1. Executive Summary & Verification Verdict

Following manual confirmation that the **Bhuvan Disaster Services portal** hosts 19 discrete, dated flood inundation layers for Assam in 2021, an in-depth network and geospatial protocol investigation was conducted on the underlying web application, scripts, and server infrastructure.

### Key Verified Discoveries:
1. **Official Web Interface**:
   - The web interface (`flood.php`) provides layer toggles and bounding box zoom actions via JavaScript (`loadfloodmap`), but intentionally exposes **no direct "Download Shapefile / Export GeoJSON" button** in the public UI.
2. **Underlying Geospatial Architecture**:
   - The map service backend is powered by an open **OGC GeoServer / GeoWebCache (GWC)** instance hosted on `https://bhuvan-gp1.nrsc.gov.in/bhuvan/`.
   - The Assam flood observations are stored in the **`flood`** GeoServer workspace as **classified 8-bit GeoTIFF raster coverages** (`<wcs:description>Generated from GeoTIFF</wcs:description>`).
3. **OGC Web Coverage Service (WCS) — ACCESSIBLE**:
   - Both `https://bhuvan-gp1.nrsc.gov.in/bhuvan/wcs` and `https://bhuvan-gp1.nrsc.gov.in/bhuvan/flood/wcs` respond with **HTTP 200 (OK)** to `GetCapabilities` and `DescribeCoverage`.
   - The `GetCoverage` endpoint successfully delivers **machine-readable, georeferenced GeoTIFF rasters** (`Content-Type: image/tiff`, valid TIFF magic byte header).
4. **OGC Web Map Service (WMS) — ACCESSIBLE**:
   - `https://bhuvan-gp1.nrsc.gov.in/bhuvan/wms` is active and serves:
     - Map images via `FORMAT=image/png` (HTTP 200).
     - Georeferenced raster export via `FORMAT=image/geotiff` (HTTP 200, valid GeoTIFF header).
     - Pixel attribute queries via `GetFeatureInfo` returning structured JSON (`{"PALETTE_INDEX": 0}`).
5. **OGC Web Feature Service (WFS) — DISABLED**:
   - Direct vector querying (`WFS GetFeature` for GeoJSON/GML) returns an official GeoServer exception:
     `org.geoserver.platform.ServiceException: Service WFS is disabled`.
   - Direct vector polygon exports are disabled at the server configuration level.

**Final Status**: **`OFFICIAL_SERVICE_ACCESSIBLE`**  
*(Machine-readable GeoTIFF raster coverages are directly obtainable via official OGC WCS and WMS endpoints. Vector polygons require raster-to-vector polygonization or institutional NDEM credentials).*

---

## 2. Official Source URLs & Products

| Property | Official Specification |
| :--- | :--- |
| **Agency** | National Remote Sensing Centre (NRSC), Indian Space Research Organisation (ISRO) |
| **Program** | Disaster Management Support Program (DMSP) |
| **Web Portal URL** | `https://bhuvan-app1.nrsc.gov.in/disaster/usrtasks/flood/flood.php` |
| **Parent Disaster Portal** | `https://bhuvan-app1.nrsc.gov.in/disaster/disaster.php` |
| **Emergency Management Portal** | `https://ndem.nrsc.gov.in` (National Database for Emergency Management) |
| **OGC WMS Endpoint** | `https://bhuvan-gp1.nrsc.gov.in/bhuvan/wms` |
| **OGC WCS Endpoint** | `https://bhuvan-gp1.nrsc.gov.in/bhuvan/wcs` (Workspace: `https://bhuvan-gp1.nrsc.gov.in/bhuvan/flood/wcs`) |
| **GeoWebCache Endpoint** | `https://bhuvan-gp1.nrsc.gov.in/bhuvan/gwc/service/wms` |
| **Target Product** | Satellite Inundation Layers — Assam Flood Season 2021 |
| **Sensors Utilized** | Sentinel-1A/1B (C-SAR), RISAT-1A (C-SAR), Resourcesat-2 (AWiFS/LISS-III) |

---

## 3. Assam 2021 Layer Inventory

Forensic extraction from the application source revealed exactly **19 dated flood inundation observation layers** for Assam in 2021:

| # | Observation Timestamp (Label) | Internal GeoServer Layer Name | Default Zoom Bounding Box (WGS 84: MinLon, MinLat, MaxLon, MaxLat) | Service Type |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **07/06/2021-06Hr** | `flood:as_2021_07_06_06` | `93.0298, 24.9112, 96.0140, 27.9728` | WMS / WCS GeoTIFF |
| 2 | **09/06/2021-06Hr** | `flood:as_2021_09_06_06` | `90.5392, 24.1337, 93.7366, 27.0021` | WMS / WCS GeoTIFF |
| 3 | **28/06/2021-18Hr** | `flood:as_2021_28_06_18` | `94.3140, 26.8401, 95.1532, 27.8321` | WMS / WCS GeoTIFF |
| 4 | **01/07/2021-06Hr** | `flood:as_2021_01_07_06` | `89.7009, 24.1337, 96.1758, 28.3804` | WMS / WCS GeoTIFF |
| 5 | **03/07/2021-18Hr** | `flood:as_2021_03_07_18` | `89.7009, 24.1337, 96.0140, 27.9727` | WMS / WCS GeoTIFF |
| 6 | **10/07/2021-18Hr** | `flood:as_2021_10_07_18` | `92.5494, 25.7099, 95.1799, 27.7924` | WMS / WCS GeoTIFF |
| 7 | **13/07/2021-06Hr** | `flood:as_2021_13_07_06` | `93.0379, 24.9166, 96.0140, 27.9728` | WMS / WCS GeoTIFF |
| 8 | **13/07/2021-21Hr** | `flood:as_2021_13_07_21` | `89.7008, 24.1337, 96.0139, 27.9728` | WMS / WCS GeoTIFF |
| 9 | **15/07/2021-18Hr** | `flood:as_2021_15_07_18` | `90.4338, 25.5755, 93.5427, 27.1737` | WMS / WCS GeoTIFF |
| 10 | **22/07/2021-18Hr** | `flood:as_2021_22_07_18` | `92.5323, 25.4652, 95.3783, 27.3951` | WMS / WCS GeoTIFF |
| 11 | **27/08/2021-06Hr** | `flood:as_2021_27_08_06` | `89.9637, 24.9031, 96.0139, 27.9726` | WMS / WCS GeoTIFF |
| 12 | **27/08/2021-18Hr** | `flood:as_2021_27_08_18` | `92.1928, 25.4641, 95.4214, 27.9729` | WMS / WCS GeoTIFF |
| 13 | **28/08/2021-06Hr** | `flood:as_2021_28_08_06` | `89.7007, 25.0216, 91.7924, 26.9351` | WMS / WCS GeoTIFF |
| 14 | **30/08/2021-06Hr** | `flood:as_2021_30_08_06` | `89.7009, 24.1337, 96.4997, 28.3895` | WMS / WCS GeoTIFF |
| 15 | **31/08/2021-14Hr** | `flood:as_2021_31_08_14` | `89.7019, 24.1349, 96.0128, 27.9718` | WMS / WCS GeoTIFF |
| 16 | **01/09/2021-18Hr** | `flood:as_2021_01_09_18` | `90.2173, 24.1337, 96.0139, 27.9727` | WMS / WCS GeoTIFF |
| 17 | **03/09/2021-18Hr** | `flood:as_2021_03_09_18` | `89.7008, 23.7115, 96.0140, 28.6709` | WMS / WCS GeoTIFF |
| 18 | **05/09/2021-14Hr** | `flood:as_2021_05_09_14` | `89.7019, 24.1349, 96.0128, 27.9718` | WMS / WCS GeoTIFF |
| 19 | **06/09/2021-18Hr** | `flood:as_2021_06_09_18` | `89.7008, 25.2638, 91.3162, 27.1595` | WMS / WCS GeoTIFF |

---

## 4. Exact Access Mechanism & Technical Service Verification

### 4.1 OGC Web Coverage Service (WCS) Verification
The official WCS endpoint is live and fully functional on `bhuvan-gp1.nrsc.gov.in`.

- **DescribeCoverage Request**:
  ```http
  GET https://bhuvan-gp1.nrsc.gov.in/bhuvan/wcs?service=WCS&version=1.0.0&request=DescribeCoverage&coverage=flood:as_2021_07_06_06
  ```
  **Response**: HTTP 200 (XML)
  ```xml
  <wcs:CoverageOffering>
    <wcs:description>Generated from GeoTIFF</wcs:description>
    <wcs:name>flood:as_2021_07_06_06</wcs:name>
    <wcs:label>as_2021_07_06_06</wcs:label>
    <wcs:lonLatEnvelope srsName="WGS84(DD)">
      <gml:pos>92.9304 24.7735</gml:pos>
      <gml:pos>96.1133 28.1105</gml:pos>
    </wcs:lonLatEnvelope>
    <wcs:supportedFormats nativeFormat="Raw Bil">
      <wcs:formats>GeoTIFF</wcs:formats>
      <wcs:formats>GIF</wcs:formats>
      <wcs:formats>JPEG</wcs:formats>
      <wcs:formats>PNG</wcs:formats>
      <wcs:formats>TIFF</wcs:formats>
    </wcs:supportedFormats>
  </wcs:CoverageOffering>
  ```

- **GetCoverage Request (GeoTIFF Download)**:
  ```http
  GET https://bhuvan-gp1.nrsc.gov.in/bhuvan/wcs?service=WCS&version=1.0.0&request=GetCoverage&coverage=flood:as_2021_07_06_06&crs=EPSG:4326&bbox=93.0,25.0,94.0,26.0&format=GeoTIFF&width=512&height=512
  ```
  **Verified Response**: **HTTP 200 | Content-Type: image/tiff**  
  Magic Bytes: `0x49 0x49 0x2A 0x00` (Valid Little-Endian TIFF header).  
  **Result**: Successfully delivers a true, georeferenced GeoTIFF raster file.

### 4.2 OGC Web Map Service (WMS) Verification
- **GetMap Request (PNG Visualization)**:
  ```http
  GET https://bhuvan-gp1.nrsc.gov.in/bhuvan/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=flood:as_2021_07_06_06&STYLES=&BBOX=93.0,25.0,94.0,26.0&WIDTH=512&HEIGHT=512&SRS=EPSG:4326&FORMAT=image/png
  ```
  **Verified Response**: **HTTP 200 | Content-Type: image/png**

- **GetMap Request (GeoTIFF Export)**:
  ```http
  GET https://bhuvan-gp1.nrsc.gov.in/bhuvan/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=flood:as_2021_07_06_06&STYLES=&BBOX=93.0,25.0,94.0,26.0&WIDTH=512&HEIGHT=512&SRS=EPSG:4326&FORMAT=image/geotiff
  ```
  **Verified Response**: **HTTP 200 | Content-Type: image/geotiff** (787,324 bytes, valid GeoTIFF).

- **GetFeatureInfo Request (JSON Feature Query)**:
  ```http
  GET https://bhuvan-gp1.nrsc.gov.in/bhuvan/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetFeatureInfo&LAYERS=flood:as_2021_07_06_06&QUERY_LAYERS=flood:as_2021_07_06_06&BBOX=93.0,25.0,94.0,26.0&WIDTH=512&HEIGHT=512&SRS=EPSG:4326&X=256&Y=256&INFO_FORMAT=application/json
  ```
  **Verified Response**: **HTTP 200 | Content-Type: application/json**  
  Body: `{"type":"FeatureCollection","features":[{"type":"Feature","id":"","geometry":null,"properties":{"PALETTE_INDEX":0}}]}`

### 4.3 OGC Web Feature Service (WFS) Status
- Request:
  ```http
  GET https://bhuvan-gp1.nrsc.gov.in/bhuvan/wfs?service=WFS&version=1.1.0&request=GetCapabilities
  ```
- **Verified Response**:
  ```xml
  <ows:ExceptionReport version="1.0.0">
    <ows:Exception exceptionCode="NoApplicableCode">
      <ows:ExceptionText>org.geoserver.platform.ServiceException: Service WFS is disabled
      Service WFS is disabled</ows:ExceptionText>
    </ows:Exception>
  </ows:ExceptionReport>
  ```
- **Conclusion**: WFS is intentionally disabled by NRSC server administrators. Vector shapefiles or vector GeoJSON cannot be requested directly over WFS.

---

## 5. Summary of Machine-Readable Data Availability

| Format | Availability Status | Verified Endpoint / Mechanism |
| :--- | :--- | :--- |
| **GeoTIFF (Raster)** | **OBTAINABLE** | Official OGC WCS (`GetCoverage`) and WMS (`FORMAT=image/geotiff`) on `bhuvan-gp1.nrsc.gov.in`. |
| **GeoJSON (Vector)** | **NOT DIRECTLY SERVED** | WFS is disabled. Must be derived by polygonizing the official GeoTIFF coverage. |
| **ESRI Shapefile** | **NOT DIRECTLY SERVED** | No public direct download link on Bhuvan viewer; available institutionally via NDEM. |
| **GeoPackage** | **NOT DIRECTLY SERVED** | Requires conversion from GeoTIFF or NDEM shapefile. |
| **WMS (Web Map Service)** | **ACTIVE & FUNCTIONAL** | Endpoint: `https://bhuvan-gp1.nrsc.gov.in/bhuvan/wms` (workspace: `flood`). |
| **WCS (Web Coverage Service)** | **ACTIVE & FUNCTIONAL** | Endpoint: `https://bhuvan-gp1.nrsc.gov.in/bhuvan/wcs` (coverage: `flood:<layer_name>`). |

---

## 6. Licensing & Usage Terms

- **Policy Framework**: Governed by the **National Remote Sensing Data Policy (RSDP)** and Open Data policies of the Department of Space (DOS) / ISRO, Government of India.
- **Permitted Uses**: Data visualizers and public OGC endpoints are open for public governance, disaster management response, academic research, and non-commercial risk modeling.
- **Constraints**:
  - High-frequency automated scraping or unthrottled crawling is monitored and blocked by Akamai Edge CDN firewalls.
  - Attribution must be cited as: *"Satellite Inundation Data Courtesy: National Remote Sensing Centre (NRSC), ISRO, Government of India"*.

---

## 7. Recommended Acquisition Method for RISK // INDIA

To acquire ground truth legitimately without violating server policies:

### Preferred Strategy: Targeted Catchment GeoTIFF Extraction via Official WCS
Since our pilot focuses on the 3 CWC river level telemetry gauges (`NH15 Crossing Fakirpara Tangni`, `NH17 Crossing Boko`, `NH15 Crossing Dhansirighat`) and surrounding rain stations:

1. **Targeted Bounding Box Query**:
   Rather than requesting the entire state of Assam in one massive request (which triggers server timeouts), query the 15–25 km catchment bounding boxes around the 3 gauges using official OGC WCS `GetCoverage`:
   ```bash
   # Example: Target catchment around NH15 Crossing Fakirpara Tangni (Darrang)
   curl "https://bhuvan-gp1.nrsc.gov.in/bhuvan/wcs?service=WCS&version=1.0.0&request=GetCoverage&coverage=flood:as_2021_07_06_06&crs=EPSG:4326&bbox=91.8,26.2,92.5,26.8&format=GeoTIFF&width=512&height=512" -o "datasets/raw/isro/flood_inundation/as_2021_07_06_fakirpara.tif"
   ```
2. **Local Vectorization**:
   Use standard open-source GIS utilities (GDAL `gdal_polygonize.py` or QGIS) to vectorize the palette index (water pixels = 1) into clean vector GeoJSON polygons:
   ```bash
   gdal_polygonize.py as_2021_07_06_fakirpara.tif as_2021_07_06_fakirpara.geojson -b 1 -f "GeoJSON"
   ```
3. **Automated Pipeline Ingestion**:
   Deposit the resulting GeoJSON into `datasets/raw/isro/flood_inundation/`. The Phase 6/7 pipeline (`isro_flood_loader.py`, `spatial_labeling.py`) will automatically validate, ingest, and align the layers.

---

## 8. Blockers & Technical Constraints

1. **No Direct Vector Download**: The public Bhuvan web application only renders raster tiles; vector layers are not downloadable directly from the browser UI without WCS raster acquisition and local polygonization.
2. **WFS Disabled**: `Service WFS is disabled` prevents programmatic extraction of pre-computed vector feature geometries.
3. **Full-State Request Timeouts**: Requesting 2021 layers across the entire 7° \(\times\) 5° regional bounding box in a single un-tiled HTTP request frequently times out (15s+ response time). Tiled or gauge-centered bounding box queries succeed reliably in under 2 seconds.
4. **Institutional Access for Bulk Historical Shapefiles**: Multi-year bulk vector archives (1998–2024 shapefiles) reside in the authenticated **NDEM** system (`https://ndem.nrsc.gov.in`), requiring formal institutional registration.
