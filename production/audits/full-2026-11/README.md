# Full audit, November 2026 (his order "Do it now", 00:18, 19 Nov, advisor 237)

Run by the cloud lane (LANE-QUEUE item 4q). Reads and reports only: nothing outside this folder and tools/lane/audit/ is changed, moved or deleted.

## Method (researched 19 Nov 2026)

Standard project and software audit practice, applied to a one-owner studio run by AI sessions:
1. Inventory first: every asset listed with owner, age, use and status, so nothing is judged from memory (software audit process guides, e.g. DisputeSoft's audit process and TechTarget's "What is a software audit").
2. Traceability both ways: every owner decision traced forward to the text and check that carries it, and every rule traced back to a decision; gaps are "lost", clashes are "contradicted" (requirements traceability practice, Siemens Polarion "7 questions" and Perforce on audit traceability).
3. Independent reviewers by area, each fresh, with evidence on every finding and a proposed end; one blind outsider with no briefing (the postmortem literature finds teams miss their own drift: Washburn et al., "What went right and what went wrong", 155 game postmortems, Microsoft Research).
4. One ranked report, checked against the evidence by a fresh reviewer before publishing.

Sources (found by search, 19 Nov 2026): https://www.disputesoft.com/software-audit-considerations-and-process/ ; https://www.techtarget.com/news/software-audit/872601/ ; https://blogs.sw.siemens.com/polarion/traceability-7-questions-you-need-to-ask-to-derive-real-value/ ; https://www.perforce.com/blog/alm/integrated-traceability-secret-surviving-your-next-software-development-audit ; https://www.microsoft.com/en-us/research/?p=238008

## Stage 1 (done 19 Nov, 01:16 to 01:45)

- INVENTORY.md and inventory.json: 1,095 repository folders (tools/lane/audit/inventory.py, tested), plus the builder's PC inventory (216 folders, pc-inventory.json).
- DECISIONS-TRACE.md and decisions-trace.json: 872 decision records from seven sources (DECISIONS.md, RULINGS.md and canon.md, the orders, 273 advisor rows and their acknowledgements, 87 page picks, the old version's records), each checked against today's texts: lost 11, contradicted 21, open 49, unclear 1, in force but unchecked 246, enforced 179, superseded 108, done 257. Extraction by seven Sonnet helpers, status by eight Sonnet helpers (briefs in work/), joined by tools/lane/audit/merge_decisions.py and build_trace.py (tested).
- Cross-cutting first signs for stage 2 (not yet verified): the repository's CLAUDE.md still carries several lines his later rulings replaced (third try needs his yes; 20% kept for him; reference first by opening Mafia's or KCD2's files; FOR-JAFAR.md summaries; orders of about 1,200 words); "monday-audit" counts as the enforcer for many rulings but tests nothing and has not yet run; the ledger/ folder holds about 1.6 GB in the working tree.

## Stage 1 (d), the real size of stage 2

Stage 1 used about 2 points of the week (31% at 00:52 to 33% at 01:32 while the main session ran no helpers). Stage 1 read about 2.5 million tokens through 16 Sonnet helpers. Stage 2's eleven Opus reviewers at high effort each read INVENTORY.md (about 6k words), DECISIONS-TRACE.md (about 48k words), canon and RULINGS (7k), then their area: estimated 300k to 500k tokens each, about 4 to 5 million Opus tokens, so about 5 to 8 points; stage 3 about 1 to 2. Under the 10-point line: stage 2 goes on, within the budget ceiling (it waits whenever the allowance is above the ceiling).
