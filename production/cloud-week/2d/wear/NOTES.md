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

4. **Every delivered mask passes on its own.** The target tests its ranges on the median of six masks and says a few kinds pass only 55 to 80 per cent of single masks (its section 8); the first full check found 15 kinds with a check under 80 per cent of single masks (rust_bleed's streak width 5 of 12, render_patch's blob size 5 of 12, wall_soot's lower-wall excess 5 of 12, the head band's course edge 6 of 12, ...). A delivered mask is used alone, so each variant keeps the first of up to 12 seeds whose mask passes every mask check of its kind (`TRIES`); the manifest records the seed kept, the seeds tried and any check still failing.

The seeds: variant N of a kind starts at seed `seed_base + 1000 N` (seed base 1990) and takes the next seed while its mask fails a check; the same seed base gives the same pixels (`make_wear.py OUTDIR --verify`).

## The check

`check_wear.py` on the third build (the one delivered): **377 rows, 0 failing in 675 s** (`checks/check_v1.json`):

- **334 kind rows**: for each kind the target's mask checks on the median of six masks at the delivered texel scale, the file checks, the refine row (the warp and the strength variation cost no check), the seed row (the same seed gives the same pixels, another seed others), and two rows this build adds:
  - **delivered**: each delivered mask passes every check of its kind on its own (33 of 33 kinds);
  - **single** (reported, not failing): the share of twelve fresh single masks inside each range. 18 kinds have every check at 80 per cent or more; 15 have one or two under it, the lowest rust_bleed's streak width (5 of 12), render_patch's blob size (5 of 12), wall_soot's lower-wall excess (5 of 12) and the head band's course edge (6 of 12). These are why the seed selection exists; the target's section 8 names the same few.
- **31 of the target's deliberately wrong masks refused**, each by its named check where the target names one.
- **12 composition checks** run on this unit's own masks (`self_check.composition` with `masks`).

Earlier builds: the first failed 6 (the foot and head bands' brick-course edge and the sign ghost's peak, which the strength variation slid; they now take the warp only); the second passed 344 of 344 before the seed selection and the delivered rows were added.

Rebuild and re-check: `python make_wear.py OUTDIR` (about 2 minutes), then `python check_wear.py OUTDIR --write checks/check_v1.json` (about 11 minutes).

Previews: `production/previews/cloud-week/wear/` (`wear-walls-runs`, `wear-walls-surface`, `wear-ground`, `wear-iron`: each kind's variants 0 and 1 in the target's colour over grey at 120 px/m, tiles twice over; `wear-composed-foot-head`: the brick foot and the head under a verge composed by the target's order, floor and colour rule).

Not yet done: the fresh review.
