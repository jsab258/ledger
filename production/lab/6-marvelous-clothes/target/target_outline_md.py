"""The outline Ron's amended clothes should show (front, back, side) with the covered body points, in the
same form as test 4's target.json, so test 4's checks run unchanged. It is the check AFTER the cloth
simulation; the pattern (pattern_md.json) is the target the simulator sews.

Method: test 4's target_outline.py, imported and run as it is, with these globals replaced from
pattern_md.json and the amendments (TARGET.md, "Outline: what changed"):
  - sleeve widths (A1, A6, A7): the new sleeve radius along the arm, the dropped shoulder, the bunching;
  - hem rib 7 cm deep, relaxed 106.6 cm (A5);
  - trouser hem 2.5 cm off the floor at the back, 54.0 cm round (A2); seat and thigh girths with the pleat fullness (A3);
  - the seat follows the body (A9): between band and seat line the cloth is the body's own section plus an
    ease growing from the band's to the seat's, instead of test 4's straight girth (O9);
  - masks to F:/LedgerTools/lab/clothes/target_md.

    python target_outline_md.py     -> target_md.json beside this file
"""
import importlib.util
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
T4 = os.path.normpath(os.path.join(HERE, "..", "..", "4-plain-clothes", "target"))
pm = json.load(open(os.path.join(HERE, "pattern_md.json")))
A, JN, TN = pm["amendments"], pm["numbers"]["jumper"], pm["numbers"]["trousers"]

spec = importlib.util.spec_from_file_location("target_outline_t4", os.path.join(T4, "target_outline.py"))
tol = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tol)                     # loads Ron, computes test 4's levels (unchanged: hem, underarm, band)

tol.OUT = r"F:/LedgerTools/lab/clothes/target_md"
tol.HERE = HERE
tol.pat = dict(tol.pat)
tol.JT = dict(tol.JT, hip_hem_rib_relaxed=JN["hem_rib_relaxed"])
tol.Z_RIB = tol.Z_HEM + A["hem_rib_depth"] / 100                              # A5
tol.Z_HEM_T = A["trouser_hem_back_z"]                                         # A2
tol.G_HEM = (2 * A["trouser_half_foot_in"] + 0.5) * 2.54 / 100                # A2
tol.G_SEAT = (tol.TT["seat"] + 2 * TN["pleat_spread_at_seat"]) / 100          # A3
yK, yw, yH = TN["yK"], TN["yw"], TN["yH"]
tol.G_THIGH = (tol.TT["thigh_at_fork_one_leg"] + A["pleat1_cm"] * np.clip((yK - yH) / (yK - yw), 0, 1)) / 100

# A9 the seat follows the body: ease grows from the band's to the seat line's, on the body's own section
_E_BAND = tol.G_BAND - tol.per(tol.torso(tol.Z_BAND_LO))
_E_SEAT = tol.G_SEAT - tol.per(tol.torso(tol.Z_SEATLINE))


def trouser_torso(z):
    B = tol.torso(z)
    if z >= tol.Z_BAND_LO:
        G = tol.G_BAND
    elif z >= tol.Z_SEATLINE:
        f = (z - tol.Z_SEATLINE) / (tol.Z_BAND_LO - tol.Z_SEATLINE)
        G = tol.per(B) + _E_SEAT + (_E_BAND - _E_SEAT) * f
    else:
        G = tol.G_SEAT
    return tol.offset(B, max(tol.T, (G - tol.per(B)) / (2 * np.pi)))


tol.trouser_torso = trouser_torso

# A1/A6/A7 sleeve: width along the arm (s from the shoulder point, m) from pattern_md's sleeve
D = A["shoulder_drop_cm"] / 100
h = JN["cap_height"] / 100
y_el, y_fa = JN["y_elbow"] / 100, JN["y_forearm"] / 100
y_bot_worn = (JN["sleeve_bottom"] - A["cuff_blouse_length"]) / 100           # the 2 cm bunch sits over the cuff
L = tol.JT["sleeve_length_shoulder_to_cuff_edge"] / 100
W0, Wel, Wfa, Wb = JN["W_biceps"] / 100, JN["W_elbow"] / 100, JN["W_forearm"] / 100, JN["W_bottom"] / 100
Wc = A["cuff_rib_relaxed"] / 100


def sleeve_radius(s):
    W = np.interp(s, [0, D + h, D + y_el, D + y_fa, D + y_bot_worn, D + y_bot_worn + 1e-4, L],
                  [W0, W0, Wel, Wfa, Wb, Wc, Wc])
    return W / (2 * np.pi)


tol.sleeve_radius = sleeve_radius

if __name__ == "__main__":
    tol.main()                                    # writes target.json beside this file, masks to OUT; fails on its self-check
    src = os.path.join(HERE, "target.json")
    tj = json.load(open(src))
    tj["pattern"] = "pattern_md.json"
    tj["rules"] = "test 4 TARGET.md O1-O14 as amended by 6-marvelous-clothes/target/TARGET.md A1-A12"
    tj["levels"]["trouser_hem_front"] = round(A["trouser_hem_back_z"] + 0.0254, 4)
    tj["covered"]["trousers"] = tj["covered"]["trousers"].replace("z 0.040 at the back, 0.065 at the front",
                                                                  "z %.3f at the back, %.3f at the front" % (A["trouser_hem_back_z"], A["trouser_hem_back_z"] + 0.0254))
    tj["changed_from_test4"] = [
        "sleeve radius from pattern_md (A1 ease 12/10/9 cm at biceps/elbow/forearm, A7 dropped shoulder 6 cm, A6 cuff 19 cm, 2 cm bunched)",
        "hem rib 7 cm deep, 106.6 cm relaxed (A5)",
        "trouser hem 2.5 cm off the floor at the back, 1 in higher at the front (T27 kept), 54.0 cm round (A2)",
        "seat and thigh girths include the pleat fullness (A3)",
        "seat follows the body between band and seat line (A9) instead of O9's straight girth",
        "the break over the boot is NOT in the outline: the body mesh has no boot; the simulation must show it (A2)",
        "masks in F:/LedgerTools/lab/clothes/target_md",
    ]
    json.dump(tj, open(os.path.join(HERE, "target_md.json"), "w"), indent=None, separators=(",", ":"))
    os.remove(src)
    print("target_md.json written; self-check", tj["self_check"])
