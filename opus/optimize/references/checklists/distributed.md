# Distributed systems

## Metrics

Tail latency at each fan-out level, network hops and round trips per request, bytes per message, throughput per node, consensus or coordination rounds, replication lag, queue depth and age, cross-zone and cross-region traffic and its cost.

## Levers

- **Fan-out**: tail latency grows with the number of parallel calls (the slowest of N), so reduce fan-out, hedge or tie requests, and set per-call deadlines.
- **Hops**: co-locate chatty services, merge services that always call each other, move data to where it is read.
- **Messages**: batching, compact encodings, deltas instead of full state, compression chosen by measured CPU versus bytes.
- **Coordination**: fewer synchronous rounds, partitioning so most operations touch one shard, avoiding distributed locks on hot paths.
- **Flow control**: backpressure, bounded queues, admission control instead of unbounded retries.

Weaker consistency, fewer replicas, async replication, and changed partitioning keys change guarantees and need the user.

## Tools

Distributed tracing (OpenTelemetry, Jaeger), per-hop latency histograms, chaos and load tools that reproduce tail behavior.

## With bench.py

`--before` and `--after` name two deployments of the same topology. A locked `bench/measure-trace.sh {cmd}` drives a fixed load and prints `{"p99_ms": …, "hops": …, "bytes_per_request": …}` from the trace backend; `--check` compares responses for a fixed request set.
