"""The CMU retarget's target tracks read inside Unreal: try 2 of 2 on the measured check's reader fault (17 Nov).
Blender read Unreal's FBX export with the armature at scale 0.01 and pose locations about 100 times too large; this
reads the retargeted sequences themselves, so no exporter or importer sits between the clip and the numbers.

    UnrealEditor-Cmd.exe <ue-probe>/LedgerProbe.uproject -run=pythonscript -script=<FULL path to this file>
        -EnablePlugins=PythonScriptPlugin -unattended -nop4 -nosplash
    env: CMU_UE_RESULT (default F:/LedgerTools/game-inputs/cmu-2026-11-17/ue/ue_result.json)

For every exported clip in ue_result.json's outputs: one JSON beside its FBX (<fbx stem>.track.json) in the shape
tools/meshgen/blender/cmu_measure.py's read_track() takes: per frame, component-space (Unreal "world" of the pose)
positions in cm of the measured roles, the reference pose of the same roles, and limb bones' local rotations
(w, x, y, z). Evaluated as tools/ue/clip_frames.py does (should_retarget and extract_root_motion off), every 1/fps from
0 to the play length. Prints one line "cmuBoneDump=DONE|FAIL ..." and writes ue_bone_dump.json beside ue_result.json.

Rest (measure fix M1, 17 Nov): the body's own reference pose from ue_result.json's body_ref (cmu_ue_retarget.py reads
it from the body mesh). The skeleton asset's reference is metahuman_base_skel, another body: scaled by leg length it
put Rocco's ankle 1.95 cm low and his standing pelvis 2.6 cm high (diagnosis 17 Nov). Without body_ref the skeleton's
reference is used and rest_from says so.
"""
import json
import os
import re
import traceback

import unreal

RES = os.environ.get("CMU_UE_RESULT", "F:/LedgerTools/game-inputs/cmu-2026-11-17/ue/ue_result.json")
ROLES = ("pelvis", "thigh_l", "calf_l", "foot_l", "ball_l", "thigh_r", "calf_r", "foot_r", "ball_r")
MH_LIMB = re.compile(r"^(clavicle|upperarm|lowerarm|hand|thigh|calf|foot|ball)_(l|r)$")
W = unreal.AnimPoseSpaces.WORLD
L = unreal.AnimPoseSpaces.LOCAL


def opts():
    o = unreal.AnimPoseEvaluationOptions()
    for k, v in (("should_retarget", False), ("extract_root_motion", False)):
        try:
            o.set_editor_property(k, v)
        except Exception:
            pass
    return o


def v3(t):
    return (round(t.translation.x, 4), round(t.translation.y, 4), round(t.translation.z, 4))


def frame_rate(seq):
    for fn in ("get_frame_rate",):
        try:
            fr = getattr(unreal.AnimationLibrary, fn)(seq)
            return float(fr.numerator) / float(fr.denominator) if hasattr(fr, "numerator") else float(fr)
        except Exception:
            pass
    return 30.0


def dump(asset, out, body_rest=None, body=None):
    seq = unreal.load_asset(asset)
    if not isinstance(seq, unreal.AnimSequence):
        raise RuntimeError("no AnimSequence at " + asset)
    o = opts()
    fps = frame_rate(seq)
    length = seq.get_play_length()
    n = int(round(length * fps)) + 1
    p0 = unreal.AnimPoseExtensions.get_anim_pose_at_time(seq, 0.0, o)
    names = [str(b) for b in unreal.AnimPoseExtensions.get_bone_names(p0)]
    missing = [r for r in ROLES if r not in names]
    if missing:
        raise RuntimeError("bones missing: %s" % missing)
    limbs = [b for b in names if MH_LIMB.match(b)]
    if body_rest and all(r in body_rest for r in ROLES):
        rest = {r: tuple(body_rest[r]) for r in ROLES}
        rest_from = "body reference pose of %s (ue_result body_ref)" % body
    else:
        rest = {r: v3(unreal.AnimPoseExtensions.get_ref_bone_pose(p0, r, W)) for r in ROLES}
        rest_from = asset + " (skeleton reference pose: no body_ref)"
    pos = {r: [] for r in ROLES}
    rot = {b: [] for b in limbs}
    for i in range(n):
        t = min(length, i / fps)
        p = unreal.AnimPoseExtensions.get_anim_pose_at_time(seq, t, o)
        for r in ROLES:
            pos[r].append(v3(unreal.AnimPoseExtensions.get_bone_pose(p, r, W)))
        for b in limbs:
            q = unreal.AnimPoseExtensions.get_bone_pose(p, b, L).rotation
            rot[b].append((round(q.w, 6), round(q.x, 6), round(q.y, 6), round(q.z, 6)))
    tr = dict(path=out, asset=asset, kind="MH", fps=fps, frame_range=[0, n - 1], pos=pos, rest=rest, rot=rot,
              rest_from=rest_from, made="tools/ue/cmu_bone_dump.py")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(tr, fh)
    return dict(asset=asset, track=out, frames=n, fps=fps, length_s=round(length, 4), rest_from=rest_from,
                rest_pelvis_cm=rest["pelvis"], first_pelvis_cm=pos["pelvis"][0], limbs=len(limbs))


res = json.load(open(RES, encoding="utf-8"))
done, errs = [], []
for o_ in res.get("outputs", []):
    for clip, c in o_.get("clips", {}).items():
        if not (c.get("exported") and c.get("fbx") and c.get("asset")):
            continue
        out = os.path.splitext(c["fbx"].replace("\\", "/"))[0] + ".track.json"
        try:
            done.append(dump(c["asset"], out, res.get("body_ref", {}).get(o_.get("body")), o_.get("body")))
        except Exception as e:
            errs.append(dict(asset=c.get("asset"), error=str(e)[:300], trace=traceback.format_exc()[-800:]))
summary = dict(made="tools/ue/cmu_bone_dump.py", result=RES, done=done, errors=errs,
               status="DONE" if done and not errs else "FAIL")
with open(os.path.join(os.path.dirname(RES), "ue_bone_dump.json"), "w", encoding="utf-8") as fh:
    json.dump(summary, fh, indent=1)
unreal.log("cmuBoneDump=%s tracks=%d errors=%d" % (summary["status"], len(done), len(errs)))
