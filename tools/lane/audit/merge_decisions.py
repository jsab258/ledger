"""Merge the decision extraction files (stage 1b of the full audit) into one list.

Reads work/dec-*.jsonl, gives each row a stable id (D-<letter>-<nnn>, the letter
naming the source group), normalises fields, and writes work/decisions-merged.json
plus per-area batch files for the classification pass.
Usage: python3 tools/lane/audit/merge_decisions.py production/audits/full-2026-11
"""
import json
import pathlib
import sys

AREAS = ["canon", "story", "design", "art", "clothing", "faces-voices", "simulation",
         "tools", "process", "budget", "licences", "disk-backup", "research", "scope", "other"]
FIELDS = ["src", "date", "topic", "area", "decision", "words", "replaces", "later_note"]


def load(workdir):
    rows = []
    for f in sorted(pathlib.Path(workdir).glob("dec-*.jsonl")):
        group = f.name.split("-")[1]
        n = 0
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            n += 1
            out = {k: (r.get(k) or "") for k in FIELDS}
            if out["area"] not in AREAS:
                out["area"] = "other"
            out["id"] = f"D-{group}-{n:03d}"
            out["group"] = group
            for extra in ("in_force_text", "enforcers", "advisor_no"):
                if extra in r:
                    out[extra] = r[extra]
            rows.append(out)
    return rows


def batches(rows, size=120):
    """Group by area (related decisions together), then cut into batches of about `size`."""
    by_area = {}
    for r in rows:
        by_area.setdefault(r["area"], []).append(r)
    out, cur = [], []
    for area in AREAS:
        items = sorted(by_area.get(area, []), key=lambda r: (r["topic"].lower(), r["date"]))
        for r in items:
            cur.append(r)
            if len(cur) >= size:
                out.append(cur)
                cur = []
    if cur:
        out.append(cur)
    return out


def main(base):
    work = pathlib.Path(base) / "work"
    rows = load(work)
    (work / "decisions-merged.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
    for i, b in enumerate(batches(rows), 1):
        (work / f"batch-{i:02d}.json").write_text(json.dumps(b, indent=1, ensure_ascii=False), encoding="utf-8")
    print(len(rows), "rows")


if __name__ == "__main__":
    main(sys.argv[1])
