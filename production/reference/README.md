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
| `hook-sheet.png` | **THE HOOK SHEET, from 22 September.** One full-frame street photograph, 2048 x 1088: Quay Street from the south end looking north, Mickey's cab office the nearest bay on the left, the parade running away up the left, the street opening out on the right, contour terraces at the far end. It IS the street panel; there is no poster around it. | Pass 4 of the regeneration Jafar ordered on 22 September, approved by him that night. `production/art/compare/hook-2026-09-22/hook22_street_p4.png`, made by `tools/imagegen` (stable-diffusion.cpp, MIT) running Z-Image-Turbo (Apache-2.0) on Jafar's machine from `tools/imagegen/hook-sheet-2026-09-22.json`, a prompt written from canon and the town form bible rather than from the old one. Nothing fetched, nothing purchased. |
| `hook-sheet-2026-09-09-retired.png` | The sheet it replaced: a 688 x 1024 poster, two panels, swatches. **RETIRED 22 September.** Kept so the audit of it can be read against it, and for nothing else. | Approved 9 September; its prompt turned out to be Codex's retired prompt translated, which is why it drew a pub (`hook-sheet-audit.md`). |

## What on the current sheet may not be cited, ruled by Jafar 22 September

- **The second MICKEY'S sign**, on the white fascia of the shop next to the
  cab office. There is one Mickey's; the model lettered its neighbour too.
- **The third car** at the kerb outside the cab office. A rank is one or two
  (his ruling of the same day); three is the model's.

**THE SATELLITE DISH IS CITABLE.** The small dish high on the wall above the
cab office is not a flaw: the household research records dishes as new and
contested in 1990, so it belongs in the street.

The other two panels generated alongside it - the working basin and the
shopfront study - are banked with it in `production/art/compare/hook-2026-09-22/`
and are NOT the reference. Only the street panel was approved.

THE STREET PANEL IS THE WHOLE IMAGE now, and `tools/hook-pair.py` says so on
every run (`sheetMode=panel`): it tells a poster from a photograph by whether
all four corners are paper, and prints which it decided.

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
