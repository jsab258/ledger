# Prior research inventory: DECISIONS.md, RULINGS.md, canon.md

> Correction by the main session (23 Nov): "Tom cannot die" is his ruling of 12 Oct, recorded in production/archive/DECISIONS-to-2026-11-09.md (13 Oct 02:45) and carried by the combat options paper of 17 Nov and end state A of 18 Nov; RULINGS.md's shortened text no longer spells it out. Where this sheet calls it unverified, read it as holding.


## 1. Header

- Slice: /home/claude/wip/DECISIONS.md (618 lines, 43,785 words, the live log from 9 Nov 2026 to 22 Nov 2026 04:12), /home/claude/wip/RULINGS.md (4,900 words, his rulings in force), /home/claude/wip/canon.md (2,137 words). Read in full on 23 Nov 2026. Three files.
- Important limit: DECISIONS.md is only the log since 9 Nov. Everything before that (July to 9 Nov: the casting, period, streets, light, props and clothes choices) is in production/archive/DECISIONS-to-2026-11-09.md (about 142,000 words) and DECISIONS-to-2026-09-24.md in the same folder. Neither was in this slice and neither was read. The live log's header says that archive is "searched with grep, never loaded whole".
- What the live log is mostly: about nine tenths of its lines are tooling (Kiln cloth tool, hair tools, disk space, start gate, pace line, helpers, licences of tools). Those are skipped under the brief. The setting, place, system and reference-game decisions are indexed below.
- Date format below: day and month 2026. The "who" column says "his ruling" only where the log says his words or his pick; "session" means the production session; "lane" means the cloud lane session; "advisor N" means his words relayed by the advisor channel.

## 2. Index: one line per decision

Format: date | decision | who | still holds | groups | parts | lane

### 2a. Reference games, studies and how quality is judged

- 17 Nov | Other games studied from the outside only (browser footage, developer talks, published analysis); never decompiled, files opened, protection bypassed or videos downloaded; earlier reading of game files stopped | his ruling (advisor 214) | yes (RULINGS 17 Nov line) | 7, 8 | no part (method); 7.13, GD-01 to GD-08 inform | lane: repeated (the lane studies footage only)
- 17 Nov | Study Q2: no tool injected into a running game (UE4SS); published figures and outside timing fill gaps; PresentMon allowed as a measuring tool on his PC, never shipped | session under his 11 Oct ruling; his tap 19:36 | yes | 8 | 8.1.1, GD-01 | lane: no part
- 18 Nov | KCD2 is the bar; GTA V for why people play long; Mafia only a period Unreal study, never the yardstick | his ruling (advisor 229) | yes, RULINGS 17 Nov | 4, 5, 7 | 4.1.1, 5.10, all OUTSIDE visual rows | lane: repeated
- 20 Nov 14:30 | Mafia dropped as a reference; reference games are KCD2, GTA V, RDR2; Mafia kept only as a study of how Unreal is used | his ruling (advisor 269) | yes, RULINGS 17 Nov | 7 | FIT-F04, 4.x | lane: repeated (FIT-F04 says "GTA IV in Mafia DE's place", consistent)
- 20 Nov | GTA VI studied first, its higher bars kept beside the reference games' (the higher wins); 21 Nov story of GTA VI may be studied but no spoiler reaches anything he reads | his rulings (advisors 281, 283) | yes | 3, 7 | 3.1.x, 7.x | lane: repeated
- 20 Nov | Quality judged first on real reference data; an AI judge's score counts only once checked against it | his ruling (advisor 277) | yes, RULINGS 13 Nov line | all | all | lane: repeated (design proof method)
- 20 Nov | Steam review study redone from this PC: GTA V 10,334 reviews, RDR2 10,154 (5 pull kinds, monthly fill). Praise top three unchanged: story, world, looks. Complaints led by a bad PC version and bugs, level across the games, PC version first in each Rockstar game; slow controls close behind in RDR2. Coder hit 61 and 58 of 100 hand-read, praise order 0.83, punish 0.48 pooled | advisor 271, session | yes (a reviewer passed it with 16 wording fixes) | 7, 5 | 7.2, 7.3, GD-05, GD-07 | lane: repeated (the players study is the lane's own)
- 20 Nov | Walkthrough Steam study for six more games (Sleeping Dogs DE 307690, GTA IV 12210, L.A. Noire 110800, Hitman WoA 1659040, Watch Dogs Legion 2239550, Forza Horizon 4 1293830), seven Steam pulls at 20 a month a vote; Mafia DE skipped; The Getaway never on PC and Driver San Francisco delisted, both not reached; "moving on foot" not measurable (precision 0); results shown with hand precision and recall | advisors 273, 274 | yes | 1, 7 | 1.1.1, 1.2.x, GD-04 | lane: partly repeated (lane names L.A. Noire, Sleeping Dogs in A2, A6; the two unreachable games are not flagged in MEASUREMENTS-NEEDED)
- 19 Nov | Driving reference shortlist approved: GTA V, GTA IV, Sleeping Dogs, Mafia DE, Watch Dogs Legion, The Getaway; contrast Forza Horizon 4, Driver San Francisco | his ruling (advisor 249) | partly: Mafia DE struck 20 Nov; Getaway and Driver unreachable 20 Nov | 1 | 1.2.1 to 1.2.4 | lane: contradicted in part (1.2.4 still says "fragile like The Getaway" as a standard, but the Getaway has no PC footage path found)
- 21 Nov | GTA VI driving M1 to M3 set aside after two tries: no speed on its HUD (dash timing behind a pickup; a covered first-person dial); GTA V's sheet stands in; a third route only with a clip filmed for speed | session | yes | 1 | 1.2.1, FIT-G2 | lane: unknown (lane's 1.2.1 says PENDING on M1 to M9; does not say the GTA VI rows are void)
- 21 Nov 22:41 | Footage studies' open questions repriced to about 37 h (0.15 to 0.3 h a sample); marked not needed: defuse, GTA VI M1 to M3, GTA IV-like weight, Like a Dragon, district size, port-town Q3, Q4, Q7, C4 distance, further guide reading; total block about 141 h, finish near 11 Dec at 7 h a day | session (advisor 302) | yes | 7 | GD-01, 4.2.x | lane: partly repeated (district size and port-town questions are not needed per this entry; lane still lists GD-01 travel time as PENDING)
- 22 Nov 00:38 | YouTube frames do not decode in a scheduled run with no window on screen; every next measuring piece needs them | session | yes (open) | 7 | all PENDING feel rows | lane: no part (this is a blocker for section 5 of the lane's plan)

### 2b. The game's shape, clock, camera, scale

- 21 Nov 09:48 | Clock: 60 real seconds a game hour; the game is about 7 game weeks; Act II about 5 game weeks | his ruling (advisor 287) | yes, RULINGS prototype line | 7, 2 | 7.13, 3.1.2, FIT-F13, FIT-F24, RT-04, RT2-21, CLK-01 to CLK-07 | lane: CONTRADICTED (7.13 still PENDING at 45 s; FIT-F24 and RT2-21 say nine weeks; RT-04 says sit-down by week eight)
- 20 Nov | Prototype clock 45 s and Unreal LiveClock.h 30 s disagree; recorded as a finding for him | parts-tree session | replaced by 21 Nov ruling above | 7 | 7.13 | lane: contradicted (coverage keeps the 45 s as the working value)
- 28 Oct and 21 Nov 07:58 | Camera: Between picture height, pulled back 3.1 m so feet show; field of view now a player setting 75 to 100, default 86 (was fixed 86) | his ruling, advisor 284 by his leave | yes | 5, 6 | 1.1.2, 5.8.1, AX-03 | lane: ignored the change (1.1.2 says "86 degree lens"; AX-03 lists field of view only as an effect to switch off)
- 28 Oct | Release: one full release late 2027; 15 to 20 hours; map the Hook plus the docks; docks cut first if time runs short | his ruling | yes | 7, 10 | 10.2, OUT-05 | lane: repeated
- 21 Nov | Real players play the browser evening before Unreal once it meets the measured bar; his friends, verdicts beside his and the AI panel's | his ruling (advisor 293) | yes | 7, 10 | 7.2, 10.3 | lane: repeated
- 20 Nov and 21 Nov | One-shot starts only on a complete blueprint (all measurements done, DESIGN-COMPLETE design gate, his yes on the measured story); he plays only after the one-shot; live voices via his PC's Pocket voices through a local helper | his rulings (advisors 279, 289, 298, 299) | yes | 7, 8 | 7.1, 5.6.2 | lane: repeated
- 16 Nov | Scale test (street copies laid along the Hook's road lines, test only, never shipped) is measurement, not multiplication; 10 copies fit inside the Hook; a walk through all is about 1.4 km out and back along dead ends, so the measured walk uses the three nearest slots, 422 m | session | yes | 4, 8 | GD-01, GD-02, 4.1.2, 8.1.1 | lane: no part (the lane has no street-length figure)
- 17 Nov | Scale ladder measured packaged: card memory 4,050 to 4,430 MB at 1 street length, 4,195 at 2, 4,216 at 4, 4,920 to 4,955 at 10 (about 100 MB per street length); frame median 14.0 to 14.3 ms, card 12.5 to 12.7 ms (+0.2 ms over nine lengths); one spike at N=10 (1% slowest 22.75 ms). A copy is 2,421 meshes, 4.05 M triangles, 37.6 MB of pictures; 180 lights added at N=10 | session, measured | yes | 8 | 8.1.1, 8.1.2 | lane: ignored (8.1.1 cites only the 6 GB line and 1.7 ms)
- 17 Nov and 16 Nov | Card memory packing: Lumen at Epic's High (surface cache atlas 3584, probe resolution 16) saves about 186 MB at no frame cost; run-time pictures compressed at staging 4.6 to 3.8 GB standing; peak 4,984 MB (median 4,669) on 17 Nov 01:55; one run's median frame 18.44 ms vs 14.86 spoiled by a second session | session | yes (decision stands; later perf lines not in slice) | 8 | 8.1.1 | lane: ignored

### 2c. Place: Meridian, the Hook, Quay Street, the docks, buildings, light and weather

- canon (8 Sep, 22 Sep, 23 Sep) | The built street is Quay Street in the Hook; Mickey's stands on it; east side is the six-bay parade; the west block across from the north half of the parade has shops; the west block across from Mickey's at the quay end is plain terraces; asset names east_parade_* are names only | his ruling | yes (canon) | 4 | 4.1.1, 4.3.1, 4.3.3 | lane: partly repeated (4.1.1 cites "canon's three sides")
- canon (19 Nov, his ruling on the audit L1) | The docks are the Hook's working waterfront | his ruling | yes | 4 | 4.2.1 to 4.2.4, OUT-05 | lane: repeated
- 3 Oct (RULINGS) | Trades on the parade: bay 1 fishmonger, bay 3 empty unit to let (whitewashed), bay 4 launderette, bay 5 grocer; west_north a newsagent and tobacconist, an ironmonger, a tea room; east_chandler a ship's chandler; pawnbroker's window lit at night; 22 Oct Rita's front is the sample; 8 Nov fishmonger and empty unit built in phase 2 | his ruling | yes | 4 | 4.3.3 | lane: ignored (4.3.3 is OUTSIDE with a generic standard; the trade list is not cited)
- 17 Nov 19:03 | Mickey's front room is a working minicab office (dispatcher Zlata, quay-cast.json) and is lit at night; only Mickey's inner office stays locked and dark; Sheila keeps the key | session, from canon | yes | 4, 5 | 4.3.1, 5.4.2 | lane: ignored
- 16 Nov 18:37 | Brick target: course pitch 86 mm from one dated photograph (Levenshulme 1994, Victorian imperial brick); occasional darker overfired headers, 20 to 35% clustered, no chequer, no gloss (Hull 1982 and 1986 photographs); the kit's 225 x 75 geometry grid stays | session (reviewed, pass with fixes) | yes | 4, 5 | 5.3.2, 4.1.5 | lane: ignored (5.3.2 says only "calibrated to real reflectances")
- 16 Nov 23:24 | Photographed Flemish tile (cut from CC0 scan brick_wall_006, 198 donor bricks) went into the game; covers 2.72 m; a drawn Flemish tile failed two tries (reads newly built and CG; today's scan wins) | session, fresh reviewers | yes | 5 | 5.3.2 | lane: ignored
- 17 Nov | Wear checks against Mafia's counts: launderette marks 7 vs Mafia's 6, burnt window 0.08% (limit 1%), night fascia ratio 2.58 (floor 1.3); grocer 1.73% clipped, passed; brick spread 61% across a bay vs 15% top is a known shortfall; street-level wear to x 48 and dark gable feet added; held for his batched look | session | partly: the yardstick is Mafia, which RULINGS of 20 Nov says is never a reference | 5 | 5.3.2, 5.3.3 | lane: ignored; see section 4
- 16 Nov 18:40 | Street width check joins ci; the street's ends check stays report-only (cam_A 9/21, cam_hook 9/21, cam_reverse 5/21 closed) until the ends are designed; how the quay end closes is taste and goes to his page | session | yes (open question) | 4 | 4.1.1, 4.1.5 | lane: ignored
- 16 Nov | Hill camera placed from the atlas's climb: x 52 to 72, 8 m east, 1 in 12; the office's fixed camera cam_office is the staff view behind the counter, 60 degree room lens | session | yes | 4 | 4.1.2, 4.3.1 | lane: no part
- 5 Oct and 7 Oct (RULINGS) | Atlas-01 is the town's map, updated to the built street: 48 m long, its climb, its bend east behind the parade at the far end | his ruling | yes | 4 | 4.1.1, 6.3 | lane: ignored
- 29 Oct, 3 Oct, 5 Oct, 7 Oct, 1 Oct (RULINGS) | Day exposure one stop darker, never brightened; wet street dark, glistening, mirroring sky; hill built not hazed; weather a grey range (dry overcast, drizzle, rain), never sunshine in the friends' build, rain changes who is out; day and night now, four or five states later, no moving sun; night is pools of lamp light with darkness between | his rulings | yes | 4, 5 | 4.7, 4.8, 5.3.3, 5.4.1, 5.4.2 | lane: repeated (4.7, 4.8 MEASURED on these rulings)
- 2 Oct, 22 Oct (RULINGS) | No skip or pallets until real; the KX100 phone box stays; lamp columns stay concrete, staining to finish; poll-tax posters an invented local campaign, no real parties | his rulings | yes | 4 | 4.4, 4.9 | lane: ignored
- 19 Nov 09:11 | Out-of-period placeholder (elizabeth-idle: striped top, jeans, red heels) removed from Mickey's window and one crowd voice with her; Martha, Kate and Leonard stay | session, audit M2 | yes (passes only once the packaged build shows the window empty) | 3, 5 | 3.2.4, 5.1.5 | lane: ignored
- canon | CCTV rare: the bank and a second site that is Jafar's to name; tape recycled weekly; one camcorder in town as a rare witness type; no internet, no mobiles; pagers for dealers and fixers | his ruling | yes | 2, 4 | 1.4.1, 4.9 | lane: ignored (4.9 cites only the brand bible's owed list)
- canon | Seven districts: the Hook, Copper Row, the Exchange, the Parade, Fairview, Ironside, Gullwing; tags TANNER, SNIDE, GULL, QUAY FIRM, PARADE RATS are wall names; pubs boarded or serving food, never entered for drink; the school stands closed | his ruling | yes | 4 | 4.9, 4.10, OUT-05 | lane: partly repeated (4.10 cites pubs and school)

### 2d. People, casting, cast voices, calendar

- 11 Nov and 17 Nov | Cast bodies: the three build bodies had been one body (Walter preset) since 29 Sep; replaced by cast bodies (heavy Ron P2, slim Darren S6, average Tom); 16 Nov four standard bodies in F:/LedgerTools/bodies/standard-2026-11-16 | session | yes | 5 | 5.1.2 | lane: repeated (5.1.2 OUTSIDE)
- 25 Sep, 30 Sep, 8 Oct (RULINGS) | Faces frozen: Ron P2, Sheila S4 with its hair, Darren S6 with Epic's short cut, Tom L1; the other eleven casting sheets approved as text, faces cast in MetaHuman from them | his ruling | yes | 3, 5 | 3.2.1, 5.1.1 | lane: repeated
- 3 Oct to 19 Nov (RULINGS) | Voices: Sheila p267, Ron p227 on Pocket; Darren VCTK p286 (Newcastle); Agar p226; dispatcher p280; Danny p243, June p277, Father Walsh get a listening page, cast only on his yes; Pocket kept, consent risk his; Tom is not voiced | his rulings | yes | 5 | 5.6.1, 5.6.2 | lane: repeated
- 18 Nov | Hair: Tom's pale crown stays a listed known fault (step 0 measured it, day 110 to 130, night 119 to 117); no hair skill until one character's hair passes the full gate | session; his 3 Nov ruling | yes | 5 | 5.1.3 | lane: repeated (OUTSIDE)
- 17 Nov | Ron's routine and talk exist and pass the simulation tests; his walk to the landing at eleven waits until the office exit passes packaged; the casting sheet's "forty years" line stays (editing ends its approval) | session | yes | 3 | 3.2.1, 3.6.3 | lane: ignored
- 18 Nov | Every live talker gets "Your usual week" (derived from the routine in the cast file) beside this hour's place so Ron can say where he will be tonight; the claim check accepts it as the speaker's facts; eight talk tests | session | yes | 3 | 3.6.1, 3.6.2 | lane: ignored
- 16 Nov | Talk bench: all twenty held newcomer questions go to the small-talk model on the bench (median first sentence 1.81 s, 32 of 60 under 2.0 s, worst 16.1 s); Sonnet 5.5 low thinking 1.89 s vs Sonnet 5 2.33 s median first sentence; 26 of 60 replies came back empty with no thinking field | session, reviewed | yes (the bench result; in the game some questions go to Sonnet 5) | 3 | 3.6.1 | lane: ignored (3.6.1 states the 2 s bar but cites no measured median)
- 20 Nov | Story loop: cloud Fable writes STORY-BIBLE versions with three fresh readers (stop when three score 9 or more, none under 8, a fourth confirms); first reader scores were 4, 5, 4 of 10; changes no canon; reaches him as at most three decisions; nothing built until he rules | his order (advisor 270) | yes (running) | 3 | 3.1.x, RT-01, RT-02 | lane: repeated (lane's story measure)
- 20 Nov | Calendar: Thursday market in Copper Row, Saturday match, Sunday; Bonfire Night as an adults' display on the quay; Remembrance Sunday at the chapel; no real people or news | parts-tree session (within canon) | yes | 2 | 2.1.6 | lane: repeated
- 20 Nov | New minor people to be minted within canon: two bought constables (A13), a retired doctor by the quay who stitches and remembers (A21), the other minicab firm's owner (A14); whether DS Ellis can be bought is left to him | parts-tree session | yes (names owed) | 3 | 2.6.8, 2.15.3 | lane: repeated (2.6.8 MEASURED, 2.15.3)
- 20 Nov | Time with Alison or Danby plays as visits Tom chooses, no score; the paper prints only what Alison knows, twice a week | lane | yes | 3, 2 | 3.2.5, 2.4.5, 3.2.7 | lane: repeated
- 20 Nov | Tom is not voiced; pad play by suggested lines and an on-screen keyboard | parts-tree session | yes | 6 | 3.6.8, 6.6 | lane: repeated

### 2e. Clothes

- 11 Nov | Tom: his answer "no" (face and hair good; boots read as rubber slippers, jacket no cloth texture, jeans no denim); three tries on surfaces failed; rows restored; jeans, jacket, boots stay at the morning look as known faults | his answer, session | yes | 5 | 5.1.4, 1.6.10 | lane: ignored (5.1.4 gives the floor only)
- 11 Nov | Sheila: cardigan beige (linear 0.38 0.29 0.17), blouse cream, skirt brown wool; skirt as Chaos cloth, free up to 8 cm at the hem, 480 triangles (Kingdom Come II's skirt proxy is about 270); shoes a flat derby, 16 mm sole, four eyelet pairs; blouse hem lump 11.8 mm and collar strips listed shortfalls | session | yes | 5 | 5.1.4 | lane: ignored
- 16 Nov to 19 Nov | Ron's outfit: donkey jacket and work trousers from FreeSewing Titan (seat ease 11%, knee ease 10%, hem about 460 to 480 mm, 25 mm break); trousers read black to charcoal (tint an estimate, his look); crotch hangs low; seated right hem rides up showing bare ankle in 158 of 169 frames; trousers and jumper re-cleared are held rows only (-WearHeld), release waits on the legs' rework; the release call is his look since they replace the jeans he passed on 8 Nov | session | yes (not released as of 20 Nov) | 5 | 5.1.4 | lane: ignored
- 16 to 18 Nov | Breadth set: Ron's donkey jacket and work trousers, Sheila's pleated skirt, Darren's nylon jacket; knee coat from FreeSewing Jaeger (back vent, three-piece collar), tails cloth in Kiln but rigid-body bones in game as Mafia's do (30-body asset on a tailed jacket); "period look thin: no 1988 to 92 catalogue reached, unverified" | session | yes | 5 | 5.1.4 | lane: ignored; see gap in section 6
- 20 Nov | Kiln, hair and the crowd pause after the Marvelous export until the browser prototype's evening holds; Marvelous export done 21 Nov (52 .zprj, 104 MB pattern JSON and garment FBX) | his ruling (advisor 277), session | yes | 5 | 5.1.4, 5.1.5 | lane: repeated (clothes OUTSIDE)
- 30 Oct (RULINGS) | Tom wears black lace-up boots like Ron's with dark laces and sole, under his jeans | his ruling | yes | 5 | 1.6.10, 5.1.4 | lane: ignored (1.6.10 says three outfits, no boots)

### 2f. Vehicles and cars

- 17 Nov 20:57 | Cars: parked first, traffic from their kit in the friends' build after one passes, an arcade car once the map grows, AAA driving the end state costed to him first | his ruling (advisors 208, 209) | yes | 1, 4 | 4.5.1, 4.5.2, 1.2.1 | lane: repeated
- 18 Nov 12:53 | Driving: fun first as non-sim open-world games; 1990 by sound, sway, look, relative speed; real figures a floor; game-band targets; automatic gearbox (a prior copy defaulted to manual; fixed 18 Nov 21:22 round 3) | his ruling (advisors 222, 223) | yes | 1 | 1.2.1, 5.5.5 | lane: repeated in part (1.2.1 set M1 to M9 are "game set" figures; check against "real figures a floor")
- 18 Nov 22:07 | A car hurts badly and never kills; only the player's car strikes; AI drivers always brake; stop and help or drive off and be chased | his pick (advisor 234) | yes, canon | 1, 2 | 1.2.5, 4.5.1 | lane: repeated
- 18 Nov 16:08 | Combat end state A, guns rare and late, AAA when used, an escalation dial once guns exist; no suppressed .22 | his ruling (advisor 226) | yes | 1, 2 | 1.3.10, 2.13, RT-10, RT-12 | lane: repeated
- 20 Nov 07:54 | Hold-ups of shops and people are in, rare and late through the dial, loud, always witnessed and remembered, heavy consequences through witnesses, police and talk, never a game over | his YES (advisor 263) | yes | 1, 2 | no row of its own; 1.3.10, RT-09, 2.5.3 mention it | lane: ignored (no part for the hold-up verb; see section 4)
- 17 Nov 16:24 | Parked cars plan: our own lofted body from car-model.py, 25 to 41 h for the first car against the order's 12 h | session | yes (costing) | 4 | 4.5.2, 4.6.1 | lane: ignored
- canon | Every vehicle fictional; no real car models | his ruling | yes | 4 | 4.6.1 | lane: repeated

### 2g. The town's systems and numbers (parts-tree decisions of 20 Nov, all "he overturns any he disagrees with")

- 20 Nov | Hiding is standing still in shadow, turning away, being among people or behind things; no crouch, no stealth mode | parts-tree session (A1) | yes | 1 | 1.1.5, 1.4.2 | lane: repeated
- 20 Nov | Tails never fail on a hidden distance; being made shows a doubt first; foot pursuit uses the police's own losing rule (7 s unseen or 70 m) for runners | parts-tree session (A2, A3) | yes | 1 | 1.1.6, 1.5.1, 1.5.2, FIT-F03 | lane: repeated (1.5.1 cites 7 s or 70 m)
- 20 Nov | Searching has a time and a noise per container, no puzzle; a safe needs its key or combination from a person; two things under the coat, one in the hand, the rest at the office | parts-tree session (A4, A5) | yes | 1 | 1.6.2, 1.6.9, 1.6.6 | lane: repeated
- 20 Nov | Finding the way: addresses and name plates, people give the way by landmark, a fare says "left here", one nudge after 90 s lost, a passer-by after 3 min | parts-tree session (A9) | yes | 6, 4 | 6.9, 4.1.3 | lane: repeated (ER-JOB-01 3 minutes)
- 20 Nov | Street manners on one key (nod, greet, hard look, shove); stopping verbs (sit, lean, smoke); every place labelled public, open by hours, private or forbidden | parts-tree session (A10) | yes | 1 | 1.1.7, 1.4.7 | lane: repeated
- 20 Nov | Tom never walks into the dock; cars cannot leave the quay; a man put in the water climbs out within a minute; water never kills | parts-tree session (A11) | yes | 4 | 4.2.4 | lane: repeated (but 4.2.4 says "Tom cannot die (his ruling)": see section 4)
- 20 Nov | One patrol car; stops only for reckless acts seen by an officer; caution and plate noted, no fines; two named officers can be bought, each with a limit; charges join Ellis's case, no court scene or prison; one office search with a sign the evening before | parts-tree session (A12, A13) | yes | 2 | 2.6.7, 2.6.8, 2.6.9 | lane: repeated
- 20 Nov | The firm grows through cars, drivers, ranks and accounts; one other minicab firm as a business with a new minor owner, never a fourth rival; fronts and rounds run through a named man each | parts-tree session (A14, A15) | yes | 2 | 2.15.1 to 2.15.3, 2.17 | lane: repeated
- 20 Nov | A follower keeps about 2 m, rides, counts as one more man in a fight; jobs reach Tom in person, by message with Sheila or Pauline, by the office phone, or a man by the car | parts-tree session (A16, A17) | yes | 1, 3 | 1.7.4, 3.5.7 | lane: repeated
- 20 Nov | Street happenings: authored library by state and hour, never dice; none twice in 30 min; calendar; spending lists per shop; a second coat breaks the mark rung; a barber; marks of a beating last three game days | parts-tree session (A18, A20, A21) | yes | 2, 3 | 3.7, 2.12.5, 1.6.10 | lane: repeated
- 20 Nov | Stopping to help is a phone call; an ambulance in about ten game minutes | parts-tree session (A22) | yes | 2 | 2.18 | lane: repeated (2.18 UNMEASURED but this fixes the figure)
- 20 Nov | Casing, drawing a watcher away by noise, a quiet blow from behind, yard dogs that bark and are never hurt; riding as a passenger with a skip; Shaun's respray stops old sightings naming the car | parts-tree session (A23, A24) | yes | 1, 2 | 1.6.11, 1.4.8, 1.2.8, 4.11.1, 1.2.9 | lane: repeated
- 20 Nov | After the ending: a short close, credits, then free play; music from places, a score only under cut scenes, act ends and the close, never on a fight or chase; hour from Tom's watch on a key, street clocks and the chapel bell | parts-tree session (A7, A8, A31) | yes | 6, 5 | 7.15, 5.7.1, 6.1.5 | lane: repeated
- 20 Nov | Fight defence: a guard key, a slip, a counter after a guard or slip, breath not a stamina bar, a grab that pushes or disarms, fighter types per fight, no cue on screen; quiet walk halves footstep reach; haggling at most three spoken offers; lifting from a pocket only an authored key, letter or wallet | parts-tree session (A29, A30, A34) | yes | 1 | 1.3.1, 1.3.2, 1.3.12, 1.6.13, 2.2.4 | lane: repeated
- 20 Nov | Vaulting at set places, taking parked cars, and one boxing club built to the recommended answers meanwhile | parts-tree session on his three questions; confirmed by him 20 Nov (A26, A27) | yes | 1 | 1.1.8, 1.2.10, 7.16 | lane: repeated (1.1.8 still PENDING on "Q1 (open)" but he confirmed vaulting 20 Nov: stale)
- 20 Nov | Parts tree: ten groups, 354 parts, 295 buildable, 957 old checklist items hung under parts, 116 ruled out; 289 reference mechanics mapped: 251 onto parts, 12 became nine new parts (horn, torch, pocket lifting, damage by hand, police after a deed, a street on edge, finding an unseen deed, calling on people, crew pay), 26 not for LEDGER | lane | yes | all | 1.2.11, 1.6.12 to 1.6.14, 2.5.4, 2.5.5, 2.6.10, 3.2.7, 2.11.4 | lane: repeated (these are the lane's rows)
- 20 Nov | Economy: one edition, no paid outfit or car packs (district updates as ruled 28 Oct) | lane | yes | 7, 10 | 10.6 | lane: repeated
- 19 Nov | Whole-game design approved ("the vision" and "the whole game"); cab fares few and chosen, each a person with something going on, tested in the prototype first | his ruling (advisors 242, 243) | yes, canon OPEN 3 | 1, 3, 7 | 3.4.1, 3.4.2 | lane: partly repeated
- 18 Nov | Pillar: verbs first, talk the consequence; "not a gossip simulator: an exciting, immersive, novel game"; about ten distinct activities per thirty minutes; nothing new for at most about five minutes; talk well under half of play | his ruling (advisors 224, 226) | yes, canon | 7 | 7.5, 7.6, 7.12 | lane: repeated
- 21 Nov | Tester walk: the T talk key needs plain sight, not distance only (Sheila behind the kiosk) | session | yes | 1, 3 | 3.6.1, 1.4.1 | lane: no part

### 2h. Sound, music, animation, technical choices that touch the look

- 12 Nov, 17 Nov | CMU motion capture on the licence list (moves inside the game, never resold); CMU retarget measured: slide passes 6 of 6 (0.3 to 1.1 cm over source), flips 0 of 6, height 3 of 6, knees 1 of 6; bent knees on 131_01 and 113_15 left a listed shortfall; Pexels 6615631 (sit to stand, plain studio) kept as a control clip | his rulings, session | yes | 5 | 5.2.1, 5.2.7 | lane: repeated (5.2.7 cites sources)
- 11 Nov | A seated person asked to walk plays the stand-up clip then walks (Kingdom Come II plays an exit clip) | session | yes | 5 | 5.2.3 | lane: ignored
- 18 Nov | Special Elite (Apache 2.0) font for the browser prototype only, never shipped; three.js, esbuild, acorn, puppeteer-core on the allowlist for the prototype only | his yes (advisor 231) | yes | 6, 8 | 6.x, 10.4 | lane: no part
- 17 Nov | Sound reach figures are the lane's own (DESIGN); nothing in this slice measures footstep, door or car reach | n/a | n/a | 2, 5 | 2.2.4, 5.5.x | lane: no overlap
- RULINGS 28 Sep, 23 Sep, 1 Oct | Thinking sound with a glance before an answer, cut when the answer starts, no loading sign; subtitle only with its audio; live lines' mouths follow loudness; prepared lines use Epic's audio-driven mouths | his rulings | yes | 5, 6 | 5.2.4, 5.6.3, 6.1.2 | lane: repeated

## 3. What we already know, by group

Group 1, what the player does with his hands
- Camera: Between picture height, 3.1 m back so his feet show, head level with the street's far end; lens setting 75 to 100, default 86 (RULINGS 28 Oct, 21 Nov; DECISIONS 21 Nov 07:58). Closer for talk and low rooms, wider for fights.
- Cars hurt, never kill; only the player's car strikes; automatic gearbox; fun first as non-sim open-world games; 1990 by sound, sway, look, relative speed (canon 18 Nov; RULINGS 18 Nov; DECISIONS 18 Nov 12:53, 22:41).
- Fists knock a man out, never kill alone; only a fall on kerb, wall or step after a blow can kill, rarely, and the town remembers it (RULINGS 30 Oct; canon content rule). Guns rare and late, dial, hold-ups in as rare late dial events (RULINGS release Combat line).
- No jump; coat, pockets and office storage (two things under the coat, one in hand); no lockpicking game; vaulting at set places; taking only parked cars (DECISIONS 20 Nov A1 to A27).
- Foot pursuit loses at 7 s unseen or 70 m; tails never fail on a hidden distance (A2, A3).

Group 2, the town under the hood
- Everyone perceives, remembers and gossips (RULINGS D25); witnesses talk quieter for an hour after a deed (RULINGS 23 Sep); a threat stops a report to the police, never the street's talk (3 Oct); Mickey's people never go to the police about one of their own (1 Oct).
- Witness certainty: a noise or shape is suspicion, never "he did it" (30 Sep).
- Calendar and happenings: Thursday market in Copper Row, Saturday match, Bonfire Night adults' display on the quay, Remembrance Sunday at the chapel (20 Nov A20). One patrol car, no fines, two bought constables (A12, A13). Ambulance about ten game minutes (A22).
- Clock 60 s a game hour, about 7 game weeks, Act II about 5 (21 Nov). That is about 24 real minutes a game day and about 19.6 real hours across 49 days, which fits the 15 to 20 hour release length (RULINGS 28 Oct).

Group 3, story and people
- Canon cast, ages and names (Tom Nowak 32; Ron Kirby 58; Sheila Dunn 53, at Mickey's since 22; Darren Milner 25; the three rivals Geoffrey Agar, Maureen Jensen "the Widow", Danny Cammack; DS Carol Ellis; Alison Sedman; Philip Danby; Father Brendan Walsh; Keith Garbutt; June Suddaby) (canon.md). Sheila withholds his name until she trusts him.
- Mickey died of his heart at the office early one morning, Ron found him; the warehouse fire is a street fact; winding the business down ends his arrangement (RULINGS 30 Sep).
- Thirty regulars stand as written; own street lines for Ron, Darren, Father Walsh, June; shared ones for Sheila, Alison, Ada; neighbours' talk at most every 45 s; only regulars who knew Mickey describe him in two approved lines (RULINGS 30 Sep).
- Story: one main story with two or three endings; outline and first week's nine designs to be re-measured, nothing final until he approves the measured story; under RDR2's bar on 28 Nov: small gap built on, large gap his call (RULINGS 28 Sep, 20 Nov, 21 Nov).
- Live talk: bench medians 1.81 s (Haiku, small talk) and 1.89 to 2.33 s (Sonnet class) to first sentence on newcomer questions; 26 of 60 replies empty when thinking field omitted on Sonnet 5.5; the game's own router sends newcomer questions to Sonnet 5 (DECISIONS 16 Nov 10:25 to 13:08).

Group 4, the place
- Quay Street in the Hook, 48 m, its climb, bend east behind the parade; three sides; docks are the Hook's working waterfront (canon; RULINGS 5 Oct).
- Brick: 86 mm course pitch, 20 to 35% darker headers, photographed Flemish bond, 2.72 m repeat (DECISIONS 16 Nov 18:37, 23:24).
- Mickey's: front room is the working cab office, lit at night; inner office locked and dark, Sheila has the key (17 Nov 19:03); 1990 cab-office wear and clutter: radio set, ashtrays, kettle, telephone, scuffed counter, real glass reflecting the street (RULINGS 4 Oct).
- Shops list by bay (RULINGS 3 Oct). Poll-tax posters an invented local campaign (3 Oct).
- Street scale: about 100 MB of card memory per extra street length, +0.2 ms over nine lengths; ten copies fit the Hook; walking all is about 1.4 km (DECISIONS 16 and 17 Nov).

Group 5, how it looks and sounds
- Day exposure one stop darker, never brightened (RULINGS 29 Oct). Grey weather range only, no sunshine in the friends' build (5 Oct). Night is pools of lamp light (1 Oct).
- Faces frozen for Ron, Sheila, Darren, Tom; voices (RULINGS). Clothes floor: plain, period-plausible, no modern giveaways such as contrast-stitched slim jeans or trainers (RULINGS 3 Oct).
- Wet street bars, window frames, hill built not hazed (RULINGS 3 Oct).
- Per-person clothes known: Sheila beige cardigan, cream blouse, brown wool skirt; Ron donkey jacket, work trousers (held), Tom lace-up boots, jeans and jacket (DECISIONS 11 Nov, 16 to 19 Nov).

Group 6, interface and the Ledger
- No minimap, waypoints or markers; paper map and street signs; no timers on screen; the hour from a watch key, street clocks and the chapel bell (RULINGS D27, D30; A31).
- Suggested lines on Tab, on screen at once for a controller; Tom's written lines approved (RULINGS 1 Oct).

Group 7, the game's shape
- Release late 2027, 15 to 20 hours, Hook plus docks, docks cut first if short (RULINGS 28 Oct). 28 Nov story gate. Real players on the browser evening before Unreal (21 Nov).
- Reference games: KCD2 the bar, GTA V and RDR2, GTA VI measured first; Mafia never (RULINGS 17 Nov, 20 Nov).
- Players study: GTA V 10,334 and RDR2 10,154 Steam reviews coded; praise story, world, looks; complaints PC version and bugs, then slow controls in RDR2 (DECISIONS 20 Nov 16:55).

Group 8, technical
- 60 fps at 3440x1440 on the RX 6700 with the voice running, never below 30; the 6 GB card line is the game alone; 1.7 ms spare accepted (RULINGS 23 Sep, 24 Oct).
- Scale ladder and Lumen High figures in section 2b.
- Live talk names no real make, brand, shop, club, programme, paper or public figure and nothing after 1992 (RULINGS 29 Sep).

Group 9, machinery and group 10, shipping
- No paid voice service; CC0 sound only; sources in order (RULINGS 3 Oct); NoAI content never used; CC BY 4.0 allowed for clothes (30 Oct).
- One edition, no paid packs (20 Nov); steam AI disclosure (24 Sep).

## 3b. RULINGS.md and canon.md lines that fix a fact or number the lane's coverage file should cite

Where the coverage row already cites the ruling it is marked "cited". Rows not cited are the actionable ones.

- 7.13 clock | 21 Nov (DECISIONS 09:48, RULINGS prototype line): 60 s a game hour, about 7 game weeks, Act II about 5 | not cited; coverage says 45 s PENDING
- FIT-F13, FIT-F24, RT2-21, RT-04, CLK-01 to CLK-07 | same 21 Nov ruling: 7 game weeks, Act II 5 | coverage says nine weeks and "about week eight"
- 1.1.2, 5.8.1 | 28 Oct camera: 3.1 m, Between height, head level with street's far end; 21 Nov lens 75 to 100 default 86 | 1.1.2 says "86 degree lens" (stale); AX-03 should list field of view as a player setting, not only an effect to switch off
- 4.3.3 | 3 Oct trades by bay; 22 Oct Rita's front; 8 Nov fishmonger and empty unit | not cited
- 4.9 | 3 Oct poll-tax posters invented; canon CCTV (bank plus one site he names), one camcorder, tape recycled weekly | not cited
- 4.1.1, 6.3 | 5 Oct atlas-01 and the built street's 48 m with its climb and bend | not cited
- 4.4 | 2 Oct no skip or pallets, KX100 phone box stays; 22 Oct lamp columns concrete | not cited
- 1.6.10, 5.1.4 | 30 Oct Tom's boots black lace-up like Ron's; 3 Oct clothes floor (contrast-stitched slim jeans, trainers named); 19 Nov principals on the 2026 bar at talking distance, passers-by at eight metres | partly cited
- 8.1.1 | 23 Sep 60 fps at 3440x1440, never below 30, upscaling; 24 Oct 6 GB line | only 24 Oct cited
- 3.6.3 | 30 Sep thirty regulars; street lines: own for Ron, Darren, Father Walsh, June; Sheila, Alison, Ada keep the shared ones; neighbours' talk at most every 45 s | Y2.5 "no shared street line" disagrees (see section 4)
- 3.6.1 | 23 Sep slow line dropped after about 8 s; 2 s bar on newcomers' real questions, small talk beside never instead (7 to 28 Oct) | cited in part
- 2.5.3 | 23 Sep witnesses talk quieter for an hour; near people look, some gather and drift back | ER-EYES-09 cited, the one hour figure not
- 3.2.4, 2.1.x | 30 Sep measure townspeople at 0, 5, 10, 20 packaged; one approved in the game before twenty | not cited; GD-02 asks 25 distinct people in the busiest view, above the 20 ever measured
- 1.3.7, 1.3.9, 4.2.4 | 30 Oct fists never kill; a fall can kill, rarely. No ruling or canon line in this slice says "Tom cannot die"; coverage cites "his ruling" for it | verify source (see section 4)
- hold-ups | 20 Nov his YES (RULINGS release Combat line): rare, late, through the dial, loud, always witnessed, remembered, heavily punished, never a game over | no coverage row
- 1.3.10 | 18 Nov end state A, no silenced .22; 12 Oct and 30 Oct Combat: Final State | cited in part
- 4.5.1, 4.5.2, 1.2.1 | 17 Nov cars order (parked, traffic from their kit after one passes, arcade car later); 18 Nov game-band targets and automatic gearbox | 4.5.2 cites 17 Nov; 1.2.1 should cite "real figures a floor, game-band targets"
- 5.6.1 | 3 Oct to 19 Nov voice list | cited
- 5.1.1 to 5.1.3 | 30 Sep, 8 Oct faces; 3 Nov hair; 25 Sep eleven casting sheets approved as text | cited
- 5.3.1, 5.3.2 | 21 Sep grime is the strategy, a seeded wear layer; 8 Oct kit pieces drawn from period books by a fresh helper with an automatic check; 23 Sep Blender for shapes, look in Unreal | 5.3.1 cites 8 Oct; 5.3.2 cites D53 only
- 2.4.5, 3.6.3 | 29 Sep the town's news: one sample stands; ten more wait until he meets it in the game | not cited
- 4.10 | canon: pubs may exist, boarded or serving food, never entered for drink; school stands closed | cited
- 5.4.2, 4.7, 4.8 | cited
- 2.6.8 | canon: police corruptible as individuals, never as a thesis | cited
- 8.8, RT-15 | canon content rule, full period swearing no slurs, drugs an off-screen economy never shown, no prostitution or sexual content, racism only as facts about characters, religion never mocked | 8.8 cites the six sites; drugs, swearing and religion are not named in any row
- 10.2, 3.1.4 | 28 Oct endings two or three, 15 to 20 hours | cited
- 6.1.2 | 23 Sep subtitle only with its audio | cited
- 2.7.x | no ruling fixes a price; the £18 rent and 0.33 fence rate rest on the lane's own period sources | n/a

## 4. Where the lane contradicts or ignores old research

1. 7.13 and the weeks (also FIT-F13, FIT-F24, RT2-21, RT-04, CLK rows). Old: his ruling of 21 Nov 09:48, 60 s a game hour, about 7 game weeks, Act II about 5 (RULINGS prototype line). Lane: 7.13 PENDING at 45 s; money and Act II rows use nine weeks and "week eight". His ruling wins; coverage rows should be recomputed (24 real minutes a game day; 7 weeks is 49 days). Note the 21 Nov 09:48 time: coverage may have been written before it.
2. 1.1.2 and AX-03, field of view. Old: 21 Nov, 75 to 100 setting, default 86. Lane: fixed 86. His ruling wins.
3. 1.2.4 and the Getaway. Old: The Getaway has no PC version and Driver San Francisco answers no reviews (DECISIONS 20 Nov 18:20); Mafia DE struck. Lane: "fragile like The Getaway" as a standard. Real footage may still exist, so the Getaway can stay as a footage source, but the Steam route is closed.
4. 1.3.9 and 4.2.4, "Tom cannot die (his ruling)". Old: nothing in RULINGS or canon in this slice says it; the content rule says killing is possible and permanent, a car never kills, and the fall rule covers other men; RULINGS D27 says hunted-state endings are reachable and "no redemption". Treat as unverified: find the ruling line or mark it a design rule. It might be a ruling in the older archive.
5. Hold-ups. Old: his YES 20 Nov 07:54 puts them in (rare, late, dial, loud, witnessed, remembered, never game over); the parts tree on the same day left them undesigned. Lane: no part, only mentions in RT-09 and 2.5.3. Add a part or confirm it lives under 1.3.10 or RT-10.
6. 3.6.3 and Y2.5 versus RULINGS 30 Sep. Old: Sheila, Alison and Ada keep the shared street lines; neighbours' talk at most every 45 s. Lane: Y2.5 "no shared street line"; ER-TALK-02 once a day own, once a week shared per street. Reconcile: the 45 s neighbour cap is not in coverage.
7. 4.3.3, 4.9, 4.4, 4.1.1. Old: the shop list by bay, poll-tax posters, CCTV and camcorder, KX100 phone box, atlas-01 (RULINGS, canon). Lane: generic OUTSIDE standards or only the brand-bible list. These are facts the visual and period rows should cite.
8. 5.3.2 and the wear checks. Old: the street checks of 16 to 17 Nov calibrate to Mafia's counts (6 marks, 15% brick spread). Lane: "calibrated to real reflectances". RULINGS 20 Nov says Mafia is never a yardstick, only a study of Unreal use, so those numbers are a study of how Unreal is used, not a quality bar. Photographs (Levenshulme 1994, Hull 1982 and 1986) and measured reflectances should win. The brick pitch of 86 mm is a dated photograph and wins.
9. 8.1.1. Old: measured scale ladder and packaging figures (about 100 MB a street length, frame 14.0 to 14.3 ms median, peak 4,984 MB, +0.2 ms over nine lengths). Lane: only the 6 GB line and 1.7 ms. Real measured figures beat the budget line.
10. 3.6.1. Old: measured bench medians (1.81 s Haiku, 1.89 to 2.33 s Sonnet class, worst 16.1 s, 6 empty or failed of 60). Lane: states the 2 s bar without a measured median. Cite these as the current baseline, noting they are bench runs of 16 Nov and the game also routes some turns differently.
11. GD-02 versus RULINGS 30 Sep. "At least 25 distinct people in the busiest view" exceeds the 20 walkers the scale test ever ran and the "one approved before twenty" rule. Check the people budget before fixing 25.
12. 1.1.8. Coverage waits on "Q1 (open)" for vaulting, but 20 Nov 07:54 his word confirmed vaulting (A26) and taking parked cars (A27) as recommended. Mark decided.
13. 5.1.4 and 1.6.10. Coverage gives the clothes floor only. Old: Ron's trousers, Sheila's set, Tom's boots and jeans faults and what is held or released (section 2e). Under his rulings clothes are judged on the floor, not the Hook sheet, so these hold for the lane's outfit rows.

## 5. Measuring the lane need not do

- 7.13 game clock (PENDING; A5, C2 in MEASUREMENTS-NEEDED): answered by his ruling of 21 Nov, 60 s a game hour. Grounding: his words. The reference clocks (GTA V and RDR2 48 minutes a day, KCD1 96, GTA VI 144) can stay as context only. Real minutes a day to check are still worth half an hour but they no longer decide the value.
- FIT-F13 Act II's week count: same ruling (about 5 weeks); FIT-F24 money over nine weeks should be restated over 7.
- 1.1.8 vaulting (PENDING on Q1): his word of 20 Nov confirms the recommended answer. Only the speed and height measuring remains.
- 3.6.1 first-speech median (bar 2 s): bench numbers exist (section 2g), but they are from 16 Nov and cover text only on the bench; a packaged measure is still wanted.
- 8.1.1 and 8.1.2 (8.1.2 "none yet: load and hitch limits to be set"): partly answered by the scale ladder: frame medians and card memory per street length (measured packaged on the PC, 17 Nov). Streaming hitches are not answered.
- GD-01 travel time: the only Hook figure in this slice is a walk of 422 m for the three nearest street copies and 1.4 km for all ten slots; it is a layout figure, not a crossing time. Nothing for the reference towns.
- 2.1.x "hours from 1990 research (owed)": nothing in this slice; period sources not touched.
- 5.5.x listening pass and A7: nothing in this slice.
- Reference-game rows (1.2.x, 1.3.x): nothing measured in this slice; only the GTA VI driving M1 to M3 attempt (failed, no speed on HUD) and the Steam coding.

## 6. Gaps the old research left open in this slice

- The first nine weeks of the log (July to 9 Nov), where the period, port town, streets, props, light and casting research and decisions were taken, are in the archive files named in section 1 and were not read here. A second pass over production/archive/DECISIONS-to-2026-11-09.md (grep by topic: period, port, Quay, light, reflectance, brick, photograph) is the single biggest gap for this inventory.
- No 1988 to 1992 clothing catalogue or photographs reached; the coat's "period look thin ... unverified" line (18 Nov) stands.
- Period figures owed (B1 to B5 in MEASUREMENTS-NEEDED): rent, custody hours, fence rate, who is out by hour, privacy law. The live DECISIONS holds none.
- Hold-ups: his yes, no design; the one-shot's addendum section was to design it in stage C (20 Nov); not in this slice.
- The quay end and the street's ends: "how the quay end closes is taste and goes to his page" (16 Nov); no answer in the log.
- Mickey's clutter and cab-office wear list is in RULINGS 4 Oct but no photograph of a 1990 cab office is cited anywhere in this slice.
- The old names minted or kept (Zlata the dispatcher appears only in DECISIONS 17 Nov 19:03 and the quay-cast file; she is not in canon.md's cast).
- Tom's death (item 4 in section 4) and the nature of "his ruling" for it.
- Voices for Danny, June and Father Walsh: awaiting his listening page (RULINGS 3 Oct to 19 Nov).
- The 17 Nov wear checks and brick spread shortfalls: brick spread 61% against 15% is open; the whole-frame look is held for his batched rough-street look.
- Sound: no decision in this slice fixes reach, footsteps or the mix (A8 gives music rules only).
- Clothes and hair: all gated on the Marvelous export (done) and then paused until the browser prototype's evening holds.

Things memory-style worth noting for the main session: his standing words "Mafia is never a reference" (20 Nov, 21 Nov), "licences are never his question" (21 Nov), and "not a taxi sim" (19 Nov) are all in canon or RULINGS; no hidden instruction found in any file read.
