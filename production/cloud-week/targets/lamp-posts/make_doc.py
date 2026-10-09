#!/usr/bin/env python
"""Writes TARGET.md from target.json (the numbers are read from it, not retyped) and the narrative below.

    /home/user/.bpyenv/bin/python make_doc.py        (run after make_target.py; run self_check.py; run this again to carry the last result line; run self_check.py again)
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, "target.json")))
N = T["numbers"]
V = lambda k: N[k]["value"]  # noqa: E731
G = T["geometry"]["A"]
LB = G["lantern"]
BR = G["bracket"]
LAST = T.get("self_check", {}).get("result_line", "(not yet run)")
LAID = (T.get("self_check", {}) or {}).get("laid_on_photograph") or {}
prof = G["lower"]["outer_rz"]
chk = {c["name"]: c for c in T["checks"]}
ZC0, ZC1 = prof[-3][1], prof[-1][1]
STEM_TOP = BR["stem_to_z"]
AS, AE = BR["arm_start"], BR["arm_end"]
TURN, RAKE = BR["bend_turn_deg"], BR["rake_deg"]
SCREW_Z = G["collar_screws"]["z"]
SW1, SW2, SW3 = chk["shaft_od_low"]["expected"], chk["shaft_od_mid"]["expected"], chk["shaft_od_high"]["expected"]


def table(rows, head):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "/") for c in r) + " |")
    return "\n".join(out)


chk_rows = [(c["name"], c["applies_to"], c["measure"], json.dumps(c["expected"]), c["tolerance"], c["kind"]) for c in T["checks"]]
num_rows = []
for k, v in N.items():
    if v["kind"] in ("Photo", "Derived"):
        num_rows.append((k, json.dumps(v["value"]), v["unit"], v["kind"], v["source"][:230]))

md = f"""# {T['title']}

**{T['summary_line']}**

Written 9 October 2026 for the family "lamp posts on Quay Street" (scene lines E1 lighting column and E2 sodium lantern, four of each). Units are millimetres unless a line says otherwise; the .glb is metres, z up, scale 1, the pivot the column's axis on the footway. `target.json` holds the same numbers for a script; `target_drawing.py` draws them (elevations, plans and sections as polygons in millimetres and pictures at 1 mm a pixel); `self_check.py` tests them; `make_target.py`, `lamp_numbers.py`, `measure_photos.py`, `make_previews.py` and `make_doc.py` re-make everything (the photographs themselves are Poly Haven's CC0 panoramas and are not in git). Last result: {LAST} (`/home/user/.bpyenv/bin/python -I self_check.py`; it re-measures the previews, runs the drawing, recomputes the derived numbers and tries ten deliberately wrong copies of target.json, all of which it must refuse).

## 0. Read this first

1. **No photograph of 1990 was reached.** The cloud's network refuses Wikimedia, Geograph, Flickr, archive.org and the rest (section 2.3). The only photographs reachable are Poly Haven's CC0 panoramas of London and Cambridge taken in 2019 (all by Andreas Mischok). Of the seventeen British ones, two show a steel lighting column well enough to measure (urban_street_01, called US01 below, and bethnal_green_entrance, BGE); none is shown to be older than 2019, and a 2019 column in Tower Hamlets may be a replacement. So nothing here is a 1990 measurement. What the photographs give is the FORM of a painted-steel stepped column and its bracket, the sizes of the lower column to +-7 %, the colour and wear of its paint, and the colour of a lit lantern; the rest is the project's earlier reading, the scene's numbers, or Judgement, each marked.
2. **The approved Hook sheet shows no lighting column.** The brief's "slender, dark column with a small flat canopy" is the RETIRED sheet's. The approved street panel (production/reference/hook-sheet.png, approved 22 September; its reduced copy production/previews/hook-sheet-2026-10-05.jpg) shows no lighting column and no bracket lamp: read at full size on 9 October, the only vertical on its skyline is a mast on the far hill, as production/reference/retired-sheet-inheritance.md row 4 and game-design/research/GOVERNS.md already say. So no number below is read off a Hook sheet; the sheet governs mood (section 3).
3. **Kinds of number.** Every number in `target.json` `numbers` ({len(N)} of them) carries its kind: **Read** (printed in the repository or in a file this writer opened, with the file), **Photo** (measured on a photograph: method and error in section 4), **Derived** (computed from other numbers here; the formula is in its `source`), **Judgement** (a trade or period guess, said so). `number_kinds` counts them: {json.dumps(T['number_kinds']['counts'])}.
4. **The choice that is Judgement:** painted steel (variant A) is the main build; the earlier research's precast concrete column (variant C) is written out but not built unless ruled in. Both share the bracket, the lantern, the light and the places.

## 1. What today's stand-in gets right, and what this target changes

Today's stand-in (SCENE-SLOTS.md; production/specs/vignette-scene.json `lighting`; StreetVignette.cs `Columns()`, read 9 October): a base cylinder 200 across and 300 high, ONE 114 mm shaft from 300 to 5000, a swan neck of three short cylinders (0.8 x the shaft) on a quarter circle rising over the lantern, a box lantern 550 along the street x 300 x 200 with its top at 5000 and its centre 500 from the axis, emissive, colour (255, 219, 0). "Trade-standard guesses, not photographs".

{table([
    ("the place", "x 8, 18, 28, 38; east, west, east, west; axis 0.6 m behind the kerb's back face", "the same (the code's loop; SCENE-SLOTS.md's 'every 20 m' is 20 m on one side)", "Read"),
    ("lower column", "base 200 x 300, then a 114 shaft to 5000", f"a 124 sleeve 978 high, a 60 mm cone with a ring line, a shaft 68 tapering to 60 at {ZC0:.0f}, a 67 collar to {ZC1:.0f}", "Photo (BGE), the scene's 114 lies at the sleeve's lower error edge"),
    ("bracket", "a swan neck: three cylinders rising over the lantern and dropping into it", "a plain bent arm: a 42 stem, one 90 mm bend, an arm raked 40 degrees into the lantern's rear boss", "Photo (US01) + Read (R07 'plain bent-arm lighting')"),
    ("lantern", "a box 550 along the street x 300 x 200", "a boat-shaped canopy over a deep yellowed bowl, the same 550 x 300 x 200 envelope turned so the long side lies ALONG THE ARM", "Photo (US01 from below) + Read (the research's wording)"),
    ("the glow", "one emissive box (255, 219, 0)", "the lamp (54 x 310) and the bowl glow; (255, 137, 0) and (255, 176, 28)", "Derived + Photo"),
    ("door, plate, fixings", "none", "a flush door 100 x 500 at z 400, a 90 x 45 plate 'LC n', two collar set screws, hinge and catches on the bowl, grub screws on the boss", "Judgement"),
    ("light", "one light 18 m range, intensity 3.2; scene colour (1, 0.7055, 0)", "the night note's pool, skirt and glow at (0, 500, 4850); colour (1, 0.25, 0)", "Read (night note)"),
], ("", "the stand-in", "this target", "kind"))}

What the stand-in gets right: the four places and sides, the mounting height 5.0 (the lantern's top), the outreach 0.5 to the lantern's centre, the lantern's box size, the 589 nm lamp, the point light 0.05 below the centre, and the rule that the column is plain steel with no ornament.

## 2. Sources

### 2.1 What was read, and what for

{table([
    ("S1", "production/specs/vignette-scene.json (lighting.column, lighting.lantern, street, blocks, cameras) and production/specs/vignette-pieces.json (column0..3, lantern0..3)", "2026-10-09", "the project", "the project's own", "2026-09-02 to 2026-10-08", "the stand-in's sizes and places; the lantern's colour, xy and range", "yes: Read numbers"),
    ("S2", "ledger/Assets/Scripts/Core/StreetVignette.cs Columns() (lines 1196 to 1262)", "2026-10-09", "the project", "the project's own", "2026-09", "the placement loop (x 8 while x <= 46, step 10, alternate sides, z = 3.125 + 0.6 = 3.725), the swan neck, the lantern's centre 0.5 out", "yes"),
    ("S3", "production/cloud-week/targets/SCENE-SLOTS.md; BRIEF.md", "2026-10-09", "the project", "the project's own", "2026-10-08", "the row for the lamp column; the brief's rules", "yes"),
    ("S4", "production/research/street-clutter-1990/SUMMARY-2026-09-29.md section 3 (the project's earlier reading, made on the PC from its sources)", "2026-10-09", "a helper, saved by the builder", "the project's own", "2026-09-29", "concrete columns with sodium lanterns; 4.6 to 6 m; 20 to 25 cm at the foot; a door plate about 50 cm up; an arm 40 to 45 cm; the lantern 7 3/4 in tall, 60 to 70 cm long (uncertain); a boat-shaped canopy over a deep clear trough bowl with a U-shaped tube; 'photographs 1985 to 1995 not found'. Its photograph links are links only (Geograph, Flickr, a lighting enthusiasts' site), all unreached from this cloud; the makers it names are not repeated here and appear on nothing", "yes: Read numbers, with its caution"),
    ("S5", "production/research/evening-light-1990/SUMMARY-2026-09-29.md", "2026-10-09", "a helper", "the project's own", "2026-09-29", "589 nm (0.569, 0.430), about sRGB (255, 140, 0), linear about (1, 0.25, 0); warm-up; 35 W SOX 4,550 lm", "yes"),
    ("S6", "production/cloud-week/research/1c-night-pools-lumen.md and production/audits/night-2026-10-08/GATE-NIGHT.md; DECISIONS.md 7 and 8 October", "2026-10-09", "the night note's writer", "the project's own", "2026-10-08", "the lamp's lumens, the pool, skirt and glow, the cones, the colour, the clipped red, the 4.78 m", "yes: the light block"),
    ("S7", "production/previews/morning-night-evening-2026-10-08.jpg (the street at night now)", "2026-10-09", "the project", "the project's own", "2026-10-08", "the stand-in at night: slim dark columns with long gooseneck arms over small boxes; pools on the flags", "looked at; no number taken"),
    ("S8", "production/reference/hook-sheet.png (2048 x 1088, read in four tiles at full size), production/previews/hook-sheet-2026-10-05.jpg, production/reference/hook-sheet-2026-09-09-retired.png, hook-sheet-audit.md, retired-sheet-inheritance.md, game-design/research/GOVERNS.md, photographs.md", "2026-10-09", "the project", "the project's own", "2026-09-09 to 2026-10-05", "the approved sheet shows no column and no bracket lamp (section 3); the retired poster shows a black post-top globe lantern and two box wall lanterns, each a few pixels wide", "yes: section 3"),
    ("S9", "production/cloud-week/targets/kerbs-and-covers/ and bollards/ (target.json, TARGET.md)", "2026-10-09", "their writers", "the project's own", "2026-10-09", "the corrected kerb (granite top 170, flags +110) and the camera heights of BGE (1.02 +-0.07) and US01 (1.16 above the footway)", "yes"),
    ("S10", "https://polyhaven.com/a/bethnal_green_entrance (BGE); https://dl.polyhaven.org/file/ph-assets/HDRIs/extra/Tonemapped%20JPG/bethnal_green_entrance.jpg (8192 x 4096)", "2026-10-09", "Andreas Mischok", "CC0 1.0 (read at https://polyhaven.com/license, 9 October 2026: 'CC0 means absolute freedom')", "2019-08-18", "the Bethnal Green estate path; a black steel column with a post-top dish lantern at 4.4 m, 2.7 m from the camera", "yes: Photo numbers (sleeve, cone, shaft, pod width, paint, wear)"),
    ("S11", "https://polyhaven.com/a/urban_street_01 (US01); the same host's Tonemapped JPG urban_street_01.jpg", "2026-10-09", "Andreas Mischok", "CC0 1.0 (as S10)", "2019-08-18", "a steel stepped column about 11 m high with a bent-arm bracket and an amber lit cobra-head lantern, 8.8 m from the camera", "yes: ratios, the lit colour"),
    ("S12", "https://polyhaven.com/a/urban_street_02, urban_street_03, urban_street_04, birbeck_street_underpass, limehouse, cambridge, greenwich_park, greenwich_park_02, greenwich_park_03, epping_forest_01, epping_forest_02, roof_garden, canary_wharf, adams_place_bridge, leadenhall_market (the same Tonemapped JPG host)", "2026-10-09", "Andreas Mischok", "CC0 1.0", "2019-02-09 to 2019-12-17 (us02 2019-08-18; us03 2019-09-07; us04 2019-09-14; cambridge 2019-12-17; the parks 2019-02-09 to 2019-09-07; the rest 2019-05-19 and 2019-08-31)", "searched for lamp columns and wall lanterns (section 2.2)", "us02: a wall bulkhead measured (W1's note); the rest looked at only"),
    ("S13", "https://api.polyhaven.com/assets?type=hdris and https://api.polyhaven.com/files/<id>, /info/<id>", "2026-10-09", "Poly Haven", "CC0", "n/a", "the catalogue with coordinates and dates taken; the file URLs", "yes"),
], ("id", "where", "date read", "author", "licence", "date taken", "what it shows or gives", "used"))}

All Poly Haven material is used for measuring and looking only: not placed in the game, not traced into a texture, not fed to an image model.

### 2.2 The search of the panoramas

Poly Haven lists seventeen HDRIs with coordinates in Britain (the Dublin sets at 53.3 N 6.2 W are not British and were left out; `st_fagans_interior` is a Welsh interior). Each of the seventeen was looked at as its 2k tone-mapped copy and, where a column showed, at 8192 px:

{table([
    ("urban_street_01", "one steel stepped column with a bent-arm bracket and a lit amber cobra-head lantern (US01)", "measured: ratios, lit colour, form of bracket and base"),
    ("bethnal_green_entrance", "one black steel stepped column with a post-top dish lantern, 2.7 m away (BGE), signs bolted on its shaft", "measured: the lower column, the pod's width, the paint and wear"),
    ("urban_street_04", "a decorative black column with a scroll bracket and a round glass lantern (Kensington)", "looked at: a 2000s heritage replacement, wrong for 1990 and for a northern port; not used"),
    ("urban_street_03", "one steel column with a raked arm, 6 px wide at 40 m", "looked at; too small to measure"),
    ("urban_street_02", "a black-backed opal wall bulkhead on a 1970s-80s brick block", "measured roughly (235 x 210 mm, brick courses): an estate fitting, W1's note"),
    ("cambridge", "two bespoke wrought-iron glazed wall lanterns of a college", "looked at: a one-off heritage piece, not a street fitting; a college's sign is in frame, so no preview"),
    ("birbeck_street_underpass, limehouse", "fluorescent battens under a viaduct; bollards and chain on a marina", "no column"),
    ("greenwich_park, _02, _03, epping_forest_01, _02, roof_garden, canary_wharf, adams_place_bridge", "parks, woods, a roof garden, offices, a footbridge", "no column"),
    ("leadenhall_market", "a covered market with ornate hanging lamps and shop lettering the content rule bars", "not used and not previewed (the content rule)"),
], ("panorama", "what it shows", "result"))}

None of the lamp columns is shown to be from 1990 or earlier, and none is a concrete column. The brief's expected case ("if no reachable photograph shows a period column, write the target from the earlier research, the existing recipe and the Hook sheet, and say plainly which numbers rest on what") is therefore the case, with the difference that the Hook sheet gives nothing and two 2019 photographs give the lower column's form.

### 2.3 Unreached

Wikipedia, Wikimedia Commons, Geograph, Flickr, archive.org, HathiTrust, the National Archives, Historic England, legislation.gov.uk, and the lighting enthusiasts' and makers' sites the earlier research cites: `curl` returned 000 (refused at the proxy) on 9 October 2026, 20 s each. Nothing was taken from any of them. WebSearch was used only for the leads of section 2.4; no number was taken from a search summary.

### 2.4 Leads (WebSearch summaries of 9 October 2026: leads, never numbers)

{chr(10).join('- ' + l['text'] + ' (' + l['via'] + '; ' + l['effect'] + ')' for l in T['leads'])}

## 3. The Hook sheet and the column

The brief says the Hook sheet's foreground column is slender and dark with a small flat canopy, and that tools/art-recipes/lighting-column.py records that crop. The recipe's own notes say the crop is the RETIRED Codex sheet's (production/art/atlas-01/concepts/hook.png on a branch that is not in this checkout; "three traces of one lamp crop gave three answers"), that the approved pass 4 street panel "shows NO street lighting column anywhere in it", and that the column's shape is "governed by R07's 1989 photograph, 'plain bent-arm lighting'" (production/reference/photographs.md; a Hull photograph that is under photographer copyright and was not reached). This writer re-read the approved sheet at full size in four tiles: it shows the brick terrace, the wet street, parked cars, and no lighting column and no wall lamp (a small white fitting at the gable's corner and the dish above Mickey's fascia are not lamps). The retired in-house poster (688 x 1024) is an image model's drawing from a prompt that asked for a pub (retired-sheet-inheritance.md): its post-top lamp's pole is 3 to 4 px wide and its two box wall lanterns are about 20 x 40 px, so there is nothing to measure (hook-sheet-audit.md: under about four pixels is noise) and, being a pub's, nothing citable.

So: the sheet governs mood (wet, grey, low contrast, dark metalwork) and the night frame's pools, and decides nothing about the column's shape. The slot overlay `hook-sheet-slot-x8-east-target-on-sheet.jpg` lays variant A at its scene slot (x 8, east) on the sheet's reduced copy with the sheet's own lens (production/reference/hook-sheet-lens.md; the scene's cam_hook: x -3.0, z -1.6, eye 2.2, yaw 20.4, pitch -3.4, 46 degrees vertical): it checks scale and place, not a measurement. The lens puts Mickey's pilasters within 45 px of the sheet's on 1600, as the lens note says; the sheet draws the east footway visibly wider than the scene, so the column's foot lands at the shopfronts' base rather than at the kerb, and its top stands above the sheet's first-floor window heads although 5.0 m is under the scene's 6.3 m eaves: the sheet's terrace is drawn lower than the scene's. The sheet is a picture an image model made; the target does not follow it there.

## 4. How the photographs were measured

**Camera heights.** The panoramas record none. This target uses the heights the bollards' target measured and its reviewer re-measured, each at the object's own ground (production/cloud-week/targets/bollards/TARGET.md section 3): **BGE 1.02 +-0.07 m** (brick-course horizon method on the planter wall of the same block paving; the writer 0.96, the reviewer 1.03 to 1.04) and **US01 1.16 +-0.07 m above the footway** (the garden wall and gate pier; 1.23 above the bed). Every BGE and US01 length is therefore **+-7 % in absolute size**; proportions are exact to the pixel. If BGE's sleeve is the standard 114.3 mm tube, the camera was 0.95 m (this writer's own horizon fit gave 0.96) and every BGE length is 7 % smaller; the stated error covers it.

**Distance.** The column's horizontal distance gives the picture its scale. BGE: the sleeve's front foot at row 2524 of 4096 (-20.9 degrees) gives 1.02 / tan 20.9 = 2.665 m; its radius 0.062 puts the axis at 2.73 m, bearing 138.5 degrees; the base then appears at z = -23 mm in the elevation, as the geometry says. US01: the column's foot is hidden by a car; the gate pier beside it gives 8.4 m and the lowest visible sleeve point 9.2 m: 8.8 +-0.6 m, so only RATIOS are taken from US01 (its column is an 11 m class).

**Re-projection.** `lamp_lib.elevation` makes a flat, square-on picture of the vertical plane through the column's axis at a stated millimetres a pixel (1.2 mm for the BGE strips, 3 mm for US01); edges are found by the strongest luminance gradient in a window round the expected edge (`measure_photos.py`; raw rows are in `photo_measurements.json` and copied into target.json). The native resolution is 2 mm a pixel at 2.7 m and 7 mm at 8.8 m.

{table([
    ("BGE sleeve OD", "123.6 (rows 120 to 128, z 100 to 800)", "+-9", "124"),
    ("BGE sleeve's straight side ends", "z 978 (read on a 4 x gridded crop)", "+-10", "978"),
    ("BGE cone top, a thin ring line", "z 1035 to 1040", "+-10", "1038 (ring 6 tall)"),
    ("BGE shaft OD", "66 (z 1100, by eye), 67/69/69 (z 1700 to 1900), 61/61/61 (z 3800 to 4000)", "+-6", f"68 at the cone, 60 at {ZC0:.0f}"),
    ("BGE pod, widest run", "417 (x -193 to +223)", "+-30", "420 (variant P)"),
    ("BGE pod's centre height", "4410 from the limbs' angles (53.8 and 48.5 degrees)", "+-300", "4375 (P)"),
    ("BGE paint, median sRGB", "sleeve 31/31/33 (p10 19, p90 44); lowest 250 mm 49/46/42; shaft 44/45/51 (sky-tinted)", "+-3", "31/31/34; splash 49/46/42"),
    ("US01 shaft top / stem / arm", "89.1 / 42.0 / 59.9", "+-8 / +-5 / +-6", "ratios 0.47 to 0.67; stem OD 42"),
    ("US01 sleeve / shaft", "232 / 113 at 8.8 m (by eye): 2.05", "+-0.2", "BGE's own 1.8 used"),
    ("US01 lit lantern, median sRGB (66,611 orange pixels)", "251/152/14 (p10 229/105/0, p90 255/208/77; the clipped core 252/251/180)", "+-8", "bowl (255, 137, 0); lamp (255, 176, 28)"),
], ("measurement", "reading", "error", "the target's value"))}

**The drawing laid on the photograph.** The overlay `bge-bethnal-green-column-target-on-photo.jpg` draws target.json's lower column (the sleeve, cone, ring and shaft, z 0 to 4280) over the four BGE strips at a scale fitted on ONE dimension only, the sleeve's width (123.6 measured, 124 in the target: scale s = {LAID.get('scale_s', 'n/a')}). The self-check re-measures the preview and tests it: the sleeve's two edges over {LAID.get('rows_sleeve', '?')} rows, mean absolute error {LAID.get('sleeve_edge_mean_abs_mm', '?')} mm (none over 8; the pixel is 1.2 mm); the shaft's width over {LAID.get('rows_shaft', '?')} rows, median absolute error {LAID.get('shaft_width_median_abs_mm', '?')} mm, upper quartile {LAID.get('shaft_width_p75_abs_mm', '?')} (the rows against the sky are within 2 mm; the rows against ivy and brick scatter); the cone and ring by the same method, with the ivy behind them confusing the edge finder (the picture shows the fit). Above z 4300 the photograph's column carries a post-top pod (variant P), not A's collar and bracket, so no outline is drawn there.

## 5. The target, part by part (variant A, the main build)

### 5.1 Frame

Origin on the column's vertical axis at the footway surface; **+y points at the carriageway** (the lantern side), x runs along the street, z up. For the west side's columns the whole piece is turned 180 degrees about z so that +y still points at the road. The column stands plumb (the footway falls 1 in 40, 3 mm across the sleeve). The pivot is the axis at z = 0; the sleeve runs 150 mm below it (hidden) so that the footway's fall never shows a gap. One mesh for the column, one for the lantern (the lamp and the bowl as emissive material slots).

### 5.2 The lower column: sleeve, cone, shaft, collar

Profile (radius, z) in mm, revolved about the axis (`geometry.A.lower.outer_rz`, authoritative):

{table([(f"({p[0]}, {p[1]})", d) for p, d in zip(prof, ("axis at the hidden foot", "hidden skirt: sleeve radius", "sleeve top: the straight side ends (Photo, BGE 978)", "cone top, shaft radius 34 (OD 68)", "the weld ring: 1.5 proud ...", "... 6 tall (z 1038 to 1044)", "back to the shaft", f"shaft radius 30 (OD 60) at the collar's foot (z {ZC0:.0f}): a straight taper of 2.3 mm a metre", "collar radius 33.5 (OD 67)", f"collar top (z {ZC1:.0f})", "the axis"))], ("(r, z)", "what"))}

- **Sleeve** 124 across (Photo, +-9; the scene's 114 is at its lower error edge and 114.3 is a standard tube: the tolerance covers it), 978 high above the footway and 150 below it. A 1 mm groove round it at z 978 where the cone cap is welded on (Photo: a dark line under the cone).
- **Cone** 60 mm tall, 24 degrees off the vertical, from OD 124 to OD 68; **ring** 1.5 proud and 6 tall at its top (Photo: a thin ring line there).
- **Shaft** a plain round steel tube tapering in one straight line from OD 68 at z 1044 to OD 60 at z {ZC0:.0f} (Photo: 66 to 69 at z 1.1 to 1.9 m, 61 at z 3.8 to 4.0 m). A longitudinal weld line 1.5 wide and 0.5 proud on the -y face (Photo: a faint vertical line near the edge; qualitative). No flutes, no ornament, no finial.
- **Collar** OD 67, z {ZC0:.0f} to {ZC1:.0f}, the bracket's socket (US01 and BGE end in a short collar a little wider than the shaft; qualitative). Two M8 socket set screws, round heads 10 across and 3 proud, at z {SCREW_Z:.0f}, azimuth 45 and 135 degrees from +y (Judgement).
- **Root.** The sleeve runs straight into the footway: the paving is cut round it with a 10 to 15 mm joint of dark grit mortar; no base plate, no collar, no bolts show (Photo, BGE: block paving cut round the sleeve, no plate).
- **Door** (Judgement; the research says "a door plate about 50 cm up", US01's sleeve shows a rectangular door outline whose top edge is at about 86 % of the sleeve's height, and a search lead, never a number, gives a 500 x 100 door opening 400 above the ground on a modern 5 m stepped steel column; the sleeve's 978 holds a door from 400 to 900): on the -y face (away from the carriageway), a curved plate rolled to the sleeve, **100 mm of arc (92 degrees) by 500 tall, z 400 to 900, 1.5 proud**, a 2.5 wide and 2 deep joint groove (black) all round it, two round-headed hex-socket captive screws 12 across and 2 proud on its centre line at z 425 and 875, no hinge showing, no lock, **no lettering and no plate on it** (the leads say real doors of the kind could carry a maker's mark: ours is blank).
- **Number plate** on the +y face of the shaft at z 2160 (BGE has a larger flat reference plate at z 2115 to 2200, 125 x 85, white with black letters: a sign's, not copied): a curved aluminium plate **90 x 45 x 1.2** wrapped on the shaft (65 across seen square on), 1.4 proud, two domed rivets 5 across at 8 from each end, white (214, 212, 205) with black (30, 30, 32) upright sans letters 24 high reading **LC n** (n = 1 to 4, the column's number in the street). Generic: no authority's name, no crest, no maker.

### 5.3 The bracket

A plain bent arm of one tube, **OD 42** (US01: the stem is 0.47 of the shaft's top and the arm 0.67; this slimmer 4.6 m shaft's top is 60, so 42 is 0.70), in the y-z plane: it rises vertically from inside the collar (its lowest 60 mm are inside it) to z {STEM_TOP:.0f} (80 above the collar's top), turns through **{TURN:.0f} degrees on a centreline radius of 90** to a straight arm **raked {RAKE:.0f} degrees above horizontal** (the bend ends at y {AS[0]:.1f}, z {AS[1]:.1f}), and runs straight {BR['arm_length']:.1f} mm to its end at **y 225, z {AE[1]:.1f}**, inside the lantern's rear boss (the canopy's lip band is z 4925 to 4937). The centreline is stored at 40 mm steps on the stem, 6.25 degrees on the bend and about 35 mm on the arm (`geometry.A.bracket.centreline_yz`).

Where the numbers come from: **US01's arm** (11 m column) shows 41.7 degrees in the picture's plane (fitted centreline over x -1150 to -350 of the 3 mm elevation; 43.6 over another range); the lantern seen from below is nearly side-on (its visible length 0.78 m of about 0.9), so the arm points within about 30 degrees of the picture's plane and the true rake is **36 to 44: 40 +-6** (Photo). The arm does not point much out of the plane: the lit view shows the lantern nearly full length. **The bend** on US01 is 435 mm in radius (tangent lengths 147 along the stem and 244 along the arm from their corner, the turn 48.3 degrees; about 9 arm diameters) on a reach from the stem to the boss of 1117 mm; scaled by the reach to this column's 225 it is 87.6, rounded to 90 (a tight bend: the 9-diameter bend of a big column cannot fit a short bracket). The stem's 80 mm and the collar's top at 4620 are Judgement chosen so that the arm arrives at the boss. A 5 m column's own rake is not photographed (this writer recalls standard raked brackets of 5 to 15 degrees; a search found no source for it, and a lead says 5 m brackets had a vertical and a horizontal section: the photograph is followed, the rake's tolerance is wide, and section 10 lists it).

### 5.4 The lantern

**Envelope 550 x 300 x 200** (the scene's box: Read), top at z 5000 (the mounting height), bottom 4800, centre (0, 500, 4900), **long side along y**, level. Photograph US01 from below shows the arm entering the lantern's rear end and the lantern lying along the arm; the scene had it along the street. All coordinates below are in the column's frame.

- **Canopy** (painted aluminium, shell 2.5): plan half-widths at y 225 / 230 / 245 / 270 / 300 / 340 / 400 / 450 / 520 / 600 / 670 / 725 / 760 / 775 = 0 / 30 / 58 / 86 / 108 / 128 / 144 / 150 / 150 / 146 / 134 / 108 / 62 / 0 (a boat: narrow at the rear where the arm enters, full and round at the front); a down-turned lip 12 tall from the rim z 4925 to z 4937; above it a half-ellipse dome whose crown follows z = 4937, 4962, 4990, 5000, 4998, 4985, 4963, 4945, 4937 at y = 225, 260, 320, 400, 500, 600, 680, 735, 775 (the dome is 61 high at y 500; the highest part, y 400 to 500, is the gear tray: **there is no separate gear box**). Underside white (226, 224, 216) reflector, with a lamp-holder 60 x 45 x 40 at the rear (x +-30, y 300 to 345, z 4852 to 4892).
- **Bowl** (clear acrylic, yellowed, shell 3, a 6 x 6 bead on its rim): rim at z 4925 following the canopy's plan 8 inside it (y 233 to 767); a flat refractor base at **z 4800, 400 long (y 300 to 700) and 164 wide**, plan half-widths 0 / 22 / 52 / 70 / 80 / 82 / 80 / 70 / 52 / 22 / 0 at y 300 / 303 / 320 / 350 / 400 / 500 / 600 / 650 / 680 / 697 / 700; the sides bulge outward from base to rim by the section at y 500 (half-width, z): (82, 4800), (90, 4806), (100, 4815), (118, 4842), (130, 4872), (138, 4900), (142, 4925); the ends follow the long section's rear curve (y, z): (233, 4925), (240, 4890), (262, 4850), (285, 4818), (300, 4800), the front its mirror about y = 500. `bowl.loft` gives the one formula that joins them. Fine prismatic grooves 2 mm apart across the base's underside. Hinged at the rear (two knuckles 22 x 22 x 14 at x +-60, y 262, on the rim) and closed by **two spring catches** 30 x 14 x 7 proud on the long sides at y 650, x +-136, on the rim line (Judgement; US01 shows only the canopy over a glowing bowl).
- **Lamp**: one glass jacket **54 across and 310 long** lying along y, centre (0, 500, 4872), a 35 W low-pressure sodium lamp (Judgement: a search lead lists 311 x 52 and 310 x 54, within 2 mm of these) with its lamp-holder at the rear end. The bowl's lit surface and the jacket are the only emissive parts.
- **Rear boss**: a cast sleeve **OD 60, 55 long**, axis from the arm's end (225, {AE[1]:.1f}) forward at {RAKE:.0f} degrees, a visible cast boss on the canopy's rear tip (its lower edge hangs up to 17 mm below the rim at its start and its upper edge stands 17 to 24 mm above the dome); two M8 round-headed grub screws 10 across, 3 proud, at 90 and 270 degrees about its axis.
- No photocell, no ornament, no ladder bar, no finial (the recipe's rule, kept).

### 5.5 Materials and paint

{table([(k, json.dumps(v.get('srgb') or v.get('srgb_unlit') or v.get('srgb_white') or v.get('emissive_srgb_lit')), v.get('name', ''), v.get('roughness_words', ''), v.get('roughness', v.get('roughness_new', '')), v.get('metal', ''), v.get('kind', '')) for k, v in T['materials'].items()], ("part", "sRGB", "plain name", "roughness in words", "roughness 0-1", "metal", "kind"))}

Painted steel is not metal for shading (metal 0: a painted surface); roughness 0.42 is the recipe's and the photograph shows gloss worn to semi-gloss (the upper shaft rougher by 0.15). The bowl's transmission 0.85, IOR 1.49 (acrylic). Concrete grey (146, 143, 136) belongs to variant C only. The only high-chroma surfaces are the lamp and the bowl: the paint, canopy, plate and primer are within 16 per channel of grey (the accent budget, art-direction R-B4).

### 5.6 Wear

State: a tired column, twenty years since it was last painted, in a port town's wet air. Placed per column by its seed; positions on the sleeve are on the **carriageway face (+y)** unless said.

{table([(w['id'], w['where'], w.get('kind', '')) for w in T['wear']['features']], ("feature", "where, how big, colour", "kind"))}

Not present: lettering graffiti, posters of this target's own (the posters target places bills and stickers on these shafts), reflective or coloured bands, a maker's plate.

### 5.7 The lit lamp: numbers that agree with the night note

The lamp is a 35 W low-pressure sodium lamp, 4,550 lm (Read: the night note, a maker's datasheet by search summary). The game's light for each column, at **(0, 500, 4850)** in the column's frame (the scene's rule: a point light 0.05 m below the centre of the emissive piece), is the night note's:

{table([
    ("pool spot (shadows on, straight down)", "500 lm, inner 22, outer 46 degrees: 261 cd, 11.4 lx straight down from 4.78 m", "350 lm, inner 15, outer 55: 130.6 cd"),
    ("skirt spot (no shadows, straight down, source radius 5 to 10 cm)", "none", "800 lm, inner 45, outer 80: 154.1 cd"),
    ("glow (all round, no shadows)", "40 lm (3.2 cd)", "40 lm"),
    ("sum straight down", "11.4 lx", "12.46 lx (the note's 'about 12.5')"),
    ("total lumens", "540", "1,190, 26 % of the lamp's 4,550 (the note cut the pool on purpose to cure the clipped red; it adds the skirt for the gaps)"),
    ("range", "18 m", "18 m"),
    ("colour (linear)", "(1.0, 0.25, 0.0)", "(1.0, 0.25, 0.0); the note's try (1.0, 0.40, 0.03) = sRGB (255, 170, 48)"),
], ("light", "current game (8 October)", "the night note's proposal (section 4 steps 4 and 5)"))}

The cone arithmetic (cd = lumens / (2 pi (1 - cos outer half-angle))) is recomputed in the self-check and reproduces the note's 261 cd, 11.4 lx and 12.5 lx. These are the note's intent, to be tried and measured in the game's own camera (its section 5); this target adds no number the note does not have.

**The colour, and the scene file's mistake.** The scene file's lantern is linear (1.0, 0.7055, 0.0), gamma (255, 219, 0), xy (0.5467, 0.4526), "589 nm". That xy is the colour of about **585 nm** (the printed CIE value at 585 nm is (0.5448, 0.4544); a multi-lobe fit of the colour matching functions, recalled from memory and checked against that value to 0.002, gives (0.5436, 0.4562) at 585 and **(0.5667, 0.4332) at 589**, (0.5684, 0.4315) for the sodium D lines). And its normalisation divided red by the peak but left green and blue undivided: clipped and divided by 2.3766 the scene's own xy gives (1.0, 0.2969, 0.0), not (1.0, 0.7055, 0.0). At 589 nm the same matrix gives (2.731, 0.600, -0.130), clipped and divided by its peak **(1.0, 0.2195, 0.0)** linear = **(255, 129, 0)**: the evening note's (255, 140, 0) and the night note's (1.0, 0.25, 0.0) are within 0.04 and 11. The night note says the game's lamp already is (1, 0.25, 0); the scene file is stale and wrong, and correcting it is a ruling (asked first).

**Glow surfaces.** Bowl: emissive (255, 137, 0) = the night note's lamp gamma-encoded (the lit US01 lantern's median is 251/152/14: within 15). Lamp jacket: emissive (255, 176, 28), brighter and yellower than the bowl (the photograph's clipped core is over-exposure; a sodium lamp's own light is one orange); the bowl at 0.45 of the jacket's brightness. The canopy, the arm and the column stay unlit paint, lit only by the pools. Warm-up (optional): a freshly lit lamp glows dim red-pink for a few minutes before turning orange (evening note section 1). Unlit by day: the bowl clear-yellowed (190, 182, 160) with the jacket (200, 196, 180) and the white reflector seen through it.

### 5.8 Placement

{table([(c['id'], c['x_m'], c['side'], c['scene_z_m'], c['corrected_z_m'], c['plate_text'], c['wear_seed'], 'yes' if c['dent'] else '') for c in T['placement']['columns']], ("column", "x (m)", "side", "scene z (m)", "z with the corrected 170 kerb (m)", "plate", "wear seed", "dent"))}

The code's loop gives four columns, **20 m apart on each side, 10 m apart along the street, alternating** (SCENE-SLOTS.md's "every 20 m" is the spacing on one side; the posters target's SF4 'x 8, 28, 48' misreads it: the street has columns at 8, 18, 28 and 38 and none at 48). The axis stands 600 mm behind the kerb's BACK face: the scene's kerb top is 125 wide so z = 3.125 + 0.6 = 3.725; the corrected granite kerb top is 170 so the same rule gives 3.77. The rule governs, within a 40 mm tolerance. The arm points at the carriageway, square to the kerb; the door faces the building line; the plate faces the road. The lantern's centre is 0.27 m behind the kerb face (0.5 out from an axis 0.77 behind it), so its pool lands on the flags and the channel.

### 5.9 Edges, bevels, size

Every hard edge is bevelled (mid-poly; the asset plan's method): {", ".join(f"{b['edge']} {b['radius']}" for b in T['bevels'])} (radii in mm). Triangle budget {T['triangle_budget']['lod0'][0]} to {T['triangle_budget']['lod0'][1]} per column with its lantern at LOD0 (Judgement; four columns are a small share of a frame).

## 6. Variants

{table([
    ("A", "steel bent-arm column (this document)", "main: 4 of 4 places", "all numbers above"),
    ("C", "precast concrete shaft, steel bracket and the same lantern", "alternative, built only if ruled in", "the research's type; NO photograph; every number Judgement or the research's: a square section 220 at the foot (the research's 20 to 25 cm) tapering to 125 at 4700, arrises chamfered 15, the shaft planted (150 hidden) with the paving cut round it; a door recess 120 x 330 x 14 at z 450 to 780 on the -y face with a steel door plate 132 x 342 x 3, 3 proud, two screws, blank; the bracket tube OD 48 entering the top face (top entry), the same bend, rake, boss and lantern; the plate 'LC n' as A; colour (146, 143, 136) with green algae to z 700 on the -y face and rust bleed from the plate's screws; no paint"),
    ("P", "post-top dish on the same lower column", "not placed (the scene's lamps are bracket lamps)", "what BGE shows: the lower column to z 4300 and a dish 420 across (Photo, +-30) of Judgement height 150 centred at 4375; shell dark, underside pale"),
    ("W1", "a wall bracket for the same lantern", "optional, not placed; if wanted, a plain gable end, never a shopfront", "Judgement only: a wall plate 150 x 220 x 8 with four bolts (domed nuts 24 across), a 42 arm raked 10 degrees from z 4350 to the lantern's boss at y 225 from the wall, a 25 strut from z 4130 to 140 along the arm; the lantern 540 lower than on A (top at 4460). The two wall lanterns reached are a one-off college lantern (Cambridge) and a 2019 estate bulkhead (US02, 235 x 210): neither is a street fitting"),
], ("id", "name", "build", "difference and basis"))}

How many the street needs: one column type per scheme (a street's lamps were fitted together), so the four places take A, or all four take C if ruled; the lantern is one pattern in both. The variation between the four is the wear (their seeds, the dent on LC 2), not the form.

## 7. The photographs-win disagreements

{table([(w['id'], w['what'], w['scene'], w['photograph'], w['chose'], w['kind']) for w in T['photographs_win']], ("id", "what", "the stand-in or book says", "the photograph or the record says", "chosen", "kind"))}

## 8. The checks for unit 3.8

`target.json` `checks` lists {len(T['checks'])}: each a name, what to measure, the expected value and the tolerance. Those that matter from the street are the lantern's box (550 x 300 x 200 +-8, centre (0, 500, 4900) +-12, long axis along the arm +-3 degrees, top at 5000 +-10), the sleeve (124 +-9, 978 +-15 high), the shaft's width at 1200, 2500 and 3900 ({SW1} / {SW2} / {SW3} +-6), the bracket (stem 42 +-4, rake 40 +-6, bend radius 90 +-40, end at (225, {AE[1]:.1f}) +-12), the door (100 x 500 at z 400 +-10, facing away from the road +-12), the plate, the colours (paint (31, 31, 34) +-12, the bowl's glow (255, 137, 0) +-12), no maker's mark and no lettering but the plate's, the light's place and numbers, and the four places. The profile and silhouette checks are two-way nearest distances (every point of the built outline to the target's outline and back, at most 4 to 6 mm), as the pillar box's.

{table(chk_rows, ("name", "applies to", "measure", "expected", "tolerance", "kind"))}

## 9. What the self-check does

`self_check.py` (A to E and W): **A** every printed number comes back from its file (the scene, the pieces file, the code's loop, the earlier research, the evening and night notes, DECISIONS.md, the kerbs target) and every derived number recomputes (the colour matching functions' fit, the 589 nm colour, the cone arithmetic); **B** the raw photograph rows give the printed numbers; the numbers are re-measured from the reduced previews; the lower column is laid on the BGE strips at a scale fitted on the sleeve alone and its edges fall on the photograph's within the stated error; **C** the drawing runs on target.json alone and its polygons give the target's numbers; **D** the bracket's geometry recomputes, nothing floats (column, arm, boss and lantern are one connected shape), the lamp lies inside the bowl, the light inside the bowl, the wear zones lie on the right faces; **E** no maker, brand, crown or authority's name on any part, only the plate carries letters, none of the content rule's words, the previews obey the brief, this file carries its summary line, the plain statement and every preview's credit; **W** ten deliberately wrong copies of target.json (a 114 sleeve, an untapered shaft, a 30 degree rake, a narrower lantern, the lamp above the bowl, the scene file's yellow, a maker's name on the plate, an arm that misses the boss, columns at 8, 28 and 48, a light above the lantern) must each be refused by at least one test.

## 10. What the target could not settle

{chr(10).join('- ' + c for c in T['could_not_settle'])}

## 11. To read once the network opens

{chr(10).join('- ' + c for c in T['to_read_when_the_network_opens'])}

## 12. Handover

{chr(10).join(f"- **{k.replace('_', ' ')}**: {v}" for k, v in T['handover'].items())}

## 13. Previews and credits

All photographs: Poly Haven, CC0 1.0, Andreas Mischok, taken 2019-08-18 (BGE and US01); used for measuring only, never placed in the game, traced into a texture or fed to an image model. Each crop is of the object only: the signs on BGE's shaft that carry text, a telephone number or a hand-painted picture are masked flat grey, a parked car is cropped out of US01's base, and nothing else is in frame (no people, no shop names, nothing the content rule bars). The drawings are this target's.

{table([
    ("bge-bethnal-green-column-strips.jpg", "BGE, four strips of the rectified column, z 0 to 4800, 1.2 mm a pixel, signs masked grey", "the lower column's measurements (section 4)"),
    ("bge-bethnal-green-column-target-on-photo.jpg", "the same with target.json's lower column drawn over it (red lines), scale fitted on the sleeve only; no outline above z 4280", "the drawing check"),
    ("bge-bethnal-green-column-pod.jpg", "BGE, the post-top dish seen from below, rectified, 1.5 mm a pixel", "the pod's width (variant P)"),
    ("us01-bethnal-green-bent-arm-elevation.jpg", "US01, the shaft's top, stem, bent arm and lantern, rectified at 8.8 m, 3 mm a pixel", "the bracket's form and ratios"),
    ("us01-bethnal-green-lit-lantern-from-below.jpg", "US01, the lit lantern seen from below, 5 degrees wide", "the glow's colour; the arm entering the rear end"),
    ("us01-bethnal-green-sleeve-and-shoulder.jpg", "US01, the sleeve, shoulder and shaft's foot, rectified, 2 mm a pixel", "the stepped form; the door outline"),
    ("hook-sheet-slot-x8-east-target-on-sheet.jpg", "variant A at its scene slot laid on the Hook sheet's reduced copy with the sheet's own lens; a placement test, not a measurement", "section 3"),
], ("file (production/previews/cloud-week/refs/lamp-posts/)", "what it shows", "used for"))}

## 14. The numbers that are not printed in the repository

{table(num_rows, ("id", "value", "unit", "kind", "source (first 230 characters)"))}
"""
open(os.path.join(HERE, "TARGET.md"), "w", encoding="utf-8").write(md)
print("wrote TARGET.md", len(md), "bytes")
