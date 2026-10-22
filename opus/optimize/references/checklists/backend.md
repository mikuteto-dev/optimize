# Backend services

Load-test at a constant arrival rate (wrk2, vegeta, k6 `constant-arrival-rate`); closed-loop tools hide queueing delay (coordinated omission) and understate tail latency.

## Metrics

p50 / p99 / p99.9 latency at a stated request rate, maximum throughput per core, CPU time and allocations per request, RSS per instance, cold start, open connections, egress bytes, cost per request.

## Levers

- **Round trips**: remove N+1 calls, batch and pipeline, keep-alive and connection pooling, co-locate services and data, fetch in parallel instead of in sequence.
- **Serialization**: faster codecs and libraries, avoiding re-encoding, streaming large bodies, response compression with a level chosen by measurement. Changing the wire format (JSON → protobuf, MessagePack) needs the user.
- **Caching**: in-process, shared (Redis, Memcached), HTTP caching headers, CDN; measure hit ratio and invalidation cost.
- **Concurrency**: no blocking calls on event loops, pool sizes from measurement, backpressure, bounded queues, lock contention removal, `sendfile` and zero-copy.
- **Runtime**: GC and heap settings, allocation reduction on the request path, startup work moved to build time, static binaries.
- **Logging and telemetry**: no formatting on the hot path when the level is disabled; sampling changes what operators see and needs the user.

Moving work to queues or background jobs changes consistency and needs the user.

## Tools

wrk2, vegeta, k6, `go tool pprof`, async-profiler, `perf`, `samply`, OpenTelemetry traces, flame graphs per endpoint.
