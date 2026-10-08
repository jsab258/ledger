# Why the brick greyed under the true sky (research, 8 October 2026)

D = read or measured here; S = search summary; I = inference or model.

## Measured (hook, day; sRGB, HSV saturation of the mean, hue)

| Region | This morning | Now | Sheet |
|---|---|---|---|
| Mickey's wall (sky_regions box) | 121/68/46, 0.62, 16° | 120/73/58, 0.51, 13° | 91/53/40, 0.56, 15° |
| Parade bay by Fresh Fish | 148/91/69, 0.53, 16° | 152/104/91, 0.40, 12° | parade 116/75/61, 0.48, 14° |
| Fresh Fish fascia | 91/71/72, 0.22 | 128/110/112, 0.14, −6° | |

The sky reads 246/247/248 in both: exposure and tone curve unchanged. Red fell one level, blue rose twelve; a fixed curve cannot, so the wall's light changed (D; fog starts beyond, at 75 m).

## Why

1. Sky light leaves brick by two paths: diffuse = base colour × light; sheen = EnvBRDF × light, never multiplied by base colour (DiffuseIndirectComposite.usf:640–651; F0 0.04, ShadingCommon.ush:122–125). At roughness 0.93 Lumen bends the sheen's direction 83% onto the normal (ReflectionEnvironmentShared.ush:125–129; LumenScreenProbeGather.usf:1303–1308), so it takes the diffuse's light, at 0.03–0.05 of it at these grazing views (split-sum, my integration) (D).
2. This morning: light ×0.41, base colour ×2.74/2.81/2.58, so the sheen ran at 41%. Solving both frames per channel through an inverse of the filmic path (ported from PostProcessCombineLUTs.usf:165–188, 369–394, TonemapCommon.ush:110–224, Scene.cpp:403–449; grey 0.18 returns 118): the sheen is now 12/44/68% of Mickey's wall's red/green/blue, was 5/19/37%; parade 21/55/75% (I: assumes bounce scales with the sky). Point 1 predicts 19/48/69% (I).
3. It weighs that much because the base colour is far darker than brick: Drawn maps skip texture_mean (VignetteShot.cpp:7133–7157, 7212–7227): map 0.140/0.047/0.028 (wear: 0.59 of the recipe) × gain 1.0/0.85/0.72 × Mickey's look = 0.128/0.032/0.013, luminance 5%. One measured red brick (Nix Spectro 2, physicallybased.info): 0.262/0.095/0.061, 13% (D, one sample). The sooted looks (terrace-front.py:8228) are pink and grey; the sheen exposes them (D).
4. Its colour: the sky photograph is 7,280 K (HDR and PNG agree; B/R 1.18), the seen sky 7,500 K (D, via the inverse); the wall's light, after warm bounce, about 6,800 K (I). The camera is balanced for 6,500 K (Scene.cpp:404). A neutral addition only greys; its blue turns orange pink and maroon mauve (D, hue arithmetic).
5. Not the cause: the tone curve (its desaturation, TonemapCommon.ush:150–180, 220, applies to both); the sun (unchanged).

## Real brick

No calibrated overcast photograph was opened (downloads need his yes): no evidence. Epic: "All Materials have specular"; cavity maps go into Specular for micro-occlusion (D).

## Options, modelled from the frames (I; about ±4 levels)

| Change | Mickey's wall | Fresh Fish bay |
|---|---|---|
| none | 120/73/58, 0.51, 13° | 0.40, 12° |
| white balance 7,000 K | 121/72/55, 0.55, 14° | 0.44, 14° |
| white balance 7,300 K | 122/72/53, 0.56, 15° | 0.46, 15° |
| sheen ×0.75 (cavity) | 118/67/51, 0.57, 13° | 0.47, 13° |
| exposure −½ stop | 95/54/43, 0.55, 12° | |
| measured brick albedo | 174/124/104, 0.40 | |

## Recommendation

White-balance the day camera to its light: a look-file WhiteTemp, written with the exposure pin on the shot camera and play volume, read off a matte 18% grey card on Mickey's wall (red equals blue within 2%); expected 6,800–7,300 K, likely 7,000. Epic: "When the light temperature and this one match the light will appear white" (D). No material touched.

Expected at 7,000 K: Mickey's wall 120/73/58, S 0.51, hue 13° → about 121/72/55, S 0.55, hue 14° (sheet 0.56, 15°; 7,300 K: 0.56, 15°); Fresh Fish bay 0.40 → 0.44; fascia hue −6° → +6°. Costs: frame mean 140/127/123 → 141/127/120 (sheet 139/129/125); white sash S 0.05 → 0.09 (sheet 0.02). Left: the brick half a stop lighter than the sheet's (exposure, for the whole frame with the road) and the sheen's share (next: cavity into Specular; base colour toward measured brick).

Test: the card frame, then hook and reverse by day. Pass: Mickey's wall S ≥ 0.54, hue ≥ 14°; fascia hue above 0°; frame mean blue ≥ 118; sash S ≤ 0.10; then a fresh reviewer per view beside its last good.
