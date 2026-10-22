# Mobile apps

Measure release builds on low-end physical devices; simulators and debug builds misreport startup, memory and energy.

## Metrics

Cold and warm startup (time to initial display, time to full display), frame time and dropped frames, memory (peak, footprint, OOM kills), download and install size, energy and wakeups, network bytes, ANRs and main-thread hangs.

## Levers

- **Startup**: defer initialization, lazy-load modules, fewer dynamic libraries and static initializers, Baseline Profiles (Android), prewarmed or cached first screen.
- **Size**: R8 shrinking and resource shrinking, app bundles and app thinning, on-demand assets, removing unused dependencies and locales, compressed and vector assets.
- **Rendering**: flatter view hierarchies, list recycling, no work on the main thread, fewer recompositions or re-renders, image decoding at display size off the main thread.
- **Energy and network**: batching requests, background work through the platform schedulers, fewer location and sensor wakeups, caching and compression.

Removing features, lowering image quality, and dropping OS versions need the user.

## Tools

Android Studio profilers, Perfetto, Macrobenchmark, Xcode Instruments (Time Profiler, Allocations, Energy Log, App Launch), MetricKit, `os_signpost`.

## With bench.py

`--before` and `--after` are the two release builds. A locked `bench/measure-app.sh {cmd}` installs the build on the attached low-end device, runs Macrobenchmark or an `xctrace` App Launch recording, and prints `{"startup_ms": …, "jank_frames": …, "size_bytes": …}`.
