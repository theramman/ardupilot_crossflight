# RadioLink archive object inventory and replacement strategy

Evidence: user ran `arm-none-eabi-ar t` on the exact RadioLink source checkout at `e0f41a18b3a6cdba0abdcf63a5d88dc620950238` and ChibiOS at `b5d48e0eb8d3e81df0c3caef0e43b0191b120aa1`. The inventory is supplied by the user; **not independently reproduced in this repository**.

## `modules/ChibiOS/libch.a`

**HC32-specific/low-level candidates to replace or validate**: `hal_lld.o`, `hc32_isr.o`, `hc32_dma.o`, `hc32_exti.o`, `hal_adc_lld.o`, `hal_pal_lld.o`, `hal_i2c_lld.o`, `hal_usb_lld.o`, `hal_sdc_lld.o`, `hal_spi_lld.o`, `hal_gpt_lld.o`, `hal_icu_lld.o`, `hal_pwm_lld.o`, `hal_st_lld.o`, `hal_serial_lld.o`, `hal_uart_lld.o`. Also investigate `vectors.o`, `crt0_v7m.o`, `chcore*.o`, `nvic.o`, `board.o`, `flash.o`, `hc32_util.o`, `watchdog.o` and `hrt.o`; these may contain target-specific glue.

**Potential upstream-source reuse**: ChibiOS OSAL, HAL generic objects (`hal_spi.o`, `hal_pwm.o`, etc.), kernel `ch*.o`, FATFS, streams. Their presence in the archive is not evidence they were modified or unmodified: compare source and symbol signatures.

## `libraries/AP_HAL_ChibiOS/libHAL_ChibiOS_libs.a`

Includes upstream-like ArduPilot C++ modules (`GPIO`, `RCOutput`, `Scheduler`, `Storage`, `UARTDriver`, `SPIDevice`, `I2CDevice`, etc.), AP_Scripting/Lua, and standard utility objects. Duplicate base names with suffixes `.0.o` and `.3.o` imply build variants or distinct targets, **not proof of source modifications**.

Key objects to compare to public source: `HAL_ChibiOS_Class.cpp.3.o`, `RCOutput.cpp.3.o`, `GPIO.cpp.3.o`, `Storage.cpp.3.o`, `system.cpp.3.o`, `RCOutput_bdshot.cpp.0.o`.

**Important:** Presence of `RCOutput_bdshot.cpp.0.o` proves only that the archive contains an object with that name. It does not demonstrate functional DShot, bidirectional capture, or CrossFlight timer DMA support.

## Next evidence to collect

Use `arm-none-eabi-nm -A -g --defined-only` on the two root-level archives to inspect symbol provenance and `arm-none-eabi-ar t` to inspect archive members. Do not mistake the demo `modules/ChibiOS/demos/various/RT-ARMCM4-USELIB/rt/libch.a` for the board library.

Then compare against available upstream source, with particular attention to the HC32 port and ArduPilot HAL overrides. Do not copy proprietary archive objects into an open-source distribution.

## Immediate development priorities

1. Determine which HC32 low-level interfaces are actually required for minimal startup/serial.
2. Implement and compile those interfaces from permissively licensed source.
3. Validate CrossFlight-specific 24 MHz oscillator and memory/bootloader boundaries.
4. Keep motor outputs disabled until safe bench validation.
