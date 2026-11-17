"""UNTESTED: needs the main session's run. The loft generator's Blender side (n16-9).

Written by the lane session, 17 November 2026, without Blender (the cloud has
none). It builds the hatch's body from tools/lane/car_loft.py's twelve
stations, so the shape is the one car_loft.py checks and draws:

    blender -b --factory-startup --python tools/lane/car_loft_blender.py -- \
        --out <a folder retention.json names>/hatch-p9.glb [--render-p9 <folder>]

What it does (2-VEHICLES.md 3.3, step 1):
- one fixed-topology mesh: each station's mirrored loop, neighbours joined by
  quads, the two ends capped (so later shape keys keep the same vertices);
- material slots by name for Unreal's masters: paint and glass (the rest of
  the kit, bumpers, lamps, plates, comes as modules on sockets later);
- subdivision at HatchParams.subdivision_levels, then weighted normals;
- the wheel arches cut by boolean, as tools/art-recipes/car-model.py does;
- two UV sets: UV0 for tiling, UV1 a unique layout for wear masks;
- with --render-p9: the four P9 views, untextured, orthographic side, front
  and rear plus a three-quarter, grey on white, for the blind test
  (production/lane/P9-BLIND-BRIEF.md).

First run checklist for the main session (expected to need fixes):
1. `python tools/retention.py space --job "car loft p9" --drives CF` first.
2. Run without --out once; read the printed face count (estimate: about 13,000
   body triangles at 2 levels) and that no error is printed.
3. If the boolean leaves holes, try solver "FAST" or cut before subdivision.
4. Then --render-p9 and the brief.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import car_loft  # noqa: E402


def args():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out = {"out": "", "render_p9": ""}
    i = 0
    while i < len(a):
        if a[i] == "--out" and i + 1 < len(a):
            out["out"] = a[i + 1]; i += 2
        elif a[i] == "--render-p9" and i + 1 < len(a):
            out["render_p9"] = a[i + 1]; i += 2
        else:
            i += 1
    return out


def material(bpy, name, rgb, rough):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    b.inputs["Roughness"].default_value = rough
    return m


def body_mesh(bpy, p):
    """The lofted body as one bmesh-built object, paint and glass slots."""
    import bmesh
    stations = car_loft.build(p)
    loops = [car_loft.full_loop(s) for s in stations]
    quads = car_loft.quads(p)          # the same order as below; carries the glass flag
    bm = bmesh.new()
    vloops = [[bm.verts.new(v) for v in loop] for loop in loops]
    n = len(vloops[0])
    qi = 0
    for i in range(len(vloops) - 1):
        a, b = vloops[i], vloops[i + 1]
        for j in range(n):
            k = (j + 1) % n
            f = bm.faces.new((a[j], a[k], b[k], b[j]))
            f.material_index = 1 if quads[qi][1] else 0
            qi += 1
    # end caps: the nose and the tail as n-gons (subdivision rounds them)
    bm.faces.new(vloops[0][::-1])
    bm.faces.new(vloops[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new("hatch_body")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("hatch_body", me)
    bpy.context.scene.collection.objects.link(ob)
    me.materials.append(material(bpy, "car_paint", (0.5, 0.5, 0.5), 0.3))
    me.materials.append(material(bpy, "car_glass", (0.05, 0.05, 0.06), 0.05))
    for poly in me.polygons:
        poly.use_smooth = True
    return ob


def cut_arches(bpy, ob, p):
    d = p.derived()
    for n, x in enumerate((d["front_axle"], d["rear_axle"])):
        bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=p.wheel_radius + p.arch_clearance,
                                            depth=p.width + 0.4, location=(x, 0.0, p.wheel_radius),
                                            rotation=(math.pi / 2, 0, 0))
        cut = bpy.context.active_object
        cut.name = "arch_cut_%d" % n
        m = ob.modifiers.new("arch%d" % n, "BOOLEAN")
        m.object, m.operation, m.solver = cut, "DIFFERENCE", "EXACT"
        cut.hide_render = cut.hide_viewport = True


def finish(bpy, ob, p):
    sub = ob.modifiers.new("sub", "SUBSURF")
    sub.levels = sub.render_levels = p.subdivision_levels
    # arches after subdivision, so the cut edge stays crisp
    cut_arches(bpy, ob, p)
    ob.modifiers.new("wn", "WEIGHTED_NORMAL")
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    for m in list(ob.modifiers):
        bpy.ops.object.modifier_apply(modifier=m.name)
    for o in list(bpy.data.objects):
        if o.name.startswith("arch_cut_"):
            bpy.data.objects.remove(o, do_unlink=True)
    # UV0 tiling, UV1 unique for wear masks
    me = ob.data
    while len(me.uv_layers) < 2:
        me.uv_layers.new()
    me.uv_layers[0].name, me.uv_layers[1].name = "UV0", "UV1_wear"
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    me.uv_layers.active_index = 0
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.01)
    me.uv_layers.active_index = 1
    bpy.ops.uv.lightmap_pack(PREF_MARGIN_DIV=0.2)
    bpy.ops.object.mode_set(mode="OBJECT")
    # origin at the car's centre on the ground, nose toward -x, as car-model.py
    ob.location.x -= p.length / 2
    bpy.ops.object.transform_apply(location=True)
    return ob


def wheels(bpy, p):
    """Plain tyres for the silhouette test only (the kit's wheels come later)."""
    d = p.derived()
    tyre = material(bpy, "tyre", (0.02, 0.02, 0.02), 0.9)
    out = []
    for x in (d["front_axle"], d["rear_axle"]):
        for s in (-1, 1):
            bpy.ops.mesh.primitive_cylinder_add(vertices=40, radius=p.wheel_radius, depth=p.tyre_width,
                                                location=(x - p.length / 2, s * p.track / 2, p.wheel_radius),
                                                rotation=(math.pi / 2, 0, 0))
            w = bpy.context.active_object
            w.data.materials.append(tyre)
            out.append(w)
    return out


def render_p9(bpy, folder, p):
    """Four untextured views, grey on white, for the blind silhouette test."""
    os.makedirs(folder, exist_ok=True)
    sc = bpy.context.scene
    for mat in bpy.data.materials:            # untextured: one grey for everything but tyres
        if mat.name != "tyre":
            b = mat.node_tree.nodes.get("Principled BSDF")
            b.inputs["Base Color"].default_value = (0.55, 0.55, 0.55, 1.0)
            b.inputs["Roughness"].default_value = 0.5
    w = bpy.data.worlds.new("w")
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sc.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(50), 0, math.radians(30))
    sun.data.energy = 3.0
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    r = sc.render
    r.engine = "BLENDER_EEVEE_NEXT"
    r.resolution_x, r.resolution_y = 1600, 900
    views = {
        # name: (location, rotation in degrees, orthographic)
        "side": ((0, -10, 0.7), (90, 0, 0), True),
        "front": ((-10, 0, 0.7), (90, 0, -90), True),
        "rear": ((10, 0, 0.7), (90, 0, 90), True),
        "three-quarter": ((-6.0, -5.2, 2.0), (78, 0, -49), False),
    }
    for name, (loc, rot, ortho) in views.items():
        cam.location = loc
        cam.rotation_euler = tuple(math.radians(v) for v in rot)
        cam.data.type = "ORTHO" if ortho else "PERSP"
        cam.data.ortho_scale = p.length * 1.15
        cam.data.lens = 50
        r.filepath = os.path.abspath(os.path.join(folder, "p9-%s.png" % name))
        bpy.ops.render.render(write_still=True)


def main():
    import bpy
    o = args()
    p = car_loft.HatchParams()
    fails = car_loft.check(p)
    if fails:
        print("car_loft check failed, not building:\n- " + "\n- ".join(fails))
        return 2
    bpy.ops.wm.read_factory_settings(use_empty=True)
    body = finish(bpy, body_mesh(bpy, p), p)
    parts = [body] + wheels(bpy, p)
    if o["render_p9"]:
        render_p9(bpy, o["render_p9"], p)
    if o["out"]:
        os.makedirs(os.path.dirname(os.path.abspath(o["out"])), exist_ok=True)
        for ob in bpy.data.objects:
            ob.select_set(ob is body)
        bpy.ops.export_scene.gltf(filepath=os.path.abspath(o["out"]), export_format="GLB",
                                  use_selection=True, export_apply=True, export_yup=True)
    tris = sum(len(poly.vertices) - 2 for poly in body.data.polygons)
    print("carLoft body_triangles=%d parts=%d out=%s" % (tris, len(parts), o["out"] or "none"))
    return 0


if __name__ == "__main__":
    try:
        rc = main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("car_loft_blender raised: %s" % str(e).splitlines()[0][:200]); rc = 3
    sys.exit(rc)
