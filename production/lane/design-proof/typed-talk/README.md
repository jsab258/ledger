# RT14 typed-talk test set (2026-11-21)

300 typed lines for checking the typed-talk reader. One JSON object per line in RT14-SET-2026-11-21.jsonl. Each line has exactly one correct act.

## Fields

id, text, phrasing, act, amount_gbp, thing, when, lie, context, hard, note.

- Offers carry an amount in pounds or a non-money thing.
- Promises carry what and when.
- A claim is marked as a lie (true or false) only when its context field settles it. Otherwise lie is null.
- hard marks tricky lines (sarcasm, polite threats, offers asked as questions, promises dressed as claims, "yeah, no"). The note says why.

## Counts by act

- question 32
- agree 30
- refuse 32
- offer 33
- threat 32
- promise 32
- claim 34 (10 lies, 10 true, 14 untested)
- insult 30
- small_talk 25
- leave 20

## Counts by phrasing

- period 122
- modern 88
- terse 44
- misspelt 46

## Other counts

- hard lines: 65

## Content

Set in the Hook, October 1990. No drink, betting, children, slurs, real names or brands, or anything after 1992. Lines are shuffled, so order gives nothing away.

## Checked 21 Nov 2026 (design proof run 3)

- Content rule: keyword scan for drink, pubs, betting, children, school, mobiles and the internet: none found; 18 random lines read by hand: clean.
- A second labeller (fresh, blind to the labels) labelled all 300: acts agreed on 295 (98.3%, kappa 0.98); hard lines 63 of 65; amounts 28 of 28; lies 20 of 20. Of the five disagreements, one label was wrong and changed (167, sarcasm is a refusal); three now allow either reading (field also_ok); one kept (7). Figures in agreement-2026-11-21.json.
- The bar for the reader (row RT-14): its act matches the label or an also_ok on at least 95% of all lines and 90% of hard lines, a little under the two labellers' own agreement; every amount read exactly; every offer, threat, promise and lie written to the hearer's memory.
- Limit: such high agreement says the lines are clear. Harder, stranger lines from real players are the job of the abuse and off-limits set (RT-15) and of reported lines after release.
