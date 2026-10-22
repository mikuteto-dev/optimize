# Numerical and scientific computing

The roofline model sets the ceiling: performance = min(peak compute, arithmetic intensity × memory bandwidth). Compute arithmetic intensity (operations per byte moved) for each kernel to know whether it is compute-bound or bandwidth-bound before optimizing it.

## Metrics

Achieved FLOP/s versus peak, achieved bandwidth versus peak, time to solution, memory footprint, scaling efficiency across cores and nodes, energy to solution.

## Levers

- **Libraries**: vendor-tuned BLAS, LAPACK and FFT (Accelerate on macOS, MKL, OpenBLAS, cuBLAS, FFTW) instead of hand-written loops for standard operations.
- **Memory**: cache blocking and tiling, loop interchange for unit stride, structure of arrays, fusing loops to reuse data while it is in cache, sparse formats (CSR, CSC, block formats) matched to the access pattern.
- **Parallelism**: SIMD, OpenMP, MPI with communication overlapped with compute, GPU kernels with coalesced access and enough occupancy.
- **Algorithm**: better asymptotics (FFT, multigrid, fast multipole), better preconditioners, fewer iterations to the same tolerance.

Lower precision, looser tolerances, and approximate methods change results and need the user.

## Tools

`perf`, Intel VTune and Advisor (roofline), `likwid`, Nsight Compute, Xcode Instruments, `valgrind --tool=cachegrind`.

## With bench.py

The default mode works for kernels run as programs that print their result. Add `gflops` and `gbps` by having a locked `--measure` script divide the known operation and byte counts by the measured time, with `--higher-better gflops,gbps`. `--check` compares results within the numerical tolerance the user accepts.
