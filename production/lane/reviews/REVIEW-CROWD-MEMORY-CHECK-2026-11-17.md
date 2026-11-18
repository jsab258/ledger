# Fresh review: crowd and card memory check, 17 November 2026

Reviewed: production/lane/CROWD-MEMORY-CHECK-2026-11-17.md (1,489 words), against PACKING-PLAN-2026-11-16.md, its review, OWNER-DUMP-2026-11-16.md (l.49, 141-158), 4-BUDGETS l.172-174, PLAN.md l.46, CROWD-DISTANCE-2026-11-09, the archived DECISIONS entry for 8 Nov, and six Epic pages fetched today. Nothing run.

**Verdict: PASS WITH FIXES.** The main conclusion holds: the line the game lives under on 16 Nov was 4,711 MB, not 6.0 GB, and about 28 people fits only a 6.0 GB grant. One subtraction is written wrong, one counter gap is misstated, and the check misses that the plan's passer-by count breaks the project's own cap.

## Arithmetic checked

Correct: 4,711 budget and 361 demoted (dump l.141-142; used less budget equals demoted); 5,072 peak, 4,952 settled; 5,213 median, 5,565 peak on Windows' counter; step 1 saves 160 (4,952 to 4,792); ceilings sum 450+600+500+300+640+800+600 = 3,890, and with TSR 156, shadows 41 and ~670 outside the dump they pass 4,711; 28 people = 3 x 100 + 25 x 20 = 800; section 4 peak 5,072 - 160 - 1,070 = 3,842 (about 3,850), 4,711 - 3,850 - 471 (10%) = 390; 3 x 100 + 4 x 20 = 380 and 19 x 20 = 380; body maps 21.38 + 21.38 + 10.69 = 53.45 MB (dump l.49, frame 1100); hours 15.5 = 1.5 + 2.5 + 10 + 1.5, about 12 to 13 left; forum skin cache 137/50 = 2.7, 31/50 = 0.6; the moving budget 9,427, 7,128, 5,771 (LAUNCH-PEAK l.20), 4,870, 4,711; the 4.6 GB is the 8 Nov COOK-PICTURES decision (now in production/archive/DECISIONS-to-2026-11-09.md l.1300).

## External claims spot-checked (fetched 17 Nov)

- MetaHuman Crowds Experimental, "caution when shipping": confirmed (Crowds page). Stripped high LODs, card hair, no correctives on instanced far characters: confirmed. "About 10 full actors near": confirmed on the Create MetaHuman Crowds page, as an example ("you might allow 10"), not on the main Crowds page.
- Animation Budget Allocator saves game-thread time, default 1.0 ms (a.Budget.BudgetMs), no memory claim: confirmed.
- Streaming pool holds "UI textures, NeverStream textures, cubemaps and streaming textures": confirmed word for word.
- LODSync warning on forcing 0 or 1 across a crowd; r.HairStrands.UseCardsInsteadOfStrands 1; minimum LOD 3: confirmed. Epic gives no distance: switching is by screen size.
- LOD table (head 24,000 to 130; body 30,500 to 1,507; 669 blendshapes; strands LOD0-1, cards LOD0-4) and no MB per MetaHuman: confirmed. UE Optimized tops at 2K: confirmed on the materials page.
- Forum "about 8 full actors": in the cited skin-cache thread per CROWD-DISTANCE l.10, 23 (a staff opinion, not a spec).

Style: no em-dashes, en-dashes or italics. Unreached sources are listed and not used as evidence. Plain enough for a lane note.

## Findings and fixes

1. **Wrong subtraction (section 2, row "Room left about 800 MB").** "5,505 less 1,230" gives 4,275 and about 436 MB room, not 280. The 5,505 peak was already read with step 1 on, so only step 2 comes off. Fix: replace "(5,505 less 1,230) only about 280 MB" with "(5,505, already with step 1, less about 1,070 for step 2) only about 280 MB, and below zero after the 10% spare".

2. **Counter gap misstated (section 1 last bullet; section 5 risk 2).** The pairs give 261 (5,213 against 4,952 settled), 356 (5,148 against 4,792 after step 1) and 493 (5,565 against 5,072 at the peak). Fix: section 1 "differ by about 350 to 500 MB" to "differ by about 260 to 490 MB"; risk 2 "about 400 MB apart" to "about 260 to 490 MB apart".

3. **Missed: the plan's passers-by break 4-BUDGETS (section 2, row "About 28 people"; section 4).** 4-BUDGETS l.173 caps passers-by at 12, at 15 MB unique each, with card grooms up to 16 MB counted separately (l.174), so a passer-by can reach about 31 MB, not 20. The plan's 25 and the check's 19 both exceed 12 while the plan says "This plan keeps it". Fix: add to that row's note "and 25 passers-by exceeds 4-BUDGETS' cap of 12; at 15 MB plus a card groom up to 16 MB, 20 MB each is low"; in section 4 change "about 19 passers-by" to "at most 12 passers-by (the 4-BUDGETS cap), about 12 x 20 = 240 MB, or fewer at up to 31 MB each".

4. **"Cards beyond 5 m" credited to Epic (section 6).** Epic's pages give no distance; groom LODs switch by screen size. The 5 m is the project's own rule (4-BUDGETS l.173-174). Fix: "Plan the passers-by as Epic's pattern: about 8 to 10 full MetaHumans near, the rest instanced at high LODs with card hair; strands only within 5 m (4-BUDGETS)".

5. **Added people against people already counted (section 4).** The 3,850 peak already holds today's cast (hair 178, MetaHuman shared 68, Rocco's body maps), so "3 near plus about 4 passers-by" reads as the whole street. Fix: "That is either up to 3 more near people plus about 4 passers-by, or ...", and say that today's cast is inside the 3,850.

6. **Room left without the spare (section 2, same row as 1).** "True on the engine's counter (4,711 less about 3,850)" is 861 before the 10% spare that section 4 takes (390 after). Fix: append "; about 390 after the 10% spare (section 4)".

7. **"Binding line" from one reading (section 1 last line).** The 4,711 is one dump; risk 1 shows it moves. Fix: "So the binding line on the 16 Nov reading was about 4.7 GB, not 6.0; it moves (risk 1)."

8. **4.6 GB citation (section 1 first bullet).** The 8 Nov entry now lives in the archive. Fix: "(DECISIONS archive to 9 Nov, 8 Nov entry, ...)".

9. **Crowds example source (section 3, Crowds bullet).** The "10 full actors" is the Create page's example, not the main page's. Fix: "Epic's Create MetaHuman Crowds page gives about 10 full actors near as an example; the Crowds page draws the rest as instanced skinned meshes ...".
