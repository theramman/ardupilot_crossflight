# HC32 clock register interface

User supplied RadioLink `os/hal/ports/HC32/HC32F4xx/hc32_rcc.h`.

The header provides constants for XTAL/HRC PLL sources, XTAL drive levels, crystal stabilization options, system-clock mux (`CLK_SYSCLKSOURCE_PLLH`), and HCLK/PCLK0..4/EXCLK divider selections.

For CrossFlight, known source-level targets are 24 MHz external oscillator, PLL M=1 N=50 P=Q=R=5, HCLK 240 MHz, PCLK1 60 MHz. **Conditional intended divider configuration:** HCLK /1, PCLK1 /4, assuming PLLH output to HCLK at 240 MHz. The header alone does not prove actual programmed divider settings or the sequence for switching clock sources.

Key considerations for a new implementation: XTAL drive setting for 24 MHz, XTAL readiness and timeout, PLL readiness and timeout, flash wait cycles, SRAM access wait cycles, protected register writes, clock switching and stable waiting. The header declares constants but does not implement these operations. Check hardware reference manual and open licensed vendor code before writing register-level operations.

Header copyright notice identifies Radiolink; do not assume reuse license without checking. Avoid copying the header into a new open-source implementation until license is established.
