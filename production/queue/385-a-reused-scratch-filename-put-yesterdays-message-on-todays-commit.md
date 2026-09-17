line: tools (the commit record itself)
spec: c2c30611 CARRIES THE WRONG MESSAGE AND IT WAS NOT A TYPO. That commit adds
  production/outbound/2026-09-17-the-right-sheet.answer.receipt.txt and two agent
  logs, 3 files, 18 insertions. Its message describes run 52's missing include
  and a broken brief reference, which is the body of a commit from 2026-09-16
  19:12Z. Both exist in the history with the same subject; 2994 commits were
  examined for duplicated subjects and this is the only pair whose two members
  describe unrelated work. The other duplicates are repeated merges and repeated
  batch drops from scripts.

  HOW IT HAPPENED, and CLAUDE.md's own rule is half of it. "Write the message to
  a file, not an unquoted heredoc" is there because a backticked identifier has
  twice been executed by the shell. Followed with a REUSED filename it opens a
  second hole: the call that writes the file and the call that commits it can be
  separated. Here `cat > scratchpad/msg3.txt <<EOF ... && git commit -F msg3.txt`
  was refused whole by the verify-gate PreToolUse hook, so the heredoc never ran
  either. The retry dropped the heredoc, kept the commit, and git read msg3.txt
  as it stood: dated 2026-09-16 19:12, 5815 bytes of yesterday.

  WHY IT IS WORTH A GATE RATHER THAN A RESOLUTION. Nothing checks that a commit
  message describes its own diff, and nothing ever will in general. But THIS
  failure has a mechanical signature: a message file whose mtime is older than
  the staged files it is about to describe. That is checkable, cheap, and it
  fires before the commit rather than after it.

  NOT FIXED BY REWRITING HISTORY. c2c30611 is pushed and his PC pulls main; the
  correction is the commit after it, which is the project's habit anyway.
acceptance: a pre-commit check that refuses a `-F <file>` commit whose message
  file is older than the newest staged path, with the accepting case run first
  (a message written in the same minute as the work passes), and the rejecting
  case planted from a deliberately stale file; plus a line in the record naming
  which commit this came from
max_sessions: 1
status: READY 2026-09-17, filed at a stop. NOT started, per his standing order.
