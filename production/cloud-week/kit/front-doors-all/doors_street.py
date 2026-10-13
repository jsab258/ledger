"""The street as data: which door, paint, condition and fittings each house has, and where each fitting stands (cloud week 42, unit 9).

    houses_data(N)       the 12 household doors and the hill's 12 doors, from the target's street order, with every fitting's mount point in the kind's own glb frame
    rules(houses, N)     the neighbour and facing rules of the target (AD rows), computed on any such table
    mix_new_street(N, slots, seed)   a house table for NEW houses (their frame set and whether their windows were modernised), mixed so that the rules hold
    paints_json(N), conditions_json(N)   the 15 paints and the three conditions as materials and a wear parameter set

The target's own table (target.json street.houses) is the authority for today's twelve houses: houses_data() takes it as it is and the check re-runs every rule on the
result. mix_new_street() is the mixer for houses that are not in the table yet (and proves the rules can be met): it picks kind, paint, condition and fittings
from the target's palette and each kind's own set of fittings, deterministically for a seed, so that no two neighbours match.

Mount points: a fitting's .glb has its origin at the fitting's mounting point on the leaf's face; houses.json gives that point in the metres of the kind's .glb
(x across from the door's centre, y into the wall, z up from the ground) and `mirror_x` for a lever that points the other way (scale x by -1).
"""
import itertools
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

SLOTS4 = ("letter_plate", "handle", "latch", "number")


def lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def paint_by_id(N):
    return {p["id"]: p for p in N["paints"]}


def frame_numbers(N, fsid):
    fs = N["frame_sets"][fsid]
    return fs


def leaf_u(N, kind, pl):
    """u of a fitting in the leaf frame (mm): 'leaf centre', 'NN.N from the stop face, right' (a stop 20.4 laps the leaf), or a number."""
    spec = N["kinds"][kind]
    fs = N["frame_sets"][spec["frame_set"][0]]
    lf = spec["leaf"]
    u = pl.get("u")
    if u == "leaf centre":
        return lf["w"] / 2.0
    if isinstance(u, str) and "from the stop face" in u:
        d = float(u.split(" ")[0])
        lap = fs["stop_edges_x"][0] - fs["leaf_x0"]
        return lf["w"] - lap - d if lf["lock_side"] == "right" else lap + d
    return float(u)


GLB_OF = {"NM1:T1": "NM1_stacked"}

# The builder's one adjustment of a placed number: F2's letter plate (LP2, 70 high, v 1545) lies on the 100 high frieze rail between the long panels and the small upper panels;
# the six-panel door's bolections stand 4.8 outside their openings, so the rail shows 1512.5 to 1602.9 and the plate's foot (1510) would lie 2.5 mm on the long panels' lip.
# Moved 5 mm up (1550, inside the row's 8 mm tolerance); the move is written beside the fitting in houses.json.
ADJUST = {("LP2", "F2"): {"v": 5.0, "why": "the plate's foot (v 1510) lies 2.5 mm on the long panels' bolection lip (the rail shows 1512.5 to 1602.9): moved 5 mm up (v 1550, the foot 2.5 mm clear), inside the target's 8 mm tolerance"}}


def mount(N, kind, slot, variant, pl):
    """One fitting's mount point in the target's frame (mm) and in the kind's glb frame (m), its glb name and whether it is mirrored."""
    spec = N["kinds"][kind]
    fsid = spec["frame_set"][0]
    fs = N["frame_sets"][fsid]
    px, py, pz = fs["glb_pivot"]
    X0, Z0, LY0 = fs["leaf_x0"], fs["leaf_z0"], fs["leaf_front_y"]
    lf = spec["leaf"]
    glb = GLB_OF.get("%s:%s" % (variant, kind), variant)
    mirror = False
    if slot == "bell":
        x, y, z = pl["x"], fs["frame_front_y"], 0.5 * (pl["z_range"][0] + pl["z_range"][1])
    elif slot == "scraper":
        x, y, z = -48.0 - 150.0 - 165.0, -60.5, fs["ground_z"]
    else:
        x = X0 + leaf_u(N, kind, pl)
        y = LY0
        v = pl.get("v")
        if slot == "number" and variant == "NM1" and kind == "T1":
            v = 0.5 * (1207.0 + 1373.0)                  # the stacked pair's middle (v 1207 to 1373)
        adj = ADJUST.get((variant, kind))
        if adj and v is not None:
            v = v + adj["v"]
        z = Z0 + v
        if slot == "handle" and variant in ("HD2a", "HD2b", "HD2c"):
            mirror = lf["lock_side"] == "right"          # the lever points toward the door's middle: built pointing +x, which is a left-locking door
    out = {"frame_mm": [round(x, 2), round(y, 2), round(z, 2)], "mount_m": [round((x - px) / 1000.0, 5), round(y / 1000.0, 5), round((z - pz) / 1000.0, 5)],
           "glb": glb, "mirror_x": mirror}
    if ADJUST.get((variant, kind)):
        out["adjusted_from_the_target"] = ADJUST[(variant, kind)]
    return out


def condition_data(N, cond):
    c = N["conditions"][cond]
    keep = {k: c[k] for k in ("paint_flake_share", "paint_fade", "roughness", "crazing", "chips", "bottom_rail", "kick_marks", "polish", "frame")}
    keep["notch_in_bottom_rail"] = cond == "neglected"
    return keep


def house_record(N, h):
    P = paint_by_id(N)
    fr = {f["id"]: f for f in N["frame_colours"]}
    kind = h["kind"]
    fur = []
    for slot, d in h["furniture"].items():
        if not d["place"] or d["variant"].endswith("0"):
            continue
        m = mount(N, kind, slot, d["variant"], d["place"])
        fur.append({"slot": slot, "variant": d["variant"], **m})
    return {"house": h["house"], "side": h["side"], "x_centre_m": h["x_centre_m"], "kind": kind, "frame_set": h["frame_set"], "door_glb": "door_%s.glb" % kind,
            "paint": h["paint"], "paint_srgb": P[h["paint"]]["srgb"], "paint_class": P[h["paint"]]["class"], "frame_colour": h["frame_colour"], "frame_srgb": fr[h["frame_colour"]]["srgb"],
            "condition": h["condition"], "windows_modernised": h["windows_modernised"], "furniture": fur,
            "variants": {slot: d["variant"] for slot, d in h["furniture"].items()}, "why": h["why"]}


def houses_data(N):
    houses = [house_record(N, h) for h in N["street"]["houses"]]
    hill = []
    for d in N["street"]["backdrop"]["doors"]:
        P = paint_by_id(N)[d["paint"]]
        first_cond = [x for x in N["street"]["houses"] if x["kind"] == d["kind"]][0]["condition"]
        glb = "door_%s_kept.glb" % d["kind"] if first_cond == "neglected" else "door_%s.glb" % d["kind"]       # a neglected kind's file carries the eroded notch; the hill's doors are kept
        hill.append({"id": d["id"], "kind": d["kind"], "door_glb": glb, "paint": d["paint"], "paint_srgb": P["srgb"], "paint_class": P["class"],
                     "frame_colour": "white", "condition": "kept", "furniture": [], "note": "seen at 44 m and more: kind and paint only; no fitting, no wear mask beyond the foot band"})
    return {"houses": houses, "hill": hill}


# ------------------------------------------------------------------ the rules (the target's AD rows)
def differ_slots(a, b):
    return sum(1 for s in SLOTS4 if a["variants"].get(s, a.get(s)) != b["variants"].get(s, b.get(s)))


def rules(H, N):
    """The target's street rules on a house table {"houses": [...], "hill": [...]} (houses carry kind, paint, paint_class, variants). Returns [(id, ok, detail)]."""
    rows = []
    byid = {h["house"]: h for h in H["houses"]}
    for side in ("east", "west"):
        order = N["street"]["order"][side]
        bad = []
        for a, b in zip(order[:-1], order[1:]):
            if a not in byid or b not in byid:
                bad.append((a, b, ["a house of the street's order has no door"]))
                continue
            A, B = byid[a], byid[b]
            problems = []
            if A["kind"] == B["kind"]:
                problems.append("kind")
            if A["paint"] == B["paint"]:
                problems.append("paint")
            if A["paint_class"] == B["paint_class"] and A["paint_class"] in ("light", "bright"):
                problems.append("two light or bright doors")
            if differ_slots(A, B) < 2:
                problems.append("fittings differ in %d of 4 slots" % differ_slots(A, B))
            if problems:
                bad.append((a, b, problems))
        rows.append(("AD-adjacent-%s" % side, not bad, bad or "every neighbouring pair differs in kind, paint and at least 2 fittings"))
    bad = []
    for a, b, d in N["street"]["opposite_pairs_within_4_6_m"]:
        if a not in byid or b not in byid:
            bad.append((a, b, "no door"))
        elif byid[a]["paint_class"] == byid[b]["paint_class"]:
            bad.append((a, b, byid[a]["paint_class"]))
    rows.append(("AD-opposite", not bad, bad or "every facing pair within 4.6 m differs in paint class"))
    nl = sum(1 for h in H["houses"] if h["paint_class"] in ("light", "bright"))
    rows.append(("PN-light-doors", nl <= 3, "%d of %d doors are light or bright (at most 3)" % (nl, len(H["houses"]))))
    cond = {c: sum(1 for h in H["houses"] if h["condition"] == c) for c in ("kept", "tired", "neglected")}
    rows.append(("WR-houses", all(v >= 1 for v in cond.values()), cond))
    kinds = sorted({h["kind"] for h in H["houses"]})
    rows.append(("AD-kinds-used", len(kinds) == 10, kinds))
    fs_bad = [h["house"] for h in H["houses"] if (h["house"].startswith("west_south") and h["kind"][0] != "T") or (not h["house"].startswith("west_south") and h["kind"][0] != "F")]
    rows.append(("AD-frame-set", not fs_bad, fs_bad or "cottages take T kinds, every other house F kinds"))
    hb = []
    for row in ("e", "w", "x"):
        ds = [d for d in H["hill"] if d["id"].split("_")[-1].startswith(row)]
        for A, B in zip(ds[:-1], ds[1:]):
            if A["kind"] == B["kind"] or A["paint"] == B["paint"]:
                hb.append((A["id"], B["id"]))
    rows.append(("AD-backdrop", not hb, hb or "no two consecutive doors of a hill row share a kind or a paint"))
    return rows


# ------------------------------------------------------------------ the mixer for new houses
def kind_template(N, kind):
    """The set of fittings a kind carries (from the target's own house table: the first house of the kind): {slot: variant}."""
    h = [x for x in N["street"]["houses"] if x["kind"] == kind][0]
    return {s: d["variant"] for s, d in h["furniture"].items()}


def mix_new_street(N, slots, seed=1, tries=4000):
    """Mix kind, paint, condition and fittings for new houses so that no two neighbours match. `slots`: [{"house", "side", "x_centre_m", "frame_set": "T"|"F",
    "modernised": bool}] in street order per side. Deterministic for a seed. Returns a table like houses_data()['houses'] (the same fields the rules read)."""
    P = paint_by_id(N)
    kinds_of = {"T": ["T1", "T2", "T3"], "F": ["F1", "F2", "F3", "F4", "F5", "F6", "F7"]}
    mod_ok = {"T": ["T3"], "F": ["F5", "F6"]}
    tpl = {k: kind_template(N, k) for k in N["kinds"]}
    sides = {}
    for s in slots:
        sides.setdefault(s["side"], []).append(s)
    for v in sides.values():
        v.sort(key=lambda s: s["x_centre_m"])
    conds = ["kept"] * 5 + ["tired"] * 5 + ["neglected"] * 2
    for attempt in range(tries):
        rng = random.Random(seed * 100003 + attempt)
        table = {}
        ok = True
        cs = list(conds)
        rng.shuffle(cs)
        n_light = 0
        for side, lst in sides.items():
            for i, s in enumerate(lst):
                prev = table.get(lst[i - 1]["house"]) if i else None
                cands = [k for k in kinds_of[s["frame_set"]]]
                if s.get("modernised") and rng.random() < 0.6:
                    cands = mod_ok[s["frame_set"]]
                rng.shuffle(cands)
                pick = None
                for k in cands:
                    if prev and prev["kind"] == k:
                        continue
                    pal = list(P.keys())
                    rng.shuffle(pal)
                    for pid in pal:
                        pc = P[pid]["class"]
                        if prev and (prev["paint"] == pid or (pc in ("light", "bright") and prev["paint_class"] in ("light", "bright"))):
                            continue
                        if pc in ("light", "bright") and n_light >= 3:
                            continue
                        if pc in ("light", "bright", "mid") and rng.random() < 0.7:
                            continue
                        rec = {"house": s["house"], "side": side, "x_centre_m": s["x_centre_m"], "kind": k, "paint": pid, "paint_class": pc,
                               "variants": dict(tpl[k]), "condition": cs[len(table) % len(cs)]}
                        if prev and differ_slots(prev, rec) < 2:
                            continue
                        pick = rec
                        break
                    if pick:
                        break
                if not pick:
                    ok = False
                    break
                if pick["paint_class"] in ("light", "bright"):
                    n_light += 1
                table[s["house"]] = pick
            if not ok:
                break
        if not ok:
            continue
        # facing doors within 4.6 m differ in paint class
        out = list(table.values())
        bad = False
        for a in sides.get("east", []):
            for b in sides.get("west", []):
                if abs(a["x_centre_m"] - b["x_centre_m"]) <= 4.6 and table[a["house"]]["paint_class"] == table[b["house"]]["paint_class"]:
                    bad = True
        if bad or len({r["kind"] for r in out}) < 10 and len(out) >= 12:
            continue
        for r in out:
            r["seed"], r["attempt"] = seed, attempt
        return out
    raise RuntimeError("the mixer found no street for seed %d" % seed)


# ------------------------------------------------------------------ paints and conditions
def paints_json(N):
    out = []
    for p in N["paints"]:
        out.append({"id": p["id"], "material": "paint_" + p["id"], "srgb": p["srgb"], "linear": [round(lin(c), 5) for c in p["srgb"]], "class": p["class"],
                    "metallic": 0.0, "roughness": {c: N["conditions"][c]["roughness"] for c in ("kept", "tired", "neglected")}, "src": p["src"]})
    frames = [{"id": f["id"], "material": "paint_" + f["id"], "srgb": f["srgb"], "linear": [round(lin(c), 5) for c in f["srgb"]], "roughness": 0.35, "src": f["src"]} for f in N["frame_colours"]]
    return {"door_paints": out, "frame_colours": frames}


def conditions_json(N):
    c = {k: condition_data(N, k) for k in ("kept", "tired", "neglected")}
    return {"note": ("The three conditions as a parameter set for the engine's materials and for the wear layer of unit 4.5 (production/cloud-week/2d/wear/, target production/cloud-week/targets/wear/target.json): "
                     "roughness is set in each house's door material; the neglected door carries the eroded notch as geometry (leaf_notch_bare); everything else is the layer's masks. "
                     "No vertex colour is written: a leaf is a few large flat faces, and a gradient across them would not carry a splash band."),
            "wear_layer_kinds": N["wear_kinds_used"], "not_covered_by_the_layer": N["wear_not_covered"], "conditions": c,
            "notch": {"height_mm": 25.0, "width_mm": 130.0, "depth_mm": 3.0, "side": "the hinge side's end of the bottom edge", "material": "timber_bare (118, 110, 100)"}}
