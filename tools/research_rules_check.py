"""Three of 21 November's rulings, as one build check (advisor 297).

  unreal    while RULINGS.md carries "no Unreal work until the prototype", no commit since the ruling entered
            RULINGS (21 Nov 10:24) touches ue-probe/. The Monday audit backs it.
  builton   every sheet in production/research/lane/measurements/ (STATUS.md excepted) carries a "Built on" line
            naming the earlier research read (advisor 294). Sheets written before the check, listed in OWED
            below, are named each run until their section lands; any other sheet without one fails.
  mafia     no Mafia game listed to be measured or compared in the measuring sheets, FEEL-MEASUREMENT-METHOD or
            the waiting list (his 17 Nov outside-only line): a line naming Mafia fails unless it says the game is
            set aside, dropped or never used, or the line cites earlier research (a "Built on" or study line).

Prints one line per finding and a last line "researchRules ok" or "researchRules FAIL ...". --selftest checks the
three detectors on made-up text.
"""
import glob
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHEETS = "production/research/lane/measurements"
RULING_TEXT = "no Unreal work until the prototype"
RULING_SINCE = "2026-11-21 10:25"
OWED = {  # written before the check (21 Nov 21:51); each gets its section, then leaves this list
    "car-chases-sheet-2026-11-21.md",
    "gtavi-being-seen-builder-2026-11-21.md", "gtavi-driving-builder-2026-11-21.md",
    "gtavi-g-rows-builder-2026-11-21.md",
}
BUILT_ON = re.compile(r"^\W*built on\b", re.I | re.M)
MAFIA = re.compile(r"\bmafia\b", re.I)
EXEMPT = re.compile(r"set aside|dropped|never|not a reference|no longer|built on|\bstudy\b|studies/|rebuilt from|"
                    r"his ruling|outside-only", re.I)


def unreal_findings(rulings, commits):
    if RULING_TEXT not in rulings:
        return []
    return ["unreal: commit %s touches ue-probe while the prototype ruling stands" % c for c in commits]


def builton_findings(sheets):
    out = []
    for name, text in sorted(sheets.items()):
        if name == "STATUS.md" or BUILT_ON.search(text):
            continue
        out.append(("owed" if name in OWED else "FAIL", "builton: %s has no Built on section" % name))
    return out


def mafia_findings(files):
    out = []
    for name, text in sorted(files.items()):
        for n, line in enumerate(text.splitlines(), 1):
            if MAFIA.search(line) and not EXEMPT.search(line):
                out.append("mafia: %s:%d lists Mafia without setting it aside" % (name, n))
    return out


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def run():
    rulings = read(os.path.join(ROOT, "RULINGS.md"))
    commits = subprocess.run(["git", "log", "--since=" + RULING_SINCE, "--format=%h", "--", "ue-probe"],
                             cwd=ROOT, capture_output=True, text=True).stdout.split()
    sheets = {os.path.basename(p): read(p) for p in glob.glob(os.path.join(ROOT, SHEETS, "*.md"))}
    lane = os.path.join(ROOT, "production/research/lane")
    watched = dict(sheets)
    for pat in ("FEEL-MEASUREMENT-METHOD*.md", "*WAITING*.md", "MEASUREMENTS-NEEDED*.md"):
        for p in glob.glob(os.path.join(lane, pat)):
            watched[os.path.basename(p)] = read(p)
    fails = unreal_findings(rulings, commits) + mafia_findings(watched)
    for kind, msg in builton_findings(sheets):
        print(("owed " if kind == "owed" else "") + msg)
        if kind == "FAIL":
            fails.append(msg)
    for msg in fails:
        print(msg)
    print("researchRules FAIL %d" % len(fails) if fails else "researchRules ok")
    return 1 if fails else 0


def selftest():
    assert unreal_findings("x " + RULING_TEXT + " y", ["abc"]) and not unreal_findings("lifted", ["abc"])
    f = builton_findings({"a.md": "# A\nBuilt on, read 21 Nov: x", "b.md": "# B\nno section",
                          "car-chases-sheet-2026-11-21.md": "x", "STATUS.md": "x"})
    assert [k for k, _ in f] == ["FAIL", "owed"], f
    m = mafia_findings({"s.md": "Mafia DE: 20 min to measure\nMafia DE: set aside (his ruling)\n"
                                "Built on study 01 (KCD2 and Mafia data)"})
    assert len(m) == 1 and ":1 " in m[0], m
    print("researchRules selftest ok")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else run())
