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


if __name__ == "__main__":
    for fix in (True, False):
        ok, rows, tris = gls06(fix)
        print("backface_fix", fix, "GLS-06", ok, "triangles", tris)
        for r in rows:
            print("   %2d deg: card reads %.3f of its own (need %.3f; F_front %.3f)" % r)
        print("   MAT-04:", mat04(fix))
