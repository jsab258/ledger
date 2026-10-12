PASS WITH FIXES

# REVIEW-7b: fresh review of COMBAT.md and CREDITS-MAP.md

Reviewer: a fresh session that wrote neither file. Read 13 October 2026. Every source below was re-opened through the proxy with the LEDGER research identity, one request at a time. K14 answered HTTP 429 once and HTTP 200 on a single retry a few minutes later; nothing else refused. Scratch work (downloads, parsers, counts) stayed outside the repository.

What was checked: in COMBAT.md, about 60 numbers and quotes against 30 sources (K1, K5, K6, K9, K10, K11, K12, K14, K18, K21, K22, K36, K37, K39, M1, M2, M3, M5, M6, M7, M10, M12, M14, M15, M19, M22, M25, S1, S2), all 42 verdict rows against game-design/combat-spec.md read in full, the code claims against Combat.cs, Interaction.cs and Rig.cs, the 17 animation entries, and a replay of run 3 through Combat.Resolve's own rules. In CREDITS-MAP.md, the KCD2 roll re-fetched through the Fandom data interface and recounted by script, S2 to S7, S10 to S12, 25 of the 29 map rows, the seven gaps, and the 29 % sum. In both, a script scan for U+2014, U+2013 and italic markup (none found), a script check that every cited repository path exists (all do), and a 16-word verbatim-run scan against every fetched source (one hit, fix 7).

## Fixes, worst first

1. **COMBAT.md, section 5.4, the bullet starting "Run 3, the strikes."**
   Wrong: the punishment figures were computed with the swing's power taken before its stamina is paid. Combat.Resolve pays first: ledger/Assets/Scripts/Core/Combat.cs line 183 subtracts StaminaCost (0.34) from the swinger, and only then line 216 sets power to 0.55 + 0.45 x the stamina left. Replayed with the file's own assumptions (2.0 s of Breathe at 0.09 a second between blows, floor 2.8, reeling at 0.55 of it, an unguarded target at full capability), the running totals are 0.847, 1.622, 2.325 and 2.956, not 1.00, 1.93, 2.78 and 3.57. The footing order (steady, reeling, reeling, down) still holds, so pass item 5 stays right, but "0.02 short of the floor" is really 0.475 short, and "With swings 2.5 s or more apart he goes down on blow 3" is false: three fully rested blows add only 3 x 0.847 = 2.541, under 2.8, so a fresh unguarded man always needs four blows (at 2.5 s apart the totals are 0.847, 1.642, 2.386, 3.077).
   Replace the whole bullet with:
   "- Run 3, the strikes. Tom strikes the second man four times, 2.0 s apart (the KCD2 mean gap), standing still between blows. Derived from the Combat.cs constants and the order Combat.Resolve works in (the swing's cost of 0.34 is paid first, then the blow's power is 0.55 + 0.45 x the stamina left; stamina back 0.09 a second; floor 2.8, reeling from 55 percent of it, 1.54; an unguarded man at full capability): the running totals are 0.847, 1.622, 2.325 and 2.956 punishment, so the man is steady after blow 1 (D03), reeling after blow 2 (D04, then D05 between blows), still reeling after blow 3 (D04 again, 0.475 short of the floor), and down on blow 4 (D06, then D07). However far apart the swings, an unguarded man at full capability needs four blows: three fully rested blows add only 2.541. A shove on him while reeling puts him down at once (C01, D02). One run uses a miss (B02) because the second man stepped back."

2. **COMBAT.md, the clinch push, four places.**
   Wrong: patch 1.2 says "Fixed the ability to push an opponent out of a fighting pen using clinch" (https://www.deepsilver.com/games/kingdom-come-deliverance-ii/news/patch-12). That removed the push as a fault; the file reads it as a feature.
   a. Section 2.2, row "Clinch, lock, grip, throw", the sentence "A patch note says the clinch can push a man out of a fighting pen." Replace with: "Patch 1.2 removed, as a fault, the ability to push an opponent out of a fighting pen with the clinch."
   b. Section 2.2, row "Shove or kick", the words "the clinch push above is the nearest." Replace with: "the nearest was a clinch push out of a fighting pen, which patch 1.2 removed as a fault."
   c. Section 4, row 9, the KCD2 cell "Clinch can push a man out of a pen; "locks, grips and throws" [K9, K5]; kick in the first game [K22]". Replace with: "Clinch with "locks, grips and throws" [K5]; a clinch push out of a fighting pen was removed as a fault in patch 1.2 [K9]; kick in the first game [K22]".
   d. Section 6, Unverified item 12, the words "only the first game's codex and a clinch-push patch note were read [K22, K9]." Replace with: "only the first game's codex and a patch note that removed a clinch push were read [K22, K9]."

3. **CREDITS-MAP.md, section 5, the sentence starting "Buying, commissioning or hiring is Jafar's alone".**
   Wrong: hiring is not merely his call today; it is ruled out. CHARTER.md, Constraints: "no hiring, new subscriptions or unapproved purchases". RULINGS.md, 24 September: "no hiring, ever" (said of voices). Buying and commissioning need his yes (RULINGS.md, 16 September and 3 October).
   Replace that sentence with: "Buying and commissioning need Jafar's yes (RULINGS.md, 16 September and 3 October). Hiring is ruled out today: CHARTER.md's constraints say "no hiring", and RULINGS.md says "no hiring, ever" of voices (24 September). Every option below that pays a person or a company (gaps 1c, 2c, 3d, 4b, 5c, 6c, 7b and 7c) needs his yes, and any that hires someone needs him to change the charter first."

4. **COMBAT.md, section 4, "Notes on the table", second bullet, the sentence starting "RULINGS "What the game is" lists".**
   Wrong: RULINGS.md has no health-bar ruling anywhere (searched: the words appear only in combat-spec.md section 4, weapons-spec.md and roadmap-history.md). The other items are right: "no jump ... fists and improvised weapons, firearms rare" is the 23 September genre line, "no stats" is D11.
   Replace that sentence with: "RULINGS "What the game is" lists no jump, fists and improvised weapons, firearms rare (23 September, genre) and no stats (D11). No health bar is the spec's own rule (combat-spec section 4), not a ruling."

5. **COMBAT.md, the KCD2 attack gap's official spread is left out (section 2.3 and entry B01).**
   Wrong: K1 (https://warhorse.youtrack.cloud/api/articles/KM-A-20?fields=idReadable,summary,content,updated) lists, beside CombatAutoMaxAttackDelay 2 s, "CombatAutoAttackDelaySigma | attack delay variation | [s] | 4" and "CombatAutoNPCOpponentAtkDelayCoef | shortening attack delay when opponent is npc | [%] | 0.5". B01 calls its plus or minus 0.5 s spread judgement without saying the game's own spread is 4 s, which matters for phase 3's rhythm.
   a. Section 2.3 table: after the row "| How the gap grows for each attacker | ... |" add two rows:
   "| Spread of that gap | CombatAutoAttackDelaySigma | 4 | seconds ("attack delay variation") |"
   "| Gap shortened when the target is another NPC | CombatAutoNPCOpponentAtkDelayCoef | 0.5 | share |"
   b. Section 2.3, the bullet starting "If the gap rule is", the words "whatever its size (derived from an unverified reading)." Replace with: "whatever its size, before the official 4 s spread is applied (derived from an unverified reading)."
   c. Section 5.3, B01, the words "(game: KCD2 official mean gap; the spread is judgement)". Replace with: "(game: KCD2 official mean gap. KCD2's own table gives a far wider spread, 4 s, CombatAutoAttackDelaySigma [K1]; LEDGER's narrow spread is judgement, chosen so the rhythm can be learned)".

6. **COMBAT.md, the guard timing does not meet its own pass line (section 5.1 and section 5.4 item 3).**
   Wrong: 0.733 s minus 0.64 s is 0.093 s, which is 2.8 frames, so "at least 3 frames before contact" cannot pass even on paper. In whole frames, a press at 0.54 s lands on f17 (0.567 s), E01 makes the guard live 3 frames later at f20 (0.667 s), 2 frames before contact at f22. Also 0.64 s is 19.2 frames, so 20 frames is rounding up, not rounding; and S2's 190 ms is a full simple reaction (see a light, press a button: https://en.wikipedia.org/w/index.php?title=Mental_chronometry&action=raw, "Simple RT paradigms"), not time "to see".
   a. Section 5.1, replace the whole bullet starting "The wind-up, derived with judgement" with: "- The wind-up, derived with judgement: 0.19 s simple reaction, seeing a signal and pressing one key (standard) + 0.35 s more to choose among three answers (judgement) + 0.10 s for the guard to come live (E01) = 0.64 s, rounded up to 20 frames (0.667 s; 0.64 s is 19.2 frames). Range 0.50 to 0.80 s. Contact comes 2 frames later, at 0.733 s, so a guard pressed at 0.54 s is live 0.09 s (between 2 and 3 frames) before the blow lands."
   b. Section 5.1, the bullet starting "Telegraph setting", the words "the wind-up is lengthened by 1.5" become "the wind-up is multiplied by 1.5".
   c. Section 5.4, replace item 3 with: "3. **Answerable.** A scripted player who presses guard 0.54 s after the wind-up starts (0.19 s standard plus 0.35 s judgement; the press lands on f17, 0.567 s, the first frame after it) has the guard live by f20 (0.667 s, E01's f3), at least 2 frames (0.067 s) before contact at f22 (0.733 s)."

7. **COMBAT.md, section 2.3, "What the patches say about timing", first bullet ("Introduced a short delay ...").**
   Wrong: a 20-word verbatim quote of patch 1.2, over the 15-word cap the brief and the file's own section 1 set. It is the only run over 15 words in either file that matches a source (script scan).
   Replace the bullet with: "- A short delay was added between melee attacks made without lock-on, so that spamming attacks works less well."

8. **COMBAT.md, section 5.3, the hit reactions do not chain for run 3 (entries D04, D05 and A02).**
   Wrong: run 3's blow 3 lands on a man in D05 and plays D04, but D04 starts only from "D03 or stance" and D05 blends only to D02, D06 and E02. A02 lists D05 as a source though D05 never blends to A02, and A02's list leaves out B01, B02, C01, D01 and D03, which all blend to A02.
   a. D04: "Start: D03 or stance." becomes "Start: D03, D05 or stance."; "Blends from D03 or any stance over 3 frames" becomes "Blends from D03, D05 or any stance over 3 frames".
   b. D05: "Blends from D04; to D02, D06, E02." becomes "Blends from D04; to D02, D04, D06, E02, A02."
   c. A02: "Blends from A01, E02, D05;" becomes "Blends from A01, B01, B02, C01, D01, D03, D05, E02;".

9. **COMBAT.md, "In plain words", item 4, the words "people need about 0.2 s just to see a move."**
   Wrong: same source point as fix 6: 190 ms is seeing and pressing, not seeing alone.
   Replace with: "people need about 0.2 s just to press one key when a light comes on, before any choice."

10. **CREDITS-MAP.md, the order of the closing sections.**
    Wrong: the brief says the file ends with Not reached, Unverified and Sources; here "## Appendix: every role title in the KCD2 roll, with its entries" comes after Sources.
    Move the whole Appendix (its heading, its first paragraph and all its lines to the end of the file) to just before "## Not reached", and rename its heading "## 7. Appendix: every role title in the KCD2 roll, with its entries". No other text changes.

11. **CREDITS-MAP.md, Unverified, the line starting "S1's own totals (1,520 people, 1,846 entries)".**
    Wrong: numbers marked unverified may not be used in a ratio, yet section 2 computes "1.1 % and 2.0 % higher" from them. In fact the totals are verified as printed: the wikitext opens "The KCD2 credits list 1,520 people across 1,846 entries" (https://kingdom-come-deliverance.fandom.com/api.php?action=parse&page=Credits/KCD2&prop=wikitext&format=json). What is unverified is only how the page counted.
    Replace the line with: "- S1's own totals: confirmed as printed on the page (1,520 people across 1,846 entries; re-read 13 October 2026), but not reproduced: this file counts 1,490 names and 1,826 entries, and the page does not say how it counted."

12. **CREDITS-MAP.md, section 4, map row 4 (Narrative and writing), the "How much" cell.**
    Wrong: "twelve casting sheets approved" matches nothing on file: CASTING.md has fourteen principals, RULINGS.md (25 September) approves "the other eleven casting sheets" as text and froze three faces on 30 September. And QUEUE.md says unit 11 is "done (13 Oct 03:55 Swiss ...; no fresh review ...)", so "being written this week" is out of date.
    Replace the cell with: "Partial: the outline approved; fourteen principals' casting sheets, three with frozen faces and the other eleven approved as text (RULINGS.md, 25 and 30 September); the thirty regulars' facts written this week (QUEUE.md unit 11, done 13 October, no fresh review yet); the rest is generated live and claim-checked".

13. **CREDITS-MAP.md, section 4, "What the map shows", first bullet, the sentence starting "LEDGER's own risk files rank talk first".**
    Wrong: neither file says "talk, then people on screen and the street". 2-FEASIBILITY.md ("What the table says") names talk, people on screen, and thirty minutes never played end to end. 6-RISKS.md ranks R1 talk, R2 replies too slow, R3 the street (3 October); its 5 October review puts R3 and R1 at 25 and R2 at 20.
    Replace that sentence with: "LEDGER's own risk files put talk first: production/research/pre-production/2-FEASIBILITY.md ("What the table says") names talk, people on screen, and thirty minutes never played end to end; 6-RISKS.md ranks talk (R1), slow replies (R2) and the street (R3) on 3 October, with R3 and R1 both at 25 after the 5 October review."

14. **CREDITS-MAP.md, the "29 %" figure (section 2, "Reading the numbers", first bullet; section 4, "What the map shows", first bullet).**
    The arithmetic is right (523 / 1,826 = 28.6 %, recomputed), but the set is a floor: it leaves out on-screen work the roll credits under other headings, which gap 1 itself counts (stunts and fencers 12; Apple Art Studio's capture editing 18), plus 3Bohemians 10, More.is.More 8 and 3D.sk 4. Its "voice cast 115" also includes 34 screams and shouts.
    a. Section 2: replace the bullet starting "The jobs that put a person on screen hold 523 entries" with: "- The jobs that put a person on screen hold at least 523 entries: character art 24, animation 39, dialogue cameras and cinematics 36, motion capture crew and actors 158, voice cast with screams and shouts 115, face models and scans 151. That is 29 % of the roll (derived: 523 / 1,826 = 28.6 %). Counting also the on-screen work credited under other headings (stunts and fencers 12; 3Bohemians 10; Apple Art Studio's capture editing 18; More.is.More's facial scanning 8; 3D.sk's scans 4) gives 575, 31 % (derived: 575 / 1,826 = 31.5 %). Technicolor's 79 are left out because the roll does not say what they made."
    b. Section 4: "In KCD2 those jobs hold 523 entries (derived, section 2)." becomes "In KCD2 those jobs hold at least 523 entries, 575 with the stunts and the outside studios that did such work (derived, section 2)."

15. **COMBAT.md, section 5.4, item 4, the words "with the shoved man moved 1.2 m, plus or minus 0.15 m."**
    Wrong: inside the stated tolerance, a correct 1.05 m shove from the judged 0.8 m start ends 1.85 m apart and fails the same item's 1.9 m line.
    Replace with: "from a start at least 0.8 m apart, with the shoved man moved 1.15 m to 1.35 m."

16. **COMBAT.md, section 5.2 table, rows D01 and D04, the "Timing source" cell "derived from repository constants".**
    Wrong: only the distances come from constants (1.9 m shove reach and the judged 0.8 m start; the 0.55 m Bumps cap). The timings (f15 in both) are judgement.
    In both rows replace the cell with: "judgement (the distance is derived from repository constants)".

17. **COMBAT.md, section 4, row 2, Reason cell, the words 'since spec 7b says nothing "touches a corpse"'.**
    Wrong: misquote. combat-spec.md section 7b: "none of them touch a corpse".
    Replace with: 'since spec 7b says none of the containment tools "touch a corpse"'.

18. **COMBAT.md, section 5.3, A02, the words "(Rig.BreathRate, 0.25 to 0.85 a second)".**
    Wrong: 0.85 is a comment's round figure. ledger/Assets/Scripts/Core/Rig.cs line 184 returns 0.25 + 0.50 x tiredness + 0.18 x hurt: 0.25 at rest, 0.75 when spent, 0.93 when spent and hurt.
    Replace with: "(Rig.BreathRate in Rig.cs: 0.25 breaths a second at rest, 0.75 when spent, at most 0.93 when spent and hurt)".

19. **COMBAT.md, section 5, the "Status: DRAFT." paragraph, two clauses.**
    Wrong: "or the project's own capture" is presented as open, but RULINGS.md (3 October) says poses come from MetaHuman's movement clips and Mixamo, and no pose estimator is on the allowlist. And "so they pass the clip-name walk" states a result for a check nobody has run.
    a. "(MetaHuman movement clips and Mixamo, per RULINGS 3 October, or the project's own capture)" becomes "(MetaHuman movement clips and Mixamo, per RULINGS 3 October; the project's own capture would need a new ruling and an allowlist record first)".
    b. "so they pass the clip-name walk of tools/content-gate.py." becomes "so they should pass the clip-name walk of tools/content-gate.py (to be run when the clips exist)."

20. **CREDITS-MAP.md, Appendix, the line for "Warhorse Studio Orchestra", the words "largest: Violins (41), Violas (16), Cellos (11)".**
    Wrong: recount from S1: Violins 41, Violas 16, Soprano 15, Tenor 15, Vocals 13, Bass 12, Cellos 11.
    Replace with: "largest: Violins (41), Violas (16), Soprano (15), Tenor (15)".

21. **CREDITS-MAP.md, section 2, the table "Performers, capture crew, scans, music players, advisors and tributes", row "Community, tributes and thanks".**
    Wrong by omission: the 123 "people" include five institutions or groups thanked by name in Special Thanks (two museums, a monuments institute, and two groups of building owners), so they are names, not all people.
    Replace the "What it is" cell with: "64 names of babies born during production, 47 forum community handles, thanks and a dedication; not roles; the 123 include five institutions or groups thanked by name".

22. **CREDITS-MAP.md, section 6, the words "a gambling den in a Mafia expansion chapter, per Wikipedia".**
    Wrong: Wikipedia (https://en.wikipedia.org/w/index.php?title=Mafia:_The_Old_Country&action=raw) puts it in a plot sub-section and does not call that an expansion.
    Replace with: "a gambling den in one part of Mafia's plot, per Wikipedia".

23. **CREDITS-MAP.md, section 5, "Why these three come first", the sentence "The street is near silent without music (gap 3)."**
    Wrong: it contradicts gap 3 (a) and QUEUE.md unit 10 (97 sound files: 21 loops, 40 footsteps, 36 one-shots).
    Replace with: "The street has its ambient sound set (97 files) but no music and no music direction (gap 3)."

24. **CREDITS-MAP.md, Appendix and the outside-studios table, song titles and spaced hyphens.**
    a. Six block headings are the titles of pieces of the game's music, in-game names the brief says not to copy. Replace "**Panychida: Veliký Den**" with "**Additional music: a bagpipe piece**", and the five headings "**Additional Music: '...'**" in order with "**Additional Music: song 1**" to "**Additional Music: song 5**". Counts and titles after the headings stay.
    b. The brief allows a hyphen only inside a word. Replace every " - " (space, hyphen, space) in CREDITS-MAP.md with ": ". There are 14 lines with it, all role titles or headings copied from the roll (for example "Testronic - Localisation QA" becomes "Testronic: Localisation QA").

## What is right

- **The KCD2 counts reproduce exactly.** Re-fetched through the same data interface and recounted by script: 86 headed blocks (82 after merging the two Special Thanks and two Dedication blocks and dropping Software and Copyright); 1,826 entries; 1,500 distinct names, minus the ten organisations the file names (two translation agencies, two recording venues, one studio, one horse supplier, four scanning companies), gives 1,490, and 1,487 with accents folded. Every group row (445/355, 439/319, 230/200, 47/45, 271/268, 271/267, 123/123), every in-house discipline row and share, every outside-studio and publisher row, 403 distinct titles, the ten biggest titles, and every title count in the appendix match.
- **The wiki's own tally and the Wikipedia leads are quoted correctly**: 1,520 and 1,846 as printed, 1.1 % and 2.0 % right; Wikipedia's 9 lead credits and 8 people, all seven roles placed in S1 as the file says. Warhorse's "a team of 300" and Wikipedia's 250 (2024) confirmed.
- **The Mafia section is honest.** Only 9 lead credits are counted (confirmed in S3); the voice cast is a floor (31: 26 named, one marked Verify, 5 additional; "Under Construction" confirmed); the Definitive Edition headings are marked inference and exist in S12; the Brno 170 and Grip Studios are confirmed in S7 and kept out of totals; Petaluma and Brno stages confirmed in S10.
- **The map rows checked hold** (1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29): every cited file exists and says what the row claims (for example MAP.md's "Typing never walks Tom: fails" and 4.6 s; HANDOVER.md's eight kit families, three 2D sets and 33 wear-mask kinds; the 41 Mixamo slots; Chatterbox Nano in THIRD-PARTY.md; FEASIBILITY areas 27 and 29; allowlist items 3, 5 and 8). The full, partial, stand-in and none judgements are fair, except row 4 (fix 12).
- **The seven gaps list options only**, with no prices and no purchase decision.
- **Every K1 number checked matches** the official table (exported 14 January 2025, page updated 25 October 2025): stamina 26, 20, 22, x0.6, x0.75, 15 to 40, 0.7, sprint 3.5; charge 0.2 and 1.4 s; mean gap 2 s and 0.8 per attacker (horse 0.1, missile 0.2, move activity 0.5); perfect block 0.3, 0.85 and exponent 0.5; combo 3; danger 0.5 s; 10 m and 100 m icons; hunt 15 to 60 s; morale 0.2; 2.35619 rad and x1.2; knock-out 0 and depth 480 at 1 a second; corpse 300 and 3,600 s game time; reputation 10,800 + 1,800 s, 400 m at 0.25, weights 5, 3 and 1; anger 0.67; view 2.5 to 50 m, night outdoors -0.7, recognition and decay 4 s; bleeding 6 s, injury 20 s, low health 40 %; stealth 0.05, 0.4 and 5.
- **The quotes and claims checked hold** in K5, K6, K9 (apart from fixes 2 and 7), K10, K11, K12, K14, K18, K21, K22, K39, M1, M2, M3, M5, M6, M7, M10, M12, M14, M15, M19, M22, M25, S1 and S2, with their dates. The unverified guides K36 and K37 are reported faithfully and used in nothing.
- **The verdict table is sound**: 12 ADOPT, 25 ADAPT, 5 IGNORE confirmed; every Reason quote but one (fix 17) is in combat-spec.md or Combat.cs word for word; no row contradicts Jafar's section 7 answers or RULINGS.md.
- **The code claims hold**: VerbBeat's default wind-up 0.18 s (Interaction.cs line 39); Reach 1.6, ShoveReach 1.9, StrikeStamina 0.34, StaminaRecovery 0.09 a second, FloorAt 2.8, reeling at 0.55, guard lets 0.22 through (Combat.cs); Bumps stagger capped at 0.55 m and shove attention 4.0 s (Interaction.cs); the Footing words and Violence.SeenFrom as quoted; 0.34 / 0.09 = 3.8 s.
- **The target list adds up**: all 17 lengths equal their frames at 30 fps; every key frame lies inside its clip; B01's 0.60 s and B02's 1.2 s recoveries are right; the 2.0 s, 0.2 s and 190 ms figures come from the sources cited.
- **Content and rulings**: no alcohol or gambling detail beyond naming where the games touch the rule; no children; no jump, fists only, firearms left out, and the test forbids any health bar on screen. The project's spec names are corrected to canon (Tom Nowak, DS Carol Ellis, the minicab office).
- **Form**: no U+2014, U+2013 or italic markup in either file; every cited repository path exists; COMBAT.md ends with Not reached, Unverified and Sources; no number marked unverified sits in a total or ratio other than the case in fix 11.

## Note for the coordinator (no change to either file)

CREDITS-MAP.md section 1 reports that MobyGames was retried "with a Chrome browser identity" after its robot check. A retry under a browser identity is a try at getting round a block, which the brief rules out. It failed, nothing from it was used, and the file says so openly, so no text change is asked; it should not be repeated.
