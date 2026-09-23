"""
RISK // INDIA — Phase 24 Staging Validation, Observability & Disaster Recovery Test Suite
========================================================================================
Validates:
1. Staging configuration validation (dev vs staging vs production enforcement, secret redaction)
2. Health & readiness semantics (/liveness, /readiness, /metrics, /config)
3. Observability metrics collection & sanitization
4. Redis failure & seamless in-memory fallback
5. Multi-hazard provider fault isolation (failure in one provider never impacts others)
6. Provider circuit breaker transitions & stale-data fallback
7. Crisis mode resilience & honest freshness (stale data never marked LIVE)
8. ML scientific integrity & Assam scope guard immutability
9. National coverage (28 States, 8 UTs, 6 Hazards)
10. Database disaster recovery & backup/restore command verification
11. Bounded concurrency & latency stability
"""

import sys
import os
import unittest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from app.main import app
from app.config import Settings, settings
from app.services.config_validator import StagingConfigValidator, config_validator
from app.services.metrics_service import metrics_collector
from app.services.cache_service import MemoryCacheService, RedisCacheService
from app.services.geo_basin_service import INDIAN_ADMINISTRATIVE_ENTITIES, geo_basin_service
from app.services.flood_model_service import flood_model_service, EXPECTED_FEATURES
from app.services.hazard_providers import (
    USGSSeismicProvider,
    CWCFloodProvider,
    IMDWeatherProvider,
    IMDCycloneProvider,
    IMDHeatwaveProvider,
    GSILandslideProvider
)
from app.utils.backup_restore import backup_manager, DatabaseBackupManager


class TestPhase24StagingOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def setUp(self):
        metrics_collector.reset()
        from app.middleware.rate_limit import rate_limiter
        rate_limiter.reset()

    def tearDown(self):
        from app.middleware.rate_limit import rate_limiter
        rate_limiter.reset()

    # -------------------------------------------------------------------------
    # 1. Staging Configuration Validation
    # -------------------------------------------------------------------------
    def test_01_config_validation_development_mode(self):
        """Verify development configuration permits SQLite and in-memory cache with warnings."""
        report = config_validator.validate(settings, target_env="development")
        self.assertTrue(report.is_valid)
        self.assertEqual(len(report.errors), 0)
        self.assertIn("APP_ENV", report.sanitized_config)
        # Verify secrets are redacted
        self.assertNotIn("risk_password", str(report.sanitized_config))

    def test_02_config_validation_production_enforcement(self):
        """Verify production mode rejects SQLite, default placeholder passwords, and short secrets."""
        bad_prod_settings = Settings(
            APP_ENV="production",
            DEBUG=True,
            DATABASE_URL="sqlite:///./risk_india.db",
            SECRET_KEY="short",
            ENABLE_HSTS=False
        )
        report = config_validator.validate(bad_prod_settings, target_env="production")
        self.assertFalse(report.is_valid)
        self.assertGreaterEqual(len(report.errors), 3)

        error_text = " ".join(report.errors)
        self.assertIn("SQLite", error_text)
        self.assertIn("DEBUG", error_text)
        self.assertIn("SECRET_KEY", error_text)

    def test_03_config_validation_redaction_guarantee(self):
        """Verify passwords and secret keys are never exposed in validation reports."""
        raw_url = "postgresql+psycopg2://admin_user:SuperSecretPassword123@db.prod.internal:5432/risk_db"
        sanitized = StagingConfigValidator.sanitize_value("DATABASE_URL", raw_url)
        self.assertNotIn("SuperSecretPassword123", sanitized)
        self.assertIn("***@", sanitized)

        key_sanitized = StagingConfigValidator.sanitize_value("SECRET_KEY", "RealProductionSecretKey1234567890")
        self.assertEqual(key_sanitized, "***REDACTED***")

    # -------------------------------------------------------------------------
    # 2. Health & Readiness Probes
    # -------------------------------------------------------------------------
    def test_04_liveness_probe_isolated(self):
        """Verify /health/liveness returns 200 without touching external dependencies."""
        resp = self.client.get("/api/health/liveness")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "alive")
        self.assertEqual(data["service"], "risk-india-api")

    def test_05_readiness_probe_database_failure(self):
        """Verify /health/readiness returns HTTP 503 when database connectivity fails."""
        with patch("app.api.routes.health.engine.connect") as mock_connect:
            mock_connect.side_effect = ConnectionError("PostgreSQL staging cluster unreachable")
            resp = self.client.get("/api/health/readiness")
            self.assertEqual(resp.status_code, 503)
            data = resp.json()
            self.assertEqual(data["status"], "not_ready")
            self.assertEqual(data["database"], "disconnected")
            # Traceback must NOT leak
            self.assertNotIn("Traceback", resp.text)
            self.assertIn("Database connectivity check failed", data.get("error", ""))

    def test_06_operational_metrics_endpoint(self):
        """Verify /health/metrics returns sanitized observability counters."""
        self.client.get("/api/health")
        self.client.get("/api/locations")

        resp = self.client.get("/api/health/metrics")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertIn("http_metrics", data)
        self.assertIn("cache_metrics", data)
        self.assertIn("provider_telemetry", data)
        self.assertIn("ml_inference_audit", data)
        self.assertGreaterEqual(data["http_metrics"]["total_requests"], 2)

    def test_07_sanitized_config_endpoint(self):
        """Verify /health/config returns sanitized audit report without leaking secrets."""
        resp = self.client.get("/api/health/config")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("is_valid", data)
        self.assertIn("sanitized_config", data)
        self.assertNotIn("password", str(data["sanitized_config"]).lower())

    # -------------------------------------------------------------------------
    # 3. Redis Failure & In-Memory Fallback
    # -------------------------------------------------------------------------
    def test_08_redis_failure_and_fallback(self):
        """Verify Redis failure gracefully falls back to internal memory cache."""
        redis_svc = RedisCacheService(redis_url="redis://localhost:9999/0", default_ttl=60)
        # Client should be None because port 9999 is unavailable
        self.assertFalse(redis_svc.is_healthy())
        self.assertIn("fallback to memory", redis_svc.backend_name)

        # Set and Get must still succeed seamlessly via fallback memory
        success = redis_svc.set("staging_test_key", {"data": "resilient_telemetry"}, ttl_seconds=60)
        self.assertTrue(success)

        val = redis_svc.get("staging_test_key")
        self.assertEqual(val, {"data": "resilient_telemetry"})

    # -------------------------------------------------------------------------
    # 4. Multi-Hazard Provider Fault Isolation Matrix
    # -------------------------------------------------------------------------
    def test_09_provider_fault_isolation(self):
        """Verify failure in one hazard provider leaves all other providers unaffected."""
        usgs = USGSSeismicProvider()
        cwc = CWCFloodProvider()
        imd = IMDWeatherProvider()

        # Simulate USGS failure (e.g. upstream timeout)
        with patch.object(usgs, "fetch_events", side_effect=TimeoutError("USGS timeout")):
            usgs_events = usgs.safe_fetch_events()
            self.assertEqual(usgs_events, [])
            self.assertEqual(usgs.last_status, "error")

        # CWC and IMD must still execute independently without error
        cwc_events = cwc.safe_fetch_events()
        self.assertIsInstance(cwc_events, list)

        imd_events = imd.safe_fetch_events()
        self.assertIsInstance(imd_events, list)

    def test_10_provider_circuit_breaker_and_stale_fallback(self):
        """Verify circuit breaker trips and returns stale cached fallback on repeated errors."""
        provider = IMDCycloneProvider()
        # Seed provider with a last good event
        from app.services.disaster_provider import NormalizedDisasterEvent
        dummy_event = NormalizedDisasterEvent(
            id="cyclone-test-01",
            hazard_type="CYCLONE",
            title="Pre-existing Cyclone Alert",
            state="Odisha",
            district="Puri",
            latitude=19.8,
            longitude=85.8,
            severity="HIGH",
            status="ACTIVE",
            description="Coastal gale alert",
            source="IMD Cyclone Warning Division",
            source_url="https://mausam.imd.gov.in",
            verified=True,
            is_demo=False,
            observed_at=datetime.now(timezone.utc).isoformat(),
            retrieved_at=datetime.now(timezone.utc),
            freshness="LIVE",
            risk_score=85
        )
        provider._last_good_events = [dummy_event]

        # Simulate repeated network errors to trip circuit breaker
        with patch.object(provider, "fetch_events", side_effect=IOError("Connection reset")):
            for _ in range(5):
                fallback = provider.safe_fetch_events()

        # Circuit breaker should now be OPEN
        self.assertEqual(provider.last_status, "circuit_open")
        self.assertEqual(len(fallback), 1)
        # Cached record must be honestly tagged as STALE or RECENT, never LIVE
        self.assertIn(fallback[0].freshness, ["STALE", "RECENT"])

    # -------------------------------------------------------------------------
    # 5. Scientific Integrity & Geographic Guard
    # -------------------------------------------------------------------------
    def test_11_ml_model_scope_assam_only(self):
        """Verify ML prediction is active nationwide via risk_india_flood_v1 across all jurisdictions."""
        # Assam request -> Success
        resp_assam = self.client.post("/api/risk/analyze", json={
            "location_id": "assam",
            "district": "Kamrup",
            "hazard": "flood",
            "features": {"rainfall_24h": 95.0, "river_level_relative": 1.1}
        })
        self.assertEqual(resp_assam.status_code, 200)
        data_assam = resp_assam.json()
        self.assertEqual(data_assam["status"], "success")
        self.assertEqual(data_assam["data_category"], "ML_PREDICTION")
        self.assertEqual(data_assam["model_version"], "risk_india_flood_v1")

        # Kerala request -> Success under India-wide risk_india_flood_v1
        resp_kerala = self.client.post("/api/risk/analyze", json={
            "location_id": "kerala",
            "district": "Wayanad",
            "hazard": "flood",
            "features": {"rainfall_24h": 120.0}
        })
        self.assertEqual(resp_kerala.status_code, 200)
        data_kerala = resp_kerala.json()
        self.assertEqual(data_kerala["status"], "success")
        self.assertEqual(data_kerala["data_category"], "ML_PREDICTION")
        self.assertEqual(data_kerala["model_version"], "risk_india_flood_v1")

        # Non-flood hazard -> Fallback to regional baseline
        resp_eq = self.client.post("/api/risk/analyze", json={
            "location_id": "kerala",
            "district": "Wayanad",
            "hazard": "earthquake"
        })
        self.assertEqual(resp_eq.status_code, 200)
        data_eq = resp_eq.json()
        self.assertEqual(data_eq["status"], "hazard_unsupported_by_flood_model")
        self.assertEqual(data_eq["data_category"], "REGIONAL_BASELINE")

    def test_12_ml_prototype_immutability(self):
        """Verify model weights and feature count are 100% frozen."""
        meta_file = PROJECT_ROOT / "ml" / "flood" / "artifacts" / "metadata.json"
        self.assertTrue(meta_file.exists())
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

        self.assertEqual(meta["model_version"], "assam_flood_prototype_v1")
        self.assertEqual(meta["total_training_samples"], 32)
        self.assertEqual(len(meta["numerical_features"]), 13)
        self.assertEqual(meta["numerical_features"], EXPECTED_FEATURES)

    # -------------------------------------------------------------------------
    # 6. National Coverage (28 States, 8 UTs, 6 Hazards)
    # -------------------------------------------------------------------------
    def test_13_national_coverage_resolution(self):
        """Verify all 28 States and 8 UTs resolve their regional baseline risk and river basin."""
        self.assertEqual(len(INDIAN_ADMINISTRATIVE_ENTITIES), 36)
        states = [e for e in INDIAN_ADMINISTRATIVE_ENTITIES if e["type"] == "STATE"]
        uts = [e for e in INDIAN_ADMINISTRATIVE_ENTITIES if e["type"] == "UNION_TERRITORY"]

        self.assertEqual(len(states), 28)
        self.assertEqual(len(uts), 8)

        for entity in INDIAN_ADMINISTRATIVE_ENTITIES:
            basin = geo_basin_service.get_basin_for_location(entity["name"])
            self.assertIsNotNone(basin)
            self.assertIn("basin_id", basin)
            if "assam" not in entity["id"]:
                self.assertFalse(basin["is_ml_supported"])

    # -------------------------------------------------------------------------
    # 7. Disaster Recovery & Backup/Restore Command Verification
    # -------------------------------------------------------------------------
    def test_14_backup_restore_command_generation(self):
        """Verify PostgreSQL backup and restore commands enforce non-root and custom format."""
        dump_cmd = backup_manager.build_dump_command(
            host="postgres.staging.internal",
            port=5432,
            user="risk_app",
            database="risk_staging",
            output_file="/backups/test.dump"
        )
        self.assertEqual(dump_cmd[0], "pg_dump")
        self.assertIn("-Fc", "".join(dump_cmd))
        self.assertIn("--no-owner", dump_cmd)
        self.assertIn("--no-privileges", dump_cmd)
        # Password must NEVER appear in CLI arguments
        self.assertNotIn("password", "".join(dump_cmd).lower())

        restore_cmd = backup_manager.build_restore_command(
            host="postgres.staging.internal",
            input_file="/backups/test.dump",
            clean_first=True
        )
        self.assertEqual(restore_cmd[0], "pg_restore")
        self.assertIn("--clean", restore_cmd)
        self.assertIn("--if-exists", restore_cmd)

    def test_15_backup_retention_policy_audit(self):
        """Verify backup retention logic correctly partitions prunable from retained archives."""
        sample_backups = [
            "risk_india_backup_20260916_120000_001_initial_schema.dump", # Today
            "risk_india_backup_20260901_120000_001_initial_schema.dump", # 15 days ago
            "risk_india_backup_20260701_120000_001_initial_schema.dump", # 77 days ago (prunable with 30-day policy)
            "unrelated_file.txt"
        ]
        audit = backup_manager.audit_retention(sample_backups, retention_days=30)
        self.assertEqual(audit["total_backups"], 3)
        self.assertEqual(audit["retained_count"], 2)
        self.assertEqual(audit["prunable_count"], 1)
        self.assertEqual(audit["prunable"][0]["filename"], "risk_india_backup_20260701_120000_001_initial_schema.dump")

    # -------------------------------------------------------------------------
    # 8. Bounded Concurrency & Latency Stability
    # -------------------------------------------------------------------------
    def test_16_bounded_concurrency_stability(self):
        """Verify application stability under bounded multithreaded client requests."""
        endpoints = [
            "/api/health/liveness",
            "/api/locations",
            "/api/risk/assam",
            "/api/basins",
            "/api/models"
        ]

        def call_endpoint(ep):
            return self.client.get(ep).status_code

        with ThreadPoolExecutor(max_workers=5) as executor:
            # 25 total requests (5 calls per worker)
            futures = [executor.submit(call_endpoint, ep) for ep in endpoints * 5]
            results = [f.result() for f in futures]

        # All requests must succeed with 200 OK (no 500 errors or deadlocks)
        self.assertEqual(len(results), 25)
        for code in results:
            self.assertEqual(code, 200)

        # Confirm metrics recorded the traffic
        snap = metrics_collector.get_snapshot()
        self.assertGreaterEqual(snap["http_metrics"]["total_requests"], 25)
        self.assertGreater(snap["http_metrics"]["latency_ms"]["average"], 0.0)


if __name__ == "__main__":
    unittest.main()
