# Wet road methods (research, 3 October 2026)

O = opened, S = search summary only, I = inference; [n] = sources below.

## Why both tries failed

- **Mirror road:** a missing ray samples the sky light's cubemap at roughness 0 [1 O]; an even overcast capture makes an even sheet, and the centre-line step is the true mirror boundary, unbroken (I).
- **0.16, full stone normal:** at grazing view a ray turns by twice the normal's tilt, so the image scatters (I); water filling the cavities flattens a wet road [2 O].

## Methods, ranked by fit and cost

1. **Water level in the road material (Lagarde)**, about 0 ms (I).
   - Albedo darkened (asphalt ×0.68); gloss raised, deliberately damped [2 O].
   - Normal blended toward the vertex normal as the water rises, fully flat in puddles [2 O, 4 O]. A heightmap marks where water collects (black = holes) [3 O].
   - Result: near-mirror cavities between rougher stone tops; many small highlights, not a sheet (I).
   - Keep both out of Lumen's weak band, 0.2 to 0.39, which flickers or blurs; about 0.1 and 0.4 up resolve well [5 O]. Above 0.4 no ray is traced [14 O].
   - Risk: mips average the two into that band far off (I); measure the far road.
2. **Large-scale variation**, about 0 ms (I).
   - Wet zones are placed by artists: vertex colour plus heightmap with separate flood levels [3 O]; in UE5 streets vertex paint [8 O] or world noise [9 S]; City Sample's road has one overall wetness, users add decals [10 S].
   - Here (I): world noise at 2 to 10 m on the water level; two wheel paths per lane wetter and smoother; the kerb channel wettest; the crown slightly drier. This breaks the sky sheet and frays the centre-line step.
3. **Give the mirrored sky structure**, about 0 ms if static (I).
   - Sky light cubemap defaults to 128; real-time capture costs about 1.47 ms for a full 128 capture, at most 0.2 ms time-sliced over 9 frames [6 O].
   - A specified cubemap from a CC0 overcast HDRI (Poly Haven, allowed; used on a UE5 rainy street [11 O]) puts cloud structure in the near lane with no per-frame capture (I). Match the visible sky.
4. **Streaks come free once the road is not a mirror**, 0 ms.
   - Lumen draws each ray from GGX's visible normals, anisotropy included, and reweights neighbours by the BRDF [1 O]: vertical elongation at grazing view (I), as Frostbite's stochastic SSR gave [12 O abstract; elongation 12 S].
   - Stronger hack: anisotropy along the road (r.AnisotropicMaterials, off by default, adds a pass) [1 O]; cost unmeasured.
5. **Puddles**: water's F0 0.02 = Specular 0.25, flat normal, full gloss [2 O, 3 O]. Single Layer Water gets mirror-forced Lumen reflections [7 O] for a hero puddle; cost unmeasured.
6. **Lumen settings** [1 O unless marked]:
   - SmoothBias (default 0): a smoothstep toward mirror below its value, reflections only, on every surface; too strong on rough ones [5 O]. No extra tracing (I).
   - Screen traces and their helpers are on by default; off-screen hits use the "splotchy" surface cache, which Lumen Scene Quality and Detail raise at cost [13 O].
   - Epic traces at full resolution, 5 reconstruction samples (High: quarter, 3); each lower level costs about half the one above [14 O].
   - Reflection captures feed only hardware hit lighting; planar reflections are skipped when Lumen composes specular (I). Neither is a route.
7. **Hardware ray tracing**: Far Cry 6 sent smooth pixels (puddles, chrome) to "high-precision" hardware traces [15 O]; here the ray-tracing scene alone cost about 3.6 ms at 1280×720 (project config), over budget.

## What to try, in order

1. Road: water level from the asphalt's height. Cavities 0.05 to 0.08, flat normal; tops 0.4 to 0.45, normal at 30 to 50%; albedo as now (I). One frame.
2. The large masks. One frame; check the centre line.
3. Sky light from a CC0 overcast HDRI, specified cubemap, 512. One frame of the near lane.
4. That frame with SmoothBias 0.15, after 16+ warm-up frames (history is 12 [1 O]); keep it only if glass and cars hold.
5. Puddles moved to where they mirror contrast.
6. Only if streaks still lack: anisotropy along the road. Measure each step (stat gpu) against 2.5 ms.

## Sources (opened 3 October 2026 unless marked)

1. UE 5.8 as installed: config, Lumen source and shaders. O
2. Lagarde, "Physically based wet surfaces", 14 April 2013. O
3. Lagarde, "Dynamic rain and its effects", 3 January 2013. O
4. fxguide, "Making wet environments", 6 June 2013. O
5. Epic forums, "Rough Lumen reflections cheat sheet", 2023. O
6. Epic, Sky Lights, UE 5.8. O
7. Epic, Lumen GI and Reflections, UE 5.8. O
8. 80.lv, Kelly, rainy Japanese street, 5 January 2023. O
9. 80.lv, Mansour, foggy Japanese street, 2025. S
10. Epic forums, City Sample asphalt puddles. S
11. 80.lv, Tanoli, Faisal Avenue, 16 October 2025. O
12. Stachowiak, "Stochastic Screen-Space Reflections", SIGGRAPH 2015. O (abstract)
13. Epic, Lumen Technical Details, UE 5.8. O
14. Epic, Lumen Performance Guide, UE 5.8. O
15. Ubisoft Toronto, Far Cry 6 at GDC, 23 March 2022. O

**Unreached:** Karis's 2013 notes (PDF unreadable); Stachowiak's slides (site down); the Far Cry 6 video; Toy Shop (2006); tyre-track wetness in shipped games.
