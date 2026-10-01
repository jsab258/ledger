"""The shop windows' displays into Unreal: each production/assets/shop-displays/*.glb
as one static mesh, in the editor run the cook step already starts.

    python tools/ue/import_shop_displays.py --selftest     # runs without Unreal

WHY IT EXISTS, 1 October (item V1). Jafar: "The shop windows have interiors
and reflections". The room behind the glass is a picture projected with depth
(tools/ue/make_interior_material.py), and that trick fails close up and at a
grazing angle, which is exactly where a pavement walker looks
(production/research/shop-window-interiors/NOTE.md, sections 1 and 7). So
the near metre behind the glass, the display on its bed, is real geometry:
built by tools/art-recipes/shop-room.py --display, from Poly Haven models
(CC0), one glb per shop.

WHAT IT MAKES, under /Game/Ledger/ShopDisplays/<stem>/: SM_<stem>, with its
materials beside it, Nanite off, by the same step as the parked cars
(import_vehicles.import_glb). The game stands it behind its shop's glass where
production/specs/shop-interiors.json says (LedgerInteriors in VignetteShot.cpp).

ONE LINE, appended to ue-material.txt: asked, made, and why not.
"""
import glob
import os
import sys
import time

DISPLAYS_REL = "production/assets/shop-displays"
PACKAGE_ROOT = "/Game/Ledger/ShopDisplays"


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def stems(root):
    return sorted(os.path.splitext(os.path.basename(p))[0]
                  for p in glob.glob(os.path.join(root, DISPLAYS_REL, "*.glb")))


def mesh_path(stem):
    return "%s/%s/SM_%s" % (PACKAGE_ROOT, stem, stem)


def displays_line(asked, made, nanite_off, seconds, notes):
    return ("shopDisplaysImportStatus=%s shopDisplaysImported=%d/%d shopDisplaysNaniteOff=%d/%d "
            "shopDisplaysImportSeconds=%.1f shopDisplaysImportNote=%s"
            % ("OK" if asked and made == asked else ("NOTHING" if not asked else "PARTIAL"),
               made, asked, nanite_off, made, seconds,
               ("/".join(notes) or "none").replace(" ", "~")[:200]))


def selftest():
    passed = failed = 0

    def ok(name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("import_shop_displays selftest FAIL %s: %s" % (name, detail))
    import json
    root = repo_root()
    found = stems(root)
    spec = json.load(open(os.path.join(root, "production", "specs", "shop-interiors.json"), encoding="utf-8"))
    wanted = sorted(s["display"]["glb"] for s in spec["shops"] if s.get("display"))
    ok("every display the spec names has its glb", all(w in found for w in wanted), "%s vs %s" % (wanted, found))
    ok("the mesh is named where the game loads it",
       mesh_path("pawnbroker-display") == "/Game/Ledger/ShopDisplays/pawnbroker-display/SM_pawnbroker-display")
    ok("the line carries its denominator", "shopDisplaysImported=1/2" in displays_line(2, 1, 1, 1.0, ["x"]))
    # The game builds the same path (VignetteShot.cpp): read it out of the source.
    src = open(os.path.join(root, "ue-probe", "Source", "LedgerProbe", "Private", "VignetteShot.cpp"), encoding="utf-8").read()
    ok("the game loads from this package root", ('TEXT("%s/' % PACKAGE_ROOT) in src)
    print("import_shop_displays selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


def main():
    import unreal
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import import_vehicles
    t0 = time.time()
    root = repo_root()
    out = os.path.join(unreal.Paths.project_dir(), "ue-material.txt")
    notes = []
    found = stems(root)
    made = nanite_off = 0
    for stem in found:
        try:
            m, off, note = import_vehicles.import_glb(unreal, os.path.join(root, DISPLAYS_REL, stem + ".glb"),
                                                      "%s/%s" % (PACKAGE_ROOT, stem), mesh_path(stem))
            made += m
            nanite_off += off
            if note:
                notes.append(note)
        except Exception as e:
            notes.append("%s-raised-%s" % (stem, str(e).splitlines()[0][:60] if str(e) else "?"))
    line = displays_line(len(found), made, nanite_off, time.time() - t0, notes)
    with open(out, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print("import_shop_displays: " + line)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
