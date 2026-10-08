# Windows at the street's low angles: boards and slits (8 October 2026)

D = read at source or measured; I = inference.

## The pictures (D, t2 frames, 2560 px)

- Hook, near-left terrace, first ground-floor window, about 16° off the wall: upper sash 6 px of lace (120-134, warm) beside 5 px of white (151-180, neutral); lower sash 2 px of lace beside 9 px of white.
- Reverse: its left row is Mickey's ("the parade stands on the left", vignette-scene.json:822), which keeps the kit, so these faults stand. First lower sash: pane 157-175, paint 178-205.

## Causes, ranked

1. **Geometry, and it is right** (D, the kit's numbers). The near jamb hides depth/tanθ of each pane: upper glass 142 mm back, lower 190 mm, behind the empty outer track. At 16° the pane is about 60% of the upper sash's visible width, 25% of the lower's; the rest is the far lining, pulley-stile track and beads, white, facing the camera. Under 13.6° no lower pane; under 10.3° no pane, only lining and track (the slits); under 7.6° only brick ("bricked-up"). Photo 9's lower sashes at about 17° show the same band.
2. **The box is lit flat** (D/I). Across that band, photo 9 (sun): lining 220-250, inside corner 105-125, track 150-180; ours 153-180, no corner line. The kit has no baked occlusion (no COLOR_0), M_LedgerSurface no AO pin (D). All joinery is one street-long mesh, its distance field capped at 256 voxels a side (DistanceFieldAtlas.cpp:68-80): decimetre voxels against 19-38 mm channels (I).
3. **The pane is a matte card, not glass** (D). Opaque, lace RGB × net_lace 0.8; its alpha is unwired (make_base_material.py ~3763), so the holes are light grey (0.35 linear), not a dark room; F0 0.04 (make_base_material.py:3917; ShadingCommon.ush:122-125). EnvBRDFApprox (BRDF.ush:622-631), roughness 0.04, weights the reflection 0.044 head-on, 0.205 at 16°, 0.435 at 8° (computed). At eye height the lace dominates; from below (reverse) the sky, reflected at full strength since today, does. net_lace was not brought back from the 41% light (D).
4. **Gloss is not the hook's white**: that white is paint, neutral beside warm lace. Real oblique panes under overcast are pale too (photo 3: panes 200-211, frame 205, sky 222, D); they read as glass by what they carry (eaves, wires, net folds) and the frame's dark corner lines.

## The professional method

- At grazing angles glass reads by reflection (one surface: 26% at 75°, 39% at 80°, computed); interior mapping is faded out there (Forza Horizon 4; shop-window-interiors/CLOSE-RANGE, OPENED there), and the reveal hides any room box.
- Kit joinery carries its small-scale occlusion baked, by trim sheet or vertex colour (WINDOWS-FACADES: Godillon, Olsen, both O), not left to real-time light. Lumen multiplies a material's AO into its sky and bounce light (LumenScreenProbeGather.usf ~1347-1352, ~1442-1446; MaterialAO on, .cpp:126-131; multi-bounce albedo capped at 0.5, LumenScreenSpaceBentNormal.cpp:56).

## Recommended change: shade the window box

Bake ambient occlusion for the checked sash with its brick reveal as occluder (faces cut to about 10 mm across the box's depth); carry it in the kit's vertex-colour alpha (every other mesh, shop kit included, exports alpha 1: terrace-front.py:3285, 3327); wire vertex alpha to M_LedgerSurface's Ambient Occlusion pin. Geometry, frames and shopfronts unchanged; about a day (I).

**Expected (I):** track faces (AO about 0.5) keep about 0.68 of their light, inside corners (about 0.2) about 0.35, so the lower sash's band steps as photo 9's does: lining about 175, track about 130, corner lines about 100. Slits gain a grey core; outer faces stay.

**Test** (kit on every row for the trial): hook-day full size, the near-left terrace's first two ground-floor windows: three tones across each lower sash's band, darkest line at most 0.7 of the lining, track at most 0.85 (sRGB). Reverse-day, the left row's first three upper windows: the same. Mickey's front faces within 3 levels of the last good. Then a fresh reviewer per view. Under 7.6° windows stay brick, as photographed: a narrow point. If reverse's panes still read as slabs: lace over a dark room (picture × alpha over 0.03) under glass's two-face reflection (Specular 1).

**Unreached:** KCD2's and City Sample's window materials; an overcast box sash under 20°.
