#!/usr/bin/env python3
"""The slice's frame times against Jafar's performance target, read off the game's own CSV profile.

    python tools/slice-perf.py CSV [--label NAME]   # prints one slicePerf line
    python tools/slice-perf.py --selftest

WHY, 24 September. Jafar's ruling of 23 September: 60 frames a second at his
monitor's resolution on this card, never below 30, with the voice running,
"and the slice measures against it". His monitor is 3440 x 1440. The probe's
slice-perf step runs the slice standing still at that size, drawn at half and
upscaled, with the engine's CSV profiler capturing its frames; this reads the
file and says where it stands. The first 300 frames are dropped because the
street is still loading in them.

THE VERDICT, in the ruling's own terms: MEETS when the median frame is at or
under 16.7 ms and the slowest 1% at or under 33.3 ms; BELOW-60 when the median
is over 16.7 ms and the slowest 1% is not; BELOW-30 otherwise.
"""
import csv
import os
import statistics
import sys

DROP = 300


def column(rows, header, name):
    if name not in header:
        return []
    i = header.index(name)
    out = []
    for r in rows:
        try:
            out.append(float(r[i]))
        except (ValueError, IndexError):
            pass
    return out


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(len(xs) * p))] if xs else 0.0


def verdict(median, p99):
    if median <= 16.7 and p99 <= 33.3:
        return "MEETS"
    if p99 <= 33.3:
        return "BELOW-60"
    return "BELOW-30"


def read(path):
    rows = list(csv.reader(open(path, encoding="utf-8", errors="ignore")))
    if not rows:
        # AN EMPTY FILE IS NO FRAMES, said as such (24 September: the reader
        # raised on one, printed nothing, and the verdict lost its line).
        return [], [], []
    header, body = rows[0], [r for r in rows[1:] if r and r[0] != "EVENTS" and len(r) > 10]
    body = body[DROP:]
    return (column(body, header, "FrameTime"), column(body, header, "GPUTime"),
            column(body, header, "GPUMem/LocalUsedMB"))


def line(label, ft, gpu, mem):
    if not ft:
        return "slicePerf=%s status=NO-FRAMES" % label
    med, p99 = statistics.median(ft), pct(ft, 0.99)
    return ("slicePerf=%s status=%s frames=%d medianMs=%.2f p95Ms=%.2f p99Ms=%.2f worstMs=%.2f fps=%.1f "
            "gpuMedianMs=%s over16.7=%d over33.3=%d gpuMemMB=%s target=60fps-at-3440x1440/never-below-30"
            % (label, verdict(med, p99), len(ft), med, pct(ft, 0.95), p99, max(ft), 1000.0 / med,
               ("%.2f" % statistics.median(gpu)) if gpu else "absent",
               sum(1 for x in ft if x > 16.7), sum(1 for x in ft if x > 33.3),
               ("%.0f" % statistics.median(mem)) if mem else "absent"))


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("slice-perf selftest FAIL " + name)
    check("meets", verdict(11.8, 12.9) == "MEETS")
    check("below 60", verdict(20.0, 30.0) == "BELOW-60")
    check("below 30", verdict(20.0, 40.0) == "BELOW-30")
    check("no frames says so", line("x", [], [], []) == "slicePerf=x status=NO-FRAMES")
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as fh:
        empty = fh.name
    check("an empty capture reads as no frames", line("x", *read(empty)) == "slicePerf=x status=NO-FRAMES")
    os.remove(empty)
    s = line("x", [10.0] * 99 + [40.0], [8.0] * 100, [3000.0] * 100)
    check("the slowest 1% is read", "p99Ms=40.00" in s and "status=BELOW-30" in s)
    print("slice-perf selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    label = sys.argv[sys.argv.index("--label") + 1] if "--label" in sys.argv else "slice"
    print(line(label, *read(sys.argv[1])))
