# CrossFlight clock defaults — source confirmed

The user supplied the full RadioLink `libraries/AP_HAL_ChibiOS/hwdef/common/hc32f4_mcuconf.h` plus a grep from CrossFlight `hwdef.dat`.

Source-level settings:

- `OSCILLATOR_HZ 24000000` in `Crossflight/hwdef.dat`.
- `HC32_PLLSRC HC32_PLLSRC_XTAL`.
- `HC32_PLLH_M_VALUE 1`, `N_VALUE 50`, `P_VALUE 5`, `Q_VALUE 5`, `R_VALUE 5`.
- `HC32_HCLK 240000000UL`.
- `HC32_PCLK1 60000000UL`.
- `HC32_ST_USE_TIMER 1`.
- The header comment: "this provides the default mcuconf.h for each board. Override values in hwdef.dat".

Thus the **intended** HCLK and PCLK1 values are explicit, not merely inferred from PLL arithmetic. The generated configuration and actual clock-register programming have **not** been inspected.

Other relevant settings: default USB OTG1 enabled; ADC1 enabled; UART/SPI/I2C DMA channel defaults; PWM and GPT TIMA flags default to FALSE unless overridden. A future DMA resource allocation audit must use *effective generated settings*, not defaults alone.

## Next verification

1. Inspect generated CrossFlight `mcuconf.h` or hwdef generation logic for inclusion of `hc32f4_mcuconf.h`.
2. Inspect `hc32_rcc.h` and available licensed HC32 clock source for SYSCLK, bus divider and wait-state programming.
3. Establish source license before incorporating Radiolink material into a distributable upstream port.
