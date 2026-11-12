# CrossFlight clock configuration gap

User searched CrossFlight hwdef and the HC32 evaluation-board directory for `HC32_PLLH_`, `HC32_HCLK`, `HC32_PCLK`, `HC32_SYSCLK`, and `OSCILLATOR_HZ`.

Only match: `libraries/AP_HAL_ChibiOS/hwdef/Crossflight/hwdef.dat:19:OSCILLATOR_HZ 24000000`.

This establishes a 24 MHz board oscillator declaration but **does not establish PLL coefficients or CPU/peripheral frequencies**. Settings could be in other ChibiOS config files, generated definitions, build flags or compiled archive.

Next action: search entire RadioLink checkout for `HC32_PLLH_M_VALUE`, `HC32_PLLH_N_VALUE`, `HC32_PLLH_P_VALUE`, and `HC32_PLLH_Q_VALUE` to find actual assignments; distinguish declarations from concrete `#define`s. Do not guess frequencies.
