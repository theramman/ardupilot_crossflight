#!/usr/bin/env python3
"""Validate an HC32F4A0 clock plan from RadioLink hwdef source inputs.

This is a host-side configuration check, NOT a hardware clock driver.
No vendor code is copied here.
"""
from __future__ import annotations

import argparse
import pathlib
import re

DEFINE = re.compile(r"^\s*#\s*define\s+(HC32_[A-Z0-9_]+)\s+([^\s/]+)", re.M)
OSC = re.compile(r"^\s*OSCILLATOR_HZ\s+(\d+)\s*(?:#.*)?$", re.M)
FIELDS = ("M", "N", "P", "Q", "R")


def parse_clock_plan(hwdef: str, mcuconf: str) -> dict[str, int]:
    osc_matches = OSC.findall(hwdef)
    if len(osc_matches) != 1:
        raise ValueError("Expected exactly one OSCILLATOR_HZ declaration")
    defs = dict(DEFINE.findall(mcuconf))
    if defs.get("HC32_PLLSRC") != "HC32_PLLSRC_XTAL":
        raise ValueError("Only XTAL-sourced PLLH is supported by this checker")

    def number(name: str) -> int:
        try:
            return int(defs[name].removesuffix("UL").removesuffix("U"), 0)
        except (KeyError, ValueError) as exc:
            raise ValueError(f"Missing or nonnumeric {name}") from exc

    osc = int(osc_matches[0])
    divs = {key: number(f"HC32_PLLH_{key}_VALUE") for key in FIELDS}
    if not (4_000_000 <= osc <= 24_000_000):
        raise ValueError("Oscillator outside expected 4–24 MHz XTAL range")
    if not 1 <= divs["M"] <= 4 or not 25 <= divs["N"] <= 150:
        raise ValueError("PLLH M/N out of header-declared bounds")
    if any(not 1 <= divs[key] <= 16 for key in ("P", "Q", "R")):
        raise ValueError("PLLH output divider outside 1–16")
    numerator = osc * divs["N"]
    denominator = divs["M"] * divs["P"]
    if numerator % denominator:
        raise ValueError("PLLH P output is not an integer number of Hz")
    pll_out = numerator // denominator
    hclk = number("HC32_HCLK")
    pclk1 = number("HC32_PCLK1")
    if hclk != pll_out:
        raise ValueError(f"Declared HCLK {hclk} differs from calculated PLLH P output {pll_out}")
    if hclk % pclk1:
        raise ValueError("PCLK1 must divide HCLK exactly")
    ratio = hclk // pclk1
    if ratio not in (1, 2, 4, 8, 16, 32, 64):
        raise ValueError("Unsupported PCLK1 divider")
    return {"xtal_hz": osc, "pllh_p_hz": pll_out, "hclk_hz": hclk,
            "pclk1_hz": pclk1, "pclk1_divider": ratio, **{f"pll_{k.lower()}": v for k, v in divs.items()}}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hwdef", type=pathlib.Path)
    parser.add_argument("mcuconf", type=pathlib.Path)
    args = parser.parse_args()
    plan = parse_clock_plan(args.hwdef.read_text(), args.mcuconf.read_text())
    for key, value in plan.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
