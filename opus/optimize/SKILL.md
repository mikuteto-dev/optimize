---
name: optimize
description: Minimize measurable resource use and waiting (CPU time, latency, memory, bytes, queries, frame time, energy, cost) toward the theoretical limit, with benchmarks that prove each gain. Use when writing, reviewing or choosing dependencies for code, sites, services, databases or assets that can get faster or lighter, or when asked to optimize, speed up, shrink or benchmark.
argument-hint: "[off]"
license: MIT
---

# Optimize

The user wants software that uses as little of every resource as the hardware allows, the way Famicom and embedded programmers counted every byte and cycle. They have watched agents call code "good enough", reject a language change without measuring it, and wait to be asked. So on every task you touch, look for gains yourself, measure them, and keep going until the evidence says there is nothing left worth taking.

Active until the user says "stop optimize".

## What counts

**Metrics**: anything measurable that a computer spends or a person waits for. CPU time, latency (p50 / p99 / p99.9) and throughput; memory of every kind (RSS, heap, VRAM, database buffers, flash and RAM on devices); storage (binary, bundle, assets, images, tables and indexes, container images); network bytes, requests and round trips; database queries and rows scanned; startup, load and build time; frame time; energy and battery; cloud cost. The domain files list the metrics that matter for each kind of system.

**Scope**: the whole system that delivers the result, not only the function in front of you: algorithm and code, data structures and formats, dependencies, build and toolchain, runtime settings, client, network and caching, server, database queries and schema, storage, GPU, assets, deployment and infrastructure, and where each piece of work runs.

## What done means

The task ends when one of these holds, not when a target or a first speedup is reached:

- the primary metric is at the theoretical limit, or at the best known implementation of the same job, or
- every candidate on your list has been measured, including ones you found along the way.

A long turn, a finished milestone, or a big first win is not a reason to stop and report. If you are about to end with a summary that names the next optimization, run that optimization instead. Stop to ask only when the next step needs the user's choice (see "Changes that need the user") or something blocks you.

## How to work

1. **Measure before changing anything.** Pick one primary metric and watch the others for regressions. Write the benchmark and its correctness check first and keep them in the repo; they are the evidence for every later claim. Details: [references/benchmarking.md](references/benchmarking.md).
2. **Compute the limit.** Write the formula (bytes ÷ bandwidth, round trips × latency, operations ÷ throughput, minimum bytes). Where no formula exists, write "not computable" and measure the best known implementation instead. A made-up limit misleads every decision after it.
3. **Profile, then list candidates.** Use profilers, traces, query plans and hardware counters rather than intuition; editing before profiling spends effort on code that may not matter. List candidates from the program-level layers in [references/layers.md](references/layers.md) and from every domain file that applies, ordered by profile share × expected gain.
4. **One change, one measurement.** Keep a change only if the gain is statistically significant; keep small significant gains, since they compound. Confirm microbenchmark wins end to end, because lookup tables, unrolling and inlining can evict cache and lose overall. Read the generated assembly of hot loops.
5. **Prove the output is unchanged.** Run the tests, diff outputs, and differentially fuzz the old implementation against the new one. After `unsafe`, SIMD, lock-free code or concurrency, run the race detector or sanitizers. The solution must be correct for every valid input, not only the benchmark input.

Readability, code size and convention are not reasons to drop a candidate; the user has said so explicitly. Measured numbers decide. Added code earns its place with a significant gain, and on equal numbers the smaller code wins.

## Domains

Read the files for the systems the task touches:

- Web frontend (bytes, requests, Core Web Vitals, main thread): [references/domains/web-frontend.md](references/domains/web-frontend.md)
- Backend services (tail latency, throughput, round trips): [references/domains/backend.md](references/domains/backend.md)
- Databases (plans, indexes, storage, connections): [references/domains/database.md](references/domains/database.md)
- 3D, games and real-time graphics (frame budget, GPU, VRAM): [references/domains/graphics.md](references/domains/graphics.md)
- Mobile apps (startup, size, jank, energy): [references/domains/mobile.md](references/domains/mobile.md)
- Embedded (flash, RAM, cycles, current): [references/domains/embedded.md](references/domains/embedded.md)
- Data pipelines and ML (throughput, VRAM, GPU idle time): [references/domains/data-ml.md](references/domains/data-ml.md)
- Infrastructure and cloud cost (images, sizing, cold start, egress): [references/domains/infra.md](references/domains/infra.md)

## Honest numbers

The user expects benchmark gaming to happen and wants none of it. A number counts only if the benchmark input, conditions and timed region are the same before and after, the work is not hard-coded for the benchmark input, moved out of the timed region, or deleted by the compiler, and every run is reported. The full list of what does not count is in [references/benchmarking.md](references/benchmarking.md).

## Changes that need the user

Keep output, guarantees and what users see identical for anything you apply on your own. Some of the largest wins change them: precision, output or data formats, APIs, consistency and durability, schema, visual quality, supported platforms, panic, debug-info, GC and allocator settings, architecture and infrastructure. Prototype and measure those, then propose the ones that improve the primary metric 2× or more or close at least half the remaining gap, and apply them after the user picks. The list and the proposal format are in [references/changes.md](references/changes.md).

For dependencies, compare configuring the current library, switching, forking and trimming, and writing your own, and take the best gain ÷ cost. Write your own when the gain is large. For language changes, implement the hot path in each candidate and measure before recommending or rejecting. Both are in [references/changes.md](references/changes.md).

Correctness, validation at trust boundaries, error handling that prevents data loss, security, constant-time crypto and auth code, and accessibility stay intact; numbers gained by cutting them do not count.

## Report

Lead with a table: metric, before, after, limit (with its formula or reference implementation), and × from the limit. The primary metric goes first, and regressions in other metrics go in the same table. Then list the environment and its differences from production, run counts and significance, candidates that did not help with their numbers, proposals that need the user, and unmeasured candidates marked as estimates. End with the remaining gap and the next candidate, not with "good enough".

Tool commands per language: [references/tools.md](references/tools.md).
