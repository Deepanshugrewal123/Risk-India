"""
RISK // INDIA — PHASE 28 TEST SUITE
===================================
Automated verification for National Live Disaster Intelligence, Freshness & Unified Risk Presentation.
Validates:
- 36 Administrative Entities (28 States + 8 Union Territories)
- 6 Hazards (FLOOD, EARTHQUAKE, CYCLONE, HEATWAVE, LANDSLIDE, SEVERE_WEATHER)
- Decoupled Freshness and Risk Severity (HIGH + STALE != LIVE)
- Offline and Cached Fallback Isolation
- ML Scope Guard (assam_flood_prototype_v1 only in Assam; zero ML outside Assam)
- Data Provenance and Zero Synthetic Data Guarantee
- REST Endpoints (/api/national-risk, /freshness, /providers, /{region}, /{region}/{hazard})
- Model and Dataset SHA-256 Hash Immutability
- Emergency Resources Integration
"""

import unittest
import hashlib
import sys
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient

from app.main import app
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


class TestPhase28NationalLiveIntelligence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.expected_model_hash = "0e05bcdf9022fa40897c12270811bc35234a7de877f32e7034e5b446c2dccccf"
        cls.expected_dataset_hash = "88b32f35b64ef14d7201463563159529c317982063796dff448d39f45073b080"

    def test_01_national_summary_returns_all_36_entities(self):
        """Test that national summary contains exactly 28 States and 8 Union Territories."""
        response = self.client.get("/api/national-risk")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["total_administrative_entities"], 36)
        self.assertEqual(data["states_covered"], 28)
        self.assertEqual(data["union_territories_covered"], 8)
        self.assertEqual(len(data["regions"]), 36)

        # Check names match authoritative catalog
        region_names = {r["region"]["name"] for r in data["regions"]}
        catalog_names = {e["name"] for e in INDIAN_ADMINISTRATIVE_ENTITIES}
        self.assertEqual(region_names, catalog_names)

    def test_02_six_hazards_supported_across_all_regions(self):
        """Test that all 6 core hazards are represented for each entity."""
        response = self.client.get("/api/national-risk")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        for region_data in data["regions"]:
            hazards = region_data.get("hazards", {})
            self.assertEqual(set(hazards.keys()), set(SUPPORTED_HAZARDS))
            for h in SUPPORTED_HAZARDS:
                self.assertIn("risk_score", hazards[h])
                self.assertIn("risk_level", hazards[h])
                self.assertIn("freshness", hazards[h])
                self.assertIn("provenance", hazards[h])

    def test_03_deterministic_freshness_classification_states(self):
        """Test freshness engine maps observation ages deterministically."""
        now = datetime.now(timezone.utc)

        # 1. Under 1 hour => OFFICIAL_LIVE
        rec_live = freshness_engine.classify_freshness(
            observed_at=(now - timedelta(minutes=25)).isoformat(),
            is_cached=False
        )
        self.assertEqual(rec_live.freshness_state, FreshnessClassification.OFFICIAL_LIVE.value)

        # 2. 1 to 24 hours => OFFICIAL_RECENT
        rec_recent = freshness_engine.classify_freshness(
            observed_at=(now - timedelta(hours=5)).isoformat(),
            is_cached=False
        )
        self.assertEqual(rec_recent.freshness_state, FreshnessClassification.OFFICIAL_RECENT.value)

        # 3. Over 24 hours => STALE
        rec_stale = freshness_engine.classify_freshness(
            observed_at=(now - timedelta(hours=36)).isoformat(),
            is_cached=False
        )
        self.assertEqual(rec_stale.freshness_state, FreshnessClassification.STALE.value)

        # 4. Regional baseline => REGIONAL_BASELINE
        rec_base = freshness_engine.classify_freshness(observed_at=None, is_baseline=True)
        self.assertEqual(rec_base.freshness_state, FreshnessClassification.REGIONAL_BASELINE.value)

    def test_04_freshness_independent_of_risk_severity(self):
        """Verify high risk with stale observation is strictly HIGH RISK / STALE, never LIVE."""
        old_timestamp = (datetime.now(timezone.utc) - timedelta(hours=48)).isoformat()
        rec = freshness_engine.classify_freshness(
            observed_at=old_timestamp,
            is_cached=False,
            source="Test Agency"
        )
        # Freshness classification is STALE regardless of any hypothetical CRITICAL or HIGH severity
        self.assertEqual(rec.freshness_state, FreshnessClassification.STALE.value)
        self.assertNotEqual(rec.freshness_state, FreshnessClassification.OFFICIAL_LIVE.value)

    def test_05_cached_data_never_classified_as_live(self):
        """Verify cached telemetry is labeled CACHED or STALE, never OFFICIAL_LIVE."""
        now = datetime.now(timezone.utc)
        rec_cached = freshness_engine.classify_freshness(
            observed_at=(now - timedelta(minutes=5)).isoformat(),
            is_cached=True,
            source="Local DB Cache"
        )
        self.assertEqual(rec_cached.freshness_state, FreshnessClassification.CACHED.value)
        self.assertNotEqual(rec_cached.freshness_state, FreshnessClassification.OFFICIAL_LIVE.value)

    def test_06_regional_baseline_never_labeled_as_ml(self):
        """Verify non-Assam regions return empirical_ml.available == False and status == NOT_AVAILABLE."""
        for state in ["Bihar", "Odisha", "Maharashtra", "Gujarat", "Kerala", "Delhi"]:
            resp = self.client.get(f"/api/national-risk/{state}")
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertFalse(data["empirical_ml"]["available"])
            self.assertEqual(data["empirical_ml"]["status"], "NOT_AVAILABLE")
            self.assertEqual(data["empirical_ml"]["model_id"], "NONE")

    def test_07_ml_scope_guard_strictly_assam(self):
        """Verify Assam has active empirical ML and assam_flood_prototype_v1."""
        resp = self.client.get("/api/national-risk/Assam")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["empirical_ml"]["available"])
        self.assertEqual(data["empirical_ml"]["status"], "APPROVED")
        self.assertEqual(data["empirical_ml"]["model_id"], "assam_flood_prototype_v1")

    def test_08_ml_scope_guard_non_assam_explanation(self):
        """Verify non-Assam regions include explicit explanation regarding ML absence."""
        resp = self.client.get("/api/national-risk/Bihar")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("Empirical ML prediction is not currently validated for this region", data["empirical_ml"]["message"])
        self.assertIn("Trained ML is strictly prohibited outside the approved Assam corridor", data["empirical_ml"]["scope_guard"])

    def test_09_zero_synthetic_data_guarantee(self):
        """Verify synthetic_records == 0 across all endpoints."""
        endpoints = [
            "/api/national-risk",
            "/api/national-risk/freshness",
            "/api/national-risk/Assam",
            "/api/national-risk/Bihar",
            "/api/national-risk/Assam/FLOOD"
        ]
        for ep in endpoints:
            resp = self.client.get(ep)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json().get("synthetic_records"), 0, f"Endpoint {ep} violated zero-synthetic rule")

    def test_10_provenance_engine_metadata_fields(self):
        """Verify provenance records contain all mandatory audit fields."""
        record = provenance_engine.build_provenance(
            provider="CWC_CENTRAL_WATER_COMMISSION",
            source_type="HYDROLOGICAL_GAUGE",
            source_record_id="CWC-TEZPUR-01",
            observation_timestamp=datetime.now(timezone.utc).isoformat(),
            freshness="OFFICIAL_LIVE",
            source_url="https://cwc.gov.in"
        )
        d = record.to_dict()
        self.assertIn("provider", d)
        self.assertIn("source_type", d)
        self.assertIn("source_record_id", d)
        self.assertIn("observation_timestamp", d)
        self.assertIn("retrieval_timestamp", d)
        self.assertIn("freshness", d)
        self.assertIn("fallback_status", d)
        self.assertIn("data_license", d)

    def test_11_provider_health_isolation(self):
        """Verify provider health report reflects operational state without cross-provider degradation."""
        resp = self.client.get("/api/national-risk/providers")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["circuit_breaker_enabled"])
        self.assertIn("providers", data)
        self.assertIn("health", data)
        self.assertIn("isolation_policy", data)

    def test_12_circuit_breaker_transition(self):
        """Verify circuit breaker record structure and thresholds."""
        from app.services.disaster_provider import CircuitBreaker, CircuitState
        cb = CircuitBreaker(failure_threshold=3, cooldown_seconds=10.0)
        self.assertEqual(cb.state, CircuitState.CLOSED)
        self.assertTrue(cb.can_execute())

        # Record 3 failures
        cb.record_failure("Upstream timeout 1")
        cb.record_failure("Upstream timeout 2")
        cb.record_failure("Upstream timeout 3")
        self.assertEqual(cb.state, CircuitState.OPEN)
        self.assertFalse(cb.can_execute())

        # Successful call resets failure count
        cb.record_success()
        self.assertEqual(cb.state, CircuitState.CLOSED)
        self.assertEqual(cb.failure_count, 0)
        self.assertTrue(cb.can_execute())

    def test_13_get_state_risk_valid_state(self):
        """Verify querying valid state returns complete profile with emergency resources."""
        resp = self.client.get("/api/national-risk/Karnataka")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["region"]["name"], "Karnataka")
        self.assertEqual(data["region"]["type"], "STATE")
        self.assertIn("emergency_resources", data)
        self.assertGreater(len(data["emergency_resources"]), 0)
        self.assertIn("hazards", data)
        self.assertIn("regional_baseline", data)

    def test_14_get_state_risk_valid_ut(self):
        """Verify querying valid Union Territory returns correct administrative type."""
        for ut in ["Delhi", "Ladakh", "Puducherry", "Chandigarh"]:
            resp = self.client.get(f"/api/national-risk/{ut}")
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertEqual(data["region"]["type"], "UNION_TERRITORY")

    def test_15_get_state_risk_invalid_region(self):
        """Verify querying nonexistent region returns 404."""
        resp = self.client.get("/api/national-risk/Atlantis")
        self.assertEqual(resp.status_code, 404)

    def test_16_get_hazard_risk_valid(self):
        """Verify hazard-specific endpoint returns 200 for valid hazard."""
        resp = self.client.get("/api/national-risk/Assam/FLOOD")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["hazard_type"], "FLOOD")
        self.assertTrue(data["empirical_ml"]["available"])

    def test_17_get_hazard_risk_unsupported(self):
        """Verify querying unsupported hazard returns 400."""
        resp = self.client.get("/api/national-risk/Assam/VOLCANO")
        self.assertEqual(resp.status_code, 400)

    def test_18_freshness_endpoint(self):
        """Verify freshness breakdown endpoint returns audit distribution."""
        resp = self.client.get("/api/national-risk/freshness")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("freshness_distribution", data)
        dist = data["freshness_distribution"]
        self.assertIn("OFFICIAL_LIVE", dist)
        self.assertIn("REGIONAL_BASELINE", dist)
        self.assertEqual(dist["REGIONAL_BASELINE"], 36)

    def test_19_providers_endpoint(self):
        """Verify providers endpoint lists provider catalog with circuit breaker state."""
        resp = self.client.get("/api/national-risk/providers")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreater(data["count"], 0)

    def test_20_assam_model_and_dataset_integrity(self):
        """Verify assam_flood_prototype_v1 and empirical dataset remain byte-for-byte unmodified."""
        model_path = os.path.join("ml", "flood", "artifacts", "model.joblib")
        dataset_path = os.path.join("datasets", "processed", "flood_assam", "flood_features.csv")

        self.assertTrue(os.path.exists(model_path), "Model artifact missing")
        self.assertTrue(os.path.exists(dataset_path), "Empirical dataset missing")

        with open(model_path, "rb") as f:
            m_hash = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(m_hash, self.expected_model_hash, "Model hash changed! Retraining is prohibited.")

        with open(dataset_path, "rb") as f:
            d_hash = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(d_hash, self.expected_dataset_hash, "Assam dataset modified! Empirical data must remain frozen.")

    def test_21_explanation_engine_rationale(self):
        """Verify explain_state_risk outputs clear, non-cryptic rationale."""
        explanation = risk_explanation_engine.explain_state_risk(
            state_name="Assam",
            primary_hazard="FLOOD",
            overall_risk_level="HIGH",
            has_active_alert=True,
            is_assam=True,
            active_alert_count=2
        )
        self.assertIn("Assam", explanation)
        self.assertIn("FLOOD", explanation)
        self.assertIn("active official warning", explanation.lower())

    def test_22_emergency_resources_integration(self):
        """Verify emergency resources in state profile have valid contact info and verified status."""
        resp = self.client.get("/api/national-risk/Assam")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        resources = data.get("emergency_resources", [])
        self.assertGreater(len(resources), 0)
        for r in resources:
            self.assertEqual(r.get("verification_status"), "VERIFIED")
            self.assertTrue(r.get("phone") or r.get("website"))


if __name__ == "__main__":
    unittest.main()
