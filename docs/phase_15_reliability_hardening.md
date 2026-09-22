# RISK // INDIA — Phase 15: Production Architecture Migration & Reliability Hardening

## Overview
Phase 15 implements production-grade operational resilience and reliability hardening across both frontend and backend systems, translating the findings from Phase 14 into robust, verifiable software architecture while maintaining 100% fidelity to the visual design, UI components, datasets, and the trained Assam flood ML prototype (`assam_flood_prototype_v1`).

---

## Key Deliverables

### 1. Frontend Error Resilience (`ErrorBoundary.tsx`)
- **Location**: `src/components/common/ErrorBoundary.tsx`
- **Integration**: Root-level protection in `src/main.tsx` wrapping `<App />`.
- **Functionality**:
  - Catches runtime rendering exceptions globally before they cause an empty blank screen.
  - Renders an editorial fallback card matching the warm paper palette (`#F7F7F4`), charcoal typography, and subtle border hierarchy.
  - Displays a safe, non-sensitive reference code (`ERR-XXXXXX`).
  - Hides technical stack traces in user-facing UI while logging sanitized diagnostics to the developer console.
  - Provides direct one-click actions: "Try Again", "Reload Page", and "Home".
  - Re-asserts direct dial access to National Emergency (`112`).
  - Full compliance with `prefers-reduced-motion`.

### 2. Offline & Network Resilience (`OfflineIndicator.tsx`)
- **Location**: `src/components/common/OfflineIndicator.tsx`
- **Integration**: Top-level mounting in `src/App.tsx`.
- **Functionality**:
  - Automatically detects browser `online` and `offline` lifecycle events.
  - When disconnected: renders a floating, non-intrusive status banner anchored at the top of the screen (`LIVE SYNC PAUSED`).
  - Guarantees that local risk maps and cached emergency resources remain accessible without network connectivity.
  - Never misleads users into believing live telemetry is fresh when offline.
  - When connection is restored: displays an emerald transition banner (`Connection restored. Disaster intelligence re-synced.`) before smoothly auto-dismissing after 3.5 seconds.
  - Fully responsive across viewports from 320px to 1440px without obstructing navbar navigation or bottom-right SOS quick-dial buttons.

### 3. Resilient API Client (`src/services/api.ts`)
- **Location**: `src/services/api.ts`
- **Functionality**:
  - Replaces raw `fetch` calls across `disasterService.ts`, `riskService.ts`, and `resourceService.ts`.
  - Enforces explicit request timeouts (default 8,000ms) with `AbortController`.
  - Normalizes network errors and aborts into structured `ApiError` objects with `isTimeout` and `isNetworkError` flags.
  - Strict retry discipline:
    - Safe idempotent `GET` requests retry once with 500ms exponential backoff.
    - Analytical `POST` requests (`/api/risk/analyze`) execute strictly **0 automatic retries** to prevent backend load amplification.
  - Pre-checks `navigator.onLine` to fail fast when offline and immediately invoke fallback catalog data.

### 4. Backend Upstream Provider Resilience (`CircuitBreaker`)
- **Location**: `backend/app/services/disaster_provider.py`
- **Circuit Breaker Parameters**:
  - `failure_threshold`: 5 consecutive failures before tripping `CLOSED` → `OPEN`.
  - `cooldown_seconds`: 60.0 seconds before probing `OPEN` → `HALF_OPEN`.
  - `recovery`: 1 successful probe transitions `HALF_OPEN` → `CLOSED`.
  - `fallback`: Returns cached records with accurate `STALE` freshness classification; halts external network hammering.
- **Robust HTTP Client (`httpx`)**:
  - Replaced synchronous `urllib.request.urlopen` in `USGSSeismicProvider` with `httpx.Client`.
  - Explicit timeouts: `connect=3.0s`, `read=10.0s`, `write=10.0s`.
  - Bounded retries: max 2 retries with exponential backoff (0.5s, 1.0s).
  - Preserved backward compatibility with unit test mocks.
  - Guaranteed immutable static provider URL endpoints.

---

## Verification & Test Results
- **Automated Test Suite**: `tests/test_phase15_reliability.py` added containing 18 unit and integration tests.
- **Backend Test Count**: 73 total tests executed (`python -m unittest discover tests`).
- **Backend Test Result**: **73 PASSED, 0 FAILED, 0 ERRORS (100% PASS)**.
- **Frontend Build**: `npm run build` completed in 2.21s with **0 errors**.
- **Regressions**: **0 regressions** across ML inference, live disaster feeds, help hub, and database contracts.
