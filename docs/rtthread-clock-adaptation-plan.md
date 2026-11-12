# Apache-2.0 HC32F4A0 clock implementation reference

## Verified source

- RT-Thread source: https://github.com/RT-Thread/rt-thread/blob/master/bsp/hc32/ev_hc32f4a0_lqfp176/board/board.c
- Copyright (C) 2022-2024 Xiaohua Semiconductor Co., Ltd.
- File SPDX identifier: **Apache-2.0**.
- Repository root LICENSE: Apache License 2.0.

This file implements `SystemClock_Config` and is a **reference**, not a drop-in ChibiOS clock driver. Any adaptation must retain applicable copyright, SPDX and modification notices.

## Reference initialization sequence

1. Configure bus dividers while still using the initial system clock.
2. Configure XTAL GPIO pins for analog mode.
3. Initialize and enable external crystal.
4. Configure and enable PLLH.
5. Configure high-speed and other SRAM wait cycles.
6. Configure embedded flash and GPIO read wait cycles.
7. Switch SYSCLK to PLL.
8. Configure USB PLLX separately if USB support is enabled.

RT-Thread board's XTAL is **8 MHz**, PLLH M=1 N=120 P=Q=R=4, resulting in a 240 MHz PLL output. Its PCLK1 divider is /2, or 120 MHz. These settings **must not** be copied unchanged.

## CrossFlight intended configuration

From RadioLink CrossFlight and common HC32 configuration:

| Item | CrossFlight | RT-Thread evaluation board |
| --- | --- | --- |
| XTAL | 24 MHz | 8 MHz |
| XTAL drive | high drive expected for 20–24 MHz, verify electrical specification | ultra-low |
| PLL M/N/P/Q/R | 1/50/5/5/5 | 1/120/4/4/4 |
| HCLK | 240 MHz | 240 MHz |
| PCLK1 | 60 MHz | 120 MHz |
| PCLK1 divider if SYSCLK=240 MHz | /4 | /2 |

The RT-Thread example configures PCLK0=/1, PCLK2=/4, PCLK3=/4, PCLK4=/2, EXCLK=/2, HCLK=/1; CrossFlight's **other bus dividers are not yet verified**.

## Requirements before integrating into ChibiOS

- Verify clock register access, write protection and wait-state constraints against HC32F4A0 vendor documentation and licensed vendor LL headers.
- Check each initialization API's return value and oscillator/PLL ready state; provide a safe failure path.
- Verify the correct XTAL GPIO pins and drive strength on the physical CrossFlight variant.
- Check whether ArduPilot's startup path calls `hc32_clock_init` and how `hal_lld_init` and `SystemCoreClock` interact.
- Implement USB clock generation if needed for CrossFlight's OTG1.
- Establish the license for each dependency (not just RT-Thread board.c) before copying or adapting source.
- No flight or flashing until build, bootloader/recovery and bench safety are validated.
