# Desktop applications and CLIs

## Metrics

Cold and warm startup, idle CPU and wakeups, memory across all processes (main, renderers, helpers, GPU process), installer and on-disk size, input latency, frame time, energy impact.

## Levers

- **Startup**: lazy-load modules and windows, fewer files read at launch, V8 snapshots or bytecode caches (Electron), avoiding interpreter startup for short-lived CLIs (static binaries in Go or Rust), no network on the startup path.
- **Memory**: fewer renderer processes, releasing hidden windows, avoiding duplicate copies of large data across processes.
- **Idle**: no polling timers, event-driven file watching, throttling background work.
- **Size**: removing unused locales, native modules and dependencies, compressing resources, stripping symbols in release artifacts (operations change, needs the user).

Switching frameworks (Electron to Tauri or native, which uses the system webview or toolkit) is an architecture change and needs the user.

## Tools

`hyperfine` for CLI startup, Xcode Instruments, Activity Monitor energy impact, Electron `--trace-startup` and Chrome tracing, `process.memoryUsage()` per process, Windows Performance Analyzer, `perf`.
