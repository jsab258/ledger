#!/usr/bin/env python3
"""THE CORNER'S PEOPLE, READ FROM A PACKAGED RUN'S LOG (n02-4-corner-people).

    python tools/corner_people.py [log]    # default: the played copy's newest log holding these lines
    python tools/corner_people.py --selftest

The plan's four checks as the game logs them: no frozen poses (LedgerMotion), people walk off
(LedgerWalkOff, with each walk's worst foot slip), someone reacts (LedgerReact, LedgerAfter), and
who could take in the window (LedgerWitness, what blocks each line). Nobody overlapping is not
logged: that one stays with the step pictures. A screen for the reader, not a pass.
"""
import collections, glob, os, re, sys

LOGS = "F:/LedgerTools/played-game/Windows/LedgerProbe/Saved/Logs"
LINE = re.compile(r"(Ledger(?:Motion|WalkOff|React|Witness|After)): (.*)$")


def newest():
    for p in sorted(glob.glob(LOGS + "/*.log"), key=os.path.getmtime, reverse=True):
        with open(p, encoding="utf8", errors="replace") as f:
            if any("LedgerMotion:" in l for l in f):
                return p
    return None


def read(lines):
    r = {"motion": collections.Counter(), "frozen": collections.Counter(), "unmeasured": set(), "walks": 0,
         "ends": collections.Counter(), "blocked": [], "slips": [], "react": [], "after": [], "witness": []}
    for l in lines:
        m = LINE.search(l)
        if not m:
            continue
        kind, t = m.group(1), m.group(2).strip()
        if kind == "LedgerMotion":
            if " not measured" in t:
                r["unmeasured"].add(t.split(" not measured")[0])
                continue
            who = t.split(" head ")[0]
            r["motion"][who] += 1
            if t.endswith("frozen") or "FROZEN" in t:
                r["frozen"][who] += 1
        elif kind == "LedgerWalkOff":
            if "blocked at once" in t:
                r["blocked"].append(t)
            elif " off the street " in t:
                r["ends"]["off the street"] += 1
            elif " stands at " in t:
                r["ends"]["stood at the end"] += 1
                s = re.search(r"worst slip ([\d.]+) cm", t)
                if s:
                    r["slips"].append((float(s.group(1)), t.split(" stands at ")[0]))
            elif re.search(r" from \(.*\) to \(", t):
                r["walks"] += 1
        elif kind == "LedgerReact":
            r["react"].append(t)
        elif kind == "LedgerAfter":
            r["after"].append(t)
        else:
            s = re.search(r"sightline (.*?), to the window ([\d.]+) m (.*?), light", t)
            if s:
                r["witness"].append((t.split(" ")[0], s.group(1), s.group(2), s.group(3)))
    return r


def show(r):
    n, f = sum(r["motion"].values()), sum(r["frozen"].values())
    print("frozen: %d of %d readings, %d people%s" % (f, n, len(r["motion"]), "; " + ", ".join(
        "%s %d" % kv for kv in r["frozen"].most_common(8)) if f else ""))
    if r["unmeasured"]:
        print("not measured: " + ", ".join(sorted(r["unmeasured"])[:8]))
    print("walks: %d set off; %s; %d blocked at once" % (r["walks"], ", ".join(
        "%d %s" % (v, k) for k, v in r["ends"].items()) or "none ended", len(r["blocked"])))
    if r["slips"]:
        print("worst foot slips: " + ", ".join("%s %.1f cm" % (w, s) for s, w in sorted(r["slips"], reverse=True)[:4]))
    print("reacts: %d lines" % len(r["react"]))
    for t in r["react"][:12] + r["after"][:8]:
        print("  " + t[:150])
    print("witness lines: %d" % len(r["witness"]))
    for w, him, m, glass in r["witness"][:16]:
        print("  %s: to him %s; to the window %s m %s" % (w, him, m, glass))


def selftest():
    lines = ["x LogTemp: Display: LedgerMotion: A head 0.3 hands 3.7 chest 0.2 cm in 4 s (ends alone 0.1), extra, frozen",
             "x LogTemp: Display: LedgerMotion: A head 3.3 hands 3.7 chest 0.2 cm in 4 s, extra, moving",
             "x LogTemp: Display: LedgerWalkOff: sam walks from (1.00, 1.00) to (2.00, 2.00), 1.6 m in 1 leg(s), at D0 13:00",
             "x LogTemp: Display: LedgerWalkOff: sam stands at (2.00, 2.00), 4 cm from the walk's end, 3.5 s after setting off; feet down 2 times, worst slip 51.0 cm",
             "x LogTemp: Display: LedgerWitness: ron where he sees them, their day says quay, 3.0 m off-axis 10, sightline clear, to the window 4.0 m clear, light 0.50 (lamp none), met on 1 day(s), familiarity 0.20"]
    r = read(lines)
    ok = (sum(r["motion"].values()) == 2 and sum(r["frozen"].values()) == 1 and r["walks"] == 1
          and r["slips"] == [(51.0, "sam")] and r["witness"] == [("ron", "clear", "4.0", "clear")])
    print("corner_people selftest: %s" % ("passed" if ok else "FAILED"))
    return 0 if ok else 1


def main():
    if "--selftest" in sys.argv:
        return selftest()
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    p = args[0] if args else newest()
    if not p:
        print("no log holds these lines")
        return 1
    print(p)
    with open(p, encoding="utf8", errors="replace") as f:
        show(read(f))
    return 0


if __name__ == "__main__":
    sys.exit(main())
