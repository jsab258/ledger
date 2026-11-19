# Review 01: canon and the design documents (full audit, 19 Nov 2026)

One fresh reviewer, read only. Area: canon.md, game-design/ (87 files), PLAN.md, CHARTER.md, content/, and the lane's unpublished synthesis drafts (production/lane/synthesis/, its pack included). Read against RULINGS.md, INVENTORY.md and DECISIONS-TRACE.md, with git history.

## Summary

The newest layer points at the game Jafar asked for on 18 Nov: canon's pillar "verbs first, talk as the consequence", his combat and car rulings, and the lane's drafts (VISION, DESIGN, TRACE, BUILD-ORDER, QUESTIONS), which are careful on names, cars and the content rule. Under that layer sit three older games still presented as current: canon's own 14 Sep framing ("what people know about you is the mechanic", everything else on the smallest budget), a July Unity game in game-design/ (a pub on Hook Street, Tom Novak, dollars, beer and a gambling marker, marked LIVE, SPEC or APPROVED), and a PLAN and CHARTER that still describe a street-and-conversation proof with friends in "eight to twelve weeks". The biggest miss: the studio's own pre-production audit of 3 Oct said a playable proof of fun comes before production, and PLAN put the first fun check after the whole street; nothing measured whether the game was fun until Jafar raised it himself (17 and 18 Nov). Of the pack's 22 contradictions, I re-checked 20 against the files and found them true; one (item 9, ".45 automatic" against "no automatic weapons") is not a real contradiction, since a .45 automatic is a self-loading pistol. Costs of the design documents are not recorded (the time log, started 5 Oct, has no design task); the lane logs the synthesis at 56 minutes of wall time, tokens not recorded. The decisions trace is weak in this area: it marks the endings ruling (D-C-009) "in-force" while noting the outline has five endings, marks the narrative baseline (D-C-216) in force without seeing that the empire roster breaks canon, and misses a page answer lost since 30 Sep (finding 8).

## Findings, ranked

### 1. Canon describes two different games (high)

Impact: canon outranks everything, and the sessions use its spend rule to decide what gets made. Its 14 Sep lines and its 18 Nov pillar pull in opposite directions.

Evidence: canon.md line 14, "open-town crime sim and social RPG"; lines 172-177 (D24, 14 Sep), "a small dense town where what people know about you is the mechanic. Anything that does not feed perception, memory, gossip or consequence gets the smallest budget". Against that, lines 155-170 (18 Nov): "The player mostly acts ... Talk stays the moat, never the main thing", and "The town's memory and gossip are the engine under the hood, not the show". The spend rule was patched with exceptions instead of being rewritten: fighting AAA (12 Oct) and driving AAA "the end state" (17 Nov), lines 177-182. Read literally, carrying, break-ins and jobs done with the hands (the pillar's verbs) still get "the smallest budget" unless someone argues they feed consequence. The trace calls D24 "in-force" (D-C-213) and does not see the tension.

End, ruling for him: Should canon's "What LEDGER is not" and its spend rule be rewritten to match the 18 Nov pillar? (a) Rewrite them: the player's verbs get full budget and the town's memory is the engine under them (recommended); (b) keep the 14 Sep text with its listed exceptions; (c) something else, in his note.

### 2. Nobody checked whether the game was fun until Jafar asked (high)

Impact: about six weeks of production (faces, clothes, the street, Kiln) went ahead with no measure of whether the game is fun. Jafar raised it himself: the loop prototype as the spec of record (17 Nov 21:57, DECISIONS.md line 339), "verbs first" (18 Nov 15:19, line 425) and "we don't want a gossip simulator" (18 Nov 16:02, canon line 166).

Evidence: production/research/pre-production/1-AUDIT.md line 16 (3 Oct) states the professional method: "Before it, a team has a playable proof that the game is worth making ... sets the idea aside if it does not excite players". Row 1 (line 31) rates LEDGER "PARTLY" and says asset production "began before any family's method and cost were proven". PLAN.md (5 Oct) still put the first judgement of play at the phase 3 exit (line 35), after 2.00W of street production; RULINGS (5 and 6 Nov) adds feel checks only "from phase 3". When play was first measured (prototype rounds, pack 08 lines 170-177), waiting took 36 to 41% of the time, the longest empty stretch ran 7.9 to 13.5 minutes, and 2 of 8 reviewers recommended it. The check that should have caught it was a first-playable gate with an activity-mix measure before any family was multiplied, which is exactly what canon line 163 now asks of the AI playtester.

End, rule: no asset family is multiplied, and no new production phase opens, until the loop's evening run meets the pillar's targets (BUILD-ORDER's M1 to M5). BUILD-ORDER already proposes "6 of 8 before Unreal multiplies anything"; make that a standing rule with a check.

### 3. PLAN.md and CHARTER.md no longer describe the work (high)

Impact: RULINGS line 17 makes these two files "replace every list", and "no new system before its place in PLAN.md". Both are now out of date in substance, so the 29 Sep rule is either broken daily or blocks the work Jafar ordered.

Evidence:
- No prototype, pillar or design stage. TRACE C4 (line 19) admits the beat constable, fares, the wash, the dial and cars and people have no place in PLAN. BUILD-ORDER names a "crime and combat phase", "empire and docks phases" and a "story phase" that exist nowhere: PLAN stops at phase 5, "First town", for a 15 to 20 hour release late in 2027 (RULINGS line 8).
- CHARTER line 5's goal is the street's look, memory and "the conversation responsive", with no verbs. Line 7 says "No new acts, combat programme ... before this works", yet PLAN line 34 has had a fight lab in phase 3 since 18 Nov (commit 470b96b74).
- CHARTER line 13 gives 70/10/20 weekly shares and a "$1-a-day" cap. RULINGS (7 and 10 Nov) keeps 10% for Monday, and money now comes from the $200 monthly credit (RULINGS line 48).
- PLAN line 46: friends' build in "eight to twelve weeks" from 5 Oct, so by 28 Dec. Phase 1 had a ceiling of "one to two weeks" (line 20). The time log shows phase 1 work from 6 Oct to 11 Nov. Its exits were reviewed "NOT MET" on 9 Nov (production/audits/phase1-exit/EXIT-C-REVIEW-2026-11-09.md, EXIT-D-REVIEW-2026-11-09.md), and NOW.md has said "Phase 2" since. PLAN has had piecemeal edits (17 and 18 Nov) and never a re-plan.

End, list item: once VISION is approved, rewrite PLAN.md as the whole road to release: the prototype stage, the one-simulation switch, and phases through crime, empire, story and the docks, each costed. Align CHARTER's goal, shares and money with RULINGS, and add a check that every phase BUILD-ORDER or an order names exists in PLAN.md. The friends' date is scope: put it to him with the new plan.

### 4. game-design/ still presents the July game as current (high)

Impact: sessions and helpers read these files as design. They already have: the 17 Nov combat options (production/lane/COMBAT-END-STATE-OPTIONS.md line 24) and the prototype scope draft (line 179) took their firearms from weapons-spec.md, and the synthesis had to settle 22 contradictions before it could write one design.

Evidence: at least 13 files marked LIVE, SPEC or APPROVED carry pre-canon names, the pub, Hook Street or in-game dollars: how-to-play, voice-casting, shopping-list, qa-matrix, empire-roster, setting-britain-2026-07-31, cast-tier1-batch2, counterparty-purses-spec, weapons-spec, town-plan, open-city-spec, street-spec and m15-the-world-speaks. how-to-play.md, lines 3-6: "STATUS: LIVE, verified 2026-08-04 ... If it is wrong, that is a bug in this file. You inherited your uncle Mickey's pub on Hook Street". Sixteen files say "build state lives in `roadmap.md`", and no such file exists (only roadmap-history.md). This was flagged on 3 Oct (production/research/pre-production/notes/H1-inventory.md line 49; 1-AUDIT.md row 2) and is unfixed 47 days later. The lane's fix (production/lane/MONEY-AND-CONTENT-PATCH-2026-11-18.md) is written but not applied. Canon's gate does not cover game-design/ (canon.md lines 6-7 name content/, ledger/Assets/Scripts and production/specs).

End, deletion plus rule. Move the July LOG files (playtest-notes, writing-samples and writing-check files, the-gap, m0-plan, research-mechanics, research-openworld-audit, roadmap-history, voice-casting-history) and the REPLACED combat-spec to legacy/. This is safe because git keeps them, legacy is the reference shelf, and none of them is read by a build. Apply the lane's patch. Then add a rule: any game-design file not marked LOG fails a check if it holds canon's retired names, "Hook Street", Mickey's as a pub, or in-game dollars, and each kept file names what supersedes it once DESIGN.md is approved.

### 5. The content rule leaks through the C# Core, and canon adopts a roster that breaks it (medium)

Impact: canon claims the rule is "Enforced at six sites" (line 133), but authored event text in the simulation is read by none of them. BUILD-ORDER's one-simulation switch compiles that Core for the browser, so these lines would reach the screen.

Evidence: ledger/Assets/Scripts/Core/ActTwo.cs line 50 and Core/Empire.cs line 1016: "A Dockside man drinks one slow beer at your pub". Game/EmpireSetup.cs line 93: "You quietly clear a slice of Victor's gambling marker." tools/content-gate.py lines 795-820 read dialogue banks, barks, cards, prompts and the brand bible, never source strings. A run today gives "NEW HITS: 0". Canon OPEN 2 (lines 198-200) makes "the empire roster" part of the approved baseline, and the only roster, game-design/empire-roster.md ("as built, 2026-07-26"), has the old rival names (Sera Kest, Aldous Vane, Danny Ro), dollars, "slow beer" (line 51) and the gambling marker (line 41). The trace marks the baseline (D-C-216) "in-force" without noticing.

End: list item (town task) to fix the three Core strings and rewrite the roster under canon's names and pounds. Rule: the content gate also reads string literals in ledger/Assets/Scripts.

### 6. The weapons spec got his 18 Nov decisions on top of a body that breaks canon (medium)

Impact: there are now two combat documents of record. His own combat-design.md (12 Oct) is the design by RULINGS line 119, yet the July spec still heads itself "APPROVED, BUILDING" and was the one updated on 18 Nov.

Evidence: commit 195a24ab6 (18 Nov) added the dial header and "DROPPED 18 Nov" to the silenced .22 rows (14 lines) and left the rest. weapons-spec.md line 1 still reads "spec v5, APPROVED, BUILDING". Line 433: "Runs the bar on Hook Street". Line 609: the bottle as a weapon. Line 654: "A bad drink and a long walk home". Line 657: "Tom Novak, a man who runs a bar". Lines 1480-1490: "ARREST, NO CHASE. APPROVED ... No chase". Lines 649-653: an accident "is the only violence in this game that produces no crime", including "A road and a moving car". These go against canon line 116 (a car never kills; a hit-and-run is chased), RULINGS line 119 (a fall after a blow is a killing) and combat-design.md line 92 (a foot chase).

End, list item: mark weapons-spec.md superseded by combat-design.md, RULINGS of 18 Nov and DESIGN section 7, keeping only its firearms and loudness tables as reference, marked as such.

### 7. The synthesis drops canon's day-life people, and its trace says it does not (medium)

Impact: the drafts will go to him for a yes as "the whole game". DESIGN section 15 says the approved first hour's beats are "kept as written" (line 388), but one is missing, and three canon principals are absent.

Evidence: the approved first hour (game-design/first-hour-2026-09-29.md lines 56-57; approval current under tools/approvals.py) has Tom meet June on day one. DESIGN.md never names June, Philip Danby or Father Walsh, even though canon lines 83-87 list them in the day-life ring and the approved outline's Act I thread is "someone worth being honest for, Alison (built) or Philip Danby". TRACE line 258 maps "the day-life ring" to sections 12, 13, 8, 15 and 16, but none of those sections names them. The drafts are unreviewed (production/lane/LANE-LOG.md line 64: "Not yet reviewed: step 3 next run"). Otherwise, names, cars, the dial, the content rule and the 22 settlements check out against canon and RULINGS.

End, list item: the fresh review of the synthesis checks DESIGN against canon's full cast and the approved first hour. Restore June's day-one beat and the day-life ring, or list them in TRACE as left out, for his eye.

### 8. A story answer lost since 30 Sep, and the endings conflict mis-traced (medium)

Impact: DESIGN section 8 now builds on a proposal whose page answer was lost, and Jafar may be asked again a question he answered.

Evidence: game-design/ending-signs-2026-09-30.md lines 83-86: "A killing with a sure witness passes through 'investigating' for at least a day before a manhunt ... it is his call. It is on the page". production/approvals/town-answered.json lists q-ending-signs as answered, but no answer is stored. The 5 Oct sweep found this (production/audits/sweep-2026-10-05/page-answers-check.md line 177), and it is still "his call" in TRACE C5 on 18 Nov. Separately, RULINGS line 13 (28 Oct) says "two or three endings", while the approved outline and ActThree.cs (enum Ending, lines 28-46) have five. QUESTIONS 1 asks him, correctly, but the trace calls the ruling "in-force".

End, list item: read the 30 Sep page's stored answers first. If none is found, ruling for him: After a killing with a sure witness, do the police spend at least a day investigating before a manhunt? (a) Yes, at least a day, with its sign shown (recommended); (b) no, straight to a manhunt.

### 9. Cars: an approved list says Tom never drives, and his July answer was asked again (medium)

Impact: his attention went on a question he had settled in July, and an approved document now contradicts canon.

Evidence: game-design/side-stories-2026-11-08.md line 16, "Tom never drives (others drive the firm's cars)", approved by his tap on 8 Nov 13:12 as the list phase 3's jobs are built from (production/orders/2026-11-02.md line 68). Canon line 117 (18 Nov): "only the player's car can strike anybody". agency-model.md line 170 still says "No drivable-vehicle physics, ever"; streets-and-cars-spec.md lines 79-80 and how-to-play.md line 50 rule out hitting people. His canon pick of 18 Nov 22:07 is recorded as "keeping his July answer" (canon line 116): that answer (27 Jul, legacy/studio-v2/game-design/decisions-answered.md line 419) lived only in legacy, so nobody read it before asking. The check that should have caught it: "Answers read before asking" (RULINGS line 31) should cover the old version's answered decisions.

End, list item: correct the side-stories line, mark the car lines in agency-model, streets-and-cars-spec and how-to-play as superseded by canon of 18 Nov, and add decisions-answered.md to the sources a page item is checked against before it goes up.

### 10. Canon lines left open or stale (low)

Impact: small, but canon is the one file every session trusts.

Evidence:
- Canon lines 188-191 say the brand bible "still owes" the club, paper, radio and television. content/brands/brand-bible-v1.json has named them since 1 Sep (Meridian Town AFC, The Meridian Argus, Radio Tideline, Coastway Television) with no ruling recorded.
- The second CCTV site, "Jafar's to name" (lines 56-58, since 10 Sep), appears in no order, page item or design.
- "The docks" in his map ruling (RULINGS line 10) is not one of canon's seven districts (TRACE C7).
- Canon line 66 says "The bar is the Meridian Test", while RULINGS line 53 says KCD2 is the bar.

End: ruling for him: Is "the docks" in the release map (a) the Hook's own working waterfront (recommended), (b) an eighth district, or (c) part of Ironside? List item: one page item batching the brand names and the CCTV site, and canon's Tone line reworded to say the Meridian Test judges the friends' build and KCD2 is the bar for the game.

### 11. Numbers read from games' files sit in a design document unmarked (low)

Impact: his 17 Nov outside-only rule makes those numbers leads, not evidence. The lane's new sheets mark them; the design document does not.

Evidence: combat-design.md's "Since 12 October" section (added 2 Nov) takes KCD2's blows "flagged unable to kill", its 10 s knock-out and "Mafia's melee camera held 0.8 s" from Study 14, which was "Read from the games' own files on 28 Oct" (production/research/aaa-reference/studies/14-combat.md line 3). The same section uses Mafia as a reference, though since 18 Nov Mafia is "never the yardstick".

End, rule: any number from studies 01 to 17 in a design document carries "lead" and its study, checked by the same pass as finding 4.

### 12. A dialogue bank that contradicts canon and is not used (low)

Impact: dead weight that would put Mickey's back as a pub if anyone wired it in.

Evidence: content/dialogue/pub-regular-v1.json (48 lines): "You'll be the one that got the pub", "Ah, the landlord" (lines 10, 31). Only crime-witness-v1.json is staged into the game (tools/ue/stage_game_data.py line 57; ue-probe CrimeProbe.cpp line 242). Outside legacy, the only readers are the content gate's glob and two old one-off scans.

End, deletion: remove pub-regular-v1.json. This is safe because no build or game code reads it, git keeps it, and it contradicts D19.

## Counts

High 4, medium 5, low 3.
