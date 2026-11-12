# HC32 MCU configuration include chain

User confirmed by repository grep:

```
libraries/AP_HAL_ChibiOS/hwdef/common/mcuconf.h:59:#include "hc32f4_mcuconf.h"
```

This establishes the **common MCU configuration's direct include** of the HC32 defaults. It does **not alone prove** CrossFlight's generated board configuration includes `common/mcuconf.h` or that the compiled firmware programs those values.

The HC32 defaults specify XTAL PLL source, M=1, N=50, P=Q=R=5, HCLK=240 MHz and PCLK1=60 MHz; CrossFlight hwdef declares a 24 MHz oscillator.

Next step: inspect source-level clock register definitions and licensing, then implement a separately licensed HC32 clock module with compile-only checks before any flashing.
