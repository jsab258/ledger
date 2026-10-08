FAIL

# Fascia signs of Quay Street: target review

Cloud week 42, 8 October 2026, by a fresh reviewer who did not write the target and will not build it. **13 faults**, worst first, then notes, then what is right. Nothing in the target was edited. Nothing was committed.

## How it was tested

- I read REVIEW-BRIEF.md, BRIEF.md, canon.md, RULINGS.md, the whole of TARGET.md and target.json, and the earlier notes the target cites: asset-plan/4-SIGNAGE-AND-WEAR.md, ui-design/PERIOD-PRINT-AND-FONTS.md, shopfronts/FRONTAGE-2026-10-06.md, street-wear/PAINTED-FRONTS-2026-10-07.md, shop-window-interiors/FISHMONGER-2026-10-03.md, reference/photographs.md and the shopfront kit README. I also read the recipe's fascia code (tools/art-recipes/terrace-front.py lines 837 to 892, 2127 to 2180, 5650 to 5700 and 8272).
- I ran `self_check.py --fetch-fonts <scratch>/fonts --no-write`: 158 of 158 pass, 4 reported, the same as the writer's run. target.json's checksum was the same before and after. I ran `target_drawing.py` into scratch: 10 boards and 4 projecting signs.
- I rendered every board from target.json with the real OFL font files (each block's origin, baseline, size, tracking, axes, face, shade and the shapes). I then reduced the renders to the game's pixel sizes across the road: 9.5 m away, 1440 rows, a 46-degree and a 60-degree vertical field, and a 67 per cent internal resolution scaled back up. All of this is in scratch only.
- I checked that every glyph each board needs (’ and · included) is in its font file. All of them are.
- I re-read every OFL.txt at raw.githubusercontent.com and checked P1 to P3 on Poly Haven's API and licence page. I downloaded P1's tone-mapped panorama and re-rendered the board at its native resolution.
- I compared the target with the game: shop-fronts-whole-2026-10-08.jpg, morning-hook-day-2026-10-08.jpg, the two proof-2.6 frames of 4 October and the Hook sheet.

**Where the network limited me.** commons.wikimedia.org, geograph.org.uk, flickr.com, archive.org, picturesheffield.com and flashbak.com refused every connection today. So I could not open t13138, t13140 or Peter Marshall's Hull set. The target's 1990 claims rest on those, through the earlier notes, so I judged them only against those notes and could not judge them against the photographs. polyhaven.com and raw.githubusercontent.com were reached.

## Faults, worst first

### 1. The board's x axis is backwards for the game. MICKEY’S lands over the window, not over the door.

- **Where.** target.json `units.board` and TARGET.md section 3 ("east shops: low street x at the left; west shops: low street x at the right"). Mickey's `x_mm` 1355. The self_check D6 line, which works out `(4.65 - 3.295) * 1000`.
- **What the game shows.** shop-fronts-whole-2026-10-08.jpg, read left to right, shows TO LET (x 21 to 27), PAWNBROKER (15 to 21), FRESH FISH (9 to 15), then MICKEY'S (3 to 9) at the right-hand end. So a viewer facing the east parade has low street x on the **right**.
  - The same picture shows Mickey's glazed shop door on the right of the window, with the side door beyond it. morning-hook-day-2026-10-08.jpg shows the same.
  - vignette-scene.json `cam_mickeys` puts the window at x 5.12 to 8.61, and DECISIONS 7 and 8 October put the door at x 4.65.
  - The recipe's docstring (terrace-front.py about line 2132: "a viewer looking at an east face has +x on their right hand") describes the frame before `_export_street`, which "exports the street's geometry, mirrored". The target used the frame before the mirror.
- **The result.** Board x 1355 is street x 8.705 − 1.355 = 7.35. That is over the up-street half of the window, 2.7 m from the door. The target says this place is "over the door, as the Hook sheet puts it", and it is not. D6 has the same reversal coded in, so the check passes the fault.
- **The west side is reversed too.** In the game a viewer facing the west block has low x on the left.
- **The hanging signs.** "Left pilaster" and "right pilaster" in `projecting_signs` now point at the wrong side. The ironmonger's and the chandler's signs have no street x at all, so a script cannot place them.
- **Amendment.**
  - Set `units.board` to: "x from the board's left as a viewer facing it sees it, in the game (after the export's mirror): east shops low street x on the viewer's RIGHT; west shops low street x on the viewer's LEFT."
  - Set Mickey's name `x_mm` to **4055** (= 3.0 + 6.0 − 0.295 − 4.65, in mm). Its ink box becomes [3171.7, 130.8, 4938.3, 417.6]. The note becomes "over the door, board x = (bay end − 0.295 − door x)".
  - D6 should read the door's x from hook-cast.json (`body_x_m` of Mickey's door place) or from the scene, not from a typed 4.65. It must test the corrected mapping.
  - Keep V4, the centred variant.
  - Give every projecting sign `x_street_m`, and say its side in viewer words under the corrected rule.
    - Rita's balls at 15.175 are on the viewer's **right** pilaster, at the window end beside the fish shop. Her doors are at the other end, about x 19.4 to 20.6. Say which end is meant. I recommend her door end, x 20.825 (Judgement).
    - The laundry box at 27.175 is on the viewer's right.
    - Add x for the ironmonger and the chandler.

### 2. The target does not say which parts are texture and which are geometry, and the height map cannot hold its own reliefs.

- **Mickey's letters.**
  - What exists today: the recipe already builds MICKEY’S as raised gilt geometry over a board picture with no letters (terrace-front.py line 857 `RAISED_LETTERS`: cap 0.24 m, 12 mm off the board, laid across the whole sign piece).
  - What the target asks: target.json puts MICKEY’S into the texture as a text block (`technique` applied, `relief_mm` 14). Check G9 then wants a height step of 8 to 18 mm across the applied letters' edges. But `textures.height` encodes 128 as the board face and 1 mm over 127 steps, which is ±1 mm at most. The box sign's "+3 mm" frame does not fit either.
  - The result: a script will either paint flat gilt letters under the recipe's raised ones (two sets of letters, out of line, because the recipe centres its letters) or fail G9.
- **The box sign's depth is missing.** The laundry's box sign has no depth, no return colour and no fixing to the board. Its returns are what make it read as a box from the hook camera and along the pavement. As a flat picture on the 0.12 m board it reads as paint.
- **Amendment.** Add a `geometry` section to target.json.
  - (a) Mickey's. The texture carries the ground, the ghost, the ten pin holes and a soft contact shadow under where the letters stand, and no letter face. The letters stay the recipe's `RAISED_LETTERS`, changed to: cap 0.270 m; centre at board x 4055 (fault 1); stand-off 0.014 m; emboldened 3 mm; face `brass_gilt`; flanks `brass_side`. G9's applied entry moves to a geometry check: letter depth 14 ± 2 mm, and the bounding box centred over the door ± 50 mm.
  - (b) The steam laundry box. A box 5200 x 480 mm, 150 mm deep (Judgement), screwed to the board face, with bronze returns (84,68,53) and the face texture on its front. Delete the "+3 mm" frame from the height map.
  - (c) The grocer's chrome edge strip and speed lines. Raised metal: 3 mm proud as geometry, or height +0.8 mm within the map's range. Say which.

### 3. The checks would not catch the faults that matter from the street.

The 165 checks cover only cap, width, safe-zone fit, contrast, face colour, shade, ground, border, paint loss, the emissive face and the unlit board. They miss these:

- **No check reads where a block is.** A name at the wrong end (fault 1), a trade line above its name, or a block 1 m off centre all pass. "fit" only tests the safe rectangle.
- **A mirrored texture passes every check.** The recipe has already made this fault once: "MICKEY'S painted backwards", terrace-front.py about line 2136. Words, cap and width are read from the renderer's own manifest, so a wrong font, a fallback glyph or a mirrored picture is never compared with the pixels.
- **Nothing outside the ten boards is checked.** There are no checks for the four projecting signs, the 24 glass rows, the letting board or the hours plates.
- **Nothing checks the ghosts, the hand jitter, the rain runs, the gull marks or the rust.** Section 2 item 5 names their absence as today's fault.
- **G9 cannot pass as written** (fault 2).

**Amendment.** Add these checks:

- Per block `pos`: the ink box's centre (anchor centre) or left edge (anchor left) within ± 15 mm of target, and the baseline within ± 3 mm. Read them on the pixels, from the face-colour mask, not from the manifest.
- G10 `mask`: re-render each manifest block from its font file and compare it with the drawn face mask. Pass at IoU ≥ 0.85. This catches mirroring, a wrong font, a wrong word and a wrong place.
- Per projecting sign: mount street x ± 0.02 m, arm height ± 0.02 m, projection ± 0.02 m, lowest point ≥ 2.5 m, and both faces reading left to right.
- Per glass row: the string is in `approved_words`, the cap within ± 5 per cent, z within ± 0.03 m.
- Per ghost: present, 3 to 5 dE from the ground, and no legible string other than its named text (fault 4).
- Hand jitter: on painted and gilded blocks the SD of the baseline residual is 0.6 to 1.6 mm. On vinyl, applied and glass blocks it is 0 to 0.3 mm.
- Wear: run, gull and rust counts within ± 1 of each shop's `age`.
- G9: move its applied entry to the geometry check.

### 4. The ghosts cannot be built from target.json, and a script that builds them would have to invent words.

- **Where.** `shops[].ghost`.
  - Mickey's is `repaint_patch`, with no text, while its note says "a ghost of an older, centred MICKEY’S".
  - fish_market and ironmonger are `faint_older_lettering` and give a box and a dE, but no words, font or size.
- **Why it matters.** "Older lettering" needs words. A former proprietor's name would be an invented name, which canon and RULINGS 3 Oct forbid. G4 reads only the manifest, so invented ghost words would not be caught.
- **Amendment.** Give every ghost a text block with `role: "ghost"`, add its string to `approved_words`, and put it in the manifest.
  - **Mickey's.** MICKEY’S in Marcellus SC, not emboldened, cap 245 mm, centred at x 2705, baseline 150, colour the ground +3.5 dE towards blue, a brush-cut edge with a 1 mm ridge, and ten pin holes along the old cap line.
  - **fish_market.** FISHMONGER in Old Standard TT Bold, cap 200 mm, centred at x 2705, baseline 160, at 4 dE, 60 per cent broken by the overpaint.
  - **ironmonger.** IRONMONGER in Old Standard TT Bold, cap 190, centred, baseline 170, at 4 dE, 60 per cent broken.
  - Or state "no glyphs: brush texture only" for any of them.

### 5. The ten boards keep the one-designer recipe the target itself names as today's first fault.

- **The layout.** TARGET.md section 2 item 1 says "every trade board is the same recipe: a name ... centred, one trade line ... under it". In target.json, 8 of the 9 lettered boards are exactly that: a centred name over a centred, wide-tracked trade line (tracking +0.14 to +0.30 em).
- **The wording.** 7 of the 8 trade lines are the same "A · B · C" middle-dot list. The fonts and colours vary, but the skeleton does not, and from across the road the skeleton is what you see. My render of target.json with the real fonts shows it board after board.
- **Amendment.**
  - Change four trade lines away from the dotted list. Each new string goes into `approved_words`:
    - steam_laundry: "SERVICE WASHES & DRY CLEANING"
    - grocer: "HIGH CLASS PROVISIONS"
    - newsagent: "TOBACCONIST & CONFECTIONER"
    - tea_rooms: "BREAKFASTS, LUNCHES & TEAS", which also fits the cast's café, open 6.30 to 22.00.
  - Break the stack on two boards:
    - **newsagent.** Name only on the fascia (Libre Franklin 900, cap 260, tracking +0.08). Its trade line moves to the door glass in white vinyl, cap 60.
    - **ironmonger.** The trade words go in its two end panels in place of the proposed 16s and the line under the name: "TOOLS &" over "HARDWARE" centred at x 600, and "PAINTS &" over "PARAFFIN" centred at x 4810. Baselines 270 and 190, Libre Baskerville 700, cap 56, black with a 5.6 mm vermilion shade. The name's baseline drops to 185, centred alone in the panel. The 16 moves to the fanlight only.
  - Trade-line tracking: at most +0.12 em on at least four boards.
  - Add check G11: no more than five boards share the centred name-over-trade skeleton, and no more than three trade lines use " · ".

### 6. The period mix leans to heritage, against the notes the target cites.

- **The mix.** One front in ten is the 1980s plastic generation (the laundry's box), plus one cut-vinyl board. Six are traditional painted or gilded boards, five of them with keylines or borders and three with numerals at both ends.
- **What the cited notes say.**
  - Note 4 (A1, 1): "by the 1980s the backlit Perspex sign was increasingly replacing the old fascias".
  - PERIOD-PRINT section 4: a 1990 provincial street "mixes old hand-signwritten fascias, plastic light-box signs and new cut-vinyl lettering".
  - photographs.md R05 and R09 (Hull, 1989): "metal shopfront, fluorescent strips", "METAL SHOPFRONTS".
- **The tea room in particular.** Its duck-egg blue-green ground with a painted scalloped valance has no source. It reads as a 2010s heritage café, the opposite of the cast's "the caff", which opens at 6.30 (hook-cast.json `cafe`).
- **Amendment.** Make the tea room the second 1980s front.
  - A flat, unlit acrylic panel screwed over the board: outer [90, 40, 5320, 510], a 25 mm white-painted timber frame, and a brown face. Fresh brown (132,82,50), 1990 brown (120,74,44), roughness 0.35.
  - The Fraunces lines as cut vinyl in cream (235,227,201). Contrast 5.8; the smallest dE to any other board is 21.1, against the empty unit.
  - Delete the duck-egg ground and the scallops (see fault 8). Construction kind becomes `flat_panel`.

### 7. The two nearest boards in the hook frame are the street's closest pair, where the sheet has a white board.

- **The numbers.** Mickey's slate (62,75,87) and the fish board's charcoal navy (40,42,49) are dE 14.9 apart, the minimum on the street. Both are dark blue-grey, side by side at bays 0 and 1, the nearest boards to the hook camera.
- **What the sheet shows.** The Hook sheet puts a white fascia beside Mickey's. The target measured it at (204,204,204) and lists it as "not used".
- **Why the photograph does not settle it.** D1 overrides the sheet with t13138. That is a different shop, and it shows a dark board with red lettering existed in 1990. It does not disagree with the sheet about this board. The sheet governs palette and composition (RULINGS 21 Sep).
- **Amendment.** Keep the photographed red sign-writing and put it on the sheet's light board:
  - Ground fresh (236,238,236), 1990 (196,202,206).
  - Vermilion letters with a **black** block shade (37,35,34), 29 mm, in place of the cream shade.
  - The vermilion rules stay.
  - Contrast 2.85 (the floor is 2.2). The smallest dE is 14.8, to the laundry, so G7 still holds.
  - Change D1's wording to "red sign-writing (t13138), on the sheet's white board".

### 8. The tea room's "scalloped valance" builds as a row of dots.

- **Where.** target.json `tea_rooms.shapes`: 66 full circles of radius 26 mm, centred at y 50, under a rule at y 86 to 92. The circles' tops are at y 76, so a 10 mm gap separates them from the rule. A script draws polka dots. The writer's own L1 layout sheet and my render both show dots.
- **Amendment.** If fault 6 is not taken: make each scallop a half-disc hanging from the rule. Circle centres at y 86, clipped below y 86, radius 26, pitch 52 so neighbours touch, filled deep teal and joined to the rule. If fault 6 is taken, delete them.

### 9. The projecting signs are mounted where the kit has no pilaster shaft.

- **Where.** Every arm is above the pilaster's top: the capital is at 2.85 m, the consoles stand from about 2.73 to 3.47 m, and the cornice sits on the fascia's top at 3.40 m.
  - Rita's arm is at 3.28 m, "face of the shaft".
  - The laundry box's arm is at 2.95 m, the ironmonger's at 3.05 m, the chandler's at 3.10 m.
- **Why it matters.** Each 0.18 x 0.30 m plate would be bolted onto a scrolled console or across the cornice line. In the bays still built as 6 m boxes, it would be bolted onto the fascia sign itself. Mounting on the shaft below 2.85 m would bring Rita's balls down to about 2.1 m, which fails the target's own 2.5 m clearance.
- **A wrong number.** The laundry box's declared `clearance_below_m` is 2.7. Its own numbers give 2.95 − 0.45 = 2.50.
- **Amendment.**
  - Mount every bracket on the brick above the cornice. Plate foot at 3.60 m, plate centre on the party-wall pier at the street x of fault 1. Arm at 3.75 m.
  - Keep the hanging signs' lowest points where they are now by lengthening their drops: Rita's hanger becomes 0.57 m (from 0.10), the ironmonger's rings become chains 0.70 m longer, and the chandler's chains 0.65 m longer.
  - Fix the laundry box by its back edge to the brick above the cornice, at 3.60 to 4.05 m, as fascia-level box signs were fixed (Judgement). Its lowest point is then 3.60 m.
  - Correct `clearance_below_m` to the computed values.

### 10. The grocer's glass fascia: no joints, the crack contradicts the cited note, and the method contradicts itself.

- **No joints.** The target specifies one glass slab 5330 x 500 mm. Structural glass came in jointed sheets. That is Judgement, from memory; no source was reached today.
- **The crack.** The target cites FRONTAGE-2026-10-06 for the method, and that note says "Vitrolite cracks low down and round doors, patched with painted ply or Perspex". The target then puts a crazed crack across the fascia's right third, 2.9 m up.
- **The method.** The target calls the panel Vitrolite, which is glass coloured right through and opaque, then specifies "back-painted" cream letters seen through it. Back-painted letters need clear glass.
- **Amendment.**
  - Three slabs, with joints at x 1380 and 4030. The name's ink, 1403.8 to 4006.2, sits inside the middle slab. Joints are 3 mm of dark mastic (30,30,28), and each slab edge has a 2 mm polished bevel.
  - Move the crack off the fascia (it belongs to the stallriser, which is not this family). If one is kept, make it a single straight crack running 300 mm from a fixing at a slab corner, with no crazing. The patch becomes "painted ply or Perspex", as the note says.
  - State the method: either black Vitrolite with applied chrome letters (geometry 6 mm proud, colour (178,181,183)), or a back-painted clear glass sign, dropping the word Vitrolite. I recommend the first; it is Judgement.

### 11. The baked frame puts a light line along the top of all ten boards, right under the cornice.

- **Where.** board.frame_note and check G2 bake a highlight 3 to 14 L* lighter along the top 24 mm, and a shade along the bottom, into the base colour.
- **Why it is wrong.**
  - Under a projecting cornice, the top of a fascia is in the cornice's shadow, both in the street and in Unreal. The target itself leaves "the cornice's shadow" to Unreal.
  - At night a street lamp lights the board from below, so a baked top highlight is wrong then too.
  - The same strip on every board is one designer again, and the kit's fascia has no such frame.
- **Amendment.** Delete the baked highlight and shade from the base colour. Where a board would have a planted moulding (Rita's, the ironmonger, the chandler), put a 24 mm moulding in the height map at +0.6 mm with a 4 mm chamfer. None on vinyl, box or glass. G2 reads the height map.

### 12. The box sign's dead tube is the wrong shape.

- **Where.** steam_laundry: "one tube dead (a band 500 to 700 mm wide, 15 per cent darker)" across the face's full height.
- **Why it is wrong.** The tubes are given as two rows along the box. A dead tube therefore darkens one row over one tube's length. It does not darken a narrow full-height band.
- **Amendment.**
  - Dead tube: upper row, x 3300 to 4800 (a 1500 mm tube; Judgement). Emissive there falls to 60 per cent of the face's, because the lower row still lights it.
  - Tube-end shadows: 60 mm wide and 10 per cent dimmer, every 1500 mm in both rows.
  - Update the `steam_laundry.emissive` check to match.

### 13. A reference preview shows drink.

- **Where.** P1-leadenhall-chamberlain-front-scale.jpg shows "COCKTAIL BAR", "Bar" opening times and "RESTAURANT", plus a real brand in a reflection, in a picture stored in production/previews.
- **The rule.** The content rule: alcohol "never shown ... in image".
- **Amendment.**
  - Re-cut that preview to the fascia and the door leaf's top and bottom lines, or blur all window and door lettering below row 640 of the preview.
  - Rename the P1 files without the business's name, for example `P1-leadenhall-no23-…`, and update TARGET.md and target.json to match.

## Notes (narrow points; they do not block a pass on their own)

1. **Mickey's size against the sheet.** The cap is 0.49 of the board against the sheet's 0.69. Marcellus SC need not be squeezed to come closer. Cap 330 mm with baseline 100 gives 0.60 of the board and about 2160 mm of width, inside the safe zone at the door-centred x (ink about 2975 to 5135).
2. **Legibility.**
   - Name lines (170 to 290 mm) read well across the road: 30 to 52 px at a 46-degree field, 22 to 38 px at 60 degrees.
   - The 52 to 62 mm trade lines in light weights (Fraunces 600, Oswald 400) come out at about 7 to 8 px at a 60-degree field, and about 5 px at a 67 per cent internal resolution. In my reduction they were barely readable.
   - The game's trade lines today are 70 mm. I recommend at least 70 mm, and Oswald at least 500.
   - Section 12 item 7 ("names readable to 40 to 66 m") leaves out the angle. From the hook camera, the boards beyond Rita's are seen at under about 15 degrees and are unreadable at any size. That matches the sheet, but the claim should go.
3. **Numerals at both ends.** P1 is Leadenhall Market, where the fronts carry their market unit number at both ends as one livery ("23 … 23"). That alone does not make it provincial practice. Keep end numbers on at most two boards.
4. **MINICABS · 24 HOURS.** This existing glass line (shop-room.py) contradicts the cast's hours for Mickey's: 7.00 to 3.00, shut 3 to 7. The target adds it to `approved_words`. Hand it to the town and the builder rather than approving it.
5. **D5 is not a real disagreement.** The cited FRONTAGE note read the guides at source: "not more than 600 mm" [CV] and "at most a fifth" [RI]. The 380 mm figure is a search summary. Cite FRONTAGE.
6. **The ironmonger's font.** PERIOD-PRINT rates Libre Baskerville low to medium ("book serifs … ATF (American)"), and it is not in note 4's signwriting list. Consider Libre Caslon Display.
7. **A reserved name.** Josefin Sans's OFL.txt reserves "Josefin Sans", not "Josefin" as target.json says.
8. **The empty unit's colour.** The street draws the empty unit's board near black (recipe `bare_timber`, linear 0.021,0.014,0.010). The target lightens it to (98,85,72). DECISIONS 3 Oct keeps the unit "as the street already draws it". Confirm before changing.
9. **The laundry's old board.** The old board showing round the box (cream, painted timber, with paint loss) is not a separate shape in target.json. A script will paint it acrylic white. Add `old_board` [0, 0, 5410, 550], cream, with timber wear, under the box.
10. **The ironmonger's rust.** The rust "under the hanging-sign bracket bolts" lands on brick or pilaster, not on this texture.
11. **Hours plates.** Their words are not in `approved_words`, so G4 fails them if they share the manifest. Give them their own rule.
12. **Texture size.** 5410 x 550 is not a power of two. From memory, and not checked in the 5.8.2 source as RULINGS 8 Oct requires: Unreal gives such textures no mips unless padded, and the letters would shimmer from the hook camera. Check this, and pad if needed.
13. **P1's gilt edge.** P1's gilt shows a slightly paler rim along the face's edge, about 1 view pixel, where the target specifies a darker "matt edge". At P1's resolution I cannot tell an outline from the tone-map's halo. Leave it open.
14. **Ten boards or twelve.** RULINGS 2 Oct counts twelve shopfronts and the scene has ten shop bays. The target was right to make ten and name the gap. Hal's shop (cast x 39) is the town's question.

## What is right

- **Words.** Every string is a trade description or a minted name:
  - MICKEY’S: canon.
  - RITA’S: the cast.
  - FISH MARKET and STEAM LAUNDRY: DECISIONS 3 Oct.
  - No proprietor is invented.
  - Nothing of drink, gambling or children: the newsagent has no pools, the grocer no off-licence, the chandler no bonded stores. Nothing after 1992.
  - The word list is checked against RealWorld.cs and the real names on P1.
- **Fonts.** All ten are OFL 1.1. I read each OFL.txt whole today. Every glyph needed is present. Overpass, Apache and GPL faces are excluded. Marcellus SC is used for Mickey's, as ruled.
- **Honesty about sources.**
  - The 1990 evidence is said plainly to be earlier notes. D1 follows FISHMONGER-2026-10-03 line 43 faithfully.
  - Everything else is marked Judgement. Unreached sites are listed and not used.
  - P1's restoration date and P2 and P3 being cladding are stated.
  - P1 to P3's authors, CC0 licence and dates are confirmed on Poly Haven today.
  - P1's block shade (down and right, about 0.10 of the cap) and its concave keyline corners hold on my native-resolution re-render. The code re-measure agrees within 2 px.
- **The board numbers.** The band at 2.85 to 3.40, 0.12 proud, and the board between the consoles at 0.295 to 5.705 all match their sources. V6 covers the street's 6 m box.
- **Mickey's colours.** Slate (62,75,87) and gilt (167,149,109) are the sheet's.
- **Rita's board** is unlit, per DECISIONS 1 Oct.
- **The wear model.** Its shape is measured, its amount is honest Judgement, and the classes are sensible.
- **Variety of fonts, grounds and constructions** is real and checked pairwise.
- **The self-check** re-reads its printed sources. It reports its departures from the sheet and from P1 openly instead of hiding them.
