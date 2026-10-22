# Audio, video and image processing

## Metrics

Real-time factor (processing time ÷ media duration), encode and decode throughput, end-to-end latency (glass-to-glass for video, round trip for audio), dropped frames and audio underruns, output size at equal quality (measured with VMAF, SSIM or PSNR), CPU and GPU use, energy.

## Levers

- **Hardware**: hardware encoders and decoders (VideoToolbox, NVENC and NVDEC, Quick Sync, MediaCodec), GPU or SIMD color conversion and scaling (libyuv).
- **Data movement**: zero-copy frame passing, staying in GPU memory between stages, planar formats that match the next stage, buffer pools.
- **Pipelines**: decode, process and encode on separate threads, processing at the output resolution, skipping work on unchanged regions.
- **Real-time audio**: no allocation, locks, I/O or logging in the audio callback; latency per buffer = buffer frames ÷ sample rate, so measure underruns before shrinking buffers.
- **Encoder settings**: presets and rate control chosen by measured quality and size.

Changing codecs, containers, bitrates, resolution or quality targets changes compatibility or what users see and needs the user.

## Tools

`ffmpeg -benchmark`, `ffprobe`, VMAF (`libvmaf`), Xcode Instruments, Nsight Systems, platform audio tracing (CoreAudio HAL logs, Perfetto).

## With bench.py

The default mode times a processing command on `{input}` media writing `{out}`. A `--measure` wrapper adds `{"rtf": …, "bytes": …}` (processing seconds ÷ media seconds from `ffprobe`, output size); `--check` runs VMAF on `{expected}` and `{actual}` and fails below the agreed score.
