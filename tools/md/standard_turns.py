"""The turns record of a standard draping body (Kiln's bodies/standard_body.py, 16 Nov 2026): which joint turns made
it from its reference-pose body, read from the two files themselves, and checked by bending the standard body back
onto the reference body.

    python tools/md/standard_turns.py REFERENCE.fbx STANDARD.fbx OUT.json [--joints joints-mm.json] [--check CHECK.json]

OUT.json is the record bend_back.py (and tools/md/unpose_garment.py) read, in pose_body.py's layout, so write it as
STANDARD.json beside STANDARD.fbx (pose_body.py's own naming).

WHY, 17 November 2026 (Kiln M5 step a and planning step 2, KILN-M5-RIGGING-METHOD-2026-11-17.md section 3): the
standard bodies carry only BUILD-NOTE.md and joints-mm.json, while bending a drape back needs each turn's angle, axis
and pivot. The note asked for "a turns record per standard body ... written from standard_body.py's own turns (36.65
degrees about each elbow, the axis unverified) and checked: the standard body bent back must land on the
reference-pose body, within 1 mm".

HOW.
- The turns are recomputed by standard_body.py's own rule (step 4, Kiln commit 3d32458): for each side, from the
  reference skeleton's bind pose, the forearm's angle to the upper arm (shoulder to elbow; elbow to hand), about
  forearm x upper arm, through the elbow. That script records only the angle; the axis and pivot come from here.
- Bones: every bone of the standard file is compared with its reference bone moved by the turns (each turn moves its
  bone and all below it). Bones placed otherwise, and bones in one file only, are listed as other changes.
- Skin: standard_body.py keeps one connected skin (points at one place, within 0.01 mm, joined) and leaves the rest
  out, keeping the points' order; the same rule applied to the reference mesh gives which reference point each
  standard point is. Then (1) the reference skin moved forward by the turns (skin weights shared out as Blender's
  armature modifier does) must give the standard skin, (2) the standard skin bent back with bend_back.py's exact
  inverse must give the reference skin, both within --tol-mm (1 mm by default), and (3) the skin weights must be the
  reference's. The blend-of-inverses way (unpose_garment.py's) is measured beside it for comparison.
- joints-mm.json, when given, is compared with the standard file's joints (Kiln millimetres: x, height, forward).
A body with a joined head (Darren) has standard points with no reference point: they are counted, not checked.
"""
import datetime
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from bend_back import bend_back_points, bone_groups, forward, group_shares, rotation_about, sha16, turn_from_joints  # noqa: E402

# standard_body.py's weld (metres): points closer than this are one point.
WELD_M = 1e-5


def components(verts, tris, weld=WELD_M):
    """Connected parts of a mesh, points at one place (to `weld`) joined: point-index arrays, largest first, each sorted."""
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    keys = np.round(np.asarray(verts, dtype=float) / weld).astype(np.int64)
    _, node = np.unique(keys, axis=0, return_inverse=True)
    node = node.ravel()
    n = int(node.max()) + 1 if len(node) else 0
    t = np.asarray(tris, dtype=np.int64)
    a = np.concatenate([node[t[:, 0]], node[t[:, 1]], node[t[:, 2]]])
    b = np.concatenate([node[t[:, 1]], node[t[:, 2]], node[t[:, 0]]])
    g = coo_matrix((np.ones(len(a)), (a, b)), shape=(n, n))
    _, lab = connected_components(g, directed=False)
    per_point = lab[node]
    parts = [np.nonzero(per_point == k)[0] for k in np.unique(per_point)]
    return sorted(parts, key=len, reverse=True)


def kiln_mm(p):
    """Blender metres (z up, facing -y) to Kiln's millimetres (x, height, forward), as standard_body.py's app_mm."""
    return [p[0] * 1000.0, p[2] * 1000.0, -p[1] * 1000.0]


def rot_angle_deg(R):
    c = (np.trace(R) - 1.0) / 2.0
    return float(np.degrees(np.arccos(np.clip(c, -1.0, 1.0))))


def stats_mm(d_m):
    d = np.asarray(d_m) * 1000.0
    if not len(d):
        return {"n": 0}
    return {"n": int(len(d)), "max": round(float(d.max()), 4), "p99": round(float(np.percentile(d, 99)), 4),
            "median": round(float(np.median(d)), 4)}


def make_record(ref, std, ref_path, std_path, joints_path=None, tol_mm=1.0):
    """(record, check) for a reference body and its standard body, both read by fbx_skin.load_skinned."""
    record = {"source": ref_path.replace("\\", "/"), "sourceSha256_16": sha16(ref_path),
              "standardBody": std_path.replace("\\", "/"), "standardBodySha256_16": sha16(std_path),
              "made": datetime.date.today().isoformat(), "madeBy": "tools/md/standard_turns.py",
              "frame": "Blender world: metres, z up, the body facing -y (as tools/md/pose_body.py records turns)",
              "rule": "Kiln bodies/standard_body.py step 4 (commit 3d32458): each forearm turned about its elbow onto "
                      "the upper arm's line; angle and axis recomputed here from the reference skeleton's bind pose",
              "turns": {}}
    for s in "lr":
        t = turn_from_joints(ref.joint("upperarm_" + s), ref.joint("lowerarm_" + s), ref.joint("hand_" + s))
        R = rotation_about(t["axis"], t["turnDeg"], t["elbow"])
        h2 = R[:3, :3] @ ref.joint("hand_" + s) + R[:3, 3]
        e = ref.joint("lowerarm_" + s)
        up = e - ref.joint("upperarm_" + s)
        after = float(np.degrees(np.arccos(np.clip((h2 - e) @ up / np.linalg.norm(h2 - e) / np.linalg.norm(up), -1, 1))))
        record["turns"][s] = {"elbow": {"turnDeg": round(t["turnDeg"], 6), "axis": [round(c, 9) for c in t["axis"]],
                                        "elbow": [round(c, 7) for c in t["elbow"]], "bendAfterDeg": round(after, 4)}}
    turns = [{"bone": "lowerarm_" + s, "pivot": record["turns"][s]["elbow"]["elbow"], "axis": record["turns"][s]["elbow"]["axis"],
              "deg": record["turns"][s]["elbow"]["turnDeg"], "side": s, "kind": "elbow"} for s in "lr"]
    check = {"tolMm": tol_mm, "reference": record["source"], "standard": record["standardBody"]}
    # bones
    bone_group, mats = bone_groups(turns, ref.subtree, list(ref.bones))
    turned = {s: sorted(b for b, g in bone_group.items() if g != 0 and b in ref.subtree("lowerarm_" + s)) for s in "lr"}
    record["bonesTurned"] = {s: len(v) for s, v in turned.items()}
    pos_err, rot_err, other = {}, {}, []
    for b, W in ref.bones.items():
        if b not in std.bones:
            other.append({"bone": b, "change": "in the reference only"})
            continue
        M = mats[bone_group[b]]
        pred = M[:3, :3] @ W[:3, 3] + M[:3, 3]
        pe = float(np.linalg.norm(pred - std.bones[b][:3, 3]))
        re = rot_angle_deg((M[:3, :3] @ W[:3, :3]).T @ std.bones[b][:3, :3])
        cls = "turned" if bone_group[b] else "still"
        pos_err.setdefault(cls, []).append(pe)
        rot_err.setdefault(cls, []).append(re)
        if pe * 1000.0 > 0.05:
            other.append({"bone": b, "change": "placed otherwise than the turns give", "mm": round(pe * 1000.0, 3), "deg": round(re, 3)})
        elif re > 0.05:
            # In place, its frame turned a little: a bone's rest frame does not move the rest skin (the skin check
            # below decides), so this is listed and fails nothing.
            other.append({"bone": b, "change": "in place, its frame turned otherwise (lists only)", "mm": round(pe * 1000.0, 3),
                          "deg": round(re, 3)})
    for b in std.bones:
        if b not in ref.bones:
            other.append({"bone": b, "change": "in the standard only"})
    check["bones"] = {cls: {"count": len(v), "positionMmMax": round(1000 * max(v), 4), "turnDegMax": round(max(rot_err[cls]), 4)}
                      for cls, v in pos_err.items()}
    check["bonesOtherwise"] = other
    for s in "lr":
        h = std.joint("hand_" + s)
        R = rotation_about(turns["lr".index(s)]["axis"], turns["lr".index(s)]["deg"], turns["lr".index(s)]["pivot"])
        check.setdefault("handMm", {})[s] = round(1000 * float(np.linalg.norm(R[:3, :3] @ ref.joint("hand_" + s) + R[:3, 3] - h)), 4)
    if joints_path:
        with open(joints_path, encoding="utf-8") as f:
            jm = json.load(f)
        diffs = {j: round(float(np.linalg.norm(np.array(kiln_mm(std.joint(j))) - np.array(v))), 3) for j, v in jm.items()}
        check["jointsFileMm"] = {"file": joints_path.replace("\\", "/"), "max": max(diffs.values()), "each": diffs}
    # skin: which reference point each standard point is
    parts = components(ref.verts, ref.tris)
    kept = parts[0]
    check["skin"] = {"referencePoints": int(len(ref.verts)), "standardPoints": int(len(std.verts)),
                     "referenceParts": len(parts), "keptPart": int(len(kept)),
                     "leftOut": {"parts": len(parts) - 1, "points": int(len(ref.verts) - len(kept))}}
    n = min(len(kept), len(std.verts))
    if len(kept) != len(std.verts):
        check["skin"]["note"] = ("the standard skin has %d points beyond the reference's kept part (a joined head): not "
                                 "checked" % (len(std.verts) - len(kept))) if len(std.verts) > len(kept) else \
                                "the standard skin has fewer points than the reference's kept part: matched by order up to it"
    ref_sh = group_shares(len(ref.verts), ref.weights, bone_group, len(mats))[kept[:n]]
    std_sh = group_shares(len(std.verts), std.weights, bone_group, len(mats))[:n]
    ref_pts, std_pts = ref.verts[kept[:n]], std.verts[:n]
    still = np.linalg.norm(std_pts - ref_pts, axis=1)
    fwd = np.linalg.norm(forward(ref_pts, ref_sh, mats) - std_pts, axis=1)
    back = np.linalg.norm(bend_back_points(std_pts, std_sh, mats, "exact") - ref_pts, axis=1)
    lbs = np.linalg.norm(bend_back_points(std_pts, std_sh, mats, "lbs") - ref_pts, axis=1)
    moving = std_sh[:, 1:].sum(axis=1) > 1e-6
    blended = moving & (std_sh[:, 1:].sum(axis=1) < 1 - 1e-6)
    check["skin"].update({
        "pointsTurned": int(moving.sum()), "pointsBlendedAtElbow": int(blended.sum()),
        "standardVsReferenceUnbentMm": stats_mm(still),
        "referenceTurnedForwardVsStandardMm": stats_mm(fwd),
        "standardBentBackVsReferenceMm": stats_mm(back),
        "standardBentBackOverTol": int(np.sum(back * 1000 > tol_mm)),
        "blendOfInversesVsReferenceMm": stats_mm(lbs),
        "blendOfInversesOverTol": int(np.sum(lbs * 1000 > tol_mm)),
        "pointsMovedOtherwise": int(np.sum(fwd * 1000 > tol_mm)),
    })
    # weights: the standard's per bone against the reference's on the same points
    wdiff = 0.0
    remap = -np.ones(len(ref.verts), dtype=np.int64)
    remap[kept[:n]] = np.arange(n)
    for b in set(ref.weights) | set(std.weights):
        a = np.zeros(n)
        c = np.zeros(n)
        if b in ref.weights:
            i, w = ref.weights[b]
            ok = remap[i] >= 0
            np.add.at(a, remap[i[ok]], w[ok])
        if b in std.weights:
            i, w = std.weights[b]
            ok = i < n
            np.add.at(c, i[ok], w[ok])
        wdiff = max(wdiff, float(np.abs(a - c).max()))
    check["skin"]["weightsMaxDiff"] = round(wdiff, 6)
    ok = (check["skin"]["standardBentBackOverTol"] == 0 and check["skin"]["pointsMovedOtherwise"] == 0
          and max(check["handMm"].values()) <= tol_mm
          and not [o for o in other if o["change"] in ("in the reference only", "placed otherwise than the turns give")]
          and wdiff <= 1e-3)
    check["verdict"] = "PASS" if ok else "FAIL"
    record["check"] = {"verdict": check["verdict"], "tolMm": tol_mm,
                       "standardBentBackVsReferenceMm": check["skin"]["standardBentBackVsReferenceMm"],
                       "handMm": check["handMm"],
                       "otherChanges": [dict(o) for o in other],
                       "leftOut": check["skin"]["leftOut"]}
    # what the standard changed, in words, from the measures above
    sk = check["skin"]
    changes = ["each forearm turned about its elbow onto the upper arm's line: left %.4f, right %.4f degrees (the turns "
               "above); %d bones on the left and %d on the right turned with it (lowerarm and all below it)"
               % (record["turns"]["l"]["elbow"]["turnDeg"], record["turns"]["r"]["elbow"]["turnDeg"],
                  record["bonesTurned"]["l"], record["bonesTurned"]["r"]),
               "the turned skin made the rest shape and the turned skeleton the rest pose: %d skin points move with the "
               "turns, %d of them shared between the arm bones at the elbows" % (sk["pointsTurned"], sk["pointsBlendedAtElbow"]),
               "%d parts not joined to the skin left out (%d points); the %d points kept are the reference's in its own "
               "order" % (sk["leftOut"]["parts"], sk["leftOut"]["points"], sk["keptPart"])]
    if len(std.verts) > len(kept):
        changes.append("%d points added beyond the reference's (a joined head)" % (len(std.verts) - len(kept)))
    if sk["pointsMovedOtherwise"]:
        changes.append("%d skin points moved otherwise than the turns give (over %.1f mm)" % (sk["pointsMovedOtherwise"], tol_mm))
    else:
        changes.append("no skin point moved otherwise than the turns give (all within %.4f mm)"
                       % sk["referenceTurnedForwardVsStandardMm"]["max"])
    changes.append("skin weights unchanged (largest difference %g)" % sk["weightsMaxDiff"] if wdiff <= 1e-3
                   else "skin weights changed (largest difference %g)" % wdiff)
    moved_bones = [o for o in other if o["change"] == "placed otherwise than the turns give"]
    framed = [o for o in other if o["change"].startswith("in place")]
    changes.append("%d bones placed otherwise than the turns give" % len(moved_bones) if moved_bones
                   else "no bone placed otherwise than the turns give")
    if framed:
        changes.append("%d bones in place with their frames turned up to %.3f degrees (%s): no effect on the rest skin"
                       % (len(framed), max(o["deg"] for o in framed), ", ".join(o["bone"] for o in framed)))
    record["changes"] = changes
    return record, check


def main(argv):
    pos = [a for a in argv if not a.startswith("--")]
    def opt(name, default=None):
        if name in argv:
            v = argv[argv.index(name) + 1]
            pos.remove(v)
            return v
        return default
    joints = opt("--joints")
    check_path = opt("--check")
    tol = float(opt("--tol-mm", "1.0"))
    if len(pos) != 3:
        print(__doc__)
        return 2
    from fbx_skin import load_skinned
    ref_path, std_path, out = pos
    if os.path.abspath(out) in (os.path.abspath(ref_path), os.path.abspath(std_path)):
        raise SystemExit("refusing to write over a body file")
    record, check = make_record(load_skinned(ref_path), load_skinned(std_path), ref_path, std_path, joints, tol)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=1)
    if check_path:
        with open(check_path, "w", encoding="utf-8") as f:
            json.dump(check, f, indent=1)
    print("TURNS " + json.dumps({"verdict": check["verdict"], "turns": {s: record["turns"][s]["elbow"]["turnDeg"] for s in "lr"},
                                 "bentBackMm": check["skin"]["standardBentBackVsReferenceMm"],
                                 "blendOfInversesMm": check["skin"]["blendOfInversesVsReferenceMm"]}), flush=True)
    return 0 if check["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
