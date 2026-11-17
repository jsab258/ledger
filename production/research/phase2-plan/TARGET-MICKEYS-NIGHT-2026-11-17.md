Method researched: NIGHT-2026-10-08.md (shop-glass-reflections), 1c-night-pools-lumen.md, LIGHT-2026-10-26.md

# Target: Mickey's front at night, the too-dark fault (17 Nov 2026)

Waiting item 5 of the order of 16 Nov (production/orders/2026-11-16.md line 40; earlier waiting item 3 of 9 Nov). What Mickey's front must read and measure at night; not the build. Tags: M measured, R read at the source, I inferred, UNVERIFIED not confirmed. "Read 17 Nov" means read today. Project files carry their own dates. Revised 17 Nov after its review (production/research/phase2-plan/reviews/TARGET-MICKEYS-NIGHT-REVIEW-2026-11-17.md) and the session's decision from canon of the same day: **the front room is a working minicab office, the dispatcher on duty, lit at night; only Mickey's inner office stays locked and dark.**

**Questions.** 1) Where the fault is recorded and what it is. 2) Why it went dark since its pass of 8 Oct. 3) What real night values and the reference games give for a front, its window and the pavement before it. 4) What exists to reuse. 5) The check, and what passes.

**Reference first.** Kingdom Come II puts light *through* windows as plane lights set in the opening, about 0.5 m wide with the wall's depth built in: 290 in Kuttenberg's region, 104 in Trosecko; its town lights reach a median 4.3 m, warm orange, no physical units (studies/05-visuals.md items 1 and 3, read 17 Nov; meaning of the fields inferred by the study). Mafia: each street lamp is a key spot plus a 1 m bulb point; **wall lamps are spots of 0.25 to 0.5 cd, reach 8 m, 2400 to 2750 K, with a light profile**; no point light casts a shadow; a fake-room window material with a warm glow of 0.3 and one global tint; night exposure compensation +2.75 to +4.0 (same study, item 3, table rows 51 to 57). Neither study names a method for a lit shop or office front at night as such: for that, **none found**; the nearest methods are KCD2's plane light in the opening (already copied as Rita's window spill) and Mafia's wall-lamp spot. Their numbers are not physical and are not taken; only the method and the lamp-to-ambient ratio carry over (Study 5).

## 1. The fault as found

- **Recorded:** the corner's packaged views, 6 Nov 6:01, "Not narrow, listed: Mickey's near-black window and night front" (production/archive/DECISIONS-to-2026-11-09.md line 1098; evidence folder F:/LedgerTools/gate/new/corner-packaged-2026-11-06, absent from F: on 17 Nov). The fresh hook-night reviewer of 7 Nov: "Mickey's near front very dark at night; the fascia, door and window nearly merge", and against the bar: "Mickey's, the hero of the frame, sinks almost to black while the near brick stays a saturated red" (F:/LedgerTools/gate/new/corner-end-2026-11-07/review-hook-night.json lines 27 and 59, read 17 Nov).
- **Not in FINDINGS.md.** FINDINGS line 8 holds only the black reflection in the glass, mended 4 Nov. The test-plan review of 8 Nov already noted the missing record (production/research/qa-practice/TEST-PLAN-REVIEW-2026-11-08.md item 4). The session should add one FINDINGS line when the item opens.
- **Seen 17 Nov, by eye only (not measured; no measuring tool was available to this helper):** in cam_mickeys at night (corner-end-2026-11-07/r1/cam_mickeys-night.png) the room behind the glass is unreadable; only the sill, the pot plant, the directories, the blind's left edge and the gilt number read. In the last good of 8 Oct (F:/LedgerTools/gate/new/office/2026-10-08-t1/cam_mickeys-night.png) the counter, the notices, the fares card and the board read dimly. In the hook night view (corner-end r1/cam_hook-night.png) the fascia, pilasters, door and window form one dark block; the tiled stallriser and the gilt name read.
- **Tries spent on this fault:** none. The two pool-tilt tries of 21 Oct belong to lamp post C's glare (unreal-look.json lantern_pool_tilt_deg_note).

## 2. Why it went dark (candidates, I unless marked)

1. **The pools were cut to a third on 29 Oct.** lantern_pool_lumens 500 to 167, "the night pools 500 to 167 lumens, since the brighter ground takes three times the light" (unreal-look.json ground_coat_note, R, re-read 17 Nov). The ground's base colour rose; the front's did not, so everything the pool lights besides the ground lost about 1.6 stops. The 8 Oct pass was at 500.
2. **The front stands at the pool's edge.** Mickey's sill is about 37 degrees off the near lamp's axis and the gilt fascia about 44, against a cone of 22 to 46 (lantern_pool_cone_note_8_october, lantern_pool_tilt_deg_note, R). Between the inner and outer angle the light falls away, so the upper front gets little even at 500.
3. **The front room is dark in the specs, against today's decision.** "lit_at_start": false (shop-interiors.json, lit_note of 7 Oct) and "dark_until_inside": true (mickeys-office.json door, 6 Oct) keep the whole front room unlit until Tom arrives with the key, from Sheila's line that the office is locked since Mickey died (R). Today's decision reads that line as Mickey's inner office only; the front room is a working, lit minicab office at night. So the unlit room is no longer a design to keep but a spec to change: both keys need a new record in DECISIONS.md, and "dark_until_inside" moves to the inner office alone (whether the inner office has its own key in the specs: UNVERIFIED). An unlit room was already so at the 8 Oct pass, so it is not what changed, but it is the window's main missing light.
4. **Dark paint, not the sodium colour.** The fascia and painted frame are linear (0.0625, 0.0875, 0.119) (tools/art-recipes/paint_wood_tile.py line 64, R), luminance about 0.085. Under the lamp's (1.0, 0.25, 0.0) the effective reflectance is about 0.074, only about 12% lower (arithmetic, I). So the blue paint is not the main cause; its low albedo is period-plausible (UNVERIFIED: no 1990 paint measure read).
5. **The 4 Nov night fill** (0.4 lux, pitch -70) falls steeply, so it lights tops and ground more than a vertical front (night_fill_* in unreal-look.json, R; effect on the front I).

The split test in section 5 decides which of 1, 2, 4 and 5 still matter once the front room is lit.

## 3. Real values and aims

| Quantity | Value | Source |
|---|---|---|
| Lit domestic windows at night | about 6 cd/m2 average | Novak et al., CIE 2025 Midterm, DOI 10.25039/x051.2025/kc7797, read by the 8 Oct note; re-fetched 17 Nov but the PDF could not be decoded here: second hand, UNVERIFIED today |
| Lit shop windows at night | about 50 cd/m2 | same, same status |
| Lit residential pavement | 2 to 15 lux (EN 13201-2 via a search summary), so about 0.1 to 0.7 cd/m2 at albedo 0.15 | NIGHT-2026-10-08.md; standard not read: UNVERIFIED |
| So, window over pavement | lit windows 10 to 100 times the lit pavement (3.3 to 6.6 stops), shop windows the top of that | NIGHT-2026-10-08.md arithmetic (I) |
| Pool to gap, real night photographs | 3.0 to 5.2 stops (95th over 10th percentile, four CC0 Poly Haven HDRs, none British sodium) | 1c-night-pools-lumen.md, measured 8 Oct by an earlier helper (M, second hand) |
| Office interior | 320 to 500 lux | https://en.wikipedia.org/wiki/Lux (read 17 Nov through the fetch tool's reader; tertiary) |
| Low-pressure sodium lamp, source | 75,000 cd/m2; fluorescent lamp 12,000 | https://en.wikipedia.org/wiki/Orders_of_magnitude_(luminance) (read 17 Nov; tertiary) |
| Floodlit buildings | about 2 cd/m2 | same page (tertiary, "based on an exposure value table") |
| Passed lit windows in the game's hook night view | Rita's mean 88 of 255, fish shop 98.5, launderette 108 (line 66); settled hook night frame mean 16.2 (line 63) | production/audits/gate-ritas-front/GATE.md (R, 22 Oct; re-read 17 Nov) |
| Pavement under Rita's lit window | 216 to 105 of 255, **in the "From the right" view, not the hook view** | same file, line 69 (R) |

The game's lights are not physical (Study 5; unreal-look.json lantern notes), so the aims are display values through the game's own camera and pin, set from the ratios above and the passed peers. Each is a judgement where marked. **All aims are judged with the front room lit, its night state from today.**

**Aim A, the front reads (the fault).** In the hook night view, a box over Mickey's fascia, pilasters, door and window frame: near black (luma under 10 of 255) on at most 40% of it (I, judgement; today by eye most of it); the fascia, the door and the window each separable from its neighbour, luma ratio at least 1.3 (the n16-5 plan's night fascia bar PC-06, N16-5-PLAN-2026-11-17.md C5); the gilt letters at least 2:1 against their board (the 8 Oct verify line, lantern_pool_cone_note_8_october). Floodlit fails too: the front box median at most 60 of 255 (I; real floodlit fronts about 2 cd/m2, about the lit pavement's level or a little above). The same front box is read in the reverse night view, where the front is seen from up the street: near black at most 40% there too (I, judgement).

**Aim B, the lit window (the main aim for the window).**
- The window's mean in the hook night view 80 to 110 of 255, with the passed peers (R above); any channel at 250 on at most 1% of the window (N16-5-PLAN C5); the window at least 2 stops over the lit pavement box (1c-night-pools-lumen.md section 5 row "Lit windows", from the real 3.3 to 6.6 stops compressed by the tonemapper, I).
- In cam_mickeys at night: the room reads as a working office, the counter, the board, the notices and the radio desk named by the reviewer (judgement); the room box mean at least the 8 Oct last good's, which step 1 measures first as the floor (UNVERIFIED until then); reflected lit rectangles at least 40 of 255 (room_glow_gain_night_note_8_october).
- Mickey's inner office (the locked door) stays dark: no light seen through its doorway from the front room or the street (judgement).

**Aim C, the pavement in front.** The nearest pool's clipped red at most 2% (pool_clip.py, his order of 8 Oct); the flags between the pool and Mickey's door not black, median 10 to 30 of 255 (1c's road-gap row applied to the footway, I). The lit window's spill on the flags, in the **hook night view**, a box on the flags directly before the window outside the lamp pool: its median at least 1.5 times the unlit footway gap's and at most the lamp pool box's median, with no clipped pixel (I, judgement; **UNVERIFIED**: no hook-view value for a passed spill exists; Rita's 216 to 105 was the "From the right" view, so it is not this bar). Step 1 measures Rita's and the fish shop's spill boxes in the same hook frame as peers and replaces this bound with their range if they differ. Darkness between pools kept (RULINGS 1 Oct night line): pool to gap 3.5 to 6.5 stops (1c section 5) where measured.

**Not changed:** the day's exposure (RULINGS 29 Oct), the night pin 0.4 and bias 0, the lamp cones (street-weathering skill, "cones not widened"), the pool tilt 0, the ground's coat and gains; the lamp colour stays sodium.

## 4. Reuse first

- **Lights:** Rita's window spill, a tube-white rect light in the window head on lighting channel 1, tipped 62 degrees down, 60 lm (shop-interiors.json Rita's spill_*, display_lights; KCD2's method, already copied). Mickey's anglepoise (60 lm, 30 degree cone) and tubes (300 lm at night) with the room's held exposure 1.6 and local exposure 0.6/0.6 while the camera is inside (mickeys-office.json "inside"); the lamp's key spot and 1 m bulb (Mafia's method, unreal-look.json lantern_*); the night fill.
- **Materials and pictures:** the room pictures per state (shop-interiors.json "states": day, night_lit, night_dark; night_lit is now the front room's night state); room_glow_gain_night 0.4; the glass's per-window night cube (eg_bay0, re-baked 4 Nov; to re-bake with the room lit); the gilt (gilt_metal_rgb); the fascia and frame rows (ps5-corner.json paint_fascia, frame_painted).
- **The light-weather target's values** (TARGET-LIGHT-WEATHER-2026-11-17.md section 4): wet_night wetness 0.90, fog 0.022 at gain 0.2, lantern 40 lm and pool 167 lm, cone 46, light 4.83 m, fill 0.4 lux warm, pin 0.4; sodium (1.0, 0.25, 0.0).
- **Tools:** production/audits/night-2026-10-08/pool_clip.py (hook boxes only); tools/measure_night_pools.py; tools/office_look.py --night; tools/shop_views.py --night (ten views; Mickey's window middle to read first, UNVERIFIED); the -NightTest= switches (1c section 4); the glass dump -GlassCatchDump (NIGHT-2026-10-08 step 1).
- **Missing:** a box tool for Mickey's front in the hook and reverse night frames, its window and the flags before it, and the window in cam_mickeys; a lighting channel that keeps a ground-only cut off the fronts (I: whether VignetteShot.cpp can split the pool by channel is UNVERIFIED).

## 5. Method, smallest first (two tries for the fault, then research)

0. **The front room lit at night, the baseline** (0.75 h): shop-interiors.json "lit_at_start" true for the front room's tubes and anglepoise at night (and "lit_at_night" as now), mickeys-office.json "dark_until_inside" kept for Mickey's inner office only, each with its DECISIONS.md line citing today's decision; the night glass re-baked with the room lit. Not a try at the fault: the specs brought into line with canon.
1. **Split test, no further change to the look** (0.75 h): hook, reverse and cam_mickeys at night, settled 30 s, at scalability 2, with the room lit: as is; pool at 500 (-LanternPoolLumens=500); fill off. Measure the front box, the window box and the flags' spill box in each, and the 8 Oct cam_mickeys room box (aim B's floor), and Rita's and the fish shop's spill boxes in the hook frame (aim C's peers). Pass: it names which of candidates 1, 2, 4 and 5 still holds the front down once the room is lit; if the lit room alone meets aims A to C, the item goes straight to the check.
2. **Try 1, the window's own light and the fronts' share:** Rita's spill light (KCD2's plane light in the opening) in Mickey's window head, so the lit office lays its window on the flags (aim C); and, if candidate 1 holds, give the fronts back the light the 29 Oct cut took without brightening the ground: the pool kept at 167 on the ground, a front-facing share on the fronts by lighting channel, or the cut moved into the ground's own gain (I; which is cheaper is the try's first read). Check aims A, B and C.
3. **Try 2, if the fascia and pilasters stay dark above a lit window:** Mafia's wall-lamp method, one small warm spot over the door or fascia (0.25 to 0.5 cd as a ratio to Mafia's key spot, not as a value; 8 m reach; shadows off), only if a 1990 minicab front carried such a lamp or a lit sign: UNVERIFIED, and a look change for his page.

## 6. The check

- Cameras, all with the front room lit at night: hook night (the fault's view, 2560x1440), cam_mickeys night (the window and the room), reverse night (the front from up the street, aim A's second box), and the office_look counter view at night (the lit room inside, nothing broken, the inner office's door dark). Packaged copy for the verdict; editor pictures only as screens, at scalability 2, after the 30 s settle.
- Numbers: aim A's box shares and ratios in the hook and reverse views; aim B's window mean, clip and stops over the pavement, the room box against the 8 Oct floor, the reflected rectangles; aim C's pool_clip.py, the footway median and the spill box against its bound; the frame's near-black share reported, not failed (skill section 6).
- Gate: one fresh reviewer per view beside the last good (8 Oct cam_mickeys, 7 Nov hook and reverse), the Hook sheet (mirrored for the hook view) and the KCD2 frames; new faults block; the whole-frame look of the hook view reaches his page before merging (the front is the frame's hero). Then the night walk by the AI tester.
- Fails: one orange wash; light seen in Mickey's inner office; light from nowhere; the near pool over 2% clipped; the window a blank light box (over 1% at 250); anything in the window suggesting alcohol, gambling or children.

## 7. Hours

Front room lit, specs and records, glass re-bake 0.75; split test 0.75; box tool (front, window, flags, room) 0.75; try 1 (spill light and the fronts' share) 2.0; try 2 1.0 (only if needed); pictures, reviewers, packaged walk 1.0; records (DECISIONS, RECIPE, FINDINGS, catalogue) 0.5. **About 6.75 h** (5.75 without try 2). The shopfront skill notes records running 2 to 4 times plans.

## Open questions

1. **Decided 17 Nov from canon (the session):** the front room is a working minicab office, the dispatcher on duty, lit at night ("one driver by day, one by night, and the dispatcher", DECISIONS archive line 119; the glass says "MINICABS · TILL 3 A.M."); only Mickey's inner office stays locked and dark. Closed.
2. Whether a 1990 British minicab front carried a door lamp or a lit sign box: no dated photograph read.
3. Whether VignetteShot.cpp's pool can be split by lighting channel without a code change.
4. Whether the specs already distinguish the inner office from the front room for "dark_until_inside", or that needs a new key.

## Unverified (13)

Novak 2025's 6 and 50 cd/m2 (not re-read today); EN 13201's 2 to 15 lux; BS 5489 values for 1990; the pool-to-gap stops (second hand); aim A's 40% and 60-of-255 bounds (judgement); aim C's footway 10 to 30 (carried from the road); aim C's spill bound in the hook view (no measured peer yet); period paint albedo; a 1990 cab office's door lamp or sign; the room's 8 Oct box mean (to measure); the channel split; the inner office's own dark key; Mickey's window middle for shop_views.py.

## Sources read 17 Nov 2026

RULINGS.md "The look and the street"; orders of 9 and 16 Nov; FINDINGS.md; the DECISIONS archive (6 Nov 6:01, 7 and 8 Oct rows); DECISIONS.md (search); TARGET-LIGHT-WEATHER and TARGET-RITA-FIXES (shape); N16-5-PLAN-2026-11-17.md; the street-weathering skill sections 5 to 6; studies/05-visuals.md; NIGHT-2026-10-08.md; 1c-night-pools-lumen.md; LIGHT-2026-10-26.md; DARK-GAP-2026-10-27.md; gate-ritas-front/GATE.md lines 55 to 74; TEST-PLAN-REVIEW-2026-11-08.md (search); unreal-look.json (night, lantern, glow, ground coat); mickeys-office.json; shop-interiors.json (Mickey's and Rita's); ps5-corner.json (paint rows); paint_wood_tile.py line 64; the corner-end 7 Nov review files; this target's review of 17 Nov; pictures looked at, not measured: cam_mickeys-night (8 Oct t1, 7 Nov) and cam_hook-night (7 Nov). Web, through the fetch tool's reader: https://en.wikipedia.org/wiki/Lux and https://en.wikipedia.org/wiki/Orders_of_magnitude_(luminance).

## Unreached

Novak et al. 2025 PDF (https://files.cie.co.at/x051_2025/P0796_ID298TomasNovak_OA_with_cover.pdf: fetched, compressed text not decodable here); EN 13201-2 and BS 5489-3:1989 texts; the ILP's obtrusive-light guidance (not tried); any dated photograph of a British minicab front at night; F:/LedgerTools/gate/new/corner-packaged-2026-11-06 (absent); Mafia's lamp Blueprints and window-glass materials (not in the study's export); KCD2's night exposure (not found by the study).
