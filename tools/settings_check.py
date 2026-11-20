#!/usr/bin/env python3
"""THE SETTINGS OUTSIDE THE REPOSITORY THAT CAN RAISE COST OR STOP WORK, read once a day.

    python tools/settings_check.py            # one line per setting, then 'settings-check wrong=N'
    python tools/settings_check.py --selftest

WHY. His decision of 16 Nov 14:12 (advisor 182, item 2): list every setting outside the repository that can
raise cost or stop work and give each a check read at the start or in the DAILY file, like the model check of
14 Nov (tools/fresh_gate.py). The list and where each lives: production/research/token-audit/SETTINGS-SWEEP-2026-11-16.md.
This reads; it changes nothing. A key's value is never printed, only 'set' or 'not set'.
API spend (RULINGS 1 Nov, 16 Nov; enforced 17 Nov): each day of the current credit month in production/api-spend.jsonl
is judged against that day's ceiling (credit left divided by days left, api_batch.py's own figures, its one home).
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPECT = {
    "active_hours": (12, 5),
    "power_scheme": "071e8fd2-530b-49c7-925c-3edb157c2910",   # Ultimate Performance
    "floors_gb": {"C": 40, "F": 20},
    "warn_gb": {"C": 45, "F": 22},
    "agents": {"diagnoser": ("opus", "high"), "extractor": ("sonnet", "medium"), "final-reviewer": ("opus", "medium"),
               "importer": ("sonnet", "medium"), "research-reader": ("sonnet", "medium"),
               "research-synthesis": ("opus", "medium"), "small-reviewer": ("sonnet", "medium")},
    "tasks_ready": ["LEDGER nightly walk", "LEDGER retention", "LEDGER morning pictures"],
    "tasks_disabled": ["LEDGER supervisor"],
    "base_url": "https://api.anthropic.com",
}
STARTUP = os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs\Startup\LEDGER runner.lnk")


def ps(cmd):
    try:
        return subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception as e:  # a reading that fails is reported, never fatal
        return "ERROR %s" % e


def agent_lines(folder):
    out = {}
    for p in glob.glob(os.path.join(folder, "*.md")):
        txt = open(p, encoding="utf-8").read()
        m = re.search(r"^model:\s*(\S+)", txt, re.M)
        e = re.search(r"^effort:\s*(\S+)", txt, re.M)
        out[os.path.splitext(os.path.basename(p))[0]] = (m.group(1) if m else None, e.group(1) if e else None)
    return out


def judge_agents(found, expect):
    return ["%s %s/%s, expected %s/%s" % (k, found.get(k, (None, None))[0], found.get(k, (None, None))[1], v[0], v[1])
            for k, v in expect.items() if found.get(k) != v]


CATCH_ALL = ("claude", "general-purpose")
USE_INSTEAD = "reading and extraction: research-reader or extractor (Sonnet); diagnosis: diagnoser; judgement: final-reviewer"


def judge_catch_all(who_models, usd):
    """Advisor's efficiency review, 20 Nov: helpers run as project types, never the catch-all ('claude',
    'general-purpose'; 8 Nov ruling). who_models: token_audit's {"<type> on <model>": (usd, steps)}.
    Returns (state, value): WRONG naming steps, dollars and share when any catch-all helper ran."""
    hit = {k: v for k, v in who_models.items() if k.split(" on ")[0] in CATCH_ALL}
    if not hit:
        return "OK", "none"
    u = sum(v[0] for v in hit.values()); n = sum(v[1] for v in hit.values())
    return "WRONG", "%d steps US$%.2f (%.1f%% of the day) as %s; use instead: %s" % (
        n, u, 100 * u / (usd or 1), ", ".join(sorted(hit)), USE_INSTEAD)


def judge_drive(letter, free_gb):
    if free_gb < EXPECT["floors_gb"][letter]:
        return "WRONG"
    return "WARN" if free_gb < EXPECT["warn_gb"][letter] else "OK"


def api_days_over(lines, today):
    """[(day, spent, ceiling)] for days of today's credit month whose logged spend passed that day's ceiling."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from api_batch import ceiling_today, month_start
    import datetime
    start, over = month_start(today), []
    for d in sorted({str(r.get("day")) for r in lines if r.get("day")}):
        try:
            day = datetime.date.fromisoformat(d)
        except ValueError:
            continue
        if start <= day <= today:
            ceiling, spent, _ = ceiling_today(lines, day)
            if spent > ceiling + 1e-9:
                over.append((d, spent, ceiling))
    return over


def api_row():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from api_batch import read_spend
    import datetime
    over = api_days_over(read_spend(), datetime.date.today())
    text = "; ".join("API spend over the day's ceiling %s: US$%.2f against US$%.2f" % o for o in over)
    return ("WRONG", text) if over else ("OK", "every day of this credit month within its ceiling")


def checks():
    rows = []

    def row(name, state, value):
        rows.append((name, state, value))

    v = ps("$s=Get-ItemProperty 'HKLM:\\SOFTWARE\\Microsoft\\WindowsUpdate\\UX\\Settings' -ErrorAction SilentlyContinue; \"$($s.ActiveHoursStart) $($s.ActiveHoursEnd)\"")
    row("windows update active hours", "OK" if v.split() == [str(x) for x in EXPECT["active_hours"]] else "WRONG", v)
    v = ps("Test-Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\WindowsUpdate\\Auto Update\\RebootRequired'")
    row("restart pending", "OK" if v == "False" else "WRONG", v)
    v = ps("powercfg /getactivescheme")
    row("power plan", "OK" if EXPECT["power_scheme"] in v else "WRONG", v[-60:])
    v = ps("powercfg /q SCHEME_CURRENT SUB_SLEEP STANDBYIDLE | Select-String 'Current AC'")
    row("sleep on mains", "OK" if v.strip().endswith("0x00000000") else "WRONG", v.split(":")[-1].strip() if v else "unread")
    v = ps("powercfg /q SCHEME_CURRENT SUB_SLEEP HIBERNATEIDLE | Select-String 'Current AC'")
    row("hibernate on mains", "OK" if v.strip().endswith("0x00000000") else "WRONG", v.split(":")[-1].strip() if v else "unread")
    for t in EXPECT["tasks_ready"] + EXPECT["tasks_disabled"]:
        st = ps("(Get-ScheduledTask -TaskName '%s' -ErrorAction SilentlyContinue).State" % t)
        want = "Disabled" if t in EXPECT["tasks_disabled"] else "Ready"
        row("task " + t, "OK" if st == want or (want == "Ready" and st == "Running") else "WRONG", st or "missing")
    for letter in ("C", "F"):
        free = shutil.disk_usage(letter + ":\\").free / 1e9
        row("drive %s: free" % letter, judge_drive(letter, free), "%.1f GB (floor %d)" % (free, EXPECT["floors_gb"][letter]))
    row("runner startup shortcut", "OK" if os.path.isfile(STARTUP) else "WRONG", "present" if os.path.isfile(STARTUP) else "missing")
    v = ps("(Get-Process Runner.Listener -ErrorAction SilentlyContinue | Measure-Object).Count")
    row("build machine listener", "OK" if v not in ("", "0") else "WRONG", "running" if v not in ("", "0") else "not running")
    bad = judge_agents(agent_lines(os.path.join(REPO, ".claude", "agents")), EXPECT["agents"])
    row("helpers' models and effort", "OK" if not bad else "WRONG", "; ".join(bad) or "as set")
    try:
        import datetime
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import token_audit
        d = datetime.datetime.combine(datetime.date.today(), datetime.time())
        out = token_audit.audit(d, d + datetime.timedelta(days=1))
        row("catch-all helpers today", *judge_catch_all(out["whoModels"], out["usd"]))
    except Exception as e:
        row("catch-all helpers today", "WARN", "not read: %s" % e)
    for name in ("ANTHROPIC_MODEL", "LEDGER_TALK_CORE_MODEL"):
        row("env " + name, "OK" if not os.environ.get(name) else "WRONG", "set" if os.environ.get(name) else "not set")
    base = os.environ.get("ANTHROPIC_BASE_URL", "")
    row("env ANTHROPIC_BASE_URL", "OK" if base in ("", EXPECT["base_url"]) else "WRONG", base or "not set")
    try:
        user = json.load(open(os.path.join(os.path.expanduser("~"), ".claude", "settings.json"), encoding="utf-8"))
    except Exception:
        user = {}
    mode = (user.get("permissions") or {}).get("defaultMode")
    row("permissions never bypassed", "OK" if mode != "bypassPermissions" else "WRONG", mode or "no default mode")
    row("API spend per day", *api_row())
    row("switchModelsOnFlag", "OK" if not user.get("switchModelsOnFlag") else "WRONG", str(user.get("switchModelsOnFlag", False)))
    return rows


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("settings_check selftest FAIL " + name)
    check("matching helpers pass", judge_agents(dict(EXPECT["agents"]), EXPECT["agents"]) == [])
    moved = dict(EXPECT["agents"], extractor=("opus", "medium"))
    check("a helper moved to a dearer model is named", judge_agents(moved, EXPECT["agents"]) == ["extractor opus/medium, expected sonnet/medium"])
    check("a missing helper is named", len(judge_agents({}, EXPECT["agents"])) == len(EXPECT["agents"]))
    check("F: under its floor is wrong", judge_drive("F", 19.5) == "WRONG")
    check("F: just above the floor warns", judge_drive("F", 20.9) == "WARN")
    check("C: with room is fine", judge_drive("C", 60) == "OK")
    import datetime
    d = datetime.date
    spend = [{"day": "2026-11-05", "usd": 100.0}, {"day": "2026-11-12", "usd": 5.0}, {"day": "2026-11-13", "usd": 30.0}]
    over = api_days_over(spend, d(2026, 11, 13))
    check("a day past its ceiling is named", [o[0] for o in over] == ["2026-11-13"])
    check("its ceiling is the credit left over the days left", abs(over[0][2] - 195.0 / 29) < 1e-9 if over else False)
    check("a day within its ceiling passes", api_days_over(spend, d(2026, 11, 12)) == [])
    check("a day of last month is not judged", api_days_over([{"day": "2026-11-05", "usd": 100.0}], d(2026, 11, 13)) == [])
    check("no catch-all helper passes", judge_catch_all({"research-reader on claude-sonnet-5-5": (2.0, 60)}, 80.0)[0] == "OK")
    st, val = judge_catch_all({"claude on claude-opus-5-5": (10.0, 137), "general-purpose on claude-opus-5-5": (1.0, 9),
                               "research-reader on claude-sonnet-5-5": (2.0, 60)}, 100.0)
    check("a catch-all helper is named with its share", st == "WRONG" and "146 steps US$11.00 (11.0%" in val and "research-reader" in val)
    print("settings_check selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    rows = checks()
    for name, state, value in rows:
        print("settings-check %-30s %-5s %s" % (name, state, value))
    print("settings-check wrong=%d warn=%d" % (sum(r[1] == "WRONG" for r in rows), sum(r[1] == "WARN" for r in rows)))
