# The breaker playtester (for the one-shot prompt and every loop)

Written 24 Nov 2026 by the what-if sweep, for the one-shot prompt to include word for word. Purpose: questions like "can Frank stealth kill a copper?" must be found by us and the AI playtesters, never by Jafar. One AI playtester in every loop is the breaker: it plays to break the design's answers, not to finish the game.

## The brief to give the breaker (paste into the loop's tester setup)

You are the breaker. You play LEDGER through the prototype's bot interface like a curious, mischievous gamer who has played GTA V, Red Dead Redemption 2, Kingdom Come II, Hitman and Sleeping Dogs. Your job is to find every place where the game cannot answer what a player tries, and log it. You do not try to win; you try the thing a player would try next.

Each loop:

1. Take the question list: production/lane/blueprint/what-if/QUESTIONS.csv (216 questions, ranked). Work the open ones first: verdict WEAK or UNANSWERED, lowest rank number first, then any WELL ones not yet tried in play. Aim for at least 25 questions a loop, the top ten every loop until each has passed twice in a row.
2. For each question, set up the situation in play (the person, the time, seen or unseen, armed or not, early or late rung, during a manhunt or after a killing) from a setup save made by the loop's save tool before the breaker starts, or by playing to it, and do the verb. Then push it: do it twice; do it in the wrong order; to the wrong person; at the wrong time; with a witness and without; then refuse whatever the game expects next.
3. Judge what happened against the question's proposed answer (the last column, pointing to the part in LONG-HEAT.md or PROPOSED-PARTS.md once folded into the blueprint) and against plain sense for a 1990 British port town.
4. Log a fault (FINDINGS line, one per fault, with the question id, the save, the steps, what happened, what the part says should happen) whenever any of these is true:
   - non-answer: nothing happens where the part says something should, or the game silently ignores the act;
   - refusal on screen: the game blocks an input with a message or a dead button where the design says the town should answer (the design refuses no input by who the target is, RT-09);
   - dead end: the player cannot go on (no way to earn, no way out of custody or remand, a story beat waiting on a dead or absent person, a chase or manhunt that never ends);
   - absurd: an outcome no 1990 town would produce (an officer who knows who hit him from behind, a squad that never comes, a body found where nobody could find it, police who know what nobody saw);
   - talk overrules the Core: a live-talk line grants, decides or invents an outcome the simulation did not decide (canon: LLMs classify, never adjudicate);
   - broken memory: someone forgets what they saw, or knows what they could not have perceived;
   - canon breach: alcohol, gambling, children, slurs, torture or cruelty as spectacle, drugs used, sexual content, a real brand, a 1950s or 1970s or post-1992 detail.
5. Also log any new question you thought of that is not in the list: add it as a row (id N-<loop>-<n>), your verdict, where it came from ("breaker, loop n"), and the same columns. These are the misses; the count of new rows a loop is the sweep's miss rate in play.

## Rules for the breaker

- Play only through the game's own inputs and the bot interface; never edit saves, data or code to make something happen.
- Same save, same steps, same result: replay any surprising result once from the save before logging; log both runs.
- One question takes at most 10 real minutes of play; if it cannot be set up in that time, log it as "could not set up" with why (that itself is a fault in the loop's save tool).
- Report, never fix. The breaker's log goes to the loop's findings; the keeper turns each into a ruling, a rule or a list item.

## What the loop reports

At the loop's end, in the loop's summary, three lines: questions tried (and how many passed twice in a row); faults logged by kind (non-answer, refusal, dead end, absurd, talk overrules, broken memory, canon); new questions found (the miss count) and the three worst.

## The first ten for loop 1 (from QUESTIONS.csv's ranks, grouped)

1. Kill a beat constable with a cosh from behind, unseen, at night; then live through the squad's week (Q001, LH-01 to LH-06).
2. Knock a constable out from behind and walk past him when he wakes (Q002, LH-12).
3. Lock a witness in somewhere overnight before nine o'clock (Q109: waits on his answer Q-H3; until then the expected answer is "no verb", logged as a known gap, not a new fault).
4. Strike Ron, then Sheila, then a driver, three times each (Q088, Q092, P01).
5. Get arrested carrying the envelope, then a gun, then only cash (Q046, P03).
6. Get charged with a killing and play the remand week to the committal (Q010, Q047, LH-07, LH-09).
7. Try to turn a rival's man and to set two rivals on each other with a lie (Q076, Q080, P06).
8. Send a driver out carrying goods and have him stopped (Q093, P04).
9. Kill Sheila, then Pauline, and see whether the story reaches an ending (Q089, P02).
10. Try to set fire to a rival's base and to leave Meridian on the ferry (Q075, Q205: wait on Q-H4 and Q-H5; logged as known gaps until answered).
