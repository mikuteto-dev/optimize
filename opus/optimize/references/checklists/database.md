# Databases

Measure with production-like data volume and distribution; plans on a 1,000-row table say nothing about 100 million rows.

## Metrics

Query latency (p50 / p99), rows scanned per row returned, buffer and cache hit ratio, IOPS and bytes read, lock and I/O wait, table and index size, WAL or binlog volume, replication lag, connection count, memory (shared buffers, work memory), queries per request.

## Levers

- **Queries**: read the plan (`EXPLAIN (ANALYZE, BUFFERS)` in PostgreSQL, `EXPLAIN ANALYZE` in MySQL, `EXPLAIN QUERY PLAN` in SQLite), select only needed columns, keyset pagination instead of `OFFSET`, remove N+1 queries, push filters and aggregation into the database, prepared statements.
- **Indexes**: composite in the right column order, covering (`INCLUDE`), partial, expression, BRIN for naturally ordered large tables; drop unused indexes that only cost writes.
- **Writes**: batching, `COPY` or multi-row inserts for bulk loads, fewer indexes on hot write paths, `fillfactor` for HOT updates, shorter transactions.
- **Storage**: narrower types (`int` over `bigint`, `smallint`, enums), column order for alignment padding, compression (TOAST, ClickHouse codecs), partitioning, archiving cold rows.
- **Connections**: a pooler (PgBouncer), pool size from measurement.
- **Engine choice**: columnar engines (DuckDB, ClickHouse) for analytics, materialized views for repeated aggregates, an embedded database where a server is not needed.

Schema migrations, isolation level changes, and durability settings (`synchronous_commit = off`, SQLite `synchronous = NORMAL` or `OFF`, async replication) change guarantees and need the user.

## Tools

`pg_stat_statements`, `auto_explain`, `pgbench`, MySQL `performance_schema`, SQLite `.eqp on` and `sqlite3_analyzer`.

## With bench.py

`--before` and `--after` are SQL files (or schema migrations applied to a disposable copy). A locked `bench/measure-query.sh {cmd} {out}` runs `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)`, prints `{"exec_ms": …, "shared_read_blocks": …}` from `"Execution Time"` and the plan's `"Shared Read Blocks"`, and writes the query's rows to `{out}`; `--check` compares the rows sorted.
