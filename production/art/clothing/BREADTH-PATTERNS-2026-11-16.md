# Breadth set, practice garments: starting patterns (16 November 2026)

First pass for item n16-1. Reading only: nothing drafted, built or run. All web pages read 16 Nov 2026 unless marked. Tags: **I** inferred, **G** guess.

## Questions

1. Per garment: which MIT/CC0 pattern to start from, its licence at the source?
2. What measurements it needs; which the body's file lacks?
3. Pieces and seams; changes from the block to the period garment; dated photograph link?
4. What the md-bridge already does for a similar garment?
5. Risky parts and what Marvelous needs; hours (guess).

## Facts common to all four

- **Licence, read at source:** the FreeSewing repository is MIT, "Copyright (c) 2022 Joost De Cock" (https://raw.githubusercontent.com/freesewing/freesewing/develop/LICENSE). package.json of brian, titan, penelope reads `"license": "MIT"`, version 4.0.0 (https://raw.githubusercontent.com/freesewing/freesewing/develop/designs/brian/package.json, .../titan/..., .../penelope/...). Design docs read at freesewing.eu (freesewing.org answered 301 to it; that the .eu host is official is unverified).
- **Avatar gap (all four):** only Tom has an arrangement-point avatar (F:/LedgerTools/garments/tom/MH_TomL1.avt). The bridge's import job takes another body by setting BODY and AVT_OUT above its text (tools/md-bridge/jobs/import_body.py lines 5-6, 40). Full-body FBX exist for RoccoP2, SamC5, LenaS4. One avatar import each (about 0.3 h G).
- **Measurement files disagree:** F:/LedgerTools/bodies/MH_LenaS4/measurements.json holds the Lena C1 numbers (its "body" line names MH_LenaC1; chest 863.8). S4's real set, with seat and trouser measures, is F:/LedgerTools/garments/sheila/step0-2026-11-11/meas_S4.json. The C1 file in bodies/ (waistToHips 100, hips 930.6) differs from step0's meas_C1.json (160, 963.8): the older one is short of seat, waistToKnee, waistToFloor.
- **Reference method (Mafia, Study 6):** garments made to one base body, skinned, plain ones do not simulate; only skirts and flaps move (production/research/aaa-reference/studies/06-characters-wardrobe.md, read 16 Nov). Trouser target 8,000-10,000 triangles, jacket 18,000-22,000 (same file).
- **Hook list estimates** (HOOK-GARMENT-LIST-2026-11-03.md, read 16 Nov): jacket 9.8 h, trousers 1.6, skirt 2.8, Darren's jacket 3.0 (all E). Records run 2 to 4 times estimates (same file).

## 1. Ron's navy donkey jacket, MH_RoccoP2

- **Start:** FreeSewing Brian (MIT) plus Simon for collar only. Two drafts exist: donkey-jacket-pattern/brian-ron.json and simon-ron.json (first, wrong armpit), and donkey-jacket-sewn/brian-ron.json (the corrected one). Use the sewn one: chest 1175, biceps 442, hpsToBust 375, shoulderToShoulder 520 (round the back), slope 5, waistToArmpit 251, chestEase 20%, lengthBonus 55%, bicepsEase 12%, cuffEase 60%, armholeDepth 6%; back 92 cm from the shoulder's high point (donkey-jacket-sewn/README.md).
- **Gap:** RoccoP2/measurements.json holds the first, rejected values (shoulderToShoulder 446.1, slope 1.2, waistToArmpit 320.6, chest 1231.4) and lacks shoulderToElbow. The README's corrected set is not in any measurements file (I).
- **Why Blender failed:** a set-in sleeve's armpit tearing and gathering at the side seams as arms move, and a bagging back below the yoke; three blind reviews failed, set aside 29 Sep (donkey-jacket-sewn/review-3.md). The pattern itself was not faulted once the armpit was re-measured.
- **Pieces:** back on fold, two fronts, two one-piece sleeves, collar fall and stand (Simon), yoke (black, to armpit level), two patch pockets 190x200 mm, front lap 40 mm, four buttons (review-3's list of what was right).
- **Changes from the block:** dropped shoulder, boxy straight sides, no hem rib or cuffs, melton 0.7 kg/m2 (README), yoke and pockets as separate pieces or as normal-map detail (the zip jacket and jeans put pockets in the map).
- **md-bridge now:** zip_jacket.py already takes a Brian draft, cuts it into named-edge pieces, places them on arrangement points, sews with AddSeamlinePairGroup, drapes, exports (docstring). Reusable: fronts, back, one-piece sleeve, collar. Not needed: rib band, cuffs, zip tapes. Sleeve end checks exist (sleeve_wrap.py); a posed avatar can be loaded and the drape re-simulated (jobs/pose_back.py, lines 1-20).
- **Risks:** sleeve armpit under motion (the Blender failure; Marvelous drapes in a fixed pose, so the check is the packaged game's arm-raised pose, not the drape); a thick stiff cloth preset (no melton preset name confirmed; unverified); yoke seam bulk.
- **Photograph:** no dated free-archive photo found. Museum record, link only for the garment's look: National Coal Mining Museum donkey jacket, navy woollen, "Late 20th Century", image licence not stated: https://www.ncm.org.uk/collections/donkey-jacket/
- **Hours (G):** 6 to 10 h with the avatar import; Hook list E 9.8.

## 2. Ron's dark wool work trousers, MH_RoccoP2

- **Start:** the work is mostly done: Tom's jeans (Titan, MIT) were carried onto Ron already (garments/ron/from_tom/ron_jeans, pattern library entry 6-7, read 16 Nov). Cheapest route: a darker, plainer material on that carried mesh (a variant). A new draft is needed only if the cut must change.
- **If redrafted:** Titan needs cross seam, cross seam front, seat, seat back, waist, waist back, knee, waist to floor, waist to knee, waist to hips, waist to seat, waist to upper leg (https://freesewing.eu/docs/designs/titan). **RoccoP2's file has none of the trouser set** (it lists only the nine upper-body figures plus waist, hips). Tom's file has all of them; a body-measure run for Ron is needed (gap).
- **Pieces:** two fronts, two backs, waistband in two halves; fly, pockets and loops in the normal map (jeans.py docstring).
- **Changes from jeans:** plain wool, a pressed crease line, straighter hem (jeans.py HEM_ROUND 419 mm, Titan's own width is 478 mm at the knee), no fade (skin_garment's `--crotch-fade` is for weights, not colour), cuffless.
- **Bridge now:** jeans.py: Titan json in, tapers the leg to the hem, band at 0.97 of waist, arranged on Leg_Front/Back and Body_Waist points; fabric V2_Woven_Denim_1.zfab (only its physics).
- **Risks:** hem over boots (the jeans needed a draped hull of boots, three tries set aside, library entry 3); a wool preset in place of denim.
- **Photograph:** none found.
- **Hours (G):** 0.5 to 1 variant; 2 to 3.5 fresh drape; Hook list E 1.6.

## 3. Sheila's brown pleated skirt, knee length, MH_LenaS4

- **Correction to the Hook list:** a skirt already exists on S4. The old Blender skirt (16 knife pleats stitched flat to the hip 16 cm down, 62 cm long, 806 mm waist, 1231 hem; sheila/README.md) was carried from C1 to S4 on 11 Nov and skinned (garments/sheila/skirt-s4-2026-11-11/carry/carry.json, skinned/). Its pose test, sitting: 505 points over 3 mm inside the thighs, deepest 26.1 mm; walking 1,321 points, deepest 40.5 mm (pose/pose-test.json). Whether it passed review: unverified (garments.json not read). A Marvelous skirt is the alternative to that failure.
- **Start:** FreeSewing has no pleated skirt (docs list: Penelope pencil, Sandy circle, Sarah block, Sunny, Walburga). Penelope (MIT, read at source) for the yoke and hip fit: needs waist, seat, waist to hips, waist to seat, waist to knee (https://freesewing.eu/docs/designs/penelope); options include length bonus (% of waist-to-knee), waistband, vent, darts. Sarah block (waist to floor, length 25-100%, 15 options, https://freesewing.eu/docs/designs/sarah/options) but its source folder returned 404 on GitHub develop (designs/sarah): licence unverified, use Penelope.
- **Measurements:** all present in meas_S4.json (waist 813.9, seat 920.4, waistToHips 150, waistToSeat 150, waistToKnee 544). Not present in bodies/MH_LenaS4/measurements.json (wrong file, see above).
- **Pieces and seams:** hip yoke front and back from Penelope (darts or none, back seam), a pleated panel below (a straight rectangle, hem about 1.5 times the seat, G), waistband. Zip drawn closed.
- **Pleats in Marvelous:** the pleat tools are Pleats Fold (types knife, box, accordion; three internal lines per pleat for knife) and Pleats Sewing, which groups three internal lines per pleat; outer intersection points must be added by hand or the sewing fails without warning (https://www.versluis.com/2020/12/md-pleats/, a 2020 third-party tutorial on CLO 6 and MD 10; the current version's behaviour unverified). Whether the bridge's API reaches these tools: not found; grep of tools/md-bridge for "pleat" found nothing. An alternative that needs only internal lines: lines with a fold angle and strength per line (reported in a search summary of a Marvelous support reply, unverified).
- **Bridge now:** jeans.py and zip_jacket.py sew plain seams by named edges; no pleated or skirt job.
- **Risk, sitting:** the failure that set the Blender skirt aside is the thigh rise when seated; a pleated panel needs a seated avatar pose, which Marvelous can load (.pos, pose_back.py) but no seated pose file was found (unverified).
- **Photograph:** none dated found. Commons "Pleated skirts" category has no 1988-92 British file by name (https://commons.wikimedia.org/wiki/Category:Pleated_skirts, read 16 Nov).
- **Hours (G):** 5 to 9 h (avatar, yoke, pleats, seated test); Hook list E 2.8 (before the sitting failure was weighed).

## 4. Darren's purple and teal nylon jacket, MH_SamS6 (corrected by the session: his garments live on S6)

- **Start:** Tom's zip jacket re-cut (Brian, MIT; zip_jacket.py pieces: 13 pieces, 29 seams per the library, line unverified). Casting: "shiny purple and teal nylon shell-suit jacket" (production/casting/darren-milner/SHEET.md).
- **Measurements:** Sam has all Brian's required eleven (chest 1025.2, biceps 327.7, hpsToBust 271.3, hpsToWaistBack 439.2, neck 450.1, shoulderToShoulder 395.6, slope -6.2, waistToArmpit 308.3, shoulderToWrist 627.5, wrist 191.6) (https://freesewing.eu/docs/designs/brian). No gap for the draft.
- **Caution:** the library says Darren's garments were carried onto the game's S6 body (37 mm from C5; pelvis 64 mm). A C5 drape would be carried again (as the jumper was): add that step.
- **Changes:** looser blouson ease than Tom's 15% (G 20-25%), stand collar, elastic hem and cuffs (rib band and cuff pieces reused), thin shiny nylon preset (name unverified), two colours either as a yoke and sleeve panel cut as separate pieces or as an ID-mask map (Hook list: "two-colour maps").
- **Photograph:** none dated found. Museum link only: Hackney Museum women's nylon shell suit, 1993, bought 1993, multi-coloured, no image licence shown: https://museum-collection.hackney.gov.uk/object-1993-236
- **Risks:** the collar showed Tom's throat and was set aside after four tries (library entry 1); rib cuffs needed three tries; both carry over. Sam's wrist 191.6 differs from the cuff cut (WRIST_MM 197.1 is hard-coded in zip_jacket.py line 54).
- **Hours (G):** 3 to 5 h on top of Tom's chain; Hook list E 3.0.

## Not reached

- Marvelous Designer's own help pages on Pleats, Fold/Sew Pleats, Make Pleats (support.marvelousdesigner.com): HTTP 403 (not worked round).
- FreeSewing designs/sarah on GitHub: 404; its licence unconfirmed.
- Dated 1988-92 free-archive photographs of a donkey jacket, shell suit, pleated skirt: Commons category pages for donkey jackets and shell suits returned 404; none found.
- Not read: garments.json (review status of the S4 skirt), skin_garment.py, the cardigan/skirt review files, FreeSewing design-option pages for Titan.
