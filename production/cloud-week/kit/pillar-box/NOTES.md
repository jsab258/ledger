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
