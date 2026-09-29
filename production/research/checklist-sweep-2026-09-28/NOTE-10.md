# A sweep for the town lane, tenth pass, 29 September 2026

What this is: every town list item is done, waiting on Jafar (i, q, aq, as,
bj, bp, bu) or hanging on his answer (bv). This pass reads the archived
checklist (706 open rows cited nowhere, nearly all the builder's screens,
physics and combat), FINDINGS for the town's faults, and the approved first
hour through to day 7. Evidence from c5ff2661.

## Candidates, most important first

1. **Replies cut at eight seconds** (FINDINGS, the voice delay, its talk half;
   ROADMAP's slice, "fast enough to feel like talk"; A31.18). About 5 h, $3.
   Why: in the 29 September sample 5, then 10, of 24 turns hit the talk
   program's 8 s limit; on the 28th the slowest tenth finished in 6.7 s.
   Sheila answered "How long have you worked here?" with "Give me ten
   minutes." In the game a slow turn says its first sentence and loses the
   rest, or brushes him off.
   Not done: tools/talk_cost_sample.py runs without --early, which the game
   passes (CrimeProbe.cpp:2636), so the game's rate is unmeasured; the limit
   covers the whole turn (TalkHelper Program.cs:753, 779); a turn cut after its
   first sentence is recorded "brush" (859-860); no step is timed.
   The work: sample as the game runs it; time each step; cut the slowest
   without losing catches (held-back half); the rest its own limit once a first
   sentence is heard; a cut turn recorded "cut"; FINDINGS corrected.

2. **Sheila's trust, and the week's end** (the first hour's day 7; the
   outline's Act I; A33.05). About 8 h; may prove bigger.
   Why: friends talk to Sheila most, and nothing makes her trust him: she
   calls him the new owner for good, her card keeps the real book "until I
   fully trust the new owner", and the week never reaches "So which is it
   going to be?"
   Not done: the program takes "trusts" from the game (Program.cs:101-103,
   466), but nothing decides it (DECISIONS, 28 September: "until the real
   book's scene is built, nothing does"); no Core code has the book or day 7.
   The work: a Core piece for when she trusts him, from what she holds of him
   (memories, owning up, a caught lie), or DS Ellis asking her (bq); the book
   shown then; on day 7 her question on state, his answer (wind it down, take
   it over, refuse to say) read in two steps as a no to Ron is, filed as the
   street's story; TownSave, SaveChaos, TownReach --first-hour to day 7; the
   trust rule and her words to his page. The fire's page waits on his ruling.

3. **A rumour at NaN confidence spoils the save** (FINDINGS: "the town's to
   fix"). About 1.5 h.
   Why: the hearer's suspicion turns NaN and the save cannot be read back: a
   friend loses his game.
   Not done: SuspicionTracker.Raise and Lower use Math.Clamp, which passes NaN
   (Suspicion.cs:206-215); Gossip.cs:471 and 684 multiply confidence in
   unchecked.
   The work: refuse a number that is not finite there and where a rumour is
   filed and told; a regression test and a SaveChaos case; the port's golden
   rows handed over.

4. **Open with nobody in** (A25.05; bo's remainder). Under 1 h.
   Why: on a Monday at eleven anyone says Hal's is open while Hal is at
   Rita's; the fish shop is open until two on Wednesdays though its keeper
   leaves at one; Mickey's has an hour on Sunday nights with nobody in.
   Not done: hook-cast.json's hours against Hal's and Marla's routines.
   The work: fit the hours, or a note ("back at twelve"). The port reads no
   hours (CastDay.h), so no golden rows change.

## Considered and set aside

- The night coming back only through Darren (the first hour on paper):
  design, already on his page.
- FINDINGS: the Core's old world still a pub (retired, renamed before
  revived); the old launchers (the builder's tools; the shortcut is his);
  Tom's history, small-talk fallbacks and a shopkeeper's "we open at eight"
  (q, his yes).
- The rivals' names overheard: new lines wait on aq's sample.
- Already covered: A40.11 (the program ends when its input closes), A39.19
  (an unwritable talk save says so), A49.14 (written to a copy, then moved).
