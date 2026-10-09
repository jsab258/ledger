# Front door (kit piece 3.1), try 2: build notes

9 October 2026, cloud week 42. Built by script from `production/cloud-week/targets/front-door/target.json` (T1 the terrace four-panel door, F1 the side door to a flat over a shop), with the fifteen departures below, each a number the photographs set against the target's own (the photographs-win rule). Try 1 (8 October) went to six fresh reviewers (`REVIEW-v1-*.md`: T1 street, low PASS; T1 close, front FAIL; F1 street, close PASS); this is try 2, the last under the two-tries rule. The brick context for the review renders also takes the target review's plinth-return numbers (TARGET-REVIEW.md, re-review try 2), as DECISIONS.md of 8 October says: the wall is the wall kit's, so it is never in the .glb. Nothing committed or pushed; the target is untouched.

## Files

| File | What |
|---|---|
| `departures.py` | the departures: `apply(T)` copies target.json and writes each photographs-win number into the copy; the builder and the check both read the copy, so every other check still measures against the target and each departure is one named number |
| `build_door.py` | builds either variant from the amended target; paint colour is a parameter (`--door-colour black\|dark_green\|maroon\|navy\|brown\|red`, default black for T1 and dark green for F1; `--frame-colour white\|cream`) |
| `check_door.py` | cuts the built mesh where `target_drawing.py` draws it (drawn from the same amended copy) and runs the target's checks; writes `checks/check_v2.json` (`--version 2`) |
| `door_context.py`, `render_door.py`, `views_T1.json`, `views_F1.json` | the review wall (brick, buff quoins, arch, plinth with its returns; F1's pilaster), the dark closing faces behind the door, and the render step (which calls `../tools/review_render.py`) |
| `checks/check_v1.json`, `checks/check_v2.json` | the check's results, every row |
| `build/` | the parts as `.npz` for the check (git-ignored; `build_door.py` rewrites it) |
| `production/assets/cloud-week/door/door_T1.glb`, `door_F1.glb` | the models (try 2 replaces try 1's in place) |
| `production/previews/cloud-week/door/door-<T1\|F1>-<view>-v2-2026-10-09.jpg` | reduced previews, each at most 1600 px and under 500 KB (this folder, `kit/door/` and `assets/cloud-week/door/` are in `.git/info/exclude`; `git add -f` when the unit changes state) |

Rebuild and re-check (about 5 s and 2 min): `/home/user/.bpyenv/bin/python build_door.py`, then `check_door.py --version 2`; the renders are `render_door.py --out <dir> --version 2 --date 2026-10-09` (about 5 minutes a view on four CPU cores at 64 samples).

## The models

| | T1 | F1 |
|---|---|---|
| triangles (counted in the file) | 9,898 (try 1: 6,788) | 13,824 (12,098) |
| size | 396,940 bytes (306,944) | 540,000 bytes (475,340) |
| materials | paint_black, paint_white, glass, brass, steel_dark, stone_step | paint_dark_green, paint_white, glass, brass, chrome_nickel, steel_dark, timber_threshold |

Metres, z up, scale 1, pivot at the base's centre on the ground (T1 x 441, z -318; F1 x 447.6, z -45 in the target's frame), the wall face at y = 0, the street toward -y. One UV set per part, cube projection at real scale (1 UV unit = 1 m). Smooth shading by angle (35 degrees) with the arrises kept sharp: in T1's .glb 3,543 of 3,553 edges above 40 degrees are split in the written normals and 610 of 610 curved moulding edges are smooth (F1 4,777 of 4,782 and 464 of 464).

Parts, by the layer prefix the check reads (`frame_`, `glass_`, `leaf_`, `panel_`, `moulding_`, `iron_`, `stone_`):
- **Frame:** two jambs rebated out of the solid (stop and rebate), the head cut to the soffit's circle (T1) or flat at 2400 (F1), the weathered transom, the glazing bead (T1) or putty fillet (F1), F1's two 5 x 2.5 stop beads. The glass is 3 mm in 4 mm slots in jambs, head and transom.
- **Leaf:** ONE solid for stiles, rails and muntin (a slab minus the four panel openings and their 12.7 grooves) with the **joint lines cut in it** (below), four flat panels floating in the grooves, four bolection sweeps outside and four single sweeps inside (mitred, one closed ring each), and for T1 the lock-rail band and the weatherboard.
- **Ironmongery:** letter plate (framed back, 45 degree rim chamfer, aperture, dished flap with a lifting lip; F1 adds the flap's two pivot bosses), cylinder lock (a collar standing 5 proud: T1 one turned body with a rounded collar, dark gap ring and plug; F1 a collar of 8 rounded scallops round its plug; a vertical 3 x 9 keyway in both), T1's bell push on the right jamb's stop (F1 has no jamb fitting). F1 also has the turned centre knob (five V-cut rings, brass cap) in its dished rose, and the plugged keyhole (round head over a parallel slot, dark recess, pale blank in the slot).
- **Setting:** T1 threshold (r 18 nose, horns 112 into the brick each side), recessed riser, and the step as one loft (below). F1 a rounded 70 mm sill, 45 above the paving, its front 80 mm in front of the leaf.

## What try 2 changed, per fault

| Fault (reviewer) | Fix |
|---|---|
| Cylinder lock a flat coin (T1 close FAIL) | collar 5.0 mm proud (T1: flat annulus with a 3 mm round on its outer edge, small round inside, plug face 0.6 behind it; F1: ring of 8 rounded scallops, front edge rounded 1.2 mm, plug 1.0 behind); the keyway is vertical on both and is cut from in front of the plug's face, 3 x 9 mm, down to 2 mm behind the leaf's face |
| Weatherboard a near-vertical strip (T1 front FAIL) | bull-nosed lower arris at 26 proud, a plain face sloping up and back at 30 degrees from the vertical (z 8 to 44), a cove at z 52, a rounded top roll of radius 10.5 falling to the door at z 80 |
| Step cut off square at both ends (T1 front FAIL) | the tread is a loft of 23 horizontal rings, each the plan outline drawn in by the nose's section at that height, so the half-round nose and its undercut run round both ends; plan corner 47, nose 42, tread x -48 to 930 (the target: nose 45, corner 40, x -39 to 921, along the front only) |
| Lock-rail band three thin reeds (T1 front FAIL) | broad lit rolls, crests at z 12, 36 and 62, two creases at z 26 and 52 only 2.6 mm deep (the target's coves were 7 mm) |
| Moulding width 41-50 against 36 | T1 46, F1 43 |
| Plate rim, screws | the rim flat at 6 proud, then a true 45 degree chamfer, 3 x 3, down to the backplate's 3 mm edge; F1's four corner screws gone, two pivot bosses (8 mm, 2.5 above the rim) at the flap's hinge ends |
| F1 keyhole | round head 15 mm over a parallel slot 8 mm wide, 32 high, the pale (chrome) blank filling the slot, the head dark |
| F1 jamb keep | removed; T1's becomes a period bell push: dark oblong back 22 x 72.6, round brass bezel 17 mm and round dark button 11 mm |
| F1 sill 188 in front of the leaf | the sill's front at y 108.3, 80 mm in front of the leaf (and 6 in front of the jambs); the review pilaster's notch for the sill's ends now starts behind it |
| Joints closed | 0.8 wide, 0.8 deep grooves along both stiles' inner edges on each of the three rails and across the muntin at each of its four ends; they stop 5 mm short of the openings (the moulding's lap hides that) and 3 mm short of the leaf's outer arris |
| Lit interior through the gaps and the fanlight | review wall: a dark closing slab right behind the frame, up to the transom's top (so the 10 mm foot gap, the 1.6 mm margins and the plate's slot show dark), and above it a dark hall (five faces, 2.2 m deep, open at the fanlight); matt (26, 24, 22), not emissive (v1's emissive grey board is gone) |

## The departures from target.json (`departures.py`; each is in the check's `adaptations` too)

Photographs: P1 `door-photo-01-teignmouth-four-panel-red.jpg` (480 x 640, 5.15 to 5.19 mm a pixel on the door plane), P2 `door-photo-02-tottenham-six-panel-black.jpg` (675 x 1200, 2.317 mm a pixel), measured on the preview copies in `production/previews/cloud-week/refs/front-door/`.

- **D1 collar stands 5.0 mm proud (T1 was 1.5, F1 2.0).** Method: a radial luminance profile about each collar's centre. P2, centre (488, 495): the collar's bright rim is 8.2 px (19 mm) in radius and outside it runs a dark ring 2 px wide all round, 2 x 2.317 = 4.6 mm. P1, centre (258.75, 290.3): a bright crescent above (rows 286-288, 142-153 against the door's 110-118) and a dark one below (row 293, 62-92), each about 1 px, 5.15 mm. A contact shadow under overcast light is about as wide as the projection it comes from, so 5.0 mm, uncertainty about 2 mm (the two photographs agree to 0.4 mm). The collar's rounded edge is what turns the crescents.
- **D2 F1's keyway vertical, 3 x 9 mm** (the target said horizontal). P2 rows 497-500, x 488-489: a dark upright streak 1-2 px by 4 px inside the bright plug.
- **D3 F1's collar 8 rounded scallops about 2.4 mm deep** (the target: 12 serrations, built in try 1 as V-notches). P2's 5x crop of the collar: about 8 rounded lobes, the rim catching light on its upper left.
- **D4 weatherboard face at 30 degrees** (the target: a near-vertical belly 22-26 proud from z 6 to z 50). P1 x 145-175: rows 520-527 (z 9 to 49), the main face, mean 134 against 78 for the flat leaf face above the board (rows 505-513): 1.7 times in the picture's values, about 3 times in linear light; under it the lower arris (rows 528-529), above it the hollow (rows 518-519, z 56) and the lit top roll (rows 514-517, z 62-77). A face that bright takes the sky: its normal tilts up. 30 degrees is mine from that; the max projection (26) and the 80 mm height are the target's.
- **D5 step ends** as above. P1 x 87-95 and 283-291, rows 562-600: the lit nose and its dark undercut roll round both ends. The end overhang beyond each reveal must hold the whole round, so the tread is 9 mm wider each side (target.json's width 960 +-25 and overhang 39 +-20 both still hold: 978 and 48); the radius 42 is inside the target's 45 +-15. The top still falls 6.6 mm to the front (a shear of the loft, none at the ground) and is two planar faces, split on the riser's face line.
- **D6 band as above.** P1 x 145-175, rows 363.5-377.5: lit across its whole height; the creases (rows 367-369 and 372-373) dip only to 0.7 of its brightest and stay twice the flat leaf.
- **D7 T1 mouldings 46 mm on the face (target 36), D8 F1 43 mm (target 42);** the section's d values scaled by 46/36 and 43/42, the heights as they were. P1, a column through the upper-left panel's left moulding (5.19 mm a pixel): outer crease col 133, nose highlight 135-136, cove 137-140, field from 141-144, so about 9 px = 46-47 mm; the four mouldings read 9-10 px between their dark lines (47-52 mm with the occlusion lines, 41 +-7 without), and three reviewers read 41-50: 46 is the middle. P2: 18.5 px x 2.317 = 43 mm.
- **D9 plate rim:** a flat at 6 mm from the aperture's edge, then the 45 degree chamfer the target's text asks for (the target_drawing section draws a 2 x 1 chamfer and a 10 degree rise; the drawing's iron section is an extra, not a pass test). P2 (plate x 293-376, rows 281-311): a bevelled frame lighter than its field.
- **D10 F1 plate pivots** (the target: four slotted screws at the rim's corners): P2's plate has two round bosses at the flap's ends, 3-4 px = about 8 mm, and nothing at the corners.
- **D11 F1 keyhole shape:** P2 5x crop centred (493, 447): a dark round head over a parallel slot holding a pale blank 3-4 px wide and 6 px high (8 x 14 mm); the target's 23 x 32 takes in the dark halo, so the recess is 15 head and 8 slot in a 32 height.
- **D12 F1 has no jamb fitting; D13 T1's is a bell push.** P2's right jamb at the keep's height (rows 515-547, x 508-530) is bare timber with the bead line only (the 'grey service box' the target meant is 1.33-1.51 m up and modern); P1 16x crop, x 271.9-276.25, rows 300.3-314.4: a dark upright oblong, 22 x 72.6, on the stop's face. A keep on the outside face of an inward-opening door's stop takes no bolt.
- **D14 F1's sill front at y 108.3** (80 mm in front of the leaf, target y 0 = 188). P2 x 300-400: the sill's top, from above, is rows 946-959 (13 px), its front rows 960-979 (19-20 px = 45 mm): the top shows two thirds as tall as the front, which for a camera 15 to 25 degrees above the sill's plane is 60 to 110 mm in front of the leaf (the coordinator's range 60-100); 80 is the middle. The camera's pitch is not known, so the photograph gives the range, not the number.
- **D15 joint grooves 0.8 x 0.8** (the target: 0.4 mm hairlines; the coordinator 0.5-1 mm). P2 rows about 648 and 733 across the muntins, x 313-353: thin dark lines where the muntin meets the rails.

## The check: `checks/check_v2.json`

| | required checks run | passed | failed |
|---|---|---|---|
| T1 | 162 | 162 | none |
| F1 | 108 | 108 | none |

Pass rule as the brief and target say: IoU >= 0.97, outline p95 <= 2 mm, worst <= 6 mm for the drawings; profiles p95 <= 1.5, worst <= 3; each dimension within its check's own tolerance. The drawing comparisons, at 0.5 mm a pixel, are drawn from the amended target:

- **A1 front view, by layer (frame, glass, leaf, panel, moulding):** IoU 0.984 to 0.995, p95 at most 1.0 mm, worst at most 2.8 mm, both variants.
- **A2 / A3 every horizontal and vertical section the drawing gives (all joinery layers together):** IoU 0.994 to 0.998, p95 0.5, worst at most 3.0 mm.
- **A4 profiles (bolection, band, weatherboard, transom front, glazing bead, threshold, step tread, knob; plinth on the wall):** p95 at most 0.63, worst at most 2.0.
- **B to I:** all the dimension, edge, transom, band, weatherboard, ironmongery, step, setting and surface checks pass on the mesh. For T1 the arch, quoin and plinth checks (G7-G12, Q1-Q3, L1-L5) are run on the review wall, since the wall is not in the .glb. The .glb itself is read for the shading normals, materials, UV sets and bounds.
- **Re-aimed at the departed numbers** (the check text says which): E3 (three crests, two creases 1 to 4 mm deep), W3 (lower arris >= 24, a straight face at 30 +-6 degrees from the vertical, a hollow >= 6 behind the roll, roll radius >= 8; measured 26, 30.0, straight to 0.0 mm, 2.5 against 14.7, 14.0), F5 (new: the collar's front 5.0 proud, the keyway 3.0 x 9.0 vertical), F7 (the bell push's back 22 x 72.6, a round button 11.2, no keep part), F8:keyhole, F1:pivots (two bosses, no screws), and G4/B10/G6 follow the amended numbers.

**Extras that do not pass** (three each, not required: A1-A3 name the joinery layers): the iron sections at the plate (IoU 0.68, p95 1.5, worst 2.0), at the lock (T1 IoU 0.92, p95 2.0, worst 6.5; F1 0.88, p95 2.0, worst 6.5) and along the muntin (IoU 0.47, p95 1.5, worst 2.5). They are 2 to 6 mm thick shapes at 0.5 mm a pixel, and the differences are mine on purpose or are the departures: the flap is dished 3 mm as the target's text says while its drawing is a flat slab, the plug runs deeper than the drawing so the lock is not floating in its bore, and the collar now stands 5 proud with a rounded edge while the drawing's collar is a rectangle of 1.5 or 2. The stone sections (tread) pass, which they did not before the tread's top faces were fixed (below).

**Covered, not measured here:** G12, H1 and H2 are the photographs' tests, made on the drawing by the target's own `self_check.py` (303 of 304); the model equals that drawing (above, and `CTX:buff_elevation` for the wall).

## Where the target contradicts itself, and which side the check took (`adaptations` in the json)

1. **The head's height.** The drawing's vertical sections draw the head 101.6 tall (top 2371.2; F1 2441.2) but its elevation, `frame.head_section_mm.top_edge`, B16, B17 and G8 cut it to the soffit (T1 2340 at the crown, 2322 at the ends; F1 2400). Built cut; the section comparison clips the drawn head at the soffit's height at the cut.
2. **`section_h_transom` at z 1955.6 (T1)** draws the transom back to y 241.3, but its own vertical profile has nothing behind y 188.3 below z 1959.6. Built to the vertical profile; the drawing is clipped at y 188.3.
3. **The tread's fall.** The drawing leaves a 6.6 mm strip between the tread's front top and the riser's foot; seen square-on the sloping top covers it. The strip is filled in the drawing for the stone comparison.
4. **A4 transom front** closes the polygon as a plain 127 x height block; compared for y < 19 only. **A4 step tread** stops at the riser's face; compared in front of it.
5. **F7 for F1** is gone (D12). It had said x 903.0, z 962.0 against target.json's own 878.6.
6. **I5 against G2.** G2 wins; the threshold's horns are the one part outside I5's 975.2 mm.
7. **L3 and L5** (T1): the target says 'nothing of the plinth in the clear opening'; the review replaces it with returns 70 +-15 wide. The wall follows the review.
8. **I1 'no coplanar overlapping faces'** is measured as the lab's hatching: faces of different parts coplanar within 0.1 mm, facing the same way, overlapping by more than 1 mm2: none (T1 and F1). Opposite-facing faces where frame members butt (309 T1, 348 F1) are hidden.
9. **C2 'the jamb face's normals within 3 degrees'** is measured on the front faces; the 1 mm eases are separate 45 degree faces.
10. **The optional house numerals** are not built and are left out of every comparison. The photograph's keyhole and the plate's aperture are painted as iron in the drawing, a recess and a slot in the model: masked in the leaf comparison.
11. **The joint grooves** (D15) are 0.8 mm: at 0.5 mm a pixel they are one or two pixels and cost the leaf comparison nothing.

## Judgements the target left to me

Numbers target.json does not give, taken from the section polygons `target_drawing.py` draws: the inside single moulding's section (4, 10/6, 16/4 of its 22 wide), the flap's 1 mm clearances, 2 mm hinge gap and 2.6 thickness, the collar's 4 mm flange, and F1's stop-bead section points.

Mine, with no number in the target:
- The leaf's framing is one solid; the panels have 0.1 mm of clearance in their grooves (1.6 mm at the sides, the target's play) and so touch nothing.
- Mouldings, band, weatherboard, bead, plate and the rest stand 0.3 to 0.5 mm into what they sit on; the jamb feet go 0.5 mm into the sill (C3 'foot at z 0 +-1').
- Bevels: frame 1 mm and leaf 1.5 mm (the target's eases), as a chamfer; the leaf's on its twelve outer edges only; stone 2 mm (F1 sill 1.5); F1's collar front edge rounded 1.2 mm.
- The lock's keyway depth (to 2 mm behind the leaf's face), the knob's V-cut rings (1.5 deep, 2.6 wide) and rose (a dished ring, r 31 to 38, let 3 mm into the rail), the bell push's build (back 3 proud, bezel 4.9, button 5.8, back's corners r 6), the pivot bosses' height and the keyhole blank's size.
- F1's sill runs under the whole frame (x -52.6 to 947.8) so the jambs stand on it; F1's stop beads run from the sill to the transom's underside.
- Glass: 0.4 mm of clearance in every slot; transmission 1.0, IOR 1.5, base colour (121, 131, 139). Paint roughness is the target's 'new' 0.35; every colour is the target's sRGB. Hinges, house numerals and wear are not built.
- The reviewers' remarks left to the engine's materials: P1's cylinder face reads a dull grey-olive (a darker finish than the plate), the bell push's back is mid-dark grey in P1 (here near black).

## The review wall (`door_context.py`, never in the .glb)

Red brick wall 342.9 thick, the reveal 114.3 deep and the check behind it for the frame, running 40 m each way. Ten buff quoin blocks of three courses a side, long and short alternating, both sides in step (Q1-Q3 pass). A 13-brick segmental arch with radial joints and dark recessed joints (G7, G9, G11 pass). The plinth: 60 proud, a 45 degree splayed top course to the wall face at z 12, and, from the review, returns 70 wide into the doorway (the threshold and riser show 742 between them). F1: painted-render pilaster returns (whole in front of the sill, notched for its ends behind it) and a plain face above the head. **Behind both: the dark closing slab and the dark hall** (above). Its own faces (`I1:context`, an extra): 22 same-facing coplanar overlaps, all inside the arch ring between a brick and its dark joint backing, hidden.

## Renders

`render_door.py` saves a scene (the .glb as built plus the wall) and calls `review_render.py` with the views: front (orthographic elevation), street (three-quarter from 3.5 m out and 2 m along, eye height 1.6 m), close (the lock rail and ironmongery from 1.2 m), low (along the street from 7 m along and 2.7 m out, 1.6 m high, about 20 degrees to the wall), and three extras (front_head, front_foot, close_plate). 1600 x 1200, 64 samples, Cycles on the CPU, `LEDGER_REVIEW_HDRI=/home/user/cache/hdri/bethnal_green_entrance_2k.hdr`; the context is review_render's `street` (its pavement) with this script's own wall in the scene. Full-size PNGs in `/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/door-build/v2/{T1,F1}/` (the scene files `scene_T1.blend`, `scene_F1.blend` beside them); the reduced previews (14 JPEG, each 1600 x 1200 and under 500 KB) are in `production/previews/cloud-week/door/` as `door-<V>-<view>-v2-2026-10-09.jpg`.

## Limits

- The tread's ends step back to y -60 beside the plinth (target L4): its side faces at the plinth are the plan outline's own.
- The house numerals, hinges and wear are not built.
- The dark hall is a render aid: in the engine whatever the scene holds behind the door shows through the foot gap, the margins and the plate's slot, so the scene wants its own dark hall behind a front door, or a water bar and a draught board.
- The previews are judged against photographs the reviewer can read in `production/previews/cloud-week/refs/front-door/`; this cloud cannot reach the source pages.
