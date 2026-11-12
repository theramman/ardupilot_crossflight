# HC32F4A0 open-source driver candidates

Research snapshot: 2026-11-12. This is a **source discovery report**, not a completed ChibiOS port or a build result.

## Confirmed sources

1. **Zephyr XHSC HAL:** https://github.com/zephyrproject-rtos/hal_xhsc — README explicitly lists HC32F4A0 as supported or planned; confirm exact driver coverage and per-file licensing before reuse.
2. **RT-Thread HC32 series:** https://github.com/RT-Thread-packages/hc32-f4-series — contains `hc32f4a0` directory. RT-Thread's copyright notice (https://github.com/RT-Thread/rt-thread/blob/master/bsp/Copyright_Notice.md) identifies `bsp/hc32f4a0/Libraries/CMSIS` and `HC32F4A0_StdPeriph_Driver` as `bsd-new`. Verify individual files and revisions.
3. **Manufacturer DDL:** https://www.xhsc.com.cn/product/1220.html — HC32F4A0_DDL_Rev2.4.0.zip; licensing not yet audited.
4. **Device pack:** https://www.keil.arm.com/packs/hc32f4a0-hdsc/versions/ — HDSC HC32F4A0 pack 1.0.8, useful for startup/device definitions; verify redistribution permissions.

## RadioLink fork observations

- https://github.com/radiolinkW/ArduPilot-RL
- README explicitly documents `libHAL_ChibiOS_libs.a` and `libch.a` as closed-source/precompiled components.
- `libraries/AP_HAL_ChibiOS/hwdef/Crossflight/hwdef.dat` specifies `MCU HC32F4xx HC32F4A0xx` and timer groups: TIMA_9 PWM 1/10; TIMA_4 PWM 2/7/8/9; TIMA_1 PWM 3/4/5/6.
- DShot is *not* verified; hwdef comment calls for timer DMA enablement and `RCOutput::setup_group_DMA` modifications.

## Engineering conclusion

Availability of open peripheral drivers reduces the risk of an open HC32 port. It **does not** replace the ChibiOS RTOS port, ArduPilot HAL adapters, timer/DMA semantics, interrupt integration, bootloader and flash safety work.

## Next checks

- Audit licenses and actual peripheral coverage file-by-file.
- Compare HC32F4A0 startup/clock/interrupt models with RadioLink's exposed HAL glue.
- Build a dependency matrix for ChibiOS and AP_HAL_ChibiOS.
- Pin exact commits for all inputs before compilation.
- Keep experimental firmware off flight hardware until recovery procedure is verified.
