# A SITTING CLIP FRAME BY FRAME, for joining two clips (30 October 2026, his order D10, the sit from straight on;
# production/research/sit-and-turn/SIT-BOW-2026-10-30.md, route (i)). Epic's front entry walks in and turns 180 degrees
# well, then folds Tom almost flat as it lowers him; Mixamo's back-down lowers a person standing with his back to the
# seat. To hand over from one to the other, the moment is wanted when the turn is done and the hips have not yet begun
# to drop. Per 1/30 s, in the clip's own frame with root motion left in the root: the root's place and yaw, the
# pelvis's and the head's height above the floor, the neck_01-to-head line's lean from the vertical (degrees; 90 is the
# head at the neck's height), and the trunk's lean (the thighs' midpoint to neck_01 from the vertical).
# Run: UnrealEditor-Cmd.exe ue-probe/LedgerProbe.uproject -run=pythonscript -script=<full path of this file>
#      -EnablePlugins=PythonScriptPlugin   (the full path, or it fails quietly; never while the build machine builds)
# Clips: LEDGER_CLIP_FRAMES (comma-separated object paths), else Epic's front entries and stand-up and the cast's
# back-down and stand-up (on the MetaHuman skeleton those carry the hips in spine_01 and the thighs, the pelvis left at
# the root, as the batch retarget writes them: their "pelvis" figures read nil; the trunk is taken from the thighs).
import json
import math
import os
import unreal

OUT = os.environ.get("LEDGER_CLIP_FRAMES_OUT", "F:/LedgerTools/scratch/sit/clip_frames.json")
BENCH = "/Game/Characters/UEFN_Mannequin/Animations/Interactions/Bench/"
DEFAULT = [BENCH + n + "." + n for n in ("M_interaction_bench_into_F_Lfoot", "M_interaction_bench_into_F_Rfoot",
                                         "M_interaction_bench_out_to_stand")] + \
          ["/Game/Ledger/Anim/Sit/%s.%s" % (n, n) for n in ("A_sit_down_MH", "A_stand_up_MH")]


def lean(a, b):
    dx, dy, dz = (b[k] - a[k] for k in range(3))
    return math.degrees(math.atan2(math.hypot(dx, dy), max(dz, 1e-6)))


def frames(path):
    seq = unreal.load_asset(path)
    if not isinstance(seq, unreal.AnimSequence):
        return {"clip": path, "error": "no sequence"}
    opts = unreal.AnimPoseEvaluationOptions()
    for k, v in (("should_retarget", False), ("extract_root_motion", False)):
        try:
            opts.set_editor_property(k, v)
        except Exception:
            pass
    length = seq.get_play_length()
    rows = []
    for i in range(int(length * 30) + 1):
        t = min(length, i / 30.0)
        pose = unreal.AnimPoseExtensions.get_anim_pose_at_time(seq, t, opts)
        p = {}
        for b in ("root", "pelvis", "thigh_l", "thigh_r", "neck_01", "head", "ball_l", "ball_r"):
            try:
                tr = unreal.AnimPoseExtensions.get_bone_pose(pose, b, unreal.AnimPoseSpaces.WORLD)
                p[b] = (tr.translation.x, tr.translation.y, tr.translation.z, tr.rotation.rotator().yaw)
            except Exception:
                pass
        if not all(b in p for b in ("root", "pelvis", "thigh_l", "thigh_r", "neck_01", "head")):
            return {"clip": path, "error": "bones missing at %.2f s: %s" % (t, sorted(p))}
        hips = tuple((p["thigh_l"][k] + p["thigh_r"][k]) / 2.0 for k in range(3))   # the hips by the thighs' midpoint
        rows.append({"t": round(t, 3), "root": [round(p["root"][k], 1) for k in range(2)], "yaw": round(p["root"][3], 1),
                     "pelvis": [round(p["pelvis"][k], 1) for k in range(2)], "pelvis_z": round(p["pelvis"][2], 1), "head_z": round(p["head"][2], 1),
                     "neck_lean": round(lean(p["neck_01"], p["head"]), 1), "trunk_lean": round(lean(hips, p["neck_01"]), 1)})
    return {"clip": path, "length": round(length, 3), "root_motion": bool(seq.get_editor_property("enable_root_motion")), "rows": rows}


clips = [c for c in os.environ.get("LEDGER_CLIP_FRAMES", "").split(",") if c] or DEFAULT
res = {"made": "tools/ue/clip_frames.py", "clips": [frames(c) for c in clips]}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
unreal.log("clip_frames: %d clips, %d with errors, to %s" % (len(res["clips"]), sum(1 for c in res["clips"] if "error" in c), OUT))
