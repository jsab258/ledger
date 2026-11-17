Method researched: game-garment SKILL.md (steps 6 to 9, "A refit", "Dressing a man"), tools/meshgen/blender/skin_garment.py and bind_garment.py, Kiln's MECHANICS.md, KILN-BODY-STANDARD-2026-11-16.md, Epic's FBX parametric-outfit page, Abdrashitov et al.'s published transfer code, studies/06-characters-wardrobe.md (all read 17 Nov 2026)

Game item: n16-1 (Kiln milestone M5). A method note only: nothing was built, run or committed. The choices it lists stay with the production session, except the one it records as decided (section 1).

# Kiln M5: from a Kiln drape to a rigged game garment on a LEDGER MetaHuman (17 November 2026)

Revised the same day after its fresh review (KILN-M5-RIGGING-METHOD-REVIEW-2026-11-17.md, verdict pass with fixes). Every fix is taken in; the list is at the end.

Every file named was read on 17 Nov 2026 unless another date is given. Tags: **U** unverified, **I** inferred, **G** guess (hours).

## Questions

1. Which body does each of the four breadth garments go on? Which file is draped on, and which file gives the weights?
2. What does a Kiln drape hand over today (format, pose, body)?
3. Which steps from drape to worn game garment already exist (the skill's chain, the scripts behind Tom's, Ron's and Darren's passed garments, Kiln's own skinning)? Which are missing?
4. How are weights moved from the body to the garment, and how is the result checked against the clothing floor (RULINGS, Clothes) and RUBRIC.md?
5. Which part of each garment simulates, if any (RULINGS 30 Sep: skinned meshes, only loose parts simulated)?
6. What test proves M5 on one garment (sitting and walking with no clipping)?
7. In what order should the work go, and how many hours will it take?

## Answers in short

- **Two bodies per wearer.** Kiln drapes on the wearer's standard body (16 Nov), whose forearms are straightened. The drape is bent back to the reference pose, and the weights come from the wearer's reference-pose body file, never from a standard body.
- **What Kiln hands over.** A static OBJ of garment and avatar, plus a .zprj and a plan file, posed with straight forearms. It carries no skin weights.
- **The route.** The bend-back step, then the skill's chain from step 6 onward: weld, game mesh, bake, clear the layers, skin, pose tests, import into mh-assemble, a held row, a packaged -WearHeld film. Kiln's own skinning is measured beside skin_garment.py on the first garment.
- **What simulates.** Jacket, trousers and nylon jacket: skinned only. The pleated skirt: Chaos cloth on a coarse proxy (Sheila's 11 Nov route).
- **The bars.** Kiln's parity bar (299 through, 44 inside, over 3 mm) is M5's tool bar. A sitting shape check runs beside the counts. The packaged film's RUBRIC lines 9 to 11 decide, where the floor is "nothing passes through".
- **First garment.** Ron's work trousers: they drape on Kiln main now. Their proof film stays held until his whole-person page, because they replace the jeans he passed.
- **Hours.** About 41 h counted step by step, which is the floor. The Hook list's estimates with the recorded 2 to 4x overrun give 34 to 69 h. The planning figure is **41 to 69 h**.

## 1. Bodies (question 1)

**Since 16 Nov 22:17, Kiln drapes only on the standard bodies.** Their folder is F:/LedgerTools/bodies/standard-2026-11-16/<who>/, holding <who>_standard_body.fbx, joints-mm.json and BUILD-NOTE.md. What makes a body standard: MetaHuman's reference pose, arms as they are, each forearm turned 36.65 degrees about its elbow onto the upper arm's line (as pose_body.py --keep-arms --straight-elbows does). The posed skin becomes the rest shape, and a head is joined where the file has none. Kiln's start check now refuses all four raw FBX files (KILN-BODY-STANDARD-2026-11-16.md; the review, fix 1).

**Weights never come from a standard body.** Its rest pose is rewritten, its joined head is weighted to "head" only, and Darren's neck ring was moved 5 to 18 mm, with 551 body points moved (KILN-BODY-STANDARD, the head join; the review, fix 2).

| Garment | Wearer | Drape body (Kiln) | Weights body (reference pose) | Notes |
|---|---|---|---|---|
| Donkey jacket | Ron | standard ron | MH_RoccoP2_FullBody.fbx | |
| Work trousers | Ron | standard ron | MH_RoccoP2_FullBody.fbx | Ron's boots' smoothed proxy gates the drape (section 7) |
| Pleated skirt | Sheila | standard sheila | MH_LenaS4_FullBody.fbx | |
| Nylon jacket | Darren | standard darren (S6 body plus SKM_MH_SamS6_FaceMesh, joined) | MH_SamS6_Body.fbx (headless) | see below |

**Darren, as his files are.**
- MH_SamS6_Body.fbx already has the full point layout: 32,334 points, 7,006 of them filled (its .json and the bodies README, per the review, fix 3). So body_full_layout.py has nothing to do, and no Unreal export is needed.
- What the body lacks is a head. His standard body has one, joined from his face mesh. For weights, the headless Body file serves: skin_garment.py moves every head and facial weight to neck_02 anyway. A reference-pose head join without straightening is the alternative.
- **Check to add before his garment:** his skeleton equals Tom's to 0.01 mm (heights 1,898 and 1,901 mm). Whether that skeleton fits Darren's own body was left unchecked (KILN-BODY-STANDARD, "Darren and Tom share one skeleton"). Compare his skeleton's joints with his skin: elbows, knees and shoulders at the limbs' bends, using the arm and neck finders Kiln already has (engines/drapestudio/src/rig.rs, find_arms and find_neck), and the head joint against the head's top. Read-only; 0.5 h G.

**Decided by the session (recorded here): each wearer's weights come from that wearer's full reference-pose body, after a check that its skeleton and weights match.** For Ron and Sheila that body is the _FullBody file. Mechanically, MH_RoccoP2_FullBody.fbx holds one combined LOD0 mesh with its head, and bind_garment.py binds from the largest mesh (the review, "What holds"). For Darren it is MH_SamS6_Body.fbx, as above.

The match check, run once per wearer before the first binding:
- the same bone names and rest transforms as the Body file, to 0.01 mm;
- the same weights on the body points the two files share, per point, to 0.001.

This replaces skin_garment.py's docstring default (the _Body file, on which Ron's passed jumper was bound: its skin.json, "body"). It follows the skill's step 2 (his order of 2 Nov).

## 2. What a Kiln drape hands over (question 2)

- The job scripts call Marvelous's own API names through Kiln's front end (F:/LedgerTools/tool-dev/kiln/python/run_job_script.py, Kiln's own, not under tools/). They end with ExportOBJ (garment and avatar) and ExportZPrj: donkey_jacket_job.py lines 55 to 61, pleated_skirt_job.py 67 to 73, nylon_jacket_job.py 57 to 63. Each job writes `<job>.plan.json` beside it. The output is static: no skeleton, no weights.
- The jobs' own AVT lines still name the raw FBX files. Kiln's start check replaces those with the standard bodies (KILN-BODY-STANDARD). So the drape has straight forearms and must be bent back (step a in section 3).
- import_md_drape.py needs the plan to rebuild the true-size "pattern" layer and weld the seams (its docstring). Whether Kiln's OBJ has Marvelous's layout (millimetres, Y up, one group per piece, UVs in fabric-tile units): U.
- **State on 17 Nov** (KILN-LANE-GATES-2026-11-17.md, KILN-LANES-VERDICT-2026-11-17.md; the review, fix 4):
  - The work trousers drape on Kiln main (gate: body through 0).
  - The donkey jacket is refused at its stand. Only the jackets lane makes it, and that lane fails its gate on other measures.
  - The nylon jacket is refused at its collar ring. The collar-plane fix is built; its gate has not run.
  - The pleated skirt falls (1,040 mm) on main until the skirt lane merges. It hangs in that lane.
  - The 16 Nov skirt OBJ was made before the standard. It is good for the format test only.
- So M5 can start on Ron's trousers now. The jacket and Darren's jacket wait on their lanes, and the skirt waits on the skirt lane's merge.

## 3. Steps that exist, and what is missing (question 3)

| # | Step | Existing tool (docstring read) | Proven on | Missing for Kiln output |
|---|---|---|---|---|
| a | Drape bent back to the reference pose | tools/md/unpose_garment.py DRAPE_BODY.fbx DRAPE_BODY.json GARMENT.obj OUT.obj: weights from the drape body, recorded joint turns undone in reverse | Tom's jacket and jeans | **Needed for every garment now.** It reads a DRAPE_BODY.json with "turns" (the elbow turn and axis per side, as tools/md/pose_body.py writes them, lines 71 to 172). The standard bodies carry only BUILD-NOTE.md and joints-mm.json. A turns record per standard body must be written from standard_body.py's own turns (36.65 degrees about each elbow, U the axis) and checked: the standard body bent back must land on the reference-pose body, within 1 mm |
| b | Weld, pieces, "pattern" layer, body and armature in one .blend | tools/meshgen/blender/import_md_drape.py OBJ PLAN.json OUT.blend | Tom's zip jacket, jeans, jumper | a format check on Kiln's OBJ (U); `--body` set to the wearer's weights body (its default is Tom's) |
| c | Detail, game mesh, UVs | retopo_pieces.py, uv_pack_low.py; skill steps 6 and 7 (jacket 18,000 to 22,000 triangles, trousers 8,000 to 10,000; 1.5 px/mm at 2048) | Tom's outfit | none |
| d | Bake, texture | zip_bake.py; the "detail" fields in garments.json | Tom's outfit, both men's knit | melton and nylon surface tiles (RON-KILN-OUTFIT-PLAN risk 7; BREADTH-PATTERNS section 4) |
| e | Layers cleared | clear_layers.py (--over; 8 mm body, 5 mm layer by default; --head from the face DNA) | Ron's and Darren's jumpers over jeans (7 Nov) | Ron's jumper must be re-cleared over the new trousers, and given a "Hidden" slot for its covered parts under the jacket, starting from ron_jumper_game.blend (RON-KILN-OUTFIT-PLAN step 11) |
| f | Skinning | skin_garment.py, which calls bind_garment.py (section 4) | every released garment | none |
| f' | Skinning, Kiln's way | Kiln's fit with the wearer as both source and target hands the garment back unchanged, with weights and walk, sit and arms-up tests (MECHANICS.md, round 2 item 1) | refits only | never run on a drape's game mesh (U); it lacks skin_garment.py's joint rules and has pose mending |
| g | Pose tests | pose_skinned.py --own-weights (down, up, walk, sit): it counts cloth inside the body over 3 mm and stretch, **not body through cloth** | the cardigan, Tom's garments | body through cloth per pose comes from Kiln's test poses (f') or from measure_fit.py through the judge's own call (named only) |
| h | Loose part as Chaos cloth | tools/ue/make_cloth_garment.py; LedgerGarments.h lines 322 to 330 (a row with "cloth": true goes to LedgerJacket::WearCloth) | SheilaSkirt row, held (480-triangle simulation mesh: garments.json line 195) | cloth has "never run packaged here" (SHEILA-SKIRT-CLOTH-ROUTE-2026-11-11.md section 4) |
| i | Import, levels of detail | tools/ue/import_garments.py in C:/LedgerTools/mh-assemble, four levels from the project's LOD groups | every worn garment | none |
| j | Held row, film, release | garments.json "hold"/"replaces"; -WearHeld; launch_line_check.py; garments_shipped_check.py | Ron and Darren, 7 and 8 Nov | none |

**Missing, in short.**
- A turns record per standard body, so the drape can be bent back.
- Kiln's OBJ checked against import_md_drape.py.
- The weights-body match check, and Darren's skeleton check.
- Ron's boots proxy.
- The jumper's re-clear and its hidden slot.
- A first measured run of Kiln's skinning on a game mesh.
- Melton and nylon surface tiles.
- Cloth seen working packaged.
- Passing drapes for the jacket, the nylon jacket and (on main) the skirt.

## 4. How weights are transferred and checked (question 4)

**The professional method.**
- **Epic's FBX outfit page.** The garment is imported as a static mesh ("importing a rigged or skinned FBX as a skeletal mesh is not recommended"). TransferSkinWeights then runs onto the render mesh from the body's combined skeletal mesh, by Closest Point on Surface. Tearing at armpits and upper thighs is mended with painted maps through SetSkinningSelection (Relax, Prune, Hammer, Clamp, Normalize). Levels of detail at 50, 30 and 10% (https://dev.epicgames.com/documentation/en-us/metahuman/building-a-metahuman-parametric-outfit-with-an-fbx-export, read 17 Nov 2026).
- **Epic's inpainting method.** Weights are copied only where the body is close and faces the same way; the rest is filled in from those points. Its published code uses a distance of 5% of the target's box diagonal, an angle of 30 degrees, and 10 smoothing steps at alpha 0.2 (https://raw.githubusercontent.com/rin-23/RobustSkinWeightsTransferCode/main/src/sphere_to_plane_transfer.py, read 17 Nov 2026; MIT per its repository page).
- **Unreal 5.8.** The TransferSkinWeights node's defaults are the same: 30 degrees, a 5% radius, 8 influences, 10 smoothing passes (RETOPOLOGY-AND-SKINNING-2026-09-30.md line 42).
- **CLO's Unreal guide.** Close pieces are skinned and only loose parts simulated; EveryWear caps at 8 joints a point (DEEP-DIVE-2026-11-01.md, M5).
- **Not taken:** the Chaos Outfit asset. Epic's pipeline transfers its weights again at every build (5.8.2 source, DEEP-DIVE line 23), so hand-fixed weights would be lost. Such garments ship as skeletal-mesh wardrobe items (skill step 9).

**LEDGER's copy of that method.**
- bind_garment.py:
  - copies the nearest body point's weights, interpolated across its triangle;
  - keeps a copy only where the body is within --reach 0.06 m and faces within --angle 50 degrees, and fills the rest in from reliable neighbours;
  - takes each panel's weights only from its own body part (sleeves from the arm; fronts and back from the trunk, with no arm bones);
  - keeps Epic's shoulder correctives in the trunk;
  - smooths lightly, then caps at 8 bones a point.
- skin_garment.py then applies:
  - the skirt rule (below the hips, the front takes the thighs' mean and the back goes to the pelvis, --skirt-pelvis 0.7);
  - for trousers, --no-skirt, --leg-sides and --crotch-fade with --centre-seam;
  - a collar free of arm, clavicle and head weights (--collar-attr);
  - each button moved as one piece, with parts over 6 cm kept and named in "notButtons";
  - head and facial weights moved to neck_02;
  - at most 8 influences, normalised, with the maps' UV layout put first.
- LEDGER's 50 degrees is wider than Epic's 30. Keep the proven settings, and change them only if a pose test fails at the armpit or crotch.

**Kiln's skinning (for the comparison, MECHANICS.md).**
- Weights come from body points within 1.5 R (R = the cloth point's distance to the body, at least 20 mm), full up to R. Each body point gives 4 bones; the cap is 8 a point, and weights under 0.01 are dropped.
- Weights are mended in the walk, sit and arms-up tests. A sleeve takes no trunk weights; trunk cloth may take thigh weights.

**Levels of detail and influences** (skill step 9, from Mafia's jacket): up to 8 influences at the top two levels and 4 below; levels at about 50, 25 and 10% (Mafia's median 47, 25, 9%: studies/06 line 82). import_garments.py makes the levels.

**Checks for every garment.**
1. **skin.json, before any film.** "notButtons" names only real buttons. Ron's passed jumper lists one 1,435-point, 0.578 m part, kept as the guard intends (I that this was harmless). "uvReordered" is recorded. --piece-attr matches the plan.
2. **Counts per pose** (rest, arms down, arms up, walking, sitting):
   - body through cloth over 3 mm, from Kiln's test poses or measure_fit.py through the judge's call;
   - cloth inside the body over 3 mm, from pose_skinned.py;
   - the worst edge stretch.
3. **The tool bar.** Kiln's parity bar, which MECHANICS.md records as the "Blender carry" bar: at most 299 body points through and 44 cloth points inside over 3 mm, in every test pose (MECHANICS.md, "Pass/fail" items 1, 2 and 8). It is the bar for M5's offline step only. **It is not the clothing floor.**
4. **The shape check beside the counts, sitting.** A count once fell from 328 to 10 while the hem still ballooned by eye (NOTEBOOK; the review, fix 6). So in the sit pose on the heavy body, measure two things beside the counts:
   - the gap from the seat and thighs to the cloth over them (median and 90th percentile);
   - the hem's height and its shape change against rest (Kiln's hem check, MECHANICS.md "Checks").
   Bars are taken from Tom's passed jeans in the same pose (U until measured).
5. **The floor, in the film.** RUBRIC lines 9 to 11 in motion: no tear, hole, spike or flying piece; **nothing passes through** (line 10); the shape holds. Judged in the packaged game's camera at talk distance (4.4 m) and street distance (3 to 28 m) against the clothing floor (RULINGS, Clothes, 3 Oct: no clipping or holes, nobody frozen stiff). These lines decide; the counts only screen.

## 5. What simulates, per garment (question 5)

The reference games:
- **Mafia.** Chaos cloth on only 10 meshes, five of them skirts (2 iterations), at the top two levels of detail. Coat tails and flaps swing on rigid-body bones. The plain vest-jacket does not simulate (studies/06 lines 40 to 51).
- **Kingdom Come II.** Only hems and skirts simulate, the tunic's skirt through a 270-triangle proxy (studies/06 lines 45, 53).

These numbers fit LEDGER's kind of game: a skinned third-person street game, one Chaos engine.

| Garment | Simulated part | Method |
|---|---|---|
| Donkey jacket | none: hip-length, boxy, no tails or vent | skinned, with the skirt rule below the hips. Both 30 Sep Ron jackets had skirts that "follow the thighs" sitting (garments.json RonJacket, RonJacketB). If sitting fails twice, a short Chaos cloth hem is a new method, under the rulings' tries rule (RULINGS 7 Nov) |
| Work trousers | none | skinned, with Tom's jeans options |
| Pleated skirt | the skirt below the yoke | Chaos cloth, coarse single-layer proxy, SKM_ kept as the weights' source (DECISIONS 2026-11-11 12:41). Sheila's mark has her standing; seated is left aside while it stands. Mafia's and Kingdom Come II's seated skirts: not found |
| Nylon jacket | none: elastic hem and cuffs | skinned, with the zip jacket's options (--piece-attr none, --collar-attr) |

## 6. The test that proves M5 on one garment (question 6)

M5 reads "outfits refitted and rigged to the cast, the heavy body sitting under its bar" (TOOLCHAIN-CORE-DESIGN-2026-11-13.md). For one garment:

1. **Drape.** The Kiln job passes the judge's checks on the wearer's standard body, with the held-back jobs run unchanged on the same build (KILN-EVALUATION; the design note, breadth by design).
2. **Rigged offline.** Bent back, then skinned on the wearer's reference-pose body (section 1). It meets section 4's checks 1 to 4 on MH_RoccoP2 (the heavy body): the tool bar in walk, sit and arms up, and the sitting shape check. Both skinnings (f and f') are measured, and the better one is kept.
3. **Rigged in the game.** Imported with garmentsShipped=PASS. Then a held row and a packaged -WearHeld film: Ron walking, and seated on his bench mark (mickeys-office.json line 64; U that the seat plays in a film run), front, side and back. One fresh reviewer passes RUBRIC lines 9 to 11 with the last good film (8 Nov's dressed-men-look) beside it. These lines decide.
4. **Not M5.** Release and the player's walk are M6. A -WearHeld run reads TEST and is never that pass (skill, "Dressing a man" 3).

**First garment: Ron's work trousers.** They drape on main now, they are the cheapest piece, they carry the jeans' proven options, and they test sitting on the heavy body.

**The trousers stay held until his page.** They replace the jeans he passed (casting sheet, production/casting/ron-kirby/SHEET.md line 13; DECISIONS 16 Nov 11:32, per the review, fix 8). So their proof film stays a held -WearHeld run, the row keeps its "hold" with "replaces": "RonJeans", and nothing is released before his whole-person page (RON-KILN-OUTFIT-PLAN section 3). M5's evidence is the held film; the release waits for his yes.

## 7. Order of work and hours (question 7)

**How the hours were reached.**
- **Recorded costs**, all floors, from a log that holds about half the hours (LOG.md, per the review, fix 7):
  - Tom's jeans 1.7 h; Tom's zip jacket 6.6 h;
  - the skirt's cloth route 0.5 h (NOTEBOOK);
  - the Blender refit chain 3.2 h a garment; both men's refits 5.8 h (TOOLCHAIN-CORE-DESIGN, cost table).
- **The Hook list's estimates** (BREADTH-PATTERNS, common facts): jacket 9.8 h, trousers 1.6, skirt 2.8, Darren's jacket 3.0, 17.2 h in all. Records ran 2 to 4 times those estimates, so **34 to 69 h**.
- **Counted step by step below:** about **41 h** (G). This is a floor: it assumes every step passes within its two tries and two review rounds.
- **Planning figure: 41 to 69 h.**

| # | Step | Hours (G) |
|---|---|---|
| 0 | Kiln's start-check fixes for the jacket and the nylon jacket, and the skirt lane's merge | in n16-1's Kiln rounds (3 to 5 at about 1 h, KILN-EVALUATION) |
| **Shared** | | **2.5** |
| 1 | Format test: import_md_drape.py on the 16 Nov skirt OBJ with its plan | 0.5 |
| 2 | Turns records for the four standard bodies, each checked by bending its standard body back onto its reference body | 0.5 |
| 3 | Weights-body match check (Ron, Sheila, Darren) | 0.5 |
| 4 | Darren's skeleton against his body | 0.5 |
| 5 | Kiln's skinning (f') set up as a job for a game mesh | 0.5 |
| **Work trousers (M5's proof)** | | **10.0** |
| 6 | Ron's boots proxy (make_boot_proxy.py), **a gate on the drape**; drape run twice | 1.0 |
| 7 | Bend back, weld, game mesh and UVs (8,000 to 10,000 triangles), bake on the jeans' route | 3.0 |
| 8 | Skin both ways, pose counts, sitting shape check, keep the better | 1.5 |
| 9 | Re-clear Ron's jumper over the trousers; held row ("replaces": "RonJeans"); import | 1.5 |
| 10 | Packaged -WearHeld film walking and seated; fresh reviewer, two rounds (RULINGS 3 Nov) | 3.0 |
| **Donkey jacket over the jumper** | | **13.0** |
| 11 | Bend back, sleeve check (sleeve_wrap.py --joints), weld, game mesh (18,000 to 22,000 triangles) | 3.5 |
| 12 | Bake (melton tile, yoke, buttons) | 2.0 |
| 13 | The jumper's hidden slot under the jacket and the jacket's clear over it, with head clearance | 1.5 |
| 14 | Skin both ways, pose counts, sitting shape check | 1.5 |
| 15 | Held row, import | 1.0 |
| 16 | Film and review, two rounds | 3.5 |
| **Nylon jacket on Darren** | | **8.0** |
| 17 | Bend back, weld, game mesh, two-colour bake, nylon tile | 3.5 |
| 18 | Skin (collar), clear over his jumper, row, import | 2.0 |
| 19 | Film and review, two rounds | 2.5 |
| **Pleated skirt** | | **8.0** |
| 20 | Bend back, weld, game mesh, bake | 2.5 |
| 21 | Skin (the SKM_ weight source), coarse proxy, make_cloth_garment.py, cloth row, import | 3.0 |
| 22 | Held packaged film standing and walking (cloth's first packaged run), two rounds | 2.5 |
| | **Floor total** | **41.5** |

- Steps 6 to 16 overlap n16-2's Ron plan (17 to 21 h, RON-KILN-OUTFIT-PLAN section 2). They are one piece of work and must not be counted in both items.
- At 41 to 69 h, this is well above both the evaluation's M5 estimate (3 to 5 Kiln rounds) and n16-1's 46 h, of which the Kiln rounds already take part. By CLAUDE.md, an item much bigger than it looked is told to him; the session decides that.

## Unverified, unreached, not read

- **U:**
  - whether Kiln's OBJ matches import_md_drape.py's layout;
  - the elbow-turn axes for the turns records;
  - the result of the weights-body match check;
  - whether Darren's shared skeleton fits his body;
  - whether Kiln's skinning meets step 9's rules on a game mesh;
  - the sitting shape bars until measured on Tom's jeans;
  - whether Ron's seat plays in a packaged film;
  - whether Chaos cloth cooks and runs packaged.
- **Unreached:** the full text of Abdrashitov et al.'s preprint. The PDF was fetched but its text could not be read here; only the abstract page and the published code were read.
- **Not opened, by brief or by choice:**
  - the judge folder (bars.json, measure_fit.py, drape_check_any.py) and anything held back;
  - Mafia's and Kingdom Come II's own garment files (Study 6 was used);
  - Kiln's fit.rs and standard_body.py sources (MECHANICS.md and KILN-BODY-STANDARD were used as their records);
  - KILN-CLOTHCRAFT-BRIEFS.md;
  - Marvelous's and CLO's help pages (cited through DEEP-DIVE-2026-11-01.md and PIPELINE-2026-10-28.md).

## Review fixes taken in (KILN-M5-RIGGING-METHOD-REVIEW-2026-11-17.md)

1. **Standard bodies with straightened forearms.** Bend-back for every garment, with the turns record it needs: sections 1, 3 a, 7 step 2.
2. **Weights never from a standard body:** section 1.
3. **Darren's S6 body as it is.** No Unreal export; the skeleton check added: section 1, step 4.
4. **Input state of 17 Nov:** section 2.
5. **Bars.** 299/44 named as Kiln's parity bar for the offline step; the floor "nothing passes through" decides in the film; body-through-cloth measured by Kiln's test poses or measure_fit.py: section 4.
6. **Sitting shape check** beside the counts: section 4, check 4.
7. **Hours.** Recorded costs and the 2 to 4x overrun used; bend-back, boots proxy, the jumper under the jacket and second review rounds added: section 7.
8. **The trousers' film held until his page;** the boots proxy a gate on the drape: sections 6 and 7.
9. **The session's decision recorded:** weights from each wearer's full reference-pose body after a skeleton-and-weights match check (section 1).
