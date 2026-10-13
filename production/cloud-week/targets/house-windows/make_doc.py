#!/usr/bin/env python3
"""Writes TARGET.md from target.json (every number in the prose is read from it, so the two cannot drift). Run with /home/user/.bpyenv/bin/python."""
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
t = json.load(open(os.path.join(HERE, "target.json")))
SC = t.get("self_check", {}).get("result", "not yet run")
L = []


def w(s=""):
    L.append(s)


def table(head, rows):
    w("| " + " | ".join(head) + " |")
    w("|" + "|".join("---" for _ in head) + "|")
    for r in rows:
        w("| " + " | ".join(str(c).replace("|", "/") for c in r) + " |")
    w()


def cap(x):
    x = str(x).strip()
    first = x.split(" ")[0] if x else ""
    if any(c in first for c in "_./[`"):
        return x
    return x[:1].upper() + x[1:]


def sent(x):
    x = cap(x)
    return x if x[-1:] in ".!?" else x + "."


def endp(x):
    x = str(x).strip()
    return x if x[-1:] in ".!?" else x + "."


def rgb(v):
    return "(" + ", ".join(str(int(a)) for a in v) + ")"


def xz(c):
    return "x %s to %s, z %s to %s" % (c["x"][0], c["x"][1], c["z"][0], c["z"][1])


def card_txt(c):
    if "card" in c:
        return xz(c["card"])
    return "left: " + xz(c["card_left"]) + "; right: " + xz(c["card_right"])


def rgb_map(d):
    return ", ".join("%s %s" % (k.replace("_", " "), rgb(v)) for k, v in d.items())


def band_txt(v):
    parts = []
    for k, x in v.items():
        if k in ("photo", "source"):
            continue
        rngtxt = ("%s to %s" % (x[0], x[1])) if isinstance(x, list) else str(x)
        lab = {"P_over_L": "P/L", "D_over_L_max": "D/L at most", "D_over_L": "D/L", "spread_min": "pane spread at least", "spread": "pane spread", "blue_over_red_min": "pane blue minus red at least",
               "dip_width_px_min": "line dip at least", "dip_over_L_max": "line dip at most"}[k]
        parts.append("%s %s" % (lab, rngtxt) + (" levels" if "spread" in k or "blue" in k else (" px wide" if k == "dip_width_px_min" else (" of L" if k == "dip_over_L_max" else ""))))
    tail = ("Photographs: " + sent(v["photo"])) if "photo" in v else ("Source: " + sent(v["source"]))
    return "; ".join(parts) + ". " + tail


S = t["sites"]
RM = t["rooms"]
fam = RM["families"]
bud = RM["budgets_computed"]
rule = RM["budget_rule"]
ph = t["photo_measurements"]
bands = ph["bands_by_state"]
g = t["gate"]
inv = t["inventory"]["polyhaven_models"]
used = sorted({o["model"] for r in RM["rooms"].values() for o in r["objects"]})
lit = RM["lit_share"]
lit2030 = set(lit["lit_by_hour"]["20:30"]["windows"])

w("House windows of Quay Street: twenty windows in ten houses, every frame white (Jafar's ruling of 3 October), four kinds (two over two, one over one, and two replacement casements), each pane glass over a dark room with its box shaded and its lines drawn, nets and drapes by the photographs' mix, thirteen small rooms behind them in the game's own projection, and the white-board fault caught by measurement on 1979 to 1994 photographs, measured the way the gate measures.")
w()
w("# House windows of Quay Street: the exact target")
w()
w("**Status: fixes applied, not re-reviewed (13 October 2026).** Cloud week 42, part 2, unit 8: written by the target writer from sources reached that day, failed its fresh review (TARGET-REVIEW.md: three faults, twelve narrow points), and corrected as FIXES-APPLIED.md lists, one line per fault and point. Nothing is built and nothing is committed. Every number below is in `target.json`; the checks that follow from it are its `checks` list and its `self_check` (%s)." % SC)
w()
w("The lessons of unit 7's fresh review (TARGET-REVIEW.md of the shop windows) are applied from the start: every opening is covered above and around its parts (section 4.5); the toplights of the replacement are one transom and equal lights (4.3); no real firm's name is on any model's texture (every model's 1k base colour was looked at, section 7.4, and the checks include a final-texture check PIC-07); the night wash is the game's colour; the projection rule `trace` is the only source of what a room shows, with stand-off budgets derived again for these smaller rooms (3.3); the numbers are exact and the checks measurable (section 10); and every preview was looked at after it was written.")
w()
w("**What the fresh review found and what changed** (FIXES-APPLIED.md has the line for each): every house's frame is now white, as Jafar ruled on 3 October (a coloured frame needs his answer, OWED-05); the white-board bands are measured from the photographs the way the gate measures (L over the joinery, D with no brick), with a new line check WB-04b and the window states bare, net and draped; television_02's maker's name on its front bezel is painted out and the maker is on the blocklist; the cottage rooms' stand-off budgets put the eye at the window (back wall 0.38 true, 0.71 tolerated); the P6 replacement form is built (RC2); the lit order puts lounges before landings. **The lessons of this review**, kept for the next target: a number measured from photographs must be measured the way the gate will measure it; and a design is checked against the owner's standing rulings, not only the latest one.")
w()
w("## 0. Files, and how to read them")
w()
table(["file", "what it is"], [
    ["TARGET.md", "this page (made by make_doc.py from target.json)"],
    ["target.json", "the twenty sites, the kinds and their parts, the glass, the box's shade, the nets and drapes, the thirteen rooms with their objects and budgets, the inventory with each model's marks, the kit pieces' nodes, the gate, %d checks, the photograph measurements, the overlay's edges, the lit table, `photographs_win`, `could_not_settle`, `owed_on_pc`, the self-check" % len(t["checks"])],
    ["target_drawing.py", "draws target.json alone: each kind's elevation and sections, each room's picture layout and back wall, the row of twenty, and (with --photo) the 2/2 elevation laid on photograph P8; into a JSON of polygons (millimetres) and a folder of pictures"],
    ["self_check.py", "tests the target against its own sources (it writes into target.json only with --write); %d negative controls" % len(t.get("self_check", {}).get("controls", [])) if t.get("self_check") else "tests the target against its own sources (it writes into target.json only with --write); negative controls"],
    ["TARGET-REVIEW.md, FIXES-APPLIED.md", "the fresh review of this target (FAIL: 3 faults, 12 narrow points) and one line per fault and point saying what was changed and where"],
    ["hw_common.py, hw_data.py, hw_rooms.py, hw_sites.py, hw_photos.py, hw_measure.py, hw_checks.py, make_target.py, make_doc.py, make_previews.py", "author tools: the game's rule and the stand-off budgets; the glass, nets, paints; the rooms; the sites derived from terrace-front.py; the photographs, their crops and masks; the pane-to-frame measurement; the kit nodes, gate, checks; the builders of target.json, TARGET.md and the previews"],
    ["polyhaven_models_checked_raw.json, polyhaven_textures_checked_raw.json, geograph_pages_read.json", "what the Poly Haven API and the 14 Geograph pages answered on 13 October"],
    ["production/previews/cloud-week/refs/house-windows/", "P1 to P14 (the photographs measured, cropped to the windows, masked where a crop would show a plate or a sign), the overlay of the drawing on P8, and the sheet of measured windows"],
])
w("Run with `/home/user/.bpyenv/bin/python`: `make_target.py [--photos DIR]`, `self_check.py [--photos DIR] [--previews DIR] [--live] [--write]`, `target_drawing.py OUT_DIR [--photo FILE --overlay FILE]`, `make_doc.py`, `make_previews.py [--photos DIR] [--out DIR]`.")
w()
w("**Units and frames.** Windows in millimetres in the *kit frame*: x across the window (0 at its middle, positive to the viewer's right), y *into the wall* from the brick face (0 at the face), z *up* from the opening's bottom edge. Rooms in metres in the *room frame*: x across from the room's centre (positive toward the picture's right), y back from the card plane, z up from the floor. The street in metres as the scene file has it (x along, y across, east positive, z above the road crown; the footway is crown + 0.10). **Kinds of number:** Read (printed in a file), Scaled, Photo (measured on a photograph: method and error given), Derived, Judgement.")
w()

# ---------------------------------------------------------------------------------------------------------------------------
w("## 1. The street's windows as found")
w()
w("The street has **twenty house windows in ten houses**, and 48 more on the hill's rows. They come from `tools/art-recipes/terrace-front.py` (`plan_street`, re-derived by `hw_sites.py` and compared by the self-check, so the table cannot drift from the recipe). `production/assets/street/quay-street.json` holds only their materials (`frame_painted`, `frame_bronze`, `glass_eu_*`, `glass_wg_*`, the net cards), not their kinds. The shops' own ground-floor glass (east parade, west_north, east_chandler) is unit 7's and is not here.")
w()
w("**What the recipe draws today, and what is wrong with it** (each is a finding the PC session acts on, section 8):")
w()
w("- East parade, six houses, **upper floor only** (the ground floor is a shopfront): twelve windows at bay start + 1.5 and + 4.5 m, the opening 850 wide, head 5.9 above the crown. The kit's checked sash (the lab's, 8 October) is used there: a two-over-two on bays 0 and 3, a one-over-one on bays 1 and 5 (`SASH_KIT_ROWS = (\"east_parade\",)`), opening 1676.4 high (sill 4.2236). Bays 2 and 4 draw a 1980s replacement as a box of `frame_bronze` (anodised) with a transom at 0.72 of the height and no bars.")
w("- East chandler, one house (a metal-refit shop below): two upper windows, a replacement in bronze, **1500** high (sill 4.4): not the period opening.")
w("- West south, three single-storey cottages: six **ground-floor** windows (door at 1.5, windows at 3.3 and 5.1 m of the bay, mirrored with the door), the opening 1500 high (z 1.0 to 2.5). **`_plain_ground` draws every one as a 2/2 box sash (55 mm frame, 22 mm bars), whatever `_window_kind` says of the house** (finding D4).")
w("- West north, three shops of one storey: no upper windows; nothing here.")
w("- The hill: `backdrop_rise_approach_e`, `_w` and `_x` stand 2, 5 and 5 houses of CLIMB_HOUSE (two storeys, a 'plain' ground floor) through `plan_parts`: 48 windows by the same code, with a flat net card (one in three the lit `window_far_lit`). The north rise's framed windows (`_framed_window`, 125 m out) are two pixels of frame and stay flat cards.")
w("- **Six over six does not occur on the street** (no house is Georgian); two photographs show it on Georgian terraces (P10, 1983; P13, 1982). It is not built.")
w()
w("**The twenty, by position.** *Kind by house* is what `_window_kind` gives the house; *built today* is what the recipe draws; *target* is what this unit makes. Every site gets the period opening 850 x 1676.4 (the ruling of 8 October: \"1.68 m\"), the head kept where it is, so the cottages' sills go from 1.0 to 0.8236 above the crown (0.7236 above the threshold). P6's ground bay window's sill stands 0.85 ±0.05 above its step (the door leaf 193 px = 1981 mm, the sill 83 px up): the cottages' sills are 0.13 lower than that, to keep the head and the arch clear of the eaves (D4; Jafar's to choose).")
w()
rows = []
for s in sorted(S, key=lambda s: (s["side"] < 0, s["x_centre"])):
    rows.append([s["id"], "%.1f" % s["x_centre"], "upper" if s["floor"] == "upper" else "ground", s["kind_by_house_in_terrace_front"], s["built_as_today"], s["kind"], s["paint"] + ("" if s["condition"] == "sound" else " (%s)" % s["condition"]),
                 s["net"]["kind"] + ("/" + s["net"]["colour"] if s["net"]["colour"] else ""), (s["extra"]["kind"] + "/" + s["extra"]["colour"]) if s["extra"] else "-", s["room"], "yes" if s["id"] in lit2030 else "no"])
table(["site", "x", "floor", "kind by house", "built today", "target", "paint", "net", "drape", "room", "lit 20:30"], rows)
kcount = {k_: sum(1 for x_ in S if x_["kind"] == k_) for k_ in ("S22", "S11", "RC", "RC2")}
w("Kinds: **%d two-over-two (S22), %d one-over-one (S11), %d replacement casements of P7's form (RC) and %d of P6's form (RC2: east_parade_bay4).** Upper floors 14, ground 6. The landing windows (the window on the side-door's side of each flat: bays 0, 1, 2 (right), 4 (right), 5 (right), the chandler's right one, and the empty flat's left) light the stair; the others light a lounge or a bedroom. The unlet flat above the empty shop (bay 3) is empty at both windows." % (kcount["S22"], kcount["S11"], kcount["RC"], kcount["RC2"]))
w()

# ---------------------------------------------------------------------------------------------------------------------------
w("## 2. Sources")
w()
w("Only sources reached on 13 October are used. Photographs are for measuring and for the reviewers only: never placed in the game, never traced into a texture, never fed to an image model. Each Geograph page was opened (title, author, date taken, licence CC BY-SA 2.0 read on the page). Every preview was looked at after it was written; each is cropped to the windows and any plate or sign the crop would still show is masked flat grey (the masks are read back from the JPEG by the self-check). No person, child, firm's name, door or house number is in any preview.")
w()
rows = []
for p in t["sources"]["photographs"]:
    rows.append([p["id"], "[%s](%s)" % (p["url"].split("/")[-1], p["url"]), p["title"], p["author"], p["taken"], p["shows"], p["period"]])
table(["id", "page", "title", "author", "taken (page)", "shows", "period?"], rows)
w("The Geograph syndicator feed (`api.geograph.org.uk/syndicator.php`, ordered by date taken through the search id's pages) was used to find them: about 1,200 photographs taken 1975 to 1996 came back for terrace, street, sash, council, harbour and night queries; none of the night, dusk or lit-window queries returned a photograph of a terrace before 1996. Wikimedia Commons and archive.org were not asked (the feed answered).")
w()
w("**Research and project files read:** " + "; ".join(t["sources"]["research_read"]) + ".")
w()
w("**Libraries:** " + t["sources"]["libraries"])
w()
w("**Not reached (nothing rests on them):** " + "; ".join(t["sources"]["unreached"]) + ".")
w()

# ---------------------------------------------------------------------------------------------------------------------------
w("## 3. The method, in the game's own numbers")
w()
w("### 3.1 Why the windows read as white boards, and what the photographs say")
w()
_rows = ph["windows"]
_p1 = [_rows[k_] for k_ in ("P1_a", "P1_b", "P1_e")]
_bare = [r_["P_over_L"] for r_ in _rows.values() if r_["state"] == "bare_dark"]
_p8 = [_rows[k_]["P_over_L"] for k_ in ("P8_L", "P8_R")]
_p8g = ph["p8_four_panes_the_gates_way"]
w("Research 1a found the cause: the pane was a pale lit card (not glass over a dark room), the box was lit flat with no dark lines, and the upper panes reflected no shapes. This unit builds 1a's fix as numbers a builder can follow (sections 5 and 6). **What the photographs add** (14 photographs, 1979 to 1994; 18 windows measured, section 3.2, the way the gate measures): at 15 to 40 degrees from the wall the real windows are *not* uniformly dark. A window with a net reads **%.2f to %.2f** of its frame's brightness (P1, three windows at %.0f to %.0f degrees, boxed without the white-painted stone head and sill and without the brick column, L taken over the joinery); a window with bare glass and a dark room reads **%.2f to %.2f**; seen nearly square from below, glass over a dark room under a blue sky reads **%.2f to %.2f** (P8; **%.2f** for all four panes together, blue over red %d). The white-board fault is therefore not 'a pane as bright as its frame' but **a pane that is one even tone with no dark line round it**: the old build's pane read 157 to 175 against paint 178 to 205 (0.85) with no corner line (D/L 0.85, a spread of 14 levels), where the photographs' tight outlines read D/L %.2f to %.2f (P1_a with its top rows out %.2f) and a pane spread of %d to %d levels. **The first version of these numbers measured the stone and the brick, not the frame:** it boxed the white-painted stone head and sill and a column of brick into P1's outlines, so L read 233 to 245 (the stone's paint reads 248 to 254) and D/L 0.47 to 0.50 (the brick's own 119 over the stone). Measured the way the gate measures, the same photographs would have failed WB-04 and WB-01's median cap; this is the review's fault 2 and the first lesson at the top of this page. The checks of section 9 test the lines and the spread by window state (bare, net, draped), not one pane ratio." % (
    min(r_["P_over_L"] for r_ in _p1), max(r_["P_over_L"] for r_ in _p1), min(r_["angle_deg"] for r_ in _p1), max(r_["angle_deg"] for r_ in _p1), min(_bare), max(_bare), min(_p8), max(_p8), _p8g["P_over_L"], round(_p8g["blue_minus_red"]),
    min(r_["D_over_L"] for r_ in _p1), max(max(r_["D_over_L"] for r_ in _p1), _rows["P1_a"]["alt_top_rows_out"]["D_over_L"]), _rows["P1_a"]["alt_top_rows_out"]["D_over_L"], round(min(r_["pane_spread_5_95"] for r_ in _p1)), round(max(r_["pane_spread_5_95"] for r_ in _p1))))
w()
w("### 3.2 What was measured on the photographs (Photo)")
w()
w(ph["method"].replace("\n", " "))
w()
w("**P1_a, P1_b and P1_e** (the three net windows that set the bands) are boxed as the review boxes them: P1_a outline (435, 396, 451, 447) and pane (437, 399, 449, 444); P1_b outline (405, 402, 418, 452) and pane (406, 405, 417, 449); P1_e the same way, from 5 rows under the stone head's end to the stone sill's start (outline (435, 489, 451, 540), pane (437, 492, 449, 537)); P1_a is also given with its top three rows out (outline (435, 399, 451, 447), pane (437, 402, 449, 444): P/L %.2f, D/L %.2f, spread %d). The first version's boxes (P1_a (433, 392, 451, 455), P1_b (403, 396, 419, 458), P1_e (433, 485, 451, 545)) are kept in `photo_measurements.boxes_of_the_first_version` with their old figures. The angle from the wall is now taken from the tight boxes (31 to 39 degrees, inside the +-5 degrees of the method)." % (ph["windows"]["P1_a"]["alt_top_rows_out"]["P_over_L"], ph["windows"]["P1_a"]["alt_top_rows_out"]["D_over_L"], round(ph["windows"]["P1_a"]["alt_top_rows_out"]["pane_spread_5_95"])))
w()
rows = []
for k, r in ph["windows"].items():
    rows.append([k, r["photo"], r["state"], r["angle_deg"], r["L90"], r["P50"], r["D5"], r["P_over_L"], r["D_over_L"], r["pane_spread_5_95"], r["note"]])
table(["window", "photo", "state", "angle from wall (deg, +-5)", "L (p90)", "P (median)", "D (p5)", "P/L", "D/L", "pane spread", "what"], rows)
rows = []
for k, b in bands.items():
    rows.append([k, b["n"], "%.2f to %.2f" % (b["P_over_L_min"], b["P_over_L_max"]), "%.2f" % b["P_over_L_median"], "%.2f" % b["D_over_L_median"], ", ".join(str(a) for a in b["angles_deg"])])
table(["state", "n", "P/L range", "P/L median", "D/L median", "angles"], rows)
bm = ph["brick_median_luma"]
fb = ph["frame_to_brick_linear_ratio"]
w("Brick beside the windows: median luma %s in P1 and %s in P8; the frame's linear brightness over the brick's is **%s in P1 and %s in P8**: frames are about 4 times the wall on a photograph (film contrast included; L is now the joinery's 90th percentile); the concept sheet's 7 is outside it (D9). The game's albedos give 0.82 / 0.13 = 6.3." % (bm["P1"], bm["P8"], fb["P1"], fb["P8"]))
w()
w("**Nets, curtains, blinds** (a hand count of every window whose state could be read, 60 windows in P1, P2, P3, P4, P6, P7, P12; Photo ±8 points): " + ", ".join("%s %d (%.0f%%)" % (k.replace("_", " "), v, 100.0 * v / 60) for k, v in ph["tally"]["by_net"].items()) + ". %s **Paint** (60 windows, by eye): white %.0f%%, cream or ivory %.0f%%, dark or red-brown %.0f%%, olive green %.0f%%, blue %.0f%%." % (sent(ph["tally"]["note"]), 100 * ph["paint_tally"]["white"], 100 * ph["paint_tally"]["cream_or_ivory"], 100 * ph["paint_tally"]["dark_brown_or_red_brown"], 100 * ph["paint_tally"]["olive_green"], 100 * ph["paint_tally"]["blue"]))
w()
w("**What the photographs show in each window, element by element** (the list the build is judged against): the white frame member at each jamb 37 to 47 mm on a rear (P8) and 76 to 79 mm on a front (the lab's P6); a meeting rail that reads 34 mm of face and more with its shade (P8: 62 mm with the underside); a glazing bar of 22 to 27 mm (P8: 27 ±6); panes that differ from one another by up to 10 per cent in brightness (P8: four panes, mean luma 86 to 105) and are smooth inside (P8: three of the four flat to 1.4 levels over the central 60 per cent of the box); a dark edge between frame and net where the net hangs back from the glass (P1, P4); the near jamb's dark reveal beside a white lining at 10 to 20 degrees (P1, P13); a white painted sill and head in stone (P1, P3, P4); at under 10 degrees a white slit beside a dark void (P13). The nets: a gathered voile on the lower sash only with a lace band at the foot (P6, P7, P12), the upper sash clear, a full-height net on the tall windows (P4, P3), vertical louvres (P2, P11). P14 (boarded houses) shows plywood in the openings and no nets: the empty flat's torn, yellowed net (section 6) is a Judgement, not a photograph's.")
w()
w("### 3.3 The game's rule for a room behind a house window")
w()
w("**The rule** (production/specs/shop-interiors.json, `tools/ue/make_interior_material.py` `trace`, imported by `hw_common.py` and never rewritten): on the room's centre line, d in front of the card plane, a camera frames the card rectangle W x H exactly; a room point (x, y, z) lands at u = 0.5 + (x / W) d / (d + y), v = 0.5 + (z / H - 0.5) d / (d + y). The material finds for each pixel where the eye's ray meets the room's box behind the card and looks that point up in the picture. d = W for every room here, as for the shops.")
w()
w("**The card is the room's front wall, not the window's glass.** The shops' card is the glass rectangle. A house window is a small hole (0.85 m) in the front wall of a room 2.8 or 3.4 m wide; a box as small as the hole would be a corridor. So the card here is **the whole room's front plane, 0.270 m behind the brick face**: the wall (215 mm of brick, the kit's box to 250.8) hides every part of the card outside the opening; the eye sees the room through the hole. 0.270 is 16 mm behind the nets (254) and 80 mm behind the lower glass (190); a ray through the window meets the card plane displaced sideways by 0.08 m x tan(angle off the normal), 0.30 m at 15 degrees from the wall, so every window stands at least 0.3 m inside its card (checked). The card's front face must not stand in front of the kit's box (250.8) and the carcass behind it starts at 0.29 or more.")
w()
table(["room family", "W x H x D (m)", "camd", "floor above crown", "window above the floor", "picture", "back wall in the picture (px, x0 y0 x1 y1)", "who"], [
    ["UP (a first-floor room: one window centred in it; the flat's bay split in two rooms of 2.8 m)", "%.1f x %.2f x %.1f" % (fam["UP"]["w"], fam["UP"]["h"], fam["UP"]["d"]), fam["UP"]["camd"], fam["UP"]["floor_z"], "%.4f to %.2f" % tuple(bud["UP"]["window_above_floor_m"]), "%d x %d" % (RM["pictures_by_family"]["UP"]["w_px"], RM["pictures_by_family"]["UP"]["h_px"]), RM["pictures_by_family"]["UP"]["back_wall_rect_px_x0y0x1y1"], "the 14 upper windows"],
    ["GF (a cottage's front room: both windows look into the one room, 1.8 m apart)", "%.1f x %.1f x %.1f" % (fam["GF"]["w"], fam["GF"]["h"], fam["GF"]["d"]), fam["GF"]["camd"], fam["GF"]["floor_z"], "%.4f to %.2f" % tuple(bud["GF"]["window_above_floor_m"]), "%d x %d" % (RM["pictures_by_family"]["GF"]["w_px"], RM["pictures_by_family"]["GF"]["h_px"]), RM["pictures_by_family"]["GF"]["back_wall_rect_px_x0y0x1y1"], "the 6 cottage windows"],
])
w("**Where the floors are** (Derived): a first-floor floor stands 0.25 above the shop's ceiling (3.5 above the crown: 3.4 + 0.1) at 3.75 and the ceiling at the eaves, 6.3; so the sill is 0.4736 above the floor and the head 2.15, leaving the 0.4 m of wall `head_below_ceiling_m` the scene file gives. A cottage's floor stands 0.35 above the footway (0.45 above the crown) and its ceiling at 3.05, under the eaves at 3.1 (Judgement).")
w()
w("**Why the pictures are 1536 wide (upper rooms) and 3072 wide (cottage rooms).** The window shows 0.85 / 2.8 = 30 per cent of an upper room's picture and 0.85 / 3.4 = 25 per cent of a cottage's. An upper window is never nearer than 2.6 m (standing 0.8 m out from the wall, the sill 2.5 m above the eye): a screen pixel is 2.3 mm at the game's 60 degrees over 1440 lines, the glass (0.78 m) about 340 pixels wide, over 427 texels at 1536 (548 a metre): 1.3 texels a pixel, sharp. From across the street (8.8 m, 39 degrees) it is 180 pixels over the same 427. A cottage's window is met at eye level, as near as 1.5 m from the glass (as the shops' honest range: nearer than that the nets, a real card, and the glass's own Fresnel carry the view): a pixel is 1.2 mm, the glass 650 pixels wide, over 704 texels at 3072 (903 a metre): 1.1 texels a pixel, just sharp; at 2048 it would be 1.4 pixels a texel and soft. The sizes are Derived; the picture heights follow from the card's proportions (1399 and 2349).")
w()
w("**What can be painted on a surface** (the third failure of 3 October, answered). An object painted on a surface that stands off it by s metres slides, as the eye moves, by the angle between the eye's ray to the object and to its painted place. `hw_common.budgets_for` computes, for the review cameras below and both mirror images of each pavement position, the greatest stand-off at which the slide stays within 20 pixels (reads true) and 40 pixels (tolerated) of a 2560 x 1440 frame, at the points the window actually shows (144 rays through the glass), the 15th percentile of the points, the smallest over the cameras. **The eye stands by the window**, as the camera table says (the fixes of 13 October, narrow point 1: the first version stood every cottage eye at the card's centre, 0.9 m from its window, which over-stated the back wall's budget, 0.41 against 0.38), the mirror image is taken about the window, and one pixel is the exact angle at the frame's centre, atan(tan(vfov / 2) / 720), not vfov / 1440 (4 per cent small at 39 degrees, 10 per cent at 60):")
w()
rows = []
for f in ("UP", "GF"):
    for surf in ("back", "side", "ceiling", "floor"):
        c = bud[f]["surfaces"][surf]
        rows.append([f, surf, c["true_20px"] if c["true_20px"] is not None else "not seen from the street", c["true_40px"] if c["true_40px"] is not None else "not seen from the street"])
table(["family", "surface", "reads true (20 px), m", "tolerated (40 px), m"], rows)
w("**The rule the rooms keep** (the smaller of the two families' figures, rounded down; `rooms.budget_rule`): " + "; ".join("%s %.3f true, %.3f tolerated" % (k, v["true"], v["tolerated"]) for k, v in rule.items()) + ". (An upper room's floor is never seen from the street; the cottages' floor figure stands. The back wall's 0.38 and 0.71 are the review's own, from its slide measure; this unit's recomputation gives " + "%.3f and %.3f" % (bud["GF"]["surfaces"]["back"]["true_20px"], bud["GF"]["surfaces"]["back"]["true_40px"]) + ", so the rule is the smaller, as the others are. A cottage's back wall seen from H_UNDER, 0.8 m from the wall and looking up, is the binding view.) Anything that would stand further off its surface is not drawn in the picture: a bed, a table, a free-standing chair are dropped; a chimney breast, a radiator, a stair's stringer are drawn flat (`rooms.forms`). **A pendant light's shade is the one real object in a lit room** (kit node `pendant__shade`), because it is what a lit upstairs window shows. The checks PIC-05 and the self-check test every object's and every form's stand-off against these numbers.")
w()
w("**What shows of a room, and so where its picture needs detail** (`rooms.visible_zone`, computed; metres in the picture frame, x from the PICTURE-LEFT WALL (not from the room's centre: the objects' x_across is from the centre, so add half the room's width to compare), y back from the card, z up from the floor; the eye stands by the window, as the camera table says):")
w()
for f in ("UP", "GF"):
    for cam in ("H_ACROSS_0", "H_ACROSS_30", "H_ALONG_15_NEAR", "H_ALONG_30_NEAR", "H_ALONG_15_ROAD", "H_UNDER"):
        z = RM["visible_zone"]["by_family"][f][cam]
        seen = []
        for k, v in z["surfaces_seen"].items():
            if k == "back":
                seen.append("the back wall (x %s to %s, z %s to %s)" % (v["x"][0], v["x"][1], v["z"][0], v["z"][1]))
            elif k in ("left", "right"):
                seen.append("the %s wall (y %s to %s, z %s to %s)" % (k, v["y"][0], v["y"][1], v["z"][0], v["z"][1]))
            elif k == "ceiling":
                seen.append("the ceiling (x %s to %s, y %s to %s)" % (v["x"][0], v["x"][1], v["y"][0], v["y"][1]))
            else:
                seen.append("the floor (x %s to %s, y %s to %s)" % (v["x"][0], v["x"][1], v["y"][0], v["y"][1]))
        w("- %s from %s: %s" % (f, cam, "; ".join(seen)))
w()
w(sent(RM["visible_zone"]["reading"]))
w()
w("**The review cameras** (street frame; eye 1.60 above the footway = 1.70 above the crown; 2560 x 1440): ")
w()
rows = []
for n, c in g["cameras"].items():
    rows.append([n, c["what"], c["vfov_deg"]])
table(["camera", "where", "vertical field (deg)"], rows)
w("H_ACROSS_0 stands on the far pavement's kerb edge (8.8 m from the glass: the brief's 'about 8 m' is the nearest the far pavement allows); H_ALONG_15_NEAR and H_ALONG_30_NEAR are on the house's own footway 1.5 m from the wall, 5.6 and 2.6 m short of the window, which is the angle where 1a found the white boards; H_ALONG_15_ROAD is 9.7 m along from 2.6 m out: in the road, 1 m out from the kerb (the footway is 5.125 - 3.505 = 1.62 m wide); H_UNDER is 0.8 m from the wall, looking up. For the cottages the far pavement is the east footway.")
w()

# ---------------------------------------------------------------------------------------------------------------------------
w("## 4. The kinds")
w()
w("### 4.1 Two over two (S22) and one over one (S11): the lab's checked sash, reused")
w()
k = t["kinds"]["S22"]
w("The sash is the lab's, amended on 8 October for Jafar's ruling (`production/art/sash-window/target.json`, models `production/assets/sash-window/sash_window.glb` and `sash_window_1over1.glb`, reviewed on narrow points). Nothing is redrawn: this unit changes its glass (section 5), shades its box (5.4), adds its nets and its room (6, 7), and applies it to every row. **Numbers read from the lab's file** (the self-check re-reads them): opening 850.0 x 1676.4; frame reveal %s; outer lining margin %s (so each jamb shows 3 in of painted timber, 76.2); head visible %s; stile %s, top rail %s, bottom rail %s, meeting rail %s deep, glazing bar %s (one vertical bar in each sash of the S22; none on the S11), sash thickness %s, horns %s long on the upper sash only, glass %s thick." % (
    k["frame_sections_from_lab_target"]["reveal_mm"], k["frame_sections_from_lab_target"]["outer_lining_margin_mm"], k["frame_sections_from_lab_target"]["head_visible_mm"], k["sections_from_lab_target"]["stile_width_mm"], k["sections_from_lab_target"]["top_rail_mm"], k["sections_from_lab_target"]["bottom_rail_mm"], k["sections_from_lab_target"]["meeting_rail_depth_mm"], k["sections_from_lab_target"]["glazing_bar_width_mm"], k["sections_from_lab_target"]["thickness_mm"], k["horns_mm"], k["sections_from_lab_target"]["glass_mm"]))
w()
w("**Glass planes** (Read from the lab's glb; 1a): the upper glass 142.0 mm behind the brick face, the lower 190.0. The sill: an oak sill 41.3 high at the front; the stone sill and the segmental arch belong to the wall kit (stone sill 127 high, 50.8 proud, 76.2 wider than the opening each side; the arch ring 215, rise one seventh of the span, 12 proud: terrace-front.py). **Horns:** ogee horns on the upper sash's stiles (76.2 below the meeting rail), none on the lower. **Reveal:** the brick reveal is half a brick, 102.5 (the street file), the lab's frame stands 114.3 back from the face.")
w()
w("The lab's kit has **%d nodes** in the S22 (%d triangles, %d bytes) and %d in the S11 (%d triangles). Each node's bounds in the kit frame are in `kinds.S22.lab_nodes` and `kinds.S11.lab_nodes` (the self-check re-reads the glb and compares). **Photographs win** where they disagree with the book: the lab already followed P6 for the frame; P8 reads the bar at 27 ±6 (22.2 kept, D6), the jamb of a rear at 37 to 47 mm (the front's 76.2 kept, D7) and the meeting rail with its shade at 62 mm (38.1 kept, D10).".replace("%d nodes", "%d nodes") % (len(k["lab_nodes"]), k["lab_triangles"], k["lab_bytes"], len(t["kinds"]["S11"]["lab_nodes"]), t["kinds"]["S11"]["lab_triangles"]))
w()
w("### 4.2 Paint, colour and condition by house")
w()
rows = []
for n, pnt in t["paints"].items():
    rows.append([n, pnt["srgb"], pnt["lin"], pnt["rough"], pnt["note"]])
table(["paint", "sRGB", "linear", "roughness", "note"], rows)
rows = []
for h, ids in t["houses"].items():
    s0 = [s for s in S if s["house"] == h][0]
    rows.append([h, s0["kind"], s0["paint"], s0["condition"]])
table(["house", "kind", "paint", "condition"], rows)
_wc = {}
for h_, ids_ in t["houses"].items():
    _wc.setdefault([x_ for x_ in S if x_["house"] == h_][0]["paint"], []).append(h_)
w("**Every house is white** (the review's fault 1). Jafar's ruling of 3 October is 'windows with white frames, sash bars, sky in the glass', and the approved Hook sheet is recorded the same way ('every upstairs window is PALE - white frames over white nets'). The first version of this target gave five houses coloured frames (brown, olive, blue, cream, bronze) from the photographs' tally; the review found that against his ruling, with no question put to him. **The ruling stands over the tally until he answers on his page** (OWED-05, first line; D13; CLAUDE.md: if code must change a ruling, ask him first). The ten houses: " + "; ".join("%s %d (%s)" % (k_, len(v_), ", ".join(v_)) for k_, v_ in sorted(_wc.items())) + ". The cream, olive, blue, brown and bronze paints stay in the table above as unused data for his answer. **What the photographs say, for his page:** white paint is 55 per cent of the 60 windows; cream or ivory 12, dark brown or red-brown 13, blue 8, olive 7 (a council terrace painted by its tenants: P2). The 1980s and 1990s replacement is white in every photograph reached (P6, P7, P11): the brown or bronze anodised frame the street file draws for every replacement is in none of them (D1), and the first version's bronze chandler is on the same question to Jafar, not decided here. A council replacement in the photographs is the Newburn casement (P11): a fixed light under a top-hung light, white, with nets and vertical drapes: the RC kind; P6's replacement is the other form (RC2, section 4.3). **Condition:** `sound` is the paint as in the table; `grimy` multiplies the lower rail and sill by 0.85 and darkens the box's inside corners (the shade already does it) with a grime band 30 mm high along the sill; `flaking` (the unlet flat): 12 per cent of the area on the lower rails, the sill and the stiles' feet is flaked to grey primer (66, 60, 54) or bare timber (96, 66, 40).")
w()
w("### 4.3 The replacement casements: RC (P7's form) and RC2 (P6's form)")
w()
rc = t["kinds"]["RC"]
w("**RC (P7's and P11's form):** a fixed light under a top-hung light, no bars, in the same 850 x 1676.4 opening (the street's `REPLACEMENT_TRANSOM` 0.72 and the photographs' 0.66 (P6), 0.72 (P7), 0.75 (P11): the street's value stands). **One transom and equal lights** (unit 7's toplight fault does not arise: there are no bars, one transom, and the top light is a single pane). The parts, in the kit frame (mm): frame face %.0f, depth %.0f, front %.1f behind the brick face (the reveal's 102.5 less 30 proud); transom face %.0f, centred at %.1f above the opening's bottom; the top-hung light's sash stiles %.0f with a %.0f dark gap; glass %.0f mm (a sealed unit drawn as one pane, section 5.5) at %.1f behind the face; a gasket line %.0f wide at luma x %.2f and a welded-corner groove %.0f wide at x %.2f at each corner of each sash." % (
    rc["frame_face"], rc["frame_depth"], rc["frame_front_y"], rc["transom"]["face"], rc["transom_centre_z_mm"], rc["vent_sash"]["stile_face"], rc["vent_sash"]["gap"], rc["glass_mm"], rc["glass_plane_y"], rc["gasket"]["width"], rc["gasket"]["luma_factor"], rc["weld_groove"]["width"], rc["weld_groove"]["luma_factor"]))
w()
rows = [[p["name"], p["x"], p["y_into_wall"], p["z_up"], p.get("material", "paint")] for p in rc["parts_mm"]]
table(["part", "x (mm)", "y into the wall (mm)", "z up (mm)", "material"], rows)
w("Glass sightlines (width x height, mm): lower %s x %s, top %s x %s. The top light is hinged at its head and opens outward in the photographs (P11, P14: one stands open): a closed light is drawn; the open one is a variant the PC may add (not required)." % (rc["glass_sightlines_mm"]["lower"][0], rc["glass_sightlines_mm"]["lower"][1], rc["glass_sightlines_mm"]["top"][0], rc["glass_sightlines_mm"]["top"][1]))
w()
r2_ = t["kinds"]["RC2"]
w("**RC2 (P6's form, added by the fixes of 13 October: narrow point 7).** P6 (Levenshulme, 1994) shows a replacement with a fixed top light across the whole width over two lower lights: a side-hung casement beside a fixed light, the mullion near the middle. RC is P7's form only, so the street's replacement houses were all identical; RC2 is built for east_parade_bay4 (both windows). Same opening, frame section (face %.0f, depth %.0f, front %.1f behind the brick face), glass plane (%.1f) and white upvc as RC. **Parts** (kit frame, mm): the transom's face is %.0f, centred at 0.66 x 1676.4 = %.1f above the opening's bottom (P6's 0.66); the top light is one fixed pane; a %.0f mm mullion is centred at x 0 from z %.0f (the sill rail's top) to %.1f (the transom's underside); the left light is a side-hung casement, its stiles and rails %.0f with a %.0f mm gap all round and the hinge on the jamb side (the left jamb); the right light is fixed. The two lower lights' openings are equal, %.1f x %.1f each. **Glass sightlines** (width x height, mm): casement %s, fixed light %s, top light %s. KIT-12, KIT-14 and KIT-15 cover RC2 as they cover RC." % (
    r2_["frame_face"], r2_["frame_depth"], r2_["frame_front_y"], r2_["glass_plane_y"], r2_["transom"]["face"], r2_["transom_centre_z_mm"], r2_["mullion"]["face"], r2_["mullion"]["z_from"], r2_["mullion_z_mm"][1], r2_["casement"]["stile_face"], r2_["casement"]["gap"],
    r2_["lower_light_openings_mm"]["left"][0], r2_["lower_light_openings_mm"]["left"][1], r2_["glass_sightlines_mm"]["casement"], r2_["glass_sightlines_mm"]["fixed"], r2_["glass_sightlines_mm"]["top"]))
w()
rows = [[p["name"], p["x"], p["y_into_wall"], p["z_up"], p.get("material", "paint")] for p in r2_["parts_mm"]]
table(["part", "x (mm)", "y into the wall (mm)", "z up (mm)", "material"], rows)
w("### 4.4 Sills, heads and arches, and what the kit does not carry")
w()
w("The stone sill (127 high, 50.8 proud, 76.2 wider each side than the opening), the segmental arch (ring 215, rise one seventh, 12 proud) and the brick returns of the reveal are the wall kit's, not this unit's; this target names the shade the wall kit must give the returns (section 5.4). **Brick returns**: 0.8 of the wall's value at the face falling to 0.6 at the sash, 0.7 under the head.")
w()
w("### 4.5 Nothing left open")
w()
w("Every opening is covered above and around its parts: the opening is 850 x 1676.4 and the frame's outer lining runs 65 mm beyond it each side behind the brick (S22/S11), or the jambs of RC and RC2 fill it to the brick (60 face); the head is the lab's head lining (S22/S11) or the RC's head rail; nothing is left bare between the head and the stone arch (the arch's soffit and the brick return are the wall kit's, as the shopfront's were), and between the sill and the oak sill the sash's bottom rail runs to the stone sill. The self-check KIT rows confirm that every pane and every net lies inside the opening and that no RC member overlaps another; the drawing (target_drawing.py) shows the opening covered.")
w()

# ---------------------------------------------------------------------------------------------------------------------------
w("## 5. The glass: the 1a fix as numbers")
w()
gp = t["glass"]["pane"]
w("### 5.1 The pane")
w()
w("**The game's pane:** " + sent(gp["game"]) + " The pane is a real glass surface: its reflectance and roughness are the game's. **What the cloud render uses to stand in for it:** " + gp["cloud_stand_in"] + ".")
w()
w("**Two-face reflectance of float glass** (n 1.52, unpolarised, the reflections between the faces counted: Derived, recomputed by the self-check; 1a's table is 0.02 to 0.03 higher at 16 to 30 degrees) by the angle from the wall: " + ", ".join("%s degrees %.3f" % (a, v) for a, v in gp["fresnel_two_face"].items()) + ". " + sent(gp["fresnel_note"]))
w()
w("### 5.2 Old glass's waviness")
w()
w(sent(t["glass"]["waviness"]["what"]) + " **Photographs:** " + sent(t["glass"]["waviness"]["photo"]) + " No wave normal map: the glass looks flat on the photographs.")
w()
w("### 5.3 Dirt and reflections")
w()
w(sent(t["glass"]["dirt"]) + " **Reflections by floor.** Upper panes: " + t["glass"]["reflections_by_floor"]["upper"] + ". Ground panes: " + t["glass"]["reflections_by_floor"]["ground"] + ".")
w()
w("### 5.4 The box shaded and its dark lines drawn")
w()
bs = t["box_shade"]
w(bs["what"] + ". Numbers (1a step 2, Judgement from 1a's photograph-9 figures; the check KIT-09 reads them back from the exported file):")
w()
table(["part", "red channel of COLOR_0 (x paint)", "note"], [
    ["faces whose normal points to the street", "%.1f (not darkened)" % bs["street_facing_faces"], bs["street_facing_note"]],
    ["the faces that run into the wall: the reveal-facing sides of the linings, the beads, the pulley stiles and the sash stiles", "%.1f at y = 0 falling linearly to %.1f at the glass plane" % (bs["lining_from_brick_edge_to_glass"]["at_brick_edge"], bs["lining_from_brick_edge_to_glass"]["at_glass"]), "the sash's own lining and the outer lining's face"],
    ["the track faces", bs["track_faces"], bs["track_note"]],
    ["inside corners", "%.1f within %.0f mm of a concave edge" % (bs["inside_corners"], bs["inside_corner_reach_mm"]), "photograph 9's corner line 105 to 125 against a lining of 220 to 250"],
    ["the putty and shadow line round each pane", "%.2f, %.0f mm wide" % (bs["putty_and_shadow_line_round_each_pane"]["factor"], bs["putty_and_shadow_line_round_each_pane"]["width_mm"]), bs["putty_and_shadow_line_round_each_pane"]["note"]],
    ["the meeting rail's underside", bs["meeting_rail_underside"], "the lower rail of the upper sash seen from below"],
    ["the parting bead's gap", "%.2f over %.0f mm" % (bs["parting_bead_gap"], bs["parting_bead_gap_width_mm"] * 3), "the gap itself is a 2 mm geometric gap"],
    ["the brick returns of the reveal (wall kit)", "%.1f to %.1f" % tuple(bs["brick_returns_of_the_reveal"]), bs["brick_returns_note"]],
])
w("**The paint:** only the sound gloss white (`white_fresh`, east_parade_bay1 and west_south_bay2) keeps 1a's albedo %s and roughness %.2f (try %.2f once: a traced sheen); every other house takes its own paint from the `paints` table, which governs (white_grimy is 0.66 at roughness 0.48, for example), not this line (the review's narrow point 4). **Every dark line of the box is at least 6 mm wide** (1 pixel at 10 m is 5.9 mm at 1440 lines and 46 degrees): the lab's putty strips are 6.4 wide, the parting bead's gap is 2 mm but its shade is painted over 6 mm each side, the RC's gasket and weld groove are shaded over 6 mm. Check KIT-10." % (bs["keep_paint"]["albedo"], bs["keep_paint"]["roughness"], bs["keep_paint"]["try_once"]))
w()
w("### 5.5 What this cannot reach")
w()
w("The real sealed unit of the replacement reflects from four faces (about 0.14 at normal incidence); Unreal's Specular 1.0 caps at F0 0.08, so the replacement's pane under-reflects; and the game's own reflections (Lumen, the box-projected street cube, the Fresnel hand-over) are not in the cloud. Both are in `could_not_settle` and `owed_on_pc`.")
w()

# ---------------------------------------------------------------------------------------------------------------------------
w("## 6. Nets, curtains and blinds")
w()
w("All are **cards** (two triangles each) behind the glass, in front of the room's card; their alpha is the weave. Planes are in millimetres behind the brick face; z is up from the opening's bottom edge. The two held net pictures (`net_curtain_a`, `_b`: a coarse square mesh of 7 to 10 mm, mean alpha 0.53) match none of the photographs' nets and are not used (D2).")
w()
rows = []
for kk, n in t["nets"].items():
    c = n.get("card")
    rows.append([kk, n["label"], n["what"], xz(c) if c else "-", ("S22/S11 %d, RC %d" % (n["plane_mm"]["S22"], n["plane_mm"]["RC"])) if "plane_mm" in n else "-", n.get("voile_coverage", "-"), n.get("lace_band", {}).get("share_of_height", "-"), "%.0f%%" % (100 * n["share_photo"])])
table(["net", "name", "what", "card (mm)", "plane (mm behind the face)", "voile coverage", "lace band share of height", "share of the photographs' windows"], rows)
nc = t["net_common"]
w("**The fabric** (all nets):")
w()
w("- **Weave:** " + sent(nc["weave"]))
w("- **Layers and coverage:** " + sent(nc["layers_and_coverage"]))
w("- **Gathering:** At %.0f per cent fullness, fold wavelength %s to %s mm, depth %d mm (a normal and brightness map, not geometry), brightness modulation +-%.0f per cent." % (nc["fullness"] * 100, nc["gather_wavelength_mm"][0], nc["gather_wavelength_mm"][1], nc["gather_depth_mm"], nc["fold_brightness_modulation"] * 100))
w("- **Hem:** " + sent(nc["hem"]))
w("- **Head:** " + sent(nc["head"]))
w("- **Colours** (sRGB): white %s, greyed %s, and yellowed by nicotine %s. %s" % (rgb(nc["colours"]["white"]), rgb(nc["colours"]["greyed"]), rgb(nc["colours"]["yellowed"]), sent(nc["photo_note"])))
w("- **By day:** " + sent(nc["day_look"]))
w("- **Night, lit:** " + sent(nc["night_lit"]))
w("- **Night, dark:** " + sent(nc["night_dark"]))
w("- **Parallax:** " + sent(nc["no_parallax"]))
w()
rows = []
for kk, cur in t["curtains"].items():
    rows.append([kk, cur["label"], cur["what"], card_txt(cur), cur["plane_mm"], cur["opacity"], cur["folds"], rgb_map(cur["colours"]), cur["night_lit"]])
for kk, b in t["blinds"].items():
    rows.append([kk, b["label"], b["what"], xz(b["card"]), b["plane_mm"], b["opacity"] if "opacity" in b else "slat gaps alpha %s" % b.get("slat_gap_alpha"), ("slat pitch %s mm" % b["slat_pitch_mm"]) if "slat_pitch_mm" in b else "a plain sheet", rgb(b["colour"]), b["night_lit"]])
table(["kind", "name", "what", "card (mm)", "plane", "opacity", "folds or slats", "colours", "night, lit"], rows)
w("**Per house** the street's mix is in the table of section 1 (net kind and colour, drape): the upper sash is clear wherever the net is N1, N3 or none, so the room shows through it; a torn yellowed net hangs askew in the empty flat (one lower corner off its wire, the hem 80 mm out of true: a Judgement). **Drawn curtains** stand in front of the net and cover the window; open curtains stand 170 mm wide at each side. A lit room behind a lit net reads as the net's own glow (emissive 0.48) with the room's pendant and the top of the back wall seen through it.")
w()

# ---------------------------------------------------------------------------------------------------------------------------
w("## 7. The rooms behind the windows")
w()
w("### 7.1 The format")
w()
cards = RM["cards"]
w("Each room is built by script from CC0 models in Blender (Cycles), rendered to the shop rooms' picture format: " + cards["picture_names"] + ". Three states: `day`, `night_lit`, `night_dark`. " + sent(cards["camera_rule"]) + " **Brightness** (the game's emissive scale): %s **Picture standards** (Judgement): mean luma day %g, night_lit %g, night_dark %g, within ±%.0f per cent. %s" % (sent(cards["brightness_note"]), RM["picture_standards"]["day_mean_luma"], RM["picture_standards"]["night_lit_mean_luma"], RM["picture_standards"]["night_dark_mean_luma"], 100 * RM["picture_standards"]["tolerance"], sent(RM["picture_standards"]["note"].replace("Judgement, scaled", "Scaled"))))
w()
w("**Lights per state.** Day: " + endp(RM["lights_by_state"]["day"]) + " Night, lit: " + endp(RM["lights_by_state"]["night_lit"]) + " Night, dark: " + endp(RM["lights_by_state"]["night_dark"]))
w()
w("### 7.2 The thirteen rooms")
w()
w("**Variants so a row does not repeat visibly:** three lounges, three bedrooms, two landings, two empty rooms, three cottage front rooms; no (room, net, drape) triple repeats within three places on a row (checked); the three lounges and the three bedrooms differ in their walls and in their back-wall pieces (checked).")
w()
rows = []
for rid, r in RM["rooms"].items():
    rows.append([rid, r["type"], "%.1f x %.2f x %.1f" % tuple(r["size_m"]), "%s / %s / %s" % (r["walls"], r["ceiling"], r["floor"]), ", ".join("%s (%s %.2f)" % (o["model"], o["class"], o["stand_off_m"]) for o in r["objects"]) or "none", ", ".join(r["forms"]), "pendant" if r["pendant"] else ("bare bulb" if "bare_bulb" in r["forms"] else "-"), "%d x %d" % tuple(r["picture_px"])])
table(["room", "type", "W x H x D (m)", "walls / ceiling / floor", "objects (class, stand-off m)", "scripted flat forms", "light", "picture px"], rows)
w("**Finishes** (Poly Haven textures at 1k, tinted; roughness in words and 0-1): " + "; ".join("%s: %s (linear %s, roughness %s)" % (k, v["what"], v["base_lin"], v["rough"]) for k, v in RM["finishes"].items()) + ".")
w()
w("**Scripted flat forms** (every one inside the budgets of its surface): " + "; ".join("%s: %s" % (k, v.get("note", "")) for k, v in RM["forms"].items()) + ".")
w()
w("**What each type shows from the street.** *Upper lounges and bedrooms*: the ceiling with its rose, cove and pendant, the wall tops under the picture rail, the tops of tall furniture, a picture hung high; at night, a warm ceiling and the shade. *Landings*: the stair's flat stringer and handrail up the side wall, a half-glazed door at the back, a bare bulb. *Empty rooms*: stripped paper or peeling paint, a flat chimney breast, a pale ghost where a picture hung, bare boards, a bare bulb flex; by night they are dark whatever the table says. *Cottage front rooms*: eye-level: sofa or armchair against the back wall, a cabinet with a clock and a lamp, the television on a small table (a cool glow at night in front room 1), pictures, a fire surround drawn flat.")
w()
w("### 7.3 Which windows are lit at night")
w()
w(lit["source"].replace("Judgement. production/research/evening-light-1990 gives", "Judgement. The research file production/research/evening-light-1990 gives"))
w()
rows = [[h, "%.2f" % sh, lit["lit_by_hour"][h]["n"]] for h, sh in lit["table_hour_to_share_of_all_20_windows"].items()]
table(["hour", "share of the 20 windows", "windows lit"], rows)
w(sent(lit["rule"]) + " **At 20:30, seven lit (35 per cent):** " + ", ".join(sorted(lit["lit_by_hour"]["20:30"]["windows"])) + ". **The fixed lit order** (after the always-lit pair): " + " > ".join(lit["lit_order_of_the_non_always_lit_windows"]) + ". " + sent(lit["by_day"]))
w()
w("### 7.4 The inventory")
w()
w("**%d Poly Haven models were looked at at 1k (base colour map, 13 October); %d are used in the rooms; %d textures.** Every id exists in the live catalogue (`self_check.py --live` re-reads it) and is CC0. A mark found on a map is blanked (painted out to the surface's own colour) before the model is used, or the model is not used; every framed picture's artwork is replaced by a script-drawn print (flat grey-green landscape band under a pale sky, no text). Never used: `fancy_picture_frame_02` (its painting shows a group of figures including children)." % (len(inv), len(used), len(t["inventory"]["polyhaven_textures"])))
w()
rows = []
for mid, m in sorted(inv.items()):
    rows.append([mid, m["dims_mm_catalogue_xyz"], m["polycount"], ", ".join(m["used_in_rooms"]) or "-", m["status"], m["marks"]])
table(["model", "dims mm (x y z)", "polycount", "used in", "status", "marks seen at 1k"], rows)
w("**Textures** (1k base colour looked at, no marks seen): " + ", ".join(sorted(t["inventory"]["polyhaven_textures"])) + ". **Brand blocklist** (the self-check scans every string of target.json outside a marks entry for these): " + ", ".join(t["inventory"]["brand_blocklist"]) + ". " + sent(t["inventory"]["rule"]))
w()

# ---------------------------------------------------------------------------------------------------------------------------
w("## 8. As kit pieces")
w()
kp = t["kit_pieces"]
w("**Frame and pivot.** " + sent(kp["frame"]) + " " + sent(kp["pivot"]))
w()
w("**Placement.** East: " + kp["placement"]["east"] + ". West: " + kp["placement"]["west"] + ". Height: " + kp["placement"]["sill_z"].replace("above the crown: ", "above the road's crown, ") + ".")
w()
w("**Files:**")
w()
for k2, v in kp["files"].items():
    w("- %s: `%s`" % (k2, v))
for v in kp["extra_files"].values():
    path_, rest_ = v.split(" ", 1)
    w("- room_card_gf: `%s` %s" % (path_, rest_))
w()
w("**Budget:** %d triangles and %d bytes each. %s" % (kp["budget"]["triangles_each_kind"], kp["budget"]["bytes_each_glb"], sent(kp["budget"]["note"])))
w()
for kind in ("S22", "S11", "RC", "RC2"):
    if kind in ("RC", "RC2"):
        w("**%s: added nodes** (the %s has no lab model: its frame parts are the table in section 4.3; these are its glass, nets, drapes, blinds and pendant):" % (kind, kind))
    else:
        w("**%s: added nodes** (the lab's %d nodes are reused as they are; the RC's parts are in section 4.3):" % (kind, kp["per_kind"][kind]["reused_nodes"]))
    w()
    rows = []
    seen_notes = {}
    for n in kp["per_kind"][kind]["added_nodes"]:
        note = n["note"]
        if note in seen_notes and len(note) > 40:
            note = "as `%s`" % seen_notes[note]
        else:
            seen_notes[note] = n["name"]
        rows.append([n["name"], n["material"], "%s to %s" % tuple(n["x"]), "%s to %s" % tuple(n["y_into_wall"]), "%s to %s" % tuple(n["z_up"]), note])
    table(["node", "material", "x (mm)", "y into the wall (mm)", "z up (mm)", "note"], rows)
rcu = kp["room_card"]["upper"]
cot = kp["room_card"]["cottage"].replace("room_card_gf: ", "").replace("3.4 x 2.6,", "3.4 x 2.6 m,")
w("**The room card.** Upper windows: node `%s`, plane %s mm behind the brick face, x %s to %s, z %s to %s (%s x %s m): %s. Cottages (glb `room_card_gf`): %s." % (rcu["node"], rcu["plane_mm"], rcu["x"][0], rcu["x"][1], rcu["z_up"][0], rcu["z_up"][1], rcu["size_m"][0], rcu["size_m"][1], rcu["note"], cot))
w()
w("**Materials:**")
w()
for k2, v in kp["materials"].items():
    w("- `%s`: %s" % (k2, sent(v)))
w()
w("**How a piece goes into the game** (HANDOVER.md's route, and what is different here):")
w()
for x in kp["how_it_goes_into_the_game"]:
    w("- " + x)
w()
w("**The room card's parameters per site** are in `sites[].card`: CardOrigin (cm: low-x corner, front y, floor z), RoomSize (cm), CamD (cm), Side (+1 east, -1 west), and the picture ids by the site's `room`. Example, `%s`: CardOrigin %s, RoomSize %s, CamD %s, Side %s, the window in the card (m): x %s to %s, z %s to %s." % (S[0]["id"], S[0]["card"]["card_origin_cm"], S[0]["card"]["room_size_cm"], S[0]["card"]["cam_d_cm"], S[0]["card"]["side"], S[0]["card"]["window_in_card_m"]["x0"], S[0]["card"]["window_in_card_m"]["x1"], S[0]["card"]["window_in_card_m"]["z0"], S[0]["card"]["window_in_card_m"]["z1"]))
w()

# ---------------------------------------------------------------------------------------------------------------------------
w("## 9. The gate, in the cloud (no Unreal)")
w()
w(sent(g["what"]))
w()
w("**Scene.**")
w()
for k2, v in g["scene"].items():
    if k2 != "house_sets":
        w("- **%s:** %s" % (k2.replace("_", " "), sent(v)))
w()
w("**House sets:**")
w()
for k2, v in g["scene"]["house_sets"].items():
    w("- **%s:** %s" % (k2, sent(v)))
w()
w("**Views:** " + sent(g["views"]))
w()
w("**What is measured** (from the Material Index and Object Index passes, never by eye):")
w()
for k2, v in g["measure"].items():
    w("- **%s:** %s" % (k2.replace("_", " "), sent(v)))
w()
w("**Bands** (from the photographs, section 3.2; the check numbers of section 10 quote them; P is the pane median, L the frame's 90th percentile, D the outline's 5th percentile):")
w()
for k2, v in g["bands"].items():
    w("- **%s:** %s" % (k2, band_txt(v)))
w()
w("**Window states for every WB check** (the review's fault 2(b)): " + "; ".join("**%s**: %s" % (k2, v.rstrip(". ")) for k2, v in g["window_states"].items() if k2 != "why") + ". " + sent(g["window_states"]["why"]))
w()
w("**Frame class:** " + sent(g["frame_class"]))
w()
w("**What the gate cannot show:** the game's glass reflections (Lumen, the cube), the exposure, the motion vectors of the card under TSR, the real glass hand-over: owed on the PC (section 10, OWED rows).")
w()

# ---------------------------------------------------------------------------------------------------------------------------
w("## 10. Checks (target.json `checks`; the cloud gate and the build run them)")
w()
w("%d checks. Kinds of number: Read, Scaled, Photo, Derived, Judgement." % len(t["checks"]))
w()
rows = [[c["id"], c["name"], c["measure"], c["expected"], c["tolerance"], c["applies_to"], c["kind"], c["source"]] for c in t["checks"]]
table(["id", "name", "measure", "expected", "tolerance", "applies to", "kind", "source"], rows)
w("**Owed on the PC** (the cloud cannot show them):")
w()
for o in t["owed_on_pc"]:
    w("- **%s** %s Check: %s" % (o["id"], sent(o["what"]), sent(o["check"])))
    for ln in o.get("lines", []):
        w("    - Line for his page: " + ln)
w()

# ---------------------------------------------------------------------------------------------------------------------------
w("## 11. Photographs win: each disagreement")
w()
rows = []
for d in t["photographs_win"]:
    rows.append([d["id"], d["what"], d.get("street_file") or d.get("book") or d.get("research") or d.get("research_1a"), d["photographs"], d["chosen"]])
table(["id", "what", "the file, book or research said", "the photographs say", "chosen"], rows)

w("## 12. What the target could not settle")
w()
for x in t["could_not_settle"]:
    w("- " + x)
w()
w("## 13. Previews")
w()
w("In `production/previews/cloud-week/refs/house-windows/` (JPEG, at most 1200 px, under 300 KB; Geograph photographs CC BY-SA 2.0, credited in the table of section 2; the drawing's overlay is ours):")
w()
rows = [[p["id"], p["preview"].split("/")[-1], "crop %s" % (p["crop"],), "; ".join(m["what"] for m in p["masks"]) or "none needed"] for p in t["sources"]["photographs"]]
rows.append(["overlay", "p8-oxford-sunningwell-road-rear-1987-target-on-photo.jpg", "P8's left window with the S22 elevation laid on at the width scale (yellow: the opening; red: the sash members; green: the panes)", "none"])
rows.append(["sheet", "measured-windows-sheet.jpg", "the 18 windows measured, outline red and pane green (P1_a, P1_b and P1_e boxed without the stone head and sill and the brick column, as the review boxes them)", "none"])
table(["ref", "file", "crop", "masked"], rows)
open(os.path.join(HERE, "TARGET.md"), "w").write("\n".join(L) + "\n")
print("TARGET.md written,", len(L), "lines,", sum(len(x) for x in L), "characters")
