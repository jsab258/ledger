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
w("Cloud week 42, 9 October 2026, SECOND TRY by the target writer, answering the fresh reviewer's FAIL of the first try (eleven faults, `TARGET-REVIEW.md`; section 17 says how each was answered, and the two places this target does not follow the review). For unit 3.2 (the parts) and the builder (the assembly). Fixes applied after the second review (section 18) by Jafar's ruling of 9 October, not re-reviewed. Nothing is committed. Everything in this file is in `target.json`; the checks that follow from it are in its `checks` list and its `self_check`.")
w()
w("## 0. Files, and how to read them")
w()
w("Files in `production/cloud-week/targets/shopfronts/`:")
w()
table(["file", "what it is"], [
    ["`TARGET.md`", "this page (written by `make_doc.py` from `target.json` and its own prose)"],
    ["`target.json`", "every part with dimensions, profiles as point lists, positions, variants, materials; the paints; the ten fronts' assembly table; the alterations; %d `checks`; the self-check result" % len(T["checks"])],
    ["`target_drawing.py`", "draws target.json ALONE: each part's elevation and sections (including the cornice's mitred ends in plan and the roller shutter's section), an elevation of Rita's whole bay and of the ten, at 1 mm to the pixel, into a folder given on the command line, with the polygons as JSON, the drawing laid on the photograph's previews and Rita's elevation laid on the re-projected pier"],
    ["`self_check.py`", "tests the target against its own sources and the photograph's saved previews; writes `self_check` into target.json"],
    ["`measure_leadenhall.py`", "author tool: re-projects the photograph to a level elevation, measures it (45 rows and columns and one notice), writes `photo_measurements.json` and the previews (including the masked door preview and the pier strip)"],
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
    ["pilaster (4 variants + an unused tall plinth)", "plinth 600 at Rita's line, 180 proud; shaft 290 x 140 proud; necking; capital 310 on a hollow flare, top 350 x 175; panelled and fluted on the kit's base ogee (15 proud), rendered on a stepped plinth with a hollow-moulded head, flush clad", "shaft 100 to 140 and plinth 150 to 180 (the shaft stands 40 or more in front of every frame); the plinth's head moulding restored; the plinth NOT raised to P1's 800 (Rita's line)"],
    ["console (scroll, block, absent)", "240 x 205 x 550 rising from the front of the capital (foot 240 x 172), a two-volute scroll under a cap block, its front at least d 140 at every height, grooves ending in eye bosses, an acanthus leaf", "a scroll in a deeper envelope (the built mesh's 180 stood behind the board's bed mould); Judgement, no photograph of a console was reached"],
    ["fascia board", "5410 x 550, 120 proud, a 40 bed mould; vertical", "the bed mould"],
    ["cornice", "215 x 150 x 5892, 19-point profile with a tall corona, a mitred return closing each end", "profile and ends only: the fixed envelope stays (the photograph's crown is not measurable by the method)"],
    ["sill, stallriser (%d variants)" % len(P["stallriser"]["variants"]), "sill 75 thick, nose 150; panelled, brick tile, square tile, patterned tile, glass slab, render, boarded, grille", "sill 50 to 75; more stallriser kinds for the ten fronts"],
    ["window frame (T1, T2, M1, M2)", "mullions 70 / 80 / 50 / 28 wide, transom 80, toplights, glass at d 30 on a 25 mm seat", "mullion 55 to 70 (the photograph reads 172: partly followed); the bottom rail withdrawn"],
    ["shop door (T1, M1, M2)", "900 x 2040 in 1006, **glazed from 600, level with the sill**, letter plate in the lock rail at z 545, brass foot strip, a hinge side per shop", "glazed from 1000 to 600 (Photo and the books agree against the scene)"],
    ["side door slot", "944 slot for the front-door family's F1 (not re-targeted): the mapping into the bay, mirrored where the doors are on the viewer's left", "none"],
    ["roller shutter", "hood 300 x 210 deep, rails d 150 to 190, curtain plane d 170, in front of every frame", "the first try's curtain stood inside the frames"],
    ["lobby", "recessed 600 (grocer) and 300 (launderette), tiled or terrazzo floors", "new"],
    ["ten fronts", "an assembly table: trade, bay, original or altered, stallriser, door end, hinge sides, lobby or flush, glazing pattern, paints", "new"],
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
w("P1 is re-projected to a level rectilinear elevation of the arcade's right-hand wall (yaw 90, focal 2400 px); a plane parallel to the wall is then at one scale, and each plane has its own. `measure_leadenhall.py` snaps each edge to the strongest luminance gradient near where it was looked for, averaged along a span chosen to avoid ornament; `self_check.py` re-measures every row and column that can be on the SAVED previews (45 rows and columns: the door's glass foot, strip and foot are on a masked door preview now). The fresh reviewer re-ran the tool on the 16k file and every stored row came back identical to 0.00 px. **Scale:** fitted on ONE dimension, an A5 notice (148 x 210 mm) on the shop door's glass, %.2f x %.2f px (England's statutory no-smoking sign, whose 2007 minimum was A5: from memory, legislation.gov.uk unreached), giving %.4f mm a pixel in the door's plane. Each plane's scale is the camera's height over its own foot row (all at one footway level): the pilaster's front **%.4f mm a pixel** (the camera about %d mm up), the window frame's **%.4f** (its foot row 559.3: it stands %s behind the pier's face) and the door's %.4f (%s behind). Error %d per cent (the A5 assumption, the plane ratios and the notice's edges); ratios carry none of it. **Parts above eye level and proud of their plane are drawn taller by D.p/(D - p)** (D the height above the eye, p the projection over the camera's distance): the crown and the capital are NOT measurable this way, only bounded." % (
    SC["notice_px"][0], SC["notice_px"][1], SC["mm_per_px_door_plane"], SC["mm_per_px_pilaster_plane"], SC["camera_height_mm_above_footway"], SC["mm_per_px_window_plane"],
    "%d mm" % SC["plane_depths_behind_pier_face_mm"]["window_frame"], SC["mm_per_px_door_plane"], "%d mm" % SC["plane_depths_behind_pier_face_mm"]["shop_door"], SC["error_pct"]))
w()
table(["what", "measured (P1, mm at the stated plane; kind Photo, +-8 per cent unless stated)", "the street's number", "reading"], [
    ["shaft width", "%.0f" % DM["shaft_width"], "290 (kit)", "the kit's 290 stands: no disagreement"],
    ["shaft relief (30.8 px of painted return at 1087 px off axis; 71 px more to the teal frame)", "%.0f (lower bound) to %.0f (the frame)" % (DM["shaft_proud"], DM["shaft_proud_to_window_frame"]), "scene 100; first try 110; target 140", "D3: the first try read the 117 as the whole relief; it is the return beside the next surface; 140 sits inside both bounds and keeps 40 or more in front of every frame"],
    ["plinth: block tops z", "%.0f / %.0f / %.0f; hollow-moulded head to %.0f" % (DM["plinth_block1_top_z"], DM["plinth_block2_top_z"], DM["plinth_block3_top_z"], DM["plinth_top_z"]), "kit 600; target 600", "R1, R2: P1's plinth is 1.33 x its sill and 0.228 of its front's height; NOT followed: Rita's line (the plinth's top level with the stallriser) wins (D1)"],
    ["capital height (neck ledge to abacus top)", "at most %.0f (1.04 x the shaft's width)" % DM["capital_height"], "kit 330; target 310", "D4: an upper bound (the flare's and abacus's undersides add 30 to 60 mm); 310 is Judgement"],
    ["the board between the crown and the capital top", "%.0f" % DM["board_between_crown_and_capital_top"], "550", "no disagreement: the street's 550 is the same order (not 'between the gilt keylines': that sits about 65 px lower)"],
    ["crown (cornice), apparent", "%.0f at the pilaster plane (%.2f of the board)" % (DM["crown_apparent_height_pilaster_plane"], RT["crown_apparent_over_board"]), "150 (0.27 of the fascia)", "D7: NOT measurable by this method: true crown 170 to 300 (0.35 to 0.6 of the board); the street's 150 stands (the fascia target fixes the cornice top at 3550); R8 withdrawn"],
    ["sill top (the window's own plane)", "%.0f (%.3f of the front's height; 0.61 m at 3.55)" % (DM["sill_top_z_window_plane"], RT["sill_top_over_front_height"]), "600", "no disagreement (2 per cent); R3 0.172 against 0.169"],
    ["window stile / mullion face (window plane)", "%.0f / %.0f (the mullion %.2f of its 1.0 m light)" % (DM["window_stile_face"], DM["mullion_face"], RT["mullion_over_light"]), "kit 50 / 55; target 50 / 70", "stile not followed (a heavy arcade frame; the first try's 145 was a bar of the cast grille); D5: mullion partly followed"],
    ["transom bar face", "%.0f" % DM["transom_bar_face"], "80 (the street's transom is a high toplight transom)", "not comparable: P1's bar is a mid glazing bar"],
    ["stallriser panel (a framed cast grille)", "%.0f high" % DM["stallriser_panel_height"], "525 (panel zone)", "the same order"],
    ["shop door (door plane)", "leaf %.0f high; glass foot %.0f up (%.3f of the leaf: row 128.9, strength 12.2); glass top %.3f" % (DM["door_leaf_height_door_plane"], DM["door_glass_foot_door_plane"], DM["door_glazed_from_fraction"], DM["door_glazed_to_fraction"]), "2040; scene glazed from 1000 (0.49); target 600 (0.294)", "D2: 620 on a 2040 leaf, level with the window's sill (844) to within 46 mm; the first try's row 95.7 (strength 1.5) lay inside the dark glass"],
    ["door foot strip", "%.0f high" % DM["door_foot_strip_height"], "-", "added: 30 high brass strip (the plate's lowest 30 on T1)"],
])
w("**Why P1 still holds for a 1900-1935 provincial parade, and where it does not.**")
w()
w("- It holds near eye level for what it measures: **the plinth against the sill, the door glass against the sill, the shaft's width, the foot strip and the order of members** (a plinth, a hollow-moulded head, a shaft, a necking and a capital, a fascia field of about half a metre, a sill group much deeper than a bead, a stallriser panel in a frame, a shop door about a third plain). Each ratio is compared with the street's own fixed numbers in section 14 (R1 to R9).")
w("- It does **not** hold for: absolute sizes of a heavy arcade's joinery (its mullion is 0.15 of its light, the street's 0.06; its stile 77); a stone- or cement-faced pier's finish; the crown's height (not measurable); its single piers and the absence of consoles; anything with a scroll, a leaf, a roller shutter, a box sign, aluminium or a lobby, because P1 shows none; and anything about 1990 (it is a 2019 restoration in fresh gloss).")
w("- Where a P1 proportion and the street's fixed number disagree beyond the error, section 14 says which won and why. Rita's window is Jafar's model: where P1 would break its line (the plinth) the model wins and the photograph's value is kept as an unused variant.")
w()
w("**Which parts rest on what** (the brief asks plainly):")
w()
rows = []
for k, e in T["evidence_basis"].items():
    rows.append([k, "; ".join(e["photo_today"]) or "nothing", "; ".join(e["earlier_notes"]) or "-", "; ".join(e["judgement"]) or "-"])
table(["part", "photographs measured today (P1, P2)", "the earlier notes (cited, not re-read)", "judgement"], rows)
w("**Edges measured on P1 and laid on it.** The drawing's projected edges (the instance polygons) fall on the saved previews within 4 px (8 px for the weakest edges); %s edges were tested and the worst is %s px. These edges were measured on the same crops that the previews are made from, so this test shows that the polygons are built from the measurements correctly, that JPEG compression does not move them, and that the snap is reproducible: it is NOT an independent validation of the numbers (that is what the ratio rules and the street's fixed numbers are for). The previews are crops of the joinery only, with the house numerals masked, the glass above the shop door's foot and everything seen through the shop window beside the pier filled flat; no whole frame and no lettering is in any preview. Rita's own elevation is laid on the re-projected pier in a second test (section 15), which is a comparison, not a circle." % (SELF.get("stats", {}).get("overlay_edges", "?"), SELF.get("stats", {}).get("overlay_worst_px", "?")))
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
    ["d: shaft front / plinth front / capital top front", "140 / 180 / 175", "Photo (bounds) and Judgement / Judgement / Judgement", "D3: the shaft 40 or more in front of every frame; the kit had 100 / 150 / 130"],
    ["d: fascia face / bed mould front / console front (at least) / cornice nose", "120 / 132 / 140 (205 at the volute and cap block) / 215", "Read / Judgement / Judgement / Read", "fascia target; fascia-01 (the console's 180 is deepened to 205); the console stands proud of the board at every height (CON-09)"],
    ["d: sill nose / stallriser face / frame fronts / mullion front / glass", "150 / 125 / 95 and 100 / 92 / 30", "Read / Read / Judgement / Judgement / Read", "kit; the mullion front is 62 in front of the glass (D5); the frames stand 45 (window) and 40 (doors) behind the shafts"],
    ["d: roller shutter hood / guide rails / curtain", "210 / 150 to 190 / 170", "Judgement", "rails and curtain clear of every frame, the sill (150) and the threshold (130); the hood is set into the toplight zone (head, bars and glass cut away behind it)"],
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
    ["slot / height / plinth top", "350 / 2850 / 600", "Read / Read / Read (Rita's line)", "scene; kit; the approved model: the plinth's top level with the sill and the stallriser. P1's 1.33 x its sill is NOT followed (D1); variants.plinth_tall (800) is offered, unused"],
    ["plinth proud / width", "180 / 350", "Judgement (the relief rule) / Read", "kit 150; the shaft 140 and the plinth 40 in front of it; the sill's nose (150) 30 behind it"],
    ["shaft width and place", "290 at u 30 to 320 of the slot", "Photo (290.1 +-8%) and Read", "P1; kit"],
    ["shaft proud", "140 (the clad casing 140)", "Photo (bounds 117 and 276) and Judgement", "D3; check PIL-15: at least 40 in front of every frame beside it (window jamb 95, shop-door and F1 frames 100)"],
    ["neck z, capital height, capital top z", "2540, 310, 2850", "Derived / Judgement (P1 301 is an upper bound) / Read", "2850 - 310; the console stands on it"],
    ["capital top face", "350 x 175 (the flat reaches d 172, an ovolo rounds the last 3)", "Judgement", "kit 130; the console's toe (240 x 60) stands wholly on it; the board's mould front (132) 43 behind it"],
    ["capital members (z local from the neck)", "astragal 0-24 (r 12), fillet 24-34, die 34-154 at d 144 with a tablet 170 x 80 x 8 proud, hollow flare 154-244 from d 144 to 172, abacus 244-296 (d 175), ovolo top 296-310", "Judgement from P1's order; the flare after P1", "P1 shows a necking ledge, a die with three roundels, a flared cap (57 and 77 px beyond the shaft's edge), a band"],
    ["optional bosses", "3 x diameter 30, 6 proud, pitch 56, on the die's centre line at z local 94", "Photo (P1's three roundels)", "off by default (Rita's is plain); allowed on the ironmonger's and the empty unit's"],
    ["panelled shaft", "base ogee on the plinth (z 600 to 660), stiles 45, sunk 12, bead 10 (quarter-round), bottom rail 600-740, top rail 2430-2540", "Judgement (the kit's)", "FRONTAGE: raised and fielded or panelled (BC1, BH)"],
    ["base ogee (panel and flute)", "the kit's BASE made 15 proud of the shaft's face (the second review's points: (140, 600) (155, 600) (155, 608) (152.6, 612) (149, 617) (146, 624) (143.6, 633) (141.8, 645) (140, 660)), 60 high, returned on both sides of the shaft", "Read (pilaster.py) and the review", "restored: P1 shows a moulding at the shaft's foot; 15 not the kit's 25 so that its front (d 155) stands on the cap's flat and does not float over the weathering"],
    ["fluted shaft", "5 flutes, 43.6 wide, 12 deep, between 12 fillets", "Judgement (the kit's)", "HE1 Skipton: fluted pilasters with consoles"],
    ["render variant: stepped plinth with a hollow head", "blocks to 360 / 450 / 484 (4 and 8 back), then a hollow (cavetto, 24 x 95) from d 172 at z 484 to d 148 at z 579 and a band 21 high to 600, the shaft 8 behind it; steps 8 / 14 / 22 in on the FREE side only", "Photo (P1's three steps and the hollow-and-band head) and Judgement (the lower blocks shortened to fit Rita's 600)", "P1's blocks are 504 / 631 / 684 on 800; the head kept whole; the steps limited by the slot's 30 mm margin"],
    ["clad variant (Mickey's, as built)", "350 wide, 140 proud (the old shaft's face), no plinth, no capital, sheet joints at z 1200 and 2400, 6 wide", "Judgement", "the Hook sheet and the street"],
    ["downpipe chase", "76 wide (u +-38) from d 50, through both neighbours' plinths (z 0-600) and capitals (2540-2850); the pipe's front (d 128) stands 12 behind the shafts", "Judgement", "the D5 pipe's own numbers (68 across, axis 94)"],
])
w("Profiles (target.json `parts.pilaster.profiles`):")
w()
prof_list("pilaster", ["plinth_cap_side", "plinth_panel_side_through_stile", "plinth_panel_side_through_field", "base_ogee", "plinth_stepped_side", "plinth_tall_stepped_side", "panel_bead", "shaft_panel_plan", "shaft_render_plan", "clad_plan", "capital_side"])
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
    ["envelope", "240 wide x 205 deep x 550 high, z 2850 to 3400 (the cornice's 215 nose oversails it by 10)", "Read (240, 550) / Judgement (205)", "fascia-01's built mesh is 180 deep and stands behind the board's bed mould (132); the second review deepened it"],
    ["centre", "u 175 and 5825; ranges 55-295 and 5705-5945", "Read", "the kit's meet; fascia-01"],
    ["foot", "240 x 172 at z 2850 on the capital's flat top (350 x 175; the flat reaches d 172), so the console rises from the capital's front", "Judgement", "CON-03"],
    ["front rule", "the front is at least d 140 at every height from 2850 to 3400, in front of the board's bed mould (132) and face (120): no board end or mould stands proud of it", "Judgement", "CON-09, recomputed from the outline"],
    ["silhouette: lower volute", "eye at d 158, z 48, outer radius 26, reaching d 184 at z 48 (9 past the capital's front), one turn, rolling the other way (clockwise inward)", "Judgement", "-"],
    ["silhouette: waist and stem", "concave, narrowest d 140 at z 140, swelling to d 150 at z 330 (straight to z 413, then a concave fillet r 10 into the upper volute)", "Judgement", "-"],
    ["silhouette: upper volute", "eye at d 160, z 468, outer radius 45: the front reaches d 205 at z 468, rolls back over the top through (160, 513) and into the eye in 1.25 turns (the groove)", "Judgement", "the review's fault 5, in the re-review's deeper numbers"],
    ["silhouette: cap block", "205 deep at z 528 to 550, over a notch 15 high at the upper volute's top", "Judgement", "the cornice's soffit lies on it"],
    ["side grooves", "8 inside the outline, 5 wide, 4 deep, each winding into an eye boss 16 across and 3 proud (upper 1.25 turns r 37 to 10, lower one turn r 18 to 11)", "Judgement", "-"],
    ["leaf (the front)", "acanthus pendant, z local 150 to 420, up to 120 wide at the top falling to a tip, 3 lobes a side, relief 12 at the rib, a rib 8 wide 4 proud, grooves 4 x 3 between lobes", "Judgement", "no photograph"],
    ["front chamfer", "12 down each front edge", "Read", "fascia-01 taper (1 part in 15)"],
    ["variants", "scroll (all original fronts); block (the grocer): the same envelope, flaring from the 172 foot to 205, no leaf, three bosses; absent (the empty unit's left: a stump 240 x 172 x 90 and two dowel holes)", "Judgement", "fascia-01 spec (the clipped console)"],
])
prof_list("console", ["side_silhouette", "plan_at_neck", "eye_boss_upper", "eye_boss_lower", "leaf_outline"])
w("`volute_upper_spiral` (%d points) and `volute_lower_spiral` (%d points) are the open centrelines of the side grooves. **Fixings:** two 12 mm hardwood dowels 40 deep from the toe into the capital and two M10 coach screws through the back into the wall plate, all hidden; a rust bleed 20 long under each on the shaded side. **What P1 shows of consoles: nothing** (its pier caps are straight stepped blocks): the scroll, the grooves and the leaf are Judgement, marked as such in the evidence table, and the console is the FIRST piece to check against a reached photograph (section 16)." % (len(P["console"]["profiles"]["volute_upper_spiral"]["points"]), len(P["console"]["profiles"]["volute_lower_spiral"]["points"])))
w()

# ------------------------------------------------------------------------------------------------
w("## 7. Fascia board, bed mould, cornice")
w()
w("**Fascia board** (kit gets right: " + "; ".join(T["kit_vs_target"]["fascia_board"]["kit_gets_right"]) + "). Changes: " + "; ".join(x["what"] + " (" + x["reason"] + ")" for x in T["kit_vs_target"]["fascia_board"]["target_changes"]) + ".")
w()
fd = P["fascia_board"]["dims"]
table(["item", "value", "kind", "source"], [
    ["board", "u 295 to 5705 (5410), z 2850 to 3400 (550), face d 120, 25 thick on rails", "Read", "the fascia target (it fixes the board: the lettering and the texture are its); the kit"],
    ["bed mould", "z 2850 to 2890, front d 132 (12 proud of the face, 43 behind the capital's top front, 175)", "Judgement (Photo for the idea)", "P1's field is framed where it meets the capital"],
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
    ["oversail", "95 past the board's face, 10 past the console's front", "Derived", "215 - 120; 215 - 205"],
    ["corona face", "0 to 52 (0.35 of the height)", "Judgement", "P1's crown is not measurable by the method (section 3); the sequence of members is P1's"],
    ["ends", "a mitred return of the full 19-point section at each end, 215 deep back to the wall (a 45 degree mitre in plan from u 269 to the nose corner at u 54; right end 5731 to 5946); the nose line keeps u 54 to 5946; the lead dressed down over the return with a 25 upstand", "Judgement", "the review's fault 8: two exposed ends at each of nine party walls, seen end-on from the street; check COR-06"],
    ["wash", "falls %.1f degrees from d 205 at z 130 to the back at 150; lead 1.8 over it, an apron 100 up the wall, upstands 25 at each end (not geometry)" % cd["wash_slope_deg"], "Judgement on a Read", "fascia-01: 27 degrees; the 4.5 degrees of change is for the new profile"],
    ["stops short of each party line", "54 (108 between neighbours; the pipe is 68)", "Derived", "fascia-01's arithmetic"],
    ["tall variant", "300 high x 280 deep (z 3400 to 3700): offered for a reviewer who wants a heavier crown; no photographic basis (the crown is not measurable); collides with the signs' brackets at 3.60", "Judgement", "D7"],
])
prof_list("cornice", ["section", "return_left_uz", "return_right_uz", "plan_front_run", "plan_return_left", "plan_return_right"])

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
    ["bottom seat", "z 600 to 625: a 25 mm seat (the glazing rebate's foot and its bead); the lights stand on the sill", "Photo (P1's sill-group top is the glazing rebate's foot) and Judgement", "the first try's 90 mm bottom rail withdrawn: the shop door's glass (600) and the window's (625) run on together"],
    ["lower lights / transom / toplights / head", "625-2400 / 2400-2480 / 2480-2790 / 2790-2850", "Read", "scene transom 2.40, 0.08; kit head"],
    ["jamb", "50 face x 95 deep, glazing rebate 12 x 12", "Read (kit 50, 85) / Judgement", "frame fronts at d 95 sit 45 behind the shaft's 140"],
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
    ["leaf / slot / thickness", "900 x 2040 / 1006 / 50; the leaf's foot stands at z 28 (the threshold's 25 + 3 clear)", "Read (scene, kit) / Read (Ellis 2 in)", "z values below are heights above the footway, as the sill's 600"],
    ["rails and stiles", "stile 115, top rail 115 (1953 to 2068), bottom rail 0-230 (202 clear above the leaf's foot: 9 in, Ellis), lower panel 230-490 raised and fielded, lock rail 490-600, **glass 600-1953**", "Read (Ellis) / Photo and Judgement", "D2: P1's glass foot 0.304 of its leaf, 46 below its sill; Coventry: the bottom panel the stallriser's height; the scene's 1000 loses"],
    ["door glass against the sill", "the glass foot (600) = the window's sill top (600): one line along the front; the window's lights start at 625 on a 25 seat", "Photo and Read", "check DOR-06, per shop with a T1 or M2 door; the aluminium (M1) doors are glass from the bottom rail"],
    ["glazing", "one 6 mm pane, ovolo bead 14 x 11 (T1)", "Judgement", "-"],
    ["kick plate / foot strip", "T1: brass 770 x 170 with 8 screws, and a brass strip 30 high 3 proud across the leaf's foot = the plate's lowest 30 (one piece in use); M1, M2: the strip alone", "Read (kit) / Photo (29 mm, P1)", "the review's note: choose or say the strip covers the plate's foot: it does"],
    ["furniture", "lever handles on 240 x 40 backplates at z 1000; a rim latch and a mortice escutcheon at 950; **letter plate 250 x 40 centred on the leaf at z 545 in the lock rail** (525 to 565: 35 clear above and below, below the glass)", "Read (kit) / Judgement and Sheet", "the game's Rita door has the plate in the lock rail; the first try's z 800 stood in the glass"],
    ["hinges and handing", "three 100 x 75 butts at 150 / middle / 150, 6 No. 8 screws each; the shop door hinged on the window side with its lever on the opposite edge; the side door on the shop-door side with its knob on the pier side; a plate centred on each leaf; mirrored where the doors are on the viewer's right (`shops[].shop_door_hinge_viewer` and the other fields; check DOR-07)", "Read (kit) and Sheet (the game frame)", "section 17, fault 6, and `game_today`"],
    ["frame and threshold", "jambs 50 x 100, leaf 3 clear; terrazzo threshold 25 high at the leaf falling to 12, nose out to d 130 (flush fronts)", "Read", "kit"],
    ["fanlight, transom, toplight", "fanlight 2131 to 2400 (one pane); the shop's transom runs across 2400-2480; a two-bar toplight 2480-2790; head 2790-2850", "Read", "kit"],
    ["variants", "T1 timber glazed from 600; M1 aluminium glass door 50 stiles, 100 top rail, 170 bottom rail, a 300 chrome D pull; M2 bronze with a bronze kick panel to 600 and glass above", "Judgement", "-"],
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
w("**Roller-shutter box.** The four Poly Haven shutters read today have hoods 153, 168, 300 and 300 deep for curtains 1546, 1561, 1851 and 2400 high, the curtain's plane at z 20 and rails 7 wider than the curtain. The target's newsagent shutter (the review's fault 7): a **hood 300 high x 210 deep** under the fascia (z 2550 to 2850, u 350 to 4706) hiding the toplights above 2550 (70 shows), **set into the toplight zone: the window's and the shop door's head, the toplight bars and the toplight glass are cut away at z 2550 behind it** (the drawing clips them; the overlap test now includes the hood; ALT-09); two **guide rails 50 wide x 40 deep at d 150 to 190**, z 0 to 2550, standing out in front of the frames on steel spacer brackets bolted through the frames into the pilaster core (bolt heads visible); the **curtain in one plane at d 170**, 20 clear of the sill's nose (150), running across window and door to the footway, clear of the stallriser (125), threshold (130), transom and door frames (100) and mullions (92). Raised by day (the hood and the rails only); lowered at night (variant `shutter_down`). The first try's curtain at d 30 stood inside every frame. Check ALT-07; the drawing `roller_shutter_section` shows the lowered curtain against the sections.")
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
                 "window %.3f, side %s" % (s["centres_street_x_m"]["window"], s["centres_street_x_m"]["side_door"]),
                 "shop door hinged %s, lever %s%s; door glass foot %d (%s)" % (s["shop_door_hinge_viewer"], s["shop_door_lever_viewer"], ("; side door hinged %s, knob %s" % (s["side_door_hinge_viewer"], s["side_door_knob_viewer"])) if s["side_door"] else "; no side door", s["shop_door_glass_foot_z"], "level with the sill" if s["door_glass_rule_applies"] else "aluminium: from the bottom rail")])
table(["id", "pilaster", "console", "shop door", "alterations", "zones (mm)", "street x (m)", "hinge sides (viewer's L or R) and door glass"], rows)
rows = []
for s in T["shops"]:
    pn = s["paint_names"]
    ps = s["paint_srgb"]
    def cc(k):
        return "%s %s" % (pn.get(k, "-"), ps.get(k, ""))
    rows.append([s["id"], cc("pilaster"), cc("fascia_board"), cc("stallriser"), cc("window_frame"), cc("shop_door"), cc("side_door") if s["paints"].get("side_door") else "none"])
table(["id", "piers, consoles, cornice", "fascia board", "stallriser", "window frame", "shop door", "side door"], rows)
w("**Why these.** The trades and bays are Jafar's (3 October). Rita's is the model he called the best thing on the page. The refits follow the street's recipe where it has one (Mickey's slate steel front on patterned tile; the fish shop's, the chandler's metal fronts with plain glazed tile) and the fascia target where it fixes a date (the grocer's glass board means a 1930s refit; the laundry's and newsagent's box signs mean 1980s additions; the tea room's flat panel a 1980s caff). The empty unit is the one front nobody repainted. Four of ten are original timber repainted (Rita's, tea, ironmonger, newsagent) and the empty unit is original and derelict; five are altered. Departures from the recipe or the fascia target are in section 16. The newsagent\'s board is the fascia target\'s old cream board (the review\'s fault 9); its piers, consoles and cornice stay dove grey.")
w()
w("**Paints.** Every colour is an aged 1990 sRGB value with a plain name; the source or kind is in `paints.<id>.note`. Rita's oxblood (93, 46, 49) is the fascia target's aged oxblood; the whole palette is in the JSON (%d entries)." % len(T["paints"]))
w()

# ------------------------------------------------------------------------------------------------
w("## 14. Photographs win: each disagreement and what was chosen")
w()
table(["id", "element", "book or scene", "photograph", "chosen"], [[x["id"], x["element"], x["book_or_scene"], x["photograph"], x["chosen"]] for x in T["disagreements_photographs_win"]])
w("**Ratio rules** (target.json `derived_rules`; self-check group 2 recomputes each):")
w()
table(["rule", "photograph", "target", "within", "reading"], [[r["id"] + " " + r["name"], ("%s to %s" % (r["photo"], r["photo_high"])) if r.get("photo_high") else r["photo"], r["target"], ("yes" if r["within"] else "NO") + ("" if r.get("followed", True) else " (not followed)"), r["reading"]] for r in T["derived_rules"]])

# ------------------------------------------------------------------------------------------------
w("## 15. Checks, previews, drawing, self-check")
w()
w("**Checks for unit 3.2** (`checks`, %d of them; each has a name, what to measure, the expected value and a tolerance): the pilaster (slot, plinth top 600, plinth proud 180, shaft proud 140, neck, capital top 350 x 175, panel and flute numbers, the pair's gap and the downpipe chase, profile fit including the stepped plinth's head and the base ogee, **the shaft's relief of at least 40 in front of every frame beside it**, the plinth head, the base ogee), the console (envelope, centre, foot on the capital, top at the cornice's soffit, silhouette, leaf, **the two volutes, the waist and the cap block, the grooves and eye bosses**), the fascia and cornice (size, foot on the abacus, bed mould, oversail, soffit gap, profile, stops, **the closed mitred return at each end**), the sill, stallriser (**STA-03 as its variant adds up**), window frame (transom, head, mullion section and positions, glass plane, length per shop), the shop door (leaf, glazed from 600, slot, foot strip, **furniture [1000, 545], door glass level with the sill per shop, hinge and lever side per shop**), the side-door slot (944, F1's head meeting the transom, frame face d 100, the threshold's nose d 130), the zones filling 5300, the alterations (**the shutter's hood 210, rails d 150 to 190, curtain plane d 170 clear of every frame**; the newsagent's cream board), and per shop the door end, zones and street x of the window and the side door (the fascia target\'s own numbers). Materials: at most three plain PBR materials per piece, no textures, paint a per-shop parameter. No lettering, no maker\'s mark." % len(T["checks"]))
w()
w("**Previews** (`production/previews/cloud-week/refs/shopfronts/`, JPEG, at most 1200 px, under 300 KB; for the reviewers; the photograph is Andreas Mischok's Leadenhall Market HDRI, CC0, taken 2019-05-19, polyhaven.com; the crops show joinery only; the house numerals are masked, the shop door's glass above its foot and everything seen through the shop window beside the pier are filled flat; no business is named; the drawings are the studio's own):")
w()
table(["file", "what"], [
    ["`P1-leadenhall-pilaster-plinth.jpg`", "the plinth's stepped members, the hollow-moulded head and the band, and the foot (350 x 700 px at the virtual 2400 px focal length; a logo fragment masked top left)"],
    ["`P1-leadenhall-pilaster-capital.jpg`", "shaft top, necking ledge, die with three roundels, flared cap, top band; the shaft's return to the right"],
    ["`P1-leadenhall-pier-fascia-cornice.jpg`", "the pier head under the fascia and the crown (numerals masked)"],
    ["`P1-leadenhall-cornice-run.jpg`", "the continuous crown to the right of the pier"],
    ["`P1-leadenhall-sill-stallriser-stile.jpg`", "sill group, framed stallriser panel, foot rail, stile"],
    ["`P1-leadenhall-transom-mullion.jpg`", "the mid transom bar and the central mullion"],
    ["`P1-leadenhall-shop-door-glass-foot.jpg`", "NEW: the shop door's glass foot (row 128.9), lock rail, lower panel and brass foot strip; the glass above row 118 is filled flat so that rows 128.9, 531.6 and 547.0 are re-measurable"],
    ["`P1-leadenhall-pier-elevation.jpg`", "NEW: the whole pier strip, foot to crown, in three tiles side by side (rows -2340 to 640 of the virtual view, 1 px to the pixel); everything seen through the shop window filled flat"],
    ["`P1-leadenhall-*-target-on-photo.jpg`", "the drawing (cyan) laid on each crop: bands built from the measured rows and columns, at the scale fitted on one dimension"],
    ["`P1-leadenhall-pier-elevation-ritas-on-photo.jpg`", "NEW: the target's own Rita elevation (pilaster, console, board, cornice in cyan; sill, seat, transom and head in yellow at the window plane's scale) laid on the pier strip at the shaft's width; the differences are tabled below"],
    ["`D1-ritas-bay-elevation.jpg`", "the target's elevation of Rita's whole bay (drawn at 1 mm to the pixel, reduced), with the neighbours' pair of pilasters and consoles in grey and the downpipe between: the door glass level with the sill, the letter plate in the lock rail, the levers and hinges"],
    ["`D2-ten-fronts-sheet.jpg`", "the ten fronts assembled from the table, now with the empty unit's whitewash, the laundry's box sign, the newsagent's box sign and shutter hood, the tea room's panel and the grocer's slabs"],
    ["`D3-parts-pilaster-console-fascia.jpg`", "four pilaster variants, the scrolled console's silhouette and front, the capital / console / fascia / cornice section"],
    ["`D4-parts-sections.jpg`", "sections at x0.3 to x3: sill, transom, stallriser, plinth cap, stepped plinth head, base ogee, capital, cornice, fascia, mullions, jamb, bead, threshold"],
    ["`D5-cornice-ends-and-shutter.jpg`", "NEW: the cornice's mitred returns in plan at a party-wall gap, and the roller shutter's lowered curtain against the frames in section (the hood set into the toplight zone, the head cut away)"],
])
w("**Rita's elevation on P1** (the review's narrow point; `photo.rita_vs_p1`; self-check group 4 checks the overlay's one scale: her shaft is as wide as P1's). Where they differ:")
w()
table(["item", "Rita's target", "P1", "reading"], [[r["item"], r["target"], r["p1"], r["reading"]] for r in PH["rita_vs_p1"]])
w("**Credits.** P1: Andreas Mischok, Leadenhall Market, CC0 (Poly Haven), taken 2019-05-19. P2 (numbers only; no picture kept): Poly Haven rollershutter models, author MP, CC0, published 2023-10-11. The drawings are LEDGER's own.")
w()
if SELF:
    w("**Self-check (%s):** **%d of %d checks pass; %d fail; %d departures reported and kept in the open.** Groups: " % (SELF["date"], SELF["passed"], SELF["total"], SELF["failed"], SELF["reported"]) + "; ".join("%s %d pass %d fail %d reported" % (k, v["pass"], v["fail"], v["report"]) for k, v in sorted(SELF["groups"].items())) + ".")
    w()
    w("The groups: 1 printed (the numbers read again from SCENE-SLOTS.md, fascia-01's recipe, the kit README, the fascia target, the front-door target, and the hinge sides read off the game's Rita frame by colour); 2 photo (every row and column re-measured on the saved previews; the scale and the ratio rules recomputed); 3 wins (each disagreement recomputed); 4 overlay (the drawing's edges on the previews, worst %s px of %s edges; and Rita's elevation laid on the pier at one scale); 5 consistency (profiles are simple counter-clockwise polygons; the parts add up; the ten fronts' zones; nothing overlaps that should not and nothing floats in any of the ten drawings; paints, shops, alterations and checks well formed; the content rule); 6 faults (eighteen deliberately broken copies, each noticed)." % (SELF["stats"].get("overlay_worst_px"), SELF["stats"].get("overlay_edges")))
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
w("Also: the fascia target's boards and glass lettering, the front-door family's F1 door, the wear target's layer and the shop-room's displays are not re-done here; where this target touches them (the board's plane and bed mould, the F1's mapping and hinge side, the splash band on tiled and slab stallrisers, the sill's display bed) it says how.")
w()

# ------------------------------------------------------------------------------------------------
w("## 17. The second try: the review's eleven faults, and how each was answered")
w()
w("`TARGET-REVIEW.md` (a fresh reviewer, 9 October 2026) failed the first try with eleven faults. Every amendment is applied except the two below, where this target says why not. The reviewer's own re-run of the measuring tool reproduced every stored row to 0.00 px, so the faults were in which edges were snapped and how they were scaled, not in the tool.")
w()
table(["fault", "what was wrong", "how it was answered", "followed?"], [[str(f["n"]), f["fault"], f["answer"], str(f["followed"])] for f in T["review_faults_answered"]])
w("**The two places this target does not follow the review.**")
w()
w("1. **The plinth at 800 (the review's note after fault 3, and the profile of fault 3 at 800).** The review itself says P1's plinth 'breaks a line in the approved model: Rita's in the game today has the plinth top level with the stallriser'. Rita's window is Jafar's model, and P1's plinth rests on one market-hall pier (1.33 x its sill, R1). So the plinth stays at **600 on every front**; the photograph's 800 is kept only as the unused `variants.plinth_tall` with the review's profile points (150 to 180 in d). The head moulding the review found (a hollow and a band) is adopted at Rita's height, with the three lower blocks shortened (360 / 450 / 484 against P1's 504 / 631 / 684 on 800). **This is a conscious choice for the plan owner**: if he wants the photograph's plinth the variant is ready, and it is a visible change to his model.")
w("2. **The side door's hinge side (fault 6).** The review reads the approved model as 'the side door's knob is on its right, so it is hinged on the pier side'. The game frame (`rita-day-kit-2026-10-06.jpg`, 1600 x 900) shows the opposite: the side door's leaf spans x 215.7 to 397.3 and its two knobs stand at x 225.7 and 220.0, in the leaf's LEFT tenth (the pier side), and its letter plate (x 275 to 338) is centred on the leaf (centre 306.5). So the side door is hinged on the viewer's RIGHT, the shop-door side, and F1 (whose optional hinges the front-door target puts on its left stile) is mirrored where the door end is the viewer's left. The shop door agrees with the review: its lever (x 448 to 475) is left of its glass (x 457.7 to 604), so it is hinged on the window side. Self-check group 1 re-reads these positions from the frame by colour.")
w()
w("**The narrow points.** The group-4 overlay was circular; Rita's elevation is now laid on the re-projected pier at the shaft's width and the differences tabled (section 15). The laundry's aluminium refit (not in the street recipe's SHOPFRONT_REFITS) is listed beside the ironmonger, and the laundry's vent pipe through the fascia band is named as a fascias or town question (section 16). The kick plate and the foot strip are one piece in use (the strip is the plate's lowest 30). The drawings now show the empty unit's whitewash, the laundry's box sign, the tea room's panel and the grocer's slabs. P1's scale notice is England's statutory no-smoking sign, whose 2007 minimum size was A5: from memory (legislation.gov.uk unreached), which supports the A5 assumption.")
w()
# ------------------------------------------------------------------------------------------------
w("## 18. Fixes applied after the second review, by Jafar's ruling of 9 October, not re-reviewed")
w()
w("The re-review of the second try passed all eleven first faults and upheld both departures (the plinth at 600 and the hinge sides), and listed one fault and two narrow points with exact fixes. By Jafar's ruling of 9 October a target left with only listed faults and exact fixes gets those fixes applied and its self-check run, and is done as 'fixes applied, not re-reviewed'. Applied exactly:")
w()
table(["item", "what was wrong", "the fix"], [[str(f["n"]), f["fault"], f["fix"]] for f in T["fixes_after_second_review"]])
w("Self-check after the fixes: **%d of %d pass; %d fail; %d reported** (the reported lines now include the console's 205 against fascia-01's printed 180 and the base ogee's 15 against the kit's 25). Three more broken copies are noticed: the console pulled back behind the board, the hood left sharing the frames' space, the base ogee back at 25." % (SELF["passed"], SELF["total"], SELF["failed"], SELF["reported"]))
w()
open(os.path.join(HERE, "TARGET.md"), "w").write("\n".join(out))
print("wrote TARGET.md", len(out), "lines")
