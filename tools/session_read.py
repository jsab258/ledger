#!/usr/bin/env python3
"""Reads the game's session records (production/specs/session-record.md) and
prints what Jafar's runbook watches for, beside his four notes.

    python tools/session_read.py Saved/Sessions/2026-10-02-193005.jsonl
    python tools/session_read.py Saved/Sessions            # every session in the folder
    python tools/session_read.py --selftest

Town list 6p. It reads and prints; it decides nothing and answers none of his
notes for him. The record can speak to one of them: whether the town reacted to
something the player had done (Meridian condition 2), shown as what the record
saw, for him to weigh against what he watched.
"""
import json
import os
import re
import statistics
import sys

# Each event's fields and their kinds; (required) fields must be there.
STR, NUM, BOOL, STRS = "text", "number", "true/false", "list of text"
FIELDS = {
    "start": {"build": (STR, False), "player": (STR, True), "fresh": (BOOL, False)},
    "place": {"at": (STR, True)},
    "still": {"s": (NUM, True), "at": (STR, False)},
    "deed": {"what": (STR, True), "seen": (STRS, False)},
    "known": {"who": (STR, True), "how": (STR, False), "story": (STR, True)},
    "talk": {"who": (STR, True)},
    "named": {"who": (STR, False), "names": (STRS, True)},
    "load": {"from": (STR, False)},
    "end": {"why": (STR, True)},
}
ENDS = {"quit", "crash"}
PLAYERS = {"friend", "jafar"}
HOWS = {"look", "remark", "recognition", "question", "talk"}
THIRTY = 30 * 60


def kind_ok(value, kind):
    if kind == STR:
        return isinstance(value, str)
    if kind == NUM:
        return isinstance(value, (int, float)) and not isinstance(value, bool) and value == value and abs(value) != float("inf")
    if kind == BOOL:
        return isinstance(value, bool)
    if kind == STRS:
        return isinstance(value, list) and all(isinstance(x, str) for x in value)
    return False


def read(path):
    """The events of one record in order, the lines it could not use, and warnings."""
    events, unread, warn = [], [], []
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    if "\x00" in text:
        return [], ["the file is not UTF-8 (UTF-16?); nothing read"], warn
    for n, raw in enumerate(text.splitlines(), 1):
        raw = raw.strip().lstrip("﻿")
        if not raw:
            continue
        try:
            ev = json.loads(raw)
        except ValueError:
            unread.append(f"line {n}: not JSON")
            continue
        if not isinstance(ev, dict) or not kind_ok(ev.get("t"), NUM) or not isinstance(ev.get("e"), str):
            unread.append(f"line {n}: no readable t or e")
            continue
        spec = FIELDS.get(ev["e"])
        if spec is None:
            unread.append(f"line {n}: unknown event {ev['e']!r}")
            continue
        bad = [f for f, (k, req) in spec.items() if (f in ev and not kind_ok(ev[f], k)) or (req and f not in ev)]
        if bad:
            unread.append(f"line {n}: {ev['e']} with {', '.join(bad)} missing or not {', '.join(spec[f][0] for f in bad)}")
            continue
        extra = [f for f in ev if f not in spec and f not in ("t", "e")]
        if extra:
            loud = " THE RECORD MUST NEVER KEEP WHAT WAS TYPED" if ev["e"] == "named" else ""
            warn.append(f"line {n}: {ev['e']} carries fields the spec does not list: {', '.join(extra)}.{loud}")
        events.append(ev)
    events.sort(key=lambda ev: ev["t"])
    if not events and not unread:
        warn.append("the record is empty")
    starts = [e for e in events if e["e"] == "start"]
    if len(starts) > 1:
        warn.append(f"{len(starts)} starts in one record: more than one session was written here; read as one")
    if not starts and events:
        warn.append("no start: whose session this was is unknown")
    for e in events:
        if e["e"] == "end" and e["why"] not in ENDS:
            warn.append(f"an end the spec does not know: {e['why']!r}")
        if e["e"] == "start" and e["player"] not in PLAYERS:
            warn.append(f"a player the spec does not know: {e['player']!r} (friend or jafar)")
        if e["e"] == "known" and "how" in e and e["how"] not in HOWS:
            warn.append(f"a way of knowing the spec does not know: {e['how']!r}")
        if e["e"] == "still" and e["s"] > e["t"]:
            warn.append(f"a still spell of {e['s']:.0f} s ending at {e['t']:.0f} s would have begun before the session")
    return events, unread, warn


def minute(t):
    return f"{t / 60:.1f}"


def when_from_name(path):
    """The date and time in a record's file name, or None."""
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})-(\d{2})(\d{2})(\d{2})?", os.path.basename(path))
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)} {m.group(4)}:{m.group(5)}" if m else None


def one(events):
    """The facts of one session, as a dict (the printer and the folder both use it)."""
    start = next((e for e in events if e["e"] == "start"), {})
    ends = [e for e in events if e["e"] == "end"]
    end = ends[-1] if ends else None
    length = (end or (events[-1] if events else {"t": 0}))["t"]
    deeds = [e for e in events if e["e"] == "deed"]
    done_at = {}
    for d in deeds:
        done_at.setdefault(d["what"], d["t"])
    knowns = [e for e in events if e["e"] == "known"]
    # THE TOWN REACTING TO SOMETHING HE HAD DONE: a `known` about a story that
    # is a deed of this session, done at or before it (the independent check).
    reacting = [e for e in knowns if e["story"] in done_at and done_at[e["story"]] <= e["t"]]
    before = [e for e in knowns if e["story"] not in done_at]
    early = [e for e in knowns if e["story"] in done_at and done_at[e["story"]] > e["t"]]
    named = {}
    for e in events:
        if e["e"] == "named":
            for who in e["names"]:
                named.setdefault(who, e["t"])
    first = reacting[0] if reacting else None
    return {
        "player": start.get("player"),
        "build": start.get("build", "?"),
        "fresh": start.get("fresh"),
        "loads": sum(1 for e in events if e["e"] == "load"),
        "length": length,
        "end": end["why"] if end else None,
        "places": [(e["t"], e["at"]) for e in events if e["e"] == "place"],
        # A still spell is written when it ends: it began s seconds earlier.
        "still": [(e["t"] - e["s"], e["s"], e.get("at", "?")) for e in events if e["e"] == "still"],
        "talks": [(e["t"], e["who"]) for e in events if e["e"] == "talk"],
        "named": named,
        "deeds": [(e["t"], e["what"], e.get("seen", [])) for e in deeds],
        "reacting": reacting,
        "before": before,
        "early": early,
        "first_known": first,
        "known_by_30": first is not None and first["t"] <= THIRTY,
    }


def describe(k):
    return f"minute {minute(k['t'])}, {k['who']}, {k.get('how', '?')}, about {k['story']}"


def show(path, facts, unread, warn):
    who = facts["player"] or "unknown player"
    when = when_from_name(path)
    out = [f"SESSION {os.path.basename(path)} ({who}{', ' + when if when else ''}, build {facts['build']})"]
    how_began = "a new game" if facts["fresh"] is True else "a game carried on" if facts["fresh"] is False else "start not written"
    out.append(f"  began: {how_began}; saves loaded: {facts['loads']}")
    out.append(f"  ran: {minute(facts['length'])} min, ended: {facts['end'] or 'no end written'}")
    out.append("  went: " + (", ".join(f"{at} ({minute(t)})" for t, at in facts["places"]) or "nowhere recorded"))
    out.append("  still: " + ("; ".join(f"from minute {minute(t)} for {s:.0f} s at {at}" for t, s, at in facts["still"]) or "never for 20 s"))
    out.append("  talked to: " + (", ".join(f"{w} ({minute(t)})" for t, w in facts["talks"]) or "nobody"))
    out.append("  named: " + (", ".join(f"{w} ({minute(t)})" for w, t in sorted(facts["named"].items(), key=lambda kv: kv[1])) or "nobody"))
    out.append("  did: " + ("; ".join(f"{what} ({minute(t)}, seen by {len(seen)})" for t, what, seen in facts["deeds"]) or "nothing the town could hold"))
    out.append("  the town showing it knew something they had done: "
               + ("; ".join(describe(k) for k in facts["reacting"]) or "nothing recorded"))
    if facts["before"]:
        why = ("before it, or a load" if facts["fresh"] is not True or facts["loads"] else "no deed in this record for it")
        out.append(f"  known about something not done in this session ({why}): "
                   + "; ".join(describe(k) for k in facts["before"]))
    if facts["early"]:
        out.append("  known before the deed it is about was done (a fault in the record?): "
                   + "; ".join(describe(k) for k in facts["early"]))
    if facts["player"] == "friend":
        fk = facts["first_known"]
        out.append("  your four notes (production/playtest/RUNBOOK.md):")
        out.append("    1. the graphics mentioned badly in the first couple of minutes: yours")
        out.append("    2. the town reacted to something they had done: yours; the record's first is "
                   + (describe(fk) + (", by thirty" if facts["known_by_30"] else ", after thirty") if fk else "none"))
        out.append("    3. called it alive without being asked: yours")
        out.append("    4. this over KCD2 on a free evening: yours alone")
    for w in warn:
        out.append(f"  warning: {w}")
    for u in unread:
        out.append(f"  unread: {u}")
    return "\n".join(out)


def folder(sessions):
    """What several sessions say together: (path, facts) pairs."""
    friends = [f for _, f in sessions if f["player"] == "friend"]
    mine = [(p, f) for p, f in sessions if f["player"] == "jafar"]
    other = len(sessions) - len(friends) - len(mine)
    out = [f"SESSIONS {len(sessions)}: {len(friends)} friends', {len(mine)} yours" + (f", {other} whose player is not friend or jafar" if other else "")]
    places = {}
    for i, f in enumerate(friends):
        for _, s, at in f["still"]:
            who, secs = places.setdefault(at, (set(), 0.0))
            who.add(i)
            places[at] = (who, secs + s)
    if places:
        ranked = sorted(places.items(), key=lambda kv: (-len(kv[1][0]), -kv[1][1]))[:5]
        out.append("  where friends went still: " + ", ".join(f"{at} ({len(who)} of {len(friends)} friends' sessions, {secs:.0f} s)" for at, (who, secs) in ranked))
    by30 = [f for f in friends if f["known_by_30"]]
    line = f"  the town reacted to something they had done by minute thirty: {len(by30)} of {len(friends)} friends' sessions"
    if by30:
        line += f"; of those {len(by30)}, the median first reaction at minute {minute(statistics.median(f['first_known']['t'] for f in by30))}"
    out.append(line)
    if mine:
        out.append("  your own sessions: " + ", ".join(f"{when_from_name(p) or os.path.basename(p)} for {minute(f['length'])} min" for p, f in mine))
    return "\n".join(out)


def run(target):
    if not os.path.exists(target):
        print(f"no such file or folder: {target}")
        return 2
    paths = sorted(os.path.join(target, n) for n in os.listdir(target) if n.endswith(".jsonl")) if os.path.isdir(target) else [target]
    if not paths:
        print(f"no session records (.jsonl) in {target}")
        return 1
    sessions = []
    for p in paths:
        try:
            events, unread, warn = read(p)
        except OSError as err:
            print(f"SESSION {os.path.basename(p)}: could not be opened ({err})")
            continue
        facts = one(events)
        sessions.append((p, facts))
        print(show(p, facts, unread, warn))
    if os.path.isdir(target):
        print(folder(sessions))
    return 0


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        def write(name, lines, raw_tail="", bom=False):
            p = os.path.join(d, name)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write("\n".join(("﻿" if bom else "") + json.dumps(x) for x in lines) + raw_tail)
            return p

        a = write("2026-10-02-193005.jsonl", [
            {"t": 0, "e": "start", "build": "abc1234", "player": "friend", "fresh": True},
            {"t": 12.0, "e": "place", "at": "mickeys_rank"},
            {"t": 95.5, "e": "talk", "who": "ron"},
            {"t": 101.0, "e": "named", "who": "ron", "names": ["sheila"]},
            {"t": 250.0, "e": "known", "who": "ada", "how": "look", "story": "player.window_d1"},
            {"t": 300.0, "e": "deed", "what": "player.window_d1", "seen": ["darren"]},
            {"t": 400.0, "e": "known", "who": "june", "how": "look", "story": "player.other"},
            {"t": 1400.0, "e": "known", "who": "darren", "how": "remark", "story": "player.window_d1"},
            {"t": 1500.0, "e": "still", "s": 300, "at": "fish_front"},
            {"t": 1550.0, "e": "wobble"},
            {"t": 1560.0, "e": "still", "s": "42", "at": "x"},
            {"t": 1570.0, "e": "named", "who": "ron", "names": ["ada"], "line": "I saw Ada"},
            {"t": 1788.0, "e": "end", "why": "quit"},
        ], "\nnot json\n", bom=True)
        events, unread, warn = read(a)
        f = one(events)
        assert len(unread) == 3 and any("wobble" in u for u in unread) and any("not JSON" in u for u in unread) and any("still with s" in u for u in unread), unread
        assert any("NEVER KEEP WHAT WAS TYPED" in w for w in warn), warn
        # Only a reaction about a deed done by then counts: not ada's (before the
        # deed), not june's (another story); darren's does.
        assert f["first_known"]["who"] == "darren" and f["known_by_30"], f["first_known"]
        assert [k["who"] for k in f["before"]] == ["june"] and [k["who"] for k in f["early"]] == ["ada"]
        assert f["still"] == [(1200.0, 300, "fish_front")] and f["named"] == {"sheila": 101.0, "ada": 1570.0}
        text = show(a, f, unread, warn)
        assert "ended: quit" in text and "quit before" not in text and "from minute 20.0 for 300 s" in text
        assert "the record's first is minute 23.3, darren, remark" in text and "yes" not in text.split("four notes")[1].split("\n")[2]
        assert "2026-10-02 19:30" in text

        b = write("2026-10-03-201500.jsonl", [{"t": 0, "e": "start", "player": "jafar", "fresh": False}, {"t": 5, "e": "load", "from": "slot1"},
                                             {"t": 60, "e": "known", "who": "ron", "how": "question", "story": "player.window_d1"},
                                             {"t": 2400, "e": "end", "why": "quit"}])
        fb = one(read(b)[0])
        assert fb["first_known"] is None and len(fb["before"]) == 1 and fb["loads"] == 1
        tb = show(b, fb, [], [])
        assert "four notes" not in tb and "saves loaded: 1" in tb and "a game carried on" in tb and "not done in this session" in tb
        c = write("2026-10-04-100000.jsonl", [{"t": 0, "e": "start", "player": "friend"}, {"t": 30, "e": "deed", "what": "player.a"},
                                             {"t": 3000, "e": "known", "who": "x", "how": "look", "story": "player.a"},
                                             {"t": 900, "e": "still", "s": 30, "at": "kiosk"}, {"t": 3100, "e": "end", "why": "unplugged"}])
        ec, uc, wc = read(c)
        fc = one(ec)
        assert not fc["known_by_30"] and any("unplugged" in w for w in wc)
        e = write("2026-10-05-100000.jsonl", [{"t": 0, "e": "start", "player": "friend"}, {"t": 800, "e": "still", "s": 30, "at": "kiosk"}])
        empty = write("2026-10-06-100000.jsonl", [])
        assert "the record is empty" in read(empty)[2]
        nostart = write("2026-10-07-100000.jsonl", [{"t": 0, "e": "talk", "who": "ron"}])
        fn = one(read(nostart)[0])
        together = folder([(a, f), (b, fb), (c, fc), (e, one(read(e)[0])), (nostart, fn)])
        assert "3 friends', 1 yours, 1 whose player is not friend or jafar" in together, together
        assert "1 of 3 friends' sessions; of those 1, the median first reaction at minute 23.3" in together, together
        assert together.index("kiosk (2 of 3") < together.index("fish_front (1 of 3"), together
        odd = write("2026-10-08-100000.jsonl", [{"t": 0, "e": "start", "player": "Jafar", "fresh": True}, {"t": 60, "e": "still", "s": 900},
                                               {"t": 70, "e": "known", "who": "x", "how": "stare", "story": "player.b"}])
        eo, uo, wo = read(odd)
        assert any("Jafar" in w for w in wo) and any("stare" in w for w in wo) and any("before the session" in w for w in wo), wo
        assert "no deed in this record for it" in show(odd, one(eo), uo, wo)
        assert "your own sessions: 2026-10-03 20:15 for 40.0 min" in together
        with open(os.path.join(d, "u16.jsonl"), "w", encoding="utf-16") as fh:
            fh.write(json.dumps({"t": 0, "e": "start", "player": "friend"}))
        assert "not UTF-8" in read(os.path.join(d, "u16.jsonl"))[1][0]
        assert run(os.path.join(d, "missing")) == 2
        os.makedirs(os.path.join(d, "none"))
        assert run(os.path.join(d, "none")) == 1
    print("session_read selftest: ok")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(run(sys.argv[1]))
