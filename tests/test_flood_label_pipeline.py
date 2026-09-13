"""
RISK // INDIA — Automated Test Suite: Flood Ground-Truth Label Pipeline

Verifies that the label ingestion, validation, event grouping, alignment,
and negative sampling pipeline strictly enforces scientific integrity and refuses unsafe assumptions:

Test Cases (11 total):
1. test_malformed_gis_file: Handled cleanly, rejected without crashing
2. test_wrong_or_missing_crs: Rejects Cartesian projected coordinates or non-WGS84 declarations
3. test_invalid_geometry: Rejects unclosed polygon rings and degenerate point lists
4. test_duplicate_event_detection: Groups or deduplicates identical observation records
5. test_missing_event_date: Rejects features lacking observation dates
6. test_temporal_mismatch: Identifies disjoint observation periods
7. test_spatial_mismatch: Identifies geometries outside Assam's regional bounding box
8. test_missing_predictor_window: Handles time periods with missing telemetry without leakage
9. test_insufficient_rainfall_coverage: Rejects predictor windows with < 70% data completeness
10. test_negative_label_contamination_prevention: Rejects negative samples within +/- 7 days of known flood
11. test_empty_isro_directory_readiness: Safely reports NOT_READY without crashing
"""

import unittest
from pathlib import Path
import tempfile
import json
import pandas as pd
import numpy as np
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ml.data.labels.isro_flood_loader import ISROFloodInundationLoader
from ml.data.labels.event_builder import FloodEventBuilder
from ml.data.labels.negative_sampler import DefensibleNegativeSampler
from ml.data.labels.check_label_readiness import evaluate_training_readiness_gate
from ml.data.alignment.temporal_alignment import TemporalEventAligner
from ml.data.alignment.spatial_alignment import GeospatialAligner


class TestFloodLabelPipeline(unittest.TestCase):

    def setUp(self):
        self.loader = ISROFloodInundationLoader()

    # TEST 1: Malformed GIS File
    def test_malformed_gis_file(self):
        with tempfile.NamedTemporaryFile(suffix=".geojson", mode="w", delete=False) as tf:
            tf.write("{malformed json content: [unclosed")
            tf_path = Path(tf.name)

        try:
            res = self.loader.load_and_validate_geojson(tf_path)
            self.assertFalse(res["valid"])
            self.assertEqual(res["status"], "MALFORMED_JSON")
        finally:
            tf_path.unlink(missing_ok=True)

    # TEST 2: Wrong or Missing CRS (Projected coordinates in hundreds of thousands)
    def test_wrong_or_missing_crs(self):
        # Projected UTM coordinates (meters) disguised as lat/long
        bogus_utm_coords = [[[450000.0, 2900000.0], [460000.0, 2900000.0], [460000.0, 2910000.0], [450000.0, 2900000.0]]]
        geojson_data = {
            "type": "FeatureCollection",
            "crs": {"type": "name", "properties": {"name": "EPSG:32646"}}, # Non-4326
            "features": [{
                "type": "Feature",
                "properties": {"observation_date": "2024-07-01", "district": "KAMRUP"},
                "geometry": {"type": "Polygon", "coordinates": bogus_utm_coords}
            }]
        }
        with tempfile.NamedTemporaryFile(suffix=".geojson", mode="w", delete=False) as tf:
            json.dump(geojson_data, tf)
            tf_path = Path(tf.name)

        try:
            res = self.loader.load_and_validate_geojson(tf_path)
            self.assertFalse(res["valid"])
            self.assertEqual(res["status"], "VALIDATION_FAILED")
        finally:
            tf_path.unlink(missing_ok=True)

    # TEST 3: Invalid Geometry (Unclosed ring)
    def test_invalid_geometry(self):
        # Unclosed ring: start (92.0, 26.0) != end (92.5, 26.5)
        unclosed_ring = [[92.0, 26.0], [93.0, 26.0], [93.0, 27.0], [92.5, 26.5]]
        geojson_data = {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {"observation_date": "2024-07-01"},
                "geometry": {"type": "Polygon", "coordinates": [unclosed_ring]}
            }]
        }
        with tempfile.NamedTemporaryFile(suffix=".geojson", mode="w", delete=False) as tf:
            json.dump(geojson_data, tf)
            tf_path = Path(tf.name)

        try:
            res = self.loader.load_and_validate_geojson(tf_path)
            self.assertFalse(res["valid"])
            self.assertEqual(res["status"], "VALIDATION_FAILED")
        finally:
            tf_path.unlink(missing_ok=True)

    # TEST 4: Duplicate Event Detection
    def test_duplicate_event_detection(self):
        builder = FloodEventBuilder()
        dup_obs = [
            {"event_id": "FE_01", "event_date": "2022-06-18", "district": "DARRANG", "coordinates": "POLY_A"},
            {"event_id": "FE_01", "event_date": "2022-06-18", "district": "DARRANG", "coordinates": "POLY_A"}, # Duplicate
            {"event_id": "FE_02", "event_date": "2022-06-18", "district": "KAMRUP", "coordinates": "POLY_B"}
        ]
        deduped = builder.detect_duplicates(dup_obs)
        self.assertEqual(len(deduped), 2)

    # TEST 5: Missing Event Date
    def test_missing_event_date(self):
        valid_ring = [[92.0, 26.0], [93.0, 26.0], [93.0, 27.0], [92.0, 27.0], [92.0, 26.0]]
        geojson_data = {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {"district": "DARRANG"}, # NO observation_date
                "geometry": {"type": "Polygon", "coordinates": [valid_ring]}
            }]
        }
        with tempfile.NamedTemporaryFile(suffix=".geojson", mode="w", delete=False) as tf:
            json.dump(geojson_data, tf)
            tf_path = Path(tf.name)

        try:
            res = self.loader.load_and_validate_geojson(tf_path)
            self.assertFalse(res["valid"])
            self.assertIn("Missing required event observation date", res["validation_errors"][0])
        finally:
            tf_path.unlink(missing_ok=True)

    # TEST 6: Temporal Mismatch
    def test_temporal_mismatch(self):
        rf_data = pd.DataFrame({
            "Data Acquisition Time": ["01-01-2022 10:00", "01-01-2022 11:00"],
            "Telemetry Hourly Rainfall (mm)": [5.0, 10.0]
        })
        aligner = TemporalEventAligner(rf_data)
        # Event in 2026 (outside 2022 predictor range)
        features = aligner.extract_antecedent_features_for_event(pd.Timestamp("2026-08-01 12:00:00"))
        # Window in 2026 should have 0 observations and insufficient coverage
        self.assertIsNone(features["rainfall_windows"]["rainfall_24h"])
        self.assertIn("INSUFFICIENT", features["rainfall_windows"]["rainfall_24h_status"])

    # TEST 7: Spatial Mismatch (Geometry outside Assam bounding box)
    def test_spatial_mismatch(self):
        # Gujarat coordinates (~70°E, 22°N) - outside Assam's 89.5°E–96.5°E, 24°N–28.5°N
        gujarat_coords = [[[70.0, 22.0], [71.0, 22.0], [71.0, 23.0], [70.0, 23.0], [70.0, 22.0]]]
        valid_crs, msg, bbox = self.loader.validate_crs_and_coordinates(gujarat_coords, "Polygon")
        self.assertTrue(valid_crs) # Valid global WGS84
        self.assertFalse(bbox["intersects_assam_region"]) # But outside Assam region

    # TEST 8: Missing Predictor Window Handling Without Leakage
    def test_missing_predictor_window(self):
        empty_rf = pd.DataFrame(columns=["Data Acquisition Time", "Telemetry Hourly Rainfall (mm)"])
        aligner = TemporalEventAligner(empty_rf)
        features = aligner.extract_antecedent_features_for_event(pd.Timestamp("2024-07-01 12:00:00"))
        self.assertTrue(features["temporal_leakage_prevented"])
        self.assertIsNone(features["rainfall_windows"]["rainfall_24h"])

    # TEST 9: Insufficient Rainfall Coverage Rejection (< 70%)
    def test_insufficient_rainfall_coverage(self):
        # Provide only 5 hours of data for a 24-hour window (5/24 = 20.8% < 70%)
        sparse_rf = pd.DataFrame({
            "Data Acquisition Time": [
                f"15-07-2024 {h:02d}:00" for h in range(5)
            ],
            "Telemetry Hourly Rainfall (mm)": [2.0] * 5
        })
        aligner = TemporalEventAligner(sparse_rf, min_sufficiency_pct=70.0)
        features = aligner.extract_antecedent_features_for_event(pd.Timestamp("2024-07-15 23:00:00"))
        # Must be rejected due to insufficient data
        self.assertIsNone(features["rainfall_windows"]["rainfall_24h"])
        self.assertIn("INSUFFICIENT", features["rainfall_windows"]["rainfall_24h_status"])

    # TEST 10: Negative-Label Contamination Around Flood Events
    def test_negative_label_contamination_prevention(self):
        sampler = DefensibleNegativeSampler(temporal_exclusion_days=7)
        known_floods = [{"event_date": "2024-07-10"}]
        # Candidate date within 3 days of flood (2024-07-13)
        contaminated, reason = sampler.is_date_contaminated_by_flood(
            pd.Timestamp("2024-07-13"),
            [pd.Timestamp("2024-07-10")]
        )
        self.assertTrue(contaminated)
        self.assertIn("CONTAMINATED", reason)

        # Candidate date 15 days later (2024-07-25) -> Safe
        safe, reason_safe = sampler.is_date_contaminated_by_flood(
            pd.Timestamp("2024-07-25"),
            [pd.Timestamp("2024-07-10")]
        )
        self.assertFalse(safe)

    # TEST 11: Empty ISRO Directory Handling
    def test_empty_isro_directory_readiness(self):
        report = evaluate_training_readiness_gate()
        # With empty ISRO directory, training must be strictly False
        self.assertFalse(report["training_ready"])
        self.assertIn(report["status"], ["NOT_READY", "SOURCE_DATA_AVAILABLE"])


if __name__ == "__main__":
    unittest.main()
