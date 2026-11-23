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

### 5.1.4 Clothes

- How it works: Clothes are Kiln garments (skinned meshes, only loose parts simulated). Tom wears three outfits across the rise (as he arrived, a decent jacket, a good overcoat) and a dark coat for nights, each changing how strangers speak to him and which doors open; prices are a second-hand coat 15 pounds, the decent jacket 45, the good overcoat 90. The floor is plain, period-plausible, no modern giveaways (contrast-stitched slim jeans, trainers), no clipping or holes, nobody frozen stiff; passers-by are judged at eight metres, principals at talking distance on the 2026 bar against KCD2 frames.
- Standard: Clothes' floor: plain, period-plausible, no modern giveaways, no clipping; principals at talking distance on the 2026 bar Test: the gate; his eye in the game's camera
- Source: RULINGS Clothes (3 Oct, 19 Nov) (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: DESIGN §14; DEFINITIONS-2026-11-21 §G8; DESIGN-ADDENDUM §A21; RULINGS Clothes 3 Oct, 29 Sep, 19 Nov; production/art/clothing/RUBRIC.md
- Status: outside. Coverage row: 5.1.4. Conflicts settled: C-113.

### 5.1.5 Crowd variety

- How it works: Named only; not designed beyond: a crowd count by hour and place (design pass 4: the parade front 12 to 20 people in the busy bands, 5 to 10 from 18:00 to 22:00, 2 to 5 from 22:00; one frame 4 to 10, GD-02) and the rule that a crowd extra who catches any slot of a deed becomes kept, with a fixed face, a coat and a home. No repeat distance or variety rule exists.
- Standard: none yet: repeat distance and variety rules to be set Test: S: no identical pair in one frame; his eye
- Source: risk R5 (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: DEFINITIONS-2026-11-21 §G9, §RT2-10; COVERAGE 5.1.5; 6-RISKS R4; PARTS-TREE 5.1.5
- Status: outside. Coverage row: 5.1.5.

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

### 5.2.5 Crowd and idle animation

- How it works: Idles must not hold still: looping idles with a random start, a play rate of 0.9 to 1.1 and neighbours differing, so nobody stands frozen. The corner plan's baseline had speakers moving in 59 of 60 four-second windows and the street's extras in 12 of 18; work, smoke and talk idles are not built.
- Standard: No stiff idle; nobody frozen stiff (clothes floor) Test: the gate
- Source: RULINGS; risk R4 (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: CORNER-PLAN-2026-11-02 step 3; BASELINE-2026-11-02 row g; RULINGS Clothes floor 3 Oct; 6-RISKS R4; DESCRIPTION-2 §7
- Status: outside. Coverage row: 5.2.5.

### 5.2.6 Body language of knowing

- How it works: Knowing shows in the body before any line, on one ladder: notice, watch, comment, avoid, refuse, confront. A watcher's head turns at the start of the 1.2 s it takes to know him (a glance is 0.35 s), at least 0.8 s before identification; also a longer look, a pause in a walk, two heads together, a step back at night, a figure at a lit window. Nobody who knows nothing shows it, and a told version never shows above a seen one.
- Standard: D29: posture first Test: H: ER-EYES-01
- Source: D29 (his ruling or canon). Designed in: D29; DESIGN §2 and ER-EYES-03; DEFINITIONS-2026-11-21 §2.4.3; DESCRIPTION-2 §5; PARTS-TREE 5.2.6
- Status: measured. Coverage row: 5.2.6.

### 5.2.7 Clip sourcing and cleanup

- How it works: Clips come from Epic's samples, MetaHuman's movement clips, Mixamo on his account, and CMU motion capture inside the game (never resold or shipped as a library). Pexels and Pixabay clips serve only as motion references and controls, each licence read and recorded; he never films or performs anything. Raw Mixamo files stay out of git, history included.
- Standard: Sources allowed: Epic samples, MetaHuman, Mixamo on his account, CMU inside the game; Pexels/Pixabay as references Test: each clip's source and licence recorded
- Source: RULINGS People's moves; 9, 12 Nov (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS People's moves, 9 Nov, 12 Nov, 19 Nov; license-allowlist item 11; PARTS-TREE 5.2.7
- Status: outside. Coverage row: 5.2.7.

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

### 5.3.2 Materials and grime

- How it works: Grime is the strategy: a seeded wear layer calibrated to real reflectances. Damage stays until mended: blood on a pavement stays until rain or a bucket washes it, a forced door shows for a day, broken glass stays until the owner mends it; marks keep across save and load. The pavement, road, brick and daylight are checked against real values and photographs of a wet overcast street.
- Standard: D53; calibrated to real reflectances Test: the gate
- Source: D53; RULINGS 21 Sep (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 21 Sep, 29 Oct (the look); D53; ONE-SHOT-PROMPT §15 lasting marks; PARTS-TREE 5.3.2
- Status: outside. Coverage row: 5.3.2.

### 5.3.3 Wet street

- How it works: The wet street is dark, glistening, mirroring sky and buildings, with puddles as water (ruling 3 Oct); the weather is dry overcast, drizzle or rain, with one wetness value driving look, hearing and who is out. A wet road takes about 3 to 14 hours to dry and puddles days, with rain on about 12 days a month; it is never sunshine in the friends' build.
- Standard: Ruling 3 Oct bars for the wet street Test: the gate
- Source: RULINGS 3 Oct (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 3 Oct, 5 Oct; DESIGN §6; LIGHT-WEATHER-VALUES-2026-11-17; PARTS-TREE 5.3.3
- Status: outside. Coverage row: 5.3.3.

### 5.3.4 Shop glass and windows

- How it works: Windows have white frames, sash bars and sky in the glass; shop glass shows the street (real glass, ruling 4 Oct, for Mickey's front room). A window is a watcher only when a figure shows at it, head and shoulders at the glass; the pawnbroker's window is lit at night; a broken window shows scattered glass and an empty frame, which stays until mended.
- Standard: Ruling 3 Oct (windows); ruling 4 Oct (real glass) Test: the gate
- Source: RULINGS 3, 4 Oct (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 3 Oct, 4 Oct, 1 Oct; DESIGN §6 ER-NIGHT-02; ONE-SHOT-PROMPT S12; PARTS-TREE 5.3.4
- Status: outside. Coverage row: 5.3.4.

## 5.4 Lighting and picture

Light and grade.


### 5.4.1 Day exposure and sky

- How it works: By day the exposure stays one stop darker, never brightened again, and the sky is a photograph. In the lamp numbers the exposure pin is 4.0 by day and 0.4 by night. Grey range only (dry overcast, drizzle, rain), no sunshine in the friends' build, and sunset around 16:00 in mid-November.
- Standard: Ruling 29 Oct; D40 Test: checked against real values
- Source: RULINGS 29 Oct, 15 Sep (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 29 Oct, 15 Sep, 5 Oct; D40; LIGHT-WEATHER-VALUES-2026-11-17; PARTS-TREE 5.4.1
- Status: outside. Coverage row: 5.4.1.

### 5.4.2 Night lighting

- How it works: Night is pools of lamp light with darkness between, lit windows, never one orange wash. The pool under a lamp is about ten times the night fill (the real range is 10 to 25); real side streets are lit to 3.5 to 6 lux average with the dimmest point 1 to 2.5 lux. Tom and the ground 5 m round him must always be visible above a brightness floor kept in the one tuning table.
- Standard: Ruling 1 Oct; ER-NIGHT-01 brightness floor Test: H: darkest-spot screenshots; the gate at night
- Source: RULINGS 1 Oct; DESIGN §6 (his ruling or canon). Designed in: RULINGS 1 Oct, 7 Oct; DESIGN §6 ER-NIGHT-01; LIGHT-WEATHER-VALUES-2026-11-17; PARTS-TREE 5.4.2
- Status: measured. Coverage row: 5.4.2.

### 5.4.3 Grade, grain and depth of field

- How it works: Named only; not designed beyond: the presentation (grade, grain, depth of field) is owed since D28 and was to be built early; one colour grade is shared between the browser prototype and Unreal. Depth of field and motion blur each get their own switch.
- Standard: D28 presentation built early Test: the gate
- Source: RULINGS 15 Sep (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 15 Sep, 18 and 19 Nov; DEFINITIONS-2026-11-21 §AX-03; PARTS-TREE 5.4.3
- Status: outside. Coverage row: 5.4.3.

## 5.5 Sound

The street heard; sound carries the town's eyes. CC0 only (D26).


### 5.5.1 Footsteps and foley

- How it works: Footsteps differ by surface and gait, for Tom and for others; a footstep at three in the morning carries about 3.6 m and at noon nothing, and sound carries twice as far in the small hours. A tester with the picture off can tell a walk from a run. The research found the standard method uses spawned sounds around the listener capped by place and hour.
- Standard: Footsteps by surface and gait (DESIGN §17) Test: H: sound-only test; his ear
- Source: DESIGN §17 (no reference figure yet). Designed in: DESIGN §17, §2, ER-SND-01; ONE-SHOT-PROMPT §8; STREET-SOUND-SOURCES plan; MEASUREMENTS-NEEDED A7; PARTS-TREE 5.5.1
- Status: unmeasured. Coverage row: 5.5.1.

### 5.5.2 Doors and impacts

- How it works: Doors creak, hit and latch; a forced door or broken glass is the loudest thing in a quiet street, heard at its force reach, and the window breaks loudly and the glass stays until mended. A forced door shows on the door for a day.
- Standard: DESIGN §17 Test: H: sound-only test; his ear
- Source: DESIGN §17 (no reference figure yet). Designed in: DESIGN §17, §4; ONE-SHOT-PROMPT S12 and §8; PARTS-TREE 5.5.2
- Status: unmeasured. Coverage row: 5.5.2.

### 5.5.3 Street beds and states

- How it works: The street sound has three parts: quiet looping beds, short one-shots spawned around the listener and capped by place and hour, and placed sources each heard within a set distance. It has four states of the hour (not named in the sources). The reference found a quiet street spawns at most 3 far voices and 3 activity sounds by day and none at night.
- Standard: DESIGN §17; STREET-SOUND-SOURCES plan Test: H: sound-only test; his ear
- Source: DESIGN §17 (no reference figure yet). Designed in: DESIGN §17; STREET-SOUND-SOURCES-AND-LISTENING-PLAN-2026-11-17 (Professional method); PARTS-TREE 5.5.3
- Status: unmeasured. Coverage row: 5.5.3.

### 5.5.4 Rain and rooms

- How it works: One rain value fades the sound layers and halves voices; rain cuts all noise reach. Rooms change the echo at the doorway; in the prototype there is a reverb when inside but no echo at doorways.
- Standard: DESIGN §17 Test: H: sound-only test; his ear
- Source: DESIGN §17 (no reference figure yet). Designed in: DESIGN §17, §6 ER-NIGHT-03; ONE-SHOT-PROMPT §8; PARTS-TREE 5.5.4
- Status: unmeasured. Coverage row: 5.5.4.

### 5.5.5 Car sound

- How it works: 1990 by sound: the car's engine note runs about 28 Hz at idle to about 210 Hz at the limit (a small four-cylinder idling at 800 to 900 rpm, limit 6,000 to 6,500). The gearbox is automatic by ruling, so a change is a short, softer dip (length not yet set), and tyre squeal starts from about 80% of the grip limit as a warning. The car is heard within about 44 m by day, the horn about 60 m.
- Standard: Driving sheet M12; ruling 18 Nov Test: H: sound-only test; his ear
- Source: DESIGN §17 (no reference figure yet). Designed in: DESIGN §5, §17; CAR-NOISE-ANCHORS-2026-11-18; FEEL-TARGETS-DRIVING M12; RULINGS Cars 18 Nov; PARTS-TREE 5.5.5
- Status: unmeasured. Coverage row: 5.5.5.

### 5.5.6 Fight sound

- How it works: A blow sounds four layers: whoosh from blow start, impact from contact, a pain cry after contact, and an enemy shout before his blow lands. The impact must come within 0.034 s of contact, the whoosh from 0.05 s before to 0.10 s after the start, the pain cry 0.05 to 0.30 s after contact, and the shout at least 0.40 s before. There is never combat music.
- Standard: Melee sheet; DESIGN §7 Test: H: sound-only test; his ear
- Source: DESIGN §17 (no reference figure yet). Designed in: FEEL-TARGETS-MELEE-2026-11-18 C13; DESIGN §7, §17; ER-MUSIC-01; PARTS-TREE 5.5.6
- Status: unmeasured. Coverage row: 5.5.6. Conflicts settled: C-115.

### 5.5.7 The mix

- How it works: The quietest lead voice sets the mix and talk lowers the beds; silence is the commonest music. Sliders cover master, voices, effects, street and music, plus a 'voices clear' switch that lifts voices over the street by 6 dB and a 'loud noise softening' switch that clips gunshots to a door slam's level.
- Standard: DESIGN §17 Test: H: sound-only test; his ear
- Source: DESIGN §17 (no reference figure yet). Designed in: DESIGN §17; DEFINITIONS-2026-11-21 §AX-04; ADDENDUM §A8; PARTS-TREE 5.5.7
- Status: unmeasured. Coverage row: 5.5.7.

## 5.6 Voices

Spoken lines.


### 5.6.1 Cast voices

- How it works: Voices are chosen per character and cast only on his yes: Sheila p267 and Ron p227 on Pocket (live and prepared lines), Darren recast on Pocket as VCTK p286 (Newcastle), Agar p226, the dispatcher p280. Danny (p243), June (p277) and Father Walsh (his July voice) get a listening page and are cast only on his yes. Voices are judged by ear; the accent checker only screens.
- Standard: Sheila p267, Ron p227, Darren p286, Agar p226, dispatcher p280; others on his yes Test: his ear
- Source: RULINGS voices (3 Oct to 19 Nov) (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS Voices 3 Oct, 26 and 27 Oct, 19 Nov, 30 Sep, 24 Sep; PARTS-TREE 5.6.1
- Status: outside. Coverage row: 5.6.1.

### 5.6.2 Voice generation and watermark

- How it works: Voices are made on his PC by the local voice program (Pocket kept, 19 Nov; consent risk his); prepared lines for Ron and Darren use an acted reference, and the watermark (D50) stays on generated speech. No paid voice service and no hiring, ever.
- Standard: D50 watermark; Pocket kept (19 Nov) Test: packaged speech measure
- Source: RULINGS D50, 19 Nov (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 25 Sep, 24 Sep, 29 Sep, 19 Nov; D50; PARTS-TREE 5.6.2
- Status: outside. Coverage row: 5.6.2.

### 5.6.3 Thinking sound and timing

- How it works: Before an answer comes a short thinking sound with a glance, cut when the answer starts, and never a loading sign. A reply is heard within 2 s or the written line plays; a line slower than 8 s is dropped with an in-character brush-off. The Unreal build misses the 2.0 s bar at 2.02 s.
- Standard: Ruling 28 Sep; no loading sign Test: S: timing
- Source: RULINGS 28 Sep (his ruling or canon). Designed in: RULINGS 28 Sep; DESIGN §11 ER-TALK-01; PARTS-TREE 5.6.3
- Status: measured. Coverage row: 5.6.3.

## 5.7 Music

Silence is the commonest music; never combat music.


### 5.7.1 Radio programmes and period songs

- How it works: Named only; not designed beyond: music comes from places (a radio in the caff, a shop, the office set, a window at night, the chapel organ), all invented or made for the game, on licences that never expire. Music is heard only where it plays in the world (DEFINITIONS P09, 21 Nov); whether a short made-for-the-game score goes under cut scenes and act ends is Q11 for him, and none is built meanwhile; no music starts or changes because a fight or chase starts. The pirate radio station is owed by the brand bible.
- Standard: No real bands, lyrics or brands (canon); content from the allowlist or the studio's own, only on licences that never expire Test: canon gate; his ear
- Source: canon Brands and law (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: canon Brands and law; ADDENDUM §A8; DEFINITIONS-2026-11-21 §P09; ER-MUSIC-01; RULINGS Sources
- Status: outside. Coverage row: 5.7.1. Conflicts settled: C-116, C-117.

### FIT-P09 Music made for the game, placed in the world

- How it works: No music station in the cab. Music is heard only where it plays in the world (a radio in the caff, the chapel's organ, a record through a window), and every piece is made for the game and listed with its maker, since canon makes every band fictional with no real lyrics and no period recording is licensed. The check is the audio files listed against the allowlist and canon's fictional-brands rule.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (his ruling or canon). Designed in: DEFINITIONS-2026-11-21 §P09; FIT-CHECK-2026-11-21 P09 and question 4 note; canon Brands and law; ADDENDUM §A8
- Status: measured. Coverage row: FIT-P09. Conflicts settled: C-118.

## 5.8 Cameras and cut scenes

The camera system and the few short scenes.


### 5.8.1 Camera rig by state

- How it works: One camera arm reads rows by Tom's state: street (the Between picture's height, 86 degree lens, 3.1 m back, feet in frame), run, room and talk (closer), fight (wider, 3.5 to 5.0 m back, both men's feet in at least 90% of frames), and car (about 5.8 m back, widening with speed). Blends take one second or less, shake obeys Reduce motion, and the camera never ends inside a wall, body or car. The field of view is a setting from 75 to 100 degrees, default 86.
- Standard: Ruling 28 Oct (street, talk closer, fights wider); blends 1 s or less; shake obeys Reduce motion Test: S: frames counted; B clip detector
- Source: RULINGS 28 Oct; DESIGN §17 (his ruling or canon). Designed in: RULINGS 28 Oct, 21 Nov; DESIGN §17 (ER-CAM-01, ER-CAM-02); FEEL-TARGETS-MELEE C10; DEFINITIONS-2026-11-21 Design pass 3 header; PARTS-TREE 5.8.1
- Status: measured. Coverage row: 5.8.1. Conflicts settled: C-119.

### 5.8.2 Cut scenes

- How it works: Cut scenes are few, short and skippable. Every scene is skippable and at most 60 s, under 5% of the first hour is watched, and no stretch passes 3.5 min without control. The only one specified is the ferry shot, about 20 s, which ends by itself or at once if skipped. The description says no long cutscenes and no watched opening.
- Standard: Every scene skippable and at most 60 s (ER-FIRST-02); few short skippable cutscenes (23 Sep) Test: S: skip works; length measured
- Source: RULINGS 23 Sep; DESIGN §15 (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 23 Sep (genre); DESIGN §15 ER-FIRST-02; ONE-SHOT-PROMPT S01; DESCRIPTION-2 §3; PARTS-TREE 5.8.2
- Status: outside. Coverage row: 5.8.2.

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
