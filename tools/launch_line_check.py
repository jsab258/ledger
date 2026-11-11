#!/usr/bin/env python3
"""DID A PACKAGED PASS RUN ON THE PLAYER'S OWN LAUNCH LINE?

    python tools/launch_line_check.py LOG [LOG ...]   # each game log's "Command Line:"; exit 1 on any test switch
    python tools/launch_line_check.py --line "-LedgerSlice -MickeysInside"
    python tools/launch_line_check.py --selftest

WHY, 8 November 2026 (n02-9-pass-is-players-launch; the exit rehearsal's gap,
production/audits/phase1-exit/CLOSE-BRIEF-2026-11-09.md, Exit A): Mickey's office
and sitting "passed packaged" for days while they were on only behind the test
switches -MickeysInside and -TomSit; the player's game had neither until 7 Nov.
A piece passes only in the game the player plays, so a pass's evidence must be a
run whose launch line is the player's plus switches that only watch or steer.

THE PLAYER'S LINE is what a plain double-click gets: a cooked game with no mode
appends -LedgerSlice -LedgerCrime -Encounter=live (ue-probe LedgerProbe.cpp,
StartupModule), and the friends' shortcut adds -EncounterSave (tools/friends/
evening.ps1). WATCH-ONLY switches change the window, the timing, the logs or how
the tester steers, never the world (play.py's own launch, the editor-photograph
list). Anything else the game reads is a TEST switch and fails the pass. Two are
allowed with a note, since they change one thing a reviewer must know: -TalkFake
(talk is the stand-in, so the run says nothing about talk) and -NoTitle (the title
menu skipped). Unknown switches count as test switches: a new one must be added
here, on purpose, before a pass can carry it.
"""
import re
import sys

PLAYER = {"ledgerslice", "ledgercrime", "encounter=live", "encountersave="}
WATCH = {"windowed", "fullscreen", "resx=", "resy=", "nosplash", "unattended", "nopause", "benchmark", "fps=",
         "abslog=", "log", "ledgerrepo=", "talkhelper=", "livefresh", "routewalk", "preparedack",
         "dpcvars=slate.forcerawinputsimulation=1", "ini:engine:[audio]:unfocusedvolumemultiplier=1.0",
         "execcmds=scalability 2", "forceres", "log="}  # the shipped picture level is High, scalability 2 (photograph-at-the-played-level)
NOTED = {"talkfake": "talk is the stand-in: the run says nothing about talk",
         "notitle": "the title menu skipped"}
# CAMERA modes only place a camera and take pictures (OfficeLook: CrimeProbe.cpp, its screenshot requests);
# the variants that remove people or others change the frame and stay test switches.
CAMERA = {"officelook", "officelooknight", "officelookhere", "pageshots=", "pageshotsize=", "pageshotsettle=",
          "titleshot=", "landingshot="}


def switches(line):
    """The -switches of a command line, lower case, values kept for exact matches and cut to 'name=' otherwise."""
    parts = re.findall(r'-[^\s"]*"[^"]*"|\S+', line)  # -ExecCmds="scalability 2" stays one switch
    out = []
    for p in parts:
        if not p.startswith("-"):
            continue
        s = p[1:].strip('"').replace('"', "").lower()
        out.append(s)
    return out


def judge(line):
    """(verdict, test switches, notes): PLAYER, PLAYER+WATCH or TEST."""
    test, notes, watched = [], [], False
    for s in switches(line):
        key = s.split("=", 1)[0] + "=" if "=" in s else s
        if s in PLAYER or key in PLAYER:
            if key == "encounter=" and s != "encounter=live":
                test.append(s)
            continue
        if s in WATCH or (key in WATCH and key not in ("dpcvars=", "ini:engine:[audio]:unfocusedvolumemultiplier=", "execcmds=")):
            watched = True
            continue
        if s in CAMERA or key in CAMERA:
            if "a camera mode: pictures, not play" not in notes:
                notes.append("a camera mode: pictures, not play")
            watched = True
            continue
        if s in NOTED:
            notes.append(NOTED[s])
            watched = True
            continue
        test.append(s)
    verdict = "TEST" if test else ("PLAYER+WATCH" if watched else "PLAYER")
    return verdict, test, notes


def from_log(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        for ln in f:
            m = re.search(r"Command Line:\s*(.*)$", ln)
            if m:
                return m.group(1).strip()
    return None


def last_command_line(path):
    """The LAST "Command Line:" in a log (8 Nov, the lean QA's step 2): a walk's log ends with its relaunch, the
    Continue, so the night report judges the launch the walk finished on. None when the file or the line is missing."""
    last = None
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for ln in f:
                m = re.search(r"Command Line:\s*(.*)$", ln)
                if m:
                    last = m.group(1).strip()
    except OSError:
        return None
    return last


def describe(line):
    """One plain sentence for the night report: what the walk ran on."""
    if line is None:
        return "launch line not found"
    v, test, notes = judge(line)
    if v == "TEST":
        return "a test launch: " + ", ".join("-" + t for t in test)
    return v + (" (" + "; ".join(notes) + ")" if notes else "")


def stamp(out_dir, line):
    """Every pass's launch judged where its pictures are kept (11 Nov, n09-9: the launch check on every pass): writes
    launch.txt beside command.txt with the verdict sentence and returns it, so a reviewer or a page item reading the
    folder sees at once whether the pictures came from the player's game or a test launch."""
    import os
    s = describe(line)
    with open(os.path.join(out_dir, "launch.txt"), "w", encoding="utf-8") as f:
        f.write(s + "\n")
    return s


def selftest():
    cases = [
        ("a plain double-click", "", "PLAYER"),
        ("the friends' shortcut", '-EncounterSave="C:/x/save"', "PLAYER"),
        ("the 8 Nov office wall walk", "-LedgerSlice -LedgerCrime -Encounter=live -TalkHelper=C:\\t\\TalkHelper.exe -TalkFake "
         "-EncounterSave=F:/w -windowed -ResX=1280 -ResY=720 -nosplash -dpcvars=Slate.ForceRawInputSimulation=1 "
         "-ini:Engine:[Audio]:UnfocusedVolumeMultiplier=1.0 -RouteWalk", "PLAYER+WATCH"),
        ("the 8 Nov sit proof", '-LedgerSlice -LedgerCrime -Encounter=live -LiveFresh -TalkFake -NoTitle -MickeysInside -windowed '
         '-unattended -nosplash -nopause -benchmark -fps=60 -ExecCmds="scalability 2" -SitProof -SitProofExit -abslog=F:/s.log', "TEST"),
        ("another encounter", "-LedgerSlice -LedgerCrime -Encounter=staged", "TEST"),
        ("another picture level", '-ExecCmds="scalability 3"', "TEST"),
        ("another console setting", "-dpcvars=r.Lumen.Enabled=0", "TEST"),
        ("an unknown switch", "-SomethingNew", "TEST"),
        ("the office's night pictures", "-LedgerSlice -LedgerCrime -Encounter=live -NoTitle -OfficeLookNight -forceres -log=o.log", "PLAYER+WATCH"),
        ("pictures with the people taken out", "-OfficeLook -OfficeLookNoPeople", "TEST"),
    ]
    failed = 0
    for name, line, want in cases:
        got = judge(line)[0]
        ok = got == want
        failed += 0 if ok else 1
        print("%s %s: %s (want %s)" % ("ok  " if ok else "FAIL", name, got, want))
    v, test, _ = judge(cases[3][1])
    ok = set(test) == {"mickeysinside", "sitproof", "sitproofexit"}
    failed += 0 if ok else 1
    print("%s the sit proof names exactly its three test switches: %s" % ("ok  " if ok else "FAIL", ", ".join(test)))
    # the lean QA's step 2 (8 Nov): the last line of a log, and the night report's sentence
    import tempfile, os
    extra = []
    d = tempfile.mkdtemp()
    two = os.path.join(d, "two.log")
    with open(two, "w", encoding="utf-8") as fh:
        fh.write("LogInit: Command Line: -LedgerSlice -MickeysInside\nother\nLogInit: Command Line: -LedgerSlice -RouteWalk\n")
    extra.append(("two launches: the last is read", last_command_line(two) == "-LedgerSlice -RouteWalk"))
    extra.append(("two launches: from_log keeps the first", from_log(two) == "-LedgerSlice -MickeysInside"))
    extra.append(("no log: launch line not found", describe(last_command_line(os.path.join(d, "none.log"))) == "launch line not found"))
    extra.append(("the sentence names the test switch", describe("-LedgerSlice -MickeysInside") == "a test launch: -mickeysinside"))
    extra.append(("the sentence carries the stand-in note", describe("-LedgerSlice -TalkFake -RouteWalk")
                  == "PLAYER+WATCH (talk is the stand-in: the run says nothing about talk)"))
    for name, ok in extra:
        failed += 0 if ok else 1
        print("%s %s" % ("ok  " if ok else "FAIL", name))
    n = len(cases) + 1 + len(extra)
    print("launch_line_check selftest: passed=%d/%d failed=%d" % (n - failed, n, failed))
    return 1 if failed else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--line" in argv:
        items = [("(line)", argv[argv.index("--line") + 1])]
    else:
        items = [(p, from_log(p)) for p in argv if not p.startswith("--")]
    bad = 0
    for name, line in items:
        if line is None:
            print("launch-line file=%s verdict=NO-LINE (no 'Command Line:' in it; not evidence)" % name)
            bad += 1
            continue
        v, test, notes = judge(line)
        bad += v == "TEST"
        print("launch-line file=%s verdict=%s%s%s" % (name, v, (" test=" + ",".join(test)) if test else "",
                                                     (" note=" + "; ".join(notes)) if notes else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
