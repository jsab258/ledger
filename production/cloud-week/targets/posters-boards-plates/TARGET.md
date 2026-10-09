# Quay Street's paper and small boards: the exact target

76 sheets, cards, boards and plates for Quay Street's paper and small boards: 16 bills and stickers (the poll-tax set, the chapel hall's, the fights, the market, the Tivoli, two goods), 7 ferry and Harbour Board sheets, 5 police and council notices, 35 shop-window and newsagent cards, 4 letting boards with a proposed agent, 9 street name plates, 2 notice cases; every word ours and listed, autumn 1990 dates with the weekdays computed, four ageing classes, a layered paste plan for the quay gable and the empty unit's glass, 70 placements and 473 checks.

Cloud week 42, written 8 to 9 October 2026. FIRST TRY. Three 2D units build from `target.json` and this page: 4.2 posters and notices, 4.3 "To Let" boards, 4.4 street name plates. Nothing is committed.

Self-check: **SELF-CHECK posters-boards-plates: 215 checks, 215 passed, 0 failed, 13 reported** (see section 14).

Plain summary. Seventy-six sheets, cards, boards and plates, every word ours, listed and checked against the content rule, canon and the 1990 calendar. The street's biggest piece of paper is the east parade's **quay gable** (the brick end wall of Mickey's block at street x 3, the big wall at the right of the hook frame): three layers of fly-posted bills there, twelve bills and three stickers, with a ferry timetable case and a Harbour Board notice case at its far end. The empty unit's whitened glass carries eight more. The plain west terrace's six brick piers carry seven. The poll tax is an invented local campaign; the chapel hall (the game's own `chapel_hall`) holds the jumble sale, the dance and the advice evening; the Tivoli's two invented films have quads and a programme; the fights are at an invented Drill Hall; the market bill matches the cast's market days to the hour. The letting boards carry a PROPOSED agent (ARMITAGE & STOBBS, not minted) and a no-agent variant. The street plates are sized from their names, Marcellus SC capitals 90 mm tall, with the district's name as a small line and no council. What the first try could not do is stand on a photograph: see section 0.

Files in this folder:

- `target.json`: the whole target (76 items, 70 placements, 2 cases, a card board, 6 piers, 8 shop fronts, 473 checks, the self-check result).
- `make_target.py`: the author tool that writes `target.json` (every width is measured on the real font files).
- `target_drawing.py`: draws every item's boxes, baselines and clean lettering at 1 mm to the pixel, the surfaces' elevations and the cases, from `target.json` alone, into a folder given on the command line, plus the polygons as JSON.
- `self_check.py`: its checks and their count are in section 14; it writes its result into `target.json` under `self_check`; `--fetch-fonts DIR` fetches the four fonts not in `production/fonts`.
- `make_previews.py`, `make_doc.py`: rebuild the previews and this page.
- Previews, in `production/previews/cloud-week/refs/posters-boards-plates/`: `P1-urban-street-01-notice-case.jpg` (the one photograph measured, windows masked), `P1-...-target-on-photo.jpg` (the proportions laid on it), `L1` to `L4` (layout sheets of every item), `L5` (the paste plan of the gable and the empty unit's glass).

## 0. What this target rests on, in plain words

- **Photographs measured today: one, and it is not the period.** Poly Haven's Urban Street 01 (CC0, Andreas Mischok, 18 August 2019) shows four glazed notice cases, blue steel, 2000s. I measured their VERTICAL proportions (header 0.152 of the height, window 0.763, foot 0.085, side bands 0.205 of the apparent width, each with its error) and used them only as a cross-check of a glazed case's shape. Nothing else in this target is measured on a photograph.
- **Photographs looked at and not used.** Eight other Poly Haven panoramas (London streets and docks, Cambridge, a Dublin quay): none shows a street name plate, a letting board or a poster hoarding that could be measured. Bethnal Green Entrance has a stickered modern pole plate and, in the same frame, a council byelaw sign about alcohol: nothing from it is kept, no crop, no file.
- **Earlier notes (they read period photographs and search summaries on the PC; read here, not re-measured):** the 1990 mix of Letraset, photocopy and two-colour print (asset-plan note 4); the 1952 Kindersley recommendation for name plates (street-clutter note); the winter timetable date of 1 October 1990 and the pasted-over summer sheet (transport-timetables note, the brand bible); cod at about 2.60 a lb in 1990 (the fishmonger note, ONS); the Harbour Board's blue and white enamel and glass case with notices drawing-pinned and curling (the brand bible); the hours, the market's days and the chapel hall (`hook-cast.json`).
- **Search summaries (leads, never numbers):** modern street-plate specifications (90 mm capitals, 150 to 230 mm plates, 12 mm borders, 11 SWG aluminium), a Hull caption on 1920s to 1930s cast plates, a statement that there is no national plate design and that each council chose its own, a Hackney Museum 1990 'Pay No Poll Tax' sheet on yellow paper in red ink, the Double Crown sheet. The pages themselves were not fetched (DNS and 403).
- **Judgement:** every size, colour, wording, price, ageing number and placement not listed above. Section 1 says the kind of each class of number.
- **The honest summary:** this is the weakest of the family targets on its photographic side. It is strong where the project's own files decide: the streets and districts canon mints, the shops' hours and the market's days, the fascia target's positions and left-right rule, the plain row's bay layout, the 1990 calendar, the content rule and the lists of real names. A fresh reviewer should look hardest at sizes and at ageing.

What I would read once the network opens (all unreached today):

- Geograph and Commons photographs of street name plates dated 1985 to 1995 in a northern English port or mill town: plate depth, letter height, border, fixings, whether a postal district or the council's name is on it (the biggest gap: nothing about plates is measured in this target)
- Photographs of estate agents' and commercial letting boards of 1988 to 1992 (Peter Marshall's Hull set; Picture Sheffield): size, layout, colours, how it is fixed to a fascia
- Photographs of fly-posted hoardings and gable walls, 1988 to 1992 (Hackney Museum and Picture Sheffield): the share of the wall covered, layer count, bill sizes in use, how torn and faded
- A 1990 provincial cinema bill and quad, and a 1990 wrestling or boxing bill (Sheffield's National Fairground and Circus Archive; V&A): type, colours, billing block
- 1990 council notices: planning notices, road closure orders, police appeal sheets (local archives, Hackney Archives 2020/26): layout, paper, how fixed to a column
- The Hackney 'Pay No Poll Tax' sheet and the Wandsworth screenprint (V&A O203232/3): colours, type, the imprint line
- The DfT circular 3/93 itself and Alistair Hall's London Street Signs (2020): plate sizes and postal districts
- Liberation Sans/Serif TTFs, if the builder wants them over Archivo and Libre Baskerville

## 1. Reading this file

- Units. Every item has its own frame: **x in millimetres from the viewer's LEFT edge as seen IN THE GAME, y UP from the item's bottom edge**; a block's `baseline_mm` is measured up from the bottom edge. Authoring scale: 2 pixels to the millimetre for paper and cards (so a 2.4 mm imprint is 4.8 px), 1 pixel to the millimetre for boards and plates. Surfaces use metres: `u` from the surface's viewer's-left edge, `z` up from the pavement; street x is metres along Quay Street (0 at the quay end), the same in the recipe and the game.
- Left and right are the VIEWER'S, in the game, by the fascia target's rule: the game mirrors the recipe, so low street x is on the viewer's RIGHT looking at the east parade and on the viewer's LEFT looking at the west block. Every sheet's x runs from the viewer's left; the quay gable is read looking +x, with the front corner at the viewer's left.
- Evidence kinds: Read (printed), Scaled (off a drawing or the game's files), Photo (measured on a photograph today), Derived (computed), Judgement (mine, to be overturned), Lead (a search summary, never a number).
- Colours are sRGB 0 to 255, contrast is WCAG, dE is CIE76. Aged colours are for four classes (section 4).

The kind of each class of number in this target:

| Numbers | Kind | Source |
|---|---|---|
| sheet sizes (crown, double crown, quad, four-sheet; A2 to A6) | Derived | imperial names x 25.4 mm; ISO 216 halving; the Double Crown name is also a Lead |
| ink width of every line, cap ratios, plate lengths, tide and ferry times | Derived | measured on the real font files / computed in make_target.py, re-measured by self_check.py |
| the calendar: every weekday and date | Derived | datetime, 1990; 1 October 1990 was a Monday |
| street x of the shops, door ends, hanging signs, the fascia, the letting board's centre | Read | the fascia target, SCENE-SLOTS.md, vignette-scene.json |
| the six piers, the glass, the shop widths | Derived | terrace-front.py's plain-row layout and the shopfront numbers (0.35, 3.562, 0.9, 0.838) |
| shop hours, the market's days and hours, the chapel hall, Hal's break, the ferry's last crossing | Read | hook-cast.json, tier2-batch-1.json, the brand bible |
| the cod price | Read (earlier note) | ONS series CZOL via FISHMONGER-2026-10-03.md |
| the case proportions (0.152, 0.763, 0.085, 0.205) | Photo | one 2019 modern case, with errors; NOT the period |
| 90 mm capitals, 175 to 240 mm plates, 12 mm border, 30 mm fixings | Judgement on a Lead | modern specifications in search summaries |
| every other size, layout, colour, cap, ageing, wear and placement number; every price but the cod | Judgement | the writer's |

## 2. Where each piece goes on the street

Everything here is **Judgement on the scene's own numbers**: SCENE-SLOTS.md, `vignette-scene.json`, the recipe (`terrace-front.py`) and the fascia target. Where a slot in the scene file is stale, the page says so.

| Surface | What it is | Frame and paste zone | What goes there |
|---|---|---|---|
| SF1 | the quay gable: the east parade's south end wall, plane x = 3.0 m, facing -x (the big brick wall at the right of the hook frame, `morning-hook-day-2026-10-08.jpg`) | u from the front corner into the block (viewer's left), 0 to 8.0 m; z 0 to 6.3 m; paste zone u 0.15 to 6.0, z 0.45 to 2.75 | 12 bills in 3 layers, 3 stickers; the ferry case FC1 at u 6.20 and the Harbour Board case HC1 at u 6.95, both z 1.20 up |
| SF2 | the empty unit's whitened glass (bay 3, east, street x 21 to 27) | u from the glass's viewer's-left edge, 0 to 3.562 m; z 0.60 to 2.40; the glass is street x 23.088 to 26.65 (the recipe's `fx` counts from the viewer's RIGHT: u = 3.562 x (1 - fx)) | 8 items: five bills, a crown bill, the planning notice, a sticker; whitewash shows above 2.0 m |
| WEST_PIER | six brick piers of the plain west block (street x 3 to 21), each 0.95 to 0.956 m, computed from the plain row's layout (door at bay start + 1.5 or + 4.5, windows 0.85 wide at + 3.3 and + 5.1 or + 0.9 and + 2.7) | street x of the pier's centre; z from the pavement | 7 items (below) |
| SF4 | the three lamp columns, street x 8, 28, 48 (SCENE-SLOTS: every 20 m, first at 8 m, 0.6 m back from the kerb, alternate sides) | the shaft 0.114 m across; a bill wraps it: the middle 0.17 m of an A3 shows face-on | C03 and a sticker at x 8; two stickers at x 28 |
| SF5 | the empty unit's fascia (0.55 m, z 2.85 to 3.40, 0.12 proud) | centre street x 24.0 = the fascia target's board x 2705; the board z 2.90 to 3.35 | the letting board L01 (or L02) |
| SF6 | first-floor brick above bay 3's cornice (3.55) and below the upper sills (about 4.3), between the two upper windows (street x 22.93 to 25.07) | centre street x 24.0, z 3.70 to 4.10 | the flat board L03 |
| SF7 | name-plate walls | see section 8 | S01d twice, S02d once |
| SF8 | a quay-edge post, street x about -0.6 (PROPOSED: SCENE-SLOTS has no quay geometry) | z 1.20 up | H02, DANGER DEEP WATER |
| SHOP | eight shop fronts: glass 3.562 m, shop door 0.9, side door 0.838, pilasters 0.35 (C5, C8, C9), the door order following the fascia target's door ends | u from the glass's (or the shop door's) viewer's-left edge | the cards: section 5.6, 5.7 |

Piers (street x of the clear brick, from the recipe's bay layout; bay 1 agrees with the scene file's note that the poster slot at x 11.4 lies between a door at 10.5 and a window at 12.3):

| Pier | x0 to x1 | centre | between | bill |
|---|---|---|---|---|
| W0.0 | 4.919 to 5.875 | 5.397 | door and window | C01a z 1.30 |
| W0.1 | 6.725 to 7.675 | 7.200 | window and window | M01 z 0.85 |
| W1.0 | 10.919 to 11.875 | 11.397 | door and window | W01 z 1.00 |
| W1.1 | 12.725 to 13.675 | 13.200 | window and window | P02 z 0.95 |
| W2.0 | 16.325 to 17.275 | 16.800 | window and window | J01 z 1.00, L04 z 2.15 |
| W2.1 | 18.125 to 19.081 | 18.603 | window and door | D01 z 0.90 |

The scene file's two held props are stale: its poster at west x 11.4 is the pier W1.0 and stays; its glazed case at west x 26.4 would stand on the tea room's glass (the west block is shops, not plain, from x 24) so both cases move to the quay gable.

## 3. Sizes, stocks, processes and what they look like

British paper sizes of the period (Derived from the imperial names: 25.4 mm to the inch; the Double Crown 20 x 30 in is a Lead from a search summary).

| Name | mm | used for |
|---|---|---|
| crown | 381 x 508 | J01 |
| double_crown | 508 x 762 | the poll-tax, fight, market, dance, tea and programme bills |
| quad_crown | 1016 x 762 | T01, T02 (landscape, 'the quad') |
| four_sheet | 1016 x 1524 | G01 (one on the gable) |
| A3 | 297 x 420 | police and road-closure notices |
| A4 | 210 x 297 | the advice sheet, planning notice, three Harbour Board notices |
| A5 | 148 x 210 | (portrait, not used) |
| A6 | 105 x 148 | (portrait, not used) |
| A2 | 420 x 594 | F01, F02 (the ferry sheets) |
| A5L | 210 x 148 | cards K01, K05, K06 a and b, K08 |
| A6L | 148 x 105 | K06c, SA15 |

Processes, in plain words (the numbers are in `processes`):

- **screen_2col**: two-colour screen print on fluorescent stock; registration_offset_mm [0.3, 0.8]; lead: Hackney Museum holds a 1990 'Pay No Poll Tax' single sheet on yellow paper with red ink (search summary, unreached page): the colour way is the lead
- **screen_1col**: one-colour screen print on fluorescent stock
- **letterpress_2col**: two-colour letterpress from metal and wood type (a small jobbing printer); registration_offset_mm [0.3, 0.7]; impression_mm [0.1, 0.18]
- **litho_4col**: four-colour offset litho, a quad or four-sheet
- **litho_2col**: two-colour offset litho; registration_offset_mm [0.1, 0.3]
- **photocopy_a4**: photocopy on A4; toner_density 0.92
- **photocopy_a3**: photocopy on A3; toner_density 0.92
- **typed_carbon**: electric typewriter, then photocopied or used as the top copy; pitch Courier 10 characters to the inch (2.54 mm), 12 point; lead: by 1990 an office letter is a crisp daisy-wheel or golfball impression (period note PERIOD-PRINT-AND-FONTS, 1 Oct)
- **felt_pen**: felt-tip marker on card
- **ballpoint_card**: ballpoint on a record card, felt-tip heading
- **sticker_print**: printed self-adhesive label or sticker, die-cut
- **plastic_print**: screen-printed plastic card on a chain
- **enamel**: vitreous enamel on pressed steel; roughness 0.12; thickness_mm 1.6; lead: the Harbour Board's 'blue and white enamel signage on gates, cranes and the weighbridge' (content/brands/brand-bible-v1.json)
- **agent_board**: painted exterior plywood, sign-written or screen-printed vinyl; roughness 0.35
- **cast_iron_raised**: cast iron, raised lettering and border, painted white with black letters; roughness 0.55; relief_mm 4.0; lead: Hull's cast plates of the 1920s were black on white and the paint faded or flaked, needing regular repainting (search summary of a Geograph caption)
- **pressed_aluminium_enamel**: die-pressed aluminium sheet, letters and border raised 1.5 mm, stove enamelled black on white; roughness 0.3; relief_mm 1.5; thickness_mm 2.0; lead: current specs: 11 SWG aluminium, die-pressed, stove-enamelled (South Kesteven, Charnwood: search summaries)
- **vitreous_enamel_steel**: vitreous enamel on pressed steel, rolled edge; roughness 0.12

The look in one paragraph per kind (all Judgement unless a lead is named):

- **Fly-posters** are two-colour jobs from a small jobbing printer: black and one colour on cheap uncoated poster paper, white or tinted or fluorescent, set in a mixture of faces with thick rules and a printer's imprint in 7-point at the foot. Letterpress bills show a darker rim at the letter edges and a faint relief; screen-printed ones are flat and a little thick; the second colour sits 0.3 to 0.8 mm off register. The poll-tax bills use fluorescent yellow and orange stock because the one 1990 sheet found is yellow in red ink (a Lead).
- **Quads and the four-sheet** are offset litho in full colour on uncoated paper. The halftone is not resolved at 2 px to the millimetre, so they are drawn as continuous tone with grain; the image model makes the picture only (no words, no people), our text layer lays every letter, and a dark scrim guarantees the contrast of the lines on the art.
- **Photocopies** (the advice sheet, the police appeals, the planning and road notices) are hard black toner on white or tinted copier paper: a grey band 3 to 6 mm along one edge, speckle, a crooked copy, a vertical streak or two. Planning and road notices sit in a clear polythene sleeve.
- **Typed notices** (the Harbour Board's) are Courier Prime, 10 characters to the inch, an electric typewriter's even impression, pinned in a glass case with drawing pins, curling.
- **Hand-lettered cards** are felt pen (a fat even line, a darker blob where the nib rested) in Patrick Hand capitals, and ballpoint (a thin line, lighter on the joins) on white or tinted record cards; each is taped or pinned and slightly crooked.
- **Stickers** are printed paper labels, die-cut, edges lifting and scratched.
- **Enamel signs** are vitreous enamel on pressed steel: gloss, rolled edge, chips to black steel with a rust halo at the corners and the bolts.

## 4. Stocks, inks, paints and ageing

Four classes by days on the wall: **A** fresh (0 to 7 days), **B** weeks (8 to 35), **C** months (36 to 120), **D** old (over 120). A colour fades by f = 1 - exp(-t / tau) (tau in days, per ink or stock) towards the paper, the paper yellows (30 per cent of the way to (214,200,168) at class D), and a grime film (62,58,52) mixes in at 0, 5, 12 and 22 per cent (35 per cent of that over ink). The order of fastness (Judgement) is fluorescent stock, then red, blue, black, toner.

| Stock | fresh | A | B | C | D | tau |
|---|---|---|---|---|---|---|
| white poster paper | (236,235,228) | (236,235,228) | (226,224,215) | (212,209,199) | (192,187,175) | none |
| white copier paper, A4 or A3 | (240,240,234) | (240,240,234) | (229,229,221) | (215,213,203) | (195,191,178) | none |
| cream poster paper | (236,226,196) | (236,226,196) | (226,216,187) | (212,202,175) | (192,183,158) | none |
| fluorescent yellow poster paper | (250,238,52) | (249,237,57) | (235,224,80) | (215,206,117) | (192,183,131) | 60 |
| fluorescent orange poster paper | (255,120,52) | (254,123,56) | (240,135,77) | (218,152,107) | (195,155,120) | 60 |
| pale pink poster paper | (240,206,210) | (240,206,210) | (229,200,199) | (214,191,187) | (193,177,167) | 150 |
| pale green copier paper | (204,226,202) | (204,226,202) | (199,216,194) | (192,203,181) | (181,184,164) | 200 |
| pale yellow copier paper | (246,238,176) | (246,238,176) | (234,226,171) | (218,210,166) | (195,187,155) | 150 |
| pale blue poster paper | (204,220,238) | (204,220,238) | (199,212,224) | (192,200,205) | (181,183,178) | 200 |
| white card, about 250 gsm | (242,240,232) | (242,240,232) | (231,229,219) | (217,213,202) | (196,191,178) | none |
| buff card, about 250 gsm | (224,204,160) | (224,204,160) | (215,197,155) | (203,186,148) | (186,171,138) | none |
| white record card | (244,242,234) | (244,242,234) | (233,230,221) | (219,215,203) | (197,191,178) | none |
| pink record card | (240,196,204) | (240,196,204) | (229,191,195) | (214,186,183) | (193,173,165) | 150 |
| blue record card | (196,214,236) | (196,214,236) | (192,206,222) | (188,196,203) | (179,180,178) | 200 |
| yellow record card | (246,232,150) | (246,232,151) | (234,221,151) | (218,206,151) | (195,186,149) | 150 |
| green record card | (196,226,196) | (196,226,196) | (192,216,188) | (189,203,178) | (180,184,162) | 200 |
| fluorescent yellow star card | (252,240,40) | (251,239,46) | (237,225,75) | (216,205,114) | (194,183,126) | 50 |
| fluorescent pink star card | (255,92,140) | (254,97,142) | (238,122,148) | (217,151,154) | (194,155,147) | 45 |
| fluorescent orange star card | (255,130,40) | (254,133,45) | (239,144,72) | (217,159,109) | (194,157,121) | 50 |

| Ink | fresh | tau (days) |
|---|---|---|
| black ink | (24,24,27) | 1500 |
| poster red | (196,34,38) | 150 |
| poster blue | (28,58,138) | 400 |
| navy | (26,38,82) | 900 |
| photocopier toner | (30,30,33) | 4000 |
| typewriter ribbon, black | (34,34,38) | 1500 |
| felt pen, black | (30,30,36) | 900 |
| felt pen, red | (200,32,40) | 120 |
| felt pen, blue | (28,62,150) | 300 |
| felt pen, green | (24,110,60) | 300 |
| ballpoint, blue | (30,52,150) | 250 |
| ballpoint, black | (40,40,46) | 900 |

| Paint | fresh | B | D |
|---|---|---|---|
| vitreous enamel, white | (238,238,230) | (227,226,217) | (191,187,175) |
| vitreous enamel, Harbour Board blue | (24,68,140) | (36,74,136) | (70,91,124) |
| vitreous enamel, red | (176,30,34) | (172,39,42) | (156,69,64) |
| vitreous enamel, black | (20,20,22) | (32,31,30) | (67,63,57) |
| plate paint, white, oil gloss gone satin | (232,230,220) | (222,219,208) | (188,182,169) |
| plate paint, black | (22,22,26) | (34,32,34) | (68,64,60) |
| agent's board, white gloss | (236,236,230) | (225,224,217) | (189,186,175) |
| agent's navy | (28,46,94) | (38,54,95) | (71,78,97) |
| agent's red | (178,34,40) | (174,43,46) | (157,72,67) |
| OPEN face, green | (30,92,66) | (40,95,70) | (73,104,82) |
| lamplight orange, the Tivoli's title colour on dark art | (240,170,64) | (229,166,68) | (192,149,81) |
| varnished timber, dark | (74,50,34) | (80,58,42) | (98,81,64) |
| cork board | (176,138,96) | (172,136,97) | (156,131,99) |
| polythene sleeve highlight | (226,230,232) | (216,219,219) | (184,182,176) |
| printed adhesive vinyl, white | (238,238,232) | (227,226,219) | (191,187,176) |

Paper wear (numbers for the builder; Judgement): wrinkles of 0.4 to 1.5 mm, wavelength 12 to 40 mm, from wallpaper-paste cockling, strongest along the brush direction (vertical); corners lifting 0 to 3 of radius 15 to 60 mm (none at class A, three at D); tears 0 to 4 of width 20 to 140 mm from an edge; rain runs 2 to 8 a metre, 10 to 60 mm long, 0.4 to 1.5 mm wide, opacity 0.15 to 0.4, down from the top edge and from any lifted corner, the red and dye inks running first; a paste halo 2 to 10 mm at class C and D; share of the sheet lost 0 to 0.05 at B, 0.03 to 0.2 at C, 0.3 to 0.6 at D, the lower corners first; skew -1.5 to +1.5 degrees; up to three layers, each newer bill covering at most 55 per cent of an older one, overlapping edges 0 to 40 mm. A wet wall darkens paper by 12 per cent and raises saturation by 10 per cent (a runtime hint).

Wear tables by kind (`wear_tables`): bill_pasted; glass_bill; notice_sleeve; card_felt; card_ballpoint; sticker; enamel_plate; cast_iron_plate; pressed_plate; letting_board; case.

## 4b. Type

Sixteen font files from thirteen families, **all SIL OFL 1.1, every family's OFL.txt read whole on raw.githubusercontent.com today** (UnifrakturMaguntia's and Arimo's OFL texts and Liberation's LICENSE were read too and are not used; Liberation's font files were not reached). Letters are RENDERED into pictures: the OFL puts no restriction on a picture made with a font. The font files themselves are NOT copied into `production/fonts` here.

| Key | Family | Used for | In production/fonts | RFN |
|---|---|---|---|---|
| marcellus-sc | Marcellus SC | S01d, S01n, S01p, S02d, S02n, S02p, S03d, S03n ... (9 items) | yes | Marcellus |
| oswald | Oswald | B01, D01, F01, F02, G01, G02, J01, K02 ... (18 items) | yes | none |
| jost | Jost | L01, L02, L03, L04 | yes | none |
| libre-franklin | Libre Franklin | B01, D01, F01, G01, G02, J01, M01, P01 ... (12 items) | yes | none |
| alfa-slab-one | Alfa Slab One | B01, D01, F01, F02, G01, G02, K02, M01 | yes | Alfa Slab |
| fraunces | Fraunces | G02, T01, T02 | yes | none |
| old-standard-tt | Old Standard TT | D01, J01 | yes | none |
| old-standard-tt-regular | Old Standard TT | J01 | yes | none |
| old-standard-tt-italic | Old Standard TT | D01, J01, W01 | yes | none |
| abril-fatface | Abril Fatface | not used | yes | Abril, Abril Fatface |
| josefin-sans | Josefin Sans | T01, T02, T03 | yes | Josefin Sans |
| archivo | Archivo | C01a, C01b, C01c, C02, C03, H01, H02, K03a ... (13 items) | NO: add with its OFL.txt | none |
| courier-prime | Courier Prime | H03, H04, H05, P04 | NO: add with its OFL.txt | none |
| courier-prime-bold | Courier Prime | H03, H04, H05 | NO: add with its OFL.txt | none |
| libre-baskerville | Libre Baskerville | C02, C03, H03, H04, H05 | NO: add with its OFL.txt | Libre Baskerville |
| patrick-hand | Patrick Hand | K01, K05, K06a, K06c, K07a, K07b, K07c, K07d ... (29 items) | yes | none |

Four are not in `production/fonts` (Archivo, Courier Prime Regular and Bold, Libre Baskerville); `self_check.py --fetch-fonts DIR` fetches them and the OFL texts. The old bills used League Gothic (in the repository, an OFL face, but not on the asset plan's table): this target uses Oswald instead. Overpass is never used. No UnifrakturMaguntia: a masthead would name a local paper, which canon owes.

## 5. The items, word by word (unit 4.2)

Each line: the exact words, the font and weight, the cap height in millimetres, the anchor and x, the baseline y, the ink, and the contrast of ink on ground in class B. Anchors are of the INK, not the advance box. Every width is measured on the real font file; every box is in `target.json` (`ink_box_mm`).

### 5.1 The poll-tax set

An INVENTED LOCAL CAMPAIGN (ruling 3 October), `MERIDIAN AGAINST THE POLL TAX` (proposed, not minted): no party, no person, no real group, no real logo. The slogan CAN'T PAY - WON'T PAY is a common slogan (and the title of a 1974 play), not a mark: it is the one phrase a reviewer may want struck. Autumn 1990 is the summons season, so the bills are about meetings, a march and what to do with a summons; DON'T REGISTER, a 1989 slogan, is gone. The sheets carry the legal imprint of a publisher and a printer. Dates: Thursday 25 October (meeting), Tuesday 30 October (advice), Saturday 10 November (march). All weekdays are computed.

#### P01  Poll tax: public meeting bill

- 508 x 762 mm (double_crown); 2 px/mm; stock: fluorescent yellow poster paper; process: screen_2col; event: THURSDAY 25 OCTOBER
- variants: 3 (age class A, B, C; skew -1.2 to +1.2 degrees; red pass shifted 0.3 to 0.8 mm; one has a top corner torn 60 to 140 mm)
- shape rule_top (rule): box [40, 420.5, 468, 425.5], fill black
- shape rule_mid (rule): box [40, 160.0, 468, 165.0], fill black
- shape footer_bar (rect): box [18, 30, 490, 82], fill black
  - `NO` | oswald 700 | cap 190 | centre 254 | base 548 | black | B 12.52
  - `POLL TAX` | oswald 700 | cap 97.5 | centre 254 | base 438.5 | red | B 3.84
  - `PUBLIC MEETING` | oswald 600 | cap 34 | centre 254 | base 374.5 | black | B 12.52
  - `THURSDAY 25 OCTOBER` | oswald 700 | cap 32.5 | centre 254 | base 328 | red | B 3.84
  - `7.30 PM` | oswald 700 | cap 76 | centre 254 | base 238 | black | B 12.52
  - `THE CHAPEL HALL` | oswald 600 | cap 38 | centre 254 | base 184 | black | B 12.52
  - `WHAT TO DO IF YOU GET A SUMMONS` | libre-franklin 800 | cap 14.5 | centre 254 | base 135.5 | black | B 12.52
  - `EVERYONE WELCOME` | libre-franklin 700 | cap 15 | centre 254 | base 112.5 | black | B 12.52
  - `MERIDIAN AGAINST THE POLL TAX` | oswald 600 | cap 24 | centre 254 | base 44 | paper | B 12.52
  - `Published by Meridian Against the Poll Tax. Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 20 | black | B 12.52

#### P02  Poll tax: don't pay bill

- 508 x 762 mm (double_crown); 2 px/mm; stock: fluorescent orange poster paper; process: screen_1col
- variants: 3 (age class B, C, C; skew; one overposted by P03 over its lower third)
- shape rule_a (rule): box [30, 293.0, 478, 299.0], fill black
- shape footer_bar (rect): box [18, 30, 490, 82], fill black
  - `DON’T` | oswald 700 | cap 154 | centre 254 | base 584 | black | B 6.82
  - `PAY` | oswald 700 | cap 184 | centre 254 | base 390 | black | B 6.82
  - `THE POLL TAX` | oswald 700 | cap 61 | centre 254 | base 311 | black | B 6.82
  - `CAN’T PAY — WON’T PAY` | oswald 600 | cap 34.5 | centre 254 | base 242.5 | black | B 6.82
  - `JOIN US EVERY THURSDAY` | libre-franklin 800 | cap 19 | centre 254 | base 175.3 | black | B 6.82
  - `7.30 PM · THE CHAPEL HALL` | libre-franklin 800 | cap 19 | centre 254 | base 130 | black | B 6.82
  - `MERIDIAN AGAINST THE POLL TAX` | oswald 600 | cap 24 | centre 254 | base 44 | paper | B 6.82
  - `Published by Meridian Against the Poll Tax. Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 20 | black | B 6.82

#### P03  Poll tax: march bill

- 508 x 762 mm (double_crown); 2 px/mm; stock: white poster paper; process: letterpress_2col; event: SATURDAY 10 NOVEMBER
- variants: 3 (age class A, B, C; ink density; overposted by P01 at the foot in one)
- shape bar_left (rect): box [18, 100, 46, 744], fill red
- shape footer_bar (rect): box [64, 30, 490, 82], fill black
  - `MARCH` | oswald 700 | cap 117 | left 64 | base 621 | red | B 3.99
  - `AGAINST THE` | oswald 600 | cap 40 | left 64 | base 569 | black | B 13.0
  - `POLL TAX` | oswald 700 | cap 92 | left 64 | base 469 | black | B 13.0
  - `SATURDAY` | oswald 700 | cap 62 | left 64 | base 367 | black | B 13.0
  - `10 NOVEMBER` | oswald 700 | cap 58.5 | left 64 | base 298.5 | black | B 13.0
  - `ASSEMBLE 11 AM` | oswald 600 | cap 37.5 | left 64 | base 237 | black | B 13.0
  - `THE EXCHANGE` | oswald 600 | cap 42 | left 64 | base 185 | black | B 13.0
  - `BRING YOUR NEIGHBOURS` | libre-franklin 800 | cap 20 | left 64 | base 141 | red | B 3.99
  - `BRING A BANNER` | libre-franklin 800 | cap 20 | left 64 | base 113 | red | B 3.99
  - `MERIDIAN AGAINST THE POLL TAX` | oswald 600 | cap 21.5 | centre 277 | base 45.2 | paper | B 13.0
  - `Published by Meridian Against the Poll Tax. Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 277 | base 20 | black | B 13.0

#### P04  Poll tax: summons advice sheet (photocopy)

- 210 x 297 mm (A4); 2 px/mm; stock: pale green copier paper; process: photocopy_a4; event: TUESDAY 30 OCTOBER
- variants: 3 (paper: pale green, pale yellow, white; skew 0.2 to 1.5 degrees; toner speckle and a copier edge shadow)
- shape rule_a (rule): box [12, 184.0, 198, 185.6], fill toner
  - `GOT A POLL TAX` | archivo 900 | cap 14.5 | centre 105 | base 269.5 | toner | B 10.96
  - `SUMMONS?` | archivo 900 | cap 19.5 | centre 105 | base 232.8 | toner | B 10.96
  - `DON’T PANIC.` | archivo 900 | cap 14 | centre 105 | base 190 | toner | B 10.96
  - `ADVICE EVENING` | archivo 800 | cap 11 | left 16 | base 161 | toner | B 10.96
  - `TUESDAY 30 OCTOBER, 7 PM` | archivo 800 | cap 8.5 | left 16 | base 146.5 | toner | B 10.96
  - `THE CHAPEL HALL` | archivo 800 | cap 8.5 | left 16 | base 133 | toner | B 10.96
  - `Bring your summons and any letters you have had.` | courier-prime 400 | cap 2.455 | left 16 | base 115 | toner | B 10.96
  - `We will go through them with you.` | courier-prime 400 | cap 2.455 | left 16 | base 106.5 | toner | B 10.96
  - `Free and confidential. Come on your own` | courier-prime 400 | cap 2.455 | left 16 | base 98.1 | toner | B 10.96
  - `or bring a neighbour.` | courier-prime 400 | cap 2.455 | left 16 | base 89.6 | toner | B 10.96
  - `MERIDIAN AGAINST THE POLL TAX` | archivo 800 | cap 6 | centre 105 | base 22 | toner | B 10.96

#### P05  Poll tax: sticker, 95 x 60

- 95 x 60 mm (own size); 2 px/mm; stock: white poster paper; process: sticker_print
- variants: 2 (on a lamp column, pillar, kiosk or wall: corners lifting, one scratched, one half scraped)
- shape frame (frame): box [2, 2, 93, 58], fill red
  - `NO` | oswald 700 | cap 20 | centre 47.5 | base 34 | red | B 3.99
  - `POLL TAX` | oswald 700 | cap 15.5 | centre 47.5 | base 15.5 | black | B 13.0
  - `MERIDIAN AGAINST THE POLL TAX` | oswald 600 | cap 3.6 | centre 47.5 | base 7 | black | B 13.0

#### P06  Poll tax: sticker, 148 x 52

- 148 x 52 mm (own size); 2 px/mm; stock: white poster paper; process: sticker_print
- variants: 2 (as P05)
- shape bar (rect): box [2, 2, 146, 50], fill black
  - `CAN’T PAY — WON’T PAY` | oswald 700 | cap 10 | centre 74 | base 24 | paper | B 13.0
  - `MERIDIAN AGAINST THE POLL TAX` | oswald 600 | cap 4 | centre 74 | base 10 | paper | B 13.0

### 5.2 The chapel hall (the game's `chapel_hall`)

`THE CHAPEL HALL` is the game's own place (`hook-cast.json`, Father Walsh's chapel and its hall); no street is minted for it, so the bills name none. Religion appears as part of life, never mocked: the jumble sale is in aid of the chapel roof fund (the content gate's own permitted sample line speaks of the chapel roof). No raffle, no bingo, no drink (`TEA AND SANDWICHES`), no children (`ALL WELCOME`, never 'families'). The band, THE SANDERLING TRIO, is a placeholder.

#### J01  Jumble sale bill (chapel hall)

- 381 x 508 mm (crown); 2 px/mm; stock: pale pink poster paper; process: letterpress_2col; event: SATURDAY 20 OCTOBER
- variants: 3 (age class A, B, C; skew +-1.5 degrees; red pass shifted 0.3 to 0.6 mm; one half-covered by P03 or W01)
- shape frame (frame): box [12, 12, 369, 496], fill black - two brass rules, 3 pt, mitred at the corners; hairline gaps at the joints
- shape rule_a (rule): box [40, 337.0, 341, 340.2], fill black
  - `GRAND` | old-standard-tt 700 | cap 34 | centre 190.5 | base 452 | red | B 3.38
  - `JUMBLE SALE` | oswald 700 | cap 49 | centre 190.5 | base 393 | black | B 10.99
  - `THE CHAPEL HALL` | oswald 600 | cap 26 | centre 190.5 | base 355 | black | B 10.99
  - `SATURDAY 20 OCTOBER` | oswald 700 | cap 24.5 | centre 190.5 | base 300.5 | red | B 3.38
  - `DOORS OPEN 2 PM` | oswald 600 | cap 24 | centre 190.5 | base 255.6 | black | B 10.99
  - `CLOTHING · BOOKS · BRIC-A-BRAC · HOUSEHOLD` | old-standard-tt-regular 400 | cap 8 | centre 190.5 | base 210 | black | B 10.99
  - `Teas and cakes` | old-standard-tt-italic 400 | cap 15 | centre 190.5 | base 165.8 | black | B 10.99
  - `ADMISSION 20p` | libre-franklin 800 | cap 19 | centre 190.5 | base 105.1 | black | B 10.99
  - `IN AID OF THE CHAPEL ROOF FUND` | libre-franklin 700 | cap 10 | centre 190.5 | base 70 | black | B 10.99
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 190.5 | base 22 | black | B 10.99

#### D01  Old-time dance bill (chapel hall)

- 508 x 762 mm (double_crown); 2 px/mm; stock: cream poster paper; process: letterpress_2col; event: SATURDAY 17 NOVEMBER
- variants: 3 (age class A, B, C; blue pass shifted 0.3 to 0.7 mm; skew)
- shape frame (frame): box [16, 16, 492, 746], fill blue
  - `OLD TIME` | old-standard-tt 700 | cap 56 | centre 254 | base 672 | blue | B 6.71
  - `and` | old-standard-tt-italic 400 | cap 26 | centre 254 | base 638 | black | B 12.1
  - `NEW VOGUE` | old-standard-tt 700 | cap 45 | centre 254 | base 587 | blue | B 6.71
  - `DANCING` | alfa-slab-one 400 | cap 58 | centre 254 | base 519 | black | B 12.1
  - `SATURDAY 17 NOVEMBER` | oswald 700 | cap 28 | centre 254 | base 449 | black | B 12.1
  - `7.30 TO 11 PM` | oswald 600 | cap 42 | centre 254 | base 377.5 | blue | B 6.71
  - `THE CHAPEL HALL` | oswald 600 | cap 30 | centre 254 | base 313.9 | black | B 12.1
  - `Music by` | old-standard-tt-italic 400 | cap 18 | centre 254 | base 241.1 | black | B 12.1
  - `THE SANDERLING TRIO` | old-standard-tt 700 | cap 19.5 | centre 254 | base 204.8 | black | B 12.1
  - `TEA AND SANDWICHES` | libre-franklin 800 | cap 16 | centre 254 | base 134.1 | black | B 12.1
  - `ADMISSION £1.50` | libre-franklin 800 | cap 16 | centre 254 | base 97 | black | B 12.1
  - `ALL WELCOME` | libre-franklin 800 | cap 16 | centre 254 | base 60 | blue | B 6.71
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 28 | black | B 12.1

### 5.3 The fights, the market and the goods

THE DRILL HALL is a generic building (proposed). The four ring names are invented placeholders. No odds, no stakes, no prize. The market bill matches `hook-cast.json`: Tuesday, Friday, Saturday, 8 to 4. The two goods are INVENTED brands (WHITEWELL washday powder, QUAYSIDE TEA), proposed, not minted; a cigarette bill is not drawn (a minted brand and the 1990 health-warning wording are both missing).

#### W01  All-in wrestling bill

- 508 x 762 mm (double_crown); 2 px/mm; stock: pale yellow copier paper; process: letterpress_2col; event: FRIDAY 2 NOVEMBER
- variants: 3 (age class A, B, C; red pass shifted; one with the date line struck through by a hand-painted band (event over): a red felt-pen stripe, NO new words)
- shape rule_a (rule): box [40, 428.0, 468, 431.4], fill black
  - `ALL-IN` | oswald 700 | cap 60 | centre 254 | base 678 | black | B 13.04
  - `WRESTLING` | oswald 700 | cap 82.5 | centre 254 | base 587.5 | red | B 3.97
  - `THE DRILL HALL` | oswald 600 | cap 34 | centre 254 | base 539.5 | black | B 13.04
  - `FRIDAY 2 NOVEMBER` | oswald 700 | cap 39.5 | centre 254 | base 488 | black | B 13.04
  - `BELL 7.30 PM` | oswald 600 | cap 34 | centre 254 | base 446 | red | B 3.97
  - `THE SEA WOLF` | oswald 700 | cap 54.5 | centre 254 | base 361.5 | black | B 13.04
  - `v` | old-standard-tt-italic 400 | cap 14 | centre 254 | base 343.2 | red | B 3.97
  - `MAD MAURICE` | oswald 700 | cap 53.5 | centre 254 | base 285.4 | black | B 13.04
  - `TIGER JIM LARKIN` | oswald 700 | cap 42.5 | centre 254 | base 223.7 | black | B 13.04
  - `v` | old-standard-tt-italic 400 | cap 14 | centre 254 | base 205.4 | red | B 3.97
  - `THE BARON` | oswald 700 | cap 53 | centre 254 | base 148.1 | black | B 13.04
  - `AND SUPPORT BOUTS` | oswald 600 | cap 20 | centre 254 | base 113.1 | black | B 13.04
  - `RINGSIDE £4 · UNRESERVED £2.50` | libre-franklin 800 | cap 17 | centre 254 | base 72.6 | red | B 3.97
  - `TICKETS AT THE DOOR` | libre-franklin 700 | cap 14 | centre 254 | base 50 | black | B 13.04
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 24 | black | B 13.04

#### B01  Boxing night bill

- 508 x 762 mm (double_crown); 2 px/mm; stock: pale blue poster paper; process: letterpress_2col; event: FRIDAY 16 NOVEMBER
- variants: 2 (age class B, C; skew)
- shape rule_a (rule): box [40, 276.00000000000006, 468, 279.40000000000003], fill black
  - `BOXING` | alfa-slab-one 400 | cap 76.5 | centre 254 | base 661.5 | black | B 11.4
  - `TEN BOUTS` | oswald 700 | cap 66.5 | centre 254 | base 547.8 | red | B 3.58
  - `THE DRILL HALL` | oswald 600 | cap 44 | centre 254 | base 437 | black | B 11.4
  - `FRIDAY 16 NOVEMBER` | oswald 700 | cap 39.5 | centre 254 | base 366 | black | B 11.4
  - `FIRST BOUT 7.30 PM` | oswald 600 | cap 38.5 | centre 254 | base 300 | red | B 3.58
  - `RINGSIDE £3 · UNRESERVED £1.50` | libre-franklin 800 | cap 17.5 | centre 254 | base 240.5 | black | B 11.4
  - `TICKETS AT THE DOOR` | libre-franklin 700 | cap 18 | centre 254 | base 90 | black | B 11.4
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 24 | black | B 11.4

#### M01  Market day bill

- 508 x 762 mm (double_crown); 2 px/mm; stock: white poster paper; process: letterpress_2col
- variants: 2 (age class B, D (the old one is mostly paste and one torn half); skew)
- shape rule_a (rule): box [40, 312.0, 468, 315.4], fill black
  - `COPPER ROW` | alfa-slab-one 400 | cap 46 | centre 254 | base 692 | blue | B 7.19
  - `MARKET` | alfa-slab-one 400 | cap 69 | centre 254 | base 588.2 | black | B 13.0
  - `TUESDAYS · FRIDAYS · SATURDAYS` | oswald 700 | cap 25.5 | centre 254 | base 475.6 | black | B 13.0
  - `8 AM TO 4 PM` | oswald 700 | cap 58.5 | centre 254 | base 330 | blue | B 7.19
  - `FRUIT · VEG · FISH · HOUSEHOLD · CLOTHING` | oswald 600 | cap 19 | centre 254 | base 271 | black | B 13.0
  - `NEW STALLS WELCOME` | libre-franklin 800 | cap 20 | centre 254 | base 125.8 | black | B 13.0
  - `ENQUIRIES: THE MARKET OFFICE` | libre-franklin 700 | cap 14 | centre 254 | base 70 | black | B 13.0
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 24 | black | B 13.0

#### G01  Washday powder four-sheet (invented brand)

- 1016 x 1524 mm (four_sheet); 2 px/mm; stock: white poster paper; process: litho_4col
- variants: 2 (age class C, D; one with the lower half pasted over by P03 and P01)
- shape title_band (rect): box [0, 0, 1016, 420], fill blue
- ART SLOT art [0, 420, 1016, 1524]: a washing line of white sheets and towels in a bright cold wind over a terraced back-yard wall, the sky pale blue; no people, no faces, no lettering anywhere in the picture. Forbidden: people, hands, faces, children, text, numerals, logos, any real product. the sheets are the whitest area; the sky is behind the title
  - `WHITEWELL` | alfa-slab-one 400 | cap 97.5 | centre 508 | base 250 | paper | B 7.19
  - `WASHES WHITE` | oswald 700 | cap 70 | centre 508 | base 150 | paper | B 7.19
  - `FOR TWIN-TUB, AUTOMATIC AND HAND WASHING` | libre-franklin 700 | cap 24 | centre 508 | base 90 | paper | B 7.19
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 4 | centre 508 | base 40 | paper | B 7.19

#### G02  Tea bill (invented brand)

- 508 x 762 mm (double_crown); 2 px/mm; stock: cream poster paper; process: letterpress_2col
- variants: 2 (age class B, C; skew)
- shape cup (roundel): box [134, 229.5, 374, 469.5], fill red - a flat red disc standing for a cup seen from above, a white ring inside; our own drawing, no photograph
  - `QUAYSIDE` | alfa-slab-one 400 | cap 61 | centre 254 | base 677 | red | B 3.72
  - `TEA` | alfa-slab-one 400 | cap 102.5 | centre 254 | base 564.5 | black | B 12.1
  - `A good strong cup` | fraunces 700 | cap 39 | centre 254 | base 503.5 | black | B 12.1
  - `80 BAGS · £1.35` | oswald 700 | cap 52 | centre 254 | base 100 | black | B 12.1
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 30 | black | B 12.1

### 5.4 The Tivoli

The Tivoli is minted (canon). Its films are invented (THE FOURTH WITNESS, A WEEK AT GULLWING; Gullwing is a minted district); the billing block's studio and three credits are placeholders; the BBFC certificate roundels are real marks and are NOT drawn. The quads' art comes from the image model with no words and no people; our text sits on a dark scrim (T01) or on a pale panel (T02). The Tivoli's own front (plastic letters on a rail, changed on Thursdays) is not this family's.

#### T01  Tivoli quad: THE FOURTH WITNESS

- 1016 x 762 mm (quad_crown); 2 px/mm; stock: white poster paper; process: litho_4col; event: SUNDAY 21 OCTOBER
- variants: 2 (age class B, C; one cut in half by a torn edge, the title half left)
- shape scrim_bottom (scrim): box [0, 0, 1016, 300], fill black - gradient, fully dark at the foot
- shape scrim_top (scrim): box [0, 690, 1016, 762], fill black
- ART SLOT art [0, 0, 1016, 762]: a narrow wet street at night seen from a first-floor window, lamplight in orange pools on the cobbles, a telephone box lit at the far end, rain on the glass in the near corner; dark blue and black with orange; no people, no faces, no lettering. Forbidden: people, hands, faces, children, text, numerals, signs, real brands, real places, vehicles with plates. the lower third and a top strip must stay dark and low in detail: a scrim is laid there for the words
  - `THE TIVOLI` | josefin-sans 700 | cap 20 | left 70 | base 706 | agent_white | B 12.41
  - `FROM SUNDAY 21 OCTOBER` | josefin-sans 600 | cap 20 | right 990 | base 706 | agent_white | B 12.41
  - `Somebody saw. Somebody will pay.` | fraunces 600 | cap 30 | centre 508 | base 640 | agent_white | B 12.41
  - `THE FOURTH` | oswald 700 | cap 128 | left 70 | base 250 | agent_white | B 12.41
  - `WITNESS` | oswald 700 | cap 128 | left 70 | base 98 | lamp_orange | B 7.72
  - `A MARSHLAND PICTURES PRODUCTION · SCREENPLAY BY A. VENN · MUSIC BY R. CORLEY · DIRECTED BY H. MADDOX` | oswald 500 | cap 6 | left 70 | base 40 | agent_white | B 12.41

#### T02  Tivoli quad: A WEEK AT GULLWING

- 1016 x 762 mm (quad_crown); 2 px/mm; stock: white poster paper; process: litho_4col; event: THURSDAY 25 OCTOBER
- variants: 2 (age class B, C; one with the sky bleached to near white)
- shape title_panel (rect): box [110, 410, 906, 590], fill agent_white - a pale panel behind GULLWING so the red holds; the sky shows round it
- ART SLOT art [0, 0, 1016, 762]: a faded seaside pier under a high pale-blue sky with striped deckchairs lined up empty on the sand in the foreground, bright flat colours like a saucy postcard; no people, no faces, no lettering. Forbidden: people, hands, faces, children, text, numerals, signs, real brands, drink, bottles, glasses, gambling machines. the sky across the top 40 per cent stays clear and flat for the title
  - `THE TIVOLI` | josefin-sans 700 | cap 20 | left 70 | base 706 | agent_white | B 4.4
  - `FROM THURSDAY 25 OCTOBER` | josefin-sans 600 | cap 20 | right 990 | base 706 | agent_white | B 4.4
  - `A WEEK AT` | fraunces 900 | cap 90 | centre 508 | base 600 | agent_white | B 4.4
  - `GULLWING` | fraunces 900 | cap 95.5 | centre 508 | base 440 | agent_red | B 4.98
  - `The funniest week of their lives.` | fraunces 600 | cap 30 | centre 508 | base 70 | agent_navy | B 7.47
  - `A MARSHLAND PICTURES PRODUCTION · DIRECTED BY H. MADDOX` | oswald 500 | cap 6 | centre 508 | base 36 | agent_navy | B 7.47

#### T03  Tivoli programme bill

- 508 x 762 mm (double_crown); 2 px/mm; stock: white poster paper; process: letterpress_2col
- variants: 2 (age class A, B; one with the lower half torn away)
- shape rule_a (rule): box [40, 307.99999999999994, 468, 311.3999999999999], fill black
  - `THE TIVOLI` | josefin-sans 700 | cap 49 | centre 254 | base 687 | red | B 3.99
  - `FROM SUNDAY 21 OCTOBER` | oswald 600 | cap 32 | centre 254 | base 622.8 | black | B 13.0
  - `SUNDAY TO WEDNESDAY` | oswald 600 | cap 30 | centre 254 | base 532 | red | B 3.99
  - `THE FOURTH WITNESS` | oswald 700 | cap 41 | centre 254 | base 473.1 | black | B 13.0
  - `THURSDAY TO SATURDAY` | oswald 600 | cap 30 | centre 254 | base 389.4 | red | B 3.99
  - `A WEEK AT GULLWING` | oswald 700 | cap 41.5 | centre 254 | base 330 | black | B 13.0
  - `PERFORMANCES 5.15 AND 8.00` | oswald 600 | cap 26.5 | centre 254 | base 259.5 | black | B 13.0
  - `SATURDAY ALSO 2.30` | oswald 600 | cap 28.5 | centre 254 | base 200.9 | black | B 13.0
  - `ALL SEATS £2.80` | libre-franklin 800 | cap 23.5 | centre 254 | base 113 | red | B 3.99
  - `O.A.P. AND UNWAGED £1.50` | libre-franklin 800 | cap 21.5 | centre 254 | base 70 | red | B 3.99
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 24 | black | B 13.0

### 5.5 The ferry and the Harbour Board

Both are minted names (canon). The ferry sheet is the WINTER SERVICE from Monday 1 October 1990, pasted over the summer sheet, as the brand bible says; the service is one a single boat could run (15-minute crossings; the check proves it) and its last crossing, 11.00 PM, is the street's own line 'Last crossing's at eleven'. The fares are foot passengers and cycles: no one is a child. The Harbour Board's notices are typed Courier on A4 in a glass case drawing-pinned and curling (the brand bible's own words); its blue and white enamel signs are 600 x 450 on a gate, post or quay edge. Board blue is Judgement: (24,68,140).

#### F01  Meridian Ferry winter timetable (A2 sheet in the ramp case)

- 420 x 594 mm (A2); 2 px/mm; stock: white poster paper; process: litho_2col
- variants: 2 (pasted over the summer sheet F02 (offset +14 mm right, -16 mm down) in both; age class B and C; the C one has two drawing-pin holes and a rain stain from the top)
- shape head_band (rect): box [0, 490, 420, 594], fill enamel_blue
- shape col_rule (rule): box [208.5, 130, 211.5, 440], fill blue
- shape fare_rule (rule): box [12, 150, 408, 152.4], fill blue
  - `MERIDIAN FERRY` | alfa-slab-one 400 | cap 29.5 | centre 210 | base 536 | enamel_white | B 6.7
  - `WINTER SERVICE` | oswald 700 | cap 24 | centre 210 | base 504 | enamel_white | B 6.7
  - `FROM MONDAY 1 OCTOBER` | oswald 600 | cap 17 | centre 210 | base 458 | blue | B 7.19
  - `FROM THE HOOK` | oswald 700 | cap 15 | centre 110 | base 425 | black | B 13.0
  - `FROM THE FAR SIDE` | oswald 700 | cap 15 | centre 310 | base 425 | black | B 13.0
  - `MONDAY TO SATURDAY` | oswald 700 | cap 13 | centre 210 | base 398 | blue | B 7.19
  - `6.30  7.00  7.30` | libre-franklin 700 | cap 10.5 | centre 110 | base 372 | black | B 13.0
  - `and every half hour` | libre-franklin 500 | cap 10.5 | centre 110 | base 351 | black | B 13.0
  - `until 5.30 PM` | libre-franklin 500 | cap 10.5 | centre 110 | base 330 | black | B 13.0
  - `then 6.30  7.30  8.30` | libre-franklin 700 | cap 10.5 | centre 110 | base 309 | black | B 13.0
  - `9.30  10.30` | libre-franklin 700 | cap 10.5 | centre 110 | base 288 | black | B 13.0
  - `LAST CROSSING 11.00` | libre-franklin 700 | cap 10.5 | centre 110 | base 267 | black | B 13.0
  - `6.45  7.15  7.45` | libre-franklin 700 | cap 10.5 | centre 310 | base 372 | black | B 13.0
  - `and every half hour` | libre-franklin 500 | cap 10.5 | centre 310 | base 351 | black | B 13.0
  - `until 5.45 PM` | libre-franklin 500 | cap 10.5 | centre 310 | base 330 | black | B 13.0
  - `then 6.45  7.45  8.45` | libre-franklin 700 | cap 10.5 | centre 310 | base 309 | black | B 13.0
  - `9.45` | libre-franklin 700 | cap 10.5 | centre 310 | base 288 | black | B 13.0
  - `LAST CROSSING 10.45` | libre-franklin 700 | cap 10.5 | centre 310 | base 267 | black | B 13.0
  - `SUNDAYS` | oswald 700 | cap 13 | centre 210 | base 236 | blue | B 7.19
  - `9.00 AM and hourly` | libre-franklin 700 | cap 10.5 | centre 110 | base 210 | black | B 13.0
  - `until 6.00 PM` | libre-franklin 500 | cap 10.5 | centre 110 | base 189 | black | B 13.0
  - `9.15 AM and hourly` | libre-franklin 700 | cap 10.5 | centre 310 | base 210 | black | B 13.0
  - `until 6.15 PM` | libre-franklin 500 | cap 10.5 | centre 310 | base 189 | black | B 13.0
  - `FARES · FOOT PASSENGERS` | oswald 700 | cap 13 | centre 210 | base 124 | blue | B 7.19
  - `SINGLE 60p · RETURN £1.00 · CYCLES 30p` | libre-franklin 700 | cap 11 | centre 210 | base 98 | black | B 13.0
  - `O.A.P. HALF FARE` | libre-franklin 700 | cap 11 | centre 210 | base 76 | black | B 13.0
  - `CROSSINGS MAY BE CANCELLED IN FOG OR HIGH WIND` | oswald 600 | cap 11 | centre 210 | base 40 | red | B 3.99
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 210 | base 20 | black | B 13.0

#### F02  Meridian Ferry summer timetable (older sheet under F01)

- 420 x 594 mm (A2); 2 px/mm; stock: white poster paper; process: litho_2col
- variants: 1 (age class D: brown paste halo, loose at the left edge)
- shape head_band (rect): box [0, 490, 420, 594], fill enamel_blue
- shape col_rule (rule): box [208.5, 130, 211.5, 440], fill blue
  - `MERIDIAN FERRY` | alfa-slab-one 400 | cap 29.5 | centre 210 | base 536 | enamel_white | B 6.7
  - `SUMMER SERVICE` | oswald 700 | cap 24 | centre 210 | base 504 | enamel_white | B 6.7
  - `14 MAY TO 30 SEPTEMBER` | oswald 600 | cap 17 | centre 210 | base 458 | blue | B 7.19

#### H01  Harbour Board enamel sign: NO ADMITTANCE

- 600 x 450 mm (own size); 1 px/mm; process: enamel
- variants: 2 (clean to grimy (age classes B and D); one shot-peppered by the old catapult: six small chips in a loose group (a chip is not a bullet hole))
- shape face (rect): box [0, 0, 600, 450], fill enamel_blue - vitreous enamel on 1.6 mm pressed steel; corners rounded 25 mm; rolled edge 12 mm
- shape border (frame): box [18, 18, 582, 432], fill enamel_white - white band 10 mm, 18 mm in from the edge
- shape rule (rule): box [70, 190, 530, 194], fill enamel_white
  - `NO ADMITTANCE` | archivo 900 | cap 33.5 | centre 300 | base 361.5 | enamel_white | B 6.7
  - `EXCEPT ON BUSINESS` | archivo 700 | cap 27 | centre 300 | base 312.5 | enamel_white | B 6.7
  - `MERIDIAN HARBOUR BOARD` | archivo 800 | cap 20.5 | centre 300 | base 140 | enamel_white | B 6.7

#### H02  Harbour Board enamel sign: DANGER DEEP WATER

- 600 x 450 mm (own size); 1 px/mm; process: enamel
- variants: 2 (age class B, D)
- shape face (rect): box [0, 0, 600, 450], fill enamel_white - vitreous enamel on 1.6 mm pressed steel; corners rounded 25 mm; rolled edge 12 mm
- shape danger_band (rect): box [0, 300, 600, 450], fill enamel_red
- shape border (frame): box [14, 14, 586, 436], fill enamel_blue
  - `DANGER` | archivo 900 | cap 60.5 | centre 300 | base 332 | enamel_white | B 5.25
  - `DEEP WATER` | archivo 900 | cap 44.5 | centre 300 | base 220 | enamel_blue | B 6.7
  - `NO SWIMMING` | archivo 800 | cap 37 | centre 300 | base 130 | enamel_blue | B 6.7
  - `MERIDIAN HARBOUR BOARD` | archivo 800 | cap 17 | centre 300 | base 56 | enamel_blue | B 6.7

#### H03  Harbour Board notice: berths closed (typed A4)

- 210 x 297 mm (A4); 2 px/mm; stock: white copier paper, A4 or A3; process: typed_carbon; event: 26 OCTOBER 1990
- variants: 2 (pinned in the case: four drawing pins; a tan tape tab; one curling top corner)
- shape rule_a (rule): box [20, 268, 190, 269.2], fill typed
  - `MERIDIAN HARBOUR BOARD` | libre-baskerville 700 | cap 7 | centre 105 | base 274 | typed | B 12.21
  - `NOTICE TO SHIPMASTERS` | courier-prime-bold 700 | cap 3.6 | centre 105 | base 255 | typed | B 12.21
  - `Berths 3 and 4 on the Hook quay will be closed to all` | courier-prime 400 | cap 2.455 | left 24 | base 238 | typed | B 12.21
  - `shipping from Monday 5 November until further notice,` | courier-prime 400 | cap 2.455 | left 24 | base 229.5 | typed | B 12.21
  - `for repairs to the quay wall.` | courier-prime 400 | cap 2.455 | left 24 | base 221.1 | typed | B 12.21
  - `Masters should apply to the Harbour Master's office` | courier-prime 400 | cap 2.455 | left 24 | base 204.1 | typed | B 12.21
  - `for other berths.` | courier-prime 400 | cap 2.455 | left 24 | base 195.7 | typed | B 12.21
  - `By order of the Board.` | courier-prime 400 | cap 2.455 | left 24 | base 178.7 | typed | B 12.21
  - `26 October 1990` | courier-prime 400 | cap 2.455 | left 24 | base 161.8 | typed | B 12.21

#### H04  Harbour Board notice: tide table (typed A4)

- 210 x 297 mm (A4); 2 px/mm; stock: white copier paper, A4 or A3; process: typed_carbon
- variants: 1 (pinned in the case, a corner curling)
- shape rule_a (rule): box [20, 268, 190, 269.2], fill typed
  - `MERIDIAN HARBOUR BOARD` | libre-baskerville 700 | cap 7 | centre 105 | base 274 | typed | B 12.21
  - `HIGH WATER, THE HOOK` | courier-prime-bold 700 | cap 3.6 | centre 105 | base 255 | typed | B 12.21
  - `NOVEMBER 1990` | courier-prime-bold 700 | cap 3.6 | centre 105 | base 247 | typed | B 12.21
  - `DAY       HW     m     HW     m` | courier-prime 400 | cap 2.455 | left 30 | base 232 | typed | B 12.21
  - `THU 1    0542 4.7   1807 4.7` | courier-prime 400 | cap 2.455 | left 30 | base 223.5 | typed | B 12.21
  - `FRI 2    0632 4.6   1857 4.6` | courier-prime 400 | cap 2.455 | left 30 | base 215.1 | typed | B 12.21
  - `SAT 3    0722 4.5   1947 4.4` | courier-prime 400 | cap 2.455 | left 30 | base 206.6 | typed | B 12.21
  - `SUN 4    0812 4.2   2037 4.1` | courier-prime 400 | cap 2.455 | left 30 | base 198.1 | typed | B 12.21
  - `MON 5    0902 4.0   2127 3.8` | courier-prime 400 | cap 2.455 | left 30 | base 189.7 | typed | B 12.21
  - `TUE 6    0952 3.7   2217 3.6` | courier-prime 400 | cap 2.455 | left 30 | base 181.2 | typed | B 12.21
  - `WED 7    1042 3.5   2307 3.4` | courier-prime 400 | cap 2.455 | left 30 | base 172.7 | typed | B 12.21
  - `Heights in metres above chart datum.` | courier-prime 400 | cap 2.455 | left 30 | base 155.8 | typed | B 12.21
  - `Times are Greenwich Mean Time.` | courier-prime 400 | cap 2.455 | left 30 | base 147.3 | typed | B 12.21

#### H05  Harbour Board notice: vacancy (typed A4)

- 210 x 297 mm (A4); 2 px/mm; stock: pale yellow copier paper; process: typed_carbon
- variants: 1 (pinned in the case)
- shape rule_a (rule): box [20, 268, 190, 269.2], fill typed
  - `MERIDIAN HARBOUR BOARD` | libre-baskerville 700 | cap 7 | centre 105 | base 274 | typed | B 11.76
  - `VACANCY` | courier-prime-bold 700 | cap 9 | centre 105 | base 244 | typed | B 11.76
  - `QUAY LABOURER` | courier-prime-bold 700 | cap 5.4 | centre 105 | base 224 | typed | B 11.76
  - `Applications in writing, giving age and experience,` | courier-prime 400 | cap 2.455 | left 24 | base 202 | typed | B 11.76
  - `to the Secretary, Meridian Harbour Board,` | courier-prime 400 | cap 2.455 | left 24 | base 193.5 | typed | B 11.76
  - `to arrive by Friday 16 November.` | courier-prime 400 | cap 2.455 | left 24 | base 185.1 | typed | B 11.76
  - `Wages by agreement.` | courier-prime 400 | cap 2.455 | left 24 | base 168.1 | typed | B 11.76

#### HC1  Harbour Board notice case

- outer 640 x 880 x 60 mm, frame left 46, right 46, top 52, bottom 52, window corner radius 6 mm; inside [548, 776] mm
- construction: varnished timber frame (dark, grain showing, varnish crazed and lifting at the lower rails), mitred corners, one glazed door hinged on the left with two brass butt hinges, a brass lock and escutcheon 20 mm across on the right stile at 0.5 of the height, a cork lining 8 mm thick, a drip rail on top 14 mm proud
- fixing: four 8 mm coach screws through the back rails at 40 mm in from the corners, on 20 mm timber battens; rust runs 40 to 180 mm below each screw
- wear: a crack across one lower corner of the glass (30 per cent of the cases), a brown water line inside the lower glass, flies and dead leaves on the cork foot, varnish lifted at the bottom rail, one hinge screw missing
- pinned inside: H03 at (24, 470) mm, 0.8 degrees; H04 at (300, 455) mm, -1.2 degrees; H05 at (160, 100) mm, 0.5 degrees
- placed on SF1 at u 6.95 m, z 1.20 m
- photograph: the photographed case is blue steel with a 0.152 header and a 0.085 foot; the target is a 1990 timber case with 52 mm top and bottom rails (0.059 each of the height), 46 mm stiles (0.072 of the width each): the photograph's wide crest header and thick steel frame are replacement-stock features and are NOT taken (Judgement: photograph of a later object)

#### FC1  Ferry timetable case at the ramp

- outer 530 x 710 x 45 mm, frame left 34, right 34, top 36, bottom 36, window corner radius 4 mm; inside [462, 638] mm
- construction: a painted steel frame in Board blue, a hinged perspex door on the left, a cylinder lock on the right at mid height, the timetable sheet F01 held behind the perspex by the frame lip; F02 underneath
- fixing: four 8 mm screws at the corners into plugs
- wear: perspex yellowed and scratched, a hairline crack from one corner, white salt bloom along the foot, paint chipped at the lock, rust at the lower screws
- pinned inside: F02 at (7, 38) mm, 0.0 degrees; F01 at (21, 22) mm, 0.0 degrees
- placed on SF1 at u 6.20 m, z 1.20 m
- photograph: as HC1: only vertical fractions of the photograph are exact; this frame is a thin painted steel one

### 5.6 Police and council notices

The police force's name and the council's name are OWED by canon, so neither appears: POLICE, HIGHWAYS DEPARTMENT and the Planning Department are the generic words. A police appeal is an A3 photocopy taped inside a window or sleeved on a column (the one dated yellow appeal board found is from 2007; a 1990 board is a hole). The three samples are slots the simulation can fill (offence line, night, hours): a smashed shop window on Quay Street (matching the 29 September deed), a van stolen from the quay, a man assaulted near the quay. The planning notice is for the empty unit itself (shop to estate agent's office): a mundane hook, struck if the town prefers. The road closure sends traffic via WEIGHHOUSE LANE (minted; the opening at x 21 to 24 is proposed to be it).

#### C01a  Police appeal for witnesses (a)

- 297 x 420 mm (A3); 2 px/mm; stock: white copier paper, A4 or A3; process: photocopy_a3; event: FRIDAY 12 OCTOBER
- variants: 2 (photocopy: a grey edge band 3 to 6 mm at the left, toner speckle; taped inside a window with four tabs of yellowed tape, or in a polythene sleeve cable-tied to a lamp column)
- shape head_band (rect): box [12, 340, 285, 408], fill toner
  - `POLICE` | archivo 900 | cap 36 | centre 148.5 | base 358 | paper | B 12.95
  - `APPEAL FOR WITNESSES` | archivo 900 | cap 13.5 | centre 148.5 | base 300 | toner | B 12.95
  - `DID YOU SEE ANYTHING?` | archivo 800 | cap 14 | centre 148.5 | base 262 | toner | B 12.95
  - `ON THE NIGHT OF FRIDAY 12 OCTOBER,` | archivo 700 | cap 8 | left 24 | base 230 | toner | B 12.95
  - `BETWEEN 11 PM AND 1 AM,` | archivo 700 | cap 8 | left 24 | base 214.8 | toner | B 12.95
  - `A SHOP WINDOW ON QUAY STREET` | archivo 700 | cap 8 | left 24 | base 199.6 | toner | B 12.95
  - `WAS SMASHED.` | archivo 700 | cap 8 | left 24 | base 184.4 | toner | B 12.95
  - `IF YOU SAW OR HEARD ANYTHING,` | archivo 700 | cap 8 | left 24 | base 158.6 | toner | B 12.95
  - `HOWEVER SMALL, PLEASE TELEPHONE` | archivo 700 | cap 8 | left 24 | base 143.4 | toner | B 12.95
  - `THE INCIDENT ROOM ON 960 640,` | archivo 700 | cap 8 | left 24 | base 128.2 | toner | B 12.95
  - `OR CALL AT ANY POLICE STATION.` | archivo 700 | cap 8 | left 24 | base 113 | toner | B 12.95
  - `YOUR INFORMATION WILL BE TREATED IN CONFIDENCE.` | archivo 600 | cap 6.5 | centre 148.5 | base 30 | toner | B 12.95

#### C01b  Police appeal for witnesses (b)

- 297 x 420 mm (A3); 2 px/mm; stock: white copier paper, A4 or A3; process: photocopy_a3; event: SATURDAY 20 OCTOBER
- variants: 2 (photocopy: a grey edge band 3 to 6 mm at the left, toner speckle; taped inside a window with four tabs of yellowed tape, or in a polythene sleeve cable-tied to a lamp column)
- shape head_band (rect): box [12, 340, 285, 408], fill toner
  - `POLICE` | archivo 900 | cap 36 | centre 148.5 | base 358 | paper | B 12.95
  - `APPEAL FOR WITNESSES` | archivo 900 | cap 13.5 | centre 148.5 | base 300 | toner | B 12.95
  - `DID YOU SEE ANYTHING?` | archivo 800 | cap 14 | centre 148.5 | base 262 | toner | B 12.95
  - `ON THE NIGHT OF SATURDAY 20 OCTOBER,` | archivo 700 | cap 8 | left 24 | base 230 | toner | B 12.95
  - `BETWEEN MIDNIGHT AND 6 AM,` | archivo 700 | cap 8 | left 24 | base 214.8 | toner | B 12.95
  - `A VAN WAS STOLEN FROM THE QUAY.` | archivo 700 | cap 8 | left 24 | base 199.6 | toner | B 12.95
  - `IF YOU SAW OR HEARD ANYTHING,` | archivo 700 | cap 8 | left 24 | base 173.8 | toner | B 12.95
  - `HOWEVER SMALL, PLEASE TELEPHONE` | archivo 700 | cap 8 | left 24 | base 158.6 | toner | B 12.95
  - `THE INCIDENT ROOM ON 960 640,` | archivo 700 | cap 8 | left 24 | base 143.4 | toner | B 12.95
  - `OR CALL AT ANY POLICE STATION.` | archivo 700 | cap 8 | left 24 | base 128.2 | toner | B 12.95
  - `YOUR INFORMATION WILL BE TREATED IN CONFIDENCE.` | archivo 600 | cap 6.5 | centre 148.5 | base 30 | toner | B 12.95

#### C01c  Police appeal for witnesses (c)

- 297 x 420 mm (A3); 2 px/mm; stock: white copier paper, A4 or A3; process: photocopy_a3; event: SUNDAY 28 OCTOBER
- variants: 2 (photocopy: a grey edge band 3 to 6 mm at the left, toner speckle; taped inside a window with four tabs of yellowed tape, or in a polythene sleeve cable-tied to a lamp column)
- shape head_band (rect): box [12, 340, 285, 408], fill toner
  - `POLICE` | archivo 900 | cap 36 | centre 148.5 | base 358 | paper | B 12.95
  - `APPEAL FOR WITNESSES` | archivo 900 | cap 13.5 | centre 148.5 | base 300 | toner | B 12.95
  - `DID YOU SEE ANYTHING?` | archivo 800 | cap 14 | centre 148.5 | base 262 | toner | B 12.95
  - `ON THE NIGHT OF SUNDAY 28 OCTOBER,` | archivo 700 | cap 8 | left 24 | base 230 | toner | B 12.95
  - `BETWEEN 10 PM AND 11 PM,` | archivo 700 | cap 8 | left 24 | base 214.8 | toner | B 12.95
  - `A MAN WAS ASSAULTED NEAR THE QUAY.` | archivo 700 | cap 8 | left 24 | base 199.6 | toner | B 12.95
  - `IF YOU SAW OR HEARD ANYTHING,` | archivo 700 | cap 8 | left 24 | base 173.8 | toner | B 12.95
  - `HOWEVER SMALL, PLEASE TELEPHONE` | archivo 700 | cap 8 | left 24 | base 158.6 | toner | B 12.95
  - `THE INCIDENT ROOM ON 960 640,` | archivo 700 | cap 8 | left 24 | base 143.4 | toner | B 12.95
  - `OR CALL AT ANY POLICE STATION.` | archivo 700 | cap 8 | left 24 | base 128.2 | toner | B 12.95
  - `YOUR INFORMATION WILL BE TREATED IN CONFIDENCE.` | archivo 600 | cap 6.5 | centre 148.5 | base 30 | toner | B 12.95

#### C02  Planning application notice (A4 in a sleeve)

- 210 x 297 mm (A4); 2 px/mm; stock: white copier paper, A4 or A3; process: photocopy_a4; event: FRIDAY 9 NOVEMBER
- variants: 2 (in a clear polythene sleeve, cable-tied to a lamp column or taped inside the empty unit's glass; water beads in the lower sleeve; a yellowing)
- shape rule_a (rule): box [16, 262, 194, 264], fill toner
  - `PLANNING APPLICATION` | archivo 900 | cap 9 | centre 105 | base 270 | toner | B 12.95
  - `NOTICE` | archivo 700 | cap 6.5 | centre 105 | base 250 | toner | B 12.95
  - `PROPOSAL` | archivo 800 | cap 3.4 | left 22 | base 232 | toner | B 12.95
  - `Change of use of the ground floor, 21 to 27 Quay Street,` | libre-baskerville 400 | cap 3.6 | left 22 | base 223.8 | toner | B 12.95
  - `from shop to estate agent's office.` | libre-baskerville 400 | cap 3.6 | left 22 | base 215.6 | toner | B 12.95
  - `COMMENTS` | archivo 800 | cap 3.4 | left 22 | base 199.2 | toner | B 12.95
  - `Anyone wishing to comment may write to the Planning` | libre-baskerville 400 | cap 3.6 | left 22 | base 191 | toner | B 12.95
  - `Officer by Friday 9 November.` | libre-baskerville 400 | cap 3.6 | left 22 | base 182.8 | toner | B 12.95
  - `THE PLANS` | archivo 800 | cap 3.4 | left 22 | base 166.4 | toner | B 12.95
  - `may be seen at the Planning Department, Monday to` | libre-baskerville 400 | cap 3.6 | left 22 | base 158.2 | toner | B 12.95
  - `Friday, 9 a.m. to 4.30 p.m.` | libre-baskerville 400 | cap 3.6 | left 22 | base 150 | toner | B 12.95

#### C03  Temporary road closure notice (A3 in a sleeve)

- 297 x 420 mm (A3); 2 px/mm; stock: pale yellow copier paper; process: photocopy_a3; event: SUNDAY 4 NOVEMBER
- variants: 2 (cable-tied in a sleeve to a lamp column at 1.6 to 2.0 m, facing the street; the sleeve fogged inside, the notice yellowed, a cable tie tail left long)
- shape rule_a (rule): box [12, 352, 285, 355], fill toner
  - `HIGHWAYS DEPARTMENT` | archivo 800 | cap 9 | centre 148.5 | base 396 | toner | B 12.47
  - `NOTICE OF TEMPORARY ROAD CLOSURE` | archivo 900 | cap 8.5 | centre 148.5 | base 364 | toner | B 12.47
  - `QUAY STREET` | archivo 900 | cap 24.5 | centre 148.5 | base 300 | toner | B 12.47
  - `WILL BE CLOSED TO VEHICLES ON` | archivo 700 | cap 8.5 | centre 148.5 | base 262 | toner | B 12.47
  - `SUNDAY 4 NOVEMBER` | archivo 800 | cap 16 | centre 148.5 | base 235.5 | toner | B 12.47
  - `FROM 8 AM TO 6 PM` | archivo 800 | cap 14 | centre 148.5 | base 201.5 | toner | B 12.47
  - `FOR GAS MAIN RENEWAL.` | archivo 700 | cap 8.5 | centre 148.5 | base 169.5 | toner | B 12.47
  - `PEDESTRIAN ACCESS WILL BE MAINTAINED.` | archivo 700 | cap 8 | centre 148.5 | base 139 | toner | B 12.47
  - `DIVERSION VIA WEIGHHOUSE LANE.` | archivo 700 | cap 8 | centre 148.5 | base 117 | toner | B 12.47
  - `We apologise for any inconvenience.` | libre-baskerville 400 | cap 6 | centre 148.5 | base 40 | toner | B 12.47

### 5.7 Shop-window cards and the newsagent's board

Cards are hand-lettered in Patrick Hand (felt pen and ballpoint) or printed. Times and prices come from the world: LAST WASH 4.30 PM is an hour before the laundry's closing (8 to 5.30, `hook-cast.json`); BACK AT with hands at 12 is the end of Hal's Monday break (11 to 12); cod 2.70 a lb is the ONS 1990 range (2.42 in January, 2.85 in December); the fish market's other prices and the 20p-a-week advertising rate are Judgement. No card names a child, a pet shop, a drink, a pool or a lottery; no 'model' or 'companion' cards (tart cards are a content-rule line). Telephone numbers are the local six-figure form 960 xxx (the fictional range the cast's own 0632 960418 uses); none is Mickey's.

#### K01  Closed for lunch card (felt pen)

- 210 x 148 mm (A5L); 2 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 3 (BACK AT 1.30 / 2 / 2.30 are not separate cards: the hour line is one of the approved strings 'BACK AT 2 O’CLOCK'; hung on a string with a rubber sucker or taped; slightly tilted; age class A to C)
- mirror cue: a tab of yellowed tape across the top-LEFT corner only
  - `CLOSED FOR LUNCH` | patrick-hand 400 | cap 17 | centre 105 | base 92 | felt_red hand=felt | B 3.95
  - `BACK AT 2 O’CLOCK` | patrick-hand 400 | cap 14 | centre 105 | base 52 | felt_black hand=felt | B 12.53

#### K02  BACK AT clock card (printed)

- 130 x 170 mm (own size); 2 px/mm; stock: buff card, about 250 gsm; process: litho_2col
- variants: 2 (hands at 12 (Hal's Monday break ends at 12 in hook-cast.json) and at 2; hung on a string)
- shape clock (roundel): box [20, 12, 110, 102], fill white - a printed clock face: white disc, black rim 2 mm, 12 tick marks, two cardboard hands on a brass paper-fastener, set to 12 o'clock
  - `BACK AT` | alfa-slab-one 400 | cap 17 | centre 65 | base 140 | red | B 3.18
  - `12` | oswald 700 | cap 8 | centre 65 | base 90 | black | B 10.11
  - `3` | oswald 700 | cap 8 | centre 100 | base 52 | black | B 10.11
  - `6` | oswald 700 | cap 8 | centre 65 | base 20 | black | B 10.11
  - `9` | oswald 700 | cap 8 | centre 30 | base 52 | black | B 10.11

#### K03a  OPEN / CLOSED hanging sign, face OPEN

- 200 x 110 mm (own size); 2 px/mm; stock: white card, about 250 gsm; process: plastic_print
- variants: 1 (one face outward at a time, from the shop's hours (hook-cast.json); the chain shows)
- shape face (rect): box [0, 0, 200, 110], fill agent_green - rounded corners 8 mm; a hole at the top centre; a bead chain
  - `OPEN` | archivo 800 | cap 40 | centre 100 | base 40 | agent_white | B 5.64

#### K03b  OPEN / CLOSED hanging sign, face CLOSED

- 200 x 110 mm (own size); 2 px/mm; stock: white card, about 250 gsm; process: plastic_print
- variants: 1 (one face outward at a time, from the shop's hours (hook-cast.json); the chain shows)
- shape face (rect): box [0, 0, 200, 110], fill agent_red - rounded corners 8 mm; a hole at the top centre; a bead chain
  - `CLOSED` | archivo 800 | cap 27 | centre 100 | base 40 | agent_white | B 4.98

#### K04  NO DOGS sticker, 150 x 105

- 150 x 105 mm (own size); 2 px/mm; stock: white poster paper; process: sticker_print
- variants: 2 (inside the glass of a shop door at 1.1 to 1.4 m, or outside on the door; one half peeled at a corner)
- shape roundel (roundel): box [8, 17, 78, 87], fill red - a red ring 7 mm wide with a diagonal bar; inside it a black dog silhouette seen from the side, our own drawing
  - `NO` | archivo 900 | cap 12 | centre 112 | base 58 | black | B 13.0
  - `DOGS` | archivo 900 | cap 12 | centre 112 | base 36 | black | B 13.0

#### K05  PLEASE SHUT THE DOOR (felt pen)

- 210 x 148 mm (A5L); 2 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 2 (taped to a door's glass at 1.45 m; one with a second line underlined in red felt)
- mirror cue: a drawing-pin hole at the top-RIGHT only and a torn lower-LEFT corner
  - `PLEASE SHUT` | patrick-hand 400 | cap 22 | centre 105 | base 96 | felt_black hand=felt | B 12.53
  - `THE DOOR` | patrick-hand 400 | cap 22 | centre 105 | base 56 | felt_black hand=felt | B 12.53

#### K06a  Launderette: LAST WASH (felt pen)

- 210 x 148 mm (A5L); 2 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 2 (the hour comes from the shop's closing time in hook-cast.json (laundry 8 to 5.30): LAST WASH is an hour before)
- mirror cue: a string loop and rubber sucker at the top-LEFT, a crease running from the top-right corner
  - `LAST WASH` | patrick-hand 400 | cap 22 | centre 105 | base 92 | felt_red hand=felt | B 3.95
  - `4.30 PM` | patrick-hand 400 | cap 26 | centre 105 | base 50 | felt_black hand=felt | B 12.53

#### K06b  Launderette: PLEASE DO NOT OVERLOAD (printed sticker)

- 210 x 148 mm (A5L); 2 px/mm; stock: white poster paper; process: sticker_print
- variants: 2 (stuck on the glass above a machine door)
  - `PLEASE DO NOT` | archivo 800 | cap 15 | centre 105 | base 119 | black | B 13.0
  - `OVERLOAD` | archivo 900 | cap 21 | centre 105 | base 90 | red | B 3.99
  - `THE MACHINES` | archivo 800 | cap 15 | centre 105 | base 67 | black | B 13.0

#### K06c  OUT OF ORDER (felt pen)

- 148 x 105 mm (A6L); 2 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 3 (taped on a machine door or the glass, a corner of tape lifting)
- mirror cue: two tape tabs, a long one at the top-LEFT and a short one at the top-RIGHT, the left one lifting
  - `OUT OF` | patrick-hand 400 | cap 14 | centre 74 | base 66 | felt_red hand=felt | B 3.95
  - `ORDER` | patrick-hand 400 | cap 14 | centre 74 | base 38 | felt_red hand=felt | B 3.95

#### K07a  Grocer's star card

- 170 x 170 mm (own size); 2 px/mm; stock: fluorescent yellow star card; process: felt_pen
- variants: 2 (taped inside the grocer's glass at 1.2 to 1.9 m; the fluorescent stock fades within weeks)
- mirror cue: a tab of yellowed tape across the top-LEFT corner only
- shape star (star): 28 points, the card is cut to a 14-point burst; the stock colour is the star
  - `SPECIAL OFFER` | patrick-hand 400 | cap 9 | centre 85 | base 100 | felt_black hand=felt | B 11.69
  - `TEA BAGS` | patrick-hand 400 | cap 13 | centre 85 | base 77 | felt_black hand=felt | B 11.69
  - `80 FOR 99p` | patrick-hand 400 | cap 15 | centre 85 | base 55 | felt_red hand=felt | B 3.71

#### K07b  Grocer's star card

- 170 x 170 mm (own size); 2 px/mm; stock: fluorescent pink star card; process: felt_pen
- variants: 2 (taped inside the grocer's glass at 1.2 to 1.9 m; the fluorescent stock fades within weeks)
- mirror cue: a drawing-pin hole at the top-RIGHT only and a torn lower-LEFT corner
- shape star (star): 28 points, the card is cut to a 14-point burst; the stock colour is the star
  - `NEW SEASON` | patrick-hand 400 | cap 9 | centre 85 | base 100 | felt_black hand=felt | B 6.02
  - `CABBAGE` | patrick-hand 400 | cap 14 | centre 85 | base 76.5 | felt_black hand=felt | B 6.02
  - `20p lb` | patrick-hand 400 | cap 15 | centre 85 | base 55 | felt_black hand=felt | B 6.02

#### K07c  Grocer's star card

- 170 x 170 mm (own size); 2 px/mm; stock: fluorescent orange star card; process: felt_pen
- variants: 2 (taped inside the grocer's glass at 1.2 to 1.9 m; the fluorescent stock fades within weeks)
- mirror cue: a string loop and rubber sucker at the top-LEFT, a crease running from the top-right corner
- shape star (star): 28 points, the card is cut to a 14-point burst; the stock colour is the star
  - `BIG SAVER` | patrick-hand 400 | cap 10 | centre 85 | base 99.5 | felt_black hand=felt | B 6.73
  - `TINNED PEARS` | patrick-hand 400 | cap 11 | centre 85 | base 78 | felt_black hand=felt | B 6.73
  - `2 FOR 69p` | patrick-hand 400 | cap 15 | centre 85 | base 55 | felt_black hand=felt | B 6.73

#### K07d  Grocer's star card

- 170 x 170 mm (own size); 2 px/mm; stock: fluorescent yellow star card; process: felt_pen
- variants: 2 (taped inside the grocer's glass at 1.2 to 1.9 m; the fluorescent stock fades within weeks)
- mirror cue: two tape tabs, a long one at the top-LEFT and a short one at the top-RIGHT, the left one lifting
- shape star (star): 28 points, the card is cut to a 14-point burst; the stock colour is the star
  - `FRESH EGGS` | patrick-hand 400 | cap 13 | centre 85 | base 87.5 | felt_black hand=felt | B 11.69
  - `85p DOZEN` | patrick-hand 400 | cap 15 | centre 85 | base 65.5 | felt_red hand=felt | B 3.71

#### K08  SORRY NO CREDIT GIVEN (printed card)

- 210 x 148 mm (A5L); 2 px/mm; stock: white card, about 250 gsm; process: letterpress_2col
- variants: 2 (on a shop counter's glass screen or the door)
  - `SORRY` | archivo 900 | cap 20 | centre 105 | base 108 | red | B 4.13
  - `NO CREDIT GIVEN` | archivo 900 | cap 12.5 | centre 105 | base 85.5 | black | B 13.62

#### K09a  Fish price ticket: COD FILLET

- 105 x 74 mm (own size); 2 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 2 (stuck in the fish on the slab, or taped to the glass; a wet corner)
- mirror cue: a tab of yellowed tape across the top-LEFT corner only
  - `COD FILLET` | patrick-hand 400 | cap 13 | centre 52.5 | base 46 | felt_black hand=felt_fine | B 12.53
  - `£2.70 lb` | patrick-hand 400 | cap 15 | centre 52.5 | base 16 | felt_red hand=felt | B 3.95

#### K09b  Fish price ticket: HADDOCK

- 105 x 74 mm (own size); 2 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 2 (stuck in the fish on the slab, or taped to the glass; a wet corner)
- mirror cue: a drawing-pin hole at the top-RIGHT only and a torn lower-LEFT corner
  - `HADDOCK` | patrick-hand 400 | cap 13 | centre 52.5 | base 46 | felt_black hand=felt_fine | B 12.53
  - `£2.50 lb` | patrick-hand 400 | cap 15 | centre 52.5 | base 16 | felt_red hand=felt | B 3.95

#### K09c  Fish price ticket: PLAICE

- 105 x 74 mm (own size); 2 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 2 (stuck in the fish on the slab, or taped to the glass; a wet corner)
- mirror cue: a string loop and rubber sucker at the top-LEFT, a crease running from the top-right corner
  - `PLAICE` | patrick-hand 400 | cap 13 | centre 52.5 | base 46 | felt_black hand=felt_fine | B 12.53
  - `£2.30 lb` | patrick-hand 400 | cap 15 | centre 52.5 | base 16 | felt_red hand=felt | B 3.95

#### K09d  Fish price ticket: KIPPERS

- 105 x 74 mm (own size); 2 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 2 (stuck in the fish on the slab, or taped to the glass; a wet corner)
- mirror cue: two tape tabs, a long one at the top-LEFT and a short one at the top-RIGHT, the left one lifting
  - `KIPPERS` | patrick-hand 400 | cap 13 | centre 52.5 | base 46 | felt_black hand=felt_fine | B 12.53
  - `95p PAIR` | patrick-hand 400 | cap 15 | centre 52.5 | base 16 | felt_red hand=felt | B 3.95

#### K09e  Fish price ticket: SMOKED HADDOCK

- 105 x 74 mm (own size); 2 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 2 (stuck in the fish on the slab, or taped to the glass; a wet corner)
- mirror cue: a tab of yellowed tape across the top-LEFT corner only
  - `SMOKED HADDOCK` | patrick-hand 400 | cap 8.5 | centre 52.5 | base 46 | felt_black hand=felt_fine | B 12.53
  - `£2.40 lb` | patrick-hand 400 | cap 15 | centre 52.5 | base 16 | felt_red hand=felt | B 3.95

#### K09f  Fish price ticket: COCKLES

- 105 x 74 mm (own size); 2 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 2 (stuck in the fish on the slab, or taped to the glass; a wet corner)
- mirror cue: a drawing-pin hole at the top-RIGHT only and a torn lower-LEFT corner
  - `COCKLES` | patrick-hand 400 | cap 13 | centre 52.5 | base 46 | felt_black hand=felt_fine | B 12.53
  - `45p` | patrick-hand 400 | cap 15 | centre 52.5 | base 16 | felt_red hand=felt | B 3.95

**The newsagent's board SB1** (760 x 560 mm on the glass at u 1.95 m, z 0.90 m): fifteen cards of two sizes (127 x 76 record cards, 148 x 105 postcards), taped inside the glass.

| Card | at (x, y) mm | size | rot | fixing |
|---|---|---|---|---|
| SA15 | 23, 428 | 148 x 105 | -2.0 | tape top-right |
| SA01 | 195, 467 | 127 x 76 | 2.3 | pin top |
| SA02 | 358, 458 | 127 x 76 | -0.5 | pin top and tape |
| SA03 | 512, 432 | 148 x 105 | -1.8 | pin top and tape |
| SA04 | 24, 332 | 127 x 76 | 1.0 | tape top-right |
| SA05 | 188, 330 | 127 x 76 | -0.7 | tape top-right |
| SA06 | 345, 306 | 148 x 105 | -1.6 | tape top-right |
| SA07 | 517, 339 | 127 x 76 | -0.4 | pin top |
| SA08 | 21, 205 | 127 x 76 | -1.0 | tape top-left |
| SA09 | 178, 169 | 148 x 105 | 0.0 | tape top-right |
| SA10 | 348, 204 | 127 x 76 | 2.1 | tape top-left |
| SA11 | 501, 205 | 127 x 76 | -0.4 | pin top |
| SA12 | 16, 73 | 127 x 76 | 1.5 | pin top and tape |
| SA13 | 181, 62 | 127 x 76 | -0.1 | tape top-right |
| SA14 | 339, 65 | 127 x 76 | -0.9 | tape top-left |

#### SA01  Newsagent window card 01

- 127 x 76 mm (own size); 2 px/mm; stock: white record card; process: ballpoint_card
- variants: 1 (pinned or taped on the newsagent's board: a pin or a tab of tape at the top; slight tilt)
- mirror cue: a string loop and rubber sucker at the top-LEFT, a crease running from the top-right corner
  - `ROOM TO LET` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_blue hand=felt_fine | B 6.81
  - `Clean, quiet, gas fire.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_black hand=ballpoint | B 11.13
  - `£28 per week. No pets.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_black hand=ballpoint | B 11.13
  - `Ring 960 417 after 5.` | patrick-hand 400 | cap 4.4 | left 8 | base 31.6 | ballpoint_black hand=ballpoint | B 11.13

#### SA02  Newsagent window card 02

- 127 x 76 mm (own size); 2 px/mm; stock: blue record card; process: ballpoint_card
- variants: 1 (pinned or taped on the newsagent's board: a pin or a tab of tape at the top; slight tilt)
- mirror cue: two tape tabs, a long one at the top-LEFT and a short one at the top-RIGHT, the left one lifting
  - `GENTS BICYCLE` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_black hand=felt_fine | B 9.97
  - `3-speed, good tyres.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_blue hand=ballpoint | B 5.79
  - `£18 or nearest offer.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_blue hand=ballpoint | B 5.79
  - `Tel. 960 233.` | patrick-hand 400 | cap 4.4 | left 8 | base 31.6 | ballpoint_blue hand=ballpoint | B 5.79

#### SA03  Newsagent window card 03

- 148 x 105 mm (own size); 2 px/mm; stock: yellow record card; process: ballpoint_card
- variants: 1 (pinned or taped on the newsagent's board: a pin or a tab of tape at the top; slight tilt)
- mirror cue: a tab of yellowed tape across the top-LEFT corner only
  - `PIANO FOR SALE` | patrick-hand 400 | cap 7 | left 8 | base 89.5 | felt_black hand=felt_fine | B 11.54
  - `Upright, good tone.` | patrick-hand 400 | cap 4.4 | left 8 | base 78.6 | ballpoint_blue hand=ballpoint | B 6.74
  - `Buyer collects. £120.` | patrick-hand 400 | cap 4.4 | left 8 | base 69.6 | ballpoint_blue hand=ballpoint | B 6.74
  - `Ring 960 528.` | patrick-hand 400 | cap 4.4 | left 8 | base 60.6 | ballpoint_blue hand=ballpoint | B 6.74

#### SA04  Newsagent window card 04

- 127 x 76 mm (own size); 2 px/mm; stock: white record card; process: ballpoint_card
- variants: 1 (pinned or taped on the newsagent's board: a pin or a tab of tape at the top; slight tilt)
- mirror cue: a drawing-pin hole at the top-RIGHT only and a torn lower-LEFT corner
  - `WINDOW CLEANER` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_blue hand=felt_fine | B 6.81
  - `Reliable. Free estimates.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_blue hand=ballpoint | B 7.31
  - `Tel. 960 361.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_blue hand=ballpoint | B 7.31

#### SA05  Newsagent window card 05

- 127 x 76 mm (own size); 2 px/mm; stock: pink record card; process: ballpoint_card
- variants: 1 (pinned or taped on the newsagent's board: a pin or a tab of tape at the top; slight tilt)
- mirror cue: a string loop and rubber sucker at the top-LEFT, a crease running from the top-right corner
  - `DECORATING` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_black hand=felt_fine | B 9.56
  - `Indoor and out.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_black hand=ballpoint | B 8.4
  - `Fair prices. 960 774.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_black hand=ballpoint | B 8.4

#### SA06  Newsagent window card 06

- 148 x 105 mm (own size); 2 px/mm; stock: white record card; process: ballpoint_card
- variants: 1 (pinned or taped on the newsagent's board: a pin or a tab of tape at the top; slight tilt)
- mirror cue: two tape tabs, a long one at the top-LEFT and a short one at the top-RIGHT, the left one lifting
  - `LOST` | patrick-hand 400 | cap 7 | left 8 | base 89.5 | felt_black hand=felt_fine | B 12.68
  - `Black and white cat,` | patrick-hand 400 | cap 4.4 | left 8 | base 78.6 | ballpoint_blue hand=ballpoint | B 7.31
  - `answers to Smudge.` | patrick-hand 400 | cap 4.4 | left 8 | base 69.6 | ballpoint_blue hand=ballpoint | B 7.31
  - `Last seen on Quay Street.` | patrick-hand 400 | cap 4.4 | left 8 | base 60.6 | ballpoint_blue hand=ballpoint | B 7.31
  - `Reward. 960 189.` | patrick-hand 400 | cap 4.4 | left 8 | base 51.6 | ballpoint_blue hand=ballpoint | B 7.31

#### SA07  Newsagent window card 07

- 127 x 76 mm (own size); 2 px/mm; stock: green record card; process: ballpoint_card
- variants: 1 (pinned or taped on the newsagent's board: a pin or a tab of tape at the top; slight tilt)
- mirror cue: a tab of yellowed tape across the top-LEFT corner only
  - `FOUND` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_blue hand=felt_fine | B 5.69
  - `Bunch of keys on` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_blue hand=ballpoint | B 6.12
  - `Quay Street. Enquire within.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_blue hand=ballpoint | B 6.12

#### SA08  Newsagent window card 08

- 127 x 76 mm (own size); 2 px/mm; stock: white record card; process: ballpoint_card
- variants: 1 (pinned or taped on the newsagent's board: a pin or a tab of tape at the top; slight tilt)
- mirror cue: a drawing-pin hole at the top-RIGHT only and a torn lower-LEFT corner
  - `TYPING DONE AT HOME` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_black hand=felt_fine | B 12.68
  - `Letters and CVs.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_blue hand=ballpoint | B 7.31
  - `960 842.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_blue hand=ballpoint | B 7.31

#### SA09  Newsagent window card 09

- 148 x 105 mm (own size); 2 px/mm; stock: blue record card; process: ballpoint_card
- variants: 1 (pinned or taped on the newsagent's board: a pin or a tab of tape at the top; slight tilt)
- mirror cue: a string loop and rubber sucker at the top-LEFT, a crease running from the top-right corner
  - `MAN WITH VAN` | patrick-hand 400 | cap 7 | left 8 | base 89.5 | felt_black hand=felt_fine | B 9.97
  - `Removals and house` | patrick-hand 400 | cap 4.4 | left 8 | base 78.6 | ballpoint_black hand=ballpoint | B 8.79
  - `clearance. Anywhere.` | patrick-hand 400 | cap 4.4 | left 8 | base 69.6 | ballpoint_black hand=ballpoint | B 8.79
  - `960 655.` | patrick-hand 400 | cap 4.4 | left 8 | base 60.6 | ballpoint_black hand=ballpoint | B 8.79

#### SA10  Newsagent window card 10

- 127 x 76 mm (own size); 2 px/mm; stock: yellow record card; process: ballpoint_card
- variants: 1 (pinned or taped on the newsagent's board: a pin or a tab of tape at the top; slight tilt)
- mirror cue: two tape tabs, a long one at the top-LEFT and a short one at the top-RIGHT, the left one lifting
  - `GAS COOKER` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_blue hand=felt_fine | B 6.32
  - `4 ring, hardly used.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_blue hand=ballpoint | B 6.74
  - `£35. Ring 960 307.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_blue hand=ballpoint | B 6.74

#### SA11  Newsagent window card 11

- 127 x 76 mm (own size); 2 px/mm; stock: white record card; process: ballpoint_card
- variants: 1 (pinned or taped on the newsagent's board: a pin or a tab of tape at the top; slight tilt)
- mirror cue: a tab of yellowed tape across the top-LEFT corner only
  - `WANTED` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_black hand=felt_fine | B 12.68
  - `Part-time help, mornings.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_blue hand=ballpoint | B 7.31
  - `Apply within.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_blue hand=ballpoint | B 7.31

#### SA12  Newsagent window card 12

- 127 x 76 mm (own size); 2 px/mm; stock: pink record card; process: ballpoint_card
- variants: 1 (pinned or taped on the newsagent's board: a pin or a tab of tape at the top; slight tilt)
- mirror cue: a drawing-pin hole at the top-RIGHT only and a torn lower-LEFT corner
  - `SEWING MACHINE` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_black hand=felt_fine | B 9.56
  - `Electric. £25.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_blue hand=ballpoint | B 5.6
  - `Tel. 960 912.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_blue hand=ballpoint | B 5.6

#### SA13  Newsagent window card 13

- 127 x 76 mm (own size); 2 px/mm; stock: white record card; process: ballpoint_card
- variants: 1 (pinned or taped on the newsagent's board: a pin or a tab of tape at the top; slight tilt)
- mirror cue: a string loop and rubber sucker at the top-LEFT, a crease running from the top-right corner
  - `COLOUR TV` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_blue hand=felt_fine | B 6.81
  - `22 inch, working. £40.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_black hand=ballpoint | B 11.13
  - `Ring 960 483.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_black hand=ballpoint | B 11.13

#### SA14  Newsagent window card 14

- 127 x 76 mm (own size); 2 px/mm; stock: green record card; process: ballpoint_card
- variants: 1 (pinned or taped on the newsagent's board: a pin or a tab of tape at the top; slight tilt)
- mirror cue: two tape tabs, a long one at the top-LEFT and a short one at the top-RIGHT, the left one lifting
  - `CHIMNEY SWEEP` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_black hand=felt_fine | B 10.4
  - `Clean and tidy.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_blue hand=ballpoint | B 6.12
  - `960 596.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_blue hand=ballpoint | B 6.12

#### SA15  Newsagent: ADVERTISE HERE card

- 148 x 105 mm (A6L); 2 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 1 (top of the board, taped)
- mirror cue: a tab of yellowed tape across the top-LEFT corner only
  - `ADVERTISE HERE` | patrick-hand 400 | cap 12 | centre 74 | base 80 | felt_red hand=felt | B 3.95
  - `20p PER WEEK` | patrick-hand 400 | cap 14 | centre 74 | base 56 | felt_black hand=felt | B 12.53
  - `PAY AT THE COUNTER` | patrick-hand 400 | cap 8 | centre 74 | base 34 | felt_black hand=felt_fine | B 12.53

## 6. "To Let" boards (unit 4.3)

The agent is PROPOSED: **ARMITAGE & STOBBS, Chartered Surveyors, Estate Agents** (not minted; a placeholder never to reach his page; not checked against real firms, the network refusing the sources). A no-agent variant keeps the number. The number is the local six-figure form 960 335. The existing board (`board_to_let.png`, 900 x 450, PT Sans, no agent, no number) is replaced. 450 mm is the height a 0.55 m fascia takes with 50 mm clear above and below, and 1200 mm gives the agent's band, TO LET at cap 150 and the number their room; area 0.54 square metres, well under the 2.0 square metres a board could be in the 1984 regulations (a Lead from a search summary; the exact figure and the later cut are not read). A letting board is white gloss on 18 mm exterior plywood, corners rounded 4 mm, the cut edges painted, a 25 x 18 mm batten at each end, four 8 mm dome-head coach screws 40 mm in from the corners with a rust run 40 to 140 mm under each lower one, hung 2 degrees askew. Colours: agent navy (28,46,94), red (178,34,40), white (236,236,230); at class D the white yellows to (214,206,184) and the red fades towards chalk-pink by 0.3. Fonts: Jost (Futura-like, the estate agents' and chemists' 1980s face, asset-plan table).

#### L01  Letting board, shop, with agent (1200 x 450)

- 1200 x 450 mm (own size); 1 px/mm; process: agent_board
- variants: 3 (askew -2, 0, +2 degrees; age class B, C, D (the D board has the white yellowed and the red faded to rust-pink); one with a diagonal LET strip: NOT USED (no new word))
- shape face (rect): box [0, 0, 1200, 450], fill agent_white - 18 mm exterior plywood painted white gloss, corners rounded 4 mm, the cut edges painted, a 25 x 18 mm batten on the back at each end
- shape band (rect): box [0, 332, 1200, 450], fill agent_navy
  - `ARMITAGE & STOBBS` | jost 700 | cap 52 | centre 600 | base 384 | agent_white | B 8.94
  - `CHARTERED SURVEYORS · ESTATE AGENTS` | jost 500 | cap 18.7 | centre 600 | base 342 | agent_white | B 8.94
  - `TO LET` | jost 800 | cap 150 | centre 600 | base 164 | agent_red | B 4.98
  - `SHOP AND PREMISES · APPROX. 520 SQ. FT.` | jost 600 | cap 24 | centre 600 | base 127.4 | agent_navy | B 8.94
  - `ENQUIRIES 960 335` | jost 700 | cap 46 | centre 600 | base 63.4 | agent_navy | B 8.94

- mounted on: the empty unit's fascia (bay 3, east, street x 21 to 27); centre street x 24.0 m; z 2.9 to 3.35 m; four 8 mm dome-head coach screws at 40 mm in from each corner; a rust run 40 to 140 mm under each lower screw; askew -2 to +2 degrees. the fascia is 0.55 m tall (2.85 to 3.40): the board leaves 50 mm above and below; its centre is the fascia target's own letting-board centre (board x 2705, y 275)

#### L02  Letting board, shop, no agent (1200 x 450)

- 1200 x 450 mm (own size); 1 px/mm; process: agent_board
- variants: 2 (askew; age class B, D)
- shape face (rect): box [0, 0, 1200, 450], fill agent_white - 18 mm exterior plywood painted white gloss, corners rounded 4 mm, the cut edges painted, a 25 x 18 mm batten on the back at each end
- shape hairline (frame): box [12, 12, 1188, 438], fill agent_navy
  - `TO LET` | jost 800 | cap 190 | centre 600 | base 200 | agent_red | B 4.98
  - `ENQUIRIES 960 335` | jost 700 | cap 56 | centre 600 | base 110.4 | agent_navy | B 8.94

- mounted on: the empty unit's fascia (bay 3, east, street x 21 to 27); centre street x 24.0 m; z 2.9 to 3.35 m; four 8 mm dome-head coach screws at 40 mm in from each corner; a rust run 40 to 140 mm under each lower screw; askew -2 to +2 degrees. the fascia is 0.55 m tall (2.85 to 3.40): the board leaves 50 mm above and below; its centre is the fascia target's own letting-board centre (board x 2705, y 275)

#### L03  Letting board, flat, with agent (600 x 400)

- 600 x 400 mm (own size); 1 px/mm; process: agent_board
- variants: 2 (age class C, D; the agent's board has been up a long time: grime streaks from the top edge)
- shape face (rect): box [0, 0, 600, 400], fill agent_white - 18 mm exterior plywood painted white gloss, corners rounded 4 mm, the cut edges painted, a 25 x 18 mm batten on the back at each end
- shape band (rect): box [0, 316, 600, 400], fill agent_navy
  - `ARMITAGE & STOBBS` | jost 700 | cap 30 | centre 300 | base 356 | agent_white | B 8.94
  - `CHARTERED SURVEYORS · ESTATE AGENTS` | jost 500 | cap 10.8 | centre 300 | base 326 | agent_white | B 8.94
  - `TO LET` | jost 800 | cap 106 | centre 300 | base 182 | agent_red | B 4.98
  - `SELF-CONTAINED FLAT` | jost 600 | cap 24 | centre 300 | base 138.4 | agent_navy | B 8.94
  - `ENQUIRIES 960 335` | jost 700 | cap 34 | centre 300 | base 76.4 | agent_navy | B 8.94

- mounted on: first-floor brick above the empty unit's cornice, between the two upper windows; centre street x 24.0 m; z 3.7 to 4.1 m; four 6 mm screws and plugs; askew -1.5 to +1.5 degrees. the cornice top is 3.55 m, the upper sill about 4.3 m (facade: head 0.4 below the ceiling, window 1.5 high): 0.75 m of plain brick; Rita's hanging sign is at street x 20.825 and the laundry's at 27.175, both outside bay 3

#### L04  Letting board, house, no agent (600 x 400)

- 600 x 400 mm (own size); 1 px/mm; process: agent_board
- variants: 2 (age class B, D)
- shape face (rect): box [0, 0, 600, 400], fill agent_white - 18 mm exterior plywood painted white gloss, corners rounded 4 mm, the cut edges painted, a 25 x 18 mm batten on the back at each end
- shape hairline (frame): box [12, 12, 588, 388], fill agent_navy
  - `TO LET` | jost 800 | cap 104 | centre 300 | base 238.5 | agent_red | B 4.98
  - `TWO BEDROOMS` | jost 600 | cap 30 | centre 300 | base 176.7 | agent_navy | B 8.94
  - `ENQUIRIES 960 335` | jost 700 | cap 32 | centre 300 | base 99.2 | agent_navy | B 8.94

- mounted on: the west terrace (bay 2 of the plain block, street x 15 to 21): the brick pier between the two windows; centre street x 16.8 m; z 2.15 to 2.55 m; four 6 mm screws and plugs; askew -1.5 to +1.5 degrees. pier 16.35 to 17.25 (window 15.9 and 17.7, 0.85 wide, from the plain row's bay layout, mirrored in bay 2); the board is 0.6 wide

## 7. Street name plates (unit 4.4)

**What 1990 British plates carried, as far as I could establish.** No photograph was reached. From search summaries (Leads): there was never a national design and each council chose its own style, colour, size and material; black capitals on white with a black border was the default the 1993 Department of Transport circular recommends and the usual look; the Ministry of Transport's alphabets date from the early 1930s, the Kindersley lettering was adopted in 1951 and recommended in 1952; Hull's cast plates of the 1920s to 1930s were black on white and their paint faded or flaked; London plates carried the borough and the postal district; councils often added a crest or their name; I found NO source that provincial plates of the 1980s carried a postal district, and the project's earlier street-clutter note lists postcodes as wrong for 1990. **What I chose (Judgement):** the street's name in capitals; below the top border a small line with the DISTRICT's name (THE HOOK, COPPER ROW, IRONSIDE: canon's minted districts); no council, no crest (canon owes the council's name); no postcode by default. Variant `n` drops the district line; variant `p` adds a placeholder postal district MR1 at the left of the district line (MR is not a real UK postcode area; never on his page). **Letter style:** Marcellus SC capitals, 90 mm tall, tracking +0.04 em, ruled on 30 September for the street plates (it stands in for the Kindersley serif, which has no allowed free version); the ruling beats the earlier note and the Hull caption (whose plates used the older MOT sans alphabets), see section 11.

**Sizes.** Plate length follows the name: ink width plus 2 x 62 mm (6 mm edge + 12 mm border + 44 mm clear), rounded up to 10 mm. Depth 170 mm without a district line and 225 mm with one; Quay Street's are 190 and 240 because the Q's tail dips 36 mm below the baseline. The border band is 12 mm, 6 mm in from the edge; corners rounded 6 mm. Fixing: four screws 30 mm in from the corners (10 mm dome heads into fibre plugs; the cast plate has four 12 mm holes cast in). Mounting height: bottom edge at 2.5 m, centre 2.63 m (the earlier note says 2.2 to 2.5 m, the existing plate hangs at 2.50 to 2.76).

**Materials by street (Judgement).** QUAY STREET: cast iron, raised letters and border 4 mm proud on an 8 mm face, painted white with black letters, repainted over the years, the paint flaking first from the raised edges to grey iron and a thin rust film (the Hook is the old port, and its plates are the oldest). WEIGHHOUSE LANE: die-pressed aluminium 2 mm, letters raised 1.5 mm, stove enamel, rolled edge. TANNERY ROW: vitreous enamel on pressed steel, rolled edge.

| Plate | street | district | variant | plate (mm) | ink width | material |
|---|---|---|---|---|---|---|
| S01d | QUAY STREET | THE HOOK | d | 980 x 240 | 855.0 | cast_iron_raised |
| S01n | QUAY STREET | (none) | n | 980 x 190 | 855.0 | cast_iron_raised |
| S01p | QUAY STREET | THE HOOK | p | 980 x 240 | 855.0 | cast_iron_raised |
| S02d | WEIGHHOUSE LANE | COPPER ROW | d | 1360 x 225 | 1234.0 | pressed_aluminium_enamel |
| S02n | WEIGHHOUSE LANE | (none) | n | 1360 x 170 | 1234.0 | pressed_aluminium_enamel |
| S02p | WEIGHHOUSE LANE | COPPER ROW | p | 1360 x 225 | 1234.0 | pressed_aluminium_enamel |
| S03d | TANNERY ROW | IRONSIDE | d | 1100 x 225 | 968.0 | vitreous_enamel_steel |
| S03n | TANNERY ROW | (none) | n | 1100 x 170 | 968.0 | vitreous_enamel_steel |
| S03p | TANNERY ROW | IRONSIDE | p | 1100 x 225 | 968.0 | vitreous_enamel_steel |

Placed: **S01d** at street x 20.47 on the west corner pier (x 19.92 to 21.0, brick to 3.12 m: the existing plate's place, kept, 80 mm of pier either side), centre z 2.63; **S01d** again on the quay gable, centre 1.0 m from the front corner, z 2.63; **S02d** (WEIGHHOUSE LANE) on the near flank of the first shop beyond the side opening (the x = 24.0 wall, facing -x), centre 0.9 m from its front corner, PROPOSED because canon does not name the opening. **S03** (TANNERY ROW) is a town kit plate and is not placed on Quay Street. The plate board's pictures: `L4` shows all nine.

#### S01d  Street name plate: QUAY STREET (name and district)

  - `QUAY STREET` | marcellus-sc | cap 90 | centre 490 | base 58 | B 11.67
  - `THE HOOK` | marcellus-sc | cap 30 | centre 490 | base 170 | B 11.67

#### S01n  Street name plate: QUAY STREET (name only)

  - `QUAY STREET` | marcellus-sc | cap 90 | centre 490 | base 58 | B 11.67

#### S01p  Street name plate: QUAY STREET (name, district and placeholder postal district)

  - `QUAY STREET` | marcellus-sc | cap 90 | centre 490 | base 58 | B 11.67
  - `THE HOOK` | marcellus-sc | cap 30 | centre 490 | base 170 | B 11.67
  - `MR1` | marcellus-sc | cap 22 | left 40 | base 174 | B 11.67

#### S02d  Street name plate: WEIGHHOUSE LANE (name and district)

  - `WEIGHHOUSE LANE` | marcellus-sc | cap 90 | centre 680 | base 40 | B 11.67
  - `COPPER ROW` | marcellus-sc | cap 30 | centre 680 | base 152 | B 11.67

#### S02n  Street name plate: WEIGHHOUSE LANE (name only)

  - `WEIGHHOUSE LANE` | marcellus-sc | cap 90 | centre 680 | base 40 | B 11.67

#### S02p  Street name plate: WEIGHHOUSE LANE (name, district and placeholder postal district)

  - `WEIGHHOUSE LANE` | marcellus-sc | cap 90 | centre 680 | base 40 | B 11.67
  - `COPPER ROW` | marcellus-sc | cap 30 | centre 680 | base 152 | B 11.67
  - `MR1` | marcellus-sc | cap 22 | left 40 | base 156 | B 11.67

#### S03d  Street name plate: TANNERY ROW (name and district)

  - `TANNERY ROW` | marcellus-sc | cap 90 | centre 550 | base 40 | B 11.67
  - `IRONSIDE` | marcellus-sc | cap 30 | centre 550 | base 152 | B 11.67

#### S03n  Street name plate: TANNERY ROW (name only)

  - `TANNERY ROW` | marcellus-sc | cap 90 | centre 550 | base 40 | B 11.67

#### S03p  Street name plate: TANNERY ROW (name, district and placeholder postal district)

  - `TANNERY ROW` | marcellus-sc | cap 90 | centre 550 | base 40 | B 11.67
  - `IRONSIDE` | marcellus-sc | cap 30 | centre 550 | base 152 | B 11.67
  - `MR1` | marcellus-sc | cap 22 | left 40 | base 156 | B 11.67

## 8. The paste plan: placements

Layers run from the oldest (0) to the newest; age class A to D is the paper's age. The gable's bills are laid by a seeded packer (seed 20261064) and kept only if every older bill keeps its share of face (layer 0 at least 0.30, layer 1 at least 0.45, the top layer all of it). The builder may re-seed; the rule must hold.

| Surface | Item | where | z bottom (m) | rot | layer | age | size (m) |
|---|---|---|---|---|---|---|---|
| SF1 | M01 | u 0.35 | 0.78 | 0.4 | 0 | D | 0.508 x 0.762 |
| SF1 | T03 | u 0.90 | 0.80 | 1.3 | 0 | D | 0.508 x 0.762 |
| SF1 | G01 | u 1.48 | 0.77 | -0.5 | 0 | C | 1.016 x 1.524 |
| SF1 | W01 | u 0.60 | 1.14 | 0.5 | 1 | B | 0.508 x 0.762 |
| SF1 | J01 | u 1.46 | 1.04 | -0.7 | 1 | B | 0.381 x 0.508 |
| SF1 | D01 | u 2.14 | 0.93 | 0.4 | 1 | C | 0.508 x 0.762 |
| SF1 | T02 | u 2.98 | 0.97 | -0.6 | 1 | B | 1.016 x 0.762 |
| SF1 | B01 | u 4.27 | 0.86 | -0.0 | 1 | B | 0.508 x 0.762 |
| SF1 | P01 | u 0.95 | 1.23 | 1.1 | 2 | A | 0.508 x 0.762 |
| SF1 | P03 | u 1.56 | 1.25 | 0.9 | 2 | A | 0.508 x 0.762 |
| SF1 | P02 | u 2.11 | 1.28 | -0.5 | 2 | B | 0.508 x 0.762 |
| SF1 | T01 | u 2.66 | 1.24 | -1.1 | 2 | A | 1.016 x 0.762 |
| SF1 | P05 | u 0.34 | 1.02 | 0.0 | 3 | B | 0.095 x 0.060 |
| SF1 | P06 | u 2.55 | 0.52 | 0.0 | 3 | C | 0.148 x 0.052 |
| SF1 | P05 | u 3.10 | 1.45 | 0.0 | 3 | D | 0.095 x 0.060 |
| SF1 | HC1 | u 6.95 | 1.20 | 0.0 | 0 | C | 0.640 x 0.880 |
| SF1 | FC1 | u 6.20 | 1.20 | 0.0 | 0 | C | 0.530 x 0.710 |
| SF2 | M01 | u 0.10 | 0.78 | 0.8 | 0 | C | 0.508 x 0.762 |
| SF2 | P03 | u 0.62 | 0.90 | 1.2 | 1 | B | 0.508 x 0.762 |
| SF2 | P01 | u 1.20 | 0.82 | 0.0 | 1 | B | 0.508 x 0.762 |
| SF2 | P01 | u 1.55 | 0.78 | -1.5 | 2 | A | 0.508 x 0.762 |
| SF2 | P02 | u 2.20 | 0.95 | 0.6 | 1 | B | 0.508 x 0.762 |
| SF2 | J01 | u 2.74 | 1.05 | -0.8 | 1 | C | 0.381 x 0.508 |
| SF2 | C02 | u 3.10 | 1.50 | 0.0 | 2 | A | 0.210 x 0.297 |
| SF2 | P06 | u 1.02 | 0.66 | 0.0 | 3 | B | 0.148 x 0.052 |
| WEST_PIER | C01a | street x 5.397 pier W0.0 | 1.30 | 0.0 | 1 | B | 0.297 x 0.420 |
| WEST_PIER | M01 | street x 7.2 pier W0.1 | 0.85 | 0.0 | 1 | C | 0.508 x 0.762 |
| WEST_PIER | W01 | street x 11.397 pier W1.0 | 1.00 | 0.0 | 1 | B | 0.508 x 0.762 |
| WEST_PIER | P02 | street x 13.2 pier W1.1 | 0.95 | 0.0 | 1 | B | 0.508 x 0.762 |
| WEST_PIER | J01 | street x 16.8 pier W2.0 | 1.00 | 0.0 | 1 | C | 0.381 x 0.508 |
| WEST_PIER | D01 | street x 18.603 pier W2.1 | 0.90 | 0.0 | 1 | C | 0.508 x 0.762 |
| WEST_PIER | L04 | street x 16.8 pier W2.0 | 2.15 | 0.0 | 2 | C | 0.600 x 0.400 |
| SF4 | C03 | street x 8.0 | 1.55 | 0.0 | 1 | A | 0.297 x 0.420 |
| SF4 | P05 | street x 8.0 | 1.25 | 0.0 | 1 | C | 0.095 x 0.060 |
| SF4 | P06 | street x 28.0 | 1.45 | 0.0 | 1 | B | 0.148 x 0.052 |
| SF4 | P05 | street x 28.0 | 1.85 | 0.0 | 1 | D | 0.095 x 0.060 |
| SF5 | L01 | street x 24.0 | 2.90 | -1.5 | 0 | C | 1.200 x 0.450 |
| SF6 | L03 | street x 24.0 | 3.70 | 1.0 | 0 | C | 0.600 x 0.400 |
| SF7 | S01d | street x 20.47 | 2.51 | 0.0 | 0 | D | 0.980 x 0.240 |
| SF7 | S01d | street x None | 2.51 | 0.0 | 0 | D | 0.980 x 0.240 |
| SF7 | S02d | street x None | 2.52 | 0.0 | 0 | D | 1.360 x 0.225 |
| SF8 | H02 | street x -0.6 | 1.20 | 0.0 | 0 | C | 0.600 x 0.450 |
| SHOP | K09a | fish_market glass u 0.30 | 0.66 | -2 | 1 | B | 0.105 x 0.074 |
| SHOP | K09b | fish_market glass u 0.95 | 0.66 | 3 | 1 | B | 0.105 x 0.074 |
| SHOP | K09c | fish_market glass u 1.60 | 0.66 | -1 | 1 | B | 0.105 x 0.074 |
| SHOP | K09d | fish_market glass u 2.25 | 0.66 | 2 | 1 | B | 0.105 x 0.074 |
| SHOP | K09e | fish_market glass u 2.80 | 0.66 | -3 | 1 | B | 0.105 x 0.074 |
| SHOP | K09f | fish_market glass u 3.30 | 0.66 | 1 | 1 | B | 0.105 x 0.074 |
| SHOP | K04 | fish_market door u 0.38 | 1.05 | 0.0 | 1 | B | 0.150 x 0.105 |
| SHOP | K03a | fish_market door u 0.35 | 1.62 | 0.0 | 1 | B | 0.200 x 0.110 |
| SHOP | K03a | ritas door u 0.35 | 1.62 | 0.0 | 1 | B | 0.200 x 0.110 |
| SHOP | K03a | steam_laundry door u 0.35 | 1.62 | 0.0 | 1 | B | 0.200 x 0.110 |
| SHOP | K06a | steam_laundry glass u 0.20 | 1.25 | 1.0 | 1 | B | 0.210 x 0.148 |
| SHOP | K06b | steam_laundry glass u 1.85 | 1.00 | -0.8 | 1 | B | 0.210 x 0.148 |
| SHOP | K06c | steam_laundry interior u 0.00 | 0.85 | 2.0 | 1 | B | 0.148 x 0.105 |
| SHOP | K07a | grocer glass u 0.20 | 1.55 | -3 | 1 | B | 0.170 x 0.170 |
| SHOP | K07b | grocer glass u 0.95 | 1.20 | 2 | 1 | B | 0.170 x 0.170 |
| SHOP | K07c | grocer glass u 1.70 | 1.60 | -2 | 1 | B | 0.170 x 0.170 |
| SHOP | K07d | grocer glass u 2.45 | 1.25 | 4 | 1 | B | 0.170 x 0.170 |
| SHOP | K08 | grocer glass u 3.00 | 0.95 | 0.0 | 1 | B | 0.210 x 0.148 |
| SHOP | K04 | grocer door u 0.38 | 1.05 | 0.0 | 1 | B | 0.150 x 0.105 |
| SHOP | K03a | grocer door u 0.35 | 1.62 | 0.0 | 1 | B | 0.200 x 0.110 |
| SHOP | K03a | chandler door u 0.35 | 1.62 | 0.0 | 1 | B | 0.200 x 0.110 |
| SHOP | K03a | ironmonger door u 0.35 | 1.62 | 0.0 | 1 | B | 0.200 x 0.110 |
| SHOP | K03a | newsagent door u 0.35 | 1.62 | 0.0 | 1 | B | 0.200 x 0.110 |
| SHOP | K05 | newsagent door u 0.34 | 1.12 | 1.5 | 1 | B | 0.210 x 0.148 |
| SHOP | K02 | newsagent glass u 0.30 | 1.20 | 0.0 | 1 | B | 0.130 x 0.170 |
| SHOP | K04 | tea_rooms door u 0.38 | 1.05 | 0.0 | 1 | B | 0.150 x 0.105 |
| SHOP | K03a | tea_rooms door u 0.35 | 1.62 | 0.0 | 1 | B | 0.200 x 0.110 |
| SHOP | SB1 | newsagent glass u 1.95 | 0.90 | 0.0 | 1 | B | 0.760 x 0.560 |

## 9. The words, as a list

308 approved strings (`approved_words`), 632 tokens (`approved_word_parts`). Every string is ours. Checked against: this file's forbidden lists (alcohol, gambling, children, real marks, names canon owes, things after 1992); `tools/content-gate.py`'s 88 speech rules; `RealWorld.cs`'s names; imagegen's forbidden tokens; canon's streets and districts; the cast's surnames. **Proposed, unminted names** (placeholders, never on his page):

- `MERIDIAN AGAINST THE POLL TAX`: the invented local anti-poll-tax campaign (ruling 3 Oct: an invented local campaign, never real parties or people). First proposed by the asset plan note 4, used by the 4 Oct bills. (mint: town task)
- `QUAY PRINT`: the jobbing printer named in the imprint of every printed bill (an imprint was the custom and is expected on political and campaign matter) (mint: town task)
- `ARMITAGE & STOBBS`: the estate agent on the letting boards (the brief asks for a proposed name, marked 'proposed, not minted') (mint: town task)
- `THE SANDERLING TRIO`: the dance band on the chapel hall's bill (mint: town task)
- `THE SEA WOLF, MAD MAURICE, TIGER JIM LARKIN, THE BARON`: four invented ring names on the wrestling bill (mint: town task)
- `THE FOURTH WITNESS, A WEEK AT GULLWING`: two invented films at the Tivoli (Gullwing is a minted district) (mint: town task)
- `WHITEWELL, QUAYSIDE TEA`: two invented goods on hoarding bills (a washday powder and a tea) (mint: town task)
- `MARSHLAND PICTURES; A. VENN, R. CORLEY, H. MADDOX`: the invented studio and three invented credits on the two film bills' billing block (mint: town task)
- `THE DRILL HALL`: the hall where the boxing and wrestling bills are held (generic building, no street given) (mint: town task)
- `MR1`: a placeholder postal district for one variant of the street plates (MR is not a real UK postcode area) (mint: town task; NEVER on his page)

Names canon owes and this target therefore does NOT use: the football club, the local paper, the pirate radio station, the regional television channel, the telephone operator, the postal cypher, the council's name. The brand bible v1 carries proposals for four of them (Meridian Town AFC, The Meridian Argus, Radio Tideline, Coastway Television); canon.md still lists them as owed, so none is drawn here.

## 10. Variants the street needs

151 seeded variants over 76 items (a poster is built once, shown in the variants its entry names; nothing is multiplied before one complete sample is approved in the assembled game, CLAUDE.md). The variants differ in: age class (always), skew, ink registration and density, which corner is torn or lifting, tape and pin positions, the second pass's shift, and the hours-driven face (OPEN or CLOSED, the BACK AT hands, the LAST WASH hour). The three police sheets are slot fillers: the same layout with another offence line. Dates move with the calendar: every event bill gives its date as computed words, so a build for another date in 1988 to 1992 re-computes the weekday (`G.dates`).

## 11. Where photographs, books and the ruling disagree, and what I chose

- **street plate lettering.** Wins: the 30 September ruling (Marcellus SC). Against it: the street-clutter note (Kindersley MOT serif, recommended 1952) and a search summary of a Hull caption (1920s to 1930s cast plates used the MOT SANS alphabets; Kindersley from 1951). Chosen: Marcellus SC capitals, 90 mm, tracking +0.04 em. No photograph reached: the ruling stands until one disagrees.
- **postal district on a plate.** Wins: judgement. Against it: the street-clutter note lists 'postcodes' as wrong for 1990; a search summary found NO source of 1980s provincial plates carrying a postal district; London plates did carry the district. Chosen: the default plate carries the DISTRICT NAME as a small line (THE HOOK, COPPER ROW, IRONSIDE: canon's minted districts) and no postcode; the postcode-style variant (MR1) exists as a placeholder, never default; the council's name and crest are omitted (canon owes the council's name)
- **the 4 October bills.** Wins: this target. Against it: tools/props/make_vignette_2d.py: clean flat bills, League Gothic, all four on one generic layout, a spring date (SATURDAY 31 MARCH), 'Admission 10p', 'WEIGHHOUSE LANE HALL', the bills' own fine print readable and straight. Chosen: autumn 1990 dates with computed weekdays, the chapel hall named as hook-cast.json names it, imprints, ageing in four classes, layered pasting, different processes and layouts
- **the letting board.** Wins: this target. Against it: board_to_let.png: 900 x 450, PT Sans, no agent, no number, a white box with a red border. Chosen: 1200 x 450 with an agent band, TO LET, size, a number; the no-agent variant keeps a number; 900 x 450 would need cap 110 and drop the agent band
- **the poster prop's place.** Wins: the plain row's bay layout (terrace-front.py _plain_ground). Against it: vignette-scene.json's held-prop notes put a poster at west x 11.4 and a case at west x 26.4 'between a side door at 25.5 and a window at 27.3' (written before the west_north block became shops). Chosen: x 11.4 is the pier W1.0 (10.919 to 11.875) and stays; the case at 26.4 would stand on the tea room's glass: both cases move to the quay gable
- **the one photograph measured.** Wins: judgement. Against it: the photographed notice case is a modern blue steel replacement with a wide crest header. Chosen: only its vertical fractions inform the glazed case's proportions; the 1990 case is a timber one with thinner rails (HC1)

## 12. The checks

473 checks in `target.json` (`checks`). Per item: `.size` (image size), `.words` (the manifest equals the approved strings), `.pos` (each block's ink box read off the pixels, widened 8 mm along the line and 3 mm up and down, pixels explained by another block's glyphs not counted), `.cap` (letter heights at scale: the cap read off flat-bottomed capitals within a stated fraction, and `cap_px` = cap x px/mm), `.mask` (the block re-rendered from its font compared with the ink pixels: F at least 0.90 for printed lines, 0.85 for small print and typing, 0.78 for hand lettering, 0.55 for imprints), `.contrast` (WCAG on the aged render, class B: not under max(2.2, min(3.0 for caps of 12 mm and over or 4.5 below, 0.9 x nominal))). Global: `G.words.approved`, `G.forbidden`, `G.dates`, `G.mirror`, `G.mirror.cues`, `G.fonts`, `G.proposed`, `G.ferry.schedule`, `G.tides`, `G.place.*`, `G.letting.mount`, `G.plates.*`.

**The checks are tested** (`self_check.py`, group 10) on reference renders of thirteen items: the true render passes every mask and position check; a MIRRORED render fails at least 80 per cent of the blocks whose glyphs can tell; a render shifted 30 mm fails the position check on at least 90 per cent of blocks; the wrong font on the largest block fails its mask check. **A hand-lettered, centred card cannot be told from its mirror by its words** (the in-place flip scores within 0.15) and its font cannot be told within the hand's jitter: the 29 all-hand cards carry an asymmetric cue instead (`mirror_cue`: tape at one corner, a pin hole, a torn corner), and `G.mirror.cues` checks it.

The reference reader is in `self_check.py` (functions `read_pixels`, `read_score`, `read_box`); the builder's own checker should do the same on its rendered item.

## 13. What the target could not settle

- No photograph of a 1990 street name plate, letting board, fly-posted wall or paper notice was reached. Every size of those is Judgement on search-summary leads (90 mm capitals, 150 to 230 mm plates, 12 mm borders: modern specs).
- Whether provincial plates of 1990 carried a postal district, the council's name or a crest: not found. The target omits the council and uses a district-name line.
- The name of the side opening at street x 21 to 24 on the west: not in canon. The WEIGHHOUSE LANE plate there is proposed; the town may name it otherwise.
- Whether the scene has a quay-edge post, a hoarding, a gable wall at x = 3 that faces the hook camera with the geometry assumed here (8 m deep, eaves 6.3 m): read from vignette-scene.json and the recipe, not from the mesh.
- Tobacco bills (cigarettes were advertised on hoardings in 1990): omitted: they need a minted brand and the exact government health-warning wording, which was not read.
- The BBFC certificate roundels on film bills are real marks and are not drawn; the 1990 bills carried them.
- A police appeal board (the yellow A-board) in 1990: the only dated photograph found is from 2007; this target uses an A3 photocopy taped in a window or sleeved on a column instead.
- The local paper's contents bill, the football club's bills and the radio station's stickers: the names are owed (canon), so none is drawn; the brand bible's proposals (Meridian Town AFC, the Argus, Radio Tideline, Coastway) are NOT used.
- Real-name coincidence: the invented film titles, ring names, credits, brands and the agent's name were not checked against real lists (the network refused the sources); each is listed in proposed_names for the town to mint or strike.
- Prices (cinema 2.80, wrestling 4 and 2.50, ferry 60p, tea 1.35) are Judgement except cod (ONS via the earlier note).
- Texture size and mip: not checked in the 5.8.2 source; the builder checks whether bills need padding to powers of two (the fascia target has the same open question).

Unreached today: en.wikipedia.org (DNS and 403); commons.wikimedia.org, geograph.org.uk, flickr.com, archive.org (403); thebeautyoftransport.com (403); legislation.gov.uk, gov.uk (403); historicengland.org.uk, nationalarchives.gov.uk (403); www.west-norfolk.gov.uk and www.wigan.gov.uk PDFs (DNS); github.com file downloads for Liberation's TTFs (403).

## 14. Self-check

Run 2026-10-09 00:29: **SELF-CHECK posters-boards-plates: 215 checks, 215 passed, 0 failed, 13 reported**.

Reported (not failures):
- [3 words] where the proposed names stand (reported) ({"ARMITAGE & STOBBS": ["L01", "L03"], "QUAY PRINT": ["B01", "D01", "F01", "G01", "G02", "J01", "M01", "P01", "P02", "P03", "T03", "W01"], "M)
- [4 fonts] 12 fonts are already in production/fonts; 4 are to be added by the builder with their OFL.txt (['archivo', 'courier-prime', 'courier-prime-bold', 'libre-baskerville'])
- [5 layout] imprints are 7 point (cap 2.4 mm) or 4.0 mm: below the 3 m legibility floor by design (12) 
- [5 layout] cap range of lettering on the street (smallest (2.455, 'H03'), biggest (190, 'P01'))
- [6 contrast] blocks that fade below 1.5 in class D (a bill a season old: reported, as intended for the oldest layer) (14 blocks, e.g. [('K01', 'l1', 1.42), ('K02', 'l1', 1.48), ('K06a', 'l1', 1.42)])
- [7 placements] SF1: stickers lie on bills or on bare brick (reported) ([('P05', ['M01']), ('P06', []), ('P05', ['T02', 'T01'])])
- [8 photograph] the glazed windows were masked in the preview (the interior is flat grey) 
- [10 the checks, tested] K01: mirror cannot be told from the words on a hand-lettered card (2 of 2 blocks blind): the card carries a mirror cue instead (its fixing at one end) 
- [10 the checks, tested] K01: every block is hand-lettered: the font is not checked, only the words 
- [10 the checks, tested] SA06: mirror cannot be told from the words on a hand-lettered card (5 of 5 blocks blind): the card carries a mirror cue instead (its fixing at one end) 
- [10 the checks, tested] SA06: every block is hand-lettered: the font is not checked, only the words 
- [10 the checks, tested] K07a: mirror cannot be told from the words on a hand-lettered card (3 of 3 blocks blind): the card carries a mirror cue instead (its fixing at one end) 
- [10 the checks, tested] K07a: every block is hand-lettered: the font is not checked, only the words 

## 15. Sources

| Id | Kind | What | Read | Author and licence | Used |
|---|---|---|---|---|---|
| P1 | photograph | https://polyhaven.com/a/urban_street_01 ; file https://dl.polyhaven.org/file/ph-assets/HDRIs/extra/Tonemapped%20JPG/urban_street_01.jpg ; info https://api.polyhaven.com/info/urban_street_01 | 8 October 2026 (tonemapped panorama 8192 x 4096, 10.6 MB) | Andreas Mischok; CC0 (polyhaven.com/license read 8 Oct: 'all licensed as CC0'); taken 18 August 2019 (info: date_taken 1566112140) | YES: proportions of a glazed case only (a 2000s replacement, not 1990) |
| P2 | photograph | https://polyhaven.com/a/bethnal_green_entrance | 8 October 2026 (tonemapped 8192 x 4096) | Andreas Mischok; CC0; taken 18 August 2019 | NO: nothing measured; the byelaw sign names alcohol, so NO crop of it is kept anywhere |
| P3 | photographs | https://polyhaven.com/hdris (urban_street_02, 03, 04, adams_place_bridge, birbeck_street_underpass, cambridge, docklands_02, limehouse; canary_wharf, docklands_01 and leadenhall_market were NOT looked at here) | 8 October 2026 (2048 x 1024 tonemapped previews in /home/user/cache/ph/scout) | Andreas Mischok and others (each page); CC0; taken 2019 to 2025 | NO |
| F1 | licence texts | https://raw.githubusercontent.com/google/fonts/main/ofl/<family>/OFL.txt and https://raw.githubusercontent.com/liberationfonts/liberation-fonts/main/LICENSE | 8 October 2026, whole | each family's authors (copyright lines in fonts[].copyright); SIL OFL 1.1 (Liberation: OFL 1.1 with Reserved Font Name Liberation); taken n/a | YES: fonts (Liberation's font files were NOT reached: github.com file downloads return 403; its LICENSE was read; it is not used here) |
| R1 | repository | canon.md; RULINGS.md; production/cloud-week/targets/BRIEF.md and SCENE-SLOTS.md | 8 October 2026 | the project; project; taken n/a | YES |
| R2 | repository | production/specs/hook-cast.json; production/specs/vignette-scene.json; tools/art-recipes/terrace-front.py; tools/props/make_vignette_2d.py; production/assets/vignette/decals2d/ | 8 October 2026 | the project; project; taken n/a | YES |
| R3 | repository | production/cloud-week/targets/fascia-signs/TARGET.md and target.json | 8 October 2026 | the fascia target writer; project; taken n/a | YES: positions and the left-right rule |
| R4 | repository | production/research/asset-plan/4-SIGNAGE-AND-WEAR.md; production/research/ui-design/PERIOD-PRINT-AND-FONTS.md; production/research/street-clutter-1990/SUMMARY-2026-09-29.md; production/art/atlas-02/research/transport-timetables.md; production/research/shop-win | 8 October 2026 | earlier research helpers (they read period photographs and search summaries on the PC); project; taken n/a | YES, cited, not re-measured |
| L1 | search summaries (leads, never numbers) | WebSearch 8 Oct 2026: street name plate specs (South Kesteven https://www.southkesteven.gov.uk/sites/default/files/2023-09/STREET_NAME_PLATE_SPECIFICATIONv2.pdf; Charnwood; Fareham; Cotswold; Wigan), DfT circular 3/93 (west-norfolk.gov.uk copy), London street  | 8 October 2026: the pages themselves were NOT fetched (DNS or 403); only the search summaries were read | various; n/a; taken n/a | LEADS ONLY |

The licences of the previews: P1 is a crop of a CC0 panorama with the glazed interiors painted out; the layout sheets are our own drawings. No preview shows a business's name, a drink, a gambling mark or a person.
