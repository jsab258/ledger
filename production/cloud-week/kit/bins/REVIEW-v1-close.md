FAIL

Fresh review of the CLOSE view of kit unit 3.5 (litter bins and dustbins), cloud week 42, 12 October 2026. The render judged is close.png (K1 B on its post at left, K2 c at right, 1.9 m, eye 1.3 m, lens 30). I also made my own renders of the .glb files (K1 B from above, from behind the post and from below; K2 c at the burn, into the aperture, from the back and in section; D1 a, b and c from the side), and ray-cast the K2 shell. I formed this view before reading NOTES.md, and I have not read any other review.

The piece fails on three build faults, all at the top of the two bins, where the close view looks. Each would be seen as wrong from a step away in the game. The forms and proportions themselves are right (see "What is right").

## Faults, worst first

1. **K2 has no inside. It is a solid with a sealed box behind the slot, not a 5 mm shell (build).**
   - Where: the aperture at right centre. Through the slot the view shows a green ledge, a grey arc and a dark back.
   - What the .glb holds: `k2_shell` is one closed surface. At z 500 every vertex is at r 210, with no inner wall at r 205. The slot is a rectangular pocket: a floor at z 680, a ceiling at z 785, side walls at y ±115, and a back wall 230 x 105 standing on the bin's axis (x = 0). My section render and ray-casts show this.
   - The liner (`k2_liner`, r 200) is buried inside the solid. Only the top 22 mm of its wall and rim pokes up through the pocket floor. That strip is the grey arc seen in the slot, and it is a pair of intersecting faces.
   - NOTES.md says "the shell 5 thick". The file does not hold that.
   - What the photograph shows instead: S12 (Geograph 974902, crop at refs/litter-bins) shows a deep dark void through the slot, with the liner's metal rim and a sack with litter inside. The target asks for shell 5 and for the liner to be seen through the aperture with a galvanised rim, a black sack's folded edge and loose litter (K2-w9). The overflow dressing O2_full has nowhere to go: inside the solid it is hidden or intersects.
   - In the engine, a player looking into the slot from half a metre sees a flat green wall 218 mm in.
   - Exact fix:
     - Build the hood and body as a 5 mm shell: offset the inner surface 5 inward from z 50 (the top of the ballast) to the underside of the dome.
     - Delete the pocket's floor, ceiling, side walls and back wall.
     - Close the slot's cut edge with a 5 mm face. Add the target's 15 x 6 return flange, turned inward at the sill only.
     - The liner then stands free inside, its rim at 702 to 708 showing 22 above the sill.
     - Add a check: a ray from the close camera through the centre of the slot must hit the liner's inside or the far inner wall, never a face at x = 0.

2. **K2 c's "burnt hole" is a closed crater, not a hole (build).**
   - Where: left of the slot on the hood.
   - What the .glb holds: the hood surface at azimuth -58, z 790 is pushed in to r 150, a crater 68 deep with a closed floor. A ray at the hole's centre hits that floor (an outward face) and then leaves by the far side of the bin. The floor is a few large flat facets, lit green.
   - It reads as a chip gouged out of stone. It does not read as glass-fibre burnt through.
   - The target (K2-w3) asks for "a hole melted and burnt through the hood ... its edge thickened and re-set".
   - Exact fix, after fault 1:
     - Cut a real opening through the 5 mm shell, about 115 x 85. Give it an irregular outline of 14 to 18 vertices.
     - Roll the cut edge into a melted bead 6 to 10 thick, curled slightly outward, with the 25 mm blistered stretch the target names.
     - Leave the inside showing dark through it (the liner scorched).
     - Shade the edge smooth. No flat facet larger than about 20 mm.
     - The move to azimuth -58, z 790 is a named departure and acceptable.

3. **K1 B's sack is a black cushion floating in the bin's mouth (build).**
   - Where: the top of the left bin.
   - What the .glb holds: `k1_sack` is a smooth closed dome of 224 triangles, about 300 x 270 across, running from z 989 to z 1139. Nothing is under it: the bin is empty below, and the sack's bottom is 440 above the base plate. It stands 25 to 30 clear of the wall all round. From above, the gap shows the empty bin beneath it (my top view).
   - Its outline is visibly faceted. In the close view it reads as a black rubber lid sitting on the bin.
   - What the photograph shows instead: Geograph 3613688 (Doddington, 2013) shows a black sack's mouth folded over a litter bin's rim and sagging down the outside. The target (K1-w11) asks for the sack as the liner, "tucked over the rim 120 on the outside, a tie, a split showing contents".
   - Exact fix:
     - Rebuild `k1_sack` as a liner: a thin sheet (single-sided, or 1 mm) lining the bin's inner wall from the base plate (z 553) up and over the rim bead, then 120 down the outside to about z 930.
     - Give it 8 to 12 soft vertical folds below the rim and slack bunched where it turns over the bead.
     - For B's full state, a lumpy heaped top, not a smooth dome.
     - Shade it smooth, 600 to 900 triangles.
     - Nothing may stand more than 10 off the wall except the heap.

## Narrow points for the builder (not failing alone)

4. **K1 clamp ears are too heavy (build; the target's "two 12 mm ears" is ambiguous).** Each ear is a block 12 thick, 24 out and 36 tall, with 12 between the two ears. The ring itself is 5 thick, so from behind the post (my back view) they read as cast lugs. On a clamp made from 40 x 5 flat bar, the ears are the bar's own ends turned out. Fix: ears 5 thick, 40 tall (as the ring), 25 out, 6 apart; M8 bolt 30 long. The target should say "ears 5 thick, 25 out" (target's wording).

5. **K1 ring and spacer bar meet only on a line (build, per the target).** The bar's flat post face (x 43.05) touches each round ring tangentially, so up close the join reads as unwelded. Fix: a 4 mm weld fillet along each contact, or make the bar's post face concave to r 43 over the ring's 40 height.

6. **K1 base edge (build).** The bottom is a crisp flat cut. The target asks for a 5 mm radius and a visible turned-up lap of 6. This is seen only from low down. Fix: as the target says.

7. **K2 base drum shoulder (target's profile).** S12 (bottom third) shows the shoulder as a conical band about 55 high. A crisp crease at its foot meets the vertical drum, with a highlight above it and a shadow line below. The profile instead blends it as a soft round from z 236 to 290. Fix: profile (247, 236), then (246, 240) with a 2 to 3 mm radius at the crease, then a straight cone to (222, 292).

8. **K2 cement patch outline (build).** The outline is a straight-segment polygon (112 triangles) with hard corners that show at 1.9 m. S12 shows a crumbly, broken edge. Fix: a 40 to 60 vertex outline jittered at 10 to 20 mm scale, or an alpha-edged decal.

9. **K2 lock (build; not in this view).** The lock (z 620 to 660, outer face r 210) is coplanar with the body below z 630, so its faces z-fight with the body. Above z 650 it is inside the hood skirt. Fix: set the escutcheon on the hood skirt at z 655 to 695, standing 3 proud of r 218.

10. **Target wording.** Under K1 "fixings" the target says "4 M8 bolts in two clamps". Its clamp note and bolt count say one bolt per clamp, 2 in all. The build has 2, which is right. Correct the fixings line.

## D1, the galvanised dustbin (a, b, c rendered from the side by me): sound, with narrow points

Against Chawleigh, Cusop and Inner Hope, D1 reads as the British galvanised bin:
- the tapering body;
- the two rolled rings under the rim bead;
- the rolled foot hoop;
- a domed lid with a riveted strap handle;
- horizontal 12 mm round-bar grips standing 38 proud, on lugs with two dome rivets each. The rivets are proud of the lugs, not buried.

The handles, lid and conditions are consistent across a, b and c, and nothing floats. Narrow points:
- **Grips (build).** On the bins in Inner Hope and Chawleigh the bar turns down at each end into a strap that hangs below the bar, with both rivets below the bend. The build centres the lug on the bar, with one rivet above it and one below. Fix: put the lug's top at the bar's centre line, hang it 55 below, set the rivets 15 and 55 below the bar, and give the bend a 10 mm radius.
- **Lid edge (build).** The lid's edge reads as a thick rounded cushion about 29 deep. Pressed 0.6 mm lids show a thin turned-down skirt (the lid lying on the ground in Chawleigh). Fix: a thin skirt band (1 to 2 thick in the mesh) with a small rolled edge.
- **D1 b contents (build).** The contents are a flat black disc 4 below the rim crown. Without the O3 dressing, this reads as the lid still on. Fix: drop it 60 to 100 and give it heaped sack folds, or delete it and rely on the dressing.
- **Body silhouette (target's).** The body's outline is smooth because the flutes are a normal map (the budget choice). Inner Hope also shows 3 or 4 horizontal corrugations just above the foot hoop, which the target lacks. That comes from one photograph, so it is a note only.

## What is right

- **K1 B:** the bin's size, taper and hanging height read right.
  - The 9 mm rolled bead is round and continuous. The rim bend at azimuth 240 reads as a real knock.
  - The two 40 x 5 rings sit on the post with their ears on the far side. Each takes a through-bolt with a hex head and a domed nut.
  - The tapered spacer bar meets the tapering wall with no gap. The bin bead clears the post by about 7.
  - The post's pressed cap is right. The four 8 mm drain holes are real holes.
  - Silhouettes are smooth everywhere except the sack.
- **K2 c:** the stepped form matches S12: the base drum is the widest part, then the shoulder, the collar, the plain body, the groove, and the hood skirt standing 8 proud under a flat dome with an R 45 shoulder.
  - The slot's size and height match the S12 overlay.
  - The cement patch is present and flush.
  - The outline is smooth with no faceting.
- **Colours:** council green and the zinc greys are the right kind.

## Photographs judged against

- **Geograph 974902** (S12), hooded glass-fibre bin beside a pillar box, Southampton. Taken 2008, CC BY-SA 2.0. Judged on the repository's crop and overlay (production/previews/cloud-week/refs/litter-bins/), not on the page itself. It is a later example of a type made since 1984; the target assumes the form is unchanged.
- **Geograph 1278296**, "Church dustbin, Chawleigh", Tom Jolliffe, https://www.geograph.org.uk/photo/1278296. Taken 2009-04-29, CC BY-SA 2.0. Shows the rings under the rim, the corrugated body, a side handle, and the lid on the ground.
- **Geograph 6880162**, "Inner Hope" (Bradninch, Devon), A J Paxton, https://www.geograph.org.uk/photo/6880162. Taken 2014-06-01, CC BY-SA 2.0. Shows the galvanised bin's flutes, a round-bar grip turned down into a riveted strap, and the corrugations at the foot.
- **Geograph 3757342**, "4 dustbins in Cusop", Jaggery, https://www.geograph.org.uk/photo/3757342. Taken 2012-06-10, CC BY-SA 2.0. Shows four lidded galvanised bins and their proportions.
- **Geograph 3613688**, "Post box and bin, Doddington", Graham Robson, https://www.geograph.org.uk/photo/3613688. Taken 2013-08-20, CC BY-SA 2.0. Shows a black sack's mouth folded over a litter bin's rim.

Why later photographs count:
- The British galvanised dustbin's form was the same from the 1950s through 1990. It was replaced by wheelie bins, not redesigned (the Cusop caption says the survivors are the old bins).
- A sack folding over a rim is behaviour, not a period form.

Not reached:
- Geograph's feed, year-filtered with takenyear:1985, 1988, 1990 and 1992 for dustbin, dustbins and litter bin, and 1989 to 1990 for litter, bin and rubbish, returned no photograph of a litter bin or dustbin from 1975 to 1995. The only result was a burning wheelie bin, 4302467, taken 1990.
- Searches for pole-mounted, round and bracketed litter bins of any year found no photograph of an open round steel bin on its own post. K1's type and fixing therefore stay Judgement: not confirmed, and not contradicted, by any photograph.
- Commons and archive.org were not tried.
