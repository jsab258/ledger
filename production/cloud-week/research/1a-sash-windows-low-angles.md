**In one line:** at the street's low angles almost no glass can be seen in a deep-set sash, and what does show is a pale, evenly lit card in a flatly lit white box with no dark lines and no reflected shapes, so it reads as a board; the fix, cheapest first, is to make the pane glass over a dark room, shade the box and draw its dark lines, then give the upper panes a reflection of the street.

# Sash windows at the street's low angles (cloud research, 8 October 2026)

Research helper, cloud session, about 40 minutes. I cannot run Unreal or see the game. I worked from the repository and the previews in it, plus the few web sources this cloud can reach.

**Tags.** [SHOWN] means I read it at its source today. [NOTE] means an earlier project note quotes it, read at the source on the PC on the date given; I did not re-read it today. [CLAIMED] means a vendor or press claim. [SS] means a search summary only: a lead, not evidence. [I] means my own inference or arithmetic.

**Network today.** The proxy refused dev.epicgames.com, unrealengine.com, Wikipedia, GDC Vault, 80.lv, ArtStation, NVIDIA, the press and every blog. Only raw.githubusercontent.com answered. So no Epic page was read today. Every Epic claim here is [NOTE] or [SS].

## 1. The question

From the third-person camera (eye height 1.7 to 2.2 m, looking along a 48 m street), why do the deep box sashes read as white boards, white slabs and white slits, and the far ones as bricked-up holes? And what change, cheapest first, makes them read as glass in a recessed frame?

The gate notes:
- GATE-2.md, hook view by day: the near-left terrace's lower sashes were "flat white boards" and the next house's windows "white slits".
- GATE-2.md, reverse view by day: most panes were "white slabs". The left row's far windows looked "empty or bricked-up". The "glass [was] not reading as glass".
- REVIEW-PHOTOGRAPHS.md: "the glass is one even grey… with nothing behind it"; "at an angle… the windows read as blank white panels".
- Third try: occlusion baked into the vertex colour and fed to the material's AO pin. It changed nothing visible: "the visible faces are the bright linings, and the shade lands only in the narrow channels."

## 2. How games and engines do windows at grazing angles

**What glass shows at a grazing angle.** A dielectric reflects more as the view flattens. Reflectance tends to 100% at grazing angles [SHOWN, Filament]. For float glass (n = 1.52) I worked it out from the Fresnel equations, both faces of the pane counted [I]:

| Angle from the wall | 90° | 30° | 24° | 18° | 16° | 10° | 8° |
|---|---|---|---|---|---|---|---|
| Pane reflects | 8% | 17% | 23% | 34% | 38% | 56% | 64% |
| Pane lets through | 92% | 83% | 77% | 66% | 62% | 44% | 36% |

Unreal's model with Specular 1 (F0 0.08) gives 26% at 16°, about two-thirds of the true two-face value [I]. That is close enough.

**Why games fade out the room at grazing angles.** Interior mapping is a technique for distance. Forza Horizon 4 fades the room out "at grazing angles" with the glass's Fresnel, and draws window, curtain and room as three layers [NOTE, CLOSE-RANGE-2026-10-03, read 3 Oct]. Spider-Man's painted rooms show flat furniture in close-ups (van Dongen, 2018) [NOTE]. At grazing angles every studio lets the reflection carry the pane [NOTE, I].

**What the reflection should contain** [I, from the street's geometry]:
- From below (the reverse view's upper windows), a ray leaving the glass meets the far side of the street at about 8.5 to 10 m. That is the eaves, roofs and chimneys, with sky only in the top panes [NOTE, WINDOWS-OTHER-DIRECTION]. A dark roofline cuts across a bright sky. That sharp horizontal edge is what reads as glass.
- New finding, from deep glass seen along the street: a reflected ray travels on along the street at the same angle, so it must get out of the reveal before it hits the far jamb.
  - Upper sash, glass 142 mm back: some of the visible glass can reflect the street only above about 18.5° from the wall.
  - Lower sash, glass 190 mm back: only above about 24°.
  - Below those angles, all the glass you can see reflects the far reveal: the white lining and the brick return, at 25 to 60%.
  - The table below uses the kit's numbers (WINDOWS-GRAZING note) and an 850 mm opening, worked in plan [I]. Widths are measured on the glass.

| Angle | Upper glass visible | Of which shows the street | Lower glass visible | Of which shows the street |
|---|---|---|---|---|
| 12° | 0.11 m | none | none | none |
| 16° | 0.28 m | none | 0.11 m | none |
| 20° | 0.38 m | 0.07 m | 0.25 m | none |
| 30° | 0.53 m | 0.36 m | 0.45 m | 0.19 m |

So "sky in the glass" (his 3 October bar) is physically possible only on panes seen at more than about 20 to 25° from the wall. Lower down, real glass reads as a darker band carrying a faint mirror image of the lining beside it.

**Where reflections come from, by engine.**
- Unity HDRP's order: screen-space hit first, then a reflection probe's cubemap, then the sky, then black [SHOWN].
- A probe is only exact at its capture point. HDRP corrects this with a box "proxy volume" that reprojects the capture. It notes that a box can lose resolution and get angles wrong at its edges [SHOWN].
- Godot's "box projection" does the same: "a small performance cost, but the quality increase is often worth it" [SHOWN].
- Unreal's software Lumen works in a similar order:
  - It traces the screen first, then each mesh's distance field for the first 1.8 to 2 m, then the coarse global distance field and the surface cache [NOTE, CLOSE-RANGE-ROUTES, 7 Oct; SS today].
  - It sends a missed ray to the sky light [NOTE, WINDOWS-OTHER-DIRECTION].
  - Reflection captures are bypassed under Lumen reflections [NOTE].
  - Epic: "Hardware Ray Tracing is the only way to achieve high quality mirror reflections" [NOTE, shop-glass NOTE, 1 Oct].

**Lumen and thin or recessed geometry.**
- Distance fields use 5 cm voxels. They are capped at 128 voxels a side, or 256 when Distance Field Resolution Scale is above 1 (DistanceFieldAtlas.cpp:68-80) [NOTE].
- Epic: large single meshes get "a poor distance field representation" [NOTE, 4 Oct], and thin surfaces may not be well represented [SS].
- Lumen places 12 cards on a mesh by default (Max Lumen Mesh Cards). Areas without cards "will not bounce light and will appear black in reflections". The fix is more cards or splitting the mesh [NOTE; SS today].
- Lumen multiplies a material's AO into its sky and bounce light (LumenScreenProbeGather.usf ~1347-1352) [NOTE].
- Lumen traces reflections only below roughness 0.4 by default [NOTE].
- Nanite takes only opaque and masked materials [NOTE]. It does not change distance fields or cards [I].

**Small-scale shade is authored, not simulated.**
- Godillon's London: "trim sheet material and vertex painting are doing all the heavy lifting" [NOTE, 80.lv 2024].
- Hitman uses edge decals [NOTE].
- Filament keeps micro-occlusion in the base colour: "devoid of lighting information, except for micro-occlusion" [SHOWN].
- Specular occlusion from AO (Lagarde's formula) increases occlusion at grazing angles on smooth surfaces [SHOWN, Filament].

**Glass in shipped games.** Little was reachable today:
- Ray-traced window reflections: Spider-Man: Miles Morales on PC [NOTE, NVIDIA 2022, CLAIMED]; Watch Dogs: Legion's shops [NOTE, PCGamesN 2019, CLAIMED].
- Planar reflections: Hitman 3's big windows [NOTE, PCGH 2022].
- Very glossy, dark glass with a slight normal wobble: Dishonored [NOTE, 80.lv 2018].
- City Sample: rooms by box projection with parallax [NOTE, Epic forum 2023]; reflections "rely heavily" on ray tracing [SS, GamingBolt].
- Kingdom Come: Deliverance II and Mafia: Definitive Edition: no glass method found.

The pattern without ray tracing: a captured or fake reflection added by Fresnel, a dark interior, and authored dark lines [I].

**Paint and glass values.**
- White joinery albedo:
  - Filament puts dielectrics at sRGB 50 to 240; 240 is 0.87 linear [SHOWN].
  - Earlier notes give BS 4800 00 E 55 white, LRV about 88 [NOTE, S]; whiteboard 0.87 and paper 0.79 to 0.88 [NOTE].
  - So weathered 1990 gloss white is about 0.72 to 0.80 linear [I]. Ours is 0.82/0.81/0.78 at roughness 0.42 (terrace-front.py:224).
- Glass: Specular 1 (F0 0.08, standing in for both faces), roughness 0.02 to 0.04 [NOTE].

## 3. Why ours read as boards and slits (ranked)

**1. The pane is a lit, pale card, not glass over a dark room.**
- Shown in the code [NOTE, WINDOWS-GRAZING; code read today]:
  - Each pane is an opaque net card: lace × net_lace 0.8, roughness 0.04 (terrace-front.py NET_PANE_ROUGHNESS), Specular 0.5 (F0 0.04).
  - The lace's alpha is not wired, so the holes are light grey (0.35 linear), not a dark room.
  - The card is not emissive by day (net_day_gain 0.0, unreal-look.json).
- Seen in the gate:
  - Reverse view: pane 157-175 against paint 178-205.
  - Hook view, about 16° from the wall: lace 120-134 beside white 151-180.
  - The reviewers: "one even grey… nothing behind it".
- Inference [I]:
  - A diffuse card at about 0.4 average albedo adds light that real glass does not have.
  - From below, the reflected sky (at full strength since 8 October) is then added on top, so the pane reaches the paint's brightness: a slab.
  - Real glass at 16° lets through 62% of a dark room (about 0.03) plus whatever nets there are.
  - The card also closes the back of the box with a bright surface. Lumen bounces light from it back onto the linings, where a real window's room returns almost none.

**2. The box is lit flat and has no dark lines.**
- Shown:
  - Photograph 9: lining 220-250, inside corner 105-125, track 150-180. Ours: 153-180 with no corner line [NOTE, WINDOWS-GRAZING].
  - In the photograph 3 preview (overcast) I read the frame at 225-236, the panes at 205-215 and the frame-to-glass lines at 40-120 [SHOWN, 1200 px preview, approximate].
- Inference [I]:
  - Real panes are only about 0.9 of the frame. What separates them is the dark lines (about 0.2 to 0.5 of the frame) and the room seen in some panes.
  - Ours has the brightness steps but not the lines.
  - The third try's AO darkened only channels under a pixel wide. At the hook camera a pixel is 5.9 mm at 10 m and 11.8 mm at 20 m (46° vertical field over 1440 rows).
  - The room-scale shade was deliberately left to Lumen (a 6 cm reach). Lumen cannot give it:
    - All the joinery is one street-long mesh, so its distance field has voxels about 14 cm across (36 m / 256), larger than the 114 mm reveal [NOTE, I].
    - 12 cards cannot cover hundreds of members [NOTE, SS].
    - And the pale card bounces light back in (cause 1).

**3. Geometry: at the street's angles there is almost no glass to see.**
- Shown: under 13.6° no lower pane shows, under 10.3° no pane at all, under 7.6° only brick [NOTE, WINDOWS-GRAZING, from the kit's numbers].
- From the scene file, both day cameras stand about 2.9 m off the near facade's line [I, vignette-scene.json].
  - Reverse view: the left row's windows more than about 10 m away are under 16°; those more than about 21 m away are under 8°.
  - Hook view: the near-left terrace runs from about 26° down to 7°.
- So the slits and the bricked-up far windows are partly true to life. What is wrong is that the far reveal reads flush:
  - its brick return is lit like the wall face;
  - no shade under the head;
  - no white lining edge strong enough to see [I].
- This cause ranks third because real windows at these angles read as recesses, not as bricked-up holes.

**4. Upper panes reflect no shapes.**
- Shown: the reflection of the opposite eaves is mostly off-screen and falls to the global distance field and surface cache [NOTE]. Uncovered areas "appear black in reflections" [NOTE, SS].
- Inference [I]: the pane gets a soft wash of sky with no roofline edge in it. That is the "white slab" seen from below in the reverse view.

**5. Possible: the paint's sheen is never traced.**
- Paint at roughness 0.42 is just above Lumen's trace limit of 0.4 [NOTE].
- Inference [I], untested: its sheen may come from blurred screen-probe light that is not occluded inside the box, which would whiten the lining evenly.

## 4. The fix that fits LEDGER, cheapest first

Try these on the hook view's near-left terrace (its first two houses) and on Mickey's row in the reverse view. Spread nothing further before the gate passes.

**Step 0. Measure before changing (an hour).**
- On the hook and reverse frames, take the Lumen Scene, Surface Cache (pink = no card), Mesh Distance Fields and Lighting Only views.
- Take one frame with `r.Lumen.Reflections.ScreenTraces 0`.
- Record the numbers in section 5. Cost: nothing.

**Step 1. The pane becomes glass over a dark room (a few hours).** On the net cards only:
- Base colour = lerp(room 0.03, lace × 0.6, the lace's alpha), with the alpha wired.
- Specular 1.0 (F0 0.08).
- Roughness 0.03.
- Day emissive stays 0.
- Expected [I]:
  - Hook view: the visible pane falls well below the lining and carries a faint mirror of it. That is a recessed pane, not a board.
  - Reverse view: the panes show the reflected sky by Fresnel, dark where the lace has holes.
  - The box gets less bounced light, so the linings darken towards the glass.
- Frame cost: none [I].
- This is also the earlier note's fallback [NOTE].

**Step 2. Shade the box and draw its lines (half a day to a day).**
- First check: after step 1, if the lining band's darkest-to-brightest ratio is still above 0.8 in Lighting Only, Lumen is not shading the box. Then bake.
- Bake the window's sky visibility with the brick reveal around it and the room as a black void behind the glass. Use a 1 m reach.
- Put it into the base colour (vertex colour multiplying the paint), not the AO pin:
  - linings 1.0 at the brick edge, falling to about 0.6 at the glass;
  - track about 0.5;
  - inside corners about 0.3.
- Widen the dark lines to at least one pixel at 10 m, about 6 mm:
  - the sash-to-bead gaps;
  - a putty and shadow line round each pane at × 0.35;
  - the underside of the meeting rail.
- Put the same shade on the brick returns of the reveal (0.6 to 0.8) and under the head. That shade is in the wall mesh, not the kit.
- Keep the paint at albedo 0.78 to 0.80, roughness 0.40. Try 0.35 once, to see whether a traced sheen helps (cause 5).
- Expected: the photograph-9 steps across the band in the hook view; the far windows in the reverse view read as recesses.
- Frame cost: none (vertex colour is already exported) [I].
- Base colour holds micro-occlusion in Filament's model [SHOWN]. This is "grime is the strategy" (D53).

**Step 3. Upper panes reflect the street (about a day).**
- Capture one cube of the street per facade side at window height. Capture it at load and at each change of light, never every frame. The glass capture already caused the BELOW-30 regression (NOW.md).
- Box-project it onto the opposite facade's plane [SHOWN, HDRP and Godot method].
- Add it to the pane as emissive × Fresnel, as the shop glass's cube already does (glass_cube_specular 0.1).
- Only where the reflected ray gets out of the reveal: a few instructions, from the pane's place in the opening, the glass depth (142 or 190 mm) and the 850 mm width.
- Where the ray does not get out, keep Lumen's own reflection at Specular 1, because screen traces see the reveal beside the pane.
- Expected: in the reverse view each upper pane shows a bright sky top cut by a darker roofline band that moves as the camera moves. The hook view barely changes, since its panes are under 24°.
- Cost [I]:
  - one cube sample per pane pixel, well under 0.1 ms on the RX 6700 (unmeasured);
  - a 512 cube in RGBA16F with mips is about 17 MB, 34 MB for two sides;
  - capture time only at light changes.

**Step 4. Only if steps 1-3 leave the box flat: windows as their own meshes (a day).**
- Make the kit instanced per window, with Distance Field Resolution Scale 2 and its own cards.
- Then each window has a distance field at 5 cm voxels and real card coverage.
- Cost: about 8 times that mesh's distance-field memory, plus some surface-cache updates. Measure it with stat gpu [NOTE, I].

**Step 5. A control frame, not shipped.**
- One frame with hardware Lumen (`r.RayTracing.Enable 1`, `r.Lumen.HardwareRayTracing 1`) as the reference for steps 2-3.
- The ray-tracing scene alone cost 3.6 ms at 1280×720 (DefaultEngine.ini note) [NOTE]. That is too much for 60 fps on RDNA 2.

**If the far windows still read bricked-up after step 2:**
- That is physics at under 8°.
- The remaining lever is how far back the frame is set: Ellis 114 mm, the 1709 Act 102 mm, a modern maker 80 mm (lab SOURCES.md).
- His ruling is that the photographs win. Photographs 3, 4 and 9 show shallower replacement frames, which suits 1990.
- It is a builder's choice, recorded in DECISIONS.md.

## 5. How to check each step from the game's camera

Measure on 2560×1440 day frames from the game's own camera. Use sRGB luma (0.2126 R + 0.7152 G + 0.0722 B).
- Hook view: the near-left terrace's first two ground-floor windows. Measure across the lower sash's band.
- Reverse view: the left row's upper windows 1-3, and windows 6-10 for the far case.

Per window, record:
- L, the lining's 90th percentile;
- D, the darkest line's 5th percentile;
- T, the track;
- P, the pane median and its 5-95% spread;
- W, the brick beside it.

| Check | Now | Target (source) |
|---|---|---|
| D/L, dark lines | about 0.85 (153-180, flat) | 0.6 or less (photograph 9: 105-125 against 220-250; photograph 3: 40-120 against about 230) |
| T/L, track | not distinct | 0.65-0.85 (photograph 9: 150-180) |
| P/L, pane | 0.77 (hook), 0.87 (reverse) | 0.6-0.9, and a pane spread of at least 20 levels (photograph 3 panes 205-215 with dark room patches) [I] |
| Reverse upper panes | even | at least 2 of 3 show a horizontal edge with a step of at least 30 levels; it moves when the camera moves 1 m [I] |
| Far windows 6-10 | brick | a white lining edge at least 1 px wide and at least 1.5 W; the reveal return 0.8 W or less [I] |
| Mickey's front faces | last good | within 3 levels (as the earlier test) |
| Motion | | over a 2 s pan, a line pixel varies by 10 levels or less (shimmer) [I] |
| Cost | | stat gpu: steps 1-3 add 0.3 ms or less in all |

Also take one frame at 100% screen percentage against the shipped percentage. If the lines appear only at 100%, they need widening, not shading [I]. Then send a fresh reviewer per view, with photographs 3, 6 and 9 and the Hook sheet.

## 6. To check on the PC (installed 5.8.2 source, file and line)

- Does software Lumen's opaque reflection apply the material AO, or any specular occlusion? Likely places: DiffuseIndirectComposite.usf, LumenReflections.cpp, ReflectionEnvironmentShared.ush. Search for "SpecularOcclusion" [I].
- The reflection trace's mesh-SDF distance, and whether reflections use the 1.8 m GI value: LumenReflectionTracing.cpp. Also `r.Lumen.Reflections.MaxRoughnessToTrace` (0.4 per the note) and how rough specular is filled above it.
- The screen-trace thickness at grazing angles: `r.Lumen.Reflections.HierarchicalScreenTraces.*` (names to confirm).
- The card count and placement on the joinery mesh: `r.Lumen.Visualize.CardPlacement 1` [SS]; Max Lumen Mesh Cards (12 [NOTE]).
- `r.DistanceFields.MaxPerMeshResolution` and `r.DistanceFields.DefaultVoxelDensity` defaults: DistanceFieldAtlas.cpp.
- `r.Lumen.ScreenProbeGather.ShortRangeAO.*` defaults and its reach (DefaultScalability.ini sets some).
- The shipped screen percentage and upscaler (the TitleScreen ladder).
- Whether net-card rows take AlbedoGrade: VignetteShot.cpp ~7932-7950 sets only emissive.

## 7. Sources

Reached today (8 October 2026), [SHOWN]:
- Filament docs, Filament.md.html (main branch; the document is undated): Fresnel, specular occlusion, base-colour range. https://raw.githubusercontent.com/google/filament/main/docs/Filament.md.html
- Unity HDRP docs, master branch: reflection-understand.md; how-hdrp-calculates-color-for-reflection-and-refraction.md; Ambient-Occlusion.md. Under https://raw.githubusercontent.com/Unity-Technologies/Graphics/master/Packages/com.unity.render-pipelines.high-definition/Documentation~/
- Godot docs, master branch: reflection_probes.rst. https://raw.githubusercontent.com/godotengine/godot-docs/master/tutorials/3d/global_illumination/reflection_probes.rst

Read in the repository today; their own sources were read on the PC on their dates (the [NOTE] items):
- The audits: GATE-2.md, GATE-HOOK-1.md, REVIEW-PHOTOGRAPHS.md.
- The research: aaa-street's WINDOWS-GRAZING (8 Oct), WINDOWS-FACADES and WINDOWS-OTHER-DIRECTION (4 Oct); shop-glass-reflections' NOTE.md (1 Oct) and CLOSE-RANGE-ROUTES (7 Oct); shop-window-interiors' CLOSE-RANGE (3 Oct); shopfronts' FRONTAGE (6 Oct, nothing on glass).
- The lab's sash target, NOTES.md and SOURCES.md (origin/lab); art/sash-window/TARGET-NOTES.md.
- The config and code: DefaultEngine.ini, DefaultScalability.ini, unreal-look.json, vignette-scene.json, terrace-front.py (224, 2795-2805, 3195-3265), make_base_material.py (~3740-3955), VignetteShot.cpp (~7166, ~7932-7950).
- Previews: the lab's photographs 3, 6 and 9; the hook and reverse day views of 8 Oct, evening.

Search summaries only, today [SS], leads not evidence (none of these pages was reached):
- Epic, Lumen Technical Details: https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-technical-details-in-unreal-engine
- Polycount, City Sample windows (guesses): https://polycount.com/discussion/comment/2763988
- GamingBolt, Matrix Awakens analysis: https://gamingbolt.com/the-matrix-awakens-technical-analysis-a-look-into-the-future-of-gaming
- GDC Vault, Spider-Man postmortem (2019): https://gdcvault.com/play/1026496

To read from the PC, or once the network opens:
- Epic's Lumen GI and Reflections, Mesh Distance Fields and Lumen Performance Guide.
- NVIDIA's UE5 Raytracing Guideline v5.4 (PDF).
- Lagarde and de Rousiers, "Moving Frostbite to PBR" (2014); Lagarde, parallax-corrected cubemaps (2012); Jimenez et al., GTAO and specular occlusion (2016).
- City Sample's own window materials.
- Kingdom Come: Deliverance II's and Mafia: Definitive Edition's glass.
- An overcast photograph of an original deep box sash seen at under 20°.
