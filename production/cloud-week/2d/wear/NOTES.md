# Wear masks of Quay Street (unit 4.5): build notes

12 October 2026, cloud week 42. Built by script from `production/cloud-week/targets/wear/target.json` (and `TARGET.md`, sections 4 to 8 and 12), the target as it stands after its second review and Jafar's ruling of 9 October. Its drawing module (`target_drawing.py`) and its reader (`self_check.py`: `measure`, `run_mask_check`, `compose_walls`, `composition`, `wrong_masks`) are imported, not edited. The target is untouched. The masks are not in git (`production/previews/cloud-week/wear/` holds the review previews); one command rebuilds them.

## What was made

| File | What |
|---|---|
| `make_wear.py` | the one command. Reads the target and writes every mask and `manifest.json` into the folder it is given |
| `wear_common.py` | loads the target, its drawing module and its reader under their own names; the seeds, the wrap behaviour of a kind, a noise helper |
| `check_wear.py` | the check (below); `checks/check_v1.json` is its result |
| `make_previews.py` | the reduced JPEG previews: a contact sheet per group of kinds, and the composed brick foot and head |

The set: **33 kinds, 165 masks** (each kind's own `variants.count`: 3 to 10), one 16-bit greyscale PNG each: 65535 is the kind's full effect (mask 1.0), row 0 is the top of the decal frame, at the kind's recommended texel scale (`texel.px_per_m_recommended`: 25 px/m for the soot tile, 1120 for the hairline cracks) over the frame `mask.frame_extent_m`; `manifest.json` gives for each file the kind, variant, seed, size in pixels and metres, px/m, how it repeats (a seamless 2 m or 4 m tile, a tile along the wall, or a stamp), the origin text, the tone rows (mark colour and multiplier per surface), the wet and dry multipliers, the variants' differences and the SHA-256 of the pixels. **Wet and dry are not separate masks**: the target makes them multipliers on the tone (`wet_dry`), applied by the material at run time; the manifest carries them beside each kind.

## How a mask is made

1. **The envelope**: `target_drawing.kind_envelope(tj, kind, seed, variant)`: the kind's rule of place, size and shape in millimetres (filled polygons with a level and a role: streaks that fall from a sill and fade, a foot band that slides by whole 75 mm brick courses, rivulets of unequal gaps and lengths, the pipe's patches laid by area quota, Voronoi cracks, discs, speckle bands, flake fields, ...), seeded from (seed, kind, variant).
2. **The raster**: `target_drawing.rasterize(polys, extent, px_per_m, edge_10_90_mm, wrap)`: levels from the lowest up, then a Gaussian blur giving the kind's stated 10 to 90 per cent edge; wrapped for a seamless tile and along x for a tile along a wall.
3. **What this unit adds** (`make_wear.refine`): the edges are warped by a few tenths of a millimetre of noise (so that no edge is a ruled polygon's), and a soft kind's strength varies a little inside its marks (up to 12 per cent, in patches five times its smallest feature; wrapping where the kind tiles). Hard-edged kinds (cracks, flakes, discs, lines) and the kinds whose checks read where a level crosses a threshold (the foot and head bands on their brick course, the salt, the gutter, the sign ghost) get the warp only: a strength variation slid their band's edge off the course line in the first try (the check showed it).

The seeds: variant N of a kind has seed `seed_base + 1000 N` (seed base 1990); the same seed gives the same pixels (`make_wear.py OUTDIR --verify`).

## The check (stopped 12 October)

`check_wear.py` on the second build: **344 rows, 0 failing in 585 s**: for each kind the target's mask checks on the median of six masks at the delivered texel scale (301 rows with the file checks, the refine row that says the warp and the strength variation cost no check, the seed row), **31 of the target's deliberately wrong masks refused** (each by its named check where the target names one), **12 composition checks** run on this unit's own masks (`self_check.composition` with `masks`). The first build failed 6 (the foot and head bands' brick-course edge and the sign ghost's peak, because the strength variation slid them; they now take the warp only). Not done: no fresh review, the single-mask shares are reported in the check rows but not summarised here, `checks/check_v1.json` is not written (`python check_wear.py OUTDIR --write checks/check_v1.json`, about 10 minutes), the previews are not in `production/previews/cloud-week/wear/`.
