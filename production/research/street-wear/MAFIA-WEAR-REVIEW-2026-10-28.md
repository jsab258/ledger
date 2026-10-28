# Review of WEAR-2026-10-28.md (fresh reviewer, 28 October 2026)

Read only. I re-measured everything from the kept files in WEAR/ (F:/LedgerTools/aaa-study/mafia/wear-2026-10-28), the 25 October exports (EXP/), Study 4 and Study 5's tables, the repository, and the engine on this PC. I extracted nothing new, did not open FModel and read no key file. A scan of WEAR/ for key-shaped strings (64 hex characters) found none. I wrote my scripts to scratchpad/mafia-wear/rv/, and the two BabelColor pages are saved in rv/dl/.

## What holds (reproduced exactly)

- **Masters and instance counts:** M_SMOpaque 318. Its tiling median is 1.5 where set (10), its roughness offset median +0.19 where set (8), and it has 6 detail-normal textures with the switch on in 3. Wall textures are 106/73/7 of 186.
- **The facade masters:** _Tint 35, plain two-layer 67 (rugged plaster second in 33 of 65), MaskBlend_VC 40+7 (blue in 22 of 40, (3.0, 2.6, 0.2, 2.1) in 9 of 40, wet flood 1 of 40, detail normals 3 of 40). Paint_Chipped is 48 and all eight of its medians match.
- **Meshes and placements:** 366 of 611 meshes and 88 of 96 slots carry vertex colour. The main street's 35 and 39 overrides are OverrideMaterials in BPP_PLA_Palermo_Buildings_01_MainStreet.
- **Decals:** 2,461 decals in 41 cells, 878 in the densest. Its actors are catacombs, a cistern, a crypt and the Opera sewers, so "underground" holds. Street kinds 1,147 = 754/335/58. Leak stains 285 (38%), plaster grunge 164, rust 47, stained 33, ground leaks 27, water lines 23, patches 20, puddles 145, ground leaks 78, edge wetness 13.
- **Decal sizes and placement:** all sizes and the 15 cm depth match. The 396 groups (median 2, p90 6, max 46) match, and so do 880 of 1,158 with a street level, the bands 37/23/17/22%, sort 2,228 and fade 0.044.
- **The decal half-size:** the doc tags it I, but the engine confirms it. DecalComponent.cpp:239 sets the default (128, 256, 256) and :474 uses it as the bounds' box extent, so it can be R.
- **Decal masters and examples:** all five are deferred, translucent, with wetness and snow functions. Four of the five have a normal, by params and by the connected-property mask. The three worked examples match.
- **Device profile:** [GlobalDefaults] PROJECT16/17/18 = 1/1/2 and decals 1. Shipped sizes are 1/2 and 1/4 of authored.
- **BP_TOD's components:** bloom, white clip, metering 70 to 80%, −3 to +1 EV100, local exposure 0.3/40%, motion blur 0.05; fog falloff 0.1, inscattering 0.15, volumetric 80 m; sun 1°, indirect 1.75. The colour head 1.1/0.9/0.0125 matches, and Palermo's 1.065/0.935/0.008125 equals 0.65 of it. No LUT.
- **Preset table:** every cell reproduces from mafia_tod_presets.csv (60/22/21).
- **Palermo's saved state:** fog 0.035/0.02, 50 m, bias 3.9, local exposure 0.5/0.62, vignette 0. The floor of 1.0 comes from the archetype's override.
- **Config:** extended range, candelas (LightUnits=1), lens flare and motion blur off.
- **Trim sheets:** 33 instances and 118 textures. The sheet sizes match, and the facade density is 758/379 (88 slots).
- **Opera:** decals 172/153 (I get 173/155 in 3D within 25 m), leak 64, fresco pattern 60, red patches 14, rug 5, centres 1.36/2.25/4.76 m, width 2.4 m. Fake glass matches. Mafia's chart blueprint is a ColorChecker plane, M_Grey18Debug and Epic's M_ChromeBall, and it is not placed.
- **ColorChecker:** I read https://babelcolor.com/index_htm_files/ColorChecker24_After_Nov2014.txt in full on 28 October 2026. All 24 L\*a\*b\* values in checker_srgb.py match the file. My own conversion (Bradford D50 to D65, IEC sRGB) gives the author's 8-bit and linear values exactly, 0 levels apart on all 24 patches. The file states M0 measurement. https://babelcolor.com/colorchecker-2.htm (read 28 October 2026) recommends X-Rite's post-2014 data for these charts.
- **Our side:** M_LedgerGrime writes BaseColor and Opacity only (make_grime_material.py:135-136). Its 177 decals are of ten kinds. The sizes hold: splash 6 to 8 by 0.6 m, wash 6.2 m tall, damp 1 m, streaks 0.8 to 0.9 by 0.9 to 1.1 m. The chandler has 8 decals (2 of each) and all its parts, including two doors and a gutter. The office record (10 to 20 decals, pale patches, head marks and damp kept, carpet set aside after two tries, masks made and left out) and white_temp_day 7,000 K in unreal-look.json match the doc.

## Faults that change the method (fix before it becomes a target)

**F1. The Opera room's grade is read from inactive values.** The doc: "a post-process volume (priority 1, blend radius 2 m) sets white balance 7,000 K, tint 0.1, shadow saturation 0.8, highlight saturation 1.2 and contrast 1.1, a slight warm gain (1, 0.98, 0.90)".
- **My measure:** in BBTD9M8I0S1FZIYMVDLECMZHD.json the volume's Settings carry only two override flags. Those are ColorGamma (1, 0.978, 0.976) and ColorGammaShadows (1, 0.936, 0.855). WhiteTemp, WhiteTint, ColorGain, both saturations and ColorContrastHighlights are stored without bOverride, so the engine ignores them. "Contrast 1.1" is highlight contrast in any case.
- **Same pattern elsewhere:** BP_TOD's "film grain 0.035" has no bOverride_FilmGrainIntensity. It is inactive unless BP_TOD's SetPostprocess (not decompiled) turns it on.
- **Correction:** the room's live grade is a warm gamma shift, stronger in the shadows. Mark the rest "stored, inactive" and film grain "unverified". O4 should try that gamma warmth, not saturation 0.8/1.2.
- **Rule for the method:** read the bOverride flags before quoting any post-process value.

**F2. Decal density and base share are measured on the wrong population.** The doc: "396 wall groups outside the tunnel cell, median 2 decals a wall, p90 6"; "bottom edge at or below 30 cm 37%"; step 2 "median 2 a wall… base grime… (Mafia: 37%)".
- **My measure:** these use all 1,158 wall decals outside the densest cell. That includes 252 PalermoTunnels-folder and 142 Opera-folder decals, which the doc's own "street kinds" exclude.
- **Street kinds only** (my groups.py, the author's grouping rule): 274 groups, median **1**, p90 6, max 46. 49% of all groups hold a single decal.
- **Bands on street kinds** (595 with a street level): at or below 30 cm **30%**, 30 cm to 1.5 m 18%, 1.5 to 4 m 21%, above 4 m 32%.
- **Box bottoms are not mark bottoms:** the bands measure the decal box's bottom edge. 249 of the 880 box bottoms lie more than 30 cm below the street proxy. Leak boxes are 5 m tall, and their p10 bottom is −1.8 m.
- **Mixed populations:** the by-kind medians (leak 0.9 m) reproduce only on street kinds. On all kinds the leak median is 0.18 m.
- **Correction:** step 2 becomes median 1 a wall (p90 6) on street walls, with about 30% of boxes reaching the base. Drop "base grime ← 37%": the boxes that reach the ground are mostly full-height leak stains.

**F3. Mafia's leak stains are drawn pictures, not a mask over grunge.** The doc: "The method: a shape mask… cuts a tiling grunge material that repeats 2 to 4 times inside it (R)". Its example is MI_StainWaterLeaky_05a.
- **05a:** placed once in 2,461 decals.
- **Leak stains:** of the 285 on street walls, 266 use their own stain picture. That is 04a ×168 (M_Decal_NoNormal, HeightToOpacity on, its default mask white) and 02a/02b/02d ×71 (M_Decal_Simple, no mask). Only 19 use a mask.
- **Tiling:** placement-weighted over mask-cut M_Decal_General decals outside the densest cell, 182 use the default 1, 27 use 1, 44 use 2 and 3 use 3.
- **Where masks are used:** plaster grunge (164) and puddles (145).
- **Correction:** describe two methods. (a) A drawn stain picture with height-to-opacity, for leaks and rust: the most placed, and what M_LedgerGrime already does. (b) A mask over the wall's own material or a roughness map, for plaster grunge and puddles, tiled mostly 1 to 2. Recipe step 1 should serve both.

**F4. The facade-blend values used for O1 are medians of a few instances.**
- **The doc:** "median 0.20/0.70… power 0.77" (O1 adopts them "as Mafia's height blend does"). **My measure:** these are set in only 7, 13 and 10 of 35 instances. The main street's MI_…_a and _b (74 placements) keep the master defaults 0, 1 and 1. **Correction:** say "where set (7, 13 and 10 of 35); the main street keeps the defaults".
- **The doc:** "on in 23 of 35". **My measure:** the master's World Position Noise defaults to True and no instance sets False. **Correction:** on in all 35, 23 of them set explicitly.
- **The doc:** "fine or coarse plaster tiled 2 over rough mortar tiled 1.5 to 5". **My measure:** _a is fine-plaster colour tiled 2 (the mortar normal at 0.3) over fine-plaster colour with the mortar's normal and HRO, tiled 1.5 at normal 1.2. _b is coarse plaster at the default tiling 1 (normal 1.0) over rough mortar tiled 5 (normal 2.0). **Correction:** state each instance as measured.
- **The doc:** "roughness offsets −0.30 to +0.26". **My measure:** that is Base Roughness Offset, set in 8 of 35. Layer 1's offset runs 0 to 1 (9 of 35). **Correction:** name the parameter and its count.

**F5. "One decal material that writes roughness" overlooks the one we have.**
- **The doc:** "177 projected decals… through M_LedgerGrime, which writes colour and opacity only".
- **My measure:** 37 of the 177 (puddles) go through M_LedgerWet (VignetteShot.cpp:8839-8840). Per make_wet_material.py:118-122 it already writes BaseColor, Roughness, Normal, Specular and Opacity.
- **Correction:** say so, and build step 1 from M_LedgerWet's wiring under the reuse-first rule, or record why not. This cuts its hours.

**F6. The calibration props are misdescribed, and C2 is undefined.**
- **The doc:** "chrome ball, grey ball, two clear-coat balls, a skin ball, and a colour-checker grid".
- **My measure:** the name table of SM_ColorCalibrator.uasset references five materials: M_ChromeBall, M_ClearCoat, M_ClearCoatBlack, M_ColorGrid and M_GreyBall. M_SkinBall (subsurface) is in the folder but on no mesh.
- **What holds:** "16-bit" is right. Color_checker is TSF_RGBA16F with SRGB serialised, and M_ColorGrid uses it. Color_checker_8bit is an 8-bit copy.
- **C2:** M_GreyBall is default-lit with clear coat, and its albedo is unknown (the doc says so). That leaves C2's "grey ball equal to neutral 5 within 5 levels" undefined.
- **Correction:** remove the skin ball, or put M_SkinBall on a sphere by script. In C2, measure neutral 5's displayed value. Compare the ball only after its base colour has been read in the editor.

**F7. The grey-balance citation points at a different patch.**
- **The doc:** "BabelColor recommends… the third neutral from the left for grey balance", while C2 and C3 use neutral 5.
- **The page:** it says "the third neutral patch from the left is often recommended". That is reported advice, not BabelColor's own, and the third from the left is **neutral 6.5** (C4: 161, 163, 163), not neutral 5 (D4: 121, 121, 121).
- **Correction:** keep neutral 5, the most neutral after conversion, and fix the attribution, or switch C3 to neutral 6.5.

**F8. The kept evidence does not show the trim numbers.**
- **The doc:** "70 material slots (30 distinct)", "39 of 95 window-folder slots", "median 1,177/589… p90 2,392/1,196, 52 slots".
- **The kept file:** meshes.json's own trimsheet kind gives 29 slots and 8 materials. Its density over 24 slots is a median of 1,171/586 and a p90 of 1,478/739.
- **How the doc's numbers reproduce:** 70/30 and 39/95 only when a slot counts as trim by its name *or* a trim texture anywhere in its instance chain. The 52-slot density reproduces only from the chain's trim texture and its Wood Tiling. No script in WEAR/scripts does either.
- **Correction:** keep the script that made the numbers, or regenerate meshes.json, and state the rule.

## Smaller faults (correct in place)

- **Study 5's range:** "−1 to +1.5 by day, +2.75 to +4 at night" contradicts the doc's own table. The 103 presets give day −1 to +6 (p10 to p90 −0.25 to +2.25) and night +1 to +4 (p10 to p90 +1.0 to +3.9).
- **Tonemapper:** "tonemapper quality 4" is set only under [PostProcessQuality@1] (DefaultScalability.ini:253). At High and Epic the engine default applies.
- **Exposure speed:** "darkening speed 3" is AutoExposureSpeedDown, adaptation into a darker scene (the image brightens).
- **Small signs:** 49, not 47 (22 smuggler, 17 Opera location, 8 branding, 2 numbers).
- **Town Hall:** the index has Floor 2 rooms A to **H**.
- **Tint mask:** "typically (0, 2, 5, 1)" is the most common value, in 7 of 57.
- **Atlas tiles:** "each has… an atlas tile": M_Decal_Simple has no TilesX/Y/TileID, so four of five.
- **Plaster grunge normal:** "1.5 to 2" is mostly 1.5, but instances range −2 to 5.
- **Decal sizes:** they are local Y by Z. Leak and rust boxes are rolled 90°, so "2.1 by 0.55" is 2.1 m tall by 0.55 m wide. The ground leak (roll −90°) is 2.5 m tall by 6.6 m wide. Write "tall by wide".
- **Densest cell:** "the underground tunnel" holds (catacombs, cistern, crypt, sewers). Add that 252 tunnel decals lie outside it.
- **New export:** "no textures" means no images. It does include 89 Texture2D property files.
- **Table counts:** "Day 08 to 17 h" holds presets from 10 to 17 h only. Several cells rest on small counts: film highlights 7 and 7, night volumetric 4, dawn fog opacity 6. Give n.
- **Opera lights:** no kept script reproduces them. Grouped by lamp Blueprint, I find 56 lamp-core lights, 49 without shadows (doc: 33 singles, 30 off). Several fill spots store no IntensityUnits, so "0.1 cd" is unverified.
- **The look file:** "lit only by the look file" is not accurate. unreal-look.json holds gains, exposure and white balance. The lamp pool and the room's lights come from the scene and office specs.
- **The shadow ruling:** "ours keep theirs inside by his ruling" is recorded as his yes in WEAR-2026-10-25.md ("Shadows raised only inside"), not in RULINGS.md. Cite it.
- **Texel budget:** our budget is 1,024 px/m inside rooms (4-BUDGETS.md:147), not 512. The comparison and S2 should say which applies.

## Checks and the estimate

**Steps without a numeric check:**
- **No check of their own:** recipe step 3, O3, S2 and S3. Suggested: S2 joinery texel density within ±20% of 512 px/m (1,024 inside), and O3's edge-wear share in the base-colour view.
- **C4:** records a ratio with no pass value.
- **C5:** qualitative.
- **C1:** the absolute 0.02 linear tolerance is about ±2 levels at white but ±60% at black. Use a relative tolerance or ΔE.

**17 hours is not plausible (I):**
- **O1:** needs vertex colour our pipeline does not carry. The room recipe strips colour attributes (shop-room.py:1553-1555), and no material in tools/ue reads vertex colour.
- **S2:** needs a wood trim sheet that does not exist (making or sourcing it, its licence line, a UV remap in the generator).
- **Done means packaged:** "done" means the packaged build walked by the AI tester, and the estimate leaves that out.
- **The record:** one office wear round took 45 minutes to an afternoon, and the light fix most of a day.
- **My estimate:** 25 to 35 hours. That is calibration 6 to 8, decal material 2 to 3 (reusing M_LedgerWet), office 8 to 12 and chandler 8 to 12.

## Verdict

**Pass with fixes:** F1 to F8 must be fixed before the method's targets (step 1, step 2, O1, O4, C2 and C3) are used. Re-measured: about 230 values, plus all 24 chart patches converted independently. Faults: 8 that change the method, 17 smaller.
