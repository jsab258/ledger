# Try 1 of his order of 25 October, item 2: mark a foot planted wherever it is low and nearly still.
# The sample's graph turns each clip's contact curve into a foot speed, (1 - contact) * 100, and its foot lock
# plants a foot only below speed 1, so a foot is held only where its curve is above 0.99. Every slide traced on
# 24 October happened where the clip marked the foot as moving although it stayed flat on the floor. Here each
# walking clip's contact_l and contact_r are set to 1 at every key where the ball is within LOW_CM of its lowest
# height and moving slower than SPEED_CMS in the clip's own frame (root motion kept): the field's contact test
# (Epic's Foot Placement graph mode uses 60 cm/s and 10 cm). Elsewhere the curve is left as it was.
# The originals are copied first to F:/LedgerTools/game-inputs/gasp/originals-2026-10-25 (restore by copying back).
# Run: UnrealEditor-Cmd.exe ue-probe/LedgerProbe.uproject -run=pythonscript -script=<this> -EnablePlugins=PythonScriptPlugin
import unreal, math, json, os, shutil
LOW_CM, SPEED_CMS = 2.5, 60.0
SRC = "F:/LedgerTools/scratch/gasp-export/clip_feet_all.json"
BACKUP = "F:/LedgerTools/game-inputs/gasp/originals-2026-10-25"
CONTENT = "C:/Users/Jafar/ledger-local/ue-probe/Content"
OUT = "F:/LedgerTools/scratch/gasp-export/contact_fix.json"
clips = [c["path"] for c in json.load(open(SRC))["clips"]]
report = []
opts = unreal.AnimPoseEvaluationOptions()
for k, v in (("should_retarget", False), ("extract_root_motion", False)):
    try:
        opts.set_editor_property(k, v)
    except Exception:
        pass


def ball_at(seq, t, f):
    pose = unreal.AnimPoseExtensions.get_anim_pose_at_time(seq, t, opts)
    return unreal.AnimPoseExtensions.get_bone_pose(pose, "ball_" + f, unreal.AnimPoseSpaces.WORLD).translation


for path in clips:
    rel = path.replace("/Game/", "", 1) + ".uasset"
    src = os.path.join(CONTENT, rel)
    dst = os.path.join(BACKUP, rel)
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    seq = unreal.load_asset(path)
    length = seq.get_play_length()
    entry = {"clip": path.split("/")[-1]}
    changed = False
    for f in ("l", "r"):
        name = unreal.Name("contact_" + f)
        try:
            times, vals = unreal.AnimationLibrary.get_float_keys(seq, name)
            times, vals = list(times), list(vals)
        except Exception as e:
            entry["err_" + f] = str(e)[:60]
            continue
        if not times:
            continue
        step = 1.0 / 60.0
        pos = {}
        def p(t):
            t = max(0.0, min(length, round(t * 600) / 600))
            if t not in pos:
                pos[t] = ball_at(seq, t, f)
            return pos[t]
        low = min(p(t).z for t in times)
        new, raised = [], 0
        for t, v in zip(times, vals):
            a, b = p(t - step), p(t + step)
            dt = (min(length, t + step) - max(0.0, t - step)) or step
            speed = math.hypot(b.x - a.x, b.y - a.y) / dt
            planted = p(t).z < low + LOW_CM and speed < SPEED_CMS
            nv = 1.0 if planted else v
            if nv != v and v < 0.99:
                raised += 1
            new.append(nv)
        if raised:
            unreal.AnimationLibrary.remove_curve(seq, name, False)
            unreal.AnimationLibrary.add_curve(seq, name, unreal.RawCurveTrackTypes.RCT_FLOAT, False)
            unreal.AnimationLibrary.add_float_curve_keys(seq, name, times, new)
            changed = True
        entry["raised_" + f] = raised
        entry["keys_" + f] = len(times)
    if changed:
        unreal.EditorAssetLibrary.save_asset(path, only_if_is_dirty=False)
    entry["saved"] = changed
    report.append(entry)
json.dump(report, open(OUT, "w"), indent=1)
unreal.log("contact_fix: %d clips, %d changed -> %s" % (len(report), sum(1 for r in report if r["saved"]), OUT))
