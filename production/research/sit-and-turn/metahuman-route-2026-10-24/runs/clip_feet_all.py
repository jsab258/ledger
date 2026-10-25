# Every clip Epic's motion matching can pick for walking, measured from the assets themselves (25 October,
# his order of 25 October, item 2: "Measure the remaining clips, then fix").
# For each clip and each foot: the longest travel of the ball while it is flat on the ground (within 1.5 cm of
# its lowest for 4 frames or more), in the clip's own frame with root motion included, so a planted foot
# should not travel at all (root motion left in the root bone: extracting it pins the root and makes every planted
# foot appear to travel a full stride); and what the clip's contact curve says during that span.
# Run: UnrealEditor-Cmd.exe ue-probe/LedgerProbe.uproject -run=pythonscript -script=<this> -EnablePlugins=PythonScriptPlugin
import unreal, math, json
OUT = "F:/LedgerTools/scratch/gasp-export/clip_feet_all.json"
L = []
reg = unreal.AssetRegistryHelpers.get_asset_registry()


def dbs():
    out = {}
    for a in reg.get_assets_by_class(unreal.TopLevelAssetPath("/Script/PoseSearch", "PoseSearchDatabase"), True):
        out[str(a.asset_name)] = str(a.package_name)
    return out


def db_anims(path):
    # the database's own clip list is not exposed to Python in 5.8; its package's hard dependencies are its clips
    opts = unreal.AssetRegistryDependencyOptions(include_soft_package_references=False, include_hard_package_references=True)
    deps = [str(d) for d in (reg.get_dependencies(unreal.Name(path), opts) or [])]
    seqs = []
    for d in deps:
        for a in reg.get_assets_by_package_name(unreal.Name(d)):
            if str(a.asset_class_path.asset_name) == "AnimSequence":
                seqs.append(d)
    if seqs:
        return seqs
    db = unreal.load_asset(path)
    names = []
    for prop in ("animation_assets", "database_animation_assets"):
        try:
            arr = db.get_editor_property(prop)
        except Exception:
            continue
        for e in arr:
            for k in ("anim_asset", "animation_asset", "sequence"):
                try:
                    a = e.get_editor_property(k)
                    if a:
                        names.append(a.get_path_name().split(".")[0])
                        break
                except Exception:
                    pass
        if names:
            break
    return names


def curve(seq, name):
    try:
        t, v = unreal.AnimationLibrary.get_float_keys(seq, unreal.Name(name))
        return list(t), list(v)
    except Exception:
        return [], []


def at(keys, t):
    ts, vs = keys
    if not ts:
        return None
    if t <= ts[0]:
        return vs[0]
    for i in range(1, len(ts)):
        if t <= ts[i]:
            a = (t - ts[i - 1]) / max(1e-6, ts[i] - ts[i - 1])
            return vs[i - 1] + (vs[i] - vs[i - 1]) * a
    return vs[-1]


def measure(path):
    seq = unreal.load_asset(path)
    if not isinstance(seq, unreal.AnimSequence):
        return None
    length = seq.get_play_length()
    ck = {f: curve(seq, "contact_" + f) for f in ("l", "r")}
    opts = unreal.AnimPoseEvaluationOptions()
    for k, v in (("should_retarget", False), ("extract_root_motion", False)):
        try:
            opts.set_editor_property(k, v)
        except Exception:
            pass
    rows = []
    n = int(length * 60) + 1
    for i in range(n):
        t = min(length, i / 60.0)
        pose = unreal.AnimPoseExtensions.get_anim_pose_at_time(seq, t, opts)
        P = {b: unreal.AnimPoseExtensions.get_bone_pose(pose, b, unreal.AnimPoseSpaces.WORLD).translation for b in ("root", "ball_l", "ball_r")}
        rows.append((t, P))
    res = {"clip": path.split("/")[-1], "path": path, "length": round(length, 3),
           "root_travel_cm": round(math.hypot(rows[-1][1]["root"].x - rows[0][1]["root"].x, rows[-1][1]["root"].y - rows[0][1]["root"].y), 1)}
    for f in ("l", "r"):
        low = min(r[1]["ball_" + f].z for r in rows)
        best, span, start, cnt = 0.0, None, None, 0
        for r in rows:
            p = r[1]["ball_" + f]
            if p.z < low + 1.5:
                if start is None:
                    start, cnt = (p.x, p.y, r[0]), 0
                cnt += 1
                d = math.hypot(p.x - start[0], p.y - start[1])
                if cnt >= 4 and d > best:
                    best, span = d, (start[2], r[0])
            else:
                start = None
        c = None
        if span:
            vals = [at(ck[f], span[0] + (span[1] - span[0]) * k / 10.0) for k in range(11)]
            vals = [v for v in vals if v is not None]
            c = (round(min(vals), 2), round(max(vals), 2)) if vals else None
        res["flat_travel_" + f] = round(best, 1)
        res["flat_span_" + f] = [round(span[0], 2), round(span[1], 2)] if span else None
        res["contact_during_" + f] = c
        res["contact_keys_" + f] = len(ck[f][0])
    return res


found = dbs()
L.append("databases: %d" % len(found))
targets = {}
WANT = ("PSD_Dense_Stand_Walk_", "PSD_Dense_Stand_TurnInPlace", "PSD_Dense_Stand_Idles")
for name, path in sorted(found.items()):
    if not name.startswith(WANT):
        continue
    anims = db_anims(path)
    L.append("%s: %d animations" % (name, len(anims)))
    for a in anims:
        targets.setdefault(a, []).append(name)
results = []
for path, in_dbs in sorted(targets.items()):
    try:
        r = measure(path)
    except Exception as e:
        L.append("ERR %s %s" % (path, str(e)[:80]))
        continue
    if r:
        r["databases"] = in_dbs
        results.append(r)
json.dump({"log": L, "clips": results}, open(OUT, "w"), indent=1)
unreal.log("clip_feet_all: %d databases, %d walk clips measured -> %s" % (len(found), len(results), OUT))
