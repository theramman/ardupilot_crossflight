# Codex handoff — CrossFlight HC32F4A0 port (2026-11-12)

## Mission and operating rules

Develop reproducible, open-source support for RadioLink **CrossFlight** (HC32F4A0, Cortex-M4) suitable for a modern/upstream ArduPilot port, replacing RadioLink's opaque HC32/ChibiOS binary HAL. **No bootable firmware has been built, flashed, or hardware-tested.** Keep the workflow KISS: one narrow, verifiable change/test at a time. Do not flash, run motors, or assume successful relocatable linking proves working hardware.

Project: `theramman/ardupilot_crossflight` (main).
Known user WSL/Linux workspace:
- `/home/doug/development/ardupilot_crossflight` — working project checkout (confirm `git status`).
- `/home/doug/development/ArduPilot-RL` — RadioLink ArduPilot fork checkout, branch `Copter-4.3.7`.
- `/home/doug/development/hal_xhsc` — `zephyrproject-rtos/hal_xhsc`, branch `zephyr`; HC32 sources `hc32_ddl/hc32f4a0/{drivers,soc}`.
- `/home/doug/development/ArduPilot-RL/modules/CrashDebug/mri/cmsis` — CMSIS headers used for compilation.
- `/home/doug/development/ArduPilot-RL/modules/ChibiOS` — RadioLink ChibiOS tree.

**Codex environment caveat:** Some work was created locally and/or under `/tmp` during a separate ChatGPT/WSL session. Confirm the working directory and presence of files. Do not assume these local files exist in Codex's cloud container or were committed to GitHub. Never overwrite local uncommitted work.

## Verified progress (user-reported tool output)

1. Compiled `hc32_ll_clk.c`, `hc32_ll_utility.c`, `system_hc32f4a0.c` using `arm-none-eabi-gcc`. Original four clock-object undefined symbols `DDL_DelayUS`, `HRC_VALUE`, `SystemCoreClock`, `SystemCoreClockUpdate` were resolved by combining these objects with `arm-none-eabi-ld -r`: **zero undefined symbols**.
2. Recompiled for CrossFlight with `-DHC32F4A0 -DXTAL_VALUE=24000000UL`: **zero undefined symbols**.
3. Compiled `hc32_ll_efm.c` and `hc32_ll_sram.c`, linked into `/tmp/hc32_clock_extended.o`: **zero undefined symbols**.
4. Created local `src/crossflight_clock.c`: `int32_t crossflight_clock_configure(void)`, compile-only prototype; compiled with warning originating in RadioLink CMSIS `core_cmFunc.h` (`unused parameter fpscr`). Linked with the clock, SRAM, EFM, utility, system objects into `/tmp/crossflight_clock_complete.o`: **zero undefined symbols**, `crossflight_clock_configure` exported, `arm-none-eabi-size` = text 7348, data 0, bss 24, dec 7372.
5. Inspected RadioLink `modules/ChibiOS/libch.a:hal_lld.o`:
   - exports `Peripheral_WE`, `SRAM_SetWaitCycle`, `SystemCoreClock`, `hal_lld_init`, `hc32_clock_init`;
   - undefined: `dmaInit`, `irqInit`.
   - The new vendor source defines `SystemCoreClock` and `SRAM_SetWaitCycle`, so **do not** link proprietary `hal_lld.o` alongside the replacements.
6. Created local `src/crossflight_hal_lld.c` (compile-only guard `CROSSFLIGHT_COMPILE_ONLY`). It exports `hal_lld_init` (calls `dmaInit(); irqInit();`) and `hc32_clock_init` (calls `crossflight_clock_configure`; loops on failure). Linked with `/tmp/crossflight_clock_complete.o` into `/tmp/crossflight_hal_candidate.o`; **only two undefined symbols: `dmaInit`, `irqInit`**. Both ChibiOS entry points exported. This code is a provisional integration sketch, not validated boot sequence.
7. Inspected `libch.a:hc32_isr.o`: exports `irqInit`, `irqDeinit`, and `Vector64`, `Vector6C`, `Vector70`, `Vector74`, `Vector78`, `Vector7C`, `Vector80`, `Vector84`, `Vector88`, `Vector8C`, `VectorC0`, `VectorC4`, `VectorC8`, `VectorCC`, `VectorD0`, `VectorD4`; undefined `_pal_events`, `_port_irq_epilogue`, `nvicDisableVector`, `nvicEnableVector`. This suggests ChibiOS GPIO event and IRQ-context integration that cannot be dropped.
8. Compiled licensed-source candidate `hal_xhsc/hc32_ddl/hc32f4a0/drivers/src/hc32_ll_interrupts.c` to `/tmp/hc32_ll_interrupts.o` with **zero undefined symbols**. Exports `INTC_IrqSignIn`, `INTC_IrqSignOut`, `IRQ000_Handler` ... `IRQ127_Handler` (among others), not ChibiOS `VectorXX`.
9. **Latest user check succeeded:** `arm-none-eabi-nm` confirms open-source `IRQ009_Handler`, `IRQ012_Handler`, `IRQ032_Handler`, `IRQ037_Handler`; RadioLink `Vector64`, `Vector70`, `VectorC0`, `VectorD4`; `vectors.S` has those names in vector table and as weak handlers. Mapping verified: `Vector64` ↔ IRQ 9, `Vector70` ↔ IRQ 12, `VectorC0` ↔ IRQ 32, `VectorD4` ↔ IRQ 37. **Naming/index correspondence only; runtime handler equivalence is NOT established.**

## Hardware/clock constraints

- `libraries/AP_HAL_ChibiOS/hwdef/Crossflight/hwdef.dat` declares `OSCILLATOR_HZ 24000000`, `FLASH_RESERVE_START_KB 184`, `FLASH_SIZE_KB 2048`.
- `libraries/AP_HAL_ChibiOS/hwdef/common/hc32f4_mcuconf.h` selects PLL XTAL M=1, N=50, P=Q=R=5, intended HCLK=240 MHz and PCLK1=60 MHz. HC32 register fields are parameter-minus-one.
- `src/crossflight_clock.c` configures 5 flash wait states, SRAMH 1 read/write wait cycle, other SRAM 2 cycles; sets PCLK1 /4 and other bus clocks, then starts XTAL, PLL and switches SYSCLK, checks frequencies.
- This is **NOT hardware validated**: bootloader may hand over with clocks already active, oscillator drive and XTAL stabilization settings must be validated, SYSCLK switch procedure and memory timing must be reviewed, and failure behavior is provisional.
- The open-source `soc/system_hc32f4a0.c` provides `SystemInit()` which writes `SCB->VTOR = VECT_TAB_OFFSET` (default 0) — dangerous with the bootloader-reserved flash region unless startup ordering/VTOR handling is confirmed.
- RadioLink ChibiOS `os/common/startup/ARMCMx/compilers/GCC/vectors.S` references `VectorXX` weak symbols; `crt0_v7m.S` may write VTOR to `_vectors`. Verify **effective startup execution order** before using `SystemInit()` in a firmware image.
- `/tmp` relocatable bundles are **not** full firmware and will disappear on environment reset.

## IRQ details from source inspection

Sources:
- `radiolinkW/ChibiOS` branch `Copter-4.3`:
  - `os/hal/ports/HC32/HC32F4xx/hc32_isr.h`
  - `os/hal/ports/HC32/HC32F4xx/hc32_registry.h`
  - `os/common/startup/ARMCMx/compilers/GCC/vectors.S`
- `zephyrproject-rtos/hal_xhsc` branch `zephyr`:
  - `hc32_ddl/hc32f4a0/drivers/inc/hc32_ll_interrupts.h`
  - `hc32_ddl/hc32f4a0/drivers/src/hc32_ll_interrupts.c`.

Important: the HC32 LL driver maintains `m_apfnIrqHandler[IRQ_NUM_MAX]` and `IRQnnn_Handler` calls the per-slot registered callback. `INTC_IrqSignIn` associates source/slot/callback with the interrupt selector. A direct `VectorXX -> IRQnnn_Handler` alias is **not sufficient** unless registration, correct event source, IRQ clearance, NVIC priority/enable and ChibiOS ISR prologue/epilogue are established.

The RadioLink `hc32_registry.h` maps EXTI GPIO IRQ slots 32–37 to `VectorC0` … `VectorD4`, and `hc32_isr.h` maps `USART2` TXI IRQ 9 to `Vector64`, etc. The existing ISR object has ChibiOS-specific references `_pal_events` and `_port_irq_epilogue`; preserve equivalent behavior. Note vendor ISR object covers only a subset of vectors and the actual board/peripheral effective `mcuconf.h` must be inspected.

## Exact recommended next task for Codex

**Do not implement handlers yet.** First perform a focused, source-level IRQ-interface audit:
1. Inspect the effective ChibiOS ISR macros and prologue/epilogue calling convention plus ChibiOS PAL/EXTI event code.
2. Compare them with HC32 LL `INTC_IrqSignIn`/callback dispatcher and the verified `VectorXX` vector table.
3. Determine which ISR slots are really enabled by CrossFlight effective `hwdef.dat`/generated config; trace `NVIC` and `INTC` registration and IRQ-source routing, including bootloader vector relocation.
4. Propose **one small, compile-only, testable** adapter change (no empty `irqInit()` stub, no fake ISR or prematurely linking proprietary objects). Show the exact command and expected output; run the test if environment permits. Ask for user output if local WSL inaccessible.

Do not modify hardware boot flow, flash, or remove `CROSSFLIGHT_COMPILE_ONLY` safeguards until explicitly reviewed.

## Compile command for HC32 LL sources (if rebuilding in local WSL)

```bash
SDK="$HOME/development/hal_xhsc/hc32_ddl/hc32f4a0"
CMSIS="$HOME/development/ArduPilot-RL/modules/CrashDebug/mri/cmsis"
arm-none-eabi-gcc -c -std=gnu11 -mcpu=cortex-m4 -mthumb -Os \
  -DHC32F4A0 -DXTAL_VALUE=24000000UL \
  -ffunction-sections -fdata-sections \
  -I"$SDK/drivers/inc" -I"$SDK/soc" -I"$CMSIS" \
  -o /tmp/hc32_ll_interrupts.o "$SDK/drivers/src/hc32_ll_interrupts.c"
arm-none-eabi-nm -u /tmp/hc32_ll_interrupts.o
```

Compiling/linking objects was user-verified, not independently re-run in Codex's environment. Source/redistribution licensing of each dependency must be checked before contributing upstream.
