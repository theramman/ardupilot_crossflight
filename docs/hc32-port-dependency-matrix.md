# CrossFlight HC32 port — implementation dependency matrix

Status: planning only; no code compiled. Verified RadioLink board mapping comes from `libraries/AP_HAL_ChibiOS/hwdef/Crossflight/hwdef.dat` in `radiolinkW/ArduPilot-RL` at `Copter-4.3.7`.

| Layer | Existing evidence | Open-port deliverable | Priority | Verified implemented? |
| --- | --- | --- | --- | --- |
| Cortex-M4 CMSIS/startup | RT-Thread HC32F4A0 CMSIS identified as BSD-new in RT-Thread copyright notice | Pin licensed startup/vector/device headers, check CPU flags | P0 | No |
| Clock/reset/interrupt | Manufacturer HC32F4A0 DDL available | Clock tree, system timer, IRQ vector mapping and ChibiOS OSAL integration | P0 | No |
| Linker/flash/bootloader | hwdef: 2048 KiB flash, `FLASH_RESERVE_START_KB 184`, `APJ_BOARD_ID 3` | Confirm bootloader reserve, application start, memory partitions and recovery | P0 | No |
| GPIO/pinmux | Crossflight hwdef contains pin assignments | GPIO and pinmux HAL with verified safe output defaults | P0 | No |
| UART/USB | hwdef: `SERIAL_ORDER OTG1 USART1 USART2 USART6` | Console/telemetry serial and USB device integration | P0 | No |
| SPI | hwdef: SPI1 IMU, SPI2 baro and other devices | SPI transactions, DMA and chip selects | P1 | No |
| I2C | hwdef: I2C2, I2C1 | I2C transactions, recovery, external GPS/compass connectivity | P1 | No |
| Timer PWM | TIMA_9: 1/10; TIMA_4: 2/7/8/9; TIMA_1: 3/4/5/6 | Safe RCOutput PWM generation and capture | P1 | No |
| DMA/DShot | hwdef has DMA channel definitions for TIMA_1 and TIMA_4; explicitly requires RCOutput changes | Timer-trigger DMA, DShot waveforms, later bidirectional capture if feasible | P2 | No |
| ADC | hwdef: battery voltage/current, 5V, RSSI | ADC scaling and sampling | P1 | No |
| SDIO/storage/flash | hwdef: SDIO1, FATFS and storage definitions | Log storage, parameters, flash integrity | P1 | No |
| IMU/baro | hwdef alternatives ICM42670/BMI270/BMI323 and LPS22HB | Identify actual board variant, verify sensor SPI and rotations | P1 | No |
| ChibiOS RTOS | RadioLink provides `libch.a` | Open HC32 ChibiOS port with context switch, scheduling, IRQ locking, timer tick | P0 | No |
| AP_HAL_ChibiOS | RadioLink provides `libHAL_ChibiOS_libs.a` | Replace HC32-specific adaptations with upstream-compatible source | P0 | No |

## Implementation order

1. Select and pin a driver source after file-level license review.
2. Produce an **unflashed** minimal ARM build with linker map, vector table, clock/interrupt and GPIO support.
3. Establish SWD or ROM-boot recovery and bootloader preservation before any flash.
4. Bench-test clock, LED, UART/USB, SPI, I2C and safe PWM outputs with motors disconnected.
5. Port upstream ArduPilot and only then evaluate DShot/ESC telemetry.

## Source references

- https://github.com/radiolinkW/ArduPilot-RL
- https://github.com/zephyrproject-rtos/hal_xhsc
- https://github.com/RT-Thread/rt-thread/blob/master/bsp/Copyright_Notice.md
- https://www.xhsc.com.cn/product/1220.html

**Important:** Existence of a vendor peripheral driver does not establish an open ChibiOS implementation or permission to redistribute all files. All compatibility and licensing questions remain open until audited.
