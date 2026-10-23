"""A cloud shopfront made ready for the game: its window and door glass taken out and recorded, the
rest joined into one mesh that keeps every material and texture.

    F:/LedgerTools/bpyenv/Scripts/python.exe tools/art-recipes/front_for_game.py \
        production/assets/cloud-week/shop-windows/ritas_front.glb ritas-front
    F:/LedgerTools/bpyenv/Scripts/python.exe tools/art-recipes/front_for_game.py --display \
        production/assets/cloud-week/shop-windows/ritas_display.glb ritas-display
    (a lit box sign: --night-glow=<material>=<the sign's emissive map>, dark until the game lights it;
     lettering on glass as solid cut-outs: --mask=<material>[,...];
     a display's side linings up to the window head: --raise=<material>:<metres>;
     and a head board across their tops, or at a height in the display's frame: --head=<material>[@<metres>];
     a mirror-glossy glass fascia dulled: --dull=<material>:<roughness>[:<specular>])
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


# LETTERING ON GLASS AS A CUT-OUT (23 October, the tea rooms' night gate: their door's number 14, see-through as the
# design exported it, lit up as a ghost once the window's light panel hung just behind the fanlight; Unreal lights a
# see-through surface from its light volume, whatever lights may touch the front). --mask=<material>[,...] writes the
# named materials cut-out (MASK at 0.5): their letters solid, lit as the front is.
def mask_materials(glb, names):
    """Rewrite a glb in place with the named materials' alphaMode MASK at 0.5. Returns how many changed."""
    import struct
    data = open(glb, "rb").read()
    jlen = struct.unpack("<I", data[12:16])[0]
    j = json.loads(data[20:20 + jlen])
    rest = data[20 + jlen:]
    n = 0
    for m in j.get("materials", []):
        if m.get("name") in names and m.get("alphaMode") == "BLEND":
            m["alphaMode"] = "MASK"
            m["alphaCutoff"] = 0.5
            n += 1
    if n:
        body = json.dumps(j, separators=(",", ":")).encode("utf-8")
        body += b" " * ((4 - len(body) % 4) % 4)
        head = data[:8] + struct.pack("<I", 20 + len(body) + len(rest)) + struct.pack("<I", len(body)) + data[16:20]
        open(glb, "wb").write(head + body + rest)
    return n


# A GLASS FASCIA DULLED TO SATIN (23 October, the grocer's gate from across the road: its glass fascia, bottle green with
# cream letters, came in nearly a mirror (roughness about 0.13) and from below it caught the bright overcast sky and read
# pale grey; the design's render, nearly head on, keeps the green). --dull=<material>:<roughness> drops the material's
# metal and roughness map and sets it plain, not metal, at that roughness.
def dull_materials(glb, specs):
    """Rewrite a glb in place: each "<material>:<roughness>" loses its metallicRoughnessTexture and takes metallicFactor 0
    and that roughnessFactor. Returns how many changed."""
    import struct
    data = open(glb, "rb").read()
    jlen = struct.unpack("<I", data[12:16])[0]
    j = json.loads(data[20:20 + jlen])
    rest = data[20 + jlen:]
    want = {sp.split(":")[0]: [float(x) for x in sp.split(":")[1:]] for sp in specs}
    n = 0
    for m in j.get("materials", []):
        if m.get("name") in want:
            pbr = m.setdefault("pbrMetallicRoughness", {})
            pbr.pop("metallicRoughnessTexture", None)
            pbr["metallicFactor"] = 0.0
            pbr["roughnessFactor"] = want[m["name"]][0]
            # (try 2, the same morning: at satin 0.45 it still read pale grey-green from below; "<material>:<roughness>:<specular>"
            # also cuts its reflectance, KHR_materials_specular)
            if len(want[m["name"]]) > 1:
                m.setdefault("extensions", {})["KHR_materials_specular"] = {"specularFactor": want[m["name"]][1]}
                if "KHR_materials_specular" not in j.setdefault("extensionsUsed", []):
                    j["extensionsUsed"].append("KHR_materials_specular")
            n += 1
    if n:
        body = json.dumps(j, separators=(",", ":")).encode("utf-8")
        body += b" " * ((4 - len(body) % 4) % 4)
        head = data[:8] + struct.pack("<I", 20 + len(body) + len(rest)) + struct.pack("<I", len(body)) + data[16:20]
        open(glb, "wb").write(head + body + rest)
    return n


# A DISPLAY'S CLOTH IS SOLID (23 October, the tea rooms' gate, square on: dark saw-tooth triangles ran down the fold
# ridges of the café curtains, which the design gives half transmission; drawn see-through in the game, a folded sheet's
# triangles are not sorted by depth, and back folds drew over front ones). Each material named here loses its
# transmission and is written opaque.
SOLID_CLOTH = ("cafe_curtain",)


def solid_cloth(glb, names=SOLID_CLOTH):
    """Rewrite a glb in place with the named materials' transmission removed and alphaMode OPAQUE. Returns how many changed."""
    import struct
    data = open(glb, "rb").read()
    jlen = struct.unpack("<I", data[12:16])[0]
    j = json.loads(data[20:20 + jlen])
    rest = data[20 + jlen:]
    n = 0
    for m in j.get("materials", []):
        if m.get("name") in names and ("KHR_materials_transmission" in m.get("extensions", {}) or m.get("alphaMode") in ("BLEND", "MASK")):
            m.get("extensions", {}).pop("KHR_materials_transmission", None)
            m["alphaMode"] = "OPAQUE"
            m.pop("alphaCutoff", None)
            n += 1
    if n:
        body = json.dumps(j, separators=(",", ":")).encode("utf-8")
        body += b" " * ((4 - len(body) % 4) % 4)
        head = data[:8] + struct.pack("<I", 20 + len(body) + len(rest)) + struct.pack("<I", len(body)) + data[16:20]
        open(glb, "wb").write(head + body + rest)
    return n


# A LIT BOX SIGN GLOWS AT NIGHT (22 October, the newsagent's front: the design's sign is lit by tubes, the target's 4.1
# `lit: tubes`; its gate puts the 4.1 board's emissive map on the sign's face material at night, sw_gate.py, and its glb is
# the day state, PC-NA1): the map goes into the front's glb as that material's emissive texture with a factor of 0, so it is
# dark by day as exported; the game sets the factor after dark (VignetteShot.cpp ReDriveShopInteriors, the shop entry's
# front "night_glow"). Unreal's glTF import keeps an emissive texture whatever its factor (its bHasEmissiveTexture switch).
def add_night_glow(glb, material, png):
    """Rewrite a glb in place: the PNG appended to its binary chunk and set as `material`'s emissive texture, on the
    same texture coordinates as its base colour, with emissiveFactor [0, 0, 0]. Returns True when it changed."""
    import struct
    data = open(glb, "rb").read()
    jlen = struct.unpack("<I", data[12:16])[0]
    j = json.loads(data[20:20 + jlen])
    rest = data[20 + jlen:]
    blen = struct.unpack("<I", rest[0:4])[0]
    assert rest[4:8] == b"BIN\x00", "no binary chunk"
    binary = rest[8:8 + blen]
    mats = [m for m in j.get("materials", []) if m.get("name") == material]
    if not mats:
        return False
    pic = open(png, "rb").read()
    binary += b"\x00" * ((4 - len(binary) % 4) % 4)
    j.setdefault("bufferViews", []).append({"buffer": 0, "byteOffset": len(binary), "byteLength": len(pic)})
    binary += pic + b"\x00" * ((4 - len(pic) % 4) % 4)
    j["buffers"][0]["byteLength"] = len(binary)
    j.setdefault("images", []).append({"bufferView": len(j["bufferViews"]) - 1, "mimeType": "image/png",
                                       "name": os.path.splitext(os.path.basename(png))[0]})
    for m in mats:
        base = m.get("pbrMetallicRoughness", {}).get("baseColorTexture", {})
        tex = {"source": len(j["images"]) - 1}
        if "index" in base and "sampler" in j["textures"][base["index"]]:
            tex["sampler"] = j["textures"][base["index"]]["sampler"]
        j.setdefault("textures", []).append(tex)
        info = {"index": len(j["textures"]) - 1, "texCoord": base.get("texCoord", 0)}
        if "extensions" in base:
            info["extensions"] = base["extensions"]
        m["emissiveTexture"] = info
        m["emissiveFactor"] = [0.0, 0.0, 0.0]
    body = json.dumps(j, separators=(",", ":")).encode("utf-8")
    body += b" " * ((4 - len(body) % 4) % 4)
    total = 12 + 8 + len(body) + 8 + len(binary)
    out = data[:8] + struct.pack("<I", total) + struct.pack("<I", len(body)) + b"JSON" + body \
        + struct.pack("<I", len(binary)) + b"BIN\x00" + binary
    open(glb, "wb").write(out)
    return True


def raise_tops(obj, material, metres):
    """A DISPLAY'S SIDE LININGS TO THE WINDOW HEAD (23 October, the tea rooms' night gate from the left: their window
    stands at the bay's end, and through its last toplights, from a slant, the eye passed over the returns' tops (0.35 m
    under the head) beyond the room's card into nothing, black against the lit room). The top edge of every face of
    `material` moves up by `metres`. Returns how many vertices moved."""
    import bmesh
    slots = [i for i, sl in enumerate(obj.material_slots) if sl.material and sl.material.name == material]
    if not slots or metres <= 0.0:
        return 0
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    faces = [f for f in bm.faces if f.material_index in slots]
    top = max(v.co.z for f in faces for v in f.verts)
    verts = {v for f in faces for v in f.verts if v.co.z >= top - 0.001}
    for v in verts:
        v.co.z += metres
    bm.to_mesh(obj.data)
    bm.free()
    return len(verts)


def add_head(obj, material, thick=0.012, at=None):
    """A DISPLAY'S HEAD (23 October, the tea rooms' night gate from the right: through the middle toplights, from below at
    a slant, the eye passed over the room's card into nothing, black; Rita's display has its own head and shows the
    room there). A board of `material` over the whole span of that material's faces, at their top, from the glass back
    to the card, as a shopfitter closes a window's lining box. Returns the board's face count."""
    import bmesh
    slots = [i for i, sl in enumerate(obj.material_slots) if sl.material and sl.material.name == material]
    if not slots:
        return 0
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    vs = [v.co.copy() for f in bm.faces if f.material_index in slots for v in f.verts]
    x0, x1 = min(v.x for v in vs), max(v.x for v in vs)
    y0, y1 = min(v.y for v in vs), max(v.y for v in vs)
    z1 = max(v.z for v in vs) if at is None else at
    res = bmesh.ops.create_cube(bm, size=1.0)
    for v in res["verts"]:
        v.co.x = x0 if v.co.x < 0 else x1
        v.co.y = y0 if v.co.y < 0 else y1
        v.co.z = z1 - thick if v.co.z < 0 else z1
    new = {f for v in res["verts"] for f in v.link_faces}
    for f in new:
        f.material_index = slots[0]
    bm.to_mesh(obj.data)
    bm.free()
    return len(new)


def smooth_by_angle(obj, materials, degrees=30.0):
    """ROUND GOODS SHADED ROUND (23 October, the grocer's night gate from the right: its tins came from the design
    flat-shaded, 16-sided, and under the window's strong night light each side face read as its own hard light or dark
    stripe, a jump of 100 levels in one pixel along a label). Each corner of a face of `materials` takes the mean normal
    of the faces of `materials` meeting at its point within `degrees` of its own face (a modeller's smooth-by-angle:
    the sides round, a rim or a lid's edge kept sharp). Flat-shaded faces share no vertices, so this goes by position,
    not by the mesh's edges; every other face keeps the normals it has, and the custom normals travel in the glTF.
    Returns how many faces were smoothed."""
    import math
    from collections import defaultdict
    from mathutils import Vector
    me = obj.data
    slots = {i for i, sl in enumerate(obj.material_slots) if sl.material and sl.material.name in materials}
    if not slots:
        return 0
    corner = [Vector(c.vector) for c in me.corner_normals]
    faces = [p for p in me.polygons if p.material_index in slots]

    def key(li):
        v = me.vertices[me.loops[li].vertex_index].co
        return (round(v.x, 5), round(v.y, 5), round(v.z, 5))
    at = defaultdict(list)
    for p in faces:
        for li in p.loop_indices:
            at[key(li)].append(p.normal.copy())
    lim = math.cos(math.radians(degrees))
    for p in faces:
        n = p.normal
        for li in p.loop_indices:
            acc = Vector((0.0, 0.0, 0.0))
            for m in at[key(li)]:
                if n.dot(m) >= lim:
                    acc += m
            corner[li] = acc.normalized() if acc.length > 0 else n.copy()
        p.use_smooth = True
    me.normals_split_custom_set([tuple(c) for c in corner])
    return len(faces)


def main(src, name, display=False, glow=None, mask=None, raise_=None, head=None, dull=None, smooth=None):
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
    raised = 0
    for spec in raise_ or []:
        material, metres = spec.split(":")
        raised += raise_tops(joined, material, float(metres))
    # (try 2, the same night: at the linings' top the board left a gap above the room's card, which stops lower, and the
    # eye still passed through it; "<material>@<height>" puts the board at the card's top, in the display's own frame)
    headed = add_head(joined, head.split("@")[0], at=float(head.split("@")[1]) if "@" in head else None) if head else 0
    smoothed = smooth_by_angle(joined, smooth) if smooth else 0
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
        solid = solid_cloth(glb)
        tris = sum(len(p.vertices) - 2 for p in joined.data.polygons)
        print("front_for_game: %s -> %s display parts=%d slots=%d sheenTinted=%d solidCloth=%d raisedVerts=%d headFaces=%d smoothFaces=%d triangles=%d bytes=%d"
              % (os.path.basename(src), glb, len(keep), len(joined.material_slots), tinted, solid, raised, headed, smoothed, tris, os.path.getsize(glb)))
        return 0
    cut_out_cards(glb)
    if dull and dull_materials(glb, dull) != len(dull):
        print("front_for_game: not every material of --dull is in this front: %s" % ",".join(dull))
        return 1
    if mask and mask_materials(glb, mask) != len(mask):
        print("front_for_game: not every material of --mask is see-through here: %s" % ",".join(mask))
        return 1
    if glow:
        material, png = glow.split("=", 1)
        if not add_night_glow(glb, material, png):
            print("front_for_game: no material %s for the night glow" % material)
            return 1
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
    glow = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--night-glow=")]
    mask = [m for a in sys.argv[1:] if a.startswith("--mask=") for m in a.split("=", 1)[1].split(",") if m]
    raise_ = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--raise=")]
    head = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--head=")]
    dull = [d for a in sys.argv[1:] if a.startswith("--dull=") for d in a.split("=", 1)[1].split(",") if d]
    smooth = [s for a in sys.argv[1:] if a.startswith("--smooth=") for s in a.split("=", 1)[1].split(",") if s]
    args = [a for a in sys.argv[1:] if a != "--display" and not a.startswith(("--night-glow=", "--mask=", "--raise=", "--head=", "--dull=", "--smooth="))]
    if len(args) != 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(main(args[0], args[1], display="--display" in sys.argv, glow=glow[0] if glow else None, mask=mask or None,
                  raise_=raise_ or None, head=head[0] if head else None, dull=dull or None, smooth=smooth or None))
