# Upper windows: the other direction (research, 4 October 2026)

Extends WINDOWS-FACADES-2026-10-04.md and shop-glass-reflections/NOTE.md. O opened, S search summary, I inference.

## Likely causes, ranked

1. **The street is lit by a sky at 41% of the one it shows; the brick gain hides it.** Lumen sends a missed reflection ray to the sky light's cubemap (ApplySkylightToTraceResult) [3 O]; the real-time capture renders only the Is Sky dome when one exists [3 O, 4 O]; a sky light is pixel × intensity [5 O]. Day: dome 0.7 × 13, sky light 0.7 × 0.58 = 0.41 of it (I, unreal-look.json, vignette-pieces.json). 1/0.41 = 2.44, close to the brick's ×2.7 (I). Albedo stops at 1, so paint lands near 3× the wall, not the concept's 7.4× (sRGB decoded, tonemap ignored, I); a pane reflects 4–8% of a sky already cut to 41%.
2. **Merged street meshes defeat software Lumen.** Distance fields: 5 cm voxels, capped near 128 a side (256 with resolution scale above 1) [3 O], so a 60 m joinery mesh gets ~47 cm voxels against a 100 mm recess; 12 Lumen cards per mesh by default [3 O]. Epic: large single meshes get "a poor distance field representation"; uncached areas "appear black in reflections" [6 O]. Pane rays likely hit the wall's own blob (I).
3. **Geometry.** A ray off an opposite upper window meets the camera-side facade at h_w + (h_w − h_cam)·W/D, whatever the distance down the street (I): about 8.5–10 m, so eaves, roofs and chimneys for most panes, sky in the top ones. At grazing angles the 100 mm reveal takes more (I).
4. **The lace is the pane.** A bright opaque base colour outshines 4–8% × sky near normal incidence (I).

Discarded: the ray clamp (40, pre-exposed) [3 O]; Lower Hemisphere black, which upward rays miss [4 O, I]; reflection captures, bypassed under Lumen [3, I].

## Methods, ranked by fit, then cost

1. **Measure first.** Chrome and 18% grey spheres [7 S] and a mirror plane at a window's angle; Lumen Reflections, Surface Cache and Mesh Distance Field views; screen traces 0/1. An hour.
2. **One sky.** Sky light gain 0.58 → ~1.43, so the light equals the dome; brick gains ÷2.44 (near brick's 0.12–0.26 [1 O, 2 O]); paint 0.8; exposure unchanged. Frames should near 200 (I). Manual exposure later (formula [8 O]; overcast EV 12–13 [9 O]). Cost: road and flags brighten too; half a day retuning (I).
3. **Fake sky by Fresnel in the window material.** Emissive += Fresnel × the sky photograph along the reflected vector, a slate band below a roofline elevation, tilt per sash, Specular lowered. The usual facade trick [10 S, 11 S]. One sample; frozen, fine upstairs (I). An afternoon.
4. **Windows as instanced assets**: each its own distance field and cards [3 O, 6 O], resolution scale 2. A day (I).
5. **Hardware Lumen reflections**: "the only way to achieve high quality mirror reflections" [6 O]; 3.6 ms [shop note]. A control frame.
6. Planar reflections, 1.7–23 ms [shop note]: rejected.

## Authored windows instead of boxes

Studios build a grid kit with real-scale UVs, trims and vertex-painted dirt [12 O, 13 O], edges faked by 45° bevel normals on a trim sheet [14 S]. For Quay Street (I): one box sash modelled in Blender, mouldings swept along the frame, horns, sashes ~45 mm apart; sill with drip; arch head with voussoir UVs [prior note]; one joinery trim sheet; glass and nets separate; Leaking decals. About 2–3 days for three sashes, sill, two arch heads and the trim (I). Free: Poly Haven has roller shutters, no sashes [15 S]; ambientCG's window facades are modern towers [16 O]; Fab's "Victorian Street" [17 S], licence unchecked.

## What to do next, in order

1. Spheres and mirror plane in the hook frame; measure seen sky, reflected sky, brick, paint.
2. One sky; real albedos; remeasure frames to wall (target ~7×), panes (~4×).
3. One authored sash, sill and arch head as instances; check the Lumen views.
4. Its glass: fake sky by Fresnel, roofline band, nets behind; hardware Lumen as control.
5. That window to Jafar as the sample; nothing multiplied before his yes.

## Unreached

City Sample's window material; the Ultimate Trim slides; Poly Haven's full list; KCD2's windows.

## Sources

1 Epic, Physically Based Materials. 2 physicallybased.info. 3 UE 5.8 source (Lumen reflections, real-time capture, mesh distance fields, EngineTypes.h). 4 Epic, Sky Lights. 5 Epic, Physical Lighting Units. 6 Epic, Lumen Technical Details. 7 CAVE Academy. 8 Epic, Auto Exposure. 9 Wikipedia, Exposure value. 10 Unreal forum, City Sample windows. 11 antondoe, 2018. 12 Vinci, 80.lv, 2017. 13 Andrews, 80.lv, 2018. 14 Olsen, GDC 2015. 15 Poly Haven. 16 ambientCG API. 17 Fab.
