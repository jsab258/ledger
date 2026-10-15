"""GLS-06 and MAT-04 on the kit's OWN slab pane (14 October, from the try 1 reviews, fault 1).

Both reviews found that MAT-04 passed because it rendered "a flat pane" (one plane), while the kit's panes are closed slabs 2.5 mm thick (a front face and a back face): the gate's glass turned the back face into a
total mirror past the critical angle and nothing passed the pane under 56 degrees from the wall. Here the pane is the glb's own `glass__lower_L` node, imported as it is exported (the slab, tilted by its seeded angle),
with the gate's own pane shader (`hw_gate.make_glass_gate`), seen at an angle from the wall in front of an emission card (GLS-06) or against a uniform sky with the room black (MAT-04).
`backface_fix=False` is the negative control: the first build's pane (no `1 - Backfacing`); it must fail both rows.
Run with /home/user/.bpyenv/bin/python (bpy), under `nice -n 15`.
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hw_t as T  # noqa: E402

ANGLES = (15.0, 20.0, 35.0, 50.0, 70.0)           # degrees from the wall (the street review's four, and the close review's 70)
CARD = 0.5                                        # the emission card's linear value
NODE = "glass__lower_L"


def fresnel_unpolarised(theta_i_deg, n=None):
    """The dielectric Fresnel reflectance of ONE surface (air to glass of index n), unpolarised, at the incidence angle (from the normal): what the pane's front face reflects (Cycles' Fresnel node on the front face)."""
    import hw_gate as HG
    n = n or HG.GLASS_IOR
    ci = math.cos(math.radians(theta_i_deg))
    st = math.sin(math.radians(theta_i_deg)) / n
    ct = math.sqrt(max(0.0, 1.0 - st * st))
    rs = (ci - n * ct) / (ci + n * ct)
    rp = (n * ci - ct) / (n * ci + ct)
    return 0.5 * (rs * rs + rp * rp)


def _scene(bpy, world_strength, card_value, backface_fix, angle_from_wall, glb_kind="S22", refl=1.0):
    """The kit's slab pane in a tiny scene: the card behind it (room side), the world a uniform `world_strength` white, the camera at `angle_from_wall` degrees from the pane's plane looking at its centre."""
    import hw_gate as HG
    from mathutils import Vector
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    bpy.ops.import_scene.gltf(filepath=os.path.join(T.ASSETS, "hw_%s.glb" % glb_kind))
    pane = None
    for o in list(bpy.data.objects):
        if o.name.split(".")[0] == NODE:
            pane = o
        else:
            bpy.data.objects.remove(o, do_unlink=True)
    assert pane is not None, "the kit's %s is not in the glb" % NODE
    me = pane.data
    gm = HG.make_glass_gate(bpy, refl, backface_fix=backface_fix)
    me.materials.clear()
    me.materials.append(gm)
    # the slab as exported: its triangles (a front and a back face) are counted for the record
    bpy.context.view_layer.update()
    ws = [pane.matrix_world @ v.co for v in me.vertices]
    lo = Vector((min(w.x for w in ws), min(w.y for w in ws), min(w.z for w in ws)))
    hi = Vector((max(w.x for w in ws), max(w.y for w in ws), max(w.z for w in ws)))
    c = (lo + hi) / 2
    # the card: room side of the pane (the kit's y runs INTO the wall; the street is at y < the pane), 0.6 m behind it, big
    mc = bpy.data.materials.new("card")
    mc.use_nodes = True
    nt = mc.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (card_value, card_value, card_value, 1.0)
    em.inputs["Strength"].default_value = 1.0
    nt.links.new(em.outputs[0], out.inputs[0])
    bpy.ops.mesh.primitive_plane_add(size=60.0, location=(c.x, c.y + 0.6, c.z), rotation=(math.radians(90.0), 0, 0))
    card = bpy.context.object
    card.data.materials.append(mc)
    card.visible_glossy = False
    w = bpy.data.worlds.new("w")
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (1, 1, 1, 1)
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = world_strength
    a = math.radians(angle_from_wall)
    d = 4.0
    eye = Vector((c.x + d * math.cos(a), c.y - d * math.sin(a), c.z))
    cd = bpy.data.cameras.new("c")
    cd.angle = math.radians(2.4)
    co = bpy.data.objects.new("c", cd)
    sc.collection.objects.link(co)
    co.location = eye
    co.rotation_euler = (c - eye).to_track_quat("-Z", "Y").to_euler()
    sc.camera = co
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 24
    sc.cycles.use_denoising = False
    sc.cycles.max_bounces = 8
    sc.cycles.transparent_max_bounces = 24
    sc.render.resolution_x = sc.render.resolution_y = 64
    sc.view_settings.view_transform = "Raw"
    sc.view_settings.look = "None"
    sc.render.image_settings.file_format = "OPEN_EXR"
    sc.render.image_settings.color_depth = "32"
    return sc, len(me.polygons), (hi - lo)


def _read_centre(bpy, path):
    img = bpy.data.images.load(path, check_existing=False)
    a = np.array(img.pixels[:], np.float32).reshape(img.size[1], img.size[0], img.channels)
    bpy.data.images.remove(img)
    return float(a[24:40, 24:40, :3].mean())


def gls06(backface_fix=True, angles=ANGLES, log=None):
    """The kit's slab at each angle from the wall in front of an emission card of 0.5 (the world black): the card through the pane must read at least (1 - F_front(angle)) of its own, less 0.03.
    Returns (ok, [(angle, reads_of_card, need, F_front)], triangles)."""
    import bpy
    res = []
    ok = True
    tris = None
    os.makedirs(T.GATE, exist_ok=True)
    for ang in angles:
        sc, tris, size = _scene(bpy, 0.0, CARD, backface_fix, ang)
        out = os.path.join(T.GATE, "gls06_%s_%d.exr" % ("fix" if backface_fix else "old", int(ang)))
        sc.render.filepath = out
        bpy.ops.render.render(write_still=True)
        v = _read_centre(bpy, out) / CARD
        f = fresnel_unpolarised(90.0 - ang)
        need = (1.0 - f) - 0.03
        ok &= v >= need
        res.append((ang, v, need, f))
        try:
            os.remove(out)
        except OSError:
            pass
    return ok, res, tris


def mat04(backface_fix=True, angle=16.0):
    """MAT-04 on the kit's slab (not a flat single plane), two readings at 16 degrees from the wall:
    (a) against a uniform sky of luma 1.0 with the room black: the pane reads 0.26 +-0.05 of the sky (Cycles' dielectric Fresnel of F0 0.08 may read up to 0.31): its reflectance;
    (b) against the same sky with the room a uniform card of 1.0 behind it: the pane reads 1.0 +-0.05: what the pane reflects and what it passes add up to all of it, no light is lost in the slab.
    (a) alone cannot see the back-face mirror (the first build's pane read 0.277 on (a): the trapped ray adds nothing to a reflection); (b) does (it read 0.28).
    Returns (ok, reflect, energy, triangles)."""
    import bpy
    outs = []
    for card in (0.0, 1.0):
        sc, tris, size = _scene(bpy, 1.0, card, backface_fix, angle)
        out = os.path.join(T.GATE, "mat04_%s_%d.exr" % ("fix" if backface_fix else "old", int(card)))
        sc.render.filepath = out
        bpy.ops.render.render(write_still=True)
        outs.append(_read_centre(bpy, out))
        try:
            os.remove(out)
        except OSError:
            pass
    v, e = outs
    ok = (abs(v - 0.26) <= 0.05 or (0.26 <= v <= 0.31)) and abs(e - 1.0) <= 0.05
    return ok, v, e, tris


def grime_test(condition="grimy", glb_kind="S22"):
    """GRM-01 (14 October, the close review's narrow point 3): the kit's own `paint_joinery__lower_bottom_rail`, painted by the gate's own `make_paint` for a house of this condition, seen square on under a uniform sky: the luma of
    its lowest 30 mm over that of the 30 mm above them. A grimy window reads 0.75 (the band x 0.75), a sound one 1.0. Returns (ratio, rows used)."""
    import bpy
    import hw_gate as HG
    from mathutils import Vector
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    bpy.ops.import_scene.gltf(filepath=os.path.join(T.ASSETS, "hw_%s.glb" % glb_kind))
    rail = None
    for o in list(bpy.data.objects):
        if o.name.split(".")[0] == "paint_joinery__lower_bottom_rail":
            rail = o
        else:
            bpy.data.objects.remove(o, do_unlink=True)
    bpy.context.view_layer.update()
    zs = [(rail.matrix_world @ v.co).z for v in rail.data.vertices]
    zmin = min(zs)
    m0 = rail.data.materials[0]
    paint = T.paints()["white_grimy"]
    gr = ("paint_joinery__lower_bottom_rail", zmin, 0.0) if condition == "grimy" else None
    m = HG.make_paint(m0, paint, condition, True, False, gr)
    rail.data.materials.clear()
    rail.data.materials.append(m)
    w = bpy.data.worlds.new("w")
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (1, 1, 1, 1)
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0
    cd = bpy.data.cameras.new("c")
    cd.type = "ORTHO"
    cd.ortho_scale = 0.9
    co = bpy.data.objects.new("c", cd)
    sc.collection.objects.link(co)
    zc = (zmin + max(zs)) / 2
    co.location = (0.0, -2.0, zc)
    co.rotation_euler = (math.radians(90.0), 0, 0)
    sc.camera = co
    W, H = 450, 200
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 24
    sc.cycles.use_denoising = False
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.view_settings.view_transform = "Raw"
    sc.render.image_settings.file_format = "OPEN_EXR"
    sc.render.image_settings.color_depth = "32"
    out = os.path.join(T.GATE, "grime_%s.exr" % condition)
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
    img = bpy.data.images.load(out, check_existing=False)
    a = np.array(img.pixels[:], np.float32).reshape(img.size[1], img.size[0], img.channels)[..., :3].mean(axis=2)[::-1]
    bpy.data.images.remove(img)
    os.remove(out)
    mm_per_px = 900.0 / W
    def rows(z0_mm, z1_mm):                         # kit z in mm (from the opening's bottom edge) to image rows (row 0 on top)
        z_top = (zc + 0.5 * H * mm_per_px / 1000.0)
        r0 = int(round((z_top - z1_mm / 1000.0) * 1000.0 / mm_per_px))
        r1 = int(round((z_top - z0_mm / 1000.0) * 1000.0 / mm_per_px))
        return slice(r0, r1)
    z0 = zmin * 1000.0
    band = a[rows(z0 + 3, z0 + 28), 150:300]
    above = a[rows(z0 + 33, z0 + 58), 150:300]
    return float(np.median(band) / max(float(np.median(above)), 1e-9)), (float(np.median(band)), float(np.median(above)))


if __name__ == "__main__":
    for fix in (True, False):
        ok, rows, tris = gls06(fix)
        print("backface_fix", fix, "GLS-06", ok, "triangles", tris)
        for r in rows:
            print("   %2d deg: card reads %.3f of its own (need %.3f; F_front %.3f)" % r)
        print("   MAT-04:", mat04(fix))
    print("GRM-01 grimy:", grime_test("grimy"), "sound:", grime_test("sound"))
