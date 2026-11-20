"""The consequence checker for the LEDGER prototype (lane task 4t, piece 5). Code, no model.

His words (19 Nov): every reaction traces to a chain of sightings and tellings, no line repeated, nothing wrong for
1990, his content rules kept. Method: the game's state is taken as a trace of snapshots (its own saved week, which
holds every event, every person's memories with their source, and every telling), and each rule is a property
checked over that trace, as runtime monitoring does for games (Varvaressos, "Etude de faisabilite du runtime
monitoring dans les jeux video", UQAC, Jan 2014: game-state snapshots each loop, bugs written as properties over the
trace). Every belief carries its source the way Talk of the Town's characters do (Ryan, Summerville, Mateas,
Wardrip-Fruin, AIIDE workshop 2015): saw, heard, was part of it, or was told by someone, so each one can be walked
back to the act itself.

Two ways to run it:

    python consequences.py --dist DIR [--hours 12] [--out DIR]     its own run: a stretch of game hours, scenes
                                                                     taken with their first choice, sampled
    python consequences.py --hidden DIR [--out DIR]                  a played session: play.py's hidden folder
                                                                     (start_save.json, actions.jsonl, final_save.json
                                                                     or the newest save_NNNN.json)

The rules (each result: rule, ok, and what it was about):
  1. every memory names a real event and was formed no earlier than the event
  2. a "saw" memory: the person is among the event's witnesses; a "was part of it" memory: the person is among the
     event's parties when it has any (a story seed or the detective's asking records none: counted, not failed)
  3. a "heard" memory was formed within minutes of the act (a sighting event the game reuses for two hours is
     exempt: anyone may hear it again later)
  4. a "told" memory: a telling from that teller to that person about that event is recorded, and the teller knew
     it first; walking the tellers back always ends at someone who saw, heard or was part of it (no loops)
  5. every recorded telling left the memory it should
  6. reactions with no memory behind them are listed as a warning, not failed: talk, fares and scenes move regard
     without a memory by design, and a passer-by who walks off again loses memories but keeps feelings
  7. no line repeated: a spoken line of five words or more shown again after 10 game minutes off screen (any speaker)
  8. nothing wrong for 1990: words of later years or of another country (fail list and warn list)
  9. the content rule: the content words (machine_checks.FAIL_WORDS) in every line shown or logged
A check that cannot run (the save's shape changed, no session file) fails. A rule that ran but had nothing to check
in this stretch (no tellings, no sounds, no spoken lines) is reported "not reached" (ok null), never as a pass; the
gate lists those in its note. Page errors other than the missing art (404) fail.
"""
import argparse
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

HEARD_WITHIN_MIN = 10        # a sound is heard as it happens: game minutes allowed after the act
MOVED = 0.02                 # regard or fear that moved more than this since the start is a reaction
REPEAT_MIN_WORDS = 5         # shorter lines ("Evening.", "Taxi!") may come round again
REPEAT_GAP_MIN = 10          # off the screen this many game minutes, then shown again: a repeat
SPOKEN_TAGS = ("face",)      # the game's log lines that people say to Tom (the "talk" tag holds Tom's own lines)
SPEAKER_PREFIX = re.compile(r"^[^:]{1,60}? said it to his face:\s*")

# words of later years or of another country, never right in Britain in 1990
FAIL_1990 = [
    "internet", "e-mail", "email", "emails", "website", "websites", "web site", "online", "smartphone",
    "text message", "texting", "texted", "wifi", "wi-fi", "dvd", "dvds", "mp3", "ipod", "iphone", "google", "googled",
    "facebook", "twitter", "selfie", "emoji", "brexit", "covid", "euro", "euros", "premier league", "national lottery",
    "playstation", "eurostar", "channel tunnel train", "two pound coin", "£2 coin", "sat nav", "satnav", "sat-nav",
    "cell phone", "cellphone", "zip code", "gas station", "parking lot", "sidewalk", "apartment", "cop car",
]
# often fine but worth a look ("mobile" existed as a car phone; Major became Prime Minister on 28 Nov 1990)
WARN_1990 = ["mobile", "mobile phone", "laptop", "cd", "cds", "cd-rom", "atm", "pc", "computer", "fax", "pager",
             "bleeper", "major", "blair", "millennium", "cashpoint", "trainers", "mum", "gotten", "truck", "cop", "cops"]


def _rx(words):
    return re.compile(r"(?<![\w-])(" + "|".join(re.escape(w) for w in sorted(words, key=len, reverse=True)) + r")(?![\w-])", re.I)


RX_FAIL_1990, RX_WARN_1990 = _rx(FAIL_1990), _rx(WARN_1990)


def res(rule, ok, **kw):
    return dict({"rule": rule, "ok": None if ok is None else bool(ok)}, **kw)


def finish(out, counts, rules):
    """Each rule's real count; a rule with no fault passes only if it had something to check, else "not reached"."""
    for rule in rules:
        n = counts.get(rule, 0)
        for o in out:
            if o["rule"] == rule:
                o["checked"] = n
        if not any(o["rule"] == rule for o in out):
            out.append(res(rule, True, checked=n) if n else res(rule, None, checked=0, steps="not reached: nothing to check in this stretch"))
    return out


TRACE_RULES = ("a memory names a real event", "a memory is formed no earlier than its event", "a sighting has its witness",
               "a part in it has its party", "a sound is heard as it happens", "a telling names its teller",
               "a telling is recorded", "a teller knew it first", "a chain of tellings ends at the act",
               "a telling leaves a memory")


# ---------- rules 1 to 6: the chain of sightings and tellings, over one saved week ----------
def trace(save, start=None):
    """Pure: the trace rules over one saved week (LEDGER.saveText() parsed). start: the save at the start, for the
    reactions warning. Returns (results, notes)."""
    out, notes, n = [], [], {}

    def count(rule):
        n[rule] = n.get(rule, 0) + 1
    try:
        events = {E["id"]: E for E in save["events"]}
        minds = save["minds"]
        transfers = save["transfers"]
    except (KeyError, TypeError) as e:
        return [res("trace: the save could be read", False, steps="not reached: the save has no %s" % e)], notes
    reused = set((save.get("sightIdx") or {}).values())  # sighting events the game reuses for a stretch of hours
    told_by = set((T.get("a"), T.get("b"), T.get("e")) for T in transfers)
    mem = {pid: {r["e"]: r for r in (m.get("mem") or [])} for pid, m in minds.items()}
    seeded = 0
    src_n = {}
    for pid, m in minds.items():
        for r in m.get("mem") or []:
            src = r.get("src")
            src_n[src] = src_n.get(src, 0) + 1
            E = events.get(r.get("e"))
            count("a memory names a real event")
            if E is None:
                out.append(res("a memory names a real event", False, person=pid, steps="event %s is not in the week" % r.get("e")))
                continue
            count("a memory is formed no earlier than its event")
            if r.get("t", 0) + 0.5 < E.get("t", 0):
                out.append(res("a memory is formed no earlier than its event", False, person=pid,
                               steps="event %s (%s) at minute %s, remembered from minute %s" % (E["id"], E.get("kind"), E.get("t"), r.get("t"))))
            if src == "saw":
                count("a sighting has its witness")
                if pid not in (E.get("wit") or []):
                    out.append(res("a sighting has its witness", False, person=pid,
                                   steps="%s saw event %s (%s) but is not among its witnesses" % (pid, E["id"], E.get("kind"))))
            elif src == "self":
                if E.get("party"):
                    count("a part in it has its party")
                    if pid not in E["party"]:
                        out.append(res("a part in it has its party", False, person=pid,
                                       steps="%s was part of event %s (%s); its parties are %s" % (pid, E["id"], E.get("kind"), ", ".join(E["party"]))))
                else:
                    seeded += 1
            elif src == "heard":
                if E["id"] in reused:
                    continue
                count("a sound is heard as it happens")
                if r.get("t", 0) > E.get("t", 0) + HEARD_WITHIN_MIN:
                    out.append(res("a sound is heard as it happens", False, person=pid,
                                   steps="event %s (%s) at minute %s, heard at minute %s" % (E["id"], E.get("kind"), E.get("t"), r.get("t"))))
            elif src == "told":
                frm = r.get("from")
                count("a telling names its teller")
                if not frm:
                    out.append(res("a telling names its teller", False, person=pid, steps="event %s: told, by nobody" % E["id"]))
                    continue
                count("a telling is recorded")
                if (frm, pid, E["id"]) not in told_by:
                    out.append(res("a telling is recorded", False, person=pid,
                                   steps="%s holds event %s (%s) as told by %s; no such telling recorded" % (pid, E["id"], E.get("kind"), frm)))
                if frm == "someone":
                    continue
                if frm not in minds:
                    notes.append("teller %s has left the week; %s's memory of event %s not walked back" % (frm, pid, E["id"]))
                    continue
                count("a teller knew it first")
                tr = mem.get(frm, {}).get(E["id"])
                if tr is None:
                    out.append(res("a teller knew it first", False, person=pid,
                                   steps="%s told %s about event %s and holds no memory of it" % (frm, pid, E["id"])))
                elif tr.get("t", 0) > r.get("t", 0) + 0.5:
                    out.append(res("a teller knew it first", False, person=pid,
                                   steps="%s told %s about event %s at minute %s but learned it at %s" % (frm, pid, E["id"], r.get("t"), tr.get("t"))))
    # walking back: every chain of tellings ends at a root (saw, heard, part of it, or a passer-by), with no loop
    for pid, m in minds.items():
        for r in m.get("mem") or []:
            if r.get("src") != "told":
                continue
            count("a chain of tellings ends at the act")
            seen, cur, who = set(), r, pid
            while cur is not None and cur.get("src") == "told":
                if who in seen:
                    out.append(res("a chain of tellings ends at the act", False, person=pid,
                                   steps="event %s: the tellers go round in a loop (%s)" % (r["e"], " > ".join(sorted(seen)))))
                    break
                seen.add(who)
                who = cur.get("from")
                if who in (None, "someone") or who not in minds:
                    break
                cur = mem.get(who, {}).get(r["e"])
    for T in transfers:
        b, e = T.get("b"), T.get("e")
        if b not in minds:
            continue
        count("a telling leaves a memory")
        if e not in mem.get(b, {}):
            out.append(res("a telling leaves a memory", False, person=b, steps="told event %s by %s at minute %s; no memory of it" % (e, T.get("a"), T.get("t"))))
    # reactions with no memory: a warning only (talk, fares, scenes and passers-by move feelings without memories)
    if start is None:
        notes.append("no start save: reactions with no memory not looked at")
    else:
        smind = start.get("minds", {})
        quiet = []
        for pid, m in minds.items():
            if re.match(r"^(c|lad)\d+$", pid) or m.get("mem"):
                continue
            s = smind.get(pid, {})
            dr, df = abs((m.get("regard") or 0) - (s.get("regard") or 0)), (m.get("fear") or 0) - (s.get("fear") or 0)
            if dr > MOVED or df > MOVED:
                quiet.append("%s (regard %+.2f, fear %+.2f)" % (pid, (m.get("regard") or 0) - (s.get("regard") or 0), df))
        if quiet:
            notes.append("warning: feelings moved with no memory behind them (talk, fares or scenes, or a fault): " + "; ".join(quiet[:12]))
    notes.append("memories %d (saw %d, heard %d, part of it %d, told %d); tellings %d; part-of-it memories with no party "
                 "recorded (story seeds, not failed) %d" % (sum(src_n.values()), src_n.get("saw", 0), src_n.get("heard", 0),
                                                            src_n.get("self", 0), src_n.get("told", 0), len(transfers), seeded))
    return finish(out, n, TRACE_RULES), notes


# ---------- rules 7 to 9: the words ----------
def appearances(frames, gap=None):
    """frames: [(game minute, [line, ...])] in order. A line counts as shown again only when it had been off the
    screen for more than `gap` game minutes (a line that stays up, or flickers between two samples or two sources,
    is one showing). Returns {line: [game minutes of each showing]}."""
    gap = REPEAT_GAP_MIN if gap is None else gap
    out, last = {}, {}
    for minute, lines in frames:
        for l in set(l.strip() for l in lines if l and l.strip()):
            if l not in last or minute - last[l] > gap:
                out.setdefault(l, []).append(minute)
            last[l] = minute
    return out


WORD_RULES = ("no line repeated", "nothing wrong for 1990", "the content rule in what is shown")


def words_rules(frames, logged=()):
    """frames: spoken lines over time (game minutes); logged: other lines shown or logged (1990 and content only)."""
    from machine_checks import FAIL_WORDS
    out, warns = [], {}
    app = appearances(frames)
    for line, mins in app.items():
        if len(mins) > 1 and len(re.findall(r"[A-Za-z']+", line)) >= REPEAT_MIN_WORDS:
            out.append(res("no line repeated", False, place=line[:80], steps="shown %d times, at game minutes %s" % (len(mins), ", ".join("%.1f" % m for m in mins[:6]))))
    rx_content = _rx(FAIL_WORDS)
    every = set(app) | set(l.strip() for l in logged if l and l.strip())
    for line in sorted(every):
        for m in RX_FAIL_1990.finditer(line):
            out.append(res("nothing wrong for 1990", False, place=m.group(1).lower(), steps=line[:160]))
        for m in RX_WARN_1990.finditer(line):
            warns.setdefault(m.group(1).lower(), []).append(line[:120])
        for m in rx_content.finditer(line):
            out.append(res("the content rule in what is shown", False, place=m.group(1).lower(), steps=line[:160]))
    counts = {"no line repeated": len([l for l in app if len(re.findall(r"[A-Za-z']+", l)) >= REPEAT_MIN_WORDS]),
              "nothing wrong for 1990": len(every), "the content rule in what is shown": len(every)}
    return finish(out, counts, WORD_RULES), {"lines_checked": len(every), "spoken_lines": len(app),
                                             "warn_1990": {k: {"count": len(v), "first": v[:3]} for k, v in warns.items()}}


def log_lines(save):
    """The saved week's log (the game keeps its last lines only): people's lines to Tom with the speaker's name taken
    off (so one line from two speakers is still a repeat), and every other line."""
    spoken, other = [], []
    for L in (save or {}).get("log") or []:
        if L.get("tag") in SPOKEN_TAGS:
            spoken.append((L.get("t", 0), SPEAKER_PREFIX.sub("", L.get("text", ""))))
        else:
            other.append((L.get("t", 0), L.get("text", "")))
    return spoken, other


# ---------- the two ways in ----------
SAMPLE_JS = """async ([secs, dt, every]) => { const L = LEDGER; let t = 0, chunk = 0, next = 0; const frames = [];
  while (t < secs - 1e-9) { L.tick(dt); t += dt; chunk += dt;
    if (t >= next) { next += every; const m = window.__gate.msgs(); frames.push([L.G.t, m.subs.concat(m.bubbles)]); }
    if (chunk >= 1) { chunk = 0; let n = 0;
      while (n < 40) { const w = L.written.read();
        if (w.open) { frames.push([L.G.t, [String(w.text || '')]]); if (w.choices && w.choices.length) await L.written.choose(0); else await L.written.next(); }
        else if (L.ui.modal) { L.press('Escape'); } else break; n++; L.tick(dt); } } }
  return frames; }"""


def own_run(dist, hours, seed=7):
    """A stretch of game hours with Tom put at a different named place each hour (so people see him and talk)."""
    from clumsy import Proto
    g = Proto(dist, seed=seed)
    try:
        g.clear()
        start = json.loads(g.js("() => LEDGER.saveText()"))
        frames = []
        secs = g.js("() => LEDGER.rules.time.realSecondsPerGameHour")
        places = sorted(g.js("() => Object.keys(LEDGER.places)"))
        for h in range(hours):
            if places:
                g.js("(p) => { if (!LEDGER.ui.modal) LEDGER.goTo(p); }", places[(h * 7) % len(places)])
            frames += g.js(SAMPLE_JS, [secs, 1 / 60, 0.5])
        end = json.loads(g.js("() => LEDGER.saveText()"))
        errors = list(g.errors)
    finally:
        g.close()
    return start, end, [(f[0], f[1]) for f in frames], errors, []


def hidden_run(hidden):
    notes = []

    def load(name):
        p = os.path.join(hidden, name)
        return json.load(open(p)) if os.path.exists(p) else None
    start, end = load("start_save.json"), load("final_save.json")
    used = "final_save.json"
    actions = os.path.join(hidden, "actions.jsonl")
    if not os.path.exists(actions):
        return start, end, None, [], ["no actions.jsonl in the hidden folder"]
    frames, unit_missing = [], 0
    for line in open(actions):
        rec = json.loads(line)
        if "words" not in rec:
            continue
        h = rec.get("hidden") or {}
        gm = (h.get("state") or {}).get("gameMinute")  # game minutes, as the save's log has
        if gm is None or "spoken" not in h:
            unit_missing += 1
            continue
        frames.append((gm, h["spoken"]))
    if unit_missing:
        notes.append("%d rows without the game minute or the spoken lines (an older play.py): left out" % unit_missing)
    if end is None:  # the session never stopped cleanly: the newest save taken every 10 actions
        saves = sorted(f for f in os.listdir(hidden) if re.match(r"save_\d+\.json$", f))
        end, used = (load(saves[-1]), saves[-1]) if saves else (None, None)
    notes.append("save checked: %s" % used)
    errs = os.path.join(hidden, "save_errors.txt")
    if os.path.exists(errs):
        notes.append("saves that could not be taken: " + open(errs).read().strip()[:400])
    sess = load("session.json") or {}
    errors = [e for e in sess.get("errors", []) if not e.startswith("save for the consequence checker failed")]
    return start, end, frames, errors, notes


def check(start, end, frames, errors=(), notes=None):
    results, notes = [], list(notes or [])
    if frames is None:
        return [res("consequence checker ran", False, steps="not reached: " + "; ".join(notes))], notes, {}
    if end is None:
        return [res("trace: the save could be read", False, steps="not reached: no save at the end of the session")], notes, {}
    r, n = trace(end, start)
    results += r
    notes += n
    spoken, other = log_lines(end)
    if end.get("log"):
        notes.append("log lines from game minute %s (the game keeps only its last lines)" % end["log"][0].get("t"))
    w, info = words_rules(sorted(frames + [(t, [s]) for t, s in spoken], key=lambda f: f[0]), [s for _, s in other])
    results += w
    bad = [e for e in errors if "404" not in e]
    results.append(res("no page errors", not bad, steps="; ".join(bad[:3])) if bad else res("no page errors", True))
    return results, notes, info


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist")
    ap.add_argument("--assets")
    ap.add_argument("--hidden")
    ap.add_argument("--hours", type=int, default=12)
    ap.add_argument("--out", default=os.path.join(os.path.expanduser("~"), ".cache", "ledger-consequences",
                                                   datetime.datetime.now().strftime("%Y%m%d-%H%M")))
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    if a.hidden:
        start, end, frames, errors, notes = hidden_run(a.hidden)
    else:
        if not a.dist:
            from clumsy import build_dist
            a.dist = build_dist(a.assets)
        start, end, frames, errors, notes = own_run(a.dist, a.hours)
    results, notes, info = check(start, end, frames, errors, notes)
    summary = {}
    for r in results:
        o = summary.setdefault(r["rule"], {"checked": 0, "failed": 0, "not_reached": False})
        o["checked"] = max(o["checked"], r.get("checked", 0 if r["ok"] is None else 1))
        o["failed"] += 1 if r["ok"] is False else 0
        o["not_reached"] = r["ok"] is None
    rep = {"when": datetime.datetime.now().isoformat(timespec="seconds"), "source": a.hidden or a.dist, "summary": summary,
           "results": results, "notes": notes, "words": info, "page_errors": errors[:20]}
    path = os.path.join(a.out, "consequences.json")
    json.dump(rep, open(path, "w"), indent=1)
    for k, v in summary.items():
        print("%-46s %s" % (k, "not reached" if v["not_reached"] else "%3d checked %3d failed" % (v["checked"], v["failed"])))
    for x in notes[:8]:
        print("note:", x)
    print("report:", path)
    return 1 if any(r["ok"] is False for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
