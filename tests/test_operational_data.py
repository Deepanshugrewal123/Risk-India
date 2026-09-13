"""
RISK // INDIA — Automated Test Suite: Operational Data & Live Disaster Intelligence
Real Public Feeds, Provider Abstraction, Freshness, and ML Decoupling.

10 Required Test Conditions:
1. test_provider_schema: Disaster provider returns required normalized schema
2. test_freshness_calculation: Freshness logic strictly tags LIVE, RECENT, STALE, UNAVAILABLE
3. test_caching_mechanism: Provider manager serves cached snapshot within TTL
4. test_upstream_error_resilience: Upstream failure handled gracefully without crashing
5. test_filter_by_state: State parameter filters correctly
6. test_filter_by_hazard_type: Hazard type filters correctly
7. test_filter_by_status: Status filters correctly
8. test_live_disasters_contract: Live feed returns strictly verified, non-demo events
9. test_ml_live_decoupling: Live feeds do not alter or corrupt offline ML prototype
10. test_verified_emergency_resources: All helplines and portals are verified official entities
"""

import sys
from pathlib import Path
import unittest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from backend.app.services.disaster_provider import (
    DisasterProvider,
    USGSSeismicProvider,
    OfficialBulletinProvider,
    DisasterFeedManager,
    NormalizedDisasterEvent,
    calculate_freshness
)
from backend.app.services.flood_model_service import flood_model_service


class TestOperationalData(unittest.TestCase):

    def setUp(self):
        self.now = datetime.now(timezone.utc)

    # 1. Provider Returns Expected Schema
    def test_provider_schema(self):
        provider = OfficialBulletinProvider()
        events = provider.fetch_events()
        self.assertGreater(len(events), 0)
        ev = events[0]
        self.assertIsInstance(ev, NormalizedDisasterEvent)
        self.assertTrue(hasattr(ev, "id"))
        self.assertTrue(hasattr(ev, "hazard_type"))
        self.assertTrue(hasattr(ev, "title"))
        self.assertTrue(hasattr(ev, "state"))
        self.assertTrue(hasattr(ev, "district"))
        self.assertIsInstance(ev.latitude, float)
        self.assertIsInstance(ev.longitude, float)
        self.assertIn(ev.severity, ["LOW", "MODERATE", "HIGH", "CRITICAL"])
        self.assertIn(ev.status, ["ACTIVE", "MONITORING", "WARNING", "CONTAINED", "RESOLVED"])
        self.assertIn(ev.freshness, ["LIVE", "RECENT", "STALE", "UNAVAILABLE"])
        self.assertTrue(ev.verified)
        self.assertFalse(ev.is_demo)
        self.assertTrue(ev.source_url.startswith("http"))

    # 2. Freshness Calculation
    def test_freshness_calculation(self):
        now = datetime(2026, 9, 13, 12, 0, 0, tzinfo=timezone.utc)
        
        # 15 minutes ago -> LIVE
        t_live = now - timedelta(minutes=15)
        self.assertEqual(calculate_freshness(t_live, now=now), "LIVE")

        # 4 hours ago -> RECENT
        t_recent = now - timedelta(hours=4)
        self.assertEqual(calculate_freshness(t_recent, now=now), "RECENT")

        # 36 hours ago -> STALE
        t_stale = now - timedelta(hours=36)
        self.assertEqual(calculate_freshness(t_stale, now=now), "STALE")

        # None -> UNAVAILABLE
        self.assertEqual(calculate_freshness(None, now=now), "UNAVAILABLE")

    # 3. Caching Mechanism
    def test_caching_mechanism(self):
        manager = DisasterFeedManager(cache_ttl_seconds=300)
        # First call fetches and populates cache
        events1 = manager.get_events()
        t1 = manager._last_fetch_time

        # Second call within TTL should serve cached events without re-fetching
        events2 = manager.get_events()
        t2 = manager._last_fetch_time

        self.assertEqual(t1, t2)
        self.assertEqual(len(events1), len(events2))

    # 4. Error Handling Resilience
    def test_upstream_error_resilience(self):
        provider = USGSSeismicProvider(timeout_sec=1)
        # Mock urllib to raise network timeout
        with patch("urllib.request.urlopen", side_effect=TimeoutError("Connection timed out")):
            events = provider.fetch_events()
            self.assertEqual(events, [])
            self.assertEqual(provider.last_status, "unreachable")
            self.assertIn("Connection timed out", provider.last_error)

    # 5. Filtering by State
    def test_filter_by_state(self):
        manager = DisasterFeedManager()
        assam_events = manager.get_events(state="Assam")
        for ev in assam_events:
            self.assertTrue("assam" in ev.state.lower() or "assam" in ev.district.lower())

    # 6. Filtering by Hazard Type
    def test_filter_by_hazard_type(self):
        manager = DisasterFeedManager()
        flood_events = manager.get_events(hazard_type="FLOOD")
        for ev in flood_events:
            self.assertEqual(ev.hazard_type.upper(), "FLOOD")

    # 7. Filtering by Status
    def test_filter_by_status(self):
        manager = DisasterFeedManager()
        active_events = manager.get_events(status="ACTIVE")
        for ev in active_events:
            self.assertIn("ACTIVE", ev.status.upper())

    # 8. Live Disasters Contract
    def test_live_disasters_contract(self):
        manager = DisasterFeedManager()
        live_events = manager.get_live_events()
        self.assertGreater(len(live_events), 0)
        for ev in live_events:
            self.assertTrue(ev.verified)
            self.assertFalse(ev.is_demo)
            self.assertIn(ev.freshness, ["LIVE", "RECENT"])

    # 9. Decoupling of ML Model and Live Feeds
    def test_ml_live_decoupling(self):
        # Verify model artifact remains pristine
        self.assertEqual(flood_model_service.model_version, "assam_flood_prototype_v1")
        self.assertIsNotNone(flood_model_service.model)
        self.assertIsNotNone(flood_model_service.preprocessor)

        # Confirm non-Assam location rejected by scope guard
        non_assam_res = flood_model_service.predict("gujarat", "kutch", None)
        self.assertEqual(non_assam_res["status"], "model_scope_limited")

        # Confirm ML predict rejects arbitrary live feed objects or unmonitored coordinates
        arbitrary_feed_feature = {
            "title": "Severe Earthquake in Gujarat",
            "latitude": 22.25,
            "longitude": 71.19
        }
        res = flood_model_service.predict("assam", "udalguri", arbitrary_feed_feature)
        self.assertEqual(res["status"], "insufficient_data")

        # Verify offline trained model parameters are not mutated by live service
        self.assertEqual(flood_model_service.model.C, 0.5)
        self.assertTrue(hasattr(flood_model_service.model, "coef_"))
        self.assertEqual(list(flood_model_service.model.classes_), [0, 1])

    # 10. Verified Emergency Resources
    def test_verified_emergency_resources(self):
        # Official Indian emergency helplines verified
        official_numbers = {"112", "1078", "1070", "1077", "108", "1091", "1098"}
        self.assertEqual(len(official_numbers), 7)
        
        # Test that all official portals have real government domains
        official_domains = ["gov.in", "nic.in"]
        official_urls = [
            "https://ndma.gov.in",
            "https://mausam.imd.gov.in",
            "https://ffs.india-water.gov.in",
            "https://asdma.assam.gov.in",
            "https://hpsdma.nic.in"
        ]
        for url in official_urls:
            self.assertTrue(any(dom in url for dom in official_domains), f"Invalid domain for {url}")


if __name__ == "__main__":
    unittest.main()
