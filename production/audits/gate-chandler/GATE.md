# The chandler's, brought in the way the grocer's was: the gate (23 October 2026)

**The piece:** no. 13, the ship's chandler, east_chandler bay 0 (street x 40 to 46). It is the cloud's design: its front (a metal 1980s refit, navy paint, a tiled stallriser, a side door to a hall), its display, and its room painted as a picture. That team's street review passed it. Its close review failed it on one point: the two sou'westers read as builders' hard hats (production/cloud-week/kit/shop-windows/REVIEW-chandler-v1-close.md, F1).

**Before the gate:**
- **The hats rebuilt to that review's exact fix** (sw_goods_b.souwester_hung): an oblate crown on a band with no raised seams; a brim all round, sloping down, with the long neck flap at the back; chin ties knotted over the rail; a duller oilskin.
  - At the review's 60-degree tip they faced the street square and showed only a dome on a disc. They hang at 30 degrees, so their profile shows. Seen in a Blender render from the street side before any game picture.
- **Built on the PC:** assets, paper, front, display; the room at 128 samples (23 minutes).
- **The street:** CLOUD_FRONTS takes east_chandler bay 0.
  - The bay was the street's metal refit, and the switch to designed fronts skipped refit bays. Now a designed front takes a refit bay whole (terrace-front.py).
  - Its lit card gets a room (INTERIOR_PICTURE, its shop-room.py picture of 7 October, over which the game lays the cloud's). Self-test 175/175.
- **The lessons applied from the start:**
  - glass lettering cut out (--mask);
  - linings to the head and a head board (--raise, --head);
  - its tins smoothed by angle (--smooth; they came flat-shaded, as the grocer's did);
  - the window's light over the window alone, just behind the glass, its shadows kept with a larger bias;
  - no street grime.
- **Its shops-file entry:** card 40.35 to 45.65; display x 40.35 to 43.70; front at x 43.0; spill over the window at 42.025; lit at night, its door card CLOSED.

## Round 1 (F:/LedgerTools/gate/new/chandler-2026-10-23/r1)

- **Seen before review:** by day the shop door's glass reads a flat pale grey, the bright sky mirrored over a room kept dim by day; at night the buoy shows plainly through it. The design's street render shows the buoy by day. Left to the reviewers.
- **Across the road by day: FAIL**, on two faults.
  - **F1, a flat white veil** over the shop door's glass and the left half of the window, with a hard vertical edge between the hats (181 of 255, against 50 in the clear panes).
    - **The cause:** the chandler's window (street_glass_eg_bay6) and its doors' glass (eg_bay7) face the gap past the west row's end, the newsagent's gable then open sky (their stored pictures show it), and the street's glass takes its stored reflection at 2.5 times a true one by day, set for windows facing houses.
    - **Fix, try 1:** a per-pane day strength (unreal-look.json glass_cube_strength_by_mesh, read by StreetMeshes.h GlassCubeStrengthFor): these two panes take a true reflection, 1.0.
  - **F2, the hanging sign's wall plate** sat buried in the brick, the arm ending in bare brick.
    - **The cause:** the street's brick above the cornice stands 165 mm proud of the front's wall line there (measured in quay-street.glb); the plate was 0 to 8 mm out.
    - **Fix, try 1:** the plate set out 168 mm (sw_front.py PC_SIGN_MOUNT, as the ironmonger's 175).
  - Noted, outside the piece: a bright white wedge where the alley's ground should be, left of the chandler's pier (x 370 to 517, y 897 to 941). To be checked against the street's own pictures.
- **Square on by day: FAIL**, on two faults.
  - **F1, the two brass hurricane lamps drew see-through all over** (cap, tubes and tank, the bed showing through). The Poly Haven lantern's one material keeps only its globe clear by a map the glTF does not carry, so it came out transmission 1 everywhere.
    - **Fix, try 1:** the material made solid at the readying step (front_for_game.py SOLID_CLOTH), its globe as its picture paints it.
  - **F2, the sou'westers**, no longer hard hats, read as smooth, plastic domes, with no neck flap from the street and the ties meeting at the crown's top; the left one was bleached by the veil.
    - **Fix, try 2** (try 1 was the review's geometry at a 30-degree tip): hung as a shop hangs one on a hook by its ties, the crown to the street, the short front brim at the top and the long neck flap hanging down. The crown's four seams and the brim's four rows of stitching are drawn as flush lines of a darker oilskin (0.6 of its value, as the review asks). The brim is a little crumpled. The oilskin is duller (roughness 0.42).
- Every view retaken as r2 after the glass is baked again.

## Round 2 (F:/LedgerTools/gate/new/chandler-2026-10-23/r2)

- **Square on by day: FAIL**, on the hats alone.
  - **The lamps are fixed:** solid, they read as Feuerhand-type hurricane lamps (handle, hood, guard, clear globe, burner, tank). They are cream-white where the design's are galvanised: a narrow point (the lantern's own picture).
  - **The hats, set aside after two tries.**
    - The right one now reads as a yellow oilskin rain hat, made a sou'wester by its card.
    - The left one, washed cream by the sky's reflection over its pane, reads as a pith helmet: a smooth dome with four seams meeting at a point, in a round brim. Each crown also has a shading pinch at its top, like a helmet's vent.
    - **Next, research in another direction, not a third script:** a modelled or scanned oilskin sou'wester (its review found none CC0; the library's is a boonie hat), or a hat laid on the bed so its long flap shows.
    - Listed with the chandler's faults.
  - Still showing: the sky reflection over the left-centre pane, weaker than r1 (the rail behind the left hat 190,173,156 against 91,61,41 in the right pane).
