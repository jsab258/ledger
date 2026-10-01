"""The interface's fonts, cut to the fixed weights the style guide names (production/design/ui/STYLE-GUIDE.md).

    python tools/ui/make_font_cuts.py SRC_DIR      # SRC_DIR holds the google/fonts files named below
    python tools/ui/make_font_cuts.py --selftest

WHY, 1 October (the interface, Jafar's yes to the evening paper). Unreal's
Slate draws a font from one file at one weight, and two of the families the
design uses come only as variable fonts (Libre Franklin by weight, League
Gothic by width), which were never checked in Unreal (FONTS.md). So each
weight the style guide asks for is cut into its own static file with
fontTools' instancer, which the OFL allows without renaming since neither
family has a Reserved Font Name; UnifrakturMaguntia and Old Standard TT are
static already and copied as they are (both reserved names are kept by not
changing them). Every file gets its family's OFL.txt beside it.

Sources, all SIL OFL 1.1, from github.com/google/fonts/tree/main/ofl (read
1 October 2026): librefranklin/LibreFranklin[wght].ttf, its Italic,
leaguegothic/LeagueGothic[wdth].ttf, unifrakturmaguntia/
UnifrakturMaguntia-Book.ttf, oldstandardtt/OldStandard-Regular.ttf and
-Italic.ttf. Out: production/fonts/evening-paper/.
"""
import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "production", "fonts", "evening-paper")
#: (out name, source file, axis settings or None for a copy)
CUTS = [("LibreFranklin-%d.ttf" % w, "LibreFranklin-VF.ttf", {"wght": w}) for w in (400, 450, 500, 600, 700, 800)] + [
    ("LibreFranklin-Italic-400.ttf", "LibreFranklin-Italic-VF.ttf", {"wght": 400}),
    ("LeagueGothic-Regular.ttf", "LeagueGothic-VF.ttf", {"wdth": 100}),
    ("UnifrakturMaguntia-Book.ttf", "UnifrakturMaguntia-Book.ttf", None),
    ("OldStandard-Regular.ttf", "OldStandard-Regular.ttf", None),
    ("OldStandard-Italic.ttf", "OldStandard-Italic.ttf", None),
]
LICENCE_OF = {"LibreFranklin": "libre-franklin", "LeagueGothic": "league-gothic",
              "UnifrakturMaguntia": "unifraktur-maguntia", "OldStandard": "old-standard-tt"}


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("make_font_cuts selftest FAIL " + name)
    check("every weight the style guide names is cut", all(any(c[0] == "LibreFranklin-%d.ttf" % w for c in CUTS) for w in (400, 450, 500, 600, 700, 800)))
    check("every family has its licence folder", all(os.path.isfile(os.path.join(REPO, "production", "design", "ui", "fonts", d, "OFL.txt"))
                                                     for d in LICENCE_OF.values()))
    made = [c[0] for c in CUTS if os.path.isfile(os.path.join(OUT, c[0]))]
    check("the cuts in the repository are the ones listed (or none yet)", not made or len(made) == len(CUTS))
    print("make_font_cuts selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


def main(src):
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    os.makedirs(OUT, exist_ok=True)
    for name, source, axes in CUTS:
        path = os.path.join(src, source)
        dst = os.path.join(OUT, name)
        if axes is None:
            shutil.copyfile(path, dst)
        else:
            f = TTFont(path)
            inst = instancer.instantiateVariableFont(f, axes, updateFontNames=False)
            inst.save(dst)
        f = TTFont(dst)
        cmap = f.getBestCmap()
        print("%s: %d glyphs, pound sign %s, %d bytes" % (name, len(f.getGlyphOrder()), "yes" if 0xA3 in cmap else "NO",
                                                         os.path.getsize(dst)))
    for fam, folder in LICENCE_OF.items():
        shutil.copyfile(os.path.join(REPO, "production", "design", "ui", "fonts", folder, "OFL.txt"),
                        os.path.join(OUT, "OFL-%s.txt" % fam))


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main(sys.argv[1])
