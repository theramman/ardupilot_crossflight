# HC32 source-tree inventory

User-provided `find modules/ChibiOS \( -iname '*hc32*' -o -iname '*f4a0*' \)` shows substantial HC32 support material in RadioLink's ChibiOS checkout despite the absence of the five searched `.c` LLD source files.

## Located paths

- `os/hal/ports/HC32/HC32F4xx/{hc32_isr.h,hc32_rcc.h,hc32_registry.h}`
- `os/hal/ports/HC32/LLD/{GPIOv1/hc32_gpio.h,RCCv1/hc32_hse.inc,RCCv1/hc32_clkdiv.inc,RCCv1/hc32_pll.inc,DMAv1/hc32_dma.h,OTGv1/hc32_otg.h,USARTv1/hc32_uart.h,EXTIv1/hc32_exti.h,TIMv1/hc32_tim.h}`
- `os/hal/boards/HC_EV_F4A0_LQ176_V10`
- `os/common/ext/HC/HC32F4xx/{system_hc32f4a0.h,hc32f4a0.h}`
- `os/common/startup/ARMCMx/compilers/GCC/{mk/startup_hc32f4xx.mk,ld/HC32F4A0xI.ld}`
- `os/common/startup/ARMCMx/devices/HC32F4xx`

These paths are **reference material, not yet audited for licensing or verified as complete driver source**. In particular, the evaluation-board clock settings must not be assumed to match CrossFlight's 24 MHz oscillator.

Next: inspect full directory contents, headers, and license notices; determine which source implementations and build rules are absent.
