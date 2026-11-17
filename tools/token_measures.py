#!/usr/bin/env python3
"""SIX MEASURES OF A DAY'S SPEND, READ FROM THE SESSION LOGS, FOR THE MORNING'S OVERVIEW. Measures only; nothing is changed by them.

    python tools/token_measures.py 2026-11-05 [--allowance 49]   # a short table for the overview, then the detail
    python tools/token_measures.py --spend 21:22   # list-price dollars since then, for the hourly row
    python tools/token_measures.py --thrown "the hill's second crowns" --since 09:30 [--until 10:10]  # record a try thrown away
    python tools/token_measures.py --kiln-share [2026-11-16]   # Kiln's share of that day's week (Monday on); KILN OVER 15% fails
    python tools/token_measures.py --helpers   # the most helpers running at once yesterday and today; HELPERS OVER CAP fails
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
from token_audit import ROOT, LOGS, TIMELOG, audit, item_at, price_of, step_cost, swiss, task_windows  # noqa: E402

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
    helper_start, helper_runs = 0.0, 0
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
            # each write at its own rate, as step_cost: helpers write at the 5-minute rate, the session at 1 hour (n09-11, 8 Nov)
            w1h = (u.get("cache_creation") or {}).get("ephemeral_1h_input_tokens", 0) or 0
            w5m = (u.get("cache_creation") or {}).get("ephemeral_5m_input_tokens", None)
            if w5m is None:
                w5m = max(cw - w1h, 0)
            cost = (w5m * p[2] + w1h * p[3]) / 1e6
            write_all += cost
            if meta is not None and i < START_STEPS:
                helper_start += cost
                helper_runs += 1 if i == 0 else 0
            elif meta is None and i < START_STEPS:
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
            "rewrite": rewrite, "rewrites": rewrites, "runs": runs, "broken": broken, "rounds": rounds,
            "helperStart": helper_start, "helperRuns": helper_runs}


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
    print("| 3 Prompt cache | %.1f%% of tokens read from cache; writes US$%.2f, of which session starts US$%.2f in %d runs, helper starts US$%.2f in %d, %d rewrites mid-run US$%.2f, the rest step growth US$%.2f; %d runs missed the shared start |" % (
        100 * t["read"] / all_in, m["writeAll"], m["startWrite"], m["runs"], m["helperStart"], m["helperRuns"], m["rewrites"], m["rewrite"],
        m["writeAll"] - m["startWrite"] - m["helperStart"] - m["rewrite"], m["broken"]))
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


def since_time(hhmm, now):
    """HH:MM's latest moment not after now: 23:22 asked at 00:11 means last night (6 November: it read US$0.00 across midnight)."""
    since = datetime.datetime.strptime(now.strftime("%Y-%m-%d ") + hhmm, "%Y-%m-%d %H:%M")
    return since - datetime.timedelta(days=1) if since > now else since


def spend_since(hhmm):
    """The session's and helpers' list-price dollars since HH:MM until now, for the hourly row (the advisor's message 18)."""
    since = since_time(hhmm, datetime.datetime.now())
    steps = [s for path, _ in logs_touched(since) for s in read_events(path)["steps"] if s["t"] >= since]
    print("spend since %s: US$%.2f" % (hhmm, sum(step_cost(s["u"], s["model"]) for s in steps)))
    print(model_line(session_model_now()))
    return 0


# THE SESSION'S MODEL IN EVERY ROW, AND DOLLARS PER STEP BY MODEL (advisor 162, 14 November: the session ran a whole
# day on Fable against RULINGS 8 Nov, about twice the dollars per step, and nothing caught it). --spend now ends with
# the row's "Model:" words, read from the newest session log's newest step; --by-model gives the DAILY file its table
# and says JUMP when the session's dollars per step rose by more than half on the day before (to his page that hour).
SESSION_MODEL = "claude-opus-5-5"
JUMP = 1.5


def model_line(model):
    if model and model.startswith(SESSION_MODEL):
        return "Model: Opus 5.5"
    return "MODEL WRONG, first in the row: the session is on %s, not Opus 5.5 (RULINGS 8 Nov). Row ends 'Model: %s'" % (model or "unknown", model or "unknown")


def session_model_now():
    """The model of the newest step in the newest main session log that has one."""
    for path in sorted(glob.glob(os.path.join(LOGS, "*.jsonl")), key=os.path.getmtime, reverse=True)[:6]:
        steps = read_events(path)["steps"]
        if steps:
            return steps[-1]["model"]
    return None


def by_model_of(day):
    """{(who, model): [steps, dollars]} for a day; who is 'session' or 'helpers'."""
    out = collections.defaultdict(lambda: [0, 0.0])
    until = day + datetime.timedelta(days=1)
    for path, meta in logs_touched(day):
        for s in read_events(path)["steps"]:
            if day <= s["t"] < until:
                row = out[("session" if meta is None else "helpers", s["model"])]
                row[0] += 1
                row[1] += step_cost(s["u"], s["model"])
    return out


def per_step(table, who="session"):
    n = sum(v[0] for k, v in table.items() if k[0] == who)
    return (sum(v[1] for k, v in table.items() if k[0] == who) / n) if n else None


def jump_line(today, before):
    if today is None or before is None or before <= 0:
        return "jump: not judged (a day without session steps)"
    word = "JUMP: to his page this hour" if today > JUMP * before else "no jump"
    return "%s: the session's dollars per step US$%.3f against US$%.3f the day before (%+.0f%%)" % (word, today, before, (today / before - 1) * 100)


def by_model(day):
    a, b = by_model_of(day), by_model_of(day - datetime.timedelta(days=1))
    print("| who | model | %s steps | US$ | US$ per step | day before: steps | US$ per step |" % day.strftime("%d %b"))
    print("|---|---|---|---|---|---|---|")
    for key in sorted(set(a) | set(b)):
        x, y = a.get(key, [0, 0.0]), b.get(key, [0, 0.0])
        print("| %s | %s | %d | %.2f | %s | %d | %s |" % (key[0], key[1], x[0], x[1], "%.3f" % (x[1] / x[0]) if x[0] else "-", y[0], "%.3f" % (y[1] / y[0]) if y[0] else "-"))
    print(jump_line(per_step(a), per_step(b)))
    return 0


# KILN'S SHARE OF THE WEEK (RULINGS 13 Nov: "at most 15% of weekly usage"; enforced 17 Nov). The week's steps are
# token_audit.py's, each given to the time-log task open at that moment (helpers' steps too); a task whose name holds
# "kiln" or "tool loop" is Kiln's. Dollars at list price, a measure of usage, not his bill.
KILN = re.compile(r"kiln|tool loop", re.I)
KILN_CAP = 15.0


def kiln_share(items):
    """(Kiln's dollars, all dollars) from token_audit's items table {task: [usd, steps]}."""
    return sum(v[0] for k, v in items.items() if KILN.search(k or "")), sum(v[0] for v in items.values())


def kiln_line(kiln, total, week):
    pct = 100.0 * kiln / total if total else 0.0
    word = "KILN OVER 15% of the week's spend" if pct > KILN_CAP else "kiln share within 15%"
    return "%s: week of %s, US$%.2f of US$%.2f (%.1f%%)" % (word, week.strftime("%d %b"), kiln, total, pct)


def kiln_week(day):
    week = day - datetime.timedelta(days=day.weekday())
    out = audit(week, week + datetime.timedelta(days=7))
    line = kiln_line(*kiln_share(out["items"]), week=week)
    print(line)
    return 1 if line.startswith("KILN OVER") else 0


# HELPERS RUNNING AT ONCE (RULINGS 6 Nov: up to four, six when behind; his picks of 17 Nov: eight a session from 16 to
# 23 Nov; enforced 17 Nov). Each helper's log runs from its first timestamp to its last; the most that overlap is the
# day's peak. Only each log's head and tail are read, so this stays light however large a log is.
TIMESTAMP = re.compile(rb'"timestamp":"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)')


def helper_cap(day):
    return 8 if datetime.date(2026, 11, 16) <= day <= datetime.date(2026, 11, 23) else 6


def log_span(path, chunk=262144, most=8 * 262144):
    """(first, last) Swiss times of a log from its head and tail, or None."""
    try:
        with open(path, "rb") as fh:
            first = TIMESTAMP.search(fh.read(chunk))
            size = fh.seek(0, 2)
            last, back = None, chunk
            while last is None and back <= most:
                fh.seek(max(0, size - back))
                found = TIMESTAMP.findall(fh.read(min(back, size)))
                last = found[-1] if found else None
                if back >= size:
                    break
                back *= 2
    except OSError:
        return None
    if not first or not last:
        return None
    return swiss(first.group(1).decode()), swiss(last.decode())


def max_at_once(spans):
    """(peak, moment) of overlapping (start, end) spans; an end and a start at the same second do not overlap."""
    events = sorted([(s, 1) for s, e in spans] + [(e, -1) for s, e in spans], key=lambda x: (x[0], x[1]))
    now = peak = 0
    when = None
    for t, d in events:
        now += d
        if now > peak:
            peak, when = now, t
    return peak, when


def helpers_line(peak, when):
    if not peak:
        return "helpers at once: none running yesterday or today"
    cap = helper_cap(when.date())
    word = "HELPERS OVER CAP" if peak > cap else "helpers within cap"
    return "%s: %d at once at %s, cap %d" % (word, peak, when.strftime("%d %b %H:%M"), cap)


def helpers_peak():
    since = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=1), datetime.time())
    spans = []
    for sub in glob.glob(os.path.join(LOGS, "*", "subagents", "agent-*.jsonl")):
        if os.path.getmtime(sub) >= since.timestamp():
            span = log_span(sub)
            if span and span[1] >= since:
                spans.append((max(span[0], since), span[1]))
    line = helpers_line(*max_at_once(spans))
    print(line)
    return 1 if line.startswith("HELPERS OVER") else 0


def selftest():
    png = base64.b64encode(b"\x89PNG\r\n\x1a\n" + b"\0\0\0\rIHDR" + struct.pack(">II", 3136, 1568)).decode()
    usage = {"input_tokens": 0, "output_tokens": 0, "cache_read_input_tokens": 100, "cache_creation_input_tokens": 0}
    steps = [{"model": "claude-opus-5-5", "u": usage}] * 4
    cases = [
        ("a large picture is sized down as the API does", picture_tokens(png) == int(1568 * 784 / 750)),
        ("an unreadable picture gets the flat guess", picture_tokens("!!") == 1500),
        ("a time later than now is last night's", since_time("23:22", datetime.datetime(2026, 11, 7, 0, 11)) == datetime.datetime(2026, 11, 6, 23, 22)),
        ("a time earlier than now is today's", since_time("09:00", datetime.datetime(2026, 11, 7, 11, 0)) == datetime.datetime(2026, 11, 7, 9, 0)),
        ("text is characters over four", result_tokens("x" * 400) == (100, False)),
        ("a result with a picture counts as one", result_tokens([{"type": "image", "source": {"data": png}}])[1]),
        ("a read's kind", kind_of_result("Read", False) == "file read"),
        ("a command's kind", kind_of_result("PowerShell", False) == "command output"),
        ("a picture's kind wins over its tool", kind_of_result("Read", True) == "picture"),
        ("an MCP tool's server", server_of("mcp__blender__get_objects_summary") == "blender"),
        ("a built-in tool", server_of("Read") == "built in"),
        ("carrying: one write at US$8, then reads at US$0.20", abs(carried_cost(1000000, 0, steps) - (8.0 + 0.2 * 2)) < 1e-9),
        ("a result at the last step costs nothing yet", carried_cost(1000, 3, steps) == 0.0),
        ("the row's model words on Opus", model_line("claude-opus-5-5") == "Model: Opus 5.5"),
        ("the row's model words fire on Fable", model_line("claude-fable-5-2").startswith("MODEL WRONG")),
        ("the row's model words fire when unknown", model_line(None).startswith("MODEL WRONG")),
        ("dollars per step up by more than half: JUMP", jump_line(0.169, 0.071).startswith("JUMP")),
        ("dollars per step up by a third: no jump", jump_line(0.094, 0.071).startswith("no jump")),
        ("dollars per step with an empty day: not judged", jump_line(0.1, None).startswith("jump: not judged")),
        ("kiln share: tasks naming kiln or the tool loop", kiln_share({"tool loop: kiln round 1": [3.0, 1], "Kiln gate": [1.0, 1], "n02 garment": [16.0, 1]}) == (4.0, 20.0)),
        ("kiln at 20% fails", kiln_line(4.0, 20.0, datetime.datetime(2026, 11, 16)).startswith("KILN OVER 15%")),
        ("kiln at exactly 15% passes", kiln_line(3.0, 20.0, datetime.datetime(2026, 11, 16)).startswith("kiln share within")),
        ("kiln with no spend passes", kiln_line(0.0, 0.0, datetime.datetime(2026, 11, 16)).startswith("kiln share within")),
        ("helper cap is eight this week", helper_cap(datetime.date(2026, 11, 17)) == 8 and helper_cap(datetime.date(2026, 11, 23)) == 8),
        ("helper cap is six outside it", helper_cap(datetime.date(2026, 11, 24)) == 6 and helper_cap(datetime.date(2026, 11, 15)) == 6),
        ("three overlapping helpers peak at three", max_at_once([(datetime.datetime(2026, 11, 17, h), datetime.datetime(2026, 11, 17, h + 3)) for h in (9, 10, 11)])[0] == 3),
        ("one ending as the next starts is not two", max_at_once([(datetime.datetime(2026, 11, 17, 9), datetime.datetime(2026, 11, 17, 10)), (datetime.datetime(2026, 11, 17, 10), datetime.datetime(2026, 11, 17, 11))])[0] == 1),
        ("nine at once this week fails", helpers_line(9, datetime.datetime(2026, 11, 17, 10)).startswith("HELPERS OVER CAP")),
        ("seven at once next week fails", helpers_line(7, datetime.datetime(2026, 11, 24, 10)).startswith("HELPERS OVER CAP")),
        ("eight at once this week passes", helpers_line(8, datetime.datetime(2026, 11, 17, 10)).startswith("helpers within cap")),
        ("a log's span from its head and tail", span_case()),
        ("per step over the session's models only", abs(per_step({("session", "a"): [2, 1.0], ("session", "b"): [2, 3.0], ("helpers", "a"): [9, 90.0]}) - 1.0) < 1e-9),
    ]
    bad = 0
    for name, good in cases:
        if not good:
            bad += 1
            print("token_measures selftest FAIL " + name)
    print("token_measures selftest: passed=%d/%d failed=%d" % (len(cases) - bad, len(cases), bad))
    return 1 if bad else 0


def span_case():
    import tempfile
    d = tempfile.mkdtemp()
    p = os.path.join(d, "agent-x.jsonl")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write('{"timestamp":"2026-11-17T08:00:00.000Z"}\n' + ('{"pad":"' + "x" * 1000 + '"}\n') * 600 + '{"timestamp":"2026-11-17T09:30:00.000Z"}\n')
    span = log_span(p, chunk=4096)
    os.remove(p)
    return span == (datetime.datetime(2026, 11, 17, 9, 0), datetime.datetime(2026, 11, 17, 10, 30))


def main(a):
    if "--selftest" in a:
        return selftest()
    if "--kiln-share" in a:
        rest = a[a.index("--kiln-share") + 1:]
        return kiln_week(datetime.datetime.strptime(rest[0], "%Y-%m-%d") if rest else datetime.datetime.combine(datetime.date.today(), datetime.time()))
    if "--helpers" in a:
        return helpers_peak()
    if "--thrown" in a:
        return record_thrown(a)
    if "--spend" in a:
        return spend_since(a[a.index("--spend") + 1])
    if "--by-model" in a:
        rest = a[a.index("--by-model") + 1:]
        return by_model(datetime.datetime.strptime(rest[0], "%Y-%m-%d") if rest else datetime.datetime.combine(datetime.date.today(), datetime.time()))
    day = datetime.datetime.strptime(a[0], "%Y-%m-%d") if a else datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=1), datetime.time())
    return overview(day, a[a.index("--allowance") + 1] if "--allowance" in a else None)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
