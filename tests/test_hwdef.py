"""Regression tests for CrossFlight timer mapping parser.

Run from repository root: python3 -m unittest discover -s tests
"""
import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "check_hwdef.py"
spec = importlib.util.spec_from_file_location("check_hwdef", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class HwdefTests(unittest.TestCase):
    def test_radio_link_timer_groups(self):
        sample = """
PE5 TIMA_9_PWM4 TIMA_9 PWM(1) GPIO(50)
PE6 TIMA_4_PWM4 TIMA_4 PWM(2) GPIO(51)
PE9 TIMA_1_PWM1 TIMA_1 PWM(3) GPIO(52)
PE11 TIMA_1_PWM2 TIMA_1 PWM(4) GPIO(53)
PE13 TIMA_1_PWM3 TIMA_1 PWM(5) GPIO(54)
PE14 TIMA_1_PWM4 TIMA_1 PWM(6) GPIO(55)
PD12 TIMA_4_PWM1 TIMA_4 PWM(7) GPIO(56)
PD13 TIMA_4_PWM2 TIMA_4 PWM(8) GPIO(57)
PD14 TIMA_4_PWM3 TIMA_4 PWM(9) GPIO(58)
PE2 TIMA_9_PWM1 TIMA_9 PWM(10) GPIO(59)
"""
        self.assertEqual(module.parse(sample), module.EXPECTED)

    def test_comments_ignored(self):
        self.assertEqual(module.parse("# PE5 TIMA_9_PWM4 TIMA_9 PWM(1)"), {})

    def test_duplicate_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate PWM output"):
            module.parse("PE5 TIMA_9_PWM4 TIMA_9 PWM(1)\nPE6 TIMA_4_PWM4 TIMA_4 PWM(1)")


if __name__ == "__main__":
    unittest.main()
