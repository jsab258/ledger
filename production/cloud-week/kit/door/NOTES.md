# Front door (kit piece 3.1), try 1: build notes

8 October 2026, cloud week 42. Built by script from `production/cloud-week/targets/front-door/target.json` (T1 the terrace four-panel door, F1 the side door to a flat over a shop). The brick context for the review renders also takes the target review's plinth-return numbers (TARGET-REVIEW.md, re-review try 2), as DECISIONS.md of 8 October says: the wall is the wall kit's, so it is never in the .glb. Nothing committed or pushed; the target is untouched.

## Files

| File | What |
|---|---|
| `build_door.py` | builds either variant from target.json; paint colour is a parameter (`--door-colour black\|dark_green\|maroon\|navy\|brown\|red`, default black for T1 and dark green for F1; `--frame-colour white\|cream`) |
| `check_door.py` | cuts the built mesh where `target_drawing.py` draws it and runs the target's checks; writes `checks/check_v1.json` |
| `door_context.py`, `render_door.py`, `views_T1.json`, `views_F1.json` | the review wall (brick, buff quoins, arch, plinth with its returns) and the render step (which calls `../tools/review_render.py`) |
| `checks/check_v1.json` | the check's result, every row |
| `build/` | the parts as `.npz` for the check (git-ignored; `build_door.py` rewrites it) |
| `production/assets/cloud-week/door/door_T1.glb`, `door_F1.glb` | the models |
| `production/previews/cloud-week/door/door-<T1\|F1>-<view>-v1-2026-10-08.jpg` | reduced previews, each at most 1600 px and under 500 KB (this folder, `kit/door/` and `assets/cloud-week/door/` are in `.git/info/exclude`; `git add -f` when the unit changes state) |

Rebuild and re-check (about 5 s and 2 min): `/home/user/.bpyenv/bin/python build_door.py`, then `check_door.py`; the renders are `render_door.py` (about 6 minutes a view on four CPU cores at 64 samples).

## The models

| | T1 | F1 |
|---|---|---|
| triangles (counted in the file) | 6,788 | 12,098 |
| size | 306,944 bytes | 475,340 bytes |
| parts (glTF nodes) | 29 | 37 |
| materials | paint_black, paint_white, glass, brass, steel_dark, stone_step | paint_dark_green, paint_white, glass, brass, chrome_nickel, steel_dark, timber_threshold |

Metres, z up, scale 1, pivot at the base's centre on the ground (T1 x 441, z -318; F1 x 447.6, z -45 in the target's frame), the wall face at y = 0, the street toward -y. One UV set per part, cube projection at real scale (1 UV unit = 1 m). Smooth shading by angle (35 degrees) with the arrises kept sharp: in T1's .glb 3,116 of 3,125 edges above 40 degrees are split in the written normals and 614 of 614 curved moulding edges are smooth (F1 the same kind).

Parts, by the layer prefix the check reads (`frame_`, `glass_`, `leaf_`, `panel_`, `moulding_`, `iron_`, `stone_`):
- **Frame:** two jambs rebated out of the solid (stop and rebate), the head cut to the soffit's circle (T1) or flat at 2400 (F1), the weathered transom (moulded nose, face, slope, glass shelf, rebate) with its ends splayed at 45 degrees, the glazing bead (T1) or putty fillet (F1) as one mitred sweep, F1's two 5 x 2.5 stop beads. The glass is 3 mm in 4 mm slots in jambs, head and transom.
- **Leaf:** ONE solid for stiles, rails and muntin (a slab minus the four panel openings and their 12.7 grooves), four flat panels floating in the grooves, four bolection sweeps outside and four single sweeps inside (mitred, one closed ring each), and for T1 the lock-rail band and the weatherboard from the target's drawn profiles.
- **Ironmongery:** letter plate (framed back, sloped rim, aperture, dished flap with a lifting lip; F1 adds four slotted screws), cylinder lock (T1 one turned body: bevelled collar, dark gap ring, plug with its 3 x 9 keyway; F1 knurled 12-serration collar and a plug with a horizontal keyway), the keep with its 8 x 50 slot. F1 also has the turned centre knob (five V-cut rings, brass cap) in its dished rose, and the plugged keyhole (recess, dark iron blank, small brass plug).
- **Setting:** T1 threshold (r 18 nose, horns 112 into the brick each side), recessed riser, and the step: a full half-round r 45 nose over a 20 undercut, plan corners r 40, ends stepped back to y -60 for the plinth. F1 a rounded 70 mm sill, 45 above the paving.

How the faults the lab's reviews found are met: no overlapping coplanar faces (mouldings, band, weatherboard, beads and hardware stand 0.3 to 0.5 mm into what they sit on; only butt joints meet face to face and those faces are opposite-facing and hidden); the jambs stand on the sill alike at both feet with no step; the plate has a rim, aperture and flap, the lock has a collar, gap ring, plug and keyway, F1 has a turned knob in a rose; every outline the target gives as points is smoothed where it is a curve (short segments, small turns) and kept sharp where it is an arris, then shaded smooth by angle, so mouldings are not faceted; the band and weatherboard are the drawn profiles (crests, coves, a flat square underside, a rolled top).

## The check: `checks/check_v1.json`

| | required checks run | passed | failed |
|---|---|---|---|
| T1 | 158 | 158 | none |
| F1 | 109 | 109 | none |

Pass rule as the brief and target say: IoU >= 0.97, outline p95 <= 2 mm, worst <= 6 mm for the drawings; profiles p95 <= 1.5, worst <= 3; each dimension within its check's own tolerance. The drawing comparisons, at 0.5 mm a pixel:

- **A1 front view, by layer (frame, glass, leaf, panel, moulding):** IoU 0.982 to 0.995, p95 at most 1.0 mm, worst at most 1.5 mm, both variants. Stone and iron, which the target also draws, are compared as extras and pass.
- **A2 / A3 every horizontal and vertical section the drawing gives (all joinery layers together):** IoU 0.994 to 0.998, p95 0.5, worst at most 3.0 mm (T1 1.4).
- **A4 profiles (bolection, band, weatherboard, transom front, bead, threshold, step tread, knob; plinth on the wall):** p95 at most 0.7, worst at most 2.0.
- **B to I:** all the dimension, edge, transom, band, weatherboard, ironmongery, step, setting and surface checks pass on the mesh. For T1 the arch, quoin and plinth checks (G7-G12, Q1-Q3, L1-L5) are run on the review wall (below), since the wall is not in the .glb. The .glb itself is read for the shading normals, materials, UV sets and bounds.

**Extras that do not pass** (three each, not required by A1-A3, which name the joinery layers): the iron sections at the plate (IoU 0.73, p95 1.4, worst 1.5), at the lock (T1 p95 2.0 worst 3.0; F1 p95 2.5 worst 3.5) and along the muntin (IoU 0.49, p95 1.5, worst 2.5). They are 2 to 6 mm thick shapes at 0.5 mm a pixel, and the differences are mine on purpose: the flap is dished 3 mm as the target's text says while its drawing is a flat 2.6 mm slab (I centre the dish on the drawn plane, so no point is more than 1.5 mm out), and the plug runs 2.3 mm deeper than the drawing so the lock is not floating in its bore.

**Covered, not measured here:** G12, H1 and H2 are the photographs' tests, made on the drawing by the target's own `self_check.py` (303 of 304); the model equals that drawing (above, and `CTX:buff_elevation` for the wall: IoU 0.996, worst 1.0 mm).

## Where the target contradicts itself, and which side the check took (`adaptations` in the json)

1. **The head's height.** The drawing's vertical sections draw the head 101.6 tall (top 2371.2; F1 2441.2) but its elevation, `frame.head_section_mm.top_edge`, B16, B17 and G8 cut it to the soffit (T1 2340 at the crown, 2322 at the ends; F1 2400). Built cut; the section comparison clips the drawn head at the soffit's height at the cut.
2. **`section_h_transom` at z 1955.6 (T1)** draws the transom back to y 241.3, but its own vertical profile has nothing behind y 188.3 below z 1959.6 (the leaf's head sits in that rebate), and draws no leaf where the leaf's top (1958) reaches the cut. Built to the vertical profile; the drawing is clipped at y 188.3 and compared with the frame layer alone.
3. **The tread's fall.** The drawing leaves a 6.6 mm strip between the tread's front top and the riser's foot; seen square-on the sloping top covers it. The strip is filled in the drawing for the stone comparison.
4. **A4 transom front** closes the polygon as a plain 127 x height block behind the moulded front; compared for y < 19 only. **A4 step tread** stops at the riser's face; compared in front of it.
5. **F7 for F1** says x 903.0, z 962.0 (the 944-bay values); target.json's own F1 keep is x 878.6, z 925.7 to 998.3 (TARGET.md section 2, fault 3). Built and measured to target.json.
6. **I5 against G2.** I5: no part beyond the frame's 975.2 by more than 5 mm; G2: the threshold runs 112 into the brick each side (65 beyond the frame). G2 wins; the threshold is the one exception.
7. **L3 and L5** (T1): the target still says 'nothing of the plinth in the clear opening'; the review replaces it with returns 70 +-15 wide into the doorway. The wall follows the review.
8. **I1 'no coplanar overlapping faces'** is measured as the lab's hatching: faces of different parts coplanar within 0.1 mm, facing the same way, overlapping by more than 1 mm2: none (T1 and F1). Opposite-facing faces where frame members butt (263 for T1, 303 for F1) are counted in the json and are hidden.
9. **C2 'the jamb face's normals within 3 degrees'** is measured on the front faces; the target's own 1 mm eases (two per jamb, 2.8% of its width) are separate 45 degree faces.
10. **The optional house numerals** are in the drawing (present = 'optional') but not built (F9: absent unless the town gives a number); they are left out of every comparison. The photograph's keyhole and the plate's aperture are painted as iron in the drawing, a recess and a slot in the model: masked in the leaf comparison, documented in the json.

## Judgements the target left to me

Numbers target.json does not give, taken from the section polygons `target_drawing.py` draws (the check measures against them): the inside single moulding's section (4, 10/6, 16/4 of its 22 wide), the letter plate's 2 x 1 chamfer and sloped rim (the text says a 45 degree chamfer; the drawing is a 2 mm rise over 12; I followed the drawing), the flap's 1 mm clearances, 2 mm hinge gap and 2.6 thickness, the collar's 4 mm flange, and F1's stop-bead section points.

Mine, with no number in the target:
- The leaf's framing is one solid; the panels have 0.1 mm of clearance in their grooves (1.6 mm at the sides, the target's play) and so touch nothing.
- Mouldings, band, weatherboard, bead, plate and the rest stand 0.3 to 0.5 mm into what they sit on; the jamb feet go 0.5 mm into the sill (C3 'foot at z 0 +-1').
- Bevels: frame 1 mm and leaf 1.5 mm (the target's eases), as a chamfer; the leaf's on its twelve outer edges only, so rail and stile meet in a closed joint; stone 2 mm (F1 sill 1.5); the keep is left square.
- Ironmongery not drawn in detail: the lock's keyway depth (3 mm), the F1 collar's serrations (12 grooves 1.4 deep), the knob's V-cut rings (1.5 deep, 2.6 wide) and rose (a dished ring, r 31 to 38, let 3 mm into the rail), the keyhole recess's shape (a round top 23 wide over a narrow slot, 32 high, 2 deep) with a dark iron blank and a 9 mm brass plug, F1's four screws (4 mm, 7.5 and 8 mm in from the plate's edges), the keep's slot depth.
- F1's sill runs under the whole frame (x -52.6 to 947.8) so the jambs stand on it; the drawing's plan stops it at the opening. F1's stop beads run from the sill to the transom's underside.
- Glass: 0.4 mm of clearance in every slot; transmission 1.0, IOR 1.5, base colour (121, 131, 139).
- Paint roughness is the target's 'new' 0.35 (wear masks add the 1990 roughness in the engine); every colour is the target's sRGB.
- Hinges: none built (they are inside, optional); no wear, no chips.

## The review wall (`door_context.py`, never in the .glb)

Red brick wall 342.9 thick, the reveal 114.3 deep and the check behind it for the frame, running 40 m each way so no end shows from the low view. Ten buff quoin blocks of three courses a side, long and short alternating, both sides in step (Q1-Q3 pass on the built blocks). A 13-brick segmental arch with radial joints, concentric extrados and dark recessed joints (G7, G9, G11 pass). The plinth: 60 proud, a 45 degree splayed top course to the wall face at z 12, and, from the review, returns 70 wide into the doorway on both sides (inner faces at x 70 and 812, from the tread's top to z 12, the splay mitred round the corner), so the threshold and riser show 742 between them. F1: painted-render pilaster returns and a plain face above the head. The courses (77 gauge, 10 mm joints struck 2 back, splay bricks 65 at a 75 pitch) are the brick shader's, not geometry. The doorway is closed behind by a lit grey board so the fanlight reads as glass; the pavement is review_render's own.

The wall is cut the same way as the door: its quoins and arch equal the drawing (IoU 0.996, worst 1.0 mm), its plinth splay equals the drawing's section (worst 0.1 mm), the review's returns and visible threshold length (742) are measured. Its own faces (`I1:context`, an extra): 22 same-facing coplanar overlaps, all inside the arch ring between a brick and its dark joint backing, hidden; nothing the camera sees.

## Renders

`render_door.py`, which saves a scene (the .glb as built plus the wall) and calls `review_render.py` with `views_T1.json` / `views_F1.json`: front (orthographic elevation, 4.0 m wide for T1), street (three-quarter from 3.5 m out and 2 m along, eye height 1.6 m), close (the lock rail and ironmongery from 1.2 m), low (along the street from 7 m along and 2.7 m out, 1.6 m high, about 20 degrees to the wall), and three extras (front_head, front_foot, close_plate). 1600 x 1200, 64 samples, Cycles on the CPU, `LEDGER_REVIEW_HDRI=/home/user/cache/hdri/bethnal_green_entrance_2k.hdr`; the context is review_render's `street` (its pavement) with this script's own wall in the scene instead of its plain wall plane. Full-size PNGs in `/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/door-build/v1/{T1,F1}/` (front, street, close, low, front_head, front_foot, close_plate; the scene files `scene_T1.blend`, `scene_F1.blend` are beside them); the reduced previews (14 JPEG, 43 to 310 KB, 1600 x 1200) are in `production/previews/cloud-week/door/`.

## Limits

- The tread's ends step back to y -60 beside the plinth (target L4); on its own the tread has a notch each end that the plinth fills.
- The house numerals, hinges and wear are not built.
- The previews are judged against photographs the reviewer can read in `production/previews/cloud-week/refs/front-door/`; this cloud cannot reach the source pages.
