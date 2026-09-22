# RISK // INDIA — Phase 17: Production Data Platform & Storage Expansion

## Executive Summary
**RISK // INDIA** has expanded its backend persistence and caching tiers from a local single-file SQLite setup toward a production-grade PostgreSQL 16 & PostGIS platform. The upgrade maintains full dual-backend capability: local development and automated CI workflows remain 100% operational with SQLite, while production environments can seamlessly bind to PostgreSQL 16 with robust connection pooling and Alembic migration governance.

All operations were executed under strict non-negotiable preservation rules:
- **Zero UI / Styling Modifications**: Colors, typography, and motion aesthetics remain completely untouched.
- **Zero ML Modifications**: Model weights, 13 empirical features, and Assam spatial boundaries for `assam_flood_prototype_v1` remain 100% intact.
- **Zero Synthetic Data Generation**: Datasets (`flood_features.csv`) and USGS seismic records are real verified records.
- **Zero Regressions**: 100% pass rate across 107 automated tests (55 legacy + 18 Phase 15 + 17 Phase 16 + 17 Phase 17).
- **No Deployment / Git Push**: Storage expansion implemented locally without commits, pushes, or deployments.

---

## 1. Database Architecture & Dual-Backend Engine

### Configuration & Pooling
The application engine in `backend/app/database/database.py` dynamically identifies the database dialect from `settings.DATABASE_URL`:
- **SQLite (Development / CI)**:
  - Default URL: `sqlite:///./risk_india.db`
  - Arguments: `check_same_thread=False`
  - Startup: Automatic non-destructive table initialization via `Base.metadata.create_all()` and idempotent state seeding.
- **PostgreSQL 16 (Production via `psycopg 3.3.5`)**:
  - URL format: `postgresql+psycopg://user:password@host:5432/risk_india`
  - Connection Pool: `QueuePool`
  - Sizing parameters: `pool_size=10`, `max_overflow=20`, `pool_timeout=30s`, `pool_recycle=1800s`
  - Liveness pre-ping: `pool_pre_ping=True` (eliminates stale connections from firewall/NAT idle disconnects).

---

## 2. Alembic Database Migration Framework

Production schema management is decoupled from startup execution using official Alembic tooling:
- **Configuration**: `alembic.ini`
- **Environment**: `alembic/env.py` (dynamically loads `settings.DATABASE_URL` and imports all registered ORM models)
- **Script Template**: `alembic/script.py.mako`
- **Initial Canonical Migration**: `alembic/versions/001_initial_schema.py`
  - Reversible DDL: full `upgrade()` creating `locations`, `disaster_events`, `risk_assessments`, `risk_factors`, `resources` and full `downgrade()` dropping in foreign key dependency order.
  - Tested and verified on clean database instances.

---

## 3. Query-Driven Database Indexing

Indexes were added to address specific production query patterns:

| Table | Indexed Columns | Query Justification |
| :--- | :--- | :--- |
| `locations` | `id`, `name`, `administrative_type`, `state_code`, `region` | Rapid state filtering (`/api/locations?type=STATE`) and spatial lookups. |
| `disaster_events` | `location_id`, `disaster_type`, `severity`, `status`, `started_at` | High-frequency chronological filtering (`order_by(started_at.desc())`). |
| `resources` | `name`, `resource_type`, `category`, `location_id`, `verification_status` | Multi-parameter verified aid directory searches (`/api/resources?category=...`). |
| `risk_assessments` | `location_id` | Join optimization with location telemetry. |
| `risk_factors` | `assessment_id` | Foreign-key join query acceleration. |

---

## 4. PostGIS Readiness & Spatial Architecture

The platform prepares for PostGIS without claiming nationwide coverage or generating synthetic spatial geometries:
- **Authoritative Data**: Real coordinates (`latitude`, `longitude`) in EPSG:4326 (WGS84) remain the single source of truth.
- **Serialization Helpers**:
  - `Location.as_geojson_point()`: Standard GeoJSON `{"type": "Point", "coordinates": [lon, lat]}` (RFC 7946).
  - `Location.as_wkt_point()`: Well-Known Text `SRID=4326;POINT(lon lat)`.
  - `DisasterEvent.as_geojson_point()` & `as_wkt_point()`.
- **Production PostGIS DDL Migration**:
  ```sql
  CREATE EXTENSION IF NOT EXISTS postgis;
  ALTER TABLE locations ADD COLUMN geom geometry(Point, 4326);
  UPDATE locations SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326);
  CREATE INDEX idx_locations_geom ON locations USING GIST (geom);

  ALTER TABLE disaster_events ADD COLUMN geom geometry(Point, 4326);
  -- Geometry derived from related location coordinates:
  UPDATE disaster_events SET geom = (SELECT geom FROM locations WHERE locations.id = disaster_events.location_id);
  CREATE INDEX idx_disaster_events_geom ON disaster_events USING GIST (geom);
  ```

---

## 5. Idempotent Seeding Architecture

In `backend/app/database/init_db.py`:
- `auto_seed_database(db)` executes individual presence checks on every location, assessment, and factor.
- **Idempotency Guarantee**: Running the application multiple times results in 0 duplicate records.
- **Production Safeguard**: When `APP_ENV=production`, auto-seeding is skipped automatically. Production data is loaded via controlled migration workflows.

---

## 6. Cache Abstraction Layer & Freshness Honesty

In `backend/app/services/cache_service.py`:
- **Interface**: `BaseCacheService` (`get`, `set`, `delete`, `clear`, `is_healthy`).
- **Implementations**:
  - `MemoryCacheService`: Thread-safe, bounded, timestamped in-memory TTL cache (default).
  - `RedisCacheService`: Redis client with connection timeouts and automatic error suppression.
- **Graceful Fallback**: If Redis is requested but unavailable, the factory logs a warning and automatically falls back to `MemoryCacheService`. Zero application crashes.
- **Freshness Honesty**: Cached disaster records retain their original observation timestamps (`observed_at`). Freshness (`LIVE`, `RECENT`, `STALE`, `UNAVAILABLE`) is recomputed dynamically against the current time upon retrieval. Cached telemetry is **never** falsely promoted to `LIVE`.

---

## 7. Health & Observability Separation

In `backend/app/api/routes/health.py`:
- `GET /api/health`: Existing comprehensive health check returning service, database, cache, and provider telemetry.
- `GET /api/health/liveness`: Pure application process liveness probe. Zero external dependencies. Returns HTTP 200 `status: alive`.
- `GET /api/health/readiness`: Orchestrator readiness check verifying primary database connectivity (`SELECT 1`) and ML model availability. Returns HTTP 200 `ready` or HTTP 503 `not_ready`.

---

## 8. Measured Performance Benchmarks

Actual measured query latencies across 50 iterations (running on local SQLite database):
- **Location Retrieval (all 37 States & UTs)**: `0.527 ms`
- **Single Location by ID / State Code (indexed)**: `0.301 ms`
- **Risk Assessment + Factors (joined query)**: `0.800 ms`
- **Disaster Events (indexed by status)**: `0.243 ms`
- **Relief Resources (indexed by verification)**: `0.193 ms`

*All core queries execute in under 1.0 millisecond.*

---

## 9. Verification & Automated Test Results

### Automated Test Execution
- **Command**: `python -m unittest discover tests`
- **Total Test Count**: **107 tests**
  - Legacy Core Suite: 55 tests (**PASS**)
  - Phase 15 Reliability Suite: 18 tests (**PASS**)
  - Phase 16 Security Suite: 17 tests (**PASS**)
  - Phase 17 Data Platform Suite: 17 tests (**PASS**)
- **Results**: **107 Passed, 0 Failed, 0 Errors (100% Pass Rate)**
- **Total Execution Time**: **16.338s**
- **Regressions**: **0**

### Frontend Production Build
- **Command**: `npm run build`
- **Result**: Built successfully in 2.18s with 0 errors.
