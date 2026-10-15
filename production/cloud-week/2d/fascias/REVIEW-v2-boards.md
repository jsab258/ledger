FAIL

# Unit 4.1 fascia boards, try 2: the ten boards at street distance (fresh review)

Cloud week 42, 11 October 2026. One view: the ten 5410 x 550 mm boards (base colour, height, ORM, wear) seen across a 6 m road from 1.6 m, judged on the set in `scratchpad/f41/set/fascias/` reduced to 7 and 10 mm a pixel and at 1:1, the sheet `fascias-all-ten-v2-2026-10-09.jpg` and each board's preview. Not judged here: hanging signs, glass, small panels. The first try's reviews were not read.

Verdict in one line: the layouts, lettering craft, colours and the three plastic or glass fronts pass, but six painted boards and the three old-board rims are aged with one "distressed wood" filter. From across the road it reads as stock barn-wood texture, not 1990 shop paint, and it is the first thing a player sees on six of the ten boards. Faults 1 to 3 are one job in `fascia_age.py` and its settings. Each has an exact fix.

## Faults, worst first

### 1. Paint loss in long horizontal ribbons along the whole board (Mickey's, fish market, Rita's, chandler, ironmonger, empty unit; the cream rims of the laundry, tea rooms and newsagent)

- **What.** Measured on the height maps (the older coat at -0.30 mm and bare wood at -0.50 mm):
  - Loss touches 88 to 100 per cent of each board's length.
  - 54 to 81 per cent of the loss area lies in connected streaks 150 mm or longer, and 36 to 70 per cent in streaks 300 mm or longer.
  - The longest streaks are 0.65 to 1.5 m (Mickey's 851 mm, chandler 1525 mm, ironmonger 1297 mm).
  - Free-zone loss: fish 6.3 per cent (target 5), chandler 10.0 (target 7), ironmonger 8.8 (target 6), Mickey's 2.9, Rita's 2.5.
  - At 7 and 10 mm a pixel these chained flakes merge into pale bands that run the length of the board. Mickey's, the fish board and the chandler read as distressed weatherboarding. The empty unit (ribbons through its whole length) reads as reclaimed barn wood.
  - The cream old-board rims round the three box and panel signs carry the same streaks (5 to 10 per cent in their bottom 50 mm).
- **Mickey's board against the Hook sheet.** The sheet, approved for mood and palette, shows a clean slate board. Try 2 used the sheet to drop Mickey's ghost (A7) but kept 4 per cent streak loss and loss bands of 8 to 12 per cent in the bottom 100 mm.
- **What the photographs show instead.** At the same scale (comparison: `scratchpad/fascia-review2-boards/red/compare_photos_vs_boards_10mm.png`):
  - **Photograph A** is the worst case on a real street: a ship chandler's board in Hull's old harbour quarter, 1983, the shop closed and for sale. It ages by grime, not by flaking. It is darker and soiled under the cornice, with soft dark run-down stains and a faded ground. There is no ribbon of bare wood anywhere along its length.
  - **Photograph B** (Hull, 1989, a newsagent's) and **D** (Macclesfield, 1989) show working shops' boards. Each is an even painted field with a darker grime band under the cornice.
  - **C** (Dorchester, 1981) is clean gloss.
  - Where paint fails on a sheltered fascia it fails locally: at the foot (the drip edge), at the ends by the consoles and at joints.
- **Whose.** Both:
  - The target's: it takes the loss shape from P2, a weatherboard cladding texture rather than a fascia, and sets the loss amounts with no 1990 photograph.
  - The maker's: try 2 chains the flakes into "damp bands" across the full length, and puts more loss than the target on three boards.
  - The check missed it because it reads the median patch, which is dominated by thousands of specks, not the area-weighted length.
- **Exact fix** (`fascia_age.py` and each board's `age`; this changes the target's loss numbers, so DECISIONS gets one line):
  1. **Patch size.** No connected loss region longer than 80 mm along the board or taller than 25 mm. At least 30 mm of whole ground between patches in the same row (no chaining).
  2. **Placement.** At least 70 per cent of each board's loss lies in three places: the bottom 40 mm of the field, the first and last 200 mm of the board, and 25 mm either side of a board joint. Everywhere else on the board, at most 0.3 per cent loss.
  3. **Amount** (free zone): Mickey's 0.3 (the sheet's clean board), Rita's 0.5, fish market 1.5, ironmonger 2.0, chandler 3.0 (the quay). The three old-board rims carry 2.0, at the foot and ends only.
  4. **Empty unit.** Keep 17 per cent, but as four to eight lifted sheets of old paint 150 to 600 mm across with ragged edges, plus the foot, and no ribbons.
  5. **The ageing the photographs show, in its place.**
     - A grime film: base colour 8 to 12 L* darker in the top 80 mm under the cornice, fading linearly to nothing by 200 mm down.
     - Two to four soft dirt runs per board: 20 to 40 mm wide, 150 to 350 mm long, 3 to 5 L* darker, from the drip points on the top edge.
     - Sun fade on reds: the vermilion faces and shades lose 15 per cent of their chroma and gain 4 L*.
  6. **New check.** The loss-area-weighted horizontal extent must be at most 80 mm, and at most 10 per cent of the loss area may lie in components 150 mm or longer. Run it on every board.

### 2. Lettering left nearly whole on grounds that are flaking (chandler, fish market, ironmonger, Rita's)

- **What.** Loss inside the letters (closed letter shapes) against loss in a 4 to 60 mm ring round them:
  - chandler 0.46 against 5.5 per cent (ratio 0.08);
  - ironmonger 0.54 against 8.8 per cent (ratio 0.06);
  - fish market 1.06 against 10.4 per cent (ratio 0.10);
  - Rita's 0.75 against 3.9 per cent (ratio 0.19).
- **Where it shows.** On the chandler's left end a bare-wood streak runs straight under the "13" and through the rope border, and both stay unbroken over bare wood. At 7 mm this gives the "new transfer on an old board" look: crisp, full-strength names on grounds falling apart. The maker's own notes record this: the `neg.chandler.letters_pristine` control does not fail.
- **What the photographs show instead.** Photograph A: the 1983 chandler's letters have dulled and broken together with their ground. Paint on paint fails with the coat beneath it.
- **Whose.** The maker's.
- **Exact fix.**
  - Letters, their block shades, rules, the rope and the keylines take loss at 0.8 to 1.0 times the ground within 60 mm (gilt 0.5: leaf on size holds better).
  - A loss patch that meets a letter carries on through it, in the same older-coat and bare-wood colours, and the shade under it goes too.
  - Painted faces fade with their ground: chroma 10 per cent lower than fresh.
  - The `letters_pristine` control must then fail on every lettered painted board.
  - After fix 1, little loss reaches the letters, so this is mostly a consistency rule. The fade still applies.

### 3. Horizontal ripple banding in the painted grounds reads as brushed metal (fish market and ironmonger most; Mickey's, chandler, Rita's)

- **What.** On the painted boards the ground's lightness varies 6.7 to 9.4 L* (5 to 95 per cent, measured in 7 mm cells): Mickey's 7.6, fish 9.0, Rita's 6.7, chandler 8.1, ironmonger 9.4. The plastic, glass and acrylic faces vary 3.8. The variation is laid out as long wavy horizontal bands, like watered silk. At street distance the fish board's pale ground reads as brushed aluminium, and Mickey's slate as rippled water (it shows clearly in the overview sheet).
- **What the photographs show instead.** Photographs B, C and D: painted grounds read as even fields. The variation there is soft mottling and a grime gradient from the top, not grain-long bands.
- **Whose.** The maker's ("damp bands"; the target asks only for grain along the board at amplitude 3 L* on the bare empty unit).
- **Exact fix.**
  - Scale the band and grain modulation on painted grounds by about 0.4, so the ground's 5 to 95 per cent span at 7 mm is at most 3.5 L*.
  - Keep any remaining variation at periods of 300 mm or more along the board.
  - Let the vertical grime gradient of fix 1.5 carry the age.
  - The empty unit's bare timber keeps its grain.

## Narrow points (each small, each with an exact fix; none fails the view alone)

1. **Fish market ground colour.**
   - **What.** The aged ground (196,202,206) reads cold blue-grey at distance. Aged white enamel yellows; the 1989 Hull board (B) is warm off-white.
   - **Whose.** The target's.
   - **Fix.** Aged ground (203,199,186).
2. **Mickey's contact shadow.**
   - **What.** It is in the base colour, so the texture alone shows a soft dark MICKEY'S. In the engine it adds to the letters' own cast shadow, and it shows as a dark halo if the geometry is placed a few millimetres off.
   - **Fix.** Write it into the ORM red channel only (255 x (1 - 0.35 x shadow)) and leave the base colour clean.
3. **Pale rain runs on the dark boards** (Mickey's, chandler).
   - **What.** At 7 mm they read as soft light smudges, like light leaks.
   - **Fix.** On grounds under L* 40, make the runs dark grime (-4 L*), with a 2 mm pale tide line at the lower end only.
4. **Ironmonger's ghost.**
   - **What.** It is 10 mm bigger and 15 mm lower than the name, so at 1:1 it reads as a second grey shadow down and right of each letter, merged with the vermilion shade.
   - **Whose.** The target's placement.
   - **Fix.** Drop it, as A7 did for Mickey's, or move it to baseline 120 and cap 230 so its strokes stand clear above and below the name.
5. **Hairline cracks** (fish market, ironmonger).
   - **What.** Near-black random-direction lines read as pen scratches at 1:1. They are invisible at street distance.
   - **Fix.** Within 10 degrees of the board's length, coloured ground -10 L*, not near-black.
6. **The two lit box faces are spotless.** Box signs ten years old carry a dirt line inside the bottom of the face.
   - **Fix.** A soft band 30 to 50 mm high, 5 L* darker, along the inside bottom edge of each lit face; the laundry's white b* +3.
7. **Grocer's glass mottle.**
   - **What.** The green behind glass shows a cloudy, chalkboard-like mottle. Paint seen through glass reads as even and deep.
   - **Fix.** Cut the mottle to at most 1.5 L* (5 to 95 per cent).

## What is right

- **Ten distinct boards.** Every board is a different layout, ground, typeface and craft, set the right way round for each parade. No two dark boards stand side by side, and there is no stray or real word.
- **Lettering craft.** The solid 45-degree block shades, small hand jitter, end numerals and the shaded roman on buff read as signwriting at 7 and 10 mm. The typefaces are all period-plausible: condensed sans for the fishmonger, fat face and roman for the pawnbroker, Egyptian for the chandler, a 1930s geometric sans for the grocer, Franklin for the newsagent, a soft caff face for the tea rooms.
- **The photographs support:**
  - red sign-writing on a pale board (B, 1989);
  - gilt shaded capitals on a dark ground (C, 1981);
  - dark shaded capitals on a cream board in a port (A, 1983);
  - and, in B, the street number painted at the board's end (the target's D3).
- **Plastic, glass and acrylic fronts.** The steam laundry's and newsagent's lit box faces and the tea rooms' panel read as 1980s plastic; the grocer's green glass with chrome strip and speed lines reads as a 1930s glass fascia. These four pass at street distance apart from narrow points 6 and 7.
- **Rita's gilt** is metallic in the ORM (99 per cent of gilt pixels metal 255, roughness about 0.30), so the engine will light it as leaf, not mustard paint.
- **Height maps** stay within plus or minus 1.3 mm, with no letter geometry in Mickey's texture.

## Photographs used

All Geograph, CC BY-SA 2.0, the 640 px and 1024 px files, downloaded on 11 October 2026 to `scratchpad/fascia-review2-boards/photos/`. Business names on the boards are not repeated here; nothing in them shows drink, gambling or children. Rejected under the content rule: Redruth 1995 and Eastbourne 1986 (children), Portsmouth 1985 (public houses), Talgarth 1987 (a tonic-wine advert), Southsea 1984 (children).

| | Page | What | Taken | Licence |
|---|---|---|---|---|
| A | https://www.geograph.org.uk/photo/3378991 ("High Street, Kingston upon Hull", Bernard Sharp) | painted fascia of a ship chandler's and sail maker's, closed and for sale, Hull old harbour | 1983 (the page gives 1 January 1983, likely the year only) | CC BY-SA 2.0 |
| B | https://www.geograph.org.uk/photo/3801638 ("Charles Street, Kingston upon Hull", Bernard Sharp) | two painted boards of a newsagent's, red lettering on off-white, street numbers at the ends | 9 February 1989 | CC BY-SA 2.0 |
| C | https://www.geograph.org.uk/photo/3418400 ("Corn merchant's shop", Richard Green) | corner shop in Dorchester, dark green boards with shaded gilt lettering | 28 March 1981 | CC BY-SA 2.0 |
| D | https://www.geograph.org.uk/photo/2818265 ("Shops on Buxton Road", darren kimpton) | second-hand furniture shop, Macclesfield, painted cream board with red lettering | 4 April 1989 | CC BY-SA 2.0 |

The measures are reproducible with the reviewer's scripts in `scratchpad/rev2tools/` (`loss.py`, `loss2.py`, `letterloss.py`, `ground.py`, `reduce.py`). The reductions are in `scratchpad/fascia-review2-boards/red/` (`sheet_7mm.png`, `sheet_10mm.png`, `sheet7_x2_A.png` and `_B.png`, the 1:1 crops, and the comparison picture).
