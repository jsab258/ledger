FAIL

# Kerbs and covers (unit 3.7), STREET view, review v1 (fresh reviewer, 12 October 2026)

Judged: `street.png` (1600 x 1200, camera (-0.8, 2.9, 1.6) to (0.6, 0, 0.05), lens 30), against the photographs listed at the end, then the target. I read the build notes only after forming this view. To find the causes I measured `review_scene.glb` and the kit .glb files with ray-casts, and projected scene points into the picture: the grate's corners land on the black rectangle and the kerb joint at x 0.082 lands on the joint in the picture, so the image positions below are exact.

**In short:** the kerb itself reads right. This view still fails, because at standing distance a player would see three things no real street shows: a gully grate that is a solid black slab, a channel with no setts in it, and a hole in the kerb line. All three come from the review composition and the render setup, not from the kit pieces. The kit's own grate has its eight slots and bars, and the setts are in the scene with their joints. The fault is in how they were put together and lit for the picture. So it is the build's fault, with exact fixes below, and a re-render is needed before this view can pass. The covers are almost entirely out of frame: this view cannot judge them.

## Faults, worst first

1. **The gully grate is a solid slab with no bars or slots** (centre-left, image x 590 to 792, y 598 to 678). The far half is a flat dark-grey plate and the near half is pure black (RGB about 1).
   - *Photographs:* urban_street_03 (gully-grate ortho, crossover-top ortho, target-on-photo) shows eight dark slots across the channel with rust-brown bars, about half iron and half slot. That is the grate's whole character, and at 3.3 m it would be plain to see (a 25 mm bar is about 10 px here).
   - *Cause (build, composition):* in `review_scene.glb` the object `grate` has 8 vertices: a plain box 440 x 290 x 45. The pot is a solid box too. `gully_grate_A.glb` itself is right: a ray-cast across it finds eight 26 mm slots and 25 mm bars over the pot at -330. The `Shift` wrapper used by `piece_review` moves only the meshes passed to `add`. The boolean cutters in `grate_plate` and `gully_pot` stay at the origin, so in the composition they cut nothing. The stud cover's `lid_leaves` is reduced the same way (12 vertices against 180 in the kit), so its diagonal joint and keyholes are lost too.
   - *Cause of the pure black:* the near half of the grate (y 204 to 380) sits inside the `ground_road` box, with its top on the road's top (both at z 6). The same happens to the round cover (the black sliver in the bottom-right corner, RGB 0.26).
   - *Exact fix:*
     - In `piece_review`, build each holed piece (gully A, stud cover, round cover) at the origin with plain `B`, then translate the finished objects. Or have `Shift` apply its offset to the boolean cutters as well.
     - Place the grate at dz 0, not 6: target 4.6 wants its top flush with the setts (z 0 +-3), and the scene has it 6 proud of them.
     - Cut `ground_road` around the grate (x 580 to 1020, y 204 to 380) and around the round cover's 690 frame.
     - Cut the setts and `mortar` out of the grate's footprint (x 580 to 1020, y 90 to 204), so the slots read black into the pot.

2. **The sett channel is invisible.** The channel reads as a flat, joint-less blue-grey strip, broken only by a few thin light dashes (the band along the kerb foot, image x 200 to 1600). A sampled line along each course shows no dark cross-joints at all.
   - *Photographs:* in every photograph, the sett joints are the main pattern of the channel at this distance: urban_street_03 kerb run and crossover ortho, St Albans 2022, Belfast 2016, and the setted street in Manchester 1991.
   - *Cause (build, render setup):* `render_kerbs.py` passes `--context street`. `review_render.py` line 111 then lays a 400 m dark plane (`ctx_pavement`) at z -0.5 mm. The setts' domed tops in the scene are at -0.3 to -7.5 mm and their mortar is at -8 mm, so the plane covers almost the whole channel. The light dashes are the few sett crowns that poke through it. The setts are there: one ray-cast run finds sett lengths of 119 to 207 and joints 12 wide, recessed 8. The notes' 12 October "pavement at z 0" fix is what now hides this kit's channel, whose top is z 0 and below.
   - *Exact fix:* in `render_kerbs.py`, pass `--context none`. The scene has its own road at z 6 and flags at z 110, so nothing needs a context ground. Re-render both views.

3. **A 245 mm hole in the kerb line where the granite run meets the concrete run, and an open slot behind the whole concrete stretch** (far left, image x about 180 to 210, y 440 to 470, and the dark line behind the bull-nosed kerbs).
   - *What is wrong:*
     - The last granite block ends at x 2.798 and the first concrete block starts at x 3.043.
     - The footway slab stops at y -170 (the granite's width), but the concrete kerb is only 125 wide. That leaves a 45 mm slot, open into the void, along x 3.04 to 6.73.
     - The flags (z 110) stand 15 mm above the concrete kerb's top (z 95), so the footway rises above its own kerb.
   - *Photographs:* a kerb line is continuous, with 8 mm joints (urban_street_03 run, St Albans, Balloon Street 1991). The flags never stand above the kerb top (every photograph, Birbeck included).
   - *Whose fault:* build (composition) for the gap and the slot. Target for the levels: 4.1 gives granite 115 and 4.2 gives concrete 95 for the same street, without saying how they meet in one run.
   - *Exact fix:*
     - Build: start the concrete run 8 mm after the last granite block (first concrete centre x 3263.5, pitch 923), and end the setts at x 2802. Lay the footway slab behind the concrete stretch from y -125.
     - Target: add a line to 4.2: "where a concrete stretch meets granite in one run, it is laid to the granite's line and top level (top z 115, the block raised 20 on its bed), joint 8; the flags run through at 110 and are cut to the concrete's back at y -125."
     - Until the target says so, raise the review scene's concrete blocks by dz 20.

## Narrow points for the builder (each has an exact fix; none fails the view alone)

- **All seven granite blocks are exactly 900 long** (`kerb_block(K, 900.0, ...)` in `piece_review`), so the joints fall in an even, precast-looking rhythm. Target 4.1 and photograph PM04 want random lengths, 750 to 1050 (0.75, 0.91 and 1.03 photographed), with no two neighbours within 20. *Fix:* draw the review run's lengths from that rule. For the engine, state whether the 900 block is scaled along x or shipped as length variants (for example 760, 830, 900, 970, 1040).
- **The setts are not truly broken-bond.** `setts_run` offsets course B's start by 40 to 90, then draws its lengths independently of course A. In the scene, 8 of 38 course-A joints have a course-B joint within 15 mm: straight joints running through both courses. The notes say "running bond". The photographs (urban_street_03 target-on-photo, St Albans three rows, Belfast 2016) show the joints broken. *Whose fault:* target 4.3 gives no bond rule, and the build follows it. *Fix:* in `setts_run`, redraw any course-B length whose joint would fall within 40 of a course-A joint. Add "joints of the two courses at least 40 apart" to target 4.3.
- **The granite end arris is a flat 10 mm chamfer, not R 10.** `bevel_ends` uses `segments=1`. At this distance every joint shows a light flat facet on both blocks, which reads slightly pillowed and precast. The dressed ends in the photographs are square, with small rounded or chipped arrises. *Fix:* use `segments=3` for the granite blocks.
- **The road slab overlaps the concrete channel's outer 51 mm.** `ground_road` starts at y 204 everywhere, but the concrete channel is 255 wide. *Fix:* start the road at y 255 along x 3.04 to 6.73.
- **The covers are out of frame.** The view is meant to show the covers, but only a sliver of the round cover appears, in the bottom-right corner. The stud cover is off the right edge, and the crossover (x 8 to 12.8 m) belongs to the close view. *Fix (composition):* put the round cover's centre at about (0.3, 1.3), which lands in the picture at about (640, 930), and the stud cover at about (1.5, -0.8), at about (665, 445). Then this view can judge the frames, studs and lugs.

## What is right

- **The granite kerb's section** reads as a dressed half-battered granite kerb at this distance: vertical foot, the set-back above it, the rounded top arris and the flat top. The proportion of a 115 upstand to a 170 top matches the urban_street_03 kerb run and the St Albans kerb. The joints are narrow, open and dark, as the photographs show (no mortar fillet). The top sits 5 above the flags. The kerb stands on the channel line with nothing floating.
- **The concrete bull-nosed kerb** at the far left has the full rounded front of the Birbeck photograph.
- **The grate's footprint and placement are right:** a 440 x 290 rectangle, long side along the kerb, 90 off the kerb foot and mostly in the carriageway, as on urban_street_03.
- **The kit pieces themselves, checked by ray-cast, are sound for this view's needs:**
  - `gully_grate_A.glb` has eight slots 26 mm wide, 25 mm bars and the black pot under them, about half iron as photographed.
  - The channel setts are 119 to 207 long, with 12 mm joints recessed 8 into dark mortar.
  - Nothing carries lettering.

  Once faults 1 to 3 are fixed in the composition and render, I expect this view to pass on the kerb and channel. The covers still need to be brought into frame.

## Photographs judged against

| Photograph | Page | Taken | Author | Licence | What it shows |
|---|---|---|---|---|---|
| Manchester: Balloon Street | https://www.geograph.org.uk/photo/1644841 | 24 August 1991 | Dr Neil Clifton | CC BY-SA 2.0 | A setted street in the old quarter, with a continuous granite kerb line and tight joints |
| Gamble Street, Belfast (1990) | https://www.geograph.org.uk/photo/2638421 | 27 May 1990 | Albert Bridge | CC BY-SA 2.0 | A harbour-side street off Donegall Quay: a continuous kerb line, the kerb top above the footway, a dropped crossing |
| Channel, Upper Heath Road, St Albans | https://www.geograph.org.uk/photo/7380232 | 15 November 2022 | Robin Stott | CC BY-SA 2.0 | A standing view like this one: a stone kerb with tight joints and a sett channel in broken bond, the joints legible at this distance |
| Granite kerbstone and setts, Belfast (October 2016) | https://www.geograph.org.uk/photo/5163333 | 21 October 2016 | Albert Bridge | CC BY-SA 2.0 | Close: a granite kerb top and a sett channel with dark, deep joints |
| Poly Haven urban_street_03 | https://polyhaven.com/a/urban_street_03 | 7 September 2019 | Andreas Mischok | CC0 | Kerb run, gully-grate ortho, crossover-top ortho, target-on-photo (the repository previews) |
| Poly Haven birbeck_street_underpass | https://polyhaven.com/a/birbeck_street_underpass | 18 August 2019 | Andreas Mischok | CC0 | Concrete bull-nosed kerb |

The St Albans and Belfast 2016 photographs are later than the period, but they show the same objects: Victorian stone kerbs and sett channels laid long before 1990 and kept unchanged. The St Albans caption names the stones (a sarsen kerb and granodiorite setts). The two Poly Haven photographs are 2019, and the target says why each object is the same in 1990.

Unreached: Wikimedia Commons answered 429 to the one search I sent. Nothing was taken from it.
