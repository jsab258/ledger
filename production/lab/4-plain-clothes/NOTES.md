# Lab test 4: Ron's plain 1990 clothes, modelled to a pattern

8 October 2026, from 07:12, branch lab. The brief:
- A fresh helper writes the target: the pattern drafted by code from Ron's measurements (Thornton's method, adapted to a jumper and trousers), and the outline the clothes should show from the front, side and back.
- I model the garments directly on Ron, with no cloth simulation. The automatic checks: the outline within 1 cm of the target in every view; no body point through the cloth; the seams where the pattern puts them.
- A fresh reviewer judges the three views against two photographs of men in such clothes around 1990.

## The pieces

| Piece | File | Who |
|---|---|---|
| Pattern | [target/draft_clothes.py](target/draft_clothes.py), [target/pattern.json](target/pattern.json) | target helper |
| Target | [target/TARGET.md](target/TARGET.md) (rules O1–O13, corrections C1–C7), [target/target_outline.py](target/target_outline.py), [target/target.json](target/target.json) | target helper |
| Photographs | [PHOTOS.md](PHOTOS.md) | photo helper |
| Model | [model_clothes.py](model_clothes.py), [solidify.py](solidify.py), [seams.py](seams.py), [model_inputs.json](model_inputs.json) | me |
| Checks | [check_clothes.py](check_clothes.py), [checks/](checks/) (one file per version), [where_off.py](where_off.py) | me |
| Review | [REVIEW.md](REVIEW.md) | fresh reviewer |

## The target

- **Trousers:** Thornton's Stout Man's draft (*International System*, c. 1911, p. 288 and Plate 112), because Ron's waist-to-seat disproportion is 5/8 in.
  - All 25 printed worked values of the normal draft are reproduced, and all five of the stout draft's.
  - Girths: waistband 110.5 cm, seat 123.8 cm; one leg 84.2 at the fork, 62.2 at the knee, 57.8 at the hem.
- **Jumper:** drafted the same way, every number sourced or marked as judgement.
  - Finished chest 133.3 cm (4 in ease), back length 72.1, armhole 26.7, cross back 45.6.
  - Sleeve 51.8 cm at the biceps, cuff 22.
  - Crew-neck rib 2.5 cm deep, hem rib 6 cm.
- **Outline rules:** the cloth stands at least 3 mm off the body. Where it is supported, its section is the body's grown to the pattern's girth. Above the underarm the jumper stands off by the chest ease (18 mm). Below the chest it falls straight. The trousers' edges run straight from the knee to the seat.

## How it is modelled (no simulation)

1. **Sections.** Each section is the body's exact cross-section, a plane cut through the mesh's faces: the tape round the body at that place. It is grown evenly to the pattern's girth, or by the rule's stand-off where the cloth hangs free. Horizontal sections every 5 mm make the jumper body and the trouser seat; sections square to the arm make the sleeves; horizontal sections make the legs.
2. **Layers lifted off the body:** the shoulders and the neck rib.
3. **Fusion.** Each part is measured as a signed distance on a 5 mm grid. The parts are united, the surface is taken out, lightly smoothed, and cut open crisply at the hem, cuffs and waist.
   - The sleeves are separate pieces that meet the body only at the armhole, so the cloth does not web across the gap under the arm.
4. **Seams** are read from the construction where the rules put them.

One run takes about 30 seconds. There were 28 runs (v0 to v27).

## Results (v27, against the target as finally corrected)

| Check | Result | Pass? |
|---|---|---|
| Body points through the jumper | 0 of 10,318 the target lists | yes |
| Body points through the trousers | 0 of 7,069 | yes |
| Trousers showing through the jumper | 0 of 15,046 trouser points under it | yes |
| Trousers' outline, front / side / back | at worst 8.0 / 8.9 / 8.0 mm (mean 3.3 / 1.9 / 3.3) | yes |
| Jumper's outline, front / side / back | at worst 11.3 / 11.3 / 11.3 mm (mean 2.3 / 1.2 / 2.3) | **no, by 1.3 mm**, in two or three 2 mm pixels at the neck rib |
| Seams within 1 cm of the target's, at their worst point | 3 of 22 (neck rib, both inseams) | **no** |

The worst seams, as mean and worst distance:
- sleeve underarm: 26 to 28 mm, worst 100;
- armholes: 16 mm, worst 69;
- shoulders: 14 mm;
- crotch: 12 mm, worst 77.

The rest have means of 5 to 8 mm, with worst points of 10 to 80 mm at their ends or at single points.

**Pictures:**
- production/previews/lab/clothes/clothes-v27-three-views-2026-10-08.jpg
- clothes-v27-outline-check-2026-10-08.jpg: green where both agree, red model only, blue target only.
- clothes-v1-and-v27-front-2026-10-08.jpg
- clothes-target-front-side-2026-10-08.jpg

## What the checks found

**In the target (seven corrections, all made by its writer in about 22 minutes).** Each was found by testing the target against Ron's body or its own pattern, and none by reference to my model.
1. **C1:** its sleeves sat inside Ron's forearm, by up to 26 mm. Its own covered points stuck out of its own outline.
2. **C2:** it asked the trousers to cover the tops of the feet.
3. **C3:** the band's top edge stopped 2.5 mm short.
4. **C4:** a 2 to 4 cm step at the top of each sleeve (its notes called it 5 mm).
5. **C5:** the elbow's ease came from an assumed arm girth of 0.30 m; Ron's is 0.345.
6. **C6:** a degenerate spike in the trousers' side outline.
7. **C7:** the neck was drawn as straight lines through three points, 17 mm off its own seam.

**Left in the target:**
- Its shoulder seams float about 7 mm above its own corrected outline.
- Its front view draws the trouser hem level and its side view draws it sloping, so no single 3D hem matches both exactly. The model's sloped hem, set 8 mm low, is within 1 cm in both.
- "Seams at the section's extreme" is ill-defined on a flat side. The target's side seams sit at one end of the flat, mine at its farthest point, so they disagree by up to 3 cm where the section is flat.
- The ring seams (hem, rib top, waistband) agree within 3 to 8 mm from the target's side. From mine they miss by up to 80 mm at the centre back and front: the 3D shape there, which no outline view constrains.

**In my model (each caught by a check or by the pictures):**
- Sections taken from the points within 6 mm of each height missed whole rows of Ron's mesh: his belly's rows are more than 12 mm apart. That made creases and wrong girths, so the sections are now exact plane cuts.
- I misread the sleeve length (J17's extra 1 cm goes over the elbow's bend, so the cuff ends at the wrist).
- The shoulder layer stood 18 mm off the surface in every direction, so the cloth hovered 1.5 cm above the shoulder tops. It now stands off sideways, as the rule's sections do, and rests on top.
- My neckline curve was wrong; it now follows the pattern's quarter-ellipse.
- The trouser legs followed the shin; they now hang plumb from the knee.
- Following the rules literally first gave a stovepipe sleeve with a shelf and showed Ron's chest anatomy through the jumper. The silhouette check could not see either; the pictures did.

## Fresh review (REVIEW.md): FAIL

The reviewer judged v27's front, side and back against two photographs: Tampere, 1988, a heavy-set man in a crew-neck jumper and pleated grey trousers; and about 1989, a plain grey knit. It did not see the code, notes, target or checks. Its words: "the sleeves look like skin, and the trousers look like tracksuit bottoms."

| Fault, worst first | Comes from |
|---|---|
| 1. Sleeves skin-tight; arm muscles show | **the target**: the pattern's sleeve widths (J16–J20, judgement) leave about 3 mm of ease on Ron's thick forearm, and O8 grows the arm's own section, so the muscles print |
| 2. A plain band, then a ridge round the trousers | **both**: the target's own step at the seat line (its "left open" note) is larger in the model |
| 3. Straight wide legs; no taper, crease or break | **the target**: straight leg and level hem 4 cm off the floor (A-T3, A-T5, judgement); a crease is in neither |
| 4. Dark toe marks at the trouser hems | **the model**: the hem cut passes through the bare feet |
| 5. Two spikes in the neck rib at the sides | **the model**, where the rib meets the neck points |
| 6. Belly ridges, a spine dent, a bump on the shoulder | **both**: O5 sets the cloth 3 mm off the belly, and the model shows the body's ridges through that |
| 7. Hem rib does not draw in at the hips | **the target**: the rib is worn over the trousers (O6, O7), which are wider there than the rib |
| 8. Cuffs a plain cut edge, no rib | **the model**: the cuff rib is in the pattern but not modelled |
| 9. Flat seat | **the target**: O9 runs the girth straight from the band to the seat line |

What is right, in the reviewer's words: the jumper's length, its loose straight hang, the sleeves stopping at the wrist, the neck at the base of the neck, and the trousers' fullness at the thigh for a heavy man.

## Verdict on the method

**The checks worked; the clothes did not.**
- **The automatic checks did their job.** They drove 28 versions to the target: no body point through either garment, the trousers' outline within 1 cm in every view, and the jumper's within 11.3 mm. On the way they found seven faults in the target that its writer then fixed, and six of mine.
- **The target did not describe clothes that look right.** It was written as outlines, girths and stand-offs, and the five biggest faults the reviewer named come from it: the pattern's judgements on ease, the straight hang of the trouser legs, the rib worn over wide trousers. An outline from three views cannot see a skin-tight sleeve, printed anatomy, a step round the waist or a crease, so a model can pass the outline and still fail the eye.
- **Seams are a stricter target than outlines,** and only 3 of 22 matched within 1 cm. Most were 5 to 8 mm off on average but up to several centimetres at single points. Part of that is the target's own ambiguity: "the extreme" of a flat side, a front-view hem that the side view contradicts, shoulder seams floating above its own outline.
- This is the lesson of tests 2 and 3 again: an exact target is only as good as what is written down. For knitwear the look (ease, folds, a rib drawing in, a trouser's break) is not written down in the pattern, so it has to come from real garments or photographs. A rule cannot supply it.

## Cost

- **Lab time:** 07:12 to 08:44 by the time log, 1 hour 31 minutes.
- **Target helper:** 28 minutes, plus 18 minutes over seven corrections.
- **Photo helper:** 23 minutes, plus a widened 17-minute search. No free period photograph of a man in a plain crew-neck was found; the two used are the nearest.
- **Fresh reviewer:** 4 minutes.
- **Model runs:** 28 of about 30 seconds each; Workbench renders of about 10 seconds a view.
