"""A Stop hook that sends LEDGER's production session back to work when it ends a turn without handing over.

    (Claude Code runs it at each turn's end, JSON on stdin; installed only on his yes, advisor 97 part 2a, 11 Nov)
    python tools/stop_hook.py --selftest

WHY, 11 November (advisor 97; advisors 64 and 68, 9 Nov): sessions ended turns with work left and no Stopped line, and
the next start waited for the gate's 30 quiet minutes. A Stop hook can refuse the stop: printing
{"decision": "block", "reason": ...} makes the session carry on with the reason as its instruction (Claude Code hooks).

WHEN IT BLOCKS, all of these:
- the turn is the production session's: the chat OPENED as a run of the scheduled task (its first user message begins
  <scheduled-task name="ledger-daily-fresh-session") AND the gate's first line in it begins "GO ". Fixed 11 Nov: the old
  test (the task's name anywhere in the first 400 KB) also held his own chats that had read the task file, and would
  have sent every WAIT run of the 15-minute task back to "carry on with the handover's next steps" beside the live
  session. WAIT runs, rehearsals, his chats and helpers are never held;
- stop_hook_active is false (the guard: a turn the hook already sent back is let go, so it can never loop);
- HANDOVER.md's Stopped line is older than its Started line (this session has not handed over).
Otherwise it prints nothing and the stop goes ahead.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HANDOVER = os.path.join(ROOT, "production", "handover", "HANDOVER.md")
OPENING = '<scheduled-task name="ledger-daily-fresh-session"'
GATE_LINES = ("GO ", "WAIT ", "REHEARSAL GO", "REHEARSAL WAIT")
SCAN_LINES = 3000  # the opening and the gate's line sit in a run's first few dozen log lines
REASON = ("The production session ended a turn without handing over. If work remains, carry on with the handover's next "
          "steps. If history_check said OVER at an item's end, rewrite HANDOVER.md, set its Stopped line from Get-Date, "
          "commit it with the work and stop.")


def stamp(text, label):
    m = re.search(r"^\*\*%s:\*\*\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})" % label, text, re.M)
    return m.group(1) if m else ""


def handed_over(text):
    """True when the Stopped line is at or after the Started line (both 'YYYY-MM-DD HH:MM', so text order is time order)."""
    started, stopped = stamp(text, "Started"), stamp(text, "Stopped")
    return bool(stopped) and stopped >= started


def _texts(content):
    """The text pieces of a message's content (a string, or a list of text / tool_result parts)."""
    if isinstance(content, str):
        return [content]
    out = []
    for part in content or []:
        if not isinstance(part, dict):
            continue
        if part.get("type") == "text":
            out.append(part.get("text", ""))
        elif part.get("type") == "tool_result":
            out.extend(_texts(part.get("content")))
    return out


def is_production(lines):
    """True only for a run of the scheduled task whose gate said GO. lines: the log's JSONL lines."""
    opened = None
    for n, line in enumerate(lines):
        if n >= SCAN_LINES:
            return False
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        if entry.get("type") != "user" or entry.get("isMeta"):
            continue
        content = (entry.get("message") or {}).get("content")
        if opened is None:
            words = [t for t in _texts(content) if t.strip()]
            if not words:
                continue
            opened = words[0].lstrip().startswith(OPENING)
            if not opened:
                return False  # his own chat or a helper: never held
            continue
        for part in content if isinstance(content, list) else []:
            if isinstance(part, dict) and part.get("type") == "tool_result":
                text = " ".join(_texts(part.get("content"))).lstrip()
                if text.startswith(GATE_LINES):
                    return text.startswith("GO ")
    return False


def is_production_log(transcript_path):
    try:
        with open(transcript_path, encoding="utf-8", errors="replace") as fh:
            return is_production(fh)
    except OSError:
        return False


def decide(event, handover_text, production):
    if event.get("stop_hook_active"):
        return None
    if not production:
        return None
    if handed_over(handover_text):
        return None
    return {"decision": "block", "reason": REASON}


def main():
    if "--selftest" in sys.argv:
        return selftest()
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0
    try:
        with open(HANDOVER, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return 0
    out = decide(event, text, is_production_log(event.get("transcript_path", "")))
    if out:
        print(json.dumps(out))
    return 0


def selftest():
    h_open = "**Started:** 2026-11-11 11:22 (hourly run)\n**Stopped:** 2026-11-11 10:25 (x)\n"
    h_done = "**Started:** 2026-11-11 11:22 (hourly run)\n**Stopped:** 2026-11-11 13:05 (x)\n"
    cases = [
        ("open session, production", {"stop_hook_active": False}, h_open, True, "block"),
        ("guard: already sent back once", {"stop_hook_active": True}, h_open, True, None),
        ("handed over", {"stop_hook_active": False}, h_done, True, None),
        ("his own chat", {"stop_hook_active": False}, h_open, False, None),
        ("no Stopped line yet", {"stop_hook_active": False}, "**Started:** 2026-11-11 11:22\n", True, "block"),
    ]
    bad = 0
    for name, ev, txt, prod, want in cases:
        got = decide(ev, txt, prod)
        got = got and got["decision"]
        if got != want:
            bad += 1
            print("stop_hook selftest FAIL %s: got %r want %r" % (name, got, want))

    run = OPENING + ' file="x">This is an automated run ... work as LEDGER\'s one production session'

    def log(first, gate=None, tool=None, meta=False, as_parts=False):
        rows = [{"type": "queue-operation", "content": run}]
        if meta:
            rows.append({"type": "user", "isMeta": True, "message": {"content": "<system-reminder>x</system-reminder>"}})
        rows.append({"type": "user", "message": {"content": [{"type": "text", "text": first}] if as_parts else first}})
        rows.append({"type": "assistant", "message": {"content": [{"type": "tool_use", "input": {}}]}})
        if tool:
            rows.append({"type": "user", "message": {"content": [{"type": "tool_result", "content": tool}]}})
        if gate:
            rows.append({"type": "user", "message": {"content": [
                {"type": "tool_result", "content": [{"type": "text", "text": gate}]}]}})
        return [json.dumps(r) for r in rows]

    prod_cases = [
        ("run, gate GO", log(run, "GO the last session stopped at 15:19; no turn written for 37 minutes"), True),
        ("run, gate WAIT", log(run, "WAIT the last session (started 11 Nov 17:22) has not stopped"), False),
        ("run, REHEARSAL GO", log(run, "REHEARSAL GO the rehearsal"), False),
        ("run, REHEARSAL WAIT", log(run, "REHEARSAL WAIT x"), False),
        ("run, gate not yet run", log(run), False),
        ("run as text parts after a meta line, GO", log(run, "GO x", meta=True, as_parts=True), True),
        ("run, a file read before the gate, GO", log(run, "GO x", tool="# Handover ... WAIT for it"), True),
        ("his chat naming the task and its goal line", log(
            "Change my scheduled task ledger-daily-fresh-session: work as LEDGER's one production session", "GO x"), False),
        ("his chat whose tool result shows a run's opening and GO", log("hello", tool=run + "\nGO x"), False),
    ]
    for name, lines, want in prod_cases:
        got = is_production(lines)
        if got != want:
            bad += 1
            print("stop_hook selftest FAIL %s: got %r want %r" % (name, got, want))
    total = len(cases) + len(prod_cases)
    print("stop_hook selftest: passed=%d/%d failed=%d" % (total - bad, total, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
