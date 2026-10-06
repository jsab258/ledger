#!/usr/bin/env python3
"""THE NIGHTLY WALK AND ITS REPORT: does the town visibly know Tom (Jafar, 3 October).

    python tools/nightly_walk.py                 # the night's walk, the bench, the eyes, the report
    python tools/nightly_walk.py --report-only   # the report again from tonight's files
    python tools/nightly_walk.py --selftest

WHY. Jafar, 3 October: "The AI tester tests the core early, since I will not test the game by
hand until it looks right. Add to its nightly walk a short report on whether the town visibly
knows Tom, played the way a player would: who noticed what he did, who mentioned it to him later
and how, how many questions got 'that's all I know', how long each reply took to be heard, and
anything that broke the illusion of a living town. One paragraph in the overview each morning,
with the numbers compared to the night before."

WHAT IT DOES, run at 02:30 by Windows' Task Scheduler (the task "LEDGER nightly walk"):
1. THE WALK, played as a player would (tools/route_walk.py --town, on his played copy of the
   finished game): the route with real key presses, the deed at Rita's window, the town's hours,
   save, quit, Continue, then Sheila, Ron and Darren greeted in turn with the same neutral line.
   The talk is the stand-in (never LEDGER's key: no automated tool may use it), which answers from
   what each character remembers, so what the town knows shows in it.
2. THE GAME'S OWN RECORD of that walk (Saved/Sessions, production/specs/session-record.md): who
   saw the deed, who showed they knew it afterwards and how, every reply's outcome and the seconds
   to its first word heard.
3. "THAT'S ALL I KNOW", counted where the real words are: the town's fixed bench of a newcomer's
   sixty first questions (ledger/ClaimBench firsts, with the game's own talk settings: the rules
   and the plain fallback), through Claude Code on his subscription; no key, no API call.
4. THE EYES: Claude Code, non-interactive, looks at the walk's pictures and the record and names
   what broke the illusion of a living town.
5. THE REPORT, text only (production/playtest/nightly/<date>.json and .md; pictures stay on F:):
   the numbers beside the night before, and the paragraph the builder puts in the overview by 07:30.

EVERY NUMBER SAYS WHERE IT CAME FROM (CLAUDE.md): the walk's reply times are the stand-in's words
with the real voice, not the real path; the bench's count is the real engine's words.
"""
import datetime as dt
import glob
import json
import os
import re
import statistics
import subprocess
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(REPO, "production", "playtest", "nightly")
NIGHT_ROOT = "F:/LedgerTools/nightly"
SESSIONS = "F:/LedgerTools/played-game/Windows/LedgerProbe/Saved/Sessions"
TESTER_RUNS = os.path.join(REPO, "production", "playtest", "ai-tester")
TOWN = {"lena": "Sheila", "rocco": "Ron", "sam": "Darren"}
BROKE = {"fallback", "refused", "brush", "paused"}


def log(msg):
    print("nightly %s %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


def runner_busy():
    out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Runner.Worker.exe"], capture_output=True, text=True).stdout
    return "Runner.Worker.exe" in out


def read_sessions(since_ts):
    """Every event of the session files written since the walk began, in order."""
    events = []
    for f in sorted(glob.glob(os.path.join(SESSIONS, "*.jsonl"))):
        if os.path.getmtime(f) < since_ts:
            continue
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    try:
                        e = json.loads(line)
                        e["_file"] = os.path.basename(f)
                        events.append(e)
                    except ValueError:
                        pass
    return events


def ev_kind(e):
    return e.get("e") or e.get("event") or e.get("kind") or ""


def summarise(events, verdict, bench, eyes):
    """The night's numbers, from the record, the walk's verdict, the bench and the eyes."""
    deeds = [e for e in events if ev_kind(e) == "deed"]
    # WHO SAW IT is the game's witness events, one a person, saw true or false (4 October: the
    # first report read a "seen" field the deed event never carried and said nobody).
    seen = sorted({TOWN.get(e.get("who"), str(e.get("who", "?")).capitalize())
                   for e in events if ev_kind(e) == "witness" and e.get("saw") is True}
                  | {w for e in deeds for w in (e.get("seen") or [])})
    onlookers = [e for e in events if ev_kind(e) == "onlookers"]
    known = [e for e in events if ev_kind(e) == "known"]
    knew = {}
    for e in known:
        knew.setdefault(e.get("who", "?"), set()).add(e.get("how", "?"))
    replies = [e for e in events if ev_kind(e) == "reply"]
    secs = [e["s"] for e in replies if isinstance(e.get("s"), (int, float))]
    police = sorted({e.get("who", "?") for e in events if ev_kind(e) == "police"})
    rows = (verdict or {}).get("rows", [])
    town_rows = [r for r in rows if r["stage"].startswith("town-")]
    return {
        "walk": {"passed": (verdict or {}).get("passed", 0), "stages": (verdict or {}).get("stages", 0),
                 "failed": [r["stage"] + ": " + r["detail"] for r in rows if not r["ok"]][:6]},
        "noticed": {"saw_the_deed": seen, "onlooker_lines": [o.get("who") or o.get("n") or o for o in onlookers][:6]},
        "knew_later": {k: sorted(v) for k, v in sorted(knew.items())},
        "greeted": [{"who": r["stage"][5:], "reached": r["ok"], "detail": r["detail"]} for r in town_rows],
        "replies": {"n": len(replies), "broke": sum(1 for e in replies if e.get("how") in BROKE),
                    # P3, 3 October: how many the claim check passed, from the game's own record.
                    "checked": sum(1 for e in replies if e.get("checked") is True),
                    "by_how": {h: sum(1 for e in replies if e.get("how") == h) for h in sorted({e.get("how") for e in replies})},
                    "seconds_median": round(statistics.median(secs), 1) if secs else None,
                    "seconds_max": round(max(secs), 1) if secs else None,
                    "source": "the walk's stand-in words with the real voice: not the real path"},
        "police_told_by": police,
        "thats_all_i_know": bench,
        "illusion": eyes,
    }


def run_walk(night):
    out = os.path.join(night, "route")
    r = subprocess.run([sys.executable, os.path.join(REPO, "tools", "route_walk.py"), "--town", "--out", out],
                       capture_output=True, text=True, cwd=REPO, timeout=3600)
    with open(os.path.join(night, "walk.log"), "w", encoding="utf-8") as fh:
        fh.write((r.stdout or "") + (r.stderr or ""))
    try:
        return json.load(open(os.path.join(out, "verdict.json"), encoding="utf-8"))
    except (OSError, ValueError):
        return None


def run_bench(night):
    """The town's sixty first questions through the real engine, as the game sets its talk."""
    d = os.path.join(night, "bench")
    os.makedirs(d, exist_ok=True)
    # THE CLAUDE CODE COMMAND BY ITS FULL PATH (4 October: under the scheduled task the bench's
    # sixty calls all failed; its client finds the command by LEDGER_CLAUDE before PATH).
    import shutil
    env = dict(os.environ)
    exe = shutil.which("claude.cmd") or shutil.which("claude") or os.path.join(os.environ.get("APPDATA", ""), "npm", "claude.cmd")
    if exe and os.path.exists(exe):
        env["LEDGER_CLAUDE"] = exe
    try:
        r = subprocess.run(["dotnet", "run", "--project", os.path.join(REPO, "ledger", "ClaimBench"), "-c", "Release", "--",
                            "firsts", "--rules", "--plain", "--dir", d, "--parallel", "4"],
                           capture_output=True, text=True, cwd=REPO, timeout=3600, env=env)
    except subprocess.TimeoutExpired:
        return {"count": None, "of": 60, "note": "the bench ran out of its hour"}
    text = (r.stdout or "") + (r.stderr or "")
    with open(os.path.join(night, "bench.log"), "w", encoding="utf-8") as fh:
        fh.write(text)
    return parse_bench(text)


def parse_bench(text):
    m = re.search(r"firsts: a newcomer's first questions, (\d+) answered \((\d+) failed\): \"that's all I know\" (\d+) \(([^)]*)\)", text)
    if not m:
        return {"count": None, "of": 60, "note": "the bench gave no count (bench.log)"}
    # A BENCH WHOSE CALLS ALL FAILED MEASURED NOTHING (4 October: "0 answered (60 failed)" was
    # reported as "0 of 60", which reads as no newcomer ever brushed off).
    if int(m.group(1)) == 0:
        return {"count": None, "of": 60, "note": "the bench's %s calls all failed, so nothing was measured (bench.log)" % m.group(2)}
    by = {}
    for part in m.group(4).split(","):
        f = part.strip().split()
        if len(f) == 2 and f[1].isdigit():
            by[TOWN.get(f[0], f[0])] = int(f[1])
    return {"count": int(m.group(3)), "of": int(m.group(1)), "failed": int(m.group(2)), "by_who": by,
            "source": "the real engine's words, through Claude Code on the subscription, the game's talk settings"}


def run_eyes(night, since_ts, summary):
    """Claude Code looks at the walk's pictures and names what broke the illusion."""
    runs = [d for d in glob.glob(os.path.join(TESTER_RUNS, "*")) if os.path.isdir(d) and os.path.getmtime(d) >= since_ts]
    pics = sorted(p for d in runs for p in glob.glob(os.path.join(d, "*.png")))
    if not pics:
        return {"lines": [], "note": "no pictures from the walk to look at"}
    step = max(1, len(pics) // 12)
    pics = pics[::step][:12]
    prompt = ("You are a fresh reviewer of a game, a third-person 1990 British port-town game. Below are pictures "
              "from one walk through it, in order, and what the game's own record says happened (JSON). Read each "
              "picture with your Read tool. Name, in at most five short lines, anything that broke the illusion of a "
              "living town (people frozen or in odd poses, someone ignoring an obvious event, replies that do not fit, "
              "visual faults, empty or dead moments), each with the picture's file name. Say NONE if nothing did. "
              "Plain words, no preamble.\n\nRECORD: " + json.dumps(summary)[:3000] + "\n\nPICTURES:\n" + "\n".join(pics))
    import shutil
    exe = shutil.which("claude") or os.path.join(os.environ.get("APPDATA", ""), "npm", "claude.cmd")
    try:
        # the prompt on its input: a scheduled task's command line would mangle its quotes
        r = subprocess.run([exe, "-p", "Follow the instructions given on standard input.", "--allowedTools", "Read"],
                           input=prompt, capture_output=True, text=True, cwd=REPO, timeout=900)
        out = (r.stdout or "").strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        return {"lines": [], "note": "the eyes did not run: %s" % type(e).__name__}
    lines = [l.strip("-• ").strip() for l in out.splitlines() if l.strip()][:5]
    return {"lines": lines, "pictures": len(pics), "source": "Claude Code, non-interactive, on the walk's pictures"}


def previous(date):
    files = sorted(f for f in glob.glob(os.path.join(REPORTS, "*.json")) if os.path.basename(f)[:10] < date)
    if not files:
        return None
    try:
        return json.load(open(files[-1], encoding="utf-8"))
    except (OSError, ValueError):
        return None


def delta(now, before, fmt="%s"):
    if before is None or now is None:
        return fmt % now if now is not None else "not measured"
    d = now - before
    return (fmt % now) + (" (%+g on the night before)" % round(d, 1) if d else " (same as the night before)")


def paragraph(rep, prev):
    s, p = rep["summary"], (prev or {}).get("summary", {})
    w = s["walk"]
    parts = ["**The town and Tom (the AI tester's walk of %s, played as a player would, the stand-in's words):**" % rep["date"]]
    parts.append("the route %d of %d stages%s." % (w["passed"], w["stages"], "" if not w["failed"] else "; failed: " + "; ".join(w["failed"][:2])))
    seen = s["noticed"]["saw_the_deed"]
    parts.append("Who saw him break Rita's window: %s." % (", ".join(seen) if seen else "nobody the record names"))
    kl = s["knew_later"]
    parts.append("Who showed they knew afterwards, and how: %s." % (
        "; ".join("%s (%s)" % (k, ", ".join(v)) for k, v in kl.items()) if kl else "nobody"))
    pk = len(p.get("knew_later", {})) if p else None
    parts.append("That is %s." % delta(len(kl), pk, "%d people"))
    t = s["thats_all_i_know"] or {}
    pt = (p.get("thats_all_i_know") or {}).get("count") if p else None
    parts.append("\"That's all I know\" to a newcomer's sixty first questions (the real engine's words): %s." % delta(t.get("count"), pt, "%s of 60"))
    r = s["replies"]
    pr = (p.get("replies") or {}).get("seconds_median") if p else None
    parts.append("Replies heard after a median %s s, at most %s s (stand-in words, real voice; not the real path), %d of %d broke." % (
        delta(r["seconds_median"], pr, "%s"), r["seconds_max"], r["broke"], r["n"]))
    ill = s["illusion"].get("lines") if s.get("illusion") else None
    parts.append("What broke the illusion: %s." % ("; ".join(ill[:3]) if ill else (s.get("illusion") or {}).get("note", "nothing named")))
    return " ".join(parts)


def report(date, night, since_ts, verdict, bench, eyes):
    events = read_sessions(since_ts)
    summary = summarise(events, verdict, bench, eyes)
    rep = {"date": date, "night": night, "events": len(events), "summary": summary}
    prev = previous(date)
    rep["paragraph"] = paragraph(rep, prev)
    os.makedirs(REPORTS, exist_ok=True)
    with open(os.path.join(REPORTS, date + ".json"), "w", encoding="utf-8") as fh:
        json.dump(rep, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(REPORTS, date + ".md"), "w", encoding="utf-8") as fh:
        fh.write(rep["paragraph"] + "\n")
    return rep


def main():
    date = dt.date.today().isoformat()
    night = os.path.join(NIGHT_ROOT, date)
    os.makedirs(night, exist_ok=True)
    since_ts = time.time()
    if "--report-only" in sys.argv:
        st = json.load(open(os.path.join(night, "state.json"), encoding="utf-8"))
        rep = report(date, night, st["since"], st.get("verdict"), st.get("bench"), st.get("eyes"))
        print(rep["paragraph"])
        return 0
    # THE NIGHT'S PACKAGED BUILD FIRST (Jafar, 6 October: pushes to wip no longer build; the
    # nightly run does), when wip has moved since the played copy; the wait below then holds the
    # walk until the build machine has finished and replaced the copy.
    if "--no-package" not in sys.argv:
        log("package")
        try:
            r = subprocess.run([sys.executable, os.path.join(REPO, "tools", "nightly_package.py")],
                               capture_output=True, text=True, timeout=300)
            log((r.stdout or r.stderr).strip()[:200])
            if "nightlyPackage=ASKED" in r.stdout:
                # the build machine picks the push up within a minute or two: wait for it to start,
                # so the wait below does not find it idle and walk beside its build
                for _ in range(20):
                    if runner_busy():
                        break
                    time.sleep(30)
        except Exception as e:
            log("package request failed: %s" % e)
    for _ in range(90):
        if not runner_busy():
            break
        time.sleep(60)
    log("walk")
    verdict = run_walk(night)
    pre = summarise(read_sessions(since_ts), verdict, None, None)
    log("bench")
    bench = run_bench(night)
    log("eyes")
    eyes = run_eyes(night, since_ts, pre)
    with open(os.path.join(night, "state.json"), "w", encoding="utf-8") as fh:
        json.dump({"since": since_ts, "verdict": verdict, "bench": bench, "eyes": eyes}, fh)
    rep = report(date, night, since_ts, verdict, bench, eyes)
    log("done")
    print(rep["paragraph"])
    return 0


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("nightly_walk selftest FAIL " + name)
    b = parse_bench('firsts: a newcomer\'s first questions, 60 answered (0 failed): "that\'s all I know" 21 (lena 7, rocco 8, sam 6), refused 1; api-rate usd, not billed=0.00 -> firsts.jsonl')
    check("the bench's count and who said it are read", b["count"] == 21 and b["by_who"] == {"Sheila": 7, "Ron": 8, "Darren": 6})
    check("a bench with no count says so", parse_bench("nothing")["count"] is None)
    check("a bench whose calls all failed measured nothing",
          parse_bench("firsts: a newcomer's first questions, 0 answered (60 failed): \"that's all I know\" 0 (), refused 0")["count"] is None)
    # WHO SAW IT from the game's witness events, as it records them (4 October).
    wv = [{"e": "witness", "who": "lena", "saw": True}, {"e": "witness", "who": "hal", "saw": False},
          {"e": "witness", "who": "marta", "saw": True}, {"e": "deed", "what": "player.window_d0"}]
    check("the witnesses who saw it are named, those who did not are not",
          summarise(wv, None, None, None)["noticed"]["saw_the_deed"] == ["Marta", "Sheila"])
    ev = [{"e": "deed", "what": "player.window_d0", "seen": ["Ada", "Rita"]},
          {"e": "known", "who": "Sheila", "how": "question", "story": "player.window_d0"},
          {"e": "known", "who": "Sheila", "how": "look", "story": "player.window_d0"},
          {"e": "reply", "who": "Sheila", "how": "own", "s": 3.2},
          {"e": "reply", "who": "Ron", "how": "fallback", "s": 4.8}]
    v = {"passed": 13, "stages": 14, "rows": [{"stage": "town-Ron", "ok": False, "detail": "never in reach"}]}
    s = summarise(ev, v, {"count": 20, "of": 60}, {"lines": []})
    check("who saw the deed", s["noticed"]["saw_the_deed"] == ["Ada", "Rita"])
    check("who knew later, and how", s["knew_later"] == {"Sheila": ["look", "question"]})
    check("replies, broken ones and the median", s["replies"]["n"] == 2 and s["replies"]["broke"] == 1 and s["replies"]["seconds_median"] == 4.0)
    rep = {"date": "2026-10-04", "summary": s}
    prev = {"summary": dict(s, thats_all_i_know={"count": 23}, knew_later={})}
    para = paragraph(rep, prev)
    check("the paragraph compares with the night before", "(-3 on the night before)" in para and "(+1 on the night before)" in para)
    check("the paragraph says the reply times are not the real path", "not the real path" in para)
    check("the bench runs with the game's own talk settings", "--rules" in open(__file__, encoding="utf-8").read() and "--plain" in open(__file__, encoding="utf-8").read())
    print("nightly_walk selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
