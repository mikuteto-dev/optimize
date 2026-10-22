# Data pipelines and machine learning

Measure on full-size data and the real hardware; small samples hide spilling, skew and memory limits.

## Metrics

Throughput (rows/s, samples/s, tokens/s), end-to-end job time, peak RAM and VRAM, GPU utilization and idle gaps, bytes read and shuffled, storage size, time to first token and per-token latency for inference, cost per job.

## Levers

- **Data**: columnar formats (Parquet, Arrow) with zstd, predicate and projection pushdown, partition pruning, vectorized engines (DuckDB, Polars), zero-copy between stages, avoiding Python per-row loops.
- **Pipelines**: overlap loading with compute (prefetch, pinned memory, multiple workers), larger batches up to the memory limit, avoiding repeated work through caching of intermediate results.
- **Training and inference**: kernel fusion (`torch.compile`), fused attention (FlashAttention), KV cache reuse, continuous batching, CUDA graphs, gradient checkpointing for memory, sharding across devices.

Mixed precision (bf16, fp16), quantization (int8, int4), pruning, distillation and approximate retrieval change results and need the user.

## Tools

`torch.profiler`, Nsight Systems, `nvidia-smi dmon`, `py-spy`, `memray`, `scalene`, DuckDB `EXPLAIN ANALYZE`, Spark UI.

## With bench.py

The default mode times a job on `{input}` writing `{out}`. A `--measure` wrapper adds `{"rows_per_s": …, "peak_vram_mib": …}` with `--higher-better rows_per_s`; `--check` compares outputs exactly, or within the tolerance the user accepts for floating-point results.
