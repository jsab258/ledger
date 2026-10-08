# The sky's gate, 8 October: two tries, one reviewer a view

The brief: GATE-SKY-BRIEF.md beside this. Six fresh reviewers in all, each shown one view beside its last good picture (the same editor build with this morning's look file), the Hook sheet, the KCD2 frames and the known list; none saw the maker's verdict or another view.

## Try 1 (the sky light equal to the dome; brick, joinery and pavement to plain colour; night camera one stop up)

| View | What changed (fault?) | New faults from the change |
|---|---|---|
| Hook, day | street lit, shadows lifted, brick now the sheet's middle brick, pavement readable, shop interiors visible: not faults | the road's near lane milky; Mickey's blue and the maroons chalky |
| Reverse, day | street lit, joinery and maroon fronts read, pavement warmer: not faults | the road glaring near-white; brick pink-grey; the foot-of-front dust reading as frost |
| Hook, night | walls read as brick under the lamps, signs readable, pools still apart: not faults | none |

## Try 2 (the paints coloured under the dark light x0.55, the brick redder, the asphalt darker, the dust darker)

| View | Against the bar | New faults from the change |
|---|---|---|
| Hook, day | closer: mean colour 139/127/123 against the sheet's 139/129/125, saturation 0.211 against 0.219 | the near lane near-white (207 against the sheet's road 152), making the known smooth-lane/textured-lane seam glaring; brick less red than this morning (saturation 0.28 against 0.41; the sheet's 0.53-0.65) and the maroon fascias grey-mauve |
| Reverse, day | slightly closer: exposure, shadows, pavement nearer the sheet | the road a blank pale mirror of the sky down the middle (centre 196, mid 222; the sheet's 164/183); brick duller (saturation 0.31 -> 0.21); grey puddle patches more visible; the quay's plane nearer the sky's white |
| Hook, night | slightly closer: pools with darkness between hold, brick no longer glows red, far end has depth | the nearest lamp pool hotter and yellower (clipped red 2% -> 10% of the pavement); the hill's unlit houses a pale flat block; the bare sky now shows as a flat brown-grey third of the frame (known, no longer narrow) |

Measured on the hook frame against the sheet's regions (share of the sky's luminance; scratchpad sky_regions.py): road 22% this morning, 41% now (sheet 41%); pavement 4% -> 9% (10%); far walls 3% -> 7% (14%); near brick 10% -> 10% (6%).

## The step

**Not passed: new faults block.** Every view is, by its own reviewer, closer to the bar than this morning on balance, so the change stays on wip (his order: back to the tag only if still worse). The faults the two tries did not remove:

1. **The wet road mirrors the sky at the sky's own brightness.** Lit at 41% of the sky this morning, the road's mirror read mid-grey; now it reflects the sky as it is, and the road's film is a flat mirror (VignetteShot.cpp: the film puts a flat normal on the asphalt), so the near lane reads near-white. The likely route is the road's texture under the film (a wet road is not a mirror at grazing angles), but seven rougher roads on 3 October read damp or matte; research first.
2. **The brick and the maroons are less red than this morning** under the neutral sky light; their plain colours (the recipe's) read greyer than the sheet's.
3. **At night the near pool runs hot** with the camera a stop up, and the bare sky now shows.

Seen in the earlier pictures too, added to the known list: pale diamond patches flat on the left pavement; bare shins into boots; the wet patches on the road like tan paint; the right edge of the night hook view pure black; a yellow-edged rectangle under the man at Mickey's.
