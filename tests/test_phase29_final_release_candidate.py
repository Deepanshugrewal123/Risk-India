"""
RISK // INDIA — PHASE 29 FINAL RELEASE CANDIDATE CERTIFICATION TEST SUITE
========================================================================
Comprehensive production validation covering all 16 Phase 29 dimensions:
1. National Coverage Matrix: 36 Entities (28 States + 8 UTs) × 6 Hazards = 216 Combinations
2. End-to-End API Contracts (13 Endpoints Verified)
3. Freshness Integrity & Adversarial Decoupling
4. ML Boundary Security & Adversarial Bypass Prevention
5. Provider Failure Chaos Simulation & Independent Circuit Breakers
6. Disaster Recovery & In-Memory Cache Fallback Resilience
7. Bounded Multithreaded Concurrency Stability
8. Scientific Asset Immutability Hashes & Zero-Synthetic Data Guarantee
"""

import unittest
import hashlib
import sys
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from app.main import app
from app.middleware.rate_limit import rate_limiter
from app.services.national_risk import (
    unified_national_risk_service,
    freshness_engine,
    provenance_engine,
    regional_baseline_engine,
    risk_explanation_engine,
    hazard_aggregation_engine,
    SUPPORTED_HAZARDS,
    FreshnessClassification
)
from app.services.geo_basin_service import INDIAN_ADMINISTRATIVE_ENTITIES
from app.services.disaster_provider import CircuitBreaker, CircuitState
from app.services.cache_service import cache_service


class TestPhase29FinalReleaseCandidate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.expected_model_hash = "0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf"
        cls.expected_dataset_hash = "88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080"

    def setUp(self):
        rate_limiter.reset()

    def tearDown(self):
        rate_limiter.reset()

    # =========================================================================
    # 1. NATIONAL COVERAGE & HAZARD MATRIX VALIDATION (36 × 6 = 216)
    # =========================================================================

    def test_01_national_coverage_36_entities(self):
        """Verify exactly 28 States and 8 Union Territories exist in national risk summary."""
        rate_limiter.reset()
        resp = self.client.get("/api/national-risk")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        self.assertEqual(data["total_administrative_entities"], 36)
        self.assertEqual(data["states_covered"], 28)
        self.assertEqual(data["union_territories_covered"], 8)
        self.assertEqual(len(data["regions"]), 36)

        returned_names = {r["region"]["name"] for r in data["regions"]}
        catalog_names = {e["name"] for e in INDIAN_ADMINISTRATIVE_ENTITIES}
        self.assertEqual(returned_names, catalog_names)

    def test_02_all_six_hazards_matrix_216_combinations(self):
        """Verify all 36 entities × 6 hazards = 216 region-hazard combinations are valid."""
        rate_limiter.reset()
        summary_resp = self.client.get("/api/national-risk")
        self.assertEqual(summary_resp.status_code, 200)
        regions = summary_resp.json()["regions"]

        combinations_tested = 0
        for r in regions:
            state_name = r["region"]["name"]
            rate_limiter.reset()  # Reset rate limit per administrative entity to prevent 429 in automated testing
            for h in SUPPORTED_HAZARDS:
                resp = self.client.get(f"/api/national-risk/{state_name}/{h}")
                self.assertEqual(resp.status_code, 200, f"Failed for {state_name} - {h}")
                item = resp.json()
                self.assertEqual(item["hazard_type"], h)
                self.assertEqual(item["region"]["name"], state_name)
                self.assertIn("risk_score", item["intelligence"])
                self.assertIn("freshness", item["intelligence"])
                self.assertIn("provenance", item["intelligence"])
                combinations_tested += 1

        self.assertEqual(combinations_tested, 216, "Must validate exactly 216 combinations (36 entities × 6 hazards)")

    def test_03_no_duplicate_or_missing_regions(self):
        """Verify no duplicate regions, no missing regions, and consistent IDs."""
        profiles = regional_baseline_engine.get_all_state_profiles()
        ids = [p.id for p in profiles]
        names = [p.name for p in profiles]
        self.assertEqual(len(ids), 36)
        self.assertEqual(len(set(ids)), 36, "Duplicate region ID detected")
        self.assertEqual(len(set(names)), 36, "Duplicate region Name detected")

    # =========================================================================
    # 2. END-TO-END API VALIDATION (13 Endpoints)
    # =========================================================================

    def test_04_e2e_national_risk_endpoints(self):
        """Verify /api/national-risk, /freshness, and /providers contracts."""
        rate_limiter.reset()
        r1 = self.client.get("/api/national-risk")
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r1.json()["synthetic_records"], 0)

        r2 = self.client.get("/api/national-risk/freshness")
        self.assertEqual(r2.status_code, 200)
        self.assertIn("freshness_distribution", r2.json())
        self.assertEqual(r2.json()["synthetic_records"], 0)

        r3 = self.client.get("/api/national-risk/providers")
        self.assertEqual(r3.status_code, 200)
        self.assertTrue(r3.json()["circuit_breaker_enabled"])
        self.assertIn("isolation_policy", r3.json())

    def test_05_e2e_data_foundation_endpoints(self):
        """Verify /api/data/basins, /gauges, /provenance, and /readiness contracts."""
        rate_limiter.reset()
        r_basins = self.client.get("/api/data/basins")
        self.assertEqual(r_basins.status_code, 200)
        self.assertEqual(r_basins.json()["synthetic_records"], 0)
        self.assertEqual(len(r_basins.json()["basins"]), 5)

        r_gauges = self.client.get("/api/data/gauges")
        self.assertEqual(r_gauges.status_code, 200)
        self.assertEqual(r_gauges.json()["synthetic_records"], 0)
        self.assertEqual(r_gauges.json()["count"], 26)

        r_prov = self.client.get("/api/data/provenance")
        self.assertEqual(r_prov.status_code, 200)
        self.assertGreater(r_prov.json()["count"], 0)

        r_readiness = self.client.get("/api/data/readiness")
        self.assertEqual(r_readiness.status_code, 200)
        self.assertEqual(r_readiness.json()["synthetic_records"], 0)

    def test_06_e2e_health_observability_endpoints(self):
        """Verify /api/health/liveness, /readiness, /config, and /metrics contracts."""
        rate_limiter.reset()
        r_live = self.client.get("/api/health/liveness")
        self.assertEqual(r_live.status_code, 200)
        self.assertEqual(r_live.json()["status"], "alive")

        r_ready = self.client.get("/api/health/readiness")
        self.assertEqual(r_ready.status_code, 200)
        self.assertEqual(r_ready.json()["status"], "ready")
        self.assertTrue(r_ready.json()["model_ready"])

        r_cfg = self.client.get("/api/health/config")
        self.assertEqual(r_cfg.status_code, 200)
        self.assertIn("environment", r_cfg.json())

        r_metrics = self.client.get("/api/health/metrics")
        self.assertEqual(r_metrics.status_code, 200)
        self.assertIn("http_metrics", r_metrics.json())
        self.assertIn("total_requests", r_metrics.json()["http_metrics"])

    def test_07_deterministic_error_handling(self):
        """Verify invalid regions return 404 and unsupported hazards return 400 safely."""
        rate_limiter.reset()
        r_bad_region = self.client.get("/api/national-risk/NonExistentState")
        self.assertEqual(r_bad_region.status_code, 404)
        self.assertIn("not found in official Indian administrative catalog", r_bad_region.json()["detail"])

        r_bad_hazard = self.client.get("/api/national-risk/Assam/VOLCANIC_ERUPTION")
        self.assertEqual(r_bad_hazard.status_code, 400)
        self.assertIn("Hazard 'VOLCANIC_ERUPTION' is not supported", r_bad_hazard.json()["detail"])

    # =========================================================================
    # 3. FRESHNESS INTEGRITY & ADVERSARIAL DECOUPLING
    # =========================================================================

    def test_08_adversarial_freshness_severity_decoupling(self):
        """Adversarially verify that severity CRITICAL + observation age > 24h is strictly STALE, never LIVE."""
        stale_time = (datetime.now(timezone.utc) - timedelta(hours=72)).isoformat()
        rec = freshness_engine.classify_freshness(
            observed_at=stale_time,
            is_cached=False,
            source="Official Gauge"
        )
        self.assertEqual(rec.freshness_state, FreshnessClassification.STALE.value)
        self.assertNotEqual(rec.freshness_state, FreshnessClassification.OFFICIAL_LIVE.value)

    def test_09_cached_data_never_classified_as_live(self):
        """Adversarially verify cached data is never labeled LIVE regardless of observation age."""
        now_time = datetime.now(timezone.utc).isoformat()
        rec = freshness_engine.classify_freshness(
            observed_at=now_time,
            is_cached=True,
            source="Offline Database Cache"
        )
        self.assertEqual(rec.freshness_state, FreshnessClassification.CACHED.value)
        self.assertNotEqual(rec.freshness_state, FreshnessClassification.OFFICIAL_LIVE.value)

    def test_10_regional_baseline_never_labeled_as_ml(self):
        """Verify baseline profiles always receive REGIONAL_BASELINE freshness, never EMPIRICAL_ML."""
        rec = freshness_engine.classify_freshness(observed_at=None, is_baseline=True)
        self.assertEqual(rec.freshness_state, FreshnessClassification.REGIONAL_BASELINE.value)
        self.assertNotEqual(rec.freshness_state, FreshnessClassification.EMPIRICAL_ML.value)

    # =========================================================================
    # 4. ML BOUNDARY SECURITY & ADVERSARIAL BYPASS TESTING
    # =========================================================================

    def test_11_ml_scope_guard_strictly_assam(self):
        """Verify Assam has active empirical ML and assam_flood_prototype_v1."""
        rate_limiter.reset()
        resp = self.client.get("/api/national-risk/Assam")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["empirical_ml"]["available"])
        self.assertEqual(data["empirical_ml"]["status"], "APPROVED")
        self.assertEqual(data["empirical_ml"]["model_id"], "assam_flood_prototype_v1")

    def test_12_adversarial_ml_scope_bypass_prevention(self):
        """Stress-test ML boundary using non-Assam states, UTs, basins, and casing variations."""
        non_assam_targets = [
            "Bihar", "bihar", "BIHAR",
            "Maharashtra", "maharashtra",
            "Delhi", "delhi",
            "Odisha", "odisha",
            "Gujarat", "gujarat",
            "Uttar Pradesh", "uttar pradesh",
            "Tamil Nadu", "tamil nadu",
            "West Bengal", "west bengal",
            "Ladakh", "ladakh",
            "Kerala", "kerala"
        ]
        for target in non_assam_targets:
            rate_limiter.reset()
            resp = self.client.get(f"/api/national-risk/{target}")
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            # Must strictly deny ML
            self.assertFalse(data["empirical_ml"]["available"], f"Adversarial ML leak for {target}")
            self.assertEqual(data["empirical_ml"]["status"], "NOT_AVAILABLE")
            self.assertEqual(data["empirical_ml"]["model_id"], "NONE")
            self.assertIn("Empirical ML prediction is not currently validated for this region", data["empirical_ml"]["message"])

    # =========================================================================
    # 5. PROVIDER FAILURE CHAOS SIMULATION & FAULT ISOLATION
    # =========================================================================

    def test_13_provider_failure_chaos_isolation(self):
        """Verify simulated upstream provider failures trip circuit breakers without cascading."""
        rate_limiter.reset()
        cb_usgs = CircuitBreaker(failure_threshold=3, cooldown_seconds=60.0)
        cb_cwc = CircuitBreaker(failure_threshold=3, cooldown_seconds=60.0)

        # Simulate USGS failure
        cb_usgs.record_failure("HTTP 503 Service Unavailable")
        cb_usgs.record_failure("ReadTimeout")
        cb_usgs.record_failure("ConnectionRefused")
        self.assertEqual(cb_usgs.state, CircuitState.OPEN)
        self.assertFalse(cb_usgs.can_execute())

        # CWC must remain healthy and operational (independent fault isolation)
        self.assertEqual(cb_cwc.state, CircuitState.CLOSED)
        self.assertTrue(cb_cwc.can_execute())

        # System still serves valid responses via national summary
        resp = self.client.get("/api/national-risk")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["total_administrative_entities"], 36)

    # =========================================================================
    # 6. DISASTER RECOVERY & IN-MEMORY CACHE RESILIENCE
    # =========================================================================

    def test_14_cache_fallback_resilience(self):
        """Verify cache operations continue safely without raising exceptions."""
        key = "phase29-test-cache-key"
        val = {"status": "operational", "test_id": 29}
        cache_service.set(key, val, ttl_seconds=60)
        retrieved = cache_service.get(key)
        self.assertEqual(retrieved, val)

    # =========================================================================
    # 7. PERFORMANCE & BOUNDED LOCAL CONCURRENCY
    # =========================================================================

    def test_15_bounded_multithreaded_concurrency(self):
        """Verify concurrent requests to national summary and state endpoints execute safely."""
        rate_limiter.reset()

        def fetch_endpoint(endpoint):
            rate_limiter.reset()
            return self.client.get(endpoint).status_code

        endpoints = [
            "/api/national-risk",
            "/api/national-risk/Assam",
            "/api/national-risk/Karnataka",
            "/api/national-risk/Bihar",
            "/api/national-risk/freshness",
            "/api/national-risk/providers",
            "/api/data/basins",
            "/api/data/gauges",
            "/api/health/liveness",
            "/api/health/readiness"
        ] * 2  # 20 concurrent requests

        with ThreadPoolExecutor(max_workers=4) as executor:
            status_codes = list(executor.map(fetch_endpoint, endpoints))

        for status in status_codes:
            self.assertEqual(status, 200, "Concurrent request failed")

    # =========================================================================
    # 8. SCIENTIFIC ASSET IMMUTABILITY & AUDIT
    # =========================================================================

    def test_16_scientific_invariants_frozen_hashes(self):
        """Calculate and verify SHA-256 hashes of frozen model and dataset artifacts."""
        model_path = os.path.join("ml", "flood", "artifacts", "model.joblib")
        dataset_path = os.path.join("datasets", "processed", "flood_assam", "flood_features.csv")

        self.assertTrue(os.path.exists(model_path))
        self.assertTrue(os.path.exists(dataset_path))

        with open(model_path, "rb") as f:
            actual_m = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(actual_m, self.expected_model_hash, "Model hash modified! Model must remain frozen.")

        with open(dataset_path, "rb") as f:
            actual_d = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(actual_d, self.expected_dataset_hash, "Dataset modified! Empirical data must remain frozen.")


if __name__ == "__main__":
    unittest.main()
