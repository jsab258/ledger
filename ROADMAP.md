# LEDGER: the six stages

The route to the game, ruled by Jafar on 2026-09-14. Six stages, in his words,
with what each one means and how it is judged.

BROUGHT BACK TO THE ROOT 2026-09-22. This was `production/stages.md` and it
went into the archive when the studio was paused, which was wrong: it is the
GAME'S ROADMAP, not studio machinery. What travelled with the studio and stays
there is the process around it — the queue, the rungs of the ladder, the
phase-gate bookkeeping, the dashboard tiles and the throughput log. None of
that is here. The stages are.

`canon.md` outranks this file. `DECISIONS.md` says what is already decided;
where a decision and a stage disagree, the decision wins and this file is
wrong. A stage is a SCHEDULE, not a reduction of the pillars: everything the
pillars promise is still promised, and the stages only say in what order it
arrives.

## The order from 23 September, ruled by Jafar

A change of plan, made explicitly: TARGETS IN ORDER, instead of chasing the
Hook sheet to the end. The stages below still say what each part of the game
means; this says what the sittings work on next, and when each target stops.

1. **PRESENTABLE.** Not PS5, just not ugly. It STOPS when the checklist below
   is met, and nothing finer is done toward it. The pair is worked toward the
   checklist and no further. The three things set aside on 23 September - the
   painted asphalt, the pavement's wet shine, the crowded hillside - are tried
   again, each with a new idea, ONLY if they stand between the frame and the
   checklist.
2. **ONE SHORT PS5 EXPERIMENT, one sitting at most, then back to the list.**
   Say plainly which of Unreal's big features the street uses and which are
   off (light that bounces and reflects, very detailed geometry, the
   post-processing, anything else a modern game relies on). Take one small
   corner - a shopfront and the pavement in front of it - and make it as good
   as the tools we have allow: every engine feature on, the best free scanned
   materials, detailed geometry, one MetaHuman standing in it. Render it
   beside a PS5-era reference frame from game-design/reference/, measure what
   it costs the card with the voice's share taken into account, and tell
   Jafar in FOR-JAFAR.md: how close the corner gets, what stood between it and
   PS5, which gaps are skill, which content and which the card, and what it
   would take to bring the whole street to that corner's level.
3. **A SLICE YOU CAN PLAY, ten to fifteen minutes in the game**: walk the
   street, talk to two or three people who answer in their own cast voices,
   commit the crime, get seen, and later hear about it from someone who did
   not see it. The first thing Jafar will test himself. Decision 7 lands here:
   (a) make faint knowledge show - a hearer who knows even a little looks at
   Tom longer, remarks on it, treats him differently - and fix the routines so
   friends actually meet (55 of 80 friendships never do, which is a fault in
   the routines, not a dial). Then measure reach again. Neither change touches
   a constant.
   ADDED THE SAME DAY, after the PS5 corner and before or as part of the
   slice: (i) a blind listening test of Chatterbox Nano against the voice
   engine we use now - ten lines, three cast voices, paired, Nano's
   paralinguistic tags where a line needs feeling, its speed on the processor
   alone and on the card with the game running, its watermark kept, the text
   model staying the paid online one (decision 4); (ii) the router made so a
   typed line can never pose as a system instruction, with that case and the
   other injection lines in its tests; and (iii), in the slice's definition of
   done, the frame time and graphics memory on this card while a character
   speaks, with everything running as a player would have it - the first
   honest reading of whether this machine runs the game as designed.
4. **AFTER THE SLICE, ALTERNATE**: one sitting of polish, one of moat, so
   neither falls behind.

ADDED 23 SEPTEMBER, 18:00, INSIDE THE SAME ORDER (presentable, then the PS5
corner, then the slice; checkpoint work only between visual items, never
ahead of them): (iv) heads that turn toward you and positional sound join
the presentable checklist, using what Unreal provides; (v) the slice is built
on Unreal's standard game framework - a player character with a body and
animation, AI people who walk on a navigation mesh and avoid you, the
engine's own sound, a simple interface - not grown out of the probe, which
stays the test harness; (vi) a simulation that runs the same at any frame
rate is part of the slice's definition of done; (vii) at a checkpoint, the
master feature checklist (production/research/feature-coverage/
MASTER-CHECKLIST.md, 957 items) is folded in below as each stage's checklist
at the level of specific items, and the standing list refills from it; its
blind spots are a floor, and what Jafar finds playing other games is added
with the way of looking that should have caught it. FOLDED THE SAME EVENING,
SORTED AS HE RULED (floor, ours, and the genre by G0 to G12 in DECISIONS.md):
"The checklist, per stage", at the end of this file.

ADDED 23 SEPTEMBER, EVENING, TO THE SLICE (item 3) AND ITS DEFINITION OF
DONE: TWO KINDS OF TESTING, WHICH NEED DIFFERENT TESTERS. (viii) REGRESSION,
which exists and stays - the Core's suites, the checks on every push, the
scripted runs in the packaged game such as the crime check - answers whether
what worked yesterday still works; when the slice exists it gains ONE
SCRIPTED RUN THROUGH THE SLICE'S WHOLE LOOP (walk the street, talk to
someone, commit the crime, be seen, hear about it later) in the packaged
build, checked automatically, so the loop cannot silently break. (ix)
EXPLORATORY, which does not exist yet: AN AI TESTER that plays the packaged
game on this PC as a person would, by looking at the screen and pressing
keys, never by calling into the code; it tries things, gets stuck, tries to
break things, and writes up bugs, dead ends, things that did not respond,
places it could not get out of and anything that looked wrong. BEFORE
ANYTHING IS BUILT FOR IT, what Unreal already provides for driving a
packaged game from outside and for automated play is found out and used.
It runs once at the end of every sitting that changed the slice, or when
Jafar asks; its findings go into FOR-JAFAR.md as a short list, worst first,
and every bug goes onto the checklist. WHAT IT CANNOT JUDGE: whether the
game is fun or the town feels alive. That is the Meridian Test, and it
needs people (production/playtest/RUNBOOK.md). The AI tester's job is that
when a person sits down, nothing broken wastes their time. THE SLICE IS NOT
DONE until the scripted run passes and the AI tester has played it once
with nothing serious left open.

### The presentable checklist - polish toward it stops when all five hold

- **Nothing in frame is a placeholder.** Cars and props are real-looking
  models rather than shapes, and no car is a recognisable real model.
- **The light is not flat, and the street is wet as the sheet is.**
- **People turn their head to look at you** when you move near them or talk
  to them.
- **Sound is positional**: a voice or a noise comes from where its source is
  and changes as you move.
- **A handful of people stand or walk in the street**, even if they only idle.

### What the Hook sheet is, and what it is not

The Hook sheet is the stage 1 target FOR A STILL FRAME. It is not the game's
quality bar. The aim stays D8: the visual quality of a high-end 2026 game in a
small place, JUDGED IN MOTION, not in one picture.

## Two rulings that bound every stage (Jafar, 23 September, night)

- **PLATFORM: PC only, Windows.** Consoles are a later, low-priority question.
- **PERFORMANCE: 60 frames a second at Jafar's monitor's resolution on this
  card (RX 6700), never below 30, with the voice running.** Every visual choice
  answers to it from now on, and the playable slice is measured against it as
  part of its definition of done, beside the frame time and graphics memory
  while a character speaks.

## The six stages

| stage | the milestone, his words | how it is judged |
|---|---|---|
| 1 | One street that looks right. | His eye, beside the in-house Hook sheet. When he cannot say which way the gap runs, the budget moves on. |
| 2 | One street that lives: residents on schedules, varied bodies, a face that moves and a voice, foley and an ambient bed. | His eye and ear, in a frame and a clip; conversation latency inside its budget. |
| 3 | One street that knows me: the crime loop visible in a place that looks right. THE MILESTONE TO PROTECT IF ANYTHING SLIPS. | A witnessed crime reaching a second and a third resident within one in-game week; the simulation holding its frame budget at the resident count; the Core tests passing; and arrest reachable from live play, its callers outside Core counted and printed rather than zero. |
| 4 | The player's shell: menus, save, settings, controls, the Ledger and the first hour. | His own UI and game-feel standard, and the Ledger reading back what the player has learned. |
| 5 | The block becomes the Hook: Mickey's interior, more buildings, more residents, a thirty-minute session worth repeating. | The four Meridian Test conditions read off one session and nothing else. |
| 6 | Then the town. | The hours-of-content reading; no detectable line repetition in a two-hour session; Meridian Test conditions 2 and 3 sampled. |

## Stage 1: one street that looks right

THE BAR IS THE IN-HOUSE HOOK SHEET, and it is a floor rather than a ceiling.
The test is one a person performs: a frame of the built street, from the
sheet's own viewpoint, stands beside the sheet, and when Jafar cannot say which
way the gap runs, the budget moves to stage 2. Not because the street is
finished — because the same bar then has to be met across a whole town, which
is the harder problem and the better place for the money. Raising the bar is
his decision when the town exists, and a floor is not licence to polish one
street past it while the town does not exist.

THE ORDER INSIDE THE STAGE, and it is deliberate: light and shadow first, then
surfaces, then wetness, then density of clutter, and geometry detail LAST. The
frame that ties them together, his words: one screenshot of the street at dusk,
wet, lamps lit, a figure in silhouette.

GRIME IS THE STRATEGY, not a finishing pass. Weather and wear are what make
this town the town, a surface carries its wear as a separable layer, and the
floor for how much is a number measured off the first authored facades rather
than invented.

His pace rule over the whole stage: "Do not wait for my verdict to move to the
next; my verdict adjusts, it does not gate."

WHAT MAY NOT HAPPEN HERE: geometry first; more unique buildings or animation
polish before the presentation order above is done; polishing past the floor
while the town does not exist.

## Stage 2: one street that lives

Residents on schedules, varied bodies, a face that moves and a voice, foley and
an ambient bed.

WHO THE RESIDENTS ARE is decided by authoring and never by memory. There are
tiers — fully authored, assembled from parts, a varied body with a routine —
and they describe how a person was MADE. Everyone perceives, remembers and
gossips, and NO PLAN MAY GIVE ANY RESIDENT NO MEMORY. Near-term counts measure
what a resident costs so the schedule can be planned; they are never a scope.
The target is a town of three to five hundred residents who all remember.

BODY LANGUAGE IS PART OF THE MOAT and belongs to this stage. Someone who
half-recognises you reads differently from someone who does not; someone lying
holds themselves differently; someone who has heard about you shows it before
they speak. The five-rung identification ladder is invisible today except in
dialogue, and body language is how a player reads it without being told.

NONE OF IT STARTS BEFORE THE VISUAL SLICE. Clothing is garment meshes on a
shared skeleton rather than a wardrobe system, and the animation route is open.

## Stage 3: one street that knows me

THE MOAT MADE VISIBLE, and the one stage that may not be traded away when
something else runs long. If stages 1 or 2 slip, they slip; this does not.

The crime loop already runs in the probe's street: a crime committed, a witness
who really saw it, a rumour that really travelled, a line overheard. Stage 3 is
that loop IN THE STAGE-1 STREET, at the bar, with the engine of consequence
underneath it — perception, memory, gossip, schedules and save on the shipping
engine, guarded by the test suite the C# original already carries.

THE ARREST CLAUSE IS PART OF THE GATE ON PURPOSE. "Arrest reachable from live
play" means the arrest outcome's callers outside Core are counted and printed,
not zero. It was added the day the terminal state of the consequence spine was
found to have no callers at all, which would have let the gate go green with
the end of the story unreachable.

A KNOWN PROBLEM, MEASURED AND UNRESOLVED: rumour reach is flat with population.
At 7, 50, 200, 300 and 500 residents, only 15 to 22 ever remember anything,
because a rumour arrives at confidence times tie strength times 0.8 and is
refused below 0.2, so with the authored tie weights ordinary talk dies at the
second transfer. The constants are untouched and what reach the moat requires
is Jafar's to decide.

## Stage 4: the player's shell

Menus, save, settings, controls, the Ledger and the first hour.

THE STANDARD IS HIS, in his own words: "it has to be EXCEPTIONALLY GOOD from a
game feel and UI/UX point of view. we don't ship low quality / AI slop here."
The Ledger feeds the information pillar directly, so it is moat work; the
menus, settings and controls are the shell the moat is read through, and a
shell that reads as generic reads as slop.

The Ledger is a notebook, not a corkboard. There is no minimap. Save's
machinery belongs to stage 3; its surface, the save menu, is here. The first
hour is what has to introduce the player's progression.

## Stage 5: the block becomes the Hook

Mickey's interior, more buildings, more residents, a thirty-minute session
worth repeating.

Mickey's is a minicab office and it is enterable here: the waiting room, the
counter and the speaking gap, with the drivers' room beyond it. Every interior
is a designed layout with chosen contents.

THIS IS WHERE THE MERIDIAN TEST IS FIRST READ, off that thirty-minute session.
It is not MET here; it is met at the end of the town. The budget arrives here
rather than staying on the street because the same bar across more of the block
is the harder problem.

## Stage 6: then the town

About a square kilometre; three to five hundred residents who all remember;
designed interiors in two bands; the venues where information moves; economy
and cash; factions; the writing at full length; radio, TV and the brand bible.

FISTS HANG HERE BESIDE IT: melee combat, improvised weapons, scarce firearms as
events, with combat resolving a blow from a call site outside Core, a feel
check, and a gunshot producing a measured town-wide perception event. Combat
comes before driving. LEDGER is not a shooter, so fighting gets the smallest
budget that keeps it from looking wrong, and it may not take budget from
perception, memory, gossip or consequence.

ONE TENSION, REPORTED AND UNRESOLVED: combat's three gaps — being outnumbered,
running away as a way out, and the police arriving mid-fight — were placed at
STAGE 3 by Jafar's own words, while fists sit here at stage 6. That is his to
settle.

## Past the sixth stage

Jafar gave six stages and this file invents no seventh. Two things sit beyond
them and keep their own gates: the region, with land, driving and traffic — and
LEDGER is not a driving game — and ship preparation, deferred until the quality
bar is met, exiting on the Meridian Test's four conditions.

## The checklist, per stage

FOLDED 23 SEPTEMBER from the master feature checklist
(production/research/feature-coverage/MASTER-CHECKLIST.md, 957 items) and the
baseline-features research, SORTED AS JAFAR RULED: floor, in by default where
the research placed it; ours, the moat, where the plan has it; genre, ruled
item by item by G0 to G12 in DECISIONS.md. An item that is out stays here,
marked out with what rules it out. `floor (my call)` marks the three areas his
sort did not name (object interaction, optional presentation, and making the
game), put in as floor and put to him in FOR-JAFAR. `research:` marks an item
the research itself ruled out, which he may overrule.

THE FOUR RULES (CLAUDE.md): the standing list refills only from the current
stage's checklist; an item leaves a stage only as done, moved with a reason or
out with a reason; done needs a frame, a test or a recording linked in its row;
a stage cannot be FINISHED while an item in it is open, which
`tools/stage-check.py` enforces on every push.

Ids are the research's: A<section>.<n> for the master list (the sections:
1 Launching and reaching the game; 2 Title screen and menu navigation; 3 Input fundamentals; 4 Onboarding and the first minute; 5 Camera behaviour; 6 Walking, running and turning; 7 Jumping, climbing and water traversal, where supported; 8 Character appearance; 9 Body animation and physical contact; 10 Looking, expressions and social presentation; 11 Object interaction; 12 Collision and object physics; 13 Ordinary civilian behaviour; 14 Enemy awareness and decision-making, where combat or stealth exists; 15 Stealth, trespass and law, where included; 16 Companions and friendly allies, where included; 17 Combat fundamentals; 18 Melee combat, where included; 19 Ranged weapons and thrown objects, where included; 20 Health, injury, death and retry; 21 World layout and navigation through space; 22 Environment art and object appearance; 23 Lighting and rendering; 24 Weather, water and environmental effects, where applicable; 25 Ambient life and world continuity; 26 Road vehicles and traffic, where included; 27 Other transport and mounts, where included; 28 Spatial sound; 29 Foley and event sound; 30 Voice, music and the final audio mix; 31 Dialogue and conversations; 32 Cutscenes and cinematic transitions; 33 Missions, objectives and activities; 34 HUD and moment-to-moment feedback; 35 Maps, journals and navigation aids, where provided; 36 Inventory, equipment and loot, where included; 37 Shops, economy and crafting, where included; 38 Progression, customisation and difficulty, where included; 39 Saving, loading and persistence; 40 Pausing, interruption and quitting; 41 Graphics and display settings; 42 Audio and control settings; 43 Accessibility: text and visual information; 44 Accessibility: hearing and speech; 45 Accessibility: motor control and interaction; 46 Accessibility: cognition, difficulty and comfort; 47 Localisation and text handling; 48 Performance and technical stability; 49 Platform integration and account handling; 50 Multiplayer and cooperative play, only if included; 51 Optional presentation and long-term conveniences; 52 From my own checklist, and not in the independent list),
letters with a number for its section 52, B<n> for the baseline research's,
J<n> for what Jafar adds himself.

### Stage 1: one street that looks right

Stage state: OPEN

| id | feature | kind | status | evidence or reason |
|---|---|---|---|---|
| A08.07 | Hair that behaves plausibly under the game's lighting | floor | open |  |
| A08.08 | Skin, fabric, leather and metal that look different | floor | open |  |
| A08.15 | Detail changes with distance that do not transform identity | floor | open |  |
| A09.01 | Idle breathing and small posture changes | floor | open |  |
| A09.02 | Idle variation rather than a conspicuous repeating loop | floor | open |  |
| A09.24 | No identical synchronised idle motion across a crowd | floor | done | six people, each started at its own phase of its loop (street-people.json), no two in step, 23 Sep: [frame](production/art/compare/hook-unreal-2026-09-23/pair-06-presentable.png) |
| A21.01 | Human-scale doors, stairs, furniture and streets | ours | open |  |
| A21.05 | Readable routes through ordinary environments | ours | open |  |
| A21.06 | Landmarks that help orientation | ours | open |  |
| A21.07 | Visually distinct areas rather than indistinguishable repeated streets | ours | open |  |
| A22.01 | Complete visible surfaces without holes or missing faces | floor | done | no holes or missing faces anywhere in the Hook view in Unreal, both terraces, roofs, road and kerbs, 24 Sep: [frame](production/art/compare/stage1-2026-09-24/hook-max.png) |
| A22.02 | Appropriate detail at normal viewing distance | floor | open |  |
| A22.03 | Textures that do not stretch conspicuously | floor | open |  |
| A22.04 | Texture scale consistent with real object size | floor | done | measured, not eyeballed, 24 Sep: the brick map carries 96 courses over its 7.2 m (75 mm, a British course) and reads about 7.5 px a course beside the 0.55 m fascia at 100 px a metre in the Hook view; the flags map carries six courses of 900 x 600 mm flags, four to a course, over its 3.6 m: [frame](production/art/compare/stage1-2026-09-24/hook-max.png) |
| A22.05 | Materials distinguishable as wood, metal, glass, cloth and stone | floor | open |  |
| A22.06 | Object edges that do not all look infinitely sharp | floor | open |  |
| A22.07 | Buildings and props visibly grounded rather than floating | floor | done | grounded, 23 Sep: [frame](production/art/compare/hook-unreal-2026-09-23/pair-06-presentable.png) |
| A22.08 | Believable joins between walls, floors, roofs and terrain | floor | open |  |
| A22.09 | No conspicuous flickering between overlapping surfaces | floor | open |  |
| A22.10 | Variation that disguises obvious repeated components | floor | open |  |
| A22.11 | Wear and dirt consistent with use and exposure | floor | open |  |
| A22.12 | Furnishing and clutter consistent with a place's function | floor | open |  |
| A22.13 | Signs and labels that are readable when they matter | floor | done | MICKEY'S, RITA'S, FISH MARKET read at the Hook view, 23 Sep: [frame](production/art/compare/hook-unreal-2026-09-23/pair-06-presentable.png) |
| A22.14 | Period and setting consistency in conspicuous objects | floor | open |  |
| A22.15 | Objects that remain recognisable across lighting conditions | floor | done | the car, the woman, the lamp post, the shopfronts and the signs all read by day and by night from the same camera, 24 Sep: [day](production/art/compare/stage1-2026-09-24/camA-day.png), [night](production/art/compare/stage1-2026-09-24/camA-night.png) |
| A22.16 | Detail changes with distance that do not cause conspicuous shape popping | floor | open |  |
| A22.17 | Interior dressing that survives viewing from both directions | floor | open |  |
| A23.01 | Lighting that establishes readable shapes and space | floor | open |  |
| A23.02 | Shadows connecting people and objects to their surroundings | floor | open |  |
| A23.03 | Shadows that broadly follow moving characters and lights | floor | open |  |
| A23.04 | No major light leaking through solid walls | floor | done | at night the lit shops light their own windows and nothing else; no glow through brick or at wall joins, 24 Sep: [night A](production/art/compare/stage1-2026-09-24/camA-night.png), [night B](production/art/compare/stage1-2026-09-24/camB-night.png) |
| A23.05 | Indoor light levels that differ plausibly from outdoors | floor | open |  |
| A23.06 | Exposure changes that do not blind the player during ordinary transitions | floor | open |  |
| A23.07 | Dark areas that remain playable under the intended rules | floor | open |  |
| A23.09 | Switchable lights whose appearance and illumination change together | floor | open |  |
| A23.10 | Reflections that broadly agree with the environment | floor | open |  |
| A23.12 | Glass that behaves consistently as transparent, reflective or obscured | floor | open |  |
| A23.13 | Stable image edges without distracting shimmer | floor | open |  |
| A23.14 | Motion rendering without severe ghost trails | floor | open |  |
| A23.15 | Consistent colour and brightness across gameplay and cutscenes | floor | open |  |
| A23.16 | Distant scenery integrated with sky and atmosphere | floor | open |  |
| A23.17 | Important targets remaining distinguishable amid visual effects | floor | open |  |
| A24.05 | Wet surfaces looking different from dry ones | floor | done | standing water in puddles and gutters, 23 Sep: [frame](production/art/compare/hook-unreal-2026-09-23/pair-06-presentable.png) |
| A41.14 | Film grain, chromatic aberration and similar presentation controls where used | floor | open |  |
| A48.07 | No large visible objects appearing suddenly at short range | floor | open |  |
| P3 | Post-processing chain | floor (my call) | open |  |
| V6 | Art direction and a style bible | floor (my call) | open |  |

### Stage 2: one street that lives

Stage state: OPEN

| id | feature | kind | status | evidence or reason |
|---|---|---|---|---|
| A05.01 | Free horizontal and vertical looking within the intended camera model | floor | open |  |
| A05.02 | A useful default viewing distance in third person | floor | open |  |
| A05.04 | Camera framing that keeps the controlled character readable | floor | open |  |
| A05.05 | Camera movement that does not lag so much that control feels detached | floor | open |  |
| A05.06 | Camera collision that prevents seeing through walls | floor | open |  |
| A05.07 | Camera recovery after an obstruction clears | floor | open |  |
| A05.08 | Smooth handling of poles, foliage and other small obstructions | floor | open |  |
| A05.09 | Character fading or another solution when the camera gets too close | floor | open |  |
| A05.13 | Camera behaviour that does not repeatedly fight manual input | floor | open |  |
| A05.14 | Predictable recentering, if provided | floor | open |  |
| A05.15 | Smooth transitions between exploration, aiming and conversation | floor | open |  |
| A05.16 | Appropriate framing when crouching or going prone | floor | open |  |
| A05.21 | Camera recovery after a cutscene without disorienting rotation | floor | open |  |
| A05.23 | Stable horizon and manageable camera motion | floor | open |  |
| A05.24 | A sensible relationship between camera direction and movement after a camera cut | floor | open |  |
| A06.01 | Walking, jogging and running appropriate to the control scheme | floor | open |  |
| A06.02 | A usable sprint where the game's travel distances imply one | floor | open |  |
| A06.03 | Acceleration that fits the character's apparent weight | floor | open |  |
| A06.04 | Deceleration that fits the intended responsiveness | floor | open |  |
| A06.05 | Turning that looks and feels connected to the feet | floor | open |  |
| A06.06 | Stationary turning without impossible foot rotation | floor | open |  |
| A06.07 | Backward movement with an appropriate gait | floor | open |  |
| A06.08 | Sideways movement with an appropriate gait | floor | open |  |
| A06.09 | Smooth transitions between movement speeds | floor | open |  |
| A06.10 | Consistent movement relative to the camera or facing convention | floor | open |  |
| A06.11 | Reliable movement over small kerbs and floor seams | floor | open |  |
| A06.12 | Reliable movement up and down ordinary stairs | floor | open |  |
| A06.13 | Sensible behaviour on slopes | floor | open |  |
| A06.14 | Clear limits on slopes too steep to climb | floor | open |  |
| A06.15 | No snagging on tiny decorative geometry | floor | open |  |
| A06.16 | Predictable sliding along a wall instead of becoming stuck | floor | open |  |
| A06.17 | A crouched collision shape that actually fits under lower obstacles | floor | open |  |
| A06.18 | Prevention of standing through a ceiling | floor | open |  |
| A06.19 | Movement that follows moving platforms | floor | open |  |
| A06.20 | Appropriate restrictions while carrying, aiming or injured | floor | open |  |
| A06.21 | Recovery from being wedged between objects | floor | open |  |
| A08.01 | A complete character model from ordinary viewing angles | floor | open |  |
| A08.02 | Consistent scale between characters and their surroundings | floor | open |  |
| A08.03 | Clothing that fits the body rather than visibly floating | floor | open |  |
| A08.04 | Believable hands and fingers | floor | open |  |
| A08.05 | Believable eyes, eyelids and gaze direction | floor | open |  |
| A08.06 | A mouth interior that survives ordinary close-ups | floor | open |  |
| A08.09 | Equipped clothing and gear reflected on the visible character | floor | open |  |
| A08.10 | Held items attached to the correct hand and orientation | floor | open |  |
| A08.11 | Holstered gear occupying a plausible place on the body | floor | open |  |
| A08.12 | No major body or clothing gaps during ordinary poses | floor | open |  |
| A08.13 | A character shadow that matches the visible body and equipment | floor | open |  |
| A08.14 | Consistent appearance across gameplay, menus and cutscenes | floor | open |  |
| A08.16 | Visible wetness, dirt or injury where the presentation promises it | floor | open |  |
| A09.03 | Feet that remain planted instead of sliding during stops | floor | open |  |
| A09.04 | Foot placement that follows stairs and uneven ground | floor | open |  |
| A09.05 | Knees and hips that accommodate different foot heights | floor | open |  |
| A09.06 | Stride length that matches travel speed | floor | open |  |
| A09.07 | Body lean during acceleration and turning | floor | open |  |
| A09.08 | Smooth transitions between idle, walking and running | floor | open |  |
| A09.09 | Upper-body actions that coexist with leg movement | floor | open |  |
| A09.10 | Head movement that is partly independent of the torso | floor | open |  |
| A09.11 | Hands that meet handles, rails and other contact points | floor | open |  |
| A09.12 | Finger poses that fit held objects | floor | open |  |
| A09.13 | Two-handed objects held by both hands | floor | open |  |
| A09.14 | Seated bodies that actually meet the chair | floor | open |  |
| A09.15 | Sit-down and stand-up transitions | floor | open |  |
| A09.16 | Animation appropriate to the character's current weapon or burden | floor | open |  |
| A09.18 | Interruptions that leave the body in a valid pose | floor | open |  |
| A09.21 | Bodies that rest on the ground rather than hover | floor | open |  |
| A09.22 | Hair, clothing and attachments that follow body movement | floor | open |  |
| A09.23 | No sudden default pose while an animation loads | floor | open |  |
| A10.01 | NPCs turning their eyes toward someone addressing them | floor | open |  |
| A10.02 | NPCs turning their head toward an approaching player when appropriate | floor | done | the engine's Look At on the head, within 5 m and in front; 6 of 6 heads found, 3 turned in the walk, 23 Sep: [frame](production/art/compare/heads-2026-09-23/elizabeth-before-after.png) |
| A10.03 | The torso turning when the player moves beyond a comfortable head angle | floor | open |  |
| A10.04 | Limits that prevent impossible head and neck rotation | floor | open |  |
| A10.05 | Gaze directed at the player's face rather than their feet or empty space | floor | done | aimed at the camera's eye, not the feet, 23 Sep: [frame](production/art/compare/heads-2026-09-23/elizabeth-before-after.png) |
| A10.06 | Eye contact that occasionally breaks | floor | open |  |
| A10.07 | Blinking rather than a permanent stare | floor | open |  |
| A10.08 | Facial expression that broadly fits the line being spoken | floor | open |  |
| A10.09 | Listener reactions while another person speaks | floor | open |  |
| A10.10 | Gestures that fit the conversation rather than random arm waving | floor | open |  |
| A10.11 | People orienting toward a shared point of interest | floor | open |  |
| A10.12 | Expression and posture changes when a conversation becomes hostile | floor | open |  |
| A10.13 | Reactions to excessive proximity | floor | open |  |
| A10.14 | A return to ordinary activity after the player leaves | floor | open |  |
| A11.08 | Feedback when an interaction succeeds | floor (my call) | open |  |
| A11.12 | Doors whose visible movement agrees with their blocking state | floor (my call) | open |  |
| A12.01 | Solid ground everywhere that appears walkable | floor | open |  |
| A12.02 | Solid walls where walls are visibly present | floor | done | the walk into the parade wall stops (collisionBlockedStatus=STOPPED, east_parade_bay0) every run: [walk verdict](production/d1-probe/ue-walk-verdict.txt), [frame](production/d1-probe/ue-walk_04_after_blocked.png) |
| A12.03 | Collision shapes that broadly match visible objects | floor | open |  |
| A12.04 | Doorways that admit a character who visibly fits | floor | open |  |
| A12.05 | Small loose objects that do not act like immovable roadblocks | floor | open |  |
| A12.06 | Heavy objects that do not behave like weightless toys | floor | open |  |
| A12.07 | Dropped objects falling under consistent gravity | floor | open |  |
| A12.08 | Objects settling instead of vibrating indefinitely | floor | open |  |
| A12.09 | No explosive physics response from mild contact | floor | open |  |
| A12.10 | Fast objects that do not pass through obvious barriers | floor | open |  |
| A12.11 | Characters not pushing through one another without explanation | floor | open | FOUND 23 Sep: the slice's player walked straight through Elizabeth (production/art/compare/slice-2026-09-23/player-walks-5f93abd7.png). PLAYER AND STANDING PEOPLE FIXED the same evening: under -LedgerSlice each person is solid and the scripted walk now slides round her, ending 29.5 cm aside (production/art/compare/slice-2026-09-23/player-steps-round-elizabeth-5d394e2b.png, production/d1-probe/ue-slicewalk-verdict.txt). Open until the walkers, which must also step round one another. |
| A12.12 | A workable solution to being blocked by a friendly character | floor | open |  |
| A12.13 | Moving machinery carrying or blocking objects consistently | floor | open |  |
| A12.14 | Appropriate friction on visibly different surfaces where it matters | floor | open |  |
| A12.15 | Physical reactions accompanied by matching sound | floor | open |  |
| A12.16 | Broken objects leaving plausible remnants if destruction exists | floor | open |  |
| A12.17 | Destruction that changes collision as well as appearance | floor | open |  |
| A12.18 | Stable interaction between bodies, props and uneven ground | floor | open |  |
| A13.01 | People walking somewhere or doing something | floor | open |  |
| A13.02 | Variation in pace, posture and activity | floor | open |  |
| A13.03 | People avoiding one another while moving | floor | open |  |
| A13.04 | People avoiding the player when there is room | floor | open |  |
| A13.05 | A response to bumping into someone | floor | open |  |
| A13.06 | A response to repeatedly blocking someone's route | floor | open |  |
| A13.07 | Navigation through doorways without permanent jams | floor | open |  |
| A13.08 | Use of stairs rather than walking through their geometry | floor | open |  |
| A13.09 | Plausible transitions into sitting, working or leaning | floor | open |  |
| A13.10 | Hands and props matching the activity being performed | floor | open |  |
| A13.12 | People taking turns rather than all speaking simultaneously | floor | open |  |
| A13.13 | Ambient speech that is not repeated every few seconds | floor | open |  |
| A13.22 | Consistency between a person's current behaviour and dialogue | floor | open |  |
| A13.23 | Appropriate response when spoken to during another activity | floor | open |  |
| A13.24 | Some continuity when briefly looking away and back | floor | open |  |
| A13.25 | No obvious appearance or disappearance directly in view | floor | open |  |
| A13.26 | A reasonable solution when an NPC's intended route becomes blocked | floor | open |  |
| A20.07 | Readable stamina or similar exhaustion feedback | floor | open |  |
| A23.08 | Visible lamps whose surroundings respond to their light | floor | open |  |
| A24.01 | Vegetation moving appropriately in wind | floor | open |  |
| A24.02 | Hanging fabric and similar objects responding to the environment | floor | open |  |
| A24.03 | Rain that does not visibly fall through ordinary roofs | floor | open |  |
| A24.04 | A change in rain sound when moving under cover | floor | open |  |
| A24.06 | Plausible transitions into and out of weather | floor | open |  |
| A24.07 | Character or NPC responses to conspicuous weather where the presentation warrants them | floor | open |  |
| A24.09 | Ripples or splashes when entering water | floor | open |  |
| A24.10 | Wakes from moving boats or swimmers | floor | open |  |
| A24.11 | Fire giving appropriate light, movement and sound | floor | open |  |
| A24.12 | Smoke and dust appearing to originate from their causes | floor | open |  |
| A24.13 | Surface-specific debris from impacts | floor | open |  |
| A24.15 | Footprints or tracks where a visibly impressionable surface invites them | floor | open |  |
| A24.16 | Effects ending when their source ends | floor | open |  |
| A24.17 | Effects staying attached to moving sources | floor | open |  |
| A24.18 | Weather and time changes that do not visibly reset at ordinary area boundaries | floor | open |  |
| A25.01 | Background activity beyond the player's immediate objective | floor | open |  |
| A25.02 | Ambient sound appropriate to the location | floor | open |  |
| A25.03 | Population density that fits the place and time | floor | open |  |
| A25.04 | People occupying different activities rather than all wandering | floor | open |  |
| A25.05 | A plausible distinction between open and closed businesses, if operating hours exist | floor | open |  |
| A25.06 | Continuity when leaving a small area and immediately returning | floor | open |  |
| A25.07 | Consistent handling of dropped objects and casualties | floor | open |  |
| A25.08 | Clear rules for replenishing loot or respawning enemies | floor | open |  |
| A25.09 | Events that do not visibly restart every time the player crosses a nearby boundary | floor | open |  |
| A25.10 | Day and night changes reflected in lighting and relevant activity, if time advances | floor | open |  |
| A25.12 | Safe handling of time skips with active missions or followers | floor | open |  |
| A25.13 | Ambient events that allow interruption and recovery | floor | open |  |
| A25.14 | Animals behaving like animals rather than stationary ornaments, where present | floor | open |  |
| A25.15 | Birds or small wildlife reacting to close movement or noise | floor | open |  |
| A25.16 | No immediate repopulation directly in front of the player after a disturbance | floor | open |  |
| A26.02 | Entry animation that fits the door and seat | genre G4 | open | in by G4 |
| A26.03 | Sensible entry when one side is obstructed | genre G4 | open | in by G4: unsure: the firm's drivers at tight kerbs; moved from ship-prep |
| A26.05 | Acceleration and braking appropriate to the vehicle | genre G4 | open | in by G4 |
| A26.08 | Wheels rotating at a plausible rate | genre G4 | open | in by G4 |
| A26.09 | Front wheels turning with steering where appropriate | genre G4 | open | in by G4 |
| A26.10 | Suspension responding to road irregularities | genre G4 | open | in by G4 |
| A26.11 | Tyre contact that broadly matches the ground | genre G4 | open | in by G4 |
| A26.12 | Engine sound responding to speed and load | genre G4 | open | in by G4 |
| A26.13 | Skid and collision sounds responding to the actual event | genre G4 | open | in by G4 |
| A26.14 | Brake lights, headlights and reversing lights where the vehicle has them | genre G4 | open | in by G4 |
| A26.20 | Traffic following plausible lanes and junction rules | genre G4 | open | in by G4 |
| A26.21 | Traffic responding to obstructions and collisions | genre G4 | open | in by G4 |
| A26.22 | Pedestrians responding to approaching vehicles | genre G4 | open | in by G4 |
| A26.23 | Passengers remaining correctly seated during movement | genre G4 | open | in by G4 |
| A26.24 | A vehicle remaining where it was left under the game's persistence rules | genre G4 | open | in by G4 |
| A28.01 | Sounds coming from the direction of their source | floor | done | the traffic bed heard from the north bend with the engine's spatialisation, 23 Sep: [recording](production/art/compare/sound-2026-09-23/walk-audio-0c836a44.wav), [levels](production/art/compare/sound-2026-09-23/walk-audio-0c836a44-levels.txt) |
| A28.02 | Sound direction changing correctly as the player turns | floor | done | the walk turns its view at 7 s and the bed swings from -0.06 to +0.40 in balance, 23 Sep: [recording](production/art/compare/sound-2026-09-23/walk-audio-0c836a44.wav), [levels](production/art/compare/sound-2026-09-23/walk-audio-0c836a44-levels.txt) |
| A28.03 | Moving sources carrying their sounds with them | floor | open |  |
| A28.04 | Distant sources sounding quieter than nearby sources | floor | open |  |
| A28.05 | Distant sources losing appropriate detail | floor | open |  |
| A28.06 | Walls and closed doors muffling relevant sounds | floor | open |  |
| A28.07 | Openings providing a plausible route for sound | floor | open |  |
| A28.08 | Room acoustics differing from open air | floor | open |  |
| A28.09 | Larger and smaller rooms sounding different where conspicuous | floor | open |  |
| A28.10 | Smooth acoustic transitions at room boundaries | floor | open |  |
| A28.11 | Large sources sounding spatially broad rather than like tiny points | floor | open |  |
| A28.12 | Above and below having useful audible distinction where supported | floor | open |  |
| A28.13 | A sensible listening position when the camera moves away from the character | floor | open |  |
| A28.14 | No distant conversation playing at intimate, full-volume closeness | floor | open |  |
| A28.15 | No obvious snapping between left and right as a source passes nearby | floor | open |  |
| A29.01 | Footsteps synchronised with foot contact | floor | open |  |
| A29.02 | Different footstep sounds on different surfaces | floor | open |  |
| A29.03 | Footstep cadence changing with movement speed | floor | open |  |
| A29.04 | Appropriate landing sound | floor | open |  |
| A29.05 | Clothing and equipment movement where audible | floor | open |  |
| A29.06 | Breathing or exertion appropriate to strenuous activity | floor | open |  |
| A29.07 | Doors sounding when they move and latch | floor | open |  |
| A29.08 | Pickups and item handling providing subtle confirmation | floor | open |  |
| A29.09 | Collision sounds appropriate to the materials involved | floor | open |  |
| A29.10 | Breakage sounds matching the object | floor | open |  |
| A29.11 | Weapon handling, firing and reloading sounds aligned with actions | floor | open |  |
| A29.12 | Damage and pain sounds fitting the affected character | floor | open |  |
| A29.13 | Machines sounding active only while operating | floor | open |  |
| A29.14 | Splash sounds matching water contact | floor | open |  |
| A29.15 | Variation that prevents repeated actions sounding mechanically identical | floor | open |  |
| A29.16 | No double-triggered sound for a single event | floor | open |  |
| A29.17 | No continued footsteps after the character stops | floor | open |  |
| A29.18 | Sound events occurring when the action happens rather than noticeably late | floor | open |  |
| A30.01 | Important speech intelligible over ambience and action | floor | open |  |
| A30.02 | Consistent dialogue loudness across speakers | floor | open |  |
| A30.04 | Speech fitting the speaker's emotional situation | floor | open |  |
| A30.05 | No clipping or harsh overload during loud events | floor | open |  |
| A30.06 | No audible clicks at the start or end of loops | floor | open |  |
| A30.10 | Appropriate silence and contrast rather than constant maximum intensity | floor | open |  |
| A30.12 | Important sounds remaining audible in a crowded mix | floor | open |  |
| A30.13 | No dialogue continuing from a dead or departed speaker without explanation | floor | open |  |
| A30.14 | Audio pausing, resuming and loading consistently with the game state | floor | open |  |
| A30.15 | Consistent presentation across headphones and supported speaker layouts | floor | open |  |
| A31.02 | Acknowledgement when the player initiates speech | floor | open |  |
| A31.03 | Conversational distance and facing that look plausible | floor | open |  |
| A31.04 | Mouth movement synchronised approximately with speech | floor | open |  |
| A31.06 | Dialogue choices that communicate the intended meaning | floor | open |  |
| A31.07 | A distinction between asking for information and making a consequential commitment | floor | open |  |
| A31.08 | Choice selection that does not accidentally confirm during menu navigation | floor | open |  |
| A31.09 | A predictable response to walking away | floor | open |  |
| A31.10 | A predictable response to combat interrupting speech | floor | open |  |
| A31.15 | Ambient and important dialogue prevented from talking over one another excessively | floor | open |  |
| A31.16 | Subtitles matching the actual spoken line | floor | open |  |
| A31.17 | Appropriate pauses and turn-taking | floor | open |  |
| A31.18 | No conspicuous silence while a character appears to be waiting for a missing line | floor | open |  |
| A32.02 | Camera placement that shows the intended action | genre G6 | open | in by G6 |
| A32.05 | Facial and body performance consistent with the dialogue | genre G6 | open | in by G6 |
| A44.05 | Captions for essential non-speech sounds | floor | open |  |
| A48.01 | A stable frame rate appropriate to the selected mode | floor | open |  |
| A48.02 | Even frame timing rather than frequent small freezes | floor | open |  |
| A48.03 | No major hitch at the first use of an ordinary effect or weapon | floor | open |  |
| A48.06 | Textures resolving before their absence becomes conspicuous | floor | open |  |
| A48.08 | Stable performance in the expected crowd and combat density | floor | open |  |
| A48.09 | Menus that remain responsive when the world is busy | floor | open |  |
| A48.11 | Long-session stability without steadily worsening performance | floor | open |  |
| A48.12 | Stable behaviour when changing graphics settings | floor | open |  |
| A48.13 | Stable behaviour when changing audio or input devices | floor | open |  |
| A48.14 | Correct recovery after task switching | floor | open |  |
| A48.15 | No simulation speed changes caused by frame-rate changes | floor | open |  |
| A48.18 | Error messages that explain the problem in player language | floor | open |  |
| A48.19 | No routine need to restart the game to restore basic controls or interactions | floor | open |  |
| A48.20 | Updates that preserve existing progress and settings where promised | floor | open |  |
| H9 | Animation budget at crowd scale | floor (my call) | open |  |
| N7 | Live spoken conversation with memory | floor (my call) | open |  |
| V1 | Voice casting and direction | floor (my call) | open |  |
| V2 | Motion capture and performance | floor (my call) | open |  |
| B01 | Music, ambience and effects lowering while dialogue plays | floor | open | from the baseline research |
| B02 | Wind and rain sound that follows the current weather | floor | open | from the baseline research |
| B03 | Camera follow smoothing rather than a rigidly locked view | floor | open | from the baseline research |
| B04 | People opening, using and closing doors on their routes | floor | open | from the baseline research |
| B05 | People queueing, waiting their turn and giving way to one another | floor | open | from the baseline research |
| B06 | Puddles that ripple in rain and splash underfoot | floor | open | from the baseline research |
| L01 | Local line-writing, judged blind: the best local writers that fit what the card has left write the same lines as the paid model, shown to Jafar without saying which is which | ours | open | queued, waiting on the slice's measurement of the card memory the game and the voice use, and on the voice's double-size export being fixed (Jafar 2026-09-23); until then line-writing is online by default, not by conclusion; production/research/local-models |

### Stage 3: one street that knows me

Stage state: OPEN

| id | feature | kind | status | evidence or reason |
|---|---|---|---|---|
| A05.12 | A usable view while climbing or hanging | floor | open |  |
| A07.01 | A responsive jump with readable height and distance | genre G1 | out | G1: unsure, my call: no jump; kerbs, low walls and fences are stepped and climbed |
| A07.02 | Predictable control while airborne | genre G1 | open | in by G1 |
| A07.03 | Forgiveness around ledge departure and landing inputs | genre G1 | open | in by G1 |
| A07.04 | A landing animation appropriate to the fall | genre G1 | open | in by G1 |
| A07.05 | Fall damage that follows understandable rules | genre G1 | open | in by G1 |
| A07.06 | A clear distinction between a safe drop and a dangerous fall | genre G1 | open | in by G1 |
| A07.07 | Consistent identification of vaultable obstacles | genre G1 | open | in by G1 |
| A07.08 | Vaulting that fits the obstacle's height and thickness | genre G1 | open | in by G1 |
| A07.09 | Mantling that puts hands and feet on the actual surface | genre G1 | open | in by G1 |
| A07.10 | Prevention of climbing into blocked space | genre G1 | open | in by G1 |
| A07.11 | A way to cancel or drop from a climb | genre G1 | open | in by G1 |
| A07.12 | Ladder entry from plausible positions | genre G1 | open | in by G1 |
| A07.13 | Ladder exit without falling or becoming stuck | genre G1 | open | in by G1 |
| A07.14 | Consistent behaviour at climbable and non-climbable lookalikes | genre G1 | open | in by G1 |
| A07.15 | Clear entry into swimming rather than walking underwater | genre G1 | open | in by G1 |
| A07.16 | A usable transition between swimming and the shore | genre G1 | open | in by G1 |
| A07.17 | Swim movement and animation that agree | genre G1 | open | in by G1 |
| A07.18 | Readable breath or drowning rules if diving is possible | genre G1 | out | G1: Swimming to a ladder only; no diving |
| A07.19 | Water camera and sound changes when submerged | genre G1 | open | in by G1: unsure: no diving, but a plunge on falling in may go under |
| A11.02 | A stable current interaction target | floor (my call) | open |  |
| A11.04 | Interaction range that matches apparent reach | floor (my call) | open |  |
| A11.05 | No interaction through an intervening solid wall | floor (my call) | open |  |
| A11.06 | Appropriate priority when talk, loot and open share a button | floor (my call) | open |  |
| A11.07 | A clear description of the action before committing | floor (my call) | open |  |
| A11.09 | Feedback explaining why an interaction is unavailable | floor (my call) | open |  |
| A11.10 | Progress indication for prolonged interactions | floor (my call) | open |  |
| A11.11 | Predictable cancellation of prolonged interactions | floor (my call) | open |  |
| A11.13 | Door handling that does not trap the player inside the door | floor (my call) | open |  |
| A11.14 | Sensible behaviour when a door's path is obstructed | floor (my call) | open |  |
| A11.15 | Locked doors that communicate their status | floor (my call) | open |  |
| A11.16 | Containers that visibly and mechanically change after opening | floor (my call) | open |  |
| A11.17 | Pickups that disappear or change state when taken | floor (my call) | open |  |
| A11.18 | A dropped object appearing in a sensible reachable place | floor (my call) | open |  |
| A11.19 | Readable inspection views for documents and small objects | floor (my call) | open |  |
| A11.20 | Return from inspection to the previous position and context | floor (my call) | open |  |
| A11.21 | Controls for switches, terminals and similar devices that produce a visible result | floor (my call) | open |  |
| A11.22 | Occupied objects that cannot be used by two characters simultaneously | floor (my call) | open |  |
| A11.23 | Clear distinction between harmless use and theft or aggression | floor (my call) | open |  |
| A11.24 | An interaction ending cleanly if its object is destroyed or removed | floor (my call) | open |  |
| A13.11 | Conversations with actual listeners | floor | open |  |
| A13.14 | Reactions to a nearby loud or unusual event | floor | open |  |
| A13.15 | Reactions to a visibly drawn weapon where the setting warrants it | floor | open |  |
| A13.16 | Different reactions to harmless proximity and actual violence | floor | open |  |
| A13.17 | Fleeing or taking cover from danger | floor | open |  |
| A13.18 | Escape routes that lead away from danger | floor | open |  |
| A13.19 | A response to an injured or dead person | floor | open |  |
| A13.20 | A way for panic to resolve once danger passes | floor | open |  |
| A13.21 | People who do not immediately resume cheerful chatter beside an ongoing emergency | floor | open |  |
| A14.01 | Enemies detecting the player through understandable senses | ours | open |  |
| A14.02 | Solid cover preventing direct sight where expected | ours | done | crime B is occluded from the witness by the wall and he files nothing: [crime verdict](production/d1-probe/ue-crime-verdict.txt) |
| A14.03 | A readable transition from unaware to suspicious to engaged | ours | open |  |
| A14.04 | Reactions to relevant sounds | ours | open |  |
| A14.05 | Investigation of a sound's location rather than magical knowledge of the player | ours | open |  |
| A14.06 | Search focused on the last plausible known position | ours | open |  |
| A14.07 | A distinction between seeing the player and being told about them | ours | done | the friend who did not see hears it retold at confidence 0.45, one hop, as a told story and not a sighting: [crime verdict](production/d1-probe/ue-crime-verdict.txt), [frame](production/d1-probe/ue-crime_05_overheard.png) |
| A14.08 | Communication of an alert through visible or audible behaviour | ours | open |  |
| A14.09 | Enemy movement that uses the actual available routes | ours | open |  |
| A14.10 | Replanning when doors, vehicles or other obstacles move | ours | open |  |
| A14.11 | Enemies able to negotiate ordinary stairs and doorways | ours | open |  |
| A14.12 | Combat positioning that avoids all enemies occupying one point | ours | open |  |
| A14.13 | Enemies using appropriate engagement distance | ours | open |  |
| A14.14 | Enemies not firing continuously into an obvious obstruction | ours | open |  |
| A14.15 | Appropriate retreat, advance or repositioning | ours | open |  |
| A14.16 | A response to being flanked | ours | open |  |
| A14.17 | A response to allies being injured or killed | ours | open |  |
| A14.18 | Believable limits on accuracy and reaction speed | ours | open |  |
| A14.19 | Clear reasons when an enemy cannot be damaged or interrupted | ours | open |  |
| A14.20 | A sensible end to searching or combat | ours | open |  |
| A14.21 | No immediate forgetting of a fight merely because the player steps around a corner | ours | open |  |
| A14.22 | No pursuit through impossible or inaccessible routes | ours | open |  |
| A14.23 | No permanent lock into combat after every threat is gone | ours | open |  |
| A15.01 | A clear indication of whether the player is concealed or exposed | ours | open |  |
| A15.02 | Consistent effects of posture on visibility and noise | ours | open |  |
| A15.03 | Consistent effects of lighting if darkness is a stealth mechanic | ours | open |  |
| A15.04 | Sound generation that matches movement and actions | ours | open |  |
| A15.05 | Readable boundaries for restricted areas | ours | open |  |
| A15.06 | A warning or understandable transition before punishment where appropriate | ours | open |  |
| A15.07 | Distinction between suspicious behaviour and an openly hostile act | ours | open |  |
| A15.08 | Witness reactions that depend on whether they could observe the event | ours | done | the witness files crime A and is blind to B behind the wall; the passer-by sees neither, in the shipping engine every run: [crime verdict](production/d1-probe/ue-crime-verdict.txt) |
| A15.09 | A visible or audible reporting process if reporting matters | ours | open |  |
| A15.10 | A chance to respond before an alert spreads, where promised by the design | ours | open |  |
| A15.11 | Law response proportionate to the apparent offence | ours | open |  |
| A15.12 | An understandable wanted or pursuit state | ours | open |  |
| A15.13 | Clear conditions for losing pursuit | ours | open |  |
| A15.14 | Searches that do not continuously know the hidden player's exact location | ours | open |  |
| A15.15 | Consistent treatment of disguises or changed appearance if supported | ours | open |  |
| A15.16 | Distinction between surrender, escape and renewed aggression | ours | open |  |
| A15.17 | Clear consequences of fines, arrest or confiscation | ours | open |  |
| A15.18 | A usable return to ordinary play after punishment or escape | ours | open |  |
| A15.19 | No punishment for an action the controls misleadingly presented as harmless | ours | open |  |
| J01 | A scripted run through the slice's whole loop - walk the street, talk to someone, commit the crime, be seen, hear about it later - in the packaged build, checked automatically on every push | jafar 23 Sep | open | part of the slice's definition of done (ROADMAP item viii) |
| J02 | An exploratory AI tester that plays the packaged game by looking at the screen and pressing keys, built on what Unreal already provides for driving a packaged game, run at the end of each sitting that changed the slice; findings to FOR-JAFAR worst first, bugs onto this checklist | jafar 23 Sep | open | part of the slice's definition of done (ROADMAP item ix); it cannot judge fun or life, which is the Meridian Test with people. SHAPE FROM THE RESEARCH (production/research/ai-tester/WHAT-UNREAL-PROVIDES.md): Gauntlet's RunUnreal launches, times out and collects log, crash and verdict; a computer-use agent looks and presses keys; the game gives a Development build in a fixed window, -abslog and Slate.ForceRawInputSimulation 1 |
| J03 | The AI tester has played the slice once with nothing serious left open | jafar 23 Sep | open | the slice's last condition (ROADMAP item ix) |
| A17.14 | Feedback for victory, escape or failure | genre G3 | open | in by G3 |
| A20.03 | Low-health warning without making the game unreadable | floor | open |  |
| A20.05 | Healing resource consumption that matches the action | floor | open |  |
| A20.06 | Clear status effects and their duration or removal conditions | floor | open |  |
| A20.08 | A clear death or defeat state | floor | open |  |
| A20.09 | Some indication of the cause of defeat | floor | open |  |
| A20.10 | A quick, understandable retry route | floor | open |  |
| A20.12 | Consistent reset of enemies, resources and objectives on retry | floor | open |  |
| A20.13 | No respawn inside an active unavoidable hazard | floor | open |  |
| A20.14 | Clear penalties for death, if any | floor | open |  |
| A20.15 | A way to recover from an unwinnable checkpoint or stuck state | floor | open |  |
| A24.08 | Water surfaces moving rather than appearing solid | floor | open |  |
| A24.14 | Temporary marks such as bullet holes or blood persisting long enough to connect cause and effect | floor | open |  |
| A25.11 | A wait or sleep mechanism where schedules make waiting necessary | floor | open |  |
| A30.03 | Distinct voices that help identify recurring characters | floor | open |  |
| A30.07 | Music transitions that do not cut abruptly without intention | floor | open |  |
| A30.09 | Exploration music that does not overwhelm ordinary interaction | floor | open |  |
| A30.11 | Avoidance of conspicuously short musical loops | floor | open |  |
| A31.01 | A clear way to start and leave a conversation | floor | open |  |
| A31.05 | Correct association between the speaking voice and visible character | floor | open |  |
| A31.12 | Conversation state that does not repeat completed introductions endlessly | floor | open |  |
| A31.13 | Dialogue that acknowledges relevant completed actions | floor | open |  |
| A31.14 | Dialogue that does not refer to absent or dead characters as visibly present | floor | open |  |
| A33.06 | Rewards actually delivered and explained | genre G7 | open | in by G7 |
| A33.11 | A solution when a required character is absent, dead or obstructed | genre G7 | open | in by G7 |
| A34.03 | Clear current weapon, tool or ability state | floor | open |  |
| A36.04 | Clear distinction between usable, equippable, valuable and quest items | genre G9 | open | in by G9 |
| A36.16 | A way to drop, store or otherwise manage unwanted items | genre G9 | open | in by G9 |
| A36.18 | Clear ownership or theft status where relevant | genre G9 | open | in by G9 |
| A38.02 | A readable current level or equivalent advancement state | genre G11 | open | in by G11: unsure: no levels; crew and access in the Ledger may be the equivalent |
| A38.07 | Visible acknowledgement of meaningful milestones | genre G11 | open | in by G11 |
| A38.14 | Explanation of irreversible choices or respec limits | genre G11 | open | in by G11 |
| A38.15 | Progression and unlocks surviving reload | genre G11 | open | in by G11 |
| A39.04 | Manual saving or an explicitly communicated alternative | floor | open |  |
| A39.10 | Player location restored to a usable position | floor | open |  |
| A39.11 | Inventory and equipment restored consistently | floor | open |  |
| A39.12 | Mission progress and completed choices restored consistently | floor | open |  |
| A39.13 | Relevant world changes restored consistently | floor | open |  |
| A39.14 | Relevant NPC states restored consistently | floor | open |  |
| A39.18 | Previous valid progress surviving an interrupted save | floor | open |  |
| A39.20 | Recovery options for a damaged save where possible | floor | open |  |
| A48.16 | No obvious corruption after repeated save and load | floor | open |  |
| A51.09 | Clear communication of the ending's effect on continued free play | floor (my call) | open |  |
| A51.10 | A usable post-completion state where continued exploration is offered | floor (my call) | open |  |
| K7 | Police and authority response | floor (my call) | open |  |
| V3 | Music composition and licensing | floor (my call) | open |  |
| V8 | QA: functional, compliance and localisation testing | floor (my call) | open |  |
| V9 | Build and release engineering | floor (my call) | open |  |

### Stage 4: the player's shell

Stage state: OPEN

| id | feature | kind | status | evidence or reason |
|---|---|---|---|---|
| A01.01 | A working launch from the installed shortcut or platform library | floor | open |  |
| A01.02 | A visible response while the application starts | floor | open |  |
| A01.03 | Startup that does not require unrelated windows or manual commands | floor | open |  |
| A01.04 | Clear identification of the game being launched | floor | open |  |
| A01.05 | A sensible initial display resolution | floor | open |  |
| A01.06 | Startup on the intended monitor | floor | open |  |
| A01.07 | Initial sound at a reasonable volume | floor | open |  |
| A01.09 | Access to subtitles before the opening dialogue | floor | open |  |
| A01.10 | Access to essential accessibility settings before gameplay | floor | open |  |
| A01.11 | A readable explanation of required account or permission requests | floor | open |  |
| A01.12 | Offline access to offline content where supported | floor | open |  |
| A01.13 | A usable response to unavailable online services | floor | open |  |
| A01.15 | An explanation when required content is still installing | floor | open |  |
| A01.16 | An actionable error when the game cannot start | floor | open |  |
| A01.17 | Remembered first-run choices | floor | open |  |
| A01.18 | Skippable repeated introductory logos where permitted | floor | open |  |
| A02.01 | A clear distinction between starting, continuing and loading | floor | open |  |
| A02.02 | "Continue" that selects the appropriate latest progress | floor | open |  |
| A02.03 | Protection against replacing an existing playthrough with "New Game" | floor | open |  |
| A02.04 | A visible selected menu item | floor | open |  |
| A02.05 | Menu navigation in a predictable order | floor | open |  |
| A02.06 | Consistent confirm and back controls | floor | open |  |
| A02.07 | A reliable way back from every screen | floor | open |  |
| A02.08 | Mouse support for visible buttons on PC | floor | open |  |
| A02.09 | Clickable areas that match their visible buttons | floor | open |  |
| A02.10 | Scroll-wheel support for scrolling lists | floor | open |  |
| A02.11 | Controller navigation that reaches every setting | floor | open |  |
| A02.12 | Selection that remains visible while a list scrolls | floor | open |  |
| A02.13 | Useful explanations for disabled options | floor | open |  |
| A02.14 | Confirmation before destructive actions | floor | open |  |
| A02.15 | Dialogues that capture input without activating buttons behind them | floor | open |  |
| A02.16 | Menus that remember position when returning from a detail screen | floor | open |  |
| A02.17 | Text entry that works with the current device | floor | open |  |
| A02.18 | An on-screen keyboard when physical typing is unavailable | floor | open |  |
| A02.20 | Protection against repeated clicks starting the same operation twice | floor | open |  |
| A03.01 | Movement and actions that respond promptly to input | floor | open |  |
| A03.02 | Camera movement that responds promptly | floor | open |  |
| A03.03 | Consistent controls across equivalent situations | floor | open |  |
| A03.04 | Correct button prompts for the connected device | floor | open |  |
| A03.05 | Prompts that update after rebinding | floor | open |  |
| A03.06 | Switching between supported mouse, keyboard and controller input | floor | open |  |
| A03.08 | No duplicate action from one physical button press | floor | open |  |
| A03.09 | Correct distinction between pressing, holding and releasing | floor | open |  |
| A03.10 | Clear feedback when an action requires holding | floor | open |  |
| A03.11 | Reasonable tolerance for slightly early action presses | floor | open |  |
| A03.12 | Predictable handling of conflicting simultaneous inputs | floor | open |  |
| A03.13 | Movement that stops when the movement input stops | floor | open |  |
| A03.14 | No stuck movement after opening a menu or changing focus | floor | open |  |
| A03.15 | No attack caused by the same click that dismisses a menu | floor | open |  |
| A03.16 | No unexpected action from an input held through a loading screen | floor | open |  |
| A03.17 | Analogue movement speed on supported sticks | floor | open |  |
| A03.18 | Equal intended movement speed in straight and diagonal directions | floor | open |  |
| A03.19 | Sensible controller dead zones | floor | open |  |
| A03.20 | Predictable mouse movement without unwanted acceleration | floor | open |  |
| A03.22 | Safe reconnection without restarting the game | floor | open |  |
| A03.23 | Input handling independent of frame rate | floor | open |  |
| A03.24 | Clear control ownership when several controllers are connected | floor | open |  |
| A04.01 | An unmistakable transition from watching to controlling | floor | open |  |
| A04.02 | A starting camera aimed at something useful | floor | open |  |
| A04.03 | A safe opportunity to test movement | floor | open |  |
| A04.04 | A safe opportunity to test the camera | floor | open |  |
| A04.05 | A clear initial purpose | floor | open |  |
| A04.06 | A discoverable first destination or activity | floor | open |  |
| A04.07 | Instructions shown when their actions become relevant | floor | open |  |
| A04.08 | Instructions using the player's actual bindings | floor | open |  |
| A04.09 | Time to read an instruction before it disappears | floor | open |  |
| A04.10 | Confirmation that a tutorial action succeeded | floor | open |  |
| A04.11 | A way to recover instructions dismissed accidentally | floor | open |  |
| A04.12 | Tutorials that cope with an action performed early | floor | open |  |
| A04.13 | Tutorials that stop repeating after understanding is demonstrated | floor | open |  |
| A04.14 | A way to revisit controls and basic rules | floor | open |  |
| A04.15 | A way to skip familiar instruction without breaking progression | floor | open |  |
| A04.16 | An opening that permits ordinary experimentation without trapping the player | floor | open |  |
| A05.03 | A useful default field of view | floor | open |  |
| A05.22 | Camera shake that does not hide essential information | floor | open |  |
| A11.01 | A clear way to distinguish usable objects from decoration | floor (my call) | open |  |
| A11.03 | Prompts attached to the intended object | floor (my call) | open |  |
| A20.11 | Checkpoints placed to avoid needless repetition | floor | open |  |
| A20.16 | Ability to adjust relevant difficulty or assistance without discarding the playthrough | floor | open |  |
| A31.11 | Important information recoverable after interruption | floor | open |  |
| A32.01 | A clear distinction between a cutscene and interactive control | genre G6 | open | in by G6 |
| A32.03 | Characters and props arriving in the correct positions | genre G6 | open | in by G6 |
| A32.04 | Player equipment and appearance carried into scenes where appropriate | genre G6 | open | in by G6 |
| A32.06 | A way to pause where the presentation permits it | genre G6 | open | in by G6 |
| A32.07 | A way to skip already-seen scenes | genre G6 | open | in by G6 |
| A32.08 | Protection against accidentally skipping an entire scene | genre G6 | open | in by G6 |
| A32.09 | Subtitles that survive cinematic framing and letterboxing | genre G6 | open | in by G6 |
| A32.10 | Gameplay resuming in a sensible position and facing | genre G6 | open | in by G6 |
| A32.11 | No damage or enemy activity during a scene that denies player control unless deliberately communicated | genre G6 | open | in by G6 |
| A32.12 | Correct state changes even when a scene is skipped | genre G6 | open | in by G6 |
| A32.13 | No prolonged loading hidden behind a frozen character or black screen without feedback | genre G6 | open | in by G6 |
| A33.01 | A clear current objective or understandable self-directed goal | genre G7 | open | in by G7 |
| A33.02 | A way to review the objective after forgetting it | genre G7 | open | in by G7 |
| A33.03 | Clear distinction between mandatory and optional tasks | genre G7 | open | in by G7 |
| A33.04 | Objective progress updating after relevant actions | genre G7 | open | in by G7 |
| A33.05 | Completion acknowledged rather than silently recorded | genre G7 | open | in by G7 |
| A33.07 | Failure conditions communicated before they matter where possible | genre G7 | open | in by G7 |
| A33.08 | A clear response to leaving an active mission area | genre G7 | open | in by G7: unsure: no mission boundaries, but walking off a job needs clear consequence |
| A33.09 | Tasks that survive doing valid steps in an unexpected order | genre G7 | open | in by G7 |
| A33.10 | Recognition of an item already owned when it is requested | genre G7 | open | in by G7 |
| A33.12 | Protection against permanently losing an indispensable quest item | genre G7 | open | in by G7 |
| A33.13 | Required interactions remaining usable despite ordinary world changes | genre G7 | open | in by G7 |
| A33.14 | A way to restart or recover a broken activity | genre G7 | open | in by G7 |
| A33.15 | Clear communication of time limits | genre G7 | open | in by G7 |
| A33.16 | Dialogue and markers agreeing on the destination | genre G7 | out | G7: No waypoint markers to agree with |
| A33.17 | Markers resolving to reachable interaction points | genre G7 | out | G7: No waypoint markers |
| A33.18 | Sensible handling of multiple simultaneous missions | genre G7 | open | in by G7 |
| A33.19 | Completed objectives not continuing to issue obsolete instructions | genre G7 | open | in by G7 |
| A33.20 | A reason to explore beyond the main route | genre G7 | open | in by G7 |
| A34.02 | Ammunition or resource information readable before an action fails | floor | open |  |
| A34.04 | Feedback when an action is on cooldown or otherwise unavailable | floor | open |  |
| A34.05 | Interaction prompts that do not obscure the object | floor | open |  |
| A34.06 | Aiming indicators visible against varied backgrounds | floor | open |  |
| A34.09 | Status-effect indicators that explain their meaning | floor | open |  |
| A34.10 | Notifications that remain long enough to read | floor | open |  |
| A34.11 | Notification handling that does not bury urgent information | floor | open |  |
| A34.12 | No overlapping subtitles, prompts and objective text | floor | open |  |
| A34.13 | Appropriate removal or reduction of HUD during noninteractive scenes | floor | open |  |
| A34.14 | A clear indication when the world continues running behind a menu | floor | open |  |
| A34.15 | UI values that match actual gameplay state | floor | open |  |
| A34.16 | A way to reduce unnecessary HUD elements where supported | floor | open |  |
| A35.01 | A map that opens promptly and returns cleanly to gameplay | genre G8 | open | in by G8 |
| A35.02 | A visible player position | genre G8 | open | in by G8: unsure: whether the paper map shows where Tom is |
| A35.03 | A clear indication of facing or travel direction | genre G8 | open | in by G8: unsure: whether the paper map shows which way Tom faces |
| A35.04 | Useful map scale and zoom | genre G8 | open | in by G8 |
| A35.05 | Panning with the current input device | genre G8 | open | in by G8 |
| A35.06 | Legible labels and distinguishable icons | genre G8 | open | in by G8 |
| A35.07 | A legend or explanation for unfamiliar symbols | genre G8 | open | in by G8 |
| A35.08 | Selection of overlapping icons | genre G8 | out | G8: A printed paper map has no selectable icons |
| A35.09 | A way to place and remove a personal waypoint | genre G8 | out | G8: No waypoints; a paper map, not a navigation screen |
| A35.11 | Recalculation after leaving a suggested route | genre G8 | out | G8: No GPS-style routing |
| A35.12 | Height or floor distinction where a flat marker would mislead | genre G8 | out | G8: No markers on the paper map to mislead |
| A35.13 | Clear distinction between discovered and undiscovered places | genre G8 | open | in by G8: unsure: the paper map is printed; places found may go in the Ledger |
| A35.14 | Clear distinction between completed and incomplete activities | genre G8 | open | in by G8 |
| A35.15 | Navigation aids that remain consistent with world signs and names | genre G8 | open | in by G8 |
| A35.16 | A journal that preserves useful task and story information | genre G8 | open | in by G8 |
| A35.17 | A way to review recently acquired notes or clues | genre G8 | open | in by G8 |
| A36.01 | A reliable record of what the player owns | genre G9 | open | in by G9 |
| A36.02 | Pickup feedback identifying what was acquired | genre G9 | open | in by G9 |
| A36.03 | Item names, quantities and useful descriptions | genre G9 | open | in by G9 |
| A36.05 | Sorting or filtering sufficient for the expected inventory size | genre G9 | open | in by G9 |
| A36.06 | Consistent stacking of identical items | genre G9 | open | in by G9 |
| A36.07 | Quantity selection for moving or discarding stacks | genre G9 | open | in by G9 |
| A36.08 | A clear equipped state | genre G9 | open | in by G9 |
| A36.10 | Equipment restrictions explained before selection | genre G9 | open | in by G9 |
| A36.11 | Immediate gameplay and visual effects from equipping | genre G9 | open | in by G9 |
| A36.12 | Quick access to frequently used items | genre G9 | open | in by G9 |
| A36.13 | Consistent consumption of single-use items | genre G9 | open | in by G9 |
| A36.14 | A clear capacity or weight rule if capacity is limited | genre G9 | open | in by G9 |
| A36.15 | Feedback when a pickup fails because the inventory is full | genre G9 | open | in by G9 |
| A36.17 | Protection against accidental destruction of valuable items | genre G9 | open | in by G9 |
| A36.19 | Containers retaining sensible contents after being opened | genre G9 | open | in by G9 |
| A36.20 | Inventory state surviving death and reload according to the stated rules | genre G9 | open | in by G9 |
| A36.21 | Menus remaining usable while quantities change | genre G9 | open | in by G9 |
| A38.01 | Clear feedback when experience or progression is earned | genre G11 | open | in by G11 |
| A38.03 | Explanation of what an upgrade actually changes | genre G11 | out | G11: No upgrades; Tom has no stats |
| A38.04 | Clear prerequisites and costs | genre G11 | out | G11: No skill trees with prerequisites or costs |
| A38.05 | Immediate application of purchased abilities | genre G11 | out | G11: No purchased abilities; Tom has no stats |
| A38.06 | Instruction for newly unlocked actions | genre G11 | open | in by G11 |
| A38.11 | Difficulty descriptions that say what changes | genre G11 | open | in by G11 |
| A38.12 | Appropriate acknowledgement when difficulty is changed | genre G11 | open | in by G11 |
| A39.01 | A clear explanation of when progress is saved | floor | open |  |
| A39.02 | Autosaving at sensible milestones | floor | open |  |
| A39.03 | A visible indication while a save is in progress | floor | open |  |
| A39.05 | Clear reasons when saving is temporarily unavailable | floor | open |  |
| A39.06 | A clear distinction between checkpoint, autosave and manual save | floor | open |  |
| A39.07 | Save entries identifiable by time, location or progress | floor | open |  |
| A39.08 | Confirmation before overwriting or deleting a save | floor | open |  |
| A39.09 | Separate playthroughs or profiles not silently overwriting each other | floor | open |  |
| A39.15 | Timers and temporary effects restored according to clear rules | floor | open |  |
| A39.16 | No duplicated rewards or consumed items after reloading | floor | open |  |
| A39.17 | No loading into an unavoidable death loop | floor | open |  |
| A39.19 | A useful message when storage is full or unwritable | floor | open |  |
| A39.21 | Clear compatibility handling after updates or missing downloadable content | floor | open |  |
| A39.22 | Offline saves retained when reconnecting | floor | open |  |
| A39.25 | Machine-specific graphics settings not making another machine unusable | floor | open |  |
| A39.27 | Control withheld until the loaded world is ready | floor | open |  |
| A39.28 | A sensible return to title or another save after load failure | floor | open |  |
| A40.01 | A pause command available during ordinary single-player play | floor | open |  |
| A40.02 | A clear distinction between menus that pause and menus that do not | floor | open |  |
| A40.03 | Simulation, animation and relevant sound pausing consistently | floor | open |  |
| A40.04 | Resuming without a queued accidental attack or movement | floor | open |  |
| A40.05 | Sensible behaviour when the application loses focus | floor | open |  |
| A40.06 | Safe recovery after system sleep or suspend | floor | open |  |
| A40.07 | A clear route back to the title menu | floor | open |  |
| A40.08 | A clear quit-to-desktop option on PC | floor | open |  |
| A40.09 | A warning when quitting would lose unsaved progress | floor | open |  |
| A40.10 | Quitting that waits for an active save or clearly explains why it cannot yet finish | floor | open |  |
| A40.11 | No indefinitely hanging process after closing the game | floor | open |  |
| A40.12 | No continued game audio after exit | floor | open |  |
| A40.13 | Settings and intended progress retained on the next launch | floor | open |  |
| A40.14 | A useful reminder of current objectives after a longer break | floor | open |  |
| A41.01 | Resolution selection appropriate to the display | floor | open |  |
| A41.02 | Windowed, borderless or fullscreen options appropriate to the platform | floor | open |  |
| A41.03 | Monitor selection on supported PC setups | floor | open |  |
| A41.04 | Refresh-rate handling that uses the chosen display correctly | floor | open |  |
| A41.05 | A frame-rate limit option on PC | floor | open |  |
| A41.06 | Vertical synchronisation or an equivalent tearing control | floor | open |  |
| A41.07 | Quality presets with meaningful performance differences | floor | open |  |
| A41.08 | Individual control over major expensive visual features | floor | open |  |
| A41.09 | Texture quality appropriate to available graphics memory | floor | open |  |
| A41.10 | Field-of-view adjustment where the camera model permits it | floor | open |  |
| A41.11 | Brightness or gamma calibration with a useful reference | floor | open |  |
| A41.13 | Motion-blur control | floor | open |  |
| A41.15 | Upscaling and image-quality choices where supported | floor | open |  |
| A41.16 | Clear distinction between rendered frame rate and generated-frame options where offered | floor | open |  |
| A41.17 | UI scaling that remains usable at the chosen resolution | floor | open |  |
| A41.18 | Correct aspect-ratio handling without stretched people or clipped HUD | floor | open |  |
| A41.19 | Preview or explanation of what a graphics setting changes | floor | open |  |
| A41.20 | Confirmation with automatic reversal of an unusable display mode | floor | open |  |
| A41.21 | Clear indication when a setting requires restarting | floor | open |  |
| A41.22 | Settings that remain applied after restarting | floor | open |  |
| A42.01 | Separate master, dialogue, effects and music volume controls | floor | open |  |
| A42.02 | Volume changes audible while adjusting them | floor | open |  |
| A42.03 | Correct selection or following of the intended output device | floor | open |  |
| A42.04 | Speaker and headphone presentation choices where relevant | floor | open |  |
| A42.05 | A reduced dynamic-range option for quiet listening | floor | open |  |
| A42.07 | Full rebinding of ordinary gameplay actions | floor | open |  |
| A42.08 | Rebinding of menu actions where necessary for accessibility | floor | open |  |
| A42.09 | Warnings about conflicting bindings | floor | open |  |
| A42.10 | A way to restore default bindings | floor | open |  |
| A42.11 | Independent horizontal and vertical sensitivity where useful | floor | open |  |
| A42.12 | Separate aiming and general camera sensitivity | floor | open |  |
| A42.13 | Camera inversion options | floor | open |  |
| A42.14 | Adjustable controller dead zones | floor | open |  |
| A42.15 | Stick and trigger response options where supported | floor | open |  |
| A42.16 | Hold-versus-toggle choices for sustained actions | floor | open |  |
| A42.17 | Adjustable vibration and haptic intensity | floor | open |  |
| A42.19 | Controls explained without requiring memorisation of a diagram | floor | open |  |
| A43.01 | Readable default text at normal viewing distance | floor | open |  |
| A43.02 | Adjustable text size | floor | open |  |
| A43.03 | Text reflow without clipping after enlargement | floor | open |  |
| A43.04 | Adequate contrast between text and background | floor | open |  |
| A43.05 | Configurable text backgrounds or outlines where needed | floor | open |  |
| A43.06 | Important information conveyed through more than colour alone | floor | open |  |
| A43.07 | Distinguishable friendly, hostile and neutral markers for different colour-vision needs | floor | open |  |
| A43.09 | Optional emphasis for interactable objects where needed | floor | open |  |
| A43.10 | A way to distinguish important objects from visual clutter | floor | open |  |
| A43.11 | Menu narration or screen-reader support where offered | floor | open |  |
| A43.12 | Narration that announces selection, value and changes | floor | open |  |
| A43.13 | Narrated or otherwise accessible error and confirmation messages | floor | open |  |
| A43.14 | Accessible reading of essential documents and clues | floor | open |  |
| A43.15 | UI focus that remains visible and inside the active dialogue | floor | open |  |
| A43.16 | Gameplay information that remains legible after changing display size or resolution | floor | open |  |
| A44.01 | Subtitles available for essential dialogue | floor | open |  |
| A44.02 | Subtitles available before the opening scene | floor | open |  |
| A44.03 | Speaker identification when the speaker is not obvious | floor | open |  |
| A44.04 | Directional indication for important off-screen speech or sound where needed | floor | open |  |
| A44.06 | Sufficient subtitle display time | floor | open |  |
| A44.07 | Subtitle styling and size options | floor | open |  |
| A44.08 | Mono output without losing essential information | floor | open |  |
| A44.09 | Visual equivalents for gameplay-critical audio signals | floor | open |  |
| A44.10 | Alternatives to required speech input where voice commands exist | floor | open |  |
| A45.01 | Core actions remappable rather than only swapping entire preset layouts | floor | open |  |
| A45.02 | Alternatives to repeated rapid button presses | floor | open |  |
| A45.03 | Alternatives to prolonged button holds | floor | open |  |
| A45.04 | Alternatives to difficult simultaneous button combinations | floor | open |  |
| A45.05 | Adjustable timing windows for demanding interactions where offered | floor | open |  |
| A45.07 | Menu operation without precise pointer placement | floor | open |  |
| A45.08 | Adjustable cursor or menu-navigation speed | floor | open |  |
| A45.09 | Assistance for sustained steering, aiming or camera control where offered | floor | open |  |
| A45.10 | A way to pause without demanding the same dexterity as combat | floor | open |  |
| A45.11 | Support for compatible alternative controllers | floor | open |  |
| A46.01 | Plain explanations of goals and unfamiliar terms | floor | open |  |
| A46.02 | A way to review tutorials and recent information | floor | open |  |
| A46.03 | Adjustable or pausable reading time | floor | open |  |
| A46.04 | Clear indication of what changed after a menu action | floor | open |  |
| A46.05 | Assistance settings separated by challenge where practical | floor | open |  |
| A46.06 | Difficulty changes that do not require restarting the game | floor | open |  |
| A46.07 | Optional navigation assistance where the world is difficult to parse | floor | open |  |
| A46.08 | Reduced camera shake and head movement options | floor | open |  |
| A46.09 | Control over camera recentering where it causes discomfort | floor | open |  |
| A46.10 | Control over strong flashing and other avoidable visual triggers | floor | open |  |
| A46.11 | Reduced motion or animated-background options in menus | floor | open |  |
| A46.12 | Control over repetitive UI pulsing and notifications | floor | open |  |
| A46.13 | Clear content information where potentially distressing content is central | floor | open |  |
| A46.14 | Accessibility settings retained across sessions | floor | open |  |
| A49.10 | Required permissions requested at a relevant moment | floor | open |  |
| A49.11 | Optional data collection distinguishable from required operation | floor | open |  |
| A49.14 | Battery or power interruptions not corrupting the last completed save | floor | open |  |
| A51.03 | A way to hide the HUD for clean captures | floor (my call) | open |  |
| A51.07 | Credits accessible without having to finish the game | floor (my call) | open |  |
| A51.13 | Returning after a long break without having to reconstruct the entire playthrough from memory | floor (my call) | open |  |
| A1 | Splash and logo screens, legal notices | floor (my call) | open |  |
| A2 | First-run hardware detection and default quality preset | floor (my call) | open |  |
| D1 | Keyboard and mouse | floor (my call) | open |  |
| E4 | Look sensitivity and acceleration | floor (my call) | open |  |
| F2 | Objective or quest log | floor (my call) | open |  |
| F7 | Screen reader or menu narration | floor (my call) | open |  |
| O6 | Statistics and a session summary | floor (my call) | open |  |
| V10 | A credits screen naming everyone | floor (my call) | open |  |

### Stage 5: the block becomes the Hook

Stage state: OPEN

| id | feature | kind | status | evidence or reason |
|---|---|---|---|---|
| A01.14 | Progress information during lengthy initial preparation | floor | open |  |
| A02.19 | Loading or busy feedback after an accepted selection | floor | open |  |
| A05.10 | A usable view in cramped interiors | floor | open |  |
| A05.11 | A usable view while ascending and descending stairs | floor | open |  |
| A21.02 | Plausible connections between adjacent spaces | ours | open |  |
| A21.03 | Exteriors and interiors that broadly agree in position and size | ours | open |  |
| A21.04 | Clear distinction between reachable scenery and background scenery | ours | open |  |
| A21.08 | Consistent visual language for climbable, breakable and inaccessible objects | ours | open |  |
| A21.09 | Boundaries communicated by believable obstacles or explicit rules | ours | open |  |
| A21.10 | A usable response to leaving the intended play area | ours | open |  |
| A21.11 | Space for the character and camera along intended routes | ours | open |  |
| A21.12 | Alternative routes where exploration is presented as open-ended | ours | open |  |
| A21.13 | Useful destinations rather than scenery alone | ours | open |  |
| A21.14 | Travel distances appropriate to available movement options | ours | open |  |
| A21.15 | A way back from ordinary exploratory detours | ours | open |  |
| A21.16 | Consistency between visible danger and actual traversal rules | ours | open |  |
| A21.17 | Clear access rules for closed buildings or locked regions | ours | open |  |
| A21.18 | Indoor layouts that permit both navigation and intended encounters | ours | open |  |
| A39.26 | Loading screens that provide progress or signs of life | floor | open |  |
| A48.04 | World loading that keeps up with supported travel speeds | floor | open |  |
| A48.05 | Terrain and collision loaded before the player reaches them | floor | open |  |
| A48.10 | Loading that does not indefinitely freeze without explanation | floor | open |  |
| J9 | Interiors that can be entered | floor (my call) | open |  |
| U5 | Playtesting with people outside the team | floor (my call) | open |  |

### Stage 6: then the town

Stage state: OPEN

| id | feature | kind | status | evidence or reason |
|---|---|---|---|---|
| A05.17 | Aiming that follows the intended sightline | floor | open |  |
| A09.17 | Reactions to impacts that fit their direction | floor | open |  |
| A09.19 | Recovery from knockdown that connects to the final fallen position | floor | open |  |
| A09.20 | Death motion or ragdoll behaviour consistent with the hit | floor | open |  |
| A16.01 | Following at a useful distance | genre G2 | out | G2: Crew act on orders; they do not trail behind Tom |
| A16.02 | Keeping up without repeatedly falling far behind | genre G2 | out | G2: Following-companion item; crew do not follow Tom |
| A16.03 | Slowing down or waiting appropriately during guided travel | genre G2 | out | G2: No guided travel with a follower |
| A16.04 | Yielding when blocking a doorway or corridor | genre G2 | open | in by G2 |
| A16.05 | Navigating the same ordinary obstacles as the player | genre G2 | out | G2: Following-companion item; crew move like townspeople, not in Tom's wake |
| A16.06 | Sensible recovery when separated | genre G2 | out | G2: Following-companion item; crew are sent on errands, not kept at heel |
| A16.07 | Entering and leaving vehicles appropriately | genre G2 | open | in by G2: unsure: crew may drive the firm's cars on Tom's orders |
| A16.08 | Participation in combat consistent with the companion's role | genre G2 | open | in by G2 |
| A16.09 | A clear response to friendly fire | genre G2 | open | in by G2 |
| A16.10 | Commands with acknowledgement and visible results | genre G2 | open | in by G2 |
| A16.11 | Dialogue that survives walking, stopping and temporary interruption | genre G2 | open | in by G2 |
| A16.12 | No repeated dialogue announcing an event that has already happened | genre G2 | open | in by G2 |
| A16.13 | Clear downed, dead or unavailable states | genre G2 | open | in by G2 |
| A16.14 | A companion's presence and equipment surviving save and load | genre G2 | open | in by G2 |
| A17.01 | A clear distinction between exploration and combat readiness | genre G3 | open | in by G3 |
| A17.02 | Attacks that occur in response to the intended input | genre G3 | open | in by G3 |
| A17.03 | Reach and hit detection that broadly match the visible action | genre G3 | open | in by G3 |
| A17.04 | A visible or audible distinction between hitting and missing | genre G3 | open | in by G3 |
| A17.06 | Reactions showing where damage came from | genre G3 | open | in by G3 |
| A17.07 | Clear feedback for blocked, resisted or ineffective attacks | genre G3 | open | in by G3 |
| A17.08 | Enemy attacks that can be read before they connect | genre G3 | open | in by G3 |
| A17.09 | A comprehensible relationship between commitment and cancellation | genre G3 | open | in by G3 |
| A17.10 | Reliable switching between available combat actions | genre G3 | open | in by G3 |
| A17.11 | A readable resource cost where attacks consume stamina or energy | genre G3 | open | in by G3 |
| A17.12 | Consistent interaction between attacks and scenery | genre G3 | open | in by G3 |
| A17.13 | A clear end to the encounter | genre G3 | open | in by G3 |
| A17.15 | Camera and effects that leave the important action visible | genre G3 | open | in by G3 |
| A18.01 | Attack animations that fit the equipped weapon | genre G3 | open | in by G3 |
| A18.02 | Contact timing that agrees with damage timing | genre G3 | open | in by G3 |
| A18.03 | Plausible weapon reach | genre G3 | open | in by G3 |
| A18.04 | Directional movement that does not slide the attacker implausibly into position | genre G3 | open | in by G3 |
| A18.05 | Readable attack recovery | genre G3 | open | in by G3 |
| A18.06 | Blocking that responds within the game's stated rules | genre G3 | open | in by G3 |
| A18.07 | Clear distinction between blockable and unblockable attacks | genre G3 | open | in by G3 |
| A18.08 | Dodge movement with understandable distance and vulnerability | genre G3 | open | in by G3 |
| A18.09 | Parry timing with readable success and failure, if present | genre G3 | open | in by G3 |
| A18.11 | Knockback or stagger appropriate to the attack | genre G3 | open | in by G3 |
| A18.13 | Multiple attackers behaving in a way the camera and controls can handle | genre G3 | open | in by G3 |
| A18.14 | Consistent handling of unarmed attacks versus weapons | genre G3 | open | in by G3 |
| A19.01 | Aiming aligned with where the shot can actually travel | genre G3 | open | in by G3 |
| A19.03 | Projectile or hit behaviour consistent with the weapon | genre G3 | open | in by G3 |
| A19.04 | Recoil that is visible and reflected in subsequent aim | genre G3 | out | G3: Recoil affecting later shots is shooter machinery; firearms are rare events |
| A19.05 | Muzzle flash or another appropriate firing cue | genre G3 | open | in by G3 |
| A19.06 | Firing sound appropriate to the weapon and distance | genre G3 | open | in by G3 |
| A19.07 | Impacts at the actual hit location | genre G3 | open | in by G3 |
| A19.08 | Different impact responses for flesh, wood, metal and stone | genre G3 | out | G3: Shooter polish; foley already covers what thrown objects sound like |
| A19.10 | Ammunition counts that agree with shots fired | genre G3 | out | G3: No ammunition management; firearms are rare events |
| A19.11 | Distinct empty-weapon feedback | genre G3 | out | G3: No ammunition management; firearms are rare events |
| A19.12 | Reloading with correct ammunition transfer | genre G3 | out | G3: No reloading system; not a shooter |
| A19.13 | Reload animation that matches the weapon | genre G3 | out | G3: No reloading system; not a shooter |
| A19.15 | Weapon switching without duplicated or missing weapons | genre G3 | open | in by G3: unsure: swapping between fists, a pocketed item and an improvised weapon |
| A19.16 | Equip and holster transitions that match the visible state | genre G3 | open | in by G3 |
| A19.18 | Controller aiming assistance appropriate to the design | genre G3 | open | in by G3: unsure: a player-aimed firearm event on a pad may need assist |
| A19.20 | A visible aiming or trajectory cue for throws where precision is expected | genre G3 | open | in by G3 |
| A19.21 | Thrown objects leaving from a plausible position | genre G3 | open | in by G3 |
| A19.23 | Damage feedback that distinguishes a hit from a kill | genre G3 | open | in by G3 |
| A19.24 | Weapon behaviour near walls that does not visibly put the barrel through everything | genre G3 | open | in by G3 |
| A20.01 | An understandable representation of remaining health | floor | open |  |
| A20.02 | Clear distinction between damage, healing and temporary protection | floor | open |  |
| A20.04 | Healing controls that give immediate acknowledgement | floor | open |  |
| A27.11 | Public transport that clearly communicates boarding and destination | genre G5 | out | G5: Buses are timetabled scenery; Tom does not board them, for now |
| A30.08 | Combat music starting and ending with the encounter | floor | open |  |
| A30.16 | Radio or other in-world music sounding attached to its source | floor | open |  |
| A33.21 | Activity variety appropriate to the game's promised scope | genre G7 | open | in by G7 |
| A34.01 | Health or equivalent survival information readable when needed | floor | open |  |
| A34.07 | Damage direction or an equivalent way to locate unseen danger | floor | open |  |
| A37.01 | Clear prices before purchase | genre G10 | open | in by G10 |
| A37.02 | A visible current balance | genre G10 | open | in by G10 |
| A37.03 | Distinct buying and selling states | genre G10 | open | in by G10 |
| A37.04 | Preview of the actual transaction quantity and total | genre G10 | open | in by G10 |
| A37.05 | Insufficient-funds feedback that explains the shortfall | genre G10 | open | in by G10 |
| A37.06 | Transactions occurring once per confirmed purchase | genre G10 | open | in by G10 |
| A37.07 | Clear distinction between sale value and purchase price | genre G10 | open | in by G10 |
| A37.08 | Recovery from accidental sale where a buyback system is provided | genre G10 | open | in by G10 |
| A37.09 | Shop stock and availability behaving consistently | genre G10 | open | in by G10 |
| A37.16 | No unexplained loss of money or materials when an operation is cancelled | genre G10 | open | in by G10 |
| V4 | Brand and legal clearance | floor (my call) | open |  |
| V7 | Writing at volume, and editing it | floor (my call) | open |  |

### Ship-prep: past the sixth stage

Stage state: OPEN

| id | feature | kind | status | evidence or reason |
|---|---|---|---|---|
| A01.08 | Access to language selection before language-dependent instructions | floor | open |  |
| A03.21 | A usable response to controller disconnection | floor | open |  |
| A26.01 | A clear way to enter the intended vehicle and seat | genre G4 | out | G4: Tom does not drive until the region |
| A26.04 | Driving controls that respond consistently | genre G4 | out | G4: Tom does not drive until the region |
| A26.06 | Steering that remains manageable across speeds | genre G4 | out | G4: Player steering; Tom does not drive until the region |
| A26.07 | Reverse controls that are clear and usable | genre G4 | out | G4: Player reversing; Tom does not drive until the region |
| A26.15 | A usable driving camera and rearward view | genre G4 | out | G4: Driving camera; Tom does not drive until the region |
| A26.16 | A way to leave the vehicle safely | genre G4 | out | G4: Player leaving a car; comes with driving in the region |
| A26.17 | Exiting that avoids placing the player inside walls or traffic | genre G4 | out | G4: Player getting out of a car; comes with driving in the region |
| A27.07 | Boats floating at a plausible height | genre G5 | open | in by G5 |
| A27.08 | Boat steering, acceleration and stopping appropriate to water travel | genre G5 | out | G5: Tom does not steer boats; they move on a timetable |
| A27.09 | Boarding and leaving without falling through the vessel | genre G5 | out | G5: Tom does not ride boats, for now |
| A27.10 | Movement that remains stable on a moving deck | genre G5 | out | G5: Tom does not ride boats, for now |
| A27.12 | Carried equipment and companions surviving transport transitions | genre G5 | out | G5: Tom rides no transport, and there are no followers |
| A39.23 | Cloud conflicts presented without silently destroying newer progress | floor | open |  |
| A39.24 | Progress transferring correctly between supported machines | floor | open |  |
| A42.06 | Independent subtitle and spoken-language settings where supported | floor | open |  |
| A47.01 | Interface text available in the selected supported language | genre G12 | out | G12: English only for now |
| A47.02 | Subtitles and audio using the selected supported languages | genre G12 | out | G12: English only for now |
| A47.03 | Correct characters rather than missing-glyph boxes | genre G12 | open | in by G12 |
| A47.04 | Longer translated text fitting the interface | genre G12 | out | G12: No translations for now; text kept out of code for later |
| A47.05 | Appropriate line breaks and reading direction | genre G12 | open | in by G12 |
| A47.06 | Names and terminology used consistently across dialogue, maps and objectives | genre G12 | open | in by G12 |
| A47.07 | Localised button and keyboard instructions that match the actual controls | genre G12 | open | in by G12 |
| A47.08 | User-entered names preserving supported accents and characters | genre G12 | open | in by G12: unsure: only matters if players type names, such as for saves |
| A47.09 | Sensible number, date and measurement formatting | genre G12 | open | in by G12 |
| A47.10 | Legible translated versions of essential in-world writing | genre G12 | out | G12: No translations for now |
| A47.11 | No exposed placeholder keys or internal labels | genre G12 | open | in by G12 |
| A47.12 | Language changes that apply predictably and explain any restart requirement | genre G12 | out | G12: One language only for now |
| A48.17 | A usable recovery route from a crash | floor | open |  |
| A49.01 | Correct association between the signed-in player and their saves | floor | open |  |
| A49.02 | A clear response when an account signs out | floor | open |  |
| A49.03 | Controller ownership changing safely with the active user | floor | open |  |
| A49.04 | Platform overlays opening and closing without breaking control | floor | open |  |
| A49.05 | Screenshots and capture shortcuts working normally | floor | open |  |
| A49.06 | Supported achievements or trophies unlocking at the intended time | floor | open |  |
| A49.07 | Offline-earned progress synchronising appropriately when supported | floor | open |  |
| A49.09 | Missing content explained without silently damaging saves | floor | open |  |
| A49.12 | System sleep and resume behaving predictably | floor | open |  |
| A51.01 | A photo mode that pauses or clearly explains its live behaviour | floor (my call) | open |  |
| A51.02 | Photo controls that do not accidentally trigger gameplay actions | floor (my call) | open |  |
| A51.04 | Captures saved somewhere discoverable | floor (my call) | open |  |
| A51.05 | A streamer-friendly music option where licensed music would obstruct sharing | floor (my call) | open |  |
| A51.06 | Rewatchable tutorials, cinematics or records where the game provides an archive | floor (my call) | open |  |
| A51.08 | Credits that can be paused, scrolled or exited | floor (my call) | open |  |
| A51.11 | Clear rules for replay, chapter selection or New Game Plus where offered | floor (my call) | open |  |
| A51.12 | A way to distinguish completed content from remaining content | floor (my call) | open |  |
| A4 | Build version visible to the player | floor (my call) | open |  |
| Q5 | Minimum specification and the hardware floor | floor (my call) | open |  |
| R11 | Accessibility information before purchase | floor (my call) | open |  |
| S5 | Content variation by locale | floor (my call) | open |  |
| T1 | A store page, a build and patching | floor (my call) | open |  |
| T4 | Age rating submission | floor (my call) | open |  |
| T5 | EULA and third-party licence attributions | floor (my call) | open |  |
| T6 | Anti-cheat or DRM decision | floor (my call) | open |  |
| T7 | Platform terminology and button naming | floor (my call) | open |  |
| U3 | A way for the player to report a problem | floor (my call) | open |  |
| U4 | Patch notes and a post-launch plan | floor (my call) | open |  |
| V5 | Marketing capture: trailers and screenshots | floor (my call) | open |  |

### Not staged: ruled out before a stage was given

Stage state: OPEN

| id | feature | kind | status | evidence or reason |
|---|---|---|---|---|
| A03.07 | Simultaneous input where useful, such as controller movement with gyro aiming | floor | out | research: no gyro: PC, keyboard and pad |
| A05.18 | Shoulder switching where the aiming design requires it | floor | out | research: D24: not a shooter, no cover system |
| A05.19 | Lock-on that selects a plausible target, if present | floor | out | research: D24: not a shooter, no lock-on |
| A05.20 | Lock-on that releases sensibly when a target dies or disappears | floor | out | research: D24: not a shooter, no lock-on |
| A07.20 | Appropriate controls and release behaviour for ropes, ziplines or grapples, if included | genre G1 | out | G1: No ropes, ziplines or grapples; no parkour |
| A08.17 | Consistent first-person hands, body and third-person appearance where both views exist | floor | out | research: third person only; no first-person view is planned |
| A17.05 | A distinction between damaging armour, a shield and an exposed target | genre G3 | out | G3: No armour or shields in 1990; not that kind of combat |
| A18.10 | Combos that accept inputs predictably, if present | genre G3 | out | G3: No combo system; brawling, not a fighting game |
| A18.12 | Finishing moves that cope with nearby walls and furniture | genre G3 | out | research: D18: no cruelty as spectacle, so no finishers |
| A19.02 | A solution to the camera seeing around cover while the muzzle remains blocked | genre G3 | out | G3: Not a shooter; no cover system |
| A19.09 | Appropriate rate of fire | genre G3 | out | G3: Firearms are events, not a rate of fire |
| A19.14 | Predictable handling of interrupted reloads | genre G3 | out | G3: Not a shooter; no reloading |
| A19.17 | Clear distinctions between ammunition types or firing modes, if supported | genre G3 | out | G3: No ammunition types or firing modes |
| A19.19 | Scope transitions that preserve orientation | genre G3 | out | G3: No scopes |
| A19.22 | Explosion effects with understandable range and cover interaction | genre G3 | out | G3: No explosives as a player weapon |
| A23.11 | A sensible solution for player visibility in mirrors where mirrors are usable | floor | out | research: no usable mirrors planned; D24 spend rule |
| A26.18 | Vehicle damage communicated visually or mechanically | genre G4 | out | G4: Not a driving game; Tom does not drive until the region |
| A26.19 | Recovery from an overturned or irretrievably stuck vehicle | genre G4 | out | G4: Not a driving game; no stuck cars for Tom to recover |
| A27.01 | Mounting and dismounting from plausible positions | genre G5 | out | research: no mounts in 1990 Britain |
| A27.02 | Mount movement whose gait matches its speed | genre G5 | out | research: no mounts |
| A27.03 | Mount turning and stopping that fit its body | genre G5 | out | research: no mounts |
| A27.04 | Mount avoidance of ordinary obstacles | genre G5 | out | research: no mounts |
| A27.05 | A usable way to call, locate or recover an owned mount | genre G5 | out | research: no mounts |
| A27.06 | Clear mount health, stamina or distress where those affect play | genre G5 | out | research: no mounts |
| A34.08 | Distinguishable friendly, hostile and neutral indicators where used | floor | out | research: D33: the player sees their own position, never other minds; no faction markers |
| A35.10 | A route or directional cue that follows reachable paths where supplied | genre G8 | out | G8: No minimap and no route guidance |
| A35.18 | Fast-travel eligibility, cost and restrictions explained where fast travel exists | genre G8 | out | research: a small dense town: no fast travel planned |
| A35.19 | Fast travel arriving at a safe, usable position | genre G8 | out | research: no fast travel planned |
| A35.20 | Travel preserving relevant equipment, followers and mission state | genre G8 | out | research: no fast travel planned |
| A36.09 | Comparison with currently equipped gear | genre G9 | out | research: no gear statistics to compare; objects carry history, not stats |
| A37.10 | Crafting recipes showing ingredients and output | genre G10 | out | G10: Crafting is out |
| A37.11 | Clear indication of which ingredients are missing | genre G10 | out | G10: Crafting is out |
| A37.12 | Preview of upgrade effects before spending resources | genre G10 | out | G10: Crafting and upgrades are out |
| A37.13 | Crafting consuming the stated ingredients and producing the stated result | genre G10 | out | G10: Crafting is out |
| A37.14 | Safe handling of crafting while inventory capacity is limited | genre G10 | out | G10: Crafting is out |
| A37.15 | Clear distinction between repair, upgrade and replacement | genre G10 | out | G10: No crafting or upgrade system |
| A38.08 | Customisation previews before commitment | genre G11 | out | research: a fixed protagonist, Tom Novak: no character creation |
| A38.09 | Character creation that can be inspected under useful lighting | genre G11 | out | research: no character creation |
| A38.10 | Appearance choices that remain recognisable in gameplay | genre G11 | out | research: no character creation |
| A38.13 | A clear distinction between cosmetic and mechanical choices | genre G11 | out | research: no character creation |
| A41.12 | HDR configuration where HDR is supported | floor | out | research: no HDR target named; PC first, smallest budget |
| A42.18 | Aim-assistance configuration where assistance is provided | floor | out | research: D24: not a shooter, no aim assistance to configure |
| A42.20 | Separate contextual bindings where driving or other modes require them | floor | out | research: driving takes the smallest budget; no separate driving bindings planned |
| A43.08 | Scalable or configurable aiming reticles | floor | out | research: D24: not a shooter, no reticle |
| A44.11 | Separate voice-chat and game-audio control in multiplayer | floor | out | research: single player: no voice chat |
| A45.06 | Quick-time events that can be simplified or bypassed where appropriate | floor | out | research: no quick-time events planned |
| A45.12 | No mandatory motion gesture without a button alternative where practical | floor | out | research: PC first: no motion controls |
| A49.08 | Owned downloadable content correctly recognised | floor | out | research: no downloadable content planned |
| A49.13 | Handheld or small-display interfaces remaining usable where the platform is supported | floor | out | research: PC first: no handheld or small-display target |
| A50.01 | A clear way to host, join or find a session | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.02 | Clear distinction between private, friends-only and public sessions | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.03 | Invitations that reach the correct session | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.04 | Useful explanation when joining fails | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.05 | Connection progress with a way to cancel | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.06 | Region or connection-quality information where latency matters | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.07 | Other players' movement represented smoothly enough to interpret | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.08 | Hits and interactions resolving consistently enough to feel fair | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.09 | Clear ownership of mission progress and rewards | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.10 | Clear rules for shared versus individual loot | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.11 | Safe handling of players joining or leaving mid-activity | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.12 | Recovery or clear consequences when the host disconnects | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.13 | Rejoining without unnecessary loss of progress where supported | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.14 | Clear downed, dead and spectating states | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.15 | A usable revive or respawn flow where the mode includes one | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.16 | Communication through voice, text or pings as appropriate | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.17 | Voice input and output selection | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.18 | Visible microphone state and a reliable mute control | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.19 | Individual mute, block and report controls | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.20 | Clear communication of friendly-fire rules | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.21 | Understandable handling of version or content mismatches | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.22 | Clear warning that menus do not pause a live session | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.23 | Protection against common forms of cheating or session disruption appropriate to the mode | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.24 | Supported cross-play and cross-progression behaving as advertised | genre G0 | out | G0: Multiplayer stays out; single player |
| A50.25 | A clear end-of-session flow that preserves earned progress | genre G0 | out | G0: Multiplayer stays out; single player |
