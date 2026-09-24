#!/usr/bin/env python3
"""Approvals that live beside what they approve, and lapse by themselves.

    python tools/approvals.py                 # every approval, and what is in the game without one
    python tools/approvals.py --record THING --against SRC [SRC ...] [--by Jafar] [--note "..."]
    python tools/approvals.py --selftest

WHY, 24 September. Jafar, after the production pipeline audit: "An approval
lives beside the thing it approves, with what it was approved against. When
that source changes, a canon rule, a spec, a voice, the approval lapses by
itself, and the build flags anything placed in the game without a current
approval." (production/audits/2026-09-24-production-pipeline-audit.md.)

AN APPROVAL is a file named <thing>.approval.json beside the thing:
    {"approves": "<repo path of the thing>", "by": "Jafar", "on": "2026-09-25",
     "note": "...", "against": {"<source>": "<sha1 of its text>", ...}}
A source is a repo path, or a path and a markdown heading, "canon.md#The
content rule", which pins that one section, so a change elsewhere in canon
does not lapse everything. The thing itself is always among its sources: an
approved sheet that is then edited is no longer the sheet he approved.

WHAT IS IN THE GAME is production/specs/in-game.json: a short list of what
the playable build uses (the cast, their voices, the dialogue banks, the
look), each naming the thing its approval sits beside.

THE BUILD FLAGS, IT DOES NOT FAIL: the verdict line and the flagged list go
to the log and the exit code is 0. An approval FILE that is malformed or names
a source that does not exist is a fault, and that exits 1.
"""
import hashlib
import json
import os
import re
import sys
from datetime import date

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN_GAME = os.path.join("production", "specs", "in-game.json")
SUFFIX = ".approval.json"


def _read(rel):
    with open(os.path.join(REPO, rel), "rb") as fh:
        return fh.read()


def section(text, heading):
    """The text under a markdown heading, down to the next heading of the same or a higher level."""
    lines = text.splitlines()
    start = level = None
    for i, line in enumerate(lines):
        m = re.match(r"^(#+)\s+(.*?)\s*$", line)
        # A heading is named by how it starts: "The content rule" names
        # "## The content rule (D18, permanent)".
        if m and start is None and m.group(2).strip().lower().startswith(heading.strip().lower()):
            start, level = i, len(m.group(1))
        elif m and start is not None and len(m.group(1)) <= level:
            return "\n".join(lines[start:i])
    return "\n".join(lines[start:]) if start is not None else None


def fingerprint(source):
    """The sha1 of a source's text (line endings normalised), or None if it does not exist."""
    path, _, heading = source.partition("#")
    try:
        raw = _read(path)
    except OSError:
        return None
    text = raw.decode("utf-8", errors="replace").replace("\r\n", "\n")
    if heading:
        text = section(text, heading)
        if text is None:
            return None
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def approval_path(thing):
    return thing + SUFFIX


def load(rel):
    doc = json.loads(_read(rel).decode("utf-8"))
    if not isinstance(doc.get("against"), dict) or not doc.get("approves") or not doc.get("by"):
        raise ValueError("needs approves, by and against")
    return doc


def status(doc):
    """current, or lapsed with the sources that changed, or broken with the ones that vanished."""
    changed, gone = [], []
    for src, want in doc["against"].items():
        have = fingerprint(src)
        if have is None:
            gone.append(src)
        elif have != want:
            changed.append(src)
    if gone:
        return "broken", gone
    if changed:
        return "lapsed", changed
    return "current", []


def all_approvals():
    found = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "Library", "Intermediate", "Saved", "Binaries", "legacy")]
        for f in files:
            if f.endswith(SUFFIX):
                found.append(os.path.relpath(os.path.join(root, f), REPO).replace("\\", "/"))
    return sorted(found)


def in_game():
    try:
        return json.loads(_read(IN_GAME).decode("utf-8")).get("placed", [])
    except OSError:
        return None


def verdict(approvals, placed):
    """(summary line, flagged lines, faults)."""
    states, faults = {}, []
    for rel in approvals:
        try:
            doc = load(rel)
        except (ValueError, json.JSONDecodeError) as e:
            faults.append("%s malformed: %s" % (rel, e))
            continue
        st, which = status(doc)
        states[doc["approves"]] = (st, which, rel)
        if st == "broken":
            faults.append("%s names sources that do not exist: %s" % (rel, ", ".join(which)))
    flagged = []
    for p in placed or []:
        thing = p.get("thing", "")
        st = states.get(thing)
        if st is None:
            flagged.append("NO APPROVAL  %s (%s)" % (p.get("what", thing), thing))
        elif st[0] != "current":
            flagged.append("%s  %s (%s): %s" % (st[0].upper(), p.get("what", thing), thing, ", ".join(st[1])))
    n_placed = len(placed or [])
    line = ("approvals: files=%d current=%d lapsed=%d broken=%d placedInGame=%s placedWithoutCurrentApproval=%d faults=%d"
            % (len(approvals), sum(1 for s in states.values() if s[0] == "current"),
               sum(1 for s in states.values() if s[0] == "lapsed"), sum(1 for s in states.values() if s[0] == "broken"),
               n_placed if placed is not None else "UNREAD", len(flagged), len(faults)))
    return line, flagged, faults


def record(thing, sources, by, note):
    srcs = [thing] + [s for s in sources if s != thing]
    against = {}
    for s in srcs:
        fp = fingerprint(s)
        if fp is None:
            raise SystemExit("approvals: cannot record, %s does not exist" % s)
        against[s] = fp
    doc = {"approves": thing, "by": by, "on": date.today().isoformat(), "note": note, "against": against}
    out = os.path.join(REPO, approval_path(thing))
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1)
        fh.write("\n")
    print("approvals: recorded %s against %d source(s)" % (approval_path(thing), len(against)))


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("approvals selftest FAIL " + name)
    md = "# A\nintro\n## The content rule\nno drink\n## Other\nx\n"
    check("a heading's section stops at the next heading of its level", section(md, "The content rule") == "## The content rule\nno drink")
    check("a missing heading is no section", section(md, "Nope") is None)
    fp_canon = fingerprint("canon.md")
    check("a real source has a fingerprint", fp_canon is not None and len(fp_canon) == 40)
    check("a missing source has none", fingerprint("no/such/file.json") is None)
    check("a section of canon has its own fingerprint", fingerprint("canon.md#The content rule") not in (None, fp_canon))
    good = {"approves": "canon.md", "by": "Jafar", "against": {"canon.md": fp_canon}}
    check("an approval against unchanged sources is current", status(good) == ("current", []))
    stale = {"approves": "canon.md", "by": "Jafar", "against": {"canon.md": "0" * 40}}
    check("an approval whose source changed has lapsed, and says which", status(stale) == ("lapsed", ["canon.md"]))
    gone = {"approves": "x", "by": "Jafar", "against": {"no/such/file.json": "0" * 40}}
    check("an approval whose source vanished is broken", status(gone)[0] == "broken")
    _, flagged, _ = verdict([], [{"thing": "production/x/sheet.md", "what": "a sheet"}])
    check("a thing in the game with no approval is flagged", flagged == ["NO APPROVAL  a sheet (production/x/sheet.md)"])
    line, _, faults = verdict([], [])
    check("nothing placed and nothing approved is a clean line with denominators", "files=0" in line and "placedInGame=0" in line and not faults)
    check("the approval file sits beside the thing", approval_path("a/b.md") == "a/b.md.approval.json")
    print("approvals selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--record" in argv:
        i = argv.index("--record")
        thing = argv[i + 1]
        sources = []
        if "--against" in argv:
            j = argv.index("--against") + 1
            while j < len(argv) and not argv[j].startswith("--"):
                sources.append(argv[j])
                j += 1
        by = argv[argv.index("--by") + 1] if "--by" in argv else "Jafar"
        note = argv[argv.index("--note") + 1] if "--note" in argv else ""
        record(thing, sources, by, note)
        return 0
    placed = in_game()
    line, flagged, faults = verdict(all_approvals(), placed)
    print(line)
    for f in flagged:
        print("  " + f)
    for f in faults:
        print("  FAULT " + f)
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
