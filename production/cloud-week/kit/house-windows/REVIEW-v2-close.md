PASS

# House windows, the CLOSE view: fresh review, try 2 (cloud week 42, unit 8 part 2; 14 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the kit. I judge one view only: the close cameras on `east_parade_bay0_upper_w1` (S22, white_grimy, N1 white voile, C2 cream curtains open, up_lounge_1 behind).
- `close` is the target's H_ALONG_30_NEAR, 19 degrees from the wall.
- `close2` is 1.5 m off the wall and 1.6 m along it, 22 degrees from the wall.

Both are judged by day and night_lit. I did not read REVIEW-v1-street.md or REVIEW-v2-street.md.

**Read:** CLAUDE.md; RULINGS.md (3 October white frames; 1 and 2 October rooms; 8 October photographs win); TARGET.md sections 3 to 7, 9, 10 and 14; my own try 1 review (REVIEW-v1-close.md); then NOTES.md, including "Try 2: what the two reviews asked and what was done"; `checks/check_windows_v2.json`; the parts of `hw_gate.py`, `hw_gate_run.py` and `hw_kit.py` named below; `tools/ue/make_interior_material.py` (`trace`).

**Looked at:**
- the four v2 close previews beside the 13 October ones;
- the four close gate frames (2560 x 1440) beside the try 1 frames (`gate_try1/`), whole and at 200 to 300 per cent;
- their masks, the clear-glass masks (`maskT_`) and the night reflection-off frames;
- `up_lounge_1` day and night_lit, the try 2 picture against the try 1 one;
- for the row rulings only: the frames `h-along30-bay3w1`, `h-along15road-bay3w1`, `h-along30-gf2w1` and `h-across0-bay2w0` night.

**Measured** (everything in my scratchpad; nothing in the repository or in the builder's scratch was changed):
- pane and frame luma per pane, from the masks;
- the night glass's hue, pixel by pixel and in 32 px blocks;
- the parallax, through `trace` itself, against the reflection-off frames;
- the four try 2 glbs against the try 1 ones (part bounds, normal maps, UVs), and a coplanar-face scan in all six directions;
- the pendant shade projected into five cameras;
- **two test renders** of the bare window `h-along30-bay3w1` (1280 x 720, 16 samples, `nice -n 15`), with the gate's own code unchanged and the glass reflection off and on. The cards were copied into my scratchpad, so nothing was baked in the builder's folder.

**In short.**
- Both try 1 faults are fixed in the close view.
- **By day** the glass is glass. The white voile and its folds show in the lower sash. The upper sash shows the room's ceiling, the box's own linings and the far cream curtain, with the grey soffit and the bright sky reflected in it. The frame's dark lines hold.
- **By night** the lit ceiling is tungsten, not olive.
- The black notch is gone, and the builder found its true cause.
- The joinery is the same believable 1990 box sash.
- The room obeys `trace` exactly at the new gain. Nothing new breaks the content rule or carries a mark.
- What is left in this view is one narrow point: by night the lit ceiling next to the rose is a flat plateau. Two things I found outside this view are listed separately and are not counted here.

**0 faults, 1 narrow point** (in this view). This is try 2 of the CLOSE view. Under Jafar's ruling of 9 October it is a PASS.

## Try 1, item by item

| try 1 item | now | measured (try 1, then try 2) |
|---|---|---|
| **Fault 1:** by day the pane was a mirror; no net, curtain or room | **FIXED** | P/L: close2 0.358, now **0.628**; close 0.248, now **0.582** (band 0.55 to 0.97; my try 1 test predicted 0.67 and 0.59). close2's lower-right pane (1376-1523, 683-958) read a flat 165; it now reads median 191, p5 75, p95 211, with the voile's folds plainly seen (preview `hw-close2-day` about (860-950, 430-600)). The upper panes, which read medians 17 and 30 (black), now read 74 and 78. GLS-06 passes at 15 to 70 degrees; MAT-04's energy reading is 1.000; NEG-01 fails the old pane as it must. |
| **Fault 2:** the lit ceiling was olive (red clipped) | **FIXED** | close2 night: 32 px blocks with linear g/r over 0.85 went from **19 of 114 to 0 of 115** (worst 0.798; median g/r 0.781, now 0.709). close: 2 of 31, now 0 of 31. Pixels at g/r 0.9 or more went from 16.7 to 1.3 per cent. Those 1.3 per cent are grey edge pixels (median 1 px from the glass's edge, luma 51, colour (50, 49, 47)): anti-aliasing, not olive. No lit picture has a channel at 250 or more (the brightest is 237). No glass pixel in either night close frame reaches 240. |
| **N1:** black notch at the head of the far jamb | **FIXED** (the cause was the kit, not the wall: see below) | Joinery pixels under luma 15 in the box (1140-1220, 600-690) of close2 day: 160, now **0**. close day: 40, now 0. In the whole window by day, joinery under luma 10: 156, now 0. At 300 per cent the outer lining, the pulley stile and the beads now run unbroken into the head. |
| **N2:** the soffit black in the upper panes | **FIXED** | The top 40 per cent of close2's two upper panes by day read median 15 and 16 (72 and 82 per cent under luma 25). They now read median 67 and 68, p5 39 and 46, and 0.0 to 0.1 per cent under 25. The soffit reads grey in the glass, as a painted soffit does. |
| **N3:** no grime band | **PARTLY: the builder's way accepted** | It is built in the gate by the house's condition and listed per site in the manifest (`sites[].grime_band`), not in the glb's COLOR_0. The builder is right and my try 1 fix was wrong: one glb serves every house of its kind, and six of the twenty sites are grimy, so a band in COLOR_0 would dirty the fourteen sound windows. GRM-01 reads 0.77 on the rail. Neither close view can show the band: from 1.5 m off the wall, looking up, the stone sill hides the lowest 0.4 m of the lower sash. |
| **N4:** WB-02 and WB-04 not to be trusted until fault 1 was fixed | **DONE** | WB-04 passes (close 0.31, close2 0.29; WB-04b dips 0.22 and 0.21). WB-02 reads 0.48, as I predicted. On its cause the builder corrected me: see the seven rows below. |

## New faults from the changes

None in this view. I looked for each one the brief names:

- **The glass.** No mirror, no black strip, no see-through slot. The clear-glass mask behind close2's glass reads card, cloth or joinery only (35,925, 42,888 and 39,092 px; no brick, no world). No glass pixel by day is over 243.
- **The lit card's gain (x 1.0).** Nothing clips (the brightest glass channel is 239). The cost is a plateau: narrow point 1.
- **The soffit.** Grey, as asked.
- **The 0.5 mm moves.** The try 2 glbs differ from the try 1 ones only in `head_outer_lining`, `head_parting_bead`, `head_staff_bead` and `lower_bottom_rail` (+0.5 mm toward the street, S22 and S11) and in the RC and RC2 weld strips (+0.3 mm). No gap or slot is seen in either close frame.
  - My coplanar scan in all six directions leaves only faces that cannot be seen: the tops of the head lining and the side linings (behind the arch); the jamb-side faces (in the brick); the room-facing faces at 250.8; and the stile feet on the sill riser (392 mm2 each by my count), which sit behind the stone sill.
- **The cottage lamps at 0.7.** Not in this view. The close night frames show no burnt joinery or brick: 8 joinery pixels under luma 10 in close2 night: four in the far jamb's inside corner at the head (1201-1202, 642-644) and four by the meeting rail (1199-1211, 927-948). That is real shade at night; by day the same corners read 0 under luma 10.

## Faults, worst first

None.

## Narrow points

1. **By night the lit ceiling next to the rose is a flat warm plateau, not a ceiling.**
   - **Where:** close2 night, the upper-right pane (1346-1492, 415-750; preview 1600 about (841-933, 259-469)).
     - Its local spread is 0.75 levels (standard deviation over 15 px), against 2.4 to 6.2 in the other three panes.
     - Half its pixels lie within 3 levels of its 90th percentile (luma 200 to 204). It is 20 per cent of the window's glass.
     - In the preview it reads as a pale warm card.
   - **Cause:**
     - Through the upper sash the close views see the ceiling within about 0.6 m of the rose (my trace: picture x 177 to 807, y 39 to 123 of 1536 x 1399).
     - The rose and the pendant stand 0.55 m behind the front wall, so that part of the ceiling lies well over the roll-off's knee: 34 per cent of that band is at luma 200 or more.
     - The roll-off eases it all onto the same 0.85 ceiling. The hue is right (g/r 0.71); the shape is lost.
     - It is the builder's listed shortfall ("a soft warm plateau").
   - **Whose:** the builder (`hw_roomgen.py`, the night_lit lights).
   - **Exact fix:**
     1. In the six lit lounges and bedrooms, halve the pendant's point-light power.
     2. Make up the mean with fill: a room-wide area light at the ceiling's centre, or the target's table-lamp glow on the back wall. Keep each picture's mean at 70 +-15 per cent and the roll-off as it is.
     3. Done when close2 night's upper-right pane has a local spread of at least 2 levels, with under 25 per cent of its pixels within 3 levels of its 90th percentile (today 0.75 and 50 per cent).
     4. Add the second figure as a row for the close views.

## The seven failing rows

None is a fault in the build. Each is ruled below.

- **WB-01 (two windows out of ten): a mis-set row, by tolerance and by size.**
  - `east_parade_bay4_upper_w1` (0.458) is read from 434 glass pixels across the street: too few, the check's own asterisk.
  - `east_parade_bay1_upper_w1` (0.545) is 0.005 under a band edge.
    - The gate's own repeatability is wider than that: my 1280 x 720, 16-sample render of the bare window reads P/L 0.509 where the gate's 2560 x 1440, 40-sample frame reads 0.476.
    - The one photograph of a half-net window (P4_E, a net over the lower half) reads 0.555.
  - **New row:** band 0.55 to 0.97 with a tolerance of 0.03 (fail under 0.52), read only on windows with at least 5,000 glass pixels at 2560 x 1440.
  - Both close views pass (0.58 and 0.63).
- **WB-02 (the bare window at 0.48): a stand-in's limit.** I checked the builder's split with my own two renders: glass reflection off, **0.423**; on, **0.509** (the gate's frame 0.476).
  - The room side is 0.42. 46 per cent of that glass sees the box's own white inner linings (luma 75 to 78) and 54 per cent sees the day card (68).
  - The stand-in dome's reflection adds 0.06 to 0.09.
  - Note that the band's only photograph at 15 to 30 degrees, P1_c, is a dark-brown frame whose inner linings are dark. A white frame's linings, seen through the glass, are not.
  - **Row change:** in the cloud, read WB-02 on a day reflection-off frame (glass_refl 0, as NIGHT-03 already reads the night frames), band 0.10 to 0.45 unchanged. Report the beauty reading beside it. Judge the beauty reading on the PC with the game's reflections (OWED-01, OWED-06), against a white-framed bare-window photograph when one is reached.
- **WB-04b (one window at 0.62): a mis-set row.**
  - The one window, `east_parade_bay2_upper_w1` in `h-along15road-bay3w1`, is cut by the frame's top edge (its box starts at y 0). The builder's own rule 3 keeps a cut window out of WB-06 and WB-07.
  - Only one edge was profiled, and that edge crosses brick seen through the glass (see "Outside this view", item 1), not a dark line.
  - **Row change:** read only windows not cut by the frame's edge and with at least 3 edges profiled.
  - Twelve windows read 0.19 to 0.34; the close views read 0.22 and 0.21.
- **WB-07 (three small far windows under the floor): a mis-set row, by size.**
  - The three readings come from 492 to 1,346 joinery pixels, seen across and along the street from the cottage footway. Most of the joinery seen from there is reveal-facing faces, shaded to 0.6 by design.
  - Every window with 8,000 joinery pixels or more reads 2.84 to 7.82.
  - **Row change:** read only windows with at least 5,000 joinery pixels. The floors (3.0, and 2.5 for grimy and flaking) stand.
- **NIGHT-01, NIGHT-02 and NIGHT-07 (over the cottage windows): the cottage rooms' brightness is what moves.** Not the lit gain, and not the rows.
  - **Not the lit gain:**
    - In this view a gain of 2 to 2.5 for every lit room would put close2's lit ceiling (today at the roll-off's 0.80 to 0.85) at linear 1.7 to 2.1: a clipped pale-yellow pane, try 1's fault 2 come back.
    - In the close views the clear glass already reads 1.35 and 1.58 of the lit net.
  - **Not the rows:**
    - The upper windows pass NIGHT-07 at gain 1.0 (0.53 to 0.68 in the Hook and from across).
    - The lit net's 0.48 is the game's own number.
    - A net lit by a room's pendant cannot glow five or six times brighter than the walls the same pendant lights. A clear upper sash at 0.19 of its net is the room too dim, not the row too strict.
  - **What is too dim:** the part a cottage's clear upper sash shows at eye level is the back wall. Its mean linear luminance in the three GF night_lit pictures (box [848.8, 649.1, 2223.2, 1700.1]) is **0.040 to 0.048**, against the lit white net's 0.306.
  - **Exact fix:**
    1. Re-light `gf_front_1` to `gf_front_3` night_lit with the target's own "table lamp's glow on the back wall" raised, not the pendant, until that box reads a mean linear luminance of at least **0.12**. That is 2.6 times today's, the factor NIGHT-07's 0.19 needs to reach 0.5.
    2. Keep the largest channel eased under 0.85 (PIC-13).
    3. Set PIC-03's GF night_lit standard to the relit pictures' mean +-15 per cent.
    4. Measure NIGHT-01, NIGHT-02 and NIGHT-07 again as worded.
  - **Alternative, if one number is preferred:** a lit gain of 2.5 on the cottage card alone (`hw_room_card_gf`), with the GF night_lit pictures rolled off toward 0.34 instead of 0.85, so the card never passes 0.85. The upper rooms stay at 1.0.

## Where the builder says a review was wrong (my measurements)

1. **The black notch's cause: the builder is right, I was wrong.**
   - The stand-in wall's 2 mm (my try 1 fix) did not remove it. Moving the kit's head lining 0.5 mm off the side linings' plane did.
   - My own scan finds no street-facing coplanar overlap left where a camera can see it.
   - JNR-01 and the new KIT-19 and NEG-02 are the right rows.
2. **WB-02: right.** The room side alone is 0.42 (my render 0.423) and the sky adds the rest. My try 1 guess, the sky alone, was only part of it.
3. **MAT-04 needs the energy reading: right.** A reflection-only reading of the slab passes a mirror (0.277). My try 1 fix 4, "use the glb's pane", was not enough by itself.
4. **"Raise the fill, not the peak" met by the roll-off: right as far as it goes.** The roll-off was the better choice than my hard clamp. Narrow point 1 is what is left of "the fill".
5. **NIGHT-03 read on the reflection-off frames: agreed.** It is the room's own colour. The beauty frames read the same (0 blocks over).

## What is right

- **The joinery** (close2 day at 200 to 300 per cent) is the try 1 box sash, unchanged but for the 0.5 mm moves.
  - It has outer lining, pulley stile, parting and staff beads as separate white members.
  - The meeting rail has its shaded underside and the ogee horn.
  - The 22 mm bars and the putty lines are there. The frame is white (grimy), as ruled.
  - The lines hold: D/L 0.31 and 0.29; WB-04b dips 0.22 and 0.21.
- **The glass by day** shows what a real pane at 19 to 22 degrees shows:
  - the voile on the lower sash with soft folds of varied pitch;
  - through the upper sash, the ceiling, the box's own white linings and the far cream curtain (clear-glass mask: 31 per cent card, 36 per cent cloth, 33 per cent joinery);
  - in reflection, the grey soffit at the top of each upper pane and the bright sky below it (Jafar's "sky in the glass").
  - The same reflection lifts the frame/pane contrast without a mirror (GLS-06 at 20 degrees: the card reads 0.785 of itself, against 1 - F of 0.786).
- **The glass by night:** a warm, lit room behind a warm-lit net, r > g > b in every block. The net shows its folds. The room shows faintly through the net in close's lower-left pane. No orange bar, no hot corner, no lit stand-in lamp, no black strip.
- **The room obeys `trace`:**
  - Over 3,000 card pixels of close2's glass, the night reflection-off frame equals the night_lit picture, at the place `trace` returns, x **1.000** at the median (quartiles 0.990 and 1.005). In close the figure is 0.995. That is the new gain 1.0 exactly (try 1: 0.276, the old 0.28).
  - The cameras, the card and the bake are as in try 1, so my two try 1 ceiling points still land where the render rule puts them.
- **Stand-off, size, marks, content:**
  - The models, their placements and their maps are those of try 1 (`up_lounge_1.placed.json` unchanged since 04:03 on 14 October). Only the lights of the night_lit pictures changed.
  - The try 2 lit picture of up_lounge_1 holds the same empty bookcase, mirror, print and plain ceiling rose: no lettering, no drink, no gambling, no child's thing, no person.
- **Export (the four try 2 glbs):**
  - both normal maps are real RGB (means 0.50, 0.50, 0.99 and 0.50, 0.50, 0.98);
  - every textured primitive has TEXCOORD_0;
  - no visible coplanar faces (above);
  - no see-through slot in the S22 from these angles.
- **Glass by day and night against the rows** (window 4, the close site):

| frame | P | L | D/L | P/L | spread | band |
|---|---|---|---|---|---|---|
| close day (19 deg) | 104.9 | 180.1 | 0.308 | **0.582** | 162 | WB-01 0.55 to 0.97, D/L at most 0.72, spread at least 40: pass |
| close2 day (22 deg) | 118.8 | 189.1 | 0.292 | **0.628** | 152 | pass |
| close night | 125.3 | 82.8 | 0.369 | **1.513** | 156 | lit, r > g > b; my try 1 wording (lit P/L at least 1.0) passes |
| close2 night | 152.3 | 86.2 | 0.353 | **1.766** | 171 | lit, r > g > b; passes |

## Which rows to trust

- **Trusted** (read from the exported files, or confirmed by my own measurement):
  - KIT-01 to KIT-19; MAT-01 to MAT-04; GLS-06 and NEG-01 to NEG-03;
  - WB-01 and WB-04 in the close views; WB-04b in the close views;
  - NIGHT-03 (my blocks agree); JNR-01 (my count agrees); PIC-13 (my count agrees);
  - PIC-01 to PIC-12 as in try 1; CONTENT-01.
- **Trusted with the row changes above:** WB-01, WB-04b, WB-07.
- **Stand-ins only:**
  - WB-02's excess over 0.45 and WB-03's colour (the dome);
  - NIGHT-01, NIGHT-02, NIGHT-07 and NIGHT-08's absolute levels (the stand-in lamps, sky and exposure: OWED-07);
  - GLS-05 (the stand-in lamps);
  - the brick, the stone sill, the arch and the soffit (the wall kit's).

## Outside this view (not counted in this verdict; for the builder and the street reviewer)

Both are narrow by size and exact by fix. Neither is in the close frames: the close site is an S22, and the pendant falls on brick from both close cameras (143 of 144 of its projected points).

1. **RC and RC2: brick seen through the glass beside the far jamb.** I found this while ruling on WB-04b.
   - The clear-glass mask reads brick (code 4) behind the glass in 33 RC and 13 RC2 window readings. The worst:
     - `h-along30-gf2w1` day, `west_south_bay1_gf_w1` (RC, 19 degrees): 7,678 of 28,912 glass pixels, a full-height strip at (1592-1608, 454-984);
     - the same frame, `west_south_bay1_gf_w0`: 5,310 of 8,472;
     - the **Hook** day, the same `_gf_w1`: 2,097 of 4,127 at (33-51, 792-1025);
     - `h-along15road-bay3w1`, `east_parade_bay2_upper_w1`: 2,985 px at (1864-1905, 0-293).
   - It reads as a strip of brick with its mortar joints between the white frame and the net or curtain. The fix of the mirror pane (try 1's fault 1) uncovered it.
   - **Cause:** the RC and RC2 frames end at 142.5 mm into the wall and have no inner reveal. The S22 and S11 carry the lab's inner linings to 250.8. So a ray at under about 30 degrees from the wall passes the frame's back and meets the stand-in wall's brick on the inner reveal, where a real house has plaster.
   - **Whose:** the target (4.3 and 4.5 give RC and RC2 no inner reveal) and the kit.
   - **Exact fix:** add to RC and RC2 an inner reveal of four parts, 12.5 mm thick, from y 142.5 to 268 (short of the card at 270):
     - two jamb linings at x +-412.5 to +-425, z 0 to 1676.4;
     - a head lining at z 1663.9 to 1676.4;
     - a window board at z 0 to 25;
     - painted white emulsion, linear (0.72, 0.70, 0.64), roughness 0.9, box shade 1.0 at 142.5 falling to 0.6 at 268.
   - **New row GLS-07:** no glass pixel of any window sees brick (clear-glass mask code 4) in any gate frame.
2. **The pendant shade can never be seen.**
   - `pendant__shade` stands 0.55 m behind the room card (y 650 to 990 against the card at 270; target section 8), and the card is opaque, so the shade is hidden in every frame.
   - From across it should show: in `h-across0-bay2w0` night, 88 of its 144 projected points fall on the lit window's glass, at (1246-1314, 598-663). The frame shows a flat warm ceiling there and no shade.
   - Target 7.2's "at night, a warm ceiling and the shade" therefore gets only the ceiling.
   - **Whose:** the target.
   - **Exact fix:**
     1. Draw the shade in the card's bake, the same way `trace` draws the room. For each card pixel, test the eye's ray against the shade's frustum (radius 0.170 at its foot, 0.105 at its top, 0.24 high, axis 0.55 m behind the card, top 0.30 below the ceiling) before the room box.
     2. Where the ray hits, write the shade: emissive WARM x 3.0 when the room is lit; paper (0.93, 0.89, 0.77) lit by the room's day or sodium light otherwise.
     3. The game's interior material does the same test (or writes the traced depth as Pixel Depth Offset so a real mesh can show).
     4. Drop the separate `pendant__shade` node.

## What I could not judge from the files

- **Hidden from both close views:**
  - the curtain pole, brackets, finials, gathered head and hem (behind the head);
  - the net's lace band and hem, the bottom rail's foot and the grime band (behind the stone sill);
  - the pendant (behind brick from these cameras).
- **Not in the close views:** the S11, RC and RC2 pieces at close range, and a cottage window as a close view. Points 1 and 2 above were measured in other frames only for the row rulings.
- **Not re-looked at in full:** the ten other lit pictures. Their objects are unchanged; only their light changed, and PIC-13 and NIGHT-03 read them.
- **Owed on the PC:**
  - the game's pane. Target 5.1 still names an opaque Default Lit pane with the room's colour in its base colour, while the kit carries nets, curtains and a room card behind it. One PC realization must be chosen and checked (OWED-01).
  - Lumen's reflections, the street cube and the night exposure (OWED-06, OWED-07);
  - the rooms at the target's 128 samples (OWED-04).
