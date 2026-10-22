# Tools

- General: `hyperfine --warmup 3 -N`, `/usr/bin/time -l` (macOS max RSS), `benchstat` (significance)
- Profilers: `samply` (macOS, Linux), `perf record` (Linux)
- Hardware counters: `perf stat -e cycles,instructions,cache-misses,branch-misses` (Linux), `xctrace record --template 'CPU Counters'` (macOS); deterministic instruction counts with `valgrind --tool=cachegrind` (Linux)
- Generated code: Compiler Explorer (godbolt.org)
- Correctness: `go test -race`, `go test -fuzz`, `cargo fuzz`, `cargo +nightly miri test`, `-fsanitize=address,undefined,thread`
- Go: `go test -bench . -benchmem -count 10`, `go tool pprof`, `-gcflags='-m'` (escape analysis), `-gcflags='-d=ssa/check_bce/debug=1'` (bounds checks), `-gcflags='-S'`, `go tool nm -size -sort size`
- Rust: `criterion`, `cargo flamegraph`, `dhat`, `cargo asm` (cargo-show-asm), `cargo bloat --release`, `twiggy` (wasm)
- TypeScript / Node.js: `node --cpu-prof`, `node --heap-prof`, `node --trace-deopt`, `mitata`, `esbuild --metafile` for bundle breakdown
- Python: `pyperf`, `py-spy`, `scalene`, `memray`
