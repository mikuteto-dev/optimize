---
name: optimize
description: Drive runtime, memory, size, latency, energy or cost toward the theoretical limit with measured, reproducible evidence. Use when code, sites, services, databases or assets can get faster or lighter, or when asked to optimize, speed up, shrink or benchmark.
argument-hint: "[off]"
license: MIT
---

# Optimize

Treat every resource as scarce, the way Famicom and embedded programmers did. Studies of coding agents on optimization tasks find the gap is not knowledge but follow-through: agents accept the first measurable speedup, prefer shortcuts and benchmark-specific fast paths over structural changes, test few distinct strategies, and game timers and caches across runs; prompts asking them not to do this barely help, while scripted measurement and gates do. This skill therefore puts the evidence and the stopping rule into bundled scripts. Readability and code size do not decide; measured numbers do.

Active until the user says "stop optimize". `scripts/` below means the `scripts` directory next to this file.

## Done

`python3 scripts/gate.py` prints `ok`: no `untested` row in `bench/candidates.md`, every kept row has raw data newer than the benchmark lock, locked files are unchanged, and a `Verified:` line records a rerun from a fresh context. Or the primary metric reached its limit (a written formula, or the best known implementation measured). Run the gate before you report; if it lists open items, keep working on them. Come back to the user only for `needs user` rows that block the rest.

## Permissions

Local and reversible, so go ahead without asking: build, run benchmarks, load tests, profilers and query plans against local or disposable environments, write scratch files, add benchmark, test, fuzz and ledger files to the repo, rewrite the implementation in another language or on another library, revert what did not help, and start a fresh context or subagent to recheck results.

## Ledger and measurement

- `bench/candidates.md`: columns `candidate | area | kind | status | before | after | p | raw`; `kind` is `structural` or `shortcut`; `status` is `untested`, `kept`, `reverted` or `needs user`.
- Lock the benchmark, tests, generators and reference before the first change: `python3 scripts/bench.py lock <globs>`.
- Measure each candidate: `python3 scripts/bench.py run --name <candidate> --before '<old cmd> {input}' --after '<new cmd> {input}' --input <file> --gen '<generator> --seed {seed} --out {out}'`. Fresh process per run, interleaved, a new random-seed input every time, outputs compared with the old implementation, medians, max RSS and p reported. A mismatch does not count. For pages, services or queries, use the field's tool and write raw results to `bench/runs/`.

## Good work

- Profile first. Prototype at least three structurally different strategies before converging, in parallel subagents when available.
- Shortcuts stay only if they hold on generated inputs and remain correct for every valid input; prefer the structural change.
- Go to the lower layer (native code, SIMD, database, GPU) when the profile points there.
- Keep small significant gains; on equal numbers the smaller code wins.

## Where to look

- Any system: [references/any-system.md](references/any-system.md). Several systems: [references/cross-domain.md](references/cross-domain.md).
- Category checklists: [references/checklists/](references/checklists/).
- Dependencies, writing your own, and language comparisons: [references/changes.md](references/changes.md).
- Measurement details and what does not count: [references/benchmarking.md](references/benchmarking.md). Commands: [references/tools.md](references/tools.md).

## The user's decisions

Apply what keeps output, guarantees and what users see identical. Changes to precision, formats, APIs, consistency or durability, schema, visual quality, supported platforms, operational settings, architecture or infrastructure are the user's call: prototype, measure, mark `needs user`, and propose those worth 2× or more or at least half the remaining gap. Validation at trust boundaries, data-loss handling, security, constant-time crypto code and accessibility stay intact.

## Report

A table from the ledger (metric, before, after, limit, × from the limit; one row per tier across systems), then the environment, rejected candidates with numbers, proposals for the user, and the remaining gap with the next candidate.
