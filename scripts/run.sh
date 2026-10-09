#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT="$PWD"
WORK="${WORK:-$ROOT/.repro-work}"
mkdir -p "$WORK" "$ROOT/results"
UPSTREAM="https://github.com/Blosc/c-blosc2.git"
BASE="6b06dd65dbf7927a9339e4f687637f97668a181a"
PATCHED="d2409997375b60cd45f58e74e69e84b5e17d6907"
FIXTURE_SHA="4c86180d078cda1dc2584497790d627573ca324f"
curl --fail --location --retry 3 --silent --show-error \
  "https://raw.githubusercontent.com/Johnny-Kao/c-blosc2/$FIXTURE_SHA/bench/rainfall-grid-150x150.bin" \
  --output "$WORK/rainfall-grid-150x150.bin"
test -s "$WORK/rainfall-grid-150x150.bin"
for variant in base patched; do
  sha="$BASE"
  [ "$variant" = patched ] && sha="$PATCHED"
  if [ ! -d "$WORK/src-$variant/.git" ]; then git clone --quiet "$UPSTREAM" "$WORK/src-$variant"; fi
  git -C "$WORK/src-$variant" fetch --quiet origin "$sha"
  git -C "$WORK/src-$variant" checkout --quiet --detach "$sha"
  cmake -S "$WORK/src-$variant" -B "$WORK/build-$variant" \
    -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTS=OFF \
    -DBUILD_BENCHMARKS=OFF -DBUILD_EXAMPLES=OFF
  cmake --build "$WORK/build-$variant" --parallel 2
  lib="$(find "$WORK/build-$variant" -name 'libblosc2.so*' -type f | head -n 1)"
  test -n "$lib"
  cc -O2 -std=c11 -I "$WORK/src-$variant/include" \
    "$ROOT/benchmark/pr805_realdata_bench.c" "$lib" \
    -Wl,-rpath,"$(dirname "$lib")" -o "$WORK/pr805-$variant"
done
python3 scripts/paired_runs.py "$WORK" "$ROOT/results"
python3 scripts/plot.py "$ROOT/results/results.csv" "$ROOT/results/comparison.png"
