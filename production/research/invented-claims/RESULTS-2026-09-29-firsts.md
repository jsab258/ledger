# A newcomer's first questions, through the real engine and check, 29 September 2026

Town list 6be, from the fourth sweep. With no instructions a friend's first lines go
to the people in front of him, and every bench so far asked about a night's events
or small talk. Twenty such questions ("Who are you?", "How did Mickey die?", "What's
behind that door?", "Where do I sleep?", ...) to each of Sheila, Ron and Darren, each
as a first line to them, 10:00 on the first day, through ConversationEngine and its
claim check, with who they know on the street as the talk helper gives it
(`dotnet run --project ledger/ClaimBench -c Release -- firsts`, bench/firsts.jsonl).

## What came back

| run | "that's all I know" | cost |
|---|---|---|
| before | 46/60 (Sheila 16, Ron 14, Darren 16) | $1.60 |
| **as kept: their own name known** | **35/60, and 41/60 run again** | $1.61, $1.60 |
| split who-is-who, first version (failed its review) | 38/60, 32/60 | $1.53, $1.48 |
| split who-is-who, second version (failed its review) | 40/60 | $1.62 |

The same code gave 35 and 41, so a run's generation varies by six or so either way
and one run of 46 before is not a precise baseline; what is sure is that "Who are
you?" now answers with the speaker's name (Sheila and Ron in the last run; Darren's
answer fell back for other details it invented). No reply was a brush-off or a
refusal. bench/firsts.jsonl is the last run, as kept.

## What was kept: their own name

Their own name was in no item the check reads (the card's heading is in no
section), so "Who are you?" answered "Sheila Dunn" fell back every time. It is now a
card item, "Their own name is Sheila Dunn.", left out when a card is lent to
somebody else. It supports the speaker's name and nothing else, so it cannot let an
invention through.

## What was tried and dropped: who the street's people are

What a character knows of the street's people is one P item a line, name and usual
place together, and a P item may clear only a habit (6ad: "usually at the quay" gave
"Darren was at the quay"). That also refuses "June, Mickey's daughter" and "Rita's
pawn shop" to a newcomer. Two designs split who somebody is from where they usually
are so the first could clear more; the independent check broke both:

1. Who-is-who items that could clear any detail: a description says what somebody
   habitually does ("Ron Kirby, who keeps Mickey's door and the rank"), so "Ron was
   on Mickey's door when the window went" passed; and "who is with them now" cleared
   "Darren was with me when the window went".
2. A new kind, "who" (a name, work, family), the only kind the who-is-who items
   could clear, with a word list to catch deeds and times: "Ron minding Mickey's
   door, Darren doing his rounds", said of the night the window went, is naturally
   "who" (minding the door is Ron's work), and no word list separates a person's
   work from what they were doing that night.

Both attacks are now tests that must stay refused (CoreTests). The held-back bench
measured the first design at 95/108 invented turns caught and the second at 98/108
(clean turns flagged 45/132 and 40/132, against 98/108 and 43/132 before); the
`again` mode, added for this, re-runs chosen turns one try at a time with the items
as built now and as before (the same request sent many at once came back alike, so
those were not separate tries).

Found on the way, older than this item and put on the list (6bf): a detail the list
calls "now" that names nobody is dropped without a look, so "he was here with me
when the window went", labelled now, would pass; and a detail's kind is kept by its
words, so the same words given twice with different kinds take the last one's.

## What is left: facts nobody has written

Most of what still falls back answers with something the town has never been told,
and the check is right to stop it:

| what they needed | answers |
|---|---|
| how Mickey died, where, who found him | 3 |
| what's behind the door (Mickey's back room, the yard, Rita's back room) | 3 |
| where to eat: the cafe, where it is, what it does | 3 |
| the business's money: rent, takings, what is owed | 3 |
| the drivers: how many cabs, day and night | 2 |
| the funeral: when, who came, where | 2 |
| what Mickey left: a will, papers | 2 |
| what Mickey was like, in plain facts | 2 |
| Darren's trade, what he "picks up" | 3 |
| Ron's years at the door | 2 |
| where Tom sleeps | 1 |
| where the office is from Rita's | 1 |

The rest is who the street's people are, refused on purpose as above. These facts
are canon, so they go to Jafar with the first hour he approved (the 29 September
page: how Mickey died, and the street's plain facts); once written, they are facts
every character knows, which the check reads like a card's.

Cost of the item: $9.44 in six first-question runs, $3.43 in two runs of the
held-back half, $1.60 in traces and re-runs; about $14.50, against the $1 the item named.
