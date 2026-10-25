# Study 5: Visuals (25 October 2026)

How Mafia: The Old Country (Unreal 5.4) and Kingdom Come: Deliverance II (CryEngine) solve the visual problems LEDGER is stuck on: windows, shop glass, night light, wet streets, wear, materials and texture sizes. Read as settings and set beside our look file (production/specs/unreal-look.json) and our own research. Our own words and numbers only. Raw counts are on F:/LedgerTools/aaa-study/study-5/. All read 25 October 2026. Tags: **M** measured (counted), **R** read (a value in a file), **I** inferred.

**What could be read.** Mafia's material instances, light components, time-of-day presets and decals were read from Palermo (191 cells), the one readable town map; its master material graphs, its lamp Blueprints and its window-glass materials were not in the export, so how a value is scaled inside them is unknown. Kingdom Come II's light entities, probe files and settings were read; its time-of-day data and material parameters were not in the unpacked files.

## By problem

**1. Windows (ours read as white boards).**
- **Mafia** has a window material with a fake room behind the glass: a switch "Use Fake Interior", a depth offset (−7), refraction (3), a little glow (0.3) in a warm tint, and a flat atlas of room pictures (R). One global colour dims or tints every fake room at once (R). The one exported use is an opera window (30 uses); three fake-room shapes exist as meshes, but no Palermo cell places them (M).
  - Game curtains use the main opaque material (R). By name: 742 window, 526 glass, 110 curtain and 73 shutter assets.
- **Kingdom Come II** builds windows from a kit (about 219 window and 38 shutter mesh names) (M) and puts the light *through* them as plane lights set in the opening: 290 in Kuttenberg's region, 104 in Trosecko (M). Each is about 0.5 m wide with the wall's thickness built in (median 0.25 m, up to 1.5 m), so the light falls as the reveal shapes it (R; meaning inferred from field names).
- Window frame depth in the meshes, and windows seen from a low street angle: not measured.

**2. Shop glass (ours costs frames).**
- **Mafia** has no reflection captures and no planar reflections in Palermo (M). Reflections are Lumen's; no ray tracing; Lumen's front layer on see-through surfaces is allowed from reflection level 2, the PC default (R); whether its window glass uses it was not seen, because its window-glass materials are not in the export (an unexported fake-glass master may be its answer). Its two exported glass instances are stained glass, so their values say nothing about shop windows.
- **Kingdom Come II** bakes probes instead: 23,270 probe files in Kuttenberg's region and 7,893 in Trosecko, about 0.10 MB a pair, baked at 11 times of day; about 7.2 GB for both regions (M). Screen-space reflections at half resolution by default, full at its two top levels (R).
- **No reflection cost figure** was found for either game.

**3. Night light (ours lacked pools).**
- **Mafia's lamps are two lights each** (M): a key spot that makes the pool and a tiny point light for the bulb's glow.
  - The common street lamp (39 in Palermo), at its most common setting: spot 1.5 cd, reach 20 m, cone 80°, 4500 K; bulb point 0.45 cd, reach 1 m. Its key spots run 0.5 to 25 cd; 20 of 39 show volumetric scattering 2.5 in the fog; 25 of 39 have shadows off and 14 do not say (the engine's default casts) (R, M). The lamp Blueprint carries a multiplier (3), so the true values may be higher.
  - A second lamp (9): spot 4 cd, 15 m, 2400 K, with a light profile (IES). Wall lamps: spot 0.25 to 0.5 cd, 8 m, 2400 to 2750 K, with a profile.
  - None of the 135 point lights that state a shadow setting casts one (M). Medians: points 0.2 cd, 1 m; spots 8 m, 70°, drawn to 30 m.
- **Its scale is not physical:** the sun is only 7 to 15 by day, 0.0035 to 0.1 at night; the sky 1.2 to 7 by day, 0.0005 to 0.045 at night; exposure compensation +2.75 to +4.0 at night (−1 to +1.5 by day) with a floor of 1.0 (R, 103 presets). Night fog is dense (0.035 to 0.05). A faint fill light (0.1, 4500 K) keeps faces readable. Exposure scales lamps and the dark between them alike: the pool comes from the ratio of lamp to ambient light, not from the exposure.
- **Kingdom Come II's lights have no physical units.** Its town lights: reach median 4.3 m (a tenth reach 8 m), warm orange; 150 of 1,000 throw a lantern pattern; 14 of the 1,000 switch by clock (its cutscene lights are the ones mostly clock-switched) (R, M). Its night exposure was not found.

**4. Wet streets (ours mirrored the sky).**
- **Mafia:** one global wetness value (0 by default) drives roughness to 0.1 on flat ground and 0.2 on slopes (R). Puddles are decals with a height, roughness and occlusion texture and a 2×2 mask atlas; 232 in Palermo (M). A flood-level switch on the wall material is used only 4 times.
- **Kingdom Come II:** rain is a screen-space layer drawn to 150 m (40 m at the low level) (R). No puddle or wet-street material was found among 7,572 materials.

**5. Wear.**
- **Mafia:** Palermo holds 2,461 decals of 180 materials (M): 40% water and rust leak stains, 9% puddles, 9% plaster grunge, 8% flood-line stains at wall bases, 2% lichen. They sit in 41 cells, a median of 11 a cell; the densest (878) is an underground tunnel holding most of the flood lines, and without it the mix is much the same (M). About 650 decal materials sit on 5 masters in the export; 14 grunge types; a dirt mask on glass (R).
- **Kingdom Come II:** a decal atlas of 256 px in 12 slices; 212 decal materials (M).
- Decals per street: not counted (only per cell).

**6. Materials.**
- **Mafia's shared library:** 253 masters and 1,189 instances (the whole game's name index holds 328 masters and 11,843 instances) (M). The main master has 307 instances and three textures (colour; a packed height, roughness and occlusion map; normal) plus a tint (R). Walls: 130 on the main master, 38 on a two-layer vertex-painted master.
- **Kingdom Come II:** one material per asset (7,572), drawing on 135 shared surface materials: 26 ground, 24 wall, 19 wood, 8 stone, 5 metal, 2 glass (M).

**7. Texture sizes.**
- **Mafia** (about 350 each of colour, normal and mask textures): 4096 px 21%, 2048 px 36%, 1024 px 38% (M). The engine's size bias in its config applies to texture groups these textures do not use, so their in-game cap is not known; 110 textures carry their own bias of −1 (R). Decals mostly 1024 (M).
- **Kingdom Come II** (bytes in the archive index): building textures median 2.8 MB (a tenth above 11), people 1.4, furniture 0.7, small props 0.35 (M).

## Settings sheet, beside LEDGER

| Setting | Mafia | Kingdom Come II | LEDGER now |
|---|---|---|---|
| Light units | candela, scale not physical | unitless | lumens (lantern 40, pool 500) |
| Lamp | key spot (commonly 1.5 cd, 20 m, 80°) plus a bulb point; a multiplier in the Blueprint | reach 4.3 m | one lantern light plus a pool light |
| Small-light shadows | point lights none; lamp spots mostly off | budget per frame (Study 12) | the street-lamp pools cast; window lamps within 15 m |
| Light profiles | IES on 2 of 3 lamp kinds | pattern on 150 of 1,000 | none |
| Night exposure | compensation +2.75 to +4.0 | not read | a deliberate two stops under (night_exposure_pin 0.4) |
| Night fog | density 0.035 to 0.05 | 525 fog volumes | a gain of 0.2 on the fog (not a density) |
| Reflections | Lumen, no captures | probes at 11 times of day | Lumen front layer plus per-window captures (256 px; 1,024 hero) |
| Shop glass | not exported | quality 2 of 0 to 3 | Thin Translucent, opacity 0.06 for dirt only, rough 0.02 |
| Fake rooms | a material switch and a global tint, rarely used | light planes in the openings | picture rooms behind windows |
| Wet ground roughness | 0.1 flat, 0.2 slopes | rain layer to 150 m | paving 0.1, kerb 0.15, asphalt 0.06 |
| Puddles | decals, 232 in Palermo | none found | none (set aside on 8 October) |
| Wear decals | 2,461 on 180 materials | 256 px atlas, 212 materials | street-wear.json |
| Main material | one master, 3 textures plus a tint | per asset | kit-materials.json |
| Texture budget | 4096 / 2048 / 1024 in 21 / 36 / 38%; in-game cap not known | building median 2.8 MB | 512 px a metre; 2048 tiling sets, 4096×2048 trim sheets (pre-production/4-BUDGETS.md) |

## One target per open visual problem

1. **Windows:** our own research (aaa-street/WINDOWS-GRAZING-2026-10-08.md) finds the white boards are flat-lit joinery at a low angle, where the reveal hides any room behind, and that fake rooms fail at shopfronts (shop-glass-reflections, close range). So: shade the frames first; a fake-room material, with one global night tint as Mafia has, only for upper and distant windows. Check: no window reads as a flat white or black board in the three morning views.
2. **Shop glass:** keep the per-window captures. Our research found software Lumen's front layer showed almost no street, which is why the captures exist, and the 23 October card-time study (frame-headroom/CARD-TIME-2026-10-23.md) found the front layer itself costs about 0.06 ms. Add the dirt mask (Mafia has one; it fits our recipe). Nothing in either game changes this.
3. **Night pools:** each lamp as Mafia builds it, a key spot with a light profile and some volumetric scattering in the fog, plus a tiny bulb light; point lights cast no shadows. The street-lamp pools keep their shadows (a choice made for our street, to be priced against the shadow-light budget of Study 12). The pool comes from the ratio of lamp to ambient light, so judge that ratio, not the exposure. Check: pools on the pavement with dark between them, in the street-at-night view.
4. **Wet streets:** wetness as one global value driving roughness (Mafia: 0.1 flat, 0.2 slopes; our asphalt's 0.06 is glassier). Our research found roughness 0.16 read as dry, so set it by eye between those. Puddles as decals in low spots return only when the puddles set aside on 8 October are taken up again (aaa-street/PUDDLES-2026-10-02.md). Check: no sky mirrored across the whole road.
5. **Wear:** a decal mix close to Mafia's street mix: leak stains under sills, gutters and pipes (about two in five), grime at wall bases, plaster grunge, densest where the player walks. Check: Quay Street's decal count by kind, against the mix.
6. **Materials:** one main master (colour, packed height-roughness-occlusion, normal, tint) and one two-layer vertex-painted wall master for dirt at the base.
7. **Texture budget:** our own budget stands (4-BUDGETS.md: 512 px a metre, 2048 tiling sets, 4096×2048 trim sheets); Mafia's spread of sizes (a fifth at 4096) is consistent with it.

## Coverage map

Ticked: rendering and the look (windows, glass, light, wet, wear, materials, textures) for both games, settings side. Open: master material graphs, lamp Blueprints and window glass (not exported).

## Open blind spots

- Kingdom Come II's time of day, exposure and sun values (only 33 profile names found).
- Kingdom Come II's material parameters and window depths.
- Mafia's master material graphs, lamp Blueprints (the real scaling of candela), window-glass materials and whether its front layer is used on windows.
- Lights and decals per street; windows from a low angle; net curtains; any cost figure for reflections.
- What 6,374 of Kingdom Come II's 7,572 materials are.

## Sources

- Mafia: material instances, light components, time-of-day presets and decals exported from Palermo; the name index of all packages; DefaultEngine and DefaultScalability; F:/LedgerTools/aaa-study/study-5/.
- Kingdom Come II: level light entities (Kuttenberg's region and Trosecko), the probe files in the level archives, Engine.pak settings; F:/LedgerTools/aaa-study/study-5/.
- LEDGER: production/specs/unreal-look.json; production/research/shop-glass-reflections; aaa-street/WINDOWS-GRAZING-2026-10-08.md and PUDDLES-2026-10-02.md; frame-headroom/CARD-TIME-2026-10-23.md; pre-production/4-BUDGETS.md.

## Review

A fresh reviewer (25 October, evening) checked the CSVs, configs, Kingdom Come II's index and our own files: pass with fixes. Corrected here: eight wrong counts (shutters, decal materials, the library's size, the probes' size, the clock-switched lights, the texture bias, a median, Kingdom Come II's window kit); unsupported claims removed (fake rooms placed, dithered curtains, lamps without shadows); the glass row re-scoped (Mafia's window glass is not in the export); the light units and exposure read rightly; our own column corrected (pool shadows, fog gain, texture budget); targets 1, 2 and 3 rewritten against our own research, which target 2 had contradicted.

Cost, from the clock: the helper to about 21:40, this synthesis to 21:48, the review to about 22:03, its fixes to 22:05.
