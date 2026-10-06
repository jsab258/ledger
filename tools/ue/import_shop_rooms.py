"""The shops' rooms as real geometry into Unreal: each production/assets/shop-rooms-3d/<shop>/<part>.glb
as one static mesh, in the editor run the cook step already starts.

    python tools/ue/import_shop_rooms.py --selftest     # runs without Unreal

WHY IT EXISTS, 3 October (item V1). Three fresh reviews failed seven shop windows whose rooms
were pictures projected with depth behind the glass: at a metre or two, anything standing off
the room's walls smeared. The close-range research (production/research/shop-window-interiors/
CLOSE-RANGE-2026-10-03.md) says games played on foot build real rooms behind the glass, and
that a whole room in one mesh is not expected to work with Lumen: so tools/art-recipes/shop-room.py
--export-room writes each room's floor, ceiling and three walls apart, and its fittings in one.

WHAT IT MAKES, under /Game/Ledger/ShopRooms/<shop>/<part>/: SM_<shop>_<part>, its materials
beside it, Nanite off, by the same step as the displays (import_vehicles.import_glb). The game
stands them behind the shop's glass where production/specs/shop-interiors.json says
("room_3d"), in place of the projected picture (LedgerInteriors in VignetteShot.cpp).

ONE LINE, appended to ue-material.txt: asked, made, and why not.
"""
import glob
import os
import sys
import time

ROOMS_REL = "production/assets/shop-rooms-3d"
PACKAGE_ROOT = "/Game/Ledger/ShopRooms"
PARTS = ("floor", "ceiling", "wall_left", "wall_right", "wall_back", "fittings")


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# THE ROOMS GIT DOES NOT HOLD, 6 October: a room's fittings run to 14 MB and git takes nothing over
# 1 MB since 5 October, so the rooms also live on F: under the same paths (tools/ue/stage_game_data.py's
# GAME_INPUTS), where the build machine on this PC reads them. A part in the checkout is preferred.
GAME_INPUTS = os.environ.get("LEDGER_GAME_INPUTS", r"F:\LedgerTools\game-inputs")


def rooms(root, inputs=None):
    """(shop, part, path) for every room part on disk, the checkout's first, then the game inputs'."""
    inputs = GAME_INPUTS if inputs is None else inputs
    found = {}
    for base in (inputs, root):
        for d in sorted(glob.glob(os.path.join(base, ROOMS_REL, "*"))):
            if not os.path.isdir(d):
                continue
            for part in PARTS:
                p = os.path.join(d, part + ".glb")
                if os.path.isfile(p):
                    found[(os.path.basename(d), part)] = p
    return [(shop, part, found[(shop, part)]) for shop, part in sorted(found, key=lambda k: (k[0], PARTS.index(k[1])))]


def mesh_path(shop, part):
    return "%s/%s/%s/SM_%s_%s" % (PACKAGE_ROOT, shop, part, shop, part)


def rooms_line(asked, made, nanite_off, seconds, notes):
    return ("shopRoomsImportStatus=%s shopRoomsImported=%d/%d shopRoomsNaniteOff=%d/%d "
            "shopRoomsImportSeconds=%.1f shopRoomsImportNote=%s"
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
            print("import_shop_rooms selftest FAIL %s: %s" % (name, detail))
    import json
    root = repo_root()
    found = rooms(root)
    spec = json.load(open(os.path.join(root, "production", "specs", "shop-interiors.json"), encoding="utf-8"))
    wanted = [s["id"] for s in spec["shops"] if s.get("room_3d")]
    have = {(s, p) for s, p, _ in found}
    ok("every shop the spec gives a real room has all six parts on disk",
       all((w, p) in have for w in wanted for p in PARTS), "%s vs %s" % (wanted, sorted(have)))
    ok("the mesh is named where the game loads it",
       mesh_path("launderette", "floor") == "/Game/Ledger/ShopRooms/launderette/floor/SM_launderette_floor")
    ok("the line carries its denominator", "shopRoomsImported=5/6" in rooms_line(6, 5, 5, 1.0, ["x"]))
    src = open(os.path.join(root, "ue-probe", "Source", "LedgerProbe", "Private", "VignetteShot.cpp"), encoding="utf-8").read()
    ok("the game loads from this package root", ('TEXT("%s/' % PACKAGE_ROOT) in src)
    print("import_shop_rooms selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


def main():
    import unreal
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import import_vehicles
    t0 = time.time()
    root = repo_root()
    out = os.path.join(unreal.Paths.project_dir(), "ue-material.txt")
    notes = []
    found = rooms(root)
    made = nanite_off = 0
    for shop, part, path in found:
        try:
            m, off, note = import_vehicles.import_glb(unreal, path, "%s/%s/%s" % (PACKAGE_ROOT, shop, part), mesh_path(shop, part))
            made += m
            nanite_off += off
            if note:
                notes.append(note)
        except Exception as e:
            notes.append("%s-%s-raised-%s" % (shop, part, str(e).splitlines()[0][:60] if str(e) else "?"))
    line = rooms_line(len(found), made, nanite_off, time.time() - t0, notes)
    with open(out, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print("import_shop_rooms: " + line)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
