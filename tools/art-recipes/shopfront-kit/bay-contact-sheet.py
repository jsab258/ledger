"""Rita's bay (the east parade's bay 2, x 15.0 to 21.0) assembled from the shopfront kit beside the
existing fascia band, cornice and consoles, the check that each pilaster's top meets its
console's underside, and the kit's contact sheet.

    python tools/art-recipes/shopfront-kit/bay-contact-sheet.py [--check-only] [--cpu]

Run with ordinary Python (Pillow). It runs Blender headless on this same file, which:
  1. appends the kit's pieces from F:\\LedgerTools\\shopfront-kit\\blend (their .blend files keep
     the preview wear) and imports ledger/Assets/Props/base-mesh/fascia_console_01.glb and
     fascia_cornice_01.glb, turned to face the street (both are authored projecting toward +Y in
     Blender, the kit toward -Y);
  2. lays the bay out left to right seen from the street: pilaster, side door, shop door, window
     over the stallriser, pilaster; the neighbours' pilasters and consoles stand beside them at the
     party walls, as the street places them (vignette-scene.json: consoles on the pilaster
     centres, 0.175 m either side of x = 15 and x = 21); the fascia band is the street's box
     (2.85 to 3.40, 0.12 proud), the cornice on it (3.40 to 3.55);
  3. measures every pilaster-to-console meet (gap between the capital's top and the console's
     underside, and whether the console's foot stands wholly on the capital) and writes
     F:\\LedgerTools\\shopfront-kit\\blend\\bay-meet.json;
  4. only if the graphics card is free (no UnrealEditor, no Runner.Worker), renders two views with
     Eevee: the bay from the street and a close view of a party-wall pilaster pair under its
     consoles. A busy card stops the render and the sheet. --cpu renders them with Cycles on the
     processor instead, which leaves the graphics card alone (slower).
Then it composes production/previews/shopfront-kit-2026-10-06.jpg (about 1600 px wide, under
500 KB): the bay, the close view, and each piece's preview labelled with its measured size,
triangles and glb size. Glass is drawn here as dark glossy planes in the openings the pieces'
reports list; it is not part of the kit (Unreal draws the glass).
"""
import json
import math
import os
import subprocess
import sys

BLENDER = r"F:\LedgerTools\blender52\blender-5.2.2-windows-x64\blender.exe"
BLEND_DIR = r"F:\LedgerTools\shopfront-kit\blend"
PREVIEW_DIR = r"F:\LedgerTools\shopfront-kit\previews"
GLB_DIR = r"F:\LedgerTools\game-inputs\production\assets\shopfront-kit"
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
BASE_MESH = os.path.join(REPO, "ledger", "Assets", "Props", "base-mesh")
OUT = os.path.join(REPO, "production", "previews", "shopfront-kit-2026-10-06.jpg")
BAY_PNG = os.path.join(PREVIEW_DIR, "bay-rita.png")
MEET_PNG = os.path.join(PREVIEW_DIR, "bay-rita-meet.png")
MEET_JSON = os.path.join(BLEND_DIR, "bay-meet.json")
PIECES = [("pilaster", "Pilaster"), ("stallriser_panelled", "Stallriser, panelled"),
          ("stallriser_tile", "Stallriser, glazed tile"), ("window_frame", "Window frame"),
          ("shop_door", "Shop door in its frame"), ("side_door", "Side door to the flat")]

# the bay's layout, left to right seen from the street (local x 0..6 = street x 15..21)
PIL_W, SIDE_W, SHOP_W = 0.35, 0.944, 1.006
X_SIDE = PIL_W + SIDE_W / 2
X_SHOP = PIL_W + SIDE_W + SHOP_W / 2
WIN_X0 = PIL_W + SIDE_W + SHOP_W
WIN_L = 6.0 - PIL_W - WIN_X0
X_WIN = WIN_X0 + WIN_L / 2
PILASTERS = [-0.175, 0.175, 5.825, 6.175]       # the party-wall pairs at x = 15 and x = 21
FASCIA = (2.85, 3.40, 0.12)


def gpu_busy():
    try:
        out = subprocess.run(["tasklist", "/FO", "CSV", "/NH"], capture_output=True, text=True,
                             timeout=60).stdout.lower()
    except Exception as e:  # noqa: BLE001
        print("GPU CHECK FAILED, treated as busy:", e)
        return True
    hits = [n for n in ("unrealeditor", "runner.worker") if n in out]
    if hits:
        print("GPU BUSY (%s): nothing rendered on the graphics card" % ", ".join(hits))
    return bool(hits)


def in_blender(check_only, cpu=False):
    import bmesh
    import bpy
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree

    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    coll = sc.collection

    def append(stem, names):
        with bpy.data.libraries.load(os.path.join(BLEND_DIR, stem + ".blend"), link=False) as (src, dst):
            dst.objects = [n for n in src.objects if n in names]
        for o in dst.objects:
            coll.objects.link(o)
        return {o.name.split(".")[0]: o for o in dst.objects}

    def box(name, a, b, mat):
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        for v in bm.verts:
            v.co = Vector((a[0] if v.co.x < 0 else b[0], a[1] if v.co.y < 0 else b[1], a[2] if v.co.z < 0 else b[2]))
        me = bpy.data.meshes.new(name)
        bm.to_mesh(me)
        bm.free()
        ob = bpy.data.objects.new(name, me)
        coll.objects.link(ob)
        if mat:
            me.materials.append(mat)
        return ob

    def plain(name, rgb, rough, metal=0.0):
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        p = m.node_tree.nodes["Principled BSDF"]
        p.inputs["Base Color"].default_value = (*rgb, 1.0)
        p.inputs["Roughness"].default_value = rough
        p.inputs["Metallic"].default_value = metal
        return m

    def glb(stem, x, z_bottom):
        """Import a fascia glb, turn it to face the street (-Y), its wall side on y = 0, its foot at
        z_bottom, centred on x."""
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=os.path.join(BASE_MESH, stem + ".glb"))
        ob = [o for o in bpy.data.objects if o not in before and o.type == "MESH"][0]
        me = ob.data
        zs = [v.co.z for v in me.vertices]
        ys = [v.co.y for v in me.vertices]

        def extent(y):
            on = [v.co.z for v in me.vertices if abs(v.co.y - y) < 1e-4]
            return max(on) - min(on) if on else 0.0
        # the back, against the wall, is one flat face the full height; the moulded front is not
        wall_y = min(ys) if extent(min(ys)) > extent(max(ys)) else max(ys)
        ob.rotation_mode = "XYZ"                         # the glTF importer leaves it in quaternions
        if wall_y < 0:                                  # authored projecting toward +Y: turn it round
            ob.rotation_euler = (0.0, 0.0, math.pi)
            ob.location = (x, wall_y, z_bottom - min(zs))
        else:
            ob.location = (x, -wall_y, z_bottom - min(zs))
        bpy.context.view_layer.update()
        return ob

    paint_m = None
    # ---- the kit's pieces ------------------------------------------------------------------
    pil = append("pilaster", ["pilaster"])["pilaster"]
    pils = []
    for i, x in enumerate(PILASTERS):
        o = pil if i == 0 else pil.copy()
        if i:
            coll.objects.link(o)
        o.location = (x, 0.0, 0.0)
        pils.append(o)
    paint_m = pil.material_slots[0].material
    side = append("side_door", ["side_door", "side_door_leaf"])
    side["side_door"].location = (X_SIDE, 0.0, 0.0)
    shop = append("shop_door", ["shop_door", "shop_door_leaf"])
    shop["shop_door"].location = (X_SHOP, 0.0, 0.0)
    win = append("window_frame", ["window_frame"])["window_frame"]
    win.location = (X_WIN, 0.0, 0.0)
    stall = append("stallriser_panelled", ["stallriser_panelled"])["stallriser_panelled"]
    stall.location = (X_WIN, 0.0, 0.0)
    # ---- the existing fascia, consoles and cornices ------------------------------------------
    # the fascia band between each bay's consoles (the fascia sits between the consoles,
    # Coventry 2014). The street's box today runs across the pilaster heads too, 0.12 proud, and
    # buries the lower half of each console, whose foot is only 0.06 deep (see the README).
    fascia_m = bpy.data.materials.new("_fascia_paint")
    fascia_m.use_nodes = True
    fp = fascia_m.node_tree.nodes["Principled BSDF"]
    base = json.loads(paint_m["plain"])["base"]
    fp.inputs["Base Color"].default_value = (*base, 1.0)
    fp.inputs["Roughness"].default_value = 0.5
    for x0, x1 in ((-0.9, -0.055), (0.295, 5.705), (6.055, 6.9)):
        box("fascia_band", (x0, -FASCIA[2], FASCIA[0]), (x1, 0.0, FASCIA[1]), fascia_m)
    consoles = [glb("fascia_console_01", x, FASCIA[0]) for x in PILASTERS]
    for x in (-3.0, 3.0, 9.0):
        glb("fascia_cornice_01", x, FASCIA[1])
    # the fascia meshes carry one plain grey slot that the street overwrites; here, the shop's paint
    for o in bpy.data.objects:
        if o.name.startswith("fascia_c") and o.type == "MESH":
            o.data.materials.clear()
            o.data.materials.append(fascia_m)
    bpy.context.view_layer.update()

    # ---- the meet: each pilaster's top against its console's underside -----------------------
    meet = []
    for p, c in zip(pils, consoles):
        pw = [p.matrix_world @ v.co for v in p.data.vertices]
        cw = [c.matrix_world @ v.co for v in c.data.vertices]
        c_bottom = min(v.z for v in cw)
        foot = [v for v in cw if v.z < c_bottom + 0.001]
        p_top = max(v.z for v in pw)
        tree = BVHTree.FromPolygons(pw, [tuple(f.vertices) for f in p.data.polygons])
        drops = []
        fc = sum(foot, Vector()) / len(foot)
        for v in foot:
            # each point of the foot, 0.5 mm in from its edge (a ray along a face's very edge can
            # slip past it), dropped onto the capital
            d = Vector((fc.x - v.x, fc.y - v.y, 0.0))
            o = v + (d.normalized() * 0.0005 if d.length > 1e-6 else Vector())
            hit = tree.ray_cast(Vector((o.x, o.y, v.z + 0.0005)), Vector((0, 0, -1)), 0.05)
            drops.append(None if hit[0] is None else round(v.z - hit[0].z, 5))
        meet.append({"pilaster_x": round(p.location.x, 4), "pilaster_top_z": round(p_top, 4),
                     "console_bottom_z": round(c_bottom, 4), "gap_mm": round((c_bottom - p_top) * 1000, 2),
                     "console_foot_x": [round(min(v.x for v in foot), 4), round(max(v.x for v in foot), 4)],
                     "console_foot_y": [round(min(v.y for v in foot), 4), round(max(v.y for v in foot), 4)],
                     "foot_points": len(foot), "foot_points_on_capital": sum(1 for d in drops if d is not None and d <= 0.005),
                     "worst_drop_mm": None if None in drops else round(max(drops) * 1000, 2)})
    ok = all(abs(m["gap_mm"]) <= 5.0 and m["foot_points_on_capital"] == m["foot_points"] for m in meet)
    res = {"bay": "east parade bay 2, Rita's (x 15.0 to 21.0)", "layout_local_x": {
        "pilasters": PILASTERS, "side_door": X_SIDE, "shop_door": X_SHOP, "window_and_stallriser": X_WIN,
        "window_length": round(WIN_L, 4)}, "meets": meet, "all_within_5mm_and_on_capital": ok}
    os.makedirs(BLEND_DIR, exist_ok=True)
    with open(MEET_JSON, "w") as f:
        json.dump(res, f, indent=1)
    print("MEET " + json.dumps(res))
    if check_only:
        return
    if not cpu and gpu_busy():
        sys.exit(3)

    # ---- context: wall above, the shop's dark interior, glass, the pavement -------------------
    brick = plain("_brick", (0.20, 0.075, 0.05), 0.85)
    box("_wall_above", (-3.0, 0.0, FASCIA[1]), (9.0, 0.4, 6.2), brick)
    box("_pier_l", (-0.35, 0.0, 0.0), (0.35, 0.4, FASCIA[1]), brick)       # the brick piers behind
    box("_pier_r", (5.65, 0.0, 0.0), (6.35, 0.4, FASCIA[1]), brick)        # the party-wall pilasters
    grey = plain("_neighbour", (0.09, 0.09, 0.09), 0.8)                    # the next shops, not shown
    box("_next_l", (-3.0, 0.0, 0.0), (-0.35, 0.4, FASCIA[1]), grey)
    box("_next_r", (6.35, 0.0, 0.0), (9.0, 0.4, FASCIA[1]), grey)
    inside = plain("_interior", (0.035, 0.03, 0.026), 0.9)
    box("_interior_back", (0.35, 3.0, 0.0), (5.65, 3.1, 3.4), inside)
    box("_interior_floor", (0.35, 0.0, -0.01), (5.65, 3.1, 0.0), inside)
    box("_interior_ceiling", (0.35, 0.0, 3.40), (5.65, 3.1, 3.41), inside)
    pave = plain("_pavement", (0.16, 0.16, 0.155), 0.8)
    box("_pavement", (-3.0, -4.0, -0.1), (9.0, 0.0, 0.0), pave)
    glass = plain("_glass", (0.010, 0.012, 0.014), 0.04)
    glass.node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0.8

    def pane(name, x0, x1, z0, z1, y):
        box(name, (x0, y - 0.003, z0), (x1, y + 0.003, z1), glass)
    wr = json.load(open(os.path.join(BLEND_DIR, "window_frame.report.json")))
    for k, p in enumerate(wr["panes"]):
        pane("_win%d" % k, X_WIN + p["x"][0], X_WIN + p["x"][1], p["z"][0], p["z"][1], wr["glass_y"])
    for stem, x0 in (("shop_door", X_SHOP), ("side_door", X_SIDE)):
        r = json.load(open(os.path.join(BLEND_DIR, stem + ".report.json")))
        for k, o in enumerate(r["layout"]["openings"]):
            pane("_%s%d" % (stem, k), x0 + o["x"][0], x0 + o["x"][1], o["z"][0], o["z"][1], o["glass_y"])

    # ---- light and views ---------------------------------------------------------------------
    world = bpy.data.worlds.new("w")
    sc.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.62, 0.66, 0.72, 1.0)
    bg.inputs["Strength"].default_value = 0.9
    sun = bpy.data.lights.new("sun", "SUN")
    sun.energy = 1.6
    sun.angle = math.radians(8)
    so = bpy.data.objects.new("sun", sun)
    coll.objects.link(so)
    so.rotation_euler = (math.radians(52), 0.0, math.radians(-38))
    if cpu:                       # Cycles on the processor: leaves the graphics card alone
        sc.render.engine = "CYCLES"
        sc.cycles.device = "CPU"
        sc.cycles.samples = 64
        sc.cycles.use_denoising = True
        sc.cycles.denoising_use_gpu = False
        sc.render.threads_mode = "FIXED"
        sc.render.threads = 4
    else:
        sc.render.engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in [i.identifier for i in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items] else "BLENDER_EEVEE_NEXT"
        if hasattr(sc.eevee, "use_raytracing"):
            sc.eevee.use_raytracing = True
        try:
            sc.eevee.taa_render_samples = 96
        except AttributeError:
            pass
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast" if "AgX - Medium High Contrast" in [
        i.identifier for i in bpy.types.ColorManagedViewSettings.bl_rna.properties["look"].enum_items] else "None"

    def shoot(path, eye, target, lens, res):
        cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
        coll.objects.link(cam)
        cam.data.lens = lens
        cam.location = Vector(eye)
        cam.rotation_euler = (Vector(target) - Vector(eye)).to_track_quat("-Z", "Y").to_euler()
        sc.camera = cam
        sc.render.resolution_x, sc.render.resolution_y = res
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
        bpy.data.objects.remove(cam)

    os.makedirs(PREVIEW_DIR, exist_ok=True)
    shoot(BAY_PNG, (0.9, -7.6, 1.55), (3.05, 0.0, 1.95), 30, (1600, 900))
    shoot(MEET_PNG, (5.35, -1.05, 2.25), (6.0, -0.06, 2.95), 50, (800, 800))


def compose():
    from PIL import Image, ImageDraw, ImageFont
    W, TILE, LAB = 1600, 400, 46
    bay = Image.open(BAY_PNG).convert("RGB")
    bay = bay.resize((W, int(bay.height * W / bay.width)))
    head = 48
    H = head + bay.height + 34 + 2 * (TILE + LAB)
    sheet = Image.new("RGB", (W, H), (38, 38, 38))
    dr = ImageDraw.Draw(sheet)
    try:
        f_big = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 24)
        f = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 17)
        f_s = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 15)
    except OSError:
        f_big = f = f_s = ImageFont.load_default()
    dr.text((16, 10), "Shopfront kit for the east parade: Rita's bay assembled (6 October 2026)", fill=(235, 235, 235), font=f_big)
    sheet.paste(bay, (0, head))
    meet = json.load(open(MEET_JSON))
    gaps = ", ".join("%.1f" % m["gap_mm"] for m in meet["meets"])
    dr.text((16, head + bay.height + 7),
            "Left to right: pilaster, side door, shop door, window over a panelled stallriser, pilaster; the street's consoles and "
            "cornice in place, the fascia band between the consoles. Pilaster-to-console gaps (mm): %s. Glass for the view only." % gaps,
            fill=(200, 200, 200), font=f_s)
    y0 = head + bay.height + 34
    tiles = PIECES + [("__meet", "Pilasters under the consoles (x = 21)")]
    for i, (stem, label) in enumerate(tiles):
        r, c = divmod(i, 4)
        x, y = c * TILE, y0 + r * (TILE + LAB)
        src = MEET_PNG if stem == "__meet" else os.path.join(PREVIEW_DIR, stem + ".png")
        im = Image.open(src).convert("RGB").resize((TILE, TILE))
        sheet.paste(im, (x, y))
        dr.text((x + 10, y + TILE + 2), label, fill=(240, 240, 240), font=f)
        if stem == "__meet":
            m = [m for m in meet["meets"] if m["pilaster_x"] > 6.0][0]
            line = "gap %.1f mm | foot on the capital: %d of %d points" % (m["gap_mm"], m["foot_points_on_capital"], m["foot_points"])
        else:
            rep = json.load(open(os.path.join(BLEND_DIR, stem + ".report.json")))
            s = rep["size_m"]
            line = "%d x %d x %d mm | %s tris | %d KB" % (round(s["x"] * 1000), round(s["y"] * 1000), round(s["z"] * 1000),
                                                         format(rep["triangles"], ","), rep["glb_bytes"] // 1024)
        dr.text((x + 10, y + TILE + 23), line, fill=(185, 185, 185), font=f_s)
    x, y = 3 * TILE, y0 + TILE + LAB
    notes = ["Sizes: width x depth x height of the", "whole piece (doors with their frames,", "step and fittings).", "",
             "Each piece: <= 3 plain materials, no", "textures, one UV map, ao + edges", "masks in COLOR_0. Paint colour set", "per shop (--paint).",
             "", "Previews show the masks' wear (the", ".blend's preview materials); glass", "is Unreal's, not the kit's."]
    for k, t in enumerate(notes):
        dr.text((x + 18, y + 14 + k * 21), t, fill=(200, 200, 200), font=f_s)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    q = 86
    while True:
        sheet.save(OUT, "JPEG", quality=q, optimize=True, progressive=True)
        if os.path.getsize(OUT) < 490 * 1024 or q <= 50:
            break
        q -= 6
    print("contact sheet", OUT, sheet.size, os.path.getsize(OUT) // 1024, "KB, quality", q)


if __name__ == "__main__":
    check_only = "--check-only" in sys.argv
    cpu = "--cpu" in sys.argv
    try:
        import bpy  # noqa: F401
        in_blender(check_only, cpu)
    except ImportError:
        args = ([BLENDER, "-b", "--factory-startup", "-P", os.path.abspath(__file__), "--"]
                + (["--check-only"] if check_only else []) + (["--cpu"] if cpu else []))
        for p in (BAY_PNG, MEET_PNG):
            if not check_only and os.path.exists(p):
                os.remove(p)
        r = subprocess.run(args, capture_output=True, text=True)
        for line in (r.stdout + r.stderr).splitlines():
            if line.startswith("MEET ") or "GPU" in line or "Traceback" in line or "Error" in line:
                print(line[:2000])
        if check_only:
            sys.exit(0 if r.returncode == 0 else 1)
        if r.returncode == 3:
            print("graphics card busy: no render, no contact sheet")
            sys.exit(3)
        if not (os.path.exists(BAY_PNG) and os.path.exists(MEET_PNG)) or "Traceback" in r.stdout + r.stderr:
            print(r.stdout[-3000:], r.stderr[-3000:])
            sys.exit(1)
        compose()
