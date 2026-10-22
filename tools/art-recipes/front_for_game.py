"""A cloud shopfront made ready for the game: its window and door glass taken out and recorded, the
rest joined into one mesh that keeps every material and texture.

    F:/LedgerTools/bpyenv/Scripts/python.exe tools/art-recipes/front_for_game.py \
        production/assets/cloud-week/shop-windows/ritas_front.glb ritas-front
    F:/LedgerTools/bpyenv/Scripts/python.exe tools/art-recipes/front_for_game.py --display \
        production/assets/cloud-week/shop-windows/ritas_display.glb ritas-display
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

AND THE CLOUD'S DISPLAY (--display, the same day): the goods on the window bed, about 330 parts,
joined whole (no glass taken out) into F:/LedgerTools/game-inputs/production/assets/shop-displays/
<name>.glb. Unjoined, the import made one static mesh per part and the game stood only the first
(an alarm clock) behind the glass.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_GLB = os.environ.get("LEDGER_FRONT_OUT", "F:/LedgerTools/game-inputs/production/assets/shop-fronts")
OUT_JSON = os.path.join(REPO, "production", "specs", "shop-fronts")
OUT_DISPLAY = os.environ.get("LEDGER_DISPLAY_OUT", "F:/LedgerTools/game-inputs/production/assets/shop-displays")
PANE = re.compile(r"^glass(\.\d+)?$")


def is_pane(material_names):
    return bool(material_names) and all(PANE.match(m or "") for m in material_names)


def tint_sheen_to_base(mat):
    """THE VELVET'S SHEEN IN ITS OWN COLOUR (21 October): the cloud's velvet carries a white sheen at
    full weight, which Cycles lays over the cloth as a soft rim but Unreal's glTF import spreads
    over the whole surface, so Rita's dark red tiers came out pale pink. The sheen takes the
    material's own mean base colour (linear) instead. True when it changed."""
    b = mat.node_tree.nodes.get("Principled BSDF") if mat and mat.node_tree else None
    if b is None or b.inputs["Sheen Weight"].default_value <= 0.0:
        return False
    rgb = list(b.inputs["Base Color"].default_value[:3])
    for link in b.inputs["Base Color"].links:
        img = getattr(link.from_node, "image", None)
        if img is not None and img.size[0] > 0:
            import numpy as np
            px = np.array(img.pixels[:], dtype=np.float32).reshape(-1, img.channels)[:, :3].mean(axis=0)
            if img.colorspace_settings.name.lower().startswith("srgb"):
                px = np.where(px <= 0.04045, px / 12.92, ((px + 0.055) / 1.055) ** 2.4)
            rgb = [float(v) for v in px]
    b.inputs["Sheen Tint"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    return True


# A FRONT'S CARDS ARE SOLID (22 October, the ironmonger's night gate: his door's card, see-through as the design exported
# it, showed the dark shop's room glowing through it as a pale tag, whichever face it turned): each material named here is
# written OPAQUE. Try 1 wrote it cut-out (glTF MASK at 0.5); from the hook camera, a few pixels wide, Rita's cut-out card
# washed out to grey by day. Its picture is transparent only in 293 of 88,000 pixels (the corners and the hole), which carry
# the card's own colour, so opaque costs nothing seen. From the hook camera (a few pixels, a low slant) the solid card reads
# grey: try 2 made it satin (roughness 0.7) and nothing changed, so it is the door glass's own reflection over it, now that
# the card is drawn behind the glass as a solid (the see-through card had been drawn over it); set aside, listed.
CUTOUT_MATERIALS = ("door_sign",)


def cut_out_cards(glb, names=CUTOUT_MATERIALS):
    """Rewrite a glb in place with the named materials' alphaMode OPAQUE. Returns how many changed."""
    import struct
    data = open(glb, "rb").read()
    jlen = struct.unpack("<I", data[12:16])[0]
    j = json.loads(data[20:20 + jlen])
    rest = data[20 + jlen:]
    n = 0
    for m in j.get("materials", []):
        if m.get("name") in names and m.get("alphaMode") in ("BLEND", "MASK"):
            m["alphaMode"] = "OPAQUE"
            m.pop("alphaCutoff", None)
            n += 1
    if n:
        body = json.dumps(j, separators=(",", ":")).encode("utf-8")
        body += b" " * ((4 - len(body) % 4) % 4)
        head = data[:8] + struct.pack("<I", 20 + len(body) + len(rest)) + struct.pack("<I", len(body)) + data[16:20]
        open(glb, "wb").write(head + body + rest)
    return n


def main(src, name, display=False):
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=os.path.abspath(src))
    bpy.context.view_layer.update()
    panes, keep = [], []
    for o in [o for o in bpy.context.scene.objects if o.type == "MESH"]:
        mats = [s.material.name for s in o.material_slots if s.material]
        if not display and is_pane(mats):
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
        if o.data.users > 1:   # a repeated good (the display's pocket watches) shares its mesh
            o.data = o.data.copy()
        o.select_set(True)
    bpy.context.view_layer.objects.active = keep[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.join()
    joined = bpy.context.view_layer.objects.active
    joined.name = name
    for o in [o for o in bpy.context.scene.objects if o is not joined]:
        bpy.data.objects.remove(o, do_unlink=True)
    tinted = sum(1 for m in bpy.data.materials if tint_sheen_to_base(m))
    out_dir = OUT_DISPLAY if display else OUT_GLB
    os.makedirs(out_dir, exist_ok=True)
    glb = os.path.join(out_dir, name + ".glb")
    bpy.ops.object.select_all(action="DESELECT")
    joined.select_set(True)
    # AUTO (21 October): each picture passes through as it came, never re-encoded (the cloud's display's normal
    # maps, already JPEG, showed 8 x 8 blocks on glossy metal; byte-identical through this step, checked).
    bpy.ops.export_scene.gltf(filepath=glb, export_format="GLB", use_selection=True, export_apply=True,
                              export_materials="EXPORT", export_image_format="AUTO", export_yup=True)
    if display:
        tris = sum(len(p.vertices) - 2 for p in joined.data.polygons)
        print("front_for_game: %s -> %s display parts=%d slots=%d sheenTinted=%d triangles=%d bytes=%d"
              % (os.path.basename(src), glb, len(keep), len(joined.material_slots), tinted, tris, os.path.getsize(glb)))
        return 0
    cut_out_cards(glb)
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
    args = [a for a in sys.argv[1:] if a != "--display"]
    if len(args) != 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(main(args[0], args[1], display="--display" in sys.argv))
