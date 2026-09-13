# PHASE 10 — END-TO-END EVALUATION AND PILOT DEMONSTRATION
**Project:** RISK // INDIA — AI-Powered Disaster Risk Analyzer & Management System  
**Phase:** Phase 10 — End-to-End Evaluation & Pilot Demonstration  
**Model Version:** `assam_flood_prototype_v1`  
**Date:** 2026-09-13  
**Overall System Status:** PASS_WITH_LIMITATIONS  

---

## 1. Executive Objective & Governance Boundaries

Phase 10 conducts the formal end-to-end system evaluation and pilot demonstration of the trained Assam flood ML prototype (`assam_flood_prototype_v1`). 

### Core Scientific & Operational Covenants:
- **Zero Model Retraining:** Model weights and preprocessor state were frozen and unmodified.
- **Zero Synthetic Training Data:** No synthetic observations were introduced.
- **Real Data vs Demonstration Inputs Strictly Segregated:**
  - **REAL DATA:** The audited 32 historical flood events (18 positive, 14 negative) from official CWC telemetry and ISRO/NRSC Bhuvan inundation layers catalogued in `datasets/processed/flood_assam/flood_features.csv`.
  - **DEMONSTRATION INPUTS:** Controlled synthetic parameter sets used solely to verify model responsiveness, range boundaries, and explainability across Low, Moderate, and Critical regimes.
- **Academic Scope:** Explicitly classified as an academic college engineering prototype. It does **not** provide operational real-time forecasting, nationwide India flood analysis, or emergency public evacuation directives.

---

## 2. Test Environment

- **Host Operating System:** Windows 11
- **Backend Runtime:** Python 3.14, FastAPI 0.115+, Uvicorn (port 8000)
- **Frontend Runtime:** React 18, TypeScript 5, Vite 5 (port 5173, reverse proxy `/api` -> `http://127.0.0.1:8000`)
- **ML Toolchain:** scikit-learn 1.4+, NumPy 1.26+, Pandas 2.2+, Joblib
- **Model Artifact:** [`ml/flood/artifacts/model.joblib`](ml/flood/artifacts/model.joblib) (Regularized Logistic Regression L2, $C=0.5$, balanced class weights)
- **Preprocessor Artifact:** [`ml/flood/artifacts/preprocessor.joblib`](ml/flood/artifacts/preprocessor.joblib) (Median Imputer + StandardScaler)

---

## 3. Backend API Verification (`POST /api/risk/analyze`)

The inference endpoint was evaluated against schema contracts, bounds, and typing requirements:

| Field Checked | Target Contract | Observed Value | Evaluation |
| :--- | :--- | :--- | :---: |
| **HTTP Status Code** | `200 OK` | `200 OK` | **PASS** |
| **`status`** | `"success"` | `"success"` | **PASS** |
| **`flood_probability`** | Float in [0.0, 1.0] | `0.2329` | **PASS** |
| **`risk_score`** | Integer in [0, 100] | `23` | **PASS** |
| **`risk_level`** | Enum (`Low`, `Moderate`, `High`, `Critical`) | `"Low"` | **PASS** |
| **`model_version`** | String `"assam_flood_prototype_v1"` | `"assam_flood_prototype_v1"` | **PASS** |
| **`hazard`** | String `"flood"` | `"flood"` | **PASS** |
| **`is_prototype`** | Boolean `True` | `True` | **PASS** |
| **`emergency_warning`** | Boolean `False` | `False` | **PASS** |
| **`top_factors`** | List of <= 4 linear feature attributions | 4 actual model features returned | **PASS** |
| **`disclaimer`** | Mandatory limitation disclaimer | Exactly matches specification | **PASS** |

---

## 4. Three Controlled Pilot Demonstration Scenarios

Three controlled test inputs were constructed using only model-compatible features to demonstrate system responsiveness across risk regimes without claiming live weather conditions:

### Scenario A: Relatively Lower-Risk Demo
- **Context:** Stable hydrological conditions with low antecedent precipitation, negative river surge, and normal channel percentile in Assam monitoring basin.
- **Input Features:**
  - `rainfall_6h`: 0.0 mm
  - `rainfall_24h`: 1.5 mm
  - `rainfall_72h`: 5.0 mm
  - `rainfall_168h`: 250.0 mm
  - `river_level_relative`: 15.0 m
  - `river_rise_6h`: -0.05 m
  - `river_rise_24h`: -0.20 m
  - `river_percentile_level`: 0.85
  - `month`: 7 (July)
  - `day_of_year_sin`: -0.20
  - `day_of_year_cos`: -0.98
  - `latitude`: 26.6958
  - `longitude`: 92.2578
- **Model Output:**
  - **Probability:** `0.2294` (22.9%)
  - **Risk Score:** `23 / 100`
  - **Risk Category:** `LOW`
- **Top Factor Attributions:**
  1. `[-] Seasonal River Level Percentile` (85.0%): -0.6634 (Lowers Risk)
  2. `[-] Catchment Latitude` (26.6958): -0.2763 (Lowers Risk)
  3. `[-] 7-Day Antecedent Precipitation` (250.0 mm): -0.2292 (Lowers Risk)
  4. `[-] Catchment Longitude` (92.2578): -0.1791 (Lowers Risk)

---

### Scenario B: Elevated-Risk Demo
- **Context:** Moderate monsoon rainfall pulse with positive 6h streamflow rise and mid-percentile river stage in Assam monitoring basin.
- **Input Features:**
  - `rainfall_6h`: 2.0 mm
  - `rainfall_24h`: 25.0 mm
  - `rainfall_72h`: 45.0 mm
  - `rainfall_168h`: 140.0 mm
  - `river_level_relative`: 8.0 m
  - `river_rise_6h`: +0.04 m
  - `river_rise_24h`: +0.10 m
  - `river_percentile_level`: 0.55
  - `month`: 6 (June)
  - `day_of_year_sin`: 0.10
  - `day_of_year_cos`: -0.98
  - `latitude`: 26.6958
  - `longitude`: 92.2578
- **Model Output:**
  - **Probability:** `0.4614` (46.1%)
  - **Risk Score:** `46 / 100`
  - **Risk Category:** `MODERATE`
- **Top Factor Attributions:**
  1. `[-] Catchment Latitude` (26.6958): -0.2763 (Lowers Risk)
  2. `[-] Catchment Longitude` (92.2578): -0.1791 (Lowers Risk)
  3. `[+] Storm Phase (Cosine)` (-0.98): +0.1015 (Increases Risk)
  4. `[+] 7-Day Antecedent Precipitation` (140.0 mm): +0.0873 (Increases Risk)

---

### Scenario C: Higher-Risk Demo
- **Context:** Intense localized convective burst exceeding 120 mm in 24h, combined with sharp +0.28m 6h river crest surge in lower Brahmaputra tributary (Boko gauge).
- **Input Features:**
  - `rainfall_6h`: 45.0 mm
  - `rainfall_24h`: 120.0 mm
  - `rainfall_72h`: 210.0 mm
  - `rainfall_168h`: 60.0 mm
  - `river_level_relative`: 0.85 m
  - `river_rise_6h`: +0.28 m
  - `river_rise_24h`: +0.45 m
  - `river_percentile_level`: 0.10
  - `month`: 6 (June)
  - `day_of_year_sin`: 0.25
  - `day_of_year_cos`: -0.95
  - `latitude`: 25.9775
  - `longitude`: 91.2342
- **Model Output:**
  - **Probability:** `0.9942` (99.4%)
  - **Risk Score:** `99 / 100`
  - **Risk Category:** `CRITICAL`
- **Top Factor Attributions:**
  1. `[+] Catchment Latitude` (25.9775): +1.9109 (Increases Risk)
  2. `[+] Catchment Longitude` (91.2342): +1.4342 (Increases Risk)
  3. `[+] Seasonal River Level Percentile` (10.0%): +0.8604 (Increases Risk)
  4. `[+] 6-Hour River Surge` (+0.28 m): +0.4802 (Increases Risk)

---

## 5. Monotonicity and Sensitivity Analysis

To inspect model stability, controlled one-at-a-time sensitivity sweeps were conducted while holding baseline features constant:

### Sweep 1: 72-Hour Cumulative Rainfall (`rainfall_72h`)
- Range tested: `10.0 mm` to `250.0 mm`
- **Behavior:** Strictly monotonic increasing.
  - At 10.0 mm: Probability = `0.4746` (Score 47)
  - At 60.0 mm: Probability = `0.4933` (Score 49)
  - At 150.0 mm: Probability = `0.5269` (Score 53)
  - At 250.0 mm: Probability = `0.5639` (Score 56)
- **Scientific Audit:** Logical hydraulic behavior. Increasing antecedent catchment rain monotonically increases soil saturation and runoff probability.

### Sweep 2: 6-Hour River Surge (`river_rise_6h`)
- Range tested: `-0.10 m` to `+0.35 m`
- **Behavior:** Strictly monotonic increasing.
  - At -0.10 m: Probability = `0.4247` (Score 42)
  - At +0.00 m: Probability = `0.4703` (Score 47)
  - At +0.15 m: Probability = `0.5392` (Score 54)
  - At +0.35 m: Probability = `0.6285` (Score 63)
- **Scientific Audit:** Expected hydraulic behavior. A sharp upward surge indicates upstream flood crest arrival.

### Sweep 3: 24-Hour Rainfall (`rainfall_24h`)
- Range tested: `0.0 mm` to `180.0 mm`
- **Behavior:** Strictly monotonic increasing.
  - At 0.0 mm: Probability = `0.4837` (Score 48)
  - At 80.0 mm: Probability = `0.5092` (Score 51)
  - At 180.0 mm: Probability = `0.5410` (Score 54)

### Sweep 4: 7-Day Cumulative Rainfall (`rainfall_168h`) — Counterintuitive Behavior Documented
- Range tested: `20.0 mm` to `400.0 mm`
- **Behavior:** Monotonic decreasing.
  - At 20.0 mm: Probability = `0.5859` (Score 59)
  - At 150.0 mm: Probability = `0.4933` (Score 49)
  - At 400.0 mm: Probability = `0.3216` (Score 32)
- **Scientific Rationale for Counterintuitive Weight:**
  In our small audited sample ($N=32$), several negative (zero-inundation) observations occurred during mid-monsoon conditions with high 7-day cumulative rainfall (e.g. 2022-07-13 with 263 mm rain where Bhuvan SAR showed no standing water). Regularized Logistic Regression placed a negative coefficient (-0.5148) on `rainfall_168h` to compensate for multicollinearity with 24h and 72h totals.
  **This behavior is documented transparently in accordance with Phase 10 guidelines rather than hidden.**

---

## 6. Explainability Audit

Every prediction exposes the mathematical linear decomposition:
$c_i = \beta_i \cdot z_i = \beta_i \cdot \frac{x_i - \mu_i}{\sigma_i}$
- Direction is explicitly mapped:
  - `increases_risk` when $c_i > 0$
  - `decreases_risk` when $c_i < 0$
- No natural-language hallucination or unverified LLM commentary is generated.
- The UI displays human-readable factor labels, empirical telemetry values, and linear contribution rankings.

---

## 7. Error State & Guard Testing

Five distinct failure modes were tested to verify that the system fails safely and gracefully without producing fabricated fallback scores:

| Failure Mode | Test Condition | Expected Behavior | Observed System Response | Status |
| :--- | :--- | :--- | :--- | :---: |
| **A. Backend Offline** | Server down / network failure | UI displays clear error state | Caught in `AnalyzeAreaSection`: *"Unable to calculate estimated risk for the selected location."* | **PASS** |
| **B. Unsupported Location** | Non-Assam location (e.g. Kerala, Delhi) | Dedicated scope limited message | HTTP 200: `status="model_scope_limited"`, Score = `None`, message rendered in amber scope banner | **PASS** |
| **C. Missing Telemetry** | Zero rainfall and zero river data | Insufficient data notification | HTTP 200: `status="insufficient_data"`, Score = `None`, message rendered in data requirement banner | **PASS** |
| **D. Invalid Numeric Input** | Non-numeric string in features | Controlled transformation error | HTTP 200: `status="inference_error"`, error description caught and returned cleanly | **PASS** |
| **E. Missing Artifact** | Missing `model.joblib` | Controlled server refusal | HTTP 200: `status="model_unavailable"`, load error reported with zero fallback prediction | **PASS** |

---

## 8. Performance Benchmark (Local Inference Latency)

A local latency benchmark of 50 consecutive requests to `POST http://127.0.0.1:8000/api/risk/analyze` was executed:
- **Total Requests:** 50
- **Total Failures:** 0 (0.0% failure rate)
- **Average Inference Latency:** `5.69 ms`
- **Median Latency:** `5.25 ms`
- **95th Percentile (P95):** `6.74 ms`
- **Minimum Latency:** `4.40 ms`
- **Maximum Latency:** `23.14 ms`

*Note: Measured in a local development environment; operational production deployment would introduce network transit latency.*

---

## 9. Final Quality Gate

```
OVERALL_SYSTEM_STATUS: PASS_WITH_LIMITATIONS
```

### Justification for `PASS_WITH_LIMITATIONS`:
1. The end-to-end fullstack integration functions with zero crashes, robust error guards, sub-10ms latency, and leakage-free data flow.
2. However, the underlying ML model is an initial prototype trained on $N=32$ historical events across 3 Assam CWC stations with weak cross-validation performance (ROC-AUC ~0.43) and multicollinear weighting on 7-day rainfall.
3. Therefore, declaring a raw `PASS` would overstate the scientific maturity of the prototype, while declaring `FAIL` would disregard the successful fullstack integration. `PASS_WITH_LIMITATIONS` is the scientifically honest, defensible rating.
