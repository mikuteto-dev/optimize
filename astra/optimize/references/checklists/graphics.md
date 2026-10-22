# 3D, games and real-time graphics

The budget is the frame: 16.7 ms at 60 fps, 11.1 ms at 90 fps, 8.3 ms at 120 fps. Measure CPU and GPU time separately, since the slower one sets the frame time, and on the weakest target device.

## Metrics

Frame time (average and 1% / 0.1% lows), CPU and GPU time per frame, draw calls, triangles and vertices, overdraw, shader instruction count and register pressure, texture and buffer bandwidth, VRAM, load time, download and install size, per-frame allocations (GC hitches), battery and thermal throttling.

## Levers

- **Draw submission**: instancing, batching, fewer state changes, GPU-driven rendering, multithreaded command recording, WebGPU over WebGL where available.
- **Culling and detail**: frustum and occlusion culling, LOD, meshlets, impostors for distant objects.
- **Geometry and textures**: vertex quantization (half floats, normalized integers), index and vertex cache optimization (meshoptimizer), mesh compression (meshopt, Draco), GPU texture compression (BCn, ASTC, ETC2 via KTX2 and Basis Universal), mipmaps, atlases, streaming.
- **Shading**: lower precision where it is invisible, fewer texture fetches and dependent reads, less branching, depth prepass or front-to-back sorting to cut overdraw, baked lighting, compute shaders for bulk work.
- **CPU side**: data-oriented layout (ECS, SoA), zero allocations per frame, job systems across cores, spatial structures for queries.

Changes users can see (resolution scaling, upscaling such as FSR or DLSS, LOD distances, texture quality, effect removal) need the user.

## Tools

RenderDoc, Xcode GPU frame capture and Metal System Trace, PIX, Nsight Graphics, Spector.js, Tracy, Unity Profiler and Frame Debugger, Unreal Insights.

## With bench.py

`--before` and `--after` are the two builds. A locked `bench/measure-frames.sh {cmd} {out}` plays a fixed camera path on the weakest target device, prints `{"frame_p99_ms": …, "gpu_ms": …, "cpu_ms": …, "vram_mib": …}` from the engine's frame-time export, and saves fixed-frame screenshots to `{out}`; `--check` compares them within an image-difference tolerance.
