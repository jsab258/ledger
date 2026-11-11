# Sheila's cardigan from Tom's jumper, carried and skinned to MH_LenaS4 (11 November 2026)

Step 3 of SHEILA-REFIT-PLAN-2026-11-09.md. Files in F:/LedgerTools/garments/sheila/cardigan-s4-2026-11-11/ ("F:"). Blender 5.2.2 headless. About 3.2 h. Nothing imported into Unreal.

## Made
- Source: garments/tom/jumper/chain-j3d/game/jumper_game.blend, object "jumper" (9,860 points, 19,480 triangles).
- **F:chain2/skinned/sheila_cardigan_s4_skinned.fbx** (10,226 points, 19,624 triangles, no lower LODs, 69 bones). Chain: carry, resize_bands, build_cardigan, clear_layers, follow_cloth, skin_garment (F:scripts/run_chain.sh, scripts named below).
- Pictures: F:chain2/pic/final-front, -back, -side, -threeq.png (workbench; blouse's outer layer pale, head blue).

## Tries and results
1. Carry Tom L1 to S4 (carry_garment.py): try 1 passed; mean move 153.6 mm, 490 points pushed out, at most 86.7 mm. The carried crew neckband sat inside the head and its hole was 60 mm wide, so it was not kept.
2. Welt and cuffs: Tom's measured 70.8 / 64.7 mm (welt front/back) and 70.2 mm (cuffs). Cut to 50 and 60 mm toward their seams (F:scripts/resize_bands.py): passed. Side effect: the welt's UV density is now 0.7 of its height (rib stitches 1.4 times too flat there).
3. Cardigan cut (F:scripts/build_cardigan.py): neck hole an ellipse about her neck from her head mesh (a 82, b 62 mm); V apex z 1.25 m (casting sheet, blouse note), corners 59 mm each side; centre front column of cells removed; one 29 mm band (3 rows, rib material, 0.72 m a side) lofted on the intact surface from the hem up the centre front, the V and round the neck, 1.5 mm proud; seven 13 mm buttons (material "Button", z 1.004 to 1.246, 40 mm apart). Passed in one try. Bands use the front welt's rib island in the packed map (both sides share it; UV overlap with the welt); buttons sit on one point of it.
4. Clear over the blouse (clear_layers.py): try 1 over the skinned blouse failed unseen: the blouse is a two-layer shell, so its signed test read the inner layer (half the blouse's outer points stood out through the cardigan, mean 12 mm). Try 2 over the blouse's outer layer only (F:blouse-outer/): passed in the main. Bands and buttons then take the cloth's displacement (F:scripts/follow_cloth.py). Head: without it 8 collar-neck points inside the head (14.3 mm); with the back clearance only (--head-below 1.30, --head-back-below 1.50; the front clearance moved points 237 to 1,006 mm and was dropped) 4 points inside, 2 over 3 mm, deepest 6.5 mm, z 1.44, back of the neck. Two tries spent: **open fault**.
5. Skin: skin_garment.py --piece-attr none, try 1 passed: notButtons empty; uvReordered true; skirt rule touched 183 hem points (hem 0.856 m, hip joint 0.892 m).
6. Blouse through the cardigan at the hem: a cover step (F:scripts/cover.py) diverged twice (worst 11.8 mm to 23 mm). Stopped: **open fault**.

## Checks (F:chain2/pose/parity-check.json, ray parity)
- Body through cloth over 3 mm: rest 0; arms down 483 (deepest 33.0 mm); walking 306 (28.8); seated 360 (32.0). All at the trunk's sides z 0.9 to 1.3, cloth inside the lowered arm, as the blouse (1,044 / 665 / 880).
- Blouse points through the cardigan (outer layer, rest, below z 1.37, not near an edge): 176 over 1 mm, 94 over 3 mm, at most 11.8 mm; 29 of them at z 1.0 to 1.02 (the blouse's lower edge, front centre and sides, white lump above the bottom button in the picture).
- Head: nearest cloth 0.4 mm; 4 inside, 2 over 3 mm (above). Checked by ray parity against the face DNA mesh, not the 1 mm grid.
- Triangles 19,624 (cap 40,000). lower_neckband.py not used (no crew band).

## Open faults
- Blouse hem lump through the cardigan at z 1.0 (two tries).
- 2 collar points 3 to 6.5 mm in the head, back of the neck (two tries).
- Seated and arms-down cloth inside the arm, not worked on.
- Welt UV density; band UV overlap; no overlap of the two bands at the centre front (butted); rib bake of the old welt island not remade; button and knit colours set at import (beige tint, "Button" slot).
- Hand-knit stitch scale from her UV scale not measured.

## Tool changes described (not made)
- clear_layers.py should say when its under garment is a two-layer shell, or take only the outer layer; its head clearance cannot take a V neck.

## Fixes after the packaged film (11 Nov, 17:25 to 17:45; both try 1 of 2)
- Left band culled in the game: build_cardigan.py now turns every band face whose normal opposes the knit under it, and stops the build if any remain (bandOrient in F:chain3/build/build.json: 468 faces, 238 turned, 0 after). Skinned file: rib faces facing against the knit, her left 211 to 0; her right 58 to 41 (those 41 are welt and cuff rib, drawn correctly in the film; the measure takes the nearest knit). Chain3 skinned and imported (garments.json points at chain3).
- Blouse through at the shoulders: the trim's collar guard kept every face above z 1.33 and its checks stopped at 1.37, so the shoulders were never cut nor measured. trim2.py (F:blouse-under-cardigan-2026-11-11/trim2.py, output v2/) keeps the collar's two islands (fall 1,795 and stand 1,318 faces) and cuts the blouse body above 1.33 wherever it is covered by, or pokes through by at most 20 mm, the cardigan, its edges included. Faces 35,845 to 7,370; V opening census unchanged (897 cardigan, 251 blouse, 0 body). Pokes past 15 cm from the centre above 1.30: 64 to 0. Pictures F:blouse-under-cardigan-2026-11-11/v2/pic/cmp-all.jpg (before left, after right): back and front shoulders clean; in the three-quarter view a little white remains by the far shoulder (collar or fault: the packaged film decides). Imported.
- Lesson: a guard band in a trim must be measured too; the check's own z limit hid the fault it guarded.
- Packaged film of f14197e (18:21, MouthFilm-close-1111c, preview production/previews/sheila-held-film-2026-11-11b.jpg): both fixes PASS (both rib bands drawn; no blouse through at the shoulders). New close faults: (c) the cardigan's neckband top shows as dark jagged shards at the collar's top corners by her neck (the head clearance's ragged cut, seen in Blender pictures since chain2); (d) the collar's lower edge ragged white on her left (blouse body by the cardigan's neck edge). Try 1 on them, a collar lift to 2.5 mm over the cardigan (F:blouse-under-cardigan-2026-11-11/trim3.py, v3/, not imported), missed: the shards sit above the collar, not under it. Next: lower or trim the cardigan's neckband under the collar (tools/meshgen/blender/lower_neckband.py first), and cut the blouse body's faces by the cardigan's neck edge outside the collar.
