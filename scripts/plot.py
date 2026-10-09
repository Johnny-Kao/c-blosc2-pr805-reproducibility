#!/usr/bin/env python3
"""Plot paired PR805 results with one consistent Navy/Teal palette."""
import csv, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

data = list(csv.DictReader(open(sys.argv[1], newline="")))
target = Path(sys.argv[2])
navy, blue, teal = "#243B53", "#376B96", "#238B78"
fig, ax = plt.subplots(figsize=(10.5, 5.8))
labels, before, after = [], [], []
for r in data:
    labels.append(f'{"Reused" if r["reusable"] == "True" else "Disposable"} / {int(r["bytes"]) // 1024}KiB / {r["threads"]}t')
    before.append(float(r["baseline_median_us"]))
    after.append(float(r["patched_median_us"]))
pos = range(len(data))
ax.barh([i + .18 for i in pos], before, height=.34, color=blue, label="Before #805")
ax.barh([i - .18 for i in pos], after, height=.34, color=teal, label="After #805")
ax.set_yticks(list(pos), labels, fontsize=8)
ax.invert_yaxis()
ax.set_xlabel("Median round-mean latency (microseconds)", color=navy)
ax.set_title("PR #805: same-runner paired benchmark", color=navy)
ax.legend(frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
target.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(target, dpi=170)
print(target)
