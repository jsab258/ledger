# Review: order items on every start (item_tags), 18 Nov 2026

Reviewed: tools/lane/item_tags.py, kiln_items.json, test_item_tags.py and production/lane/ITEM-TAGS-MERGE-NOTE-2026-11-18.md, against tools/timelog.py, token_audit.py, token_measures.py and the Claude Code hooks reference (code.claude.com/docs/en/hooks.md, read 18 Nov 2026).

## Verdict: PASS WITH FIXES

The tests now number 23, up from 17, and all pass. token_audit's selftest passes 22 of 22. The note's numbers match production/time-log.jsonl: since 9 Nov, 30.2 hours, 16.7 of them tagged (55%); the last line is 17 Nov 14:30.

## Findings

1. Fixed. A compaction (which happens mid-session) or a resume wrote a start line. That cut the running task and could give it a stale current item. With a task open, those two now write nothing. Test added.
2. Fixed. The hooks crashed on a payload that was not a JSON object, on a description that was not text, or on a malformed current-item.json. Every hook failure now exits 0 silently. Test added.
3. Fixed. `kiln-share` dropped the 15% cap that token_measures --kiln-share enforces, which it is meant to replace. Over the cap it now prints "KILN OVER 15%" and fails. Test added.
4. Fixed. The module note described a "helper record (by agent id)" step that the code never runs. The claim is removed, and the merge note calls that matching a follow-up.
5. Fixed. Merge note: the reference says updatedInput "Replaces the entire input object". The hook already sends the whole input, now checked by a test. The test count is corrected.
6. Checked. Attribution matches token_audit's at every minute from 9 to 18 Nov on the real log. A new test adds an unsorted log with overlapping times, a stop with no start, steps on window edges and a "+01:00" offset. Both tools handle these the same way.
7. Open. The two tools treat an open last window differently. item_tags lets it run on with no end, while token_audit drops it ("not in the time log"). After the merge the last line will usually be an automatic start, so the two will disagree, and a start never stopped would take every later step.
8. Open. Search titles report updatedInput being ignored at times for the Agent tool, or when no permission decision is given. The pages were not reached, so this is unverified. The first helper on the PC settles it.
9. Open, small. A second session in the same checkout would share the current item and close the open window.
10. Open, small. A malformed "at" in the time log stops `by-item`, as it already stops token_audit. Suggestion: the SessionStart hook could print the current item, since the reference says that output reaches the session's context.

## For the main session

Merge as the note says, after settling finding 7. The reviewer recommends that both tools end an open window after a set limit (a few hours, estimate). Check finding 8 on the first day.
