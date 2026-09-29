# What is open when, through the real engine and check, 29 September 2026

Town list 6bo. Eight questions a friend asks about the street's shops ("Is Rita's
open now?", "What time does the cafe shut?", "Can I get a paper on a Sunday?",
"Is the cab office open all night?", ...) to each of Sheila, Ron and Darren, as a
first line, on a Wednesday at half past two (the half day: Rita's and Hal's
shut; the fish shop too until round 6, when its half day came out, since
fishmongers were exempt), through ConversationEngine and its claim check, without the
street's hours and with them (`dotnet run --project ledger/ClaimBench -c Release
-- hours`; the rows on drive F, F:\town-bench for round 1 and its folders hours2 to hours8). Each answer read
by eye against the cast file.

## What came back, with the hours (24 answers a round)

| round | right | wrong | no answer | cost |
|---|---|---|---|---|
| without the hours (each round) | 0 to 2 | about 1 ("Should be", of Rita's on her half day) | 21 to 23 | in the rounds below |
| 1. the hours as one of the people lines (P) | 0 | 0 | 24: every true hour refused as an invented time | $1.15 |
| 2. and the check told a shop's hours are a habit | 9 | 1 (Rita's "half one") | 14 | $1.11 |
| 3. the hours as their own item (O), clearing a detail on the list's word | 16 | 4 ("half eight" for eight, Rita's "half five on Wednesdays") | 4 | $0.81 |
| 4. O details sent to the second look | 11 | 1 | 12: true hours refused | $0.98 |
| 5. each shop's hours said in full | 14 | 1 (Ron: the cafe shuts at ten on Sundays, not twelve) | 9, of which four refused a wrong draft | $0.99 |
| 6. a shop's hours always listed and always looked at twice | 18 | 1 (Sheila: the laundry shuts at one on Wednesdays) | 5, of which one refused a wrong draft | $0.91 |
| 7. only talk of opening or shutting at a time counts as hours | 15 | 1 (Darren: "half an hour late" for Rita's, shut an hour and a half before) | 8, of which two refused a wrong draft | $0.98 |
| **8. hours of any kind cleared from the hours item alone (the kept rule differs, below)** | **15** | **2** (Darren: the laundry opens at "half eight", which the same check refused in Ron's mouth; Rita's shut "about an hour" ago, an hour and a half) | **7**, of which one refused a wrong draft | $0.98 |

Round 4's refusals were the second look not reading the short form ("Hal's, ten
till six, Wednesdays till one" did not support "Hal's shuts at one on
Wednesdays"). One probe of nine details (`-- hourslook`, $0.02) found it; said in
full ("on Wednesdays it shuts at one, shut on Sundays"), the probe cleared all five
true details and refused all four false ones, and round 5 followed.

Rounds 6 and 7 answer the independent check of round 5 and its recheck: the first pass had been told
never to list a habit an item describes, so a wrong hour it took for the hours
item's was never looked at twice (Ron's Sunday close passed with nothing
flagged), and a habit cited to the card was cleared on the card's word. Now a
shop's hours are always listed, given as the street or now they are read as a
habit, never cleared on the card's word, and a full answer about every shop is
looked at rather than refused for its length. Round 7 narrowed what counts as
hours (a word of opening or shutting and a word of when, so "the door's open"
and "the till" are left alone) and checked it against the hours, never against
what they know of the street's people. After it, a third check found hours
given as the speaker's own ("we open at eight"), a denial or an event cited to
a memory still passed on the list's word, and "they close at eleven" was not
read as hours: round 8 sent every kind to a second look that cleared a shop's
hours from the hours item alone. Its check found that too strict (a witness's
"he shut the boot at ten to ten", cited to his memory, was refused; so were
"I opened the post this morning" and "it's closing in") and still leaky ("I'm
shutting at five", "nine till six", "an hour ago" not read as hours). As kept:
a shop's hours given as a habit, the street, now, a denial or an event are
never cleared on the list's word, and the second look may clear them from
anything but the people lines, as for any event; the speaker's own doings, the
weather and the talk itself are left as they were. The bench's speakers hold
no memory of hours, so for them it reads as round 8 did; not measured again. Rounds 6 to 8 differ by about what
the same code gives from run to run; the second look itself is not steady ("half
eight" for the laundry refused in one mouth and passed in another). Rounds 6 and 7 differ by about
what the same code gives from run to run.

The change did not open a hole or silence small talk: the twelve inventions
hidden in small talk were all still caught (`-- disguise`, $0.06, before round
6), and a newcomer's twenty first questions to each of the three gave "that's
all I know" 38 times in 60 after round 6 and 37 after round 8 (`-- firsts`,
$1.64 and $1.51), inside the 35 to 41 the same code gave before.

## What is left

About one true hour in four or five is still refused on its second look
(Darren's "ten at night" of the cafe, Ron's "shuts at four" of the market), and
one or two answers in 24 pass wrong. Eight rounds, two probes and the three
checks: $11.16.
