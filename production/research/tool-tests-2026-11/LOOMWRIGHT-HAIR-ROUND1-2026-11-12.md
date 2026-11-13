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
- Run 5 (13 Nov, 06:40, the next session): an empty level first (LevelEditorSubsystem.new_level, /Temp, never saved), B's own Hair hidden, the tool's groom in its own GroomActor attached to his face. Both held. Found two harness faults: the strands came in 100 times too big (25 m wide), because the groom importer already brings this file in at head size, so the times 100 went (scale 1, -1, 1); and every picture was black even at +3.5 EV, because spawned lights are stationary and a new level has no built lighting, so the lights became movable, with a sky light added. Neither is a try on the tool: both are the picture set-up.
- Run 6 (scale 1): the tool's hair sits right, 25 cm wide, its top 2.8 cm above his crown (face top 189.4 cm). The empty level was refused this time, and the pictures showed floor tiles and sky: unreal.Rotator's positional order is roll, pitch, yaw, so the camera had pointed straight down and straight up since run 4 (run 4's "walls" were the floor). Angles now by keyword, and the start level is kept. Lesson for every scripted capture: never build a Rotator positionally.
- Run 7 (13 Nov, 06:43; read 07:23 by the next session): cameras level, both views right. The tool's groom sits where his scalp is: its bounds x 48.3 to 73.0, y -12.9 to 13.4, z 166.4 to 192.2 cm (B at x 60), its scalp crown at 189.7 cm against his face top 189.4 (0.3 cm). But the hair lies flat on and under his skin: from behind his crown is bare scalp; from the front only dark smudges show at the brows, temples and sideburns; the hair rises only 2.8 cm above his crown, too little for a perm. The four exposures differ only in brightness (+3.5 EV clips). Its own report passes every number (curl diameter 41.7 px, curl turning 99.9 rad/m, detail by day 0.26) and leaves the reviewer check open: its checks do not see buried hair. Picture: production/previews/loomwright-round2-on-darren-2026-11-13.jpg (front left, behind right; in the behind view B is on the left).
- Round 2 verdict (hair), first written 07:30 and WRONG: it blamed the tool. Corrected after run 8 (below). Harness runs 7 (all picture set-up, none a try on the tool). Cost round 2 about 1.6 h, no helpers. Leftovers: F:/LedgerTools/tool-tests-2026-11/loomwright-r2 (ue to ue7 pictures about 40 MB), kept until his keep-or-drop.
- The tool's own output measured (13 Nov 08:20, advisor 127; tools/strand_skin_check.py on its USD curves against darren_head.obj, both in its frame): the tuned job's 22,626 curves sit a median 10.2 mm off his skin, 14% of points inside (roots on the skin, 93% within a hair's width under it), tips a median 15.4 mm out, each strand's highest point 26 mm out (p50), 35.5 (p95); the first perm job 20.2 mm, 4% inside. Its bounds (x 24.8, depth 26.2 cm) are the Unreal groom's to the millimetre. So the strands are not buried in the tool's file, and Unreal holds them where the tool put them.
- Run 8 (08:15): the strand width was the suspect (the import kept 0.01 cm, Unreal's default, not too thin); set to 0.007 cm: the picture is unchanged (crown bare from behind, smudges at the right temple and brows). Width ruled out.
- Corrected verdict: the bare head is a fault on our side of the Unreal picture (how the groom draws in the scene capture, or its orientation inside its bounds), not the tool's; the tool's hair is not judged yet. Harness runs 8. Next, when his Loomwright folder changes or the order allows (advisor 127): research how a groom without a binding renders in a scene capture and whether the Maya conversion flips it inside its own bounds (compare the groom's guide points with the USD's), before any further run.

## The bald look settled (advisor 133), 13 Nov 11:32 onward, harness runs 9 and 10
Method researched: Unreal 5.8.2's own source, read 13 Nov: HairStrandsMacroGroup.cpp 159 (strands are left out only of reflection captures, not scene captures); GroomComponent.cpp 1169-1184 (strands are drawn by the hair passes, not the main pass), 2179-2234 (a groom attached to a skeletal mesh reports the mesh's bounds, expanded, not its own) and 2825-2847 (binding and deformation paths when the parent is a skeletal mesh).
- Run 9: Epic's default strands material instead of his hair material (in case his material colours strands from data the tool's file lacks). Run 10: the groom detached from the face, kept where it was (world 60, 1.52, 16.89 cm, its points at head height), so it draws as a plain actor. Pictures: F:/LedgerTools/tool-tests-2026-11/loomwright-r2/ue9, ue10.
- Result: the pictures of runs 7, 8, 9 and 10 differ only by the run-to-run noise (behind B's head about 1,000 of 157,500 pixels change by more than 8 levels between any two runs, the same whichever setting changed). Width, material and attachment all change nothing: **the tool's strands are not drawn in our picture at all.** The dark patches at B's brows and right temple are B's own (they stay whatever the tool's hair does), not the tool's hair lying under the skin.
- Also corrected: the 'bounds match his scalp to the millimetre' of run 7 proved nothing, since an attached groom reports the face mesh's bounds (run 9 lists his own Hair, Eyebrows and Fuzz grooms all with exactly the face's box).
- **Verdict: the bald look is our picture set-up, not the tool.** The tool's hair is still unjudged in Unreal. Run 7's 'lies flat on and under his skin' is withdrawn.
- Tries on this fault (our picture): width 1, material 2, detach 3 (the one method found by research). None closed the gap, so it is set aside and listed. The likely remaining cause, unproven: strands that the editor's scene capture does not draw while his own hair shows (most likely through its cards); the next method is to read how Epic's MetaHuman hair picks strands or cards in a capture, then photograph the groom in the packaged game or through the editor's own view instead of a scene capture.
- The round itself: his Loomwright folder is unchanged since 12 Nov 13:06 (newest file at 11:25 today), so by advisor 127 the tool's next round has not started.

## Round 3, 13 November 2026 (14:05): his update of 10:42 (advisor 136, step 0)
- The update did not touch the hair: hair.rs is dated 12 Nov 10:01, and Darren's curls job came out byte-identical to round 1 (hair_strands.abc compared). Every hair fault above stands; nothing new to test. Correction: the 11:41 note that his folder was unchanged since 12 Nov 13:06 was wrong; his cloth code changed at 10:42 (see LOOMWRIGHT-CLOTH-ROUND1-2026-11-13.md, round 2).
