"""
RISK // INDIA — Phase 20 Verification Suite
===========================================
Validates:
1. Dockerfile.backend non-root configuration, Gunicorn concurrency, and readiness healthcheck.
2. Dockerfile.frontend multi-stage build, zero node_modules in runtime, and SPA setup.
3. Nginx reverse proxy configuration, SPA fallback, proxy headers, timeouts, gzip, security headers.
4. .dockerignore leak prevention for secrets, SQLite databases, and node_modules.
5. docker-compose.yml service topology, network isolation, volume persistence, and healthchecks.
6. docker-compose.prod.yml resource quotas and log rotation.
7. Environment templates completeness (.env.example, backend/.env.example).
8. Comprehensive deployment documentation (docs/DEPLOYMENT.md).
9. FastAPI lifespan context manager graceful shutdown behavior (engine disposal, cache closure).
10. Health check probes (/health/liveness, /health/readiness) and sensitive information sanitization.
11. Redis cache fallback and close method idempotency.
"""

import os
import sys
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient

from app.main import app, lifespan

from app.config import settings
from app.services.cache_service import (
    BaseCacheService,
    MemoryCacheService,
    RedisCacheService,
    cache_service,
    get_cache_service
)


class TestPhase20ContainerizationAndReliability(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # -------------------------------------------------------------------------
    # 1. Backend Dockerfile Tests
    # -------------------------------------------------------------------------
    def test_dockerfile_backend_exists_and_configured(self):
        path = os.path.join(self.project_root, "Dockerfile.backend")
        self.assertTrue(os.path.exists(path), "Dockerfile.backend must exist at project root.")

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Verify base image
        self.assertIn("FROM python:3.11-slim", content)
        # Verify non-root execution
        self.assertIn("useradd", content)
        self.assertIn("appuser", content)
        self.assertIn("USER appuser", content)
        # Verify process management with Gunicorn + Uvicorn workers
        self.assertIn("gunicorn", content)
        self.assertIn("uvicorn.workers.UvicornWorker", content)
        self.assertIn("app.main:app", content)
        # Verify readiness probe in healthcheck
        self.assertIn("HEALTHCHECK", content)
        self.assertIn("/api/health/readiness", content)
        # Verify frozen ML artifacts are copied
        self.assertIn("COPY ml /app/ml", content)
        # Verify port
        self.assertIn("EXPOSE 8000", content)

    # -------------------------------------------------------------------------
    # 2. Frontend Dockerfile Tests
    # -------------------------------------------------------------------------
    def test_dockerfile_frontend_multi_stage(self):
        path = os.path.join(self.project_root, "Dockerfile.frontend")
        self.assertTrue(os.path.exists(path), "Dockerfile.frontend must exist at project root.")

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Multi-stage check
        self.assertIn("FROM node:20-alpine AS builder", content)
        self.assertIn("npm ci", content)
        self.assertIn("npm run build", content)
        self.assertIn("FROM nginx:1.27-alpine AS production", content)
        # Check copy from builder
        self.assertIn("COPY --from=builder /app/dist /usr/share/nginx/html", content)
        # Check custom nginx config
        self.assertIn("COPY nginx/default.conf /etc/nginx/conf.d/default.conf", content)
        self.assertIn("EXPOSE 80", content)
        self.assertIn("HEALTHCHECK", content)
        self.assertIn("/healthz", content)

    # -------------------------------------------------------------------------
    # 3. Nginx Reverse Proxy Configuration Tests
    # -------------------------------------------------------------------------
    def test_nginx_reverse_proxy_configuration(self):
        path = os.path.join(self.project_root, "nginx", "default.conf")
        self.assertTrue(os.path.exists(path), "nginx/default.conf must exist.")

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Upstream backend definition
        self.assertIn("upstream backend_service", content)
        self.assertIn("server backend:8000", content)
        # Reverse proxy location for /api/
        self.assertIn("location /api/", content)
        self.assertIn("proxy_pass http://backend_service;", content)
        # Proxy headers
        self.assertIn("proxy_set_header Host $host;", content)
        self.assertIn("proxy_set_header X-Real-IP $remote_addr;", content)
        self.assertIn("proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;", content)
        self.assertIn("proxy_set_header X-Forwarded-Proto $scheme;", content)
        # Upstream timeouts
        self.assertIn("proxy_connect_timeout 5s;", content)
        self.assertIn("proxy_read_timeout 30s;", content)
        # SPA routing fallback
        self.assertIn("try_files $uri $uri/ /index.html;", content)
        # Caching for assets
        self.assertIn("location /assets/", content)
        self.assertIn("Cache-Control", content)
        # Gzip compression
        self.assertIn("gzip on;", content)
        # Security headers
        self.assertIn("X-Frame-Options", content)
        self.assertIn("X-Content-Type-Options", content)

    # -------------------------------------------------------------------------
    # 4. .dockerignore Leak Prevention Tests
    # -------------------------------------------------------------------------
    def test_dockerignore_rules(self):
        path = os.path.join(self.project_root, ".dockerignore")
        self.assertTrue(os.path.exists(path), ".dockerignore must exist.")

        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        # Ensure secrets and databases are ignored
        self.assertIn(".git", lines)
        self.assertIn(".env", lines)
        self.assertIn("node_modules", lines)
        self.assertIn("__pycache__", lines)
        self.assertIn("tests/", lines)
        self.assertIn("*.db", lines)
        self.assertIn("*.sqlite", lines)

    # -------------------------------------------------------------------------
    # 5. Docker Compose Specification Tests
    # -------------------------------------------------------------------------
    def test_docker_compose_structure(self):
        path = os.path.join(self.project_root, "docker-compose.yml")
        self.assertTrue(os.path.exists(path), "docker-compose.yml must exist.")

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check all 4 core services exist
        self.assertIn("postgres:", content)
        self.assertIn("redis:", content)
        self.assertIn("backend:", content)
        self.assertIn("frontend:", content)

        # Storage port isolation: PostgreSQL and Redis must NOT expose host ports
        # Check that 5432:5432 and 6379:6379 do not exist in ports mappings
        self.assertNotIn('"5432:5432"', content)
        self.assertNotIn("'5432:5432'", content)
        self.assertNotIn('"6379:6379"', content)
        self.assertNotIn("'6379:6379'", content)

        # Frontend must expose port 80
        self.assertIn('"${FRONTEND_PORT:-80}:80"', content)

        # Check health checks on all services
        self.assertIn("pg_isready", content)
        self.assertIn("redis-cli", content)
        self.assertIn("/api/health/readiness", content)
        self.assertIn("/healthz", content)

        # Check isolated network and persistent volumes
        self.assertIn("risk-network:", content)
        self.assertIn("postgres_data:", content)
        self.assertIn("redis_data:", content)

    def test_docker_compose_prod_overlay(self):
        path = os.path.join(self.project_root, "docker-compose.prod.yml")
        self.assertTrue(os.path.exists(path), "docker-compose.prod.yml must exist.")

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("resources:", content)
        self.assertIn("limits:", content)
        self.assertIn("json-file", content)
        self.assertIn("restart: always", content)

    # -------------------------------------------------------------------------
    # 6. Environment Templates Tests
    # -------------------------------------------------------------------------
    def test_environment_templates_completeness(self):
        root_env = os.path.join(self.project_root, ".env.example")
        backend_env = os.path.join(self.project_root, "backend", ".env.example")

        self.assertTrue(os.path.exists(root_env), "Root .env.example must exist.")
        self.assertTrue(os.path.exists(backend_env), "Backend .env.example must exist.")

        with open(root_env, "r", encoding="utf-8") as f:
            root_content = f.read()

        self.assertIn("DATABASE_URL=", root_content)
        self.assertIn("REDIS_URL=", root_content)
        self.assertIn("WEB_CONCURRENCY=", root_content)
        self.assertIn("LOG_LEVEL=", root_content)
        self.assertIn("CORS_ORIGINS=", root_content)
        self.assertIn("ENABLE_HSTS=", root_content)

    # -------------------------------------------------------------------------
    # 7. Documentation Completeness Tests
    # -------------------------------------------------------------------------
    def test_deployment_runbook_completeness(self):
        path = os.path.join(self.project_root, "docs", "DEPLOYMENT.md")
        self.assertTrue(os.path.exists(path), "docs/DEPLOYMENT.md must exist.")

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check key runbook sections
        self.assertIn("1. System Architecture & Container Topology", content)
        self.assertIn("2. Hardware & Host Sizing Specifications", content)
        self.assertIn("3. Network & Port Requirements", content)
        self.assertIn("4. Environment Variables Reference", content)
        self.assertIn("5. Container Registry & Image Building", content)
        self.assertIn("6. Docker Compose Quickstart", content)
        self.assertIn("7. Production Database Provisioning", content)
        self.assertIn("8. Alembic Migration Strategy", content)
        self.assertIn("9. Redis Cluster / Standalone Configuration", content)
        self.assertIn("10. Nginx Ingress & SSL/TLS Configuration", content)
        self.assertIn("11. Health Probes", content)
        self.assertIn("12. Resource Quotas & CPU/Memory Limits", content)
        self.assertIn("13. Backup & Disaster Recovery Runbook", content)
        self.assertIn("14. Secret Management & Key Rotation", content)
        self.assertIn("15. Observability", content)
        self.assertIn("16. High Availability & Horizontal Scaling", content)
        self.assertIn("17. Security Hardening", content)
        self.assertIn("18. Troubleshooting Common Production Incidents", content)
        self.assertIn("19. Rollback Runbook", content)

    # -------------------------------------------------------------------------
    # 8. Application Lifespan & Graceful Teardown Tests
    # -------------------------------------------------------------------------
    def test_fastapi_lifespan_lifecycle(self):
        import asyncio

        async def run_lifespan_test():
            async with lifespan(app):
                # Verify app is healthy during lifespan
                self.assertIsNotNone(app)
            # Lifespan teardown executed cleanly without raising exceptions

        asyncio.run(run_lifespan_test())

    def test_cache_service_close_idempotency(self):
        mem_cache = MemoryCacheService()
        mem_cache.set("test_key", "test_val")
        self.assertEqual(mem_cache.get("test_key"), "test_val")
        mem_cache.close()
        # After close, store is cleared
        self.assertIsNone(mem_cache.get("test_key"))
        # Idempotent call
        mem_cache.close()

    # -------------------------------------------------------------------------
    # 9. Health & Probe Endpoint Tests
    # -------------------------------------------------------------------------
    def test_liveness_probe(self):
        response = self.client.get("/api/health/liveness")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "alive")
        self.assertEqual(data["service"], "risk-india-api")
        self.assertIn("timestamp", data)

    def test_readiness_probe_healthy(self):
        response = self.client.get("/api/health/readiness")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ready")
        self.assertEqual(data["database"], "connected")
        self.assertTrue(data["model_ready"])

    def test_readiness_probe_database_failure_sanitization(self):
        """
        When the database connection fails, readiness must return 503
        and sanitize error messages to avoid leaking credentials.
        """
        with patch("app.api.routes.health.engine.connect", side_effect=Exception("FATAL: password authentication failed for user 'secret_db_user' at 10.0.1.5:5432")):
            response = self.client.get("/api/health/readiness")
            self.assertEqual(response.status_code, 503)
            data = response.json()
            self.assertEqual(data["status"], "not_ready")
            self.assertEqual(data["database"], "disconnected")
            # Must NOT expose sensitive strings from raw exception
            self.assertNotIn("secret_db_user", str(data))
            self.assertNotIn("10.0.1.5", str(data))
            self.assertEqual(data.get("error"), "Database connectivity check failed")

    # -------------------------------------------------------------------------
    # 10. Cache Fallback and Config Tests
    # -------------------------------------------------------------------------
    def test_redis_graceful_fallback(self):
        with patch("app.config.settings.CACHE_BACKEND", "redis"), \
             patch("app.config.settings.REDIS_URL", "redis://non_existent_host_xyz:6379/0"):
            fallback_svc = get_cache_service()
            # Should gracefully fall back to in-memory cache without crashing
            self.assertEqual(fallback_svc.backend_name, "memory")
            fallback_svc.set("probe_key", "probe_val")
            self.assertEqual(fallback_svc.get("probe_key"), "probe_val")

    def test_config_defaults(self):
        self.assertGreaterEqual(settings.WEB_CONCURRENCY, 1)
        self.assertIn(settings.LOG_LEVEL, ["DEBUG", "INFO", "WARNING", "ERROR"])


if __name__ == "__main__":
    unittest.main()
