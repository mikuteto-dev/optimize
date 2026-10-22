---
name: optimize
description: Drive runtime, memory, size, latency, energy or cost toward the theoretical limit with measured, reproducible evidence. Use when code, sites, services, databases or assets can get faster or lighter, or when asked to optimize, speed up, shrink or benchmark.
argument-hint: "[off]"
license: MIT
---

# Optimize

Treat every resource as scarce, the way Famicom and embedded programmers did. Find gains on your own, back each one with a measurement, and carry the work through to the limit rather than the first speedup. Readability and code size do not decide; measured numbers do, and on equal numbers the smaller code wins.

Active until the user says "stop optimize".

## Ledger

Keep the work in `bench/` in the repo so it survives compaction and serves as evidence: `bench/candidates.md` with one row per candidate (area, hypothesis, status `untested` / `kept` / `reverted` / `needs user`, before, after, significance, raw-data file), plus the benchmark, the correctness check, and raw measurements. Create it before the first change; update it after every measurement.

## Done

The primary metric has reached its limit (a written formula, or the best known implementation measured), or no row is `untested`. Keep adding rows as you find candidates. A target, a milestone or a large first win is not done. Come back to the user when a `needs user` row blocks the rest.

## Permissions

Local and reversible, so go ahead without asking: build, run benchmarks, load tests, profilers and query plans against local or disposable environments, write scratch files, add benchmark, test, fuzz and ledger files to the repo, rewrite the implementation in another language or on another library, revert what did not help, and start a fresh context to recheck results.

## Good evidence

- A primary metric the user or payer feels end to end, with the others checked for regressions.
- Every reported number traceable to a file in `bench/` from a command you ran.
- Same build mode, machine and inputs before and after, interleaved, with a significance test.
- Real, worst-case and freshly seeded random inputs, with output checked against the old implementation.
- A rerun of the benchmark and output comparison from a fresh context, using only the ledger.

## Where to look

- Any system: [references/any-system.md](references/any-system.md). Several systems: [references/cross-domain.md](references/cross-domain.md).
- Category checklists (program layers, then per field): [references/checklists/](references/checklists/).
- Dependencies, writing your own, and language comparisons: [references/changes.md](references/changes.md).
- Measurement details and what does not count: [references/benchmarking.md](references/benchmarking.md). Commands: [references/tools.md](references/tools.md).

## The user's decisions

Apply what keeps output, guarantees and what users see identical. Changes to precision, formats, APIs, consistency or durability, schema, visual quality, supported platforms, operational settings, architecture or infrastructure are the user's call: prototype, measure, mark `needs user`, and propose those worth 2× or more or at least half the remaining gap. Validation at trust boundaries, data-loss handling, security, constant-time crypto code and accessibility stay intact.

## Report

A table from the ledger (metric, before, after, limit, × from the limit; one row per tier across systems), then the environment, rejected candidates with numbers, proposals for the user, and the remaining gap with the next candidate.
