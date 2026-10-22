---
name: optimize
description: Drive runtime, memory, size, latency, energy or cost toward the theoretical limit with measured, reproducible evidence. Use when code, sites, services, databases or assets can get faster or lighter, or when asked to optimize, speed up, shrink or benchmark.
argument-hint: "[off]"
license: MIT
hooks:
  Stop:
    - hooks:
        - type: command
          command: 'for d in "$CLAUDE_PROJECT_DIR/.claude/skills/optimize" "$HOME/.claude/skills/optimize"; do [ -f "$d/scripts/gate.py" ] && exec python3 "$d/scripts/gate.py" --hook; done; exit 0'
---

# Optimize

The user wants every resource treated as scarce, the way Famicom and embedded programmers counted every byte and cycle. You already know the techniques; studies of coding agents on optimization tasks show the failures are elsewhere, and this skill is built around them:

- Agents accept the first measurable speedup and stop (SWE-fficiency; in GSO 75% of runs ended before 100 of 200+ allowed steps).
- They prefer shortcuts (caches, fast paths for the benchmark input, compiler flags) over structural changes, and avoid the lower layer even when the gain lives there (GSO).
- They list many techniques but test few distinct ones and converge on the first (InferenceBench).
- They tamper with timers, cache results across timed runs, and hard-code test inputs; asking them not to cheat barely changes the rate, while hardening the harness removes most of it (METR, Reward Hacking Benchmark, PerfAgent).
- Profiler instructions in a prompt did not help; a loop that always profiles and feeds results back doubled expert-level results (PerfAgent).

So the evidence and the stopping rule live in files and scripts, not in your judgment of when you are done.

Active until the user says "stop optimize".

## Ledger and gate

Work in `bench/` in the repo; it survives compaction and is the evidence.

- `bench/candidates.md`: a table with columns `candidate | area | kind | status | before | after | p | raw`. `kind` is `structural` or `shortcut`; `status` is `untested`, `kept`, `reverted` or `needs user`; `raw` is the file `bench.py` wrote.
- Before the first change, write the benchmark and correctness check, then lock them: `python3 ${CLAUDE_SKILL_DIR}/scripts/bench.py lock <globs>`.
- Measure every candidate with `python3 ${CLAUDE_SKILL_DIR}/scripts/bench.py run --name <candidate> --before '<old cmd> {input}' --after '<new cmd> {input}' --input <file> --gen '<generator> --seed {seed} --out {out}'`. It interleaves before and after, adds an input from a new random seed every time, checks every run's output against the old implementation, logs raw rows, and reports medians, gain and p. A mismatch means the candidate does not count. For anything that is not a command reading `{input}` (a page, a service, a query, a binary's size, a microbenchmark), pass `--measure '<locked script>'` that prints a JSON object of numbers, and `--check '<cmd>'` for how outputs are compared; each checklist shows its field's form, and [references/benchmarking.md](references/benchmarking.md) has the contract.
- A Stop hook runs `scripts/gate.py`. It blocks ending while any row is `untested`, a kept row lacks raw data newer than the lock, locked files changed, or there is no `Verified:` line. Run it yourself any time: `python3 ${CLAUDE_SKILL_DIR}/scripts/gate.py`.

## Working the list

1. Profile first, then build the list from [references/any-system.md](references/any-system.md); several systems: [references/cross-domain.md](references/cross-domain.md); check for missing categories against [references/checklists/](references/checklists/).
2. Before converging, prototype at least three structurally different strategies (different algorithm, data layout, language or library, architecture) and measure each. When subagents are available, run independent strategies in parallel; parallel attempts beat longer single attempts in GSO.
3. A `shortcut` row stays only if it holds on the generated inputs and the change is still correct for every valid input; prefer the structural change that removes the cost.
4. Include the lower layer (native code, SIMD, the database, the GPU) when the profile points there.
5. Keep small significant gains; they compound. Readability and code size do not decide; on equal numbers the smaller code wins.
6. Dependencies, writing your own (large gain means write your own), and language comparisons: [references/changes.md](references/changes.md). Measurement details: [references/benchmarking.md](references/benchmarking.md). Commands: [references/tools.md](references/tools.md).

## Done

The primary metric reached its limit (a written formula, or the best known implementation measured), or `gate.py` passes with no `untested` rows. Before that, have a fresh context (a subagent) rerun the benchmark and output comparison from the ledger alone and record `Verified: <who> <date> <result>`. A milestone or a large win is not done.

## Needs the user

Apply on your own only what keeps output, guarantees and what users see identical. Prototype and measure changes to precision, formats, APIs, consistency or durability, schema, visual quality, supported platforms, operational settings, architecture or infrastructure; mark them `needs user` and propose those worth 2× or more, or at least half the remaining gap. Correctness, validation at trust boundaries, data-loss handling, security, constant-time crypto code and accessibility stay intact.

## Report

A table from the ledger: metric, before, after, limit, × from the limit, one row per tier across systems. Then the environment and differences from production, rejected candidates with numbers, `needs user` proposals, and the remaining gap with the next candidate.
