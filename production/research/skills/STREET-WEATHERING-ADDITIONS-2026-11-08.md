**Merged 8 Nov** into .claude/skills/street-weathering/SKILL.md, with all seven fixes from STREET-WEATHERING-ADDITIONS-REVIEW-2026-11-08.md (PASS WITH FIXES). The skill's text is the version that counts; the additions below are as corrected.

# Street weathering: additions from phase 1 (8 November 2026)

The advisor asked for skills on "street wear and dirt" and "the night light". Reuse first: no new skill. The existing .claude/skills/street-weathering/SKILL.md and .claude/skills/shopfront/SKILL.md already hold most of it. This note lists what phase 1 proved that neither skill holds. All sources were read on 8 November 2026. Both skills were read whole; RECIPE.md and DECISIONS.md were searched, not read whole. Nothing was run or measured again. "Unverified" marks what the records do not settle.

## Already covered (not repeated)

- **street-weathering:** the chart and exposure (C1 to C5); real surface bands and the band research method; wetting by Lekner and Dorf; wear in the material first (M_LedgerKit, brick streaks, chipped paint, room smoke and grade); M_LedgerStain, make_wear_masks, Mafia's decal counts, the black-only rule on ground that brightens, stain_check; the wet ground as stone plus a coat, and the coat cut at soles; lamps scaled to albedo, no wider cones; pool_clip and measure_night_pools, C4 unmeasured; pictures and the gate.
- **shopfront:** a front's wear bake (front_wear.py); grime kept off a front that carries its own (homes_check); the window's night light by the 250-on-1% bar; settling 30 s after the clock jumps; Mickey's black glass (the bake waiting for 90 drawn frames); Mickey's near-black night front listed; the sash windows' fix (unverified); trims 9a to 9d, gilt and slate.

## Additions, where each went in the skill

1. **Header, the research list:** SURFACE-BANDS-2026-11-02.md, LAMP-STAINING-BAKE-2026-10-22.md, and RECIPE's entries of 4 and 5 November. "Values live in their homes" now says three values files and names night_fill_*.
   Why: SURFACE-BANDS has fed surface_values.py's BANDS since 2 Nov (its line 32); the lamp bake passed on 22 Oct.
2. **Always, the night bullet:** the text from "How dark the gaps are is his ruling" to the end is replaced. His corner note of 4 Nov (DECISIONS 4 Nov 18:21, point 3; 23:07) replaced 29 Oct's stop on night fills, and the bullet points to section 6. NIGHT-GAPS' wider cones stay unused. Lifted blacks and the night sky gain stay unused unless he asks (DECISIONS 29 Oct 06:02). The moon remains a trial switch only (-PlayNightMoon). *Fixes 1 and 2.*
3. **Section 2, a new bullet after "The bands as revised":** SURFACE-BANDS covers paint, gilt, cream joinery, slate and glazed tiles. For gloss paint, base colour = LRV − 0.04, floor about 0.02 (I; BS 8493 not reached). Its kiosk-red band is a K6's and does not apply to the street's grey KX100. *Fix 3.*
4. **Section 3, a new bullet before the room bullet:** a kit piece's named stains, baked from their sources on its own unwrap (kit_stain.py, StainMap and StainStrength default 0, run-off of 1 to 2.5 m). The 21 Oct world-aligned tries read as grain. It passed six views in editor pictures on 22 Oct; no packaged record of its own was found: unverified.
5. **Section 4, after the placement bullet:** a projected mark prints onto loose objects, so project its centre into the logged camera before moving it. Loose objects that take no decals: untried (RECIPE 29 Oct). *Fix 7: moved here from section 3.*
6. **Section 4, the pictures bullet:** marks fade to nothing at every edge, and damp stains carry a tide line (`make_wear_masks.py --selftest`; RECIPE 26 Oct). On M_LedgerGrime the tint is multiplied by the picture's grey, 64 of 255, so write four times the colour meant (STAIN_GREY; street_wear.py).
7. **Section 4, the ground bullet:** "check first" is replaced by the rule that ground marks take M_LedgerGrime, never M_LedgerStain; the coat cut itself is still untested. Two more points are added: the 16 cm climb (VignetteShot.cpp SpawnWear), and stains on the wet flags, which failed both rounds and are listed (DECISIONS 5 Nov 07:58).
8. **Section 4, a new bullet before the Check:** wear at street level by rule (street_level_wear): 5 m bands every 2.5 m; one owner, so -NoWearOn=street_level shows the street without them; the corner's 33 m only. Round 2 of 2 passed in the editor. The frame without the stains was seen by the builder only. It was inside the packaged views that passed on 6 Nov.
9. **Section 5, a new bullet before the Check:** the sky and far water, by day. Split the causes with the fog off; keep the product of sky_seen_gain and sky_light_gain; set sea_specular under 0.25; measure that the setting moved its thing. Reference: none found, for the sky (DECISIONS 5 Nov 05:42). *Fix 6: moved out of the night section and labelled "by day".*
10. **Section 6, three new bullets and the Check:**
    - **The readable night:** one soft, warm, desaturated high fill. 66% to 45% near black was measured in round 1 (DECISIONS 4 Nov 23:07). After try 2 the unlit brick was still near pure red, listed (DECISIONS 5 Nov 05:40). The haze's home was not found: unverified. Reference: Mafia's faint night sun (Study 5, as cited in VignetteShot.cpp's moon note); Kingdom Come II for the fill: unverified. *Fixes 4 and 5.*
    - **Lamps:** a key spot plus a bulb light. The pool lean was set aside after two tries (gate-lamp-post-C GATE.md, 21 Oct).
    - **Lit windows:** each glows as its own picture, with room_glow_gain_night; kept, not passed alone (GATE-NIGHT.md, 8 Oct).
    - **The Check:** pool_clip's boxes stay on the flags, clear of the yellow lines and legs. The 4 Nov shares are luma under 10, never compared with measure_night_pools.

The skill went from 86 to 99 lines.

## Not added (open, unproven, or another skill's)

- Sodium on coloured surfaces (unlit brick near pure red): SODIUM-IN-RGB-READING-2026-11-03.md makes no recommendation, and most of its sources were unreached (the Jakob and Hanika PDF and Photrio returned 403; Smits 1999 not reached). It stays listed.
- Mickey's near-black night front, black glass and edge chips (9c): in the shopfront skill.
- Puddle decals (set aside 8 Oct): the skill already says they wait.
- The pale line's packaged check: no record later than DECISIONS 2 Nov 09:31 was found, so the skill's line stands.
