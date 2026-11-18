# Review: PROTOTYPE-SCOPE-DRAFT.md (17 November 2026)

Fresh reviewer, about 13 minutes. Checked against canon.md, RULINGS.md, PLAN.md, RECIPE.md, game-design (combat-design.md, weapons-spec.md, open-city-spec.md, story-outline-2026-09-28.md, warehouse-fire-2026-09-29.md, rumour-reach-2026-09-23.md), production/research/lane/SIM-IN-BROWSER-2026-11-17.md, and the published prototype page (read with the Artifact tool: its page and its 1.21 MB ledger.js, version 1794862482-9f9b).

## Verdict: PASS WITH FIXES

The structure is right (system by system, question, hand-over, checks, wave, rough size), the content rule is respected (drugs never a verb, no children in crowds, no sexual content, no alcohol goods), sizes are marked rough throughout, the build plan (source folder, one-HTML build, Node tests, one simulation with the Core as the home of every rule) is sensible, and no em-dashes or italics were found. Prototype claims spot-checked in the code hold: 45 seconds a game hour, naming thresholds 0.36 and 0.2, Tommy at 1.05, starting money 23.50, Grace's kitchen, the "Not built" list, the rivals and Garbutt as names only, Philip absent. But two rulings are contradicted (the map, the endings count), three of the five decisions are already settled by his rulings, and several research figures are misquoted.

## Fixes

1. Map (ruling 28 Oct: "the Hook plus the docks; more districts in updates after release"; 5 and 6 Nov: deep before wide). Section 3, "The town beyond Quay Street (seven districts)", and section 1 line 2 ("a town beyond one street") put seven districts in scope. Retitle it "The Hook and the docks", size it for those two, and say the other five districts are after release. The docks are not mentioned anywhere in the draft; add them (they carry the Widow's fish dock, already spoken of in the prototype).

2. Endings (ruling 28 Oct: "one main story with two or three endings"). Section 3 "Story beats and endings" lists five (Quiet, Both, Kingdom, Straight Life, Burn Both) from the older outline and ActThree.cs. Either cut to the ruled count or name the conflict and make it one decision with a recommendation. This is a real story-scope question and can take the place of a removed decision.

3. Decision 4 (combat option A) is already settled: RULINGS 28 Oct ("fists, improvised and carried weapons, rare guns") and 12 Oct (combat-design.md, guns only after melee works). Remove it; cite the rulings in the combat entry instead. Likewise drop "guns last after fists pass your playtest" from decision 1, since the ruling already fixes it.

4. Decision 3 (the invented fire) is settled: RULINGS 30 Sep rules "the warehouse fire as drafted" (warehouse-fire-2026-09-29.md; the approved outline makes it Act I's founding rumour). The prototype's "No. 4 burned five weeks before" must be replaced by the ruled fire, as a wave 1 item, not a question. The invented night jobs are story drafts the session may replace within canon (RULINGS 8 Nov); record in DECISIONS.md, no decision for him.

5. Combat entry misses the carried-weapons tier. combat-design.md has three tiers (improvised; carried: cosh, knuckleduster, utility knife, flick knife, bat; rare firearms). The draft says "fists and improvised" in sections 3, 4 and decision 4. Add carried weapons to wave 2, with their rule (seen on you, found in a search, must be got rid of). Also name the three ordered gaps (outnumbered, running away, police arriving during a fight; D56) as the wave 2 order.

6. "Tom will not hit a woman, anyone 60 or over, or the priest" (section 2, and the check "who he will not hit holds" in section 3) is a prototype invention, not in canon or combat-design.md. Mark it invented, and either drop the check or put it to him as a menace and violence question; it must not reach the Unreal spec unruled.

7. Sim-in-browser figures misquoted (SIM-IN-BROWSER-2026-11-17.md, section 4 bullet 3 and section 3):
   a. 102,960 golden answers (102,962 lines including two headers), not "102,962 rows". Fix in the perception entry too.
   b. "only two small files need leaving out" is wrong: the research found they cannot be left out; both stay compiled and their unsupported calls are never made.
   c. Download "about 2 to 4 MB, not measured", not "2 to 3 MB".
   d. The research's own plan builds on a GitHub build machine, so no cloud access to Microsoft's sites is needed; his PC at most 2 hours. Update the "either cloud access or one try on his PC" line.
   e. Add the research's 15 to 27 cloud hours for the browser Core as its own wave 1 line, and count it in the total.

8. Total does not match the parts. The listed ranges sum to about 253 to 468 hours (side stories at three to five samples), not "270 to 480". Recompute after fixes 1, 5 and 7e, still marked rough.

9. Fable's role (section 4, "Who builds it") conflicts with rulings: 10 Nov, Fable only after two failed tries on code or tool faults; 16 to 23 Nov, up to 20% for the hardest code. "Fable for big jumps" and "the cloud session at about 10% of a normal week" are new budget and model uses; either follow the rulings as they stand or put it to him as one money decision. Note too that 10% is the week's review share in CLAUDE.md, so pick a different budget or explain.

10. Place in the plan and the orders. RULINGS 29 Sep: "no new system before its place in PLAN.md"; CLAUDE.md: new work goes on the order's waiting list for the next Monday order, each item costed. Add a short line: the prototype stage gets its PLAN.md place and wave 1 enters through the next Monday order. Also his 17 Nov decision is not yet in RULINGS.md; say it must land there the same day.

11. Recipe map is not missing: RULINGS 16 Nov names it (the recipe map artifact, kept by the builder). Remove "unverified: no file of that name was found". Also per RULINGS 9 Nov, new recipe lines go to NOTEBOOK.md first and RECIPE.md is rewritten from it at phase end; say the section 5 lines land in NOTEBOOK.md, not RECIPE.md directly.

12. Clock and gossip differences. The note under section 2 cites gossip half-life (about 20 game hours in the page against 96 in the Core; the Core's 96 halves certainty, so say which quantity the page's "heat" maps to). Add the clock: the page runs 45 real seconds a game hour, the Core's rumour note 2 game minutes a real second (30 seconds a game hour). Both feed "does the town know within thirty minutes", so both belong in decision 2's list.

13. Canon coverage gaps. Add, briefly: permanent per-person memory (canon's moat: nothing is ever wiped) as a check in saving and gossip; the empire firsts of open-city-spec.md (first business and first racket, not only first recruit) under jobs and crew or money; June Suddaby and Father Brendan Walsh (canon's day-life ring) under story or routines; the pub as a place without drink (canon: "a design task, not a subtraction") alongside the Parade note; religion never a mechanic as a check on the chapel routine.

14. CCTV wording. In the page the CCTV is a placed prop (a "cctv" object by the bus stop) with no rule behind it found. Say "a camera prop only, no rule" instead of "unverified what it does".

15. Section 2 size wording. "One file of game code, three.js, about 5.5 MB in all" and section 4's "one 1.2 MB JavaScript file" read as a contradiction. Say: one 1.21 MB game code file, fifteen published files, about 5.5 MB in all (unverified total).

After fixes 3 and 4, decisions left: wave order (1), one simulation and the .NET licence line (2), the second CCTV site (5), plus the endings count (fix 2) and, if kept, Fable's budget (fix 9). Keep it to at most three on his page at once, per his page's rule.
