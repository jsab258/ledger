# Why Haiku refuses true sentences: research, begun 26 October 2026 (night)

His page answer of 26 October night, with the fast checker's third try: "Keep working on why Haiku refuses true sentences in parallel." Every first sentence Haiku refuses is heard at 5 s or later (SENTENCE-REPAIR-2026-10-26.md), so each false refusal is a slow turn with no safety bought.

## Questions

1. How often does the game's check refuse a true detail or sentence, and which kinds (stated or implied; person, time, place, habit; by speaker)?
2. Where in the check does the refusal come from: a specific mapped to "none" in the list step, or a specific the line does not really state?
3. Is the gold label right? (A spot check of the refused true items against their facts.)
4. Would the check's own second look (ClaimCheck.Looks = 2, Haiku at low effort on what the list refused) clear them, at what added time, and would it let an invented detail through?
5. Are any refusals caused by the facts list's wording (an item that implies something only to a reader who knows the street)?

## Data

- The 127 held details, Haiku 5.5 as the game runs it (thinking off; F:/LedgerTools/town-scratch/talk-ladder/successors/successors-run3.jsonl, read 26 October night).
- Next: the third try's enlarged held test, a few hundred whole first sentences labelled by Gemini 3.8 Flash, each through the game's check (ledger/ClaimBench sentcheck), with what the check named.

## First reading (question 1, the 127 details)

| Gold label | True details | Refused by Haiku |
|---|---|---|
| stated | 57 | 9 (16%) |
| implied | 28 | 14 (50%) |
| all true | 85 | 23 (27%) |

The check's prompt asks for "the item that states it or directly implies it" (ClaimCheck.RequestItems), yet with thinking off Haiku refuses half of what the labellers judged implied: "the dispatcher keeps things running when the office is open", "Ron's out at the rank", "the new owner's about somewhere". Unverified as yet: whether those labels are right (question 3).

## Question 4, first reading: thinking does not change it

The same 127 held details through every check setting measured on 7 October (F:/LedgerTools/town-scratch/talk-ladder/successors/successors-run1 to run4, read 26 October night):

| Setting | Invented let through, of 42 | True refused, of 85 | Implied refused, of 28 |
|---|---|---|---|
| Haiku 4.5 | 3 | 23 | 19 |
| Haiku 5.5, thinking off | 6 | 22 | 13 |
| Haiku 5.5, thinking low | 0 | 22 | 14 |
| Haiku 5.5, thinking full | 0 | 26 | 17 |
| Haiku 5.5, off, then a second look at low (as the game runs it) | 1 | 23 | 14 |
| Sonnet 5.5, low (40 details only) | 1 of 13 | 12 of 27 | 12 of 18 |

More thinking buys safety (fewer inventions through) but not fewer false refusals: every setting refuses about a quarter of the true details and half or more of the implied ones, and the larger model refuses more. So the cause is not the model's effort. The two candidates left: the check's own wording (it forbids supplying a detail from a person's role or habits, and an "implied" detail is often exactly that), or the labels (question 3: the labellers may have counted as implied what the facts only suggest). Next: read each refused implied detail beside its facts.

## Question 3, first reading: the refusals fall where people disagreed

Each of the 127 details was labelled by two people, a third breaking ties (detail-gold.jsonl, "labels"). Against the game's own check (successors-run3):

| True details | Both labellers agreed | The two disagreed |
|---|---|---|
| passed by Haiku (62) | 53 | 9 |
| refused by Haiku (23) | 4 | 19 |

So 19 of Haiku's 23 "false" refusals are details on which one of the two people also called it invented; only 4 of 85 true details (5%) are refused where both agreed they were true (d012 "June is about", d037 "books are here", d048 "the dispatcher keeps things running when the office is open", d239 "twelve o'clock"). Haiku sides with the stricter reader on arguable details, and that strictness is also what keeps inventions out (1 of 42). The enlarged test (617 sentences, the game's check on each) will show whether whole first sentences behave the same.

The four, beside their facts: "June is about" (Sheila; H11 "is still in town", P15 "Here with you now: ... June") and "the dispatcher keeps things running when the office is open" (Ron; H13 "a dispatcher on the radio and the phone") are plainly supported; "books are here" (Sheila; C1, C2, H4 imply the office's books, none says where they are) and "twelve o'clock" (Darren; only H16's café hours on Sundays give a twelve) are arguable. The 7 October runs kept only pass or refuse, not which specific the check named, so question 2 waits on the enlarged test's run, which keeps it.

## Whole first sentences (the fast checker's enlarged test, 26 October night)

The game's whole check (ClaimCheck.CheckAsync, Haiku 5.5) on 617 first sentences from the held contexts, labelled by Gemini 3.8 Flash and spot-checked (77 of 80 agreed): **96 of 309 true sentences refused (31%)**, 35 of 308 invented let through (11%), the same for all three speakers and for plain and near-miss sentences (27 to 33% refused). Median 2.4 s and three calls a sentence. Data: F:/LedgerTools/checkers/train3/haiku-verdicts.jsonl, with what the check named for each.

**Question 2, a lead from the code:** the list step clears an event only when the item it cites is a belief, memory or something they were told (B, M, W items; ClaimCheck.ParseItems). These three speakers' facts are C, H, P and K items, so every event they state goes on to the second look, one call per detail: hence three calls and 2.4 s a sentence, against 1.1 s for the list alone. The second look is where the refusals are decided. Whether H items (what the character knows happened) should count as support at the list step, as B, M and W do, is the next thing to measure: it would cut calls and time, and must be weighed against the leaks.

Read by hand (the fast checker's hand reading, LOCAL-CHECKERS-2026-10-26.md): of the 35 invented sentences Haiku passed, 18 to 23 are truly invented, among them a denial of the story's central secret ("your uncle never kept two sets of books") and two contradictions of where Mickey died and who lives above the office. Gemini's labels erred only on the strict side (12 of 44 read supported). The same strict lean will inflate the 96 refused "true" sentences by little, since Gemini called those true.

## Question 2, measured: the second look on history facts is real safety (27 October, 01:55)

The 617 held sentences through the game's whole check twice, the second time with the cast's H items counted as an event's support at the list (ClaimCheck.HistorySupports, a bench switch, off in the game; ledger/ClaimBench sentcheck --history-supports; $0.47):

| | Invented let through, of 308 | True refused, of 309 | Median | Calls, median | Slowest tenth |
|---|---|---|---|---|---|
| The game's check | 35 | 96 | 2.43 s | 3 | 3.58 s |
| H items counted at the list | **66** | 64 | 1.93 s | 2 | 3.15 s |

Faster by half a second and a third fewer false refusals, but nearly twice the inventions through: 40 newly passed, among them plain contradictions of the facts ("the cafe ... shuts its doors at eleven", "I found him stone cold up in his flat over the office", Ron "shouting at a stranger out back two nights before Mickey died"). The list step cites an H item for details the item does not give; the second look is what catches them. **The switch stays off.** The time lever, if any, is a faster second look, not a skipped one. Data: F:/LedgerTools/checkers/train3/haiku-verdicts-history.jsonl.

## The 96 true sentences refused, sorted by cause (27 October, 06:00; a helper's reading, its fresh review running)

Each of the 96 true first sentences the game's check refused, read beside its facts and the details the check named
(FALSE-REFUSALS-BY-CAUSE-2026-10-27.md; existing data, nothing spent): not a claim but listed anyway 27 (20 of them name a
place, person or number, which the code counts as a claim); a paraphrase missed 23 (7 of them "inside the office" against
"at the office"); the check misreading the sentence 14; a detail cut from its subject, so the second look cannot place it,
5; a people line that can clear only a habit, by design, 5; a reasonable inference the rules forbid, 7; a time, 3; the
label wrong, none for certain, 12 unsure. "Who runs things round here?" is refused most (18 of 35). The reading says the
list's wording could fix the misreadings and the cut details at low risk; the non-claims need a narrower rule in code, and
the paraphrases looser examples in the look, both with risk; the inferences and times are refused on purpose.

**Its fresh review (27 October, 06:05; 30 re-sorted blind, then compared): sound with fixes.** Every number and quote
checks; the conclusions follow. Fixes: bare details such as "right here in the office" and "sitting on the key" are cut
from their subject and belong with the wording fix rather than the paraphrases (the blind sort found 6 such in 30); the
naming rule in code reaches about 20 of the 27 non-claims, and sentences with two refused details need both fixed, so
nearer 55 of the 96 than the reading's 62; "held the service three weeks ago" is a forbidden inference with a time, as
the look's own example says; and "low risk" is assumed: **any wording change is measured on the invented sentences
first, against his bar** (no more invented details through than Haiku today). Next: the list's wording for the misread
and cut-off details as a bench switch, run on the 617 held sentences, when the measuring money allows.

## The wording fix measured on all 617 (27 October, afternoon; his extra $4)

ClaimCheck.WholeDetails (each detail written whole, as the line says it) against the game's check as it is, on every
held sentence. The two runs alternated sentence by sentence (ledger/ClaimBench sentcheck --ab whole;
F:/LedgerTools/checkers/train3/whole-ab.jsonl; $1.28, 3,242 calls). Gemini's labels, as before.

| | Invented let through, of 308 (per 300) | True refused, of 309 | Median check |
|---|---|---|---|
| The check as the game runs it | 40 (39.0) | 99 (32%) | 2.50 s |
| With the wording fix | 31 (30.2) | 95 (31%) | 2.46 s |

- **Its aim missed.** True sentences refused fell by 4. Where the runs disagreed, 27 true sentences passed only with the fix and 23 only without it: noise.
- **But it let fewer inventions through.** Where the runs disagreed, 14 invented sentences passed only without the fix and 5 only with it.
  - That is suggestive, not proven: a sign test gives p about 0.06.
  - The same check alone moves by about 5 between runs (35 last night, 40 today).
  - The 5 it newly passed (F:/LedgerTools/checkers/train3/whole-ab-discordant.json) include Mickey's nephew "living upstairs right now" and the cafe opening "at half past seven". So it is not cleaner in kind, only fewer.
- **Verdict: left off.** It holds his bar (no more inventions through), but the safety gain is unproven and its purpose was not met.
- **Next, with money:** a second run on the 617 would settle the safety gain (about $1.30). The rest of his $4 went to the two-copies whole-turn test, so this waits for his word or a later budget.
