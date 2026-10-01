# Independent review of 1 October: are the 30 September faults really fixed?

An independent review, 1 October 2026, of the builder's and the town's fixes to the faults found on 30 September, now in the game. It was done by reading the changes and by running the game's own code on small cases. Four readers who had not seen the fixing work took one area each: the route's logic, time, saves and the port. Nothing was fixed here.

The game's own tests pass here: 38 of 38. As on 30 September, that clears nothing on its own. Most of what is below lives in the game's own wiring, which no test reaches.

The details, with the places in the code, are in FAULTS.md. What each proof printed is in RESULTS.md.

"Proved" below means a small program ran the game's own code and got that result. The rest is from reading, and says so.

## The 30 September faults

**Fixed, and proved by running:**
- The smash's witnesses are now the people really there that hour, from where they stand, in that hour's light.
- Hearing the glass go is no longer filed as a story about him, and no debug words reach the town.
- Somebody who has met him can now recognise him and report him, and the constable comes.
- A shape or a noise no longer counts as "it was him".
- DS Ellis asks only people on Quay Street.
- Rita finds her own window in her own words.
- Sheila asks her question on Monday if Sunday morning was missed.
- A deed after midnight is reported that morning.
- Ada's tea treats a late guest who stays as staying.
- After a Continue, the conversations come back.
- A reload at any point of the week gives the same week as playing straight through. That was run at 311 points.
- The four faults written into the test tables are gone from them.

**Fixed from reading:**
- After a Continue, people can still see the smash.
- Walking up to Darren afterwards no longer files a sighting.
- The witness lines lost their wrong times and their pub.
- His "no" to Ron is kept across one in the morning, and when he walks off.

**Not fully fixed:**
1. **The witness who saw him is told she knows nothing about it, at every line.** High, proved. The deed's new name reached everything but the evidence sent with each line he says. This one was already wrong on 30 September and that review missed it too.
2. **The wait can still say "DS Ellis is on Quay Street, asking after you" when she is not.** Medium, proved. On a morning when the town's talk only gets loud enough after nine, she comes the next day.
3. **His no, and a night away, still reach the man at the landing late.** Low.
4. **A few small save items remain.** Low. Among them, Ron's question "tell them no?" and Sheila's question are forgotten across a Continue.

## What the fixes opened

1. **Whoever recognises him calls him "Nowak", though nobody has been told his name, and the town passes it on.** High, proved. Recognition was out of reach before today's fix, so the witness lines that say his surname were never used. Canon says the town calls him "the new owner" until it knows his name.
2. **A threat never stops a witness reporting him.** Medium, proved. Jafar's ruling of 1 October says it should: "talks them round (keep it quiet, a threat)".
3. **Nobody he can talk to can be won over, and Mickey's own two report him.** Medium, proved in part. This one is Jafar's to rule on. Only Ada's tea moves anybody. Sheila trusting him does not count. Canon calls Ron and Sheila Mickey's inherited loyalists, yet Ron recognising him at the window has him charged two days later.
4. **Ada invites him to tea in the hour he is arrested.** Medium, proved.
5. **How well the three know his face is worked out two ways.** Medium. For witnessing it comes from his meetings. For their looks and remarks on the street it is still fixed: Ron counts as knowing him from the first minute, and Darren never does.
6. **The route's rows where Ada sees the window cannot happen in play.** Medium for the route's acceptance. Behind her window she can never see Rita's glass well enough.
7. **Low items:**
   - People on Rita's step with no body "were there" but "never saw who did it".
   - Rita hearing her own window remembers it as Rita's.
   - A failed or unfinished talk save still loses every conversation.
   - Sheila can put her question at the fish market.
   - Two late replies in a row lose the first.
   - A short late visit to Ada's tea counts for more than a long early one.
   - Where people stand is not saved.
   - Saves from older builds are always taken.

## The tests

The two versions of the town agree on every one of the 57,864 rows the tests compare, and on a full dump of the week's town. But much of the new code is never reached by those rows. The port reader broke twelve new lines in the C++ one at a time, and the tests still passed.

## What still needs the game

Six short runs of the packaged game, listed at the end of FAULTS.md. They settle what only the real street can show. Chiefly:
- whether a witness's suspicion is wiped in play;
- whether "Nowak" spreads;
- which way the three really face;
- whether a quit straight after a reply loses the talk.
