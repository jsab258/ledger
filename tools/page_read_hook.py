#!/usr/bin/env python3
"""After each tool call: has his page been read within the last 45 minutes?

His ruling of 2 November: the page's answers are read at least once an hour
while working; the advisor channel with them (4 November). Claude Code runs this
as a PostToolUse hook, through its faster front page_read_hook.sh (.claude/settings.json).
It notes every read of the page's
verdicts and advisor collections in .claude/page-read-stamp.json, and when either
is over 45 minutes old it tells the production session to read them before its
next step. Silent otherwise, so it costs no tokens when the reads are on time.

It stays silent for helpers, for the fresh-session gate's own run (a WAIT must
read nothing else), and whenever the handover says no session is working. Any
fault of its own is swallowed: it must never stop the work.
"""
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAMP = ROOT / ".claude" / "page-read-stamp.json"
HANDOVER = ROOT / "production" / "handover" / "HANDOVER.md"
PAGE_ID = "1VZHkCBAHdw8HBdNHrByL8"
COLLECTIONS = ("verdicts", "advisor")
LIMIT_S = 45 * 60


def session_working() -> bool:
    """Started later than Stopped in the handover: a production session is on."""
    text = HANDOVER.read_text(encoding="utf-8")
    started = re.search(r"^\*\*Started:\*\* (\S+ \S+)", text, re.M)
    stopped = re.search(r"^\*\*Stopped:\*\* (\S+ \S+)", text, re.M)
    if not started:
        return False
    return not stopped or started.group(1) > stopped.group(1)


def load_stamps() -> dict:
    try:
        return json.loads(STAMP.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def run(event: dict, now: float) -> str:
    """The reminder to give, or '' for silence; records a page read if this was one."""
    if event.get("agent_id"):
        return ""
    tool = event.get("tool_name", "")
    given = event.get("tool_input") or {}
    if tool == "PowerShell" or tool == "Bash":
        if "fresh_gate.py" in str(given.get("command", "")):
            return ""
    stamps = load_stamps()
    if (
        "ArtifactData" in tool
        and PAGE_ID in str(given.get("url", ""))
        and given.get("collection") in COLLECTIONS
        and given.get("action") in ("list", "query", "get")
    ):
        stamps[given["collection"]] = now
        STAMP.write_text(json.dumps(stamps), encoding="utf-8")
        oldest = min(stamps.get(c, 0) for c in COLLECTIONS)
        os.utime(STAMP, (oldest, oldest))  # the shell's fast path reads this time
    if not session_working():
        return ""
    late = [c for c in COLLECTIONS if now - stamps.get(c, 0) > LIMIT_S]
    if not late:
        return ""
    return (
        "His ruling of 2 November: over 45 minutes since his page was read. If you are "
        "the production session, before your next step read these collections of "
        f"https://claude.ai/artifact/{PAGE_ID} through ArtifactData: {', '.join(late)}; "
        "act on anything new. A helper ignores this."
    )


def main() -> None:
    try:
        text = run(json.load(sys.stdin), time.time())
    except Exception:  # never stop the work over a reminder
        return
    if text:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PostToolUse", "additionalContext": text}}))


if __name__ == "__main__":
    main()
