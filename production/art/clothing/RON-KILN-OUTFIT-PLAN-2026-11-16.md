# Ron's Kiln outfit: the plan for M6 and n16-2 (16 November 2026)

A plan only. Nothing here is decided, built, run or committed; the choices it lists stay with the production session. Written for the steer of advisor 172 (16 Nov): Kiln's M6 outfit is Ron's navy donkey jacket and dark wool work trousers from the breadth set, refit to his own body (MH_RoccoP2), so the first Kiln-made garments walked in the packaged game are the ones Ron's whole-person look (n16-2) needs, landing together on his page; every breadth garment that passes goes into garments.json for its wearer.

Method researched: the game-garment skill (.claude/skills/game-garment/SKILL.md, steps 1 to 9, "Dressing a man", "A refit"). Reference: Mafia's method (Study 6, production/research/aaa-reference/studies/06-characters-wardrobe.md, as cited by BREADTH-PATTERNS-2026-11-16.md): garments made to one base body, skinned, plain ones not simulated; jacket 18,000 to 22,000 triangles, trousers 8,000 to 10,000; levels of detail about 50, 25, 10%; up to 8 influences at the top two levels. Its numbers fit (a skinned third-person street game, the same skeleton family); Kingdom Come II not consulted for this plan.

All files below were read 16 Nov 2026. Tags: **U** unverified, **I** inferred, **G** guess.

## 1. What Ron wears now, and which rows change

From production/specs/garments.json (who "Rocco"):

| row | state now | what this plan does to it |
|---|---|---|
| RonBoots (lines 5-108) | worn, no hold (handed 30 Sep, maps 30 Oct) | unchanged; its smoothed proxy becomes the trousers' hem collider |
| RonJeans (574-608) | released 8 Nov 16:30 (Tom's jeans carried, his page passed) | replaced by the new trousers row; once his yes lands, held or removed (session's choice) |
| RonJumper (610-644) | released 8 Nov 16:30, shown whole, one slot | stays under the jacket (casting sheet); needs a re-clear over the new trousers and a covered-parts version under the jacket, as a new held row with "replaces": "RonJumper" |
| RonJacket (287-301) | held since 30 Sep, a method test | superseded; proposed: retired once the new jacket is released (session's choice) |
| RonJacketB (303-317) | held since 30 Sep, a method test | the same |
| new: the donkey jacket (name e.g. RonDonkeyJacket, G) | does not exist | new row, "hides": ["top"], "hold" until a packaged walk and his page |
| new: the work trousers (e.g. RonWorkTrousers, G) | does not exist | new row, "hides": ["lower"], "replaces": "RonJeans", "hold" the same |

The game supports this: a held row with "replaces" takes the named row's place in a -WearHeld test run, so the jeans and the trousers never draw over each other, and the player's game stays unchanged until release (ue-probe/Source/LedgerProbe/Public/LedgerGarments.h lines 277-303). Sections in a slot named "Hidden" are not drawn (same file, lines 390-404; Mafia's covered-parts method, used for Tom's jumper under his jacket).

**Casting conflict to carry to his page:** Ron's casting sheet (production/casting/ron-kirby/SHEET.md line 13) records "a navy donkey jacket with a black shoulder panel over a dark navy knitted jumper; jeans; scuffed black leather boots", the jeans "as Jafar passed them in the game, 8 Nov"; its first wording was "dark grey work trousers". The order n16-2 names trousers from the breadth set, and DECISIONS 16 Nov 07:09 records that they are not a recoloured variant of the jeans. The sheet's line changes only with his yes on the whole-person page (I). The trousers' colour (dark grey per the sheet's first wording, or dark navy/charcoal) is unsettled (U).

## 2. From the two patterns to both garments skinned on MH_RoccoP2 in the packaged game

Inputs already at home (read 16 Nov):
- Jacket draft: production/art/clothing/donkey-jacket-sewn/brian-ron.json (Brian, MIT, the corrected armpit; chest 1175, biceps 442, shoulderToShoulder 520, slope 5, waistToArmpit 251, ease as README.md); collar from Simon (donkey-jacket-pattern/simon-ron.json, drafted with the earlier wrong armpit; its neckline only matters, U whether it still matches).
- **Correction to BREADTH-PATTERNS section 2:** the trouser measures it calls missing are at home. production/art/clothing/donkey-jacket-sewn/ron-measurements.json (29 Sep, tools/meshgen/blender/body_measurements.py) holds seat 1184.6, seatBack 610.7, waistBack 487.7, waistToSeat 170, waistToUpperLeg 254, waistToKnee 598.7, waistToFloor 1142.1, inseam 888.1, crossSeam 748, crossSeamFront 390.9, knee 433.5, waist 1078.5. It was taken on MH_RoccoP2_Body.fbx, not the full body the skill requires (his order of 2 Nov), and whether that FBX has changed since 29 Sep is U.
- Job writers: tools/md-bridge/zip_jacket.py (Brian to named-edge pieces, sewn, draped, exported), tools/md-bridge/jeans.py (Titan, two fronts, two backs, band halves, arranged on Leg_Front/Back and Body_Waist points). Kiln runs such job scripts unchanged through F:/LedgerTools/tool-dev/kiln/python/run_job_script.py (its docstring; compat.py: an unreadable avatar file falls back to an FBX beside it, an unreadable fabric to a .drape-fabric.json beside it or a preset by name). Kiln has loaded Ron's body before (LOOP.md line 14: M1's baseline re-taken on MH_RoccoP2).
- Missing: Ron's straight-elbow drape body (only MH_TomL1_straight exists in F:/LedgerTools/bodies), Ron's Marvelous avatar (.avt; only Tom's exist), a smoothed proxy of Ron's boots (Tom's maker exists: F:/LedgerTools/garments/tom/jeans/n6/proxy/make_boot_proxy.py), a melton and a wool-trouser fabric file for either tool.

Steps (the order the skill gives; a refit reruns only what it changes). Hours are G.

| # | step | tool | acceptance check | hours |
|---|---|---|---|---|
| 1 | Re-measure Ron on MH_RoccoP2_FullBody.fbx and compare with ron-measurements.json; keep brian-ron.json if the upper-body girths agree within a few mm, else redraft (tools/meshgen/freesewing_draft.mjs, alter_brian.py --back-tuck 20 as before) | Blender headless (body_measurements.py) | the delta table written; pattern girths = body + ease (README's) | 0.5 |
| 2 | Draft Titan for the trousers at Ron's measures: work-trouser ease (seat about 10-12%, knee about 20%, waist at the natural waist, G), straight leg, hem wider than the jeans' 419 mm (about 460-480, G; no dated photograph found, BREADTH section 2), cuffless; crease and fly in the normal map | freesewing_draft.mjs | girths against body + ease; a fresh look at the outline beside a 1990 reference from production/research/plain-1990-clothes (U whether one exists) | 0.5 |
| 3 | Ron's straight-elbow drape body (tools/md/pose_body.py --keep-arms --straight-elbows) and a smoothed boots proxy (make_boot_proxy.py on ron_boots_skinned_v2.fbx, laces bridged, 3 mm out) | Blender headless | body whole to the crown; proxy over the boot everywhere, 3 mm | 0.7 |
| 4 | Write the jacket job: a new writer beside zip_jacket.py importing its helpers (as jeans.py does): whole back, two fronts with the 40 mm lap, two one-piece sleeves, Simon's collar fall and stand in a stiffer fabric, no rib, cuffs or zip tapes; yoke and patch pockets as ID areas or separate pieces (session's choice; the zip jacket put pockets in the map); melton about 0.7 kg/m2 as a fabric file (no Marvelous melton preset confirmed, U) | Python (job file) | the job's own selftest; seams paired by named ends; piece areas against the draft | 2.0 |
| 5 | Write the trousers job: jeans.py's route with the step 2 draft, a wool preset in place of V2_Woven_Denim_1, the new hem | Python | selftest; waistband 0.97 of waist | 0.5 |
| 6 | Kiln drapes, layered as worn: boots proxy, trousers, the jumper (as a smoothed proxy or as a layer, U which Kiln accepts for a ready skinned mesh), the jacket; on the straight-elbow body; 20 mm particles then 10 mm body, 6 mm collar and sleeve ends; each job run twice | Kiln (run_job_script.py) | skill step 3: no edge over 1.2x outside seams; body through cloth 0 beyond 1 mm; cloth inside 0 beyond the offset; sleeve_wrap.py --joints (90% cover); hem resting on the boot proxy; the jumper not seen through the jacket (0, as M4); a fresh reviewer against the references | 2 to 5 (M5's rounds, in n16-1) |
| 7 | Marvelous runs of the same two jobs, for the judge's bars and as the fallback drape (RULINGS 13 Nov: the game never waits on Kiln): import Ron's avatar first (jobs/import_body.py with BODY and AVT_OUT set; the skill's adoption rule for a DNA avatar: 100+ points, 2 mm or less at the neck) | Marvelous via the bridge | avatar points 100+; the same step 3 measures, twice each; exports kept for the month-end (26 Nov) | 1.5 |
| 8 | Bend the chosen drape back to the reference pose with Ron's own weights | tools/md/unpose_garment.py (or Kiln's refit, U whether its output meets step 9's rules) | points over 3 mm inside the body at rest: 0 | 0.5 |
| 9 | Detail, game mesh, UVs: weld, thickness last; retopology; jacket 18,000-22,000 triangles, trousers 8,000-10,000 (Mafia, Study 6); texel 1.5 px/mm at 2048, no overlap, 8 px padding | Blender (import_md_drape.py, retopo_pieces.py, uv_pack_low.py) | no non-manifold edge; openings as planned (jacket: neck, hem, two cuffs; trousers: waist, two hems); every open end closed by a lip and facing (skill step 4) | jacket 2.5, trousers 1.5 |
| 10 | Bake and surface: normal, AO, ID (wool, yoke black, buttons); pockets, stitching, crease and fly in the normal map; a wool detail tile (home first, then CC0; melton is nearly smooth, a felt or fine twill tile, U which); navy and the trousers' colour judged under the street's light | Blender (zip_bake.py), the garments.json "detail" fields | bake hits 97%+; ID areas within 1%; RUBRIC.md; navy jacket over navy jumper read apart at street distance (the skill warns dark navy reads near black) | 2.0 |
| 11 | Clear the layers: the jumper over the new trousers (clear_layers.py --over, 6 mm body, 8 mm trousers as on 7 Nov), the jacket over the jumper; the jumper's covered parts into a "Hidden" slot, starting from ron_jumper_game.blend (one slot), not ron_jumper.blend (memory note head-mesh-reaches-the-chest); head clearance near the neck checked from the face DNA (--head) | Blender (clear_layers.py, dna_mesh.py) | unsigned distances checked first; no skin seen at the open neck from the front or the back | 1.0 |
| 12 | Skin and levels of detail: Ron's own weights, at most 8 influences at LOD0-1 and 4 below, the elbow's blend from the body; cuff and collar edges kept to LOD2; LODs about 50/25/10% | Blender (skin_garment.py) | skin.json: notButtons empty except the real buttons, uvReordered recorded, --piece-attr as the BAKE-PLAN says; points over 3 mm inside per pose (rest, arms down, arms up, walking, sitting); worst edge stretch | 1.0 |
| 13 | Rows: the two new rows and the jumper's held row, each with "hold" and "replaces" as section 1; then import into C:/LedgerTools/mh-assemble (never F:/LedgerTools/mh-dress), Marvelous closed for the build and said so; commit before the editor session; one Unreal job at a time | Unreal (tools/ue/import_garments.py, LEDGER_MH_SCRIPT=import_garments) | garments_shipped_check.py says garmentsShipped=PASS; the game log names each piece "worn for this test run (-WearHeld)" and RonJeans "replaced for this test run" | 1.0 |

Garment-side total about 17 to 21 h (G), before reviews and films. The Hook list's estimates are 9.8 h (jacket) and 1.6 h (trousers), and its records ran 2 to 4 times their estimates (BREADTH-PATTERNS, common facts). n16-2 holds 10 h; Kiln's share (steps 4 to 8) belongs to n16-1's 46 h. The garment part alone is larger than n16-2's whole budget: by CLAUDE.md, an item much bigger than it looked is told to him (I that this applies).

## 3. What M6 needs beyond that, and one walk for both

- **M6** (LOOP.md line 13): one outfit walked in the packaged game. The evaluation estimates about 2 rounds plus one night walk (KILN-EVALUATION, cost of the next milestones).
- **n16-2's done line** (order line 16): Ron on his page with the cost table, batched with Tom's look; the item also needs the office exit, his routine and his talk.
- **The films** for his page and for M6's evidence: packaged -FaceAB -MouthFilm -PreparedAck runs, close and at 180, 225, 135 degrees (-MouthFilmDeg), talk (4.4 m) and street (3 to 28 m) distance, with -WearHeld naming the three held rows; one fresh reviewer per man covering his views (RULINGS 3 Nov, medium piece), the last good film (8 Nov's dressed-men-look) beside each. A -WearHeld run reads TEST in launch_line_check.py and is never the pass (skill, "Dressing a man", 3).
- **One walk for both (proposed, the session's to decide):** films under -WearHeld go on his page with Tom's look; on his yes the three rows' "hold" becomes "released" (date, reason, evidence) and is pushed before that night's build; that night's tester walk, with Ron on its route and passing his office exit and routine, is then both M6's walk and n16-2's last condition, as on 8 Nov (commit 0b2621d00), the row saying the walk is its remaining condition. Check: launch_line_check.py says PLAYER or PLAYER+WATCH; the log names "Rocco wears" each of the four pieces and no "held back" line. If the walk shows a fault the hold returns with that fault (skill, 5).
- The other order (release first, walk, then the page) would put an unseen look in the player's game; CLAUDE.md sends anything touching the look to him on one page before merging, so it is not proposed.
- Timing: M6 is due with M5 by Tuesday 24 Nov (order line 15); the walk waits on his answer, and the page is batched with Tom's look, so either can hold M6 past that date (I).

## 4. What blocks today, and what can be prepared first

**Blocked:** Marvelous's bridge does not start (UI Automation FindFirst timed out on 8 and 16 Nov, worked on 9 Nov; production/research/clothing-pipeline/BRIDGE-START-TIMEOUT-2026-11-16.md); his click is asked on his page. This blocks step 7 only: Ron's avatar, the Marvelous drapes, the judge's Marvelous bars for these two jobs, and the fallback drape the game would use if Kiln failed.

**Can be prepared now, no Marvelous and no clicks** (all headless or text):
- Step 1 (re-measure on the full body) and step 2 (the Titan draft).
- Step 3 (the straight-elbow body and the boots proxy).
- Steps 4 and 5 (both job files, with selftests), and the two fabric files.
- Step 6 on Kiln as dry runs: Kiln reads the FBX directly, so the drapes can be run and measured before the bridge works; judging against "at or better than Marvelous" waits for step 7's numbers (I; bars.json not read).
- The three draft rows (section 1), kept out of garments.json until their FBX exist (U whether a row without its file fails a check).
- The page's cost table frame and the film commands, without running them.

## 5. Risks

1. **The armpit under motion.** The Blender jacket failed on a set-in sleeve's armpit tearing with the arms raised and side seams gathering (donkey-jacket-sewn/review-3.md). A drape is judged in one pose; only the packaged arm-raised and sitting poses show it. Two tries per fault, then research, a third only with his yes.
2. **The game waiting on Kiln.** RULINGS 13 Nov: the game never waits on Kiln. If Kiln's drape fails its checks, Ron's look needs the Marvelous drape, which waits on the bridge. Both routes blocked at once is possible.
3. **Kiln's front end licence.** The design note (TOOLCHAIN-CORE-DESIGN-2026-11-13.md, front end) says the copied Drape Studio interface goes to him as one tap before any garment made through it is adopted, and nothing made through it enters the game before then. Whether that tap was answered: U (DECISIONS 10 Nov 13:41 records Drape Studio tested as his own tool, "no licence check, his written word"; whether that covers adoption is U). Check before step 13.
4. **Kiln's outputs beyond the drape.** Whether Kiln's refit and skinned FBX meet step 9's rules (influences, LODs, UV order) is U; the Blender chain is the known route.
5. **The heavy body sitting.** M5's own hard case; the jacket's skirt followed the thighs in both 30 Sep bindings (RonJacket, RonJacketB holds). The skill simulates only hems, skirts and coat tails; whether a donkey jacket's hem needs that is U.
6. **Layers.** Three tops-and-bottoms interactions (jumper over trousers, jacket over jumper, trousers over boots); a carry knows nothing of the layer beneath (skill, refit); the head mesh can show at the open neck.
7. **Fabric.** No melton or wool-trouser preset confirmed in either tool (BREADTH, U); a felt-like surface tile not yet found.
8. **Look.** Navy over navy may read as one dark mass at street distance; the casting sheet's change from jeans to trousers is his.
9. **Measures from the wrong body file.** ron-measurements.json was taken on the Body FBX, not the full body; the rejected first set sits in bodies/MH_RoccoP2/measurements.json (BREADTH section 1); a draft from the wrong file repeats the 29 Sep armpit fault.
10. **Budget and dates.** About 17 to 21 h of garment work (G) against n16-2's 10 h; M6 due 24 Nov; Marvelous renews 26 Nov, so its exports (skill, month-end) fall inside this work.
11. **Not read for this plan:** the judge's bars.json and held-back setup (not opened, as briefed), RUBRIC.md, the Hook sheet, the M4 layered job's files, Kiln's arrangement-point list for Ron's body (U whether Kiln names Leg_Front_R and Body_Waist points on him), FreeSewing Titan's option pages, the Needs-you page's current answers.
