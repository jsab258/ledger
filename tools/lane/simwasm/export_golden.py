#!/usr/bin/env python3
"""Export the committed perception golden table to JSON, grouped by rule.

Usage (from the repository root):
  python -I tools/lane/simwasm/export_golden.py OUT.json

Reads ue-probe/perception-golden/part-*.txt in order (joined, they are the
table byte for byte), drops the '#' header lines and carriage returns, and
writes {"Rule": [{"args": [...], "expected": "..."}, ...], ...}.
Every value stays a string, exactly as the C# wrote it: whether a column is
a number or text (bits are "0"/"1") is decided by the harness, per rule,
never guessed from the value. The output (about 7 MB) is not committed.
"""
import glob, json, os, sys
from collections import OrderedDict

def main():
    if len(sys.argv) != 2:
        print(__doc__); return 2
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    parts = sorted(glob.glob(os.path.join(root, "ue-probe", "perception-golden", "part-*.txt")))
    if not parts:
        print("no golden parts found"); return 3
    by = OrderedDict()
    rows = 0
    for p in parts:
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\r\n")
                if not line or line.startswith("#"):
                    continue
                cols = line.split("|")
                by.setdefault(cols[0], []).append({"args": cols[1:-1], "expected": cols[-1]})
                rows += 1
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        json.dump(by, f, separators=(",", ":"))
    print(f"rows={rows} rules={len(by)} parts={len(parts)} out={sys.argv[1]}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
