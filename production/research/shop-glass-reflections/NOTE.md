# Shop-window glass that reflects the street by day (UE 5.8, software Lumen)

1 October 2026, research helper, about thirty minutes. **Question:** how do games make shop glass that clearly reflects the street by day while a lit interior shows through, and why do our two attempts give only "a faint grey veil"? "Mine" marks the helper's own reasoning.

## In brief

- **Two faults, both confirmed.** Unreal's Translucent blend multiplies the glass's whole colour, reflection included, by Opacity: at 0.25, a 4% reflection becomes 1%. And the room is as bright as the pavement, so even a real pane's 8% reflection of the terrace vanishes against it.
- **The fix.** The **Thin Translucent** shading model (reflection not scaled by opacity, still lit by Lumen's front layer), Opacity used only for dirt, and the room dimmed by day to about a tenth of the pavement.

## 1. Why the attempts failed (installed 5.8 engine source)

- **Translucent multiplies by Opacity.** It blends SourceAlpha / InverseSourceAlpha (TranslucentRendering.cpp), and the base pass adds the reflection into the colour that Opacity then scales (BasePassPixelShader.usf, ForwardLightingCommon.ush). A 2022 forum answer says the same: "lowering opacity reduces reflection visibility".
- **Front-layer reflections were probably already working.** The project setting sets the post-process default (SceneView.cpp). The material qualifies: Translucent, a Surface lighting mode, and "Allow Front Layer Translucency" on by default (Material.cpp). The reflection was computed, then cut to a quarter.
- **Thin Translucent keeps the reflection whole** (ThinTranslucentCommon.ush). It adds (diffuse + emissive) × Opacity plus the unscaled reflection. It multiplies what lies behind by Transmittance Color × (1 − Fresnel)², so the room dims where the reflection grows.
  - Its Transmittance Color **defaults to 0.5 grey if unconnected**, so connect it.
- **Ruled out:** AlphaComposite (without Substrate it is excluded from Lumen's translucent reflection path, MaterialTemplate.ush, so it reflects only the sky); the Single Layer Water trick (no Lumen reflections; forum, 2022); ray-traced translucency (hardware only). The project is not on Substrate, and does not need it.

## 2. Software Lumen's limit

- Epic: "Hardware Ray Tracing is the only way to achieve high quality mirror reflections". Software Lumen traces the screen first, then distance fields and the surface cache.
- The opposite terrace is usually behind the camera, so its reflection will be soft but rightly shaped and coloured. Mine: at 8%, under dirt and a slight ripple, that is probably enough. Test it.
- **Fallbacks, cheapest first:** (a) a static cubemap captured at each shop front, added as emissive × Fresnel: sharp and nearly free, but frozen (no passers-by), with day and night versions; (b) one planar reflection for the facade plane, which renders the scene again (1.7 to 23 ms in Epic's examples); (c) hardware Lumen, compiled in but off, measured at 3.6 ms here.

## 3. Brightness balance

- **Glass** reflects 4% per surface, 8% per pane, rising towards a mirror at grazing angles.
- **Light levels:** an overcast day is 1,000 lux; daylight out of direct sun is 10,000 to 25,000 lux; a shop is 300 to 500 lux. An overcast sky's zenith is three times as bright as its horizon (CIE).
- **Worked numbers (mine), with the pavement = 1:**
  - The terrace is about 0.5 and the low sky about 2. Through an 8% pane they reflect at 0.04 and 0.16.
  - **Room at 1 (now):** the terrace reflection is 4% of the room: invisible, as the reviewer saw.
  - **Room at 0.1:** it is 40% of the room, plainly readable. The sky glares along the top of the pane, as in photographs; the room reads below it and where the reflection is dark (the skip, the eaves' shadow).
  - Physically the ratio would be 1:20 to 1:40. About **1:8 to 1:10** keeps the interior "clearly readable".
- The daylit display bed by the glass will read brighter than the deep room, as in photographs.

## 4. Dirt

- Dirt makes glass read as a surface: a grunge mask raises roughness, opacity and base colour (Overdraw, 2019). Dishonored's windows are very glossy, with dark albedo and slight normal variation wobbling the reflection (80.lv, 2018).
- For 1990 (mine): a splash band along the bottom 30 to 40 cm, grime at the frame edges, faint wipe arcs; 10 to 25% coverage.

## 5. What others do

- **City Sample:** interior-mapped building rooms (State of Unreal 2022 talk, known only from a search summary). No source we could open describes its shop glass.
- **Spider-Man and Miles Morales:** interior-mapped rooms; ray-traced window reflections on PS5 and PC (NVIDIA, 2022).
- **Cyberpunk 2077, Hitman, GTA:** no reliable source.
- **Mine:** upper-floor windows can be one opaque material (emissive = interior × (1 − Fresnel), with Lumen's opaque reflection on top). Shops need thin translucent glass in front of the real display.

## 6. Recipe (M_LedgerGlass, UE 5.8, software Lumen)

1. **Material settings:** Blend Mode Translucent; Shading Model **Thin Translucent**; Lighting Mode Surface ForwardShading; Allow Front Layer Translucency on. Keep EnableForProject=True, and check that no post-process volume turns High Quality Translucency Reflections off.
2. **Thin Translucent Material Output node:** Transmittance Color (0.88, 0.92, 0.90), connected; Surface Coverage 1.
3. **Opacity** = DirtMask × 0.6, so clean glass is 0.
4. **Base Color** (0.18, 0.16, 0.13): the dirt, seen only where Opacity > 0.
5. **Specular 1** (F0 ≈ 0.08, standing in for both faces of the pane); Metallic 0.
6. **Roughness** = lerp(0.03, 0.5, DirtMask).
7. **Normal:** a broad, very weak ripple (strength 0.01 to 0.02).
8. **Painted lettering** goes inside this material, never as a separate translucent card. Only the frontmost translucent layer gets Lumen's reflections.
9. **The room card by day:** lower its emissive until the room averages 1/8 to 1/10 of the daylit pavement, measured through the game's camera and exposure. The night state is separate.

**Main risk.** The off-screen terrace's reflection may look too soft: then add fallback (a), lowering Specular so it is not doubled. Measure the front layer's frame cost.

**One-frame test.** The game camera on the pavement, overcast, 2560 × 1440, the same shot three times:
- **A:** as it is now.
- **B:** the new glass, room emissive 0. The pane must be a dark mirror showing terrace, skip and sky; if not, compare `r.Lumen.TranslucencyReflections.FrontLayer.Allow` 0 and 1.
- **C:** the new glass with the room at 1/10.
- **Pass:** in C, the skip, the roofline and the sky band can be named in the pane, and the room reads below them.

## Sources (read 1 October 2026)

- UE 5.8 engine source (local install), the files named in section 1
- Lumen GI and Reflections (5.8): https://dev.epicgames.com/documentation/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine
- Lumen Technical Details (5.8): https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-technical-details-in-unreal-engine
- Lit Translucency (5.8): https://dev.epicgames.com/documentation/unreal-engine/lit-translucency-in-unreal-engine
- Shading Models (5.8): https://dev.epicgames.com/documentation/en-us/unreal-engine/shading-models-in-unreal-engine
- Substrate (5.8): https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-substrate-materials-in-unreal-engine
- Planar Reflections (5.8): https://dev.epicgames.com/documentation/en-us/unreal-engine/planar-reflections-in-unreal-engine
- Forum, Sept to Dec 2022: https://forums.unrealengine.com/t/strong-reflection-on-translucent-materials/650210
- Forum, Feb 2025: https://forums.unrealengine.com/t/ue5-translucency-reflections-limitation-or-bug/2316417
- Forum, May 2022: https://forums.unrealengine.com/t/solution-to-blurry-reflections-on-translucency/556987
- Forum, Jan 2023: https://forums.unrealengine.com/t/city-sample-how-are-the-holographic-building-windows-made/748544
- https://en.wikipedia.org/wiki/Fresnel_equations ; https://en.wikipedia.org/wiki/Lux
- CIE sky standard, ESIM 2002: https://publications.ibpsa.org/proceedings/esim/2002/papers/esim2002_o2.pdf
- Overdraw, 25 March 2019: https://www.overdraw.xyz/blog/2019/3/24/a-practical-approach-to-creating-glass-materials-for-physically-based-rendering
- 80.lv, 10 May 2018: https://80.lv/articles/dishonored-environment-art-shaders
- NVIDIA, Nov 2022: https://www.nvidia.com/en-gb/geforce/news/spider-man-miles-morales-pc-geforce-rtx-dlss-ray-tracing-out-now
- Talk devlog, 5 April 2022: https://johnlogostini.itch.io/the-matrix-awakens/devlog/726015/the-matrix-awakens-creating-a-world-state-of-unreal-2022
