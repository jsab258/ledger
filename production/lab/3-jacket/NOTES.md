# Lab test 3: one jacket from a pre-1929 tailoring draft

Started 7 October 2026. The method on trial: take a published draft as the exact target, reproduce its pattern pieces in code with every rule re-measured automatically, then sew and drape it on Ron's body in Blender and compare its front and side outlines with period photographs; report honestly whether the lapel holds.

Context: the builder's Marvelous Designer jacket failed its fresh review on 2 October on the cut and the lapel (production/art/clothing/md-suit-jacket/review-1-ingame-ron.md): the right lapel collapsed, the front hung as a sack, the shoulders boxy, the sleeves full. Its pattern came from FreeSewing's Jaeger, corrected by measurement. This test asks whether a period draft, followed exactly and checked, does better.

## The pieces

| Piece | File | What it is |
|---|---|---|
| The manual | [MANUAL.md](MANUAL.md), [draft-source.json](draft-source.json) | the book, its status, the draft transcribed step by step (helper, checked on return) |
| Photographs | [PHOTOS.md](PHOTOS.md) | period photographs with licences (helper, checked on return) |
| Shared tools | [../tools/draft.py](../tools/draft.py), [../tools/panel_mesh.py](../tools/panel_mesh.py), [../tools/blender_sew.py](../tools/blender_sew.py) | the draft as named points with each rule re-measured; flat pieces to sewing meshes; Blender cloth sewing, headless |
| Body | F:\LedgerTools\lab\jacket\ron_down.npz | Ron (MH_RoccoP2_Body.fbx, the builder's export of 29 September) with the arms let down from MetaHuman's A-pose to 12 degrees off vertical (pose_body.py beside it), so the drape can be compared with standing photographs |

## Log

- 7 Oct, 21:15: the sewing script tested on two squares and a box: a 30 cm gap sewn shut in 20 frames (seam gap 0.300 m to 0.000 m).
- 7 Oct, 21:25: Ron's arms let down (37 to 12 degrees off vertical at the shoulder); front and side outlines drawn from the mesh.
- 7 Oct, 21:45: photographs back (PHOTOS.md): ten kept, two set aside (possible minors; IWM non-commercial licence); no true profile survives, so the side comparison is weak. Landmarks read off front-04 and front-02 into photo-landmarks.json: they give bands (shoulder width 0.56 to 0.71 of the jacket's length, notch 0.08 to 0.18, top button 0.25 to 0.35), not one target.
- 7 Oct, 21:50: the manual back (MANUAL.md): Thornton, *The International System of Garment Cutting*, 2nd ed., c. 1911-12, archive.org scan under the Public Domain Mark. The helper first took the *Sectional System* (c. 1898) from the Antique Pattern Library, whose scans carry a non-commercial licence; set aside on the lab's word.
- 7 Oct, 22:00: the draft as code (thornton.py) and its three automatic checks:
  - **worked values**: all sixteen bracketed values on p. 54 reproduced for the book's example (to the book's own eighth of an inch: Q is 16/3 + 1/4 = 5.58, printed 5 5/8; the first check failed on that until the rounding was understood);
  - **rules**: every rule re-measured on the finished points, all hold;
  - **Plate 16**: the example draft fitted to the plate's points read off the scan (plate16-digitized.json): mean 0.15 in, worst 0.39 in (round the shoulder, where the plate draws L about 1/4 in further out than its own rule).
  - What the checks caught: **SS** was transcribed as "half waist + 1/4" (16 1/4) where the bracket says 8 1/4: half of the half waist (the helper's error, caught by the worked value); **X** read from C along GG-L put it 0.86 in from the plate's X: the "back shoulder seam" is GG-LL (my error, caught by the plate); the scye **N-RR** round the bottom read 7.4 in against the book's "say 9 1/2": it runs over the top (9.0) (my error, caught by the book's example).
- 7 Oct, 22:05: the full pattern (pattern.py): ruled points by rule; curves, lapel, fish, buttons from Plates 16, 46 and 49, graded stretch by stretch between ruled points (a first global warp waved the side seam and twisted the under sleeve once Ron's 2 3/4 in waist suppression moved points unevenly; replaced). Seam checks (pattern_check.py): side seams, shoulder ease (1/4 in, once X was applied to the curved seam's length as the plate shows), fish, forearm and hind-arm seams, sleeve head ease, collar to neck: all pass for the example and for Ron.
- Judgements the text leaves open, taken and recorded: the collar's fall (printed "1 8/8"; German 3 3/4 cm; plate about 1 3/4) taken as 1 5/8 in; the back side seam's second printed rule (in all three languages) over the first (English only); P, the fish's position, the lapel's width and notch, the front's rounding, buttons and pocket from Plate 16 as the text says ("Curve ... as diagram"). Thornton himself says the lapels ("turns") "set all rules at defiance" and depend on taste (p. 14).
- Ron's measures (pattern.py, RON): breast 24 3/4, waist 21 3/4, seat 23 1/4 (half, over waistcoat and trousers), natural waist length 18 1/4, length 31 1/2, across back 8 1/4, elbow 21 1/2, sleeve 33 1/2; no shoulder measures (the loop round his shoulder could not be taken reliably off the posed mesh: two tries cut the hanging arm lengthwise), so the scale is the half breast, as the Normal Model (p. 22) does.
