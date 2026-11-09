# Garment pattern library, first entries (9 November 2026)

For n09-6. Built only from LEDGER's own records; every source read 9 Nov 2026. Tags: **M** measured (time-log window), **I** inferred, **R** a RECIPE.md cost line, **not recorded**. No .zprj was opened; paths are as found on F:. Not run: `git log` (this helper had no shell), so commit history is unread.

Reference method: Mafia's, through the garment skill's refit section (.claude/skills/game-garment/SKILL.md lines 99-107): reuse a finished garment on another body before making a new one; carry close-fitting pieces point for point; re-drape anything loose from the same pattern graded to the new wearer.

## 1. Tom's zip jacket (first of its kind: a draped, baked, skinned top)

- **What:** zip-front blouson, navy, in the game since 30 Oct (garments.json, TomZipJacket).
- **Pattern:** FreeSewing's Brian (MIT) at Tom's measures, cut by tools/md-bridge/zip_jacket.py into 13 pieces, 29 seams: two fronts, whole back, two sleeves, rib hem band in three parts, rib cuffs, stand collar, two 12 mm zip tapes (SPEC.md lines 45-47). Chest 1,229 mm on his 1,069 (15% ease; JUMPER-PLAN line 7).
- **Body:** MH_TomL1 (F:/LedgerTools/bodies/MH_TomL1; avatar F:/LedgerTools/garments/tom/MH_TomL1.avt), chest 1069, waist 885, hips 1042, neck 420 mm (SPEC.md lines 41, 44).
- **Files:** drape 19, F:/LedgerTools/garments/tom/zip_jacket/v19/zip_jacket.zprj; maps in v28-built19/baked; shipped mesh v30-reskinned/skinned/zip_jacket_skinned.fbx (skin.json, bind.json beside it).
- **Skinned:** skin_garment.py --piece-attr none --collar-attr piece:10 --keep-correctives (garments.json).
- **Failed, fixed:** a cuff sewn inside out (cut mirrored, re-draped); draped rib cuffs never closed (straight-elbow drape, cuffs built in the bake); 29 Oct holes and a vanished right sleeve (piece 3 read as a button; UV order wrong; fixed by re-skin and two guards in skin_garment.py) (RECIPE.md 720-734; garments.json). The collar showing his throat: set aside after four tries on his word (DECISIONS lines 923, 1041).
- **Hours:** 6.78 M; at least 9.78 I with the bake chain; RECIPE lines about 7.7 R (unit-costs JSON lines 167-204).
- **Start for:** any zip or button-front top; its bake chain and skinning recipe, not its collar.

## 2. Tom's jumper (first knit top)

- **What:** plain crew-neck jumper; held, never drawn under the zipped jacket (garments.json, TomJumper).
- **Pattern:** Brian re-cut (j3) from a body with a neck: shoulder slope 26 degrees, ease 4%, crew neck 8.5 by 4 in (garments.json). Pieces: front, back, two sleeves, welt in two parts, two cuffs, neckband (JUMPER-PLAN line 8). Draft measures: F:/LedgerTools/garments/tom/jumper/pattern-j3/brian-jumper-j3.json (chest 1068.8, neck 420, wrist 197.1 mm).
- **Files:** F:/LedgerTools/garments/tom/jumper/drape-j3/jumper.zprj; chain-j3d (retopo, bake); shipped skin-try1/slots-neck/jumper_skinned.fbx. 19,480 triangles, maps 2048.
- **Skinned:** from his full body; neckband with no head weight; two slots (neckband shown, the rest hidden).
- **Failed, fixed:** draped bands left flat flaps, so bands were built from the shell's own edges (build_rib_band.py); the hidden sleeve end above the cuff set aside after two tries; a body without a neck put shoulder lines flat (RECIPE.md 229-239).
- **Hours:** 2.81 M/I, of which 1.0 R set aside (unit-costs JSON lines 231-253).
- **Start for:** every plain knit top (Ron's and Darren's came from it, below).

## 3. Tom's jeans (first trousers)

- **What:** straight-leg 1990 jeans, faded mid-blue, worn since 30 Oct (garments.json, TomJeans).
- **Pattern:** FreeSewing's Titan (Charlie set aside: its band sat about 205 mm under the waist). titan-jeans.json: seatEase 9%, kneeEase 20%, waistHeight 90%; seat 1,136 mm, knee 478, front rise 280, back 250, outseam 1,108, inseam 934, hem 419 mm (16.5 in), waistband 38 mm at 0.97 of the waist. Pieces: two fronts, two backs, waistband in two halves; fly, pockets, yoke, loops in the normal map (JEANS-PLAN lines 9-10, 26).
- **Files:** pattern F:/LedgerTools/garments/tom/jeans/pattern/titan-jeans.json; drape n7/drape/jeans.zprj; chain-n7 (retopo, bake, fade); shipped chain-n7/skinned/jeans_skinned.fbx. 9,728 triangles, maps 2048.
- **Skinned:** skin_garment.py --leg-sides --crotch-fade (each leg from its own leg, crotch faded to the pelvis over 7 cm); two-sided since 2 Nov after a hole behind the knee seated.
- **Failed, fixed:** a hem cut on a bare foot would not sit over boots, three tries set aside, then draped over a smoothed hull of the boots (RECIPE.md 206-215; garments.json).
- **Hours:** 1.61 M/I; set aside 1.2 R (unit-costs JSON lines 207-228).
- **Start for:** all plain trousers; work trousers by changing cloth and options.

## 4. Ron's boots (first footwear)

- **What:** black leather derby work boots, about 10,400 triangles the pair (F:/LedgerTools/garments/ron_boots/README.md).
- **Pattern:** none; modelled by tools/meshgen/blender/model_footwear.py --kind boot (its first version) on the foot of the body. Sole 20 mm below the bare floor; leather 2.7 mm off the skin (garments.json, TomBoots text).
- **Body:** MH_RoccoP2 full body.
- **Files:** F:/LedgerTools/garments/ron_boots/ron_boots.blend; maps/ron_boots_v2_maps.blend; shipped maps/ron_boots_skinned_v2.fbx.
- **Skinned:** foot, ball and calf only, no toe bones; never re-transferred.
- **Failed, fixed:** passed its first blind review, 30 Sep (ron-boots-review-1.md); leather maps added 30 Oct (garments.json).
- **Hours:** not recorded (made 30 Sep; the time log starts 5 Oct, SCOREBOARD "Unread").
- **Start for:** every boot and shoe (Tom's and Darren's came from it).

## 5. Tom's boots (repeat: footwear carried)

- Ron's pair carried point for point (carry_footwear.py), Ron's weights kept, leather 4.5 mm off; toe reshaped (v3) and sole thinned 17 to 12 mm (v4), raise 12 mm. Files: F:/LedgerTools/garments/tom/boots/ (carry.json, maps/boot-toe-record.json, boot-sole-record.json); shipped maps/tom_boots_skinned_v4.fbx.
- **Hours:** 2.95 M/I, of which 1.45 set aside (unit-costs JSON lines 256-277); toe 1.0 R and sole 1.0 R on 2 Nov (RECIPE.md 1654, 1670); whether those overlap the 2.95: unverified.

## 6-7. Ron's jumper and jeans (repeats: carried)

- Tom's jumper and jeans carried onto Ron (carry_garment.py, sigma 0.06), skinned from Ron's weights, Tom's maps (garments.json). Jumper drawn whole, one slot.
- **Files:** F:/LedgerTools/garments/ron/from_tom/ron_jeans/ (carry.json, skinned/ron_jeans_skinned.fbx); ron_jumper_clear/ (clear.json, skinned/ron_jumper_skinned.fbx); start a refit from ron_jumper_game.blend, not ron_jumper.blend (SKILL.md line 103).
- **Failed, fixed:** first refit drew his chest empty (wrong source file); hem on the jeans' waist, moved 6 mm off body, 8 mm off jeans (clear_layers.py); collar rim eased; skin at the neck ring's back cleared from behind, passed 8 Nov (DECISIONS lines 1149-1150, 1153, 1156, 1163). Released 8 Nov 16:30; his page passed both men (garments.json).
- **Hours:** not recorded per garment; see the table.

## 8-10. Darren's jumper, jeans and boots (repeats: carried)

- Same carry onto Darren; first onto C5, then again onto the game's S6 body rebuilt in the full layout (body_full_layout.py; S6 37 mm from C5, pelvis 64 mm). Boots: Ron's v2 carried, 4.5 mm off, raise 20 mm (garments.json; DECISIONS line 1147).
- **Files:** F:/LedgerTools/garments/darren/on_s6/darren_jeans/, darren_jumper_band/ (band.json, skinned/darren_jumper_skinned.fbx), darren_boots/ (carry.json, darren_boots_skinned.fbx).
- **Failed, fixed:** skin at chest and shins on C5 (carried again onto S6); breastbone slits from the head mesh, cleared 7 mm (clear_layers.py --head, his yes for a third try); neckband lowered to 22 mm (lower_neckband.py, try 1 of 2) (DECISIONS lines 1147-1152; garments.json). Final review passed 7 Nov (DECISIONS line 1155).
- **Hours:** Darren alone 1.96 M (SCOREBOARD line 17); not split by garment.

## Not pattern garments, listed for completeness

- **Sheila's handbag:** passed review 30 Sep, modelled, not patterned (accessories/README.md line 5). Hours not recorded.
- **Martha's trousers:** a recolour of her Mixamo body's painted texture (tools/art-recipes/person_recolour.py), passed try 1 of 2 (DECISIONS line 1132). No pattern, no mesh; nothing to start from. Hours not recorded.
- Held, not passed: Sheila's spectacles and chain, Darren's belt and pager, RonJacket/RonJacketB (garments.json).

## Hours per garment (for the scoreboard)

| Garment | Kind | Hours | Source |
|---|---|---|---|
| Tom's zip jacket | first of a kind | 6.78 M; at least 9.78 I; 7.7 R | unit-costs-2026-11-02.json lines 167-204, 281 |
| Tom's jumper | first knit | 2.81 M/I (1.0 R set aside) | same, lines 231-253 |
| Tom's jeans | first trousers | 1.61 M/I (1.2 R set aside) | same, lines 207-228 |
| Ron's boots | first footwear | not recorded | before the log (SCOREBOARD, Unread) |
| Tom's boots | repeat (carried) | 2.95 M/I (1.45 set aside); plus toe 1.0 R, sole 1.0 R | unit-costs JSON 256-277; RECIPE.md 1654, 1670 |
| Tom's whole outfit | first outfit | 14.15 M/I | unit-costs JSON line 285 |
| Ron's jumper, jeans | repeat (carried) | not recorded per garment | inside 5.81 M, below |
| Darren's jumper, jeans, boots | repeat (carried) | not recorded per garment; Darren alone 1.96 M | SCOREBOARD line 17 |
| Both men, six garments | repeat outfit | 5.81 M (windows also hold front wear, hair, office board) | RON-MEASURES lines 17-23 |
| Knit surface, both jumpers | finishing step | 0.35 M logged; about 2 R | RON-MEASURES lines 53-57; RECIPE.md 1931 |
| Layer and head clearing | refit fixes | about 1 R; under 1 plus about 1 diagnosis R; about 0.5 R | RECIPE.md 1893, 1899, 1902 |
| Handbag, Martha's trousers | other | not recorded | none found |

Reading (I): a carried repeat outfit cost 5.81 h against the first outfit's 14.15 h (ratio 0.41, SCOREBOARD line 16); per-garment repeat hours cannot be given, because the dress-the-cast windows name men, not garments. The scoreboard needs time-log windows named by garment from now on.

## Corrections after review (9 Nov, DRAFTS-REVIEW-2026-11-09.md: pass with fixes)
- The jumper's shipped file sits under its chain-j3d/ folder; the path above lacks it.
- The jacket's 13 pieces and 29 seams are cited to the wrong line of its spec; the count stands, its line to be found when the jacket is next used.
- The jeans' hem, rise and leg figures are unverified.
