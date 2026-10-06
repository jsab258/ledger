# Atlas 01: Meridian's map

Start with [ADOPTED-2026-10-06.md](ADOPTED-2026-10-06.md): what was adopted on Jafar's ruling of 5 October 2026, what was left out and why, and how the map was updated to the built street. The map's data is [data/atlas.json](data/atlas.json).

Draw and check, with the existing Python (standard library only; no network, no GPU):

```text
python production/art/atlas-01/scripts/draw.py --out F:/LedgerTools/atlas-01-<date>
python production/art/atlas-01/scripts/check.py --out F:/LedgerTools/atlas-01-<date>
```

draw.py writes SVGs outside git; check.py writes verification.json. Pictures never go into git except reduced previews in production/previews/ (tools/make_preview.py). The branch's own pictures (concepts, previews, references, artwork) are archived unchanged in F:/LedgerTools/atlas-01-2026-09-22.

REVIEW.md and the lighting-column, pair, street and terrace-front folders beside this file are the studio's earlier files, not part of the atlas branch.
