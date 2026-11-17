# P9: the blind silhouette test, the reviewer's brief (n16-9)

Written by the lane session, 17 November 2026. The test itself: production/research/pre-production/3-PROOFS.md P9 and production/research/asset-plan/2-VEHICLES.md section 3.6, step 3. The main session runs it on the four renders from tools/lane/car_loft_blender.py --render-p9 (untested until then).

## How to run it

- One fresh helper per round, never one that has seen the plan, the provenance line, the class research, car_loft.py or an earlier round's answer. It runs on the subscription (Agent tool), no API calls.
- It gets only the four pictures (side, front, rear, three-quarter; untextured grey on white) and the text in the box below, word for word. Nothing else: no file names that say "hatch", "fictional" or "1990", no folder names, no game name.
- Copy the pictures to neutral names first (view-1.png to view-4.png) in a folder of their own.
- Two rounds at most (RULINGS 3 Nov, medium piece); after a fail, change only the named feature, then a new helper.

## The brief (give exactly this)

> You are an automotive design historian. You will see four pictures of one car body, plain grey with no badges, lamps or texture: view-1.png to view-4.png in <folder>. Look at all four before answering. Do not search the web, do not open any other file, and do not guess from file names.
>
> Answer each question on its own line:
> 1. What make and model is this? Give your single best guess, then up to three other candidates.
> 2. How sure are you of your best guess, from 0 to 100? (0: no idea; 50: it could well be; 90: I would bet on it.)
> 3. Which country or region does the design look like it comes from?
> 4. Which years does it look like it was designed or sold in? Give a range.
> 5. Which single feature most made you think of your best guess (for example the rear pillar, the window line, the nose, the hatch angle, the wheel arches)?
> 6. Does anything look wrong or impossible for a real road car (proportions, stance, wheels, glass)? Say what.
>
> Keep the whole answer under 200 words.

## How to read the answer

- Pass: confidence on the best guess under 50, and no candidate given at 50 or more; region Britain or Europe; years overlapping 1985 to 1991 with a range no wider than about 12 years.
- Fail (a confident name): best guess at 50 or more. Change the feature named in answer 5 (and only that), re-run with a new helper.
- Fail (era or region): the range misses 1985 to 1991, or the region is America or Japan only. Check proportions against the class file first (production/research/lane/HATCH-CLASS-AND-PLATES-2026-11-17.md).
- Answer 6 is a finding for the build, not a pass or fail: list it.
- Record the four answers' text, the pictures' version and the pass or fail beside the asset (tools/approvals.py), and one line in DECISIONS.md.

## Why these numbers

- The asset plan's pass words are "no single model named with confidence, and placed in Britain or Europe, 1985 to 1991" (2-VEHICLES.md 3.6). "Confidence" is turned into a number (under 50) so two reviewers can be compared; the threshold is the lane's judgement, not a source's.
- The candidates list catches a near-miss: a body that three reviewers each call a different real car is fine; one named every time is not, even under 50. If two rounds both name the same model first, treat it as a fail.
- The pictures carry no lamps, grille or badges on purpose: the silhouette must pass alone, before the nose and tail modules (which can only make it more recognisable) are added. Those modules get their own run of the same brief at the material pass.
