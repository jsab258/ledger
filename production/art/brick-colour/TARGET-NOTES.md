# Brick colour target: measurements for the 8 October order

Fresh helper, not the builder. S: HSV saturation of a region's mean sRGB colour, (max - min) / max; hue: that mean's. Boxes and definitions: target.json. Re-run: `python measure_brick.py --sheet --photos`.

## Photographs (S, hue; P3 and P4 converted from Display P3)

- P3 Beeston 1886, overcast: front 0.537-0.555 (three boxes), 18.2-19.9; gable 0.480, 18.7.
- P4 Beeston 1896, sky: front 0.546, 19.0; return 0.510, 13.6.
- P2 West Bromwich 1897, full sun: 0.410-0.413, 15.7-16.3.
- Dressings: P6 gauged arch 0.489, 18.4; P9 sunlit red jambs 0.601, 15.7.
- P1, P5, P7, P8: no red-brick wall.

Pale joints: 0-5% of pixels, moving S at most 0.01. Per-pixel S averages within 0.02 of S.

## Sheet

Near building 0.605 (five boxes, 0.436-0.678), hue 15.5; right cottage 0.599, 19.9; parade's second building 0.480 (0.444-0.499), 15.0; far right row 0.427 (0.366-0.460), 14.3; maroon front: board 0.312, 6.3; pilaster 0.530, 4.8.

## Where they disagree

The sheet's near brick and cottage are redder than any photographed wall (most 0.555; only P9's sunlit dressings reach 0.60). The photographs win: **ceiling 0.56, not 0.65.** The floor 0.53 holds for faces in the light (photographs 0.537-0.555); the terrace, out of the light, takes **0.48** (P3's gable, P4's return: each below its lit front). Hue agrees: 13.6-19.9, band 13.5-20.

## Target, hook frame 2560 x 1440 (S; hue; sRGB at today's V)

- brick_near, corner house side and front above Mickey's: 0.53-0.56; 13.5-20; 125/76/57.
- brick_parade, upper wall over Fresh Fish: 0.44-0.50; 13.5-20; 147/97/78.
- brick_far, far cross-street gable and two far bays: 0.36-0.46; 13.5-20; 136/96/80.
- brick_left_terrace: 0.48-0.56; 13.5-20; 63/39/30.
- fascia_maroon, Fresh Fish and pawnbroker boards: 0.31-0.53; 0-10; 124/76/72.

Parade and far follow the sheet's own loss of colour with distance, not the director's band; photographs cannot measure distance. No photograph shows maroon paint: the sheet's board-to-pilaster range. Brightness is not judged.

## The frames (S / hue: near, parade, far, terrace, fascias)

- Now: 0.506/14.2, 0.406/13.3, 0.340/13.2, 0.385/11.2, 0.172/346.9.
- This morning: 0.605/17.4, 0.540/16.8, 0.438/15.2, 0.577/12.9, 0.281/351.3.

Both fail. Now every region is under its band; this morning near, parade and terrace were over: the target lies between. The terrace's hue and the fascias' pink-mauve fail in both.

The gate's 0.28 does not reproduce on the near brick (0.506); it matches the far bays (0.300, 0.305; this morning 0.427, 0.451 against its 0.41): far brick set against the sheet's near.

## Unsure

- Photographs dry, street wet. Wet brick reads darker and probably redder; none measured, so 0.56 may be low by an unknown amount.
- Three walls, two from Beeston. The research gives Hull red and buff, Grimsby red-brown (BRICK-2026-10-04.md): duller, if anything.
- The maroon rests on one small far shop (924 pixels); its hue band's width is a judgement.
- Small samples: far 6,810 pixels; terrace 22,860.
- S barely moves with exposure under a power curve; the game's tone curve may shift it at dark values (terrace, V 0.25).
