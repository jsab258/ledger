# A 1990 shampoo-and-set, groomed by script (Blender 4.5): research note, 29 September 2026

**The problem.** Sheila's hair (her sheet: "greying brown, a short shampoo-and-set perm, done weekly"; her approved portrait production/casting/sheila-dunn/front.jpg: short, soft, rounded, side-parted, swept off the face, to about the jaw, fullest at the crown) grown by script (tools/meshgen/blender/hair/grow_perm.py) failed twice: independent strands made a mushroom of fuzz with a false parting; clumps along 700 random guides came out as flat ribbons and a windblown wig. Researched under the two-tries rule by a separate helper given the problem; saved by the builder. "Mine" marks the helper's inference. All sources accessed 29 September 2026.

## What the style is

- Shampoo and set: washed, setting lotion, wound wet on rollers, dried under a hood, brushed out; common in the UK from the 1930s, kept by older women by 2016 [R1]; kept between visits with rollers at home [R2]. Sections no wider than the roller, each on its own base, back-brushed on top, brushed into an all-over wave [R3]. Patterns: rows back from the forehead, sides angled to the ears, tidy or brick-offset rows at the back; "large curlers give volume but minimal curl" [R4]. 12 to 20 rollers (e.g. 3 on top, 2 each side, 9 at the back); hair wraps about twice; 1.6 cm rollers give tight curls, 3 cm looser waves [R5].
- Photographs (links only): Thora Hird, 1974, Allan Warren, CC BY-SA 3.0 (a brushed-out roller set: rows of rounded barrel curls, height at the crown, off the forehead, ears half covered) [P1]; Margaret Thatcher, 6 August 1990, Bush Library, public domain (a smooth rounded shape swept back, lifted crown, curls brushed into waves) [P2].
- Mine: Sheila's portrait sits between them (a side parting on her left, a soft fringe swept across, sides to the earlobe or upper jaw, a tapered nape): day five of a weekly set. The portrait decides the shape; the photographs what a set looks like.

## Why the attempts failed (mine) and how grooms stay neat

- Guides first, then children, clump, curl, noise [T3][T7]; for curls two levels, flow guides then clump guides [T6]; curl the clump, not the strand [T4]. Blender's Duplicate Hair Curves places copies on a disc in each point's own cross-section (round tubes) and writes guide_curve_index for Curl and Clump [T1][T2]. Clumps tighter at the tips with gaps between [T9], a convex profile [T5].
- Attempt 2's clumps were flat because the offsets stayed in the scalp's plane; windblown because every guide had its own random length, curl and phase, where the hair from one roller moves as one shape; attempt 1's false parting came from the left/right sweep rule applied behind the crown; its mushroom from a constant distance off the head with the ends not turned under.
- Brushed-out roller curls: one roll per roller, a C-shaped arc turned under round a horizontal axis square to the combing direction (Blender's Roll Hair Curves does this); the perm is a small ripple on top.

## The recipe (the helper's)

1. Cameras matching the portraits.
2. An envelope above the scalp (by ray from the head's centre): crown 30-35 mm, front hairline 20-25, temples 18-22, earlobe level 8-12, nape 5-8; tips tuck to 3-6 mm.
3. Flow: in front of the crown, away from a parting 35 mm left of centre, then back and down; behind the crown straight down from the whorl, no left/right flip.
4. 18 rollers: 4 on top (roll radius 15-18 mm, 150 degrees), 3 each side (12 mm, 180), 8 at the back in rows of 3, 3, 2 (the nape row 9-10 mm, 120); each roller's axis = surface normal x flow; alternate rows offset.
5. Lengths by position (+-4% at most): top 85-100 mm, fringe 75-90 swept across, sides 60-75 to the earlobe or jaw, nape 35-50.
6. About 150 flow guides, no randomness: rising 45-60 degrees off the scalp over the first 10 mm, along the envelope, the last 30-40% rolled under round its roller's axis.
7. 500-700 clump guides, each blended from the 3-4 nearest flow guides of the same roller only; a perm ripple 1.5-3 mm high, 20-30 mm between waves, one phase per roller, +-0.1 rad jitter.
8. 35-40 strands per clump (about 22,000): offsets in each point's own frame along the guide, carried without twisting, from the real root offset into a disc of radius sqrt(u) x 3.5 mm within the first 15%, narrowing to 1.5 mm at the tip (or Duplicate Hair Curves, amount 36, radius 0.0035, roots snapped back); children 0-8% shorter; 24 points; radius 0.00004 m.
9. Tidy: Shrinkwrap against the head (offset 0.0015, lock roots); clamp every point to the envelope + 2 mm; Smooth (0.3, 3 iterations, preserve length); frizz 0.8 mm on about 2% of strands.
10. Checks: no point beyond envelope + 3 mm; no root more than 1 mm off the skin; no scalp gap wider than 3 mm from behind; the outline over the portrait.

Pitfalls: Blender's hair node defaults are at 10 cm scale (Guide Distance 0.1, Radius 0.1, Roll Radius 0.05): set every value; Curl's Random Offset (0.25) and Roll's Random Orientation (0.5) break coherence; Interpolate needs a surface object and UV map, and its guide index must be named guide_curve_index; Duplicate's roots can float; a curl radius of 5 mm or more reads as a wild perm, not a set (mine).

## Sources

- R1 "Shampoo and set", Wikipedia (current revision): https://en.wikipedia.org/wiki/Shampoo_and_set
- R2 Kids of the 50s and 60s, 25 July 2016: https://kidsofthe50sand60s.com/2016/07/25/mums-and-their-weekly-hair-dos/
- R3 Salon Geek thread, 16 August 2013: https://www.salongeek.com/threads/shampoo-and-set.231934/
- R4 Pammy Delux, roller patterns (undated; cites magazines 1969-1982): https://www.pammydelux.com/bebetter/Hair/Hairstyling/RollerSets.shtml
- R5 L. Rennells, VintageHairstyling.com, July 2025: https://vintagehairstyling.com/bobbypinblog/2025/07/hair-rollers-decoded-vintage-stylist-guide-matching-rollers-your-hair-and-style-goals.html
- P1 https://commons.wikimedia.org/wiki/File:Dame_Thora_Hird_Allan_Warren.jpg (1974, CC BY-SA 3.0)
- P2 https://commons.wikimedia.org/wiki/File:Margaret_Thatcher_visiting_George_H._W._Bush_at_White_House.jpg (1990, public domain)
- T1 Blender 4.5 LTS Manual, Hair Nodes (2025): https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/hair/index.html
- T2 Blender 4.5.13's procedural_hair_node_assets.blend, inspected locally
- T3 Blender Studio, "Procedural Hair Nodes", 22 February 2023: https://studio.blender.org/blog/procedural-hair-nodes/
- T4 SideFX, Hair Clump 2.0 (current docs): https://www.sidefx.com/docs/houdini/nodes/sop/hairclump.html
- T5 J. Coetzer, SideFX tutorial, 7 June 2022: https://www.sidefx.com/tutorials/advanced-grooming-tips-and-houdini-to-unreal-engine-tutorial/
- T6 P. Zielinski, 80.lv, 6 February 2026: https://80.lv/articles/artist-shows-grooming-workflow-for-curls-afros-braids-in-houdini
- T7 Chang et al., ACM Transactions on Graphics 44(4), SIGGRAPH 2025: https://weschang.com/publications/iphg/
- T9 Autodesk, XGen Clump modifier (Maya 2025)
