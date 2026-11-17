# Capping tool output with hooks: research (n16-10)

Dated 17 Nov 2026. Helper for the production session; the advisor's review of 17 Nov
(tool output carried through later steps cost US$67 in a day, mostly helpers' shell
output: 2.64 M tokens in 5,061 calls, plus whole-file reads).

Method researched: official Claude Code docs, read as their raw markdown in full
(fetched with curl, not search snippets), all read 17 Nov 2026:

- Hooks reference: https://code.claude.com/docs/en/hooks.md
- Hooks guide: https://code.claude.com/docs/en/hooks-guide.md (skimmed for examples only)
- Settings and precedence: https://code.claude.com/docs/en/settings.md
- Subagents: https://code.claude.com/docs/en/sub-agents.md
- Tools reference (Bash output limits, Read limits): https://code.claude.com/docs/en/tools-reference.md

Reference first: no game reference applies (tooling); the docs' own examples
(block-rm.sh, the Bash validator) are the method copied: a PreToolUse command hook
reading JSON on stdin and answering with hookSpecificOutput.

## Questions

1. Can a PreToolUse hook on Bash rewrite the command? With which fields and exit codes?
2. Can a PostToolUse hook replace the tool's output? Does it cover failing commands?
3. Can a PreToolUse hook on Read refuse a read with a message Claude sees?
4. Do settings-file hooks apply to subagents?
5. Where do hook settings live, and how do levels combine?
6. What does Claude Code already cap on its own?
7. What about the PowerShell tool?

## Answers (hooks.md unless named)

1. Yes. `hookSpecificOutput.updatedInput` "replaces the entire input object, so include
   unchanged fields"; permission rules and a Bash command's auto-background eligibility
   are evaluated against the input the hook returns, not the one Claude sent. With no
   `permissionDecision` the normal permission flow applies. In auto mode a changed input
   can be denied because the server reviewed the original, but "a command hook in
   settings or a plugin's hooks file can change Bash, PowerShell, Monitor, Edit, Write,
   and NotebookEdit calls without this denial" (section "PreToolUse updatedInput in auto
   mode"). Exit 0 + JSON is the structured path; exit 2 blocks with stderr as the reason;
   any other code is a non-blocking error and the call runs unchanged (unless
   `onFailure: "block"`, v2.1.295+). Stdout must be one JSON object and nothing else.
   `permissionDecision: "deny"` with `permissionDecisionReason` is shown to Claude.
2. Yes for success only: PostToolUse `updatedToolOutput` replaces what Claude sees, and
   must match the tool's output shape (Bash: stdout, stderr, interrupted, isImage; a
   mismatch is ignored). PostToolUse "runs immediately after a tool completes
   successfully"; PostToolUseFailure "can't rewrite a result, so a failing command's
   output reaches Claude unchanged". For Bash, any exit 1 except grep/rg/find/diff/test/
   git diff/git grep counts as a failure (tools-reference, Output limits). So a
   PostToolUse cap would miss failing builds and tests, the noisiest output. Chosen:
   PreToolUse rewrite, which covers both.
3. Yes: Read's tool_input has file_path (always absolute, backslashes on Windows),
   offset, limit; a deny reason reaches Claude. Hooks don't fire for @-mentioned files.
4. Yes. "Hooks from settings files, managed policy settings, and plugins also run inside
   subagents ... the input carries the agent_id and agent_type" (Hook locations; same in
   sub-agents.md, "Define hooks for subagents"). Subagent frontmatter hooks are extra
   and need workspace trust.
5. ~/.claude/settings.json (all projects), .claude/settings.json (project, committed),
   .claude/settings.local.json (project, personal), managed policy, plugin hooks.json,
   skill and subagent frontmatter. Hook entries merge across levels rather than replace;
   the same handler in two files runs once. Matching hooks for one event run in parallel.
   Default timeout for a command hook 600 s. Shell form runs under Git Bash on Windows.
6. Bash: inline up to about 30,000 characters for a valid result, past that a file path
   plus a 2,000-character preview; a failure inline up to about 10,000 characters, then a
   head-and-tail excerpt with no file path. BASH_MAX_OUTPUT_LENGTH changes the read-back
   window (max 150,000), not the inline ceiling (tools-reference). Read: one call returns
   at most 25,000 tokens and refuses a whole file over 256 KB; `allow_large: true` reads
   it whole (v2.1.296+). Hook strings (additionalContext, plain stdout) are capped at
   10,000 characters. So outputs from 6,000 to 30,000 characters, and failing output to
   10,000 with no file, are what the built-in limits leave; that is the band this item
   cuts.
7. On Windows with the PowerShell tool on, Claude treats PowerShell as the primary shell;
   a hook matching only Bash never sees those calls. The docs show no wrapper pattern for
   PowerShell output and its exit code ($LASTEXITCODE vs $?) differs, so PowerShell is
   not rewritten here; only an unfiltered recursive Get-ChildItem is refused.

## Project facts checked (17 Nov)

- Existing hooks (.claude/settings.json): UserPromptSubmit gate_prompt_hook.py,
  PostToolUse page_read_hook.sh, Stop stop_hook.py; settings.local.json empty. No
  PreToolUse hook exists, so nothing is replaced. Style reused: shell-form
  `python "$CLAUDE_PROJECT_DIR/tools/..."`, faults swallowed.
- Allow rules exist (Bash(git add *), git commit, git fetch, dotnet run/build/test...).
  Because rules match the rewritten text, the tool rewrites only in auto and
  bypassPermissions modes; other modes pass through (dontAsk would otherwise deny).
- Python starts in about 0.08 s here today (the 1 s note in page_read_hook.sh is old);
  the hook takes about 0.14 s a call, measured over five runs.
- Shelf: F:/LedgerTools/tmp, storage map "working", retention.json scratch limit age
  7 days, pruned file by file (retention.py prune_old). Run files go in
  F:/LedgerTools/tmp/tool-output/<date>/, the log in .../log/<date>.tsv.

## Design taken (tools/output_cap.py)

The command runs unchanged inside `{ ...\n} > out 2> err` in the same shell, then a
short sh function prints whole output under 60 lines / 6,000 characters (and deletes
the file), else the first and last 25 lines (2,500 characters each) and a line naming
the file, lines and bytes; stderr likewise on stderr with a smaller budget; the group's
exit code is returned with `return`, not `exit`, so the tool's own cwd tracking still
runs. Passed through untouched and logged: run_in_background, a trailing `&`, exit,
exec, set -e, nohup, an unterminated heredoc, a trailing backslash, `# full-output`.

## Unverified / not reached

- Not yet run as a live hook: the hook was tested by feeding it the documented JSON and
  executing its rewritten command in Git Bash, not inside a Claude Code session. The
  session's one real run checks: the rewrite applies in auto mode without the
  "a hook changed this call's input" denial; cd persists in the main session; the
  transcript shows the capped text.
- Whether the installed Claude Code version has every field named above (versions are
  given in the docs for onFailure, allow_large, scratchpad_dir) was not checked.
- The hooks guide was skimmed, not read in full; nothing in it was used.
