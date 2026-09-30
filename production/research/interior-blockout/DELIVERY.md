# Making a game interior, from requirements to a tested layout: the detail

Research, 30 September 2026, by a separate research helper (about thirty minutes of searching and reading). It supports the list item "Mickey's office: a rough playable layout first, routes, camera and interactions, from its requirements and several references". It does not repeat the period photograph hunt in ../cab-office-interior-1990/ or the business facts in ../cab-office-1990/.

Labels. OPENED: the page itself was read. SNIPPET: only a search engine's summary was seen. PROJECT: read from this repository. A source numbered [S1] and so on is listed in full at the end. Most design sites (the Level Design Book, GDC Vault, Game Developer, 80.lv, World of Level Design, Medium, YouTube, legislation.gov.uk, Historic England, council sites) were closed to this helper's network, so much below is SNIPPET. Where the text says "my recommendation" or "estimate", it is not established practice.

---

## (a) The professional pipeline, stage by stage

Established practice, in the order the sources give it. The Level Design Book (Robert Yang and others, a free online book widely used in teaching) sets the phases out as: pre-production, layout, blockout, scripting, lighting, environment art, release. It adds that there is "no single foolproof way" and that with experience you learn when to skip or expand a phase [S1]. Epic's own tutorial, the Fortnite editor's greyboxing guide and several studio talks describe the same order [S10, S12, S21, S22].

### Stage 0. Brief: what the space is for

- What it is. A short written statement: the space's purpose, the beats that happen there, who is in it and where they stand, what the player does, and the rules of the place. Pre-production is "plan out the big ideas and overall experience design" [S1]. At IO Interactive (Hitman 2), pre-production of levels began by treating each space as a social space with its own rules: public, public with a purpose, public with rules, private, private professional, private personal. Each type tells the designer who belongs there, what counts as trespass, and what the player can get away with [S16]. A back office where a bookkeeper keeps the books is a "private professional" space in those terms. A waiting area by a counter is "public with a purpose". Some studios also draw a beat chart: one page listing what happens, in order, and where [S7].
- Gate. The brief is agreed. Every space in it has a reason tied to something a person does. Nothing goes in "because rooms have one".

### Stage 1. References from many sources

- What it is. Designers and environment artists gather many references: photographs, plans, catalogues, film and TV, and other games. No source describes waiting for one exact photograph.
  - Gone Home (GDC 2015). The environment artist researched a 1990s family in a Victorian house through web searches, libraries and old blueprints, and used a 1990 Sears catalogue bought on eBay [S14].
  - Max Payne (GDC 2002). The team aimed for "realistic level design", real places rather than rooms laid on a grid [S8].
  - Arkane. The studio splits "level architects", who make places credible and not "game-y", from "level designers", who make them play well. The two sit side by side [S18].
  - Environmental storytelling. Smith and Worch (GDC 2010) drew on documentary photography and narrative journalism as well as games [S15].
- Gate. The board answers the layout questions: what fixtures such a room has, roughly how big they are, and how people use them. Holes are listed, not waited on. Our project rule (photographs govern what things looked like) applies at dressing, stage 7.

### Stage 2. Layout on paper: bubble diagram, then plan from above

- What it is. The Level Design Book's layout phase:
  - thumbnail "partis" of the core shapes;
  - a bubble diagram of which spaces connect and how;
  - a floor plan, a top-down drawing with walls and floors [S1, S2].

  Totten's book *An Architectural Approach to Level Design* (2014; 2nd edition 2019) teaches proximity and "molecule" diagrams for the same step [S6]. McMillan's Gamasutra pieces "The Metrics of Space" (2012 and 2013) do the same [S9]. A 2023 Game Developer piece on stealth level design says some studios do "extensive work on paper as flow diagrams" before any blockout [S13].
- Gate. A dimensioned plan with every space in the brief, every route in and out, and every standing position marked.

### Stage 3. Metrics

- What it is. The numbers for this character and this camera: height, width, door and corridor widths, ceiling heights, stair sizes, and distances between people.
  - The Level Design Book says metrics cannot really be tested on paper. It says to settle them at blockout, early, because changing them late is costly. It recommends a developer-only "metrics zoo" or "playground" map with sample rooms, doors and stairs to walk [S3].
  - Epic's tutorial gives generic metrics for its 1.8 m character: "Hallways: 2-3m wide, 3-4m tall", "Doors: 1 - 1.5m wide, 2m tall", "Walls: 4m tall" [S10, OPENED]. These suit a fast shooter template and are wider than real rooms.
  - Bethesda (Skyrim, GDC 2013) built "kits" snapped to a grid so that metrics hold across every room [S5].
- Gate. A one-page metrics sheet for Tom and the third-person camera, checked in a test room.

### Stage 4. Blockout (also called greybox, whitebox or blockmesh) in the engine

- What it is. "A playable rough draft of the level", built with simple blocky shapes, so it can be tested in the engine [S4]. Epic's Fortnite guide says the same: "Greyboxing (also known as blockout) is the process of making a playable rough draft of a level to get a sense of its gameplay before polishing its look" [S12, OPENED]. World of Level Design says a blockout is NOT meant to be finished, pretty, textured, lit or detailed [S11].
- Tools in Unreal (5.8 documentation):
  - Plain shapes on a grid. Epic's Designer 01 tutorial builds from basic shapes and uses a 10 cm grid snap, a grid material with 1 m and 0.1 m lines, blocking volumes and "Play From Here" to test sections [S10, OPENED].
  - CubeGrid, in Modeling Mode, "creates blockout meshes using a repositionable grid". It pushes and pulls faces and outputs a static mesh, dynamic mesh or volume. It is marked Beta [S23, OPENED].
  - Geometry Script is a plugin of mesh functions callable from Blueprint and Python. It is marked Beta [S24, OPENED]. Epic's Lyra sample used it for parametric blockout pieces: set width and height in the details panel, bake to a mesh, swap back to edit [S25, OPENED].
  - Level Instances group actors into a reusable sub-level. Packed Level Actors merge static meshes for rendering [S26, SNIPPET].
  - BSP brushes are the older route, still present [S27, SNIPPET].
- Colour. No shared industry colour code for blockout was found (see (e)). What the sources do say:
  - Naughty Dog's David Shaver (GDC 2018) urges "consistent shape and color language" [S17].
  - One community guide reports yellow for climbable and red for hazards as one studio's habit [S28].
  - The Level Design Book notes light gridded textures for judging size [S4].

  Each project sets its own key.
- Gate. The player can move through it. Doors, blockers and navigation work, and the interactive objects exist as marked stand-ins.

### Stage 5. Playtest and iterate

- What it is. Walk it and have others walk it. The Level Design Book recommends critique by someone else after each phase: after layout, blockout, scripting and art pass. It says it is "cheap" to delete or rebuild blockout geometry and "expensive" to throw away finished art [S4]. Shaver: the biggest tool is getting other people to play "as early and often as possible and iterate quickly" [S17]. Riot's Valorant maps are reported to spend about a month in greybox and playtest before art blockout [S19].
- Gate. The playtest checklist passes: routes, camera, conversations, interactions, sightlines. A fresh tester who did not build it finds nothing blocking.

### Stage 6. Scripting and a plain lighting pass

- What it is. Wire the interactions and the NPC positions. Then do a lighting pass "early in the level design process, before a proper art pass", because light serves gameplay and readability [S20]. Shaver treats the layout itself as a lighting tool and sets the dominant mood early [S17].
- Gate. Readable through the game's own camera and exposure (our rule, Jafar, 30 September): the book, the radio, Sheila's desk and both yard exits can be picked out in a normal frame.

### Stage 7. Lock and hand-off to art; dressing

- What it is.
  - Environment artists usually wait for a mature blockout. An intermediate "art blockout" keeps geometry changeable while art starts [S21].
  - The sequence reported in one survey: greybox, then whitebox or art blockout (rough models, basic materials, first light), then art production [S19].
  - Modular kits replace the grey pieces [S5].
  - Set dressing then carries the story: props, texturing, lighting and composition that let the player infer what happened [S15].
  - Arkane builds basic volumes first and "layers" detail and extra routes on top [S18].
- Gate. The layout is locked, and any later change to it is a deliberate decision. For us, the art is then judged against the period photographs (production/reference/). By our rule, "done" means in the build and walked by the AI tester.

---

## (b) Third-person camera in small interiors

Established practice and evidence:

1. Third-person games make interiors roomier than life.
   - Max Payne (GDC 2002; third-person). Summaries say rooms in a third-person game run at about 150 to 200 per cent of real size, with the example of a real 4 x 5 m bedroom at 2.5 m high becoming about 8 x 10 m at 4 m high. Furniture stays near real size, "since the characters are also of real size" (larger furniture makes adults look like children). The same summaries also quote the talk warning against rooms "200% of the size they should be" [S8, SNIPPET; the two summaries do not agree on wording, see (e)].
   - Doors in third-person games are often made about 1.5 to 2 times real width. Mike Bithell says the doors in Gears of War "need to be massive for the third person camera to go through". Naughty Dog reportedly uses a subtle pull field around doors to steer the player through them [S29, SNIPPET].
   - Epic's generic metrics (doors 1 to 1.5 m, halls 2 to 3 m) point the same way [S10, OPENED].
2. Too big is also a failure. Gone Home's first rooms, laid out with shooter habits, were "too big" and lacked intimacy, and the artist shortened proportions [S14, SNIPPET]. Gone Home is first-person; the lesson about intimacy still applies to a small office.
3. The camera pulls in rather than clipping.
   - Unreal's spring arm "tries to maintain its children at a fixed distance from the parent, but will retract the children if there is a collision, and spring back when there is no collision". Its settings include a probe sphere size, a probe channel, camera lag, and a socket offset at the end of the arm [S30, OPENED].
   - Epic's third-person template reportedly uses a 400 cm arm and a capsule of 42 cm radius and 96 cm half-height [S31, SNIPPET].
   - Common practice is to pull in instantly, so walls never show through, and ease out slowly. Another option is to raise the camera and fade whatever blocks the view [S32, SNIPPET].
   - Unreal's Gameplay Camera System (Experimental in 5.8) can switch between camera rigs by context through a camera director and transitions [S33, OPENED]. A simpler route is to change the spring arm's length and offset inside a trigger volume (my recommendation, not sourced).
4. Camera talks. John Nesky (Journey), "50 Game Camera Mistakes", GDC 2014 [S34, SNIPPET]:
   - "Dynamic third-person cameras are the hardest to design."
   - Honour the player's intent.
   - Use a sphere check for collision and ease the camera closer gradually rather than jumping.
   - Do not let the camera intersect narrow columns.
   - Leave enough space between people and adjacent walls so the camera's near plane never cuts into a character.

   The last point is a level-design metric, not only a camera one.
5. Shipped games. The evidence reached here is thin.
   - Red Dead Redemption 2: player reports say the default camera sits higher and closer indoors and in camp, and Rockstar's support page documents cycling camera distances [S35, SNIPPET].
   - The Resident Evil 2 remake keeps a tight over-the-shoulder view in the police station's corridors [S36, SNIPPET].
   - Nothing primary was found on Yakuza or Like a Dragon, GTA, Mafia or Hitman interiors (see (e)).
6. Conversations. The Witcher 3 placed dialogue cameras algorithmically (a generator filled a first pass of shots that people then fixed) [S37, SNIPPET]. It still needs room around the speakers for over-the-shoulder shots. Any conversation spot needs clear floor beyond each speaker's shoulder.

What this means for LEDGER (PROJECT facts, then my recommendation):

- The street camera today (read 30 September from ue-probe/Source/LedgerProbe/Private/SliceCharacter.cpp):
  - arm length 320 cm;
  - socket offset 45 cm to the side and 55 cm up;
  - Tom's body hides when the camera comes too close.

  The older LedgerCharacter uses 350 cm with collision on. Both characters set Tom's capsule to a 34 cm radius and an 88 cm half-height, so it is 0.68 m wide and 1.76 m tall (checked in the same files by the session that saved this note, 30 September).
- In a room 4.5 to 5.5 m wide (see (c)), a 3.2 m arm will retract almost everywhere Tom stands with his back to a wall. Retracting is correct behaviour. But when it retracts to about a metre, the view is cramped, and the body-hiding rule will blink Tom out.
- Recommendation, to test in the blockout, not adopt blind:
  - An indoor setting at three trial arm lengths (about 1.6, 2.0 and 2.5 m), a little higher, with a slightly larger shoulder offset.
  - Fast pull-in and slow ease-out.
  - Pick the one that keeps both Tom and the person he faces in frame in the tightest spot.
- Keep the building's outside as built (the shell is fixed by the street). Inside:
  - make doors and the counter gap game-sized (1.0 to 1.2 m) rather than real (0.76 to 0.84 m);
  - keep aisles at least 1.2 m;
  - use the tall ceiling (see (c));
  - keep furniture at real size, as Max Payne did.

  An interior larger than its exterior is a known trick. It is not recommended here unless the tests fail, because the window and the street make the mismatch visible.

---

## (c) Real-world dimensions: a small British shop-front office around 1990

The shell that already exists (PROJECT; the governing numbers for our room, but check the built street before fitting, per our versioning rule):

- Source: production/art/facades/2026-09-24-measured/east_parade-drawing.json, the measured drawing of 24 September, read 30 September.
- Each parade bay is 6.0 m wide and 8.0 m deep. The ground storey is 3.4 m floor to floor and the first floor 2.8 m.
- The frontage edges read, by my reading: pier 0 to 0.35 m; an opening of about 0.77 m (0.386 to 1.152); an opening of about 0.90 m (1.188 to 2.088); glazing of about 3.56 m (2.088 to 5.65); pier to 6.0 m. Height marks include 1.981 m (a 6 ft 6 in door head) and 2.4 m.
- The superseded pub study (production/research/atlas-01/MICKEYS.md) called these the public door and a narrower private door to a stair. The stair had 19 rises to 3.4 m and 18 goings of 0.24 m, about 4.3 m long in plan. That study also proposed a 2.4 m rear lane, a 1.2 m yard gate and a 1.8 m yard wall. It is a proposal for a pub, not a ruling, and only a hint for the yard.
- Wall thickness inside the shell was not checked. A 9-inch (about 0.23 m) solid brick wall was the byelaw norm [S38, OPENED], so the clear floor may be nearer 5.5 x 7.5 m. This is an estimate.

Period and general dimensions:

| Item | Figure | Status |
|---|---|---|
| Standard British internal door | 1981 x 762 mm (6 ft 6 in x 2 ft 6 in), the most common; 838 mm (2 ft 9 in) for wider openings. Imperial sizes are the ones found in buildings from before the 1990s | SNIPPET [S39] |
| External doors | Commonly about 813 to 914 mm wide, 2032 mm high in modern stock; older shop doors vary | SNIPPET [S39]; period value is an estimate |
| Accessible entrance | 775 mm clear opening (Part M, visitable dwellings; later than 1990); 1000 mm for new public buildings today | SNIPPET [S40]; not period; an old shop in 1990 would not have been rebuilt to it |
| Shopfront | "Narrow" frontage is under 4 m; glazing head usually 2.4 m or more; stall riser 300 to 600 mm (council shopfront guides, 2005 onwards) | SNIPPET [S41] |
| Terrace streets | Street at least 36 ft (11 m) wide; at least 150 sq ft (14 m²) open area at the rear of each house (Local Government Act 1858); ginnels every fourth house | OPENED [S38, S42] |
| Room heights | Victorian principal rooms often about 2.7 to 3 m | SNIPPET [S43], weak source; our storey of 3.4 m allows about 3.0 to 3.2 m clear, estimate |
| Space per worker, in force in 1990 | Offices, Shops and Railway Premises Act 1963, s.5: 40 sq ft (3.7 m²) per person, or 400 cubic ft (11.3 m³) where the ceiling is under 10 ft, in rooms not open to the public | Figures SNIPPET [S44]; the Act's replacement by the Workplace Regulations 1992 (new workplaces from 1 January 1993, existing ones from 1 January 1996) OPENED [S45] |
| Counter | About 900 to 1100 mm; customer side often 1050 to 1100 mm, staff writing side about 900 mm | SNIPPET, modern [S46]; use as an estimate for 1990 |
| Desk | About 720 to 760 mm | Estimate (common furniture height, not sourced here) |
| Typical British shop unit | Frontage about 4 to 6 m, depth 8 to 15 m, with a back room or yard | Estimate; no dated British survey found |

For the game this means:

- A 6 m shop is wide by British standards, so the shell is plausible and generous.
- The 1963 Act means a staff-only back room of about 13 m² would lawfully hold three workers in 1990.
- The yard should be at least about 14 m² if it follows the terrace rule.

---

## (d) Concrete steps for this project

### 1. The brief for Mickey's (one page, drawn from canon)

Canon's words: "its information room is the business: a book of every fare, a radio nobody can help overhearing, a yard with two escapes, a rank outside". Sheila Dunn is the bookkeeper, at Mickey's since she was 22. Ron Kirby minds the door and the rank. Tom arrives, a stranger, having inherited it. Content rules: no alcohol, no gambling, no children; tobacco allowed, so ashtrays and smoke are fine.

| Space | What it is for | Who is there, where | What Tom does |
|---|---|---|---|
| The rank, at the kerb outside | Cars wait for jobs; drivers chat | Ron by the door or the kerb; drivers by their cars | Arrives; talks to Ron; is seen by the street |
| Front office, public side | Customers book and wait | A waiting bench along a wall; a customer or two | Walks in; hears the radio; reads the notices |
| Booking counter | Taking bookings; the book of every fare lives here by day | Whoever takes bookings, behind it | Looks at, or later reads, the book |
| Radio desk, staff side of the front office | Sending jobs; the radio "nobody can help overhearing" | The controller at the microphone | Overhears; later perhaps uses it |
| Back room | Sheila's books, the accounts, the safe or cupboard | Sheila at her desk, facing the door | His first real conversation; the books |
| Rear lobby | Back door, WC, kettle | Nobody | Passes through |
| Yard, two exits | Escape or discreet arrival | Nobody, or a driver having a smoke | Leaves by either exit |
| Stair door and upstairs | Behind the narrower front door | Nobody | Locked for this milestone (my recommendation) |

A canon question for Jafar: who works the radio? Canon names a bookkeeper and a door and rank man but no controller. For the blockout, put a stand-in mark at the radio desk and invent nobody.
- (a) Sheila takes bookings and the radio by day.
- (b) An unnamed night controller.
- (c) Mickey did it himself, and the chair is empty now. My recommendation is (c): it says the most about the inheritance and adds no character.

### 2. The reference board (several sources, in production/reference/)

- Room use:
  - the 1980 Brixton minicab office, with the booking man writing at the window and the number painted on the glass;
  - Pinter's controller "sitting at microphone";
  - the Minder, Boon and EastEnders dispatch sets (frame grabs when obtainable).
- Surfaces and fittings: Anna Fox's 1987 offices (carpet, wood-effect desks, fabric swivel chairs, letter trays, blinds).
- Objects: BT Viscount phone; Pye desk microphone; BT payphones of 1989 to 1990.
- The street: our own built Quay Street, for the window view and the rank.
- The camera: frames or clips of third-person interiors that work (Red Dead Redemption 2 interiors, the Resident Evil 2 remake corridors), for camera height and distance only.

Each entry says what it governs: layout, surface, object or camera. The earlier notes (../cab-office-interior-1990/) have the links.

### 3. The top-down plan (first guess, to be tested and changed)

Street at the bottom, yard at the top. The shell is 6.0 x 8.0 m outside, about 5.5 x 7.5 m inside (estimate). The stair strip sits behind the narrow front door. Game-sized doors are marked in brackets.

```
                 YARD  (at least 14 m2; exit A: gate to rear lane; exit B: second way out)
   +--------------------------------------+------+
   | rear lobby: back door (1.1) to yard,  |      |   ~1.2 m
   | WC, kettle                            |  S   |
   +-------------door (1.1)---------------+  T   |
   | BACK ROOM: Sheila's desk facing door, |  A   |   ~2.5 m
   | the books, filing, safe               |  I   |
   +-------------door (1.1)---------------+  R   |
   | staff side: RADIO DESK facing window  |      |   ~1.4 m
   |======= COUNTER (book, phones) ===gap 1.0      |
   | public side: BENCH, notices           | 0.9  |   ~2.4 m
   |      [ WINDOW ~3.6 m ]  [DOOR 0.9]   [stair door 0.77]
   +--------------------------------------+------+
        PAVEMENT                     RANK at the kerb
```

- With a stair strip about 0.9 m wide, the office's clear width falls to about 4.6 m. This is the tightest camera test and the first thing to try.
- If the stair is dropped for now, keep the strip as a boxed void so the layout stays true when it comes.
- Radio placement: at the side wall behind the counter it can be heard from the bench and the counter, and faintly from the back room.
- Window: sightline from the radio desk through the window to the rank.

### 4. The blockout, built by script in Unreal

- An editor Python script places scaled cube meshes on a 10 cm grid, following the plan's numbers.
  - Geometry Script and CubeGrid are both Beta. Plain scaled cubes are cheaper and enough.
  - Keep the numbers in one data file so a change is a one-line edit and the plan and the room cannot drift apart.
- Put the interior in its own Level Instance so it can later be swapped for art without touching the street.
- Add blocking volumes, navigation for NPCs, working doors, and simple standing mannequins at each NPC mark. The approved heads are not needed for a blockout.
- Our own colour key (my recommendation; no industry standard exists):

| Colour | Meaning |
|---|---|
| Mid grey with a 1 m grid | Walls, floor, ceiling |
| Darker grey | Fixed furniture (counter, desks, bench) |
| Yellow | Anything Tom can use (the book, radio, phone, doors, gate) |
| Blue floor discs | Where people stand |
| Green arrows | Routes and exits |
| Red | No-go or blocked |

  Use the same key in every future room.
- Two Unreal builds must not overlap. Render frames through the game's own camera.

### 5. The metrics check (before the first walk)

- Tom's capsule (34 cm radius, so 0.68 m wide) against the 0.90 m front door: about 11 cm a side, walkable but easy to snag if he enters at an angle. Through the 0.77 m stair door: about 4.5 cm a side, too tight for comfortable play, which is one more reason to keep that door locked for this milestone.
- Every interior door and the counter gap at least 1.0 m, preferably 1.1 to 1.2 m.
- Aisles at least 1.2 m.
- Clear ceiling about 3.0 to 3.2 m.
- Each conversation spot has the two speakers about 1.2 m apart, with about 1.5 m of clear floor beyond one shoulder (estimate, to be tested).
- The indoor camera at the three trial arm lengths in (b).

### 6. The playtest checklist

1. Routes:
   - street to front office to back room to lobby to yard, and out by exit A and by exit B;
   - back in by the yard;
   - no snagging on door frames, the counter gap or the bench.
2. Camera:
   - stand in every corner and every doorway and turn a full circle;
   - no wall through the picture, no pop or jump, Tom never blinks out;
   - both Tom and the other person visible in the tightest spot.
3. Conversations: talk to Sheila at her desk and to Ron at the door. Both faces are framed, and nothing sits between them and the camera.
4. Interactions: the book, radio, phone, doors and gate are reachable from where a person would naturally stand, and obvious in a normal frame.
5. Sound: the radio is audible at the bench and the counter, and faint in the back room.
6. Sightlines: from the radio desk and the window, the rank is visible; from the rank, the window. From the front door, can Tom see Sheila? Decide whether he should.
7. NPCs: Sheila, Ron and the stand-in controller stand where the brief says, and nobody blocks a route.
8. Light: one plain, readable lighting pass, judged through the game's own camera and exposure, day and night, not in portrait frames.
9. A fresh reviewer who did not build it walks it and tries to break it. Then the AI tester walks it in the build.

### 7. What "done" means before any dressing

- Every route and both escapes are walked cleanly in the build.
- The indoor camera setting is chosen, and it holds in every corner and doorway.
- Both first conversations are framed, and every interaction is reachable.
- The plan, the numbers file and the built room agree. A top-down frame and three or four game-camera frames are saved.
- The AI tester has walked it in the build.
- The layout is locked. Any later move is a deliberate decision, and dressing then follows the photographs.

### 8. Rough effort (my estimate, not measured)

| Step | Estimate |
|---|---|
| Brief | Half a day |
| Board | A few hours |
| Plan | Half a day |
| Scripted blockout | About a day |
| Indoor camera trials | Half a day |
| Two rounds of walking and fixing, plus a fresh reviewer | About a day |
| Lighting readability pass | Half a day |
| **Total** | **About three to four days of session time** |

The yard's second exit and the stair are the likeliest surprises.

---

## (e) What could not be verified or reached

- Blocked sites. The network refused most design sources: the Level Design Book, GDC Vault and its slides, Game Developer (Gamasutra), 80.lv, World of Level Design, Medium, YouTube, archive.org, the Radiator blog, Joel Burgess's blog, Game AI Pro, legislation.gov.uk, Historic England and council design guides. Only Epic's documentation and Wikipedia could be opened. Everything from the others is SNIPPET: a search engine's summary, which can misquote.
- Max Payne. The room-size figures (150 to 200 per cent; the 4 x 5 m bedroom becoming 8 x 10 m) and the warning against rooms at "200% of the size they should be" come from summaries of the same GDC 2002 talk that seem to pull in different directions. The original article could not be read.
- Colour. No industry-wide colour code for blockouts was found; the key in (d) is a recommendation.
- Shipped games. Nothing primary was found on how Yakuza or Like a Dragon, GTA, Mafia or Hitman handle tight rooms with the camera. The Red Dead Redemption 2 point rests on player reports and a support page seen only as a summary.
- The Naughty Dog door "pull field" and Bithell's Gears of War quote come from a GamesRadar summary.
- British shop dimensions. No dated survey of British shop units around 1990 was found. The period law figures (1963 Act) are from summaries. The shell numbers are the project's own and were not checked against the built street in the engine.
- Project checks not made. The spring arm's probe size in our characters was not confirmed. (Tom's capsule radius, 34 cm, was checked afterwards by the session that saved this note.)
- Canon. Who works the radio is not in canon; it is a question for Jafar.

---

## Sources (all read 30 Sep 2026)

1. [S1] "How to make a level", The Level Design Book (Robert Yang et al.), undated, continuously revised. https://book.leveldesignbook.com/process/overview. SNIPPET.
2. [S2] "Layout", The Level Design Book, undated. https://book.leveldesignbook.com/process/layout. SNIPPET.
3. [S3] "Metrics", The Level Design Book, undated. https://book.leveldesignbook.com/process/blockout/metrics. SNIPPET.
4. [S4] "Blockout" and "Playtesting", The Level Design Book, undated. https://book.leveldesignbook.com/process/blockout and https://book.leveldesignbook.com/process/blockout/playtesting. SNIPPET.
5. [S5] Joel Burgess and Nate Purkeypile, "Skyrim's Modular Level Design", GDC 2013, transcript April 2013. http://blog.joelburgess.com/2013/04/skyrims-modular-level-design-gdc-2013.html. SNIPPET.
6. [S6] Christopher W. Totten, *An Architectural Approach to Level Design*, CRC Press 2014; second edition, Routledge 2019. https://www.routledge.com/Architectural-Approach-to-Level-Design-Second-edition/Totten/p/book/9780815361367. SNIPPET.
7. [S7] "Beat-chart: game designer's best friend", Game Developer, undated in summary. https://www.gamedeveloper.com/design/beat-chart-game-designer-s-best-friend. SNIPPET.
8. [S8] Aki Määttä, "GDC 2002: Realistic Level Design in Max Payne", Gamasutra, 2002 (day not seen). https://www.gamedeveloper.com/design/gdc-2002-realistic-level-design-in-i-max-payne-i-. SNIPPET.
9. [S9] Luke McMillan, "The Metrics of Space: Tactical Level Design", Gamasutra, 4 Sep 2012, and "The Metrics of Space: Molecule Design", 2013. https://www.gamedeveloper.com/design/the-metrics-of-space-tactical-level-design and https://www.gamedeveloper.com/design/the-metrics-of-space-molecule-design. SNIPPET.
10. [S10] "Designer 01: Project Setup and Level Blockout in Unreal Engine", Epic Games, Unreal Engine 5.8 documentation, undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/designer-01-project-setup-and-level-blockout-in-unreal-engine. OPENED.
11. [S11] Alex Galuzin, "Blocktober: Your Quick Start Guide to Blockouts", World of Level Design, undated. https://www.worldofleveldesign.com/categories/level_design_tutorials/guide-to-blocktober.php. SNIPPET.
12. [S12] "Greyboxing in Unreal Editor for Fortnite", Epic Games, undated. https://dev.epicgames.com/documentation/fortnite/greyboxing-in-unreal-editor-for-fortnite. OPENED.
13. [S13] "From pen-and-paper to blockouts: How level designers craft iconic stealthy encounters", Game Developer, 20 Nov 2023 (author not seen). https://www.gamedeveloper.com/design/from-pen-and-paper-to-blockouts-how-level-designers-craft-iconic-stealthy-encounters. SNIPPET.
14. [S14] Steve Gaynor and Kate Craig, "Level Design in a Day: The Level Design of Gone Home", GDC 2015. https://gdcvault.com/play/1022112/Level-Design-in-a-Day; write-ups at https://gonehome.fandom.com/wiki/User_blog:Pseudobread/GDC_2015:_5_Things_You_Didn't_Know_About_Gone_Home and https://medium.com/@ZacCroslow/the-level-design-of-gone-home-4bcd2cc0e322. SNIPPET.
15. [S15] Harvey Smith (Arkane) and Matthias Worch (LucasArts), "What Happened Here? Environmental Storytelling", GDC 2010. https://gdcvault.com/play/1012647/What-Happened-Here-Environmental; https://www.worch.com/2010/03/11/gdc-2010/. SNIPPET.
16. [S16] Mette Podenphant Andersen (IO Interactive), "Hitman Levels as Social Spaces: The Social Anthropology of Level Design", GDC 2019. https://gdcvault.com/play/1026531/Level-Design-Workshop-Hitman-Levels; slides https://media.gdcvault.com/gdc2019/presentations/MettePodenphantAndersen_HitmanSocial.pdf. SNIPPET. Also Mette Poedenphant Andersen and Jacob Mikkelsen, "Level Design in HITMAN: Guiding Players in a Non-Linear Sandbox", GDC Europe 2016, https://www.gdcvault.com/play/1023872/Level-Design-in-HITMAN-Guiding. SNIPPET.
17. [S17] David Shaver (Naughty Dog) with Robert Yang, "Invisible Intuition: Blockmesh and Lighting Tips to Guide Players and Set the Mood", GDC 2018. https://gdcvault.com/play/1025360/Level-Design-Workshop-Invisible-Intuition; slides http://davidshaver.net/DShaver_Invisible_Intuition_GDC2018.pdf. SNIPPET.
18. [S18] Christophe Carrier (Arkane), "Dishonored 2 PC Interview", GameWatcher, date not seen (about 2016). https://www.gamewatcher.com/interviews/dishonored-2-interview/12695. SNIPPET.
19. [S19] Summary of greybox, art blockout and art production stages, including the Valorant month-long greybox phase, from search results citing The Level Design Book's environment art page and Neil Blevins, "Greybox", Soulburn Studios art lessons, undated. http://www.neilblevins.com/art_lessons/greybox/greybox.htm. SNIPPET.
20. [S20] "Lighting", The Level Design Book, undated. https://book.leveldesignbook.com/process/lighting. SNIPPET.
21. [S21] "Environment Art", The Level Design Book, undated. https://book.leveldesignbook.com/process/env-art. SNIPPET.
22. [S22] Robert Yang, "How to Graybox / Blockout a 3D Video Game Level", Radiator Blog, September 2017. https://www.blog.radiator.debacle.us/2017/09/how-to-graybox-blockout-3d-video-game.html. SNIPPET.
23. [S23] "CubeGrid Tool in Unreal Engine", Epic Games, UE 5.8 documentation, undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/cubegrid-tool-in-unreal-engine. OPENED.
24. [S24] "Geometry Scripting Users Guide in Unreal Engine", Epic Games, UE 5.8 documentation, undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/geometry-scripting-users-guide-in-unreal-engine. OPENED.
25. [S25] "Lyra Geometry Tools in Unreal Engine", Epic Games, UE 5.8 documentation, undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/lyra-geometry-tools-in-unreal-engine. OPENED.
26. [S26] "Level Instancing in Unreal Engine", Epic Games, UE 5.8 documentation, undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/level-instancing-in-unreal-engine. SNIPPET.
27. [S27] "UE4: What are BSP Blockouts in Unreal Engine 4?", World of Level Design, undated. https://www.worldofleveldesign.com/categories/ue4/bsp-02-blockout.php. SNIPPET.
28. [S28] "Level Design Fundamentals: Blockout, Flow, and Visual Guidance in UE5", StraySpark, undated. https://www.strayspark.studio/blog/level-design-fundamentals-blockout-flow. SNIPPET; community source, weak.
29. [S29] "Why are the doors so big in video games? Some developers explain", GamesRadar+, date not seen. https://www.gamesradar.com/why-are-the-doors-so-big-in-video-games-some-developers-explain/. SNIPPET.
30. [S30] "unreal.SpringArmComponent", Unreal Python API 5.6, Epic Games, undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/SpringArmComponent?application_version=5.6. OPENED.
31. [S31] "[UE5] Spring Arm Basics", UhiyamaLab, undated (template values: arm 400, capsule 42 x 96). https://uhiyama-lab.com/en/notes/ue/camera-spring-arm-guide/. SNIPPET. Epic's own "Third Person Template in Unreal Engine" page (UE 5.8, undated, https://dev.epicgames.com/documentation/en-us/unreal-engine/third-person-template-in-unreal-engine) was OPENED but gives no numbers.
32. [S32] "Third Person Camera View in Games: a record of the most common problems in modern games, solutions taken from new and retro games", Game Developer blog, undated in summary. https://www.gamedeveloper.com/design/third-person-camera-view-in-games-a-record-of-the-most-common-problems-in-modern-games-solutions-taken-from-new-and-retro-games. SNIPPET.
33. [S33] "Gameplay Camera System Overview", Epic Games, UE 5.8 documentation, undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-camera-system-overview. OPENED.
34. [S34] John Nesky, "50 Game Camera Mistakes", GDC 2014. https://gdcvault.com/play/1020460/50-Camera and https://www.youtube.com/watch?v=C7307qRmlMI; notes at https://shermanrose.uk/knowledge/programming/games/50-game-camera-mistakes/. SNIPPET.
35. [S35] "Changing the Perspective of the Third Person Camera in Red Dead Redemption 2", Rockstar Games Support, undated. https://support.rockstargames.com/articles/Gz8C860wUX2b8Hin1fxf1/changing-the-perspective-of-the-third-person-camera-in-red-dead-redemption-2; player reports at https://www.nexusmods.com/reddeadredemption2/mods/1657. SNIPPET.
36. [S36] "Capcom Explains Over-the-Shoulder Perspective in Resident Evil 2 Remake", The Nexus, undated. https://nexushub.co.za/nexus/capcom-explains-over-the-shoulder-perspective-in-resident-evil-2-remake.html. SNIPPET.
37. [S37] Piotr Tomsiński (CD Projekt Red), "Behind the Scenes of the Cinematic Dialogues in The Witcher 3: Wild Hunt", GDC 2016. https://www.gamedeveloper.com/design/video-producing-cinematic-dialogue-for-i-the-witcher-3-wild-hunt-i-. SNIPPET.
38. [S38] "Byelaw terraced house", Wikipedia, undated revision. https://en.wikipedia.org/wiki/Byelaw_terraced_house. OPENED.
39. [S39] UK door sizes: "Internal Door Sizing: Are There Standard UK Door Sizes?", Vibrant Doors, undated, https://www.vibrantdoors.co.uk/internal-doors/advice/internal-door-sizing, and "Standard Door Sizes UK", JB Kind, undated, https://www.jbkind.com/info-centre/useful-door-information/standard-door-sizes. SNIPPET.
40. [S40] "Insight: Approved Document M – Accessible Doors", HAG Ltd, undated. https://www.hag.co.uk/briefing-document-approved-document-m-accessible-doors/. SNIPPET.
41. [S41] Shopfront design guides: Brighton and Hove, adopted 8 Sep 2005, https://www.brighton-hove.gov.uk/sites/default/files/migrated/article/inline/downloads/conservation/Shop_Front_Design_SPD_-_Final_Version.pdf; Wigan, October 2005, https://www.wigan.gov.uk/Docs/PDF/Resident/Planning-and-Building-Control/ShopFrontDesignGuide.pdf; Bristol PAN 8, undated, https://www.bristol.gov.uk/files/documents/2683-pan8-shopfront/file. SNIPPET.
42. [S42] "Terraced houses in the United Kingdom", Wikipedia, undated revision. https://en.wikipedia.org/wiki/Terraced_houses_in_the_United_Kingdom. OPENED.
43. [S43] "UK Ceiling Heights by Property Age", Furniture in Fashion blog, undated. https://www.furnitureinfashion.net/blog/uk-ceiling-heights-by-property-age-lighting/. SNIPPET; weak.
44. [S44] Offices, Shops and Railway Premises Act 1963, s.5, legislation.gov.uk, https://www.legislation.gov.uk/ukpga/1963/41/section/5, and Hansard, Lords, 18 Mar 1963, https://api.parliament.uk/historic-hansard/lords/1963/mar/18/offices-shops-and-railway-premises-bill. SNIPPET.
45. [S45] "Offices, Shops and Railway Premises Act 1963", Wikipedia, undated revision. https://en.wikipedia.org/wiki/Offices,_Shops_and_Railway_Premises_Act_1963. OPENED. Workplace (Health, Safety and Welfare) Regulations 1992 and ACOP L24 (11 m³ per person, height over 3 m disregarded), https://www.legislation.gov.uk/uksi/1992/3004. SNIPPET.
46. [S46] Counter heights: "Retail Counter Fabrication", BRAC Projects, undated, https://brac-projects.co.uk/retail-counter-fabrication-heavy-duty-pos/, and "Accessible Counter Heights for Premium Reception Desks Explained", Elite Projex, undated, https://eliteprojex.com.au/accessible-counter-heights-for-premium-reception-desks. SNIPPET; modern.

PROJECT files (read 30 Sep 2026):
- canon.md, lines 13 to 100
- production/research/cab-office-interior-1990/NOTE-2026-09-30.md and NOTE-2-2026-09-30.md
- production/research/cab-office-1990/SUMMARY-2026-09-28.md
- production/research/atlas-01/MICKEYS.md (superseded pub proposal)
- production/art/facades/2026-09-24-measured/east_parade-drawing.json
- ue-probe/Source/LedgerProbe/Private/SliceCharacter.cpp and LedgerCharacter.cpp (camera arm values)
- production/audits/2026-09-30-adversarial-audit.md, line 26
