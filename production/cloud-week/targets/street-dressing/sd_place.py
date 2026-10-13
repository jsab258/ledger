"""sd_place: the shared placement check of the street-dressing targets (cloud week 42, unit 13, after the fresh review).

Why it exists: the first version's placement rows only tested each target's own numbers (a stallriser line minus a
depth), so no row could fail on a neighbour. The review found an awning, a shop door, a litter bin, a carriageway and a
missing floor that every such row passed. This module puts a family's pieces into the street's own frame, from the
family's BUILT PARTS and a stated pose, and tests them against the street's own pieces and rulings:

  * the zone it says it stands on (footway, carriageway, quay apron, yard floor), its ground level, whether that ground
    is modelled in the scene (the yard mouth is not: "a gap in the data", vignette-scene.json west_north note);
  * every piece of production/specs/vignette-pieces.json (kerbs, ground planes, decals and litter left out; the shop
    awnings replaced by their measured sloping sheet and valance), with the piece's height, within a clearance;
  * the shop and side door zones of the shopfronts target (door slot plus a 0.9 m approach in front of it);
  * the walking strip: a person is 0.68 m wide and 2.0 m tall, so the widest free width between the kerb's back edge and
    the frontage, over every height from the footway to 2.0 m, must stay 0.68 m along the whole piece (an awning's
    valance, a bin, a lid, a bracket all narrow it; the head-height strip is the same test at 1.6 to 2.0 m);
  * the carriageway: a pose in the road leaves a lane at least 2.8 m wide;
  * its front: the direction the pose turns the piece's front (-y) to matches the direction the target states.

Frame of a pose: the piece's own frame is millimetres, front -y, pivot the base's centre on the ground. A pose is
{x_m, z_m, yaw_deg}: street x = x_m + (xl cos yaw - yl sin yaw) / 1000, street z = z_m + (xl sin yaw + yl cos yaw) / 1000;
yaw 0 puts the piece's front towards street -z (the road, from the east side). The street's frame is the scene's: x along
the street, z across it (+z east), y up from the road's crown (metres).
"""
import copy
import json
import math
import os
import re
import sys

import numpy as np
from shapely import affinity
from shapely.geometry import MultiPoint, Point, Polygon, box as sbox
from shapely.ops import unary_union

import sd_lib as L

PIECES_REL = "production/specs/vignette-pieces.json"
SCENE_REL = "production/specs/vignette-scene.json"
SHOPS_REL = "production/cloud-week/targets/shopfronts/target.json"
DOORS_REL = "production/cloud-week/targets/front-doors-all/target.json"
QUAY_REL = "tools/art-recipes/south-quay"

WALKER_W_M = 0.68          # the walking person's width (RULINGS-era tester finding of 29 September)
WALKER_H_M = 2.0           # the corridor a walker needs is this tall
HEAD_LOW_M = 1.6           # the head-height strip starts here
LANE_MIN_M = 2.8           # least a bus needs
CLEARANCE_M = 0.05         # nothing of a piece within this of a street piece, unless the pose says it leans there
APPROACH_M = 0.9           # the approach in front of a door that nothing may stand in
DOOR_SLOT_M = {"shop_door": 1.006, "side_door": 0.944}
FOOTWAY_Z = (3.125, 5.125)  # east footway, back edge of the kerb to the frontage (west is the mirror)
CARRIAGEWAY_Z = (-3.0, 3.0)
STREET_X = (0.0, 48.0)
CROWN_ABOVE_CHANNEL_M = 0.075
FOOTWAY_CROSSFALL = 0.025

SKIP_BOM_PREFIX = ("A0_", "A5_", "A7_", "A8_", "B1_", "B2_", "B3_", "G")
AWNING_ASSET = "awning_02"

_cache = {}


def repo():
    return L.REPO


# ------------------------------------------------------------------------------------------------ the ground
def ground_y(x, z, zone=None):
    """Height of the ground above the road's crown (metres) at street (x, z)."""
    a = abs(z)
    if a <= 3.0:
        return -0.025 * a
    if a <= 3.125:
        return -0.025 * 3.0 + 0.125
    if a <= 5.125 + 1e-9:
        return 0.05 + FOOTWAY_CROSSFALL * (a - 3.125)
    return 0.10


ZONES = {
    "east_footway": sbox(STREET_X[0], FOOTWAY_Z[0], STREET_X[1], FOOTWAY_Z[1]),
    "west_footway": sbox(STREET_X[0], -FOOTWAY_Z[1], STREET_X[1], -FOOTWAY_Z[0]),
    "west_carriageway": sbox(STREET_X[0], -3.0, STREET_X[1], 0.0),
    "east_carriageway": sbox(STREET_X[0], 0.0, STREET_X[1], 3.0),
}


def footway_of(zone):
    return {"east_footway": 1, "west_footway": -1}.get(zone)


# ------------------------------------------------------------------------------------------------ the scene's own pieces
class Obs:
    __slots__ = ("name", "bom", "poly", "y0", "y1", "kind")

    def __init__(self, name, bom, poly, y0, y1, kind="piece"):
        self.name, self.bom, self.poly, self.y0, self.y1, self.kind = name, bom, poly, y0, y1, kind


def _rect(cx, cz, sx, sz, yaw):
    r = sbox(cx - sx / 2.0, cz - sz / 2.0, cx + sx / 2.0, cz + sz / 2.0)
    return affinity.rotate(r, yaw, origin=(cx, cz)) if abs(yaw) > 1e-6 else r


def _awning_slices(x, ytop_wall, wall_z, side, width=3.0):
    """The measured awning_02 as thin plates: the canopy is one sloping sheet from the wall (top 0.005 above the piece's
    origin) to 1.729 out, falling 1.003; the valance hangs 0.32 below the canopy's front edge (scalloped, 1.318 below the
    origin at the lowest). Read from ledger/Assets/Props/base-mesh/awning_02.glb's POSITION accessor (the review of
    13 October measured 0.995 over 1.577; the mesh has no vertex between 0 and 1.729, so the sheet is one plane)."""
    out = []
    n = 48
    out_dir = -side        # the awning hangs from the wall towards the street (east wall at +z: street is -z)
    for i in range(n):
        d0 = 1.729 * i / n
        d1 = 1.729 * (i + 1) / n
        y_top0 = ytop_wall + 0.005 - 1.003 * (d0 / 1.729)
        y_top1 = ytop_wall + 0.005 - 1.003 * (d1 / 1.729)
        za, zb = wall_z + out_dir * d0, wall_z + out_dir * d1
        poly = sbox(x - width / 2, min(za, zb), x + width / 2, max(za, zb))
        out.append(Obs("awning canopy %d" % i, "E18_shop_awnings", poly, min(y_top0, y_top1) - 0.02, max(y_top0, y_top1), "awning"))
    zv = wall_z + out_dir * 1.735
    zv2 = wall_z + out_dir * 1.729
    out.append(Obs("awning valance", "E18_shop_awnings", sbox(x - width / 2, min(zv, zv2), x + width / 2, max(zv, zv2)),
                   ytop_wall + 0.005 - 1.318 + 0.0, ytop_wall + 0.005 - 0.995, "awning"))
    return out


def scene():
    """The street's own pieces as obstacles, the door zones and the wall table."""
    if "scene" in _cache:
        return _cache["scene"]
    root = repo()
    d = json.load(open(os.path.join(root, PIECES_REL)))
    obs = []
    awn = []
    for p in d["pieces"]:
        bom = p["bom"]
        if bom.startswith(SKIP_BOM_PREFIX) or p["shape"] == "decal":
            continue
        cx, cy, cz = p["x_m"], p["y_m"], p["z_m"]
        sx, sy, sz = p["sx_m"], p["sy_m"], p["sz_m"]
        if p.get("asset") == AWNING_ASSET:
            side = 1 if cz > 0 else -1
            awn += _awning_slices(cx, cy + sy / 2.0 - 0.005, (5.125 * side), side, width=sx)
            continue
        pit, rol, yaw = p["pitch_deg"], p["roll_deg"], p["yaw_deg"]
        if p["shape"] == "cyl":
            if abs(rol) > 80 and abs(rol) < 100:         # laid along the street
                poly = sbox(cx - sy / 2.0, cz - sz / 2.0, cx + sy / 2.0, cz + sz / 2.0)
                h = sx
            elif abs(pit) > 80 and abs(pit) < 100:       # axis along z
                poly = sbox(cx - sx / 2.0, cz - sy / 2.0, cx + sx / 2.0, cz + sy / 2.0)
                h = sz
            elif abs(pit) > 1 or abs(rol) > 1:           # a tilted neck: a conservative disc
                r = sy / 2.0 + sx / 2.0
                poly = Point(cx, cz).buffer(r)
                h = 2 * r
            else:
                poly = Point(cx, cz).buffer(sx / 2.0, 16)
                h = sy
        else:
            if abs(pit) > 1.5 or abs(rol) > 1.5:         # a roof plane: conservative axis box of the tilted slab
                ext = abs(sy * math.sin(math.radians(pit))) + abs(sz * math.cos(math.radians(pit)))
                poly = sbox(cx - sx / 2.0, cz - ext / 2.0, cx + sx / 2.0, cz + ext / 2.0)
                h = abs(sy * math.cos(math.radians(pit))) + abs(sz * math.sin(math.radians(pit)))
            else:
                poly = _rect(cx, cz, sx, sz, yaw)
                h = sy
        obs.append(Obs(p["name"], bom, poly, cy - h / 2.0, cy + h / 2.0))
    obs += awn
    # door zones from the shopfronts target (the slot, not the scene's stand-in door) and the houses' doors
    doors = []
    sh = json.load(open(os.path.join(root, SHOPS_REL)))
    for s in sh["shops"]:
        side = 1 if s["side"] == "east" else -1
        for kind in ("shop_door", "side_door"):
            c = s["centres_street_x_m"].get(kind)
            if c is None:
                continue
            w = DOOR_SLOT_M[kind]
            doors.append({"id": "%s/%s" % (s["id"], kind), "kind": kind, "side": side, "x0": c - w / 2.0, "x1": c + w / 2.0,
                          "source": "shopfronts target shops[%s].centres_street_x_m.%s (slot %.3f m)" % (s["id"], kind, w)})
    p = os.path.join(root, DOORS_REL)
    if os.path.exists(p):
        try:
            for dd in houses_doors(json.load(open(p))):
                doors.append(dd)
        except Exception:
            pass
    sc = json.load(open(os.path.join(root, SCENE_REL)))
    walls = []
    for b in sc["blocks"]:
        side = 1 if b["side"] == "east" else -1
        st = (b.get("drawn") or {}).get("storey_heights_m") or b["storey_heights_m"]
        walls.append({"id": b["id"], "side": side, "x0": b["start_x_m"], "x1": b["start_x_m"] + b["bays"] * b["bay_width_m"],
                      "eaves_m": 0.1 + sum(st), "storeys_drawn": len(st), "wall_z": 5.125 * side,
                      "shopfront": b.get("ground_floor") == "shopfront" or b["id"] == "west_north"})
    res = {"obs": obs, "doors": doors, "walls": walls, "pieces_file": PIECES_REL, "n_pieces": len(d["pieces"])}
    _cache["scene"] = res
    return res


def houses_doors(T):
    """Household doors of the front-doors target, when it lists them with street x (west cottages, flats, side doors)."""
    out = []
    for h in T.get("houses", []) if isinstance(T.get("houses"), list) else []:
        x = h.get("street_x_m") or h.get("x_m")
        side = h.get("side")
        if x is None or side not in ("east", "west"):
            continue
        w = h.get("door_width_m", 0.838)
        out.append({"id": "house/%s" % h.get("id"), "kind": "house_door", "side": 1 if side == "east" else -1,
                    "x0": x - w / 2.0, "x1": x + w / 2.0, "source": "front-doors-all target houses[%s]" % h.get("id")})
    return out


def frontage_z(x, side):
    """The line the walking strip ends at: the stallriser face (0.15 proud of the wall) in front of a shopfront, the wall
    itself in front of a plain wall, the footway's back where no building stands."""
    w = walls_at(x, side)
    if w is None:
        return 5.125 * side
    return (4.975 if w.get("shopfront") else 5.125) * side


def walls_at(x, side):
    for w in scene()["walls"]:
        if w["side"] == side and w["x0"] - 1e-9 <= x <= w["x1"] + 1e-9:
            return w
    return None


# ------------------------------------------------------------------------------------------------ a pose into the street
def to_street(pose, xl_mm, yl_mm):
    th = math.radians(pose.get("yaw_deg", 0.0))
    c, s = math.cos(th), math.sin(th)
    return (pose["x_m"] + (xl_mm * c - yl_mm * s) / 1000.0, pose["z_m"] + (xl_mm * s + yl_mm * c) / 1000.0)


def front_direction(pose):
    """The street direction the piece's front (-y) faces, as a unit vector (x, z)."""
    xs, zs = to_street(dict(pose, x_m=0.0, z_m=0.0), 0.0, -1000.0)
    return xs, zs


def direction_name(v):
    x, z = v
    if abs(x) > abs(z):
        return "+x" if x > 0 else "-x"
    return "+z" if z > 0 else "-z"


class Prism:
    __slots__ = ("part", "poly", "y0", "y1")

    def __init__(self, part, poly, y0, y1):
        self.part, self.poly, self.y0, self.y1 = part, poly, y0, y1


def object_prisms(T, pose):
    """The pose's parts in the street frame: one plan polygon per part with its height range above the crown."""
    prisms, base = _prisms_one(T, pose)
    for ex in pose.get("extra_poses", []):
        q, _ = _prisms_one(T, ex)
        prisms = prisms + q
    return prisms, base


_prism_cache = {}


def _prisms_one(T, pose):
    key = L.jhash([L.variant_parts(T, pose.get("variant", T.get("sample"))), {k: v for k, v in pose.items() if k != "extra_poses"}])
    if key not in _prism_cache:
        _prism_cache[key] = _prisms_one_raw(T, pose)
    return _prism_cache[key]


def _prisms_one_raw(T, pose):
    V = pose.get("variant", T.get("sample"))
    parts = L.variant_parts(T, V)
    only = pose.get("parts")
    ps = L.PartSet([p for p in parts if (only is None or p["id"] in only or any(p["id"].startswith(o) for o in only if o.endswith("*")))])
    # the ground under the pivot sets the base; a pose may state it (a yard floor, the quay apron)
    base = pose.get("base_y_m")
    if base is None:
        base = ground_y(pose["x_m"], pose["z_m"])
    out = []
    th = math.radians(pose.get("yaw_deg", 0.0))
    c, s = math.cos(th), math.sin(th)
    for p, pcs in zip(ps.parts, ps.pieces):
        polys = []
        z0 = np.inf
        z1 = -np.inf
        for pc in pcs:
            V3 = pc.V
            xs = pose["x_m"] + (V3[:, 0] * c - V3[:, 1] * s) / 1000.0
            zs = pose["z_m"] + (V3[:, 0] * s + V3[:, 1] * c) / 1000.0
            h = MultiPoint(list(zip(xs, zs))).convex_hull
            if h.geom_type == "Polygon" and h.area > 1e-9:
                polys.append(h)
            elif h.geom_type in ("LineString", "Point"):
                polys.append(h.buffer(0.002))
            z0 = min(z0, V3[:, 2].min())
            z1 = max(z1, V3[:, 2].max())
        if polys:
            out.append(Prism(p["id"], unary_union(polys), base + z0 / 1000.0, base + z1 / 1000.0))
    return out, base


def _is_ignored(part, pose):
    return any(part.startswith(i) for i in pose.get("ignore_parts", []))


# ------------------------------------------------------------------------------------------------ the tests
def separation(a, y0a, y1a, b, y0b, y1b):
    """3D clearance between two prisms: 0 when they overlap."""
    dp = a.distance(b)
    dv = max(0.0, max(y0a, y0b) - min(y1a, y1b))
    return math.hypot(dp, dv)


def collisions(T, pose, margin=CLEARANCE_M, near=2.0):
    prisms, base = object_prisms(T, pose)
    body = [q for q in prisms if not _is_ignored(q.part, pose)]
    if not body:
        return [], base
    u = unary_union([q.poly for q in body])
    area = u.buffer(near)
    leans = pose.get("leans_on", [])
    tol = pose.get("contact_tol_m", 0.03)
    rep = tuple(pose.get("replaces", []))
    hits = []
    for o in scene()["obs"]:
        if not o.poly.intersects(area) or (rep and o.bom.startswith(rep)):
            continue
        shrink = any(re.search(pat, o.name) or re.search(pat, o.bom) for pat in leans)
        for q in body:
            poly = q.poly.buffer(-tol) if shrink and q.poly.area > 4 * tol * tol else q.poly
            if poly.is_empty:
                continue
            sep = separation(poly, q.y0, q.y1, o.poly, o.y0, o.y1)
            lim = 0.0 if shrink else margin
            if sep < lim:
                hits.append((o.name, q.part, round(sep, 3)))
    seen = {}
    for n, part, sp in hits:
        seen.setdefault(n, (part, sp))
    return [(n, v[0], v[1]) for n, v in seen.items()], base


def door_hits(T, pose, approach=APPROACH_M):
    prisms, base = object_prisms(T, pose)
    out = []
    for dz in scene()["doors"]:
        side = dz["side"]
        wall = 5.125 * side
        z0, z1 = sorted((wall, wall - side * (approach + 0.15)))
        zone = sbox(dz["x0"], z0, dz["x1"], z1)
        for q in prisms:
            if _is_ignored(q.part, pose):
                continue
            if q.y0 < base + 2.0 and q.poly.intersects(zone) and q.poly.intersection(zone).area > 1e-6:
                out.append((dz["id"], q.part))
                break
    return out


def free_gap(blocked, lo, hi):
    """Largest free interval inside [lo, hi] given blocked intervals."""
    iv = sorted((max(a, lo), min(b, hi)) for a, b in blocked if b > lo and a < hi)
    best, cur = 0.0, lo
    for a, b in iv:
        if a > cur:
            best = max(best, a - cur)
        cur = max(cur, b)
    best = max(best, hi - cur)
    return best


def _slice_intervals(poly, x):
    line = sbox(x - 1e-6, -50, x + 1e-6, 50)
    inter = poly.intersection(line)
    if inter.is_empty:
        return []
    geoms = [inter] if inter.geom_type == "Polygon" else [g for g in getattr(inter, "geoms", []) if g.geom_type == "Polygon"]
    return [(g.bounds[1], g.bounds[3]) for g in geoms]


def walking_strip(T, pose, zone, with_object=True, pad=0.0, h_lo=None, h_hi=None):
    """Narrowest, over the piece's x range, of the widest free width across the footway at the heights a walker occupies
    (the footway to 2.0 m above it, or the band h_lo to h_hi above it). Returns (width_m, x_at_min, None). The strip runs
    from the kerb's back edge to the frontage line (the stallriser face in front of a shopfront); every piece of the scene
    and every part of the pose that stands in it, at those heights, closes part of it."""
    side = footway_of(zone)
    prisms, base = object_prisms(T, pose)
    body = [q for q in prisms if not _is_ignored(q.part, pose)] if with_object else []
    if not body:
        return None
    xs0 = min(q.poly.bounds[0] for q in body) - pad
    xs1 = max(q.poly.bounds[2] for q in body) + pad
    obs = scene()["obs"]
    rep = tuple(pose.get("replaces", []))
    best = (9.0, None, None)
    for x in np.arange(xs0, xs1 + 1e-9, 0.05):
        z_lo, z_hi = sorted((3.125 * side, frontage_z(x, side)))
        blocked = []
        gl = ground_y(x, (z_lo + z_hi) / 2.0)
        y_lo = gl + (h_lo if h_lo is not None else 0.0)
        y_hi = gl + (h_hi if h_hi is not None else WALKER_H_M)
        for o in obs:
            if o.y1 <= y_lo or o.y0 >= y_hi or (rep and o.bom.startswith(rep)):
                continue
            b = o.poly.bounds
            if x < b[0] - 1e-9 or x > b[2] + 1e-9:
                continue
            blocked += _slice_intervals(o.poly, x)
        for q in body:
            if q.y1 <= y_lo or q.y0 >= y_hi:
                continue
            b = q.poly.bounds
            if x < b[0] - 1e-9 or x > b[2] + 1e-9:
                continue
            blocked += _slice_intervals(q.poly, x)
        g = free_gap(blocked, z_lo, z_hi)
        if g < best[0]:
            best = (g, float(x), None)
    return best


def lane_width(T, pose):
    """Free carriageway width at the piece's x range with the piece in the road (the road is z -3.0 to 3.0)."""
    prisms, base = object_prisms(T, pose)
    body = [q for q in prisms if not _is_ignored(q.part, pose)]
    xs0 = min(q.poly.bounds[0] for q in body)
    xs1 = max(q.poly.bounds[2] for q in body)
    obs = scene()["obs"]
    best = 99.0
    for x in np.arange(xs0, xs1 + 1e-9, 0.1):
        blocked = []
        for q in body:
            if q.y1 <= base or q.y0 >= base + 2.5:
                continue
            b = q.poly.bounds
            if b[0] - 1e-9 <= x <= b[2] + 1e-9:
                blocked += _slice_intervals(q.poly, x)
        for o in obs:
            if o.bom.startswith(("C", "D")) or o.y1 < 0.0 or o.y0 > 2.5:
                continue
            b = o.poly.bounds
            if b[0] - 1e-9 <= x <= b[2] + 1e-9:
                for a, c in _slice_intervals(o.poly, x):
                    if c > -3.0 and a < 3.0:
                        blocked.append((a, c))
        best = min(best, free_gap(blocked, -3.0, 3.0))
    return best


def foot_prisms(T, pose, reach=0.05):
    """The parts that touch the ground (their lowest point within reach of the pose's ground level)."""
    prisms, base = object_prisms(T, pose)
    return [q for q in prisms if q.y0 - base <= reach and not _is_ignored(q.part, pose)], base


_quay = {}


def quay():
    """The south quay kit's surfaces (tools/art-recipes/south-quay/south_quay_geom.py), top faces projected on (x, z)."""
    if "q" in _quay:
        return _quay["q"]
    sys.path.insert(0, os.path.join(repo(), QUAY_REL))
    import south_quay_geom as G
    kit, jn, info = G.build()

    def top(key):
        p = kit.pieces.get(key)
        if not p:
            return Polygon()
        polys = []
        for f in p["faces"]:
            pts = np.array([p["verts"][i] for i in f])
            n = np.zeros(3)
            for i in range(len(pts)):
                a, b = pts[i], pts[(i + 1) % len(pts)]
                n += np.array([(a[1] - b[1]) * (a[2] + b[2]), (a[2] - b[2]) * (a[0] + b[0]), (a[0] - b[0]) * (a[1] + b[1])])
            n /= (np.linalg.norm(n) + 1e-12)
            if n[2] > 0.5:
                poly = Polygon(pts[:, :2])
                if poly.is_valid and poly.area > 1e-6:
                    polys.append(poly)
        return unary_union(polys) if polys else Polygon()

    road_keys = [k for k in kit.pieces if k.startswith("asphalt__road_")]
    foot_keys = [k for k in kit.pieces if k.startswith("paving__footway")]
    furn = []
    for k, p in kit.pieces.items():
        if k.split("__")[0] in ("iron_black", "rope") or "fish" in k or "dustbin" in k or "bollard" in k or "ring" in k or "ladder" in k:
            for f in p["faces"]:
                pts = np.array([p["verts"][i] for i in f])
                furn.append((k, MultiPoint(pts[:, :2].tolist()).convex_hull, float(pts[:, 2].min()), float(pts[:, 2].max())))
    res = {"apron": top("quay_stone__apron_setts"), "roads": unary_union([top(k) for k in road_keys]),
           "footways": unary_union([top(k) for k in foot_keys]), "apron_z": info["apron_z"], "info": {k: info[k] for k in ("apron_z", "water_z", "yard_z")},
           "furniture": furn}
    _quay["q"] = res
    return res


# ------------------------------------------------------------------------------------------------ the rows
def placement_rows(T, rows):
    pl = T.get("placement", {})
    poses = pl.get("poses", [])
    rows.add("placement", "place/poses are declared", bool(poses), "%d poses" % len(poses))
    sc = scene()
    rows.add("placement", "place/the street's pieces were read", sc["n_pieces"] > 500 and len(sc["doors"]) >= 15,
             "%d scene pieces, %d obstacles, %d door zones from %s and %s" % (sc["n_pieces"], len(sc["obs"]), len(sc["doors"]), PIECES_REL, SHOPS_REL))
    for pose in poses:
        pid = pose["id"]
        g = "place/%s" % pid
        zone = pose["zone"]
        prisms, base = object_prisms(T, pose)
        body = [q for q in prisms if not _is_ignored(q.part, pose)]
        # 1. the front
        fd = front_direction(pose)
        want = pose.get("front_faces")
        if want:
            rows.add("placement", "%s/front faces %s" % (g, want), direction_name(fd) == want,
                     "the pose turns the piece's front to %s (vector %.2f, %.2f)" % (direction_name(fd), fd[0], fd[1]))
        # 2. the zone, on the parts that touch the ground
        feet, _ = foot_prisms(T, pose)
        if zone in ZONES:
            ok = all(ZONES[zone].buffer(1e-6).contains(q.poly) for q in feet) and bool(feet)
            rows.add("placement", "%s/feet lie in zone %s" % (g, zone), ok,
                     "%d ground parts; outside: %s" % (len(feet), [q.part for q in feet if not ZONES[zone].buffer(1e-6).contains(q.poly)][:5]))
        elif zone == "quay_apron":
            Q = quay()
            fp = unary_union([q.poly for q in feet]).buffer(pose.get("apron_margin_m", 1.0))
            rows.add("placement", "%s/footprint plus %.1f m lies on the quay apron's setts" % (g, pose.get("apron_margin_m", 1.0)), Q["apron"].contains(fp),
                     "south_quay_geom's apron_setts (x %.1f to %.1f); the piece stands at x %.1f to %.1f, z %.1f to %.1f" % (Q["apron"].bounds[0], Q["apron"].bounds[2], *unary_union([q.poly for q in feet]).bounds[0::2], *unary_union([q.poly for q in feet]).bounds[1::2]))
            on_road = Q["roads"].intersects(fp) or Q["footways"].intersects(fp)
            rows.add("placement", "%s/footprint plus the margin touches no quay road or footway" % g, not on_road, "roads or footways of south_quay_geom within %.1f m" % pose.get("apron_margin_m", 1.0))
            near = [(n, round(poly.distance(unary_union([q.poly for q in feet])), 2)) for n, poly, z0, z1 in Q["furniture"] if poly.distance(unary_union([q.poly for q in feet])) < pose.get("apron_margin_m", 1.0)]
            rows.add("placement", "%s/nothing of the quay's furniture within %.1f m" % (g, pose.get("apron_margin_m", 1.0)), not near, str(near[:4]))
            rows.add("placement", "%s/ground level is the apron's (%.2f above the crown)" % (g, Q["apron_z"]), abs(base - Q["apron_z"]) < 0.005, "base %.3f, apron %.3f" % (base, Q["apron_z"]))
        elif zone == "yard_floor":
            owed = pose.get("floor_owed")
            modelled = scene_ground_names(unary_union([q.poly for q in feet]))
            if owed:
                ob = sbox(owed["x"][0], owed["z"][0], owed["x"][1], owed["z"][1])
                inside_owed = all(ob.buffer(1e-6).contains(q.poly) for q in feet)
                rows.add("placement", "%s/every foot lies on a modelled surface or on the floor the slot owes" % g,
                         bool(feet) and all(scene_ground_names(q.poly) or ob.buffer(1e-6).contains(q.poly) for q in feet),
                         "%d feet; the scene models no floor there (%s); owed floor x %s, z %s at %.3f above the crown" % (len(feet), "a gap in the data" if not modelled else "partly modelled", owed["x"], owed["z"], owed["level_m"]))
                rows.add("placement", "%s/the owed floor is stated with a level equal to the footway's back" % g, abs(owed["level_m"] - 0.100) < 0.002 and abs(base - owed["level_m"]) < 0.002,
                         "owed level %.3f, pose base %.3f, footway back 0.100" % (owed["level_m"], base))
            else:
                rows.add("placement", "%s/every foot lies on a modelled surface or on the floor the slot owes" % g,
                         bool(feet) and all(scene_ground_names(q.poly) for q in feet), "no owed floor stated; modelled ground under the feet: %s" % bool(modelled))
        else:
            rows.add("placement", "%s/zone %s is known" % (g, zone), False, zone)
        # 3. collisions with the street's pieces
        if zone in ZONES:
            hits, _ = collisions(T, pose)
            rows.add("placement", "%s/clear of every street piece within %d mm (%s)" % (g, int(CLEARANCE_M * 1000), "scene pieces within 2 m, wall props and awnings included"), not hits,
                     "hits: %s" % hits[:6] if hits else "no piece of vignette-pieces.json within %d mm of any of its %d parts" % (int(CLEARANCE_M * 1000), len(body)))
            # 4. doors
            if pose.get("door_check", True):
                dh = door_hits(T, pose)
                rows.add("placement", "%s/clear of every shop and house door zone (slot plus %.1f m approach)" % (g, APPROACH_M), not dh,
                         "in front of: %s" % dh[:5] if dh else "no door of the shopfronts target within reach")
        # 5. walking strip or lane
        fw = footway_of(zone)
        if fw and pose.get("walk_check", True):
            w, xm, _ = walking_strip(T, pose, zone)
            rows.add("placement", "%s/walking strip at least %d mm over the whole piece, floor to %.1f m" % (g, int(WALKER_W_M * 1000), WALKER_H_M), w >= WALKER_W_M,
                     "narrowest widest-free-width %.0f mm at x %.2f" % (w * 1000, xm if xm is not None else float("nan")))
            if pose.get("head_check", True):
                wh, xh, _ = walking_strip(T, pose, zone, h_lo=HEAD_LOW_M, h_hi=WALKER_H_M)
                rows.add("placement", "%s/head-height strip (%.1f to %.1f m) at least %d mm" % (g, HEAD_LOW_M, WALKER_H_M, int(WALKER_W_M * 1000)), wh >= WALKER_W_M,
                         "narrowest %.0f mm at x %.2f" % (wh * 1000, xh if xh is not None else float("nan")))
            if "clear_behind_mm" in pose:
                got = pose["clear_behind_mm"]
                rows.add("placement", "%s/the stated clear strip %d mm is measured off the parts" % (g, got), abs(measured_behind(T, pose, zone) * 1000 - got) <= pose.get("clear_tol_mm", 5.0),
                         "measured %.0f mm" % (measured_behind(T, pose, zone) * 1000))
        elif zone in ("west_carriageway", "east_carriageway"):
            lw = lane_width(T, pose)
            rows.add("placement", "%s/the carriageway keeps a lane of at least %d mm" % (g, int(LANE_MIN_M * 1000)), lw >= LANE_MIN_M, "widest free width across the road %.0f mm" % (lw * 1000))
        # 6. wires and anchors (families that carry wires)
        if pose.get("wires"):
            wire_rows(T, pose, rows, g)


def scene_ground_names(poly):
    """Names of the scene's ground pieces (A0) that fully carry a plan polygon, or [] when the ground is not modelled there."""
    root = repo()
    if "ground" not in _cache:
        d = json.load(open(os.path.join(root, PIECES_REL)))
        gp = []
        for p in d["pieces"]:
            if p["bom"] == "A0_ground_planes":
                gp.append((p["name"], sbox(p["x_m"] - p["sx_m"] / 2, p["z_m"] - p["sz_m"] / 2, p["x_m"] + p["sx_m"] / 2, p["z_m"] + p["sz_m"] / 2)))
        _cache["ground"] = gp
    u = unary_union([g for n, g in _cache["ground"]])
    return [n for n, g in _cache["ground"] if g.intersects(poly)] if u.buffer(1e-6).contains(poly) else []


def measured_behind(T, pose, zone, exclude=None):
    """Free width between the piece's wall-side face and the stallriser line, at the piece's widest (metres). Parts named in
    the pose's measure_exclude (a handle that stands proud) are left out, as the target's own overall depth leaves them out."""
    ex = exclude if exclude is not None else pose.get("measure_exclude", [])
    prisms, base = object_prisms(T, pose)
    body = [q for q in prisms if not _is_ignored(q.part, pose) and not any(q.part.startswith(e) for e in ex)]
    u = unary_union([q.poly for q in body])
    side = footway_of(zone)
    b = u.bounds
    wall = frontage_z(0.5 * (b[0] + b[2]), side)
    return (wall - b[3]) if side > 0 else (b[1] - wall)


def wire_rows(T, pose, rows, g):
    """Wires and anchors: every anchor lies on a modelled wall below its eaves; every wire clears every other piece."""
    cfg = pose["wires"]
    prisms, base = object_prisms(T, pose)
    byname = {q.part: q for q in prisms}
    bad = []
    for a in cfg["anchors"]:
        q = byname.get(a["part"])
        if q is None:
            bad.append((a["part"], "part missing"))
            continue
        cx, cz = q.poly.centroid.x, q.poly.centroid.y
        side = 1 if cz > 0 else -1
        w = walls_at(cx, side)
        top = q.y1
        if w is None:
            bad.append((a["part"], "no wall at x %.2f on that side" % cx))
        elif abs(abs(cz) - 5.125) > 0.15:
            bad.append((a["part"], "z %.2f is not on the frontage line" % cz))
        elif top > w["eaves_m"] - cfg.get("under_eaves_min_m", 0.1):
            bad.append((a["part"], "top %.2f m is above the eaves %.2f m of %s" % (top, w["eaves_m"], w["id"])))
    rows.add("placement", "%s/every anchor lies on a modelled wall below its eaves (drawn storeys)" % g, not bad, "bad: %s" % bad[:5] if bad else "%d anchors, each on the frontage of a drawn row, under its eaves" % len(cfg["anchors"]))
    # wires clear the scene's pieces (the walls they land on excepted)
    skip_names = set()
    for a in cfg["anchors"]:
        w = walls_at(byname[a["part"]].poly.centroid.x, 1 if byname[a["part"]].poly.centroid.y > 0 else -1) if a["part"] in byname else None
        if w:
            skip_names.add(w["id"])
    close = []
    for q in prisms:
        if not any(q.part.startswith(wp) for wp in cfg["wire_parts"]):
            continue
        for o in scene()["obs"]:
            if o.bom.startswith("C1_") or any(o.name.startswith(s) for s in skip_names):
                continue
            sep = separation(q.poly, q.y0, q.y1, o.poly, o.y0, o.y1)
            if sep < cfg.get("wire_clear_m", 0.5):
                close.append((q.part, o.name, round(sep, 2)))
    rows.add("placement", "%s/wires clear every street piece by %.1f m (their own walls excepted)" % (g, cfg.get("wire_clear_m", 0.5)), not close, "close: %s" % close[:5] if close else "none within %.1f m" % cfg.get("wire_clear_m", 0.5))
    lo = min(q.y0 for q in prisms if any(q.part.startswith(wp) for wp in cfg["wire_parts"]) and q.poly.bounds[1] < 3.0 and q.poly.bounds[3] > -3.0) if cfg.get("over_road_min_m") else None
    if lo is not None:
        rows.add("placement", "%s/wires over the road stay at least %.1f m above it" % (g, cfg["over_road_min_m"]), lo >= cfg["over_road_min_m"], "lowest wire part over the road %.2f m above the crown" % lo)


# ------------------------------------------------------------------------------------------------ controls
def pose_by_id(T, pid):
    return next(p for p in T["placement"]["poses"] if p["id"] == pid)


def set_pose(T, pid, **kw):
    p = pose_by_id(T, pid)
    for k, v in kw.items():
        p[k] = v


def ctl(name, pid, prefix, **kw):
    return (name, (lambda t: set_pose(t, pid, **kw)), prefix)


def ctl_copies_across(name, pid, prefix, step=0.5):
    """A fence of copies of the piece across the whole footway at the same x: no gap can be left."""
    def mut(t):
        base = pose_by_id(t, pid)
        poses = []
        east = base["z_m"] > 0
        z = 3.2 if east else -5.1
        zend = 5.1 if east else -3.2
        i = 0
        while z < zend:
            p = {k: v for k, v in base.items() if k not in ("extra_poses", "id", "clear_behind_mm")}
            p["z_m"] = z
            poses.append(p)
            z += step
            i += 1
        base["extra_poses"] = poses
    return (name, mut, prefix)
