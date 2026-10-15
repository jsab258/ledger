FAIL

# Wear masks of Quay Street (unit 4.5): second and last fresh review, one view (the masks as wear)

12 October 2026. The reviewer looked at the v2 contact sheets, the composed foot and head, and every variant of the nine changed kinds at full size in `wear2/v5`, measured with numpy. `checks/check_v2.json` had not landed and was not read. Findings 1 to 3 fail it: they show at every downpipe, at every poster site and at the foot of every painted front.

## The first review, finding by finding

1. algae_downpipe: **partly fixed.** The patch is on the shoe (0.32 to 0.51 m wide at 0.02 m up) and the moss is on joints near it. The run is still a ruled cone, and the patch rises too little (finding 1).
2. render_patch: **fixed**, six distinct types. v4 merges (finding 5).
3. Streak banding: **fixed.** The strongest column of every sill, coping and rust variant moves at most 0.005 a texel, against steps of 0.05 to 0.10.
4. poster_remnant: **partly fixed.** The layers, tears, intact shares and strips are right. The rim is a closed frame (finding 2).
5. tyre_scuff: **fixed.**
6. gutter_grime: **fixed.**
7. paint_flake: **partly fixed.** The crazing on/off, the flakes on cracks and the stallriser rule are done. The shapes still contradict the photographs (finding 3).
8. Narrow points: a and b fixed; c, d and e unchanged, and they pass.

## Findings, worst first

1. **algae_downpipe: the patch hardly rises; the run is a floating cone.** WHAT: v0, v2 and v4 rise 0.20, 0.25 and 0.23 m (mask 0.5 connected to the shoe), where the rule says 0.4 to 1.2 m. So in the composed foot the patch sits inside the dark splash band and shows only as a green tinge. The run (v0, v2) is a straight-sided cone, 0.05 m wide at 0.58 m widening to 0.12 m. It peaks at 0.65 at its top and fades to 0.14 to 0.19 at 0.26 m, so a pale neck parts it from the patch: a spike on a dome. It is visible (0.25 or more) for 0.20 to 0.24 m; the rule says 0.5 to 1.5 m. WHERE: v0, v2, v4. WHOSE: the maker's `algae()`, which draws no upper blob when n is 1 and gives the run the streak fade (head_frac 0.15). FIX: (a) Draw 1 to 3 upper blobs, never 0, adding blobs by the same rule until the top is at least 0.4 m. New check `algae_rise`: without the run, the highest row at 0.5 or more connected to the shoe is 0.4 to 1.2 m up, in every variant. (b) The run: y0 uniform 0.9 to 1.35 m, its centre within 0.03 m of x 0. w0 is 0.08 to 0.12 m, widening to 0.15 to 0.30 m: the target's 0.1 to 0.3, because a 0.03 m top hides behind the 68 mm pipe. It runs down to half the patch's height, with `core` 0.8, `head_frac` 1.0 (no fade) and wander 15 mm. New check `algae_run` (v0, v2): on the run's axis, every row from the patch top to y0 − 0.05 m is at 0.5 or more, over at least 0.5 m.

2. **poster_remnant: the paste ghost is a picture frame.** WHAT: In v0, v1, v3 and v4 the rim at 0.25 is one closed, even, ruled rectangle standing apart from the paper; v2's breaks only under a layer. It is +8 L* on brick and +11 on dark timber: a pale frame drawn round every site. In v0, two tears leave an arrowhead pointing right. WHERE: all five; v0's right edge. WHOSE: the maker's `poster()`, following the first review's too-literal "rim". FIX: The rim is 2 to 4 runs covering 30 to 60 % of the perimeter in all, starting at uniform points along it. Each run is 10 to 40 mm wide, varying by smooth noise of wavelength 0.1 to 0.3 m, at level 0.25. There is no rim elsewhere. A tear leaving a corner under 70 degrees is redrawn, up to 10 times, then dropped. New check `poster_rim`: of the outer 40 mm band outside the layers, 0.3 to 0.6 is at 0.15 or more.

3. **paint_flake (and render_crack): seed-shaped flakes and a ruled crack net.** WHAT: Every flake is a smooth lens or seed. The target's photographs (`ph-peeling_painted_wall`, `ph-preconcrete_wall_001`) show angular chips with straight broken sides. The crazing is straight Voronoi edges, 0.1 to 0.2 m long, meeting at 120 degrees: a polygon net, where the photographed cracks wander every few centimetres. render_crack's map cracks (v0, v3, v5) use the same primitive. The timber variants (v3 to v5) point their flakes every way like scattered rice; on timber, paint splits along the grain. WHOSE: the target's `blob()` (low noise modes) and `voronoi_cracks()` (3-point ribbons), used by the maker's `flakes()`. FIX: (a) Flakes: `blob(..., n=rng.integers(6, 10), rough=0.35)`, straight sides kept; big sheets n 12 to 16, rough 0.4. (b) Wrap `voronoi_cracks` in `install()` as `streak` is: resample each centre line every 5 mm and offset it sideways by smooth noise of amplitude 0.06 × the edge length (at least 3 mm) and wavelength 25 to 50 mm, with the ends fixed. (c) v3 to v5: flake angle normal(0, 8 degrees) about x. Placer: x along the grain, in the target's 90-degree steps. Re-run both kinds' checks.

4. **rust_bleed: the halo is a flat disc.** WHAT: The halo is a plateau at exactly 0.18 from 15 mm out to 35 to 55 mm, then it falls to 0 within 9 mm: a crisp circle round every fixing. The rule says diffuse, and the rust photographs show no ring. It is −7 L* on render, −8 on light timber and −5 on stone. WHERE: v0 to v4. WHOSE: the target's envelope (`circle` at `halo_level`). FIX: 12 nested discs. Disc i (0 to 11) has radius R × (12 − i)/12 and level 0.18 × ((i + 1)/12)^1.5, where R = h/2, centred 0.3 R below the fixing.

5. **render_patch v4: two smooth lumps, not a loss cluster.** WHAT: The 4 to 9 losses merge into two smooth pieces, eqd 261 and 121 mm. `ph-damaged_plaster` shows many separate ragged losses. Nothing keeps v4 (render loss) off brick, or v5 (a brick) off render. WHOSE: the maker's `render_patch()` (scatter σ 110 by 90 mm). FIX: Scatter σ 150 mm in x and 110 mm in y. Redraw a loss (up to 50 times) that comes within 15 mm of another. Outline n 9, rough 0.45, inside the frame less 20 mm. New check: 4 to 9 pieces of 800 mm² or more at 0.5. Placer: v4 on render_cream only; v5 on brick_red and brick_painted only, on one of the target's brick cells (0.215 by 0.075 m, stretcher bond from the pavement line).

6. **Narrow points (pass):**
   a. **The sill and coping washes are flat trapezoids** at 0.18, with a straight lower edge 1.1 to 6 m long. That is −1.3 to −1.8 L*, and the coping's lies under the head band. FIX: the level falls linearly from 0.18 to 0 down the wash in 5 mm slices, and the lower edge moves ±20 mm by smooth noise.
   b. **The gutter fringe steps**: 40 mm plateaus at 0.115, 0.105, 0.095, 0.075 (1 to 1.3 % contours). FIX: levels interpolated every 5 mm.
   c. **Moss orientation**: draw perpend candidates vertical and bed-joint ones horizontal.
   d. **render_patch v3's smear** falls under 0.25 within 50 mm: faint.
   e. **Rust trickles are clean lines**, where the photograph's are broken; at 5 to 20 mm they pass.

## What the masks alone cannot show

The colours, and wet and dry. Also: whether moss, salt and v5 land on the wall's real courses; the run beside a real pipe (salt bricks cover it in the composed foot); the placer rules; mipmapping beyond 6 to 8 m. No era or content breach was seen: no words, bottles, cans or slips.
