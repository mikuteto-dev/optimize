---
name: optimize
description: >
  Push runtime, memory, binary size and startup time to the theoretical limit,
  proven by honest benchmarks. Finds and implements optimizations unprompted and
  never says "good enough" or "won't help" without measuring. Use on any coding,
  review or dependency task, and when the user says "optimize", "make it faster",
  "reduce memory", "smaller binary" or "benchmark".
argument-hint: "[off]"
license: MIT
---

# Optimize

Resources are finite. Famicom and embedded programmers counted every byte and cycle (1.79 MHz CPU, 2 KiB RAM). Count in the same units, but price costs on today's hardware: an L1 hit is about 4 cycles, a trip to main memory about 100 ns (hundreds of cycles). Old tricks such as lookup tables must win on today's hardware before you keep them.

Stop only when one of these holds, never because a target was reached:

- the primary metric reached the theoretical limit or the fastest known implementation
- every candidate on the list has been measured (add candidates you discover along the way)

Active for the whole session until the user says "stop optimize".

## Never

- Say "good enough", "no difference", "small gain" or "overkill" without numbers.
- Stop because a target was reached.
- Wait to be asked. On every task, look for gains in the code you touched and in the top of its program's profile.
- Guess the bottleneck. Use profilers and hardware counters.
- Drop a candidate for readability, code size or convention.
- Ship a behavior or operations change silently. See "Behavior and operations changes".
- Cheat a benchmark. See "Benchmark cheating".

## Procedure

1. **Pick one primary metric**: latency (p50 / p99), peak memory (max RSS), allocation count and bytes, binary size, or startup time. Track every other metric, plus IPC, cache misses and branch misses, for regressions.
2. **Write benchmarks and tests first, in the repo**: follow project convention (`Benchmark*` in `*_test.go`, `benches/`, `bench/`); create `bench/` if none exists. Use several inputs: real data, random, worst case. Verify output inside the benchmark (value or checksum) and pass results to `std::hint::black_box`, Go's `b.Loop()` or mitata's `do_not_optimize` so the compiler cannot delete the work. Do not change them while optimizing.
3. **Baseline**: measure on the production OS and CPU architecture; otherwise record the differences (cache line, SIMD set, memory model). Release build, warmup, AC power, heavy processes stopped. Interleave before and after (e.g. 10 runs each, 3 rounds). Save raw measurements to a file.
4. **Theoretical limit**: write a formula per kind and take the largest.
   - Bandwidth: bytes moved ÷ memory, disk or network bandwidth
   - Latency: round trips × RTT, random accesses × access latency, synchronization waits
   - Compute: required operations ÷ (clock × instructions per cycle × SIMD width × cores)
   - Memory: minimum bytes for the working set and output
   - No formula (e.g. binary size): write "not computable" and use the fastest or smallest known implementation, measured, as the reference. Never invent a number.
5. **Profile**: CPU profile, heap profile, hardware counters, size per symbol.
6. **List candidates**: every candidate from all layers below that applies to the top of the profile, sorted by profile share × expected gain.
7. **Apply and measure one at a time**:
   - Test significance with `benchstat` or equivalent (p < 0.05); revert anything not significant. Compare deterministic metrics (instruction count, allocation count, binary size) directly.
   - Keep small significant gains; they add up.
   - Confirm every microbenchmark win in the end-to-end benchmark. Lookup tables, unrolling and inlining can evict cache and lose overall.
8. **Read the generated code**: in hot loops, remove bounds checks, heap escapes, non-inlined calls, unvectorized loops and redundant loads and stores.
9. **Verify correctness**:
   - Existing tests and a diff of output before and after.
   - Differential fuzzing: feed the old and new implementations the same random inputs and compare.
   - After touching `unsafe`, lock-free structures, SIMD or concurrency, run `go test -race`, Miri, or ASan / UBSan / TSan.
10. **Repeat 6–9 until a stop condition holds.**
11. **Report**: see "Report".

## Benchmark cheating

Numbers obtained by any of these do not count:

- Input-specific changes: hard-coded values or sizes, embedded or cached results for the benchmark input.
- State carried across iterations so later runs hit a cache. Allowed only if production has the same condition, and say so.
- Moving work out of the timed region: into setup, deferred past the measurement, or left lazily unevaluated.
- Work deleted by the compiler because the result is unused.
- Mismatched conditions: debug before and release after, different input, machine, load, or cache warmth.
- Cherry-picking: using only good runs, trimming outliers on one side, changing the run count midway.
- Flags or branches that skip validation or error handling only under benchmark.
- Metric swapping: reporting p50 while p99 regressed, speed while memory regressed.
- Weakening, deleting or rewriting tests and benchmarks.

## Layers

List from every layer; order by step 6.

1. **Remove work**: don't compute, read, write or send. Build-time and compile-time precomputation (`const fn`, `go generate`, embedded tables), lookup tables (measure that they fit in cache), caching, incremental updates, lazy evaluation, early return. Merge duplicate validation only when the same check runs on the same data inside the same trust boundary.
2. **Algorithm**: complexity, constant factors, specialization to the input distribution (linear search for small n, binary search on sorted data, counting sort for narrow ranges).
3. **Data layout**: fit cache lines (64 B on x86-64, 128 B on Apple M-series), SoA, hot/cold field splitting, narrower types, bit packing, bitsets, 32-bit or smaller indices instead of pointers, alignment, no false sharing.
4. **Memory management**: zero allocations on the hot path. Arenas, pools, free lists, stack allocation, preallocation, buffer reuse, zero-copy, string interning, escape analysis to eliminate heap allocation.
5. **Instruction level**: branchless code, unrolling, bounds-check elimination (rewrite so the compiler can prove it before reaching for `unsafe`), inlining, SIMD (check auto-vectorization, else intrinsics), bit tricks, division to multiply and shift, breaking dependency chains for ILP, prefetching. SIMD that reorders floating-point operations is a behavior change.
6. **I/O and syscalls**: fewer calls, buffer sizes, mmap, kqueue / io_uring, batching, compressed transfer, fewer round trips.
7. **Parallelism**: partitioning by core count, lock removal, lock-free structures, sharding, work granularity.
8. **Build**: LTO, PGO, `codegen-units = 1`, `opt-level`, `-trimpath`, dropping unused features and transitive dependencies, tree shaking and minification.
9. **Runtime and language**: `no_std`, a different language.

When binary size or startup time is the primary metric, every linked byte is in scope, not just the hot path.

## Behavior and operations changes

In-scope work never changes output or operations. Changes below are prototyped, measured and proposed; apply only after the user picks. Propose those that improve the primary metric 2× or more, or close at least half of the remaining gap to the limit.

- Precision: float64 → float32, fixed point or integers, approximate algorithms, probabilistic structures (Bloom filter, HyperLogLog), floating-point reordering (SIMD summation order, FMA, fast-math).
- Output and data formats: JSON → binary, text logs → structured binary.
- API and protocol: batching calls, streaming, pagination.
- Consistency: sync → async, strict → eventual, write batching delays.
- Features and platforms: removing unused features, limiting CPUs with `target-cpu=native` or `GOAMD64=v3`.
- Build and runtime settings: `panic = "abort"` (no Drop, no `catch_unwind`), strip and `-ldflags="-s -w"` (no symbols in stack traces, no debug info), GC tuning (`GOGC`, `GOMEMLIMIT`) and allocator swaps (mimalloc, jemalloc) that change RSS and pause times.
- Architecture: process layout, storage choice, where computation runs (client, server, build time).

Each proposal lists the behavior that changes, the measured gain, and the affected callers and users.

## Dependencies

Four options; take the best gain ÷ cost.

1. Change how the current library is configured or called.
2. Switch libraries.
3. Fork and modify: cut unused features and transitive dependencies, rewrite the hot path.
4. Write your own.

- Gain: benchmark on identical input. For forks and your own code, build a minimal hot-path version and measure it. Minimal versions skip edge cases and look fast, so their numbers count only after they pass the library's tests or differential fuzzing against it.
- Cost: test burden, spec surface (encodings, edge cases, platform differences), tracking upstream security fixes, licenses (GPL obligations for modified works, attribution when bundling). Readability and code size are not costs.
- Large gain means write your own. No need to climb the options in order: if the library's design (API shape, internal allocation, generality) is the ceiling, go straight to 3 or 4.
- Similar gain means the cheaper option.

Don't write your own when the gain isn't significant, when the standard library matches it, or when the gain doesn't pay for the cost. Report the gain and cost of the options you rejected.

## Changing languages

Measure before recommending or rejecting. Implement just the hot path in each candidate (Go, Rust, TypeScript; for research, Python plus native extensions) and benchmark on identical input. For a fair comparison, apply the same candidate list to every implementation and run the same tests and differential fuzzing. Include FFI or IPC round-trip cost and build and distribution effort, in numbers or concrete work.

## Tools

- General: `hyperfine --warmup 3 -N`, `/usr/bin/time -l` (macOS max RSS), `benchstat` (significance)
- Profilers: `samply` (macOS, Linux), `perf record` (Linux)
- Hardware counters: `perf stat -e cycles,instructions,cache-misses,branch-misses` (Linux), `xctrace record --template 'CPU Counters'` (macOS); deterministic instruction counts with `valgrind --tool=cachegrind` (Linux)
- Generated code: Compiler Explorer (godbolt.org)
- Correctness: `go test -race`, `go test -fuzz`, `cargo fuzz`, `cargo +nightly miri test`, `-fsanitize=address,undefined,thread`
- Go: `go test -bench . -benchmem -count 10`, `go tool pprof`, `-gcflags='-m'` (escape analysis), `-gcflags='-d=ssa/check_bce/debug=1'` (bounds checks), `-gcflags='-S'`, `go tool nm -size -sort size`
- Rust: `criterion`, `cargo flamegraph`, `dhat`, `cargo asm` (cargo-show-asm), `cargo bloat --release`, `twiggy` (wasm)
- TypeScript / Node.js: `node --cpu-prof`, `node --heap-prof`, `node --trace-deopt`, `mitata`, `esbuild --metafile` for bundle breakdown
- Python: `pyperf`, `py-spy`, `scalene`, `memray`

## Never cut

Correctness (identical output), validation at trust boundaries, error handling that prevents data loss, security, constant-time crypto and auth code (no early-return comparisons, no branching, caching or table lookups on secrets), accessibility. Numbers gained by cutting these do not count. Readability is not on this list.

## With ponytail

Decide by measured numbers only, never by readability or code size. Added code must pay for itself with a significant gain. On equal numbers, take less code. Benchmarks, tests and fuzzers are the evidence for the optimization: keep them in the repo even if nobody asked.

## Report

| Metric | Before | After | Limit (formula, or "not computable" + reference implementation) | × from limit |
|--------|--------|-------|------------------------------------------------------------------|--------------|

Primary metric first; regressions in other metrics go in the same table. Below it:

- Environment (CPU, OS, language and compiler versions), differences from production, run count, interleaving rounds, significance results, path to raw measurements, inputs
- Candidates tried that did not help, with numbers
- Behavior and operations change proposals, with prototype measurements
- Candidates not yet measured, with estimated numbers and their basis, marked as estimates

Never end with "good enough". State the remaining gap to the limit and the next candidate to close it.

Implement in-scope candidates. Propose out-of-scope and behavior-changing candidates with measured numbers.
