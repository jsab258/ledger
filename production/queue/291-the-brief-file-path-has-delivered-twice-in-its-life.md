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

BUILT 2026-09-15, all three fixes and the retirement, in one batch with queue
299. Nothing here was proven to DELIVER and that is said first: the workflow
runs on Jafar's PC, no run could be made from the container, and no receipt
exists. The logic and the selftests are proven; the accepting case for the real
path is the next day a brief is written on his machine.

  FIX ONE, ROUTE CHOSEN: A MODE OF THE SENDER. telegram-bot.py's brief_pass
  asks brief.recovery_target when the caller asked for today and today has no
  brief, and hands the answer to the day argument --send-brief already took.
  NOT the workflow step, because choosing which day to recover is measurement
  arithmetic and a decision, and a day-chooser written in pwsh on a machine
  this container cannot execute ships UNRUN, which is the silent-instrument
  failure .claude/rules/instruments.md names. NOT the sweep, because
  outbox.sweep hands its sender a sender(text) with nowhere to put a keyboard,
  so wiring the brief into it builds a second sender for the one message a day,
  which is the race brief.py's own docstring forbids and the thing being
  retired. It goes THROUGH the one-receipt-per-day guard rather than around it:
  recovery_target takes BriefReceipts.state as an argument and returns None
  when it answers sent or held.

  THE WINDOW IS ONE DAY AND THE SERIES IS WHY. The lag between each brief's own
  day and the day it was sent, over every brief on disk, is [0, 0, 0] across 3
  receipts. THE REPOSITORY HOLDS NO DISTRIBUTION OF RECOVERY LAG AT ALL, so
  there is nothing to set a wider bound from and rule 2 forbids inventing one.
  One day is not a chosen threshold, it is the gap between the day a brief is
  written and the next run of the step that sends it.

  AND 2026-09-12 IS DELIBERATELY NOT SWEPT UP. Its NEEDS YOU asks Jafar to "end
  the two leftover background programs and copy the project folder", which he
  did on the 14th (production/pc-ops/windowless-proof.txt). Delivering it now
  puts a stale ask on his phone and hides the fault that caused it, which was
  sixty one hours with no run. It is named out loud by fix TWO instead, with
  the exact command beside it, so sending it costs one run if anyone wants it.

  FIX TWO, SAID WHERE A PERSON OPENS IT. producer-day.py is what the resident
  runs before every brief and what the Producer reads, so the channel section
  now prints, off the FILES rather than off a log: "BRIEFS WRITTEN AND NEVER
  SENT: 1 of 4 written since the daily path opened on 2026-09-09 have no
  receipt of any kind: 2026-09-12", with the command. Three more silences
  closed: brief_pass emits its done line on the missing path too, where it used
  to return before it and leave NO done line at all, so a grep could not tell a
  miss from a step that never started; the same line goes into brief-send.txt;
  and the workflow's exit-6 branch emits a warning annotation.

  FIX THREE WAS OPEN, AND THE EVIDENCE IS A GREP THAT RETURNED NOTHING.
  producer-day.py's brief_receipts read only production/outbound in the
  checkout, and a grep of that file for pc-inbox, inbox-read, INBOX_BRANCH and
  outbound_from_branch returned no hit. The existing briefsSentKnown and
  nothing-measured path fires only when the FOLDER is absent, never when the
  BRANCH is unreadable, which is exactly why 2026-09-14 printed
  briefsSentEver=2: the folder existed, held two, and the third was on
  origin/pc-inbox. A number that looked like an answer. brief_receipts now
  unions both places by CALLING tools/inbox-read.py rather than copying the
  ref, the fetch or the walk, and returns None when the branch cannot be read,
  so briefsSentEver prints nothing-measured instead of the checkout's number
  while the checkout's count survives in words beside it. ref_exists was added
  to inbox-read.py because outbound_from_branch returned an empty dict both for
  "no receipts" and for "never saw the branch", which cannot be told apart.

  WHAT THE FIX DOES NOT DO TODAY, and it is claimed nowhere else: the tree and
  the branch currently AGREE at 566 records and 3 brief-days, so the union
  moves no number right now. It buys the window between the PC pushing and
  inbox-read delivering, which is the window the incident fell into.

  THE RETIREMENT, AND THE NET WAS MEASURED BEFORE IT WAS REMOVED. Retired: the
  brief register in production/outbox/. outbox.sweep refuses a .brief.md, the
  clause names production/briefs/<day>.md and --send-brief and .unprompted.md,
  and .claude/agents/producer.md and production/outbox/README.md say so.
  BLAST RADIUS, COUNTED RATHER THAN ASSUMED: all 9 .brief.md files in the live
  outbox already carry receipts, and the refusal sits after the already and
  held checks, so 0 of 9 are refused and none grows a refusal record. That is a
  live selftest row printing its own denominator.
  AND WHAT THE NET CAUGHT ON 8 AND 9 SEPTEMBER WAS NOT A FAILURE OF THIS PATH:
  --send-brief and its buttons did not exist until Jafar's ruling of
  2026-09-09, so those five went out because nothing else could send them. The
  outbox route has NO KEYBOARD, so the ruling's only measure cannot ride it; it
  was never a net for the brief, it was a way to send an unmeasurable copy.
  THE COST THAT IS REAL, stated rather than waved away: a Producer push in
  brief shape is gone, and .unprompted.md is 120 words against 150 and requires
  BUDGET, so four messages on the 14th would have needed trimming.

  SELFTESTS, run by the resident rather than taken from the report: brief.py 45
  to 57 with 0 failed, producer-day.py 14 to 19 with 0 failed and notMeasured=0,
  outbox.py 115 to 119 cases with 0 failed, inbox-read.py 28 unchanged,
  telegram-bot.py 151 unchanged.
  THE ONE notMeasured=1 IS NOT THIS BATCH'S AND WAS CHECKED RATHER THAN
  ACCEPTED: accept/live/2026-09-15-names-a-picture is queue 232's live fixture
  for the photo sidecar reader, and it sits at lines 1205 to 1214 of the
  COMMITTED brief.py, proven with git show. It cannot measure on a day with no
  brief written, it prints its own NOT MEASURED line with the reason, and it is
  counted outside "0 failed" rather than folded into it. It will measure on the
  next day a brief with a picture is written, which is the same event that
  proves fix ONE.

  RULED 2026-09-15 00:52Z (decision-2026-09-15-ruling-the-grade-lands-as-the-
  legacy-number-and-the-outbox-brief-was-never-a-net.md): the outbox brief
  register retires as built. Its record since the daily path opened on
  2026-09-09: zero catches (no copy of the 12th was written) and two duplicates
  (the 9th, id 39 then id 56; the 14th, id 93 then id 95). THE FILE PATH DID
  SEND ON THE 9TH: brief-2026-09-09.receipt.txt, messageId 56, 10:55:44Z, which
  corrects the framing this item and its brief both carried. On a runner-dark
  day the day's message goes ONCE as .unprompted.md and no brief file is
  written for that day, so the file path cannot duplicate it when the runner
  returns; the streak then carries a true hole. The one-day recovery does not
  reach the 12th (no brief on the 13th to recover from) and --send-brief <day>
  has no caller: queue 303. The 12th's brief is not sent by this item; the
  Producer decides in the next brief whether to say one was missed.

  AND IT RAN ON THE LIVE PATH WITHIN THE HOUR, unasked, which is the evidence
  this item said could only come from his machine. production/pc-ops/
  brief-send.txt on run af6700c at 03:21:03Z, the first run of the step after
  the fix landed. All three lines are new; none of them existed before tonight.

    brief: no recovery either: 2026-09-14 was already sent (messageId=95),
      so nothing is owed for it
    brief: NOTHING MEASURED, there is no brief for 2026-09-15
      (FileNotFoundError). 9 brief(s) are in the tree, newest 2026-09-14.
      Nothing was sent.
    brief: BRIEFS WRITTEN AND NEVER SENT: 1 of 4 written since the daily path
      opened on 2026-09-09 have no receipt of any kind: 2026-09-12. Send one
      from his PC with `python3 tools/runner/telegram-bot.py --send-brief
      2026-09-12`.
    brief-send done: briefDay=2026-09-15 briefSent=0/1 briefAlready=0/1
      briefRefused=0/1 briefChecked=no briefButtons=0 briefChars=0
      messageId=none records=0 briefPhotoCarried=0/1

  WHAT EACH ONE PROVES. The first is FIX ONE'S REJECTING CASE on the live
  path: the recovery ran, asked the one-receipt-per-day guard rather than
  going around it, was told the 14th already went as messageId 95, and
  declined to send anything. The second is FIX TWO: the miss says so, with its
  denominator (9 in the tree, newest named), where it used to exit 6 into
  silence. The third is the dossier line, in the log a person opens, naming
  the one unsent day and the exact command. AND THE DONE LINE EXISTS AT ALL,
  which is the quietest of the four and not the smallest: brief_pass used to
  return before it on this path, so a run that found nothing left NO done line
  and a grep could not tell a miss from a step that never started.
  briefExitCode is still 6 and that is correct: nothing was owed and nothing
  was sent.
  WHAT IS STILL NOT PROVEN, and no run since has changed it: a brief being
  SENT. Every line above is a run that correctly sent nothing. The accepting
  case needs a day on which a brief exists and has not gone, which is the next
  day the Producer writes one. Fix THREE is not visible here either: the
  branch union is producer-day.py's and that is the resident's dossier, not
  this step.

  THE ACCEPTING CASE LANDED AT 05:34:08Z ON RUN e7564eb5, AND IT CLOSES THIS
  ITEM. The acceptance written at the top asks for exactly one thing:
  "briefsSentEver rises on the next day a brief is written, and that is the
  accepting case rather than a green run." It has.

    brief sent: production/briefs/2026-09-15.md chars=947 buttons=2
      messageId=99 photoRef=game-design/sim-shots/grade_three_way.jpg
      photoState=carried
      photoSizes=78x90/279x320/697x800/1115x1280/1192x1369
    brief-send done: briefDay=2026-09-15 briefSent=1/1 briefAlready=0/1
      briefRefused=0/1 briefChecked=yes briefButtons=2 briefChars=947
      messageId=99 records=1 briefPhotoCarried=1/1 briefPhoto=carried
      briefPhotoCapOverBy=0 clause=none
    briefExitCode=0

  WHAT EACH PART OF THAT PROVES. briefSent=1/1 with briefExitCode=0 is the
  path working on its own, unaided, on a day a brief existed. buttons=2 is the
  ruling's only measure riding the message, which the retired outbox route
  could never carry. briefPhotoCarried=1/1 is the PICTURE arriving, which is
  the whole point of a brief about a frame, and briefChars=947 is why: the
  Producer wrote to 947 against the 1024 caption cap, and brief.photo_plan
  drops the picture and sends the words alone when a brief goes over it.
  AND THE COUNTER MOVED: producer-day now reads briefsSentEver=4, where it
  read 2 before tonight and 3 after the fix landed. That is fix THREE working
  on live data rather than on a fixture, because the run's own receipt was
  pushed to pc-inbox as 8f2a506 and the counter reads the union of the branch
  and the checkout rather than the checkout alone.

  SO ALL THREE FIXES AND THE RETIREMENT ARE NOW PROVEN ON THE LIVE PATH, in
  two runs four hours apart: the 03:21:03Z run proved the REJECTING half (the
  recovery declined because the 14th was already sent, the miss said so with
  its denominator, the dossier named the one unsent day and its command), and
  the 05:34:08Z run proved the ACCEPTING half. Rule 5b asks for both outcomes
  with the accepting case first; the live path delivered them in the other
  order, which is not a choice anyone made and is worth saying plainly.

  WHAT IS STILL NOT PROVEN, and it is the one thing left: a RECOVERY actually
  sending. Both live runs exercised the recovery and both correctly declined,
  one because the day was already sent and one because today's brief existed
  so no recovery was needed. The recovery's own accepting case needs a day
  whose brief was written and missed, which is the case queue 303 exists for
  and which nobody can manufacture without waiting for the runner to go dark
  again.

