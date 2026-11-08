# Review: street-weathering additions (8 November 2026)

Fresh reviewer, 8 November 2026. DECISIONS.md and RECIPE.md were searched, not read whole. Read: the proposal, both skills, RULINGS "The look and the street", the look file's notes, SURFACE-BANDS, LAMP-STAINING-BAKE, gate-lamp-post-C GATE.md, GATE-NIGHT.md, street_wear.py, make_wear_masks.py, VignetteShot.cpp (the fill and the moon), the order of 2 Nov and its archive, and the memory note grime-tint-times-grey. The commit 8db3212 was looked at read-only.

**Verdict: PASS WITH FIXES** (7 faults, none blocking).

**The night-fill replacement (check 2): confirmed.** His midweek answer (DECISIONS 4 Nov 18:21, point 3) asks for "an overcast town sky's dull orange glow and a little fill, the lamp pools kept". DECISIONS 4 Nov 23:07 records that it replaces the 29 Oct stop. The look file's night_fill_note says "overriding 29 October's stop". The moon is still a trial switch only (VignetteShot.cpp). No haze change was committed on 4 Nov, so the "unverified" on the haze's home is honest.

Everything else checked out: the lamp bake, the tilt, the lit windows, the 16 cm climb, the tint times the grey, the 5 m bands every 2.5 m, sea_specular, the LRV rule (tagged I), and RECIPE 26 and 29 Oct.

## Faults

1. **Addition 2: a stale sentence is left in place.** The replacement starts at "NIGHT-GAPS...". That leaves "How dark the gaps are is his ruling, not a fault (DECISIONS 29 Oct 06:02)", which his 4 Nov note overrode. Source: DECISIONS 4 Nov 18:21 and 23:07. Fix: start the replacement at "How dark the gaps are", and cite the note's own record (18:21, point 3) beside 23:07.

2. **Addition 2: two stops are dropped without a source.** The 29 Oct stop also covered lifted blacks and the night sky gain, "not used unless he asks". The new text keeps only the cones and the moon. "Step 6" is unclear. Source: DECISIONS 29 Oct 06:02; the skill, line 17. Fix: add "lifted blacks and the night sky gain stay unused unless he asks", and write "section 6" for "step 6".

3. **Addition 3: the kiosk band is for the wrong kiosk.** SURFACE-BANDS §6 gives a K6's red. The skill's own line 39 says the street's kiosk is the grey steel KX100. Fix: say the kiosk-red band is a K6's and does not apply to the street's grey kiosk.

4. **Addition 9, bullet 1: a cause is stated as settled when it is not.** "A saturated fill turned unlit brick pure red" comes from RECIPE 4 Nov. After the less saturated fill, the brick was "still near pure red" (DECISIONS 5 Nov 05:40), and the proposal's own "Not added" lists it as a shortfall. Also, 66% to 45% was measured in round 1, before try 2. Fix: add that the brick stayed near pure red after the change (listed), and that the 66% to 45% is round 1's.

5. **Addition 9, header: a citation does not support the claim.** "Kingdom Come II: none found for the fill or the sky (DECISIONS 5 Nov 05:42)". The 05:42 entry says "Reference: none found" for the sky only. 23:07 states no reference for the fill. Fix: cite the fill's reference record, or mark "none found for the fill" as unverified.

6. **Addition 9, bullet 4: the day's sky is in the night section.** sky_seen_gain and sky_light_gain are day keys (DECISIONS 4 Nov 23:07, "Day's seen sky 13 to 7"). The night has its own keys (sky_seen_gain_night). Section 6 is "Night". Fix: label the bullet "by day" and move it out of section 6, for example after section 5, next to the water.

7. **Addition 5: a decal trap sits in the wrong section.** It is about projected decals but is added to section 3's room bullet, "Wear in the material first". Source: RECIPE 29 Oct. Fix: put the sentence in section 4, after the placement bullet.

No conflict was found with RULINGS 29 Oct (exposure kept), the shopfront skill (gilt is metal, Mickey's front, the window light), or grime-tint-times-grey.
