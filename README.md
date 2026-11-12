# ArduPilot CrossFlight — Open Board Support

An independent effort to develop **reproducible, open-source RadioLink CrossFlight board support** suitable for eventual submission to upstream [ArduPilot](https://github.com/ArduPilot/ardupilot).

**Status: feasibility audit. No firmware has been built or tested.**

## Sources

- [RadioLink's ArduPilot fork](https://github.com/radiolinkW/ArduPilot-RL), public default branch `Copter-4.3.7`
- [RadioLink's Crossflight hwdef.dat](https://github.com/radiolinkW/ArduPilot-RL/blob/Copter-4.3.7/libraries/AP_HAL_ChibiOS/hwdef/Crossflight/hwdef.dat)
- [Upstream ArduPilot](https://github.com/ArduPilot/ardupilot)

## Verified board-definition facts

- MCU declaration: `HC32F4xx HC32F4A0xx`; flash: 2048 KiB
- PWM timer groups: TIMA_9 outputs 1/10, TIMA_4 outputs 2/7/8/9, TIMA_1 outputs 3/4/5/6
- RadioLink's board definition comments that DShot requires DMA enablement and modifications to `RCOutput::setup_group_DMA`. **DShot is not verified.**
- The board definition contains alternative IMU entries for ICM42670, BMI270 and BMI323; installed sensor variant must be identified on test hardware.

## Critical blocker: binary HAL dependencies

RadioLink's README identifies `libHAL_ChibiOS_libs.a` and `libch.a` as precompiled replacements for substantial portions of AP_HAL_ChibiOS and HC32 ChibiOS sources. A genuinely open port requires appropriately licensed source implementations or replacements. Compatibility with current upstream ArduPilot is **unknown**.

## Milestones

1. Inventory HC32-specific patches, libraries, licenses and toolchain.
2. Identify or implement an open HC32 startup, clock, interrupt, GPIO, UART, USB, SPI, I2C, timer/DMA, ADC, flash and RTOS port.
3. Validate a minimal recoverable boot image on spare CrossFlight hardware.
4. Integrate a pinned stable upstream ArduPilot release; build and test incrementally.
5. Bench-test sensors, receiver input, servo safety, telemetry and logging.
6. Investigate DShot and ESC telemetry; prepare upstream-ready contributions.

## Safety

Do not flash experimental firmware to aircraft in service. Back up stock firmware and parameters, establish bootloader/recovery access, and remove rotor blades before output testing.

## Licensing

Contributions must comply with upstream ArduPilot and component licenses. No proprietary binary or source redistribution without permission.
