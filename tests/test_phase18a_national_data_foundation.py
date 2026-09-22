"""
RISK // INDIA — Automated Test Suite: Phase 18A National Data Foundation & Multi-Hazard Intelligence
====================================================================================================
Comprehensive tests validating:
1. Authoritative Provider Catalog & Source Tiers
2. Normalized Multi-Hazard Schema & Field Backward Compatibility
3. Deterministic Spatio-Temporal Event Deduplication (5 scenarios)
4. India Administrative Normalization (28 States + 8 UTs = 36 Entities)
5. River Basin Foundation & Hydrological Resolution
6. Data Quality Gates & Quarantine Mechanism
7. Dataset Manifest & Strict Zero-Synthetic Record Guarantee
8. Model Registry Architecture & Assam Prototype Scope Guard
9. Public ML Honesty & Unsupported-Region Behavior
10. Provider Failure Isolation & Circuit Breaker Recovery
11. REST API Endpoints Integration (/api/basins, /api/models, /api/datasets/manifests, /api/disasters/providers, /api/disasters/status)
"""

import sys
from pathlib import Path
import unittest
from datetime import datetime, timezone, timedelta

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi.testclient import TestClient
from app.main import app
from app.services.disaster_provider import (
    disaster_feed_manager,
    NormalizedDisasterEvent,
    AUTHORITATIVE_PROVIDER_CATALOG,
    CircuitBreaker,
    CircuitState
)
from app.services.event_deduplication import EventDeduplicator, haversine_distance_km
from app.services.geo_basin_service import geo_basin_service, INDIAN_ADMINISTRATIVE_ENTITIES, RIVER_BASINS_CATALOG
from app.services.ml_data_pipeline import (
    DataQualityGate,
    RawObservation,
    MLDataPipelineManager,
    PipelineStage
)
from app.services.dataset_manifest import dataset_manifest_registry
from app.services.model_registry import model_registry, ModelStatus
from app.services.flood_model_service import flood_model_service


class TestPhase18ANationalDataFoundation(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.now = datetime.now(timezone.utc)

    # 1. Authoritative Provider Catalog
    def test_authoritative_provider_catalog(self):
        catalog = disaster_feed_manager.get_provider_catalog()
        self.assertIsInstance(catalog, list)
        self.assertGreaterEqual(len(catalog), 8)

        provider_ids = [p["provider_id"] for p in catalog]
        self.assertIn("usgs_seismic", provider_ids)
        self.assertIn("imd_mausam", provider_ids)
        self.assertIn("cwc_ffs", provider_ids)
        self.assertIn("asdma_assam", provider_ids)
        self.assertIn("ndma_india", provider_ids)
        self.assertIn("isro_bhuvan_disaster", provider_ids)

        # Check source tier validity
        valid_tiers = {"LIVE_API", "PUBLIC_WEB_DATA", "DOWNLOADABLE_DATA", "AUTHENTICATED_API", "MANUAL_DATA", "NOT_CURRENTLY_AVAILABLE"}
        for p in catalog:
            self.assertIn(p["source_tier"], valid_tiers)
            self.assertTrue(p["endpoint"].startswith("http"))
            self.assertIn("auth_required", p)

    # 2. Normalized Multi-Hazard Schema Backward Compatibility
    def test_normalized_event_schema(self):
        ev = NormalizedDisasterEvent(
            id="ev-test-01",
            hazard_type="CYCLONE",
            title="Bay of Bengal Severe Depression",
            state="Odisha",
            district="Puri",
            latitude=19.8,
            longitude=85.8,
            severity="HIGH",
            status="WARNING",
            description="Deep depression monitored off Puri coastline.",
            source="IMD",
            source_url="https://mausam.imd.gov.in",
            verified=True,
            is_demo=False,
            observed_at=self.now,
            retrieved_at=self.now,
            freshness="LIVE",
            basin="Coastal and Island Drainage Basins",
            event_subtype="DEEP_DEPRESSION",
            confidence="HIGH",
            official_alert=True
        )

        d = ev.to_dict()
        # Existing backward-compatible keys
        self.assertEqual(d["id"], "ev-test-01")
        self.assertEqual(d["hazard_type"], "CYCLONE")
        self.assertEqual(d["disaster_type"], "CYCLONE")
        self.assertEqual(d["state"], "Odisha")
        self.assertEqual(d["district"], "Puri")
        self.assertEqual(d["coordinates"], [19.8, 85.8])
        self.assertEqual(d["freshness"], "LIVE")

        # Phase 18A normalized keys
        self.assertEqual(d["event_id"], "ev-test-01")
        self.assertEqual(d["basin"], "Coastal and Island Drainage Basins")
        self.assertEqual(d["event_subtype"], "DEEP_DEPRESSION")
        self.assertEqual(d["confidence"], "HIGH")
        self.assertTrue(d["official_alert"])
        self.assertEqual(d["geometry"]["type"], "Point")

    # 3. Deduplication: Exact Identifiers
    def test_deduplication_exact_id(self):
        ev1 = NormalizedDisasterEvent(
            id="eq-001", hazard_type="EARTHQUAKE", title="Quake A", state="Assam", district="Golaghat",
            latitude=26.5, longitude=93.9, severity="MODERATE", status="ACTIVE", description="Quake A",
            source="USGS", source_url="https://earthquake.usgs.gov", verified=True, is_demo=False,
            observed_at=self.now, retrieved_at=self.now, freshness="LIVE"
        )
        ev2 = NormalizedDisasterEvent(
            id="eq-001", hazard_type="EARTHQUAKE", title="Quake A Duplicate", state="Assam", district="Golaghat",
            latitude=26.5, longitude=93.9, severity="MODERATE", status="ACTIVE", description="Quake A Dup",
            source="USGS", source_url="https://earthquake.usgs.gov", verified=True, is_demo=False,
            observed_at=self.now, retrieved_at=self.now, freshness="LIVE"
        )

        deduped, stats = EventDeduplicator.deduplicate([ev1, ev2])
        self.assertEqual(len(deduped), 1)
        self.assertEqual(stats["duplicates_removed"], 1)

    # 4. Deduplication: Near-Duplicate Event
    def test_deduplication_near_duplicate(self):
        ev1 = NormalizedDisasterEvent(
            id="fl-001", hazard_type="FLOOD", title="Brahmaputra Flood Advisory", state="Assam", district="Kamrup",
            latitude=26.14, longitude=91.73, severity="HIGH", status="ACTIVE", description="Water level warning",
            source="CWC", source_url="https://ffs.india-water.gov.in", verified=True, is_demo=False,
            observed_at=self.now, retrieved_at=self.now, freshness="LIVE"
        )
        # Same hazard, 5km away, 1 hour later
        ev2 = NormalizedDisasterEvent(
            id="fl-002", hazard_type="FLOOD", title="Kamrup River Rise", state="Assam", district="Kamrup",
            latitude=26.16, longitude=91.75, severity="HIGH", status="ACTIVE", description="Rising river alert",
            source="ASDMA", source_url="https://asdma.assam.gov.in", verified=True, is_demo=False,
            observed_at=self.now + timedelta(minutes=45), retrieved_at=self.now, freshness="LIVE"
        )

        deduped, stats = EventDeduplicator.deduplicate([ev1, ev2])
        self.assertEqual(len(deduped), 1)
        self.assertEqual(stats["duplicates_removed"], 1)
        # Attribution merged
        self.assertIn("CWC", deduped[0].source)
        self.assertIn("ASDMA", deduped[0].source)

    # 5. Deduplication: Different Events Not Merged
    def test_deduplication_different_events(self):
        ev1 = NormalizedDisasterEvent(
            id="fl-001", hazard_type="FLOOD", title="Assam Flood", state="Assam", district="Dhubri",
            latitude=26.0, longitude=90.0, severity="HIGH", status="ACTIVE", description="Flood in Dhubri",
            source="CWC", source_url="https://ffs.india-water.gov.in", verified=True, is_demo=False,
            observed_at=self.now, retrieved_at=self.now, freshness="LIVE"
        )
        ev2 = NormalizedDisasterEvent(
            id="cy-001", hazard_type="CYCLONE", title="Odisha Storm", state="Odisha", district="Puri",
            latitude=19.8, longitude=85.8, severity="HIGH", status="ACTIVE", description="Cyclone in Puri",
            source="IMD", source_url="https://mausam.imd.gov.in", verified=True, is_demo=False,
            observed_at=self.now, retrieved_at=self.now, freshness="LIVE"
        )

        deduped, stats = EventDeduplicator.deduplicate([ev1, ev2])
        self.assertEqual(len(deduped), 2)
        self.assertEqual(stats["duplicates_removed"], 0)

    # 6. Deduplication: Same Location Different Time
    def test_deduplication_same_location_different_time(self):
        ev1 = NormalizedDisasterEvent(
            id="eq-001", hazard_type="EARTHQUAKE", title="Tremor Day 1", state="Himachal Pradesh", district="Mandi",
            latitude=31.7, longitude=76.9, severity="LOW", status="RESOLVED", description="Day 1 tremor",
            source="USGS", source_url="https://earthquake.usgs.gov", verified=True, is_demo=False,
            observed_at=self.now - timedelta(days=2), retrieved_at=self.now, freshness="STALE"
        )
        ev2 = NormalizedDisasterEvent(
            id="eq-002", hazard_type="EARTHQUAKE", title="Tremor Day 3", state="Himachal Pradesh", district="Mandi",
            latitude=31.7, longitude=76.9, severity="MODERATE", status="ACTIVE", description="Day 3 new tremor",
            source="USGS", source_url="https://earthquake.usgs.gov", verified=True, is_demo=False,
            observed_at=self.now, retrieved_at=self.now, freshness="LIVE"
        )

        deduped, stats = EventDeduplicator.deduplicate([ev1, ev2])
        self.assertEqual(len(deduped), 2)
        self.assertEqual(stats["duplicates_removed"], 0)

    # 7. Geographic Normalization: Exactly 28 States and 8 UTs
    def test_geographic_normalization_counts(self):
        counts = geo_basin_service.get_administrative_count()
        self.assertEqual(counts["states"], 28, "India must have exactly 28 states")
        self.assertEqual(counts["union_territories"], 8, "India must have exactly 8 union territories")
        self.assertEqual(counts["total"], 36, "Total administrative entities must equal 36")

        # Verify Dadra and Nagar Haveli and Daman and Diu is unified
        dn = next((e for e in INDIAN_ADMINISTRATIVE_ENTITIES if e["id"] == "dadra-nagar-haveli-daman-diu"), None)
        self.assertIsNotNone(dn)
        self.assertEqual(dn["code"], "DN")
        self.assertEqual(dn["type"], "UNION_TERRITORY")

    # 8. Geographic Normalization: Aliases
    def test_geographic_normalization_aliases(self):
        # Legacy aliases must resolve to unified entity
        norm_dnh = geo_basin_service.normalize_location("dadra-nagar-haveli")
        self.assertIsNotNone(norm_dnh)
        self.assertEqual(norm_dnh["id"], "dadra-nagar-haveli-daman-diu")

        norm_dd = geo_basin_service.normalize_location("daman-diu")
        self.assertIsNotNone(norm_dd)
        self.assertEqual(norm_dd["id"], "dadra-nagar-haveli-daman-diu")

        # Standard state resolution
        norm_as = geo_basin_service.normalize_location("AS")
        self.assertIsNotNone(norm_as)
        self.assertEqual(norm_as["id"], "assam")

    # 9. River Basin Foundation
    def test_river_basin_foundation(self):
        basins = geo_basin_service.get_all_basins()
        self.assertGreaterEqual(len(basins), 10)

        # Assam must resolve to Brahmaputra basin
        b_assam = geo_basin_service.get_basin_for_location(state="Assam", district="Kamrup Metro")
        self.assertEqual(b_assam["basin_id"], "brahmaputra")
        self.assertTrue(b_assam["is_ml_supported"])

        # Barak valley district in Assam
        b_cachar = geo_basin_service.get_basin_for_location(state="Assam", district="Cachar")
        self.assertEqual(b_cachar["basin_id"], "barak_others")
        self.assertTrue(b_cachar["is_ml_supported"])

        # Non-Assam location (Delhi -> Ganga basin, not ML supported)
        b_delhi = geo_basin_service.get_basin_for_location(state="Delhi", district="New Delhi")
        self.assertEqual(b_delhi["basin_id"], "ganga")
        self.assertFalse(b_delhi["is_ml_supported"])

    # 10. Data Quality Gates: Valid Observation
    def test_data_quality_gates_valid(self):
        obs = RawObservation(
            source="CWC Telemetry",
            station_id="STN_DHANSIRI_01",
            station_name="Dhansirighat",
            basin="Brahmaputra",
            latitude=26.6958,
            longitude=92.2578,
            observation_time=self.now.isoformat(),
            parameter="rainfall",
            value=25.4,
            unit="mm"
        )
        is_valid, reason, rule = DataQualityGate.validate_record(obs)
        self.assertTrue(is_valid)
        self.assertIsNone(reason)

    # 11. Data Quality Gates: Rejections (Negative Rainfall, Out of Bounds, Leakage)
    def test_data_quality_gates_rejections(self):
        # Negative rainfall
        obs_neg = RawObservation(
            source="CWC", station_id="STN_01", station_name="Test", basin="Brahmaputra",
            latitude=26.5, longitude=92.0, observation_time=self.now.isoformat(),
            parameter="rainfall", value=-12.5, unit="mm"
        )
        is_valid, reason, rule = DataQualityGate.validate_record(obs_neg)
        self.assertFalse(is_valid)
        self.assertEqual(rule, "NEGATIVE_RAINFALL")

        # Impossible river stage
        obs_stage = RawObservation(
            source="CWC", station_id="STN_02", station_name="Test", basin="Ganga",
            latitude=25.0, longitude=85.0, observation_time=self.now.isoformat(),
            parameter="river_stage", value=45.0, unit="meters"
        )
        is_valid, reason, rule = DataQualityGate.validate_record(obs_stage)
        self.assertFalse(is_valid)
        self.assertEqual(rule, "PHYSICALLY_IMPOSSIBLE_STAGE")

        # Future-data leakage (obs_time after event_time)
        t_event = datetime(2026, 6, 15, 12, 0, 0, tzinfo=timezone.utc).isoformat()
        t_leak = datetime(2026, 6, 15, 18, 0, 0, tzinfo=timezone.utc).isoformat()
        obs_leak = RawObservation(
            source="CWC", station_id="STN_03", station_name="Test", basin="Brahmaputra",
            latitude=26.5, longitude=92.0, observation_time=t_leak,
            parameter="rainfall", value=15.0, unit="mm"
        )
        is_valid, reason, rule = DataQualityGate.validate_record(obs_leak, event_time=t_event)
        self.assertFalse(is_valid)
        self.assertEqual(rule, "DATA_LEAKAGE")

    # 12. Dataset Manifest: Strict Zero-Synthetic Guarantee
    def test_dataset_manifest_zero_synthetic(self):
        manifest = dataset_manifest_registry.get_manifest("assam_flood_features_v1")
        self.assertIsNotNone(manifest, "Assam dataset manifest must be registered")
        self.assertEqual(manifest.synthetic_records, 0, "MANDATORY: synthetic_records must strictly equal 0")
        self.assertEqual(manifest.row_count, 32, "Audited row count must be exactly 32")
        self.assertTrue(len(manifest.sha256) == 64, "Must contain valid 64-char SHA256 hex digest")
        self.assertTrue(manifest.is_audited)

    # 13. Model Registry: Assam Prototype Scope Guard
    def test_model_registry_integrity(self):
        model = model_registry.get_model("assam_flood_prototype_v1")
        self.assertIsNotNone(model)
        self.assertEqual(model.status, ModelStatus.PROTOTYPE)
        self.assertIn("Assam", model.geographic_scope)
        self.assertTrue(model.is_active)
        self.assertIn("not applicable outside assam", model.limitations.lower())

        # Un-trained future basin models must not be active
        godavari = model_registry.get_model("flood_godavari_v1")
        self.assertIsNotNone(godavari)
        self.assertEqual(godavari.status, ModelStatus.NOT_TRAINED)
        self.assertFalse(godavari.is_active)

    # 14. ML Scope Guard Honesty: Non-Assam Rejection
    def test_ml_scope_guard_non_assam(self):
        # Non-Assam location rejected honestly without fake prediction
        res = flood_model_service.predict(location_id="bihar", district="Patna", hazard="flood")
        self.assertEqual(res["status"], "model_scope_limited")
        self.assertIn("Assam", res["message"])
        self.assertFalse(res.get("prediction", False))

        # Assam location accepts prediction when features provided
        features = {
            "rainfall_6h": 5.0,
            "rainfall_24h": 45.0,
            "rainfall_72h": 120.0,
            "rainfall_168h": 250.0,
            "river_level_relative": 1.5,
            "river_rise_6h": 0.1,
            "river_rise_24h": 0.4,
            "river_percentile_level": 0.85,
            "month": 7,
            "day_of_year_sin": -0.1,
            "day_of_year_cos": -0.99,
            "latitude": 26.69,
            "longitude": 92.25
        }
        res_assam = flood_model_service.predict(location_id="assam", district="Udalguri", features=features)
        self.assertEqual(res_assam["status"], "success")
        self.assertTrue(res_assam["is_prototype"])

    # 15. REST API: /api/basins
    def test_api_basins_endpoint(self):
        response = self.client.get("/api/basins")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("basins", data)
        self.assertGreaterEqual(data["count"], 10)
        self.assertIn("disclaimer", data)

        # Filter by state
        resp_filtered = self.client.get("/api/basins?state=Assam")
        self.assertEqual(resp_filtered.status_code, 200)
        data_filtered = resp_filtered.json()
        basin_names = [b["basin_name"] for b in data_filtered["basins"]]
        self.assertTrue(any("Brahmaputra" in name for name in basin_names))

    # 16. REST API: /api/models
    def test_api_models_endpoint(self):
        response = self.client.get("/api/models")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("models", data)
        model_ids = [m["model_id"] for m in data["models"]]
        self.assertIn("assam_flood_prototype_v1", model_ids)

        # Detail endpoint
        resp_detail = self.client.get("/api/models/assam_flood_prototype_v1")
        self.assertEqual(resp_detail.status_code, 200)
        detail = resp_detail.json()
        self.assertEqual(detail["status"], "PROTOTYPE")
        self.assertEqual(detail["training_dataset"], "assam_flood_features_v1")

    # 17. REST API: /api/datasets/manifests
    def test_api_dataset_manifests_endpoint(self):
        response = self.client.get("/api/datasets/manifests")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("manifests", data)
        manifests = data["manifests"]
        self.assertGreaterEqual(len(manifests), 1)
        assam_m = next((m for m in manifests if m["dataset_id"] == "assam_flood_features_v1"), None)
        self.assertIsNotNone(assam_m)
        self.assertEqual(assam_m["synthetic_records"], 0)
        self.assertEqual(assam_m["row_count"], 32)

    # 18. REST API: /api/disasters/providers and /api/disasters/status
    def test_api_disasters_telemetry_endpoints(self):
        resp_prov = self.client.get("/api/disasters/providers")
        self.assertEqual(resp_prov.status_code, 200)
        data_prov = resp_prov.json()
        self.assertIn("providers", data_prov)
        self.assertIn("health", data_prov)

        resp_status = self.client.get("/api/disasters/status")
        self.assertEqual(resp_status.status_code, 200)
        data_status = resp_status.json()
        self.assertEqual(data_status["operational_status"], "OPERATIONAL")
        self.assertIn("freshness_breakdown", data_status)
        self.assertIn("deduplication_stats", data_status)


if __name__ == "__main__":
    unittest.main()
