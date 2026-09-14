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
status: READY 2026-09-14.
  PROVEN ON THE SAME DAY IT WAS FILED. The 2026-09-14 brief was sent through
  the outbox as ruled here. production/pc-ops/outbox-sweep.txt on 622bc39
  records all three of that evening's messages leaving the PC in three
  seconds, message ids 92, 93 and 94, consecutive: sent=1 captionedSent=2
  refused=0 unsent=0 sendFailed=0 receiptRefused=0 recordsWritten=3
  outboundLatencySecAtWorst=39 (file commit instant to send instant). The
  brief FILE path was not invoked that night and sent nothing, exactly as
  this item predicts. So the accepting case for the outbox route is already
  on record; what is owed is the choice of route and the buttons.
  NOTE FOR WHOEVER TAKES THIS: receipts are pushed to the pc-inbox BRANCH
  (the sweep line reads "inbox: pushed 3 file(s) as 09c6d19 to pc-inbox"),
  not to main, so an absence of receipts under production/outbound/ on main
  is NOT evidence that nothing sent. That absence misled this resident for
  several minutes before the sweep log settled it, which is the ci.md rule
  working: run the existing entry point and read its output.
  Found while checking whether today's brief would
  reach Jafar before writing it. It would not have. The 2026-09-14 brief was
  therefore ALSO written as an outbox message so it would send, and the
  double-send risk was accepted deliberately: twice is better than never, and
  never is what 12 and 13 September measured. Jafar read the missing briefs of
  11 to 14 September as the runner being dark from the 11th. That is part of
  it. Briefs were also unsent on days the machine was up, and briefStreakReadable
  printed 0/7 the whole time and was read as him not tapping rather than as
  messages not arriving. CLAUDE.md rule 12: this is the outbound half of the
  feedback channel.

  RETRACTED IN ITS CAUSE, 2026-09-14T20:2xZ, BY THE RESIDENT WHO FILED IT.
  THE CENTRAL CLAIM OF THIS ITEM IS FALSE. "Nothing in the tree invokes
  --send-brief" is wrong. The caller is
  .github/workflows/ledger-install-supervisor-task.yml:683, which runs
  telegram-bot.py --send-brief as its own step, with its own log at
  production/pc-ops/brief-send.txt. That log's header states the design
  plainly: "ONE message: the brief a Producer turn wrote for today, checked
  here against the register before it goes, carrying two buttons, readable and
  unreadable. One receipt per day, so it is never sent twice. The bot's loop
  does NOT also send it: one sender, no race."
  AND IT RAN TONIGHT AND WORKED. production/outbound/brief-2026-09-14.receipt.txt
  reads file=production/briefs/2026-09-14.md, messageId=95,
  sent=2026-09-14T19:09:03Z, buttons=2/2, outboundLatencySec=50. A later pass
  read "ALREADY SENT production/briefs/2026-09-14.md (messageId=95), so nothing
  was sent this pass", which is the one-receipt-per-day guard working.
  HOW THE ERROR WAS MADE, recorded because the shape of it is the lesson: the
  grep was `grep -rn "send-brief" --include=*.yml ... | grep -v "telegram-bot.py"`.
  The workflow line invokes `tools\runner\telegram-bot.py --send-brief`, so
  THE EXCLUSION FILTER DELETED THE CALLER BECAUSE THE CALLER NAMES THE CALLEE.
  A filter that hid the answer, in a project whose own rules say any cap in an
  extraction step must announce when it bites. It did not announce, and nothing
  made it.
  THE COST. A builder was dispatched to rebuild a working delivery path and was
  stopped mid-flight. Jafar was told in his own brief that "the daily-brief path
  has delivered twice; this one always sends", which is false, and he ordered
  work off it. AND HE RECEIVED THE BRIEF TWICE tonight: id 95 by the brief path
  WITH its two buttons, and id 93 by the outbox copy this item ordered, without
  them. The double send was accepted as a deliberate risk on a premise that was
  wrong, so it bought nothing.
  WHAT SURVIVES AND IS STILL OPEN. briefsSentEver read 2 before today and briefs
  exist on disk for 7, 9, 10 and 12 September, so a gap between briefs written
  and briefs sent IS real; production/briefs/2026-09-12.md still has no receipt
  of any kind. WHY is NOT diagnosed and must not be guessed at again. The next
  person reads production/pc-ops/brief-send.txt for those days before forming
  any theory, per .claude/rules/ci.md: the entry point is cheaper than the
  argument, and this item is what happens when it is skipped.

  AND HERE IS THE ACTUAL CAUSE, found from logs that already existed, which is
  what should have happened first. TWO FACTS, together sufficient.
  ONE: NO RUN OF THE SENDING WORKFLOW HAPPENED BETWEEN 2026-09-11 09:04 AND
  2026-09-14 17:47, sixty one hours. All five files that workflow writes share
  the identical gap (brief-send.txt, outbox-sweep.txt, scheduled-task-verify.txt,
  inbox-flush.txt, supervisor-status.txt), 01c3fd57 to 3df34890. The 09-12
  brief WAS committed at 2026-09-12 04:26 in 2ae59607, touching
  production/briefs/2026-09-12.md, which is exactly the workflow's push filter
  path. So the trigger's condition was met and no run followed. THE PC WAS NOT
  DARK: supervise reported studio-watcherUptimeSec=268411, 3.1 days, and the
  bot sent two replies on the 13th with receipts on origin/pc-inbox. The
  machine was up and the poll loop was delivering while the brief was not,
  because nothing but that CI step sends the brief.
  TWO: WHEN A RUN FINALLY CAME, THE SENDER COULD NOT REACH BACK FOR IT.
  3df34890's brief-send.txt reads briefExitCode=6 and "brief: NOTHING MEASURED,
  there is no brief for 2026-09-14 (FileNotFoundError). 8 brief(s) are in the
  tree, newest 2026-09-12. Nothing was sent." --send-brief asks for the brief
  whose name is TODAY IN UTC and exits 6 when it is absent. SO A BRIEF THAT
  MISSES ITS OWN DAY IS UNREACHABLE AFTERWARDS BY DESIGN, NOT BY FAULT. That is
  the whole mechanism: the 09-12 brief had no run on its day, and the day is
  the only key the sender accepts.
  AND THE MISS IS SILENT. Exit 6 is continue-on-error in the workflow, so
  nobody learns of it unless they open brief-send.txt. The recovery ALREADY
  EXISTS as a command, since --send-brief takes an optional day argument, and
  nothing runs it.
  AND THE COUNTER READS THE WRONG BRANCH. briefsSentEver is computed by
  tools/producer-day.py over production/outbound/ ON MAIN, but receipts are
  pushed to the pc-inbox BRANCH and merge later.
  brief-2026-09-14.receipt.txt existed on origin/pc-inbox from 19:09Z and was
  not on main, so the counter read 2 while three briefs had in fact been
  delivered. The counter is not wrong about what it reads; it is reading a
  branch that is not where receipts land. THAT, not a missing caller, is why
  this item opened with a false number.
acceptance-superseded-2026-09-14: the original acceptance below was written
  against a cause that turned out false. The real ones: a brief that misses its
  own UTC day is RECOVERABLE, by something that actually runs the day argument
  the sender already accepts; a run that finds no brief for today SAYS SO
  somewhere a person sees, rather than exiting 6 under continue-on-error; and
  briefsSentEver counts receipts wherever they land rather than only on main.
  Nothing about the delivery mechanism itself needs rebuilding.
