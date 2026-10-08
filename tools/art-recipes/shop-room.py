"""A shop's room, seen through its window: built and rendered by script (item 2a, 1 October).

    C:/LedgerTools/blender/4.5.13/blender-4.5.13-windows-x64/blender.exe -b --factory-startup --python tools/art-recipes/shop-room.py -- \
        --shop pawnbroker --out F:/LedgerTools/tmp/shop-rooms [--samples 96] [--gpu]
    C:/LedgerTools/blender/4.5.13/blender-4.5.13-windows-x64/blender.exe -b --factory-startup --python tools/art-recipes/shop-room.py -- \
        --shop pawnbroker --display production/assets/shop-displays/pawnbroker-display.glb
    python tools/art-recipes/shop-room.py --selftest

WHY. Jafar, 1 October: "the shop windows are black voids in every view", and
"fake interiors in the shop windows by interior mapping, as games do it". The
method (production/research/shop-window-interiors/NOTE.md): each shop's room
is one perspective picture taken from in front of its window, per lighting
state, and the game projects it with depth on the card behind the glass. This
builds the room from production/specs/shop-interiors.json (its size, its
trade's fittings), frames the front rectangle exactly (the spec's camera rule)
and renders the day, lit-night and dark-night pictures with a JSON beside them
giving W, H, D and d, which the material needs.

Nothing in a room is a person, a brand, alcohol or gambling (the spec's
"never"). Room coordinates: x across (0 at the centre), y back from the front
plane (the card), z up from the floor.
"""
import json
import math
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPEC = os.path.join(REPO, "production", "specs", "shop-interiors.json")


def project(x, y, z, w, h, d):
    """Where a room point lands in the picture (the spec's camera rule): u, v in 0..1, v up."""
    return 0.5 + (x / w) * d / (d + y), 0.5 + ((z - h / 2.0) / h) * d / (d + y)


def horizontal_fov(w, d):
    return 2.0 * math.atan(w / (2.0 * d))


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("shop-room selftest FAIL " + name)
    w, h, d = 5.3, 2.4, 5.3
    u, v = project(-w / 2, 0.0, 0.0, w, h, d)
    check("the front's corner is the picture's corner", abs(u) < 1e-9 and abs(v) < 1e-9)
    u, v = project(w / 2, w, h, w, h, d)
    check("a cube-deep back wall fills half the picture (Golus)", abs(u - 0.75) < 1e-9 and abs(v - 0.75) < 1e-9)
    check("the field frames the front exactly", abs(math.tan(horizontal_fov(w, d) / 2) * d * 2 - w) < 1e-9)
    spec = json.load(open(SPEC, encoding="utf-8"))
    check("every shop has a room and a camera", all("room" in s and s.get("camera_d", 0) > 0 for s in spec["shops"]))
    print("shop-room selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


# ---------------------------------------------------------------- Blender side
def build_and_render(argv):
    import bpy
    shop_id = argv[argv.index("--shop") + 1]
    # absolute: Blender resolves a relative render path against its own root, not the working directory
    out = os.path.abspath(argv[argv.index("--out") + 1])
    samples = int(argv[argv.index("--samples") + 1]) if "--samples" in argv else 96
    spec = json.load(open(SPEC, encoding="utf-8"))
    shop = next(s for s in spec["shops"] if s["id"] == shop_id)
    W, H, D = shop["room"]["w"], shop["room"]["h"], shop["room"]["d"]
    # A REAL ROOM FOR THE GAME (--export-room, 3 October; production/research/shop-window-
    # interiors/CLOSE-RANGE-2026-10-03.md): built as for its picture, but its ceiling above the
    # window head (2.9 m from its floor) and its walls 12 cm thick, as Lumen wants them.
    EXPORT = "--export-room" in argv
    if EXPORT:
        H = shop["room"].get("h_real", 2.9)
    d = shop["camera_d"]
    os.makedirs(out, exist_ok=True)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.cycles.device = "GPU" if "--gpu" in argv else "CPU"
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x = shop["pixels_wide"]
    sc.render.resolution_y = int(round(shop["pixels_wide"] * H / W))
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_depth = "8"
    sc.world = bpy.data.worlds.new("world")
    sc.world.use_nodes = True
    bg = sc.world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)

    mats = {}

    def mat(name, colour, rough=0.6, metal=0.0, emit=None, emit_strength=0.0, glass=False, noise=0.0):
        if name in mats:
            return mats[name]
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        nt = m.node_tree
        p = nt.nodes["Principled BSDF"]
        p.inputs["Base Color"].default_value = (*colour, 1.0)
        p.inputs["Roughness"].default_value = rough
        p.inputs["Metallic"].default_value = metal
        if glass:
            p.inputs["Transmission Weight"].default_value = 1.0
            p.inputs["IOR"].default_value = 1.5
            p.inputs["Roughness"].default_value = 0.02
        if emit is not None:
            p.inputs["Emission Color"].default_value = (*emit, 1.0)
            p.inputs["Emission Strength"].default_value = emit_strength
        if noise > 0.0:
            # a little unevenness, so nothing reads as a flat colour: paint, worn floor
            tex = nt.nodes.new("ShaderNodeTexNoise")
            tex.inputs["Scale"].default_value = 6.0
            ramp = nt.nodes.new("ShaderNodeMixRGB")
            ramp.blend_type = "MULTIPLY"
            ramp.inputs["Fac"].default_value = noise
            ramp.inputs["Color1"].default_value = (*colour, 1.0)
            nt.links.new(tex.outputs["Fac"], ramp.inputs["Color2"])   # grey: the noise's own colours tinted everything pastel (3 October)
            nt.links.new(ramp.outputs["Color"], p.inputs["Base Color"])
        mats[name] = m
        return m

    def box(name, x0, x1, y0, y1, z0, z1, m):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
        o = bpy.context.object
        o.name = name
        o.scale = (max(x1 - x0, 1e-3), max(y1 - y0, 1e-3), max(z1 - z0, 1e-3))
        o.data.materials.append(m)
        return o

    def cyl(name, x, y, z, r, depth, m, axis="z", verts=24):
        rot = {"z": (0, 0, 0), "x": (0, math.pi / 2, 0), "y": (math.pi / 2, 0, 0)}[axis]
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=(x, y, z), rotation=rot)
        o = bpy.context.object
        o.name = name
        o.data.materials.append(m)
        return o

    def text(name, body, x, y, z, size, m, rot_x=math.pi / 2, font=None, extrude=0.002, res=None):
        bpy.ops.object.text_add(location=(x, y, z), rotation=(rot_x, 0, 0))
        o = bpy.context.object
        o.name = name
        o.data.body = body
        o.data.size = size
        if font:
            # OUR OWN TYPEFACES (production/fonts, OFL), never Blender's default
            o.data.font = bpy.data.fonts.load(os.path.join(REPO, "production", "fonts", font), check_existing=True)
        if shop["id"] == "mickeys":
            # LIGHT LETTERING for a real room in git (4 October: at Blender's curve resolution its
            # notices made most of 615,000 triangles): coarser curves, small print flat
            o.data.resolution_u = 3
            if size < 0.05:
                o.data.extrude = 0.0
        o.data.align_x = "CENTER"
        o.data.extrude = extrude
        if res is not None:
            o.data.resolution_u = res
        o.data.materials.append(m)
        return o

    POLY = os.environ.get("LEDGER_POLYHAVEN", "F:/LedgerTools/polyhaven")

    def model(asset, x, y, z, turn=0.0, size=None, res="1k"):
        """A Poly Haven model (CC0; tools/art-recipes/fetch_polyhaven.py) stood with its base at z,
        centred on x and y, turned about the vertical; scaled so its largest side is size metres
        when size is given, otherwise at its own real size."""
        folder = os.path.join(POLY, asset, res)
        gl = next((f for f in os.listdir(folder) if f.endswith(".gltf")), None) if os.path.isdir(folder) else None
        if gl is None:
            print("shop-room: model %s missing (run fetch_polyhaven.py)" % asset, flush=True)
            return None
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=os.path.join(folder, gl))
        new = [o for o in bpy.data.objects if o not in before]
        meshes = [o for o in new if o.type == "MESH"]
        if not meshes:
            return None
        root = bpy.data.objects.new(asset + "_root", None)
        sc.collection.objects.link(root)
        for o in new:
            if o.parent is None:
                o.parent = root
        bpy.context.view_layer.update()
        from mathutils import Vector
        pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
        lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
        hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
        k = 1.0
        if size:
            k = size / max(hi.x - lo.x, hi.y - lo.y, hi.z - lo.z, 1e-4)
        root.scale = (k, k, k)
        root.rotation_euler = (0.0, 0.0, turn)
        centre = Vector(((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, lo.z))
        root.location = (x - centre.x * k, y - centre.y * k, z - centre.z * k)
        return root

    # THE SHELL: floor, walls, ceiling. The front is open: the card is the front plane.
    # A WORN LINO OF TWO CLOSE BROWNS, 1 October's second pass: the first, a bold
    # cream-and-brown checker, read as a clean render in the game and blew out
    # white under the tubes at night; a pawnbroker's floor was old and trodden.
    # THE THIRD PASS (1 October, after a fresh reviewer: "a spotless, evenly lit
    # showroom"): an old patterned lino and painted plaster from Poly Haven's
    # textures (CC0), laid in world metres, tinted to the room's colours.
    def texmat(name, asset, tile_m, tint, base=None):
        folder = os.path.join(POLY, asset, "1k", "textures")
        if not os.path.isdir(folder):
            print("shop-room: texture %s missing (run fetch_polyhaven.py %s)" % (asset, asset), flush=True)
            return base
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        nt = m.node_tree
        p = nt.nodes["Principled BSDF"]
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = (1.0 / tile_m, 1.0 / tile_m, 1.0 / tile_m)
        nt.links.new(geo.outputs["Position"], mp.inputs["Vector"])

        def img(kind, colour):
            path = next((os.path.join(folder, f) for f in os.listdir(folder) if "_%s_" % kind in f), None)
            if path is None:
                return None
            n = nt.nodes.new("ShaderNodeTexImage")
            n.image = bpy.data.images.load(path, check_existing=True)
            n.image.colorspace_settings.name = "sRGB" if colour else "Non-Color"
            n.projection = "BOX"
            n.projection_blend = 0.2
            nt.links.new(mp.outputs["Vector"], n.inputs["Vector"])
            return n
        d = img("diff", True)
        if d is not None:
            mul = nt.nodes.new("ShaderNodeMixRGB")
            mul.blend_type = "MULTIPLY"
            mul.inputs["Fac"].default_value = 1.0
            mul.inputs["Color2"].default_value = (*tint, 1.0)
            nt.links.new(d.outputs["Color"], mul.inputs["Color1"])
            nt.links.new(mul.outputs["Color"], p.inputs["Base Color"])
        r = img("arm", False) or img("rough", False)
        if r is not None:
            sep = nt.nodes.new("ShaderNodeSeparateColor")
            nt.links.new(r.outputs["Color"], sep.inputs["Color"])
            nt.links.new(sep.outputs["Green" if "_arm_" in r.image.filepath else "Red"], p.inputs["Roughness"])
        nm = img("nor_gl", False)
        if nm is not None:
            nmap = nt.nodes.new("ShaderNodeNormalMap")
            nt.links.new(nm.outputs["Color"], nmap.inputs["Color"])
            nt.links.new(nmap.outputs["Normal"], p.inputs["Normal"])
        mats[name] = m
        return m

    floor_lino = texmat("lino_old", "old_linoleum_flooring_01", 1.2, (0.62, 0.55, 0.50),
                        base=mat("vinyl_a", (0.30, 0.25, 0.19), rough=0.6, noise=0.45))
    if shop["id"] == "fishmonger":
        # RED QUARRY TILES, wet: a fish shop's floor was hosed down (the trade's own floor)
        fm = bpy.data.materials.new("quarry_tile")
        fm.use_nodes = True
        fnt = fm.node_tree
        fp = fnt.nodes["Principled BSDF"]
        fbr = fnt.nodes.new("ShaderNodeTexBrick")
        fbr.offset = 0.0
        fbr.inputs["Scale"].default_value = 1.0 / 0.15
        fbr.inputs["Mortar Size"].default_value = 0.02
        fbr.inputs["Color1"].default_value = (0.32, 0.10, 0.06, 1.0)
        fbr.inputs["Color2"].default_value = (0.26, 0.08, 0.05, 1.0)
        fbr.inputs["Mortar"].default_value = (0.12, 0.10, 0.09, 1.0)
        fbr.inputs["Brick Width"].default_value = 1.0
        fbr.inputs["Row Height"].default_value = 1.0
        fgeo = fnt.nodes.new("ShaderNodeNewGeometry")
        fnt.links.new(fgeo.outputs["Position"], fbr.inputs["Vector"])
        fnt.links.new(fbr.outputs["Color"], fp.inputs["Base Color"])
        fp.inputs["Roughness"].default_value = 0.12
        floor_lino = fm
    if shop["id"] == "mickeys":
        # A BROWN CARPET, trodden (offices of 1987: "dark brown carpet", cab-office-interior-1990 NOTE-2)
        floor_lino = texmat("carpet_dirty", "dirty_carpet", 1.0, (0.78, 0.46, 0.22),
                            base=mat("carpet_brown", (0.095, 0.060, 0.038), rough=0.95, noise=0.45))
    box("floor", -W / 2, W / 2, 0, D, -0.02, 0.0, floor_lino)
    wall = texmat("plaster_cream", "painted_plaster_wall", 1.5, (0.95, 0.86, 0.66),
                  base=mat("paint_cream", (0.55, 0.50, 0.39), rough=0.85, noise=0.3))
    dado = texmat("plaster_brown", "painted_plaster_wall", 1.5, (0.42, 0.27, 0.17),
                  base=mat("paint_brown", (0.22, 0.14, 0.09), rough=0.6, noise=0.1))
    ceiling = mat("ceiling", (0.70, 0.68, 0.62), rough=0.9)
    if shop["id"] == "fishmonger":
        # WHITE GLAZED TILES TO THE CEILING (Picture Sheffield t13140, c.1989, seen 3 October),
        # square, grey grout, a little soiled; the dado the same tiles.
        def tiles(name, colour, size_m):
            m = bpy.data.materials.new(name)
            m.use_nodes = True
            nt = m.node_tree
            p = nt.nodes["Principled BSDF"]
            geo = nt.nodes.new("ShaderNodeNewGeometry")
            br = nt.nodes.new("ShaderNodeTexBrick")
            br.offset = 0.0
            br.inputs["Scale"].default_value = 1.0 / size_m
            br.inputs["Mortar Size"].default_value = 0.012
            br.inputs["Color1"].default_value = (*colour, 1.0)
            br.inputs["Color2"].default_value = (colour[0] * 0.95, colour[1] * 0.95, colour[2] * 0.93, 1.0)
            br.inputs["Mortar"].default_value = (0.42, 0.42, 0.40, 1.0)
            br.inputs["Brick Width"].default_value = 1.0
            br.inputs["Row Height"].default_value = 1.0
            # along the wall (x on the back wall, y on the sides) and up: an upright wall's tiles
            sep = nt.nodes.new("ShaderNodeSeparateXYZ")
            add = nt.nodes.new("ShaderNodeMath")
            add.operation = "ADD"
            comb = nt.nodes.new("ShaderNodeCombineXYZ")
            nt.links.new(geo.outputs["Position"], sep.inputs["Vector"])
            nt.links.new(sep.outputs["X"], add.inputs[0])
            nt.links.new(sep.outputs["Y"], add.inputs[1])
            nt.links.new(add.outputs["Value"], comb.inputs["X"])
            nt.links.new(sep.outputs["Z"], comb.inputs["Y"])
            nt.links.new(comb.outputs["Vector"], br.inputs["Vector"])
            # SOILED, a working shop's (the first pass read as a showroom): grime in broad
            # patches and darker toward the floor
            noise = nt.nodes.new("ShaderNodeTexNoise")
            noise.inputs["Scale"].default_value = 2.5
            nt.links.new(geo.outputs["Position"], noise.inputs["Vector"])
            grime = nt.nodes.new("ShaderNodeMixRGB")
            grime.blend_type = "MULTIPLY"
            grime.inputs["Fac"].default_value = 0.45
            nt.links.new(br.outputs["Color"], grime.inputs["Color1"])
            nt.links.new(noise.outputs["Fac"], grime.inputs["Color2"])   # grey, never the noise's own colours
            nt.links.new(grime.outputs["Color"], p.inputs["Base Color"])
            p.inputs["Roughness"].default_value = 0.22
            mats[name] = m
            return m
        wall = tiles("tile_white", (0.78, 0.78, 0.74), 0.152)
        dado = tiles("tile_white_lower", (0.66, 0.66, 0.61), 0.152)
    if shop["id"] == "tea_room":
        # a warm papered room over a dark green dado, as a seaside tea room's was
        wall = texmat("plaster_peach", "painted_plaster_wall", 1.5, (0.98, 0.84, 0.70),
                      base=mat("paint_peach", (0.62, 0.50, 0.40), rough=0.85, noise=0.3))
        dado = mat("paint_green", (0.06, 0.14, 0.09), rough=0.5, noise=0.15)
    if shop["id"] == "chandler":
        # a chandler's distempered walls, sea-green, over a dark blue dado
        wall = texmat("plaster_seagreen", "painted_plaster_wall", 1.5, (0.72, 0.80, 0.70),
                      base=mat("paint_seagreen", (0.45, 0.52, 0.45), rough=0.85, noise=0.3))
        dado = mat("paint_navy", (0.04, 0.06, 0.12), rough=0.5, noise=0.15)
    if shop["id"] == "mickeys":
        # MAGNOLIA GONE YELLOW WITH SMOKE over a wood-effect dado, the ceiling the same
        # nicotine cream: a cab office open day and night since the sixties (tobacco is allowed).
        # (darker than first built: in the game the room read as a clean beige showroom)
        wall = texmat("plaster_nicotine", "painted_plaster_wall", 1.5, (0.66, 0.54, 0.34),
                      base=mat("paint_nicotine", (0.38, 0.31, 0.19), rough=0.85, noise=0.3))
        dado = mat("dado_wood_effect", (0.14, 0.085, 0.045), rough=0.45, noise=0.25)
        ceiling = mat("ceiling_nicotine", (0.46, 0.40, 0.29), rough=0.9, noise=0.2)
    t = 0.12 if EXPORT else 0.05
    if EXPORT:
        box("floor_slab", -W / 2 - t, W / 2 + t, 0, D + t, -0.12, -0.02, floor_lino)
    box("wall_left", -W / 2 - t, -W / 2, 0, D, 0, H, wall)
    box("wall_right", W / 2, W / 2 + t, 0, D, 0, H, wall)
    # MICKEY'S BACK WALL OPEN AT ITS DOOR (8 October, item 1.1's third review, V9: "the room
    # beyond the door flat untextured grey"): his back room is built behind it (below, with his
    # fittings), where a painted board stood in the doorway
    back_gap = (1.1 - 1.12, 1.95 - 1.12) if shop["id"] == "mickeys" else None
    if back_gap:
        box("wall_back", -W / 2, back_gap[0], D, D + t, 0, H, wall)
        box("wall_back", back_gap[1], W / 2, D, D + t, 0, H, wall)
        box("wall_back", back_gap[0], back_gap[1], D, D + t, 2.0, H, wall)
    else:
        box("wall_back", -W / 2, W / 2, D, D + t, 0, H, wall)
    box("ceiling", -W / 2, W / 2, 0, D, H, H + t, ceiling)
    for side, x0, x1 in (("left", -W / 2, -W / 2 + 0.01), ("right", W / 2 - 0.01, W / 2)):
        box("dado_" + side, x0, x1, 0, D, 0, 0.95, dado)
    if back_gap:
        box("dado_back", -W / 2, back_gap[0], D - 0.01, D, 0, 0.95, dado)
        box("dado_back", back_gap[1], W / 2, D - 0.01, D, 0, 0.95, dado)
    else:
        box("dado_back", -W / 2, W / 2, D - 0.01, D, 0, 0.95, dado)
    # The back door, half open onto a dark back room.
    door = mat("door", (0.28, 0.17, 0.10), rough=0.5, noise=0.1)
    dark = mat("back_room", (0.02, 0.02, 0.02), rough=1.0)
    # MICKEY'S BACK DOOR where its plan has it (production/specs/mickeys-office.json: x 5.0 to 6.1
    # along the street, so just right of the room's centre seen from the window), onto Sheila's
    # back room, lit: not a black gap.
    dx = -1.12 if shop["id"] == "mickeys" else 0.0
    if shop["id"] == "mickeys":
        dark = mat("back_room_lit", (0.13, 0.10, 0.07), rough=0.9)
    if not back_gap:
        box("door_gap", 1.1 + dx, 1.95 + dx, D - 0.02, D + 0.06, 0, 2.0, dark)
    for name, fx0, fx1, fz0, fz1 in (("door_frame_l", 1.02, 1.1, 0, 2.08), ("door_frame_r", 1.95, 2.03, 0, 2.08),
                                     ("door_frame_head", 1.02, 2.03, 2.0, 2.08)):
        box(name, fx0 + dx, fx1 + dx, D - 0.035, D - 0.005, fz0, fz1, door)
    door_leaf = box("door_leaf", 1.1 + dx, 1.92 + dx, D - 0.06, D - 0.02, 0, 1.98, door)
    door_leaf.rotation_euler[2] = math.radians(-35)
    # ITS KNOB, on the open edge, room side (the second review: "the door has no handle")
    th_ = math.radians(-35)
    ax_, ay_ = 1.51 + dx + 0.34 * math.cos(th_), D - 0.04 + 0.34 * math.sin(th_)
    nx_, ny_ = math.sin(th_), -math.cos(th_)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.03,
                                         location=(ax_ + 0.045 * nx_, ay_ + 0.045 * ny_, 1.0))
    bpy.context.object.name = "door_knob"
    bpy.context.object.data.materials.append(mat("door_brass", (0.55, 0.40, 0.16), rough=0.3, metal=1.0))

    # THE TUBES: three T12 battens across the ceiling, 1.5 m long (an empty unit has a bare bulb).
    # LIT IN A REAL ROOM (4 October: a fresh reviewer saw Mickey's battens dark): the exported
    # tubes glow; the pictures set their strength per lighting state below
    # AN OPAL DIFFUSER OVER EACH, 7 October (his order: "the ragged white strip across the top pane"):
    # seen from the pavement through the top pane, the bare 38 mm tube burned out to a hard white
    # line, ragged under the game's upscaler. The office and shop fitting of 1990 was the batten
    # with an opal diffuser: a soft white box 15 cm wide, far dimmer per square metre than the bare
    # tube. The glowing material keeps its name, tube_on, which the game switches off and on.
    tube_on = mat("tube_on", (0.92, 0.94, 0.93), rough=0.5, emit=(0.95, 0.97, 1.0), emit_strength=1.8 if EXPORT else 0.0)
    batten = mat("batten", (0.75, 0.75, 0.72), rough=0.5)
    for k, y in enumerate((1.0, 2.4, 3.8) if shop["id"] != "to_let" else ()):
        if y > D - 0.3:
            continue
        box("batten_%d" % k, -0.8, 0.8, y - 0.09, y + 0.09, H - 0.03, H - 0.01, batten)
        box("tube_%d" % k, -0.78, 0.78, y - 0.075, y + 0.075, H - 0.09, H - 0.03, tube_on)

    # BOARDS, for the trades that had them (the ironmonger's and the chandler's): worn timber
    # laid over the lino, as the empty unit's are.
    def boards(name, c1, c2):
        bm = bpy.data.materials.new(name)
        bm.use_nodes = True
        bnt = bm.node_tree
        bp = bnt.nodes["Principled BSDF"]
        bbr = bnt.nodes.new("ShaderNodeTexBrick")
        bbr.inputs["Scale"].default_value = 1.0
        bbr.inputs["Mortar Size"].default_value = 0.004
        bbr.inputs["Brick Width"].default_value = 2.4
        bbr.inputs["Row Height"].default_value = 0.15
        bbr.inputs["Color1"].default_value = (*c1, 1.0)
        bbr.inputs["Color2"].default_value = (*c2, 1.0)
        bbr.inputs["Mortar"].default_value = (0.04, 0.03, 0.02, 1.0)
        bgeo = bnt.nodes.new("ShaderNodeNewGeometry")
        bnt.links.new(bgeo.outputs["Position"], bbr.inputs["Vector"])
        bno = bnt.nodes.new("ShaderNodeTexNoise")
        bno.inputs["Scale"].default_value = 3.0
        bnt.links.new(bgeo.outputs["Position"], bno.inputs["Vector"])
        bmix = bnt.nodes.new("ShaderNodeMixRGB")
        bmix.blend_type = "MULTIPLY"
        bmix.inputs["Fac"].default_value = 0.35
        bnt.links.new(bbr.outputs["Color"], bmix.inputs["Color1"])
        bnt.links.new(bno.outputs["Fac"], bmix.inputs["Color2"])
        bnt.links.new(bmix.outputs["Color"], bp.inputs["Base Color"])
        bp.inputs["Roughness"].default_value = 0.7
        return bm

    def place(asset, x, y, z, rot=(0.0, 0.0, 0.0), size=None, upright=False):
        """A Poly Haven model turned any way (a tool hung flat on a wall, a broom stood on end),
        then stood with its bounds' centre at x, y and its lowest point at z."""
        root = model(asset, 0.0, 0.0, 0.0, size=size)
        if root is None:
            return None
        return turn_and_settle(bpy, root, x, y, z, rot, upright)

    def boarded(x0, x1, cy0, wood):
        """A counter's front boarded, tongue and groove, rubbed pale where knees and bags
        catch it (3 October: a plain front read as a blank box from the street)."""
        groove = mat("groove", (0.07, 0.04, 0.02), rough=0.6)
        xg = x0 + 0.1
        while xg < x1 - 0.05:
            box("counter_groove", xg, xg + 0.006, cy0 - 0.008, cy0, 0.1, 0.9, groove)
            xg += 0.095
        # (no rubbed patch: drawn as a box it read as a pale panel set in the front)

    # A NEWSAGENT AND TOBACCONIST (V1, 3 October; west_north bay 0): the papers on a stepped
    # stand down the left wall with greeting cards above, the magazines on a rack down the
    # right; the counter across with chocolate bars along its front and the till, and at its
    # right end the pension counter's glazed screen (hook-cast: "the newsagent's counter, where
    # the pensions are paid"); behind it the cigarettes in their gantry (tobacco is allowed) and
    # jars of sweets on the shelves above. Nothing of gambling: no pools coupons (canon).
    if shop["id"] == "newsagent":
        import random
        rnd = random.Random(21)
        wood = mat("counter_wood", (0.17, 0.10, 0.055), rough=0.45, noise=0.25)
        top = mat("counter_top", (0.42, 0.37, 0.30), rough=0.35, noise=0.1)
        shelfm = mat("shelf", (0.38, 0.27, 0.16), rough=0.6, noise=0.15)
        paper = mat("newsprint", (0.70, 0.69, 0.64), rough=0.85, noise=0.25)
        print_grey = mat("print_grey", (0.30, 0.30, 0.30), rough=0.85)
        glassm = mat("glass", (1.0, 1.0, 1.0), glass=True)
        ink = mat("ink", (0.05, 0.05, 0.08), rough=0.8)
        card = mat("card_white", (0.85, 0.83, 0.76), rough=0.85)
        cy0, cy1 = D - 1.2, D - 0.72     # near the back wall, where a projected room holds (3 October)
        box("counter", -W / 2 + 0.2, 1.3, cy0, cy1, 0.0, 0.92, wood)
        box("counter_top", -W / 2 + 0.18, 1.32, cy0 - 0.02, cy1 + 0.02, 0.92, 0.95, top)
        box("counter_kick", -W / 2 + 0.2, 1.3, cy0 - 0.006, cy0, 0.0, 0.1, mat("kick_black", (0.03, 0.03, 0.03), rough=0.5))
        boarded(-W / 2 + 0.2, 1.3, cy0, wood)
        # chocolate bars in their open boxes along the counter's front edge
        bars = [(0.30, 0.06, 0.05), (0.50, 0.38, 0.08), (0.08, 0.14, 0.34), (0.38, 0.06, 0.20), (0.62, 0.55, 0.12), (0.18, 0.09, 0.04)]
        boxcard = mat("box_card", (0.55, 0.50, 0.40), rough=0.8)
        x = -W / 2 + 0.35
        while x < -0.3:
            c = rnd.choice(bars)
            m = mat("bars_%d_%d_%d" % tuple(int(v * 99) for v in c), c, rough=0.4)
            box("bar_box", x, x + 0.2, cy0 + 0.03, cy0 + 0.2, 0.95, 0.985, boxcard)
            for k in range(5):
                box("bar", x + 0.012 + k * 0.037, x + 0.044 + k * 0.037, cy0 + 0.04, cy0 + 0.19, 0.96, 0.995, m)
            x += 0.22
        model("CashRegister_01", -0.05, cy0 + 0.25, 0.95, turn=math.pi + 0.15, size=0.4)
        # the pension counter: a glazed screen in a wooden frame on the counter's right end, its card above
        frame = mat("screen_frame", (0.22, 0.14, 0.08), rough=0.5)
        box("screen_glass", 0.35, 1.3, cy0 + 0.1, cy0 + 0.11, 0.95, 1.75, glassm)
        for xx in (0.35, 0.81, 1.265):
            box("screen_post", xx, xx + 0.035, cy0 + 0.09, cy0 + 0.12, 0.95, 1.78, frame)
        box("screen_head", 0.35, 1.3, cy0 + 0.09, cy0 + 0.12, 1.75, 1.8, frame)
        box("pension_card", 0.40, 1.25, cy0 + 0.085, cy0 + 0.09, 1.82, 1.97, card)
        text("pension_text", "PENSIONS & ALLOWANCES", 0.825, cy0 + 0.08, 1.875, 0.042, ink)
        # THE GANTRY behind the counter: the cigarettes, rows of their packets in a dark unit
        dark = mat("gantry_wood", (0.10, 0.06, 0.035), rough=0.5)
        gx0, gx1 = -W / 2 + 0.25, 1.0
        box("gantry", gx0, gx1, D - 0.32, D - 0.02, 0.95, 1.78, dark)
        packs = [(0.82, 0.81, 0.77), (0.62, 0.06, 0.05), (0.62, 0.50, 0.20), (0.08, 0.12, 0.32), (0.75, 0.75, 0.77),
                 (0.06, 0.24, 0.12), (0.25, 0.08, 0.28), (0.05, 0.05, 0.05)]
        for row in range(5):
            z = 1.0 + row * 0.155
            box("gantry_shelf", gx0, gx1, D - 0.36, D - 0.32, z - 0.012, z, shelfm)
            x = gx0 + 0.03
            run_c = rnd.choice(packs)
            while x < gx1 - 0.07:
                if rnd.random() < 0.25:
                    run_c = rnd.choice(packs)
                m = mat("cigs_%d_%d_%d" % tuple(int(v * 99) for v in run_c), run_c, rough=0.35)
                box("cig_pack", x, x + 0.056, D - 0.35, D - 0.33, z, z + 0.088, m)
                x += 0.062
        # the jars of sweets above, on two shelves (the lower one stops short of the back door)
        lid = mat("jar_lid", (0.50, 0.08, 0.05), rough=0.4)
        sweets = [(0.78, 0.18, 0.22), (0.82, 0.66, 0.12), (0.22, 0.50, 0.18), (0.88, 0.45, 0.08), (0.50, 0.12, 0.36),
                  (0.84, 0.83, 0.78), (0.32, 0.16, 0.07), (0.90, 0.60, 0.65)]
        for z, xr in ((1.86, 1.0), (2.12, W / 2 - 0.05)):
            box("jar_shelf", -W / 2 + 0.05, xr, D - 0.24, D - 0.02, z - 0.02, z, shelfm)
            x = -W / 2 + 0.16
            while x < xr - 0.08:
                c = rnd.choice(sweets)
                cyl("jar", x, D - 0.13, z + 0.1, 0.055, 0.2, glassm)
                cyl("sweets", x, D - 0.13, z + 0.07, 0.05, 0.14, mat("sweet_%d_%d_%d" % tuple(int(v * 99) for v in c), c, rough=0.25, noise=0.5))
                cyl("jar_lid", x, D - 0.13, z + 0.21, 0.042, 0.025, lid)
                x += 0.135
        # THE PAPERS down the left wall, folded on a stand of three tiers stepping back to the
        # wall, each title a run of its own copies under a band of colour (no real titles)
        stand = mat("stand_wood", (0.34, 0.24, 0.14), rough=0.6, noise=0.1)
        heads = [(0.55, 0.05, 0.04), (0.06, 0.10, 0.30), (0.04, 0.04, 0.04), (0.55, 0.05, 0.04), (0.30, 0.30, 0.32)]
        for k, (z, xin) in enumerate(((0.55, 0.52), (0.85, 0.40), (1.15, 0.28))):
            box("paper_tier", -W / 2, -W / 2 + xin, 0.45, 2.35, z - 0.02, z, stand)
            box("paper_riser", -W / 2 + xin - 0.02, -W / 2 + xin, 0.45, 2.35, z - 0.3 if k else 0.0, z, stand)
            y = 0.5
            while y < 2.25:
                h = rnd.choice(heads)
                pw = 0.3 if rnd.random() < 0.5 else 0.38     # a tabloid, or a broadsheet folded
                if y + pw > 2.32:
                    break
                n = rnd.randint(6, 12)
                for j in range(n):
                    box("paper", -W / 2 + 0.03, -W / 2 + xin - 0.03, y, y + pw - 0.02, z + j * 0.006, z + j * 0.006 + 0.005, paper)
                zt = z + n * 0.006
                hm = mat("head_%d_%d_%d" % tuple(int(v * 99) for v in h), h, rough=0.6)
                box("masthead", -W / 2 + xin - 0.11, -W / 2 + xin - 0.05, y + 0.01, y + pw - 0.03, zt, zt + 0.002, hm)
                for q in range(3):
                    box("print", -W / 2 + xin - 0.2 - q * 0.04, -W / 2 + xin - 0.18 - q * 0.04, y + 0.02, y + pw - 0.04, zt, zt + 0.001, print_grey)
                y += pw + 0.02
        # greeting cards in a wall rack above the papers, in rows
        pastel = [(0.80, 0.70, 0.72), (0.70, 0.78, 0.82), (0.85, 0.82, 0.62), (0.74, 0.80, 0.68), (0.86, 0.84, 0.80), (0.45, 0.10, 0.12)]
        box("card_rack", -W / 2 + 0.005, -W / 2 + 0.03, 0.5, 2.3, 1.42, 2.25, mat("rack_brown", (0.25, 0.16, 0.09), rough=0.6))
        for row in range(4):
            z = 1.46 + row * 0.2
            y = 0.55
            while y < 2.15:
                c = rnd.choice(pastel)
                box("greeting_card", -W / 2 + 0.03, -W / 2 + 0.036, y, y + 0.12, z, z + 0.17, mat("gc_%d_%d_%d" % tuple(int(v * 99) for v in c), c, rough=0.7, noise=0.4))
                y += 0.135
        # THE MAGAZINES down the right wall, five tiers, each cover its picture's colours
        # under a title band
        covers = [(0.55, 0.10, 0.08), (0.10, 0.20, 0.42), (0.75, 0.62, 0.20), (0.15, 0.32, 0.18), (0.45, 0.30, 0.50),
                  (0.80, 0.78, 0.72), (0.05, 0.05, 0.06), (0.65, 0.35, 0.15)]
        bands = [mat("band_white", (0.88, 0.87, 0.82), rough=0.5), mat("band_red", (0.65, 0.05, 0.05), rough=0.5),
                 mat("band_yellow", (0.85, 0.72, 0.10), rough=0.5)]
        for k, z in enumerate((0.55, 0.9, 1.25, 1.6, 1.95)):
            box("mag_shelf", W / 2 - 0.3, W / 2, 0.4, 2.35, z - 0.02, z, shelfm)
            box("mag_lip", W / 2 - 0.3, W / 2 - 0.28, 0.4, 2.35, z, z + 0.05, shelfm)
            y = 0.43
            while y < 2.1:
                c = rnd.choice(covers)
                cm = mat("cover_%d_%d_%d" % tuple(int(v * 99) for v in c), c, rough=0.3, noise=0.6)
                # each turned to face the door and the window, as a rack shows its covers
                mg = box("magazine", W / 2 - 0.2, W / 2 - 0.19, y, y + 0.21, z, z + 0.29, cm)
                bd = box("mag_band", W / 2 - 0.201, W / 2 - 0.2, y + 0.005, y + 0.205, z + 0.23, z + 0.28, rnd.choice(bands))
                for o in (mg, bd):
                    o.rotation_euler = (0.0, 0.0, 0.6)
                    o.location = (o.location.x - 0.05, o.location.y, o.location.z)
                y += 0.2
    # AN IRONMONGER (V1, 3 October; west_north bay 1): the back wall a cabinet of small drawers
    # to the ceiling, each with its knob and its label (screws, hinges, nails by the pound);
    # tins of paint, cleaners and oils down the left wall with galvanised buckets on top; hand
    # tools hung on a pegboard down the right with brooms stood below; boards underfoot; the
    # counter across with a brass rule let into its top.
    if shop["id"] == "ironmonger":
        import random
        rnd = random.Random(31)
        box("boards", -W / 2, W / 2, 0, D, -0.019, 0.001, boards("boards_iron", (0.20, 0.13, 0.08), (0.15, 0.10, 0.06)))
        wood = mat("counter_wood", (0.15, 0.09, 0.05), rough=0.45, noise=0.25)
        drawer = mat("drawer_wood", (0.36, 0.22, 0.11), rough=0.5, noise=0.2)
        brass = mat("brass", (0.75, 0.55, 0.25), rough=0.3, metal=1.0)
        label = mat("drawer_label", (0.82, 0.79, 0.68), rough=0.8)
        shelfm = mat("shelf", (0.36, 0.25, 0.14), rough=0.6, noise=0.15)
        galv = mat("galvanised", (0.40, 0.41, 0.41), rough=0.55, metal=1.0, noise=0.4)
        # the drawers, across the back wall from 0.9 m to the ceiling, the back door kept clear
        for (x0, x1, z0) in ((-W / 2 + 0.05, 1.0, 0.9), (2.05, W / 2 - 0.05, 0.9), (1.0, 2.05, 2.05)):
            box("drawer_case", x0, x1, D - 0.4, D - 0.01, z0, H - 0.02, wood)
            if z0 < 1.0:
                box("drawer_base", x0, x1, D - 0.45, D - 0.01, 0.0, z0, wood)
            nx = max(1, int((x1 - x0 - 0.04) / 0.2))
            nz = max(1, int((H - 0.06 - z0) / 0.13))
            dw = (x1 - x0 - 0.04) / nx
            dh = (H - 0.06 - z0) / nz
            for i in range(nx):
                for j in range(nz):
                    dx0 = x0 + 0.02 + i * dw
                    dz0 = z0 + 0.02 + j * dh
                    box("drawer", dx0 + 0.006, dx0 + dw - 0.006, D - 0.415, D - 0.4, dz0 + 0.006, dz0 + dh - 0.006, drawer)
                    box("drawer_label", dx0 + dw * 0.3, dx0 + dw * 0.7, D - 0.418, D - 0.415, dz0 + dh * 0.55, dz0 + dh * 0.8, label)
                    cyl("drawer_knob", dx0 + dw / 2, D - 0.425, dz0 + dh * 0.32, 0.009, 0.02, brass, axis="y", verts=8)
        # down the left wall: paint in tins on the lower shelves, cleaners and oils above, buckets on top
        tins = [(0.70, 0.68, 0.62), (0.55, 0.08, 0.06), (0.10, 0.20, 0.42), (0.80, 0.70, 0.30), (0.20, 0.35, 0.20), (0.20, 0.20, 0.20)]
        tinlid = mat("tin_metal", (0.62, 0.62, 0.60), rough=0.35, metal=1.0)
        for k, z in enumerate((0.45, 0.85, 1.25, 1.65, 2.05)):
            box("left_shelf", -W / 2 + 0.02, -W / 2 + 0.42, 0.35, 2.4, z - 0.025, z, shelfm)
            if k == 0:
                for yu in (0.33, 1.36, 2.4):     # the unit's uprights, floor to the top shelf
                    box("left_upright", -W / 2 + 0.02, -W / 2 + 0.42, yu - 0.02, yu, 0.0, 2.07, shelfm)
            if k < 3:
                y = 0.42
                while y < 2.25:
                    c = rnd.choice(tins)
                    lab = mat("tin_%d_%d_%d" % tuple(int(v * 99) for v in c), c, rough=0.4)
                    r = rnd.choice((0.055, 0.075, 0.09))
                    for row in range(2 if r < 0.08 else 1):
                        paint_tin(bpy, -W / 2 + 0.32 - row * 0.17, y + r, z, r, r * 1.25, lab, tinlid)
                    y += 2 * r + 0.015
            elif k == 3:
                y = 0.42
                # oils and polish in tins (the scanned cleaner bottles' labels echo real products)
                pool = ["cleaner_tin_01", "oil_tin", "small_oil_can_01", "metal_jug", "pot_enamel_01"]
                while y < 2.2:
                    a = rnd.choice(pool)
                    sz = 0.22 if a in ("multi_cleaner_bottle", "bleach_bottle", "drain_cleaner", "all_purpose_cleaner") else 0.15
                    place(a, -W / 2 + 0.24, y + sz * 0.35, z, rot=(0.0, 0.0, math.pi / 2 + rnd.uniform(-0.3, 0.3)), size=sz, upright=True)
                    y += sz * 0.7 + 0.03
            else:
                y = 0.5
                while y < 2.15:
                    for j in range(rnd.randint(1, 2)):
                        bucket(bpy, "bucket", -W / 2 + 0.22, y + 0.15, z + j * 0.045, 0.1, 0.14, 0.22, galv)
                    y += 0.33
        # down the right wall: a pegboard of hand tools, hung flat, and brooms stood beneath
        box("pegboard", W / 2 - 0.015, W / 2, 0.35, 2.45, 0.95, 2.25, mat("pegboard", (0.30, 0.21, 0.13), rough=0.8, noise=0.3))
        tools = ["adjustable_wrench", "combination_wrench", "cross_pein_hammer", "wooden_hammer_01", "pliers",
                 "tongue_groove_pliers", "screwdriver", "flathead_screwdriver", "handsaw_wood", "hatchet",
                 "measuring_tape_01", "vintage_hand_drill", "trowel_01", "garden_gloves_01"]
        long_ones = {"handsaw_wood": 0.55, "hatchet": 0.38, "vintage_hand_drill": 0.34, "cross_pein_hammer": 0.3, "wooden_hammer_01": 0.3}
        # CRAMMED, as an ironmonger's board was (the first render hung a dozen tools on it)
        for zrow in (1.0, 1.28, 1.56, 1.84):
            y = 0.4 + rnd.uniform(0.0, 0.06)
            while True:
                a = rnd.choice(tools)
                sz = long_ones.get(a, 0.22)
                if y + sz > 2.42:
                    break
                place(a, W / 2 - 0.04, y + sz / 2, zrow, rot=(0.0, math.pi / 2, rnd.uniform(-0.25, 0.25)), size=sz)
                y += sz + 0.015
        for k, (a, y) in enumerate((("plastic_broom", 0.55), ("wooden_broom", 0.75), ("plastic_broom", 0.95), ("wooden_broom", 1.15))):
            place(a, W / 2 - 0.12, y, 0.0, rot=(0.0, 0.0, rnd.uniform(-0.2, 0.2)), size=1.25, upright=True)
        for k, y in enumerate((1.5, 1.85, 2.2)):
            bucket(bpy, "floor_bucket", W / 2 - 0.22, y, 0.0, 0.12, 0.16, 0.27, galv)
        place("watering_can_metal_01", W / 2 - 0.25, 1.5, 0.27, rot=(0.0, 0.0, math.pi / 2), size=0.4)
        # the counter across, a brass rule let into its top, the till, a toolbox on it
        cy0, cy1 = D - 1.2, D - 0.72     # near the back wall, where a projected room holds (3 October)
        box("counter", -W / 2 + 0.45, 1.3, cy0, cy1, 0.0, 0.92, wood)
        box("counter_top", -W / 2 + 0.43, 1.32, cy0 - 0.02, cy1 + 0.02, 0.92, 0.95, mat("counter_top_iron", (0.30, 0.20, 0.11), rough=0.35, noise=0.2))
        boarded(-W / 2 + 0.45, 1.3, cy0, wood)
        box("brass_rule", -1.8, -0.3, cy0 + 0.02, cy0 + 0.05, 0.95, 0.953, brass)
        model("CashRegister_01", 0.9, cy0 + 0.25, 0.95, turn=math.pi + 0.15, size=0.4)
        model("metal_toolbox", -0.9, cy0 + 0.25, 0.95, turn=0.1, size=0.45)
        ink = mat("ink", (0.05, 0.05, 0.08), rough=0.8)
        box("keys_card", -0.1, 0.6, cy0 - 0.03, cy0 - 0.025, 0.5, 0.7, mat("card_yellowed", (0.80, 0.72, 0.50), rough=0.85))
        text("keys_text", "KEYS CUT", 0.25, cy0 - 0.035, 0.6, 0.06, ink)
        text("keys_text2", "while you wait", 0.25, cy0 - 0.035, 0.53, 0.035, ink)
    # A TEA ROOM (V1, 3 October; west_north bay 2): small tables down both walls under red
    # gingham, wooden chairs at their ends, pictures above; across the back a counter with the
    # cakes under glass, a tea urn, cups and the till, the menu chalked on a blackboard behind;
    # the kitchen through the back door.
    if shop["id"] == "tea_room":
        import random
        rnd = random.Random(41)
        gm = bpy.data.materials.new("gingham")
        gm.use_nodes = True
        gnt = gm.node_tree
        gp = gnt.nodes["Principled BSDF"]
        gch = gnt.nodes.new("ShaderNodeTexChecker")
        gch.inputs["Scale"].default_value = 40.0
        gch.inputs["Color1"].default_value = (0.52, 0.06, 0.06, 1.0)
        gch.inputs["Color2"].default_value = (0.82, 0.80, 0.76, 1.0)
        ggeo = gnt.nodes.new("ShaderNodeNewGeometry")
        gnt.links.new(ggeo.outputs["Position"], gch.inputs["Vector"])
        gnt.links.new(gch.outputs["Color"], gp.inputs["Base Color"])
        gp.inputs["Roughness"].default_value = 0.85
        china = mat("china_white", (0.86, 0.85, 0.82), rough=0.2)
        steel = mat("steel", (0.62, 0.63, 0.64), rough=0.3, metal=1.0)
        glassm = mat("glass", (1.0, 1.0, 1.0), glass=True)
        wood = mat("counter_wood", (0.16, 0.09, 0.05), rough=0.45, noise=0.25)
        shelfm = mat("shelf", (0.30, 0.20, 0.11), rough=0.6, noise=0.1)
        for side in (-1, 1):
            for k, y in enumerate((0.6, 2.2)):
                xa, xb = (-W / 2 + 0.02, -W / 2 + 0.62) if side < 0 else (W / 2 - 0.62, W / 2 - 0.02)
                box("cloth_top", xa, xb, y, y + 0.7, 0.74, 0.755, gm)
                xo = xb if side < 0 else xa
                box("cloth_drop_side", xo - 0.004, xo + 0.004, y, y + 0.7, 0.57, 0.755, gm)
                box("cloth_drop_front", xa, xb, y - 0.004, y + 0.004, 0.57, 0.755, gm)
                box("cloth_drop_back", xa, xb, y + 0.696, y + 0.704, 0.57, 0.755, gm)
                cx, cyy = (xa + xb) / 2, y + 0.35
                cyl("table_leg", cx, cyy, 0.29, 0.03, 0.58, wood)
                cyl("table_foot", cx, cyy, 0.015, 0.2, 0.03, wood)
                # the cruet, the sugar, a little vase
                cyl("cruet_salt", cx - 0.05, cyy - 0.12, 0.79, 0.016, 0.07, china)
                cyl("cruet_pepper", cx - 0.01, cyy - 0.12, 0.79, 0.016, 0.07, mat("pepper", (0.15, 0.12, 0.10), rough=0.3))
                cyl("sugar_bowl", cx + 0.06, cyy - 0.1, 0.785, 0.04, 0.05, china)
                cyl("vase", cx, cyy + 0.18, 0.81, 0.02, 0.11, mat("vase_blue", (0.12, 0.20, 0.45), rough=0.2))
                for q in range(3):
                    bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=5, radius=0.018,
                                                         location=(cx + rnd.uniform(-0.02, 0.02), cyy + 0.18 + rnd.uniform(-0.02, 0.02), 0.88 + q * 0.012))
                    bpy.context.object.data.materials.append(mat("flower_%d" % q, [(0.70, 0.10, 0.15), (0.85, 0.70, 0.20), (0.80, 0.45, 0.55)][q], rough=0.6))
                if k == 0 and side < 0:
                    model("tea_set_01", cx, cyy + 0.02, 0.755, turn=0.4, size=0.32)
                # a plain painted chair at each end of the table (the carved one came out a throne)
                # one chair each, at the table's back end (the front chairs, near the glass and
                # out from the wall, smeared and warped in the projected room)
                for (yc, turn) in ((y + 0.92, 0.0),):
                    place("painted_wooden_chair_01", cx, yc, 0.0, rot=(0.0, 0.0, turn), size=0.85)
                # A PRINT OF THE HARBOUR above each table, framed and mounted: sky, sea, the far
                # shore and a boat (the scanned frames hung empty, or turned to the wall)
                wx = (-W / 2 + 0.012) if side < 0 else (W / 2 - 0.012)
                inward = -side

                def flat(name, y0, y1, z0, z1, m, depth):
                    xa_, xb_ = sorted((wx, wx + inward * depth))
                    box(name, xa_, xb_, cyy + y0, cyy + y1, z0, z1, m)
                frame_m = mat("frame_wood", (0.12, 0.07, 0.04), rough=0.4)
                flat("print_frame", -0.24, 0.24, 1.25, 1.62, frame_m, 0.02)
                flat("print_mount", -0.21, 0.21, 1.28, 1.59, mat("mount_cream", (0.80, 0.76, 0.64), rough=0.8), 0.022)
                # A REAL PHOTOGRAPH in each, a different harbour or pier (Poly Haven, CC0; the
                # second fresh review: "the same buoy picture hangs on every wall")
                photo = ["small_harbour_sunset", "gray_pier", "small_harbor_01", "bell_park_pier"][k + 2 * (side > 0)]
                pm = bpy.data.materials.new("print_" + photo)
                pm.use_nodes = True
                ptex = pm.node_tree.nodes.new("ShaderNodeTexImage")
                ptex.image = bpy.data.images.load(os.path.join(REPO, "production/assets/shop-displays/photos/%s.jpg" % photo))
                pm.node_tree.links.new(ptex.outputs["Color"], pm.node_tree.nodes["Principled BSDF"].inputs["Base Color"])
                pm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.6
                bpy.ops.mesh.primitive_plane_add(size=1.0, location=(wx + inward * 0.026, cyy, 1.435))
                pl = bpy.context.object
                pl.scale = (0.34, 0.26, 1.0)
                pl.rotation_euler = (math.pi / 2, 0.0, inward * math.pi / 2)
                pl.data.materials.append(pm)
        # THE COUNTER across the back, the cakes under glass, the urn, the cups, the till
        cy0, cy1 = D - 1.05, D - 0.5
        box("counter", -W / 2 + 0.25, 0.95, cy0, cy1, 0.0, 0.9, wood)
        box("counter_top", -W / 2 + 0.23, 0.97, cy0 - 0.02, cy1 + 0.02, 0.9, 0.93, mat("formica_cream", (0.72, 0.66, 0.52), rough=0.3, noise=0.1))
        boarded(-W / 2 + 0.25, 0.95, cy0, wood)
        box("cabinet_glass_front", -1.6, -0.2, cy0 + 0.03, cy0 + 0.04, 0.93, 1.3, glassm)
        box("cabinet_glass_top", -1.6, -0.2, cy0 + 0.03, cy1 - 0.03, 1.3, 1.31, glassm)
        for xx in (-1.6, -0.21):
            box("cabinet_end", xx, xx + 0.01, cy0 + 0.03, cy1 - 0.03, 0.93, 1.31, glassm)
        model("carrot_cake", -1.3, cy0 + 0.25, 0.935, size=0.24)
        model("strawberry_chocolate_cake", -0.85, cy0 + 0.25, 0.935, size=0.24)
        for q in range(4):
            model("croissant", -0.5 + (q % 2) * 0.1, cy0 + 0.17 + (q // 2) * 0.12, 0.935, turn=rnd.uniform(0, 3.0), size=0.11)
        cyl("urn", -2.05, cy0 + 0.27, 0.93 + 0.24, 0.15, 0.48, steel)
        cyl("urn_lid", -2.05, cy0 + 0.27, 1.43, 0.12, 0.04, steel)
        box("urn_tap", -2.08, -2.02, cy0 + 0.08, cy0 + 0.13, 1.0, 1.03, mat("tap_black", (0.03, 0.03, 0.03), rough=0.4))
        for q in range(6):
            cyl("cup_stack", 0.15 + (q % 3) * 0.1, cy0 + 0.15 + (q // 3) * 0.12, 0.93 + 0.06, 0.04, 0.12, china)
        model("CashRegister_01", 0.7, cy0 + 0.28, 0.93, turn=math.pi + 0.2, size=0.38)
        # behind it, on the back wall: shelves of teapots and cups, the blackboard menu, a clock
        for z in (1.55, 1.95):
            box("china_shelf", 0.0, 1.0, D - 0.22, D - 0.02, z - 0.02, z, shelfm)
            for q in range(5):
                cyl("plate", 0.1 + q * 0.2, D - 0.06, z + 0.11, 0.09, 0.012, china, axis="y")
        board = mat("blackboard", (0.04, 0.05, 0.05), rough=0.7, noise=0.3)
        chalk = mat("chalk", (0.82, 0.82, 0.78), rough=0.9)
        box("menu_board", -2.3, -0.3, D - 0.03, D - 0.01, 1.25, 2.25, board)
        box("menu_frame", -2.33, -0.27, D - 0.012, D - 0.002, 1.22, 2.28, wood)
        for q, (body, size) in enumerate((("TODAY", 0.075), ("Pot of Tea  45p", 0.05), ("Coffee  50p", 0.05),
                                          ("Toasted Teacake  55p", 0.05), ("Scone, Jam & Cream  80p", 0.05),
                                          ("Beans on Toast  95p", 0.05), ("Soup of the Day  £1.10", 0.05),
                                          ("Home-made Cakes from 45p", 0.05))):
            text("menu_%d" % q, body, -1.3, D - 0.035, 2.12 - q * 0.105 - (0.02 if q else 0.0), size, chalk)
        model("wall_clock", 0.5, D - 0.05, 2.2, size=0.3)
    # A SHIP'S CHANDLER (V1, 3 October; east_chandler bay 0): ropes in hanks on pegs down the
    # left wall and in flat coils on the floor beneath; life jackets, a lifebuoy and oilskin hats
    # down the right with boots below; a buoy and a sea marker in the back corner; the back wall
    # shelves of marine paint, lamps and oils; the counter across with a brass lamp and a
    # compass on it; boards underfoot.
    if shop["id"] == "chandler":
        import random
        rnd = random.Random(51)
        box("boards", -W / 2, W / 2, 0, D, -0.019, 0.001, boards("boards_chandler", (0.17, 0.11, 0.07), (0.13, 0.09, 0.05)))
        ropes = [mat("rope_manila", (0.55, 0.42, 0.25), rough=0.9, noise=0.4), mat("rope_white", (0.78, 0.77, 0.72), rough=0.85, noise=0.3),
                 mat("rope_blue", (0.08, 0.18, 0.45), rough=0.8, noise=0.3), mat("rope_orange", (0.80, 0.35, 0.06), rough=0.8, noise=0.3),
                 mat("rope_green", (0.12, 0.30, 0.15), rough=0.8, noise=0.3)]
        pegm = mat("peg_wood", (0.30, 0.20, 0.11), rough=0.6)
        shelfm = mat("shelf", (0.32, 0.22, 0.12), rough=0.6, noise=0.15)
        wood = mat("counter_wood", (0.14, 0.08, 0.04), rough=0.45, noise=0.25)
        for zrow in (2.2, 1.5):
            y = 0.5
            while True:
                r = rnd.uniform(0.14, 0.21)
                if y + 2 * r > 2.4:
                    break
                cyl("peg", -W / 2 + 0.06, y + r, zrow, 0.015, 0.12, pegm, axis="x", verts=8)
                # natural and dark hanks only, close to the wall (white ones read as floating plates)
                rope_hank(bpy, "hank", -W / 2 + 0.03, y + r, zrow + 0.012, r, rnd.randint(5, 7), rnd.uniform(0.011, 0.016),
                          rnd.choice([ropes[0], ropes[2], ropes[4]]), rnd)
                y += 2 * r + 0.07
        y = 0.5
        while True:
            r = rnd.uniform(0.17, 0.25)
            if y + 2 * r > 2.4:
                break
            rope_coil(bpy, sc, "coil", -W / 2 + 0.3, y + r, 0.0, 0.05, r, rnd.randint(2, 4), rnd.uniform(0.009, 0.013), rnd.choice(ropes))
            y += 2 * r + 0.05
        # down the right wall: life jackets hung, the lifebuoy, oilskin hats on a shelf, boots below
        box("hat_shelf", W / 2 - 0.3, W / 2, 0.4, 2.0, 1.9, 1.925, shelfm)
        for k, y in enumerate((0.75, 1.3)):
            place("life_jacket", W / 2 - 0.1, y, 0.95, rot=(0.0, 0.0, -math.pi / 2), size=0.62)
        place("lifebuoy", W / 2 - 0.06, 1.9, 1.0, rot=(0.0, math.pi / 2, 0.0), size=0.62)
        # lamps and torches on the shelf (the scanned "fisherman's hat" is a bush hat, not a
        # sou'wester: the fresh review, 3 October)
        for k, (a, y) in enumerate((("Lantern_01", 0.6), ("signal_flashlight", 0.95), ("Lantern_01", 1.3), ("vintage_flashlight", 1.65))):
            place(a, W / 2 - 0.15, y, 1.925, rot=(0.0, 0.0, rnd.uniform(-0.4, 0.4)), size=0.3 if a == "Lantern_01" else 0.2,
                  upright=a != "Lantern_01")
        # (no boots on the floor: twenty centimetres out from the wall they streaked across the
        # projected floor, the second fresh review; the window shows a pair)
        # (no buoy or sea marker standing in the back corner: a metre from the walls they smeared
        # into ghosts in the projected room, the fresh review, 3 October)
        # the back wall's shelves, the door kept clear: marine paint, lamps, oil, boxes of stock
        tins = [(0.72, 0.70, 0.64), (0.10, 0.16, 0.36), (0.55, 0.08, 0.06), (0.12, 0.26, 0.16), (0.80, 0.62, 0.15)]
        tinlid = mat("tin_metal", (0.62, 0.62, 0.60), rough=0.35, metal=1.0)
        for k, z in enumerate((0.5, 0.95, 1.4, 1.85, 2.25)):
            box("back_shelf", -W / 2 + 0.05, 1.0, D - 0.4, D - 0.02, z - 0.025, z, shelfm)
            x = -W / 2 + 0.12
            while x < 0.9:
                roll = rnd.random()
                if k in (0, 1):
                    c = rnd.choice(tins)
                    r = rnd.choice((0.06, 0.08))
                    paint_tin(bpy, x + r, D - 0.2, z, r, r * 1.3, mat("tin_%d_%d_%d" % tuple(int(v * 99) for v in c), c, rough=0.4), tinlid)
                    x += 2 * r + 0.02
                elif k == 4:
                    model("cardboard_box_01", x + 0.17, D - 0.22, z, turn=rnd.uniform(-0.2, 0.2), size=rnd.uniform(0.28, 0.34))
                    x += 0.38
                else:
                    a = rnd.choice(["Lantern_01", "signal_flashlight", "small_oil_can_01", "vintage_flashlight", "oil_tin", "seadogs_compass"])
                    sz = {"Lantern_01": 0.34, "signal_flashlight": 0.22, "small_oil_can_01": 0.2, "vintage_flashlight": 0.2, "oil_tin": 0.2, "seadogs_compass": 0.14}[a]
                    place(a, x + sz / 2, D - 0.2, z, rot=(0.0, 0.0, rnd.uniform(-0.4, 0.4)), size=sz, upright=a in ("signal_flashlight", "vintage_flashlight"))
                    x += sz + 0.05
        place("metal_jerrycan", 0.6, D - 0.25, 0.0, rot=(0.0, 0.0, 0.1), size=0.45)
        # crates of stock in the back corner (the scanned drum carried an explosives sign)
        place("wooden_crate_01", -W / 2 + 0.4, D - 0.8, 0.0, rot=(0.0, 0.0, 0.1), size=0.6)
        place("wooden_crate_01", -W / 2 + 0.42, D - 0.8, 0.55, rot=(0.0, 0.0, -0.15), size=0.5)
        # the counter across, a brass lamp, the compass and the till on it
        cy0, cy1 = D - 1.2, D - 0.72     # near the back wall, where a projected room holds (3 October)
        box("counter", -W / 2 + 0.7, 1.3, cy0, cy1, 0.0, 0.92, wood)
        box("counter_top", -W / 2 + 0.68, 1.32, cy0 - 0.02, cy1 + 0.02, 0.92, 0.95, mat("counter_top_ch", (0.28, 0.17, 0.09), rough=0.3, noise=0.2))
        boarded(-W / 2 + 0.7, 1.3, cy0, wood)
        place("Lantern_01", -1.4, cy0 + 0.25, 0.95, size=0.36)
        place("seadogs_compass", -0.7, cy0 + 0.22, 0.95, size=0.16)
        model("CashRegister_01", 0.85, cy0 + 0.25, 0.95, turn=math.pi + 0.15, size=0.4)
    # A GROCER (V1, 3 October): shelves of tins and packets down both walls and the back,
    # a counter with scales and a till, a dairy fridge, sacks of potatoes.
    if shop["id"] == "grocer":
        import random
        rnd = random.Random(9)
        shelfm = mat("shelf", (0.40, 0.30, 0.18), rough=0.6, noise=0.2)
        # PRINTED STOCK (3 October: plain colour blocks read as toy bricks to three fresh
        # reviews): tins and packets carrying the made-up labels of one sheet
        # (tools/art-recipes/make_label_atlas.py), runs of one product as a grocer stacks them
        lab = label_material(bpy, mats)
        tinm = mat("tin_metal", (0.62, 0.62, 0.60), rough=0.35, metal=1.0)
        _sheet, tiles = label_sheet()
        tins = [t_ for t_ in tiles if t_["kind"] in ("tin", "jar")]
        packets = [t_ for t_ in tiles if t_["kind"] in ("packet", "bottle")]

        def stock(x0, x1, y0, y1, along_x, facing):
            # a shelving unit, not planks in the air: a back board and an upright every metre
            if along_x:
                box("unit_back", x0, x1, y1 - 0.015, y1, 0.0, 1.9, shelfm)
                xs = [x0 + k * (x1 - x0) / max(1, round((x1 - x0) / 1.0)) for k in range(int(round((x1 - x0) / 1.0)) + 1)]
                for xu in xs:
                    box("unit_upright", xu - 0.012, xu + 0.012, y0, y1, 0.0, 1.9, shelfm)
            else:
                xb = x0 if x0 < 0 else x1 - 0.015
                box("unit_back", xb, xb + 0.015, y0, y1, 0.0, 1.9, shelfm)
                ys = [y0 + k * (y1 - y0) / max(1, round((y1 - y0) / 1.0)) for k in range(int(round((y1 - y0) / 1.0)) + 1)]
                for yu in ys:
                    box("unit_upright", x0, x1, yu - 0.012, yu + 0.012, 0.0, 1.9, shelfm)
            for tier, z in enumerate((0.45, 0.85, 1.25, 1.65)):
                box("shelf", x0, x1, y0, y1, z, z + 0.02, shelfm)
                a, b = (x0, x1) if along_x else (y0, y1)
                t = a + 0.04
                run_left, kind, tile = 0, None, None
                while t < b - 0.06:
                    if run_left <= 0:
                        kind = "tin" if rnd.random() < 0.55 else "packet"
                        tile = rnd.choice(tins if kind == "tin" else packets)
                        run_left = rnd.randint(3, 7)
                    run_left -= 1
                    if kind == "tin":
                        r = 0.037 if tile["kind"] == "tin" else 0.04
                        h = 0.11 if tile["kind"] == "tin" else 0.13
                        cx, cy = ((t + r, (y0 + y1) / 2) if along_x else ((x0 + x1) / 2, t + r))
                        labelled_tin(bpy, cx, cy, z + 0.02, r, h, tile["uv"], lab, tinm, facing)
                        t += 2 * r + 0.006
                    else:
                        w, h, dpt = (0.075, 0.19, 0.05) if tile["kind"] == "packet" else (0.06, 0.22, 0.06)
                        if along_x:
                            labelled_packet(bpy, t, t + w, y1 - 0.04 - dpt, y1 - 0.04, z + 0.02, z + 0.02 + h, tile["uv"], lab, facing)
                        else:
                            mid = (x0 + x1) / 2
                            labelled_packet(bpy, mid - dpt / 2, mid + dpt / 2, t, t + w, z + 0.02, z + 0.02 + h, tile["uv"], lab, facing)
                        t += w + 0.006
        stock(-W / 2 + 0.3, W / 2 - 0.3, D - 0.35, D - 0.02, True, -90.0)
        stock(-W / 2, -W / 2 + 0.35, 1.2, D - 0.4, False, 0.0)
        stock(W / 2 - 0.35, W / 2, 1.2, D - 1.4, False, 180.0)
        counter = mat("counter_wood", (0.32, 0.20, 0.11), rough=0.45, noise=0.2)
        # the counter near the back, where a projected room holds (3 October: 2.0 m back it
        # smeared into a slab across the floor from the pavement's angle)
        gy = D - 1.25 - 2.0
        box("counter", -0.4, 1.6, 2.0 + gy, 2.55 + gy, 0.0, 0.9, counter)
        boarded(-0.4, 1.6, 2.0 + gy, counter)
        box("counter_top", -0.42, 1.62, 1.98 + gy, 2.57 + gy, 0.9, 0.93, mat("counter_top", (0.55, 0.52, 0.45), rough=0.35))
        steel = mat("steel", (0.62, 0.63, 0.64), rough=0.3, metal=1.0)
        box("scale", 0.0, 0.3, 2.1 + gy, 2.4 + gy, 0.93, 1.0, steel)
        # (no white scale head: it read as a blank board on the counter)
        model("CashRegister_01", 1.25, 2.3 + gy, 0.93, turn=math.pi + 0.15, size=0.4)
        box("fridge", W / 2 - 0.9, W / 2 - 0.1, D - 1.3, D - 0.5, 0.0, 1.8, mat("fridge_white", (0.78, 0.78, 0.75), rough=0.3))
        box("fridge_glass", W / 2 - 0.9, W / 2 - 0.88, D - 1.28, D - 0.52, 0.2, 1.7, mat("fridge_dark", (0.08, 0.10, 0.12), rough=0.05))
        # behind its glass, milk in pint bottles with their foil tops, butter and cheese
        # (3 October: a blank white box to the second fresh review)
        milk = mat("milk", (0.86, 0.86, 0.84), rough=0.25)
        foil = [mat("foil_silver", (0.7, 0.7, 0.72), rough=0.3, metal=1.0), mat("foil_gold", (0.75, 0.55, 0.2), rough=0.3, metal=1.0),
                mat("foil_red", (0.6, 0.08, 0.06), rough=0.3, metal=1.0)]
        fx = W / 2 - 0.85
        for k, zf in enumerate((0.25, 0.65, 1.05, 1.45)):
            box("fridge_shelf", fx, W / 2 - 0.12, D - 1.27, D - 0.53, zf - 0.01, zf, mat("fridge_rack", (0.55, 0.56, 0.57), rough=0.3, metal=1.0))
            yb = D - 1.22
            while yb < D - 0.6:
                if k < 2:
                    cyl("milk_bottle", fx + 0.1, yb, zf + 0.1, 0.032, 0.2, milk)
                    cyl("milk_top", fx + 0.1, yb, zf + 0.2, 0.022, 0.006, foil[(int(yb * 10) + k) % 3])
                    yb += 0.075
                else:
                    box("butter", fx + 0.05, fx + 0.17, yb, yb + 0.08, zf, zf + 0.05, mat("butter_gold", (0.78, 0.62, 0.22), rough=0.4))
                    yb += 0.1
        # a crate of potatoes on the floor (the sacks came out as faceted eggs)
        crate = mat("crate_wood", (0.45, 0.34, 0.20), rough=0.8, noise=0.2)
        box("veg_crate", -W / 2 + 0.05, -W / 2 + 0.75, 0.45, 0.95, 0.0, 0.3, crate)     # against the wall
        spud = mat("potato", (0.50, 0.38, 0.22), rough=0.8)
        for j in range(40):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=rnd.uniform(0.03, 0.045),
                                                 location=(rnd.uniform(-W / 2 + 0.1, -W / 2 + 0.7), rnd.uniform(0.5, 0.9), 0.32))
            bpy.ops.object.shade_smooth()
            bpy.context.object.data.materials.append(spud)
    # A LAUNDERETTE (the Steam Laundry; V1, 3 October): front-loading washers down the left
    # wall, dryers stacked two high down the right, a wooden bench and plastic chairs, a
    # folding table, a notice board, a change machine; lino and tubes, bright, a little worn.
    if shop["id"] == "launderette":
        enamel = mat("machine_white", (0.74, 0.74, 0.71), rough=0.3, noise=0.15)
        steel = mat("steel", (0.62, 0.63, 0.64), rough=0.3, metal=1.0)
        port = mat("porthole", (0.04, 0.05, 0.06), rough=0.05)
        rim = mat("door_rim", (0.55, 0.56, 0.57), rough=0.25, metal=1.0)
        y = 0.9
        while y < D - 0.6:
            box("washer", -W / 2 + 0.02, -W / 2 + 0.62, y, y + 0.6, 0.0, 0.85, enamel)
            cyl("washer_rim", -W / 2 + 0.625, y + 0.3, 0.5, 0.17, 0.02, rim, axis="x")
            cyl("washer_door", -W / 2 + 0.63, y + 0.3, 0.5, 0.14, 0.02, port, axis="x")
            box("washer_panel", -W / 2 + 0.6, -W / 2 + 0.625, y + 0.05, y + 0.55, 0.72, 0.82, steel)
            y += 0.64
        y = 0.9
        while y < D - 0.6:
            for z0 in (0.0, 0.82):
                # enamelled cases with a steel front (3 October: all-steel, the stack's end read
                # as a black slab in the game at night)
                # built into the wall, 0.45 deep (at 0.68 the stack smeared into slabs, the review)
                box("dryer", W / 2 - 0.45, W / 2 - 0.02, y, y + 0.7, z0, z0 + 0.8, enamel)
                box("dryer_front", W / 2 - 0.47, W / 2 - 0.45, y + 0.02, y + 0.68, z0 + 0.04, z0 + 0.78, steel)
                cyl("dryer_door", W / 2 - 0.475, y + 0.35, z0 + 0.42, 0.25, 0.02, port, axis="x")
                # its coin panel: two slots and a dial (flat panels with discs, the review)
                box("dryer_panel", W / 2 - 0.48, W / 2 - 0.47, y + 0.08, y + 0.62, z0 + 0.69, z0 + 0.77, mat("panel_grey", (0.30, 0.31, 0.32), rough=0.4))
                for k, yy in enumerate((y + 0.16, y + 0.26)):
                    box("coin_slot", W / 2 - 0.485, W / 2 - 0.48, yy, yy + 0.05, z0 + 0.72, z0 + 0.74, mat("slot_black", (0.02, 0.02, 0.02), rough=0.5))
                cyl("dryer_dial", W / 2 - 0.49, y + 0.5, z0 + 0.73, 0.025, 0.02, mat("dial_chrome", (0.8, 0.8, 0.82), rough=0.2, metal=1.0), axis="x")
            y += 0.74
        # THE SEATING AGAINST THE BACK WALL (3 October: a bench and chairs in the middle of the
        # floor smeared in the projected room, and the chairs were flat cards): moulded plastic
        # chairs in a row under the notice board, the folding table beside them
        for k, x in enumerate((-2.3, -1.8, -1.3)):
            place("plastic_monobloc_chair_01", x, D - 0.32, 0.0, rot=(0.0, 0.0, math.pi), size=0.8)
        # a folding table on its legs, a laundry bag and a box of powder on it (a bare box before)
        formica = mat("formica", (0.62, 0.55, 0.42), rough=0.35, noise=0.15)
        box("folding_table_top", -0.95, 0.35, D - 0.62, D - 0.05, 0.82, 0.85, formica)
        for lx in (-0.9, 0.3):
            for ly in (D - 0.57, D - 0.1):
                box("folding_table_leg", lx - 0.02, lx + 0.02, ly - 0.02, ly + 0.02, 0.0, 0.82, steel)
        box("laundry_bag", -0.75, -0.35, D - 0.5, D - 0.2, 0.85, 1.12, mat("bag_blue", (0.12, 0.20, 0.42), rough=0.85, noise=0.4))
        box("powder_box", 0.0, 0.18, D - 0.4, D - 0.3, 0.85, 1.1, mat("powder_red", (0.60, 0.08, 0.06), rough=0.5))
        box("notice_board", -2.5, -0.95, D - 0.02, D, 1.15, 1.9, mat("cork", (0.45, 0.32, 0.18), rough=0.9, noise=0.3))
        biro = mat("biro", (0.06, 0.08, 0.30), rough=0.8)
        notices = [("SERVICE WASH", "£2.50 a load"), ("ROOM TO LET", "ask within"), ("IRONING DONE", "ring 2846"),
                   ("NO DYEING", "in the machines"), ("LOST: KEYS", "on a red ring"), ("DRY CLEANING", "taken in"),
                   ("SETTEE £40", "ring 4417"), ("PLEASE DO NOT", "overload"), ("WINDOW CLEANER", "ring 6631")]
        for k, (a, b) in enumerate(notices):
            cx0 = -2.42 + (k % 3) * 0.5
            cz0 = 1.22 + (k // 3) * 0.22
            box("notice_card", cx0, cx0 + 0.36, D - 0.025, D - 0.02, cz0, cz0 + 0.17,
                mat("card_%d" % (k % 3), [(0.85, 0.84, 0.78), (0.82, 0.78, 0.45), (0.65, 0.78, 0.85)][k % 3], rough=0.85))
            text("notice_a", a, cx0 + 0.18, D - 0.027, cz0 + 0.1, 0.035, biro)
            text("notice_b", b, cx0 + 0.18, D - 0.027, cz0 + 0.045, 0.028, biro)
        # the change machine, its front lettered, its slot and its tray
        box("change_machine", 0.55, 0.98, D - 0.3, D - 0.02, 0.9, 1.6, mat("change_grey", (0.40, 0.42, 0.44), rough=0.4))
        box("change_front", 0.58, 0.95, D - 0.305, D - 0.3, 1.25, 1.55, mat("change_panel", (0.75, 0.70, 0.30), rough=0.4))
        text("change_word", "CHANGE", 0.765, D - 0.307, 1.44, 0.06, mat("change_ink", (0.05, 0.05, 0.05), rough=0.6))
        text("change_coins", "10p 20p 50p", 0.765, D - 0.307, 1.31, 0.035, mat("change_ink", (0.05, 0.05, 0.05), rough=0.6))
        box("change_slot", 0.72, 0.81, D - 0.305, D - 0.3, 1.12, 1.135, mat("slot_black", (0.02, 0.02, 0.02), rough=0.5))
        box("change_tray", 0.68, 0.85, D - 0.36, D - 0.3, 0.95, 1.0, steel)
        # the prices on a board, with their pound sign (floating letters on bare wall before)
        box("price_board", -0.95, 0.95, D - 0.03, D - 0.01, 1.95, 2.25, mat("board_white", (0.85, 0.84, 0.80), rough=0.6))
        text("price_sign", "WASH £1.20   DRY 20p", 0.0, D - 0.035, 2.05, 0.11, mat("sign_red", (0.6, 0.06, 0.04), rough=0.6))
        # and the room lived in: a clock over the door, powder and a basket on the washers
        model("wall_clock", 1.5, D - 0.05, 2.25, size=0.28)
        for k, yy in enumerate((1.2, 2.5)):
            box("washer_powder", -W / 2 + 0.15, -W / 2 + 0.33, yy, yy + 0.1, 0.85, 1.1, mat("powder_blue", (0.08, 0.22, 0.55), rough=0.5))
        model("wicker_basket_02", -W / 2 + 0.33, 3.2, 0.85, turn=0.4, size=0.42)
    # AN EMPTY UNIT, TO LET (V1, 3 October): stripped out, bare boards, the plaster scarred
    # where the fittings came off, a stepladder, a dust sheet, a bare bulb, the old counter's
    # outline on the floor; the window half whitewashed, as empty shops' were.
    if shop["id"] == "to_let":
        bm = bpy.data.materials.new("bare_boards")
        bm.use_nodes = True
        bnt = bm.node_tree
        bp = bnt.nodes["Principled BSDF"]
        bbr = bnt.nodes.new("ShaderNodeTexBrick")
        bbr.inputs["Scale"].default_value = 1.0
        bbr.inputs["Mortar Size"].default_value = 0.004
        bbr.inputs["Brick Width"].default_value = 2.4
        bbr.inputs["Row Height"].default_value = 0.15
        bbr.inputs["Color1"].default_value = (0.20, 0.13, 0.08, 1.0)
        bbr.inputs["Color2"].default_value = (0.15, 0.10, 0.06, 1.0)
        bbr.inputs["Mortar"].default_value = (0.04, 0.03, 0.02, 1.0)
        bgeo = bnt.nodes.new("ShaderNodeNewGeometry")
        bnt.links.new(bgeo.outputs["Position"], bbr.inputs["Vector"])
        bnt.links.new(bbr.outputs["Color"], bp.inputs["Base Color"])
        bp.inputs["Roughness"].default_value = 0.85
        box("boards", -W / 2, W / 2, 0, D, -0.019, 0.001, bm)
        scar = mat("plaster_scar", (0.20, 0.17, 0.13), rough=0.9, noise=0.4)
        for k, (x0, x1, z0, z1) in enumerate(((-2.2, -0.6, 1.2, 1.9), (0.4, 1.9, 0.9, 1.6), (-1.0, 0.3, 0.0, 1.0))):
            box("scar_%d" % k, x0, x1, D - 0.012, D - 0.008, z0, z1, scar)
        for k in range(5):
            box("shelf_ghost_%d" % k, -W / 2 + 0.02, -W / 2 + 0.03, 0.8 + k * 0.5, 1.3 + k * 0.5, 1.2, 1.205, scar)
        # a stepladder leaning on the back wall, paint-spattered
        ladder = mat("ladder_wood", (0.36, 0.27, 0.17), rough=0.7, noise=0.3)
        lx = 1.3
        for sgn in (-1, 1):
            leg = box("ladder_leg", lx + sgn * 0.2 - 0.02, lx + sgn * 0.2 + 0.02, D - 0.62, D - 0.58, 0.0, 2.0, ladder)
            leg.rotation_euler = (-0.28, 0.0, 0.0)
            leg.location = (leg.location.x, D - 0.33, 0.97)
        for k in range(6):
            yk = D - 0.62 + k * 0.095
            box("ladder_step", lx - 0.2, lx + 0.2, yk, yk + 0.08, 0.28 + k * 0.3, 0.30 + k * 0.3, ladder)
        # a dust sheet in a heap: a lumpy draped shape, not a ball
        sheet = mat("dust_sheet", (0.48, 0.45, 0.39), rough=0.95, noise=0.3)
        bpy.ops.mesh.primitive_plane_add(size=1.0, location=(-1.3, 3.1, 0.0))
        heap = bpy.context.object
        heap.scale = (1.2, 0.9, 1.0)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        sub = heap.modifiers.new("fine", "SUBSURF")
        sub.subdivision_type = "SIMPLE"
        sub.levels = 5
        ht = bpy.data.textures.new("folds", "CLOUDS")
        ht.noise_scale = 0.18
        dsp = heap.modifiers.new("folds", "DISPLACE")
        dsp.texture = ht
        dsp.strength = 0.35
        dsp.mid_level = 0.25
        bpy.context.view_layer.objects.active = heap
        for md in list(heap.modifiers):
            bpy.ops.object.modifier_apply(modifier=md.name)
        for v in heap.data.vertices:
            v.co.z = max(0.0, v.co.z) * (1.0 - min(1.0, ((v.co.x / 0.6) ** 2 + (v.co.y / 0.45) ** 2)))
        heap.data.materials.append(sheet)
        cyl("flex", 0.0, 2.0, H - 0.25, 0.006, 0.5, mat("flex", (0.05, 0.05, 0.05), rough=0.6))
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, location=(0.0, 2.0, H - 0.53))
        bulb = bpy.context.object
        bulb.scale = (0.03, 0.03, 0.045)
        bulb.data.materials.append(mat("bulb", (0.95, 0.9, 0.75), rough=0.3))
        box("counter_ghost", -W / 2 + 0.4, W / 2 - 1.0, 2.6, 2.62, 0.0, 0.003, mat("floor_mark", (0.18, 0.13, 0.08), rough=0.9))
    # THE TRADE, A FISHMONGER (V1, 3 October; FISHMONGER-2026-10-03.md and t13140): a white
    # refrigerated serve-over counter across the room with fish in white trays, a scale on
    # it, a steel rail overhead, shelves of tins and jars high on the back wall, a clock,
    # and the back room's door.
    if shop["id"] == "fishmonger":
        white = mat("counter_white", (0.68, 0.68, 0.65), rough=0.35, noise=0.3)
        steel = mat("steel", (0.62, 0.63, 0.64), rough=0.3, metal=1.0)
        glassm = mat("glass", (1.0, 1.0, 1.0), glass=True)
        trayw = mat("tray_white", (0.86, 0.86, 0.84), rough=0.4)
        fish_grey = mat("fish_grey", (0.38, 0.38, 0.36), rough=0.25)
        fish_gold = mat("fish_smoked", (0.78, 0.55, 0.18), rough=0.4)
        crab = mat("crab", (0.55, 0.22, 0.08), rough=0.45)
        tin_cols = [(0.38, 0.10, 0.07), (0.10, 0.18, 0.30), (0.45, 0.38, 0.12), (0.14, 0.26, 0.12), (0.55, 0.53, 0.48)]
        import random
        rnd = random.Random(5)
        cy0, cy1 = 2.0, 2.75
        box("counter_body", -W / 2 + 0.25, W / 2 - 0.9, cy0, cy1, 0, 0.85, white)
        # its front: a steel kick plate, a grille to the cooling, and panel joints
        box("kick_plate", -W / 2 + 0.25, W / 2 - 0.9, cy0 - 0.01, cy0, 0.0, 0.16, steel)
        # THE CHILLER'S GRILLE as steel louvres (3 October: a black panel here, mid-room, smeared
        # across the floor in the game as a black slab)
        for k in range(5):
            box("grille_louvre", -W / 2 + 0.6, -W / 2 + 1.4, cy0 - 0.012, cy0, 0.22 + k * 0.032, 0.235 + k * 0.032, steel)
        for k in range(1, 4):
            xj = -W / 2 + 0.25 + k * (W - 1.15) / 4.0
            box("joint", xj - 0.004, xj + 0.004, cy0 - 0.008, cy0, 0.16, 0.85, mat("joint", (0.35, 0.35, 0.33), rough=0.5))
        box("counter_well", -W / 2 + 0.3, W / 2 - 0.95, cy0 + 0.05, cy1 - 0.25, 0.85, 0.9, steel)
        box("counter_glass", -W / 2 + 0.25, W / 2 - 0.9, cy0 - 0.005, cy0, 0.85, 1.25, glassm)
        x = -W / 2 + 0.4
        while x < W / 2 - 1.05:
            box("tray", x - 0.14, x + 0.14, cy0 + 0.08, cy0 + 0.42, 0.9, 0.93, trayw)
            m = rnd.choice([fish_grey, fish_gold, crab])
            for k in range(3):
                bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6,
                                                     location=(x - 0.08 + k * 0.08, cy0 + 0.25, 0.945))
                o = bpy.context.object
                o.scale = (0.035, 0.12, 0.02)
                o.data.materials.append(m)
            x += 0.32
        box("scale_base", W / 2 - 1.3, W / 2 - 1.0, cy0 + 0.45, cy0 + 0.7, 0.85, 0.95, white)
        box("scale_pan", W / 2 - 1.32, W / 2 - 0.98, cy0 + 0.42, cy0 + 0.72, 0.97, 0.98, steel)
        box("scale_head", W / 2 - 1.22, W / 2 - 1.08, cy0 + 0.6, cy0 + 0.68, 0.95, 1.25, white)
        box("rail", -W / 2 + 0.2, W / 2 - 0.2, D - 0.6, D - 0.56, H - 0.35, H - 0.32, steel)
        for k in range(6):
            box("hook", -W / 2 + 0.5 + k * 0.7, -W / 2 + 0.51 + k * 0.7, D - 0.6, D - 0.59, H - 0.5, H - 0.35, steel)
        shelfm = mat("shelf", (0.75, 0.75, 0.72), rough=0.6)
        for tier, z in enumerate((1.55, 1.85)):
            box("shelf_%d" % tier, -W / 2 + 0.1, W / 2 - 0.1, D - 0.3, D - 0.02, z, z + 0.02, shelfm)
            x = -W / 2 + 0.15
            while x < W / 2 - 0.2:
                c = rnd.choice(tin_cols)
                cyl("tin", x, D - 0.16, z + 0.075, 0.035, 0.11, mat("tin_%d_%d_%d" % tuple(int(v * 99) for v in c), c, rough=0.5))
                x += 0.08 + rnd.random() * 0.03
        # THE WORKING SIDE: a chopping block with knives, a bucket, wrapping paper, a till,
        # and the price board above the shelves (the first pass: "a spotless showroom").
        block = mat("block_wood", (0.45, 0.32, 0.20), rough=0.7, noise=0.25)
        box("chop_block", W / 2 - 0.85, W / 2 - 0.35, cy1 + 0.25, cy1 + 0.75, 0, 0.82, block)
        for k in range(3):
            box("knife", W / 2 - 0.8 + k * 0.12, W / 2 - 0.78 + k * 0.12, cy1 + 0.3, cy1 + 0.6, 0.82, 0.83, steel)
        cyl("bucket", -W / 2 + 0.35, cy1 + 0.4, 0.17, 0.15, 0.34, mat("bucket_white", (0.8, 0.8, 0.78), rough=0.4))
        cyl("paper_roll", -W / 2 + 0.9, cy0 + 0.6, 0.97, 0.06, 0.5, mat("paper", (0.85, 0.82, 0.74), rough=0.9), axis="x")
        box("till", W / 2 - 1.75, W / 2 - 1.45, cy0 + 0.45, cy0 + 0.7, 0.85, 1.05, mat("till_grey", (0.28, 0.27, 0.25), rough=0.5))
        board = mat("price_board", (0.05, 0.06, 0.05), rough=0.8)
        box("price_board", -1.1, 1.1, D - 0.04, D - 0.02, 2.06, 2.38, board)
        chalk = mat("chalk", (0.85, 0.85, 0.80), rough=0.9)
        for k, line in enumerate(("COD 1.80   HADDOCK 1.90   PLAICE 2.20", "KIPPERS 1.20   SMOKED HADDOCK 2.40")):
            text("board_%d" % k, line, 0.0, D - 0.045, 2.28 - k * 0.11, 0.07, chalk)
        cyl("clock_face", 1.7, D - 0.03, 2.15, 0.13, 0.02, mat("clock_face", (0.9, 0.9, 0.86), rough=0.4), axis="y")
        cyl("clock_rim", 1.7, D - 0.025, 2.15, 0.14, 0.015, steel, axis="y")
    # THE TRADE. A pawnbroker: a long glass counter of rings and watches on red
    # velvet, shelves of radios, cassette players and cameras behind, guitars on
    # the wall, every piece with a white ticket, and handwritten notices.
    if shop["id"] == "pawnbroker":
        wood = mat("counter_wood", (0.30, 0.18, 0.10), rough=0.45, noise=0.15)
        velvet = mat("velvet", (0.32, 0.03, 0.05), rough=0.9)
        glassm = mat("glass", (1.0, 1.0, 1.0), glass=True)
        gold = mat("gold", (0.85, 0.62, 0.25), rough=0.25, metal=1.0)
        silver = mat("silver", (0.80, 0.80, 0.82), rough=0.2, metal=1.0)
        black = mat("plastic_black", (0.03, 0.03, 0.03), rough=0.35)
        grey = mat("plastic_grey", (0.35, 0.35, 0.36), rough=0.4)
        ticket = mat("ticket", (0.85, 0.83, 0.75), rough=0.8)
        ink = mat("ink", (0.05, 0.05, 0.12), rough=0.8)
        shelfm = mat("shelf", (0.42, 0.30, 0.18), rough=0.6, noise=0.1)
        # The counter, across the room 2.4 m back, with a gap to pass at the right.
        cy0, cy1 = 2.4, 2.95
        box("counter_base", -W / 2 + 0.3, 1.2, cy0, cy1, 0, 0.75, wood)
        box("counter_velvet", -W / 2 + 0.35, 1.15, cy0 + 0.04, cy1 - 0.04, 0.75, 0.77, velvet)
        box("counter_glass_top", -W / 2 + 0.3, 1.2, cy0, cy1, 1.0, 1.01, glassm)
        box("counter_glass_front", -W / 2 + 0.3, 1.2, cy0 - 0.005, cy0, 0.75, 1.0, glassm)
        import random
        rnd = random.Random(7)
        x = -W / 2 + 0.45
        while x < 1.05:
            y = cy0 + 0.1 + rnd.random() * 0.35
            kind = rnd.random()
            if kind < 0.45:
                bpy.ops.mesh.primitive_torus_add(major_radius=0.012, minor_radius=0.003, location=(x, y, 0.785))
                o = bpy.context.object
                o.data.materials.append(gold if rnd.random() < 0.7 else silver)
            elif kind < 0.8:
                cyl("watch", x, y, 0.78, 0.018, 0.008, gold if rnd.random() < 0.5 else silver)
                box("strap", x - 0.008, x + 0.008, y - 0.05, y + 0.05, 0.771, 0.775, black)
            else:
                box("chain", x - 0.06, x + 0.06, y - 0.004, y + 0.004, 0.771, 0.776, gold)
            box("tag", x + 0.02, x + 0.045, y - 0.01, y + 0.01, 0.771, 0.773, ticket)
            x += 0.05 + rnd.random() * 0.05
        # THE STOCK, CRAMMED, as a 1990 pawnbroker's was (the second pass: the first
        # read as a showroom, a few things lost on long shelves). Five tiers on the
        # back wall and a unit down the left wall, filled shoulder to shoulder from
        # the stock pool (Poly Haven, CC0), each piece with its white ticket.
        pool = [("boombox", 0.5), ("cassette_player", 0.3), ("portable_cassette_player", 0.22), ("television_02", 0.4),
                ("Camera_01", 0.15), ("vintage_video_camera", 0.28), ("vintage_binocular", 0.17), ("mantel_clock_01", 0.28),
                ("brass_vase_01", 0.22), ("cardboard_box_01", 0.3)]

        def fill(x0, x1, y, z, depth_turn=0.0, along="x"):
            pos = x0
            while True:
                asset, size = pool[rnd.randrange(len(pool))]
                size *= rnd.uniform(0.85, 1.1)
                if pos + size > x1:
                    break
                c = pos + size / 2
                if along == "x":
                    model(asset, c, y + rnd.uniform(-0.03, 0.03), z, turn=depth_turn + rnd.uniform(-0.3, 0.3), size=size)
                    box("ticket_%d_%d" % (int(c * 100), int(z * 100)), c - 0.02, c + 0.02, y - 0.17, y - 0.168, z + 0.01, z + 0.045, ticket)
                else:
                    model(asset, y + rnd.uniform(-0.03, 0.03), c, z, turn=depth_turn + rnd.uniform(-0.3, 0.3), size=size)
                pos += size + rnd.uniform(0.0, 0.04)

        tiers = (0.9, 1.25, 1.6, 1.95, 2.28)
        for k, z in enumerate(tiers):
            box("back_shelf_%d" % k, -W / 2 + 0.05, W / 2 - 0.05, D - 0.4, D - 0.02, z - 0.025, z, shelfm)
            if z < 1.2:
                fill(-W / 2 + 0.1, 0.95, D - 0.22, z)
                fill(2.05, W / 2 - 0.1, D - 0.22, z)
            elif z < 2.2:
                fill(-W / 2 + 0.1, W / 2 - 0.1, D - 0.22, z)
            else:
                pos = -W / 2 + 0.15
                while pos < W / 2 - 0.4:      # the top tier: boxes of stock to the ceiling
                    model("cardboard_box_01", pos + 0.17, D - 0.22, z, turn=rnd.uniform(-0.2, 0.2), size=rnd.uniform(0.28, 0.36))
                    pos += 0.38
        # A unit down the left wall, side-on to the window, as full as the back.
        for k, z in enumerate((0.5, 0.9, 1.3, 1.7)):
            box("left_shelf_%d" % k, -W / 2 + 0.02, -W / 2 + 0.42, 0.3, 2.2, z - 0.025, z, shelfm)
            fill(0.35, 2.15, -W / 2 + 0.22, z, depth_turn=-math.pi / 2, along="y")
        # Behind the counter, a glazed cabinet; pocket watches among the rings in the counter;
        # a clock on the wall; tools on a side shelf; suitcases on the floor.
        model("vintage_cabinet_01", -0.2, D - 0.7, 0.0, size=1.6)
        for n, x in enumerate((-1.9, -1.5, -1.1, -0.6, -0.1, 0.5, 0.9)):
            model("pocket_watch" if n % 2 else "vintage_pocket_watch", x, cy0 + 0.3, 0.775, turn=rnd.uniform(-1, 1), size=0.06)
        model("wall_clock", 1.6, D - 0.05, 2.15, size=0.3)
        # THE SECOND PASS (1 October, judged in the game against the Hook sheet and
        # the KCD2 frames): the right wall stood nearly bare and the floor empty, so
        # the room read as a showroom. A unit down the right wall as full as the
        # left, tools and household goods on it; instruments and frames hung above;
        # the till on the counter; a tool chest, a television and a long-case clock
        # on the floor, as pledges stood wherever there was room.
        pool_right = [("vintage_electric_kettle", 0.24), ("tea_set_01", 0.3), ("alarm_clock_01", 0.14),
                      ("vintage_radio_transceiver", 0.4), ("filmstrip_projector_8mm", 0.3), ("metal_toolbox", 0.45),
                      ("hand_plane_no4", 0.26), ("bench_vice_01", 0.25), ("chess_set", 0.32), ("mantel_clock_01", 0.28)]
        for k, z in enumerate((0.45, 0.85, 1.25)):
            box("right_shelf_%d" % k, W / 2 - 0.42, W / 2 - 0.02, 0.3, 2.1, z - 0.025, z, shelfm)
            pos = 0.35
            while True:
                asset, size = pool_right[rnd.randrange(len(pool_right))]
                size *= rnd.uniform(0.85, 1.1)
                if pos + size > 2.05:
                    break
                model(asset, W / 2 - 0.22 + rnd.uniform(-0.03, 0.03), pos + size / 2, z, turn=math.pi / 2 + rnd.uniform(-0.3, 0.3), size=size)
                box("rticket_%d_%d" % (int(pos * 100), k), W / 2 - 0.42, W / 2 - 0.418, pos + size / 2 - 0.02, pos + size / 2 + 0.02, z + 0.01, z + 0.045, ticket)
                pos += size + rnd.uniform(0.0, 0.04)
        # Above the unit, read from the window: two ukuleles hung by their heads,
        # then the notices; the mirror in the gap before the counter.
        for n, y in enumerate((0.45, 0.8)):
            model("Ukulele_01", W / 2 - 0.08, y, 1.72, turn=-math.pi / 2 + 0.1 * n, size=0.62)
        model("ornate_mirror_01", W / 2 - 0.04, 2.25, 1.2, turn=-math.pi / 2, size=0.42)
        model("CashRegister_01", 0.85, cy0 + 0.3, 1.01, turn=math.pi + 0.2, size=0.42)
        model("vintage_grandfather_clock_01", 2.3, D - 0.62, 0.0, turn=0.0, size=2.0)
        # NOTHING STANDS ON THE OPEN FLOOR (the fresh reviewer, 1 October: the
        # television and the tool chest in the middle of the floor smeared into a
        # flat slab from the side, because a projected room is true only on its
        # walls, floor and ceiling; the method's own rule is to keep the room simple
        # and put the detail in the display). Floor stock stands against a wall:
        # under the right-hand unit and along the back, between counter and clock.
        # (and not under the side unit either: a television there, standing 0.4 m
        # out from the wall, still smeared into a black wedge; the second reviewer)
        model("vintage_suitcase", 1.55, D - 0.2, 0.0, turn=0.0, size=0.55)
        model("cardboard_box_01", 1.85, D - 0.22, 0.0, turn=0.1, size=0.36)
        # Notices: the counter's own card, and the printed notices a licensed
        # pawnbroker had to show (the Consumer Credit Act 1974 governed pawn
        # loans), pinned up on the walls among handwritten ones.
        # A pawnbroker lends on pledges and sells what is not redeemed; "PLEDGES BOUGHT
        # & SOLD" was the wrong trade's wording (the fresh reviewer, 1 October).
        text("notice_pledges", "CASH LOANS", -0.6, cy0 - 0.012, 1.15, 0.075, ink, rot_x=math.pi / 2)
        text("notice_loans", "on Gold, Watches & Tools", -0.6, cy0 - 0.012, 1.065, 0.045, ink, rot_x=math.pi / 2)
        box("notice_card", -1.25, 0.05, cy0 - 0.01, cy0 - 0.005, 1.03, 1.23, ticket)
        red = mat("ink_red", (0.45, 0.04, 0.03), rough=0.8)
        yellowed = mat("card_yellowed", (0.78, 0.72, 0.55), rough=0.85, noise=0.2)

        def wall_notice(name, lines, y, z, w, h, inkm, cardm):
            # on the right wall, read from the window: the card faces -x
            box(name, W / 2 - 0.006, W / 2 - 0.002, y - w / 2, y + w / 2, z - h / 2, z + h / 2, cardm)
            for i, (body, size) in enumerate(lines):
                o = text(name + "_t%d" % i, body, W / 2 - 0.008, y, z + h / 2 - 0.03 - i * size * 1.5 - size * 0.4, size, inkm, rot_x=math.pi / 2)
                o.rotation_euler = (math.pi / 2, 0.0, -math.pi / 2)
        wall_notice("notice_licence", [("LICENSED PAWNBROKER", 0.035), ("Consumer Credit Act 1974", 0.024),
                                       ("Loans on all articles of value", 0.022)],
                    1.3, 2.1, 0.5, 0.2, ink, ticket)
        wall_notice("notice_unredeemed", [("UNREDEEMED", 0.04), ("PLEDGES FOR SALE", 0.04)], 1.85, 2.12, 0.48, 0.16, red, yellowed)
        # and on the counter's front, low, the electrical goods' promise
        text("notice_tested", "ALL ELECTRICAL GOODS TESTED", 0.2, cy0 - 0.012, 0.5, 0.04, red, rot_x=math.pi / 2)
        box("notice_tested_card", -0.45, 0.85, cy0 - 0.01, cy0 - 0.005, 0.46, 0.58, yellowed)
        # a worn mat inside the door, and the floor's traffic path scuffed darker
        box("door_mat", -W / 2 + 0.3, -W / 2 + 1.3, 0.05, 0.75, 0.0, 0.012, mat("mat", (0.08, 0.06, 0.05), rough=0.95, noise=0.4))
        # (no trodden path: on the textured lino it read as a flat grey slab, the second reviewer)

    # MICKEY'S: A MINICAB OFFICE'S FRONT ROOM (his order, 3 October: "Mickey's interior is part of the
    # shopfronts step, first among them"; his ruling: "Mickey's window shows its office"). Laid out
    # from its plan (production/specs/mickeys-office.json, game-design/mickeys-office/BRIEF.md),
    # turned into this room's frame: x across, +x the viewer's right from the street (the stair
    # strip's side), y back from the glass. The public side: a vinyl bench down the left wall under
    # the fares and the licence; the booking counter across, the book of every fare, the phone, an
    # ashtray and the dockets on it; the staff side: the radio set and its desk microphone, Mickey's
    # chair empty behind them (the brief: he worked the radio himself), the district map above; the
    # door to Sheila's back room ajar. Dressed from the cab office research (production/research/
    # cab-office-interior-1990): paper and voice radio, not screens; wood-effect tops, a fabric
    # swivel chair on a five-star base, plastic trays, coiled phone cords, a pot plant; the firm's
    # number signwritten on the glass ("the window is the sign"). Nobody in it, no brands, no drink,
    # no betting slips; tobacco allowed.
    if shop["id"] == "mickeys":
        import random
        rnd = random.Random(19)
        # REAL SURFACES (the second fresh review: "flat colour, no grain, seams or wear"): Poly Haven's
        # veneer for the wood-effect laminate (the counter, bench and chair carry their own materials)
        laminate = texmat("laminate_ash", "ash_veneer", 0.8, (0.78, 0.62, 0.44),
                          base=mat("laminate_wood_effect", (0.42, 0.29, 0.17), rough=0.38, noise=0.2))

        def metre_uvs(o, tile):
            # UVs in metres before export, so a picture tiles at its own size on a long counter
            bpy.ops.object.select_all(action="DESELECT")
            o.select_set(True)
            bpy.context.view_layer.objects.active = o
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.uv.cube_project(cube_size=tile)
            bpy.ops.object.mode_set(mode="OBJECT")

        PRINT = "production/assets/office-print/mickeys/"

        def print_plane(name, pic, cx, cy, cz, w, h, facing):
            """One of tools/props/make_office_print.py's pictures on a plane (the dressing research:
            print is texture, not geometry): facing "-y" to the glass, "+x" off the left wall, "up"."""
            rot = {"-y": (math.pi / 2, 0.0, 0.0), "+x": (math.pi / 2, 0.0, math.pi / 2), "up": (0.0, 0.0, 0.0)}[facing]
            bpy.ops.mesh.primitive_plane_add(size=1.0, location=(cx, cy, cz), rotation=rot)
            o = bpy.context.object
            o.name = name
            o.scale = (w, h, 1.0)
            key = "print_" + pic
            m = bpy.data.materials.get(key)
            if m is None:
                m = bpy.data.materials.new(key)
                m.use_nodes = True
                pr = m.node_tree.nodes["Principled BSDF"]
                tx = m.node_tree.nodes.new("ShaderNodeTexImage")
                tx.image = bpy.data.images.load(os.path.join(REPO, PRINT + pic + ".png"), check_existing=True)
                m.node_tree.links.new(tx.outputs["Color"], pr.inputs["Base Color"])
                pr.inputs["Roughness"].default_value = 0.65
            o.data.materials.append(m)
            return o
        black = mat("plastic_black", (0.025, 0.025, 0.025), rough=0.4)
        cream_plastic = mat("phone_cream", (0.60, 0.55, 0.43), rough=0.35)
        paper = mat("paper", (0.80, 0.77, 0.66), rough=0.85)
        paper_yellow = mat("paper_yellowed", (0.74, 0.66, 0.46), rough=0.85)
        card_white = mat("card_white", (0.84, 0.82, 0.74), rough=0.85)
        ink = mat("ink", (0.04, 0.04, 0.07), rough=0.8)
        ink_red = mat("ink_red", (0.45, 0.04, 0.03), rough=0.8)
        ink_blue = mat("ink_blue", (0.04, 0.08, 0.35), rough=0.8)
        cloth_green = mat("ledger_cloth", (0.04, 0.10, 0.06), rough=0.7)
        gilt = mat("gilt", (0.86, 0.64, 0.28), rough=0.25, metal=1.0)
        ash_glass = mat("ashtray_glass", (0.35, 0.42, 0.38), rough=0.15)
        ash = mat("ash_grey", (0.30, 0.29, 0.27), rough=1.0)
        stub = mat("stub_white", (0.85, 0.82, 0.72), rough=0.8)
        filter_tan = mat("filter_tan", (0.70, 0.45, 0.20), rough=0.8)
        mug_brown = mat("mug_brown", (0.30, 0.15, 0.07), rough=0.3)
        red_led = mat("led_red", (0.9, 0.05, 0.03), emit=(1.0, 0.05, 0.02), emit_strength=8.0)
        green_led = mat("led_green", (0.05, 0.8, 0.1), emit=(0.1, 1.0, 0.15), emit_strength=6.0)

        # THE STAIR STRIP'S WALL on the right (the plan: x 4.05 to 4.19 along the street), floor to
        # ceiling; the street door opens between it and the window.
        box("stair_wall", 1.81, 1.95, 0.0, D, 0.0, H, wall)
        box("stair_wall_dado", 1.80, 1.81, 0.0, D, 0.0, 0.95, dado)
        # THE REVEAL'S TIMBER LINING, 6 October (item 1.1's first gate: "the window reveal still has
        # the black pitted scan material"; MICKEYS-OTHER-DIRECTION-2026-10-04.md: "the reveal's
        # timber lining (replacing the black scan)"): a painted board down each side of the opening
        # and across its head, just behind the glass, covering the walls' raw ends.
        lining = mat("reveal_lining_gloss", (0.62, 0.58, 0.48), rough=0.35, noise=0.05)
        box("reveal_lining_left", -W / 2, -W / 2 + 0.07, -0.02, 0.10, 0.0, H, lining)
        box("reveal_lining_right", 1.74, 1.81, -0.02, 0.10, 0.0, H, lining)
        box("reveal_lining_head", -W / 2, 1.81, -0.02, 0.10, H - 0.07, H, lining)

        # THE WINDOW BOARD inside the glass, and what sits on it: a spider plant, two directories
        # gone yellow in the sun, a saucer ashtray.
        metre_uvs(box("window_board", -2.62, 0.86, 0.0, 0.24, 0.62, 0.655, laminate), 0.8)
        def lighten(root, ratio):
            # a scanned plant cut to a fraction of its triangles: at the window it reads the same
            for o in ([root] + list(root.children_recursive)) if root else []:
                if o.type == "MESH":
                    o.modifiers.new("lighten", "DECIMATE").ratio = ratio
        lighten(model("potted_plant_02", -2.25, 0.12, 0.655, turn=0.4, size=0.42), 0.3)
        # EACH A BOOK, NOT A BOX (8 October, item 1.1's third review: "the two telephone directories
        # plain boxes"): thin soft covers a little proud of the pages, the spine to the room, and the
        # fore-edge to the street as newsprint in uneven layers, so the edge reads as pages; the
        # upper one dropped a few degrees askew. Geometry only: the room's glb keeps no noise.
        edge_lt = mat("directory_pages", (0.62, 0.58, 0.47), rough=0.9)
        # (second try, the night gate's reviewer: "4 or 5 even, coarse bands", "covers overhang like a
        # hardback"): a phone book is a paperback, its covers flush with the pages, the newsprint in
        # many thin gatherings a shade apart
        edge_dk = mat("directory_pages_dark", (0.54, 0.50, 0.40), rough=0.9)
        def turn_about(objs, px, py, ang):
            ca, sa = math.cos(ang), math.sin(ang)
            for o in objs:
                dx, dy = o.location.x - px, o.location.y - py
                o.location.x, o.location.y = px + dx * ca - dy * sa, py + dx * sa + dy * ca
                o.rotation_euler[2] += ang
        for k, (x0, w, h, c, ang) in enumerate(((-0.55, 0.22, 0.05, (0.62, 0.52, 0.16), 0.0),
                                                 (-0.53, 0.21, 0.045, (0.58, 0.48, 0.15), -0.07))):
            z0, x1, y0, y1, cv = 0.655 + k * 0.05, x0 + w, 0.04, 0.32, 0.0015
            cover = mat("directory_%d" % k, c, rough=0.8)
            parts = [box("directory_%d_back" % k, x0, x1, y0, y1, z0, z0 + cv, cover),
                     box("directory_%d_front" % k, x0, x1, y0, y1, z0 + h - cv, z0 + h, cover),
                     box("directory_%d_spine" % k, x0, x1, y1 - 0.004, y1, z0, z0 + h, cover)]
            n = 12
            for j in range(n):
                # each gathering under a millimetre in or out at the fore-edge, the tones alternating
                inset = 0.0002 + 0.0008 * ((j * 5 + k) % 4) / 3.0
                parts.append(box("directory_%d_pages_%d" % (k, j), x0 + 0.0005, x1 - 0.0005, y0 + inset,
                                 y1 - 0.004, z0 + cv + (h - 2 * cv) * j / n, z0 + cv + (h - 2 * cv) * (j + 1) / n,
                                 edge_lt if (j + k) % 2 == 0 else edge_dk))
            if k == 1:
                # their covers printed (a district's directories, no publisher named), sun-faded
                parts.append(print_plane("directory_cover", "directory", -0.43, 0.18, z0 + h + 0.0005, 0.20, 0.25, "up"))
            turn_about(parts, (x0 + x1) / 2, (y0 + y1) / 2, ang)
        # (the heater under the window is a modelled prop now, placed with the others below)

        # THE FIRM'S NUMBER ON THE GLASS, in gilt (the 1980 Brixton photograph: the window is the
        # sign). 0632 is the code television used for numbers that rang nowhere. Our Marcellus SC,
        # read from the street.
        # GILT WITH ITS BLACK SHADE behind, down and to the right, as a signwriter laid it (the
        # first film: gold alone was lost over the lit room)
        shade = mat("gilt_shade", (0.01, 0.01, 0.01), rough=0.6)
        # LAID ON THE GLASS AS PAINT IS, 6 October (item 1.1's first gate: "seen from inside, the
        # gilt number is a thick black slab with a sawtooth edge"): leaf and shade flat against the
        # pane's inside face, a hair apart, their curves smooth at the lettering's own size; from
        # inside the room they read as a signwriter's backs do, crisp dark letters on the glass.
        for name, body, z, size in (("glass_number", "0632  960418", 2.02, 0.17), ("glass_word", "MINICABS  ·  24 HOURS", 1.82, 0.085)):
            text(name, body, -0.92, 0.03, z, size, gilt, font="marcellus-sc/MarcellusSC-Regular.ttf", extrude=0.0003, res=7)
            text(name + "_shade", body, -0.92 + size * 0.03, 0.0312, z - size * 0.03, size, shade,
                 font="marcellus-sc/MarcellusSC-Regular.ttf", extrude=0.0003, res=7)

        # (the venetian blind half down over the window's left run is a modelled prop now, below)
        # (the oxblood bench down the left wall is a modelled prop now, below)

        # THE NOTICES above the bench, printed, facing across the room: the fares, the licence, the
        # accounts card, the calendar (tools/props/make_office_print.py)
        lw = -W / 2 + 0.006
        print_plane("notice_fares", "fares", lw, 1.05, 1.58, 0.30, 0.42, "+x")
        print_plane("notice_licence", "licence", lw, 1.62, 1.70, 0.21, 0.148, "+x")
        print_plane("notice_accounts", "accounts", lw, 0.48, 1.42, 0.30, 0.10, "+x")
        print_plane("calendar", "calendar", lw, 1.62, 1.22, 0.30, 0.42, "+x")

        # THE BOOKING COUNTER across the room (the plan: z 7.5 to 8.0 back from the pavement),
        # from the left wall to a gap at the stair wall for the staff to pass
        cy0, cy1 = 2.23, 2.73
        cx0, cx1 = -W / 2, 0.80
        # (the counter itself is a modelled prop now, placed with the others below; its top at 0.985)
        # on it: THE BOOK OF EVERY FARE, open, its cloth cover and ruled pages written up
        bkx, bky = -1.20, 2.47
        box("fare_book_cover", bkx - 0.27, bkx + 0.27, bky - 0.19, bky + 0.19, 0.985, 0.995, cloth_green)
        print_plane("fare_book_spread", "farebook", bkx, bky, 1.0, 0.52, 0.36, "up")
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.004, depth=0.14, location=(bkx + 0.12, bky - 0.05, 1.012), rotation=(0.0, math.pi / 2, 0.35))
        bpy.context.object.data.materials.append(ink_blue)
        # THE HERO PROPS, 6 October (phase 1, item 1.1; tools/art-recipes/mickeys-props, production/art/
        # mickeys-props/README.md): modelled by script at their real sizes from dated period references,
        # in place of the boxes and cylinders the third review called "plain props". Each glb lives on
        # F:/LedgerTools/game-inputs; its base stands at z, its front toward the glass (-y) before the turn.
        # Its ao and edge masks are left out of this room's export until the wear material reads them.
        props_dir = os.path.join(os.environ.get("LEDGER_GAME_INPUTS", "F:/LedgerTools/game-inputs"),
                                 "production", "assets", "mickeys-props")

        def prop(name, x, y, z, turn=0.0):
            path = os.path.join(props_dir, name + ".glb")
            if not os.path.isfile(path):
                print("shop-room: prop %s missing at %s" % (name, path), flush=True)
                return None
            before = set(bpy.data.objects)
            bpy.ops.import_scene.gltf(filepath=path)
            new = [o for o in bpy.data.objects if o not in before]
            root = bpy.data.objects.new(name + "_prop", None)
            sc.collection.objects.link(root)
            for o in new:
                if o.type == "MESH":
                    for nm in [a.name for a in o.data.color_attributes]:
                        o.data.color_attributes.remove(o.data.color_attributes[nm])
                if o.parent is None:
                    o.parent = root
            root.rotation_euler = (0.0, 0.0, turn)
            root.location = (x, y, z)
            return root

        # THE FURNITURE, 6 October (set 2 of the same props, modelled by script at their researched
        # sizes): the counter built to this room, 3.45 m from the left wall to the staff passage, its
        # top at 0.985 and no flap (the plan leaves the passage at the stair wall open); the bench
        # down the left wall facing across; the convector heater on the stallriser under the window;
        # the blind half down over the window's left run, its slats tilted half open; the four-drawer
        # cabinet behind the counter, its drawers to the window.
        prop("counter_mickeys", (cx0 + cx1) / 2.0, (cy0 + cy1) / 2.0, 0.0)
        prop("bench", -W / 2 + 0.255, 1.185, 0.0, turn=math.pi / 2)
        # (no folded paper on it: a plain box with no print, it read as a blank white slab through the
        # glass, item 1.1's third review, V10, 8 October)
        prop("heater", -1.35, 0.06, 0.14, turn=math.pi)
        # the blind's 1.32 m centred at -1.94 ran 0.3 m past the first mullion into the middle pane
        # (item 1.1's third review, V10, 8 October): its right end now meets the mullion and its spare
        # width lies behind the solid pier, seen only from inside, as a blind hung outside the recess
        prop("blind_mickeys", -2.26, 0.05, 1.62, turn=math.pi)
        prop("filing_cabinet", -W / 2 + 0.255, 3.61, 0.0)

        # the phone, a cream push-button set of the decade with its coiled cord (one line: the black
        # dial set of before was boxes)
        phx, phy = -2.30, 2.45
        prop("telephone", phx, phy, 0.985, turn=0.25)
        # the glass ashtray, its ash and filter ends
        prop("ashtray", -1.75, 2.42, 0.985, turn=0.4)
        model("cigarette_pack", -1.58, 2.50, 0.985, turn=0.7, size=0.09)
        # the dockets on their spike, a mug of tea gone cold, a pad
        prop("docket_spike", -0.62, 2.48, 0.985, turn=0.3)
        prop("mug-chipped", -0.95, 2.62, 0.985, turn=2.2)
        # (the second mug stands on the radio desk, below) and the stationery and pads of an office that works
        model("office_notepads", 0.10, 2.50, 0.985, turn=0.2, size=0.22)
        model("stationery_supplies", -1.48, 3.13 + 0.12, 0.74 + 0.02, turn=0.5, size=0.25)
        box("pad", 0.15, 0.36, 2.36, 2.62, 0.985, 0.995, paper_yellow)
        # a plastic letter tray at the counter's right end (set 3, modelled: foolscap, smoked brown)
        prop("letter_tray", 0.58, 2.49, 0.985, turn=0.1)
        # a metal bin on the customers' side
        prop("waste_bin", 0.35, 1.95, 0.0)

        # THE RADIO DESK on the staff side (the plan: z 8.4 to 8.95), grey steel under a wood-effect top
        ry0, ry1 = 3.13, 3.68
        rx0, rx1 = -1.80, -0.30
        # (4 October, after the fresh review's "featureless slabs": Poly Haven's metal office
        # desk, CC0, at 1.5 m, its top read back and the set stood on it)
        desk = model("metal_office_desk", (rx0 + rx1) / 2.0, (ry0 + ry1) / 2.0, 0.0, turn=0.0, size=1.5)
        desk_top = 0.74
        if desk is not None:
            bpy.context.view_layer.update()
            from mathutils import Vector
            desk_top = max((o.matrix_world @ Vector(c)).z for o in [desk] + list(desk.children_recursive)
                           if o.type == "MESH" for c in o.bound_box)
        dz = desk_top - 0.74
        # THE SET ON A DISPATCHER'S RISER SHELF, 6 October (phase 1, item 1.1; production/research/
        # shop-window-interiors/MICKEYS-OTHER-DIRECTION-2026-10-04.md, method 1: compose for the window).
        # From the pavement 1.2 m out at eye 1.6 m the counter's top edge hides everything at the desk
        # below about 0.86 m: on the desk the set showed its top 9 cm, the third review's "radio desk
        # out of sight". On a riser at 1.15 m it is seen whole over the counter, as a dispatcher keeps it.
        rz = 1.15 + dz
        box("radio_riser_shelf", -1.42, -0.74, ry0 + 0.04, ry0 + 0.54, rz - 0.03, rz, laminate)
        for xx in (-1.42, -0.77):
            box("radio_riser_side", xx, xx + 0.03, ry0 + 0.04, ry0 + 0.54, 0.74 + dz, rz - 0.03, laminate)
        # the base station with its desk microphone and coiled lead (the hero prop: a car set on its
        # mains unit, as late-1980s minicab offices had it), turned a little to the window so its
        # face, its knobs and its red channel window read from the street
        prop("radio-base-station", -1.08, ry0 + 0.29, rz, turn=-0.45)
        # the anglepoise over the desk, its warm pool on the dockets at night; a clipboard of the jobs
        prop("desk-lamp", -1.62, ry0 + 0.35, desk_top, turn=2.6)
        model("clipboard", -0.45, ry0 + 0.18, desk_top, turn=0.3, size=0.32)
        # a pad of dockets, a mug gone cold, a second ashtray
        box("radio_pad", -0.70, -0.46, ry0 + 0.32, ry0 + 0.50, 0.74 + dz, 0.75 + dz, paper)
        prop("mug", -0.40, ry0 + 0.42, desk_top, turn=1.2)
        prop("ashtray", -0.62, ry0 + 0.10, desk_top, turn=1.0)
        # the loudspeaker on its bracket above the desk, so the room hears every job
        # (set 3, modelled: a wooden cabinet with its cloth front, tipped down on its bracket)
        prop("loudspeaker", -1.10, D, 2.0)
        # MICKEY'S CHAIR, empty: the modelled fabric swivel chair on its five-star base, at its real
        # 0.80 m (the 1.25 m box back is gone: the set on its riser is what reads over the counter),
        # pushed in under the desk's back edge and left turned a little, as he got up from it
        prop("chair", -1.05, 3.84, 0.0, turn=0.25)
        # a jacket left over the chair's back (his)
        # (no jacket: as a box over the chair's back it read as a flat card, the second fresh review)

        # THE DISTRICT'S STREET PLAN over the radio desk, 6 October (the brief's "the district map
        # above"; held back on 4 October until the town's map was his, adopted since, RULINGS D13;
        # item 1.1's first gate: "no district map"): printed from the atlas by
        # tools/props/make_office_print.py, Mickey's ringed in red, clear of the loudspeaker
        print_plane("district_map", "district_map", -1.675, D - 0.008, 1.615, 0.95, 0.71, "-y")
        # the drivers' board over the radio desk: each car's number and its status
        print_plane("drivers_board", "drivers_board", -0.62, D - 0.008, 1.60, 0.60, 0.70, "-y")
        # a pot plant in the corner by the stair wall, and a strip of light under the back door's head
        lighten(model("potted_plant_01", 1.55, 3.6, 0.0, turn=1.2, size=0.75), 0.1)
        # WEAR: thirty years of boots on the counter's kick and front, a trodden path in the carpet
        # from the door to the counter, the counter top's laminate rubbed pale where the book lies
        # (no scuff boxes on the counter's foot: in the game they read as a dark skyline)
        box("carpet_path", -0.6, 1.6, 0.6, 2.2, 0.0, 0.004, mat("carpet_trodden", (0.065, 0.045, 0.032), rough=0.98, noise=0.5))
        box("counter_rubbed", bkx - 0.4, bkx + 0.4, cy0 + 0.02, cy0 + 0.25, 0.985, 0.9858, mat("laminate_rubbed", (0.55, 0.43, 0.30), rough=0.3))
        # A PINBOARD right of the back door: dockets, a postcard, a card of phone numbers
        print_plane("pinboard", "pinboard", 1.35, D - 0.008, 1.45, 0.70, 0.60, "-y")
        # "BOOKINGS" on a stand at the counter's front edge, read from the window
        box("bookings_stand", -1.95, -1.55, cy0 + 0.045, cy0 + 0.05, 0.985, 1.105, card_white)
        print_plane("bookings_card", "bookings", -1.75, cy0 + 0.043, 1.045, 0.40, 0.12, "-y")
        # the fares again, taped to the counter's front where the waiting customer reads them (the
        # dressing research: face the important notices to the glass)
        print_plane("counter_fares", "fares", -1.95, cy0 + 0.019, 0.55, 0.30, 0.42, "-y")   # on the panel mouldings' face
        # (no stacking chair by the stair wall: it stood 1.1 m inside the door, in the line Tom walks
        # in by, and he walked through it; the bench seats the customers. Item 1.1's third review, V9,
        # 8 October)
        # the lighter by the counter's ashtray
        model("vintage_lighter", -1.62, 2.36, 0.985, turn=0.4, size=0.06)
        # COAT HOOKS by the back door, a rail of four (no coats: as boxes they read as boards)
        prop("coat_rail", 1.32, D, 1.64)
        # THE OFFICE CLOCK over the back door (Poly Haven's wall clock, CC0)
        model("wall_clock", 0.42, D - 0.03, 2.25, turn=0.0, size=0.30)
        # SHEILA'S BACK ROOM through the half-open back door (8 October, item 1.1's third review,
        # V9: "the room beyond the door flat untextured grey"): a real room a metre deep, so the
        # office's light falls into it and falls off, its walls, floor and skirting meeting in
        # corners, a shelf with a mug and a coat rail on the far wall (the office's calendar is the only print, so none here)
        bx0, bx1 = back_gap
        by0, by1 = D + t, D + t + 1.1
        rx0, rx1 = bx0 - 0.6, bx1 + 0.9
        back_wall = mat("back_room_wall", (0.46, 0.40, 0.30), rough=0.9)
        back_floor = mat("back_room_lino", (0.20, 0.15, 0.11), rough=0.6)
        back_wood = mat("back_room_wood", (0.22, 0.14, 0.08), rough=0.6)
        box("back_room_floor", rx0, rx1, by0, by1, -0.012, 0.0, back_floor)
        box("back_room_far", rx0, rx1, by1, by1 + 0.05, 0.0, 2.4, back_wall)
        box("back_room_side_l", rx0 - 0.05, rx0, by0, by1, 0.0, 2.4, back_wall)
        box("back_room_side_r", rx1, rx1 + 0.05, by0, by1, 0.0, 2.4, back_wall)
        box("back_room_ceiling", rx0, rx1, by0, by1, 2.4, 2.45, back_wall)
        box("back_room_skirting", rx0, rx1, by1 - 0.015, by1, 0.0, 0.10, back_wood)
        box("back_room_shelf", bx0 + 0.05, bx1 + 0.3, by1 - 0.22, by1, 1.10, 1.125, back_wood)
        prop("mug", bx0 + 0.25, by1 - 0.10, 1.125, turn=0.3)
        prop("coat_rail", bx0 + 0.45, by1, 1.64)
        # THE FANLIGHT'S LETTERS, reverse-gilded on the glass over the street door (the dressing
        # research; the second review read the fanlight as "a blank board")
        for nm_, col_, off_ in (("fanlight_word_shade", mat("gilt_shade2", (0.01, 0.01, 0.01), rough=0.6), 0.003),
                                ("fanlight_word", gilt, 0.0)):
            text(nm_, "MINICABS", 1.40 + off_, -0.088 + abs(off_), 2.43 - off_, 0.085, col_,
                 font="marcellus-sc/MarcellusSC-Regular.ttf")
        # a doormat inside the street door
        box("door_mat", 0.95, 1.78, 0.05, 0.70, 0.0, 0.014, mat("door_mat", (0.10, 0.07, 0.05), rough=0.98, noise=0.4))
        # A PICTURE RAIL round the room at 2.2 m, the paint above it browner with thirty years'
        # smoke (the first film: the left wall one flat bright panel)
        rail = mat("picture_rail", (0.20, 0.12, 0.065), rough=0.5)
        frieze = mat("frieze_smoke", (0.24, 0.18, 0.10), rough=0.9, noise=0.35)
        box("rail_left", -W / 2, -W / 2 + 0.025, 0.0, D, 2.18, 2.22, rail)
        box("frieze_left", -W / 2, -W / 2 + 0.004, 0.0, D, 2.22, H, frieze)
        box("rail_back", -W / 2, 1.81, D - 0.025, D, 2.18, 2.22, rail)
        box("frieze_back", -W / 2, 1.81, D - 0.004, D, 2.22, H, frieze)
        box("rail_stair", 1.785, 1.81, 0.0, D, 2.18, 2.22, rail)
        box("frieze_stair", 1.806, 1.81, 0.0, D, 2.22, H, frieze)
        # behind the counter on the left wall: a shelf of box files and ledgers, a grey four-drawer
        # cabinet under it, a fire extinguisher on its bracket
        metre_uvs(box("files_shelf", -W / 2, -W / 2 + 0.30, 2.85, 4.05, 1.78, 1.80, laminate), 0.8)
        for k in range(14):
            yy = 2.88 + k * 0.083
            c = rnd.choice(((0.08, 0.10, 0.22), (0.30, 0.05, 0.04), (0.10, 0.10, 0.10), (0.42, 0.36, 0.20), (0.06, 0.16, 0.10)))
            hgt = rnd.uniform(0.28, 0.34)
            o = box("box_file_%d" % k, -W / 2 + 0.01, -W / 2 + 0.28, yy, yy + 0.075, 1.80, 1.80 + hgt,
                    mat("file_%d_%d_%d" % tuple(int(v * 99) for v in c), c, rough=0.6))
            if k == 13:
                o.rotation_euler[0] = 0.25
        # (the four-drawer cabinet, its drawers to the window, is a modelled prop, placed above)
        # the jug kettle on the cabinet's top, where the office makes its tea (the plan's kettle, 6 October)
        prop("jug-kettle", -W / 2 + 0.25, 3.64, 1.32, turn=0.5)
        # the water extinguisher on its wall bracket (set 3, modelled: all red, BS 5423, before 1997's colour bands)
        prop("extinguisher", -W / 2, 3.05, 0.45, turn=math.pi / 2)

    if EXPORT:
        export_room(bpy, sc, os.path.abspath(argv[argv.index("--export-room") + 1]), shop_id)
        return
    # THE CAMERA: on the centre line, d in front of the front plane, framing W x H.
    cam_data = bpy.data.cameras.new("cam")
    cam_data.sensor_fit = "HORIZONTAL"
    cam_data.angle = horizontal_fov(W, d)
    cam = bpy.data.objects.new("cam", cam_data)
    sc.collection.objects.link(cam)
    cam.location = (0.0, -d, H / 2.0)
    cam.rotation_euler = (math.pi / 2.0, 0.0, 0.0)
    sc.camera = cam

    # THE LIGHTS for each state. An area light shines along its own -Z: turned +90 degrees about x it
    # shines along +y, into the room (the first renders had the daylight and the sodium turned away).
    # THE LIGHTS for each state. Daylight comes in through the front as a wide
    # soft source; the tubes are emissive; shut at night, only the street's
    # sodium spill and a faint light from the back room.
    def area(name, loc, rot, size_x, size_y, energy, colour):
        ld = bpy.data.lights.new(name, "AREA")
        ld.shape = "RECTANGLE"
        ld.size, ld.size_y = size_x, size_y
        ld.energy, ld.color = energy, colour
        o = bpy.data.objects.new(name, ld)
        sc.collection.objects.link(o)
        o.location, o.rotation_euler = loc, rot
        return o

    daylight = area("daylight", (0.0, -0.3, H * 0.6), (math.pi / 2.0, 0.0, 0.0), W, H * 0.8, 0.0, (0.9, 0.95, 1.0))
    sodium = area("sodium", (0.0, -0.6, H * 0.9), (math.pi / 2.0 - 0.3, 0.0, 0.0), W, 0.5, 0.0, (1.0, 0.55, 0.15))
    backlight = area("back_room_light", (1.5, D + 0.4, 1.8), (-math.pi / 2.0, 0.0, 0.0), 0.6, 0.6, 0.0, (1.0, 0.85, 0.65))
    tube_emit = tube_on.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    tube_light = [area("tube_light_%d" % k, (0.0, y, H - 0.1), (0.0, 0.0, 0.0), 1.5, 0.2, 0.0, (0.92, 0.97, 1.0))
                  for k, y in enumerate((1.0, 2.4, 3.8)) if y <= D - 0.3]
    states = {
        # name: (daylight W, tubes emission, tube light W, sodium W, back W, exposure)
        "day": (70.0, 25.0, 60.0, 0.0, 0.0, 0.0),       # daylight a soft fill through the front, the tubes the main light
        "night_lit": (0.0, 25.0, 60.0, 0.0, 0.0, 0.0),
        "night_dark": (0.0, 0.0, 0.0, 10.0, 2.0, 0.0),   # shut: a faint sodium spill near the front, the back room barely lit
    }
    record = {"shop": shop_id, "w": W, "h": H, "d": D, "camera_d": d, "pixels": [sc.render.resolution_x, sc.render.resolution_y],
              "states": {}, "made_by": "tools/art-recipes/shop-room.py", "samples": samples}
    for name, (day_w, tube_s, tube_w, sod_w, back_w, exposure) in states.items():
        daylight.data.energy = day_w
        tube_emit.default_value = tube_s
        # The back of the shop darker than the front (the reviewer: "lit too flatly,
        # no falloff toward the back"): the back tube's light at a third.
        for k, o in enumerate(tube_light):
            o.data.energy = tube_w * (0.35 if k == len(tube_light) - 1 else 1.0)
        sodium.data.energy = sod_w
        backlight.data.energy = back_w
        sc.view_settings.exposure = exposure
        path = os.path.join(out, "%s_%s.png" % (shop_id, name))
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
        record["states"][name] = os.path.basename(path)
        print("shop-room: %s %s written" % (shop_id, name), flush=True)
    json.dump(record, open(os.path.join(out, shop_id + ".json"), "w", encoding="utf-8"), indent=1)
    print("shop-room: done %s" % json.dumps(record))


def label_sheet():
    """The grocer's sheet of made-up labels (tools/art-recipes/make_label_atlas.py): its path and tiles."""
    d = os.path.join(REPO, "production", "assets", "shop-goods")
    idx = json.load(open(os.path.join(d, "labels.json"), encoding="utf-8"))
    return os.path.join(d, "labels.jpg"), idx["tiles"]


def label_material(bpy, mats):
    if "labels" in mats:
        return mats["labels"]
    path, _tiles = label_sheet()
    m = bpy.data.materials.new("labels")
    m.use_nodes = True
    nt = m.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(path, check_existing=True)
    pr = nt.nodes["Principled BSDF"]
    nt.links.new(tex.outputs["Color"], pr.inputs["Base Color"])
    pr.inputs["Roughness"].default_value = 0.35
    mats["labels"] = m
    return m


def labelled_tin(bpy, x, y, z, r, h, uv, label_m, metal_m, facing_deg):
    """A tin with its printed label round it, the label's face toward facing_deg (the direction
    from the tin to whoever looks at it); its top and bottom bare metal. The label runs across
    the half of the tin that faces out and back again over the hidden half, so it has no seam."""
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=r, depth=h, location=(x, y, z + h / 2))
    o = bpy.context.object
    o.data.materials.append(label_m)
    o.data.materials.append(metal_m)
    me = o.data
    lay = me.uv_layers.active.data
    u0, v0, u1, v1 = uv
    for poly in me.polygons:
        if abs(poly.normal.z) > 0.5:
            poly.material_index = 1
            continue
        for li in poly.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            a = (math.atan2(co.y, co.x) / (2 * math.pi)) % 1.0
            uf = 1.0 - abs(2.0 * a - 1.0)
            vf = (co.z + h / 2) / h
            lay[li].uv = (u0 + uf * (u1 - u0), v0 + (0.04 + 0.92 * vf) * (v1 - v0))
    try:
        bpy.ops.object.shade_smooth_by_angle(angle=0.6)
    except Exception:
        pass
    o.rotation_euler = (0.0, 0.0, math.radians(facing_deg - 90.0))
    return o


def labelled_packet(bpy, x0, x1, y0, y1, z0, z1, uv, label_m, facing_deg):
    """A packet, its printed face toward facing_deg; its other faces take the label's ground."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    o = bpy.context.object
    o.scale = (max(x1 - x0, 1e-3), max(y1 - y0, 1e-3), max(z1 - z0, 1e-3))
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(label_m)
    me = o.data
    lay = me.uv_layers.active.data
    u0, v0, u1, v1 = uv
    nx, ny = math.cos(math.radians(facing_deg)), math.sin(math.radians(facing_deg))
    rx, ry = -ny, nx                         # the looker's right along the face
    w = abs(rx) * (x1 - x0) + abs(ry) * (y1 - y0)
    h = z1 - z0
    for poly in me.polygons:
        front = poly.normal.x * nx + poly.normal.y * ny > 0.9
        for li in poly.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            if front:
                sf = (co.x * rx + co.y * ry) / w + 0.5
                tf = co.z / h + 0.5
                lay[li].uv = (u0 + sf * (u1 - u0), v0 + tf * (v1 - v0))
            else:
                # a corner of the label's own ground colour
                lay[li].uv = (u0 + 0.04 * (u1 - u0), v0 + 0.95 * (v1 - v0))
    return o


def _export_material(m, tex_dir=None):
    """A room's material made plain enough for glTF: a colour multiplied by noise becomes its
    colour; a picture multiplied by a tint becomes a tinted copy of the picture (the glTF
    export drops the multiply: in Unreal the cream plaster came out grey and the lino grey,
    3 October); a picture laid by position is laid by the UVs the shell is given instead."""
    import bpy
    if m is None or not m.use_nodes:
        return
    nt = m.node_tree
    pr = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if pr is None:
        return
    bc = pr.inputs["Base Color"]
    if bc.is_linked:
        src = bc.links[0].from_node
        if src.type == "MIX_RGB" and not src.inputs["Color1"].is_linked:
            bc.default_value = src.inputs["Color1"].default_value
            nt.links.remove(bc.links[0])
        elif (src.type == "MIX_RGB" and src.blend_type == "MULTIPLY" and src.inputs["Color1"].is_linked
              and not src.inputs["Color2"].is_linked and tex_dir is not None
              and src.inputs["Color1"].links[0].from_node.type == "TEX_IMAGE"):
            img_node = src.inputs["Color1"].links[0].from_node
            tint = tuple(src.inputs["Color2"].default_value[:3])
            img = img_node.image
            w, h = img.size
            px = [0.0] * (w * h * 4)
            img.pixels.foreach_get(px)
            for i in range(0, len(px), 4):
                px[i] *= tint[0]
                px[i + 1] *= tint[1]
                px[i + 2] *= tint[2]
            name = "%s_tinted_%s" % (os.path.splitext(img.name)[0], m.name)
            out = bpy.data.images.new(name, w, h, alpha=False)
            out.pixels.foreach_set(px)
            os.makedirs(tex_dir, exist_ok=True)
            out.filepath_raw = os.path.join(tex_dir, name + ".png")
            out.file_format = "PNG"
            out.save()
            img_node.image = out
            nt.links.remove(bc.links[0])
            nt.links.new(img_node.outputs["Color"], bc)
    for n in nt.nodes:
        if n.type == "TEX_IMAGE" and n.inputs["Vector"].is_linked:
            tc = next((x for x in nt.nodes if x.type == "TEX_COORD"), None) or nt.nodes.new("ShaderNodeTexCoord")
            nt.links.remove(n.inputs["Vector"].links[0])
            nt.links.new(tc.outputs["UV"], n.inputs["Vector"])
            n.projection = "FLAT"
        if n.type in ("TEX_BRICK", "TEX_CHECKER", "TEX_NOISE", "TEX_WAVE") and n.outputs and n.outputs[0].is_linked:
            # a procedural pattern cannot travel: its first colour stands for it
            for link in list(n.outputs[0].links):
                if link.to_socket == bc:
                    nt.links.remove(link)
                    c1 = n.inputs.get("Color1")
                    if c1 is not None:
                        bc.default_value = c1.default_value


def export_room(bpy, sc, out_dir, shop_id):
    """THE ROOM AS REAL GEOMETRY, one glb a part: its floor, ceiling and three walls apart
    (Epic: a whole room in one mesh is not expected to work with Lumen) and its fittings in
    one; curves made meshes, every placed model freed of its parent, the shell given UVs in
    metres so its pictures tile as they did. tools/ue/import_shop_rooms.py brings them in."""
    import bmesh  # noqa: F401  (kept for the operators' context)
    os.makedirs(out_dir, exist_ok=True)
    for o in list(sc.objects):
        if o.type in ("FONT", "CURVE"):
            bpy.ops.object.select_all(action="DESELECT")
            o.select_set(True)
            bpy.context.view_layer.objects.active = o
            bpy.ops.object.convert(target="MESH")
    bpy.context.view_layer.update()
    meshes = [o for o in sc.objects if o.type == "MESH"]
    for o in meshes:
        mw = o.matrix_world.copy()
        o.parent = None
        o.matrix_world = mw
    for o in [o for o in sc.objects if o.type != "MESH"]:
        bpy.data.objects.remove(o, do_unlink=True)
    for m in bpy.data.materials:
        _export_material(m, os.path.join(os.environ.get("LEDGER_SCRATCH", "F:/LedgerTools/tmp/builder"), "rooms-tinted", shop_id))
    parts = {"floor": ("floor", "floor_slab", "boards"), "ceiling": ("ceiling",),
             "wall_left": ("wall_left",), "wall_right": ("wall_right",), "wall_back": ("wall_back",)}
    taken = set()
    groups = {}
    for part, names in parts.items():
        objs = [o for o in sc.objects if o.type == "MESH" and o.name.split(".")[0] in names]
        groups[part] = objs
        taken.update(objs)
    groups["fittings"] = [o for o in sc.objects if o.type == "MESH" and o not in taken]
    # THE PROPS' PICTURES AT 512 PX (4 October: Mickey's fittings reached 30 MB with Poly Haven's
    # 1k maps, over git's 25 MB a file); at a window's distance 512 reads the same
    for o in groups["fittings"]:
        for slot in o.material_slots:
            m = slot.material
            if m is None or not m.use_nodes:
                continue
            for n in m.node_tree.nodes:
                if n.type == "TEX_IMAGE" and n.image is not None and n.image.size[0] > 512:
                    w_, h_ = n.image.size
                    n.image.scale(512, max(1, int(512 * h_ / w_)))
    written = []
    for part, objs in groups.items():
        if not objs:
            continue
        bpy.ops.object.select_all(action="DESELECT")
        for o in objs:
            if o.data.users > 1:
                o.data = o.data.copy()
            o.select_set(True)
        bpy.context.view_layer.objects.active = objs[0]
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        if len(objs) > 1:
            bpy.ops.object.join()
        joined = bpy.context.view_layer.objects.active
        joined.name = "%s_%s" % (shop_id, part)
        if part != "fittings":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.uv.cube_project(cube_size=1.2 if part == "floor" else 1.5)
            bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")
        joined.select_set(True)
        path = os.path.join(out_dir, "%s.glb" % part)
        bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True,
                                  export_image_format="JPEG", export_apply=True)
        tris = sum(len(p.vertices) - 2 for p in joined.data.polygons)
        written.append("%s %d tris %.1f MB" % (part, tris, os.path.getsize(path) / 1e6))
    print("shop-room export: %s -> %s: %s" % (shop_id, out_dir, "; ".join(written)), flush=True)


# ------------------------------------------------- what more than one trade uses
def turn_and_settle(bpy, root, x, y, z, rot=(0.0, 0.0, 0.0), upright=False, flat=False):
    """Turn a placed model (z first, then y, then x) and stand it again with its bounds'
    centre at x, y and its lowest point at z. upright first stands its longest side on end
    (a broom, a torch), whichever way the model was built lying."""
    from mathutils import Vector

    def bounds():
        bpy.context.view_layer.update()
        pts = [o.matrix_world @ Vector(c) for o in root.children_recursive if o.type == "MESH" for c in o.bound_box]
        if not pts:
            return None, None
        return (Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts))),
                Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts))))
    root.rotation_mode = "ZYX"
    pre = (0.0, 0.0)
    if flat:
        # LAID ON ITS BROADEST SIDE, whichever way it was scanned (3 October: tools stood on
        # their tips in the ironmonger's window)
        root.rotation_euler = (0.0, 0.0, 0.0)
        lo, hi = bounds()
        if lo is not None:
            dx, dy, dz = hi.x - lo.x, hi.y - lo.y, hi.z - lo.z
            if dx < dy and dx < dz:
                pre = (0.0, math.pi / 2)
            elif dy < dx and dy < dz:
                pre = (math.pi / 2, 0.0)
    if upright:
        root.rotation_euler = (0.0, 0.0, 0.0)
        lo, hi = bounds()
        if lo is not None:
            dx, dy, dz = hi.x - lo.x, hi.y - lo.y, hi.z - lo.z
            if dx > dz and dx >= dy:
                pre = (0.0, math.pi / 2)
            elif dy > dz:
                pre = (math.pi / 2, 0.0)
    root.rotation_euler = (rot[0] + pre[0], rot[1] + pre[1], rot[2])
    lo, hi = bounds()
    if lo is None:
        return root
    root.location = root.location + Vector((x - (lo.x + hi.x) / 2, y - (lo.y + hi.y) / 2, z - lo.z))
    return root


def rope_coil(bpy, sc, name, x, y, z, r_in, r_out, layers, thick, m):
    """A rope coiled flat, as a chandler stacks it: a spiral out and in again a layer at a time,
    LAID FROM THREE STRANDS twisted round its path (3 October: one smooth tube read as garden
    hose to the fresh review); curves made a mesh, so the glTF carries it."""
    turns = max(1.0, (r_out - r_in) / (2.1 * thick))
    pitch = 3.4 * thick                      # one twist of the lay
    path = []
    a = 0.0
    for k in range(layers):
        length = 2.0 * math.pi * turns * (r_in + r_out) / 2.0
        n = max(60, int(length / (pitch / 5.0)))
        for i in range(n):
            t = i / float(n)
            r = r_in + (r_out - r_in) * (t if k % 2 == 0 else 1.0 - t)
            a += 2.0 * math.pi * turns / n
            path.append((x + r * math.cos(a), y + r * math.sin(a), z + thick + k * 1.9 * thick, a))
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = thick * 0.52
    cu.bevel_resolution = 1
    s_len = 0.0
    prev = None
    lens = []
    for (px, py, pz, pa) in path:
        if prev is not None:
            s_len += math.sqrt((px - prev[0]) ** 2 + (py - prev[1]) ** 2 + (pz - prev[2]) ** 2)
        lens.append(s_len)
        prev = (px, py, pz)
    d = thick * 0.48
    for strand in range(3):
        sp = cu.splines.new("POLY")
        sp.points.add(len(path) - 1)
        for pnt, (px, py, pz, pa), sl in zip(sp.points, path, lens):
            ph = 2.0 * math.pi * sl / pitch + 2.0 * math.pi * strand / 3.0
            rx, ry = math.cos(pa), math.sin(pa)
            pnt.co = (px + d * math.cos(ph) * rx, py + d * math.cos(ph) * ry, pz + d * math.sin(ph), 1.0)
    o = bpy.data.objects.new(name, cu)
    sc.collection.objects.link(o)
    o.data.materials.append(m)
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.convert(target="MESH")
    return bpy.context.view_layer.objects.active


def rope_hank(bpy, name, x, y, z, r, loops, thick, m, rnd):
    """A rope hung in a hank from a peg on a side wall: loops of about one size in the wall's
    plane, all hanging from the peg at z."""
    for k in range(loops):
        rr = r * (1.0 + rnd.uniform(-0.1, 0.1))
        bpy.ops.mesh.primitive_torus_add(major_radius=rr, minor_radius=thick, major_segments=32, minor_segments=6,
                                         location=(x + 0.012 * k * (1 if x < 0 else -1), y + rnd.uniform(-0.015, 0.015), z - rr),
                                         rotation=(0.0, math.pi / 2, 0.0))
        bpy.context.object.name = name
        bpy.context.object.data.materials.append(m)


def bucket(bpy, name, x, y, z, r_bot, r_top, h, m):
    """A galvanised bucket: an open tapered pail with a wall of its own thickness, a bottom and
    a rolled rim."""
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=r_bot, radius2=r_top, depth=h, end_fill_type="NOTHING",
                                    location=(x, y, z + h / 2))
    o = bpy.context.object
    o.name = name
    o.data.materials.append(m)
    sol = o.modifiers.new("wall", "SOLIDIFY")
    sol.thickness = 0.003
    bpy.ops.object.modifier_apply(modifier=sol.name)
    smooth_round(bpy)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=r_bot, depth=0.004, location=(x, y, z + 0.002))
    bpy.context.object.data.materials.append(m)
    bpy.ops.mesh.primitive_torus_add(major_radius=r_top, minor_radius=0.004, major_segments=24, minor_segments=6, location=(x, y, z + h))
    bpy.context.object.data.materials.append(m)
    return o


def smooth_round(bpy):
    """The active round piece smooth-shaded on its sides and sharp at its rims (3 October:
    twenty flat sides read as faceted plastic in the game)."""
    try:
        bpy.ops.object.shade_smooth_by_angle(angle=0.6)
    except Exception:
        bpy.ops.object.shade_smooth()


def tin_label(bpy, box, x, y, z, r, h, words, paper, ink):
    """A paint tin's printed label on its face toward the street: a paper panel and its words
    (3 October: plain coloured tins read as blocks to the fresh review). Fictional makers only."""
    panel = box("tin_label", x - r * 0.85, x + r * 0.85, y - r - 0.002, y - r + 0.004, z + h * 0.18, z + h * 0.86, paper)
    parts = [panel]
    for k, (body, size) in enumerate(words):
        bpy.ops.object.text_add(location=(x, y - r - 0.003, z + h * 0.66 - k * size * 1.3), rotation=(math.pi / 2, 0.0, 0.0))
        o = bpy.context.object
        o.data.body = body
        o.data.size = size
        o.data.align_x = "CENTER"
        o.data.materials.append(ink)
        bpy.ops.object.convert(target="MESH")
        parts.append(bpy.context.view_layer.objects.active)
    return parts


def paint_tin(bpy, x, y, z, r, h, label, lid):
    """A tin of paint: its printed body, and the metal rim and lid of a paint can."""
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=r, depth=h, location=(x, y, z + h / 2))
    smooth_round(bpy)
    bpy.context.object.data.materials.append(label)
    # the lid's band stands 3 mm proud of the body, so their tops never share a face (3 October:
    # flush, the two fought and the lids rendered black)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=r * 1.015, depth=h * 0.12, location=(x, y, z + h - h * 0.06 + 0.003))
    smooth_round(bpy)
    bpy.context.object.data.materials.append(lid)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=r * 1.015, depth=h * 0.08, location=(x, y, z + h * 0.04))
    smooth_round(bpy)
    bpy.context.object.data.materials.append(lid)


def standing_card(bpy, sc, box, cx, cy, w, h, lines, inkm, cardm, lean=0.1, z0=0.0):
    """A card stood in a window, read from the pavement: its lines of lettering, leaned back
    against a prop at its foot, as the pawnbroker's notices stand."""
    parts = [box("card", cx - w / 2, cx + w / 2, cy - 0.002, cy + 0.002, z0, z0 + h, cardm)]
    top = z0 + h - 0.02
    for body, size in lines:
        bpy.ops.object.text_add(location=(cx, cy - 0.0035, top - size * 0.8), rotation=(math.pi / 2, 0.0, 0.0))
        o = bpy.context.object
        o.data.body = body
        o.data.size = size
        o.data.align_x = "CENTER"
        o.data.materials.append(inkm)
        bpy.ops.object.convert(target="MESH")
        parts.append(bpy.context.object)
        top -= size * 1.35
    return tilt_join(bpy, parts, (cx, cy, z0), -lean)


def photo_plane(bpy, name, x0, x1, y, z0, z1, image_rel, crop):
    """A printed picture facing the street (a magazine's cover photograph): a plane whose corners
    take the crop (u0, v0, u1, v1) of one of our own pictures in the repository, so the glTF
    carries the whole image and the crop in its UVs (3 October: blank panels read as placeholders)."""
    path = os.path.join(REPO, image_rel)
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=((x0 + x1) / 2, y, (z0 + z1) / 2), rotation=(math.pi / 2, 0.0, 0.0))
    o = bpy.context.object
    o.name = name
    o.scale = (x1 - x0, z1 - z0, 1.0)
    u0, v0, u1, v1 = crop
    uv = o.data.uv_layers.active.data
    for loop in o.data.loops:
        co = o.data.vertices[loop.vertex_index].co
        uv[loop.index].uv = (u0 if co.x < 0 else u1, v0 if co.y < 0 else v1)
    key = "photo_" + os.path.basename(image_rel)
    m = bpy.data.materials.get(key)
    if m is None:
        m = bpy.data.materials.new(key)
        m.use_nodes = True
        nt = m.node_tree
        pr = nt.nodes["Principled BSDF"]
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(path, check_existing=True)
        nt.links.new(tex.outputs["Color"], pr.inputs["Base Color"])
        pr.inputs["Roughness"].default_value = 0.3
    o.data.materials.append(m)
    return o


def tilt_join(bpy, parts, pivot, rx, rz=0.0):
    """Join the parts into one piece and turn it about a point (a card about its foot).
    3 October: parenting them to a new empty, as the pawnbroker's notices were, read the
    empty's place before Blender had worked it out, so every piece landed shifted by it:
    the notices outside the window, a chocolate box's ribbon a gold sheet across it."""
    bpy.ops.object.select_all(action="DESELECT")
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    if len(parts) > 1:
        bpy.ops.object.join()
    o = bpy.context.view_layer.objects.active
    bpy.context.scene.cursor.location = pivot
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    o.rotation_euler = (rx, 0.0, rz)
    return o


def flat_tag(bpy, box, ticket, ink, x, y, z, price, turn=0.0):
    """A price ticket stood by its piece, leaned back, the price inked on it (3 October: laid
    flat on the bed, the fresh review saw no tickets at all from the pavement)."""
    t = box("tag", x - 0.036, x + 0.036, y - 0.022, y + 0.022, z, z + 0.0015, ticket)
    bpy.ops.object.text_add(location=(x, y - 0.009, z + 0.0016))
    o = bpy.context.object
    o.data.body = price
    o.data.size = 0.022
    o.data.align_x = "CENTER"
    o.data.materials.append(ink)
    bpy.ops.object.convert(target="MESH")
    tilt_join(bpy, [t, bpy.context.view_layer.objects.active], (x, y - 0.022, z), 1.2, turn * 0.3)


def placed(bpy, model, asset, x, y, z, rot=(0.0, 0.0, 0.0), size=None, upright=False, flat=False):
    root = model(asset, 0.0, 0.0, 0.0, size=size)
    if root is None:
        return None
    return turn_and_settle(bpy, root, x, y, z, rot, upright, flat)


def newsagent_display(bpy, sc, mat, box, model, L, Dp, rnd):
    """A NEWSAGENT'S WINDOW (V1, 3 October): the cards in the window, small ads handwritten on
    postcards in rows on a board at the left; jars of sweets on a step, boxes of chocolates
    stood on end, and the week's magazines fanned on the bed. Nothing for children, nothing of
    gambling (canon)."""
    box("bed", -L / 2, L / 2, 0.0, Dp, -0.02, 0.0, mat("bed_board", (0.20, 0.13, 0.08), rough=0.7))
    box("crepe", -L / 2 + 0.01, L / 2 - 0.01, 0.01, Dp - 0.01, 0.0, 0.004, mat("crepe_faded_blue", (0.16, 0.24, 0.36), rough=0.9))
    ink = mat("biro_blue", (0.04, 0.06, 0.25), rough=0.8)
    ink_black = mat("ink_black", (0.04, 0.04, 0.05), rough=0.8)
    cork = mat("ads_board", (0.36, 0.25, 0.14), rough=0.85)
    bx0, bx1 = -L / 2 + 0.03, -L / 2 + 1.45
    box("ads_board", bx0, bx1, Dp - 0.06, Dp - 0.04, 0.0, 0.8, cork)
    cards = [mat("postcard_white", (0.86, 0.85, 0.80), rough=0.85), mat("postcard_cream", (0.84, 0.78, 0.60), rough=0.85),
             mat("postcard_blue", (0.62, 0.72, 0.80), rough=0.85), mat("postcard_yellow", (0.86, 0.80, 0.45), rough=0.85),
             mat("postcard_pink", (0.84, 0.66, 0.66), rough=0.85)]
    ads = [("SETTEE FOR SALE", "£40  ring 4417"), ("ROOM TO LET", "apply within"), ("WINDOW CLEANER", "reliable  6631"),
           ("LOST GREY CAT", "reward  2290"), ("TYPING DONE", "ring 5108"), ("BIKE FOR SALE", "£25 ono"),
           ("CARPET 12 x 9", "£30  ring 3374"), ("SEWING MACHINE", "£15  7712"), ("DRIVING LESSONS", "ring 4059"),
           ("TV REPAIRS", "no call-out fee"), ("WANTED", "old records"), ("IRONING DONE", "ring 2846"),
           ("GARAGE TO RENT", "ring 6018"), ("FRIDGE FREEZER", "£50  3391"), ("PIANO LESSONS", "ring 5527"),
           ("ODD JOBS", "no job too small"), ("WARDROBE", "£20  ring 1185"), ("ROOM WANTED", "quiet man"),
           ("GAS COOKER", "£35  4470"), ("CHIMNEY SWEEP", "ring 2963")]
    order = ads[:]
    rnd.shuffle(order)
    k = 0
    cw, ch = 0.127, 0.076
    for row in range(7):
        z = 0.14 + row * 0.094
        x = bx0 + 0.03 + rnd.uniform(0.0, 0.02)
        while x + cw < bx1 - 0.02:
            c = box("postcard", x, x + cw, Dp - 0.064, Dp - 0.061, z, z + ch, cards[rnd.randrange(len(cards))])
            c.rotation_euler = (0.0, rnd.uniform(-0.04, 0.04), 0.0)
            a, b = order[k % len(order)]
            k += 1
            for body, size, dz in ((a, 0.0105, 0.048), (b, 0.009, 0.02)):
                bpy.ops.object.text_add(location=(x + cw / 2, Dp - 0.0655, z + dz), rotation=(math.pi / 2, 0.0, 0.0))
                o = bpy.context.object
                o.data.body = body
                o.data.size = size
                o.data.align_x = "CENTER"
                o.data.materials.append(ink)
                bpy.ops.object.convert(target="MESH")
            x += cw + rnd.uniform(0.008, 0.02)
    standing_card(bpy, sc, box, bx0 + 0.32, Dp - 0.12, 0.5, 0.1, [("CARDS IN THIS WINDOW", 0.026), ("20p a week", 0.022)],
                  ink_black, cards[0], lean=0.05)
    # THE RIGHT OF THE WINDOW (the second pass, 3 October, after the fresh review: jars with no
    # sweets, plain slabs for chocolates, flat cards for magazines): the week's magazines stood on
    # a step with their titles and cover lines, boxes of chocolates on end before them with their
    # lids lettered. Every title and maker is made up; nothing for children, of drink or gambling.
    # (No sweet jars here: the room behind shows them in real glass, filled.)
    sx0 = bx1 + 0.05
    step = mat("step_crepe", (0.30, 0.10, 0.10), rough=0.9)
    box("step", sx0, L / 2 - 0.03, 0.3, Dp - 0.03, 0.0, 0.16, step)
    white_ink = mat("ink_white", (0.92, 0.91, 0.86), rough=0.6)
    gold_ink = mat("ink_gold", (0.78, 0.60, 0.22), rough=0.35, metal=0.7)

    def lettering(parts, lines, cx, y, top, m, gap=1.3):
        for body, size in lines:
            bpy.ops.object.text_add(location=(cx, y, top - size), rotation=(math.pi / 2, 0.0, 0.0))
            o = bpy.context.object
            o.data.body = body
            o.data.size = size
            o.data.align_x = "CENTER"
            o.data.materials.append(m)
            bpy.ops.object.convert(target="MESH")
            parts.append(bpy.context.view_layer.objects.active)
            top -= size * gap

    # EACH COVER'S PHOTOGRAPH IS A REAL ONE (Poly Haven's photographed places, CC0;
    # production/assets/shop-displays/photos/source.json): crops of our own frames read as
    # debug to the second fresh review, 3 October
    ph = "production/assets/shop-displays/photos/"
    mid = (0.15, 0.0, 0.85, 1.0)
    mags = [("HOME & HEARTH", (0.62, 0.12, 0.10), ["SPRING ISSUE", "40 IDEAS FOR LESS"], ph + "garden_nook.jpg", mid),
            ("PRACTICAL DIY", (0.08, 0.16, 0.36), ["SHELVES IN A DAY", "TOOLS ON TEST"], ph + "carpentry_shop_01.jpg", mid),
            ("WOMAN'S WEEK", (0.70, 0.40, 0.48), ["KNITTING PATTERN", "ROSES IN BLOOM"], ph + "sunny_rose_garden.jpg", mid),
            ("OUT & ABOUT", (0.16, 0.30, 0.14), ["WALKS ON THE COAST", "AUTUMN DAYS"], ph + "white_cliff_top.jpg", mid),
            ("TIDE & LINE", (0.10, 0.28, 0.36), ["SEA ANGLING", "WINTER COD"], ph + "small_harbour_morning.jpg", mid),
            ("TELEVISION WEEK", (0.80, 0.70, 0.20), ["ALL THE CHANNELS", "AT THE PICTURES"], ph + "cinema_hall.jpg", mid)]
    mx = sx0 + 0.14
    for k, (title, colour, lines, pic, crop) in enumerate(mags):
        if mx > L / 2 - 0.12:
            break
        cover = mat("cover_%d" % k, colour, rough=0.25)
        yb = 0.44
        parts = [box("magazine", mx - 0.105, mx + 0.105, yb, yb + 0.006, 0.16, 0.45, cover),
                 photo_plane(bpy, "mag_photo", mx - 0.095, mx + 0.095, yb - 0.0008, 0.17, 0.38, pic, crop)]
        # dark lettering on a pale cover, white on a dark one (white on pink and yellow could not be read)
        ink_k = white_ink if sum(colour) < 1.4 else mat("ink_dark", (0.06, 0.05, 0.08), rough=0.6)
        lettering(parts, [(title, 0.022)], mx, yb - 0.002, 0.44, ink_k)
        lettering(parts, [(lines[0], 0.012), (lines[1], 0.012)], mx, yb - 0.0025, 0.37, ink_k, gap=1.5)
        tilt_join(bpy, parts, (mx, yb, 0.16), -0.22, rnd.uniform(-0.05, 0.05))
        mx += 0.235
    boxes = [("ASSORTED", "Chocolates", (0.20, 0.04, 0.26)), ("DELUXE", "Selection", (0.42, 0.04, 0.06)),
             ("MINT", "Creams", (0.05, 0.20, 0.12)), ("DAIRY", "Fudge", (0.40, 0.24, 0.08)),
             ("ASSORTED", "Toffees", (0.05, 0.08, 0.24))]
    x = sx0 + 0.04
    for k, (a, b, colour) in enumerate(boxes):
        w = rnd.uniform(0.24, 0.3)
        if x + w > L / 2 - 0.05:
            break
        lid = mat("choc_lid_%d" % k, colour, rough=0.3)
        parts = [box("choc_box", x, x + w, 0.2, 0.235, 0.0, 0.18, lid),
                 box("choc_ribbon", x + w * 0.78, x + w * 0.83, 0.198, 0.2, 0.0, 0.18, gold_ink)]
        lettering(parts, [(a, 0.024), (b, 0.02)], x + w * 0.42, 0.197, 0.145, gold_ink, gap=1.4)
        tilt_join(bpy, parts, (x + w / 2, 0.235, 0.0), -0.25, rnd.uniform(-0.08, 0.08))
        x += w + 0.04


def ironmonger_display(bpy, sc, mat, box, model, L, Dp, rnd):
    """AN IRONMONGER'S WINDOW (V1, 3 October), crowded as they were: galvanised buckets and
    brooms at the back, paint in a pyramid of tins, a watering can, oil cans, a blowtorch and
    light bulbs on the step, hand tools laid in rows at the front, each ticketed; the card that
    every ironmonger's had: keys cut while you wait."""
    box("bed", -L / 2, L / 2, 0.0, Dp, -0.02, 0.0, mat("bed_boards", (0.22, 0.14, 0.08), rough=0.75))
    galv = mat("galvanised", (0.55, 0.56, 0.56), rough=0.45, metal=1.0)
    ticket = mat("ticket", (0.86, 0.84, 0.76), rough=0.85)
    ink = mat("ticket_ink", (0.04, 0.04, 0.10), rough=0.8)
    # THE STEP takes the back half of the bed, deep enough for a bucket (3 October: the buckets
    # stood half in a shallow step, one in the tins, and the brooms stood in a bucket)
    box("step", -L / 2 + 0.03, L / 2 - 0.03, 0.22, Dp - 0.01, 0.0, 0.12, mat("step_board", (0.26, 0.17, 0.10), rough=0.7))
    # on it, left to right: the tins, two buckets (one nested), the brooms, the cans, the jerrycan
    for (bx_, nested) in ((-0.72, True), (-0.36, False)):
        bucket(bpy, "bucket", bx_, 0.39, 0.12, 0.11, 0.15, 0.27, galv)
        if nested:
            bucket(bpy, "bucket_nested", bx_, 0.39, 0.17, 0.105, 0.145, 0.26, galv)
    # (no brooms in the window: stood on the step they leaned on nothing, the fresh review)
    placed(bpy, model, "metal_jerrycan", L / 2 - 0.2, 0.4, 0.12, rot=(0.0, 0.0, 0.2), size=0.36)
    # on the step: a pyramid of paint tins, the watering can, oil, the blowtorch, bulbs, cleaners
    tins = [mat("tin_white", (0.80, 0.78, 0.72), rough=0.4), mat("tin_red", (0.55, 0.08, 0.06), rough=0.4),
            mat("tin_blue", (0.10, 0.20, 0.42), rough=0.4), mat("tin_green", (0.18, 0.34, 0.18), rough=0.4)]
    lidm = mat("tin_metal", (0.62, 0.62, 0.60), rough=0.35, metal=1.0)
    r, h = 0.07, 0.09
    paper = mat("tin_paper", (0.86, 0.84, 0.78), rough=0.7)
    tin_ink = mat("tin_ink", (0.06, 0.06, 0.10), rough=0.7)
    words = [[("HALDEN", 0.013), ("GLOSS", 0.016)], [("HALDEN", 0.013), ("EMULSION", 0.012)],
             [("BRILLIANT", 0.011), ("WHITE", 0.016)], [("UNDERCOAT", 0.011), ("2½ LTR", 0.011)]]
    for tier, n in enumerate((4, 3, 2, 1)):
        for j in range(n):
            px = -L / 2 + 0.15 + (j + tier * 0.5) * 2 * r
            paint_tin(bpy, px, 0.39, 0.12 + tier * h, r, h, tins[(tier + j) % len(tins)], lidm)
            tin_label(bpy, box, px, 0.39, 0.12 + tier * h, r, h, words[(tier + j) % len(words)], paper, tin_ink)
    # (no cleaner bottles or spray: their scanned labels echo real products, the fresh review)
    for a, x, sz in (("small_oil_can_01", 0.22, 0.18), ("oil_tin", 0.4, 0.17), ("brass_blowtorch", 0.6, 0.22),
                     ("metal_jug", 0.8, 0.2), ("pot_enamel_01", 1.02, 0.22), ("watering_can_metal_01", 1.27, 0.3)):
        if x < L / 2 - 0.1:
            placed(bpy, model, a, x, 0.38, 0.12, rot=(0.0, 0.0, rnd.uniform(-0.4, 0.4)), size=sz)
    # the front: hand tools laid in rows, each with its ticket
    prices = ["99p", "£1.20", "£1.49", "£1.99", "£2.50", "£2.99", "£3.49", "£4.99", "75p", "£5.99"]
    front = [("adjustable_wrench", 0.2), ("pliers", 0.18), ("screwdriver", 0.2), ("cross_pein_hammer", 0.28),
             ("combination_wrench", 0.2), ("handsaw_wood", 0.55), ("flathead_screwdriver", 0.2), ("tongue_groove_pliers", 0.22),
             ("measuring_tape_01", 0.08), ("wooden_hammer_01", 0.28), ("trowel_01", 0.24), ("mousetrap", 0.1),
             ("vintage_hand_drill", 0.32), ("garden_gloves_01", 0.2), ("lightbulb_01", 0.1), ("lightbulb_01", 0.1)]
    x = -L / 2 + 0.08
    for a, sz in front:
        foot = sz * 0.7 if sz > 0.15 else sz + 0.02
        if x + foot > L / 2 - 0.06:
            break
        placed(bpy, model, a, x + foot / 2, 0.14, 0.0, rot=(0.0, 0.0, math.pi / 2 + rnd.uniform(-0.35, 0.35)), size=sz, flat=True)
        flat_tag(bpy, box, ticket, ink, x + foot / 2, 0.035, 0.0, prices[rnd.randrange(len(prices))], rnd.uniform(-0.3, 0.3))
        x += foot + rnd.uniform(0.02, 0.05)
    standing_card(bpy, sc, box, L / 2 - 0.45, 0.03, 0.42, 0.2, [("KEYS CUT", 0.055), ("while you wait", 0.03)],
                  mat("card_ink", (0.45, 0.04, 0.03), rough=0.8), mat("card_yellowed", (0.82, 0.74, 0.52), rough=0.85), lean=0.12)


def tea_room_display(bpy, sc, mat, box, model, L, Dp, rnd):
    """A TEA ROOM'S WINDOW (V1, 3 October): on a white cloth, a cake on a china stand at each
    side, a three-tier stand of small cakes between them, scones and croissants on plates, a
    teapot and cups, a plant at each end, and the menu card on its little easel."""
    box("bed", -L / 2, L / 2, 0.0, Dp, -0.02, 0.0, mat("bed_board", (0.20, 0.13, 0.08), rough=0.7))
    cloth = mat("cloth_white", (0.84, 0.83, 0.79), rough=0.85)
    box("cloth", -L / 2 + 0.01, L / 2 - 0.01, 0.01, Dp - 0.01, 0.0, 0.004, cloth)
    box("step", -L / 2 + 0.04, L / 2 - 0.04, 0.3, Dp - 0.04, 0.0, 0.13, cloth)
    china = mat("china", (0.88, 0.87, 0.84), rough=0.2)
    doily = mat("doily", (0.92, 0.91, 0.88), rough=0.9)

    def disc(x, y, z, r, h, m):
        bpy.ops.mesh.primitive_cylinder_add(vertices=28, radius=r, depth=h, location=(x, y, z + h / 2))
        bpy.context.object.data.materials.append(m)

    def stand(x, y, z, r):
        disc(x, y, z, 0.05, 0.012, china)
        disc(x, y, z + 0.012, 0.018, 0.09, china)
        disc(x, y, z + 0.1, r, 0.012, china)
        disc(x, y, z + 0.112, r * 0.85, 0.002, doily)
        return z + 0.114
    top = stand(-0.75, 0.42, 0.13, 0.15)
    model("carrot_cake", -0.75, 0.42, top, turn=0.3, size=0.24)
    top = stand(0.75, 0.42, 0.13, 0.15)
    model("strawberry_chocolate_cake", 0.75, 0.42, top, turn=-0.4, size=0.24)
    # THE THREE-TIER STAND, its tiers piled with scanned buns and croissants (Poly Haven, CC0;
    # 3 October: the first pass's iced pucks read as toys to the fresh review)
    disc(0.0, 0.42, 0.13, 0.008, 0.35, china)      # the pole ends at the top tier
    for tier, (z, r) in enumerate(((0.14, 0.17), (0.3, 0.13), (0.46, 0.09))):
        disc(0.0, 0.42, z, r, 0.01, china)
        n = 5 if tier == 0 else (4 if tier == 1 else 2)
        for j in range(n):
            a = 2 * math.pi * j / n + tier
            cx, cy = 0.0 + (r - 0.045) * math.cos(a), 0.42 + (r - 0.045) * math.sin(a)
            model("croissant", cx, cy, z + 0.01, turn=a + math.pi / 2, size=(0.09, 0.08, 0.07)[tier])
    # (no buns or scones: the scanned buns are drawn see-through and only their seeds came in;
    # the Megascans tea cake and breads wait on his Fab library, the goods research)
    # a third cake at the front left, on a plate
    disc(-0.35, 0.16, 0.0, 0.13, 0.012, china)
    model("carrot_cake", -0.35, 0.16, 0.012, turn=2.1, size=0.2)
    disc(0.35, 0.16, 0.0, 0.12, 0.012, china)
    placed(bpy, model, "jug_01", 0.62, 0.42, 0.13, rot=(0.0, 0.0, 2.6), size=0.16)
    for j in range(4):
        model("croissant", 0.35 + (j % 2) * 0.09 - 0.045, 0.16 + (j // 2) * 0.08 - 0.04, 0.012, turn=rnd.uniform(0, 3), size=0.11)
    # (no tea set: the scanned set is silver, and read as small silver bowls)
    for x, a in ((-L / 2 + 0.16, "potted_plant_01"), (L / 2 - 0.16, "potted_plant_02")):
        placed(bpy, model, a, x, 0.4, 0.13, size=0.42)
    standing_card(bpy, sc, box, 1.25, 0.12, 0.3, 0.26,
                  [("TEAS", 0.04), ("COFFEES", 0.03), ("LIGHT LUNCHES", 0.025), ("HOME BAKING", 0.025)],
                  mat("menu_ink", (0.10, 0.18, 0.12), rough=0.8), mat("menu_card", (0.86, 0.82, 0.70), rough=0.85), lean=0.2)


def chandler_display(bpy, sc, mat, box, model, L, Dp, rnd):
    """A SHIP CHANDLER'S WINDOW (V1, 3 October): ropes in flat coils of four colours, a lifebuoy
    leaned at the back, a brass lamp and a compass, sea boots and an oilskin hat, a signal lamp,
    oil, a coil of galvanised chain, tins of marine varnish, each ticketed."""
    box("bed", -L / 2, L / 2, 0.0, Dp, -0.02, 0.0, mat("bed_boards", (0.18, 0.12, 0.07), rough=0.75))
    box("step", -L / 2 + 0.03, L / 2 - 0.03, 0.3, Dp - 0.03, 0.0, 0.12, mat("step_navy", (0.05, 0.07, 0.14), rough=0.8))
    ticket = mat("ticket", (0.86, 0.84, 0.76), rough=0.85)
    ink = mat("ticket_ink", (0.04, 0.04, 0.10), rough=0.8)
    ropes = [mat("rope_manila", (0.55, 0.42, 0.25), rough=0.9), mat("rope_white", (0.78, 0.77, 0.72), rough=0.85),
             mat("rope_blue", (0.08, 0.18, 0.45), rough=0.8), mat("rope_orange", (0.80, 0.35, 0.06), rough=0.8)]
    prices = ["£2.40", "£3.95", "£6.50", "£1.80", "£12.50", "£4.75", "£8.99", "£19.50"]
    for k, (x, y, r, layers) in enumerate(((-1.35, 0.16, 0.13, 3), (-0.95, 0.15, 0.11, 2), (0.15, 0.15, 0.12, 4), (1.0, 0.16, 0.13, 3))):
        rope_coil(bpy, sc, "coil", x, y, 0.0, 0.03, r, layers, 0.009 + 0.002 * (k % 2), ropes[k % len(ropes)])
        flat_tag(bpy, box, ticket, ink, x + 0.04, y - r - 0.03 + 0.04, 0.0, prices[k], 0.1)
    # the lifebuoy stands upright as made, leaned a little back (tipped 1.35 it lay flat and
    # reached through into the room, 3 October)
    placed(bpy, model, "lifebuoy", -0.35, Dp - 0.12, 0.12, rot=(-0.15, 0.0, 0.0), size=0.6)
    placed(bpy, model, "Lantern_01", -1.4, 0.43, 0.12, rot=(0.0, 0.0, 0.3), size=0.32)
    placed(bpy, model, "seadogs_compass", -0.45, 0.13, 0.0, rot=(0.0, 0.0, 0.2), size=0.15)
    placed(bpy, model, "rubber_boots", 0.55, 0.38, 0.12, rot=(0.0, 0.0, math.pi / 2 + 0.2), size=0.4)
    placed(bpy, model, "metal_jerrycan", 0.95, 0.43, 0.12, rot=(0.0, 0.0, 0.5), size=0.3)
    for (tx, ty, tz, price) in ((-1.4, 0.3, 0.12, "£6.95"), (-0.45, 0.04, 0.0, "£14.50"), (0.55, 0.26, 0.12, "£8.99"),
                                (0.5, 0.03, 0.0, "£4.25"), (1.38, 0.3, 0.12, "£1.20"), (0.95, 0.3, 0.12, "£3.50")):
        flat_tag(bpy, box, ticket, ink, tx + 0.08, ty, tz, price, 0.1)
    placed(bpy, model, "signal_flashlight", 0.5, 0.13, 0.0, rot=(0.0, 0.0, 0.9), size=0.2)
    placed(bpy, model, "small_oil_can_01", 1.38, 0.42, 0.12, rot=(0.0, 0.0, -0.3), size=0.2)
    placed(bpy, model, "ocean_buoy", L / 2 - 0.2, 0.42, 0.12, rot=(0.0, 0.0, 0.2), size=0.4)
    # a heap of galvanised chain, link through link
    galv = mat("chain_galvanised", (0.55, 0.56, 0.56), rough=0.45, metal=1.0)
    a = 0.0
    for j in range(40):
        a += 0.42
        rr = 0.03 + 0.0025 * j
        cx, cy = -0.85 + rr * math.cos(a), 0.42 + rr * math.sin(a) * 0.8
        bpy.ops.mesh.primitive_torus_add(major_radius=0.016, minor_radius=0.004, major_segments=12, minor_segments=5,
                                         location=(cx, cy, 0.12 + 0.006 + 0.004 * (j % 3)),
                                         rotation=(math.pi / 2 if j % 2 else 0.0, 0.0, a + math.pi / 2))
        bpy.context.object.data.materials.append(galv)
    tins = [mat("varnish_tin", (0.45, 0.26, 0.08), rough=0.4), mat("antifoul_tin", (0.40, 0.06, 0.05), rough=0.4),
            mat("deck_tin", (0.70, 0.70, 0.66), rough=0.4)]
    lidm = mat("tin_metal", (0.62, 0.62, 0.60), rough=0.35, metal=1.0)
    r, h = 0.06, 0.08
    paper = mat("tin_paper", (0.86, 0.84, 0.78), rough=0.7)
    tin_ink = mat("tin_ink", (0.06, 0.06, 0.10), rough=0.7)
    words = [[("YACHT", 0.012), ("VARNISH", 0.012)], [("ANTIFOUL", 0.011), ("RED", 0.014)], [("DECK", 0.013), ("PAINT", 0.013)]]
    for tier, n in enumerate((3, 2, 1)):
        for j in range(n):
            tx = 0.0 + (j + tier * 0.5) * 2 * r
            paint_tin(bpy, tx, 0.42, 0.12 + tier * h, r, h, tins[(tier + j) % len(tins)], lidm)
            tin_label(bpy, box, tx, 0.42, 0.12 + tier * h, r, h, words[(tier + j) % len(words)], paper, tin_ink)
    standing_card(bpy, sc, box, 1.3, 0.03, 0.36, 0.2, [("ROPES  CHAINS", 0.032), ("PAINTS  OILSKINS", 0.032), ("BOOTS", 0.032)],
                  mat("card_ink", (0.05, 0.08, 0.25), rough=0.8), mat("card_white", (0.86, 0.85, 0.80), rough=0.85), lean=0.12)


# ------------------------------------------------------- the window display
def grocer_display(bpy, sc, mat, box, model, L, Dp, rnd):
    """A GROCER'S WINDOW (V1, 3 October; the second pass after the fresh review: "it reads as a
    toy shop", the produce primitive shapes on boards): scanned fruit and vegetables (Poly
    Haven, CC0), heaped two deep in slatted crates on green display grass, each kind in its own
    crate, every piece turned, sized and tilted on its own, a price card stood in each; the
    research (production/research/shop-window-interiors/GOODS-2026-10-03.md): piles are scans,
    varied, never one copy repeated in step."""
    import math
    grass = mat("display_grass", (0.05, 0.17, 0.04), rough=0.9)
    box("bed", -L / 2, L / 2, 0.0, Dp, -0.02, 0.0, grass)
    box("step", -L / 2 + 0.03, L / 2 - 0.03, 0.28, Dp - 0.02, 0.0, 0.14, grass)
    wood = mat("crate_wood", (0.30, 0.22, 0.13), rough=0.9)      # weathered, not new deal
    wood_dark = mat("crate_wood_dark", (0.22, 0.16, 0.10), rough=0.9)
    card = mat("price_card", (0.93, 0.90, 0.75), rough=0.85)
    ink = mat("price_ink", (0.05, 0.05, 0.08), rough=0.8)

    def crate(x0, x1, y0, y1, z0):
        """A shallow slatted fruit crate: two ends, a slatted floor and slatted sides."""
        h = 0.09
        for xe in (x0, x1 - 0.015):
            box("crate_end", xe, xe + 0.015, y0, y1, z0, z0 + h, wood_dark)
        n = 4
        for k in range(n):
            ya = y0 + k * (y1 - y0) / n + 0.004
            box("crate_floor", x0, x1, ya, ya + (y1 - y0) / n - 0.008, z0, z0 + 0.008, wood)
        for yy in (y0, y1 - 0.008):
            for zz in (z0 + 0.01, z0 + 0.055):
                box("crate_side", x0, x1, yy, yy + 0.008, zz, zz + 0.03, wood)

    # (label, price, scan, its size in metres, how many deep)
    produce = [("APPLES", "45p lb", "food_apple_01", 0.085, 2), ("LEMONS", "12p each", "lemon", 0.075, 2),
               ("BANANAS", "39p lb", "bananas", 0.34, 1), ("ONIONS", "25p lb", "yellow_onion", 0.075, 2),
               ("KIWI FRUIT", "10p each", "food_kiwi_01", 0.07, 2), ("LIMES", "15p each", "food_lime_01", 0.065, 2),
               ("AVOCADOS", "35p each", "food_avocado_01", 0.1, 1), ("APPLES", "Cookers 38p lb", "food_apple_01", 0.095, 2)]
    per_row = 4
    w = (L - 0.1) / per_row
    for k, (label, price, asset, size, deep) in enumerate(produce):
        row = k // per_row
        xc = -L / 2 + 0.05 + (k % per_row) * w + w / 2
        y0, y1, z0 = (0.02, 0.26, 0.0) if row == 0 else (0.30, 0.52, 0.14)
        crate(xc - w / 2 + 0.03, xc + w / 2 - 0.03, y0, y1, z0)
        if asset == "bananas":
            # HANDS OF BANANAS laid over each other the length of the crate (the first pass laid
            # four apart and they read as scattered)
            for j in range(7):
                # laid along the crate and kept inside it (loose ones lay on the grass, the review)
                model(asset, xc - w / 2 + 0.17 + j * (w - 0.34) / 6,
                      (y0 + y1) / 2 + rnd.uniform(-0.015, 0.015), z0 + 0.01 + (j % 2) * 0.025,
                      turn=rnd.uniform(-0.15, 0.15) + (math.pi if j % 2 else 0.0), size=size * 0.8 * rnd.uniform(0.92, 1.0),
                      tilt=rnd.uniform(-0.1, 0.1))
        else:
            # HEAPED, three deep and close (the first pass left each crate half bare): every
            # layer set on the gaps of the one below
            step = size * 0.9
            cols = max(1, int((w - 0.08) / step))
            rows = max(2, int((y1 - y0 - 0.02) / step) + 1)
            for layer in range(deep + 1):
                off = step / 2 * layer
                for i in range(cols - layer):
                    for j in range(rows - layer):
                        if layer == 2 and rnd.random() < 0.4:
                            continue
                        px = xc - w / 2 + 0.05 + off + i * step + step / 2 + rnd.uniform(-0.01, 0.01)
                        py = y0 + 0.012 + off + j * step + step / 2 + rnd.uniform(-0.01, 0.01)
                        py = min(py, y1 - size / 2)
                        model(asset, px, py, z0 + 0.008 + layer * size * 0.55, turn=rnd.uniform(0, 2 * math.pi),
                              size=size * rnd.uniform(0.88, 1.08), tilt=rnd.uniform(-0.5, 0.5))
        # its price card, stood in the crate's front corner
        cx = xc - w / 2 + 0.16
        cz = z0 + 0.09
        for body, sz, dz, m in ((None, 0, 0, card), (label, 0.017, 0.05, ink), (price, 0.02, 0.018, ink)):
            if body is None:
                box("price_card", cx - 0.07, cx + 0.07, y0 - 0.004, y0 - 0.001, cz, cz + 0.08, card)
                continue
            bpy.ops.object.text_add(location=(cx, y0 - 0.005, cz + dz), rotation=(math.pi / 2, 0.0, 0.0))
            o = bpy.context.object
            o.data.body = body
            o.data.size = sz
            o.data.align_x = "CENTER"
            o.data.materials.append(m)
            bpy.ops.object.convert(target="MESH")


def launderette_display(bpy, sc, mat, box, model, L, Dp, rnd):
    """A LAUNDERETTE'S WINDOW (V1, 3 October): mostly clear, to see the machines; on the bed a
    wicker basket of folded towels and sheets, a plant at each end, and cards stood against the
    glass: SERVICE WASHES and the opening hours. The second pass (3 October, filmed in the game):
    the laundry was five flat slabs on a blue box and the plant a ring of green strips, so the
    basket and the plants are Poly Haven's (CC0) and the folds are rounded, uneven and soft."""
    import math
    box("bed", -L / 2, L / 2, 0.0, Dp, -0.02, 0.0, mat("bed_lino", (0.30, 0.27, 0.22), rough=0.6))
    bx = L / 2 - 0.42
    placed(bpy, model, "wicker_basket_01", bx, 0.32, 0.0, rot=(0.0, 0.0, 0.15), size=0.5)
    cloths = [(0.80, 0.79, 0.74), (0.58, 0.20, 0.18), (0.30, 0.40, 0.58), (0.76, 0.70, 0.46), (0.72, 0.74, 0.70)]
    z = 0.1      # in the basket (0.15 deep), piled above its rim
    for k in range(5):
        h = rnd.uniform(0.03, 0.045)
        o = box("folded", bx - 0.13 + rnd.uniform(-0.01, 0.01), bx + 0.13 + rnd.uniform(-0.01, 0.01),
                0.24 + rnd.uniform(-0.01, 0.01), 0.40 + rnd.uniform(-0.01, 0.01), z, z + h,
                mat("cloth_%d" % k, cloths[k], rough=0.95))
        bev = o.modifiers.new("soft", "BEVEL")
        bev.width = h * 0.45
        bev.segments = 4
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.modifier_apply(modifier=bev.name)
        bpy.ops.object.shade_smooth()
        o.rotation_euler = (0.0, 0.0, rnd.uniform(-0.06, 0.06))
        z += h - 0.004
    placed(bpy, model, "potted_plant_02", -L / 2 + 0.3, 0.32, 0.0, rot=(0.0, 0.0, 0.4), size=0.5)
    placed(bpy, model, "potted_plant_01", -0.85, 0.38, 0.0, rot=(0.0, 0.0, 1.2), size=0.45)
    card = mat("window_card", (0.92, 0.90, 0.80), rough=0.85)
    ink = mat("card_ink", (0.05, 0.10, 0.45), rough=0.8)
    # both cards in the middle pane, clear of the mullions (the hours card stood behind one)
    standing_card(bpy, sc, box, -0.32, 0.05, 0.5, 0.3, [("SERVICE", 0.06), ("WASHES", 0.06), ("taken in", 0.035)], ink, card, lean=0.1)
    standing_card(bpy, sc, box, 0.25, 0.05, 0.36, 0.26, [("OPEN", 0.05), ("8am - 8pm", 0.04), ("7 days", 0.035)], ink, card, lean=0.1)
    # SOAP POWDER sold by the box, a stack of them lettered (a made-up maker), and the dry
    # cleaning card (3 October: the window was too sparse for the fresh review)
    powder = [mat("powder_blue", (0.08, 0.22, 0.55), rough=0.5), mat("powder_red", (0.60, 0.08, 0.06), rough=0.5)]
    white_ink = mat("powder_ink", (0.92, 0.92, 0.88), rough=0.5)
    for k, (bx2, by2, bz2, turn) in enumerate(((0.62, 0.38, 0.0, 0.1), (0.62, 0.38, 0.27, -0.05), (0.86, 0.4, 0.0, -0.15))):
        m = powder[k % 2]
        parts = [box("powder_box", bx2 - 0.1, bx2 + 0.1, by2 - 0.035, by2 + 0.035, bz2, bz2 + 0.27, m)]
        for j, (body, size) in enumerate((("CLEARWHITE", 0.026), ("Soap Powder", 0.02), ("E10", 0.03))):
            bpy.ops.object.text_add(location=(bx2, by2 - 0.036, bz2 + 0.2 - j * 0.05), rotation=(math.pi / 2, 0.0, 0.0))
            o = bpy.context.object
            o.data.body = body
            o.data.size = size
            o.data.align_x = "CENTER"
            o.data.materials.append(white_ink)
            bpy.ops.object.convert(target="MESH")
            parts.append(bpy.context.view_layer.objects.active)
        tilt_join(bpy, parts, (bx2, by2, bz2), 0.0, turn)
    standing_card(bpy, sc, box, -1.25, 0.06, 0.4, 0.2, [("DRY CLEANING", 0.04), ("taken in here", 0.03)], ink, card, lean=0.1)


def empty_display(bpy, sc, mat, box, L, Dp, rnd):
    """AN EMPTY SHOP'S WINDOW (V1, 3 October): the bed bare and dusty, post fanned on it, a
    dead fly or two of litter, and the glass whitewashed in broad swirls over its lower half
    (the inside of the pane, y = 0), as a shop to let was screened."""
    import math
    bed = mat("bare_bed", (0.26, 0.20, 0.13), rough=0.85)
    box("bed", -L / 2, L / 2, 0.0, Dp, -0.02, 0.0, bed)
    post = [mat("envelope_white", (0.85, 0.83, 0.76), rough=0.85), mat("envelope_brown", (0.55, 0.42, 0.25), rough=0.85),
            mat("leaflet", (0.80, 0.25, 0.15), rough=0.8)]
    for k in range(14):
        x = rnd.uniform(L / 2 - 1.1, L / 2 - 0.3)
        y = rnd.uniform(0.08, 0.4)
        e = box("post", x - 0.11, x + 0.11, y - 0.055, y + 0.055, 0.001 + k * 0.0012, 0.002 + k * 0.0012, rnd.choice(post))
        e.rotation_euler = (0.0, 0.0, rnd.uniform(-0.8, 0.8))
    wash = mat("whitewash_glass", (0.86, 0.85, 0.80), rough=0.95)
    # broad swirls: overlapping thin discs up the lower glass, thinning toward the top
    for k in range(90):
        x = rnd.uniform(-L / 2 + 0.05, L / 2 - 0.05)
        z = rnd.uniform(0.05, 1.25) ** 1.0
        if z > 1.0 and rnd.random() < 0.6:
            continue
        r = rnd.uniform(0.12, 0.26)
        bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=r, depth=0.001, location=(x, -0.003, z),
                                            rotation=(math.pi / 2, 0.0, 0.0))
        bpy.context.object.data.materials.append(wash)


def fish_display(bpy, sc, mat, box, L, Dp, rnd):
    """THE FISHMONGER'S WINDOW (V1, 3 October; production/research/shop-window-interiors/
    FISHMONGER-2026-10-03.md, and the builder's own look at Picture Sheffield t13140 and
    t13138): a white slab tilted to the pavement under crushed ice, the fish in rows on it
    (cod and haddock, plaice, smoked haddock, kippers, mackerel), crabs and prawns in white
    trays, a ticket priced by the pound on each (cod about 2.60 a pound in 1990, the ONS
    series), and the fish hand-lettered in white on the glass, as the 1990 photograph shows."""
    import math
    slab = mat("slab_white", (0.82, 0.83, 0.82), rough=0.35)
    ice = mat("ice", (0.80, 0.86, 0.90), rough=0.12)
    tray = mat("tray_white", (0.86, 0.86, 0.84), rough=0.4)
    eye = mat("fish_eye", (0.02, 0.02, 0.02), rough=0.2)
    ticket = mat("fish_ticket", (0.92, 0.92, 0.88), rough=0.8)
    ink = mat("fish_ink", (0.55, 0.04, 0.03), rough=0.8)
    whitewash = mat("whitewash", (0.92, 0.92, 0.90), rough=0.9)
    grass = mat("plastic_grass", (0.08, 0.35, 0.06), rough=0.5)

    TILT = math.radians(14.0)          # the slab tilted to the pavement, as the trade's slabs were

    def on_slab(y, h=0.0):
        """Height on the tilted slab at y back from the glass (the back stands higher)."""
        return 0.04 + y * math.tan(TILT) + h

    # THE SLAB AND ITS ICE: a white base, then crushed ice in small irregular pieces.
    base = box("fish_slab", -L / 2, L / 2, 0.02, Dp - 0.02, 0.0, 0.03, slab)
    base.rotation_euler = (TILT, 0.0, 0.0)
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0.0, Dp / 2, on_slab(Dp / 2, 0.012)))
    ice_bed = bpy.context.object
    ice_bed.scale = (L - 0.06, Dp - 0.06, 1.0)
    ice_bed.rotation_euler = (TILT, 0.0, 0.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    sub = ice_bed.modifiers.new("fine", "SUBSURF")
    sub.subdivision_type = "SIMPLE"
    sub.levels = 6
    tex = bpy.data.textures.new("crushed", "VORONOI")
    tex.noise_scale = 0.015
    disp = ice_bed.modifiers.new("crush", "DISPLACE")
    disp.texture = tex
    disp.strength = 0.012
    bpy.context.view_layer.objects.active = ice_bed
    for md in list(ice_bed.modifiers):
        bpy.ops.object.modifier_apply(modifier=md.name)
    ice_bed.data.materials.append(ice)

    def ellipsoid(name, x, y, z, sx, sy, sz, m, turn=0.0):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, location=(x, y, z))
        o = bpy.context.object
        o.name = name
        o.scale = (sx, sy, sz)
        o.rotation_euler = (TILT, 0.0, turn)
        o.data.materials.append(m)
        return o

    def round_fish(x, y, length, body, belly, turn):
        z = on_slab(y, 0.035 * length / 0.45)
        ellipsoid("fish", x, y, z, length / 2, length * 0.11, length * 0.075, body, turn)
        ellipsoid("belly", x, y, z - length * 0.02, length * 0.42, length * 0.095, length * 0.05, belly, turn)
        # the tail: a flattened wedge at one end
        dx, dy = math.cos(turn), math.sin(turn)
        bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=length * 0.09, depth=length * 0.16,
                                        location=(x + dx * length * 0.55, y + dy * length * 0.55, z))
        t = bpy.context.object
        t.scale = (1.0, 0.25, 1.0)
        t.rotation_euler = (0.0, -math.pi / 2, turn)
        t.data.materials.append(body)
        ellipsoid("eye", x - dx * length * 0.4, y - dy * length * 0.4 - length * 0.03, z + length * 0.03,
                  length * 0.014, length * 0.014, length * 0.014, eye)

    def flat_fish(x, y, length, top, spots, turn):
        z = on_slab(y, 0.012)
        ellipsoid("plaice", x, y, z, length / 2, length * 0.3, length * 0.03, top, turn)
        for k in range(7):
            a = rnd.uniform(0.0, 2.0 * math.pi)
            r = rnd.uniform(0.0, 0.7)
            ellipsoid("spot", x + math.cos(a) * r * length * 0.4, y + math.sin(a) * r * length * 0.22, z + length * 0.028,
                      length * 0.03, length * 0.03, length * 0.006, spots)

    def fillet(x, y, length, m, turn):
        ellipsoid("fillet", x, y, on_slab(y, 0.008), length / 2, length * 0.16, length * 0.025, m, turn)

    def tag(x, y, label, price):
        z = on_slab(y, 0.03)
        card = box("fish_ticket", x - 0.045, x + 0.045, y - 0.002, y + 0.002, z, z + 0.055, ticket)
        card.rotation_euler = (-0.25, 0.0, 0.0)
        for body, size, dz in ((label, 0.013, 0.033), (price, 0.016, 0.012)):
            bpy.ops.object.text_add(location=(x, y - 0.003, z + dz), rotation=(math.pi / 2 - 0.25, 0.0, 0.0))
            o = bpy.context.object
            o.data.body = body
            o.data.size = size
            o.data.align_x = "CENTER"
            o.data.materials.append(ink)
            bpy.ops.object.convert(target="MESH")

    cod = mat("cod_skin", (0.42, 0.40, 0.33), rough=0.25)
    haddock = mat("haddock_skin", (0.30, 0.31, 0.33), rough=0.25)
    belly_white = mat("belly", (0.80, 0.80, 0.78), rough=0.3)
    mackerel = mat("mackerel", (0.12, 0.25, 0.26), rough=0.2)
    plaice = mat("plaice_top", (0.30, 0.24, 0.16), rough=0.35)
    plaice_spot = mat("plaice_spot", (0.75, 0.30, 0.05), rough=0.4)
    smoked = mat("smoked_haddock", (0.80, 0.58, 0.18), rough=0.4)
    kipper = mat("kipper", (0.42, 0.20, 0.07), rough=0.35)
    white_fillet = mat("white_fillet", (0.86, 0.84, 0.78), rough=0.35)
    crab = mat("crab_shell", (0.55, 0.22, 0.08), rough=0.45)
    prawn = mat("prawn", (0.85, 0.42, 0.32), rough=0.5)

    # THE ROWS, front to back, each run along the window with its ticket.
    x0 = -L / 2 + 0.12
    rows = [
        ("COD FILLET", "£2.60 lb", lambda x, y: fillet(x, y, 0.26, white_fillet, rnd.uniform(-0.2, 0.2)), 0.11, 0.09),
        ("SMOKED HADDOCK", "£2.40 lb", lambda x, y: fillet(x, y, 0.24, smoked, rnd.uniform(-0.2, 0.2)), 0.11, 0.09),
        ("KIPPERS", "£1.20 lb", lambda x, y: fillet(x, y, 0.22, kipper, rnd.uniform(-0.15, 0.15)), 0.11, 0.09),
    ]
    # front row: fillets in three runs
    run = (L - 0.24) / 3.0
    for k, (label, price, make, step, _) in enumerate(rows):
        xa = x0 + k * run
        x = xa + 0.06
        while x < xa + run - 0.12:
            make(x, 0.10)
            x += step
        tag(xa + run / 2, 0.035, label, price)
    # middle row: whole round fish, heads to the glass
    y = 0.27
    x = x0 + 0.05
    kinds = [(cod, 0.50, "COD", "£1.80 lb"), (haddock, 0.42, "HADDOCK", "£1.90 lb"), (mackerel, 0.32, "MACKEREL", "90p lb")]
    for k, (skin, length, label, price) in enumerate(kinds):
        xa = x0 + k * run
        x = xa + 0.06
        while x < xa + run - 0.06:
            round_fish(x, y, length * rnd.uniform(0.9, 1.08), skin, belly_white, math.pi / 2 + rnd.uniform(-0.25, 0.25))
            x += length * 0.32
        tag(xa + run / 2, y - 0.17, label, price)
    # back row: plaice, crabs, a tray of prawns
    y = 0.44
    xa = x0
    x = xa + 0.1
    while x < xa + run - 0.1:
        flat_fish(x, y, 0.30 * rnd.uniform(0.9, 1.1), plaice, plaice_spot, rnd.uniform(-0.4, 0.4))
        x += 0.17
    tag(xa + run / 2, y - 0.12, "PLAICE", "£2.20 lb")
    xa = x0 + run
    x = xa + 0.1
    while x < xa + run - 0.08:
        z = on_slab(y, 0.035)
        ellipsoid("crab", x, y, z, 0.075, 0.06, 0.03, crab)
        for leg in range(4):
            for sgn in (-1, 1):
                bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.006, depth=0.07,
                                                    location=(x + sgn * 0.07, y - 0.03 + leg * 0.02, z - 0.01),
                                                    rotation=(0.0, math.pi / 2, sgn * 0.3))
                bpy.context.object.data.materials.append(crab)
        x += 0.17
    tag(xa + run / 2, y - 0.12, "DRESSED CRAB", "£1.50 each")
    xa = x0 + 2 * run
    tr = box("prawn_tray", xa + 0.06, xa + run - 0.06, y - 0.08, y + 0.08, on_slab(y, 0.0), on_slab(y, 0.03), tray)
    tr.rotation_euler = (TILT, 0.0, 0.0)
    for k in range(70):
        ellipsoid("prawn", rnd.uniform(xa + 0.09, xa + run - 0.09), rnd.uniform(y - 0.06, y + 0.06), on_slab(y, 0.035),
                  0.014, 0.008, 0.007, prawn, rnd.uniform(0, math.pi))
    tag(xa + run / 2, y - 0.12, "PRAWNS", "£3.50 lb")
    # plastic grass along the front edge, as a fish slab was dressed
    for k in range(int(L / 0.04)):
        bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.006, depth=0.035,
                                        location=(-L / 2 + 0.03 + k * 0.04, 0.025, on_slab(0.025, 0.015)))
        bpy.context.object.data.materials.append(grass)
    # THE WHITEWASH ON THE GLASS, hand-lettered, the 1990 photograph's own detail: on the
    # inside of the pane, read from the pavement (mirrored text would be wrong; the words
    # face out). y = 0: the glass plane.
    for body, xx, zz, size in (("FRESH FISH", -L / 4, 1.55, 0.13), ("CRABS", L / 4 + 0.1, 1.62, 0.11),
                               ("SCOTCH PLAICE", L / 4 + 0.1, 1.45, 0.08), ("Smoked Haddock", -L / 4, 1.38, 0.08)):
        bpy.ops.object.text_add(location=(xx, -0.004, zz), rotation=(math.pi / 2, 0.0, 0.0))
        o = bpy.context.object
        o.data.body = body
        o.data.size = size
        o.data.align_x = "CENTER"
        o.data.extrude = 0.0005
        o.data.materials.append(whitewash)
        bpy.ops.object.convert(target="MESH")


def build_display(argv):
    """THE NEAR METRE AS REAL MESHES (the note, sections 1 and 7): interior
    mapping fails close up and at a grazing angle, which is exactly where a
    pavement walker looks, so what stands on the bed behind the glass is
    geometry, exported as one glTF model (production/assets/shop-displays/
    <glb>.glb) that tools/ue/import_shop_displays.py brings into Unreal and the
    game stands behind the shop's glass (VignetteShot.cpp, LedgerInteriors).

    Local frame: x along the window, + to the viewer's right; y back from the
    glass; z up from the bed (the stallriser's top). Every material is a plain
    colour or the model's own pictures, so the glTF carries it; pictures are
    cut to 512 pixels and written as JPEG to keep the file small."""
    import bpy
    import random
    shop_id = argv[argv.index("--shop") + 1]
    out = os.path.abspath(argv[argv.index("--display") + 1])
    spec = json.load(open(SPEC, encoding="utf-8"))
    shop = next(s for s in spec["shops"] if s["id"] == shop_id)
    disp = shop["display"]
    L, Dp = disp["x1"] - disp["x0"], disp["depth"]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    POLY = os.environ.get("LEDGER_POLYHAVEN", "F:/LedgerTools/polyhaven")
    mats = {}

    def mat(name, colour, rough=0.6, metal=0.0):
        if name not in mats:
            m = bpy.data.materials.new(name)
            m.use_nodes = True
            p = m.node_tree.nodes["Principled BSDF"]
            p.inputs["Base Color"].default_value = (*colour, 1.0)
            p.inputs["Roughness"].default_value = rough
            p.inputs["Metallic"].default_value = metal
            mats[name] = m
        return mats[name]

    def box(name, x0, x1, y0, y1, z0, z1, m):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
        o = bpy.context.object
        o.name = name
        o.scale = (max(x1 - x0, 1e-3), max(y1 - y0, 1e-3), max(z1 - z0, 1e-3))
        o.data.materials.append(m)
        return o

    templates = {}
    # EACH MODEL CUT TO ABOUT 6000 TRIANGLES, BUT NEVER BY MORE THAN TWO THIRDS:
    # the first cut, 1500 a part and 300 for a watch, broke the watches into black
    # shards and the cameras into blocks (filmed in the game, 1 October).
    TRIS, KEEP_AT_LEAST = 4500, 0.3
    # SMALL GOODS IN HEAPS keep fewer (3 October): a crate holds twenty apples, and a scan of
    # seven thousand triangles each would make a window of a million
    SMALL_TRIS = {"food_apple_01": 550, "lemon": 450, "food_lime_01": 450, "yellow_onion": 500,
                  "food_kiwi_01": 450, "food_avocado_01": 500, "food_pears_asian_01": 600,
                  "hamburger_buns": 1200, "croissant": 1200, "sweet_potato": 800}
    # which way each model shows its face: the clocks were built facing the other way
    FACE = {"alarm_clock_01": 0.0, "mantel_clock_01": 0.0}

    def template(asset):
        """The asset imported once, cut down to TRIS triangles a mesh, and kept
        out of the scene: every placement is a copy sharing its mesh and pictures."""
        if asset in templates:
            return templates[asset]
        folder = os.path.join(POLY, asset, "1k")
        gl = next((f for f in os.listdir(folder) if f.endswith(".gltf")), None) if os.path.isdir(folder) else None
        if gl is None:
            print("shop-room display: model %s missing (run fetch_polyhaven.py --set %s_display)" % (asset, shop_id), flush=True)
            templates[asset] = None
            return None
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=os.path.join(folder, gl))
        new = [o for o in bpy.data.objects if o not in before]
        bpy.context.view_layer.update()
        meshes = []
        for o in new:
            if o.type != "MESH":
                continue
            mw = o.matrix_world.copy()
            o.parent = None
            o.matrix_world = mw
            meshes.append(o)
        for o in new:
            if o.type != "MESH":
                bpy.data.objects.remove(o, do_unlink=True)
        # A CLOCK'S OR A WATCH'S GLASS LEAVES OUT: the glTF's see-through glass came
        # into Unreal as an opaque black disc over the dial (the fresh reviewer:
        # "six alarm clocks have plain black faces with no dials").
        def glassy(o):
            return any(ms.material is not None and ("glass" in ms.material.name.lower()
                       or getattr(ms.material, "blend_method", "OPAQUE") not in ("OPAQUE", "CLIP")) for ms in o.material_slots)
        if any(not glassy(o) for o in meshes):
            for o in [o for o in meshes if glassy(o)]:
                meshes.remove(o)
                bpy.data.objects.remove(o, do_unlink=True)
        total = sum(len(p.vertices) - 2 for o in meshes for p in o.data.polygons)
        ratio = (max(0.06, min(1.0, SMALL_TRIS[asset] / float(max(total, 1)))) if asset in SMALL_TRIS
                 else max(KEEP_AT_LEAST, min(1.0, TRIS / float(max(total, 1)))))
        for o in meshes:
            bpy.ops.object.select_all(action="DESELECT")
            o.select_set(True)
            bpy.context.view_layer.objects.active = o
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            if o.data.shape_keys is not None:
                o.shape_key_clear()      # a still piece in a window needs no shape keys, and they block the cut
            if ratio < 1.0:
                md = o.modifiers.new("cut", "DECIMATE")
                md.ratio = ratio
                bpy.ops.object.modifier_apply(modifier=md.name)
            sc.collection.objects.unlink(o)
        from mathutils import Vector
        pts = [Vector(c) for o in meshes for c in o.bound_box]
        lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
        hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
        templates[asset] = (meshes, lo, hi)
        return templates[asset]

    def model(asset, x, y, z, turn=0.0, size=None, tilt=0.0):
        t = template(asset)
        if t is None:
            return None
        meshes, lo, hi = t
        root = bpy.data.objects.new(asset + "_root", None)
        sc.collection.objects.link(root)
        for m in meshes:
            c = m.copy()            # shares the mesh data, so the pictures and materials once
            sc.collection.objects.link(c)
            c.parent = root
        k = size / max(hi.x - lo.x, hi.y - lo.y, hi.z - lo.z, 1e-4) if size else 1.0
        from mathutils import Vector
        root.scale = (k, k, k)
        root.rotation_euler = (tilt, 0.0, turn)
        centre = Vector(((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, lo.z))
        root.location = (x - centre.x * k, y - centre.y * k, z - centre.z * k)
        return root

    rnd = random.Random(11)
    velvet = mat("velvet_red", (0.30, 0.025, 0.04), rough=0.92)
    velvet_blue = mat("velvet_blue", (0.03, 0.05, 0.16), rough=0.92)
    board = mat("bed_board", (0.20, 0.13, 0.08), rough=0.7)
    ticket = mat("ticket", (0.86, 0.84, 0.76), rough=0.85)
    string = mat("ticket_string", (0.75, 0.72, 0.62), rough=0.9)
    gold = mat("gold", (0.85, 0.62, 0.25), rough=0.22, metal=1.0)
    silver = mat("silver", (0.82, 0.82, 0.84), rough=0.18, metal=1.0)
    leather = mat("strap_leather", (0.12, 0.06, 0.03), rough=0.6)

    ink = mat("ticket_ink", (0.04, 0.04, 0.10), rough=0.8)
    prices = ["£4", "£6.50", "£8", "£12", "£15", "£18.50", "£25", "£35", "£45", "£60", "£3.75", "£9.99"]

    def tag(x, y, z, turn=0.0):
        # TICKETS OF A FEW SIZES, AND MOST WITH A PRICE in ink (the fresh reviewer:
        # "identical blank white tickets"); a text mesh, so the glTF carries it.
        w, h = rnd.uniform(0.013, 0.02), rnd.uniform(0.009, 0.013)
        t = box("tag", x - w, x + w, y - h, y + h, z, z + 0.0015, ticket)
        t.rotation_euler = (0.0, 0.0, turn)
        if rnd.random() < 0.75:
            bpy.ops.object.text_add(location=(x, y - h * 0.35, z + 0.0016))
            o = bpy.context.object
            o.data.body = prices[rnd.randrange(len(prices))]
            o.data.size = h * 1.1
            o.data.align_x = "CENTER"
            o.data.materials.append(ink)
            o.rotation_euler = (0.0, 0.0, turn)
            bpy.ops.object.convert(target="MESH")

    if shop_id == "fishmonger":
        fish_display(bpy, sc, mat, box, L, Dp, rnd)
    elif shop_id == "to_let":
        empty_display(bpy, sc, mat, box, L, Dp, rnd)
    elif shop_id == "launderette":
        launderette_display(bpy, sc, mat, box, model, L, Dp, rnd)
    elif shop_id == "grocer":
        grocer_display(bpy, sc, mat, box, model, L, Dp, rnd)
    elif shop_id == "newsagent":
        newsagent_display(bpy, sc, mat, box, model, L, Dp, rnd)
    elif shop_id == "ironmonger":
        ironmonger_display(bpy, sc, mat, box, model, L, Dp, rnd)
    elif shop_id == "tea_room":
        tea_room_display(bpy, sc, mat, box, model, L, Dp, rnd)
    elif shop_id == "chandler":
        chandler_display(bpy, sc, mat, box, model, L, Dp, rnd)
    else:
        # THE BED: a board covered in red velvet, and two velvet steps at the back
        # so the far rows stand above the near ones, as window dressers built them.
        box("bed", -L / 2, L / 2, 0.0, Dp, -0.02, 0.0, board)
        box("bed_velvet", -L / 2 + 0.01, L / 2 - 0.01, 0.01, Dp - 0.01, 0.0, 0.006, velvet)
        steps = ((0.24, 0.12), (0.40, 0.25))
        for k, (y0, h) in enumerate(steps):
            box("step_%d" % k, -L / 2 + 0.05, L / 2 - 0.05, y0, Dp - 0.02, 0.0, h, velvet)
        # THE FRONT ROW, on the bed, CRAMMED as a pawnbroker's was (the first build
        # stood each thing alone on bare velvet): trays of rings, pads of watches,
        # pocket watches, a chain, spectacles, a lighter, each with its white ticket.
        dial = mat("dial_white", (0.90, 0.88, 0.82), rough=0.3)

        def cyl(name, x, y, z, r, depth, m, verts=16):
            bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=(x, y, z + depth / 2))
            o = bpy.context.object
            o.name = name
            o.data.materials.append(m)
            return o

        def wristwatch(wx, wy, z, metal):
            # A WATCH THREE CENTIMETRES ACROSS IS MODELLED, NOT SCANNED: a case, a dial
            # and a strap read at a window's distance, and a scan cut to a few hundred
            # triangles did not (1 October).
            strap = leather if rnd.random() < 0.5 else metal
            box("strap", wx - 0.009, wx + 0.009, wy - 0.045, wy + 0.045, z, z + 0.003, strap)
            cyl("case", wx, wy, z + 0.003, 0.0155, 0.007, metal)
            cyl("dial", wx, wy, z + 0.010, 0.0125, 0.0008, dial)

        def pocketwatch(wx, wy, z, metal):
            cyl("pcase", wx, wy, z, 0.022, 0.009, metal, verts=20)
            cyl("pdial", wx, wy, z + 0.009, 0.019, 0.0008, dial, verts=20)
            bpy.ops.mesh.primitive_torus_add(major_radius=0.006, minor_radius=0.0015, major_segments=10, minor_segments=4,
                                             location=(wx, wy + 0.027, z + 0.004), rotation=(0.0, 0.0, 0.0))
            bpy.context.object.data.materials.append(metal)

        def watch_pad(x):
            box("watch_pad", x - 0.13, x + 0.13, 0.04, 0.2, 0.006, 0.022, velvet_blue if rnd.random() < 0.5 else velvet)
            for r in range(2):
                for c in range(4):
                    wx, wy = x - 0.095 + c * 0.063, 0.08 + r * 0.075
                    metal = gold if rnd.random() < 0.55 else silver
                    if rnd.random() < 0.6:
                        wristwatch(wx, wy, 0.022, metal)
                    else:
                        pocketwatch(wx, wy, 0.022, metal)
            tag(x + 0.1, 0.025, 0.007, 0.2)

        def ring_tray(x):
            box("ring_tray", x - 0.12, x + 0.12, 0.04, 0.2, 0.006, 0.03, velvet_blue if rnd.random() < 0.6 else velvet)
            for r in range(4):
                for c in range(6):
                    bpy.ops.mesh.primitive_torus_add(major_radius=0.009, minor_radius=0.0025, major_segments=12, minor_segments=5,
                                                     location=(x - 0.1 + c * 0.04, 0.065 + r * 0.035, 0.036),
                                                     rotation=(math.pi / 2, 0.0, 0.0))
                    bpy.context.object.data.materials.append(gold if rnd.random() < 0.75 else silver)
            tag(x + 0.09, 0.025, 0.007, -0.2)

        def chain(x):
            for i in range(18):
                a = i / 17.0 * math.pi
                bpy.ops.mesh.primitive_torus_add(major_radius=0.004, minor_radius=0.0012, major_segments=8, minor_segments=4,
                                                 location=(x - 0.07 + 0.14 * i / 17.0, 0.12 + 0.035 * math.sin(a), 0.008),
                                                 rotation=(0.0, math.pi / 2 if i % 2 else 0.0, 0.0))
                bpy.context.object.data.materials.append(gold)
            tag(x + 0.07, 0.07, 0.007, 0.1)

        x = -L / 2 + 0.14
        while x < L / 2 - 0.16:
            kind = rnd.random()
            if kind < 0.35:
                ring_tray(x)
                x += 0.255
            elif kind < 0.65:
                watch_pad(x)
                x += 0.275
            elif kind < 0.78:
                chain(x)
                x += 0.16
            elif kind < 0.86:
                model("round_spectacles", x, 0.12, 0.007, turn=rnd.uniform(-0.3, 0.3), size=0.13)
                tag(x + 0.04, 0.05, 0.007, 0.0)
                x += 0.15
            else:
                model("vintage_lighter" if rnd.random() < 0.5 else "cigarette_case", x, 0.12, 0.007, turn=rnd.uniform(-0.5, 0.5), size=0.08)
                pocketwatch(x + 0.07, 0.08, 0.007, gold)
                tag(x + 0.03, 0.04, 0.007, 0.3)
                x += 0.15
        # THE MIDDLE AND BACK STEPS, each piece drawn from a shuffled set so no two
        # neighbours match and few things repeat (the fresh reviewer: "four identical
        # mantel clocks, five identical cameras, six identical alarm clocks ... in a
        # regular grid"); sizes, turns and depths vary, the gaps uneven.
        def lay(pool, y, z, x0, x1, gap, depth_jitter):
            bag = []
            x = x0
            last = None
            while x < x1:
                if not bag:
                    bag = pool[:]
                    rnd.shuffle(bag)
                asset, size = bag.pop()
                if asset == last and bag:
                    bag.insert(0, (asset, size))
                    asset, size = bag.pop()
                last = asset
                size *= rnd.uniform(0.85, 1.12)
                foot = size * (0.55 if asset in ("Camera_01", "binoculars", "vintage_video_camera") else 0.9)
                if x + foot > x1:
                    break
                model(asset, x + foot / 2, y + rnd.uniform(-depth_jitter, depth_jitter), z,
                      turn=FACE.get(asset, math.pi) + rnd.uniform(-0.45, 0.45), size=size)
                if rnd.random() < 0.8:
                    tag(x + foot / 2 + rnd.uniform(-0.02, 0.02), y - 0.065, z + 0.001, rnd.uniform(-0.3, 0.3))
                x += foot + rnd.uniform(*gap)

        # (no alarm clocks: their glass is one piece with the dial and still came out black)
        mid = [("Camera_01", 0.24), ("binoculars", 0.2), ("portable_cassette_player", 0.2),
               ("magnifying_glass_01", 0.17), ("brass_vase_02", 0.17), ("seadogs_compass", 0.1), ("vintage_flashlight", 0.18),
               ("measuring_tape_01", 0.08), ("ceramic_vase_01", 0.15), ("standing_picture_frame_01", 0.16),
               ("carved_wooden_elephant", 0.14), ("jug_01", 0.16), ("brass_vase_01", 0.15)]
        lay(mid, 0.32, steps[0][1], -L / 2 + 0.08, L / 2 - 0.1, (0.015, 0.07), 0.03)
        back = [("mantel_clock_01", 0.24), ("Camera_01", 0.24), ("brass_vase_03", 0.24),
                ("portable_cassette_player", 0.22), ("vintage_video_camera", 0.3), ("antique_ceramic_vase_01", 0.24),
                ("horse_statue_01", 0.2), ("standing_picture_frame_02", 0.2), ("ceramic_vase_03", 0.2)]
        # (no military radio: corroded salvage, not pawn stock; the second reviewer)
        lay(back, 0.46, steps[1][1], -L / 2 + 0.1, L / 2 - 0.12, (0.03, 0.1), 0.02)

        # NOTICES STOOD IN THE WINDOW against the glass, read from the pavement, as
        # the Hook sheet's shop has (the second reviewer: "the glass has no ...
        # notices"): a printed card and a hand-lettered one.
        red_ink = mat("notice_red", (0.50, 0.04, 0.03), rough=0.8)
        card_pale = mat("notice_card", (0.88, 0.85, 0.74), rough=0.85)
        card_yellow = mat("notice_yellowed", (0.80, 0.72, 0.50), rough=0.85)
        for (cx, w, h, lines, inkm, cardm, lean) in (
                (-L / 2 + 0.42, 0.42, 0.26, [("UNREDEEMED", 0.05), ("PLEDGES", 0.05), ("FOR SALE", 0.035)], red_ink, card_yellow, 0.12),
                (L / 2 - 0.5, 0.46, 0.2, [("CASH LOANS", 0.05), ("on Gold & Watches", 0.028)], ink, card_pale, 0.1)):
            cy = 0.035
            cardo = box("notice", cx - w / 2, cx + w / 2, cy - 0.002, cy + 0.002, 0.0, h, cardm)
            parts = [cardo]
            top = h - 0.035
            for body, size in lines:
                bpy.ops.object.text_add(location=(cx, cy - 0.0035, top - size * 0.8), rotation=(math.pi / 2, 0.0, 0.0))
                o = bpy.context.object
                o.data.body = body
                o.data.size = size
                o.data.align_x = "CENTER"
                o.data.materials.append(inkm)
                bpy.ops.object.convert(target="MESH")
                parts.append(bpy.context.object)
                top -= size * 1.35
            # leaned back against a prop at its foot, the way a card stands in a window
            piv = bpy.data.objects.new("notice_pivot", None)
            sc.collection.objects.link(piv)
            piv.location = (cx, cy, 0.0)
            for o in parts:
                mw = o.matrix_world.copy()
                o.parent = piv
                o.matrix_world = mw
            piv.rotation_euler = (-lean, 0.0, 0.0)     # top away from the glass (+x turns +z toward -y)

    # ONE MESH, in the order Unreal wants it: transforms applied, everything joined.
    bpy.context.view_layer.update()
    meshes = [o for o in sc.objects if o.type == "MESH"]
    for o in meshes:
        mw = o.matrix_world.copy()
        o.parent = None
        o.matrix_world = mw
    bpy.ops.object.select_all(action="DESELECT")
    for o in meshes:
        if o.data.users > 1:
            o.data = o.data.copy()
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.join()
    joined = bpy.context.view_layer.objects.active
    joined.name = disp["glb"]
    for o in list(sc.objects):
        if o != joined:
            bpy.data.objects.remove(o, do_unlink=True)
    for img in bpy.data.images:
        if img.size[0] > 512:
            img.scale(512, max(1, int(512 * img.size[1] / img.size[0])))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", export_image_format="JPEG", export_apply=True)
    tris = sum(len(p.vertices) - 2 for p in joined.data.polygons)
    print("shop-room display: %s written, %d triangles, %d materials, %.1f MB"
          % (out, tris, len(joined.data.materials), os.path.getsize(out) / 1e6), flush=True)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--" in sys.argv:
        a = sys.argv[sys.argv.index("--") + 1:]
        build_display(a) if "--display" in a else build_and_render(a)
