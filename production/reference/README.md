# The references

THE ONLY PLACE A REFERENCE LIVES. Every tool, recipe and check that compares
our work against an approved picture reads from this directory and from
nowhere else — no branch, no `git show`, no second copy beside a recipe.

WHY THE RULE IS THIS BLUNT. Jafar's ruling of 9 September made the in-house
Hook sheet the reference and retired Codex's. `tools/hook-pair.py` and
`tools/art-recipes/lighting-column.py` stayed hard-wired to Codex's file at
`production/art/atlas-01/concepts/hook.png`, and THAT FILE STILL RESOLVES on
the art branch — so nothing errored, nothing warned, and a week of comparisons
went to the wrong picture in silence. A reference that resolves is not the same
as a reference that governs. One path, and a tool that refuses when it is
empty, is the only version of this that fails loudly.

## What is here

| file | what it is | where it came from |
| --- | --- | --- |
| `hook-sheet.png` | THE HOOK SHEET, the visual bar for stage 1. A poster: title, a harbour panel, the STREET panel, a material swatch strip, object studies. 688 x 1024. | `production/art/compare/hook-2026-09-09-pass2/hook_pass2.png`, approved by Jafar on 9 September. Made in house by `tools/imagegen` (stable-diffusion.cpp, MIT) running Z-Image-Turbo (Apache-2.0) on Jafar's own machine. Nothing fetched, nothing purchased, no third-party asset was an input. Its provenance record is `ATTRIBUTION.json` beside the original. |

THE STREET PANEL IS THE LOWER PHOTOGRAPH and is what stage 1 is judged on:
our street from that panel's own viewpoint, beside it, in daylight as it is.
`tools/hook-pair.py` finds the panel by measuring the sheet rather than by
typed pixel coordinates, so a re-export at another size still works.

## The second reference, and why it is a page of links

`photographs.md` is the other half. THE SHEET GOVERNS MOOD, PALETTE AND
COMPOSITION; THE PHOTOGRAPHS GOVERN WHAT THINGS ACTUALLY LOOKED LIKE; WHERE
THEY DISAGREE, THE PHOTOGRAPHS WIN (Jafar 2026-09-22). It holds no images:
every period photograph the research cites is under photographer copyright
with no open reuse licence established, the research's own `RIGHTS.md` says
they are "linked rather than redistributed", and the allowlist fails anything
untagged. So it links them and says what each one establishes.

`hook-sheet-audit.md` is the check nobody had done: the sheet against the
research and canon, sorted into what it gets right, what the image model
invented, and the four things that contradict a ruling and are no longer
citable - the pub, the timber-only shopfronts, the narrowboats, and the
free-standing corner building.

## Adding one

Copy the approved file in, add a row above saying what it is and where it came
from, and point the tool at the path. Do not leave a copy anywhere else.
