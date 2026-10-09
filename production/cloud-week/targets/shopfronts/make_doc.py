#!/usr/bin/env python
"""Writes TARGET.md from target.json (tables and numbers) and the prose below. Run after make_target.py
and self_check.py:   /home/user/.bpyenv/bin/python make_doc.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, "target.json")))
P = T["parts"]
PH = T["photo"]
DM = PH["derived_mm"]
RT = PH["ratios"]
SC = PH["scale"]
SELF = T.get("self_check") or {}
out = []


def w(s=""):
    out.append(s)


def table(head, rows):
    w("| " + " | ".join(head) + " |")
    w("|" + "|".join("---" for _ in head) + "|")
    for r in rows:
        w("| " + " | ".join(str(c).replace("|", "/") for c in r) + " |")
    w()


def pl(pr, maxn=34):
    pts = pr["points"]
    if len(pts) > maxn:
        return "%d points, see target.json" % len(pts)
    return " ".join("(%s, %s)" % (("%g" % a), ("%g" % b)) for a, b in pts)


def prof_list(part, names):
    pr = P[part]["profiles"] if part != "stallriser" else None
    rows = []
    for key in names:
        node = pr[key]
        rows.append(["`%s`" % key, node["plane"], pl(node), node.get("note", "")])
    table(["profile", "plane", "points (mm)", "note"], rows)


# ------------------------------------------------------------------------------------------------
w(T["summary_line"])
w()
w("# Shopfronts of Quay Street, as a kit of parts: the exact target")
w()
w("Cloud week 42, 9 October 2026, FIRST TRY by a fresh target writer for unit 3.2 (the parts) and the builder (the assembly). Not reviewed. Nothing is committed. Everything in this file is in `target.json`; the checks that follow from it are in its `checks` list and its `self_check`.")
w()
w("## 0. Files, and how to read them")
w()
w("Files in `production/cloud-week/targets/shopfronts/`:")
w()
table(["file", "what it is"], [
    ["`TARGET.md`", "this page (written by `make_doc.py` from `target.json` and its own prose)"],
    ["`target.json`", "every part with dimensions, profiles as point lists, positions, variants, materials; the paints; the ten fronts' assembly table; the alterations; %d `checks`; the self-check result" % len(T["checks"])],
    ["`target_drawing.py`", "draws target.json ALONE: each part's elevation and sections, an elevation of Rita's whole bay and of the ten, at 1 mm to the pixel, into a folder given on the command line, with the polygons as JSON, and the drawing laid on the photograph's previews"],
    ["`self_check.py`", "tests the target against its own sources and the photograph's saved previews; writes `self_check` into target.json"],
    ["`measure_leadenhall.py`", "author tool: re-projects the photograph to a level elevation, measures it (43 rows and columns and one notice), writes `photo_measurements.json` and the previews"],
    ["`make_target.py`, `tgt_parts.py`, `tgt_shops.py`, `tgt_text.py`, `tgt_profiles.py`", "author tools: build target.json from the parts, shops and prose"],
    ["`make_previews.py`, `make_doc.py`", "author tools: the previews; this page"],
])
w("Run with `/home/user/.bpyenv/bin/python`: `target_drawing.py OUT_DIR [--json drawing.json] [--all-fronts] [--photos PREVIEW_DIR --overlay-out DIR]`, `self_check.py`. Previews: `production/previews/cloud-week/refs/shopfronts/` (section 15).")
w()
w("**Units and axes.** Millimetres; sRGB 0 to 255, aged to 1990; roughness 0 to 1; metal 0 to 1. The frame is the GAME's viewer frame, as the fascia target uses it: **u** across the bay from the viewer's left party-wall line (0) to the right one (6000); **d** out from the wall face toward the street (the kit's y is -d); **z** up from the footway. On the east parade low street x is on the viewer's right, so a front's door end is read off the viewer's side (`shops[].door_end_viewer`), with the street's word (`door_end_street`) and the recipe's `doors_on` word beside it; street x = bay high end - u/1000 on the east parade and bay low end + u/1000 on the west block. Section planes: `d-z` a side section, `u-d` a plan, `a-p` a small moulding, `u-z` an elevation; closed outlines are counter-clockwise.")
w()
w("**Kinds of number.** Read: printed in a source file. Scaled: measured off a drawing or the project's own files. **Photo: measured on a photograph today** (method and error stated). Derived: worked from others. Judgement: nothing else fits; a better source overturns it. A number with no kind is a Read from the street's own files.")
w()
w("## 1. What the target does, in one table")
w()
table(["part", "what the target gives", "main change from the kit, and why"], [
    ["pilaster (4 variants)", "plinth 800, shaft 290 x 110 proud, necking, capital 310, 350 x 130 at the top; panelled, fluted, rendered on a stepped plinth, flush clad", "plinth 600 to 800 (Photo: the plinth stands 1.27 x the sill)"],
    ["console (scroll, block, absent)", "240 x 180 x 550 on the capital; the S silhouette smoothed; a volute on each face and an acanthus leaf", "the volute and leaf are Judgement; no photograph of a scrolled console was reached"],
    ["fascia board", "5410 x 550, 120 proud, a 40 bed mould; vertical", "the bed mould"],
    ["cornice", "215 x 150 x 5892, 19-point profile with a tall corona", "profile only: the fixed envelope stays (the photograph's crown is 3 x taller and is NOT followed)"],
    ["sill, stallriser (%d variants)" % len(P["stallriser"]["variants"]), "sill 75 thick, nose 150; panelled, brick tile, square tile, patterned tile, glass slab, render, boarded, grille", "sill 50 to 75; more stallriser kinds for the ten fronts"],
    ["window frame (T1, T2, M1, M2)", "mullions 70 / 80 / 50 / 28 wide, transom 80, toplights, glass at d 30", "mullion 55 to 70 (the photograph reads 164: partly followed)"],
    ["shop door (T1, M1, M2)", "900 x 2040 in 1006, **glazed from 700**, brass foot strip", "glazed from 1000 to 700 (Photo and the books agree against the scene)"],
    ["side door slot", "944 slot for the front-door family's F1 (not re-targeted): the mapping into the bay", "none"],
    ["lobby", "recessed 600 (grocer) and 300 (launderette), tiled or terrazzo floors", "new"],
    ["ten fronts", "an assembly table: trade, bay, original or altered, stallriser, door end, lobby or flush, glazing pattern, paints", "new"],
])

# ------------------------------------------------------------------------------------------------
w("## 2. Sources")
w()
w("Only sources actually reached today are used. Search summaries are not used as numbers. Photographs are for measuring only: never placed in the game, never traced into a texture, never fed to an image model. No NoAI source.")
w()
rows = []
for s in T["sources"]:
    rows.append([s["id"], s["what"], s.get("url", "-"), s["read"], s["author"], s["licence"], s.get("taken", "-"), s["shows"], s["used"]])
table(["id", "what", "URL", "read", "author", "licence", "taken", "shows", "used"], rows)
w("**P1's date and kind.** " + T["sources"][0]["period"])
w()
w("**P1's scale.** " + T["sources"][0]["scale"] + ".")
w()
w("**Unreached (403, no route or not tried): nothing from them is used.**")
w()
for u in T["unreached"]:
    w("- " + u)
w()
w("**What I would read once the network opens:**")
w()
for u in T["would_read_when_network_opens"]:
    w("- " + u)
w()

# ------------------------------------------------------------------------------------------------
w("## 3. What was measured on the photograph today, and how far it holds")
w()
w("P1 is re-projected to a level rectilinear elevation of the arcade's right-hand wall (yaw 90, focal 2400 px); a plane parallel to the wall is then at one scale. `measure_leadenhall.py` snaps each edge to the strongest luminance gradient near where it was looked for, averaged along a span chosen to avoid ornament; `self_check.py` re-measures every row and column that can be on the SAVED previews. Scale: fitted on ONE dimension, an A5 notice (148 x 210 mm) on the shop door's glass, %.2f x %.2f px, giving %.4f mm a pixel in the door's plane; the door's plane is %.3f times farther than the pilasters' front (the foot rows 604.1 and 547.0), so the pilaster plane is **%.4f mm a pixel** (the camera about %d mm above the footway); error %d per cent, which is the A5 assumption, the plane ratio and the notice's edges. Ratios carry none of it." % (
    SC["notice_px"][0], SC["notice_px"][1], SC["mm_per_px_door_plane"], 1.0 / (1.0 / SC["door_plane_over_pilaster_plane"]), SC["mm_per_px_pilaster_plane"], SC["camera_height_mm_above_footway"], SC["error_pct"]))
w()
table(["what", "measured (P1, mm at the stated plane; kind Photo, +-8 per cent unless stated)", "the street's number", "reading"], [
    ["shaft width", "%.0f" % DM["shaft_width"], "290 (kit)", "the kit's 290 stands: no disagreement"],
    ["shaft projection (from the right return: 30.8 px at 1087 px off axis)", "%.0f (+-14 per cent)" % DM["shaft_proud"], "scene 100; target 110", "D3: 110 is inside both"],
    ["plinth: block tops z", "%.0f / %.0f / %.0f; cap slab top %.0f" % (DM["plinth_block1_top_z"], DM["plinth_block2_top_z"], DM["plinth_block3_top_z"], DM["plinth_top_z"]), "kit 600; target 800", "ratios R1, R2: plinth top is 1.27 x the sill's top and 0.228 of the front's height; at 3.55 m that is 811"],
    ["capital height (neck ledge to abacus top)", "%.0f (1.04 x the shaft's width)" % DM["capital_height"], "kit 330; target 310", "D4"],
    ["fascia field (between the gilt keylines)", "%.0f" % DM["fascia_field_height"], "550", "no disagreement: the street's 550 is the same order"],
    ["crown (fillet to cap, on the continuous run)", "%.0f (%.2f of the field)" % (RT["crown_height_mm_wall_plane"], RT["crown_over_field"]), "150 (0.27 of the fascia)", "D7: NOT followed (the fascia target fixes the cornice top at 3550)"],
    ["sill top (wall plane)", "%.0f (%.2f of the front's height; 0.64 m at 3.55)" % (DM["sill_top_z_wall_plane"], RT["sill_top_over_front_height"]), "600", "no disagreement (6 per cent)"],
    ["window stile / mullion face (wall plane)", "%.0f / %.0f (the mullion %.2f of its 1.0 m light)" % (DM["window_stile_face"], DM["mullion_face"], RT["mullion_over_light"]), "kit 50 / 55; target 70 / 80", "D5: partly followed"],
    ["transom bar face", "%.0f" % DM["transom_bar_face"], "80 (the street's transom is a high toplight transom)", "not comparable: P1's bar is a mid glazing bar"],
    ["stallriser panel (a framed cast grille)", "%.0f high" % DM["stallriser_panel_height"], "525 (panel zone)", "the same order"],
    ["shop door (door plane)", "leaf %.0f high; glazed from %.3f to %.3f of it" % (DM["door_leaf_height_door_plane"], DM["door_glazed_from_fraction"], DM["door_glazed_to_fraction"]), "2040; scene glazed from 1000 (0.49)", "D2: 700 (0.343); the books say two-thirds glazed"],
    ["door foot strip", "%.0f high" % DM["door_foot_strip_height"], "-", "added: 30 high brass strip"],
])
w("**Why P1 still holds for a 1900-1935 provincial parade, and where it does not.**")
w()
w("- It holds for the **order and proportion of the members** that every period front shares: a plinth taller than the stallriser, a shaft about 8 to 9 widths high, a necking and a capital about one shaft-width high, a fascia field of about half a metre, a sill group much deeper than a bead, a stallriser panel in a frame, a shop door two-thirds glazed. Each ratio is compared with the street's own fixed numbers in the rules of section 14 (R1 to R8): the seven the target follows agree within 12 per cent and the eighth (the crown) is the stated departure D7, which is the best argument that the street's numbers (the scene's) are of the right kind.")
w("- It does **not** hold for: absolute sizes of a heavy arcade's joinery (its mullion is 0.16 of its light, the street's 0.06); a stone- or cement-faced pier's finish (it has sharp arrises and no panel); the crown's height (three times the street's); anything with a scroll, a leaf, a roller shutter, a box sign, aluminium or a lobby, because P1 shows none; and anything about 1990 (it is a 2019 restoration in fresh gloss).")
w("- Where a P1 proportion and the street's fixed number disagree beyond the error, section 14 says which won and why.")
w()
w("**Which parts rest on what** (the brief asks plainly):")
w()
rows = []
for k, e in T["evidence_basis"].items():
    rows.append([k, "; ".join(e["photo_today"]) or "nothing", "; ".join(e["earlier_notes"]) or "-", "; ".join(e["judgement"]) or "-"])
table(["part", "photographs measured today (P1, P2)", "the earlier notes (cited, not re-read)", "judgement"], rows)
w("**Edges measured on P1 and laid on it.** The drawing's projected edges (the instance polygons) fall on the saved previews within 4 px (8 px for the weakest edges); %s edges were tested and the worst is %s px. These edges were measured on the same crops that the previews are made from, so this test shows that the polygons are built from the measurements correctly, that JPEG compression does not move them, and that the snap is reproducible: it is NOT an independent validation of the numbers (that is what the ratio rules and the street's fixed numbers are for). The previews are crops of the joinery only, with the house numerals and one logo fragment masked; no whole frame and no lettering is in any preview." % (SELF.get("stats", {}).get("overlay_edges", "?"), SELF.get("stats", {}).get("overlay_worst_px", "?")))
w()

# ------------------------------------------------------------------------------------------------
B = T["bay"]
w("## 4. The bay: datum, zones, planes")
w()
table(["item", "value (mm)", "kind", "source"], [
    ["bay width, party line to party line", B["width"], "Read", "scene bay_width_m 6.0"],
    ["pilaster slot at each party wall", B["pilaster_slot"], "Read", "scene pilaster_width_m 0.35"],
    ["opening zone between the piers", B["opening_zone"], "Derived", "6000 - 2 x 350"],
    ["side-door slot (F1 + 24.4 filler each side)", B["side_door_slot"], "Read", "kit README (944); F1 opening 895.2 + 2 x 24.4"],
    ["shop-door slot", B["shop_door_slot"], "Read", "kit README (900 leaf + 2 x 3 gap + 2 x 50 jamb)"],
    ["window, with a side door / without", "%g / %g" % (B["window_default"], B["window_no_side_door"]), "Derived", "5300 - 944 - 1006; 5300 - 1006"],
    ["sill top / sill underside", "600 / 525", "Read / Judgement", "scene stallriser 0.60; the sill is 75 thick (D8)"],
    ["transom / head / fascia / cornice (z)", "2400-2480 / 2790-2850 / 2850-3400 / 3400-3550", "Read", "scene; fascia target; fascia-01"],
    ["d: shaft front / plinth front / capital top front", "110 / 150 / 130", "Photo (110) / Read / Read", "D3; kit"],
    ["d: fascia face / console front / cornice nose", "120 / 180 / 215", "Read", "fascia target; fascia-01"],
    ["d: sill nose / stallriser face / frame fronts / mullion front / glass", "150 / 125 / 95 and 100 / 92 / 30", "Read / Read / Judgement / Judgement / Read", "kit; the mullion front is 62 in front of the glass (D5)"],
])
w("The zones fill the opening: **door end on the viewer's LEFT**: side door [350, 1294], shop door [1294, 2300], window [2300, 5650]; **RIGHT**: window [350, 3700], shop door [3700, 4706], side door [4706, 5650]; with no side door (the grocer) the shop door takes the outer 1006 and the window the other 4294. The side door is the outermost zone, next to the pier, as the street's frames show. Self-check group 5 recomputes all ten fronts' zones.")
w()

# ------------------------------------------------------------------------------------------------
w("## 5. Pilaster")
w()
d = P["pilaster"]["dims"]
w("**The kit gets right:** " + "; ".join(T["kit_vs_target"]["pilaster"]["kit_gets_right"]) + ".")
w()
w("**The target changes:**")
w()
table(["change", "reason", "kind"], [[c["what"], c["reason"], c["kind"]] for c in T["kit_vs_target"]["pilaster"]["target_changes"]])
table(["item", "value", "kind", "source"], [
    ["slot / height / plinth top", "350 / 2850 / 800", "Read / Read / Photo", "scene; kit; R1, R2"],
    ["plinth proud / width", "150 / 350", "Read", "kit (the sill's nose is also 150)"],
    ["shaft width and place", "290 at u 30 to 320 of the slot", "Photo (290.1 +-8%) and Read", "P1; kit"],
    ["shaft proud", "110", "Photo", "118 +-14% (D3)"],
    ["neck z, capital height, capital top z", "2540, 310, 2850", "Derived / Photo / Read", "2850 - 310; P1 301 +-24; the console stands on it"],
    ["capital top face", "350 x 130", "Read", "kit; the console's toe (240 x 60) stands wholly on it"],
    ["capital members (z local from the neck)", "astragal 0-24 (r 12), fillet 24-34, die 34-154 with a tablet 170 x 80 x 8 proud, hollow flare 154-244 (d 114 to 128), abacus 244-296 (d 130), ovolo top 296-310", "Judgement from P1's order", "P1 shows a necking ledge, a die with three roundels, a flared cap, a band"],
    ["optional bosses", "3 x diameter 30, 6 proud, pitch 56, on the die's centre line at z local 94", "Photo (P1's three roundels)", "off by default (Rita's is plain); allowed on the ironmonger's and the empty unit's"],
    ["panelled shaft", "stiles 45, sunk 12, bead 10 (quarter-round), bottom rail 800-940, top rail 2430-2540", "Judgement (the kit's)", "FRONTAGE: raised and fielded or panelled (BC1, BH)"],
    ["fluted shaft", "5 flutes, 43.6 wide, 12 deep, between 12 fillets", "Judgement (the kit's)", "HE1 Skipton: fluted pilasters with consoles"],
    ["render variant: stepped plinth", "blocks to 504 / 631 / 680, cap slab to 800, each 4 to 8 back in depth and 15 / 26 / 38 in on the FREE side only", "Photo (P1's four stepped members: tops at 0.63 / 0.79 / 0.85 / 1.0 of the plinth)", "R1"],
    ["clad variant (Mickey's, as built)", "350 wide, 100 proud, no plinth, no capital, sheet joints at z 1200 and 2400, 6 wide", "Judgement", "the Hook sheet and the street"],
    ["downpipe chase", "76 wide (u +-38) from d 50, through both neighbours' plinths (z 0-800) and capitals (2540-2850)", "Judgement", "the D5 pipe's own numbers (68 across, axis 94)"],
])
w("Profiles (target.json `parts.pilaster.profiles`):")
w()
prof_list("pilaster", ["plinth_cap_side", "plinth_panel_side_through_stile", "plinth_panel_side_through_field", "plinth_stepped_side", "panel_bead", "shaft_panel_plan", "shaft_render_plan", "clad_plan", "capital_side"])
w("`shaft_flute_plan` has %d points. The elevation of each variant is in `variants.<v>.elevation` (rectangles and trapezoids in u, z)." % len(P["pilaster"]["profiles"]["shaft_flute_plan"]["points"]))
w()
w("**Joints and meets.**")
w()
for j in T["meets"]:
    if j["between"].startswith(("pilaster", "console and capital", "stallriser and plinths", "sill and plinth")):
        w("- **%s:** %s." % (j["between"], j["how"]))
w()
w("**Edges.** Timber: arrises square from the saw, eased 1 to 2.5 by repainting. Render: arrises run to a 1 mm radius. The plinth cap's nose is a 6 mm bead; the astragal a half-round r 12. Painted-over screw heads at 600 pitch in two lines 40 from the edges.")
w()

# ------------------------------------------------------------------------------------------------
w("## 6. Console")
w()
c = P["console"]["dims"]
w("**The kit gets right:** " + "; ".join(T["kit_vs_target"]["console"]["kit_gets_right"]) + ".")
w()
table(["change", "reason", "kind"], [[x["what"], x["reason"], x["kind"]] for x in T["kit_vs_target"]["console"]["target_changes"]])
table(["item", "value", "kind", "source"], [
    ["envelope", "240 wide x 180 deep x 550 high, z 2850 to 3400", "Read", "fascia-01 (the built mesh)"],
    ["centre", "u 175 and 5825; ranges 55-295 and 5705-5945", "Read", "the kit's meet; fascia-01"],
    ["toe", "240 x 60 at z 2850, a rounded nose r 14 to d 74", "Read", "fascia-01 profile"],
    ["silhouette", "the built profile's 11 key points, Catmull-Rom smoothed to 53 points", "Judgement on a Read", "self-check: every printed point within 4.5 mm"],
    ["volute (each side face)", "groove 5 wide, 4 deep, 1.75 turns from r 3 to r 24 about (d 34, z 82)", "Judgement", "the brief's 'scroll'; no photograph"],
    ["leaf (the front)", "acanthus pendant, z local 120 to 440, up to 120 wide at the top falling to a tip, 3 lobes a side, relief 12 at the rib, a rib 8 wide 4 proud, grooves 4 x 3 between lobes", "Judgement", "no photograph"],
    ["front chamfer", "12 down each front edge", "Read", "fascia-01 taper (1 part in 15)"],
    ["variants", "scroll (all original fronts); block (the grocer): S straightened to a 45-degree chamfer, no leaf, three bosses; absent (the empty unit's left: a stump 240 x 60 x 90 and two dowel holes)", "Judgement", "fascia-01 spec (the clipped console)"],
])
prof_list("console", ["side_silhouette", "plan_at_neck", "leaf_outline"])
w("`volute_spiral` is an open curve of %d points. **Fixings:** two 12 mm hardwood dowels 40 deep from the toe into the capital and two M10 coach screws through the back into the wall plate, all hidden; a rust bleed 20 long under each on the shaded side. **What P1 shows of consoles: nothing** (its pier caps are straight stepped blocks); the scroll and leaf are Judgement and are marked as such in the evidence table." % len(P["console"]["profiles"]["volute_spiral"]["points"]))
w()

# ------------------------------------------------------------------------------------------------
w("## 7. Fascia board, bed mould, cornice")
w()
w("**Fascia board** (kit gets right: " + "; ".join(T["kit_vs_target"]["fascia_board"]["kit_gets_right"]) + "). Changes: " + "; ".join(x["what"] + " (" + x["reason"] + ")" for x in T["kit_vs_target"]["fascia_board"]["target_changes"]) + ".")
w()
fd = P["fascia_board"]["dims"]
table(["item", "value", "kind", "source"], [
    ["board", "u 295 to 5705 (5410), z 2850 to 3400 (550), face d 120, 25 thick on rails", "Read", "the fascia target (it fixes the board: the lettering and the texture are its); the kit"],
    ["bed mould", "z 2850 to 2890, front d 132 (12 proud of the face, 2 proud of the capital's top front)", "Judgement (Photo for the idea)", "P1's field is framed where it meets the capital"],
    ["face", "one vertical plane", "Photo", "D6: P1; the book's 'sloped slightly forward' loses"],
    ["foot on the capital", "55 each end (u 295 to 350, 5650 to 5705)", "Derived", "350 - 295"],
    ["ends", "let into the consoles' inner sides by a 12 rebate", "Judgement", "-"],
    ["boxed, panelled or glazed", "a box sign (laundry 5200 x 480 x 150, newsagent 5220 x 470 x 140) or a flat panel (tea 5230 x 470 x 30) stands on this board; the grocer's board is three glass slabs on a backing in the same plane", "Read", "the fascia target"],
])
prof_list("fascia_board", ["section"])
w("**Cornice** (kit gets right: " + "; ".join(T["kit_vs_target"]["cornice"]["kit_gets_right"]) + "). Changes: " + "; ".join(x["what"] + " (" + x["reason"] + ")" for x in T["kit_vs_target"]["cornice"]["target_changes"]) + ".")
w()
cd = P["cornice"]["dims"]
table(["item", "value", "kind", "source"], [
    ["envelope", "5892 long (u 54 to 5946) x 215 deep x 150 high, soffit at z 3400, top at 3550", "Read", "fascia-01; the fascia target's cornice top 3.55"],
    ["drip groove", "d 155 to 175, 12 deep (35 outside the board's face)", "Read", "fascia-01"],
    ["oversail", "95 past the board's face, 35 past the console's front", "Derived", "215 - 120; 215 - 180"],
    ["corona face", "0 to 52 (0.35 of the height)", "Photo (P1's plain face is 0.39 of its crown)", "the sequence in section 3"],
    ["wash", "falls %.1f degrees from d 205 at z 130 to the back at 150; lead 1.8 over it, an apron 100 up the wall, upstands 25 at each end (not geometry)" % cd["wash_slope_deg"], "Judgement on a Read", "fascia-01: 27 degrees; the 4.5 degrees of change is for the new profile"],
    ["stops short of each party line", "54 (108 between neighbours; the pipe is 68)", "Derived", "fascia-01's arithmetic"],
    ["tall variant", "300 high x 280 deep (z 3400 to 3700): offered for a reviewer who reads P1's crown as binding; collides with the signs' brackets at 3.60", "Photo (not followed)", "D7"],
])
prof_list("cornice", ["section"])

# ------------------------------------------------------------------------------------------------
w("## 8. Sill and stallriser")
w()
w("**Sill.** Kit gets right: " + "; ".join(T["kit_vs_target"]["sill"]["kit_gets_right"]) + ". Changes: " + "; ".join(x["what"] + " (" + x["reason"] + ")" for x in T["kit_vs_target"]["sill"]["target_changes"]) + ".")
w()
sd = P["sill"]["dims"]
table(["item", "value", "kind", "source"], [
    ["z range / thickness / nose d", "525 to 600 / 75 / 150", "Read (600, 150) / Judgement (75)", "scene; Ellis's stout sill (the earlier reading); P1's sill group is 140 deep"],
    ["throat", "d 128 to 134, 6 deep, 16 back from the nose", "Judgement", "-"],
    ["weathering", "24 mm over 82 mm (15 degrees) to a flat bed 60 deep", "Judgement", "Ellis: top edges bevelled to shed rain"],
    ["length", "the window frame's 3350 plus 40 under each jamb (3430)", "Judgement", "-"],
    ["fixing", "No. 12 countersunk screws at 450 (7 along 3350), pellet-plugged, painted over", "Judgement", "-"],
])
prof_list("sill", ["section"])
w("**Stallriser** (kit gets right: " + "; ".join(T["kit_vs_target"]["stallriser"]["kit_gets_right"]) + "). Changes: " + "; ".join(x["what"] + " (" + x["reason"] + ")" for x in T["kit_vs_target"]["stallriser"]["target_changes"]) + ".")
w()
rows = []
for k, v in P["stallriser"]["variants"].items():
    rows.append([k, v["use"], json.dumps(v.get("dims", {}))[:300]])
table(["variant", "use", "numbers"], rows)
w("The stallriser is 0 to 525 under the sill, face d 125 (25 behind the plinth's 150 and the sill's nose). Tiled kinds: joints 3 mm, the tile's cap bullnose r 12 (brick tile) or a 35 high cap tile; courses add to exactly 525 (self-check). The brick-tile section and the panel section are `variants.tile.section` and `variants.panel.section`.")
w()

# ------------------------------------------------------------------------------------------------
w("## 9. Window frame, mullions, transom, toplights, glazing")
w()
w("**Kit gets right:** " + "; ".join(T["kit_vs_target"]["window_frame"]["kit_gets_right"]) + ".")
w()
table(["change", "reason", "kind"], [[x["what"], x["reason"], x["kind"]] for x in T["kit_vs_target"]["window_frame"]["target_changes"]])
wd = P["window_frame"]["dims"]
table(["item", "value", "kind", "source"], [
    ["frame length", "3350 (4294 with no side door), z 600 to 2850 on the sill", "Derived", "section 4"],
    ["bottom rail", "z 600 to 690", "Photo (P1's stallriser frame carries one)", "Judgement for 90"],
    ["lower lights / transom / toplights / head", "690-2400 / 2400-2480 / 2480-2790 / 2790-2850", "Read", "scene transom 2.40, 0.08; kit head"],
    ["jamb", "50 face x 95 deep, glazing rebate 12 x 12", "Read (kit 50, 85) / Judgement", "frame fronts at d 95 sit 15 behind the shaft's 110"],
    ["T1 mullion", "70 x front d 92 (62 in front of the glass), oval nose, rebates 10 x 12", "Judgement; Cornwall guide 40-70 projection", "D5"],
    ["T2 mullion", "80 x d 92, flat face with a quirk bead each edge", "Judgement", "the older, heavier section"],
    ["M1 / M2", "aluminium 50 x 75 box with glazing pockets; bronze-plated 28 x 40", "Judgement", "R05, R09 (the earlier reading)"],
    ["toplight bars", "28 wide (T1, T2, M2) or 50 (M1), counts per fronts[].glazing", "Judgement", "the kit's 8 lights on Rita's"],
    ["glass", "6 mm plate at d 30, in 12 mm rebates; beads: T1 ovolo 16 x 12 on brass screws at 250; old putty 14 x 10 (T2, the empty unit); M1 snap-in bead 14 x 8 over a black gasket", "Read (30) / Judgement", "kit; FRONTAGE"],
    ["mullion positions", "the kit's default is n = ceil((L - 100) / 1250) - 1, at most 3 (2 on 3350); the table sets the number per front (fish 3, laundry 1, ironmonger 1, grocer 2 on 4294); positions per shop in `shops[].glazing_layout` (mullion centres from the frame's left edge, toplight bars, light widths)", "Derived", "the kit's rule; the table"],
])
prof_list("window_frame", ["mullion_t1_plan", "mullion_t2_plan", "mullion_m1_plan", "bar_m2_plan", "jamb_t1_plan", "jamb_m1_plan", "transom_t1", "transom_m1", "toplight_bar_plan", "glazing_bead_ovolo", "glazing_bead_gasket", "glazing_putty", "head_section"])
w("**Joints.** " + "; ".join("%s: %s" % (j["between"], j["how"]) for j in T["meets"] if j["between"].startswith(("window frame", "transom", "mullions"))) + ".")
w()

# ------------------------------------------------------------------------------------------------
w("## 10. Shop door, side-door slot, lobby")
w()
w("**Shop door.** Kit gets right: " + "; ".join(T["kit_vs_target"]["shop_door"]["kit_gets_right"]) + ".")
w()
table(["change", "reason", "kind"], [[x["what"], x["reason"], x["kind"]] for x in T["kit_vs_target"]["shop_door"]["target_changes"]])
dd = P["shop_door"]["dims"]
table(["item", "value", "kind", "source"], [
    ["leaf / slot / thickness", "900 x 2040 / 1006 / 50", "Read (scene, kit) / Read (Ellis 2 in)", "-"],
    ["rails and stiles", "stile 115, top rail 115 (1925 to 2040), bottom rail 0-230 (9 in, Ellis), lower panel 230-590 raised and fielded, lock rail 590-700, glass 700-1925", "Read (Ellis) / Judgement", "P1: glazed from 0.328 of the leaf; BH: two-thirds glazed (D2)"],
    ["glazing", "one 6 mm pane, ovolo bead 14 x 11 (T1)", "Judgement", "-"],
    ["kick plate / foot strip", "brass 770 x 170 with 8 screws / brass 30 high across the leaf's foot, 3 proud", "Read (kit) / Photo (29 mm, P1)", "-"],
    ["furniture", "lever handles on 240 x 40 backplates at z 1000; a rim latch and a mortice escutcheon at 950; letter plate 250 x 40 at z 800 on the lower panel's centre", "Read (kit) / Judgement", "-"],
    ["hinges", "three 100 x 75 butts at 150 / middle / 150, 6 No. 8 screws each", "Read", "kit"],
    ["frame and threshold", "jambs 50 x 100, leaf 3 clear; terrazzo threshold 25 high at the leaf falling to 12, nose out to d 130 (flush fronts)", "Read", "kit"],
    ["fanlight, transom, toplight", "fanlight 2131 to 2400 (one pane); the shop's transom runs across 2400-2480; a two-bar toplight 2480-2790; head 2790-2850", "Read", "kit"],
    ["variants", "T1 timber; M1 aluminium glass door 50 stiles, 100 top rail, 170 bottom rail, a 300 chrome D pull; M2 bronze, 150 kick plate", "Judgement", "-"],
])
prof_list("shop_door", ["threshold_section", "glazing_bead", "leaf_stile_plan", "frame_jamb_plan", "raised_field_edge"])
w("**Side-door slot (the front-door family's F1, NOT re-targeted).** The slot is 944 wide: F1's opening shows 895.2 (jambs 49 past the shopfront's framing) and a 24.4 filler strip each side (the pier's return, painted the pier's colour). It sits in the bay like this:")
w()
for k, v in P["side_door_slot"]["mapping_from_F1"].items():
    if isinstance(v, list):
        for i in v:
            w("- trim: " + i + ".")
    else:
        w("- **%s:** %s." % (k, v))
w("- Above the F1 head: the shop's transom (2400-2480) runs across the slot, then a raised-and-fielded panel 2480-2790 and the head 2790-2850 (the kit's). The leaf's letter plate is 250 x 40 (scene), at F1's own height.")
w()
w("**Lobby.** Flush fronts have none. Recessed: the door frame's front face stands `100 - recess` (grocer 600: d -500; launderette 300: d -200); the window's end and the pier's side are returned (grocer: a glazed display return with a 600 kick panel in the green glass, and a panelled lining; launderette: both square). Floors: the grocer's terrazzo (grey with white chips, z 25, a 150 border of 20 mm tiles in cream and bottle green, a 30 x 6 brass nosing at the frame line); the launderette's 150 quarry tile, red-brown. Ceiling: plaster or board at z 2400, the toplights running on above. The shop-room's card is behind; the lobby takes 300 to 600 of the shop's depth.")
w()

# ------------------------------------------------------------------------------------------------
w("## 11. How the parts meet")
w()
table(["between", "how"], [[j["between"], j["how"]] for j in T["meets"]])
w("**Fixings by part** (what is visible after repainting is stated; the rest is hidden):")
w()
table(["part", "fixing"], [[f["part"], f["fixing"]] for f in T["fixings"]])

# ------------------------------------------------------------------------------------------------
w("## 12. 1990: condition and the alterations by kind")
w()
w("Wear: " + T["wear"]["earlier_notes_1990"] + ". " + "What the photograph shows of wear on a part: " + T["wear"]["photo_P1_2019"] + ".")
w()
w("Geometry that wear adds to the parts: " + "; ".join(T["wear"]["geometry_wear_in_this_target"]) + ".")
w()
rows = []
for k, a in T["alterations"].items():
    rows.append([k, a["what"], json.dumps(a["numbers"])[:360], ", ".join(a["applies_to"]), a["kind"]])
table(["kind", "what", "numbers", "applies to", "evidence"], rows)
w("**Roller-shutter box, from the CC0 scans.** The four Poly Haven shutters read today have hoods 153, 168, 300 and 300 deep for curtains 1546, 1561, 1851 and 2400 high, the curtain's plane at z 20 and rails 7 wider than the curtain: the target's hood is 300 high x 190 deep over the window and shop door (z 2550 to 2850), with the curtain at d 30 and the guide rails 50 x 40 on the frames. Raised by day (the box and the rails only); lowered at night (a variant).")
w()

# ------------------------------------------------------------------------------------------------
w("## 13. The ten fronts: the assembly table")
w()
w("Twelve shopfronts are RULINGS' count; the scene has ten shop bays (six east, the chandler, three west). Ten are tabled. Door end is the VIEWER's side in the game. Paint columns are plain names; sRGB values are in `shops[].paint_srgb` and `paints`.")
w()
rows = []
for s in T["shops"]:
    rows.append([s["id"], s["trade"], "%s %d, x %g-%g" % (s["block"], s["bay"], s["street_x_m"][0], s["street_x_m"][1]), s["original_or_altered"] + ": " + s["kind"], s["stallriser"]["variant"] + " (" + s["paint_names"]["stallriser"] + ")",
                 "%s; recipe doors_on %s; side door %s" % (("viewer's LEFT" if s["door_end_viewer"] == "L" else "viewer's RIGHT"), s["recipe_doors_on"], "yes" if s["side_door"] else "none"),
                 s["lobby"]["kind"] + (" %d" % s["lobby"]["depth"] if s["lobby"]["kind"] == "recessed" else ""), "%s: %d lights, %d toplights, %s" % (s["glazing"]["pattern"], s["glazing"]["n_mullions"] + 1, s["glazing_layout"]["toplights"], s["glazing"]["window_frame"])])
table(["id", "trade", "bay", "original or altered", "stallriser", "door position", "lobby", "glazing pattern"], rows)
rows = []
for s in T["shops"]:
    rows.append([s["id"], s["pilaster"], s["console"] + (" (left absent)" if s.get("console_absent_viewer") else ""), s["shop_door"], ", ".join(s["alterations"]),
                 "u: window %s, shop door %s, side door %s" % (s["zones_u"]["window"], s["zones_u"]["shop_door"], s["zones_u"]["side_door"]),
                 "window %.3f, side %s" % (s["centres_street_x_m"]["window"], s["centres_street_x_m"]["side_door"])])
table(["id", "pilaster", "console", "shop door", "alterations", "zones (mm)", "street x (m)"], rows)
rows = []
for s in T["shops"]:
    pn = s["paint_names"]
    ps = s["paint_srgb"]
    def cc(k):
        return "%s %s" % (pn.get(k, "-"), ps.get(k, ""))
    rows.append([s["id"], cc("pilaster"), cc("fascia_board"), cc("stallriser"), cc("window_frame"), cc("shop_door"), cc("side_door") if s["paints"].get("side_door") else "none"])
table(["id", "piers, consoles, cornice", "fascia board", "stallriser", "window frame", "shop door", "side door"], rows)
w("**Why these.** The trades and bays are Jafar's (3 October). Rita's is the model he called the best thing on the page. The refits follow the street's recipe where it has one (Mickey's slate steel front on patterned tile; the fish shop's, the chandler's metal fronts with plain glazed tile) and the fascia target where it fixes a date (the grocer's glass board means a 1930s refit; the laundry's and newsagent's box signs mean 1980s additions; the tea room's flat panel a 1980s caff). The empty unit is the one front nobody repainted. Four of ten are original timber repainted (Rita's, tea, ironmonger, newsagent) and the empty unit is original and derelict; five are altered. Departures from the recipe or the fascia target are in section 16.")
w()
w("**Paints.** Every colour is an aged 1990 sRGB value with a plain name; the source or kind is in `paints.<id>.note`. Rita's oxblood (93, 46, 49) is the fascia target's aged oxblood; the whole palette is in the JSON (%d entries)." % len(T["paints"]))
w()

# ------------------------------------------------------------------------------------------------
w("## 14. Photographs win: each disagreement and what was chosen")
w()
table(["id", "element", "book or scene", "photograph", "chosen"], [[x["id"], x["element"], x["book_or_scene"], x["photograph"], x["chosen"]] for x in T["disagreements_photographs_win"]])
w("**Ratio rules** (target.json `derived_rules`; self-check group 2 recomputes each):")
w()
table(["rule", "photograph", "target", "within", "reading"], [[r["id"] + " " + r["name"], r["photo"], r["target"], ("yes" if r["within"] else "NO") + ("" if r.get("followed", True) else " (not followed)"), r["reading"]] for r in T["derived_rules"]])

# ------------------------------------------------------------------------------------------------
w("## 15. Checks, previews, drawing, self-check")
w()
w("**Checks for unit 3.2** (`checks`, %d of them; each has a name, what to measure, the expected value and a tolerance): the pilaster (slot, plinth top, proud, shaft width, neck, capital top and size, panel and flute numbers, the pair's gap and the downpipe chase, profile fit), the console (envelope, centre, foot on the capital, top at the cornice's soffit, silhouette, leaf, volute), the fascia and cornice (size, foot on the abacus, bed mould, oversail, soffit gap, profile, stops), the sill, stallriser, window frame (transom, head, mullion section and positions, glass plane, length per shop), the shop door (leaf, glazed from 700, slot, foot strip, furniture), the side-door slot (944, F1's head meeting the transom, frame face d 100, the threshold's nose d 130), the zones filling 5300, the alterations, and per shop the door end, zones and street x of the window and the side door (the fascia target's own numbers). Materials: at most three plain PBR materials per piece, no textures, paint a per-shop parameter. No lettering, no maker's mark." % len(T["checks"]))
w()
w("**Previews** (`production/previews/cloud-week/refs/shopfronts/`, JPEG, at most 1200 px, under 300 KB; for the reviewers; the photograph is Andreas Mischok's Leadenhall Market HDRI, CC0, taken 2019-05-19, polyhaven.com; the crops show joinery only; the two sets of house numerals and a fragment of a shop-window logo are masked; no business is named; the drawings are the studio's own):")
w()
table(["file", "what"], [
    ["`P1-leadenhall-pilaster-plinth.jpg`", "the plinth's four stepped members and the foot (350 x 700 px at the virtual 2400 px focal length; a logo fragment masked top left)"],
    ["`P1-leadenhall-pilaster-capital.jpg`", "shaft top, necking ledge, die with three roundels, flared cap, top band"],
    ["`P1-leadenhall-pier-fascia-cornice.jpg`", "the pier head under the fascia and the crown (numerals masked)"],
    ["`P1-leadenhall-cornice-run.jpg`", "the continuous crown to the right of the pier"],
    ["`P1-leadenhall-sill-stallriser-stile.jpg`", "sill group, framed stallriser panel, foot rail, stile"],
    ["`P1-leadenhall-transom-mullion.jpg`", "the mid transom bar and the central mullion"],
    ["`P1-leadenhall-*-target-on-photo.jpg`", "the drawing (cyan) laid on each crop: bands built from the measured rows and columns, at the scale fitted on one dimension"],
    ["`D1-ritas-bay-elevation.jpg`", "the target's elevation of Rita's whole bay (drawn at 1 mm to the pixel, reduced), with the neighbours' pair of pilasters and consoles in grey and the downpipe between"],
    ["`D2-ten-fronts-sheet.jpg`", "the ten fronts assembled from the table"],
    ["`D3-parts-pilaster-console-fascia.jpg`", "four pilaster variants, the console's silhouette and front, the capital / console / fascia / cornice section"],
    ["`D4-parts-sections.jpg`", "eighteen sections at x0.3 to x3"],
])
w("**Credits.** P1: Andreas Mischok, Leadenhall Market, CC0 (Poly Haven), taken 2019-05-19. P2 (numbers only; no picture kept): Poly Haven rollershutter models, author MP, CC0, published 2023-10-11. The drawings are LEDGER's own.")
w()
if SELF:
    w("**Self-check (%s):** **%d of %d checks pass; %d fail; %d departures reported and kept in the open.** Groups: " % (SELF["date"], SELF["passed"], SELF["total"], SELF["failed"], SELF["reported"]) + "; ".join("%s %d pass %d fail %d reported" % (k, v["pass"], v["fail"], v["report"]) for k, v in sorted(SELF["groups"].items())) + ".")
    w()
    w("The groups: 1 printed (the numbers read again from SCENE-SLOTS.md, fascia-01's recipe, the kit README, the fascia target and the front-door target); 2 photo (every row and column re-measured on the saved previews; the scale and the ratio rules recomputed); 3 wins (each disagreement recomputed); 4 overlay (the drawing's edges on the previews, worst %s px of %s edges); 5 consistency (profiles are simple counter-clockwise polygons; the parts add up; the ten fronts' zones; nothing overlaps that should not and nothing floats in any of the ten drawings; paints, shops, alterations and checks well formed; the content rule); 6 faults (eight deliberately broken copies, each noticed)." % (SELF["stats"].get("overlay_worst_px"), SELF["stats"].get("overlay_edges")))
    w()
    w("The reported lines are not failures but departures kept visible:")
    w()
    for l in SELF["reported_lines"]:
        w("- %s: %s%s" % (l["group"], l["name"], (" (" + l["detail"] + ")") if l.get("detail") else ""))
    w()

# ------------------------------------------------------------------------------------------------
w("## 16. What the target could not settle")
w()
for i, s in enumerate(T["could_not_settle"], 1):
    w("%d. %s" % (i, s))
w()
w("Also: the fascia target's boards and glass lettering, the front-door family's F1 door, the wear target's layer and the shop-room's displays are not re-done here; where this target touches them (the board's plane and bed mould, the F1's mapping, the splash band on tiled and slab stallrisers, the sill's display bed) it says how.")
w()
open(os.path.join(HERE, "TARGET.md"), "w").write("\n".join(out))
print("wrote TARGET.md", len(out), "lines")
