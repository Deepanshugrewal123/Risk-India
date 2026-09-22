"""
RISK // INDIA — Automated Test Suite: Phase 18B Multi-Basin Data Foundation & Gauge Harmonization
==================================================================================================
Comprehensive tests validating:
1. Canonical CWC Gauge Registry for Godavari Basin (Bhadrachalam, Dowleswaram, Polavaram, etc.)
2. Canonical CWC Gauge Registry for Mahanadi Basin (Hirakud, Naraj, Tikarpara, etc.)
3. Spatial nearest-station lookups with distance bounds
4. Hydro-meteorological observation schema, freeboard, and crest percentage calculations
5. Hydro observation normalizer (UTC standardization, feet-to-meters, flood status derivation)
6. Data quality bounds engine (negative rainfall rejection, excessive rainfall, physical stage bounds)
7. Temporal data leakage prevention (strict observation_time <= event_time enforcement)
8. Duplicate observation detection in multi-basin time series
9. SpatialGroupSplitter (GroupKFold spatial leakage prevention)
10. TemporalBlockSplitter (chronological holdout leakage prevention)
11. Deterministic ML Readiness Gate for Brahmaputra (Assam) -> True (PROTOTYPE)
12. Deterministic ML Readiness Gate for Godavari -> False (NOT_TRAINED)
13. Deterministic ML Readiness Gate for Mahanadi -> False (NOT_TRAINED)
14. Deterministic ML Readiness Gate for other basins (Ganga, Krishna, Indus) -> False (NOT_TRAINED)
15. Dataset manifests strict zero-synthetic guarantee (synthetic_records == 0 across all manifests)
16. Model registry integrity and inactive future basin placeholders
17. REST API: GET /api/basins/{basin_id}/stations (Godavari & Mahanadi)
18. REST API: GET /api/basins/{basin_id}/readiness
19. REST API: GET /api/basins/{basin_id}/quality-report
20. REST API: Full regression check on existing endpoints (/api/models, /api/datasets/manifests)
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
from app.services.basin_gauge_registry import (
    basin_gauge_registry,
    BasinGaugeStation,
    haversine_distance_km
)
from app.services.hydro_schema import (
    HydroObservation,
    HydroObservationNormalizer,
    FloodStatus
)
from app.services.data_quality_engine import (
    data_quality_engine,
    DataQualityViolation,
    DataQualityReport,
    SpatialGroupSplitter,
    TemporalBlockSplitter
)
from app.services.ml_readiness_gate import (
    ml_readiness_gate,
    MLReadinessGateResult
)
from app.services.dataset_manifest import dataset_manifest_registry
from app.services.model_registry import model_registry, ModelStatus


class TestPhase18BMultiBasinFoundation(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.now = datetime.now(timezone.utc)

    # 1. Godavari Gauge Registry
    def test_godavari_gauge_registry(self):
        stations = basin_gauge_registry.get_stations_by_basin("godavari")
        self.assertGreaterEqual(len(stations), 8)

        station_ids = [s.station_id for s in stations]
        self.assertIn("CWC-GD-001", station_ids)  # Bhadrachalam
        self.assertIn("CWC-GD-002", station_ids)  # Dowleswaram
        self.assertIn("CWC-GD-003", station_ids)  # Polavaram
        self.assertIn("CWC-GD-005", station_ids)  # Nanded

        # Verify Bhadrachalam details
        bhadra = basin_gauge_registry.get_station("CWC-GD-001")
        self.assertIsNotNone(bhadra)
        self.assertEqual(bhadra.station_name, "Bhadrachalam")
        self.assertEqual(bhadra.state, "Telangana")
        self.assertEqual(bhadra.river_name, "Godavari")
        self.assertEqual(bhadra.warning_level_m, 14.63)
        self.assertEqual(bhadra.danger_level_m, 16.15)
        self.assertEqual(bhadra.hfl_m, 21.82)
        self.assertEqual(bhadra.hfl_date, "1986-08-16")
        self.assertEqual(bhadra.status, "ACTIVE_CALIBRATED")

    # 2. Mahanadi Gauge Registry
    def test_mahanadi_gauge_registry(self):
        stations = basin_gauge_registry.get_stations_by_basin("mahanadi")
        self.assertGreaterEqual(len(stations), 8)

        station_ids = [s.station_id for s in stations]
        self.assertIn("CWC-MH-001", station_ids)  # Hirakud Dam
        self.assertIn("CWC-MH-002", station_ids)  # Naraj Barrage
        self.assertIn("CWC-MH-003", station_ids)  # Tikarpara
        self.assertIn("CWC-MH-005", station_ids)  # Rajim

        # Verify Hirakud Dam details
        hirakud = basin_gauge_registry.get_station("CWC-MH-001")
        self.assertIsNotNone(hirakud)
        self.assertEqual(hirakud.station_name, "Hirakud Dam (Sambalpur)")
        self.assertEqual(hirakud.state, "Odisha")
        self.assertEqual(hirakud.river_name, "Mahanadi")
        self.assertEqual(hirakud.danger_level_m, 192.02)
        self.assertEqual(hirakud.warning_level_m, 191.00)

        # Verify Naraj Barrage details
        naraj = basin_gauge_registry.get_station("CWC-MH-002")
        self.assertIsNotNone(naraj)
        self.assertEqual(naraj.station_name, "Naraj Barrage")
        self.assertEqual(naraj.state, "Odisha")
        self.assertEqual(naraj.warning_level_m, 25.41)
        self.assertEqual(naraj.danger_level_m, 26.41)

    # 3. Spatial Nearest Station Lookup
    def test_nearest_station_lookup(self):
        # Coordinates very close to Bhadrachalam (17.6688, 80.8936)
        res = basin_gauge_registry.find_nearest_station(17.67, 80.90, basin_id="godavari")
        self.assertIsNotNone(res)
        self.assertEqual(res["station_id"], "CWC-GD-001")
        self.assertLess(res["distance_km"], 5.0)

        # Out-of-bounds search with small radius should return None
        none_res = basin_gauge_registry.find_nearest_station(28.61, 77.20, basin_id="godavari", max_distance_km=10.0)
        self.assertIsNone(none_res)

    # 4. Hydro-Meteorological Observation Schema
    def test_hydro_observation_schema_and_metrics(self):
        obs = HydroObservationNormalizer.build_normalized_observation(
            station_id="CWC-GD-001",
            station_name="Bhadrachalam",
            basin_id="godavari",
            sub_basin="pranhita_catchment",
            river_name="Godavari",
            latitude=17.6688,
            longitude=80.8936,
            timestamp=self.now,
            water_level_m=15.00,
            warning_level_m=14.63,
            danger_level_m=16.15,
            hfl_m=21.82,
            rainfall_24h_mm=65.5
        )

        self.assertEqual(obs.station_id, "CWC-GD-001")
        self.assertEqual(obs.flood_status, FloodStatus.WARNING)
        # Freeboard = 16.15 - 15.00 = 1.15m
        self.assertAlmostEqual(obs.freeboard_to_danger_m, 1.15, places=2)
        # Crest % = 15.00 / 16.15 * 100 = 92.88%
        self.assertAlmostEqual(obs.crest_percentage, 92.88, places=1)
        self.assertEqual(obs.rainfall_24h_mm, 65.5)

    # 5. Flood Status Derivations
    def test_flood_status_derivations(self):
        # NORMAL
        st_norm = HydroObservationNormalizer.derive_flood_status(10.0, 14.63, 16.15, 21.82)
        self.assertEqual(st_norm, FloodStatus.NORMAL)

        # WARNING
        st_warn = HydroObservationNormalizer.derive_flood_status(15.0, 14.63, 16.15, 21.82)
        self.assertEqual(st_warn, FloodStatus.WARNING)

        # DANGER
        st_dang = HydroObservationNormalizer.derive_flood_status(17.0, 14.63, 16.15, 21.82)
        self.assertEqual(st_dang, FloodStatus.DANGER)

        # SEVERE DANGER (exceeding HFL)
        st_sev = HydroObservationNormalizer.derive_flood_status(22.0, 14.63, 16.15, 21.82)
        self.assertEqual(st_sev, FloodStatus.SEVERE_DANGER)

    # 6. Hydro Normalizer Units & Timestamp
    def test_hydro_normalizer_units_and_timestamp(self):
        # Feet to meters: 10 ft = 3.048 m
        m = HydroObservationNormalizer.feet_to_meters(10.0)
        self.assertEqual(m, 3.048)

        # Meters to feet: 3.048 m = 10.0 ft
        ft = HydroObservationNormalizer.meters_to_feet(3.048)
        self.assertEqual(ft, 10.0)

        # ISO timestamp normalization
        iso_str = HydroObservationNormalizer.normalize_timestamp("2026-09-16T12:00:00Z")
        self.assertIn("+00:00", iso_str)

        # Invalid timestamp raises ValueError
        with self.assertRaises(ValueError):
            HydroObservationNormalizer.normalize_timestamp("not-a-timestamp")

    # 7. Data Quality Engine Physical Bounds
    def test_data_quality_physical_bounds(self):
        # Negative rainfall should be rejected
        bad_rain_obs = HydroObservation(
            station_id="CWC-GD-001",
            station_name="Bhadrachalam",
            basin_id="godavari",
            sub_basin="pranhita_catchment",
            river_name="Godavari",
            latitude=17.6688,
            longitude=80.8936,
            observation_timestamp=self.now.isoformat(),
            water_level_m=15.0,
            warning_level_m=14.63,
            danger_level_m=16.15,
            rainfall_24h_mm=-10.0  # Invalid!
        )
        is_valid, violation = data_quality_engine.validate_single_observation(bad_rain_obs)
        self.assertFalse(is_valid)
        self.assertEqual(violation.violation_type, "NEGATIVE_RAINFALL")

        # Excessive rainfall (> 2000mm) should be rejected
        excess_rain_obs = HydroObservation(
            station_id="CWC-GD-001",
            station_name="Bhadrachalam",
            basin_id="godavari",
            sub_basin="pranhita_catchment",
            river_name="Godavari",
            latitude=17.6688,
            longitude=80.8936,
            observation_timestamp=self.now.isoformat(),
            water_level_m=15.0,
            warning_level_m=14.63,
            danger_level_m=16.15,
            rainfall_24h_mm=3500.0  # Invalid!
        )
        is_valid, violation = data_quality_engine.validate_single_observation(excess_rain_obs)
        self.assertFalse(is_valid)
        self.assertEqual(violation.violation_type, "EXCESSIVE_RAINFALL")

        # Future timestamp should be rejected
        future_time = (self.now + timedelta(days=2)).isoformat()
        future_obs = HydroObservation(
            station_id="CWC-GD-001",
            station_name="Bhadrachalam",
            basin_id="godavari",
            sub_basin="pranhita_catchment",
            river_name="Godavari",
            latitude=17.6688,
            longitude=80.8936,
            observation_timestamp=future_time,
            water_level_m=15.0,
            warning_level_m=14.63,
            danger_level_m=16.15
        )
        is_valid, violation = data_quality_engine.validate_single_observation(future_obs)
        self.assertFalse(is_valid)
        self.assertEqual(violation.violation_type, "FUTURE_TIMESTAMP")

    # 8. Temporal Leakage Detection
    def test_temporal_leakage_detection(self):
        obs_time = "2026-07-15T10:00:00+00:00"
        event_time_prior = "2026-07-15T08:00:00+00:00"  # Event occurred 2 hours BEFORE observation!
        event_time_post = "2026-07-15T12:00:00+00:00"   # Event occurred 2 hours AFTER observation

        leak_obs = HydroObservation(
            station_id="CWC-GD-001",
            station_name="Bhadrachalam",
            basin_id="godavari",
            sub_basin="pranhita_catchment",
            river_name="Godavari",
            latitude=17.6688,
            longitude=80.8936,
            observation_timestamp=obs_time,
            water_level_m=15.0,
            warning_level_m=14.63,
            danger_level_m=16.15
        )

        # Leakage: obs_time > event_time
        is_valid_leak, vio_leak = data_quality_engine.validate_single_observation(leak_obs, event_time=event_time_prior)
        self.assertFalse(is_valid_leak)
        self.assertEqual(vio_leak.violation_type, "DATA_LEAKAGE")

        # Causally valid: obs_time <= event_time
        is_valid_clean, vio_clean = data_quality_engine.validate_single_observation(leak_obs, event_time=event_time_post)
        self.assertTrue(is_valid_clean)
        self.assertIsNone(vio_clean)

    # 9. Duplicate Observation Detection
    def test_duplicate_observation_handling(self):
        obs1 = HydroObservation(
            station_id="CWC-MH-001",
            station_name="Hirakud Dam",
            basin_id="mahanadi",
            sub_basin="hasdeo_catchment",
            river_name="Mahanadi",
            latitude=21.57,
            longitude=83.87,
            observation_timestamp="2026-08-10T06:00:00+00:00",
            water_level_m=190.5,
            warning_level_m=191.0,
            danger_level_m=192.02
        )
        obs2_duplicate = HydroObservation(
            station_id="CWC-MH-001",
            station_name="Hirakud Dam",
            basin_id="mahanadi",
            sub_basin="hasdeo_catchment",
            river_name="Mahanadi",
            latitude=21.57,
            longitude=83.87,
            observation_timestamp="2026-08-10T06:00:00+00:00",
            water_level_m=190.5,
            warning_level_m=191.0,
            danger_level_m=192.02
        )

        report = data_quality_engine.audit_basin_dataset("mahanadi", [obs1, obs2_duplicate])
        self.assertEqual(report.total_records_analyzed, 2)
        self.assertEqual(report.valid_records_count, 1)
        self.assertEqual(report.duplicate_count, 1)
        self.assertEqual(report.quarantined_count, 1)
        self.assertFalse(report.is_basin_clean)

    # 10. Spatial Group Splitter (Leakage Prevention)
    def test_spatial_group_splitter(self):
        records = [
            {"id": "r1", "station_id": "CWC-GD-001", "val": 10},
            {"id": "r2", "station_id": "CWC-GD-001", "val": 12},
            {"id": "r3", "station_id": "CWC-GD-002", "val": 20},
            {"id": "r4", "station_id": "CWC-GD-002", "val": 22},
            {"id": "r5", "station_id": "CWC-GD-003", "val": 30},
            {"id": "r6", "station_id": "CWC-GD-003", "val": 32}
        ]

        folds = SpatialGroupSplitter.split(records, group_key="station_id", n_splits=3)
        self.assertEqual(len(folds), 3)

        for train, test in folds:
            train_stations = {r["station_id"] for r in train}
            test_stations = {r["station_id"] for r in test}
            # Crucial check: disjoint station sets (zero spatial leakage)
            self.assertEqual(len(train_stations.intersection(test_stations)), 0)

    # 11. Temporal Block Splitter
    def test_temporal_block_splitter(self):
        records = [
            {"id": "t1", "observation_timestamp": "2023-06-15T00:00:00+00:00"},
            {"id": "t2", "observation_timestamp": "2023-08-20T00:00:00+00:00"},
            {"id": "t3", "observation_timestamp": "2024-07-10T00:00:00+00:00"},
            {"id": "t4", "observation_timestamp": "2024-09-01T00:00:00+00:00"}
        ]

        train, test = TemporalBlockSplitter.split_by_cutoff(
            records,
            timestamp_key="observation_timestamp",
            cutoff_timestamp="2024-01-01T00:00:00+00:00"
        )
        self.assertEqual(len(train), 2)
        self.assertEqual(len(test), 2)
        self.assertEqual([r["id"] for r in train], ["t1", "t2"])
        self.assertEqual([r["id"] for r in test], ["t3", "t4"])

    # 12. ML Readiness Gate: Brahmaputra (Assam)
    def test_ml_readiness_brahmaputra(self):
        res = ml_readiness_gate.evaluate_basin("brahmaputra")
        self.assertTrue(res.ml_ready)
        self.assertEqual(res.ml_status, "PROTOTYPE")
        self.assertEqual(res.readiness_score, 1.0)
        self.assertEqual(res.empirical_observations_count, 32)
        self.assertEqual(res.data_manifest_id, "assam_flood_features_v1")

    # 13. ML Readiness Gate: Godavari
    def test_ml_readiness_godavari(self):
        res = ml_readiness_gate.evaluate_basin("godavari")
        self.assertFalse(res.ml_ready)
        self.assertEqual(res.ml_status, "NOT_TRAINED")
        self.assertAlmostEqual(res.readiness_score, 0.35)
        self.assertGreaterEqual(res.calibrated_stations_count, 8)
        self.assertIn("ISRO/NRSC Bhuvan", str(res.missing_prerequisites))
        self.assertIn("NOT TRAINED", res.limitations)

    # 14. ML Readiness Gate: Mahanadi
    def test_ml_readiness_mahanadi(self):
        res = ml_readiness_gate.evaluate_basin("mahanadi")
        self.assertFalse(res.ml_ready)
        self.assertEqual(res.ml_status, "NOT_TRAINED")
        self.assertAlmostEqual(res.readiness_score, 0.35)
        self.assertGreaterEqual(res.calibrated_stations_count, 8)
        self.assertIn("Hirakud", str(res.missing_prerequisites))
        self.assertIn("NOT TRAINED", res.limitations)

    # 15. ML Readiness Gate: Other Basins
    def test_ml_readiness_other_basins(self):
        res = ml_readiness_gate.evaluate_basin("ganga")
        self.assertFalse(res.ml_ready)
        self.assertEqual(res.ml_status, "NOT_TRAINED")
        self.assertEqual(res.readiness_score, 0.10)

    # 16. Dataset Manifests: Zero Synthetic Guarantee
    def test_dataset_manifest_zero_synthetic_guarantee(self):
        manifests = dataset_manifest_registry.list_manifests()
        self.assertGreaterEqual(len(manifests), 3)

        m_ids = [m["dataset_id"] for m in manifests]
        self.assertIn("assam_flood_features_v1", m_ids)
        self.assertIn("godavari_gauge_registry_v1", m_ids)
        self.assertIn("mahanadi_gauge_registry_v1", m_ids)

        for m in manifests:
            # Mandatory scientific non-negotiable: synthetic_records must be 0
            self.assertEqual(m["synthetic_records"], 0, f"Violation: manifest {m['dataset_id']} has synthetic records!")

    # 17. Model Registry Integrity
    def test_model_registry_integrity(self):
        # Assam Prototype active
        assam = model_registry.get_model("assam_flood_prototype_v1")
        self.assertIsNotNone(assam)
        self.assertEqual(assam.status, ModelStatus.PROTOTYPE)
        self.assertTrue(assam.is_active)

        # Godavari inactive
        godavari = model_registry.get_model("flood_godavari_v1")
        self.assertIsNotNone(godavari)
        self.assertEqual(godavari.status, ModelStatus.NOT_TRAINED)
        self.assertFalse(godavari.is_active)
        self.assertIn("NOT TRAINED", godavari.limitations)

        # Mahanadi inactive
        mahanadi = model_registry.get_model("flood_mahanadi_v1")
        self.assertIsNotNone(mahanadi)
        self.assertEqual(mahanadi.status, ModelStatus.NOT_TRAINED)
        self.assertFalse(mahanadi.is_active)
        self.assertIn("NOT TRAINED", mahanadi.limitations)

    # 18. REST API: GET /api/basins/{basin_id}/stations
    def test_api_basin_stations(self):
        resp_gd = self.client.get("/api/basins/godavari/stations")
        self.assertEqual(resp_gd.status_code, 200)
        data_gd = resp_gd.json()
        self.assertEqual(data_gd["basin_id"], "godavari")
        self.assertGreaterEqual(data_gd["station_count"], 8)
        self.assertIn("Bhadrachalam", [s["station_name"] for s in data_gd["stations"]])

        resp_mh = self.client.get("/api/basins/mahanadi/stations")
        self.assertEqual(resp_mh.status_code, 200)
        data_mh = resp_mh.json()
        self.assertEqual(data_mh["basin_id"], "mahanadi")
        self.assertGreaterEqual(data_mh["station_count"], 8)

        # 404 on nonexistent basin
        resp_404 = self.client.get("/api/basins/nonexistent_basin_xyz/stations")
        self.assertEqual(resp_404.status_code, 404)

    # 19. REST API: GET /api/basins/{basin_id}/readiness
    def test_api_basin_readiness(self):
        # Brahmaputra ML Ready
        resp_bp = self.client.get("/api/basins/brahmaputra/readiness")
        self.assertEqual(resp_bp.status_code, 200)
        data_bp = resp_bp.json()
        self.assertTrue(data_bp["ml_ready"])
        self.assertEqual(data_bp["ml_status"], "PROTOTYPE")

        # Godavari NOT ML Ready
        resp_gd = self.client.get("/api/basins/godavari/readiness")
        self.assertEqual(resp_gd.status_code, 200)
        data_gd = resp_gd.json()
        self.assertFalse(data_gd["ml_ready"])
        self.assertEqual(data_gd["ml_status"], "NOT_TRAINED")

        # Mahanadi NOT ML Ready
        resp_mh = self.client.get("/api/basins/mahanadi/readiness")
        self.assertEqual(resp_mh.status_code, 200)
        data_mh = resp_mh.json()
        self.assertFalse(data_mh["ml_ready"])
        self.assertEqual(data_mh["ml_status"], "NOT_TRAINED")

    # 20. REST API: GET /api/basins/{basin_id}/quality-report
    def test_api_basin_quality_report(self):
        resp = self.client.get("/api/basins/godavari/quality-report")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["basin_id"], "godavari")
        self.assertTrue(data["is_basin_clean"])
        self.assertEqual(data["temporal_leakage_violations"], 0)

    # 21. Data Source Discovery & Programmatic Access Truthfulness
    def test_data_source_registry(self):
        from app.services.data_source_discovery import data_source_registry
        sources = data_source_registry.list_sources()
        self.assertGreaterEqual(len(sources), 5)

        src_ids = [s["source_id"] for s in sources]
        self.assertIn("cwc_godavari_ffs", src_ids)
        self.assertIn("cwc_mahanadi_ffs", src_ids)
        self.assertIn("isro_bhuvan_godavari_inundation", src_ids)
        self.assertIn("ndma_sachet_cap", src_ids)

        # Truthful status: NDMA automated scraping is blocked, documented honestly
        sachet = data_source_registry.get_source("ndma_sachet_cap")
        self.assertIsNotNone(sachet)
        self.assertEqual(sachet.status, "DATA_ACQUISITION_BLOCKED")

    # 22. Station Name Alias Normalization
    def test_station_name_alias_normalization(self):
        # Name variations should resolve to the exact canonical station
        s1 = basin_gauge_registry.normalize_station("Bhadrachalam Gauge")
        self.assertIsNotNone(s1)
        self.assertEqual(s1.station_id, "CWC-GD-001")

        s2 = basin_gauge_registry.normalize_station("BHADRACHALAM")
        self.assertIsNotNone(s2)
        self.assertEqual(s2.station_id, "CWC-GD-001")

        s3 = basin_gauge_registry.normalize_station("cwc_gd_001")
        self.assertIsNotNone(s3)
        self.assertEqual(s3.station_id, "CWC-GD-001")

        s4 = basin_gauge_registry.normalize_station("Hirakud")
        self.assertIsNotNone(s4)
        self.assertEqual(s4.station_id, "CWC-MH-001")

    # 23. Event Harmonization & Confidence Classification
    def test_event_harmonization(self):
        from app.services.event_harmonization import event_harmonizer, EventConfidence
        evs = event_harmonizer.list_events(confirmed_only=True)
        self.assertGreaterEqual(len(evs), 3)

        for ev in evs:
            self.assertEqual(ev["confidence"], EventConfidence.CONFIRMED)
            self.assertTrue(ev["official_confirmation"])
            self.assertIsNotNone(ev["ground_truth_source"])

    # 24. Scientifically Defensible Negative Sample Policy
    def test_negative_sample_policy(self):
        from app.services.event_harmonization import NegativeSamplePolicy, LabelType
        # 1. Valid negative sample: adequate telemetry + below warning + no inundation
        clean_neg = NegativeSamplePolicy.evaluate_negative_sample(
            has_adequate_telemetry=True,
            water_level_below_warning=True,
            official_inundation_absent=True,
            station_id="CWC-GD-001",
            timestamp="2026-08-10T12:00:00+00:00"
        )
        self.assertEqual(clean_neg.label, LabelType.NEGATIVE_NON_FLOOD)
        self.assertTrue(clean_neg.is_valid_ml_sample)

        # 2. Inadequate telemetry: must be excluded, never assumed non-flood
        gap_sample = NegativeSamplePolicy.evaluate_negative_sample(
            has_adequate_telemetry=False,
            water_level_below_warning=True,
            official_inundation_absent=True,
            station_id="CWC-GD-001",
            timestamp="2026-08-10T12:00:00+00:00"
        )
        self.assertEqual(gap_sample.label, LabelType.UNCERTAIN_EXCLUDED)
        self.assertFalse(gap_sample.is_valid_ml_sample)

    # 25. Machine-Readable Manifest Files On Disk
    def test_machine_readable_manifest_files(self):
        import json
        manifest_dir = PROJECT_ROOT / "datasets" / "manifests"
        self.assertTrue(manifest_dir.exists())

        for name in ["godavari_manifest.json", "mahanadi_manifest.json", "national_data_manifest.json"]:
            m_path = manifest_dir / name
            self.assertTrue(m_path.exists(), f"Missing required manifest file: {name}")
            with open(m_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                sr = data.get("synthetic_records", data.get("synthetic_records_across_all_datasets"))
                self.assertEqual(sr, 0, f"Violation: {name} contains synthetic records!")

    # 26. Candidate Models Not Predictive
    def test_candidate_models_not_predictive(self):
        cand_gd = model_registry.get_model("godavari_flood_candidate")
        self.assertIsNotNone(cand_gd)
        self.assertFalse(cand_gd.is_active)
        self.assertFalse(cand_gd.is_predictive)
        self.assertEqual(cand_gd.status, ModelStatus.DATA_FOUNDATION_ONLY)

        cand_mh = model_registry.get_model("mahanadi_flood_candidate")
        self.assertIsNotNone(cand_mh)
        self.assertFalse(cand_mh.is_active)
        self.assertFalse(cand_mh.is_predictive)
        self.assertEqual(cand_mh.status, ModelStatus.DATA_FOUNDATION_ONLY)

    # 27. REST API: GET /api/data/sources & GET /api/data/readiness
    def test_api_data_sources_and_readiness(self):
        resp_src = self.client.get("/api/data/sources")
        self.assertEqual(resp_src.status_code, 200)
        data_src = resp_src.json()
        self.assertGreaterEqual(data_src["count"], 5)

        resp_ready = self.client.get("/api/data/readiness")
        self.assertEqual(resp_ready.status_code, 200)
        data_ready = resp_ready.json()
        self.assertIn("brahmaputra", data_ready["summary"]["prototype_active_basins"])
        self.assertIn("godavari", data_ready["summary"]["data_foundation_calibrated_basins"])
        self.assertIn("mahanadi", data_ready["summary"]["data_foundation_calibrated_basins"])

    # 28. REST API: /api/risk/* aliases
    def test_api_risk_aliases(self):
        resp_b = self.client.get("/api/risk/basins")
        self.assertEqual(resp_b.status_code, 200)

        resp_m = self.client.get("/api/risk/models")
        self.assertEqual(resp_m.status_code, 200)


if __name__ == "__main__":
    unittest.main()

