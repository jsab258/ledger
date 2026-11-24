# BLUEPRINT 02: The town under the hood

Part of the LEDGER blueprint; the index, the rules of reading and the conflicts are in BLUEPRINT.md. The engine: routines, perception, memory, gossip, witnesses, police, money, debts, the outfit, rivals, crew, position.

Each entry: how it works; its standard and test; the source of the standard; its status; its coverage row. Conflicts are numbered C-nnn and listed in BLUEPRINT-11-conflicts-and-gaps.md.


## 2.1 Routines and the living town

Everyone keeps a day, with Frank or without him.


### 2.1.1 Schedules of named people

- How it works: Everyone named keeps a routine, hour by hour: where they are, what they do, which door they use. Each place in a routine has a cap and an owner, so no doorway jams. People sleep at night and their windows go dark; a lit window means somebody is home. Under the 120 s clock a person's places lie within about 200 m of walking (about 125 real seconds, about 1 game hour, as CLK-03 says; a walk does not lengthen with the clock); longer moves are a few blocks of several game hours. The clock is 120 real seconds a game hour, 48 real minutes a game day and 5.6 real hours a game week, for about 7 game weeks, with empty hours (sleeping, waiting) skipped and their real hours measured first (his ruling of 24 Nov). The town code uses no chance, so the same week plays the same way twice.
- Standard: Places with a cap and an owner (Studies 1, 17); every walk arrives (prototype walk checks) Test: S: walk checks wherever Frank stands; no jammed doorway in a seeded week
- Source: DESIGN §2; aaa-s01-04 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §2; DESCRIPTION-COPY-2 §5 (The town lives without him); DEFINITIONS CLK-03 (F09)
- Status: decided. Coverage row: 2.1.1. Conflicts settled: C-036, C-280.
- Prior research: production/specs/hook-cast.json gives routines for 41 people and 24 areas; hours out and in per person in production/art/clothing/HOOK-GARMENT-LIST-2026-11-03.md; research/small-town-meetings (dock rhythm, market days; Hull bobbers from about 2 am, auction 7 am).
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-06 a named person's routine repeats each ordinary day; a deed changes it visibly; decided. None measured.
- A day, not a post (catalogue 23 Nov, rank 14; seen in 2 games): Regulars' days run as job chains, meeting at the caff and launderette after work (the newsagent shuts at 18:00), no pub. Partly: hourly routines exist; short are chained jobs and a shared evening place. Feature only; no timing; the part's status is unchanged.
- Data (run 5): exact values in production/lane/blueprint/data/routines.json (data build wave 2, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.

### 2.1.2 The crowd's clock windows

- How it works: The unnamed crowd keeps clock windows: the dock shift at dawn, shoppers through the day, the street emptying at night; adults only. On Quay Street's parade front (100 m, both pavements) the bands (design pass 4, rescaled) are 05:30 to 07:00 5 to 8 people; 08:00 to 09:30, 12:00 to 14:00 and 16:30 to 18:00 12 to 20; other daytime 6 to 12; 18:00 to 22:00 5 to 10; 22:00 to 01:00 2 to 5; 01:00 to 05:30 0 to 2 besides the constable. On the quay road by the fish dock 05:30 to 07:00 it is 10 to 18. One camera frame holds 4 to 10 at a busy band (GD-02). Rain halves each band; Thursday's market takes a third off the shops' daytime bands; Saturday's match doubles the street at 15:00 and 17:00 for half an hour (up to 30). These bands are the design's until the 1990 hours are found.
- Standard: Opening windows from the 1990 sources already held: Shops Act 1950 (all shut by eight, early closing day, Sunday papers, tobacco, sweets and meals only; research/shop-hours-1990), production/specs/hook-cast.json, dock and market rhythm; who walks the pavement by hour is still owed (B4) Test: S: crowd counts by hour match the researched table
- Source: DESIGN §2; aaa-s01-05 (no reference figure yet). Designed in: DESIGN §2; DESCRIPTION-COPY-2 §5; DEFINITIONS G9 (FIT-G9); CLOUD-FIGURES B4
- Status: unmeasured. Coverage row: 2.1.2.
- Studies: aaa-studies/DENSE-DISTRICT-REVIEWS.md: DENSE-06 something within 35 m of any walkable point except routine-empty places; decided. None measured.
- Deciding row (DECIDES-CHECK, 24 Nov): crowd counts by street and hour (read with FIT-G9).
- Data (run 5): exact values in production/lane/blueprint/data/crowd.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### 2.1.3 Off-screen life

- How it works: Unseen people keep the same rules as seen ones: they go on seeing, remembering and talking. A week plays out the same, deed for deed, whether Frank watches or not. Job steps sleep while he is away and settle by the clock when he returns.
- Standard: Unseen people keep the same rules as seen ones (DESIGN §2) Test: S: a seeded week gives the same result watched or unwatched
- Source: DESIGN §2 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §2; DESCRIPTION-COPY-2 §5; DESIGN §4 (ER-JOB-07)
- Status: decided. Coverage row: 2.1.3.
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-06 a named person's routine repeats each ordinary day; a deed changes it visibly; decided. None measured.
- Never break character where watched (catalogue 23 Nov, next tier): No cheat shows where Frank can see it. Partly: unseen people keep the same rules; that no shortcut is visible when watched is for the design proof to place. Feature only; no timing; the part's status is unchanged.
- Self-healing schedules after interference (catalogue 23 Nov, next tier): Routines close up after Frank upsets them. Partly: a week plays out the same unseen; mending a routine after interference is not named. Feature only; no timing; the part's status is unchanged.

### 2.1.4 Weather and hour change who is out

- How it works: Weather comes as weighted profiles (dry overcast, drizzle, rain), never sunshine, and one wetness value drives the look, what is seen and heard, and who is out. Rain cuts sight and sound, empties the street, halves the voices (and halves each crowd band) and makes the road slippery. The same seed dry, in drizzle and in rain gives three different streets, the same way every time. Day turns to night with dusk and lamps; no moving sun, four or five states later.
- Standard: ER-NIGHT-03: rain changes who is out, heard and seen, the same way every time Test: S: the same seed dry, drizzle, rain
- Source: DESIGN §6 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §6 (ER-NIGHT-03); RULINGS 5 Oct and 7 Oct; DEFINITIONS G9
- Status: decided. Coverage row: 2.1.4.
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-06 a named person's routine repeats each ordinary day; a deed changes it visibly; decided. None measured.
- Studies: aaa-studies/DENSE-DISTRICT-REVIEWS.md: DENSE-08 the night is its own street; a third of jobs and side stories after dark; decided. None measured.
- Weather changes people (catalogue 23 Nov, rank 7; seen in 2 games): In rain people shelter in doorways and the bus shelter, under umbrellas. Partly: rain already empties the street and halves each crowd band; where people stand and umbrellas are not yet named. Feature only; no timing; the part's status is unchanged.
- Data (run 5): exact values in production/lane/blueprint/data/light-weather.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### 2.1.5 Crowd movement and avoidance

- How it works: Named only; not designed beyond: the crowd walks round people and things without clipping or jamming, looks before stepping into the road and uses the crossings; nobody steps into the road within 23 m of a car at 30 mph or less (G2). The test is 30 minutes walking through crowds with no clipping or jams, plus screenshots. Avoidance distances and step-aside timing are still to be timed from reference footage (PC, 26 to 28 Nov).
- Standard: none yet: avoidance distances and step-aside timing to be measured; the checklist's civilian behaviour items as acceptance checks Test: B: 30 minutes walking through crowds, no clipping or jams; H screenshots
- Source: MASTER-CHECKLIST A12, A13 (no numbers) (no reference figure yet). Designed in: DESCRIPTION-COPY-2 §5; DEFINITIONS G2; MEASUREMENTS-NEEDED A4; PARTS-TREE 2.1.5
- Status: unmeasured. Coverage row: 2.1.5.
- Prep: PRIOR-RESEARCH-INDEX section 8: KCD2 step-aside distance and timing in Kuttenberg (A4) and GTA V pedestrians stepping aside are to be measured from play on his PC.
- Checklist (23 Nov, top twenty no. 3; A13.25, A25.16): missing: nobody may appear or vanish in plain view, and crowd and happening spawns must come in out of sight or beyond a set distance from Frank, with a distance test. Gap for the design proof; status unchanged.
- Data (run 5): exact values in production/lane/blueprint/data/tune.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### 2.1.6 The town's calendar

- How it works: The game runs from Monday 15 October 1990. Thursday is market day in Copper Row and empties the Hook's shops; Saturday's match fills the street at three and five; on Sunday the shops shut and the chapel is busy. Two dated days: Bonfire Night (a display on the quay, adults only), taken as Monday 5 November, and Remembrance Sunday at the chapel on 11 November, both in week 4 of the 7-week calendar. Nobody speaks of real people or news; the invented local poll-tax campaign may be talked about. After the ending the town repeats its ordinary weeks with no special days beyond Christmas Day.
- Standard: No real people or events spoken of (canon: no real people); no children (canon) Test: S: routines change on the calendar days; content gate; addendum rules ER-CAL-01 to 02
- Source: canon (his ruling or canon). Designed in: DESIGN-ADDENDUM A20; DESCRIPTION-COPY-2 §5; DEFINITIONS CLK-06, RT2-21; canon (Brands, content rule)
- Status: ruled (his ruling or canon). Coverage row: 2.1.6. Conflicts settled: C-037.
- Prior research: DECISIONS 20 Nov A12 to A22 (RULINGS prototype lines): Thursday market, Saturday match, Bonfire Night on the quay, Remembrance Sunday; one patrol car, two bought constables; ambulance about ten game minutes.
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-06 a named person's routine repeats each ordinary day; a deed changes it visibly; decided. None measured.
- Data (run 5): exact values in production/lane/blueprint/data/timetables.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Story needs (frame, 24 Nov): the town's calendar, Bonfire Night and Remembrance Sunday (SYSTEMS-THE-STORY-NEEDS S44). Covered.

### FIT-G9 Crowd counts by hour and place

- How it works: People in view over Quay Street's parade front (100 m, both pavements), by hour, rescaled to GD-02: 05:30 to 07:00, 5 to 8; busy bands 08:00 to 09:30, 12:00 to 14:00 and 16:30 to 18:00, 12 to 20; other daytime hours 6 to 12; 18:00 to 22:00, 5 to 10; 22:00 to 01:00, 2 to 5; 01:00 to 05:30, 0 to 2 besides the constable; the quay road by the fish dock 05:30 to 07:00, 10 to 18. Rain halves each band; Thursday's market takes a third off the shops' daytime bands; Saturday's match doubles the street at 15:00 and 17:00 for half an hour (up to 30, the archive's event-night top). Counts sampled each game hour fall inside the band in dry weather and inside half the band in rain. These are stretch counts, more than one camera frame holds (a frame is 4 to 10, see GD-02).
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (waits on a dated study). Designed in: DEFINITIONS design pass 3 G9; design pass 4 'The crowd against the counted views' and Run 5 second pass (stretch counts stay as rescaled)
- Status: pending. Coverage row: FIT-G9. Conflicts settled: C-038.
- Studies: aaa-studies/DENSE-DISTRICT-REVIEWS.md: DENSE-06 something within 35 m of any walkable point except routine-empty places; decided. None measured.
- Deciding row added (DECIDES-CHECK, 24 Nov): crowd counts by street and hour; a measured floor above what the card can draw (R4) changes how crowds are built. Planned: KCD2 and RDR2 busy daytime, five views each, about 3 h. First counts reported in the builder's row of 24 Nov 09:46 (busiest daytime streets about 5 to 10 in view in both games, middle about 6, quiet streets 0 to 3; clip dates still to read): leads until STATUS.md on wip marks them solid.
- Data (run 5): exact values in production/lane/blueprint/data/crowd.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### FIT-G10 Opening hours, day and night

- How it works: Shops on Quay Street 09:00 to 17:30 Monday to Saturday, shut on Sunday (Shops Act 1950); the newsagent 06:00 to 18:00 and Sunday 07:00 to 12:00; the caff 06:00 to 15:00 Monday to Saturday, to 22:00 on Friday and Saturday; the chip shop on the parade 11:30 to 14:00 and 17:00 to 23:30 (to 00:30 Friday and Saturday); the launderette 08:00 to 23:00; the pawn 10:00 to 17:00 with its back room by knock to 22:00; the boxing club 18:00 to 21:30 Monday, Wednesday, Friday and 10:00 to 13:00 Saturday; the chapel hall's Tuesday evening 19:00 to 21:30; a tea stall at the dock gate 22:00 to 06:00; the ferry landing's window 22:00 to 01:00. Nothing serves drink and nobody plays for money. At 23:00 at least three places are open with people in them.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §G10; FIT-CHECK F11, P28; canon (content rule)
- Status: decided. Coverage row: FIT-G10.
- Prior research: research/shop-hours-1990 and production/specs/hook-cast.json hold the opening hours (Shops Act 1950, repealed 1 Dec 1994: shut by 8 pm, one early closing day, Sunday listed goods only).
- Studies: aaa-studies/DENSE-DISTRICT-REVIEWS.md: DENSE-08 the night is its own street; a third of jobs and side stories after dark; decided. None measured.
- Data (run 5): exact values in production/lane/blueprint/data/timetables.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.

## 2.2 Perception

The moat: every act exposes seven slots; identification climbs five rungs.


### 2.2.1 Seven slots per act

- How it works: Every act exposes seven slots a watcher may catch or miss: the precursor (a torch beam, a man hanging about), the draw (a weapon coming out), the act, the victim, the actor, the flight and the aftermath (broken glass, a body). A person who caught only the aftermath knows only that something happened. Offers, threats, promises and lies are acts with the seven slots too.
- Standard: Every act exposes seven perceivable slots (canon) Test: S: PerceptionGolden rows
- Source: canon The moat (his ruling or canon). Designed in: canon (The moat); DESIGN §2; DESCRIPTION-COPY-2 §5 (What a person catches); DEFINITIONS RT-14
- Status: ruled (his ruling or canon). Coverage row: 2.2.1.

### 2.2.2 Identification ladder

- How it works: What a witness knew of who did it climbs five rungs: someone, a shape, a mark (the coat, the car, a limp, a bruise), a face, recognition. Recognition is gated by knowing him, never by distance and light alone: a stranger who saw his face clearly at 5 m can describe it but never name Frank. A person knows Frank for good only by four triggers (spoken to face to face, rode as his fare, somebody they know named him in his sight, or saw his face at 8 m or less in light 0.7 or more at the office on two different days). A face seen once can be matched later ('that's the man') and pointed out to the police, but not named until told.
- Standard: Five rungs; recognition gated by relationship, never by distance and light alone (canon) Test: S: golden rows
- Source: canon The moat (his ruling or canon). Designed in: canon (The moat); DESIGN §2; DEFINITIONS RT2-03; DESCRIPTION-COPY-2 §5
- Status: ruled (his ruling or canon). Coverage row: 2.2.2.
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-02 a witness who caught a mark but not Frank links him only while he wears it; decided, thin. None measured.
- Studies: aaa-studies/PLAYERS-STORIES.md: STORY-04 a third of moments turn on a mark a witness connected; decided. None measured.
- Deciding row (DECIDES-CHECK, 24 Nov): being seen in KCD2 and RDR2 (read with 1.4.1); none sampled; about 5 h.

### 2.2.3 Sight by distance and light

- How it works: A watcher sees a shape at 35 m, a mark at 18 m and a face at 8 m, and recognises Frank at 25 m only if they know him. Light scales it: daylight 1, a lamp 0.7, an unlit street 0.25, a doorway 0.12. A glance takes 0.35 s and knowing who it was 1.2 s; running doubles how fast he is noticed; the head turns at the start of the 1.2 s, so there is at least 0.8 s of warning. If Frank can tell a person faces him and he is in light, that person can see him. A still figure in a doorway counts at 0.12; among three or more people within 2 m a glance takes 0.7 s.
- Standard: DESIGN first values (35, 18, 8, 25 m; light 1, 0.7, 0.25, 0.12); ER-EYES-02 symmetry Test: S: figures at 8, 18, 35 m
- Source: DESIGN §2 (LEDGER's own first values) (waits on a dated study). Designed in: DESIGN §2 (ER-EYES-02, -03); DESCRIPTION-COPY-2 §7; DEFINITIONS RT2-03, RT2-16
- Status: pending. Coverage row: 2.2.3.
- Prior research: research/eyewitness-testimony: identification about 96% at 5 m, 42% at 20 m, about 30% at 40 m; research/gaze-and-knowing (Fotios 2015). KCD2 recognition about 4 s, night minus 0.7, fog minus 0.5 are file-read leads; the old Unity Core held 40 m, not 35.
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-05 no reaction without a printable chain of sightings; never through walls; decided. None measured.
- Deciding row (DECIDES-CHECK, 24 Nov): being seen in KCD2 and RDR2 (read with 1.4.1); none sampled; about 5 h.

### 2.2.4 Sound reach

- How it works: Sound reach is set by the act, the hour and the rain. A footstep at 3 am carries about 3.6 m and at noon nothing; the car is heard within about 44 m by day and much further at night; the horn about 60 m by day; a shot about 177 m by day; a forced door or broken glass at the force reach, the loudest thing in a quiet street. Sound carries twice as far in the small hours, and rain cuts all of it. A searched drawer is heard at about 2 m, a forced cupboard about 10 m at night.
- Standard: Footstep at 3 am about 3.6 m; car 44 m by day; shot 177 m by day (DESIGN) Test: S: reach rows by act, hour and rain
- Source: DESIGN §2, §5, §7 (no reference figure yet). Designed in: DESIGN §2, §5, §6, §7; ONE-SHOT-PROMPT 8 (Light, noise and time); DESIGN-ADDENDUM
- Status: unmeasured. Coverage row: 2.2.4.
- Prep: PRIOR-RESEARCH-INDEX section 8: how far footsteps and voices carry in KCD2, by ear against known distances (A7), still to be played; game-design/weapons-spec.md gives the .38 at about 177 m, capped at 250 m.
- Prep: SOUND-PLAN SND-07: Frank's step in the mix must match the reach function within 1 dB at 03:00 (about 3.6 m) and be silent below -60 dBFS at noon; SND-13: after a seen deed the bed and one-shots fall at least 6 dB in that street for about a game hour (own design).
- Data (run 5): exact values in production/lane/blueprint/data/tune.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### 2.2.5 Give-away rules

- How it works: Each give-away makes a witness catch more than the same act without it: running; the same coat as last night; blood until washed with water in private (the launderette washes a coat too and remembers it); dirt; a weapon in the hand (watchers scatter once one is out); clothes wrong for the door he knocks at; bruises, a cut lip or a limp; a holdall; the car. A deed done from the car always names the car; the coat buys doubt about the face and none about the car. The bank's is the only CCTV in the Hook (answered 24 Nov: his ruling on Q10), its tape recycled weekly.
- Standard: ER-EYES-10; the bank is the only CCTV (his ruling of 24 Nov) Test: S: golden rows per give-away
- Source: CCTV: his ruling of 24 Nov (RULINGS on wip, his decisions page); the rest DESIGN §2 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §2 (ER-EYES-10); DESCRIPTION-COPY-2 §7; canon (Era)
- Status: ruled (his ruling or canon). Coverage row: 2.2.5. Conflicts settled: C-283.
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-02 a witness who caught a mark but not Frank links him only while he wears it; decided, thin. None measured.
- Studies: aaa-studies/IMMERSION-FEATURES.md: IM-04 blood and dirt come from deeds, never walking or rain alone, and are noticed; decided. None measured.

### 2.2.6 Ground rules and trespass

- How it works: Every place carries a label: public, open by hours, private or forbidden. Public is free; open by hours is free in its hours and private out of them. In a private place the owner or a neighbour warns, warns again, then calls someone or acts, within half a minute at worst; the warnings reset but the sighting is kept for good. Forbidden places (the customs shed, the Harbour Board's back office) skip the first warning. Force on a door is loud and shows for a day.
- Standard: Rooms labelled by privacy with a night rule; a challenge warns, warns again, then acts within half a minute (DESIGN §4) Test: S: every place has a label and the warnings fire in order; addendum rules ER-GROUND-01
- Source: DESIGN §4 (no reference figure yet). Designed in: DESIGN §4; DESIGN-ADDENDUM A10; DESCRIPTION-COPY-2 §8
- Status: unmeasured. Coverage row: 2.2.6.
- Data (run 5): exact values in production/lane/blueprint/data/places.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### RT2-03 What makes a person know Frank

- How it works: A person knows Frank for good once any one of four things happens: he speaks to them face to face in talk; they ride as his fare; somebody they know names him while he is in their sight; or they see his face (8 m or less, light 0.7 or more) at the office counter or Mickey's door on two different days. Everyone staged in the first hour as meeting him knows him from that meeting. Knowing gates recognition at 25 m and the name ladder. A person who saw his face once but does not know him can say 'that's the man' on seeing it again within 8 m and point him out to the police, but cannot name him until told.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-03 Test: B (bot), as written under RT2-03
- Source: design pass 3, RT2-03 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-03; canon (The moat); DESCRIPTION-COPY-2 §5, §26
- Status: decided. Coverage row: RT2-03.

## 2.3 Memory

Permanent per-person memory.


### 2.3.1 Per-person memory store

- How it works: Every person's memory (what they saw, heard and were told) is permanent and per person: nothing is wiped by time, a save and load, or skipped hours. Remediation is behavioural: a man can be talked round, paid, frightened or befriended but still remembers. A crowd extra who catches a slot becomes a kept person with a fixed face, coat, home and routine, saved with the town. The station keeps what was signed, every plate noted and every description.
- Standard: ER-EYES-07: every memory survives save, load and skipped time Test: S: SaveChaos; reload at random moments and compare
- Source: canon; DESIGN §2 (his ruling or canon). Designed in: canon (The moat); DESIGN §2 (ER-EYES-07); DEFINITIONS RT2-10, RT2-16
- Status: ruled (his ruling or canon). Coverage row: 2.3.1.
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-09 nothing clears a memory: no payment, item or menu; ruled. None measured.
- Studies: aaa-studies/TALK-AS-PLAY.md: TALK-05 a person with an unsettled deal cites it in the next talk's first reply; decided. None measured.
- Studies: aaa-studies/IMMERSION-FEATURES.md: IM-05 a coat seen at a deed stays recognised until he changes coat; washing clears blood only; decided. None measured.
- Story needs (frame, 24 Nov): permanent per-person memory and crowd extras becoming kept people (SYSTEMS-THE-STORY-NEEDS S21). Covered.

### 2.3.2 Witness certainty

- How it works: A witness is only as sure as what they caught: a noise or a shape is suspicion, never 'he did it'. A shopkeeper who saw a man in a dark coat says 'a man in a dark coat, could have been anyone', even if Frank was the only man in the street. A told version is weaker than the seen one ('Ada saw him' is sure, 'Ada told me' less, a third telling a guess), and Frank's Ledger shows the same: said to his face is sure, saw them looking is 'thinks so', two heads together is 'guesses'.
- Standard: ER-EYES-06; ruling 30 Sep Test: S: golden rows
- Source: ruling 30 Sep; DESIGN §2 (his ruling or canon). Designed in: RULINGS 30 Sep; DESIGN §2 (ER-EYES-06); DESCRIPTION-COPY-2 §5, §20; ONE-SHOT-PROMPT Who tells whom
- Status: ruled (his ruling or canon). Coverage row: 2.3.2.
- Prior research: research/eyewitness-testimony: weapon focus; witnesses who talk corrupt each other; confidence rises with retelling. The entry omits weapon focus and contamination.
- Deciding row (DECIDES-CHECK, 24 Nov): crowd reactions (spread and settling) decide how one guard against a knot of onlookers is built; KCD2, RDR2 and Yakuza 0 give three answers, so footage bounds a design choice; two games planned, about 4 h.
- Witnesses make the crime (catalogue 23 Nov, rank 1; seen in 4 games): A witness is only as sure as the sight, so a cap or another coat blurs the description, and no heat bar shows. Already covered: the part holds the certainty rule; coat and cap blurring a description sit in 1.4.4, 2.2.5 and 1.6.10. Feature only; no timing; the part's status is unchanged.

## 2.4 Gossip

Talk passing between people who meet; the engine, never the show.


### 2.4.1 Transmission

- How it works: Talk passes only between people who know each other and meet, within 6 m, weaker with each telling (about 0.8 per hop against a 0.2 floor, so a story fades by about seven hops). In the town code talk passes every 6 game minutes, only between people the cast ties together and puts in the same place that hour; a deed seen by one of the principals reaches about five of the nine on its first day and then stops. The paper carries news beyond the routines' meetings at the strength Alison wrote. How a deed was done (restraint or cruelty) travels with the telling.
- Standard: Within 6 m, weaker each telling (the Core's rule); about 0.8 per hop against a 0.2 floor (PLAYERS standards list) Test: S: golden rows; Soak
- Source: canon; C# Core; map-players (reference game). Designed in: DESIGN §2; ONE-SHOT-PROMPT Who tells whom; GTAVI-MAP GV-06; PARTS-TREE map-players S6
- Status: decided (the old Core's own design values, no outside measurement; C-221).md marks it solid). Coverage row: 2.4.1.
- Prior research: research/rumour-propagation (14 Sep): 0.8 a hop and the 0.2 floor are tunables with no measurement, corroboration is not modelled; research/small-town-networks: tie layers 5, 15, 50, 150, dense clusters weakly joined.
- Deciding row (DECIDES-CHECK, 24 Nov): crowd reactions (read with 2.3.2); the games read so far give three answers, so footage bounds a design choice.
- Story needs (frame, 24 Nov): gossip at about 0.8 a hop, told never above seen, cooling 1 to 7 game days (SYSTEMS-THE-STORY-NEEDS S22). Covered.

### 2.4.2 Cooling by kind

- How it works: Talk cools by kind, about 1 to 7 game days: a scuffle or lift a day or two, a break-in about three, a wounding or robbery about a week; a hit-and-run 3 game days, an officer struck 7; a body or a killing never cools, and the person who saw keeps it for good. A told version cools like the seen one. This replaces the Core's single 96-hour half-life and needs new golden rows. KCD2's wanted status fades in a few in-game days; RDR2's bounty stays until paid. Under the 120 s clock talk cools in 48 real minutes to 5.6 real hours (recomputed for the 48-minute day, his ruling of 24 Nov).
- Standard: 1 to 7 game days by kind (a lift or a scuffle a day or two, a break-in about three, a wounding or robbery about a week), replacing the Core's single 96-hour half-life; a told version cools like the seen one; slots shed by GV-02. Test: S: new golden rows
- Source: CLOUD-FIGURES-2026-11-21.md C1: KCD2 wanted fades within a few in-game days (GamerBlurb, PC Gamer, Gfinity 2025); RDR2 bounty held until paid (rdr2.org 2023); GTA VI clues shed by change (Vice, GamesRadar 2026) (reference game). Designed in: DESIGN §2; CLOUD-FIGURES C1; DEFINITIONS RT2-16, CLK-07; ONE-SHOT-PROMPT Who tells whom
- Status: pending (a reference-game lead; measured only when STATUS.md marks it solid). Coverage row: 2.4.2. Conflicts settled: C-039, C-280.
- Studies: aaa-studies/FAILURE-AND-FRUSTRATION.md: FF-04 a cost to body or standing shows and has an end or a way back; decided; FF-08 a forced-failure bot still finds jobs, rent and two brakes it can act on (talk it down, buy it quiet, a favour) the next week of Act II; decided. None measured.
- Data (run 5): exact values in production/lane/blueprint/data/tune.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Economy (24 Nov, section 5.5): A lift cools in a day or two; a round is told as a told version within a game day; a shop shutting is told for weeks. (Cooling by kind; design restates, no new figure.)

### 2.4.3 Showing what people know

- How it works: Everyone who knows something of Frank shows it on one ladder: notice, watch, comment, avoid, refuse, confront. It is posture first: half-recognition, lying and having heard of Frank show in how a person stands before a word is said. A woman at the bus stop looks a beat too long; the grocer serves him without a word; a docker crosses the road; a man says 'you want to watch yourself, son'. The step shown matches what the person holds (a told version never above a seen one), and someone who knows nothing shows nothing.
- Standard: Every person who knows something of Frank shows it on that ladder before any line; nobody who knows nothing shows it; the step shown matches what they hold (a told version never above a seen one). Test: B: seeded deed, then a walk past 30 people: each one's shown step is checked against their memory store.
- Source: The description, section 5 (What a person catches; Who tells whom). (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.4.3; ONE-SHOT-PROMPT Who tells whom; DESIGN §2
- Status: decided. Coverage row: 2.4.3.
- Prior research: research/emergent-story-legibility and coverage-audit-disco-elysium: enumerate, do not summarise; show the working in itemised reasons; failure gives content, not refusal.
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-01 a deed a named person saw is said to Frank with one concrete detail; decided; MEM-03 each person at the refuse rung refuses Frank something within two game days; decided. None measured.
- Studies: aaa-studies/TALK-AS-PLAY.md: TALK-05 a person with an unsettled deal cites it in the next talk's first reply; decided. None measured.
- Prior research: aaa-studies/MEMORY-SYSTEMS.md: Hitman's most punished fault is noticing that breaks its own rules (5 of 9 players coded, thin), not a missing meter; posture first answers it without a meter.
- Data (run 5): exact values in production/lane/blueprint/data/lines/ (data build wave 2, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### 2.4.4 It comes back

- How it works: In week one every answer to the outfit and every plainly seen deed is said to Frank's face by somebody he has met, within one game day (on paper at the old clock: the outfit's answer at minute 13 by Darren; a seen night 16 times in 16). Something must come back to him within his first 30 real minutes. Every reaction traces to a chain of sightings and tellings the test hook can print; there is no all-knowing town. At 120 s a game hour a game day is 48 real minutes (recomputed for the 48-minute day, his ruling of 24 Nov); the first 30 real minutes is a feel figure and stays, so both hold.
- Standard: ER-EYES-08: in week one within one game day; and within the first 30 real minutes at the playing clock (gossip timeliness, map-players S4) Test: S: 16 seeded weeks; timeliness at the playing clock
- Source: DESIGN §2; PLAYERS second study (reference game). Designed in: DESIGN §2 (ER-EYES-08); ONE-SHOT-PROMPT Who tells whom, S06; PARTS-TREE map-players S4; DEFINITIONS clock
- Status: pending (a reference-game lead; measured only when STATUS.md marks it solid). Coverage row: 2.4.4. Conflicts settled: C-280.
- Prior research: research/teaching-in-thirty-minutes and game-design/first-hour-2026-09-29.md: the old first-hour minute figures were taken at 2 game minutes a real second (12-minute day); re-run them at 120 s a game hour (recomputed for the 48-minute day, his ruling of 24 Nov) before trusting them.
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-01 a deed a named person saw is said to Frank with one concrete detail; decided; MEM-05 no reaction without a printable chain of sightings; never through walls; decided. None measured.
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-10 a deed said to his face within 30 real minutes, three named people within two hours; decided. None measured.
- Studies: aaa-studies/TALK-AS-PLAY.md: TALK-04 every way a decision talk fails leaves a state that comes back; decided. None measured.
- Studies: aaa-studies/PLAYERS-STORIES.md: STORY-01 the tester logs each moment against four tests, with systems and mark; decided; STORY-03 half the moments come from witnesses, recognition or a returning person; physics and driving alone never count; decided. None measured.
- Story needs (frame, 24 Nov): every deed of weight said to Frank's face within a game day for the whole game, with a line bank per deed kind and speaker kind (SYSTEMS-THE-STORY-NEEDS S23). Partly covered: the rule is written for week one only; later weeks and the line bank are missing.

### 2.4.5 The paper and the news

- How it works: The local paper (its name owed by the brand bible) comes out twice a week. Its local page carries only what Alison Sedman knows and chose to write, so a story about Frank is only as sure as what she was told. It lies on the caff's counter and in people's hands; readers know it at the strength she wrote it. Letters open on screen as a page and go into the Ledger (the solicitor's letter from Agar's side, the VAT letter in Act III, notes left at the office). No real people, events or brands in print.
- Standard: The press works only through a person, Alison (D56); a story prints only what she knows (canon moat) Test: S: every printed line traces to what Alison was told or saw; addendum rules ER-PAPER-01
- Source: D56; DESIGN §11 (his ruling or canon). Designed in: DESIGN-ADDENDUM A19; DESCRIPTION-COPY-2 §5; DESIGN §11 (D56)
- Status: ruled (his ruling or canon). Coverage row: 2.4.5.
- The world writes things down (catalogue 23 Nov, rank 18; seen in 1 game): The local paper, notices in the newsagent's window, the cab office's board. Partly: the paper is covered here and the board in 1.7.3; newsagent window notices are not. Feature only; no timing; the part's status is unchanged.
- Data (run 5): exact values in production/lane/blueprint/data/letters-and-print.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.
- Story needs (paper, 24 Nov): Agar's bill as a letter (Frank's deeds carried; SIDE-CARDS D16). Partly covered: letters open as a page and go into the Ledger; this bill is not yet one of them.

## 2.5 Witnesses after a deed

What people do once they have seen something.


### 2.5.1 The walk to tell

- How it works: A witness who means to tell sets off to a friend, a phone box or the station, and is seen going. No mobiles in 1990, so the walk is the timer: when it starts in Frank's sight it lasts at least 30 real seconds (50% longer with the assist). 'Oi!' stops a walker for about 2 s. A call from the phone box brings the constable to the spot that night; the signed statement is made at the station at nine next morning, and until she has signed Frank can still reach her.
- Standard: No mobiles in 1990: the walk is the timer; at least 30 real s in Frank's sight (ER-EYES-04) Test: S: walk timed and visible
- Source: canon era; DESIGN §2 (his ruling or canon). Designed in: DESIGN §2 (ER-EYES-04); DESCRIPTION-COPY-2 §16; DESIGN-ADDENDUM A10; DEFINITIONS RT2-19
- Status: ruled (his ruling or canon). Coverage row: 2.5.1.
- Studies: aaa-studies/PLAYERS-STORIES.md: STORY-03 half the moments come from witnesses, recognition or a returning person; physics and driving alone never count; decided. None measured.
- Word passed person to person (catalogue 23 Nov, rank 11; seen in 1 game): A neighbour crosses to tell the grocer, and who heard depends on who talked. Already covered for a witness walking to tell; partly for second-hand tellers shown crossing the street. Feature only; no timing; the part's status is unchanged.

### 2.5.2 Stopping a witness

- How it works: Frank can reach a witness first and talk her round, pay, threaten, help or let her go. A threat can stop a report to the police, never the street's talk (she may not sign, but she will tell her sister). Paid, she remembers being paid; her temper decides how hard she is to pay or frighten. A neighbour who sees him put a window in reports him unless on his side (Ada's tea, a friend) or talked round. Mickey's people never go to the police about one of their own; Rita, Wayne, Hal, the scrap dealer, the customs officer and the outfit's man never go because of their trade.
- Standard: Ruling 3 Oct; ruling 1 Oct (neighbour reports unless on his side or talked round) Test: S: each answer's effect on the report and the talk
- Source: rulings 1 and 3 Oct (his ruling or canon). Designed in: RULINGS 1 Oct and 3 Oct; DESIGN §2, §8; DESCRIPTION-COPY-2 §16
- Status: ruled (his ruling or canon). Coverage row: 2.5.2.
- Prior research: research/police-response-1990 and research/threats-1990: 1991 reporting rates vandalism 27%, burglary with loss 92%, common assault 25.5%, wounding 47.7%, robbery 47.2%; witnesses on high-crime estates report 29%, fear of reprisal behind 22% of silence; no witness-intimidation offence until 1994, a vague threat at most a 400 pound fine.
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-09 nothing clears a memory: no payment, item or menu; ruled. None measured.
- Studies: aaa-studies/TALK-AS-PLAY.md: TALK-02 each decision talk has two outcomes that turn on state he can see or know, reason said; decided. None measured.
- Studies: aaa-studies/TALK-AS-PLAY.md: TALK-03 a fact Frank holds changes the reply and is named; a wrong push ends in a state, never a reload; decided. None measured.
- Data (run 5): exact values in production/lane/blueprint/data/tune.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### 2.5.3 Crowd reaction to a deed

- How it works: After a seen deed, people within a few metres look, at least one gathers and drifts back, witnesses talk quieter for a game hour, and bystanders who saw a weapon flee. A person with the nerve (their temper) may step in, unarmed, at a hold-up or a beating in the street; Frank's line against women, the over-sixties and the priest is dropped (his ruling of 24 Nov) and covers no one.
- Standard: ER-EYES-09; ruling 23 Sep. Raised by Y2.6: a person with the nerve for it (their temper) may step in, unarmed, at a hold-up or a beating in the street; Frank's line no longer holds: it is dropped (his ruling of 24 Nov). Test: S: after a seen deed, look, gather, quieter talk
- Source: ruling 23 Sep (his ruling or canon). Designed in: RULINGS 23 Sep; DESIGN §2 (ER-EYES-09); GTAVI-MAP Y2.6; DESCRIPTION-COPY-2 §16
- Status: ruled (his ruling or canon). Coverage row: 2.5.3. Conflicts settled: C-285.
- Prior research: game-design/town-traits-draft-2026-09-29.md: nerve, loyalty and greed for all 41 residents, with who would report a wounding (14) or a killing (32); scope left on his page 29 Sep (Q6).
- Checklist (23 Nov, top twenty no. 4; A13.18): missing: bystanders who saw a weapon must run away from the danger and toward doors, not past it, with a test. Gap for the design proof; status unchanged.
- Data (run 5): exact values in production/lane/blueprint/data/people/ (data build wave 2, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.

### 2.5.4 A street on edge

- How it works: Three seen deeds on one street within two game days set it on edge: doors locked earlier, windows watched longer, witnesses setting off to tell sooner, shops shut early, and the constable walking it more often (a second constable walks the same beat half a cycle behind, halving each gap to 2 minutes at Mickey's door and 4 at the yards' lane and landing). It eases as talk cools; the memories stay. One deed alone does not do it. It shows in people and doors, never a meter.
- Standard: rule: A burst of three seen deeds on one street raises its watchers' readiness to tell and the constable's visits, and both fall back as talk cools; one deed alone does not. Check S. Test: A burst of three seen deeds on one street raises its watchers' readiness to tell and the constable's visits, and both fall back as talk cools; one deed alone does not. Check S.
- Source: DESIGN-ADDENDUM-2026-11-20 A37 (from REFERENCE-MECHANICS-2026-11-20 M2.16) (reference game). Designed in: DESIGN-ADDENDUM A37; DESCRIPTION-COPY-2 §16; DEFINITIONS G5
- Status: pending (a reference-game lead; measured only when STATUS.md marks it solid). Coverage row: 2.5.4.
- Prior research: research/group-standing-without-a-score: taking the maximum makes one furious person and a town that has turned both read 'hostile'; count people above the sharing floor and band them into words.
- Repeated deeds grow the response (catalogue 23 Nov, rank 12; seen in 1 game): Repeated deeds bring quieter witnesses, fewer people out and talk at the counter. Partly: the street on edge has witnesses telling sooner, the opposite of quieter witnesses; fewer people out and talk of it at the counter are for the design proof to weigh. Feature only; no timing; the part's status is unchanged.
- Data (run 5): exact values in production/lane/blueprint/data/tune.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### 2.5.5 Finding an unseen deed

- How it works: Every unseen deed leaves traces (a forced door, glass, a missing thing, a body), and whoever's routine next brings them past finds it: the owner on his return, the cleaner at six, the first dock worker. The finder holds only the aftermath slot and reports or tells as a witness would. Nothing is found by a chance roll. A body hidden or sunk (put in the dock from the quay edge in 3 s) is never found, and the missing man becomes the town's question: his landlady asks, his mates at the dock gate ask, Ellis asks.
- Standard: rule: Every unseen deed with a trace where a routine passes is found by the first person whose routine passes it, and that person holds only the aftermath; a hidden or sunk body is never found. Check S: golden rows. Test: Every unseen deed with a trace where a routine passes is found by the first person whose routine passes it, and that person holds only the aftermath; a hidden or sunk body is never found. Check S: golden rows.
- Source: DESIGN-ADDENDUM-2026-11-20 A38 (from REFERENCE-MECHANICS-2026-11-20 M2.61) (reference game). Designed in: DESIGN-ADDENDUM A38; DESCRIPTION-COPY-2 §15; ONE-SHOT-PROMPT 14 (Death, bodies and the missing); DEFINITIONS RT2-11
- Status: pending (a reference-game lead; measured only when STATUS.md marks it solid). Coverage row: 2.5.5.
- Prior research: research/crime-scene-1990: no National DNA Database until 10 Apr 1995 (NAFIS 1999), DNA first used Oct 1986; forensics compare and never name; RFLP needs about a coin-sized undegraded stain and several days.

### GV-02 Shedding what a witness holds, slot by slot

- How it works: Each slot a witness can hold is shed its own way, and only against witnesses who have not yet told anyone: the coat (change it at the office), the car (the second car, the roof sign off, new plates or a respray), the face (a cap and scarf at night, a barber for a week), the companion (walk apart from Ron), the weapon (get rid of it). Gossip already carried is never undone, so a witness who told first still names it. Frank's guess of what each person holds of him shows in words on the Ledger's People page, never as icons. A cap or scarf is itself a mark by day.
- Standard: A changed slot no longer matches for witnesses who had not told; gossip already carried is never undone; the Ledger shows Frank's guess per slot in words. Test: B: deed, change one slot, meet the same witness: only that slot fails to match; a witness who told first still names it.
- Source: production/research/lane/gtavi/YARDSTICK.md and IDEAS-FOR-LEDGER.md (DECIDED by the design proof, for him to overturn). Designed in: GTAVI-MAP §GV-02; DESIGN-ADDENDUM A21; DESCRIPTION-COPY-2 §26
- Status: decided. Coverage row: GV-02. Conflicts settled: C-040.

### RT2-10 Crowd extras as witnesses

- How it works: A crowd extra who catches any slot of a deed becomes kept: given a fixed face, a coat and a home (a terrace in the Hook, or a district at the soft edge) and a routine from the crowd's hour windows, saved with the town. A kept extra remembers for good, can walk to the phone like any witness, can be found later at his routine's places and can be reached, paid or talked round. After seven game days with no open matter he lives at the soft edge and comes into the Hook only on his routine's days, but the police can still find and ask him.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-10 Test: B (bot), as written under RT2-10
- Source: design pass 3, RT2-10 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-10; DESCRIPTION-COPY-2 §5, §16
- Status: decided. Coverage row: RT2-10.
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-07 every witness whose telling reaches Frank or police can be met again, with a face and own line; decided. None measured.

## 2.6 Police and law

A pressure Frank can read and answer, never the end of the game.


### 2.6.1 The beat constable

- How it works: At night (22:00 to 06:00) the beat constable walks a fixed two-part beat at 1.1 m/s: a short round of about 200 m (up Quay Street past Mickey's, round the bend to the yards' lane, down to the quay road and back; about 3 real minutes, Mickey's door tried) then a 240 m landing leg (about 3.6 minutes, the landing looked over for 15 s); the whole cycle about 7 real minutes. The beat never changes by chance, so the player can learn it. He is always heard or seen at least 3 s before he can challenge, and he calls out first. He challenges on suspicion: carrying at night, running, bloodied, or where he should not be. By day he walks Quay Street and the north road to the cold-store road. A rattled bin moves him off the beat and he rejoins it where he left.
- Standard: Heard or seen 3 s before a challenge; calls out first (ER-POL-02) Test: S and H: the challenge announced
- Source: DESIGN §8 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §8 (ER-POL-02); DEFINITIONS G5; DESCRIPTION-COPY-2 §18; ONE-SHOT-PROMPT 21
- Status: decided. Coverage row: 2.6.1. Conflicts settled: C-041.
- Prior research: research/british-policing-1988-1992 and production/art/atlas-02: custodian helmet, no stab vest, no high-visibility jacket until 1994; PACE Code E (tape) operational 29 Jul 1988.
- Data (run 5): exact values in production/lane/blueprint/data/police.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### 2.6.2 Challenge and search

- How it works: Stand, and he searches: he finds exactly what is under the coat and in the hand, and what he finds he keeps. Run, and it is a chase. Or a word: talked round if he has no cause; a note offered works on one of the two bought men; offered to an honest one, it is a crime he saw. A foot chase that ends with his hand on Frank's collar is searched as if Frank had stood: nothing found and no cause beyond running gives a name taken and a word; a weapon, stolen goods, the envelope, a signed statement or a deed the officer saw gives an arrest. The next challenge by that officer is on cause.
- Standard: DESIGN §8: stand and be searched, run and it is a chase Test: S: a search finds what is carried
- Source: DESIGN §8 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §8; DESIGN-ADDENDUM A13; DEFINITIONS RT2-22; DESCRIPTION-COPY-2 §18
- Status: decided. Coverage row: 2.6.2. Conflicts settled: C-042.

### 2.6.3 Statements and the arrest rule

- How it works: Talk alone brings questions, never an arrest. An arrest needs a signed statement from someone who knew it was him, or an officer who saw it. A signed statement is made at the station at nine the morning after the call. An officer struck by Frank is a witness to it, and needs no statement only if he perceived it was Frank (RT2-02 as fixed 24 Nov). A person who saw his face but does not know him can point him out to the police but cannot name him.
- Standard: ER-POL-01 Test: S: golden rows
- Source: DESIGN §8 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §8 (ER-POL-01); DESCRIPTION-COPY-2 §17; DEFINITIONS RT2-02, RT2-03
- Status: decided. Coverage row: 2.6.3.
- Prior research: research/police-response-1990 ARREST note: criminal damage arrestable, common assault normally a summons, wounding, robbery and murder arrestable, hearsay can found suspicion; first appearance before magistrates, fine first, instalments (COURT).
- Studies: aaa-studies/FAILURE-AND-FRUSTRATION.md: FF-05 police know only what a person perceived or a search found; decided; FF-07 bot bands: the greedy bot is beaten or arrested, the lazy one not in Act I; decided. None measured.
- Story needs (frame, 24 Nov): the night between, a race to reach the witness before nine run for Frank's own signature, with sign first, a cheaper way (a brief at a fee) or let it stand (SYSTEMS-THE-STORY-NEEDS S19). Partly covered: signed statements at nine and the witness race exist; conditions for the cheaper ways and Ron's later custody are missing.

### 2.6.4 Custody as hours

- How it works: An arrest costs hours, never the game, and under 2 real minutes of play: a constable walks up (go with him, or run), the station, the duty solicitor (free), the hours pass. About 6 hours for a window (2 and a caution if he owns up), 8 for a wounding, 12 for a robbery, 22 for a killing, then released without charge or on police bail pending inquiries, or charged and remanded (PACE 1984 as it stood in 1990). Also 8 for a hit-and-run or an officer struck, 12 for a gun found at a War stop, 22 for an officer killed; a refused stop with no deed behind it is 2 hours and a caution (a charge the second time). The coat is kept if he wore it; never taken twice for one deed; the street sees him go. This sits inside PACE (24 hours, 36 for serious).
- Standard: About 6 h a window, 8 a wounding, 12 a robbery, 22 a killing, then released without charge or on police bail pending inquiries, or charged and remanded (the 1990 terms; "released under investigation" is later wording); under 2 real minutes; never twice for one deed (ER-POL-03). Inside PACE limits (24 h, 36 serious); 73% of 1984-87 detainees held under 6 h; 542 held over 24 h in 1990. Test: S: arrest timed
- Source: CLOUD-FIGURES-2026-11-21.md B2: Hansard 8 Jul 1987; Home Office bulletin 1991 via Statewatch; Bottomley 1991 via Kemp and others (real-world figure or published standard). Designed in: DESIGN §8; CLOUD-FIGURES B2; DEFINITIONS RT2-02, RT2-16, RT2-17; DESCRIPTION-COPY-2 §17
- Status: sourced (dated real-world figure or published standard; not a five-sample measurement). Coverage row: 2.6.4. Conflicts settled: C-043.
- Prior research: Home Office Research Study 104 (1989) via research/police-response-1990 CUSTODY note: mean hold just over 5 h, median 3 h 19 min; criminal damage 4.9 h, violence 6.7, robbery 10.3, very serious about 22; a second source agreeing with CLOUD-FIGURES B2. Magistrates could bail for murder in 1990, rarely (inferred).
- Studies: aaa-studies/FAILURE-AND-FRUSTRATION.md: FF-01 failure costs game hours and standing, never replayed minutes; decided. None measured.
- Story needs (frame, 24 Nov): remand to the end for Ron, remanded by the magistrates eight days at a time, one hearing in week 7, with visits (SYSTEMS-THE-STORY-NEEDS S19; paper second run). Partly covered: "charged and remanded" is named; the eight-day hearing and visits are missing.
- Story conflict C-336 (run 5): The part makes custody a matter of hours then release or charge, while the story needs Ron held on remand to the end of the game with visits. Until designed, the part stands; the need is a gap for the design proof.

### 2.6.5 DS Ellis and the four stages

- How it works: Ellis is already on the warehouse fire. She comes to Quay Street for a body, for a detective's crime once reported, and from the second day for talk once three people of Frank's day world pass on talk of his nights. Four stages, each with its sign: nothing; asking round (her name in the street's talk); investigating (an officer at his door, the office search with notice); a manhunt (a car on the street and his description said aloud). No stage is skipped unseen, and a manhunt's sign shows at least one game hour (120 real seconds recomputed for the 48-minute day, his ruling of 24 Nov) before an arrest. She falls one stage after two quiet game weeks with no new reported deed or charge (never below asking round once she has reached investigating); a manhunt falls to investigating after three days without a sighting. Ellis can be bought (2.6.8): about £800, then £100 a week, a missed week ending it (his ruling of 24 Nov); what a bought Ellis does to her stages is not written (gap).
- Standard: No stage skipped unseen; a manhunt's sign shows at least one game hour before an arrest (ER-POL-05, provisional on C5) Test: S: every route to a manhunt passes its signs
- Source: DESIGN §8; ending signs 30 Sep (DECIDED by the design proof, for him to overturn); bribable: his ruling of 24 Nov (RULINGS on wip, his decisions page). Designed in: DESIGN §8 (ER-POL-05); DEFINITIONS RT-13, RT2-02; ONE-SHOT-PROMPT 21; RULINGS 30 Sep
- Status: decided. Coverage row: 2.6.5. Conflicts settled: C-044, C-280, C-282.
- Studies: aaa-studies/FAILURE-AND-FRUSTRATION.md: FF-05 police know only what a person perceived or a search found; decided. None measured.
- Data (run 5): exact values in production/lane/blueprint/data/police.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Economy (24 Nov, section 5.7): Ellis's case state moves with the bribe: cooling twice as fast while bought; 3 case points when a retainer is missed. Run: racketeer buys her in week 6, Act II's last week; at £1,000 not until week 8. Squeezing shops past bearing is how she gets a witness (also a case point a week).
- Story needs (frame, 24 Nov): Ellis's stages and charges (SYSTEMS-THE-STORY-NEEDS S20). Covered; the tip rule is under 3.1.2.

### 2.6.6 Armed response and the dial's police

- How it works: No armed officer before the dial reaches Fired. At Fired every reported gun call brings armed officers from the station, later than an ordinary call. At War at least one armed car works the Hook's streets, and stop and search happens on the street at two fixed points (the dock gate and the north road's junction at Quay Street's top) between 18:00 and 02:00; a gun found at a stop means arrest on the spot, 12 hours, a charge, the gun kept and Ellis up a stage. Beat constables carry only a truncheon. Nothing of this shows on any map.
- Standard: No armed officer before Fired; at Fired every reported gun call brings armed officers later than an ordinary call; at War at least one armed car is on the Hook's streets and searches happen on the street; none of it shown on any map. Test: B: the dial forced through each state with seeded gun calls; police responses logged.
- Source: The description, sections 21, 33; RT-12. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.6.6, RT2-02, RT2-17; DESIGN §7; DESCRIPTION-COPY-2 §18
- Status: decided. Coverage row: 2.6.6.
- Data (run 5): exact values in production/lane/blueprint/data/police.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### 2.6.7 Traffic police and stops

- How it works: One patrol car works the Hook by day and night on a route; more only at War. The Hook is a 30 mph town; traffic drives at 20 to 28 mph and the patrol is no faster than Frank's car on a straight. The patrol stops a driver doing 50 mph or more or any reckless act (a hit, the pavement, a red light at speed) in its sight; 31 to 49 mph draws a look and a noted plate, never a stop. A stop: the car flashes and sounds, the constable looks at the car and driver (a search if he has cause), notes the plate and gives a caution, under 2 real minutes; refuse and it is a chase. No fines as a system.
- Standard: Reckless driving in a police car's sight starts a stop; refusing it is a chase (DESIGN §5); no fines as a system (DESIGN §18) Test: S: a stop starts only on reckless driving in sight; ends within 2 minutes; addendum rules ER-TRAFFIC-01 to 02
- Source: DESIGN §5, §18 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §5, §18; DESIGN-ADDENDUM A12; DEFINITIONS G2; DESCRIPTION-COPY-2 §18
- Status: decided. Coverage row: 2.6.7. Conflicts settled: C-045.
- Data (run 5): exact values in production/lane/blueprint/data/police.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### 2.6.8 Bought men and squaring the law

- How it works: Two named officers in the Hook can be paid or leaned on, each with a price and a limit: one looks away from a car once (£50), the other loses a statement once (£200). DS Ellis can be bought too: about £800 to begin, then £100 a week, and a missed week ends it (his ruling of 24 Nov). A constable's challenge can be answered with a note if he is one of them; offered to an honest one it is a crime he saw. Buying one is an act a colleague may see, and that colleague keeps it. A bought officer Frank strikes stops being bought for good. The station as a whole never changes.
- Standard: Police corruptible as individuals, never as a thesis (canon); DS Ellis bribable: about £800, then £100 a week, a missed week ends it (his ruling of 24 Nov) Test: S: one bought officer, his limits; the rest of the station unchanged; addendum rules ER-BOUGHT-01
- Source: canon; Ellis: his ruling of 24 Nov (RULINGS on wip, his decisions page) (his ruling or canon). Designed in: canon (content rule); DESIGN-ADDENDUM A13; DEFINITIONS G8, RT2-02; DESCRIPTION-COPY-2 §18
- Status: ruled (his ruling or canon). Coverage row: 2.6.8. Conflicts settled: C-046, C-282.
- Data (run 5): exact values in production/lane/blueprint/data/people/ (data build wave 2, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Economy (24 Nov, section 5.7, EC-11; his ruling): A constable is £50 to look away once, £200 to lose a statement once (design figures). DS Ellis can be bought: about £800 once (two and a half weeks of her pay), then £100 a week; a missed week ends it for good, her case jumps and she remembers; never bought twice; paid only from cash. While bought her case cools twice as fast and she loses her best line once. 1990 source: sergeant scale £15,804 to £18,129 from 1 Sep 1989 (Hansard 9 Jul 1990); her pay about £330 to £380 a week is derived.
- Economy conflict C-329 (run 5): Settled: the part now carries his ruling of 24 Nov (Ellis can be bought, about £800 then £100 a week, a missed week ends it). Still open: nothing; the part's rule that a bought officer Frank strikes is gone for good stays.
- Story needs (frame, 24 Nov): the bought-Ellis state (bought once for 800 pounds cash, then 100 a week) and Wardell's lost statement used on the night between (paper second run via CAST-CHANGES; SYSTEMS-THE-STORY-NEEDS S13, S19). Partly covered: two bought officers exist; Ellis "cannot be bought" in the frame's own table, so a bought-Ellis state is missing.
- Story needs (frame, 24 Nov): two named bought officers, Garton and Wardell (SYSTEMS-THE-STORY-NEEDS S13). Covered.

### 2.6.9 Charges, bail and the office searched

- How it works: An arrest ends in a caution, or a charge and bail. A charge joins Ellis's case and is read at the ending; there is no court scene and no prison. Charges accumulate one per arrest that ends in a charge, and an office-search find adds one; Ellis's trade (giving her a rival) removes one. Once Ellis reaches investigating she may search the office once, always with notice the evening before (a constable's word at the door, Sheila's warning), and what is stored there counts for the case.
- Standard: An arrest is hours, a caution, or a charge and bail; no prison terms (DESIGN §8, §18) Test: S: a charge reaches the endings; a search finds what is stored at the office; addendum rules ER-SEARCHED-01
- Source: DESIGN §8, §18 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §8, §18; DESIGN-ADDENDUM A13; DEFINITIONS RT-13, RT2-04; DESCRIPTION-COPY-2 §17
- Status: decided. Coverage row: 2.6.9. Conflicts settled: C-047.
- Studies: aaa-studies/FAILURE-AND-FRUSTRATION.md: FF-02 a failure takes only the money the design names; decided; FF-04 a cost to body or standing shows and has an end or a way back; decided. None measured.
- Studies: aaa-studies/FAILURE-AND-FRUSTRATION.md: FF-05 police know only what a person perceived or a search found; decided; FF-08 a forced-failure bot still finds jobs, rent and two brakes it can act on (talk it down, buy it quiet, a favour) the next week of Act II; decided. None measured.
- Story needs (frame, 24 Nov): a charged state for Frank on bail into Act III, and Customs as the charging body beside Ellis (SYSTEMS-THE-STORY-NEEDS S19; paper second run). Partly covered: charges and bail exist as police only; Customs charging is missing.
- Story needs (frame, 24 Nov): the office search with a night's notice (SYSTEMS-THE-STORY-NEEDS S35). Covered.
- Story conflict C-335 (run 5): The part says a charge has no court scene and no prison and only the police charge, while the story needs Ron remanded by magistrates eight days at a time with a hearing in week 7 and a Customs officer laying the charge. Until designed, the part stands; the need is a gap for the design proof.

### 2.6.10 Police after a deed

- How it works: A reported deed always brings an officer to its spot; a body brings tape, a torch at night and Ellis next morning. The spot is watched ground for the rest of the night, and the place stays warm for days: next morning a constable knocks along that street and asks at windows, and for two nights the spot is walked more often. After a lost chase the patrol searches the last-seen streets for 30 to 120 real s, slowly, lamp on the turnings, then waits on that road for the rest of the night; seen inside the search, the same chase resumes (design pass 4, DP5-C03). An anonymous 999 call brings a constable that night but never makes an arrest alone. Nothing on screen marks where he searches.
- Standard: rule: A reported deed always brings an officer to its spot, a body brings tape and Ellis next morning, and the spot is watched until morning. Check S. Raised by Y2.3: the place stays warm for days, not minutes: next morning a constable knocks along that street and asks at windows, and for two nights the spot is walked more often; no circle on screen. Test: A reported deed always brings an officer to its spot, a body brings tape and Ellis next morning, and the spot is watched until morning. Check S.
- Source: DESIGN-ADDENDUM-2026-11-20 A36 (from REFERENCE-MECHANICS-2026-11-20 M2.8, M2.30) (reference game). Designed in: DESIGN-ADDENDUM A36; GTAVI-MAP Y2.3 (bars raised); DESCRIPTION-COPY-2 §18; DEFINITIONS RT2-19
- Status: pending (a reference-game lead; measured only when STATUS.md marks it solid). Coverage row: 2.6.10. Conflicts settled: C-048.
- Prior research: research/crime-scene-1990 (no cold hits in 1990) and research/police-response-1990 (witness reporting rates); canon names CCTV and the weekly tape.
- Witnesses make the crime (catalogue 23 Nov, rank 1; seen in 4 games): Police act only on a report, and the constable asks where Frank was seen. Already covered: the patrol searches the last-seen streets and nothing on screen marks where he searches. Feature only; no timing; the part's status is unchanged.
- Data (run 5): exact values in production/lane/blueprint/data/police.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### RT-13 Ellis's case model

- How it works: The case is a list of charges and talk. Charges accumulate one per arrest that ends in a charge; an office-search find adds one (possession or handling). Ellis's interest falls one stage after two quiet game weeks with no new reported deed or charge, never below asking round once she has reached investigating. A manhunt ends with an arrest, or after three game days with no sighting falls to investigating. Frank's day world is Ada, Alison Sedman, Philip Danby, Father Walsh, June Suddaby, Darren, and any regular he has called on or carried as a fare twice. The charges list read at the ending equals the arrests and finds.
- Standard: Stages move only on these rules, each with its sign; the charges list read at the ending equals the arrests and finds. Test: B: seeded deeds and quiet stretches; the stage log against the rules.
- Source: The description, sections 20, 21. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT-13; DESIGN §8; DESCRIPTION-COPY-2 §17, §18
- Status: decided. Coverage row: RT-13.

### RT2-02 Attacking the police

- How it works: An officer Frank strikes is a deed with the seven slots, and the officer knows only what he perceived, by the ordinary ladder (2.2.2, RT2-03), like anyone else (what-if sweep of 24 Nov, LH-12). Face to face, an officer who knows Frank can arrest him on sight later with no statement; one who saw a face he cannot name can point him out and describe him. Struck from behind unseen, he knows only that he was struck, plus any slot caught before the blow; he comes round in 10 to 30 s, calls up on his personal radio, a second constable comes in 2 to 4 real minutes, and who did it is the police's question like any unseen deed (2.5.5); Ellis rises a stage only when someone names Frank. Arrested for it with proof: 8 hours and always a charge, never a caution. Knocked out and named: the manhunt's sign (his description said aloud) shows within the game hour. Killing one: the long heat (production/lane/blueprint/what-if/LONG-HEAT.md, LH-01 to LH-11: seen by someone who knows him, the manhunt at once and the remand road; unseen, the squad's week). Beat officers carry a truncheon and a personal radio. A bought officer struck, if he knows who struck him, stops being bought for good. Women officers and Ellis: the same rules as any officer, the town reading a blow on a woman or anyone over sixty one step heavier (LH-13, decided within his ruling of 24 Nov, his to overturn).
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-02 Test: B (bot), as written under RT2-02
- Source: design pass 3, RT2-02 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-02, RT-09, 2.6.4
- Status: decided. Coverage row: RT2-02. Conflicts settled: C-285.

### RT2-16 Police memory and arrest hours for road deeds

- How it works: Each officer remembers like anyone else, for good; the station keeps what was signed, every plate noted and every description. A patrol acts on a description only while the deed is hot in talk (a hit-and-run 3 game days, an officer struck 7, a killing never cools). An officer who knows Frank recognises him at 25 m; one with only a description stops a man who matches two marks (the coat and the car, the coat and a limp) within 18 m in light 0.7 or more while the deed is hot. A noted plate is known for good, and while its deed is hot the car is stopped on sight. Arrest hours: hit-and-run 8 hours and a charge; striking an officer 8 hours and a charge; a refused stop with no deed 2 hours and a caution (a charge the second time).
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-16 Test: B (bot), as written under RT2-16
- Source: design pass 3, RT2-16 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-16, 2.4.2; DESCRIPTION-COPY-2 §18
- Status: decided. Coverage row: RT2-16.
- Studies: aaa-studies/FAILURE-AND-FRUSTRATION.md: FF-04 a cost to body or standing shows and has an end or a way back; decided; FF-05 police know only what a person perceived or a search found; decided. None measured.

### RT2-17 A gun found in a stop at War

- How it works: At War the police stop cars at two fixed points (the dock gate and the north road's junction at Quay Street's top) between 18:00 and 02:00, so the player can learn them. A gun found on Frank or in the cab at any stop: arrest on the spot, 12 hours, always a charge, the gun kept, Ellis's interest up one stage. A crewman driving a firm car with a gun in it is arrested instead and may break past his nerve.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-17 Test: B (bot), as written under RT2-17
- Source: design pass 3, RT2-17 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-17, 2.6.6; DESCRIPTION-COPY-2 §18, §27
- Status: decided. Coverage row: RT2-17.
- Studies: aaa-studies/FAILURE-AND-FRUSTRATION.md: FF-05 police know only what a person perceived or a search found; decided. None measured.

### FIT-G5 The beat constable's round

- How it works: At night the beat constable walks a fixed two-part beat at 1.1 m/s: a short round of about 200 m (up Quay Street past Mickey's, round the bend to the yards' lane, down to the quay road and back to the street's foot, about 3 real minutes, Mickey's door tried) and a landing leg of 240 m (about 3.6 minutes, 15 s looking over the landing), the whole cycle about 7 real minutes under either clock. Mickey's door is in his sight at least every 4 real minutes, the yards' lane and the landing every 7.5; with the street on edge a second constable walks half a cycle behind and the gaps become 2 and 4. The beat never changes by chance and two runs from the same save are identical; a rattled bin moves him off and he rejoins where he left. By day he walks Quay Street and the north road to the cold-store road.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §G5; FIT-CHECK F06, P53; DESCRIPTION-COPY-2 §18
- Status: decided. Coverage row: FIT-G5. Conflicts settled: C-049.
- Data (run 5): exact values in production/lane/blueprint/data/police.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

## 2.7 Money

Two pots: clean money in the fare book, night money in the tin.


### 2.7.1 Clean money and the fare book

- How it works: Clean money is in the fare book and can be spent anywhere. Every fare driven, by Frank or the firm's drivers, enters the book; rent (£18 every Friday) leaves it on its day. Drivers keep half each car's takings and the firm pays fuel and cover (his pick of 24 Nov; the £90 weekly wage is replaced, and how the driver's half passes through the book is not written: gap). Fares are few, £2.50 to £3.50 each, at least 7 in week one (his ruling of 24 Nov). Frank starts with £23.50. The old figure of about £85 to £95 a week from each driver, set against the £90 wage, is not recomputed (gap); a week of Frank's own fares pays Friday's rent. The book's balance always equals its flows, and it never goes below zero.
- Standard: Every fare driven, by Frank or the firm's drivers, enters the book; rent leaves it on its day; drivers keep half each car's takings and the firm pays fuel and cover (his pick of 24 Nov); the book's balance always equals its flows (ER-MONEY-01). Test: B: a week of fares and the drivers' halves; the book audited against the flows.
- Source: his ruling of 24 Nov (RULINGS on wip, his decisions page) (his picks, advisor 347; fares R11); earlier: the description, section 24; RT-17. Designed in: DEFINITIONS §2.7.1, G8, RT-17, RT2-06; DESIGN §9; DESCRIPTION-COPY-2 §20
- Status: decided (his ruling of 24 Nov sets the half split and the fare range; the rest is design). Coverage row: 2.7.1. Conflicts settled: C-286, C-287.
- Prior research: research/cab-office-1990: agent model (driver pays a weekly settle) against principal; settle about 49 to 54 pounds a week (derived from a 2004 figure and RPI, a 1990 figure not found), radio licence 120 pounds a year, VAT threshold 25,400 pounds; bears on the firm's takings, not Frank's 18 pound rent.
- Studies: aaa-studies/FAILURE-AND-FRUSTRATION.md: FF-02 a failure takes only the money the design names; decided. None measured.
- Economy (24 Nov, section 4, EC-02; his ruling): Each car's takings are split half to the driver and half to the book; the firm pays fuel and cover (the design also puts repairs on the book, about £46 a car a week in all). A dead rank gives a car £130 a week in takings, a good rank from rung 2 £210, the cold-store contract £40 more. Judgement (inferred from the old £85 to £95 figure, tuned in the run).
- Economy (24 Nov, section 4): Book from one car a week, owned / on terms: dead rank £19 / minus £3, good rank £59 / £37, with the contract £79 / £57. Cars are a slow earner and a sink until paid off; Mickey's two cars are the firm's Act I profit. Fuel £26 a week (13 gallons at £2.00; 1990 source: petrol £1.86 a gallon Oct 1989, Hansard 13 Feb 1990, with the autumn Gulf rise), cover £12 and repairs £8 (both judgement).
- Economy conflict C-320 (run 5): Settled: the part now carries his ruling of 24 Nov (drivers keep half each car's takings, the firm pays fuel and cover; the £90 wage is gone). Still open: the old £85 to £95 a week a driver in the part's text is not recomputed (gap); a dead-rank car brings the book £65 a week less its costs.

### 2.7.2 Night money and the tin

- How it works: Night money is in the tin at the office and cannot be explained. Every night job's take goes to the tin or the pocket, never the book except through the count, and nothing turns the book back into tin. The tin can be lost only by being stolen in an office break-in or found in the office search, and that is said in words. Night money spent where it can be seen to be explained (a car, a front's share) is a lie someone may one day have to hold up. A man's night cut is agreed in talk and paid from the tin.
- Standard: Every night job's take goes to the tin or the pocket, never the book except through the count; the tin can be lost only by being stolen or searched, said in words. Test: B: night jobs then the count; a break-in on the tin.
- Source: The description, sections 24, 26; RT-17. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.7.2, RT-17; DESIGN §9; DESCRIPTION-COPY-2 §20, §22
- Status: decided. Coverage row: 2.7.2.
- Studies: aaa-studies/FAILURE-AND-FRUSTRATION.md: FF-02 a failure takes only the money the design names; decided. None measured.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-02 no take over the greater of £150 or 1.5 weeks' income; Act II's last week 3 to 10 times Act I's; decided. None measured.
- Economy (24 Nov, section 2): Night money (debt book, runs, round, tobacco, loans, hooks, hold-ups, goods to a fence) goes to the tin or pocket. Night outgoings (men's cuts £10 to £40, men posted at rung 4 at £40 a week each, bribes, Ellis) are paid only from cash in hand; nothing turns the book into tin. Short pay is recorded and lowers that man's loyalty, never borrowed. Posts at £40 a week are judgement.

### 2.7.3 The wash

- How it works: At the count with Sheila, once a day and in twenty seconds, the fare book can hide £10 plus 80% of the fares really driven since the last wash, by Frank and by the firm's drivers. Over that, Sheila says so first ('That's more than the book will stand, love. You sure?'), thinks less of him, and each week over is recorded for the Act III inspection. A front's till raises the limit by a set amount a week. While the licence is suspended the count washes only the £10.
- Standard: The count never washes over the limit without Sheila's warning first; each week over is recorded for Act III; a front raises the limit by its set amount. The 80% and the front's amount are balance figures checked against GD-07's money curve. Test: B: counts at, under and over the limit; the record read by RT-01's grading.
- Source: The description, sections 26, 31; GD-07. (waits on a dated study). Designed in: DEFINITIONS §2.7.3, RT2-18; DESIGN §9 (ER-MONEY-04); DESCRIPTION-COPY-2 §21
- Status: pending. Coverage row: 2.7.3.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-06 money held at Act III's start never changes a morning's grade; decided. None measured.
- Prep: NUMBERS-RUN M4: the wash binds only the hard player (over 100 per cent of the limit in 3 of 7 weeks at mid amounts, all 7 at high); counting drivers' fares at 40 per cent and Frank's own at 80 per cent makes the steady player use 109 to 143 per cent in six of seven weeks. A rule change to record, his to overturn; the 80 per cent is PENDING (GD-07).
- Data (run 5): the data sweep (class B) sends its exact figures to the economy job: production/lane/blueprint/economy/ECONOMY-DESIGN-2026-11-26.md (see the Economy lines).
- Economy (24 Nov, section 2, from NUMBERS-RUN M4): The wash counts 40% of drivers' fares and 80% of Frank's own, plus £60 a week for each front. M4 is used as written; the 80% and the front's amount are marked balance figures.
- Economy conflict C-332 (run 5): The part says the count hides £10 plus 80% of all fares really driven, by Frank and drivers alike. The design (M4) counts drivers' fares at 40% and Frank's at 80%, plus £60 a week a front; the design wins (the 80% was pending).
- Story needs (frame, 24 Nov): the wash and the count, including the habit line "Same as your first night?" (SYSTEMS-THE-STORY-NEEDS S42, S18). Covered for the wash; the stored line is under 3.6.5.

### 2.7.4 Rent and running costs

- How it works: Rent is £18 every Friday, owed to the landlord's agent, a named man who calls at the counter; drivers keep half each car's takings and the firm pays fuel and cover (his pick of 24 Nov; the £90 weekly wage is replaced). Doing nothing misses Friday's rent; a week of Frank's own fares alone pays it (fares £2.50 to £3.50 each, at least 7 in week one: his ruling of 24 Nov). A missed Friday becomes arrears said in the Ledger and by the agent on Monday; two missed: a letter and notice to quit the flat above in a fortnight; three: the flat is let and Frank sleeps in the office. The office itself is never lost, and paying arrears ends the ladder. A car hit at about 35 mph is off the road for a day.
- Standard: Doing nothing misses Friday's rent; a week of fares alone pays it (ER-MONEY-03). The £18 rent sits in the 1990 band: council £23.36 a week (Apr 1990), private £65 (1991); cab running costs from 1990 fares (about £1.04 a mile London cab) and diesel about 38p a litre (economy/PRICES-WAGES-1990.md, a dated figure; the economy design's own working uses 36p a litre in section 8 and £2.00 a gallon elsewhere, to be reconciled by the economy lane). Test: S: both weeks scripted
- Source: CLOUD-FIGURES-2026-11-21.md B1: Hansard 27 Jun 1990, 15 Apr 1993, 30 Jan 1992, 18 May 1990 (real-world figure or published standard). Designed in: DESIGN §9 (ER-MONEY-03); CLOUD-FIGURES B1; DEFINITIONS RT-16, G8; DESIGN §5
- Status: sourced (dated real-world figure or published standard; not a five-sample measurement). Coverage row: 2.7.4. Conflicts settled: C-050, C-286, C-287.
- Prior research: production/art/atlas-02: average gross weekly earnings 263.10 pounds; research/street-lines-1990: prescription 3.05 an item from 1 Apr 1990, dental check 3.15; archived DECISIONS 13 Oct: cod 2.60 a pound (one source).
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-03 each rung adds a weekly cost; outgoings at least half of income each Friday; decided; MP-04 the lazy bot pays every Friday's rent; needs fares near £2.50 to £3.50; decided. None measured.
- Economy (24 Nov, section 2): Rent stays £18 every Friday; office running £12 a week (phone, electric, radio licence; judgement). 1990 source: radio licence £120 a year (cab research S11); council rent £23.36 (Hansard 27 Jun 1990); private terrace £35 and rooms £25 are judgement. Diesel is about 36p to 38p a litre, not 45p (1990 source: 34.2p to 37.3p a litre, Jan to Oct 1989, Hansard 13 Feb 1990).
- Economy conflict C-321 (run 5): The part says diesel about 45p a litre. The design (newer) wins: about 38p a litre from the dated prices file (the design's section 8 says 36p and £2.00 a gallon elsewhere, to be reconciled by the economy lane). The wage half is already replaced.

### 2.7.5 Purses, tills and shops

- How it works: Everybody's money is somebody's circumstance: a debtor, a shopkeeper or a fence pays only what is in the purse or the drawer. Shops keep hours, restock weekly, and Thursday's market empties them. A shop buys, haggles or refuses, and remembers a robber, a man who walked out of a haggle, a man who robbed the shop next door. A haggle is three offers at most: the buyer names a price, Frank asks more, takes it, or walks; the buyer's answers come from his purse, how hot the goods are and how he regards Frank; no number shows except prices spoken. Walking away is remembered. No price tables, stock or supply chains.
- Standard: Purses and a weekly restock stay; no price tables or supply chains (DESIGN §18) Test: S: a shop refuses and remembers; addendum rules ER-HAGGLE-01
- Source: DESIGN §9, §18 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §9, §18; DESIGN-ADDENDUM A30; DESCRIPTION-COPY-2 §14; DEFINITIONS G10
- Status: decided. Coverage row: 2.7.5.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-05 every buyer has a weekly purse; a refusal or part-payment in the last two weeks; decided. None measured.
- Shopkeepers remember (catalogue 23 Nov, rank 2; seen in 3 games): The grocer and newsagent remember Frank's last visit and any trouble. Partly: shops already remember a robber or a walked-out haggle; short is a clerk asking after the last visit, and trust or a quicker call to the police following. Feature only; no timing; the part's status is unchanged.
- Townspeople visibly buy (catalogue 23 Nov, next tier): People are seen buying, and the calls match the stock. Not yet: the part holds shop stock and haggling but not visible buying or calls matching stock. Feature only; no timing; the part's status is unchanged.
- Data (run 5): the data sweep (class B) sends its exact figures to the economy job: production/lane/blueprint/economy/ECONOMY-DESIGN-2026-11-26.md (see the Economy lines).
- Economy (24 Nov, sections 1 and 6, EC-04): Each shop has weekly takings, costs, its owner's draw and a margin, which is its purse (margins £44 to £175: fishmonger £1,100 takings, grocer £1,500, newsagent £1,900, launderette £420, caff £750, chip shop £900, ironmonger £650, tea room £380, pawn £700). Takings fall when its board rises and while it is afraid. Four losing weeks in a row and it shuts, saying so at two; no shop shuts without a cause the town can name. Judgement throughout (shops file section 5); this keeps "no price tables, stock or supply chains".
- Economy (24 Nov, section 6, EC-05): Prices move only on a shop's own board, for a cause. A shop on a round pays out of up to 60% of its margin; past that, half the excess goes on its board (chalked over, capped at a quarter over) and half off its purse. The town says "prices are up" at 10% and "steep" at 25%. With no squeeze, robbery or rival, a board never moves. Judgement (Economy.cs's words).

### 2.7.6 Fencing

- How it works: Rita's back room (open from rung 2) buys hot goods at about a third of retail (0.33): about 0.2 for jewellery up to 0.4 for a video recorder, less for each further piece the same week. Buyers differ: the second-hand shop takes radios and video recorders, the scrap yard car parts, a man at the back of the caff jewellery, and Wayne's pawn takes goods too; each is also a listener. Rita refuses or lowballs goods whose deed is still hot in talk. A haggle is three offers at most, and no price table shows. Buyback (his list of 24 Nov): 7 game days, price plus a quarter; fences hold nothing (what is bought back, and from whom, is not written: gap).
- Standard: About a third of retail (0.33), from 0.2 for jewellery to 0.4 for a video recorder; less for each further piece the same week; buyers differ in what they take (second-hand shop radios and video recorders, scrap yard car parts, a man at the back of the caff jewellery); each is also a listener. No price table on screen. Test: S: golden rows
- Source: CLOUD-FIGURES-2026-11-21.md B3: Sutton 2014; AIC 2002; BOCSAR 1998 (real-world figure or published standard); buyback: his ruling of 24 Nov (RULINGS on wip, his decisions page). Designed in: CLOUD-FIGURES B3; DESIGN §4, §9; GTAVI-MAP Y2.7; DESIGN-ADDENDUM A30; DESCRIPTION-COPY-2 §14
- Status: sourced (dated real-world figure or published standard; not a five-sample measurement). Coverage row: 2.7.6. Conflicts settled: C-051.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-02 no take over the greater of £150 or 1.5 weeks' income; Act II's last week 3 to 10 times Act I's; decided. None measured.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-05 every buyer has a weekly purse; a refusal or part-payment in the last two weeks; decided. None measured.
- Data (run 5): the data sweep (class B) sends its exact figures to the economy job: production/lane/blueprint/economy/ECONOMY-DESIGN-2026-11-26.md (see the Economy lines).
- Economy (24 Nov, sections 5.5 and 6, EC-10; his ruling): Buy-back: within 7 game days the shop or pawnbroker that bought an item sells it back at what it paid plus a quarter; a fence holds nothing. Test: a radio sold for £12 is £15 on day 6, gone on day 8.
- Economy (24 Nov, section 5.5): A lift pays about a third of retail at a fence (about £40), a fifth less for each further piece the same week; Rita opens at rung 2; a lift cools in a day or two. Judgement; the fence's third is inferred from later studies (Sutton 2014, AIC 2002, BOCSAR 1998). Best repeatable lever, £305 to £340 an hour; ten lifts a week bring about £100 more than two at the cost of three arrests.
- Economy conflict C-330 (run 5): The part has no buy-back and says Rita holds goods for sale on. His ruling says the buyer sells back within 7 game days at price plus a quarter and a fence holds nothing; the ruling wins.

### 2.7.7 Flows ledger

- How it works: No money from nowhere: every pound in or out is a flow from a person, a purse, a fare, a till, a wage or a bribe, and every pound balances. The firm's takings are said when they come in. Frank always knows in words what he has and what is owed by Friday, for example '£31 in your pocket. The tin has about £40 in it. Rent, £18, Friday. Darren still owes £12.'
- Standard: ER-MONEY-01 Test: S: no money from nowhere
- Source: DESIGN §9 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §9 (ER-MONEY-01, -02); DESCRIPTION-COPY-2 §20
- Status: decided. Coverage row: 2.7.7.

### 2.7.8 Spending

- How it works: Money buys position, spoken by the seller and never shown as a table. The newsagent and tobacconist (20 cigarettes £1.70, the paper 25p), the caff (tea 30p, a meal £2.50), the ironmonger (crowbar £6, torch £4, key cut £1.50), coats (second-hand £15, the decent jacket £45, the good overcoat £90), the barber £4, a used car £600 to £1,200, the retired doctor's stitches £20, a solicitor's brief £50 a week, a bought officer £50 or £200, DS Ellis about £800 and then £100 a week (his ruling of 24 Nov), a man's night cut £10 to £40. Each shop sells only its list, by its hours, from its purse.
- Standard: What money buys is position (DESIGN §9); purses and weekly restock, no price tables (DESIGN §18) Test: S: each shop sells its list; H: 'what did you spend on?'; addendum rules ER-SPEND-01
- Source: DESIGN §9, §18 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN-ADDENDUM A21; DEFINITIONS G8; DESCRIPTION-COPY-2 §14; DESIGN §9, §18
- Status: decided. Coverage row: 2.7.8. Conflicts settled: C-282.
- Studies: aaa-studies/IMMERSION-FEATURES.md: IM-02 every daily act pays in the town; decided. None measured.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-01 on every Friday a wanted thing on the bot's own path is out of reach; the hard player at high amounts and fares-only player fail on the numbers run; decided. None measured.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-03 each rung adds a weekly cost; outgoings at least half of income each Friday; decided; MP-07 no purchase raises a fighting, driving or speaking value; decided. None measured.
- Data (run 5): the data sweep (class B) sends its exact figures to the economy job: production/lane/blueprint/economy/ECONOMY-DESIGN-2026-11-26.md (see the Economy lines).
- Economy (24 Nov, section 3 and prices file section 1): Spoken or written prices: 20 cigarettes £1.70 (1990 source: 161p on 12 Feb 1990, Hansard 14 Feb 1990, rising after the March Budget), paper 25p, tea 30p, caff breakfast £1.80 (judgement), caff meal £2.50, chip shop fish and chips £1.60 (judgement), milk 30p a pint (1990 source: 30.5p, Hansard 15 Mar 1991), sliced loaf about 52p (derived from 48.8p in 1989, Hansard 28 Feb 1990), bus 45p (judgement). Other list prices as the part has them (design-held).
- Economy (24 Nov, prices file section 3): Property for talk: council house £23 a week, private terrace £35, rooms £25 (judgement), a shop unit on the parade £25 to £35 a week (judgement), a terraced house to buy about £25,000 (1990 source: North £37,374 in 1989, Hansard 9 Jul 1990, set well under).

### GD-07 Economy over weeks: what money buys and how it rises across about 20 hours

- How it works: Money buys position, never numbers. Act I: £23.50, rent £18 a week, a week of fares pays it, the debts £156. Act II: what money buys rises with the rung (a third car, a driver's wage, men's cuts, a front's share, a bribe to a bought man, the decent jacket, the good overcoat, the doctor). Act III: money cannot buy the books clean. Sinks never run dry before Act III: at each act's end, for a greedy and a lazy bot, one named thing on the rung ladder is still out of reach. A car on a good rank brings £110 to £140 a week from rung 2 (set against the old wage, not recomputed: gap). The main story aims at about 20 hours, measured in the first loops (his ruling of 24 Nov, replacing 15 to 20 hours). Drivers keep half each car's takings and the firm pays fuel and cover; an honest firm stops at rung 2 (his picks of 24 Nov).
- Standard: The players study punishes money with nothing to buy (GTA V and RDR2 late game). Pass: at each act's end, in both a greedy and a lazy bot playthrough, at least one named thing on the rung ladder he does not yet hold is still out of reach of his money; the curve's shape is set from the reference games' money over a playthrough. Test: B: an economy bot playing greedy and lazy; the curve plotted against the rung ladder.
- Source: The description, sections 24, 28, 31, 32; MEASUREMENTS-NEEDED A (money over a playthrough); PLAYERS-KCD2-GTAV-RDR2 complaints. (waits on a dated study). Designed in: DEFINITIONS §GD-07, G8; DESCRIPTION-COPY-2 Economy over weeks; FIT-CHECK F24
- Status: pending. Coverage row: GD-07. Conflicts settled: C-281, C-286, C-288.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-01 on every Friday a wanted thing on the bot's own path is out of reach; the hard player at high amounts and fares-only player fail on the numbers run; decided. None measured.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-02 no take over the greater of £150 or 1.5 weeks' income; Act II's last week 3 to 10 times Act I's; decided. None measured.
- Prior research: aaa-studies/MONEY-AND-PROGRESSION.md: reference ratios for the numbers run: RDR2 late cash a few times to about 20 times its dearest common buy; GTA V biggest take about 33 times its first; KCD2 buyers run out of money. Thin figures, none measured.
- Prep: NUMBERS-RUN M2: GD-07's test (a named thing out of reach at every act's end) should also be run on a fares-only player; for him money stops mattering by week 3 at a high fare.
- Data (run 5): the data sweep (class B) sends its exact figures to the economy job: production/lane/blueprint/economy/ECONOMY-DESIGN-2026-11-26.md (see the Economy lines).
- Economy (24 Nov, section 7, EC-12): Run of four styles over 13 weeks (7 story, 6 after), 300 noisy runs each (takings within 15%), breakages 0. Worth at weeks 1/3/5/7/13: honest 92/146/398/188/147, racketeer 199/459/693/785/1,207, mix 149/141/191/584/1,222, lazy 45/133/262/109/742; wants left at week 7: honest 4, racketeer 2, mix 2, lazy 5. Pass: nobody rich by week 3, nobody broke with no way back, no causeless shop closing (0 in 1,200), the lazy player pays every Friday's rent, a named want out of reach at week 7, no lever over twice the middle one an hour (best lift 339 against middle 182), flows balance every week.
- Economy (24 Nov, section 7): Pounds an hour of Frank's hands (judgement, from effort estimates): lift £305 to £339, smuggled tobacco £240, landing run £200, round £177 to £182, loans £41 to £82, fares £55.

### RT-16 Missed rent

- How it works: Rent is owed to the landlord's agent, a named man who calls at the counter. A missed Friday becomes arrears said in the Ledger and by the agent on Monday; two missed: a letter and notice to quit the flat above in a fortnight; three: the flat is let to someone else and Frank sleeps in the office. The office itself is never lost, arrears can be paid at any time, which ends the ladder. No game over, no dead end.
- Standard: Each step on its Friday; paying clears it; the office itself is never lost at any point in the game (only the flat above). Test: B: the do-nothing run through three Fridays; a pay-late run.
- Source: The description, sections 24 (rent), 3 (no game over); the doing-nothing run of S23. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT-16; DESIGN §9; DESCRIPTION-COPY-2 §20
- Status: decided. Coverage row: RT-16.
- Studies: aaa-studies/FAILURE-AND-FRUSTRATION.md: FF-08 a forced-failure bot still finds jobs, rent and two brakes it can act on (talk it down, buy it quiet, a favour) the next week of Act II; decided. None measured.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-04 the lazy bot pays every Friday's rent; needs fares near £2.50 to £3.50; decided. None measured.
- Prep: NUMBERS-RUN M2, M5: at the Act I firm rate and a 1.30 fare the book loses 21 a week, so rent goes unpaid, RT-16's ladder lets the flat by week 4 and wages go unpaid (RT2-06); nothing in the money rules can end the game itself.

### RT-17 Money pots in practice

- How it works: Money is in three places: the pocket, the tin (night money at the office, which cannot be explained) and the book (clean money, spent anywhere). Rent comes out of the book weekly (the £90 wage is replaced by drivers keeping half each car's takings, his pick of 24 Nov); a car, a front's share, shops and the doctor can be paid from the book or from cash; bribes and men's night cuts come from cash. The count turns tin money into book money within the wash limit; nothing turns the book back into tin. The tin can be stolen in an office break-in and is then gone, said in words. A constable's search finds what is under the coat and in the hand, cash included, and keeps what it finds.
- Standard: Every payment draws from a place the rules allow; the flows ledger balances (ER-MONEY-01); a search keeps exactly what was found. Test: B: every kind of payment from each place; a break-in; a night search with cash on Frank.
- Source: The description, sections 21 (what he finds he keeps), 24 (two pots; clean money spent anywhere), 26 (the count), 27 (cut from the tin). (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT-17, §2.7.2; DESCRIPTION-COPY-2 §20 to §22
- Status: decided. Coverage row: RT-17. Conflicts settled: C-286.
- Studies: aaa-studies/FAILURE-AND-FRUSTRATION.md: FF-02 a failure takes only the money the design names; decided. None measured.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-03 each rung adds a weekly cost; outgoings at least half of income each Friday; decided. None measured.
- Economy (24 Nov, section 2): Which pocket pays: rent, office running, fuel, cover, repairs and car terms (£22 a week each) come from the book; men's night cuts, men posted, bribes and Ellis's retainer from cash only; loans come out of the tin first.

### FIT-G8 Prices of what money buys

- How it works: Every item on the spending list has a price, spoken by the seller and never shown as a table (1990 prices, to be checked): 20 cigarettes £1.70; the paper 25p; tea at the caff 30p; a caff meal £2.50; a crowbar £6; a torch £4; a key cut £1.50; a second-hand coat £15; the decent jacket £45; the good overcoat £90; the barber £4; a used car £600 to £1,200; the doctor's stitches £20; a brief on call £50 a week; a bought officer £50 to look away once, £200 to lose a statement once; DS Ellis about £800, then £100 a week, a missed week ending it (his ruling of 24 Nov). A driver keeps half his car's takings and the firm pays fuel and cover (his pick of 24 Nov; the £90 wage is replaced); a man's cut £10 to £40. A fare is £2.50 to £3.50 (his ruling of 24 Nov). The old book figures set against the wage (about £85 to £95 a driver in Act I; £110 to £140 a car from rung 2) are not recomputed (gap).
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (waits on a dated study). Designed in: DEFINITIONS §G8; FIT-CHECK F24, P15; DESCRIPTION-COPY-2 §14
- Status: pending. Coverage row: FIT-G8. Conflicts settled: C-052, C-282, C-286, C-287.
- Studies: aaa-studies/IMMERSION-FEATURES.md: IM-02 every daily act pays in the town; decided. None measured.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-01 on every Friday a wanted thing on the bot's own path is out of reach; the hard player at high amounts and fares-only player fail on the numbers run; decided. None measured.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-03 each rung adds a weekly cost; outgoings at least half of income each Friday; decided; MP-04 the lazy bot pays every Friday's rent; needs fares near £2.50 to £3.50; decided. None measured.
- Prep: NUMBERS-RUN sections 1 and 2: the design gives no pence a mile; at a London 1990 fare of 1.30 the first week's rent of 18 needs 14 fares against about 6 offered, so a typical Hook fare should pay 2.50 to 3.50 (answered 24 Nov: his ruling sets fares at 2.50 to 3.50, at least 7 in week one). The driver's wage of 90 is low against 1990 average earnings of 263.10 (ONS, art sheet) unless part-time or commission; minicabs needed no meter in 1990, so the fare rate may be the firm's price board (a lead).
- Data (run 5): the data sweep (class B) sends its exact figures to the economy job: production/lane/blueprint/economy/ECONOMY-DESIGN-2026-11-26.md (see the Economy lines).
- Economy conflict C-325 (run 5): Settled: the part now carries his ruling of 24 Nov on the wage and the design's dated prices. Still open: the old £85 to £95 a driver and £110 to £140 a car in the part's text are not recomputed (gap); G8 moves from pending to sourced or inferred as the prices file labels.

### FIT-F24 Money over nine weeks (in against out; seven under the ruled clock)

- How it works: In week one Frank's own fares (at least 7, each £2.50 to £3.50: his ruling of 24 Nov, replacing about 18 at around £1.30) come to £17.50 to £24.50 for seven, set against the £18 rent (seven fares at £2.50 is £17.50, under the £18 rent: at the low fare 8 are needed; gap for the design proof), and the debts alone could bring £156; after week one there is nothing to compare, and the worry is money that stops mattering. The fix is G8's amounts for the spending list, then a money run over the whole calendar on the sim once the figures exist (cloud, by Sat 28 Nov). The related wash row (F25) needs night income, which has no amount; the count can hide at least £70 a week plus 80% of the firm's fares (the economy design counts drivers' fares at 40% and Frank's at 80%: C-332).
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (waits on a dated study). Designed in: DEFINITIONS §G8, GD-07; FIT-CHECK F24, F25
- Status: pending. Coverage row: FIT-F24. Conflicts settled: C-053, C-287.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-01 on every Friday a wanted thing on the bot's own path is out of reach; the hard player at high amounts and fares-only player fail on the numbers run; decided. None measured.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-02 no take over the greater of £150 or 1.5 weeks' income; Act II's last week 3 to 10 times Act I's; decided. None measured.
- Data (run 5): the data sweep (class B) sends its exact figures to the economy job: production/lane/blueprint/economy/ECONOMY-DESIGN-2026-11-26.md (see the Economy lines).
- Economy (24 Nov, section 7): Money ratio (MP-02), Act II's last week against week one, counting income before outgoings and leaving out the debt book, judged on the mean curve: honest 3.7, mix 7.0, racketeer 10.0 (the top of the 3 to 10 band). No single take over the greater of £150 or 1.5 weeks' income. Single noisy weeks outside the band are reported, not failed.
- Economy conflict C-326 (run 5): Settled: the part now carries his ruling of 24 Nov (fares £2.50 to £3.50, at least 7 in week one; £1.30 dropped). Still open: seven fares at £2.50 are £17.50, under the £18 rent (gap for the design proof).

## 2.8 Debts

Mickey's debt book.


### 2.8.1 The five debtors

- How it works: Mickey's debt book holds five debts and five lessons, £156 in all: Darren Milner £22 (pays in what he hears); Wayne Harrison £30 (pays in goods from the pawn's back room, haggled); Lee Drewery £15 (stands, with the docks behind him, and it comes to blows); Julie Kettlewell £9 (cannot pay: mercy or shame); Dennis Iveson £80 (has the money, a yard and a yard hand in his twenties; three keys: front up the yard hand, the hut at night, or lean on what he bought out of the burned warehouse). In the first hour Frank can front Darren up, take what he hears, or strike the debt out.
- Standard: Each debt teaches a different answer (DESIGN §4) Test: H: the five debts named as different
- Source: DESIGN §4 (no reference figure yet). Designed in: DESIGN §4; ONE-SHOT-PROMPT 25, 4 (5:30); DEFINITIONS RT2-05
- Status: unmeasured. Coverage row: 2.8.1.
- Data (run 5): exact values in production/lane/blueprint/data/people/ (data build wave 2, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.
- Story needs (frame, 24 Nov): the debts (SYSTEMS-THE-STORY-NEEDS S41). Covered.

### 2.8.2 Partial payment and the book

- How it works: A debtor pays what his purse holds and the rest stays on the book, said in the Ledger's Money page ('Darren still owes £12'). Fronting up is a collection in person on the lower rungs: a stare, a word, a shove. Squeezing a debtor and letting a debt go are both told on the street, as a told version within a game day. A round, later, is the same collection repeated by a man of his crew.
- Standard: A payment never exceeds the debtor's purse; the remainder stays and is said in the Ledger's Money page; a squeeze or a let-off produces a told version within a game day. Test: B: each of the five debtors fronted up with different purses.
- Source: The description, section 25. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.8.2; ONE-SHOT-PROMPT 25; DESIGN §4; DESCRIPTION-COPY-2 §20
- Status: decided. Coverage row: 2.8.2.
- Studies: aaa-studies/TALK-AS-PLAY.md: TALK-03 a fact Frank holds changes the reply and is named; a wrong push ends in a state, never a reload; decided. None measured.
- Economy (24 Nov, section 2): Mickey's debt book stays £156, five debts (Darren in news, the other four in money or goods); it is left out of the money-ratio check as inherited. A debtor pays on Friday or not at all, since households have a few pounds left on Friday night and little by Thursday.

## 2.9 The outfit and the arrangement

The run to the ferry landing that Mickey kept.


### 2.9.1 The asks

- How it works: In Act I the outfit asks on nights one, three, five and seven, at most one a night. Ron brings it in person after dark: a dark coat and an envelope for the ferry landing after ten. Frank can go, say no (asked twice), or stay away; staying away means Ron leaves the envelope with Sheila's word and the ask ends unanswered, written in the Ledger. No ask comes twice before it is taken. At the landing a man says 'Mickey's?', the hand-over plays and Frank's cut comes back into the tin. If a constable stops him and searches, the envelope is kept and the ask fails as a state the outfit hears of.
- Standard: At most one ask a night, every other night in Act I (DESIGN §6) Test: S: ask schedule in a seeded week
- Source: DESIGN §6, §16 (no reference figure yet). Designed in: DESIGN §6, §16; ONE-SHOT-PROMPT 4 (7:00 to 11:30), S04, S05
- Status: unmeasured. Coverage row: 2.9.1.
- Studies: aaa-studies/TALK-AS-PLAY.md: TALK-02 each decision talk has two outcomes that turn on state he can see or know, reason said; decided. None measured.
- Data (run 5): the data sweep (class B) needs the scenes file (data file 18), still to be made from the story on paper; exact values pending it.
- Economy (24 Nov, section 5.6): Frank's cut of a run to the ferry landing is £20, on nights one, three, five and seven of Act I (about £200 an hour of his hands, judgement). A stop and search keeps the envelope.
- Story needs (frame, 24 Nov): the outfit's asks on nights 1, 3, 5, 7 and the arrangement kept or ended (SYSTEMS-THE-STORY-NEEDS S34). Covered.

### 2.9.2 Keeping or ending the arrangement

- How it works: Kept (he went to the landing and took the firm on): the landing men hand him their end of the Hook in Act II and fade, the asks become his own runs, and he becomes what Mickey was: night money, cover and asks that grow. Ended (wound down or refused): the ground is open, every rival's ladder starts one rung up and each rival's first visit comes earlier on the game clock; freedom without cover. Winding down ends only Mickey's arrangement, never the cab trade. Both roads reach Act II at rung 2.
- Standard: Kept gives the hand-over beat; ended starts every rival one rung up; both reach rung 2 (RT-04). Test: B: week-one runs kept and ended; the Act II state compared.
- Source: The description, sections 36, 37; RT-04. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.9.2, RT-04, RT2-01; DESIGN §16; DESCRIPTION-COPY-2 §30, §31; ONE-SHOT-PROMPT S31
- Status: decided. Coverage row: 2.9.2.

### RT2-01 The cold-store contract and rung 3 are circular

- How it works: The contract comes before rung 3, never from it. The cold stores' shift manager (a named minor man) offers it once the firm has met the packing shift on time on five mornings in one game week and holds at least four cars; winning it opens the dock gate. Rung 3 is reached with five cars, a night desk, a first front, a first round and the contract. It is open on every road out of Act I, wound down included. It is lost after three missed mornings in one game week (its fares stop and the dock gate's daily pass goes, but no rung or name goes back), paused while the licence is suspended, and can be won again once, the same way.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-01 Test: B (bot), as written under RT2-01
- Source: design pass 3, RT2-01 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-01; DESIGN §14; DESCRIPTION-COPY-2 §25
- Status: decided. Coverage row: RT2-01. Conflicts settled: C-054.
- Prep: NUMBERS-RUN M3: no rule says who pays for the third car; at 600 to 1,200 a car the third car runs in week 4 at best and week 7 at worst, only the hard player at high amounts reaches five cars (week 7); a car earns the book 20 to 50 a week over its driver's wage, so cars are a pure sink. Fix proposed: hire purchase (a tenth down, 15 to 25 a week from the book).

## 2.10 Rivals

Three heads, each going after a different ledger.


### 2.10.1 Rival ladders

- How it works: Each rival climbs the same ladder: noticed, a visit, pressure, a threat, a sit-down. No rung is skipped and each is said to his face or shown on his street within a game day. Every climb is lifted from the rung below by a state: noticed by the first thing its people see or hear of Frank; a visit by two more sightings or tellings, or Frank reaching rung 2; pressure by refusing the visit, rung 3 or a deed against its men; a threat by defying or countering a pressure or a second deed; the sit-down by defying the threat, rung 4 or one of its men killed. Paying holds a rival two game weeks unless Frank does a deed against him.
- Standard: ER-RIV-02 Test: S: no rung skipped, each said or shown
- Source: DESIGN §13 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §13 (ER-RIV-02); DEFINITIONS RT2-07, RT-04; DESCRIPTION-COPY-2 §24
- Status: decided. Coverage row: 2.10.1. Conflicts settled: C-055.
- Studies: aaa-studies/PLAYERS-STORIES.md: STORY-05 a rival's man meets Frank twice; every man he beat meets him within three game days; decided. None measured.
- Story needs (frame, 24 Nov): rivals climb noticed, visit, pressure, threat, sit-down with the fail-safe (SYSTEMS-THE-STORY-NEEDS S3). Covered; the rivals' lieutenants and men are not yet named in the part.

### 2.10.2 Rival eyes

- How it works: Each rival knows only what its own people saw or heard. Each has eyes among the regulars: Lee Drewery and Kevin Needham for the docks, Susan Coverdale for Agar, Rita Welburn for Cammack, so the first thing the Widow learns of Frank may come from his own day driver over a radio nobody can help overhearing. Every rival move traces to something one of its people saw or heard. Each rival has a base, a named lieutenant and three named men with routines.
- Standard: ER-RIV-01 Test: S: every rival move traces; ER-EYES-05 no all-knowing town: every reaction by a neighbour, the police or a rival prints its chain of sightings
- Source: DESIGN §13; Core rule (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §13 (ER-RIV-01); DESCRIPTION-COPY-2 §24; DEFINITIONS RT2-08
- Status: decided. Coverage row: 2.10.2.
- Studies: aaa-studies/PLAYERS-STORIES.md: STORY-03 half the moments come from witnesses, recognition or a returning person; physics and driving alone never count; decided; STORY-05 a rival's man meets Frank twice; every man he beat meets him within three game days; decided. None measured.
- Data (run 5): exact values in production/lane/blueprint/data/people/ (data build wave 2, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### 2.10.3 Pressures and answers

- How it works: The Widow taxes his drivers at the dock gate and poaches his least loyal man; Agar sends paper (the licence letter, a solicitor's letter, an inspection of the cars); Cammack brings heat (trouble on Quay Street outside Mickey's). Every pressure has three answers: pay, defy, or counter with what he knows (which needs a hook Frank holds); none ends the game. At the threat rung each shows one harm in its style (the office window put in, a licence hearing date, car two's tyres slashed), all repairable for money and a day. Paying holds a rival on its rung two game weeks.
- Standard: ER-RIV-03: three answers, none ends the game Test: S: each pressure's three answers
- Source: DESIGN §13 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §13 (ER-RIV-03); DEFINITIONS RT-06, RT2-07, RT2-18; DESCRIPTION-COPY-2 §24
- Status: decided. Coverage row: 2.10.3.
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-08 every sit-down and 80% of Act II beats name a deed of Frank's the speaker holds; decided; MEM-11 no memory closes the game or a main thread; another road within a game day; decided. None measured.
- Data (run 5): exact values in production/lane/blueprint/data/happenings.json (data build wave 2, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Economy (24 Nov, section 5.8): The Widow's tax is £5 a car a week at the dock gate once Frank has five cars, until answered (by a man posted there at £40 a week, a cost the run leaves out). Judgement.
- Story needs (frame, 24 Nov): each outside power (police, docks, council, press, Customs) as a named power with one want and one fear the story can read, and the docks as a workforce (SYSTEMS-THE-STORY-NEEDS S5). Partly covered by the rivals' pressures; missing is the powers table for the non-rival factions.

### 2.10.4 The Fixer

- How it works: Keith Garbutt, the Fixer, brokers between all three rivals and sells three things: true reads of a rival (true to what the town really holds at that moment), a meeting that then happens, and one truce that holds a rival at its rung for exactly two game weeks, offered once a game. He carries a pager: paged from a box, he rings that box back within half a game hour. His prices follow the economy curve.
- Standard: Every read he sells is true to the town's memory at that moment; a meeting he brokers happens; the truce holds exactly two game weeks and is offered once. His prices follow GD-07's curve. Test: B: reads compared with the rival's true state; truce timing.
- Source: The description, sections 29, 30; RT-06. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.10.4, RT-06, RT2-19; DESIGN §13; DESCRIPTION-COPY-2 §24
- Status: decided. Coverage row: 2.10.4.
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-08 every sit-down and 80% of Act II beats name a deed of Frank's the speaker holds; decided. None measured.
- Data (run 5): exact values in production/lane/blueprint/data/people/ (data build wave 2, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Story needs (frame, 24 Nov): Garbutt's one truce a game and paying a rival to hold him two game weeks (SYSTEMS-THE-STORY-NEEDS S9). Covered; amounts are gaps.

### RT-05 The two rivals not met at Act II's end

- How it works: After Act II's sit-down with one head, the two rivals whose ladders did not reach it keep their rung into Act III and their weekly pressure continues; neither is absorbed or defeated by the story alone. Act III's close names each: what they hold and what they call him.
- Standard: After the sit-down, both other rivals' rungs are unchanged by it, their weekly pressure continues, and the close names both. Test: B: an Act III run checking the other two ladders' state and pressure each day.
- Source: The description, sections 29, 37, 39. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT-05; DESCRIPTION-COPY-2 §38
- Status: decided. Coverage row: RT-05.

### RT-06 Rival threat rung and counters

- How it works: At the threat rung each rival shows one harm in its own style, said to his face or shown on his property, never yet done to a person: the Widow's men put the office window in or tell a driver he will not drive again; Agar's solicitor names a date for the licence hearing; Cammack's lads slash car two's tyres on the rank. Property harm is repaired by people for money and a day (the glazier, the tyre man) and the street sees it. A counter spends a hook Frank holds. The Fixer's truce holds a rival two game weeks, once a game.
- Standard: Each rival's threat rung shows one harm in its own style; every harm repairable; a counter needs a hook Frank holds; a truce holds exactly two game weeks. Test: B: ladder runs to the threat rung for each rival; counter with and without a hook.
- Source: The description, sections 29, 30. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT-06, RT2-18; DESCRIPTION-COPY-2 §24, §38
- Status: decided. Coverage row: RT-06.
- Studies: aaa-studies/MISSIONS-AND-SIDE-QUESTS.md: MS-08 a threat Frank ignores is kept within the time named, else three game days; decided. None measured.
- Data (run 5): exact values in production/lane/blueprint/data/happenings.json (data build wave 2, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### RT2-07 What moves a rival up his ladder

- How it works: Each rival rung is lifted by a state, from the rung below, never two, never by time alone: noticed on the first thing its people see or hear of Frank; a visit on two more sightings or tellings of his firm on that rival's ground, or Frank reaching rung 2; pressure on refusing the visit, rung 3 or any deed against its men or property; a threat on defying or countering a pressure or a second deed; the sit-down on defying the threat, rung 4 or one of its men killed. A deed against a rival lifts him one rung at once. Paying at a rung holds that rival there two game weeks unless Frank does a deed against him. Each climb is said to Frank's face or shown on his street within a game day. The only climb on time is the fail-safe.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-07 Test: B (bot), as written under RT2-07
- Source: design pass 3, RT2-07 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-07, RT-04, RT-06; DESCRIPTION-COPY-2 §24
- Status: decided. Coverage row: RT2-07. Conflicts settled: C-056.
- Prep: NUMBERS-RUN R1 to R3: as written an aggressive player's Act II ends on day 12 (Widow noticed day 8, sit-down day 12); a payer sees rung changes only in weeks 1 and 5. Fix A one rung a rival every 5 game days (hard player ends day 28); fix B a paid rival holds 7 days and takes at most 2 payments (payer's sit-down day 38). Fail-safe kept as written. First notice staggered (assumed): Widow day 8, Cammack day 10, Agar day 13.

### RT2-08 Rivals as actors

- How it works: Each rival has a base inside the map, a named lieutenant and three named men with routines: the Widow a dock office over the fish dock's net store; Agar an estate agent's office on the cold-store road holding his papers; Cammack the lock-ups on the north road (east side, y 290 to 320). Sending men at a rival's property hits one thing: the base's windows and door, a vehicle (the Widow's van, Cammack's car) or a front or round of theirs. Each hit is a deed against that rival (he climbs a rung), leaves a mark until mended and points his next pressure at the crewman who did it. A night raid is a break-in with two or three of the base's men inside; what is found (the rival's book, a letter) can be used as a counter at the sit-down.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-08 Test: B (bot), as written under RT2-08
- Source: design pass 3, RT2-08 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-08, RT-07, RT-08; DESCRIPTION-COPY-2 §22
- Status: decided. Coverage row: RT2-08.
- Data (run 5): exact values in production/lane/blueprint/data/map.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

## 2.11 Crew under the hood

Men who know: needs, nerve, loyalty, fates.


### 2.11.1 Recruiting

- How it works: Recruits come from the thirty regulars by two roads: meet a need (slow, holds; Julie Kettlewell, laid off, wants work and can drive) or spend a hook (quick, brittle). A need recruit's loyalty ceiling is higher and a hook recruit breaks sooner under the same pressure. Each brings a use the firm lacks: Ian Megginson's locks, Lee Drewery's fists, Norman Dent's nights on the warehouse row, Karen Grummitt's view of the ferry, Shaun Hewson's paint. Men who train at the boxing club can be recruited there.
- Standard: A need recruit's loyalty ceiling is higher than a hook recruit's; each named recruit brings the use the description gives (locks, fists, nights on the warehouse row, the ferry, paint); boxing club men can be recruited there. Test: B: both roads on two men; the same pressure applied; who breaks first.
- Source: The description, section 27; RT-07. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.11.1, RT-07; DESIGN §12; DESCRIPTION-COPY-2 §22
- Status: decided. Coverage row: 2.11.1.
- Data (run 5): exact values in production/lane/blueprint/data/people/ (data build wave 2, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.
- Story needs (frame, 24 Nov): recruiting a rival's man (low loyalty to his head) by a need met or a hook spent, with one true read of his head, and taking a beaten firm in whole (SYSTEMS-THE-STORY-NEEDS S10). Partly covered: the two roads exist but only for the thirty regulars; missing are rival men as kept people, the turning check, the true read as a held fact and the old head's reaction.
- Story conflict C-342 (run 5): The part draws recruits from the thirty regulars and rivals only poach Frank's men (2.11.3), while the story needs Frank to turn a rival's man and take a beaten firm in. Until designed, the part stands; the need is a gap for the design proof.

### 2.11.2 Nerve, loyalty and breaking

- How it works: Crew are named residents with a routine, a need, a nerve and a loyalty with a ceiling. Each man sent is a second person who knows: past his nerve he talks, to a rival or to the police, and the sign always comes first: he looks away, he asks for his cut early, he is not at his post. Paid short or late his loyalty falls; a hook recruit breaks sooner than a need recruit. A man at Frank's side never blocks a door or lane and never lags more than 10 s.
- Standard: ER-CREW-03 Test: S: sign before event in every seeded case
- Source: DESIGN §12 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §12 (ER-CREW-03); DESIGN-ADDENDUM A40; DEFINITIONS RT-07; DESCRIPTION-COPY-2 §22
- Status: decided. Coverage row: 2.11.2.
- Story needs (frame, 24 Nov): crew nerve and loyalty with signs before a break, read by "who comes for him in the yard" and the successor's offer (SYSTEMS-THE-STORY-NEEDS S11). Partly covered; the loyalty ceiling, nerve and break numbers are still gaps.

### 2.11.3 Crew fates

- How it works: Crew can be poached (the Widow takes his least loyal man), frightened off, arrested, docked or expelled by Frank, or killed for good. Each fate is reachable in play, becomes a told version and a Ledger line, and is a town fact. Drivers also leave if unpaid or frightened. Where the man held a post (the dock gate, the cold store, the landing), losing him loses the post.
- Standard: Each fate reachable in play; each produces a told version and a Ledger line; a poach always takes the least loyal man. Test: B: seeded runs for each fate.
- Source: The description, section 27. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.11.3, RT2-09; DESIGN §12; DESCRIPTION-COPY-2 §22
- Status: decided. Coverage row: 2.11.3.

### 2.11.4 Crew pay and the cut

- How it works: A driver keeps half of his car's takings and the firm pays fuel and cover (his pick of 24 Nov; the weekly £90 wage is replaced); drivers leave if unpaid or frightened (what unpaid means under the split is not written: gap). A man on a night job gets a cut (£10 to £40) agreed in a line of talk before it, paid from the tin. Going alone keeps the whole take but brings no second man. Paid short or late, a man's loyalty falls and he asks for his cut first, the sign before breaking; paid fairly he holds longer. Every pound paid out balances in the flows ledger.
- Standard: rule: S: a seeded night job paid short lowers that man's loyalty and he asks for his cut before any break; every pound paid out balances in the flows ledger. Test: S: a seeded night job paid short lowers that man's loyalty and he asks for his cut before any break; every pound paid out balances in the flows ledger.
- Source: DESIGN-ADDENDUM-2026-11-20 A40 (from REFERENCE-MECHANICS-2026-11-20 M7.8) (reference game). Designed in: DESIGN-ADDENDUM A40; DEFINITIONS G8, RT-17; DESCRIPTION-COPY-2 §22
- Status: pending (a reference-game lead; measured only when STATUS.md marks it solid). Coverage row: 2.11.4. Conflicts settled: C-286.
- Studies: aaa-studies/IMMERSION-FEATURES.md: IM-06 cars and men show harm; no repeated care action required; decided. None measured.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-03 each rung adds a weekly cost; outgoings at least half of income each Friday; decided. None measured.
- Economy (24 Nov, section 2): Men's night cuts £10 to £40 from cash; a man posted at the gate, cold store or landing £40 a week (judgement, a part-time wage beside the £227 manual figure). Short pay is recorded and lowers loyalty. The honest firm would pay yard men from the book.
- Economy conflict C-322 (run 5): Settled: the part now carries his ruling of 24 Nov (the driver keeps half his car's takings). Still open: nothing; the loyalty and short-pay rule for night cuts stands.

## 2.12 Position in the town

The rise under the hood: never a number.


### 2.12.1 The name ladder

- How it works: Each person uses the name they have reached: the new owner, then Nowak, then Frank, then Frankie (Frank to most and Frankie to two or three at rung 4). The gate is knowing, not liking: a man who fears him may still call him Frank. A step never goes back, and each step up is heard within a game day of being reached. Sheila withholds his name until she trusts him; her trust is a state the town sees, not a day count (answered 24 Nov: his ruling on Q7). The clean week in which he never asked her to put the books off was the meanwhile build; what the state is and what shows it is not yet written (gap).
- Standard: canon; ER-RISE-02 (heard within a game day, never goes back); Sheila's trust a state the town sees (his ruling of 24 Nov) Test: S: each step heard within a day
- Source: canon premise; ruling 29 Sep; canon of 24 Nov (the lead is Frank Nowak; the ladder is the new owner, Nowak, Frank, Frankie); Sheila's trust: his ruling of 24 Nov (RULINGS on wip, his decisions page) (his ruling or canon). Designed in: canon (Premise and cast); DESIGN §14 (ER-RISE-02); DESCRIPTION-COPY-2 §26; RULINGS 29 Sep
- Status: ruled (his ruling or canon). Coverage row: 2.12.1. Conflicts settled: C-284.
- Studies: aaa-studies/TALK-AS-PLAY.md: TALK-02 each decision talk has two outcomes that turn on state he can see or know, reason said; decided. None measured.
- Story needs (frame, 24 Nov): the name ladder (the new owner, Nowak, Frank, Frankie) heard within a game day of each rung and never going back, with Sheila's exception (SYSTEMS-THE-STORY-NEEDS S1, S40). Covered; Sheila's trust is still open as Q7.

### 2.12.2 Rung table

- How it works: Four rungs, each on exactly its holdings. Rung 1, the nephew: two cars, two drivers, Ron, Sheila, £23.50, the debt book; opens the street, the rank, the landing. Rung 2, Nowak: his answer to Sheila, a third car, a first recruit; opens Mickey's locked office and the real book (on trust) and Rita's back room. Rung 3, Frank: five cars, a night desk, a first front, a first round and the cold-store contract; opens the Harbour Board's counter and a solicitor. Rung 4, the port's man: fronts and rounds across the Hook (at least two of each), men at the dock gate, cold store and landing, a brief on call; opens the sit-down and people stepping aside. An honest firm stops at rung 2 (his pick of 24 Nov, advisor 347).
- Standard: As RT-04: each rung on exactly its holdings; what opens at each rung opens then and not before; an honest firm stops at rung 2 (his pick of 24 Nov). Test: B: rung climbs with holdings added one at a time.
- Source: honest firm stops at rung 2: his ruling of 24 Nov (RULINGS on wip, his decisions page) (his picks, advisor 347); earlier: the description, section 32; RT-04. Designed in: DESIGN §14; DEFINITIONS §2.12.2, RT-04, RT2-01, RT2-09; DESCRIPTION-COPY-2 §26
- Status: decided (his ruling of 24 Nov sets that an honest firm stops at rung 2; the rest is design). Coverage row: 2.12.2. Conflicts settled: C-057, C-058, C-288.
- Economy (24 Nov, sections 0 and 7; ruling): An honest firm stops at rung 2, because rung 3 needs a front and a round; the clean firm stays a respectable cab office. Rung 2 brings the third car on terms, the £90 deposit from the book. Run: racketeer rung 3 in week 5, rung 4 in week 9; mix rung 3 in week 7; honest and lazy never past rung 2.
- Economy (24 Nov, section 5.2 and 7): Smuggled tobacco is a night lever tied to rung 4 posts: two cases a week pass unseen, four with men at the gate; pushed past, customs take the week's load and Ellis hears (run: seizures and three arrests within three weeks).
- Economy conflict C-334 (run 5): The table asks for a first front and a first round for rung 3, and RT2-01 says the contract comes before rung 3, yet the design pays the contract's £40 a week from rung 3 and the run does not model the recruit (rung 2), night desk (rung 3) or three posts (rung 4). The table wins; his ruling that an honest firm stops at rung 2 agrees. Contract income from rung 3 is the design's own looseness (RT2-01 notes the circle).
- Story needs (frame, 24 Nov): four rungs on exactly their holdings (SYSTEMS-THE-STORY-NEEDS S1). Covered; the gaps the blueprint already lists stand (what earns "Nowak" before rung 2, rung 4 fleet size).

### 2.12.3 Access and soft keys

- How it works: Access is by soft keys: standing, dress, an introduction, an appointment the Fixer brokers. The Harbour Board's counter refuses him in the arrival clothes and lets him in with the decent jacket (£45); any door that opens to him clean refuses him bloodied or filthy. Three outfits across the game (as he arrived, the decent jacket, the good overcoat £90) plus a dark coat for nights; the licensing hearing needs the decent jacket or better.
- Standard: Each soft key opens exactly its doors: the Harbour Board's counter refuses him in the arrival clothes and lets him in with the decent jacket; any door that opens to him clean refuses him bloodied or filthy. Test: B: the same doors tried in each outfit and state.
- Source: The description, section 32. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.12.3, RT2-18, G8; DESIGN §14; DESCRIPTION-COPY-2 §26
- Status: decided. Coverage row: 2.12.3.
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-03 each person at the refuse rung refuses Frank something within two game days; decided. None measured.
- Studies: aaa-studies/TALK-AS-PLAY.md: TALK-02 each decision talk has two outcomes that turn on state he can see or know, reason said; decided. None measured.
- Studies: aaa-studies/DENSE-DISTRICT-REVIEWS.md: DENSE-03 Acts II and III each open a new place or way; decided. None measured.
- Studies: aaa-studies/IMMERSION-FEATURES.md: IM-02 every daily act pays in the town; decided; IM-05 a coat seen at a deed stays recognised until he changes coat; washing clears blood only; decided. None measured.
- Data (run 5): exact values in production/lane/blueprint/data/people/ (data build wave 2, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### 2.12.4 Greetings by regard

- How it works: How the rise is heard in the street: greetings by regard (afraid, angry, knows and likes him, his appearance, neutral), at least 6 lines per situation per kind of speaker. A nod, a door held, a path cleared, 'morning, Mr Nowak', or a street that goes quiet. A person's own line is said once a day and a shared line once a week per street; everyday street talk comes at most every 45 s. Walked at rung 1 and at rung 3 the same street gives at least three differences a newcomer can point to. Street lines number 60 own street lines for each of the 12 people seen most, 30 for the rest (FIT-L01); residents (200 to 300) share lines and each has about 5 own lines, made after the first loops (his ruling of 24 Nov, Q9 and R13).
- Standard: At least 6 lines per situation per kind of speaker (DESIGN §11); street lines 60 own for each of the 12 people seen most, 30 for the rest (FIT-L01); residents 200 to 300 with shared lines plus about 5 own each, after the first loops (his ruling of 24 Nov) Test: H: same street walked at rung 1 and rung 3 (ER-RISE-03)
- Source: his ruling of 24 Nov (RULINGS on wip, his decisions page) for the line counts; DESIGN §11, §14 for the rest. Designed in: DESIGN §11, §14 (ER-RISE-03); DESCRIPTION-COPY-2 §26; ONE-SHOT-PROMPT 32
- Status: unmeasured (his ruling of 24 Nov sets the line counts; the rest is design). Coverage row: 2.12.4. Conflicts settled: C-289.
- Prior research: production/cloud-week/lines: 1,626 ambient lines, at least 8 per kind and situation, with silence rules, not yet merged; the count of 6 is met on paper (PRIOR-RESEARCH-INDEX section 4 item 6); KCD2 crowd pool median 5 variants, repeat gap 32 s is a file-read lead.
- Studies: aaa-studies/TALK-AS-PLAY.md: TALK-06 every person answers a street manner within 1 s (ruled, though the study says measured). None measured.
- Data (run 5): exact values in production/lane/blueprint/data/lines/ (data build wave 2, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.
- Story needs (frame, 24 Nov): each rung change said to Frank's face by a named person within a game day, Pauline's on-air name following the ladder, and each rung adding one new kind of night job (SYSTEMS-THE-STORY-NEEDS S2). Partly covered by greetings by regard; missing is the "named person says it within a game day" rule for every rung and the new job kind per rung.

### 2.12.5 Property that reacts

- How it works: Each rung changes at least three things a newcomer can point to. The office fills (a night desk, more phones, the board crowded) and the flat above stops being Mickey's; his cars pass him in the street. The rung 1 street and the rung 3 street, walked, differ in at least three listed ways.
- Standard: Each rung changes three things a newcomer can point to (ER-RISE-03) Test: H: office at rung 1 and rung 3 compared
- Source: DESIGN §14 (no reference figure yet). Designed in: DESIGN §14 (ER-RISE-03); DESCRIPTION-COPY-2 §26
- Status: unmeasured. Coverage row: 2.12.5.
- Studies: aaa-studies/DENSE-DISTRICT-REVIEWS.md: DENSE-01 three changes a week a returning player can point to; decided. None measured.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-07 no purchase raises a fighting, driving or speaking value; decided. None measured.
- Studies: aaa-studies/WHERE-PLAYERS-QUIT.md: WQ-02 Act II in at least four stages of 4 real hours at most, each ending in a rung change; decided. None measured.
- Prior research: aaa-studies/MONEY-AND-PROGRESSION.md MP-07: KCD2 skills reach about 20 of 30 by the first region's end and late Henry is a powerhouse (two reviews, thin); growth here is mainly position (his ruling of 23 Nov: practice, taught skills, hand skills at most a quarter better).
- Data (run 5): exact values in production/lane/blueprint/data/rooms.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### RT-07 Hooks and knowledge as leverage

- How it works: A hook is a fact Frank holds (a Ledger People line he is sure of) about a person which that person would not want told to a named other. He gets one by being told (Darren sells what he hears), seeing it himself, or from Mickey's real book. Spending it is one line of talk and buys a recruit (quick, brittle), an answer to a pressure, or a counter at a sit-down. A hook is spent once: the person now knows Frank knows and remembers. A 'guesses' line is no hook; using it is a bluff that works only if believed.
- Standard: Hooks exist only from a perceived source; spent once; a hook recruit breaks sooner than a need recruit under the same pressure. Test: B: recruit two men by each road and apply the same pressure; hook use logged.
- Source: The description, sections 24 (Ledger certainty), 27, 29, 30. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT-07; DESIGN §12; DESCRIPTION-COPY-2 §38
- Status: decided. Coverage row: RT-07.
- Economy (24 Nov, section 5.4, EC-09): A hook spent for money takes what the person's purse holds (£50 to £300; the run uses £120) and is spent once; the person hates him and is a teller waiting. Rationed by hooks, never a timer, about one a fortnight at most; 0.6 of a case point. Judgement.

## 2.13 The escalation dial

Fists, shown, fired, war: a fact in the town's memory, not a meter.
- Prior research: game-design/combat-design.md (12 Oct): eight-rung ladder (stare, square up, threaten, shove, strike, weapon out, weapon used, kill); most confrontations end on rungs 1 to 4.

### 2.13 The escalation dial

- How it works: The dial is a fact in the town's memory, not a meter, in four states: 0 Fists (nobody carries a gun); 1 Shown (a gun has been seen, news across town, the rivals' top men start carrying); 2 Fired (a shot heard to about 177 m by day, kept for good; armed officers come slowly; Ellis up a step); 3 War (a few named men on each side carry and everyone knows who; armed cars and stop and search; watchers run sooner, night fares fall; a shot can kill, each death named and permanent). Fired moves to War on a second shooting by a different side, a named man wounded by another firm's shot, or more than two of Frank's men seen carrying. It never moves on a deed nobody saw or heard, and falls one step after about two quiet game weeks, never back to 0.
- Standard: ER-FIGHT-08, ER-FIGHT-09 (guns and killing stay rare at every state); falls one step after about two quiet game weeks, never back to 0 Test: S: dial never moves on an unseen deed; War weeks counted
- Source: ruling 18 Nov; DESIGN §7 (his ruling or canon). Designed in: DESIGN §7 (ER-FIGHT-08, -09); DEFINITIONS RT-12; RULINGS 18 Nov; DESCRIPTION-COPY-2 §27
- Status: ruled (his ruling or canon). Coverage row: 2.13.
- Story needs (frame, 24 Nov): the escalation dial 0 to 3, moving only on what was seen, read directly by the quay's "fists unless Fired or War" (SYSTEMS-THE-STORY-NEEDS S4). Covered.

### RT-12 Escalation dial War trigger

- How it works: Fired moves to War when the town learns of either a second shooting by a different side from the first or a named man of one firm wounded by a shot from another. Frank's men seen carrying (more than two, each seen by someone) also move it. Nothing that nobody saw or heard moves it. It falls one step after about two quiet game weeks, never back to 0.
- Standard: War only on these learned events; never on an unseen one; the fall rule as the description. Test: B: seeded sequences of shootings seen and unseen; the dial's state checked.
- Source: The description, section 33. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT-12; DESIGN §7; DESCRIPTION-COPY-2 §27
- Status: decided. Coverage row: RT-12.
- Prep: NUMBERS-RUN R4: the dial and Ellis each fall one step after about two quiet game weeks (RT-12, RT-13), so in a 5-week Act II either falls at most twice; the cooling numbers were set for 7 weeks and should be re-read when the panel plays a 5-week Act II. No rate change proposed. RT2-14's first gun ways can arrive in Act II's first week for a player Sheila trusts early.

## 2.14 Each person's temper

Nerve, loyalty and readiness to talk for each named person.
- Prior research: game-design/town-traits-draft-2026-09-29.md: nerve, loyalty to Frank (a stranger 0.3), greed and a 'police never' flag drafted for all 41 residents (Ron 0.8/0.7/0.3, Sheila 0.6/0.6/0.2); ready, pending his scope answer (Q6).
- Studies: aaa-studies/TALK-AS-PLAY.md: TALK-09 no empty dodge: a reply lacks neither a fact nor a stated reason; decided. None measured.

### 2.14 Each person's temper

- How it works: Every named person has their own nerve, loyalty and readiness to talk, so the same deed goes differently with different people there: one neighbour walks straight to the phone box, another pulls her curtain and tells only her sister, a debtor with nerve stands while another pays at once, a witness loyal to Mickey's people keeps quiet. The real simulation currently gives everyone the same middling nerve and loyalty; the design builds to the recommended answer, measured before it lands.
- Standard: Recommended answer to QUESTIONS 3: every named person their own, measured before it lands Test: S: the same deed goes differently with different people there
- Source: QUESTIONS 3 (open since 29 Sep) (DECIDED by the design proof, for him to overturn). Designed in: QUESTIONS 3; DESCRIPTION-COPY-2 §5 (Each person their own temper); DESIGN §2
- Status: decided. Coverage row: 2.14.
- Data (run 5): exact values in production/lane/blueprint/data/people/ (data build wave 2, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.
- Story needs (frame, 24 Nov): values of nerve, loyalty and readiness to talk for the core six and thirty supporting people, written from their casting sheets, so "one deed only they would do" holds (SYSTEMS-THE-STORY-NEEDS S14). Partly covered; the part names the three traits but gives no values.

## 2.15 The firm runs without him

Kevin drives days, Terry nights; the book fills slowly; the firm's name rises and falls.


### 2.15.1 Fleet and drivers

- How it works: Two cars and two drivers at rung 1 (Kevin Needham days, Terry Hodgson nights), a third car at rung 2, at least four for the cold-store contract, five at rung 3. A car is bought from a man selling one or from the used-car lot by the north road (£600 to £1,200); a driver is hired from the regulars or a stranger who asks at the counter; drivers leave if their half is under £60 two weeks running, or if frightened. The board is a chalkboard in the office with a line per car and driver; it takes a minute a day at most and Pauline runs it if he never touches it. Car two is Mickey's own and cannot be sold, seized or wrecked for more than a day.
- Standard: Two cars and two drivers at rung 1, five cars at rung 3 (DESIGN §14) Test: S: a bought car joins the board and the ranks; addendum rules ER-FIRM-01 to 02
- Source: DESIGN §14 (no reference figure yet). Designed in: DESIGN §12, §14; DESIGN-ADDENDUM A14; DEFINITIONS RT2-01, RT2-06, G8; DESCRIPTION-COPY-2 §23
- Status: unmeasured. Coverage row: 2.15.1.
- Prior research: production/art/mickeys-cars drew the office for nine cars; production/specs/hook-cast.json has Mickey's open 7 to 27 every day, while cab-operations.json differs.
- Data (run 5): exact values in production/lane/blueprint/data/people/ (data build wave 2, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Economy (24 Nov, section 4, EC-03): More cars come on terms: about £90 down and £22 a week for a year from the book; a missed week is a letter said by Sheila, two and the car goes back; Mickey's car two is never taken. Outright price £600 to £1,200 (the run uses £900). Judgement (no 1990 used-car list reached). A steady player reaches five cars inside Act II (run: week 6; racketeer week 4; honest week 7).
- Economy (24 Nov, section 4; ruling): A driver whose half of the takings is under £60 for two weeks running leaves, or if frightened. Drivers are not paid a wage. Judgement; the run records such weeks, none on the recommended figures.
- Economy conflict C-323 (run 5): Applied: the part says cars on terms (£90 down and £22 a week) under the half split, and drivers leave if their half is under £60 two weeks running. Won: his ruling where one speaks, else the newer economy design.

### 2.15.2 Ranks and accounts

- How it works: The rank outside Mickey's is his. The ferry rank and a second rank are won by being there with a car on the board five days in a fortnight, or by a word with whoever holds them. Accounts open in order: the cold-store contract, the Harbour Board's late men, a solicitor's office. The cold-store manager offers the contract once the packing shift has been met on time five mornings in one game week and the firm holds at least four cars; it is lost after three missed mornings in a week and can be won again once. From rung 2 each car on a good rank takes £210 a week, £105 to the book (£125 with the cold-store contract), under the half split (economy design of 24 Nov).
- Standard: A rank is won by either road and never otherwise; accounts open in that order, each at its rung (the cold store at rung 3); "enough days" is five days in a fortnight (a balance figure checked with GD-07). Test: B: rank presence runs; account order.
- Source: The description, sections 28, 31. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.15.2, RT2-01, G8; DESIGN-ADDENDUM A14; DESCRIPTION-COPY-2 §23
- Status: decided. Coverage row: 2.15.2. Conflicts settled: C-059.
- Prior research: research/cab-office-1990: radio licence 120 pounds a year, VAT threshold 25,400 pounds, settle about 49 to 54 a week bear on ranks and accounts; the laundering cap for a cab office is still owed from the 28 Sep outline.
- Data (run 5): exact values in production/lane/blueprint/data/places.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Economy conflict C-324 (run 5): Applied: the part now says takings £210 a week, £105 to the book, £125 with the contract (economy design, newer); the ruling only fixes the half split.
- Story needs (frame, 24 Nov): ranks (SYSTEMS-THE-STORY-NEEDS S43). Covered.

### 2.15.3 Other firms on the ranks

- How it works: One other minicab firm works the Hook, a small outfit with two cars whose owner is a new minor person. It takes the fares people stop giving Mickey's after a hit-and-run and gives them back as the talk fades. It is a business, never a fourth rival and never a crime faction.
- Standard: 'People ring another firm for a while' (DESIGN §5); the three rivals stay three (canon) Test: S: fares move to the other firm after a drive-off and come back
- Source: DESIGN §5; canon (his ruling or canon). Designed in: DESIGN-ADDENDUM A14; DESIGN §5; canon (three rivals)
- Status: ruled (his ruling or canon). Coverage row: 2.15.3.
- Data (run 5): exact values in production/lane/blueprint/data/people/ (data build wave 2, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### RT2-06 The firm failing for good

- How it works: The firm has a floor: the office, Pauline's radio and car two are never lost; car two cannot be sold, seized or wrecked for more than a day. The fare book never goes below zero; unpaid wages make drivers leave; Pauline leaves after two unpaid weeks and comes back when paid (until then fares come only by the office phone when Frank is there). Sheila leaves if asked to put the books off three counts running; without her there is no count and no wash, every week without her reads as put off, and she comes back if Frank calls at her house after a game week in which he asked nobody to put the books off. From any failed state but a revoked licence the way back is the same: drive car two, pay Pauline, hire a driver, buy a car at the lot.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-06 Test: B (bot), as written under RT2-06
- Source: design pass 3, RT2-06 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-06, RT-16, RT2-18; DESCRIPTION-COPY-2 §20
- Status: decided. Coverage row: RT2-06.

## 2.16 Death, bodies and the missing

A killing is permanent and remembered forever; a man who stops keeping his routine becomes the town's question.
- Studies: aaa-studies/FAILURE-AND-FRUSTRATION.md: FF-04 a cost to body or standing shows and has an end or a way back; decided. None measured.

### 2.16 Death, bodies and the missing

- How it works: A killing is rare, permanent and remembered forever; a body never cools in talk and is never wiped. Frank cannot die: beaten, he comes round on the pavement, in Grace Rinaldi's kitchen or in hospital, in control within 60 real seconds. Fists never kill on open ground; a fall onto a kerb's edge, a step or a wall's foot within 3 s of a heavy blow, when the man was already spent, can kill (1 in 50 to 1 in 20 such knockdowns). Finishing a downed man is a separate decision, asked twice. A body left where a routine passes is found; a hidden or sunk one never is, and the missing man becomes the town's question. The blow on a downed man stays, fully animated with no cut-away (his ruling of 24 Nov, Q4; PEGI 18 within canon's limits: the blows fully animated, the gore light).
- Standard: Killing possible, rare, permanent, remembered forever (canon) Test: S: a missing routine is noticed; a body never cools
- Source: canon content rule; the downed man: his ruling of 24 Nov (RULINGS on wip, his decisions page) (his ruling or canon). Designed in: canon (content rule); DESIGN §7; DEFINITIONS RT2-11, RT2-12; ONE-SHOT-PROMPT 14
- Status: ruled (his ruling or canon). Coverage row: 2.16.
- The gap the bar leaves (catalogue 23 Nov, rank 13; seen in 1 game): A regular who stops appearing is noticed, asked after and talked about. Already covered for a killed or missing man; partly for an ordinary absence such as illness. Feature only; no timing; the part's status is unchanged.

### RT2-05 Killing principals and needed people

- How it works: Frank's line is dropped (his ruling of 24 Nov) and keeps no one from his hands; it once kept Sheila, Pauline, Ada, June, Alison, Ellis, the Widow, Father Walsh and anyone of sixty or over, and no fallback by role is written for them (gap). Anyone can be killed or hospitalised and the story falls back by role: Ron's asks come by the outfit's man at the office door; Darren's tips come through Pauline's radio talk and the caff, his debt closed; Kevin or Terry, a car short until a driver is hired; a rival head, his lieutenant takes the ladder at the same rung and counts as having seen the deed; Garbutt gone means no reads or truce; Danby gone ends that friendship; a hurt person is absent for the days their hurt sets; the beat constable's place goes to the second constable from the next night; the cold-store manager's deputy holds the contract; the car-lot man, cars come from a man selling one; Iveson, the fire thread runs on through Alison and Ellis, his debt closed; the dock gun seller, guns come the other three ways; the landlord's agent, letters by post. Act II's beats, the sit-down and Act III never depend on one killable person.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-05 Test: B (bot), as written under RT2-05
- Source: design pass 3, RT2-05 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-05; DESCRIPTION-COPY-2 §38
- Status: decided. Coverage row: RT2-05. Conflicts settled: C-285.
- Data (run 5): exact values in production/lane/blueprint/data/people/ (data build wave 2, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Story needs (frame, 24 Nov): three chairs of fallback carriers (the opponent's place, the bond's place, the book's place if Sheila has left) (SYSTEMS-THE-STORY-NEEDS S33). Partly covered: role fallbacks exist for rival heads and others; these three are missing.

## 2.17 Fronts and rackets held

Taking a share of a business, putting a man in, money and trouble coming back; run through people, never sliders.
- Studies: aaa-studies/DENSE-DISTRICT-REVIEWS.md: DENSE-01 three changes a week a returning player can point to; decided. None measured.

### 2.17 Fronts and rackets held

- How it works: A front is a share of a real business on the street (the launderette, the caff, the empty unit once let), got by money, a favour or pressure. It washes night money through its till, hides men and things, and is a place his men are. A round is a set of payments collected on a day by a man of his crew; trouble on it comes back to Frank through that man. Each has a named man with nerve and loyalty and is a target for rival pressure. Rung 3 needs a first front and round, rung 4 at least two of each. No stock, prices, sliders or screen; money arrives as the man brings it, short if the man is.
- Standard: A first front and a first round at rung 3 (DESIGN §14); empire as management on the street (his lesson 8); not an economy game (canon) Test: S: a front pays through its man; trouble at it reaches Frank through people; addendum rules ER-FRONT-01 to 02
- Source: DESIGN §14; canon (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §14; DESIGN-ADDENDUM A15; DESCRIPTION-COPY-2 §25; DEFINITIONS RT-04
- Status: decided. Coverage row: 2.17.
- Data (run 5): exact values in production/lane/blueprint/data/places.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Economy (24 Nov, section 5.1, EC-06): Protection is £5 to £15 a shop a week by what it can bear (eight shops at £10 is about £60 a week to the tin); the man on the round keeps a quarter. Asking past what a shop can bear raises its board and thins its trade; after three squeezed weeks the owner refuses and tells; four losing weeks shuts it. At £40 a shop Frank ends the story poorer (£224 against £785 at week 7). Judgement (margins from the shops file).

### RT2-09 Turf: posts held and lost

- How it works: The three posts (the dock gate, the cold store, the landing) are held by one crewman each, standing there by his routine: the dock gate and cold store 06:00 to 22:00, the landing 22:00 to 02:00. Contested: a rival's men stand there too and it is a stare each time Frank or his man arrives. Lost: the post's man poached, frightened off, arrested or killed, the post empty three game days, or a sit-down defied and lost on it. Retaken by putting a man there and winning the stare or the fight. Holding all three is part of rung 4; losing one never drops the rung but costs: the landing loses the night runs, the cold store puts the contract at risk, the dock gate brings the Widow's tax back.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-09 Test: B (bot), as written under RT2-09
- Source: design pass 3, RT2-09 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-09; DESIGN §14; DESCRIPTION-COPY-2 §26
- Status: decided. Coverage row: RT2-09.
- Data (run 5): exact values in production/lane/blueprint/data/timetables.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Story needs (frame, 24 Nov): a post stands while its man is loyal and has the nerve, and the player is called only to one authored crisis per post (landing by night, cold store before dawn, dock gate by day) (SYSTEMS-THE-STORY-NEEDS S12). Not covered; the part says the opposite (see CONFLICT).
- Story conflict C-337 (run 5): The part has a post lost after three empty days and a stare each time Frank arrives, while the story drops the daily stare and the three-day count and calls him only to one authored crisis per post. Until designed, the part stands; the need is a gap for the design proof.

### RT2-18 The licence hearing

- How it works: Agar's licence letter is his pressure; his threat is a hearing at the council's licensing committee (in the Exchange, reached at the soft edge, a talk scene under 2 real minutes). The firm keeps its licence if at least two of four hold: every car passed Agar's inspection (no unmended damage), the fare book's last four weeks have no week put off, Frank attends in the decent jacket or better, and no road deed charge is outstanding; not attending counts as one failed. Otherwise the licence is suspended two game weeks: no bookings, Pauline cannot dispatch, the contract is paused and the count washes only £10. A firm car seen carrying a booked fare while suspended is stopped, and a second such stop revokes the licence for good, so the business does not survive.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-18 Test: B (bot), as written under RT2-18
- Source: design pass 3, RT2-18 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-18, RT2-01, RT2-04; DESCRIPTION-COPY-2 §24
- Status: decided. Coverage row: RT2-18.
- Story needs (frame, 24 Nov): a charge that suspends the licence a fortnight, back before the books open (SYSTEMS-THE-STORY-NEEDS S19). Partly covered: the suspension exists only as the hearing's outcome; the charge trigger is missing.
- Story conflict C-340 (run 5): The part suspends the licence only after a failed hearing, while the story needs a charge to suspend it a fortnight (back before the books open, since RT2-04 needs the licence standing). Until designed, the part stands; the need is a gap for the design proof.

## 2.18 Ambulance and the hospital

Someone hurt is taken to hospital after a call from the phone box; stopping to help means making that call.
- Studies: aaa-studies/PLAYERS-STORIES.md: STORY-03 half the moments come from witnesses, recognition or a returning person; physics and driving alone never count; decided. None measured.

### 2.18 Ambulance and the hospital

- How it works: Stopping to help after a hit costs minutes and puts Frank's face beside the cab. Help is a call from the nearest phone box (10p) or the office, or a neighbour rings; the ambulance comes in about ten game minutes and takes the hurt person to hospital for the days their hurt sets. A car never kills, and only the player's car can strike anyone.
- Standard: Stop and help costs minutes and puts his face beside the cab (DESIGN §5) Test: S: an ambulance arrives after a call within its set time; addendum rules ER-AMB-01
- Source: DESIGN §5 (no reference figure yet). Designed in: DESIGN §5; DESIGN-ADDENDUM A22; DEFINITIONS RT2-19; canon (content rule)
- Status: unmeasured. Coverage row: 2.18.
- Emergency services come (catalogue 23 Nov, rank 16; seen in 2 games): An ambulance for a man hurt, never killed. Partly: the ambulance is covered (tape only for a body, 2.6.10); short are a crowd kept at a distance and the constable's notebook. Feature only; no timing; the part's status is unchanged.
- Story needs (frame, 24 Nov): the infirmary's next-of-kin label and a hurt person's days in hospital (Frank's deeds carried; SYSTEMS-THE-STORY-NEEDS S26). Partly covered: the hospital stay exists; the next-of-kin label is missing.

## 2.19 Lasting marks on the town

A forced door shows for a day; glass stays broken until mended; his cars on the ranks; things stay where they were left.
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-04 a man Frank beat shows a mark for a game day and mentions it first; decided. None measured.
- Studies: aaa-studies/DENSE-DISTRICT-REVIEWS.md: DENSE-01 three changes a week a returning player can point to; decided. None measured.

### 2.19 Lasting marks on the town

- How it works: Damage stays until mended: a forced door shows for a day, broken glass stays broken until the owner mends it, blood stays until rain or a bucket washes it; a rival's base keeps a mark until mended and property harm is repaired by people for money and a day. A beaten Frank carries bruises and a cut lip for three game days and a limp for one. Marks keep across save and load, and nothing is ever wiped.
- Standard: Force shows on the door for a day (DESIGN §4); nothing is ever wiped (canon) Test: S: marks persist across save and load for their set time
- Source: DESIGN §4; canon (his ruling or canon). Designed in: DESIGN §4; ONE-SHOT-PROMPT 15; DEFINITIONS RT-06, RT2-08; canon (The moat)
- Status: ruled (his ruling or canon). Coverage row: 2.19.
- Economy (24 Nov, section 5.1): A shop shutting from protection, a hold-up or smuggled tobacco is told for weeks and is a lasting mark, with the cause the town can name.
