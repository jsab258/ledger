"""Builds target.json for the Quay Street pillar box from pb_numbers.py.

    /home/user/.bpyenv/bin/python make_target.py            (writes target.json beside this file)

Nothing here is measured on a photograph: no photograph of a pillar box was reached (TARGET.md section 2).
The self-check result block is written later by self_check.py.
"""
import json
import math
import numpy as np
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pb_numbers as P  # noqa: E402

REG = P.REG
V = lambda k: REG[k]["value"]  # noqa: E731

R_BODY = P.R_BODY
H_TOTAL = P.H_TOTAL


# ---------------------------------------------------------------------------------------------------------------
# 1. the lathe profile (radius, z) of the outer surface, from the buried skirt up the axis. mm.
# ---------------------------------------------------------------------------------------------------------------
def arc_pts(cx, cz, a, b, t0, t1, n, fr, fz):
    out = []
    for i in range(n + 1):
        t = math.radians(t0 + (t1 - t0) * i / n)
        out.append((fr(cx, a, t), fz(cz, b, t)))
    return out


def rnd(p):
    return [round(p[0], 2), round(p[1], 2)]


def profile():
    pts = []
    segs = []

    def add(name, plist):
        segs.append({"name": name, "first": len(pts), "last": len(pts) + len(plist) - 1})
        pts.extend(plist)

    rf = V("foot_radius")
    add("buried_skirt", [(rf, -V("hidden_skirt")), (rf, 0.0)])
    add("foot_band", [(rf, 0.0), (rf, V("foot_band_height"))])
    # quarter round on the foot's top edge: centre (rf - R, band), 0 to 90 degrees
    R = V("foot_top_round")
    add("foot_top_round", [(rf - R + R * math.cos(math.radians(a)), V("foot_band_height") + R * math.sin(math.radians(a)))
                           for a in range(0, 91, 15)])
    r_round_end = rf - R
    z_round_end = V("foot_band_height") + R
    # splay 45 degrees (here 14 x 12) to (262, 72)
    add("foot_splay", [(r_round_end, z_round_end), (V("foot_splay_top_radius"), V("foot_splay_top_z"))])
    # cove: ellipse quadrant, horizontal at the splay, vertical at the body
    a_ = V("foot_splay_top_radius") - R_BODY
    b_ = V("foot_cove_top_z") - V("foot_splay_top_z")
    cove = [(V("foot_splay_top_radius") - a_ * math.sin(math.radians(t)), V("foot_cove_top_z") - b_ * math.cos(math.radians(t)))
            for t in range(0, 91, 10)]
    add("foot_cove", cove)
    add("body", [(R_BODY, V("foot_cove_top_z")), (R_BODY, V("cap_soffit_z"))])
    # cap under-moulding: quarter ellipse, vertical at the body, horizontal at the rim lip
    a2 = V("cap_radius") - R_BODY
    b2 = V("cap_cove_height")
    z_c = V("cap_soffit_z")
    add("cap_cove", [(V("cap_radius") - a2 * math.cos(math.radians(t)), z_c + b2 * math.sin(math.radians(t)))
                     for t in range(0, 91, 10)])
    add("cap_rim", [(V("cap_radius"), z_c + b2), (V("cap_radius"), V("cap_rim_top_z"))])
    rb = V("cap_bead_radius")
    add("cap_bead", [(V("cap_radius") - rb + rb * math.cos(math.radians(t)), V("cap_rim_top_z") + rb * math.sin(math.radians(t)))
                     for t in range(0, 91, 15)])
    z_bead_end = V("cap_rim_top_z") + rb
    add("cap_shoulder", [(V("cap_radius") - rb, z_bead_end), (V("cap_shoulder_radius"), z_bead_end)])
    add("cap_neck", [(V("cap_shoulder_radius"), z_bead_end), (V("cap_shoulder_radius"), V("dome_base_z"))])
    a = V("cap_shoulder_radius")
    s = V("dome_sagitta")
    Rs = (a * a + s * s) / (2 * s)
    dome = []
    n = 20
    for i in range(n + 1):
        r = a * (1 - i / n)
        z = H_TOTAL - (Rs - math.sqrt(Rs * Rs - r * r))
        dome.append((r, z))
    add("dome", dome)
    out = [rnd(p) for p in pts]
    return out, segs, Rs


# ---------------------------------------------------------------------------------------------------------------
# 2. colour: red dry, wet and under sodium light
# ---------------------------------------------------------------------------------------------------------------
def s2l(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def l2s(x):
    x = max(0.0, min(1.0, x))
    return 255 * (12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055)


def g(lam, mu, s1, s2):
    s = s1 if lam < mu else s2
    return math.exp(-0.5 * ((lam - mu) / s) ** 2)


def cmf(lam):  # Wyman, Sloan and Shirley 2013 multi-lobe fit of the CIE 1931 functions (the writer's memory of it: see TARGET.md)
    x = 1.056 * g(lam, 599.8, 37.9, 31.0) + 0.362 * g(lam, 442.0, 16.0, 26.7) - 0.065 * g(lam, 501.1, 20.4, 26.2)
    y = 0.821 * g(lam, 568.8, 46.9, 40.5) + 0.286 * g(lam, 530.9, 16.3, 31.1)
    z = 1.217 * g(lam, 437.0, 11.8, 36.0) + 0.681 * g(lam, 459.0, 26.0, 13.8)
    return x, y, z


def d65_like(lam):  # a 6504 K blackbody stands in for D65: only relative values are used
    T = 6504.0
    l = lam * 1e-9
    return 1.0 / (l ** 5 * (math.exp(1.4388e-2 / (l * T)) - 1))


M = [[3.2406, -1.5372, -0.4986], [-0.9689, 1.8758, 0.0415], [0.0557, -0.2040, 1.0570]]

LAMS = np.arange(380, 781, 2.0)
_E = np.array([d65_like(l) for l in LAMS])
_C = np.array([cmf(l) for l in LAMS])          # (n, 3)
_W = _E[:, None] * _C                           # illuminant x cmf
_MM = np.array(M)


def refl_curve(lam, lam0, w, rmin, rmax):
    return rmin + (rmax - rmin) / (1 + np.exp(-(lam - lam0) / w))


def _rgb_of_weights(wxyz):
    return _MM @ wxyz


_WHITE = _rgb_of_weights(_W.sum(0) / _W[:, 1].sum())


def daylight_lin(lam0, w, rmin, rmax):
    r = refl_curve(LAMS, lam0, w, rmin, rmax)
    xyz = (r[:, None] * _W).sum(0) / _W[:, 1].sum()
    rgb = _rgb_of_weights(xyz)
    return list(rgb / _WHITE)          # white-balanced so a flat grey stays grey


def fit_red():
    """Fit (edge, rmax, rmin) of a logistic reflectance edge, for three edge widths, so daylight gives the red's linear sRGB."""
    tgt = np.array([s2l(c) for c in V("red_srgb")])
    res = {}
    for w in (8.0, 12.0, 18.0):
        best = None
        for rmin in (0.006, 0.014, 0.022, 0.030):
            for lam0 in np.arange(570.0, 641.0, 1.0):
                for rmax in np.arange(0.30, 1.001, 0.01):
                    rgb = np.array(daylight_lin(lam0, w, rmin, rmax))
                    err = float(np.sum(np.log(np.maximum(rgb, 1e-6) / tgt) ** 2))
                    if best is None or err < best[0]:
                        best = (err, lam0, rmax, rmin, rgb)
        err, lam0, rmax, rmin, rgb = best
        r589 = float(refl_curve(589.0, lam0, w, rmin, rmax))
        r589_up = float(refl_curve(589.0, lam0 - 12.0, w, rmin, rmax))   # the same pigment with its edge 12 nm bluer: the upper estimate
        res[w] = {"reflectance_589_edge_12nm_bluer": round(r589_up, 3), "edge_nm": float(lam0), "rmax": round(float(rmax), 2), "rmin": rmin, "w_nm": w, "fit_rms_log_error": round(math.sqrt(err / 3), 3),
                  "daylight_lin": [round(float(x), 4) for x in rgb], "reflectance_589": round(r589, 3)}
    return res


def colour_block():
    red = V("red_srgb")
    lin = [s2l(c) for c in red]
    Y = 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
    mx, mn = max(red), min(red)
    hsv_s = (mx - mn) / mx
    wet_mult = 0.88
    wet_srgb = [round(l2s(c * wet_mult)) for c in lin]
    fit = fit_red()
    lamp = V("scene_lantern_linear_srgb")
    out = {"albedo_srgb": red, "albedo_linear": [round(x, 4) for x in lin], "relative_luminance": round(Y, 4),
           "L_star": round(116 * (Y ** (1 / 3)) - 16 if Y > 0.008856 else 903.3 * Y, 1),
           "hsv": {"s": round(hsv_s, 2), "v": round(mx / 255, 2)},
           "wet": {"albedo_multiplier_linear": wet_mult, "albedo_srgb": wet_srgb,
                   "roughness_delta": -0.18, "note": "paint stays glossy; a water film darkens the diffuse by about 12 % and the highlights sharpen"},
           "sodium": {"lamp_linear_srgb": lamp, "fits": fit}}
    white = 0.85
    rows = {}
    for w, f in fit.items():
        r = f["reflectance_589"]
        # spectral reading under a monochromatic 589 nm lamp: the surface can only return the lamp's colour at a fraction r of it
        # a perfect-white-ish surface of reflectance 0.85 under the lamp is (0.85 x lamp); the box is r x lamp
        box_lin = [r * c for c in lamp]
        rows[str(w)] = {"reflectance_589": r, "ratio_to_white_0.85": round(r / white, 3),
                        "lit_linear_at_lamp_x1": [round(x, 4) for x in box_lin],
                        "lit_srgb_at_lamp_x1": [round(l2s(x)) for x in box_lin]}
    naive = [lin[i] * lamp[i] for i in range(3)]
    ynaive = 0.2126 * naive[0] + 0.7152 * naive[1] + 0.0722 * naive[2]
    ywhite = white * (0.2126 * lamp[0] + 0.7152 * lamp[1] + 0.0722 * lamp[2])
    out["sodium"]["spectral_reading"] = rows
    out["sodium"]["naive_rgb_multiply"] = {"lit_linear": [round(x, 4) for x in naive], "lit_srgb": [round(l2s(x)) for x in naive],
                                           "luminance_ratio_to_white_0.85": round(ynaive / ywhite, 3),
                                           "note": "an RGB engine multiplies albedo by the lamp triple and keeps the red channel: the box stays a dark RED; a real 589 nm lamp can only make it a dark orange-olive brown"}
    ups = [fit[w]["reflectance_589_edge_12nm_bluer"] / white for w in fit]
    out["sodium"]["spectral_ratio_range"] = [round(min(rows[k]["ratio_to_white_0.85"] for k in rows), 3), round(max(ups), 3)]
    out["sodium"]["spectral_ratio_range_note"] = "from the fitted edges (lower) to the same pigments with the edge 12 nm bluer (upper): a box about a tenth to a quarter as bright as a white surface; Judgement, the curve's shape is assumed"
    return out



# ---------------------------------------------------------------------------------------------------------------
# 3. the document
# ---------------------------------------------------------------------------------------------------------------
def main():
    prof, segs, Rs = profile()
    col = colour_block()

    foot_d = 2 * V("foot_radius")
    cap_d = 2 * V("cap_radius")
    ap_half_angle = math.degrees(math.asin((V("aperture_width") / 2) / R_BODY))
    R_DOOR = R_BODY + V("door_proud")
    door_half_angle = math.degrees(math.asin(V("door_half_width") / R_DOOR))
    ap_z0 = V("aperture_centre_z") - V("aperture_height") / 2
    ap_z1 = V("aperture_centre_z") + V("aperture_height") / 2
    circumference = math.pi * 2 * R_BODY
    lt = V("lettering_area")
    cy = V("cypher_area")
    cf = V("collection_plate_frame")
    proj_area = round(V("body_diameter") / 1000 * H_TOTAL / 1000 + 0.05, 2)
    d = {}
    d["family"] = "pillar-box"
    d["title"] = "Quay Street's pillar box: the target (cloud week 42, 9 October 2026, second try)"
    d["written"] = "2026-10-09"
    d["revision"] = "second try, after TARGET-REVIEW.md (FAIL on F1, the height, and nine narrow points N1 to N9, all applied)"
    d["units"] = {"length": "millimetres in this file unless a key says metres (_m)", "glb": "metres, z up, scale 1",
                  "frame": "origin on the box's vertical axis at the footway surface; +y is the FRONT (the door and slot side); +x is to the viewer's right when looking at the front; z up",
                  "pivot": "the axis at the footway surface (z = 0): the pivot of the .glb; the hidden skirt runs to z = -150",
                  "kinds": "Read (printed in the repository), Derived (computed), Judgement (the writer's choice; basis 'Memory' where it rests on general knowledge of the type). Scaled and Photo are EMPTY: no drawing and no photograph of a pillar box was reached."}
    d["summary_line"] = ("Quay Street's pillar box is a cast-iron cylinder of the 1950s-60s standard 'Type A' pattern, painted pillar-box red (sRGB 150/30/32) above a black base band 200 mm high: "
                         "body 489 mm across, a 576 mm foot, a 560 mm cap with a shallow 80 mm dome, 1500 mm above the footway in all (the research's working figure; the stand-in's 1612 is 0.11 m too tall), "
                         "a 320 x 45 mm letter slot centred at 1278 mm under a 30 mm hood, a 300 x 888 mm door (flush: 1 mm proud, a joint groove round it, hinged on the left with no hinge showing; a keyhole escutcheon and one collection-plate frame) "
                         "and, where the cypher and the operator's lettering belong, FLUSH reserved areas with no raised or cut geometry (canon owes them): no cypher, crown, operator lettering or maker's mark, "
                         "the collection plate saying only COLLECTIONS, MON-FRI 5.30 PM, SAT 12 NOON, and the front facing the building line; "
                         "no photograph of a pillar box was reached, so no number is Photo-measured: every size is the repository's earlier figures (Read), derived from them, or the writer's judgement, and the first dated photograph overrides them.")
    d["no_photograph_measured"] = True
    d["decision_type"] = {
        "main": "Type A, 1950s-60s, cast iron, domed cap with a moulded rim, hooded aperture, a flush door; cypher, lettering and maker's mark reserved flush and blank",
        "variant": {"id": "type_k_capless", "build": False,
                    "why_a_variant_at_all": "the earlier research (Read) says the capless Type K was introduced on 31 July 1980 and made to about 2000, so a few were in the street in 1990 as new or replacement boxes; two search-summary leads (not numbers) give it the same 19 1/4 in width",
                    "why_not_built": "the street needs one box; the research's own recommendation is the older Type A; and the evidence for the Type K's shape is two search summaries and no photograph, so no profile is offered beyond the coarse one below",
                    "coarse_profile_rz": [[288, -150], [288, 0], [288, 48], [262, 72], [244.5, 140], [244.5, 1418], [236, 1458], [150, 1490], [0, 1500]],
                    "differences": "no separate cap or overhanging rim; a flush rounded crown; the aperture set in a shallow recess rather than under a hood; the same 489 mm body and about the same height (Judgement; lead only)"},
        "reasons_for_main": [
            "1990 on a Victorian port quarter: the stock is the older cast-iron standard boxes, not the 1980 capless replacement (the research says so, and recommends a 1950s-60s Type A: Read)",
            "the stand-in already has a cap and a dome, so the silhouette the street was blocked with is the Type A's",
            "the Type A's cap, hooded slot, door and plate give the sheet four things to show at the camera's 1.6 m; the capless box has fewer",
            "the postal cypher and the operator lettering are what canon owes: on a Type A they have clear places to stay reserved and flush (a band, a disc); on a capless box they are cast into the aperture plate"]}
    d["frame_numbers"] = {
        "scene": {"x_m": V("scene_x"), "side": "east", "axis_setback_from_kerb_back_m": V("scene_setback"),
                  "front_faces": "the building line: the east (shop) side, away from the carriageway (review N6)",
                  "front_direction_in_scene": "+z on the east side (toward the shops); the stand-in's slot is on the road side (StreetVignette.cs PillarBox: z - sgn x 0.48 x d, Read), so the kit piece is turned 180 degrees about the vertical against the stand-in",
                  "reason": "the foot stands 312 mm from the kerb's back, so a road-facing slot would put the poster on the kerb edge or in the channel; a kerbside box on a 2 m footway faces the footway or along it; the player walks the footway and would otherwise see the box's plain back. Judgement (the reviewer's); the scene's road side is a Read figure against it: the scene owner is told (handover) and, if the road side is kept, records why",
                  "kind": "Judgement against a Read"},
        "footway": {"flags_at_kerb_back_above_channel": V("flag_level_above_channel"), "kerb_top_above_channel": V("kerb_top_above_channel"),
                    "fall_toward_road": V("scene_footway_crossfall"), "footway_at_axis_above_channel": V("footway_at_axis_above_channel"),
                    "fall_across_the_foot": V("footway_fall_across_foot"), "kind": "Read / Derived (REG)"},
        "clear_footway_past_box_mm": {"value": round(V("scene_footway_width") - V("scene_setback") * 1000 - V("foot_radius")), "kind": "Derived",
                                      "note": "2000 - 600 - 288 = 1112 if 'the setback' is to the axis (the scene's code); 0.6 m to the NEAREST edge would put the axis at 888 and leave 824 (see could_not_settle)"},
        "nearest_lamp_column": {"x_m": V("scene_lamp_column_x_east"), "side": "east", "gap_to_box_axis_m": round(V("scene_lamp_column_x_east") - V("scene_x"), 2), "kind": "Derived",
                                "note": "the scene's east column at x = 28.0 stands 1.0 m from the box on the same setback: the lantern (5 m up, 0.5 m out) lights the cap from above and at night the box is the street's nearest object to a sodium lamp"}}
    d["overall"] = {"total_height": H_TOTAL, "height_over_body_width": round(H_TOTAL / V("body_diameter"), 2), "body_diameter": V("body_diameter"), "foot_diameter": foot_d, "cap_diameter": cap_d,
                    "aperture_centre_z": V("aperture_centre_z"), "hidden_skirt": V("hidden_skirt"), "body_circumference": round(circumference, 1),
                    "upper_alternative_total_height": {"value": V("upper_alternative_height"), "why": "the research's untraced Type A, 5 ft 4 in tall (and 1 ft 7 1/4 in wide); the scene's stand-in (1612) agrees; a photograph settles 1500 against 1626"},
                    "lower_range_not_used": {"value_mm": V("research_visible_range_cm"), "why": "the 73 in listing less 15 to 20 in buried is a casting's length, and a lead sells that box as the narrow Type B; the research's own Type A figures are 150 cm and 5 ft 4 in"},
                    "stand_in_for_comparison": {"body_diameter": V("scene_body_diameter"), "total_height": V("scene_body_height") + V("scene_cap_height") + V("scene_dome_height"),
                                                "too_tall_by_mm": V("scene_body_height") + V("scene_cap_height") + V("scene_dome_height") - H_TOTAL, "cap_diameter": V("scene_cap_diameter")}}
    d["profile"] = {"note": "outer surface of the lathe, (radius, z) in mm, from the foot of the hidden skirt up to the apex; revolve about the axis. Hard edges get the bevels in `bevels`. The features that are not bodies of revolution (slot, hood, sill, door, escutcheon, plate frame) are in `parts`.",
                    "outer_rz": prof, "segments": segs, "dome": {"sphere_radius": round(Rs, 2), "sagitta": V("dome_sagitta"), "chord_radius": V("cap_shoulder_radius"), "apex_z": H_TOTAL},
                    "wall_thickness": V("wall_thickness"), "inner_offset": "the inside is the outer profile offset 12 mm inward, closed at z = -138 (for the section drawing; a closed solid is acceptable to the build apart from the slot)"}
    d["bevels"] = [{"edge": "cap rim top and bottom lips", "radius": 1.5}, {"edge": "foot band bottom", "radius": 2.0}, {"edge": "door perimeter (outer)", "radius": 1.0},
                   {"edge": "hood front lip", "radius": 2.0}, {"edge": "plate frame bezel (outer)", "radius": 1.5}, {"edge": "slot lips", "radius": 1.0}]
    d["parts"] = {
        "foot_plinth": {"what": "the foot: a 48 mm vertical band at r 288 with a 12 mm quarter-round, a 45 degree splay and a cove into the body; the casting continues some 15 to 20 in deeper (the research); 150 mm of it is modelled as a hidden skirt", "z0": 0, "z1": V("foot_cove_top_z"),
                        "radius": V("foot_radius"), "diameter": foot_d, "set_in_footway": {
                            "datum": "z = 0 is the footway surface at the box's axis",
                            "hidden_skirt": "profile segment buried_skirt to z = -150 so no gap shows where paving dips",
                            "fillet": {"width_mm": V("base_fillet")["width"], "height_mm": V("base_fillet")["height"], "colour_srgb": V("base_fillet")["colour_srgb"],
                                       "how": "an irregular ring of dark bitumen and mortar, 15 to 35 mm wide, 10 mm high at the foot, feathered to nothing on the paving; wider on the uphill (building) side because the footway falls 14 mm across the foot while the box stands vertical",
                                       "kind": "Judgement"},
                            "paving_cut": "the flags are cut to a rough round, 20 to 60 mm from the foot, with a 5 to 12 mm gap the fillet covers (the footway family owns the flags)"}},
        "body": {"what": "plain cylinder with a sand-cast surface", "z0": V("foot_cove_top_z"), "z1": V("cap_soffit_z"), "radius": R_BODY,
                 "surface": {"sand_cast_bump_mm": 0.3, "wavelength_mm": 4.0, "kind": "Judgement (normal map; no photograph)", "casting_seam": "a 0.5 mm raised seam line down the back (x = 0, y < 0), where the two mould halves met"}},
        "cap": {"what": "the cap: an under-moulding (cove) from the body to a 280 rim, a vertical rim, a quarter-round bead, a flat shelf, a short neck and the shallow dome. The rim is the outermost line above the foot; the hood tucks inside it.",
                "soffit_z": V("cap_soffit_z"), "rim_radius": V("cap_radius"), "rim_diameter": cap_d, "rim_proud_of_body": V("cap_radius") - R_BODY, "rim_z": [V("cap_soffit_z") + V("cap_cove_height"), V("cap_rim_top_z")],
                "dome_base_z": V("dome_base_z"), "apex_z": H_TOTAL, "sagitta": V("dome_sagitta"), "sphere_radius": round(Rs, 2),
                "finial": "none (no boss, no ring): the earlier research names none (Read) and no photograph shows one"},
        "aperture": {"slot": {"x0": -V("aperture_width") / 2, "x1": V("aperture_width") / 2, "z0": ap_z0, "z1": ap_z1, "width": V("aperture_width"), "height": V("aperture_height"),
                              "centre_z": V("aperture_centre_z"), "corner_radius": V("aperture_corner_radius"), "half_angle_deg": round(ap_half_angle, 1),
                              "through": "yes: through the 12 mm wall into a black interior (albedo 8/8/8, roughness 0.9)", "kind": "size Read (the scene's 320 x 45); centre Derived (the scene's 1150 + 128)"},
                     "hood": {"what": "a curved lip wrapped round the front above the slot", "z0": V("hood_z_bottom"), "front_top_z": V("hood_front_top_z"), "top_z": V("hood_top_z"),
                              "outer_radius": R_BODY + V("hood_projection"), "projection": V("hood_projection"), "half_angle_deg": V("hood_half_angle"),
                              "section_rz": [[R_BODY, V("hood_z_bottom")], [R_BODY + V("hood_projection"), V("hood_z_bottom")], [R_BODY + V("hood_projection"), V("hood_front_top_z")], [R_BODY, V("hood_top_z")]],
                              "cheeks": "radial planes at +-48 degrees, square", "gap_to_cap_soffit": V("cap_soffit_z") - V("hood_top_z"),
                              "inside_the_cap_rim_by": V("cap_radius") - (R_BODY + V("hood_projection"))},
                     "sill": {"what": "a lip under the slot", "section_rz": [[R_BODY, V("sill_z_bottom")], [R_BODY + V("sill_projection"), V("sill_z_bottom") + V("sill_projection")], [R_BODY + V("sill_projection"), ap_z0], [R_BODY, ap_z0]],
                              "projection": V("sill_projection"), "half_angle_deg": V("sill_half_angle")},
                     "flap": V("flap")},
        "door": {"x0": -V("door_half_width"), "x1": V("door_half_width"), "z0": V("door_z_bottom"), "z1": V("door_z_top"), "width": 2 * V("door_half_width"), "height": V("door_z_top") - V("door_z_bottom"),
                 "half_angle_deg": round(door_half_angle, 1), "outer_radius": R_DOOR, "proud": V("door_proud"), "corner_radius": V("door_corner_radius"),
                 "placement": "a flush door concentric with the body: a cylindrical panel of outer radius 245.5 (1 mm proud of the body's 244.5), 300 wide as a chord (half angle 37.0 degrees), z 280 to 1168; only the 3 x 3 joint groove round it shows it",
                 "joint_groove": V("door_groove"), "hinged": "on the left as seen from the front, as the side of the joint only: the hinges are INTERNAL (a knocked-out pin must not open the box), so no knuckle, pin or strap shows; no part on the door's left edge stands more than 1.5 mm proud of the door face",
                 "face": "plain, sand-cast, a thick-painted bead along its edges",
                 "lock": V("lock")},
        "panels": {"reserved_for_lettering": {**lt, "note": "FLUSH: no raised or cut geometry (relief 0 within the area, measured radially above the body's own curved face). The minted lettering is cast here once canon supplies it."},
                   "reserved_for_cypher": {**cy, "note": "FLUSH: no raised or cut geometry (relief 0 within the area, measured radially above the door's own curved face). The minted cypher is cast here once canon supplies it."},
                   "note": "a real box carries its cypher and lettering as raised letters directly on the iron: it has no blank disc and no blank tablet (review N5). Canon owes the postal cypher and the operator's name; the box is correct and incomplete."},
        "plates": {"collection_frame": V("collection_plate_frame"),
                   "collection_plate": {"window_w": cf["outer_w"] - 2 * cf["bezel"], "window_h": cf["outer_h"] - 2 * cf["bezel"],
                                        "face": "white vitreous enamel (232,229,218), roughness 0.12, thin black border line 2 mm inset 4 mm", "text_colour_srgb": [22, 22, 24],
                                        "text": [{"string": "COLLECTIONS", "cap_height": 11, "align": "centre", "from_top": 14, "weight": "bold"},
                                                 {"rule": "a 1.5 mm black rule under the heading, 24 mm from the top, inset 14 mm each side"},
                                                 {"string": "MON-FRI", "cap_height": 8, "align": "left", "inset": 14, "baseline_from_top": 52},
                                                 {"string": "5.30 PM", "cap_height": 8, "align": "right", "inset": 14, "baseline_from_top": 52},
                                                 {"string": "SAT", "cap_height": 8, "align": "left", "inset": 14, "baseline_from_top": 76},
                                                 {"string": "12 NOON", "cap_height": 8, "align": "right", "inset": 14, "baseline_from_top": 76}],
                                        "font": "any plain grotesque already in production/fonts (OFL); not a period-correct face, none is needed at 8 mm",
                                        "allowed_words": ["COLLECTIONS", "MON-FRI", "SAT", "5.30 PM", "12 NOON"]},
                   "enamel_plate": "none: the box carries ONE plate (review N5); a blank enamel plate in a frame reads as a placeholder",
                   "words_decision": {"on_the_object": ["COLLECTIONS", "MON-FRI", "SAT", "5.30 PM", "12 NOON"], "nowhere_else": "no other letters or numerals appear on the box",
                                      "why_safe": "they are the plain English words and times a collection plate needs; none names a company, brand, council, maker or reign, none is a cypher or a crown; 'POST OFFICE', 'ROYAL MAIL', 'LETTERS' on the slot, 'PO', 'GPO', 'ER' and any foundry name are NOT used. If the brand bible later wants zero lettering the text list is removed and the frame is removed with it (variant `no_plate`: a flush door; the self-check and the checks accept both)."}}}
    d["paint"] = {"red": {"srgb": V("red_srgb"), "name": "pillar-box red, a deep gloss red (the colour of the box above the black band)", "source": "kept from the wear target: Read",
                          "roughness_body": 0.35, "roughness_cap_top": 0.45, "metal": 0,
                          "roughness_words": "semi-gloss: a gloss enamel five to eight years after its last repaint, dulled and a little chalked on the top of the cap (0.45) and brighter on the vertical faces (0.35)",
                          "kind": "Judgement (roughness); Read (colour)"},
                  "black_base": {"srgb": V("black_srgb"), "top_z": V("black_band_top"), "height": V("black_band_top"), "roughness": 0.5, "metal": 0,
                                 "edge": "the line between black and red is a brush line, wavering +-3 mm, the red overlapping the black by 1 to 2 mm in places; it crosses the foot's cove and the lower body",
                                 "kind": "Read (the research: black, about 20 cm); a variant with no band is listed under variants"},
                  "plate_enamel": {"srgb": [232, 229, 218], "roughness": 0.12, "metal": 0},
                  "keyhole_shutter": {"srgb": V("red_srgb"), "metal": 0, "roughness": 0.35, "edge_srgb": V("lock")["shutter_edge_srgb"], "edge_width": V("lock")["shutter_edge_width"],
                                      "note": "painted with the door, worn to dark bare metal at its edge only (review N8: not bright brass); if a builder prefers brass it is Memory"},
                  "flap_and_interior": {"flap_srgb": V("flap")["colour_srgb"], "interior_srgb": [8, 8, 8]},
                  "colour_reading": col}
    d["wear"] = {
        "state": "tired: five to eight years since its last repaint, one tidy-up of the plate and the lock, no touch-up of the chips; the street is a port town's old quarter in a wet climate",
        "agrees_with_wear_target": {"surface": "pillar_box_red", "mark_srgb": V("wear_pillar_tone_mark"), "mask_kind": "iron_wear (unwrapped strip)", "uv_repeats_round_girth": V("repeat_count"),
                                    "repeat_width_mm": round(circumference / V("repeat_count"), 1), "repeat_rule": f"the 214 mm strip does not fit the {circumference:.0f} mm girth a whole number of times (7.2); an odd count cannot be mirrored closed, so 8 repeats of {circumference / 8:.0f} mm (the strip 10 % narrower), mirrored on alternate repeats, the seam at the back (x = 0, y < 0)",
                                    "height": "the mask runs from z = 0 up the 1500 mm of the box (the wear target's is 2.4 m; the lowest 0.3 m keeps its 40 % of the lost paint)",
                                    "share_of_area_lost": V("wear_share_box"), "typical_share": 0.04,
                                    "disagreement": "the wear target's 0.04 to 0.08 is the downpipe's; the box takes 0.03 to 0.06 (typical 0.04) because a box in service is touched up. The wear writer should accept or overrule.",
                                    "patch_eqd_mm": V("wear_patch_eqd"), "edge_mm": V("wear_edge_mm")},
        "layers_in_a_chip": {"description": "a chip shows the layers of the repaints: the top red, an older red, then primer or bare iron; chips are hard-edged with a thick paint bead (0.3 to 0.6 mm) round them",
                             "top_red_srgb": V("red_srgb"), "older_red_srgb": [112, 26, 30], "older_red_share": 0.5,
                             "grey_primer_srgb": [118, 112, 106], "bare_rusty_iron_srgb": [141, 102, 72], "rust_halo_srgb": [112, 56, 34],
                             "black_under_srgb": [35, 35, 36], "black_under_share_on_base_and_door": 0.2,
                             "mix_at_the_bottom_layer": {"grey_primer": 0.45, "rusty_iron": 0.4, "black": 0.15},
                             "kind": "Judgement; the tone mark 124/104/92 of the wear target is the mean of primer and rust",
                             "nearest_evidence": "a Poly Haven CC0 scan of a weathered red-painted container (rusty_painted_metal, published 2025): faded red 119/64/47 with run streaks that read 44/28/23 (a third of the red's luminance) over about 7 % of its area; a scan of a shipping container, NOT a pillar box, used only for how rust runs over red paint"},
        "chips_at_the_base": {"zone_z": [0, 400], "count": [14, 22], "eqd_mm": {"p10": 3, "p50": 9, "p90": 25}, "share_below_300_mm": 0.7,
                              "foot_top_edge_scuff": "the quarter-round on the foot top (z 48 to 60) is worn to bare iron over 30 % of the circumference, a band 10 to 14 mm wide, colour 96/84/76, strongest on the road side (the back: kerb-side knocks from wheels and bags)",
                              "kerb_side_scrape": {"z": [380, 520], "length_mm": 180, "height_mm": [20, 40], "bare_share": 0.15, "side": "the road side (the back, 180 degrees from the front, which faces the shops)"}},
        "chips_at_the_aperture": {"hood_lower_front_edge": {"share_of_edge": 0.4, "chip_eqd_mm": [2, 10], "rust_halo": True},
                                  "sill_lip": {"bare_band_mm": 10, "share_of_length": 0.6, "colour_srgb": [80, 76, 72], "note": "letters scrape the lip bright; a dull dark iron band, not shiny"},
                                  "slot_interior": "black; a faint pale line where the flap's lip catches the light",
                                  "micro_chips": {"count": [30, 60], "eqd_mm": [2, 8], "on": "door perimeter, hood edge, sill edge, cap rim lips, foot top edge, the keyhole shutter's edge"}},
        "rust_bleed": {"sources": ["every chip below 400 mm", "the cap's under-moulding joint (z 1343)", "the hood's underside, one trickle under its LEFT end", "the foot top edge"],
                       "trickle": {"width_mm": [5, 10, 20], "length_mm": [80, 200, 350], "per_source": [1, 2], "colour_on_red_srgb": [84, 40, 26], "edge_10_90_mm": [8, 25],
                                   "head": "a dark dot at the source 3 to 10 mm and a 15 to 40 mm brown halo", "drops": {"count": [0, 2], "eqd_mm": [20, 60]}},
                       "kind": "Judgement; widths from the wear target's rust_bleed (Photo M14, a wall, not iron)"},
        "flyposting_traces": {"patches": {"count": [1, 2], "size_mm": [[150, 260], [120, 300]], "z_centre": [600, 900], "where": "on the sides and back, 70 to 140 degrees round from the front (never on the door, the plate, the lock, the slot or the hood)",
                                          "intact_share": [0.2, 0.6], "paper_srgb": V("wear_poster_paper_mark"), "paste_ghost_mm": [10, 30], "edges": "torn on the diagonal, 2 to 10 mm hard edge", "content": "unreadable remnants; nothing that shows a word, a face, a drink or a wager"},
                              "stickers": {"count": [0, 3], "size_mm": [40, 100], "z": [300, 1100], "same_exclusions": True},
                              "cross_reference": "the scene's G5 sticker decal (0.15 x 0.15 m on the street face at 0.15 m up) sits on the box's road side, which is now the back: keep it there, clear of the door"},
        "grime": {"ground_up": {"levels_mm_strength": V("wear_splash_levels"), "darkening_at_full_strength_multiplier_linear": 0.62, "note": "the wear target's foot-splash envelope (full to 240, half at 450, gone by 750) applied to the box: multiplier = 1 - 0.38 x level on the red; the black band takes 0.8 x level"},
                  "soot_under_the_cap": {"zone_z": [1318, 1343], "multiplier_linear": 0.7},
                  "rain_streaks_from_the_cap_rim": {"count": [5, 9], "width_mm": [10, 30], "length_mm": [100, 350], "effect": "a cleaner, brighter streak (x 1.12) down a dirtier ground (the cap's overhang protects what is under it)"},
                  "bird_droppings_on_the_dome": {"count": [1, 3], "eqd_mm": [30, 120], "colour_srgb": V("wear_bird_mark"), "runs": "0 to 1 run of 10 to 30 mm wide, 50 to 300 long down the cap rim", "place": "the dome's top and the rim; the quay end gets more (the box stands at x 27: weight 0.4)"},
                  "chalking": {"where": "the top of the dome and the cap rim's upper face", "effect": "lighter and a little pink, x 1.08 in linear light, roughness 0.45"}},
        "dents": {"count": [1, 2], "eqd_mm": [30, 60], "depth_mm": [1, 2], "z": [300, 700], "kind": "Judgement"},
        "first_look_at_1p6_m": "from the game camera the eye should read: a red cylinder as tall as a man's shoulder, a dark grimy foot and black band, three or four orange-brown chip clusters low down, one dark rust trickle under the hood's left end, a torn paper remnant on the side, the bright white plate, the black slot"}
    d["variants"] = {"count_needed": 1, "list": [
        {"id": "main", "build": True, "description": "Type A, red body, black band, tired wear, the collection plate lettered with the five allowed strings"},
        {"id": "no_black_band", "build": False, "description": "all red to the ground (a repaint that skipped the base); the black band's top z = 0; the evidence for the band in 1990 is the research's Read plus leads that a red-and-black-base livery was stipulated long before", "kind": "Judgement"},
        {"id": "type_k_capless", "build": False, "description": "see decision_type.variant"},
        {"id": "no_plate", "build": True, "description": "no plate and no frame (a flush door), if canon wants no lettering at all: delete the collection frame and its plate; the reserved areas are unchanged"}]}
    d["materials"] = {"red_paint": d["paint"]["red"], "black_paint": d["paint"]["black_base"], "enamel": d["paint"]["plate_enamel"], "keyhole_shutter": d["paint"]["keyhole_shutter"],
                      "bare_iron_and_rust": {"srgb": [141, 102, 72], "primer_srgb": [118, 112, 106], "roughness": 0.65, "metal": 0.3, "metal_note": "bare iron is metal 1 but a rust skin is a dielectric; 0.3 on a chip that is mostly rust, 1.0 only on the bright sill band"},
                      "bitumen_fillet": {"srgb": V("base_fillet")["colour_srgb"], "roughness": 0.9, "metal": 0}}
    d["bevels_note"] = "every hard edge is bevelled (mid-poly, bevel on every edge: the asset plan's method, Read); the radii are in `bevels`"
    d["triangle_budget"] = {"lod0": [8000, 30000], "kind": "Judgement: the asset plan's mid-poly with a bevel on every edge (Read); the box fills at most 1 % of a frame beyond 8 m"}
    d["accent_budget"] = {"note": "art-direction R-B4: the red boxes are the street's whole high-chroma accent; the frame's pixels above saturation 0.6 must be non-zero and under 0.078",
                          "saturation_of_the_red": col["hsv"]["s"], "projected_area_m2": proj_area,
                          "share_of_a_2560x1440_frame": {f"at_{dd}_m": round(proj_area * (1440 / (2 * dd * math.tan(math.radians(23)))) ** 2 / (2560 * 1440), 4) for dd in (5, 8, 12)},
                          "kind": "Derived: area x (1440 / (2 d tan 23 degrees))^2 / 3.686 Mpx",
                          "wet_note": "the sky's reflection lowers saturation on the cap's top and the highest bright patches to about 0.6 to 0.7; the body's vertical faces stay at 0.75 to 0.8"}
    d["photographs_win"] = {
        "applies": False,
        "why": "no photograph of a pillar box was reached, so no photograph overrides anything. The disagreements below are between the repository's own figures (and the reviewer's judgement); each says what was chosen.",
        "disagreements": [
            {"item": "body width", "a": "the scene 597 (a trade guess)", "b": "the research 49 cm / 19 1/4 in (untraced) and 19 in (a c.1955 listing)", "chosen": "489 for the body; the scene's 597 is read as the foot (576 chosen)"},
            {"item": "height", "a": "the first draft's 1372 (the scene's BODY figure read as the whole box, and the 73 in listing's 135 to 147 cm)", "b": "the research's working figure 150 cm ('the top is at about 150 cm'), its Type A line 5 ft 4 in (1626), the scene's own stand-in 1612", "chosen": "1500 (Read: the research's working figure); 1626 recorded as the upper alternative; 1350 to 1470 is a casting's length (a lead says a Type B's) and is not used; the stand-in is 0.11 m too tall"},
            {"item": "cap width", "a": "the scene 660 (1.35 x the body)", "b": "the research: the rim is 'a few centimetres proud of the body'", "chosen": "560 (35.5 proud), the outermost line above the foot; the hood tucks 5.5 inside it"},
            {"item": "dome rise", "a": "the scene 140", "b": "none", "chosen": "80 (rise / diameter 0.14 on the 560 cap)"},
            {"item": "door", "a": "the research: 'a flush panel with the cast cipher, a plate frame and a keyhole'", "b": "the first draft: 4 proud with hinges", "chosen": "1 proud (outer radius 245.5), a 3 x 3 joint groove showing the door; no hinge shows (internal hinges); the research is Read, the hinges were an invention"},
            {"item": "facing", "a": "the scene: the slot on the road side (StreetVignette.cs PillarBox, Read)", "b": "the review (Judgement): a kerbside box on a 2 m footway faces the footway; the poster must not stand on the kerb edge, and the player walks the footway", "chosen": "the building line (toward the shops); the scene owner is told and, if the road side is kept, records why"},
            {"item": "aperture", "a": "the scene 320 x 45 at 1150", "b": "a search lead: an aperture widening in 1957 (6 1/4 to 8 in); unclear which dimension; the research: 'just under the cap'", "chosen": "320 x 45 kept (Read); the centre moves up with the cap to 1278"},
            {"item": "red", "a": "the wear target 150/30/32", "b": "BS 381C 538 or 539 (a search lead from hobbyist and heritage pages: 538 to about 1968, 539 after)", "chosen": "150/30/32 kept: the lead gives a shade name, not an sRGB"},
            {"item": "black band height", "a": "the research about 200", "b": "a lead: about 6 in (152) showing when a reclamation firm sets a box", "chosen": "200"},
            {"item": "iron_wear share", "a": "the wear target 4 to 8 % (a downpipe)", "b": "this target 3 to 6 %", "chosen": "3 to 6 %, typical 4 % (the wear writer to confirm)"}]}
    d["to_read_when_the_network_opens"] = [
        "dated photographs, 1975 to 2000, of Type A and Type B boxes of the 1950s-60s on provincial British streets, front, side and three-quarter, with a person or a kerb in frame for scale (Geograph, Wikimedia Commons categories of UK pillar boxes, Flickr archives of the 1980s, local archives such as Leodis, Picture Sheffield, Tyne and Wear and Hull History Centre); the one photograph that settles most is a dated, square-on front view of a Type A of the 1950s-60s with the kerb's 125 mm upstand or a standing person in frame, camera about 1 m up and 4 to 6 m away",
        "the Letter Box Study Group's type records: Type A and Type K entries (heights, widths, the order of cypher, lettering and plates, apertures by date), and its notes on how the aperture changed in 1957",
        "Royal Mail's and the Postal Museum's archives: repaint and paint specifications of the 1980s (the base band's height, the exact red), drawings of the standard boxes, the dimensions of the A and B castings",
        "Historic England and Cadw listing records for listed Type A boxes (some give measured sizes)",
        "a measured visit: a real Type A on a street near the PC, with a tape and a scale rod (the PC has the network the cloud lacks)",
        "dated photographs of the Type K as new in the 1980s, to decide whether it needs a second variant"]
    d["unreached"] = [
        {"what": "Wikipedia, Wikimedia Commons, Geograph, Flickr, archive.org, Sketchfab, the Letter Box Study Group (lbsg.org), postboxmap.co.uk, the Postal Museum, Europeana, the National Archives, Historic England, British Pathe, Library of Congress, Internet Archive, Gutenberg, the British Library, the Open Verse API", "result": "refused or no connection (curl status 000) from this cloud on 9 October 2026 (the reviewer found the same for six of them)", "used": "nothing"},
        {"what": "ambientCG (catalogue API answered; searches for 'postbox', 'mailbox' and 'pillar box' returned nothing; downloads refused in earlier targets)", "result": "no pillar box asset", "used": "nothing"},
        {"what": "GitHub search (the API refuses searches outside the session's repositories)", "result": "403", "used": "nothing"},
        {"what": "WebSearch result summaries (9 October 2026): leads only, listed in `leads`", "result": "summaries", "used": "to corroborate, never as a number"}]
    d["leads"] = [
        {"text": "a salvage dealer's listing of a Carron Elizabeth II box: 73 in tall, about 20 in in the ground, body 15 in wide (also called PB42/2 Type B, circa 1966)", "via": "WebSearch summary of ukaa.com", "use": "the 73 in casting is, by this lead, a Type B's: it is NOT used for the Type A's height (review F1)"},
        {"text": "the Letter Box Study Group lists a 1937 Type B at 64 in high and 48 in in circumference (15.3 in across)", "via": "WebSearch summary citing lbsg.org and a Scottish heritage listing", "use": "tells the narrow Type B (about 15 in) from the wider Type A (about 19 in): the 19 1/4 in body of this target is the A"},
        {"text": "the Letter Box Study Group's Type K record: cast iron, 63 in high, 19 1/4 in wide, introduced 1980; five foundries cast it", "via": "WebSearch summary of lbsg.org", "use": "the Type K variant's width; the Type A's width has the same 19 1/4 in; its 63 in (1600) agrees with a total near 1.5 to 1.6 m"},
        {"text": "OSM wiki: the larger Type A box has a circumference of about 60 in (19.1 in across)", "via": "WebSearch summary", "use": "corroborates 489"},
        {"text": "BS 381C 538 (to about 1968) and 539 (after) as the box reds; the shades renamed Cherry and Currant about 1988 (hobbyist source)", "via": "WebSearch summary", "use": "a colour NAME for the review; no sRGB taken"},
        {"text": "red with a black base stipulated in 1874; a listed box of 1936 'painted red with black base'; wartime boxes with a white base", "via": "WebSearch summaries of a Jersey heritage report and a listed-building record", "use": "supports the black band as the long-standing livery"},
        {"text": "a 1957 widening of the aperture (6 1/4 to 8 in) for C4 envelopes", "via": "WebSearch summary of an Oxford history page", "use": "none: it is unclear which dimension; the scene's 320 x 45 kept"},
        {"text": "a Type K has a slightly recessed aperture and no separate domed top; an angled notice plate and a rotary collection dial", "via": "WebSearch summary of uknature.co.uk", "use": "the variant's description only"}]
    d["panorama_search"] = {
        "method": "every British panorama listed by api.polyhaven.com/assets?type=hdris with coordinates in Britain was downloaded as its tone-mapped JPG (every one is 8192 px wide) and searched twice: (1) saturated-red blob detection on a 4096 px reduction (hue within 30 degrees of red, saturation above 0.68, value above 0.30), then every blob over 80 px was looked at as a rectilinear crop; (2) eight rectilinear views at 72 degrees across each street panorama, looked at by eye. Script: scan_panoramas.py. The reviewer re-ran a looser search (saturation above 0.45, value above 0.12, 40 px) on three of them and found no pillar box either.",
        "catalogue": {"hdris_listed": 997, "with_coordinates": 732, "without_coordinates": 265, "source": "api.polyhaven.com/assets?type=hdris on 9 October 2026 (the writer's count of 997; the review's 732 with coordinates, so 265 without)", "tone_mapped_jpg_width_px": 8192},
        "searched": ["adams_place_bridge", "bethnal_green_entrance", "birbeck_street_underpass", "cambridge", "canary_wharf", "epping_forest_01", "epping_forest_02", "greenwich_park", "greenwich_park_02", "greenwich_park_03", "leadenhall_market (red blobs only: a covered market's painted shopfronts)", "limehouse", "roof_garden", "urban_street_01", "urban_street_02", "urban_street_03", "urban_street_04"],
        "left_out": ["docklands_01, docklands_02 and the other 2025 Poly Haven panoramas at 53.3 N, 6.2 W: Dublin, where boxes are green and Irish", "st_fagans_interior (Wales, an interior)", "the 265 Poly Haven panoramas with no coordinates (none labelled British; a pillar box abroad is not a British one)"],
        "result": "NO PILLAR BOX in any of them. Every saturated-red blob was a tail light, a brick wall, a painted shopfront, a refuse bin or a sign. Poly Haven's 521 CC0 models include no pillar box, post box or letter box; its textures include none; ambientCG's catalogue has none.",
        "red_blobs_checked": {"urban_street_01": "tail lights and brick", "urban_street_02": "a purple bin, brick, an orange barrier", "urban_street_03": "tail lights of two parked cars, a brick wall", "bethnal_green_entrance": "brick piers, graffiti", "canary_wharf": "a lit ticker sign", "limehouse": "brick courses", "leadenhall_market": "painted shopfronts"}}
    d["could_not_settle"] = [
        "whether a Type A of the 1950s-60s stands 1500 above the footway (the research's working figure, kept) or up to 1626 (5 ft 4 in, the research's untraced Type A line): a photograph beside a kerb (125) or a person settles it in a minute; read it FIRST",
        "the slot's width: 320 is 65 % of the body's width (Read, the scene's); the reviewer's judgement is that a 1950s-60s Type A's slot is nearer half the body's width; read it SECOND, after the height",
        "the real order and positions on the front of the cypher, the operator lettering, the collection plate and the lock; the reserved areas and the frame are placed by the writer's general knowledge (basis Memory) and each may be 40 mm or more out",
        "the shape of the cap's moulding, the dome's rise (80 against the scene's 140) and the 30 mm neck, whether a finial or boss exists, and the hood's depth: not to be moved without a photograph",
        "whether the front faces the building line (this target's choice, the reviewer's) or the carriageway (the scene's stand-in), and which side the door's joint is on",
        "whether '0.6 m back from the kerb' is to the axis (the scene's code; kept) or to the nearest edge: it moves the box 0.29 m and the clear footway from 1112 to 824 mm",
        "the exact 1990 red: pillar-box reds were BS 381C 538 or 539 (a lead); the sRGB 150/30/32 is the wear target's guess, kept, and is checked against the accent budget not against a paint chip",
        "the base band's height (200 Read; 152 as a lead) and whether a 1990 repaint kept it",
        "the Type K as a second variant: only worth writing once a dated photograph shows one in a street like this",
        "a 'next collection' number tablet or rotary dial: not modelled (the research: uncertain)",
        "the red's reflectance at 589 nm (6.5 of TARGET.md): a fitted edge gives 0.08, a bluer edge 0.12 to 0.20; a spectrum of the real paint would settle it"]
    d["handover"] = {
        "for_scene_file": "furniture E4: replace body 0.597 / 1.372, cap 0.660 x 0.100 and dome 0.140 with the kit piece (total height 1.500, foot 0.576, body 0.489, cap 0.560); its pivot is the axis at the footway; the stand-in (1.612 in all) was 0.11 m too tall. THE FRONT (door, slot, plate) FACES THE BUILDING LINE, 180 degrees from the stand-in, whose slot is on the road side (StreetVignette.cs PillarBox): tell the scene owner; if the road side is kept, record why",
        "for_kerbs_and_footway": "the footway stands at +125 above the channel at the box's axis (110 at the kerb back, +15 for the fall); the box stands vertical on it; the flags are cut round the foot with a fillet (see parts.foot_plinth.set_in_footway)",
        "for_wear": "pillar_box_red keeps 150/30/32; iron_wear strip: 8 repeats of 192 mm round the 1536 mm girth, not the 7.2 of the 214 strip; the share 0.03 to 0.06 (typical 0.04); the mask runs from the footway to 1500; the foot-splash envelope applies from the footway; the road side is the back",
        "for_lighting": "the east lamp column stands at x = 28.0, 1.0 m from the box on the same line: expect the cap's dome and rim lit from above; at night under the 589 nm lantern the red box reads dark (about a tenth to a quarter as bright as a white surface), not red: the accent budget at night is the lamp's and the lit windows' (section 6 of TARGET.md)",
        "for_NOW_md": "Pillar box target (unit 3.6/3.7 family), second try: NO photograph of a pillar box was reached; Type A, 1500 above the footway (the research's working figure; 1626 the upper alternative), body 489, foot 576, cap 560, red 150/30/32 over a 200 black band, flush reserved areas for the cypher and the lettering, one collection plate with only COLLECTIONS / MON-FRI 5.30 PM / SAT 12 NOON, the front toward the shops; the first dated photograph overrides every size."}
    d["checks"] = checks(prof)
    d["numbers"] = REG
    d["number_kinds"] = {"registry": "pb_numbers.py REG, copied whole into `numbers`", "counts": count_kinds(),
                         "photo_numbers": 0, "scaled_numbers": 0}
    d["self_check"] = {"note": "written by self_check.py"}
    path = os.path.join(HERE, "target.json")
    if os.path.exists(path):
        try:
            old = json.load(open(path))
            if "self_check" in old and "result_line" in old["self_check"]:
                d["self_check"] = old["self_check"]
        except Exception:
            pass
    json.dump(d, open(path, "w"), indent=1, ensure_ascii=False)
    print("wrote", path, "bytes", os.path.getsize(path))


def count_kinds():
    c = {}
    for k, v in REG.items():
        c[v["kind"]] = c.get(v["kind"], 0) + 1
    return c


def checks(prof):
    ck = []

    def add(name, applies, measure, expected, tol, kind):
        ck.append({"name": name, "applies_to": applies, "measure": measure, "expected": expected, "tolerance": tol, "kind": kind})
    H = H_TOTAL
    lt = V("lettering_area"); cy = V("cypher_area"); cf = V("collection_plate_frame"); lk = V("lock")
    soff = V("cap_soffit_z")
    rim0 = soff + V("cap_cove_height")
    add("total_height", "whole piece", "max z of the visible mesh above the footway datum (z = 0 at the axis), in mm", H, 15, "Read (the research's working figure, 150 cm)")
    add("pivot_and_datum", "whole piece", "the pivot (origin) lies on the axis at z = 0 and the lowest vertex lies between z = -160 and z = -100", {"origin_xy_mm": [0, 0], "lowest_z_range": [-160, -100]}, 3, "Read (brief: pivot at the base's centre on the ground)")
    add("verticality", "whole piece", "angle between the axis and the vertical, degrees", 0.0, 0.3, "Derived (the box stands vertical on a footway that falls 14 mm across the foot)")
    add("profile_silhouette", "foot, body, cap, dome", "on the back half (y < 0, clear of the casting seam), the mesh's radius every 2 mm of z from 0 to the apex, against profile.outer_rz interpolated; largest absolute deviation, mm. A cap that is a plain disc, or a foot without its quarter-round, splay and cove, fails.", 0, 1.5, "Derived (the profile); 3.0 allowed within 2 mm of a bevelled edge")
    add("body_diameter", "body", "x extent of the horizontal section at z = 1000 (the door's edges lie inside it), mm", V("body_diameter"), 5, "Derived from Read (19 1/4 in)")
    add("foot_diameter", "foot", "maximum x extent in z 0 to 48, mm", 2 * V("foot_radius"), 6, "Judgement")
    add("cap_rim_diameter", "cap", f"maximum x extent in z {rim0:g} to {V('cap_rim_top_z'):g}, mm", 2 * V("cap_radius"), 6, "Judgement (the research: a few centimetres proud)")
    add("cap_soffit_height", "cap", "on the back half (y < 0): z at which the profile radius first exceeds the body radius by 1 mm (at the front the hood exceeds the body's radius from z 1300.5)", soff, 8, "Derived")
    add("dome_sagitta", "dome", "apex z minus the z of the dome's base circle (r 250), mm", V("dome_sagitta"), 6, "Judgement")
    add("dome_apex", "dome", "apex z, mm", H, 10, "Read (the research)")
    add("body_straight", "body", f"radius variation along z 140 to {soff:g} on the back half (cylinder: no taper), mm", 0.0, 2.0, "Judgement")
    add("aperture_width", "aperture", "chord width of the slot (x extent at its centre z), mm", V("aperture_width"), 6, "Read (scene)")
    add("aperture_height", "aperture", "slot height, mm", V("aperture_height"), 3, "Read (scene)")
    add("aperture_centre_z", "aperture", "z of the slot's centre, mm", V("aperture_centre_z"), 12, "Derived (the scene's 1150 + 128)")
    add("aperture_centred", "aperture", "x of the slot's centre, mm", 0.0, 5, "Judgement")
    add("aperture_through", "aperture", "a ray from the front through the slot centre along -y meets no surface for 100 mm (the slot is open into a dark interior)", True, None, "Read (scene had a box slot); Judgement")
    add("hood_projection", "hood", f"radius of the hood's front above the slot minus the body radius, at z {V('hood_z_bottom') + 10:g}, mm", V("hood_projection"), 4, "Judgement")
    add("hood_inside_cap_rim", "hood", "cap rim radius minus the hood's front radius, mm (the hood tucks inside the rim)", V("cap_radius") - (R_BODY + V("hood_projection")), 3, "Derived")
    add("hood_top_clear_of_cap", "hood", "cap soffit z minus hood top z, mm", soff - V("hood_top_z"), 6, "Derived")
    add("hood_span", "hood", "angular half-width of the hood, degrees", V("hood_half_angle"), 4, "Judgement")
    add("sill_lip", "sill", "radius of the sill front minus the body radius, mm", V("sill_projection"), 3, "Judgement")
    add("door_size", "door", "width (x extent of the door face) and height (z extent), mm", {"width": 2 * V("door_half_width"), "height": V("door_z_top") - V("door_z_bottom")}, {"width": 8, "height": 12}, "Judgement")
    add("door_bottom_z", "door", "z of the door's lower edge, mm", V("door_z_bottom"), 10, "Judgement")
    add("door_proud", "door", "door face radius minus body radius, mm", V("door_proud"), 1, "Judgement (the research: a flush panel, Read)")
    add("door_joint", "door", "width and depth of the groove round the door, mm", {"width": 3, "depth": 3}, 1.0, "Judgement")
    add("door_left_edge_flush", "door", "no part on the door's left edge (the joint side) stands more than 1.5 mm proud of the door face: no hinge knuckle, pin or strap is modelled", 1.5, None, "Judgement (internal hinges)")
    add("lock_place", "lock", "x and z of the escutcheon's centre, mm (on the side opposite the joint side)", {"x": lk["x"], "z": lk["z"]}, 10, "Judgement")
    add("lock_size", "lock", "escutcheon diameter and projection, mm", {"diameter": 36, "proud": 3}, {"diameter": 4, "proud": 1.5}, "Judgement")
    add("keyhole_shutter_paint", "lock", "the shutter's albedo is the door's red, metal 0, and only its edge (1 mm) is dark bare metal 60/52/46; no bright brass", {"srgb": V("red_srgb"), "metal": 0, "edge_srgb": [60, 52, 46]}, {"srgb": 6, "metal": 0.05}, "Judgement (review N8)")
    add("reserved_for_lettering", "reserved area", f"flush area {lt['x1'] - lt['x0']:g} x {lt['z1'] - lt['z0']:g}, centre z {(lt['z0'] + lt['z1']) / 2:g}: no geometry, relief measured radially above the body's own curved face (r 244.5) is 0 everywhere within it", {"width": 300, "height": 40, "cz": (lt["z0"] + lt["z1"]) / 2, "relief_max": 0}, {"size": 8, "cz": 8, "relief": 0.3}, "Judgement; canon (no operator lettering)")
    add("reserved_for_cypher", "reserved area", f"flush disc {cy['diameter']:g} across, centre z {cy['cz']:g} on the door's axis: no geometry, relief measured radially above the door's own curved face (r 245.5) is 0 everywhere within it", {"diameter": 110, "cz": cy["cz"], "relief_max": 0}, {"diameter": 6, "cz": 10, "relief": 0.3}, "Judgement; canon (the postal cypher is owed)")
    add("collection_frame", "collection plate frame", f"outer width x height {cf['outer_w']:g} x {cf['outer_h']:g}, centre z {cf['cz']:g}, bezel {cf['bezel']:g}, plate recess {cf['plate_recess']:g}, face plane y = {R_BODY + V('door_proud') + cf['bezel_proud_at_axis']:g}, mm", {"w": cf["outer_w"], "h": cf["outer_h"], "cz": cf["cz"], "bezel": cf["bezel"], "recess": cf["plate_recess"], "face_plane_y": R_BODY + V("door_proud") + cf["bezel_proud_at_axis"]}, {"size": 6, "cz": 10, "bezel": 2, "recess": 1, "face_plane_y": 2}, "Judgement")
    add("black_band", "paint", "z of the black-to-red line (median round the girth), mm", V("black_band_top"), 10, "Read (the research: about 20 cm)")
    add("black_band_colour", "paint", "median albedo sRGB of the band between z 20 and 180 on unworn paint", V("black_srgb"), 6, "Read (wear target iron_black)")
    add("red_albedo", "paint", f"median albedo sRGB of the body between z 400 and 1000 within 60 degrees of the front, wear marks excluded (per channel)", V("red_srgb"), 6, "Read (wear target pillar_box_red)")
    add("red_roughness", "paint", "median roughness of unworn red on the body, and on the dome's top", {"body": 0.35, "dome_top": 0.45}, 0.08, "Judgement")
    add("red_not_metal", "paint", "metallic of the painted surfaces", 0.0, 0.05, "Judgement")
    add("plate_words", "plate", "every string rendered on the box is one of COLLECTIONS, MON-FRI, SAT, 5.30 PM, 12 NOON (or the list is empty and the frame with it); nothing else is lettered anywhere on the piece or in its textures", ["COLLECTIONS", "MON-FRI", "SAT", "5.30 PM", "12 NOON"], None, "canon; brief (no real marks)")
    add("no_marks", "whole piece", "no cypher, crown, 'POST OFFICE', 'ROYAL MAIL', 'ER', 'GR', foundry name, date or registration number anywhere: count of such glyphs or relief features", 0, 0, "canon; brief")
    add("nothing_floats", "whole piece", "each part (hood, sill, door groove, escutcheon, plate frame) touches or overlaps the lathe body: smallest gap, mm", 0.0, 1.0, "Derived")
    add("clear_of_lamp_column", "placement", "gap between the foot and the east lamp column's base (x 28.0, base 200 across) along the footway, mm", round(1000 - V("foot_radius") - 100), 40, "Derived from Read (scene)")
    add("kerb_clearance", "placement", "distance from the back of the kerb to the nearest point of the foot, mm (axis 0.60 m behind the kerb back)", round(V("scene_setback") * 1000 - V("foot_radius")), 20, "Read / Derived")
    add("front_faces_footway", "placement", "angle of the slot's normal to the direction pointing at the buildings (away from the carriageway), degrees", 0.0, 10, "Judgement (review N6) against the scene's Read (the stand-in's slot is on the road side)")
    add("wear_share", "wear", "share of the body and foot area where paint is lost on the generated mask", V("wear_share_box"), None, "Judgement (the wear target's 4 to 8 % is the pipe's)")
    add("wear_uv_repeats", "wear", "number of mirrored repeats round the girth (even, the seam at the back)", V("repeat_count"), 0, "Derived")
    add("triangles", "whole piece", "triangle count of the LOD0 mesh", [8000, 30000], None, "Judgement")
    add("edge_bevels", "whole piece", "every hard edge of the bevels table has a radius of at least 1 mm", 1.0, None, "Read (asset plan: a bevel on every edge)")
    return ck


if __name__ == "__main__":
    main()
