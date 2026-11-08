# Review: proposed additions to the game-garment skill (8 November 2026)

Verdict: **PASS WITH FIXES** (8 faults, none a wrong number).

Checked: every figure against KNIT-PLAN, the four review files (round 1 and r2), import_garments.py, garments.json (RonJumper, DarrenJumper, TomJeans), lower_neckband.py and band.json, garments_shipped_check.py and ci-checks.sh, body_full_layout.py, clear_layers.py, DECISIONS 7 Nov 17:40 to 8 Nov 14:25 and RECIPE 1892 to 1930 (grep only), the two memory notes, the asset-import skill and RULINGS (Clothes). Tints, UV scales, tiling 2.0 and 1.8, 3 px/mm, 22 mm, 98 of 159 and 11.1 mm, S6's 25,328 of 32,334, 37 and 64 mm, the false 9.6 mm reading and the three film angles all match their sources.

## Faults

1. **Addition 1, bullets 1 and 3.** Mafia's 7.1 cm repeat and its 3.6 px/mm stand in the skill text with no unverified mark. The mark is only in the proposal's footer, which the skill will not carry. A fresh session could also take 7.1 cm as the target, when the repeat used is 66.5 cm (KNIT-PLAN step 2; DECISIONS 11:03). Fix: add "(Mafia's UV set unverified)" to both bullets and say that stitch size and px/mm are matched, while the repeat length follows the tile.

2. **Addition 1, bullet 4.** The bullet leaves out that a rib is drawn only beside a "detail" map and shares its tiling (import_garments.py line 84; selftest lines 291-295). Fix: add "needs a detail map in the same row; it uses that map's tiling".

3. **Addition 1 check and Addition 6.** Both ask for "one fresh reviewer per man", but the skill's step 9 check asks for one per view. That is a contradiction a fresh session cannot settle. Fix: say that one reviewer per man covering all his views is allowed for a medium piece (RULINGS 3 Nov, reviewers sized to the piece), or keep one per view.

4. **Addition 3, placement.** Step 4 covers Marvelous's elastic. This is a Blender fix on a skinned mesh after a carry (lower_neckband.py docstring). Fix: move it into "A refit to another body", after Addition 4.

5. **Addition 4, bullet 3.** "Carry the footwear before the trousers and the trousers before the top" is written as a sourced rule, but no source says it. DECISIONS 18:45 and clear_layers.py say only that the carry ignores the garment beneath and that clear_layers needs `--over UNDER`. The 6 mm and 8 mm also differ from the tool's defaults (`--body-clear 0.008`, `--over-clear 0.005`). Fix: reword it as "carry the garment beneath first, since clear_layers.py's --over needs it", and name the flags with the values used.

6. **Addition 4, bullet 4, citations.** "Pose-test pictures draw body and cloth one grey" comes from the memory note head-mesh-reaches-the-chest, not from RECIPE. His yes of 20:09 is recorded in DECISIONS 7 Nov 21:28, not in an entry timed 20:09. Fix: cite the memory note and DECISIONS 21:28.

7. **Addition 5.** It repeats the asset-import skill's step 5: only mh-assemble reaches the game, and mh-dress does not (asset-import SKILL.md line 53). It also dates the wasted build 7 Nov (memory note), while garments_shipped_check.py's docstring says 2 November, "cost a night". Fix: keep the project's name and the garments_shipped_check sentence, point to asset-import step 5 for the rest, and drop the date or give both sources.

8. **Addition 6.** "A meant iron cover" is not in the source. RECIPE (8 Nov, the judged garment) says "a flat dark cover". Fix: say "a meant flat dark cover".

## Notes, not faults

- The unverified list names the reviewer's "about 4 mm" stitch, which no addition uses. It can go.
- No addition claims that the night's packaged walk has passed. That is honest, and the footer says the walk is not yet read.
- Additions 2 and 6 sit in the right sections. A fresh session could follow all six once the fixes are made.
