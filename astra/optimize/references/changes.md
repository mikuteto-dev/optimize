# Changes beyond the implementation

## Behavior and operations changes

These change what users or operators observe, so prototype, measure and propose them; apply only after the user picks. Propose those that improve the primary metric 2× or more, or close at least half of the remaining gap to the limit.

- Precision: float64 → float32, fixed point or integers, approximate algorithms, probabilistic structures (Bloom filter, HyperLogLog), floating-point reordering (SIMD summation order, FMA, fast-math).
- Output and data formats: JSON → binary, text logs → structured binary.
- API and protocol: batching calls, streaming, pagination.
- Consistency: sync → async, strict → eventual, write batching delays.
- Features and platforms: removing unused features, limiting CPUs with `target-cpu=native` or `GOAMD64=v3`.
- Build and runtime settings: `panic = "abort"` (no Drop, no `catch_unwind`), strip and `-ldflags="-s -w"` (no symbols in stack traces, no debug info), GC tuning (`GOGC`, `GOMEMLIMIT`) and allocator swaps (mimalloc, jemalloc) that change RSS and pause times.
- Durability and guarantees: fsync and commit settings, isolation levels, replication acknowledgment, retention periods.
- What users see: image and texture quality, fonts, animations, render resolution and upscaling, LOD distances, supported browsers, OS versions and devices.
- Schema and data model: migrations, denormalization that changes write paths.
- Architecture: process layout, storage and database choice, where computation runs (client, edge, server, build time), CPU architecture and region of the infrastructure.

Each proposal states the behavior that changes, the measured gain, and the affected callers and users.

## Dependencies

Four options; take the best gain ÷ cost, without climbing them in order. If the library's design (API shape, internal allocation, generality) is the ceiling, go straight to forking or writing your own.

1. Configure or call the current library differently.
2. Switch libraries.
3. Fork and modify: cut unused features and transitive dependencies, rewrite the hot path.
4. Write your own.

- Gain: benchmark on identical input. Minimal hot-path prototypes skip edge cases and look faster than they are, so their numbers count only after they pass the library's tests or differential fuzzing against it.
- Cost: test burden, spec surface (encodings, edge cases, platform differences), tracking upstream security fixes, licenses (GPL obligations for modified works, attribution when bundling). Readability and code size are not costs.
- Large gain: write your own. Similar gain: the cheaper option. No significant gain, or the standard library matches it: keep what exists.

Report the gain and cost of the options you rejected.

## Changing languages

Measure before recommending or rejecting. Implement the hot path in each candidate (Go, Rust, TypeScript; for research, Python plus native extensions) and benchmark on identical input. For a fair comparison, apply the same candidate list to every implementation and run the same tests and differential fuzzing. Include FFI or IPC round-trip cost and build and distribution effort.
