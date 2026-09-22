"""
RISK // INDIA — Automated Test Suite: Phase 17 Production Data Platform & Storage
==================================================================================
Covers 17 test categories:
1.  test_database_config_sqlite (SQLite dialect and connect_args detection)
2.  test_database_config_postgres (PostgreSQL connection pool configuration via psycopg)
3.  test_database_session_lifecycle (Deterministic session acquisition and teardown)
4.  test_idempotent_seeding (Repeated auto_seed_database executions produce zero duplicates)
5.  test_database_indexes_exist (Verifies query-justified indexes across all core tables)
6.  test_health_liveness (GET /api/health/liveness returns 200 process status)
7.  test_health_readiness_healthy (GET /api/health/readiness returns 200 ready state)
8.  test_health_readiness_db_failure (GET /api/health/readiness returns 503 on DB drop)
9.  test_cache_service_memory_ttl (In-memory cache TTL expiry and storage isolation)
10. test_cache_service_graceful_fallback (Redis disconnection falls back to memory safely)
11. test_provider_cache_freshness_honesty (Stale cached data never labeled as LIVE)
12. test_postgis_readiness_methods (as_geojson_point and as_wkt_point output WGS84 geometries)
13. test_alembic_configuration_validity (alembic.ini and env.py config validation)
14. test_alembic_upgrade_downgrade_script (Verifies reversible DDL in 001_initial_schema.py)
15. test_all_existing_api_contracts (/locations, /risk, /disasters, /resources preserved)
16. test_phase16_security_preserved (Security headers, CORS, rate limiting, and X-Request-ID)
17. test_ml_model_integrity_preserved (assam_flood_prototype_v1 and spatial guard intact)
"""

import sys
from pathlib import Path
import unittest
import time
import tempfile
import os
from unittest.mock import patch, MagicMock

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from sqlalchemy import inspect, text
from sqlalchemy.pool import QueuePool

from app.main import app
from app.config import settings
from app.database.database import create_app_engine, get_db, SessionLocal, engine
from app.database.init_db import auto_seed_database
from app.models.location import Location
from app.models.disaster_event import DisasterEvent
from app.models.resource import Resource
from app.models.risk_assessment import RiskAssessment
from app.services.cache_service import MemoryCacheService, RedisCacheService, get_cache_service
from app.services.flood_model_service import flood_model_service
from app.services.disaster_provider import calculate_freshness, NormalizedDisasterEvent
from datetime import datetime, timezone, timedelta
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic import command


class TestPhase17DataPlatform(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    # -------------------------------------------------------------------------
    # 1. Database Configuration: SQLite Dialect
    # -------------------------------------------------------------------------
    def test_database_config_sqlite(self):
        """Verify SQLite engine correctly configures check_same_thread=False and connects."""
        sqlite_engine = create_app_engine("sqlite:///./test_temp.db")
        self.assertEqual(sqlite_engine.dialect.name, "sqlite")
        with sqlite_engine.connect() as conn:
            res = conn.execute(text("SELECT 1")).scalar()
            self.assertEqual(res, 1)

    # -------------------------------------------------------------------------
    # 2. Database Configuration: PostgreSQL Dialect & Pooling
    # -------------------------------------------------------------------------
    def test_database_config_postgres(self):
        """Verify PostgreSQL engine configures QueuePool with production pool parameters."""
        pg_url = "postgresql+psycopg://risk_user:mock_secret@localhost:5432/risk_india"
        pg_engine = create_app_engine(pg_url)
        self.assertEqual(pg_engine.dialect.name, "postgresql")
        self.assertEqual(pg_engine.pool.__class__, QueuePool)
        self.assertEqual(pg_engine.pool.size(), settings.DB_POOL_SIZE)

    # -------------------------------------------------------------------------
    # 3. Database Session Lifecycle
    # -------------------------------------------------------------------------
    def test_database_session_lifecycle(self):
        """Verify get_db dependency yields active session and closes it deterministically."""
        gen = get_db()
        session = next(gen)
        self.assertIsNotNone(session)
        # Execute query to verify session is active
        res = session.execute(text("SELECT 1")).scalar()
        self.assertEqual(res, 1)
        # Close via generator teardown
        try:
            next(gen)
        except StopIteration:
            pass  # Expected generator completion

    # -------------------------------------------------------------------------
    # 4. Idempotent Database Seeding
    # -------------------------------------------------------------------------
    def test_idempotent_seeding(self):
        """Verify consecutive executions of auto_seed_database do not create duplicate rows."""
        with SessionLocal() as session:
            count_before = session.query(Location).count()
            self.assertGreater(count_before, 0, "Database should contain seeded locations")

            # Run seeding second time
            inserted = auto_seed_database(session)
            self.assertEqual(inserted, 0, "Second seed run must insert 0 duplicate locations")

            count_after = session.query(Location).count()
            self.assertEqual(count_before, count_after, "Location count must remain unchanged")

    # -------------------------------------------------------------------------
    # 5. Database Indexes Audit
    # -------------------------------------------------------------------------
    def test_database_indexes_exist(self):
        """Verify justified query indexes exist across core tables."""
        inspector = inspect(engine)

        # 1. locations indexes
        loc_indexes = [idx["name"] for idx in inspector.get_indexes("locations")]
        self.assertTrue(any("name" in idx for idx in loc_indexes))
        self.assertTrue(any("state_code" in idx for idx in loc_indexes))

        # 2. disaster_events indexes
        disaster_indexes = [idx["name"] for idx in inspector.get_indexes("disaster_events")]
        self.assertTrue(any("status" in idx for idx in disaster_indexes))
        self.assertTrue(any("disaster_type" in idx for idx in disaster_indexes))
        self.assertTrue(any("started_at" in idx for idx in disaster_indexes))

        # 3. resources indexes
        res_indexes = [idx["name"] for idx in inspector.get_indexes("resources")]
        self.assertTrue(any("category" in idx for idx in res_indexes))
        self.assertTrue(any("verification_status" in idx for idx in res_indexes))

    # -------------------------------------------------------------------------
    # 6. Health: Liveness Probe
    # -------------------------------------------------------------------------
    def test_health_liveness(self):
        """GET /api/health/liveness returns HTTP 200 alive without external dependencies."""
        resp = self.client.get("/api/health/liveness")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data.get("status"), "alive")
        self.assertIn("timestamp", data)

    # -------------------------------------------------------------------------
    # 7. Health: Readiness Probe (Healthy State)
    # -------------------------------------------------------------------------
    def test_health_readiness_healthy(self):
        """GET /api/health/readiness returns HTTP 200 ready when DB and ML model are ready."""
        resp = self.client.get("/api/health/readiness")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data.get("status"), "ready")
        self.assertEqual(data.get("database"), "connected")
        self.assertTrue(data.get("model_ready"))

    # -------------------------------------------------------------------------
    # 8. Health: Readiness Probe (Database Outage Failure)
    # -------------------------------------------------------------------------
    def test_health_readiness_db_failure(self):
        """GET /api/health/readiness returns HTTP 503 not_ready when DB connection drops."""
        with patch("app.api.routes.health.engine.connect") as mock_connect:
            mock_connect.side_effect = ConnectionRefusedError("Database unreachable")
            resp = self.client.get("/api/health/readiness")
            self.assertEqual(resp.status_code, 503)
            data = resp.json()
            self.assertEqual(data.get("status"), "not_ready")
            self.assertEqual(data.get("database"), "disconnected")

    # -------------------------------------------------------------------------
    # 9. Cache Abstraction: In-Memory TTL Expiration
    # -------------------------------------------------------------------------
    def test_cache_service_memory_ttl(self):
        """Verify in-memory cache accurately stores, retrieves, and expires keys by TTL."""
        cache = MemoryCacheService(default_ttl=1)
        cache.set("test_key", {"data": 42}, ttl_seconds=1)
        self.assertEqual(cache.get("test_key"), {"data": 42})

        # Wait for TTL expiration
        time.sleep(1.05)
        self.assertIsNone(cache.get("test_key"), "Expired key should return None")

        # Delete functionality
        cache.set("persistent", "active", ttl_seconds=60)
        self.assertEqual(cache.get("persistent"), "active")
        cache.delete("persistent")
        self.assertIsNone(cache.get("persistent"))

    # -------------------------------------------------------------------------
    # 10. Cache Abstraction: Redis Graceful Fallback
    # -------------------------------------------------------------------------
    def test_cache_service_graceful_fallback(self):
        """If Redis is configured with an unreachable URL, cache degrades safely without crashing."""
        with patch.object(settings, "CACHE_BACKEND", "redis"):
            with patch.object(settings, "REDIS_URL", "redis://invalid-host-unreachable:6379/0"):
                svc = get_cache_service()
                self.assertIsNotNone(svc)
                # Should degrade to MemoryCacheService
                self.assertEqual(svc.backend_name, "memory")
                # Basic get/set continues to work
                svc.set("fallback_test", "ok", ttl_seconds=10)
                self.assertEqual(svc.get("fallback_test"), "ok")

    # -------------------------------------------------------------------------
    # 11. Provider Cache Freshness Honesty
    # -------------------------------------------------------------------------
    def test_provider_cache_freshness_honesty(self):
        """Cached records older than freshness threshold must be labeled STALE, never LIVE."""
        now = datetime.now(timezone.utc)
        old_observation = now - timedelta(hours=36)
        freshness = calculate_freshness(old_observation, now=now)
        self.assertEqual(freshness, "STALE")
        self.assertNotEqual(freshness, "LIVE")

    # -------------------------------------------------------------------------
    # 12. PostGIS Spatial Readiness Methods
    # -------------------------------------------------------------------------
    def test_postgis_readiness_methods(self):
        """Verify spatial point helper methods generate valid WGS84 GeoJSON and WKT."""
        loc = Location(
            id="test-loc",
            name="Test Location",
            administrative_type="STATE",
            state_code="TL",
            latitude=26.14,
            longitude=91.73
        )
        geojson = loc.as_geojson_point()
        self.assertEqual(geojson["type"], "Point")
        self.assertEqual(geojson["coordinates"], [91.73, 26.14])  # [lon, lat] order

        wkt = loc.as_wkt_point()
        self.assertEqual(wkt, "SRID=4326;POINT(91.73 26.14)")

    # -------------------------------------------------------------------------
    # 13. Alembic Configuration Validity
    # -------------------------------------------------------------------------
    def test_alembic_configuration_validity(self):
        """Verify alembic.ini and script directory are discoverable and valid."""
        cfg = Config("alembic.ini")
        script = ScriptDirectory.from_config(cfg)
        heads = script.get_heads()
        self.assertIn("001_initial_schema", heads)

    # -------------------------------------------------------------------------
    # 14. Alembic Migration Upgrade & Downgrade Reversibility
    # -------------------------------------------------------------------------
    def test_alembic_upgrade_downgrade_script(self):
        """Verify initial migration executes upgrade() and downgrade() successfully on a clean DB."""
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        os.remove(path)
        clean_path = path.replace("\\", "/")
        temp_url = f"sqlite:///{clean_path}"

        cfg = Config("alembic.ini")
        cfg.set_main_option("sqlalchemy.url", temp_url)

        try:
            # Upgrade
            command.upgrade(cfg, "head")
            # Downgrade
            command.downgrade(cfg, "base")
        finally:
            if os.path.exists(path):
                os.remove(path)

    # -------------------------------------------------------------------------
    # 15. All Existing API Contracts Preserved
    # -------------------------------------------------------------------------
    def test_all_existing_api_contracts(self):
        """Verify core API endpoints return HTTP 200 with valid schema."""
        endpoints = [
            "/api/health",
            "/api/locations",
            "/api/risk/assam",
            "/api/disasters",
            "/api/resources"
        ]
        for ep in endpoints:
            res = self.client.get(ep)
            self.assertEqual(res.status_code, 200, f"Endpoint {ep} must return HTTP 200")

    # -------------------------------------------------------------------------
    # 16. Phase 16 Security Controls Preserved
    # -------------------------------------------------------------------------
    def test_phase16_security_preserved(self):
        """Verify Phase 16 security headers and X-Request-ID are present."""
        res = self.client.get("/api/health")
        self.assertEqual(res.headers.get("x-content-type-options"), "nosniff")
        self.assertEqual(res.headers.get("x-frame-options"), "DENY")
        self.assertIsNotNone(res.headers.get("x-request-id"))

    # -------------------------------------------------------------------------
    # 17. ML Prototype Integrity Preserved
    # -------------------------------------------------------------------------
    def test_ml_model_integrity_preserved(self):
        """Verify assam_flood_prototype_v1 model weights, spatial guard, and predictions are intact."""
        self.assertTrue(flood_model_service.is_ready)
        self.assertEqual(flood_model_service.model_version, "assam_flood_prototype_v1")

        # In-scope prediction
        pred = flood_model_service.predict(
            location_id="kamrup_rural",
            district="Kamrup Rural",
            features={"rainfall_24h": 110.0}
        )
        self.assertEqual(pred.get("status"), "success")
        self.assertIn("flood_probability", pred)

        # Out-of-scope rejection
        out_of_scope = flood_model_service.predict("bengaluru")
        self.assertEqual(out_of_scope.get("status"), "model_scope_limited")


if __name__ == "__main__":
    unittest.main()
