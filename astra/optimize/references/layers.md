# Layers

These are the program-level layers that apply to any code. The levers outside the program (client, network, database, GPU, devices, infrastructure) are in [domains/](domains/).

List candidates from every layer, then order them by profile share × expected gain. Price costs on today's hardware: an L1 hit is about 4 cycles and a trip to main memory about 100 ns, so old tricks such as lookup tables must win in measurement before they stay.

1. **Remove work**: don't compute, read, write or send. Build-time and compile-time precomputation (`const fn`, `go generate`, embedded tables), lookup tables that fit in cache, caching, incremental updates, lazy evaluation, early return. Merge duplicate validation only when the same check runs on the same data inside the same trust boundary.
2. **Algorithm**: complexity, constant factors, specialization to the input distribution (linear search for small n, binary search on sorted data, counting sort for narrow ranges).
3. **Data layout**: fit cache lines (64 B on x86-64, 128 B on Apple M-series), SoA, hot/cold field splitting, narrower types, bit packing, bitsets, 32-bit or smaller indices instead of pointers, alignment, no false sharing.
4. **Memory management**: zero allocations on the hot path. Arenas, pools, free lists, stack allocation, preallocation, buffer reuse, zero-copy, string interning, escape analysis.
5. **Instruction level**: branchless code, unrolling, bounds-check elimination (rewrite so the compiler can prove it before reaching for `unsafe`), inlining, SIMD (check auto-vectorization, else intrinsics), bit tricks, division to multiply and shift, breaking dependency chains, prefetching. SIMD that reorders floating-point operations changes output and needs the user.
6. **I/O and syscalls**: fewer calls, buffer sizes, mmap, kqueue / io_uring, batching, compressed transfer, fewer round trips.
7. **Parallelism**: partitioning by core count, lock removal, lock-free structures, sharding, work granularity.
8. **Build**: LTO, PGO, `codegen-units = 1`, `opt-level`, `-trimpath`, dropping unused features and transitive dependencies, tree shaking and minification.
9. **Runtime and language**: `no_std`, a different language.

When binary size or startup time is the primary metric, every linked byte is in scope, not just the hot path.
