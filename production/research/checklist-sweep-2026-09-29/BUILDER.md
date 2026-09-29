# The builder's checklist sweep for the thirty-minute friends' build, 29 September 2026

What this is: Jafar's request of 29 September. The archived checklist (production/archive/ROADMAP-checklist-to-2026-09-24.md, 979 rows) read for the builder's lane, which had not been swept since it was archived: controls, camera, sound, interface, animation, lighting and everything else the Unreal game, its people and its packaging own. Each row is marked NEEDED for the thirty-minute build for his friends (ROADMAP: the block becomes the Hook, Mickey's interior, more residents, a session worth repeating), LATER, OUT under his genre rulings G0 to G12 (DECISIONS archive, 23 September) and the research's own outs, or DONE with its evidence. The town's lane (talk content, the simulation, the relay and the business) was swept twelve times by the town (production/research/checklist-sweep-2026-09-28/) and is left out here except where the builder shows what the town decides.

THE TEST FOR NEEDED: a friend installs the packaged game on their own Windows PC and plays thirty minutes: walks the Hook and Mickey's office, talks to people in their voices, does the deed, is seen, hears of it later, saves, quits and comes back. Needed is what that friend would plainly miss or be hurt by. Keyboard and mouse only for this build; controllers later. The floor he ruled (menus, controls, camera, settings, accessibility) keeps its basics here and its fuller forms later.

## Counts

| verdict | rows |
|---|---:|
| needed | 359 |
| later | 440 |
| out | 113 |
| done | 43 |
| town's lane | 24 |

Needed by owner: builder 328; builder and town 28; clothing, then builder 3. The rows are fine-grained: one title menu closes about twenty of them, one settings screen about twenty more. Two are much bigger than a row looks: moving traffic (his G4 says it is in the street now; nothing moves today) and a running clock with waits (the first week's handovers need it too).

## Needed, in work packages

### 1. Launch, the first run and a friend's copy (23)

- A01.01: a friend's copy starts from its own shortcut, with its data inside (no -LedgerRepo)
- A01.02, A01.14: a sign of life at once, and progress while shaders compile on first launch (or a shipped shader cache)
- A01.03: the talk program and the voice start with the game, no commands
- A01.04: the window and a title card say LEDGER
- A01.05, A01.06, A01.07: sensible resolution, the main monitor, a sane first volume
- A01.09, A01.10: subtitles on before the first line; text size and volume reachable from the title menu
- A01.11 (builder and town): the AI notice (wired 29 Sep) and where typed words go, shown before the first talk
- A01.12: with no network the town still sees, remembers and talks in its written lines
- A01.13 (builder and town): plain words when talk cannot be reached (town's text, the builder's screen)
- A01.16: a plain message when the talk program or the voice cannot start
- A01.17: first-run choices and settings kept
- A2: first-run detection of the card and a default quality preset: friends' PCs differ
- A4: the build's version on the title screen, so a friend's report names it
- Q5: a minimum specification to give friends before they install
- V9, T1: a packaged copy friends can download and update (the route, Steam playtest or a download, is his call when we get there)
- T5: the third-party attributions shipped inside the build (CC BY, OFL where used)
- U3: a way to report a problem as well as bad output (the report key is wired)
- A48.17: a crash leaves a log and a way to send it

### 2. Title and pause menus, saving and quitting (45)

- A02.01, A02.02, A02.03: New game, Continue and Quit on a title screen; New game warns before replacing a save
- A02.04, A02.05, A02.06, A02.07, A02.08, A02.09, A02.14, A02.15, A02.19, A02.20: menus that work with mouse and keys, always a way back, confirm before destructive steps
- A02.17: typed talk takes the keyboard's text, backspace, accents and paste
- A39.01, A39.02, A39.03, A39.04: say when the game saves; autosave at the day's turns; a sign while saving; a save on quit
- A39.07, A39.08: the save named by day and hour; confirm before overwriting
- A39.10: Tom back where he stood, facing the same way, never inside a wall
- A39.13, A39.14, A39.21 (builder and town): the world, the people's memories and the talk restored; a save from an older build still loads (town's Core side done)
- A39.17, A39.18, A39.19, A39.25, A39.26, A39.27, A39.28: no death loop, a failed save keeps the last, a full disk said plainly, settings per machine, a loading screen, control only when ready, back to the title on a failed load
- A48.16, A48.20: repeated save and load, and a new build over an old save, with nothing lost
- A40.01, A40.02, A40.03, A40.04, A40.05: Esc pauses the world, sound and people; resume without a queued step; losing focus pauses
- A40.07, A40.08, A40.09, A40.10, A40.11, A40.12, A40.13: back to title, quit to desktop with a save, no process or sound left behind, settings kept

### 3. Settings (17)

- A41.01, A41.02, A41.04, A41.05, A41.06, A41.07, A41.11, A41.17, A41.18, A41.20, A41.21, A41.22: resolution, window mode, refresh, a frame limit, vsync, presets that matter, brightness, UI scale, aspect, a safe revert, kept
- A42.01, A42.02, A42.11, A42.13, A42.19: master, voices, effects volumes heard while set; mouse sensitivity and inversion; the controls explained

### 4. Controls and the camera (32)

- D1, E4: keyboard and mouse throughout, with look sensitivity
- A03.01, A03.02, A03.03, A03.08, A03.09, A03.13, A03.18, A03.20, A03.23: prompt, consistent, frame-rate-independent keys and mouse; no double presses; diagonals not faster; no mouse acceleration
- A03.12: typing to someone never walks Tom (WASD inside the talk box)
- A03.14, A03.15, A03.16: no stuck movement after a menu or alt-tab; the click that closes a menu does nothing else
- A04.14: the controls listed in the pause menu
- A05.01, A05.02, A05.03, A05.04, A05.05, B03: free look, a good distance and field of view, Tom readable, smoothed but not detached
- A05.06, A05.07, A05.08, A05.13: the camera never sees through walls, recovers after, handles lamp posts and bollards, never fights the mouse
- A05.09: fixed in the editor game on 29 Sep (the camera kept out of Tom); still to be walked in the packaged build
- A05.10: a usable view inside Mickey's office
- A05.15, A05.24: into and out of talk without a jolt; movement follows the camera after any cut
- A05.22, A05.23: no shake, a level horizon

### 5. Walking and collision (26)

- A06.01, A06.02, A06.03, A06.04, A06.05, A06.06, A06.07, A06.08, A06.09, A06.10: walk, run, start, stop and turn with feet that agree, in every direction, relative to the camera
- A06.11, A06.12, A06.13: kerbs, the office's steps and the street's slope taken without catching
- A06.15, A06.16, A06.21: no snagging on clutter, sliding along walls, never wedged
- A12.01, A12.03, A12.04, A12.18: solid ground and walls where they look solid, doors that admit him, bodies steady on uneven ground
- A12.11, A12.12: people and Tom never pass through one another, walkers included; a way past someone in a doorway
- A12.15, A12.16, A12.17: the smashed window's remnants and sound agree (FINDINGS: its inside card shows through)
- A20.15: a way out of a stuck spot (stand-up or return-to-pavement)

### 6. People: faces, hair, clothes, animation, looking (28)

- A08.01, A08.02, A08.04, A08.05, A08.06, A08.13, A08.14, A08.15: complete, right-sized people with believable hands, eyes and mouths, shadows, and faces that hold from near to far
- A08.07: hair that holds up in the street's light (Darren's man's haircut first)
- A08.03, A08.12, A09.22 (clothing, then builder): clothes that fit, show no gaps and move with the body (sewn by the clothing session, fitted by the builder)
- A09.01, A09.02, A09.03, A09.06, A09.08, A09.10, A09.18, A09.21, A09.23: breathing, varied idles, planted feet, matched strides, clean blends, heads a little free of the torso, never a default pose
- A10.01, A10.03, A10.04, A10.06, A10.07, A10.14: eyes and torso that follow within limits, eye contact that breaks, blinks, back to what they were doing after
- A10.08: a face that broadly fits the line it speaks

### 7. People who live: routines, avoiding, reacting (15)

- A13.01, A13.02, A13.03, A13.04, A13.05, A13.06, A13.07, A13.24, A13.25, A13.26: people who walk the town's routines (CastDay ported, not yet moving them), avoid each other and Tom, react to a bump, use doors, and never pop in or out in view
- A13.14, A13.16, A14.04, A14.05: people turn toward the smash and tell a passer-by from a vandal
- A15.19: the crime is its own deliberate key: nothing harmless-looking smashes a window

### 8. A running clock, waits, day and night (3)

- A25.10, A25.11, A25.12 (builder and town): a clock that runs (two game minutes a second, the town's ruling), waits that stop for the town, the light following the hour (town list ci; today the game only jumps between scenes)

### 9. The street busy by the hour (8)

- A25.02: ambient sound for the street and the office
- A25.01, A25.03, A25.04, A25.06, A25.09, A25.13, A25.16: the street busy with different doings, the right numbers by hour, continuous when he turns away

### 10. Mickey's office, doors and using things (24)

- A11.01, A11.02, A11.03, A11.04, A11.05, A11.06, A11.07, A11.08, A11.09: a prompt on the thing he can use, in reach, not through walls, talk before open, saying what will happen and why not
- A11.12, A11.13, A11.15: doors that move as they block, never trap him, and a locked office door that says so
- A11.23: using a thing and smashing it are plainly different acts
- J9, A21.02, A21.03, A21.04, A21.11, A21.17, A21.18: Mickey's office entered (list item 11), agreeing with its front, with room for Tom and the camera, closed doors reading closed
- A21.13, A21.14, A21.15: places worth going to, near enough to walk, always a way back
- A22.17: the office's dressing holds from both sides of its window

### 11. Light and image (12)

- A22.02, A22.09, A22.16, A48.07: enough detail at walking distance; no flicker, popping or late-appearing objects
- A23.03: shadows that follow people and moving lights
- A23.06, A23.07: exposure that eases between the office and the street; the night street playable
- A23.10, A23.13, A23.14, A23.16: reflections that agree, a stable image without shimmer or ghosting, the hill sitting in the sky
- A24.03: if rain falls, not through roofs; wind and rain sound that follow the weather

### 12. Sound (29)

- B02: if rain falls, not through roofs; wind and rain sound that follow the weather
- A28.03, A28.04, A28.06, A28.07, A28.08, A28.10, A28.13, A28.14, A28.15: moving sources carry sound, distance quietens, the office muffles the street and sounds like a room, no hard jumps
- A29.01, A29.02, A29.03, A29.07, A29.09, A29.10, A29.15, A29.16, A29.17, A29.18: footsteps in time, by surface and pace, stopping when he stops; doors and the smash heard; varied, once, on time
- A30.01, A30.02, A30.05, A30.06, A30.10, A30.12, A30.13, A30.14, B01: speech clear over the street and level across speakers, ambience ducking under it, no clipping or clicks, pausing with the game

### 13. Talk on screen and in the voice (14)

- A30.03, V1: a voice for each person who talks: Sheila has none that holds her English accent
- N7 (builder and town): speech soon enough to feel like talk: the voice half of the delay (list item 6)
- A31.01, A31.02, A31.03, A31.04, A31.05, A31.15, A31.16, A31.17: start and leave a talk plainly, an acknowledgement, facing at a talking distance, lips roughly in time, the voice from the speaker, subtitles that match
- A31.09 (builder and town): walking away mid-reply (town list 9 for the talk's side)
- A31.11: the last lines recoverable after an interruption
- A31.18: thinking sounds for Ron and Darren (his yes); Sheila has none

### 14. Interface: hints, prompts, subtitles, notes, the envelope (60)

- A04.01, A04.02, A04.03, A04.04, A04.16: a clear hand-over to the player, a first view of something useful, a safe street to try walking and looking
- A04.05, A04.06 (builder and town): a clear first purpose and destination (day one: Sheila's walk-round, town list cg)
- A04.07, A04.08, A04.09, A04.10, A04.12, A04.13 (builder and town): hints the first time they matter, in the player's keys, long enough to read, stopping once learned (the town's hint book; the builder's screen)
- A44.01, A44.02, A44.03, A44.05, A44.06, A44.07, A44.09: subtitles and captions from the start, naming the speaker, long enough, sizeable, with the smash shown as well as heard
- A32.01, A32.10: the evening's cut and day one's walk-round read as watching, then hand back control sensibly
- A32.12 (builder and town): skipping Sheila's walk-round still counts her as met (town list cg)
- A33.01, A33.02, A33.04, A33.05, F2 (builder and town): a light note of what Tom is doing, reachable from the pause menu, updating as it changes
- A36.01, A36.02, A36.03: the envelope of night one: in his pocket, said when taken and given
- A34.04, A34.05, A34.10, A34.11, A34.12, A34.13, A34.14, A34.15: prompts that don't hide the thing, notices long enough and never piled up, no overlaps, nothing on screen during a cut, the world's running state clear
- A43.01, A43.02, A43.04, A43.05, A43.06, A43.16: readable text at his screen size and a friend's, a size setting, backgrounds behind subtitles, nothing by colour alone
- A46.01, A46.03, A46.04, A46.13, A46.14: plain words, time to read, clear effects of a menu change, a content note (menace, a smashed window), settings kept
- A45.07, A45.10: menus work from the keyboard; Esc always pauses
- A47.03, A47.05, A47.06, A47.07, A47.09, A47.11: no missing glyphs or placeholder keys; names and keys consistent; British dates and money
- A49.05, A49.11 (builder and town): screenshots work; what is collected (the session record, typed words) said plainly (town's words)

### 15. Traffic (his G4: in the street now) (8)

- A26.05, A26.08, A26.09, A26.12, A26.14, A26.20, A26.21, A26.22: a few cars passing on the carriageway, wheels turning, lamps lit at night, engine sound, keeping lane, stopping for people (his G4: a street with no traffic feels dead). Bigger than it looks

### 16. Frame rate and stability (11)

- A48.01, A48.02, A48.03, A48.06, A48.08, A48.09, A48.11, A48.12, A48.13, A48.14, A48.19: 60 fps at his screen with the voice running (70.7 today), even frames, no first-use hitch, textures in time, thirty minutes without decline, settings and devices changed safely, alt-tab

### 17. Testing and the friends' session (4)

- J03: the AI tester plays the friends' build with nothing serious open
- V8, U5 (builder and town): the AI tester on every friends' build; the friends' session itself (the runbook is the town's)
- V4: no real brand or mark in view (the pillar box and kiosk marks made up, 29 Sep)

## Every row of the builder's lane

| id | stage | feature | verdict | why, or the evidence |
|---|---|---|---|---|
| A08.07 | 1 | Hair that behaves plausibly under the game's lighting | needed | hair that holds up in the street's light (Darren's man's haircut first) |
| A08.08 | 1 | Skin, fabric, leather and metal that look different | done | done by 24 Sep: in one frame of the corner, 24 Sep: the MetaHuman's skin with its pores and sheen, the knitted jumper and denim beside him, patent shoes, the car's painted meta |
| A08.15 | 1 | Detail changes with distance that do not transform identity | needed | complete, right-sized people with believable hands, eyes and mouths, shadows, and faces that hold from near to far |
| A09.01 | 1 | Idle breathing and small posture changes | needed | breathing, varied idles, planted feet, matched strides, clean blends, heads a little free of the torso, never a default pose |
| A09.02 | 1 | Idle variation rather than a conspicuous repeating loop | needed | breathing, varied idles, planted feet, matched strides, clean blends, heads a little free of the torso, never a default pose |
| A09.24 | 1 | No identical synchronised idle motion across a crowd | done | done by 24 Sep: six people, each started at its own phase of its loop (street-people.json), no two in step, 23 Sep: [frame](production/art/compare/hook-unreal-2026-09-23/pair-0 |
| A21.01 | 1 | Human-scale doors, stairs, furniture and streets | done | done by 24 Sep: measured on a straight-on Unreal frame at 100 px a metre, 24 Sep: the side door stands 1981 mm (the British standard door, found within 4 mm), the shop door 900 |
| A21.05 | 1 | Readable routes through ordinary environments | done | done by 24 Sep: a pavement on each side behind a kerb, the carriageway between, the yard's mouth and the road running on to the quay: where a person walks and where a car goes  |
| A21.06 | 1 | Landmarks that help orientation | done | done by 24 Sep: the lettered fronts (MICKEY'S, FISH MARKET, RITA'S, the laundry), the red post box and phone box, and the hill that closes the north end tell which way you face |
| A21.07 | 1 | Visually distinct areas rather than indistinguishable repeated streets | later | the Hook's more buildings (stage 5) |
| A22.01 | 1 | Complete visible surfaces without holes or missing faces | done | done by 24 Sep: no holes or missing faces anywhere in the Hook view in Unreal, both terraces, roofs, road and kerbs, 24 Sep: [frame](production/art/compare/stage1-2026-09-24/ho |
| A22.02 | 1 | Appropriate detail at normal viewing distance | needed | enough detail at walking distance; no flicker, popping or late-appearing objects |
| A22.03 | 1 | Textures that do not stretch conspicuously | done | done by 24 Sep: on straight-on Unreal frames at 100 px a metre, brick, render, slate, paint and paving keep one scale across every wall, pier, fascia and roof, with no smear al |
| A22.04 | 1 | Texture scale consistent with real object size | done | done by 24 Sep: measured, not eyeballed, 24 Sep: the brick map carries 96 courses over its 7.2 m (75 mm, a British course) and reads about 7.5 px a course beside the 0.55 m fas |
| A22.05 | 1 | Materials distinguishable as wood, metal, glass, cloth and stone | done | done by 24 Sep: each reads as itself: the crates' and pallet's bare wood, the cars', bins' and lamp posts' metal, the shop glass with the room behind it, the clothes' knit and  |
| A22.06 | 1 | Object edges that do not all look infinitely sharp | done | done by 24 Sep: every piece of the street shorter than 12 m and longer than 0.25 m is rounded 6 mm at export (two steps at the corner, one elsewhere; cf1a0e62); close up, the t |
| A22.07 | 1 | Buildings and props visibly grounded rather than floating | done | done by 24 Sep: grounded, 23 Sep: [frame](production/art/compare/hook-unreal-2026-09-23/pair-06-presentable.png) |
| A22.08 | 1 | Believable joins between walls, floors, roofs and terrain | done | done by 24 Sep: on a straight-on frame the joins are built, not butted: slate eaves over a gutter and a dentil course, sills and heads let into the brick, fascias on consoles,  |
| A22.09 | 1 | No conspicuous flickering between overlapping surfaces | needed | enough detail at walking distance; no flicker, popping or late-appearing objects |
| A22.10 | 1 | Variation that disguises obvious repeated components | done | done by 24 Sep: the six-bay parade is six different fronts (Mickey's, the fish market, Rita's, the laundry, a letting board, an empty unit), each with its own paint, sign and d |
| A22.11 | 1 | Wear and dirt consistent with use and exposure | done | done by 24 Sep: the scene file's ten stains stand as decals in Unreal (stainsStood=10, f0de9751): water streaks down the party walls, moss at the west row's foot, broken tarmac |
| A22.12 | 1 | Furnishing and clutter consistent with a place's function | done | done by 24 Sep: each thing is where its trade puts it: crates out in front of the fish market, pallet, crates and an oil drum at the yard's mouth, cones, barrier and a skip whe |
| A22.13 | 1 | Signs and labels that are readable when they matter | done | done by 24 Sep: MICKEY'S, RITA'S, FISH MARKET read at the Hook view, 23 Sep: [frame](production/art/compare/hook-unreal-2026-09-23/pair-06-presentable.png) |
| A22.14 | 1 | Period and setting consistency in conspicuous objects | done | done by 24 Sep: nothing conspicuous in the Hook view is out of 1990: invented period saloons, a red post box and phone box, a 60 cm dish (ruled citable), lettered fascias, sash |
| A22.15 | 1 | Objects that remain recognisable across lighting conditions | done | done by 24 Sep: the car, the woman, the lamp post, the shopfronts and the signs all read by day and by night from the same camera, 24 Sep: [day](production/art/compare/stage1-2 |
| A22.16 | 1 | Detail changes with distance that do not cause conspicuous shape popping | needed | enough detail at walking distance; no flicker, popping or late-appearing objects |
| A22.17 | 1 | Interior dressing that survives viewing from both directions | needed | the office's dressing holds from both sides of its window |
| A23.01 | 1 | Lighting that establishes readable shapes and space | done | done by 24 Sep: under the sheet's overcast the street still reads in depth: the facades' planes, reveals and roofs separate by shade, and the haze steps the hill back behind th |
| A23.02 | 1 | Shadows connecting people and objects to their surroundings | done | done by 24 Sep: close up in the corner, a person's feet and a car's wheels sit in their own contact shadow on the flags and the road, and nothing hovers, 24 Sep: [crop](product |
| A23.03 | 1 | Shadows that broadly follow moving characters and lights | needed | shadows that follow people and moving lights |
| A23.04 | 1 | No major light leaking through solid walls | done | done by 24 Sep: at night the lit shops light their own windows and nothing else; no glow through brick or at wall joins, 24 Sep: [night A](production/art/compare/stage1-2026-09 |
| A23.05 | 1 | Indoor light levels that differ plausibly from outdoors | done | done by 24 Sep: by night the shops are lit rooms in a dark street and by day their rooms sit a little under the daylight, as the sheet's windows do, 24 Sep: [night](production/ |
| A23.06 | 1 | Exposure changes that do not blind the player during ordinary transitions | needed | exposure that eases between the office and the street; the night street playable |
| A23.07 | 1 | Dark areas that remain playable under the intended rules | needed | exposure that eases between the office and the street; the night street playable |
| A23.09 | 1 | Switchable lights whose appearance and illumination change together | later | switchable lights and effects-heavy scenes: none in the friends' build |
| A23.10 | 1 | Reflections that broadly agree with the environment | needed | reflections that agree, a stable image without shimmer or ghosting, the hill sitting in the sky |
| A23.12 | 1 | Glass that behaves consistently as transparent, reflective or obscured | done | done by 24 Sep: each kind keeps its behaviour: shop glass shows the room through a sheen; house windows are dark panes behind white sashes, some netted; car glass is dark and r |
| A23.13 | 1 | Stable image edges without distracting shimmer | needed | reflections that agree, a stable image without shimmer or ghosting, the hill sitting in the sky |
| A23.14 | 1 | Motion rendering without severe ghost trails | needed | reflections that agree, a stable image without shimmer or ghosting, the hill sitting in the sky |
| A23.15 | 1 | Consistent colour and brightness across gameplay and cutscenes | later | G6: the handful of short scenes (the arrival with the suitcase) |
| A23.16 | 1 | Distant scenery integrated with sky and atmosphere | needed | reflections that agree, a stable image without shimmer or ghosting, the hill sitting in the sky |
| A23.17 | 1 | Important targets remaining distinguishable amid visual effects | later | switchable lights and effects-heavy scenes: none in the friends' build |
| A24.05 | 1 | Wet surfaces looking different from dry ones | done | done by 24 Sep: standing water in puddles and gutters, 23 Sep: [frame](production/art/compare/hook-unreal-2026-09-23/pair-06-presentable.png) |
| A41.14 | 1 | Film grain, chromatic aberration and similar presentation controls where used | later | finer display settings, after the presets |
| A48.07 | 1 | No large visible objects appearing suddenly at short range | needed | enough detail at walking distance; no flicker, popping or late-appearing objects |
| P3 | 1 | Post-processing chain | done | the street's light and grade in production/specs/unreal-look.json, on the street frames of 29 Sep |
| V6 | 1 | Art direction and a style bible | later | a style bible: the concept sheet governs until the town |
| A05.01 | 2 | Free horizontal and vertical looking within the intended camera model | needed | free look, a good distance and field of view, Tom readable, smoothed but not detached |
| A05.02 | 2 | A useful default viewing distance in third person | needed | free look, a good distance and field of view, Tom readable, smoothed but not detached |
| A05.04 | 2 | Camera framing that keeps the controlled character readable | needed | free look, a good distance and field of view, Tom readable, smoothed but not detached |
| A05.05 | 2 | Camera movement that does not lag so much that control feels detached | needed | free look, a good distance and field of view, Tom readable, smoothed but not detached |
| A05.06 | 2 | Camera collision that prevents seeing through walls | needed | the camera never sees through walls, recovers after, handles lamp posts and bollards, never fights the mouse |
| A05.07 | 2 | Camera recovery after an obstruction clears | needed | the camera never sees through walls, recovers after, handles lamp posts and bollards, never fights the mouse |
| A05.08 | 2 | Smooth handling of poles, foliage and other small obstructions | needed | the camera never sees through walls, recovers after, handles lamp posts and bollards, never fights the mouse |
| A05.09 | 2 | Character fading or another solution when the camera gets too close | needed | fixed in the editor game on 29 Sep (the camera kept out of Tom); still to be walked in the packaged build |
| A05.13 | 2 | Camera behaviour that does not repeatedly fight manual input | needed | the camera never sees through walls, recovers after, handles lamp posts and bollards, never fights the mouse |
| A05.14 | 2 | Predictable recentering, if provided | later | stairs to the flat, recentering, crouch framing: when the Hook has them |
| A05.15 | 2 | Smooth transitions between exploration, aiming and conversation | needed | into and out of talk without a jolt; movement follows the camera after any cut |
| A05.16 | 2 | Appropriate framing when crouching or going prone | later | stairs to the flat, recentering, crouch framing: when the Hook has them |
| A05.21 | 2 | Camera recovery after a cutscene without disorienting rotation | later | G6: the handful of short scenes (the arrival with the suitcase) |
| A05.23 | 2 | Stable horizon and manageable camera motion | needed | no shake, a level horizon |
| A05.24 | 2 | A sensible relationship between camera direction and movement after a camera cut | needed | into and out of talk without a jolt; movement follows the camera after any cut |
| A06.01 | 2 | Walking, jogging and running appropriate to the control scheme | needed | walk, run, start, stop and turn with feet that agree, in every direction, relative to the camera |
| A06.02 | 2 | A usable sprint where the game's travel distances imply one | needed | walk, run, start, stop and turn with feet that agree, in every direction, relative to the camera |
| A06.03 | 2 | Acceleration that fits the character's apparent weight | needed | walk, run, start, stop and turn with feet that agree, in every direction, relative to the camera |
| A06.04 | 2 | Deceleration that fits the intended responsiveness | needed | walk, run, start, stop and turn with feet that agree, in every direction, relative to the camera |
| A06.05 | 2 | Turning that looks and feels connected to the feet | needed | walk, run, start, stop and turn with feet that agree, in every direction, relative to the camera |
| A06.06 | 2 | Stationary turning without impossible foot rotation | needed | walk, run, start, stop and turn with feet that agree, in every direction, relative to the camera |
| A06.07 | 2 | Backward movement with an appropriate gait | needed | walk, run, start, stop and turn with feet that agree, in every direction, relative to the camera |
| A06.08 | 2 | Sideways movement with an appropriate gait | needed | walk, run, start, stop and turn with feet that agree, in every direction, relative to the camera |
| A06.09 | 2 | Smooth transitions between movement speeds | needed | walk, run, start, stop and turn with feet that agree, in every direction, relative to the camera |
| A06.10 | 2 | Consistent movement relative to the camera or facing convention | needed | walk, run, start, stop and turn with feet that agree, in every direction, relative to the camera |
| A06.11 | 2 | Reliable movement over small kerbs and floor seams | needed | kerbs, the office's steps and the street's slope taken without catching |
| A06.12 | 2 | Reliable movement up and down ordinary stairs | needed | kerbs, the office's steps and the street's slope taken without catching |
| A06.13 | 2 | Sensible behaviour on slopes | needed | kerbs, the office's steps and the street's slope taken without catching |
| A06.14 | 2 | Clear limits on slopes too steep to climb | later | steep slopes, crouching, moving platforms and burdens: none in the Hook |
| A06.15 | 2 | No snagging on tiny decorative geometry | needed | no snagging on clutter, sliding along walls, never wedged |
| A06.16 | 2 | Predictable sliding along a wall instead of becoming stuck | needed | no snagging on clutter, sliding along walls, never wedged |
| A06.17 | 2 | A crouched collision shape that actually fits under lower obstacles | later | steep slopes, crouching, moving platforms and burdens: none in the Hook |
| A06.18 | 2 | Prevention of standing through a ceiling | later | steep slopes, crouching, moving platforms and burdens: none in the Hook |
| A06.19 | 2 | Movement that follows moving platforms | later | steep slopes, crouching, moving platforms and burdens: none in the Hook |
| A06.20 | 2 | Appropriate restrictions while carrying, aiming or injured | later | steep slopes, crouching, moving platforms and burdens: none in the Hook |
| A06.21 | 2 | Recovery from being wedged between objects | needed | no snagging on clutter, sliding along walls, never wedged |
| A08.01 | 2 | A complete character model from ordinary viewing angles | needed | complete, right-sized people with believable hands, eyes and mouths, shadows, and faces that hold from near to far |
| A08.02 | 2 | Consistent scale between characters and their surroundings | needed | complete, right-sized people with believable hands, eyes and mouths, shadows, and faces that hold from near to far |
| A08.03 | 2 | Clothing that fits the body rather than visibly floating | needed | clothes that fit, show no gaps and move with the body (sewn by the clothing session, fitted by the builder) |
| A08.04 | 2 | Believable hands and fingers | needed | complete, right-sized people with believable hands, eyes and mouths, shadows, and faces that hold from near to far |
| A08.05 | 2 | Believable eyes, eyelids and gaze direction | needed | complete, right-sized people with believable hands, eyes and mouths, shadows, and faces that hold from near to far |
| A08.06 | 2 | A mouth interior that survives ordinary close-ups | needed | complete, right-sized people with believable hands, eyes and mouths, shadows, and faces that hold from near to far |
| A08.09 | 2 | Equipped clothing and gear reflected on the visible character | later | held things, sitting, hands on rails, lean and foot placement on stairs: stage 2's finer animation, after the people walk |
| A08.10 | 2 | Held items attached to the correct hand and orientation | later | held things, sitting, hands on rails, lean and foot placement on stairs: stage 2's finer animation, after the people walk |
| A08.11 | 2 | Holstered gear occupying a plausible place on the body | later | held things, sitting, hands on rails, lean and foot placement on stairs: stage 2's finer animation, after the people walk |
| A08.12 | 2 | No major body or clothing gaps during ordinary poses | needed | clothes that fit, show no gaps and move with the body (sewn by the clothing session, fitted by the builder) |
| A08.13 | 2 | A character shadow that matches the visible body and equipment | needed | complete, right-sized people with believable hands, eyes and mouths, shadows, and faces that hold from near to far |
| A08.14 | 2 | Consistent appearance across gameplay, menus and cutscenes | needed | complete, right-sized people with believable hands, eyes and mouths, shadows, and faces that hold from near to far |
| A08.16 | 2 | Visible wetness, dirt or injury where the presentation promises it | later | held things, sitting, hands on rails, lean and foot placement on stairs: stage 2's finer animation, after the people walk |
| A09.03 | 2 | Feet that remain planted instead of sliding during stops | needed | breathing, varied idles, planted feet, matched strides, clean blends, heads a little free of the torso, never a default pose |
| A09.04 | 2 | Foot placement that follows stairs and uneven ground | later | held things, sitting, hands on rails, lean and foot placement on stairs: stage 2's finer animation, after the people walk |
| A09.05 | 2 | Knees and hips that accommodate different foot heights | later | held things, sitting, hands on rails, lean and foot placement on stairs: stage 2's finer animation, after the people walk |
| A09.06 | 2 | Stride length that matches travel speed | needed | breathing, varied idles, planted feet, matched strides, clean blends, heads a little free of the torso, never a default pose |
| A09.07 | 2 | Body lean during acceleration and turning | later | held things, sitting, hands on rails, lean and foot placement on stairs: stage 2's finer animation, after the people walk |
| A09.08 | 2 | Smooth transitions between idle, walking and running | needed | breathing, varied idles, planted feet, matched strides, clean blends, heads a little free of the torso, never a default pose |
| A09.09 | 2 | Upper-body actions that coexist with leg movement | later | held things, sitting, hands on rails, lean and foot placement on stairs: stage 2's finer animation, after the people walk |
| A09.10 | 2 | Head movement that is partly independent of the torso | needed | breathing, varied idles, planted feet, matched strides, clean blends, heads a little free of the torso, never a default pose |
| A09.11 | 2 | Hands that meet handles, rails and other contact points | later | held things, sitting, hands on rails, lean and foot placement on stairs: stage 2's finer animation, after the people walk |
| A09.12 | 2 | Finger poses that fit held objects | later | held things, sitting, hands on rails, lean and foot placement on stairs: stage 2's finer animation, after the people walk |
| A09.13 | 2 | Two-handed objects held by both hands | later | held things, sitting, hands on rails, lean and foot placement on stairs: stage 2's finer animation, after the people walk |
| A09.14 | 2 | Seated bodies that actually meet the chair | later | held things, sitting, hands on rails, lean and foot placement on stairs: stage 2's finer animation, after the people walk |
| A09.15 | 2 | Sit-down and stand-up transitions | later | held things, sitting, hands on rails, lean and foot placement on stairs: stage 2's finer animation, after the people walk |
| A09.16 | 2 | Animation appropriate to the character's current weapon or burden | later | held things, sitting, hands on rails, lean and foot placement on stairs: stage 2's finer animation, after the people walk |
| A09.18 | 2 | Interruptions that leave the body in a valid pose | needed | breathing, varied idles, planted feet, matched strides, clean blends, heads a little free of the torso, never a default pose |
| A09.21 | 2 | Bodies that rest on the ground rather than hover | needed | breathing, varied idles, planted feet, matched strides, clean blends, heads a little free of the torso, never a default pose |
| A09.22 | 2 | Hair, clothing and attachments that follow body movement | needed | clothes that fit, show no gaps and move with the body (sewn by the clothing session, fitted by the builder) |
| A09.23 | 2 | No sudden default pose while an animation loads | needed | breathing, varied idles, planted feet, matched strides, clean blends, heads a little free of the torso, never a default pose |
| A10.01 | 2 | NPCs turning their eyes toward someone addressing them | needed | eyes and torso that follow within limits, eye contact that breaks, blinks, back to what they were doing after |
| A10.02 | 2 | NPCs turning their head toward an approaching player when appropriate | done | done by 24 Sep: the engine's Look At on the head, within 5 m and in front; 6 of 6 heads found, 3 turned in the walk, 23 Sep: [frame](production/art/compare/heads-2026-09-23/eli |
| A10.03 | 2 | The torso turning when the player moves beyond a comfortable head angle | needed | eyes and torso that follow within limits, eye contact that breaks, blinks, back to what they were doing after |
| A10.04 | 2 | Limits that prevent impossible head and neck rotation | needed | eyes and torso that follow within limits, eye contact that breaks, blinks, back to what they were doing after |
| A10.05 | 2 | Gaze directed at the player's face rather than their feet or empty space | done | done by 24 Sep: aimed at the camera's eye, not the feet, 23 Sep: [frame](production/art/compare/heads-2026-09-23/elizabeth-before-after.png) |
| A10.06 | 2 | Eye contact that occasionally breaks | needed | eyes and torso that follow within limits, eye contact that breaks, blinks, back to what they were doing after |
| A10.07 | 2 | Blinking rather than a permanent stare | needed | eyes and torso that follow within limits, eye contact that breaks, blinks, back to what they were doing after |
| A10.08 | 2 | Facial expression that broadly fits the line being spoken | needed | a face that broadly fits the line it speaks |
| A10.09 | 2 | Listener reactions while another person speaks | later | listeners' reactions, gestures, hostility in the face: finer performance, after the voices |
| A10.10 | 2 | Gestures that fit the conversation rather than random arm waving | later | listeners' reactions, gestures, hostility in the face: finer performance, after the voices |
| A10.11 | 2 | People orienting toward a shared point of interest | later | listeners' reactions, gestures, hostility in the face: finer performance, after the voices |
| A10.12 | 2 | Expression and posture changes when a conversation becomes hostile | later | listeners' reactions, gestures, hostility in the face: finer performance, after the voices |
| A10.13 | 2 | Reactions to excessive proximity | later | listeners' reactions, gestures, hostility in the face: finer performance, after the voices |
| A10.14 | 2 | A return to ordinary activity after the player leaves | needed | eyes and torso that follow within limits, eye contact that breaks, blinks, back to what they were doing after |
| A11.08 | 2 | Feedback when an interaction succeeds | needed | a prompt on the thing he can use, in reach, not through walls, talk before open, saying what will happen and why not |
| A11.12 | 2 | Doors whose visible movement agrees with their blocking state | needed | doors that move as they block, never trap him, and a locked office door that says so |
| A12.01 | 2 | Solid ground everywhere that appears walkable | needed | solid ground and walls where they look solid, doors that admit him, bodies steady on uneven ground |
| A12.02 | 2 | Solid walls where walls are visibly present | done | done by 24 Sep: the walk into the parade wall stops (collisionBlockedStatus=STOPPED, east_parade_bay0) every run: [walk verdict](production/d1-probe/ue-walk-verdict.txt), [fram |
| A12.03 | 2 | Collision shapes that broadly match visible objects | needed | solid ground and walls where they look solid, doors that admit him, bodies steady on uneven ground |
| A12.04 | 2 | Doorways that admit a character who visibly fits | needed | solid ground and walls where they look solid, doors that admit him, bodies steady on uneven ground |
| A12.05 | 2 | Small loose objects that do not act like immovable roadblocks | later | loose physics objects: the Hook's clutter is fixed |
| A12.06 | 2 | Heavy objects that do not behave like weightless toys | later | loose physics objects: the Hook's clutter is fixed |
| A12.07 | 2 | Dropped objects falling under consistent gravity | later | loose physics objects: the Hook's clutter is fixed |
| A12.08 | 2 | Objects settling instead of vibrating indefinitely | later | loose physics objects: the Hook's clutter is fixed |
| A12.09 | 2 | No explosive physics response from mild contact | later | loose physics objects: the Hook's clutter is fixed |
| A12.10 | 2 | Fast objects that do not pass through obvious barriers | later | loose physics objects: the Hook's clutter is fixed |
| A12.11 | 2 | Characters not pushing through one another without explanation | needed | people and Tom never pass through one another, walkers included; a way past someone in a doorway |
| A12.12 | 2 | A workable solution to being blocked by a friendly character | needed | people and Tom never pass through one another, walkers included; a way past someone in a doorway |
| A12.13 | 2 | Moving machinery carrying or blocking objects consistently | later | loose physics objects: the Hook's clutter is fixed |
| A12.14 | 2 | Appropriate friction on visibly different surfaces where it matters | later | loose physics objects: the Hook's clutter is fixed |
| A12.15 | 2 | Physical reactions accompanied by matching sound | needed | the smashed window's remnants and sound agree (FINDINGS: its inside card shows through) |
| A12.16 | 2 | Broken objects leaving plausible remnants if destruction exists | needed | the smashed window's remnants and sound agree (FINDINGS: its inside card shows through) |
| A12.17 | 2 | Destruction that changes collision as well as appearance | needed | the smashed window's remnants and sound agree (FINDINGS: its inside card shows through) |
| A12.18 | 2 | Stable interaction between bodies, props and uneven ground | needed | solid ground and walls where they look solid, doors that admit him, bodies steady on uneven ground |
| A13.01 | 2 | People walking somewhere or doing something | needed | people who walk the town's routines (CastDay ported, not yet moving them), avoid each other and Tom, react to a bump, use doors, and never pop in or out in view |
| A13.02 | 2 | Variation in pace, posture and activity | needed | people who walk the town's routines (CastDay ported, not yet moving them), avoid each other and Tom, react to a bump, use doors, and never pop in or out in view |
| A13.03 | 2 | People avoiding one another while moving | needed | people who walk the town's routines (CastDay ported, not yet moving them), avoid each other and Tom, react to a bump, use doors, and never pop in or out in view |
| A13.04 | 2 | People avoiding the player when there is room | needed | people who walk the town's routines (CastDay ported, not yet moving them), avoid each other and Tom, react to a bump, use doors, and never pop in or out in view |
| A13.05 | 2 | A response to bumping into someone | needed | people who walk the town's routines (CastDay ported, not yet moving them), avoid each other and Tom, react to a bump, use doors, and never pop in or out in view |
| A13.06 | 2 | A response to repeatedly blocking someone's route | needed | people who walk the town's routines (CastDay ported, not yet moving them), avoid each other and Tom, react to a bump, use doors, and never pop in or out in view |
| A13.07 | 2 | Navigation through doorways without permanent jams | needed | people who walk the town's routines (CastDay ported, not yet moving them), avoid each other and Tom, react to a bump, use doors, and never pop in or out in view |
| A13.08 | 2 | Use of stairs rather than walking through their geometry | later | people at stairs, seats, work and in pairs: after they walk their routines |
| A13.09 | 2 | Plausible transitions into sitting, working or leaning | later | people at stairs, seats, work and in pairs: after they walk their routines |
| A13.10 | 2 | Hands and props matching the activity being performed | later | people at stairs, seats, work and in pairs: after they walk their routines |
| A13.24 | 2 | Some continuity when briefly looking away and back | needed | people who walk the town's routines (CastDay ported, not yet moving them), avoid each other and Tom, react to a bump, use doors, and never pop in or out in view |
| A13.25 | 2 | No obvious appearance or disappearance directly in view | needed | people who walk the town's routines (CastDay ported, not yet moving them), avoid each other and Tom, react to a bump, use doors, and never pop in or out in view |
| A13.26 | 2 | A reasonable solution when an NPC's intended route becomes blocked | needed | people who walk the town's routines (CastDay ported, not yet moving them), avoid each other and Tom, react to a bump, use doors, and never pop in or out in view |
| A20.07 | 2 | Readable stamina or similar exhaustion feedback | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A23.08 | 2 | Visible lamps whose surroundings respond to their light | done | sodium lamps light pools under themselves at night: production/approvals/2026-09-30/street-night-camA.webp |
| A24.01 | 2 | Vegetation moving appropriately in wind | later | weather that changes, wind in fabric, the basin's water, fire and smoke: with the town |
| A24.02 | 2 | Hanging fabric and similar objects responding to the environment | later | weather that changes, wind in fabric, the basin's water, fire and smoke: with the town |
| A24.03 | 2 | Rain that does not visibly fall through ordinary roofs | needed | if rain falls, not through roofs; wind and rain sound that follow the weather |
| A24.04 | 2 | A change in rain sound when moving under cover | later | weather that changes, wind in fabric, the basin's water, fire and smoke: with the town |
| A24.06 | 2 | Plausible transitions into and out of weather | later | weather that changes, wind in fabric, the basin's water, fire and smoke: with the town |
| A24.07 | 2 | Character or NPC responses to conspicuous weather where the presentation warrants them | later | weather that changes, wind in fabric, the basin's water, fire and smoke: with the town |
| A24.09 | 2 | Ripples or splashes when entering water | later | weather that changes, wind in fabric, the basin's water, fire and smoke: with the town |
| A24.10 | 2 | Wakes from moving boats or swimmers | later | weather that changes, wind in fabric, the basin's water, fire and smoke: with the town |
| A24.11 | 2 | Fire giving appropriate light, movement and sound | later | weather that changes, wind in fabric, the basin's water, fire and smoke: with the town |
| A24.12 | 2 | Smoke and dust appearing to originate from their causes | later | weather that changes, wind in fabric, the basin's water, fire and smoke: with the town |
| A24.13 | 2 | Surface-specific debris from impacts | done | the smash leaves a fan of glass on the pavement (29 Sep): production/research/broken-window-look |
| A24.15 | 2 | Footprints or tracks where a visibly impressionable surface invites them | later | weather that changes, wind in fabric, the basin's water, fire and smoke: with the town |
| A24.16 | 2 | Effects ending when their source ends | later | weather that changes, wind in fabric, the basin's water, fire and smoke: with the town |
| A24.17 | 2 | Effects staying attached to moving sources | later | weather that changes, wind in fabric, the basin's water, fire and smoke: with the town |
| A24.18 | 2 | Weather and time changes that do not visibly reset at ordinary area boundaries | later | weather that changes, wind in fabric, the basin's water, fire and smoke: with the town |
| A25.01 | 2 | Background activity beyond the player's immediate objective | needed | the street busy with different doings, the right numbers by hour, continuous when he turns away |
| A25.02 | 2 | Ambient sound appropriate to the location | needed | ambient sound for the street and the office |
| A25.03 | 2 | Population density that fits the place and time | needed | the street busy with different doings, the right numbers by hour, continuous when he turns away |
| A25.04 | 2 | People occupying different activities rather than all wandering | needed | the street busy with different doings, the right numbers by hour, continuous when he turns away |
| A25.05 | 2 | A plausible distinction between open and closed businesses, if operating hours exist | later | shop hours shown in doors and lights, casualties and loot, animals |
| A25.06 | 2 | Continuity when leaving a small area and immediately returning | needed | the street busy with different doings, the right numbers by hour, continuous when he turns away |
| A25.07 | 2 | Consistent handling of dropped objects and casualties | later | shop hours shown in doors and lights, casualties and loot, animals |
| A25.08 | 2 | Clear rules for replenishing loot or respawning enemies | later | shop hours shown in doors and lights, casualties and loot, animals |
| A25.09 | 2 | Events that do not visibly restart every time the player crosses a nearby boundary | needed | the street busy with different doings, the right numbers by hour, continuous when he turns away |
| A25.10 | 2 | Day and night changes reflected in lighting and relevant activity, if time advances | needed | a clock that runs (two game minutes a second, the town's ruling), waits that stop for the town, the light following the hour (town list ci; today the game only jumps between scenes) |
| A25.12 | 2 | Safe handling of time skips with active missions or followers | needed | a clock that runs (two game minutes a second, the town's ruling), waits that stop for the town, the light following the hour (town list ci; today the game only jumps between scenes) |
| A25.13 | 2 | Ambient events that allow interruption and recovery | needed | the street busy with different doings, the right numbers by hour, continuous when he turns away |
| A25.14 | 2 | Animals behaving like animals rather than stationary ornaments, where present | later | shop hours shown in doors and lights, casualties and loot, animals |
| A25.15 | 2 | Birds or small wildlife reacting to close movement or noise | later | shop hours shown in doors and lights, casualties and loot, animals |
| A25.16 | 2 | No immediate repopulation directly in front of the player after a disturbance | needed | the street busy with different doings, the right numbers by hour, continuous when he turns away |
| A26.02 | 2 | Entry animation that fits the door and seat | later | G4: the firm's cars driven by others, after passing traffic |
| A26.03 | 2 | Sensible entry when one side is obstructed | later | G4: the firm's cars driven by others, after passing traffic |
| A26.05 | 2 | Acceleration and braking appropriate to the vehicle | needed | a few cars passing on the carriageway, wheels turning, lamps lit at night, engine sound, keeping lane, stopping for people (his G4: a street with no traffic feels dead). Bigger than it looks |
| A26.08 | 2 | Wheels rotating at a plausible rate | needed | a few cars passing on the carriageway, wheels turning, lamps lit at night, engine sound, keeping lane, stopping for people (his G4: a street with no traffic feels dead). Bigger than it looks |
| A26.09 | 2 | Front wheels turning with steering where appropriate | needed | a few cars passing on the carriageway, wheels turning, lamps lit at night, engine sound, keeping lane, stopping for people (his G4: a street with no traffic feels dead). Bigger than it looks |
| A26.10 | 2 | Suspension responding to road irregularities | later | G4: the firm's cars driven by others, after passing traffic |
| A26.11 | 2 | Tyre contact that broadly matches the ground | later | G4: the firm's cars driven by others, after passing traffic |
| A26.12 | 2 | Engine sound responding to speed and load | needed | a few cars passing on the carriageway, wheels turning, lamps lit at night, engine sound, keeping lane, stopping for people (his G4: a street with no traffic feels dead). Bigger than it looks |
| A26.13 | 2 | Skid and collision sounds responding to the actual event | later | G4: the firm's cars driven by others, after passing traffic |
| A26.14 | 2 | Brake lights, headlights and reversing lights where the vehicle has them | needed | a few cars passing on the carriageway, wheels turning, lamps lit at night, engine sound, keeping lane, stopping for people (his G4: a street with no traffic feels dead). Bigger than it looks |
| A26.20 | 2 | Traffic following plausible lanes and junction rules | needed | a few cars passing on the carriageway, wheels turning, lamps lit at night, engine sound, keeping lane, stopping for people (his G4: a street with no traffic feels dead). Bigger than it looks |
| A26.21 | 2 | Traffic responding to obstructions and collisions | needed | a few cars passing on the carriageway, wheels turning, lamps lit at night, engine sound, keeping lane, stopping for people (his G4: a street with no traffic feels dead). Bigger than it looks |
| A26.22 | 2 | Pedestrians responding to approaching vehicles | needed | a few cars passing on the carriageway, wheels turning, lamps lit at night, engine sound, keeping lane, stopping for people (his G4: a street with no traffic feels dead). Bigger than it looks |
| A26.23 | 2 | Passengers remaining correctly seated during movement | later | G4: the firm's cars driven by others, after passing traffic |
| A26.24 | 2 | A vehicle remaining where it was left under the game's persistence rules | later | G4: the firm's cars driven by others, after passing traffic |
| A28.01 | 2 | Sounds coming from the direction of their source | done | done by 24 Sep: the traffic bed heard from the north bend with the engine's spatialisation, 23 Sep: [recording](production/art/compare/sound-2026-09-23/walk-audio-0c836a44.wav) |
| A28.02 | 2 | Sound direction changing correctly as the player turns | done | done by 24 Sep: the walk turns its view at 7 s and the bed swings from -0.06 to +0.40 in balance, 23 Sep: [recording](production/art/compare/sound-2026-09-23/walk-audio-0c836a4 |
| A28.03 | 2 | Moving sources carrying their sounds with them | needed | moving sources carry sound, distance quietens, the office muffles the street and sounds like a room, no hard jumps |
| A28.04 | 2 | Distant sources sounding quieter than nearby sources | needed | moving sources carry sound, distance quietens, the office muffles the street and sounds like a room, no hard jumps |
| A28.05 | 2 | Distant sources losing appropriate detail | later | finer acoustics, with more interiors |
| A28.06 | 2 | Walls and closed doors muffling relevant sounds | needed | moving sources carry sound, distance quietens, the office muffles the street and sounds like a room, no hard jumps |
| A28.07 | 2 | Openings providing a plausible route for sound | needed | moving sources carry sound, distance quietens, the office muffles the street and sounds like a room, no hard jumps |
| A28.08 | 2 | Room acoustics differing from open air | needed | moving sources carry sound, distance quietens, the office muffles the street and sounds like a room, no hard jumps |
| A28.09 | 2 | Larger and smaller rooms sounding different where conspicuous | later | finer acoustics, with more interiors |
| A28.10 | 2 | Smooth acoustic transitions at room boundaries | needed | moving sources carry sound, distance quietens, the office muffles the street and sounds like a room, no hard jumps |
| A28.11 | 2 | Large sources sounding spatially broad rather than like tiny points | later | finer acoustics, with more interiors |
| A28.12 | 2 | Above and below having useful audible distinction where supported | later | finer acoustics, with more interiors |
| A28.13 | 2 | A sensible listening position when the camera moves away from the character | needed | moving sources carry sound, distance quietens, the office muffles the street and sounds like a room, no hard jumps |
| A28.14 | 2 | No distant conversation playing at intimate, full-volume closeness | needed | moving sources carry sound, distance quietens, the office muffles the street and sounds like a room, no hard jumps |
| A28.15 | 2 | No obvious snapping between left and right as a source passes nearby | needed | moving sources carry sound, distance quietens, the office muffles the street and sounds like a room, no hard jumps |
| A29.01 | 2 | Footsteps synchronised with foot contact | needed | footsteps in time, by surface and pace, stopping when he stops; doors and the smash heard; varied, once, on time |
| A29.02 | 2 | Different footstep sounds on different surfaces | needed | footsteps in time, by surface and pace, stopping when he stops; doors and the smash heard; varied, once, on time |
| A29.03 | 2 | Footstep cadence changing with movement speed | needed | footsteps in time, by surface and pace, stopping when he stops; doors and the smash heard; varied, once, on time |
| A29.04 | 2 | Appropriate landing sound | later | landing, clothing rustle, exertion, pickups, weapons, machines, water |
| A29.05 | 2 | Clothing and equipment movement where audible | later | landing, clothing rustle, exertion, pickups, weapons, machines, water |
| A29.06 | 2 | Breathing or exertion appropriate to strenuous activity | later | landing, clothing rustle, exertion, pickups, weapons, machines, water |
| A29.07 | 2 | Doors sounding when they move and latch | needed | footsteps in time, by surface and pace, stopping when he stops; doors and the smash heard; varied, once, on time |
| A29.08 | 2 | Pickups and item handling providing subtle confirmation | later | landing, clothing rustle, exertion, pickups, weapons, machines, water |
| A29.09 | 2 | Collision sounds appropriate to the materials involved | needed | footsteps in time, by surface and pace, stopping when he stops; doors and the smash heard; varied, once, on time |
| A29.10 | 2 | Breakage sounds matching the object | needed | footsteps in time, by surface and pace, stopping when he stops; doors and the smash heard; varied, once, on time |
| A29.11 | 2 | Weapon handling, firing and reloading sounds aligned with actions | later | landing, clothing rustle, exertion, pickups, weapons, machines, water |
| A29.12 | 2 | Damage and pain sounds fitting the affected character | later | landing, clothing rustle, exertion, pickups, weapons, machines, water |
| A29.13 | 2 | Machines sounding active only while operating | later | landing, clothing rustle, exertion, pickups, weapons, machines, water |
| A29.14 | 2 | Splash sounds matching water contact | later | landing, clothing rustle, exertion, pickups, weapons, machines, water |
| A29.15 | 2 | Variation that prevents repeated actions sounding mechanically identical | needed | footsteps in time, by surface and pace, stopping when he stops; doors and the smash heard; varied, once, on time |
| A29.16 | 2 | No double-triggered sound for a single event | needed | footsteps in time, by surface and pace, stopping when he stops; doors and the smash heard; varied, once, on time |
| A29.17 | 2 | No continued footsteps after the character stops | needed | footsteps in time, by surface and pace, stopping when he stops; doors and the smash heard; varied, once, on time |
| A29.18 | 2 | Sound events occurring when the action happens rather than noticeably late | needed | footsteps in time, by surface and pace, stopping when he stops; doors and the smash heard; varied, once, on time |
| A30.01 | 2 | Important speech intelligible over ambience and action | needed | speech clear over the street and level across speakers, ambience ducking under it, no clipping or clicks, pausing with the game |
| A30.02 | 2 | Consistent dialogue loudness across speakers | needed | speech clear over the street and level across speakers, ambience ducking under it, no clipping or clicks, pausing with the game |
| A30.04 | 2 | Speech fitting the speaker's emotional situation | later | acted delivery (his blind pick kept the game's own engine), music, radio |
| A30.05 | 2 | No clipping or harsh overload during loud events | needed | speech clear over the street and level across speakers, ambience ducking under it, no clipping or clicks, pausing with the game |
| A30.06 | 2 | No audible clicks at the start or end of loops | needed | speech clear over the street and level across speakers, ambience ducking under it, no clipping or clicks, pausing with the game |
| A30.10 | 2 | Appropriate silence and contrast rather than constant maximum intensity | needed | speech clear over the street and level across speakers, ambience ducking under it, no clipping or clicks, pausing with the game |
| A30.12 | 2 | Important sounds remaining audible in a crowded mix | needed | speech clear over the street and level across speakers, ambience ducking under it, no clipping or clicks, pausing with the game |
| A30.13 | 2 | No dialogue continuing from a dead or departed speaker without explanation | needed | speech clear over the street and level across speakers, ambience ducking under it, no clipping or clicks, pausing with the game |
| A30.14 | 2 | Audio pausing, resuming and loading consistently with the game state | needed | speech clear over the street and level across speakers, ambience ducking under it, no clipping or clicks, pausing with the game |
| A30.15 | 2 | Consistent presentation across headphones and supported speaker layouts | later | acted delivery (his blind pick kept the game's own engine), music, radio |
| A31.02 | 2 | Acknowledgement when the player initiates speech | needed | start and leave a talk plainly, an acknowledgement, facing at a talking distance, lips roughly in time, the voice from the speaker, subtitles that match |
| A31.03 | 2 | Conversational distance and facing that look plausible | needed | start and leave a talk plainly, an acknowledgement, facing at a talking distance, lips roughly in time, the voice from the speaker, subtitles that match |
| A31.04 | 2 | Mouth movement synchronised approximately with speech | needed | start and leave a talk plainly, an acknowledgement, facing at a talking distance, lips roughly in time, the voice from the speaker, subtitles that match |
| A31.08 | 2 | Choice selection that does not accidentally confirm during menu navigation | later | no choice menus while talk is typed |
| A31.09 | 2 | A predictable response to walking away | needed | walking away mid-reply (town list 9 for the talk's side) |
| A31.10 | 2 | A predictable response to combat interrupting speech | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A31.15 | 2 | Ambient and important dialogue prevented from talking over one another excessively | needed | start and leave a talk plainly, an acknowledgement, facing at a talking distance, lips roughly in time, the voice from the speaker, subtitles that match |
| A31.16 | 2 | Subtitles matching the actual spoken line | needed | start and leave a talk plainly, an acknowledgement, facing at a talking distance, lips roughly in time, the voice from the speaker, subtitles that match |
| A31.17 | 2 | Appropriate pauses and turn-taking | needed | start and leave a talk plainly, an acknowledgement, facing at a talking distance, lips roughly in time, the voice from the speaker, subtitles that match |
| A31.18 | 2 | No conspicuous silence while a character appears to be waiting for a missing line | needed | thinking sounds for Ron and Darren (his yes); Sheila has none |
| A32.02 | 2 | Camera placement that shows the intended action | later | G6: the handful of short scenes (the arrival with the suitcase) |
| A32.05 | 2 | Facial and body performance consistent with the dialogue | later | G6: the handful of short scenes (the arrival with the suitcase) |
| A44.05 | 2 | Captions for essential non-speech sounds | needed | subtitles and captions from the start, naming the speaker, long enough, sizeable, with the smash shown as well as heard |
| A48.01 | 2 | A stable frame rate appropriate to the selected mode | needed | 60 fps at his screen with the voice running (70.7 today), even frames, no first-use hitch, textures in time, thirty minutes without decline, settings and devices changed safely, alt-tab |
| A48.02 | 2 | Even frame timing rather than frequent small freezes | needed | 60 fps at his screen with the voice running (70.7 today), even frames, no first-use hitch, textures in time, thirty minutes without decline, settings and devices changed safely, alt-tab |
| A48.03 | 2 | No major hitch at the first use of an ordinary effect or weapon | needed | 60 fps at his screen with the voice running (70.7 today), even frames, no first-use hitch, textures in time, thirty minutes without decline, settings and devices changed safely, alt-tab |
| A48.06 | 2 | Textures resolving before their absence becomes conspicuous | needed | 60 fps at his screen with the voice running (70.7 today), even frames, no first-use hitch, textures in time, thirty minutes without decline, settings and devices changed safely, alt-tab |
| A48.08 | 2 | Stable performance in the expected crowd and combat density | needed | 60 fps at his screen with the voice running (70.7 today), even frames, no first-use hitch, textures in time, thirty minutes without decline, settings and devices changed safely, alt-tab |
| A48.09 | 2 | Menus that remain responsive when the world is busy | needed | 60 fps at his screen with the voice running (70.7 today), even frames, no first-use hitch, textures in time, thirty minutes without decline, settings and devices changed safely, alt-tab |
| A48.11 | 2 | Long-session stability without steadily worsening performance | needed | 60 fps at his screen with the voice running (70.7 today), even frames, no first-use hitch, textures in time, thirty minutes without decline, settings and devices changed safely, alt-tab |
| A48.12 | 2 | Stable behaviour when changing graphics settings | needed | 60 fps at his screen with the voice running (70.7 today), even frames, no first-use hitch, textures in time, thirty minutes without decline, settings and devices changed safely, alt-tab |
| A48.13 | 2 | Stable behaviour when changing audio or input devices | needed | 60 fps at his screen with the voice running (70.7 today), even frames, no first-use hitch, textures in time, thirty minutes without decline, settings and devices changed safely, alt-tab |
| A48.14 | 2 | Correct recovery after task switching | needed | 60 fps at his screen with the voice running (70.7 today), even frames, no first-use hitch, textures in time, thirty minutes without decline, settings and devices changed safely, alt-tab |
| A48.15 | 2 | No simulation speed changes caused by frame-rate changes | done | the simulation runs on a fixed clock (ue-probe FixedClock.h), from the town's sweep |
| A48.19 | 2 | No routine need to restart the game to restore basic controls or interactions | needed | 60 fps at his screen with the voice running (70.7 today), even frames, no first-use hitch, textures in time, thirty minutes without decline, settings and devices changed safely, alt-tab |
| A48.20 | 2 | Updates that preserve existing progress and settings where promised | needed | repeated save and load, and a new build over an old save, with nothing lost |
| H9 | 2 | Animation budget at crowd scale | later | held things, sitting, hands on rails, lean and foot placement on stairs: stage 2's finer animation, after the people walk |
| N7 | 2 | Live spoken conversation with memory | needed | speech soon enough to feel like talk: the voice half of the delay (list item 6) |
| V1 | 2 | Voice casting and direction | needed | a voice for each person who talks: Sheila has none that holds her English accent |
| V2 | 2 | Motion capture and performance | later | held things, sitting, hands on rails, lean and foot placement on stairs: stage 2's finer animation, after the people walk |
| VX01 | 2 | Voices that carry feeling, not flat read speech: the VCTK recordings are calm read speech and cloning copies that delivery. An experiment, cheapest first: the emotion control set per line from what the character is feeling, which the game knows; the paralinguistic tags; livelier reference clips; and only if those fall short, a more expressive source of voices within the licence rules. Blind listening pages for Jafar at each step | later | acted delivery (his blind pick kept the game's own engine), music, radio |
| B01 | 2 | Music, ambience and effects lowering while dialogue plays | needed | speech clear over the street and level across speakers, ambience ducking under it, no clipping or clicks, pausing with the game |
| B02 | 2 | Wind and rain sound that follows the current weather | needed | if rain falls, not through roofs; wind and rain sound that follow the weather |
| B03 | 2 | Camera follow smoothing rather than a rigidly locked view | needed | free look, a good distance and field of view, Tom readable, smoothed but not detached |
| B04 | 2 | People opening, using and closing doors on their routes | later | people at stairs, seats, work and in pairs: after they walk their routines |
| B05 | 2 | People queueing, waiting their turn and giving way to one another | later | people at stairs, seats, work and in pairs: after they walk their routines |
| B06 | 2 | Puddles that ripple in rain and splash underfoot | later | weather that changes, wind in fabric, the basin's water, fire and smoke: with the town |
| A05.12 | 3 | A usable view while climbing or hanging | later | G1: climbing low walls and fences, the basin's ladder: escapes, with the law (stage 3) |
| A07.01 | 3 | A responsive jump with readable height and distance | out | G1: unsure, my call: no jump; kerbs, low walls and fences are stepped and climbed |
| A07.02 | 3 | Predictable control while airborne | later | G1: climbing low walls and fences, the basin's ladder: escapes, with the law (stage 3) |
| A07.03 | 3 | Forgiveness around ledge departure and landing inputs | later | G1: climbing low walls and fences, the basin's ladder: escapes, with the law (stage 3) |
| A07.04 | 3 | A landing animation appropriate to the fall | later | G1: climbing low walls and fences, the basin's ladder: escapes, with the law (stage 3) |
| A07.05 | 3 | Fall damage that follows understandable rules | later | G1: climbing low walls and fences, the basin's ladder: escapes, with the law (stage 3) |
| A07.06 | 3 | A clear distinction between a safe drop and a dangerous fall | later | G1: climbing low walls and fences, the basin's ladder: escapes, with the law (stage 3) |
| A07.07 | 3 | Consistent identification of vaultable obstacles | later | G1: climbing low walls and fences, the basin's ladder: escapes, with the law (stage 3) |
| A07.08 | 3 | Vaulting that fits the obstacle's height and thickness | later | G1: climbing low walls and fences, the basin's ladder: escapes, with the law (stage 3) |
| A07.09 | 3 | Mantling that puts hands and feet on the actual surface | later | G1: climbing low walls and fences, the basin's ladder: escapes, with the law (stage 3) |
| A07.10 | 3 | Prevention of climbing into blocked space | later | G1: climbing low walls and fences, the basin's ladder: escapes, with the law (stage 3) |
| A07.11 | 3 | A way to cancel or drop from a climb | later | G1: climbing low walls and fences, the basin's ladder: escapes, with the law (stage 3) |
| A07.12 | 3 | Ladder entry from plausible positions | later | G1: climbing low walls and fences, the basin's ladder: escapes, with the law (stage 3) |
| A07.13 | 3 | Ladder exit without falling or becoming stuck | later | G1: climbing low walls and fences, the basin's ladder: escapes, with the law (stage 3) |
| A07.14 | 3 | Consistent behaviour at climbable and non-climbable lookalikes | later | G1: climbing low walls and fences, the basin's ladder: escapes, with the law (stage 3) |
| A07.15 | 3 | Clear entry into swimming rather than walking underwater | later | G1: climbing low walls and fences, the basin's ladder: escapes, with the law (stage 3) |
| A07.16 | 3 | A usable transition between swimming and the shore | later | G1: climbing low walls and fences, the basin's ladder: escapes, with the law (stage 3) |
| A07.17 | 3 | Swim movement and animation that agree | later | G1: climbing low walls and fences, the basin's ladder: escapes, with the law (stage 3) |
| A07.18 | 3 | Readable breath or drowning rules if diving is possible | out | G1: Swimming to a ladder only; no diving |
| A07.19 | 3 | Water camera and sound changes when submerged | later | G1: climbing low walls and fences, the basin's ladder: escapes, with the law (stage 3) |
| A11.02 | 3 | A stable current interaction target | needed | a prompt on the thing he can use, in reach, not through walls, talk before open, saying what will happen and why not |
| A11.04 | 3 | Interaction range that matches apparent reach | needed | a prompt on the thing he can use, in reach, not through walls, talk before open, saying what will happen and why not |
| A11.05 | 3 | No interaction through an intervening solid wall | needed | a prompt on the thing he can use, in reach, not through walls, talk before open, saying what will happen and why not |
| A11.06 | 3 | Appropriate priority when talk, loot and open share a button | needed | a prompt on the thing he can use, in reach, not through walls, talk before open, saying what will happen and why not |
| A11.07 | 3 | A clear description of the action before committing | needed | a prompt on the thing he can use, in reach, not through walls, talk before open, saying what will happen and why not |
| A11.09 | 3 | Feedback explaining why an interaction is unavailable | needed | a prompt on the thing he can use, in reach, not through walls, talk before open, saying what will happen and why not |
| A11.10 | 3 | Progress indication for prolonged interactions | later | containers, pickups, documents and devices: when the Hook has them |
| A11.11 | 3 | Predictable cancellation of prolonged interactions | later | containers, pickups, documents and devices: when the Hook has them |
| A11.13 | 3 | Door handling that does not trap the player inside the door | needed | doors that move as they block, never trap him, and a locked office door that says so |
| A11.14 | 3 | Sensible behaviour when a door's path is obstructed | later | containers, pickups, documents and devices: when the Hook has them |
| A11.15 | 3 | Locked doors that communicate their status | needed | doors that move as they block, never trap him, and a locked office door that says so |
| A11.16 | 3 | Containers that visibly and mechanically change after opening | later | containers, pickups, documents and devices: when the Hook has them |
| A11.17 | 3 | Pickups that disappear or change state when taken | later | containers, pickups, documents and devices: when the Hook has them |
| A11.18 | 3 | A dropped object appearing in a sensible reachable place | later | containers, pickups, documents and devices: when the Hook has them |
| A11.19 | 3 | Readable inspection views for documents and small objects | later | containers, pickups, documents and devices: when the Hook has them |
| A11.20 | 3 | Return from inspection to the previous position and context | later | containers, pickups, documents and devices: when the Hook has them |
| A11.21 | 3 | Controls for switches, terminals and similar devices that produce a visible result | later | containers, pickups, documents and devices: when the Hook has them |
| A11.22 | 3 | Occupied objects that cannot be used by two characters simultaneously | later | containers, pickups, documents and devices: when the Hook has them |
| A11.23 | 3 | Clear distinction between harmless use and theft or aggression | needed | using a thing and smashing it are plainly different acts |
| A11.24 | 3 | An interaction ending cleanly if its object is destroyed or removed | later | containers, pickups, documents and devices: when the Hook has them |
| A13.11 | 3 | Conversations with actual listeners | later | people at stairs, seats, work and in pairs: after they walk their routines |
| A13.14 | 3 | Reactions to a nearby loud or unusual event | needed | people turn toward the smash and tell a passer-by from a vandal |
| A13.15 | 3 | Reactions to a visibly drawn weapon where the setting warrants it | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A13.16 | 3 | Different reactions to harmless proximity and actual violence | needed | people turn toward the smash and tell a passer-by from a vandal |
| A13.17 | 3 | Fleeing or taking cover from danger | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A13.18 | 3 | Escape routes that lead away from danger | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A13.19 | 3 | A response to an injured or dead person | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A13.20 | 3 | A way for panic to resolve once danger passes | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A13.21 | 3 | People who do not immediately resume cheerful chatter beside an ongoing emergency | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A14.01 | 3 | Enemies detecting the player through understandable senses | done | witnesses see by sight lines through the real perception code: [crime verdict](production/d1-probe/ue-crime-verdict.txt) |
| A14.02 | 3 | Solid cover preventing direct sight where expected | done | done by 24 Sep: crime B is occluded from the witness by the wall and he files nothing: [crime verdict](production/d1-probe/ue-crime-verdict.txt) |
| A14.03 | 3 | A readable transition from unaware to suspicious to engaged | done | how a person looks at Tom follows what they have heard (RegardFor, wired); his yes to Sheila's three ways on 29 Sep: production/approvals/2026-09-30/look-sheila-little.webp.approval.json |
| A14.04 | 3 | Reactions to relevant sounds | needed | people turn toward the smash and tell a passer-by from a vandal |
| A14.05 | 3 | Investigation of a sound's location rather than magical knowledge of the player | needed | people turn toward the smash and tell a passer-by from a vandal |
| A14.06 | 3 | Search focused on the last plausible known position | later | searches: with the law and the fights (stage 3 and 6) |
| A14.07 | 3 | A distinction between seeing the player and being told about them | done | done by 24 Sep: the friend who did not see hears it retold at confidence 0.45, one hop, as a told story and not a sighting: [crime verdict](production/d1-probe/ue-crime-verdict |
| A14.08 | 3 | Communication of an alert through visible or audible behaviour | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A14.09 | 3 | Enemy movement that uses the actual available routes | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A14.10 | 3 | Replanning when doors, vehicles or other obstacles move | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A14.11 | 3 | Enemies able to negotiate ordinary stairs and doorways | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A14.12 | 3 | Combat positioning that avoids all enemies occupying one point | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A14.13 | 3 | Enemies using appropriate engagement distance | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A14.14 | 3 | Enemies not firing continuously into an obvious obstruction | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A14.15 | 3 | Appropriate retreat, advance or repositioning | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A14.16 | 3 | A response to being flanked | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A14.17 | 3 | A response to allies being injured or killed | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A14.18 | 3 | Believable limits on accuracy and reaction speed | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A14.19 | 3 | Clear reasons when an enemy cannot be damaged or interrupted | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A14.20 | 3 | A sensible end to searching or combat | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A14.21 | 3 | No immediate forgetting of a fight merely because the player steps around a corner | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A14.22 | 3 | No pursuit through impossible or inaccessible routes | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A14.23 | 3 | No permanent lock into combat after every threat is gone | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A15.01 | 3 | A clear indication of whether the player is concealed or exposed | later | the law's response: the police come from day 4 (the town's week), past a thirty-minute session; the town's ports first |
| A15.02 | 3 | Consistent effects of posture on visibility and noise | later | the law's response: the police come from day 4 (the town's week), past a thirty-minute session; the town's ports first |
| A15.03 | 3 | Consistent effects of lighting if darkness is a stealth mechanic | later | the law's response: the police come from day 4 (the town's week), past a thirty-minute session; the town's ports first |
| A15.04 | 3 | Sound generation that matches movement and actions | later | the law's response: the police come from day 4 (the town's week), past a thirty-minute session; the town's ports first |
| A15.05 | 3 | Readable boundaries for restricted areas | later | the law's response: the police come from day 4 (the town's week), past a thirty-minute session; the town's ports first |
| A15.06 | 3 | A warning or understandable transition before punishment where appropriate | later | the law's response: the police come from day 4 (the town's week), past a thirty-minute session; the town's ports first |
| A15.07 | 3 | Distinction between suspicious behaviour and an openly hostile act | later | the law's response: the police come from day 4 (the town's week), past a thirty-minute session; the town's ports first |
| A15.08 | 3 | Witness reactions that depend on whether they could observe the event | done | done by 24 Sep: the witness files crime A and is blind to B behind the wall; the passer-by sees neither, in the shipping engine every run: [crime verdict](production/d1-probe/u |
| A15.09 | 3 | A visible or audible reporting process if reporting matters | later | the law's response: the police come from day 4 (the town's week), past a thirty-minute session; the town's ports first |
| A15.10 | 3 | A chance to respond before an alert spreads, where promised by the design | later | the law's response: the police come from day 4 (the town's week), past a thirty-minute session; the town's ports first |
| A15.11 | 3 | Law response proportionate to the apparent offence | later | the law's response: the police come from day 4 (the town's week), past a thirty-minute session; the town's ports first |
| A15.12 | 3 | An understandable wanted or pursuit state | later | the law's response: the police come from day 4 (the town's week), past a thirty-minute session; the town's ports first |
| A15.13 | 3 | Clear conditions for losing pursuit | later | the law's response: the police come from day 4 (the town's week), past a thirty-minute session; the town's ports first |
| A15.14 | 3 | Searches that do not continuously know the hidden player's exact location | later | the law's response: the police come from day 4 (the town's week), past a thirty-minute session; the town's ports first |
| A15.15 | 3 | Consistent treatment of disguises or changed appearance if supported | later | the law's response: the police come from day 4 (the town's week), past a thirty-minute session; the town's ports first |
| A15.16 | 3 | Distinction between surrender, escape and renewed aggression | later | the law's response: the police come from day 4 (the town's week), past a thirty-minute session; the town's ports first |
| A15.17 | 3 | Clear consequences of fines, arrest or confiscation | later | the law's response: the police come from day 4 (the town's week), past a thirty-minute session; the town's ports first |
| A15.18 | 3 | A usable return to ordinary play after punishment or escape | later | the law's response: the police come from day 4 (the town's week), past a thirty-minute session; the town's ports first |
| A15.19 | 3 | No punishment for an action the controls misleadingly presented as harmless | needed | the crime is its own deliberate key: nothing harmless-looking smashes a window |
| J01 | 3 | A scripted run through the slice's whole loop - walk the street, talk to someone, commit the crime, be seen, hear about it later - in the packaged build, checked automatically on every push | done | the integrated encounter runs in the packaged build on every push as the build's regression (ROADMAP, passed 24 Sep; green on 9625b9fa, 29 Sep) |
| J02 | 3 | An exploratory AI tester that plays the packaged game by looking at the screen and pressing keys, built on what Unreal already provides for driving a packaged game, run at the end of each sitting that changed the slice; findings to FOR-JAFAR worst first, bugs onto this checklist | done | tools/ai-tester/play.py, played by Claude Code with no API calls (29 Sep); walked the packaged build on 29 Sep |
| J03 | 3 | The AI tester has played the slice once with nothing serious left open | needed | the AI tester plays the friends' build with nothing serious open |
| A17.14 | 3 | Feedback for victory, escape or failure | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A20.03 | 3 | Low-health warning without making the game unreadable | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A20.05 | 3 | Healing resource consumption that matches the action | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A20.06 | 3 | Clear status effects and their duration or removal conditions | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A20.08 | 3 | A clear death or defeat state | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A20.09 | 3 | Some indication of the cause of defeat | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A20.10 | 3 | A quick, understandable retry route | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A20.12 | 3 | Consistent reset of enemies, resources and objectives on retry | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A20.13 | 3 | No respawn inside an active unavoidable hazard | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A20.14 | 3 | Clear penalties for death, if any | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A20.15 | 3 | A way to recover from an unwinnable checkpoint or stuck state | needed | a way out of a stuck spot (stand-up or return-to-pavement) |
| A24.08 | 3 | Water surfaces moving rather than appearing solid | later | weather that changes, wind in fabric, the basin's water, fire and smoke: with the town |
| A24.14 | 3 | Temporary marks such as bullet holes or blood persisting long enough to connect cause and effect | later | weather that changes, wind in fabric, the basin's water, fire and smoke: with the town |
| A25.11 | 3 | A wait or sleep mechanism where schedules make waiting necessary | needed | a clock that runs (two game minutes a second, the town's ruling), waits that stop for the town, the light following the hour (town list ci; today the game only jumps between scenes) |
| A30.03 | 3 | Distinct voices that help identify recurring characters | needed | a voice for each person who talks: Sheila has none that holds her English accent |
| A30.07 | 3 | Music transitions that do not cut abruptly without intention | later | acted delivery (his blind pick kept the game's own engine), music, radio |
| A30.09 | 3 | Exploration music that does not overwhelm ordinary interaction | later | acted delivery (his blind pick kept the game's own engine), music, radio |
| A30.11 | 3 | Avoidance of conspicuously short musical loops | later | acted delivery (his blind pick kept the game's own engine), music, radio |
| A31.01 | 3 | A clear way to start and leave a conversation | needed | start and leave a talk plainly, an acknowledgement, facing at a talking distance, lips roughly in time, the voice from the speaker, subtitles that match |
| A31.05 | 3 | Correct association between the speaking voice and visible character | needed | start and leave a talk plainly, an acknowledgement, facing at a talking distance, lips roughly in time, the voice from the speaker, subtitles that match |
| A33.06 | 3 | Rewards actually delivered and explained | later | G7: jobs beyond night one's ask |
| A33.11 | 3 | A solution when a required character is absent, dead or obstructed | later | G7: jobs beyond night one's ask |
| A34.03 | 3 | Clear current weapon, tool or ability state | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A36.04 | 3 | Clear distinction between usable, equippable, valuable and quest items | later | G9: coat and pockets beyond the one envelope, and the office's storage |
| A36.16 | 3 | A way to drop, store or otherwise manage unwanted items | later | G9: coat and pockets beyond the one envelope, and the office's storage |
| A36.18 | 3 | Clear ownership or theft status where relevant | later | G9: coat and pockets beyond the one envelope, and the office's storage |
| A38.02 | 3 | A readable current level or equivalent advancement state | later | G11: no stats; assists and milestones with the shell's later passes |
| A38.07 | 3 | Visible acknowledgement of meaningful milestones | later | G11: no stats; assists and milestones with the shell's later passes |
| A38.14 | 3 | Explanation of irreversible choices or respec limits | later | G11: no stats; assists and milestones with the shell's later passes |
| A38.15 | 3 | Progression and unlocks surviving reload | later | G11: no stats; assists and milestones with the shell's later passes |
| A39.04 | 3 | Manual saving or an explicitly communicated alternative | needed | say when the game saves; autosave at the day's turns; a sign while saving; a save on quit |
| A39.10 | 3 | Player location restored to a usable position | needed | Tom back where he stood, facing the same way, never inside a wall |
| A39.11 | 3 | Inventory and equipment restored consistently | later | save slots, profiles, damaged-save recovery and checkpoints: one playthrough and autosave suffice for friends |
| A39.12 | 3 | Mission progress and completed choices restored consistently | later | save slots, profiles, damaged-save recovery and checkpoints: one playthrough and autosave suffice for friends |
| A39.13 | 3 | Relevant world changes restored consistently | needed | the world, the people's memories and the talk restored; a save from an older build still loads (town's Core side done) |
| A39.14 | 3 | Relevant NPC states restored consistently | needed | the world, the people's memories and the talk restored; a save from an older build still loads (town's Core side done) |
| A39.18 | 3 | Previous valid progress surviving an interrupted save | needed | no death loop, a failed save keeps the last, a full disk said plainly, settings per machine, a loading screen, control only when ready, back to the title on a failed load |
| A39.20 | 3 | Recovery options for a damaged save where possible | later | save slots, profiles, damaged-save recovery and checkpoints: one playthrough and autosave suffice for friends |
| A48.16 | 3 | No obvious corruption after repeated save and load | needed | repeated save and load, and a new build over an old save, with nothing lost |
| A51.09 | 3 | Clear communication of the ending's effect on continued free play | later | optional presentation and the ending, before release |
| A51.10 | 3 | A usable post-completion state where continued exploration is offered | later | optional presentation and the ending, before release |
| K7 | 3 | Police and authority response | later | the law's response: the police come from day 4 (the town's week), past a thirty-minute session; the town's ports first |
| V3 | 3 | Music composition and licensing | later | acted delivery (his blind pick kept the game's own engine), music, radio |
| V8 | 3 | QA: functional, compliance and localisation testing | needed | the AI tester on every friends' build; the friends' session itself (the runbook is the town's) |
| V9 | 3 | Build and release engineering | needed | a packaged copy friends can download and update (the route, Steam playtest or a download, is his call when we get there) |
| A01.01 | 4 | A working launch from the installed shortcut or platform library | needed | a friend's copy starts from its own shortcut, with its data inside (no -LedgerRepo) |
| A01.02 | 4 | A visible response while the application starts | needed | a sign of life at once, and progress while shaders compile on first launch (or a shipped shader cache) |
| A01.03 | 4 | Startup that does not require unrelated windows or manual commands | needed | the talk program and the voice start with the game, no commands |
| A01.04 | 4 | Clear identification of the game being launched | needed | the window and a title card say LEDGER |
| A01.05 | 4 | A sensible initial display resolution | needed | sensible resolution, the main monitor, a sane first volume |
| A01.06 | 4 | Startup on the intended monitor | needed | sensible resolution, the main monitor, a sane first volume |
| A01.07 | 4 | Initial sound at a reasonable volume | needed | sensible resolution, the main monitor, a sane first volume |
| A01.09 | 4 | Access to subtitles before the opening dialogue | needed | subtitles on before the first line; text size and volume reachable from the title menu |
| A01.10 | 4 | Access to essential accessibility settings before gameplay | needed | subtitles on before the first line; text size and volume reachable from the title menu |
| A01.11 | 4 | A readable explanation of required account or permission requests | needed | the AI notice (wired 29 Sep) and where typed words go, shown before the first talk |
| A01.12 | 4 | Offline access to offline content where supported | needed | with no network the town still sees, remembers and talks in its written lines |
| A01.13 | 4 | A usable response to unavailable online services | needed | plain words when talk cannot be reached (town's text, the builder's screen) |
| A01.15 | 4 | An explanation when required content is still installing | later | installers and language selection come with the store (G12: English only) |
| A01.16 | 4 | An actionable error when the game cannot start | needed | a plain message when the talk program or the voice cannot start |
| A01.17 | 4 | Remembered first-run choices | needed | first-run choices and settings kept |
| A01.18 | 4 | Skippable repeated introductory logos where permitted | done | no logos yet, so nothing to skip |
| A02.01 | 4 | A clear distinction between starting, continuing and loading | needed | New game, Continue and Quit on a title screen; New game warns before replacing a save |
| A02.02 | 4 | "Continue" that selects the appropriate latest progress | needed | New game, Continue and Quit on a title screen; New game warns before replacing a save |
| A02.03 | 4 | Protection against replacing an existing playthrough with "New Game" | needed | New game, Continue and Quit on a title screen; New game warns before replacing a save |
| A02.04 | 4 | A visible selected menu item | needed | menus that work with mouse and keys, always a way back, confirm before destructive steps |
| A02.05 | 4 | Menu navigation in a predictable order | needed | menus that work with mouse and keys, always a way back, confirm before destructive steps |
| A02.06 | 4 | Consistent confirm and back controls | needed | menus that work with mouse and keys, always a way back, confirm before destructive steps |
| A02.07 | 4 | A reliable way back from every screen | needed | menus that work with mouse and keys, always a way back, confirm before destructive steps |
| A02.08 | 4 | Mouse support for visible buttons on PC | needed | menus that work with mouse and keys, always a way back, confirm before destructive steps |
| A02.09 | 4 | Clickable areas that match their visible buttons | needed | menus that work with mouse and keys, always a way back, confirm before destructive steps |
| A02.10 | 4 | Scroll-wheel support for scrolling lists | later | controller support and finer menu comfort: keyboard and mouse first |
| A02.11 | 4 | Controller navigation that reaches every setting | later | controller support and finer menu comfort: keyboard and mouse first |
| A02.12 | 4 | Selection that remains visible while a list scrolls | later | controller support and finer menu comfort: keyboard and mouse first |
| A02.13 | 4 | Useful explanations for disabled options | later | controller support and finer menu comfort: keyboard and mouse first |
| A02.14 | 4 | Confirmation before destructive actions | needed | menus that work with mouse and keys, always a way back, confirm before destructive steps |
| A02.15 | 4 | Dialogues that capture input without activating buttons behind them | needed | menus that work with mouse and keys, always a way back, confirm before destructive steps |
| A02.16 | 4 | Menus that remember position when returning from a detail screen | later | controller support and finer menu comfort: keyboard and mouse first |
| A02.17 | 4 | Text entry that works with the current device | needed | typed talk takes the keyboard's text, backspace, accents and paste |
| A02.18 | 4 | An on-screen keyboard when physical typing is unavailable | later | controller support and finer menu comfort: keyboard and mouse first |
| A02.20 | 4 | Protection against repeated clicks starting the same operation twice | needed | menus that work with mouse and keys, always a way back, confirm before destructive steps |
| A03.01 | 4 | Movement and actions that respond promptly to input | needed | prompt, consistent, frame-rate-independent keys and mouse; no double presses; diagonals not faster; no mouse acceleration |
| A03.02 | 4 | Camera movement that responds promptly | needed | prompt, consistent, frame-rate-independent keys and mouse; no double presses; diagonals not faster; no mouse acceleration |
| A03.03 | 4 | Consistent controls across equivalent situations | needed | prompt, consistent, frame-rate-independent keys and mouse; no double presses; diagonals not faster; no mouse acceleration |
| A03.04 | 4 | Correct button prompts for the connected device | later | controller support and finer menu comfort: keyboard and mouse first |
| A03.05 | 4 | Prompts that update after rebinding | later | controller support and finer menu comfort: keyboard and mouse first |
| A03.06 | 4 | Switching between supported mouse, keyboard and controller input | later | controller support and finer menu comfort: keyboard and mouse first |
| A03.08 | 4 | No duplicate action from one physical button press | needed | prompt, consistent, frame-rate-independent keys and mouse; no double presses; diagonals not faster; no mouse acceleration |
| A03.09 | 4 | Correct distinction between pressing, holding and releasing | needed | prompt, consistent, frame-rate-independent keys and mouse; no double presses; diagonals not faster; no mouse acceleration |
| A03.10 | 4 | Clear feedback when an action requires holding | later | controller support and finer menu comfort: keyboard and mouse first |
| A03.11 | 4 | Reasonable tolerance for slightly early action presses | later | controller support and finer menu comfort: keyboard and mouse first |
| A03.12 | 4 | Predictable handling of conflicting simultaneous inputs | needed | typing to someone never walks Tom (WASD inside the talk box) |
| A03.13 | 4 | Movement that stops when the movement input stops | needed | prompt, consistent, frame-rate-independent keys and mouse; no double presses; diagonals not faster; no mouse acceleration |
| A03.14 | 4 | No stuck movement after opening a menu or changing focus | needed | no stuck movement after a menu or alt-tab; the click that closes a menu does nothing else |
| A03.15 | 4 | No attack caused by the same click that dismisses a menu | needed | no stuck movement after a menu or alt-tab; the click that closes a menu does nothing else |
| A03.16 | 4 | No unexpected action from an input held through a loading screen | needed | no stuck movement after a menu or alt-tab; the click that closes a menu does nothing else |
| A03.17 | 4 | Analogue movement speed on supported sticks | later | controller support and finer menu comfort: keyboard and mouse first |
| A03.18 | 4 | Equal intended movement speed in straight and diagonal directions | needed | prompt, consistent, frame-rate-independent keys and mouse; no double presses; diagonals not faster; no mouse acceleration |
| A03.19 | 4 | Sensible controller dead zones | later | controller support and finer menu comfort: keyboard and mouse first |
| A03.20 | 4 | Predictable mouse movement without unwanted acceleration | needed | prompt, consistent, frame-rate-independent keys and mouse; no double presses; diagonals not faster; no mouse acceleration |
| A03.22 | 4 | Safe reconnection without restarting the game | later | controller support and finer menu comfort: keyboard and mouse first |
| A03.23 | 4 | Input handling independent of frame rate | needed | prompt, consistent, frame-rate-independent keys and mouse; no double presses; diagonals not faster; no mouse acceleration |
| A03.24 | 4 | Clear control ownership when several controllers are connected | later | controller support and finer menu comfort: keyboard and mouse first |
| A04.01 | 4 | An unmistakable transition from watching to controlling | needed | a clear hand-over to the player, a first view of something useful, a safe street to try walking and looking |
| A04.02 | 4 | A starting camera aimed at something useful | needed | a clear hand-over to the player, a first view of something useful, a safe street to try walking and looking |
| A04.03 | 4 | A safe opportunity to test movement | needed | a clear hand-over to the player, a first view of something useful, a safe street to try walking and looking |
| A04.04 | 4 | A safe opportunity to test the camera | needed | a clear hand-over to the player, a first view of something useful, a safe street to try walking and looking |
| A04.05 | 4 | A clear initial purpose | needed | a clear first purpose and destination (day one: Sheila's walk-round, town list cg) |
| A04.06 | 4 | A discoverable first destination or activity | needed | a clear first purpose and destination (day one: Sheila's walk-round, town list cg) |
| A04.07 | 4 | Instructions shown when their actions become relevant | needed | hints the first time they matter, in the player's keys, long enough to read, stopping once learned (the town's hint book; the builder's screen) |
| A04.08 | 4 | Instructions using the player's actual bindings | needed | hints the first time they matter, in the player's keys, long enough to read, stopping once learned (the town's hint book; the builder's screen) |
| A04.09 | 4 | Time to read an instruction before it disappears | needed | hints the first time they matter, in the player's keys, long enough to read, stopping once learned (the town's hint book; the builder's screen) |
| A04.10 | 4 | Confirmation that a tutorial action succeeded | needed | hints the first time they matter, in the player's keys, long enough to read, stopping once learned (the town's hint book; the builder's screen) |
| A04.11 | 4 | A way to recover instructions dismissed accidentally | later | recovering and skipping hints: after the hint book is in |
| A04.12 | 4 | Tutorials that cope with an action performed early | needed | hints the first time they matter, in the player's keys, long enough to read, stopping once learned (the town's hint book; the builder's screen) |
| A04.13 | 4 | Tutorials that stop repeating after understanding is demonstrated | needed | hints the first time they matter, in the player's keys, long enough to read, stopping once learned (the town's hint book; the builder's screen) |
| A04.14 | 4 | A way to revisit controls and basic rules | needed | the controls listed in the pause menu |
| A04.15 | 4 | A way to skip familiar instruction without breaking progression | later | recovering and skipping hints: after the hint book is in |
| A04.16 | 4 | An opening that permits ordinary experimentation without trapping the player | needed | a clear hand-over to the player, a first view of something useful, a safe street to try walking and looking |
| A05.03 | 4 | A useful default field of view | needed | free look, a good distance and field of view, Tom readable, smoothed but not detached |
| A05.22 | 4 | Camera shake that does not hide essential information | needed | no shake, a level horizon |
| A11.01 | 4 | A clear way to distinguish usable objects from decoration | needed | a prompt on the thing he can use, in reach, not through walls, talk before open, saying what will happen and why not |
| A11.03 | 4 | Prompts attached to the intended object | needed | a prompt on the thing he can use, in reach, not through walls, talk before open, saying what will happen and why not |
| A20.11 | 4 | Checkpoints placed to avoid needless repetition | later | save slots, profiles, damaged-save recovery and checkpoints: one playthrough and autosave suffice for friends |
| A20.16 | 4 | Ability to adjust relevant difficulty or assistance without discarding the playthrough | later | save slots, profiles, damaged-save recovery and checkpoints: one playthrough and autosave suffice for friends |
| A31.11 | 4 | Important information recoverable after interruption | needed | the last lines recoverable after an interruption |
| A32.01 | 4 | A clear distinction between a cutscene and interactive control | needed | the evening's cut and day one's walk-round read as watching, then hand back control sensibly |
| A32.03 | 4 | Characters and props arriving in the correct positions | later | G6: the handful of short scenes (the arrival with the suitcase) |
| A32.04 | 4 | Player equipment and appearance carried into scenes where appropriate | later | G6: the handful of short scenes (the arrival with the suitcase) |
| A32.06 | 4 | A way to pause where the presentation permits it | later | G6: the handful of short scenes (the arrival with the suitcase) |
| A32.07 | 4 | A way to skip already-seen scenes | later | G6: the handful of short scenes (the arrival with the suitcase) |
| A32.08 | 4 | Protection against accidentally skipping an entire scene | later | G6: the handful of short scenes (the arrival with the suitcase) |
| A32.09 | 4 | Subtitles that survive cinematic framing and letterboxing | later | G6: the handful of short scenes (the arrival with the suitcase) |
| A32.10 | 4 | Gameplay resuming in a sensible position and facing | needed | the evening's cut and day one's walk-round read as watching, then hand back control sensibly |
| A32.11 | 4 | No damage or enemy activity during a scene that denies player control unless deliberately communicated | later | G6: the handful of short scenes (the arrival with the suitcase) |
| A32.12 | 4 | Correct state changes even when a scene is skipped | needed | skipping Sheila's walk-round still counts her as met (town list cg) |
| A32.13 | 4 | No prolonged loading hidden behind a frozen character or black screen without feedback | later | G6: the handful of short scenes (the arrival with the suitcase) |
| A33.01 | 4 | A clear current objective or understandable self-directed goal | needed | a light note of what Tom is doing, reachable from the pause menu, updating as it changes |
| A33.02 | 4 | A way to review the objective after forgetting it | needed | a light note of what Tom is doing, reachable from the pause menu, updating as it changes |
| A33.03 | 4 | Clear distinction between mandatory and optional tasks | later | G7: jobs beyond night one's ask |
| A33.04 | 4 | Objective progress updating after relevant actions | needed | a light note of what Tom is doing, reachable from the pause menu, updating as it changes |
| A33.05 | 4 | Completion acknowledged rather than silently recorded | needed | a light note of what Tom is doing, reachable from the pause menu, updating as it changes |
| A33.07 | 4 | Failure conditions communicated before they matter where possible | later | G7: jobs beyond night one's ask |
| A33.08 | 4 | A clear response to leaving an active mission area | later | G7: jobs beyond night one's ask |
| A33.09 | 4 | Tasks that survive doing valid steps in an unexpected order | later | G7: jobs beyond night one's ask |
| A33.10 | 4 | Recognition of an item already owned when it is requested | later | G7: jobs beyond night one's ask |
| A33.12 | 4 | Protection against permanently losing an indispensable quest item | later | G7: jobs beyond night one's ask |
| A33.13 | 4 | Required interactions remaining usable despite ordinary world changes | later | G7: jobs beyond night one's ask |
| A33.14 | 4 | A way to restart or recover a broken activity | later | G7: jobs beyond night one's ask |
| A33.15 | 4 | Clear communication of time limits | later | G7: jobs beyond night one's ask |
| A33.16 | 4 | Dialogue and markers agreeing on the destination | out | G7: No waypoint markers to agree with |
| A33.17 | 4 | Markers resolving to reachable interaction points | out | G7: No waypoint markers |
| A33.18 | 4 | Sensible handling of multiple simultaneous missions | later | G7: jobs beyond night one's ask |
| A33.19 | 4 | Completed objectives not continuing to issue obsolete instructions | later | G7: jobs beyond night one's ask |
| A33.20 | 4 | A reason to explore beyond the main route | later | G7: jobs beyond night one's ask |
| A34.02 | 4 | Ammunition or resource information readable before an action fails | later | resources, status effects and a minimal HUD option: none in the friends' build |
| A34.04 | 4 | Feedback when an action is on cooldown or otherwise unavailable | needed | prompts that don't hide the thing, notices long enough and never piled up, no overlaps, nothing on screen during a cut, the world's running state clear |
| A34.05 | 4 | Interaction prompts that do not obscure the object | needed | prompts that don't hide the thing, notices long enough and never piled up, no overlaps, nothing on screen during a cut, the world's running state clear |
| A34.06 | 4 | Aiming indicators visible against varied backgrounds | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A34.09 | 4 | Status-effect indicators that explain their meaning | later | resources, status effects and a minimal HUD option: none in the friends' build |
| A34.10 | 4 | Notifications that remain long enough to read | needed | prompts that don't hide the thing, notices long enough and never piled up, no overlaps, nothing on screen during a cut, the world's running state clear |
| A34.11 | 4 | Notification handling that does not bury urgent information | needed | prompts that don't hide the thing, notices long enough and never piled up, no overlaps, nothing on screen during a cut, the world's running state clear |
| A34.12 | 4 | No overlapping subtitles, prompts and objective text | needed | prompts that don't hide the thing, notices long enough and never piled up, no overlaps, nothing on screen during a cut, the world's running state clear |
| A34.13 | 4 | Appropriate removal or reduction of HUD during noninteractive scenes | needed | prompts that don't hide the thing, notices long enough and never piled up, no overlaps, nothing on screen during a cut, the world's running state clear |
| A34.14 | 4 | A clear indication when the world continues running behind a menu | needed | prompts that don't hide the thing, notices long enough and never piled up, no overlaps, nothing on screen during a cut, the world's running state clear |
| A34.15 | 4 | UI values that match actual gameplay state | needed | prompts that don't hide the thing, notices long enough and never piled up, no overlaps, nothing on screen during a cut, the world's running state clear |
| A34.16 | 4 | A way to reduce unnecessary HUD elements where supported | later | resources, status effects and a minimal HUD option: none in the friends' build |
| A35.01 | 4 | A map that opens promptly and returns cleanly to gameplay | later | G8: the paper map, when the town is bigger than the Hook |
| A35.02 | 4 | A visible player position | later | G8: the paper map, when the town is bigger than the Hook |
| A35.03 | 4 | A clear indication of facing or travel direction | later | G8: the paper map, when the town is bigger than the Hook |
| A35.04 | 4 | Useful map scale and zoom | later | G8: the paper map, when the town is bigger than the Hook |
| A35.05 | 4 | Panning with the current input device | later | G8: the paper map, when the town is bigger than the Hook |
| A35.06 | 4 | Legible labels and distinguishable icons | later | G8: the paper map, when the town is bigger than the Hook |
| A35.07 | 4 | A legend or explanation for unfamiliar symbols | later | G8: the paper map, when the town is bigger than the Hook |
| A35.08 | 4 | Selection of overlapping icons | out | G8: A printed paper map has no selectable icons |
| A35.09 | 4 | A way to place and remove a personal waypoint | out | G8: No waypoints; a paper map, not a navigation screen |
| A35.11 | 4 | Recalculation after leaving a suggested route | out | G8: No GPS-style routing |
| A35.12 | 4 | Height or floor distinction where a flat marker would mislead | out | G8: No markers on the paper map to mislead |
| A35.13 | 4 | Clear distinction between discovered and undiscovered places | later | G8: the paper map, when the town is bigger than the Hook |
| A35.14 | 4 | Clear distinction between completed and incomplete activities | later | G8: the paper map, when the town is bigger than the Hook |
| A35.15 | 4 | Navigation aids that remain consistent with world signs and names | later | G8: the paper map, when the town is bigger than the Hook |
| A35.16 | 4 | A journal that preserves useful task and story information | later | G8: the Ledger notebook; how it reads waits on his ruling (town list 6i); the town keeps the knowledge |
| A35.17 | 4 | A way to review recently acquired notes or clues | later | G8: the Ledger notebook; how it reads waits on his ruling (town list 6i); the town keeps the knowledge |
| A36.01 | 4 | A reliable record of what the player owns | needed | the envelope of night one: in his pocket, said when taken and given |
| A36.02 | 4 | Pickup feedback identifying what was acquired | needed | the envelope of night one: in his pocket, said when taken and given |
| A36.03 | 4 | Item names, quantities and useful descriptions | needed | the envelope of night one: in his pocket, said when taken and given |
| A36.05 | 4 | Sorting or filtering sufficient for the expected inventory size | later | G9: coat and pockets beyond the one envelope, and the office's storage |
| A36.06 | 4 | Consistent stacking of identical items | later | G9: coat and pockets beyond the one envelope, and the office's storage |
| A36.07 | 4 | Quantity selection for moving or discarding stacks | later | G9: coat and pockets beyond the one envelope, and the office's storage |
| A36.08 | 4 | A clear equipped state | later | G9: coat and pockets beyond the one envelope, and the office's storage |
| A36.10 | 4 | Equipment restrictions explained before selection | later | G9: coat and pockets beyond the one envelope, and the office's storage |
| A36.11 | 4 | Immediate gameplay and visual effects from equipping | later | G9: coat and pockets beyond the one envelope, and the office's storage |
| A36.12 | 4 | Quick access to frequently used items | later | G9: coat and pockets beyond the one envelope, and the office's storage |
| A36.13 | 4 | Consistent consumption of single-use items | later | G9: coat and pockets beyond the one envelope, and the office's storage |
| A36.14 | 4 | A clear capacity or weight rule if capacity is limited | later | G9: coat and pockets beyond the one envelope, and the office's storage |
| A36.15 | 4 | Feedback when a pickup fails because the inventory is full | later | G9: coat and pockets beyond the one envelope, and the office's storage |
| A36.17 | 4 | Protection against accidental destruction of valuable items | later | G9: coat and pockets beyond the one envelope, and the office's storage |
| A36.19 | 4 | Containers retaining sensible contents after being opened | later | G9: coat and pockets beyond the one envelope, and the office's storage |
| A36.20 | 4 | Inventory state surviving death and reload according to the stated rules | later | G9: coat and pockets beyond the one envelope, and the office's storage |
| A36.21 | 4 | Menus remaining usable while quantities change | later | G9: coat and pockets beyond the one envelope, and the office's storage |
| A38.01 | 4 | Clear feedback when experience or progression is earned | later | G11: no stats; assists and milestones with the shell's later passes |
| A38.03 | 4 | Explanation of what an upgrade actually changes | out | G11: No upgrades; Tom has no stats |
| A38.04 | 4 | Clear prerequisites and costs | out | G11: No skill trees with prerequisites or costs |
| A38.05 | 4 | Immediate application of purchased abilities | out | G11: No purchased abilities; Tom has no stats |
| A38.06 | 4 | Instruction for newly unlocked actions | later | G11: no stats; assists and milestones with the shell's later passes |
| A38.11 | 4 | Difficulty descriptions that say what changes | later | G11: no stats; assists and milestones with the shell's later passes |
| A38.12 | 4 | Appropriate acknowledgement when difficulty is changed | later | G11: no stats; assists and milestones with the shell's later passes |
| A39.01 | 4 | A clear explanation of when progress is saved | needed | say when the game saves; autosave at the day's turns; a sign while saving; a save on quit |
| A39.02 | 4 | Autosaving at sensible milestones | needed | say when the game saves; autosave at the day's turns; a sign while saving; a save on quit |
| A39.03 | 4 | A visible indication while a save is in progress | needed | say when the game saves; autosave at the day's turns; a sign while saving; a save on quit |
| A39.05 | 4 | Clear reasons when saving is temporarily unavailable | later | save slots, profiles, damaged-save recovery and checkpoints: one playthrough and autosave suffice for friends |
| A39.06 | 4 | A clear distinction between checkpoint, autosave and manual save | later | save slots, profiles, damaged-save recovery and checkpoints: one playthrough and autosave suffice for friends |
| A39.07 | 4 | Save entries identifiable by time, location or progress | needed | the save named by day and hour; confirm before overwriting |
| A39.08 | 4 | Confirmation before overwriting or deleting a save | needed | the save named by day and hour; confirm before overwriting |
| A39.09 | 4 | Separate playthroughs or profiles not silently overwriting each other | later | save slots, profiles, damaged-save recovery and checkpoints: one playthrough and autosave suffice for friends |
| A39.15 | 4 | Timers and temporary effects restored according to clear rules | later | save slots, profiles, damaged-save recovery and checkpoints: one playthrough and autosave suffice for friends |
| A39.16 | 4 | No duplicated rewards or consumed items after reloading | later | save slots, profiles, damaged-save recovery and checkpoints: one playthrough and autosave suffice for friends |
| A39.17 | 4 | No loading into an unavoidable death loop | needed | no death loop, a failed save keeps the last, a full disk said plainly, settings per machine, a loading screen, control only when ready, back to the title on a failed load |
| A39.19 | 4 | A useful message when storage is full or unwritable | needed | no death loop, a failed save keeps the last, a full disk said plainly, settings per machine, a loading screen, control only when ready, back to the title on a failed load |
| A39.21 | 4 | Clear compatibility handling after updates or missing downloadable content | needed | the world, the people's memories and the talk restored; a save from an older build still loads (town's Core side done) |
| A39.22 | 4 | Offline saves retained when reconnecting | later | the platform's machinery, with the store |
| A39.25 | 4 | Machine-specific graphics settings not making another machine unusable | needed | no death loop, a failed save keeps the last, a full disk said plainly, settings per machine, a loading screen, control only when ready, back to the title on a failed load |
| A39.27 | 4 | Control withheld until the loaded world is ready | needed | no death loop, a failed save keeps the last, a full disk said plainly, settings per machine, a loading screen, control only when ready, back to the title on a failed load |
| A39.28 | 4 | A sensible return to title or another save after load failure | needed | no death loop, a failed save keeps the last, a full disk said plainly, settings per machine, a loading screen, control only when ready, back to the title on a failed load |
| A40.01 | 4 | A pause command available during ordinary single-player play | needed | Esc pauses the world, sound and people; resume without a queued step; losing focus pauses |
| A40.02 | 4 | A clear distinction between menus that pause and menus that do not | needed | Esc pauses the world, sound and people; resume without a queued step; losing focus pauses |
| A40.03 | 4 | Simulation, animation and relevant sound pausing consistently | needed | Esc pauses the world, sound and people; resume without a queued step; losing focus pauses |
| A40.04 | 4 | Resuming without a queued accidental attack or movement | needed | Esc pauses the world, sound and people; resume without a queued step; losing focus pauses |
| A40.05 | 4 | Sensible behaviour when the application loses focus | needed | Esc pauses the world, sound and people; resume without a queued step; losing focus pauses |
| A40.06 | 4 | Safe recovery after system sleep or suspend | later | save slots, profiles, damaged-save recovery and checkpoints: one playthrough and autosave suffice for friends |
| A40.07 | 4 | A clear route back to the title menu | needed | back to title, quit to desktop with a save, no process or sound left behind, settings kept |
| A40.08 | 4 | A clear quit-to-desktop option on PC | needed | back to title, quit to desktop with a save, no process or sound left behind, settings kept |
| A40.09 | 4 | A warning when quitting would lose unsaved progress | needed | back to title, quit to desktop with a save, no process or sound left behind, settings kept |
| A40.10 | 4 | Quitting that waits for an active save or clearly explains why it cannot yet finish | needed | back to title, quit to desktop with a save, no process or sound left behind, settings kept |
| A40.11 | 4 | No indefinitely hanging process after closing the game | needed | back to title, quit to desktop with a save, no process or sound left behind, settings kept |
| A40.12 | 4 | No continued game audio after exit | needed | back to title, quit to desktop with a save, no process or sound left behind, settings kept |
| A40.13 | 4 | Settings and intended progress retained on the next launch | needed | back to title, quit to desktop with a save, no process or sound left behind, settings kept |
| A40.14 | 4 | A useful reminder of current objectives after a longer break | later | save slots, profiles, damaged-save recovery and checkpoints: one playthrough and autosave suffice for friends |
| A41.01 | 4 | Resolution selection appropriate to the display | needed | resolution, window mode, refresh, a frame limit, vsync, presets that matter, brightness, UI scale, aspect, a safe revert, kept |
| A41.02 | 4 | Windowed, borderless or fullscreen options appropriate to the platform | needed | resolution, window mode, refresh, a frame limit, vsync, presets that matter, brightness, UI scale, aspect, a safe revert, kept |
| A41.03 | 4 | Monitor selection on supported PC setups | later | finer display settings, after the presets |
| A41.04 | 4 | Refresh-rate handling that uses the chosen display correctly | needed | resolution, window mode, refresh, a frame limit, vsync, presets that matter, brightness, UI scale, aspect, a safe revert, kept |
| A41.05 | 4 | A frame-rate limit option on PC | needed | resolution, window mode, refresh, a frame limit, vsync, presets that matter, brightness, UI scale, aspect, a safe revert, kept |
| A41.06 | 4 | Vertical synchronisation or an equivalent tearing control | needed | resolution, window mode, refresh, a frame limit, vsync, presets that matter, brightness, UI scale, aspect, a safe revert, kept |
| A41.07 | 4 | Quality presets with meaningful performance differences | needed | resolution, window mode, refresh, a frame limit, vsync, presets that matter, brightness, UI scale, aspect, a safe revert, kept |
| A41.08 | 4 | Individual control over major expensive visual features | later | finer display settings, after the presets |
| A41.09 | 4 | Texture quality appropriate to available graphics memory | later | finer display settings, after the presets |
| A41.10 | 4 | Field-of-view adjustment where the camera model permits it | later | finer display settings, after the presets |
| A41.11 | 4 | Brightness or gamma calibration with a useful reference | needed | resolution, window mode, refresh, a frame limit, vsync, presets that matter, brightness, UI scale, aspect, a safe revert, kept |
| A41.13 | 4 | Motion-blur control | later | finer display settings, after the presets |
| A41.15 | 4 | Upscaling and image-quality choices where supported | later | finer display settings, after the presets |
| A41.16 | 4 | Clear distinction between rendered frame rate and generated-frame options where offered | later | finer display settings, after the presets |
| A41.17 | 4 | UI scaling that remains usable at the chosen resolution | needed | resolution, window mode, refresh, a frame limit, vsync, presets that matter, brightness, UI scale, aspect, a safe revert, kept |
| A41.18 | 4 | Correct aspect-ratio handling without stretched people or clipped HUD | needed | resolution, window mode, refresh, a frame limit, vsync, presets that matter, brightness, UI scale, aspect, a safe revert, kept |
| A41.19 | 4 | Preview or explanation of what a graphics setting changes | later | finer display settings, after the presets |
| A41.20 | 4 | Confirmation with automatic reversal of an unusable display mode | needed | resolution, window mode, refresh, a frame limit, vsync, presets that matter, brightness, UI scale, aspect, a safe revert, kept |
| A41.21 | 4 | Clear indication when a setting requires restarting | needed | resolution, window mode, refresh, a frame limit, vsync, presets that matter, brightness, UI scale, aspect, a safe revert, kept |
| A41.22 | 4 | Settings that remain applied after restarting | needed | resolution, window mode, refresh, a frame limit, vsync, presets that matter, brightness, UI scale, aspect, a safe revert, kept |
| A42.01 | 4 | Separate master, dialogue, effects and music volume controls | needed | master, voices, effects volumes heard while set; mouse sensitivity and inversion; the controls explained |
| A42.02 | 4 | Volume changes audible while adjusting them | needed | master, voices, effects volumes heard while set; mouse sensitivity and inversion; the controls explained |
| A42.03 | 4 | Correct selection or following of the intended output device | later | rebinding, controller and finer audio settings: the friends' build is keyboard and mouse |
| A42.04 | 4 | Speaker and headphone presentation choices where relevant | later | rebinding, controller and finer audio settings: the friends' build is keyboard and mouse |
| A42.05 | 4 | A reduced dynamic-range option for quiet listening | later | rebinding, controller and finer audio settings: the friends' build is keyboard and mouse |
| A42.07 | 4 | Full rebinding of ordinary gameplay actions | later | rebinding, controller and finer audio settings: the friends' build is keyboard and mouse |
| A42.08 | 4 | Rebinding of menu actions where necessary for accessibility | later | rebinding, controller and finer audio settings: the friends' build is keyboard and mouse |
| A42.09 | 4 | Warnings about conflicting bindings | later | rebinding, controller and finer audio settings: the friends' build is keyboard and mouse |
| A42.10 | 4 | A way to restore default bindings | later | rebinding, controller and finer audio settings: the friends' build is keyboard and mouse |
| A42.11 | 4 | Independent horizontal and vertical sensitivity where useful | needed | master, voices, effects volumes heard while set; mouse sensitivity and inversion; the controls explained |
| A42.12 | 4 | Separate aiming and general camera sensitivity | later | rebinding, controller and finer audio settings: the friends' build is keyboard and mouse |
| A42.13 | 4 | Camera inversion options | needed | master, voices, effects volumes heard while set; mouse sensitivity and inversion; the controls explained |
| A42.14 | 4 | Adjustable controller dead zones | later | rebinding, controller and finer audio settings: the friends' build is keyboard and mouse |
| A42.15 | 4 | Stick and trigger response options where supported | later | rebinding, controller and finer audio settings: the friends' build is keyboard and mouse |
| A42.16 | 4 | Hold-versus-toggle choices for sustained actions | later | rebinding, controller and finer audio settings: the friends' build is keyboard and mouse |
| A42.17 | 4 | Adjustable vibration and haptic intensity | later | rebinding, controller and finer audio settings: the friends' build is keyboard and mouse |
| A42.19 | 4 | Controls explained without requiring memorisation of a diagram | needed | master, voices, effects volumes heard while set; mouse sensitivity and inversion; the controls explained |
| A43.01 | 4 | Readable default text at normal viewing distance | needed | readable text at his screen size and a friend's, a size setting, backgrounds behind subtitles, nothing by colour alone |
| A43.02 | 4 | Adjustable text size | needed | readable text at his screen size and a friend's, a size setting, backgrounds behind subtitles, nothing by colour alone |
| A43.03 | 4 | Text reflow without clipping after enlargement | later | fuller accessibility (narration, colour-vision, mono), with the shell before strangers play |
| A43.04 | 4 | Adequate contrast between text and background | needed | readable text at his screen size and a friend's, a size setting, backgrounds behind subtitles, nothing by colour alone |
| A43.05 | 4 | Configurable text backgrounds or outlines where needed | needed | readable text at his screen size and a friend's, a size setting, backgrounds behind subtitles, nothing by colour alone |
| A43.06 | 4 | Important information conveyed through more than colour alone | needed | readable text at his screen size and a friend's, a size setting, backgrounds behind subtitles, nothing by colour alone |
| A43.07 | 4 | Distinguishable friendly, hostile and neutral markers for different colour-vision needs | later | fuller accessibility (narration, colour-vision, mono), with the shell before strangers play |
| A43.09 | 4 | Optional emphasis for interactable objects where needed | later | fuller accessibility (narration, colour-vision, mono), with the shell before strangers play |
| A43.10 | 4 | A way to distinguish important objects from visual clutter | later | fuller accessibility (narration, colour-vision, mono), with the shell before strangers play |
| A43.11 | 4 | Menu narration or screen-reader support where offered | later | fuller accessibility (narration, colour-vision, mono), with the shell before strangers play |
| A43.12 | 4 | Narration that announces selection, value and changes | later | fuller accessibility (narration, colour-vision, mono), with the shell before strangers play |
| A43.13 | 4 | Narrated or otherwise accessible error and confirmation messages | later | fuller accessibility (narration, colour-vision, mono), with the shell before strangers play |
| A43.14 | 4 | Accessible reading of essential documents and clues | later | fuller accessibility (narration, colour-vision, mono), with the shell before strangers play |
| A43.15 | 4 | UI focus that remains visible and inside the active dialogue | later | fuller accessibility (narration, colour-vision, mono), with the shell before strangers play |
| A43.16 | 4 | Gameplay information that remains legible after changing display size or resolution | needed | readable text at his screen size and a friend's, a size setting, backgrounds behind subtitles, nothing by colour alone |
| A44.01 | 4 | Subtitles available for essential dialogue | needed | subtitles and captions from the start, naming the speaker, long enough, sizeable, with the smash shown as well as heard |
| A44.02 | 4 | Subtitles available before the opening scene | needed | subtitles and captions from the start, naming the speaker, long enough, sizeable, with the smash shown as well as heard |
| A44.03 | 4 | Speaker identification when the speaker is not obvious | needed | subtitles and captions from the start, naming the speaker, long enough, sizeable, with the smash shown as well as heard |
| A44.04 | 4 | Directional indication for important off-screen speech or sound where needed | later | fuller accessibility (narration, colour-vision, mono), with the shell before strangers play |
| A44.06 | 4 | Sufficient subtitle display time | needed | subtitles and captions from the start, naming the speaker, long enough, sizeable, with the smash shown as well as heard |
| A44.07 | 4 | Subtitle styling and size options | needed | subtitles and captions from the start, naming the speaker, long enough, sizeable, with the smash shown as well as heard |
| A44.08 | 4 | Mono output without losing essential information | later | fuller accessibility (narration, colour-vision, mono), with the shell before strangers play |
| A44.09 | 4 | Visual equivalents for gameplay-critical audio signals | needed | subtitles and captions from the start, naming the speaker, long enough, sizeable, with the smash shown as well as heard |
| A44.10 | 4 | Alternatives to required speech input where voice commands exist | later | fuller accessibility (narration, colour-vision, mono), with the shell before strangers play |
| A45.01 | 4 | Core actions remappable rather than only swapping entire preset layouts | later | motor accessibility with rebinding |
| A45.02 | 4 | Alternatives to repeated rapid button presses | later | motor accessibility with rebinding |
| A45.03 | 4 | Alternatives to prolonged button holds | later | motor accessibility with rebinding |
| A45.04 | 4 | Alternatives to difficult simultaneous button combinations | later | motor accessibility with rebinding |
| A45.05 | 4 | Adjustable timing windows for demanding interactions where offered | later | motor accessibility with rebinding |
| A45.07 | 4 | Menu operation without precise pointer placement | needed | menus work from the keyboard; Esc always pauses |
| A45.08 | 4 | Adjustable cursor or menu-navigation speed | later | motor accessibility with rebinding |
| A45.09 | 4 | Assistance for sustained steering, aiming or camera control where offered | later | motor accessibility with rebinding |
| A45.10 | 4 | A way to pause without demanding the same dexterity as combat | needed | menus work from the keyboard; Esc always pauses |
| A45.11 | 4 | Support for compatible alternative controllers | later | motor accessibility with rebinding |
| A46.01 | 4 | Plain explanations of goals and unfamiliar terms | needed | plain words, time to read, clear effects of a menu change, a content note (menace, a smashed window), settings kept |
| A46.02 | 4 | A way to review tutorials and recent information | later | comfort and assists with the shell |
| A46.03 | 4 | Adjustable or pausable reading time | needed | plain words, time to read, clear effects of a menu change, a content note (menace, a smashed window), settings kept |
| A46.04 | 4 | Clear indication of what changed after a menu action | needed | plain words, time to read, clear effects of a menu change, a content note (menace, a smashed window), settings kept |
| A46.05 | 4 | Assistance settings separated by challenge where practical | later | comfort and assists with the shell |
| A46.06 | 4 | Difficulty changes that do not require restarting the game | later | comfort and assists with the shell |
| A46.07 | 4 | Optional navigation assistance where the world is difficult to parse | later | comfort and assists with the shell |
| A46.08 | 4 | Reduced camera shake and head movement options | later | comfort and assists with the shell |
| A46.09 | 4 | Control over camera recentering where it causes discomfort | later | comfort and assists with the shell |
| A46.10 | 4 | Control over strong flashing and other avoidable visual triggers | later | comfort and assists with the shell |
| A46.11 | 4 | Reduced motion or animated-background options in menus | later | comfort and assists with the shell |
| A46.12 | 4 | Control over repetitive UI pulsing and notifications | later | comfort and assists with the shell |
| A46.13 | 4 | Clear content information where potentially distressing content is central | needed | plain words, time to read, clear effects of a menu change, a content note (menace, a smashed window), settings kept |
| A46.14 | 4 | Accessibility settings retained across sessions | needed | plain words, time to read, clear effects of a menu change, a content note (menace, a smashed window), settings kept |
| A49.10 | 4 | Required permissions requested at a relevant moment | later | the platform's machinery, with the store |
| A49.11 | 4 | Optional data collection distinguishable from required operation | needed | screenshots work; what is collected (the session record, typed words) said plainly (town's words) |
| A49.14 | 4 | Battery or power interruptions not corrupting the last completed save | later | the platform's machinery, with the store |
| A51.03 | 4 | A way to hide the HUD for clean captures | later | optional presentation and the ending, before release |
| A51.07 | 4 | Credits accessible without having to finish the game | later | optional presentation and the ending, before release |
| A51.13 | 4 | Returning after a long break without having to reconstruct the entire playthrough from memory | later | optional presentation and the ending, before release |
| A1 | 4 | Splash and logo screens, legal notices | later | optional presentation and the ending, before release |
| A2 | 4 | First-run hardware detection and default quality preset | needed | first-run detection of the card and a default quality preset: friends' PCs differ |
| D1 | 4 | Keyboard and mouse | needed | keyboard and mouse throughout, with look sensitivity |
| E4 | 4 | Look sensitivity and acceleration | needed | keyboard and mouse throughout, with look sensitivity |
| F2 | 4 | Objective or quest log | needed | a light note of what Tom is doing, reachable from the pause menu, updating as it changes |
| F7 | 4 | Screen reader or menu narration | later | fuller accessibility (narration, colour-vision, mono), with the shell before strangers play |
| V10 | 4 | A credits screen naming everyone | later | optional presentation and the ending, before release |
| A01.14 | 5 | Progress information during lengthy initial preparation | needed | a sign of life at once, and progress while shaders compile on first launch (or a shipped shader cache) |
| A02.19 | 5 | Loading or busy feedback after an accepted selection | needed | menus that work with mouse and keys, always a way back, confirm before destructive steps |
| A05.10 | 5 | A usable view in cramped interiors | needed | a usable view inside Mickey's office |
| A05.11 | 5 | A usable view while ascending and descending stairs | later | stairs to the flat, recentering, crouch framing: when the Hook has them |
| A21.02 | 5 | Plausible connections between adjacent spaces | needed | Mickey's office entered (list item 11), agreeing with its front, with room for Tom and the camera, closed doors reading closed |
| A21.03 | 5 | Exteriors and interiors that broadly agree in position and size | needed | Mickey's office entered (list item 11), agreeing with its front, with room for Tom and the camera, closed doors reading closed |
| A21.04 | 5 | Clear distinction between reachable scenery and background scenery | needed | Mickey's office entered (list item 11), agreeing with its front, with room for Tom and the camera, closed doors reading closed |
| A21.08 | 5 | Consistent visual language for climbable, breakable and inaccessible objects | later | the Hook's more buildings and the town's variety |
| A21.09 | 5 | Boundaries communicated by believable obstacles or explicit rules | done | the street's ends walled, checked in the editor game on 29 Sep by the tester's fix |
| A21.10 | 5 | A usable response to leaving the intended play area | done | as A21.09: walking off the play area meets a wall |
| A21.11 | 5 | Space for the character and camera along intended routes | needed | Mickey's office entered (list item 11), agreeing with its front, with room for Tom and the camera, closed doors reading closed |
| A21.12 | 5 | Alternative routes where exploration is presented as open-ended | later | the Hook's more buildings and the town's variety |
| A21.13 | 5 | Useful destinations rather than scenery alone | needed | places worth going to, near enough to walk, always a way back |
| A21.14 | 5 | Travel distances appropriate to available movement options | needed | places worth going to, near enough to walk, always a way back |
| A21.15 | 5 | A way back from ordinary exploratory detours | needed | places worth going to, near enough to walk, always a way back |
| A21.16 | 5 | Consistency between visible danger and actual traversal rules | later | the Hook's more buildings and the town's variety |
| A21.17 | 5 | Clear access rules for closed buildings or locked regions | needed | Mickey's office entered (list item 11), agreeing with its front, with room for Tom and the camera, closed doors reading closed |
| A21.18 | 5 | Indoor layouts that permit both navigation and intended encounters | needed | Mickey's office entered (list item 11), agreeing with its front, with room for Tom and the camera, closed doors reading closed |
| A39.26 | 5 | Loading screens that provide progress or signs of life | needed | no death loop, a failed save keeps the last, a full disk said plainly, settings per machine, a loading screen, control only when ready, back to the title on a failed load |
| A48.04 | 5 | World loading that keeps up with supported travel speeds | later | streaming: the Hook is one small level |
| A48.05 | 5 | Terrain and collision loaded before the player reaches them | later | streaming: the Hook is one small level |
| A48.10 | 5 | Loading that does not indefinitely freeze without explanation | later | streaming: the Hook is one small level |
| J9 | 5 | Interiors that can be entered | needed | Mickey's office entered (list item 11), agreeing with its front, with room for Tom and the camera, closed doors reading closed |
| U5 | 5 | Playtesting with people outside the team | needed | the AI tester on every friends' build; the friends' session itself (the runbook is the town's) |
| A05.17 | 6 | Aiming that follows the intended sightline | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A09.17 | 6 | Reactions to impacts that fit their direction | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A09.19 | 6 | Recovery from knockdown that connects to the final fallen position | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A09.20 | 6 | Death motion or ragdoll behaviour consistent with the hit | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A16.01 | 6 | Following at a useful distance | out | G2: Crew act on orders; they do not trail behind Tom |
| A16.02 | 6 | Keeping up without repeatedly falling far behind | out | G2: Following-companion item; crew do not follow Tom |
| A16.03 | 6 | Slowing down or waiting appropriately during guided travel | out | G2: No guided travel with a follower |
| A16.04 | 6 | Yielding when blocking a doorway or corridor | later | G2: crew on orders, with the crime layer (stage 6) |
| A16.05 | 6 | Navigating the same ordinary obstacles as the player | out | G2: Following-companion item; crew move like townspeople, not in Tom's wake |
| A16.06 | 6 | Sensible recovery when separated | out | G2: Following-companion item; crew are sent on errands, not kept at heel |
| A16.07 | 6 | Entering and leaving vehicles appropriately | later | G2: crew on orders, with the crime layer (stage 6) |
| A16.08 | 6 | Participation in combat consistent with the companion's role | later | G2: crew on orders, with the crime layer (stage 6) |
| A16.09 | 6 | A clear response to friendly fire | later | G2: crew on orders, with the crime layer (stage 6) |
| A16.10 | 6 | Commands with acknowledgement and visible results | later | G2: crew on orders, with the crime layer (stage 6) |
| A16.11 | 6 | Dialogue that survives walking, stopping and temporary interruption | later | G2: crew on orders, with the crime layer (stage 6) |
| A16.12 | 6 | No repeated dialogue announcing an event that has already happened | later | G2: crew on orders, with the crime layer (stage 6) |
| A16.13 | 6 | Clear downed, dead or unavailable states | later | G2: crew on orders, with the crime layer (stage 6) |
| A16.14 | 6 | A companion's presence and equipment surviving save and load | later | G2: crew on orders, with the crime layer (stage 6) |
| A17.01 | 6 | A clear distinction between exploration and combat readiness | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A17.02 | 6 | Attacks that occur in response to the intended input | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A17.03 | 6 | Reach and hit detection that broadly match the visible action | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A17.04 | 6 | A visible or audible distinction between hitting and missing | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A17.06 | 6 | Reactions showing where damage came from | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A17.07 | 6 | Clear feedback for blocked, resisted or ineffective attacks | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A17.08 | 6 | Enemy attacks that can be read before they connect | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A17.09 | 6 | A comprehensible relationship between commitment and cancellation | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A17.10 | 6 | Reliable switching between available combat actions | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A17.11 | 6 | A readable resource cost where attacks consume stamina or energy | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A17.12 | 6 | Consistent interaction between attacks and scenery | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A17.13 | 6 | A clear end to the encounter | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A17.15 | 6 | Camera and effects that leave the important action visible | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A18.01 | 6 | Attack animations that fit the equipped weapon | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A18.02 | 6 | Contact timing that agrees with damage timing | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A18.03 | 6 | Plausible weapon reach | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A18.04 | 6 | Directional movement that does not slide the attacker implausibly into position | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A18.05 | 6 | Readable attack recovery | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A18.06 | 6 | Blocking that responds within the game's stated rules | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A18.07 | 6 | Clear distinction between blockable and unblockable attacks | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A18.08 | 6 | Dodge movement with understandable distance and vulnerability | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A18.09 | 6 | Parry timing with readable success and failure, if present | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A18.11 | 6 | Knockback or stagger appropriate to the attack | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A18.13 | 6 | Multiple attackers behaving in a way the camera and controls can handle | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A18.14 | 6 | Consistent handling of unarmed attacks versus weapons | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A19.01 | 6 | Aiming aligned with where the shot can actually travel | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A19.03 | 6 | Projectile or hit behaviour consistent with the weapon | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A19.04 | 6 | Recoil that is visible and reflected in subsequent aim | out | G3: Recoil affecting later shots is shooter machinery; firearms are rare events |
| A19.05 | 6 | Muzzle flash or another appropriate firing cue | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A19.06 | 6 | Firing sound appropriate to the weapon and distance | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A19.07 | 6 | Impacts at the actual hit location | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A19.08 | 6 | Different impact responses for flesh, wood, metal and stone | out | G3: Shooter polish; foley already covers what thrown objects sound like |
| A19.10 | 6 | Ammunition counts that agree with shots fired | out | G3: No ammunition management; firearms are rare events |
| A19.11 | 6 | Distinct empty-weapon feedback | out | G3: No ammunition management; firearms are rare events |
| A19.12 | 6 | Reloading with correct ammunition transfer | out | G3: No reloading system; not a shooter |
| A19.13 | 6 | Reload animation that matches the weapon | out | G3: No reloading system; not a shooter |
| A19.15 | 6 | Weapon switching without duplicated or missing weapons | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A19.16 | 6 | Equip and holster transitions that match the visible state | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A19.18 | 6 | Controller aiming assistance appropriate to the design | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A19.20 | 6 | A visible aiming or trajectory cue for throws where precision is expected | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A19.21 | 6 | Thrown objects leaving from a plausible position | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A19.23 | 6 | Damage feedback that distinguishes a hit from a kill | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A19.24 | 6 | Weapon behaviour near walls that does not visibly put the barrel through everything | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A20.01 | 6 | An understandable representation of remaining health | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A20.02 | 6 | Clear distinction between damage, healing and temporary protection | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A20.04 | 6 | Healing controls that give immediate acknowledgement | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A27.11 | 6 | Public transport that clearly communicates boarding and destination | out | G5: Buses are timetabled scenery; Tom does not board them, for now |
| A30.08 | 6 | Combat music starting and ending with the encounter | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A30.16 | 6 | Radio or other in-world music sounding attached to its source | later | acted delivery (his blind pick kept the game's own engine), music, radio |
| A33.21 | 6 | Activity variety appropriate to the game's promised scope | later | G7: jobs beyond night one's ask |
| A34.01 | 6 | Health or equivalent survival information readable when needed | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A34.07 | 6 | Damage direction or an equivalent way to locate unseen danger | later | G3 and D4: fists and scarce firearms come at stage 6; no fight in the friends' build |
| A37.01 | 6 | Clear prices before purchase | later | G10: buying, selling and fencing come with the town's economy (stage 6) |
| A37.02 | 6 | A visible current balance | later | G10: buying, selling and fencing come with the town's economy (stage 6) |
| A37.03 | 6 | Distinct buying and selling states | later | G10: buying, selling and fencing come with the town's economy (stage 6) |
| A37.04 | 6 | Preview of the actual transaction quantity and total | later | G10: buying, selling and fencing come with the town's economy (stage 6) |
| A37.05 | 6 | Insufficient-funds feedback that explains the shortfall | later | G10: buying, selling and fencing come with the town's economy (stage 6) |
| A37.06 | 6 | Transactions occurring once per confirmed purchase | later | G10: buying, selling and fencing come with the town's economy (stage 6) |
| A37.07 | 6 | Clear distinction between sale value and purchase price | later | G10: buying, selling and fencing come with the town's economy (stage 6) |
| A37.08 | 6 | Recovery from accidental sale where a buyback system is provided | later | G10: buying, selling and fencing come with the town's economy (stage 6) |
| A37.09 | 6 | Shop stock and availability behaving consistently | later | G10: buying, selling and fencing come with the town's economy (stage 6) |
| A37.16 | 6 | No unexplained loss of money or materials when an operation is cancelled | later | G10: buying, selling and fencing come with the town's economy (stage 6) |
| V4 | 6 | Brand and legal clearance | needed | no real brand or mark in view (the pillar box and kiosk marks made up, 29 Sep) |
| A01.08 | Ship-prep | Access to language selection before language-dependent instructions | later | installers and language selection come with the store (G12: English only) |
| A03.21 | Ship-prep | A usable response to controller disconnection | later | controller support and finer menu comfort: keyboard and mouse first |
| A26.01 | Ship-prep | A clear way to enter the intended vehicle and seat | out | G4: Tom does not drive until the region |
| A26.04 | Ship-prep | Driving controls that respond consistently | out | G4: Tom does not drive until the region |
| A26.06 | Ship-prep | Steering that remains manageable across speeds | out | G4: Player steering; Tom does not drive until the region |
| A26.07 | Ship-prep | Reverse controls that are clear and usable | out | G4: Player reversing; Tom does not drive until the region |
| A26.15 | Ship-prep | A usable driving camera and rearward view | out | G4: Driving camera; Tom does not drive until the region |
| A26.16 | Ship-prep | A way to leave the vehicle safely | out | G4: Player leaving a car; comes with driving in the region |
| A26.17 | Ship-prep | Exiting that avoids placing the player inside walls or traffic | out | G4: Player getting out of a car; comes with driving in the region |
| A27.07 | Ship-prep | Boats floating at a plausible height | later | G5: boats as timetabled scenery, with the basin |
| A27.08 | Ship-prep | Boat steering, acceleration and stopping appropriate to water travel | out | G5: Tom does not steer boats; they move on a timetable |
| A27.09 | Ship-prep | Boarding and leaving without falling through the vessel | out | G5: Tom does not ride boats, for now |
| A27.10 | Ship-prep | Movement that remains stable on a moving deck | out | G5: Tom does not ride boats, for now |
| A27.12 | Ship-prep | Carried equipment and companions surviving transport transitions | out | G5: Tom rides no transport, and there are no followers |
| A39.23 | Ship-prep | Cloud conflicts presented without silently destroying newer progress | later | the platform's machinery, with the store |
| A39.24 | Ship-prep | Progress transferring correctly between supported machines | later | the platform's machinery, with the store |
| A42.06 | Ship-prep | Independent subtitle and spoken-language settings where supported | later | rebinding, controller and finer audio settings: the friends' build is keyboard and mouse |
| A47.01 | Ship-prep | Interface text available in the selected supported language | out | G12: English only for now |
| A47.02 | Ship-prep | Subtitles and audio using the selected supported languages | out | G12: English only for now |
| A47.03 | Ship-prep | Correct characters rather than missing-glyph boxes | needed | no missing glyphs or placeholder keys; names and keys consistent; British dates and money |
| A47.04 | Ship-prep | Longer translated text fitting the interface | out | G12: No translations for now; text kept out of code for later |
| A47.05 | Ship-prep | Appropriate line breaks and reading direction | needed | no missing glyphs or placeholder keys; names and keys consistent; British dates and money |
| A47.06 | Ship-prep | Names and terminology used consistently across dialogue, maps and objectives | needed | no missing glyphs or placeholder keys; names and keys consistent; British dates and money |
| A47.07 | Ship-prep | Localised button and keyboard instructions that match the actual controls | needed | no missing glyphs or placeholder keys; names and keys consistent; British dates and money |
| A47.08 | Ship-prep | User-entered names preserving supported accents and characters | later | G12: only if players type names |
| A47.09 | Ship-prep | Sensible number, date and measurement formatting | needed | no missing glyphs or placeholder keys; names and keys consistent; British dates and money |
| A47.10 | Ship-prep | Legible translated versions of essential in-world writing | out | G12: No translations for now |
| A47.11 | Ship-prep | No exposed placeholder keys or internal labels | needed | no missing glyphs or placeholder keys; names and keys consistent; British dates and money |
| A47.12 | Ship-prep | Language changes that apply predictably and explain any restart requirement | out | G12: One language only for now |
| A48.17 | Ship-prep | A usable recovery route from a crash | needed | a crash leaves a log and a way to send it |
| A49.01 | Ship-prep | Correct association between the signed-in player and their saves | later | the platform's machinery, with the store |
| A49.02 | Ship-prep | A clear response when an account signs out | later | the platform's machinery, with the store |
| A49.03 | Ship-prep | Controller ownership changing safely with the active user | later | the platform's machinery, with the store |
| A49.04 | Ship-prep | Platform overlays opening and closing without breaking control | later | the platform's machinery, with the store |
| A49.05 | Ship-prep | Screenshots and capture shortcuts working normally | needed | screenshots work; what is collected (the session record, typed words) said plainly (town's words) |
| A49.06 | Ship-prep | Supported achievements or trophies unlocking at the intended time | later | the platform's machinery, with the store |
| A49.07 | Ship-prep | Offline-earned progress synchronising appropriately when supported | later | the platform's machinery, with the store |
| A49.09 | Ship-prep | Missing content explained without silently damaging saves | later | the platform's machinery, with the store |
| A49.12 | Ship-prep | System sleep and resume behaving predictably | later | the platform's machinery, with the store |
| A51.01 | Ship-prep | A photo mode that pauses or clearly explains its live behaviour | later | optional presentation and the ending, before release |
| A51.02 | Ship-prep | Photo controls that do not accidentally trigger gameplay actions | later | optional presentation and the ending, before release |
| A51.04 | Ship-prep | Captures saved somewhere discoverable | later | optional presentation and the ending, before release |
| A51.05 | Ship-prep | A streamer-friendly music option where licensed music would obstruct sharing | later | optional presentation and the ending, before release |
| A51.06 | Ship-prep | Rewatchable tutorials, cinematics or records where the game provides an archive | later | optional presentation and the ending, before release |
| A51.08 | Ship-prep | Credits that can be paused, scrolled or exited | later | optional presentation and the ending, before release |
| A51.11 | Ship-prep | Clear rules for replay, chapter selection or New Game Plus where offered | later | optional presentation and the ending, before release |
| A51.12 | Ship-prep | A way to distinguish completed content from remaining content | later | optional presentation and the ending, before release |
| A4 | Ship-prep | Build version visible to the player | needed | the build's version on the title screen, so a friend's report names it |
| Q5 | Ship-prep | Minimum specification and the hardware floor | needed | a minimum specification to give friends before they install |
| R11 | Ship-prep | Accessibility information before purchase | later | fuller accessibility (narration, colour-vision, mono), with the shell before strangers play |
| S5 | Ship-prep | Content variation by locale | later | release work, past the friends' build |
| T1 | Ship-prep | A store page, a build and patching | needed | a packaged copy friends can download and update (the route, Steam playtest or a download, is his call when we get there) |
| T4 | Ship-prep | Age rating submission | later | release work, past the friends' build |
| T5 | Ship-prep | EULA and third-party licence attributions | needed | the third-party attributions shipped inside the build (CC BY, OFL where used) |
| T6 | Ship-prep | Anti-cheat or DRM decision | later | release work, past the friends' build |
| T7 | Ship-prep | Platform terminology and button naming | later | release work, past the friends' build |
| U3 | Ship-prep | A way for the player to report a problem | needed | a way to report a problem as well as bad output (the report key is wired) |
| U4 | Ship-prep | Patch notes and a post-launch plan | later | release work, past the friends' build |
| V5 | Ship-prep | Marketing capture: trailers and screenshots | later | release work, past the friends' build |
| A03.07 | Not staged | Simultaneous input where useful, such as controller movement with gyro aiming | out | research: no gyro: PC, keyboard and pad |
| A05.18 | Not staged | Shoulder switching where the aiming design requires it | out | research: D24: not a shooter, no cover system |
| A05.19 | Not staged | Lock-on that selects a plausible target, if present | out | research: D24: not a shooter, no lock-on |
| A05.20 | Not staged | Lock-on that releases sensibly when a target dies or disappears | out | research: D24: not a shooter, no lock-on |
| A07.20 | Not staged | Appropriate controls and release behaviour for ropes, ziplines or grapples, if included | out | G1: No ropes, ziplines or grapples; no parkour |
| A08.17 | Not staged | Consistent first-person hands, body and third-person appearance where both views exist | out | research: third person only; no first-person view is planned |
| A17.05 | Not staged | A distinction between damaging armour, a shield and an exposed target | out | G3: No armour or shields in 1990; not that kind of combat |
| A18.10 | Not staged | Combos that accept inputs predictably, if present | out | G3: No combo system; brawling, not a fighting game |
| A18.12 | Not staged | Finishing moves that cope with nearby walls and furniture | out | research: D18: no cruelty as spectacle, so no finishers |
| A19.02 | Not staged | A solution to the camera seeing around cover while the muzzle remains blocked | out | G3: Not a shooter; no cover system |
| A19.09 | Not staged | Appropriate rate of fire | out | G3: Firearms are events, not a rate of fire |
| A19.14 | Not staged | Predictable handling of interrupted reloads | out | G3: Not a shooter; no reloading |
| A19.17 | Not staged | Clear distinctions between ammunition types or firing modes, if supported | out | G3: No ammunition types or firing modes |
| A19.19 | Not staged | Scope transitions that preserve orientation | out | G3: No scopes |
| A19.22 | Not staged | Explosion effects with understandable range and cover interaction | out | G3: No explosives as a player weapon |
| A23.11 | Not staged | A sensible solution for player visibility in mirrors where mirrors are usable | out | research: no usable mirrors planned; D24 spend rule |
| A26.18 | Not staged | Vehicle damage communicated visually or mechanically | out | G4: Not a driving game; Tom does not drive until the region |
| A26.19 | Not staged | Recovery from an overturned or irretrievably stuck vehicle | out | G4: Not a driving game; no stuck cars for Tom to recover |
| A27.01 | Not staged | Mounting and dismounting from plausible positions | out | research: no mounts in 1990 Britain |
| A27.02 | Not staged | Mount movement whose gait matches its speed | out | research: no mounts |
| A27.03 | Not staged | Mount turning and stopping that fit its body | out | research: no mounts |
| A27.04 | Not staged | Mount avoidance of ordinary obstacles | out | research: no mounts |
| A27.05 | Not staged | A usable way to call, locate or recover an owned mount | out | research: no mounts |
| A27.06 | Not staged | Clear mount health, stamina or distress where those affect play | out | research: no mounts |
| A34.08 | Not staged | Distinguishable friendly, hostile and neutral indicators where used | out | research: D33: the player sees their own position, never other minds; no faction markers |
| A35.10 | Not staged | A route or directional cue that follows reachable paths where supplied | out | G8: No minimap and no route guidance |
| A35.18 | Not staged | Fast-travel eligibility, cost and restrictions explained where fast travel exists | out | research: a small dense town: no fast travel planned |
| A35.19 | Not staged | Fast travel arriving at a safe, usable position | out | research: no fast travel planned |
| A35.20 | Not staged | Travel preserving relevant equipment, followers and mission state | out | research: no fast travel planned |
| A36.09 | Not staged | Comparison with currently equipped gear | out | research: no gear statistics to compare; objects carry history, not stats |
| A37.10 | Not staged | Crafting recipes showing ingredients and output | out | G10: Crafting is out |
| A37.11 | Not staged | Clear indication of which ingredients are missing | out | G10: Crafting is out |
| A37.12 | Not staged | Preview of upgrade effects before spending resources | out | G10: Crafting and upgrades are out |
| A37.13 | Not staged | Crafting consuming the stated ingredients and producing the stated result | out | G10: Crafting is out |
| A37.14 | Not staged | Safe handling of crafting while inventory capacity is limited | out | G10: Crafting is out |
| A37.15 | Not staged | Clear distinction between repair, upgrade and replacement | out | G10: No crafting or upgrade system |
| A38.08 | Not staged | Customisation previews before commitment | out | research: a fixed protagonist, Tom Novak: no character creation |
| A38.09 | Not staged | Character creation that can be inspected under useful lighting | out | research: no character creation |
| A38.10 | Not staged | Appearance choices that remain recognisable in gameplay | out | research: no character creation |
| A38.13 | Not staged | A clear distinction between cosmetic and mechanical choices | out | research: no character creation |
| A41.12 | Not staged | HDR configuration where HDR is supported | out | research: no HDR target named; PC first, smallest budget |
| A42.18 | Not staged | Aim-assistance configuration where assistance is provided | out | research: D24: not a shooter, no aim assistance to configure |
| A42.20 | Not staged | Separate contextual bindings where driving or other modes require them | out | research: driving takes the smallest budget; no separate driving bindings planned |
| A43.08 | Not staged | Scalable or configurable aiming reticles | out | research: D24: not a shooter, no reticle |
| A44.11 | Not staged | Separate voice-chat and game-audio control in multiplayer | out | research: single player: no voice chat |
| A45.06 | Not staged | Quick-time events that can be simplified or bypassed where appropriate | out | research: no quick-time events planned |
| A45.12 | Not staged | No mandatory motion gesture without a button alternative where practical | out | research: PC first: no motion controls |
| A49.08 | Not staged | Owned downloadable content correctly recognised | out | research: no downloadable content planned |
| A49.13 | Not staged | Handheld or small-display interfaces remaining usable where the platform is supported | out | research: PC first: no handheld or small-display target |
| A50.01 | Not staged | A clear way to host, join or find a session | out | G0: Multiplayer stays out; single player |
| A50.02 | Not staged | Clear distinction between private, friends-only and public sessions | out | G0: Multiplayer stays out; single player |
| A50.03 | Not staged | Invitations that reach the correct session | out | G0: Multiplayer stays out; single player |
| A50.04 | Not staged | Useful explanation when joining fails | out | G0: Multiplayer stays out; single player |
| A50.05 | Not staged | Connection progress with a way to cancel | out | G0: Multiplayer stays out; single player |
| A50.06 | Not staged | Region or connection-quality information where latency matters | out | G0: Multiplayer stays out; single player |
| A50.07 | Not staged | Other players' movement represented smoothly enough to interpret | out | G0: Multiplayer stays out; single player |
| A50.08 | Not staged | Hits and interactions resolving consistently enough to feel fair | out | G0: Multiplayer stays out; single player |
| A50.09 | Not staged | Clear ownership of mission progress and rewards | out | G0: Multiplayer stays out; single player |
| A50.10 | Not staged | Clear rules for shared versus individual loot | out | G0: Multiplayer stays out; single player |
| A50.11 | Not staged | Safe handling of players joining or leaving mid-activity | out | G0: Multiplayer stays out; single player |
| A50.12 | Not staged | Recovery or clear consequences when the host disconnects | out | G0: Multiplayer stays out; single player |
| A50.13 | Not staged | Rejoining without unnecessary loss of progress where supported | out | G0: Multiplayer stays out; single player |
| A50.14 | Not staged | Clear downed, dead and spectating states | out | G0: Multiplayer stays out; single player |
| A50.15 | Not staged | A usable revive or respawn flow where the mode includes one | out | G0: Multiplayer stays out; single player |
| A50.16 | Not staged | Communication through voice, text or pings as appropriate | out | G0: Multiplayer stays out; single player |
| A50.17 | Not staged | Voice input and output selection | out | G0: Multiplayer stays out; single player |
| A50.18 | Not staged | Visible microphone state and a reliable mute control | out | G0: Multiplayer stays out; single player |
| A50.19 | Not staged | Individual mute, block and report controls | out | G0: Multiplayer stays out; single player |
| A50.20 | Not staged | Clear communication of friendly-fire rules | out | G0: Multiplayer stays out; single player |
| A50.21 | Not staged | Understandable handling of version or content mismatches | out | G0: Multiplayer stays out; single player |
| A50.22 | Not staged | Clear warning that menus do not pause a live session | out | G0: Multiplayer stays out; single player |
| A50.23 | Not staged | Protection against common forms of cheating or session disruption appropriate to the mode | out | G0: Multiplayer stays out; single player |
| A50.24 | Not staged | Supported cross-play and cross-progression behaving as advertised | out | G0: Multiplayer stays out; single player |
| A50.25 | Not staged | A clear end-of-session flow that preserves earned progress | out | G0: Multiplayer stays out; single player |

Left to the town's sweeps: A13.12, A13.13, A13.22, A13.23, A31.06, A31.07, A31.12, A31.13, A31.14, A48.18, L01, R01 to R03, AI01 to AI08, V7 and O6.
