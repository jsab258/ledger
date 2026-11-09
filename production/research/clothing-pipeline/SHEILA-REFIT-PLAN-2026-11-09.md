# Sheila out of the white layer by the refit route: the plan (9 November 2026)

Order of 9 Nov, item n09-6. A plan only; nothing built. Wearer: Sheila Dunn, code name "Lena", approved take MH_LenaS4 (face frozen). Casting sheet (production/art/clothing/sheila/README.md, 29 Sep): beige hand-knitted cardigan buttoned over a cream blouse with a small round collar, brown knee-length pleated skirt, flesh tights, flat brown lace-ups, handbag, spectacles. A bookkeeper of 53 at the cab office in 1990: plain high-street and home-knit, no brand mark, no modern cut. Her day is mostly indoors at her desk (Hook list, 3 Nov: 11 h out, 38 h in; CrimeProbe.cpp, her seat mark), so **sitting is her main pose**, unlike the men.

Sources read 9 Nov 2026: .claude/skills/game-garment/SKILL.md; garments.json; SHEILA-CLOTHES-2026-09-29.md; sheila/README.md, blouse-reviews.md, skirt-review-standing.md, cardigan-review-3.md; footwear/README.md; HOOK-GARMENT-LIST(-REVIEW)-2026-11-03.md; WHITE-LAYER-WALK-DIAGNOSIS-2026-11-09.md; TRIED-ARCHIVE.md; docstrings of the scripts named below; MAFIA-JACKET-2026-10-28.md and its review. F:\LedgerTools listed by folder and file name only.

## 1. What exists (reuse first)

| Piece | Exists? | Where | State |
|---|---|---|---|
| Handbag | yes | garments/sheila_handbag | worn in the game now |
| Spectacles, chain | yes | garments/sheila_spectacles | held: made on C1, sit 2-3 cm high on S4 |
| Skirt | yes, unskinned | garments/sheila_skirt (.blend, render_static.fbx) | passed standing review, 30 Sep; sitting set aside after 7 tries, 29 Sep; made on **MH_LenaC1** |
| Blouse | yes, unskinned | garments/sheila_blouse | passed on shape (review 2, 30 Sep); colour read grey-putty; on C1 |
| Cardigan | **no file** | none on F: | model_cardigan.py route failed 3 blind reviews, set aside 29 Sep |
| Shoes | **no file** | the "sh19" candidate folder no longer exists | set aside after 3 reviews |
| Tights | no | was planned as a skin material (retired CLOTHES.md) | |
| Knit tiles | yes | polyhaven/knitted_fleece/tiles (knit + our rib) | worn by Ron and Darren |
| Bodies | yes | bodies/MH_LenaC1, bodies/MH_LenaS4 (Body, FullBody, measurements) | which one the game builds: unverified |

garments.json has no skirt, blouse or tights row; CLOTHES.md line 12 calling the skirt and tights "kept in the game" is wrong (audits of 5 Oct and 3 Nov).

## 2. What differs from Ron's and Darren's route

- **Female body.** carry_garment.py and carry_footwear.py need the same point layout (men's bodies: 32,334 points). Whether her body shares the men's layout is **unverified**; it decides whether Tom's jumper or Ron's boots can carry onto her at all.
- **Height about 1.50 m** (SHEILA-CLOTHES, B). clear_layers.py's head limits (--head-below 1.56, --head-back-below 1.60) are men's heights and must be re-measured on her head.
- **Skirt.** The rule is skinned, with only hems, skirts and coat tails simulated. But the game's garment rows draw only skinned meshes: the only Chaos path is LedgerJacket::WearCloth (portrait runs), and make_cloth_garment.py writes into F:/LedgerTools/mh-dress, the project that does not ship. Mafia does not use cloth on a skirted coat: about 20 flap joints, 12 at the hem (MAFIA-JACKET-2026-10-28.md item 7; review F15, 28 Oct; the "rigid-body" part unverified). Kingdom Come II's skirt method: not looked up in this pass (unreached).
- **Layer order** is blouse, then skirt (blouse tucked under its band), then cardigan over both.

## 3. Steps

Times are estimates (E). The one measured refit is Ron's boots carried to Tom, 2.95 h (Hook review, 3 Nov).

**0. The body (1.0 h E).** Confirm the body the game builds for MH_LenaS4 (as Darren's S6 was not C5). Count points on MH_LenaS4_Body.fbx against C1 and against the men's 32,334. If it is an Optimized build, run tools/meshgen/blender/body_full_layout.py. Measure C1 to S4 per point (Darren's trap: 37 mm average, 64 at the pelvis). Read her head from the S4 face DNA (tools/meshgen/dna_mesh.py). *Check:* point counts, C1-S4 distance on record, head lower edge height. *Decides:* steps 2 to 4.

**1. Blouse (1.5 h E).** Start from sheila_blouse.blend. tools/meshgen/blender/carry_garment.py C1 to S4 (skip if step 0 finds them identical), then skin_garment.py from her own Body.fbx. Only the collar and the V show under the cardigan: draw them as Shown, the rest Hidden, as Tom's jumper slots do. Base colour near-white cream, judged in the game's light, not Blender's (blouse review 2). *Check:* body through cloth per pose; skin.json notButtons empty, uvReordered recorded.

**2. Skirt, skinned (2.5 h E).** Start from sheila_skirt.blend (render skirt, not the SkirtSim cone). Carry as in 1. clear_layers.py --over blouse at the band. skin_garment.py with its skirt correction (--skirt-from, --skirt-pelvis: thighs' weight passed to the pelvis toward the hem). *Check:* tools/meshgen/blender/garment_pose_check.py or pose_skinned.py at rest, walking, **seated at the desk**: points over 3 mm inside, the front hem. If the seated thighs pierce it, that is the known 29 Sep fault. Name it and choose a route (skinned with the desk hiding it, flap joints, or Chaos via code). Do not run cloth settings a third time.

**3. Cardigan (4.0 h E, the risk).** None exists, and the model_cardigan.py route is not repeated. If step 0 shows a shared layout, start from Tom's jumper game file (garments/tom/jumper/chain-j3d; FreeSewing Brian, built rib bands, the knit maps). Carry it to her body, then cut the centre front: a 29 mm button band (tools/meshgen/blender/build_rib_band.py), seven plain buttons, the welt at the top of the hip, 5 cm welt and 6 cm cuffs (README). Otherwise re-drape in Marvelous on MH_LenaS4_FullBody, Brian graded to her measures (waist 824, seat 964), per the skill's steps 2 to 4. clear_layers.py --over blouse, with --head and her own heights. tools/meshgen/blender/lower_neckband.py if the band stands tall. Knit: the shared tiles, tiling from her measured UV scale (cm per UV unit); a finer hand-knit stitch than the men's 2.5 times scale (unverified). Beige tint picked against the casting sheet. *Check:* the skill's step 9 checks; the head drawn from the front and the back on a 1 mm grid, unsigned distance first.

**4. Shoes (3.0 h E).** None exist. If the layout is shared, tools/meshgen/blender/carry_footwear.py Ron's v2 boots onto her feet, cut to a low flat derby, recoloured brown (footwear_maps.py already cuts a derby's seams). Then sole_footprints.py and raise_mm. Otherwise new, via the footwear script. *Check:* standing on the floor, no toe through, a reviewer at 4.4 m.

**5. Tights (0.3 h E).** Legs below a knee-length hem read close to skin. A flesh tint on her body's leg material is the old plan; whether LedgerGarments or the body material can take it is unknown. Optional for "out of the white layer".

**6. Spectacles (0.5 h E, optional).** Already planned for S4; the hold names the body.

**7. Rows, import, held film, release (2.5 h E).** Rows "who": "Lena" with hides (top, lower, shoes) and "hold". Run tools/ue/import_garments.py in **C:/LedgerTools/mh-assemble** only. tools/garments_shipped_check.py must say PASS. Film with -WearHeld close up and at 180, 225 and 135 degrees. One fresh reviewer per view, or one for her whole. Then his page (a whole-person look). Then "hold" becomes "released", pushed before the night build. *Check:* the log lists "LedgerGarments: Lena wears ..." for each piece and no "held back"; tools/launch_line_check.py says PLAYER; and the walked copy's build-commit.txt matches the requested head.

Total about 15 h E (12.5 without steps 4 to 6). The whole n09-6 item is 18 h, so this alone takes most of it: tell him if step 3 or 4 grows.

## 4. Known traps (from Ron's and Darren's fits, 7 to 9 Nov)

- Carry onto the body the game builds, not an older export (DECISIONS 7 Nov 17:40).
- Start from the garment's game file, not its first carry (19:18; ron_jumper_game.blend).
- A carry ignores the garment beneath: run clear_layers.py --over (18:45).
- The head mesh reaches the chest and is not in the body FBX. Pose pictures draw both grey and cannot show it (TRIED-ARCHIVE). A signed distance to the open head edge lied: 9.6 mm (8 Nov 00:30). Darren's head clearance was a third try, with his yes.
- A neckband standing tall after a carry: shorten it, do not re-drape (lower_neckband.py, 22 mm).
- Skinning without --piece-attr none tied a sleeve to one bone, and the wrong UV layer cut holes (Tom, 29-30 Oct).
- Import into mh-dress changes nothing (7 Nov). A held row shows the white layer in the player's game (8 Nov). The 9 Nov walk replayed the 8 Nov copy because the build stopped at F:'s floor (the diagnosis note). The caller reports Ron and Darren passed packaged on 9 Nov; confirm that walk's copy carried the release.
- Two tries per step, then research. The skirt's sitting and the cardigan are already past two: **a new route for either may need his yes**.

## 5. Open questions only the builder can answer

1. Does her body share the men's 32,334-point layout (Tom's jumper and Ron's boots carried onto her)?
2. Which body does the game build for MH_LenaS4: C1's, S4's own, or Optimized (full layout needed)?
3. Is the skirt allowed skinned-only for now, given that she sits behind a desk? Or does it need flap joints or a Chaos path in the garment code, which none of the code has today?
4. Is a new cardigan or skirt route a "third try" that needs his yes?
5. Can a tights tint reach her body's legs in the game, and do they matter at the counter?
6. Did the 9 Nov pass walk a copy with Ron's and Darren's release in it?
7. Is the Marvelous month's time free for a cardigan re-drape if the carry fails?

## Corrections after review (9 Nov, DRAFTS-REVIEW-2026-11-09.md: pass with fixes)
- Her seat of 964 mm is unsupported; her body files give hips 931 mm: use 931 until her game body is measured (step 1).
- Mafia's "12 at the hem" is loosely worded; read its source before it sets a number.
- Her age and height are uncited here; take them from her casting sheet.
- The step total without steps 4 to 6 is 11.5 h, not 12.5 h.
