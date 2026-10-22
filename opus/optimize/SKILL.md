---
name: optimize
description: Drive runtime, memory, size, latency, energy or cost toward the theoretical limit with measured, reproducible evidence. Use when code, sites, services, databases or assets can get faster or lighter, or when asked to optimize, speed up, shrink or benchmark.
argument-hint: "[off]"
license: MIT
---

# Optimize

The user wants every resource treated as scarce, the way Famicom and embedded programmers counted every byte and cycle. You already know the techniques. This skill exists because agents fail at this work in predictable ways: they stop after the first win, call code good enough without measuring, reject other languages, libraries or their own implementation without trying them, tune to the benchmark input, and quote numbers no file backs. The rules below close those gaps.

Active until the user says "stop optimize".

## Ledger

Keep the work in `bench/` in the repo. Files survive context compaction, and they are the evidence for every claim.

- `bench/candidates.md`: one row per candidate with its area, hypothesis, status (`untested`, `kept`, `reverted`, `needs user`), before, after, significance, and the raw-data file.
- The benchmark, the correctness check, and the raw measurements.

Create the ledger before the first change and update it after every measurement.

## Done

Done means the primary metric has reached its limit (a written formula, or the best known implementation measured), or no row is `untested`. Add rows as you discover candidates. A milestone, a large win, or a long turn is not done: if you are about to end with a summary that names the next candidate, measure it instead. Stop for the user only when a `needs user` row blocks the remaining work, or something else blocks you.

## Evidence

- The primary metric is what the user or payer feels end to end; check the others for regressions.
- Every number you report comes from a file in `bench/` written by a command you ran.
- Before and after use the same build mode, machine and inputs, run interleaved, with a significance test.
- Inputs include real data, worst cases, and random data regenerated with a new seed each round, and the benchmark checks output against the old implementation, so a change tuned to one input fails.
- Before reporting, have a fresh context (a subagent, or a new session) rerun the benchmark and the output comparison using only the ledger.

Readability and code size do not decide; measured numbers do, and on equal numbers the smaller code wins.

## Building the list

- Any system: [references/any-system.md](references/any-system.md). Several systems: [references/cross-domain.md](references/cross-domain.md).
- To catch missing categories: [references/checklists/](references/checklists/) (program layers, then one file per field).
- Dependencies (configure, switch, fork, write your own; large gain means write your own) and language comparisons: [references/changes.md](references/changes.md).
- Measurement details and what does not count: [references/benchmarking.md](references/benchmarking.md). Commands: [references/tools.md](references/tools.md).

## Needs the user

Apply on your own only what keeps output, guarantees and what users see identical. Prototype and measure changes to precision, formats, APIs, consistency or durability, schema, visual quality, supported platforms, operational settings, architecture or infrastructure; mark them `needs user` and propose those worth 2× or more, or at least half the remaining gap. Correctness, validation at trust boundaries, data-loss handling, security, constant-time crypto code and accessibility stay intact.

## Report

A table from the ledger: metric, before, after, limit, and × from the limit, with one row per tier when several systems are involved. Then the environment and its differences from production, rejected candidates with their numbers, `needs user` proposals, and the remaining gap with the next candidate.
