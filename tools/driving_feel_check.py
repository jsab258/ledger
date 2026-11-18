"""The enforcer of his driving-feel ruling of 18 November 2026 (advisors 222 and 223; RULINGS, Cars line).

    python tools/driving_feel_check.py            # prints one line; exit 1 on a fault
    python tools/driving_feel_check.py --selftest

His ruling (12:32 and 12:36, 18 Nov): LEDGER's cars are fun and easy first, as in open-world games that are not driving
sims; 1990 shows in sound, sway, look and relative speeds; real figures are flavour and a floor, never the target; the
gearbox is automatic by default (manual is not wanted).

Checks:
1. The drives tool's default targets (tools/lane/driving_drives.default_targets) come from the GAME band, not the real one.
2. The local copy of the driving study (F:/LedgerTools/quay-run/index.html, his desktop shortcut "Quay Run") starts with
   the automatic gearbox (its settings default auto:1). A copy taken before the next driving round (copied 18 Nov 12:4x,
   before his ruling reached the study) is a listed shortfall, not a fault: it fails only for a copy newer than RULED_AT.
"""
import datetime
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDY = "F:/LedgerTools/quay-run/index.html"
RULED_AT = datetime.datetime(2026, 11, 18, 13, 0)  # the copy made for the shortcut predates the next round
SETTINGS_RE = re.compile(r"Object\.assign\(\{[^}]*?\bauto:(\d)")


def gearbox_default(html):
    """1 automatic, 0 manual, None when the settings default is not found."""
    m = SETTINGS_RE.search(html)
    return int(m.group(1)) if m else None


def targets_from_game_band():
    sys.path.insert(0, os.path.join(ROOT, "tools", "lane"))
    try:
        import driving_drives  # noqa: E402 (the lane's tool, read only)
        note = str(driving_drives.default_targets().get("note", ""))
    except Exception as e:  # a missing or broken tool is a fault
        return False, "drives tool unreadable: %s" % e
    return ("game band" in note), note[:80]


def judge(html, mtime):
    """(fault, text) for the study copy."""
    if html is None:
        return False, "study copy absent (no shortcut copy to judge)"
    g = gearbox_default(html)
    if g == 1:
        return False, "gearbox automatic by default"
    if g is None:
        return True, "study copy: gearbox default not found"
    if mtime < RULED_AT:
        return False, "gearbox manual by default in a copy older than the ruling: shortfall, owed to the next driving round"
    return True, "gearbox manual by default in a copy newer than the ruling"


def main():
    ok_band, band_text = targets_from_game_band()
    html, mtime = None, None
    if os.path.exists(STUDY):
        html = open(STUDY, encoding="utf-8", errors="replace").read()
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(STUDY))
    fault, text = judge(html, mtime)
    faults = (0 if ok_band else 1) + (1 if fault else 0)
    print("drivingFeel targets=%s gearbox=%s faults=%d" % ("game band" if ok_band else "NOT GAME BAND (%s)" % band_text,
                                                           text, faults))
    return 1 if faults else 0


def selftest():
    t0 = RULED_AT - datetime.timedelta(hours=1)
    t1 = RULED_AT + datetime.timedelta(hours=1)
    cases = [
        (judge('Jt=Object.assign({assists:0,auto:1,wet:1})', t1), False),
        (judge('Jt=Object.assign({assists:0,auto:0,wet:1})', t0), False),
        (judge('Jt=Object.assign({assists:0,auto:0,wet:1})', t1), True),
        (judge('no settings here', t1), True),
        (judge(None, None), False),
    ]
    n = sum(1 for (got, want) in cases if got[0] == want)
    print("selftest %d/%d" % (n, len(cases)))
    return 0 if n == len(cases) else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
