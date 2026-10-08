**Summary: the slow frames come from re-photographing fifteen panes' six-sided street pictures with full Lumen inside play, at load and at every change of light (the three 1024 panes at five times the main view's pixels, with a 2.4 to 2.9 GB memory surge beside the voice); shipped games take such pictures once per light state and only look them up, so LEDGER should bake each pane's picture per state (compressed, box-projected, blended between states later) and never catch in play, with "catch both states at load, behind the title" as the same-day stop-gap.**

# Shop glass that reflects the street without the frame cost (note 1d, 8 October 2026)

## What I could reach

The cloud's network refused Epic's pages, GDC Vault, SIGGRAPH archives, blogs and the press (not retried). I read the repository, and open-source engine code and docs on raw.githubusercontent.com (Godot 4, Unity's HDRP). The rest is search summaries.

Marks. **[SHOWN]** read at its source today (a repository file or a raw GitHub file; a measurement marked SHOWN is as the repository records it). **[CLAIMED]** an earlier repository note read it on the PC (Epic pages, engine source, forums); not re-checked. **[SS]** search summary only: a lead, not evidence. **[I]** my inference.

## 1. The question

The shop glass must show the street: Rita's window as the model, twelve shopfronts with fifteen caught panes, Mickey's office glass seen from both sides. How do we keep that look while the slowest 1% of frames stays at or under 33.3 ms on the RX 6700 at 3440 x 1440 drawn smaller? On 8 October the evening build's 99th percentile was 46.8 ms (33.7 that afternoon, 31.2 that morning).

## 2. How shipped games and engines do reflective glass

**Baked local cubemaps, parallax-corrected ("box-projected").** A six-sided picture of the surroundings is taken once, at build time, near the glass, and stored compressed with blurred smaller copies (mips) for rough glass. "Parallax-corrected" means the reflected ray is first met with a simple box standing for the room or street, and that point is looked up; the reflection then stays in place as the camera moves, instead of acting as if infinitely far.
- Cost: one texture lookup and about ten arithmetic steps a pixel. Godot's box projection is about ten lines of shader [SHOWN]; its docs call it "a small performance cost", "often worth it in box-shaped rooms" [SHOWN]. Unity HDRP rates baked probes "Low" runtime cost and realtime probes "Medium-High (depends on the resolution)" [SHOWN, Unity docs].
- Who: Lagarde and Zanuttini, "Local image-based lighting with parallax-corrected cubemaps", SIGGRAPH 2012, for Dontnod [SS]. Remember Me (2013, Unreal 3): 150 to 200 local cubemaps per large level [SS]. Spider-Man 2 (2023): window interiors from emissive cubemaps through "a custom baking pipeline" [SS, a developer's portfolio].
- Limit: nothing moving shows, and each lighting state needs its own picture.

**Runtime captures (Unreal's scene capture; "realtime probes" elsewhere).** The same picture, re-rendered by the game. Engines keep it cheap by doing less:
- Godot draws at most one "Once" probe a frame, its six faces in that frame, the blurring spread over later frames. For "Always" (every frame) its docs advise shadows off, as "very expensive", and offer coarser meshes [SHOWN].
- Unity HDRP can "time slice" a realtime probe over seven frames, one face a frame [SHOWN].
- GTA V (2013) re-renders a cube every frame, but at 128 x 128 a face, about thirty draw calls a face, no people or vehicles [SS, Courrèges, 2015].
- None of these runs global illumination inside the capture. Ours does: Lumen, six faces, twelve passes [SHOWN, our code].

**Planar reflections.** The scene drawn again, mirrored about one plane: sharp and live. 1.7 to 23 ms in Epic's examples; the clip plane adds about 15% to every base pass [CLAIMED]. Lumen does not run in a planar view, so our terrace would come back dark [CLAIMED]. Hitman 3's windows and 007 First Light's mirrors use them [CLAIMED].

**Screen-space reflections** reuse the picture on screen (Unity: "the depth and color buffer of the screen") [SHOWN], so they reflect only what is on screen. Facing a pane, the reflected ray points behind the camera: nothing to find. At glancing angles it goes forward and often finds the far frontage [I]. Our translucent glass takes Lumen's front layer instead [CLAIMED].

**Lumen on translucent and opaque glass.**
- Translucent (ours, Thin Translucent): Lumen's "front layer" gives the frontmost pane a reflection [CLAIMED]. It traces the screen, then distance fields, then the coarse surface cache, so a terrace behind the camera returns soft and dim [CLAIMED]; the 6 October gate found "almost no street reflection" [SHOWN, DECISIONS.md].
- Opaque glass, a reflective coat over an interior-mapped room: Lumen's full opaque reflections, no translucency cost. City Sample and Spider-Man use it for rooms nobody enters [SS]. Our shops have real 3D rooms behind glass since 3 October [SHOWN, import_shop_rooms.py], so it suits only upstairs and house windows.
- Hardware ray tracing is the sharp answer (Watch Dogs Legion's windows) [CLAIMED]; its scene alone cost 3.6 ms here [SHOWN, DefaultEngine.ini].

**Baked states, blended.** Assassin's Creed Unity (2014) baked its light at four time-of-day keyframes [SS, a SIGGRAPH 2025 course table]; a transition blends two neighbouring states [I]. LEDGER's pictured rooms already swap day, lit and dark pictures by state [SHOWN, make_interior_material.py].

**On and behind the glass.** Interior mapping meets the eye's ray with a box behind a flat pane (van Dongen, 2007-2008) [SS]. Fresnel: about 4% face on, toward a mirror at grazing angles [CLAIMED]; ours is Schlick, base 0.04, exponent 5 [SHOWN]. Dirt raises roughness and dims the reflection; Dishonored's glass is glossy, dark, slightly wobbly [CLAIMED]; with mips, roughness can also blur it, as Godot does [SHOWN]; our runtime cubes have no mips [I]. At night a pane shows only light sources and lit surfaces, so each emitter's brightness must be in proportion [CLAIMED]. Rain on the pane is a normal map of drops and runs [I]; a wet road changes what the glass reflects, and our hook reviewer saw a matte road in the catch as a pale wash [SHOWN, DECISIONS 8 Oct 16:05].

## 3. Why our catch costs so much

**What the game does now** [SHOWN, VignetteShot.cpp, unreal-look.json, CrimeProbe.cpp]:
- Fifteen panes each own a cube: 1024 a face for Mickey's window, Rita's and Mickey's door glass; 256 for the twelve others.
- A "round" catches every pane in turn: a new capture renders all six faces on twelve consecutive frames (the first eleven into a spare cube), then is destroyed.
- Each capture runs Lumen's light and reflections, keeps its rendering state, records linear colour, leaves out people and hair.
- A round starts six seconds after the panes are made, and again at every change of light: in play, at 19:00 and 07:00, also when a wait crosses them.

**The measurements** [SHOWN, ue-perf-verdict.txt history; DECISIONS.md; GATE-GLASS.md]:

| Build (8 Oct) | Hero panes | Median ms | p99 ms | Worst ms | Frames over 33.3 (of 1,500) |
|---|---|---|---|---|---|
| 0b52227 (03:02) | two at 512 | 13.81 | 31.19 | 50.6 | 5 |
| 62be907 (14:04) | three at 512 | 14.36 | 33.66 | 55.6 | 16 |
| same, -GlassCatchNoLumen (played copy) | | | 26 | | 5 |
| 69d0948 (16:43) | three at 1024 | 14.38 | 46.83 | 234.8 | 43 |

The morning build already had Lumen catches; its slow passes were probably just under the bar until the afternoon's heavier street and third hero pane pushed them over [I]. Two tries failed: one capture moved from pane to pane; a cheaper catch (no reflections, half the gather) that caught the road pale. In the gate's runs the game's card memory peaked at 7.4 and 7.9 GB in rounds, against 4.98 before and 5.27 after.

**The causes, most likely first.**
1. **Lumen inside each capture, from a fresh start for every pane** [SHOWN by the no-Lumen run]. The builder found each pane's first pass over 33 ms: about fifteen slow frames a round. The probe allows only 14 of its 1,500 frames over the bar [SHOWN, tools/slice-perf.py]. Why that first pass is slow is not known (section 6).
2. **Pixels at 1024** [I, from SHOWN settings]. Each hero pass draws 6 x 1024 x 1024 = 6.3 million pixels with full Lumen; the probe's main view (3440 x 1440 at 50%) draws 1.24 million. Five times the main view, 36 times a round. Slow frames rose from 16 to 43 with the change to 1024: close to the 33 hero passes after each first one.
3. **The memory surge beside the voice** [I, from SHOWN numbers]. A round adds 2.4 to 2.9 GB. A voice held 2.1 GB of the card in P1's packaged measure (the slice probe runs another voice; its share is not recorded). 7.9 + 2.1 fills the 10 GB card, and an overfull card pages to system memory and stalls: the likeliest cause of the single 235 ms frame.
4. **One-off allocations at the first 1024 pane** [I]: the spare 1024 cube made and cleared on the game thread, scene buffers at 3072 x 2048, a fresh Lumen state.
5. **Where the round falls** [SHOWN code; I for the effect]. The slice probe profiles from launch and drops only the first 300 frames, so the load's round is inside its measured frames. P1's profile starts eight seconds into play and may miss part of the round: perhaps why it read p99 25 ms on 7 October with Lumen catches at 512 [SHOWN, P1-PACKAGED].
6. **Spreading the round would not fix p99** [I]: the slow frames stay as many, only further apart. Only cheap pieces, or none in play, help.

Probably not the cause: the glass's shading in the main view (median 14.36 to 14.38) [I].

## 4. What fits LEDGER, cheapest first

Costs are at 3440 x 1440 drawn at 50 to 55% on the RX 6700, all [I] unless marked; section 5 measures them.

### A. A baked picture per pane per light state (recommended)

- **Frame cost.** No capture in play. One cube lookup plus the box arithmetic per glass pixel: well under 0.1 ms. The day/night switch swaps a texture: no slow frame.
- **Memory.** Compressed HDR (BC6H) is 1 byte a texel against 8 today: a 1024 cube about 8 MB with mips, a 512 cube about 2 MB. Three heroes at 1024 and twelve at 512: about 50 MB a state, 100 MB for day and night, against about 230 MB held today plus the surge.
- **Hook camera.** The same light as today's catch, being the same capture made at build time. Time no longer matters there, so supersample it (the lab's four quarter-texel turns averaged, or 2048 halved): the remaining steps go. Box projection keeps the reflected roofline in place as Tom moves.
- **Reverse view.** Grazing panes are near-mirrors: 512 and box projection help most here.
- **Inside Mickey's office.** Add a room-side cube for the pane's inner face, baked inside the office dark and lit, box-projected to the room's walls (a box room is the ideal case [SHOWN, Godot docs]). At night with the office lit, the glass then shows the room, as real night glass does.
- **Day, night, later states.** Phase 1: two bakes. Four or five states with transitions later: one bake each, the material blending the two neighbours (two lookups). Night bakes keep the lamp heads' highlights; the format holds bright values [I].
- **Rain.** Dry and wet bakes per state, blended by the wetness value the road uses; drops on the pane as a normal map.
- **Not shown:** passers-by and cars, as today.

**Setup in Unreal 5.8:**
1. **Bake run.** A launch flag (for example -GlassBake=day or night) lights the street in that state, lets it settle and runs today's catch unchanged: Scene Colour HDR, Lumen light and reflections, kept rendering state, bExcludeFromSceneTextureExtents, people and hair off, twelve passes; heroes supersampled.
2. **Saving.** In the editor, UTextureRenderTargetCube::ConstructTextureCube makes a cube asset from the render target [SS, Epic API listing]. Or the existing dump (-GlassCatchDump) to .hdr under F:\LedgerTools\game-inputs\glass-bake\<state>, imported as cubes: check its resolution first (section 6).
3. **Texture settings.** "HDR Compressed" (BC6H), sRGB off, mips from the texture group, LOD group World, Never Stream on. Under /Game/Ledger/GlassBake/<state>/: /Game/Ledger is always cooked [SHOWN, DefaultGame.ini].
4. **A stamp.** Each bake's manifest holds hashes of the street export, the look file and the pane list; the import step fails the build when they differ, so a stale bake cannot ship.
5. **Material** (make_glass_material.py): ReflectCubeA, ReflectCubeB, ReflectBlend; ReflectOrigin, ReflectBoxMin, ReflectBoxMax, made relative to the pane outside the code as M_LedgerInterior does; a Custom node with Godot's box projection; the mip chosen by roughness; the reflection times (1 minus dirt).
6. **The box.** Far wall: the opposite frontage's plane. Floor: the road's crown. Ends: 20 m along the street each way. Top: 100 m, so the sky stays far.
7. **Game.** CatchStreetInGlass loads the baked cubes instead of making render targets; ReDriveStreetLook swaps them; no captures in play. -GlassCatchLive keeps today's route for the bake and for comparison.
8. **Console variables.** None new. Keep r.Lumen.TranslucencyReflections.FrontLayer.EnableForProject=True and FrontLayer.Allow=1 (ours; 0 at the engine's High [CLAIMED]). Separately, later: "Allow Front Layer Translucency" off in the material for baked panes may save median time; measure first.

### B. Catch both states at load, behind the title (stop-gap)

- **Frame cost:** none in steady play; the switch swaps pictures already caught.
- **Load:** two rounds, about 400 frames, roughly 10 to 20 more seconds [I]. **Memory:** about 180 MB more for the second set; the surge moves to load, where it can still overfill the card.
- **Look:** identical to today.
- **Snags.** The title shows the street behind it [SHOWN, TitleScreen.cpp], so catching night shows it at night for some seconds (or catch that state at its first switch, behind a short fade). The first launch's picture tuning times 90 frames or more [SHOWN]: it must not run during a round, or it steps the picture down for nothing.
- **Steps:** count the street "ready" only when LedgerVignetteShot::GlassCatchesLeft() is 0; give each pane a day and a night cube; ReDriveStreetLook swaps them instead of starting a round.

### C. Catch at load, catch again at each switch

The direction named on 8 October. Steady play is free, but 19:00 and 07:00 still bring 16 to 43 slow frames. Acceptable only if every switch is hidden: waits are, walking through 19:00 is not.

### D. Not fitting

A capture sliced one face a frame (Lumen's start-up falls on each face; a 1024 face with Lumen is near the main view's whole cost; complex). Planar reflections (1.7 to 23 ms every frame, dark without Lumen [CLAIMED]). Hardware ray tracing (3.6 ms before tracing [SHOWN]). The front layer alone (almost no street [SHOWN]). The cheaper catch (the pale wash [SHOWN]).

### Recommendation

**A.** It is what shipped games and both open engines read here do for a static street, and the only route where play and the switch both cost nothing. It also fixes the steps and the memory, and carries later states and rain by blending. Keep 1024 for the three camera panes (free once baked), 512 for the rest. Do B first only if A cannot reach the packaged build within the item.

## 5. How to verify with numbers

**Frame time,** packaged build, the probe's slice-perf line (median, p95, p99, worst, frames over 33.3):
1. Standing still, as now.
2. A forced day-to-night switch about ten seconds into the measured frames (a new flag): the old cost came with each switch.
3. Walking (PerfHook walk).
4. Each also with -GlassCatchLive in the same build, and once with the cubes off as the baseline.

**Pass:** p99 at or under 33.3 ms in all three (at most 14 of 1,500 frames over); the slowest frame within two seconds of the switch at or under 33.3; the median within 0.3 ms of the baseline; the worst at or under 55 ms (this week's passing builds: 40 to 55 [SHOWN]); no memory rise at the switch, the card with the voice under 9.5 GB (P1's peak [SHOWN]). For any cost left, one GPU profile (ProfileGPU or Unreal Insights) of the switch frame.

**Look:** fixed cameras (office by day and night, hook by day, reverse view, night street), each beside its last good picture (the glass gate's t2 and t3 by day, t1 by night):
- Office by day: reflected terrace, gable and road within 10% of 62, 54 and 84 [SHOWN, GATE-GLASS].
- Hook: Mickey's pane foot and Fresh Fish's patch within 10% of 43 and 110 [SHOWN].
- At a 4x crop, no regular steps.
- Box projection: the reflected roofline within 5 px of the true one from two spots a metre apart (the 7 October bar [CLAIMED]).
- The baked cube's mean within 10% of a live dump.
- A fresh reviewer per view.

## 6. To check on the PC (installed 5.8.2 source first, file and line cited)

1. **Why a fresh Lumen capture's first pass is slow:** Insights on a catch frame; Lumen's per-view state (Renderer/Private/Lumen), the surface cache's card-capture budget (r.LumenScene.SurfaceCache.CardCapturesPerFrame, CardCaptureRefreshFraction: names and defaults), and whether a scene capture gets its own Lumen scene data (ScenePrivate.h, LumenSceneRendering.cpp).
2. **ConstructTextureCube** (Engine/Classes/Engine/TextureRenderTargetCube.h): editor-only? A size rule? (A forum answer says "divisible by 512" [SS].)
3. **ExportRenderTargetCubeAsHDR** (ImageUtils.cpp, CubemapUnwrapUtils.cpp): a long-lat unwrap, at what size? And the importer's face size from it. A 2:1 unwrap may halve a 1024 cube's resolution.
4. **BC6H for a cube texture** on DirectX 12, and seamless mip filtering.
5. **The inner face:** does the office camera see the pane's back face, and what does the street cube give there? (The material samples the world reflection direction [SHOWN].)
6. **UpdateResourceImmediate(true)** on a 1024 cube (TextureRenderTargetCube.cpp): a render-thread stall? (Cause 4.)
7. **The surge with the voice,** from Windows' counters during a slice-perf run, as P1 did. (Cause 3.)

## 7. To read from the PC or once the network opens

Epic's Scene Capture, Reflection Captures and Lumen Performance Guide pages (5.8); Lagarde and Zanuttini's 2012 slides; Courrèges' GTA V study (2015); the GDC 2013 Remember Me talk; Assassin's Creed Unity's GDC 2015 lighting talk; the SIGGRAPH 2025 Advances course (Assassin's Creed Shadows); the Unreal answers thread on "Create Static Texture" for cube targets.

## 8. Sources

**Repository**, branch cloud/week-42, read 8 October 2026 [SHOWN; engine and web claims inside the notes CLAIMED]:
- FOR-JAFAR.md, NOW.md, RULINGS.md (7 Oct lighting, 5 Oct weather), FINDINGS.md, DECISIONS.md (6 Oct; 8 Oct 14:40 to 16:45)
- production/research/shop-glass-reflections/: NOTE.md (1 Oct), CAPTURE-STEPS-2026-10-07.md, CLOSE-RANGE-ROUTES-2026-10-07.md, NIGHT-2026-10-08.md
- origin/lab:production/lab/GLASS-NOTES.md (8 Oct, a710829)
- production/audits/glass-2026-10-08/GATE-GLASS.md
- production/d1-probe/ue-perf-verdict.txt at 03c0476, f2422f8, 61acbe1, ebe22f0, 25cddd9 (7 to 8 Oct)
- production/research/pre-production/P1-PACKAGED-2026-10-07.md; production/research/unreal-frame-budget/ (14 Sep; nothing on glass)
- ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp (FGlassCatch, MakeGlassCapture, GlassCatchScratch, TickGlassCatch, CatchStreetInGlass, ReDriveStreetLook), CrimeProbe.cpp (ClockLight, PerfHookTick, PageShotsTick), TitleScreen.cpp, Public/StreetMeshes.h; commits ea5c567, ce05477
- ue-probe/Config/DefaultEngine.ini, DefaultScalability.ini, DefaultGame.ini; production/specs/unreal-look.json
- tools/ue/make_glass_material.py, make_interior_material.py, import_shop_rooms.py; tools/slice-perf.py; .github/workflows/ledger-probe-unreal.yml (slice-perf step)

**Open source, reached 8 October 2026** [SHOWN] (master branches, undated):
- https://raw.githubusercontent.com/godotengine/godot/master/servers/rendering/renderer_scene_cull.cpp
- https://raw.githubusercontent.com/godotengine/godot/master/servers/rendering/renderer_rd/shaders/scene_forward_lights_inc.glsl
- https://raw.githubusercontent.com/godotengine/godot-docs/master/tutorials/3d/global_illumination/reflection_probes.rst
- https://raw.githubusercontent.com/Unity-Technologies/Graphics/master/Packages/com.unity.render-pipelines.high-definition/Documentation~/ (Reflection-Probe.md, reflection-understand.md, Override-Screen-Space-Reflection.md)

**Search summaries only, 8 October 2026** [SS], not reached:
- https://history.siggraph.org/?p=140207 (Lagarde and Zanuttini)
- https://polycount.com/discussion/comment/1910043 (Dontnod's cubemaps); https://gdcvault.com/play/1019260/The-Art-and-Rendering-of (GDC 2013)
- https://www.adriancourreges.com/blog/2015/11/02/gta-v-graphics-study/ (2 Nov 2015)
- https://gamedeveloper.com/programming/interior-mapping-rendering-real-rooms-without-geometry; https://automaton-media.com/en/news/20231201-23558/ (1 Dec 2023); https://jtuason.artstation.com/projects/XgVxQL
- https://www.realtimerendering.com/advances/s2025/content/Advances%202025%20-%20Raytracing%20the%20world%20of%20Assassin's%20Creed%20Shadows.pdf (2025)
- https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UTextureRenderTargetCube; https://answers.unrealengine.com/questions/523339/view.html

**Refused** (8 October 2026): adriancourreges.com, realtimerendering.com, history.siggraph.org, developer.valvesoftware.com, the GitHub API.

Nothing here needs a purchase, Megascans, a real brand or anything marked NoAI. Godot (MIT) and Unity's documentation were read as references; no code was copied.
