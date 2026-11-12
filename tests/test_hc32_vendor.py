import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from check_hc32_vendor import REQUIRED, check


class TestVendorFiles(unittest.TestCase):
    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertIn("src/hc32_ll_clk.c", check(Path(d)))

    def test_complete_directory(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for item in REQUIRED:
                path = root / item
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("BSD 3-Clause" if item == "LICENSE" else "")
            self.assertEqual(check(root), [])

    def test_license_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "LICENSE").write_text("unknown license")
            self.assertTrue(any("expected BSD" in item for item in check(root)))


if __name__ == "__main__":
    unittest.main()
