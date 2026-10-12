FAIL

Kit 3.5, Quay Street's litter bins and dustbins: close view (K1 B on its post, K2 c), the v2 render of 12 October 2026. A fresh reviewer wrote this without reading the earlier reviews or TARGET-REVIEW.md. I sliced and ray-cast the .glb files and made my own renders of K1 A (inside and underneath), K1 B (clamp), K2 c (looking down into the aperture, and the burn) and D1 a, b and c.

## Faults, worst first

1. **K2 is a solid block, not a 5 mm shell, so the aperture and the burnt hole have no inside (all three conditions; the build's fault).** Ray-casts on K2 a and c find no inner surface anywhere. A ray at z 0.50 passes the outer skin at r 210 and leaves only at the far side, and the liner sits buried in the solid. The aperture is a blind box cut to the bin's axis: a ray in through the aperture hits a wall at x = 0, and a ray from above hits the box's floor at z 0.680, about 22 mm under the liner's rim. So looking in from the camera's 1.3 m eye height shows a flat green floor and a back wall, with the liner rim floating across them (my render from above shows it plainly). It does not show the dark depth of a 70-litre liner. NOTES.md says "the shell 5 thick", but the mesh disagrees. The target says shell 5, liner inside, a 15 x 6 return flange on the sill. The Southampton photograph (S12) shows a dark interior and the liner through the slot.
   - **Fix:** give k2_shell an inner surface offset 5 mm inside the outer profile, from the ballast top (z 50) up to the dome's underside (skirt inner r 213 from z 650 to 778; dome underside 5 below its top).
   - Cut the aperture through the 5 mm wall only, with the target's 15 x 6 return flange turned in at the sill.
   - **Acceptance:** a ray from (0.4, 0, 0.73) toward -x must cross the shell within 20 mm and next hit the liner's far wall near x = -0.196. A ray from (0, 0, 1.2) straight down must hit the dome, then its underside near z 0.895, then the liner bottom near z 0.06.
2. **K2 c: the burnt hole is a faceted pit carved into the solid. It is not a hole melted through the hood (build).** In the close view, just left of the aperture on the dome's lip, its inside shows lit green flat facets and a floor. No dark opening, no liner. At z 0.77 a slice shows a V-shaped notch about 70 mm deep and a loose triangular sliver of shell between it and the aperture. Target K2-w3 asks for a hole melted through the hood, with a thickened melted edge and the scorched liner seen inside. A burnt-through glass-fibre hood shows a ragged opening with a thin curled lip and black behind it.
   - **Fix:** once item 1 is done, cut the hole through the 5 mm hood at the build's azimuth -58, z 790 (clear of the aperture), about 115 x 85. Use an irregular outline of 14 to 18 points, each jittered by up to ±10 mm.
   - Thicken the cut edge to 8 to 10 mm, curled slightly inward (the melted lip), and add a 25 mm blistered band.
   - Remove the sliver. The liner rim and the dark inside must show through the hole.
3. **K1 B: the sack reads as a black rubber lid on a black collar, and the bin pokes through it (build).**
   - **What the view shows:** the turned-over mouth is a rigid band, a perfect cylinder about 120 deep and about 10 mm proud. Its hem is dead straight, with no fold anywhere. The top is a closed smooth dome rising about 80 mm over the rim, like a cushion lid.
   - **Two green slivers in the band:** one at the band's centre-left, one at its right end. These are the rim bead showing through. The sack and the bin intersect in 758 triangle pairs. The sack also runs through the spacer bar, in 32 pairs.
   - **What the target asks:** K1-w11 says "tucked over the rim 120 on the outside, a tie, a split showing contents". The build has no tie and no split, and the top is closed.
   - **What sacks look like:** Hyde 3132365 shows thin film with sharp creases, loose folds and shine.
   - **Fix:** remodel k1_sack as an open film 1 to 2 mm thick:
     - (a) The bag down the inside of the bin, 2 to 4 mm off the wall.
     - (b) The mouth turned over the bead, its inner face at least 2 mm clear of every bin vertex: the bead at r 186.5, z 1.046, and B's 8 mm rim dent at azimuth 240. It hangs 120 ± 25 with an uneven hem and 6 to 10 gathered vertical folds 10 to 25 deep (the bag's spare girth). At the back it passes over the top of the spacer bar, not through it.
     - (c) A knot of the spare bag at one side (the tie).
     - (d) No dome: the open mouth with the contents' lumpy surface 20 to 60 mm below the rim, and a split showing contents. The O1_full dressing sits on it.
   - **Acceptance:** zero triangle overlaps between k1_sack and k1_bin and between k1_sack and k1_strap.
4. **Narrow, K1 (build): the bolts' heads and nuts float 10 mm off the ears.** The ears' outer faces are at y ±8 mm. The hex head starts at y +18 and the domed nut at y -18, on a 48 mm shank, so about 10 mm of bare shank shows each side. In the close view it is a knob on a stalk beside each clamp.
   - **Fix:** seat the head at y +8 to +13.3 and the nut at y -8 to -16. Shorten the shank to y -15 to +10 (an M8 x 25).
5. **Narrow, K2 (build): the base's moulded edges read soft.** The photograph shows a crisp line where the shoulder meets the base drum (z 236), and a distinct collar band with an edge (z 300 to 364). The close render shows one long smooth swell: the shading is smoothed across the 3 or 4 profile vertices there.
   - **Fix:** split the normals (sharp edges) at z 236, 345 and 364. Or add one vertex pair at each to bring the radius to about 5 mm.
6. **Narrow, K2 (build): the lock is 40 mm low.** k2_lock is centred at z 0.600, on the plain body, where it cannot hold the hood. The target says z 640, at the join. Move it up 40 mm. It is not seen in this view.
7. **Narrow (target): the burn's position overlaps the aperture.** The target's burn at azimuth -28, 115 wide, overlaps the aperture's span of ±31.8° at r 218. The builder's -58 / z 790 is right; the target should say so.
8. **Narrow (notes):** NOTES.md says the collar is r 230. The mesh is r 220, which is right by the target. NOTES.md also says "shell 5 thick" (see item 1). Correct both.

## D1, the galvanised dustbin (my own close renders from the side)

- **D1 a and D1 c pass.** The tapered body, rolled foot hoop, two rolled rings under the rim and top bead match Pentonville 2908276. So do the shallow domed lid with its skirt, the flat strap handle and rivets, and the round-bar side grips on riveted lugs about a quarter of the way down. The 64 flutes and the lid's ribs, which the photograph shows, are normal maps; that is fine here.
  - Narrow note: Pentonville also seems to show a second rolled ring just above the foot hoop. One photograph only, so it is not a fault.
- **D1 b fails (build).** The body is a solid closed at the rim (NOTES.md admits "closed at the rim"). With the lid off, a player sees a flat galvanised disc flush with the bead where the open mouth should be. The "contents" disc at z 0.604 sits 5 mm under that closed top: a ray from above hits the body at z 0.609 first, so it never shows.
  - **Fix:** open the body at the rim. Model an inside wall from the bead down at least 150 mm, the 0.6 mm sheet or a single inward-facing surface. Put the contents 40 to 120 mm below the bead as a lumpy black sack surface, or the lower half of O3_sacks' sack seated in it, not a flat disc.

## What is right

- **K1, how the bin is held:**
  - **The post:** the 76.1 post has its pressed cap.
  - **The clamps:** two 40 x 5 clamp rings at z 620 to 660 and 960 to 1000, each with two ears and one bolt on the side away from the bin. The tapered spacer bar is welded between the rings and the tapering bin wall. Contacts are within 0.6 mm: no gap and no floating part apart from the bolts in item 4.
  - **The bin:** it hangs 232 from the post's axis. It is hollow, with a 1.5 mm wall, r 165 tapering to 180.5, and is 500 high. The rolled bead reads in my top-down render. The flat base plate has its four 8 mm drain holes, which I checked from below.
  - **The meshes:** every mesh is closed (merged, zero open edges).
  - **The kind:** a round bin hung on its own post agrees with Maesteg 4229090.
- **K2:**
  - **The profile:** the shell matches target.json to the millimetre at every point: base drum r 247 (the widest part), shoulder, collar r 220, body r 210, groove 630 to 650, skirt r 218, lip r 224 at 782 to 790, flat dome to 900. That is the silhouette of the 2008 Southampton photograph.
  - **The slot:** the aperture (230 x 105, sill 680) sits high under the dome's overhang as in the photograph.
  - **The patch and the liner:** the cement patch is flush and ragged. The liner's rolled rim shows through the slot.
  - **Faceting:** none is visible at this distance on either bin.
- **The colours' kind:** council green paint, green gel coat, black sack, zinc. All are right for 1990.

## Photographs judged against

- **Geograph 974902**, Jim Champion, Wilton Road, Southampton, taken 2008-09-21, CC BY-SA 2.0: the target's S12, with its crop and overlay in the refs folder. K2's form; the dark interior through the slot.
- **Geograph 2908276**, Stephen McKay, "Northdown Street, Pentonville", taken 2012-04-20, CC BY-SA 2.0. "The old galvanised metal dustbin", seen at the door. It is a later photograph of an unchanged object, since this pressed galvanised bin was the standard household bin through the period.
- **Geograph 4229090**, Jaggery, "Yellow litter bin on a river footbridge in Maesteg", taken 2014-10-30, CC BY-SA 2.0. An "old-style" round bin hung on its own short post, lettered LITTER. It confirms the kind; its fixings are hidden at the back.
- **Geograph 3132365**, Gerald England, "New and old litter bins", Hyde, taken 2012-09-15, CC BY-SA 2.0. Black polythene refuse sacks on the footway: thin film, sharp creases, loose folds, shine.
- **Geograph 5320257**, Jaggery, Anglesey Way, Nottage, taken 2017-03-16, CC BY-SA 2.0. A bin banded to a lamp column: modern, looked at for the idea of the fixing only.
- **Geograph 6703708**, Stephen McKay, Wollaton, taken April 1976, CC BY-SA 2.0. A period street with a yellow fitting on the bus-stop post, too small to judge: looked at, not evidence.
- **Not reached:** no 1975 to 1995 close photograph of a pole bin's clamps, a sack in an open bin or a dustbin close up was found. Geograph's year-filtered feed (1986 to 1994) returned no litter-bin or dustbin photograph. Wikimedia Commons was not tried for lack of time. The clamp details are judged against the target and good engineering, not a photograph.
