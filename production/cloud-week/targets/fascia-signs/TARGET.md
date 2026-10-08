**Summary line.** Ten fascias for Quay Street, each its own trade, hand and construction (applied brass letters, red sign-writing on dark, gilt on oxblood, a painted-out bare board, a lit plastic box, Art Deco glass, cut vinyl, black shaded roman, soft teal roman, white Egyptian on navy), on the kit's 5410 x 550 mm board at one pixel a millimetre, with the lettering craft measured on one photograph (a 2019 restoration, not 1990) and the Hook sheet, and everything else said plainly to be earlier notes or judgement; self_check passes 158 of 158 and keeps 4 disagreements and gaps visible.

# Fascia signs of Quay Street: the target for unit 4.1

Cloud week 42, written 8 October 2026 by a target writer. Folder: `production/cloud-week/targets/fascia-signs/`. Reference previews: `production/previews/cloud-week/refs/fascia-signs/`. Nothing was committed, no font was added to `production/fonts/`.

Unit 4.1 makes each shop's fascia as a finished 2D texture by script, from this file alone: `target.json` has every number, `target_drawing.py` draws the layouts from it, `self_check.py` tests it against its sources. This page says what the numbers mean, where each came from, and what is not known.

## 0. What rests on what (read this first)

| Kind | What rests on it | How much to trust it |
|---|---|---|
| **Photo, measured today** | P1, a level square-on elevation of a restored Victorian arcade fascia (Poly Haven, CC0): the keyline, the shade, the numerals, the cap height over the lettered field, the tracking. P2 and P3, two weathered painted-timber textures (CC0): the shape and size of paint loss. | Real measurements, but of a **2019 heritage restoration** (P1) and of **cladding planks** (P2, P3). They give craft proportions and the shape of wear. They give no 1990 colour, no 1990 wear amount, no provincial letter size. |
| **Sheet, measured today** | The Hook sheet's Mickey's board and letters: colours (62,75,87) and (167,149,109), the cap over the board, the position over the door. | A generated picture, approved for mood, palette and composition. Colours and ratios, nothing else. |
| **Read** | The game's own files (SCENE-SLOTS.md, the scene spec, the kit README, the recipes, hook-cast hours, DECISIONS 3 Oct), brand bible, OFL.txt of each font. | Exact. `self_check.py` group 1 reads them again. |
| **Earlier notes, cited not re-read** | Picture Sheffield t13138 (25 Aug 1990: a dark fascia sign-written in red; window glass lettered in white) and t13140; Peter Marshall's Hull set 1979-1994 (painted fascias, metal fronts, trade-only boards); note 4's three generations (painted, backlit Perspex, cut vinyl). Written by earlier helpers who looked at the pictures on the PC. | The only 1990 evidence in this target. I could not reach any of those sources today, so I did not re-measure them. |
| **Judgement** | Every colour not measured, every wear amount, the letter sizes of the provincial boards, the hanging signs, the street numbers and "est." years, the glass rows, the fonts chosen to stand in for hand lettering. | Mine. Marked `Judgement` in target.json and below. Any better source overrides it. |

**No 1990 photograph of a fascia was reached.** The network refused Wikimedia, Geograph, Flickr, archive.org, Wikipedia, Picture Sheffield, Historic England and the rest (403 on every connection; list in section 12). The reviewer should treat the ten designs as a considered proposal built on one photographed craft, not as a copy of 1990 provincial boards.

## 1. Sources

All read 8 October 2026. "Used" means a number in target.json comes from it.

| id | URL (or file) | Author | Licence | Taken | Shows | Used |
|---|---|---|---|---|---|---|
| **P1** | https://api.polyhaven.com/files/leadenhall_market, tone-mapped JPG at https://dl.polyhaven.org/file/ph-assets/HDRIs/extra/Tonemapped%20JPG/leadenhall_market.jpg (8192 x 4096) | Andreas Mischok, Poly Haven | CC0 1.0 (polyhaven.com/license) | 19 May 2019 (API `date_taken`) | A covered City of London arcade, **heritage-restored**: red boards, gilt shaded capitals, numbers at both ends, cut-corner keylines, gilt window lettering. Real business names are on it and **must never be copied**. A 2019 restoration, not 1990. | Yes: craft proportions only. Preview: `P1-leadenhall-chamberlain-board-elevation.jpg`, `…-front-scale.jpg`, `…-target-on-photo.jpg` |
| **P2** | https://polyhaven.com/a/blue_painted_planks (2K diffuse) | Rob Tuytel, Poly Haven | CC0 1.0 | published 20 Jul 2018, no photo date | Weathered blue timber cladding, 1.0 m square, flaking paint | Yes: shape and size of paint loss. `P2-bluepaintedplanks-weathering-measure.jpg` |
| **P3** | https://polyhaven.com/a/black_painted_planks (2K diffuse) | Dimitrios Savva, Poly Haven | CC0 1.0 | published 15 Oct 2025 | Black gloss planks, 1.6 m, scuffed | Yes: the luminance spread of worn dark gloss. `P3-blackpaintedplanks-scuff-measure.jpg` |
| **H1** | `production/reference/hook-sheet.png` (preview `production/previews/hook-sheet-2026-10-05.jpg`) | the project's image lane | own work | Sep to Oct 2026 | Mickey's slate board and standing gilt letters; a white, a dark and a cream fascia beyond | Yes: Mickey's colours, cap over board, position. `H1-hook-sheet-mickeys-board-measure.jpg` |
| G1 | `production/previews/proof-2.6-shop-signs-and-bills-2026-10-04.jpg`, `shop-fronts-whole-2026-10-08.jpg` | the project's builds | own work | 4 and 8 Oct 2026 | the fascias as they stand now | Yes: section 2 |
| N1 | `production/research/asset-plan/4-SIGNAGE-AND-WEAR.md`, `0-SOURCES-AND-LICENCES.md`, `SUMMARY.md` s.7 | project research | own work | 3 Oct 2026 | font table; three generations of 1990 fascia | Yes |
| N2 | `production/research/shop-window-interiors/FISHMONGER-2026-10-03.md` (Picture Sheffield t13138, 25 Aug 1990; t13140, c.1989) | Picture Sheffield | reference, linked only | 1989, 1990 | dark sign-written fascia in red; white glass lettering | Yes, as an earlier note |
| N3 | `production/research/casting/notes/names.md` s.4 (Marshall's Hull set, Flashbak, 14 Nov 2024) | Peter Marshall | photographer copyright, linked only | 1979-1994 | naming patterns, trade-only boards ("Fresh Meat", "Boot Repairs", "Refreshments"), "Sail Makers & Ship Chandlers" | Yes, as an earlier note |
| N4 | `production/research/shopfronts/FRONTAGE-2026-10-06.md`, `production/art/shopfront-kit/README.md`, `production/art/fascia-01/01-SPEC-fascia-package.md` | project helpers | own work | 6 Oct 2026 | fascia 0.55 m, 0.12 proud, between consoles 0.295 to 5.705; 1930s structural-glass refits; the guides' depth envelope | Yes |
| F1 | https://raw.githubusercontent.com/google/fonts/main/ofl/<dir>/OFL.txt and the files named in section 8 | the font designers | SIL OFL 1.1, each OFL.txt read whole | n/a | licences and glyph files | Yes: every width in the target is measured on the real files |

Search summaries were not used for any number.

## 2. What is wrong in the game today

Read from `proof-2.6-shop-signs-and-bills-2026-10-04.jpg` and `shop-fronts-whole-2026-10-08.jpg` (by eye), and `make_vignette_2d.py` TRADE_FASCIAS.

1. **One designer.** Every trade board is the same recipe: a name in 200 mm capitals centred, one trade line in 70 mm capitals under it, a faint near-black drop copy 3.5 per cent of the cap away, on a flat colour. Six of eight boards share the same sans for the trade line.
2. **The fish board reads FRESH FISH twice** across one board (`shop-fronts-whole`): the 5650 mm picture is tiled on a wider box.
3. **The launderette is cut off** at the left edge in `proof-2.6`; it is a flat white board with blue letters, not a box sign: no frame, no depth, no lit face.
4. **Mickey's is flat and centred**, a thin gold on flat navy; the sheet has standing gilt capitals on slate blue, over the door.
5. **No relief, no gilding, no border, no number, no ghost of an older trade, no wear on any lettering.** The board is a clean decal on a dirty wall.
6. **Boards run the whole 6.0 m bay** across the pilaster heads and bury the consoles' feet (kit README, "For the session").

## 3. The board

| Number | Value | Kind and source |
|---|---|---|
| Fascia band | 2.85 to 3.40 m up, 0.55 m high, 0.12 m proud of the wall | Read: SCENE-SLOTS.md; `vignette-scene.json` shopfront `fascia_bottom_m` 2.85, `fascia_projection_m` 0.12; `vignette-pieces.json` `east_parade_fascia0` 6 x 0.55 x 0.12 |
| Board between the consoles | 0.295 to 5.705 in the bay = **5410 mm** | Read: kit README ("0.295 to 5.705 in Rita's bay"); the street's box today is 6000 mm and buries the consoles |
| Texture | **5410 x 550 px at 1 px per mm** (double allowed) | Derived |
| Frame | outer 24 mm: highlight on top (+3 to +14 L*), shade below (-14 to -2 L*), baked bevel | Judgement: the kit's board is a plain box |
| Lettered field | 24 mm in on every side = 5362 x 502 mm | Derived |
| Safe rectangle | x 150 to 5260, y 40 to 510 (150 mm off the ends where the consoles stand, 40 mm off the top and bottom) | Judgement |
| Axes | x from the board's left as a viewer facing it sees it; y up from the board's bottom edge | east shops: low street x at the left; west shops (the block is turned a half turn): low street x at the right |
| Pieces that are not the texture | the cornice's shadow, the weather streaks off the lead, the splash, the sun-fade, the reflection: the wear material's and Unreal's | Read: PAINTED-FRONTS-2026-10-07 |

The ten boards, by street position (the recipe's turned west block puts bay 0 at the far end):

| # | id | Side, street x (m) | Trade | Name on the board | Minted name? |
|---|---|---|---|---|---|
| 0 | mickeys | E 3 to 9 | minicab office | MICKEY’S | yes (canon, brand bible, founded 1962) |
| 1 | fish_market | E 9 to 15 | fishmonger | FISH MARKET | yes (DECISIONS 3 Oct "the fishmonger (Fish Market)") |
| 2 | ritas | E 15 to 21 | pawnbroker | RITA’S, PAWNBROKER | yes (cast, DECISIONS) |
| 3 | empty_unit | E 21 to 27 | empty, to let | none | n/a |
| 4 | steam_laundry | E 27 to 33 | launderette | STEAM LAUNDRY | yes (DECISIONS 3 Oct "the Steam Laundry as a launderette") |
| 5 | grocer | E 33 to 39 | grocer | FAMILY GROCER | **no: trade only** |
| 6 | newsagent | W 36 to 42 | newsagent and tobacconist | NEWSAGENT | **no: trade only** |
| 7 | ironmonger | W 30 to 36 | ironmonger | IRONMONGER | **no: trade only** |
| 8 | tea_rooms | W 24 to 30 | tea room | Tea Rooms | **no: trade only** |
| 9 | chandler | E 40 to 46 | ship chandler | SHIP CHANDLER | **no: trade only** |

Five boards are trade-only because canon and the town have minted no proprietor for them. That is correct; no name is invented. FAMILY GROCER is a trade description. The street counts ten shop bays in the scene (RULINGS 2 Oct says "twelve shopfronts"); section 12 says what that leaves open.

## 4. How every fascia is made (rules common to all)

**Order of layers**, bottom to top: ground colour and grain; the frame's baked bevel; the border or panel; old paint under (ghosts, painted-out patches); each text block (shade or extrusion, then size, then face, then outline); the technique's own details; wear (loss, runs, droppings, rust, yellowing, lifted vinyl); then the maps (roughness, metallic, height, emissive) and the layers manifest.

**Letter heights are the H's (or the T of Tea Rooms), in mm at 1 px per mm.** Spacing: each block's tracking is added between glyphs on top of the font's own spacing and kerning; blocks are centred on their ink; round capitals overshoot the baseline and cap line by 1.6 per cent of the cap.

**Block shade** (P1, Photo): the letter's extrusion at 45 degrees down and to the right, length **0.10 of the cap** (4.5 px on a 45 px cap), solid, hard-edged, not a blur. Colour per block. Used on hand-painted and gilded boards only (not on vinyl, applied letters or back-painted glass).

**Keyline** (P1, Photo): one line, thickness 0.027 of the field, inset 0.078 (top) to 0.102 (bottom) of the field, corners cut by a concave quarter circle of radius 0.136 of the field; a panel of a gilded board.

**Numbers at both ends** (P1, Photo): the street number at each end of the panel, 0.91 of the name's cap height, 25 to 46 px inside the keyline in P1. The name's ink sits 1.4 per cent of the panel width left of the panel's centre in P1; a hand's tolerance of +-1.5 per cent is allowed.

**Hand jitter** on painted and gilded blocks (Judgement): each glyph's baseline +-1.6 mm, advance +-1.5 per cent, rotation +-0.35 degree, stroke weight +-3 per cent. None on vinyl, applied or glass-gilt letters.

**Gilding** (Judgement): oil gilding on size for boards; fresh leaf (214,175,74), roughness 0.30, metallic 1; a matt edge 3 to 5 mm where the leaf meets the shade; chips show the size, (150,110,50). Water gilding on glass is seen from behind.

**Wear model** (shape: Photo from P2 and P3; amount: Judgement):

- Paint loss follows the grain: patches elongated **median 3.6:1** (p90 6.7), equivalent diameter **median 8.9 mm** (p90 17.4), largest 577 x 88 mm. P2 loses 28.6 per cent of its area; that is an upper bound for unmaintained cladding. A fascia under its cornice, repainted every few years, loses a stated share: class 1 (sound) 0.1 x, class 2 (tired) 0.2 to 0.3 x, class 3 (neglected) 0.6 x of 0.286. Each shop's `age.loss_fraction` is that share (0.02 to 0.17).
- Worn dark gloss (P3): L* median 8, p95 22; 9 per cent of the area scuffed more than 8 L* brighter.
- Rain runs from the cornice's lead: vertical streaks 5 to 30 mm wide, length per shop, 6 L* darker than the board. Gull droppings on the top 80 mm: pale blotches (230,226,214) with a short run. Rust runs under fixings where the shop's `rust` says so. A film of grime blended in (the share per shop), chalk lift in L* for dark gloss, yellowing for creams and acrylic. How each colour's 1990 value was got from its fresh value is `age_rules` in target.json (Judgement).
- Edges chip 2 to 4 mm where the paint is thick.

**Maps** (4.1's choice of format, the content is given): base colour sRGB; roughness; metallic; height (8-bit, 128 = board face, 1 mm over 127 steps: letter ridge +0.2 mm, keyline +0.15, vinyl +0.08, gilt +0.05, paint loss -0.3 mm, bare board -0.5, box-sign frame +3 mm); emissive on the box sign only; a **layers manifest** (per text block: string, font, size, anchor, ink box, colours). The checks read the manifest.

**Materials** (colours in section 7; full table `materials` in target.json): gold leaf rough 0.30 metal 1; applied brass 0.38, 0.85; signwriter's enamel 0.35 to 0.5 (0.55 chalked); cut vinyl 0.45; back-painted glass 0.08; acrylic face 0.35; anodised bronze 0.35 metal; chrome 0.15 metal; hemp rope 0.80; whitewash 0.90; bare timber 0.85; paint loss 0.85.

## 5. The ten fascias

Layout boxes are in mm on the board, y up, as `[x0, y0, x1, y1]` (the ink, shade included in the effects box in target.json). Contrast is the WCAG ratio of the aged (1990) face over the aged ground. "Cap/field" is the cap over the 502 mm field.

### 0. Mickey's (bay 0, x 3 to 9, proposed No. 1) — applied letters on slate

- **Words:** MICKEY’S (typographic apostrophe), nothing else on the board. Glass (exists, shop-room.py): 0632  960418 and MINICABS · 24 HOURS in gilt.
- **Board:** slate blue-grey **(62,75,87)** [Sheet: mean; p10 (48,60,70), p90 (80,91,102)], eggshell, roughness 0.55, fine orange-peel, grain along (L* +-1.2). No border.
- **Letters:** Marcellus SC, **cap 270 mm** (0.54 of the field), tracking +0.03 em, **emboldened 3 mm each side** (the font's stem 0.09 of the cap becomes 0.11; the sheet's is about 0.15), one block, ink box **[471.7, 130.8, 2238.3, 417.6]**, baseline y 140, cap line y 410, width 1767 mm. Centre **x 1355**, which is the shop door's centre (street x 4.65) and the sheet's 0.245 of the board from the door end.
- **Applied:** stand-off **14 mm** off the board [Judgement; the recipe's RAISED_LETTERS already stands them off], square-cut edges, flanks (112,96,68), face **brass-gilt (167,149,109)** aged [Sheet], p90 (193,171,130); fresh (205,172,86). Roughness 0.38, metallic 0.85. Contact shadow on the board: soft, 6 mm, opacity 0.35, offset (-2,-5) mm. Contrast 3.05.
- **1990:** the sign "hand-painted and repainted a shade off each time" (brand bible): under the letters a **ghost of an older, centred, smaller MICKEY’S** in a blue 3.5 dE off the board, box [1900,120,3510,430], brush-cut edge with a 1 mm ridge, and ten dark pin holes (3 to 4 mm) of the older lettering. Class 2: loss 4 per cent, four rain runs 40 to 160 mm, two gull marks, two short rust runs under the console fixings, chalk +3 L*, grime 7 per cent.
- **Does not match the sheet:** the sheet's letters are taller and narrower (0.69 of the board; width 3.5 caps). Marcellus SC (ruled) is 1.8 times wider; so the cap is set smaller (0.49 of the board; width 6.5 caps) rather than the font squeezed. REPORTED by self_check.

### 1. Fish Market (bay 1, x 9 to 15, proposed No. 3) — red on dark

- **Words:** FISH MARKET; WET FISH · SHELLFISH · SMOKED. Glass (whitewash, Patrick Hand stand-in, [Read] that t13138 had white hand lettering on the glass): FRESH DAILY, SHELLFISH, SMOKED FISH, cap 100 to 120 mm.
- **Board:** charcoal navy **(24,30,40)** fresh, **(40,42,49)** aged, gloss enamel gone flat, roughness 0.58. [Photo, earlier note t13138: "a dark fascia sign-written in red"; the hue is mine.] Two **vermilion rules** 12 mm thick at y 34 to 46 and 504 to 516, x 120 to 5290.
- **Name:** Oswald 600, **cap 290** (0.58 of the field), tracking +0.06, box **[1646.3, 184.1, 3763.7, 481.6]**, baseline 188, width 2117 mm. Face **vermilion (200,40,36)** fresh, **(197,75,62)** aged; block shade **cream (230,220,192)**, 29 mm. Contrast 3.04.
- **Trade line:** Oswald 400, cap 62, tracking +0.20, box [2042.0, 81.3, 3368.1, 144.5], baseline 82, cream (236,226,198) flat, contrast 9.45.
- **1990:** the oxblood-and-cream fish board of the game today is replaced by what the dated photograph shows. A faint ghost of an older lettering, box [900,90,4500,470], 4 dE. Class 2: loss 5 per cent, six rain runs 50 to 200 mm, three gull marks. Chalk +4 L*. The recipe's metal refit is the window frame only; the fascia stays timber.

### 2. Rita’s (bay 2, x 15 to 21, proposed No. 5) — gilt on oxblood

- **Words:** RITA’S; PAWNBROKER. Toplight glass (gilt, one word to a pane): WATCHES, JEWELLERY, LOANS. Hanging: the three balls (section 6). The board's trade words are not repeated.
- **Board:** oxblood **(88,32,38)** fresh, **(93,46,49)** aged [Scaled: the game's board today is 92,39,43], oil gloss now satin, roughness 0.45. **Gilt keyline panel** [Photo P1]: one line 13 mm thick, inset 44 mm, concave quarter-circle corners of radius 70 mm; panel [68, 68, 5342, 482].
- **Name:** Abril Fatface, **cap 230** (0.46), tracking +0.10, box **[2119.7, 217.7, 3290.4, 460.2]**, baseline 221, width 1171. Gold leaf face (214,175,74) fresh, (195,161,77) aged, **black block shade 23 mm** (0.10 of the cap). Contrast 4.49.
- **Trade:** Old Standard TT Bold, cap 84, tracking +0.30, box [2110.8, 96.2, 3299.1, 185.1], baseline 99, same gilt, shade 8.4 mm.
- **Ends:** the number **5** (proposed), Abril Fatface, cap 214 (0.93 of the name), boxes [200, 164.9, 365.1, 384.8] and [5044.9, 164.9, 5210.0, 384.8], baseline 168, shade 21 mm.
- **1990:** class 1 (the model shop is the best kept): loss 3 per cent, three rain runs 40 to 140 mm, one gull mark, a small repaint patch [2300,140,3300,340] 3 dE. **The board is not lit at night;** only the window is (DECISIONS 1 Oct).
- Rita's name is larger over its field (0.46) than the photographed board's (0.31): deliberate, a trading parade not a restored arcade. REPORTED.

### 3. The empty unit (bay 3, x 21 to 27, proposed No. 7) — bare and painted out

- **Words:** none on the board. The letting board (900 x 450 mm, TO LET, red on white, Libre Franklin 800, cap 130, four screws, slightly askew) is a separate asset (`board_to_let`); its place is centred at [2705, 275].
- **Board:** bare soot-darkened timber, **(92,80,68)** fresh, **(98,85,72)** aged [Scaled: the recipe's `bare_timber` is 40,31,25 when freshly bared; a board left for years greys and lightens: Judgement], roughness 0.85, grain along with strong amplitude (L* +-4, 25 to 600 mm).
- **Painted-out patch:** buff (176,170,150) fresh, (165,157,131) aged, box **[1105, 120, 4305, 420]** (3200 x 300 mm) where the last trade's name was, brush strokes along the board, its edge a ragged ridge 0.4 mm high, six old pin holes, **nothing legible**.
- **1990:** class 3: loss 0.17 (0.6 of P2), ten rain runs 60 to 300 mm, six gull marks 20 to 70 mm, three rust runs from old bracket bolts. Whole window whitewashed (ruled 3 Oct, not mine).

### 4. Steam Laundry (bay 4, x 27 to 33, proposed No. 9) — lit plastic box sign

- **Words:** STEAM LAUNDRY; LAUNDERETTE · SERVICE WASHES · DRY CLEANING. Window glass: SERVICE WASHES in white cut vinyl. Hanging: LAUNDERETTE on a double-sided box (section 6).
- **Construction:** a 1970s-80s box sign screwed over the old board: bronze anodised extrusion (96,76,58) fresh, outer **[105, 35, 5305, 515]**, frame 26 mm; **white acrylic face** (238,236,228) fresh, (225,217,197) aged (yellowing, b* +7), face [131, 61, 5279, 489]. The old painted board (cream) shows 105 mm each end and 35 mm top and bottom. Eight pan-head screws on the frame.
- **Name:** Jost 800, **cap 205**, tracking +0.05, box **[1328.2, 214.8, 4081.8, 443.8]**, baseline 225, width 2754. **Royal blue vinyl (24,62,140)**, aged (46,68,136), flat, 0.08 mm, no shade. Contrast 6.5.
- **Trade:** Jost 600, cap 66, tracking +0.14, box [1260.5, 115.1, 4149.6, 188.9], baseline 119, **scarlet vinyl (176,30,34)**, contrast 4.56.
- **Emissive** (lit when the shop is open; hours Mon-Sat 8 to 17.30 [Read: hook-cast], so lit on winter afternoons): face colour at full; two tube rows show as +6 per cent bands at 25 and 75 per cent of the face height; the last 250 mm at each end 12 per cent dimmer; **one tube dead** (a band 500 to 700 mm wide, 15 per cent darker).
- **1990:** class 2: yellowing at the edges, grime streaks off the top edge (seven, 60 to 220 mm), a lifted corner of the lower frame. No paint loss on the face.

### 5. Grocer (bay 5, x 33 to 39, proposed No. 11) — Art Deco glass

- **Words:** FAMILY GROCER; PROVISIONS · FRUIT · VEG. Trade only. Fanlight number 11.
- **Construction:** a **1930s refit in back-painted structural glass** [N4: "the 1930s used … bronze, chrome and Vitrolite"; Vitrolite "cracks low down and round doors, patched with painted ply"]: slab [40, 25, 5370, 525], **dark bottle green (30,58,46)** fresh, (36,61,49) aged, roughness **0.08**; chrome edge strip 12 mm (196,200,202); **three chrome speed lines** 6 mm thick at y 262, 282, 302, x 52 to 640 and 4770 to 5358.
- **Name:** Josefin Sans 700, **cap 190**, tracking +0.14, box **[1403.8, 228.9, 4006.2, 428.7]**, baseline 231, **cream (236,226,198)** back-painted, flat, no shade. Contrast 7.75.
- **Trade:** Josefin Sans 600, cap 58, tracking +0.30, box [1913.8, 126.3, 3496.1, 189.0], baseline 129.
- **1990:** a crazed diagonal crack across the right third (three branches), patched with a painted board 120 x 300 mm; five rain runs; grime film 6 per cent. No paint loss (glass).

### 6. Newsagent and tobacconist (west bay 0, x 36 to 42, proposed No. 18) — cut vinyl on red

- **Words:** NEWSAGENT; TOBACCONIST · CONFECTIONER. Trade only. Window or door glass: NEWSPAPERS · MAGAZINES in white vinyl.
- **Board:** signal red **(176,36,40)** fresh, (175,68,63) aged, gloss, tired, roughness 0.5. One **black vinyl stripe** 26 mm at y 40 to 66, x 24 to 5386.
- **Name:** Libre Franklin 900, **cap 240**, tracking +0.05, box **[1537.7, 225.8, 3872.3, 472.2]**, baseline 229, width 2335, **cream vinyl (236,226,198)**, flat, no shade. Contrast 4.4.
- **Trade:** Libre Franklin 700, cap 66, tracking +0.16, box [1804.8, 122.1, 3605.1, 189.9], baseline 123.
- **1990:** computer-cut vinyl (note 4: "beginning to appear by the end of the decade") on a plain refit. Two lifted corners (the stripe's right end lifts 30 mm), no letter lost, loss 6 per cent on the red between, five rain runs, two gull marks.

### 7. Ironmonger (west bay 1, x 30 to 36, proposed No. 16) — shaded roman on buff

- **Words:** IRONMONGER; TOOLS · HARDWARE · PARAFFIN. Trade only. Toplight glass: EST. 1884 (proposed). Hanging: KEYS CUT board (section 6).
- **Board:** buff **(200,188,156)** fresh, (188,173,136) aged [Scaled: the game's is 190,176,140], gloss chalked and grimy, roughness 0.55. **Double rule**: black line 8 mm inset 36 mm, a vermilion hairline 3 mm 14 mm inside it, square corners with 30 mm black corner blocks; panel [79.5, 79.5, 5330.5, 470.5].
- **Name:** Libre Baskerville 700, **cap 180**, tracking +0.08, box **[1618.5, 231.7, 3791.6, 416.3]**, baseline 234, width 2173, **black (26,26,24)** (aged (40,39,37)), **vermilion block shade 18 mm**. Contrast 6.73.
- **Trade:** Libre Baskerville 400, cap 56, tracking +0.20, box [1857.4, 135.3, 3552.6, 192.7], baseline 136.
- **Ends:** the number 16 (proposed), cap 167, boxes [210, 188.8, 450.7, 360.2] and [4959.3, 188.8, 5200, 360.2], baseline 191, vermilion shade 16.7.
- **1990:** the metal window refit did not reach the board. Faint older lettering ghost [800,100,4600,430]. Class 2: loss 6 per cent, rust under the hanging-sign bracket bolts, chalk +4 L*, grime 12 per cent.

### 8. Tea Rooms (west bay 2, x 24 to 30, proposed No. 14) — soft roman on duck-egg

- **Words:** Tea Rooms (the only mixed-case name); TEAS · LIGHT LUNCHES · HOME BAKING. Trade only (hook-cast calls it "the cafe"). Window glass: Home Baking in gold leaf.
- **Board:** duck-egg blue-green **(158,192,182)** fresh, (151,177,160) aged, gloss a few years old, roughness 0.42. Scalloped valance along the bottom: circles of radius 26 mm, pitch 80 mm, x 100 to 5310, centres y 50, deep teal, with a 6 mm rule above at y 86 to 92.
- **Name:** Fraunces 900 (Softness 100, Optical Size 144), **cap 215** (the T's), tracking +0.02, box **[1932.8, 244.0, 3477.1, 468.5]**, baseline 248, **deep teal (24,74,76)** (aged (44,82,82)), no shade. Contrast 3.74.
- **Trade:** Fraunces 600, cap 52, tracking +0.24, box [1738.0, 154.7, 3671.9, 209.4], baseline 156.
- **1990:** a 1980s refit, hand-painted; class 1: loss 2 per cent, three rain runs, one gull mark.

### 9. Ship chandler (east_chandler, x 40 to 46, proposed No. 13) — white Egyptian on navy

- **Words:** SHIP CHANDLER; ROPE · PAINT · CHARTS · TWINE. Trade only. Toplight glass: EST. 1879 (proposed). Hanging: CHANDLERY board (section 6).
- **Board:** navy **(28,42,78)** fresh, (44,53,83) aged, salt-weathered gloss, roughness 0.50; **painted rope keyline** 12 mm, inset 34, corner radius 40, strand pitch 28 mm, hemp (196,176,136); panel [70, 70, 5340, 480].
- **Name:** Alfa Slab One, **cap 170** (0.34, the smallest), tracking +0.05, box **[1628.6, 235.9, 3781.4, 412.1]**, baseline 239, width 2153, **signwriter's white (238,234,220)**, **black block shade 17 mm**. Contrast 8.48.
- **Trade:** Libre Franklin 700, cap 58, tracking +0.20, box [1870.5, 140.2, 3539.6, 199.8], baseline 141, cream.
- **Ends:** the number 13 (proposed), cap 158, boxes [210, 193.2, 442.5, 356.8] and [4967.5, 193.2, 5200, 356.8], baseline 196, shade 15.8.
- **1990:** metal window refit under a painted board; class 2: loss 7 per cent, six rain runs 40 to 200 mm, four gull marks 20 to 60 mm, three rust runs, salt bloom whiter along the lower edge.

### Why no two are alike

Nine different name-line fonts on the nine lettered boards (Marcellus SC, Oswald, Abril Fatface, Jost, Josefin Sans, Libre Franklin, Libre Baskerville, Fraunces, Alfa Slab One), ten distinct grounds (smallest dE76 between aged grounds 14.9), eight construction kinds (applied letters, sign-written, gilded, bare, box sign, glass panel, cut vinyl, hand-painted), nine different name caps from 0.34 to 0.58 of the field. `distinctness` in target.json lists every pair; `self_check` fails if one pair comes within 14 dE or shares a font.

## 6. Other signage

All Judgement unless marked. Geometry in metres, lettering in mm. Full numbers in `projecting_signs`, `glass_lettering`, `small_panels`.

**Projecting and hanging signs (four, as the asset plan's "3 to 4").** Each has a clear drop of at least 2.5 m and a projection of 1.0 m at most (self_check tests it).

| id | What | Where and size |
|---|---|---|
| ritas_three_balls | **The pawnbroker's three balls**: three gilt balls, 0.26 m across, two above one, on a wrought-iron scroll bracket (20 x 8 mm bar, four scrolls, a hook and a ring; plate 0.18 x 0.30 m, four bolt heads). No lettering, no mark. | Arm at 3.28 m, projection 0.85 m, on the left pilaster of bay 2 (street x 15.175); ball centres (0.57, 3.00, -0.14), (0.57, 3.00, +0.14), (0.57, 2.78, 0); lowest point 2.65 m. Gilt paint on sheet metal, roughness 0.38, metal 0.8, scuffed where hands reach; iron black, rust at the bolts. No photograph of one was reached. |
| steam_laundry_box | A double-sided lit box: bronze extrusion, white acrylic faces, LAUNDERETTE in royal blue vinyl, Jost 800, cap 60, tracking +0.03; each face reads left to right from its own side. | 0.62 out x 0.45 high x 0.14 thick, arm at 2.95 m, left pilaster of bay 4 (street x 27.175). Emissive with the box sign above. |
| ironmonger_hanging_board | A hanging painted board on a forged bracket (the KCD2 frame's kind): KEYS CUT, Libre Baskerville 700 cap 92, black on buff with a vermilion shade 9 mm, a black rule 6 mm inset 20 mm; both faces alike. | Board 0.55 x 0.38 x 0.04 on two rings, arm at 3.05 m, projection 0.70. |
| chandler_hanging_board | CHANDLERY, Alfa Slab One cap 105, white on navy, black shade 10 mm, a rope border; both faces alike. | Board 0.80 x 0.50 x 0.05 on two four-link chains, arm at 3.10 m, projection 0.90. |

**Glass lettering** (gilt on the inside of the glass, white vinyl or whitewash as listed): Mickey's existing number and MINICABS · 24 HOURS (Read); Rita's toplights WATCHES · JEWELLERY · LOANS, cap 90, gold leaf, black shade, one to a pane, centre 2.64 m; the fish shop's whitewash FRESH DAILY, SHELLFISH, SMOKED FISH (Read for the technique, Judgement for the words); the launderette's SERVICE WASHES; the newsagent's NEWSPAPERS · MAGAZINES; the tea room's Home Baking; EST. 1884 and EST. 1879 on the toplights. **Street numbers** 1, 3, 5, 7, 9, 11, 13 east and 14, 16, 18 west in gilt or vinyl on each side-door fanlight, cap 110, centre 2.18 m. **All numbers and years are proposed, not minted** (section 12).

**Small panels.** The letting board above. An **hours plate** per shop that has hours in the cast (Rita's, fish, laundry, newsagent, tea rooms): white enamel 300 x 190 mm, black Libre Franklin 700 cap 24, blue border 4 mm, rolled edge, chips to black iron at the corners, centre 1.45 m up on the door glass or pilaster; the words are read from `hook-cast.json` at build time (Rita's: Mon, Tue, Thu to Sat 9 to 5.30; Wed 9 to 1), not written here.

## 7. Palette

Fresh is what the renderer paints; 1990 is the median the checks expect. Kind: Sheet, Scaled (the game's own file), Photo, Read, Judgement.

| Name | Plain name | Fresh sRGB | 1990 sRGB | Kind |
|---|---|---|---|---|
| slate | slate blue-grey | 52,66,80 | **62,75,87** | Sheet |
| brass_gilt | dull brass-gilt | 205,172,86 | **167,149,109** | Sheet |
| brass_side | letter flank | 120,98,58 | 112,96,68 | Judgement |
| gold_leaf | gold leaf | 214,175,74 | 195,161,77 | Judgement |
| shade_black | sign-writer's black | 22,20,20 | 37,35,34 | Photo (P1 shade (66,53,42) under warm lamps, taken as near-black) |
| oxblood | oxblood | 88,32,38 | 93,46,49 | Scaled (game 92,39,43) |
| charcoal_navy | charcoal navy | 24,30,40 | 40,42,49 | Judgement (t13138's "dark") |
| vermilion | signwriter's vermilion | 200,40,36 | 197,75,62 | Judgement |
| cream / cream_shade | cream | 236,226,198 / 230,220,192 | 222,209,175 / 216,203,170 | Judgement |
| bare_timber | bare soot-darkened timber | 92,80,68 | 98,85,72 | Scaled, Judgement |
| painted_out | buff grey | 176,170,150 | 165,157,131 | Judgement |
| acrylic_white | white acrylic face | 238,236,228 | 225,217,197 | Judgement |
| vinyl_blue / vinyl_red | royal blue / scarlet | 24,62,140 / 176,30,34 | 46,68,136 / 173,50,46 | Scaled (the game's 28,64,140 and 176,30,34) |
| bronze_anodised | bronze | 96,76,58 | 84,68,53 | Judgement |
| deco_green_glass | bottle-green glass | 30,58,46 | 36,61,49 | Judgement |
| chrome | chrome strip | 196,200,202 | 178,181,183 | Judgement |
| signal_red / vinyl_black / vinyl_cream | newsagent's board, stripe, letters | 176,36,40 / 28,28,28 / 236,226,198 | 175,68,63 / 39,38,37 / 235,227,201 | Judgement |
| buff_board / sign_black | ironmonger | 200,188,156 / 26,26,24 | 188,173,136 / 40,39,37 | Scaled (game 190,176,140), Judgement |
| duck_egg / deep_teal | tea room | 158,192,182 / 24,74,76 | 151,177,160 / 44,82,82 | Judgement |
| navy / white_paint / hemp | chandler | 28,42,78 / 238,234,220 / 196,176,136 | 44,53,83 / 223,216,196 / 184,162,118 | Scaled (game 30,40,70), Judgement |
| whitewash | whitewash | 238,236,228 | 224,218,204 | Read (white on the glass, t13138) |

Other sheet colours measured but **not used**: the sheet's white fascia (204,204,204), dark one (99,81,72), cream one (128,101,98) in shade.

## 8. Fonts

Every file named was read at https://raw.githubusercontent.com/google/fonts/main/ofl/<dir>/ on 8 October 2026 and its OFL.txt read whole: the header is "SIL OPEN FONT LICENSE Version 1.1" in all ten. The letters are rendered into pictures; the OFL puts no restriction on a picture made with the font (earlier note FAQ 1.1, 1.13); the font file itself is not modified or redistributed by this target. Unit 4.1 adds the files to `production/fonts/` with their OFL.txt, as the rule says.

| Key | Family | File (in google/fonts, ofl/…) | Reserved name | Looks like | Used for |
|---|---|---|---|---|---|
| marcellus-sc | Marcellus SC (Astigmatic) | marcellussc/MarcellusSC-Regular.ttf | Marcellus | flared humanist capitals; already in `production/fonts` | Mickey's, glass number |
| abril-fatface | Abril Fatface (TypeTogether) | abrilfatface/AbrilFatface-Regular.ttf | Abril, Abril Fatface | fat-face Didone | Rita's name |
| old-standard-tt-bold | Old Standard TT (Kryukov) | oldstandardtt/OldStandard-Bold.ttf | none | Victorian modern roman | Rita's trade, glass |
| oswald | Oswald | oswald/Oswald[wght].ttf, wght 600 and 400 | none | condensed gothic block | Fish Market |
| jost | Jost (Owen Earl) | jost/Jost[wght].ttf, wght 800 and 600 | none | Futura-like | Steam Laundry |
| josefin-sans | Josefin Sans (Orozco) | josefinsans/JosefinSans[wght].ttf, wght 700 and 600 | Josefin | Art Deco geometric | Grocer |
| libre-franklin | Libre Franklin (Impallari) | librefranklin/LibreFranklin[wght].ttf, 900 and 700 | none | Franklin Gothic | Newsagent, chandler trade line, plates |
| libre-baskerville | Libre Baskerville (Impallari) | librebaskerville/LibreBaskerville[wght].ttf, 700 and 400 | Libre Baskerville | sturdy roman | Ironmonger |
| fraunces | Fraunces (Undercase) | fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf, wght 900 and 600, Softness 100, Optical Size 144 | none | soft heavy "Cooper/Windsor" roman | Tea Rooms |
| alfa-slab-one | Alfa Slab One (JM Solé) | alfaslabone/AlfaSlabOne-Regular.ttf | Alfa Slab | fat Egyptian | Chandler |
| patrick-hand | Patrick Hand | already in `production/fonts/patrick-hand` | | neat hand print | fish shop's whitewash hand, with jitter |

Not used: Overpass (American highway gothic, ruled out), any Apache or GPL face, Transport, Gill Sans, Futura, Helvetica, Franklin Gothic (Jost, Libre Franklin and Oswald are the stand-ins). A real signwriter drew every letter; these are starting shapes, which is why hand jitter, shade, gilt edges and wear are specified.

## 9. Where the photograph wins

| # | Element | The book or the game said | The photograph says | Chose |
|---|---|---|---|---|
| D1 | The fishmonger's colour way | oxblood board, cream letters (game; recipe's "wave") | t13138 (25 Aug 1990, earlier note): dark fascia sign-written in red | the photograph: dark ground, red letters |
| D2 | Shade under signwriting | a near-black copy 3.5 per cent of the cap away on every board (game) | P1: a solid block shade 45 degrees, 0.10 of the cap, near-black | the photograph, only on painted and gilded boards |
| D3 | Numbers at the ends | none | P1: both ends, 0.91 of the cap | the photograph, on Rita's, the ironmonger, the chandler (numbers proposed) |
| D4 | Keyline corners | a plain rectangle | P1: concave quarter circle, radius 0.136 of the field | the photograph, on Rita's |
| D5 | Fascia depth | council guides: "do not exceed 380 mm" (fascia-01 spec, search summaries, PDFs blocked) | P1: lettered field 0.45 to 0.49 m (door-leaf scale), board with bead 0.53 to 0.57 m | the street's 0.55 m stands |
| D6 | Mickey's name position | centred (game today) | the sheet, not a photograph: over the door, 0.245 of the board from the door end | the sheet (variant V4 centres it) |
| D7 | Size of the name | 200 mm cap on every board (game), 0.43 of the field | P1 0.31; the sheet 0.69 | 0.34 to 0.58 by trade |

## 10. The checks for unit 4.1 (`checks` in target.json; 165 of them)

Each has an id, a name, a scope, what to measure, the expected value, a tolerance, a unit, the method and whether it reads pixels or the layers manifest. Groups:

- **G1** size 5410 x 550. **G2** frame bevel (top strip lighter, bottom darker). **G3** no repeated word on a board (the FRESH FISH FRESH FISH fault). **G4** every string in the manifest is in `approved_words` (exact) and none in `forbidden_patterns`. **G5** no tiling period under 5 m in the ground (autocorrelation peak under 0.55). **G6** grain along the board (0 to 8 degrees). **G7** distinct boards. **G8** contrast of every name line. **G9** relief present by technique.
- **Per shop:** ground colour (median within dE76 9); **per block:** cap height (+-3 per cent or 2 mm), ink width (+-4 per cent or 6 mm), inside the safe rectangle, contrast (not below 0.85 of nominal and 2.2), face colour (dE 14), block shade (colour dE 16, length +-2 mm); border lines (+-4 mm); paint loss (fraction +-0.012 absolute or 50 per cent, median aspect at least 2.0, equivalent diameter 4 to 16 mm); the box sign's emissive map; Rita's board unlit.
- The approved words are **44 strings** (listed in `approved_words`, 72 distinct word parts); the numerals and "EST." rows are in it as proposed.

## 11. Self-check result

`python self_check.py` (Python `/home/user/.bpyenv/bin/python`), run 8 October 2026 after the last change:

**158 of 158 checks pass; 0 fail; 4 reported disagreements or gaps kept visible.**

- Group 1 (printed): the fascia numbers return from SCENE-SLOTS.md, the scene spec, the kit README and `vignette-pieces.json`; all ten street x ranges from the scene's blocks (the west block turned); the 3 October trades; the recipe's bays; hours exist for each plate shop; Mickey's minted; the ten OFL.txt headers read.
- Group 2 (photo wins): D1 to D7 hold in the target's own numbers.
- Group 3 (P1): the code re-measures the saved preview (cap top and bottom, keyline top, bottom, left, right, name extent, field top and bottom) and agrees with my hand numbers within 3 preview px (largest 1.9 px); the drawing's edges, laid on the photograph at a scale fitted on **one dimension only** (the field's height, 136.5 px = 502 mm, 0.2719 px/mm), fall within 2.3 px of the photograph's (3 px is the stated error; one preview px is about 3.7 mm at the board).
- Group 4 (sheet): Mickey's board and letter colours re-measured from `hook-sheet.png`.
- Group 5 (consistency): every ink box inside the safe rectangle; no overlaps; panels hold their words with 15 mm to spare; contrast at least 2.2; pairwise distinct; words clear of the content rule, the real-mark lists and RealWorld.cs; every stored ink width equals a fresh measure on the real font files; P2's loss fraction recomputed from the texture.
- Group 6 (checks): well formed, unique, the target meets its own nominal values.

**Reported, kept visible:** (1) the cast and the recipe disagree about the newsagent's place (section 12); (2) Rita's name is larger over its field than P1's; (3) Mickey's cap over the board is 0.49 against the sheet's 0.69; (4) Mickey's name width over its cap is 6.5 against the sheet's 3.5.

## 12. What could not be settled

1. **No 1990 photograph of a fascia was reached** (above). Everything provincial rests on the earlier notes and judgement. The reviewer should expect the ten designs to need a second pass when the network opens.
2. **Where the newsagent and the ironmonger stand.** The recipe (`terrace-front.py`, a west block turned a half turn) puts the newsagent at street x 36 to 42 and the ironmonger at 30 to 36. `hook-cast.json` puts the newsagent's pension counter at **x 32** and "Hal's shop, the same block's far end" at **x 39**. One of them is wrong. The boards are keyed by trade, so a swap is a rename. A town task, not mine to rule.
3. **Hal's shop.** The cast has a keeper "Hal, who keeps the coin shop that sells no coins" at x 39; DECISIONS 3 Oct has no such shop in the west row. If the town keeps it, it needs a fascia (HAL'S is minted in the cast; its trade line is the town's to say). The scene has **ten shop bays** and RULINGS 2 Oct counts **twelve** shopfronts; I made ten.
4. **Street numbers, "est." years, the hanging signs' words** (KEYS CUT, CHANDLERY), the glass words and every colour not measured are proposed. The fascias work without the numbers and years (variant V3).
5. **The existing glass number 0632 960418** (shop-room.py) uses 0632, which from memory (not checked) was Newcastle upon Tyne's code until 1992. Meridian is fictional. Not changed: it is another family's.
6. **P1's absolute scale** rests on the door leaf being 2.1 to 2.3 m (it gives a camera 0.93 m up, low for a panorama); every ratio used is scale-free, and the one fitted dimension is stated.
7. **Reading at the game camera.** At 15 arcminutes a capital is readable at about 230 x its height: the 52 to 66 mm trade lines to about 12 to 15 m, the 170 to 290 mm names to 40 to 66 m (Judgement). Nobody has looked at these at the game's exposure.
8. **Night.** Only Rita's window is ruled lit. The box sign's emissive is specified; whether it is on after dark follows the town's hours (the shop shuts at 17.30).
9. **The wear amounts** are a stated share of two cladding photographs; no fascia was measured.

### What I would read when the network opens

Picture Sheffield t13137, t13138 and t13140 at full size (the fishmonger's board, the red lettering's height over the board, the glass); Peter Marshall's Hull set 1979-1994 and the Brixton 1987 fishmonger (fascia depth, letter height over board, how many box signs, painted-out boards); Geograph 1996 to 2000 northern parades (the three generations side by side, a bare board); Historic England's "Shopping Parades" (fascia depths and lettering of 1900-1935 parades); signpainting.co.uk "Letters Potent: the modern age" and Designing Buildings "Shop signs" (the dates of the shift to Perspex and vinyl); public-domain sign-writing and gilding manuals on archive.org or HathiTrust (the proportions of shade, the gilding method, numeral sizes); Wikimedia Commons categories of UK shop fronts of the 1980s, with the author, licence and date read on each file page.

### Unreached today

commons.wikimedia.org, geograph.org.uk, flickr.com, archive.org, en.wikipedia.org, picturesheffield.com, flashbak.com, historicengland.org.uk, signpainting.co.uk, hathitrust.org, britishnewspaperarchive.co.uk, bygonely.com: the proxy refused every connection (403). ambientcg.com answered its API but refused every file download (403), so no ambientCG photograph was measured. Reached: polyhaven.com (API and files), raw.githubusercontent.com.

## 13. Files

| File | What |
|---|---|
| `TARGET.md` | this page |
| `target.json` | the numbers (written by `make_target.py`; `self_check` is written into it by `self_check.py`) |
| `target_drawing.py` | `python target_drawing.py OUTDIR [--json drawing.json] [--sheet]`: draws each board at 1 mm a pixel (boxes, baselines, cap lines, borders, ghosts), the four projecting signs in side elevation and the P1 template, from target.json alone |
| `self_check.py` | `python self_check.py [--fonts DIR \| --fetch-fonts DIR]`: the test above; writes `self_check` into target.json and the overlay picture |
| `make_target.py` | author tool: the hand decisions and the computation of widths, boxes, contrast, checks; needs the font files (`--fonts DIR`) |
| `make_previews.py` | rebuilds the reference previews from Poly Haven (CC0) |
| `production/previews/cloud-week/refs/fascia-signs/` | `P1-…-board-elevation.jpg`, `P1-…-front-scale.jpg`, `P1-…-board-target-on-photo.jpg`, `P2-…`, `P3-…`, `H1-…`, `L1-quay-street-ten-fascias-layout-sheet.jpg`; each at most 1200 px, under 300 KB |

Credit for the previews: P1 Andreas Mischok, P2 Rob Tuytel, P3 Dimitrios Savva (Poly Haven, CC0); H1 the project's Hook sheet; L1 the project's drawing. The photographs are for measuring only: never placed in the game, never traced into a texture, never fed to an image model; the real business names visible on P1 are never to be copied.
