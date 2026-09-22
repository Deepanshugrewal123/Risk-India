# RISK // INDIA — Production Deployment & Operations Runbook

Comprehensive production deployment, containerization, and operations guide for the **RISK // INDIA** AI-Powered Disaster Risk Analyzer & Management System.

---

## 1. System Architecture & Container Topology

RISK // INDIA is architected as a modular 4-tier micro-service topology orchestrated via Docker Compose or Kubernetes:

```
                          [ Internet / Client Traffic ]
                                        │
                                        ▼ (Port 80/443)
                 ┌──────────────────────────────────────────────┐
                 │          NGINX INGRESS / SPA SERVER           │
                 │         (risk-india-frontend:80)             │
                 │  - Serves compiled React 18 / Vite SPA       │
                 │  - Reverse-proxies /api/ requests to backend │
                 │  - Injects security headers & gzip           │
                 └──────────────────────┬───────────────────────┘
                                        │
                                        ▼ (Internal risk-india-network:8000)
                 ┌──────────────────────────────────────────────┐
                 │       FASTAPI ASGI APPLICATION CLUSTER       │
                 │          (risk-india-backend:8000)           │
                 │  - Gunicorn master + 4 Uvicorn ASGI workers  │
                 │  - Frozen ML Model (assam_flood_prototype_v1)│
                 │  - Multi-Hazard Provider Engine (USGS/CWC/IMD)│
                 │  - Lifespan connection pool management       │
                 └──────────────┬────────────────┬──────────────┘
                                │                │
        (Internal: 5432)        ▼                ▼ (Internal: 6379)
┌─────────────────────────────────────────┐   ┌─────────────────────────────────────────┐
│     POSTGRESQL 16 RELATIONAL STORE      │   │         REDIS 7 DISTRIBUTED CACHE       │
│         (risk-india-postgres)           │   │           (risk-india-redis)            │
│  - National spatial entities (28+8)     │   │  - Telemetry cache (TTL 300s)           │
│  - Multi-hazard event tables            │   │  - Rate limiting sliding windows        │
│  - Audited emergency relief hubs        │   │  - Dynamic freshness recalculation      │
│  - Persistent volume: postgres_data     │   │  - Persistent volume: redis_data        │
└─────────────────────────────────────────┘   └─────────────────────────────────────────┘
```

### Inviolate Scientific & Engineering Guarantees
- **assam_flood_prototype_v1 is Frozen**: Model weights, 13 features, and 32 training observations are immutable. No online retraining.
- **Explicit Regional ML Scope**: ML risk prediction is strictly restricted to Assam. All other 27 states and 8 UTs receive Regional Baseline Risk and Official Live Telemetry.
- **Zero Synthetic Telemetry**: Upstream sensor failures degrade gracefully to cached stale status or inactive status. No synthetic alerts are ever generated.
- **Storage Port Isolation**: PostgreSQL (5432) and Redis (6379) ports are strictly internal to `risk-india-network` and NEVER published to host.

---

## 2. Hardware & Host Sizing Specifications

| Deployment Tier | Virtual CPUs (vCPU) | RAM | Storage (SSD/NVMe) | Max Concurrent Users | Target Workload |
|---|---|---|---|---|---|
| **Staging / Evaluation** | 2 vCPU | 4 GB | 20 GB | ~100 | QA, integration tests, baseline audit |
| **Production Baseline** | 4 vCPU | 8 GB | 50 GB | ~1,000 | Normal operations, daily hazard feeds |
| **Emergency Scaled** | 8–16 vCPU | 16–32 GB | 100+ GB | ~10,000+ | Active cyclone / severe flood emergency |

---

## 3. Network & Port Requirements

| Service | Container Port | Host Port | Network Scope | Protocol | Purpose |
|---|---|---|---|---|---|
| `frontend` (Nginx) | 80 | 80 (or 443 with TLS) | Public / Ingress | HTTP / HTTPS | Web traffic & API reverse proxy |
| `backend` (FastAPI) | 8000 | None (Internal) | `risk-india-network` | HTTP (ASGI) | REST API & ML computation |
| `postgres` | 5432 | None (Internal) | `risk-india-network` | TCP | Relational state & spatial entities |
| `redis` | 6379 | None (Internal) | `risk-india-network` | TCP | Caching & rate limiting state |

**Egress Firewall Requirements**:
The backend container requires outbound HTTPS access (port 443) to:
- `earthquake.usgs.gov` (USGS Seismic feed)
- `ffs.india-water.gov.in` (CWC Flood monitoring bulletins)
- `mausam.imd.gov.in` / `rsmcnewdelhi.imd.gov.in` (IMD Weather & Cyclone bulletins)

---

## 4. Environment Variables Reference

| Variable | Type | Default | Production Recommendation | Description |
|---|---|---|---|---|
| `APP_NAME` | string | `risk-india-api` | `risk-india-api` | Application logging and tracing identifier |
| `APP_ENV` | string | `development` | `production` | Environment mode (`production` disables auto-seed, activates Alembic enforcement) |
| `DEBUG` | boolean | `true` | `false` | Disables debug stack traces in production API responses |
| `PORT` | integer | `8000` | `8000` | Internal container port for FastAPI |
| `WEB_CONCURRENCY` | integer | `4` | `4` (or `2 * vCPU + 1`) | Gunicorn Uvicorn worker process count |
| `LOG_LEVEL` | string | `INFO` | `INFO` | Structured JSON log verbosity |
| `DATABASE_URL` | string | `sqlite:///./risk_india.db` | `postgresql+psycopg2://<user>:<pwd>@postgres:5432/<db>` | Database connection URI |
| `DB_POOL_SIZE` | integer | `10` | `10` | SQLAlchemy QueuePool baseline connection count |
| `DB_MAX_OVERFLOW` | integer | `20` | `20` | Maximum burst connections beyond pool size |
| `DB_POOL_TIMEOUT` | integer | `30` | `30` | Timeout in seconds waiting for connection from pool |
| `DB_POOL_RECYCLE` | integer | `1800` | `1800` | Connection lifetime in seconds to prevent stale pool drops |
| `REDIS_URL` | string | `None` | `redis://redis:6379/0` | Redis distributed cache connection string |
| `CACHE_BACKEND` | string | `memory` | `redis` | Cache provider (`redis` or fallback to `memory`) |
| `CACHE_TTL_SECONDS`| integer | `300` | `300` | Feed and assessment cache TTL in seconds |
| `CORS_ORIGINS` | string | `http://localhost:5173,...` | `https://risk-india.gov.in` | Strict whitelist of allowed origins (no wildcards) |
| `ENABLE_HSTS` | boolean | `false` | `true` | Enables HTTP Strict Transport Security (max-age=31536000) |
| `RATE_LIMIT_GENERAL`| integer| `60` | `60` | Max requests per minute per IP for general endpoints |
| `RATE_LIMIT_COMPUTE`| integer| `10` | `10` | Max requests per minute per IP for `/api/risk/analyze` |

---

## 5. Container Registry & Image Building

To build the production images locally:

```bash
# 1. Build Backend Image (Multi-worker Gunicorn + ML artifacts)
docker build -t risk-india-backend:latest -f Dockerfile.backend .

# 2. Build Frontend Image (Node.js 20 build -> Alpine Nginx)
docker build -t risk-india-frontend:latest -f Dockerfile.frontend .
```

---

## 6. Docker Compose Quickstart

### Step 1: Configure Environment Variables
Copy `.env.example` to `.env` and set strong, secure passwords:
```bash
cp .env.example .env
# Edit .env and supply:
# POSTGRES_PASSWORD=<strong_random_secret_32_chars>
# APP_ENV=production
# DEBUG=false
```

### Step 2: Start Services
```bash
# Start in detached mode
docker compose up -d

# Verify all 4 containers are healthy
docker compose ps
```

### Step 3: Check Health
```bash
# Test Frontend Ingress
curl -I http://localhost/healthz

# Test Backend Readiness Probe via Nginx reverse proxy
curl http://localhost/api/health/readiness
```

---

## 7. Production Database Provisioning (PostgreSQL 16 + PostGIS)

If deploying against an external managed PostgreSQL instance (e.g. AWS RDS, Azure Database for PostgreSQL, or Google Cloud SQL):

1. **Provision PostgreSQL 16 Instance** with at least 2 vCPU and 4 GB RAM.
2. **Enable Spatial Extensions**:
   ```sql
   CREATE DATABASE risk_india;
   \c risk_india;
   CREATE EXTENSION IF NOT EXISTS postgis;
   ```
3. **Create Application User**:
   ```sql
   CREATE USER risk_app_user WITH PASSWORD '<strong_password>';
   GRANT ALL PRIVILEGES ON DATABASE risk_india TO risk_app_user;
   GRANT ALL ON SCHEMA public TO risk_app_user;
   ```

---

## 8. Alembic Migration Strategy & Zero-Downtime Releases

In production (`APP_ENV=production`), automatic runtime DDL table creation is disabled. All schema migrations must be executed explicitly:

```bash
# Run migrations inside the backend container
docker compose exec backend alembic upgrade head

# Check current revision status
docker compose exec backend alembic current
```

**Zero-Downtime Migration Rule**:
- Migrations must be backward-compatible (add columns, don't drop or rename active columns in the same release).
- Follow the **Expand-Contract Pattern**:
  1. Release 1 (Expand): Add nullable column or new table.
  2. Release 2 (Deploy): Update application to write to new column.
  3. Release 3 (Contract): Backfill old records and add NOT NULL / remove obsolete columns.

---

## 9. Redis Cluster / Standalone Configuration

Redis 7 runs with in-memory storage and RDB snapshots every 60s if at least 1 key changed (`--save 60 1`).
- If Redis becomes unavailable, RISK // INDIA automatically degrades to `MemoryCacheService` without crashing or returning HTTP 500 errors.
- Stored cache keys include `hazard_feed:*`, `loc_risk:*`, and `rate_limit:*`.

---

## 10. Nginx Ingress & SSL/TLS Configuration

For HTTPS termination in production, configure Let's Encrypt / Certbot on the host or in an ingress gateway:

```nginx
server {
    listen 443 ssl http2;
    server_name risk-india.gov.in;

    ssl_certificate /etc/letsencrypt/live/risk-india.gov.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/risk-india.gov.in/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://frontend:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

---

## 11. Health Probes (Liveness & Readiness Specification)

| Probe | Endpoint | Status Codes | Evaluation Logic | Orchestrator Action on Failure |
|---|---|---|---|---|
| **Liveness** | `GET /api/health/liveness` | 200 | Confirms ASGI event loop is active and process is alive. No external dependencies. | Restart container if unresponsive after 3 attempts |
| **Readiness** | `GET /api/health/readiness` | 200 (Ready), 503 (Not Ready) | Verifies PostgreSQL connectivity (`SELECT 1`), ML inference model readiness, and Cache health. | Remove container from load balancer ingress pool |
| **Composite** | `GET /api/health` | 200 (ok / degraded) | Full system diagnostic including upstream hazard feeds (USGS, CWC, IMD, GSI). | Monitored by Ops / Prometheus for incident tracking |

---

## 12. Resource Quotas & CPU/Memory Limits

Apply the production hardened overlay `docker-compose.prod.yml`:
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

Resource specifications enforced per container:
- **`backend`**: 4 vCPU limit, 1 vCPU reservation; 4096 MB RAM limit, 1024 MB reservation.
- **`postgres`**: 2 vCPU limit, 0.5 vCPU reservation; 2048 MB RAM limit, 512 MB reservation.
- **`redis`**: 1 vCPU limit, 0.2 vCPU reservation; 512 MB RAM limit, 128 MB reservation.
- **`frontend`**: 1 vCPU limit, 0.1 vCPU reservation; 512 MB RAM limit, 64 MB reservation.

---

## 13. Backup & Disaster Recovery Runbook

### Automated Daily PostgreSQL Backup
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/risk-india"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
mkdir -p "${BACKUP_DIR}"

docker compose exec -T postgres pg_dump -U risk_user -d risk_india -Fc > "${BACKUP_DIR}/risk_india_${TIMESTAMP}.dump"
find "${BACKUP_DIR}" -type f -name "*.dump" -mtime +14 -exec rm {} \;
```

### Database Restore Procedure
```bash
# 1. Stop backend traffic
docker compose stop backend

# 2. Restore database from dump
docker compose exec -T postgres pg_restore -U risk_user -d risk_india --clean < /var/backups/risk-india/risk_india_YYYYMMDD_HHMMSS.dump

# 3. Restart backend
docker compose start backend
```

---

## 14. Secret Management & Key Rotation

- **Zero Secrets in Git**: No credentials, database connection strings, or encryption keys are committed to version control.
- **Environment Injection**: Production secrets are injected into containers via Docker secrets, AWS Secrets Manager, or HashiCorp Vault.
- **Password Rotation**:
  1. Alter PostgreSQL user password in DB.
  2. Update `DATABASE_URL` in `.env`.
  3. Perform rolling restart of `backend` service: `docker compose up -d --no-deps backend`.

---

## 15. Observability (Logs, Metrics, Correlation IDs)

- **Structured JSON Logging**: Every request outputs standardized JSON:
  `{"timestamp": "...", "level": "INFO", "request_id": "uuid4", "method": "GET", "path": "/api/disasters/live", "status_code": 200, "latency_ms": 12.4}`
- **Tracing Header**: `X-Request-ID` is extracted or generated on all inbound requests and propagated into downstream logs and client error responses.
- **Zero PII**: Passwords, connection URIs, and user-submitted notes in Get Help forms are sanitized prior to logging.

---

## 16. High Availability & Horizontal Scaling

The FastAPI backend is completely stateless (application state is stored in PostgreSQL and Redis).
To scale backend processing:
```bash
# Scale to 3 backend container replicas
docker compose up -d --scale backend=3
```
Nginx will automatically distribute requests across backend replicas using upstream round-robin.

---

## 17. Security Hardening & Principle of Least Privilege

1. **Non-Root Execution**: Backend container executes strictly as non-root user `appuser` (UID 10001).
2. **Read-Only Codebase**: Application source files in `/app` are read-only for the container process.
3. **Strict CORS**: Only origins explicitly defined in `CORS_ORIGINS` are accepted. Wildcards (`*`) are disallowed when credentials are enabled.
4. **Rate Limiting**: General endpoints throttled at 60 req/min; compute-heavy risk analysis throttled at 10 req/min per IP.
5. **Security Headers**: All responses carry `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Content-Security-Policy`, and `Strict-Transport-Security`.

---

## 18. Troubleshooting Common Production Incidents

| Symptom | Probable Cause | Diagnostic Command | Remediation Action |
|---|---|---|---|
| `502 Bad Gateway` on `/api/*` | Backend container crashed or restarting | `docker compose logs backend --tail 50` | Inspect logs for unhandled exceptions or missing dependencies; check DB connectivity |
| `503 Service Unavailable` on `/api/health/readiness` | PostgreSQL connection pool exhausted or DB down | `docker compose exec postgres pg_isready` | Verify PostgreSQL service is running; verify `DB_POOL_SIZE` and `DB_MAX_OVERFLOW` settings |
| High response latency (> 2s) | Upstream provider timeout blocking worker thread | `curl http://localhost/api/disasters/providers` | Circuit breaker will trip after 5 failures and serve cached responses; check upstream network egress |
| `429 Too Many Requests` | Client IP exceeding sliding-window rate limit | Inspect client request headers for `X-RateLimit-*` | Check if legitimate client is polling too aggressively; increase `RATE_LIMIT_GENERAL` if warranted |

---

## 19. Rollback Runbook

If a deployment exhibits regressions:
```bash
# 1. Rollback code to previous container image tag
docker compose stop backend frontend
docker tag risk-india-backend:previous risk-india-backend:latest
docker tag risk-india-frontend:previous risk-india-frontend:latest

# 2. If database migration needs rollback:
docker compose run --rm backend alembic downgrade -1

# 3. Restart services
docker compose up -d
```
