# Across domains

Most real systems span several domains: a page, an API, a database, a CDN, a build. Optimizing each tier on its own misses where the time goes and can move cost from one tier to another without reducing the total.

## Primary metric

Pick the metric the user or operator actually experiences end to end (time until the page is usable, request latency seen by the client, job completion time, cost per request). Tier metrics (query time, bundle size, server CPU) are candidates' local evidence, not the goal.

## Find where the end-to-end metric goes

Trace one request or one job through every tier and attribute its time and bytes:

- browser waterfall and main-thread profile (DevTools Performance, WebPageTest)
- network and CDN timing (DNS, TLS, TTFB, cache status)
- server spans (OpenTelemetry or equivalent distributed tracing)
- database time per query (`pg_stat_statements`, slow query log)
- background jobs, queues and third-party calls on the path

The tier with the largest share, and the longest serial chain of dependent steps, comes first. Shortening the critical path beats speeding up work that runs in parallel with it.

## One candidate list for the whole system

Collect candidates from every system into the single ledger (`bench/candidates.md`), ordered by their share of the end-to-end metric × expected gain.

Moving work between tiers is a candidate in its own right, measured on the total:

- to build time: precomputation, static generation, asset processing
- to the edge or CDN: caching, rendering, redirects
- into the database: filtering, joins and aggregation instead of moving rows to the application
- out of the database: caching hot reads, moving analytics to a columnar store
- between client and server: server rendering versus client rendering, where validation and formatting run
- to background work: anything not needed for the response (changes consistency, so it needs the user)

## Cost shifting

A change that improves one tier often costs another: a server cache raises memory, client-side rendering raises INP and battery use, denormalization speeds reads and slows writes, compression trades CPU for bytes, larger batches trade latency for throughput. Measure every tier the change touches and keep it only if the end-to-end metric improves without unreported regressions.

## Report

Show the end-to-end metric first, then one row per tier (before, after) so moved cost is visible.
