"""The kit pieces, the gate, the checks, the photographs-win list and what could not be settled (cloud week 42, unit 8). Merged into target.json by make_target.py."""
import hw_common as H
import hw_data as D

PIECE_DIR = "production/assets/cloud-week/house-windows"


def kit_pieces(target):
    sites = target["sites"]
    nets = D.NETS
    nodes_extra = {}
    for kind in ("S22", "S11", "RC"):
        plane = {k: nets[k]["plane_mm"][kind] for k in ("N1", "N2", "N3")}
        nodes = []
        if kind == "S22":
            gl = [n for n in target["kinds"]["S22"]["lab_nodes"] if n["name"].startswith("glass__")]
            for n in gl:
                lo = "lower" in n["name"]
                for side, (a, b) in (("L", (n["x"][0], -4.7)), ("R", (4.7, n["x"][1]))):
                    nodes.append({"name": "glass__%s_%s" % ("lower" if lo else "upper", side), "material": "glass_house", "x": [a, b], "y_into_wall": n["y_into_wall"], "z_up": n["z_up"],
                                  "note": "the lab's glass sheet split at the bar: each pane runs to the bar's fillet (4.7 from the middle, the putty's inner edge), 2.5 thick"})
        elif kind == "S11":
            for n in [n for n in target["kinds"]["S11"]["lab_nodes"] if n["name"].startswith("glass__")]:
                nodes.append({"name": n["name"].replace("glass__", "glass__").replace("_glass", ""), "material": "glass_house", "x": n["x"], "y_into_wall": n["y_into_wall"], "z_up": n["z_up"], "note": "the lab's sheet, one pane a sash"})
        else:
            for p in target["kinds"]["RC"]["parts_mm"]:
                if p.get("material") == "glass_house":
                    nodes.append({"name": "glass__" + p["name"].replace("glass_", ""), "material": "glass_house", "x": p["x"], "y_into_wall": p["y_into_wall"], "z_up": p["z_up"], "note": "4 mm, one pane drawn for the sealed unit"})
        for k in ("N1", "N2", "N3"):
            c = nets[k]["card"]
            nodes.append({"name": "net__" + k, "material": "net_voile" if k != "N3" else "net_voile", "x": c["x"], "y_into_wall": [plane[k], plane[k] + 1], "z_up": c["z"], "note": "a flat card, alpha = the weave and folds (NET_COMMON); one of N1, N2, N3 or none is switched on per house"})
        for k, c in D.CURTAINS.items():
            if k == "C1":
                nodes.append({"name": "curtain__C1_drawn", "material": "curtain", "x": c["card"]["x"], "y_into_wall": [c["plane_mm"], c["plane_mm"] + 1], "z_up": c["card"]["z"], "note": "drawn across; colour per house"})
            else:
                nodes.append({"name": "curtain__C2_open_L", "material": "curtain", "x": c["card_left"]["x"], "y_into_wall": [c["plane_mm"], c["plane_mm"] + 1], "z_up": c["card_left"]["z"], "note": "drawn back, left"})
                nodes.append({"name": "curtain__C2_open_R", "material": "curtain", "x": c["card_right"]["x"], "y_into_wall": [c["plane_mm"], c["plane_mm"] + 1], "z_up": c["card_right"]["z"], "note": "drawn back, right"})
        for k, c in D.BLINDS.items():
            nodes.append({"name": "blind__" + k, "material": "blind", "x": c["card"]["x"], "y_into_wall": [c["plane_mm"], c["plane_mm"] + 1], "z_up": c["card"]["z"], "note": c["label"]})
        # the pendant and the room card for the upper windows (centred on the window)
        nodes.append({"name": "pendant__shade", "material": "pendant_shade", "x": [-170, 170], "y_into_wall": [650, 990], "z_up": [1536, 1776], "note": "a paper shade 340 across and 240 high, 0.55 behind the card, its top 0.30 below the ceiling; emissive only in a lit room; present where the room's `pendant` is true; the one real object in the room (the picture's ceiling carries its rose)"})
        nodes_extra[kind] = nodes
    pieces = {
        "frame": "kit frame (units): x across the window, y into the wall (0 at the brick face), z up (0 at the opening's bottom edge); the lab glb's frame is glTF y-up with the wall at negative z: kit (x, y, z) = (x_glb, -z_glb, y_glb)",
        "pivot": "the opening's bottom-edge centre on the brick face: (0, 0, 0); the street toward -y; z up; metres, scale 1",
        "placement": {"east": "translate (x_centre, +5.125, sill_z_above_crown); the street is at -y, no turn", "west": "turn 180 degrees about z, then translate (x_centre, -5.125, sill_z_above_crown)",
                      "sill_z": "above the crown: the site's `sill_z_above_crown` (the opening's bottom edge); the stone sill and the arch ring belong to the wall kit"},
        "files": {k: "%s/hw_%s.glb" % (PIECE_DIR, k) for k in ("S22", "S11", "RC")},
        "extra_files": {"room_card_gf": "%s/hw_room_card_gf.glb (the cottages' shared room card, one per house, placed between its two windows)" % PIECE_DIR},
        "per_kind": {kind: {"reused_nodes": (len(target["kinds"][kind].get("lab_nodes", [])) if kind != "RC" else 0), "added_nodes": nodes_extra[kind]} for kind in nodes_extra},
        "materials": {"paint_<paint name>": "per house, colour from `paints`; roughness per paint; vertex colour R multiplies (BOX_SHADE)", "glass_house": "the pane material (GLASS.pane): one per pane id so each pane's tilt is its own node",
                      "net_voile": "alpha-textured card: the weave and folds (NET_COMMON), colour white, greyed or yellowed per house", "curtain": "colour per house (CURTAINS), folds as a normal and a brightness map, opacity 0.97",
                      "blind": "slat texture with the gap alpha (BLINDS)", "pendant_shade": "paper, emissive in night_lit only", "room_card": "plain quad; the game's M_LedgerInterior takes CardOrigin, RoomSize, CamD, Side, three textures and Night, LitOn, Brightness: the quad has no UVs that matter"},
        "room_card": {"upper": {"node": "room__card", "plane_mm": 270, "x": [-1400, 1400], "z_up": [-473.6, 2076.4], "size_m": [2.8, 2.55], "note": "centred on the window; floor level 473.6 below the opening's bottom, ceiling 2076.4 above it"},
                      "cottage": "room_card_gf: 3.4 x 2.6, centred between the house's two windows (each window's place in it is sites[].card.window_in_card_m), its floor 373.6 mm below the opening's bottom and its ceiling 2226.4 mm above it; both windows look into the same card and the same picture"},
        "budget": {"triangles_each_kind": 6000, "bytes_each_glb": 400000, "note": "the lab's 2/2 is 2,000 or so triangles; nets, curtains and blinds are cards (2 triangles each); the push guard allows 1 MB a model in git"},
        "how_it_goes_into_the_game": ["terrace-front.py: SASH_KIT_ROWS to None (every row takes the period opening 850 x 1676.4: the cottages' sill goes to 0.8236 above the crown, 0.7236 above the threshold, the head kept at 2.5), and `_plain_ground` to follow `_window_kind` (it draws every cottage window as a 2/2 today)",
                                      "HOUSE_PANE_TRANSLUCENT stays False: the glass is the pane material, the net card behind it; the translucent pane stays shops' only",
                                      "held props: one glb per kind, placed by `sites[]` (HANDOVER.md steps 1 to 4); the room pictures are rebuilt on the PC by their one command and imported as textures (sRGB, no mips below 256)",
                                      "M_LedgerInterior parameters per site from `sites[].card` (CardOrigin, RoomSize, CamD, Side) and the picture ids; Night and LitOn from the lit table; Brightness day 0.12, night 0.7",
                                      "the wall kit takes the reveal's brick returns' shade (BOX_SHADE.brick_returns_of_the_reveal) and the carcass behind the card (its front face at 0.29 m or more)"],
    }
    return pieces


def gate(target):
    cams = {}
    for name, c in H.CAMERAS.items():
        cams[name] = {"what": c["what"], "spec": [c["spec"][0], c["spec"][1], c["spec"][2]], "vfov_deg": c["vfov_deg"], "resolution": [2560, 1440], "eye_above_footway_m": 1.6}
    return {
        "what": "what the cloud shows without Unreal: a house front built from the kit pieces, its neighbours, the opposite row as proxies, the street's lamps and sky, the room cards baked through the game's `trace`, the pane drawn as the game draws it (GLASS.pane.cloud_stand_in)",
        "scene": {"engine": "Blender 5.2 Cycles, CPU, 2560 x 1440 (the dark lines are 6 mm: 1.4 pixel at 8.8 m; do not render smaller), 48 samples, OpenImageDenoise, Standard view transform, film not transparent",
                  "house_sets": {"GS_A": "east_parade bays 1, 2, 3 and neighbours (bay 0 and 4 as plain blocks): the S11, RC and S22 houses; the unlet house; the wall kit's brick, sills and arches (stand-ins from the street file's materials are enough)",
                                 "GS_B": "west_south bays 0, 1, 2 (the three cottages) with the door, the plinth and the wall, and one house of the east parade opposite as proxy"},
                  "opposite_row_proxies": "boxes at the street file's numbers: east parade eaves 6.3 above the crown, pitch 35 degrees, depth 8; west cottages eaves 3.1 above the crown, pitch 40; the hill and sky as the dome",
                  "street": "road 6 m crowned 0.075, footways 2 m at crown + 0.10, kerb 0.125 up; the four lamp columns at x 8, 18, 28, 38 (stand-ins)",
                  "sky": "the overcast dome (Poly Haven belfast_open_field_2k, CC0, the scene file's own), sun off; the world's strength is calibrated so that a Lambertian grey card (albedo 0.18) facing the street reads linear 0.18 +- 0.01 (sRGB 118 +- 4) in the render's own pixels",
                  "night": "dome x 0.15 (unreal-look.json sky_seen_gain_night), the four lamps: point lights (linear (1.0, 0.25, 0.0) = lantern_linear_rgb) at 4.78 m, power set so the paving under the near lamp reads sRGB 150 +- 20; the lit windows by the table at 20:30 (`rooms.lit_share.lit_by_hour`): lit room card (night_lit picture x 0.7 x room_glow_gain_night 0.4), lit net emissive 0.48; the rest night_dark",
                  "room_cards": "for every window and every camera the card's emission picture is computed per pixel through `tools/ue/make_interior_material.py` `trace` (imported, not rewritten) from the room's picture and set as the card's emission; a lit room has its net and curtain cards emissive as NET_COMMON says; a dark one is lit by the sodium wash only",
                  "passes": "Cycles passes: Material Index (pane = 1 glass_house, frame = 2 paint_*, net/curtain/blind = 3, brick/wall = 4, card = 5), Object Index per window (id), Z; the masks come from these, never by eye"},
        "cameras": cams,
        "views": "GS_A: H_ACROSS_0, H_ACROSS_30, H_ALONG_15_NEAR, H_ALONG_30_NEAR, H_ALONG_15_ROAD by day and by night (20:30), H_UNDER by day; GS_B: from the east footway's kerb edge (H_ACROSS_0, H_ACROSS_30), and along the cottages' own footway (H_ALONG_15_NEAR, H_ALONG_30_NEAR, H_ALONG_15_ROAD), by day and by night; 22 renders",
        "measure": {
            "P": "the median sRGB luma of a window's pane pixels (material index 1 and 3 inside the window's outline: glass and net together as the eye sees them)",
            "L": "the 90th percentile of the luma of the window's joinery pixels (material index 2: the sash members, linings, beads, sill)",
            "D": "the 5th percentile of the luma over the window's outline (joinery and pane pixels, no brick)",
            "spread": "the pane pixels' 95th minus 5th percentile",
            "angle": "the angle from the wall at which the window's centre is seen from the camera, from the scene's geometry (not from the picture)",
            "window_state": "its net class (sites[].net.kind with N0 = bare) and its time (day, or night lit or dark)",
            "bands_come_from": "photo_measurements.bands_by_state (Photo, +-5 degrees on the angle, outlines by eye)",
        },
        "bands": {
            "net_N1_N2_in_15_to_30_deg": {"P_over_L": [0.55, 0.95], "D_over_L_max": 0.55, "spread_min": 40, "photo": "P1_a, P1_b, P1_e at 31 to 37 degrees: 0.83, 0.87, 0.85 (D/L 0.47 to 0.50); the nine net windows 0.60 to 0.97"},
            "net_N3_cafe": {"P_over_L": [0.35, 0.75], "photo": "P4_E (a net over the lower half, 35 degrees): 0.56"},
            "bare_N0_in_15_to_30_deg": {"P_over_L": [0.10, 0.45], "spread_min": 20, "photo": "P1_c (22 degrees) 0.32; P4_G 0.19; P3_d 0.36"},
            "bare_N0_over_60_deg_from_across": {"P_over_L": [0.35, 0.70], "blue_over_red_min": 10, "photo": "P8_L, P8_R (near square, from below, sky over a dark room): 0.62, 0.51; the pane's colour (87, 99, 135): blue over red 48"},
            "old_fault_to_fail": {"P_over_L": 0.85, "D_over_L": 0.85, "spread": 14, "source": "1a: pane 157 to 175 against paint 178 to 205, the lace uniform, no corner line; the checks below must fail this"},
        },
    }


def checks(target):
    C = []

    def add(cid, group, name, measure, expected, tol, applies, kind, src):
        C.append({"id": cid, "group": group, "name": name, "measure": measure, "expected": expected, "tolerance": tol, "applies_to": applies, "kind": kind, "source": src})
    # ---- the kit's geometry
    add("KIT-01", "kit", "the opening", "bounding box of the glass-plus-frame nodes' outer lining in x and z of each kit", "850.0 wide, 1676.4 high (the frame's outer lining at the brick line)", "+-0.5 mm", "S22 S11 RC", "Read", "lab target.json opening; ruling of 8 October")
    add("KIT-02", "kit", "pivot", "the bounding box of the whole piece in the kit frame", "x centred on 0 (+-1 mm), z min 0 (+-0.5 mm), y (into the wall) min 0 within 115 mm (the lab's oak sill reaches 108.3 in front of the opening's inner lining but not past the brick face)", "+-1 mm", "S22 S11 RC", "Derived", "HANDOVER.md pivot rule")
    add("KIT-03", "kit", "glass planes", "the y (into the wall) of each pane node's front face", "S22/S11: upper panes 142.0, lower panes 190.0; RC: both 112.5", "+-1.0 mm", "S22 S11 RC", "Read", "1a section 2; the lab glb; RC Judgement from the photographs' frames")
    add("KIT-04", "kit", "one mesh a pane", "count of nodes named glass__*", "S22 4, S11 2, RC 2", "exact", "S22 S11 RC", "Derived", "per-pane tilt needs per-pane meshes")
    add("KIT-05", "kit", "pane tilt", "the rotation of each glass node about the vertical and horizontal axes", "each within +-0.5 degrees vertical axis and +-0.3 degrees horizontal, none exactly zero, a window's panes spread at least 0.3 degrees", "exact bounds", "S22 S11 RC", "Photo", "P8: panes 86 to 105 mean luma, +-10 per cent; 1a step 3 0.5 to 1 degree")
    add("KIT-06", "kit", "net cards", "the node `net__N1`, `N2`, `N3`: x and z extents and the y plane", "N1 x +-450, z 60 to 880; N2 x +-450, z 60 to 1630; N3 x +-430, z 100 to 500; planes S22/S11 254, RC 235 behind the face", "+-1 mm", "S22 S11 RC", "Judgement", "NETS; photographs P1 to P7")
    add("KIT-07", "kit", "net inside the box", "the net plane minus the pane's rear face", "S22/S11 lower pane: 254 - 190 = 64 mm or more; no net node crosses a joinery node", "no intersection", "S22 S11 RC", "Derived", "1a: nets behind the sashes")
    add("KIT-08", "kit", "the room card", "node `room__card` (upper windows): size, plane, UV range and the world's CardOrigin from sites[].card", "2.8 x 2.55 m, plane 270 +-1 mm behind the face, centred on the window (+-1 mm), floor 473.6 below the opening's bottom", "+-1 mm", "S22 S11 RC (upper)", "Derived", "trace rule; shop-windows target 3")
    add("KIT-09", "kit", "vertex colour on the joinery", "COLOR_0 on every joinery vertex; the red channel's values", "present on all; min >= 0.25; lining faces 1.0 at the brick edge falling to 0.6 +-0.05 at the glass; track faces 0.50 +-0.08; inside corners within 8 mm: 0.30 +-0.10; putty strips 0.35 +-0.05; meeting rail underside 0.40 +-0.08", "as stated", "S22 S11 RC", "Judgement", "1a step 2, BOX_SHADE")
    add("KIT-10", "kit", "the dark lines are wide enough", "every shade step or gap that the box draws as a line (putty strip, parting bead gap, weld groove, gasket)", "at least 6 mm wide (the putty strip 6.4, the parting bead gap 2.0 stays a geometric gap of 2 mm with its shade painted 0.10 over 6 mm of each side)", ">= 6 mm", "S22 S11 RC", "Derived", "1a: 1 px = 5.9 mm at 10 m")
    add("KIT-11", "kit", "budget", "triangles and file size per kit glb", "<= 6,000 triangles and <= 400,000 bytes", "limit", "S22 S11 RC", "Judgement", "push guard 1 MB")
    add("KIT-12", "kit", "RC parts", "the RC nodes' bounds against target.kinds.RC.parts_mm", "every part within", "+-0.5 mm", "RC", "Judgement", "photographs P6, P7, P11")
    add("KIT-13", "kit", "paint and material names", "material names on the nodes", "paint_<name> per `paints`, glass_house, net_voile, curtain, blind, pendant_shade", "exact", "all", "Derived", "HANDOVER.md step 3")
    # ---- the glass
    add("MAT-01", "glass", "the pane material", "the pane material's inputs in the build and in the cloud stand-in", "specular 1.0 (F0 0.08; Cycles specular IOR level 1.0), roughness 0.03, metallic 0, transmission 0, base colour 0.03 where the net's alpha is 0", "+-0.02 (roughness 0.02 to 0.04)", "all panes", "Read", "1a step 1; unreal-look.json glass_roughness 0.02")
    add("MAT-02", "glass", "no day glow", "the pane's emission by day", "0 (the net is not emissive by day: net_day_gain 0.0)", "exact", "all", "Read", "unreal-look.json net_day_gain")
    add("MAT-03", "glass", "the alpha is wired", "the net material's alpha input", "linked to the weave texture (not a constant)", "exact", "net cards", "Read", "1a: 'the lace's alpha is not wired' was the fault")
    add("MAT-04", "glass", "reflectance at a grazing angle", "render a flat pane at 16 degrees from the wall against a uniform sky of luma 1.0 with the room black", "the pane's luma 0.26 of the sky (+-0.03) with F0 0.08: Unreal's own figure for Specular 1 (1a section 2)", "+-0.03", "the pane material", "Derived", "1a Fresnel table: true two-face 0.38, Unreal 0.26")
    # ---- the white-board fault, by measurement (the gate renders)
    add("WB-01", "gate", "net windows are darker than their frames", "P/L of every net N1 or N2 window seen at 15 to 30 degrees from the wall (day, the gate's five views)", "0.55 to 0.95 and the median of the set at most 0.92", "bands", "GS_A GS_B", "Photo", "P1_a, P1_b, P1_e (31 to 37 degrees) 0.83 to 0.87; nine net windows 0.60 to 0.97")
    add("WB-02", "gate", "bare windows are much darker", "P/L of every bare (N0) window seen at 15 to 30 degrees from the wall, by day", "0.10 to 0.45", "band", "GS_A GS_B", "Photo", "P1_c 0.32, P4_G 0.19, P3_d 0.36")
    add("WB-03", "gate", "bare windows from across, near square", "P/L of every N0 window seen from H_ACROSS_0 by day (over 60 degrees), and the pane's blue minus red", "0.35 to 0.70 and blue over red at least 10 levels", "bands", "GS_A", "Photo", "P8_L, P8_R: 0.62, 0.51; (87, 99, 135)")
    add("WB-04", "gate", "the dark lines are present", "D/L of every window (net or bare) seen at 15 to 30 degrees", "at most 0.55", "limit", "GS_A GS_B", "Photo", "P1 tight outlines 0.47 to 0.50; 1a D/L <= 0.6; the fault was 0.85")
    add("WB-05", "gate", "the pane is not one tone", "the pane spread (95th minus 5th percentile) of every net window; of every bare window", "net at least 40 levels; bare at least 20", "limit", "GS_A GS_B", "Photo", "nets 85 to 173 on the photographs; 1a: at least 20; the fault 14")
    add("WB-06", "gate", "something is behind the glass by day", "for every N0, N3 or N1 window seen from H_ACROSS_0 by day: the clear pane's pixels (upper sash for N1, whole pane for N0)", "at least two tonal regions (the ceiling and the back wall, or the net's edge) whose medians differ by 10 levels or more, from the room picture through `trace`", "10 levels", "GS_A GS_B", "Derived", "brief item 6")
    add("WB-07", "gate", "the frame is brighter than the wall", "L (linear) over the brick's median (linear) beside the window, by day", "3.0 to 9.0", "band", "GS_A GS_B", "Photo", "P1 4.3 and P8 3.7 on photographs (film contrast); the game's albedos give 0.82/0.13 = 6.3; the concept sheet's 7 is outside the photographs")
    add("WB-08", "gate", "the old fault fails", "run WB-01 to WB-05 on a render with the old pane (a lit lace card, F0 0.04, no lines) in the same views", "WB-04 and WB-05 and WB-02 must FAIL (D/L 0.85, spread 14, bare windows lighter than 0.45)", "must fail", "GS_A", "Derived", "1a section 3; a check that cannot fail checks nothing")
    add("WB-09", "gate", "the window under 10 degrees", "a window seen under 10 degrees from the wall (the far end of H_ALONG_15_ROAD)", "reads as a white lining edge at least 1 px wide beside a dark void; the reveal's brick return 0.8 of the wall's luma or less; no pane luma above the lining's", "as stated", "GS_A", "Photo", "P13: a white slit beside a dark void; 1a")
    # ---- night
    add("NIGHT-01", "gate", "lit and dark windows at night", "count of windows with pane median luma >= 100 (lit) and <= 30 (dark) at 20:30 over the 20 street windows (GS_A and GS_B together, rendered from the one camera that sees each squarely)", "7 lit (+-1), the rest dark; none between 30 and 100", "+-1", "all 20", "Judgement", "rooms.lit_share")
    add("NIGHT-02", "gate", "lit against dark", "the median pane luma of the lit windows over that of the dark windows, night", "at least 4 (linear at least 10)", "limit", "GS_A GS_B", "Judgement", "NIGHT-2026-10-08.md: real lit windows are 10 to 100 times the lit paving; the game's gain gives 0.4")
    add("NIGHT-03", "gate", "the lit net glows its own colour", "a lit net or curtain's mean colour (linear) ratio r:g:b", "r > g > b, g/r 0.55 to 0.80, b/r 0.20 to 0.45 (tungsten 2700 K and the fabric)", "band", "lit windows", "Read", "interior_lit (1.0, 0.714, 0.344)")
    add("NIGHT-04", "gate", "a dark window shows only the sodium wash", "the dark rooms' mean colour (linear)", "b/r under 0.05 (the wash is (1.0, 0.25, 0.0)); luma 8 to 30 sRGB", "limit", "dark windows", "Read", "unreal-look.json lantern_linear_rgb")
    add("NIGHT-05", "gate", "the lit order is nested", "the set lit at 23:00 is a subset of the set lit at 20:30 except the always-lit pair's end; empty rooms never lit", "true", "exact", "table", "Derived", "lit_share.rule")
    # ---- rooms and pictures
    add("PIC-01", "rooms", "size and states", "each room's three PNGs", "2048 x 1865 (UP) or 2048 x 1566 (GF), 8-bit sRGB, named <room>_<state>.png, with <room>.json", "exact", "13 rooms x 3 states = 39", "Derived", "shop-windows target 3")
    add("PIC-02", "rooms", "mean luma", "the mean sRGB luma of each picture", "day 105, night_lit 70, night_dark 15 (landings and empty rooms at night_lit: bare bulb: 40)", "+-15 per cent", "all", "Judgement", "picture_standards")
    add("PIC-03", "rooms", "no black void", "the share of pixels under luma 8 and the largest dark region", "day and night_lit: under 25 per cent and the largest region under 15 per cent of the picture; the composite (x brightness) day >= 14, night_lit >= 40", "limits", "all but night_dark", "Derived", "the 3 October failure")
    add("PIC-04", "rooms", "the back wall lands where the rule puts it", "the back wall's corners in the picture by edge detection", "UP: (614, 559) to (1434, 1306); GF: (566, 433) to (1482, 1133)", "+-8 px", "all", "Derived", "trace/project rule, camd = W")
    add("PIC-05", "rooms", "stand-off", "every object's stand-off from its surface (rooms.rooms[].objects)", "back wall <= 0.80 (true <= 0.40), side walls and ceiling <= 0.06 (true <= 0.03), floor <= 0.037 (true <= 0.018)", "limit", "all", "Derived", "hw_common budgets")
    add("PIC-06", "rooms", "parallax", "from H_ACROSS_0 and the same point moved 2.0 m along the street, a marker at the picture's centre", "moves as `trace` predicts", "+-20 px of 2048", "UP and GF samples", "Derived", "shop-windows PRJ-02 (proves the gate, not the game)")
    add("PIC-07", "rooms", "no marks", "every picture searched by eye at full size, and the final base colour of every model used", "no maker's name, brand, logo, barcode, person or child; every `marks` entry blanked or the model not used", "none", "all", "Derived", "TARGET-REVIEW of unit 7, fault 2")
    add("PIC-08", "rooms", "the room is lit as the table says", "the picture used for each window in each state", "lit windows night_lit, the others night_dark, day for all by day", "exact", "20 sites", "Derived", "lit_share")
    # ---- sites and variety
    add("SITE-01", "sites", "the twenty openings", "the derived list of terrace-front.py's windows re-derived live", "20 sites, centres and kinds as sites[]; the cottage windows' kind by house", "+-1 mm", "20 sites", "Read", "terrace-front.py plan_street, _window_kind")
    add("SITE-02", "sites", "no visible repeat", "along each row, any two windows within three places", "never the same (room, net kind, curtain) triple, never the same paint on neighbouring houses unless white", "exact", "sites", "Judgement", "variants")
    add("SITE-03", "sites", "the mix", "the street's twenty windows by net class", "N0 4 to 5, N1 8 to 10, N2 2 to 4, N3 1, curtain or blind 6 to 8 (some windows carry two)", "counts", "20 sites", "Photo", "tally")
    add("SITE-04", "sites", "paint", "houses by paint", "white (any kind) 5 to 7 of 10, cream 2, olive 1, blue 1, bronze 1", "counts", "10 houses", "Photo", "paint_tally")
    # ---- previews and the content rule
    add("CONTENT-01", "content", "the content rule", "every string of target.json, every picture, every preview", "no alcohol, gambling, child; no real firm's name; tobacco allowed", "none", "all", "Derived", "canon.md; CLAUDE.md")
    return C


def photographs_win():
    return [
        {"id": "D1", "what": "the replacement frame's colour", "street_file": "dark anodised bronze (frame_bronze) for every replacement (terrace-front.py _sash)", "photographs": "white in all four replacement windows reached (P6, P7, P11, and P6's ground bay): none brown or bronze", "chosen": "white satin (white_upvc) by default; bronze kept for the one metal-refit house (the ship chandler's, whose front is aluminium: Judgement, D06 'Hook shops receive metal frames'); not Jafar's ruling: the asset plan's"},
        {"id": "D2", "what": "the nets", "street_file": "one square mesh picture over the whole pane (net_curtain_a, _b: 7 to 10 mm squares, mean alpha 0.53), alternated by house", "photographs": "about half the windows have a voile on the lower sash only (47 of 60), the upper sash clear; full nets 22 per cent; bare 18 per cent; curtains 10; blinds 2", "chosen": "six net and drape kinds, per house, with the mix of the photographs; the two held pictures are not used"},
        {"id": "D3", "what": "the pane", "street_file": "the net card is the pane: lit lace over a pale card, F0 0.04 (the 8 October note)", "photographs": "every bare window reads dark (0.19 to 0.36 of its frame) and the room shows; a net reads 0.6 to 0.97 of the frame with lines round it", "chosen": "glass over a dark room, the net a separate card (1a)"},
        {"id": "D4", "what": "the cottages' windows", "street_file": "all six drawn as 2/2 box sashes 1.5 high (the per-house kind is not read on the ground floor)", "photographs": "the ground windows of P1, P3, P4, P12 are the same sashes as the floor above; P6's ground sill stands 0.72 to 0.92 above the step (Photo: door leaf 195 px = 1.98 m)", "chosen": "the house's own kind and the period opening 1676.4 with the head kept (sill 0.7236 above the threshold)"},
        {"id": "D5", "what": "six over six", "street_file": "none", "photographs": "P10 (Copenhagen Street, Georgian, 1983) and P13 (Prince Street, Hull, 1982) show it, on Georgian terraces; no house of Quay Street is Georgian", "chosen": "not built; listed as the sash kind a Georgian house would need"},
        {"id": "D6", "what": "the glazing bar", "book": "22.2 mm (the lab's amended value)", "photographs": "P8 (Oxford, 1987): the bar is 2.3 px wide on a window 71.9 px wide = 27 mm (+-6)", "chosen": "22.2 kept: inside the error"},
        {"id": "D7", "what": "the frame's visible width", "book": "76.2 (3 in, the ruling)", "photographs": "P8, the BACK of a terrace (plain, no outer lining): the visible white jamb is 3.1 to 4.0 px of 71.9 = 37 to 47 mm; the lab's P6 (a front, Tottenham) 79 mm", "chosen": "76.2 kept for the fronts (the ruling); a rear window narrower, not on this street"},
        {"id": "D8", "what": "the lit share", "street_file": "one in three of the upstairs nets lit at night, two cottage windows always", "photographs": "none reached (no night photograph of a terrace before 1996)", "chosen": "kept near the street's one in three (0.35 at 20:30); a Judgement"},
        {"id": "D9", "what": "frame to wall ratio", "research": "WINDOWS-OTHER-DIRECTION: frames about 7 times the wall", "photographs": "P1 4.3, P8 3.7 (linear, display values of film scans)", "chosen": "the check's band is 3 to 9; the game's own albedos give 6.3"},
        {"id": "D10", "what": "the meeting rail", "book": "38.1 mm (the lab kept it)", "photographs": "P8: the rail with its shade reads 5 px of 134 = 62 mm; the lab's note (P6 Tottenham 24 to 28 mm face) stands for the face; the rest is the underside's shade", "chosen": "38.1 kept; the shade is BOX_SHADE.meeting_rail_underside"},
        {"id": "D11", "what": "the top light of the replacement", "street_file": "the transom at 0.72 of the opening (REPLACEMENT_TRANSOM)", "photographs": "P6 0.66, P7 0.72, P11 0.75", "chosen": "0.72 kept (inside the three)"},
        {"id": "D12", "what": "the white-board look at 15 to 30 degrees", "research_1a": "the panes should be darker than the frame by about 0.6 to 0.9", "photographs": "net windows read 0.83 to 0.87 of the frame at 31 to 37 degrees: nets ARE nearly white; bare windows 0.19 to 0.36", "chosen": "the bands above are by state; the fault is the missing lines and the uniform tone, not a bright net"},
    ]


def could_not_settle():
    return [
        "No 1975 to 1995 night photograph of a terraced street was reached: the lit share by hour is a Judgement (anchored on the street's own one in three).",
        "No period photograph of a brown or bronze anodised aluminium window on a house was reached: the bronze replacement is kept for one house only, marked Judgement.",
        "The photograph measurements are on 640 to 1024 px scans: a window is 15 to 100 px wide, so D (the darkest line) is a floor, and the angle from the wall is +-5 degrees from the window's proportion; the bands are wide for that reason.",
        "A sealed double-glazed unit's four reflecting faces (about 0.14 at normal incidence) cannot be reached by Unreal's Specular 1.0 (F0 0.08): the replacement's pane under-reflects; the cure (an emissive sky term) is a PC tuning, listed in owed_on_pc.",
        "How the game's Lumen reflections and the street cube show on the pane (the box projection, the Fresnel hand-over) is not shown by the cloud: the cloud's pane reflects the proxies and the dome through Cycles.",
        "The rooms' contents were chosen from 44 Poly Haven models and 17 textures; none shows a period British room: no 1975 to 1995 photograph of a domestic interior was reached, so the rooms rest on the photographs' windows (nets, drapes, a pot plant, a dark room) and on the budgets, not on a room photograph.",
        "Whether Jafar wants the kit for the whole street at the period height (the cottages' sills lowered by 0.176 m) is his: the ruling of 8 October is followed here for every row; the PC session widens SASH_KIT_ROWS.",
        "Six over six is not on the street and was not built.",
        "The backdrop rows (48 windows) take the same pieces with no pictures: their paint and lit pane are rules, not a table.",
    ]


def owed_on_pc():
    return [
        {"id": "OWED-01", "what": "the pane in the game: Specular 1.0 at roughness 0.03 with the net's alpha wired, the opaque Default Lit material, seen at 15 to 30 degrees with Lumen's own reflections", "check": "WB-01 to WB-05 on the packaged game's frames at the Hook camera and the reverse view (1a's step 1 test)"},
        {"id": "OWED-02", "what": "the joinery's shade as vertex colour (BOX_SHADE) read by M_LedgerSurface (not the AO pin)", "check": "1a section 5: D/L <= 0.6, T/L 0.65 to 0.85, P/L 0.6 to 0.9 and a pane spread of 20 levels in the hook frame's near-left terrace and Mickey's row"},
        {"id": "OWED-03", "what": "a marker at the room picture's centre moves as `trace` predicts from two eyes 2.0 m apart, in the packaged game", "check": "PIC-06 on the PC: 20 px of 2048"},
        {"id": "OWED-04", "what": "the room pictures rebuilt on the PC (`python make_house_rooms.py`: not written here), the masters on F:/LedgerTools/house-rooms, imported as sRGB textures", "check": "PIC-01 to PIC-05, PIC-07 at full size"},
        {"id": "OWED-05", "what": "Jafar's page: the house windows as a sample (the look): one page with the 15 and 30 degree frames, day and night, and the old frame beside", "check": "nothing is multiplied before his yes (CLAUDE.md)"},
    ]
