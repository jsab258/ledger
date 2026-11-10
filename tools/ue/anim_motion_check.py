"""Does an exported animation move? Samples a few bones' positions and rotations across its frames.

Run as a commandlet: -run=pythonscript -script=<full path> with ANIM_PATH (asset path) and ANIM_OUT (JSON file).
Writes per bone the range of translation (cm) and rotation (degrees) over the clip; all near zero means a still pose.
"""
import json
import os

import unreal

PATH = os.environ.get("ANIM_PATH", "")
OUT = os.environ.get("ANIM_OUT", "")
res = {"anim": PATH}
anim = unreal.load_asset(PATH)
if anim is None:
    res["error"] = "not found"
else:
    skel = anim.get_editor_property("skeleton")
    n = unreal.AnimationLibrary.get_num_frames(anim)
    names = [str(b) for b in unreal.AnimationLibrary.get_animation_track_names(anim)]
    res.update({"frames": n, "length_s": anim.get_editor_property("sequence_length"),
                "skeleton": skel.get_path_name() if skel else None, "tracks": len(names)})
    want = [b for b in names if any(k in b.lower() for k in ("pelvis", "spine_03", "thigh_l", "calf_r", "upperarm_l", "head", "foot_l"))][:8]
    if not want:
        want = names[:8]
    bones = {}
    for b in want:
        locs, rots = [], []
        for f in range(0, max(n, 1), max(1, n // 20)):
            t = unreal.AnimationLibrary.get_bone_pose_for_frame(anim, b, f, False)
            locs.append([t.translation.x, t.translation.y, t.translation.z])
            r = t.rotation.rotator()
            rots.append([r.roll, r.pitch, r.yaw])
        rng = lambda a, i: round(max(v[i] for v in a) - min(v[i] for v in a), 2)
        bones[b] = {"move_cm": [rng(locs, i) for i in range(3)], "turn_deg": [rng(rots, i) for i in range(3)]}
    res["bones"] = bones
if OUT:
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
unreal.log("ANIMCHECK " + json.dumps(res)[:2000])
