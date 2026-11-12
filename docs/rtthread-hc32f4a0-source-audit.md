# HC32F4A0 upstream reference audit — clock and peripheral bring-up

Date: 2026-11-12. **No firmware has been built or flashed.**

## Directly inspected source

- [RT-Thread EV HC32F4A0 board README](https://github.com/RT-Thread/rt-thread/blob/master/bsp/hc32/ev_hc32f4a0_lqfp176/README.md) lists a GCC-capable HC32F4A0SITB BSP and support for ADC, flash, GPIO, clock timer, I2C, input capture, PWM, SDIO, SPI, UART, USB and watchdog.
- [RT-Thread board.c](https://github.com/RT-Thread/rt-thread/blob/master/bsp/hc32/ev_hc32f4a0_lqfp176/board/board.c) is **Apache-2.0** per its source header, and contains actual `SystemClock_Config`, `PeripheralClock_Config` and flash/cache initialization.
- [RT-Thread board Kconfig](https://github.com/RT-Thread/rt-thread/blob/master/bsp/hc32/ev_hc32f4a0_lqfp176/board/Kconfig) exposes peripheral features and UART DMA settings.
- [RT-Thread copyright notice](https://github.com/RT-Thread/rt-thread/blob/master/bsp/Copyright_Notice.md) lists its older `bsp/hc32f4a0/Libraries/CMSIS` and `HC32F4A0_StdPeriph_Driver` as BSD-new; **this is not a license determination for every current BSP file**.

## Critical hardware difference — do not copy clock configuration blindly

The EV board's `SystemClock_Config` explicitly uses an **8 MHz** external crystal in its PLL comments:

```
/* VCO = (8/1)*120 = 960MHz*/
PLLM = 1, PLLN = 120, PLLP = 4
```

The CrossFlight hwdef declares **`OSCILLATOR_HZ 24000000` (24 MHz)**. Copying those PLL factors directly to CrossFlight would target a very different VCO/CPU clock and could cause unstable or nonfunctional startup. A new clock tree must be derived from the HC32F4A0 reference manual, respecting its PLL input/VCO/flash wait-state limits and measured oscillator.

The EV BSP uses a distinct HC32F4A0SITB package/board from the RadioLink CrossFlight HC32F4A0Px definition. Reuse **device-family driver logic**, not EV board pin assignments, LED definitions, linker address assumptions or clock configuration.

## ChibiOS work remaining

1. Establish CPU startup/vector and memory map, exception priorities, SysTick/OSAL and context switching.
2. Implement a 24 MHz CrossFlight clock configuration and validate flash wait states.
3. Implement ChibiOS serial, GPIO, SPI, I2C and timer/DMA interfaces, using licensed HC32 DDL where suitable.
4. Confirm that AP_HAL_ChibiOS can be built from source, without either RadioLink precompiled archive.
5. Only after a clean link and a proven recovery mechanism, perform bench hardware bring-up.

## Immediate software acceptance criteria

- A reproducible compiler/toolchain environment is documented.
- An ELF and map file are produced with **zero** references to `libch.a` and `libHAL_ChibiOS_libs.a`.
- The linker and vector table are checked offline.
- **No flight outputs may energize at reset.**

## Risk

The public RT-Thread BSP demonstrates that open HC32F4A0 peripheral and RTOS code exists, but it does **not** establish that the same code is compatible with ChibiOS or that a CrossFlight image will boot. This document is source analysis, not hardware validation.
