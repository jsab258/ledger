# BLUEPRINT 05: How it looks and sounds

Part of the LEDGER blueprint; the index, the rules of reading and the conflicts are in BLUEPRINT.md. Presentation: people, motion, places, light, sound, voices, music, camera, effects.

Each entry: how it works; its standard and test; the source of the standard; its status; its coverage row. Conflicts are numbered C-nnn and listed in BLUEPRINT-11-conflicts-and-gaps.md.


## 5.1 Characters

People on screen.


### 5.1.1 Faces

- How it works: Four faces are frozen and approved: Ron P2, Sheila S4 with its hair, Darren S6 with Epic's short cut, Tom L1. The other eleven casting sheets are approved as text and their faces are cast in MetaHuman from them, a generated portrait being a mood only. The test is his eye at talking distance, and a face must not read underlit in passing.
- Standard: Faces frozen: Ron P2, Sheila S4, Darren S6, Tom L1; the other eleven cast from their sheets Test: his eye at talking distance
- Source: RULINGS 30 Sep, 8 Oct (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 25 Sep, 30 Sep, 8 Oct (Faces, hair and voices); PARTS-TREE 5.1.1; 6-RISKS R4
- Status: outside. Coverage row: 5.1.1. Conflicts settled: C-112.
- Prior research: research/character-pipeline: blended presets gave only three white European female presets; Python can sculpt face landmarks; iris colour is a position on a 512 by 256 chart.

### 5.1.2 Bodies

- How it works: Bodies are the MetaHuman bodies kept in F:\LedgerTools\bodies and the clothing session works only on them. Four exist today (Rocco P2, Sam C5, Lena S4 as body files, and Tom L1); there are no crowd bodies. The test is the gate.
- Standard: Bodies in F:\LedgerTools\bodies; clothes fit them Test: the gate
- Source: CLAUDE.md sessions (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: CLAUDE.md Sessions; PARTS-TREE 5.1.2; RULINGS 2 and 8 Oct (fitting six bodies, stopped)
- Status: outside. Coverage row: 5.1.2.

### 5.1.3 Hair

- How it works: Hair is built as strands, which stay (9 Nov). No hair skill is made until one character's hair passes the full gate with his look included. The pass list is his words: seen from behind, in a talk close-up, sitting and walking side-on; at about 1, 3.1, 10 and 25 m with no colour change or popping; by day, overcast, by a window, under lamps at night and wet; no shimmer, no hard shadow on collar or neck, no pale scalp; its frame cost measured for one person and the corner's crowd.
- Standard: Hair PASS-LIST (his words); strands stay (9 Nov) Test: the full gate and his look
- Source: RULINGS 3, 9 Nov (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 3 Nov, 9 Nov; production/art/hair-2026-09-29/PASS-LIST.md
- Status: outside. Coverage row: 5.1.3.
- Prior research: research/hair (8 to 9 Nov): cards cut card memory (5,639 to 5,194 MB) and GPU (14.17 to 12.89 ms) but add faults (flat orange-brown crown patch, white blotches, scalloped nape); reviewers judged them not usable close; packaged strands 0.16 ms against cards 0.25 ms close.

### 5.1.4 Clothes

- How it works: Clothes are Kiln garments (skinned meshes, only loose parts simulated). Tom wears three outfits across the rise (as he arrived, a decent jacket, a good overcoat) and a dark coat for nights, each changing how strangers speak to him and which doors open; prices are a second-hand coat 15 pounds, the decent jacket 45, the good overcoat 90. The floor is plain, period-plausible, no modern giveaways (contrast-stitched slim jeans, trainers), no clipping or holes, nobody frozen stiff; passers-by are judged at eight metres, principals at talking distance on the 2026 bar against KCD2 frames.
- Standard: Clothes' floor: plain, period-plausible, no modern giveaways, no clipping; principals at talking distance on the 2026 bar Test: the gate; his eye in the game's camera
- Source: RULINGS Clothes (3 Oct, 19 Nov) (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: DESIGN §14; DEFINITIONS-2026-11-21 §G8; DESIGN-ADDENDUM §A21; RULINGS Clothes 3 Oct, 29 Sep, 19 Nov; production/art/clothing/RUBRIC.md
- Status: outside. Coverage row: 5.1.4. Conflicts settled: C-113.
- Prior research: research/plain-1990-clothes and production/reference: what reads 2020s is slim contrast-stitched jeans and casual trainers; men's palette navy, black, charcoal, grey, brown, bottle green, oatmeal; dockers wore nylon anoraks by 1989, the donkey jacket is one garment among many; research/wardrobe-at-scale counts assumed six bodies, recount.
- People react to appearance (catalogue 23 Nov, rank 5; seen in 3 games): A better coat draws a different greeting. Already covered: the three outfits change how strangers speak to him and which doors open. Feature only; no timing; the part's status is unchanged.

### 5.1.5 Crowd variety

- How it works: Named only; not designed beyond: a crowd count by hour and place (design pass 4: the parade front 12 to 20 people in the busy bands, 5 to 10 from 18:00 to 22:00, 2 to 5 from 22:00; one frame 4 to 10, GD-02) and the rule that a crowd extra who catches any slot of a deed becomes kept, with a fixed face, a coat and a home. No repeat distance or variety rule exists.
- Standard: none yet: repeat distance and variety rules to be set Test: S: no identical pair in one frame; his eye
- Source: risk R5 (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: DEFINITIONS-2026-11-21 §G9, §RT2-10; COVERAGE 5.1.5; 6-RISKS R4; PARTS-TREE 5.1.5
- Status: outside. Coverage row: 5.1.5.
- Prior research: casting/notes/crowd.md (SIGGRAPH 2008): colour tint doubles the time to spot a clone, so vary clothes before faces; idles 5 to 8 per kind with randomised starts (game-design/research/inhabited-street.md); game-design/authored-breadth-2026-11-13.md.

## 5.2 Animation

Movement.


### 5.2.1 Locomotion

- How it works: Walk and run use Epic's Game Animation Sample with motion matching; the third try is the default (his eye, 26 Oct). Tom walks at 1.6 m/s, walks slowly (Z held) at 0.9 m/s and runs at 5.5 m/s (5.3 with a holdall); a constable walks at 1.1 m/s and runs at 5.2. Feet must not slide, and speeds never depend on the frame rate.
- Standard: Third try the default (his eye 26 Oct); feet do not slide Test: his eye; foot-slide measure
- Source: RULINGS People's moves (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 13 Oct, 26 Oct, 30 Sep; DEFINITIONS-2026-11-21 §G4; PARTS-TREE 5.2.1
- Status: outside. Coverage row: 5.2.1.

### 5.2.2 Fight animation

- How it works: Fight animation follows the melee sheet: a jab lands 0.25 to 0.40 s after the press, a hook 0.45 to 0.75 s, the committed heavy blow 0.63 to 0.85 s and cannot be cancelled; the struck man reacts for 0.5 to 0.7 s (light) or 0.9 to 1.3 s (heavy), and a knocked-down man starts to get up after 1.5 to 3.0 s. A struck man reels by the side he was hit and nobody is hit through a wall. Per the 12 Oct ruling, the animation source is lab-tested before anything is built; no fight animation exists yet.
- Standard: Melee sheet C2 to C4; ruling 12 Oct: animation source lab test before building Test: melee drills in Unreal match the browser
- Source: RULINGS combat; melee sheet (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: FEEL-TARGETS-MELEE-2026-11-18 C2, C3, C4, C7; DESIGN §7; RULINGS Combat 12 Oct; PARTS-TREE 5.2.2
- Status: outside. Coverage row: 5.2.2. Conflicts settled: C-114.

### 5.2.3 Interaction animation

- How it works: Named only; not designed beyond: a list of interactions found across the description (doors open and stairs climb with no stop over 5 s; getting into a car 1.5 to 2.5 s door to seated and out under 2 s, from both sides (1.2.3); sit, lean and light a cigarette on B; carry a holdall; search; raise the watch with N). The only standard is that none glitches.
- Standard: No glitches (CLAUDE.md gate) Test: the gate
- Source: CLAUDE.md (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: ONE-SHOT-PROMPT S01, S02 and §9; DESIGN §5 ER-DRIVE-07; DESCRIPTION-2 §8; PARTS-TREE 5.2.3
- Status: outside. Coverage row: 5.2.3.

### 5.2.4 Faces and mouths

- How it works: Live lines' mouths follow the voice's loudness; prepared lines (thinking sounds included) use Epic's audio-driven mouths. Tom stands about 1.5 m from a speaker and both face each other, with a glance before a live answer. A speaker's face must not be broken when talking (the 4 Oct friends' build line asks for Sheila's face whole).
- Standard: Live lines' mouths follow loudness; prepared lines use Epic's audio-driven mouths (1 Oct); Sheila's face whole when she talks Test: his eye at talking distance
- Source: RULINGS 1 Oct, 4 Oct (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 1 Oct (Voices); DESIGN §11 Staging; PARTS-TREE 5.2.4; production/research/talking-face-faults/NOTE.md
- Status: outside. Coverage row: 5.2.4.
- Prior research: research/lip-sync: Epic's StreamingADA (hidden beta in 5.8.2) returns 81 face controls every 20 ms about 80 ms behind, 34 MB; amplitude jaw as fallback; research/talking-face-faults: the captured idle passes about 150 mouth controls, only 11 overridden by loudness.

### 5.2.5 Crowd and idle animation

- How it works: Idles must not hold still: looping idles with a random start, a play rate of 0.9 to 1.1 and neighbours differing, so nobody stands frozen. The corner plan's baseline had speakers moving in 59 of 60 four-second windows and the street's extras in 12 of 18; work, smoke and talk idles are not built.
- Standard: No stiff idle; nobody frozen stiff (clothes floor) Test: the gate
- Source: RULINGS; risk R4 (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: CORNER-PLAN-2026-11-02 step 3; BASELINE-2026-11-02 row g; RULINGS Clothes floor 3 Oct; 6-RISKS R4; DESCRIPTION-2 §7
- Status: outside. Coverage row: 5.2.5.
- Prior research: research/natural-idles: base loop 8 to 12 s with weight shift, breaks every 30 to 60 s, breathing additive 1 to 2 cm at 15 to 20 a minute; research/townspeople-animation: Witcher 3 about 35 idles per body type; foot slide bar 3 cm a contact.

### 5.2.6 Body language of knowing

- How it works: Knowing shows in the body before any line, on one ladder: notice, watch, comment, avoid, refuse, confront. A watcher's head turns at the start of the 1.2 s it takes to know him (a glance is 0.35 s), at least 0.8 s before identification; also a longer look, a pause in a walk, two heads together, a step back at night, a figure at a lit window. Nobody who knows nothing shows it, and a told version never shows above a seen one.
- Standard: D29: posture first Test: H: ER-EYES-01
- Source: D29 (his ruling or canon). Designed in: D29; DESIGN §2 and ER-EYES-03; DEFINITIONS-2026-11-21 §2.4.3; DESCRIPTION-2 §5; PARTS-TREE 5.2.6
- Status: ruled (his ruling or canon). Coverage row: 5.2.6.
- Prior research: research/gaze-and-knowing: Fotios 2015 (Sheffield, 1,538 pedestrians): 73% looked, median two looks, at 10.3 m (13.0 day, 8.9 dark), median 0.48 s; baseline 49% no look, 46% polite glance 0.06 s; eyes away inside 2.4 m.

### 5.2.7 Clip sourcing and cleanup

- How it works: Clips come from Epic's samples, MetaHuman's movement clips, Mixamo on his account, and CMU motion capture inside the game (never resold or shipped as a library). Pexels and Pixabay clips serve only as motion references and controls, each licence read and recorded; he never films or performs anything. Raw Mixamo files stay out of git, history included.
- Standard: Sources allowed: Epic samples, MetaHuman, Mixamo on his account, CMU inside the game; Pexels/Pixabay as references Test: each clip's source and licence recorded
- Source: RULINGS People's moves; 9, 12 Nov (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS People's moves, 9 Nov, 12 Nov, 19 Nov; license-allowlist item 11; PARTS-TREE 5.2.7
- Status: outside. Coverage row: 5.2.7.
- Prior research: research/ai-video-motion: local clip (Wan 2.2 TI2V 5B) about 100 min of card for 81 frames at 832 by 480; markerless solve 35 to 41 min CPU, about 10 min per second of motion; foot slide under 2 cm. He never films (RULINGS 9 Nov).

### 5.2.8 Physical reactions and falls

- How it works: A struck man reels by the side he was hit; nobody is pushed through a wall. A person hit by Tom's car falls by speed: under 10 mph a stagger and a hand on the bonnet; 10 to 25 mph knocked down, rolls once, sits up within 5 s; over 25 mph thrown down, lies up to 20 s, then moves and calls out. Never flung through the air, never limp as dead, and the choice of stopping comes within 2 s; Tom beaten comes round and is in control within 60 s.
- Standard: A struck man reels by the side he was hit (DESIGN §7); nothing through walls Test: his eye; drills
- Source: DESIGN §7 (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: DESIGN §7, §5 ER-DRIVE-03, ER-DRIVE-05; DEFINITIONS-2026-11-21 §P04, §8.10; FEEL-TARGETS-MELEE C7
- Status: outside. Coverage row: 5.2.8.

### 5.2.9 Live-talk faces

- How it works: Live lines' mouths follow the voice's loudness, with a glance and a short thinking sound before the answer, cut when the answer starts. Gestures and glances for live lines are not designed beyond that.
- Standard: Live lines' mouths follow the voice's loudness (ruling 1 Oct) Test: his eye at talking distance
- Source: RULINGS 1 Oct (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 1 Oct, 28 Sep; DESIGN §11; PARTS-TREE 5.2.9
- Status: outside. Coverage row: 5.2.9.

## 5.3 Environment art

Buildings and ground.


### 5.3.1 Building kits

- How it works: Building kits are made from dated photographs and period books: windows, doors, shopfronts, railings, brick. Pieces the period books draw are written as a target by a fresh helper, never the builder, then an automatic check and a fresh reviewer against photographs; yes only for 2026-grade work against the Hook sheet and KCD2 frames. Built so far: a shopfront kit, a sash window and a terrace carcass kit, with seven fronts gated; Flemish bond appears as a photographed brick texture in the corner spec.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, dated photographs win; yes only for 2026-grade work; kit pieces from period books checked by a fresh helper (8 Oct) Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate; ruling 8 Oct (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 21 Sep, 1 Oct, 8 Oct; CLAUDE.md gate; PARTS-TREE 5.3.1; production/specs/ps5-corner.json
- Status: outside. Coverage row: 5.3.1.
- Prior research: research/phase5-procedural TERRACE-KIT-TABLE (Levenshulme 1994 photograph): brick course 85 to 88 mm, windows 1.00 to 1.06 by 1.62 to 1.69 m, storey 2,925 mm (parade 3.4 m and 2.8 m); Hull red and buff, Grimsby red-brown with blue bands; brick saturation ceiling 0.56 (the Hook sheet's 0.65 rejected).

### 5.3.2 Materials and grime

- How it works: Grime is the strategy: a seeded wear layer calibrated to real reflectances. Damage stays until mended: blood on a pavement stays until rain or a bucket washes it, a forced door shows for a day, broken glass stays until the owner mends it; marks keep across save and load. The pavement, road, brick and daylight are checked against real values and photographs of a wet overcast street.
- Standard: D53; calibrated to real reflectances Test: the gate
- Source: D53; RULINGS 21 Sep (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 21 Sep, 29 Oct (the look); D53; ONE-SHOT-PROMPT §15 lasting marks; PARTS-TREE 5.3.2
- Status: outside. Coverage row: 5.3.2.
- Prior research: measured reflectances: wet asphalt albedo 0.07 to 0.08, wet flags 0.13 to 0.22; gloss paint base colour is LRV minus 0.04 (floor 0.02); research/texture-pipeline edge wear 0.7 to 0.8 gives a worn band of 3 to 10% within 5 cm.
- Wear placed by use (catalogue 23 Nov, rank 19; seen in 2 games): A worn line across the verge, scuffed shop steps, pigeon marks under ledges, soot over coal-fire chimneys. Partly: the wear layer is seeded; placing it by use is not yet stated. Feature only; no timing; the part's status is unchanged.

### 5.3.3 Wet street

- How it works: The wet street is dark, glistening, mirroring sky and buildings, with puddles as water (ruling 3 Oct); the weather is dry overcast, drizzle or rain, with one wetness value driving look, hearing and who is out. A wet road takes about 3 to 14 hours to dry and puddles days, with rain on about 12 days a month; it is never sunshine in the friends' build.
- Standard: Ruling 3 Oct bars for the wet street Test: the gate
- Source: RULINGS 3 Oct (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 3 Oct, 5 Oct; DESIGN §6; LIGHT-WEATHER-VALUES-2026-11-17; PARTS-TREE 5.3.3
- Status: outside. Coverage row: 5.3.3.
- Prior research: a road reads wet when dark and near-mirror (roughness 0.06) (research/aaa-street, street-wear); harbour water dark, near-neutral, reflection-led with centimetre chop (game-design/research/water.md).

### 5.3.4 Shop glass and windows

- How it works: Windows have white frames, sash bars and sky in the glass; shop glass shows the street (real glass, ruling 4 Oct, for Mickey's front room). A window is a watcher only when a figure shows at it, head and shoulders at the glass; the pawnbroker's window is lit at night; a broken window shows scattered glass and an empty frame, which stays until mended.
- Standard: Ruling 3 Oct (windows); ruling 4 Oct (real glass) Test: the gate
- Source: RULINGS 3, 4 Oct (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 3 Oct, 4 Oct, 1 Oct; DESIGN §6 ER-NIGHT-02; ONE-SHOT-PROMPT S12; PARTS-TREE 5.3.4
- Status: outside. Coverage row: 5.3.4.
- Prior research: research/shop-glass-reflections: Translucent multiplies the reflection by opacity (4% becomes 1%), so use Thin Translucent with the room dimmed to about a tenth of the pavement by day; research/broken-window-look: radial cracks, ragged dark hole low, glass thrown back up to 3 m, a glittering band of shards about 2 m deep.

## 5.4 Lighting and picture

Light and grade.


### 5.4.1 Day exposure and sky

- How it works: By day the exposure stays one stop darker, never brightened again, and the sky is a photograph. In the lamp numbers the exposure pin is 4.0 by day and 0.4 by night. Grey range only (dry overcast, drizzle, rain), no sunshine in the friends' build, and sunset around 16:00 in mid-November.
- Standard: Ruling 29 Oct; D40 Test: checked against real values
- Source: RULINGS 29 Oct, 15 Sep (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 29 Oct, 15 Sep, 5 Oct; D40; LIGHT-WEATHER-VALUES-2026-11-17; PARTS-TREE 5.4.1
- Status: outside. Coverage row: 5.4.1.
- Prior research: game-design/research/art-direction.md: noon sun 58.9 degrees at midsummer, 35.5 at the equinox, 12.1 at midwinter (54.5 N), about 1,403 sunshine hours a year; overcast sky 3 times brighter at the zenith than the horizon; research/photoreal-on-a-budget: sky first, soft fill, tonemapping.

### 5.4.2 Night lighting

- How it works: Night is pools of lamp light with darkness between, lit windows, never one orange wash. The pool under a lamp is about ten times the night fill (the real range is 10 to 25); real side streets are lit to 3.5 to 6 lux average with the dimmest point 1 to 2.5 lux. Tom and the ground 5 m round him must always be visible above a brightness floor kept in the one tuning table.
- Standard: Ruling 1 Oct; ER-NIGHT-01 brightness floor Test: H: darkest-spot screenshots; the gate at night
- Source: RULINGS 1 Oct; DESIGN §6 (his ruling or canon). Designed in: RULINGS 1 Oct, 7 Oct; DESIGN §6 ER-NIGHT-01; LIGHT-WEATHER-VALUES-2026-11-17; PARTS-TREE 5.4.2
- Status: ruled (his ruling or canon). Coverage row: 5.4.2.
- Prior research: research/evening-light-1990 and archived DECISIONS 4 Nov: real night photographs 3.0 to 5.2 stops from pool to gap; the readable-night fix took the near-black share from 66% to 45%; sodium 589 nm (see 4.7).

### 5.4.3 Grade, grain and depth of field

- How it works: Named only; not designed beyond: the presentation (grade, grain, depth of field) is owed since D28 and was to be built early; one colour grade is shared between the browser prototype and Unreal. Depth of field and motion blur each get their own switch.
- Standard: D28 presentation built early Test: the gate
- Source: RULINGS 15 Sep (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 15 Sep, 18 and 19 Nov; DEFINITIONS-2026-11-21 §AX-03; PARTS-TREE 5.4.3
- Status: outside. Coverage row: 5.4.3.
- Prior research: research/1990-on-film-stock: surviving 1990 photographs are warm (Kodak Gold 200, minilab, scan), so evidence of geometry and material, never colour.

## 5.5 Sound

The street heard; sound carries the town's eyes. CC0 only (D26).
- Prep: SOUND-PLAN SND-01 to SND-27 (23 Nov): 27 standards each with a test (A through LEDGER.mix(), E by ear), 118 sound kinds counted (INVENTORY), a build order in five steps, built on the 97 cloud-week sound files (46 CC0 recordings; beds -36.5 LUFS day, -39.5 night, -33.5 rain; judgement figures, unheard in the game).

### 5.5.1 Footsteps and foley

- How it works: Footsteps differ by surface and gait, for Tom and for others; a footstep at three in the morning carries about 3.6 m and at noon nothing, and sound carries twice as far in the small hours. A tester with the picture off can tell a walk from a run. The research found the standard method uses spawned sounds around the listener capped by place and hour.
- Standard: Footsteps by surface and gait (DESIGN §17) Test: H: sound-only test; his ear
- Source: DESIGN §17 (no reference figure yet). Designed in: DESIGN §17, §2, ER-SND-01; ONE-SHOT-PROMPT §8; STREET-SOUND-SOURCES plan; MEASUREMENTS-NEEDED A7; PARTS-TREE 5.5.1
- Status: unmeasured. Coverage row: 5.5.1.
- Prior research: research/footsteps: walk = Freesound 273077 (CC0, 94 steps a minute), run = BigSoundBank s0514 (trainers; replace for boots, C-232) (CC0); production/cloud-week/sound holds 97 built files with a loudness plan (day bed -36.5, night -39.5, rain -33.5 LUFS), judgement, not yet heard: run the listening pass on them.
- Prep: SOUND-PLAN SND-05 to 07: at least 7 surfaces (setts, flagstone, tarmac, wet, wood and stairs, iron plates, indoor boards and lino; the count is the plan's own), walk, run and slow walk for Tom, at least three shoe kinds, steps one function of reach (audio.js today: loudness is reach in metres over 10); 40 footstep files exist in cloud-week/sound; the prototype has no surface, shoe or left and right.
- Footsteps by sole and surface; coughs at smoke (catalogue 23 Nov, next tier): Footsteps by surface and gait are already covered. Not yet: people coughing at smoke. Feature only; no timing; the part's status is unchanged.
- Checklist (23 Nov, top twenty no. 16; A29.15, A29.16, A29.17): missing: a no-repeat and variant-count rule per sound, a test that one event fires one sound, and a test that steps stop when Tom stops. Gap for the design proof; status unchanged.

### 5.5.2 Doors and impacts

- How it works: Doors creak, hit and latch; a forced door or broken glass is the loudest thing in a quiet street, heard at its force reach, and the window breaks loudly and the glass stays until mended. A forced door shows on the door for a day.
- Standard: DESIGN §17 Test: H: sound-only test; his ear
- Source: DESIGN §17 (no reference figure yet). Designed in: DESIGN §17, §4; ONE-SHOT-PROMPT S12 and §8; PARTS-TREE 5.5.2
- Status: unmeasured. Coverage row: 5.5.2.
- Prep: SOUND-PLAN SND-18: a forced door or broken glass is the loudest one-shot in the street's mix at its force reach (testable through LEDGER.mix()); SND-17 each room has its own tone at least 10 dB under speech.

### 5.5.3 Street beds and states

- How it works: The street sound has three parts: quiet looping beds, short one-shots spawned around the listener and capped by place and hour, and placed sources each heard within a set distance. It has four states of the hour (not named in the sources). The reference found a quiet street spawns at most 3 far voices and 3 activity sounds by day and none at night.
- Standard: DESIGN §17; STREET-SOUND-SOURCES plan Test: H: sound-only test; his ear
- Source: DESIGN §17 (no reference figure yet). Designed in: DESIGN §17; STREET-SOUND-SOURCES-AND-LISTENING-PLAN-2026-11-17 (Professional method); PARTS-TREE 5.5.3
- Status: unmeasured. Coverage row: 5.5.3.
- Prep: SOUND-PLAN SND-01 to 04: four hour states (early 05:30 to 08:00, day to 18:00, evening to 23:00, small hours; the plan's own) by three weathers, 12 mixes; caps day 3 far voices and 3 activity sounds, early and evening 2 and 2 (own design); at most 40 sounds at once, 24 on low (own design; Rockstar tracks about 1,000 and plays 96); every placed source names its owner.
- The day's clock heard and seen (catalogue 23 Nov, rank 10; seen in 3 games): Bells, the milk float, the paper round, and a night noise bringing a light and a face at the curtain. Partly: the chapel bell and lit windows are covered; milk float, paper round and the curtain answer are not. Feature only; no timing; the part's status is unchanged.
- Checklist (23 Nov, top twenty no. 1; A28.01, A28.02, A28.15): missing: a sound must come from its source's side and follow Tom's facing, with a smooth pan as a car passes and a drive-past listening test; today only reach in metres is set. Gap for the design proof; status unchanged.
- Checklist (23 Nov, top twenty no. 11; A28.12, A28.13): missing: a rule for sound above and below (the flat over the office, stairs) and for where the ears sit when the camera is 3.1 m back, Tom or the camera. Gap for the design proof; status unchanged.

### 5.5.4 Rain and rooms

- How it works: One rain value fades the sound layers and halves voices; rain cuts all noise reach. Rooms change the echo at the doorway; in the prototype there is a reverb when inside but no echo at doorways.
- Standard: DESIGN §17 Test: H: sound-only test; his ear
- Source: DESIGN §17 (no reference figure yet). Designed in: DESIGN §17, §6 ER-NIGHT-03; ONE-SHOT-PROMPT §8; PARTS-TREE 5.5.4
- Status: unmeasured. Coverage row: 5.5.4.
- Prep: SOUND-PLAN SND-16: one shared reverb swapped at the doorway, crossfaded over about 1 m of walking and at least 0.5 s (A test: wet level changes over at least 0.5 s); room kinds: office, caff, launderette, chapel, shop, flat, hut, back room.
- Checklist (23 Nov, top twenty no. 2; A28.06, A28.07): missing: walls and shut doors must dull sound, and open doors and windows must let it through, so a shout through an open door carries; a listening test for each. Gap for the design proof; status unchanged.

### 5.5.5 Car sound

- How it works: 1990 by sound: the car's engine note runs about 28 Hz at idle to about 210 Hz at the limit (a small four-cylinder idling at 800 to 900 rpm, limit 6,000 to 6,500). The gearbox is automatic by ruling, so a change is a short, softer dip (length not yet set), and tyre squeal starts from about 80% of the grip limit as a warning. The car is heard within about 44 m by day, the horn about 60 m.
- Standard: Driving sheet M12; ruling 18 Nov Test: H: sound-only test; his ear
- Source: DESIGN §17 (no reference figure yet). Designed in: DESIGN §5, §17; CAR-NOISE-ANCHORS-2026-11-18; FEEL-TARGETS-DRIVING M12; RULINGS Cars 18 Nov; PARTS-TREE 5.5.5
- Status: unmeasured. Coverage row: 5.5.5.
- Prep: SOUND-PLAN SND-08 to 11: engine note tracks speed within 5 per cent, exhaust a separate layer; gear changes are soft dips (a three- or four-speed automatic changes up two or three times to 50 mph, own design); reaches 44 m, horn 60 m; period siren in a chase only; no keyless chirps, reversing beepers or phone ringtones.
- Damaged cars sound damaged (catalogue 23 Nov, next tier): A hurt cab sounds hurt. Not yet: the part gives engine, squeal and horn but no damage sound. Feature only; no timing; the part's status is unchanged.

### 5.5.6 Fight sound

- How it works: A blow sounds four layers: whoosh from blow start, impact from contact, a pain cry after contact, and an enemy shout before his blow lands. The impact must come within 0.034 s of contact, the whoosh from 0.05 s before to 0.10 s after the start, the pain cry 0.05 to 0.30 s after contact, and the shout at least 0.40 s before. There is never combat music.
- Standard: Melee sheet; DESIGN §7 Test: H: sound-only test; his ear
- Source: DESIGN §17 (no reference figure yet). Designed in: FEEL-TARGETS-MELEE-2026-11-18 C13; DESIGN §7, §17; ER-MUSIC-01; PARTS-TREE 5.5.6
- Status: unmeasured. Coverage row: 5.5.6. Conflicts settled: C-115.
- Prep: SOUND-PLAN SND-19, 20: the four layers and timings are testable from the mix record; a shot is heard about 177 m by day with an echo off warehouses and quay walls, after which the street goes quiet (SND-13) and birds lift.

### 5.5.7 The mix

- How it works: The quietest lead voice sets the mix and talk lowers the beds; silence is the commonest music. Sliders cover master, voices, effects, street and music, plus a 'voices clear' switch that lifts voices over the street by 6 dB and a 'loud noise softening' switch that clips gunshots to a door slam's level.
- Standard: DESIGN §17 Test: H: sound-only test; his ear
- Source: DESIGN §17 (no reference figure yet). Designed in: DESIGN §17; DEFINITIONS-2026-11-21 §AX-04; ADDENDUM §A8; PARTS-TREE 5.5.7
- Status: unmeasured. Coverage row: 5.5.7.
- Prep: SOUND-PLAN SND-24 to 26: during a spoken line the bed is at least 6 dB under the voice; loudness -23 LUFS integrated over 30 minutes plus or minus 2 LU (Sony's Garry Taylor, 2012; IESD says -24 for console), true peak at most -1 dBTP, the loudest sound at most 20 LU above (400 ms momentary); whether headless Chrome renders audio is untried, so the first run is on his PC.

## 5.6 Voices

Spoken lines.


### 5.6.1 Cast voices

- How it works: Voices are chosen per character and cast only on his yes: Sheila p267 and Ron p227 on Pocket (live and prepared lines), Darren recast on Pocket as VCTK p286 (Newcastle), Agar p226, the dispatcher p280. Danny (p243), June (p277) and Father Walsh (his July voice) get a listening page and are cast only on his yes. Voices are judged by ear; the accent checker only screens.
- Standard: Sheila p267, Ron p227, Darren p286, Agar p226, dispatcher p280; others on his yes Test: his ear
- Source: RULINGS voices (3 Oct to 19 Nov) (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS Voices 3 Oct, 26 and 27 Oct, 19 Nov, 30 Sep, 24 Sep; PARTS-TREE 5.6.1
- Status: outside. Coverage row: 5.6.1.
- Prior research: research/voice-alternatives and casting/notes/voices.md: all 23 cast voices from VCTK (CC BY 4.0); no Hull accent source and no speaker over 38; the accent checker fails about half of genuine Scotsmen (a screen only).

### 5.6.2 Voice generation and watermark

- How it works: Voices are made on his PC by the local voice program (Pocket kept, 19 Nov; consent risk his); prepared lines for Ron and Darren use an acted reference, and the watermark (D50) stays on generated speech. No paid voice service and no hiring, ever.
- Standard: D50 watermark; Pocket kept (19 Nov) Test: packaged speech measure
- Source: RULINGS D50, 19 Nov (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 25 Sep, 24 Sep, 29 Sep, 19 Nov; D50; PARTS-TREE 5.6.2
- Status: outside. Coverage row: 5.6.2.
- Prior research: research/tts-licensing-and-consent: 23 cast voices, all VCTK CC BY 4.0, all conditional because no text says speakers agreed to cloning; credit to VCTK, Edinburgh and CSTR owed; watermark unresolved.

### 5.6.3 Thinking sound and timing

- How it works: Before an answer comes a short thinking sound with a glance, cut when the answer starts, and never a loading sign. A reply is heard within 2 s or the written line plays; a line slower than 8 s is dropped with an in-character brush-off. The Unreal build misses the 2.0 s bar at 2.02 s.
- Standard: Ruling 28 Sep; no loading sign Test: S: timing
- Source: RULINGS 28 Sep (his ruling or canon). Designed in: RULINGS 28 Sep; DESIGN §11 ER-TALK-01; PARTS-TREE 5.6.3
- Status: decided (the 2 s bar is his ruling of 7 Oct; the written line at 2 s is the design's rule, C-251 and R10). Coverage row: 5.6.3.
- Prep: TECH-PLAN section 10: the written line after 2.0 s is the design's rule (ONE-SHOT-PROMPT section 40), not a ruling of his; the live reply is dropped when it lands late and abandoned after about 8 s.

## 5.7 Music

Silence is the commonest music; never combat music.


### 5.7.1 Radio programmes and period songs

- How it works: Named only; not designed beyond: music comes from places (a radio in the caff, a shop, the office set, a window at night, the chapel organ), all invented or made for the game, on licences that never expire. Music is heard only where it plays in the world (DEFINITIONS P09, 21 Nov); whether a short made-for-the-game score goes under cut scenes and act ends is Q11 for him, and none is built meanwhile; no music starts or changes because a fight or chase starts. The pirate radio station is owed by the brand bible.
- Standard: No real bands, lyrics or brands (canon); content from the allowlist or the studio's own, only on licences that never expire Test: canon gate; his ear
- Source: canon Brands and law (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: canon Brands and law; ADDENDUM §A8; DEFINITIONS-2026-11-21 §P09; ER-MUSIC-01; RULINGS Sources
- Status: outside. Coverage row: 5.7.1. Conflicts settled: C-116, C-117.
- Prep: SOUND-PLAN SND-21 to 23: no music unless a world source (caff radio, record through a window, chapel organ, club radio, busker) is within its distance; the prototype's generated score is removed; world music passes a small-speaker filter; every tune carries its tool and licence line.

### FIT-P09 Music made for the game, placed in the world

- How it works: No music station in the cab. Music is heard only where it plays in the world (a radio in the caff, the chapel's organ, a record through a window), and every piece is made for the game and listed with its maker, since canon makes every band fictional with no real lyrics and no period recording is licensed. The check is the audio files listed against the allowlist and canon's fictional-brands rule.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (his ruling or canon). Designed in: DEFINITIONS-2026-11-21 §P09; FIT-CHECK-2026-11-21 P09 and question 4 note; canon Brands and law; ADDENDUM §A8
- Status: ruled (his ruling or canon). Coverage row: FIT-P09. Conflicts settled: C-118.
- Prep: SOUND-PLAN SND-21, 22: the check is every music file or recipe carrying its tool and licence against the allowlist (item 5: self-hosted MusicGen (MIT) or Stable Audio Open, verify the weights licence) and the content check finding no real band names; radio speech is fictional presenters.

## 5.8 Cameras and cut scenes

The camera system and the few short scenes.


### 5.8.1 Camera rig by state

- How it works: One camera arm reads rows by Tom's state: street (the Between picture's height, 86 degree lens, 3.1 m back, feet in frame), run, room and talk (closer), fight (wider, 3.5 to 5.0 m back, both men's feet in at least 90% of frames), and car (about 5.8 m back, widening with speed). Blends take one second or less, shake obeys Reduce motion, and the camera never ends inside a wall, body or car. The field of view is a setting from 75 to 100 degrees, default 86.
- Standard: Ruling 28 Oct (street, talk closer, fights wider); blends 1 s or less; shake obeys Reduce motion Test: S: frames counted; B clip detector
- Source: RULINGS 28 Oct; DESIGN §17 (his ruling or canon). Designed in: RULINGS 28 Oct, 21 Nov; DESIGN §17 (ER-CAM-01, ER-CAM-02); FEEL-TARGETS-MELEE C10; DEFINITIONS-2026-11-21 Design pass 3 header; PARTS-TREE 5.8.1
- Status: ruled (his ruling or canon). Coverage row: 5.8.1. Conflicts settled: C-119.
- Prior research: production/specs/camera.json: street row is his ruling and measured in the packaged game; talk, run and room rows came from Mafia's files, to be shown to him before kept.

### 5.8.2 Cut scenes

- How it works: Cut scenes are few, short and skippable. Every scene is skippable and at most 60 s, under 5% of the first hour is watched, and no stretch passes 3.5 min without control. The only one specified is the ferry shot, about 20 s, which ends by itself or at once if skipped. The description says no long cutscenes and no watched opening.
- Standard: Every scene skippable and at most 60 s (ER-FIRST-02); few short skippable cutscenes (23 Sep) Test: S: skip works; length measured
- Source: RULINGS 23 Sep; DESIGN §15 (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 23 Sep (genre); DESIGN §15 ER-FIRST-02; ONE-SHOT-PROMPT S01; DESCRIPTION-2 §3; PARTS-TREE 5.8.2
- Status: outside. Coverage row: 5.8.2.
- Checklist (23 Nov, top twenty no. 18; A32.08, A32.10, A05.21): missing: a confirm or hold-to-skip so one stray key cannot skip a scene, and a rule that control and the camera return at a usable place and facing after a scene. Gap for the design proof; status unchanged.

### 5.8.3 Staged scenes in play

- How it works: Scripted moments inside play take control away as little as possible: talk can run while walking or driving where a scene is staged that way (Alison asks her question from the back seat). No talk scene runs 60 s without a choice or control, and the clock stops in talk.
- Standard: No talk scene runs 60 s without a choice or control (ER-TALK-06) Test: H: control returns; S: timing
- Source: DESIGN §11 (no reference figure yet). Designed in: DESIGN §11, §15; ER-TALK-06; PARTS-TREE 5.8.3
- Status: unmeasured. Coverage row: 5.8.3.

### GV-06 How a deed is told: restraint and cruelty

- How it works: The telling carries how a deed was done, not only that it was: a man put down with three blows and left alone is told differently from one beaten further once he is down. The version is derived from people's beliefs, never a stored meter, and the worst telling once carried is never undone. The test is two seeded fights differing only in restraint, giving different told versions and different greetings within a game day.
- Standard: Two seeded fights differing only in restraint produce different told versions and different greetings within a game day. Test: B: paired fights; the told lines and greetings compared.
- Source: production/research/lane/gtavi/YARDSTICK.md and IDEAS-FOR-LEDGER.md (DECIDED by the design proof, for him to overturn). Designed in: GTAVI-MAP-2026-11-21 §GV-06; YARDSTICK.md; IDEAS-FOR-LEDGER.md idea 9; DESIGN §2
- Status: decided. Coverage row: GV-06.

## 5.9 Effects

Blood (light gore at most), rain, breath, smoke, broken glass.


### 5.9 Effects

- How it works: Effects named: blood (light gore at most, no cruelty as spectacle, never a beating at length), rain, breath, smoke and broken glass. Blood shows on a coat or pavement until washed by water or rain; breath shows in a fight (mashing makes him breathe hard in 6 to 10 jabs); smoking is allowed and glass stays broken until mended. A photosensitivity line shows once guns flash, and a 'reduce flashing' switch keeps flashes below three a second.
- Standard: Blood and light gore, no cruelty as spectacle (canon); photosensitivity line once guns flash Test: the gate; content check
- Source: canon; DESIGN §17 (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: canon content rule; DESIGN §17, §7; DEFINITIONS-2026-11-21 §AX-03; ONE-SHOT-PROMPT §15; PARTS-TREE 5.9
- Status: outside. Coverage row: 5.9.

## 5.10 Art direction and look reference

The Hook sheet, grade targets, the floors and the KCD2 frames everything is judged against.


### 5.10 Art direction and look reference

- How it works: The Hook sheet (pass 4) governs mood, palette and composition; dated photographs govern what things looked like and win. Every visual except clothes is judged against the Hook sheet and KCD2 frames, and yes only for 2026-grade work; references live only in production/reference/, never other games' screenshots.
- Standard: The Hook sheet (pass 4) governs mood, palette and composition Test: the gate uses it
- Source: RULINGS 21 Sep, 1 Oct (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 21 Sep, 1 Oct, 3 Oct, 17 Nov; CLAUDE.md gate
- Status: outside. Coverage row: 5.10.


## 5.11 Craft standards (Kiln and Unreal phases)

Added 23 Nov (keeper run 2) from the earlier teardowns, side by side: KCD2 and RDR2 (ledger-v2/research), Mafia: The Old Country (an Unreal-use reference only, never a design reference: game-clothing-pipeline, phase5-procedural, street-wear), inZOI (study-a-inzoi), Silent Hill 2 (study-b-silent-hill-2), the KCD2 coverage audit, the 145 study lines of 28 Oct and the trace of 18 Nov, with the project's own budgets (pre-production/4-BUDGETS.md of 3 Oct, production/specs/asset-budgets.json of 28 Oct). A Sonnet helper extracted the figures; every figure carries its source in square brackets. GTA V's teardown has not landed (GTA V is now installed on his PC; Sleeping Dogs, GTA IV and RDR2 follow); its column joins when it does.

Status of every standard below: decided (a craft standard the design proof may overturn), with its confidence: "figure" rests on a source number, "judgement" does not. None is measured: no teardown figure was taken to the five-sample rule, and most were read from the games' files before his ruling of 17 Nov barred it (C-205); "figure" below means the band rests on such a note, not on a measurement. Mafia, inZOI and Silent Hill 2 are studies of Unreal's use only, never design references (his ruling of 17 Nov names KCD2, GTA V and RDR2 as references). What things looked like (street width, props per 10 m, decals, wear, kit variety a newcomer sees) is governed by dated photographs (rulings of 21 Sep and 1 Oct); the Mafia figures on those rows are density checks only, to be replaced by counts from the dated photographs. Where KCD2 and Mafia both give a number, the low end of a band is KCD2's (the bar) and the high end Mafia's (what Unreal 5.x carries). Phases: Kiln (made by his Kiln pipeline: clothes first, then props, vehicles, buildings, people) or Unreal (assembled or judged in Unreal); both wait behind the browser prototype's evening (rulings of 20 and 21 Nov).
- Prior research: PRIOR-RESEARCH-INDEX section 6 (craft-teardowns sheets): nearly every reference number was read from game files before 17 Nov, so a lead. Public figures are few: Epic's MetaHuman levels (head 24,000 vertices over 8 levels, body 30,500 over 4), Lumen about 8 ms at 1080p, Warhorse's GDC 2025 abstract, one cars blog, inZOI's ModKit hair.
- Prior research: index section 6 items 7 and 8: add uses per mesh to the kit check (LEDGER records none today); storey heights from the dated photograph (terrace 2,925 mm, parade 3.4 m and 2.8 m); Mafia's 4.08 m belongs to Palermo; trial family of 24 to 32 distinct meshes a front is the basis once built and seen at the street camera.
- Prior research: index section 6 items 9 and 16: Rita's front carries 4096 maps (10.7 MB each, frame-headroom/OWNER-DUMP 16 Nov); the 16 Nov packaged dump held 340 uncompressed single-mip pictures (1,350 of 1,704 MB of textures) against a 1,000 MB pool; compressing them with mips is the largest saving any comparison shows.
- Prior research: index section 6 items 12, 13, 17: people in full detail under 10 m, buildings drawn to 192 m, props to 64 m (first guesses); Nanite off until a packaged re-test (3 Oct editor test: +0.7 ms); 55% of 3440 by 1440 (about 1892 by 792) matches Silent Hill 2's PS5 performance mode.
- Prior research: index section 6 items 14 and 15: the 9 Nov measure left 0.21 ms spare by day; one MetaHuman at 3.5 m costs about 0.31 to 0.36 ms against a 0.06 ms figure never measured; add no person or car until the packaged people ladder (0 to 40) gives a cost per person; KCD2's 3.5 ms and Mafia's 3 ms are whole-system budgets.

### 5.11.1 Sources


Folders are under production/research/ unless a full path is given.

- TD = ledger-v2/research/full/kcd2-rdr2-teardown-FULL.md (section letters as in the file); TS = ledger-v2/research/kcd2-rdr2-summary.md
- AUD-K = coverage-audit-kcd2/SUMMARY.md; AUD-R = coverage-audit-rdr2/SUMMARY.md
- S1, S4, S5, S6, S12 = aaa-reference/studies/01-npc-life, 04-street-world, 05-visuals, 06-characters-wardrobe, 12-tech-budgets (all 25 Oct 2026; Mafia and KCD2 read from their own files: read from files before 17 Nov, notes only, C-205)
- Read from files before 17 Nov (notes only, C-205): JACK, SWEAT, SURF, KIT, WEAR, INZ-C, INZ-F, SH2-F, and S1 to S12 above.
- JACK = game-clothing-pipeline/MAFIA-JACKET-2026-10-28.md; SWEAT = MAFIA-SWEATER-2026-10-29.md; SURF = MAFIA-CLOTH-SURFACES-2026-11-11.md; PIPE = PIPELINE-2026-10-28.md
- KIT = phase5-procedural/MAFIA-KIT-2026-10-28.md; TERR = TERRACE-KIT-TABLE-2026-10-29.md; PCG = PCG-COUNT-2026-11-07.md; WEAR = street-wear/MAFIA-WEAR-2026-10-28.md
- INZ-A = study-a-inzoi/STUDY-A-2026-11-01.md; INZ-C = CLOTHES-FILES-2026-11-06.md (with its REVIEW); INZ-F = FILES-READ-2026-11-06.md
- SH2-N = study-b-silent-hill-2/NOTES-2026-11-06.md (public sources only); SH2-F = FILES-2026-11-06.md (with its REVIEW)
- BUD = pre-production/4-BUDGETS.md (3 Oct; [M] measured on his PC, [I] its author's allocation); AB = production/specs/asset-budgets.json (28 Oct, the build's thresholds)
- FRAME = unreal-frame-budget/SUMMARY.md; PB = game-design/research/performance-budget.md (25 Aug, Unity era)
- RUL = RULINGS.md; SL = production/lane/synthesis/pack/04-study-lines.md (18 Nov); TRACE = production/lane/synthesis/TRACE.md (18 Nov); GROWS = production/research/lane/measurements/gtavi-g-rows-builder-2026-11-21.md (GTA VI, not GTA V)

Files named in the brief that hold no craft figures: TD, TS, AUD-K, AUD-R, coverage-audit/CROSS-CUTTING.md (systems and content mass only; the KCD2 and RDR2 figures they do give are NPC counts, script size and budget, used in the crowd row). TRACE and SL mark every craft line "left out: craft" (TRACE rows aaa-s04-02, s04-04, s05-07, s06-01, s06-04, s06-05, s12-01, s12-04), so the study lines add no new figures beyond S4, S5, S6 and S12. No performance budget or inZOI or Silent Hill 2 budget table landed on 21 to 23 November: the only "budget" files are BUD, AB, FRAME, PB and S12.

The last column of each table is LEDGER's own figure today, for comparison; it is not a game.

### 5.11.2 The teardowns side by side

#### People: People

| Row | KCD2 | RDR2 | Mafia: The Old Country | inZOI | Silent Hill 2 | LEDGER today |
|---|---|---|---|---|---|---|
| Hero character: triangles and textures | Male body 5 parts, 17,318 triangles at full detail, then 8,268 and 3,868; female body 16,588; unique head median 19,455 triangles, about 360 facial bones; a visible man about 71,000 at full detail with head, hair, hands (the study's own sum) [S6, Bodies and heads; Budgets]. Textures: body 2048; head 1024 colour and 2048 normal, two wrinkle maps (U) [S6]. People textures median 1.4 MB in the archive [S5, 7] | none | Body, head and hair triangle counts not exported (a gap) [S6]. Whole outfit about 43,000 [S6, Budgets]. Hero jumper file 41,204 triangles with its spare sleeves, 19,406 of them the worn jumper [SWEAT, 1]. Male skeleton 272 bones, 28 on coat flaps [S6]. Garment textures authored 4096, shipped 2048 [S6; JACK] | Triangles unread (no mappings file). Body file sizes only: SKM_PlayerMale 6,243,072 bytes, SKM_Female_Base 2,938,236 bytes (bytes, not triangles) [INZ-C, 4] | Triangles unread. Hero mesh files 26,049,138 to 52,500,119 bytes (Angela, James); 762 to 791 morph targets per main character mesh; textures by bulk size: Maria 68 bulk files, 15 at 4096 class (22,364,160 bytes), 18 at 11,182,080, 11 at 5,586,944 (estimates, format unread) [SH2-F, Clothes] | MetaHuman Optimized High: head 24,000 vertices, body 30,500 at LOD0, 8 head and 4 body LODs, 2K maximum, up to 100 MB; measured 27 to 43 MB of textures and 0.31 to 0.36 ms GPU each at 3.5 m [BUD 4.7, 4.2]. Epic gives vertices only, so no triangle figure [BUD 4.9] |
| Crowd character | One shared body per sex for ordinary people; distance mesh a pre-merged whole character of 2,597 to 3,100 triangles; Kutná Hora has 1,354 soul slots but only 139 hand-set appearances using 90 heads; 1,171 stock faces, 151 named [S6, Bodies; How crowds are dressed; S1] | none | Far away: single-mesh puppets (14 male, 7 female) and baked vertex-animated crowds [S6]; set-piece crowds have shared animation, no collision, no AI, 14 set-ups [S1, S12]. 32 male and 21 female body meshes; 780 outfit presets [S6] | none | none | Crowd outfit up to 8,000 triangles, 3 LODs, 1024 [AB crowd_outfit]. MetaHuman at LOD 2 or higher beyond 5 m, up to 15 MB unique each, 0.06 ms each (all [I]) [BUD 4.7] |
| Garment | Plain tunic 3 pieces: torso 3,734, arms 2,824, skirt 904 (7,462); only the skirt simulated, through a 270-triangle proxy; colour 1024, normal 2048; hose 6,806; caps about 5,400 (U); median whole outfit 24,532 men, 16,548 women (44 presets) [S6]. 2,139 human garment variants on about 513 meshes [S6] | none | Plain vest-jacket 19,131 / 8,509 / 4,781 / 1,505 triangles, vertices 12,226 / 6,109 / 3,758 / 1,467 [JACK, table]. Medians at full detail: top 21,994 (87; 6,112 to 57,369), trousers 9,566 (61; 5,396 to 23,022), shoes 6,718 (18; 1,780 to 9,964), hat 4,495 (59; 1,578 to 14,797) [S6, Budgets]. Jumper 19,406 / 8,108 / 4,452 / 1,632 [SWEAT, 1]. Textures shipped 2048 (jackets), mostly 1024 for tops and bottoms, 512 for shoes and hats [S6]. Jacket about 12 px/cm at 2048, jumper about 16 [JACK; SWEAT]. Chaos cloth on 10 meshes (8 garments), none for crowd; flaps on rigid-body bones [S6] | One skeletal mesh per garment, skinned to the body; adult files: Top 250, Bottom 161, Full 167, Outer 93, Shoes 118, Under 102, Acc 268, Custom 348, Unique 97, total 1,604; Top 1,792 rows on 295 meshes; four maps (D, N, M, ARM) per material, sizes inferred as 512 to 2048 class (U); triangles unread [INZ-C, 1 to 5]. No garment physics asset found beside the meshes (one test file) [INZ-C, 6] | Clothes sit in one skeletal mesh per character (inferred); Chaos cloth assets per hero mesh: Maria 5, Angela 4, James 8, Mary 3 [SH2-F, Clothes]. No triangle figure | Caps: jacket 22,000, jumper 20,000, trousers 10,000, shoes 6,000, accessory 4,000 triangles; 4 LODs (2 for accessories) keeping 100, 47, 25, 9 per cent at screen sizes 1.0, 0.4, 0.15, 0.08; textures 2048, shoes 1024, accessories 512 [AB kinds, garment_jacket]. Principal outfit "up to 25,000" in total [BUD 4.7] |
| Face and hair | Heads unique, median 19,455 triangles; hair cards alpha-tested, median 9,700 triangles, 39 haircuts in 9 colours (U); beards fitted per head, 1,445 beard meshes [S6, Hair and hats] | none | 101 male and 20 female unique heads, each on a MetaHuman head animation blueprint; hair strands (183 male rows on about 24 grooms) plus hair cards; a hat swaps hair for a cap-hair mesh in 147 of 269 hatted male presets; hair casts shadows to half its distance [S6; S12]. Triangle counts not exported | Heads 171 male and 165 female files; 3,134 hair files; 39 hair physics assets; body shape 71 rows with 17 modifier values [INZ-C, 2, 6, 7]. No triangle figure | Strand hair "with physics-driven movement" is a reviewer's taste statement, no figure [SH2-N, 2] | MetaHuman faces; strands on at most two people within 5 m, cards beyond; up to 16 MB per card groom (forum or search summary only) [BUD 4.7] |

#### Buildings and ground: Buildings and ground

| Row | KCD2 | RDR2 | Mafia: The Old Country | inZOI | Silent Hill 2 | LEDGER today |
|---|---|---|---|---|---|---|
| Building facade or kit piece | Each house one whole-building mesh plus placed window and doorway pieces; window kit about 219 window and 38 shutter mesh names; plot 12.6 to 12.9 m, gable to the street; building textures median 2.8 MB [S4, Unique buildings; S5, 1, 7]. No triangle figure | none | A base shell per house type from a Houdini generator plus 0 to 3 floor shells; storey step median 4.08 m, window pitch median 3.99 m, floor shells 3.9 to 5.9 m high, widths 7.8 to 17.2 m; 35 trim sets, mostly 2048 authored, 1024 shipped; in-game median 575 px/m [KIT, 1, 2]. Game-wide 540 facade, 585 roof, 60 interior, 1,163 distant meshes [S4]. No triangle figure | none | File counts only: Art/Enviro/LakeViewHotel 4,393, Buildings 3,471 [SH2-F, question 4] | Module up to 8,000 triangles, 3 LODs, up to 4 materials, shared 4096 x 2048 trim sheets; whole frontage up to 150,000, up to 12 materials [AB; BUD 4.7]. Whole street today 183,416 triangles over 112 meshes [BUD 4.7, M] |
| Ground and terrain materials | Terrain 2048 x 2048 m and 4096 x 4096 m [TD A1]. 135 shared surface materials: 26 ground, 24 wall, 19 wood, 8 stone, 5 metal, 2 glass; one material per asset (7,572); no wet-street material found; rain layer to 150 m (40 m at low) [S5, 4, 6] | none | One global wetness drives roughness to 0.1 flat and 0.2 on slopes; 232 puddle decals in Palermo; 2,461 decals of 180 materials; 91 pieces of ground dressing in a 73 m street; 253 masters and 1,189 instances in the shared library; wall textures 4096 (106 of 186) or 2048 (73) [S5; S4; WEAR, 1] | none | r.DBuffer on; 1,925 files in Art/texture/Decals, 782 in BlendMaterial (file counts) [SH2-F, question 3] | Roughness: asphalt 0.06, paving 0.1, kerb 0.15; research found 0.16 read as dry [S5 settings sheet]. Textures 512 px/m, 2048 tiling sets [BUD 4.7] |
| Kit reuse per block | Town: 232 building instances from 77 meshes, about 3 uses each; most reused house 7 times, sheds and lean-tos 11 to 19; library 465 templates, 5,553 structure meshes [S4]. Garments: 2,139 variants on about 513 meshes [S6] | none | Palermo main-street group (about 100 buildings): 33,986 placements of 433 meshes, 78.5 uses per mesh, 88 per cent kit, 32 meshes used once (about 7 per cent unique, the keeper's division). The 73 m street alone: about 2,350 placements of about 150 meshes (about 15 uses), 18 to 19 facade pieces from 2 families [S4]. A whole front: median 103 pieces, 26 distinct meshes (p90 49); a storey band 32 pieces, 15 meshes; one house family 62 to 94 meshes; 22 per cent of placements take a different material from their mesh's own [KIT, 1, 2] | Garments only: Top 1,792 rows on 295 meshes, Bottom 1,151 on 141, Jacket 1,403 on 93 [INZ-C, 3] | none | Target only, nothing built: 30 to 45 meshes a house family, each front at least 15 distinct meshes [KIT, 5.1]; terrace table of 39 meshes [TERR, 3]. Quay Street today: 43 props and 10 decals in its scene file [S4, Targets] |

#### Props and vehicles: Props and vehicles

| Row | KCD2 | RDR2 | Mafia: The Old Country | inZOI | Silent Hill 2 | LEDGER today |
|---|---|---|---|---|---|---|
| Small prop | Texture medians in the archive: small props 0.35 MB, furniture 0.7 MB [S5, 7]. Loose meshes stored apart, so props not countable [S4] | none | 4.9 true props per 10 m of street (17.4 with ground dressing, 21 with decals and facade add-ons); plant pots 1.2, boxes and buckets 1.0, laundry 0.7 per 10 m [S4]. Props cast shadows to a quarter of hair's distance [S12]. No triangle figure | none | File counts only: Props/Trash 677, Props/Lamp 892, Props/Street 522 [SH2-F, question 4] | Up to 1,500 triangles, 2 LODs, 512, up to 2 materials [AB prop_small]. Today's clutter 950 to 7,548 triangles each [BUD 4.7] |
| Large prop | none | none | none | none | none | Up to 15,000 triangles, 3 LODs, 2048, up to 10 hulls; medium prop up to 5,000, 3 LODs, 1024 [AB prop_large, prop_medium] |
| Vehicle | Horses (21 in the town) are the only transport counted; no vehicle figure [S4, Vehicles, plants and weather] | Trains and stagecoaches named as moving world furniture; no figure [TD, matrix row 15] | None parked in the measured street; traffic spawned; no figure [S4] | none | none | Parked car up to 40,000 triangles, 4 LODs, up to 8 materials, 2048, up to 6 hulls, at most 6 in view, 0.5 ms in all [AB car; BUD 4.5, 4.7]. Scripted hatchback 15,294 triangles, 9 materials [BUD 4.7] |

#### LODs and distances: LODs and distances

| Row | KCD2 | RDR2 | Mafia: The Old Country | inZOI | Silent Hill 2 | LEDGER today |
|---|---|---|---|---|---|---|
| LOD count and switch distances | Three mesh levels for people plus a merged whole-character distance mesh; switch distances not read (named blind spot) [S6]. Distant-detail tree: 8,000 m layer roots, median node radii 33, 181, 45, 12 and 6 m [S12, Memory and streaming] | none | Four levels at screen sizes 1.0, 0.4, 0.15, 0.08 keeping a median 47, 25 and 9 per cent [S6]; the engine's default groups keep 25, 12.5, 6 per cent at 1.0, 0.3, 0.15, 0.1 [AB, garment_jacket]. Civilians simplify from 10 m, look-at paused beyond 32 m [S1]. Distant detail: 6 layers, 9 levels deep [S4] | none | none (HZB occlusion off in High, Medium, Low presets; no LOD figure) [SH2-F, question 2] | Garments 4 levels as Mafia; crowd outfit 3; module 3; props 2 to 3; car 4; hill rows one merged distance version, up to 2,000 triangles a house at 110 to 206 m [AB; BUD 4.7]. Nanite off [AB; DECISIONS 3 Oct via AB] |
| Draw or detail distances | View-distance ratio 50 / 100 / 180 (low / default / top); detail ratio 10 / 25 / 300; vegetation ratio 70 / 110 / 250; sun cascades 4 / 5 / 5; shadow pool 2,048 / 4,096 / 16,384; shadow-casting lights up to 10 / 16 / 32 with 8 per frame (6 in PS5 performance mode); PS5 performance mode 60 fps at 2560 x 1440 output, FSR 0.75, view ratio 80 [S12, Quality levels]. Light reach median 4.3 m [S5, 3] | none | World-partition loading ranges x0.8 / 1 / 1 / 1.5; 27,680 runtime cells; Palermo main grid 73 cells at 128 m, props grid 32 m; Nanite visible-cluster cap 1,048,576 to 2,000,000; 60 fps profile: TSR at 83 per cent with dynamic resolution 40 to 83 per cent; lamp spots drawn to 30 m; volumetric fog 80 m; decal fade-out median 0.044 screen size [S12; S4; S5, 3; WEAR, 3; KIT, 3] | Cloth physics "only player / by distance" setting exists, distance value unread [INZ-C, 6] | Shadow max resolution 1500 (High), 1280 (Medium, Low); cascades 3 (Epic), 2 (others); volumetric fog grid 7 / 164 (Epic), 8 / 148 (High), 8 / 128 (Medium), 16 / 96 (Low) [SH2-F, question 2] | Draws at 55 per cent of 3440 x 1440 (ladder tries 100, 70, 55) [BUD 4.1]. At most 6 shadow-casting lights in view; up to 300 decals in view; up to 3 million triangles in view and 2,000 mesh sections (all [I]) [BUD 4.5, 4.7] |

#### Load and memory: Load and memory

| Row | KCD2 | RDR2 | Mafia: The Old Country | inZOI | Silent Hill 2 | LEDGER today |
|---|---|---|---|---|---|---|
| Crowd count and traffic against frame time | About 2,400 NPCs simulated at a 60 fps target by AI level of detail, about half in Kuttenberg [TD, A1]. Full detail for 70 people within 150 m (80 within 180 to 220 m at top levels); people update budget 3.5 ms (2.5 ms in PS5 performance mode); a test quest in Kuttenberg holds 1,000 to 2,500 people [S12; S1] | People despawn when the player walks away [AUD-R]. Market view 2 to 7 people (the street-life sheet, cited second-hand in GROWS, not read) | Animation budget 3 ms; civilians freeze when unseen for 3 s beyond 70 m, never within 10 m; set-piece crowds animation-shared [S12; S1]. Measured street: 134 placed actors; Palermo level 7,555 actors [S4] | Five sleepy characters on screen after 11 p.m. "may cause lag"; no figure [INZ-A, 2] | none | 3 principals near 1.0 ms and up to 12 passers-by 0.7 ms, 1.7 ms in all [I], from 0.31 to 0.36 ms per MetaHuman [M] [BUD 4.5]. Standing slice median 13.32 ms, GPU 11.43 ms [BUD 4.2, M]. 0.07 ms per simulated person was measured in Unity, not Unreal [FRAME; BUD 4.6] |
| Texture budget in memory | Pool sized to card memory: 4,096 MB at 6 GB, 5,120 at 8 GB, 8,192 at 12 GB; PS5 2,240; mesh stream pool 768 MB [S12, Memory and streaming] | none | Texture pool 1,200 / 1,500 / 2,000 / 2,000 MB by level; top-level pools textures 2,000, virtual textures 323, Nanite 300 MB; memory thresholds at 3, 7, 15 GB; a 6 GB card falls at level 1, 1,500 MB [S12]. Texture sizes by count: 4096 21 per cent, 2048 36, 1024 38 [S5, 7]. Colour and normal ship one mip down [WEAR, 1] | Peak 12.1 GB at 4K maximum with frame generation and the language-model feature, against up to 10 GB without (a guide's measure, second-hand); alone about 5,004 MiB on a 10 GB card (one player's Linux reading) [INZ-A, 2]. Language model budget 2,048 MB [INZ-F, A2] | On-disk texture bulk per hero, not memory: Maria 625,623,040 bytes, Angela 346,570,752, James 1,335,058,432 (estimates) [SH2-F] | Game 6.0 GB of the 9.4 GB usable (voice 2.8 GB, margin 0.6); textures a fixed streaming pool of 1,500 MB, 2.4 GB with non-streamed; meshes 0.6, skinned 0.5, engine and render targets 1.6 GB [BUD 4.4, I]. S12 gives 1.5 to 2 GB of textures at "High" |

37 of 70 cells hold a figure; RDR2 is blank in 13 of 14 rows (its sources hold content mass, not craft figures); inZOI and Silent Hill 2 give counts and file sizes but almost no triangles.

### 5.11.3 How clothes and faces are built

Clothes: skinned meshes, only loose parts simulated; the shoulders judged in Unreal [RUL 30 Sep]. Built in his Kiln pipeline [RUL 13 Nov, 18 Nov]: real sewing patterns, drape in zero gravity, retopologise to quads, bake colour with occlusion, normal and one packed map, mask-only painting coloured in an Unreal material, weights transferred from the body and hand-fixed, then LODs [PIPE, 2]. One base body per sex for the crowd, garments made to it, the skin under each garment hidden; a second body only where a cast member needs one [S6, For LEDGER; RUL 2 Oct stop on six-body fitting]. People wear only gated garments from CC0, unmarked CC-BY, CC BY 4.0 for clothes and their accessories (makers credited, brand marks painted out; ruling of 30 Oct), Blender (including Kiln, rulings of 13 and 18 Nov) or Marvelous Designer; the bar for principals is 2026 grade at talking distance against KCD2 frames; the floor for passers-by is plain, period-plausible, no clipping, judged at 8 m [RUL, Clothes]. Marvelous lapses 26 Nov; what it made stays [RUL 19 Nov].

Faces: MetaHuman faces cast from the casting sheets; Ron P2, Sheila S4 (with hair), Darren S6, Tom L1 are frozen; the other eleven cast from approved text [RUL 25 Sep, 30 Sep, 8 Oct]. Hair strands stay; no hair skill until one character's hair passes the full gate [RUL 3 Nov, 9 Nov]. Prepared lines use Epic's audio-driven mouths [RUL 1 Oct].

Note: RUL 20 and 21 Nov put Kiln, hair and the crowd, and all Unreal work, behind the browser prototype's evening. The phases below say who does what once that opens.

### 5.11.4 The standards

| Kind of asset | Standard | Rests on (per-asset limits are allocations inside 4-BUDGETS' totals, unproven until the first profile; with Nanite off every triangle is drawn again into each shadow cascade, BUD 4.3) | Phase | Confidence |
|---|---|---|---|---|
| Jacket or coat (principal) | LOD0 18,000 to 22,000 triangles (S6's principal target; KCD2's tunic set of 7,462 is a different garment, kept as comparison); 4 LODs keeping about 47, 25, 9 per cent at screen sizes 1.0, 0.4, 0.15, 0.08; textures shipped 2048 | KCD2 tunic set 7,462 [S6] to Mafia median top 21,994 [S6] and S6's LOD medians (the jacket itself keeps 44, 25, 8 per cent [JACK]); AB already enforces 22,000. inside BUD's allocation, unproven until the first profile | Kiln | figure |
| Jumper (principal) | LOD0 15,000 to 20,000; LODs about 42, 23, 8 per cent; 2048 | Mafia jumper 19,406 / 8,108 / 4,452 / 1,632 [SWEAT] | Kiln | figure |
| Trousers | LOD0 8,000 to 10,000 (S6's target; KCD2 hose 6,806 as comparison); 1024 to 2048 | KCD2 hose 6,806 [S6]; Mafia median 9,566, pair 7,906 at 1024 [S6] | Kiln | figure |
| Shoes | Low shoes up to 6,000 a pair; boots up to 10,000 a pair as their own kind (not a waiver); 512 to 1024 | Mafia shoe median 6,718, range 1,780 to 9,964 [S6]; the two boots waivers sit at 10,416 [AB waivers] | Kiln | figure |
| Principal's whole outfit | 25,000 to 43,000 triangles at LOD0 summed (KCD2's median 24,532 and 4-BUDGETS' 25,000 the target, Mafia's median about 43,000 the ceiling), at most 3 principals near; confirmed or cut by the first profile | BUD 4.7 (25,000); S6 (KCD2 24,532 men; Mafia about 43,000); asset-budgets has no outfit cap (the garment caps sum to 58,000, which is above both games). See C-204 | Kiln | judgement |
| Crowd outfit | Up to 8,000 triangles, 3 LODs, 1024; judged at 8 m; passes only with no clipping or placeholder | AB crowd_outfit [I from BUD]; Mafia drops far crowds to puppets and vertex-animated meshes [S6]; KCD2 median outfit 16,548 to 24,532 is higher, so 8,000 is cheaper than both | Kiln | judgement |
| Accessory (hat, bag, watch, spectacles) | 500 to 4,000 triangles, 2 LODs, 512 | Mafia hat median 4,495 at 512 [S6]; AB accessory | Kiln | figure |
| Garment texel density | About 12 px/cm at 2048 for jackets, about 16 px/cm for knit | Mafia jacket 11.9 and jumper about 16 px/cm [JACK; SWEAT] | Kiln | figure |
| Cloth motion | Skinned only; simulate loose parts only (coat tails, skirt hem), up to 300 simulated points a garment, up to 2 simulated garments in view; no crowd garment simulates; flaps on short rigid-body bone chains | Mafia: Chaos cloth on 10 meshes, none for crowd, 68 of 74 garment animation blueprints on rigid bodies [S6]; KCD2: only hems and skirts, 1,926 pendulum joints [S6]; Silent Hill 2: 3 to 8 cloth assets per hero [SH2-F]. The 300-point cap is a forum figure [BUD 4.7] | Kiln builds, Unreal judges | figure for the shape, judgement for 300 |
| Garment colour | One layered garment material; 4 to 8 colourways a mesh from tint and ID mask, not new meshes | Mafia: 1,213 of 1,416 garment materials children of one master, median 4 to 10 colourways [S6]; KCD2 4 to 6 [S6]. Saves meshes and card memory | Unreal | figure |
| Garment wear | Grime, scratch, blood and wet as material values, never extra meshes | Both games [S6, Dirt, blood and wear]; fits the grime strategy [RUL 21 Sep] | Unreal | figure |
| Crowd dressing | Presets with slots and tags, random pick per slot, a hat left out by chance 20 to 80 per cent; pool about 10 tops, 8 bottoms, 6 coats, 6 hats, 5 shoes at 4 to 8 colourways | S6 recipe scaled down from both games; hundreds of looks for a few dozen people | Unreal | judgement |
| Bodies | One base MetaHuman body per sex for the crowd, garments made to it, covered skin hidden; second body only for a cast member | KCD2 one body per sex [S6]; Mafia 126 of 176 tagged garment meshes for the base body [S6]; ruling 2 Oct | Kiln | figure |
| Principal face | MetaHuman Optimized High, 2K maximum, up to 100 MB, at most 3 near, up to 0.35 ms GPU each, passes the full gate and his look | Measured 0.31 to 0.36 ms each [BUD 4.2, M]; KCD2 unique heads median 19,455 triangles [S6]. Epic gives vertices, KCD2 triangles: not comparable | Unreal (people come last in Kiln) | figure |
| Passer-by | MetaHuman at LOD 2 or higher beyond 5 m; at most 12 in view; 1K textures; up to 15 MB unique each; up to 0.06 ms each | BUD 4.7 [I]; KCD2 distance mesh 2,597 to 3,100 triangles [S6] | Unreal | judgement |
| Distance crowd | Beyond the last LOD, a merged whole-person mesh of 2,600 to 3,100 triangles or a vertex-animated set-piece; switch distance set by the first profile | KCD2 and Mafia [S6; S1]; distances not in any source | Unreal | figure for the mesh, judgement for the distance |
| Hair | Strands on at most 2 people within 5 m; cards for everyone else and for the crowd; a hat swaps in a cap-hair mesh | Mafia strands plus cards, cap-hair swap [S6]; KCD2 cards [S6]; BUD 4.7; ruling 9 Nov keeps strands | Unreal | figure |
| People update and significance | People unseen for 3 s beyond 70 m freeze, never within 10 m; animation up to 3 ms; people update up to 3.5 ms | Mafia [S12; S1]; KCD2 3.5 ms [S12]. Plugins exist in 5.8 [S12] | Unreal | figure |
| People in full detail | At most 3 principals plus 12 passers-by in view (pass or fail); KCD2's 70 within 150 m is a ceiling far above a street | BUD 4.5; S12 | Unreal | judgement |
| Building module | Up to 8,000 triangles, 3 LODs, up to 4 materials, shared 4096 x 2048 trim sheets; simple box collision | AB; neither game gives a facade triangle figure. Merged-geometry draw cost, not triangles, is the constraint [PB, Unity era] | Kiln (buildings come after clothes, props, vehicles) | judgement |
| Whole frontage | Up to 150,000 triangles, up to 12 materials, about 6 near frontages | AB; today's whole street is 183,416 triangles [BUD 4.7, M] | Kiln | judgement |
| Kit variety | Each whole front shows at least 15 distinct meshes; a house family 30 to 45 meshes; at most 10 per cent of kit meshes used once; each house differs from both neighbours in wall variant or joinery paint; checked by script | Mafia: storey band median 15 meshes, front median 26, family 62 to 94, 32 of 433 used once, 22 per cent material swaps [KIT; S4]. Half of Mafia's family size fits plainer terraces | Unreal | figure |
| Kit grid and fit | Opening pieces keep their size; linear pieces fit within 10 per cent; sizes in names; pivots at bottom face or sill | Mafia: 88 per cent of windows and doors within 10 per cent of scale, 54 per cent of meshes carry their size [KIT, 1]. Grid size set by dated photographs (C-208) | Kiln | figure |
| Wall and trim texel density | 512 px/m at walking distance; 1,024 px/m only within 2 m (interiors) and small print | BUD 4.7 geometry (1,720 / d pixels per metre at 3440 wide); Mafia ships a median 575 px/m [KIT, 2] | Unreal | figure |
| Texture size mix | No texture over 4096; about a fifth at 4096, a third at 2048, two fifths at 1024 or smaller | Mafia 21 / 36 / 38 per cent [S5, 7]; BUD cap 4096 [AB] | Unreal | figure |
| Street width and dressing | Front to front 9 to 15 m; at least 5 true props per 10 m of the walked street, thinner elsewhere | KCD2 median 9.9 m, Mafia 14.7 m; Mafia 4.9 props per 10 m from one 73 m sample [S4] | Unreal | figure |
| Wear decals | Median 1 per wall, up to 6 where the player looks; leak stains about 2 in 5; up to 300 in view; fade-out near 0.044 screen size; grime mostly in the material | Mafia median 1, p90 6, 38 to 40 per cent leaks, fade 0.044 [WEAR; KIT, 3]; 300 is BUD [I] | Unreal | figure |
| Interiors | Real rooms only where the story goes; mapped or fake rooms elsewhere; a real room behind glass up to 100,000 triangles, 2 LODs, at most 4 in view | Mafia 24 fake rooms in about 8,100 windows [S4]; BUD 4.7 for the 100,000 [I] | Unreal | judgement |
| Hill and distance | Up to 2,000 triangles a house, rows merged, one atlas | BUD 4.7 [I]; KCD2 pre-merged distance meshes [S6, S12] | Kiln (buildings) | judgement |
| Small prop | Up to 1,500 triangles, 2 LODs, 512, up to 2 materials, shadow casting off | AB prop_small [I]; no game gives a prop triangle figure. Many instanced props are cheap; shadow draws are not (PB, Unity era) | Kiln | judgement |
| Medium and large prop | Up to 5,000 (3 LODs, 1024) and up to 15,000 (3 LODs, 2048); up to 10 hulls | AB [I] | Kiln | judgement |
| Parked car | Parked background cars up to 25,000 triangles and Tom's car up to 40,000, 4 LODs, up to 8 materials, 2048, at most 6 in view, 0.5 ms in all | AB car; BUD 4.5 [I] (a single cap of 40,000); background and hero bands from the prior research index section 6 item 11 (field scans, a public studio blog: background 5,000 to 25,000, hero 40,000 to 80,000; C-262). Mafia gives no car figure | Kiln | judgement |
| Wet ground | The wet street dark, glistening, mirroring sky and buildings, puddles as water (his ruling of 3 Oct); the means: one global wetness value driving roughness, between Mafia's 0.1 flat and LEDGER's 0.06 asphalt, with 0.16 the upper bound (it reads dry) | RUL 3 Oct (the bar); S5 settings sheet; BUD research (0.16 reads dry) | Unreal | ruling for the bar, judgement for the values |
| LOD rule | Every static and skeletal mesh carries levels, each about half the last, none above 0.6 of the one before; Nanite stays off | AB lod_step_max 0.6; DECISIONS 3 Oct via AB; Mafia 47 / 25 / 9 per cent | Unreal | figure |
| Frame | Median up to 16.0 ms planned (16.7 ruling), slowest 1 per cent up to 25 ms, never above 33.3 ms; GPU median up to 14.0 ms, with the voice running | RUL 23 Sep; BUD 4.1 [M and I]; today's slice 13.32 ms median [M] | Unreal | figure |
| Memory | Game up to 6.0 GB of card; texture pool fixed at 1,500 MB (2.4 GB with non-streamed) | RUL 24 Oct; BUD 4.4; Mafia pool 1,500 MB for a 6 GB card [S12]; KCD2 pool 4,096 MB at 6 GB [S12] | Unreal | figure |
| Lights | At most 6 shadow-casting lights in view at night; KCD2's 8 a frame (6 in performance mode) noted as a ceiling; window lamps cast within 15 m | BUD 4.5 [I]; KCD2 [S12] | Unreal | judgement |
| Drawing smaller | Fixed 55 per cent of 3440 x 1440 now; try a dynamic range once the voice shares the card | RUL 23 Sep; Mafia 60 fps profile 40 to 83 per cent [S12]; KCD2 FSR 0.75 [S12] | Unreal | figure |

Frame, memory, lights and drawing smaller also stand in chapter 08 (8.1.1 and 8.11).
