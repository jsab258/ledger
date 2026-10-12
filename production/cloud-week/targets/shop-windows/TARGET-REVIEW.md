FAIL

# Shop windows target: fresh review (cloud week 42, unit 7, 12 October 2026)

Reviewer: a fresh target reviewer who did not write the target and will not build it. I read REVIEW-BRIEF.md, unit 7 in QUEUE.md (part 2) and the task as given, commit 2f475f5's message, TARGET.md (summary, sections 0 to 4 and 6 to 12 in full, and section 5 sampled), target.json (Rita's entry in full; every shop's front, glazing, door, lights and spec entry), the 2.2 target (`parts.shop_door`, `parts.side_door_slot`), the 3.2 kit's NOTES.md and street review, the 4.1 notes on the whitewash, shop-room.py (the pawnbroker), `trace` in make_interior_material.py, production/specs/shop-interiors.json, unreal-look.json, the approved Rita previews (rita-day-kit and rita-night-kit, 6 October) and the approved pawnbroker_day.png.

**Three faults.** The worst shows on every front from the street. Above both doors, between the transom line (2400) and the fascia (2850), target.json has nothing, and the target's own drawings show a hole there. Second, Rita's room places a model that carries a real British retailer's name ("Dixons"). Third, a committed preview shows a real firm's name, although the target says every one is masked. Rita's room, the method and the stand-off rules otherwise hold up. The rest is fifteen narrow points with exact fixes. The most visible of them is the toplights: the same unaligned layout the 3.2 street review already failed, back on five fronts.

## How this was checked

- **Scripts.** `self_check.py` gives 267 pass, 0 fail, 3 reported offline and 269 pass with `--live`, as stated. `target_drawing.py` drew all ten fronts, eight plans, rooms and pictures into scratch.
  - Note for the writer: `self_check.py` writes its results back into target.json, and the order of tied rows changes from run to run. My live run changed two `detail` lines. I restored target.json from git (`git checkout`), so the target is as committed. See narrow point 13.
- **The game's rule, re-derived independently.** I wrote my own slide measure in scratch. It imports `trace` and does not use sw_common:
  - A room point is painted where the render camera's ray through it meets the box.
  - For each eye, I solve on the card for the point whose `trace` returns that picture (u, v).
  - The slide is the angle from the eye between the true point and the painted one, in pixels of 2560 x 1440 (f = 720 / tan(vfov/2)). I used Rita's own eyes.
- **Photographs.** I opened the Geograph pages of P1, P4 and P6 (title, author, date taken, CC BY-SA 2.0 all as stated). I looked at every preview and re-read D1's door numbers from the pixel table in section 8.
- **Poly Haven.** I read `api.polyhaven.com/assets?t=models` today: 521 models.
  - I checked all 104 inventory ids, not a sample of 15. All exist, every model placed in any shop is in the inventory, and no denied id is placed.
  - All 17 surface textures exist (`?t=textures`, 868).
  - Poly Haven's licence page (polyhaven.com/license) states that every asset is CC0.
  - I looked at the thumbnails of about 45 models at 384 to 1200 px: 23 of Rita's, plus every model whose description mentions labels, print, decals, stickers or stamps.

## Faults, worst first

### 1. Nothing above the doors: a 1.95 m x 0.45 m hole under the fascia on every front

- **Where:**
  - In D1 (`D1-ritas-front.jpg`), the whole band from u 350 to 2300, z 2400 to 2850 is blank: above the side door and above the shop door's fanlight.
  - D2 (`D2-ten-fronts-sheet.jpg`) shows the same blank band over the doors of all ten fronts.
  - The approved game front (`production/previews/rita-day-kit-2026-10-06.jpg`) shows what belongs there:
    - the transom carried across both doors;
    - three toplights (two bars) over the shop door;
    - a white raised-and-fielded panel over the side door;
    - the head under the fascia.
- **Why it is the target's:**
  - The 3.2 kit left the door slots empty on purpose (kit NOTES.md: "no head, no transom over them: the target puts the transom, a fielded panel and the head over the doors in the door family's work").
  - This target takes the doors on (4.1: "except the doors, the lobby and the side door's trim, which are this target's").
  - target.json's `door` and `front` hold no fanlight, no over-door transom, no toplights over the door, no panel over the side door and no head across the door slots. Only target_drawing.py hard-codes a fanlight (2131 to 2400).
  - FRN-01 checks "transom 2400 to 2480, head 2790 to 2850" against the kit, which builds them over the window only. FRN-03 checks the leaf. No check looks at what stands above the leaf.
  - A builder working from target.json, or from the drawing it makes, leaves the hole.
- **Amendment:** in each shop's `door`, add the following, copied from 2.2 (`targets/shopfronts/target.json` `parts.shop_door.dims` and `parts.side_door_slot.dims.above`; TARGET.md 2.2 lines 368 and 387), with numbers resolved per shop from `front.zones_u_mm`. Rita's are given here (2.2 bay frame, mm above the footway):
  - `fanlight`: z 2131 to 2400, one 6 mm pane in an ovolo bead, between the shop door frame's jambs (u 1344 to 2250). 4.1's fanlight street number ("5") goes on it. 4.1 gives it at "z 2.18"; say which frame that is, because 2.18 above the crown is 2080 above the footway, which is below this fanlight.
  - `transom`: `transom_t1`, z 2400 to 2480, running across both door slots from u 350 to 2300 and meeting the window frame's left jamb.
  - `toplights_over_shop_door`: z 2480 to 2790, three panes of 283.3 between the door frame's jambs (u 1344 to 2250). Two 28 wide `toplight_bar_plan` bars at u 1641.3 and 1952.7; glass and beads as the window's toplights.
  - `panel_over_side_door`: one raised-and-fielded panel 844 wide (944 − 2 x 50), z 2480 to 2790, with 2.2's `raised_field_edge`, painted white joinery (226, 224, 214) as on the approved front.
  - `head`: the window's `head_section` (95 x 60), z 2790 to 2850, from u 350 to 2300.
  - The other nine fronts: the same, mirrored where the door end is the viewer's right. Metal fronts (M1, M2) take their own variant's transom section (`transom_m1`) and 2.2's numbers for their doors' tops.
  - Draw all of these in target_drawing.py.
  - Add a check **FRN-07, no opening in the front:** on the elevation drawn from target.json, every point between the pilasters' inner edges from z 0 to 2850 lies on a part (stallriser, sill, frame, glass, door, fanlight, transom, toplight, panel, head). The largest uncovered rectangle is at most 5 x 5 mm. It applies to all 10 shops.

### 2. A real firm's name in Rita's room: `cassette_player` reads "Dixons TR12 Cassette Recorder"

- **Where:**
  - The Poly Haven thumbnail of `cassette_player` (1200 px, read today) shows, above the cassette window, a red roundel, then **"Dixons"**, then "TR12 Cassette Recorder". Dixons was the British high-street electrical retailer of 1990.
  - Rita's room places three on `R-back-stock` (TARGET.md 4.4), and nothing is blanked on them.
  - It is not in the target's list of marks seen (section 11), not in the denied list, and 'dixons' is not in `brand_blocklist`.
  - INV-05's scripted half searches manifest text and so cannot see it. On the 4096 picture the back wall is drawn at about 418 px a metre, so the lettering is about 8 px high: readable on the texture itself.
  - The same model is in the approved recipe's stock pool (shop-room.py, `pool`), so the approved `pawnbroker_*.png` may carry it already. At 2048 wide it is about 4 px high.
- **Amendment:**
  - `inventory.polyhaven.cassette_player`: add `"marks": "red roundel, 'Dixons' and 'TR12 Cassette Recorder' above the cassette window: painted out of the base-colour map to the case's brushed grey; the tape's handwritten label kept"`.
  - Rita's goods row `cassette_player`: note "maker's name painted out".
  - Add `dixons` (and, for the same reason, `currys`, `comet`, `rumbelows`) to `brand_blocklist`.
  - Add a line to INV-05: "the approved pawnbroker pictures are searched by eye at full size for the same mark".
  - Better still, do the 1k look at every one of the 104 models before the build rather than at the gate. Thumbnails alone missed this one.

### 3. A real firm's name in a committed preview (P6), and P1's door number

- **Where:**
  - `P6-kames-unlet-shop-1995.jpg` shows the fascia lettering "GROCER ... FERGUSON ... DRAPER". The Geograph page's own title is "Ferguson the grocer and draper in Kames".
  - The neighbouring shop's board ("... Crafts") is also partly legible.
  - `P1-worcester-fish-front-below-fascia.jpg` and its overlay show the door's number plate "384".
  - Section 2 says that every real firm's name and number is "cropped away or masked grey".
- **Amendment:**
  - Re-crop P6 below the fascia (only the glass, door and pier are used: "for the empty unit's glass"), or mask the fascia band and the neighbour's board grey.
  - Mask P1's number plate (pixel table row y 338) grey in both P1 previews.
  - Re-run make_previews.py.

## Narrow points (each with its exact fix, for the writer or the builder)

### 1. Toplights: the 3.2 street review's fault is back on five fronts, and Rita's data contradicts itself

- **The fault:**
  - `shops[ritas].front.glazing` says `3L-8T`, 8 toplights, unaligned. `glazing_layout.toplight_bar_centres` lists the seven bars the 3.2 street review failed (REVIEW-v1-street.md, fault 1; kit departure D6).
  - Meanwhile TARGET.md 4.1, `toplights_as_built` (9) and FRN-04 say nine.
  - D1 draws the result: sliver panes of 94.5 mm beside each mullion.
  - The same pattern is set for:
    - the newsagent (T1, slivers 94.5 mm);
    - the empty unit (T2, 91.2 mm);
    - the ironmonger (T2, two 273.8 mm half-panes on the mullion);
    - the grocer (M2, 256.4 mm panes beside both mullions).
  - FRN-04 counts toplights and so passes all of them.
- **Fix:** D6's rule on every front: each mullion carried up through the toplight row as a bar of its own width, and each light's toplight split equally by 28 bars. Bar centres from the frame's left (mm):
  - Rita's and the newsagent (T1): pattern `3L-9T`, 9 toplights of 326.9, bars 390.9, 745.8, 1497.6, 1852.5, 2604.2, 2959.1.
  - The empty unit (T2, 80 mullions): 9 toplights of 324.7, bars 388.7, 741.3, 1498.7, 1851.3, 2608.7, 2961.3.
  - The ironmonger (T2, 2 lights): 6 toplights of 509.7, bars 573.7, 1111.3, 2238.7, 2776.3.
  - The grocer (M2): 6 of 683.0, bars 725.0, 2147.0, 3569.0. If "sunrise" means one sunburst glazing per light, then 3 toplights with bars on the mullion lines only.
  - The tea room: bars 568.4, 1675.0, 2781.7, not 582.3, 1128.7, 1675.0, 2221.3, 2767.7. The panes are then equal, at 504.4.
  - The launderette: the mullion carried up to give 2 toplights of 1600. P5, its own type photograph, shows the upper lights divided on the lower lights' lines.
  - Set `toplight_aligned` true on all of these.
  - FRN-04: also check bar centres (±2 mm), a bar on every mullion line, and no toplight narrower than 250 mm.

### 2. Rita's back door stands inside the stock wall

- **The fault:** `R-back-door` (x 1.45 to 2.35, z 0 to 2.0) overlaps `R-back-stock` (x −2.6 to 2.6, tiers at z 0.5 to 2.05). D3's back-wall drawing shows the tiers running across the door. A script builds shelves through the door, and night_dark's back-room light ("through the ajar back door") then has nowhere to come from.
- **Fix:** `R-back-stock.x` becomes [−2.6, 1.35], with one tier of boxes over the door only at z 2.05 to 2.25 (x 1.45 to 2.35). The strip x 2.40 to 2.6 is plain wall. The stock wall's "five tiers ... filled shoulder to shoulder" applies to x −2.6 to 1.35.

### 3. `R-back-stock` is 0.40 deep against the target's own 0.30 rule for shelves

- **The fault:** the rule says shelf units and their goods stand at 0.30 (true). My independent measure gives 22 px at CLOSE_35 for goods 0.40 off the back wall, at the window's middle (the 20 px budget is about 0.36 there). The self-check passes it only because 0.40 falls under the 0.60 "furniture" class.
- **Fix:** boards 0.30 deep. The four `television_02` (about 0.35 deep at their size) go on the two tiers above the counter, where 0.35 stays under 20 px at mid height. Alternatively, write R-back-stock into the tolerated class by name.

### 4. Rita's side walls are left about three-quarters bare

- **The fault:** with both side units removed, the left wall carries one 1.8 x 1.2 pegboard and two cards, and the right wall one 2.2 x 1.0 board, two ukuleles and a mirror: about a quarter of each wall above the floor. From STREET_30 the viewer's-left wall is a third of the view. The approved recipe's second pass (1 October) was made because "the right wall stood nearly bare ... the room read as a showroom".
- **Fix (within the 0.10 rule):**
  - `R-left-board`: y 0.3 to 4.2, z 0.45 to 2.15, hung with ticketed small goods, wall clocks and framed pictures. The notices move onto it.
  - `R-right-board`: y 1.3 to 4.2, z 0.45 to 2.15. The ukuleles and the mirror stay at y 0.4 to 1.2.
  - Both stay at 0.08.

### 5. Other marks the thumbnails show

- `CashRegister_01` (six shops): the readout reads "$021.37" and the drawer plate "TITCH BANKS". Paint out the "$" (or make it "£") and blank the plate.
- `cement_bag`: besides the red logo, "CEM 42.5 N" (the EN 197-1 name of 2000) and a panel of modern safety pictograms. Blank all of the print to a plain stamp, not only the logo.
- `lifebuoy` (chandler, in the display at the close view): "Lighthouse" and "PH • SA • 20" are lettered on it. Replace them with a made-up vessel name, or blank them.
- `rubber_boots`: the description names an "embossed logo". Confirm it at 1k.

### 6. The night_dark sodium wash uses the stale scene colour

- **The fault:** every room's night_dark state uses linear (1.0, 0.7055, 0.0). QUEUE.md's log of 9 Oct 12:10 calls that value stale. The game's look file uses `lantern_linear_rgb` (1.0, 0.25, 0.0) (unreal-look.json), so the dark windows would glow yellower than the street's lamps.
- **Fix:** linear (1.0, 0.25, 0.0) from unreal-look.json, in every `lights.night_dark` and in TARGET.md section 3.

### 7. The M1 doors' letter plate sits in the glass

- **The fault:** Mickey's, the fish market, the laundry and the chandler have M1 doors glazed from 198, but their `letter_plate` is at z 545, inside the glass. Its note is copied from the T1 door.
- **Fix:** an M1 letter plate centred in the 170 bottom rail at z 113, or none. Correct the note.

### 8. Jafar's page

- **The door question.** It offers 871 (photograph) against 600 (2.2). The approved game door he has seen (rita-day-kit-2026-10-06.jpg) has its glass from about 1000 (one pane, no bar). Add that as the third option. 871 is still the recommendation, as photographs win.
- **Rita's approved room is changed in composition:**
  - the counter goes to the back wall;
  - both side units go;
  - the long-case clock and the cabinet go.
  
  Rita's room is the approved model (RULINGS 2 Oct). CLAUDE.md sends anything touching the look to him on one page before merging. Add one line: "Rita's room flattened so nothing smears at 1.5 m: approve?", with before and after pictures. Recommended: yes.
- **To keep his page at three:** drop the lit-list question. The street file and RULINGS 1 Oct already settle it, and the target keeps the street file's list.

### 9. Photographs-win records

- Add **D10**: P6 (Kames, 1995) shows an unlet shop's glass blank and grey with no whitewash. The empty unit is whitewashed by Jafar's ruling of 3 October (4.1). Chosen: whitewash. Why: the ruling.
- The lever at 1000 is kept against P1's handle at 0.42 of the leaf (about 890). Write the reason: the approved game door's lever stands at about 1050 (rita-day-kit). The present text only says "not adopted (narrow point)".
- Section 8 says "a 2100 leaf would move the glass foot to 867". It would be 896 above the footway (0.413 x 2100 + 28).

### 10. Checks: what the gate cannot catch, and one gap it can close

- **PRJ-02.** It runs on the gate's own `trace()` bake, so it proves the gate, not the game. Mark it so, and add an owed PC row: from CLOSE_35 and CLOSE_35_B in the packaged game, a marker at the picture's centre moves as `trace` predicts (Rita's: 1322 px of 4096, ±20).
- **Add LIT-05, the display lit at night.** In STREET_SQUARE at night, for the six lit shops, the display zone (the window lights' lowest 0.85 m) has a mean luma of 45 or more, with the spec's spill (350 lm rect light in the window head, tipped 62 degrees) modelled in the gate. LIT-01 and LIT-02 are room-only, so a lit shop with a dark window bed passes them today.
- The rest do catch what was asked:
  - **A black void:** PIC-02 (luma floors, dark share, largest dark region), PIC-06 (no flat surface), LIT-02 (three views).
  - **A room that does not shift:** PIC-04 (back-wall corners to ±8 px) and PRJ-01 (identity) catch a picture not rendered to the rule.
  - **A lit room dark at night:** LIT-01 and PIC-02 (night_lit).

### 11. The nine other fronts point to a Markdown section

- **The fault:** the missing kit variants (`front.missing_from_3_2`, plus M1 and M2 doors: "M1 and M2 as 2.2") cite "targets/shopfronts/TARGET.md section 10".
- **Fix:** name the JSON instead, at its commit: `targets/shopfronts/target.json` with `parts.window_frame`, `parts.shop_door`, `parts.stallriser`, `parts.pilaster`, `parts.lobby`, `alterations.aluminium_refit`, `alterations.steel_refit`, `alterations.refit_1930s`, `alterations.recessed_lobby` and the `profiles` each uses. A script can then build every front from this target.json and that one versioned input.

### 12. Rita's grille by day

- **The fault:** `blinds_grilles_shutters` says "none by day", but not what stays.
- **Fix:** "by day the lattice is lifted out and stored inside; the 40 x 40 top rail and the bottom channel stay, powder black". Alternatively, both come off, with their four fixing plates visible on the pilaster shafts. LIT-04 then applies at night only. Also, "a 40 x 40 box top rail under the fascia at z 2.50" stands at the transom, 450 below the fascia: say "at the transom".

### 13. `self_check.py` rewrites target.json

- **The fault:** every run writes the self-check rows back into target.json, with ties in an order that varies, so re-running a check edits the target.
- **Fix:** sort ties by name, and write only when `--write` is given.

### 14. Statements to correct

- Section 11 says Rita's room "stays on the project's earlier sources (Marshall's Hull photographs, the Black Country museum, as links)". Section 2 lists both as not reached or not used, and an unreached source is never evidence. Say instead: "Rita's room rests on the approved pictures (RULINGS 2 Oct); no period photograph of a pawnbroker's room was reached."
- Section 4.6 says the pawnbroker's spec entry is "unchanged except pixels_wide and the display's x0/x1". The `decal` also changes, from interiors-2026-09-23/int23_pawn to shop-rooms/pawnbroker_day. Say so, or keep the old value.

### 15. Ceiling fixtures' extents

- **The fault:** every `*-ceiling-tubes` fixture has `y` null and `z` [0.0, 2.4], which describes a full-height object. The tubes' real places are in `lights.tubes`.
- **Fix:** Rita's `R-ceiling-tubes`: x [−0.75, 0.75], y [0.9, 3.1], z [2.355, 2.4]. Other shops: from their own `lights.tubes`.

## Answers to the seven points asked

1. **Rita's room and front.**
   - Front: faults 1 and 2, and narrow points 1 to 4. Otherwise sound:
     - zones, pilasters, consoles, fascia, cornice (150 by ruling), sill and stallriser match the kit;
     - paints match 2.2;
     - the door's handing matches the approved front;
     - the grille is specified in numbers;
     - the cameras' eyes and aims are right (CLOSE_35: 1.5 m out, 1.05 m along = 35 degrees).
   - Room: the box, finishes, lights per state, luma targets and goods list are complete enough to script, once narrow points 2, 3, 4 and 15 are applied.
2. **The stand-off rules, re-derived** with my own measure on `trace`, at Rita's own eyes:
   - Goods 0.25 off the back wall, card middle: 2.6 / 13.6 / 13.7 px (STREET_SQUARE, STREET_30, CLOSE_35). The target has 3 / 14 / 15.
   - A counter at 0.60: 6.5 / 33.3 / 34.5 px. The target has 7 / 35 / 38.
   - Back-wall budget at the card middle: 0.36 m for 20 px and 0.69 m for 40 px. The target has 0.33 and 0.64, the minimum over many places, so more cautious.
   - A board 0.05 off a side wall at mid depth: at most 13.7 px. A board at 0.08: 19.7 to 21.9 px. That matches the target's 0.06 true and 0.10 tolerated.
   - A floor item 0.03 high: 20 px. The target has 22.
   - Exact matches: the parallax test (1322.1 px) and the back wall's corners ((940.4, 425.9) to (3155.6, 1429.1)). The window's far end is at 61.2 degrees from 1.5 m and 67.2 from 1.0 m.
   - **The rules hold.**
3. **Never-list.**
   - Faults 2 and 3, and narrow point 5.
   - The denied list is thorough: drink, toys, school furniture, weapons, the post-1992 items, the branded cleaners. The tobacco items are handled (the cigarette pack's face goes to the atlas; it reads "Kentucky Ace", and 'kentucky' is blocklisted).
   - The previews show no alcohol, no gambling and no child.
   - People: P2's figure is outside the crop and none is visible in the others.
4. **Poly Haven.** All 104 model ids exist in the live catalogue (checked in full, not sampled) and all 17 texture ids exist. All are CC0 under Poly Haven's licence.
5. **Photographs win.**
   - D1 re-read from the pixel table:
     - glass foot (457.5 − 319) / 335 x 2040 = 843 above the leaf's foot, so 871: right;
     - bar 1425;
     - top rail 95.
   - It follows the photograph against 2.2's 600, as it should. The approved game door (about 1000) belongs in the question to Jafar (narrow point 8).
   - Not recorded:
     - P6's unwhitewashed glass, against the 3 October ruling (narrow point 9);
     - P5's divided upper lights, against the laundry's single toplight (narrow point 1).
   - Followed against a photograph without a written reason: the lever height (narrow point 9).
6. **Scriptable from target.json alone?**
   - Rooms and displays: yes, after narrow points 2 and 15.
   - Rita's front: yes from the kit's glb, except above the doors (fault 1) and the glazing data (narrow point 1).
   - The other nine fronts: only with 2.2's target.json as a second input (narrow point 11).
7. **Would the checks catch the three failures?**
   - A black void: yes.
   - A picture not made to the rule: yes.
   - A lit room dark at night: yes for the room. Not for the display (LIT-05, narrow point 10), nor for the game's own card (owed on the PC).

## What is right

- **The count of ten.** The street has ten units as built. "Twelve" is the superseded atlas proposal, and the brief's twelve is answered plainly. The Hal's shop conflict and the lit-list conflict are named, not hidden.
- **The method.**
  - The game's rule is kept exactly and imported, not rewritten.
  - The honest range (the CLOSE view at 1.5 m, the near 0.55 m real) is argued from numbers.
  - The 4096 picture is justified by texel density.
  - The three failures of 3 October are each answered with a rule and a check.
- **Rita's front data**, beyond the gaps above:
  - the kit's own sizes, the 12 October cornice ruling and the paints;
  - the bell and the OPEN sign as Judgement, marked as such;
  - the grille in numbers;
  - the cameras computed per shop.
- **The inventory.** Every model has an id, size and shop. The denied list is reasoned. Scans that need a login are named as a failed capability of the cloud, not dressed another way.
- **Sources.** Only reached ones are relied on, with dates and licences, which I confirmed on Geograph for P1, P4 and P6. Unreached sources are listed apart.
- **The self-check.** 269 rows and 13 negative controls, a fair base for the build's gate once FRN-04, FRN-07 and LIT-05 are added.
