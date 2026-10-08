"""Build closed solids in Blender from a parts list, export them for the checker.

Run inside Blender (headless):
    blender -b --factory-startup --python blender_parts.py -- parts.json out.npz [out.blend]

parts.json: {"parts": [{"name": str, "material": str,
                        "profile": [[a, b], ...]   # metres, closed polygon, no repeat
                        "axis": "x"|"y"|"z",       # extrusion direction
                        "plane": ["y", "z"],       # world axes of profile's a and b
                        "start": float, "end": float}, ...]}
Each part is a prism: the profile extruded along `axis` from start to end, capped.
Parts may also be given as "mesh": {"V": [[x,y,z]...], "F": [[i,j,k]...]} for shapes
that are not prisms (horns with a curved end, arch heads).
Every part is written to out.npz as <name>_V and <name>_F in world metres.
"""
import json
import sys

import bpy
import bmesh
import numpy as np

AX = {"x": 0, "y": 1, "z": 2}


def prism(profile, axis, plane, start, end):
    P = np.asarray(profile, float)
    n = len(P)
    ia, ib, ic = AX[plane[0]], AX[plane[1]], AX[axis]
    V = np.zeros((2 * n, 3))
    for k, z in enumerate((start, end)):
        V[k * n:(k + 1) * n, ia] = P[:, 0]
        V[k * n:(k + 1) * n, ib] = P[:, 1]
        V[k * n:(k + 1) * n, ic] = z
    return V


def make_object(name, V, faces, material=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in V], [], faces)
    me.validate()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    if material:
        mat = bpy.data.materials.get(material) or bpy.data.materials.new(material)
        me.materials.append(mat)
    return ob


def build(spec):
    obs = []
    for p in spec["parts"]:
        if "mesh" in p:
            V = np.asarray(p["mesh"]["V"], float)
            faces = [tuple(f) for f in p["mesh"]["F"]]
        else:
            V = prism(p["profile"], p["axis"], p["plane"], p["start"], p["end"])
            n = len(p["profile"])
            faces = [tuple(range(n))[::-1], tuple(range(n, 2 * n))]
            faces += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        obs.append(make_object(p["name"], V, faces, p.get("material")))
    return obs


def export(obs, path):
    dg = bpy.context.evaluated_depsgraph_get()
    out = {}
    for o in obs:
        e = o.evaluated_get(dg)
        m = e.to_mesh()
        m.calc_loop_triangles()
        out[o.name + "_V"] = np.array([(o.matrix_world @ v.co)[:] for v in m.vertices])
        out[o.name + "_F"] = np.array([t.vertices[:] for t in m.loop_triangles], dtype=np.int64)
        e.to_mesh_clear()
    np.savez_compressed(path, **out)


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:]
    spec = json.load(open(argv[0]))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    obs = build(spec)
    export(obs, argv[1])
    if len(argv) > 2 and argv[2].lower().endswith(".glb"):
        # THE GAME'S PIECE (8 October): the same solids as the checked model, each node named
        # <material>__<part> as the shopfront kit's are; the lab's "paint" is the street's
        # painted joinery. Read by tools/art-recipes/terrace-front.py (_kit_sash_window).
        for o in obs:
            mat = o.data.materials[0].name if len(o.data.materials) else "none"
            if mat == "paint":
                o.data.materials[0].name = mat = "paint_joinery"
            o.name = "%s__%s" % (mat, o.name)
        bpy.ops.export_scene.gltf(filepath=argv[2], export_format="GLB", export_yup=True,
                                  export_normals=True, export_texcoords=False, export_cameras=False,
                                  export_animations=False, export_extras=False)
    elif len(argv) > 2:
        bpy.ops.wm.save_as_mainfile(filepath=argv[2])
    print("BUILT", len(obs), "parts ->", argv[1])
