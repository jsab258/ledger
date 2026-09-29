# Sheila's trust, and the week's end

Town list 6bz and 6ca. Decided by the town, 29 September. Winding it down
ending Mickey's arrangement (6cc) is still Jafar's call; it is built as
recommended. Design: game-design/sheila-trust-2026-09-29.md and
game-design/week-end-2026-09-29.md. Code: ledger/Assets/Scripts/Core/Trust.cs,
WeeksEnd.cs and the talk program.

**What the player gets:**
- Sheila keeps him at "the new owner" and keeps Mickey's real book back until
  she trusts him. That takes three different days of talk, with her never
  seeing or hearing of him about the place when a deed was done, never catching
  him out, and not wary.
- On the week's seventh day, a Sunday, she waits at the office from ten and
  asks "So which is it going to be?": wind it down, take it over, or refuse to
  say.
- The street learns his answer. Winding it down ends Mickey's arrangement that
  night.

## Wire it

1. **Trust is the talk program's.** Each reply to her carries `trusts`, and on
   the one turn it is earned, `"trustEarned": true`. It travels with the talk's
   save. Send `"trusts": true` only if the game itself decides she trusts him.
   Once trust is earned, the game may show her the real book; its scene waits
   on the fire.
2. **On the seventh day,** when it is a Sunday and `week.Waits(now)`: place
   Sheila at Mickey's office from ten till twelve, and while her question
   stands, until six.
3. **The first time he talks with her at the office from that day:**
   `week.Ask(now, sheTrustsHim, atOffice: true)`, and send
   `week: {ask: true, realBook, dayOff}` with the line.
4. **While `week.Stands(now)`:** send `week: {stands: true, realBook}` with each
   line to her. Add `ended` once Mickey's arrangement has ended.
5. **On a reply's `weekAnswer`:** `week.Give(answer, thatTurnsTime, mill, cast, asks)`.
   WindDown ends the arrangement that night (`Arrangement.WoundDown`). Ron knows
   at once; the man at the landing knows once Ron has been down at eleven.
6. **At each midnight:** `week.Close(now, mill, cast)`. A day ended unanswered
   is his refusal to say.
7. **Session record:** `trust`, `week` and `calls` lines
   (production/specs/session-record.md).

## Port

`WeeksEnd` (Ask, Stands, Give, Close, Waits, ToJson, FromJson), and
StreetVoice's banks:
- recognition/week-winddown, week-takeover and week-wontsay;
- recognition/outfit-wounddown.

`StoryThatShows` takes the week's answer except for Sheila herself, and
`RegardFor` weighs it nothing. Match the rows behind `--awaiting-port`:
`WeekAsk`, `WeekFiled`, `RecognitionWeek`, `WeekShows` and
`RecognitionOutfitWound`. Her lines here are fixed, so with talk off they still
come.

## Save

`week.ToJson()`, already inside `TownSave.Week`. Trust is in the talk's own
save.

## Walk it

1. Talk with Sheila on three different mornings. On the third, she calls him by
   name.
2. On Sunday at ten she is in the office: "So which is it going to be?"
3. Say "Take it over." The next day someone on the street says they heard he
   is taking Mickey's on.
