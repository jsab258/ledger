#!/usr/bin/env python3
"""THE ROOM TEST'S VERDICTS INTO THE SEATS (his order of 28 October 2026, D10; the sitting method's step 4,
production/research/sit-and-turn/SPOTS-2026-10-28.md).

    python tools/seats_kept.py 0=ue-probe/Saved/Logs/sit-room.log 1=ue-probe/Saved/Logs/sit-room-1.log ...
    python tools/seats_kept.py --selftest

The game's room test (-TomSitRoomTest -TomSitRoomSeat=N, SliceCharacter.cpp) plays every In clip of a seat from
inside the room and logs each "LedgerSitRoom: <side> KEPT" or "DROPPED", then one "ledgerSitRoom=" line. Kingdom
Come II plays only the entries its tests keep, so each seat's kept entries are written to production/specs/seats.json
as "in_kept" (the game chooses among them, TryStartSitApproach), with "in_kept_from" naming the test. A log that
did not finish (no "ledgerSitRoom=" line) or names another seat writes nothing for that seat.

A log of every In clip sets "in_kept" and starts "in_kept_starts_cm" afresh: each kept entry passed at that run's start
distance. A log of fewer clips (-TomSitRoomClips, another -TomSitRoomRemainCm) adds or removes its distance for the
kept entries it tried; the game seeks its start only inside the distances each entry passed (28 October: one window
of 30 cm let his stride line up with the clip's on no walk-in of nine).
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEATS = os.path.join(ROOT, "production", "specs", "seats.json")
VERDICT = re.compile(r"LedgerSitRoom: (\S+) (KEPT|DROPPED)\s*$")
DONE = re.compile(r"ledgerSitRoom=(\S+)(?: seat=(\d+))? kept=(\d+) of (\d+) entries, starts (\d+) cm")
STAMP = re.compile(r"^\[(\d{4})\.(\d\d)\.(\d\d)-")


def read_log(text):
    """(kept sides, dropped sides, the seat the log names or None, starts cm, date) or None if unfinished."""
    kept, dropped, done, date = [], [], None, None
    for line in text.splitlines():
        m = VERDICT.search(line)
        if m:
            (kept if m.group(2) == "KEPT" else dropped).append(m.group(1))
        d = DONE.search(line)
        if d:
            done = d
            s = STAMP.search(line)
            date = "%s-%s-%s" % s.groups() if s else None
    if done is None or len(kept) != int(done.group(3)) or len(kept) + len(dropped) != int(done.group(4)):
        return None
    return kept, dropped, (int(done.group(2)) if done.group(2) else None), int(done.group(5)), date


def apply(seats, index, verdict, log_name):
    """Write one seat's kept entries; returns the fault, or None."""
    kept, dropped, named, starts, date = verdict
    if named is not None and named != index:
        return "the log names seat %d, not %d" % (named, index)
    s = seats["seats"][index]
    full = {x: [c for c in s.get("in", []) if c == "M_interaction_bench_into_%s_Montage" % x] for x in kept + dropped}
    missing = [x for x, c in full.items() if not c]
    if missing:
        return "sides not among the seat's In clips: %s" % missing
    if len(kept) + len(dropped) >= len(s.get("in", [])):
        s["in_kept"] = [full[x][0] for x in kept]
        s["in_kept_from"] = "the room test of %s (%s), every In clip from %d cm of its travel before the seat and the start envelope's four corners, the warp on: %d of %d kept" % (
            date or "?", log_name, starts, len(kept), len(kept) + len(dropped))
        s["in_kept_starts_cm"] = {full[x][0]: [starts] for x in kept}
        return None
    if "in_kept" not in s:
        return "a log of some clips before any log of all of them"
    # an entry passing at any tried distance is kept, with the distances it passed (29 October: R_090_Lfoot fits
    # the middle and counter-end seats from 100 cm and touches the room from 150, where the full run tried it)
    windows = s.setdefault("in_kept_starts_cm", {})
    for x in kept + dropped:
        clip = full[x][0]
        have = [d for d in windows.get(clip, []) if d != starts]
        windows[clip] = sorted(have + [starts]) if x in kept else sorted(have)
        if windows[clip] and clip not in s["in_kept"]:
            s["in_kept"].append(clip)
        if not windows[clip]:
            del windows[clip]
            if clip in s["in_kept"]:
                s["in_kept"].remove(clip)
    s["in_kept_from"] += "; %s (%s): from %d cm, %d of %d kept" % (date or "?", log_name, starts, len(kept), len(kept) + len(dropped))
    return None


def selftest():
    ok = bad = 0
    def check(name, cond):
        nonlocal ok, bad
        ok += 1 if cond else 0
        bad += 0 if cond else 1
        print("  %s %s" % ("ok  " if cond else "FAIL", name))
    log = "\n".join(["[2026.10.28-18.57.17:262][238]LogTemp: Display: LedgerSitRoom: F_Lfoot DROPPED",
                     "[2026.10.28-18.57.17:262][238]LogTemp: Display: LedgerSitRoom: BR_LFoot KEPT",
                     "[2026.10.28-18.57.44:418][273]LogTemp: Display: ledgerSitRoom=SOME-KEPT seat=1 kept=1 of 2 entries, starts 150 cm before the seat"])
    v = read_log(log)
    check("a finished log reads", v is not None and v[0] == ["BR_LFoot"] and v[2] == 1 and v[4] == "2026-10-28")
    check("an unfinished log reads as nothing", read_log(log.rsplit("\n", 1)[0]) is None)
    check("a count that disagrees reads as nothing", read_log(log.replace("kept=1", "kept=2")) is None)
    seats = {"seats": [{"in": ["M_interaction_bench_into_F_Lfoot_Montage", "M_interaction_bench_into_BR_LFoot_Montage"]}] * 2}
    seats = json.loads(json.dumps(seats))
    check("the log's seat must be the one written", apply(seats, 0, v, "x.log") is not None)
    check("kept entries written", apply(seats, 1, v, "x.log") is None and seats["seats"][1]["in_kept"] == ["M_interaction_bench_into_BR_LFoot_Montage"])
    check("a full log starts the distances afresh", seats["seats"][1]["in_kept_starts_cm"] == {"M_interaction_bench_into_BR_LFoot_Montage": [150]})
    part = read_log("\n".join(l for l in log.splitlines() if "F_Lfoot" not in l).replace("kept=1 of 2", "kept=1 of 1").replace("starts 150", "starts 200"))
    check("a log of some clips reads", part is not None and part[3] == 200)
    check("a log of some clips adds its distance", apply(seats, 1, part, "y.log") is None and seats["seats"][1]["in_kept_starts_cm"]["M_interaction_bench_into_BR_LFoot_Montage"] == [150, 200]
          and seats["seats"][1]["in_kept"] == ["M_interaction_bench_into_BR_LFoot_Montage"])
    other = read_log("\n".join(l for l in log.splitlines() if "BR_LFoot" not in l).replace("F_Lfoot DROPPED", "F_Lfoot KEPT").replace("kept=1 of 2", "kept=1 of 1").replace("starts 150", "starts 100"))
    check("an entry passing only at another distance becomes kept", other is not None and apply(seats, 1, other, "z.log") is None
          and "M_interaction_bench_into_F_Lfoot_Montage" in seats["seats"][1]["in_kept"]
          and seats["seats"][1]["in_kept_starts_cm"]["M_interaction_bench_into_F_Lfoot_Montage"] == [100])
    br_only = "\n".join(l for l in log.splitlines() if "F_Lfoot" not in l).replace("BR_LFoot KEPT", "BR_LFoot DROPPED").replace("kept=1 of 2", "kept=0 of 1")
    for d in (150, 200):
        apply(seats, 1, read_log(br_only.replace("starts 150", "starts %d" % d)), "w.log")
    check("an entry dropped at every distance it passed leaves in_kept",
          "M_interaction_bench_into_BR_LFoot_Montage" not in seats["seats"][1]["in_kept"]
          and "M_interaction_bench_into_BR_LFoot_Montage" not in seats["seats"][1]["in_kept_starts_cm"])
    seats["seats"][1]["in"] = ["M_interaction_bench_into_F_Lfoot_Montage"]
    check("a side not among the In clips refused", apply(seats, 1, v, "x.log") is not None)
    print("seats_kept selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    seats = json.load(open(SEATS, encoding="utf-8"))
    faults = 0
    for arg in argv:
        idx, path = arg.split("=", 1)
        v = read_log(open(path, encoding="utf-8", errors="replace").read())
        if v is None:
            print("seats_kept: %s did not finish; seat %s unchanged" % (path, idx))
            faults += 1
            continue
        why = apply(seats, int(idx), v, os.path.basename(path))
        if why:
            print("seats_kept: seat %s: %s" % (idx, why))
            faults += 1
            continue
        print("seats_kept: seat %s keeps %s" % (idx, v[0]))
    # the file's own line ends kept, so the change reads as the lines it changes
    crlf = b"\r\n" in open(SEATS, "rb").read()
    with open(SEATS, "w", encoding="utf-8", newline="\r\n" if crlf else "\n") as fh:
        json.dump(seats, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
