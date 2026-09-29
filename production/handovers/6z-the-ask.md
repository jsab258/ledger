# The outfit's ask: Ron, the envelope, the landing

Town list 6z, 6bn and 6cj. Settled as written, 29 September (DECISIONS).
Design: game-design/first-ask-2026-09-29.md and game-design/landing-2026-09-29.md.
Code: ledger/Assets/Scripts/Core/Arrangement.cs and TheLanding.cs.

**What the player gets:**
- On the first night, then every other night, Ron brings a plain dark coat and
  Mickey's envelope after dark.
- He can take it to the man at the ferry landing after ten, tell Ron no (which
  ends it for good), or stay away. Three nights away with none done between
  also end it.
- The man at the landing says the job is done and when the next one comes.
- Whatever he does becomes the outfit's talk.
- Never a game over.

## Wire it

1. **An ask night** is `asks.NextNight` (days count from 0, as `GameTime` does).
   After dark (eight), Ron comes to the office with the coat and the envelope.
   If Tom is not there, Ron goes to find him before ten.
2. **When Ron hands them over:** `asks.Delivered(night, ronGossiper, now)`. Ron
   then remembers the terms. Also `hints.Happened(Moment.FirstAsk, …)` the first
   time.
3. **Talking to Ron while `asks.AskStands(now)`** (from then until one in the
   morning, unanswered): send `"ask": {"tonight": true}` with each line. The talk
   program asks Ron's plain question itself when a line sounds like a no.
4. **When a talk reply carries `"refusedAsk": true`** (a walked-off reply
   included): `asks.Answer(NextNight, Refused, mill, t)`. Here `t` is the later
   of when he said it and 22:00 on that night's own day, even after midnight.
5. **At the ferry landing, from ten till one:** show `TheLanding.Line(asks, now, moment, seed)`
   as plain text, once a night each (no voice is cast for him):
   - `Comes` when Tom comes up to him;
   - `HandsOver` just after `asks.Answer(night, Did, mill, now)`;
   - `NothingToHand` when he leaves with nothing handed over;
   - `TalksToHim` in place of talk (he has no talk card).
6. **At each dawn and after every load:** `asks.PassedTo(today, mill, now)`.
   It counts a night Ron brought and nobody answered as one he stayed away; a
   night Ron never reached him passes silently.
7. **Session record:** an `ask` line (`night`, `answer`, `story`) each time a
   night is answered, `PassedTo`'s nights included.
8. **Bodies and voices:**
   - The outfit's man (cast id `outfit_man`) needs a body at the ferry landing
     at night and at the cafe at nine.
   - The three new outfit banks still need recording in the speakers' voices.
   - Ron's fixed lines (his plain question, "Right you are, boss. I'll take
     your no down the landing.") go in his voice.

## Port

`Arrangement` (in place of the old week's cast-out rule, which stays only in
the legacy Unity build) and `TheLanding`, with `Arrangement.WoundWordAt` and
`WoundNight`. Match the rows behind `--awaiting-port`: `Ask`, `AskStory`,
`AskRonRemembers`, `AskSave`, `AskLoad` and `Landing`.

## Save

`asks.ToJson()`, already inside `TownSave.Asks`.

## Walk it

1. Night one: at eight, Ron brings the coat and the envelope.
2. At the landing after ten, the man asks for Mickey's. Hand it over: "Right.
   Wednesday, same again."
3. The next morning Darren says something like "Heard you did Mickey's run."
4. On night three, tell Ron no: Ron asks plainly, "yes" ends it, and at the
   landing the man says "Ron's been down. We're done, you and us."
