# The reviewer test, 7 October 2026: how it was done

Asked for: test the gate's AI reviewer with planted faults of the kinds that have reached him, using the gate's own brief exactly as the gate does, with no person in any picture; count caught, missed and false alarms; then show the reviewer the last good picture beside each one and count again. Started from wip at 39ae711a. Nothing outside this folder was changed.

## The reviewer

The gate's reviewer as the gate runs it: a fresh, read-only helper on Opus, given the gate's brief and the pictures, never the maker's view. Every review in this test was a new helper that judged one picture (plus the last good one in round two), with no word of the test, of planted faults, or that some pictures were clean. The brief and what was changed in it are in BRIEF-AS-USED.md.

## The pictures

**Ten bases** from production/previews, five views of the street and Mickey's frontage and four of Mickey's office and Rita's front by day and night (KEY.md). Mickey's office views have no one in them and were used whole. Every street view has passers-by, so each was cut to a part with nobody in it: the upper band of the hook, night and reverse views, Rita's front without the woman at her door, the shop row either side of the passer-by. Every cut edge was checked at twice the size for any part of a person, a reflection included. Mickey's frontage close-up was swapped for the hook view's door-and-corner part because a faint shape in its glass might have been a person's reflection. The Hook sheet's passers-by were left out the same way (its upper part only).

**Twenty faulty copies**, two per base, one fault each, of the kinds that have reached him (the black block in the hook view, the white strip in the top pane, dark seams down the roofs, opaque placeholder panes, the floating "Talk to Sheila", engine text) and the ones asked for: black square, test-colour block, floating object (twice), missing window pane, hole in a wall, stretched texture, duplicated object, light where none belongs, debug text, mirrored text, wrong scale, fireflies, stray interface prompt, texture tiling, low-resolution texture, untextured placeholder window, z-fighting, seam stripe and the white strip. Each was checked at full size against its clean copy and redone where the cut-out read as a paste-up (five were). Sizes run from a 27 by 50 pixel pane (0.17% of the picture) to a tiled wall (18%).

**Five clean copies**: the office by day, the hook view, the street at night, Rita's front by day and the shop row's right part.

All twenty-five were encoded the same way (JPEG, quality 88), so nothing about the file gives a fault away, and shuffled under neutral names (frame-01 to frame-25). The key stayed outside the repository until every review was in.

The pictures are not in git: the size guard keeps pictures to production/previews/, and this task writes only here. `plant_faults.py` remakes the bases and all twenty-five frames from the committed previews.

## The three runs

1. **Alone:** twenty-five fresh reviewers, one frame each, the brief as the gate gives it.
2. **Beside the last good picture:** twenty-five more fresh reviewers, the same frames, the brief with one line more naming the last good picture of the same view. Here that was the clean original, so for a clean frame it was the identical picture. This is the best case: the gate's real last good picture is days older and differs by real work.
3. **Realism check:** eight more fresh reviewers, six faulty and two clean frames of Mickey's office and corner, beside the same views' real earlier versions (4 October's office by day and night and the corner's second try), which differ by two days' real work.

## Scoring

By SCORING.md, written before any review ran. I scored every review against the key. Then two fresh helpers checked it: one scored caught and missed again from the key and the reviews alone, without my scores, and one went through the ten clean-picture reviews claim by claim for false alarms. Every review is kept word for word in `reviews/`.

## What this test cannot tell

- **Previews, not full frames.** The reviewers saw reduced copies (about 1600 pixels wide, the cuts smaller), not the 2560 by 1440 frames the gate judges. The faults were sized for that.
- **Faults painted on, not rendered.** They have crisp edges. Real render faults can be softer, and some (z-fighting, fireflies) flicker in a running game, which a still does not show.
- **One picture a reviewer.** The gate gives one reviewer a whole bundle at once (item 1.1's second review judged more than thirty pictures). Attention spread across a bundle was not tested.
- **Hook sheet only.** The KCD2 frames are on his PC and could not be reached from the cloud.
- **One reviewer per frame per run.** Repeat runs were not made. The five bases seen both clean and faulty show how steadily the same real faults are named across reviewers.
