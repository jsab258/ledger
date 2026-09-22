line: tools and channel
spec: The one-receipt-per-day guard stops a brief being SENT twice. Nothing
  stops the brief FILE being rewritten after it was sent, and nothing notices
  when it has been. A tap is then recorded against text he never read, and the
  streak, which is the channel's only measure, counts a verdict on words that
  no longer exist. Give the day's brief the assertion the send already has the
  data for.
acceptance: a run in which production/briefs/<day>.md differs from the version
  its own receipt names SAYS SO, in the place a person opens, before anything
  records a tap against it. Both outcomes watched and the accepting case first:
  a brief untouched since its send reads as matched, and a brief edited after
  its send reads as changed with both identifiers printed. No new sender, no
  new gate on writing; this is a reading, not a refusal.
max_sessions: 1
status: READY 2026-09-15. Found by nearly walking into it, which is the only
  reason it is written down tonight.

  HOW IT WAS FOUND. The daily wake fired at 04:06:55Z and its step 6 is "spawn
  the Producer, give it the gathered file, and let it write
  production/briefs/<day>.md in its own words". Today's brief had ALREADY been
  written and sent at 03:34:08Z as messageId 99, because the ruling of 00:52Z
  dictated the frame go to him through the Producer and that happened before
  the wake came round. FOLLOWING STEP 6 MECHANICALLY WOULD HAVE OVERWRITTEN
  THE FILE HE WAS SENT. The send would not have doubled, because the
  one-receipt-per-day guard would have refused it, so the fault would have
  been silent: a brief file on disk carrying words he never received, and a
  tap on messageId 99 recorded against them.

  THE ASSERTION IS MISSING AND THE DATA FOR IT ALREADY EXISTS. Every brief
  receipt carries the commit of the file it sent:
  production/outbound/brief-2026-09-15.receipt.txt reads
  fileCommit: e7564eb578d93ca1c124c9f729dc271d4db08bbc. A grep for fileCommit
  across tools/ returns only the sites that WRITE it, in brief.py and
  outbox.py, and a docstring. NOTHING READS IT BACK. So the receipt knows
  exactly which version went and no reader ever asks.

  WHY THIS IS THE INVERSE OF THE HOLE THE WAKE ALREADY NAMES. That prompt
  says, in its own words: "on a day this wake fires, a brief file for that day
  must EXIST. Its absence currently looks identical to a quiet day, and the
  streak will read 0 of 7 as though he had not tapped when the truth is that
  nothing was written." The same sentence holds with one word changed: a brief
  that exists but no longer matches what was sent looks identical to one that
  does, and the streak counts a tap on it either way. One hole is a missing
  file, the other is a changed one, and only the first has been written down.

  WHAT THIS ITEM IS NOT. It is not a lock on the brief file. Rewriting a brief
  after it sent is sometimes right, for instance when the next day's is being
  drafted from it, and a refusal would get in the way of that. The ask is that
  a run SAYS the file and its receipt disagree, which is this project's
  standing shape: verify a job's EFFECTS, not its exit code.

  AND THE OPERATIONAL FINDING UNDERNEATH IT, which outlives this fix. Two
  things can now want to write the same brief file on the same day: the daily
  wake at 04:00 UTC, and a ruling that dictates the Producer send something.
  Tonight they missed each other by twenty-six minutes. Nobody decided that
  ordering and nothing enforces it.

  RULED BY JAFAR 2026-09-15, in his words: "Queue 304 is right and gets the
  assertion: nothing reads fileCommit back, so a changed brief looks identical
  to an unchanged one and a tap can be recorded against text I never saw. Only
  one thing may write a day's brief; if a ruling dictates a send, the daily
  wake defers rather than overwriting."

  SO THE ITEM GAINS A SECOND HALF, and it is the ordering rule rather than the
  assertion. The assertion says a changed brief is NOTICED. The ordering rule
  says it should not happen: ONE WRITER PER DAY'S BRIEF, and when a ruling
  dictates a send the daily wake DEFERS rather than overwriting. That is the
  near miss of this morning turned into a rule: the wake fired at 04:06:55Z on
  a brief already sent at 03:34:08Z, and twenty-six minutes was the whole
  margin.
  THE DEFERRAL NEEDS SOMETHING TO READ. A wake that is to defer must be able to
  tell that today's brief already went, and the receipt is what says so:
  production/outbound/brief-<day>.receipt.txt exists with a messageId. That is
  the same file the assertion reads for fileCommit, so both halves of this item
  read one artifact and neither needs a new one.
  STATUS: READY, and both halves land together. The assertion without the
  ordering rule would report a collision it could have prevented.

