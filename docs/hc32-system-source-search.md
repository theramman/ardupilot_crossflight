# HC32 system initialization source search

The user ran:

```sh
find modules/ChibiOS/os/common -type f \( -name 'system_hc32f4a0.c' -o -name 'startup_hc32f4xx.c' -o -name 'board.c' \) | grep -i hc32
```

No output. This excludes matching filenames/paths **in the searched directory only**; it does not prove all HC32 startup source is absent from the repository.

Prior evidence: HC32 ChibiOS LLD source is missing from the HC32 port directory, while compiled driver objects are present in `modules/ChibiOS/libch.a`. The intended CrossFlight configuration uses 24 MHz XTAL, HCLK 240 MHz and PCLK1 60 MHz.

Next: evaluate the independently licensed RT-Thread HC32F4A0 BSP's clock implementation, carefully accounting for its evaluation board's 8 MHz XTAL. Confirm file-level licensing and hardware reference before adapting code. Do not flash hardware until safe startup/bootloader boundaries and recovery are established.
