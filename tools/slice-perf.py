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
is over 16.7 ms and the slowest 1% is not; BELOW-30 otherwise. AND NEVER BELOW 30
MEANS EVERY FRAME (21 October, P1's fresh review: a slice with a 211.8 ms frame
and 13 over 33.3 still read MEETS): a MEETS with any frame over 33.3 ms is SPIKES.

CARD MEMORY AT ITS PEAK (8 November, n09-9; QA-FIRST-STEPS-2026-11-08.md step 3):
gpuMemMB is the MEDIAN, and medians had been read as peaks (the exit rehearsal found
6,161 to 8,481 MB where the night report said 5,810 to 6,089). The line now also gives
gpuMemPeakMB, the highest GPUMem/LocalUsedMB in any frame row after the header and
EVENTS rows, the dropped loading frames included (the launch peak sits there),
gpuMemPeakSettledMB, the highest after the drop, and memVerdict UNDER or OVER-LINE
against memLine=5650 (MEMORY-PLAN-2026-11-07.md section 4: the table's ceiling under
Windows' budget of 5,771). It reports and never fails. Until the build machine's perf
step runs at High the reading is at Highest; the line says which only by its label.
"""
import csv
import os
import statistics
import sys

DROP = 300
MEM_LINE = 5650


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


def verdict(median, p99, worst=None):
    if median <= 16.7 and p99 <= 33.3:
        return "SPIKES" if worst is not None and worst > 33.3 else "MEETS"
    if p99 <= 33.3:
        return "BELOW-60"
    return "BELOW-30"


def read(path):
    rows = list(csv.reader(open(path, encoding="utf-8", errors="ignore")))
    if not rows:
        # AN EMPTY FILE IS NO FRAMES, said as such (24 September: the reader
        # raised on one, printed nothing, and the verdict lost its line).
        return [], [], []
    # THE PROFILER'S METADATA ROW IS NOT A FRAME (8 Nov: "[HasHeaderRowAtEnd]" and its
    # values close the file, and read as an 1,794,111,057 MB peak on the 3b3454e capture)
    header, body = rows[0], [r for r in rows[1:] if r and r[0] != "EVENTS" and not r[0].startswith("[")
                             and len(r) > 10]
    return (column(body[DROP:], header, "FrameTime"), column(body[DROP:], header, "GPUTime"),
            column(body[DROP:], header, "GPUMem/LocalUsedMB"), column(body, header, "GPUMem/LocalUsedMB"))


def mem_peak(mem_all, mem_settled):
    """The peak fields: every frame's peak, the settled peak, the line and the verdict."""
    if not mem_all and not mem_settled:
        return "gpuMemPeakMB=absent gpuMemPeakSettledMB=absent memLine=%d memVerdict=absent" % MEM_LINE
    peak = max(mem_all or mem_settled)
    settled = max(mem_settled) if mem_settled else peak
    return ("gpuMemPeakMB=%.0f gpuMemPeakSettledMB=%.0f memLine=%d memVerdict=%s"
            % (peak, settled, MEM_LINE, "OVER-LINE" if peak > MEM_LINE else "UNDER"))


def line(label, ft, gpu, mem, mem_all=None):
    if not ft:
        # a short capture still has a launch peak worth reading (8 Nov review, finding 5)
        return "slicePerf=%s status=NO-FRAMES" % label + (" " + mem_peak(mem_all, mem) if mem_all else "")
    med, p99 = statistics.median(ft), pct(ft, 0.99)
    return ("slicePerf=%s status=%s frames=%d medianMs=%.2f p95Ms=%.2f p99Ms=%.2f worstMs=%.2f fps=%.1f "
            "gpuMedianMs=%s over16.7=%d over33.3=%d gpuMemMB=%s target=60fps-at-3440x1440/never-below-30 %s"
            % (label, verdict(med, p99, max(ft)), len(ft), med, pct(ft, 0.95), p99, max(ft), 1000.0 / med,
               ("%.2f" % statistics.median(gpu)) if gpu else "absent",
               sum(1 for x in ft if x > 16.7), sum(1 for x in ft if x > 33.3),
               ("%.0f" % statistics.median(mem)) if mem else "absent",
               mem_peak(mem_all if mem_all is not None else mem, mem)))


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
    check("a single frame over 33.3 is SPIKES, not MEETS", verdict(11.8, 12.9, 211.8) == "SPIKES")
    check("every frame under the bar still MEETS", verdict(11.8, 12.9, 20.1) == "MEETS")
    check("below 60", verdict(20.0, 30.0) == "BELOW-60")
    check("below 30", verdict(20.0, 40.0) == "BELOW-30")
    check("no frames says so", line("x", [], [], []) == "slicePerf=x status=NO-FRAMES")
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as fh:
        empty = fh.name
    check("an empty capture reads as no frames", line("x", *read(empty)) == "slicePerf=x status=NO-FRAMES")
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["FrameTime", "GPUTime", "GPUMem/LocalUsedMB"] + ["c%d" % i for i in range(9)])
        for i in range(400):
            w.writerow([10.0, 8.0, 6100.0 if i < 300 else 5500.0] + [0] * 9)
        w.writerow(["EVENTS"] + [""] * 11)
        w.writerow(["[HasHeaderRowAtEnd]", "1", "1794111057"] + ["x"] * 9)
        tiny = fh.name
    s = line("x", *read(tiny))
    check("read() keeps the dropped frames for the peak", "gpuMemPeakMB=6100" in s and "gpuMemPeakSettledMB=5500" in s)
    os.remove(tiny)
    os.remove(empty)
    s = line("x", [10.0] * 99 + [40.0], [8.0] * 100, [3000.0] * 100)
    check("the slowest 1% is read", "p99Ms=40.00" in s and "status=BELOW-30" in s)
    # card memory at its peak (8 Nov, n09-9 step 3)
    rising = [6100.0] * 300 + [5500.0] * 100
    s = line("x", [10.0] * 100, [8.0] * 100, rising[DROP:], rising)
    check("a launch peak in the dropped frames reads OVER-LINE",
          "gpuMemPeakMB=6100" in s and "gpuMemPeakSettledMB=5500" in s and "memVerdict=OVER-LINE" in s
          and "gpuMemMB=5500" in s)
    s = line("x", [10.0] * 100, [8.0] * 100, [5000.0] * 100, [5000.0] * 400)
    check("all frames at 5,000 read UNDER", "gpuMemPeakMB=5000" in s and "memVerdict=UNDER" in s)
    s = line("x", [10.0] * 100, [8.0] * 100, [], [])
    check("no memory column says absent", "gpuMemMB=absent" in s and "memVerdict=absent" in s)
    print("slice-perf selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    label = sys.argv[sys.argv.index("--label") + 1] if "--label" in sys.argv else "slice"
    print(line(label, *read(sys.argv[1])))
