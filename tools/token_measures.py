#!/usr/bin/env python3
"""SIX MEASURES OF A DAY'S SPEND, READ FROM THE SESSION LOGS, FOR THE MORNING'S OVERVIEW. Measures only; nothing is changed by them.

    python tools/token_measures.py 2026-11-05 [--allowance 49]   # a short table for the overview, then the detail
    python tools/token_measures.py --thrown "the hill's second crowns" --since 09:30 [--until 10:10]  # record a try thrown away
    python tools/token_measures.py --selftest

WHY, 5 November 2026 (the advisor's message 11, within his efficiency rulings): 1 failed tries and rework per item; 2 the ten
biggest tool results and pictures' share; 3 the prompt cache; 4 what the app's own tokens at every start are made of and which
the builder never used this week; 5 cycle time; 6 the week's allowance left at Monday 13:00.

WHAT IS REAL AND WHAT IS NOT:
- Dollars are token_audit.py's: the same steps at published API prices, a measure to compare work, not his bill.
- A tool result's tokens are estimated: characters / 4 for text, width x height / 750 for a picture sized as the API sizes it
  (long edge 1,568 px). Its cost is one cache write at the step that took it in, plus a cache read at every later step of
  that log: what carrying it cost, which the bill does not list apart.
- The start's parts are the logged request's own text / 4, tools scaled to the app's usage card (TOOLS_SCALE); "never used" counts
  calls by the session and helpers since Monday. Dropping one may not be ours to do: this measures, it decides nothing.
- A try thrown away cannot be read from a log: nothing marks it. So the session records it (--thrown, at the moment it sets the
  try aside, with the time it began) and its dollars are every step of the session and its helpers in that window. No record: 0, said so.
- Change to verdict: the time from a commit touching the game to the first night walk's start after it, the tester's verdict being
  the walk; a reviewer's later reading of it is not logged.
"""
import base64
import collections
import datetime
import glob
import json
import os
import re
import statistics
import struct
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from token_audit import ROOT, LOGS, TIMELOG, item_at, price_of, step_cost, swiss, task_windows  # noqa: E402

THROWN = os.path.join(ROOT, "production", "research", "token-audit", "thrown-tries.jsonl")
ITEMS = os.path.join(ROOT, "production", "approvals", "needs-you")
ANSWERS = os.path.join(ROOT, "production", "approvals", "answers", "1VZHkCBAHdw8HBdNHrByL8")
WALKS = os.path.join(ROOT, "production", "playtest", "ai-tester")
GAME_PATHS = ["ue-probe/Source", "ue-probe/Config", "production/specs", "production/assets"]
REVIEWER = re.compile(r"review", re.I)
READS = ("Read", "Grep", "Glob")
COMMANDS = ("Bash", "PowerShell")
START_STEPS = 8
# Tools as the model is really charged: the app's usage card, 5 Nov evening, gave 60,861 tokens (system 39,777, MCP 21,084) where the
# logged schemas' characters / 4 give 32,627; the same run's first step, 84,000, agrees with the card, so the tools' figures are scaled
TOOLS_SCALE = 60861 / 32627.0


def picture_tokens(data):
    """A base64 PNG or JPEG's tokens by its size in the header, sized as the API sizes it; a flat guess when unreadable."""
    try:
        raw = base64.b64decode(data[:64000] + "=" * (-len(data[:64000]) % 4))
        w = h = None
        if raw[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = struct.unpack(">II", raw[16:24])
        elif raw[:2] == b"\xff\xd8":
            i = 2
            while i + 9 < len(raw):
                if raw[i] != 0xFF:
                    i += 1
                    continue
                mark = raw[i + 1]
                if mark in (0xC0, 0xC1, 0xC2):
                    h, w = struct.unpack(">HH", raw[i + 5:i + 9])
                    break
                i += 2 + struct.unpack(">H", raw[i + 2:i + 4])[0]
        if w and h:
            scale = min(1.0, 1568.0 / max(w, h))
            return int(w * scale * h * scale / 750)
    except (ValueError, struct.error):
        pass
    return 1500


def result_tokens(content):
    """(tokens, has a picture) of a tool result's content."""
    if isinstance(content, str):
        return len(content) // 4, False
    tokens, pic = 0, False
    for c in content or []:
        if not isinstance(c, dict):
            continue
        if c.get("type") == "image":
            tokens += picture_tokens((c.get("source") or {}).get("data") or "")
            pic = True
        else:
            tokens += len(c.get("text") or "") // 4
    return tokens, pic


def kind_of_result(tool, pic):
    if pic:
        return "picture"
    if tool in READS:
        return "file read"
    if tool in COMMANDS:
        return "command output"
    return "other"


def read_events(path):
    """A log in time order: {steps: [(time, usage, model, context, [tool names])], results: [(step index, tool, tokens, picture)]}."""
    steps, order, names, results = {}, [], {}, []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"assistant"' in line and '"usage"' in line:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                m = d.get("message") or {}
                u = m.get("usage")
                if d.get("type") != "assistant" or not u or m.get("model") == "<synthetic>" or not d.get("timestamp"):
                    continue
                mid = m.get("id") or d.get("uuid")
                if mid not in steps:
                    ctx = (u.get("input_tokens", 0) or 0) + (u.get("cache_read_input_tokens", 0) or 0) + (u.get("cache_creation_input_tokens", 0) or 0)
                    steps[mid] = {"t": swiss(d["timestamp"]), "u": u, "model": m.get("model"), "ctx": ctx, "tools": []}
                    order.append(mid)
                for c in m.get("content") or []:
                    if isinstance(c, dict) and c.get("type") == "tool_use":
                        names[c.get("id")] = c.get("name", "")
                        inp = c.get("input") or {}
                        steps[mid]["tools"].append(c.get("name", "") + ((":" + str(inp.get("skill"))) if c.get("name") == "Skill" else ""))
            elif '"tool_result"' in line:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                if d.get("type") != "user":
                    continue
                content = (d.get("message") or {}).get("content")
                for c in content if isinstance(content, list) else []:
                    if isinstance(c, dict) and c.get("type") == "tool_result":
                        tokens, pic = result_tokens(c.get("content"))
                        results.append((len(order) - 1, names.get(c.get("tool_use_id"), "?"), tokens, pic))
    return {"steps": [steps[m] for m in order], "results": results}


def logs_touched(since):
    """(path, helper's meta or None) of every log written since that day."""
    out = []
    stamp = since.timestamp()
    for main in glob.glob(os.path.join(LOGS, "*.jsonl")):
        sess = main[:-len(".jsonl")]
        if os.path.getmtime(main) >= stamp:
            out.append((main, None))
        for sub in glob.glob(os.path.join(sess, "subagents", "agent-*.jsonl")):
            if os.path.getmtime(sub) >= stamp:
                meta = {}
                try:
                    meta = json.load(open(sub[:-len(".jsonl")] + ".meta.json", encoding="utf-8"))
                except (OSError, ValueError):
                    pass
                out.append((sub, meta))
    return out


def carried_cost(tokens, step_index, steps):
    """One write at the step after the result, then a read at every step after that, at each step's own model's prices."""
    later = steps[step_index + 1:]
    if not later:
        return 0.0
    p, _ = price_of(later[0]["model"])
    return tokens * (p[3] + p[4] * (len(later) - 1)) / 1e6


def measure_day(day):
    since, until = day, day + datetime.timedelta(days=1)
    windows = task_windows(TIMELOG)
    usd = 0.0
    biggest, by_kind = [], collections.Counter()
    tokens = collections.Counter()
    start_write, rewrite = 0.0, 0.0
    write_all, runs, broken, rewrites = 0.0, 0, 0, 0
    rounds = collections.Counter()
    for path, meta in logs_touched(since):
        ev = read_events(path)
        steps = ev["steps"]
        today = [i for i, s in enumerate(steps) if since <= s["t"] < until]
        if not today:
            continue
        for i in today:
            s = steps[i]
            u = s["u"]
            usd += step_cost(u, s["model"])
            p, _ = price_of(s["model"])
            cw, cr, fresh = u.get("cache_creation_input_tokens", 0) or 0, u.get("cache_read_input_tokens", 0) or 0, u.get("input_tokens", 0) or 0
            tokens["read"] += cr
            tokens["write"] += cw
            tokens["fresh"] += fresh
            cost = cw * p[3] / 1e6
            write_all += cost
            if meta is None and i < START_STEPS:
                start_write += cost
            elif meta is None and cw > 30000:
                rewrite += cost
                rewrites += 1
        if meta is None and today[0] == 0:
            runs += 1
            u = steps[0]["u"]
            if (u.get("cache_read_input_tokens", 0) or 0) < 0.5 * max(steps[0]["ctx"], 1):
                broken += 1
        if meta is not None and REVIEWER.search((meta.get("agentType") or "") + " " + (meta.get("description") or "")):
            rounds[item_at(windows, steps[today[0]]["t"])] += 1
        for i, tool, tok, pic in ev["results"]:
            if i < 0 or i >= len(steps) or not since <= steps[i]["t"] < until:
                continue
            kind = kind_of_result(tool, pic)
            cost = carried_cost(tok, i, steps)
            by_kind[kind] += cost
            biggest.append((tok, kind, tool, cost, os.path.basename(path)[:14]))
    biggest.sort(key=lambda b: -b[0])
    return {"usd": usd, "biggest": biggest[:10], "byKind": by_kind, "tokens": tokens, "writeAll": write_all, "startWrite": start_write,
            "rewrite": rewrite, "rewrites": rewrites, "runs": runs, "broken": broken, "rounds": rounds}


def thrown_of(day):
    """[(what, dollars)] of the tries recorded as thrown away that day, every step of the session and its helpers in each window."""
    out = []
    if not os.path.exists(THROWN):
        return out
    since, until = day, day + datetime.timedelta(days=1)
    rows = [json.loads(x) for x in open(THROWN, encoding="utf-8") if x.strip()]
    rows = [r for r in rows if since <= datetime.datetime.fromisoformat(r["from"]) < until]
    if not rows:
        return out
    all_steps = [s for path, _ in logs_touched(since) for s in read_events(path)["steps"]]
    for r in rows:
        a, b = datetime.datetime.fromisoformat(r["from"]), datetime.datetime.fromisoformat(r["to"])
        out.append((r["what"], sum(step_cost(s["u"], s["model"]) for s in all_steps if a <= s["t"] < b)))
    return out


def start_parts(path=None):
    """What the newest log's request is made of: tokens of the system text, each tool (grouped by server), and the first turn's attachments."""
    if path is None:
        mains = [p for p in glob.glob(os.path.join(LOGS, "*.jsonl")) if os.path.getsize(p) < 100 * 1024 * 1024]
        path = max(mains, key=os.path.getmtime)
    parts, servers, tools = collections.Counter(), collections.Counter(), {}
    skills = {}
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"api-request-shape"' in line and not servers:
                d = json.loads(line)
                if d.get("type") != "api-request-shape":
                    continue
                parts["system prompt"] = len(json.dumps(d["shape"].get("system"))) // 4
                for t in d["shape"].get("tools") or []:
                    name = t.get("name", "")
                    tok = int(len(json.dumps(t)) / 4 * TOOLS_SCALE)
                    tools[name] = tok
                    servers[server_of(name)] += tok
            elif '"attachment"' in line and '"rendered"' in line:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                a = d.get("attachment") or {}
                kind = a.get("type")
                if kind == "skill_listing" and not skills:
                    for row in (a.get("content") or "").split("\n"):
                        if row.startswith("- ") and ":" in row:
                            skills[row[2:].split(": ")[0].split(":\n")[0].strip()] = len(row) // 4
                if kind in ("skill_listing", "deferred_tools_delta", "mcp_instructions_delta", "agent_listing_delta", "instructions", "session_context") and kind not in parts:
                    parts[kind] = len(json.dumps(a)) // 4
    return parts, servers, tools, skills


def server_of(name):
    return name.split("__")[1] if name.startswith("mcp__") else "built in"


def used_this_week(day):
    """Tools and skills called since that day's Monday, by the session and helpers, read from every log touched since."""
    monday = day - datetime.timedelta(days=day.weekday())
    used = collections.Counter()
    for path, _ in logs_touched(monday):
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if '"tool_use"' not in line or '"assistant"' not in line or '"api-request-' in line[:40]:
                    continue
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                content = (d.get("message") or {}).get("content") if d.get("type") == "assistant" else None
                for c in content if isinstance(content, list) else []:
                    if isinstance(c, dict) and c.get("type") == "tool_use":
                        used[c.get("name", "")] += 1
                        if c.get("name") == "Skill":
                            used["skill:" + str((c.get("input") or {}).get("skill"))] += 1
                        # the project's skills are mostly read as files by the lean start's "its skill", which counts as use
                        read = re.search(r"skills[/\\]+([^/\\]+)[/\\]+SKILL\.md", str((c.get("input") or {}).get("file_path") or ""))
                        if read:
                            used["skill:" + read.group(1)] += 1
    return used


def ask_minutes(day):
    """[(id, minutes)] from each of his page's asks to his answer, answers dated that day, from the page's items and the night's read-back."""
    items = []
    for f in ("items.json", "archive.json"):
        try:
            d = json.load(open(os.path.join(ITEMS, f), encoding="utf-8"))
        except (OSError, ValueError):
            continue
        items += d.get("items", []) if isinstance(d, dict) else d
    out = []
    for it in items:
        for p in glob.glob(os.path.join(ANSWERS, "**", it.get("id", "?") + ".json"), recursive=True):
            try:
                d = json.load(open(p, encoding="utf-8"))
            except (OSError, ValueError):
                continue
            at = (d.get("data") or d).get("at")
            if not at or not it.get("added"):
                continue
            answered = swiss(at)
            if answered.date() != day.date():
                continue
            try:
                added = datetime.datetime.strptime(it["added"][:16], "%Y-%m-%d %H:%M")
            except ValueError:
                continue
            if answered >= added:  # an item stamped after its answer was written up late: no ask time to read
                out.append((it["id"], (answered - added).total_seconds() / 60))
            break
    return out


def change_to_walk(day):
    """Hours from each commit of that day touching the game to the first night walk's start after it (None while none has run)."""
    walks = []
    for name in os.listdir(WALKS) if os.path.isdir(WALKS) else []:
        m = re.fullmatch(r"(\d{4}-\d\d-\d\d)-(\d\d)(\d\d)", name)
        if m and 1 <= int(m.group(2)) < 5:
            walks.append(datetime.datetime.strptime(name, "%Y-%m-%d-%H%M"))
    walks.sort()
    a = day.strftime("%Y-%m-%d")
    b = (day + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    log = subprocess.run(["git", "log", "--all", "--since=%sT00:00:00" % a, "--until=%sT00:00:00" % b, "--format=%ct", "--"] + GAME_PATHS,
                         cwd=ROOT, capture_output=True, text=True).stdout.split()
    hours = []
    for ct in log:
        t = datetime.datetime.fromtimestamp(int(ct))
        nxt = [w for w in walks if w > t]
        hours.append((nxt[0] - t).total_seconds() / 3600 if nxt else None)
    return hours


def overview(day, allowance=None):
    m = measure_day(day)
    tot = m["usd"] or 1.0
    t = m["tokens"]
    all_in = (t["read"] + t["write"] + t["fresh"]) or 1
    thrown = thrown_of(day)
    parts, servers, tools, skills = start_parts()
    used = used_this_week(day)
    pic = m["byKind"]["picture"]
    carried = sum(m["byKind"].values())
    idle_tools = {n: k for n, k in tools.items() if not used[n]}
    idle_skills = {n: k for n, k in skills.items() if not used["skill:" + n]}
    asks = ask_minutes(day)
    walk = change_to_walk(day)
    known = [h for h in walk if h is not None]
    print("| Measure, %s | Reading |" % day.strftime("%Y-%m-%d"))
    print("|---|---|")
    print("| 1 Tries thrown away, reviewer runs | %s; %d reviewer runs on %d items |" % (
        ("%d, US$%.2f" % (len(thrown), sum(u for _, u in thrown))) if thrown else "none recorded (the record began 5 Nov evening)", sum(m["rounds"].values()), len(m["rounds"])))
    print("| 2 Tool results' carrying cost | US$%.2f of US$%.2f; pictures US$%.2f, %.0f%% of the day (estimated) |" % (carried, tot, pic, 100 * pic / tot))
    print("| 3 Prompt cache | %.1f%% of tokens read from cache; writes US$%.2f, of which starts US$%.2f in %d runs; %d rewrites mid-run US$%.2f; %d runs missed the shared start |" % (
        100 * t["read"] / all_in, m["writeAll"], m["startWrite"], m["runs"], m["rewrites"], m["rewrite"], m["broken"]))
    print("| 4 The start, tokens | tools %d (%d tools), skills' list %d (%d), memory and project files %d, system %d; never used this week: %d tools, %d tokens; %d skills, %d tokens |" % (
        sum(servers.values()), len(tools), parts["skill_listing"], len(skills), parts["instructions"], parts["system prompt"], len(idle_tools), sum(idle_tools.values()), len(idle_skills), sum(idle_skills.values())))
    print("| 5 Cycle time | change to its night walk: %s; his answers: %s |" % (
        ("median %.1f h over %d commits, %d not walked yet" % (statistics.median(known), len(walk), len(walk) - len(known))) if known else ("%d commits, none walked yet" % len(walk)),
        ("median %.0f min over %d" % (statistics.median(u for _, u in asks), len(asks))) if asks else "none dated that day in the read-back"))
    print("| 6 Week's allowance | %s |" % (("%s%% used when read" % allowance) if allowance is not None else "read at Monday 12:50, before its 13:00 reset (the app's usage card)"))
    print()
    print("Biggest tool results (estimated tokens, kind, tool, carrying cost):")
    for tok, kind, tool, cost, log in m["biggest"]:
        print("  %7d %-14s %-28s US$%.3f %s" % (tok, kind, tool[:28], cost, log))
    print("Results' carrying cost by kind: " + ", ".join("%s US$%.2f" % kv for kv in m["byKind"].most_common()))
    print("Reviewer runs by item: " + "; ".join("%s %d" % (k[:50], n) for k, n in m["rounds"].most_common(8)))
    for what, u in thrown:
        print("Thrown: %s US$%.2f" % (what, u))
    print("The start by server (tokens): " + ", ".join("%s %d" % kv for kv in servers.most_common()))
    print("Other parts of the start: " + ", ".join("%s %d" % kv for kv in parts.most_common()))
    print("Tools never used this week, largest first: " + ", ".join("%s %d" % kv for kv in sorted(idle_tools.items(), key=lambda kv: -kv[1])[:20]))
    print("Skills never used this week, largest first: " + ", ".join("%s %d" % kv for kv in sorted(idle_skills.items(), key=lambda kv: -kv[1])[:20]))
    return 0


def record_thrown(a):
    what = a[a.index("--thrown") + 1]
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    frm = "%sT%s:00" % (today, a[a.index("--since") + 1])
    to = ("%sT%s:00" % (today, a[a.index("--until") + 1])) if "--until" in a else datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:00")
    with open(THROWN, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"what": what, "from": frm, "to": to}, ensure_ascii=False) + "\n")
    print("thrown recorded: %s %s to %s" % (what, frm[11:16], to[11:16]))
    return 0


def selftest():
    png = base64.b64encode(b"\x89PNG\r\n\x1a\n" + b"\0\0\0\rIHDR" + struct.pack(">II", 3136, 1568)).decode()
    usage = {"input_tokens": 0, "output_tokens": 0, "cache_read_input_tokens": 100, "cache_creation_input_tokens": 0}
    steps = [{"model": "claude-opus-5-5", "u": usage}] * 4
    cases = [
        ("a large picture is sized down as the API does", picture_tokens(png) == int(1568 * 784 / 750)),
        ("an unreadable picture gets the flat guess", picture_tokens("!!") == 1500),
        ("text is characters over four", result_tokens("x" * 400) == (100, False)),
        ("a result with a picture counts as one", result_tokens([{"type": "image", "source": {"data": png}}])[1]),
        ("a read's kind", kind_of_result("Read", False) == "file read"),
        ("a command's kind", kind_of_result("PowerShell", False) == "command output"),
        ("a picture's kind wins over its tool", kind_of_result("Read", True) == "picture"),
        ("an MCP tool's server", server_of("mcp__blender__get_objects_summary") == "blender"),
        ("a built-in tool", server_of("Read") == "built in"),
        ("carrying: one write at US$8, then reads at US$0.20", abs(carried_cost(1000000, 0, steps) - (8.0 + 0.2 * 2)) < 1e-9),
        ("a result at the last step costs nothing yet", carried_cost(1000, 3, steps) == 0.0),
    ]
    bad = 0
    for name, good in cases:
        if not good:
            bad += 1
            print("token_measures selftest FAIL " + name)
    print("token_measures selftest: passed=%d/%d failed=%d" % (len(cases) - bad, len(cases), bad))
    return 1 if bad else 0


def main(a):
    if "--selftest" in a:
        return selftest()
    if "--thrown" in a:
        return record_thrown(a)
    day = datetime.datetime.strptime(a[0], "%Y-%m-%d") if a else datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=1), datetime.time())
    return overview(day, a[a.index("--allowance") + 1] if "--allowance" in a else None)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
