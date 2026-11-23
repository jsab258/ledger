# Budget table: Silent Hill 2 and inZOI from their files (23 Nov 2026)

Order of 23 Nov, advisor 317. Files read 23 Nov 2026; nothing run against the games. Not yet checked by a fresh reviewer.

## 1. Built on

- Study 12 (production/research/aaa-reference/studies/12-tech-budgets.md): Kingdom Come II's pools and levels (no Mafia game is a reference: his ruling of 20 Nov); LEDGER's frame (16.7 ms median) and 6 GB card line.
- PUBLISHED-NUMBERS-2026-11-09.md, "Still empty": draw distances, memory, asset sizes.
- The extraction in F:/LedgerTools/aaa-study/study-12/budget-2026-11-23/ (NOTES.md, values.json, sizes.json, sh2-ini/).

Adds: Silent Hill 2's own per-preset settings, its console texture pools and its install split. Draw distance gains a value (view distance scale); asset sizes and crowd counts stay empty.

Paths are under sh2-ini/. **G** = SHProto/Config/GFXSettings.ini, section [GFXSettings<preset>]; **E** = SHProto/Config/DefaultEngine.ini; **C** = SHProto/Config/DefaultGFXSettingsConfig.ini; **BS** = Engine/Config/BaseScalability.ini in the game's pak (Epic's defaults, used only to resolve a group level). "Own" = the game's value; "grp" = engine default reached through the group level the preset names. Reading "BaseScalability=Group@n" as "apply Epic's [Group@n]" rests on the names; the game's code was not read (inferred). Where two sections set one key, which wins is not known.

## 2. Silent Hill 2, per preset

The menu's advanced quality defaults to High (C, Adv_Quality Default=2).

| Budget | Low | Medium | High | Epic | Source, key | Kind |
|---|---|---|---|---|---|---|
| Group levels: view, shadow, texture, effects, foliage, GI, reflection, post | 2,2,1,1,1,2,2,1 | 3,2,2,3,3,2,2,2 | 3,2,3,3,3,2,2,3 | all 3 | G, BaseScalability= | own |
| Texture pool, MB | 600 | 800 | 1,000 | 1,000 | BS [TextureQuality@n] r.Streaming.PoolSize | grp; no PC preset sets its own |
| Pool capped to card memory | yes | yes | no | no | BS r.Streaming.LimitPoolSizeToVRAM | grp |
| Console pools, MB | Series S 1,024; PS5, Series X 2,048; PS5 Pro 2,348; editor 3,096 | | | | G [Lockhart], [PS5], [Anaconda], [PS5Ext], [Editor] r.Streaming.PoolSize | own |
| View distance scale | 0.8 | 1.0 | 1.0 | 1.0 | BS [ViewDistanceQuality@n] r.ViewDistanceScale | grp |
| Skeletal mesh LOD bias | 0 | 0 | 0 | 0 | BS r.SkeletalMeshLODBias | grp |
| Virtual shadow maps | off | off | off | off | E [/Script/Engine.RendererSettings] r.Shadow.Virtual.Enable=0 | own |
| Shadow max resolution | 1,280 | 1,280 | 1,500 | 2,048 | G r.Shadow.MaxResolution (Epic: BS ShadowQuality@3) | own; Epic grp |
| Sun cascades | 2 | 2 | 2 | 3 | G r.Shadow.CSM.MaxCascades (groups would give 4 or 10) | own |
| Cascade resolution | 2,048 | 2,048 | 2,048 | 2,048 | BS r.Shadow.MaxCSMResolution | grp |
| Shadow distance scale | 0.85 | 0.85 | 0.85 | 1.0 | BS r.Shadow.DistanceScale | grp |
| Lumen card, max texels | 256 | 512 | 512 | 512 | G r.LumenScene.SurfaceCache.CardMaxResolution | own |
| Card texel density | 0.1 | 0.2 | 0.2 | 0.2 | G ...CardMaxTexelDensity | own |
| Radiance cache probe resolution | 16 | 32 | 32 | 32 | G r.Lumen.ScreenProbeGather.RadianceCache.ProbeResolution (GI@2 alone gives 16) | own |
| Probe atlas, probes | 128 | 128 | 128 | 128 | G ...ProbeAtlasResolutionInProbes; Low's comment: "must be, otherwise interior is leaking" | own |
| Screen probe downsample | 32 | 32 | 32 | 16 | G r.Lumen.ScreenProbeGather.DownsampleFactorProxy | own |
| Reflection downsample | 2 | 2 | 2 | 1 | G r.Lumen.Reflections.DownsampleFactorProxy | own |
| Hardware ray tracing | off by default | | | | C Raytracing Default=0; G [GFXSettings_Raytracing_Off] r.Lumen.HardwareRayTracing=0 | own |
| Screen percentage, upscaler | 100%, TAA, no upscaler by default | | | | C Adv_Supersampling Default=0, Adv_ResolutionScalability Default=3; G [GFXSettingsAdv_Supersampling_None] r.ScreenPercentage=100, r.AntiAliasingMethod=2; the presets also set r.AntiAliasingMethod=4 (TSR); which wins is unknown | own |
| Dynamic resolution | off by default; range 50 to 74.07% | same | same | none set | C DynamicRes Default=0; G r.DynamicRes.Min/MaxScreenPercentage | own |
| Frame-time threshold, ms (a hitch threshold, not a target) | 33.9 | 33.9 | 33.9 | not set | G t.TargetFrameTimeThreshold, r.DynamicRes.FrameTimeBudget | own |
| Motion blur target fps; max | 60; 2 | 60; 2.5 | 60; 3 | 60; 4 | G r.MotionBlur.TargetFPS, r.MotionBlur.Max | own |
| Volumetric fog grid, px / slices | 16 / 96 | 8 / 128 | 8 / 148 | 7 / 164 | G r.VolumetricFog.GridPixelSize, GridSizeZ | own |
| Foliage density | 0.4 | 1.0 | 1.0 | 1.0 | BS foliage.DensityScale | grp |
| Light significance | 2 | 1 | 0 | 0 | G r.LightSignificanceLevel; absent from UE 5.8's base files, meaning by name (unverified) | own |
| Animation budget, significance | none found | | | | values.json name pattern (a.Budget, URO, significance) | — |
| Streaming | own level-streaming asset; 2 level requests at once; no distances | | | | SHProto/Config/DefaultGame.ini [/Script/LevelStreaming.LevelStreamingSettings]; E s.MaxLevelRequestsAtOnceWhileInMatch | own |
| Audio | Wwise; Unreal mixer channels 0; 128 system audio objects | | | | E AudioMaxChannels=0; DefaultGame.ini [AkWindowsInitializationSettings] MaxSystemAudioObjects=128 | own |

**LEDGER for comparison.** No look file sets these: production/specs holds only ps5-corner.json, a one-off experiment at group level 4; no repository ini sets the pool, view distance or virtual shadows (searched 23 Nov). At level 2, UE 5.8's defaults (C:/Program Files/Epic Games/UE_5.8/Engine/Config/BaseScalability.ini, read 23 Nov) give pool 800 MB, view distance 0.8, shadow resolution 1,024, 4 cascades, distance scale 0.85, foliage 0.8, the same as Silent Hill 2's engine copy. The packaged walk draws at a fixed 55% (study 12).

## 3. Install budget (sizes.json)

Classification is by names and folders only; asset classes were not read.

**Silent Hill 2**, 34.93 GB as listed (SHProto-Windows.pak 4.31 + .utoc 30.62):

| Kind | GB | Share |
|---|---|---|
| Textures | 22.77 | 65% |
| Audio (almost all .wem in the pak) | 4.19 | 12% |
| Bulk data not matched by name | 3.95 | 11% |
| Other | 2.62 | 8% |
| Shader code | 0.48 | 1.4% |
| Animation | 0.37 | 1.1% |
| Maps and levels | 0.33 | 0.9% |
| Meshes (static 0.16, skeletal 0.005) | 0.17 | 0.5% |
| Materials | 0.04 | 0.1% |

Meshes look tiny most likely because their data sits in the unmatched bulk (inferred).

**inZOI v0.10.1**, containers only (encrypted), about 29.2 GB: main BlueClient 7.02; backgrounds (eight BG_ containers) 6.48; Characters 5.90; Sound 3.90; Content 1.65; Characters_Anims 1.57; UI 1.25; UE 0.77; Map 0.30; FX 0.28; MetaHumans 0.02. Kinds read from container names only.

## 4. What it means for LEDGER's budgets

1. **Texture pool at High:** flat level 2 leaves LEDGER at 800 MB; Silent Hill 2's PC High gets 1,000, its PS5 2,048. This supports setting the pool explicitly at 1.5 to 2 GB within the 6 GB line, as study 12 proposed (inferred).
2. **What "High" means:** Silent Hill 2 (view, textures, effects, foliage at 3; shadows, GI, reflections at 2) ships a mixed preset, not one flat level. This informs whether LEDGER's High is set per group.
3. **Shadows:** Silent Hill 2 runs without virtual shadow maps, with 2 sun cascades at 1,280 to 1,500 below Epic. This informs the street's shadow method and cascade budget; Silent Hill 2's numbers suit a fog-bounded, 30 fps game (inferred).
4. **Lumen for interiors:** Silent Hill 2 keeps GI at level 2 but raises probe resolution to 32 at Medium and above (Low stays at 16) and holds the atlas at 128; only Low's comment gives the reason, interior light leaks; that the same reason holds at the other levels is inferred. This informs LEDGER's Lumen settings for shop interiors behind glass.
5. **Frame and memory spend:** its PC presets set a 33.9 ms hitch threshold (dynamic resolution off by default), so a 30 fps aim is inferred, against LEDGER's 16.7 ms; and two thirds of its install is textures. A horror-paced, tight-street game spends on texture detail and fog, not distance or crowds; its frame numbers are ceilings, not targets (inferred).

## 5. Not reached

- inZOI's settings and all asset internals: its containers are encrypted; no key was sought.
- Triangle counts, bone counts and texture sizes of people, clothes, props and buildings for both games: these need an asset reader that was not used. Advisor 316 deferred exact asset budgets to the Unreal phase, when a game can be reinstalled.
- No NPC or crowd count keys were found. Wwise voice limits sit in its project data, not reached.


## Review

One fresh reviewer, 23 Nov 2026: pass with fixes; 24 claims checked against the cited files, all correct; four wording fixes applied (the frame threshold, the probe reason, TSR, inZOI's sizes). F:/LedgerTools/gate/new/budget-table-2026-11-23-review.json
