# Reproducing C-Blosc2 PR #805

A standalone, **non-fork** reproduction repository for [Blosc/c-blosc2#805](https://github.com/Blosc/c-blosc2/pull/805) (merged). This repository contains **benchmark harness code only**; it checks out fixed C-Blosc2 revisions during CI.

## Scope

This is a reproduction of the *existing* paired Linux/GitHub Actions benchmark from [the original research workflow](https://github.com/Johnny-Kao/c-blosc2/actions/runs/37932979182), not a new compression or scheduling study.

- **Baseline**: `6b06dd65dbf7927a9339e4f687637f97668a181a`
- **Patched (#805)**: `d2409997375b60cd45f58e74e69e84b5e17d6907`
- **Runner**: `ubuntu-24.04`, POSIX path; Windows startup handling is different.
- **Fixture**: original 150 × 150 rainfall-grid binary from the pinned [research repository](https://github.com/Johnny-Kao/c-blosc2/blob/4c86180d078cda1dc2584497790d627573ca324f/bench/rainfall-grid-150x150.bin). Larger inputs **repeat the fixture bytes**; they are *not* distinct real-world datasets.
- **Parameters**: `typesize=4`, `clevel=5`, `blocksize=16384` bytes; data sizes 16, 48, 64, 128, 512 KiB; 4/16 threads; disposable and reused compression contexts.
- **Measurement**: 20 warm-ups + 350 timed iterations per round; nine rounds per variant in alternating baseline/patched order; report median of round means. Disposable timing includes context create/free; reused timing excludes context creation.

## Run

In GitHub Actions, open **Actions → Reproduce PR #805 → Run workflow**. The job checks out the fixed upstream commits, builds each independently, compiles the benchmark against each, runs paired measurements, and saves CSV/JSON and the plot as downloadable artifacts.

To reproduce locally on Linux, use `bash scripts/run.sh` from this repository root (requires CMake, a C compiler, Python 3, Git, and curl). Data is fetched from the pinned research commit.

**Do not compare raw microseconds across unrelated hardware.** Evaluate baseline vs patched on the same runner. CI numbers are **not** the historical 35.86→2.02 microsecond local benchmark: that earlier benchmark used another configuration; the graphs in the article must identify their dataset and test provenance.

## Source and caveats

- Upstream implementation: [PR #805](https://github.com/Blosc/c-blosc2/pull/805)
- Original paired run: [run #37932979182](https://github.com/Johnny-Kao/c-blosc2/actions/runs/37932979182)
- Original benchmark: [tests/pr805_realdata_bench.c](https://github.com/Johnny-Kao/c-blosc2/blob/4c86180d078cda1dc2584497790d627573ca324f/tests/pr805_realdata_bench.c)
- Original workflow: [pr805-realdata.yml](https://github.com/Johnny-Kao/c-blosc2/blob/4c86180d078cda1dc2584497790d627573ca324f/.github/workflows/pr805-realdata.yml)

Results are workload-dependent: not every test improves; changes to shared-pool notification can regress on some workloads. This is a microbenchmark, not end-to-end application throughput. No C-Blosc2 library source code is modified by this repository.
