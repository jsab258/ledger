"""A parked car for the street: a generic late-1980s hatchback, no make's, as a glb.

    blender -b --factory-startup --python tools/art-recipes/car-model.py -- \
        --paint 0.035,0.042,0.075 --out production/assets/vehicles/hatch-navy.glb \
        [--render preview.png]

WHY IT EXISTS, 23 September. Jafar's presentable checklist: "nothing in frame
is a placeholder: cars and props are real-looking models rather than shapes,
with no recognisable real car model". The street's car was an outline pushed
sideways (terrace-front.py _vehicles): flat flanks, a glasshouse the width of
the body, a box. The car kits held on disk are toys. So it is built here, the
way a modeller would block it: a rounded lower body with the arches cut out
of it, a glasshouse that narrows to the roof with the pillars and roof in the
paint and the openings in glass, black bumpers, lamps, plates, mirrors,
wheels with tyres and hubs, all smoothed.

NOT ANY MAKE'S. The proportions are the class average the street recipe
already uses (4.12 m, 1.64 m, 1.42 m, a 2.5 m wheelbase on 13-inch wheels);
no grille shape, badge, lamp graphic or glasshouse line is taken from a real
car, which canon forbids.
"""
import math
import os
import sys

L, W, H = 4.12, 1.64, 1.42          # length, width, height (m)
WB, TR = 2.50, 1.38                 # wheelbase, track
WHEEL_R, TYRE_W = 0.289, 0.175      # 175/70 R13: 0.578 m across
FRONT_AXLE = 0.80                   # from the nose
BELT_Z, SILL_Z = 0.92, 0.30
ROOF_Z = H


def args():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out = {"paint": "0.035,0.042,0.075", "out": "", "render": ""}
    i = 0
    while i < len(a):
        if a[i] in ("--paint", "--out", "--render") and i + 1 < len(a):
            out[a[i][2:]] = a[i + 1]; i += 2
        else:
            i += 1
    out["paint"] = tuple(float(v) for v in out["paint"].split(","))
    return out


def material(bpy, name, rgb, rough, metal=0.0, emit=None):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit is not None:
        b.inputs["Emission Color"].default_value = (emit[0], emit[1], emit[2], 1.0)
        b.inputs["Emission Strength"].default_value = 0.0
    return m


def box(bpy, name, x0, x1, y0, y1, z0, z1, mat, bevel=0.0, segs=3):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    o = bpy.context.active_object
    o.name = name
    o.scale = (x1 - x0, y1 - y0, z1 - z0)
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(mat)
    if bevel > 0:
        m = o.modifiers.new("bev", "BEVEL")
        m.width, m.segments, m.limit_method = bevel, segs, "NONE"
    return o


def lower_body(bpy, paint):
    """The tub: a box from bumper line to belt, the bonnet falling to the nose
    and the tail's top edge turned, the corners rounded, then smoothed."""
    import bmesh
    o = box(bpy, "body", 0.06, L - 0.06, -W / 2, W / 2, SILL_Z, BELT_Z, paint, bevel=0.12, segs=4)
    bm = bmesh.new()
    bm.from_mesh(o.data)
    for v in bm.verts:
        if v.co.z > 0.8 and v.co.x < 0.5:          # the bonnet falls to the nose
            v.co.z -= 0.16
        if v.co.x < 0.5:                             # the nose pulled in at its corners
            v.co.y *= 0.94
        if v.co.x > L - 0.5:                         # the tail's corners turned
            v.co.y *= 0.96
    bm.to_mesh(o.data)
    bm.free()
    sub = o.modifiers.new("sub", "SUBSURF")
    sub.levels = sub.render_levels = 2
    return o


def arches(bpy, body):
    """Wheel arches cut out of the tub, a little larger than the tyre."""
    for n, x in enumerate((FRONT_AXLE, FRONT_AXLE + WB)):
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=WHEEL_R + 0.045, depth=W + 0.4,
                                            location=(x, 0.0, WHEEL_R), rotation=(math.pi / 2, 0, 0))
        cut = bpy.context.active_object
        cut.name = "arch_cut_%d" % n
        m = body.modifiers.new("arch%d" % n, "BOOLEAN")
        m.object, m.operation, m.solver = cut, "DIFFERENCE", "EXACT"
        cut.hide_render = True
        cut.hide_viewport = True
    return body


def glasshouse(bpy, paint, glass):
    """The cabin above the belt: glass all round, narrowing to the roof, the
    windscreen raked and the hatch sloped; the roof and the pillars in the
    paint, set just proud of the glass."""
    import bmesh
    x0, x1 = 1.18, L - 0.34                  # windscreen foot, hatch foot
    xr0, xr1 = 1.85, L - 0.72                # roof front and back
    inset = 0.11                              # the narrowing each side
    bm = bmesh.new()
    y0, yt = W / 2 - 0.03, W / 2 - 0.03 - inset
    zb, zt = BELT_Z - 0.02, ROOF_Z - 0.04
    base = [bm.verts.new(p) for p in ((x0, -y0, zb), (x1, -y0, zb), (x1, y0, zb), (x0, y0, zb))]
    top = [bm.verts.new(p) for p in ((xr0, -yt, zt), (xr1, -yt, zt), (xr1, yt, zt), (xr0, yt, zt))]
    bm.faces.new(base[::-1])
    bm.faces.new(top)
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((base[i], base[j], top[j], top[i]))
    me = bpy.data.meshes.new("glass")
    bm.to_mesh(me)
    bm.free()
    g = bpy.data.objects.new("glass", me)
    bpy.context.scene.collection.objects.link(g)
    g.data.materials.append(glass)
    bev = g.modifiers.new("bev", "BEVEL")
    bev.width, bev.segments, bev.limit_method = 0.05, 3, "NONE"
    # THE ROOF, a panel over the glass, and the PILLARS: A at the screen's
    # sides, B between the doors, C at the hatch's sides, each a slim strip
    # in the paint laid on the glass so the windows read as openings.
    roof = box(bpy, "roof", xr0 - 0.04, xr1 + 0.04, -yt - 0.01, yt + 0.01, zt - 0.01, zt + 0.035,
               paint, bevel=0.03)
    parts = [g, roof]

    def strip(name, p0, p1, width):
        """A pillar from p0 to p1 (x, z) on both sides, sitting on the glass."""
        for side in (-1, 1):
            bm = bmesh.new()
            (xa, za), (xb, zb2) = p0, p1
            ya = side * (y0 - (za - zb) / (zt - zb) * inset + 0.012)
            yb = side * (y0 - (zb2 - zb) / (zt - zb) * inset + 0.012)
            vs = [bm.verts.new(v) for v in ((xa - width / 2, ya, za), (xa + width / 2, ya, za),
                                             (xb + width / 2, yb, zb2), (xb - width / 2, yb, zb2))]
            bm.faces.new(vs if side > 0 else vs[::-1])
            me = bpy.data.meshes.new(name)
            bm.to_mesh(me)
            bm.free()
            ob = bpy.data.objects.new("%s_%d" % (name, side), me)
            bpy.context.scene.collection.objects.link(ob)
            ob.data.materials.append(paint)
            sol = ob.modifiers.new("sol", "SOLIDIFY")
            sol.thickness = 0.02
            parts.append(ob)
    strip("pillar_a", (x0 + 0.03, zb + 0.02), (xr0 + 0.02, zt), 0.09)
    strip("pillar_b", (2.52, zb + 0.02), (2.47, zt), 0.08)
    strip("pillar_c", (x1 - 0.10, zb + 0.02), (xr1 - 0.08, zt), 0.22)
    return parts


def wheel(bpy, x, side, tyre, hub):
    y = side * (TR / 2)
    bpy.ops.mesh.primitive_cylinder_add(vertices=40, radius=WHEEL_R, depth=TYRE_W,
                                        location=(x, y, WHEEL_R), rotation=(math.pi / 2, 0, 0))
    t = bpy.context.active_object
    t.name = "tyre_%d_%d" % (int(x * 10), side)
    t.data.materials.append(tyre)
    b = t.modifiers.new("bev", "BEVEL")
    b.width, b.segments, b.limit_method = 0.05, 3, "NONE"
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=WHEEL_R * 0.62, depth=0.02,
                                        location=(x, y + side * (TYRE_W / 2 + 0.002), WHEEL_R),
                                        rotation=(math.pi / 2, 0, 0))
    h = bpy.context.active_object
    h.name = "hub_%d_%d" % (int(x * 10), side)
    h.data.materials.append(hub)
    return [t, h]


def details(bpy, mats):
    out = []
    # BUMPERS, moulded black plastic wrapping the ends.
    out.append(box(bpy, "bumper_f", -0.02, 0.16, -W / 2 + 0.02, W / 2 - 0.02, 0.30, 0.47, mats["trim"], 0.05))
    out.append(box(bpy, "bumper_r", L - 0.16, L + 0.02, -W / 2 + 0.02, W / 2 - 0.02, 0.30, 0.47, mats["trim"], 0.05))
    # HEADLAMPS and a plain slatted grille between them - no make's shape.
    for s in (-1, 1):
        out.append(box(bpy, "lamp_f_%d" % s, 0.035, 0.075, s * 0.50 - 0.16, s * 0.50 + 0.16, 0.56, 0.68,
                       mats["lens"], 0.01))
        out.append(box(bpy, "lamp_r_%d" % s, L - 0.08, L - 0.04, s * 0.60 - 0.10, s * 0.60 + 0.10, 0.55, 0.80,
                       mats["red"], 0.01))
        # MIRRORS on the doors, at the screen's foot.
        out.append(box(bpy, "mirror_%d" % s, 1.20, 1.30, s * (W / 2 - 0.04) - 0.07, s * (W / 2 - 0.04) + 0.07,
                       0.94, 1.03, mats["trim"], 0.02))
    out.append(box(bpy, "grille", 0.04, 0.08, -0.32, 0.32, 0.58, 0.66, mats["trim"], 0.01))
    # PLATES: white in front and yellow behind, the law since 1973.
    out.append(box(bpy, "plate_f", -0.035, -0.02, -0.26, 0.26, 0.35, 0.46, mats["plate_f"]))
    out.append(box(bpy, "plate_r", L + 0.02, L + 0.035, -0.26, 0.26, 0.52, 0.63, mats["plate_r"]))
    # A RUBBING STRIP along each flank, and the SILLS dark under the doors.
    for s in (-1, 1):
        out.append(box(bpy, "strip_%d" % s, 0.40, L - 0.40, s * (W / 2) - 0.012, s * (W / 2) + 0.012,
                       0.60, 0.64, mats["trim"]))
    return out


def build(paint_rgb):
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mats = {
        "paint": material(bpy, "car_paint", paint_rgb, 0.22),
        "glass": material(bpy, "car_glass", (0.02, 0.022, 0.026), 0.06),
        "trim": material(bpy, "car_trim", (0.018, 0.018, 0.019), 0.55),
        "tyre": material(bpy, "tyre", (0.012, 0.012, 0.012), 0.88),
        "hub": material(bpy, "car_hub", (0.16, 0.16, 0.17), 0.45, 0.3),   # pressed steel, dulled
        "lens": material(bpy, "lamp_clear", (0.42, 0.42, 0.40), 0.12),
        "red": material(bpy, "lamp_red", (0.16, 0.012, 0.010), 0.22),
        "plate_f": material(bpy, "plate_front", (0.56, 0.56, 0.54), 0.5),
        "plate_r": material(bpy, "plate_rear", (0.48, 0.38, 0.035), 0.5),
    }
    body = arches(bpy, lower_body(bpy, mats["paint"]))
    parts = [body] + glasshouse(bpy, mats["paint"], mats["glass"]) + details(bpy, mats)
    for x in (FRONT_AXLE, FRONT_AXLE + WB):
        for s in (-1, 1):
            parts += wheel(bpy, x, s, mats["tyre"], mats["hub"])
    # THE ORIGIN AT THE CAR'S CENTRE ON THE GROUND, the nose toward -x, so
    # the probe places it by its footprint's centre and turns it by its yaw.
    for p in parts:
        p.location.x -= L / 2
    # ONE OBJECT, every modifier applied, so the engine imports one car with
    # its materials as sections rather than thirty meshes.
    for ob in bpy.data.objects:
        ob.select_set(ob in parts)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.convert(target="MESH")
    bpy.ops.object.join()
    car = bpy.context.active_object
    car.name = "car"
    for ob in list(bpy.data.objects):
        if ob.name.startswith("arch_cut_"):
            bpy.data.objects.remove(ob, do_unlink=True)
    return bpy, [car]


def render(bpy, path):
    sc = bpy.context.scene
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    sc.collection.objects.link(cam)
    cam.location = (-4.6, -4.4, 1.9)
    cam.rotation_euler = (math.radians(78), 0, math.radians(-46))
    cam.data.lens = 50
    sc.camera = cam
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sc.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(40), 0, math.radians(20))
    sun.data.energy = 2.5
    w = bpy.data.worlds.new("w")
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.7, 0.72, 0.75, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.9
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
    g = bpy.context.active_object
    g.data.materials.append(material(bpy, "ground", (0.12, 0.12, 0.12), 0.6))
    r = sc.render
    r.engine = "BLENDER_EEVEE_NEXT"
    r.resolution_x, r.resolution_y = 900, 560
    r.filepath = os.path.abspath(path)
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)
    bpy.data.objects.remove(sun)
    bpy.data.objects.remove(g)


def main():
    o = args()
    bpy, parts = build(o["paint"])
    if o["render"]:
        render(bpy, o["render"])
    if o["out"]:
        os.makedirs(os.path.dirname(os.path.abspath(o["out"])), exist_ok=True)
        for ob in bpy.data.objects:
            ob.select_set(ob in parts)
        bpy.ops.export_scene.gltf(filepath=os.path.abspath(o["out"]), export_format="GLB",
                                  use_selection=True, export_apply=True, export_yup=True)
    faces = 0
    dg = bpy.context.evaluated_depsgraph_get()
    for p in parts:
        faces += len(p.evaluated_get(dg).data.polygons)
    print("carModel parts=%d faces=%d out=%s" % (len(parts), faces, o["out"] or "none"))
    return 0


if __name__ == "__main__":
    try:
        rc = main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("car-model raised: %s" % str(e).splitlines()[0][:200]); rc = 3
    sys.exit(rc)
