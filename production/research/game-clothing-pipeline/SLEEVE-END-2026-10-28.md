# The sleeve's end, then the cuffs: the fourth round (28 October 2026)

His pick of 27 October night: the sleeve's end first, then the cuffs, by script. Marvelous reopened and the bridge clicked by him at 09:03. Everything below was measured on Marvelous's own OBJ exports; nothing is judged from memory. Drapes in F:/LedgerTools/garments/tom/zip_jacket/v14 to v20; arrangement probes in F:/LedgerTools/garments/tom/sleeve_try4.

## Questions (written first)

1. Where does the sleeve's cloth lie round the forearm, before and after the drape, slab by slab?
2. Is the flap a matter of length, of the arrangement, or of the end's width?
3. How do Marvelous's makers place a sleeve, and in which pose do they drape?
4. What can the 2026.1 API reach: arrangement, pose, read-back?

## Measures (tools/md-bridge/sleeve_wrap.py)

For each 10 or 25 mm slab along the forearm: the share of the circle round its axis the cloth covers, and how far the cloth's middle lies off the axis. A sleeve round the arm covers about 90% or more with its middle near the axis. The forearm comes from the body (tools/md-bridge/cuff_measure.py) or from the skeleton's elbow and hand joints (`--joints`). The arm's centre line, elbow to 80 mm past the hand joint, is tested against every sleeve and cuff triangle (it must cross none).

## What was found

- **Not length.** Drape 13 (full length, no cuffs) is round down to the wrist, then a flap 100 mm onto the hand (cover 33 to 39%, its middle 35 mm off the axis). Shortened 100 and 140 mm (drapes 14, 15), the flap moves up with the end: the last 40 to 60 mm is always a flap.
- **The arrangement.** Placed but not sewn, the sleeve lies on a curve whose centre is 107 mm off the forearm's axis 250 mm above the wrist and 47 mm off at the wrist. No offset fixes it: 5 to 40 flatten it, 60 to 100 move it out (sweeps in sleeve_try4/arrange, arrange3).
- **Why:** Tom's elbows bend 36.6 degrees in his reference pose, the forearm pointing forward, while Marvelous wraps a sleeve round one straight volume per arm (its manual: a volume runs between two joints). The narrow end closes beside the forearm, and its seam pulls the cloth through the wrist.
- **The method, read 28 October** (a helper, all through the manual and forum pages, no sign-in): Marvelous drapes "a T-pose avatar which can be easily draped", then loads the target pose; volumes are refitted after a pose change ("Fit to Avatar", a menu command only). No API call edits volumes or wrap direction. `ImportPose`, `GetClothPositions` and `ImportAlembic` (a morph target) exist.

## The sleeve's end: first try, passed on its measures

- **A drape body** (tools/md/pose_body.py `--keep-arms --straight-elbows`): his body with each forearm turned 36.65 degrees about its elbow to run on along the upper arm; imported with its 109 points (MH_TomL1_straight.avt). Placed there (offset 40), the sleeve's middle lies 2 to 20 mm off the forearm's axis.
- **Drapes 16 and 17** (no cuffs, full and 100 mm short): round to the very end (cover 89 to 100%, the middle 0 to 15 mm off); the centre line crosses no sleeve cloth (drape 13 crossed it).
- **Back to his pose.** Loading his reference pose in Marvelous (`ImportPose`, then 300 steps) left the hand 154 mm low: not used. tools/md/unpose_garment.py bends the drape back as the game will: each garment point takes the skin weights of the nearest point of the drape body, and the elbows turn back. The body bent back the same way lands on his own within 0.0 mm (median), 5.3 mm at most. Bent back, drape 16's sleeves stay round to their ends (cover 86 to 100%) and the centre line crosses nothing.

## The cuffs: two tries, and a third against the rule

| Drape | What changed | Cuff centre past the wrist, L / R (mark 30) | Off the axis, L / R (mark 30) | Largest gap, L / R (mark 10.5) | Cloth inside the wrist |
|---|---|---|---|---|---|
| 18 | the third try's cuffs on the round sleeve end | 41 / 17 | 20 / 29 | 14.9 / 12.0 | not measured: flat bands beside the wrist (cover 11 to 64%) |
| **19** | each cuff placed at the wrist (offset 30), its side seam sewn after 400 steps | **27 / 12** | **5 / 8** | **11.9 / 9.5** | **5 points each** |
| 20 | as 19, placed at offset 40 (19's cuffs started 1 mm from the skin) | 27 / 20 | 14 / 28 | 16.7 / 18.6 | side seams 41 and 53 mm open |

Bent back to his pose, with the grip (each cuff's width drawn to 85%). Drape 19: both cuffs go right round the wrist (cover 97 to 100% over 20 mm). The left cuff misses the gap mark by 1.4 mm at one point. Five points of each cuff are pulled 4 to 19 mm inside the wrist, their edges stretched to 11 to 45 mm against 6. No skin shows through the sleeve or cuff: 1 or 2 points of about 1,200, the same as drape 13 (pictures: F:/LedgerTools/garments/tom/zip_jacket/v19/grip/look4/sheet.jpg, against v13/look4/sheet.jpg).

**Verdict:** the sleeve's end is fixed; the cuffs are set aside at drape 19. Drape 20 was a third try at the cuffs in this round, made against the two-tries rule (my fault); it failed.

## Next direction for the cuffs (for his word)

1. **Drape 19 with a clean-up** (recommended): in Blender, any garment point inside the body moves out along the skin's normal to the skin offset (3 mm), its neighbours relaxed. The usual repair before baking. It is new code, so it is his to allow.
2. Another round in Marvelous: the cuff's own collision thickness or particle size at the wrist, or an Alembic morph back to his pose instead of skinning.

## Unverified

- That `ImportPose` cannot return the arm. One load and 300 steps were tried; the pose may need more steps or other arguments.
- That skinning back looks as good as a drape at the bent elbow. It is how the game will bend the jacket, and it has not been seen in the game.
- The units of `SetArrangementPosition`'s offset.
