#!/usr/bin/env python3
"""THE THIRTY-MINUTE SESSION, PLAYED AND COUNTED (proof P4 (a), production/research/pre-production/3-PROOFS.md).

    python tools/long_session.py --request [DATE]        # ask for one night run (writes the request file; plays nothing)
    python tools/long_session.py --play                  # play it now, by day (refused near the night jobs)
    python tools/long_session.py --report DIR [DATE]     # the table again from a run's folder (plays nothing)
    python tools/long_session.py --selftest

Run with no arguments or with --help it prints this text and plays nothing.

WHY. P4: "the AI tester plays 30 real minutes from New Game in the packaged build, as a player would", part (a)
on the stand-in talk, and logs each minute: what happened; who saw the deed; who mentioned it later and how;
"that's all I know" counts; reply delays; minutes with nothing to do; anything that broke the illusion. Pass: a
minute-by-minute table whose empty minutes become the content list for the friends' build.

HOW IT PLAYS. Reference games: none found (no studied game publishes how its testers log a long session minute
by minute). So it reuses the nightly walk's own pieces (tools/route_walk.py): its real key presses through the AI
tester (tools/ai-tester/play.py, stand-in talk, -TalkFake, never a key), New Game, Sheila's walk round, the first
talk, the deed at Rita's window, then a varied loop until thirty real minutes have passed since New Game: talk to
Sheila, Ron and Darren in turn wherever their day has them (a different line each time, some naming the others or
the window), wander to a street place from the cast file and look round, go back to look at the window, and at
night press Z as a player would rather than stand in the dark. Nothing stands idle as filler: a minute in which
nothing happened is counted, never hidden. Then Esc and Q, so the game's record ends "quit".

THE CLOCK. The game's clock runs at two game minutes a real second (LiveClock.h, MinutesPerRealSecond = 2.0)
whatever the player does, so thirty real minutes cover about sixty game hours less the Z waits. Each minute's
row carries the game clock the tester read at its start. (P4's known issue: the clock runs while the tester
thinks; this tester is a script with no model, so it thinks for well under a second between commands.)

WHAT IT WRITES. production/playtest/p4/<date>-session.json and .md: one row a real minute, built only from the
game's own session record (Saved/Sessions, production/specs/session-record.md) and the walk's own action log
(actions.json in the run's folder); a minute with no line in either says so. A totals block and the empty
minutes list follow. Pictures stay where the tester saves them; the run's folder is on F:.

THE NIGHT. tools/nightly_walk.py runs it once, after the night's report is written, only when
production/playtest/nightly/long-session-request.json names tonight (its "date" the night's own date or the
day before it) and the session can end by NIGHT_DEADLINE (15 minutes before retention at 03:30); else the
request waits for the next night. It is renamed before play, so it runs once. With no request file nothing
changes in the nightly walk.
"""
import datetime as dt
import glob
import json
import math
import os
import re
import statistics
import sys
import threading
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))

OUT_DIR = os.path.join(REPO, "production", "playtest", "p4")
REQUEST = os.path.join(REPO, "production", "playtest", "nightly", "long-session-request.json")
SESSIONS = "F:/LedgerTools/played-game/Windows/LedgerProbe/Saved/Sessions"
NIGHT_ROOT = "F:/LedgerTools/nightly"
TOWN = {"lena": "Sheila", "rocco": "Ron", "sam": "Darren"}

DURATION_S = 30 * 60
# THE BUDGET, from the code's own limits: the start (route_walk.start, close then launch, ~1.7 min on 18 Nov from
# the walk's start to the record's first line) allowed 3 min; the play 30 min; the quit (route_walk waits up to 60 s
# for the game to close, then close and 5 s) 2 min.
START_S, QUIT_S = 3 * 60, 2 * 60
NEEDED_S = START_S + DURATION_S + QUIT_S
# An activity begun just before the end can run on (walk_to_person's legs: go_to, 14 legs of up to ~5 s, by road
# and follow, twice); the watchdog closes the game WATCHDOG_S (10 min) after the end at the latest, after which every
# step returns at once, so a night run is over by about 03:25. So the night's hard stop is 15 minutes before retention (03:30), and
# a run starts only if NEEDED_S ends by then.
NIGHT_DEADLINE = (3, 15)
WATCHDOG_S = 600                        # review F3: a game still open 10 minutes after the end is closed by tree
GUARD_S = 300                           # nothing long (the first talk, the deed) begun in the last 5 minutes
NIGHT_WINDOW = ((1, 15), (4, 30))       # 15 minutes before the walk to the morning pictures' 04:15 plus margin
SLOW_S = 2.0                            # P2's target: the first word heard within 2 s
FALLBACK = {"fallback", "ladder-refuse"}  # TalkHelper Program.cs: fellBack = the "that's all I know" wording or the ladder's refusal
BROKE = {"fallback", "refused", "brush", "paused", "ladder-refuse", "cut", "walkedOff"}
CONTENT = {"deed", "witness", "known", "talk", "reply", "hint", "ask", "police", "ellis", "taken", "tea", "found",
           "trust", "week", "calls", "onlookers", "reacted", "gathered", "named"}
STREET_PLACES = ("ritas_step", "kiosk", "fish_front", "mickeys_rank", "quay", "cafe_front", "laundry_front",
                 "adas_step", "bus_stop")

# The lines Tom says, in turn; {other} is another of the three, {greet} by the clock. Plain newcomer's talk, so what
# each answers comes from what they remember.
LINES = (
    "{greet}. Anything going on round here?",
    "Somebody put Rita's window in. Did you see who?",
    "I'm new here. Who should I ask about work?",
    "What do you make of {other}?",
    "Has anybody been asking about me?",
    "Quiet today. Is it always like this?",
    "Where does a man get a cup of tea round here?",
    "Did {other} say anything about the window?",
)


def log(msg):
    print("long %s %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


def name_of(key):
    return TOWN.get(key, str(key or "?").capitalize())


def at_local(day, hm):
    """The epoch of hh:mm local on the given date."""
    return time.mktime(dt.datetime.combine(day, dt.time(hm[0], hm[1])).timetuple())


# ---------------------------------------------------------------- the request

def write_request(date, path=REQUEST):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"date": date, "what": "proof P4 (a): one thirty-minute session on the stand-in talk",
                   "asked": time.strftime("%Y-%m-%d %H:%M")}, fh, indent=1)
    return path


def read_request(path=REQUEST):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def request_for(req, night_date):
    """'run', 'wait' (a later night's) or 'stale' (older than the night before), for the night of night_date."""
    if not req or not re.match(r"^\d{4}-\d{2}-\d{2}$", str(req.get("date", ""))):
        return "stale"
    d = dt.date.fromisoformat(req["date"])
    n = dt.date.fromisoformat(night_date)
    if d > n:
        return "wait"
    return "run" if (n - d).days <= 1 else "stale"


def consume(path, night_date, how):
    """Renamed once: long-session-request.<night>.<how>.json beside it; never read again."""
    to = os.path.join(os.path.dirname(path), "long-session-request.%s.%s.json" % (night_date, how))
    if os.path.exists(to):
        os.remove(to)
    os.replace(path, to)
    return to


def fits_night(now, deadline=NIGHT_DEADLINE):
    """True when a run started now ends (NEEDED_S) by the night's hard stop."""
    d = dt.datetime.fromtimestamp(now).date()
    return now + NEEDED_S <= at_local(d, deadline)


def clear_of_night(now):
    """A run by day must not reach into the night jobs' window (01:15 to 04:30)."""
    d = dt.datetime.fromtimestamp(now).date()
    for day in (d, d + dt.timedelta(days=1)):
        a, b = at_local(day, NIGHT_WINDOW[0]), at_local(day, NIGHT_WINDOW[1])
        if now < b and now + NEEDED_S + 15 * 60 > a:
            return False
    return True


def night_run(night_date, night, path=REQUEST, log=log, now=None, runner=None):
    """Called by nightly_walk.py after its report, only when the request file exists. Returns what it did."""
    req = read_request(path)
    state = request_for(req, night_date)
    if state == "wait":
        log("long session: the request names a later night (%s); left for it" % req.get("date"))
        return {"did": "waiting"}
    if state == "stale":
        to = consume(path, night_date, "stale")
        log("long session: the request was unreadable or older than the night before; set aside as %s" % os.path.basename(to))
        return {"did": "stale"}
    now = time.time() if now is None else now
    if not fits_night(now):
        # moved to the next night (review F2), or the next night would read it as older than the night before
        req["date"] = (dt.date.fromisoformat(night_date) + dt.timedelta(days=1)).isoformat()
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(req, fh, indent=1)
        log("long session: too late to end by %02d:%02d (needs %d min); the request waits for the next night" % (
            NIGHT_DEADLINE[0], NIGHT_DEADLINE[1], NEEDED_S // 60))
        return {"did": "deferred"}
    taken = consume(path, night_date, "ran")       # renamed BEFORE play: a crash never makes it run twice
    out = os.path.join(night, "long-session")
    log("long session: play (request %s)" % os.path.basename(taken))
    stop_at = at_local(dt.datetime.fromtimestamp(now).date(), NIGHT_DEADLINE)
    rep = (runner or play_session)(out, night_date, hard_stop=stop_at)
    log("long session: done, %s" % ((rep or {}).get("headline") or "no table"))
    return {"did": "ran", "request": taken, "report": rep}


# ---------------------------------------------------------------- the play

class Actions:
    """The walk's own log: each thing the tester did, its wall times and the game clock it read."""
    def __init__(self):
        self.rows = []

    def add(self, t0, what, kind, ok=True, detail="", clock=""):
        self.rows.append({"t0": round(t0, 2), "t1": round(time.time(), 2), "what": what, "kind": kind,
                          "ok": bool(ok), "detail": detail, "clock": clock})
        log("%-7s %s%s" % (kind, what, "" if ok else "  (" + detail + ")"))


def play_session(out, date, hard_stop=None, sessions=SESSIONS, out_dir=OUT_DIR):
    """Plays the session in the packaged game and writes the table. Launches the game: never from a test."""
    import route_walk as rw
    saved = rw.PACKAGED_SAVED
    os.makedirs(out, exist_ok=True)
    save_dir = "F:/LedgerTools/tmp/long-session/" + time.strftime("%Y-%m-%d-%H%M")
    for name in ("route-checks.jsonl", "route-where.txt"):
        try:
            os.remove(os.path.join(saved, name))
        except OSError:
            pass
    since = time.time()
    r = rw.Route(saved, out)
    acts = Actions()
    unsent = []

    def play(*args):
        last = rw.play(*args)
        if "NOT-IN-FRONT" in last:
            unsent.append({"at": time.time(), "cmd": str(args[0]) if args else "?"})
        return last

    def clock():
        t = r.where().get("tom")
        return " ".join(t[3:5]) if t and len(t) >= 5 else ""

    # THE GAME IS ALWAYS CLOSED (review F1, 18 Nov): an error anywhere still closes it, by play.py and then by tree
    # (close_games: taskkill /F /T), so the morning pictures never find it open; a watchdog (F3) closes it if the
    # loop runs on past its end by WATCHDOG_S.
    st = {"play_start": since, "stop": "the run stopped on an error"}
    dogs = []
    try:
        st["stop"] = _run(r, play, acts, clock, save_dir, hard_stop, st, dogs)
    except Exception as e:
        acts.add(time.time(), "the run stopped on an error", "error", False, "%s: %s" % (type(e).__name__, e))
    finally:
        for d in dogs:
            d.cancel()
        try:
            play("close")
            import close_games
            close_games.close_games(log=log)
        except Exception as e:
            log("cleanup failed: %s" % e)
    try:
        r.write()
    except Exception as e:
        log("verdict not written: %s" % e)
    return finish(out, date, since, st["play_start"], acts, unsent, st["stop"], sessions=sessions, out_dir=out_dir)


def watchdog(end_at, closer=None):
    """A daemon timer that closes every game WATCHDOG_S after end_at (review F3). Cancelled when the run ends."""
    if closer is None:
        import close_games
        closer = lambda: close_games.close_games(log=log)
    w = threading.Timer(max(0.0, end_at + WATCHDOG_S - time.time()), closer)
    w.daemon = True
    w.start()
    return w


def _run(r, play, acts, clock, save_dir, hard_stop, st, dogs):
    import route_walk as rw
    play("close")
    t0 = time.time()
    if not rw.start(False, save_dir, []):
        acts.add(t0, "the game did not start", "start", False, rw.START_SAID[0][:120])
        return "the game did not start"
    if hard_stop and time.time() >= hard_stop - GUARD_S:
        acts.add(t0, "started under 5 minutes before the night's hard stop: not played", "start", False, "too late")
        return "the night's hard stop"
    play("press", "Enter")                                                  # New game
    st["play_start"] = play_start = time.time()
    end_at = play_start + DURATION_S
    if hard_stop:
        end_at = min(end_at, hard_stop)
    dogs.append(watchdog(end_at))
    if not r.expect("street", 60):
        acts.add(play_start, "New Game chosen; play never began", "start", False, "no street line")
        return "play never began"
    acts.add(play_start, "New Game chosen", "start", clock=clock())
    t0 = time.time()
    for _ in range(14):                                                     # Sheila's walk round, page by page
        if r.where().get("tom"):
            break
        play("press", "Enter")
        play("wait", "3")
    acts.add(t0, "Sheila's walk round, read to its end", "story", bool(r.where().get("tom")), clock=clock())
    if time.time() < end_at - GUARD_S:
        talk(r, play, acts, "lena", rw.LINE, clock)
    if time.time() < end_at - GUARD_S:
        deed(r, play, acts, clock)
    loop(r, play, acts, clock, end_at)
    stop = "thirty minutes played" if time.time() >= play_start + DURATION_S - 30 else "the night's hard stop"
    t0 = time.time()
    play("press", "Esc")
    play("wait", "1")
    play("press", "Q")
    gone = False
    import subprocess
    for _ in range(60):
        if "LedgerProbe.exe" not in subprocess.run(["tasklist"], capture_output=True, text=True).stdout:
            gone = True
            break
        time.sleep(1)
    acts.add(t0, "Esc, then Q: quit", "quit", gone, "" if gone else "still running a minute after Q")
    return stop


def finish(out, date, since, play_start, acts, unsent, stop, sessions=SESSIONS, out_dir=OUT_DIR):
    with open(os.path.join(out, "actions.json"), "w", encoding="utf-8") as fh:
        json.dump({"since": since, "play_start": play_start, "stop": stop, "actions": acts.rows, "unsent": unsent}, fh, indent=1)
    return report(out, date, sessions=sessions, out_dir=out_dir)


def talk(r, play, acts, key, line, clock):
    """To one of the three wherever their day has them, and the line said (route_walk.greet's way)."""
    import route_walk as rw
    t0, who = time.time(), name_of(key)
    c = clock()
    w = r.where()
    if key not in w or "tom" not in w:
        return acts.add(t0, "looked for %s" % who, "talk", False, "%s is not on the street" % who, c)
    rw.walk_to_person(r, key, 1.1)
    w = r.where()
    if not (w.get("tom") and key in w):
        return acts.add(t0, "walked toward %s" % who, "talk", False, "lost sight of %s" % who, c)
    r.turn_to(rw.bearing(w["tom"][0], w["tom"][1], w[key][0], w[key][1]))
    w = r.where()
    d = math.hypot(w[key][0] - w["tom"][0], w[key][1] - w["tom"][1]) if (w.get("tom") and key in w) else 99.0
    if key in w and d > w[key][2]:
        r.go_to(0, 0, tol=0.4, legs=6, follow=rw.follow_aim(key, 0.9))
        w = r.where()
        if w.get("tom") and key in w:
            r.turn_to(rw.bearing(w["tom"][0], w["tom"][1], w[key][0], w[key][1]))
            w = r.where()
            d = math.hypot(w[key][0] - w["tom"][0], w[key][1] - w["tom"][1])
    if key not in w or d > w[key][2]:
        return acts.add(t0, "walked toward %s" % who, "talk", False, "never in reach of %s (%.1f m)" % (who, d), c)
    for st in ("talk-open", "talk-typed", "reply-words", "reply-heard"):
        r.discard(st)
    play("say", line)
    opened = r.wait_stage("talk-open", 10)
    words = r.wait_stage("reply-words", 40)
    r.wait_stage("reply-heard", 40)
    play("wait", "6")
    said = r.said_back()
    ok = bool(opened and words) and said == line
    return acts.add(t0, "talked to %s: \"%s\"" % (who, line), "talk", ok,
                    "" if ok else ("no box" if not opened else "no answer" if not words else "said %r, not as typed" % said), c)


def deed(r, play, acts, clock):
    """The walk's deed: by the road to Rita's window, facing it, E."""
    import route_walk as rw
    t0, c = time.time(), clock()
    w = r.where()
    if "window" in w and "tom" in w:
        wx, wz, reach = w["window"][0], w["window"][1], w["window"][2]
        r.by_road(wx, wz - min(1.0, reach * 0.6), tol=0.3)
        t = r.where().get("tom")
        if t:
            r.turn_to(rw.bearing(t[0], t[1], wx, wz))
    w = r.where()
    if "window" in w and "tom" in w and math.hypot(w["window"][0] - w["tom"][0], w["window"][1] - w["tom"][1]) <= w["window"][2]:
        r.discard("deed")
        play("press", "E")
        got = r.wait_stage("deed", 15)
        acts.add(t0, "broke Rita's window (E)", "deed", bool(got), "" if got else "no deed line", c)
    else:
        acts.add(t0, "went to Rita's window", "deed", False, "never in reach of it", c)
    play("wait", "6")


def street_places():
    with open(os.path.join(REPO, "production", "specs", "hook-cast.json"), encoding="utf-8") as fh:
        places = json.load(fh)["places"]
    return [(k, places[k]["x_m"], places[k]["z_m"]) for k in STREET_PLACES if k in places]


def wander(r, play, acts, clock, place):
    t0, c = time.time(), clock()
    key, x, z = place
    got = r.by_road(x, z, tol=0.8)
    for _ in range(4):                                                      # a look round, as a newcomer would
        play("turn", "90")
        play("wait", "1")
    acts.add(t0, "walked to %s and looked round" % key.replace("_", " "), "wander", got, "" if got else "did not arrive", c)


def look_at_window(r, play, acts, clock):
    import route_walk as rw
    t0, c = time.time(), clock()
    w = r.where()
    if "window" not in w or "tom" not in w:
        return acts.add(t0, "went back to Rita's window", "wander", False, "the window is not reported", c)
    got = r.by_road(w["window"][0], w["window"][1] - 2.0, tol=0.8)
    t = r.where().get("tom")
    if t:
        r.turn_to(rw.bearing(t[0], t[1], w["window"][0], w["window"][1]))
    play("wait", "4")
    acts.add(t0, "went back to look at Rita's window", "wander", got, "" if got else "did not arrive", c)


def night_now(clock_text):
    m = re.search(r"(\d+):(\d+)", clock_text or "")
    return bool(m) and (int(m.group(1)) >= 22 or int(m.group(1)) < 7)


def loop(r, play, acts, clock, end_at):
    """Talk, wander, talk, the window, talk, wander... until end_at; at night Z, as a player would."""
    places = street_places()
    turn, said, wandered = 0, 0, 0
    order = ("lena", "wander", "rocco", "window", "sam", "wander")
    while time.time() < end_at - 20:
        c = clock()
        if night_now(c):
            t0 = time.time()
            play("press", "Z")
            play("wait", "8")
            acts.add(t0, "waited out the night (Z)", "wait", True, "now %s" % clock(), c)
            continue
        step = order[turn % len(order)]
        turn += 1
        if step == "wander":
            wander(r, play, acts, clock, places[wandered % len(places)])
            wandered += 1
        elif step == "window":
            look_at_window(r, play, acts, clock)
        else:
            others = [n for k, n in TOWN.items() if k != step]
            hour = int(re.search(r"(\d+):", c).group(1)) if re.search(r"(\d+):", c) else 10
            line = LINES[said % len(LINES)].format(other=others[said % 2],
                                                   greet="Morning" if hour < 12 else "Afternoon" if hour < 17 else "Evening")
            said += 1
            talk(r, play, acts, step, line, clock)


# ---------------------------------------------------------------- the table

def file_start(path):
    """Saved/Sessions/<yyyy-mm-dd-hhmmss>.jsonl: the local time the session started."""
    m = re.match(r"(\d{4}-\d{2}-\d{2}-\d{6})", os.path.basename(path))
    return time.mktime(time.strptime(m.group(1), "%Y-%m-%d-%H%M%S")) if m else os.path.getmtime(path)


def read_record(since, folder=SESSIONS):
    """Every line of the session files begun since the run started, with "_at", its local epoch."""
    events = []
    for f in sorted(glob.glob(os.path.join(folder, "*.jsonl"))):
        st = file_start(f)
        if st < since - 60:
            continue
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                if isinstance(e.get("t"), (int, float)):
                    e["_at"] = st + e["t"]
                    e["_file"] = os.path.basename(f)
                    events.append(e)
    return sorted(events, key=lambda e: e["_at"])


def kind(e):
    return e.get("e") or ""


def build_table(events, actions, play_start, minutes, unsent=()):
    """One row a real minute from New Game, from the record's lines and the walk's actions, nothing else."""
    rows = [{"minute": m + 1, "clock": "", "happened": [], "saw_deed": [], "mentioned_later": [], "thats_all_i_know": 0,
             "reply_delays": [], "nothing_to_do": "", "broke_illusion": [], "_content": False, "_lines": 0,
             "_where": ""} for m in range(minutes)]

    def at(ts):
        return max(0, min(minutes - 1, int((ts - play_start) // 60)))
    deed_at = {}
    for e in events:
        if kind(e) == "deed":
            deed_at.setdefault(e.get("what"), e["_at"])
        if kind(e) == "ask" and e.get("story"):
            deed_at.setdefault(e["story"], e["_at"])
    places = {}
    for e in events:
        row, k = rows[at(e["_at"])], kind(e)
        row["_lines"] += 1
        row["_content"] |= k in CONTENT
        if k == "place":
            places.setdefault(row["minute"], []).append(e.get("at", "?"))
            row["_where"] = e.get("at", "?")
        elif k == "deed":
            row["happened"].append("deed: %s" % e.get("what"))
            row["saw_deed"] += [name_of(w) for w in (e.get("seen") or [])]
        elif k == "witness" and e.get("saw") is True:
            row["saw_deed"].append(name_of(e.get("who")) + (" (the glass only)" if e.get("rung") == 0 else ""))
        elif k == "known":
            later = e.get("story") in deed_at and e["_at"] >= deed_at[e["story"]]
            row["mentioned_later"].append("%s (%s, %s%s)" % (name_of(e.get("who")), e.get("how", "?"), e.get("story", "?"),
                                                             "" if later else ", not a deed of this session"))
        elif k == "talk":
            row["happened"].append("talked to %s" % name_of(e.get("who")))
        elif k == "reply":
            s = e.get("s")
            how = e.get("how", "?")
            if isinstance(s, (int, float)):
                row["reply_delays"].append("%s %.1f s" % (name_of(e.get("who")), s))
                if s > SLOW_S:
                    row["broke_illusion"].append("slow reply: %s %.1f s" % (name_of(e.get("who")), s))
            if how in FALLBACK:
                row["thats_all_i_know"] += 1
            if how in BROKE:
                row["broke_illusion"].append("reply %s: %s" % (how, name_of(e.get("who"))))
        elif k == "wait":
            row["happened"].append("waited %s to %s" % (e.get("from", "?"), e.get("to", "?")))
            row["clock"] = row["clock"] or e.get("from", "")
        elif k == "still":
            row["happened"].append("stood still %ss at %s" % (e.get("s"), e.get("at", "?")))
        elif k == "end":
            row["happened"].append("session ended: %s" % e.get("why"))
            if e.get("why") == "crash":
                row["broke_illusion"].append("the game crashed")
        elif k in ("hint", "ask", "police", "ellis", "taken", "tea", "found", "trust", "week", "calls", "gathered", "named"):
            detail = {"hint": e.get("moment"), "ask": e.get("answer") or "night %s" % e.get("night"),
                      "police": "%s told them (%s)" % (name_of(e.get("who")), e.get("how")), "ellis": e.get("why"),
                      "taken": e.get("end"), "tea": e.get("state"), "found": "%s found %s" % (name_of(e.get("who")), e.get("damage")),
                      "trust": name_of(e.get("who")), "week": e.get("answer"),
                      "calls": "%s calls him %s" % (name_of(e.get("who")), e.get("name")),
                      "gathered": "%s people" % e.get("people"), "named": "named %s" % ", ".join(name_of(n) for n in e.get("names") or [])}[k]
            row["happened"].append("%s: %s" % (k, detail))
    for m, ps in places.items():
        rows[m - 1]["happened"].insert(0, "passed " + ", ".join(dict.fromkeys(p.replace("_", " ") for p in ps)))
    for a in actions:
        row = rows[at(a["t0"])]
        row["_lines"] += 1
        row["clock"] = row["clock"] or a.get("clock", "")
        row["happened"].append("tester: " + a["what"] + ("" if a.get("ok", True) else " (failed: %s)" % a.get("detail", "")))
        if not a.get("ok", True):
            row["broke_illusion"].append("tester: " + a.get("detail", a["what"]))
        for m in range(at(a["t0"]) + 1, at(a.get("t1", a["t0"])) + 1):    # a long walk spans minutes: say so in each
            rows[m]["_lines"] += 1
            rows[m]["happened"].append("tester (still at it): " + a["what"])
    for u in unsent:
        rows[at(u["at"])]["broke_illusion"].append("the tester's keys did not reach the game (%s): not in front" % u["cmd"])
    where = ""
    for row in rows:
        where = row["_where"] or where
        if row["_lines"] == 0:
            row["happened"] = ["no record: neither the game's session record nor the walk's log has a line in this minute"]
            row["nothing_to_do"] = "no record"
        elif not row["_content"]:
            row["nothing_to_do"] = "yes"
        else:
            row["nothing_to_do"] = "no"
        row["where"] = where
    return rows


def totals(rows, events):
    replies = [e for e in events if kind(e) == "reply"]
    secs = [e["s"] for e in replies if isinstance(e.get("s"), (int, float))]
    end = next((e for e in reversed(events) if kind(e) == "end"), None)
    saw = sorted({e.get("who") for e in events if kind(e) == "witness" and e.get("saw") is True and e.get("rung") != 0}
                 | {w for e in events if kind(e) == "deed" for w in (e.get("seen") or [])})
    glass = sorted({e.get("who") for e in events if kind(e) == "witness" and e.get("saw") is True and e.get("rung") == 0} - set(saw))
    later = sorted({"%s (%s)" % (name_of(e.get("who")), e.get("how")) for e in events if kind(e) == "known"})
    return {
        "minutes": len(rows),
        "minutes_with_record": sum(1 for r in rows if r["nothing_to_do"] != "no record"),
        "minutes_nothing_to_do": sum(1 for r in rows if r["nothing_to_do"] == "yes"),
        "minutes_no_record": sum(1 for r in rows if r["nothing_to_do"] == "no record"),
        "deeds": sum(1 for e in events if kind(e) == "deed"),
        "saw_the_deed": [name_of(w) for w in saw],
        "took_in_the_glass_only": [name_of(w) for w in glass],
        "mentioned_later": later,
        "talks": sum(1 for e in events if kind(e) == "talk"),
        "replies": len(replies),
        "thats_all_i_know": sum(r["thats_all_i_know"] for r in rows),
        "reply_seconds_median": round(statistics.median(secs), 1) if secs else None,
        "reply_seconds_max": round(max(secs), 1) if secs else None,
        "slow_replies": sum(1 for s in secs if s > SLOW_S),
        "broke_illusion": sum(len(r["broke_illusion"]) for r in rows),
        "still_seconds": sum(e.get("s", 0) for e in events if kind(e) == "still" and isinstance(e.get("s"), (int, float))),
        "ended": (end or {}).get("why", "no end line"),
        "talk_usd": (end or {}).get("usd"),
        "source": "the game's own session record and the walk's action log; replies are the stand-in's words with the "
                  "real voice, not the real path, so the delays and the \"that's all I know\" count measure the stand-in",
    }


def empty_list(rows):
    """The minutes with nothing to do, each with where and when, and what the tester did meanwhile."""
    out = []
    for r in rows:
        if r["nothing_to_do"] == "yes":
            did = [h.replace("tester: ", "").replace("tester (still at it): ", "") for h in r["happened"] if h.startswith("tester")]
            out.append("minute %d%s%s: %s" % (r["minute"], ", " + r["clock"] if r["clock"] else "",
                                              " near " + r["where"].replace("_", " ") if r["where"] else "",
                                              "; ".join(did) or "; ".join(r["happened"]) or "nothing recorded but movement"))
    return out


def cell(xs):
    s = "; ".join(xs) if isinstance(xs, list) else str(xs)
    return (s or "-").replace("|", "/").replace("\n", " ")


def markdown(date, rows, tot, empty, stop):
    head = ["# The thirty-minute session, %s (proof P4 (a), the stand-in talk)" % date, "",
            "Played by the AI tester from New Game in the packaged build; stopped: %s. Every row comes from the game's own "
            "session record and the walk's action log; a minute with neither says so." % stop, "",
            "| min | game clock | what happened | who saw the deed | who mentioned it later, and how | \"that's all I know\" "
            "| reply delays | nothing to do | broke the illusion |",
            "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        head.append("| %d | %s | %s | %s | %s | %d | %s | %s | %s |" % (
            r["minute"], cell(r["clock"]), cell(r["happened"]), cell(r["saw_deed"]), cell(r["mentioned_later"]),
            r["thats_all_i_know"], cell(r["reply_delays"]), r["nothing_to_do"], cell(r["broke_illusion"])))
    head += ["", "## Totals", ""]
    head += ["- %s: %s" % (k.replace("_", " "), cell(v) if isinstance(v, list) else v) for k, v in tot.items()]
    head += ["", "## Empty minutes (the content list for the friends' build)", ""]
    head += ["- " + e for e in empty] or ["- none"]
    return "\n".join(head) + "\n"


def report(run_dir, date, sessions=SESSIONS, out_dir=OUT_DIR):
    with open(os.path.join(run_dir, "actions.json"), encoding="utf-8") as fh:
        st = json.load(fh)
    events = read_record(st["since"], sessions)
    ends = [a["t1"] for a in st["actions"]] + [e["_at"] for e in events] + [st["play_start"] + 60]
    minutes = max(1, int(math.ceil((max(ends) - st["play_start"]) / 60.0)))
    rows = build_table(events, st["actions"], st["play_start"], minutes, st.get("unsent", ()))
    tot = totals(rows, events)
    empty = empty_list(rows)
    clean = [{k: v for k, v in r.items() if not k.startswith("_")} for r in rows]
    rep = {"date": date, "proof": "P4 (a)", "stop": st.get("stop"), "run_dir": run_dir, "rows": clean, "totals": tot,
           "empty_minutes": empty, "passed_length": minutes >= 30 and st.get("stop") == "thirty minutes played",
           "headline": "%d minutes played, %d with nothing to do, %d with no record, %d broke the illusion" % (
               tot["minutes"], tot["minutes_nothing_to_do"], tot["minutes_no_record"], tot["broke_illusion"])}
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, date + "-session.json"), "w", encoding="utf-8") as fh:
        json.dump(rep, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(out_dir, date + "-session.md"), "w", encoding="utf-8") as fh:
        fh.write(markdown(date, clean, tot, empty, st.get("stop")))
    return rep


# ---------------------------------------------------------------- selftest

def selftest():
    import tempfile
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("long_session selftest FAIL " + name)
    P = 1000.0

    def ev(minute, sec, **k):
        return dict(k, _at=P + minute * 60 + sec, t=minute * 60 + sec)
    events = [ev(0, 2, e="start", player="jafar", fresh=True),
              ev(0, 30, e="talk", who="lena"), ev(0, 33, e="reply", who="lena", how="own", s=0.2),
              ev(2, 10, e="witness", who="rocco", saw=True, rung=2), ev(2, 10, e="witness", who="sam", saw=True, rung=2),
              ev(2, 10, e="witness", who="rita", saw=True, rung=0), ev(2, 10, e="witness", who="hal", saw=False, rung=0),
              ev(2, 10, e="deed", what="player.window_d0"),
              ev(3, 5, e="place", at="kiosk"), ev(4, 40, e="still", s=25, at="kiosk"),
              ev(5, 12, e="known", who="rocco", how="remark", story="player.window_d0"),
              ev(6, 1, e="place", at="fish_front"),
              ev(7, 20, e="talk", who="rocco"), ev(7, 22, e="reply", who="rocco", how="fallback", s=0.3),
              ev(8, 3, e="place", at="quay"),
              ev(9, 15, e="talk", who="sam"), ev(9, 20, e="reply", who="sam", how="own", s=4.8),
              ev(10, 50, e="end", why="quit", usd=0.002)]
    acts = [{"t0": P + 0.5, "t1": P + 40, "what": "talked to Sheila", "kind": "talk", "ok": True, "clock": "D0 09:40"},
            {"t0": P + 125, "t1": P + 131, "what": "broke Rita's window (E)", "kind": "deed", "ok": True, "clock": "D0 13:50"},
            {"t0": P + 181, "t1": P + 300, "what": "walked to kiosk and looked round", "kind": "wander", "ok": True, "clock": "D0 15:40"},
            {"t0": P + 600, "t1": P + 650, "what": "looked for Sheila", "kind": "talk", "ok": False,
             "detail": "Sheila is not on the street", "clock": "D0 23:40"}]
    rows = build_table(events, acts, P, 12)
    check("the deed's minute names the two who saw it and the one who took in the glass only",
          rows[2]["saw_deed"] == ["Ron", "Darren", "Rita (the glass only)"])
    check("one who did not see it is not named", not any("Hal" in s for r in rows for s in r["saw_deed"]))
    check("a later mention says who and how, and that it was this session's deed",
          rows[5]["mentioned_later"] == ["Ron (remark, player.window_d0)"])
    check("\"that's all I know\" counted in its minute", rows[7]["thats_all_i_know"] == 1 and sum(r["thats_all_i_know"] for r in rows) == 1)
    check("reply delays listed per minute", rows[0]["reply_delays"] == ["Sheila 0.2 s"] and rows[9]["reply_delays"] == ["Darren 4.8 s"])
    check("a slow reply breaks the illusion", "slow reply: Darren 4.8 s" in rows[9]["broke_illusion"])
    check("the fallback is named as a break", "reply fallback: Ron" in rows[7]["broke_illusion"])
    check("minutes of walking only are nothing to do", [r["minute"] for r in rows if r["nothing_to_do"] == "yes"] == [4, 5, 7, 9, 11])
    check("a minute with no line anywhere says so", rows[1]["nothing_to_do"] == "no record" and rows[11]["nothing_to_do"] == "no record" and rows[11]["happened"][0].startswith("no record"))
    check("a long walk is carried into the minutes it spans", any("still at it" in h for h in rows[4]["happened"]))
    check("a failed look for someone is said, in the table and as a break",
          any("failed: Sheila is not on the street" in h for h in rows[10]["happened"]) and rows[10]["broke_illusion"])
    tot = totals(rows, events)
    check("totals: one deed, two saw, one glass only, one later mention",
          tot["deeds"] == 1 and tot["saw_the_deed"] == ["Ron", "Darren"] and tot["took_in_the_glass_only"] == ["Rita"]
          and tot["mentioned_later"] == ["Ron (remark)"])
    check("totals: replies, the median and the slow one", tot["replies"] == 3 and tot["reply_seconds_median"] == 0.3 and tot["slow_replies"] == 1)
    check("totals: empty minutes and no-record minutes apart", tot["minutes_nothing_to_do"] == 5 and tot["minutes_no_record"] == 2)
    em = empty_list(rows)
    check("the empty list gives the minute, the clock and where", em[0].startswith("minute 4, D0 15:40 near kiosk"))
    md = markdown("2026-11-19", rows, tot, em, "thirty minutes played")
    check("the table has the seven columns besides minute and clock",
          all(c in md for c in ("what happened", "who saw the deed", "who mentioned it later, and how", "\"that's all I know\"",
                                "reply delays", "nothing to do", "broke the illusion")) and md.count("\n| ") == 13)
    # a relaunch writes a second file: its lines are placed by its own start time
    with tempfile.TemporaryDirectory() as td:
        a, b = os.path.join(td, "2026-11-19-020000.jsonl"), os.path.join(td, "2026-11-19-021000.jsonl")
        open(a, "w").write('{"t":0.0,"e":"start","player":"jafar"}\n{"t":30.0,"e":"talk","who":"lena"}\n')
        open(b, "w").write('{"t":5.0,"e":"talk","who":"sam"}\nnot json\n')
        rec = read_record(file_start(a), td)
        check("two session files are read in order, each by its own start", [e.get("who") for e in rec if kind(e) == "talk"] == ["lena", "sam"]
              and abs(rec[-1]["_at"] - file_start(a) - 605.0) < 1e-6)
        # the whole report from a run folder: json and md written
        run = os.path.join(td, "run")
        os.makedirs(run)
        json.dump({"since": file_start(a), "play_start": file_start(a), "stop": "thirty minutes played", "actions": []},
                  open(os.path.join(run, "actions.json"), "w"))
        rep = report(run, "2026-11-19", sessions=td, out_dir=os.path.join(td, "p4"))
        check("the report writes <date>-session.json and .md", os.path.exists(os.path.join(td, "p4", "2026-11-19-session.md"))
              and rep["totals"]["talks"] == 2 and not rep["passed_length"])
        # the request: consumed once, deferred when late, a later night's left alone
        req = os.path.join(td, "long-session-request.json")
        night = dt.date(2026, 11, 19)
        early = at_local(night, (2, 15))
        calls = []
        runner = lambda out, date, hard_stop=None: calls.append((date, hard_stop)) or {"headline": "fake"}
        quiet = lambda m: None
        write_request("2026-11-18", req)                                    # dropped by day for "tonight"
        first = night_run("2026-11-19", td, req, log=quiet, now=early, runner=runner)
        second = night_run("2026-11-19", td, req, log=quiet, now=early, runner=runner) if os.path.exists(req) else None
        check("a request is run once and renamed", first["did"] == "ran" and len(calls) == 1 and second is None
              and os.path.exists(os.path.join(td, "long-session-request.2026-11-19.ran.json")))
        check("the run is given the night's hard stop", calls[0][1] == at_local(night, NIGHT_DEADLINE))
        write_request("2026-11-19", req)
        late = night_run("2026-11-19", td, req, log=quiet, now=at_local(night, (2, 45)), runner=runner)
        check("too late to end by the hard stop: deferred, the file kept", late["did"] == "deferred" and os.path.exists(req) and len(calls) == 1)
        write_request("2026-11-21", req)
        check("a later night's request waits", night_run("2026-11-19", td, req, log=quiet, now=early, runner=runner)["did"] == "waiting"
              and os.path.exists(req))
        write_request("2026-11-10", req)
        check("an old request is set aside, not played", night_run("2026-11-19", td, req, log=quiet, now=early, runner=runner)["did"] == "stale"
              and not os.path.exists(req) and len(calls) == 1)
        # F2: a deferred request is moved to the next night, which runs it
        write_request("2026-11-18", req)
        d1 = night_run("2026-11-19", td, req, log=quiet, now=at_local(night, (2, 45)), runner=runner)
        d2 = night_run("2026-11-20", td, req, log=quiet, now=at_local(dt.date(2026, 11, 20), (2, 15)), runner=runner)
        check("a request deferred on the 19th runs on the 20th, not set aside as stale (F2)",
              d1["did"] == "deferred" and d2["did"] == "ran" and calls[-1][0] == "2026-11-20")
        # F1: an error mid-run still closes the game, by play.py and by tree
        import route_walk as rw
        import close_games
        saved_fns = (rw.play, rw.start, rw.Route, rw.PACKAGED_SAVED, close_games.close_games, globals()["talk"])
        played, closed = [], []

        class FakeRoute:
            def __init__(self, saved, out):
                self.out = out
            def expect(self, *a):
                return True
            def where(self):
                return {"tom": [0.0, 0.0, 0.0, "D0", "09:00"]}
            def write(self):
                return {}

        def boom(*a, **k):
            raise RuntimeError("the talk fell over")
        try:
            rw.play = lambda *a: played.append(a) or "ok"
            rw.start = lambda *a, **k: True
            rw.Route, rw.PACKAGED_SAVED = FakeRoute, td
            close_games.close_games = lambda dry=False, log=print: closed.append(1) or 0
            globals()["talk"] = boom
            rep = play_session(os.path.join(td, "f1"), "2026-11-19", sessions=td, out_dir=os.path.join(td, "p4f1"))
        finally:
            rw.play, rw.start, rw.Route, rw.PACKAGED_SAVED, close_games.close_games, globals()["talk"] = saved_fns
        check("an error mid-run still closes the game, by play.py then by tree, and the table says why (F1)",
              closed == [1] and played[-1] == ("close",) and rep["stop"] == "the run stopped on an error"
              and not rep["passed_length"])
    # F3: the watchdog fires WATCHDOG_S after the end
    fired = threading.Event()
    w = watchdog(time.time() - WATCHDOG_S + 0.05, closer=fired.set)
    check("the watchdog closes the game after the end (F3)", fired.wait(5.0))
    w.cancel()
    later = watchdog(time.time() + 60, closer=fired.clear)
    later.cancel()
    check("a cancelled watchdog does nothing", fired.is_set())
    check("the budget: 35 minutes, the latest night start 02:40",
          NEEDED_S == 35 * 60 and fits_night(at_local(night, (2, 40))) and not fits_night(at_local(night, (2, 41))))
    check("a day run near the night jobs is refused, by day it is allowed",
          not clear_of_night(at_local(night, (0, 50))) and not clear_of_night(at_local(night, (3, 0))) and clear_of_night(at_local(night, (14, 0))))
    src = open(__file__, encoding="utf-8").read()
    check("the stand-in talk only: no real-talk start", src.count("--real" + "-talk") == 0 and "rw.start(False, save_dir, [])" in src)
    check("night: Z at 23:10 and 03:00, not at 09:00", night_now("D1 23:10") and night_now("D2 03:00") and not night_now("D1 09:00"))
    check("the street places are in the cast file", len(street_places()) == len(STREET_PLACES))
    check("each line fills", all("{" not in l.format(other="Ron", greet="Morning") for l in LINES))
    print("long_session selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--request" in argv:
        i = argv.index("--request")
        date = argv[i + 1] if i + 1 < len(argv) and re.match(r"^\d{4}-\d{2}-\d{2}$", argv[i + 1]) else dt.date.today().isoformat()
        print("longSession request=%s date=%s" % (write_request(date), date))
        return 0
    if "--report" in argv:
        i = argv.index("--report")
        run_dir = argv[i + 1]
        date = argv[i + 2] if i + 2 < len(argv) else dt.date.today().isoformat()
        print(report(run_dir, date)["headline"])
        return 0
    if "--play" in argv:
        if not clear_of_night(time.time()):
            print("longSession REFUSED: it would reach the night jobs' window (01:15 to 04:30)")
            return 2
        date = dt.date.today().isoformat()
        rep = play_session(os.path.join(NIGHT_ROOT, date, "long-session-day"), date)
        print("longSession " + rep["headline"])
        return 0
    print(__doc__)                                                          # no arguments, --help, anything else: plays nothing
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
