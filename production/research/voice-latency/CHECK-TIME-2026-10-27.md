# The check's own time (27 October 2026, night)

His speech order of 25 October, item 4, and his ruling of the 26th: the 2-second bar is judged on a newcomer's real
questions. The one-sentence rewrite (SENTENCE-REPAIR-2026-10-26.md, last section) left one lever: the time of a check.

## Questions

1. Where does a check's time go: the service's uneven pace, or the check's own steps?
2. Can the second look start sooner without changing a single verdict?
3. Would a second copy of a slow call (a hedged request) cut the slow tail, and at what risk to the verdicts?

## 1. Where the time goes (our own records, nothing spent)

The game's whole check (ClaimCheck.CheckAsync on Haiku 5.5) on the 617 first sentences of the checker's held test,
26 October night (F:/LedgerTools/checkers/train3/haiku-verdicts.jsonl), by how many calls it made:

| Outcome | Calls | Sentences | Median | Slowest tenth from |
|---|---|---|---|---|
| passed | 1 (the list cleared it) | 104 | 1.06 s | 1.60 s |
| passed | 2 | 70 | 2.48 s | 3.49 s |
| passed | 3 | 59 | 2.78 s | 3.84 s |
| passed | 4 to 5 | 15 | 3.03 s | 4.43 s |
| refused | 2 | 103 | 2.25 s | 3.30 s |
| refused | 3 | 153 | 2.52 s | 3.42 s |
| refused | 4 to 5 | 110 | 2.84 s | 3.85 s |

- (Three refused sentences that made 6 or more calls are left out.) A sentence the list clears outright is checked in
  about 1.1 s. **Anything the list flags waits for a second look,
  and the second look starts only once the whole list is written:** 2.3 to 2.8 s, every refusal and 144 of the 248
  sentences that passed (213 of the 248 true by the labels).
- This corrects the note of 26 October evening ("the checks of 2 to 4 s in the runs are the service's own varying
  wait"): that measured the list call alone, on sentences that had passed. A check of 2 to 4 s is mostly two calls
  one after the other, the list and then the look, each with the service's uneven wait (section 2 shows how uneven).

## 2. Starting each second look as its detail is written (ClaimCheck.EarlyLooks)

Method: the list is streamed; each time an entry closes, the answer so far is read the way the finished one is
(ClaimCheck.Salvaged, the same reading the check already uses for an answer cut off at its cap) and each flagged
detail that is not stated word for word gets its look at once. A look asks about its detail alone, with everything
they know, so it is the very request the finished list would make. The finished answer is then read exactly as
before; a look started early that it does not need is waited for and costed, never read, or stopped when the list's
verdict stands without looks (more than eight flagged). A broken stream is asked for again whole, the looks already
started kept.

Checks (CoreTests, TestEarlyLooks, 12 checks, all pass): the flagged detail's look is asked for while the list is
still being written; the verdict and the number of calls are the same with the switch on and off; an early look that
supports the detail clears it; a broken stream; a line made up wholesale (its early looks stopped and cancelled); a
client that cannot stream runs as before. On the test's timings (a 400 ms list, a 200 ms look) the check took 409 ms
on and 621 ms off.

**The measurement** (27 October, 03:10 to 03:50): every third sentence of the held test, 206, each checked twice by
the game's whole check on Haiku 5.5, once with the switch and once without, the order alternating sentence by sentence
(ClaimBench `sentcheck --ab-early --every 3`; F:/LedgerTools/town-scratch/slow-replies/early-looks/ab.jsonl, scored by
tools/voice-live/early_looks_ab.py; $0.42):

| Sentences | Off: median / slowest tenth from | On: median / slowest tenth from | Saved, median per sentence |
|---|---|---|---|
| all 206 | 2.24 / 3.58 s | 2.27 / 3.37 s | 0.04 s |
| the 170 that needed a look | 2.50 / 3.76 s | 2.43 / 3.51 s | 0.11 s |
| the 36 the list cleared | 1.05 / 1.89 s | 1.15 / 2.27 s | -0.08 s |

- **Verdicts unchanged:** 189 of 206 the same both ways, the rest split 9 and 8; invented sentences passed 8 of 108
  both ways, true ones 72 and 71 of 98. Two runs of the switch-off check a night apart differ on 31 of the 206 (15%),
  the check's own run-to-run spread.
- **The saving is too small to matter:** the list is written fast once it starts, so its flagged entries close only
  a few tenths before its end; nearly all of its time is the wait before its first word. The same sentence checked
  twice a few seconds apart often differs by a second or more (3.76 against 1.09 s; 0.84 against 3.94 s): the
  service's own pace, not the order of the steps, decides how long a check takes.
- **Left off,** as a bench switch beside the others; the lever is the slow call itself (section 3).

## 3. A second copy of a slow look (hedged requests)

Source (read 27 October 2026, the hedged and tied request sections and the caveat that follows them; the rest of the
article not read): Jeffrey Dean and Luiz André Barroso, "The Tail at Scale", Communications of the ACM 56(2), February
2013, https://www.barroso.org/publications/TheTailAtScale.pdf (the ACM page itself answered 403).

- A hedged request sends the same request again after a short delay and uses whichever answer comes first, cancelling
  the rest. Sending the second copy only once the first has been out longer than the 95th-percentile time for that
  kind of request "limits the additional load to approximately 5%" while "substantially shortening the latency tail".
- Their example: 1,000 keys read across 100 servers; a hedge after 10 ms took the 99.9th percentile from 1,800 ms to
  74 ms, with 2% more requests.
- Tied requests (each copy cancels the other when it starts work) cut a file system's read times by 16 to 38% at
  every percentile, under 1% extra disk use.
- The caveat: these techniques work "only when the phenomena that causes variability does not tend to simultaneously
  affect multiple request replicas".

For us: the replicas are hidden behind one service, so whether a slow look is slow for both of two copies is the
question to measure first (ClaimBench `lookpairs`: each refused detail's look sent twice at the same moment). And the
copy to keep must be chosen before its content is seen: a refusing answer is longer, so taking whichever copy
*finishes* first would favour passes and let more inventions through.

**The pairs** (27 October, 03:40 to 03:47): the first 70 sentences of the A/B run; each sentence's list streamed twice
at the same moment, then each detail the run refused had its look streamed twice at the same moment; each copy's first
words and end timed (ClaimBench `lookpairs`; F:/LedgerTools/town-scratch/slow-replies/early-looks/pairs.jsonl, scored
by tools/voice-live/hedge_pairs.py; $0.11). A hedge sent after a delay is simulated as the second copy starting that
much later; the copy kept is the one whose first words come first.

| Call | One copy: end median / slowest tenth from | Copies slow together (rank correlation of first words) | Two at once, first to answer kept | Second copy only after the 75th percentile (16 to 24% sent) |
|---|---|---|---|---|
| the list (70) | 1.08 / 1.79 s | 0.22 (both in the slowest tenth: 1.4% of pairs, 0.2% if independent) | 1.00 / 1.21 s | 1.04 / 1.50 s |
| a look (71) | 0.98 / 1.86 s | 0.63 (4.2%, 1.3% if independent) | 0.87 / 1.41 s | 0.95 / 1.86 s |
| the whole check of a sentence with a refused detail (47): the list, then its looks side by side | 2.32 / 3.38 s | | 2.09 / 2.73 s | 2.32 / 3.33 s |

- **The paper's delayed hedge does not carry over:** its 10 ms delay was a sliver of its slow tail; here a copy sent
  late needs its own 0.6 to 0.8 s before its first word, so it rarely overtakes the first.
- **Two copies at once, the first to answer kept, cuts the slow tail by about 0.6 s on a check that needs a look,**
  and its median by about 0.2 s. The list's slowness is mostly not shared between copies; a look's is more so (both
  copies think about the same detail before answering), so it gains less.
- **Verdicts:** the two copies of a look agreed on 70 of 71; the one disagreement is too few to show a lean. The copy
  is chosen at its first words, before its verdict is written, but a look thinks before writing, so a lean through
  thinking time cannot be ruled out by design; it is measured on the real path before any use.
- **Cost:** every check call twice. At Haiku 5.5's price ($0.10 a million tokens read, about 4,300 a call) that is
  about $0.0004 more a call, roughly a tenth of a cent a turn; the copy stopped early is billed for what it read.
## 4. Two copies at once, in the check itself (ClaimCheck.TwoCopies)

Method: every call of the check (the list, each look) is streamed twice at once; the copy whose first words come first
is read and the other stopped, its tokens added to the kept answer's for the cost; a copy that fails leaves the other;
the kept copy breaking after its first words is asked for again whole; both failing fails as one would. Checks
(CoreTests, TestTwoCopies, 7 checks, all pass), the one that matters most: the copy that starts first is kept even when
the other ends first, so a refusal's longer answer stands against a quicker pass.

**The A/B** (27 October, 04:00 to 04:09): the same sentences as section 2, each checked with the switch and without,
alternating (`sentcheck --ab two --every 3`; F:/LedgerTools/town-scratch/slow-replies/two-copies/ab.jsonl). It stopped
at its $0.80 cap after 119 of the 206. That cap was the budget counter's, not the bill: it kept every stopped
copy at its worst case (the fresh review below); the run really cost about $0.24 to $0.36.

| Sentences | One copy: median / slowest tenth from | Two copies: median / slowest tenth from | Saved, median per sentence |
|---|---|---|---|
| all 119 | 2.22 / 3.80 s | 2.06 / 2.93 s | 0.25 s |
| the 98 that needed a look | 2.36 / 3.95 s | 2.12 / 2.95 s | 0.34 s |
| the 21 the list cleared | 1.06 / 1.73 s | 1.05 / 2.21 s | 0.03 s |

- **A second off the slowest tenth of checks that need a look,** a quarter of a second off their median.
- **Verdicts:** 100 of 119 the same; invented sentences passed 10 of 63 with one copy and 7 with two, true ones 35 and
  33 of 56. No sign of more inventions getting through, but 63 sentences cannot rule out up to about 3 more (the fresh
  review: 6 passed only with one copy, 3 only with two; p about 0.5), and fewer true passes would mean more false
  refusals, not a gain.
- **This run raced on first words,** which for a look come after its thinking: the copy kept was the one that thought
  least, a route to a lean the review named. Section 5 replaces it.

## The fresh review (27 October, 04:20 to 04:30): sound with fixes

A fresh reviewer re-ran every scorer and the tests and read the code and the source. Every number in sections 2 to 4
re-ran; section 1's small slips are corrected above. Its fixes:

1. **The cost was the counter's, not the bill.** BudgetedClient reserved each call's worst case and never settled a
   stream stopped on purpose, so every stopped copy stayed counted at its dearest (about $0.0025 for a look); the bench's
   call log never counted stopped copies at all. The two-copies run's real use, from its own token counts, is about
   $0.24 to $0.36, and an extra copy costs about $0.0004 a call, as section 3 first said. The same fault has charged
   every first draft the game stops after a refused first sentence at its worst case against the friends' evening's
   cap. **Fixed:** a stopped stream is settled at what it used, its thinking now counted in what it used
   (BudgetedClient, AnthropicClient), and the bench counts stopped copies (KeyRuns.Counted).
2. **"Nothing more invented gets through" overstated:** corrected in section 4.
3. **The bias route:** a look thinks before writing, so racing on first words keeps the copy that thought least, and
   its verdict follows its first words by about 61 ms. **Fixed by racing on the model's beginning** (section 5).
4. **Both copies breaking before any words threw with no retry,** where the plain call retries three times; in the
   whole-reply check a throw lets the line be said unchecked. **Fixed:** a stream that broke is asked for again whole.
5. **The kept answer's cost missed the stopped copy's thinking and a broken copy's prompt. Fixed** (a broken copy is
   counted at the kept answer's prompt).
6. **The source's warning left out:** Dean and Barroso say naive hedging "add[s] unacceptable additional load", and
   every call twice is the naive form; their tied requests cancel when work starts. Here the load is a doubling of a
   cheap call's requests; whether the service's rate limits allow it on a busy evening is not checked.

Not checked by the review: Haiku 5.5's real price beyond the repository's rate card, how a stopped stream is billed, and
rate limits under doubled traffic.

## 5. The race on the model's beginning (ClaimCheck.TwoCopies as it now stands)

Method: the stream reports, once, the moment the model takes a copy up, its thinking included (the first content block,
IStartingLlmClient); the copy begun first is kept and the other stopped at that moment, before either has a thought or
a word of its answer, so the choice cannot depend on what either says. A client that cannot report it gets one plain
call. Checks (TestTwoCopies, now 10 checks): a copy begun first but writing and ending last is kept against one that
writes and ends first; both copies breaking before either began are asked for again whole; a client without the signal
makes one plain call; a stopped stream is settled at what it used. All 5,115 CoreTests checks pass.

**The pairs again,** on 40 sentences not used before (rows 71 to 110 of section 2's run; `lookpairs`, each copy's
beginning now kept; F:/LedgerTools/town-scratch/slow-replies/two-copies/pairs-begin.jsonl; $0.06, counted right):

| Call | One copy: begins (median) | One copy: end median / slowest tenth from | The two copies' beginnings, rank correlation | Two at once, the one begun first kept |
|---|---|---|---|---|
| the list (40) | 0.76 s (no thinking: it writes as it begins) | 1.10 / 1.67 s | 0.26 | 0.99 / 1.22 s |
| a look (32) | 0.58 s, then a median 0.27 s of thinking | 0.92 / 1.79 s | 0.01 | 0.88 / 1.33 s |
| the whole check of a sentence with a refused detail (25) | | 2.24 / 3.23 s | | 1.98 / 2.69 s |

- **The wait before the model begins is not shared between copies at all** (0.01 for a look); the thinking is (first
  words 0.44). Racing on the beginning gets the whole saving, and the same as racing on first words did.
- The copies of a look agreed on all 32.
- **Cost:** about $0.0004 more a call (the stopped copy's prompt, if it is billed in full); with some 4.7 check calls a
  turn, about $0.002 a turn, roughly $0.30 on a 150-turn friends' evening. An estimate; not measured in play.
- **Not yet measured:** whole turns on the real path (the voice heard), a larger verdict test of this version, and the
  service's rate limits under doubled traffic. A money change in the game: his yes before it is switched on.

**The verdict test of this version** (27 October, 04:40 to 04:55): the 87 sentences the first A/B never reached, each
checked with two copies (raced on the model's beginning) and without, alternating; the counter stopped it at 61
(F:/LedgerTools/town-scratch/slow-replies/two-copies/ab-begin.jsonl).

| Sentences | One copy: median / slowest tenth from | Two copies: median / slowest tenth from | Saved, median per sentence |
|---|---|---|---|
| all 61 | 2.35 / 4.04 s | 2.17 / 3.20 s | 0.29 s |
| the 46 that needed a look | 2.65 / 4.21 s | 2.34 / 3.35 s | 0.42 s |

- **Verdicts:** 52 of 61 the same; invented sentences passed 4 and 4 of 29; true ones 27 with one copy and 22 with two
  of 32 (6 passed only with one copy, 1 only with two).
- **Over both A/B runs, 180 sentences:** one copy passed what two copies refused 19 times, the reverse 9 (true sentences
  12 and 5, invented 7 and 4), where the plain switch of section 2 split 9 and 8. Suggestive, not certain (a sign test,
  p about 0.09): **two copies may refuse more true sentences.** The race cannot see content; one possible cause is
  that the copy the service starts first runs on a different kind of its machines. A refused first sentence is what
  makes a turn slow, so more refusals could eat the check's speed gain: only whole turns can say.
- **The counter still over-counted:** a copy stopped before the service answered at all arrives as a plain
  cancellation and was left at its worst case. Fixed: settled at its prompt, counted as read (one more CoreTests check;
  all 5,116 pass).
- **Next, with his word (money):** whole turns, the newcomer's 60 questions, two runs with two copies and two without
  (one run proves nothing: two identical runs gave 17 and 9 slow turns), about $3 beyond his $10 for these tests
  (the counter says $9.18 of it spent; the real spend is lower).

## Whole turns, two copies against one (27 October, afternoon; his extra $4)

The newcomer's 60 real questions at the game's own settings, four runs alternating two copies and one (ClaimBench
`firsts --early ... --two-copies`; F:/LedgerTools/town-scratch/slow-replies/two-copies-turns; $3.25 by the counter,
which counts each stopped copy at its dearest). Scored by tools/voice-live/slow_turns.py (heard = the first sentence's
hand-over plus 0.2 s of Pocket).

| Run | Turns | Heard, median (slowest tenth from) | 5 s or more | First sentence refused |
|---|---|---|---|---|
| two copies, 1 | 58 (2 stopped by its own cap) | 3.71 s (8.15) | 17 | 9 |
| one copy, 1 | 60 | 7.03 s (14.19) | 36 | 12 |
| two copies, 2 | 60 | 4.80 s (11.49) | 29 | 7 |
| one copy, 2 | 60 | 3.29 s (9.65) | 19 | 8 |
| **two copies, both** | 118 | | **46** | **16** |
| **one copy, both** | 120 | | **55** | **20** |

- **No sign of more refusals.** The verdict tests' hint that two copies refuse more true sentences (19 against 9 of 180) does not show in whole turns: 16 first sentences refused against 20.
- **The speed gain cannot be read here.** The service's own pace swung more than any switch could. The two one-copy runs, minutes apart and identical, gave medians of 7.0 s and 3.3 s.
  - The sentence-level measure stands: a median 0.29 s saved, the slowest tenth from 3.2 s instead of 4.0.
- **Verdict: no harm found, the gain as measured by sentence.** Switching it on is a money change in the game, about $0.30 a friends' evening (estimated), so it waits for his yes.
