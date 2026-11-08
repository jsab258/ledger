# Street weathering: additions from phase 1 (8 November 2026)

The advisor asked for skills on "street wear and dirt" and "the night light". Reuse first: no new skill. The existing .claude/skills/street-weathering/SKILL.md and .claude/skills/shopfront/SKILL.md already hold most of it. This note lists what phase 1 proved that neither skill holds, and gives the text to add to street-weathering/SKILL.md in that skill's own style. All sources were read on 8 November 2026. Both skills were read whole. RECIPE.md and DECISIONS.md were searched, not read whole. Nothing here was run or measured again. "Unverified" marks what the records do not settle.

## Already covered (not repeated below)

- **street-weathering:** the chart and exposure (C1 to C5); real surface bands from the two values files and the band research method; wetting by Lekner and Dorf; wear in the material first (M_LedgerKit, brick streaks, chipped paint, room smoke and grade); M_LedgerStain, make_wear_masks, Mafia's decal counts, the black-only rule on ground that brightens, stain_check; the wet ground as stone plus a coat, and the coat cut at soles; the lamps scaled to albedo, no wider cones; pool_clip and measure_night_pools, C4 unmeasured; pictures and the gate.
- **shopfront:** a front's wear bake (front_wear.py); grime kept off a front that carries its own (homes_check); the window's night light by the 250-on-1% bar; settling 30 s after the clock jumps; Mickey's black glass (the bake waiting for 90 drawn frames); Mickey's near-black night front listed; the sash windows' fix (unverified); 9a to 9d trims, gilt and slate.

## Additions

**1. Header, the research list (line 8): one line added after "PALE-LINE-RESEARCH-2026-11-02.md (the coat at contacts);"**
Why: the skill cites two band files and no stain bake. SURFACE-BANDS has fed surface_values.py's BANDS since 2 November (its line 32, "reviewed PASS WITH FIXES"). The lamp bake passed its gate on 22 October.

> SURFACE-BANDS-2026-11-02.md (paint, gilt, joinery, slate, glazed tiles, kiosk red), LAMP-STAINING-BAKE-2026-10-22.md (stains baked from their sources on a kit piece); and RECIPE's entries of 4 and 5 November (the readable night, the pale sky, ground wear at street level).

**2. Always, the night bullet (line 17): replace the sentence from "NIGHT-GAPS-2026-10-29.md failed its review" to the end with:**
Why: the line is out of date. His corner note of 4 November replaced 29 October's stop on night fills (DECISIONS 4 Nov 23:07; unreal-look.json night_fill_note). As written, the skill would forbid the fill that is now in the game.

> His corner note of 4 November replaced 29 October's stop on night fills: the buildings stay readable under a faint warm fill, and the pools are kept (DECISIONS 4 Nov 23:07; the look file's night_fill_note; step 6). NIGHT-GAPS-2026-10-29.md's wider cones are still not used: they bring back the wash narrowed on 1 Oct and undo the 8 Oct clip fix. Its moon remains a trial switch only (-PlayNightMoon, VignetteShot.cpp). Its sections 1 to 3 stand with the review's corrections.

**3. Section 2, after the bullet "The bands as revised": one bullet**
Why: the skill names only two band files and has no rule for gloss paints. The LRV rule is tagged inferred in its source.

> - Paint, gilt, cream joinery, slate, glazed tiles and kiosk red have their bands in SURFACE-BANDS-2026-11-02.md, which surface_values.py's BANDS takes in. A gloss paint's maker LRV holds about 0.04 of specular, so base colour = LRV − 0.04, floor about 0.02, with Specular 0.5 supplying the rest (I: BS 8493 not reached; SURFACE-BANDS, Method). The kiosk red's hue and value are unverified (same, §6).

**4. Section 3, before the room bullet: one bullet**
Why: the skill has no method for a kit piece's named stains. Two world-aligned tries on the lamp column read as grain (gate-lamp-post-C GATE.md, 21 Oct). The bake passed all six views in round 2, judged in editor pictures. No packaged record of its own was found: unverified.

> - A kit piece with named stains (a lamp column's lime, rust and run-off): an even, world-aligned pattern on every face read as grey timber grain in two tries. So give the piece's faces their own unwrap, bake each texel's position and facing (Cycles), and draw seeded runs from each source in the piece's design rows: tools/art-recipes/kit_stain.py with production/specs/kit-wear/<piece>.json. Lay the result over the shared master by StainMap and StainStrength (default 0, so no other slot moves; make_kit_materials.py). Add broad run-off of 1 to 2.5 m, since design-sized stains do not read from the pavement. Draw each stain over the earlier ones, spread runs from one source, and keep his approved shade: the shaft went 4 to 5% lighter once the pattern was gone (LAMP-STAINING-BAKE; gate-lamp-post-C GATE.md, 22 Oct; RECIPE 22 Oct, the lamp).

**5. Section 3, the room bullet: one sentence added at its end**
Why: the skill does not record this trap.

> A projected mark prints onto whatever lies on its surface (papers, slips): project each mark's centre into the gate's logged camera before moving it. Moving marks around props proved fragile, and one stayed listed. The direction noted next, loose objects that take no surface decals, is untried (RECIPE 29 Oct, wear decals printing onto loose objects).

**6. Section 4, the "Pictures" bullet: two sentences added at its end**
Why: neither skill states the soft-edge rule or the grey multiplier. The multiplier made a tint meant as a colour print near black on 5 November.

> Every mark picture fades to nothing at all its edges, and a damp stain carries a strong tide line with a fainter middle, or it reads as a cut-out (RECIPE 26 Oct, a room's second wear pass; `python tools/make_wear_masks.py --selftest` checks both). On M_LedgerGrime a mark's tint is multiplied by the picture's grey, 64 of 255 (make_wear_masks.py STAIN_GREY), so write four times the colour meant (street_wear.py, its tints' note; RECIPE 5 Nov, ground wear).

**7. Section 4, the ground bullet (line 58): replace "check first before any ground stain." with:**
Why: on 5 November the street-level wear settled which material ground marks take, and found two traps. The coat cut by M_LedgerStain is still read from code, not tested.

> so ground marks take M_LedgerGrime, as the oil does, never M_LedgerStain (street_wear.py street_level_wear; the cut itself untested). A flat mark reaches 16 cm up whatever stands in its box (VignetteShot.cpp SpawnWear), so nothing rings a post or a bin (dark socks), and silt stops short of the kerb's face (streaks). Stains on the wet flags themselves failed both rounds on 5 Nov: broad ones read as leaf shadows, small ones as stamps, and every one as a grey shape under the coat. They are listed, and need the coat changed, not a decal (DECISIONS 5 Nov 07:58; RECIPE 5 Nov).

**8. Section 4, before the Check: one bullet**
Why: the corner's street-level wear (his point 5) is a proven method that the skill does not hold. Round 2 of 2 passed in the editor. The frame without the flag stains was seen by the builder only. The work was inside the packaged whole-frame views that passed on 6 Nov.

> - Wear at street level, by rule (street_wear.py street_level_wear, from the Hook sheet's foot of frame): dirt where the flags meet the wall, silt in the channel, dirt on the kerb top, a dark foot on the end gables. They are long flat bands, 5 m each, laid every 2.5 m so they overlap (at every 4 m the band read as dashes). Every mark is owned by one name, so -NoWearOn=street_level gives the picture without them. The corner's 33 m only, nothing multiplied before he has seen it (DECISIONS 5 Nov 07:58; 6 Nov 6:01). A narrow point is listed: the wall dirt takes some wet sheen at the wall's foot.

**9. Section 6, after the first bullet: four bullets**
Why: the night that passed on 5 and 6 November holds a fill, a lamp layout, a lamp tilt set aside, lit windows and a sky method. The skill holds none of them, and the shopfront skill holds only the shop window's light. Reference: Mafia's faint night sun and its key spot with a bulb light (Study 5; MAFIA-WEAR). Kingdom Come II: none found for the fill or the sky (DECISIONS 5 Nov 05:42).

> - The readable night (his note of 4 Nov): when the sky light cannot lift the gaps at any gain, use one soft directional fill by night only. It is warm, since the street's lamps light the cloud, less saturated than the lamps, and high (look file night_fill_*, read by VignetteShot.cpp). Measure the near-black share and the clipped share together. Then the hook view's near black fell from 66% to 45%, with the nearest pool's clipped red at 0.08% (DECISIONS 4 Nov 23:07). A saturated fill turned unlit brick pure red, and too much haze read as dusk (RECIPE 4 Nov). It passed four final packaged reviews with narrow points (DECISIONS 5 Nov 05:40). The record says the haze was tinted "rather than the sky picture" and lowered by a quarter. Its home was not found: fog_night_colour and fog_density_gain_night read the same as on 1 Oct: unverified.
> - A lamp is a key spot for the pool plus a small bulb light (RECIPE, universal values 4; the look file's lantern_bulb_radius_m note). Leaning the pool out over the road (lantern_pool_tilt_deg) cleared the column's own clipped stripe but darkened the fronts behind. Mickey's sill lies about 37 degrees off the lamp's axis, past the 46-degree cone at 11 degrees of lean. So the lean was set aside after two tries, left at 0, and the stripe is listed (gate-lamp-post-C GATE.md, 21 Oct).
> - Lit windows above the shops: each lit room or net glows as its own picture (EmissiveFromMap, make_base_material.py), with room_glow_gain_night against the target of reflected rectangles at 40 of 255 or more in cam_mickeys (the look file's note of 8 Oct). It was kept after two tries but did not pass alone, on three local faults (production/audits/night-2026-10-08/GATE-NIGHT.md). pool_clip's boxes stay on the flags: the double yellow lines (10 to 12%) and people's legs clip on their own (same).
> - The sky and far water (his note of 4 Nov, reverse view): first split the causes by switching the fog off in the shipped build, its show flag quoted. Lower the sky as seen (sky_seen_gain) and raise sky_light_gain by the same factor, so their product and the street hold. Flat water mirrors the sky at grazing angles: cut its own reflection with a specular under 0.25 (sea_specular). After any setting, measure that the thing it names moved: the first sea_specular sat in a branch the sea never enters (DECISIONS 5 Nov 05:42, 05:47, 05:55; RECIPE 5 Nov). It passed one small review in the editor. In the packaged views of 6 Nov the night sea is listed as a smooth brown band (DECISIONS 6 Nov 6:01).

About 30 lines added to the skill, one sentence replaced.

## Not added (open, unproven, or another skill's)

- Sodium's look on coloured surfaces (unlit brick pure red at night): SODIUM-IN-RGB-READING-2026-11-03.md lists methods with no recommendation, and most sources were unreached (the Jakob and Hanika PDF and Photrio returned 403; Smits 1999 not reached). It stays a listed shortfall.
- Mickey's near-black night front, black glass and edge chips (9c, flakes set aside 7 Nov): already in the shopfront skill.
- The puddles as decals, set aside on 8 Oct: the skill already says they wait on the corner's list.
- The pale line's packaged check and the pale patch on the far pavement: no later record was found (DECISIONS 2 Nov 09:31 is the last). The skill's own line stands.
