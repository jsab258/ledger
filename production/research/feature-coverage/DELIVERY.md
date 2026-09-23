# Feature coverage: what the plan holds, and what it does not

STATUS: SPEC (research delivery). Branch `research/feature-coverage`. The
commission is [BRIEF.md](./BRIEF.md) beside this file, written before the work
began. The one-page reading is [SUMMARY.md](./SUMMARY.md).

This audits THE PLAN, not the build. Its predecessor,
[baseline-features](../baseline-features/SUMMARY.md), audited the build and
found that on the Unreal side the floor had not been laid. The question here is
different: is each feature WRITTEN DOWN somewhere, so it cannot be forgotten.
An entry typed `absent` in the systems inventory counts as IN THE PLAN. It is
written down with a phase against it. That is the whole test.

## 0. The answer, in numbers

| | count | of |
|---|---|---|
| Expected features merged from the four lenses | **179** | |
| In the plan | **90** | 179 |
| Partly in the plan | **42** | 179 |
| Absent from the plan | **47** | 179 |
| Of the 89 not properly held, noticed inside thirty minutes | **65** | 89 |
| Ruled out by D24 | **0** | 179 |

Plan sources searched: **73 files**. `ROADMAP.md`, `canon.md`, `DECISIONS.md`,
`legacy/studio-v2/production/systems-inventory.json` (111 systems), and 69
research files, being the 66 under `production/research/` on `main` plus the
three files of the baseline-features delivery, which is still on its own branch.

## 1. Four things about the plan that have to be said before the checklist

**1. D24 rules nothing out.** The brief offered "or that D24 rules it out" as a
verdict. It was never available. D24's own words: "That is a spend rule, not a
ban. Driving, fighting and trade may exist and must not look broken; they may
not take budget from the four things that are the game." Of the 179 items here,
D24 rules out zero and caps the budget of about six (firearms, driving and
traffic, trade, swimming, combat depth, the region). Every absent item below
therefore carries a stage, not an exemption.

**2. The inventory's phase numbers do not point at ROADMAP's stages.** The
inventory says `phase names a row in ledger-v2/respec/roadmap-v2.md`. That file
is now `legacy/studio-v2/respec/roadmap-v2.md` and its phases R and 0 to 6 are
not `ROADMAP.md`'s six stages, which Jafar ruled on 2026-09-14 and which were
brought back to the root on 2026-09-22. Every stage in the tables below is
ROADMAP's, assigned here; where it disagrees with an inventory phase, say so and
the inventory is the stale one.

**3. "Around two hundred systems" is 111.** The inventory holds 111 entries in
five areas: 30 exists, 41 partial, 36 absent, 4 ruled-out. Forty-two of them are
in the area `what the player touches`. The figure matters because the gap this
commission is about is not a gap in a two-hundred-row list; it is a gap in a
111-row list whose rows are often one word wide.

**4. The two features found by accident are STILL not in the plan.** Neither
`head turn` nor `positional sound` nor `look`, `gaze`, `spatial` or `bump`
appears in the name of any of the 111 systems, in `ROADMAP.md`, in `canon.md` or
in `DECISIONS.md`. Both live in exactly one place: the baseline-features
delivery, on a branch that has not been merged. The audit that found them has
not yet put them anywhere a future session would read.

## 2. How each lens was built, and what it cost

Claim labels: CITED (from a source read this session), CITED-SUMMARY (from a
source describing another source), DERIVED (constructed from a cited structure),
ASSUMED (general knowledge, marked so it can be rejected), HOLE (wanted and not
obtained).

### Lens 1: who builds it

ASKED FOR: the full credits of GTA V, Red Dead Redemption 2 and Kingdom Come
Deliverance 2, and every department in them.

WHAT HAPPENED: `www.mobygames.com`, the credits database, is refused by this
environment's proxy, as are `www.giantbomb.com`, `store.steampowered.com` and
`www.igdb.com`. No credits roll was reachable. HOLE, and it is the weakest
half of this delivery's sourcing after lens 4.

WHAT WAS BUILT INSTEAD, by construction rather than by recall:

- The discipline list in Wikipedia's `Video game development`, CITED: producer,
  publisher, designer (with writer), artist (2D and 3D), programmer, level
  designer, sound engineer, tester, and the programmer's own ten sub-disciplines
  named in that article: physics, AI, graphics, sound, gameplay, scripting, UI,
  input processing, network communications and game tools.
- Three independent craft taxonomies the industry votes on, CITED: the BAFTA
  Games Awards 2025 categories (Animation, Artistic Achievement, Audio
  Achievement, Game Design, Music, Narrative, Performer in a Leading Role,
  Performer in a Supporting Role, Technical Achievement); the Game Developers
  Choice Awards craft categories (Audio, Design, Narrative, Technology, Visual
  Art, Innovation); and the D.I.C.E. craft categories (Story, Character, Audio
  Design, Game Direction, Game Design, Animation, Art Direction, Technical,
  Original Music Composition).
- The development sections of the three games' own articles, CITED: Rockstar
  co-opting all its studios into one 1,600-person team for RDR2, recording
  sessions from 2013, three kinds of score (narrative, interactive,
  environmental), 110 musicians, a companion app.

The mapping from department to player-facing feature is DERIVED.

### Lens 2: what runs every frame

ASKED FOR: Unreal's own module list and the standard texts on engine
architecture.

WHAT HAPPENED: this one worked, and better than the previous delivery managed.
baseline-features reported that Epic's site would not give up page bodies. It
does: the body of a documentation page is a JSON document inside the
`serverApp-state` blob, under a key whose `b` object carries `blocks`, and for
the API reference the whole page is one `markdown` block under `content_html`.
That is a correction to a limit stated in a delivered document, and it is how
the list below was read.

CITED, from `dev.epicgames.com/documentation/en-us/unreal-engine/API`, the
Unreal Engine C++ API Reference, read this session: **1,869 modules** in four
categories. Developer 109, Editor 139, **Runtime 246**, Plugins 1,375. Epic's
own words for the Runtime category: "contains functionality necessary to run
Unreal Engine. These modules are compiled for every type of build configuration
and build target." That is the list of what runs every frame, from the engine
rather than from memory.

The 246 runtime modules and the 1,375 plugin modules were grouped into the
eighteen families below. The grouping is DERIVED; every module name in it is
CITED.

| family | modules it was built from |
|---|---|
| Rendering | Renderer, RenderCore, RHI, RHICore, D3D12RHI, VulkanRHI, OpenGLDrv, MaterialShaderQualitySettings, SynthBenchmark, ImageCore, ImageWrapper, OpenColorIOWrapper |
| Animation | AnimationCore, AnimGraphRuntime, SkeletalMeshDescription, Constraints, ControlRig, IKRig, FullBodyIK, PBIK, PoseSearch, BlendStack, MotionWarping, ContextualAnimation, Chooser, AnimationBudgetAllocator, AnimationSharing, Mover, Locomotor, MLDeformerFramework |
| Faces and people | MetaHumanCharacter, MetaHumanGenerator, MetaHumanCrowd, MetaHumanSpeech2Face, SpeechAnimationSolver, FacialAnimation, RigLogicModule, DNACalibModule, HairStrandsCore, ChaosCloth, ChaosClothAsset, SkeletalMerging, CustomizableObject |
| Physics | Chaos, ChaosCore, ChaosSolverEngine, PhysicsCore, PhysicsControl, ChaosVehiclesEngine, GeometryCollectionEngine, FieldSystemEngine, Buoyancy, CableComponent, DynamicWind |
| Audio | AudioMixer, AudioMixerCore, AudioExtensions, SignalProcessing, SoundFieldRendering, Spatialization, AudioGameplayVolume, AudioModulation, MetasoundEngine, MetasoundStandardNodes, SoundScape, SoundUtilities, SteamAudio, ResonanceAudio, MicrosoftSpatialSound, SubtitlesAndClosedCaptions, Voice, VoiceChat, AudioSynesthesia, AudioInsights |
| AI and navigation | AIModule, NavigationSystem, Navmesh, NavCorridor, ZoneGraph, ZoneGraphAnnotations, SmartObjectsModule, StateTreeModule, GameplayBehaviorsModule, HTNPlanner, MassEntity, MassAIBehavior, MassCrowd, MassNavigation, MassMovement, MassLOD, MassRepresentation, EnvironmentQueryEditor, GameplayTasks, LearningAgents |
| Input | InputCore, InputDevice, EnhancedInput, CommonInput, RawInput, GameInputBase, SteamController, StylusInput, ApplicationCore |
| Camera | GameplayCameras, EngineCameras, CinematicCamera, CineCameraRigs, CameraShakePreviewer, LensComponent |
| Interface | Slate, SlateCore, UMG, CommonUI, AdvancedWidgets, ModelViewViewModel, UIFramework, WidgetCarousel, GameMenuBuilder, SlateIMInGame, ScreenReader, SlateScreenReader, TextToSpeech |
| Save and serialization | Serialization, Json, JsonUtilities, SaveGameNetworkReplayStreaming, LevelStreamingPersistence, SandboxFile, PlainProps |
| Streaming and loading | PakFile, IoStoreOnDemandCore, StreamingFile, StreamingPauseRendering, AssetRegistry, InstallBundleManager, BuildPatchServices, ChunkDownloader, MoviePlayer, PreLoadScreen, CinematicPrestreaming, FastGeoStreaming, WorldPartitionHLODUtilities |
| Localisation | Localization, LocalizationService, LocalizableMessage, PortableObjectFileDataSource, Text3D |
| Platform services | CoreOnline, OnlineSubsystem, OnlineSubsystemSteam, OnlineServicesInterface, HTTP, Sockets, Networking, XMPP, LauncherPlatform, PlatformDLC, PlatformCrypto, GooglePAD |
| Effects | Niagara, NiagaraCore, NiagaraFluids, NiagaraShader, SurfaceEffects, GeometryCache |
| World and time | DaySequence, SunPosition, CelestialVault, Water, WaterAdvanced, Landscape, Landmass, Foliage, ProceduralVegetation, PCG, VirtualHeightfieldMesh, GeoReferencing, InstancedActors |
| Media | Media, MediaAssets, MediaUtils, MediaPlate, ElectraPlayerRuntime, ElectraSubtitles, WebMMedia, BinkMediaPlayer, AVEncoder, WebBrowser |
| Telemetry and crash | CrashReportCore, Analytics, AnalyticsET, StudioTelemetry, RuntimeTelemetry, HardwareSurvey, PerfCounters, MemoryUsageQueries, Instrumentation, TraceLog |
| Scale and budget | SignificanceManager, AnimationBudgetAllocator, MassLOD, WorldMetricsCore, Reflex, AutomatedPerfTesting |

Note three modules by name, because they are the answer to items the plan does
not hold: `SubtitlesAndClosedCaptions`, `ScreenReader` and `TextToSpeech` ship
with the engine. So does `Spatialization`. The absences below are not
engine absences.

### Lens 3: moment by moment

ASKED FOR: the first thirty minutes of a modern open-world game, second by
second, from launching it to quitting it.

WHAT IT IS: a walkthrough constructed from the fixed order every PC game of this
kind imposes, which is DERIVED, with four documented anchors, CITED from
Wikipedia's `Loading screen`, `Saved game`, `HUD (video games)` and
`Video game development`. I did not play a game to write it and could not have:
this environment has no game and no GPU. It is marked DERIVED throughout and it
is the lens most open to challenge. Its value is not authority; it is ORDER. It
is the only lens that produces a clock, and the clock is what ranks the list.

The walk: launcher and splash, legal and logo screens, a first-run hardware
detection and a default preset, the title screen with Continue and New Game,
the settings screens (display, audio, controls, language, accessibility), a
content and photosensitivity warning, a difficulty or mode choice, the loading
screen, the opening scene with its subtitles and its skip, the handover of
control, the first walk with its footsteps and its ambience and the people who
move out of the way, the first prompt and the first interaction, the first
objective and how the player learns it, the first conversation, the first
failure, the weather changing, the pause, the map, the save, a settings change
mid-session, the quit, and the relaunch that has to put everything back.

### Lens 4: what the industry already checks

ASKED FOR: the Xbox Accessibility Guidelines and the Game Accessibility
Guidelines, plus platform certification requirements.

WHAT HAPPENED, and it should be read before any number from this lens is used:
**both named sources are refused by this environment's proxy.**
`gameaccessibilityguidelines.com` and `learn.microsoft.com` (which hosts the
Xbox Accessibility Guidelines) both fail to connect, as do
`partner.steamgames.com`, `developer.playstation.com`, `accessible.games`,
`caniplaythat.com`, `www.w3.org` and `web.archive.org`. Wikipedia has no article
on Lotcheck or on console certification. NO CERTIFICATION CHECKLIST AND NO
ACCESSIBILITY GUIDELINE WAS READ THIS SESSION. That is a HOLE and it is
the largest one in this delivery.

WHAT WAS BUILT INSTEAD: Wikipedia's `Game accessibility`, CITED, which gives the
structure rather than the checklist. Its three barrier classes (sensory, motor,
cognitive) and six strategies (enhance stimuli, replace stimuli, replace input,
reduce input, reduce stimuli, reduce time constraints) are the frame; the
individual items in section R below are DERIVED from that frame and are ASSUMED
where they name a specific affordance. The same article carries three CITED
facts worth having: the CVAA has applied to games released since 1 January 2019
and covers in-game communication and the interface used to reach it; The Last of
Us Part II shipped over sixty accessibility settings and won the first
Innovation in Accessibility award; and the ESA's Accessibility Games Initiative
(2025) defines **24 tags** for product labelling. Those 24 tags are exactly the
checklist this lens wanted. THEIR CONTENTS WERE NOT OBTAINED. Anybody with an
unblocked browser can close this hole in ten minutes, and should.

## 3. How the comparison was made

A term search over the 73 plan files, one regular expression per item, run twice
with the expressions tightened between runs after the first pass produced false
positives ("equity" matching `quit`, photo captions matching `caption`,
"schedule resolution" matching `resolution`, `gdcvault.com` matching `vault`).

The instrument carries two controls, both run on every pass, because a search
that finds nothing and a search that is broken look identical: `gossip`, which
must hit, returned 52 hits across 4 of the 5 sources; a nonce token that exists
nowhere returned 0 in all 5. It also has a known limit: it reads line by line,
so a feature named across a line break is invisible to it.

NO VERDICT BELOW WAS SET BY A COUNT. Every hit was read, and several verdicts
moved on reading: save integrity went from absent to partly because the
inventory's save entry names a quarantine and a SaveChaos harness that no search
term of mine would have found; the objective row stayed absent because the word
`objective` genuinely appears zero times in all 73 files, which I disbelieved
and checked separately.

## 4. The checklist

**Plan**: **Y** in the plan, named in its own right with a home. **P** partly:
named only inside a coarser entry, or only in a research delivery with no place
in ROADMAP or the inventory. **N** absent: nothing in the 73 files names it.

**Lenses**: 1 who builds it, 2 what runs every frame, 3 moment by moment, 4 what
the industry already checks.

**Notice**: minutes into a first session before a player would register it
missing. `later` means a player would not notice inside a session; it still
matters to somebody.

### 4.1 Boot and the first screens

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| A1 | Splash and logo screens, legal notices | 1,3,4 | **N** | nothing in ROADMAP, canon, DECISIONS or the 111 inventory entries names a boot sequence | stage 4 | 0 min |
| A2 | First-run hardware detection and default quality preset | 2,3 | **N** | no first-run detection anywhere; the hardware floor tile is the minimum machine, not a detector | stage 4 | 1 min |
| A3 | Title screen with Continue, New Game, Load, Settings, Quit | 2,3 | **Y** | inventory `menus` (exists, ph6) and `new game` (exists, ph6); ROADMAP stage 4 | stage 4 |  |
| A4 | Build version visible to the player | 1,3,4 | **N** | no version string named anywhere in the plan | past the sixth stage | 1 min |
| A5 | Loading screen with progress, and no infinite load | 2,3,4 | **Y** | inventory `loading and streaming` (partial, ph5) | stage 5 |  |
| A6 | Quit confirmation and a clean exit | 3,4 | **P** | inside the coarse `menus` tile; no line says a quit confirmation exists | stage 4 | 30 min |
| A7 | Continue from the last save on relaunch | 3 | **Y** | inventory `new game`: "New game and Continue are both on the front screen" | stage 4 |  |
| A8 | Photosensitivity and content warnings at boot | 1,4 | **N** | canon's content rule is a taste rule, not a player-facing warning screen | stage 4 | 0 min |
| A9 | Credits and third-party attributions | 1,4 | **Y** | inventory `credits and attributions` (partial, ph6); DECISIONS names THIRD-PARTY.md | stage 4 |  |

### 4.2 Settings

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| B1 | Display settings: resolution, window mode, vsync, frame cap | 2,3 | **P** | inventory `graphics settings` names two sliders, a preset and render scale; resolution, window mode, vsync and a frame cap are not named | stage 4 | 1 min |
| B2 | Brightness or gamma calibration | 2,3,4 | **P** | named only in the baseline-features delivery's settings row | stage 4 | 2 min |
| B3 | Graphics quality options and presets | 2,3 | **Y** | inventory `graphics settings including the local-LLM toggle` (partial, ph6) | stage 4 |  |
| B4 | Upscaling or resolution scale | 2 | **P** | render scale 100/75/55 is named; no temporal upscaler is | stage 4 | 2 min |
| B5 | Audio sliders per category and output device | 2,3,4 | **P** | inventory `audio mix` (exists) is the bus model, not a settings surface; sliders named only in baseline-features | stage 4 | 2 min |
| B6 | Subtitle options: size, background, speaker names | 2,3,4 | **P** | inventory `subtitles` (exists) carries a 0/1/2 setting and `accessibility` a text scale; size, background and speaker name are not named | stage 4 | 12 min |
| B7 | Control remapping for keyboard and gamepad | 2,3,4 | **Y** | inventory `controls`: nine rebindable actions, and `accessibility` names pad remapping as the gap | stage 4 |  |
| B8 | Sensitivity, invert axes, dead zones | 2,3 | **P** | named only in the baseline-features settings row | stage 4 | 2 min |
| B9 | Language selection, text and speech separately | 2,3,4 | **Y** | inventory `text localisation` (absent, ph6) | past the sixth stage |  |
| B10 | Apply and revert countdown for display changes | 3 | **N** | nothing names how a display change is applied or reverted | stage 4 | 1 min |
| B11 | Settings persist across sessions | 3,4 | **Y** | inventory `settings`: "defaults survive a round trip" | stage 4 |  |
| B12 | Field of view control | 2,3,4 | **P** | named only in the baseline-features camera row | stage 4 | 3 min |
| B13 | Camera shake, motion blur and depth of field toggles | 2,4 | **P** | `accessibility` names reduced motion as a gap; motion blur and depth of field toggles are not named | stage 4 | 3 min |
| B14 | Difficulty or assist options | 3,4 | **N** | no difficulty or assist option anywhere in the plan; whether this game has one is undecided | stage 4 | 1 min |
| B15 | HUD customisation or HUD off | 3,4 | **N** | the HUD tile does not say the HUD can be turned off or changed | stage 4 | 20 min |

### 4.3 Save and persistence

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| C1 | Manual save with named slots | 2,3 | **Y** | inventory `save and load` (exists, ph1): codec in Core, slots and quarantine in Game | stage 3 |  |
| C2 | Autosave with a visible indicator | 2,3,4 | **P** | inventory `failure states and autosave policy` has the policy; no indicator that a save is being written | stage 4 | 15 min |
| C3 | Save integrity: no corruption, storage-full handling | 2,4 | **P** | quarantine and the SaveChaos harness cover corruption; a full disk is not named | stage 4 | later |
| C4 | Load menu with timestamps, thumbnails and playtime | 3 | **N** | no load menu contents named: no timestamp, thumbnail or playtime | stage 4 | later |
| C5 | Cloud save | 2,4 | **N** | cloud save appears nowhere | past the sixth stage | later |
| C6 | World state surviving a save and reload | 2,3 | **Y** | canon's moat line on permanent memory; inventory `consequence persistence` | stage 3 |  |

### 4.4 Input

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| D1 | Keyboard and mouse | 2,3 | **Y** | inventory `controls` (exists, ph2) | stage 4 |  |
| D2 | Gamepad support and hot-swap | 2,3,4 | **Y** | inventory `gamepad` (absent, ph6): written down, unbuilt | stage 4 |  |
| D3 | Button prompts that match the device in hand | 2,3,4 | **N** | no device-aware prompt glyphs named; no prompt of any kind is named in the plan | stage 4 | 2 min |
| D4 | Controller disconnect pauses the game | 4 | **N** | controller disconnect is not named | past the sixth stage | later |
| D5 | Hold versus toggle for held inputs | 4 | **N** | hold versus toggle is not named | stage 4 | 6 min |
| D6 | Input latency inside a budget | 1,2 | **N** | the frame budget tile is frame time; the conversation latency budget is speech. Input latency is neither | stage 4 | 1 min |

### 4.5 Camera

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| E1 | Camera that does not pass through walls | 2,3 | **Y** | inventory `camera` (exists, ph2): third person, spring rig; baseline-features read the collision test on in the Unreal build | stage 2 |  |
| E2 | Camera smoothing and framing | 2,3 | **Y** | inventory `camera`: the spring rig IS the smoothing, though baseline-features found no lag set in Unreal | stage 2 |  |
| E3 | Camera behaviour in tight interiors | 2,3 | **N** | no line anywhere on what the camera does in a room the size of Mickey's front office | stage 5 | 25 min |
| E4 | Look sensitivity and acceleration | 2,3 | **P** | named only in the baseline-features settings row | stage 4 | 2 min |
| E5 | Photo mode | 1,2 | **Y** | inventory `photo mode` (absent, ph6) | past the sixth stage |  |
| E6 | Cinematic camera for conversation and cutscene | 1,2,3 | **Y** | inventory `dialogue staging` (absent, ph2) | stage 2 |  |

### 4.6 Interface

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| F1 | Interaction prompts | 2,3 | **P** | named only in baseline-features; the words prompt and press-to appear nowhere in ROADMAP, canon, DECISIONS or the inventory | stage 4 | 3 min |
| F2 | Objective or quest log | 1,3 | **P** | the Ledger is named and D37 rules it a notebook; a quest log or task list is named nowhere, which may be deliberate | stage 4 | 8 min |
| F3 | Map and compass | 3 | **Y** | inventory `map and minimap` (absent, ph3); ROADMAP and D20 rule the minimap out | stage 4 |  |
| F4 | Feedback when something happens | 3,4 | **Y** | inventory `HUD` (exists, ph2): clock, money, slot and the toast channel | stage 2 |  |
| F5 | Menus navigable by gamepad as well as mouse | 2,4 | **N** | menu navigation by pad is not named; the gamepad tile is about play, not menus | stage 4 | 1 min |
| F6 | Text scaling and safe area | 2,4 | **P** | text scale 80 to 150 is named; safe area is not | stage 4 | 12 min |
| F7 | Screen reader or menu narration | 2,4 | **N** | no screen reader and no menu narration; `accessibility` names an audio-description pass as missing, which is a different thing | stage 4 | 1 min |
| F8 | Inventory screen | 3 | **Y** | inventory `inventory` (partial, ph4) | stage 4 |  |
| F9 | A pause that actually pauses | 3,4 | **Y** | inventory `pause` (exists, ph6) | stage 4 |  |

### 4.7 Movement and the player's body

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| G1 | Walk, run and sprint with exertion | 2,3 | **Y** | inventory `sprinting and exertion outside a fight` (absent, ph2) | stage 2 |  |
| G2 | A visible player body and its shadow | 1,3 | **P** | `bodies and faces` covers residents; the player's own body and shadow are named only in baseline-features | stage 2 | 0 min |
| G3 | Turning on the spot, acceleration, stopping | 2,3 | **P** | named only in baseline-features; `bodies and faces` cites MotionMatch.cs with no caller | stage 2 | 2 min |
| G4 | Feet planted on stairs and slopes | 2,3 | **Y** | inventory `bodies and faces` cites Game/FootIk.cs as evidence | stage 2 |  |
| G5 | Collision with props and not getting stuck | 2,3 | **P** | named only in baseline-features | stage 2 | 4 min |
| G6 | Jump, vault and climb, or a decision not to | 3 | **N** | jump, vault, climb and mantle appear nowhere, although `burglary and lockpicking` implies getting in somehow | stage 3 | 2 min |
| G7 | Crouch and sneak | 3 | **P** | the four-rung concealment model and `disguise` exist; crouch and sneak as movement verbs are not named | stage 3 | 6 min |
| G8 | Swimming and water entry | 2,3 | **Y** | inventory `swimming` (absent, ph3) | stage 3 |  |

### 4.8 Animation, and how a person reads

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| H1 | Idle variety and fidgets | 1,3 | **Y** | ROADMAP's presentable checklist: "a handful of people stand or walk in the street, even if they only idle" | stage 1 |  |
| H2 | Head and eye look-at toward the player | 1,2,3 | **P** | THE FEATURE THAT STARTED THIS COMMISSION. Named only in the baseline-features delivery, which is on its own branch. No inventory entry name contains head, look or gaze | stage 2 | 2 min |
| H3 | Facial animation and lip sync | 1,2,3 | **Y** | ROADMAP stage 2: "a face that moves and a voice" | stage 2 |  |
| H4 | Reaction when bumped or shoved | 1,3 | **P** | named only in baseline-features; no inventory entry name contains bump | stage 2 | 5 min |
| H5 | Sitting, leaning, working poses at objects | 1,2,3 | **Y** | inventory `ambient street life beyond the crowd` (absent, ph2): deliveries, a shopkeeper sweeping, washing on a line | stage 2 |  |
| H6 | Ragdoll and physical hit reactions | 1,2 | **P** | `combat` and `injury and healing` are named; ragdoll and physical hit reactions are not | stage 6 | later |
| H7 | Cloth and hair movement | 1,2 | **N** | ROADMAP stage 2 rules clothing to be garment meshes on a shared skeleton; no cloth or hair movement is named anywhere | stage 2 | 6 min |
| H8 | Varied bodies, faces and clothing | 1,3 | **Y** | ROADMAP stage 2: varied bodies; inventory `bodies and faces` | stage 2 |  |
| H9 | Animation budget at crowd scale | 2 | **N** | the frame budget tile is the whole frame; no per-character animation budget or significance scheme is named | stage 2 | later |

### 4.9 Sound

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| I1 | Positional sound from its source | 2,3 | **P** | THE SECOND FEATURE THAT STARTED THIS COMMISSION. `sound in the Unreal build` (absent, ph2) is the tile it would live in; positional sound is named only in baseline-features | stage 2 | 0 min |
| I2 | Distance falloff | 2,3 | **P** | same tile; falloff named only in baseline-features | stage 2 | 1 min |
| I3 | Occlusion and muffling through walls | 2,3 | **P** | the moat's hearing model carries WallAttenuation = 22 dB; nothing says the PLAYER hears the muffling | stage 2 | 6 min |
| I4 | Reverb that depends on the space | 2,3 | **Y** | inventory `ambient beds and room tone` (partial, ph2) | stage 2 |  |
| I5 | Footsteps that change with the surface | 1,2,3 | **Y** | inventory `foley` (partial, ph2) | stage 2 |  |
| I6 | Ambient beds and background life | 1,2,3 | **Y** | ROADMAP stage 2: "foley and an ambient bed" | stage 2 |  |
| I7 | Weather and water sound | 1,2,3 | **P** | covered only by the coarse foley and ambient tiles; weather and water sound are not named separately in a port town | stage 2 | 2 min |
| I8 | Dialogue ducking and a dynamic mix | 1,2,3 | **P** | inventory `audio mix` (exists) has buses and a per-bus voice budget; ducking under dialogue is not named | stage 2 | 10 min |
| I9 | Music that responds to the game | 1,2,3 | **Y** | inventory `music` (partial, ph3) | stage 3 |  |
| I10 | Voice acting and casting consistency | 1,3 | **Y** | ROADMAP stage 3: people "who answer in their own cast voices"; inventory `voices` | stage 3 |  |
| I11 | Captions for non-speech sound | 2,4 | **Y** | inventory `subtitles`: setting 2 is speech and sounds | stage 2 |  |
| I12 | Mono audio output | 4 | **N** | mono output appears nowhere | stage 4 | 1 min |
| I13 | Visual indicator of off-screen sound | 4 | **N** | no visual indicator of a sound the player cannot see, in a game whose whole subject is who heard what | stage 4 | 8 min |

### 4.10 The world

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| J1 | Time of day | 2,3 | **Y** | inventory `light and the time of day` (exists, ph2) | stage 2 |  |
| J2 | Weather, and what it changes | 1,2,3 | **Y** | inventory `weather and wet streets` (partial, ph2) | stage 2 |  |
| J3 | Wet surfaces and puddles | 1,2 | **Y** | ROADMAP stage 1's order names wetness; D53 grime is the strategy | stage 1 |  |
| J4 | Street lighting at night | 2,3 | **Y** | inventory `street lighting at night` (absent, ph2) | stage 2 |  |
| J5 | Props that move when pushed | 2,3 | **N** | nothing in the plan says an object moves when the player walks into it | stage 2 | 3 min |
| J6 | Foliage and wind | 2,3 | **P** | asset-coverage records that no vegetation of any kind exists; no plan entry names foliage or wind | stage 2 | 2 min |
| J7 | Water and tide | 2 | **Y** | inventory `the tide and the water` (absent, ph3) | stage 3 |  |
| J8 | Doors that open, and people using them | 2,3 | **Y** | inventory `doors and who gets in` (exists, ph2) | stage 2 |  |
| J9 | Interiors that can be entered | 1,3 | **Y** | ROADMAP stage 5; inventory `interiors you can enter` (absent, ph2) | stage 5 |  |
| J10 | Traffic and parked vehicles | 1,3 | **Y** | inventory `traffic and vehicles` (exists) and `parked vehicles as street dressing` (absent, ph2) | stage 2 |  |
| J11 | Clutter that can be interacted with or broken | 2 | **P** | ROADMAP names density of clutter as a LOOK; nothing says a bin or a crate can be touched | stage 2 | 5 min |
| J12 | Litter, decals, wear and grime | 1 | **Y** | ROADMAP and D53: grime is the strategy, a surface carries its wear | stage 1 |  |

### 4.11 People

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| K1 | People on daily routines | 1,3 | **Y** | inventory `daily routines` (exists, ph1); canon: gossip spreads through schedule intersections | stage 2 |  |
| K2 | Crowd density and variety | 1,2,3 | **Y** | inventory `the crowd you see` (partial, ph2) | stage 2 |  |
| K3 | People avoiding the player and each other | 2,3 | **P** | named only in baseline-features; the sim keeps gaps between walkers, but nothing says a walker gives way to the PLAYER | stage 2 | 1 min |
| K4 | Reaction to noise, to a fight, to a gun | 2,3 | **Y** | ROADMAP stage 6: a gunshot producing a measured town-wide perception event; perception exists | stage 3 |  |
| K5 | People talking among themselves | 1,3 | **Y** | ROADMAP stage 3: "a line overheard"; inventory `the town's own voice` (exists) | stage 3 |  |
| K6 | People reacting to weather and time | 1,3 | **N** | weather changes what people can SEE and HEAR in the perception model. Nothing says it changes what they DO | stage 2 | 5 min |
| K7 | Police and authority response | 1,3 | **Y** | inventory `the law and the police` (partial, ph1) | stage 3 |  |
| K8 | Animals and birds | 1,3 | **N** | no bird, no animal, no dog anywhere in the plan. Every gull in the corpus is the Gullwing district | stage 2 | 2 min |

### 4.12 Verbs

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| L1 | Pick up, examine, use | 3 | **P** | `object provenance across five origins` makes an object a thing with a history; pick up, examine and use as verbs are not named | stage 3 | 4 min |
| L2 | Search a container, a room or a body | 3 | **Y** | inventory `searching a room, a container or a body` (absent, ph2) | stage 3 |  |
| L3 | Talk to a person | 3 | **Y** | canon's moat: live LLM conversations with per-character memory | stage 3 |  |
| L4 | Open, close, lock, unlock, lockpick | 3 | **Y** | inventory `burglary and lockpicking` (absent, ph2) | stage 3 |  |
| L5 | Steal and pickpocket | 3 | **Y** | inventory `pickpocketing` (absent, ph2) | stage 3 |  |
| L6 | Sit, rest, sleep to pass time | 3 | **Y** | inventory `sleep as a way to cross a day` (absent, ph2) and `sleep and the day boundary` (absent, ph3) | stage 3 |  |
| L7 | Buy and sell | 3 | **Y** | inventory `economy and trading` (partial, ph3); ROADMAP stage 6 names economy and cash | stage 6 |  |

### 4.13 Combat and harm

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| M1 | Melee with hit feedback | 1,3 | **Y** | ROADMAP stage 6: melee combat, improvised weapons; inventory `combat` (partial, ph4) | stage 6 |  |
| M2 | Blocking, dodging, being outnumbered | 1,3 | **Y** | ROADMAP names being outnumbered as one of combat's three gaps, and names the tension between stage 3 and stage 6 | stage 6 |  |
| M3 | Firearms and their rarity | 1,3 | **Y** | ROADMAP stage 6: scarce firearms as events | stage 6 |  |
| M4 | Damage, health, healing, injury | 1,3 | **Y** | inventory `injury and healing` (partial, ph4) | stage 6 |  |
| M5 | Death, failure and reload | 2,3 | **Y** | inventory `failure states and autosave policy` (partial, ph1) | stage 3 |  |
| M6 | Fleeing and pursuit | 1,3 | **Y** | ROADMAP: running away as a way out, placed at stage 3 by Jafar's words | stage 3 |  |
| M7 | Hit reactions, blood and gore | 1,2 | **Y** | canon D18: violence stays, including blood and light gore; inventory `blood on the player` | stage 6 |  |

### 4.14 Story and speech

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| N1 | Opening cinematic or arrival | 1,3 | **P** | canon has Tom arriving with one suitcase and a letter; no opening scene, cinematic or arrival sequence is named | stage 4 | 2 min |
| N2 | Dialogue interface with choices | 1,3 | **Y** | inventory `spoken conversation` (partial, ph2), evidence DialogueUI.cs | stage 2 |  |
| N3 | Subtitles with speaker names | 3,4 | **N** | the subtitles tile carries no speaker name, in a game where who said it is the whole point | stage 4 | 10 min |
| N4 | Barks and ambient lines | 1,3 | **Y** | inventory `dialogue banks` (partial, ph2) and the bark generator | stage 2 |  |
| N5 | Cutscene skip and pause during a cutscene | 3,4 | **N** | no cutscene skip and no pause inside a scene is named | stage 4 | 3 min |
| N6 | Branching consequence in the story | 1,3 | **Y** | D58 holds the endings at five; canon's three acts | stage 3 |  |
| N7 | Live spoken conversation with memory | 1,3 | **Y** | canon's moat: live LLM conversations with per-character memory and local voice | stage 2 |  |

### 4.15 What the player is told

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| O1 | Tutorial and the first hour | 1,3 | **Y** | ROADMAP stage 4: the first hour; inventory `first hour and tutorial` (partial, ph3) | stage 4 |  |
| O2 | Objectives, and knowing what to do next | 3,4 | **P** | teaching-in-thirty-minutes covers onboarding. The word objective appears NOWHERE in ROADMAP, canon, DECISIONS or the inventory | stage 4 | 5 min |
| O3 | A notebook the player reads back | 1,3 | **Y** | ROADMAP stage 4 and D37: the Ledger is a notebook, not a corkboard | stage 4 |  |
| O4 | Reminder of the objective after time away | 4 | **N** | nothing says how a player who comes back after a week learns what they were doing | stage 4 | later |
| O5 | Progression and unlocks | 1,3 | **Y** | D11 player progression; ROADMAP stage 4: the first hour introduces the player's progression | stage 4 |  |
| O6 | Statistics and a session summary | 3 | **N** | no statistics screen and no session summary | stage 4 | 30 min |

### 4.16 The image

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| P1 | Dynamic lighting and shadows | 1,2,3 | **Y** | ROADMAP stage 1's order: light and shadow first | stage 1 |  |
| P2 | Global illumination and reflections | 2 | **Y** | ROADMAP's PS5 experiment names light that bounces and reflects | stage 1 |  |
| P3 | Post-processing chain | 1,2 | **Y** | ROADMAP's PS5 experiment names the post-processing | stage 1 |  |
| P4 | Materials that read as real surfaces | 1,2 | **Y** | ROADMAP stage 1: surfaces after light; the best free scanned materials | stage 1 |  |
| P5 | Detail that appears without popping | 2,3 | **P** | ROADMAP names detailed geometry and the research names Nanite; no line says detail must arrive without popping | stage 1 | 4 min |
| P6 | Anti-aliasing and image stability | 2 | **N** | no anti-aliasing, no image stability, no shimmer, on a wet street at night which is where it shows | stage 1 | 0 min |
| P7 | Character rendering: skin, eyes, hair | 1,2 | **Y** | ROADMAP's PS5 corner names one MetaHuman standing in it | stage 1 |  |
| P8 | Effects: rain, smoke, breath, blood | 1,2 | **P** | Weather.cs makes rain and the plan names it; smoke, breath and blood spray as effects are named nowhere | stage 2 | 3 min |

### 4.17 Performance and scale

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| Q1 | Frame budget on the target machine | 1,2,3 | **Y** | inventory `the frame budget` (partial, ph2); ROADMAP measures frame time on this card | stage 2 |  |
| Q2 | Streaming without hitching | 2,3 | **Y** | inventory `loading and streaming` (partial, ph5) | stage 5 |  |
| Q3 | Budget management at crowd scale | 2 | **P** | the frame budget tile is the whole frame; no scheme for what gets cheaper as the crowd grows | stage 2 | later |
| Q4 | Memory budget and long-session stability | 2,4 | **Y** | ROADMAP: graphics memory on this card while a character speaks | stage 2 |  |
| Q5 | Minimum specification and the hardware floor | 1,4 | **Y** | inventory `the hardware floor` (absent, ph6); D52 says nobody writes one from the paper | past the sixth stage |  |

### 4.18 Accessibility

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| R1 | Subtitle presentation options | 4 | **P** | baseline-features names subtitle size and background; the plan carries a text scale only | stage 4 | 12 min |
| R2 | Colourblind modes, and not colour alone | 4 | **Y** | inventory `accessibility`: colourblind-safe hues, shipped | stage 4 |  |
| R3 | Text size and high contrast | 4 | **P** | text scale 80 to 150 is named; high contrast is not | stage 4 | 12 min |
| R4 | Full remapping, one-handed play | 4 | **P** | `accessibility` names pad remapping as the gap; one-handed play is named nowhere | stage 4 | 1 min |
| R5 | No button mashing, hold alternatives | 4 | **N** | no rule against a held or repeated input | stage 4 | later |
| R6 | Difficulty and assist options | 4 | **N** | no assist mode, no skippable encounter | stage 4 | later |
| R7 | Motion sickness options | 4 | **P** | `accessibility` names reduced motion as missing; head bob, FOV and camera shake are not named | stage 4 | 3 min |
| R8 | Screen reader for menus | 2,4 | **N** | no screen reader for menus | stage 4 | 1 min |
| R9 | Photosensitivity safety | 4 | **N** | no photosensitivity guidance and no flash limit | stage 4 | 0 min |
| R10 | Adjustable timing, no forced timed input | 4 | **N** | nothing says a timed input may not be required, in a game with a live conversation that runs in real time | stage 4 | later |
| R11 | Accessibility information before purchase | 1,4 | **N** | no accessibility labelling of the kind a store page now carries | past the sixth stage | later |

### 4.19 Localisation

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| S1 | All player-visible text localisable | 1,2,4 | **Y** | inventory `text localisation` (absent, ph6) | past the sixth stage |  |
| S2 | Font fallback and text expansion | 1,2 | **N** | no font fallback and no text expansion allowance, for a game whose UI is built from code | past the sixth stage | later |
| S3 | Localised audio, or a subtitles-only policy | 1,4 | **N** | no policy on whether the synthesised voices are ever anything but English | past the sixth stage | later |
| S4 | Date, time and number formats | 2 | **N** | the clock and calendar are displayed; no locale format is named | past the sixth stage | 8 min |
| S5 | Content variation by locale | 1,4 | **N** | no locale content variation, although canon's content rule already excludes most of what triggers one | past the sixth stage | later |

### 4.20 Platform and release

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| T1 | A store page, a build and patching | 1,2,4 | **P** | asset-coverage ASKS whether a store page ever needs to exist; no plan line answers | past the sixth stage | later |
| T2 | Achievements | 2,4 | **N** | achievements appear nowhere | past the sixth stage | later |
| T3 | Cloud save and cross-device | 2,4 | **N** | cloud save appears nowhere | past the sixth stage | later |
| T4 | Age rating submission | 1,4 | **N** | no age rating and no submission, although canon's content rule is most of the answer to one | past the sixth stage | later |
| T5 | EULA and third-party licence attributions | 1,4 | **Y** | DECISIONS: the licence allowlist is law, and THIRD-PARTY.md carries the attributions | past the sixth stage |  |
| T6 | Anti-cheat or DRM decision | 1 | **N** | no anti-cheat or DRM decision, in a single-player PC game where the answer is probably none | past the sixth stage | later |
| T7 | Platform terminology and button naming | 4 | **N** | no platform terminology or button naming rule | past the sixth stage | later |

### 4.21 Telemetry, support and after release

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| U1 | Crash reporting | 1,2 | **N** | no crash reporting, for a game that runs a local model beside a renderer | past the sixth stage | later |
| U2 | Opt-in analytics and a privacy notice | 1,2,4 | **N** | no analytics and NO PRIVACY NOTICE, while D4 keeps the text model on a paid online service that the player's typed lines reach | stage 4 | 12 min |
| U3 | A way for the player to report a problem | 1,3 | **Y** | inventory `feedback path` (absent, ph6) | past the sixth stage |  |
| U4 | Patch notes and a post-launch plan | 1 | **N** | no patch notes and no post-launch plan | past the sixth stage | later |
| U5 | Playtesting with people outside the team | 1 | **Y** | ROADMAP stages 5 and 6 read the Meridian Test off a session; meridian-test-administration is a whole delivery | stage 5 |  |

### 4.22 The departments' own deliverables

| id | feature | lenses | plan | where the plan holds it, or why not | stage | notice |
|---|---|---|---|---|---|---|
| V1 | Voice casting and direction | 1 | **Y** | inventory `voices` (partial, ph2); asset-coverage on what is missing | stage 2 |  |
| V2 | Motion capture and performance | 1 | **Y** | markerless-mocap is a delivery with a verdict; DECISIONS names Mixamo on Jafar's account | stage 2 |  |
| V3 | Music composition and licensing | 1 | **Y** | inventory `music` (partial, ph3) and the licence allowlist | stage 3 |  |
| V4 | Brand and legal clearance | 1 | **Y** | canon: every brand is fictional, and the brand bible still owes six names | stage 6 |  |
| V5 | Marketing capture: trailers and screenshots | 1 | **P** | asset-coverage asks whether key art and a store page need to exist; nothing answers | past the sixth stage | later |
| V6 | Art direction and a style bible | 1 | **Y** | canon's visual target; the in-house Hook sheet is the stage 1 bar | stage 1 |  |
| V7 | Writing at volume, and editing it | 1 | **Y** | ROADMAP stage 6: the writing at full length; holding-a-large-script is a delivery | stage 6 |  |
| V8 | QA: functional, compliance and localisation testing | 1 | **Y** | inventory `the verify suite` (exists); ROADMAP stage 3 names the test suite | stage 3 |  |
| V9 | Build and release engineering | 1 | **Y** | inventory `the evidence channel` (exists); the CI rules are a studio document | stage 3 |  |
| V10 | A credits screen naming everyone | 1,4 | **Y** | inventory `credits and attributions` (partial, ph6) | stage 4 |  |

## 5. Which lens found what the others missed

No item was found by all four lenses. 28 items were found by three, 100 by two,
and **51 by one lens alone**. The sole-lens items are the whole point of the
exercise: they are where the other three are blind.

| lens | items it touched | absent from the plan | partly | found by this lens ALONE | of those, absent |
|---|---|---|---|---|---|
| 1: who builds it | 79 | 16 | 11 | 13 | 2 |
| 2: what runs every frame | 89 | 18 | 29 | 8 | 3 |
| 3: moment by moment | 108 | 16 | 28 | 15 | 4 |
| 4: what the industry checks | 59 | 29 | 15 | 15 | 10 |

**Lens 4 is the one that earned its place.** It found 15 items nobody else
found, and 10 of those 15 are absent from the plan against 1 that is in it. No
other lens comes near that ratio. Its subjects are the ones a studio with no
publisher and no compliance department never meets: what happens when a pad is
unplugged, whether a sound the player cannot see has a visual form, whether
anything may require a fast repeated press, whether a menu can be read aloud,
whether the screen may flash. It is also the lens whose sources this environment
could not reach, so it is simultaneously the most productive and the worst
sourced. Both facts should travel together.

**Lens 1 confirms rather than discovers.** It found 13 items alone and 10 of
them are already in the plan: casting, mocap, music, clearance, art direction,
writing at volume, QA, build engineering, playtesting. That is what a studio
that has been running for a month already knows it does. Its two absences, a DRM
decision and a post-launch plan, are both ship-prep. Lens 1 would probably have
done better with the credits rolls it was supposed to have.

**Lens 3 produces the clock.** Nine of its 15 sole items are in the plan, but it
is the only lens that says WHEN a gap is met, and every ranking in the summary
is its ordering. It is also the lens that noticed that the plan has a Ledger and
a first hour and no statement anywhere of how a player knows what to do next.

**Lens 2 is narrow and deep.** Only 8 sole items, but they are the ones nobody
without engine knowledge would write down: image stability on a wet street, what
gets cheaper as the crowd grows, an animation budget, a date format.

## 6. What all four lenses are blind to

Worth saying plainly, because a checklist built this way could quietly become
the plan. Not one of the four lenses would have produced:

- the seven perceivable slots every act exposes
- the five-rung identification ladder, and that recognition is gated by
  relationship rather than by distance and light
- permanent per-NPC memory that is never wiped
- gossip travelling through schedule intersections
- a deterministic Core that decides every outcome the player feels, with the
  language model classifying and never adjudicating

Four lenses built from credits, engines, a first session and compliance
checklists find what every game has. They cannot find what only this game has.
The moat is in `canon.md` and it is safe from this document; the point of the
document is that the floor underneath it is not.

## 7. What could not be established

1. **The two named accessibility guidelines and every certification document.**
   Refused by the proxy. Section R is DERIVED from a structure, not read off a
   checklist, and its item list is certainly incomplete. The ESA's 24 labelling
   tags are the cheapest thing to fetch next and would replace most of section
   R.
2. **Any full credits roll.** MobyGames, GiantBomb, IGDB and the Steam store are
   all refused. Lens 1's department list is a reconstruction from four cited
   taxonomies rather than from the thing the brief asked for.
3. **Whether a stage assignment is right.** Every stage in the tables is mine.
   ROADMAP's six stages are Jafar's; the mapping of an absent feature onto one
   is a judgement, and stage 4, the player's shell, carries most of the weight
   because most of what is missing is shell.
4. **Anything about the build.** This delivery never opened the engine or ran
   anything. Where it says a feature is in the plan, that is all it says. The
   build's state is baseline-features' subject and the inventory's.
