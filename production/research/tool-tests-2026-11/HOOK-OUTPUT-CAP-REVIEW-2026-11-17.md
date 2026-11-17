# Review: output-cap hook (n16-10), 17 Nov 2026

Fresh, hostile review of tools/output_cap.py (uncommitted, 551 lines), the snippet
HOOK-OUTPUT-CAP-SETTINGS.json and HOOK-OUTPUT-CAP-RESEARCH-2026-11-17.md. Nothing was edited.

**Verdict: PASS WITH FIXES.** Fixes 1 to 4 are needed before the hook goes into
.claude/settings.json. Fixes 5 to 9 can follow.

## What was run

- `python tools/output_cap.py --self-test`: 79 checks, 79 passed, failed=none.
- 13 extra inputs of the reviewer's own, through `decide()`. Each was run twice in Git Bash,
  once as written and once as rewritten, and the results compared. Four malformed inputs
  went through the `hook` entry point. The run folder was the session scratchpad, removed
  afterwards.
- A replay of 6,675 real Bash and PowerShell calls from the last 150 transcripts of this
  project through the refusal rules and `skip_reason`.
- The existing hooks, the user-level and local settings (no deny or ask rules today),
  storage-map.json, retention.json and retention.py's prune_old.

## Findings by question

**(1) Does the rewrite change what a command does, or hide an error?**

In normal running it does not. Each of these behaved the same both ways, with the same
exit code and the same output:
- paths with spaces and `cd` carried after the group (`cd "/c/Program Files" && pwd`);
- stdin (`read x`);
- quotes, heredocs with `{ } $` inside, `if/fi`, `false || echo`;
- a trailing `# }` comment;
- `&&` chains, pipes, the exit codes of child processes, and stderr kept on stderr.

The faults found are in the edge cases (fixes 1, 2 and 6 below):
- **The output vanishes when the shell exits early.** `set -u` on an unset variable,
  `${X:?msg}`, and `source` of a script that calls `exit` all leave the shell inside the
  group (output_cap.py:236). `__oc_show` never runs. Measured: the original printed `start`
  and `NOPE_UNSET: unbound variable` (exit 127); the rewrite printed nothing at all (exit
  127). The sourced script that exits behaved the same way (exit 4, empty). The error text
  is kept only in a run file whose name Claude is never told. `skip_reason`
  (output_cap.py:196-215) catches a literal `exit`, `exec` and `set -e`, but not these
  cases. A timeout that kills the whole process tree would lose the output the same way.
  A plain kill on Windows left the msys shell running to the end, so this part is
  unverified.
- **The command does not run when the run folder is missing or F: is full.** The folder is
  made when the hook runs (output_cap.py:247), but the redirect `{ } > "$__oc_o"` opens the
  file only when the command runs. If the folder is gone by then, bash skips the command:
  measured exit 1, `No such file or directory`, and the command never ran. The folder can
  disappear through retention, the drive filling, or F: being away.

  On a full drive the command runs, but its writes fail. Python exits 120 on a failed
  flush, so behaviour changes. This matters here because F: often sits at its 20 GB floor
  (handover, 17 Nov).

  `decide()` checks only that F:/LedgerTools/tmp exists (output_cap.py:350), not the
  free space.
- **Failing output is capped hard.** A failing command's stderr shows only 6 head and 6 tail
  lines, 600 characters each (output_cap.py:65). An error in the middle of long stderr is
  hidden. The exit code still comes back, so a failure never looks like a success.
- **Unverified.** Claude Code decides that grep, find and diff exiting 1 is not a failure,
  and whether a command may move to the background, from the command text (research note,
  answers 1 and 2). The rewritten text begins `__oc_o=`, so `grep` with no match may now be
  reported as an error.

**(2) Can a bug in the hook block all work?**

Inside Python it cannot. hook() (output_cap.py:359-370) catches every Exception and exits
0. These four inputs each gave exit 0 and no output:
- `[1]`;
- `tool_input` as a list;
- `command` as a number;
- `file_path` as a number.

The JSON written back is ASCII. One path does block, outside Python. When
tools/output_cap.py is missing, `python <missing file>` exits **2** (measured). For a
PreToolUse hook, exit 2 refuses the call, so every Bash, PowerShell and Read call would be
refused. That includes the git command needed to get the file back. This can happen
mid-rebase, with a stash holding the file, or after a checkout where settings.json carries
the hook but the tool is absent (fix 3).

A very large file (gigabytes, over 100 KB) makes `outline()` scan the whole file. Past 10 s
Claude Code times the hook out and the call runs anyway, so it fails open, only slowly.

**(3) Writes, and the retention shelf.**

The hook writes only under BASE: F:/LedgerTools/tmp/tool-output/<date>/ and .../log/
(output_cap.py:58, 82, 246). The self-test writes a sibling folder,
F:/LedgerTools/tmp/tool-output-selftest-xxxxxx, and removes it (output_cap.py:386, 539).
If F: is missing it falls back to the system temp folder on C:, which is small and
removed.

F:/LedgerTools/tmp is in storage-map.json (line 685, shelf "working"). It is also in
retention.json's "voice tests and scratch" rule (age 7 days, line 125). prune_old removes
old date folders whole.

**But retention's deletion is still switched off** (commit 93a05b206: "still off"). Run
files and logs therefore pile up until it is switched on. The docstring
(output_cap.py:38-39) says they are pruned. A smaller point: storage-map.json says
"14 days" for this folder, against retention.json's 7. That mismatch is not this tool's
fault.

**(4) Refusals of ordinary commands.**

Replay of real calls: 7 refusals in 6,675 calls, 4 distinct commands, 2 of them wrong.
`git log`, `grep -rn foo tools` and `find . -name` all pass. The wrong refusals:
- `sed -i 's#...find more own leftovers ...#' HANDOVER.md` was refused. `segments()`
  (output_cap.py:116-120) splits text inside quotes at `;`, so a fragment of prose starting
  with "find" counts as a `find` command. Reproduced with `grep -rn "a; find ." tools`.
- `for f in $(find . -name command.txt | head -5); do ...; cat $f; done` was refused,
  although the list is already limited to five by `head`.

Wrong refusals found by constructed tests:
- `find tmp -type f -exec rm {} +` is refused, although it prints nothing. Only an -exec
  of a filter word counts (output_cap.py:161-162).
- In PowerShell, `Remove-Item $dir -Recurse -Force`, `Copy-Item $dir -Destination ...
  -Recurse` and `Get-ChildItem ... -Recurse -File | Remove-Item` are all refused. The
  pattern PS_RECURSE (output_cap.py:181) matches the variable `$dir` as the `dir` command,
  and treats a pipe into Remove-Item as no filter. `Get-ChildItem -Recurse *.cs` (second
  word is a positional -Filter) is refused too.
- A loop body that writes to a file (`cat "$f" >> "$2"`, from a project script) counts as
  "cats many files". The check that follows `cat` (output_cap.py:172) sees only a `>`
  straight after `cat`.

**(5) Snippet.**

It adds only `PreToolUse` and says the three existing hooks (UserPromptSubmit,
PostToolUse, Stop) stay as they are. Hook entries merge, so nothing is replaced. The matcher
`Bash|PowerShell|Read` and the 10 s timeout are sound. It lacks the guard against exit 2
(fix 3). page_read_hook.sh reacts only to ArtifactData, so capped Bash output does not
affect it.

## Faults ranked, with the exact fix

1. **The output and error vanish when the shell exits inside the group** (high; 1). Set an
   EXIT/TERM/INT/HUP trap before the group that shows both files once. In wrap()
   (output_cap.py:236), before `{`, add:
   `__oc_done=0; __oc_fin() { [ "$__oc_done" = 1 ] && return; __oc_done=1; __oc_show "$__oc_o" 60 6000 25 2500; __oc_show "$__oc_e" 12 1500 6 600 >&2; }; trap '__oc_fin' EXIT; trap '__oc_fin; exit 143' TERM HUP INT`
   After the group, use `__oc_rc=$?; trap - EXIT TERM HUP INT; __oc_fin; __oc_ret $__oc_rc`.
   Add `trap` to skip_reason so a command that sets its own trap passes through. Add
   self-test cases for `set -u`, `${X:?}` and a sourced `exit 4`: the error text shown and
   the code kept.
2. **The command is skipped or changed when the run folder is missing or F: is full**
   (high; 1).
   - In decide() (output_cap.py:350), skip with a logged `skip:low-space` when
     `shutil.disk_usage(SHELF_ROOT).free < 2 GB`.
   - In wrap(), make the redirect fall back to a plain run:
     `if mkdir -p "${__oc_o%/*}" 2>/dev/null && : > "$__oc_o" 2>/dev/null && : > "$__oc_e" 2>/dev/null; then <group as now>; else { cmd
     }; fi`.
     Simpler alternative: emit the `{ cmd }` group twice, behind that test.
   - Add a self-test case that deletes the date folder between hook and run. The command
     must still run.
3. **A missing tool file exits 2 and refuses every call** (high; 2). In the snippet, make
   the command
   `python "$CLAUDE_PROJECT_DIR/tools/output_cap.py" hook || true`
   (shell form runs under Git Bash; the tool always exits 0 itself, so nothing is lost).
4. **Wrong refusals** (medium; 4). Make these four changes:
   - Before segments() in refuse_bash, blank out quoted text:
     `cmd = re.sub(r"'[^']*'|\"(\\.|[^\"\\])*\"", "''", cmd)`. skip_reason already does this
     at output_cap.py:203.
   - Count any `-exec`, `-execdir`, `-ok`, `-print0` or `-fprint` as a filter
     (output_cap.py:161-163).
   - In the loop rule, count a list that contains `| head` as few, and any `>` in the body
     as a filter.
   - For PowerShell, anchor PS_RECURSE to the start of a pipeline:
     `(^|[;|\n(]\s*)(Get-ChildItem|gci|dir|ls)\b`. Count any later pipeline stage other
     than Sort-Object, Format-* and Out-String as a filter, and a second positional
     argument as a -Filter.

   Add each of the wrong refusals above to the self-test's allowed list.
5. **Failing output capped to 6+6 stderr lines** (medium; 1). When `__oc_rc` is not 0, show
   stderr with the stdout budget (60 / 6000 / 25 / 2500), and put `exit N` in the cap line.
6. **Claude Code's command-name rules may misread the rewrite** (medium, unverified; 1).
   The live trial named in the research must also check four things:
   - `echo a | grep zzz` still shows as a non-error;
   - no "hook changed this call's input" refusal in auto mode;
   - `cd` carries over in the main session;
   - a 10-minute timeout leaves output Claude can see.

   There are no deny rules today. If one is ever added, check that the rewrite (text
   beginning `__oc_o=`) does not slip past it.
7. **Run files never pruned while retention is off** (low; 3). Either wait for retention to
   go on, or let the hook remove date folders under BASE older than 7 days, at most once a
   day: a stamp file in BASE, a few milliseconds. Correct the docstring
   (output_cap.py:38-39) in the meantime.
8. **Binary files over 100 KB refused with a junk outline** (low; 2). The test file was
   300 KB of random bytes saved as `blob.fbx`: refused, with "2299 lines" reported. In
   check_read (output_cap.py:292), pass a file whose first 8 KB holds a NUL byte, and add
   .fbx, .uasset, .wav, .zip and .exe to READ_PASS_EXT.
9. **The log copies up to 240 characters of each command** (low; standing rule on keys).
   Commands are logged at output_cap.py:88. In log(), redact before writing:
   `re.sub(r"(sk-[A-Za-z0-9_-]{8,}|Bearer\s+\S+|(?i)(key|token|secret|password)=\S+)", "[redacted]", detail)`.
