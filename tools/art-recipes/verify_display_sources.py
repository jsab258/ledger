"""Every model in a shop's window display, traced to its source and licence (phase 1, item 1.1, 6 October).

    python tools/art-recipes/verify_display_sources.py --shop pawnbroker [--write]
    python tools/art-recipes/verify_display_sources.py --selftest

WHY. PLAN.md's first proof asks for "one frontage ... its window of verified CC0 goods". The goods
in a display are Poly Haven models that tools/art-recipes/fetch_polyhaven.py stored on F: with a
source.json beside each (its name, its page, its licence). This reads the display's own branch of
tools/art-recipes/shop-room.py, finds every Poly Haven asset it names, and checks each source.json:
present, licence CC0, from polyhaven.com. Any asset without that record fails. --write puts the
table in production/art/shop-rooms/<shop>-goods-sources.md, the record a reviewer reads.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RECIPE = os.path.join(REPO, "tools", "art-recipes", "shop-room.py")
POLY = os.environ.get("LEDGER_POLYHAVEN", r"F:\LedgerTools\polyhaven")
# The pawnbroker is the display builder's last branch ("else"); the others call a named function.
BRANCH = {"pawnbroker": ("    else:\n        # THE BED: a board covered in red velvet", "\n    # ")}


def branch_text(shop, recipe_text):
    if shop in BRANCH:
        start, _ = BRANCH[shop]
        i = recipe_text.index(start)
        j = recipe_text.find("\ndef ", i)
        return recipe_text[i:j if j > 0 else len(recipe_text)]
    m = re.search(r"\ndef %s_display\(.*?(?=\ndef )" % re.escape(shop), recipe_text, re.S)
    return m.group(0) if m else ""


def candidates(text):
    return sorted(set(re.findall(r'"([A-Za-z][A-Za-z0-9_]*)"', text)))


def source_of(asset, poly=POLY):
    for res in ("1k", "2k", "4k"):
        p = os.path.join(poly, asset, res, "source.json")
        if os.path.isfile(p):
            with open(p, encoding="utf-8") as f:
                return p, json.load(f)
    return None, None


def verify(shop, poly=POLY, recipe_text=None):
    recipe_text = recipe_text if recipe_text is not None else open(RECIPE, encoding="utf-8").read()
    rows, bad = [], []
    for name in candidates(branch_text(shop, recipe_text)):
        if not os.path.isdir(os.path.join(poly, name)):
            continue        # a material, a name or a word, not a Poly Haven asset
        path, src = source_of(name, poly)
        if src is None:
            bad.append("%s: no source.json" % name)
            rows.append((name, "?", "?", "MISSING"))
            continue
        lic = str(src.get("license") or src.get("licence") or "")
        url = str(src.get("page") or src.get("url") or src.get("source") or "")
        ok = "CC0" in lic.upper() and "polyhaven.com" in url
        if not ok:
            bad.append("%s: licence %r, page %r" % (name, lic, url))
        rows.append((name, lic, url, "ok" if ok else "FAIL"))
    return rows, bad


def selftest():
    import tempfile
    ok = True

    def t(c, what):
        nonlocal ok
        print(("  ok   " if c else "  FAIL ") + what)
        ok = ok and c
    d = tempfile.mkdtemp()
    for name, lic in (("Camera_01", "CC0"), ("jug_01", "CC-BY")):
        os.makedirs(os.path.join(d, name, "1k"))
        json.dump({"license": lic, "page": "https://polyhaven.com/a/" + name}, open(os.path.join(d, name, "1k", "source.json"), "w"))
    os.makedirs(os.path.join(d, "brass_vase_01"))
    text = ('\ndef fishmonger_display(a):\n    model("Camera_01", 0)\n    model("jug_01", 0)\n    model("brass_vase_01", 0)\n    m("velvet_red")\n'
            '\ndef other():\n    pass\n')
    rows, bad = verify("fishmonger", d, text)
    t(any(r[0] == "Camera_01" and r[3] == "ok" for r in rows), "a CC0 asset with its Poly Haven page passes")
    t(any("jug_01" in b for b in bad), "an asset whose record says another licence fails")
    t(any("brass_vase_01" in b for b in bad), "an asset with no source record fails")
    t(not any(r[0] == "velvet_red" for r in rows), "a material's name is not taken for an asset")
    print("verify_display_sources selftest: " + ("passed" if ok else "FAILED"))
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    shop = argv[argv.index("--shop") + 1]
    if not os.path.isdir(POLY):
        # the cloud has no F:: the record written here on this PC stands until the next run here
        print("display-sources shop=%s outcome=SKIPPED (no %s on this machine)" % (shop, POLY))
        return 0
    rows, bad = verify(shop)
    lines = ["# %s's window goods: sources and licences" % shop, "",
             "Written by tools/art-recipes/verify_display_sources.py from the display's branch of tools/art-recipes/shop-room.py "
             "and each asset's source.json on F:/LedgerTools/polyhaven (stored by fetch_polyhaven.py).", "",
             "| Asset | Licence | Page | Verdict |", "|---|---|---|---|"]
    lines += ["| %s | %s | %s | %s |" % r for r in rows]
    lines += ["", "%d assets, %d failing." % (len(rows), len(bad))]
    print("\n".join(lines))
    if "--write" in argv:
        out = os.path.join(REPO, "production", "art", "shop-rooms", "%s-goods-sources.md" % shop)
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines) + "\n")
    print("display-sources shop=%s assets=%d failing=%d outcome=%s" % (shop, len(rows), len(bad), "FAIL" if bad or not rows else "PASS"))
    return 1 if bad or not rows else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
