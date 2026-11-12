# HC32 clock interface and build boundary

User supplied the full RadioLink `os/hal/ports/HC32/HC32F4xx/hal_lld.h` and `platform.mk`.

## Observed interface

- `hal_lld_init(void)` and `hc32_clock_init(void)`.
- PLL configuration bounds: `HC32_PLLH_M_VALUE` 1..4, `HC32_PLLH_N_VALUE` 25..150, and `HC32_PLLH_{P,Q,R}_VALUE` 1..16.
- Clock-related helper constants include flash wait states, SRAM wait cycles, and PLL source XTAL/HRC.
- `platform.mk` references missing `HC32F4xx/hal_lld.c` and `HC32F4xx/hc32_isr.c` and includes TIM/RCC/DMA/GPIO/SPI/USB/UART/I2C/ADC/EXTI/SDIO driver makefiles.
- Header uses `#ifdef _cplusplus` rather than standard `#ifdef __cplusplus`; verify C++ linkage in a future source implementation.

## Open questions

1. What exact `HC32_PLLH_*_VALUE` and clock-divider settings are selected by the CrossFlight board configuration?
2. Which HC32 startup and system clock definitions are provided by existing sources?
3. What are the license conditions on the Radiolink header and any proposed replacement driver sources?

Do not reuse the evaluation board's 8 MHz XTAL assumptions for CrossFlight's 24 MHz oscillator. Do not claim a build or clock validation until compiled and tested.
