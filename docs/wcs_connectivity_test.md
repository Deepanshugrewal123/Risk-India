# Bhuvan WCS Endpoint Connectivity & Metadata Test Report

**Project**: RISK // INDIA — AI-Powered Disaster Risk Analysis Platform  
**Phase**: Phase 7E-A — WCS Endpoint Connectivity & Metadata Verification  
**Test Timestamp**: `2026-09-12 23:31:25 IST`  
**Endpoint**: `https://bhuvan-gp1.nrsc.gov.in/bhuvan/wcs`  
**Method Used**: System HTTP Client (`curl.exe`) with Standard HTTPS Certificate Verification  
**Timeout Configuration**:
- Connect timeout: `10 seconds`
- Maximum total attempt duration: `40 seconds`
- Total elapsed time: `0.985 seconds`

---

## 1. Test Results Summary

| Parameter | Configuration / Observed Value | Evaluation |
| :--- | :--- | :--- |
| **Endpoint URL** | `https://bhuvan-gp1.nrsc.gov.in/bhuvan/wcs` | Accessible |
| **Target Coverage Tested** | `flood:as_2023_23_06_18` *(and checked alias `flood:as_2023_06_23_18`)* | Validated |
| **HTTP Status** | `200 OK` | **SUCCESS** |
| **Total Request Time** | `0.985 seconds` (sub-second response) | Normal Latency |
| **SSL Verification** | Standard CA Verification (`ssl.CERT_REQUIRED` / default Windows CA store) | **PASS** (Valid SSL Cert) |
| **Response Size** | `2,715 bytes` | Complete WCS XML |
| **Result Status** | **`SUCCESS`** | Unblocked |

---

## 2. Technical Findings & Coverage Naming Validation

1. **Service Availability**:
   The official Bhuvan WCS endpoint is active, healthy, and responds in under 1 second under standard HTTPS certificate validation when using system socket / curl HTTP clients.
2. **Coverage Key Naming Syntax**:
   - Querying `coverage=flood:as_2023_23_06_18` (official ISRO naming convention `YYYY_DD_MM_HH`) returned the full `<wcs:CoverageOffering>` descriptor with native GeoTIFF raster bounds `[90.5612°E, 24.1326°N]` to `[93.7145°E, 26.9999°N]` and native pixel grid resolution `8.98315e-5` degrees (~10m).
   - Querying alias `flood:as_2023_06_23_18` confirmed that ISRO strictly enforces day-first ordering (`DD_MM`), returning `ServiceException: Could not find coverage 'flood:as_2023_06_23_18'`.

---

## 3. Final Quality Gate

```
WCS_METADATA_TEST = SUCCESS
```
