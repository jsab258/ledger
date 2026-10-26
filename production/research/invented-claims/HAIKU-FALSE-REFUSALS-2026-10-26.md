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
