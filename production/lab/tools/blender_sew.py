"""Sew flat pattern pieces round a body with Blender's cloth, headless, CPU only.

    blender -b --factory-startup --python blender_sew.py -- garment.npz body.npz out.npz out.blend [settings.json]

garment.npz (made by the pattern code):
    V (n,3) metres, every piece already placed round the body;
    F (m,3) triangles;
    seams (k,2) vertex pairs to be sewn (loose edges, pulled shut by sewing springs);
    pin (n,) 0..1 pinning weight (Blender's mass group: 1 = held where it starts);
    bend (n,) 0..1 bending-stiffness weight (fused canvas, the lapel's roll);
body.npz: <name>_V/<name>_F, the body collider in the same space.

The rest shape for bending is the starting mesh, so a lapel folded back before the
run keeps that fold as its rest angle, as a pressed and canvassed lapel does.
Writes the last frame's garment (world metres) to out.npz as garment_V/garment_F,
plus garment_V_<frame> every `keep_every` frames, and the scene to out.blend.
"""
import json
import sys

import bpy
import numpy as np

DEFAULTS = {
    "frames": 120, "sew_frames": 60, "fps": 24,
    "quality": 8, "mass_kg_m2": 0.32,            # wool suiting about 300-350 g/m2
    "tension": 40.0, "compression": 40.0, "shear": 20.0,
    "bending": 0.6, "bending_max": 40.0,         # bend weight 1 gets bending_max
    "air": 1.0, "sewing_force_max": 8.0,
    "collision_distance": 0.004, "self_collision": True, "self_distance": 0.003,
    "body_thickness_outer": 0.004, "body_friction": 5.0,
    "gravity_during_sew": 0.0, "keep_every": 20,
}


def load(path):
    d = np.load(path, allow_pickle=False)
    return {k: d[k] for k in d.files}


def mesh_object(name, V, F, edges=()):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in V], list(map(tuple, edges)), [tuple(f) for f in F])
    me.validate()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def vgroup(ob, name, w):
    g = ob.vertex_groups.new(name=name)
    for i, x in enumerate(w):
        if x > 0:
            g.add([i], float(x), "REPLACE")
    return g


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    g, b = load(argv[0]), load(argv[1])
    out_npz, out_blend = argv[2], argv[3]
    S = dict(DEFAULTS)
    if len(argv) > 4:
        S.update(json.load(open(argv[4])))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.fps = S["fps"]
    sc.frame_start, sc.frame_end = 1, S["frames"]

    names = sorted({k[:-2] for k in b if k.endswith("_V")})
    for n in names:
        body = mesh_object("body_" + n, b[n + "_V"], b[n + "_F"])
        if n + "_Vkey" in b and S.get("body_morph"):
            # the body moves during the run (MetaHuman's A-pose to arms down): a shape key, keyed
            body.shape_key_add(name="Basis")
            key = body.shape_key_add(name="down")
            Vk = b[n + "_Vkey"]
            for i, v in enumerate(key.data):
                v.co = Vk[i]
            f0, f1 = S["body_morph"]
            key.value = 0.0
            key.keyframe_insert("value", frame=f0)
            key.value = 1.0
            key.keyframe_insert("value", frame=f1)
        body.modifiers.new("Collision", "COLLISION")
        body.collision.thickness_outer = S["body_thickness_outer"]
        body.collision.cloth_friction = S["body_friction"]

    gar = mesh_object("garment", g["V"], g["F"], edges=g["seams"])
    if "pin" in g:
        vgroup(gar, "pin", g["pin"])
    if "bend" in g:
        vgroup(gar, "bend", g["bend"])
    cl = gar.modifiers.new("Cloth", "CLOTH")
    cs = cl.settings
    cs.quality = S["quality"]
    cs.mass = S["mass_kg_m2"] * 0.0  # set below from area
    area = 0.0
    V, F = g["V"], g["F"]
    area = 0.5 * np.linalg.norm(np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]), axis=1).sum()
    cs.mass = max(1e-4, S["mass_kg_m2"] * area / len(V))   # Blender's mass is per vertex
    cs.tension_stiffness = S["tension"]
    cs.compression_stiffness = S["compression"]
    cs.shear_stiffness = S["shear"]
    cs.bending_stiffness = S["bending"]
    cs.air_damping = S["air"]
    cs.use_sewing_springs = True
    cs.sewing_force_max = S["sewing_force_max"]
    if "bend" in g:
        cs.vertex_group_bending = "bend"
        cs.bending_stiffness_max = S["bending_max"]
    if "pin" in g:
        cs.vertex_group_mass = "pin"
    cc = cl.collision_settings
    cc.distance_min = S["collision_distance"]
    cc.use_self_collision = S["self_collision"]
    cc.self_distance_min = S["self_distance"]
    cc.collision_quality = 4
    cl.point_cache.frame_start, cl.point_cache.frame_end = 1, S["frames"]

    # gravity off while sewing, on afterwards (keyframed on the scene's gravity)
    sc.use_gravity = True
    sc.gravity = (0, 0, -9.81 * S["gravity_during_sew"])
    sc.keyframe_insert("gravity", frame=1)
    sc.keyframe_insert("gravity", frame=S["sew_frames"])
    sc.gravity = (0, 0, -9.81)
    sc.keyframe_insert("gravity", frame=S["sew_frames"] + 10)
    cl.settings.use_dynamic_mesh = False

    keep = {}
    for f in range(1, S["frames"] + 1):
        sc.frame_set(f)
        if f % S["keep_every"] == 0 or f == S["frames"]:
            dg = bpy.context.evaluated_depsgraph_get()
            e = gar.evaluated_get(dg)
            m = e.to_mesh()
            keep["garment_V_%03d" % f] = np.array([(gar.matrix_world @ v.co)[:] for v in m.vertices])
            e.to_mesh_clear()
            print("FRAME", f, flush=True)
    last = keep["garment_V_%03d" % S["frames"]]
    np.savez_compressed(out_npz, garment_V=last, garment_F=F, **keep)
    bpy.ops.wm.save_as_mainfile(filepath=out_blend)
    print("SEWN", out_npz)


if __name__ == "__main__":
    main()
