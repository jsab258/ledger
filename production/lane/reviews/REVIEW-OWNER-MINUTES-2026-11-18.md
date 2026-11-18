# Review: owner minutes a week (draft of 18 November 2026)

Fresh reviewer, 18 November 2026. Verdict: PASS WITH FIXES.

## Checked and confirmed

- tools/token_measures.py ask_minutes(day): reads items.json and archive.json, joins each item to its stored answer under production/approvals/answers/1VZHkCBAHdw8HBdNHrByL8 by id, converts "at" to Swiss time, returns minutes from "added" to the answer. It is waiting time, and the overview prints it as measure 5, "Cycle time". The draft's reading is right.
- tools/needs_you_page.py: --action-week lists ACTION items since a date from both files; the batch check counts only open items' distinct "added" times. The draft's reading is right.
- Week 9 to 15 November, recomputed from items.json and archive.json: 49 items, 7,253 words over the named fields, median 116, 36.3 minutes at 200 a minute; distinct "added" times 12 on 9 Nov and 10 on 11 Nov; 46 stored answers in the week by Swiss time (no answer stored twice), 7.7 minutes at 10 seconds each. All match.
- Spec arithmetic (1.17 minutes; 10 minutes for a 10-step ACTION) is right.
- Both web sources found by search at the cited addresses (BPS Research Digest on Brysbaert; Nielsen Norman Group on mobile comprehension). Their figures were not reread in full in this review.
- Plain words, third person, no em-dashes or italics, content rule kept, nothing recommended that needs a licence, no ask of him outside scope: the target is offered as his choice, to be batched by the main session.

## Findings

1. Fixed. Advisor rows 75 and 177 were cited "in RULINGS"; RULINGS names neither. Now cited to production/research/ai-video-motion/SOLVE-CPU-ROUTE-2026-11-10.md (advisor 75) and tools/needs_you_page.py (advisor 177, the 16 Nov audit). The "about 100 a week" stays marked unverified.
2. Fixed. The sample Monday line said "61 estimated" with "chosen 17", which contradicts the draft's own estimate of over three hours of advisor time. Now "44 measured" with chosen marked n.m.; the note says which numbers are real.
3. Fixed. Option B said 30 minutes was "about two thirds below last week's estimate"; 30 against 44 asked minutes is about a third. Corrected.
4. Fixed. "His rulings allow one page a day": there are no daily pages (RULINGS 2 Nov, one standing page). Reworded to one standing page, items in up to two batches a day (RULINGS 2 and 8 Nov).
5. Open. "Hands 0" last week partly reflects that the ACTION tag only began on 17 Nov (RULINGS 2 Nov line, 17 Nov addition); none of the 49 items carry a tag or his_hands. The audit should say hands were not tagged before 17 Nov, not that there were none.
6. Open. The 21 of 36 asks figure and the blind plans' 10 and 15 minutes come from the brief, not from repository files; already marked unverified, fine to keep.
7. Open. The advisor estimate of 2 minutes a row may dominate the total; the first real count should come from the page database's "advisor" collection before the target is shown to him.

## For the main session

Merge the draft as fixed. Put options A to C on his page as one decision in the next batch, B recommended. When building owner_minutes, read the advisor row count from the database and label pre-17 Nov hands as untagged.
