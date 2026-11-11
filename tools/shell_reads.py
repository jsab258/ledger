#!/usr/bin/env python3
"""SHELL OUTPUT BY COMMAND AND PICTURES READ IN A WINDOW, FROM THIS PC'S SESSION LOGS (advisor 11 Nov 19:45, items 2 and 3).

    python tools/shell_reads.py --from "2026-11-11 19:00" --until "2026-11-12 19:00"
    python tools/shell_reads.py --selftest

Measures only. Counts every Bash and PowerShell result of the session and its helpers whose call was made in the window:
its tokens (characters / 4, as token_measures) under the command's first word (after cd ... && and env settings), and every
picture block in any tool result (the DAILY file's row 9). Baseline, this tool on 10 Nov 14:30 to 11 Nov 14:30, session and
helpers: shell 712,539 tokens in 1,820 calls; file reading 424,185 in 691 (sed 155k, cat 123k, grep 116k); pictures 287 (the
DAILY file's own count, matched). The 11 Nov DAILY file's 238,000 in 398 was a narrower scratch count (session, to midday).
"""
import argparse
import collections
import datetime
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from token_audit import swiss  # noqa: E402
from token_measures import result_tokens  # noqa: E402
from fresh_gate import LOGS  # noqa: E402

SHELLS = ("Bash", "PowerShell")
READERS = ("sed", "grep", "cat", "head", "tail", "Get-Content", "Select-String", "rg", "awk")
LEAD = re.compile(r"^\s*(?:cd\s+[^&;]+(?:&&|;)\s*|unset\s+\S+\s*;\s*|[A-Z_]+=\S+\s+|export\s+[^;&]+(?:&&|;)\s*)*")


def first_word(cmd):
    rest = LEAD.sub("", cmd or "", count=1)
    m = re.match(r"\s*([^\s|;&()]+)", rest)
    return os.path.basename(m.group(1)) if m else "?"


def scan(path, since, until, calls, toks, pics):
    pending = {}
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"tool_use"' in line and '"assistant"' in line:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                if d.get("type") != "assistant" or not d.get("timestamp"):
                    continue
                t = swiss(d["timestamp"])
                for c in (d.get("message") or {}).get("content") or []:
                    if isinstance(c, dict) and c.get("type") == "tool_use":
                        word = first_word((c.get("input") or {}).get("command")) if c.get("name") in SHELLS else None
                        pending[c.get("id")] = (since <= t < until, word)
            elif '"tool_result"' in line:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                content = (d.get("message") or {}).get("content")
                for c in content if isinstance(content, list) else []:
                    if not (isinstance(c, dict) and c.get("type") == "tool_result"):
                        continue
                    inside, word = pending.pop(c.get("tool_use_id"), (False, None))
                    if not inside:
                        continue
                    tok, pic = result_tokens(c.get("content"))
                    if pic:
                        pics[0] += sum(1 for x in c.get("content") or [] if isinstance(x, dict) and x.get("type") == "image")
                    if word:
                        calls[word] += 1
                        toks[word] += tok


def measure(since, until, logs=LOGS):
    calls, toks, pics = collections.Counter(), collections.Counter(), [0]
    lo = since.timestamp() - 86400
    paths = glob.glob(os.path.join(logs, "*.jsonl")) + glob.glob(os.path.join(logs, "*", "subagents", "*.jsonl"))
    for p in paths:
        if os.path.getmtime(p) >= lo:
            scan(p, since, until, calls, toks, pics)
    return calls, toks, pics[0]


def report(calls, toks, pics, since, until):
    rd = [w for w in toks if w in READERS]
    print("Shell output %s to %s: %d tokens in %d calls; file reading (%s) %d tokens in %d calls; pictures read %d"
          % (since.strftime("%d %b %H:%M"), until.strftime("%d %b %H:%M"), sum(toks.values()), sum(calls.values()),
             ", ".join(sorted(rd)) or "none", sum(toks[w] for w in rd), sum(calls[w] for w in rd), pics))
    print("| command | calls | tokens |\n|---|---|---|")
    for w, n in toks.most_common(10):
        print("| %s | %d | %d |" % (w, calls[w], n))


def selftest():
    ok = True
    for cmd, want in [("cd /c/x && sed -n 1,5p f", "sed"), ("unset MSYS_NO_PATHCONV; git add a", "git"),
                      ("python tools/a.py", "python"), ("MSYS_NO_PATHCONV=1 /c/x/UnrealEditor.exe", "UnrealEditor.exe"),
                      ("Get-Content f -TotalCount 3", "Get-Content")]:
        got = first_word(cmd)
        print(("ok   " if got == want else "FAIL ") + "%r -> %s" % (cmd, got))
        ok &= got == want
    print("selftest " + ("passed" if ok else "FAILED"))
    return 0 if ok else 1


def main(argv):
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--from", dest="since")
    ap.add_argument("--until")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.since:
        print(__doc__)
        return 2
    since = datetime.datetime.strptime(a.since, "%Y-%m-%d %H:%M")
    until = datetime.datetime.strptime(a.until, "%Y-%m-%d %H:%M") if a.until else datetime.datetime.now()
    report(*measure(since, until), since, until)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
