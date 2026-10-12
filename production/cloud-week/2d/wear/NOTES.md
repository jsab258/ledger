# Wear masks of Quay Street (unit 4.5): build notes

12 October 2026, cloud week 42. Built by script from `production/cloud-week/targets/wear/target.json` (and `TARGET.md`, sections 4 to 8 and 12), the target as it stands after its second review and Jafar's ruling of 9 October. Its drawing module (`target_drawing.py`) and its reader (`self_check.py`: `measure`, `run_mask_check`, `compose_walls`, `composition`, `wrong_masks`) are imported, not edited. The target is untouched. The masks are not in git (`production/previews/cloud-week/wear/` holds the review previews); one command rebuilds them.

## What was made

| File | What |
|---|---|
| `make_wear.py` | the one command. Reads the target and writes every mask and `manifest.json` into the folder it is given |
| `wear_common.py` | loads the target, its drawing module and its reader under their own names; the seeds, the wrap behaviour of a kind, a noise helper |
| `check_wear.py` | the check (below); `checks/check_v1.json` is its result |
| `wear_departures.py` | where this unit departs from the target's drawing after the fresh review (below), and the review's new checks |
| `make_previews.py` | the reduced JPEG previews: a contact sheet per group of kinds, and the composed brick foot and head |

The set: **33 kinds, 165 masks** (each kind's own `variants.count`: 3 to 10), one 16-bit greyscale PNG each: 65535 is the kind's full effect (mask 1.0), row 0 is the top of the decal frame, at the kind's recommended texel scale (`texel.px_per_m_recommended`: 25 px/m for the soot tile, 1120 for the hairline cracks) over the frame `mask.frame_extent_m`; `manifest.json` gives for each file the kind, variant, seed, size in pixels and metres, px/m, how it repeats (a seamless 2 m or 4 m tile, a tile along the wall, or a stamp), the origin text, the tone rows (mark colour and multiplier per surface), the wet and dry multipliers, the variants' differences and the SHA-256 of the pixels. **Wet and dry are not separate masks**: the target makes them multipliers on the tone (`wet_dry`), applied by the material at run time; the manifest carries them beside each kind.

## How a mask is made

1. **The envelope**: `target_drawing.kind_envelope(tj, kind, seed, variant)`: the kind's rule of place, size and shape in millimetres (filled polygons with a level and a role: streaks that fall from a sill and fade, a foot band that slides by whole 75 mm brick courses, rivulets of unequal gaps and lengths, the pipe's patches laid by area quota, Voronoi cracks, discs, speckle bands, flake fields, ...), seeded from (seed, kind, variant).
2. **The raster**: `target_drawing.rasterize(polys, extent, px_per_m, edge_10_90_mm, wrap)`: levels from the lowest up, then a Gaussian blur giving the kind's stated 10 to 90 per cent edge; wrapped for a seamless tile and along x for a tile along a wall.
3. **What this unit adds** (`make_wear.refine`): the edges are warped by noise of 0.35 to 1.6 texels (0.5 mm on the flakes, 18 mm on the soot tile, 40 mm on the paint fade: it softens an edge; it does not unrule a straight side, which is why the review's findings 4 and 6 needed new drawing), and a soft kind's strength varies a little inside its marks (up to 12 per cent, in patches five times its smallest feature; wrapping where the kind tiles). Hard-edged kinds (cracks, flakes, discs, lines) and the kinds whose checks read where a level crosses a threshold (the foot and head bands on their brick course, the salt, the gutter, the sign ghost) get the warp only: a strength variation slid their band's edge off the course line in the first try (the check showed it).

4. **Every delivered mask passes on its own.** The target tests its ranges on the median of six masks and says a few kinds pass only 55 to 80 per cent of single masks (its section 8); the first full check found 15 kinds with a check under 80 per cent of single masks (rust_bleed's streak width 5 of 12, render_patch's blob size 5 of 12, wall_soot's lower-wall excess 5 of 12, the head band's course edge 6 of 12, ...). A delivered mask is used alone, so each variant keeps the first of up to 12 seeds whose mask passes every mask check of its kind (`TRIES`); the manifest records the seed kept, the seeds tried and any check still failing.

The seeds: variant N of a kind starts at seed `seed_base + 1000 N` (seed base 1990) and takes the next seed while its mask fails a check; the same seed base gives the same pixels (`make_wear.py OUTDIR --verify`).

## After the fresh review (REVIEW-v1.md, FAIL, 7 findings and 5 narrow points, 12 October)

Every finding was in the target's own drawing (`target_drawing.py`), which this unit had carried over unchanged. The target is not edited (Jafar's ruling of 11 October: no more polishing of targets); `wear_departures.py` draws the kinds below with the target's own primitives instead, and records why:

1. **algae_downpipe**: the first patch stands on the shoe (its lower edge at y = 0, 0.3 to 0.65 m wide: the rule's 0.9 m is past the target's own size check, eqd 450 mm), the others overlap it and narrow upward; the moss is 18 to 44 patches of eqd 5.5 / 10.2 / 31.5 mm on the bed joints and perpends within 0.15 m of the patch and below 1.2 m (none in variant 3: "moss on/off"); the run from a leaking joint (variants 0 and 2) is 0.03 to 0.05 m wide at the joint and widens to 0.1 to 0.3 m as it falls. New check `algae_shoe`: mask 0.5 or more over at least 0.3 m at 0.02 m up, every variant.
2. **render_patch**: one of the target's own six types per variant: v0 a rectangle, v1 an L (one corner cut, 40 to 60 per cent of each side), v2 a cut chase (0.06 to 0.12 by 0.4 to 0.7 m), v3 a square with a smear tail at 0.4, v4 a cluster of 4 to 9 losses (33 / 67 / 294 mm) and no patch, v5 one replacement brick (0.215 by 0.065 m; the target's coverage check, 10 per cent of the frame, is not applied to it).
3. **Every streak fades continuously**: the target's `streak()` fades in 5 to 14 flat slices (steps of 0.05 to 0.10 every 50 to 80 mm, seen as banding down a sill); it now takes one slice per 5 mm of length (the module's own function, wrapped).
4. **poster_remnant**: a paste-ghost rim at 0.25 (10 to 40 mm wide) round the site; 2 to 4 layers at 0.6 to 1.0, the first covering 20, 40, 70 or 40 per cent of the site by variant, each torn by 1 or 2 ragged tears at 30 to 60 degrees that take a corner or an edge (the larger part stays); v4 is 2 to 5 strips, 30 to 120 mm wide. New checks `poster_intact` (the share of the site at 0.5 or more is the variant's fraction +/- 0.1) and `poster_strips`; they replace the target's `coverage_of_decal` (0.25 to 0.75 of the frame), which assumed one whole sheet.
5. **tyre_scuff**: radius 2, 3 or 5 m or near-straight by variant; strength 0.45 + 0.55 x smooth noise (0.3 to 0.8 m) along the arc (the review asked 0.4 + 0.6; at 0.4 the peak, 0.7 x 0.4, falls under the target's length threshold of 0.3 and the scuff breaks in two); the ends fade over 0.25 m. Placer: chained stamps overlap by 0.25 m.
6. **gutter_grime**: no trapezoid "fingers" (the target's `fingers.n_per_m` 1.0 becomes 0): the rule names no such mark, and they repeated every 2 m.
7. **paint_flake**: crazing in variants 0 to 2 only (3 to 5 are for timber, where the flakes are 1.45 times the size so that they alone bare the target's 3 to 15 per cent); in 0 to 2, 60 per cent of the flakes are centred on a crack with their long axis along it (+/- 10 degrees; new check `flake_on_crack`, at least 0.5); one big sheet only in variants 1 and 4. **Placer: the stallriser's 1 m tile takes variants 0, 2, 3 and 5 only** (no big sheet repeating every metre).

Narrow points: (a) footway_infill and graffiti_buff take the warp only (`HARD`): the strength variation let the flag joints show through by up to 11 per cent; (b) the warp's size is now stated truly (above); (c) the foot and head bands step by courses in flat runs 0.3 to 0.6 m long, under the brick's own per-brick tone (placer: one 2 m tile repeats three times in a 6 m bay); (d) bird droppings are plain ovals and (e) road patches are all square covers: both pass as they are.

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
