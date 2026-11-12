# HC32 binary interface audit — confirmed exported symbols

Source: user-provided output of `arm-none-eabi-nm -A -g --defined-only modules/ChibiOS/libch.a` from RadioLink checkout `e0f41a18b3a6cdba0abdcf63a5d88dc620950238`. No source implementation or running firmware was inspected.

| Archive member | Exported interfaces | Porting significance |
| --- | --- | --- |
| `hal_lld.o` | `Peripheral_WE`, `SRAM_SetWaitCycle`, `SystemCoreClock`, `hal_lld_init`, `hc32_clock_init` | clock, memory timing, low-level init |
| `hc32_isr.o` | `irqInit`, `irqDeinit`, multiple `VectorXX` | interrupts and IRQ dispatch |
| `hc32_dma.o` | `dmaInit`, `dmaChannelAllocI`, `dmaChannelFreeI`, `dmaBtcEnable`, `_hc32_dma_channels`, `hc32_dma_btc_src`, multiple `VectorXX` | DMA allocation and completion IRQs |
| `hal_pwm_lld.o` | `PWMD9`, `PWMD12`, `PWMD14`, `PWMD17`; `pwm_lld_init/start/stop/enable_channel/disable_channel` and notifications | PWM driver instances and ChibiOS LLD API |
| `hal_st_lld.o` | `st_lld_init`, `st_lld_serve_interrupt`, `Vector48` | ChibiOS system timer |

## Important caveats

- `PWMD9`, `PWMD12`, `PWMD14`, `PWMD17` are compiled driver-instance symbols. Their relationship to CrossFlight hwdef's `TIMA_1`, `TIMA_4`, `TIMA_9` is **not established**.
- `VectorXX` symbols are handler names; their numerical suffixes alone do not establish peripheral assignments without inspecting the vector table and interrupt routing.
- `nm` symbol offsets are zero because archive members can be relocatable or built with function sections; zero offsets do not imply missing code.
- Exports do not prove a function is actually linked into the CrossFlight application or exercised on the board.

## Next checks

1. Examine `nm -u` for `hal_lld.o`, `hc32_dma.o`, `hal_pwm_lld.o`, `hal_st_lld.o` to map external dependencies.
2. Locate the matching HC32 ChibiOS headers and board timer config; compare driver-instance declarations with hwdef timer mapping.
3. Inspect the interrupt vector definitions and IRQ source routing before assigning `VectorXX` to peripherals.
4. Use this interface inventory to define a source-level compatibility layer, but **do not reverse-engineer/copy proprietary object code**.
