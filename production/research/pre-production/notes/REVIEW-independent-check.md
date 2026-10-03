> **Independent check** of this review, 3 October 2026, by a fresh reviewer that had not seen the work made. Kept as written. What was changed in answer is listed in ../SOURCES.md, "The independent check".

# Adversarial review of production/research/pre-production (3 Oct 2026)

Nothing in the repository changed. Highest severity first.

## High

1. **"Every measured run on the key ran unchecked" is false** (SUMMARY l.33; FEASIBILITY l.47).
   - talk-cost-2026-09-30-after.md, a `--live` run on the key, logs "check… (21 turns)".
   - That line exists only with a checker attached (ConversationEngine.cs l.1733–1748).
   - True: the tester's in-game run was unchecked; the cost sample's next run will be too (talk_cost_sample.py l.202).
2. **P3 and P4 cannot run as written.**
   - The tester's cap is $0.50 in code (play.py l.82, self-test l.683; DECISIONS l.173).
   - Checked talk costs about $0.018 a turn (talk-cost-2026-09-30-after), so 30 lines cost about $0.54.
   - P4's thirty minutes cost $0.54–1.61 at its own rates, not "$0.50–1.10".
   - Both runs would be cut short; both need a ruling and a code change, unsaid.
3. **The memory envelope is already full, unsaid.**
   - 6.0 GB on Windows' counter (4-BUDGETS l.24), against 4.8–6.1 GB measured on that counter (l.38).
   - Textures 2.38–2.43 GB against a 2.4 GB line.
   - l.79's "about 8.4 GB" is 6.0 + 2.8 = 8.8.
4. **The performance history is misreported.**
   - l.31 says "20 runs, GPU 11.2–11.8, 3.6–4.1 GB"; git holds 23, three at GPU 12.34–12.45 ms and 4.5–4.77 GB, and omits a p99 of 21.96 ms.
   - GPU varies 1.2 ms between builds: half the 2.6 ms headroom.
5. **The base-share sum contradicts its own measurement.**
   - l.87 subtracts 0.9 ms for three MetaHumans; ue-mhcost.txt measured all three at +0.63, so the base is about 9.8 ms, not 9.5.
   - The 0.7 ms for the voice is a frame difference, not GPU time.
6. **The game's own resolution ladder is ignored.** TitleScreen.cpp l.59–74 steps the frame through 100, 70 and 55% to stay under 16 ms, and the game now draws at 55% (H4a l.267). The budgets plan at 50%, and P1 measures 50% and 67%.
7. **The texture densities measure distance from Tom, not from the camera.**
   - l.128 says "1 m (a shopfront Tom stands at)".
   - The arm is 320 cm (SliceCharacter.cpp l.65), so that shopfront is about 4 m from the camera: about 430 px/m, where 512 is enough.
   - The 1,024 tier (four times the memory) holds only where the camera comes close.
8. **"Derived" overclaims** (SUMMARY l.18).
   - Only the 14 ms and 6.0 GB envelopes are derived; with no milliseconds-per-triangle figure, every limit and split is asserted.
   - P11's 0.2 ms times four rooms uses the whole 0.8 ms share, leaving nothing for mapped rooms or glass.
   - P6's 600 MB for twelve passers-by exceeds the 0.5 GB line for all skinned meshes.

## Medium

9. **The feasibility verdicts break their own rule.** The rule (l.17) makes a conflict RISKY.
   - Areas 4, 9, 30 and 34 carry "!" yet stand FEASIBLE.
   - Area 5 (props) shows the bar met. DECISIONS l.196 says "the phone box, skip and pallets look like placeholders", and the asset plan has about 25 kinds still to make.
   - Area 9's rain and dusk part, UNKNOWN, has no proof.
10. **Search summaries are used as evidence without their mark.**
    - Area 11's automotive and area 17's crowd "reported NoAI" are [SS] at their source (2-VEHICLES l.10; 0-SOURCES l.172).
    - The cloth, hair and animation-budget limits and P21's buffer rest on [SS] too.
11. **Misquotes:**
    - "23–25 of 60": the source has 48 answerable questions in that set, on the bench, not the real path.
    - "2.1 s, 24 turns": the source says 22.
    - "Against their sheets": DECISIONS l.81 says "concept portraits".
    - "Four of six cores": the source runs the game "on the other eight" logical processors.
    - "No privacy notice": DECISIONS l.80 records one.
    - "(4.6)" at l.53 points to the processor section.
    - "Neither is true" (area 36): his unbudgeted play is checked.
12. **The key's dollar is read two ways.** 1-AUDIT row 9 and R10 read it as "for the runs"; area 32 reads it as his play too. DECISIONS l.257 ("nothing else uses it") excludes friends' play, against l.200: a conflict, not "not ruled".
13. **Praise:** "settled what it wants early and well" (SUMMARY l.13; 1-AUDIT l.55).
14. **R2's fallback reopens the voices.** The paid voice would reopen "voices as chosen" (DECISIONS l.183), and Inworld is not on the allowlist. Neither is said.

## The risk register

Broadly right. Missing:
- the rulings conflict over friends' talk on the key (likelihood 5, consequence 5 until he rules);
- a target date, without which no slip can be scored;
- Jafar's eye as the only judge of every visual;
- a canon breach still placed: the back-bar picture (vignette-pieces.json, decal_05_interior_bar_back);
- the key in plain text in an account his friends use.

## Gaps against the brief

- 5-DONE lacks decals and wear, accessories, the hillside, ground materials and animation.
- There is no decal or particle budget.
- The internal resolution (1720×720) is never stated.
- "Narrative bible: HAS" has no row in the audit.

## Verified correct

- Code and records: Program.cs l.273; BudgetedClient l.23; CrimeProbe l.3248; the workflow l.555; ROADMAP l.74; the rulings sweep l.166; terrace-front l.5672; allowlist entry 8; 42/42 NoAI.
- Figures: perf, walk, card-timing and TitleScreen; GLB counts; the repository is public; 57,872 rows; 12 mutations.
- Arithmetic: 1720 ÷ d, 14.0 ms, 6.0 GB.
- The counts 23/4/10/21 and the P and area cross-references.
