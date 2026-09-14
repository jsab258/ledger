line: tools and channel
spec: the daily brief is written and mostly never sent. On 2026-09-14
  tools/producer-day.py prints briefsSentEver=2 briefStreakReadable=0/7
  briefDaysTapped=0 briefTapRecords=0 briefLastDay=nothing-measured
  briefAccepted=no. The two are brief-2026-09-09.receipt.txt and
  brief-2026-09-10.receipt.txt, the brief-<day> shape --send-brief writes.
  Briefs exist on disk for 7, 9, 10 and 12 September;
  production/briefs/2026-09-12.md has a photo sidecar and NO receipt of any
  kind. THE CAUSE: nothing in the tree invokes --send-brief. A grep returns
  tools/runner/run-night.ps1:106 (which says in its own words that the night
  runner neither writes nor sends it), tools/runner/cards.py (a retirement
  notice) and telegram-bot.py itself. No caller.
  THE OTHER HALF, and it names the fix: production/outbound/ holds five MORE
  receipts shaped <name>.brief.receipt.txt, four on 8 September and one on the
  9th. Those are OUTBOX messages in the brief register, delivered by the bot's
  sweep, which needs no caller. The brief REGISTER has reached him seven times;
  the brief FILE path twice.
acceptance: briefsSentEver rises on the next day a brief is written, and that
  is the accepting case rather than a green run. A run that finds no brief for
  the day must PRINT that rather than exit 6 into silence, which is the
  rejecting case and is the half that hid this. Choose one route and record
  which: give --send-brief a caller on the sweep's schedule, or deliver the
  brief through the outbox and rebuild the readable/unreadable buttons there,
  or retire the brief file and make the daily message an outbox message.
max_sessions: 1
status: READY 2026-09-14. Found while checking whether today's brief would
  reach Jafar before writing it. It would not have. The 2026-09-14 brief was
  therefore ALSO written as an outbox message so it would send, and the
  double-send risk was accepted deliberately: twice is better than never, and
  never is what 12 and 13 September measured. Jafar read the missing briefs of
  11 to 14 September as the runner being dark from the 11th. That is part of
  it. Briefs were also unsent on days the machine was up, and briefStreakReadable
  printed 0/7 the whole time and was read as him not tapping rather than as
  messages not arriving. CLAUDE.md rule 12: this is the outbound half of the
  feedback channel.
