"""Self-check of pattern_md.json (run after draft_md.py). Writes the result into pattern_md.json under
"self_check" and prints it. Fails (exit 1) if any check fails.

1. every seam pair: equal lengths within 3 mm, or the stated ratio within 3 mm, or a stated ease (eased seams pass
   only if the difference is at most 2 cm, the tailor's limit for easing worsted);
2. finished girths and lengths, measured from the piece outlines, against the target table within 5 mm;
3. sleeve widths minus Ron's arm girths (ron_parts.npz, measured afresh) give the amended ease within 5 mm;
4. every photograph element is covered by an existing piece, edge, seam, internal line or rule.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import draft_md as dm  # noqa: E402

PJ = os.path.join(HERE, "pattern_md.json")
pat = json.load(open(PJ))
P, A = pat["pieces"], pat["amendments"]
JN, TN = pat["numbers"]["jumper"], pat["numbers"]["trousers"]
T4J = dm.PAT4["table"]["jumper_cm"]
T4T = dm.PAT4["table"]["trousers_cm"]
IN = 2.54


def width_at(piece, y):
    O = np.array(P[piece]["outline"]); xs = []; y = y + 1e-6
    for a, b in zip(O, np.roll(O, -1, 0)):
        if (a[1] - y) * (b[1] - y) < 0:
            xs.append(a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]))
    return max(xs) - min(xs)


def side_x(piece, y):
    """the outline's smallest x crossing at height y (the side seam on Thornton's front, y up)"""
    O = np.array(P[piece]["outline"]); xs = []; y = y + 1e-6
    for a, b in zip(O, np.roll(O, -1, 0)):
        if (a[1] - y) * (b[1] - y) < 0:
            xs.append(a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]))
    return min(xs)


def ylo(piece):
    return min(p[1] for p in P[piece]["outline"])


def elen(piece, edge):
    return P[piece]["edges"][edge]["length_cm"]


res = dict()
# ---- 1. seams
sres, sfail = [], 0
for s in pat["seams"]:
    la, lb = s["a"]["length_cm"], s["b"]["length_cm"]
    e = s["ease"]
    if e["kind"] == "equal":
        ok, what = abs(la - lb) <= 0.3, "equal: %.2f vs %.2f" % (la, lb)
    elif e["kind"] == "ratio":
        ok, what = abs(lb - e["b_over_a"] * la) <= 0.3, "ratio %.3f: %.2f x r = %.2f vs %.2f" % (e["b_over_a"], la, la * e["b_over_a"], lb)
    else:
        ok, what = abs(lb - la) <= 2.0, "eased: %.2f vs %.2f (difference %.2f cm stated)" % (la, lb, lb - la)
    sfail += not ok
    sres.append(dict(id=s["id"], ok=bool(ok), detail=what))
res["seams"] = dict(count=len(sres), failed=sfail, each=sres)

# ---- 2. target table (amended values, set from the amendments and test 4, not from the pieces)
y_u = -(JN["y_underarm_on_body"] + 1.0)
spread_seat = TN["pleat_spread_at_seat"]
leg_delta = (TN["measures_in"]["leg"] - dm.PAT4["trouser_measures_inches"]["leg"]) * IN
yH = -TN["yH"]; yK = -TN["yK"]; yE = -TN["yE"]
t1 = lambda y: float(np.clip((TN["yK"] - y) / (TN["yK"] - TN["yw"]), 0, 1))
pts = {k: np.array(v) for k, v in TN["points"].items()}
target = {
    "jumper chest finished": (T4J["chest_finished"], width_at("jumper_front", y_u) + width_at("jumper_back", y_u)),
    "jumper back length, neck point to hem edge (incl. 1.5 blouse)": (T4J["back_length_hps_to_hem"] + A["body_blouse_length"],
                                                                      -ylo("jumper_back") + A["hem_rib_depth"]),
    "jumper hem rib relaxed": (A["hem_rib_ratio"] * T4J["chest_finished"], elen("hem_rib_front", "seam_0") + elen("hem_rib_back", "seam_0")),
    "jumper hem rib depth": (A["hem_rib_depth"], (max(p[1] for p in P["hem_rib_front"]["outline"]) - ylo("hem_rib_front"))),
    "sleeve top width (at the underarm)": (pat["ron_arm_girths_cm"]["biceps"]["girth"] + A["ease_biceps"], width_at("jumper_sleeve_R", -(JN["cap_height"] + 0.01))),
    "sleeve length, cap top to cuff edge (incl. 2 bunching)": (T4J["sleeve_length_shoulder_to_cuff_edge"] - A["shoulder_drop_cm"] + A["cuff_blouse_length"],
                                                               -ylo("jumper_sleeve_R") + A["cuff_rib_depth"]),
    "sleeve width above the cuff": (A["sleeve_bottom_width"], elen("jumper_sleeve_R", "bottom")),
    "cuff rib relaxed": (A["cuff_rib_relaxed"], elen("cuff_R", "seam_0")),
    "neck rib relaxed": (A["neck_rib_ratio"] * (elen("jumper_front", "neckline") + elen("jumper_back", "neckline")),
                         elen("neck_rib", "seam_0") + elen("neck_rib", "seam_1")),
    "shoulder seam (neck point to dropped end)": (np.hypot(T4J["cross_back"] / 2 - 9.0, 6.8) + A["shoulder_drop_cm"], elen("jumper_front", "shoulder_L")),
    "trouser waistband (both halves, without the fly extension)": (T4T["waist_band"], 2 * sum(elen("waistband_L", e) for e in
                                                                   ("band_cf", "band_fmid", "band_fside", "band_bside", "band_bmid", "band_cb"))),
    "trouser waist seam after pleats and darts": (T4T["waist_band"], 2 * sum([elen("trouser_front_R", e) for e in ("waist_cf", "waist_mid", "waist_side")] +
                                                                             [elen("trouser_back_R", e) for e in ("waist_side", "waist_mid", "waist_cb")])),
    "trouser seat (incl. pleat fullness): Thornton's measure, outline side seam to E on the seat line + back 10-11, doubled": (T4T["seat"] + 2 * spread_seat,
        2 * ((pts["E"][0] - side_x("trouser_front_R", yE)) + np.linalg.norm(pts["11"] - pts["10"]))),
    "trouser thigh at the fork, one leg (incl. pleat fullness)": (T4T["thigh_at_fork_one_leg"] + A["pleat1_cm"] * t1(TN["yH"]),
                                                                  width_at("trouser_front_R", yH + 0.01) + width_at("trouser_back_R", yH + 0.01) -
                                                                  0),
    "trouser knee, one leg": (T4T["knee_one_leg"], width_at("trouser_front_R", yK) + width_at("trouser_back_R", yK)),
    "trouser hem, one leg": ((2 * A["trouser_half_foot_in"] + 0.5) * IN, elen("trouser_front_R", "hem") * 0 +
                             abs(pts["L"][0] - pts["P"][0]) + abs(pts["4"][0] - pts["13"][0])),
    "trouser inseam (test 4 + the longer leg)": (T4T["inseam"] + leg_delta, elen("trouser_front_R", "inseam")),
    "trouser outside leg incl. band (test 4 + the longer leg, + pleat spread)": (None, elen("trouser_front_R", "outseam") + TN["band_depth"]),
}
tres, tfail = [], 0
for k, (want, got) in target.items():
    if want is None:
        tres.append(dict(item=k, target=None, measured=round(float(got), 2), ok=True, note="reported, no target (rule A2 sets the length by the break)"))
        continue
    ok = abs(want - got) <= 0.5
    tfail += not ok
    tres.append(dict(item=k, target=round(float(want), 2), measured=round(float(got), 2), ok=bool(ok)))
res["table"] = dict(failed=tfail, each=tres)

# ---- 3. sleeve ease against Ron's arm, girths measured afresh from ron_parts.npz
G = dm.arm_girths()
sl = "jumper_sleeve_R"
st = [("biceps (sleeve top width vs the fullest upper-arm girth)", width_at(sl, -(JN["cap_height"] + 0.01)), G["biceps"][0], A["ease_biceps"]),
      ("elbow", width_at(sl, -JN["y_elbow"]), G["elbow"][0], A["ease_elbow"]),
      ("forearm (fullest, 4-12 cm below the elbow)", width_at(sl, -JN["y_forearm"]), G["forearm"][0], A["ease_forearm"])]
eres, efail = [], 0
for nm, w, g, e in st:
    ok = abs((w - g) - e) <= 0.5
    efail += not ok
    eres.append(dict(station=nm, sleeve_width=round(w, 2), ron_girth=round(g, 2), ease=round(w - g, 2), amended_ease=e,
                     stand_off_mm=round((w - g) / (2 * np.pi) * 10, 1), ok=bool(ok)))
res["sleeve_ease"] = dict(failed=efail, each=eres, girth_method="convex hull of the plane section square to the arm axis (tape), left arm, ron_parts.npz")

# ---- 4. photograph elements covered
RULES = {"A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12"}
PHOTO = [
    ("crew-neck rib lying flat round the neck", ["piece:neck_rib", "seam:neck_rib_front", "rule:A5"]),
    ("hem rib drawn in at the hip, body bloused over it", ["piece:hem_rib_front", "piece:hem_rib_back", "seam:hem_rib_front", "rule:A5"]),
    ("rib cuffs gripping the wrist, sleeve bunched over them", ["piece:cuff_R", "seam:cuff_R", "rule:A6"]),
    ("sleeve standing off the arm with soft folds", ["piece:jumper_sleeve_R", "rule:A1"]),
    ("dropped shoulder: the armhole seam on the upper arm", ["edge:jumper_front/shoulder_L", "rule:A7"]),
    ("jumper hem at the top of the hip, over the trouser waistband", ["rule:A8"]),
    ("sleeve ends at the wrist bone", ["rule:A6"]),
    ("jumper body hangs straight and loose", ["piece:jumper_front", "rule:A8"]),
    ("shirt collar showing above the crew neck (photo 1)", ["rule:A12"]),
    ("trouser waistband flush with the trousers", ["piece:waistband_L", "seam:band_cf_L", "rule:A4"]),
    ("fly front", ["piece:fly_facing_L", "piece:fly_shield_R", "seam:fly_closed", "line:trouser_front_L/fly_topstitch", "rule:A4"]),
    ("two front pleats each side", ["seam:pleat1_L", "seam:pleat2_L", "rule:A3"]),
    ("pressed front crease from the pleat to the hem", ["line:trouser_front_R/crease_front", "rule:A3"]),
    ("slant side pocket opening at the hip", ["line:trouser_front_R/slant_pocket", "rule:A10"]),
    ("full seat for a heavy man", ["edge:trouser_back_R/seat", "rule:A9"]),
    ("full thigh narrowing to the hem", ["rule:A2"]),
    ("hem breaking on the shoe front, plain hem without turn-ups", ["edge:trouser_front_R/hem", "rule:A2"]),
    ("no belt visible (photo 1 hides the waist under the rib)", ["rule:A11"]),
]
seam_ids = {s["id"] for s in pat["seams"]}
cres, cfail = [], 0
for el, refs in PHOTO:
    bad = []
    for r in refs:
        kind, ref = r.split(":", 1)
        if kind == "piece":
            ok = ref in P
        elif kind == "seam":
            ok = ref in seam_ids
        elif kind == "edge":
            pc, ed = ref.split("/"); ok = pc in P and ed in P[pc]["edges"]
        elif kind == "line":
            pc, ln = ref.split("/"); ok = pc in P and any(i["name"] == ln for i in P[pc]["internal_lines"])
        else:
            ok = ref in RULES
        if not ok:
            bad.append(r)
    cfail += bool(bad)
    cres.append(dict(element=el, covered_by=refs, ok=not bad, missing=bad))
res["photo_elements"] = dict(failed=cfail, each=cres)

# ---- outline orientation sanity (every outline CCW, every edge index list walks adjacent points)
ofail = []
for nm, p in P.items():
    O = np.array(p["outline"]); n = len(O)
    a = 0.5 * np.sum(O[:, 0] * np.roll(O[:, 1], -1) - np.roll(O[:, 0], -1) * O[:, 1])
    if a <= 0:
        ofail.append(nm + " not CCW")
    for en, e in p["edges"].items():
        ii = e["indices"]
        if any(((j - i) % n) not in (1, n - 1) for i, j in zip(ii, ii[1:])):
            ofail.append(nm + "/" + en + " not contiguous")
res["outlines"] = dict(failed=len(ofail), problems=ofail)

res["passed"] = not (sfail or tfail or efail or cfail or ofail)
pat["self_check"] = res
pat["photo_elements"] = [dict(element=e, covered_by=r) for e, r in PHOTO]
json.dump(pat, open(PJ, "w"), indent=1)
print("seams: %d of %d pass" % (len(sres) - sfail, len(sres)))
for s in sres:
    if not s["ok"] or "eased" in s["detail"] or "ratio" in s["detail"]:
        print("  ", s["id"], s["ok"], s["detail"])
print("table: %d of %d pass" % (len(tres) - tfail, len(tres)))
for t in tres:
    print("  ", t)
print("sleeve ease:")
for e in eres:
    print("  ", e)
print("photo elements: %d of %d covered" % (len(cres) - cfail, len(cres)), [c for c in cres if not c["ok"]])
print("outlines:", ofail or "all CCW and contiguous")
print("PASSED" if res["passed"] else "FAILED")
sys.exit(0 if res["passed"] else 1)
