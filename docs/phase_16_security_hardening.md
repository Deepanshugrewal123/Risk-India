# RISK // INDIA — Phase 16: Production Security Hardening

## Overview & Scope
**RISK // INDIA** has been hardened with production-grade defense-in-depth security controls to ensure public resilience without altering the existing visual design, UI layouts, ML model (`assam_flood_prototype_v1`), datasets (32 observations), or existing API contracts.

This phase was executed under strict non-negotiable preservation rules:
- **Zero UI / Styling Modifications**: Colors, typography, and motion aesthetics remain completely untouched.
- **Zero ML Changes**: The trained model weights, 13 empirical features, and Assam spatial boundaries remain intact.
- **Zero Synthetic Data Generation**: Datasets (`flood_features.csv`) and USGS seismic records are real verified records.
- **Zero Regressions**: 100% pass rate maintained across all existing 73 tests, expanding the test suite to 90 automated tests.
- **No Deployment / Git Push**: Security hardening is implemented locally for production readiness without live deployment or code pushes.

---

## Implemented Security Controls

### 1. CORS Hardening & Credentials Protection
- **Vulnerability Remediated**: Wildcard `*` in CORS origins when `allow_credentials=True` violates RFC specifications and allows malicious third-party origins to read credentialed responses.
- **Implementation**:
  - `backend/app/config.py`: Explicitly whitelist exact frontend origins (`http://localhost:5173`, `http://127.0.0.1:5173`, etc.).
  - `cors_origin_list` dynamically strips any wildcard `*` to guarantee wildcard origins are never combined with `allow_credentials=True`.
  - Unlisted origins are strictly denied CORS authorization headers.

### 2. Comprehensive Defense-in-Depth Security Headers
- **Middleware**: `backend/app/middleware/security.py` (`SecurityHeadersMiddleware`)
- **Injected Headers**:
  - `X-Content-Type-Options: nosniff`: Prevents MIME-type sniffing attacks.
  - `X-Frame-Options: DENY`: Prevents UI redressing and clickjacking across external framing contexts.
  - `Referrer-Policy: strict-origin-when-cross-origin`: Restricts referrer information leakage to cross-origin destinations.
  - `Permissions-Policy: camera=(), microphone=(), geolocation=(self)`: Restricts browser device hardware access.
  - `Content-Security-Policy`: Custom policy tailored to RISK // INDIA's client dependencies:
    - Allows Vite/React scripts (`'self' 'unsafe-inline' 'unsafe-eval'`)
    - Google Fonts (`https://fonts.googleapis.com`, `https://fonts.gstatic.com`)
    - OpenStreetMap tiles (`https://*.tile.openstreetmap.org`, `https://tile.openstreetmap.org`)
    - Upstream seismic endpoints (`https://earthquake.usgs.gov`)
    - Frame ancestors strictly denied (`frame-ancestors 'none'`)
  - `Strict-Transport-Security` (HSTS): Conditionally applied (`max-age=31536000; includeSubDomains`) in production environments or HTTPS schemes, avoiding breakage in local HTTP development.

### 3. Sliding-Window Rate Limiting & Abuse Protection
- **Middleware**: `backend/app/middleware/rate_limit.py` (`RateLimitMiddleware`)
- **Architecture**:
  - In-memory sliding-window timestamp accounting with sub-second accuracy.
  - Memory bounding via LRU / TTL cleanup to prevent state memory exhaustion.
  - Client IP resolution securely inspects `X-Forwarded-For` with regex sanitization before falling back to client host.
- **Tiers**:
  - **Compute Tier**: 10 requests / 60 seconds for compute-intensive endpoints (`POST /api/risk/analyze`, `GET /api/disasters/refresh`).
  - **General Tier**: 60 requests / 60 seconds for standard API read operations.
- **Response**:
  - HTTP `429 Too Many Requests` with RFC-compliant `Retry-After: <seconds>` header and structured JSON payload.

### 4. Distributed Request Correlation & Safe Structured Logging
- **Middlewares**: `backend/app/middleware/logger.py` (`CorrelationIdMiddleware`, `StructuredLoggingMiddleware`)
- **Request Correlation**:
  - Validates client-supplied `X-Request-ID` against strict regex (`^[a-zA-Z0-9_-]{1,64}$`).
  - Malformed or injection IDs are discarded and replaced with cryptographically random UUIDv4.
  - Returned in all response headers (`X-Request-ID: <uuid>`) and attached to `request.state.request_id`.
- **Structured Safe Logging**:
  - Emits JSON records containing `timestamp`, `level`, `request_id`, `method`, `path`, `status_code`, and `latency_ms`.
  - **Zero Credential Leakage**: Explicitly suppresses Authorization headers, bearer tokens, passwords, cookies, and sensitive parameters from log streams.

### 5. Input Validation & Physical Domain Bounds
- **Schema**: `backend/app/schemas/risk.py` (`RiskAnalyzeRequest`)
- **Pydantic Field Validators**:
  - **Geographic Bounds**: Coordinates strictly validated against Indian bounding box: `6.0 <= latitude <= 38.0`, `68.0 <= longitude <= 98.0`.
  - **Rainfall Physical Bounds**: `rainfall_6h`, `rainfall_24h`, `rainfall_72h`, `rainfall_168h` validated between `0.0 mm` and `2000.0 mm`.
  - **River Level Bounds**: `river_level_relative` validated between `-10.0 m` and `15.0 m`.
  - Violations result in HTTP `422 Unprocessable Entity` with explicit validation details.

### 6. Information Leakage Prevention & Error Sanitization
- **Exception Handlers**: `backend/app/main.py` (`global_exception_handler`), `backend/app/middleware/logger.py`
- **Sanitization**:
  - Internal server errors (HTTP 500) scrub all Python tracebacks, database URLs, local file system paths (`C:\Users\...`), and internal exception types.
  - Client receives clean generic error message accompanied by correlation `request_id` for administrative auditing.

### 7. Frontend Hyperlink Hardening
- Audited all 10 external anchor tags (`target="_blank"`) across `CurrentDisastersSection.tsx`, `VerifiedHelpSection.tsx`, `HelpOthersPage.tsx`, `GetHelpPage.tsx`, and `Footer.tsx`.
- Guaranteed `rel="noopener noreferrer"` across all external links to defend against reverse tabnabbing and window object manipulation.

---

## Verification & Test Results

### 1. Automated Security Suite (`tests/test_phase16_security.py`)
17 unit and integration tests passing in 0.24s:
1. `test_security_headers_present`: PASS
2. `test_csp_header_present_and_valid`: PASS
3. `test_cors_rejection_for_unlisted_origin`: PASS
4. `test_cors_acceptance_for_allowed_origin`: PASS
5. `test_cors_no_wildcard_with_credentials`: PASS
6. `test_rate_limiting_compute_route`: PASS
7. `test_rate_limiting_retry_after_header`: PASS
8. `test_request_id_generated_when_absent`: PASS
9. `test_request_id_preserved_when_valid`: PASS
10. `test_request_id_sanitized_when_malformed`: PASS
11. `test_coordinate_validation_bounds`: PASS
12. `test_rainfall_validation_bounds`: PASS
13. `test_ssrf_protection_maintained`: PASS
14. `test_500_error_sanitization`: PASS
15. `test_logging_no_credential_leak`: PASS
16. `test_phase15_circuit_breaker_reliability_preserved`: PASS
17. `test_ml_prototype_integrity`: PASS

### 2. Complete Repository Test Suite
- Total tests: **90 tests**
- Result: **100% passing (0 failures, 0 errors)**
- Execution time: **10.6s**

### 3. Frontend Production Build
- Command: `npm run build`
- Modules transformed: 1,973
- Compilation time: 2.17s
- Build errors: 0
