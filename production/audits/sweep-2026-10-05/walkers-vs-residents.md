# The street's walkers against the simulation's residents

Date: 5 October 2026 (phase 0, the fourth disagreement named in CATALOGUE.md). Read-only audit; nothing was run, built, committed or pushed.

**What was compared.** Every person or figure the street can show, against the simulation's residents.
- Figures: each entry of production/specs/street-people.json (six Mixamo stand-ins, three cast MetaHumans), plus every other person spawned in the Unreal source (ue-probe/Source/LedgerProbe: VignetteShot.cpp, CrimeProbe.cpp, SliceCharacter.cpp) and in the other specs (ps5-corner.json, street-vehicles.json, shop-interiors.json, mickeys-office.json: no other figures found).
- Residents: the 41 people in production/specs/hook-cast.json (the cast file the game reads, joined to the mill at CrimeProbe.cpp:4984-5003), the C# Core's Gossiper (ledger/Assets/Scripts/Core/Gossip.cs:96), the cards in production/cast/cards, CASTING.md and its sheets, REGULARS.md.
- Rulings searched for "scenery": RULINGS.md, canon.md, DECISIONS.md, CHARTER.md, PLAN.md, NOW.md, FINDINGS.md.

**How.** By reading the specs, the source and the records, and by recomputing from hook-cast.json's routines who stands on Quay Street at an hour (a small script, outside the repository; it reproduces the nightly walk's "measured 15" at noon of day 0). The route is the 30 minutes of production/playtest/thirty-minutes-2026-10-03.md and ROUTE.md, read as the cast file's days 0 to 5.

**Not checked.**
- Whether anything plays or shows in the packaged game as the code says (no run; the AI tester's pictures were not opened).
- The apparent age of every Mixamo body (no file records it).
- Whether the cast classes named in street-people.json:82-96 still exist in the current build.
- Which Mixamo body Tom wears.

## Counts

- Figures: 13 rows.
- With a resident behind them: 6 (Ron, Sheila and Darren as MetaHumans, wired; their three stand-ins, named in street-people.json as placeholders for them, not wired). The other 7 have none.
- Perceiving and remembering: 3 (Ron, Sheila, Darren). A fourth row, the scripted encounter's grey test bodies, perceives as test archetypes, not as residents. Tom is the player (not applicable). The other 8: no.
- Scenery by ruling: 0. No ruling makes any person scenery.
- Disagreeing: 6 rows. One on name, sex, age or role (the note on Darren's stand-in: his hours). Two on place (Martha stands in front of the window the player breaks; Leonard's walk ends on Ada's step). Three on the face or spec (the cast block names superseded faces; Sheila's and Darren's faces fail their sheets). No sex disagreement was found.

**The one-line finding.** The street shows three people who do not perceive (Martha, Leonard, Kate, all high) and hides 38 residents who do. At the window deed of 5 October eight residents saw it; six of them (Hana, Ines, Marla, Marta, Rita, Victor) have no figure anywhere.

## The figures

Importance is for the charter's scope ("Every visible person takes part in perception and memory unless ruled scenery", CHARTER.md:7; "Every visible person has a simulation identity", PLAN.md:33).

| # | Figure | Resident behind it | Perceives and remembers | Ruled scenery | Disagreement | Matters |
|---|---|---|---|---|---|---|
| 1 | Ron, MetaHuman (the live body at Mickey's door) | Yes: id rocco, Ron Kirby, 58, hook-cast.json:295; card production/cast/cards/rocco.md:1; CASTING.md:62; sheet ron-kirby/SHEET.md:8. Spawned CrimeProbe.cpp:2826 | Yes. A Gossiper in the mill (CrimeProbe.cpp:9494); measured as an onlooker (:6895); files through GMill->Witness (:2636). Nightly walk of 5 Oct: saw the deed, and "rocco (recognition)" showed he knew (production/playtest/nightly/2026-10-05.md:1) | No | Name, sex, age match the sheet (names by canon.md:92-100). The spec's cast block still names the 24 September preset face, "Rocco from Jorge" (street-people.json:77, :89), against "Ron P2" (RULINGS.md:53); only used outside the route | Low |
| 2 | Sheila, MetaHuman (the live witness at Mickey's) | Yes: id lena, Sheila Dunn, 53, hook-cast.json:360; card lena.md:1; CASTING.md:61; sheet SHEET.md:8. Spawned CrimeProbe.cpp:2343 | Yes. Gossiper (:9483); measured as an onlooker. By the cast file's routine she stands at the fish front at noon of day 0, so she is among the 15 readings, and not among the eight who saw | No | Name, sex, age match. Her face fails her sheet: "Sheila's lean East Asian from the front, the haircuts" (FINDINGS.md:15). The spec names "Lena from Grace" (street-people.json:77, :82) | Low |
| 3 | Darren, MetaHuman (the live lad) | Yes: id sam, Darren Milner, 25, hook-cast.json:613; card sam.md:1; CASTING.md:63; sheet SHEET.md:8. Spawned CrimeProbe.cpp:2344 | Yes. Gossiper (:9486); named among those who saw the deed on 5 Oct (nightly) | No | Name, sex, age match. Face fails its sheet on the haircut (FINDINGS.md:15). The spec names "Sam from Orlando" (street-people.json:77, :96) | Low |
| 4 | Stand-in "joe-pockets" (Mixamo man) | Named, not wired: the cast block says rocco replaces it (street-people.json:86-92) | No: "no perception, nothing a system reads" (street-people.json:2; VignetteShot.cpp:2185-2187). Left out of the live route (VignetteShot.cpp:2241) but still in the automation's street frames and the scripted encounter (VignetteShot.cpp:2205-2211; H4a-visual-areas.md:243) | No | Sex agrees (Joe is a man, BodyArchetype.cs:54; Ron is a man). Age not checked. Name differs by design: a Mixamo file name, never shown | Medium: it is in the frames on his page |
| 5 | Stand-in "david-pockets" (Mixamo man) | Named, not wired: sam replaces it (street-people.json:93-99) | No (same) | No | The cast note says "Sam is at the fish front from nine to one" (street-people.json:98). hook-cast.json:613 has Darren at the cafe at 9, Rita's step at 10, the fish front only 12 to 13. The "nine to one" is the older quay-cast.json:23. Sex agrees; age not checked | Medium |
| 6 | Stand-in "elizabeth-idle" (Mixamo woman) | Named, not wired: lena replaces it (street-people.json:79-85) | No (same) | No | None found. Sex agrees (BodyArchetype.cs:66). "At Mickey's door" matches where the game stands Sheila while she is in the office (CrimeProbe.h:1981). Age not checked | Medium |
| 7 | Martha (Mixamo woman, standing still; x 19.6, z 4.6) | None. No resident, sheet or canon line has the name (the nearest are Marta, the pawn's clerk, hook-cast.json:2016, and Marla, :1124) | No: "They are not in the town, so they witness nothing" (FINDINGS.md:20). The deed's onlookers are read from the cast file only (CrimeProbe.h:2030-2050), so she is never measured. She speaks stock lines (street-sounds.json:64-75). She has no walk clip, so after the smash she stays put (CrimeProbe.cpp:2471) | No. The nearest text is his 23 September wish for people who "only idle" (street-people.json:2), which says nothing on perception | She stands 0.4 m in front of Rita's pane, back to it: the pane east_parade_glass2 spans x 17.1 to 20.7 at z 4.985 (vignette-pieces.json:284; CrimeProbe.cpp:203), and Rita's step is at 18.0, 4.4 (hook-cast.json). The player breaks that pane. Age not checked | High |
| 8 | Leonard (Mixamo man, walks x 15.5 to 6.0 at z -4.3, 5 to 12 s pauses; street-people.json:31-48) | None. His stock lines say a docker out of work (street-sounds.json:50-62: "There's no work at the docks. None."); the sim's dockers are Ron and three regulars of other ages and names (REGULARS.md rows 5, 15, 16) | No (FINDINGS.md:20). But after the smash every body with a walk clip within 35 m walks to the glass and looks (CrimeProbe.cpp:2472-2500, called at :9222; RULINGS.md:79): he reacts to a deed that nobody files for him | No | His walk ends on Ada's front step: adas_step is 6.5, -4.5 (hook-cast.json:68); the route's invitation arrives as "Ada, from her step" (CrimeProbe.cpp:6476; thirty-minutes md:28). By the cast file Ada is on that step 29 of the 144 hours of days 0 to 5 | High |
| 9 | Kate (Mixamo woman, walks x 27.0 to 19.5 at z -4.6, "with her shopping"; street-people.json:49-66) | None. Nearest name: Katarina, seamstress, Tracey Scarth, 28 (hook-cast.json:1894; REGULARS.md row 14) | No (FINDINGS.md:20). Gathers at the glass like Leonard (CrimeProbe.cpp:2472). Stock lines at street-sounds.json:76-87 | No | Her stretch ends at x 19.5, straight across the road from Rita's pane. Sex F agrees with the Mixamo list (BodyArchetype.cs:66); age not checked | High |
| 10 | Michelle (the night scene's figure) | None | No. Barred from play (VignetteShot.cpp:9017, :6638; FINDINGS.md:20); shown only in the automation's night frames, not page frames (-NoControlQuads) | No | None; the body is adult by the gate (VignetteShot.cpp:6714) | Low |
| 11 | MH_Test, the PS5 corner's MetaHuman | None (made by him in MetaHuman Creator, ps5-corner.json:455-463) | No. Hidden in play; shown only in the corner shots (VignetteShot.cpp:1531-1534, :2056-2067) | No | None | Low |
| 12 | Tom's body | Not a resident: the player, Tom Nowak, 32 (CASTING.md:64; tom-nowak/SHEET.md:9). The town holds facts about "player" (CrimeProbe.cpp:2628) | Not applicable: he is the one the town perceives | No | The body is "a stand-in until Tom's look is settled" (SliceCharacter.h:6). Its sex and apparent age are not recorded: not checked | Low |
| 13 | The scripted encounter's grey test bodies: shopkeeper w1, lad n2, mate r3, constable c1 | In the live route w1, n2, r3 carry the ids lena, sam, rocco and sit hidden under the MetaHumans (CrimeProbe.cpp:9475). In the scripted encounter they are archetypes, not residents (:9476-9494; FINDINGS.md:12). c1 has none ("NO CONSTABLE IN PLAY", :2332) | Partly: they perceive and remember as test archetypes (:9483-9494) | No | Names are archetypes: "the shopkeeper", "the lad in the yard" | Low (not on the friends' route) |

Other spawns, not street figures: MetaHumanCost.cpp:114 (a cost measurement) and MetaHumanPortrait.cpp:253 (portrait photographs) spawn the cast on command-line flags only.

## What the rulings say

- **For perception.** "D25: Everyone perceives, remembers and gossips (owed at stage 2)" (RULINGS.md:80). The decision itself: "NO PLAN MAY GIVE ANY RESIDENT NO MEMORY" (legacy/studio-v2/respec/decision-register/D25-residents-are-tiered-by-authoring-never-by-memory.md). The Core's own definition of a walker: "Near — a walker in the world with a full brain: memory, knowledge, suspicion" (ledger/Assets/Scripts/Core/Population.cs:17).
- **For scenery.** None for people. The only "scenery" in RULINGS.md is "boats and buses scenery" (RULINGS.md:117). canon.md has no line on extras; its only crowd rule is "none in the crowd" for children (canon.md:121). The "no perception" sentence is the spec's own (street-people.json:2, repeated in a code comment at VignetteShot.cpp:2185-2187), written 23 September, not a ruling of his.
- **How it was left.** The rulings sweep of 1 October listed it: "give them perception and memory in the game's spawn, or a ruling to remove them" (production/audits/rulings-sweep/SUMMARY.md:107). The builder put it on the old roadmap (production/archive/2026-10-05-retired/ROADMAP.md:72; DECISIONS.md:228). No answer was found. PLAN.md:33 now makes it phase 3's work.
- **A related builder decision.** 30 September: "until the townspeople walk, anybody without a body counts only from behind their own shop window, never from an empty pavement" (DECISIONS.md:178; CrimeProbe.h:1963-1966, :2046). That is why pavement residents are neither drawn nor counted.
- **The regulars.** "The thirty regulars stand as written" (RULINGS.md:109; DECISIONS.md:149). None of them is Martha, Kate or Leonard, and none of them has a drawn body yet.

## Residents never seen on the street in the route

The cast file holds 41 residents. Three have bodies (Ron, Sheila, Darren). The other 38 never appear: the P4 record says "Only three people can be talked to (and Ada from her step)" (thirty-minutes md:55). The 5 October nightly walk saved no pictures (nightly md:1), so this is read from the records and the code, not from pictures.

**The striking part.** At noon of day 0 the walk measured 15 onlookers (nightly 2026-10-05.json, "measured": 15). Three are the bodies; twelve stand behind counters nobody can see into. The eight who saw the deed were Darren, Hana, Ines, Marla, Marta, Rita, Ron and Victor (nightly md:1). So six of the eight witnesses have no figure. P4 counted "three passers-by" (thirty-minutes md:18); by the code, a witness without a body can only be somebody behind a counter (CrimeProbe.h:2046), so those three were not on the pavement.

Hours below are computed from hook-cast.json for the six days 0 to 5 (144 hours). "Behind a counter" means a place with |z| of 7 or more on Quay Street (counted as an onlooker, never drawn); "on the pavement" counts for nothing in the game (CrimeProbe.h:2046). Names, ages and trades are from REGULARS.md rows, CASTING.md or the sheets.

| id (hook-cast.json line) | Who | Behind a counter, h | On the pavement, h | Note |
|---|---|---|---|---|
| zlata (450) | Pauline Kitching, 44, Mickey's dispatcher | 72 | 6 | Sits in Mickey's office; never seen |
| ferko (493) | Kevin Needham, 36, day driver | 6 | 66 | On Mickey's rank, never drawn |
| dusan (532) | Terry Hodgson, 52, night driver | 0 | 54 | |
| june (563) | June Suddaby, 38, Mickey's daughter (CASTING.md) | 10 | 0 | A principal with a sheet |
| ada (880) | Ada, 78, the widow with a window on Quay Street (CASTING.md) | 7 | 47 | A line only, "Ada, from her step" (CrimeProbe.cpp:6476); "the tea with Ada happens unseen" (thirty-minutes md:30) |
| noor (990) | Alison Sedman, 30, reporter (CASTING.md) | 3 | 22 | |
| marla (1124) | Brenda Laverack, 50, fish shop | 41 | 4 | Saw the deed on 5 Oct |
| joey (1191) | Lee Drewery, 24, casual on the quay | 0 | 72 | |
| rita (1234) | Rita Welburn, 56, keeps the pawn | 39 | 10 | Saw the deed; the window is hers |
| victor (1289) | Wayne Harrison, 27, the pawn's back room | 33 | 10 | Saw the deed |
| hal (1335) | Henry Metcalfe, 66, coin shop | 43 | 0 | |
| tibor (1400) | Susan Coverdale, 38, customs officer | 0 | 5 | |
| emil (1442) | Father Brendan Walsh, about 61 (CASTING.md) | 0 | 6 | A principal |
| vesna (1550) | Nora Cronin, 67, the priest's housekeeper | 6 | 0 | |
| magda (1649) | Winifred Duggleby, 76, chapel cleaner | 0 | 3 | |
| zora (1760) | Doreen Harland, 61, laundry | 46 | 1 | |
| iva (1805) | no sheet: a crowd face (REGULARS.md, how they were chosen) | 54 | 0 | Folded into the third tier |
| selma (1836) | no sheet: a crowd face | 48 | 0 | Same |
| tanja (1867) | Julie Kettlewell, 29, laundry | 66 | 0 | The sheet says she is laid off and "the laundry's day loses her" (REGULARS.md row 8 and its opening); the routine still keeps her there 66 hours |
| katarina (1894) | Tracey Scarth, 28, seamstress | 34 | 0 | |
| ines (1971) | no sheet: a crowd face | 44 | 5 | Saw the deed on 5 Oct |
| marta (2016) | no sheet: a crowd face | 38 | 6 | Saw the deed on 5 Oct |
| jelena (2057) | no sheet: a crowd face | 27 | 0 | |
| stipe (2142) | Colin Mastin, 41, crane driver | 0 | 5 | |
| fabjan (2179) | Albert Suggitt, 78, net mender | 0 | 5 | |
| goran (2216) | no sheet: a crowd face | 6 | 0 | |
| tomas (2313) | Gary Mawer, 29, boat repairer | 6 | 0 | |
| luka (2396) | Ian Megginson, 34, locksmith | 6 | 0 | |
| bruno (2435) | Christine Pickering, 39, harbour clerk | 0 | 0 | Never on Quay Street in the six days |
| petra (2476) | Karen Grummitt, 25, ferry clerk | 0 | 1 | |
| dario (2521) | Gordon Leckenby, 55, ferryman | 0 | 1 | |
| sanja (2566) | Sylvia Rennison, 64, boarding house | 5 | 5 | |
| hana (2627) | Edith Stockill, 79, letter writer | 14 | 6 | Saw the deed on 5 Oct |
| franjo (2702) | Shaun Hewson, 26, sign painter | 6 | 37 | |
| danica (2785) | Dawn Pybus, 27, rent collector's runner | 1 | 8 | |
| drago (2916) | Dennis Iveson, 62, scrap dealer | 12 | 0 | |
| filip (2948) | Norman Dent, 57, night watchman | 0 | 0 | Never on Quay Street in the six days |
| outfit_man (2967) | unnamed, the man at the ferry landing (canon; REGULARS.md leaves him out) | 6 | 0 | Shown as text only: "The man at the landing is never seen" (thirty-minutes md:53) |

Totals: 27 are behind a counter at some hour (counted as onlookers, never drawn); 9 are on the pavement only (dusan, joey, tibor, emil, magda, stipe, fabjan, petra, dario); 2 are never on the street (bruno, filip).

**Named by the route but not residents.**
- DS Ellis has no entry in hook-cast.json (no "ellis" id); she is the Core's PoliceFile (PoliceFile.cs:141, "on her visit"), a woman in CASTING.md:65 (Carol Ellis, 40). The playtest record calls her "him" and "He" (thirty-minutes md:36, :52): a sex disagreement in the record, not in the game's line (CrimeProbe.cpp:6468). She is "never seen".
- Agar, Jensen, Cammack, Danby and Garbutt have casting sheets (CASTING.md:66-68, :73-74) and no entry in hook-cast.json, so they are principals who are not residents of the mill.
- The Core also holds a generated district population (Population.cs), tested in CoreTests (Program.cs:148). It is not ported: "The crowd's generation (Population.Generate) ... is NOT PORTED" (ue-probe/Source/LedgerProbe/Public/Schedule.h:27-29), so none of it stands behind any figure.

## What follows for the charter's scope

- The three high rows are the whole of the visible gap: Martha, Leonard and Kate. The charter allows a visible person only with a simulation identity or a ruling that makes them scenery. There is neither. Martha, in particular, stands at the pane the player breaks.
- The cheapest honest readings, for the builder to choose from (no choice is made here): give each of the three a resident id from the cast file's unseen residents (Rita's counter, Ada's step and the laundry front have none drawn); or ask him for a scenery ruling; or remove them from the route.
- The imbalance runs both ways. The nightly question "does the town visibly know Tom" is answered mostly by residents nobody sees (six of eight witnesses), so drawing a few of them is the same work as the charter's rule, from the other end.
- Small repairs, not for this audit: street-people.json's cast block (names the 24 September preset faces; Sam's "nine to one"); the playtest record's "him" for Ellis.
