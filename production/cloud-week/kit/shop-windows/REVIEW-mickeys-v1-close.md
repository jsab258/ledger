FAIL

# Mickey's (east_parade bay 0, no. 1, front only), the CLOSE view: fresh review, try 1 (cloud week 42, unit 7 part 2, stage 2; 15 October 2026)

Reviewer: a fresh reviewer who did not write the target, build the front or write any other review. One view only: CLOSE_35 and CLOSE_35_B, day and night_lit, 2560 x 1440 frames in ledger-scratch/shop-windows/mickeys/gate (all dated 13 Oct, 18:15 to 18:34), and the two close previews. I did not read the street view's review.

The front is well made. Up close, though, nothing on it says "minicab office". The target's two window rows, the phone number and MINICABS · 24 HOURS, were not built. The builder's notes do not name the gap, and the check could not see it. That one gap is the fault.

Coordinates are pixels of the 2560 x 1440 frames unless a preview is named.

## Faults (worst first)

### 1. The window's two lettering rows are missing: 0632 960418 and MINICABS · 24 HOURS

- **Pictures:** every frame. In CLOSE_35 day and night, all three lights (360-1580 x 1.6, 20-830 x 1.6 in preview terms, i.e. about 576-2528, 32-1328) show only the stand-in card and the reflection. CLOSE_35_B is the same over its three lights (0-2060, 0-1330). The street preview agrees.
- **What should be there:**
  - The target asks for three glass rows: '0632 960418', 'MINICABS · 24 HOURS' and '1'. They are in TARGET.md section 5.1 "glass", in target.json `shops.mickeys.glass.lettering`, and in section 1 ("What unit 7 does for Mickey's: ... the glass rows `0632 960418` and `MINICABS . 24 HOURS`").
  - Only '1' was built, in gilt on the fanlight.
- **Why it matters:**
  - The fascia is out of the close frames, so at 1.5 m the glass rows are the only sign of the trade.
  - The NOTES section does not list the gap as a shortfall.
- **WHOSE:**
  - The builder, for the missing rows.
  - The kit, for the check. GLS-02 tested "1: 0 of 850 ink points", the one row that exists, and passed. It never compares the rows built against the target's list.
- **EXACT FIX:**
  - **(a) Build the two rows** as glass rows on the inside face of the window glass (d 29 to 36), the same way as Rita's WATCHES / JEWELLERY / LOANS, using 4.1's glass-row lettering.
  - Unless 4.1 gives Mickey's another place:
    - 'MINICABS · 24 HOURS' as one row centred on the window zone (u 2025), cap height 110 mm, centre z 1700.
    - '0632 960418' under it, cap height 90 mm, centre z 1520.
    - Both in the fascia's gilt with a 3 mm dark keyline, as signwritten gilt on glass. Neither row may cross a mullion (u 1100-1150 and 2200-2250): if 'MINICABS · 24 HOURS' at 110 mm is wider than the middle light (1050), put it on two lights or reduce it to 90 mm.
  - **(b) Kit check.** GLS-02 must also count the rows. The number of rows drawn must equal the number of non-empty strings in `glass.lettering`, or the row fails.
  - **(c)** OCR the close frames to confirm both rows read (ocr_words.py).

## Narrow points (each with its exact fix)

Points N1 to N3 are the shared gate fixes of 14 Oct. Target.json records Mickey's as "rebuilt for the shared gate fixes only (T2-16)", but the frames and check_mickeys_v1.json are of 13 Oct. That rebuild never reached these files. One re-run of `build_shop.py --shop mickeys front gate checks` with the current kit settles N1 to N3. None of them fails the shop alone.

**N1. The stand-in street lamp's pool shows in the night glass as a burnt orange bar.** This is the brief's point (g).
- **Where:**
  - CLOSE_35 night_lit, about 610-1380, 670-780: mean (145, 95, 47), 6,322 px clipped red.
  - CLOSE_35_B night_lit, about 1360-2190, 665-760: 9,406 px clipped red.
  - Close night preview, 380-860, 420-490.
- **What it is:** the far pavement's lamp pool and its kerb line, mirrored by the gate's glass. It is the same as shared point (a) of the newsagent's try 1 close review.
- **WHOSE:** the kit; already fixed there.
- **FIX:** re-run the gate with `street_glossy: false`. Check v2 must carry and pass GLS-04 (the largest patch 40 levels over the reflection-off render is under 0.1 per cent of the glass) and PIC-05g (burnt share under 0.01).
- **Measured now:** the burnt share is 0.0017 and 0.0026, which already passes PIC-05g. The bar is the fault, not the burn.
- **No arc and no burn otherwise:**
  - The near pavement at night has mean luma 99, max 136.
  - The faint curve across the middle light (CLOSE_35_B night, about 1440-1600, 80-1150) is the edge of the same lamp's reflected cone. It should go with the same fix; confirm it in the re-run.

**N2. The door card reads CLOSED in night_lit although Mickey's is lit and open until 3 am.**
- **Where:** CLOSE_35_B night_lit, about 2160-2215, 585-635 of the frame (the door crop's 100-155, 585-635).
- **WHOSE:** the kit (the 14 Oct "door sign by hours" fix).
- **FIX:** OPEN in day and night_lit. CLOSED only in a night_dark picture (before Tom's key), if one is made.

**N3. A reveal slab shows through the shop door's glass.**
- **Where:** CLOSE_35_B day, about 2060-2230, 925-1000. A flat grey shelf ends at mid-height behind the door's pane, with a hard top edge.
- **WHOSE:** the kit (FRN-13, 14 Oct).
- **FIX:** re-run with FRN-13 in the check (560 rays through the door's glass never end on a reveal slab).

**N4. The tile stallriser reads as a printed panel at 100 per cent, not as tiles.**
- **Where:**
  - CLOSE_35 day 560-1700, 1060-1440.
  - CLOSE_35_B day 1290-2050, 1100-1440.
- **What is wrong:**
  - The triangles are about 300 mm across, with no grout joint anywhere.
  - At every 609.6 mm repeat a jagged cream "bite" sits on the top edge. CLOSE_35 day has them at about (615, 1095), (710, 1145), (810, 1175), (930, 1225), (1055, 1265), (1180, 1305) and (1410, 1395). This is the print's own border repeated at each seam.
  - The blue triangles carry dark dots, like screw heads.
- **WHOSE:** the builder (M4, the repeat), with the 4.1 print.
- **FIX:**
  - Repeat only the print's whole-tile interior, cropping its border, so that no bite shows at a seam.
  - Draw grout joints every 152.4 mm (6 in), 2 mm wide, in (150, 148, 140), with the normal map giving them a 0.5 mm recess.
  - Give the glaze a roughness of 0.12 to 0.20, varied per tile.
  - Remove the dots, or keep them only if 4.1's print shows fixings.
- **Note:** the dark plinth under the tiles is slate (luma 45 to 47), not black. It is fine.

**N5. No hours plate on the shop door.**
- **Target:** 4.2 puts the hours plate on the glass beside the OPEN / CLOSED sign, and 5.1 says the door's furniture is "as 4.2". The brief's point (c) lists it. Mickey's door shows the OPEN card only (CLOSE_35_B day, the door crop).
- **WHOSE:** the builder.
- **FIX:** add 4.1's engraved laminate hours plate, 300 x 190, inside the door glass under the card (top z 1380, at the card's depth), reading the hook-cast hours: MON-SAT 7 AM - 3 AM, SUN 9 AM - 3 AM.

**N6. The target contradicts itself on the hours.**
- **The contradiction:** the glass row says MINICABS · 24 HOURS, but hook-cast.json's hours are 7 to 3 am (9 on Sundays).
- **WHOSE:** the target.
- **FIX:** the target's owner settles it in one line before the rows are drawn. My recommendation: keep "24 HOURS" on the glass, because a minicab office's phone line is answered all night, which is period-true. Make the hours plate read "OFFICE 7 AM - 3 AM, SUN FROM 9", so the two do not disagree on the door.

**N7. The builder's named shortfalls, judged:**
- **Front only, a flat stand-in card behind the glass:** not a fault. It is the brief's scope. The real room is owed to the PC (PC-01).
- **The door shut and the night lit from the card only:** narrow. The visible part is N2. The real night states are the game's.
- **Plain gilt with no gilding wear, and the tile being 4.1's print:** the gilt is a narrow point that blocks nothing. The tile is N4.
- **LIT-02, LIT-05, LIT-08, DSP, ROOM and INV n/a:** accepted. There is no room or display in this unit.

## What is right

- **The front's sizes and parts:** FRN-01 to FRN-05 hold within 1.5 mm, and the close frames agree with them.
  - The slate steel window and its mullions, the transom band and the beads read as painted steel sections.
  - The clad pilaster shows its sheet joints (CLOSE_35 day, 430-470, 145 and 750 of the preview).
- **The shop door:**
  - The glass foot sits on a 170 mm bottom rail.
  - The chrome letter plate is in the bottom rail, clear of the glass (CLOSE_35_B day, about 2120-2210, 1190-1210).
  - The chrome D pull is a vertical bar on the lever stile.
  - The jambs are clean.
  - The gilt "1" on the fanlight is crisp.
  - The OPEN card is green with white letters, hung on its hook.
- **The bell:** it hangs inside, by the door (CLOSE_35_B day, about 2010-2040, 440-470).
- **The side door:** an oxblood four-panel F1 door, with a vertical chrome letter plate in the muntin and a black centre knob. Both are period-true. Its sill and step are there.
- **No black strips, no see-through slot:**
  - FRN-10: 0 dark patches of 28 px or wider at either close camera. I looked along the shared jambs of the shop door, the side door and the pilaster and found none.
  - FRN-08: 0 backdrop px at CLOSE_35 and CLOSE_35_B.
- **The export faults of Rita's shop are not repeated:**
  - The normal map is a true tangent map (GLB-01, FAS-01n, mean (128, 128, 256)).
  - No textured primitive lacks UVs (FAS-03).
  - There are no coplanar black strips and no slot.
- **No black void or slab at the second camera:** the card fills every light in both cameras (lowest light mean 45.6, sd 5.5 to 25).
- **Glass luma (my boxes inside the three lights, frames as rendered, reflection on):**
  - Day: 45.6 / 47.3 / 48.3 at CLOSE_35 and 47.3 / 57.7 / 55.5 at CLOSE_35_B. The day floor is 33, so this passes.
  - Night_lit: 57.9 / 62.0 / 59.4 and 60.6 / 56.7 / 53.4. The night floor is 45, so this passes.
  - The wall beside the glass reads 88 and 77 by day, and 23 and 14 at night. So at night the window is 2.5 to 4 times brighter than the wall, as a lit shop should be.
  - These numbers measure the stand-in card, not Mickey's room.
- **Burn:** the burnt share is 0.0000 / 0.0017 / 0.0013 / 0.0026 across the four close frames (limit 0.01).
- **Every legible word at 100 per cent:**
  - "1" (fanlight), "OPEN" (card, day) and "CLOSED" (card, night). All three are acceptable.
  - MICKEY'S is out of the close frames; only a gilt corner shows at CLOSE_35_B's top right.
  - No word, maker's name or mark on the tiles, the letter plates or the pull.
- **The content rule holds:**
  - No drink, betting, child, toy, person, barcode or flat screen, and nothing after 1992.
  - NEV-01 matched none of 188 strings.
- **Check rows I trust (measured on the meshes or frames):** GLB-01, FRN-01 to FRN-05, FRN-07, FRN-08, FRN-09, FRN-10 (by day only), FAS-01, FAS-01n, FAS-03, FAS-04, CAM-01 and X-PRV.
- **Rows I trust only in part:**
  - GLS-01 and GLS-02 are true of what was built, but blind to the missing rows (fault 1).
  - NEV-02 is a statement about the front's parts, not a measurement.
- **Rows that are only the cloud's stand-ins:** the glass and its reflection (the day reflection is a Poly Haven street, not Quay Street), the night lamp, the card and every luma above.

## What I cannot judge from the files

- **The room's own criteria (a) and (b):** the near-metre display, the projected room's depth and parallax, the trace-rule point, and the display-to-room seam.
  - This unit has no display and no room picture. The card is a flat stand-in, not traced, so CLOSE_35 against CLOSE_35_B shows no room parallax by design.
  - Mickey's real walked room (room_3d) is the game's, owed to the PC.
- **The game's own glass, light and image:** the glass's reflections and its Fresnel hand-over at 61 degrees, Lumen, the exposure, TSR, and the sign's and room's real night (dark until Tom's key).
- **The 14 Oct rebuild:** I judged it only as far as it is recorded. The files on disk are the 13 Oct build.
- **The gilt letters at close range:** they are not in the close frames.
