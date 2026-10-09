# Shop fascia signs of Quay Street: the exact target

Cloud week 42, 8 October 2026. SECOND AND LAST TRY, amended after the fresh reviewer's 13 faults and 14 notes (TARGET-REVIEW.md, which this file does not touch). Unit 4.1 builds from `target.json` and this page. Nothing is committed.

Plain summary. Ten shop fronts, ten different boards, on the kit's board of 5.41 m by 0.55 m, drawn at 1 mm to the pixel and set the way round the GAME shows them (on the east parade the low street numbers are on the viewer's right, so MICKEY'S stands over its own door, 4.055 m from the board's left edge). The name over Mickey's door, the two lit box signs, the tea room's flat panel and the four hanging signs are solid parts, not painting. Three boards carry the ghost of older lettering with its exact words. Every word is a trade description or a name already minted. Checks read the pixels of the finished board, so a mirrored board, a name at the wrong end, a wrong font or a stray ghost word is caught.

Files in this folder:

- `target.json`: the whole target (10 shops, 4 hanging signs, 23 glass rows, 316 checks, the self-check result).
- `make_target.py`: the author tool that writes `target.json` (every width is measured on the real font files).
- `pixel_checks.py`: the REFERENCE reader of the finished picture (the pixel checks: position, glyph mask, mirror, jitter), with a crude reference renderer to test the checks themselves.
- `target_drawing.py`: draws the boxes and baselines of every board (1 mm to the pixel) and the four hanging signs into a folder given on the command line, plus the polygons as JSON, plus a layout sheet.
- `self_check.py`: 296 checks, writes its result into `target.json` under `self_check`.
- `make_previews.py`: rebuilds the previews of the photographs measured.
- Previews, in `production/previews/cloud-week/refs/fascia-signs/`: `P1-leadenhall-board-elevation.jpg` (the two ends of the board, nothing else), `P1-leadenhall-board-target-on-photo.jpg` (the drawing laid on them), `P2-...` and `P3-...` (plank textures), `H1-...` (the Hook sheet's board), `L1-quay-street-ten-fascias-layout-sheet.jpg` (the ten boards, boxes and baselines).

## 0. What the second try changed, in one table

| Fault | Where it is answered |
|---|---|
| 1 axis backwards | section 2; `axis`, every shop's `board_u0_street_x_m`, Mickey's name at board x 4055, the hanging signs' street x |
| 2 texture or geometry | section 3; `geometry` on three shops and Mickey's letters; height map within its range |
| 3 checks did not read the pixels | section 8; `pixel_checks.py`; G10, G12 to G18 and 298 per-item checks |
| 4 ghosts without words | section 5 and `ghost` blocks; three ghosts with exact words, two as brush texture only |
| 5 one-designer layouts | section 5; nine different layout classes |
| 6 too heritage | three plastic fronts, a plain caff; section 5 |
| 7 two dark boards side by side | the fish board is the sheet's pale board with red lettering and a black shade |
| 8 dots for scallops | the scallops are gone with the duck-egg tea room |
| 9 signs bolted to consoles | brackets on the brick above the cornice; section 6 |
| 10 grocer's glass | three slabs, no crack, method stated; section 5 |
| 11 baked frame highlight | removed; planted mouldings in the height map |
| 12 dead tube | upper row only, 1500 mm, 60 per cent |
| 13 drink in a preview | the preview is the board's two ends only; section 9 |

The full answer to each fault and each note is section 12.

## 1. Reading this file

- Units. Board x in millimetres runs from the board's LEFT edge as a viewer in the street, facing it, sees it IN THE GAME. y is UP from the board's bottom edge. Street x is metres along the street and is the same in the recipe and in the game. Colours are sRGB 0 to 255. Contrast is WCAG. dE is CIE76 on Lab D65.
- Evidence kinds, on every number that matters:
  - Read: printed in a source file.
  - Scaled: measured off a drawing or the game's own files.
  - Photo: measured on a photograph today.
  - Sheet: measured on the Hook sheet (a generated picture, approved for mood, palette and composition).
  - Derived: computed from the above.
  - Judgement: the writer's. A better source overturns it.
- NO PHOTOGRAPH OF A 1990 FASCIA WAS REACHED. The network refused Wikimedia, Geograph, Flickr, archive.org, Picture Sheffield, Flashbak, Historic England and the others (403). The only photograph measured is a 2019 restoration of a 19th-century arcade, used for craft ratios only, never for colour or wear. What 1990 looked like rests on earlier notes (cited, not re-measured), the Hook sheet and Judgement, and is marked.
- A photograph beats a book. Where they differ, section 10 says which won.

## 2. The board and its left-right direction (fault 1)

The board texture is 5410 by 550 mm at 1 pixel to the millimetre (field [24, 24, 5386, 526], safe zone [150, 40, 5260, 510]). It is the kit's fascia between the consoles: 0.295 to 5.705 m of a 6.0 m bay, z 2.85 to 3.40 m, 0.12 m proud, the cornice top at 3.55 m. Read: SCENE-SLOTS.md, the shopfront kit README, vignette-scene.json, the fascia-01 spec.

The rule, as the game shows it. The recipe builds the street with east on the +y side, where the kit README's "left to right seen from the street" is the pre-mirror frame. Then `_export_street` REFLECTS y to -y ("mirror"), and lettered faces take UVs that run "from the reader's left to the reader's right in the reflected street". Street x itself is unchanged; only the viewer's left and right swap. So, in the game:

- East parade (Mickey's to the grocer, and the chandler): low street x is on the viewer's RIGHT. Board x = (u0 - street x) x 1000, where u0 = the bay's HIGH end - 0.295.
- West block (tea room, ironmonger, newsagent): low street x is on the viewer's LEFT. Board x = (street x - u0) x 1000, where u0 = the bay's LOW end + 0.295.

Evidence (all read again today):

- `production/previews/shop-fronts-whole-2026-10-08.jpg`, from the left: TO LET (street x 21 to 27), PAWNBROKER (15 to 21), FRESH FISH (9 to 15), MICKEY'S (3 to 9) at the right-hand end, with Mickey's glazed door at the right of its window. The pawnbroker's door is at the left of its window, the fish shop's and the empty unit's at the right: exactly the door ends below.
- `production/previews/morning-hook-day-2026-10-08.jpg`: Mickey's window on the left of its bay and its door at the right, the end nearer the camera.
- terrace-front.py, the export and the UV rule (about lines 7925 to 7945 and 8455 to 8480), and the recipe's own record that "unmirrored, the first film read S'YEKCIM from the pavement" (about line 6616).
- The earlier version of this target used the pre-mirror frame. The reviewer was right and the fault is accepted; the checks that hid it (D6) now read the door's x from `production/specs/mickeys-office.json` (4.65 m) and test the corrected mapping.

Door ends (`BAY_DOORS_ON = left, left, right, left, right, right` in the recipe's Blender frame; east left = low street x; the west blocks are turned a half turn, so their left = HIGH street x; the chandler's `doors_on` is right = high):

| Shop | Side | Bay street x | Door end (street) | Door on the viewer's | Board's left edge is street x |
|---|---|---|---|---|---|
| Mickey's | east | 3 to 9 | low | right | 8.705 |
| fish market | east | 9 to 15 | low | right | 14.705 |
| Rita's | east | 15 to 21 | high | left | 20.705 |
| empty unit | east | 21 to 27 | low | right | 26.705 |
| steam laundry | east | 27 to 33 | high | left | 32.705 |
| grocer | east | 33 to 39 | high | left | 38.705 |
| chandler | east | 40 to 46 | high | left | 45.705 |
| tea rooms | west | 24 to 30 | low | left | 24.295 |
| ironmonger | west | 30 to 36 | high | right | 30.295 |
| newsagent | west | 36 to 42 | high | right | 36.295 |

Mickey's name: over the door at street x 4.65, board x = (8.705 - 4.65) x 1000 = **4055** (the right half of the board). Variant V4 centres it (board x 2705) as the game does today. Self-check group 2 recomputes all of this from the recipe and the specs.

## 3. Texture, geometry and the height map (fault 2)

Texture (the picture on the board): every ground colour; every painted, gilded, cut-vinyl or back-painted letter EXCEPT Mickey's; keylines, borders, ropes, rules, panels; the ghosts; the ten pin holes; the wear (runs, gull marks, rust, loss); the box faces' printed look and their emissive map; a soft contact shadow under Mickey's letters.

Height map (8 bit, 128 = board face, 0.01 mm a step, so -1.28 to +1.27 mm): letter paint ridge +0.20, keyline +0.15, vinyl +0.08, gilt +0.05, paint loss -0.30 (bare board -0.50), planted moulding +0.60 with a 4 mm chamfer (Rita's, the ironmonger's, the chandler's: the outer 24 mm), the grocer's chrome edge strip and speed lines +0.80 (a raised metal strip, in the map, not geometry), the grocer's slab joints -0.50 and bevels a 2 mm ramp to -0.30. No relief of 3 mm or more lives in the map.

Geometry (solid parts a script must place; none of it is in the texture):

| Part | What it is | Numbers |
|---|---|---|
| Mickey's letters | the recipe's `RAISED_LETTERS` (terrace-front.py line 857), AMENDED. No second set of letters in the texture. | MICKEY’S, Marcellus SC; cap 0.330 m (Blender text size 0.4708 from the font's measured cap ratio 0.701, not the recipe's 0.66 which makes them 6 per cent too tall); stand-off 0.014 m; emboldened 3 mm; face `brass_gilt` (167,149,109), flanks `brass_side`; centred at board x 4055 (street x 4.65); baseline y 100; box [2996, 90, 5114, 439]; width 2118 mm; roughness 0.38, metallic 0.85 |
| Steam laundry box sign | a box on the board | outer [105, 35, 5305, 515] = 5200 x 480 mm; depth 0.15 m (Judgement); bronze returns (84,68,53); eight pan-head screws through the frame; the face texture on its front |
| Newsagent box sign | a box on the board | outer [95, 40, 5315, 510]; depth 0.14 m (Judgement); returns powder black (48,46,43); eight screws |
| Tea room panel | a flat unlit acrylic panel | outer [90, 40, 5320, 510]; depth 0.03 m; white timber returns; screwed through the frame |
| Hanging signs | four | section 6 |

The old "+3 mm" frame on the box sign is gone from the height map. The recipe's cap 0.24 m, 12 mm stand-off and its centring across the whole sign piece are replaced by the values above. Check G17 (geometry) holds the letter depth 14 mm plus or minus 2, the cap, and the bounding box centred over the door within 50 mm; G9 no longer contains an applied entry.

Texture size. 5410 x 550 is not a power of two. From memory, and NOT checked in the 5.8.2 source (not on this machine; RULINGS 8 Oct wants file and line): Unreal gives such a texture no mips unless it is padded or stretched at import, and thin letters would shimmer from the hook camera. The builder checks this FIRST. If it is confirmed, either pad to 8192 x 1024 (the render in the top-left 5410 x 550; u 0 to 0.6604, v 0 to 0.5371) or stretch to 5120 x 512 (a 1.7 per cent aspect error). The checks run on the authored 5410 x 550 render before any packing. Still open (section 11).

## 4. Fonts, palette, style

Nine fonts, all SIL OFL 1.1, each OFL.txt read whole today at raw.githubusercontent.com; every glyph needed (’ and · included) is in its file. Letters are RENDERED into pictures: the OFL puts no restriction on a picture made with a font. The font files themselves are not copied into `production/fonts/` here. Overpass, Apache and GPL faces are excluded. Reserved Font Names are parsed from the OFL files by the author tool (Josefin Sans is reserved as "Josefin Sans", not "Josefin").

| Font | Used for |
|---|---|
| Marcellus SC (ruled 30 Sep) | MICKEY’S, letters and ghost |
| Abril Fatface | Rita's name and numerals |
| Old Standard TT Bold | Rita's trade line, the ironmonger (all lines, its ghost and its hanging board), the fish ghost |
| Oswald (500 and 600) | the fish market |
| Jost | steam laundry, and its box sign |
| Josefin Sans | the grocer |
| Libre Franklin | the newsagent, the chandler's trade line, the letting board, the hours plates |
| Fraunces | the tea room |
| Alfa Slab One | the chandler, its numerals, its hanging board |
| Patrick Hand (already in `production/fonts`) | the fish shop's whitewash glass |

Palette: every colour has a fresh value and an aged 1990 value (from a grime film, a chalk lift, a chroma factor and a yellowing, by wear class; Judgement). Measured ones: Mickey's slate (62,75,87) and gilt (167,149,109) are the Hook sheet's means (Sheet); the fish board's pale ground is the sheet's white fascia (204,204,204) brought to a light board (196,202,206) aged. The empty unit's board is the recipe's own `bare_timber` (linear 0.021, 0.014, 0.010, which is sRGB 40,31,25 fresh, 46,37,30 aged), the colour the street draws today (DECISIONS 3 Oct keeps the unit "as the street already draws it").

Style, common to the hand-lettered boards (Photo, from P1, unless marked):

- Block shade: 45 degrees down and to the right, 0.10 of the cap high, a solid extrusion of the glyph, not a blurred drop; colour per block. On painted and gilded boards only. None on vinyl, applied or back-painted letters.
- Keyline: thickness 0.027 of the field, inset 0.078 at the top and 0.102 at the bottom and 0.150 at the sides, corners cut by a concave quarter circle of radius 0.136 of the field. On Rita's board only.
- Numerals: 0.91 of the cap, near the board's ends. On TWO boards only (Rita's "5", the chandler's "13"; the numbers are proposed).
- Hand jitter on painted and gilded blocks: each glyph's baseline off by a normal draw of SD 0.6 to 1.6 mm (at most 1.6), advance 1.5 per cent, rotation 0.35 degrees, stroke 3 per cent (Judgement). None on vinyl, applied or glass letters.
- Round capitals overshoot the baseline and the cap line by 1.6 per cent of the cap. Blocks are centred on the ink, not the advance box.
- Trade lines are at least 70 mm cap. Oswald is 500 or heavier. Tracking on trade lines is at most +0.12 em on at least four boards.

## 5. The ten boards

Ten shops, one board each (the scene has ten shop bays; RULINGS 2 Oct counts twelve shopfronts, the gap is named in section 11). Order is the street's. Anchor "centre", "left" or "right" is the block's ink. x and baseline are in board millimetres. Contrast is aged face to aged ground. Layout classes are all different except where noted.

The distinctness rule (G7, G11): every pair of boards differs in aged ground by dE >= 14 (the least is 14.8); no two boards share a name-line font; at most five boards share a centred name over a trade line (three do: Rita's, the grocer, the chandler); at most three trade lines use a middle dot (one does: the chandler's); at least six layout classes (nine are used).

### 5.1 Mickey's (minicab office), `name_only_offset`

Painted timber, eggshell slate (62,75,87), a little orange-peel, grain along. NO name in the texture. The name is the raised geometry of section 3, over the door at board x 4055; the texture carries the ground, a ghost, ten pin holes and a soft contact shadow under where the letters stand (blur 6 mm, opacity 0.35, offset -2, -5).

Ghost (fault 4): the older, CENTRED name. MICKEY’S in Marcellus SC, not emboldened, cap 245 mm, centred at board x 2705, baseline 150, ink box [1921, 145, 3489, 400]; colour the ground +3.5 dE towards blue (64,80,96 on 62,75,87); brush-cut edge with a 1 mm ridge; not broken. Ten pin holes along the old cap line y 395, from x 1999.4 to 3410.6 at 156.8 mm. The new letters at x 2996 to 5114 overlap the ghost's right end only.

Wear (class 2): loss 0.04, chalk +3 L*, grime 0.07, four runs of 40 to 160 mm, two gull marks, two short rust runs under the console fixings.

The cap is 0.60 of the board (330 of 550), against the sheet's 0.69; Marcellus SC is 1.8 times wider than the sheet's tall narrow capitals, so the cap stops at 330 mm (the reviewer's note 1). Width over cap is 6.42 against the sheet's 3.52; reported, not hidden.

### 5.2 Fish market, `name_left_list_right`

The sheet's pale board beside Mickey's (fault 7). Ground (196,202,206) aged, gloss enamel gone flat and chalky, roughness 0.58. Two vermilion rules (y 34 to 46 and 504 to 516, x 120 to 5290). Red sign-writing (the photographed 1990 fishmonger's colour way, earlier note): vermilion (197,75,62) on the pale board, contrast 2.85, with a BLACK block shade (37,35,34), 29 mm.

| Block | Text | Font | Cap | Anchor, x | Baseline | Tracking | Face |
|---|---|---|---|---|---|---|---|
| name | FISH MARKET | Oswald 600 | 290 | left, 1270 | 188 | 0.06 | vermilion, black shade 29 |
| trade_1 | WET FISH | Oswald 500 | 70 | left, 3715 | 408 | 0.10 | sign black |
| trade_2 | SHELLFISH | Oswald 500 | 70 | left, 3715 | 298 | 0.10 | sign black |
| trade_3 | SMOKED | Oswald 500 | 70 | left, 3715 | 188 | 0.10 | sign black |

The trade is a list beside the name, its three lines left-aligned at x 3715 (contrast 9.0). Door at the low end (viewer's right).

Ghost: FISHMONGER, Old Standard TT Bold, cap 200 mm, centred at 2705, baseline 160, ink box [1724, 153, 3686, 365]; 4 dE DARKER than the ground (185,191,195 on 196,202,206); 60 per cent of its strokes painted over by the newer white. Trade word only, no proprietor.

Wear (class 2): loss 0.05, chalk +4, grime 0.08, six runs of 50 to 200 mm, three gull marks, no rust.

### 5.3 Rita's (pawnbroker), `centred_stack_with_ends`

Oil-gilded capitals with a black block shade on oxblood (93,46,49 aged) inside a gilt cut-corner keyline panel (panel [68, 68, 5342, 482], line 13 mm, inset 44 mm, radius 70 mm; P1's corner). Planted moulding round the board (24 mm, +0.6 mm, 4 mm chamfer). Not lit (DECISIONS 1 Oct: only her WINDOW is lit). Oil gloss gone satin, roughness 0.45.

| Block | Text | Font | Cap | Anchor, x | Baseline | Tracking | Face |
|---|---|---|---|---|---|---|---|
| name | RITA’S | Abril Fatface | 230 | centre, 2705 | 221 | 0.10 | gold leaf, shade 23 |
| trade | PAWNBROKER | Old Standard TT Bold | 84 | centre, 2705 | 99 | 0.12 | gold leaf, shade 8.4 |
| end_l | 5 | Abril Fatface | 214 | left, 200 | 168 | 0 | gold leaf, shade 21.4 |
| end_r | 5 | Abril Fatface | 214 | right, 5210 | 168 | 0 | gold leaf, shade 21.4 |

Contrast 4.49. Door at the high end (viewer's left). Ghost: a repaint patch [2300, 140, 3300, 340], 3 dE, brush-cut edge, NO GLYPHS (brush texture only; no word is invented). Wear (class 1): loss 0.03, three runs, one gull mark. Her name is larger over its field (0.458) than P1's (0.306): deliberate, a trading parade and not a restored arcade; reported.

### 5.4 Empty unit, `none`

Bare soot-darkened timber (the recipe's `bare_timber`, 46,37,30 aged), paint long gone, a few patches of old paint, roughness 0.85, grain strong (amplitude 3 L*). The last trade's lettering is painted out in buff: a painted-out patch [1105, 120, 4305, 420] with a 0.4 mm ragged ridge and six nail holes, NO GLYPHS. A letting board across the middle (section 6.3). Class 3 wear: loss 0.17, ten runs of 60 to 300 mm, six gull marks, three rust runs from the nail heads of the removed lettering. No text on the board, so no word to approve beyond the letting board's.

### 5.5 Steam laundry, `panel_left_name_right`

A lit plastic box sign, 1980s: white acrylic face (225,217,197 aged), a red cut-vinyl panel [320, 100, 2070, 450], the name in blue cut vinyl, bronze anodised frame. The old board shows round the box: `old_board` [0, 0, 5410, 550], cream painted timber with paint loss 0.08 (the first shape on the board). The box itself is geometry (section 3).

| Block | Text | Font | Cap | Anchor, x | Baseline | Tracking | Face |
|---|---|---|---|---|---|---|---|
| name | STEAM LAUNDRY | Jost 800 | 200 | right, 5030 | 175 | 0.05 | vinyl blue (46,68,136) |
| trade_1 | LAUNDERETTE | Jost 600 | 90 | centre, 1195 | 340 | 0.06 | vinyl cream |
| trade_2 | SERVICE WASHES | Jost 600 | 70 | centre, 1195 | 230 | 0.06 | vinyl cream |
| trade_3 | DRY CLEANING | Jost 600 | 70 | centre, 1195 | 120 | 0.06 | vinyl cream |

The trade is three short lines in the red panel at the LEFT (contrast 5.0); the name stands alone at the right (contrast 6.5). Door at the high end (viewer's left).

Emissive (the lit face): face rectangle [131, 61, 5279, 489]; two tube rows at y 168 and 382 with a 6 per cent band; tube joints every 1500 mm at x 300, 1800, 3300, 4800; tube-end shadows 60 mm wide and 10 per cent dimmer at every joint in both rows. DEAD TUBE (fault 12): the UPPER row only, x 3300 to 4800 (a 1500 mm tube), its light down to 60 per cent because the lower row still lights it. Lit when the shop is open (hours in hook-cast.json), dull and dark when shut (variant V2). Wear class 2: seven runs, no gulls, grime 0.10; the vinyl is clean.

### 5.6 Grocer, `centred_stack`

1930s refit, bottle green glass (36,61,49 aged), cream Art Deco capitals. METHOD (fault 10): reverse-painted CLEAR plate glass, the signwriter's glass fascia, so the cream letters are painted on the back and seen through. The word Vitrolite (colour right through, opaque) is NOT used. Judgement, from memory, no source reached. Of the reviewer's two fine ways this is the cheaper one: the letters stay in the texture and no letter geometry is added.

Three slabs: joints at board x 1380 and 4030, 3 mm of dark mastic (30,30,28), a 2 mm polished bevel on every slab edge. The name's ink (1450.5 to 3959.5) lies inside the middle slab. Chrome edge strip (12 mm) and three speed lines (6 mm, at y 262, 282, 302, x 52 to 640 and 4770 to 5358) are raised metal in the height map at +0.8 mm. NO crack across the fascia: the cited note puts cracks low, at the stallriser, which is not this family.

| Block | Text | Font | Cap | Anchor, x | Baseline | Tracking | Face |
|---|---|---|---|---|---|---|---|
| name | FAMILY GROCER | Josefin Sans 700 | 190 | centre, 2705 | 238 | 0.12 | cream, back-painted |
| trade | HIGH CLASS PROVISIONS | Josefin Sans 600 | 70 | centre, 2705 | 122 | 0.12 | cream, back-painted |

Contrast 7.75. A trade description, no proprietor. Door at the high end (viewer's left). Wear class 2: no loss, grime 0.06, five runs, one gull mark. Roughness 0.08.

### 5.7 Newsagent, `name_only_rules`

A lit plastic box sign: translucent red acrylic (184,70,62 aged), the name only in cream cut vinyl, two cream vinyl rules (y 90 to 104 and 446 to 460, x 220 to 5190). The trade moves to the door glass (section 6.2). `old_board` as the laundry's. The box is geometry (section 3).

| Block | Text | Font | Cap | Anchor, x | Baseline | Tracking | Face |
|---|---|---|---|---|---|---|---|
| name | NEWSAGENT | Libre Franklin 900 | 260 | centre, 2705 | 145 | 0.08 | vinyl cream |

Contrast 4.11. Emissive as the laundry's, with no dead tube. Wear class 2: five runs, two gull marks, one vinyl rule lifting 30 mm at its right end, no letter lost. West block, door at the high end (viewer's right).

### 5.8 Ironmonger, `name_centre_trade_in_ends`

Sign-written black roman capitals with a vermilion block shade on buff (188,173,136 aged), a black rule border (a double rule, black and vermilion) with corner blocks, and a planted moulding. The trade is in the two end panels, not under the name.

| Block | Text | Font | Cap | Anchor, x | Baseline | Tracking | Face |
|---|---|---|---|---|---|---|---|
| name | IRONMONGER | Old Standard TT Bold | 180 | centre, 2705 | 185 | 0.08 | black, vermilion shade 18 |
| end_l_1 | TOOLS & | Old Standard TT Bold | 70 | centre, 600 | 285 | 0.06 | black, shade 7 |
| end_l_2 | HARDWARE | Old Standard TT Bold | 70 | centre, 600 | 190 | 0.06 | black, shade 7 |
| end_r_1 | PAINTS & | Old Standard TT Bold | 70 | centre, 4810 | 285 | 0.06 | black, shade 7 |
| end_r_2 | PARAFFIN | Old Standard TT Bold | 70 | centre, 4810 | 190 | 0.06 | black, shade 7 |

Contrast 6.73. The font is Old Standard TT Bold (the reviewer's note 6: Libre Baskerville was rated low to medium by the period note and is gone). Ghost: IRONMONGER, Old Standard TT Bold, cap 190, centred 2705, baseline 170, 4 dE darker than the ground (177,162,126 on 188,173,136), 60 per cent broken. Wear class 2: loss 0.06, six runs, two gull marks, two rust runs from the board's OWN nail heads at the left end (not from the bracket bolts, which are on the brick: note 10). The street number "16" is on the fanlight only. West block, door at the high end (viewer's right).

### 5.9 Tea rooms, `trade_above_name`

A plain 1980s caff front (fault 6; the cast's "the caff", open 6.30 to 22.00). A flat, unlit acrylic panel screwed over the old board (outer [90, 40, 5320, 510], a 25 mm white-painted timber frame, face [115, 65, 5295, 485]). Brown face fresh (132,82,50), 1990 (120,74,44), roughness 0.35. Cream cut-vinyl lettering (235,227,201). `old_board` visible round the panel. No duck-egg ground, no scalloped valance (fault 8): both are deleted.

| Block | Text | Font | Cap | Anchor, x | Baseline | Tracking | Face |
|---|---|---|---|---|---|---|---|
| trade | BREAKFASTS, LUNCHES & TEAS | Fraunces 600 | 70 | centre, 2705 | 362 | 0.06 | vinyl cream |
| name | Tea Rooms | Fraunces 900 | 200 | centre, 2705 | 118 | 0.02 | vinyl cream |

Contrast 5.81. The trade line stands ABOVE the name. The panel is geometry (section 3). Wear class 1: three runs, one gull mark. West block, door at the low end (viewer's left).

### 5.10 Chandler, `centred_stack_with_ends`

White Egyptian capitals with a black block shade on navy (44,53,83 aged), a painted rope border (rope 12 mm, pitch 28 mm, corner radius 40 mm, inset 34 mm, panel [70, 70, 5340, 480]), a planted moulding.

| Block | Text | Font | Cap | Anchor, x | Baseline | Tracking | Face |
|---|---|---|---|---|---|---|---|
| name | SHIP CHANDLER | Alfa Slab One | 170 | centre, 2705 | 245 | 0.05 | white paint, shade 17 |
| trade | ROPE · PAINT · CHARTS · TWINE | Libre Franklin 700 | 70 | centre, 2705 | 135 | 0.10 | vinyl cream |
| end_l | 13 | Alfa Slab One | 158 | left, 210 | 196 | 0 | white paint, shade 15.8 |
| end_r | 13 | Alfa Slab One | 158 | right, 5200 | 196 | 0 | white paint, shade 15.8 |

Contrast 8.5 and 9.4. The only dotted trade line on the street. Wear class 2: loss 0.07, six runs, four gull marks, three rust runs under fixings (the quay is near). East, door at the high end (viewer's left).

## 6. Hanging signs, glass lettering, small panels

### 6.1 The four hanging signs (fault 9)

Every bracket is fixed to the BRICK ABOVE THE CORNICE (cornice top 3.55 m): plate foot 3.60 m, plate centre 3.75 m, arm 3.75 m, over the party-wall pier at the street x below. The kit has no pilaster shaft to bolt to between 2.85 and 3.55 m: there are consoles, a capital and a cornice. The drops are lengthened so the signs hang where they did (lowest point at least 2.5 m). `clearance_below_m` is the computed lowest point.

| Sign | Street x | Viewer's side | Arm | Projection | Drop | Lowest |
|---|---|---|---|---|---|---|
| Rita's three balls (gilt, 0.26 m each, two above and one below) | 20.825 | LEFT end of her bay, her DOOR end (high x) | 3.75 | 0.85 | hanger 0.57 | 2.65 |
| Steam laundry double-sided box (0.62 x 0.45 x 0.14, back edge on the brick, 3.60 to 4.05 m) | 27.175 | RIGHT end of its bay (low x) | 4.05 | 0.62 | none | 3.60 |
| Ironmonger hanging board "KEYS CUT" (0.55 x 0.38 x 0.04, two rings and chains 0.70 m longer) | 35.825 | RIGHT end of its bay (high x) | 3.75 | 0.70 | 0.76 | 2.61 |
| Chandler hanging board "CHANDLERY" (0.80 x 0.50 x 0.05, two chains, 0.65 m longer) | 45.825 | LEFT end of its bay (high x) | 3.75 | 0.90 | 0.71 | 2.54 |

Rita's balls are at her door end, not beside the fish shop (Judgement: the reviewer's recommendation). Each face of a hanging sign reads left to right from its own side (mirror-correct). KEYS CUT is the ironmonger's key-cutting (DECISIONS 7 Oct); CHANDLERY is a word not on the fascia, so the street does not repeat itself. All the numbers here are Judgement. G15 checks them.

### 6.2 Glass lettering (23 rows)

The fish shop's whitewash (Patrick Hand: FRESH DAILY at z 0.95, SHELLFISH at 1.52, SMOKED FISH at 2.02), the pawnbroker's gold leaf (WATCHES, JEWELLERY, LOANS at z 2.64, at street x 18.142, 17.025, 15.908), the laundry's SERVICE WASHES (white vinyl, z 2.05), the newsagent's trade line on the door glass (TOBACCONIST & CONFECTIONER, cap 70, white vinyl, z 1.35, x 40.2), EST. 1884 (ironmonger) and EST. 1879 (chandler) in gold leaf at z 2.64, and the fanlight street numbers at z 2.18 (Mickey's 1, fish 3, Rita's 5, empty 7, laundry 9, grocer 11, tea 14, ironmonger 16, newsagent 18, chandler 13). The empty unit's glass is whitewash with nothing legible (ruled 3 Oct). Street numbers, years and the EST. lines are PROPOSED (Judgement), not minted: the town mints or strikes them, and variant V3 strips them. Every lettered row not already in the game has a street x inside its bay and a check (G16): 20 rows.

Mickey's two existing glass lines (the phone number 0632 960418 and MINICABS · 24 HOURS) are another family's, are NOT approved here and are not in `approved_words`. The second contradicts the cast's hours for Mickey's (7.00 to 3.00, shut 3 to 7); it goes to the town and the shop-room builder (the reviewer's note 4). Reported by the self-check.

### 6.3 Small panels

- Letting board on the empty unit: 900 x 450 mm, white, TO LET in Libre Franklin 800, cap 130, vinyl red, four screws, slightly askew (2 degrees), a rust run under each lower screw; centre at board x 2705, y 275. The game's own `board_to_let.png` (PT Sans) exists; the font here is an OFL replacement. No agent and no number are minted.
- Hours plates on five shop doors (Rita's, fish, laundry, newsagent, tea rooms): 300 x 190 mm white enamel plates, black Libre Franklin 700, cap 24, blue border 4 mm. Their lines are SET AT BUILD TIME from hook-cast.json (Mon-Sat hours, a Wednesday half-day where the cast has one). Their own rule (note 11): each line must match the pattern in `hours_plate_rule` (day names, times "H" or "H.MM", a dash, OPEN or CLOSED). They are NOT in `approved_words`, so G4 does not fail them.

## 7. Words

45 approved strings (`approved_words`): the ten shop names or trades, every trade line, every glass row not already in the game, the numerals, the hanging signs' words, and the three ghost words. Each is a trade description or a name already minted. Minted: MICKEY’S (canon), RITA’S (the cast), FISH MARKET and STEAM LAUNDRY (DECISIONS 3 Oct). Everything else is a trade description. NO proprietor is invented. Ghost lettering carries trade words only (G14).

`ghost_words` = FISHMONGER, IRONMONGER, MICKEY’S. A ghost word appears only as a ghost: FISHMONGER is on no board and no glass row. Nothing of drink, gambling or children: the newsagent has no pools or lottery, the grocer no off-licence, the chandler no bonded stores. Nothing after 1992. The word list is checked against the content rule's lists, the real-mark list and every name in RealWorld.cs's AnyCase list (210 names read). `forbidden_patterns` in the JSON holds them.

## 8. Checks (316)

Every check has an id, name, scope, measure, expected, tolerance, unit, method and what it reads (`pixels`, `pixels+font`, `geometry`, `manifest`). The pixel checks are the ones the first try lacked (fault 3). `pixel_checks.py` is the reference reader; the tolerances below are the ones it uses and the ones tested.

- G1 texture size. G2 planted moulding: read from the HEIGHT MAP (the outer 24 mm ring against the field just inside it, and the chamfer width), not a baked highlight. G3 no repeated word on a board. G4 words: every manifest string in `approved_words` (hours plates by their own rule), none in `forbidden_patterns`. G5 no tiling period at lags 600 to 5000 mm. G6 grain along the board (0 to 8 degrees). G7 distinct fascias. G8 contrast of every name line (0.85 of nominal and not under 2.2).
- G9 relief present: gilded 0.02 to 0.15 mm, vinyl 0.04 to 0.20, painted 0.10 to 0.35 (the applied-letter step lives in G17).
- G10 glyph mask against the font, per block. The block's string is re-rendered from its font file (font, weight, size from the cap, tracking, anchor, origin) and compared with the face mask READ ON THE PIXELS (pixels within dE 14 of the face colour and nearer to it than to the ground, inside the block's effects box dilated 8 mm and inside its panel). Score F is the mean of recall and precision, each against the other mask dilated 2.5 mm (hand-painted) or 1 mm (vinyl, applied, glass). Pass at F >= 0.90, and the same re-render FLIPPED about the block's centre line must score lower by at least 0.15. No string on the street is mirror-symmetric; the weakest margin is 0.175 (the chandler's "13").
- Per-block `pos`: the ink box of the pixel face mask (widened 40 mm along the line and 8 mm up and down) has its centre (anchor centre) or its left or right edge (anchor left or right) within plus or minus 15 mm of the target and its baseline within 3 mm (the median bottom of flat-bottomed letters where the string is round-bottomed).
- G11 layout variety: at most five boards share a centred name over a trade line, at most three trade lines use a middle dot, at least six layout classes.
- G12 hand jitter: the SD of each glyph's bottom edge from a straight baseline is 0.6 to 1.6 mm on painted and gilded blocks, and 0 to 0.6 mm on vinyl, applied and glass blocks (the pixel grid alone gives 0.3 to 0.5 mm at 1 pixel to the millimetre, so an unjittered reference render must read at most 0.6).
- G13 wear counts: runs, gull marks and rust runs within one of each shop's `age` numbers.
- G14 ghosts: present at its position, 3 to 5 dE from the ground, the share of strokes painted over, and no OTHER legible string.
- G15 hanging signs: x within 0.02 m, arm height 0.02 m, projection 0.02 m, lowest point at least 2.5 m, plate foot above the cornice top 0.05 m, both faces read left to right from their own side.
- G16 glass lettering: the string is in `approved_words`, the cap within 5 per cent, z within 0.03 m, street x within 0.10 m.
- G17 geometry parts: Mickey's letter depth 14 mm plus or minus 2, cap, centre over the door within 50 mm, no letter geometry left in the texture; each box's outer rectangle and depth.
- G18 mirrored board: any block that is off centre by more than 200 mm and whose pixels sit at the board's width minus x better than at x fails.
- Per item: `pos`, `width`, `mask`, `fit` (inside the safe zone with shade, outline and jitter), `contrast`, `face`, `shade`, `jitter` for every block; `ground`, `border` and `age` for every board; `emissive` for the laundry and the newsagent and the unlit Rita's; `mount` and `faces` for every hanging sign; one per glass row not already in the game; the letting board; the hours plates.

The checks are tested on a reference render of every lettered board (self-check group 8): the true render passes all of them; the MIRRORED board fails; a board shifted 60 mm either way fails every position check and a mask check; a hand-jittered render (SD 1.0 mm) still passes position, mask, width and face; a wrong font on one block (Rita's name in Oswald) fails that block's mask.

## 9. Photographs, previews and the content rule

Photographs reached: Poly Haven (CC0), through its API and file host. Authors and licences were read on its pages today. The firewall refused everything else.

| Id | What | Used for | Kind |
|---|---|---|---|
| P1 | Leadenhall Market, Andreas Mischok, taken 19 May 2019, CC0; a rectilinear, level, square-on view (yaw 90, pitch 0, 110 degrees wide, 3600 x 2400) of heritage-restored fronts | CRAFT ONLY: field proportions, keyline, shade, numerals, cap over field | Photo |
| P2 | Blue Painted Planks, Rob Tuytel (CC0, published 2018) | paint-loss shape: median aspect 3.6, median equivalent diameter 8.9 mm; the loss fraction 0.286 as an UPPER bound | Photo |
| P3 | Black Painted Planks, Dimitrios Savva (CC0, published 2025) | scuff fraction 0.091 and the luminance range of a worn dark gloss | Photo |
| H1 | the Hook sheet (production/reference/hook-sheet.png) | Mickey's board and gilt colours, the white fascia beside it, cap 0.69 of the board, letters at 0.755 along the board | Sheet |
| G1 | the game's own frames (shop-fronts-whole and morning-hook-day, 8 Oct; proof 2.6, 4 Oct) | the left-right direction; how the fascias stand today | Scaled |
| N1 to N4 | earlier notes in `production/research/` (signage and wear; the fishmonger; Peter Marshall's Hull set; frontage) | the 1990 mix of three generations of fascia, red sign-writing on a dark board (Picture Sheffield t13138, 25 Aug 1990), whitewashed glass, that trade-only boards existed, that metal fronts and fluorescent strips were the 1989 street | cited, NOT re-measured |

P1's own numbers (Photo): cap 0.306 of the field (45 of 147 view pixels); shade 0.10 of the cap; keyline thickness 0.027, top inset 0.078, bottom inset 0.102, side inset 0.150 of the field; concave corner radius 0.136; numerals 0.91 of the cap; the name sits 1.4 per cent of the panel width left of centre. Scale: fitted on ONE dimension, the lettered field's height (147 view pixels = 502 mm on our board, 0.6488 preview pixels to the millimetre); the door leaf taken as 2.1 to 2.3 m would put the camera at 0.93 m, low for a panorama, so only ratios are used. The self-check lays the drawing on P1 (cyan) and Rita's two ends (magenta) at the same scale: every edge falls within 3 view pixels.

THE CONTENT RULE AND THE PREVIEWS. P1 shows, on its board and in its windows, a real business's name and a bar's lettering and hours. None of that is kept (fault 13):

- `P1-leadenhall-board-elevation.jpg` is a composite of two crops of the unmasked view, the board's LEFT end (view x 1150 to 1480) and its RIGHT end (view x 2250 to 2440), at 2.2 times, 20 pixels apart. The name lies between them (view x 1492 to 2123) and is not kept. Nothing below the board's fanlight line is in the picture. No file, folder or JSON string names the business.
- The cap, name x0 and x1, shade, door leaf and base row were measured on the unmasked view on 8 Oct and are recorded in `photo.P1.px`; they are NOT re-measurable on the saved picture, and the self-check says so (a reported line). The numerals, field and keyline are re-measured by code on the saved picture and agree with the hand measure within 3 view pixels.
- The earlier picture of the whole front with the door leaf marked, and the earlier whole-board crops, are gone (the coordinator removed the front-scale one and renamed the board crops). `make_previews.py` no longer writes any of them. No preview shows drink, gambling or a real business's name, now or on a rebuild.

## 10. Where photographs and books disagree, and the variants

| Id | Element | Book | Photograph | Chosen |
|---|---|---|---|---|
| D1 | fishmonger's colour way | the game's oxblood board with cream letters | t13138 (1990, earlier note): dark fascia sign-written in red, another shop | red sign-writing (t13138) on the sheet's white board: the photograph settles the lettering, the sheet the ground beside Mickey's |
| D2 | shade under sign-writing | a near-black copy 3.5 per cent of the cap away | P1: a solid block shade, 45 degrees down-right, 0.10 of the cap | the photograph, on hand-painted and gilded boards only |
| D3 | numerals at the ends | none in the game | P1 has them both ends (a market unit-number livery, not necessarily provincial practice) | on TWO boards only (Rita's, the chandler), proposed numbers |
| D4 | keyline corner | plain rectangle | P1: concave quarter circle, 0.14 of the field | the photograph, on Rita's |
| D5 | fascia depth | FRONTAGE-2026-10-06 read at source: "not more than 600 mm" [CV], "at most a fifth of the front's height" [RI] | P1 field 0.45 to 0.49 m | NO DISAGREEMENT: the street's 0.55 m is inside both. The 380 mm figure was a search summary and is not used |
| D6 | Mickey's name position | centred (the game today) | not a photograph: the Hook sheet puts the letters over the door | the sheet, mapped through the export's mirror: board x 4055 |
| D7 | name size | 200 mm cap on every board | P1 0.31 of the field; the sheet 0.69 of the board | 0.34 to 0.66 of the field by trade |

Variants: V1 ten boards; V2 day and night (the two box signs lit when open); V3 proposed marks off (strip the street numbers and EST. lines); V4 Mickey's centred (board x 2705, as the game has it today); V5 a minted name (one more line, cap 0.5 of the trade line's, on a board that has none); V6 the street keeps its 6.0 m box (centre the 5410 texture, 295 mm of plain frame each end).

## 11. What could not be settled

1. No 1990 photograph of a fascia was reached. The reviewer could not open t13138, t13140 or Marshall's set either. Letter heights over board, colours, wear and which shops had box signs rest on P1, the sheet, earlier notes and Judgement.
2. Where the newsagent and the ironmonger stand. The recipe puts the newsagent at street x 36 to 42 and the ironmonger at 30 to 36; hook-cast.json puts the newsagent's pension counter at x 32 and Hal's shop at x 39. One is wrong. A town question; sign targets are keyed by trade, so a swap is a rename. Reported by the self-check.
3. Hal's shop and the count. hook-cast.json has Hal's shop at x 39 ("the coin shop that sells no coins"); DECISIONS 3 Oct has no coin shop in the west row. If it stays it needs a fascia (HAL'S is minted in the cast; its trade line is the town's) and the street has eleven. RULINGS 2 Oct counts twelve shopfronts; the scene has ten bays. The target made ten and names the gap (the reviewer's note 14).
4. The street numbers and EST. years are proposed (Judgement), not minted. Delete the end blocks and the proposed glass rows (V3) if the town does not mint them.
5. No proprietor name exists for the grocer, newsagent, ironmonger, tea room or chandler, so each board says only its trade. A minted name adds one line (V5).
6. MINICABS · 24 HOURS (contradicts the cast's hours) and 0632 960418 on Mickey's glass are another family's, not approved. From memory (unchecked), 0632 was Newcastle's STD code until 1992 and Meridian is fictional.
7. P1's absolute scale (door leaf 2.1 to 2.3 m gives a camera at 0.93 m). Only ratios are used.
8. The texture's non-power-of-two size and Unreal's treatment of it: from memory, NOT checked in the 5.8.2 source. The builder checks first and pads or stretches.
9. P1's gilt shows a slightly paler rim along the face's edge (about 1 view pixel); at its resolution an outline cannot be told from the tone-map's halo. The target keeps a 3 mm rim 4 L* paler, as P1 shows, not a dark matt edge. Whether the rim is gilding or halo is open (the reviewer's note 13: left open).
10. The grocer's glass method (reverse-painted clear plate glass, three jointed slabs), the box depths (0.15 and 0.14 m), the panel depth (0.03 m), the hanging signs' drops and the tube layout: Judgement from memory, no source reached.
11. Legibility. The 70 mm trade lines read to about 15 m straight on (15 arcminutes); the 170 to 330 mm names to about 40 to 75 m straight on. From the hook camera the boards beyond Rita's are seen at under about 15 degrees, where nothing reads at any size (that matches the sheet). The old claim that names read to 40 to 66 m left out the angle and is gone. Nobody has looked at these at the game's exposure and internal resolution.
12. Night: only Rita's WINDOW is ruled lit (DECISIONS 1 Oct). The box signs' emissive is specified; whether it is on after dark follows the town's hours, not this target.

## 12. The review, fault by fault, and note by note

Faults:

1. Axis backwards. ACCEPTED, verified in the export code and on the two game frames (section 2). Board x, Mickey's name at 4055, every u0, the sides and street x of the four hanging signs, the glass rows' street x and D6 are all remapped. V4 kept. Rita's balls at her door end (20.825).
2. Texture or geometry. ACCEPTED. Mickey's letters are the recipe's raised letters (amended: cap 0.330, board x 4055, stand-off 0.014, emboldened 3 mm, flanks brass_side) with none in the texture; the laundry box (0.15 m deep, bronze returns), the newsagent box (0.14 m) and the tea room panel (0.03 m) are geometry; the "+3 mm" frame is gone; chrome and speed lines are +0.8 mm in the map. G9's applied entry moved to G17. The cap 0.330 follows the reviewer's note 1 rather than the 0.270 in fault 2's own amendment (the note is the later and the better-fitting number).
3. Checks. ACCEPTED, built and tested: `pos`, `mask`, G10, G12 to G18, hanging signs, glass, ghosts, wear, all reading pixels (section 8). The test of the checks themselves is in the self-check.
4. Ghosts. ACCEPTED. Mickey's, the fish shop's and the ironmonger's are text blocks with exact words, font, size, colour and share broken (section 5); Rita's and the empty unit's are brush texture only, stated. The reviewer's colour for Mickey's (+3.5 dE) and cap 245, baseline 150 are used; the fish ghost FISHMONGER cap 200, baseline 160, 4 dE, 60 per cent; the ironmonger's cap 190, baseline 170.
5. One designer. ACCEPTED, and done more widely than asked: nine layout classes (name left with a list right; panel left and name right; name only with rules; trade in the end panels; trade above the name; name only offset; bare; and the two centred-stack classes, which three boards use). Four trade lines are off the dotted list (laundry, grocer, newsagent moved to the door glass, tea room); the newsagent is name-only; the ironmonger's trade is in its end panels. Three boards share the centred skeleton (limit five); one trade line is dotted (limit three); trade tracking is at most +0.12 em on at least four boards. G11 added. The laundry's trade is three short lines in its red panel rather than the reviewer's single "SERVICE WASHES & DRY CLEANING" line, which gives a different skeleton; the words are the same.
6. Heritage lean. ACCEPTED. Three plastic or modern fronts: two lit box signs and the tea room's flat caff panel (brown acrylic, white timber frame, cream vinyl, as the reviewer set it), plus the grocer's 1930s glass. The duck-egg ground is gone.
7. Two dark boards. ACCEPTED. The fish board is the sheet's white board, ground (196,202,206) aged, vermilion letters with a black 29 mm shade, rules kept, contrast 2.85. The least ground dE on the street is 14.8, to the laundry. D1 reworded as the reviewer asked.
8. Scallops. Moot with fault 6: deleted.
9. Mounts. ACCEPTED. Brackets on the brick above the cornice at 3.60 to 3.75 m; drops lengthened; lowest points kept (2.65, 2.61, 2.54); the laundry box fixed by its back edge at 3.60 to 4.05 m; `clearance_below_m` is computed.
10. Grocer's glass. ACCEPTED. Three slabs with 3 mm mastic joints at 1380 and 4030, 2 mm bevels; the crack is gone; the method is stated: reverse-painted clear plate glass, the word Vitrolite dropped. The reviewer's other way (black Vitrolite with applied chrome letters) was not taken because it adds letter geometry; both are Judgement.
11. Baked frame highlight. ACCEPTED. Removed from the base colour; planted mouldings (+0.6 mm, 4 mm chamfer) on Rita's, the ironmonger's and the chandler's boards; G2 reads the height map.
12. Dead tube. ACCEPTED. Upper row, x 3300 to 4800, light at 60 per cent; tube-end shadows 60 mm wide and 10 per cent dimmer every 1500 mm in both rows; the emissive check matches.
13. Drink in a preview. ACCEPTED, and the coordinator had already removed the front-scale preview and renamed the board crops. The surviving P1 picture is now two crops of the board's ends, with no name, no window and no front; the overlay is written from it; `make_previews.py` and TARGET.md match; no file names the business (section 9).

Notes: 1 adopted (Mickey's cap 330, baseline 100, 0.60 of the board; width 2118 mm, ink 2996 to 5114, inside the safe zone). 2 adopted (every trade line at least 70 mm; Oswald at least 500; the angle added to the legibility claim). 3 adopted (numerals on two boards). 4 handed to the town and the shop-room builder, not approved. 5 adopted (D5 is no disagreement; FRONTAGE cited). 6 adopted (Old Standard TT Bold; Libre Baskerville gone). 7 adopted (Reserved Font Name "Josefin Sans", parsed from the OFL file). 8 adopted (the empty unit's board is the recipe's colour again; the lighter proposal is withdrawn). 9 adopted (`old_board` under the laundry, newsagent and tea room panels). 10 adopted (the ironmonger's rust is from the board's own nail heads). 11 adopted (the hours plates have their own rule). 12 kept open and flagged for the builder. 13 left open as the reviewer advised. 14 adopted (ten boards, the gap named).

## 13. Self-check

`self_check.py` (8 October 2026), run with the font files fetched from the OFL sources into a scratch folder, writes its result into `target.json` under `self_check`:

**296 of 296 checks pass; 0 fail; 6 reported disagreements or gaps kept visible.**

Groups: 1 printed (24 rows: the numbers read again from the source files, the OFL headers, the fonts used); 2 axis (40: the export's mirror, the door ends, every board's left edge, D6, the hanging signs' sides); 3 photograph wins (6); 4 P1 (20: the saved picture re-measured by code, the drawing laid on it, the overlay written); 5 sheet H1 (5: the board and gilt colours, the white fascia, Mickey's cap); 6 consistency (154: every ink box inside its safe zone and its panel, no overlaps, contrast, ghosts, geometry, signs, glass, words, fonts, paint loss, the height map's range); 7 checks (10: every check has all its fields, the ids are unique, G1 to G18 exist, pixel checks read pixels); 8 pixels (43: the reference renders, mirrored, shifted, jittered and wrong-font tests).

The six reported lines, which are departures kept in the open rather than failures: the newsagent and ironmonger positions against the cast; MINICABS · 24 HOURS against the cast's hours; the parts of P1 not re-measurable on the saved ends; Rita's name larger over its field than P1's; Mickey's cap 0.60 of the board against the sheet's 0.69; the width over cap 6.42 against the sheet's 3.52.

To rebuild: `make_previews.py` (the previews), `make_target.py` (the JSON), `target_drawing.py OUTDIR --json drawing.json --sheet` (the drawings), `self_check.py` (the result). Python with Pillow, NumPy and SciPy; the fonts are fetched with `--fetch-fonts DIR` if they are not on the machine.
