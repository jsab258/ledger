#!/usr/bin/env python3
"""HOW MANY TOKENS A FRESH SESSION READS BEFORE ITS FIRST ITEM, BY SOURCE. Read from its own session log.

    python tools/start_size.py <session-log-id or path> [<another> ...]
    python tools/start_size.py --selftest

WHY, 4 November 2026 (his ruling A1): "Make the start lean: measure what a fresh session reads before its first item
(its first steps' input tokens, by source), then cut it to well under 80,000 tokens ... Tell me the start's size before
and after."

WHAT IT COUNTS: the first step's context (what the app loads before the session does anything), split into the parts the
log records (the skill list, CLAUDE.md with the memory index, the deferred tool names, the servers' instructions, the
helper list, the task's own prompt; characters / 3.6, marked estimated) and the rest, the app's own system prompt and tool
schemas, which no file of ours sets. Then each later step's growth in context (fresh input + cache reads + cache writes,
as token_audit.py counts a step) is laid to the tool calls of the step before it, shared by their results' lengths: a
file read, a skill loaded, his page, a tool's schema. THE START ENDS at the first Edit or Write of any file but the
handover (the first item's first change), or at --steps.
"""
import json
import os
import re
import sys
from collections import OrderedDict

LOGS = os.path.join(os.path.expanduser("~"), ".claude", "projects", "C--Users-Jafar-ledger-local")
CHARS_PER_TOKEN = 3.6
START_FILES = re.compile(r"HANDOVER\.md$", re.I)
ATTACH = {"skill_listing": "the skill list", "instructions": "CLAUDE.md and the memory index",
          "deferred_tools_delta": "deferred tool names", "mcp_instructions_delta": "servers' instructions",
          "agent_listing_delta": "helper list", "session_context": "session context"}


def ctx_of(u):
    return (u.get("input_tokens", 0) or 0) + (u.get("cache_read_input_tokens", 0) or 0) + (u.get("cache_creation_input_tokens", 0) or 0)


def label(name, inp):
    if name in ("Read", "Edit", "Write"):
        p = inp.get("file_path", "")
        return "read " + os.path.basename(p) if name == "Read" else name.lower() + " " + os.path.basename(p)
    if name in ("Bash", "PowerShell"):
        cmd = inp.get("command", "")
        files = re.findall(r"[\w.-]+\.(?:md|json|jsonl|txt|py|ps1)\b", cmd)
        return "shell " + (" ".join(OrderedDict.fromkeys(files)) if files else cmd.strip().split("\n")[0][:40])
    if name == "Skill":
        return "skill " + inp.get("skill", "")
    if name == "ToolSearch":
        return "tool schemas " + inp.get("query", "").replace("select:", "")[:60]
    if name == "ArtifactData":
        return "his page's answers"
    if name == "Artifact":
        return "page " + (inp.get("action") or "publish") + " " + os.path.basename(inp.get("file_path") or inp.get("url") or "")
    if name.startswith("mcp__ccd_turn__"):
        return "task list"
    return name.split("__")[-1]


def measure(path, steps=None):
    first_user, attach, msgs, results = None, {}, [], {}
    seen = {}
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            t = d.get("type")
            if t == "attachment" and not msgs:
                a = d.get("attachment") or {}
                k = ATTACH.get(a.get("type"))
                if k:
                    attach[k] = attach.get(k, 0) + len(json.dumps(a, ensure_ascii=False))
            elif t == "user":
                c = (d.get("message") or {}).get("content")
                if first_user is None and not msgs:
                    first_user = len(c) if isinstance(c, str) else len(json.dumps(c, ensure_ascii=False))
                if isinstance(c, list):
                    for x in c:
                        if x.get("type") == "tool_result":
                            results[x.get("tool_use_id")] = len(json.dumps(x.get("content"), ensure_ascii=False))
            elif t == "assistant":
                m = d.get("message") or {}
                if not isinstance(m, dict) or not m.get("usage"):
                    continue
                mid = m.get("id")
                if mid not in seen:
                    seen[mid] = {"ctx": ctx_of(m["usage"]), "out": m["usage"].get("output_tokens", 0) or 0, "tools": []}
                    msgs.append(seen[mid])
                for c in m.get("content", []):
                    if c.get("type") == "tool_use":
                        seen[mid]["tools"].append((c.get("id"), c.get("name", ""), c.get("input") or {}))
    if not msgs:
        return None
    first = msgs[0]["ctx"]
    parts = OrderedDict()
    est = 0
    for k, n in attach.items():
        parts[k + " (estimated)"] = round(n / CHARS_PER_TOKEN)
        est += round(n / CHARS_PER_TOKEN)
    parts["the task's or his prompt (estimated)"] = round((first_user or 0) / CHARS_PER_TOKEN)
    est += parts["the task's or his prompt (estimated)"]
    parts["the app's own system prompt and tools (the rest)"] = first - est
    reads = OrderedDict()
    end = len(msgs) - 1
    for i, s in enumerate(msgs):
        if steps and i >= steps:
            end = i
            break
        stop = [x for x in s["tools"] if x[1] in ("Edit", "Write") and not START_FILES.search(x[2].get("file_path", ""))]
        if stop:
            end = i
            break
        if i + 1 >= len(msgs):
            break
        grow = max(msgs[i + 1]["ctx"] - s["ctx"], 0)
        if not s["tools"]:
            reads["the session's own words"] = reads.get("the session's own words", 0) + grow
            continue
        lens = [max(results.get(tid, 0), 1) for tid, _, _ in s["tools"]]
        own = min(s["out"], grow)
        reads["the session's own words"] = reads.get("the session's own words", 0) + own
        for (tid, name, inp), n in zip(s["tools"], lens):
            k = label(name, inp)
            reads[k] = reads.get(k, 0) + round((grow - own) * n / sum(lens))
    return {"log": os.path.basename(path), "first_step": first, "parts": parts, "reads": reads,
            "start": msgs[end]["ctx"], "steps": end}


def show(r):
    print(f"{r['log']}: the start {r['start']:,} tokens over {r['steps']} steps; the first step {r['first_step']:,}")
    for k, v in r["parts"].items():
        print(f"  {v:>7,}  {k}")
    for k, v in sorted(r["reads"].items(), key=lambda kv: -kv[1]):
        if v >= 300:
            print(f"  {v:>7,}  {k}")
    small = sum(v for v in r["reads"].values() if v < 300)
    if small:
        print(f"  {small:>7,}  everything under 300 each")


def selftest():
    import tempfile
    lines = [
        {"type": "attachment", "attachment": {"type": "skill_listing", "content": "x" * 3600}},
        {"type": "user", "message": {"content": "y" * 360}},
        {"type": "assistant", "message": {"id": "a", "usage": {"input_tokens": 10000, "output_tokens": 50},
                                          "content": [{"type": "tool_use", "id": "t1", "name": "Read", "input": {"file_path": "C:/x/RULINGS.md"}}]}},
        {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "t1", "content": "z" * 100}]}},
        {"type": "assistant", "message": {"id": "b", "usage": {"input_tokens": 17050, "output_tokens": 20},
                                          "content": [{"type": "tool_use", "id": "t2", "name": "Edit", "input": {"file_path": "C:/x/NOW.md"}}]}},
    ]
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "s.jsonl")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("\n".join(json.dumps(x) for x in lines))
        r = measure(p)
    ok = [r["first_step"] == 10000, r["start"] == 17050, r["reads"].get("read RULINGS.md") == 7000,
          r["parts"]["the skill list (estimated)"] == round(len(json.dumps(lines[0]["attachment"])) / CHARS_PER_TOKEN)]
    print("selftest", "ok" if all(ok) else f"FAILED {ok}")
    return 0 if all(ok) else 1


def main(a):
    if "--selftest" in a:
        return selftest()
    steps = None
    if "--steps" in a:
        steps = int(a[a.index("--steps") + 1])
        a = [x for x in a if x not in ("--steps", str(steps))]
    for x in a:
        p = x if os.path.isfile(x) else next((os.path.join(LOGS, f) for f in os.listdir(LOGS) if f.startswith(x) and f.endswith(".jsonl")), None)
        r = measure(p) if p else None
        if r:
            show(r)
        else:
            print(x, ": no log")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
