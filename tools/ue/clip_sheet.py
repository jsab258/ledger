# THE CLIP SHEET OF A SPOT'S CLIPS, measured once from the assets (28 October 2026, his order D10; the method's
# step 2, production/research/sit-and-turn/SPOTS-2026-10-28.md). For every clip a seat in production/specs/seats.json
# names (In, Loop, Out), sampled at 60 per second with root motion left in the root, in the clip's own frame:
#   - length, root travel (cm) and turn (degrees) from first frame to last;
#   - the warp window and its warp bone, read from the clip's notify states where Python can reach them (else "unread");
#   - every bone named like a warp or attach bone, its offset from the root at the window's end;
#   - the pelvis at the clip's end against that bone and the floor (the seated height, for the +-3 cm check);
#   - per frame the planted foot (the ball within 1.5 cm of its lowest for 4 frames or more) and the stance phase
#     (0 to 100 through that foot's planted span), the start table step 6 chooses from;
#   - the head's lowest point and the neck's greatest bend (the fold Epic's clips show, flagged, never fixed here).
# Built on production/research/sit-and-turn/metahuman-route-2026-10-24/runs/clip_feet_all.py (the same sampling).
# Run: UnrealEditor-Cmd.exe ue-probe/LedgerProbe.uproject -run=pythonscript -script=<full path of this file>
#      -EnablePlugins=PythonScriptPlugin   (never while the build machine builds; the full path, or it fails quietly)
import json
import math
import os
import unreal

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.environ.get("LEDGER_CLIP_SHEET", "F:/LedgerTools/scratch/sit/clip_sheet.json")
CLIP_DIR = "/Game/Characters/UEFN_Mannequin/Animations/Interactions/Bench/"
L = []


def seq_of(name):
    # a seat names montages; the sheet measures each montage's own sequence (the same name without _Montage)
    base = name[:-len("_Montage")] if name.endswith("_Montage") else name
    a = unreal.load_asset(CLIP_DIR + base + "." + base)
    return a if isinstance(a, unreal.AnimSequence) else None


def bones_of(seq):
    try:
        sk = seq.get_editor_property("skeleton")
        return [str(b) for b in unreal.SkeletonLibrary.get_bone_names(sk)] if hasattr(unreal, "SkeletonLibrary") else []
    except Exception:
        return []


def warp_notifies(seq):
    out = []
    try:
        evs = unreal.AnimationLibrary.get_animation_notify_events(seq)
    except Exception as e:
        return "unread: %s" % str(e)[:80]
    for ev in evs:
        try:
            st = ev.get_editor_property("notify_state_class")
            if st is None or "Warp" not in st.get_class().get_name():
                continue
            row = {"class": st.get_class().get_name()}
            for k in ("link_value", "trigger_time_offset", "duration"):
                try:
                    row[k] = round(float(ev.get_editor_property(k)), 3)
                except Exception:
                    pass
            try:
                mod = st.get_editor_property("root_motion_modifier")
                for k in ("warp_target_name", "warp_point_anim_provider", "warp_point_anim_bone_name", "b_warp_translation", "b_ignore_z_axis"):
                    try:
                        row[k] = str(mod.get_editor_property(k))
                    except Exception:
                        pass
            except Exception:
                pass
            out.append(row)
        except Exception as e:
            out.append({"unread": str(e)[:80]})
    return out


def measure(name):
    seq = seq_of(name)
    if seq is None:
        return {"clip": name, "error": "no sequence"}
    length = seq.get_play_length()
    opts = unreal.AnimPoseEvaluationOptions()
    for k, v in (("should_retarget", False), ("extract_root_motion", False)):
        try:
            opts.set_editor_property(k, v)
        except Exception:
            pass
    names = bones_of(seq)
    special = [b for b in names if any(w in b.lower() for w in ("attach", "warp", "interaction", "ik_hand_root", "seat"))]
    want = ["root", "pelvis", "head", "neck_01", "neck_02", "ball_l", "ball_r"] + special
    rows = []
    for i in range(int(length * 60) + 1):
        t = min(length, i / 60.0)
        pose = unreal.AnimPoseExtensions.get_anim_pose_at_time(seq, t, opts)
        P = {}
        for b in want:
            try:
                tr = unreal.AnimPoseExtensions.get_bone_pose(pose, b, unreal.AnimPoseSpaces.WORLD)
                P[b] = (tr.translation.x, tr.translation.y, tr.translation.z, tr.rotation.rotator().yaw)
            except Exception:
                pass
        rows.append((t, P))
    r0, r1 = rows[0][1].get("root"), rows[-1][1].get("root")
    res = {"clip": name, "length": round(length, 3), "bones_special": special, "warp": warp_notifies(seq)}
    if r0 and r1:
        res["root_travel_cm"] = [round(r1[0] - r0[0], 1), round(r1[1] - r0[1], 1)]
        res["root_turn_deg"] = round(((r1[3] - r0[3] + 180.0) % 360.0) - 180.0, 1)
    end = rows[-1][1]
    if "pelvis" in end and r1:
        res["pelvis_end_cm"] = [round(end["pelvis"][k] - r1[k], 1) for k in range(3)]
    for b in special:
        if b in end and r1:
            res["end_offset_" + b] = [round(end[b][k] - r1[k], 1) for k in range(3)]
            if "pelvis" in end:
                res["pelvis_from_" + b] = [round(end["pelvis"][k] - end[b][k], 1) for k in range(3)]
    if all("head" in r[1] for r in rows):
        res["head_lowest_cm"] = round(min(r[1]["head"][2] for r in rows), 1)
    if all("neck_01" in r[1] and "head" in r[1] for r in rows):
        bend = 0.0
        for _, p in rows:
            dx, dy, dz = (p["head"][k] - p["neck_01"][k] for k in range(3))
            bend = max(bend, math.degrees(math.atan2(math.hypot(dx, dy), max(dz, 1e-6))))
        res["neck_bend_max_deg"] = round(bend, 1)
    table = []
    for f in ("l", "r"):
        key = "ball_" + f
        if not all(key in r[1] for r in rows):
            continue
        low = min(r[1][key][2] for r in rows)
        spans, cur = [], []
        for i, (t, p) in enumerate(rows):
            if p[key][2] < low + 1.5:
                cur.append(i)
            else:
                if len(cur) >= 4:
                    spans.append((cur[0], cur[-1]))
                cur = []
        if len(cur) >= 4:
            spans.append((cur[0], cur[-1]))
        for a, b in spans:
            for i in range(a, b + 1):
                rest = math.hypot(r1[0] - rows[i][1]["root"][0], r1[1] - rows[i][1]["root"][1]) if r1 else None
                table.append({"t": round(rows[i][0], 3), "foot": f, "phase": round(100.0 * (i - a) / max(1, b - a), 1),
                              "remaining_cm": round(rest, 1) if rest is not None else None})
    res["starts"] = sorted(table, key=lambda x: x["t"])
    return res


seats = json.load(open(os.path.join(REPO, "production", "specs", "seats.json"), encoding="utf-8"))
clips = []
for s in seats.get("seats", []):
    for c in list(s.get("in", [])) + [lp["clip"] for lp in s.get("loops", [])] + list(s.get("out", [])):
        if c not in clips:
            clips.append(c)
sheet = []
for c in clips:
    try:
        sheet.append(measure(c))
    except Exception as e:
        sheet.append({"clip": c, "error": str(e)[:120]})
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump({"made": "tools/ue/clip_sheet.py", "clips": sheet, "log": L}, open(OUT, "w", encoding="utf-8"), indent=1)
unreal.log("ledgerClipSheet clips=%d out=%s" % (len(sheet), OUT))
