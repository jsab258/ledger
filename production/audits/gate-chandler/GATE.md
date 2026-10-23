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
- **Across the road by day: FAIL**, on F1 alone.
  - **F2 is fixed:** the plate sits on the brick face with its four bolts and carries the arm.
  - **F1 is weaker but still there:** an even grey sheet, 117 to 133 against 46 to 48 in the clear panes, with the same hard edge down the middle pane.
    - **Measured:** street_glass_eg_bay6 is the whole window and the shop door (street x 40.39 to 44.66); eg_bay7 is only the side door's fanlight. So the edge lies inside one pane's picture: the newsagent's gable reflected, and left of it the even overcast sky.
    - Open sky outshines a shop kept dim by day, as real glass does, but it hides the goods the design shows.
    - **Fix, try 2 (the last for this fault):** that pane reflects at 0.4 by day, below a true reflection, as games keep a window's goods readable. Every view retaken as r3.

## Round 3 (r3: the window's day reflection at 0.4)

- **Measured:** door glass 176, then 113, now 64; left pane 179, then 127, now 88; the clear panes about 59.
- **Square on by day: FAIL** on the hats alone. With the wash gone, both read as pith helmets crown-on (a round dome, four seams meeting at a peak, a stiff round brim, the flap only an off-centre brim). Each crown also has a shading pinch at its peak.
  - **Set aside, removed:** by the design's own rule for goods that read as another trade's (the grocer's tomatoes), the two hats and their card leave the window (sw_shops_chandler.py SOUWESTERS_SET_ASIDE) until a modelled or scanned oilskin hat is found. The rail stays for the rope.
  - **A narrow point fixed with it:** the blowlamp's card reads BLOWLAMP, the British trade's word, as two reviewers asked.
- Every view retaken as r4.
- **Across the road by day (r3): PASS.** F1 is gone: the door glass is 59 to 63 where r2 read 109 to 112, and the added light is about 4% of white in linear terms (19% in r2), what plain glass reflects from an overcast sky near normal incidence. The goods keep their colour, and the door reads as dark glass with a sheen, its buoy showing. No new fault.
  - Narrow points, not failing: the reflection's edge down the middle pane is now faint, under the listed stair-steps; the sheen reaches below eye level in the lower left pane and the door.

## Round 4 (r4: the hats set aside)

- **Square on by day (r4): PASS.** Where the hats were, the jackets' tops and the room's shelves show through their necks, with no cord, knot, hole or float left, and the rail clean. BLOWLAMP reads right. Nothing burns (max 247). No new fault.
- **From the left by day (r4): FAIL.** A white void 17 to 19 px wide at the foot of both doors (x 493 to 690, y 963 to 1135; mean 244, the sky's own value). It is present since r1, unseen until this view.
  - **The cause:** this recipe's footway stops at its frontage (5.125 m), and the cloud's front stands CLOUD_WALL_BEHIND_M (0.17 m) behind it. The metal refit drawn in this bay filled that strip with its own threshold and stall, which the cloud front replaces; at its doors nothing did.
  - **Fix, try 1:** where a designed front replaces a refit, the strip is paved flush with the footway (terrace-front.py cloud_footway_fill). Self-test 175/175. Street exported and imported, glass baked again, every view retaken as r5.
  - The rest of the view held up: the plate on the brick, the side door's hall through its fanlight, the room's dado level through door and window, nothing clipped.
  - Noted, the street's: hard tone steps in the brick right of the right pilaster (x 2147 and 2230 to 2245), the same in r1 and at night, likely the street's projected grime's edges.
- **From the right by day (r4): PASS.** The pilaster, console, sill and plinth meet the brick and the grocer's tight; the room's dado level sits on the horizon; nothing floats or burns. No new fault.
  - Narrow points: the hurricane lamps cream-white (the lantern's own picture; the design's grey came from its see-through material); a thin gap between the upper rail and the jackets' tops, as the design builds them; the jackets a little browner than the design.

## Round 5 (r5: the doors' strip paved)

- **Across the road by day (r5): PASS.** The hats, their strings, card and road reflections are gone cleanly, the jackets' necks showing as the design's own. The doors' feet are paved with no seam. The glass is as r3 (0.2 to 0.5 levels). No new fault.
- **From the left by day (r5): PASS.** The void is gone: in r4's box, near-white pixels fall from 2,202 to 180, all of them the alley wedge's tip. The new paving matches the slab beside it (69/61/52 against 67/59/51), with a joint line and no step, no flicker-prone overlap and no gap at either door. No new fault.
  - Noted, not new (since r1): a straight-edged grey veil down the near brick pier, from this camera only, akin to the smears on glass; and the alley wedge's 2 to 3 px tail under the shop's pier, to recheck when the alley is paved.
- **Across the road at night (r5): FAIL**, two faults.
  - **F1, the CLOSED card unreadable:** its letters about 30 to 35 on a ground of 22. Hung inside the door's glass with the lit shop behind it, the card's street face takes no light.
  - **F2, the shop door's lower glass black** (x 829 to 964, y 830 to 903). The design's M1 door is glazed from its bottom rail (0.198 m), and the room behind is a picture from 0.65 m up, so below it there is nothing to see. The design's own night render shows the same.
  - **Fix, try 1 for each:**
    - F2: the door takes a flat aluminium panel to the sill's line (0.60 m), with a mid rail, as the target's glazed-from rule asks of its timber and 1930s doors (sw_front.py PC_DOOR_KICK_MM; the target not edited). The street's glass in the door now starts at 0.594 m.
    - F1: the card takes the faint light the window's lamps and the lobby throw back: its own face as an emissive map, a fifth of the lit room's strength after dark, turned with the card (front "night_glow" on door_sign; VignetteShot.cpp keeps one material for the glow and the turn).
  - Every view retaken as r6.
- **Square on at night (r5): PASS.** The room lit warm and true behind the window; all eight cards read; the glass clear; the linings hide the room's edges; the tins round. No new fault.
  - The listed shortfall at its worst here: the window's light leaves the front row dark, not only under the goods (the left oil can 2 against 30 by day, the blowlamp 5 against 34, the compass dials 17 against 85; about a tenth of the window near-black). The design's night render has the oil cans and compasses lit. Listed, as the street's night-fill shortfall.
  - Narrow points: the white rope's upper arc clips to white; small orange glints above the jackets' strap tabs; a hard self-shadow notch on the tan rope.

## Round 6 (r6: the door's lower panel, the CLOSED card's glow)

- **Across the road at night (r6): PASS.** F1 is gone: the card reads CLOSED, its red about 92 and its letters about 150 (r5: 22 and 30 to 35), darker than the lit buoy beside it, with no halo. F2 is gone: the door's foot is a flat panel (8 to 17) in its frame, flush with the stiles, a rail line at its top; by day plain aluminium matching the frame. The door's reflection in the wet pavement evens out with it. Everything else that changed is sampling sparkle. No new fault.
  - Narrow points: the panel's thin left shadow line starts a little below its top; the door's hours lettering dark against the lit room, partly read; the side door and the hanging sign nearly lost in the dark.
- **From the left at night (r6): FAIL**, two faults (both already in r5's frame, which was not reviewed).
  - **F3, the shop door's glass black above its new panel** (x 632 to 716, y 628 to 916; 0 to 3 where the room through the window beside it is lit). At this slant the eye meets, through the door, the hall's wall that faces into the shop. The design paints that face as the room's walls (cream over the green dado), and in its renders it carries the room picture's wall; in the game nothing lit it at night.
  - **F4, the display's side lining by the door burned near white** (x 745 to 926, y 375 to 632; 236 to 244), brighter than the room's own tubes (208 to 213). The window's head lamp ended 0.375 m from it.
  - **Fix, try 1 for each:**
    - F3: the hall's shop-facing paints glow after dark as the lit room's own wall beside them: flat maps of its colours measured off the room's night picture (112, 98, 78 above the dado; 32, 46, 31 below), at the room's night brightness (0.7). The game's front glow now takes a list (VignetteShot.cpp), and the readying and wear scripts write several glows and flat colours.
    - F4: the head lamp narrowed from 2.6 to 2.2 m, its ends 0.575 m from each lining.
  - The worn front came in at round 7 (r7). Every view retaken as r8.
- **From the right at night (r7, the first with the wear): FAIL**, one fault.
  - **F5, a dark slab down the right of the shop door's glass, black at its foot** (x 435 to 620, y 170 to 1440; under 3 at x 480 to 619 from y 1060 down). At this slant the eye meets, through the door, the back of the display's side lining, painted as the room's walls; nothing lit it at night (about 34 against the room's 111 at the same heights). In r4 to r6 too.
  - **Fix, try 1:** that face takes a veneer, 1 mm off it, in the hall's two shop-facing paints, which glow after dark as the lit room's walls (sw_front.py PC_LINING_FACE, the chandler's alone).
  - The wear: invisible at night here; brightened, real chips and dirt where feet put them. Not a fault.
  - Listed: hard black shadows of the rope rail's string and a jacket on the right lining, cast by the window's lamp with no fill; the street lamp's orange reflection with stepped edges.
- **Round 8 (r8: the hall wall's glow, the lamp at 2.2 m), measured from the left at night:** the door's glass shows the lit hall wall and its hours lettering (12.9 against 1.8); F3's fix holds, for review. The lining's cream fell only from a median of 232 to 225 (none now at 236): try 1 for F4 not enough. **Try 2, the last:** the lamp at 1.6 m, its ends 0.875 m from each lining. Every view retaken as r9, with F5's veneer.
