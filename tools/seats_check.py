#!/usr/bin/env python3
"""THE SEATS AS INTERACTION SPOTS, CHECKED (his order of 28 October 2026, D10; the method's step 1,
production/research/sit-and-turn/SPOTS-2026-10-28.md).

    python tools/seats_check.py              # production/specs/seats.json against the office and the clips
    python tools/seats_check.py --selftest

Each seat in seats.json is a spot's slot: an anchor (the floor point under the sitter's seat bone, and the way
he faces), a cap of one, who may use it, and its clips: In clips by side and foot, weighted Loops, Outs, and the
exit point he stands up to. Mafia runs every seat this way (478 slots, Study 1); Kingdom Come II drops any
entry its tests fail. This fails when:
  - a slot has no In or no Out clip, or a Loop without a weight, or a cap other than 1;
  - an anchor lies outside its furniture's floor box (mickeys-office.json) or within 20 cm of its ends (ours);
  - two anchors are closer than 50 cm (ours);
  - a named clip is not in the project (its .uasset under ue-probe/Content; skipped, and said, where the
    content is not on this machine);
  - the exit lies outside the room where he may stand ("room");
  - a kept entry ("in_kept", written from the room test by tools/seats_kept.py) is not among the seat's In clips,
    or kept entries carry no word of the test they came from ("in_kept_from").
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEATS = os.path.join(ROOT, "production", "specs", "seats.json")
OFFICE = os.path.join(ROOT, "production", "specs", "mickeys-office.json")
CLIPS = os.path.join(ROOT, "ue-probe", "Content", "Characters", "UEFN_Mannequin", "Animations", "Interactions", "Bench")
END_MARGIN_M, APART_M = 0.20, 0.50


def check(seats, office, clip_dir=CLIPS):
    faults, notes = [], []
    boxes = {b.get("name"): b for b in office.get("boxes", [])}
    room = seats.get("room", {})
    have_clips = os.path.isdir(clip_dir)
    if not have_clips:
        notes.append("clips not checked: no %s on this machine" % clip_dir)
    anchors = []
    for s in seats.get("seats", []):
        n = s.get("name", "?")
        if s.get("cap", 1) != 1:
            faults.append("%s: cap %r, not 1" % (n, s.get("cap")))
        if not s.get("in"):
            faults.append("%s: no In clip" % n)
        if not s.get("out"):
            faults.append("%s: no Out clip" % n)
        for lp in s.get("loops", []):
            if not isinstance(lp, dict) or not isinstance(lp.get("weight"), (int, float)) or lp["weight"] <= 0:
                faults.append("%s: a Loop without a weight" % n)
        kept = s.get("in_kept")
        if kept is not None:
            stray = [c for c in kept if c not in s.get("in", [])]
            if stray:
                faults.append("%s: kept entries not among its In clips: %s" % (n, stray))
            if not s.get("in_kept_from"):
                faults.append("%s: kept entries without the test they came from" % n)
            loose = [c for c in s.get("in_kept_starts_cm", {}) if c not in kept]
            if loose:
                faults.append("%s: start distances for entries not kept: %s" % (n, loose))
        clips = list(s.get("in", [])) + [lp.get("clip") for lp in s.get("loops", []) if isinstance(lp, dict)] + list(s.get("out", []))
        if have_clips:
            for c in clips:
                if not c or not os.path.isfile(os.path.join(clip_dir, c + ".uasset")):
                    faults.append("%s: clip %s not in the project" % (n, c))
        b = boxes.get(s.get("furniture"))
        if b is None:
            faults.append("%s: furniture %r not in the office" % (n, s.get("furniture")))
        else:
            x, z = s.get("x"), s.get("z")
            if not (b["x0"] <= x <= b["x1"] and b["z0"] <= z <= b["z1"]):
                faults.append("%s: anchor (%.3f, %.3f) outside %s" % (n, x, z, b["name"]))
            elif min(z - b["z0"], b["z1"] - z) < END_MARGIN_M - 1e-9:
                faults.append("%s: anchor within %.2f m of the %s's end" % (n, END_MARGIN_M, b["name"]))
        ex = s.get("exit")
        if not ex or not (room.get("x0", -1e9) <= ex.get("x", 1e9) <= room.get("x1", 1e9) and room.get("z0", -1e9) <= ex.get("z", 1e9) <= room.get("z1", 1e9)):
            faults.append("%s: exit %r not inside the room" % (n, ex))
        anchors.append((n, s.get("x", 0.0), s.get("z", 0.0)))
    for i in range(len(anchors)):
        for j in range(i + 1, len(anchors)):
            d = ((anchors[i][1] - anchors[j][1]) ** 2 + (anchors[i][2] - anchors[j][2]) ** 2) ** 0.5
            if d < APART_M - 1e-9:
                faults.append("%s and %s: %.3f m apart, under %.2f" % (anchors[i][0], anchors[j][0], d, APART_M))
    if not seats.get("seats"):
        faults.append("no seats: nothing measured")
    return faults, notes


def selftest():
    office = {"boxes": [{"name": "bench", "x0": 8.14, "x1": 8.65, "z0": 5.65, "z1": 7.26}]}
    seat = {"name": "a", "furniture": "bench", "x": 8.44, "z": 5.92, "cap": 1, "in": ["i"], "loops": [{"clip": "l", "weight": 1}],
            "out": ["o"], "exit": {"x": 7.8, "z": 5.92}}
    room = {"x0": 4.19, "x1": 9.0, "z0": 5.12, "z1": 7.5}
    def run(seats):
        return check({"room": room, "seats": seats}, office, clip_dir=os.path.join(ROOT, "no-such-dir"))[0]
    b = dict(seat, name="b", z=6.455, exit={"x": 7.8, "z": 6.455})
    cases = [
        ("ACCEPT two good slots", [seat, b], 0),
        ("REFUSE a slot with no Out", [dict(seat, out=[])], 1),
        ("REFUSE a slot with no In", [dict(seat, **{"in": []})], 1),
        ("REFUSE a Loop without a weight", [dict(seat, loops=[{"clip": "l"}])], 1),
        ("REFUSE a cap of two", [dict(seat, cap=2)], 1),
        ("REFUSE an anchor outside the bench", [dict(seat, x=7.9)], 1),
        ("REFUSE an anchor near the bench's end", [dict(seat, z=5.75)], 1),
        ("REFUSE anchors under 50 cm apart", [seat, dict(b, z=6.30)], 1),
        ("REFUSE an exit outside the room", [dict(seat, exit={"x": 9.5, "z": 5.92})], 1),
        ("REFUSE no seats: nothing measured", [], 1),
        ("ACCEPT a kept entry among the In clips, with its test", [dict(seat, in_kept=["i"], in_kept_from="the room test")], 0),
        ("REFUSE a kept entry not among the In clips", [dict(seat, in_kept=["x"], in_kept_from="the room test")], 1),
        ("REFUSE kept entries without their test", [dict(seat, in_kept=["i"])], 1),
    ]
    fails = 0
    print("seats-check selftest")
    for name, seats, bad in cases:
        got = run(seats)
        ok = bool(got) == bool(bad)
        fails += 0 if ok else 1
        print("  %s %s: %d fault(s)" % ("ok  " if ok else "FAIL", name, len(got)))
    print("seats-check selftest: %s" % ("passed" if not fails else "FAILED (%d)" % fails))
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    faults, notes = check(json.load(open(SEATS, encoding="utf-8")), json.load(open(OFFICE, encoding="utf-8")))
    for n in notes:
        print("seats-check note: " + n)
    for f in faults:
        print("seats-check FAIL " + f)
    print("seats-check: %d seat(s), %d fault(s)" % (len(json.load(open(SEATS, encoding="utf-8")).get("seats", [])), len(faults)))
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
