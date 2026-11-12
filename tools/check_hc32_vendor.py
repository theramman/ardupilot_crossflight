#!/usr/bin/env python3
"""Check that a local HC32F4A0 vendor checkout contains required LL sources.

Read-only. This does not build firmware, alter source trees or flash hardware.
"""
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED = (
    "LICENSE",
    "inc/hc32_ll.h",
    "inc/hc32_ll_clk.h",
    "inc/hc32_ll_efm.h",
    "inc/hc32_ll_gpio.h",
    "inc/hc32_ll_pwc.h",
    "inc/hc32_ll_sram.h",
    "src/hc32_ll.c",
    "src/hc32_ll_clk.c",
    "src/hc32_ll_efm.c",
    "src/hc32_ll_gpio.c",
    "src/hc32_ll_pwc.c",
    "src/hc32_ll_sram.c",
    "src/hc32_ll_utility.c",
)


def check(root: Path) -> list[str]:
    missing = [path for path in REQUIRED if not (root / path).is_file()]
    license_path = root / "LICENSE"
    if license_path.is_file() and "BSD 3-Clause" not in license_path.read_text(errors="replace"):
        missing.append("LICENSE: expected BSD 3-Clause license text")
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vendor_dir", type=Path, help="Path to hc32-f4-series/hc32f4a0")
    args = parser.parse_args()
    missing = check(args.vendor_dir)
    if missing:
        for item in missing:
            print(f"MISSING/INVALID: {item}")
        return 1
    print(f"OK: HC32F4A0 vendor LL clock prerequisites found at {args.vendor_dir}")
    print("NOTE: no compile/link or hardware validation has been performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
