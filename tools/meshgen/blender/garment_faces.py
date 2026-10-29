"""WHICH WAY A GARMENT'S FACES POINT, MEASURED AGAINST THE BODY INSIDE IT (Blender, background).

    blender -b --factory-startup --python tools/meshgen/blender/garment_faces.py -- GARMENT.fbx BODY.fbx OUT.json

WHY, 29 October 2026 (his order C9; the packaged sit film's fresh review: see-through patches over Tom's jacket and
skin through its right sleeve when the arm bends). A one-sided material draws a face that points into the body as a
hole. The retopology's own measure (retopo_pieces.py facesOutwardShare, 84%) counts a face as inward when it points
toward the garment's vertical centre line, which every sleeve's inner side and the collar's inside do rightly, so it
cannot tell a wrong face from a right one. Here each face is asked directly: a ray from its centre along its normal
that meets the body within 25 cm says it points in; one against its normal that meets the body says it points out;
neither (an edge far from the body) is not judged. Counted per separate piece of the mesh and per material slot, so a
piece wound the wrong way shows by name. No change is made to any file but OUT.json.
"""
import json
import sys

import bpy
import bmesh
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:]
garment_path, body_path, out_path = argv[0], argv[1], argv[2]
REACH = 25.0          # cm, the FBX's own units


def import_fbx(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=path)
    return [o for o in bpy.data.objects if o not in before and o.type == "MESH"]


bpy.ops.wm.read_factory_settings(use_empty=True)
garments = import_fbx(garment_path)
bodies = import_fbx(body_path)
dg = bpy.context.evaluated_depsgraph_get()


def world_bmesh(obj):
    bm = bmesh.new()
    bm.from_object(obj, dg)
    bm.transform(obj.matrix_world)
    bm.normal_update()
    return bm


body_bm = bmesh.new()
for b in bodies:
    tmp = world_bmesh(b)
    m = bpy.data.meshes.new("tmp")
    tmp.to_mesh(m)
    body_bm.from_mesh(m)
    tmp.free()
tree = BVHTree.FromBMesh(body_bm)

out = {"garment": garment_path, "body": body_path, "reachCm": REACH, "objects": []}
for g in garments:
    bm = world_bmesh(g)
    bm.faces.ensure_lookup_table()
    # the separate pieces: faces joined through shared edges
    island = {}
    k = 0
    for f in bm.faces:
        if f.index in island:
            continue
        stack = [f]
        island[f.index] = k
        while stack:
            cur = stack.pop()
            for e in cur.edges:
                for nf in e.link_faces:
                    if nf.index not in island:
                        island[nf.index] = k
                        stack.append(nf)
        k += 1
    slots = [s.material.name if s.material else "slot%d" % i for i, s in enumerate(g.material_slots)]
    per = {}
    for f in bm.faces:
        c = f.calc_center_median()
        n = f.normal
        hit_in = tree.ray_cast(c + n * 0.05, n, REACH)[0] is not None
        hit_out = tree.ray_cast(c - n * 0.05, -n, REACH)[0] is not None
        key = (island[f.index], slots[f.material_index] if f.material_index < len(slots) else "?")
        row = per.setdefault(key, {"faces": 0, "in": 0, "out": 0, "unjudged": 0})
        row["faces"] += 1
        if hit_in and not hit_out:
            row["in"] += 1
        elif hit_out and not hit_in:
            row["out"] += 1
        else:
            row["unjudged"] += 1
    rows = [{"piece": i, "slot": s, **v, "inShare": round(v["in"] / max(1, v["in"] + v["out"]), 3)} for (i, s), v in sorted(per.items())]
    tot_in = sum(r["in"] for r in rows)
    tot_out = sum(r["out"] for r in rows)
    out["objects"].append({"name": g.name, "faces": len(bm.faces), "pieces": k, "in": tot_in, "out": tot_out,
                           "inShare": round(tot_in / max(1, tot_in + tot_out), 3), "rows": rows})
    bm.free()
json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
for o in out["objects"]:
    print("garmentFaces %s faces=%d pieces=%d pointingIn=%d pointingOut=%d inShare=%.3f" % (o["name"], o["faces"], o["pieces"], o["in"], o["out"], o["inShare"]))
    for r in o["rows"]:
        if r["faces"] >= 50:
            print("  piece %d %-8s faces=%d in=%d out=%d unjudged=%d inShare=%.3f" % (r["piece"], r["slot"], r["faces"], r["in"], r["out"], r["unjudged"], r["inShare"]))
