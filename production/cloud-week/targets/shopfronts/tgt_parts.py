"""The parts of the shopfront kit as data: dimensions, profiles, elevations, joints, fixings.
Everything is millimetres. See tgt_profiles.py for the section planes. Read by make_target.py.

Coordinates of a bay (the GAME's viewer frame, as the fascia target uses):
  u  across the bay from the viewer's left party-wall line (0) to the right one (6000)
  d  out from the wall face (positive toward the street)
  z  up from the footway at the frontage
"""
import math

from tgt_profiles import arc, bezier, ccw, dedupe, pts, r1, spiral

# ---- the bay's fixed numbers (SCENE-SLOTS.md, the fascia target, the kit README) -------------------
BAY = 6000.0
SLOT = 350.0                  # a pilaster's slot at each party wall
ZONE = BAY - 2 * SLOT         # 5300: the opening between the piers
SIDE_SLOT = 944.0             # the flat's door, frame and its share of the pier return
SHOP_SLOT = 1006.0            # the shop door in its frame (900 leaf + 2 x 3 gaps + 2 x 50 jambs)
WINDOW_LEN = ZONE - SIDE_SLOT - SHOP_SLOT     # 3350
SILL_TOP = 600.0
TRANSOM = (2400.0, 2480.0)
HEAD = (2790.0, 2850.0)
FASCIA = (2850.0, 3400.0)
CORNICE_TOP = 3550.0
FASCIA_FACE = 120.0
CORNICE_DEPTH = 215.0
GLASS_D = 30.0

# ---- the pilaster ---------------------------------------------------------------------------------
SHAFT_W = 290.0
SHAFT_PROUD = 110.0
PLINTH_TOP = 800.0
PLINTH_PROUD = 150.0
NECK_Z = 2540.0
CAP_H = 310.0


def pilaster():
    sw = SHAFT_W
    u0 = (SLOT - sw) / 2.0            # 30
    u1 = u0 + sw                      # 320
    # ---- profiles (d, z) and (u, d) -------------------------------------------------------------
    plinth_cap = [(0, 720), (150, 720), (150, 764), (147, 770), (130, 794), (124, 800), (0, 800)]
    plinth_panel_stile = [(0, 0), (150, 0), (150, 764), (147, 770), (130, 794), (124, 800), (0, 800)]
    plinth_panel_field = [(0, 0), (150, 0), (150, 120), (146, 124), (138, 132), (138, 708), (146, 716), (150, 720),
                          (150, 764), (147, 770), (130, 794), (124, 800), (0, 800)]
    plinth_stepped = [(0, 0), (150, 0), (150, 504), (146, 504), (146, 631), (142, 631), (142, 680), (136, 680),
                      (136, 770), (133, 776), (120, 800), (0, 800)]
    bead_qr = [(0, 0)] + [(12 * math.cos(math.pi / 2 * k / 4), 12 * math.sin(math.pi / 2 * k / 4)) for k in range(5)]
    # shaft plans (u, d), CCW seen from above with u right and d up the page (d outward)
    # through the sunk field: a 10 mm quarter-round bead sits in each angle, the field floor at d 98
    shaft_panel_plan = [(u0, 0), (u1, 0), (u1, 110), (275, 110), (275, 108), (273.5, 102.9), (270.0, 99.0), (265, 98), (85, 98),
                        (80.0, 99.0), (76.5, 102.9), (75, 108), (75, 110), (u0, 110)]
    # fluted: five flutes between 12 mm fillets, each a segmental arc 12 deep
    fw = (sw - 6 * 12.0) / 5.0
    fl = [(u0, 0), (u1, 0), (u1, 110)]
    flute_edges = []
    x = u1
    for k in range(5):
        x -= 12.0
        a, b = x, x - fw
        mid = 0.5 * (a + b)
        arcp = [(mid + (a - mid) * math.cos(t), 110 - 12.0 * math.sin(t)) for t in
                [math.pi * j / 10 for j in range(0, 11)]]
        fl += [(a, 110)] + arcp[1:-1] + [(b, 110)]
        flute_edges.append([r1(b), r1(a)])
        x = b
    fl += [(u0, 110)]
    shaft_flute_plan = fl
    shaft_render_plan = [(u0, 0), (u1, 0), (u1, 108), (u1 - 3, 110), (u0 + 3, 110), (u0, 108)]
    clad_plan = [(0, 0), (350, 0), (350, 96), (346, 100), (4, 100), (0, 96)]
    # the capital (d, z local from the neck, 0 to 310), side section through the centre line
    cap_side = [(0, 0), (110, 0)]
    for k in range(1, 8):
        a = math.pi * k / 8
        cap_side.append((110 + 12 * math.sin(a), 12 - 12 * math.cos(a)))
    cap_side += [(110, 24), (116, 24), (116, 34), (114, 34), (114, 154)]
    # the cavetto (echinus) flare: from d 114 at z 154 out to d 128 at z 244, hollow
    cap_side += [(114 + 14 * (1 - math.cos(math.pi / 2 * k / 8)), 154 + 90 * math.sin(math.pi / 2 * k / 8)) for k in range(1, 9)]
    cap_side += [(128, 244), (130, 244), (130, 296)]
    # top moulding: a small ovolo then the flat top at 310
    cap_side += [(129.6, 300), (128.0, 304), (126.0, 308), (124.0, 310), (0, 310)]
    cap_side = dedupe(cap_side)
    # make the polygon simple: drop the (0,0)->(110,0) base line artefact by keeping the loop closed
    # ---- elevations (u, z) in the pilaster's own frame: u 0..350 across the slot, z up -----------------
    def rect(name, x0, z0, x1, z1, kind="face"):
        return {"name": name, "kind": kind, "pts": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]}

    cap_elev = [
        rect("astragal", u0 - 12, NECK_Z, u1 + 12, NECK_Z + 24),
        rect("neck_fillet", u0 - 3, NECK_Z + 24, u1 + 3, NECK_Z + 34),
        rect("die", u0, NECK_Z + 34, u1, NECK_Z + 154),
        rect("die_tablet", 90, NECK_Z + 54, 260, NECK_Z + 134, "raised"),
        {"name": "flare", "kind": "face", "pts": [[u0, NECK_Z + 154], [u1, NECK_Z + 154], [350, NECK_Z + 244], [0, NECK_Z + 244]]},
        rect("abacus", 0, NECK_Z + 244, 350, NECK_Z + 296),
        rect("top_moulding", 0, NECK_Z + 296, 350, NECK_Z + 310),
    ]
    el_panel = [
        rect("plinth_skirting", 0, 0, 350, 120),
        rect("plinth_stile_l", 0, 120, 50, 720), rect("plinth_stile_r", 300, 120, 350, 720),
        rect("plinth_field", 50, 132, 300, 708, "sunk"),
        rect("plinth_cap", 0, 720, 350, 800),
        rect("shaft_bottom_rail", u0, 800, u1, 940), rect("shaft_stile_l", u0, 940, 75, 2430),
        rect("shaft_stile_r", 275, 940, u1, 2430), rect("shaft_field", 75, 940, 275, 2430, "sunk"),
        rect("shaft_top_rail", u0, 2430, u1, NECK_Z),
    ] + cap_elev
    el_flute = [
        rect("plinth_skirting", 0, 0, 350, 120),
        rect("plinth_stile_l", 0, 120, 50, 720), rect("plinth_stile_r", 300, 120, 350, 720),
        rect("plinth_field", 50, 132, 300, 708, "sunk"),
        rect("plinth_cap", 0, 720, 350, 800),
        rect("shaft_bottom_rail", u0, 800, u1, 940), rect("shaft_top_rail", u0, 2430, u1, NECK_Z),
    ] + [rect("flute_%d" % (k + 1), lo, 940, hi, 2430, "sunk") for k, (lo, hi) in enumerate(reversed(flute_edges))] + cap_elev
    el_render = [
        rect("plinth_block1", 0, 0, 350, 504), rect("plinth_block2", 0, 504, 335, 631),
        rect("plinth_block3", 0, 631, 324, 680), rect("plinth_cap", 0, 680, 312, 800),
        rect("shaft", u0, 800, u1, NECK_Z),
    ] + cap_elev
    el_clad = [rect("clad_sheet_1", 0, 0, 350, 1200), rect("clad_sheet_2", 0, 1200, 350, 2400),
               rect("clad_sheet_3", 0, 2400, 350, 2850)]
    # the stepped plinth of the render variant steps in on the FREE side only (the party side stays flush
    # with its partner); el_render above is drawn for a LEFT pilaster (free side to the right, u=350)
    return {
        "name": "pilaster",
        "count_per_bay": 2,
        "slot_u": [[0, 350], [5650, 6000]],
        "centre_u": [175, 5825],
        "dims": {
            "slot_width": SLOT, "height": 2850.0, "shaft_width": SHAFT_W, "shaft_proud": SHAFT_PROUD,
            "shaft_u_in_slot": [u0, u1], "plinth_top_z": PLINTH_TOP, "plinth_proud": PLINTH_PROUD,
            "plinth_width": 350.0, "neck_z": NECK_Z, "capital_height": CAP_H, "capital_top_z": 2850.0,
            "capital_top_width": 350.0, "capital_top_proud": 130.0,
            "shaft_bottom_rail_top_z": 940.0, "shaft_top_rail_bottom_z": 2430.0,
            "panel_stile_width": 45.0, "panel_sunk_mm": 12.0, "panel_bead_mm": 10.0,
            "flutes": 5, "flute_width": r1(fw), "flute_depth": 12.0, "flute_fillet": 12.0,
            "capital_members_z_local": {"astragal": [0, 24], "neck_fillet": [24, 34], "die": [34, 154],
                                        "flare": [154, 244], "abacus": [244, 296], "top_moulding": [296, 310]},
            "die_tablet_u_in_slot": [90, 260], "die_tablet_proud": 8.0,
            "bosses": {"optional": True, "count": 3, "diameter": 30.0, "proud": 6.0, "pitch": 56.0,
                       "on": "the die's centre line, z_local 94 (the photograph's three roundels)"},
            "downpipe_chase": {"width": 76.0, "from_d": 50.0, "z_ranges": [[0, 800], [2540, 2850]], "at": "each party line (u 0 and 6000): both neighbours' plinths and capitals are notched; the D5 pipe (68 across, axis d 94) stands in it"},
            "backing": "a solid core board 330 wide x 110 deep behind shaft and capital (the kit's backing board), "
                       "so the faces between pilaster and frames close with no daylight",
        },
        "variants": {
            "panel": {"use": "original timber pilaster: sunk-panelled plinth and shaft (Rita's, the empty unit, tea rooms, ironmonger, chandler, fish)",
                      "material": "painted softwood", "elevation": el_panel},
            "flute": {"use": "original timber pilaster with five flutes (one alternative on the original fronts; the newsagent)",
                      "material": "painted softwood", "elevation": el_flute},
            "render": {"use": "painted render or cement pier on a stepped plinth (the 1930s grocer; the laundry's re-clad pier)",
                       "material": "painted render, arrises 1 mm eased", "elevation": el_render,
                       "painted_keyline": {"what": "P1's shaft carries a painted line panel, not a moulding: a line 10 wide in a darker, redder tone (about 25 L* below the cream), inset 35 from the shaft's edges, its top corners cut 35 at 45 degrees; z from 940 to 2400",
                                           "width": 10.0, "inset": 35.0, "corner_cut": 35.0, "z_range": [940, 2400], "kind": "Photo (texture, not geometry)"},
                       "stepped_plinth_inset_free_side": {"block2": 15, "block3": 26, "cap": 38}},
            "clad": {"use": "a 1960s-80s flush clad pier, no plinth, no capital (Mickey's, painted steel; kept as built)",
                     "material": "steel or aluminium sheet on a timber core, or painted board, 3 sheets", "elevation": el_clad,
                     "dims": {"proud": 100.0, "width": 350.0, "sheet_joints_z": [1200, 2400], "joint_width": 6.0}},
        },
        "profiles": {
            "plinth_cap_side": {"plane": "d-z", "points": pts(plinth_cap),
                                "note": "the weathered cap: a 44 mm nose face, a 6 mm bead, then the top falling 30 mm toward the street over 23 mm (the kit's steep weathering); the shaft's foot stands on the flat (d 0 to 124)"},
            "plinth_panel_side_through_stile": {"plane": "d-z", "points": pts(plinth_panel_stile)},
            "plinth_panel_side_through_field": {"plane": "d-z", "points": pts(plinth_panel_field),
                                                "note": "sunk 12 mm between the stiles; 45 degree sticking at the field's edge; the quarter-round bead is a separate planted piece"},
            "plinth_stepped_side": {"plane": "d-z", "points": pts(plinth_stepped),
                                    "note": "four members as the photograph: block (0 to 504), a step (504 to 631) 4 mm back, a step (631 to 680) 8 mm back, a weathered cap slab (680 to 800)"},
            "panel_bead": {"plane": "a-p", "points": pts(bead_qr), "note": "quarter-round, 12 mm, planted in the angle of the sunk field"},
            "shaft_panel_plan": {"plane": "u-d", "points": pts(shaft_panel_plan),
                                 "note": "through the sunk field: 45 mm stiles at full projection, the field 12 mm down, a 10 mm quarter-round bead each side"},
            "shaft_flute_plan": {"plane": "u-d", "points": pts(shaft_flute_plan), "note": "five flutes (segmental, 12 deep) between 12 mm fillets"},
            "shaft_render_plan": {"plane": "u-d", "points": pts(shaft_render_plan), "note": "plain face, arrises eased 3 mm by paint build-up"},
            "clad_plan": {"plane": "u-d", "points": pts(clad_plan)},
            "capital_side": {"plane": "d-z", "points": pts(cap_side),
                             "note": "z is local from the neck (add NECK_Z 2540): astragal (r 12), neck fillet, die, a hollow flare 90 high from d 114 to 128, abacus 52, a small ovolo top; flat top at 310 (z 2850) from the wall to d 130, where the console's toe and the fascia's bed mould meet it"},
        },
        "elevation_frame": "u 0..350 across the slot (left pilaster; the right pilaster is the same piece, symmetric), z from the footway",
        "plan_free_side": "the free (opening) side is u = 350 on the left pilaster and u = 0 on the right pilaster; the party side is flush with its partner",
    }


# ---- the console ---------------------------------------------------------------------------------
def console():
    # silhouette (d, z) refined from the street's built mesh (fascia_console_01, production/art/fascia-01):
    # the same 240 x 180 x 550 envelope, the same toe and neck, an S that is smooth rather than faceted
    key = [(60, 0), (74, 26), (62, 58), (70, 120), (88, 190), (112, 265), (138, 340), (158, 410), (170, 470), (176, 515), (180, 528)]
    # a Catmull-Rom through the key points, 5 samples a span
    def cr(p0, p1, p2, p3, n=5):
        out = []
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[i]) + (-p0[i] + p2[i]) * t + (2 * p0[i] - 5 * p1[i] + 4 * p2[i] - p3[i]) * t2 +
                                    (-p0[i] + 3 * p1[i] - 3 * p2[i] + p3[i]) * t3) for i in range(2)))
        return out
    ext = [key[0]] + key + [key[-1]]
    smooth = []
    for i in range(1, len(ext) - 2):
        smooth += cr(ext[i - 1], ext[i], ext[i + 1], ext[i + 2])
    smooth.append(key[-1])
    # round the toe's nose (the spline would overshoot between (60,0) and (74,26)): replace the first span
    toe = [(60, 0)] + [(60 + 14 * math.sin(math.radians(a)), 14 - 14 * math.cos(math.radians(a))) for a in (30, 60, 90)] + [(74, 26)]
    smooth = toe + [p for p in smooth if p[1] > 26]
    side = [(0, 0)] + smooth + [(180, 550), (0, 550)]
    side = dedupe(side)
    # volute: a spiral relief on each side face (a shallow groove 6 wide, 4 deep), centre (46, 74)
    vol = spiral(34, 82, 3, 24, 200, 1.75, n=40)
    # the leaf on the front face (u from the console's centre line, z local): an acanthus pendant, 3 lobes
    def leaf_outline():
        right = []
        # top at z 440 half-width 58, three scallops down each side, tip at z 120
        for z, w in [(440, 58), (420, 60), (396, 52), (384, 46), (368, 54), (344, 50), (330, 42), (312, 48), (288, 42),
                     (272, 34), (252, 38), (232, 30), (212, 24), (190, 18), (160, 9), (120, 0)]:
            right.append((w, z))
        left = [(-u, z) for u, z in reversed(right[:-1])]
        return right + left
    leaf = leaf_outline()
    plan = [(-120, 0), (120, 0), (120, 168), (108, 180), (-108, 180), (-120, 168)]
    front_el = [{"name": "face", "kind": "face", "pts": [[-120, 0], [120, 0], [120, 550], [-120, 550]]},
                {"name": "leaf", "kind": "relief", "pts": [[round(a, 1), round(b, 1)] for a, b in leaf]}]
    return {
        "name": "console",
        "count_per_bay": 2,
        "centre_u": [175, 5825],
        "u_range": [[55, 295], [5705, 5945]],
        "dims": {"width": 240.0, "depth": 180.0, "height": 550.0, "z_bottom": 2850.0, "z_top": 3400.0,
                 "toe_depth": 60.0, "toe_width": 240.0, "side_chamfer": 12.0,
                 "foot_on_capital": "the toe (240 x 60 at z 2850) stands wholly on the capital's top, whose top is 350 x 130",
                 "neck_flat": [528, 550], "scroll_eye_centre_dz": [34, 82], "scroll_outer_radius": 24.0,
                 "leaf": {"height": 330, "z_local": [120, 440], "max_half_width": 60, "relief_mm": 12,
                          "lobes_per_side": 3, "rib": "a raised central rib 8 wide, 4 proud of the leaf's dome",
                          "groove_between_lobes": {"width": 4, "depth": 3}}},
        "variants": {
            "scroll": {"use": "the original console: S-curve, volute on each side, an acanthus leaf on the face (all original fronts)",
                       "elevation": front_el},
            "block": {"use": "a plain block console (the 1930s grocer): the same envelope, the S curve straightened to a 45 degree chamfer, no leaf, three bosses",
                      "points_side": pts([(0, 0), (60, 0), (60, 40), (180, 400), (180, 550), (0, 550)])},
            "absent": {"use": "console gone: the foot's stump (60 x 240 x 90) and the screw holes remain on the capital (the empty unit's left console)"},
        },
        "profiles": {
            "side_silhouette": {"plane": "d-z", "points": pts(side),
                                "note": "z local from the console's foot (add 2850); the same envelope as the built fascia_console_01; wall at d=0 (back), the cornice's soffit meets the top"},
            "plan_at_neck": {"plane": "u-d", "points": pts(plan), "note": "240 wide, 12 mm chamfer down each front edge (the built mesh's per-station taper)"},
            "volute_spiral": {"plane": "d-z", "points": pts(vol, closed=False),
                              "note": "centreline of the groove cut in each side face: 1.75 turns from r 3 (the eye, centre d 34, z 82) to r 24, inside the silhouette; groove 5 wide, 4 deep"},
            "leaf_outline": {"plane": "u-z", "points": pts(leaf), "note": "u from the console's centre line, z local; relief domed 12 mm at the rib, 0 at the outline"},
        },
    }


# ---- fascia board, bed mould and cornice -----------------------------------------------------------
def fascia_board():
    bed = [(120, 0), (132, 0), (132, 10), (129, 22), (123, 34), (120, 40)]
    section = [(0, 0), (132, 0), (132, 10), (129, 22), (123, 34), (120, 40), (120, 550), (0, 550)]
    return {
        "name": "fascia_board",
        "dims": {"u_range": [295, 5705], "length": 5410.0, "z_range": [2850, 3400], "height": 550.0, "face_d": 120.0,
                 "board_thickness": 25.0, "carried_by": "a rail behind the board's foot and top, fixed to the consoles' backs and to the wall plate",
                 "bed_mould": {"z_range": [2850, 2890], "proud_of_face": 12.0},
                 "face": "vertical, plain, one plane; the planted mouldings and the lettering are the fascia target's (production/cloud-week/targets/fascia-signs)"},
        "profiles": {"section": {"plane": "d-z", "points": pts(section),
                                 "note": "z local from the board's foot (2850); the bed mould's front stands 12 proud of the face and 2 proud of the capital's top front (130), so the board's foot overhangs the capitals by the mould only"}},
        "ends": "each end is let into the console's side with a 12 mm rebate; at the capital the foot rests on the abacus for 55 mm (u 295 to 350)",
        "variants": {"timber": "the original board (O fronts)", "boxed": "the old board with a plastic box or flat panel screwed over it (fascia target)",
                     "glass": "the grocer's board is a reverse-painted glass fascia in three slabs on a timber backing, the same plane"},
    }


def cornice():
    # (d, z local from the cornice's soffit at 3400), the built envelope 215 x 150, drip groove kept at 155 to 175
    p = [(0, 0), (155, 0), (155, 12), (175, 12), (175, 0), (215, 0), (215, 52), (211, 56), (211, 60),
         (205, 68), (201, 76), (200, 86), (203, 90), (207, 98), (208, 110), (207, 124), (205, 130), (150, 150), (0, 150)]
    # an ovolo bed mould on the soffit between the wall and the drip, hidden behind the board's top edge
    p = dedupe(p)
    return {
        "name": "cornice",
        "count_per_bay": 1,
        "dims": {"length": 5892.0, "u_range": [54, 5946], "depth": 215.0, "height": 150.0, "z_bottom": 3400.0, "z_top": 3550.0,
                 "drip_groove": {"d_range": [155, 175], "depth": 12.0},
                 "stops_each_end": 54.0,
                 "reason_for_length": "the D5 downpipe at each party wall stands 94 from the wall, 68 across: 6000 - 68 - 2 x 20 = 5892 (fascia-01 spec)",
                 "lead": "a 1.8 mm lead apron over the wash, turned 100 up the wall behind (a grey line on the brick), an upstand 25 at each end; not geometry",
                 "wash_slope_deg": round(math.degrees(math.atan((150 - 130) / (205 - 150))), 1),
                 "corona_face": [0, 52], "corona_face_fraction_of_height": round(52 / 150, 3)},
        "profiles": {"section": {"plane": "d-z", "points": pts(p),
                                 "note": "z local from the soffit (3400): flat soffit, drip groove 12 deep, a tall corona face 52 (0.35 of the height, as P1's plain face is 0.39 of its crown), a fillet, a cyma reversa back to d 200 at z 86, a fillet, a cap ovolo out to d 208 at z 110, a short face, then the wash falling 20 mm over 55 mm to a flat top at 150 that runs back to the wall"}},
        "joints": ["a 45 degree scarf in the timber every 2.4 m at most (none visible on a 5.9 m run, painted over); a butt at each console's side is not needed (the cornice runs over the consoles' tops)"],
    }


# ---- sill and stallriser ---------------------------------------------------------------------------
def sill():
    p = [(0, 525), (128, 525), (128, 531), (134, 531), (134, 525), (144, 525), (150, 531), (150, 566), (147, 572),
         (142, 576), (60, 600), (0, 600)]
    return {
        "name": "sill",
        "dims": {"z_range": [525, 600], "thickness": 75.0, "nose_d": 150.0, "drip_throat": {"d_range": [128, 134], "depth": 6.0},
                 "weathering": "15 degrees: 24 mm over 82 mm", "flat_bed_d": [0, 60], "length": "the window frame's length, 3350, plus 40 each end under the jambs (3430) where the pier meets it",
                 "screw_pitch": 450.0, "screws": "No. 12 brass or steel countersunk screws, pellet-plugged, painted over; 7 along 3350"},
        "profiles": {"section": {"plane": "d-z", "points": pts(p),
                                 "note": "3 in (75 mm) sill, a bullnose of r 6, a 6 x 6 throat 16 back from the nose, top weathered to a flat bed 60 deep where the frame's bottom rail stands"}},
    }


def stallriser():
    face = 125.0
    pan_front = [(0, 0), (135, 0), (135, 120), (125, 120), (125, 525), (0, 525)]
    pan_plinth = [(0, 0), (135, 0), (135, 105), (131, 112), (125, 120), (125, 525), (0, 525)]
    tile_side = [(0, 0), (126, 0), (126, 120), (113, 120), (113, 492), (121, 495), (125, 501), (125, 519), (121, 525), (113, 525), (0, 525)]
    return {
        "name": "stallriser",
        "dims": {"z_range": [0, 525], "face_d": face, "sill": "see sill (z 525 to 600)", "length_default": 3350.0,
                 "plinth_meets_pilaster": "the stallriser's ends butt the pilaster plinths' sides at u 350 / 5650; its face (125) is 25 behind the plinth's front (150)"},
        "variants": {
            "panel": {"use": "timber panelled: a plinth 120, bottom rail 80, three raised and fielded panels between 80 stiles and muntins, top rail 80 (Rita's; the kit)",
                      "dims": {"plinth": 120.0, "stile": 80.0, "bottom_rail": [120, 200], "top_rail": [445, 525], "panel_inset": 14.0,
                               "field_margin": 35.0, "field_rise": 12.0, "bead": 14.0,
                               "panels_rule": "one panel per light of the window above, 3 on 3350 (muntins on the mullion lines)"},
                      "section": {"plane": "d-z", "points": pts(pan_plinth)}},
            "tile": {"use": "glazed brick-shaped tile 152 x 72 in stretcher bond, 3 mm joints, a 120 skirting course of 304 x 117, then 5 courses of 75 (72 + joint), a bullnose capping 30 high (r 12): 120 + 375 + 30 = 525",
                     "dims": {"tile": [152.0, 72.0], "joint": 3.0, "skirting": [304.0, 120.0], "capping_height": 30.0, "capping_r": 12.0, "courses": 5, "course_pitch": 75.0, "bond": "stretcher, half-lap"},
                     "section": {"plane": "d-z", "points": pts(tile_side)}},
            "tile_square": {"use": "glazed square tiles 152.4 (6 in), 3 mm joints, a black skirting 100, two full courses and one half course (152.4 x 76.2), a bullnose cap 35: 100 + 2 x 155.4 + 79.2 + 35 = 525 (fish and laundry white, chandler pale green)",
                            "dims": {"tile": [152.4, 152.4], "half_course_tile": [152.4, 76.2], "joint": 3.0, "skirting": 100.0, "courses": 2, "half_courses": 1, "course_pitch": 155.4,
                                     "half_course_pitch": 79.2, "capping_height": 35.0, "bond": "straight (stack)"}},
            "tile_patterned": {"use": "6 in tiles with a printed diamond-lattice pattern in a 2 x 2 repeat (Mickey's: cream, mid blue, black), black skirting 100, two full courses patterned, one plain half course, cap 35: as tile_square",
                               "dims": {"tile": [152.4, 152.4], "joint": 3.0, "skirting": 100.0, "courses": 2, "half_courses": 1, "course_pitch": 155.4, "half_course_pitch": 79.2, "capping_height": 35.0,
                                        "repeat": "2 x 2 tiles = 304.8 square: A cream with a mid-blue diamond whose corners touch the tile's edge midpoints and a black dot at its centre; B black with a cream diamond; A B over B A",
                                        "colours": {"cream": [222, 212, 184], "blue": [46, 68, 136], "black": [30, 30, 32]}}},
            "slab": {"use": "opaque coloured structural glass in three slabs, bottle green, polished, 6 mm chrome capping, 3 mm black mastic joints (the grocer)",
                     "dims": {"slabs": 3, "joint": 3.0, "bevel": 2.0, "capping": {"height": 18.0, "material": "chrome strip"}, "z_range": [0, 525]}},
            "render": {"use": "painted render with a rendered cill under the sill (cheap 1920s-50s repair), or hardboard painted (the tea rooms)", "dims": {"coat": 12.0}},
            "grille": {"use": "available, not used by the ten fronts: pierced cast-iron or pressed-metal ventilation panels in the panel variant's frame, one per light, as P1's stallriser (a framed grille 580 high at the measured scale); the earlier reading (Dover guide) mentions grilles under the fascia too",
                       "dims": {"bars": 12.0, "open_fraction": 0.6, "set_back": 20.0, "backed_by": "black mesh", "field_height": 245.0}, "kind": "Photo (the type) and Judgement (the sizes)"},
            "boarded": {"use": "the empty unit: the panelling painted out, a sheet of ply or hardboard screwed over the lower 525 with 12 screws, paint peeling",
                        "dims": {"sheet_thickness": 9.0, "screws": 12}},
        },
        "profiles": {"panel_bead": {"plane": "a-p", "points": pts([(0, 0)] + [(14 * math.cos(math.pi / 2 * k / 4), 14 * math.sin(math.pi / 2 * k / 4)) for k in range(5)]),
                                    "note": "quarter-round 14 planted round each panel"}},
    }


# ---- window frame ----------------------------------------------------------------------------------
def window_frame():
    # T1 mullion: 70 wide, front at d 92, a rounded (oval) nose, glazing rebates in both sides at d 24..36
    hw = 35.0
    nose_c = 92.0 - 31.5
    mull = [(-hw, 0), (-hw, 24), (-hw + 10, 24), (-hw + 10, 36), (-hw, 36), (-hw, nose_c)]
    for k in range(1, 8):
        a = math.pi * k / 8
        mull.append((-hw * math.cos(a), nose_c + 31.5 * math.sin(a)))
    mull += [(hw, nose_c), (hw, 36), (hw - 10, 36), (hw - 10, 24), (hw, 24), (hw, 0)]
    # T2: flat face 80 wide, two 8 mm quirk beads each side of a flat, front at d 92
    t2 = [(-40, 0), (-40, 24), (-30, 24), (-30, 36), (-40, 36), (-40, 82), (-36, 86), (-32, 88), (-26, 86), (-24, 92),
          (24, 92), (26, 86), (32, 88), (36, 86), (40, 82), (40, 36), (30, 36), (30, 24), (40, 24), (40, 0)]
    # M1 aluminium: a 50 x 75 box, 3 mm wall, glazing pockets, snap-on cover cap
    m1 = [(-25, 0), (-25, 75), (25, 75), (25, 0)]
    m1_pocket = [(-25, 0), (-25, 44), (-17, 44), (-17, 56), (-25, 56), (-25, 72), (-22, 75), (22, 75), (25, 72), (25, 56),
                 (17, 56), (17, 44), (25, 44), (25, 0)]
    # the jamb with its rebate on the glass side: section (u, d); u = 0 is the frame's outer edge
    jamb_t1 = [(0, 0), (50, 0), (50, 24), (38, 24), (38, 36), (50, 36), (50, 95), (3, 95), (0, 92)]
    transom_t1 = [(0, 0), (70, 0), (70, 6), (77, 6), (77, 0), (96, 0), (100, 4), (100, 46), (98, 51), (93, 54), (46, 80), (0, 80)]
    toplight_bar = [(-14, 0), (-14, 24), (-8, 24), (-8, 36), (-14, 36), (-14, 38)] + \
        [(-14 * math.cos(math.pi * k / 6), 38 + 17 * math.sin(math.pi * k / 6)) for k in range(1, 6)] + \
        [(14, 38), (14, 36), (8, 36), (8, 24), (14, 24), (14, 0)]
    bead = [(0, 0), (16, 0), (16, 2), (14, 7), (10, 10.5), (5, 12), (0, 12)]
    # M2: a bronze-plated bar 28 x 40: a rounded front, a 3 mm rebate each side for 6 mm plate
    m2 = [(-14, 0), (-14, 24), (-11, 24), (-11, 30), (-14, 30), (-14, 33)] + \
        [(-14 * math.cos(math.pi * k / 6), 33 + 7 * math.sin(math.pi * k / 6)) for k in range(1, 6)] + \
        [(14, 33), (14, 30), (11, 30), (11, 24), (14, 24), (14, 0)]
    # M1: the 50 x 75 aluminium jamb (open on the glass side) and transom (box with a sloped top and a drip)
    jamb_m1 = [(0, 0), (50, 0), (50, 44), (38, 44), (38, 56), (50, 56), (50, 72), (47, 75), (3, 75), (0, 72)]
    transom_m1 = [(0, 0), (50, 0), (50, 4), (54, 4), (54, 0), (75, 0), (75, 40), (70, 46), (32, 50), (0, 50)]
    gasket_bead = [(0, 0), (14, 0), (14, 5), (11, 8), (3, 8), (0, 6)]
    putty = [(0, 0), (14, 0), (0, 10)]
    head = [(0, 0), (95, 0), (95, 60), (0, 60)]

    def bar_positions(length, n_mull, mull_w, jamb_w):
        clear = length - 2 * jamb_w
        light = (clear - n_mull * mull_w) / (n_mull + 1)
        xs = []
        x = jamb_w + light
        for _ in range(n_mull):
            xs.append(round(x + mull_w / 2, 1))
            x += mull_w + light
        return xs, round(light, 1)

    out_xs, out_light = bar_positions(WINDOW_LEN, 2, 70.0, 50.0)
    # toplight bars: 8 lights between 2 jambs of 50: 7 bars of 28
    tl_n = 8
    tl_clear = WINDOW_LEN - 2 * 50.0
    tl_light = (tl_clear - 7 * 28.0) / 8.0
    tl_xs = [round(50 + tl_light * (k + 1) + 28 * k + 14, 1) for k in range(7)]
    return {
        "name": "window_frame",
        "dims": {"length_default": WINDOW_LEN, "length_no_side_door": ZONE - SHOP_SLOT, "z_range": [525, 2850],
                 "sits_on": "the sill's flat bed (z 600) through a bottom rail 90 high (z 600 to 690)",
                 "bottom_rail": [600, 690], "transom": list(TRANSOM), "head": list(HEAD),
                 "lower_lights_z": [690, 2400], "toplights_z": [2480, 2790],
                 "jamb_face": 50.0, "jamb_depth": 95.0, "mullion_face": 70.0, "mullion_front_d": 92.0,
                 "mullion_projection_beyond_glass": 62.0, "glass_d": GLASS_D, "glass_thickness": 6.0,
                 "mullions_rule": "n = 2 on 3350 (3 lights of 1015); n = ceil((L - 100) / 1250) - 1, at most 3, as the kit",
                 "mullion_centres_u_default": out_xs, "light_width_default": out_light,
                 "toplights": {"count": tl_n, "bar_face": 28.0, "bar_xs_default": tl_xs, "light_width": round(tl_light, 1)},
                 "bead": "timber ovolo 16 x 12, mitred, brass round-head screws every 250 (T1)",
                 "frame_front_d": 95.0},
        "profiles": {
            "mullion_t1_plan": {"plane": "u-d", "points": pts(mull), "note": "70 wide, oval nose, front at d 92 (62 in front of the glass at 30); glazing rebates 10 x 12 in both sides"},
            "mullion_t2_plan": {"plane": "u-d", "points": pts(t2), "note": "80 wide flat face with a quirk bead at each edge (the heavier, older section; the empty unit and the ironmonger)"},
            "mullion_m1_plan": {"plane": "u-d", "points": pts(m1_pocket), "note": "aluminium box 50 x 75 with glazing pockets 12 deep; a snap-on cover cap 38 wide, front at d 75 (metal fronts)"},
            "jamb_t1_plan": {"plane": "u-d", "points": pts(jamb_t1), "note": "50 face x 95 deep with the glazing rebate on its inner side"},
            "transom_t1": {"plane": "d-z", "points": pts(transom_t1),
                           "note": "z local from 2400: a 6 x 7 drip groove under the nose at d 70 to 77, the nose at d 100, the top weathered 26 mm over 47 mm to the glass bed; as the kit's"},
            "toplight_bar_plan": {"plane": "u-d", "points": pts(toplight_bar), "note": "28 wide, rounded front at d 55, glazing rebates"},
            "bar_m2_plan": {"plane": "u-d", "points": pts(m2), "note": "M2 (1930s): a bronze-plated bar 28 wide, front at d 40, rounded; 3 mm rebates; the jamb is the same bar cut square"},
            "jamb_m1_plan": {"plane": "u-d", "points": pts(jamb_m1), "note": "M1: aluminium jamb 50 x 75 with a glazing pocket 12 deep; a snap-on cover cap not drawn"},
            "transom_m1": {"plane": "d-z", "points": pts(transom_m1), "note": "M1: a 50 high box, 75 deep, top sloped 4 mm over 38, a 4 x 4 drip at d 50 to 54"},
            "glazing_bead_gasket": {"plane": "a-p", "points": pts(gasket_bead), "note": "M1: a snap-in bead 14 x 8 over a black gasket"},
            "glazing_bead_ovolo": {"plane": "a-p", "points": pts(bead), "note": "T1: planted ovolo 16 along the face x 12 proud"},
            "glazing_putty": {"plane": "a-p", "points": pts(putty), "note": "old putty-glazed lights: a 45 degree fillet 14 x 10, cracked and painted over"},
            "head_section": {"plane": "d-z", "points": pts(head), "note": "z local from 2790: a plain 95 x 60 rail under the fascia's foot"},
        },
        "variants": {
            "T1": "timber, oval mullions, ovolo beads (Rita's)",
            "T2": "timber, flat-faced quirk-bead mullions 80 x 92",
            "M1": "aluminium extrusions, anodised silver or bronze: stiles and mullions 50 x 75, transom 50 x 75 flat-topped with a drip, snap-in beads, black gasket",
            "M2": "chromium- or bronze-plated bars (1930s): 28 face, 40 deep, curved glass returns",
        },
        "elevations": {"bar_positions": {"mullion_centres": out_xs, "toplight_bars": tl_xs}},
    }


# ---- the shop door ---------------------------------------------------------------------------------
def shop_door():
    thr = [(0, 0), (130, 0), (130, 10), (126, 15), (120, 17), (75, 23), (70, 25), (0, 25)]
    return {
        "name": "shop_door",
        "dims": {"slot_width": SHOP_SLOT, "leaf_width": 900.0, "leaf_height": 2040.0, "leaf_thickness": 50.0, "leaf_gap": 3.0,
                 "frame_jamb_face": 50.0, "frame_depth": 100.0, "leaf_front_d": 70.0,
                 "stile": 115.0, "top_rail": 115.0, "lock_rail": [590, 700], "bottom_rail": [0, 230],
                 "lower_panel": [230, 590], "glazed_from": 700.0, "glazed_to": 1925.0,
                 "glazed_fraction_of_leaf_from": 0.343,
                 "kick_plate": {"height": 170.0, "width": 770.0, "metal": "brass", "screws": 8},
                 "foot_strip": {"height": 30.0, "metal": "brass", "proud": 3.0},
                 "threshold": "terrazzo or tiled, 25 at the leaf falling to 12 at a rounded nose out on the pavement, the full frame width",
                 "fanlight": {"z_range": [2043, 2400], "bars": "none (one pane) or two bars when the door is wider"},
                 "transom": list(TRANSOM), "head": list(HEAD), "above_transom": "toplight with 2 bars (as the kit)",
                 "hinges": {"count": 3, "size": "100 x 75 butt, brass or steel, at 150 from top, 150 from bottom, middle", "screws": 6},
                 "furniture": {"lever_handles": {"z": 1000.0, "pair": True, "backplate": [240, 40], "metal": "brass"},
                               "latch": "a rim night-latch (cylinder and case) on the inside, a mortice lock's keyhole escutcheon on the lock stile at z 950",
                               "letter_plate": {"width": 250.0, "height": 40.0, "z": 800.0, "on": "the lower panel's centre"},
                               "push_plate": "none on timber doors",
                               "seen_in_P1_not_adopted": "P1's double doors carry octagonal brass knobs on the lock rail and long brass pull plates: an alternative to the lever set for a 1900s front (Judgement: a 65 mm octagonal knob at z 780)"}},
        "profiles": {"threshold_section": {"plane": "d-z", "points": pts(thr)},
                     "leaf_stile_plan": {"plane": "u-d", "points": pts([(0, 70), (115, 70), (115, 20), (101, 20), (101, 31), (89, 31), (89, 20), (0, 20)]),
                                         "note": "the leaf's stile (u across, d out; the leaf's outside face at d 70, inside at 20): 115 face, 50 thick; the glass rebate and the ovolo bead are on the glazing side; the 12 mm sticking on the panel side is a_p below"},
                     "frame_jamb_plan": {"plane": "u-d", "points": pts([(0, 0), (50, 0), (50, 100), (0, 100), (0, 78), (14, 78), (14, 36), (0, 36)]),
                                         "note": "the door frame's jamb: 50 face x 100 deep, rebated 14 x 42 for the leaf's stop; the leaf's face stands 30 behind the frame's face"},
                     "raised_field_edge": {"plane": "a-p", "points": pts([(32, 0), (60, 0), (60, 10), (40, 10)]), "note": "a raised and fielded panel: a flat margin 32, a bevel 8 rising 10, the field; as the kit"},
                     "glazing_bead": {"plane": "a-p", "points": pts([(0, 0), (14, 0), (14, 2), (12, 6), (8, 9.5), (4, 11), (0, 11)]), "note": "T1: ovolo 14 x 11"}},
        "variants": {"T1": "half-glazed timber leaf (Rita's, empty, tea, ironmonger, newsagent)",
                     "M1": "aluminium-framed glass door 900 x 2040: 50 stiles, 100 top rail, 170 bottom rail, a 300 chrome D pull and a push plate (fish, laundry, chandler)",
                     "M2": "bronze-framed glass door, a 150 kick plate in bronze (grocer, 1930s)"},
    }


def side_door_slot():
    return {
        "name": "side_door_slot",
        "note": "The flat's door is the front-door family's F1 variant (production/cloud-week/targets/front-door/): NOT re-targeted here.",
        "dims": {"slot_width": SIDE_SLOT, "opening_showing": 895.2, "filler_each_side": 24.4,
                 "leaf": [838.0, 1981.0], "head_z_visible": [2339.6, 2400.0], "above": "one raised-and-fielded panel from the transom's top (2480) to 2850, 944 wide minus 2 x 50",
                 "letter_plate": [250.0, 40.0],
                 "leaf_panels_uv_mm": [[114.3, 359.0, 192.8, 672.7], [479.0, 723.7, 192.8, 672.7], [114.3, 359.0, 901.3, 1854.0], [479.0, 723.7, 901.3, 1854.0]],
                 "leaf_panels_note": "[u0, u1, v0, v1] from the leaf's left edge and bottom, copied from the front-door target's F1 `panels.openings_leaf_uv_mm` for the drawing only"},
        "mapping_from_F1": {
            "x": "F1 x 0 is the left edge of the brick reveal; the slot is centred on the F1 opening (x 447.6): u_bay = u_slot_centre + (x_F1 - 447.6)",
            "y": "F1 y = 0 is its brick face; its frame's outside face is at F1 y 114.3. In the bay the frame's outside face stands at d = 100 (flush with the shop door's and window's frames, 10 behind the pilaster shaft's face): d = 214.3 - y_F1, i.e. the leaf's outside face (F1 188.3) is at d 26",
            "z": "F1 z 0 is the top of its threshold, 45 above the pavement (F1 ground z -45): z_bay = z_F1 + 45. Its head's visible face (F1 2339.6 to 2400) therefore reaches z 2445: the shop transom (2400 to 2480) covers the top 45, so the builder trims the F1 head at z 2400",
            "trim": ["the threshold board's front (F1 y 0, d 214) is cut back to d 130, flush with the shop door's threshold nose and under the plinth's 150",
                     "F1's brick arch, quoins, plinth and step are NOT built: the shopfront holds the head"],
        },
        "bay_parts_around_it": "a 24.4 mm filler strip each side (the pilaster return, painted the pier's colour), a fielded panel above, and the transom bar across the head",
    }


# ---- the recessed lobby --------------------------------------------------------------------------
def lobby():
    # plan (u relative to the shop-door slot's left edge, d out from the wall face; the frame line is d 100)
    def plan(depth):
        top = 100.0
        bottom = 100.0 - depth
        return [(0, bottom), (1006, bottom), (1006, top), (0, top)]
    return {
        "name": "lobby",
        "note": "A recess for the shop door: the door frame stands R behind the frame line (d 100), the window's end and the pier's side are returned. Flush fronts have none.",
        "dims": {
            "slot_width": 1006.0, "frame_line_d": 100.0,
            "grocer": {"recess": 600.0, "door_frame_front_d": -500.0, "returns": {"window_side": "glazed display return, frame 28, kick panel z 0 to 600 in the green glass", "pier_side": "a panelled lining in the pier's paint, 2 panels"},
                       "floor": {"z": 25.0, "kind": "terrazzo", "mosaic_border": {"width": 150.0, "tile": 20.0, "colours": ["cream", "bottle green"]}, "nosing": "brass, 30 x 6, at the frame line"},
                       "soffit": "plaster at z 2400 (the transom line), flat; the toplights above run on over the lobby's mouth", "splay_deg": 0},
            "steam_laundry": {"recess": 300.0, "door_frame_front_d": -200.0, "returns": {"window_side": "the window's end frame returned square, glazed to 600 up", "pier_side": "the pier's side, painted"},
                              "floor": {"z": 25.0, "kind": "quarry tile 150 x 150, red-brown, 3 mm joints", "nosing": "aluminium channel 30 x 6"}, "soffit": "painted board at z 2400", "splay_deg": 0},
            "door_frame_d_rule": "door_frame_front_d = 100 - recess",
        },
        "profiles": {"plan_grocer": {"plane": "u-d", "points": pts(plan(600.0)), "note": "floor outline, u from the slot's left edge; the street is at the top of the list (d 100)"},
                     "plan_laundry": {"plane": "u-d", "points": pts(plan(300.0))}},
        "variants": {"flush": "the door frame's front at d 100, the threshold nose at d 130 (the kit)", "recessed": "as above"},
    }
