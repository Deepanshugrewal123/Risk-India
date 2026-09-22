# RISK // INDIA — Operator Handover & Production Operations Runbook
**Document Version:** 1.0 (Post-Phase-2C Frozen Baseline)  
**Authoritative Workspace:** `C:\Users\HP\Desktop\Risk Analyser`  
**Target Audience:** Disaster Management Operations Personnel, Platform Engineers, Statutory Civil Defense Analysts  
**System Classification:** National Disaster Risk Intelligence & Early Warning Decision Support Prototype  

---

## 1. What RISK // INDIA Does

**RISK // INDIA** is a nationwide, multi-hazard disaster intelligence platform designed to translate authoritative hydro-meteorological observations and numerical predictions into glanceable, plain-language, actionable guidance for ordinary Indian citizens and administrative emergency coordinators.

The system continuously fuses real-time and forecast evidence to answer the **12 Foundational Citizen Safety Questions**:
1. What is happening now?
2. What could happen next?
3. What is the future risk trend?
4. How serious could it become?
5. Why might risk increase?
6. What official evidence supports the assessment?
7. What should I do now?
8. What should I prepare before the disaster?
9. What should I do during the event?
10. What should I do after the event?
11. What data is missing or uncertain?
12. When should I check again?

---

## 2. What Data Sources It Uses

The platform ingests only verified statutory and physical observational data streams:
- **India Meteorological Department (IMD)**: Automated Weather Station (AWS/ARG) observations, regional Doppler weather radar, gridded precipitation analyses, numerical weather prediction (NWP) model outputs, cyclone tracking bulletins, and official color-coded alert bulletins (Red, Orange, Yellow, Green).
- **Central Water Commission (CWC)**: Basin-level river telemetry, stream-gauge water level elevations, danger level (DL) / warning level (WL) thresholds, and river basin crest trends.
- **National Disaster Management Authority (NDMA) & State Disaster Management Authorities (SDMAs)**: Statutory emergency advisories, relief protocol guidelines, and civil defense alerts.
- **United States Geological Survey (USGS) & National Centre for Seismology (NCS)**: Real-time seismic catalog for contextual seismic history (strictly non-predictive).
- **Geological Survey of India (GSI)**: Baseline landslide susceptibility zonation and regional rainfall threshold curves.
- **National Remote Sensing Centre (NRSC) / ISRO Bhuvan**: Satellite inundation extent rasters used for spatial validation of historical flood events.

---

## 3. What the System Can Predict / Project

The system generates analytical projections across **5 Standard Forecast Horizons**:
- **`NOW` (Immediate)**: Real-time ground station state derived from current telemetry and radar feeds.
- **`0–6 Hours` (Nowcasting)**: Convective storm track progression, immediate flash-flood susceptibility, and rapid wind gust intensification.
- **`6–24 Hours` (Short-Range)**: River-stage rises based on upstream precipitation, diurnal maximum/minimum temperature anomalies, and cyclone outer-band rain loading.
- **`1–3 Days` (Medium-Range)**: Atmospheric depression trajectories, synoptic rainfall totals, heatwave persistence, and multi-basin flood crest propagation.
- **`3–7 Days` (Extended Outlook)**: Broad synoptic convective trends, monsoon trough positioning, and low-pressure area formation indicators.

*Scientific Constraint*: Projections represent analytical trend consensus, NOT guaranteed deterministic outcomes.

---

## 4. What the System Cannot Predict

Operators must understand the physical and scientific boundaries of the system:
- **Cannot Predict Exact Cloudburst Footprints**: Micro-scale convective cells below numerical model grid resolution (<4 km) cannot be pinpointed to individual street lanes.
- **Cannot Guarantee Hyper-Local Urban Drainage Failure**: Localized urban street flooding depends on storm-drain clogs, silt accumulation, and municipal pump operations, which are outside regional telemetry scope.
- **Cannot Predict Landslide Timing Down to the Minute**: Slope failure models project susceptibility windows based on cumulative antecedent moisture; they do not predict exact slope detachment seconds.
- **Cannot Predict Lightning Strike Coordinate**: Severe thunderstorm alerts indicate convective lightning risk across a sub-division; individual lightning bolt strikes are non-deterministic.

---

## 5. Assam Flood ML Model Scope

The platform contains an approved statistical machine learning model:
- **Model Identifier**: `assam_flood_prototype_v1` (Random Forest Classifier).
- **Artifact Path**: `ml/flood/artifacts/model.joblib` (SHA-256: `0e05bcdf...`).
- **Feature Dataset**: `datasets/processed/flood_assam/flood_features.csv` (SHA-256: `88b32f35...`).
- **Operational Boundary**: Scoped exclusively to the Brahmaputra River valley within the State of Assam.
- **Strict Boundary Enforcement**: For all other 35 States and Union Territories, `ml_available = False` is hard-enforced. The system rejects synthetic model inference outside calibrated empirical boundaries.

---

## 6. Earthquake Limitation (Non-Prediction Guard)

- **Absolute Physical Invariant**: Current seismological science cannot predict the exact time, location, or magnitude of an impending tectonic earthquake.
- **Enforcement**:
  - Temporal forecasting is completely disabled for seismic hazards across all 5 horizons.
  - The UI prominently renders the mandatory **Scientific Mandate // Earthquake Non-Prediction Notice**.
  - Seismic information is strictly confined to ambient tectonic zoning under BIS standard IS 1893:2016 (Zones II, III, IV, V) and recent historical event catalogs.
  - Action guidance emphasizes structural retrofitting, drop-cover-hold drill procedures, and household emergency supply readiness.

---

## 7. How to Start the Backend API

From the repository root on a Windows host:

```powershell
# Set Python path to include backend module
$env:PYTHONPATH = "backend;."

# Start FastAPI Uvicorn ASGI server on port 8000
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Verify backend health:
```powershell
curl http://127.0.0.1:8000/api/health
# Expected: {"status":"healthy", "timestamp":"...", "version":"1.0.0"}
```

---

## 8. How to Start the Frontend Client

From the repository root in a separate terminal:

```powershell
# Start Vite development server
npm run dev
```

The application client will be accessible at `http://localhost:5173`.

---

## 9. How to Run the Automated Test Suite

From the repository root:

```powershell
$env:PYTHONPATH = "backend;."
python -m unittest discover tests
```

- **Pass Condition**: `Ran 609 tests in ~15s ... OK`.
- **Fail Condition**: Any failure, error, or regression requires immediate operator halt.

---

## 10. How to Run the Production Frontend Build

From the repository root:

```powershell
npm run build
```

- **Pass Condition**: TypeScript type-check succeeds with 0 errors, and Vite builds static assets into `dist/` (`dist/index.html`, `dist/assets/index-*.css`, `dist/assets/index-*.js`).

---

## 11. How to Verify Scientific Cryptographic Hashes

To verify that model artifacts and empirical datasets remain byte-for-byte unmodified:

```powershell
Get-FileHash ml/flood/artifacts/model.joblib -Algorithm SHA256
# MUST EQUAL: 0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf

Get-FileHash datasets/processed/flood_assam/flood_features.csv -Algorithm SHA256
# MUST EQUAL: 88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080
```

---

## 12. How to Interpret Future Risk

- **Current Risk State**: Reflects actual ground telemetry and immediate hazard intensity right now (`NORMAL`, `WATCH`, `ELEVATED`, `HIGH`, `CRITICAL`).
- **Future Risk State**: Projected risk level during the peak lead-time window based on incoming multi-model forecasts.
- **Trend State**: Directional momentum of the hazard:
  - `RISING`: Incoming signals indicate intensifying hazard conditions.
  - `STABLE`: Parameters remain consistent within current seasonal bounds.
  - `DECLINING`: Atmospheric fronts or flood crests are subsiding.
  - `VOLATILE`: Highly erratic or rapidly shifting convective conditions.

---

## 13. How to Interpret Early Warning

The Early Warning state provides progressive civil protection advisory tiers:
- `NO_ACTIVE_SIGNAL`: Baseline conditions.
- `WATCH`: Routine monitoring; conditions may become favorable for hazard development.
- `PREPARE`: Community preparedness; review household supplies.
- `GET_READY`: Heightened readiness; secure surroundings, charge communications.
- `EVACUATION_READINESS`: High hazard convergence; vulnerable citizens stand ready for orderly relocation.
- `EMERGENCY`: Imminent life-threatening threshold reached.

---

## 14. How to Interpret Data Gaps

When physical sensors are missing or offline:
- The system **never fabricates** synthetic readings or interpolates unverified numbers.
- It displays the **7-Point Data Gap Card**:
  1. *What is known*: Administrative baseline and climatological profile.
  2. *What is unknown*: Missing gauge or radar telemetry.
  3. *Last observation*: Timestamp of last valid reading or "None".
  4. *Source / provenance*: Operating agency network.
  5. *Freshness status*: `DATA UNAVAILABLE` or `LIMITED EVIDENCE`.
  6. *Forecast availability*: Regional Climatology Only.
  7. *Warning availability*: Confirmation of whether statutory red/orange bulletins are active.

---

## 15. How to Interpret Confidence

Confidence expresses the degree of convergence among available observational and model inputs:
- `HIGH`: Multiple independent sources (CWC gauges, IMD radar, NWP ensemble consensus) agree on hazard trajectory.
- `MODERATE`: Primary forecast models agree, but local gauge telemetry is sparse or slightly delayed.
- `LOW`: Single-source signal, conflicting model runs, or stale telemetry requiring precautionary verification.

*Numeric pseudo-probabilities (e.g. "87% chance") are strictly prohibited.*

---

## 16. How to Interpret Uncertainty

Uncertainty represents the physical spread of possible outcomes. In accordance with meteorological physics:
- **Monotonic Expansion Rule**: Uncertainty expands mathematically as lead time increases:
  - `NOW`: $\pm 0.08$ (Low)
  - `0–6H`: $\pm 0.12$ (Low to Moderate)
  - `6–24H`: $\pm 0.18$ (Moderate)
  - `1–3D`: $\pm 0.25$ (High)
  - `3–7D`: $\pm 0.35$ (Very High)
- Citizens are explicitly informed that 7-day outlooks carry higher projection uncertainty than 6-hour nowcasts.

---

## 17. Difference Between Preparation Guidance and Evacuation Orders

Operators and citizens must clearly distinguish between technical advisory and legal order:
- **Preparation Guidance**: Technical safety guidance generated by RISK // INDIA under NDMA standard operating procedures.
- **Mandatory Evacuation Orders**: Legally issued **exclusively** by the District Magistrate, District Disaster Management Authority (DDMA), or State Disaster Management Authority (SDMA) under the **Disaster Management Act, 2005**.
- RISK // INDIA provides decision support to prepare citizens; it **never** claims statutory authority to issue mandatory evacuation orders.

---

## 18. Emergency Resource Behavior

- Emergency resource directory contacts (112, 1078, 1070, 1077) are verified statutory numbers.
- If physical location telemetry for nearby shelter facilities or relief distribution points is unverified, the system displays:
  > *"Verified nearby resource location is currently unavailable."*
- Zero synthetic or imaginary relief camp coordinates are ever rendered.

---

## 19. Known Non-Blocking Observations

- **OBS-01 (JS Bundle Size)**: `dist/assets/index-DvNHvJSg.js` (798 kB) generates a Rollup minification warning. This is normal for single-bundle SPAs including charting and map libraries and has no functional defect impact.
- **OBS-02 (IMD Percentage Values)**: Raw IMD rainfall departure datasets contain legitimate negative percentages (e.g. `-87%`, `-95%` departure from normal rainfall). These are official statistical departures, NOT confidence probabilities.
- **OBS-03 (Dynamic Sensor Cycles)**: In uninstrumented catchments, the UI correctly displays `DATA_UNAVAILABLE` rather than generating synthetic approximations.

---

## 20. Release Verification Procedure

Before releasing or deploying to a staging/production server, operators must execute:

1. **Hash Integrity**: Confirm SHA-256 for `model.joblib` and `flood_features.csv`.
2. **Regression Suite**: Run `python -m unittest discover tests` (must pass 609/609).
3. **Frontend Build**: Run `npm run build` (must complete with exit code 0).
4. **Backend Health Check**: Probe `/api/health` and `/api/predictive-risk/national`.
5. **UI Smoke Test**: Open `http://localhost:5173` and confirm:
   - National India-wide overview is loaded by default.
   - 6-question intelligence strip is visible above fold.
   - "Open Risk Map" navigation triggers properly.
   - Earthquakes display the Non-Prediction Notice.
   - Non-Assam states show `Approved ML: None (Assam Only)`.
