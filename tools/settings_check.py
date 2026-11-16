#!/usr/bin/env python3
"""THE SETTINGS OUTSIDE THE REPOSITORY THAT CAN RAISE COST OR STOP WORK, read once a day.

    python tools/settings_check.py            # one line per setting, then 'settings-check wrong=N'
    python tools/settings_check.py --selftest

WHY. His decision of 16 Nov 14:12 (advisor 182, item 2): list every setting outside the repository that can
raise cost or stop work and give each a check read at the start or in the DAILY file, like the model check of
14 Nov (tools/fresh_gate.py). The list and where each lives: production/research/token-audit/SETTINGS-SWEEP-2026-11-16.md.
This reads; it changes nothing. A key's value is never printed, only 'set' or 'not set'.
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


def judge_drive(letter, free_gb):
    if free_gb < EXPECT["floors_gb"][letter]:
        return "WRONG"
    return "WARN" if free_gb < EXPECT["warn_gb"][letter] else "OK"


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
    print("settings_check selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    rows = checks()
    for name, state, value in rows:
        print("settings-check %-30s %-5s %s" % (name, state, value))
    print("settings-check wrong=%d warn=%d" % (sum(r[1] == "WRONG" for r in rows), sum(r[1] == "WARN" for r in rows)))
