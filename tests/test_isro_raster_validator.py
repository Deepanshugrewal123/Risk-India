import unittest
from pathlib import Path
from ml.data.labels.isro_raster_validator import inspect_isro_geotiff

class TestISRORasterValidator(unittest.TestCase):
    def setUp(self):
        self.nematighat_tif = Path("datasets/raw/isro/flood_inundation/assam_2021_07_06_06hr_nematighat.tif")
        self.fakirpara_tif = Path("datasets/raw/isro/flood_inundation/assam_2021_07_06_06hr_fakirpara.tif")

    def test_nematighat_raster_validation(self):
        if not self.nematighat_tif.exists():
            self.skipTest("Nematighat GeoTIFF not present locally.")
        res = inspect_isro_geotiff(
            self.nematighat_tif,
            gauge_coords=(26.860300, 94.252200),
            gauge_name="Nematighat"
        )
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["final_verdict"], "VALID_REAL_FLOOD_RASTER")
        self.assertEqual(res["crs"], "EPSG:4326")
        self.assertEqual(res["width"], 512)
        self.assertEqual(res["height"], 512)
        self.assertEqual(res["flood_pixel_count"], 2349)
        self.assertTrue(res["gauge_spatial_overlap"]["is_inside_raster_bounds"])
        self.assertAlmostEqual(res["gauge_spatial_overlap"]["nearest_flood_pixel_meters"], 806.5, places=0)

    def test_fakirpara_raster_validation(self):
        if not self.fakirpara_tif.exists():
            self.skipTest("Fakirpara GeoTIFF not present locally.")
        res = inspect_isro_geotiff(
            self.fakirpara_tif,
            gauge_coords=(26.508333, 92.116389),
            gauge_name="NH15 Crossing Fakirpara Tangni"
        )
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["final_verdict"], "EMPTY_RASTER")
        self.assertEqual(res["flood_pixel_count"], 0)
        self.assertFalse(res["gauge_spatial_overlap"]["is_inside_raster_bounds"])

if __name__ == "__main__":
    unittest.main()
