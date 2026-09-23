# Baseline features: the full checklist

STATUS: SPEC (research delivery). Branch `research/baseline-features`.
Written 2026-09-23. Audited against [BRIEF.md](./BRIEF.md), written first.

NOTHING HERE IS AN INSTRUCTION. Nothing is proposed into the game's list.

## 0. Method and sourcing

Every "our build" cell was produced by a command run against the repository this
session. Nothing in the status column is recalled.

The Unreal side is `ue-probe/`: 57 files, 19,922 lines across its headers and
sources. Counts below come from case-insensitive greps over
`ue-probe/Source/` and `ue-probe/Config/`.

Unreal capability was checked against `dev.epicgames.com`, which is reachable.
Three pages were confirmed to exist with their titles and descriptions:
**Spatialization Overview** ("An overview of spatialization in Unreal Engine"),
**Control Rig** ("Rig and Animate characters in real-time using Control Rig")
and **Nanite Virtualized Geometry Overview**. Their bodies did not extract from
Epic's page format, so those three are CITED for existence and not for detail.
Every other Unreal-capability cell is ASSUMED from general knowledge and marked
so; none of them should be used to size work without a check.

AN INSTRUMENT FAULT OF MINE, recorded because the rules require it. My first
capability sweep used `grep -E` with BRE-style escaped pipes (`"Audio\|Sound"`),
which searches for the literal text `Audio|Sound`. It returned zero files for
all seven probes, which I nearly wrote down as seven findings. A control grep
for terms I knew were present exposed it. The corrected sweep is what this file
reports.

## 1. The finding that reorganises the whole checklist

**The question "does our Unreal build have it" has almost one answer, and the
answer is more useful than a column of No.**

`ue-probe` is not a game build with features missing from it. It is a street
photography rig and a walk test. Measured:

| probe | files in `ue-probe` |
|---|---|
| any audio playback (`PlaySound`, `UAudioComponent`, `USoundCue`, `USoundWave`) | **0 hits** |
| `skeletal` | **0** |
| `anim` | **0** |
| `aicontroller` | **0** |
| `navmesh` | **0** |
| `widget` | **0** |
| `niagara`, `particle` | **0**, **0** |
| `timeofday` / "time of day" | **0** |
| `physics` | 1 |

What it does have, from `LedgerCharacter.h` read in full: an `ACharacter` with a
`USpringArmComponent` and `UCameraComponent`, two axes of movement and two of
mouse look, and its own comment says "no jump, no crouch, no interact" and "this
capsule carries no visible mesh". `VignetteShot.cpp` spawns 593 street pieces
and four `ADirectionalLight`s. `WalkProbe` drives a scripted route to capture a
clip and frames.

**So the player character is an invisible capsule walking in silence through a
street with no people in it.** Neither feature Jafar found by accident is an
oversight on top of a populated build. There is nobody to turn a head, and there
is no audio subsystem to position a sound in.

**And the counterpart is the sharpest sentence in this audit.** The same repo
models sound in detail for the simulation: `ue-probe/Source/LedgerProbe/Public/Perception.h`
carries `WallAttenuation = 22.0` and a loudness-to-distance rule ported from
`Perception.cs`, so the game computes who can hear what through which wall.
**We simulate hearing and we produce no sound.**

## 2. Stage names, corrected

The brief asks for the stage of `ROADMAP.md`: "presentable, the playable slice,
or later". Measured: there is no `ROADMAP.md`, and the words "presentable" and
"playable slice" appear nowhere in `ledger-v2/`, `production/` or
`game-design/`. The live plan is `ledger-v2/respec/roadmap-v2.md` and it runs
phases R and 0 to 6.

Mapping used below, stated so it can be rejected:

- **PRESENTABLE = Phase 2**, "A street that lives: one street at the visual bar;
  kit and decal density; moving faces; live voice loop".
- **SLICE = Phase 3**, "The town: full Phase A scope; interior tiers; economy
  and cash; factions; narrative v2".
- **LATER = Phase 4 and beyond** (fists, then region and driving).

## 3. The checklist

Status: **N** none in the build, **P** partial, **Y** present. Unreal: **S**
shipped and documented, **W** shipped but needs assets or wiring, **B** build it
yourself. Notice: minutes into a first session before a player would register it
missing.

### 3.1 How characters move and look

| feature | ours | Unreal | stage | notice |
|---|---|---|---|---|
| A visible player body at all | **N** (capsule, no mesh, by its own comment) | W | PRESENTABLE | 0 min |
| Your own shadow in third person | **N** | S | PRESENTABLE | 1 min |
| Walk and look | **Y** | S | done | n/a |
| Idle variety | **N** (no anim) | W | PRESENTABLE | 3 min |
| Eye contact and head turn toward you | **N** | S, Control Rig (CITED for existence) | PRESENTABLE | 2 min |
| Feet that sit on stairs and slopes | **N** | S, Control Rig foot IK (ASSUMED) | PRESENTABLE | 4 min |
| Turning on the spot | **N** | W (anim asset) | PRESENTABLE | 3 min |
| Reacting when bumped | **N** | B | SLICE | 5 min |
| Sitting, leaning, carrying, working poses | **N** | W | SLICE | 6 min |
| Ragdoll on collapse | **N** | S (ASSUMED) | LATER (Phase 4) | n/a until combat |

### 3.2 Sound

Every row here is **N**, because the build plays no audio at all.

| feature | ours | Unreal | stage | notice |
|---|---|---|---|---|
| Any sound whatsoever | **N** | S | PRESENTABLE | 0 min |
| Positional sound from its source | **N** | S, Spatialization (CITED) | PRESENTABLE | 0 min |
| Falloff with distance | **N** | S, attenuation (ASSUMED) | PRESENTABLE | 1 min |
| Muffling through walls (occlusion) | **N** | S, attenuation occlusion (ASSUMED) | SLICE | 5 min |
| Reverb that depends on the space | **N** | S, audio volumes and submixes (ASSUMED) | SLICE | 6 min |
| Footsteps that change with the surface | **N** | W, physical materials plus anim notifies (ASSUMED) | PRESENTABLE | 1 min |
| Background ambience | **N** | W | PRESENTABLE | 1 min |
| Dialogue ducking other sound | **N** | S, submix ducking (ASSUMED) | SLICE | 8 min |
| Wind, rain and weather sound | **N** | W | PRESENTABLE | 2 min |

NOTE, and it is the one place this project is ahead rather than behind: the
hearing model that decides who perceives a sound already exists, is ported to
C++ and is golden-tested (`CoreGolden.h` reads `WallAttenuation` back). The
audio work is output, not modelling, and the two should not be confused when
this becomes a queue item.

### 3.3 The camera

| feature | ours | Unreal | stage | notice |
|---|---|---|---|---|
| Camera does not pass through walls | **Y**, `bDoCollisionTest = true` set explicitly at `LedgerCharacter.cpp:45` | S | done | n/a |
| Smoothing and lag | **N**, no camera lag is set, so the component default of off applies | S | PRESENTABLE | 3 min |
| Field of view, and a slider for it | **N** for the slider | S | SLICE | 10 min |
| Camera shake and impact feedback | **N** | S (ASSUMED) | LATER | n/a |

Read this session rather than inferred from the component being present:
`CameraBoom->TargetArmLength = 350.0f`, `bUsePawnControlRotation = true` on the
boom and false on the camera, and `bDoCollisionTest = true` with its own comment
saying the value is named rather than left to the default. So the one camera
row a player would notice in the first minutes is already correct, and the gap
is smoothing rather than collision.

### 3.4 How people behave around you

Every row is **N**: there is no AI, no navigation mesh and no NPC in the Unreal
build.

| feature | ours | Unreal | stage | notice |
|---|---|---|---|---|
| Anybody else in the street at all | **N** | W | PRESENTABLE | 0 min |
| Walking around you rather than into you | **N** | S, Detour Crowd (ASSUMED) | PRESENTABLE | 1 min |
| Reacting to you coming close | **N** | B (our own rules) | PRESENTABLE | 2 min |
| Reacting to a noise | **N** | B, and the Core model already exists | SLICE | 6 min |
| Talking among themselves | **N** in Unreal; the simulation has it | B | SLICE | 4 min |
| Using doors | **N** | W | SLICE | 7 min |
| Queueing, waiting, giving way | **N** | B | SLICE | 8 min |

### 3.5 The world

| feature | ours | Unreal | stage | notice |
|---|---|---|---|---|
| Time of day | **N** (0 hits) | W, no built-in cycle (ASSUMED) | PRESENTABLE | 4 min |
| Weather, and weather changing what people do | **N** | B | SLICE | 6 min |
| Objects that move when pushed | **N** (1 physics mention) | S | SLICE | 5 min |
| Detail appearing without visible popping | **P** | S, Nanite (CITED for existence) | PRESENTABLE | 3 min |
| Puddles, wet surfaces, water response | **P** as material only | W | PRESENTABLE | 4 min |
| Wind in cloth and foliage | **N** | S (ASSUMED) | SLICE | 7 min |
| Interiors you can enter | **N** | W | SLICE | 10 min |

### 3.6 What the player is told

| feature | ours | Unreal | stage | notice |
|---|---|---|---|---|
| Any UI at all (`widget`: 0 files) | **N** | S, UMG | PRESENTABLE | 1 min |
| Interaction prompts | **N** | W | PRESENTABLE | 2 min |
| Subtitles | **N** | S (ASSUMED) | PRESENTABLE | 2 min |
| Feedback that something happened | **N** | W | PRESENTABLE | 3 min |
| Pause | **N** | S | PRESENTABLE | 1 min |
| Settings: sensitivity, brightness, volume | **N** | W | SLICE | 10 min |
| Save and load | **N** in Unreal; `SaveCodec.cs` exists in Core | W | SLICE | n/a in 10 min |

## 4. What the brief's list was missing

Asked for, and these are the ones I would add:

1. **Pause, save, load and autosave.** Older than the PS3 era and absent from
   every row above.
2. **A settings screen**, including mouse sensitivity, invert, volume sliders
   and brightness. The first thing many players open.
3. **Gamepad support and rumble.** Our input is bound directly to hardware keys
   by `LedgerCharacter`'s own comment, so a controller is not merely unbound, it
   is unconsidered.
4. **Accessibility floor**: subtitle size and background, colourblind-safe
   critical colours, a motion and camera-shake toggle. Since 2009 these moved
   from courtesy to expectation.
5. **Loading without hitching**, and a loading screen that is not a freeze.
6. **Your own shadow**, listed in 3.1 because in third person its absence reads
   as the character not being in the world.
7. **Collision that feels solid**: not walking through a wall or a person. The
   walk probe already judges "is collision real", so this one has an instrument.
8. **A death or failure state that resolves**, rather than a stuck player.

## 5. Ranked by how fast a player notices

Combining the notice column across every section, missing only:

1. Silence (0 min)
2. No people in the street (0 min)
3. No visible body (0 min)
4. No footsteps (1 min)
5. No ambience (1 min)
6. Nobody avoids you (1 min)
7. No UI or pause (1 min)
8. No head turn or eye contact (2 min)
9. No prompts or subtitles (2 min)
10. Feet not planted on slopes and stairs (4 min)
11. No time of day (4 min)
12. Nothing moves when pushed (5 min)

## 6. What could not be established

1. **Unreal's out-of-box behaviour for every row marked ASSUMED.** Three pages
   were confirmed by title; the rest is general knowledge and should be checked
   before any of it is used to size work.
2. **Whether the reference games do these things the way I think they do.** No
   game was played and no per-game source was read this session; the feature
   list is derived from the brief's own enumeration plus section 4's additions,
   not from a survey of the nine titles named.
3. **Anything about the C# Game layer's own presentation.** This audit looked at
   `ue-probe`. `ledger/Assets/Scripts/Game/` has 89 files and may contain
   presentation logic that a future Unreal port would inherit.
4. **Frame cost of any of it.** Nothing here is a budget.
