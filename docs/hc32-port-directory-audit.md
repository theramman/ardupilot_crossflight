# HC32 port directory audit

User enumerated all regular files under `modules/ChibiOS/os/hal/ports/HC32` in RadioLink checkout `e0f41a18b3a6cdba0abdcf63a5d88dc620950238`.

**Finding:** The listed directory contains headers, `.inc` configuration fragments and `driver.mk`/`platform.mk` files, but **no `.c` source files**. This does not exclude HC32 C source elsewhere in the checkout or external libraries.

- Core: `HC32F4xx/hal_lld.h`, `hc32_isr.h`, `hc32_rcc.h`, `hc32_registry.h`, `platform.mk`.
- Drivers: `ADCv1`, `DMAv1`, `EXTIv1`, `GPIOv1`, `I2Cv1`, `I2Cv2`, `OTGv1`, `RCCv1`, `SDIOv1`, `SPIv1`, `TIMv1`, `USARTv1`.
- Driver interfaces: `hal_adc_lld.h`, `hc32_dma.h`, `hc32_exti.h`, `hal_pal_lld.h`, `hal_i2c_lld.h`, `hal_usb_lld.h`, `hal_sdc_lld.h`, `hal_spi_lld.h`, `hal_gpt_lld.h`, `hal_icu_lld.h`, `hal_pwm_lld.h`, `hal_st_lld.h`, `hal_serial_lld.h`, `hal_uart_lld.h`.

**Next:** inspect `HC32F4xx/hal_lld.h` and `HC32F4xx/platform.mk` for exact clock API, oscillator assumptions, and build dependencies. Review file-level licensing before copying any code.
