"""A cloud shopfront made ready for the game: its window and door glass taken out and recorded, the
rest joined into one mesh that keeps every material and texture.

    F:/LedgerTools/bpyenv/Scripts/python.exe tools/art-recipes/front_for_game.py \
        production/assets/cloud-week/shop-windows/ritas_front.glb ritas-front
    python tools/art-recipes/front_for_game.py --selftest

WHY, 21 October 2026 (his order, item 5, and his ruling of the day: Rita's front as the family's
sample). The cloud's front (production/cloud-week/kit/shop-windows, build_shop.py front) is one glb
of about 220 parts. The game takes a front in two halves:
  * THE GLASS stays the street's own: the street recipe (tools/art-recipes/terrace-front.py,
    CLOUD_FRONTS) builds a pane where each of the front's panes was, so the game's glass, its
    reflections and the smashed-window crime work on it as on every other bay. The panes' boxes are
    written to production/specs/shop-fronts/<name>-glass.json in the front's own frame.
  * EVERYTHING ELSE (joinery, fascia with its lettering, the gilt words on the glass, the doors, the
    hall) is joined into one mesh, so the import makes one static mesh with its materials beside it
    (tools/ue/import_shop_displays.py), written to F:/LedgerTools/game-inputs/production/assets/
    shop-fronts/<name>.glb (over git's 1 MB).
The front's frame (production/cloud-week/kit/shop-windows/sw_ctx.py): metres; x across the bay from
the viewer's left to right about the bay's middle; y = -(distance out from the wall face toward the
street); z above the footway. Only material names "glass" and "glass.NNN" are panes; the gilt words
on the glass ("glass_row_*") stay with the front.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_GLB = os.environ.get("LEDGER_FRONT_OUT", "F:/LedgerTools/game-inputs/production/assets/shop-fronts")
OUT_JSON = os.path.join(REPO, "production", "specs", "shop-fronts")
PANE = re.compile(r"^glass(\.\d+)?$")


def is_pane(material_names):
    return bool(material_names) and all(PANE.match(m or "") for m in material_names)


def main(src, name):
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=os.path.abspath(src))
    bpy.context.view_layer.update()
    panes, keep = [], []
    for o in [o for o in bpy.context.scene.objects if o.type == "MESH"]:
        mats = [s.material.name for s in o.material_slots if s.material]
        if is_pane(mats):
            ws = [o.matrix_world @ v.co for v in o.data.vertices]
            panes.append({"name": o.name,
                          "min": [round(min(p[i] for p in ws), 4) for i in range(3)],
                          "max": [round(max(p[i] for p in ws), 4) for i in range(3)]})
            bpy.data.objects.remove(o, do_unlink=True)
        else:
            keep.append(o)
    for o in bpy.context.scene.objects:
        o.select_set(False)
    for o in keep:
        mw = o.matrix_world.copy()
        o.parent = None
        o.matrix_world = mw
        o.select_set(True)
    bpy.context.view_layer.objects.active = keep[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.join()
    joined = bpy.context.view_layer.objects.active
    joined.name = name
    for o in [o for o in bpy.context.scene.objects if o is not joined]:
        bpy.data.objects.remove(o, do_unlink=True)
    os.makedirs(OUT_GLB, exist_ok=True)
    glb = os.path.join(OUT_GLB, name + ".glb")
    bpy.ops.object.select_all(action="DESELECT")
    joined.select_set(True)
    bpy.ops.export_scene.gltf(filepath=glb, export_format="GLB", use_selection=True, export_apply=True,
                              export_materials="EXPORT", export_yup=True)
    os.makedirs(OUT_JSON, exist_ok=True)
    js = os.path.join(OUT_JSON, name + "-glass.json")
    with open(js, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"what": "the glass panes taken out of %s (tools/art-recipes/front_for_game.py): each pane's box in "
                           "the front's own frame (metres; x across from the viewer's left to right about the bay's "
                           "middle; y = -(out from the wall face); z above the footway); the street recipe builds "
                           "the street's own glass there (terrace-front.py CLOUD_FRONTS)" % os.path.basename(src),
                   "source": os.path.relpath(os.path.abspath(src), REPO).replace(os.sep, "/"),
                   "panes": sorted(panes, key=lambda p: p["name"])}, f, indent=1)
    tris = sum(len(p.vertices) - 2 for p in joined.data.polygons)
    print("front_for_game: %s -> %s panes=%d kept=%d slots=%d triangles=%d bytes=%d"
          % (os.path.basename(src), glb, len(panes), len(keep), len(joined.material_slots), tris, os.path.getsize(glb)))
    return 0


def selftest():
    ok = bad = 0

    def check(n, c):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if c else (ok, bad + 1)
        if not c:
            print("front_for_game selftest FAIL " + n)
    check("plain glass is a pane", is_pane(["glass"]) and is_pane(["glass.001"]))
    check("the gilt words on the glass stay with the front", not is_pane(["glass_row_7"]))
    check("a part with glass and a frame stays with the front", not is_pane(["glass", "paint_white_joinery"]))
    check("a part with no material is not a pane", not is_pane([]))
    print("front_for_game selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    sys.exit(main(sys.argv[1], sys.argv[2]))
