# RISK // INDIA — Scientific Integrity & Safeguards Forensic Audit
## Absolute Invariants, Model Boundaries & Non-Prediction Guards

**Document:** `scientific_integrity_audit.md`  
**Classification:** Forensic System Re-Analysis  
**Authoritative Workspace:** `C:\Users\HP\Desktop\Risk Analyser`  

---

### 1. Inviolate File Hashes Audit

Forensic SHA-256 validation was conducted directly against the filesystem artifacts:

| Artifact Path | Expected Canonical SHA-256 | Actual Checksum | Status |
| :--- | :--- | :--- | :---: |
| `ml/flood/artifacts/model.joblib` | `0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf` | `0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf` | **PASS (Exact)** |
| `datasets/processed/flood_assam/flood_features.csv` | `88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080` | `88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080` | **PASS (Exact)** |

Neither file has been modified, re-trained, corrupted, or replaced.

---

### 2. Machine Learning Scope Audit

1. **Assam Brahmaputra Corridor**:
   - `assam_flood_prototype_v1` is operational.
   - Evaluates river stage and upstream rainfall features derived from historical CWC gauges.
   - `ml_available = True` is reported strictly for `region_id == 'assam'` and `hazard == 'FLOOD'`.
2. **Non-Assam Jurisdictions (35 Entities)**:
   - For all 27 other States and 8 Union Territories, the system enforces:
     - `ml_available = False`
     - `status = "NOT_AVAILABLE"`
     - `model_name = None`
   - Unified risk is derived via transparent evidence fusion of live IMD forecasts, CWC gauge ratios, and BIS regional baselines.
   - Zero synthetic machine learning claims exist anywhere in the codebase.

---

### 3. Earthquake Non-Prediction Scientific Guard

1. **Geophysical Boundary**:
   - Under current modern geophysics, deterministic prediction of the exact time, epicenter, and magnitude of an earthquake is scientifically impossible.
   - Any software claiming to forecast "an earthquake in 2 days" is engaging in scientific fraud and causing public panic.
2. **Implementation Safeguards**:
   - In `hazard_forecast_engine.py`, `trend_engine.py`, and `predictive_service.py`:
     - For `hazard == "EARTHQUAKE"`, the future trajectory is permanently locked to `TrendState.STABLE`.
     - Future timeline points across all horizons (`NOW`, `0-6h`, `6-24h`, `1-3d`, `3-7d`) equal the ambient regional baseline score.
     - Confidence is permanently set to `ConfidenceLevel.LOW`.
     - Uncertainty is permanently set to `UncertaintyLevel.VERY_HIGH`.
     - `is_predictable = False` is hardcoded.
   - UI presentations clearly state:
     > *"Earthquakes cannot currently be predicted deterministically. Projections represent ambient lithospheric baselines (BIS IS 1893:2016) and observed USGS/NCS seismic catalog records."*

---

### 4. Zero Synthetic Data Guarantee

1. **Audit Standard**: `synthetic_records = 0` strictly enforced across all database tables, Pydantic schemas, and API responses.
2. **Forensic Findings**:
   - Backend APIs strictly return `synthetic_records: 0`.
   - Dynamic telemetry gates reject simulated records.
   - **UI Discrepancy Flagged**: Legacy `AnalyzeAreaSection.tsx` had an initial state containing `isDemoData: true` and `isSimulated: true`. While this was an initial frontend fallback for UI prototyping, it conflicted with the zero-synthetic data policy.
   - **Resolution**: `AnalyzeAreaSection.tsx` is completely refactored to consume live `predictiveRiskService` data with `synthetic_records: 0`.

---

### 5. Qualitative Confidence & Uncertainty Engine

1. **Elimination of Pseudo-Probabilities**:
   - The platform strictly prohibits displaying fabricated percentages like "87% chance of disaster".
   - Confidence is evaluated as qualitative:
     - **`HIGH`**: Corroborated by statutory official warnings + live telemetry + NWP forecasts + zero source disagreement.
     - **`MODERATE`**: Multi-signal agreement with minor sensor latency or moderate lead time.
     - **`LOW`**: Limited sensor density, active source disagreement, or non-predictable hazard.
2. **Monotonic Uncertainty Expansion**:
   - Uncertainty must expand with lead time:
     $$\text{Uncertainty}_{\text{NOW}} \le \text{Uncertainty}_{6\text{h}-24\text{h}} \le \text{Uncertainty}_{1\text{d}-3\text{d}} \le \text{Uncertainty}_{3\text{d}-7\text{d}}$$
   - If sensor telemetry is stale (`STALE` freshness) or sources disagree, uncertainty immediately escalates.
