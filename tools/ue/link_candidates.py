#!/usr/bin/env python3
"""Show the game project the MetaHuman candidates built on drive F, without copying them.

    python tools/ue/link_candidates.py            # links MH_<Who>C<n> and Speech into ue-probe
    python tools/ue/link_candidates.py --remove   # takes the links away again
    python tools/ue/link_candidates.py --selftest

WHY, 25 September. Fifteen built candidates are about 6 GB, drive C: has about
4 GB free, and the portrait tool that photographs them runs in the game
project on C:. So they are built in the scratch copy on F:
(F:/LedgerTools/mh-dress) and each folder is linked into
ue-probe/Content/Ledger/MetaHumans (a directory junction: Windows shows the F:
folder at the C: path, nothing is copied). That folder is outside the public
repository (.gitignore), and --remove deletes only the links, never what they
point to.
"""
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = r"F:\LedgerTools\mh-dress\Content\Ledger\MetaHumans"
DST = os.path.join(REPO, "ue-probe", "Content", "Ledger", "MetaHumans")
PATTERN = re.compile(r"^(MH_(Lena|Rocco|Sam)C\d|Speech)$")


def wanted(names):
    return sorted(n for n in names if PATTERN.match(n))


def is_junction(path):
    try:
        return bool(os.readlink(path))
    except (OSError, ValueError):
        return False


def link():
    made = 0
    for n in wanted(os.listdir(SRC)):
        target, here = os.path.join(SRC, n), os.path.join(DST, n)
        if os.path.exists(here):
            continue
        subprocess.run(["cmd", "/c", "mklink", "/J", here, target], check=True, capture_output=True)
        made += 1
    print("link_candidates: %d linked, %d present" % (made, len(wanted(os.listdir(DST)))))


def remove():
    gone = 0
    for n in wanted(os.listdir(DST)):
        here = os.path.join(DST, n)
        if is_junction(here):
            os.rmdir(here)          # removes the link only, never the folder it points to
            gone += 1
    print("link_candidates: %d links removed" % gone)


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("link_candidates selftest FAIL " + name)
    check("the candidates and the speech are linked, nothing else",
          wanted(["MH_LenaC1", "MH_RoccoC5", "MH_SamC3", "Speech", "MH_LenaT2", "MH_Test", "Clothing"]) == ["MH_LenaC1", "MH_RoccoC5", "MH_SamC3", "Speech"])
    check("the links land in the ignored MetaHuman folder", DST.replace("\\", "/").endswith("ue-probe/Content/Ledger/MetaHumans"))
    print("link_candidates selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(remove() if "--remove" in sys.argv else link())
