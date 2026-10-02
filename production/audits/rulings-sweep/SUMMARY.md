# Rulings sweep, 1 October 2026: what became of every ruling

**The question (Jafar, 1 October).** Twice this week a ruling of his turned out never to have been built:
- "Grime is the strategy" (D53, 21 September). The street generator says its wear layer is not its job, so nothing built it.
- Character casting. It was flagged as missing a week before the characters were built without it.

Every ruling in DECISIONS.md and canon.md was swept, along with every ruling of his in the files CLAUDE.md names. Each was read against the code, the content and the lists, not the sessions' own claims. The question for each: was it built, partly built, put on a list, superseded, or nowhere? What is nowhere is ranked below by how much it matters to a player, with where it belongs and whose lane it is.

No fixes, no praise. Files beside this one:
- `TABLE.md`: one entry per ruling, with its status, what is missing and the evidence.
- `rulings.json`: the full record, every citation.
- `METHOD.md`: the brief each helper worked to.

## What was swept

**440 rulings:**

| Source | Rulings |
|---|---|
| DECISIONS.md | 211 |
| Its archive, production/archive/DECISIONS-to-2026-09-24.md (CLAUDE.md: "its archive still binds"; D53 lives there; the old D-records were opened for their operative requirements) | 138 |
| canon.md | 43 |
| Lines carrying his rulings in CLAUDE.md, ROADMAP.md, NOW.md, TOWN.md and CLOTHES.md | 48 |

**Against which code.** Main as of 3981e28 (1 October, 21:28). Later commits, up to 90db276:
- add the clothing session's Marvelous Designer tools and research note, which changes no verdict;
- record one new ruling, his yes at 21:33 to Tom's written suggested lines (DECISIONS.md's last line, not counted here). The suggested-lines spec now says "passed", so DEC-200 moves from "on a list" toward built once the builder's panel shows them.

**Not swept:**
- the 111 dated rulings in legacy/studio-v2/game-design/, except those the archive names;
- the old queue items;
- the checklist.

## How it was done, and how far to trust it

**Eleven helpers.** Each took one batch of rulings, worked to one brief (METHOD.md) and wrote nothing in the repository. Their rules:
- Judge from the code, content and lists, never from a claim. A line saying "built in X" means X was opened.
- Cite file and line for everything.
- Keep what was seen in the code apart from what was inferred.
- Something that exists only in the C# Core or the old Unity build, and that the Unreal game does not reach, is only partly built.
- A ruling takes the status of its weakest part.

**What I checked myself:**
- Every "nowhere" verdict and the high-impact "partly" ones, in the code: 31 rulings, marked **R** in TABLE.md.
- A random sample of eight "built" verdicts. I opened five; all held.
- Two helper claims were wrong when I checked them:
  - A witness path said to use daylight at night runs only in the scripted story, not in play. It is left out.
  - The town branch on GitHub holds none of the fixes the town's summary claims (below).

**Two limits:**
- **The disk filled for about six minutes (19:55 to 20:01).** My own earlier fetch of every branch caused it. Two helpers' last commands returned empty output in that window. The canon helper re-ran every empty search its verdicts rest on, and I re-checked the other helper's late "nowhere" verdicts myself.
- **The 248 "built" verdicts are the helpers' own, with file:line evidence.** Only a sample was checked again.

Nothing was run in Unreal: there is no Windows machine or graphics card here.

## The counts

| Source | Built | Partly | On a list | Superseded | Nowhere | Conduct only |
|---|---|---|---|---|---|---|
| DECISIONS.md | 135 | 27 | 24 | 16 | 8 | 1 |
| The archive | 71 | 32 | 14 | 12 | 8 | 1 |
| canon.md | 23 | 9 | 7 | 0 | 3 | 1 |
| The other five files | 19 | 11 | 14 | 2 | 0 | 2 |
| **All 440** | **248** | **79** | **59** | **30** | **19** | **5** |

**What the columns mean:**
- **Partly:** some of the ruling is built and some is not. Often the missing part is the only part a player would meet.
- **On a list:** not built, but named as work still to do on NOW.md, TOWN.md, CLOTHES.md, ROADMAP.md or FINDINGS.md.

## Ranked: what is nowhere at all

**Definition.** Nowhere means the ruling, or the part of it a player would meet, is:
- not built;
- on no current list;
- not superseded by a later ruling.

That covers the 19 whole rulings, plus the missing parts of part-built rulings that are themselves on no list. Those parts are the same failure as the grime ruling.

**Impact scale:**

| Score | Meaning |
|---|---|
| 5 | The first session, or the premise or a rule broken |
| 4 | Ordinary play |
| 3 | A particular path, or a long session |
| 2 | Rare, or polish |
| 1 | Invisible to a player |

Within a score, what a player meets sooner comes first.

**The checked column:**
- **R:** checked by me in the code.
- **H:** checked by a helper in the code.
- **I:** inferred.

### Impact 4: met in ordinary play

| # | What is nowhere | The ruling | Where it belongs | Lane | Checked |
|---|---|---|---|---|---|
| 1 | Sheila speaks in voice D, which came off his page for leaning American. His pick, p267, is in no file of the game's. The voice server learns her from the only Sheila clip there, lena.parler-d.mp3. A clip kept only on his PC cannot be seen from here. | DECISIONS:136 (30 September) | game-design/picked-clips, production/specs/in-game.json; a line on NOW.md's list | builder | R |
| 2 | Darren wears his old face. CrimeProbe.cpp:917 hard-codes take C5; he approved S6 on 30 September. Only the overview's prose says "S6 next"; no list item does. | DECISIONS:136, :184; CLAUDE.md "faces frozen" | CrimeProbe.cpp:917, in-game.json; NOW.md | builder | R |
| 3 | Sheila has no thinking sound, so every line put to her waits about five seconds in silence. Only Ron and Darren have them (content/voice/acks). | DECISIONS:84; archive:200 | content/voice/acks/lena, under NOW.md item 2 (the delay) | builder | R (the five seconds is I, from the measured delay) |
| 4 | Subtitles appear when the words arrive, about 3.5 s before the voice. The ruling: "the subtitle appears only with the audio it belongs to". | archive:200 (23 September) | CrimeProbe.cpp:5001: show each piece on its playback | builder | R (the 3.5 s is H) |
| 5 | The man at the ferry landing never says his lines (when to come back, kept waiting, "we're done"). The game shows its own caption instead (CrimeProbe.cpp:6247). His lines are ported (TheLanding::Line) and called only by tests. | DECISIONS:125 ("settled as written") | CrimeProbe.cpp's quay handling | builder | R |
| 6 | After the smash nobody gathers and nobody drifts back. The looking is in the twenty basics and the quieter talk is under V4; gathering and drifting back are on no list. | archive:201, "the minute after" (23 September) | PersonAnim.cpp and the walkers; V4 | builder | H |
| 7 | No moving traffic, and no firm's cars driven by others. His words: "in the street now, because a street with no traffic feels dead". The traffic model is in the C# Core and the Unity build only. | archive:111 (G4, 23 September) | a port of Core Traffic.cs; NOW.md | builder | H |
| 8 | The people you see in the street neither see nor remember. Their spec: "seen and not simulated: no collision, no perception, nothing a system reads". D25: everyone perceives, remembers and gossips. | archive:53 (D25) | street-people.json and VignetteShot.cpp's spawn: give them perception and memory, or a ruling to remove them | builder | R |
| 9 | Voices are still flat. The experiment he ordered, cheapest first, never got its first two steps: per-line emotion from what the character feels, and paralinguistic tags. Acted references and VoxCPM2 were tried. | archive:226 (24 September) | voice-server.py taking a direction per line from the talk program's mood; NOW.md | builder | H |
| 10 | Attributions do not travel with the game. THIRD-PARTY.md's engine section still says Unity, with no Unreal, MetaHuman or Epic entry. Nothing packages it, and there is no credits page. VCTK's CC BY needs credit. Invisible in play; a licence breach the day a copy leaves his PC. | archive:133-134 ("the allowlist is law"; "the attributions themselves, for everything shipped") | THIRD-PARTY.md, tools/ue/stage_game_data.py, a credits page | builder | R (THIRD-PARTY.md), H (packaging) |
| 11 | People talk through a worse model because of who they are, which D48 forbids. The model follows each card's tier (ConversationEngine.cs:281): Ron and Darren on the cheaper model, Sheila on the better. His 1 October tap kept Sheila on hers without naming D48. | archive:42 (D48) | a ruling: tier by the interaction, everyone on the better model, or D48 retired | Jafar | R |

### Impact 3: met on a path, or over a session

| # | What is nowhere | The ruling | Where it belongs | Lane | Checked |
|---|---|---|---|---|---|
| 12 | **The day-one arrival.** The ruling: his arrival "waits for day 0" (who saw him come, and the line said to his face). A free-play new game now starts on day 0 at nine (CrimeProbe.cpp:8030). Both pieces are ported, but only the tests call them. **The condition has arrived and nobody picked the work up: the grime pattern exactly.** | DECISIONS:135 | CrimeProbe.cpp, free play's day 0 | builder | R |
| 13 | **Grime's floor.** Wear itself reached a list on 1 October (V4's "stains and wear"), ten days after the ruling, and only after his no to the street. D53's own requirements are on no list: a wear floor in numbers, and wear coverage printed per surface. Neither exists; the terrace spec says "THE FLOOR HAS NO NUMBER". | archive:65 (D53) | the material step in tools/ue and the frame's verdict line; V4 | builder | R |
| 14 | No beat constable in free play who knows Tom by sight. CrimeProbe.cpp:2310 says "NO CONSTABLE IN PLAY"; he exists only in the scripted test. | archive:158 (his decision 3, 22 September) | a constable in hook-cast.json (town) and among free play's witnesses (builder) | builder, town | R |
| 15 | Nobody has their own nerve, loyalty or greed: all forty share one temper. The rule that answers the bravest as frightened is still in the Core (StreetVoice.cs:813) and the port (StreetVoice.h:457). | DECISIONS:123 | hook-cast.json, both StreetVoice files; TOWN.md | town (port: builder) | R |
| 16 | The ending's signs, Tom's reading of what the ending will cost, and the police's investigating day. Deferred "until the playable route works", and no list will bring them back. | DECISIONS:66, :113, :152, :158 | TOWN.md, after the route | town | H |
| 17 | Townspeople: the crowd measured at 0, 5, 10 and 20 in the package; the walkers' feet matched to their clips (PersonAnim.cpp:344 moves them at a fixed speed); one approved sample before twenty. V6 lists natural walking only. | DECISIONS:166 | NOW.md, beside V6 | builder | R |
| 18 | The crime layer's owed verbs, in order: order a man hurt, point a plan at a person, frame someone, lean on a witness, move a body, sanction crew, hit a rival's property, have someone vouch. Also the press through a person, grassing, and combat's three gaps. None is on ROADMAP's stages. | archive:44 (D56) | ROADMAP stage 3; then TOWN.md (Core) and NOW.md (port) | town, builder | H |
| 19 | The genre items ruled "in" that the game lacks and no list carries: climbing low walls and fences (G1), crew acting on Tom's orders (G2), fists and improvised weapons (G3), short skippable cutscenes (G6), coat and pockets (G9), buying, selling and fencing (G10), killing (canon). Most exist in the C# Core or the Unity build; none is ported. The builder's checklist sweep marks them "later", which is research, not a list. | archive:108-117; canon:115 | ROADMAP's stages, then ports into ue-probe | builder | H; R for cutscenes (no sequencer module) |
| 20 | The story past the first week: the three rivals, Acts II and III, the five endings and their hunted-state paths. They exist in the C# Core only, whose text still calls Mickey's a pub; never ported and on no list. | canon:80, :174-178; archive:57 (D58); DECISIONS:54, :59 | TOWN.md (reword the Core), then a port | town, then builder | H |
| 21 | The town's own news. His terms: ten more stories "wait until Jafar has met it in the assembled game". As wired he cannot: the game never loads production/specs/town-news.json. The ported TownNews runs only in tests. | DECISIONS:70, :124 | CrimeProbe.cpp, filing the stories at their hour | builder | H |
| 22 | Overheard gossip in free play is never voiced: StreetVoice::Exchange is called only in the scripted encounter. The neighbours' own talk is on V4; this half is not. | DECISIONS:63 | CrimeProbe.cpp's free-play tick | builder | H |
| 23 | Owning up to a window never earns the caution (two hours, no charge), because nothing passes the owned-up flag. And the coat, never built, is never kept as evidence. | DECISIONS:98 | CrimeProbe.cpp's constable hour | builder | H |
| 24 | **The brand bible.** The kiosk's operator mark and the pillar box's cypher were never made, and the two stand plain. The football club, paper, pirate radio and TV were never minted. The bible still says "MICKEY'S IS A PUB AND STAYS A PUB", founded 1962 (content/brands/brand-bible-v1.json:11, :88-89), against D19. | canon:163-167; DECISIONS:131 | content/brands/brand-bible-v1.json, then the two pieces | town, then builder | R |
| 25 | Presentation's owed steps: film grain, slight chromatic aberration, lens dirt, a grade toward the period's film stock, and depth of field in conversation. Only the engine's defaults run. | archive:67 (D28) | production/specs/unreal-look.json's post-process; the visual bar (V5) | builder | H |
| 26 | The performance target: 60 frames a second at his screen with the voice running, never below 30. The last measurement is from 24 September, before the MetaHumans, shop rooms and cloth. Nothing checks it. | archive:216 | route_walk.py or the AI tester logging frame times; NOW.md | builder | H |

### Impact 2: rare, or polish

| # | What is nowhere | The ruling | Where it belongs | Lane | Checked |
|---|---|---|---|---|---|
| 27 | The voice watermark on lines made in advance (the street bank, thinking sounds, takes). On live speech, a failure to mark is silent. | archive:135 (D50) | every take tool in tools/voice-live | builder | H |
| 28 | His voice picks Danny p243 and June p277 were never made into clips; the old clips are still in place. Clean older voices for Ada, Carol Ellis, Geoffrey Agar, June and Maureen Jensen were never made. Only Walsh's is listed. | DECISIONS:13, :28; archive:225 | game-design/picked-clips; NOW.md | builder | H |
| 29 | No graffiti in the street. The Hook's tag, QUAY FIRM, is missing. | canon:47-51 | the street's decals | builder | H |
| 30 | The era's kit: CCTV at the bank, the camcorder as a rare witness, answering machines. His second CCTV site has never been put to him. | canon:55-59 | Core and port; Needs you for the site | town | H |
| 31 | The "what-they-know" display that D20 makes the way round instead of a minimap. The paper map waits with the Ledger. | archive:88 (D20) | the interface; ROADMAP stage 4 | builder | R |
| 32 | The plain statement of what is permanent, for a player who reloads. | archive:56 (D35) | the pause or save screen | builder | H |
| 33 | Boats and buses as moving scenery on a timetable. | archive:112 (G5) | ue-probe | builder | H |
| 34 | Credits, photo mode, and the state after an ending. | archive:202 | the interface | builder | H |
| 35 | The thirty regulars into the game: names, talk cards, routines, and the takeaway's bay and sign. Deferred "after the route works", with no list. | DECISIONS:149, :160 | hook-cast.json, the cards; TOWN.md | town | H |
| 36 | The smoking clip he said was wrongly dropped. Its only copy is still marked rejected, and no one in the game smokes. | archive:82 (queue 406, 21 September) | the animation set; V6 | builder | R |
| 37 | Father Walsh's and June's approved street lines can never be heard: only Sheila, Darren and Ron make street remarks (CrimeProbe.cpp:5730-5737). | DECISIONS:199 | free play's remark path, or a body and routine for each | builder | H |
| 38 | The content rule's checks miss the game itself. The animation check walks the old Unity library, not the game's clips; Epic's animation sample is coming under V6. The word and era gates skip the talk cards that go into every live prompt. No breach was found. | canon:129-139; archive:40 | tools/content-gate.py, tools/canon-gate.py | builder | H |
| 39 | The street layout spec with testable requirements, and the reads-as-real check. | archive:76 (D13) | the town's documents | town | R (the record) |
| 40 | Enforcement of the comedy register: no gate and no judge, and the live prompt does not state it. | archive:43 (D3) | the talk program's rules | town | H |

### Impact 1: invisible to a player

| # | What is nowhere | The ruling | Where it belongs | Lane | Checked |
|---|---|---|---|---|---|
| 41 | The microphone, "looked at again once the playable route works": on no list. | DECISIONS:208 | NOW.md, after the route | builder | H |
| 42 | The privacy notice, "drafted before any friend plays through our server". | DECISIONS:115 | TOWN.md | town | H |
| 43 | Players' own-key mode, from the business direction. | DECISIONS:10 | ROADMAP | builder | H |
| 44 | Text kept out of the code so it can be translated later. Interface strings and street lines are in the C++ and C# source. | archive:119 (G12) | the interface kit | builder | H |

**Not ranked, but dated, and money.** The Marvelous Designer trial becomes a paid subscription on 15 October unless cancelled (DECISIONS:217). That date is in no list and not in Needs you. (Jafar, clothing; H.)

## Built, but against a ruling

Each of these is built and contradicts a ruling. None was recorded as a new ruling.

1. **A budget cap switches off the claim check.**
   - The talk program sets the checker only when its model client is the plain Anthropic one (ledger/TalkHelper/Program.cs:273). Any budget wraps that client (:1424-1432), so no check runs.
   - The AI tester always sets a budget for real talk (tools/ai-tester/play.py:426-428). So the 30 September measuring run (DECISIONS:173) ran with no claim check, and its 1.9 s to the words is not the whole real path.
   - Any capped live play would also run unchecked, while the AI notice tells players every line is checked.
   - Jafar's own play passes no budget, so it is checked.
   - R, read and not run.
2. **The relay would refuse two of today's live calls:** suggested lines ("You suggest…") and the threat read ("You read one line a man says…"). It admits only three openings (Relay.cs:62-71). So "every live call can go through it" (DECISIONS:56) no longer holds. R, read and not run.
3. **The brand bible's "Mickey's is a pub"** contradicts D19 (above, item 24). R.
4. **D48's model by person** (above, item 11). R.
5. **The accent checker still acts as a gate.** take_gate.py prints REJECT, and page_voices.py leaves failed lines off the page. The 30 September rule says it is "a screen, never a gate", flagged beside the take for his ear (DECISIONS:154; CLAUDE.md). H.
6. **The names gate does not know "Emil"**, retired on 28 September (tools/names-gate.py; DECISIONS:90). R.
7. **Stale "Blender only" lines.** CLAUDE.md:67 and CLOTHES.md:3 still say "Blender only" and "not Marvelous Designer", against DECISIONS:216. H.
8. **The spectacles failure, again in the handovers.** NOW.md:39 tells clothing to fit Sheila on MH_LenaC1's body, while NOW.md:37 says the C1 export is superseded (CLAUDE.md: every handover names the exact version). H.
9. **Work called done that is not on GitHub.** FOR-JAFAR.md's "Town, 2 October" calls three things done, "each test first":
   - Ron and Sheila never going to the police;
   - a threat silencing a witness;
   - no tea invitation from the cells.

   None is on main (the last Core commit is a0a0891, 20:01). GitHub's `town` branch was last pushed on 28 September. If the work exists, it is only on his PC. (DECISIONS:186 and :210; R.)
10. **No approval is current.** tools/approvals.py, run read-only, reports all eight things placed in the game with no current approval (DECISIONS:29). H.
11. **cleanup.py admits production/playtest,** which holds tracked records, the measuring run's among them. The disk rule admits only ignored build and scratch output (CLAUDE.md, Disk). H.
12. **A pub picture is still in a street spec.** The fallback spec (production/specs/vignette-pieces.json:657) places a back-bar picture of spirit bottles and pumps. It is hidden only while the Blender street loads. The content gate does not read that spec. H.

## Why rulings do not become work: the patterns

1. **Deferred "until something", with no list to bring it back.**
   - The ending's signs and reading (item 16), the regulars (35), the townspeople steps (17), the microphone (41) and the privacy notice (42) each wait on a condition that no list watches.
   - The arrival (12) waited for day 0. Day 0 came, and the work did not.
   - The town's news (21) waits on a condition that cannot happen as wired.

   This is the grime ruling and casting again.
2. **"Built" often means built in the C# Core, or ported and never called.**
   - The router (recorded done, DECISIONS:22), Act III and the endings, the rivals, crew orders, combat, the economy, the coat, the press, heat, killing, bribes and traffic are real, tested code. The game never reaches them, and no list carries their port. Twenty rulings are "partly" for that reason alone: DEC-006, 016, 048 and 053; ARC-007, 021, 047, 048, 049, 054, 055, 082, 105, 114 and 134; CAN-017, 023, 024, 031 and 043.
   - Five more were ported into the game's C++ and are called only by tests: the town's news, the landing's lines, the arrival, the crowd schedule and the fixed clock (DEC-064, 119, 129; ARC-100, 112).
3. **His picks are recorded and not carried into the game.** Darren's S6, Sheila's p267, the Danny and June voices, and the approval files the build checks (items 1, 2, 28; "built, but against a ruling" 10).
4. **An umbrella list line names the topic, and the ruling's specifics fall out.**
   - V4's "stains and wear" now carries D53's direction but not its floor or its measure.
   - ROADMAP stage 4's "the Ledger" carries D12, D20, D33, D36, D37, G7 and G8.
   - "Then the town" carries canon's districts and streets.
5. **Later code quietly changes a ruling, and no ruling follows.** D48, the accent gate and the budget wrapper (above).

## Lanes

| Lane | Nowhere items |
|---|---|
| Builder | 36, four of them shared with the town (items 14, 18, 20 and 24). All ten of impact 4 except D48 are the builder's (items 1-10). |
| Town | 11, the four shared included. Its highest are impact 3: items 14, 15, 16, 18, 20 and 24. |
| Jafar | 1: item 11, D48. Plus the trial's date. |

## Checked, and inferred

**Checked by me in the code:** the 31 rows marked R in TABLE.md, each with its line. These are every "nowhere" verdict and the high-impact "partly" ones above. Among them:
- the constable's absence;
- the router's absence from the talk path;
- Darren's C5 and Sheila's clip;
- the subtitle timing;
- THIRD-PARTY.md's engine;
- the unused fixed clock;
- the smoking clip;
- D20 and D13's owed parts;
- D48's model by card;
- no cutscene module;
- no per-person nerve, and the reversed nerve rule;
- the fixed walking speed;
- day 0 and the uncalled arrival;
- Sheila's missing thinking sounds;
- the landing's unused lines;
- the unsimulated street people;
- the relay's openings;
- the brand bible's pub;
- the budget-cap path;
- the town's claimed fixes, missing on main and on the town branch.

**Checked by a helper in the code:** every other row. Each carries its own file:line evidence in TABLE.md and rulings.json.

**Inferred, not proved:**
- Every impact score is a judgement.
- "3.5 s early" for the subtitles is a helper's estimate from the delay figures.
- The relay refusals and the unchecked capped run were read, not run.
- Whether Sheila's p267 clip or the town's three fixes exist on his PC cannot be seen from here.
- "On no list" means none of NOW.md, TOWN.md, CLOTHES.md, ROADMAP.md, FINDINGS.md or the overview's Needs you. The builder's 29 September checklist sweep, which marks many genre items "later", was read as research, not a list.
