"""The front doors for every house kind, built by one command (cloud week 42, unit 9).

    cd production/cloud-week/kit/front-doors-all
    nice -n 15 /home/user/.bpyenv/bin/python build_doors.py [--stages kinds,furniture,street] [--kinds T1,F2] [--out-dir DIR] [--npz-dir DIR]

(`python3 build_doors.py` runs the same file when python3 is that interpreter; the Python of the cloud session is /home/user/.bpyenv/bin/python with bpy 5.2.2.)
About 20 seconds on four cores. It writes, under production/assets/cloud-week/front-doors-all/ (each .glb under 1 MB: metres, z up, scale 1, the pivot at the
base's centre on the ground, the wall face at y = 0, the street toward -y):
  door_<K>.glb           the ten kinds in their frames (T1 T2 T3 F1 to F7), in the paint and condition of the kind's first street house; no fitting in them
  furniture/<ID>.glb     the 28 furniture variants (and NM1_stacked), each its own part, the origin at its mounting point on the leaf's face
  houses.json            the 12 household doors and the hill's 12: kind, paint, frame, condition, each fitting and its mount point in the kind's own frame
  paints.json, conditions.json   the 15 paints and 2 frame colours (sRGB and linear), the three conditions as a wear parameter set
  manifest.json          every file's bytes, triangles, parts, materials and sha256
and, beside the script, build/*.npz (the named parts, for check_doors.py; git-ignored). A kind in another paint, frame colour or condition (the check builds
neglected and kept copies of one kind to prove the notch) is `--kinds F1 --paint navy --condition neglected --name door_F1_test --out-dir SCRATCH`.
Made from the 3.1 door's script (kit/door/build_door.py: class Door, whose frame, transom, glazing bead, sill and step are kept as built) and the numbers of
production/cloud-week/targets/front-doors-all/target.json. NOTES.md says part by part what is kept, what changes and why.
"""
import argparse
import hashlib
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doors_kinds as K  # noqa: E402
from doors_kinds import bd  # noqa: E402
import doors_furniture as DF  # noqa: E402
import doors_street as DS  # noqa: E402

import bpy  # noqa: E402

ASSET_DIR = os.path.join(bd.REPO, "production", "assets", "cloud-week", "front-doors-all")
NPZ_DIR = os.path.join(HERE, "build")

NIGHT = {"lantern_colour_linear": [1.0, 0.25, 0.0],
         "note": "the game's lantern colour (linear red 1.0, green 0.25, blue 0.0); the cloud renders are overcast day only, so no light of this colour is made here"}


def build_kind(T31, N, kind, out_dir, npz_dir, paint=None, frame_colour=None, condition=None, name=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    d = K.KindDoor(T31, N, kind, paint, frame_colour, condition).build()
    obs = d.finish()
    name = name or "door_%s" % kind
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(npz_dir, exist_ok=True)
    glb = os.path.join(out_dir, name + ".glb")
    npz = os.path.join(npz_dir, name + ".npz")
    bd.blender_parts.export(obs, npz)
    bd.export_glb(glb)
    info = {"kind": kind, "paint": d.paint, "frame_colour": d.frame_colour, "condition": d.condition, "glb": glb, "npz": npz, "glb_bytes": os.path.getsize(glb),
            "triangles": bd.tri_count(obs), "parts": {o.name: len(o.data.polygons) for o in obs}, "pivot_mm": d.pivot, "notes": d.notes,
            "materials": sorted({o.data.materials[0].name for o in obs})}
    json.dump({o.name: {"material": o.data.materials[0].name} for o in obs}, open(os.path.join(npz_dir, name + ".parts.json"), "w"), indent=1)
    return info


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stages", default="kinds,furniture,street")
    ap.add_argument("--kinds", default=",".join(K.KINDS))
    ap.add_argument("--out-dir", default=ASSET_DIR)
    ap.add_argument("--npz-dir", default=NPZ_DIR)
    ap.add_argument("--paint")
    ap.add_argument("--condition")
    ap.add_argument("--frame-colour")
    ap.add_argument("--name")
    a = ap.parse_args()
    stages = a.stages.split(",")
    T31 = bd.load_target()
    N = K.load_new_target()
    manifest = {"made_by": "production/cloud-week/kit/front-doors-all/build_doors.py", "target": "production/cloud-week/targets/front-doors-all/target.json", "kinds": {}, "furniture": {}}
    t_all = time.time()
    if "kinds" in stages:
        for k in a.kinds.split(","):
            t0 = time.time()
            info = build_kind(T31, N, k, a.out_dir, a.npz_dir, a.paint, a.frame_colour, a.condition, a.name)
            info["sha256"] = sha(info["glb"])
            manifest["kinds"][k] = {x: info[x] for x in ("paint", "frame_colour", "condition", "glb_bytes", "triangles", "materials", "sha256", "notes")}
            manifest["kinds"][k]["file"] = os.path.basename(info["glb"])
            manifest["kinds"][k]["parts"] = sorted(info["parts"])
            print("%s: %d triangles, %d bytes, %.1f s" % (k, info["triangles"], info["glb_bytes"], time.time() - t0), flush=True)
    if "kinds" in stages and not a.name and not a.condition:
        for k in a.kinds.split(","):
            if K.first_house(N, k)["condition"] == "neglected":          # the kept copy of a kind whose street house is neglected (the hill's doors; the check's proof that the notch is the condition)
                info = build_kind(T31, N, k, a.out_dir, a.npz_dir, a.paint, a.frame_colour, "kept", "door_%s_kept" % k)
                info["sha256"] = sha(info["glb"])
                manifest["kinds"][k + "_kept"] = {x: info[x] for x in ("paint", "frame_colour", "condition", "glb_bytes", "triangles", "materials", "sha256")}
                manifest["kinds"][k + "_kept"]["file"] = os.path.basename(info["glb"])
                print("%s kept: %d triangles, %d bytes" % (k, info["triangles"], info["glb_bytes"]), flush=True)
    if "furniture" in stages:
        for vid in DF.variant_builders(N):
            t0 = time.time()
            info = DF.build_variant(N, vid, os.path.join(a.out_dir, "furniture"), a.npz_dir)
            info["sha256"] = sha(info["glb"])
            manifest["furniture"][vid] = {x: info[x] for x in ("glb_bytes", "triangles", "parts", "materials", "sha256")}
            print("furniture %s: %d triangles, %d bytes, %.1f s" % (vid, info["triangles"], info["glb_bytes"], time.time() - t0), flush=True)
    if "street" in stages:
        H = DS.houses_data(N)
        H["night"] = NIGHT
        H["numbers"] = {"note": "The forms are the target's (NM1 NM3 NM6); the digits are placeholders the town assigns (none is canon, none is a real address).",
                        "digits": {k: v for k, v in DF.NUMBERS.items()}}
        H["night_light"] = NIGHT
        H["notes"] = ("mount_m is the fitting's origin (its mounting point on the leaf's face; the bell push on the jamb's stop face; the scraper on the ground against the wall) in "
                      "metres in the kind's own .glb frame; mirror_x: scale x by -1 (a lever built pointing toward a left-locking door's middle). The hill's doors take kind and paint only.")
        os.makedirs(a.out_dir, exist_ok=True)
        json.dump(H, open(os.path.join(a.out_dir, "houses.json"), "w"), indent=1)
        slots = [{"house": h["house"], "side": h["side"], "x_centre_m": h["x_centre_m"], "frame_set": h["frame_set"], "modernised": h["windows_modernised"]} for h in N["street"]["houses"]]
        mixed = DS.mix_new_street(N, slots, seed=1)
        json.dump({"note": "A sample of the mixer (doors_street.mix_new_street, seed 1) on the twelve slots, ignoring the target's own table: kind, paint, condition and fittings mixed so that no two neighbours match "
                           "(the check re-runs every street rule on it). The authority for today's houses is houses.json, which is the target's table.", "houses": mixed},
                  open(os.path.join(a.out_dir, "houses_mixed_sample.json"), "w"), indent=1)
        json.dump(DS.paints_json(N), open(os.path.join(a.out_dir, "paints.json"), "w"), indent=1)
        json.dump(DS.conditions_json(N), open(os.path.join(a.out_dir, "conditions.json"), "w"), indent=1)
        print("street data: %d houses, %d hill doors" % (len(H["houses"]), len(H["hill"])), flush=True)
    if a.stages == "kinds,furniture,street" and a.kinds == ",".join(K.KINDS) and not a.name:
        json.dump(manifest, open(os.path.join(a.out_dir, "manifest.json"), "w"), indent=1)
    print("done in %.1f s" % (time.time() - t_all))


if __name__ == "__main__":
    main()
