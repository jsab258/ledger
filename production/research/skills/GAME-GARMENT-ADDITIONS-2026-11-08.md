**Merged 8 Nov 2026** into .claude/skills/game-garment/SKILL.md, after one fresh review (GAME-GARMENT-ADDITIONS-REVIEW-2026-11-08.md, pass with fixes, all eight fixes applied below and in the skill). The skill's text is the version in force; this file records what was added, where and why.

# Proposed additions to the game-garment skill: dressing a MetaHuman, the knit jumper surface (8 November 2026)

Asked for: two items from the advisor's list of skills from phase 1's proven methods, "dressing a MetaHuman" and "the knit jumper material". Reuse first: no new skill; additions to the existing game-garment skill.

Sources, all read 8 Nov 2026: .claude/skills/game-garment/SKILL.md (whole); production/research/game-clothing-pipeline/KNIT-PLAN-2026-11-08.md (whole); F:/LedgerTools/gate/new/knit-2026-11-08/review-ron.json, review-darren.json, r2/review-ron.json, r2/review-darren.json (whole); production/orders/2026-11-02.md section 9, lines n02-9-dress-the-cast and n02-9-knit-and-neckband; DECISIONS.md by grep (entries 7 Nov 17:40 to 8 Nov 14:25); RECIPE.md by grep (7 and 8 Nov sections on the carried garment, the head mesh and the knitwear surface); CLOTHES.md by grep; the docstrings of tools/meshgen/blender/clear_layers.py, body_full_layout.py, lower_neckband.py and tools/garments_shipped_check.py; tools/ue/import_garments.py lines 74 to 84, 153 to 156, 226 to 230; garments.json rows RonJumper and DarrenJumper; the asset-import skill's section list; the memory notes import-garments-right-project and head-mesh-reaches-the-chest.

## What game-garment already covered (not repeated)

- Reuse and refit first; carry_footwear.py and carry_garment.py; re-drape for draped pieces; the Outfit Asset as the untried comparison; only touched steps rerun, skinning always.
- Drape over footwear before the trousers' hem (step 2).
- Rib bands and collars made in Marvelous; "the rib's ridges in the normal map" (step 4), with no method for the rib's surface.
- The ID-tinted material and tint (step 8); crowd variants by material values, a variants field still to be built.
- The head hidden-face map's limit (step 9); import by import_garments.py "into the MetaHuman project", unnamed.
- Packaged walk, one fresh reviewer per view, Jafar's whole-person look.

## The additions as merged

1. **Step 8, the knit's or weave's surface** (five bullets): a shared tiling detail normal set in the garment's row ("detail", "detail_tiling", "detail_strength"); the tile from home first, then CC0 (Poly Haven knitted_fleece), resampled whole and looked at as a lit card; stitch size and pixels per millimetre matched, the repeat following the tile (66.5 cm, tiling 2.0 and 1.8 from measured UV scales of 132.2 and 121.4 cm a unit, about 3 px a mm), Mafia's 7.1 cm and 3.6 px a mm a comparison only, its UV set unverified; the rib as "detail_rib" on the rib part (green 0.25), DetailRibOn, needing a "detail" map in the same row and using its tiling; the rib across each band, a turned tile with its normals turned, checked by lighting; judged in the packaged film. Why: the jumpers read as smooth rubber until 8 Nov; the method passed two rounds and his look (DECISIONS 8 Nov 13:10, 14:25).
2. **Material variants, a colour each** (one bullet): per-row tint from the casting sheets until the variants field exists; navy reads near black far off. Why: the route used today was unwritten.
3. **Step 9, the shipping project** (one bullet): C:/LedgerTools/mh-assemble is the only project that reaches the game, the rest by pointer to the asset-import skill's step 5; tools/garments_shipped_check.py must pass before a build is asked (its docstring, 8 Nov, records the one wasted night, dated there to the asset-import skill's review of 2 November; the memory note dates a wasted build 7 Nov). Why: step 9 named no project.
4. **Refit section** (four bullets): carry onto the game's built body (S6, not C5; body_full_layout.py restores the full layout); start from the game file (ron_jumper_game.blend; DECISIONS 7 Nov 19:18, memory note); clear_layers.py with the garment beneath named by --over, so that one is carried first, defaults --body-clear 8 mm and --over-clear 5 mm, the jumpers cleared 6 mm off the body and 8 mm off the jeans (DECISIONS 7 Nov 18:45); the head mesh to the chest, --head from the face DNA, a 1 mm grid from the side seen, unsigned distance first, pose pictures one grey (memory note head-mesh-reaches-the-chest), the third try with his yes (DECISIONS 7 Nov 21:28). The earlier "footwear, then trousers, then top" rule was dropped: no source states it.
5. **Refit section, the neckband** (one bullet, moved here from step 4, since it is a Blender fix on a skinned mesh after a carry): lower_neckband.py to 22 mm, 98 of 159 points, at most 11.1 mm; one try passed.
6. **Checkpoints, a dressed man** (one bullet): close plus 180, 225, 135 degrees (-MouthFilmDeg); one fresh reviewer per view as step 9 asks, or for a medium piece one per man covering all his views (RULINGS 3 Nov, reviewers sized to the piece); name a view that cannot judge; frame off flat untextured ground props (a meant flat dark cover was once called a placeholder, RECIPE 8 Nov).

Also: one example in "Requests this covers" and "a knit or weave surface and a colour per wearer" in the description; step 4's "the rib's ridges in the normal map" now points to step 8.

## Unverified and unreached

- Unverified: Mafia's 7.1 cm repeat and 3.6 px a mm (UV set unconfirmed in the sweater study); the 20 to 25 mm crew neckband depth (lower_neckband.py's docstring citing JUMPER-PLAN-2026-10-29.md, not re-read); the rib's 0.0 lighting difference (quoted from DECISIONS 8 Nov 12:34, not re-run). The night's packaged walk of the knit build was not read when this was written.
- Unreached: nothing.
