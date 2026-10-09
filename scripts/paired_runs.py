#!/usr/bin/env python3
"""Re-run the original nine-round paired PR #805 matrix, unchanged."""
import csv, json, statistics, subprocess, sys
from pathlib import Path

work, output = map(Path, sys.argv[1:3])
output.mkdir(parents=True, exist_ok=True)
source = work / "rainfall-grid-150x150.bin"
sizes = [16384, 49152, 65536, 131072, 524288]
threads = [4, 16]
records = []
for mode in (0, 1):
    for size in sizes:
        for nt in threads:
            by = {"base": [], "patched": []}
            for round_ in range(9):
                order = ("base", "patched") if round_ % 2 == 0 else ("patched", "base")
                for variant in order:
                    cmd = [str(work / f"pr805-{variant}"), str(source),
                           str(size), str(nt), "350", str(mode)]
                    line = subprocess.check_output(cmd, text=True).strip()
                    us = float(line.split("mean_us=")[1].split(",")[0])
                    by[variant].append(us)
                    print(f"PAIR mode={mode} size={size} threads={nt} round={round_+1} variant={variant}: {line}", flush=True)
            before = statistics.median(by["base"])
            after = statistics.median(by["patched"])
            rec = dict(reusable=bool(mode), bytes=size, threads=nt,
                       baseline_median_us=before, patched_median_us=after,
                       speedup=before / after, samples_per_variant=9,
                       iterations_per_sample=350,
                       pair_median_speedup=statistics.median(a / b for a, b in zip(by["base"], by["patched"])))
            print("SUMMARY " + json.dumps(rec, sort_keys=True), flush=True)
            records.append(rec)
(output / "results.json").write_text(json.dumps(records, indent=2) + "\n")
with (output / "results.csv").open("w", newline="") as fp:
    writer = csv.DictWriter(fp, fieldnames=[k for k in records[0] if k != "pair_median_speedup"] + ["pair_median_speedup"])
    writer.writeheader()
    writer.writerows(records)
print("ALL_RESULTS " + json.dumps(records, sort_keys=True), flush=True)
