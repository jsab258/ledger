# Costing one complete named person end to end: Ron (plan, 8 November 2026)

For the waiting-list item n02-9-phase1-skills-playbook (order of 2 November, section 9, joined 8 Nov 14:25). This is a plan only: nothing was built or run, and no API was called. Every local file named here was read on 8 November 2026. Tags follow UNIT-COSTS-2026-11-02.md: **M** measured (summed or copied from a named file), **I** inferred (judgement or arithmetic on measured figures), **R** a RECIPE.md Cost line (the session's own rounded figure), **E** an estimate made before the work. Anything with no record is marked **not recorded**. The session makes the decisions.

## Method and reference

**Reference: Mafia and Kingdom Come II, as Study 6 reads them** (production/research/aaa-reference/studies/06-characters-wardrobe.md, read 25 Oct). Both split a person into **unique parts** and **shared parts**:
- Unique: the head. Mafia has 101 male and 20 female heads. KCD2's Kutná Hora has 139 hand-set appearances built from 90 heads.
- Shared: bodies by type (Mafia has 32 male body meshes in five families; KCD2 has one body per sex), and a garment library with colour variants (Mafia has 62 male tops making 338 top-and-colour rows, and 780 outfit presets).

The plan takes the method, not the numbers. LEDGER has about 44 named people (14 main characters plus about 30 regulars: production/progress-page/progress.json phase 5; RULINGS 30 Sep). Mafia's counts are far larger than anything here, so they are not used as targets. Neither game has live talk, so for talk the method is **none found**.

**Unit-cost formula (I).** A person's unit cost is the sum of:
- their unique parts' hours;
- each shared part's hours divided by the number of people who use it;
- their own gate;
- their talk production.

Hours are turned into dollars at the stand-in rate of **US$22 to 38 per logged hour (I)**. That rate comes from the week of 26 Oct to 1 Nov (UNIT-COSTS-2026-11-02.md; unit-costs-2026-11-02.json, conversion_usd_per_logged_hour), and it is used only until a token audit covers 2 to 8 November. Helpers' clock time is extra.

**Counting rule.** Shared time-log windows are split equally across the clauses or people they name, the same rule as UNIT-COSTS. Overlapping windows are task-hours, not wall-clock hours.

## Ron, part by part

Ron Kirby: canon's "Mickey's door and rank", age 58, body MH_RoccoP2 (CLOTHES.md; production/casting/ron-kirby/SHEET.md; production/specs/hook-cast.json, id "rocco").

| Part | Done | Cost on record | Left |
|---|---|---|---|
| Body | MH_RoccoP2 exported to F:\LedgerTools\bodies (CLOTHES.md) | not recorded (before the time log began on 5 Oct) | nothing |
| Face | frozen as Ron P2 (RULINGS 30 Sep; RECIPE.md PROVEN, People) | "Cost not recorded" (RECIPE.md line 1550) | street light still underlights faces (FINDINGS: faces); no Ron-specific fault listed |
| Clothes: boots | Ron's own pair, v2 maps; passed in the game; also carried to Tom and Darren (garments.json RonBoots; DECISIONS 7 Nov 17:40) | the pair itself not recorded (September clothing session); refitting it to Tom took 2.95 h with 1.45 h set aside (M/I, UNIT-COSTS) | none for Ron; boots shortfall listed: 10,416 triangles against 6,000, waived (FINDINGS: clothes) |
| Clothes: jeans | RonJeans, Tom's jeans carried onto Ron (garments.json) | Ron's refit share of the dress-the-cast windows, see the next table; source piece (Tom's jeans) 1.61 h (M/I, UNIT-COSTS) | the sheet says "dark grey work trousers" (SHEET.md line 13): not settled, see "For the session" |
| Clothes: jumper | RonJumper, carried from Tom's, cleared front and back of the head mesh; wool knit, rib, navy (garments.json; DECISIONS 7 Nov 21:45, 8 Nov 00:30, 04:44, 13:10) | refit and knit, see the next table; source piece (Tom's jumper) 2.81 h (M/I, UNIT-COSTS) | shortfalls listed: hem rib faint, navy near black at a distance, a scaly highlight on the shoulder (DECISIONS 8 Nov 13:10); the sheet says grey |
| Clothes: donkey jacket | not made. RonJacket and RonJacketB are held method tests of 30 Sep, "not for his page" (garments.json) | Ron's earlier outfit attempt on 7 Oct failed three reviews: its third try sits in a 1.99 h window (M), shared with other work (unit-costs json, garment set_aside) | everything. Estimate 9.8 h E (HOOK-GARMENT-LIST-2026-11-03.md row 1). The first jacket of its kind took "at least 9.8 h" (I) and never passed its collar (n02-tom-jacket set aside, 4 Nov) |
| Hair | Epic groom; moustache strands kept (time log 2 Nov 13:36). Hair colour item: two tries failed 7 Nov, for the whole cast (DECISIONS 7 Nov 19:18) | under 0.5 h Ron share (I). The hair sky-light try took about 2 h across the cast (R, RECIPE 7 Nov) | the hair gate of RULINGS 3 Nov has not been passed by anyone. Ron's near hair reads dark, not grey (FINDINGS: clothes and hair); a third colour try is his to give |
| Voice | VCTK p227 on Pocket for live and prepared lines (RULINGS: voices; DECISIONS 3 Nov 13:04) | about 0.9 h (I): Pocket switch 1.2 h R for two people, so 0.6; listening test 0.6 h R for three people, so 0.2; Pocket mend 0.3 h R, so about 0.1 | nothing known |
| Daily routine | in the simulation: hook-cast.json "routine" (off, cafe 7, rank 8, fish front 12, rank 13, quay 17, office 19, off 23) plus a Sunday table | not recorded. UNIT-COSTS: "Person's routine: none measured" | the quay spot moved 7 Nov, not yet walked (FINDINGS: quay end) |
| Live talk and claim check | Ron on the shipped talk program, small talk on Haiku (DECISIONS 3 Nov 07:58); claim check shared | shared features cost 1.5 to 2.8 h each (R, UNIT-COSTS). Running cost about US$0.12 an hour of play at 15 replies (M, run D, COST-PER-HOUR-2026-11-02.md), about 27% less with caching (M, TALK-LEVERS, 7 Nov) | speech bar missed for everyone (2.02 s, FINDINGS: speech). Nothing Ron-specific |
| Prepared lines | 159 street lines of his own (DECISIONS 30 Sep); made-ahead sounds remade on Pocket (RECIPE 26 Oct) | lines: not recorded. Remake: inside the 1.2 h above | count of voiced clips not read (unverified) |
| Mouths | live lines follow the voice's loudness. Epic's audio-made faces kept on file, played only with -MadeFace (DECISIONS 1 Oct) | not recorded | prepared lines on Epic's audio-driven mouths: ruled 1 Oct, still "carried over" (archive order, aaa-s07-07). No record of it being built (unverified) |
| Gate | collar back passed one fresh final reviewer (8 Nov 04:44); knit passed two rounds (13:10); his look: interim yes 07:41, then yes on the clothes' floor 13:12 (DECISIONS 8 Nov 08:28, 14:25) | about 5 Ron reviews at US$0.59 to 1.66 each (M, per reviewer), so about US$3 to 8 (I), already inside the window dollars. His own minutes not recorded | full whole-person gate: hair, jacket, the sit (his sit proof failed "never-seated" on 8 Nov, DECISIONS 07:05), the packaged walk, and his look at the whole person |

### Ron's refit windows (production/time-log.jsonl, read 8 Nov to line 586)

| Window | Logged h (M) | Ron share (I) |
|---|---|---|
| 7 Nov 15:21-17:07, dress, front wear, hair | 1.77 | 0.29 (a third of the window to dressing, half of that Ron) |
| 7 Nov 18:42-20:11, Darren's second fit, both hems (Ron's jumper redone, DECISIONS 19:18) | 1.49 | 0.5 to 0.75 |
| 7 Nov 21:32-22:41, Darren's third try, Ron's collar points (no stop; ended by the next start) | 1.15 | 0.57 |
| 7 Nov 22:41-23:19, whole-person films and review | 0.63 | 0.32 |
| 8 Nov 00:22-00:40, Ron's collar try 2 | 0.30 | 0.30 |
| 8 Nov judging of the collar, not in the log | | 0.33 (R, RECIPE 8 Nov "about 20 minutes") |
| 8 Nov knit, both men (0.35 h logged, the rest after the log's last line) | 0.35 | 1.0 (R, about 2 h for two) |
| **Ron's clothes refit** | | **about 3.3 to 3.6 h (I)** |

### What is known of Ron's cost so far

- **Logged work kept, Ron-specific (I): about 4.2 to 5.0 h.** That is the clothes refit, 3.3 to 3.6 h; the voice, about 0.9 h; hair, under 0.5 h.
- **Set aside:** about 1 to 2 h of the 7 Oct outfit (I).
- **Dollars (I):** about US$90 to 270 at the stand-in rate. No token audit covers 2 to 8 November.
- **Not in that figure:**
  - shared source pieces: Tom's jeans 1.61 h and jumper 2.81 h; the knit tile;
  - shared systems: talk features, walk-off 3 h (R), sitting;
  - everything made before 5 October: body, face, voice pick, street lines, talk card and facts, routine;
  - everything still left.

**Biggest unknown: the donkey jacket.** It is estimated at 9.8 h E. Records run 2 to 4 times their estimates (HOOK-GARMENT-LIST, "Against the order"). No jacket of any kind has passed in the game, and Tom's collar fault came from his neck turning against a collar that follows his chest (n02-tom-jacket). A donkey jacket collar faces the same risk (I).

## Steps to measure it

1. **Dollars for 2 to 8 November.** The session runs `python tools/token_audit.py --since 2026-11-02 --until 2026-11-09`. It reads this PC's session logs only, with no API call. Then read the n02-9-dress-the-cast and n02-9-knit-and-neckband rows. Caution: the audit books parallel helpers to the window opened last (UNIT-COSTS method), so per-window dollars are not floors. Recount helpers by their own timestamps, as the 2 Nov review did. About 0.3 h.
2. **Work before 5 October.** Read-only `git log` commit times on production/casting/ron-kirby/, the face and body records (DECISIONS 28 to 30 Sep), the routine rows in hook-cast.json, and production/casting/ron-kirby/STREET-LINES.md. Results are tagged I. Anything git cannot bound stays "not recorded". About 0.5 h.
3. **From now on, one tag per person and part** in the time-log task text, for example "person ron: jacket". Then the token audit groups by person. Darren, dressed in the same windows, is the repeat to compare (the efficiency ruling of 8 Nov: each repeat clearly cheaper than the first).
4. **Time Ron's remaining parts as they are built**, each its own window, tries and set-asides counted:
   - the donkey jacket (Hook list row 1, reference: Mafia's method by way of the game-garment skill);
   - Ron's hair through the 3 Nov hair gate;
   - his prepared lines on audio-driven mouths, after first counting his voiced clips;
   - the sit re-proved;
   - the whole-person gate, the packaged walk and his look.
5. **Talk per person.** Check whether the talk program's closing cost line splits by speaker (unverified). If it does not, use the per-hour figure times Ron's share of replies in a measured walk. No paid run only for costing: use the next speech run's existing lines (api-spend.jsonl).
6. **A regular, for the second tier.** Cost one regular end to end as well, cheapest first: row 5 of the Hook list, the rank men, who are variants only (0.3 h E each). Regulars differ from main characters: shared kind lines, one of about ten voice slots (DECISIONS 30 Sep), clothing variants. RULINGS 3 Nov treats whole people to the full gate and his look, so the regular's gate is measured, not assumed smaller.

## From Ron to the 2027 line

- **Two units.** U_main is Ron complete, checked against Darren's repeat. U_regular is the measured regular. Each has unique hours plus a share of shared hours, its gate and its talk production.
- **The 2027 people line (I):** 14 × U_main + about 30 × U_regular + the shared one-offs.
  - Shared one-offs: the garment bases, at most the Hook list's 77.0 h E, or its rows 1 to 3 at 29.0 h E. At the records' 2 to 4 times, rows 1 to 3 come to 58 to 116 h.
  - Systems: the talk features, walk-off and sitting.
  - Use either the Hook list's garment hours or the per-person garment hours, never both.
- **Hours into weeks.** Divide by the week's measured production hours. The week of 26 Oct to 1 Nov had 55.35 logged hours inside windows (unit-costs json; 70% production by CLAUDE.md). That figure is from one week only (I).
- **Done when:**
  - every part of Ron's table has an M or R figure, or a stated "not recorded" with git's bounds;
  - Darren's repeat and one regular are measured;
  - one fresh reviewer has checked the sums against the time log and the audit.

## For the session (found, not decided)

- **Jumper colour against the sheet.** Ron's sheet says "a grey knitted jumper; dark grey work trousers" (SHEET.md line 13). DECISIONS 8 Nov 11:04 chose navy "unlike Tom's grey", saying the casting sheets settle it. His tap of 13:12 passed the look in navy, and the game wears jeans. Whether his tap or the sheet governs, and whether the sheet's approval file is affected (tools/approvals.py), is the session's to settle.
- **Ron's name in old records.** The 25 Sep entry calls Ron's approved face "C1" (DECISIONS line 41). RULINGS has it frozen as P2 from 30 Sep, and RULINGS stands.

## Unverified, unreached

- Unverified:
  - all of Ron's dollars;
  - the Ron share of every shared window;
  - whether audio-driven mouths exist for any prepared line;
  - the count of Ron's voiced clips;
  - whether talk cost splits by speaker.
- Not read:
  - time-log entries after line 586 (11:05, 8 Nov);
  - the knit and page work after 11:05;
  - any token audit after 2 November (none exists).
- Mafia's and KCD2's per-character production costs are unpublished in the studies.
