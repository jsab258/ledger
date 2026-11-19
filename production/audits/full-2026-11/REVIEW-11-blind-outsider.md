# Review 11: a blind outsider's audit of LEDGER

Written 19 November 2026 from the repository alone (working tree at lane-2026-11, 80e3bb433, which merges wip 345772ac4) and its git history. Nothing under production/audits/full-2026-11/ was read. Nothing on F: or C: was seen, so anything the records place there is taken from the records, not checked.

## What the project is making

LEDGER is a single-player, third-person crime and social game for Windows PC, set in a fictional British port town, Meridian, in 1990 (canon.md). The player is Tom Nowak, who inherits his dead uncle's minicab office on Quay Street in the Hook, with a half-dead criminal outfit and a book of bad debts, and rises against three rival organisations. The selling point canon calls "the moat": every act has perceivable traits, people identify the player on a five-rung ladder, each person remembers permanently, gossip spreads along daily routines, and named people hold live AI conversations with local voices, while a deterministic simulation decides every outcome.

The stated release (RULINGS.md, 28 Oct) is one full game late in 2027, 15 to 20 hours, the Hook plus the docks. The nearer goal (CHARTER.md) is thirty minutes of Quay Street that the owner's friends play on his PC. The work is done almost entirely by AI sessions: a production session on the PC, a cloud "lane" session, an "advisor" the owner talks to, and many helpers. The game runs in Unreal (ue-probe/, about 74,000 lines of C++); the C# simulation in ledger/ (about 176,000 lines, the old Unity project) stays the source of truth the C++ port is checked against.

## The state in one paragraph

After four and a half months and 6,234 commits (first commit 9 July 2026), the game is one built street of about 48 metres (RULINGS, "the built street (48 m...)"), Mickey's front office, Tom and three speaking characters, a talk system near its speed bar, and a nightly packaged build walked by an AI tester. The street frame is close to its reference picture. Clothing, people in motion, frame and memory budgets and speech speed all missed phase 1's exit, and phase 1 was closed on 9 November with those faults carried, not passed. This week's order (16 Nov) has 0 of 11 items done three days in, its allowance was spent by Wednesday, and 70% of it was given to building a custom cloth simulator. The project's records are thorough and unusually honest about failure, but the volume of process now rivals the volume of game work.

## Findings, most important first

### 1. The rate of progress cannot reach the stated release, and the binding stop rule was not applied

- PLAN.md gives phase 1 a ceiling of 1.00W ("one to two weeks") and says: "Binding stop: a sample that cannot pass within this ceiling halts expansion; the failed capability is reported plainly, never dressed as another plan." CHARTER.md repeats it.
- production/progress-page/progress.json records phase 1 as "planned_w": [1.0, 2.0], "actual_w": 4.9, began 2026-10-06, "Closed on 9 November by your tap, with four faults carried into phase 2, not passed".
- All four fresh exit reviews of 9 November say NOT MET (production/audits/phase1-exit/EXIT-A to EXIT-D-REVIEW-2026-11-09.md): a black frame and the camera inside Tom's head in the office; no speaker dressed, sitting or walking without slips (Darren 45 cm); speech 2.02 s against 2.0 s; card memory walking at 6,145 to 6,151 MB against a 6 GB line and 0.2 ms spare card time.
- The owner chose to close it (production/orders/2026-11-09.md, n09-1: "his yes at 07:17 ... phase 1 closed with its four open faults carried"). That is his right, but "closed, faults carried" is the very move the charter's stop condition was written to forbid, and nothing in the records says the stop rule was weighed.
- progress.json still says friends' evening "around January", with the note "if phase 1 passes in the next week or two". Phase 1 did not pass; phases 2 (2.00W), 3 (0.75W) and 4 (0.50W) remain, and phase 1 ran at nearly five times its ceiling.
- At this rate one 48 m street took about four months; the release asks for a district plus the docks, 14 principals, about 30 regulars and 15 to 20 hours of play. RULINGS (5 and 6 Nov) says scope moves first if cost per piece has not clearly fallen by 1 February. No measured fall in cost per piece was found.

### 2. Effort has drifted from the game to tools and process

- Share of commits touching game code (ue-probe/Source, ledger/Assets/Scripts, ledger/CoreTests): August 719 of 1,824 (39%), September 311 of 1,747, October 198 of 1,343, November 68 of 712 (10%). The last commit to ue-probe/Source is 16 November.
- In November, DECISIONS.md was touched by 379 commits against 261 for ue-probe. DECISIONS.md gained 70, 103 and 111 entries on 16, 17 and 18 November, though CLAUDE.md says "one entry per material choice".
- tools/ holds about 230,000 lines of Python against about 74,000 lines of game C++.
- Markdown is 2,634 tracked files and 32 MB; NOTEBOOK.md alone is 83,825 words, DECISIONS.md 31,096.
- The owner's channel: advisor rows numbered to 237 since 4 November; the lane counted 129 rows and 30,469 words in the week of 9 to 15 November and 49 page items in that week (production/lane/OWNER-MINUTES-MEASURE-2026-11-18.md). CHARTER.md says he "gives orders on Mondays".

### 3. This week's main effort is a home-made cloth simulator, and the game items wait for it

- production/week-shape.json: "kiln_share": 70. The handover: "HIS GOAL THIS WEEK (advisor 220): Kiln v1 by Mon 23 Nov 13:00; everything else serves it or waits ... 0 of 6 lines done."
- Kiln is a separate Rust project on F: (cargo tests in DECISIONS 18 Nov 18:06 and 19:11), not in this repository.
- RULINGS 13 Nov: "Kiln serves LEDGER ... game never waits on it". The order of 16 Nov, n16-9: parked cars "Moved to the next order's waiting list ... to make room for Kiln lanes."
- The order ledger (production/orders/2026-11-16.md lines 81 to 91): every item open or carried over. Order item 23 records the meter going "from 97% to 100%" on 18 Nov; week-shape.json shows the spare reset pressed at 2026-11-18 15:20, and the handover says the new guard tripped by 23:18 ("Start nothing new"). A doubled week was spent by Wednesday with no item finished.
- Clothing has been the hardest problem since early October: CLOTHES.md still reads "State, 7 October: failed by both allowed routes"; the owner's answer to Tom's whole-person look on 11 Nov was no ("boots read as rubber slippers, jacket has no cloth texture, jeans no denim", items.json, tom-whole-person-2026-11-11); FINDINGS.md lists collars showing chin and neck, a hole at the knee, cardigans through collars. PLAN.md's clothing task was "one allowed plain outfit"; the project is now writing its own garment engine with Fable at maximum effort "up to 40% of the week" (DECISIONS 18 Nov 16:23).

### 4. Kiln's engine has decompiled ancestry, and the licence question was withdrawn rather than settled

- DECISIONS 10 Nov 10:26: Drape Studio was built by an AI tool "from Marvelous Designer Personal on 9 Nov ... decompiling it and taking 59 of 82 values from Marvelous's preset files; CLO's General Terms forbid reverse engineering".
- DECISIONS 18 Nov 03:13 and 03:14: "Kiln's engine is the Drape Studio engine" and "carries values from decompiling Marvelous (engines/drapestudio/MECHANICS.md, 78 address references); the item had said only names were reused."
- 58 values were replaced in one morning (DECISIONS 18 Nov 09:30), and two items were still open: "start values read from the installed program's data files, and the leg and torso start fits made against Marvelous's drapes".
- The page item (items.json, kiln-front-end-licence-2026-11-17) still opens with "the command names only, not its engine, presets or files", which the session had found untrue. It was closed on 18 Nov 12:16: "withdrawn on his message ... Kiln is his own tool, not a licence".
- Replacing values row by row in code grown from a decompiled program is not a clean-room rewrite; if Kiln garments ship, that exposure is real. The allowlist is "law" (CLAUDE.md), yet the tool is outside it by the owner's word alone.

### 5. Other games' files were opened, and the startup file still says to do it

- production/research/study-a-inzoi/KEY-AND-MAPPINGS-2026-11-06.md: an encryption key for a commercial game was taken from a modding page (which points to a forum for current keys) and "opens the install: the project's reader mounted 36 of 37 containers and listed 258,469 files"; Mafia's key was used as a control.
- RULINGS was changed on 17 Nov 22:33 to "other games are studied from the outside only ... Never decompiled, their files never opened" (commit 0b1195845), the extracts were deleted (DECISIONS 17 Nov 14:43), and tools/outside_only_check.py now fails the build. Good.
- But the repository's own CLAUDE.md, read at every start, still says "look up how Mafia or Kingdom Come II does it (the studies, then their files on demand)" and has a "Game extracts" rule. NOW.md still lists "n16-11 the games' numbers", whose order text is "UE4SS once per game", and order item 15 still cites "its files read once". The highest-read file now contradicts the newest ruling.

### 6. The rule files contradict each other and are kept just under their caps

- CLAUDE.md (repository copy) says FOR-JAFAR.md is due by 07:00 daily; FOR-JAFAR.md itself begins "Stopped 9 Nov 2026" and RULINGS says "No FOR-JAFAR.md".
- CLAUDE.md says the word cap for itself is 1,000; tools/doc-caps.py sets 1,625 and the file is 1,622. RULINGS.md is 4,899 against 4,900; FINDINGS.md 2,000 against 2,000; PLAN.md 1,200 against 1,200; CATALOGUE.md 1,499 against 1,500 (python tools/doc-caps.py, run read-only).
- FINDINGS.md meets its 20-entry cap by bundling: one bullet ("Street details") holds more than a dozen separate faults from 7 October to 17 November.
- CLAUDE.md: "Two tries means two ... a third try needs his yes"; RULINGS 7 Nov allows up to four tries, "None asks him".
- CLAUDE.md: orders "small (about 1,200 words)"; the 16 Nov order is 3,599 words. CLAUDE.md: "Between them nothing new"; within this week the goal changed to Kiln (advisor 220), and the waiting list grew to 24 items.
- RULINGS 11 Nov: "startup files edited at most once a day". RULINGS.md was committed 5, 8 and 8 times on 16, 17 and 18 Nov; the handover 15, 33 and 19 times.
- Several new rulings name "the Monday audit" as their enforcer (DECISIONS 18 Nov 16:53, 22:41); the only Monday audit file in git is production/research/token-audit/MONDAY-AUDIT-2026-11-09.md.

### 7. main has not moved since 5 October

- origin/main is 5437820f0, 2026-10-05 ("UE machine probe from 17bf9da1"). origin/wip is 1,840 commits ahead. CLAUDE.md: "main gets only what passed review". Either nothing has passed review in six weeks, or the rule is dead. Either way the branch meant to hold accepted work holds none of the last six weeks, and the guards tied to main protect nothing current.

### 8. The core promise is thin in play, and the simulation now exists three times

- The lane's synthesis (production/lane/synthesis/QUESTIONS.md, 18 Nov): "In the real simulation every person has the same middling nerve and loyalty, so nobody reports him, nobody stands up to him, and the street has one temper." Open since 29 September.
- production/lane/K2-SIM-PORT-FAULTS-2026-11-18.md: "the only crime in play is Rita's window"; suspicion is kept in two places that can disagree (also FINDINGS: "nothing in the game reads the port's number yet"); three police-file faults reproduced. On the strong side, the same note measured the port against the C# goldens: "102997 check(s), 0 failure(s)".
- RULINGS 18 Nov freezes the town simulation and lets a browser prototype (three.js) "find the fun"; order item 21 plans to build the C# simulation for the browser to replace "the prototype's own copy". That is three copies of the rules (C#, C++, JavaScript).
- On 18 Nov canon gained a pillar, "we don't want a gossip simulator", and the prototype is driving design: it "invented a rule that is in no ruling" (Tom never strikes women, anyone over sixty or the priest; QUESTIONS.md item 2), and the built story has five endings against the owner's ruling of two or three (item 1). The prototype's AI panel: "In round 5 two of the eight recommended it" (VISION.md). This is a late change of centre of gravity for a project whose moat is memory and gossip.

### 9. Talk, speed and budgets miss their bars

- Speech: median 2.02 s against 2.0 s in the packaged game, 7 of 30 at 4 s or more, "Three tries spent" (FINDINGS.md).
- Invention: 16 of 240 test turns carry an invented detail (7%); in small talk 13 to 15 of 36 questions end in "That's as far as I can take you" (FINDINGS.md, from 28 to 29 September, not re-measured since).
- Budgets: shop displays 74,000 to 702,000 triangles against 60,000, Mickey's fittings 479,000 against 100,000 (FINDINGS.md, 8 Nov sweep); card memory over 6 GB walking; the target card is a 10 GB RX 6700 shared with the voice (CHARTER.md).

### 10. The look is the strongest part, with visible placeholders

- production/previews/morning-hook-day-2026-11-18.jpg against production/previews/hook-sheet-2026-10-05.jpg: same street, bend, hill, Mickey's front and wet road; a credible match in composition. In the same game frame a woman in a striped top, skinny jeans and red heels stands outside Mickey's: FINDINGS.md confirms the three Mixamo placeholder figures "stand in play and in his page's frames; out of period". Faces "underlit" and "read East Asian" in street light remain open (FINDINGS.md, since 26 September).

### 11. Housekeeping that misleads a reader

- Git holds 2.7 GB of tracked files, 91 over 5 MB, the largest ledger/Assets/Characters/Adam.fbx at 87 MB; CLAUDE.md says "Git holds text, small files and previews".
- ledger/README.md still says "LEDGER: Unity project. The game ... Current milestone: M0 tech spike".
- CLOTHES.md and TOWN.md describe states of 5 and 7 October; NOW.md lists n16-9 and n16-11 as open though the order says both were carried over.
- Disk: F: has repeatedly sat at its 20 GB floor; one night's build was lost to it (FOR-JAFAR.md, 9 Nov; order of 9 Nov, n09-1).

## What is working

- The deterministic simulation and its port check (102,997 checks, 0 failures) is real engineering.
- Fresh reviews say NOT MET when work fails, and the records keep failures with evidence and dates.
- Licence and content discipline mostly work: the Drape Studio and game-file problems were found by the project itself, the backup was attacked and hardened (production/audits/backup-review-2026-11-17.md), the content rule is enforced by gates.

## What I would do

1. Apply the charter's stop rule honestly: state which capabilities failed (clothing, people in motion, memory headroom), cost them, and re-plan the release against the measured rate, not the planned one. Correct the friends' date on the progress page.
2. Stop building the cloth engine as the week's goal, or rebuild it cleanly from scratch with no Drape Studio code, before any garment from it enters the game; put the licence question back to the owner with accurate wording.
3. Make CLAUDE.md agree with RULINGS (game files, FOR-JAFAR, tries, caps, order size) in one pass; delete n16-11's file-reading wording.
4. Cut the process: fewer advisor rows, one decision record per real choice, caps not raised, and a hard target of half or more of commits touching the game.
5. Either merge accepted work to main or retire the rule.
6. Give each named person their own temper and wire one serious crime end to end before more tooling, so the moat shows in play.
