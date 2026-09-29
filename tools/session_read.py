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
    "load": {"from": (STR, False), "deeds": (STRS, False)},
    "end": {"why": (STR, True), "usd": (NUM, False)},
    "reply": {"who": (STR, True), "how": (STR, True), "s": (NUM, False)},
    "hint": {"moment": (STR, True)},
    "ask": {"night": (NUM, True), "answer": (STR, True), "story": (STR, True)},
    "police": {"who": (STR, True), "story": (STR, True), "how": (STR, True)},
    "ellis": {"why": (STR, True), "day": (NUM, False)},
    "taken": {"story": (STR, True), "day": (NUM, True), "end": (STR, False)},
    # The first week's scenes (town list 6cf): Ada's tea, the damage found,
    # Sheila's trust and his answer at the week's end.
    "tea": {"day": (NUM, True), "state": (STR, True)},
    "found": {"who": (STR, True), "damage": (STR, True), "story": (STR, True)},
    "trust": {"who": (STR, True)},
    "week": {"answer": (STR, True), "story": (STR, True)},
}
ENDS = {"quit", "crash"}
PLAYERS = {"friend", "jafar"}
HOWS = {"look", "remark", "recognition", "question", "talk"}
# How a reply went (town list 6bd): all but "own" and "ended" are talk that broke.
WENT = {"own", "fallback", "refused", "brush", "cut", "paused", "ended", "walkedOff"}
BROKE = {"fallback", "refused", "brush", "paused"}
# The hints (FirstMoments) and the answers to the outfit's ask (Arrangement), town list 6bh.
MOMENTS = ["StandingStill", "CanTalk", "FirstAsk", "SeenAtDeed", "OverheardAboutHim", "LedgerOpened"]
ANSWERS = {"did", "refused", "noshow"}
# What the police hold (PoliceFile.Known), town list 6bm.
POLICE_HOW = {"statement", "description", "talk"}
# How a spell in custody ended (Custody.End), town list 6bt.
CUSTODY_ENDS = {"Cautioned", "Charged", "BailedToReturn"}
# How Ada's tea went, once the evening closes (TeaState), and his answer at the
# week's end (WeekAnswer), town list 6cf.
TEA_STATES = {"Stayed", "LeftEarly", "StoodUp"}
WEEK_ANSWERS = {"WindDown", "TakeOver", "WontSay"}
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
        if e["e"] == "reply" and e["how"] not in WENT:
            warn.append(f"a way a reply went the spec does not know: {e['how']!r}")
        if e["e"] == "hint" and e["moment"] not in MOMENTS:
            warn.append(f"a hint the spec does not know: {e['moment']!r}")
        if e["e"] == "ask" and e["answer"] not in ANSWERS:
            warn.append(f"an answer to the ask the spec does not know: {e['answer']!r}")
        if e["e"] == "taken" and "end" in e and e["end"] not in CUSTODY_ENDS:
            warn.append(f"a way custody ends the spec does not know: {e['end']!r}")
        if e["e"] == "tea" and e["state"] not in TEA_STATES:
            warn.append(f"a way Ada's tea went the spec does not know: {e['state']!r}")
        if e["e"] == "week" and e["answer"] not in WEEK_ANSWERS:
            warn.append(f"an answer at the week's end the spec does not know: {e['answer']!r}")
        if e["e"] == "police" and e["how"] not in POLICE_HOW:
            warn.append(f"a way the police hold something the spec does not know: {e['how']!r}")
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
    # A deed held by a loaded save was done before this record began (town list 6bd).
    for e in events:
        if e["e"] == "load":
            for what in e.get("deeds", []):
                done_at.setdefault(what, -1.0)
    for d in deeds:
        done_at.setdefault(d["what"], d["t"])
    # What he did with the outfit's ask is a deed of this session too (town list
    # 6bh); an answer the spec does not know is warned of and is no deed (the
    # independent check of 6bn: a night the ask never reached him is no deed).
    asks = [e for e in events if e["e"] == "ask" and e["answer"] in ANSWERS]
    for a in asks:
        done_at.setdefault(a["story"], a["t"])
    # His answer to Sheila is a deed of this session too: the street learns it
    # (town list 6cf); an answer the spec does not know is none.
    weeks = [e for e in events if e["e"] == "week" and e["answer"] in WEEK_ANSWERS]
    for w in weeks:
        done_at.setdefault(w["story"], w["t"])
    knowns = [e for e in events if e["e"] == "known"]
    # The damage he did found by somebody who comes by counts as the town
    # reacting to that deed, though it names nobody (town list 6cf).
    knowns += [{"t": e["t"], "e": "known", "who": e["who"], "how": "found", "story": e["story"]} for e in events if e["e"] == "found"]
    knowns.sort(key=lambda k: k["t"])
    # WHAT FOLLOWS A DEED (town list 6bt): his being taken in follows the deed
    # he was taken for; DS Ellis asking after him follows the crime she came
    # for, or, come for the street's talk, whatever he had done by then; what
    # he claimed about a deed follows it. Each counts as the town reacting to
    # that deed (Meridian condition 2), not as something done before.
    follows = {}
    for e in events:
        if e["e"] == "taken":
            follows["player.taken_d%d" % int(e["day"])] = e["story"]
        if e["e"] == "ellis" and "day" in e:
            why = e["why"]
            follows["player.police_d%d" % int(e["day"])] = why.split(" ", 1)[1] if " " in why else "*the street's talk*"

    def followed(k):
        s = k["story"]
        if s in done_at:
            return s
        f = follows.get(s)
        if f is None and s.startswith("player.claim_"):
            f = "player." + s[len("player.claim_"):]
        if f == "*the street's talk*":
            done = [d for d, at in done_at.items() if at <= k["t"]]
            return min(done, key=lambda d: done_at[d]) if done else None
        return f
    reacting, before, early = [], [], []
    for k in knowns:
        d = followed(k)
        if d is None or d not in done_at:
            before.append(k)
        elif done_at[d] > k["t"]:
            early.append(k)
        else:
            if d != k["story"]:
                k = dict(k, follows=d)
            reacting.append(k)
    named = {}
    for e in events:
        if e["e"] == "named":
            for who in e["names"]:
                named.setdefault(who, e["t"])
    first = reacting[0] if reacting else None
    replies = [e for e in events if e["e"] == "reply"]
    broke = {}
    for e in replies:
        if e["how"] in BROKE:
            broke.setdefault(e["who"], {}).setdefault(e["how"], 0)
            broke[e["who"]][e["how"]] += 1
    waits = sorted(e["s"] for e in replies if "s" in e and e["how"] in ("own", "ended"))
    hints = []
    for e in events:
        if e["e"] == "hint" and e["moment"] not in [m for _, m in hints]:
            hints.append((e["t"], e["moment"]))
    return {
        "hints": hints,
        "police": [(e["t"], e["who"], e["story"], e["how"]) for e in events if e["e"] == "police"],
        "ellis": [(e["t"], e["why"]) for e in events if e["e"] == "ellis"],
        "taken": [(e["t"], e["story"], e.get("end", "?")) for e in events if e["e"] == "taken"],
        "tea": [(e["t"], int(e["day"]), e["state"]) for e in events if e["e"] == "tea"],
        "found": [(e["t"], e["who"], e["damage"]) for e in events if e["e"] == "found"],
        "trust": [(e["t"], e["who"]) for e in events if e["e"] == "trust"],
        "week": [(e["t"], e["answer"]) for e in weeks],
        "asks": [(e["t"], int(e["night"]), e["answer"], e["story"]) for e in asks],
        "replies": len(replies),
        "broke": broke,
        "wait_median": statistics.median(waits) if waits else None,
        "usd": end.get("usd") if end else None,
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
    return f"minute {minute(k['t'])}, {k['who']}, {k.get('how', '?')}, about {k['story']}" + (f", following {k['follows']}" if "follows" in k else "")


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
    if facts["replies"]:
        broke = "; ".join(f"{who} " + ", ".join(f"{how} {n}" for how, n in sorted(hows.items())) for who, hows in sorted(facts["broke"].items()))
        wait = f", first word a median {facts['wait_median']:.1f} s after his line" if facts["wait_median"] is not None else ""
        out.append(f"  replies: {facts['replies']}{wait}; talk that broke: " + (broke or "none"))
    if facts["usd"] is not None:
        out.append(f"  the talk cost: ${facts['usd']:.2f}")
    out.append("  named: " + (", ".join(f"{w} ({minute(t)})" for w, t in sorted(facts["named"].items(), key=lambda kv: kv[1])) or "nobody"))
    out.append("  did: " + ("; ".join(f"{what} ({minute(t)}, seen by {len(seen)})" for t, what, seen in facts["deeds"]) or "nothing the town could hold"))
    if facts["asks"]:
        out.append("  the outfit's asks: " + "; ".join(f"night {night} {answer} (minute {minute(t)})" for t, night, answer, _ in facts["asks"]))
    out.append("  hints shown: " + (", ".join(f"{m} ({minute(t)})" for t, m in facts["hints"]) or "none"))
    if facts["police"]:
        out.append("  the police heard: " + "; ".join(f"{how} from {who} about {story} (minute {minute(t)})" for t, who, story, how in facts["police"]))
    out.append("  DS Ellis on Quay Street: " + (", ".join(f"minute {minute(t)}, for {why}" for t, why in facts["ellis"]) or "never"))
    if facts["taken"]:
        out.append("  taken in: " + "; ".join(f"for {story}, minute {minute(t)}, {end}" for t, story, end in facts["taken"]))
    if facts["tea"]:
        out.append("  Ada's tea: " + "; ".join(f"day {day + 1}, {state} (minute {minute(t)})" for t, day, state in facts["tea"]))
    if facts["found"]:
        out.append("  the damage found: " + "; ".join(f"{damage} by {who} (minute {minute(t)})" for t, who, damage in facts["found"]))
    if facts["trust"]:
        out.append("  came to trust him: " + ", ".join(f"{who} (minute {minute(t)})" for t, who in facts["trust"]))
    if facts["week"]:
        out.append("  his answer at the week's end: " + "; ".join(f"{answer} (minute {minute(t)})" for t, answer in facts["week"]))
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
    broke = {}
    for f in friends:
        for who, hows in f["broke"].items():
            for how, n in hows.items():
                broke[how] = broke.get(how, 0) + n
    replies = sum(f["replies"] for f in friends)
    if replies:
        out.append(f"  friends' talk: {replies} replies; broke " + (", ".join(f"{how} {n}" for how, n in sorted(broke.items())) or "never"))
    if friends:
        shown = {m: sum(1 for f in friends if m in [x for _, x in f["hints"]]) for m in MOMENTS}
        out.append("  hints shown in friends' sessions: " + ", ".join(f"{m} {n}" for m, n in shown.items()))
        answers = {}
        for f in friends:
            for _, night, answer, _ in f["asks"]:
                if night == min((x[1] for x in f["asks"]), default=night):
                    answers[answer] = answers.get(answer, 0) + 1
        if answers:
            out.append("  the outfit's first ask, what friends did: " + ", ".join(f"{a} {n}" for a, n in sorted(answers.items())))
        came = [f["ellis"][0][0] for f in friends if f["ellis"]]
        out.append(f"  DS Ellis came in {len(came)} of {len(friends)} friends' sessions"
                   + (f", first at a median minute {minute(statistics.median(came))}" if came else ""))
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
    records = []
    for p in paths:
        try:
            events, unread, warn = read(p)
        except OSError as err:
            print(f"SESSION {os.path.basename(p)}: could not be opened ({err})")
            continue
        records.append((p, events, unread, warn))
    # ONE SITTING ACROSS A LOAD (town list 6bd): a record that carries a game on
    # by loading a save is joined to the record before it for the same player,
    # its minutes counted on from where that one ended, so a friend who quits
    # and comes back is one half hour, and the town reacting after the load is
    # read against what was done before it.
    joined = []
    for p, events, unread, warn in records:
        start = next((e for e in events if e["e"] == "start"), {})
        carries = start.get("fresh") is False and any(e["e"] == "load" for e in events)
        if carries and joined and joined[-1][3] == start.get("player"):
            prev_p, prev_events, prev_notes, player = joined[-1]
            offset = max((e["t"] for e in prev_events), default=0.0)
            more = [dict(e, t=e["t"] + offset) for e in events if e["e"] != "start"]
            ends = [e for e in prev_events if e["e"] != "end"]
            joined[-1] = (prev_p + " + " + os.path.basename(p), ends + more, (prev_notes[0] + unread, prev_notes[1] + warn), player)
        else:
            joined.append((p, list(events), (unread, warn), start.get("player")))
    for p, events, (unread, warn), _ in joined:
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
        # Where talk broke, and the cost (town list 6bd).
        talky = write("2026-10-09-100000.jsonl", [{"t": 0, "e": "start", "player": "friend", "fresh": True},
                                                 {"t": 10, "e": "reply", "who": "ron", "how": "own", "s": 1.5},
                                                 {"t": 20, "e": "reply", "who": "ron", "how": "fallback", "s": 2.0},
                                                 {"t": 30, "e": "reply", "who": "sheila", "how": "brush"},
                                                 {"t": 40, "e": "reply", "who": "ron", "how": "own", "s": 2.5},
                                                 {"t": 50, "e": "reply", "who": "ron", "how": "shrugged"},
                                                 {"t": 60, "e": "end", "why": "quit", "usd": 0.42}])
        et, ut, wt = read(talky)
        ft = one(et)
        tt = show(talky, ft, ut, wt)
        assert ft["broke"] == {"ron": {"fallback": 1}, "sheila": {"brush": 1}} and ft["replies"] == 5 and abs(ft["wait_median"] - 2.0) < 1e-9, ft
        assert "talk that broke: ron fallback 1; sheila brush 1" in tt and "the talk cost: $0.42" in tt and any("shrugged" in w for w in wt), tt
        # One sitting across a load: the reaction after the load counts against the deed before it.
        sit = os.path.join(d, "sitting")
        os.makedirs(sit)
        def write_in(name, lines):
            p = os.path.join(sit, name)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write("\n".join(json.dumps(x) for x in lines))
            return p
        write_in("2026-10-10-100000.jsonl", [{"t": 0, "e": "start", "player": "friend", "fresh": True},
                                             {"t": 300, "e": "deed", "what": "player.window_d1"}, {"t": 600, "e": "end", "why": "quit"}])
        write_in("2026-10-10-101500.jsonl", [{"t": 0, "e": "start", "player": "friend", "fresh": False},
                                             {"t": 5, "e": "load", "from": "slot1", "deeds": ["player.window_d1"]},
                                             {"t": 400, "e": "known", "who": "ron", "how": "question", "story": "player.window_d1"},
                                             {"t": 900, "e": "end", "why": "quit"}])
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            run(sit)
        joined_text = buf.getvalue()
        assert "SESSIONS 1: 1 friends'" in joined_text and "minute 16.7, ron, question, about player.window_d1" in joined_text and ", by thirty" in joined_text, joined_text
        alone = one(read(os.path.join(sit, "2026-10-10-101500.jsonl"))[0])
        assert alone["first_known"] is not None and alone["first_known"]["who"] == "ron", alone
        # Hints shown, and the outfit's ask answered, its story coming back (town list 6bh).
        firsthour = write("2026-10-11-100000.jsonl", [{"t": 0, "e": "start", "player": "friend", "fresh": True},
                                                      {"t": 4, "e": "hint", "moment": "StandingStill"},
                                                      {"t": 60, "e": "hint", "moment": "CanTalk"},
                                                      {"t": 61, "e": "hint", "moment": "CanTalk"},
                                                      {"t": 400, "e": "hint", "moment": "FirstAsk"},
                                                      {"t": 430, "e": "ask", "night": 0, "answer": "refused", "story": "player.outfit_d0"},
                                                      {"t": 800, "e": "known", "who": "darren", "how": "recognition", "story": "player.outfit_d0"},
                                                      {"t": 900, "e": "hint", "moment": "Nonsense"},
                                                      {"t": 910, "e": "ask", "night": 2, "answer": "maybe", "story": "player.outfit_d2"},
                                                      {"t": 1000, "e": "end", "why": "quit"}])
        eh, uh, wh = read(firsthour)
        fh_ = one(eh)
        th = show(firsthour, fh_, uh, wh)
        assert [m for _, m in fh_["hints"]] == ["StandingStill", "CanTalk", "FirstAsk", "Nonsense"], fh_["hints"]
        assert fh_["first_known"] is not None and fh_["first_known"]["story"] == "player.outfit_d0" and fh_["known_by_30"], fh_["first_known"]
        assert "night 0 refused" in th and "hints shown: StandingStill" in th and any("Nonsense" in w for w in wh) and any("maybe" in w for w in wh), (th, wh)
        assert "night 2" not in th and [a[1] for a in fh_["asks"]] == [0], (th, fh_["asks"])
        # What follows a deed counts as the town reacting to it (town list 6bt).
        followed_ = write("2026-10-13-100000.jsonl", [{"t": 0, "e": "start", "player": "friend", "fresh": True},
                                                      {"t": 100, "e": "deed", "what": "player.window_d1", "seen": ["ada"]},
                                                      {"t": 300, "e": "taken", "story": "player.window_d1", "day": 3, "end": "Charged"},
                                                      {"t": 400, "e": "known", "who": "joey", "how": "recognition", "story": "player.taken_d3"},
                                                      {"t": 500, "e": "ellis", "why": "talk", "day": 4},
                                                      {"t": 600, "e": "known", "who": "lena", "how": "recognition", "story": "player.police_d4"},
                                                      {"t": 700, "e": "known", "who": "sam", "how": "talk", "story": "player.claim_window_d1"},
                                                      {"t": 800, "e": "known", "who": "rita", "how": "remark", "story": "player.police_d9"},
                                                      {"t": 850, "e": "taken", "story": "player.x", "day": 5, "end": "Hanged"},
                                                      {"t": 900, "e": "end", "why": "quit"}])
        ef, uf, wf = read(followed_)
        ff = one(ef)
        tf = show(followed_, ff, uf, wf)
        assert [k["who"] for k in ff["reacting"]] == ["joey", "lena", "sam"] and all(k["follows"] == "player.window_d1" for k in ff["reacting"]), ff["reacting"]
        assert [k["who"] for k in ff["before"]] == ["rita"] and "following player.window_d1" in tf and "taken in: for player.window_d1" in tf, tf
        assert any("Hanged" in w for w in wf) and not uf, (wf, uf)
        # The first week's scenes (town list 6cf): the damage found counts as the
        # town reacting to the deed; his answer is a deed the street can know.
        week_ = write("2026-10-14-100000.jsonl", [{"t": 0, "e": "start", "player": "friend", "fresh": True},
                                                  {"t": 100, "e": "deed", "what": "player.window_d1", "seen": []},
                                                  {"t": 400, "e": "found", "who": "joey", "damage": "rita_window", "story": "player.window_d1"},
                                                  {"t": 900, "e": "tea", "day": 2, "state": "Stayed"},
                                                  {"t": 1200, "e": "trust", "who": "lena"},
                                                  {"t": 1500, "e": "week", "answer": "TakeOver", "story": "player.week_d6"},
                                                  {"t": 1700, "e": "known", "who": "ada", "how": "recognition", "story": "player.week_d6"},
                                                  {"t": 1800, "e": "tea", "day": 4, "state": "Spilt"},
                                                  {"t": 1900, "e": "week", "answer": "Maybe", "story": "player.week_d8"},
                                                  {"t": 2000, "e": "end", "why": "quit"}])
        ew, uw, ww = read(week_)
        fw = one(ew)
        tw = show(week_, fw, uw, ww)
        assert [k["who"] for k in fw["reacting"]] == ["joey", "ada"] and fw["first_known"]["how"] == "found" and fw["known_by_30"], fw["reacting"]
        assert "Ada's tea: day 3, Stayed" in tw and "rita_window by joey" in tw and "came to trust him: lena" in tw and "TakeOver (minute 25.0)" in tw, tw
        assert "Maybe" not in tw.split("warning")[0] and any("Spilt" in w for w in ww) and any("Maybe" in w for w in ww) and not uw, (tw, ww, uw)
        # What the police heard, and DS Ellis on the street (town list 6bm).
        policed = write("2026-10-12-100000.jsonl", [{"t": 0, "e": "start", "player": "friend", "fresh": True},
                                                    {"t": 1500, "e": "police", "who": "ron", "story": "player.outfit_d2", "how": "talk"},
                                                    {"t": 1500, "e": "ellis", "why": "talk"},
                                                    {"t": 1600, "e": "police", "who": "ada", "story": "x", "how": "gossip"},
                                                    {"t": 3600, "e": "end", "why": "quit"}])
        ep, up, wp = read(policed)
        fp = one(ep)
        tp = show(policed, fp, up, wp)
        assert fp["ellis"] == [(1500, "talk")] and "talk from ron about player.outfit_d2" in tp and "minute 25.0, for talk" in tp and any("gossip" in w for w in wp), (tp, wp)
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
