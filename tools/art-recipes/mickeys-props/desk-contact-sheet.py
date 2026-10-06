"""Contact sheet of set 1 (the desk props) for Mickey's front office.

    python tools/art-recipes/mickeys-props/desk-contact-sheet.py

Run with ordinary Python (Pillow). It first runs Blender headless on this same
file to render all seven glbs side by side at true scale (front three-quarter,
neutral grey ground), then lays that strip over the seven single-prop
previews the prop scripts rendered, each labelled with its size and triangle
count, and writes production/previews/mickeys-props-desk-2026-10-06.jpg
(about 1600 px wide, under 500 KB).
"""
import json
import math
import os
import subprocess
import sys

BLENDER = r"F:\LedgerTools\blender52\blender-5.2.2-windows-x64\blender.exe"
GLB_DIR = r"F:\LedgerTools\game-inputs\production\assets\mickeys-props"
PREVIEW_DIR = r"F:\LedgerTools\mickeys-props\previews"
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
OUT = os.path.join(REPO, "production", "previews", "mickeys-props-desk-2026-10-06.jpg")
PROPS = [("radio-base-station", "Radio base station and desk mic"), ("telephone", "Telephone"),
         ("jug-kettle", "Jug kettle"), ("mug", "Mug"), ("mug-chipped", "Mug, chipped"),
         ("ashtray", "Glass ashtray"), ("desk-lamp", "Desk lamp")]
LINEUP = os.path.join(PREVIEW_DIR, "desk-set-lineup.png")


def render_lineup():
    """Inside Blender: import the glbs in a row and render them."""
    import bpy
    from mathutils import Vector
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    order = ["desk-lamp", "radio-base-station", "telephone", "jug-kettle", "mug", "mug-chipped",
             "ashtray"]
    x = 0.0
    gap = 0.07
    for stem in order:
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=os.path.join(GLB_DIR, stem + ".glb"))
        objs = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
        lo = min(min((o.matrix_world @ Vector(c)).x for c in o.bound_box) for o in objs)
        hi = max(max((o.matrix_world @ Vector(c)).x for c in o.bound_box) for o in objs)
        for o in objs:
            o.location.x += x - lo
            # glTF viewers multiply base colour by COLOR_0; ours holds masks,
            # so for this preview the imported colour set is made white
            for ca in o.data.color_attributes:
                ca.data.foreach_set("color", [1.0] * (4 * len(ca.data)))
            for m in o.data.materials:
                b = m.node_tree.nodes.get("Principled BSDF") if m and m.node_tree else None
                if b and b.inputs["Transmission Weight"].default_value > 0:
                    for k, v in (("use_raytrace_refraction", True), ("surface_render_method", "DITHERED")):
                        if hasattr(m, k):
                            setattr(m, k, v)
        x += (hi - lo) + gap
    width = x - gap
    sc.render.engine = "BLENDER_EEVEE"
    if hasattr(sc.eevee, "use_raytracing"):
        sc.eevee.use_raytracing = True
    sc.render.resolution_x, sc.render.resolution_y = 1600, 640
    sc.view_settings.view_transform = "AgX"
    world = bpy.data.worlds.new("w")
    sc.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.2, 0.2, 0.2, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.35
    bpy.ops.mesh.primitive_plane_add(size=20, location=(width / 2, 0, 0))
    g = bpy.data.materials.new("ground")
    g.use_nodes = True
    g.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.105, 0.105, 0.105, 1)
    g.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.85
    bpy.context.active_object.data.materials.append(g)
    ctr = Vector((width / 2, -0.06, 0.30))
    az, el = math.radians(-12), math.radians(15)
    d = Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    cam.data.lens = 85
    fov = 2 * math.atan(18 / 85)                   # horizontal, sensor 36 mm
    cam.location = ctr + d * (width / 2 / math.tan(fov / 2) * 1.22)
    cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    for name, e, dv, size in (("key", 420, (-0.8, -1.0, 1.2), 2.0), ("fill", 110, (1.2, -0.6, 0.5), 2.6),
                              ("rim", 220, (0.4, 1.2, 0.9), 2.0)):
        ld = bpy.data.lights.new(name, "AREA")
        ld.energy, ld.size = e, size
        lo_ = bpy.data.objects.new(name, ld)
        sc.collection.objects.link(lo_)
        v = Vector(dv).normalized()
        lo_.location = ctr + v * 4.0
        lo_.rotation_euler = (-v).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = LINEUP
    bpy.ops.render.render(write_still=True)


def compose():
    from PIL import Image, ImageDraw, ImageFont
    W, TILE, LAB = 1600, 400, 44
    lineup = Image.open(LINEUP).convert("RGB")
    lineup = lineup.resize((W, int(lineup.height * W / lineup.width)))
    head = 46
    rows = 2
    H = head + lineup.height + 30 + rows * (TILE + LAB)
    sheet = Image.new("RGB", (W, H), (38, 38, 38))
    dr = ImageDraw.Draw(sheet)
    try:
        f_big = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 24)
        f = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 17)
        f_s = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 15)
    except OSError:
        f_big = f = f_s = ImageFont.load_default()
    dr.text((16, 9), "Mickey's front office - set 1, the desk props (6 October 2026)", fill=(235, 235, 235),
            font=f_big)
    sheet.paste(lineup, (0, head))
    dr.text((16, head + lineup.height + 5),
            "Together at true scale, left to right: desk lamp, radio set, telephone, jug kettle, two mugs, ashtray",
            fill=(200, 200, 200), font=f_s)
    y0 = head + lineup.height + 30
    for i, (stem, label) in enumerate(PROPS):
        r, c = divmod(i, 4)
        x, y = c * TILE, y0 + r * (TILE + LAB)
        im = Image.open(os.path.join(PREVIEW_DIR, stem + ".png")).convert("RGB").resize((TILE, TILE))
        sheet.paste(im, (x, y))
        info = json.load(open(os.path.join(PREVIEW_DIR, stem + ".json")))
        s = info["size_m"]
        dims = "%d x %d x %d mm" % (round(s["x"] * 1000), round(s["y"] * 1000), round(s["z"] * 1000))
        tris = info["glb_report"]["triangles"]
        dr.text((x + 10, y + TILE + 2), label, fill=(240, 240, 240), font=f)
        dr.text((x + 10, y + TILE + 22), "%s  |  %s tris" % (dims, format(tris, ",")),
                fill=(185, 185, 185), font=f_s)
    # the eighth tile: a key
    x, y = 3 * TILE, y0 + TILE + LAB
    notes = ["Sizes: width x depth x height, whole prop", "(radio with mic and lead; phone with", "its cord).",
             "", "Front toward the viewer, three-quarter", "view; Eevee preview, neutral grey", "ground.",
             "", "Each prop: one mesh, <= 3 plain", "materials, no textures; ao + edges", "masks in COLOR_0."]
    for k, line in enumerate(notes):
        dr.text((x + 18, y + 20 + k * 22), line, fill=(200, 200, 200), font=f_s)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    q = 86
    while True:
        sheet.save(OUT, "JPEG", quality=q, optimize=True, progressive=True)
        if os.path.getsize(OUT) < 490 * 1024 or q <= 50:
            break
        q -= 6
    print("contact sheet", OUT, sheet.size, os.path.getsize(OUT) // 1024, "KB, quality", q)


if __name__ == "__main__":
    try:
        import bpy  # noqa: F401
        render_lineup()
    except ImportError:
        if os.path.exists(LINEUP):
            os.remove(LINEUP)
        r = subprocess.run([BLENDER, "-b", "--factory-startup", "-P", os.path.abspath(__file__)],
                           capture_output=True, text=True)
        if not os.path.exists(LINEUP) or "Traceback" in r.stdout + r.stderr:
            print(r.stdout[-3000:], r.stderr[-3000:])
            sys.exit(1)
        compose()
