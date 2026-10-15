# Pillar box (kit piece 3.6): build notes

12 October 2026, cloud week 42, built by the coordinating session from `production/cloud-week/targets/pillar-box/target.json` with the amendments of `targets/pillar-box/PHOTO-CHECK.md` (two dated Geograph photographs, CC BY-SA 2.0, 2009 and 2012, and the Letter Box Study Group's 48 inch circumference): `build_pillarbox.py` (about 10 s), `check_pillarbox.py` (62 of 62 in `checks/check_v1.json`) and `render_pillarbox.py` (the two review views).

**Built** (one model, `production/assets/cloud-week/pillar-box/pillar_box.glb`, 9,996 triangles, 287 KB; metres, z up, the axis at the origin on the footway surface, +y the front, a hidden skirt to z -150):

| Part | Material | What it is |
|---|---|---|
| base | paint_black | a straight black band, the body's diameter plus 4 a side (398), 300 high, a small chamfered collar to z 306; no splayed foot (PHOTO-CHECK 4) |
| body | paint_red | a cylinder 390 across to z 1342; a cove out to the cap rim 535 across (z 1362 to 1420, R6 top edge); a flat shelf to r 245, a short neck (the edge eased R2.5) and the dome rising 60 to z 1500; the slot cut through the front wall (250 x 45, R5 corners, centre z 1278, a pocket to y 60) |
| door | paint_red | a cylindrical panel 240 wide (a chord at the body), z 330 to 1180, 1 proud; a 3 x 3 joint groove round it cut in the body |
| hood | paint_red | the lip over the slot, 30 proud, z 1301 to 1333, a quarter of the way round (plus and minus 47 degrees), edges eased 1.5 |
| plate_frame, plate | paint_red, enamel_white | the collection plate's frame 168 x 100 at z 950, bezel 10, flat face 9 proud of the body at the axis, the enamel panel 148 x 80 sunk 2.4 in the recess (words are the engine's texture, the five allowed strings) |
| escutcheon | paint_red | a plate 36 across, 3 proud, at x 90, z 818 (the right of the door, opposite the joint side), with its 4 x 12 keyhole |

**Departures from the target, all from PHOTO-CHECK.md** (the photographs win): body 390 (the target 489), the straight base 300 high (a splayed 576 foot, 200 high), the cap rim 535 (560), the dome rising 60 (80), the slot 250 wide (320). The door's width, the plate frame and the lock position are the target's scaled 0.8 to the narrower body (300 to 240, 210 x 125 to 168 x 100, 112 to 90). The door's head stops at z 1180 so that the lettering band (z 1190 to 1230) stays clear of its joint. The hood's underside is 0.5 over the slot's ceiling so that no two faces share a plane. 96 sides to the lathe (the target's budget is 8,000 to 30,000 triangles).

**Not built, by the target's own rule:** the cypher, the crown, ROYAL MAIL or POST OFFICE, the maker's mark (the lettering band z 1190 to 1230 and the cypher disc 110 across at z 1088 on the door are flat and blank: canon owes the cypher), the capless Type K variant (not built in the target either), the wear (engine masks, unit 4.5: its black band follows the 300 base) and the plate's words (a texture).

**Type name:** the target calls the pattern Type A; the Letter Box Study Group calls the 48 inch size Type B (PHOTO-CHECK.md). The shape follows the photographs and the name is left as written.

**For the builder:** the front of the box faces the buildings (the east, shop side of Quay Street, +z in the scene file; the stand-in's slot is on the road side). The scene file's E4 stand-in (body 0.597, 1.612 high) is replaced by this mesh (total height 1.500, base 0.398, body 0.390, cap rim 0.535); its pivot is the axis at the footway. The target's gaps (0.612 m from the east lamp column's base, 0.312 m from the kerb's back, the axis 0.60 m behind the kerb) were measured to a 576 foot; the 398 base makes them about 0.70 m and 0.40 m.

## Try 2 (12 October, after REVIEW-v1-street.md: FAIL on two faults, both the target's and PHOTO-CHECK's; the build was faithful)

The first street review set five photographs (two Geograph pages given, three found: Rhayader 2011, Alresford 2012, Chester 2019; all CC BY-SA 2.0; none before 2009, so the 1990 plate is not shown) against the render. Applied as the review writes it (`build_pillarbox.py`, `check_pillarbox.py` 68 of 68 in `checks/check_v2.json`; v1's 62 of 62 stays beside it):

1. **The cap** (fault 1): the target's cove, shelf and neck dome read as a mushroom. Now, from the photographs (fractions of 1500): a **collar ring** (r 205, z 1350 to 1380, a ring 10 proud of the body, just over the slot's hood), a **deep concave flare** from the collar to the rim's lower edge at z 1440, the **rim band 1440 to 1485** (535 across, a small bead on its lower edge, R6 top edge), and a **low dome** rising 15 straight from just inside the rim's top bead (apex 1500). The hood's top (1333) stands 17 under the collar. The beaded (dentil) underside is a normal map.
2. **The collection plate** (fault 2): an **upright frame 130 x 240**, on the axis, its top at z 1210 (45 under the slot's bottom), bezel 10, enamel panel 110 x 220. The door's head rises to z 1235 (under the slot frame).
3. **The reserved areas move down** with the photographs (crown and cypher below the plate, the lettering below them): the cypher disc 110 across is now at z 620 and the lettering band, 230 x 40 (the door's width), at z 420, both flush and blank on the door; the target's z 1088 and 1210 are superseded (canon owes the cypher).
4. **Narrow points applied:** the lock on the **viewer's right** (x -90; with +y the front and z up the viewer's right is -x, so the target's frame line "+x is to the viewer's right" is mirrored and the first build followed it), an upright oblong escutcheon 100 x 40 with a small lever handle; a **frame round the slot** (10 wide, 3 proud) and a **sill** under it; the **base's top is a rolled R6**, meeting the body at z 297.7.
5. **Not built:** the small raised tablet (50 x 30, brass in one photograph) between the collar and the hood (the target has none; the gap is 17 mm: an engine decal if wanted), the cap rim's dentils, the deep box hood with cheeks of the two older patterns (the shallow lip is the pattern of three of the five photographs).

Triangles 15,958 (the target's 8,000 to 30,000). The hidden inner radii of the frame (195 - 2.5), the sill (195 - 3.5) and the hood (195 - 3) differ so that no two hidden faces share a plane.

## After the second street review (REVIEW-v2-street.md: PASS, four narrow points; applied, 12 October)

The street view of try 2 passed (eleven photographs of twelve boxes). Its four narrow points are applied where the exact fix is a size: the **slot frame** now has borders 22 wide standing 12 proud (a raised oblong about 300 x 110 over all; its bottom border is the sill, which is gone as a separate part; the door's head drops to z 1224 to make room), the **lock** stands 9 proud (the review: 8 to 10) with a **lever handle** 25 across and 18 proud, and nothing else changes (`check_v2.json`: 67 of 67). **Not applied:** the rim's dentils (a normal map on the band's upright face: about 60 blocks round, 16 wide and 20 tall at a pitch of 28, gaps 4 to 6 deep) and the small tablet frame above the slot (about 55 x 45, with a 40 x 30 window), which the review wants in all eleven boxes: the 17 mm between the hood's top and the collar is too little for it; an engine decal, or the hood's top lip lowered, is the builder's call.

**The review tool's ground (found by that review):** `tools/review_render.py` laid the pavement at the model's lowest vertex, so a buried skirt (this box's, the lamp posts', the kerbs' depth) showed above the ground: the first street picture showed the box 150 too tall with a black base 450 high. Fixed (the pavement is at z 0); the previews v2 of the pillar box are re-rendered.

## After the second close review (REVIEW-v2-close.md: PASS, four narrow points; applied, 12 October; this section's numbers are the current ones)

The close view passed. All four points are applied as the review writes them (`check_v3.json`: 71 of 71; 16,536 triangles, 474 KB; previews v3):

1. **The hood is the Elizabeth II pattern** (three of the five photographs: G1, P1, P2): a deep box 40 proud (30 before) with a face 46 high (z 1301 to 1347, its roof rising to the body at 1351, under the collar), cheeks at 50 degrees. The **tablet** is a new part, `tablet_frame`: a frame 55 x 38 standing 3 proud of the hood's face round a 40 x 28 window to the hood's own face (the cast words are the engine's texture; the window is a flush reserved area, like the cypher and the lettering band). The George VI pattern (a lip with a panel above it) was not used: the strip between the lip and the collar is 17, too little for a 40 high tablet, and the cap and the plate frame already follow the Elizabeth II photographs.
2. **The cap's rim band is 60 deep** (z 1425 to 1485) with an R8 round on its top edge and the R4 bead below; the flare runs 1380 to 1421 (collar 30, flare 41, rim 60). The dentils stay the engine's normal map (about 60 blocks round the band's face, 16 wide and 20 tall at a pitch of 28, 4 to 6 deep).
3. **The lock**: the escutcheon is 45 x 70 (9 proud) with a true keyhole cut through it, a round top 10 across over a slot 4 across, 20 high in all; the door's **grip** is its own part, `lock_grip` (70 across, 25 high, 25 proud, centred z 745, 73 under the escutcheon's centre). The earlier `lock_lever` is gone.
4. **The door is 300 wide** (the target's; its edges at 50 degrees from the front, the photographs' 45 to 50). The hood (50 degrees) and the slot frame (49) stand inside the door's width above it.

Nothing is left from the close review. Not built, as before: the cypher, the lettering and the maker's mark (flush areas), the plate's words, the dentils (a normal map), the wear. The nine parts are now ten: base, body, door, hood, tablet_frame, plate_frame, plate, escutcheon, slot_frame, lock_grip.
