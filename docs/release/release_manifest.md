# RISK // INDIA — Cryptographic Release Manifest
**Authoritative Workspace:** `C:\Users\HP\Desktop\Risk Analyser`  
**Release Tag:** `RELEASE_2026_POST_PHASE2C_FROZEN`  
**Verification Date:** 2026-09-21  
**Audit Standard:** Strict Post-Phase-2C Freeze Compliance  

---

## 1. Cryptographic Scientific Invariants

| Artifact | Expected SHA-256 Digest | Actual Verified Digest | Status |
|---|---|---|:---:|
| **ML Model Artifact**<br>`ml/flood/artifacts/model.joblib` | `0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf` | `0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf` | **EXACT MATCH** |
| **Flood Feature Dataset**<br>`datasets/processed/flood_assam/flood_features.csv` | `88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080` | `88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080` | **EXACT MATCH** |

---

## 2. Frozen Repository Snapshot

| Parameter | Recorded Value | Notes |
|---|---|---|
| **Git Branch** | `main` | Production branch |
| **Git Commit** | `b10175a6abab8f82a3035fc99440ef4352a34efc` | Frozen commit reference |
| **Tracked Files** | 266 files | Core repository tracking |
| **Working Tree Status** | Frozen post-Phase-2C baseline | Clean state preserved under strict freeze |
| **Python Runtime** | Python 3.14.7 | Verified operational runtime |
| **Node.js Runtime** | Node v24.21.0 | Verified operational runtime |
| **npm Runtime** | npm 11.19.0 | Package manager runtime |
| **Frontend Package** | `risk-india` v1.0.0 | Vite + React + TypeScript |
| **Backend Package** | `risk-india-api` | FastAPI + Uvicorn + Pydantic v2 |

---

## 3. Operational Execution Commands

| Operation | Canonical Command Line |
|---|---|
| **Run Regression Tests** | `powershell -Command "$env:PYTHONPATH = 'backend;.'; python -m unittest discover tests"` |
| **Run Frontend Build** | `npm run build` (executes `tsc && vite build`) |
| **Start Backend API** | `powershell -Command "$env:PYTHONPATH = 'backend;.'; python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"` |
| **Start Frontend Client** | `npm run dev` (Runs on `http://localhost:5173`) |
| **Preview Prod Build** | `npm run preview` |

---

## 4. Production Quality Gates Verification

- **Full Regression Test Suite**:
  - Total Tests: **609**
  - Passed: **609 (100%)**
  - Failed: **0**
  - Errors: **0**
  - Duration: **14.49s**
- **Production Frontend Build**:
  - TypeScript Errors: **0**
  - Vite Build Result: **SUCCESS**
  - Build Duration: **3.40s**
  - Modules Transformed: **2001**
  - Generated Assets:
    - `dist/index.html` (1.54 kB, gzip: 0.70 kB)
    - `dist/assets/index-DaL2ijZv.css` (77.44 kB, gzip: 12.54 kB)
    - `dist/assets/index-DvNHvJSg.js` (798.05 kB, gzip: 206.34 kB)

---

## 5. Non-Blocking Informational Observations

- **OBS-01**: Production JavaScript bundle is approximately 798 kB and triggers an informational Rollup minification warning. Functional execution is completely unimpaired.
- **OBS-02**: Raw IMD rainfall departure dataset contains legitimate negative percentage values (e.g., `-87%`, `-95%`). These are physical rainfall departures, NOT confidence probabilities.
- **OBS-03**: Some rural catchments lack physical CWC/IMD sensor coverage and therefore correctly display `DATA_UNAVAILABLE` instead of interpolated/synthetic information.
