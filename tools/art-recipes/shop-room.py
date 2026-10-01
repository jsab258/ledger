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
            nt.links.new(tex.outputs["Color"], ramp.inputs["Color2"])
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

    def text(name, body, x, y, z, size, m, rot_x=math.pi / 2):
        bpy.ops.object.text_add(location=(x, y, z), rotation=(rot_x, 0, 0))
        o = bpy.context.object
        o.name = name
        o.data.body = body
        o.data.size = size
        o.data.align_x = "CENTER"
        o.data.extrude = 0.002
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
    box("floor", -W / 2, W / 2, 0, D, -0.02, 0.0, floor_lino)
    wall = texmat("plaster_cream", "painted_plaster_wall", 1.5, (0.95, 0.86, 0.66),
                  base=mat("paint_cream", (0.55, 0.50, 0.39), rough=0.85, noise=0.3))
    dado = texmat("plaster_brown", "painted_plaster_wall", 1.5, (0.42, 0.27, 0.17),
                  base=mat("paint_brown", (0.22, 0.14, 0.09), rough=0.6, noise=0.1))
    ceiling = mat("ceiling", (0.70, 0.68, 0.62), rough=0.9)
    t = 0.05
    box("wall_left", -W / 2 - t, -W / 2, 0, D, 0, H, wall)
    box("wall_right", W / 2, W / 2 + t, 0, D, 0, H, wall)
    box("wall_back", -W / 2, W / 2, D, D + t, 0, H, wall)
    box("ceiling", -W / 2, W / 2, 0, D, H, H + t, ceiling)
    for side, x0, x1 in (("left", -W / 2, -W / 2 + 0.01), ("right", W / 2 - 0.01, W / 2)):
        box("dado_" + side, x0, x1, 0, D, 0, 0.95, dado)
    box("dado_back", -W / 2, W / 2, D - 0.01, D, 0, 0.95, dado)
    # The back door, half open onto a dark back room.
    door = mat("door", (0.28, 0.17, 0.10), rough=0.5, noise=0.1)
    dark = mat("back_room", (0.02, 0.02, 0.02), rough=1.0)
    box("door_gap", 1.1, 1.95, D - 0.02, D + 0.06, 0, 2.0, dark)
    door_leaf = box("door_leaf", 1.1, 1.92, D - 0.06, D - 0.02, 0, 1.98, door)
    door_leaf.rotation_euler[2] = math.radians(-35)

    # THE TUBES: three T12 battens across the ceiling, 1.5 m long.
    tube_on = mat("tube_on", (0.9, 0.95, 0.95), rough=0.3, emit=(0.92, 0.97, 1.0), emit_strength=0.0)
    batten = mat("batten", (0.75, 0.75, 0.72), rough=0.5)
    for k, y in enumerate((1.0, 2.4, 3.8)):
        if y > D - 0.3:
            continue
        box("batten_%d" % k, -0.8, 0.8, y - 0.05, y + 0.05, H - 0.06, H - 0.01, batten)
        cyl("tube_%d" % k, 0.0, y, H - 0.075, 0.019, 1.5, tube_on, axis="x")

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


# ------------------------------------------------------- the window display
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
        ratio = max(KEEP_AT_LEAST, min(1.0, TRIS / float(max(total, 1))))
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
