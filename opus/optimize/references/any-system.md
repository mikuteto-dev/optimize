# Any system

The domain files are worked examples, not the boundary. For any system, listed or not, derive the metrics and levers this way.

## 1. Draw the path

List every component that does work between the input and the result the user gets: devices, browsers, networks, CDNs, servers, queues, databases, caches, GPUs, external APIs, models, build and deploy steps, and people waiting on any of them. Mark which steps are serial and which run in parallel.

## 2. List what each component consumes

For each component: compute (CPU, GPU, accelerators), memory at each level (registers, caches, RAM, VRAM, buffers), storage, network bytes and round trips, energy, money, and wall-clock waiting. Each one is a candidate metric. The primary metric is the one the user or payer feels end to end; the rest are checked for regressions.

## 3. Apply the generic levers to every component

- **Less**: skip, deduplicate, early exit, remove unused features and data.
- **Once**: precompute, cache, memoize, move to build time.
- **Smaller**: narrower types, better formats, compression, quantized assets, fewer fields.
- **Closer**: locality in caches, data next to compute, edge and CDN, co-located services.
- **Together**: batching, fusion, pipelining, fewer round trips.
- **Parallel**: cores, SIMD, GPU, concurrent requests, sharding.
- **Better timing**: prefetch, defer, move off the critical path.
- **Better hardware or placement**: the unit that does this work most cheaply (SIMD units, GPU, hardware codecs, accelerators, cheaper instances).
- **Better algorithm**: lower complexity, specialization to the real input distribution.

## 4. Pull in the domain's existing knowledge

Every field has its own terms, profilers, canonical optimization guides, and a best known implementation. Find them before inventing candidates: search with the field's own vocabulary, read primary sources (official performance guides, papers, talks, maintainers' writing), and take the field's profilers and benchmarks. The best known implementation becomes the reference for the limit when no formula exists.

## 5. Find the limit

Use the formulas in [benchmarking.md](benchmarking.md). For compute-heavy kernels, the roofline model (arithmetic intensity × memory bandwidth versus peak compute) gives the ceiling. For waiting, the critical path of serial steps × their minimum latency gives the floor.
