#!/usr/bin/env python3
"""EVERY SESSION AND HELPER START TAGGED WITH ITS ORDER ITEM, AND THE SPEND SPLIT BY ITEM.

Why (blind-spots review, recommendation 4, adopted by Jafar 18 Nov 08:05, advisor 218): the 1 February
cost-per-piece check needs hours and dollars per order item, but since 9 November only about 40% of
logged hours carried an item code, the time log has no entry after 17 Nov 14:30, and Kiln's share was
counted by task names ("kiln", "tool loop"), so Kiln work under another name was missed (22.9% at
08:09 on 18 Nov, marked undercounting by the main session). This module, written by the cloud lane
for the main session to merge (production/lane/ITEM-TAGS-MERGE-NOTE-2026-11-18.md):

1. The current item. `python tools/lane/item_tags.py set n16-1` writes production/current-item.json.
   The session runs it whenever it takes up an item; everything below falls back to it.
2. Session start, automatic. A SessionStart hook (`hook-session`) writes a start line into
   production/time-log.jsonl carrying an "item" field, so no session runs untagged.
3. Helper start, automatic. A PreToolUse hook on the Agent tool (`hook-helper`) finds the item code in
   the helper's description or prompt; when there is none it prefixes the description with
   "[<current item>] " (so the helper's own log metadata carries it) and records the helper in
   production/helper-items.jsonl. Helper lines go to their own file because token_audit.task_windows
   closes the open task on ANY time-log line, so a helper line there would cut the session's window.
4. Spend by item. `by-item --since HH:MM` gives the hourly row's split; `kiln-share [date]` counts
   Kiln by item code (tools/lane/kiln_items.json: n16-1, n09-6 and any later Kiln item), not by name.

Step attribution, in order: a helper's own item code (its description), then the item of the time-log window open at that moment (its "item" field, else the
code in its task name), then the current item when the step falls after the log's last line
(marked "(current item, inferred)"), else "untagged". Dollars are token_audit's list prices: a measure
of usage, not his bill.

    python tools/lane/item_tags.py set n16-1 [--note "Kiln round 11"]
    python tools/lane/item_tags.py hook-session   < hook JSON   (SessionStart)
    python tools/lane/item_tags.py hook-helper    < hook JSON   (PreToolUse, matcher "Agent|Task")
    python tools/lane/item_tags.py by-item --since 07:15
    python tools/lane/item_tags.py kiln-share [2026-11-16]
"""
import datetime as dt
import glob
import io
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
TIMELOG = os.path.join(ROOT, "production", "time-log.jsonl")
HELPERS = os.path.join(ROOT, "production", "helper-items.jsonl")
CURRENT = os.path.join(ROOT, "production", "current-item.json")
KILN_ITEMS = os.path.join(HERE, "kiln_items.json")

# An order item code: n16-1, n09-12, and the same as the first two parts of n02-3-3-stutter.
# Word boundaries keep "kn16-1" and "n16-1x" out; brackets and parentheses around it are fine.
CODE = re.compile(r"(?<![A-Za-z0-9])(n\d{2}-\d{1,2})(?![0-9])")
UNTAGGED = "untagged"
# An open window (a start with no later line) ends after this many hours; estimate, the review of 18 Nov.
# token_audit drops an open window entirely; the main session should give both the same limit on merge.
OPEN_LIMIT_H = 4
KILN_CAP = 15.0   # RULINGS 13 Nov, as tools/token_measures.py KILN_CAP
# Fable's weekly cap (his pick 18 Nov, advisors 227-228; the backstop of 21:35): the last reading pace_line.py stored.
PACE_STATE = os.path.join(ROOT, "production", "handover", "pace-state.json")
FABLE_CAP = 70.0  # 19 Nov 11:07, advisor 244: "Fable cap to 70%"


def fable_refusal(inp, state_path=PACE_STATE):
    """A refusal reason when a new helper asks for model fable while Fable's stored weekly reading is at its cap, else None."""
    if str(inp.get("model") or "").lower() != "fable":
        return None
    try:
        with io.open(state_path, encoding="utf-8") as f:
            st = json.load(f)
    except (OSError, ValueError):
        return None
    fable = st.get("fable")
    if isinstance(fable, (int, float)) and fable >= FABLE_CAP:
        return ("Fable reads %.0f%% of its week (at %s), at or over his %.0f%% cap: no new Fable helper; use Opus "
                "or wait for the reset (pace_line.py --fable)." % (fable, st.get("fable_at", "?"), FABLE_CAP))
    return None


def code_in(text):
    """The first order item code in a text, or None."""
    m = CODE.search(text if isinstance(text, str) else "")
    return m.group(1) if m else None


def now():
    return dt.datetime.now().replace(microsecond=0)


# ---------------------------------------------------------------- the current item

def read_current(path=CURRENT):
    try:
        with io.open(path, encoding="utf-8") as f:
            d = json.load(f)
    except (OSError, ValueError):
        return None
    item = d.get("item") if isinstance(d, dict) else None
    return item if item and code_in(item) == item else None


def set_current(item, note="", path=CURRENT, at=None):
    if code_in(item) != item:
        raise SystemExit("item_tags: '%s' is not an order item code like n16-1" % item)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"item": item, "since": (at or now()).isoformat(), "note": note}, f, ensure_ascii=False)
        f.write("\n")


# ---------------------------------------------------------------- the hooks

def _append(path, row):
    with io.open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def hook_session(payload, timelog=TIMELOG, current=CURRENT, at=None, phase="2"):
    """SessionStart: a start line carrying the item. Returns the line written, or None for a subagent's hook
    and for a compaction or resume while a task is open (a new line would cut the running task's window and
    could retag it with a stale current item; the open task already names its item)."""
    if payload.get("agent_id"):
        return None   # a hook firing inside a helper: helpers are recorded by hook_helper
    source = payload.get("source") or "startup"
    if source in ("compact", "resume"):
        wins, last = windows(timelog)
        if wins and last is not None and wins[-1][0] == last:
            return None
    item = read_current(current) or UNTAGGED
    row = {"event": "start", "at": (at or now()).isoformat(), "task": "%s session %s (auto)" % (item, source),
           "item": item, "phase": phase, "kind": "production", "auto": "session-" + source,
           "session": payload.get("session_id", "")}
    _append(timelog, row)
    return row


def hook_helper(payload, helpers=HELPERS, current=CURRENT, at=None):
    """PreToolUse on the Agent tool. Returns (hook output dict or None, record written or None).
    A helper whose description or prompt names an item is recorded as it is; otherwise its description
    gets "[<item>] " in front through updatedInput, so its log metadata carries the item."""
    if payload.get("tool_name") not in ("Agent", "Task"):
        return None, None
    inp = dict(payload.get("tool_input") or {})
    refusal = fable_refusal(inp)
    if refusal:
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                       "permissionDecisionReason": refusal}}, None
    desc = inp.get("description") if isinstance(inp.get("description"), str) else ""
    item = code_in(desc) or code_in(inp.get("prompt"))
    out = None
    if not item:
        item = read_current(current) or UNTAGGED
        if item != UNTAGGED:
            inp["description"] = "[%s] %s" % (item, desc)
            out = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "updatedInput": inp}}
    elif not code_in(desc):
        inp["description"] = "[%s] %s" % (item, desc)
        out = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "updatedInput": inp}}
    row = {"at": (at or now()).isoformat(), "item": item, "description": inp.get("description", ""),
           "type": inp.get("subagent_type", ""), "session": payload.get("session_id", ""),
           "tool_use_id": payload.get("tool_use_id", "")}
    _append(helpers, row)
    return out, row


# ---------------------------------------------------------------- attribution

def _parse(at):
    return dt.datetime.strptime(at[:19], "%Y-%m-%dT%H:%M:%S")


def windows(timelog=TIMELOG):
    """[(start, end, item)] as token_audit.task_windows, but each window carries the item:
    the line's "item" field, else the code in its task name, else untagged."""
    ev = []
    if os.path.exists(timelog):
        for line in io.open(timelog, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("at"):
                item = d.get("item") or code_in(d.get("task")) or UNTAGGED
                ev.append((_parse(d["at"]), d.get("event"), item))
    ev.sort(key=lambda e: e[0])
    out, open_item, since = [], None, None
    for t, kind, item in ev:
        if open_item is not None:
            out.append((since, t, open_item))
            open_item = None
        if kind == "start":
            open_item, since = item, t
    if open_item is not None:
        # still open: runs on for at most OPEN_LIMIT_H hours (a start never stopped must not take every later step)
        out.append((since, since + dt.timedelta(hours=OPEN_LIMIT_H), open_item))
    return out, (ev[-1][0] if ev else None)


def item_at(wins, t):
    for s, e, item in reversed(wins):
        if s <= t and (e is None or t < e):
            return item
        if e is not None and e <= t and s <= t:
            break
    return None


def attribute(step_time, wins, last_line, helper_desc=None, current=None):
    """The item one step is charged to (see the module's note for the order)."""
    item = code_in(helper_desc)
    if item:
        return item
    item = item_at(wins, step_time)
    if item:
        return item
    if current and (last_line is None or step_time >= last_line):
        return current + " (current item, inferred)"
    return UNTAGGED


def base_item(name):
    return name.split(" ")[0]


def split(steps, wins, last_line, current=None):
    """steps: [(time, dollars, helper description or None)] -> {item: dollars}."""
    out = defaultdict(float)
    for t, usd, desc in steps:
        out[attribute(t, wins, last_line, desc, current)] += usd
    return dict(out)


def kiln_items(path=KILN_ITEMS):
    with io.open(path, encoding="utf-8") as f:
        return set(json.load(f)["items"])


def kiln_share(by_item, kiln):
    """(Kiln's dollars, all dollars, untagged dollars): by item code only. Inferred items count with their code."""
    k = sum(v for name, v in by_item.items() if base_item(name) in kiln)
    u = sum(v for name, v in by_item.items() if name == UNTAGGED)
    return k, sum(by_item.values()), u


def kiln_line(k, total, untagged, week, cap=None):
    pct = 100.0 * k / total if total else 0.0
    upct = 100.0 * untagged / total if total else 0.0
    line = "Kiln's share by item: week of %s, US$%.2f of US$%.2f (%.1f%%); untagged US$%.2f (%.1f%%)" % (
        week.strftime("%d %b"), k, total, pct, untagged, upct)
    if cap is not None and pct > cap:
        line = "KILN OVER %.0f%%: " % cap + line
    return line


def hourly_line(by_item, since_hhmm):
    total = sum(by_item.values())
    parts = ["%s US$%.2f" % (k, v) for k, v in sorted(by_item.items(), key=lambda kv: -kv[1]) if v >= 0.005]
    return "By item since %s (US$%.2f): %s" % (since_hhmm, total, "; ".join(parts) if parts else "nothing spent")


# ---------------------------------------------------------------- reading the PC's logs (token_audit's readers)

def steps_from_logs(since, until=None):
    """[(swiss time, dollars, helper description or None)] from this PC's session logs, through token_audit."""
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    from token_audit import LOGS, read_log, step_cost, swiss  # noqa: E402
    out = []
    for main in sorted(glob.glob(os.path.join(LOGS, "*.jsonl"))):
        sess = os.path.splitext(os.path.basename(main))[0]
        logs = [(main, None)]
        for sub in sorted(glob.glob(os.path.join(LOGS, sess, "subagents", "agent-*.jsonl"))):
            meta = {}
            mp = sub[:-len(".jsonl")] + ".meta.json"
            if os.path.exists(mp):
                try:
                    meta = json.load(io.open(mp, encoding="utf-8"))
                except ValueError:
                    meta = {}
            logs.append((sub, meta.get("description", "") or ""))
        for path, desc in logs:
            for s in read_log(path).values():
                t = swiss(s["ts"])
                if t >= since and (until is None or t < until):
                    out.append((t, step_cost(s["usage"], s["model"]), desc))
    return out


def since_time(hhmm, at):
    s = dt.datetime.strptime(at.strftime("%Y-%m-%d ") + hhmm, "%Y-%m-%d %H:%M")
    return s - dt.timedelta(days=1) if s > at else s


def main(argv):
    if not argv:
        print(__doc__)
        return 0
    cmd = argv[0]
    if cmd == "set":
        note = argv[argv.index("--note") + 1] if "--note" in argv else ""
        set_current(argv[1], note)
        print("current item: %s" % argv[1])
        return 0
    if cmd in ("hook-session", "hook-helper"):
        try:
            payload = json.load(sys.stdin)
            if not isinstance(payload, dict):
                return 0
            if cmd == "hook-session":
                hook_session(payload, timelog=TIMELOG, current=CURRENT)
            else:
                out, _ = hook_helper(payload, helpers=HELPERS, current=CURRENT)
                if out:
                    print(json.dumps(out))
        except Exception:   # noqa: BLE001  never block or flag a start over a bad payload or a file error
            pass
        return 0
    wins, last = windows()
    cur = read_current()
    if cmd == "by-item":
        hhmm = argv[argv.index("--since") + 1] if "--since" in argv else "00:00"
        since = since_time(hhmm, now())
        print(hourly_line(split(steps_from_logs(since), wins, last, cur), hhmm))
        return 0
    if cmd == "kiln-share":
        day = dt.datetime.strptime(argv[1], "%Y-%m-%d") if len(argv) > 1 else dt.datetime.combine(dt.date.today(), dt.time())
        week = day - dt.timedelta(days=day.weekday())
        by = split(steps_from_logs(week, week + dt.timedelta(days=7)), wins, last, cur)
        line = kiln_line(*kiln_share(by, kiln_items()), week=week, cap=KILN_CAP)
        print(line)
        return 1 if line.startswith("KILN OVER") else 0   # as token_measures --kiln-share: over the cap fails
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
