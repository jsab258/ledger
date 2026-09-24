#!/usr/bin/env python3
"""The integrated encounter, judged: the build's regression.

    python tools/encounter-verdict-check.py --sha abc1234 PLAY RELOAD UNSEEN
    python tools/encounter-verdict-check.py --selftest

Jafar, 24 September (ROADMAP.md, "Now"): the player commits a crime by their
own input; a witness sees it through the real perception; it spreads through
the real gossip and the conversation helper answers from the simulation's own
memory and day; there is an audible consequence; the player is questioned;
the game quits and a new process loads the save from disk and the town still
knows; and from a clean start an unseen crime is known by nobody. The Unreal
probe runs it as three launches (-Encounter=play, reload, unseen) and each
writes ue-encounter-<mode>-verdict.txt. This passes only when all three say
encounterStatus=PASS for this commit.
"""
import sys

MODES = ("play", "reload", "unseen")


def read(path):
    try:
        text = open(path, encoding="utf-8-sig", errors="replace").read()
    except OSError:
        return None
    out = {}
    for line in text.splitlines():
        for tok in line.split(" ") if not line.startswith("talkReply=") and not line.startswith("filedSummaryA=") else [line]:
            if "=" in tok:
                k, v = tok.split("=", 1)
                out.setdefault(k, v)
    return out


def judge(verdicts, sha):
    """[(mode, ok, why)] for the three runs, in order."""
    rows = []
    for mode, v in zip(MODES, verdicts):
        if v is None:
            rows.append((mode, False, "no-verdict-file"))
            continue
        if v.get("encounterMode") != mode:
            rows.append((mode, False, "wrong-mode/%s" % v.get("encounterMode")))
            continue
        commit = v.get("encounterCommit", "")
        if sha and not (commit.startswith(sha) or sha.startswith(commit) and commit):
            rows.append((mode, False, "stale/%s" % (commit or "no-commit")))
            continue
        if v.get("encounterStatus") != "PASS":
            rows.append((mode, False, "failed/%s" % v.get("encounterFailed", "unknown")))
            continue
        rows.append((mode, True, "held"))
    return rows


def main(argv):
    if "--selftest" in argv:
        return selftest()
    sha = argv[argv.index("--sha") + 1] if "--sha" in argv else ""
    paths = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or argv[i - 1] != "--sha")]
    if len(paths) != 3:
        print("encounterCheck status=USAGE need three verdict files: play, reload, unseen")
        return 2
    rows = judge([read(p) for p in paths], sha)
    ok = all(r[1] for r in rows)
    print("encounterCheck status=%s %s" % ("PASS" if ok else "FAIL",
          " ".join("%s=%s" % (m, w) for m, _, w in rows)))
    return 0 if ok else 1


def selftest():
    good = {"play": {"encounterMode": "play", "encounterStatus": "PASS", "encounterCommit": "abc1234"},
            "reload": {"encounterMode": "reload", "encounterStatus": "PASS", "encounterCommit": "abc1234"},
            "unseen": {"encounterMode": "unseen", "encounterStatus": "PASS", "encounterCommit": "abc1234"}}
    passed = failed = 0

    def check(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("encounter-verdict-check selftest FAIL " + name)
    check("three passes for this commit pass", all(r[1] for r in judge([good[m] for m in MODES], "abc1234")))
    bad = dict(good["reload"], encounterStatus="FAIL", encounterFailed="the-lad-still-knows")
    rows = judge([good["play"], bad, good["unseen"]], "abc1234")
    check("a failed reload fails and says why", not rows[1][1] and "the-lad-still-knows" in rows[1][2])
    check("a missing file fails", not judge([good["play"], None, good["unseen"]], "abc1234")[1][1])
    check("an older commit's verdict fails", not judge([dict(good["play"], encounterCommit="0000000"), good["reload"], good["unseen"]], "abc1234")[0][1])
    check("files in the wrong order fail", not judge([good["reload"], good["play"], good["unseen"]], "abc1234")[0][1])
    import tempfile, os
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as fh:
        fh.write("encounterMode=play\nencounterStatus=PASS\nencounterFailed=none\nencounterCommit=abc1234\ntalkReply=I know what happened. Was that you?\n")
        path = fh.name
    v = read(path)
    os.remove(path)
    check("a verdict file reads back", v and v.get("encounterStatus") == "PASS" and v.get("talkReply", "").startswith("I know"))
    print("encounter-verdict-check selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
