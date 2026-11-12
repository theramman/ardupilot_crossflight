# CrossFlight PLL configuration candidate

User found concrete defines in RadioLink `libraries/AP_HAL_ChibiOS/hwdef/common/hc32f4_mcuconf.h`:

```
#define HC32_PLLH_M_VALUE 1
#define HC32_PLLH_N_VALUE 50
#define HC32_PLLH_P_VALUE 5
#define HC32_PLLH_Q_VALUE 5
#define HC32_PLLH_R_VALUE 5
```

CrossFlight hwdef separately declares `OSCILLATOR_HZ 24000000`.

**Conditional calculation:** If the HC32 PLL relation is `(XTAL/M)*N` and P/Q/R are simple output dividers, then 24 MHz / 1 * 50 = 1200 MHz VCO and 1200 MHz / 5 = 240 MHz outputs. This is **not yet confirmed** as CrossFlight's effective CPU clock or valid PLL operation: verify the HC32 clock reference, board inclusion of `hc32f4_mcuconf.h`, SYSCLK mux and bus dividers.

Another matching set in `modules/ChibiOS/demos/STM32/RT-STM32F401RE-NUCLEO64/cfg/mcuconf.h` is 1/120/4/4/4 and must not be mistaken for the CrossFlight board configuration.

Next: inspect `hwdef.dat` includes, `hwdef/common/hc32f4_mcuconf.h` full content, and HC32 clock source/divider declarations.
