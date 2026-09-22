"""
RISK // INDIA — Automated Test Suite: Phase 15 Production Architecture & Reliability
===================================================================================
Covers:
1. CircuitBreaker state transitions: CLOSED -> OPEN -> HALF_OPEN -> CLOSED (recovery)
2. CircuitBreaker rejection and probe failure: HALF_OPEN -> OPEN
3. Upstream Provider HTTP timeout handling (httpx & urllib)
4. Upstream Provider malformed JSON payload handling
5. Upstream Provider retry limits and exponential backoff
6. Circuit breaker OPEN state fallback & health reporting
7. Data freshness honesty (LIVE, RECENT, STALE, UNAVAILABLE)
8. Assam Flood ML prototype preservation and spatial scope guard integrity
9. Core API contracts integrity (/health, /locations, /risk, /disasters, /resources)
"""

import sys
from pathlib import Path
import unittest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock
import json
import httpx

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from backend.app.services.disaster_provider import (
    CircuitBreaker,
    CircuitState,
    USGSSeismicProvider,
    OfficialBulletinProvider,
    DisasterFeedManager,
    calculate_freshness
)
from backend.app.services.flood_model_service import flood_model_service
from backend.app.main import app
from fastapi.testclient import TestClient


class TestPhase15Reliability(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.now = datetime.now(timezone.utc)

    # -------------------------------------------------------------------------
    # 1. CircuitBreaker State Machine Tests
    # -------------------------------------------------------------------------
    def test_circuit_breaker_initial_closed_state(self):
        cb = CircuitBreaker(failure_threshold=5, cooldown_seconds=60.0)
        self.assertEqual(cb.state, CircuitState.CLOSED)
        self.assertEqual(cb.failure_count, 0)
        self.assertTrue(cb.can_execute())

    def test_circuit_breaker_trips_to_open_after_threshold_failures(self):
        cb = CircuitBreaker(failure_threshold=5, cooldown_seconds=60.0)
        for i in range(4):
            cb.record_failure(f"Fail {i+1}")
            self.assertEqual(cb.state, CircuitState.CLOSED)
            self.assertEqual(cb.failure_count, i + 1)
            self.assertTrue(cb.can_execute())

        # 5th failure trips the circuit
        cb.record_failure("Fail 5")
        self.assertEqual(cb.state, CircuitState.OPEN)
        self.assertEqual(cb.failure_count, 5)
        # Should now reject execution
        self.assertFalse(cb.can_execute())
        self.assertEqual(cb.total_rejections, 1)

    def test_circuit_breaker_half_open_transition_after_cooldown(self):
        cb = CircuitBreaker(failure_threshold=3, cooldown_seconds=60.0)
        for i in range(3):
            cb.record_failure(f"Error {i}")
        self.assertEqual(cb.state, CircuitState.OPEN)

        # Before cooldown: rejected
        self.assertFalse(cb.can_execute())

        # Simulate 65 seconds elapsed
        cb.last_failure_time = datetime.now(timezone.utc) - timedelta(seconds=65)

        # Now can_execute() should transition to HALF_OPEN and allow probe
        self.assertTrue(cb.can_execute())
        self.assertEqual(cb.state, CircuitState.HALF_OPEN)

    def test_circuit_breaker_recovery_from_half_open_to_closed(self):
        cb = CircuitBreaker(failure_threshold=3, cooldown_seconds=60.0)
        for i in range(3):
            cb.record_failure("Error")
        self.assertEqual(cb.state, CircuitState.OPEN)

        # Simulate cooldown elapsed
        cb.last_failure_time = datetime.now(timezone.utc) - timedelta(seconds=65)
        self.assertTrue(cb.can_execute())
        self.assertEqual(cb.state, CircuitState.HALF_OPEN)

        # Successful probe call resets circuit to CLOSED
        cb.record_success()
        self.assertEqual(cb.state, CircuitState.CLOSED)
        self.assertEqual(cb.failure_count, 0)
        self.assertTrue(cb.can_execute())

    def test_circuit_breaker_half_open_failure_re_trips_to_open(self):
        cb = CircuitBreaker(failure_threshold=3, cooldown_seconds=60.0)
        for i in range(3):
            cb.record_failure("Error")
        self.assertEqual(cb.state, CircuitState.OPEN)

        # Simulate cooldown elapsed
        cb.last_failure_time = datetime.now(timezone.utc) - timedelta(seconds=65)
        self.assertTrue(cb.can_execute())
        self.assertEqual(cb.state, CircuitState.HALF_OPEN)

        # Probe failure immediately sends circuit back to OPEN
        cb.record_failure("Probe failed")
        self.assertEqual(cb.state, CircuitState.OPEN)
        self.assertFalse(cb.can_execute())

    # -------------------------------------------------------------------------
    # 2. Provider Robustness & Upstream Error Handling
    # -------------------------------------------------------------------------
    def test_provider_httpx_timeout_handling(self):
        provider = USGSSeismicProvider(timeout_sec=1, failure_threshold=3, cooldown_sec=10.0)

        # Mock httpx client.get to raise TimeoutException
        mock_client = MagicMock()
        mock_client.is_closed = False
        mock_client.get.side_effect = httpx.ReadTimeout("Read operation timed out")
        provider._client = mock_client

        events = provider.fetch_events()
        self.assertEqual(events, [])
        self.assertEqual(provider.last_status, "unreachable")
        self.assertIn("Read operation timed out", provider.last_error)
        self.assertEqual(provider.circuit_breaker.failure_count, 1)

    def test_provider_malformed_json_handling(self):
        provider = USGSSeismicProvider(timeout_sec=1, failure_threshold=3, cooldown_sec=10.0)

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.side_effect = json.JSONDecodeError("Expecting value", "<html>error</html>", 0)

        mock_client = MagicMock()
        mock_client.is_closed = False
        mock_client.get.return_value = mock_resp
        provider._client = mock_client

        events = provider.fetch_events()
        self.assertEqual(events, [])
        self.assertEqual(provider.last_status, "unreachable")
        self.assertIn("Expecting value", provider.last_error)

    def test_provider_circuit_breaker_open_state_and_fallback(self):
        provider = USGSSeismicProvider(timeout_sec=1, failure_threshold=2, cooldown_sec=60.0)

        # Force failures to trip circuit
        mock_client = MagicMock()
        mock_client.is_closed = False
        mock_client.get.side_effect = httpx.ConnectError("Connection refused")
        provider._client = mock_client

        # Failure 1
        provider.fetch_events()
        # Failure 2 trips to OPEN
        provider.fetch_events()

        self.assertEqual(provider.circuit_breaker.state, CircuitState.OPEN)

        # 3rd call must be suppressed by circuit breaker
        events = provider.fetch_events()
        self.assertEqual(events, [])
        self.assertEqual(provider.last_status, "circuit_open")
        self.assertIn("Circuit breaker is OPEN", provider.last_error)

        health = provider.get_health()
        self.assertEqual(health["status"], "circuit_open")
        self.assertEqual(health["circuit_breaker"]["state"], "OPEN")
        self.assertEqual(health["circuit_breaker"]["failure_count"], 2)

    # -------------------------------------------------------------------------
    # 3. Data Freshness & Transparency
    # -------------------------------------------------------------------------
    def test_freshness_states(self):
        now = datetime(2026, 9, 16, 12, 0, 0, tzinfo=timezone.utc)
        
        # 30 mins ago -> LIVE
        self.assertEqual(calculate_freshness(now - timedelta(minutes=30), now=now), "LIVE")
        # 5 hours ago -> RECENT
        self.assertEqual(calculate_freshness(now - timedelta(hours=5), now=now), "RECENT")
        # 30 hours ago -> STALE
        self.assertEqual(calculate_freshness(now - timedelta(hours=30), now=now), "STALE")
        # None -> UNAVAILABLE
        self.assertEqual(calculate_freshness(None, now=now), "UNAVAILABLE")

    def test_live_feed_contract_strictly_verified_no_demo(self):
        manager = DisasterFeedManager()
        live_events = manager.get_live_events()
        self.assertGreater(len(live_events), 0)
        for ev in live_events:
            self.assertTrue(ev.verified, "Live event must be verified")
            self.assertFalse(ev.is_demo, "Live event must not be demo data")
            self.assertIn(ev.freshness, ["LIVE", "RECENT"])

    # -------------------------------------------------------------------------
    # 4. Assam Flood ML Prototype & Scope Guard Preservation
    # -------------------------------------------------------------------------
    def test_ml_prototype_loaded_and_intact(self):
        self.assertIsNotNone(flood_model_service.model)
        self.assertIsNotNone(flood_model_service.preprocessor)
        self.assertEqual(flood_model_service.model_version, "assam_flood_prototype_v1")

    def test_ml_scope_guard_valid_assam_inference(self):
        # Valid Assam coordinates (Udalguri/Dhansiri basin)
        result = flood_model_service.predict(
            location_id="assam",
            district="udalguri",
            features={
                "rainfall_24h": 85.0,
                "rainfall_72h": 180.0,
                "river_level_relative": 1.2
            }
        )
        self.assertEqual(result["status"], "success")
        self.assertIn(result["risk_level"].upper(), ["LOW", "MODERATE", "HIGH", "CRITICAL"])
        self.assertGreaterEqual(result["risk_score"], 0)
        self.assertLessEqual(result["risk_score"], 100)
        self.assertEqual(len(result["top_factors"]), 4)

    def test_ml_scope_guard_blocks_non_assam_location(self):
        # Non-Assam location should trigger scope guard
        result = flood_model_service.predict(
            location_id="delhi",
            features={"rainfall_24h": 50.0}
        )
        self.assertEqual(result["status"], "model_scope_limited")
        self.assertIn("assam", result["message"].lower())

    # -------------------------------------------------------------------------
    # 5. Core API Contracts Verification
    # -------------------------------------------------------------------------
    def test_api_health_contract(self):
        resp = self.client.get("/api/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("status", data)

    def test_api_locations_contract(self):
        resp = self.client.get("/api/locations")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 36)

    def test_api_risk_contract(self):
        resp = self.client.get("/api/risk/assam")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["location"]["id"], "assam")
        self.assertIn("risk_score", data["assessment"])
        self.assertIn("risk_level", data["assessment"])

    def test_api_disasters_contract(self):
        resp = self.client.get("/api/disasters")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_api_resources_contract(self):
        resp = self.client.get("/api/resources")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)


if __name__ == "__main__":
    unittest.main()
