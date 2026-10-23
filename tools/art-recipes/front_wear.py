"""A cloud shopfront worn at the foot, baked into its own paints: a second copy of the front for the game.

    F:/LedgerTools/bpyenv/Scripts/python.exe tools/art-recipes/front_wear.py \
        production/specs/shop-fronts/ritas-front-wear.json
    (LEDGER_WEAR_PX=1024 for a quick trial; the spec's atlas_px otherwise)

WHY, 22 October 2026 (his page of 21 October on Rita's front: "not yet 2026-grade until the wear and the
night light are done"). Try 1 drew her painted slots in the street's own material for its foot wear; the
gate failed it, the street's material drawing her oxblood darker with no setting to blame
(production/research/street-wear/FRONT-WEAR-BAKE-2026-10-22.md). So the wear goes into the front's
own paints as the industry wears a unique piece: masks from what the model itself gives (height,
ambient occlusion, faces turned up, convex edges, distance from a hand's place), a colour and a
roughness baked from them into textures, and the front's own glTF material kept, which drew the
approved paint.

THE METHOD, in the front's own frame (metres, z above the footway):
  * the paint faces alone get a new unwrap into one atlas, the faces low on the front (below
    detail_below_m, or near the lever) at detail_ratio times the texel density of the rest;
  * one Cycles emission bake computes, per texel, the paint's colour drawn toward a warm dirt at a
    fraction of the paint's own luminance (so dirt only darkens a pale paint, never lightens it) by
    a mask = the foot band (ragged by a 3D noise) or splash above it, plus occlusion near the foot and
    faintly everywhere, plus dust on faces turned up, plus the band round the lever; then chips of
    an undercoat on convex edges (occlusion measured inside the solid) inside named regions;
  * a second bake gives roughness, toward matt under dirt;
  * every other material of the front is untouched; the glb is written beside the front's own as
    the spec's "out", with the two pictures beside it for inspection.
"""
import json
import math
import os
import sys
import time

GAME_INPUTS = "F:/LedgerTools/game-inputs"
FRONTS_REL = "production/assets/shop-fronts"
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def dirt_colour(paint, spec):
    """The dirt a paint is drawn toward: the spec's hue at dirt_luminance of the paint's own luminance."""
    hue = spec["dirt_hue"]
    # on a near-black paint road dirt dries a little lighter and browner than the paint: a floor (22 October, the
    # ironmonger's dark green and black, luminance 0.04 and 0.02; 0 keeps Rita's as they were)
    k = max(lum(paint) * spec["dirt_luminance"], spec.get("dirt_luminance_floor", 0.0)) / lum(hue)
    return [h * k for h in hue]


def one_texture_per_picture(glb):
    """The exporter writes one glTF texture per material that uses a picture, and Unreal's import makes
    one texture asset per glTF texture: the three paints' one atlas came in three times (22 October,
    about 25 MB of the card's memory for nothing). Every texture reference is pointed at the first
    texture of its (picture, sampler) and the rest dropped; the file is rewritten in place."""
    import struct
    data = open(glb, "rb").read()
    jlen = struct.unpack("<I", data[12:16])[0]
    j = json.loads(data[20:20 + jlen])
    rest = data[20 + jlen:]
    first, keep, remap = {}, [], {}
    for i, t in enumerate(j.get("textures", [])):
        key = json.dumps(t, sort_keys=True)
        if key not in first:
            first[key] = len(keep)
            keep.append(t)
        remap[i] = first[key]

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k.endswith("Texture") and isinstance(v, dict) and "index" in v:
                    v["index"] = remap[v["index"]]
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    merged = len(j.get("textures", [])) - len(keep)
    walk(j.get("materials", []))
    j["textures"] = keep
    body = json.dumps(j, separators=(",", ":")).encode("utf-8")
    body += b" " * ((4 - len(body) % 4) % 4)
    total = 12 + 8 + len(body) + len(rest)
    head = data[:8] + struct.pack("<I", total) + struct.pack("<I", len(body)) + data[16:20]
    open(glb, "wb").write(head + body + rest)
    return merged


def main(spec_path):
    import bpy
    import bmesh
    spec = json.load(open(spec_path, encoding="utf-8"))
    src = os.path.join(GAME_INPUTS, FRONTS_REL, spec["front"] + ".glb")
    out_dir = os.path.join(GAME_INPUTS, FRONTS_REL)
    out = os.path.join(out_dir, spec["out"] + ".glb")
    cap = int(os.environ.get("LEDGER_WEAR_PX", 1 << 14))
    px = {name: min(cap, int(n)) for name, n in spec["texture_px"].items()}
    rpx = {name: min(n, int(spec["roughness_px"])) for name, n in px.items()}
    t0 = time.time()

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=src)
    front = [o for o in bpy.context.scene.objects if o.type == "MESH"][0]
    # TRIMMED UNDER A LOW EAVE (23 October; the west row's gates, one fix owed for its three fronts): designed for a
    # two-storey row, each front's cornice tops out at 3.55 m and stands 0.3 m proud, but this single-storey row's
    # slates start at its 3.4 m eave, so the cornice's top showed as a tan strip on the slates and the rest was lost
    # behind the gutter. "clip_top_m" cuts the front there; under it a thin bed moulding stays below the gutter.
    clip = spec.get("clip_top_m")
    if clip:
        bm = bmesh.new()
        bm.from_mesh(front.data)
        bmesh.ops.bisect_plane(bm, geom=list(bm.verts) + list(bm.edges) + list(bm.faces), dist=0.0001,
                               plane_co=(0.0, 0.0, float(clip)), plane_no=(0.0, 0.0, 1.0), clear_outer=True)
        bm.to_mesh(front.data)
        bm.free()
    paints = {}
    for s in front.material_slots:
        if s.material and s.material.name in spec["paints"]:
            bsdf = next(n for n in s.material.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
            paints[s.material.name] = (list(bsdf.inputs["Base Color"].default_value)[:3],
                                       float(bsdf.inputs["Roughness"].default_value))
    missing = [p for p in spec["paints"] if p not in paints]
    if missing:
        raise SystemExit("front_wear: the front has no %s" % missing)

    # THE PAINT FACES INTO AN OBJECT OF THEIR OWN, so the bake touches nothing else and the rest still
    # occludes them.
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = front
    front.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmesh.from_edit_mesh(front.data)
    idx = {i for i, s in enumerate(front.material_slots) if s.material and s.material.name in paints}
    for f in bm.faces:
        f.select = f.material_index in idx
    bmesh.update_edit_mesh(front.data)
    bpy.ops.mesh.separate(type="SELECTED")
    bpy.ops.object.mode_set(mode="OBJECT")
    paint_obj = [o for o in bpy.context.scene.objects if o.type == "MESH" and o is not front][0]
    paint_obj.name = "wear-paints"
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = paint_obj
    paint_obj.select_set(True)
    bpy.ops.object.material_slot_remove_unused()

    # THE UNWRAP: the high faces first, then the low, the high scaled down to detail_ratio less density.
    lever = spec["lever"]
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = paint_obj
    paint_obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")

    def low(f):
        zs = [v.co.z for v in f.verts]
        near = min(math.dist(v.co, lever) for v in f.verts) < 0.35
        return min(zs) < spec["detail_below_m"] or near

    # ONE TEXTURE SET PER PAINT, as a texturing tool makes one per material (22 October, the gate's
    # square view: three paints in one atlas over a black ground, and the narrow faces seen at a slant
    # read the smaller copies of the picture, where the black bled in as hairlines along the mouldings).
    # Each paint's faces fill their own picture; the high faces first, then the low, the high scaled
    # down to detail_ratio less density, then packed.
    bpy.context.scene.tool_settings.use_uv_select_sync = True
    slot_of = {i: s.material.name for i, s in enumerate(paint_obj.material_slots)}
    density = {}
    high_scale = {}
    for name in paints:
        def faces_of(which):
            b2 = bmesh.from_edit_mesh(paint_obj.data)
            return b2, [f for f in b2.faces if slot_of[f.material_index] == name and (low(f) == (which == "low"))]
        dens = {}
        for which in ("high", "low"):
            b2, fs = faces_of(which)
            for f in b2.faces:
                f.select = False
            for f in fs:
                f.select = True
            bmesh.update_edit_mesh(paint_obj.data)
            if fs:
                bpy.ops.uv.smart_project(angle_limit=math.radians(66.0), island_margin=0.003, scale_to_bounds=False)
            b2, fs = faces_of(which)
            uvl = b2.loops.layers.uv.active
            a3 = sum(f.calc_area() for f in fs)
            a2 = 0.0
            for f in fs:
                pts = [l[uvl].uv for l in f.loops]
                a2 += 0.5 * abs(sum(pts[i].x * pts[i - 1].y - pts[i - 1].x * pts[i].y for i in range(len(pts))))
            dens[which] = (a2 / a3 if a3 else 0.0, a3)
        k = math.sqrt(dens["low"][0] / max(dens["high"][0], 1e-12)) / spec["detail_ratio"] if dens["high"][1] else 1.0
        b2, fs = faces_of("high")
        uvl = b2.loops.layers.uv.active
        for f in fs:
            for l in f.loops:
                l[uvl].uv = l[uvl].uv * k
        for f in b2.faces:
            f.select = slot_of[f.material_index] == name
        bmesh.update_edit_mesh(paint_obj.data)
        try:
            bpy.ops.uv.pack_islands(rotate=True, scale=True, margin=0.003)
        except TypeError:
            bpy.ops.uv.pack_islands(rotate=True, margin=0.003)
        density[name] = {w: round(v[1], 2) for w, v in dens.items()}
        high_scale[name] = round(k, 3)
    bpy.ops.object.mode_set(mode="OBJECT")

    # THE BAKE.
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = int(os.environ.get("LEDGER_WEAR_SAMPLES", 8))
    scene.view_settings.view_transform = "Standard"
    scene.render.bake.margin = 16
    atlas, rough = {}, {}
    for name in paints:
        tag = name.replace("paint_", "")
        atlas[name] = bpy.data.images.new("%s_%s_basecolor" % (spec["out"], tag), px[name], px[name], alpha=False)
        rough[name] = bpy.data.images.new("%s_%s_roughness" % (spec["out"], tag), rpx[name], rpx[name], alpha=False)
        rough[name].colorspace_settings.name = "Non-Color"

    def mask_tree(mat, paint, r0):
        nt = mat.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        N = nt.nodes.new
        L = nt.links.new

        def math_(op, a, b=None, clamp=False):
            n = N("ShaderNodeMath")
            n.operation = op
            n.use_clamp = clamp
            for i, v in enumerate((a, b)):
                if v is None:
                    continue
                if isinstance(v, (int, float)):
                    n.inputs[i].default_value = v
                else:
                    L(v, n.inputs[i])
            return n.outputs[0]

        def noise(scale, detail, roughness):
            n = N("ShaderNodeTexNoise")
            n.noise_dimensions = "3D"
            n.inputs["Scale"].default_value = scale
            n.inputs["Detail"].default_value = detail
            n.inputs["Roughness"].default_value = roughness
            L(geo.outputs["Position"], n.inputs["Vector"])
            return n.outputs["Fac"]

        def ao(distance, inside):
            n = N("ShaderNodeAmbientOcclusion")
            n.samples = 16
            n.inside = inside
            n.only_local = inside
            n.inputs["Distance"].default_value = distance
            return n.outputs["AO"]

        def mix(fac, a, b):
            n = N("ShaderNodeMix")
            n.data_type = "RGBA"
            L(fac, n.inputs[0])
            ins = [i for i in n.inputs if i.type == "RGBA"]
            for sock, v in ((ins[0], a), (ins[1], b)):
                if isinstance(v, (list, tuple)):
                    sock.default_value = (v[0], v[1], v[2], 1.0)
                else:
                    L(v, sock)
            return [o for o in n.outputs if o.type == "RGBA"][0]

        def box(x0, x1, z0, z1):
            a = math_("GREATER_THAN", px_, x0)
            b = math_("LESS_THAN", px_, x1)
            c = math_("GREATER_THAN", pz, z0)
            d = math_("LESS_THAN", pz, z1)
            return math_("MULTIPLY", math_("MULTIPLY", a, b), math_("MULTIPLY", c, d))

        geo = N("ShaderNodeNewGeometry")
        sep = N("ShaderNodeSeparateXYZ")
        L(geo.outputs["Position"], sep.inputs[0])
        nsep = N("ShaderNodeSeparateXYZ")
        L(geo.outputs["Normal"], nsep.inputs[0])
        px_, pz = sep.outputs["X"], sep.outputs["Z"]
        n1 = noise(12.0, 6.0, 0.6)
        n2 = noise(70.0, 3.0, 0.5)
        n3 = noise(spec["chip_scale"], 4.0, 0.7)
        # the foot band, its top ragged: top = foot + ragged * (2 n1 - 1); full below foot_full of the top,
        # fading to nothing at it; a damp tide line, darker, just under the top
        top = math_("ADD", spec["foot_m"], math_("MULTIPLY", math_("SUBTRACT", math_("MULTIPLY", n1, 2.0), 1.0), spec["foot_ragged_m"]))
        fade = math_("MULTIPLY", top, 1.0 - spec["foot_full"])
        foot = math_("DIVIDE", math_("SUBTRACT", top, pz), fade, clamp=True)
        foot = math_("MULTIPLY", foot, math_("ADD", 0.8, math_("MULTIPLY", math_("SUBTRACT", n1, 0.5), 0.4)))
        tide = math_("SUBTRACT", 1.0, math_("DIVIDE", math_("ABSOLUTE", math_("SUBTRACT", pz, math_("MULTIPLY", top, 0.85))),
                                            spec["tide_m"]), clamp=True)
        foot = math_("ADD", foot, math_("MULTIPLY", tide, spec["tide"]), clamp=True)
        splash = math_("MULTIPLY", math_("SUBTRACT", 1.0, math_("DIVIDE", pz, spec["splash_m"]), clamp=True),
                       math_("MULTIPLY", math_("SUBTRACT", n2, spec["splash_above"]), 5.0, clamp=True))
        splash = math_("MULTIPLY", splash, spec["splash"])
        occl = math_("SUBTRACT", 1.0, ao(spec["ao_m"], False))
        reach = math_("ADD", math_("MULTIPLY", math_("SUBTRACT", 1.0, math_("DIVIDE", pz, spec["ao_reach_m"]), clamp=True), spec["ao"]),
                      spec["ao_everywhere"])
        aodirt = math_("MULTIPLY", occl, reach)
        ledge = math_("MULTIPLY", math_("DIVIDE", math_("SUBTRACT", nsep.outputs["Z"], 0.7), 0.3, clamp=True),
                      math_("MULTIPLY", math_("ADD", 0.4, math_("MULTIPLY", n1, 0.6)), spec["ledge"]))
        lv = N("ShaderNodeVectorMath")
        lv.operation = "DISTANCE"
        L(geo.outputs["Position"], lv.inputs[0])
        lv.inputs[1].default_value = lever
        lever_band = math_("MULTIPLY", math_("SUBTRACT", 1.0, math_("DIVIDE", lv.outputs["Value"], spec["lever_m"]), clamp=True),
                           spec["lever_weight"])
        m = math_("MAXIMUM", foot, splash)
        m = math_("ADD", math_("ADD", m, aodirt), math_("ADD", ledge, lever_band), clamp=True)
        # chips: convex edges by occlusion inside the solid, spotted by a noise, inside the named regions
        edge = math_("MULTIPLY", math_("SUBTRACT", math_("SUBTRACT", 1.0, ao(spec["chip_edge_m"], True)), 0.1), 8.0, clamp=True)
        region = None
        for r in spec["chip_regions"]:
            # a region may name its paints (23 October, the grocer's: its bronze and its green slab are no paint that
            # chips, the cream render beside them is)
            if "paints" in r and mat.name not in r["paints"]:
                continue
            w = math_("MULTIPLY", box(r["x"][0], r["x"][1], r["z"][0], r["z"][1]), r["amount"])
            region = w if region is None else math_("MAXIMUM", region, w)
        if region is None:
            region = 0.0
        # crisp flakes, not smudges: a hard threshold on the noise times a hard edge
        chip = math_("MULTIPLY", math_("MULTIPLY", math_("SUBTRACT", math_("MULTIPLY", n3, math_("ADD", 0.7, math_("MULTIPLY", n2, 0.6))),
                                                         spec["chip_above"]), 40.0, clamp=True),
                     math_("GREATER_THAN", math_("MULTIPLY", edge, region), 0.5))
        colour = mix(chip, mix(m, paint, dirt_colour(paint, spec)), spec["chip_colour"])
        rmix = math_("ADD", r0, math_("MULTIPLY", math_("MULTIPLY", m, 1.5, clamp=True), spec["roughness_dirt"] - r0))
        rfin = math_("ADD", rmix, math_("MULTIPLY", chip, math_("SUBTRACT", spec["roughness_chip"], rmix)))
        emit = N("ShaderNodeEmission")
        outn = N("ShaderNodeOutputMaterial")
        L(emit.outputs[0], outn.inputs["Surface"])
        return nt, emit, colour, rfin

    trees = {}
    for slot in paint_obj.material_slots:
        mat = slot.material
        paint, r0 = paints[mat.name]
        trees[mat.name] = mask_tree(mat, paint, r0)

    def bake(images, socket_of):
        for name, (nt, emit, colour, rfin) in trees.items():
            image = images[name]
            src_ = socket_of(colour, rfin)
            for l in list(emit.inputs[0].links):
                nt.links.remove(l)
            if src_.type == "VALUE":
                cc = nt.nodes.new("ShaderNodeCombineColor")
                for i in range(3):
                    nt.links.new(src_, cc.inputs[i])
                src_ = cc.outputs[0]
            nt.links.new(src_, emit.inputs[0])
            img = nt.nodes.get("wear-target") or nt.nodes.new("ShaderNodeTexImage")
            img.name = "wear-target"
            img.image = image
            for n in nt.nodes:
                n.select = False
            img.select = True
            nt.nodes.active = img
        bpy.ops.object.select_all(action="DESELECT")
        paint_obj.select_set(True)
        bpy.context.view_layer.objects.active = paint_obj
        bpy.ops.object.bake(type="EMIT", margin=16, use_clear=True)

    tb = time.time()
    bake(atlas, lambda c, r: c)
    bake(rough, lambda c, r: r)
    bake_s = time.time() - tb

    # THE GROUND OF EACH PICTURE, everything the bake and its margin left black, becomes the paint's own
    # clean colour (and roughness), so no smaller copy of the picture can draw anything else.
    import numpy as np

    def fill(im, value):
        w, h = im.size
        buf = np.empty(w * h * 4, dtype=np.float32)
        im.pixels.foreach_get(buf)
        buf = buf.reshape(-1, 4)
        empty = buf[:, :3].sum(axis=1) == 0.0
        buf[empty, :3] = value
        im.pixels.foreach_set(buf.ravel())
        return float(empty.mean())

    def srgb(c):
        return [12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055 for v in c]

    ground = {}
    for name, (paint, r0) in paints.items():
        ground[name] = round(fill(atlas[name], srgb(paint)), 3)
        fill(rough[name], [r0, r0, r0])
        for im, kind in ((atlas[name], "basecolor"), (rough[name], "roughness")):
            im.filepath_raw = os.path.join(out_dir, "%s.png" % im.name)
            im.file_format = "PNG"
            im.save()

    # THE FRONT'S OWN MATERIALS AGAIN, now textured: glTF's Principled, base colour and roughness from
    # the bakes, everything else as the import made it.
    for slot in paint_obj.material_slots:
        mat = slot.material
        nt = mat.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
        outn = nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(bsdf.outputs[0], outn.inputs["Surface"])
        bsdf.inputs["Metallic"].default_value = 0.0
        ti = nt.nodes.new("ShaderNodeTexImage")
        ti.image = atlas[mat.name]
        nt.links.new(ti.outputs["Color"], bsdf.inputs["Base Color"])
        tr = nt.nodes.new("ShaderNodeTexImage")
        tr.image = rough[mat.name]
        sc = nt.nodes.new("ShaderNodeSeparateColor")
        nt.links.new(tr.outputs["Color"], sc.inputs[0])
        nt.links.new(sc.outputs["Green"], bsdf.inputs["Roughness"])
        mat.use_backface_culling = False

    # One mesh again, as the front came.
    bpy.ops.object.select_all(action="DESELECT")
    front.select_set(True)
    paint_obj.select_set(True)
    bpy.context.view_layer.objects.active = front
    bpy.ops.object.join()
    front.name = spec["out"]
    bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", export_image_format="AUTO",
                              export_apply=True, export_yup=True)

    shared = one_texture_per_picture(out)
    # and its door card solid, as the front's own copy is (front_for_game.cut_out_cards, 22 October)
    import importlib.util
    ffg = importlib.util.spec_from_file_location("front_for_game", os.path.join(os.path.dirname(os.path.abspath(__file__)), "front_for_game.py"))
    mod = importlib.util.module_from_spec(ffg)
    ffg.loader.exec_module(mod)
    mod.cut_out_cards(out)
    # and a lit box sign's night glow put back, dark until the game lights it (front_for_game.add_night_glow, 22 October:
    # Blender's own round trip does not keep an emissive map whose factor is 0)
    glow = spec.get("night_glow")
    if glow and not mod.add_night_glow(out, glow["material"], glow["png"]):
        raise SystemExit("front_wear: no material %s for the night glow" % glow["material"])

    report = {"out": out, "textures_merged": shared, "px": px, "bake_s": round(bake_s, 1), "total_s": round(time.time() - t0, 1),
              "density_low_per_high": spec["detail_ratio"], "high_scale": high_scale, "area_m2": density,
              "ground_filled": ground}
    print("front_wear: " + json.dumps(report))
    return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
