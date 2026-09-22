line: instruments (the reporting channel's own readback)
spec: FOUND BY GETTING IT WRONG IN FRONT OF JAFAR, 2026-09-16, which is the
  only reason it is worth an item.

  At about 21:05Z the resident ran `tools/inbox-read.py` to answer "has the
  figure frame gone out", read `sent=33 newestMessageId=110`, and told him it
  had NOT. IT HAD. The receipt
  `production/outbound/2026-09-16-the-figure-frame.answer.receipt.txt` was
  already on disk and reads `receipt: sent-with-photo`, `messageId: 111`,
  `sent: 2026-09-16T20:18:45+00:00`, 29 seconds after the push.

  SO THE TALLY LAGGED A REAL SEND BY AT LEAST ONE MESSAGE AND FORTY MINUTES.
  The likely cause, stated as a hypothesis and NOT as a finding because it was
  not checked: the receipt was UNTRACKED at the time, and the scan may read
  committed records rather than the working tree. That guess is cheap to
  settle and must be settled before anything is changed.

  WHY IT MATTERS MORE THAN ITS SIZE. `newestMessageId` is the number a session
  reaches for to answer DID IT REACH HIM, and it answered no while the answer
  was yes. A false negative there is worse than a missing number: it invites a
  session to re-send, which is how Jafar gets the same message twice, and the
  register exists to stop exactly that kind of noise.
acceptance: the question "did this message send" is answered from the RECEIPT
  beside the message rather than from a tally, with the accepting case (a
  message with a receipt reads sent) proven first and the rejecting case (a
  message with none reads nothing-measured, never "not sent") beside it; and
  whatever `newestMessageId` is a statistic OF is named where it prints
max_sessions: 1
status: READY 2026-09-16, filed at the budget ceiling, NOT started.

  THE CORRECTION ITSELF IS ALREADY MADE: he was told in the same session that
  the frame did arrive, with the message id and the send instant. This item is
  the instrument, not the apology.

  DO NOT "FIX" THIS BY COMMITTING RECEIPTS SOONER. That hides the lag behind a
  habit and leaves the next session with the same wrong instrument the moment
  a receipt is fresh. The reading has to be right on an uncommitted receipt,
  because that is exactly when the question gets asked.
