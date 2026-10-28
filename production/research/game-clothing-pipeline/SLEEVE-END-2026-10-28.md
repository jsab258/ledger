# The sleeve's end, then the cuffs: the fourth round (28 October 2026)

His pick of 27 October night: the sleeve's end first, then the cuffs, by script. He reopened Marvelous and clicked the bridge at 09:03. Everything below was measured on Marvelous's own OBJ exports; nothing is judged from memory. Drapes are in F:/LedgerTools/garments/tom/zip_jacket/v14 to v22, arrangement probes in F:/LedgerTools/garments/tom/sleeve_try4, the fresh review's scripts in the session's scratchpad (review-sleeve/check1 to check10).

## Questions (written first)

1. Where does the sleeve's cloth lie round the forearm, before and after the drape, slab by slab?
2. Is the flap a matter of length, of the arrangement, or of the end's width?
3. How do Marvelous's makers place a sleeve, and in which pose do they drape?
4. What can the 2026.1 API reach: arrangement, pose, read-back?

## Measures

tools/md-bridge/sleeve_wrap.py cuts the forearm into 10 or 25 mm slabs. For each slab it gives the share of the circle round the forearm's axis that the cloth covers, and how far the cloth's middle lies off that axis. A sleeve round the arm covers about 90% or more, with its middle near the axis.

The forearm comes from one of two places: the body itself (tools/md-bridge/cuff_measure.py, as a tape finds the wrist) or the skeleton's elbow and hand joints (`--joints`). The two wrists sit 16 mm apart, so each number below names its finder.

The arm's centre line runs from the elbow to 80 mm past the hand joint. It is tested against every sleeve and cuff triangle: it must cross none.

## What was found

- **Not length.** Drape 13 had no cuffs, its sleeve 10 mm short of the full pattern. It is round down to the wrist, then the last 86 to 89 mm past the wrist (joint finder) is a flap. There, cover is 31 to 47%, and the middle lies 30 to 45 mm off the axis.

  Drapes 14 and 15 were 90 and 130 mm shorter than drape 13. The flap moves up with the end: the last 40 to 60 mm is always a flap.
- **The arrangement.** Placed but not sewn, on his reference pose, the sleeve lies on a curve. A circle fitted to each 25 mm slab puts the curve's centre about 100 mm off the forearm's axis, at every offset from 10 to 100 (sweeps in sleeve_try4/arrange, arrange3). By the body finder it is 107 mm off, 250 mm above the wrist, and 47 mm off at the wrist. The offset changes only the curve's radius.
- **Why:** Tom's elbows bend 36.6 degrees in his reference pose, and his forearm points forward. Marvelous wraps a sleeve round one straight volume per arm (its manual: a volume runs between two joints). The sleeve's narrow end closes beside the forearm, and its seam pulls the cloth through the wrist.
- **The method, read 28 October** (a helper, through the manual and forum pages, no sign-in):
  - Marvelous drapes "a T-pose avatar which can be easily draped", then loads the target pose.
  - The volumes are refitted after a pose change ("Fit to Avatar", a menu command only).
  - No API call edits volumes or wrap direction.
  - `ImportPose`, `GetClothPositions` and `ImportAlembic` (a morph target) exist.

## The sleeve's end: first try, round in the drape

- **A drape body** (tools/md/pose_body.py `--keep-arms --straight-elbows`): his body with each forearm turned 36.65 degrees about its elbow, so it runs straight on from the upper arm. It was imported with its 109 points (MH_TomL1_straight.avt). On it, a placed sleeve's curve centre lies 15 to 25 mm off the forearm. At offset 40, the sleeve's middle lies 2 to 21 mm off.
- **Drapes 16 and 17** (straight body, offset 40, no cuffs, full and 100 mm short):
  - Each sleeve is round to its very end: cover 89 to 100%, its middle 0 to 15 mm off.
  - The centre line crosses no sleeve cloth (drape 13 crosses it).
- **Which change did it** (two drapes after the review, each changing one thing against drape 16):

  | Drape | Body | Offset | Left sleeve | Right sleeve |
  |---|---|---|---|---|
  | 21 | reference | 40 | flap past the wrist (cover 8 to 64%); 2 crossings | flap past the wrist (cover 25 to 58%); 2 crossings |
  | 22 | straight | the point's own | round to its end; no crossing | the last 50 mm a flap (cover 17 to 64%); 1 crossing |
  | 16 | straight | 40 | round to its end; no crossing | round to its end; no crossing |

  So the straight elbows are the main cause, and the closer offset completes them.
- **Back to his pose.** Loading his reference pose in Marvelous (`ImportPose`, then 300 steps) did not return his arm. That one try says little, though: the body it left had its feet 223 mm below the floor and was shifted 179 mm sideways.

  tools/md/unpose_garment.py bends the drape back the way the game will. Each garment point takes the skin weights of the nearest point of the drape body, and the elbows turn back.
  - Bent back the same way, the body lands on his own within 2.3 mm (median) and 5.3 mm at most, within 80 mm of the elbows. That proves the frames and the turn. It cannot test the garment's borrowed weights, because body points take their own weights exactly.
  - Beyond 50 mm from the elbow, the sleeve moves as a rigid piece. "Still round to its ends" therefore repeats drape 16's result.
  - Within 50 mm of the elbow, the cloth is crushed and stretched. Edges change to 0.61 to 1.91 of their draped length, and 13% of them change by more than a fifth. Three or four points per side end up inside the body there, none deeper than 0.3 mm.

**Verdict:** the sleeve's end is round in the drape. In the game it is not yet seen, and the bent elbow's crushing is not yet judged by eye.

## The cuffs: two tries, and a third against the rule

The table gives each drape bent back to his pose, with the grip (each cuff's width drawn in to 85%), by the body finder. The marks:

- the cuff's centre within 30 mm of the wrist, along the arm and off its axis;
- its largest gap to the skin within 10.5 mm (the skin offset and the cloth's thickness, plus 5);
- no cuff cloth crossing the arm's centre line.

| Drape | What changed | Centre past the wrist, L / R | Off the axis, L / R | Largest gap, L / R | Centre line crossed (L / R) |
|---|---|---|---|---|---|
| 18 | the third try's cuffs on the round sleeve end | 41 / 17 | 20 / 29 | 14.9 / 12.0 | 1 / 1; left cuff a flat band beside the wrist (cover 11 to 64%), right up to 78% |
| **19** | each cuff placed at the wrist (offset 30), its side seam sewn after 400 steps | **27 / 12** | **5 / 8** | **11.9 / 9.5** | **2 / 2** |
| 20 | as 19, placed at offset 40 (19's cuffs started 1 mm from the skin) | 27 / 20 | 14 / 28 | 16.7 / 18.6 | 2 / 1; side seams left 41 and 53 mm open |

Drape 19 is the best:

- Both cuffs go right round the wrist: cover 97 to 100% over 20 mm.
- It still fails two marks:
  - The arm's centre line crosses 2 cuff triangles at each wrist.
  - Points are pulled inside the wrist: 8 on the left (7 to 22 mm deep) and 5 on the right (11 to 22 mm deep).
- 69 cuff edges per side are stretched past 15 mm, the longest to 57.5 mm, against a 6 mm cloth spacing.
- The left cuff's gap is 11.9 mm against the 10.5 allowed.
- The drape is the same before it is bent back, so Marvelous made these faults, not the bend-back.
- Skin is barely covered wrongly: 2 points poke through on each side, of about 1,175 under the cloth, and 6 on the right wrist have no cloth over them. Drape 13 had 167 to 201 bare skin points at the wrist.

The pictures (F:/LedgerTools/garments/tom/zip_jacket/v19/grip/look4/sheet.jpg, against v13/look4/sheet.jpg) show what the numbers do not:

- a crumpled, faceted ring of cloth above each cuff;
- a knotted lump where sleeve meets cuff on the outer wrist;
- dark slits at that seam;
- small dark nubs at the cuff's lower back edge.

**Verdict:** the cuffs are set aside at drape 19. Drape 20 was a third try at the cuffs in this round, made against the two-tries rule (my fault); it failed.

## Next direction for the cuffs (for his word)

A clean-up that pushes caught points out of the skin would not mend the lump, the crumples or the cloth through the wrist, so it is not offered.

1. **The cuffs built in the bake** (recommended):
   - each sleeve cut a little above the wrist, where it is now round;
   - a rib band made round the wrist's own shape and joined to that round end;
   - the band skinned to the hand and forearm.

   This route is certain and fully controlled. It is new code.
2. **Another round in Marvelous at the seam:** finer cloth there, a gentler gather (elastic on the sleeve's end instead of shrinking the cuff), and the cuff's own collision thickness. It is uncertain, and it needs his click.
3. **Tom dressed now** with drape 19's cuffs, their faults listed and mended later.

## Unverified

- That `ImportPose` cannot return the arm: the one try is confounded (see above).
- How the bent-back elbow looks; it has not been seen in the game.
- The units of `SetArrangementPosition`'s offset.
