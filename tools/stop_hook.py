"""A Stop hook that sends LEDGER's production session back to work when it ends a turn without handing over.

    (Claude Code runs it at each turn's end, JSON on stdin; installed only on his yes, advisor 97 part 2a, 11 Nov)
    python tools/stop_hook.py --selftest

WHY, 11 November (advisor 97; advisors 64 and 68, 9 Nov): sessions ended turns with work left and no Stopped line, and
the next start waited for the gate's 30 quiet minutes. A Stop hook can refuse the stop: printing
{"decision": "block", "reason": ...} makes the session carry on with the reason as its instruction (Claude Code hooks).

WHEN IT BLOCKS, all of these:
- the turn is the production session's: its transcript holds the scheduled task's name (ledger-daily-fresh-session) or
  the handover's goal line, so his own chats in this folder and helpers are never held;
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
MARKERS = ("ledger-daily-fresh-session", "work as LEDGER's one production session")
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


def is_production(transcript_path):
    try:
        with open(transcript_path, encoding="utf-8", errors="replace") as fh:
            head = fh.read(400000)
    except OSError:
        return False
    return any(m in head for m in MARKERS)


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
    out = decide(event, text, is_production(event.get("transcript_path", "")))
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
    print("stop_hook selftest: passed=%d/%d failed=%d" % (len(cases) - bad, len(cases), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
