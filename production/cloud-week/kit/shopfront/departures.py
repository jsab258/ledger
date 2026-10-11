"""Try 2's departures from the shopfront target (cloud week 42, 11 October 2026, by Jafar's ruling no more target polishing).

The two fresh reviews of try 1 (REVIEW-v1-close.md, REVIEW-v1-street.md) set photographs against the target in five places.
Each is one named number or profile here, written into a COPY of target.json by `apply(T)`; the builder and the check both
read the copy (and target_drawing.py draws from it), so every other number is still measured against the target itself and each
departure is visible in `DEPARTURES`. The target is untouched.

    D1  the console's side profile (close review fault 1): a tapering bracket, not a block with two rolls
    D2  the console's side spirals are raised fillets 10 wide standing 6 proud, the eye bosses 30 and 20 across, 8 proud
    D3  the acanthus leaf (close fault 2, street narrow point 2): raised rib, chevron veins, domed lobes, the head over the roll
    D4  the cornice breaks forward 85 over each console, with mitred returns (close fault 1's last bullet)
    D5  a cyma reversa bed mould, 40 high, d 120 to 150, under the cornice between the consoles (close narrow point 1)
    D6  the toplights: nine of 326.9, the mullions carried up as 70 wide bars and two 28 bars a light (street narrow point 1)
    D7  the capital tablet's edge eased 3 mm (close narrow point 2)
"""
import copy
import math

# ---- D1: the side profile, (d, z local from the console's foot at z 2850), front edge from the foot up
LOWER = {"eye": (125.0, 60.0), "r": 40.0}            # the lower volute: eye d 125, z 60, front 165
UPPER = {"eye": (200.0, 440.0), "r": 80.0}           # the upper volute: eye d 200, z 440, front 280, top z 520
FOOT_D, WAIST = 134.0, (140.0, 170.0)
CAP_D, CAP_Z = 290.0, (520.0, 550.0)


def _bez(p0, p1, p2, p3, n=10):
    out = []
    for i in range(1, n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def side_silhouette():
    """[(0,0), (130,0), ..., (290,550), (0,550)]: the lower roll (r 40, front 165), the concave body to the waist (d 140 at z 170),
    the cove up to the upper roll (r 80, front 280 at z 440, top z 520), the cap block 290 deep at z 520 to 550."""
    pts = [(0.0, 0.0), (FOOT_D, 0.0)]
    ex, ez = LOWER["eye"]
    r = LOWER["r"]
    th0 = -math.degrees(math.acos((FOOT_D - ex) / r))              # the roll leaves the foot's front (d 130) at z 20.3
    th = th0
    while th <= 30.0 + 1e-9:
        pts.append((ex + r * math.cos(math.radians(th)), ez + r * math.sin(math.radians(th))))
        th += 6.0
    p0 = pts[-1]
    t0 = (-math.sin(math.radians(30.0)), math.cos(math.radians(30.0)))
    pts += _bez(p0, (p0[0] + 25 * t0[0], p0[1] + 25 * t0[1]), (WAIST[0], WAIST[1] - 30.0), WAIST)           # concave, vertical at the waist
    pts += _bez(WAIST, (WAIST[0], WAIST[1] + 70.0), (160.0, 340.0), (UPPER["eye"][0], UPPER["eye"][1] - UPPER["r"]), 14)   # the cove
    ex, ez, r = UPPER["eye"][0], UPPER["eye"][1], UPPER["r"]
    for k in range(1, 31):                                         # the upper roll, bottom to top, 6 degrees a step
        a = math.radians(-90.0 + 6.0 * k)
        pts.append((ex + r * math.cos(a), ez + r * math.sin(a)))
    pts += [(CAP_D, CAP_Z[0]), (CAP_D, CAP_Z[1]), (0.0, CAP_Z[1])]
    return [[round(a, 3), round(b, 3)] for a, b in pts]


def spiral(eye, r0, r1, turns, ccw, step=6.0):
    n = int(round(turns * 360.0 / step))
    out = []
    for k in range(n + 1):
        a = k * step * (1.0 if ccw else -1.0)
        r = r0 + (r1 - r0) * k / n
        out.append([round(eye[0] + r * math.cos(math.radians(a)), 3), round(eye[1] + r * math.sin(math.radians(a)), 3)])
    return out


def circle(eye, r, n=16):
    return [[round(eye[0] + r * math.cos(2 * math.pi * k / n), 3), round(eye[1] + r * math.sin(2 * math.pi * k / n), 3)] for k in range(n)]


# ---- D3: the leaf
LEAF_HEAD = [[58.0, 420.0], [54.0, 436.0], [46.0, 452.0], [32.0, 464.0], [14.0, 470.0], [0.0, 471.0]]   # the head carried 50 over the roll
LEAF = {"dome_mm": 12.0, "rib_w": 8.0, "rib_proud": 4.0, "vein_w": 3.0, "vein_depth": 2.0, "vein_angle_deg": 35.0, "tip_forward": 6.0, "dome_radius": 22.0}

# ---- D4: the cornice's break over each console (plan, nose line: the main run's nose is d 215)
BREAK = {"forward": 85.0, "left_u": [54.0, 305.0], "right_u": [5695.0, 5946.0], "nose_d": 300.0}

# ---- D5: the bed mould
BED = {"z": [3360.0, 3400.0], "d": [120.0, 150.0], "u": [295.0, 5705.0]}

# ---- D6: the toplights
TOP_BARS = [390.9, 745.8, 1497.6, 1852.5, 2604.2, 2959.1]        # 28 wide, two a light
TOP_MULLION_BARS = [1121.7, 2228.3]                              # 70 wide: the mullions carried up

DEPARTURES = [
    "D1 console side profile: cap block 290 deep, upper roll r 80 (front 280 at z 440, top z 520), lower roll r 40 (front 165), foot 134 deep (REVIEW-v1 gave 130; REVIEW-v2-close narrow point 2 sets 134 so that the board's bed mould, 132, does not stand proud of it), waist 140 at z 170 (REVIEW-v1-close fault 1; target: 205 deep, rolls r 45 and 26, foot 172)",
    "D2 console sides: raised spiral fillets 10 wide standing 6 proud (upper 1.5 turns r 62 to 17, lower 1 turn r 24 to 11) and eye bosses 30 and 20 across standing 8 proud, not 5 x 4 grooves (fault 1; target: grooves)",
    "D3 acanthus leaf: raised rib 8 wide 4 proud the full length, chevron veins 3 wide 2 deep from each notch up and inward to the rib, each lobe domed 12 with its tip turned 6 forward, the head carried 50 over the upper roll to z 471 (fault 2; the target says only 'grooves between lobes')",
    "D4 cornice: broken forward 85 (nose d 300) over each console, u 54 to 305 and 5695 to 5946, with mitred returns back to the main nose d 215 (fault 1; target: one straight run)",
    "D5 bed mould: cyma reversa 40 high, d 120 to 150, z 3360 to 3400, between the consoles (close narrow point 1; target: none)",
    "D6 toplights: nine of 326.9, the mullions carried up as 70 wide bars (centres 1121.7, 2228.3) and two 28 wide bars a light (390.9, 745.8, 1497.6, 1852.5, 2604.2, 2959.1) (street narrow point 1; target: eight, bars between the lights' middles)",
    "D7 capital tablet: edges eased 3 mm (close narrow point 2; target: 1 mm)",
]


def apply(T):
    """A copy of the target with the departures written in."""
    T = copy.deepcopy(T)
    P = T["parts"]
    C = P["console"]
    d, pr = C["dims"], C["profiles"]
    d["depth"] = CAP_D
    d["toe_depth"] = FOOT_D
    d["cap_block"] = {"d": CAP_D, "z_local": list(CAP_Z)}
    d["upper_volute"] = {"eye_dz": list(UPPER["eye"]), "outer_radius": UPPER["r"], "front_d_at_eye_z": UPPER["eye"][0] + UPPER["r"],
                         "top_point_dz": [UPPER["eye"][0], UPPER["eye"][1] + UPPER["r"]], "turns": 1.5, "direction": "counter-clockwise: up the front, over the top, back and down into the eye"}
    d["lower_volute"] = {"eye_dz": list(LOWER["eye"]), "outer_radius": LOWER["r"], "reach_d_at_eye_z": LOWER["eye"][0] + LOWER["r"], "direction": "clockwise inward: rolling the other way"}
    d["waist"] = {"narrowest_d": WAIST[0], "at_z_local": WAIST[1], "concave": True}
    d["side_fillets"] = {"width": 10.0, "proud": 6.0, "eye_boss_diameter_upper": 30.0, "eye_boss_diameter_lower": 20.0, "eye_boss_proud": 8.0,
                         "upper": "from r 62 in 1.5 turns to r 17", "lower": "one turn clockwise, r 24 to 11"}
    d.pop("side_grooves", None)
    d["stem"] = {"d_at_z_local_330": None}
    sil = side_silhouette()
    pr["side_silhouette"]["points"] = sil
    pr["plan_at_neck"]["points"] = [[-120.0, 0.0], [120.0, 0.0], [120.0, CAP_D - 12.0], [108.0, CAP_D], [-108.0, CAP_D], [-120.0, CAP_D - 12.0]]
    pr["volute_upper_spiral"]["points"] = spiral(UPPER["eye"], 62.0, 17.0, 1.5, True)
    pr["volute_lower_spiral"]["points"] = spiral(LOWER["eye"], 24.0, 11.0, 1.0, False)
    pr["eye_boss_upper"]["points"] = circle(UPPER["eye"], 15.0)
    pr["eye_boss_lower"]["points"] = circle(LOWER["eye"], 10.0)
    lf = d["leaf"]
    lf.update({"z_local": [150.0, 471.0], "relief_mm": LEAF["dome_mm"] + LEAF["rib_proud"], "head_extension": LEAF_HEAD, "try2": LEAF,
               "groove_between_lobes": {"width": LEAF["vein_w"], "depth": LEAF["vein_depth"]}})
    P["cornice"]["dims"]["break_forward"] = BREAK
    P["cornice"]["dims"]["depth_max"] = BREAK["nose_d"]
    P["fascia_board"]["dims"]["bed_mould_cyma"] = BED
    S = [s for s in T["shops"] if s["id"] == "ritas"][0]
    S["glazing_layout"]["toplight_bar_centres"] = TOP_BARS
    S["glazing_layout"]["toplight_mullion_bar_centres"] = TOP_MULLION_BARS
    S["glazing_layout"]["toplights"] = 9
    S["glazing_layout"]["toplight_width"] = 326.9
    P["window_frame"]["dims"]["toplights"].update({"count": 9, "light_width": 326.9, "bar_xs_default": TOP_BARS, "mullion_bar_xs_default": TOP_MULLION_BARS})
    P["pilaster"]["dims"]["die_tablet_chamfer"] = 3.0
    T["try2_departures"] = DEPARTURES
    return T
