"""How far a sitting clip bows the body: the trunk's lean, the upper back and the neck, frame by frame.

    blender -b --python tools/meshgen/blender/clip_bow.py -- CLIP.fbx OUT.json [--standing first|last]

WHY, 30 October 2026 (his order D10, sitting; production/research/sit-and-turn/SIT-BOW-2026-10-30.md): Tom bows almost
flat when he sits from straight on, and the clips are to be judged against a person's lean before one is chosen.
Per frame, from the clip's own skeleton (bones found by their name's ending: hips, spine2, neck, head):
  * lean: the hips-to-neck line against the vertical, degrees;
  * upper back: the bend between the lower trunk (hips to spine2) and the upper (spine2 to neck), minus its value
    standing (positive = rounded forward); the study the target comes from has the thoracic spine extending, not
    rounding, as the trunk leans;
  * neck: the angle between the spine2-to-neck and neck-to-head segments, minus its value standing;
  * the head's height above the hips.
Standing is the clip's first frame (a sit-down) or last (a stand-up: --standing last). Seat contact is the first
frame whose hips lie within 3 cm of their seated height (the clip's lowest). Writes the peaks, the frame of each,
the values at seat contact and every frame's row.
"""
import json
import math
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
CLIP, OUT = argv[0], argv[1]
STANDING = argv[argv.index("--standing") + 1] if "--standing" in argv else "first"


def angle_to_vertical(v):
    return math.degrees(math.acos(max(-1.0, min(1.0, v.normalized().z))))


def between(a, b):
    return math.degrees(math.acos(max(-1.0, min(1.0, a.normalized().dot(b.normalized())))))


bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=CLIP)
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
act = arm.animation_data.action if arm.animation_data else None
f0, f1 = (int(act.frame_range[0]), int(act.frame_range[1])) if act else (1, 1)
names = [b.name for b in arm.pose.bones]


def find(key):
    return next(n for n in names if n.lower().endswith(key))


HIPS, SPINE2, NECK, HEAD = find("hips"), find("spine2"), find("neck"), find("head")
rows = []
for f in range(f0, f1 + 1):
    bpy.context.scene.frame_set(f)
    mw = arm.matrix_world
    h, s2, n, hd = (mw @ arm.pose.bones[b].head for b in (HIPS, SPINE2, NECK, HEAD))
    rows.append({"frame": f, "hipsM": round(h.z, 3), "leanDeg": round(angle_to_vertical(n - h), 1),
                 "upperBackDeg": between(s2 - h, n - s2), "neckDeg": between(n - s2, hd - n), "headAboveHipsM": round(hd.z - h.z, 3)})
stand = rows[0] if STANDING == "first" else rows[-1]
for r in rows:
    r["upperBackDeg"] = round(r["upperBackDeg"] - stand["upperBackDeg"], 1)
    r["neckDeg"] = round(r["neckDeg"] - stand["neckDeg"], 1)
seated = min(r["hipsM"] for r in rows)
order = rows if STANDING == "first" else list(reversed(rows))
contact = next(r for r in order if r["hipsM"] <= seated + 0.03)
peak = {k: max(rows, key=lambda r: r[k]) for k in ("leanDeg", "upperBackDeg", "neckDeg")}
out = {"clip": CLIP, "frames": [f0, f1], "standing": STANDING, "seatedHipsM": seated,
       "peaks": {k: {"value": v[k], "frame": v["frame"]} for k, v in peak.items()},
       "atSeatContact": contact, "rows": rows}
json.dump(out, open(OUT, "w"), indent=1)
print("CLIPBOW %s: lean peak %.0f deg (frame %d), upper back %+.0f (frame %d), neck %+.0f (frame %d); at seat contact (frame %d) lean %.0f, head %.2f m above the hips"
      % (CLIP.replace("\\", "/").split("/")[-1], peak["leanDeg"]["leanDeg"], peak["leanDeg"]["frame"], peak["upperBackDeg"]["upperBackDeg"],
         peak["upperBackDeg"]["frame"], peak["neckDeg"]["neckDeg"], peak["neckDeg"]["frame"], contact["frame"], contact["leanDeg"], contact["headAboveHipsM"]))
