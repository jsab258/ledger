"""The south quay kit: what Quay Street's south end looks out on, built by script.

    blender.exe -b --factory-startup -P tools/art-recipes/south-quay/south-quay.py -- --out <dir>
    python tools/art-recipes/south-quay/south-quay.py --selftest        # plain Python, no Blender

Blender 4.5: C:/LedgerTools/blender/4.5.13/blender-4.5.13-windows-x64/blender.exe

Arguments (after "--" in Blender):
    --out <dir>        where south-quay.glb and south-quay.report.json go
                       (default F:/LedgerTools/game-inputs/production/assets/south-quay)
    --street <glb>     the street's export, appended for the previews and checked at the joint
                       (default F:/LedgerTools/tmp/street-kit/quay-street.glb)
    --previews <dir>   where the two preview JPEGs go (default production/previews)
    --date <yyyy-mm-dd> the previews' date in their names (default today)
    --no-render        the glb and its report only
    --check-views <dir> also three work views (behind Tom at Mickey's window, the junction looking
                       east and west) into <dir>; never into production/previews
    --selftest         the plain-Python checks only (works inside Blender too)

The geometry is south_quay_geom.py's (plain Python). This script makes it Blender meshes, one
object per piece named "<material>__<piece>" with its material of the same street name, no
transforms; REFLECTS y to -y with every face re-wound, as terrace-front.py's street export does
(production/assets/street/quay-street.json "mirror"), so the glb sits beside quay-street.glb with
no transform; and writes the glb (glTF y up, metres) and a report. The previews are rendered in that
export frame, with the street's own glb appended (its south backdrop, which this kit replaces,
cut away for the picture only).
"""
import datetime
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import south_quay_geom as G  # noqa: E402

ROOT = G.ROOT
DEFAULT_OUT = "F:/LedgerTools/game-inputs/production/assets/south-quay"
DEFAULT_STREET = "F:/LedgerTools/tmp/street-kit/quay-street.glb"
STREET_SIDECAR_REL = "production/assets/street/quay-street.json"
#: Mickey's door, the gate's view: on the east footway 0.8 m out from his front, 1.6 m above the
#: footway, looking south down Quay Street with a 60-degree horizontal field (recipe frame).
EYE_RECIPE = (4.6, 4.3)
EYE_HEIGHT_M = 1.6
EYE_HFOV_DEG = 60.0
PREVIEW_W, PREVIEW_H = 1600, 900
#: The plan's window, recipe frame: x (north) and y (east) ranges.
PLAN_X = (-190.0, 45.0)
PLAN_Y = (-190.0, 228.0)


def parse_args(argv):
    a = {"out": DEFAULT_OUT, "street": DEFAULT_STREET, "previews": os.path.join(ROOT, "production", "previews"),
         "date": datetime.date.today().isoformat(), "render": True, "selftest": False}
    i = 0
    while i < len(argv):
        k = argv[i]
        if k == "--selftest":
            a["selftest"] = True
        elif k == "--check-views" and i + 1 < len(argv):
            a["check_views"] = argv[i + 1]
            i += 1
        elif k == "--no-render":
            a["render"] = False
        elif k in ("--out", "--street", "--previews", "--date") and i + 1 < len(argv):
            a[k[2:]] = argv[i + 1]
            i += 1
        i += 1
    return a


def gpu_busy():
    """True while Unreal or the build machine's runner holds the card (the kit's rule)."""
    try:
        out = subprocess.run(["tasklist"], capture_output=True, text=True, timeout=20).stdout.lower()
    except Exception:
        return False
    return "unrealeditor" in out or "runner.worker" in out


# =================================================================================================
# Blender
# =================================================================================================
def make_material(bpy, name, rgb, rough, emit=None, backface_cull=True):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = 0.0
    if emit is not None:
        bsdf.inputs["Emission Color"].default_value = (emit[0], emit[1], emit[2], 1.0)
        bsdf.inputs["Emission Strength"].default_value = emit[3]
    m.diffuse_color = (rgb[0], rgb[1], rgb[2], 1.0)
    m.roughness = rough
    # single-sided, as Unreal draws them: a face wound the wrong way shows as a hole
    m.use_backface_culling = backface_cull
    return m


def build_objects(bpy, pieces, mats):
    import bmesh
    coll = bpy.data.collections.new("south_quay")
    bpy.context.scene.collection.children.link(coll)
    objs = []
    for key in sorted(pieces):
        p = pieces[key]
        me = bpy.data.meshes.new(key)
        me.from_pydata(p["verts"], [], p["faces"])
        me.validate(clean_customdata=False)
        # UVs in metres by each face's own axis, as the street's export does
        uv = me.uv_layers.new(name="UVMap")
        for poly in me.polygons:
            n = poly.normal
            ax, ay, az = abs(n.x), abs(n.y), abs(n.z)
            for li in poly.loop_indices:
                co = me.vertices[me.loops[li].vertex_index].co
                if az >= ax and az >= ay:
                    uv.data[li].uv = (co.x, co.y)
                elif ax >= ay:
                    uv.data[li].uv = (co.y, co.z)
                else:
                    uv.data[li].uv = (co.x, co.z)
        if p.get("smooth"):
            me.shade_smooth()
            try:
                me.set_sharp_from_angle(angle=math.radians(40.0))
            except Exception:
                pass
        else:
            me.shade_flat()
        rgb, rough = mats[p["material"]]
        me.materials.append(bpy.data.materials.get(p["material"]))
        ob = bpy.data.objects.new(key, me)
        coll.objects.link(ob)
        objs.append(ob)
    return coll, objs


def export_glb(bpy, objs, path):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_apply=True,
                              export_yup=True, export_texcoords=True, export_normals=True,
                              export_materials="EXPORT", export_cameras=False, export_lights=False,
                              export_extras=False)


def import_street(bpy, path, root):
    """The street's glb in its own collection, coloured from its sidecar; its south backdrop (the
    apron box, sheds and crane at x < -2, which this kit replaces) cut away for the picture."""
    import bmesh
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    side = {}
    try:
        for row in json.load(open(os.path.join(root, STREET_SIDECAR_REL), encoding="utf-8"))["meshes"]:
            side[row["mesh"]] = row
    except (OSError, ValueError, KeyError):
        pass
    bpy.context.view_layer.update()
    cut = 0
    for o in list(new):
        if o.type != "MESH":
            continue
        row = side.get(o.data.name) or side.get(o.name)
        # what the game shows only when something happens (a broken pane, the office's door open)
        if row and row.get("reveal_on"):
            bpy.data.objects.remove(o, do_unlink=True)
            new.remove(o)
            continue
        bm = bmesh.new()
        bm.from_mesh(o.data)
        M = o.matrix_world
        lim = -1.99 if o.name.startswith("street_stone") else -2.05
        dead = [v for v in bm.verts if (M @ v.co).x < lim]
        cut += len(dead)
        bmesh.ops.delete(bm, geom=dead, context="VERTS")
        bm.to_mesh(o.data)
        bm.free()
        if not row:
            continue
        rgb = row.get("linear_rgb") or [0.3, 0.3, 0.3]
        tint = row.get("house_tint") or [1.0, 1.0, 1.0]
        rgb = [rgb[i] * tint[i] for i in range(3)]
        emit = None
        if row.get("emit_day"):
            emit = (rgb[0], rgb[1], rgb[2], float(row["emit_day"]))
        m = make_material(bpy, "street::" + row["material"], rgb, row.get("roughness") or 0.6, emit)
        o.data.materials.clear()
        o.data.materials.append(m)
    return new, cut


def world_and_light(bpy, scene, sky_h=(0.60, 0.63, 0.66), sky_z=(0.36, 0.41, 0.48)):
    w = bpy.data.worlds.new("overcast")
    scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    bg = nt.nodes.new("ShaderNodeBackground")
    out = nt.nodes.new("ShaderNodeOutputWorld")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (sky_h[0] * 0.55, sky_h[1] * 0.55, sky_h[2] * 0.55, 1)
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[1].color = (sky_z[0], sky_z[1], sky_z[2], 1)
    e = ramp.color_ramp.elements.new(0.5)
    e.color = (sky_h[0], sky_h[1], sky_h[2], 1)
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = 1.0
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    sun = bpy.data.lights.new("sun", "SUN")
    sun.energy = 1.2
    sun.angle = math.radians(25.0)
    so = bpy.data.objects.new("sun", sun)
    scene.collection.objects.link(so)
    # high and to the south-west of the view (export frame: west is +y)
    so.rotation_euler = (math.radians(40.0), 0.0, math.radians(-60.0))
    return w, so


def setup_render(bpy, scene, cpu):
    scene.render.resolution_x, scene.render.resolution_y = PREVIEW_W, PREVIEW_H
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "JPEG"
    scene.render.image_settings.quality = 86
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.exposure = 0.0
    if cpu:
        scene.render.engine = "CYCLES"
        scene.cycles.device = "CPU"
        scene.cycles.samples = 48
        scene.cycles.use_denoising = True
        scene.render.threads_mode = "FIXED"
        scene.render.threads = 6
    else:
        scene.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in [
            e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items] else "BLENDER_EEVEE"
        ee = scene.eevee
        ee.taa_render_samples = 64
        for attr, val in (("use_raytracing", True), ("use_shadows", True), ("use_gtao", True)):
            if hasattr(ee, attr):
                setattr(ee, attr, val)


def mist_composite(bpy, scene, start, depth, colour, on=True):
    vl = scene.view_layers[0]
    vl.use_pass_mist = on
    scene.world.mist_settings.start = start
    scene.world.mist_settings.depth = depth
    scene.world.mist_settings.falloff = "QUADRATIC"
    scene.use_nodes = True
    nt = scene.node_tree
    nt.nodes.clear()
    rl = nt.nodes.new("CompositorNodeRLayers")
    comp = nt.nodes.new("CompositorNodeComposite")
    if not on:
        nt.links.new(rl.outputs["Image"], comp.inputs["Image"])
        return
    mix = nt.nodes.new("CompositorNodeMixRGB")
    mix.blend_type = "MIX"
    mul = nt.nodes.new("CompositorNodeMath")
    mul.operation = "MULTIPLY"
    mul.inputs[1].default_value = 0.55
    nt.links.new(rl.outputs["Mist"], mul.inputs[0])
    nt.links.new(mul.outputs[0], mix.inputs[0])
    nt.links.new(rl.outputs["Image"], mix.inputs[1])
    mix.inputs[2].default_value = (colour[0], colour[1], colour[2], 1.0)
    nt.links.new(mix.outputs[0], comp.inputs["Image"])


def eye_camera(bpy, scene, jn):
    cam = bpy.data.cameras.new("mickeys_door")
    cam.sensor_fit = "HORIZONTAL"
    cam.angle = math.radians(EYE_HFOV_DEG)
    cam.clip_start = 0.05
    cam.clip_end = 20000.0
    ob = bpy.data.objects.new("mickeys_door", cam)
    scene.collection.objects.link(ob)
    fz = jn.footway_z_at(abs(EYE_RECIPE[1]) - jn.half - jn.kerb_w)
    ob.location = (EYE_RECIPE[0], -EYE_RECIPE[1], fz + EYE_HEIGHT_M)   # export frame: y reflected
    ob.rotation_euler = (math.radians(90.0), 0.0, math.radians(90.0))  # looking along -x, z up
    scene.camera = ob
    return ob


def plan_camera(bpy, scene):
    cam = bpy.data.cameras.new("plan")
    cam.type = "ORTHO"
    cam.sensor_fit = "HORIZONTAL"
    cam.ortho_scale = PLAN_Y[1] - PLAN_Y[0]
    cam.clip_start = 1.0
    cam.clip_end = 500.0
    ob = bpy.data.objects.new("plan", cam)
    scene.collection.objects.link(ob)
    cx = (PLAN_X[0] + PLAN_X[1]) / 2.0
    cy = -(PLAN_Y[0] + PLAN_Y[1]) / 2.0
    ob.location = (cx, cy, 200.0)
    ob.rotation_euler = (0.0, 0.0, math.radians(-90.0))   # north (+x) up, east (-y export) right
    scene.camera = ob
    return ob


def overlay_lines(bpy, scene, at, z=60.0):
    """The atlas's coast, roads and blocks as flat lines over the plan (export frame)."""
    A = at["atlas"]
    coll = bpy.data.collections.new("atlas_overlay")
    scene.collection.children.link(coll)
    styles = {"coast": ((0.02, 0.45, 0.95), 0.9), "road": ((1.0, 0.42, 0.02), 0.8),
              "foot": ((1.0, 0.85, 0.10), 0.5), "block": ((0.95, 0.10, 0.75), 0.6)}
    mats = {}
    for k, (c, _w) in styles.items():
        m = bpy.data.materials.new("overlay_" + k)
        m.use_nodes = True
        nt = m.node_tree
        nt.nodes.clear()
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Color"].default_value = (c[0], c[1], c[2], 1)
        em.inputs["Strength"].default_value = 3.0
        o = nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(em.outputs[0], o.inputs["Surface"])
        mats[k] = m

    def poly(name, pts, style, closed=False, dash=None):
        w = styles[style][1]
        P = [G.atlas_to_recipe(p) for p in pts]
        if closed:
            P = P + [P[0]]
        verts, faces = [], []
        for a, b in zip(P[:-1], P[1:]):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            if L < 1e-6:
                continue
            d = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
            n = (-d[1] * w / 2, d[0] * w / 2)
            segs = [(0.0, L)]
            if dash:
                segs, s = [], 0.0
                while s < L:
                    segs.append((s, min(L, s + dash)))
                    s += dash * 2
            for s0, s1 in segs:
                p0 = (a[0] + d[0] * s0, a[1] + d[1] * s0)
                p1 = (a[0] + d[0] * s1, a[1] + d[1] * s1)
                k = len(verts)
                for q in ((p0[0] - n[0], p0[1] - n[1]), (p1[0] - n[0], p1[1] - n[1]),
                          (p1[0] + n[0], p1[1] + n[1]), (p0[0] + n[0], p0[1] + n[1])):
                    verts.append((q[0], -q[1], z))      # export frame
                faces.append((k, k + 3, k + 2, k + 1))
        me = bpy.data.meshes.new(name)
        me.from_pydata(verts, [], faces)
        me.materials.append(mats[style])
        ob = bpy.data.objects.new(name, me)
        coll.objects.link(ob)

    poly("atlas_coast", A["land"], "coast", closed=True)
    for r in A["routes"]:
        if r["id"] in ("quay", "harbourlink", "coast"):
            poly("atlas_route_" + r["id"], r["points"], "road")
        elif r["id"] in ("yardlane", "dockfoot"):
            poly("atlas_route_" + r["id"], r["points"], "foot", dash=3.0)
    for name, e, n, w, h in A["blocks"]:
        poly("atlas_block_" + name, [(e, n), (e + w, n), (e + w, n + h), (e, n + h)], "block", closed=True, dash=2.5)
    # the legend and a 50 m scale bar, as text and lines in the picture's lower left
    def text(s, x, y, size, colour):
        cu = bpy.data.curves.new("t", "FONT")
        cu.body = s
        cu.size = size
        ob = bpy.data.objects.new("label", cu)
        ob.location = (x, -y, z + 1)
        ob.rotation_euler = (0, 0, math.radians(-90.0))
        m = bpy.data.materials.new("label")
        m.use_nodes = True
        nt = m.node_tree
        nt.nodes.clear()
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Color"].default_value = (colour[0], colour[1], colour[2], 1)
        em.inputs["Strength"].default_value = 2.5
        o = nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(em.outputs[0], o.inputs["Surface"])
        cu.materials.append(m)
        coll.objects.link(ob)
    x0, y0 = PLAN_X[1] - 8.0, PLAN_Y[0] + 6.0
    # a dark panel under the legend
    panel = bpy.data.meshes.new("legend_panel")
    px0, px1, py0, py1 = x0 - 40.0, x0 + 4.0, y0 - 4.0, y0 + 112.0
    panel.from_pydata([(px0, -py0, z - 0.5), (px0, -py1, z - 0.5), (px1, -py1, z - 0.5), (px1, -py0, z - 0.5)], [],
                      [(0, 1, 2, 3)])
    pm = bpy.data.materials.new("legend_panel")
    pm.use_nodes = True
    pnt = pm.node_tree
    pnt.nodes.clear()
    pe = pnt.nodes.new("ShaderNodeEmission")
    pe.inputs["Color"].default_value = (0.03, 0.035, 0.04, 1)
    po = pnt.nodes.new("ShaderNodeOutputMaterial")
    pnt.links.new(pe.outputs[0], po.inputs["Surface"])
    panel.materials.append(pm)
    pob = bpy.data.objects.new("legend_panel", panel)
    coll.objects.link(pob)
    text("ATLAS 01 OVER THE SOUTH QUAY KIT (plan, north up)", x0 - 6, y0, 4.6, (1, 1, 1))
    text("blue: atlas coast", x0 - 13, y0, 4.0, styles["coast"][0])
    text("orange: atlas roads   yellow dashed: atlas footways", x0 - 19, y0, 4.0, styles["road"][0])
    text("magenta dashed: atlas massing blocks", x0 - 25, y0, 4.0, styles["block"][0])
    for s_, (lx, ly) in (("Mickey's", (5.0, 15.0)), ("junction", (-25.0, -14.0)), ("Old Basin", (-92.0, -45.0)),
                         ("jetty and light", (-124.0, -80.0)), ("Harbour Board approach", (-46.0, 64.0)),
                         ("quay edge x = -70", (-66.0, -98.0)), ("east quay warehouses", (-110.0, 74.0)),
                         ("open sea", (-160.0, -10.0))):
        text(s_, lx, ly, 3.6, (1, 1, 1))
    # scale bar, 50 m along east
    me = bpy.data.meshes.new("scale_bar")
    yb, xb = y0, x0 - 33.0
    me.from_pydata([(xb, -yb, z), (xb, -(yb + 50), z), (xb + 1.2, -(yb + 50), z), (xb + 1.2, -yb, z)], [],
                   [(0, 3, 2, 1)])
    me.materials.append(mats["foot"])
    sb = bpy.data.objects.new("scale_bar", me)
    coll.objects.link(sb)
    text("50 m", xb - 5.0, yb + 52.0, 4.0, styles["foot"][0])
    return coll


def render(bpy, scene, path):
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    return os.path.getsize(path) if os.path.exists(path) else -1


def main_blender(a):
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    kit, jn, info = G.build(ROOT)
    mats = G.all_materials(ROOT)
    pieces = G.reflected(kit.pieces)
    for name in sorted(set(p["material"] for p in pieces.values())):
        rgb, rough = mats[name]
        emit = (rgb[0], rgb[1], rgb[2], 0.0)
        make_material(bpy, name, rgb, rough)
    coll, objs = build_objects(bpy, pieces, mats)
    os.makedirs(a["out"], exist_ok=True)
    glb = os.path.join(a["out"], "south-quay.glb")
    export_glb(bpy, objs, glb)
    # the report
    tris = {k: sum(len(f) - 2 for f in p["faces"]) for k, p in pieces.items()}
    used = sorted(set(p["material"] for p in pieces.values()))
    street_mats = G.read_street_materials(ROOT)
    allv = [v for p in pieces.values() for v in p["verts"] if abs(v[0]) < 1000 and abs(v[1]) < 1000]
    report = {
        "what": "The south quay kit: Quay Street's south end as the atlas has it. tools/art-recipes/south-quay/"
                "south-quay.py; README production/art/south-quay/README.md.",
        "frame": "export frame: the recipe frame (x along Quay Street, y east, z up, metres) REFLECTED y to -y, "
                 "faces re-wound, as quay-street.glb; glTF is y up. East arrives at Unreal +Y.",
        "glb": glb.replace("\\", "/"), "bytes": os.path.getsize(glb),
        "triangles": sum(tris.values()), "budget": G.TRI_BUDGET,
        "nodes": len(pieces),
        "materials": {m: {"linear_rgb": list(mats[m][0]), "roughness": mats[m][1],
                          "new": m not in street_mats,
                          "why": G.KIT_NEW_MATERIALS[m][2] if m in G.KIT_NEW_MATERIALS else None} for m in used},
        "pieces": {k: {"material": pieces[k]["material"], "triangles": tris[k]} for k in sorted(pieces)},
        "levels_recipe_frame": {"road_crown": 0.0, "channel": jn.channel_z, "kerb_top": jn.kerb_top,
                                "footway_back": info["yard_z"], "apron_and_cope": info["apron_z"],
                                "half_tide_water": info["water_z"]},
        "joins_street_at_x": jn.join_x, "junction": list(jn.J), "quay_edge_x": info["quay_edge_x"],
        "water_far_x": info["water_far_x"], "water_half_y": info["water_half_y"],
        "bounds_near_export_frame": {"x": [min(v[0] for v in allv), max(v[0] for v in allv)],
                                     "y": [min(v[1] for v in allv), max(v[1] for v in allv)],
                                     "z": [min(v[2] for v in allv), max(v[2] for v in allv)]},
        "built": datetime.datetime.now().isoformat(timespec="seconds"),
        "blender": bpy.app.version_string,
    }
    with open(os.path.join(a["out"], "south-quay.report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    print("sqExport glb=%s bytes=%d nodes=%d tris=%d materials=%d"
          % (glb, report["bytes"], len(pieces), report["triangles"], len(used)))
    # re-import the glb and count, so what is written is what is reported
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=glb)
    back = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
    t_back = 0
    bad_names = []
    for o in back:
        o.data.calc_loop_triangles()
        t_back += len(o.data.loop_triangles)
        mname = o.data.materials[0].name if o.data.materials else ""
        if o.name.split("__")[0] != mname.split(".")[0]:
            bad_names.append(o.name)
        if any(abs(c) > 1e-9 for c in o.location) or any(abs(c) > 1e-9 for c in o.rotation_euler) \
                or any(abs(c - 1) > 1e-9 for c in o.scale):
            bad_names.append(o.name + "(transform)")
    print("sqReimport objects=%d tris=%d bad=%s" % (len(back), t_back, bad_names[:5]))
    for o in back:
        bpy.data.objects.remove(o, do_unlink=True)
    report["reimport"] = {"objects": len(back), "triangles": t_back, "name_or_transform_faults": bad_names}
    with open(os.path.join(a["out"], "south-quay.report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    if not a["render"]:
        return
    # ---- the previews --------------------------------------------------------------------------
    cpu = gpu_busy()
    world_and_light(bpy, scene)
    setup_render(bpy, scene, cpu)
    street_objs, cut = [], 0
    if a["street"] and os.path.isfile(a["street"]):
        street_objs, cut = import_street(bpy, a["street"], ROOT)
    print("sqStreet objects=%d backdrop_vertices_cut=%d engine=%s" % (len(street_objs), cut, scene.render.engine))
    os.makedirs(a["previews"], exist_ok=True)
    eye_camera(bpy, scene, jn)
    mist_composite(bpy, scene, 35.0, 1400.0, (0.50, 0.52, 0.55), on=True)
    p1 = os.path.join(a["previews"], "south-quay-from-mickeys-%s.jpg" % a["date"])
    s1 = render(bpy, scene, p1)
    print("sqPreview %s bytes=%d" % (p1, s1))
    if a.get("check_views"):
        # the gate's failing frame (step-025): behind Tom at Mickey's window, looking east-south-east
        # past the gable; and the junction looking east up the approach. Work pictures only.
        for tag, (ex, ey, ez), (tx, ty), fov in (("tom-at-window", (7.5, 0.6, 1.9), (-0.45, 1.0), 85.0),
                                                 ("junction-east", (-31.0, -2.0, 1.7), (-0.05, 1.0), 70.0),
                                                 ("junction-west", (-30.0, 2.0, 1.7), (-0.2, -1.0), 70.0)):
            cam = bpy.data.cameras.new(tag)
            cam.sensor_fit = "HORIZONTAL"
            cam.angle = math.radians(fov)
            cam.clip_end = 20000.0
            ob = bpy.data.objects.new(tag, cam)
            scene.collection.objects.link(ob)
            ob.location = (ex, -ey, ez)
            yaw = math.atan2(-ty, tx)                       # export frame: y reflected
            ob.rotation_euler = (math.radians(90.0), 0.0, yaw - math.radians(90.0))
            scene.camera = ob
            os.makedirs(a["check_views"], exist_ok=True)
            pc = os.path.join(a["check_views"], "check-%s.jpg" % tag)
            print("sqCheck %s bytes=%d" % (pc, render(bpy, scene, pc)))
    plan_camera(bpy, scene)
    mist_composite(bpy, scene, 0.0, 1.0, (0, 0, 0), on=False)
    overlay_lines(bpy, scene, G.read_atlas(ROOT))
    p2 = os.path.join(a["previews"], "south-quay-plan-%s.jpg" % a["date"])
    s2 = render(bpy, scene, p2)
    print("sqPreview %s bytes=%d" % (p2, s2))


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    a = parse_args(argv)
    if a["selftest"]:
        ok, lines, info, kit = G.selftest(ROOT, street_glb=a["street"])
        print("sqSelftest %s" % ("PASS" if ok else "FAIL"))
        if "bpy" not in sys.modules:
            sys.exit(0 if ok else 1)
        return
    main_blender(a)


if __name__ == "__main__":
    main()
