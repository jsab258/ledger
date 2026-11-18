# Order items on every start: merge note for the main session (18 Nov 2026)

Blind-spots recommendation 4, adopted by Jafar 18 Nov 08:05 (advisor 218): every session and helper start writes its order item into the time log automatically, and the hourly spend is split by item. Written by the cloud lane; nothing here is merged. Code: tools/lane/item_tags.py, tools/lane/kiln_items.json, tools/lane/test_item_tags.py (23 tests pass here; one reads the real time log).

## Why now

- The time log's last line is 17 Nov 14:30 (read 18 Nov 08:36). Every step since then is "not in the time log".
- Since 9 Nov the log holds 30.2 hours, of which 16.7 (55%) carry an item code (measured from production/time-log.jsonl by the new reader; the review's 40% counted differently, the whole-log figure is in tools/lane/forecast.py's note).
- Kiln's share is counted by task name (KILN in tools/token_measures.py: "kiln" or "tool loop"), so Kiln work logged under another name is missed and a task that only mentions Kiln is counted as Kiln. The 08:09 row calls the 22.9% an undercount.

## What it does

1. `python tools/lane/item_tags.py set n16-1` writes production/current-item.json. The session runs it each time it takes up an item (one line; the handover's start steps should say so).
2. SessionStart hook: writes a start line into production/time-log.jsonl with a new "item" field, task "<item> session <source> (auto)". No current item: "untagged", so the gap shows instead of hiding. A compaction or resume while a task is open writes nothing, so the running task is neither cut nor retagged.
3. PreToolUse hook on the Agent tool: if the helper's description and prompt name no item, the description gets "[<current item>] " in front (through the hook's updatedInput), so the helper's log metadata, which token_audit already reads, carries the item. If only the prompt names one, that code goes in front. Each helper start is also recorded in production/helper-items.jsonl.
4. `by-item --since HH:MM`: the hourly row's split, for example "By item since 07:15 (US$4.25): n16-1 US$3.00; n16-6 US$1.25".
5. `kiln-share [date]`: Kiln by item code (kiln_items.json: n16-1 and n09-6, the clothing item closed into it), with the untagged dollars shown beside it, so an undercount is visible. Over 15% it prints "KILN OVER 15%" and fails, as token_measures --kiln-share does.

Attribution order for a step: the helper's own item code, then the time-log window open at that moment (its "item" field, else the code in its task name), then the current item for steps after the log's last line (labelled "inferred"), else untagged.

## Why helper lines are not in the time log itself

token_audit.task_windows closes the open task on any line, whatever its event. A helper line in the time log would cut the session's own window. So helper starts go to production/helper-items.jsonl. If the main session prefers one file, the change is one line in task_windows (only "start" and "stop" close a window) and the same in item_tags.windows; then the helper lines can move into the time log.

## To merge (main session, about 1 hour, estimate)

1. Copy item_tags.py into tools/ (or import it from tools/lane/), and kiln_items.json beside it. Run the tests.
2. Hooks in .claude/settings.json, beside the existing ones:
   - "SessionStart": command `python "$CLAUDE_PROJECT_DIR/tools/lane/item_tags.py" hook-session`, timeout 10.
   - "PreToolUse" with matcher "Agent|Task": command `python "$CLAUDE_PROJECT_DIR/tools/lane/item_tags.py" hook-helper`, timeout 10.
   The hooks never block a start: a bad payload or a file error exits 0 with no output. The Claude Code hooks reference (code.claude.com/docs/en/hooks, read 18 Nov 2026) documents SessionStart's source values (startup, resume, clear, compact, fork), the agent_id field when a hook fires inside a helper, and PreToolUse's updatedInput under hookSpecificOutput. The reference says updatedInput replaces the whole input, so the hook sends every field back with only the description changed (checked by a test). Bug reports found by search (titles only, pages not reached) say updatedInput has at times been ignored for the Agent tool or without a permission decision: unverified until the first helper on the PC shows "[n16-x]" in its description. If it does not, the record in helper-items.jsonl still holds the item, but attribution does not read that file yet: matching it to the helper's log is a follow-up.
3. tools/timelog.py: `start` writes an "item" field, taken from `--item`, else the code in the task's name, else current-item.json; `start` also runs set_current, so the two never disagree.
4. tools/token_measures.py: `--kiln-share` calls item_tags (by item code) instead of the KILN name pattern; the hourly `--spend` line adds item_tags.hourly_line. The old name count can stay one week beside it, so the switch is seen.
5. Kiln's share is then counted by n16-1 and every later Kiln item: add each to kiln_items.json when an order names one.
6. Retention: production/helper-items.jsonl and production/current-item.json are small text; check production/retention.json names production/ for them.

## Checks once merged

- The first session start after the merge writes a time-log line with "item".
- The first helper shows "[n16-x]" in its description in the session log's metadata.
- `kiln-share` and the old `--kiln-share` both print for one week; the untagged share falls under 10% within a day (target, estimate).

## Added after the review (18 Nov)

An open window (a start with no later line) now ends after 4 hours (OPEN_LIMIT_H, an estimate), so a start never stopped cannot take every later step; steps after that fall to the current item, labelled inferred. token_audit drops an open window entirely ("not in the time log"). On merge, give both tools the same limit.
