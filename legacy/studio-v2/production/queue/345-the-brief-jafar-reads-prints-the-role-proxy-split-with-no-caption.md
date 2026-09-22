line: instruments (tools/morning-brief.py, the split section)
spec: queue 344 captioned gameShareDay in ledger/verify.py so the number cannot
  be read without knowing it classifies by ROLE. There is a SECOND reader of
  the same set, and it is the one Jafar actually reads: tools/morning-brief.py
  imports vf.GAME_AGENTS and prints splitStudio and splitGame with
  basis=spawns, which names the UNIT and is silent on the CLASSIFIER. So the
  captioned number lives in a footer and the uncaptioned one goes to his phone
  every morning.
acceptance: the brief's split tokens carry the same basis caption as the
  footer's, from the same single constant, so the two cannot drift apart
max_sessions: 1
status: READY 2026-09-16, found by the 344 builder and outside its one-file
  brief, which was the correct call.

  THE THREE SITES, read rather than recalled:

      tools/morning-brief.py:562   if agent in vf.GAME_AGENTS: game += 1
      tools/morning-brief.py:1420  "splitStudio=%d/%d basis=spawns %s"
      tools/morning-brief.py:1422  "splitGame=%d/%d basis=spawns %s"
      tools/morning-brief.py:1645  "splitStudio=%d/%d splitGame=%d/%d splitBasis=spawns ..."

  basis=spawns is TRUE and answers a question nobody asked. The unit was never
  in doubt; the classifier was. A caption that names the unit while the error
  is in the classifier is the shape of an honest-looking number that misleads.

  ONE CONSTANT, NOT TWO CAPTIONS. 344 added GAME_SHARE_BASIS beside
  GAME_AGENTS in verify.py and this file already imports GAME_AGENTS from
  there as vf.GAME_AGENTS, so the same import carries the caption and the two
  readers cannot drift. A second hand-typed caption here would be the
  duplicated-idea fault, and it would drift on the first edit.

  WHY IT MATTERS MORE HERE THAN IN THE FOOTER. Queue 111's own status line
  says this number "BLOCKS THE BRIEF'S BUDGET SECTION BEING TRUSTED". The
  footer is read by the studio, which now has the caption and the queue items.
  The brief is read by the one person who cannot check it against the source.

  UNDER D45 a tool that measures the game: a test, no review.
