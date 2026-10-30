"""HOW A SKINNED PAIR OF BOOTS (OR SHOES) SITS ON ITS WEARER AND UNDER HIS TROUSERS, posed, measured before Unreal
(30 October 2026, Tom's boots carried from Ron's; shoe_pose_check.py's poses, its measure taken in the pose itself
since a boot's shaft rides the calf and is not rigid on the foot).

    blender -b --factory-startup -P tools/meshgen/blender/footwear_pose_check.py -- PAIR.blend OUT.json
        [--pair tom_boots] [--depth 0.001] [--jeans JEANS_SKINNED.fbx] [--render DIR]

PAIR.blend is carry_footwear.py's (or skin_shoes.py's): the skeleton, the body (its finest mesh, skinned) and the pair.
Poses from the reference pose: rest; walking (the front foot's toes up 12 degrees at heel strike, the back foot's
heel up 20 and its toes bent up 35 at the ball for the push-off); sitting (thighs forward 90, knees 90, the feet
relaxed 10 down); stair, a foot up a stair (the left thigh forward 55, its knee bent 75, as pose_skinned.py's stair,
then the left shin 25 degrees forward over its flat foot, the step's weight coming onto it); toe bend (45 at the
ball).

Per pose:
  - THROUGH: the boot's visible outside (its faces that face away from the foot's bones, knee to toes, and see out
    past the boot itself: the leather's outer face, the sole, welt, laces and eyelets) sampled at its points and faces' middles, and each
    sample lying inside the posed body by more than --depth (the nearest face's side, confirmed by rays: at least 5
    of 7 say inside), so the skin stands outside the leather there and shows through it;
  - HIDDEN INSIDE: the same for the boot's hidden faces (the lining, the inner sole, the collar's turn-in): the leather
    there lies in the skin, unseen from outside; listed, not a fault;
  - the worst stretch of the boot's edges against rest.
With --jeans (a skinned FBX on the same skeleton; both raised alike, as the game raises the wearer by the sole):
  - BOOT POINTS THROUGH THE JEANS: the boot's points (all, and its visible outside) outside the jeans' leg by more
    than --depth where the leg covers them (a ray from the point to the shin's axis crosses the cloth);
  - THE HEMS ON THE BOOTS: each hem's points (the leg's lowest open edge) above the sole's floor (the ground in the
    game; read in the foot's own frame, so in a pose it is the height on the boot), at the front, the sides and the back, how many lie inside the boot (a ray from the point out from the shin's
    axis meets the boot's outside: the boot through the hem) and how deep, and the boot's top against the hem.
--render DIR draws each pose (front three-quarter, side, back), the body hidden under the pair as the game hides it.
"""
import json
import math
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:]
BLEND, OUT = argv[:2]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
PAIR = opt("--pair", "tom_boots", str)
DEPTH = opt("--depth", 0.001)
JEANS = opt("--jeans", None, str)
RENDER = opt("--render", None, str)

bpy.ops.wm.open_mainfile(filepath=BLEND)
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
pair = bpy.data.objects[PAIR]
body = max([o for o in bpy.data.objects if o.type == "MESH" and o is not pair], key=lambda o: len(o.data.vertices))
pb = arm.pose.bones
jeans = None
if JEANS:
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=JEANS)
    new = [o for o in bpy.data.objects if o not in before]
    jarm = next(o for o in new if o.type == "ARMATURE")
    jeans = max([o for o in new if o.type == "MESH"], key=lambda o: len(o.data.vertices))
    missing = [g.name for g in jeans.vertex_groups if g.name not in arm.data.bones]
    if missing:
        raise SystemExit("FOOTPOSE the jeans name bones the skeleton lacks: %s" % missing[:8])
    jrest = {b.name: (jarm.matrix_world @ b.head_local) for b in jarm.data.bones}
    off = max((jrest[b.name] - arm.matrix_world @ b.head_local).length for b in arm.data.bones if b.name in jrest)
    mw = jeans.matrix_world.copy()
    jeans.parent = None
    jeans.matrix_world = mw
    for m in list(jeans.modifiers):
        jeans.modifiers.remove(m)
    jm = jeans.modifiers.new("Armature", "ARMATURE")
    jm.object = arm
    for o in new:
        if o is not jeans:
            bpy.data.objects.remove(o, do_unlink=True)
    print("FOOTPOSE jeans", jeans.name, "points", len(jeans.data.vertices), "skeletons apart %.3f mm" % (off * 1000), flush=True)


def update():
    bpy.context.view_layer.update()


def reset():
    for p in pb:
        p.rotation_mode = "QUATERNION"
        p.matrix_basis = Matrix.Identity(4)
    update()


def head(b):
    return arm.matrix_world @ pb[b].head


def rotate_world(bone, axis, degrees):
    p = pb[bone]
    update()
    hw = arm.matrix_world @ p.head
    R = Matrix.Translation(hw) @ Matrix.Rotation(math.radians(degrees), 4, axis) @ Matrix.Translation(-hw)
    p.matrix = arm.matrix_world.inverted() @ R @ arm.matrix_world @ p.matrix
    update()


def turn_toward(bone, tip_fn, direction, deg):
    update()
    h = head(bone)
    t = tip_fn()
    axis = (t - h).cross(direction)
    if axis.length < 1e-6:
        return
    rotate_world(bone, axis.normalized(), deg)


reset()
fwd = head("ball_l") - head("foot_l")
fwd.z = 0
fwd.normalize()
UP = Vector((0, 0, 1))
TOE = {s: (lambda s=s: head("ball_" + s) + (head("ball_" + s) - head("foot_" + s)).normalized() * 0.06) for s in "lr"}


def flex_foot(s, deg):
    turn_toward("foot_" + s, lambda: head("ball_" + s), UP if deg > 0 else -UP, abs(deg))


def bend_toes(s, deg):
    turn_toward("ball_" + s, TOE[s], UP, deg)


def tilt_l():
    a = head("ball_l") - head("foot_l")
    return math.degrees(math.atan2(a.z, Vector((a.x, a.y, 0)).length))


TILT0 = tilt_l()


def pose(name):
    reset()
    if name == "walking":
        turn_toward("thigh_l", lambda: head("calf_l"), fwd, 28)
        turn_toward("thigh_r", lambda: head("calf_r"), -fwd, 18)
        turn_toward("calf_r", lambda: head("foot_r"), -fwd, 35)
        flex_foot("l", 12)
        flex_foot("r", -20)
        bend_toes("r", 35)
    elif name == "sitting":
        for s in "lr":
            turn_toward("thigh_" + s, lambda s=s: head("calf_" + s), fwd, 90)
            turn_toward("calf_" + s, lambda s=s: head("foot_" + s), Vector((0, 0, -1)), 90)
            flex_foot(s, -10)
    elif name == "stair":
        turn_toward("thigh_l", lambda: head("calf_l"), fwd, 55)
        turn_toward("calf_l", lambda: head("foot_l"), -fwd - UP, 75)
        # the foot back to flat on the step (its rest tilt), then the shin over it: the ankle bent 25 degrees more
        update()
        flex_foot("l", TILT0 - tilt_l())
        turn_toward("calf_l", lambda: head("foot_l"), -fwd, 25)
        flex_foot("l", 25)
    elif name == "toe bend":
        for s in "lr":
            bend_toes(s, 45)


def evaluated(o):
    dg = bpy.context.evaluated_depsgraph_get()
    e = o.evaluated_get(dg)
    m = e.to_mesh()
    P = np.array([tuple(o.matrix_world @ v.co) for v in m.vertices])
    m.calc_loop_triangles()
    T = [tuple(t.vertices) for t in m.loop_triangles]
    e.to_mesh_clear()
    return P, T


RAYS = [Vector(d).normalized() for d in ((0.12, 0.31, 0.94), (0.83, -0.4, 0.38), (-0.7, -0.6, 0.39), (-0.25, 0.9, -0.36),
                                         (0.5, 0.2, -0.84), (-0.9, 0.3, -0.3), (0.2, -0.97, -0.1))]


def inside(bvh, p, need=5):
    votes = 0
    for d in RAYS:
        n, t = 0, 0.0
        for _ in range(60):
            hit = bvh.ray_cast(p + d * (t + 1e-6), d, 3.0)
            if hit[0] is None:
                break
            t = (hit[0] - p).length
            n += 1
        votes += n % 2
    return votes >= need


def depth_in(bvh, p):
    hit, nrm, _f, d = bvh.find_nearest(p)
    if hit is None or (p - hit).dot(nrm) >= 0:
        return 0.0
    return d


# ---- the pair at rest: its faces' visibility, its samples ----------------------------------------------------------
reset()
S0, ST = evaluated(pair)
B0, BT = evaluated(body)
me = pair.data
polys = [tuple(p.vertices) for p in me.polygons]
mats = [m.name for m in me.materials]
pmat = [mats[p.material_index] for p in me.polygons]
bvh_s0 = BVHTree.FromPolygons([tuple(v) for v in S0], ST)
bvh_b0 = BVHTree.FromPolygons([tuple(v) for v in B0], BT)
rng = np.random.default_rng(7)


def chain(s):
    """The foot's bones as a line: knee, ankle, ball, toes (the boot's own middle, whatever the skin does)."""
    k, a, b = (np.array(head(n + "_" + s)) for n in ("calf", "foot", "ball"))
    return [k, a, b, b + (b - a) / np.linalg.norm(b - a) * 0.06]


def to_chain(p, pts):
    best, bd = None, 1e9
    for a, b in zip(pts[:-1], pts[1:]):
        ab = b - a
        t = max(0.0, min(1.0, float((p - a) @ ab / (ab @ ab))))
        q = a + ab * t
        d = float(np.linalg.norm(p - q))
        if d < bd:
            best, bd = q, d
    return best


CHAIN = {s: chain(s) for s in "lr"}
visible = []
for f in polys:
    P = S0[list(f)]
    c = Vector(tuple(P.mean(0)))
    n = Vector(tuple(np.cross(P[1] - P[0], P[2] - P[0])))
    if len(f) == 4:
        n = Vector(tuple(np.cross(P[2] - P[0], P[3] - P[1])))
    if n.length < 1e-12:
        visible.append(False)
        continue
    n.normalize()
    q = to_chain(np.array(c), CHAIN["l" if c.x > 0 else "r"])
    if n.dot(c - Vector(tuple(q))) <= 0:
        visible.append(False)            # it faces the foot's middle: the lining, the inner sole, the collar's turn-in
        continue
    seen = False
    for k in range(8):
        d = n if k == 0 else (n + Vector(tuple(rng.normal(size=3))) * 0.6).normalized()
        if d.dot(n) < 0.1:
            continue
        if bvh_s0.ray_cast(c + d * 1e-5, d, 2.0)[0] is None:
            seen = True
            break
    visible.append(seen)
visible = np.array(visible)
# samples: every point (visible if any of its faces is) and every face's middle
pt_vis = np.zeros(len(S0), bool)
for f, v in zip(polys, visible):
    if v:
        pt_vis[list(f)] = True
side_pt = np.where(S0[:, 0] > 0, "l", "r")
rep = {"blend": BLEND, "pair": PAIR, "depthMm": DEPTH * 1000, "points": len(S0), "faces": len(polys),
       "visibleFaces": int(visible.sum()), "visibleFacesBySlot": {m: int(sum(1 for pm, v in zip(pmat, visible) if v and pm == m)) for m in mats},
       "poses": {}}
bm = bmesh.new()
bm.from_mesh(me)
E = np.array([[e.verts[0].index, e.verts[1].index] for e in bm.edges])
bm.free()
L0 = np.linalg.norm(S0[E[:, 0]] - S0[E[:, 1]], axis=1)
floor_sole = float(S0[:, 2].min())
top_rest = {s: float(S0[side_pt == s][:, 2].max()) for s in "lr"}

if jeans is not None:
    J0, JT = evaluated(jeans)
    jb = bmesh.new()
    jb.from_mesh(jeans.data)
    loops, seen_v = [], set()
    bnd = {v.index for e in jb.edges if e.is_boundary for v in e.verts}
    adj = {i: [] for i in bnd}
    for e in jb.edges:
        if e.is_boundary:
            a, b = e.verts[0].index, e.verts[1].index
            adj[a].append(b)
            adj[b].append(a)
    for s0 in bnd:
        if s0 in seen_v:
            continue
        ring, st = [], [s0]
        while st:
            a = st.pop()
            if a in seen_v:
                continue
            seen_v.add(a)
            ring.append(a)
            st += adj[a]
        loops.append(ring)
    jb.free()
    hems = {}
    for ring in loops:
        zc = J0[ring][:, 2].mean()
        if zc < 0.3:
            hems["l" if J0[ring][:, 0].mean() > 0 else "r"] = np.array(ring)
    rep["jeans"] = {"fbx": JEANS, "points": len(J0), "hemPoints": {s: int(len(h)) for s, h in hems.items()},
                    "hemRestZ": {s: [round(float(J0[h][:, 2].min()), 4), round(float(J0[h][:, 2].max()), 4)] for s, h in hems.items()}}

POSES = ("rest", "walking", "sitting", "stair", "toe bend")
for name in POSES:
    pose(name)
    S1, _ = evaluated(pair)
    B1, _ = evaluated(body)
    bvh_b = BVHTree.FromPolygons([tuple(v) for v in B1], BT)
    bvh_s = BVHTree.FromPolygons([tuple(v) for v in S1], ST)
    r = {}
    # heights read in each foot's own frame (rest), so a lifted foot's are still on its boot
    FM = {}
    for s in "lr":
        p_ = pb["foot_" + s]
        FM[s] = np.array((arm.matrix_world @ p_.matrix @ p_.bone.matrix_local.inverted() @ arm.matrix_world.inverted()).inverted())

    def rest_z(s, p):
        return float(FM[s][2, :3] @ p + FM[s][2, 3])

    vslot = [""] * len(S1)
    for f, m in zip(polys, pmat):
        for i in f:
            vslot[i] = m
    samples = [(S1[i], pt_vis[i], side_pt[i], "point " + vslot[i]) for i in range(len(S1))]
    samples += [(S1[list(f)].mean(0), v, side_pt[f[0]], "face " + m) for f, v, m in zip(polys, visible, pmat)]
    for s in "lr":
        thr, thr_w, thr_z, hid, hid_w, where = 0, 0.0, [], 0, 0.0, []
        k_, a_ = np.array(head("calf_" + s)), np.array(head("foot_" + s))
        ax_ = (k_ - a_) / np.linalg.norm(k_ - a_)
        fw_ = np.array(head("ball_" + s) - head("foot_" + s))
        fw_ -= ax_ * (fw_ @ ax_)
        fw_ /= np.linalg.norm(fw_)
        for p, vis, sd, kind in samples:
            if sd != s:
                continue
            q = Vector(tuple(p))
            d = depth_in(bvh_b, q)
            if d <= DEPTH:
                continue
            if not inside(bvh_b, q):
                continue
            if vis:
                thr += 1
                thr_w = max(thr_w, d)
                thr_z.append(rest_z(s, p) - floor_sole)
                rad = (p - a_) - ax_ * ((p - a_) @ ax_)
                ang = math.degrees(math.atan2(float(np.cross(fw_, rad) @ ax_), float(rad @ fw_)))
                where.append((round(d * 1000, 1), kind, round(thr_z[-1] * 1000), round(ang)))
            else:
                hid += 1
                hid_w = max(hid_w, d)
        r[s] = {"throughVisible": thr, "throughVisibleWorstMm": round(thr_w * 1000, 1),
                "throughHeightAboveSoleMm": [round(min(thr_z) * 1000, 1), round(max(thr_z) * 1000, 1)] if thr_z else None,
                "hiddenInside": hid, "hiddenInsideWorstMm": round(hid_w * 1000, 1),
                "throughWorstPlaces_depthMm_kind_heightMm_angleDeg(0 toes-ward)": sorted(where, reverse=True)[:6]}
    L1 = np.linalg.norm(S1[E[:, 0]] - S1[E[:, 1]], axis=1)
    ratio = L1 / np.maximum(L0, 1e-9)
    r["stretch"] = {"worst": round(float(ratio[np.argmax(np.abs(np.log(ratio)))]), 3),
                    "p99": round(float(np.percentile(ratio, 99)), 3), "p1": round(float(np.percentile(ratio, 1)), 3)}
    if jeans is not None:
        J1, _ = evaluated(jeans)
        bvh_j = BVHTree.FromPolygons([tuple(v) for v in J1], JT)
        jr = {}
        for s in "lr":
            a0, a1 = np.array(head("calf_" + s)), np.array(head("foot_" + s))
            ax = (a0 - a1) / np.linalg.norm(a0 - a1)

            def to_axis(p):
                v = p - a1
                foot_pt = a1 + ax * (v @ ax)
                return foot_pt - p

            ids = np.where(side_pt == s)[0]
            n_all, n_vis, worst = 0, 0, 0.0
            for i in ids:
                p = S1[i]
                t = to_axis(p)
                L = float(np.linalg.norm(t))
                if L < 1e-6:
                    continue
                # (the cloth within 40 mm of the point: farther, the ray has only crossed the hem on its way)
                hit = bvh_j.ray_cast(Vector(tuple(p)), Vector(tuple(t / L)), min(L, 0.04))
                if hit[0] is not None and hit[3] > DEPTH:
                    n_all += 1
                    n_vis += int(pt_vis[i])
                    worst = max(worst, hit[3])
            h = hems.get(s)
            hem = {}
            if h is not None:
                H = J1[h]
                foot_fwd = np.array(head("ball_" + s) - head("foot_" + s))
                foot_fwd[2] = 0
                foot_fwd /= np.linalg.norm(foot_fwd)
                v2 = (H - H.mean(0))[:, :2]
                ang = np.degrees(np.arctan2(foot_fwd[0] * v2[:, 1] - foot_fwd[1] * v2[:, 0], v2 @ foot_fwd[:2]))
                parts = {"front": np.abs(ang) < 45, "back": np.abs(ang) > 135, "sides": (np.abs(ang) >= 45) & (np.abs(ang) <= 135)}
                ins, ins_w = 0, 0.0
                for pnt in H:
                    # out from the shin's axis: any of the boot met within 60 mm means the hem lies in it (in the
                    # leather or in the shaft), the last face met is where it would come out
                    t = -to_axis(pnt)
                    L = float(np.linalg.norm(t))
                    if L < 1e-6:
                        continue
                    d_ = Vector(tuple(t / L))
                    o_ = Vector(tuple(pnt))
                    tt, last = 0.0, None
                    for _ in range(20):
                        hit = bvh_s.ray_cast(o_ + d_ * (tt + 1e-6), d_, 0.06 - tt)
                        if hit[0] is None:
                            break
                        tt = (hit[0] - o_).length
                        last = tt
                    if last is not None and last > DEPTH:
                        ins += 1
                        ins_w = max(ins_w, last)
                Hz = np.array([rest_z(s, q) for q in H]) - floor_sole
                hem = {k: [round(float(Hz[m].min()) * 1000, 1), round(float(np.median(Hz[m])) * 1000, 1),
                           round(float(Hz[m].max()) * 1000, 1)] for k, m in parts.items() if m.any()}
                hem["hemPointsInsideBoot"] = ins
                hem["hemInsideBootWorstMm"] = round(ins_w * 1000, 1)
                hem["bootTopAboveSoleMm"] = round(top_rest[s] * 1000 - floor_sole * 1000, 1)
            jr[s] = {"bootPointsThroughJeans": n_all, "visibleBootPointsThroughJeans": n_vis,
                     "throughJeansWorstMm": round(worst * 1000, 1), "hemAboveSoleFloorMm_minMedianMax": hem}
        r["jeans"] = jr
    rep["poses"][name] = r
    print("FOOTPOSE", name, json.dumps(r), flush=True)
    if RENDER:
        os.makedirs(RENDER, exist_ok=True)
        sc = bpy.context.scene
        sc.render.engine = "BLENDER_WORKBENCH"
        sc.display.shading.light = "STUDIO"
        sc.display.shading.color_type = "MATERIAL"
        sc.display.shading.show_specular_highlight = False
        sc.render.resolution_x, sc.render.resolution_y = 900, 700
        if "in_shoe" not in body.vertex_groups:
            g = body.vertex_groups.new(name="in_shoe")
            hide = [i for i in range(len(B0)) if B0[i, 2] < min(top_rest.values()) - 0.03 and abs(B0[i, 0]) > 0.02]
            g.add(hide, 1.0, "REPLACE")
            mk = body.modifiers.new("hide", "MASK")
            mk.vertex_group = "in_shoe"
            mk.invert_vertex_group = True
            mk.show_viewport = False         # the counts read the whole body; only the pictures hide the feet
        grey = bpy.data.materials.get("M_BodyGrey") or bpy.data.materials.new("M_BodyGrey")
        grey.diffuse_color = (0.5, 0.5, 0.5, 1)
        body.data.materials.clear()
        body.data.materials.append(grey)
        cam = bpy.data.objects.get("cam") or bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
        if cam.name not in sc.collection.objects:
            sc.collection.objects.link(cam)
        sc.camera = cam
        cam.data.lens = 50
        c = Vector(tuple(S1.mean(0)))
        c.z = float(S1[:, 2].min()) + 0.07
        for view, d in (("three-quarter", Vector((0.65, -0.65, 0.3))), ("side", Vector((1, 0.0, 0.08))), ("back", Vector((0.0, 1, 0.25)))):
            cam.location = c + d.normalized() * 0.95
            cam.rotation_euler = (c - cam.location).to_track_quat("-Z", "Y").to_euler()
            sc.render.filepath = os.path.join(RENDER, "%s-%s.png" % (name.replace(" ", "-"), view))
            bpy.ops.render.render(write_still=True)
reset()
json.dump(rep, open(OUT, "w"), indent=1)
print("FOOTPOSE written", OUT, flush=True)
