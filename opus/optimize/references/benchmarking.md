# Benchmarking

## Setup

- Put benchmarks and tests where the project keeps them (`Benchmark*` in `*_test.go`, `benches/`, `bench/`); create `bench/` if there is nothing. They stay in the repo so later changes can be checked against them.
- Use several inputs: real data, random, worst case.
- Verify the output inside the benchmark (value or checksum), and pass results to `std::hint::black_box`, Go's `b.Loop()` or mitata's `do_not_optimize` so the compiler cannot delete the work.
- Freeze the benchmarks and tests before optimizing. Changing them mid-way makes before and after incomparable. For random inputs, freeze the generator and change only the seed each round.

## Measuring

- Measure on the production OS and CPU architecture. If you cannot, record the differences (cache line size, SIMD set, memory model), because results may not transfer.
- Release build, warmup, AC power, heavy processes stopped.
- Interleave before and after (e.g. 10 runs each, 3 rounds) so drift and thermal throttling hit both equally.
- Save raw measurements to a file.
- Decide with a significance test (`benchstat`, p < 0.05). Deterministic metrics (instruction count, allocation count, binary size) can be compared directly.

## scripts/bench.py

`bench.py` owns how numbers are counted; the field's own tool owns how they are measured. It interleaves before and after in random order, adds an input from a new random seed on every invocation (`--gen`), checks every run's output against the old implementation, writes raw rows to `bench/runs/`, and reports medians, gain and Mann-Whitney p for every metric.

Three ways to measure:

1. **A command that reads `{input}`** and prints its result: wall time and max RSS of the process tree are measured, stdout is compared byte for byte. If the command writes a file instead, put `{out}` in it.
2. **`--measure '<cmd>'`** for anything else: it receives `{cmd}` (the `--before` or `--after` string), `{input}`, `{out}` and `{variant}`, and prints a JSON object of numbers on its last line. Put longer measure commands in a script under `bench/` and lock it.
3. **Microbenchmarks** below the cost of starting a process: run the language's own harness (criterion, `go test -bench`, mitata) inside `--measure` and print its per-operation number.

Output checks: byte-identical by default; `--check '<cmd>'` replaces it with any command that exits 0 when `{expected}` and `{actual}` match (tolerances, sorted lines, API responses). With `--measure` and no `--check`, nothing is verified and the script says so.

```sh
# a CLI, plus a generated input with a new seed
bench.py run --name simd-scan --before './old {input}' --after './new {input}' \
  --input data/real.ndjson --gen 'node gen.mjs --seed {seed} --out {out}'

# binary size
bench.py run --name lto --before old/app --after new/app \
  --measure 'printf "{\"bytes\": %s}\n" $(wc -c < {cmd})' --primary bytes

# any field tool behind a locked script that prints one JSON line
bench.py run --name index-on-user --before before.sql --after after.sql \
  --measure 'bench/measure-query.sh {cmd} {out}' --check 'bench/same-rows.sh {expected} {actual}'
```

## Numbers that do not count

- Input-specific changes: hard-coded values or sizes, embedded or cached results for the benchmark input.
- State carried across iterations so later runs hit a cache, unless production has the same condition (say so).
- Work moved out of the timed region: into setup, deferred past the measurement, or left lazily unevaluated.
- Work the compiler deleted because the result is unused.
- Mismatched conditions: debug before and release after, different input, machine, load or cache warmth.
- Cherry-picking: using only good runs, trimming outliers on one side, changing the run count mid-way.
- Flags or branches that skip validation or error handling only under benchmark.
- Metric swapping: p50 while p99 regressed, speed while memory regressed.
- Weakened, deleted or rewritten tests and benchmarks.

## Limits

Write the formula for each kind that applies and take the largest:

- Bandwidth: bytes moved ÷ memory, disk or network bandwidth
- Latency: round trips × RTT, random accesses × access latency, synchronization waits
- Compute: required operations ÷ (clock × instructions per cycle × SIMD width × cores)
- Memory: minimum bytes for the working set and output

With no formula (binary size, for example), write "not computable" and measure the fastest or smallest known implementation of the same job as the reference.
