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
SHAFT_PROUD = 140.0           # P1: the shaft stands 117 mm in front of the next surface it returns to, about 285 in front
                              # of the window frame (a lower and an upper bound); 140 keeps 40 or more in front of every frame
PLINTH_TOP = 600.0            # Rita's line (the kit, the approved front): the plinth's top is level with the stallriser/sill top
PLINTH_PROUD = 180.0
NECK_Z = 2540.0
CAP_H = 310.0
CAP_DIE_D = SHAFT_PROUD + 4.0          # 144: the die stands 4 proud of the shaft
CAP_FLARE_D = 172.0                    # the hollow flare reaches 172 over its 90
CAP_TOP_PROUD = 175.0                  # abacus front and nominal top face (the flat reaches 172, the ovolo rounds the last 3)
TALL_PLINTH_TOP = 800.0                # P1's plinth at the street's scale: NOT used by the ten fronts (see variants.plinth_tall)
FRAME_FRONT = {"T1": 95.0, "T2": 95.0, "M1": 75.0, "M2": 40.0, "door": 100.0, "F1": 100.0}   # the faces beside the piers


def cavetto(d0, z0, dd, dz, n=4):
    """A hollow (cavetto) moulding, a quarter ellipse centred at (d0, z0 + dz), from (d0, z0) at its foot back to
    (d0 - dd, z0 + dz) at its head, semi-axes dd (in d) and dz (in z); n segments."""
    out = []
    for k in range(n + 1):
        t = math.pi / 2 * k / n
        out.append((d0 - dd * math.sin(t), z0 + dz - dz * math.cos(t)))
    return out


def pilaster():
    sw = SHAFT_W
    SP, PP, PT = SHAFT_PROUD, PLINTH_PROUD, PLINTH_TOP
    u0 = (SLOT - sw) / 2.0            # 30
    u1 = u0 + sw                      # 320
    # ---- profiles (d, z) and (u, d) -------------------------------------------------------------
    # the timber (panel, flute) plinth: a skirting 120, two stiles round a sunk field, a cap 80 with a weathered top; the kit's
    plinth_cap = [(0, PT - 80), (PP, PT - 80), (PP, PT - 30), (PP - 4, PT - 24), (SP + 15, PT), (0, PT)]
    plinth_panel_stile = [(0, 0), (PP, 0), (PP, PT - 30), (PP - 4, PT - 24), (SP + 15, PT), (0, PT)]
    plinth_panel_field = [(0, 0), (PP, 0), (PP, 120), (PP - 4, 124), (PP - 12, 132), (PP - 12, PT - 92), (PP - 4, PT - 84), (PP, PT - 80),
                          (PP, PT - 30), (PP - 4, PT - 24), (SP + 15, PT), (0, PT)]
    # the base ogee (the kit's BASE, pilaster.py, made 15 proud instead of 25): 60 high, on the plinth's top, returned along both
    # sides of the shaft
    # the second review's points: 15 proud, so its front (d 155) stands on the cap's flat (which runs to d 155), not over the weathering
    base_ogee = [(SP, PT), (SP + 15, PT), (SP + 15, PT + 8), (SP + 12.6, PT + 12), (SP + 9, PT + 17), (SP + 6, PT + 24),
                 (SP + 3.6, PT + 33), (SP + 1.8, PT + 45), (SP, PT + 60)]
    # the stepped plinth of the render variant, from P1's four members: three steps, then a hollow moulding (cavetto) and a band
    # under the shaft. P1's plinth is 1123 mm high at its own scale; Rita's line keeps ours at 600: the head (cavetto 95 + band 21,
    # as P1's) is kept whole and the three lower blocks are shortened (360 / 450 / 484 against P1's 504 / 631 / 684 on 800)
    head_z = PT - 116.0                                         # 484: the cavetto's foot
    stepped = [(0, 0), (PP, 0), (PP, 360), (PP - 4, 360), (PP - 4, 450), (PP - 8, 450), (PP - 8, head_z)] + \
        cavetto(PP - 8, head_z, 24.0, 95.0, 4)[1:] + [(PP - 32, PT), (0, PT)]
    # the same, at P1's own 800 (the reviewer's points, +30 in d): offered, not used (variants.plinth_tall)
    tall = [(0, 0), (PP, 0), (PP, 504), (PP - 4, 504), (PP - 4, 631), (PP - 8, 631), (PP - 8, 684)] + \
        cavetto(PP - 8, 684.0, 24.0, 95.0, 4)[1:] + [(PP - 32, 800), (0, 800)]
    bead_qr = [(0, 0)] + [(12 * math.cos(math.pi / 2 * k / 4), 12 * math.sin(math.pi / 2 * k / 4)) for k in range(5)]
    # shaft plans (u, d), CCW seen from above with u right and d up the page (d outward)
    # through the sunk field: a 10 mm quarter-round bead sits in each angle, the field floor 12 below the stiles' face
    fl_d = SP - 12.0
    shaft_panel_plan = [(u0, 0), (u1, 0), (u1, SP), (275, SP), (275, SP - 2), (273.5, SP - 7.1), (270.0, SP - 11.0), (265, fl_d), (85, fl_d),
                        (80.0, SP - 11.0), (76.5, SP - 7.1), (75, SP - 2), (75, SP), (u0, SP)]
    # fluted: five flutes between 12 mm fillets, each a segmental arc 12 deep
    fw = (sw - 6 * 12.0) / 5.0
    fl = [(u0, 0), (u1, 0), (u1, SP)]
    flute_edges = []
    x = u1
    for k in range(5):
        x -= 12.0
        a, b = x, x - fw
        mid = 0.5 * (a + b)
        arcp = [(mid + (a - mid) * math.cos(t), SP - 12.0 * math.sin(t)) for t in
                [math.pi * j / 10 for j in range(0, 11)]]
        fl += [(a, SP)] + arcp[1:-1] + [(b, SP)]
        flute_edges.append([r1(b), r1(a)])
        x = b
    fl += [(u0, SP)]
    shaft_flute_plan = fl
    shaft_render_plan = [(u0, 0), (u1, 0), (u1, SP - 2), (u1 - 3, SP), (u0 + 3, SP), (u0, SP - 2)]
    clad_proud = SP                                              # the casing follows the old shaft's face
    clad_plan = [(0, 0), (350, 0), (350, clad_proud - 4), (346, clad_proud), (4, clad_proud), (0, clad_proud - 4)]
    # the capital (d, z local from the neck, 0 to 310), side section through the centre line
    cap_side = [(0, 0), (SP, 0)]
    for k in range(1, 8):
        a = math.pi * k / 8
        cap_side.append((SP + 12 * math.sin(a), 12 - 12 * math.cos(a)))
    cap_side += [(SP, 24), (SP + 6, 24), (SP + 6, 34), (CAP_DIE_D, 34), (CAP_DIE_D, 154)]
    # the cavetto (echinus) flare: from d 144 at z 154 out to d 172 at z 244, hollow
    cap_side += [(CAP_DIE_D + (CAP_FLARE_D - CAP_DIE_D) * (1 - math.cos(math.pi / 2 * k / 8)), 154 + 90 * math.sin(math.pi / 2 * k / 8)) for k in range(1, 9)]
    cap_side += [(CAP_FLARE_D, 244), (CAP_TOP_PROUD, 244), (CAP_TOP_PROUD, 296)]
    # top moulding: a small ovolo back to the flat top at 310 (the flat reaches d 172)
    cap_side += [(172.0 + 3.0 * math.cos(math.pi / 2 * k / 4), 296 + 14.0 * math.sin(math.pi / 2 * k / 4)) for k in range(1, 5)] + [(0, 310)]
    cap_side = dedupe(cap_side)

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
    br_top = PT + 140.0                                          # the shaft's bottom rail (the ogee stands on its foot)
    el_panel = [
        rect("plinth_skirting", 0, 0, 350, 120),
        rect("plinth_stile_l", 0, 120, 50, PT - 80), rect("plinth_stile_r", 300, 120, 350, PT - 80),
        rect("plinth_field", 50, 132, 300, PT - 92, "sunk"),
        rect("plinth_rail_b", 50, 120, 300, 132), rect("plinth_rail_t", 50, PT - 92, 300, PT - 80),
        rect("plinth_cap", 0, PT - 80, 350, PT),
        rect("base_ogee", u0 - 15, PT, u1 + 15, PT + 60, "raised"),
        rect("shaft_bottom_rail", u0, PT + 60, u1, br_top), rect("shaft_stile_l", u0, br_top, 75, 2430),
        rect("shaft_stile_r", 275, br_top, u1, 2430), rect("shaft_field", 75, br_top, 275, 2430, "sunk"),
        rect("shaft_top_rail", u0, 2430, u1, NECK_Z),
    ] + cap_elev
    el_flute = [
        rect("plinth_skirting", 0, 0, 350, 120),
        rect("plinth_stile_l", 0, 120, 50, PT - 80), rect("plinth_stile_r", 300, 120, 350, PT - 80),
        rect("plinth_field", 50, 132, 300, PT - 92, "sunk"),
        rect("plinth_rail_b", 50, 120, 300, 132), rect("plinth_rail_t", 50, PT - 92, 300, PT - 80),
        rect("plinth_cap", 0, PT - 80, 350, PT),
        rect("base_ogee", u0 - 15, PT, u1 + 15, PT + 60, "raised"),
        rect("shaft_bottom_rail", u0, PT + 60, u1, br_top), rect("shaft_top_rail", u0, 2430, u1, NECK_Z),
    ] + [rect("flute_%d" % (k + 1), lo, br_top, hi, 2430, "sunk") for k, (lo, hi) in enumerate(reversed(flute_edges))] + cap_elev
    # the render variant, drawn for a LEFT pilaster (the free side to the right, u = 350): the steps are inset on the free side only
    # (the party side stays flush with its partner); the free-side insets are the slot's 30 mm margin less 8 for the shaft's return
    ins = {"block2": 8.0, "block3": 14.0, "head": 22.0}

    def el_render_for(plinth_top, zs):
        b1, b2, b3 = zs
        return [
            rect("plinth_block1", 0, 0, 350, b1), rect("plinth_block2", 0, b1, 350 - ins["block2"], b2),
            rect("plinth_block3", 0, b2, 350 - ins["block3"], b3),
            rect("plinth_cavetto", 0, b3, 350 - ins["head"], plinth_top - 21),
            rect("plinth_band", 0, plinth_top - 21, 350 - ins["head"], plinth_top),
            rect("shaft", u0, plinth_top, u1, NECK_Z),
        ] + cap_elev
    el_render = el_render_for(PT, (360, 450, head_z))
    el_render_tall = el_render_for(TALL_PLINTH_TOP, (504, 631, 684))
    el_clad = [rect("clad_sheet_1", 0, 0, 350, 1200), rect("clad_sheet_2", 0, 1200, 350, 2400),
               rect("clad_sheet_3", 0, 2400, 350, 2850)]
    return {
        "name": "pilaster",
        "count_per_bay": 2,
        "slot_u": [[0, 350], [5650, 6000]],
        "centre_u": [175, 5825],
        "dims": {
            "slot_width": SLOT, "height": 2850.0, "shaft_width": SHAFT_W, "shaft_proud": SP,
            "shaft_u_in_slot": [u0, u1], "plinth_top_z": PT, "plinth_proud": PP,
            "plinth_width": 350.0, "neck_z": NECK_Z, "capital_height": CAP_H, "capital_top_z": 2850.0,
            "capital_top_width": 350.0, "capital_top_proud": CAP_TOP_PROUD, "capital_flat_top_reaches_d": 172.0,
            "capital_die_d": CAP_DIE_D, "capital_flare_d": [CAP_DIE_D, CAP_FLARE_D],
            "relief_beside_frames": {"rule": "the shaft's face stands at least 40 in front of the front face of every frame beside it (window jamb, shop-door frame, F1 frame)",
                                     "frame_fronts_d": FRAME_FRONT, "min_relief": SP - max(FRAME_FRONT.values()),
                                     "required": 40.0},
            "plinth_top_rule": "Rita's line: the plinth's top is level with the sill's top and the stallriser's (600), on every front; P1's is 1.33 times its sill (variants.plinth_tall)",
            "shaft_bottom_rail_top_z": br_top, "shaft_top_rail_bottom_z": 2430.0,
            "base_ogee": {"proud_of_shaft_face": 15.0, "height": 60.0, "z_range": [PT, PT + 60], "returned_on": "both sides of the shaft (to u 15 and u 335 in the slot)",
                          "kit_proud": 25.0, "why_15": "the cap's flat runs to d 155 and the weathering falls beyond it: a 25 ogee (front d 165) would float 10 over the slope (the second review's narrow point 1)",
                          "used_by": "panel and flute variants (the stepped render variant has a cavetto head instead)"},
            "stepped_head": {"cavetto_z": [head_z, PT - 21], "cavetto_d": [PP - 8, PP - 32], "band_z": [PT - 21, PT], "band_d": PP - 32,
                             "band_in_front_of_shaft": (PP - 32) - SP, "note": "P1: a hollow moulding 77.5 px (134 mm at the pilaster plane, 95 at 800/1123) high setting back about 26, a flat band 17.5 px (21 at 800/1123) on top, the shaft just behind it"},
            "panel_stile_width": 45.0, "panel_sunk_mm": 12.0, "panel_bead_mm": 10.0,
            "flutes": 5, "flute_width": r1(fw), "flute_depth": 12.0, "flute_fillet": 12.0,
            "capital_members_z_local": {"astragal": [0, 24], "neck_fillet": [24, 34], "die": [34, 154],
                                        "flare": [154, 244], "abacus": [244, 296], "top_moulding": [296, 310]},
            "die_tablet_u_in_slot": [90, 260], "die_tablet_proud": 8.0,
            "bosses": {"optional": True, "count": 3, "diameter": 30.0, "proud": 6.0, "pitch": 56.0,
                       "on": "the die's centre line, z_local 94 (the photograph's three roundels)"},
            "downpipe_chase": {"width": 76.0, "from_d": 50.0, "z_ranges": [[0, PT], [2540, 2850]], "at": "each party line (u 0 and 6000): both neighbours' plinths and capitals are notched; the D5 pipe (68 across, axis d 94, front d 128) stands in it, 12 behind the shafts' faces (140)"},
            "backing": "a solid core board 330 wide x 140 deep behind shaft and capital (the kit's backing board, deepened by the 30 the shaft has gained), "
                       "so the faces between pilaster and frames close with no daylight",
        },
        "variants": {
            "panel": {"use": "original timber pilaster: sunk-panelled plinth and shaft on a base ogee (Rita's, the empty unit, fish, chandler, newsagent)",
                      "material": "painted softwood", "elevation": el_panel},
            "flute": {"use": "original timber pilaster with five flutes on a base ogee (the tea room, the ironmonger)",
                      "material": "painted softwood", "elevation": el_flute},
            "render": {"use": "painted render or cement pier on a stepped plinth with a hollow-moulded head (the 1930s grocer; the laundry's re-clad pier)",
                       "material": "painted render, arrises 1 mm eased", "elevation": el_render,
                       "painted_keyline": {"what": "P1's shaft carries a painted line panel, not a moulding: a line 10 wide in a darker, redder tone (about 25 L* below the cream), inset 35 from the shaft's edges, its top corners cut 35 at 45 degrees; z from 1000 to 2400",
                                           "width": 10.0, "inset": 35.0, "corner_cut": 35.0, "z_range": [1000, 2400], "kind": "Photo (texture, not geometry)"},
                       "stepped_plinth_inset_free_side": ins, "step_heights_z": [360, 450, head_z, PT]},
            "clad": {"use": "a 1960s-80s flush clad pier, no plinth, no capital (Mickey's, painted steel): the casing follows the old shaft's face",
                     "material": "steel or aluminium sheet on a timber core, or painted board, 3 sheets", "elevation": el_clad,
                     "dims": {"proud": clad_proud, "width": 350.0, "sheet_joints_z": [1200, 2400], "joint_width": 6.0}},
            "plinth_tall": {"use": "NOT USED by the ten fronts: P1's plinth at the street's scale, 800 high, 1.33 times the sill (R1 = 1.330). It breaks Rita's line (the plinth's top level with the stallriser), so Rita's 600 wins; offered here so that the builder can try it if the plan owner asks. The stepped (render) form: blocks to 504 / 631 / 684, the cavetto 684 to 779, the band 779 to 800; for the panel and flute forms move the plinth cap up 200 (cap 720 to 800), lengthen the stiles and field by 200, move the base ogee and the shaft's bottom rail up 200",
                           "plinth_top_z": TALL_PLINTH_TOP, "elevation": el_render_tall,
                           "side_profile_ref": "profiles.plinth_tall_stepped_side"},
        },
        "profiles": {
            "plinth_cap_side": {"plane": "d-z", "points": pts(plinth_cap),
                                "note": "the timber plinth's cap, the kit's: a 50 mm nose face, a 4 x 6 bead, then the top falling to the street over 21 mm from d 155 to 176 (the kit's steep weathering); the flat (d 0 to 155) takes the shaft's foot and the base ogee (d 140 to 155)"},
            "plinth_panel_side_through_stile": {"plane": "d-z", "points": pts(plinth_panel_stile)},
            "plinth_panel_side_through_field": {"plane": "d-z", "points": pts(plinth_panel_field),
                                                "note": "sunk 12 mm between the stiles; 45 degree sticking at the field's edge; the quarter-round bead is a separate planted piece"},
            "base_ogee": {"plane": "d-z", "points": pts(base_ogee),
                          "note": "the kit's base moulding (pilaster.py BASE) at 15 proud instead of 25 (the second review's points): an ogee 15 proud of the shaft's face and 60 high, standing on the plinth's top (z 600 to 660) wholly on the cap's flat (to d 155), returned on both sides of the shaft; panel and flute variants only (restored: P1 shows a moulding at the shaft's foot)"},
            "plinth_stepped_side": {"plane": "d-z", "points": pts(stepped),
                                    "note": "render variant, P1's members at Rita's 600: block (0 to 360), a step (360 to 450) 4 back, a step (450 to 484) 8 back, a hollow (cavetto, a quarter ellipse centred at d 172, z 579, 24 by 95) from d 172 at z 484 back to d 148 at z 579, a flat band 21 high at d 148 to z 600; the shaft (140) stands 8 behind the band"},
            "plinth_tall_stepped_side": {"plane": "d-z", "points": pts(tall),
                                         "note": "UNUSED variant plinth_tall: P1's own members at 800 (the reviewer's points, 150 -> 180 in d): block 0-504, steps to 631 and 684, the cavetto 684-779 from d 172 to 148, the band 779-800 at d 148"},
            "panel_bead": {"plane": "a-p", "points": pts(bead_qr), "note": "quarter-round, 12 mm, planted in the angle of the sunk field"},
            "shaft_panel_plan": {"plane": "u-d", "points": pts(shaft_panel_plan),
                                 "note": "through the sunk field: 45 mm stiles at full projection (140), the field 12 mm down, a 10 mm quarter-round bead each side"},
            "shaft_flute_plan": {"plane": "u-d", "points": pts(shaft_flute_plan), "note": "five flutes (segmental, 12 deep) between 12 mm fillets"},
            "shaft_render_plan": {"plane": "u-d", "points": pts(shaft_render_plan), "note": "plain face, arrises eased 3 mm by paint build-up"},
            "clad_plan": {"plane": "u-d", "points": pts(clad_plan)},
            "capital_side": {"plane": "d-z", "points": pts(cap_side),
                             "note": "z is local from the neck (add NECK_Z 2540): astragal (r 12), neck fillet, die at d 144 (4 proud of the shaft), a hollow flare 90 high from d 144 to 172, abacus front 175 (52 high), a small ovolo back to d 172 and the flat top at 310 (z 2850), nominally 350 x 175, where the console's toe (240 x 60) and the fascia's bed mould (front 132) stand"},
        },
        "elevation_frame": "u 0..350 across the slot (left pilaster; the right pilaster is the same piece, symmetric), z from the footway",
        "plan_free_side": "the free (opening) side is u = 350 on the left pilaster and u = 0 on the right pilaster; the party side is flush with its partner",
    }


# ---- the console ---------------------------------------------------------------------------------
CONSOLE_DEPTH = 205.0         # under the cornice's 215 nose: the oversail is 10
CONSOLE_FOOT_D = 172.0        # the foot stands on the capital's flat top (which reaches d 172)
CONSOLE_MIN_FRONT = 140.0     # the console's front is at least this far out at every height (the board's face is 120, its mould 132)


def console():
    """A scrolled bracket in a 240 x 205 x 550 envelope (the second review's amendment of the first try's 180: the built fascia_console_01
    stands behind the fascia board's bed mould for most of its height), drawn as a scroll that rises from the front of the capital: a foot
    240 x 172 on the capital's flat, a lower volute (eye d 158, z 48, outer radius 26, reaching d 184), a concave waist (narrowest d 140 at
    z 140), a stem swelling to d 150 at z 330, an upper volute (eye d 160, z 468, outer radius 45: the front reaches d 205 at z 468 and rolls
    back over the top through (160, 513) into the eye) and a cap block 205 deep at z 528 to 550. Judgement: no photograph of a console was
    reached."""
    UC, UR = (160.0, 468.0), 45.0
    LC, LR_ = (158.0, 48.0), 26.0

    def circ(c, r, a0, a1, n):
        return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)), c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]
    zf = LC[1] - math.sqrt(LR_ ** 2 - (CONSOLE_FOOT_D - LC[0]) ** 2)             # where the foot's front (d 172) meets the lower volute
    a0 = math.degrees(math.atan2(zf - LC[1], CONSOLE_FOOT_D - LC[0]))
    lower = circ(LC, LR_, a0, 0.0, 5)[:-1] + circ(LC, LR_, 0.0, 40.0, 4)         # from the foot through the eastern point (d 184 at z 48) to 40 degrees
    p40 = lower[-1]
    waist1 = bezier(p40, (p40[0] - 16.1, p40[1] + 19.2), (140.0, 115.0), (140.0, 140.0), 8)   # concave: d falls to its narrowest, 140 at z 140
    waist2 = bezier((140.0, 140.0), (140.0, 200.0), (150.0, 270.0), (150.0, 330.0), 10)        # swelling to d 150 at z 330
    stem = [(150.0, 330.0), (150.0, 413.0)]
    fillet = circ((160.0, 413.0), 10.0, 180.0, 90.0, 6)                                        # the concave corner under the upper volute
    upper = circ(UC, UR, 270.0, 450.0, 24)                                                    # up the front of the upper volute and over its top
    side = [(0, 0), (CONSOLE_FOOT_D, 0), (CONSOLE_FOOT_D, zf)] + lower[1:] + waist1[1:] + waist2[1:] + stem[1:] + fillet[1:] + upper[1:] + \
        [(160.0, 528.0), (CONSOLE_DEPTH, 528.0), (CONSOLE_DEPTH, 550.0), (0.0, 550.0)]
    side = dedupe(side)

    # the side grooves follow the outline 8 mm inside it (5 wide, 4 deep) and wind into an eye boss 16 across, 3 proud
    def spiral_cw_or_ccw(c, r_start, r_end, turns, flat_deg, sign, n=48):
        out = []
        total = 360.0 * turns
        for k in range(n + 1):
            th = total * k / n
            if th <= flat_deg:
                r = r_start
            else:
                r = r_start + (r_end - r_start) * (th - flat_deg) / (total - flat_deg)
            a = math.radians(sign * th)
            out.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a)))
        return out
    g_up = spiral_cw_or_ccw(UC, 37.0, 10.0, 1.25, 90.0, +1)          # counter-clockwise from the front, over the top, into the eye
    g_lo = spiral_cw_or_ccw(LC, 18.0, 11.0, 1.0, 0.0, -1, n=32)      # clockwise: rolling the other way
    boss_up = circ(UC, 8.0, 0.0, 360.0, 16)[:-1]
    boss_lo = circ(LC, 8.0, 0.0, 360.0, 16)[:-1]

    # the leaf on the front face (u from the console's centre line, z local): an acanthus pendant, 3 lobes, between z 150 and 420
    def leaf_outline():
        right = []
        for z, w in [(440, 58), (420, 60), (396, 52), (384, 46), (368, 54), (344, 50), (330, 42), (312, 48), (288, 42),
                     (272, 34), (252, 38), (232, 30), (212, 24), (190, 18), (160, 9), (120, 0)]:
            right.append((w, 150.0 + (z - 120.0) * 270.0 / 320.0))          # the first try's 120..440 squeezed into 150..420
        left = [(-u, z) for u, z in reversed(right[:-1])]
        return right + left
    leaf = leaf_outline()
    plan = [(-120, 0), (120, 0), (120, CONSOLE_DEPTH - 12), (108, CONSOLE_DEPTH), (-108, CONSOLE_DEPTH), (-120, CONSOLE_DEPTH - 12)]
    front_el = [{"name": "face", "kind": "face", "pts": [[-120, 0], [120, 0], [120, 550], [-120, 550]]},
                {"name": "leaf", "kind": "relief", "pts": [[round(a, 1), round(b, 1)] for a, b in leaf]}]
    return {
        "name": "console",
        "count_per_bay": 2,
        "centre_u": [175, 5825],
        "u_range": [[55, 295], [5705, 5945]],
        "dims": {"width": 240.0, "depth": CONSOLE_DEPTH, "height": 550.0, "z_bottom": 2850.0, "z_top": 3400.0,
                 "toe_depth": CONSOLE_FOOT_D, "toe_width": 240.0, "side_chamfer": 12.0,
                 "min_front_d": CONSOLE_MIN_FRONT,
                 "front_rule": "the console's front stands at least d 140 at every height from 2850 to 3400, in front of the fascia board's bed mould (132) and face (120), so no board end is exposed beside the console; the board's ends are let into the console's sides behind its front",
                 "foot_on_capital": "the foot (240 x 172 at z 2850) stands on the capital's flat top (which reaches d 172; nominally 350 x 175), so the console rises from the capital's front; the lower volute reaches d 184, 9 past the capital's front (175)",
                 "cap_block": {"d": CONSOLE_DEPTH, "z_local": [528.0, 550.0]},
                 "upper_volute": {"eye_dz": [160.0, 468.0], "outer_radius": 45.0, "front_d_at_eye_z": CONSOLE_DEPTH, "top_point_dz": [160.0, 513.0], "turns": 1.25,
                                  "direction": "counter-clockwise seen with the street to the right: up the front, over the top, back and down into the eye"},
                 "waist": {"narrowest_d": 140.0, "at_z_local": 140.0, "concave": True},
                 "stem": {"d_at_z_local_330": 150.0},
                 "lower_volute": {"eye_dz": [158.0, 48.0], "outer_radius": 26.0, "reach_d_at_eye_z": 184.0, "direction": "clockwise inward: rolling the other way"},
                 "side_grooves": {"inset_from_outline": 8.0, "width": 5.0, "depth": 4.0, "eye_boss_diameter": 16.0, "eye_boss_proud": 3.0,
                                  "upper": "from the front at r 37 round the top and into the eye in 1.25 turns (r 37 to 10)", "lower": "one turn clockwise (r 18 to 11)"},
                 "leaf": {"height": 270, "z_local": [150, 420], "max_half_width": 60, "relief_mm": 12,
                          "lobes_per_side": 3, "rib": "a raised central rib 8 wide, 4 proud of the leaf's dome",
                          "groove_between_lobes": {"width": 4, "depth": 3}}},
        "variants": {
            "scroll": {"use": "the original console: two volutes joined by a concave waist under a cap block, an acanthus leaf on the face (all original fronts)",
                       "elevation": front_el},
            "block": {"use": "a plain block console (the 1930s grocer): the same 240 x 205 x 550 envelope, flaring from the 172 foot to the 205 cap, no leaf, three bosses; its front is at least 172 at every height",
                      "points_side": pts([(0, 0), (172, 0), (172, 40), (205, 300), (205, 550), (0, 550)])},
            "absent": {"use": "console gone: the foot's stump (172 x 240 x 90) and the screw holes remain on the capital (the empty unit's left console)"},
        },
        "profiles": {
            "side_silhouette": {"plane": "d-z", "points": pts(side),
                                "note": "z local from the console's foot (add 2850); wall at d=0 (back), the cornice's soffit meets the top. A scroll that rises from the front of the capital: the foot 172 deep, the lower volute (eye 158, 48, r 26, reaching d 184), a concave waist (narrowest d 140 at z 140), a stem swelling to d 150 at z 330, a concave fillet under the upper volute (eye 160, 468, r 45: front d 205 at z 468, top (160, 513)), then the cap block (d 205, z 528 to 550) over a notch 15 high at the volute's top. The front is at least 140 at every height. Judgement; the first piece to check against a reached photograph"},
            "plan_at_neck": {"plane": "u-d", "points": pts(plan), "note": "240 wide, 12 mm chamfer down each front edge (the built mesh's per-station taper)"},
            "volute_upper_spiral": {"plane": "d-z", "points": pts(g_up, closed=False),
                                    "note": "centreline of the groove cut in each side face: 8 inside the outline at the front, then winding into the eye (160, 468) in 1.25 turns, r 37 to 10; 5 wide, 4 deep"},
            "volute_lower_spiral": {"plane": "d-z", "points": pts(g_lo, closed=False),
                                    "note": "centreline of the lower groove: one turn clockwise about (158, 48), r 18 to 11; 5 wide, 4 deep"},
            "eye_boss_upper": {"plane": "d-z", "points": pts(boss_up), "note": "a boss 16 across, 3 proud, at the upper eye (160, 468)"},
            "eye_boss_lower": {"plane": "d-z", "points": pts(boss_lo), "note": "a boss 16 across, 3 proud, at the lower eye (158, 48)"},
            "leaf_outline": {"plane": "u-z", "points": pts(leaf), "note": "u from the console's centre line, z local 150 to 420; relief domed 12 mm at the rib, 0 at the outline"},
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
                                 "note": "z local from the board's foot (2850); the bed mould's front stands 12 proud of the face and 43 behind the capital's top front (175), so the board's foot stands wholly on the capitals' tops"}},
        "ends": "each end is let into the console's side with a 12 mm rebate; at the capital the foot rests on the abacus for 55 mm (u 295 to 350)",
        "variants": {"timber": "the original board (O fronts)", "boxed": "the old board with a plastic box or flat panel screwed over it (fascia target)",
                     "glass": "the grocer's board is a reverse-painted glass fascia in three slabs on a timber backing, the same plane"},
    }


def cornice():
    # (d, z local from the cornice's soffit at 3400), the built envelope 215 x 150, drip groove kept at 155 to 175
    p = [(0, 0), (155, 0), (155, 12), (175, 12), (175, 0), (215, 0), (215, 52), (211, 56), (211, 60),
         (205, 68), (201, 76), (200, 86), (203, 90), (207, 98), (208, 110), (207, 124), (205, 130), (150, 150), (0, 150)]
    p = dedupe(p)
    sec = pts(p)
    D = CORNICE_DEPTH
    # the mitred returns at the two ends (the party-wall gaps): the nose line turns through 90 degrees and runs back to the wall; the
    # section, turned 90 degrees, shows in elevation: left end u = 54 + (215 - d), right end u = 5731 + d (u 54..269 and 5731..5946)
    ret_left = [(54.0 + D - d, z) for d, z in sec]
    ret_right = [(5946.0 - D + d, z) for d, z in sec]
    plan_front = [(54.0 + D, 0.0), (5946.0 - D, 0.0), (5946.0, D), (54.0, D)]
    plan_left = [(54.0, 0.0), (54.0 + D, 0.0), (54.0, D)]
    plan_right = [(5946.0 - D, 0.0), (5946.0, 0.0), (5946.0, D)]
    return {
        "name": "cornice",
        "count_per_bay": 1,
        "dims": {"length": 5892.0, "u_range": [54, 5946], "depth": 215.0, "height": 150.0, "z_bottom": 3400.0, "z_top": 3550.0,
                 "drip_groove": {"d_range": [155, 175], "depth": 12.0},
                 "stops_each_end": 54.0,
                 "reason_for_length": "the D5 downpipe at each party wall stands 94 from the wall, 68 across: 6000 - 68 - 2 x 20 = 5892 (fascia-01 spec)",
                 "lead": "a 1.8 mm lead apron over the wash, turned 100 up the wall behind (a grey line on the brick), dressed down over each return with a 25 upstand where it meets the wall; not geometry",
                 "wash_slope_deg": round(math.degrees(math.atan((150 - 130) / (205 - 150))), 1),
                 "corona_face": [0, 52], "corona_face_fraction_of_height": round(52 / 150, 3)},
        "ends": {
            "kind": "mitred return",
            "rule": "each end of the run is closed by a mitred return of the full 19-point section: the moulding turns through 90 degrees at the mitre (a 45 degree line in plan from the wall at u 269 / 5731 to the nose corner at u 54 / 5946) and runs back to the wall, 215 deep, so the nose line keeps the full 5892 (u 54 to 5946) and the back (soffit and wall line) is 5462 (u 269 to 5731); seen from the street at an angle the end is a moulded face, not an open box",
            "return_depth": D,
            "plan_note": "plan in u (right) and d (up the page, the wall at d 0); the returns are the two right triangles with 215 legs, the front run the trapezoid between them",
            "faces_outward": "the returns' moulded faces look along -u (left end) and +u (right end); the section turned 90 degrees (profiles.return_left_uz / return_right_uz, u from the end plane, z local from the soffit)",
            "lead": "the lead apron is dressed down over each return with a 25 upstand; a lead flashing 100 up the wall behind, as the front run",
        },
        "profiles": {"section": {"plane": "d-z", "points": sec,
                                 "note": "z local from the soffit (3400): flat soffit, drip groove 12 deep, a tall corona face 52 (0.35 of the height: Judgement), a fillet, a cyma reversa back to d 200 at z 86, a fillet, a cap ovolo out to d 208 at z 110, a short face, then the wash falling 20 mm over 55 mm to a flat top at 150 that runs back to the wall"},
                     "return_left_uz": {"plane": "u-z", "points": pts(ret_left),
                                        "note": "the section turned 90 degrees at the left end: u = 54 + (215 - d), nose at u 54, back at u 269; z local from the soffit"},
                     "return_right_uz": {"plane": "u-z", "points": pts(ret_right),
                                         "note": "the section turned 90 degrees at the right end: u = 5731 + d, back at u 5731, nose at u 5946"},
                     "plan_front_run": {"plane": "u-d", "points": pts(plan_front), "note": "plan of the front run between the mitres"},
                     "plan_return_left": {"plane": "u-d", "points": pts(plan_left), "note": "plan of the left return: a right triangle, legs 215, the mitre its hypotenuse"},
                     "plan_return_right": {"plane": "u-d", "points": pts(plan_right), "note": "plan of the right return"}},
        "joints": ["a 45 degree scarf in the timber every 2.4 m at most (none visible on a 5.9 m run, painted over); a butt at each console's side is not needed (the cornice runs over the consoles' tops)",
                   "a 45 degree mitre at each end, glued and cramped, with a loose tongue; the return's back is screwed to the wall plate"],
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
                 "plinth_meets_pilaster": "the stallriser's ends butt the pilaster plinths' sides at u 350 / 5650; its face (125) is 55 behind the plinth's front (180) and 25 behind the sill's nose (150)"},
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
                 "sits_on": "the sill's flat bed (z 600) through a 25 mm seat (the glazing rebate's foot and its bead): the lights stand on the sill, as P1's sill group is the glazing rebate's foot, and the glass starts within 25 of the shop door's glass beside it",
                 "bottom_rail": [600, 625], "transom": list(TRANSOM), "head": list(HEAD),
                 "lower_lights_z": [625, 2400], "toplights_z": [2480, 2790],
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
                 "leaf_foot_z": 28.0, "leaf_top_z": 2068.0,
                 "z_note": "every z below is a height above the footway, as the sill's 600; the leaf's foot stands 28 up (the threshold's 25 + 3 clear), so the bottom rail is 202 clear",
                 "frame_jamb_face": 50.0, "frame_depth": 100.0, "leaf_front_d": 70.0,
                 "stile": 115.0, "top_rail": 115.0, "top_rail_z": [1953.0, 2068.0], "lock_rail": [490.0, 600.0], "bottom_rail": [0.0, 230.0],
                 "lower_panel": [230.0, 490.0], "glazed_from": 600.0, "glazed_to": 1953.0,
                 "glazed_fraction_of_leaf_from": round(600.0 / 2040.0, 3),
                 "glazed_fraction_note": "glazed_from over the leaf's height, both from the footway (600 / 2040); counted from the leaf's own foot (28 up) it is 572 / 2040 = 0.280",
                 "glazed_from_rule": "level with the window's sill top (600) on every timber (T1) and 1930s (M2) front: the door's glass line and the sill line run on as one line along the shopfront (P1: within 46 mm; Coventry: the door's bottom panel the stallriser's height)",
                 "kick_plate": {"height": 170.0, "width": 770.0, "metal": "brass", "screws": 8, "z_range": [28.0, 198.0], "used_by": "T1 (Rita's model)"},
                 "foot_strip": {"height": 30.0, "metal": "brass", "proud": 3.0, "z_range": [28.0, 58.0],
                                "note": "the strip is the plate's lowest 30 mm, a separate bar 3 proud over the plate's foot (P1 shows a strip over a bare leaf; the game's Rita door a plate): on a door without a kick plate (M1, M2) it stands alone"},
                 "threshold": "terrazzo or tiled, 25 at the leaf falling to 12 at a rounded nose out on the pavement, the full frame width",
                 "fanlight": {"z_range": [2131, 2400], "bars": "none (one pane) or two bars when the door is wider"},
                 "transom": list(TRANSOM), "head": list(HEAD), "above_transom": "toplight with 2 bars (as the kit)",
                 "hinges": {"count": 3, "size": "100 x 75 butt, brass or steel, at 150 from top, 150 from bottom, middle", "screws": 6,
                            "side": "on the window side of the leaf (the end away from the side door or the pier); shops[].shop_door_hinge_viewer gives the viewer's side"},
                 "handing": {"rule": "taken from Rita's front in the game today (rita-day-kit-2026-10-06.jpg): the shop door's lever is on the leaf's LEFT edge, the side-door side, so it is hinged on the window side (the viewer's right in Rita's, whose doors are on the viewer's left); the same rule on a front with its doors on the right gives the mirror: hinged on the viewer's left, the lever on the viewer's right. The grocer (no side door): hinged on the window side, the lever on the pier side. The letter plate is centred on the leaf's width on every door",
                             "lever_side": "the edge opposite the hinges (the viewer's side of the door end)",
                             "fields": "shops[].shop_door_hinge_viewer, shop_door_lever_viewer, side_door_hinge_viewer, side_door_knob_viewer, letter_plate_viewer",
                             "game_today_note": "the street's recipe (terrace-front.py _kit_shopfront) places the kit's door by translation only, so every bay carries Rita's handing; this target gives the five mirrored fronts (Mickey's, fish, empty unit, ironmonger, newsagent) the mirror: a change for the builder"},
                 "furniture": {"lever_handles": {"z": 1000.0, "pair": True, "backplate": [240, 40], "metal": "brass", "edge": "the lock edge, opposite the hinges"},
                               "latch": "a rim night-latch (cylinder and case) on the inside, a mortice lock's keyhole escutcheon on the lock stile at z 950",
                               "letter_plate": {"width": 250.0, "height": 40.0, "z": 545.0, "z_range": [525.0, 565.0], "on": "the lock rail (490 to 600), 35 clear above and below, centred on the leaf's width"},
                               "push_plate": "none on timber doors",
                               "seen_in_P1_not_adopted": "P1's double doors carry octagonal brass knobs on the lock rail and long brass pull plates: an alternative to the lever set for a 1900s front (Judgement: a 65 mm octagonal knob on the lock rail at z 545)"}},
        "profiles": {"threshold_section": {"plane": "d-z", "points": pts(thr)},
                     "leaf_stile_plan": {"plane": "u-d", "points": pts([(0, 70), (115, 70), (115, 20), (101, 20), (101, 31), (89, 31), (89, 20), (0, 20)]),
                                         "note": "the leaf's stile (u across, d out; the leaf's outside face at d 70, inside at 20): 115 face, 50 thick; the glass rebate and the ovolo bead are on the glazing side; the 12 mm sticking on the panel side is a_p below"},
                     "frame_jamb_plan": {"plane": "u-d", "points": pts([(0, 0), (50, 0), (50, 100), (0, 100), (0, 78), (14, 78), (14, 36), (0, 36)]),
                                         "note": "the door frame's jamb: 50 face x 100 deep, rebated 14 x 42 for the leaf's stop; the leaf's face stands 30 behind the frame's face"},
                     "raised_field_edge": {"plane": "a-p", "points": pts([(32, 0), (60, 0), (60, 10), (40, 10)]), "note": "a raised and fielded panel: a flat margin 32, a bevel 8 rising 10, the field; as the kit"},
                     "glazing_bead": {"plane": "a-p", "points": pts([(0, 0), (14, 0), (14, 2), (12, 6), (8, 9.5), (4, 11), (0, 11)]), "note": "T1: ovolo 14 x 11"}},
        "variants": {"T1": "half-glazed timber leaf, glazed from 600: bottom rail, one raised and fielded lower panel (230 to 490), a lock rail 110 high carrying the letter plate (Rita's, empty, tea, ironmonger, newsagent)",
                     "M1": "aluminium-framed glass door 900 x 2040: 50 stiles, 100 top rail, 170 bottom rail, a 300 chrome D pull and a push plate (fish, laundry, chandler, Mickey's); its glass runs from the bottom rail, so the door-glass-level rule is not asked of it",
                     "M2": "bronze-framed glass door with a bronze kick panel to 600 (level with the lobby's kick panels and the sill), glazed from 600 (grocer, 1930s)"},
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
            "y": "F1 y = 0 is its brick face; its frame's outside face is at F1 y 114.3. In the bay the frame's outside face stands at d = 100 (flush with the shop door's frame, 40 behind the pilaster shaft's face, 140): d = 214.3 - y_F1, i.e. the leaf's outside face (F1 188.3) is at d 26",
            "hinge": "the leaf is hinged on the SHOP-DOOR side (the viewer's right where the doors are on the left, as Rita's; its knob and lock on the pier side). The front-door target gives optional butts on F1's left stile seen from outside (its 'Hinges' row) and a centred knob: F1 is therefore used mirrored where the door end is the viewer's left (Rita's), and as drawn where it is the viewer's right. Measured on the game's Rita frame (rita-day-kit-2026-10-06.jpg, 1600 x 900): the side door's leaf spans x 215.7 to 397.3 and its two knobs stand at x 225.7 and 220.0, in the leaf's left tenth: the knob is on the pier side, not the shop-door side",
            "z": "F1 z 0 is the top of its threshold, 45 above the pavement (F1 ground z -45): z_bay = z_F1 + 45. Its head's visible face (F1 2339.6 to 2400) therefore reaches z 2445: the shop transom (2400 to 2480) covers the top 45, so the builder trims the F1 head at z 2400",
            "trim": ["the threshold board's front (F1 y 0, d 214) is cut back to d 130, flush with the shop door's threshold nose and 50 behind the plinth's front (180)",
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
