---
name: optimize
description: Optimize runtime, memory, binary size or startup time toward the theoretical limit, with benchmarks that prove each gain. Use when writing, reviewing or choosing dependencies for code whose performance or footprint can improve, or when asked to optimize, speed up, shrink or benchmark.
argument-hint: "[off]"
license: MIT
---

# Optimize

The user wants software that uses as little time, memory and space as the hardware allows, the way Famicom and embedded programmers counted every byte and cycle. They have watched agents call code "good enough", reject a language change without measuring it, and wait to be asked. So on every task you touch, look for gains yourself, measure them, and keep going until the evidence says there is nothing left worth taking.

Active until the user says "stop optimize".

## What done means

The task ends when one of these holds, not when a target or a first speedup is reached:

- the primary metric is at the theoretical limit, or at the fastest known implementation of the same job, or
- every candidate on your list has been measured, including ones you found along the way.

A long turn, a finished milestone, or a big first win is not a reason to stop and report. If you are about to end with a summary that names the next optimization, run that optimization instead. Stop to ask only when the next step needs the user's choice (see "Changes that need the user") or something blocks you.

## How to work

1. **Measure before changing anything.** Pick one primary metric (p50 / p99 latency, max RSS, allocations, binary size, startup) and watch the others for regressions. Write the benchmark and its correctness check first and keep them in the repo; they are the evidence for every later claim. Details: [references/benchmarking.md](references/benchmarking.md).
2. **Compute the limit.** Write the formula (bytes ÷ bandwidth, round trips × latency, operations ÷ throughput, minimum bytes). Where no formula exists, write "not computable" and measure the best known implementation instead. A made-up limit misleads every decision after it.
3. **Profile, then list candidates.** Use profilers and hardware counters rather than intuition; editing before profiling spends effort on code that may not matter. List candidates from every layer in [references/layers.md](references/layers.md) that apply to the top of the profile, ordered by profile share × expected gain.
4. **One change, one measurement.** Keep a change only if the gain is statistically significant; keep small significant gains, since they compound. Confirm microbenchmark wins end to end, because lookup tables, unrolling and inlining can evict cache and lose overall. Read the generated assembly of hot loops.
5. **Prove the output is unchanged.** Run the tests, diff outputs, and differentially fuzz the old implementation against the new one. After `unsafe`, SIMD, lock-free code or concurrency, run the race detector or sanitizers. The solution must be correct for every valid input, not only the benchmark input.

Readability, code size and convention are not reasons to drop a candidate; the user has said so explicitly. Measured numbers decide. Added code earns its place with a significant gain, and on equal numbers the smaller code wins.

## Honest numbers

The user expects benchmark gaming to happen and wants none of it. A number counts only if the benchmark input, conditions and timed region are the same before and after, the work is not hard-coded for the benchmark input, moved out of the timed region, or deleted by the compiler, and every run is reported. The full list of what does not count is in [references/benchmarking.md](references/benchmarking.md).

## Changes that need the user

Keep output and operational behavior identical for anything you apply on your own. Some of the largest wins change behavior: precision, output or data formats, APIs, consistency, supported CPUs, panic or debug-info settings, GC and allocator settings, architecture. Prototype and measure those, then propose the ones that improve the primary metric 2× or more or close at least half the remaining gap, and apply them after the user picks. The list and the proposal format are in [references/changes.md](references/changes.md).

For dependencies, compare configuring the current library, switching, forking and trimming, and writing your own, and take the best gain ÷ cost. Write your own when the gain is large. For language changes, implement the hot path in each candidate and measure before recommending or rejecting. Both are in [references/changes.md](references/changes.md).

Correctness, validation at trust boundaries, error handling that prevents data loss, security, constant-time crypto and auth code, and accessibility stay intact; numbers gained by cutting them do not count.

## Report

Lead with a table: metric, before, after, limit (with its formula or reference implementation), and × from the limit. The primary metric goes first, and regressions in other metrics go in the same table. Then list the environment and its differences from production, run counts and significance, candidates that did not help with their numbers, proposals that need the user, and unmeasured candidates marked as estimates. End with the remaining gap and the next candidate, not with "good enough".

Tool commands per language: [references/tools.md](references/tools.md).
