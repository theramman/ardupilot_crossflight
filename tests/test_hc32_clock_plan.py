"""Host-side clock configuration regression tests."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from hc32_clock_plan import parse_clock_plan

HWDEF = "MCU HC32F4xx HC32F4A0xx\nOSCILLATOR_HZ 24000000\n"
CONFIG = """#define HC32_PLLSRC HC32_PLLSRC_XTAL
#define HC32_PLLH_M_VALUE 1
#define HC32_PLLH_N_VALUE 50
#define HC32_PLLH_P_VALUE 5
#define HC32_PLLH_Q_VALUE 5
#define HC32_PLLH_R_VALUE 5
#define HC32_HCLK 240000000UL
#define HC32_PCLK1 60000000UL
"""


class TestClockPlan(unittest.TestCase):
    def test_crossflight(self):
        plan = parse_clock_plan(HWDEF, CONFIG)
        self.assertEqual(plan["hclk_hz"], 240_000_000)
        self.assertEqual(plan["pclk1_divider"], 4)

    def test_wrong_clock_rejected(self):
        with self.assertRaisesRegex(ValueError, "differs"):
            parse_clock_plan(HWDEF, CONFIG.replace("240000000UL", "200000000UL"))

    def test_unsupported_divider_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unsupported"):
            parse_clock_plan(HWDEF, CONFIG.replace("60000000UL", "48000000UL"))

    def test_missing_oscillator_rejected(self):
        with self.assertRaisesRegex(ValueError, "exactly one"):
            parse_clock_plan("MCU HC32F4xx HC32F4A0xx", CONFIG)

    def test_pll_source_rejected(self):
        with self.assertRaisesRegex(ValueError, "XTAL"):
            parse_clock_plan(HWDEF, CONFIG.replace("HC32_PLLSRC_XTAL", "HC32_PLLSRC_HRC"))


if __name__ == "__main__":
    unittest.main()
