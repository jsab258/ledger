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
