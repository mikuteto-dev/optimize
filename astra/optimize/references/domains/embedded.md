# Embedded and constrained systems

Every resource has a hard ceiling: flash, RAM, stack, cycles per interrupt, current draw. Measure on the target hardware.

## Metrics

Flash and RAM use per section, maximum stack depth, cycles per hot function, interrupt latency and jitter, worst-case execution time, average and sleep current, wake-up count.

## Levers

- **Size**: `-Os` or `-Oz`, LTO, `-ffunction-sections -fdata-sections` with `--gc-sections`, newlib-nano, no floating-point `printf`, removing unused drivers and HAL layers, `no_std` and `panic = "abort"` where behavior allows.
- **RAM**: static allocation, overlaying buffers that are never live together, narrower types, bit fields, constants placed in flash.
- **Cycles**: fixed point instead of software floating point (output must match or the user decides), lookup tables placed in fast memory, DMA instead of CPU copies, code in RAM or tightly coupled memory for hot loops, intrinsics for DSP instructions.
- **Power**: sleep modes, interrupt-driven instead of polling, lower clock when idle, batching radio transmissions.

## Tools

`arm-none-eabi-size`, linker map files, `-fstack-usage`, `cargo bloat`, the DWT cycle counter (`CYCCNT`), logic analyzers, power profilers (Nordic PPK2, Joulescope).
