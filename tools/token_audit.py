#!/usr/bin/env python3
"""WHAT EACH ITEM AND EACH KIND OF WORK COSTS, FROM THIS PC'S OWN CLAUDE CODE SESSION LOGS.

    python tools/token_audit.py [--since 2026-10-26] [--until 2026-11-02] [--out production/research/token-audit]
    python tools/token_audit.py --selftest

WHY, 1 November 2026 (his order of 2 November, 6.1: "a token audit from your own Claude Code session logs on this PC:
the cost of each item and of each kind of work (building, reviewing, reporting, research, helpers), records and reports
included, by Wednesday; then every week"; 6.2: "from the audit, how much a long session's history adds to each step").

WHAT IT READS: every session log of this project (~/.claude/projects/C--Users-Jafar-ledger-local/*.jsonl) and every
helper's (<session>/subagents/agent-*.jsonl, with its .meta.json naming the helper). Each step the model took is one
assistant message with its token counts (fresh input, cache writes, cache reads, output); a message logged over several
lines is counted once, by its id.

WHAT IT COUNTS:
- the cost of each step at Anthropic's published API prices (claude-api skill, cached 6 October 2026): what the same
  work would cost on the API, so kinds of work compare; his plan's allowance is metered differently, so the dollars are
  a measure, not a bill;
- each step's item: the task open in production/time-log.jsonl at that moment (helpers' steps too, rule 9: helpers'
  time counts against their item); a step in no task window is "not in the time log";
- each step's kind: helpers by their own description (reviewing, research, building); the session's own steps by the
  tools they used: records and reports (DECISIONS, FOR-JAFAR, RECIPE, NOW, FINDINGS, RULINGS, CLAUDE, the ledger, the
  progress page, the time log, his pages, the task list), research (web, the engine's source, the research library),
  helpers (launching and reading them), building (everything else that edits, runs or reads), replies (no tool);
- the history's share: each step re-reads the whole conversation; the part above the session's own first step (its
  system and tools) is the history, and its cost is the history's share of the step.
"""
import datetime
import glob
import json
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS = os.path.join(os.path.expanduser("~"), ".claude", "projects", "C--Users-Jafar-ledger-local")
TIMELOG = os.path.join(ROOT, "production", "time-log.jsonl")

# US$ per million tokens: input, output, cache write (5 min), cache write (1 h), cache read. The claude-api skill's table
# (cached 2026-10-06); cache writes at Anthropic's usual 1.25x and 2x of input; Haiku 5.5's cache read at 0.1x (unverified)
PRICES = {
    "claude-fable-5-1": (10.0, 50.0, 12.5, 20.0, 0.25),
    "claude-fable-5": (10.0, 50.0, 12.5, 20.0, 0.25),
    "claude-opus-5-5": (4.0, 20.0, 5.0, 8.0, 0.20),
    "claude-opus-5": (5.0, 25.0, 6.25, 10.0, 0.50),
    "claude-sonnet-5-5": (2.0, 10.0, 2.5, 4.0, 0.20),
    "claude-sonnet-5": (2.0, 10.0, 2.5, 4.0, 0.20),
    "claude-haiku-5-5": (0.10, 0.50, 0.125, 0.20, 0.01),
}
DEFAULT_PRICE = "claude-opus-5-5"
RECORDS = re.compile(r"(DECISIONS|FOR-JAFAR|RECIPE|NOW|FINDINGS|RULINGS|CLAUDE|MEMORY)\.md|production[/\\](orders|progress-page|approvals)|"
                     r"time-log\.jsonl|timelog\.py|progress_page\.py|day_page\.py|\.claude[/\\]projects[/\\].*memory", re.I)
RESEARCH = re.compile(r"production[/\\]research|Epic Games[/\\]UE_|studies[/\\]|aaa-reference", re.I)
REVIEW_WORDS = re.compile(r"review|gate|judge|check the|verify|reviewer", re.I)
RESEARCH_WORDS = re.compile(r"research|study|find|read|survey|look up|deep-dive|extract", re.I)


def price_of(model):
    m = (model or "").replace("[1m]", "")
    for k in PRICES:
        if m.startswith(k):
            return PRICES[k], k
    return PRICES[DEFAULT_PRICE], DEFAULT_PRICE + "?"


def step_cost(u, model):
    p, _ = price_of(model)
    cc = u.get("cache_creation") or {}
    w1h = cc.get("ephemeral_1h_input_tokens", 0) or 0
    w5m = cc.get("ephemeral_5m_input_tokens", None)
    cw = u.get("cache_creation_input_tokens", 0) or 0
    if w5m is None:
        w5m = max(cw - w1h, 0)
    return (u.get("input_tokens", 0) * p[0] + u.get("output_tokens", 0) * p[1] + w5m * p[2] + w1h * p[3]
            + u.get("cache_read_input_tokens", 0) * p[4]) / 1e6


def swiss(ts):
    """A log's UTC time as Swiss local time (CET, CEST from the last Sunday of March to the last of October, 01:00 UTC)."""
    t = datetime.datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S")

    def last_sunday(y, m):
        d = datetime.datetime(y, m + 1, 1) - datetime.timedelta(days=1)
        return d - datetime.timedelta(days=(d.weekday() + 1) % 7)
    start = last_sunday(t.year, 3).replace(hour=1)
    end = last_sunday(t.year, 10).replace(hour=1)
    return t + datetime.timedelta(hours=2 if start <= t < end else 1)


def task_windows(path=TIMELOG):
    """[(start, end, task)] from the time log: each start runs to its stop or to the next start."""
    ev = []
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            at = d.get("at")
            if not at:
                continue
            ev.append((datetime.datetime.strptime(at[:19], "%Y-%m-%dT%H:%M:%S"), d.get("event"), d.get("task")))
    ev.sort(key=lambda e: e[0])
    out, open_task, since = [], None, None
    for t, kind, task in ev:
        if open_task is not None:
            out.append((since, t, open_task))
            open_task = None
        if kind == "start":
            open_task, since = task, t
    return out


def item_at(windows, t):
    lo, hi = 0, len(windows)
    while lo < hi:
        mid = (lo + hi) // 2
        if windows[mid][1] <= t:
            lo = mid + 1
        else:
            hi = mid
    for s, e, task in windows[lo:lo + 3]:
        if s <= t < e:
            return task
    return "not in the time log"


def kind_of_main(tools):
    """A session's own step, by what its tool calls touched."""
    if not tools:
        return "replies and thinking"
    names = [n for n, _ in tools]
    text = " ".join(x for _, x in tools)
    if any(n.startswith("mcp__ccd_turn__") for n in names) or (RECORDS.search(text) and not re.search(r"\.(py|cpp|h|cs|ps1)\b(?!.*(DECISIONS|RECIPE))", text)):
        return "records and reports"
    if any(n in ("WebFetch", "WebSearch") or n.startswith("mcp__Claude_Browser") for n in names) or RESEARCH.search(text):
        return "research"
    if any(n in ("Agent", "SendMessage", "TaskStop") for n in names):
        return "helpers (briefing and reading)"
    return "building"


def kind_of_helper(description):
    d = description or ""
    if REVIEW_WORDS.search(d):
        return "reviewing (helpers)"
    if RESEARCH_WORDS.search(d):
        return "research (helpers)"
    return "building (helpers)"


def read_log(path, helper_desc=None):
    """{message id: step} for one log; a message logged over several lines is merged."""
    steps, first_ctx = {}, None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"assistant"' not in line or '"usage"' not in line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("type") != "assistant":
                continue
            m = d.get("message") or {}
            u = m.get("usage")
            mid = m.get("id") or d.get("uuid")
            if not u or not d.get("timestamp"):
                continue
            s = steps.get(mid)
            if s is None:
                ctx = (u.get("input_tokens", 0) or 0) + (u.get("cache_read_input_tokens", 0) or 0) + (u.get("cache_creation_input_tokens", 0) or 0)
                s = steps[mid] = {"ts": d["timestamp"], "model": m.get("model"), "usage": u, "ctx": ctx, "tools": []}
            for c in m.get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    inp = c.get("input") or {}
                    s["tools"].append((c.get("name", ""), " ".join(str(inp.get(k, ""))[:300] for k in ("file_path", "command", "description", "url", "pattern", "path", "prompt"))))
    return steps


def audit(since=None, until=None, logs=LOGS, timelog=TIMELOG):
    windows = task_windows(timelog)
    rows = []
    for main in sorted(glob.glob(os.path.join(logs, "*.jsonl"))):
        sess = os.path.splitext(os.path.basename(main))[0]
        steps = read_log(main)
        base = min((s["ctx"] for s in steps.values()), default=0)
        for s in steps.values():
            rows.append(("main", sess, None, s, base))
        for sub in sorted(glob.glob(os.path.join(logs, sess, "subagents", "agent-*.jsonl"))):
            meta = {}
            mp = sub[:-len(".jsonl")] + ".meta.json"
            if os.path.exists(mp):
                try:
                    meta = json.load(open(mp, encoding="utf-8"))
                except ValueError:
                    meta = {}
            hs = read_log(sub)
            hbase = min((s["ctx"] for s in hs.values()), default=0)
            for s in hs.values():
                rows.append(("helper", sess, meta.get("description", ""), s, hbase))
    out = {"items": defaultdict(lambda: [0.0, 0]), "kinds": defaultdict(lambda: [0.0, 0]), "days": defaultdict(lambda: [0.0, 0]),
           "models": defaultdict(lambda: [0.0, 0]), "history": [0.0, 0.0], "steps": 0, "usd": 0.0,
           "itemKinds": defaultdict(lambda: defaultdict(float))}
    for who, sess, desc, s, base in rows:
        t = swiss(s["ts"])
        if since and t < since or until and t >= until:
            continue
        usd = step_cost(s["usage"], s["model"])
        item = item_at(windows, t)
        kind = kind_of_helper(desc) if who == "helper" else kind_of_main(s["tools"])
        for key, name in (("items", item), ("kinds", kind), ("days", t.strftime("%Y-%m-%d")), ("models", price_of(s["model"])[1])):
            out[key][name][0] += usd
            out[key][name][1] += 1
        out["itemKinds"][item][kind] += usd
        out["steps"] += 1
        out["usd"] += usd
        # the history: what this step re-read above its session's own start, at the cache-read price
        p, _ = price_of(s["model"])
        hist = max(s["ctx"] - base, 0)
        out["history"][0] += hist * p[4] / 1e6
        out["history"][1] += usd
    return out


def report(out, since, until):
    tot = out["usd"] or 1.0
    lines = ["# The token audit, %s to %s" % (since.strftime("%d %B %Y") if since else "the start", (until - datetime.timedelta(days=1)).strftime("%d %B %Y") if until else "now"), "",
             "From this PC's own Claude Code session logs (tools/token_audit.py). Dollars are what the same steps would cost at Anthropic's published API prices: a measure to compare work, not his bill.", "",
             "**%d steps, US$%.2f at API prices.** The history's share (each step re-reading the conversation above its session's own start): **%.0f%%** of the cost." % (out["steps"], out["usd"], 100 * out["history"][0] / tot), "",
             "## By kind of work", "", "| Kind | US$ | Share | Steps |", "|---|---|---|---|"]
    for k, (u, n) in sorted(out["kinds"].items(), key=lambda kv: -kv[1][0]):
        lines.append("| %s | %.2f | %.0f%% | %d |" % (k, u, 100 * u / tot, n))
    lines += ["", "## By item (the time log's task open at each step)", "", "| Item | US$ | Share | Steps | Largest kind |", "|---|---|---|---|---|"]
    for k, (u, n) in sorted(out["items"].items(), key=lambda kv: -kv[1][0])[:40]:
        big = max(out["itemKinds"][k].items(), key=lambda kv: kv[1])[0] if out["itemKinds"][k] else ""
        lines.append("| %s | %.2f | %.0f%% | %d | %s |" % (k[:90], u, 100 * u / tot, n, big))
    lines += ["", "## By day (Swiss time)", "", "| Day | US$ | Steps |", "|---|---|---|"]
    for k, (u, n) in sorted(out["days"].items()):
        lines.append("| %s | %.2f | %d |" % (k, u, n))
    lines += ["", "## By model", "", "| Model | US$ | Steps |", "|---|---|---|"]
    for k, (u, n) in sorted(out["models"].items(), key=lambda kv: -kv[1][0]):
        lines.append("| %s | %.2f | %d |" % (k, u, n))
    return "\n".join(lines) + "\n"


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("token_audit selftest FAIL " + name)
    u = {"input_tokens": 1000000, "output_tokens": 0, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
    check("a million fresh Opus 5.5 tokens cost $4", abs(step_cost(u, "claude-opus-5-5") - 4.0) < 1e-9)
    u2 = {"input_tokens": 0, "output_tokens": 0, "cache_read_input_tokens": 1000000, "cache_creation_input_tokens": 1000000,
          "cache_creation": {"ephemeral_1h_input_tokens": 1000000, "ephemeral_5m_input_tokens": 0}}
    check("cache reads and hour-long writes priced apart", abs(step_cost(u2, "claude-opus-5-5") - 8.20) < 1e-9)
    check("summer time in Zurich is UTC+2", swiss("2026-10-24T10:00:00.000Z").hour == 12)
    check("winter time from the last Sunday of October", swiss("2026-10-26T10:00:00.000Z").hour == 11)
    w = [(datetime.datetime(2026, 11, 1, 10), datetime.datetime(2026, 11, 1, 11), "a")]
    check("a step inside a task window is that task's", item_at(w, datetime.datetime(2026, 11, 1, 10, 30)) == "a")
    check("a step outside every window is not in the time log", item_at(w, datetime.datetime(2026, 11, 1, 12)) == "not in the time log")
    check("editing the decisions is records", kind_of_main([("Edit", "C:/x/DECISIONS.md")]) == "records and reports")
    check("a web search is research", kind_of_main([("WebSearch", "")]) == "research")
    check("a reviewer helper is reviewing", kind_of_helper("Gate review: Tom boots view") == "reviewing (helpers)")
    check("an edit of code is building", kind_of_main([("Edit", "C:/x/tools/ue/import_garments.py")]) == "building")
    print("token_audit selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


def main(a):
    if "--selftest" in a:
        return selftest()

    def day(name):
        return datetime.datetime.strptime(a[a.index(name) + 1], "%Y-%m-%d") if name in a else None
    since, until = day("--since"), day("--until")
    out = audit(since, until)
    dest = os.path.join(ROOT, a[a.index("--out") + 1]) if "--out" in a else os.path.join(ROOT, "production", "research", "token-audit")
    os.makedirs(dest, exist_ok=True)
    stamp = (since or datetime.datetime(2026, 9, 1)).strftime("%Y-%m-%d") + "_to_" + ((until - datetime.timedelta(days=1)) if until else datetime.datetime.now()).strftime("%Y-%m-%d")
    md = report(out, since, until)
    open(os.path.join(dest, "AUDIT-%s.md" % stamp), "w", encoding="utf-8").write(md)
    j = {k: (dict(v) if isinstance(v, defaultdict) else v) for k, v in out.items() if k != "itemKinds"}
    j["itemKinds"] = {k: dict(v) for k, v in out["itemKinds"].items()}
    json.dump(j, open(os.path.join(dest, "audit-%s.json" % stamp), "w", encoding="utf-8"), indent=1)
    print("token-audit steps=%d usd=%.2f history=%.0f%% -> %s" % (out["steps"], out["usd"], 100 * out["history"][0] / (out["usd"] or 1), os.path.join(dest, "AUDIT-%s.md" % stamp)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
