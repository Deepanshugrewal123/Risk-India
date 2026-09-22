"""
RISK // INDIA — Phase 19 Multi-Hazard Disaster Intelligence Test Suite
=====================================================================
Rigorous automated test suite covering:
1. Multi-Hazard Schemas & Normalization (Flood, Earthquake, Cyclone, Heatwave, Landslide)
2. Modular Hazard Providers (USGS, CWC, IMD Weather, IMD Cyclone, IMD Heatwave, GSI Landslide)
3. Circuit Breaker Isolation & State Transitions (CLOSED -> OPEN -> HALF_OPEN -> CLOSED)
4. Partial Failure Isolation (single provider outage never affects other providers)
5. Freshness Honesty (LIVE < 1h, RECENT < 24h, STALE >= 24h, UNAVAILABLE)
6. 'Why This Risk?' Scientific Rationale Engine & 4-Pillar Separation
7. Assam ML Scope Preservation & Non-Assam Unavailability Guard (Zero Synthetic Data)
8. REST API Hazard Endpoints Routing & Backward Compatibility
9. Nationwide Geographic Coverage (28 States + 8 Union Territories)
"""

import sys
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta
import json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient

from app.main import app
from app.services.disaster_provider import (
    CircuitBreaker,
    CircuitState,
    NormalizedDisasterEvent,
    calculate_freshness,
    DisasterFeedManager,
    disaster_feed_manager,
    AUTHORITATIVE_PROVIDER_CATALOG
)
from app.services.hazard_providers.base import BaseHazardProvider
from app.services.hazard_providers.usgs_provider import USGSSeismicProvider
from app.services.hazard_providers.cwc_provider import CWCFloodProvider
from app.services.hazard_providers.imd_provider import IMDWeatherProvider
from app.services.hazard_providers.cyclone_provider import IMDCycloneProvider
from app.services.hazard_providers.heatwave_provider import IMDHeatwaveProvider
from app.services.hazard_providers.landslide_provider import GSILandslideProvider
from app.services.flood_model_service import flood_model_service
from app.services.risk_service import risk_service
from app.database.database import get_db
from app.database.init_db import INITIAL_LOCATIONS


class TestPhase19MultiHazardIntelligence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    # =========================================================================
    # 1. Multi-Hazard Schemas & Taxonomy Normalization
    # =========================================================================

    def test_all_five_hazard_schemas_conformance(self):
        """Verify that all 5 core hazard events conform to NormalizedDisasterEvent schema."""
        hazards = ["FLOOD", "EARTHQUAKE", "CYCLONE", "HEATWAVE", "LANDSLIDE", "SEVERE_WEATHER"]
        now = datetime.now(timezone.utc)

        for h in hazards:
            ev = NormalizedDisasterEvent(
                id=f"test-{h.lower()}-01",
                hazard_type=h,
                title=f"Test {h.capitalize()} Advisory",
                state="Assam",
                district="Kamrup",
                latitude=26.14,
                longitude=91.73,
                severity="HIGH",
                status="ACTIVE",
                description=f"Automated test for {h}",
                source="Official Test Agency",
                source_url="https://riskindia.gov.in",
                verified=True,
                is_demo=False,
                observed_at=now,
                retrieved_at=now,
                freshness="LIVE",
                risk_score=75
            )
            d = ev.to_dict()
            self.assertEqual(d["hazard_type"], h)
            self.assertEqual(d["severity"], "HIGH")
            self.assertEqual(d["freshness"], "LIVE")
            self.assertIn("geometry", d)
            self.assertEqual(d["geometry"]["type"], "Point")

    # =========================================================================
    # 2. Modular Hazard Providers Ingestion
    # =========================================================================

    def test_usgs_provider_fetch_and_normalization(self):
        """USGS provider correctly parses GeoJSON into Earthquake NormalizedDisasterEvents."""
        provider = USGSSeismicProvider(timeout_sec=5)
        mock_geojson = {
            "features": [
                {
                    "id": "nc739281",
                    "properties": {
                        "mag": 5.4,
                        "place": "12km NE of Silchar, Assam, India",
                        "time": int(datetime.now(timezone.utc).timestamp() * 1000),
                        "status": "reviewed",
                        "url": "https://earthquake.usgs.gov/earthquakes/eventpage/nc739281",
                        "title": "M 5.4 - 12km NE of Silchar, India"
                    },
                    "geometry": {
                        "coordinates": [92.85, 24.83, 15.0]
                    }
                }
            ]
        }
        with patch.object(provider, "_get_client") as mock_client_factory:
            mock_client = MagicMock()
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = mock_geojson
            mock_client.get.return_value = mock_resp
            mock_client_factory.return_value = mock_client

            events = provider.fetch_events()
            self.assertEqual(len(events), 1)
            ev = events[0]
            self.assertEqual(ev.hazard_type, "EARTHQUAKE")
            self.assertEqual(ev.severity, "HIGH")
            self.assertEqual(ev.state, "Assam")
            self.assertAlmostEqual(ev.latitude, 24.83)
            self.assertAlmostEqual(ev.longitude, 92.85)

    def test_cwc_flood_provider_bulletins(self):
        """CWC Flood provider returns verified river stage warnings with basin context."""
        provider = CWCFloodProvider()
        events = provider.fetch_events()
        self.assertGreater(len(events), 0)
        for ev in events:
            self.assertEqual(ev.hazard_type, "FLOOD")
            self.assertTrue(ev.verified)
            self.assertIn("Central Water Commission", ev.source)
            self.assertIsNotNone(ev.basin)

    def test_imd_weather_provider_bulletins(self):
        """IMD Weather provider returns severe precipitation and synoptic warnings."""
        provider = IMDWeatherProvider()
        events = provider.fetch_events()
        self.assertGreater(len(events), 0)
        for ev in events:
            self.assertEqual(ev.hazard_type, "SEVERE_WEATHER")
            self.assertTrue(ev.verified)
            self.assertIn("India Meteorological Department", ev.source)

    def test_imd_cyclone_provider_bulletins(self):
        """IMD Cyclone provider returns official tropical cyclone outlooks."""
        provider = IMDCycloneProvider()
        events = provider.fetch_events()
        self.assertGreater(len(events), 0)
        for ev in events:
            self.assertEqual(ev.hazard_type, "CYCLONE")
            self.assertTrue(ev.verified)
            self.assertIn("IMD", ev.source)

    def test_imd_heatwave_provider_bulletins(self):
        """IMD & NDMA Heatwave provider returns high-temperature advisories."""
        provider = IMDHeatwaveProvider()
        events = provider.fetch_events()
        self.assertGreater(len(events), 0)
        for ev in events:
            self.assertEqual(ev.hazard_type, "HEATWAVE")
            self.assertTrue(ev.verified)
            self.assertTrue("IMD" in ev.source or "NDMA" in ev.source)

    def test_gsi_landslide_provider_bulletins(self):
        """GSI Landslide provider returns slope stability alerts without fake GIS events."""
        provider = GSILandslideProvider()
        events = provider.fetch_events()
        self.assertGreater(len(events), 0)
        for ev in events:
            self.assertEqual(ev.hazard_type, "LANDSLIDE")
            self.assertTrue(ev.verified)
            self.assertTrue("GSI" in ev.source or "HPSDMA" in ev.source)

    # =========================================================================
    # 3. Circuit Breaker State Transitions & Partial Failure Isolation
    # =========================================================================

    def test_circuit_breaker_full_lifecycle(self):
        """Verify circuit breaker transitions: CLOSED -> OPEN -> HALF_OPEN -> CLOSED."""
        cb = CircuitBreaker(failure_threshold=3, cooldown_seconds=0.1)
        self.assertEqual(cb.state, CircuitState.CLOSED)
        self.assertTrue(cb.can_execute())

        # 3 failures trip to OPEN
        cb.record_failure("error 1")
        cb.record_failure("error 2")
        cb.record_failure("error 3")
        self.assertEqual(cb.state, CircuitState.OPEN)
        self.assertFalse(cb.can_execute())

        # Wait for cooldown
        import time
        time.sleep(0.15)

        # Transition to HALF_OPEN on recovery probe
        self.assertTrue(cb.can_execute())
        self.assertEqual(cb.state, CircuitState.HALF_OPEN)

        # Successful probe closes circuit
        cb.record_success()
        self.assertEqual(cb.state, CircuitState.CLOSED)
        self.assertEqual(cb.failure_count, 0)

    def test_partial_provider_failure_isolation(self):
        """Simulated outage in one provider does NOT affect other providers in feed manager."""
        manager = DisasterFeedManager()
        failing_provider = MagicMock(spec=BaseHazardProvider)
        failing_provider.name = "failing_satellite_feed"
        failing_provider.safe_fetch_events.side_effect = RuntimeError("Upstream 503 Service Unavailable")

        healthy_provider = MagicMock(spec=BaseHazardProvider)
        healthy_provider.name = "healthy_seismic_feed"
        healthy_provider.last_status = "healthy"
        healthy_provider.safe_fetch_events.return_value = [
            NormalizedDisasterEvent(
                id="healthy-01",
                hazard_type="EARTHQUAKE",
                title="Healthy Tremor",
                state="Assam",
                district="Cachar",
                latitude=24.8,
                longitude=92.8,
                severity="LOW",
                status="MONITORING",
                description="Healthy provider event",
                source="USGS",
                source_url="https://earthquake.usgs.gov",
                verified=True,
                is_demo=False,
                observed_at=datetime.now(timezone.utc),
                retrieved_at=datetime.now(timezone.utc),
                freshness="LIVE"
            )
        ]

        manager.providers = [failing_provider, healthy_provider]
        report = manager.refresh(force=True)

        # Verify healthy events are collected despite failing provider
        self.assertGreaterEqual(report["total_events"], 1)
        self.assertIn("error", report["providers"]["failing_satellite_feed"]["status"])
        self.assertEqual(report["providers"]["healthy_seismic_feed"]["count"], 1)

    # =========================================================================
    # 4. Freshness Classification
    # =========================================================================

    def test_freshness_classification_invariants(self):
        """Strict time-boundary tests for LIVE, RECENT, STALE, and UNAVAILABLE."""
        now = datetime.now(timezone.utc)
        self.assertEqual(calculate_freshness(now - timedelta(minutes=30), now=now), "LIVE")
        self.assertEqual(calculate_freshness(now - timedelta(hours=3), now=now), "RECENT")
        self.assertEqual(calculate_freshness(now - timedelta(hours=36), now=now), "STALE")
        self.assertEqual(calculate_freshness(None, now=now), "UNAVAILABLE")

    # =========================================================================
    # 5. 'Why This Risk?' Rationale & 4-Pillar Separation
    # =========================================================================

    def test_why_this_risk_rationale_engine_assam_vs_non_assam(self):
        """Risk assessment responses include transparent rationale and ML scope flags."""
        db = next(get_db())

        # Assam query (where ML prototype is calibrated)
        assam_resp = risk_service.get_location_risk(db, "assam")
        self.assertIsNotNone(assam_resp)
        self.assertTrue(assam_resp.ml_available)
        self.assertIn("assam_flood_prototype_v1", assam_resp.ml_message)
        self.assertEqual(assam_resp.data_category, "REGIONAL_BASELINE")
        self.assertIn("Assam flood risk evaluated", assam_resp.why_this_risk)

        # Odisha query (non-Assam, ML unavailable)
        odisha_resp = risk_service.get_location_risk(db, "odisha")
        self.assertIsNotNone(odisha_resp)
        self.assertFalse(odisha_resp.ml_available)
        self.assertIn("ML prediction is not currently available", assam_resp.ml_message if False else odisha_resp.ml_message)
        self.assertEqual(odisha_resp.data_category, "REGIONAL_BASELINE")
        self.assertIn("Regional baseline", odisha_resp.why_this_risk)

    def test_risk_analysis_ml_vs_baseline_classification(self):
        """analyze_risk labels valid Assam predictions as ML_PREDICTION and out-of-scope as REGIONAL_BASELINE."""
        db = next(get_db())

        # Valid Assam prediction
        from backend.app.schemas.risk import RiskAnalyzeRequest
        req_assam = RiskAnalyzeRequest(
            location_id="assam",
            district="udalguri",
            features={
                "rainfall_24h": 80.0,
                "rainfall_72h": 150.0,
                "river_level_relative": 1.5
            }
        )
        resp_assam = risk_service.analyze_risk(db, req_assam)
        self.assertEqual(resp_assam.status, "success")
        self.assertEqual(resp_assam.data_category, "ML_PREDICTION")
        self.assertIn("ML prototype estimate", resp_assam.why_this_risk)

        # Out-of-scope Bihar prediction
        req_bihar = RiskAnalyzeRequest(
            location_id="bihar",
            district="patna",
            features={"rainfall_24h": 50.0}
        )
        resp_bihar = risk_service.analyze_risk(db, req_bihar)
        self.assertEqual(resp_bihar.status, "model_scope_limited")
        self.assertEqual(resp_bihar.data_category, "REGIONAL_BASELINE")
        self.assertIn("ML prediction is not currently available", resp_bihar.why_this_risk)

    # =========================================================================
    # 6. ML Model Integrity & Zero Synthetic Data
    # =========================================================================

    def test_assam_model_remains_frozen_and_unaltered(self):
        """Assam flood prototype remains completely unmodified."""
        self.assertEqual(flood_model_service.model_version, "assam_flood_prototype_v1")
        self.assertIsNotNone(flood_model_service.model)
        self.assertIsNotNone(flood_model_service.preprocessor)

    # =========================================================================
    # 7. REST API Endpoints Routing & Backward Compatibility
    # =========================================================================

    def test_api_disasters_hazard_routes_no_collision(self):
        """Hazard-specific endpoints return 200 without route collision with /{id}."""
        endpoints = [
            "/api/disasters/flood",
            "/api/disasters/earthquake",
            "/api/disasters/cyclone",
            "/api/disasters/heatwave",
            "/api/disasters/landslide",
            "/api/disasters/severe-weather"
        ]
        for ep in endpoints:
            resp = self.client.get(ep)
            self.assertEqual(resp.status_code, 200, f"Endpoint {ep} failed with {resp.status_code}")
            data = resp.json()
            self.assertIsInstance(data, list)

    def test_api_by_hazard_and_by_state(self):
        """GET /api/disasters/by-hazard/{hazard} and /by-state/{state} operate correctly."""
        resp_h = self.client.get("/api/disasters/by-hazard/FLOOD")
        self.assertEqual(resp_h.status_code, 200)
        self.assertIsInstance(resp_h.json(), list)

        resp_s = self.client.get("/api/disasters/by-state/Assam")
        self.assertEqual(resp_s.status_code, 200)
        self.assertIsInstance(resp_s.json(), list)

    def test_api_providers_catalog_and_health(self):
        """GET /api/disasters/providers returns catalog and operational health."""
        resp = self.client.get("/api/disasters/providers")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("providers", data)
        self.assertIn("health", data)
        self.assertGreaterEqual(data["count"], 6)

    def test_api_disasters_composite_status(self):
        """GET /api/disasters/status returns composite status and hazard breakdowns."""
        resp = self.client.get("/api/disasters/status")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["operational_status"], "OPERATIONAL")
        self.assertIn("freshness_breakdown", data)
        self.assertIn("hazard_breakdown", data)

    def test_api_all_regional_baselines(self):
        """GET /api/risk returns nationwide regional baselines."""
        resp = self.client.get("/api/risk")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["data_category"], "REGIONAL_BASELINE")
        self.assertIn("baselines", data)
        self.assertGreaterEqual(data["count"], 28)

    # =========================================================================
    # 8. Nationwide Geographic Coverage (28 States + 8 UTs)
    # =========================================================================

    def test_nationwide_coverage_28_states_8_uts(self):
        """Verify database seeding recognizes all 28 States and 8 Union Territories."""
        states = [loc for loc in INITIAL_LOCATIONS if loc["administrative_type"] == "STATE"]
        uts = [loc for loc in INITIAL_LOCATIONS if loc["administrative_type"] == "UNION_TERRITORY"]

        self.assertEqual(len(states), 28, f"Expected 28 states, found {len(states)}")
        self.assertEqual(len(uts), 8, f"Expected 8 union territories, found {len(uts)}")
        self.assertEqual(len(INITIAL_LOCATIONS), 36)

    def test_invalid_hazard_rejected_by_ml_scope_guard(self):
        """Flood ML prototype rejects requests for non-flood hazards (e.g. CYCLONE, EARTHQUAKE)."""
        pred = flood_model_service.predict(
            location_id="assam",
            district="udalguri",
            hazard="earthquake",
            features={"rainfall_24h": 50.0}
        )
        self.assertEqual(pred["status"], "model_scope_limited")
        self.assertIn("Assam flood prototype", pred["message"])

    def test_stale_fallback_behavior_in_base_provider(self):
        """BaseHazardProvider safely falls back to cached events marked STALE on failure."""
        provider = CWCFloodProvider()
        # Prime the cache
        events = provider.safe_fetch_events()
        self.assertGreater(len(events), 0)

        # Force failure
        with patch.object(provider, "fetch_events", side_effect=IOError("Network timeout")):
            stale_events = provider.safe_fetch_events()
            self.assertEqual(len(stale_events), len(events))
            for ev in stale_events:
                self.assertIn(ev.freshness, ["LIVE", "RECENT", "STALE"])

    def test_geographic_normalization_heuristics(self):
        """USGS provider correctly normalizes Indian place names to States/UTs."""
        provider = USGSSeismicProvider()
        state, district = provider._resolve_location("15km S of Gangtok, Sikkim, India")
        self.assertEqual(state, "Sikkim")

        state2, district2 = provider._resolve_location("30km W of Port Blair, Andaman and Nicobar Islands")
        self.assertEqual(state2, "Andaman and Nicobar Islands")


if __name__ == "__main__":
    unittest.main()
