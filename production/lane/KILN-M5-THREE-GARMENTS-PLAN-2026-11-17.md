Method researched: KILN-M5-RIGGING-METHOD-2026-11-17.md and its review, RON-KILN-OUTFIT-PLAN-2026-11-16.md, BREADTH-PATTERNS-2026-11-16.md, SHEILA-SKIRT-CLOTH-ROUTE-2026-11-11.md, studies/06-characters-wardrobe.md, the licence allowlist, and the web sources listed at the end (all read 17 Nov 2026). Reference: Mafia and Kingdom Come II (Study 6).

Game item: the next order's waiting item 13 (Kiln M5 for the donkey jacket, the pleated skirt and the nylon jacket). A paper plan: nothing was built, run or committed.

# Kiln M5 for three garments: a step plan (17 November 2026)

## In short

1. Ron's work trousers go first and prove the shared chain: bending the drape back, the weights from Ron's own body, the heavy body sitting, and the held film.
2. The donkey jacket and Darren's nylon jacket are worn as plain skinned clothes, with no cloth and no extra bones, as Mafia does with plain jackets.
3. Sheila's pleated skirt is the odd one: the waist part is skinned and the pleated part below swings as cloth, as Mafia's and Kingdom Come II's skirts do.
4. The outside check agrees with the method note on every point it could reach; two points (the coarse cloth stand-in driving the skirt, and the skirt-bone alternative) stay unconfirmed.
5. Honest hours for the three, after the trousers: about 29 h at best, 31 to 62 h to plan on (the method note's two to four times overrun on the risky steps, plus 2.5 h of shared steps), and none can start until each garment's drape passes.

## The check (second look at the method note's key claims)

1. Epic's own outfit route imports the garment as a plain mesh, copies weights from the body by "Closest Point on Surface", and mends armpit and upper-thigh tearing with painted fix maps (Relax, Prune, Hammer, Clamp, Normalize). Confirmed. The page gives no radius or angle numbers: those in the note come from the project's own files (Epic, parametric outfit with an FBX export).
2. Detail levels on that page: 50, 30 and 10%, four levels expected. Confirmed; the project's 50, 25 and 10% (Mafia's median) sits within it (same page; Study 6).
3. The two-stage "robust" weight copy (copy only where the body is close and alike, fill in the rest) is Epic researchers' published method, made for loose garments. Confirmed from the abstract; the numbers were not re-read (project page). Its code is MIT but MIT code is not on the allowlist for this use: porting it needs a licence pick. The project's own bind_garment.py already does the same thing, so nothing needs porting.
4. Epic's Chaos Outfit route re-copies the weights at every build, so hand-fixed weights are lost. Supported by a 12 Nov 2026 forum answer (UE 5.8), not from Epic staff. The note's choice to ship plain skinned meshes stands.
5. Bone limits: 4 or 8 bones a point by platform, at most 12 in unlimited mode, and a per-level "Bone Influence Limit". This supports 8 bones at the top two levels and 4 below (Epic, skeletal mesh rendering paths; the page is labelled 5.9, so 5.8 is assumed the same).
6. Cloth painting: a value of 0 means the point stays skinned and cannot move. This is how the skirt's waistband and yoke stay fixed while the pleats move (Epic, clothing tool; labelled 5.9).
7. The cloth asset takes a separate render mesh and simulation mesh, with weights from the body (Epic, panel cloth editor overview). Whether the fine render mesh can follow a coarse stand-in mesh (the "proxy deformer"): Epic's node pages did not load, but Epic's 5.3 Python reference documents the proxy deformer (found by the review): it exists; its 5.8 setup is unmeasured, and a forum question on wiring it has no answer, so the risk stays.
8. Marvelous's own guide to MetaHumans uses the same weight node and says UE 5.5 cannot use cloth assets; 5.6 and later can (Marvelous support article, no date shown).
9. Swinging coat tails: Unreal's Rigid Body node is for "secondary structures" and is cheaper than true cloth (Epic, Rigid Body node, 5.8). This matches Mafia's tails on rigid-body bones (Study 6). It is not needed here: none of the three has tails or a vent.
10. Skirts in games: no professional write-up with substance was reached (a 2019 tech-artists thread and a 2000 article only touch it). The evidence stays Study 6: Mafia's 5 skirts on cloth at 2 iterations, top two levels only; Kingdom Come II's skirt through a 270-triangle stand-in.

## What Ron's trousers prove first

The format check of Kiln's file, the turns record and bend-back, the weights-body match check on Ron, both skinning ways measured side by side, the counts and sitting shape check on the heavy body, the boots stand-in, the held row and the packaged held film. Each garment below reuses all of that and lists only what it adds.

## Plan 1: Ron's donkey jacket (over his jumper)

- **What moves how.** Skinned only. No extra bones (no tails, no vent; Mafia's plain jacket does not simulate). Below the hips the skirt rule shares the thighs' weights.
- **Weights.** From Ron's reference-pose full body, bind_garment.py with sleeves from the arms only and the fronts and back from the trunk. Fixes: armpit relax and the shoulder correctives kept; each button moved whole; the collar free of arm and head weights.
- **What it adds.** Set-in sleeves (the fault that set the Blender jacket aside on 29 Sep), a second layer (the jumper's covered parts into a hidden slot), the open neck, 18,000 to 22,000 triangles, melton.
- **The test.** Arms down, arms forward, arms raised to shoulder height and full height, crossed arms, walk, turn, seated on his bench. Failure looks like the armpit tearing or folding inward, side seams gathering, the jumper or skin seen through, the hem through the thighs seated, a gap at the neck. Screened by Kiln's tool bar (299 through, 44 inside) and the shape check; decided by the packaged film against RUBRIC lines 9 to 11.
- **Risks.** The armpit (two tries, then research); the hem sitting on a heavy body; navy over navy reading as one dark shape; the drape is refused at its stand today.
- **If sitting fails twice.** A short cloth hem, or two hem bones that follow the thighs at part strength: both new methods beyond the parent note, researched first, a third try only with his yes.
- **Hours (G).** 13 h floor (method note steps 11 to 16), 13 to 22 h to plan on.

## Plan 2: Darren's nylon jacket

- **What moves how.** Skinned only, with the zip jacket's options. No bones added. Elastic hem and cuffs hold the cloth to the body, so nothing needs to swing.
- **Weights.** From MH_SamS6_Body (headless; head weights go to the neck anyway), after the check that his shared skeleton fits his own body. Collar kept free of arm, clavicle and head weights.
- **What it adds.** A third body and its skeleton check; a looser blouson cut, so more cloth sits far from the body and the fill-in step does more of the work; the stand collar (set aside after four tries on Tom's jacket); rib cuffs (three tries before); a shiny surface that shows every stretch; two colours.
- **The test.** Head turned both ways and tilted (collar), arms raised and crossed, reaching forward, walk, sit. Failure looks like the collar cutting into or standing off the neck, the blouson hem through the belly or hips seated, cuffs stretching over the hands, shine sliding or streaking where the skin stretches.
- **Risks.** The collar; his skeleton not fitting his body; the drape is refused at its collar ring today.
- **Hours (G).** 8 h floor (steps 17 to 19), 8 to 14 h.

## Plan 3: Sheila's pleated skirt

- **What moves how.** Both. The waistband and hip yoke skinned and pinned (cloth value 0); the pleated panel below runs as Chaos cloth on a coarse single-layer stand-in of a few hundred triangles (Kingdom Come II: 270), at the top two detail levels only. The two lower levels show the skinned skirt with the skirt rule, as Mafia does.
- **Extra bones.** None. Skirt bones driven by the thighs are the usual cheaper alternative in games but no source for it was reached; keep it as the research direction if cloth fails twice.
- **Weights.** From her full reference-pose body; the skinned skirt stays the weights' source, the lower levels' mesh and the fallback.
- **What it adds.** Cloth's first packaged run here; the physics asset's thigh shapes as colliders; the pleats kept as modelled folds riding on the stand-in, not simulated one by one; the old skinned skirt's failure as the bar to beat (505 points inside seated, 1,321 walking).
- **The test.** Standing still for 30 seconds, walking, turning on the spot, a sudden stop, the game moving her (cloth reset), the camera crossing the level switch. Failure looks like legs through the skirt on the stride, jitter at rest, the skirt flying after a move, a pop at the level switch, pleats spreading flat or splitting, or the cloth missing in the packaged game.
- **Seated.** Left aside while her mark stands (route note, 11 Nov).
- **Risks.** Cloth never yet cooked into the packaged game here; the stand-in driving the fine mesh unconfirmed (if not, the render mesh itself is simulated, more costly); the skirt lane must merge before the drape stands on main.
- **Hours (G).** 8 h floor (steps 20 to 22; the cloth route note alone counted 7.5 h), 8 to 16 h.

## Totals

About 29 h floor and 31 to 62 h to plan on (review fix: the per-garment tops add to 52 h, the method's overrun rule and its 2.5 h of shared steps give 31 to 62), not counting the drapes (Kiln rounds) or the trousers. That is about 70% of the method note's 41 to 69 h for all four.

## Tools named and their licences

Kiln (allowlist 10), Marvelous drapes (allowlist 9), Unreal and its cloth and Rigid Body node (Unreal EULA, allowlist 3). Blender is the house chain already in use but is not named on the allowlist (it ships nothing). The robust-transfer code and any outside bone-sway plugin: needs a licence pick; none is recommended.

## Unverified points

- The coarse stand-in driving the skirt's fine mesh: exists (5.3 Python reference), 5.8 setup unmeasured.
- Whether cloth cooks and runs in the packaged game; Sheila's thigh colliders.
- The skirt-bone alternative's professional practice (no source reached).
- Docs labelled 5.9 assumed true of 5.8 (bone limits, cloth painting).
- Kiln's skinning on a game mesh; Darren's skeleton; the hem-bone fallback for the jacket.
- Hours are guesses (G).

## Sources (all read 17 Nov 2026)

- Epic, parametric outfit with an FBX export: https://dev.epicgames.com/documentation/metahuman/building-a-metahuman-parametric-outfit-with-an-fbx-export
- Abdrashitov et al., Robust Skin Weights Transfer (abstract): https://www.dgp.toronto.edu/~rinat/projects/RobustSkinWeightsTransfer ; code licence: https://github.com/rin-23/RobustSkinWeightsTransferCode
- Forum, parametric outfits and custom weights (UE 5.8): https://forums.unrealengine.com/t/metahuman-parametric-outfits-can-i-preserve-custom-skin-weights-from-maya/2849842
- Epic, skeletal mesh rendering paths: https://dev.epicgames.com/documentation/unreal-engine/skeletal-mesh-rendering-paths-in-unreal-engine
- Epic, clothing tool: https://dev.epicgames.com/documentation/unreal-engine/clothing-tool-in-unreal-engine
- Epic, panel cloth editor: https://dev.epicgames.com/documentation/unreal-engine/panel-cloth-editor-overview
- Marvelous, USD garments to MetaHuman: https://support.marvelousdesigner.com/hc/en-us/articles/52699135975705-Marvelous-Designer-to-MetaHuman-USD-Garment-Integration-Workflow
- Epic, Rigid Body node: https://dev.epicgames.com/documentation/unreal-engine/animation-blueprint-rigid-body-in-unreal-engine
- Tech-Artists.Org (2019): https://www.tech-artists.org/t/rigging-for-game-characters-baggy-clothing-need-advice/11557 ; Lander (2000): https://www.gamedeveloper.com/programming/devil-in-the-blue-faceted-dress-real-time-cloth-animation
- Unreached: Epic's proxy deformer, skinning blend and max distance node pages (empty when fetched).

## Review fixes taken in (REVIEW-KILN-M5-THREE-GARMENTS-2026-11-17.md, 17 Nov)

Hours range corrected to 31 to 62 h; the proxy deformer marked as existing, 5.8 setup unmeasured; the hem-bone fallback marked as new beyond the parent. Still open for the main session: whether the skirt reuses the 480-triangle stand-in already made; the nylon jacket and skirt tests use a screen first and the packaged film as the decider.
