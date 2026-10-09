"""Try 2: where the photographs win over target.json.

`apply(T)` returns a deep copy of the target with each departure written into it, and the list of departures
(what, the measurement, which photograph). build_door.py builds from the amended copy and check_door.py draws target_drawing.py's
reference from the same amended copy, so every other check still tests the build against the target and every departure is one named,
measured number. The list goes into the check's `adaptations` and into NOTES.md.

Measurements are on the preview copies of the two photographs (production/previews/cloud-week/refs/front-door/):
  P1  door-photo-01-teignmouth-four-panel-red.jpg      480 x 640,   5.15 to 5.19 mm a pixel on the door plane
  P2  door-photo-02-tottenham-six-panel-black.jpg      675 x 1200,  2.317 mm a pixel
"""
import copy
import math


def _arc(cp, cz, r, a0, a1, n):
    """Points (p, z) of an arc about (cp, cz) from angle a0 to a1 (degrees, measured from +p toward +z)."""
    return [(cp + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cz + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def weatherboard_profile():
    """(z up from the underside, p proud of the leaf face): a flat underside, a bull-nosed lower arris, a plain face
    sloping up and back at 30 degrees from the vertical (its normal tilts 30 degrees upward, so it sheds water and takes the sky), a small
    cove at z 52 and a rounded top roll that falls back onto the door at z 80."""
    pts = [(0.0, 0.0), (0.0, 21.0)]
    # the lower arris: a round of 5 mm, from heading +p (the underside) round to heading 120 degrees (up and back)
    r, ctr = 5.0, (21.0, 5.0)                                   # centre (p, z)
    arc = _arc(ctr[0], ctr[1], r, -90.0, 30.0, 8)               # from the underside round the nose to the slope's start
    pts += [(z, p) for p, z in arc[1:]]                         # (z, p) order
    p_end, z_end = arc[-1]
    # the face: up and back along (-sin30, +cos30) in (p, z) until z 44
    t = (44.0 - z_end) / math.cos(math.radians(30.0))
    pts.append((44.0, p_end - t * math.sin(math.radians(30.0))))
    # the cove at the foot of the roll: a concave round of 6 mm
    pf = pts[-1][1]
    pts += [(48.0, pf - 1.0), (52.0, pf - 1.2)]
    # the top roll: centre (p 4.2, z 67), radius 10.5 -- from the cove up over and back to the door at z 80
    pts += [(z, p) for p, z in _arc(4.2, 67.0, 10.5, -100.0, 100.0, 16)]
    pts += [(80.0, 0.0)]
    # remove stray duplicates; round to 0.1
    out = []
    for z, p in pts:
        q = (round(z, 2), round(max(p, 0.0), 2))
        if not out or abs(out[-1][0] - q[0]) + abs(out[-1][1] - q[1]) > 0.05:
            out.append(q)
    return [[q[0], q[1]] for q in out]


def band_profile():
    """The lock-rail band (z up from the underside, p proud): a square underside, then broad lit rolls with shallow creases
    (about 2.6 mm deep, at z 26 and z 52, as P1's two darks), crests at z 12, 36 and 62, a rounded top nosing rolling back."""
    return [[0.0, 0.0], [0.0, 16.0], [1.2, 18.6], [3.5, 20.4], [7.0, 21.4], [12.0, 21.8], [17.0, 21.0], [21.5, 19.8], [26.0, 19.2],
            [29.5, 19.9], [33.0, 21.2], [36.5, 21.8], [41.0, 21.2], [45.5, 20.2], [49.0, 19.5], [52.0, 19.2], [55.0, 19.9], [58.5, 21.4],
            [62.0, 22.0], [66.0, 21.3], [69.5, 18.0], [71.5, 10.0], [72.5, 0.0]]


def apply(T):
    T = copy.deepcopy(T)
    log = []

    def dep(id_, what, measured, photo):
        only = [v for v in ("T1", "F1") if id_.endswith(":" + v)] or {"D4:weatherboard": ["T1"], "D5:step_ends": ["T1"], "D6:lock_rail_band": ["T1"]}.get(id_, ["T1", "F1"])
        log.append({"id": id_, "what": what, "measured": measured, "photograph": photo, "variants": only})

    # ---- 1. the cylinder lock: a collar standing proud, a vertical keyway on both variants, rounded scallops on F1
    for var, parts in (("T1", T), ("F1", T["variants"]["flat_door_over_shop"]["parts"])):
        cl = parts["ironmongery"]["cylinder_lock"]
        was = cl["collar_proud_mm"]
        cl["collar_proud_mm"] = 5.0
        cl["keyway"] = "vertical slot 3 x 9 mm in the plug"
        cl["keyway_w_mm"], cl["keyway_h_mm"] = 3.0, 9.0
        if var == "F1":
            cl["scallops"] = 8
            cl["metal"] = "chrome/nickel, a collar of 8 rounded scallops"
        dep("D1:collar_proud:" + var, "cylinder collar stands %.1f mm proud of the leaf (target.json %.1f, flush)" % (5.0, was),
            "contact-shadow halo round the collar, from a radial luminance profile about its centre: P2 centre (488, 495), a dark ring 2 px wide outside the collar's bright rim "
            "(rim radius 8.2 px = 19 mm): 2 px x 2.317 = 4.6 mm; P1 centre (258.75, 290.3), the dark crescent below and the bright crescent above the collar, 1 px x 5.15 = 5 mm. "
            "Under overcast light a contact shadow is about as wide as the projection it comes from, so 5.0 +-2 mm",
            "P2 (F1) and P1 (T1)")
    cl = T["variants"]["flat_door_over_shop"]["parts"]["ironmongery"]["cylinder_lock"]
    dep("D2:keyway:F1", "F1's keyway is a vertical slot 3 x 9 mm (target.json: a horizontal slot)",
        "P2 rows 497-500, x 488-489: a dark upright streak 1-2 px x 4 px = about 3 x 9 mm inside the bright plug (values 100/98, 64/24, 15, 76)", "P2")
    dep("D3:collar_scallops:F1", "F1's collar is 8 rounded scallops about 2.4 mm deep (target.json: 12 serrations, built as V-notches)",
        "P2 5x crop of the collar (centre (488, 495)): about 8 rounded lobes round the rim, not 12 sharp teeth; the rim catches light on its upper left", "P2")

    # ---- 2. the weatherboard (T1)
    wb = T["mouldings"]["weatherboard"]
    wb["profile_zp_mm"] = weatherboard_profile()
    wb["max_projection_mm"] = 26.0
    wb["profile_note"] = ("(z from the underside, p proud of the leaf face). Flat underside, a bull-nosed lower arris at 26 proud, a plain face sloping up and back at "
                          "30 degrees from the vertical to z 44, a small cove at z 52, a rounded top roll (radius 10.5) falling back onto the door at z 80.")
    dep("D4:weatherboard", "weatherboard's main face slopes up and back at 30 degrees (target.json: a near-vertical belly at 22-26 mm proud from z 6 to z 50)",
        "P1 column profile x 145-175, rows 513.7-529.7 (80 mm): the main face, rows 520-527 (z 9 to 49), is the brightest part, mean 134 (sRGB) against 78 for the flat leaf face "
        "just above it (rows 505-513): 1.7 times in the picture's values, about 3 times in linear light (the review's reading, re-measured on the preview); a face that bright takes the sky, so its normal tilts upward; under it the lower arris (rows 528-529) and above it the "
        "hollow (rows 518-519, z 56) and the lit top roll (rows 514-517, z 62-77)", "P1")

    # ---- 3. the step: the nose and its undercut return round both ends
    td = T["step"]["tread"]
    td["nosing_radius_mm"] = 42.0
    td["x_mm"] = [-48.0, 930.0]
    td["width_mm"] = 978.0
    td["plan_corner_radius_mm"] = 47.0
    td["nose"] = ("a full half-round of radius 42 along the front and returning round both ends in the same section (a torus at the corners), its underside "
                  "turning in to a base face set 20 behind the front-most point all the way round; the base runs down to the ground in shadow")
    dep("D5:step_ends", "tread: the half-round nose and the undercut return round both ends (target.json: along the front only, ends cut off square by a plan corner of 40); "
        "nose radius 42 (45), plan corner 47 (40), x from -48 to 930 (-39 to 921, width 978 against 960)",
        "P1 x 87-95 and 283-291, rows 562-600: the lit nose and its dark undercut roll round both ends (the front review's reading); the end overhang beyond each reveal must hold the whole "
        "round, so the tread is 9 mm wider each side (the target's own width 960 +-25 and overhang 39 +-20 both hold); the radius 42 is inside the target's 45 +-15", "P1")

    # ---- 4. the lock-rail band (T1)
    bd_ = T["mouldings"]["lock_rail_band"]
    bd_["profile_zp_mm"] = band_profile()
    bd_["profile_note"] = ("(z from the underside, p proud of the rail face). Square underside (a crisp shadow line beneath), a lower fillet, then broad lit rolls with two shallow "
                           "creases (about 2.6 mm deep) at z 26 and 52, crests at z 12, 36 and 62, a rounded top nosing rolling back to the rail.")
    dep("D6:lock_rail_band", "band is broad lit rolls (crests at z 12, 36, 62) with two shallow creases about 2.6 mm deep (target.json: three narrow crests between 7 mm deep coves)",
        "P1 column profile x 145-175, rows 363.5-377.5: the band is lit across its whole height; the creases (rows 367-369 and 372-373, z 52 and z 26) dip only to about 0.7 of its "
        "brightest and stay about twice the flat leaf (the front review's reading); a 7 mm cove would be dark", "P1")

    # ---- 5. the narrow points
    # 5a. the panel mouldings' width on the face
    for var, parts, new in (("T1", T, 46.0), ("F1", T["variants"]["flat_door_over_shop"]["parts"], 43.0)):
        bol = parts["mouldings"]["outside_bolection"]
        was = bol["width_on_face_mm"]
        k = new / was
        bol["profile_dh_mm"] = [[round(d * k, 3), h] for d, h in bol["profile_dh_mm"]]
        bol["width_on_face_mm"] = new
    dep("D7:moulding_width:T1", "T1 panel mouldings 46 mm on the face (target.json 36); the section's d values scaled by 46/36, heights as they were",
        "P1 column luminance profile across the upper-left panel's left moulding (cols 130-145, 5.19 mm a pixel): the outer crease at col 133, the nose highlight at 135-136, the cove 137-140 and the "
        "field from col 141-144, so 9 px = 46-47 mm; the four mouldings in P1 read 9-10 px between their outer and inner dark lines (cols 134-144, 173-182, 203-212, 241-251: 47-52 mm "
        "with the occlusion lines, 41 +-7 without). Three fresh reviewers read 41-50. 46 is the middle of both readings", "P1")
    dep("D8:moulding_width:F1", "F1 panel mouldings 43 mm on the face (target.json 42); the section's d values scaled by 43/42",
        "P2: 18.5 px x 2.317 = 43 mm all round (the column profile across the lock rail's moulding agrees: 18-19 px between the outer crease and the field)", "P2")
    # 5b. the letter plate
    for var, parts in (("T1", T), ("F1", T["variants"]["flat_door_over_shop"]["parts"])):
        lp = parts["ironmongery"]["letter_plate"]
        lp["rim_chamfer_mm"] = 3.0
        lp["screws"] = "none (T1: none seen); two round pivot bosses at the flap's hinge ends, 8 mm across, standing 2.5 mm above the rim" if var == "F1" else lp["screws"]
        if var == "F1":
            lp["pivot_bosses"] = {"diameter_mm": 8.0, "proud_of_rim_mm": 2.5, "x_from_centre_mm": 29.5}
    dep("D9:plate_rim", "letter-plate rim: flat at 6 mm proud from the aperture edge to 3 mm short of the outer edge, then the 45-degree chamfer the target's text asks for, "
        "3 x 3 mm, down to the backplate's 3 mm edge (target_drawing.py draws a 2 x 1 chamfer and a 10-degree rise)",
        "target.json: 'the rim's outer edge chamfered 45 degrees from 6 mm down to the backplate'; P2 (plate x 293-376, rows 281-311) a bevelled frame lighter than the field; "
        "the close reviewer: 'a true 45 degree bevel would read closer to P1's lighter border'", "P2 and P1")
    dep("D10:plate_pivots:F1", "F1 letter plate: no corner screws; two round pivot bosses at the ends of the flap's hinge (target.json: four slotted screws at the rim's corners)",
        "P2 plate crop (x 293-376, rows 281-311): two round bosses at the flap's ends, in its upper third, 3-4 px = about 8 mm; no screws at the corners", "P2")
    # 5c. the plugged keyhole
    kh = T["variants"]["flat_door_over_shop"]["parts"]["ironmongery"]["old_keyhole"]
    kh["head_diameter_mm"], kh["slot_w_mm"] = 15.0, 8.0
    kh["kind"] = "a plugged mortice keyhole: a round head over a parallel slot, a dark recess 2 mm sunk, a pale metal blank filling the slot"
    dep("D11:keyhole:F1", "F1 keyhole is a round head 15 mm over a parallel slot 8 mm wide, the pale blank in the slot (target.json: a keyhole-shaped recess 23 x 32 with a small brass dot in the head)",
        "P2 5x crop centred (493, 447): a dark round head over a parallel slot, the slot holding a pale metal blank 3-4 px wide x 6 px (8 x 14 mm); the 23 mm of the target's reading takes in the dark halo", "P2")
    # 5d. the jamb fitting
    F1p = T["variants"]["flat_door_over_shop"]["parts"]
    F1p["ironmongery"]["keep"]["present"] = False
    T["ironmongery"]["keep"]["kind"] = ("a period bell push: a dark oblong back 22 x 72.6, a round brass bezel 17 mm across and a round dark button 10 mm across standing 5 mm proud; "
                                        "never a keep (a keep on the outside face of an inward-opening door's stop takes no bolt)")
    dep("D12:keep:F1", "F1 has no jamb fitting (target.json: a dark steel keep, 22 x 72.6, on the right jamb's stop)",
        "P2 right jamb at the keep's height (rows 515-547, x 508-530): bare painted timber with only the bead line; the 'grey service box' the target means is at rows 293-370 (1.33-1.51 m up), "
        "a modern fitting left out; and a keep on the outside face of the stop of an inward-opening door takes no bolt", "P2")
    dep("D13:bell_push:T1", "T1's jamb fitting is a period bell push: dark oblong back 22 x 72.6 (as P1), round brass bezel and a round button (target.json: a dark steel box keep with an 8 x 50 slot)",
        "P1 16x crop, cols 271.9-276.25 x rows 300.3-314.4: a dark upright oblong 22 x 72.6 on the right jamb's stop face, lighter speck near its middle; on the outside face of an inward-opening "
        "door's stop it can only be a bell push", "P1")
    # 5e. F1's threshold
    th = F1p["step"]["threshold"]
    th["front_y_mm"] = 108.3
    th["visible_front_face_mm"] = 45.0
    dep("D14:sill_front:F1", "F1's sill front stands 80 mm in front of the leaf's outside face, y 108.3 (target.json y 0, 188.3 in front of the leaf)",
        "P2 x 300-400: the sill's top, seen from above, is rows 946-959 (13 px) and its front face rows 960-979 (19-20 px = 45 mm), so the top shows two thirds as tall as the front; "
        "for a camera 15-25 degrees above the sill's plane that is a depth in front of the leaf of about 60-110 mm (the coordinator's range 60-100); 80 mm is the middle, against 188 mm",
        "P2")
    # 5f. the joints
    for var, parts in (("T1", T), ("F1", F1p)):
        parts["leaf"]["joint_groove_mm"] = {"width": 0.8, "depth": 0.8}
    dep("D15:joint_lines", "0.8 mm wide, 0.8 mm deep grooves at every rail-to-stile and muntin-to-rail joint on the face (v1 closed them)",
        "P2 (rows about 648 and 733, across the muntins at x 313-353): thin dark lines where the muntin meets the rails; target.json joints_and_seams: 'paint-bridged hairlines 0.4 mm'; the "
        "coordinator's range 0.5-1 mm", "P2")
    T["_departures"] = log
    return T, log
