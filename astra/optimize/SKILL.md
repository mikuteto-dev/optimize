---
name: optimize
description: Minimize measurable resource use and waiting (CPU time, latency, memory, bytes, queries, frame time, energy, cost) toward the theoretical limit, with benchmarks that prove each gain. Use when writing, reviewing or choosing dependencies for code, sites, services, databases or assets that can get faster or lighter, or when asked to optimize, speed up, shrink or benchmark.
argument-hint: "[off]"
license: MIT
---

# Optimize

Treat every resource as scarce, the way Famicom and embedded programmers did. Look for gains on your own, back every claim with a measurement, and keep going past the first speedup. Readability and code size do not count against a candidate; measured numbers decide, and on equal numbers the smaller code wins.

Active until the user says "stop optimize".

## What counts

Any metric a computer spends or a person waits for: CPU time, latency and throughput, memory of every kind (RSS, heap, VRAM, database buffers, device RAM and flash), storage and transfer size (binaries, bundles, assets, tables, indexes, images), requests and round trips, queries and rows scanned, startup, load and build time, frame time, energy, cloud cost.

The scope is the whole system that delivers the result: code, data formats, dependencies, build, runtime settings, client, network and caching, server, database, storage, GPU, assets, infrastructure, and where each piece of work runs.

## Done

Keep working until the primary metric reaches the theoretical limit (or the best known implementation of the same job), or every candidate you listed has been measured. Reaching a target, a milestone or a large first win is not done. Stop early only for a decision that belongs to the user.

## Permissions

These are local and reversible, so do them without asking: build, run benchmarks, load tests, profilers and query plans against local or disposable environments, write scratch files, add benchmark, test and fuzz files to the repo, rewrite the implementation in another language or on another library, and revert changes that did not help.

## What good evidence looks like

- One primary metric, with the others checked for regressions.
- A written limit: a formula, or "not computable" plus a measured reference implementation.
- Before and after on the same input, build and machine, interleaved, with a significance test; microbenchmark wins confirmed end to end.
- Identical output on every valid input, shown by tests and differential fuzzing against the old implementation.
- Validation at trust boundaries, error handling that prevents data loss, security, constant-time crypto and auth code, and accessibility left intact.
- No benchmark gaming: [references/benchmarking.md](references/benchmarking.md) lists what does not count.

## Where to look

- Program-level layers, from removing work to changing languages: [references/layers.md](references/layers.md)
- The systems the task touches: [web frontend](references/domains/web-frontend.md), [backend](references/domains/backend.md), [database](references/domains/database.md), [3D and games](references/domains/graphics.md), [mobile](references/domains/mobile.md), [embedded](references/domains/embedded.md), [data and ML](references/domains/data-ml.md), [infrastructure and cost](references/domains/infra.md)
- Dependencies (configure, switch, fork, write your own) and language comparisons: [references/changes.md](references/changes.md)
- Commands per language: [references/tools.md](references/tools.md)

## The user's decisions

Apply anything that keeps output, guarantees and what users see identical. Changes to precision, output or data formats, APIs, consistency or durability, schema, visual quality, supported platforms, panic or debug-info settings, GC or allocator settings, architecture or infrastructure are the user's call: prototype them, and propose those worth 2× or more on the primary metric or at least half the remaining gap. See [references/changes.md](references/changes.md).

## Report

A table of metric, before, after, limit and × from the limit, primary metric first and regressions included. Then the environment, run counts and significance, what did not help, proposals for the user, and the remaining gap with the next candidate.
