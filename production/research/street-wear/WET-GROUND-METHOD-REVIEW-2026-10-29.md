# Wet ground method: review (29 October 2026)

A fresh reviewer, read only. Every page was read on 29 October 2026.

## Verdict: PASS WITH FIXES

The direction holds; its sources say what it quotes, except as below. Steps 1 to 5 wait for fixes 1 to 6.

## Faults

1. **Step 3's flat top normal flattens the daylight.** Lumen's screen-probe diffuse uses the top normal (LumenScreenProbeGather.usf 963, 1381); only its rough specular (1524) and direct lights (DeferredLightingCommon.ush 327) take the bottom. Under overcast nearly all light is Lumen's, so the relief would go again, as at 14:27. Lagarde blends the normal to flat by the water (2b: N = lerp(N, flat, AccumulatedWater); 3b: "a slight smoothing" for thin water). Fix: top normal = lerp(stone, flat, c); bottom = stone; §1 to say "rough specular only".
2. **Step 2's check cannot be read under a coat.** The roughness view shows the stone only; coat amount and roughness sit in CustomData, which UE 5.8 has no buffer view for (BaseEngine.ini). Fix: a debug switch writing c into base colour for one capture, read with surface_values.py boxes: c ≥ 0.9 and ≤ 0.1, under 10% between, mean c per surface.
3. **Step 4's first option cannot make water on a coat.** A DBuffer decal writes only base colour, normal, roughness, metallic and specular (DBufferDecalShared.ush 508-529; Epic's decal page): roughness lands on the stone, the normal on the coat, and under the coat Specular is pulled to the refraction term (ClearCoatCommon.ush 42). That answers "how decals reach its bottom layer". Fix: the DBuffer read alone (Decal Response None, stains re-applied through ApplyDBuffer), naming the channel carrying c and keeping oil and grime off it.
4. **Mean c 0.4 to 0.6 belongs to the brighter exposure.** It is ROAD-NOTES' factor at 8 October's exposure, about pin 2. At pin 4, round 3b, a full film over the whole road, read 178/163/193 against 2c's 152/164/183 (measure_road.py, re-run); half that reflection leaves the reverse regions about 30 to 35 levels short (I). Step 3's c and its own 2c check cannot both pass. Fix: derive c at pin 4 from the morning and round-3b readings; if a broken film cannot meet 2c at the darker day, that is one question for his page, not a tuning.
5. **Step 1's formula misses its own check.** Asphalt 0.10-0.12 × 0.68-0.75 gives 0.068-0.090 against 0.05-0.06; flags reach 0.24 against 0.20 (M). The water's 0.02 is not subtracted (FLAGS-BRICK-BANDS §5), and 0.75 is Lekner and Dorf's ratio at 0.08, not 0.10-0.12 (0.68 to about 0.71). The flags' band has two homes: 0.11-0.20 (surface_values.py) and 0.09-0.22 (FLAGS-BRICK-BANDS, reviewed later). Fix: wet base = dry × that ratio − 0.02; one band, its home named, surface_values.py matched.
6. **Step 5 makes two changes for one fault.** Dividing the lamps by the albedo ratio returns the pool's linear light to the morning's (0.1% clipped); highlight contrast 0.75 is then unneeded and shrinks pool against gap, against "pools of lamp light with darkness between". Fix: lamps alone first; 0.75 only as a second try if clipped red stays over 2%. Measure with the 8 October rule's own pool_clip.py (rounds 2 and 3b: 14.0% and 14.2%). Add Mickey's fascia at least 2 to 1 and the lamp-lit brick, which a divisor fitted to the flags darkens.
7. **Step 3's other checks have no project tool.** Blue against red, p90/p10 and dash to road live in session scratchpad scripts, and their sheet boxes are not the game's regions (sheet middle road 70 to 76% across, game 25 to 30%). Fix: move them into production/lab/road/ with boxes stated and pictured.
8. **Step 4's check cannot run.** stain_check.py finds a mark by its roughness change and needs a with-and-without pair; only -NoOfficeWear exists, its camera mode reads mickeys_room only, and a black stain with no roughness change is not found. M_LedgerGrime also lays the kept walls' streaks, soot and algae and the light TintOnly marks. Fix: a ground-only "without" switch, selection by base-colour change, the walls' and light marks' tint left alone.
9. **Smaller source points.**
   - Far Cry 6's wetness shadow map serves props and structures, not terrain or puddles.
   - "Water over wet stone barely darkens it further" is not in 3b; it is inferred: tag I. 3b does call the 0.04 to 0.02 change "not visible enough in game", which supports the coat's 0.04.
   - "Within about 17%" was computed for Default Lit at roughness 0.10; the coat's Schlick 0.04 is 18 to 20% over water at 10 to 20°, 35% at 40° (M): tag I.
   - Round 2's dash ratio, 6.0, comes from no kept script.
   - Step 3 is Lagarde's structure, not Mafia's: say so, for the reference-first rule.

## Rulings

Nothing brightens the day camera (29 October). The night ruling (1 October) holds once fix 6 is taken.

## Re-checked

- Read in full: Lagarde's Water drop 1, 2a, 2b, 3a, 3b, 4a (4b never written); Ubisoft's Far Cry 6 page; the brugr9/Wetness README; Epic's Lumen, decal and auto-exposure pages. Their quoted numbers and claims match, except as above.
- Engine source, UE 5.8: ShadingModels.ush 357, 406-407; ClearCoatCommon.ush; LumenMaterial.ush 677; PostProcessHistogramCommon.ush 279-307; RenderUtils.cpp 2068-2071. Project: no Substrate, screen-probe gather.
- Re-run: the three scratchpad scripts reproduce the table; the gloss conversion gives 0.51 to 0.69 against 0.54 to 0.68.
