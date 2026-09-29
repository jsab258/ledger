"""A MetaHuman body's measurements as FreeSewing asks for them (mm; the slope in degrees), taken off its exported mesh.

    blender -b -P tools/meshgen/blender/body_measurements.py -- BODY.fbx OUT.json

WHY, 29 September (Jafar's list, item 5, the pattern route:
production/research/clothing-pipeline/pattern-jacket-2026-09-29.md). A jacket
cut from FreeSewing's Brian block is drafted to the wearer's measurements:
biceps, chest, hpsToBust, hpsToWaistBack, neck, shoulderToShoulder,
shoulderSlope, shoulderToWrist, waistToArmpit, waistToHips and wrist
(Simon's collar adds nothing more). They are taken as a tape takes them: a girth is the length round the
convex outline of a slice through the body (a tape bridges the hollows), a
length a straight line between two landmarks found from the skeleton. The
slices are taken off the torso alone (the arms hang clear in the rest pose)
and, for the biceps, across the upper arm square to its bone.

Landmarks (the MetaHuman skeleton's joints, in the body's own rest pose):
  chest  the fullest girth between the armpits and 12 cm below them
  waist  the girth at the spine_02 joint, where a man's trouser waist sits
  hips   the fullest girth from the waist down to the crotch
  neck   the girth just under the body mesh's top edge, where the head joins
  HPS    the high point of the shoulder: the top of the body beside the
         neck, at the neck's radius out from its centre
  shoulder point  the top of the body above each upperarm joint
  bust point      the most forward point of the chest slice on one side
"""
import json
import math
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
BODY, OUT = argv[0], argv[1]

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=BODY)
arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
body = max((o for o in bpy.context.scene.objects if o.type == "MESH"), key=lambda o: len(o.data.vertices))
names = {g.index: g.name for g in body.vertex_groups}
W = body.matrix_world
pts = []
for v in body.data.vertices:
    best, w = "", 0.0
    for g in v.groups:
        if g.weight > w:
            best, w = names.get(g.group, ""), g.weight
    pts.append((W @ v.co, best))


def joint(name):
    return arm.matrix_world @ arm.data.bones[name].head_local


ARM_BONES = ("upperarm", "lowerarm", "hand", "thumb", "index", "middle", "ring", "pinky", "clavicle", "wrist", "elbow")
# THE TORSO ALONE: by the bones that move each point, and, below the
# shoulders, inside the shoulders' width too (in the rest pose the hands hang
# beside the hips, and a wrist bone's points are not all named for an arm).


def hull(xy):
    xy = sorted(set((round(a, 5), round(b, 5)) for a, b in xy))
    if len(xy) < 3:
        return xy

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for q in xy:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(xy):
        while len(up) >= 2 and cross(up[-2], up[-1], q) <= 0:
            up.pop()
        up.append(q)
    return lo[:-1] + up[:-1]


def perimeter(poly):
    return sum(math.dist(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))) if len(poly) > 2 else 0.0


def girth_at(z, points, band=0.006):
    sl = [(p.x, p.y) for p in points if abs(p.z - z) < band]
    return perimeter(hull(sl)), sl


pelvis, spine2, neck, head = joint("pelvis"), joint("spine_02"), joint("neck_01"), joint("head")
up_l, up_r, low_l = joint("upperarm_l"), joint("upperarm_r"), joint("lowerarm_l")
SHOULDER_X = abs(up_l.x)
torso = [p for p, b in pts if not b.startswith(ARM_BONES) and (p.z > up_l.z - 0.05 or abs(p.x) < SHOULDER_X)]
thigh_l = joint("thigh_l")
# THE ARMPIT, FOUND ON THE BODY (the clothing session, 29 September): the
# highest level at which a ray from the torso's middle out towards the arm
# leaves the torso and meets air before it meets the arm, as a ruler held up
# under the arm finds it. The rule it replaces, 9 cm below the arm's joint,
# put Ron's armpit 15 cm under his shoulder (a man's is about 23 to 30): the
# jacket drafted from it had a shirt's 17 cm armhole and a 4 cm sleeve cap,
# and its sleeves fought his arms.
import bmesh
from mathutils.bvhtree import BVHTree
_bm = bmesh.new()
_bm.from_mesh(body.data)
_bm.transform(W)
_bvh = BVHTree.FromBMesh(_bm)


def _air_between(z, y):
    """Along +x at height z and depth y from the middle: is there air between the torso and the arm?"""
    o = Vector((0.0, y, z))
    d = Vector((1.0, 0.0, 0.0))
    hits, t = [], 0.0
    while t < 0.6:
        h = _bvh.ray_cast(o + d * (t + 1e-4), d, 0.6 - t)
        if h[0] is None:
            break
        t = (h[0] - o).x
        hits.append(t)
    # out of the torso, then into the arm more than 5 mm further on
    return len(hits) >= 3 and hits[1] - hits[0] > 0.005


ARMPIT = None
for k in range(0, 300):
    z = up_l.z - 0.02 - k * 0.002
    if all(_air_between(z, up_l.y + dy) for dy in (-0.01, 0.0, 0.01)):
        ARMPIT = z
        break
if ARMPIT is None:
    ARMPIT = up_l.z - 0.09

chest_z, chest = max(((z, girth_at(z, torso)[0]) for z in [ARMPIT - k * 0.01 for k in range(0, 13)]), key=lambda t: t[1])
waist_z = spine2.z
waist = girth_at(waist_z, torso)[0]
# THE SEAT, the fullest girth round the buttocks: searched on down to 10 cm
# under the hip joints (the clothing session, 29 September: stopped at the
# joints it read the girth just under the waist, 12 cm down on Ron)
hips_z, hips = max(((z, girth_at(z, torso)[0]) for z in [waist_z - k * 0.01 for k in range(0, int((waist_z - thigh_l.z + 0.10) * 100) + 1)]), key=lambda t: t[1])
# the body mesh ends at the base of the neck, where the head's mesh joins:
# the neck is measured just under that edge
TOP = max(p.z for p, _ in pts)
neck_z = TOP - 0.012
neck_g, neck_sl = girth_at(neck_z, [p for p, b in pts if abs(p.x) < 0.12])
neck_c = Vector((sum(x for x, _ in neck_sl) / max(1, len(neck_sl)), sum(y for _, y in neck_sl) / max(1, len(neck_sl)), neck_z))
neck_r = neck_g / (2 * math.pi)


def top_near(x, y, r=0.015, pool=torso):
    near = [p for p in pool if abs(p.x - x) < r and abs(p.y - y) < r]
    return max(near, key=lambda p: p.z) if near else None


# the high point of the shoulder: beside the neck, on the side (x>0), a
# little out from the neck's radius
hps = top_near(neck_c.x + neck_r + 0.01, neck_c.y)
all_pts = [p for p, _ in pts]
# THE SHOULDER POINT (the acromion, where a tailor takes shoulder to
# shoulder) sits outside the arm's joint, over the edge of the shoulder: the
# top of the body 3.5 cm further out than the joint (at the joint itself the
# first measure read 37.5 cm, a boy's shoulders)
sp_l = top_near(up_l.x + 0.035 * (1 if up_l.x > 0 else -1), up_l.y, 0.02, all_pts)
sp_r = top_near(up_r.x + 0.035 * (1 if up_r.x > 0 else -1), up_r.y, 0.02, all_pts)
chest_sl = [p for p in torso if abs(p.z - chest_z) < 0.006 and p.x > 0.02]
front_sign = -1.0          # the body faces -Y once imported
bust = min(chest_sl, key=lambda p: front_sign * -1 * p.y) if chest_sl else None
bust = min(chest_sl, key=lambda p: p.y) if chest_sl else None

# the biceps: the upper arm's points in a 1 cm slab square to the bone, halfway
# down it, measured round their outline in that plane
axis = (low_l - up_l).normalized()
mid = up_l + (low_l - up_l) * 0.5     # halfway down the upper arm (at a third it caught the deltoid)
u = axis.orthogonal().normalized()
v2 = axis.cross(u).normalized()
arm_pts = [p for p, b in pts if b.startswith("upperarm") and b.endswith("_l")]
slab = [((p - mid).dot(u), (p - mid).dot(v2)) for p in arm_pts if abs((p - mid).dot(axis)) < 0.006]
biceps = perimeter(hull(slab))

# THE SLEEVE'S TWO (Brian's sleeve needs them; without them it drafted 55 mm
# long): shoulder to wrist, from the shoulder point along the arm's bones to
# the wrist joint; and the wrist's girth, square to the forearm just above it.
hand_l = joint("hand_l")
shoulder_to_wrist = ((sp_l - low_l).length + (low_l - hand_l).length) if sp_l else 0.0
fa = (hand_l - low_l).normalized()
wu = fa.orthogonal().normalized()
wv = fa.cross(wu).normalized()
at_wrist = hand_l - fa * 0.02
fore_pts = [p for p, b in pts if b.startswith(("lowerarm", "wrist", "hand")) and b.endswith("_l")]
wrist = perimeter(hull([((p - at_wrist).dot(wu), (p - at_wrist).dot(wv)) for p in fore_pts if abs((p - at_wrist).dot(fa)) < 0.006]))

# SHOULDER TO SHOULDER AS FREESEWING TAKES IT, round the back (the clothing
# session, 29 September): a tape from one shoulder point over the upper back
# to the other, not the straight line between them (Ron's straight line, 446
# mm, drafted shoulders narrower than a standard man of his chest by 8 cm).
def _over_back(a, b, n=40):
    path = [a]
    for k in range(1, n):
        p = a.lerp(b, k / n)
        h = _bvh.ray_cast(Vector((p.x, p.y + 0.5, p.z)), Vector((0.0, -1.0, 0.0)), 1.0)
        if h[0] is not None:
            path.append(h[0])
    path.append(b)
    pl = [(q.x, q.y) for q in path]
    # a tape bridges the hollows: the outline's back half, round its hull
    hl = hull(pl)
    back = [q for q in hl if q[1] >= min(a.y, b.y) - 0.005]
    back.sort(key=lambda q: q[0])
    return sum(math.dist(back[i], back[i + 1]) for i in range(len(back) - 1)) if len(back) > 1 else (a - b).length


# TROUSERS' MEASUREMENTS (the clothing session, 29 September; CLOTHES.md item
# 4: FreeSewing's Titan and Charlie ask for these), as a tape takes them, off
# the legs, which hang straight in the rest pose:
#   seat           the fullest girth from the waist to the crotch (so, as
#                  "hips" above, which Brian treats as the seat line)
#   seatBack, waistBack   the back half of each girth, side to side
#   crotch         the highest level where nothing lies between the legs
#   crossSeam      from the centre front waist between the legs to the
#                  centre back waist, round the hull of the body's middle
#                  slice (a tape bridges the cleft); crossSeamFront its front
#                  part, to the crotch's lowest point
#   knee           the leg's girth at the knee joint
#   waistToSeat, waistToUpperLeg (the crotch), waistToKnee, waistToFloor, inseam
floor_z = min(p.z for p in all_pts)
legs = [p for p, b in pts if not b.startswith(ARM_BONES)]
crotch_z = None
for k in range(0, 400):
    # a ray from front to back along the middle line: while it meets the
    # body, the torso still joins the legs (the mesh's points are too sparse
    # to test a thin band of them)
    z = waist_z - 0.05 - k * 0.002
    if _bvh.ray_cast(Vector((0.0, -1.0, z)), Vector((0.0, 1.0, 0.0)), 2.0)[0] is None:
        crotch_z = z + 0.002
        break
knee_z = joint("calf_l").z


def back_half(z, band=0.006):
    sl = [(p.x, p.y) for p in legs if abs(p.z - z) < band and abs(p.x) < 0.3]
    h = hull(sl)
    if len(h) < 3:
        return 0.0
    left = max(h, key=lambda q: q[0])
    right = min(h, key=lambda q: q[0])
    side_y = (left[1] + right[1]) / 2
    back = sorted([q for q in h if q[1] >= side_y] + [left, right], key=lambda q: q[0])
    return sum(math.dist(back[i], back[i + 1]) for i in range(len(back) - 1))


mid_slab = [(p.y, p.z) for p in legs if abs(p.x) < 0.006 and crotch_z - 0.03 < p.z < waist_z + 0.005]
cross, cross_front = 0.0, 0.0
if len(mid_slab) > 3:
    h = hull(mid_slab)
    top_front = min((q for q in h if q[1] > waist_z - 0.02), key=lambda q: q[0], default=None)
    top_back = max((q for q in h if q[1] > waist_z - 0.02), key=lambda q: q[0], default=None)
    low = min(h, key=lambda q: q[1])
    if top_front and top_back:
        i0, i1, il = h.index(top_front), h.index(top_back), h.index(low)
        n_h = len(h)

        def run(a, b):
            path = [h[a]]
            i = a
            while i != b:
                i = (i + 1) % n_h
                path.append(h[i])
            return path
        # the hull runs round one way; take the way from front to back that passes the lowest point
        p1 = run(i0, i1)
        if low not in p1:
            p1 = list(reversed(run(i1, i0)))
        cross = sum(math.dist(p1[k], p1[k + 1]) for k in range(len(p1) - 1))
        j = p1.index(low)
        cross_front = sum(math.dist(p1[k], p1[k + 1]) for k in range(j))
knee_sl = [((p.x), (p.y)) for p in legs if abs(p.z - knee_z) < 0.006 and p.x > 0.0]
knee_g = perimeter(hull(knee_sl))

m = lambda metres: round(metres * 1000.0, 1)
out = {
    "body": BODY,
    "measurements": {
        "biceps": m(biceps),
        "chest": m(chest),
        "waist": m(waist),
        "hips": m(hips),
        "neck": m(neck_g),
        "hpsToBust": m((hps - bust).length) if hps and bust else None,
        "hpsToWaistBack": m(hps.z - waist_z) if hps else None,
        "shoulderToShoulder": m(_over_back(sp_r, sp_l)) if sp_l and sp_r else None,
        "shoulderSlope": round(math.degrees(math.atan2(hps.z - sp_l.z, abs(sp_l.x - hps.x))), 1) if hps and sp_l else None,
        "waistToArmpit": m(ARMPIT - waist_z),
        "waistToHips": m(waist_z - hips_z),
        "shoulderToWrist": m(shoulder_to_wrist),
        "wrist": m(wrist),
        "seat": m(hips),
        "seatBack": m(back_half(hips_z)),
        "waistBack": m(back_half(waist_z)),
        "waistToSeat": m(waist_z - hips_z),
        "waistToUpperLeg": m(waist_z - crotch_z) if crotch_z else None,
        "waistToKnee": m(waist_z - knee_z),
        "waistToFloor": m(waist_z - floor_z),
        "inseam": m(crotch_z - floor_z) if crotch_z else None,
        "crossSeam": m(cross),
        "crossSeamFront": m(cross_front),
        "knee": m(knee_g),
    },
    "heights_m": {"chest": round(chest_z, 3), "waist": round(waist_z, 3), "hips": round(hips_z, 3), "neck": round(neck_z, 3),
                  "armpit": round(ARMPIT, 3), "hps": round(hps.z, 3) if hps else None, "top": round(max(p.z for p in all_pts), 3),
                  "crotch": round(crotch_z, 3) if crotch_z else None, "knee": round(knee_z, 3), "floor": round(floor_z, 3)},
}
json.dump(out, open(OUT, "w"), indent=1)
print("MEASURED", json.dumps(out["measurements"]))
