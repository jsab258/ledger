# What came from the retired sheet, and is suspect until checked

Jafar, 2026-09-22: "Everything derived from the retired sheet is suspect until
checked, not only what you have found so far. Search for any other value, crop
or measurement that came from it and list them."

THE RETIRED SHEET is `production/art/atlas-01/concepts/hook.png` on the
`art/atlas-01` branch, 1024 x 1536, made by Codex. Jafar retired it on
9 September and it still resolves on that branch, which is how a week of
comparisons went to it with nothing failing.

This is a list of what it touched, not a list of things that are wrong. Each
row says what was taken, where it lives, and what it would take to check it.

## 1. The approved sheet's own prompt is Codex's prompt

**This is the deepest one and it was not in the first audit.**
`tools/imagegen/compare-hook-2026-09-09-pass2.json` records its own source:
branch `origin/art/atlas-01`, file `production/art/atlas-01/data/concept-prompts.json`,
key `hook`, 1599 characters, sha256 `53408df5...`, and states that only the
`not a ...` clauses were moved into the negative channel. **The in-house sheet
was generated from the retired sheet's prompt, nearly word for word.**

So three of the four contradictions the audit found were COMMANDED rather than
invented, and the audit's own wording needs that correction:

| the audit said | the prompt actually said |
| --- | --- |
| the sheet draws Mickey's as a pub | "Mickey's a SMALL SINGLE 6m-wide two-storey **PUB** ... maroon fascia MICKEY'S". The prompt asked for a pub. D19 made it a minicab office on 14 September, five days later. |
| not one metal shopfront; no signage on any fascia | "**ONLY TWO PIECES OF LETTERING IN THE WHOLE SHEET** ... every other shopfront fascia is plain unlettered **PAINTED TIMBER**". Both were specified. |
| a wooded hill closes the view | "inland town gently rising behind" - the rise was asked for; the woods and villas are the model's. |
| the basin carries canal narrowboats | The prompt said "a commercial cargo basin" and the negative already carried "pleasure marina, yacht, leisure moorings, pontoon". **This one is the model disobeying**, which is why the new prompt NAMES the craft instead of only forbidding the wrong ones. |

**Checked by:** superseded. `tools/imagegen/hook-sheet-2026-09-22.json` is
written from canon, the town form bible and the evidence ledger, with each
item's sources named in its own `governed_by`.

## 2. The whole hook camera in the governing scene spec

`production/specs/vignette-scene.json`, camera `cam_hook`:

    x_m 4.0   z_m -2.1   eye_height_m 1.65
    yaw_deg 11.0   pitch_deg -2.6   fov_vertical_deg 39.0

Its own note says every number was measured off "the LOWER PANEL of
production/art/atlas-01/concepts/hook.png on branch origin/art/atlas-01", with
the panel content area given as x 11..1012, y 662..1278 of a 1024 x 1536
sheet. The note is careful, long and honest about its uncertainties - and all
of it is about the wrong picture.

**Checked by:** HALF DONE, 22 September. The lens WAS re-derived from the
new sheet - `production/reference/hook-sheet-lens.md` - and the Blender
recipe's hook camera uses it (46 degrees vertical, level at 1.9 m, a lens
shift putting the horizon at 0.570, turned 20.4 degrees). The SCENE SPEC's
`cam_hook` above still carries the retired numbers, and it is what the
Unreal probe's hook shot and the A1 grid rows read, so moving it is a probe
change with its own tests; it is on NOW.md's list as its own item.
DONE 23 September: `cam_hook` in the scene spec is the new sheet's lens
(x -3.2, z -2.2, eye 2.0 on the quay apron, which it declares as its ground,
46 degrees vertical), with the tests that tie rows to it moved with it; see
DECISIONS.md of that day. Unreal has no lens shift, so it looks up a little.

## 3. The hook camera's field of view in the recipe

`tools/art-recipes/terrace-front.py`, `HOOK_FOV_V_DEG = 60.0`. Not derived
from the retired sheet - derived from NOTHING. It is this recipe's default for
its elevation and eye cameras and was carried across. The only field ever
derived for a Hook panel is row 2's 39.0 vertical / 59.7 horizontal, off the
retired sheet. 60 vertical on our 1.892 frame is 95.1 horizontal.

**Checked by:** 22 September. `HOOK_FOV_V_DEG` is 46.0, derived from the new
sheet's own geometry - `production/reference/hook-sheet-lens.md` says how.

The frame's ASPECT, `HOOK_RES = (1400, 740)`, is clean: 617 x 326 was measured
on the APPROVED sheet, on 21 September.

## 4. The lighting column's shape

`tools/art-recipes/lighting-column.py`. `SHEET_REF` is already labelled
RETIRED-REFERENCE, but the GEOMETRY CONSTANTS taken from that crop are not,
and they are what the mesh is built from:

    SHEET_REF["crop_px"] = "185,700,320,1000/tracedSubWindow-220,690,280,800"
    curve_vertical_fraction  ~8px / ~450px of visible pole (~1.8 per cent)
    head_width_to_height     ~23px : 7px = 3.3 : 1
    assembly_bbox_aspect     25px : 11px = 2.27 : 1
    NECK_DIAMETER_RATIO      0.8
    NECK_ARC_RADIUS_RATIO    0.6   - the file says in terms that this was
                                    picked "from the sheet", from the crop
                                    x185-320 y700-1000

The file's own note already records that three traces of that crop gave three
different answers, on a lamp twenty-five pixels wide.

**Checked by:** 22 September, and there is nothing to trace. The approved
pass 4 street panel shows NO street lighting column anywhere in it - the only
vertical on its skyline is a mast on the far hill. So the retired crop's
constants cannot be re-measured against the new sheet; they stay in the file,
labelled as the retired sheet's, and the column's SHAPE is governed by R07's
1989 photograph, "plain bent-arm lighting" (`photographs.md`), which the
column already is. Its dimensions were always written ones, not traced.

## 5. The per-asset routing index

`game-design/research/GOVERNS.md`, 17 asset families. Every row cites
`hook.png` and several say "crop-verified at 3x". All of it was read on the
retired sheet. Rerouted and marked unverified on 22 September; the CLAIMS are
still unchecked. Affected rows with a measured claim in them: street lighting
column, wall bracket lamp, road surface, pavement surface, roof, dustbin,
shopfront, window, door.

`production/research/README.md` carried the same pointer and is rerouted.

**Checked by:** 22 September. All seventeen rows re-read on the approved
sheet, in a new section of GOVERNS.md: 2 kept, 10 changed, 5 not on the
sheet. The original table is left as it was, as the record of what was
claimed.

## 6. Smaller inheritances

- `tools/citypack/shortlist-candidates.json` quotes the lighting column's
  retired-sheet crop note in its own reasoning.
- `production/art/concept-fairview-2026-09-10/fairview-sheet-2026-09-10.json`
  binds to `production/art/atlas-01/concepts/fairview.png` - a sibling of the
  retired Hook sheet, on the same branch, never re-approved.
- `tools/imagegen/compare-hook-2026-09-09.json` (pass 1) carries the same
  Codex prompt and the same source record as pass 2.

- FOUND AND FIXED 23 September: the parked cars' facing. The recipe's note
  said "seen from behind, nose north, with the traffic, as on the sheet",
  and the new sheet's cars show their FRONTS - as a British street does on
  the kerb to the right of a camera looking up it. Whether it came from the
  retired sheet or from the mirrored street Blender draws, it crossed into
  the true street the wrong way round. Turned in tools/art-recipes/
  terrace-front.py VEHICLE_AT (facing -1), with headlamps.

## What is NOT inherited

The four whole-frame colour numbers (mean, highlights, warmth, colour
fraction) were measured against the APPROVED sheet on 21 and 22 September, and
`tools/hook-pair.py` finds its panel by measuring the approved sheet rather
than by typed coordinates. They are honest measurements of the approved sheet
- which is itself now superseded, so they are due to be re-taken against the
new one, but they are not retired-sheet values.
