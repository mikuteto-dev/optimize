# Infrastructure, deployment and cloud cost

## Metrics

Cost per request or per job, CPU and memory utilization per instance, container image size, cold start, deploy and build time, egress bytes, CDN cache hit ratio, storage cost by tier.

## Levers

- **Images and artifacts**: multi-stage builds, distroless or scratch images with static binaries, layer ordering for cache reuse, removing build tools and caches from the final image.
- **Sizing**: right-sizing instances and limits from measured utilization, autoscaling on the metric that actually saturates, bin-packing.
- **Cold start**: smaller bundles, less initialization, snapshotting where supported.
- **Network and storage**: compression, CDN in front of static and cacheable responses, region placement next to users and data, lifecycle rules moving cold data to cheaper tiers.
- **Build time**: remote and local caches, incremental builds, parallel jobs, fewer dependencies.

Changing CPU architecture (ARM instances), regions, provisioned capacity, or retention periods changes cost, compatibility or guarantees and needs the user.

## Tools

`dive` for image layers, cloud cost explorers, provider metrics dashboards, build tracing (`--profile` flags, BuildKit timings).
