Method researched: production/research/tool-tests-2026-11/PLAN-2026-11-11.md (test 1, the groom route: strands through Epic's groom importer, a cards version for distance, judged against reference photographs) and RULINGS 3 Nov's hair bar; the tool's own MECHANICS.md (read 2026-11-12 23:40)

# Loomwright, hair, round 1 (12 Nov 2026, 23:40 to 00:10, the session alone, no helpers)

His own replacement for Houdini (C:\Game Dev Tools\Loomwright), advisor 119 and 120: hair first, its streets last. Work folder F:/LedgerTools/tool-tests-2026-11/loomwright-r1; nothing written into his folder; nothing enters the game.

## Verdict

**Level 2 (can the builder use it): passes, and already does what Houdini Apprentice cannot.** One job file, no click, 1.1 to 1.7 s a style, every output and number the same twice (its own verify: one fingerprint). Its Alembic strands import headless into Unreal 5.8 as a GroomAsset (1 group, 19,646 curves, 903,716 points); Houdini's free edition cannot write the Alembic at all (PLAN-2026-11-11).

**Level 1 (is it good at the job): not yet.** The strands read as curls at talk distance (its own check: curl 20.8 px across at 1.2 m in 1080p, detail 0.29 by day, 0.22 by night), but: the cards version, the one the game draws beyond talk distance, is almost bald (about nine in ten card points sit inside the head); the head is a crude built-in proxy, so nothing is judged on Darren's head; styles do not match their names (the "short back and sides" has a fringe to the eyes and long sides); a beard floats below the jaw. Against RULINGS 3 Nov's hair bar (crown from behind, talk close-up, sitting and walking, four distances without popping, five lights, no shimmer, no hard shadow, no pale scalp, frame cost, photographs): none of it can be judged in the tool's own pictures; all of it needs the groom on Darren in the game.

## The test

| Job | Result |
|---|---|
| Darren's curls (its example job: tight curls, 600 guides, 32 strands per cm2, 6 cm top) | runs; all eight automatic checks pass; one check left to a person (photographs) |
| Same result twice | yes, every file and number |
| Strands into Unreal (groom importer, headless) | GroomAsset, 19,646 curves, 903,716 points (Unreal adds one point per curve) |
| Cards into Unreal (FBX) | imported, two meshes |
| Cards into Blender 5.2 | refused: ASCII FBX is not supported |
| Perm, short back and sides | run, pass, 1.7 and 1.1 s |
| On Darren's own head | not run: no scalp mesh of his on disk yet (the job takes scalp_obj) |
| Beside his reference photographs | not run: the job's reference_photo is empty; the picture's reference panel is missing |

## Numbers

| Measure | Value | Its bar |
|---|---|---|
| Strands | 19,646 (614 cm2 scalp at 32 per cm2) | 120,000 or fewer |
| Strand memory (its estimate) | 27.0 MB | 40 MB |
| Card memory (its estimate) | 5.5 MB (200 cards, 3,200 triangles, 1024 atlas) | 8 MB |
| Curl across at talk distance | 20.8 px | 2.5 px or more |
| Curl turning measured in the strands | 203 rad/m (a perfect helix of the asked curl: 192) | 135 or more |
| Detail by day / night | 0.288 / 0.224 contrast | 0.08 or more |
| Card points inside the head | 3,216 of 3,600, about 89% (my measure: card points against an ellipsoid fitted to the head proxy's bounds; rough) | none should be |
| Time | 1.7 s a head | |

Builder time for the round: about 0.5 h, logged ("tool test: Loomwright hair round 1").

## What works

- No clicks: job files, exit code 0, 1 or 2; report.json with every check, number and output hash; a job log; day and night pictures, a cards close-up and a distance view.
- Same result twice, to the byte.
- Output Unreal reads: Alembic strands as a real GroomAsset; USD curves with the groom schema as well; cards as FBX.
- Real groom ideas inside (clumping by circle packing, guides, curl measured from the strands, frizz, strays), each number in MECHANICS.md with estimates marked.
- Budgets checked per head (strand count, strand and card memory) as part of every run.
- One job file also holds cloth, street and motion settings: the shared job format already exists across its modules.

## What fails, and why

1. **The cards are buried in the head.** About nine in ten card points sit inside the head proxy; the close-up shows a bald head with two patches. Its check "cards made for distance: 200 or more than 1" counts cards, not where they are or what they cover. Cause most likely: cards rooted on the scalp surface and laid along it without an offset or a lift along the hair's growth.
2. **No real head.** With scalp_obj empty it grows hair on its own proxy head (an egg with an ear at the front); nothing about Darren's hairline, crown or nape can be judged.
3. **No reference beside it.** The talk picture is meant as reference, day, night; without a photograph the reference panel is dropped silently and the "fresh reviewer agrees" check stays a person's job.
4. **Styles not like their names.** "Short back and sides" grows a fringe to the eyes and long sides; the period cut is short at the back and sides with length only on top.
5. **A beard that floats** below the jaw, in front of the neck, not on the chin.
6. **Blender cannot read its FBX** (ASCII FBX 7.4); Unreal can. Our garment and hair checks run in Blender.
7. **Its pictures are a stand-in renderer**: flat proxy, no shadowing from the hair on the head, no scalp; they cannot show shimmer, popping, pale scalp or hard shadows, which the bar lists.

## Improvements, most useful first

1. Place the cards outside the scalp: root each card at the surface, lift it along the growth direction by the hair's thickness, and add a coverage check (share of the scalp hidden from the camera views at 3, 10 and 25 m) instead of a card count.
2. Take a real head: read the character's head mesh (FBX or OBJ from the engine's export), its scalp from a painted mask, and fail the run when no scalp is given for a named person.
3. Require the reference photograph for a named person, and put it beside the day and night pictures; fail rather than drop the panel.
4. Period cuts by measurement: per-zone lengths (top, sides, back, nape, fringe) with a check that the result's measured lengths match the asked ones.
5. Facial hair rooted on a chin and jaw mask of the real head; a check that every facial strand starts on the skin.
6. Write binary FBX (or also OBJ) for the cards so Blender and other checkers can read them.
7. A picture of the groom on the real head from behind (the crown), side and at the four distances, so the bar's views come from the tool before the engine.

## Next (round 2)

1. Darren's head and scalp exported from his MetaHuman (an engine job, outside 01:15 to 04:30), his reference photographs, then the curls job on them, strands and cards.
2. The groom on Darren in the editor at talk distance and from behind, beside the current strands, before any packaged walk.
3. Loomwright's streets after the hair rounds (advisor 120).

## Files

F:/LedgerTools/tool-tests-2026-11/loomwright-r1/: hair_*.json (job copies with outputs here), out/darren_curls, out/perm, out/short_back_and_sides (strands, cards, pictures, report.json), run1.log, ue/ (the scratch Unreal check, groom_check.py, groom_result.json, run.log). The card measure was done by parsing the FBX text (Blender refused it).

## Round 2, 13 November 2026 (from 06:08): on Darren's own scalp
- His head exported from his MetaHuman (tools/ue/export_mesh_fbx.py, SKM_MH_SamS6_FaceMesh, LOD 0). His scalp cut in Blender headless (F:/LedgerTools/tool-tests-2026-11/loomwright-r2/darren_scalp.py): the skin faces inside the tool's own hair region, placed in its frame (metres, Y up, face +Z, his skull centre on the tool's at 0, 1.62 m, 0; a rotation, never a mirror). 4,620 faces, 754 cm² (the proxy's 614). The exported slot names are shifted (the skin carries the teeth's name), so the skin is taken by face count.
- Style from his casting sheet (a grown-out perm with bleached tips; light stubble), so the perm job, not the tool's tight curls. Two jobs (hair_darren_perm_r2*.json): both pass all eight automatic checks in 2 s; 31,626 strands. The second, tuned to his photograph (shorter 6 to 8 cm, looser, lighter), is closer in length and shape. Picture: production/previews/loomwright-round2-darren-2026-11-13.jpg (his photograph | day | night).
- Found: it cannot read a JPEG photograph (says so in its log, then drops the panel; a PNG works); no tip colour, so his bleached tips cannot be made; its pictures still draw its stand-in head, not the scalp it was given, so the fringe and the stubble (a floating beard) cannot be judged there; the cards are still mostly buried (round 1's fault, unchanged).
- Unreal: the strands import as a groom (31,626 curves, 714,780 points) only with the AlembicHairImporter plugin loaded for the run (-EnablePlugins=AlembicHairImporter; the project's own Alembic importer takes the file otherwise). tools/ue/groom_on_darren.py imports them with the Maya conversion times 100 and offset (0, 1.52, 16.89) cm, stands two of his MetaHumans side by side and photographs them. Its fourth run worked end to end but proved nothing: the MetaHuman blueprint kept its own hair on B (the swap did not hold), and the project's start level put walls in front of the camera. Next: a blank level, and the tool's groom on its own groom component attached to his face, his own hair hidden on B; then compare the hair top with his crown (face top 189.4 cm).
- Cost so far: about 0.8 h, no helpers. Time log: "tool test: Loomwright hair round 2".
