"""The CMU retarget's measured check: review fix 8 of
production/research/ai-video-motion/CMU-RETARGET-METHOD-REVIEW-2026-11-17.md and fix 6 of
F:/LedgerTools/game-inputs/cmu-2026-11-17/STEP4-SCRIPT-REVIEW-2026-11-17.md.

    blender -b --factory-startup --python C:/Users/Jafar/ledger-local/tools/meshgen/blender/cmu_measure.py -- \
        [--out DIR] [--stand-frame N] SOURCE.fbx RETARGETED.fbx [SOURCE2.fbx RETARGETED2.fbx ...]
    blender -b --factory-startup --python .../cmu_measure.py -- --ue-result CMU_OUT/ue_result.json [--src-dir DIR] [--out DIR]
    blender -b --factory-startup --python .../cmu_measure.py -- --self SOURCE.fbx [...]   (source against itself)
    python .../cmu_measure.py --selftest        (synthetic tracks, no Blender, no Unreal output)

SOURCE is cmu_clips.py's motion-only clip (CMU bone names, rest = cgspeed's T-pose); RETARGETED is
cmu_ue_retarget.py's CMU_OUT/fbx/<clip>__<body>.fbx (MetaHuman bone names). Frames are paired by index.
A CMU source's rest pose is read from tpose_<subject>_<trial>.fbx beside it (Blender's FBX writer stores the
export-time pose, the clip's last frame, as a motion-only file's rest: measured 17 Nov, knees 9 to 35 degrees).
One JSON (DIR/<retargeted stem>.json, default DIR F:/LedgerTools/game-inputs/cmu-2026-11-17/measure) and one
printed line "cmuMeasure=PASS|FAIL ..." per pair. Measures and bars (review fix 8; how each was read):

- frames: the two files have the same frame count (the pairing is by index). Bar: equal.
- feet: a foot is planted while the SOURCE ball bone (LeftToeBase/RightToeBase) moves under 1 cm (3D) from the
  frame before; a span is a run of 2 or more planted frames. Over each span, on the retargeted file's foot and
  ball bones: slide = largest horizontal distance from the bone's place at the span's first frame; height = the
  span's lowest point against the floor, read as min over the span and both bones of (bone height - the bone's
  height in the rest pose, feet flat on the floor). Joint centres never touch the floor, so the rest pose sets each
  bone's contact height. No span at all fails. Bars RELATIVE TO THE SOURCE over the same span (session decision
  17 Nov: the source clips fail 2 cm absolute bars themselves, slide 2.4 to 13 cm, 131_01's height 4.2 cm): slide
  at most 2 cm more than the source's, height at most 2 cm further off the floor than the source's. The absolute
  worst values are written beside.
- knees: flexion = 180 - the angle at the knee between thigh and shin (thigh->calf->foot heads). Read on the
  retargeted file from the first frame of its last run at or above 97% of standing pelvis height to the end;
  standing height = the rest pose's pelvis height (scaled by the clip's leg length over the rest's, since
  Unreal writes the preview mesh's reference pose as the file's rest: EditorExporters.cpp 2465-2496,
  FbxSkeletalMeshExport.cpp 46-77). Each frame passes at most max(10, source knee + 3) degrees: "within 3 of
  the source where the source stands softer" read one-sided (a target straighter than the source never fails).
  No frame reaching 97% fails.
- flips: no limb bone (clavicle, upper arm, forearm, hand, thigh, calf, foot, ball; CMU: cmu_clips.is_limb)
  turns over 90 degrees between two 30 fps frames (local rotation, every round(fps/30) frames), on the
  retargeted file; the source file's count is written beside (cmu_clips.py checks the BVH). Twist, corrective
  and finger bones are not counted.
- stand: the method's single standing frame (step 4). The frame with both source balls planted and the source
  pelvis at or above 97% of its standing height where the source's knees are straightest (else the source
  pelvis's highest frame; --stand-frame N overrides, 0-based); both knees compared, same bar as knees.
- hands: not measured here (needs the chair's box in the film; the review allows a by-eye check), written as such.
"""
import json
import math
import os
import re
import sys

OUT_DIR = "F:/LedgerTools/game-inputs/cmu-2026-11-17/measure"
SRC_DIR = "F:/LedgerTools/game-inputs/cmu-2026-11-17"
PLANT_CM = 1.0      # source ball under 1 cm a frame
SLIDE_CM = 2.0      # slide at most 2 cm
HEIGHT_CM = 2.0     # lowest point within +-2 cm of the floor
KNEE_DEG = 10.0     # at most 10 degrees ...
KNEE_SRC_DEG = 3.0  # ... or within 3 of the source
STAND_FRAC = 0.97   # last time the pelvis reaches 97% of standing height
FLIP_DEG = 90.0     # a limb bone turning over 90 degrees between two 30 fps frames
ROLES = ("pelvis", "thigh_l", "calf_l", "foot_l", "ball_l", "thigh_r", "calf_r", "foot_r", "ball_r")
CMU = dict(pelvis="Hips", thigh_l="LeftUpLeg", calf_l="LeftLeg", foot_l="LeftFoot", ball_l="LeftToeBase",
           thigh_r="RightUpLeg", calf_r="RightLeg", foot_r="RightFoot", ball_r="RightToeBase")
MH = {r: r for r in ROLES}
CMU_LIMB_END = ("UpLeg", "Leg", "Foot", "ToeBase", "Arm", "ForeArm", "Hand", "Shoulder")  # as cmu_clips.py
MH_LIMB = re.compile(r"^(clavicle|upperarm|lowerarm|hand|thigh|calf|foot|ball)_(l|r)$")


def is_limb(name):
    if MH_LIMB.match(name):
        return True
    return name.startswith(("Left", "Right")) and name.endswith(CMU_LIMB_END) and "Finger" not in name


# ---------------------------------------------------------------- pure measures (no bpy)
def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def norm(a):
    return math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])


def angle(a, b):
    la, lb = norm(a), norm(b)
    if la < 1e-9 or lb < 1e-9:
        return 0.0
    c = (a[0] * b[0] + a[1] * b[1] + a[2] * b[2]) / (la * lb)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


def knee_flex(tr, s, i):
    """180 - the angle at the knee between thigh and shin = the angle between (knee-hip) and (ankle-knee)."""
    p = tr["pos"]
    return angle(sub(p["calf_" + s][i], p["thigh_" + s][i]), sub(p["foot_" + s][i], p["calf_" + s][i]))


def leg_len(pts):
    return (norm(sub(pts["calf_l"], pts["thigh_l"])) + norm(sub(pts["foot_l"], pts["calf_l"])) +
            norm(sub(pts["calf_r"], pts["thigh_r"])) + norm(sub(pts["foot_r"], pts["calf_r"]))) / 2.0


def body_scale(tr):
    """The clip's leg length over the rest pose's (Unreal's file rest is the preview mesh, maybe another body)."""
    rest = leg_len(tr["rest"])
    anim = leg_len({r: tr["pos"][r][0] for r in ROLES})
    return anim / rest if rest > 1e-6 else 1.0


def standing(tr):
    k = body_scale(tr)
    return tr["rest"]["pelvis"][2] * k, k


def planted(src, s):
    b = src["pos"]["ball_" + s]
    n = len(b)
    step = [norm(sub(b[i], b[i - 1])) for i in range(1, n)]
    if not step:
        return [False] * n
    return [step[0] < PLANT_CM] + [d < PLANT_CM for d in step]


def spans(flags, n_max):
    out, a = [], None
    for i, f in enumerate(flags[:n_max] + [False]):
        if f and a is None:
            a = i
        elif not f and a is not None:
            if i - 1 > a:
                out.append((a, i - 1))
            a = None
    return out


def span_numbers(tr, s, a, b, k):
    p, rest = tr["pos"], tr["rest"]
    slide, low = 0.0, None
    for bone in ("foot_" + s, "ball_" + s):
        x0, y0 = p[bone][a][0], p[bone][a][1]
        rz = rest[bone][2] * k
        for i in range(a, b + 1):
            slide = max(slide, math.hypot(p[bone][i][0] - x0, p[bone][i][1] - y0))
            off = p[bone][i][2] - rz
            low = off if low is None else min(low, off)
    return round(slide, 2), round(low, 2)


def quat_turn(q0, q1):
    l0, l1 = math.sqrt(sum(x * x for x in q0)), math.sqrt(sum(x * x for x in q1))
    d = abs(sum(x * y for x, y in zip(q0, q1))) / (l0 * l1)
    return math.degrees(2.0 * math.acos(min(1.0, d)))


def flips(tr):
    step = max(1, int(round(tr["fps"] / 30.0)))
    found = []
    for bone, qs in tr["rot"].items():
        if not is_limb(bone):
            continue
        for i in range(step, len(qs), step):
            a = quat_turn(qs[i - step], qs[i])
            if a > FLIP_DEG:
                found.append((bone, i, round(a, 1)))
    return found, step


def last_stand_run(h, top):
    above = [x >= top for x in h]
    if not any(above):
        return None
    i = len(h) - 1
    while not above[i]:
        i -= 1
    while i > 0 and above[i - 1]:
        i -= 1
    return i


def measure(src, tgt, stand_frame=None):
    """Every measure of review fix 8 for one pair of tracks; returns the result dict."""
    ns, nt = len(src["pos"]["pelvis"]), len(tgt["pos"]["pelvis"])
    n = min(ns, nt)
    M = []

    def add(name, value, bar, ok, **detail):
        M.append(dict(name=name, value=value, bar=bar, result="PASS" if ok else "FAIL", **detail))

    add("frames", [ns, nt], "equal frame counts (pairing by index)", ns == nt)
    s_stand, s_k = standing(src)
    t_stand, t_k = standing(tgt)
    # --- feet
    feet_rows, worst_slide, worst_low, any_span, over_src, low_over = [], 0.0, 0.0, False, 0.0, 0.0
    for s in "lr":
        for a, b in spans(planted(src, s), n):
            any_span = True
            ts, tl = span_numbers(tgt, s, a, b, t_k)
            ss, sl = span_numbers(src, s, a, b, s_k)
            feet_rows.append(dict(side=s, frames=[a, b], slide_cm=ts, low_cm=tl, source_slide_cm=ss, source_low_cm=sl))
            worst_slide = max(worst_slide, ts)
            over_src = max(over_src, ts - ss)
            worst_low = tl if abs(tl) > abs(worst_low) else worst_low
            low_over = max(low_over, abs(tl) - abs(sl))
    # RELATIVE TO THE SOURCE (session decision 17 Nov): the source clips fail the absolute bars themselves (slide 2.4 to
    # 13 cm: 1 cm a frame counts shuffles as planted; 131_01's height 4.2 cm), so the check judges what the retarget
    # adds: slide at most SLIDE_CM over the source's in the same span, height off the floor at most HEIGHT_CM worse.
    if any_span:
        add("feet_slide_cm", round(over_src, 2), "over source <= %.1f" % SLIDE_CM, over_src <= SLIDE_CM, spans=feet_rows,
            source_worst=round(max(r["source_slide_cm"] for r in feet_rows), 2), worst_slide=round(worst_slide, 2))
        add("feet_height_cm", round(low_over, 2), "worse than source <= %.1f" % HEIGHT_CM, low_over <= HEIGHT_CM,
            source_worst=max((r["source_low_cm"] for r in feet_rows), key=abs), worst_low=round(worst_low, 2))
    else:
        add("feet_slide_cm", None, "<= %.1f" % SLIDE_CM, False, why="no planted span on the source ball")
        add("feet_height_cm", None, "within +-%.1f" % HEIGHT_CM, False, why="no planted span on the source ball")
    # --- knees
    ht = [tgt["pos"]["pelvis"][i][2] for i in range(n)]
    hs = [src["pos"]["pelvis"][i][2] for i in range(n)]
    w0 = last_stand_run(ht, STAND_FRAC * t_stand)
    ws = last_stand_run(hs, STAND_FRAC * s_stand)
    bar_k = "<= max(%.0f, source + %.0f) deg" % (KNEE_DEG, KNEE_SRC_DEG)
    if w0 is None:
        add("knees_deg", None, bar_k, False, why="the pelvis never reaches 97%% of standing height %.1f cm (highest %.1f)"
            % (t_stand, max(ht)), standing_cm=round(t_stand, 1))
    else:
        worst = None
        for i in range(w0, n):
            for s in "lr":
                t, sv = knee_flex(tgt, s, i), knee_flex(src, s, i)
                ex = t - max(KNEE_DEG, sv + KNEE_SRC_DEG)
                if worst is None or ex > worst[0]:
                    worst = (ex, i, s, t, sv)
        add("knees_deg", round(worst[3], 1), bar_k, worst[0] <= 1e-9, frame=worst[1], side=worst[2],
            source_deg=round(worst[4], 1), window=[w0, n - 1], source_window_start=ws, standing_cm=round(t_stand, 1),
            body_scale=round(t_k, 4))
    # --- flips
    tf, tstep = flips(tgt)
    sf, _ = flips(src)
    add("limb_flips", len(tf), "0 turns over %.0f deg per 30 fps frame (every %d frames)" % (FLIP_DEG, tstep), not tf,
        first=tf[:10], source_flips=len(sf))
    # --- the single standing frame
    if stand_frame is None:
        pl, pr = planted(src, "l"), planted(src, "r")
        cand = [i for i in range(n) if pl[i] and pr[i] and hs[i] >= STAND_FRAC * s_stand]
        how = "both source balls planted, source pelvis >= 97%, straightest source knees"
        if not cand:
            cand = [max(range(n), key=lambda i: hs[i])]
            how = "source pelvis highest (no planted standing frame)"
        f = min(cand, key=lambda i: knee_flex(src, "l", i) + knee_flex(src, "r", i))
    else:
        f, how = min(max(0, stand_frame), n - 1), "given"
    rows, ok = {}, True
    for s in "lr":
        t, sv = knee_flex(tgt, s, f), knee_flex(src, s, f)
        rows[s] = dict(target_deg=round(t, 1), source_deg=round(sv, 1), diff_deg=round(t - sv, 1))
        ok = ok and t <= max(KNEE_DEG, sv + KNEE_SRC_DEG) + 1e-9
    worst_s = max("lr", key=lambda s: rows[s]["target_deg"] - rows[s]["source_deg"])
    add("stand_knee_deg", rows[worst_s]["target_deg"], bar_k, ok, frame=f, chosen=how, sides=rows)
    verdict = "PASS" if all(m["result"] == "PASS" for m in M) else "FAIL"
    return dict(verdict=verdict, measures=M, not_measured=[
        "hands: not measured by this tool (needs the chair's box; review fix 8 allows a by-eye check front and side)"],
        source_standing_cm=round(s_stand, 1), target_standing_cm=round(t_stand, 1))


def line(name, r):
    parts = []
    for m in r["measures"]:
        v = m["value"]
        v = "n/a" if v is None else (",".join(str(x) for x in v) if isinstance(v, list) else v)
        parts.append("%s=%s[%s]%s" % (m["name"], v, m["bar"].replace(" ", ""), m["result"]))
    return "cmuMeasure=%s pair=%s %s" % (r["verdict"], name, " ".join(parts))


# ---------------------------------------------------------------- Blender reader
def load_arm(path):
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=path, automatic_bone_orientation=False)
    arms = [o for o in bpy.context.scene.objects if o.type == "ARMATURE"]
    if not arms:
        raise RuntimeError("no armature in " + path)
    arm = max(arms, key=lambda o: len(o.pose.bones))
    names = set(b.name for b in arm.pose.bones)
    if "LeftUpLeg" in names:
        return arm, "CMU", CMU
    if "thigh_l" in names:
        return arm, "MetaHuman", MH
    raise RuntimeError("neither CMU nor MetaHuman leg bones in " + path)


def rest_of(arm, mp):
    mw = arm.matrix_world
    return {r: tuple(c * 100.0 for c in (mw @ arm.data.bones[mp[r]].head_local)) for r in ROLES}


def tpose_beside(path):
    """cmu_clips.py's skeleton file for a CMU clip: <dir>/tpose_<subject>_<trial>.fbx. A motion-only FBX that
    Blender wrote carries the pose at export time (the clip's last frame, measured 17 Nov) as its rest, not the
    T-pose; the T-pose file holds the true rest (bound stand-in, straight knees)."""
    m = re.search(r"(\d+_\d+)\.fbx$", os.path.basename(path), re.I)
    if not m:
        return None
    t = os.path.join(os.path.dirname(path), "tpose_%s.fbx" % m.group(1))
    return t if os.path.isfile(t) and os.path.abspath(t) != os.path.abspath(path) else None


def read_fbx(path):
    import bpy
    rest_from, rest = path, None
    arm, kind, mp = load_arm(path)
    if kind == "CMU":
        t = tpose_beside(path)
        if t:
            tarm, _, _ = load_arm(t)
            rest, rest_from = rest_of(tarm, mp), t
            arm, kind, mp = load_arm(path)
    act = arm.animation_data.action if arm.animation_data else None
    if act is None:
        raise RuntimeError("no animation in " + path)
    f0, f1 = int(round(act.frame_range[0])), int(round(act.frame_range[1]))
    sc = bpy.context.scene
    fps = sc.render.fps / sc.render.fps_base
    mw = arm.matrix_world
    cm = lambda v: (v.x * 100.0, v.y * 100.0, v.z * 100.0)
    rest = rest or rest_of(arm, mp)
    limbs = [b.name for b in arm.pose.bones if is_limb(b.name)]
    pos = {r: [] for r in ROLES}
    rot = {b: [] for b in limbs}
    for fr in range(f0, f1 + 1):
        sc.frame_set(fr)
        bpy.context.view_layer.update()
        for r in ROLES:
            pos[r].append(cm(mw @ arm.pose.bones[mp[r]].head))
        for b in limbs:
            q = arm.pose.bones[b].matrix_basis.to_quaternion()
            rot[b].append((q.w, q.x, q.y, q.z))
    tr = dict(path=path, kind=kind, fps=fps, frame_range=[f0, f1], pos=pos, rest=rest, rot=rot, rest_from=rest_from)
    tr["rest_knees_deg"] = [round(angle(sub(rest["calf_" + s], rest["thigh_" + s]), sub(rest["foot_" + s], rest["calf_" + s])), 1)
                            for s in "lr"]
    pz = rest["pelvis"][2] * body_scale(tr)
    if not 50.0 <= pz <= 130.0:
        raise RuntimeError("standing pelvis %.1f cm in %s: up axis or units wrong" % (pz, path))
    return tr


def run_pairs(pairs, out_dir, stand_frame=None):
    os.makedirs(out_dir, exist_ok=True)
    cache, bad = {}, 0
    for src_p, tgt_p, name in pairs:
        try:
            for p in (src_p, tgt_p):
                if p not in cache:
                    cache[p] = read_fbx(p)
            src, tgt = cache[src_p], cache[tgt_p]
            r = measure(src, tgt, stand_frame)
            r.update(source=src_p, target=tgt_p, source_kind=src["kind"], target_kind=tgt["kind"],
                     rest_from=[src["rest_from"], tgt["rest_from"]], rest_knees_deg=[src["rest_knees_deg"], tgt["rest_knees_deg"]],
                     fps=[src["fps"], tgt["fps"]], frame_ranges=[src["frame_range"], tgt["frame_range"]])
        except Exception as e:
            r = dict(verdict="FAIL", error=str(e)[:300], source=src_p, target=tgt_p, measures=[])
        out = os.path.join(out_dir, name + ".json")
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(r, fh, indent=1)
        print((line(name, r) if r["measures"] else "cmuMeasure=FAIL pair=%s error=%s" % (name, r["error"].replace(" ", "~")))
              + " json=" + out.replace(" ", "~"))
        bad += r["verdict"] != "PASS"
    print("cmuMeasureRun pairs=%d failed=%d" % (len(pairs), bad))
    return 0


# ---------------------------------------------------------------- selftest (synthetic, no bpy)
def synth(n=60, fps=30.0, flex=None, ankle=None, dz=0.0, pelvis_dz=None, rest_scale=1.0, rot=None):
    """A two-leg track: ankles fixed (or moved by ankle(i, s)), knees bending forward by flex(i) degrees,
    thighs and shins 45 cm, pelvis 5 cm above the hips, ball 12 cm ahead of and 5 cm below the ankle."""
    flex = flex or (lambda i: 2.0)
    pos = {r: [] for r in ROLES}
    for i in range(n):
        th = math.radians(flex(i)) / 2.0
        hipz = 0.0
        for s, y in (("l", 10.0), ("r", -10.0)):
            ax, ay, az = ankle(i, s) if ankle else (0.0, y, 8.0)
            az += dz
            hip = (ax, ay, az + 90.0 * math.cos(th))
            knee = (hip[0] + 45.0 * math.sin(th), ay, hip[2] - 45.0 * math.cos(th))
            pos["thigh_" + s].append(hip)
            pos["calf_" + s].append(knee)
            pos["foot_" + s].append((ax, ay, az))
            pos["ball_" + s].append((ax + 12.0, ay, az - 5.0))
            hipz = hip[2]
        pz = hipz + 5.0 + (pelvis_dz(i) if pelvis_dz else 0.0)
        pos["pelvis"].append((0.0, 0.0, pz))
    k = rest_scale
    rest = dict(pelvis=(0, 0, 103 * k), thigh_l=(0, 10, 98 * k), calf_l=(0, 10, 53 * k), foot_l=(0, 10, 8 * k),
                ball_l=(12, 10, 3 * k), thigh_r=(0, -10, 98 * k), calf_r=(0, -10, 53 * k), foot_r=(0, -10, 8 * k),
                ball_r=(12, -10, 3 * k))
    rots = {"calf_l": [(1.0, 0.0, 0.0, 0.0)] * n, "LeftFingerBase": [(1.0, 0.0, 0.0, 0.0)] * n}
    if rot:
        rots.update(rot)
    return dict(kind="synthetic", fps=fps, frame_range=[0, n - 1], pos=pos, rest=rest, rot=rots)


def sit_rise(i):
    """Stand 2 deg (0-9), down to 90 (to 25), seated (to 35), up to 4 (to 45), stand 4 deg (to 59)."""
    if i < 10:
        return 2.0
    if i < 25:
        return 2.0 + 88.0 * (i - 10) / 15.0
    if i < 35:
        return 90.0
    if i < 45:
        return 90.0 - 86.0 * (i - 35) / 10.0
    return 4.0


def qx(deg):
    h = math.radians(deg) / 2.0
    return (math.cos(h), math.sin(h), 0.0, 0.0)


def selftest():
    src = synth(flex=sit_rise)
    get = lambda r, name: next(m for m in r["measures"] if m["name"] == name)
    cases = []

    def case(label, tgt, expect, src_tr=None, **kw):
        r = measure(src_tr or src, tgt, **kw)
        got = {m["name"]: m["result"] for m in r["measures"]}
        ok = all(got[k] == v for k, v in expect.items())
        cases.append((label, ok, {k: (got[k], get(r, k)["value"]) for k in expect}))

    allpass = {k: "PASS" for k in ("frames", "feet_slide_cm", "feet_height_cm", "knees_deg", "limb_flips", "stand_knee_deg")}
    case("identical tracks pass every measure", synth(flex=sit_rise), allpass)
    case("target ball and foot slide 0.2 cm a frame while the source is planted: slide fails",
         synth(flex=sit_rise, ankle=lambda i, s: (0.2 * i, 10.0 if s == "l" else -10.0, 8.0)),
         dict(feet_slide_cm="FAIL", feet_height_cm="PASS"))
    case("target slides 0.03 cm a frame (1.8 cm over the clip): slide passes",
         synth(flex=sit_rise, ankle=lambda i, s: (0.03 * i, 10.0 if s == "l" else -10.0, 8.0)), dict(feet_slide_cm="PASS"))
    case("target floats 3 cm: height fails", synth(flex=sit_rise, dz=3.0), dict(feet_height_cm="FAIL", knees_deg="PASS"))
    case("target sinks 2.5 cm: height fails", synth(flex=sit_rise, dz=-2.5), dict(feet_height_cm="FAIL"))
    case("target 1.5 cm low: height passes", synth(flex=sit_rise, dz=-1.5), dict(feet_height_cm="PASS"))
    case("target stands 10 deg bent past the source (12 and 14 against 2 and 4): knees and stand fail",
         synth(flex=lambda i: sit_rise(i) + (10.0 if i >= 45 or i < 10 else 0.0)), dict(knees_deg="FAIL", stand_knee_deg="FAIL"))
    case("target stands at 9 and 10 deg against the source's 2 and 4: at most 10, knees and stand pass",
         synth(flex=lambda i: sit_rise(i) + (7.0 if i < 10 else 6.0 if i >= 45 else 0.0)),
         dict(knees_deg="PASS", stand_knee_deg="PASS"))
    soft = lambda i: max(sit_rise(i), 11.0)
    case("source stands soft at 11, target at 13: within 3 of the source, knees pass",
         synth(flex=lambda i: max(sit_rise(i), 13.0)), dict(knees_deg="PASS", stand_knee_deg="PASS"), src_tr=synth(flex=soft))
    case("source soft at 11, target at 15: knees fail",
         synth(flex=lambda i: max(sit_rise(i), 15.0)), dict(knees_deg="FAIL", stand_knee_deg="FAIL"), src_tr=synth(flex=soft))
    case("knees bent only while seated (before the last stand): knees pass", synth(flex=sit_rise), dict(knees_deg="PASS"))
    case("target pelvis 10 cm low throughout (never 97% standing): knees fail",
         synth(flex=sit_rise, pelvis_dz=lambda i: -10.0), dict(knees_deg="FAIL"))
    case("file rest is a 10% smaller preview mesh, clip on the real body: all pass", synth(flex=sit_rise, rest_scale=0.9), allpass)
    flip = [qx(0)] * 30 + [qx(120)] * 30
    case("target calf turns 120 deg in one frame: flips fail", synth(flex=sit_rise, rot={"calf_l": flip}), dict(limb_flips="FAIL"))
    case("a finger turns 170 deg: not a limb, flips pass", synth(flex=sit_rise, rot={"LeftFingerBase": [qx(0)] * 30 + [qx(170)] * 30}),
         dict(limb_flips="PASS"))
    ramp = [qx(min(50.0 * max(0, i - 20), 300.0)) for i in range(120)]
    case("60 fps file, calf 50 deg a frame (100 per 30 fps frame): flips fail",
         synth(n=120, fps=60.0, rot={"calf_l": ramp}), dict(limb_flips="FAIL"), src_tr=synth(n=120, fps=60.0))
    case("30 fps file, calf 50 deg a frame: flips pass", synth(n=120, fps=30.0, rot={"calf_l": ramp}), dict(limb_flips="PASS"),
         src_tr=synth(n=120))
    case("frame counts differ: frames fails", synth(n=59, flex=sit_rise), dict(frames="FAIL"))
    case("source ball always moving 1.5 cm a frame: no span, feet fail",
         synth(), dict(feet_slide_cm="FAIL", feet_height_cm="FAIL"),
         src_tr=synth(ankle=lambda i, s: (1.5 * i, 10.0 if s == "l" else -10.0, 8.0)))
    case("stand frame given (frame 30, seated 90 deg on both): stand passes against the source", synth(flex=sit_rise),
         dict(stand_knee_deg="PASS"), stand_frame=30)
    for label, ok, got in cases:
        print("%s  %s  %s" % ("ok  " if ok else "FAIL", label, got))
    bad = sum(not ok for _, ok, _ in cases)
    print("cmuMeasureSelftest=%s cases=%d failed=%d" % ("PASS" if not bad else "FAIL", len(cases), bad))
    return 1 if bad else 0


def main(argv):
    out, stand, ue, src_dir, selfpairs, files = OUT_DIR, None, None, SRC_DIR, False, []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--selftest":
            return selftest()
        if a in ("--out", "--stand-frame", "--ue-result", "--src-dir"):
            v = argv[i + 1]
            i += 2
            if a == "--out":
                out = v
            elif a == "--stand-frame":
                stand = int(v)
            elif a == "--ue-result":
                ue = v
            else:
                src_dir = v
            continue
        if a == "--self":
            selfpairs = True
        else:
            files.append(a)
        i += 1
    pairs = []
    if ue:
        res = json.load(open(ue, encoding="utf-8"))
        for o in res.get("outputs", []):
            for clip, c in o.get("clips", {}).items():
                if c.get("exported") and c.get("fbx"):
                    pairs.append((os.path.join(src_dir, clip + ".fbx"), c["fbx"], os.path.splitext(os.path.basename(c["fbx"]))[0]))
    elif selfpairs:
        pairs = [(f, f, os.path.splitext(os.path.basename(f))[0] + "__self") for f in files]
    else:
        if len(files) % 2:
            print("cmuMeasure=FAIL error=give~SOURCE~RETARGETED~pairs")
            return 2
        pairs = [(files[k], files[k + 1], os.path.splitext(os.path.basename(files[k + 1]))[0]) for k in range(0, len(files), 2)]
    if not pairs:
        print("cmuMeasure=FAIL error=no~pairs")
        return 2
    return run_pairs(pairs, out, stand)


if __name__ == "__main__":
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    sys.exit(main(args))
