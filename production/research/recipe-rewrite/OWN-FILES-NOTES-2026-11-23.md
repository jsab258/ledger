# Own-files notes for the recipe rewrite (n23-5), questions 1, 4, 5, 6 (read 23 Nov 2026, project files only)

## Question 1: the 20 Nov lesson

- The lesson is named, not explained, in the project files. The order says "research first, then measure the design, then the one-shot (the 20 Nov lesson; advisor 289)": production/orders/2026-11-23.md:22 and :53.
- The attempt that ran before its design was measured is the cloud one-shot. From 20 Nov 14:21 it built from one giant prompt (41 play stories as the finish line), Fable 5.2, one builder, overnight until every story passed, the week reached 90%, or Sat 21 Nov 18:00: DECISIONS.md:581. Its second run began about 10:13 on 20 Nov: DECISIONS.md:580.
- Cost figure: helper spend on 19 Nov was about US$645.57, of it Fable US$529.43; on 20 Nov US$83.07. The cloud one-shot's own spend is not in those logs: production/research/token-audit/DAILY-2026-11-20.md:10 and :34. Whether the US$529 was the one-shot is unverified.
- The same evening the design was found unmeasured: Kiln, hair and the crowd were paused until the prototype holds "on reference numbers"; the one-shot's rise and end wait for "the new story measure": DECISIONS.md:587.
- Rule that followed (20-21 Nov): the giant prompt's rewrite and the one-shot's rerun wait for DESIGN-COMPLETE.md's design gate (all parts measured or ruled out, review themes answered, two red teams in a row catching 9 of 10 planted gaps, nothing new) and his approval of the measured story: DECISIONS.md:588. Then, no date, the one-shot starts only on a complete blueprint: DECISIONS.md:603; RULINGS.md:38.
- Earlier evidence of unmeasured design: the loop prototype's gate found 8 real faults (crashes untold, lamp posts and parked cars not solid on foot, keyboard steering snapping, pad unusable, camera hiding Tom indoors): production/lane/PROTOTYPE-GATE-FINDINGS.md:21-42. The prototype's clock (45 s a game hour) and Unreal's (30 s) disagreed until 21 Nov ruled 60 s: production/lane/PROTOTYPE-SCOPE-DRAFT.md:41-45; DECISIONS.md:551 and :600.
- The scope draft's own recipe proposals, 17 Nov, "confidence low": a playable skeleton before production, feel studies before big systems, the skeleton as spec of record: production/lane/PROTOTYPE-SCOPE-DRAFT.md:262-270.

## Question 4: what "measured" means

- Solid rule (advisor 302, 21 Nov): a number is solid only on at least five samples from uncut, dated footage, read at a step finer than the thing measured. Everything else is a lead; only solid numbers count as measured for the design gate. Each open question is either priced to finish or marked not needed, naming the blueprint part it would have served: production/research/lane/measurements/STATUS.md:11.
- State on 23 Nov: one solid number named in the repricing (G5 heat length at peak two stars), plus a few rows the table reports solid (parked-car entry time, return resumes pursuit); every other number in the eleven sheets rests on fewer than five samples, mixed cut footage, or a coarse step: STATUS.md:14 and :21-22.
- Reading by code, not by model: no model passed as star reader; the answer key for any later trial is the code count: STATUS.md:56-59, :61-62.
- Design gate (as quoted): all parts measured or ruled out, review themes answered, two red teams in a row catching 9 of 10 planted gaps, nothing new: DECISIONS.md:588.
- Parts-tree standard: each part a player feels has a standard (a measured reference game or a rule), else it is a research item: RULINGS.md:39. Tree size 354 parts (295 buildable): DECISIONS.md:522; felt parts without a measured standard were given 18 research items: DECISIONS.md:550.
- Drills in installed games versus footage, estimates: STATUS.md:40-49.

## Question 5: the check that fails a build

- Prototype ruling, Unreal part: tools/research_rules_check.py fails (in ci) any commit touching ue-probe since the ruling entered RULINGS (21 Nov 10:24) while "no Unreal work until the prototype" stands: tools/research_rules_check.py:3, :23, :35; production/rulings-enforcers.json:186.
- "He plays only after the one-shot": tools/needs_you_page.py refuses an item asking him to play or test the prototype while no production/lane/one-shot/REPORT-*.md exists: tools/needs_you_page.py:34-36, :145-153; selftest :333-336.
- One-shot start gate: enforced by "the advisor's launch check" and a Monday audit line; "the giant prompt task checks this gate first": production/rulings-enforcers.json:631. No script is named. The Monday audit is a review, not a build failure.
- Parts tree: tools/lane/parts-tree/check.py, run by the cloud lane each loop and by the Monday audit: production/rulings-enforcers.json:638. The file is not in this checkout.
- Clock held by the design proof's clock rows and the prototype's clock test: production/rulings-enforcers.json:631.
- Not found: any script testing DESIGN-COMPLETE.md's gate or the five-sample rule. Tool hits for "DESIGN-COMPLETE", "one-shot" or "design gate" are needs_you_page.py, progress_page.py, pace_line.py (pace and display, not the gate) and mixamo-pick.
- Does RECIPE.md link any of this: a grep of RECIPE.md for "one-shot", "20 Nov", "blueprint" matched nothing. It does not today.

## Question 6: the six preparation items

- The list: (1) checkers proven with planted faults, (2) technical plan, (3) design numbers through the simulation, (4) full inventory against the one-shot's week, (6) sound plan (cloud), (7) live talk settled from the talk bake-off (n16-6), by Fri 4 Dec. Item (5), him playing the prototype, was struck 21 Nov 21:43: production/orders/2026-11-16.md:73; DECISIONS.md:612; production/orders/2026-11-23.md:9. The numbering keeps its gap; DECISIONS.md:603 (earlier) still said seven.
- Order item 35 adds four footage studies before the one-shot and says "Monday's recipe rewrite puts the one-shot preparation order first, each step with its method file and cost": production/orders/2026-11-16.md:72.
- What each item taught was not found written down: none is reported finished in the files read.
- Related rule: live voices run on his PC's Pocket voices via a local helper, built in the loops, hookup in the blueprint: RULINGS.md:38; DECISIONS.md:612.

## What could not be found

- DESIGN-COMPLETE.md (searched the whole repository; DECISIONS.md:588 and :612 place it under lane/design-proof/, absent here; likely on the cloud lane's branch, unverified). Its checklist is known only from DECISIONS.md:588.
- production/lane/parts-tree/ (PARTS-TREE.json, GAPS-2026-11-20.md) and tools/lane/parts-tree/check.py: absent in this checkout.
- production/lane/one-shot/, ONE-SHOT-PROMPT.md, REVIEWS-oneshot.md, any "One-shot stopped" row, any one-shot report: absent.
- A written statement of what the 20 Nov lesson was, its cost in hours, or how the one-shot ended: not in any file read. Advisors 289 and 290 are only summarised at DECISIONS.md:603.
- NOTEBOOK.md: no 18-23 Nov entry on the one-shot lesson (only line 2936, the withdrawn ask).
- A distinct "prototype-ruling enforcer" script: only research_rules_check.py (Unreal part) and needs_you_page.py found.
