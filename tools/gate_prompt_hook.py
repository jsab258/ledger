"""A prompt-submit hook that ends a WAIT run of the hourly task before the model is called.

    (Claude Code runs it on each submitted prompt, JSON on stdin; to be installed in .claude/settings.json only on his yes)
    python tools/gate_prompt_hook.py --selftest

WHY, 15 November (the advisor's efficiency review "eff", 19:46): session starts cost US$15.83 of the day's US$26.12 in
76 runs, one of them working; each WAIT run pays the whole start (about 80,000 tokens written to the cache, US$0.17 to
0.21 on Opus) only for tools/fresh_gate.py to say WAIT. Claude Code's hooks page (code.claude.com/docs/en/hooks, read
15 Nov 2026 about 19:58): a UserPromptSubmit hook receives the submitted text in "prompt"; printing
{"decision": "block"} "stops the prompt before it reaches Claude"; the block message is still written to the session's
transcript, and "suppressOriginalPrompt": true inside hookSpecificOutput leaves the prompt's text out of it; command
hooks on UserPromptSubmit default to a 30 s limit; the event also fires when a scheduled task fires. UNVERIFIED: whether
it fires on the first prompt of a session the desktop app's scheduled task opens; the first real runs after
installation settle it (every call is logged, below).

WHAT IT DOES: only for the task's own prompt (it holds "fresh_gate.py" and the task's name or its opening words), it
runs the gate with this session's id as its own; a line beginning WAIT or REHEARSAL WAIT blocks the prompt and the
session id goes into production/handover/gate-blocked.jsonl, which the gate reads so a blocked run never counts as
activity. GO, REHEARSAL GO, his own messages, helpers' prompts and every error let the prompt through: on any fault the
run behaves exactly as before the hook (the model runs the gate itself).
"""
import datetime
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, "tools", "fresh_gate.py")
BLOCKED = os.path.join(ROOT, "production", "handover", "gate-blocked.jsonl")
MARKS = ("ledger-daily-fresh-session", "FIRST, AND NOTHING ELSE BEFORE IT")
GATE_LIMIT_S = 25


def is_task_prompt(prompt):
    return isinstance(prompt, str) and "fresh_gate.py" in prompt and any(m in prompt for m in MARKS)


def own_id(event):
    tp = event.get("transcript_path") or ""
    base = os.path.basename(tp)
    return base[:-6] if base.endswith(".jsonl") else (event.get("session_id") or "")


def run_gate(own):
    env = dict(os.environ, CLAUDE_CODE_SESSION_ID=own)
    out = subprocess.run([sys.executable, GATE], cwd=ROOT, env=env, capture_output=True, text=True,
                         timeout=GATE_LIMIT_S, encoding="utf-8", errors="replace")
    lines = [l for l in out.stdout.splitlines() if l.strip()]
    return lines[0].strip() if lines else ""


def record(own, line, blocked, seconds, path=BLOCKED):
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "session": own,
                             "blocked": blocked, "seconds": round(seconds, 2), "gate": line[:300]}) + "\n")


def decide(event, gate=run_gate, log=record):
    """The JSON to print, or None to let the prompt through."""
    if not is_task_prompt(event.get("prompt")):
        return None
    own = own_id(event)
    t0 = time.time()
    line = gate(own)
    blocked = line.startswith(("WAIT ", "REHEARSAL WAIT"))
    log(own, line, blocked, time.time() - t0)
    if not blocked:
        return None
    return {"decision": "block", "reason": "LEDGER gate: " + line[:300],
            "hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "suppressOriginalPrompt": True}}


def selftest():
    task = '<scheduled-task name="ledger-daily-fresh-session">FIRST, AND NOTHING ELSE BEFORE IT ... python tools/fresh_gate.py'
    logged = []
    lg = lambda *a: logged.append(a)
    ev = lambda p: {"prompt": p, "transcript_path": "C:/x/abc-123.jsonl", "session_id": "abc-123"}
    cases = [
        ("WAIT blocks", decide(ev(task), lambda o: "WAIT a stated quiet spell", lg) is not None, True),
        ("REHEARSAL WAIT blocks", decide(ev(task), lambda o: "REHEARSAL WAIT x", lg) is not None, True),
        ("GO passes", decide(ev(task), lambda o: "GO the last session stopped", lg), None),
        ("REHEARSAL GO passes", decide(ev(task), lambda o: "REHEARSAL GO x", lg), None),
        ("his message passes, gate not run", decide(ev("how is Tom's jumper?"), lambda o: 1 / 0, lg), None),
        ("a chat quoting the gate passes", decide(ev("run python tools/fresh_gate.py"), lambda o: "WAIT x", lg), None),
        ("an empty gate line passes", decide(ev(task), lambda o: "", lg), None),
        ("own id from the transcript", own_id(ev(task)), "abc-123"),
        ("the block hides the prompt", decide(ev(task), lambda o: "WAIT y", lg)["hookSpecificOutput"]["suppressOriginalPrompt"], True),
    ]
    bad = [(n, g, w) for n, g, w in cases if g != w]
    for n, g, w in bad:
        print("FAIL", n, "got", g, "want", w)
    print("selftest", "failed=%d" % len(bad) if bad else "failed=none", "(%d cases)" % len(cases))
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    try:
        event = json.load(sys.stdin)
        out = decide(event)
    except Exception:  # fail open: the run then behaves as before the hook
        return 0
    if out:
        print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
