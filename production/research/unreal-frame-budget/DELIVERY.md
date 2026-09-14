# Unreal performance budgets for a dense street, on consumer hardware

Research topic 17. Delivered to the studio. Nothing here is an instruction.

Scope, declared in topic 2 and honoured here: topic 2 asked what FITS (memory,
a wall). This one asks what is FAST (frame time, a negotiation). Topic 2 closed
by naming "how much memory the Unreal street actually uses" as never measured.
This topic finds the frame-time half in the same condition, and worse: the
engine we ship on has no frame-time instrument at all.

Method: establish what this repository has actually measured, at HEAD, by
running the checks rather than recalling them; then assemble the published
figures for the Unreal systems we have committed to; then do the arithmetic in
the open so every step can be disputed.

Labels follow `production/art/atlas-02/research/`: CITED (a source says it),
DERIVED (arithmetic on cited or measured numbers, shown), ASSUMED (a judgement
with no source), HOLE (could not be established).

---

## Part 1. What this repository has measured

Every claim in this part was produced by a command run on 2026-09-14 against
this checkout, not recalled.

### 1.1 The engine is Unreal, and the only frame-time instrument is in Unity

CITED, `ledger-v2/respec/decision-register/D16-engine-unreal.md`: "The engine
is Unreal", DECIDED 2026-09-10 by Jafar. Unity becomes the legacy reference
build; the C# Core stays as the source of truth the C++ port is checked
against.

CITED, this checkout: the project's only frame-time readout is
`ledger/Assets/Scripts/Core/FrameRate.cs`. It is careful and well argued. Its
header states the reason it exists: "CI has no GPU, so this project has never
measured a frame time that means anything, and the first person to play it is
the first real measurement." It carries `MeanMs` and `WorstMs` over a
`WindowSeconds = 3.0` rolling window, deliberately two numbers rather than one,
"because thirty seconds at 120fps with four 200ms hitches in it averages
beautifully and is horrible to play."

It has exactly one live call site. A grep for `FrameRate` across every `.cs`
file returns five files: the class itself, `CoreTests/Program.cs` (its tests),
two comments in `NpcWalker.cs` and `Perception.cs` that mention it, and
`Game/DialogueUI.cs:1350`, which declares `FrameRate _frames`, ticks it at
:1354 and prints it at :1573. `DialogueUI` is a Unity Game-layer script.

DERIVED: the project's only frame-time instrument is consumed only by the
engine that D16 archived.

### 1.2 The Unreal probe has no frame-time instrument, and one file's name says otherwise

CITED: `ue-probe/Source/LedgerProbe/Public/FrameStats.h` is an IMAGE statistic
file. It carries MeanLuma, NonBlackPct and DistinctBuckets. It is not a frame
timer, and its name is the closest thing in the tree to one. A false friend.

CITED: grepping `ue-probe/` for `FrameTime`, `DeltaTime`, `FPlatformTime`,
`GAverageFPS`, `GAverageMS`, `stat unit`, `stat gpu` and
`RHIGetGPUFrameCycles` returns nine hits, all of them `FPlatformTime::Seconds()`
used for wall-clock elapsed time: run duration, probe timeouts, a start stamp.

CITED: two verdict lines do carry a tick count beside an elapsed time.
`VignetteSpec.h:3150` `CaptureDoneLine` emits `captureSeconds=%.2f
captureTicks=%d`; `CrimeProbe.cpp:1121` emits `crimeTicks=%d
crimeSeconds=%.2f`. Nothing anywhere divides one by the other.

Interpretation, not finding: the quotient would not be a frame time if anyone
did divide them. Both runs do substantial non-frame work inside the measured
span, `VignetteShot` decodes and re-encodes PNGs, so seconds-over-ticks is a
mean cost of a probe iteration and not a mean cost of a rendered frame. Saying
so is cheaper than someone deriving it later and quoting it for a year.

### 1.3 The Unity reference build's numbers, and exactly what they are statistics of

The live evidence channel is one file, `game-design/sim-shots/verdict.txt`,
written by the Windows build, header `# Sim verdict - cb4767e @1788396374`. Its
two performance lines read, verbatim:

    perf[samples=24702 meanMs=0.24 limit=4.00]
    frame[mean=29.0ms gameBudget=12ms npcsMs=4.85 populationMs=0.06
    bodyLodMs=0.06 sunMs=0.15 mixMs=0.21 checksMs=0.01 trafficMs=0.24
    signalsMs=0.08 rigsMs=0.70 game=6.36ms render+rest=22.67ms
    gameShare=21.91%]

(reflowed here for width; it is one line in the file.)

What each number is a statistic OF, read out of `SimDirector.cs:14134` rather
than inferred:

- Every `...Ms` on the frame line is `c.TotalMs / Perf.FrameCount`. That is the
  subsystem's total cost divided by the number of frames in the whole run, so
  it is "milliseconds of this subsystem per frame of the run, mean over every
  frame". This is the correct statistic for a budget and it is worth stating
  because it is NOT the same as the subsystem's own per-call mean.
- `perf[meanMs=0.24]` is different: it is `Perf.Counter.MeanMs`, which is
  `TotalMs / Samples`, a per-call mean for traffic over 24,702 calls, gated
  against `limit=4.00`. Two numbers on one page called mean, computed two ways.
- `game=6.36ms` is the sum of the nine attributed scopes.
- `render+rest=22.67ms` is `Math.Max(0, meanFrameMs - attributed)`. It is a
  RESIDUE, not a measurement, and it therefore absorbs every attribution error
  in the frame. `SimDirector` says so itself at :14095.
- `gameBudget=12ms` is not a target. `SimDirector.cs:14204` sets
  `GameFrameBudgetMs = 12.0` and the comment gives the reasoning in full:
  "6.00ms of game systems against a 16.67ms frame at 60fps is the real budget,
  and 12ms, under three quarters of that frame, twice what was measured, is a
  ceiling a genuine regression crosses and runner noise does not." It is a
  regression ratchet set at roughly two times the measured value, and it is
  honest about being that.

Populations on the same run: `npcsListed=65`, `walkers=64`, `npcs=42`,
`rigs=92`, `riggered=21`, `streetBodiesSkinned=13`, `walkersPrimitiveOf=65`.

DERIVED per-unit costs, with denominators named:

| quantity | value | denominator |
|---|---|---|
| sim cost per walker per frame | 0.0746 ms | 4.85 ms over 65 listed walkers |
| rig solve per solved rig per frame | 0.0333 ms | 0.70 ms over 21 solved that frame |
| rig cost per rig component per frame | 0.0076 ms | 0.70 ms over 92 rig components |
| traffic against its own gate | 6% | 0.24 of a 4.00 limit |
| game systems as share of a 60fps frame | 38.2% | 6.36 of 16.67 |
| game systems as share of a 30fps frame | 19.1% | 6.36 of 33.33 |
| npcs as share of game systems | 76.3% | 4.85 of 6.36 |

The `npcs` scope is `GameController.cs:1061`, a `using (Perf.Time("npcs"))`
around a loop calling `npc.Tick(Now)` on every walker. It is simulation:
steering, perception reporting, schedule targets. It contains no animation
evaluation and no rendering. The animation half is `rigs`, a separate scope at
`CharacterRig.cs:1727`.

### 1.4 The geometric load, which is the half that transfers between engines

CITED, `verdict.txt` line 22: `SceneAudit: renderers=23072 skinned=199
skinnedBones=4824 skinnedVerts=998766 clean=True findings=0`.

`SceneAudit.cs:180` explains why those and not milliseconds, and the reasoning
is the best thing in this part of the repository:

    "This runner cannot answer the other half in milliseconds, it has no GPU
    and software-rasterises everything, so a skinning time measured here
    describes a software rasteriser and would be quoted for a year and wrong on
    every real machine. Bones and vertices are not like that. They are what the
    mesh actually is, they are identical on any hardware, and they are the input
    any GPU estimate needs."

DERIVED: 24.2 bones and 5,019 vertices per skinned renderer; 199 skinned
renderers are 0.86% of the scene's 23,072 renderers. Against the 13 skinned
bodies on the street that run, 76,828 vertices per body, which either means
bodies are being counted that are not on the street, or the bought bodies are
being imported at a density no shipped game would ship. Both are worth knowing
and neither is settled here: HOLE, the denominator that would settle it
(skinned renderers per body) is not printed.

### 1.5 A decayed claim, and the one key that would settle it

Three source files state that the CI runner has no GPU:

- `Game/Perf.cs:37`: "CI runner has no GPU, falls back to software
  rasterisation, and turns in 191ms frames"
- `Game/SceneAudit.cs:193`: "it has no GPU and software-rasterises everything"
- `Game/CharacterRig.cs:1739`: "HONEST ABOUT WHAT THIS RUNNER CAN ANSWER. It
  has no GPU"

Dates, from `git log -S` on each sentence: the `Perf.cs` line landed
2026-07-26 (b72a0f4c), the other two 2026-08-03 (380eb3ef).

CITED, `.github/workflows/ledger-build-windows.yml:23`: `runs-on: [self-hosted,
ledger-pc]`. That change landed 2026-08-22 in 70ba3530, "The builds move onto
Jafar's PC, and three smaller things ride along". `ledger-pc` is the machine in
`production/mesh-reports/mesh-machine-report.txt`: Ryzen 5 5600X, 6 cores,
31.9 GB RAM, AMD Radeon RX 6700 with 9.98 GB, plus a Parsec Virtual Display
Adapter.

CITED, the same workflow at :435: the sim runs the packaged player with
`-screen-width 1280 -screen-height 720 -screen-fullscreen 0 -force-d3d11`, and
with NO `-nographics`. The `-nographics` flag appears once in the file, at :370,
on the Unity editor BUILD step, not on the sim run.

So: the three comments were true when written, the machine underneath them
changed nineteen to twenty-seven days later, and none of the three has been
re-read since. That is rule 1's second corollary ("changing code changes the
comments about it") paying out at a distance, where the thing that changed was
not code at all but the runner.

What I will NOT claim: that the 29.0 ms frame was rendered by the RX 6700.
`verdict.txt` prints no adapter name. A grep for `gpu`, `adapter`,
`graphicsDevice` and `d3d` keys in it returns one hit, `gPush=0.8600`, which is
a gossip term. A `-force-d3d11` request on a Windows session can still land on
WARP or on the Parsec virtual adapter, and this machine has both. HOLE, and it
is a one-line hole: nothing prints
`SystemInfo.graphicsDeviceName`.

That single missing key is the difference between "this project has never
measured a real frame time" and "this project has been measuring real frame
times on the target GPU for three weeks and telling itself it has not."

### 1.6 Nobody has ever rendered a person on the Unreal street

CITED, `production/systems-inventory.json`, tile "the crowd you see", status
partial, typed 2026-09-09: "Walkers move, keep their gaps and huddle in the
headless sim: 65 listed, none duplicated, tightest gap 0.33 metres. No frame
committed here shows anybody walking the Unreal street, which is rung 4 and not
started."

CITED, tile "the frame budget", status partial: "no budget for the Unreal
street at a resident count is set in this checkout, which is phase 1's gate."

CITED, `ledger-v2/respec/roadmap-v2.md:26`, phase 1's gate includes "sim holds
frame budget at target resident count". Line 27, phase 2: "one street at the
visual bar ... 30 to 50 residents".

DERIVED: phase 1 gates on two numbers, a frame budget and a target resident
count, and neither exists in this checkout. Phase 2 supplies one of them, 30 to
50, and no document supplies the other. A grep of `D8-visual-bar.md` for fps,
frame, 1080, 720, resolution, 60 and 30 returns nothing: the visual bar names
no frame rate.

### 1.7 The graphics preset ladder is a Unity cost model and does not port

CITED, `ledger/Assets/Scripts/Core/Detail.cs:129`: `CostIndex` weights the
presets `0.42 * shafts + 0.26 * shadows + 0.20 * bodies + 0.12 * crowd`,
described as "Weighted by what actually costs: the shafts dominate, shadows
next, and the crowd contributes but is never the lever." The function is honest
about its purpose, "used only to prove the presets are ordered", so it is not
claiming to be a budget.

The weights are ASSUMED, no series is cited, and more to the point light shafts
and reflection probes are not how Unreal lights a scene. The three preset
distances that DO port are physical, not rendering: `BodyDetailDistance` 12 /
22 / 34 metres, `CharacterRig.SolveWithinMetres = 34f`, and `CrowdFraction`
0.75 / 0.9 / 1.0, the last of which carries an argument worth keeping in the
port: "Halving the crowd is the biggest single frame-time win available and it
is the one thing that must not be taken. The street is the game."

---

## Part 2. The published figures for the systems we are committed to

Egress note, stated plainly because it is silent when it fails: the primary
sources for most of this part are blocked from this container.
`dev.epicgames.com`, `gpuopen.com`, `getperfguard.com`,
`www.coconutlizard.co.uk` and `en.gamegpu.com` all returned EGRESS_BLOCKED from
the network proxy on 2026-09-14. Everything below therefore comes from search
result summaries rather than from a primary page I opened myself. Where two
summaries disagree I say so instead of picking one. Where a figure appeared in
exactly one snippet and did not reproduce on a differently worded search, it is
labelled as such and should not be leaned on.

### 2.1 The frame budget itself

CITED: 60 fps means 16.67 ms for CPU and GPU both; 30 fps means 33.33 ms. The
first console command in any Unreal optimisation session is `stat unit`, which
splits the frame into Game thread (blueprints, tick, AI, animation, physics),
Draw / Render thread (render command generation, material processing) and GPU.
The highest of the three is the bottleneck. `stat gpu` gives the per-pass
breakdown.
[Intel, Unreal Engine Optimization Guide: Profiling Fundamentals](https://www.intel.com/content/www/us/en/developer/articles/technical/unreal-engine-optimization-profiling-fundamentals.html),
[StraySpark, UE5 Performance Profiling 101](https://www.strayspark.studio/blog/ue5-performance-profiling-101),
[Unreal Art Optimization, Measuring Performance](https://unrealartoptimization.github.io/book/process/measuring-performance/)

CITED, a conventional 60 fps decomposition: game logic about 2 ms, culling and
sorting about 1 ms, draw call submission about 2 ms, geometry pass about 4 ms,
lighting and shadows about 4 ms, post about 2 ms, vsync and buffer overhead
about 1 ms, headroom 0.67 ms.
[StraySpark, UE5 Performance Profiling 101](https://www.strayspark.studio/blog/ue5-performance-profiling-101)

Interpretation: that decomposition assumes the game logic is the smallest term
in the frame. For LEDGER it is the product. Keep the arithmetic, discard the
allocation.

### 2.2 Lumen

CITED, and this is the most load-bearing number in the topic: Lumen "targets 30
and 60 frames per second on consoles with 8ms and 4ms frame budgets at 1080p
for global illumination and reflections on opaque and translucent materials,
and volumetric fog". The Epic scalability level produces around 8 ms on
next-generation consoles at 1080p internal resolution, relying on Temporal
Super Resolution to output at something approaching 4K.
[Epic, Lumen Performance Guide (via search summary; the page itself is egress-blocked)](https://dev.epicgames.com/documentation/unreal-engine/lumen-performance-guide-for-unreal-engine)

CITED: Lumen's software ray tracing path runs on GPUs around the GTX 1080 class
and above; mid-range cards usually require careful optimisation even at a 1080p
target.
[Althera Games, Lumen Deep Dive](https://altheragames.com/en/blog/ue5-lumen-guide)

CITED: on an RTX 3060, software Lumen typically holds an editor viewport above
60 fps at 1080p with moderate scene complexity, while hardware Lumen ray
tracing drops it to 30 to 45 fps on complex scenes.
[EveZone, RTX 3060 for Unreal Engine 5 Development](https://evezone.evetech.co.za/performance-pulse/rtx-3060-for-unreal-engine-5-development-professional-benchmark-2026)

### 2.3 Nanite

CITED: Nanite costs about 4.5 ms of GPU at 60 fps, "which fits the bill for a
60fps render time (you have still 10-12ms to do everything else)".
[IconEra thread quoting the UE5.1 60fps-on-console material](https://icon-era.com/threads/unreal-engine-5-1-now-60fps-on-next-gen-console-with-lumen-nanite-and-virtual-shadow-maps.1494/)

CITED: Nanite meshes have effectively no per-instance draw call cost regardless
of instance count, and more than roughly 2,000 draw calls in a conventional
path is the signal to instance or merge.
[Intel, Profiling Fundamentals](https://www.intel.com/content/www/us/en/developer/articles/technical/unreal-engine-optimization-profiling-fundamentals.html)

### 2.4 Virtual shadow maps and why a crowd is not a prop

CITED, and this is the finding that reframes the whole topic: "Geometry that
can be deformed using Skeletal animation always invalidates cached pages every
frame." A skeletal mesh casting a VSM shadow invalidates pages every frame the
animation updates, and "this invalidation is unavoidable for crowd NPCs".
[Epic, Virtual Shadow Maps (via search summary; page egress-blocked)](https://dev.epicgames.com/documentation/unreal-engine/virtual-shadow-maps-in-unreal-engine),
[StraySpark, Virtual Shadow Map Optimization for Open Worlds](https://www.strayspark.studio/blog/virtual-shadow-map-optimization-open-worlds-ue5-7)

Interpretation: VSM is the shadow system Lumen and Nanite assume. In that
system a standing building is nearly free to shadow after the first frame,
because its page stays cached, and a walking person is not, every frame,
forever. This is a structural reason why crowd counts from older engines do not
transfer to UE5, and it is the mechanism behind the specific reconciliation in
Part 3.

### 2.5 Skeletal meshes and the animation budget

CITED: Nanite's skinned mesh support was experimental in 5.4 and stabilised in
5.5.
[Epic Developer Community Forums, Nanite Skeletal Mesh in UE5.5](https://forums.unrealengine.com/t/nanite-skeletal-mesh-in-unreal-engine-5-5-main/1792367)

CITED: the Animation Budget Allocator "determines a fixed budget that can be
adjusted on a per-platform basis in milliseconds of work to perform on the game
thread", with a default of `a.Budget.BudgetMs=1.0`, and it throttles each
component's tick rate by significance, evaluating the significant ones fully
and skipping frames on the rest. Benchmarks show "noticeable degradation beyond
about 128 to 255 budgeted components".
[Epic, Animation Budget Allocator (via search summary; page egress-blocked)](https://dev.epicgames.com/documentation/unreal-engine/animation-budget-allocator-in-unreal-engine),
[Unreal Directive, Animation Budget Allocator](https://unrealdirective.com/resources/engine-plugins/animationbudgetallocator/)

CONTRADICTION, recorded rather than resolved: a second summary of the same
documentation describes BudgetMs as a frame stride, "a value of one would mean
animation is being updated and ticking every frame, while a value of five would
mean every five frames it performs an update and tick". That is a description of
Update Rate Optimisation, not of a millisecond budget, and the two readings
cannot both be right. The primary page is blocked. HOLE: what
`a.Budget.BudgetMs=1.0` actually denominates is not established here, and it
matters, because under one reading Epic's default says a whole crowd's
animation should fit in one millisecond of game thread.

SINGLE-SNIPPET, do not lean on: one summary reported ABA taking 64 AI from
14.2 ms to 4.0 ms and 128 AI from 29.3 ms to 7.6 ms. It did not reproduce on a
second, differently worded search, and its host is egress-blocked. If true it
implies about 0.22 ms per character unbudgeted and about 0.06 ms budgeted,
which is internally consistent across both rows and roughly consistent with the
0.1 to 0.3 ms per pedestrian figure below. Both of those budgeted totals are
well above the 1.0 ms default, which is another reason the default's meaning
needs settling.

CITED, also single-source and consistent with the above: "A single pedestrian
NPC with full AI, skeletal mesh animation, and physics collision costs roughly
0.1-0.3ms per frame."
[StraySpark, Building Crowds and Traffic in UE5](https://www.strayspark.studio/blog/crowd-traffic-simulation-ue5-mass-ai)

CITED: Update Rate Optimizations is a per-component checkbox with per-mesh
tuning through `FAnimUpdateRateParameters`, a curve mapping screen size to
"evaluate every Nth tick". Master Pose Component shares one animation
evaluation across many meshes. Mass Entity is the ECS path for the ten-thousand
scale.
[Epic Developer Community Forums, Skeletal Mesh Crowd Performance](https://forums.unrealengine.com/t/skeletal-mesh-crowd-performance-and-efficiency-questions/98295),
[vrealmatic, Ways to achieve well performing crowds in UE5](https://vrealmatic.com/unreal-engine/crowds)

CITED, a tiered scheme reported as the standard approach: full Animation
Blueprint evaluation at 0 to 15 m, reduced-frequency blend tree updates at 15
to 40 m, a simplified animation sequence beyond 40 m. One developer target
quoted is 200 NPCs in front of the player at 60 fps, with the skeletal mesh and
the animation blueprint named as the bottleneck.
[80.lv, Character Behavior Programming and Game Optimization in UE5](https://80.lv/articles/character-behavior-programming-game-optimization-in-unreal-engine-5),
[Epic Developer Community Forums, Stable amount of NPC](https://forums.unrealengine.com/t/stable-amount-of-npc/448673)

HOLE: no authoritative figure exists for how many skeletal characters a
mid-range GPU renders at 60 fps. Two searches returned the same answer, that it
depends on LOD strategy, animation complexity and scene load, and no source
states a number with its conditions. Anyone quoting one is quoting a forum.

### 2.6 The City Sample, which is the closest published thing to our question

CITED: Epic's City Sample, the Matrix Awakens city with Mass AI crowds, Nanite,
Lumen, virtual shadow maps and MetaHumans, averages 25 fps at 1920x1080 on
cards "of the level of Radeon RX 6800 XT or GeForce RTX 3070", with the RX 6700
XT and RTX 3060 Ti holding a 25 fps MINIMUM at 1440p.
[GameGPU, The Matrix Awakens City Sample UE5.4 GPU and CPU test (via search summary; the site is egress-blocked)](https://en.gamegpu.com/test-gpu/action-fps-tps/the-matrix-awakens-city-sample-unreal-engine-5-4-test-gpu-cpu)

HOLE: the City Sample's crowd count did not come back from search, and the
benchmark's settings (preset, TSR ratio, Lumen mode) could not be read because
the host is blocked. Without the settings the 25 fps figure bounds the demo's
cost, not any particular configuration's.

CITED, the baseline spec quoted for UE5 games generally: "Ryzen 5 5600 /
Core i5-12400 or better, 16GB of RAM, an RTX 3060 / RX 6700 or better GPU, and
an NVMe SSD".
[EveZone, UE5 GPU Performance Guide 2025](https://evezone.evetech.co.za/performance-pulse/best-gpu-unreal-engine-5-nanite-lumen-2025/)

DERIVED, and it is worth stating flatly: `mesh-machine-report.txt` says Jafar's
machine is a Ryzen 5 5600X with 31.9 GB and an RX 6700. That is the published
FLOOR for UE5 games, component for component, not the middle of the range. Our
development machine and our minimum spec machine are the same machine.

### 2.7 The comparator, on the same hardware

CITED: Kingdom Come Deliverance 2 at high or ultra presets at 1080p averages
about 25 fps on an RTX 3060 and about 25 fps on an RX 6700 XT; at the Medium
preset the RX 6700 XT delivers well over 60 fps at native 1440p. Its
performance is attributed to being "built on an older but highly efficient game
engine".
[TechSpot, Kingdom Come: Deliverance II GPU Benchmark](https://www.techspot.com/review/2952-kingdom-come-deliverance-2-benchmark/),
[pcoptimizedsettings, KCD2 Settings for Low-end PC](https://pcoptimizedsettings.com/kingdom-come-deliverance-2-settings-for-low-end-pc-rtx-3060-3060-ti-4060/)

DERIVED, and it is the most useful single comparison in this topic: at maximum
settings on our own class of hardware, KCD2 costs 40 ms per frame, which is the
same figure as Epic's City Sample. The game whose visual bar we are chasing is
itself a 25 fps game when you ask it for everything, and a comfortable 60 fps
game when you ask it for slightly less.

Interpretation: the comparator reaches the bar without Lumen and without
Nanite, on CryEngine. That does not mean we should leave Unreal, a decision D16
closed on other evidence. It does mean that "photoreal" and "the full UE5
feature set switched on" are not the same commitment, and the second is not
required to reach the first.

---

## Part 3. The arithmetic

All of it shown, so that any step can be disputed without re-deriving the rest.

### 3.1 The GPU side, before a single person is drawn

At 1080p, taking Epic's own Lumen configurations and the Nanite figure:

| target | Lumen | Nanite | subtotal | frame | left for everything else |
|---|---|---|---|---|---|
| 60 fps | 4.0 ms | 4.5 ms | 8.5 ms | 16.67 ms | 8.17 ms |
| 30 fps | 8.0 ms | 4.5 ms | 12.5 ms | 33.33 ms | 20.83 ms |

"Everything else" is the base pass, virtual shadow maps, post processing, TSR,
UI, and the per-frame shadow invalidation of every animated person.

Caveat that must travel with this table: those Lumen and Nanite figures are
console figures, quoted for PS5-class hardware. The RX 6700 is roughly that
class in raw terms and worse in ray tracing, and a PC stack adds driver
overhead a console does not have. Treat the table as the optimistic case.

### 3.2 The CPU side, from our own measurements

Using this project's own 0.0746 ms per walker per frame, sim only, no animation:

| residents | sim cost | of a 60 fps frame | of a 30 fps frame |
|---|---|---|---|
| 30 | 2.24 ms | 13.4% | 6.7% |
| 50 | 3.73 ms | 22.4% | 11.2% |
| 65 (measured) | 4.85 ms | 29.1% | 14.6% |
| 100 | 7.46 ms | 44.8% | 22.4% |

Add the rest of the attributed game systems, 1.51 ms for sun, mix, traffic,
signals, population, body LOD and checks, and add animation. Under the ABA
default read as a millisecond budget, animation for the whole crowd is 1.0 ms.
Under the 0.1 to 0.3 ms per pedestrian figure with no budgeting, 50 residents
is 5 to 15 ms of animation on its own.

At phase 2's 50 residents that gives, on the game thread:

- with a working animation budget: 3.73 + 1.51 + 1.0 = about 6.2 ms
- without one, at the low end of the per-pedestrian figure: about 10.2 ms
- without one, at the high end: about 20.2 ms

The first fits a 60 fps frame with room for the render thread. The second fits
30 fps and not 60. The third fits nothing.

### 3.3 The reconciliation with Hitman, and why it is not a contradiction

Topic 3 recorded Hitman Absolution achieving "1200 character crowds while
running at 30fps on current-gen consoles" (2012 consoles), and closed by saying
"a thousand of ours would cost incomparably more, and topic 17 is where that
gets measured". This is that measurement, and the answer is in two parts.

Part 2.4 says a UE5 crowd invalidates shadow pages every frame, unavoidably.
Both figures are true and the gap between them is the whole lesson.
Absolution's crowd was a bespoke system that gave up per-person shadow
fidelity, per-person AI and per-person memory to buy the count. We are not
buying the count. We are buying the memory.

The split that follows from it, and it is the single most useful idea in this
topic:

**Simulated persons and rendered bodies are two different budgets and should
never have been one number.** They differ in cost, and more importantly they
differ in whether the cost can be spread over time.

The simulation costs 0.0746 ms per walker and nothing on the GPU, and it is
currently paying that EVERY FRAME for EVERY walker. CITED, `GameController.cs`
:1061: the `npcs` scope is an unstrided loop, `for (int i = _npcs.Count - 1; i
>= 0; i--) npc.Tick(Now)`, with no interval guard on the loop. Inside `Tick`
the interval guards that exist are on specific behaviours (an avoidance step
every 2.5 s at `NpcWalker.cs:1700`, a confrontation point every 25 s at :1716),
not on the steering or the perception report. So 4.85 ms over 65 walkers is a
FULL-RATE figure, and nothing about a schedule, a memory or a rumour requires
60 Hz. That headroom is real and unproven: it is the standard crowd answer
(Mass Entity, and Shadows of Doubt's pre-computed day with proximity-scaled
update rate from coverage-audit game 5), and no run in this project has
measured it.

The render can hold tens, and that budget does NOT have the same escape. A body
evaluated at a quarter rate reads as a body evaluated at a quarter rate, which
is what Update Rate Optimisation manages rather than eliminates, and the shadow
invalidation in 2.4 happens on every frame the animation updates.

Our moat lives entirely in the first budget, the one that can be spread. Our
visual bar lives entirely in the second, which cannot. A resident count that
does not say which one it means cannot gate anything.

### 3.4 The City Sample anchor, read honestly

Epic's own dense city runs at 25 fps, 40.0 ms per frame, at 1080p on a GPU
faster than ours. That is the cost of the full UE5 feature set applied to a
city block with crowds and traffic, on a demo nobody shipped.

Two readings, and the second is the one I believe:

1. Pessimistic: the thing we want costs 40 ms on better hardware than we have,
   so it is out of reach.
2. What the numbers actually support: the City Sample is a whole streaming city
   with thousands of vehicles and pedestrians at 1080p. `vignette-scene.json`
   is 42.0 metres of street with a 6.0 m carriageway and 2.0 m footways.
   Roadmap phase 2 asks for 30 to 50 residents on it. That is between two and
   three orders of magnitude less world, and the deliberately small footprint
   in the goal statement is not a compromise on the visual bar, it is the thing
   that PAYS for the visual bar.

The City Sample is therefore an upper bound on cost and a lower bound on
discipline, and not a prediction about LEDGER.

---

## Part 4. What could not be established

Named plainly rather than filled in.

1. **Which device rendered the 29.0 ms frame.** `verdict.txt` prints no adapter
   name and the runner machine has two adapters.
2. **What `a.Budget.BudgetMs=1.0` denominates.** Two secondary summaries of the
   same Epic page contradict each other and the page is blocked.
3. **The City Sample's crowd count and benchmark settings.** Host blocked.
4. **A defensible figure for skeletal characters at 60 fps on mid-range
   hardware.** No source states one with its conditions. Two searches agreed
   only that it depends.
5. **Whether the ABA benchmark figures (64 AI 14.2 to 4.0 ms; 128 AI 29.3 to
   7.6 ms) are real.** One snippet, one blocked host, no reproduction.
6. **Skinned renderers per body**, which is what turns 998,766 vertices into a
   per-character vertex budget. The denominator is not printed.
7. **Anything at all about this project's GPU cost in Unreal.** Not a hole in
   the research: a hole in the repository. There is no instrument.

---

## Part 5. Findings, separated from interpretation

### Findings (each one checked in this checkout on 2026-09-14)

F1. The engine is Unreal (D16, 2026-09-10) and the only frame-time instrument
in the project, `Core/FrameRate.cs`, has one live call site and it is in Unity.

F2. `ue-probe/` contains no frame-time instrument. `FrameStats.h` is an image
statistic file whose name suggests otherwise.

F3. The live verdict reports `game=6.36ms` of attributed game systems, of which
`npcsMs=4.85` is 76.3%, against a `render+rest=22.67ms` residue that is not a
measurement.

F4. `gameBudget=12ms` is a regression ratchet at roughly two times measured,
not a performance target, and says so.

F5. Three source comments assert the CI runner has no GPU. They date from
2026-07-26 and 2026-08-03; the builds moved to Jafar's PC on 2026-08-22; the
sim runs with `-force-d3d11` and no `-nographics` at 1280x720.

F6. Nothing prints the graphics device name, so the 29.0 ms frame cannot be
attributed to hardware or to software rasterisation.

F7. No committed frame shows a person walking on the Unreal street. The 65 is a
headless simulation count.

F7b. The `npcs` scope ticks every walker every frame with no stride, so
0.0746 ms per walker is a full-rate cost and not a floor.

F8. Phase 1 gates on "frame budget at target resident count" and neither number
exists in this checkout. D8, the visual bar, names no frame rate.

F9. `Detail.CostIndex`'s weights are a Unity lighting cost model and do not
port; its three distances and its crowd-fraction argument do.

F10. Epic's published figures put Lumen at 4 ms (60 fps config) or 8 ms (30 fps
config) and Nanite at 4.5 ms, at 1080p, on console-class hardware.

F11. A skeletal mesh casting a virtual shadow map invalidates cached pages
every frame it animates, unavoidably for crowd NPCs.

F12. Epic's City Sample averages 25 fps at 1080p on an RX 6800 XT or RTX 3070,
both faster than the RX 6700 in this project's only machine report.

F13. The published baseline spec for UE5 games is a Ryzen 5 5600 with an RTX
3060 or RX 6700. That is Jafar's machine, component for component.

F14. KCD2 on an RX 6700 XT runs at about 25 fps at high or ultra at 1080p and
well over 60 fps at Medium at 1440p, on an engine that uses neither Lumen nor
Nanite.

### Interpretation (mine, arguable)

I1. The most valuable thing this topic can produce is not a budget. It is the
observation that a budget cannot be set because the instrument does not exist,
and that the instrument is small: a `stat unit` equivalent in the probe's
verdict, three keys, plus a device name.

I2. The single-number resident count in phase 1's gate is the wrong shape. Two
numbers, simulated persons and rendered bodies, would gate the two things that
actually cost differently, and the moat sits entirely in the cheap one.

I3. 60 fps is not obviously the right target for this game. The photoreal bar,
Lumen's cost, and the fact that our development machine is the published
minimum spec all point at 30 fps at 1080p as the honest first target, with 60
as a preset that gives things up. Section 2.7 shows the named comparator makes
exactly that trade on exactly our hardware. This is a decision, not a finding,
which is why it appears in the summary as a question.

I4. The decayed no-GPU comments are more interesting than they look. If the
runner has been rendering on an RX 6700 since 22 August, then this project has
three weeks of real frame times on target hardware that it has been discounting
in three separate files, and the cheapest measurement on the board is the one
that tells us which world we are in.

I5. The 42-metre street is the frame budget. Every argument in this topic that
ends well ends there.
