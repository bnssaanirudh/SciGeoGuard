import unittest
from scigeoguard_core import Artifact, Step, Intent, verify_science

class CoreVerifierTests(unittest.TestCase):
    def test_nominal_bilinear_resampling_is_refuted(self):
        result = verify_science(
            [Artifact("land cover", "land_cover_class", scale="nominal", provenance="fixture")],
            [Step("resample", {"artifact": 0, "method": "bilinear", "target_resolution_m": 10})],
            Intent("preserve class identity"),
        )
        self.assertEqual(result["verdict"], "REFUTED")
        self.assertIn("CATEGORICAL_INTERPOLATION", {f["code"] for f in result["findings"]})

    def test_nearest_resampling_is_not_refuted_by_interpolation_rule(self):
        result = verify_science(
            [Artifact("land cover", "land_cover_class", scale="nominal", provenance="fixture")],
            [Step("resample", {"artifact": 0, "method": "nearest", "target_resolution_m": 10})],
            Intent("preserve class identity"),
        )
        self.assertNotIn("CATEGORICAL_INTERPOLATION", {f["code"] for f in result["findings"]})

if __name__ == "__main__":
    unittest.main()
