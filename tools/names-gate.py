#!/usr/bin/env python3
"""No retired name in anything the player sees or hears.

    python tools/names-gate.py              # exit 1 and every hit, or 0
    python tools/names-gate.py --selftest

WHY, 25 September. Jafar ruled the casting research's renames on 24
September (DECISIONS; canon.md, the NAMES block): Lena became Sheila Dunn,
Rocco Ron Kirby, Sam Darren Milner, and so on, and "the old names survive
only as internal ids ... never what the player sees or hears". The ruling
reached canon that night and nothing else: the talking characters' cards
still named themselves Lena Moreau, Rocco and Sam, the crowd said "I heard it
from Sam", the witnesses said Novak, and the game's own subtitles said "Sam,
Lena and Rocco are in the yard". This reads every place speech and on-screen
text come from and refuses a retired name in any of them.

WHAT COUNTS. A retired name with its capital, or in capitals, as a word:
internal ids are lower case (lena, rocco, novak) and stay. In source every
string literal is read; a line that must name one on purpose (an asset still
called MH_Lena, an old save migrated) carries "names-gate: allow".
Research notes, decision records and history keep the old names: they are
about the past, and nobody plays them.

THE LIST IS CANON'S. The self-test fails if a retired name here is missing
from canon's NAMES block, so the two cannot drift apart silently.
"""
import glob
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# retired -> canon name (for the message). "Danny Ro" first, so its "Ro" is
# never read alone.
# NOT BARE "VANE": Ada, whom canon keeps, is Ada Vane (a question for Jafar,
# 25 September), so only Aldous's own forms are refused.
RETIRED = [("Danny Ro", "Danny Cammack"), ("Vane, Holt", "Agar, Holt"), ("Lena", "Sheila"), ("Moreau", "Dunn"),
           ("Rocco", "Ron"), ("Sam", "Darren"), ("Mara", "Carol"), ("Aldous", "Geoffrey"),
           ("Sera", "Maureen"), ("Kest", "Jensen"), ("Noor", "Alison"), ("Farid", "Sedman"),
           ("Elias", "Philip"), ("Fisher", "Danby"), ("Novak", "Nowak"), ("Toma", "Tommy")]
# Surnames canon does not spell out, retired with the first name they went
# with (the card was "Lena Moreau"; canon says "Lena became Sheila Dunn").
WITH = {"Moreau": "Lena", "Farid": "Noor", "Fisher": "Elias", "Vane, Holt": "Aldous Vane"}
# With its capital, or all in capitals (a sign, a heading): "NOVAK" is a name too.
PATTERN = re.compile(r"\b(" + "|".join(re.escape(a) + "|" + re.escape(a.upper()) for a, _ in RETIRED)
                     + r")\b(?!\s+(?:Cammack|CAMMACK))")
CANON = {a.upper(): a for a, _ in RETIRED}
CANON.update({a: a for a, _ in RETIRED})
# A line that names a retired name ON PURPOSE (an old save being migrated, an
# asset still named MH_Lena) carries this marker, with the reason beside it.
ALLOW = "names-gate: allow"

# Where speech and on-screen text come from.
DATA = ["content/dialogue/*.json", "game-design/barks.json", "game-design/bark-names.json",
        "game-design/tier2-batch-1.json", "ledger/Assets/StreamingAssets/tier2-batch-1.json",
        "ledger/Assets/StreamingAssets/Audio/Voice/barks-manifest.json"]
CARDS = ["production/cast/cards/*.md"]
# The Core's own text (acts, the empire, the street's templates) and the
# game's source. The old Unity game layer (ledger/Assets/Scripts/Game) is not
# read: nobody plays it now, and it still holds about a hundred old names
# (FINDINGS).
SOURCE = ["ledger/Assets/Scripts/Core/*.cs", "ue-probe/Source/LedgerProbe/Private/*.cpp",
          "ue-probe/Source/LedgerProbe/Public/*.h"]
LITERAL = re.compile(r'"((?:[^"\\\n]|\\.)*)"')


def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)


def hits_in_text(where, text):
    return ["%s: %s -> %s in %r" % (where, m.group(1), dict(RETIRED)[CANON[m.group(1)]], text[max(0, m.start() - 40):m.end() + 30])
            for m in PATTERN.finditer(text)]


def scan(repo=REPO):
    found, read = [], 0
    for g in DATA:
        for f in sorted(glob.glob(os.path.join(repo, g))):
            rel = os.path.relpath(f, repo).replace("\\", "/")
            with open(f, encoding="utf-8") as fh:
                doc = json.load(fh)
            read += 1
            for s in strings(doc):
                found += hits_in_text(rel, s)
    for g in CARDS:
        for f in sorted(glob.glob(os.path.join(repo, g))):
            rel = os.path.relpath(f, repo).replace("\\", "/")
            read += 1
            with open(f, encoding="utf-8") as fh:
                for n, line in enumerate(fh, 1):
                    if not line.lower().startswith("id:"):
                        found += hits_in_text("%s:%d" % (rel, n), line)
    for g in SOURCE:
        for f in sorted(glob.glob(os.path.join(repo, g))):
            rel = os.path.relpath(f, repo).replace("\\", "/")
            read += 1
            with open(f, encoding="utf-8", errors="replace") as fh:
                for n, line in enumerate(fh, 1):
                    if ALLOW in line:
                        continue
                    code = line.split("//", 1)[0] if not line.lstrip().startswith("\"") else line
                    # Every literal, one word or a sentence: a one-word "Sam"
                    # was a gossip agent's name, and reached the talk model as
                    # "I heard from Sam" (the independent check, 25 September).
                    for lit in LITERAL.findall(code):
                        found += hits_in_text("%s:%d" % (rel, n), lit)
    return found, read


def canon_names(repo=REPO):
    with open(os.path.join(repo, "canon.md"), encoding="utf-8") as fh:
        text = fh.read()
    at = text.find("- NAMES, ruled by Jafar")
    return text[at:text.find("\n\n", at)] if at >= 0 else ""


def selftest():
    import tempfile
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("names-gate selftest FAIL " + name)
    block = canon_names()
    check("canon has the NAMES block", len(block) > 100)
    for old, new in RETIRED:
        check("canon retires %s" % old, re.search(r"\b" + re.escape(WITH.get(old, old)) + r"\b", block) is not None)
        check("canon names %s" % new, new.split()[0] in block)
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "content", "dialogue"))
        os.makedirs(os.path.join(d, "production", "cast", "cards"))
        with open(os.path.join(d, "canon.md"), "w", encoding="utf-8") as fh:
            fh.write("x")
        with open(os.path.join(d, "content", "dialogue", "b.json"), "w", encoding="utf-8") as fh:
            json.dump({"rungs": ["novak"], "lines": [{"id": "rocco-1", "rung": "novak", "text": "Evening, Nowak. Ron was in. Mrs Vane waved."},
                                                     {"id": "x", "text": "Mind the weather vane, Darren. Danny Cammack's lot."}]}, fh)
        with open(os.path.join(d, "production", "cast", "cards", "lena.md"), "w", encoding="utf-8") as fh:
            fh.write("# Sheila Dunn\nid: lena\n")
        found, read = scan(d)
        check("the accepting case: canon names, lower-case ids and ordinary words pass (%d hits)" % len(found), found == [] and read == 2)
        with open(os.path.join(d, "content", "dialogue", "b.json"), "w", encoding="utf-8") as fh:
            json.dump({"lines": [{"id": "a", "text": "Evening, Novak. Rocco was in, and Danny Ro's boys. NOVAK."}]}, fh)
        with open(os.path.join(d, "production", "cast", "cards", "lena.md"), "w", encoding="utf-8") as fh:
            fh.write("# Lena Moreau\nid: lena\n")
        found, _ = scan(d)
        names = sorted(h.split(": ", 1)[1].split(" ->")[0] for h in found)
        check("the refusing case: each retired name is caught once, Danny Ro whole (%s)" % names,
              names == ["Danny Ro", "Lena", "Moreau", "NOVAK", "Novak", "Rocco"])
    print("names-gate selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    found, read = scan()
    for h in found:
        print(h)
    print("names-gate: files=%d retired-names=%d" % (read, len(found)))
    sys.exit(1 if found or read == 0 else 0)
