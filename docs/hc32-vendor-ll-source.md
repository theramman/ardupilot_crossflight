# HC32F4A0 vendor low-level driver source — verified

## Source and licensing

- Package: https://github.com/RT-Thread-packages/hc32-f4-series/tree/master/hc32f4a0
- **License:** `hc32f4a0/LICENSE` is **BSD 3-Clause**, copyright (c) 2022–2025 Xiaohua Semiconductor Co., Ltd. The license requires retaining notices and disclaimer and disallows endorsement without permission.
- Source directory includes `hc32_ll.c`, `hc32_ll_clk.c`, `hc32_ll_efm.c`, `hc32_ll_gpio.c`, `hc32_ll_pwc.c`, `hc32_ll_sram.c`.
- Include directory includes `hc32_ll.h`, `hc32_ll_clk.h`, `hc32_ll_efm.h`, `hc32_ll_sram.h`.
- Board initialization reference: https://github.com/RT-Thread/rt-thread/blob/master/bsp/hc32/ev_hc32f4a0_lqfp176/board/board.c (SPDX-License-Identifier: Apache-2.0).

These are the actual vendor LL implementation files; prior search of the RadioLink checkout returned none because it searched different filenames and a different repository.

## Next engineering action

Pin the package to a commit, audit per-file SPDX/copyright and dependencies, and create a minimal clock-only build integrating vendor LL source with the existing HC32 CMSIS device header. Adapt the RT-Thread sequence for CrossFlight's 24 MHz XTAL, PLL 1/50/5, 240 MHz HCLK and 60 MHz PCLK1. Confirm all other clock dividers and XTAL pins. Preserve notices. Do not flash until bootloader/recovery and safe startup are validated.

**Status:** source located; driver integration, compile/link and hardware validation not yet done.
