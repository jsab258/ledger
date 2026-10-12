#!/usr/bin/env python
"""Author tool: write TARGET.md from target.json (every number in the tables comes from the file) and the prose below.

    /home/user/.bpyenv/bin/python make_doc.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sw_common as S  # noqa: E402
import target_drawing as TD  # noqa: E402

T = json.load(open(os.path.join(HERE, "target.json")))
SH = {s["id"]: s for s in T["shops"]}
OUT = []


def w(s=""):
    OUT.append(s)


def esc(x):
    return str(x).replace("|", "/").replace("\n", " ")


def table(head, rows):
    w("| " + " | ".join(head) + " |")
    w("|" + "|".join(["---"] * len(head)) + "|")
    for r in rows:
        w("| " + " | ".join(esc(c) for c in r) + " |")
    w()


def hours_str(h):
    if not h:
        return "none"
    names = {"mon": "Mon", "tue": "Tue", "wed": "Wed", "thu": "Thu", "fri": "Fri", "sat": "Sat", "sun": "Sun"}
    def f(a):
        return ("%d:%02d" % (int(a), round((a % 1) * 60))) if a < 24 else ("%d:%02d (next day)" % (int(a - 24), round((a % 1) * 60)))
    out = []
    for d in ("mon", "tue", "wed", "thu", "fri", "sat", "sun"):
        if d in h:
            out.append("%s %s-%s" % (names[d], f(h[d][0]), f(h[d][1])))
    return "; ".join(out)


def goods_by_fixture(room):
    by = {}
    for g in room["goods"]:
        by.setdefault(g["on"], []).append("%s x%d" % (g["model"], g["n"]))
    fx = {f["id"]: f for f in room["fixtures"]}
    return ["%s (%s, stand-off %.2f): %s" % (k, fx[k]["kind"], fx[k]["depth_m"], ", ".join(v)) for k, v in by.items()]


def display_str(d):
    return ", ".join("%s x%d" % (i["model"], i["n"]) for i in d["items"])


def build():
    w(T["summary_line"])
    w()
    w("# Shop windows of Quay Street: the exact target")
    w()
    w("**Status: fixes applied, not re-reviewed.** The fresh review of 12 October (TARGET-REVIEW.md: 3 faults, 15 narrow points) failed this target; every exact amendment is applied here and in `target.json`, the author scripts, the self-check and the previews. "
      "By Jafar's rule of 11 October (no more polishing of targets) it is not reviewed a second time: the build's gate holds it to the checks in section 10.")
    w()
    w("Cloud week 42, part 2, unit 7 (12 October 2026). Written by the target writer from sources reached that day; nothing is built and nothing is committed. Every number below is in `target.json`; "
      "the checks that follow from it are its `checks` list and its `self_check` (%s; %d of %d negative controls caught)." % (T["self_check"]["result"], json.load(open(os.path.join(HERE, "controls_result.json")))["caught"], json.load(open(os.path.join(HERE, "controls_result.json")))["of"]))
    w()
    w("## 0. Files, and how to read them")
    w()
    table(["file", "what it is"], [
        ["TARGET.md", "this page (made by make_doc.py from target.json)"],
        ["target.json", "the ten shops (front, door, glass, fascia, room, display, lights, pictures, cameras), the method's numbers, the inventory, the spec entries, the checks, the self-check"],
        ["target_drawing.py", "draws target.json alone: each bay's elevation, each room's plan, back wall and picture layout, the ten fronts' sheet, and the elevation laid on the main photograph"],
        ["self_check.py, controls.py", "tests the target against its sources (%d rows; it writes nothing unless --write) and shows the self-check can fail (%d mutations of target.json, every one caught)" % (len(T["self_check"]["rows"]), json.load(open(os.path.join(HERE, "controls_result.json")))["of"])],
        ["sw_common.py, sw_shops.py, make_target.py, extras.py, make_doc.py, make_previews.py", "author tools: the game's rule and the stand-off budgets; the rooms and displays as data; the builders of target.json, TARGET.md and the previews"],
        ["polyhaven_checked.json, sketchfab_checked.json, ambientcg_checked.json", "what the three libraries' APIs answered on 12 October"],
        ["production/previews/cloud-week/refs/shop-windows/", "P1 to P6 (the photographs, cropped to the craft), the overlay, D1 to D4 (drawings)"],
    ])
    w("Run with `/home/user/.bpyenv/bin/python`: `make_target.py [--refresh]`, `self_check.py [--live]`, `controls.py`, `target_drawing.py OUT_DIR`, `make_previews.py`, `make_doc.py`.")
    w()
    w("**Units and frames.** Metres for rooms and the street; millimetres for the front, in the 2.2 bay frame (u across the bay from the viewer's LEFT, d out from the wall face toward the street, z up from the footway). "
      "Street z is above the road crown (crown + 0.10 = footway). **Kinds of number:** Read (printed in a file), Scaled, Photo (measured on a photograph: method and error given), Derived, Judgement.")
    w()

    # ---- 1
    w("## 1. The ten units as found: twelve not found")
    w()
    w("The street has **ten shop units as built; twelve not found.** east_parade bays 0 to 5 (x 3 to 39, 6 m each), east_chandler bay 0 (x 40 to 46), west_north bays 0 to 2 counted from the high-x end (x 36 to 42, 30 to 36, 24 to 30). "
      "canon.md and TOWN.md name no shop count; DECISIONS 3 Oct lists ten; 'twelve' is the superseded atlas proposal (terrace-fronts.md 290 to 322) and 'the other eleven' in RULINGS 2 Oct. "
      "One conflict is NOT resolved: " + T["street"]["hal_conflict"])
    w()
    rows = []
    for s in T["shops"]:
        rows.append([s["id"], s["street_number"], s["trade"], s["owner"] or "none named", "%s bay %d (%s)" % (s["block"], s["bay"], s["side"]), "%.0f to %.0f" % tuple(s["street_x_m"]),
                     "yes (4096 x 1855)" if s.get("room") else ("no: whitewashed, no card" if s["id"] == "empty_unit" else "no: its room is real and walked already"),
                     ("lit after Tom's key" if s["id"] == "mickeys" else ("lit" if s["lit_at_night"] else "dark")), s["spec_id"] or "-"])
    table(["id", "no.", "trade", "owner", "block, bay, side", "street x", "room picture", "at night", "spec id"], rows)
    w("**Hours and lit windows.** Hours are hook-cast.json's `areas` where they exist (Mickey's 7 to 3 am, Sundays from 9; Rita's 9 to 17:30, Wednesday to 13:00; fish market 7:30 to 14:00; laundry 8 to 17:30; cafe 6:30 to 22:00, Sundays 8 to 12; newsagent 6 to 17:30, Sundays 7 to 12). "
      "Not found: the grocer, ironmonger and chandler; settled as a Judgement from the Shops Act (Mon to Sat, 8 to 17:30 or 17:00, early closing Wednesday 13:00), marked in each shop's `hours_source`. "
      "Lit at night is vignette-pieces.json's `lit_names` (Mickey's after Tom's key, Rita's, the grocer, the newsagent, the tea room, the chandler); the street file lights three shops that the hours say are shut by then (the newsagent at 17:30, the grocer and the chandler by the Judgement; D8): kept as the street file has it, noted for the town.")
    w()
    w("**What unit 7 does for Mickey's:** only its front. The room is the real walked room (spec entry untouched, `room_3d`, its lamps and brightness): the front is the A2 painted-steel refit assembled from the 3.2 parts (clad pilasters, M1 window 3L-3T with 2 mullions, patterned-tile stallriser), the 4.1 board with its raised gilt letters (geometry), the glass rows `0632 960418` and `MINICABS . 24 HOURS`.")
    w()

    # ---- 2
    w("## 2. Sources")
    w()
    w("Only sources reached on 12 October are used. Photographs are for measuring and for the reviewers only: never placed in the game, never traced into a texture, never fed to an image model; each preview is cropped to the craft, with every person, real firm's name, number and drink merchant's sign cropped away or masked grey (exactly what is masked in each preview is in section 12; the masks are drawn on every rebuild and read back from the JPEG). No NoAI source.")
    w()
    table(["id", "what", "URL", "read", "author", "licence", "taken", "shows", "used"], [[s["id"], s["what"], s["url"], s["read"], s["author"], s["licence"], s["taken"], s["shows"] + " " + (("[" + s["dated_object"] + "]") if s["dated_object"] not in ("n/a", "-") else ""), s["used"]] for s in T["sources"]])
    w("**Not reached (nothing rests on them):**")
    w()
    for u in T["unreached"]:
        w("- " + u)
    w()

    # ---- 3
    m = T["method"]
    w("## 3. The method, in the game's own numbers")
    w()
    w("**The game's rule** (production/specs/shop-interiors.json, tools/ue/make_interior_material.py `trace`, kept exactly): " + m["game_rule"]["camera_rule"] + ". The card is %.1f x %.1f m at street z %.2f to %.2f, %.3f behind the street's midline on its side (y %+.3f), "
      "0.61 m behind the glass (glass y %.3f to %.3f). The picture's left is the viewer's left (an east card: the card's HIGH x; a west card: its LOW x)." % (S.W, S.H, S.CARD_BOTTOM, S.CARD_TOP, S.CARD_Y, S.CARD_Y, S.GLASS_Y_FRONT, S.GLASS_Y_BACK))
    w()
    w("**Where the floor line and the back wall land.** The box is W x H x D = 5.3 x 2.4 x D with its floor at the card's bottom edge (0.65 above the crown) and its ceiling at the card's top (3.05): the picture's floor is the window bed carried back, 0.55 above the shop's real floor, "
      "which the stallriser hides from the street. For D = 4.5 the back wall is the rectangle u 0.2296 to 0.7704, v 0.2296 to 0.7704 of the picture, in the 4096 x 1855 picture from (940, 426) to (3156, 1429) (check PIC-04, +-8 px). "
      "The side walls and floor are the wedges outside it; nothing else is in the picture.")
    w()
    w("**What a projected room can honestly hold (the answer to the third failure).** An object painted on a surface that stands off it by s metres is drawn where the render camera saw it and slides, as the eye moves, by the angle between the eye's rays to the object and to its painted place. "
      "`sw_common.standoff_table` computes, from `trace`'s geometry, the greatest stand-off whose slide stays within N pixels of a 2560 x 1440 frame at STREET_SQUARE, STREET_30 and CLOSE_35 (and their mirror images). Results (D = 4.5):")
    w()
    b20, b40 = m["standoff_budget"]["reads_true_20px"], m["standoff_budget"]["tolerated_40px"]
    table(["surface", "reads true (20 px)", "tolerated (40 px)", "the target's rule"], [
        ["back wall", "%.2f m" % b20["back_wall"], "%.2f m" % b40["back_wall"], "shelf units and goods on them: 0.30 (true); a counter, machine or floor piece against the wall: up to 0.60 (tolerated)"],
        ["side walls", "%.2f m" % b20["side_walls"], "%.2f m" % b40["side_walls"], "boards, posters, pegboards, hung things: 0.05 flat; racks and boards with hung tools: up to 0.10"],
        ["floor and ceiling", "%.3f m" % b20["floor_and_ceiling"], "%.3f m" % b40["floor_and_ceiling"], "flat things only: 0.025 (a mat, a drain, a tile pattern); a ceiling batten fitting 0.045 is tolerated (0.05)"],
    ])
    w("Anything that would need to stand further off a surface (a counter across the room, a table, a chair, a free-standing unit, a buoy at the side) is NOT drawn in the picture: it stands in the display, which is real geometry, or it is dropped. "
      "The slide of the standard objects at the three cameras (px of 2560 x 1440):")
    w()
    sl = m["honest_range"]["slide_px_at_2560x1440"]["table"]
    names = list(sl["CLOSE_35"].keys())
    table(["object"] + ["STREET_SQUARE", "STREET_30", "CLOSE_35"], [[n] + ["%.0f" % sl[c][n] for c in ("STREET_SQUARE", "STREET_30", "CLOSE_35")] for n in names])
    w("**From how near the projected room holds, and why the CLOSE view stands at 1.5 m.** " + m["honest_range"]["why"])
    w()
    w("Resolution, at the game's 1440 lines, 35 degrees off (screen pixels a texel; above 2 is soft): " + "; ".join("%s: median %.2f, p95 %.2f, %.0f%% soft" % (k.replace(" from the glass, 35 deg", ""), v["median"], v["p95"], 100 * v["soft_fraction_over_2"]) for k, v in m["honest_range"]["resolution"]["table"].items()) + ". " + m["honest_range"]["resolution"]["reading"] + ".")
    w()
    w("The window's far end is seen at (degrees off the glass normal, from 35 degrees off the window centre): " + ", ".join("%s: %.0f" % (k, v) for k, v in m["honest_range"]["window_far_end_angle_deg"]["table"].items()) + ". " + m["honest_range"]["window_far_end_angle_deg"]["reading"] + ".")
    w()
    w("**The pictures.** " + str(T["pictures"]["pixels_wide"]) + " x " + str(T["pictures"]["pixels_high"]) + " px, 8-bit sRGB PNG, three states (day, night_lit, night_dark), named `<spec_id>_<state>.png` with `<spec_id>.json` beside them holding `shop, w, h, d, camera_d, pixels, states, made_by, samples` "
      "(the pawnbroker's own file's fields); Cycles, 128 samples, denoised; masters on F:/LedgerTools/shop-rooms, 2048-wide copies in production/art/shop-rooms as for the pawnbroker. The game's brightness values are kept for every shop: **day 0.15, night 0.7**. "
      "The mean luma of each approved pawnbroker picture (measured 12 October) is the standard: **day 119.5, night_lit 79.8, night_dark 17.7**; a new picture's mean is within 15 per cent of the state's, and the checks' floors (PIC-02, PIC-03) are 0.7 of them. "
      "Composite floors (the picture times the brightness, tone-mapped Standard, glass reflection off): day >= 33, night_lit >= 45, night_dark 10 to 35 (of 255).")
    w()
    w("**Lights per state, for every room** (each shop's own tubes are in its `room.lights`): day = an overcast area light the size of the card on its plane (6500 K, strength set so the picture's mean matches the standard) plus the battens on (the shop is open); night_lit = the battens only, cool white 4000 K, 5 ft T12, 38 mm (about 12 kcd/m2 on the tube: DRESSING note), "
      "no sky; night_dark = a faint sodium wash through the front (linear (1.0, 0.25, 0.0): the game's `lantern_linear_rgb` in production/specs/unreal-look.json; the scene file's (1, 0.7055, 0) is stale, QUEUE.md 9 Oct 12:10; 6 per cent of night_lit's energy) and one small practical so the room is not black. Windows are not lit by a second picture's worth of tungsten: the pawnbroker's display spots (2700 K) are the display's, not the picture's.")
    w()
    w("**The review cameras** (street frame, metres; eye 1.70 above the crown = 1.60 above the footway; 2560 x 1440). STREET_SQUARE: on the far pavement's kerb edge (the brief's 'about 8 m' is 8.76 m to the glass, the nearest the far pavement allows), square to the window's centre, vertical field 39 degrees. "
      "STREET_30: the same distance, 30 degrees off the normal toward the quay end (low street x), 39 degrees. CLOSE_35: on the shop's own pavement 1.5 m from the glass, 35 degrees off the normal toward the quay end, aimed at the display's middle (z 1.45), vertical field 60 degrees (the vignette camera's). "
      "CLOSE_35_B: CLOSE_35 moved 2.0 m along the street, for the parallax test. By day and by night (night_lit for the lit shops, night_dark for the dark). Every shop's eye and aim are in `shops[].cameras`.")
    w()
    w("**The gate in the cloud, which has no Unreal.** " + T["gate_in_the_cloud"]["how"] + " What it cannot show: " + T["gate_in_the_cloud"]["what_it_cannot_show"] + ".")
    w()

    # ---- 4 Rita
    r = SH["ritas"]
    f = r["front"]
    w("## 4. Rita's shop in full (the pawnbroker; east_parade bay 2, x 15 to 21; the model, RULINGS 2 Oct)")
    w()
    w("**What it keeps and what it changes.** Keeps: " + r["keeps"] + ". Changes: " + r["changes"] + ".")
    w()
    w("### 4.1 The front, from the 3.2 parts")
    w()
    w("Rita's front is the 3.2 kit's own (every part built, `shopfront_ritas.glb`, 34,780 triangles, out of git; `python build_shopfront.py` rebuilds it) except the doors, the lobby, the side door's trim and the band above the doors (4.1a), which are this target's and the door family's. "
      "Door end: the viewer's LEFT (street high x). Zones across the bay (u, mm): side door 350 to 1294, shop door 1294 to 2300, window 2300 to 5650 (3350 long). Assembly order, bottom to top, then left to right:")
    w()
    for i, p in enumerate(f["assembly_order"], 1):
        w("%d. %s" % (i, p))
    w()
    table(["part", "built by 3.2?", "size and place (mm, 2.2 frame)", "paint (sRGB)"], [
        ["pilaster, panel (two, the right one mirrored)", "yes", "slot 350; plinth z 0 to 600, 180 proud; shaft 290 x 140 proud, z 600 to 2540; capital 310 high to z 2850, top 350 x 175; base ogee 60 high", "oxblood 93,46,49"],
        ["console, scroll (two)", "yes", "240 x 205 x 550 (z 2850 to 3400), at u 175 and 5825; the third review's leaf and rolls as built (3.2 D1 to D3)", "oxblood"],
        ["fascia board", "yes", "5410 x 550 x 120 proud, u 295 to 5705, z 2850 to 3400; cyma bed mould 40 (3.2 D5); carries the 4.1 board", "oxblood (board texture: 4.1 ritas)"],
        ["cornice", "yes", "5892 x 150 x 215 deep, z 3400 to 3550, broken forward 85 over each console, mitred returns (3.2 D4); 150 mm as built is Jafar's ruling of 12 Oct", "oxblood"],
        ["sill", "yes", "75 thick, nose 150, z 525 to 600, u 2300 to 5647 (3 short of the plinth)", "white joinery 226,224,214"],
        ["stallriser, panel", "yes (three panels)", "z 0 to 600, 125 proud, three raised and fielded panels (1002, 1026, 1002) between 80 stiles", "oxblood"],
        ["window frame T1", "yes", "jambs 50 x 95; seat 25 (z 600 to 625); 3 lights 625 to 2400; transom 2400 to 2480; **nine toplights of 326.9 as built** (3.2 D6: each mullion carried up as a 70 wide bar, two 28 wide bars a light at 390.9, 745.8, 1497.6, 1852.5, 2604.2, 2959.1; the 2.2 table said eight, unaligned) 2480 to 2790; head 2790 to 2850; mullions 70 wide, front d 92, centres 1121.7 and 2228.3 from the frame's left; glass 6 mm at d 30 to 36, ovolo bead 16 x 12", "white joinery"],
        ["shop door T1", "NO: specified here (4.2)", "slot 1006, leaf 900 x 2040 at z 28, frame jambs 50 x 100 running up to the head; fanlight z 2131 to 2400 between the jambs (u 1344 to 2250), three toplights over it (4.1a)", "white joinery"],
        ["transom over both door slots", "NO: specified here (4.1a)", "transom_t1, u 350 to 2300, z 2400 to 2480, meeting the window frame's left jamb", "white joinery"],
        ["panel over the side door", "NO: specified here (4.1a)", "one raised-and-fielded panel, field 844 wide (944 - 2 x 50), z 2480 to 2790, raised_field_edge", "white joinery 226,224,214"],
        ["head across the door slots", "NO: specified here (4.1a)", "head_section 95 x 60, u 350 to 2300, z 2790 to 2850", "white joinery"],
        ["side door F1 (3.1)", "door_F1.glb, yes", "slot 944, mirrored (door end left): hinge on the shop-door side, knob on the pier side; head trimmed at z 2400; 24.4 filler strip each side", "buttermilk 222,212,184"],
        ["night grille (4.3)", "NO: specified here", "see 4.3", "black powder-coat 37,35,34"],
    ])
    w("### 4.1a The band above the doors (transom line 2400 to the fascia 2850) and the toplights: the fault the review found")
    w()
    w("The 3.2 kit built the window only and left the door slots empty on purpose; this target takes the doors on, so it also puts in what stands above them. The numbers are 2.2's (`targets/shopfronts/target.json` `parts.shop_door.dims` and `parts.side_door_slot.dims.above`, at commit %s), resolved per shop from `front.zones_u_mm` and written into each shop's `door` (keys `fanlight`, `transom`, `toplights_over_shop_door`, `panel_over_side_door`, `head`). Rita's, in millimetres in the 2.2 bay frame (u from the viewer's left, z above the footway):" % r["front"]["build_from"]["commit"])
    w()
    rd = r["door"]
    tb = rd["toplights_over_shop_door"]
    table(["part", "u (mm)", "z (mm)", "what it is"], [
        ["fanlight", "%g to %g" % tuple(rd["fanlight"]["u_mm"]), "%g to %g" % tuple(rd["fanlight"]["z_mm"]), "one 6 mm pane in a timber ovolo bead, between the shop door frame's jambs (50 face each side of the 1006 slot). The street number %s goes on it (4.1; see the note below)" % rd["fanlight"]["street_number"]["text"]],
        ["transom (door slots)", "%g to %g" % tuple(rd["transom"]["u_mm"]), "%g to %g" % tuple(rd["transom"]["z_mm"]), "`transom_t1`, across both door slots, meeting the window frame's left jamb; the window's own transom continues it"],
        ["toplights over the shop door", "%g to %g" % tuple(tb["u_mm"]), "%g to %g" % tuple(tb["z_mm"]), "three panes of %.1f between two 28 wide `toplight_bar_plan` bars at u %.1f and %.1f; glass and beads as the window's toplights; the door frame's jambs run up beside them" % (tb["pane_width_mm"], tb["bars"][0]["centre"], tb["bars"][1]["centre"])],
        ["panel over the side door", "%g to %g" % tuple(rd["panel_over_side_door"]["u_mm"]), "%g to %g" % tuple(rd["panel_over_side_door"]["z_mm"]), "one raised-and-fielded panel, field %g wide (944 - 2 x 50), `raised_field_edge`, painted white joinery (226, 224, 214) as on the approved front (2.2 gives it 2480 to 2850; here the head takes 2790 to 2850, as the approved front shows)" % rd["panel_over_side_door"]["field_width_mm"]],
        ["head (door slots)", "%g to %g" % tuple(rd["head"]["u_mm"]), "%g to %g" % tuple(rd["head"]["z_mm"]), "the window's `head_section` (95 x 60) carried across the door slots under the fascia"],
    ])
    w("**On the other nine fronts** the same, mirrored where the door end is the viewer's right (the band runs from the window frame's right jamb to the pilaster); the metal fronts (M1: Mickey's, the fish market, the laundry and the chandler; M2: the grocer) take their own variant's transom section (`transom_m1`, a 50 high box carrying a 30 mm cover plate to keep 2.2's 80 high band: Judgement) and 2.2's numbers for their doors' tops; the grocer has no side door and so no panel; the newsagent's roller-shutter hood (u 350 to 4706, z 2550 to 2850) cuts the toplights, bars and head away behind it and leaves 70 of the toplights showing. "
      "**FRN-07 (no opening in the front):** on the elevation drawn from `target.json` (D1 and D2), every point between the pilasters' inner edges (u 350 to 5650) from z 0 to 2850 lies on a part; the largest uncovered rectangle is at most 5 x 5 mm. Computed here, per shop (width x height, mm):")
    w()
    rows41 = []
    for s_ in T["shops"]:
        pl_ = TD.front_polys(s_)
        ar_, ww_, hh_, at_ = S.largest_uncovered(TD.covering_rects(pl_), 350.0, 5650.0, 0.0, 2850.0)
        gl_ = s_["front"]["glazing_layout"]
        d_ = s_["door"]
        rows41.append([s_["id"], s_["front"]["glazing"]["pattern"], "%d of %.1f" % (gl_["toplights"], gl_["toplight_width"]), ", ".join("%.1f" % c for c in gl_["toplight_bar_centres"]) or "none (the mullions carry up)", ", ".join("%.1f" % c for c in gl_["mullion_centres"]) + (" (%g wide)" % gl_["mullion_face"]),
                       "3 of %.1f" % d_["toplights_over_shop_door"]["pane_width_mm"], "%.1f x %.1f" % (ww_, hh_)])
    table(["shop", "glazing pattern", "window toplights", "28 wide toplight bars (u from the frame's left)", "mullions carried up as bars (centres)", "over the shop door", "largest open rectangle"], rows41)
    w("**The toplight rule (3.2 street review fault 1, kit departure D6), now on every front:** each mullion is carried up through the toplight row as a bar of its own width, and each light's toplight is split equally by 28 wide bars. 2.2's table (a fixed pitch of bars, slivers of 91 to 95 mm beside the mullions on five fronts, the grocer's 256 mm panes beside both mullions, the launderette's one long pane) is replaced; the launderette's divided upper lights are P5's (disagreement D11); the grocer's sunrise is etched one to a light across its two toplights (Judgement). "
      "FRN-04 checks the bar centres (+-2 mm), a bar on every mullion line, equal widths in a light and no toplight under 250, not only the count. (The kit's D6 and the review list the second light's second bar of Rita's at 1852.5; the rule gives 1852.43, a rounding of 0.07 mm, far inside the check's 2 mm.)")
    w()
    w("**The street number on the fanlight.** " + rd["fanlight"]["street_number"]["where"] + ". " + rd["fanlight"]["street_number"]["frame_of_z"] + ".")
    w()
    w("### 4.2 The shop door, the side door and the bell (the 3.2 kit has none)")
    w()
    d = r["door"]
    w("The door is **specified from 2.2's JSON (`targets/shopfronts/target.json` at commit dd706f6: `parts.shop_door`, its `variants` T1, M1, M2 and its `profiles`; not built by 3.2)** and changed where a photograph of an untouched timber shop front disagrees (D1: Geograph 2192169, a Worcester fish shop's front, May 2000, scaled on the leaf's height). "
      "T1 for Rita's, in millimetres above the footway (the leaf's foot stands at 28 on a terrazzo threshold 25 high):")
    w()
    rl = d["t1_rails_mm"]
    table(["member", "z (mm)", "kind and source"], [
        ["bottom rail", "%d to %d" % tuple(rl["bottom_rail"]), "Photo (195 high in the photograph); 2.2 had 230"],
        ["lower panel, raised and fielded", "%d to %d" % tuple(rl["lower_panel_field"]), "Photo; the 12 mm sticking and the 8 mm bevel as 2.2's raised_field_edge"],
        ["lock rail, carrying the plates", "%d to %d" % tuple(rl["lock_rail"]), "Photo: 322 high; **2.2 had the glass starting at 600 (D1 supersedes it)**"],
        ["letter plate 250 x 40, brass", "centre %d" % d["letter_plate"]["z_mm"], "Photo: 0.32 of the leaf; 2.2 had 545; in the lock rail, centred across the leaf"],
        ["lever handle on a 240 x 40 backplate", "1000 (rim latch and escutcheon at 950)", "Read (the kit); the photograph's handle sits at 0.42 of the leaf (about 890) and is not adopted because the approved game door's lever (rita-day-kit-2026-10-06.jpg, the door Jafar has seen) stands at about 1050 (D12)"],
        ["glass, two panes", "%d to %d" % tuple(rl["glass"]), "Photo: 6 mm in an ovolo bead 14 x 11; the glass 99.5 px wide = 600 of a leaf 853 wide in the photograph; here the leaf is 900 with stiles 115"],
        ["glazing bar", "centre %d, 28 wide" % rl["glazing_bar"]["z"], "Photo: one bar, two panes of about 540"],
        ["top rail", "%d to %d" % tuple(rl["top_rail"]), "Photo: 95 high; 2.2 had 115"],
        ["kick plate / foot strip", "brass 770 x 170 with 8 screws on the lower panel's bottom, a 30 high strip across the foot", "Read (the kit); Photo (2.2's P1)"],
        ["hinges", "three 100 x 75 butts at 150 / middle / 150 on the window side", "Read; the lever is on the viewer's left, the hinge on the right (2.2's game-frame reading of Rita's front)"],
        ["threshold", "terrazzo 25 high falling to 12, nose to d 130", "Read (2.2)"],
        ["the bell", "inside the leaf's top rail at z 1950 to 2050", d["bell"]["kind"] + " (" + d["bell"]["kind_of_number"] + ")"],
        ["the OPEN / CLOSED sign", "inside the glass at z 1500", d["sign"]],
    ])
    w("The side door is the door family's **F1** (3.1: production/assets/cloud-week/door/door_F1.glb), used as 2.2's `parts.side_door_slot` (and its `mapping_from_F1`) places it: slot 944, F1 mirrored where the door end is the viewer's left, its frame's outside face at d 100, trimmed at the shop transom, painted buttermilk (222, 212, 184), "
      "letter plate 250 x 40, the bell push the 3.1 fix leaves as a plain oblong. Metal doors (M1 aluminium: full-height glass in a 50 frame, 100 top rail, 170 bottom rail, a 300 chrome D pull and a floor spring; M2 bronze: a bronze kick panel to 600, glass above) are as 2.2 for the shops that have them, with one change: an M1 door's letter plate is centred in the 170 bottom rail at z 113, outside the glass (2.2's 545 stood inside it); the M2 door's plate stays in the kick panel at 545.")
    w()
    w("### 4.3 The glass, the fascia, the paint and the grille")
    w()
    w("- **Glass:** one 6 mm plate per light (three lights, nine toplights), no astragal bars (D2: the photographs split; Rita's approved window is single sheets); a pane's reflectance is the game's (M_LedgerGlass, night 0.2 of day), not set here. Nothing lies across the glass but the 4.1 rows (WATCHES, JEWELLERY, LOANS, the number 5), the OPEN sign and the hours plate (GLS-01).")
    w("- **Fascia:** the 4.1 board `fascias/ritas/ritas_basecolour.png`, `_height.png`, `_orm.png`, `_wear.png` (5410 x 550 at 1 px/mm), the name RITA'S and PAWNBROKER, the street number 5; the hanging sign is the three balls on a bracket at street x 20.825 (4.1 `ritas_three_balls`). Rebuilt by `make_fascias.py OUTDIR --seed-base 1`.")
    w("- **Paint:** oxblood (93, 46, 49) on piers, consoles, board, cornice and stallriser (rough 0.45); gloss white, yellowed (226, 224, 214) on the window, sill and shop door (0.50); buttermilk on the side door; aged brass (160, 120, 55) fittings.")
    w("- **The grille at night:** " + SH["ritas"]["display"]["night"] + ".")
    w()
    w("### 4.4 The room")
    w()
    room = r["room"]
    table(["", ""], [["box", "W 5.3, H 2.4, D %.1f m; camera_d 5.3; the card at street z 0.65 to 3.05, y +5.875, x 15.35 to 20.65" % room["d"]], ["floor", room["floor"]["material"]], ["walls", room["walls"]["above"] + "; dado " + room["walls"]["dado"]], ["ceiling", room["ceiling"]],
                      ["lights", "; ".join("%s: %s" % (k, room["lights"][k]) for k in ("day", "night_lit", "night_dark"))]])
    table(["fixture", "surface", "stand-off", "extent (x, y, z)", "what"], [[x["id"], x["surface"], "%.3f" % x["depth_m"], "%s %s %s" % (x.get("x") or "", x.get("y") or "", x["z"]), x["what"]] for x in room["fixtures"]])
    table(["goods (model or scripted form)", "n", "on", "why or note"], [[g["model"], g["n"], g["on"], g.get("why") or g.get("note") or ""] for g in room["goods"]])
    w("### 4.5 The near metre: the display")
    w()
    dsp = r["display"]
    w("**Keeps:** " + dsp["keeps"] + ". **Changes:** " + dsp["changes"] + ". Display frame: u from the window zone's viewer-left edge (0 to 3.35 m), v out from the back of the glass (0 to 0.55), w above the bed (the stallriser's top, 0.70 above the crown), at most %.2f high." % dsp["height_max_w"])
    w()
    table(["model", "n", "zone u0-u1, v0-v1, w0-w1 (m)", "note"], [[i["model"], i["n"], "%.2f-%.2f, %.2f-%.2f, %.2f-%.2f" % tuple(i["zone"]), i.get("note") or i.get("why") or ""] for i in dsp["items"]])
    w("### 4.6 The pictures, the spec entry and the cameras")
    w()
    w("Files `pawnbroker_day.png`, `pawnbroker_night_lit.png`, `pawnbroker_night_dark.png` (4096 x 1855) and `pawnbroker.json` (w 5.3, h 2.4, d 4.5, camera_d 5.3, pixels [4096, 1855]). The spec entry is unchanged except `pixels_wide` 2048 to 4096, the display's `x0`/`x1` (15.45 to 18.8 measured on the street model's glass; 15.35 to 18.7 with the 3.2 front's window zone: "
      "a 0.10 m shift the builder takes from whichever front stands) and its `decal`, which goes from `production/art/interiors-2026-09-23/int23_pawn` to `production/art/shop-rooms/pawnbroker_day`. Lit at night (RULINGS 1 Oct): night_lit is the picture the game shows all night; `spill_lumens` 350 and the display's rect light stay as approved.")
    w()
    table(["camera", "eye (street m)", "aim (street m)"], [[c, v["eye_street_m"], v["aim_street_m"]] for c, v in r["cameras"].items()])
    w("Parallax test (PRJ-02): between CLOSE_35 and CLOSE_35_B the card's centre moves **%.0f px** (of 4096) by the rule." % r["parallax_test"]["expected_du_px"])
    w()

    # ---- 5 the other nine
    w("## 5. The other nine, one table each")
    w()
    w("Each table is the shop's row set from `target.json`: front (variants against what 3.2 built), door, paint, fascia, room box and finishes, contents (grouped by the fixture they stand on), display, lights, and what it keeps and changes. Fixture ids name the stand-off class (`true` up to the 20 px budget, `tolerated` to the 40 px budget).")
    w()
    for sid in ("mickeys", "fish_market", "empty_unit", "steam_laundry", "grocer", "chandler", "tea_rooms", "ironmonger", "newsagent"):
        s = SH[sid]
        fr = s["front"]
        w("### 5.%d %s: %s (%s bay %d, x %.0f to %.0f)" % (["mickeys", "fish_market", "empty_unit", "steam_laundry", "grocer", "chandler", "tea_rooms", "ironmonger", "newsagent"].index(sid) + 1, sid, s["trade"], s["block"], s["bay"], s["street_x_m"][0], s["street_x_m"][1]))
        w()
        rows = []
        rows.append(["keeps / changes", "Keeps: %s. Changes: %s." % (s["keeps"], s["changes"])])
        rows.append(["front", "Alterations: %s. Variants: pilaster %s, console %s, cornice %s, stallriser %s, window %s %s (%.0f mm long), shop door %s, side door %s. Door end the viewer's %s. Missing from 3.2: %s. Lobby: %s." % (
            ", ".join(fr["alterations"]), fr["variants"]["pilaster"], fr["variants"]["console"], fr["variants"]["cornice"], fr["variants"]["stallriser"], fr["variants"]["window_frame"], fr["glazing"]["pattern"], fr["window_length_mm"], fr["variants"]["shop_door"],
            fr["variants"]["side_door"] or "none (the flat is reached from the rear yard)", {"L": "left", "R": "right"}[fr["door_end_viewer"]], ", ".join(fr["missing_from_3_2"]) or "nothing", fr["lobby"]["kind"] + (" %s deep" % fr["lobby"].get("depth", "") if fr["lobby"].get("depth") else ""))])
        rows.append(["built from", "`front.build_from`: %s at commit %s (a script builds the front from this target.json and that one versioned input): %s" % (fr["build_from"]["file"], fr["build_from"]["commit"], "; ".join(fr["build_from"]["keys"]))])
        lay_ = fr["glazing_layout"]
        dd_ = s["door"]
        rows.append(["toplights (D6)", "%s: %d toplights of %.1f in %d lights; %s bars between a light's toplights at %s; each mullion carried up as a bar (centres %s, %g wide); 2.2 had pattern %s (%d toplights, aligned: %s)" % (
            fr["glazing"]["pattern"], lay_["toplights"], lay_["toplight_width"], len(lay_["lights"]), "%g wide" % lay_["toplight_bar_face"], ", ".join("%.1f" % c for c in lay_["toplight_bar_centres"]) or "no", ", ".join("%.1f" % c for c in lay_["mullion_centres"]), lay_["mullion_face"],
            fr["glazing"]["from_2_2"]["pattern"], fr["glazing"]["from_2_2"]["toplights"], fr["glazing"]["from_2_2"]["toplight_aligned"])])
        rows.append(["band above the doors (FRN-07)", "fanlight u %s z %s; transom u %s z %s; three toplights of %.1f over the shop door (bars at %s) z %s%s; panel over the side door: %s; head u %s z %s%s" % (
            dd_["fanlight"]["u_mm"], dd_["fanlight"]["z_mm"], dd_["transom"]["u_mm"], dd_["transom"]["z_mm"], dd_["toplights_over_shop_door"]["pane_width_mm"], ", ".join("%.1f" % b_["centre"] for b_ in dd_["toplights_over_shop_door"]["bars"]), dd_["toplights_over_shop_door"]["z_mm"],
            (" (visible %s only: the roller-shutter hood stands over u %s, z %s)" % (dd_["toplights_over_shop_door"]["z_visible_mm"], dd_["shutter_hood"]["u_mm"], dd_["shutter_hood"]["z_mm"])) if dd_.get("shutter_hood") else "",
            ("one raised-and-fielded panel, field %g wide, u %s z %s" % (dd_["panel_over_side_door"]["field_width_mm"], dd_["panel_over_side_door"]["u_mm"], dd_["panel_over_side_door"]["z_mm"])) if dd_.get("panel_over_side_door") else "none (no side door)",
            dd_["head"]["u_mm"], dd_["head"]["z_mm"], ("; the head over the shop door is cut away behind the hood (u %s)" % dd_["head"]["cut_away_behind_hood_mm"]) if dd_["head"].get("cut_away_behind_hood_mm") else "")])
        rows.append(["zones across the bay (u, mm)", "side door %s; shop door %s; window %s" % (fr["zones_u_mm"]["side_door"], fr["zones_u_mm"]["shop_door"], fr["zones_u_mm"]["window"])])
        rows.append(["door", "%s leaf 900 x 2040; glass foot %d; letter plate z %d (%s); hinge on the viewer's %s, lever on the %s; paint %s; the bell and the OPEN / CLOSED sign as 4.2%s" % (
            s["door"]["variant"], s["door"]["glass_foot_z_mm"], s["door"]["letter_plate"]["z_mm"], s["door"]["letter_plate"]["note"], {"L": "left", "R": "right"}[s["door"]["hinge_viewer"]], {"L": "left", "R": "right"}[s["door"]["lever_viewer"]], s["door"]["paint"],
            ("; T1 rails as Rita's" if s["door"]["variant"] == "T1" else ""))])
        rows.append(["paint (sRGB)", "; ".join("%s %s" % (k, v) for k, v in (fr["paint_srgb"] or {}).items())])
        rows.append(["glass", "%d lights + %d toplights, 6 mm plate; lettering rows: %s; blinds, grilles, shutters: %s" % (s["glass"]["lights"], s["glass"]["toplights"], s["glass"]["lettering"] or "none", s["blinds_grilles_shutters"])])
        rows.append(["fascia (4.1)", "%s; name blocks %s; hanging sign %s" % (s["fascia"]["board"], s["fascia"]["name_blocks"], (s["fascia"]["hanging_sign"] or {}).get("id") or "none")])
        rows.append(["night furniture", s["night_furniture"] or "none"])
        rows.append(["hours, lit", "%s (%s); at night: %s (%s)" % (hours_str(s["hours"]), s["hours_source"], "lit" if s["lit_at_night"] else "dark", s["lit_why"])])
        if s.get("room"):
            rm = s["room"]
            rows.append(["room box", "W 5.3, H 2.4, D %.1f; floor: %s; walls: %s; dado %s; ceiling %s" % (rm["d"], rm["floor"]["material"], rm["walls"]["above"], rm["walls"]["dado"], rm["ceiling"])])
            rows.append(["contents of the room", " || ".join(goods_by_fixture(rm))])
            rows.append(["display (real, 0.55 deep)", "keeps: %s. Changes: %s. Items: %s" % (s["display"]["keeps"], s["display"]["changes"], display_str(s["display"]))])
            rows.append(["lights", "day: %s. night_lit: %s. night_dark: %s. Tubes: %d x 5 ft T12." % (rm["lights"]["day"], rm["lights"]["night_lit"], rm["lights"]["night_dark"], len(rm["lights"]["tubes"]))])
            rows.append(["pictures and spec", "%s_{day,night_lit,night_dark}.png 4096 x 1855 + %s.json; spec entry in target.json `spec_entries` (id %s, side %+d, card x %.2f to %.2f, display x %.3f to %.3f)" % (
                s["spec_id"], s["spec_id"], s["spec_id"], 1 if s["side"] == "east" else -1, s["card"]["x0"], s["card"]["x1"], next(e for e in T["spec_entries"] if e["id"] == s["spec_id"])["display"]["x0"], next(e for e in T["spec_entries"] if e["id"] == s["spec_id"])["display"]["x1"])])
        elif sid == "empty_unit":
            rows.append(["room", "none: every pane whitewashed from inside (4.1 `glass/empty_unit/window_whitewash`, 3250 x 1800 mm; the shop door's glass too), no card, no picture; a pale blank by day (LIT-03), dark at night; the letting board and boards as 4.1/4.4"])
        else:
            rows.append(["room", "the real walked room (mickeys-office.json; shop-room.py's mickeys branch; room_3d; the spec's lamps 150 lm, room 180 day and 300 night): not changed by this unit; the projected picture is only its far fallback"])
        table(["", ""], rows)
        if s.get("conflict"):
            w("**Conflict (not resolved):** " + s["conflict"])
            w()

    # ---- 6
    w("## 6. The three failures of 3 October, answered")
    w()
    w("Commit 2f475f5 (3 October) set the seven shops aside after three fresh reviews: goods made by hand, then named faults, then what a projected room cannot do at a metre or two.")
    w()
    for fl in T["previous_failures_answered"]:
        w("**%s. %s.**" % (fl["id"], fl["failure"]))
        w()
        if isinstance(fl["answer"], list):
            for a in fl["answer"]:
                w("- " + a)
            w()
        else:
            w(fl["answer"])
            w()
    # ---- 7
    w("## 7. Reuse: what each part keeps and what it changes")
    w()
    table(["part", "keeps", "changes"], [[x["part"], x["keeps"], x["changes"]] for x in T["reuse"]])
    # ---- 8
    w("## 8. Photographs win: each disagreement")
    w()
    for dgs in sorted(T["disagreements_photographs_win"], key=lambda d_: int(d_["id"][1:])):
        w("- **%s, %s.** Target: %s. Photograph or research: %s. Chosen: %s. Why: %s" % (dgs["id"], dgs["what"], dgs.get("target_2_2") or dgs.get("target"), dgs.get("photograph") or dgs.get("photograph/research"), dgs["chosen"], dgs["why"]))
    w()
    pm = T["photographs"]
    w("**The main photograph's readings** (P1; %s):" % pm["method"])
    w()
    table(["what", "pixel"], [[r_["what"], ("y %.1f" % r_["y_px"]) if "y_px" in r_ else ("x %.1f" % r_["x_px"])] for r_ in pm["rows"]])
    # ---- 9
    w("## 9. The inventory")
    w()
    inv = T["inventory"]
    w("**Every Poly Haven model the target places (%d, CC0, each read from api.polyhaven.com on 12 October with a 1k glTF):**" % len(inv["polyhaven"]))
    w()
    table(["id", "size cm", "triangles", "published", "shops"], [[k, "x".join("%g" % x for x in v["dims_cm"]), v["polycount"], v["published"], ", ".join(v["shops"])] for k, v in sorted(inv["polyhaven"].items())])
    w("**Looked at and refused (denied list; the self-check refuses any of them):**")
    w()
    table(["id", "why"], [[k, v] for k, v in sorted(inv["denied"].items())])
    w("**Made by script because no CC0 model exists (each with its reason; the cheapest method that should read at 1 to 3 m, per the GOODS note; any that fails its first try is set aside):**")
    w()
    table(["form", "shops", "why"], [[k, ", ".join(v["shops"]), v["why"]] for k, v in sorted(inv["scripted"].items())])
    w("**Scans (CC0, Sketchfab, on the allowlist as 'Sketchfab CC0 filter'; read 12 October; the download API answers 401 without a login, so none is downloaded):**")
    w()
    table(["uid", "name", "licence", "faces", "published"], [[v["uid"], v["name"], v["license"], v["faces"], v["published"][:10]] for v in inv["sketchfab_checked"].values()])
    tm = inv["texture_marks"]
    w("**Marks on the models' base-colour maps, and how each is blanked (the second fault of the review: the real retailer's name 'Dixons' stood on `cassette_player`).** After the review the writer opened the 1k base-colour map of every one of the %d models (25 contact sheets at 512 px; the marked ones at 1k with the boxes drawn on them) and found the marks below; thumbnails alone had missed them. Every model carries `marks` in `inventory.polyhaven` (a mark, or none seen at 1k). The step, for every map below: %s" % (len(inv["polyhaven"]), tm["step"]))
    w()
    mrows = []
    for mid in tm["models_with_marks"]:
        rec_ = inv["polyhaven"][mid]
        for b_ in rec_["blank"]:
            mrows.append([mid, rec_["marks"] if b_ is rec_["blank"][0] else "(as above)", b_["map"], "; ".join(str(bx) for bx in b_["boxes"]), b_["fill"], b_["reads"]])
    table(["model", "what is printed on it", "map (1k, 1024 x 1024)", "boxes [x0, y0, x1, y1]", "fill", "what the boxes hold"], mrows)
    w("**What is kept:** " + "; ".join("%s: %s" % (m_, inv["polyhaven"][m_]["keep"]) for m_ in tm["models_with_marks"] if inv["polyhaven"][m_].get("keep")) + ".")
    w()
    nts = [(m_, inv["polyhaven"][m_]["marks_note"]) for m_ in tm["models_with_marks"] if inv["polyhaven"][m_].get("marks_note")]
    w("**Notes on particular models:** " + "; ".join("%s: %s" % x_ for x_ in nts) + ".")
    w()
    w("**The final texture is checked (INV-06).** Script: " + tm["final_check"]["script"] + ". Visual: " + tm["final_check"]["visual"] + ".")
    w()
    w("**The brand blocklist** (`inventory.brand_blocklist`, searched by INV-05 and the self-check): " + ", ".join("'%s'" % b_ for b_ in inv["brand_blocklist"]) + ". The first four are the real British high-street retailers the review named; the next group are the makers and look-alikes read off the maps.")
    w()
    w("**Surfaces:** Poly Haven textures " + ", ".join(inv["surfaces"]["polyhaven_textures"]) + " (all exist: LIVE check); ambientCG " + ", ".join(inv["surfaces"]["ambientcg"]) + " (the ones read from its API are in ambientcg_checked.json). The packaged goods' labels are the project's atlas (production/assets/shop-goods/labels.jpg: 32 fictional makers in our OFL fonts), twelve tiles to add.")
    w()
    w("**Rules the inventory enforces.** " + inv["rule"])
    w()
    # ---- 10
    w("## 10. Checks (target.json `checks`; the cloud gate and the build run them)")
    w()
    table(["id", "name", "measure", "expected", "tolerance", "applies to"], [[c["id"], c["name"], c["what"], c["expected"], c["tolerance"], ", ".join(c["applies_to"]) if len(c["applies_to"]) < 5 else "%d shops" % len(c["applies_to"])] for c in T["checks"]])
    cr_ = json.load(open(os.path.join(HERE, "controls_result.json")))
    import controls as CT   # the list of mutations
    w("**Self-check** (before anything is built): %s. Groups: %s. Negative controls: %d of %d mutations of target.json make it fail (controls.py): %s." % (
        T["self_check"]["result"], "; ".join("%s: %d pass %d fail %d reported" % (k, v["pass"], v["fail"], v["report"]) for k, v in sorted(T["self_check"]["groups"].items())), cr_["caught"], cr_["of"], "; ".join(CT.CONTROLS.keys())))
    w()
    # ---- 11
    w("## 11. What the target could not settle")
    w()
    for c in T["could_not_settle"]:
        w("- " + c)
    w()
    w("**Needs Jafar (at most three, one line each, recommended first):**")
    w()
    for n in T["needs_you"]:
        w("- %s Recommended: %s. Why: %s." % (n["q"], n["recommended"], n["why"]))
    w()
    # ---- 12
    w("## 12. Previews")
    w()
    w("Eleven JPEGs in production/previews/cloud-week/refs/shop-windows/ (at most 1200 px, under 300 KB each; credits in section 2). **What is masked in each, exactly** (flat grey 120, 120, 120, drawn on the original before the crop by `make_previews.py` on every rebuild from the list `extras.PREVIEW_PHOTOS`, then read back from the JPEG it wrote; `self_check.py` reads the committed JPEGs against the same list, checks PRV-01 to PRV-03; every preview was looked at by eye after the rebuild of 12 October and none shows a real firm's name, a door number, a face, alcohol, a gambling sign or a child):")
    w()
    pv_ = T["previews"]
    for ph in pv_["photos"]:
        name_ = ph["name"] + ".jpg"
        ms_ = ph["masks"]
        w("- **%s `%s`** (original crop %s). %s Masked: %s" % (ph["id"], name_, ph["crop"], ph["cropped_away"][0].upper() + ph["cropped_away"][1:] + ("." if not ph["cropped_away"].endswith(".") else ""),
            ("; ".join("%s (%s %s)" % (m_["what"], "box" if m_["shape"] == "rect" else "polygon", m_["box"] if m_["shape"] == "rect" else m_["poly"]) for m_ in ms_) + ".") if ms_ else "nothing needed masking (nothing legible is in the crop)."))
    w("- **P1 overlay `P1-worcester-fish-front-target-on-photo.jpg`**: made from the masked P1 crop, so it carries the same three masks (the door's number plate included) with the target's door, stallriser, glass-foot and glazing-bar lines laid on at the scale fitted on the leaf's height.")
    w("- **D1 `D1-ritas-front.jpg`, D2 `D2-ten-fronts-sheet.jpg`, D3 `D3-ritas-room-plan-picture.jpg`, D4 `D4-standoff-and-cameras.jpg`**: drawn from target.json alone; no photograph is in them and nothing in them is masked. D1 and D2 now show the band above the doors (fanlight, transom, three toplights, panel, head) and the aligned toplights on every front.")
    w("- The earlier P6 (it showed the old fascia's lettering and the neighbouring board) and the earlier P1 (it showed the door's number) were deleted from the folder and rebuilt as above; the earlier files remain in the history of the commit that first added them.")
    w()
    open(os.path.join(HERE, "TARGET.md"), "w").write("\n".join(OUT) + "\n")
    print("wrote TARGET.md", len("\n".join(OUT).split()), "words")


if __name__ == "__main__":
    build()
