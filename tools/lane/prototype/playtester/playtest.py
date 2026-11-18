#!/usr/bin/env python3
"""The loop prototype's AI playtester: one command after every Fable round.

  python playtest.py --assets DIR [--out DIR] [--minutes 60] [--seed N] [--no-shots]

It builds the prototype from tools/lane/prototype/project (build.py, byte for byte against the
published page unless --allow-changed), serves it, and plays it in the cloud's headless
Chromium through the game's own test hook (window.LEDGER), taking screenshots. Two parts:

  (a) the sweep: every person on the street at four times of day is walked up to (Tom placed
      1.2 m in front, facing them, everyone else where the game has them). The talk prompt on
      offer is compared with who is actually in front and with that person's record (sex, age,
      whether Tom knows the name). Then a talk is opened with every person who offers one: the
      replies are classed as the person's own written lines, stock lines anyone says, or other
      (made from what they know, scenes); the number of turns held is counted; people with no
      talk at all are listed. Text running off screen or overlapping, and prompts for someone
      out of reach or behind Tom, are caught.
  (b) the newcomer run: a scripted player follows what the game asks for the first N minutes
      of play (default 60), talks to people, takes a fare or a night job when one is offered,
      walks the street and waits when there is nothing to do. Play time is booked by activity
      (talking, walking, driving, job actions, fighting, waiting) with stated estimates for
      reading and walking time; something new (a place, a person, a kind of action, a scene) is
      logged as it arrives, so each 30 minutes' count and the longest stretch with nothing new
      can be compared with Study 2.

Output (default ~/.cache/ledger-playtest/<time>/, outside the repository): report.json,
sweep.md, newcomer.md, transcripts.md and shots/*.png. Live AI talk only runs inside claude.ai
(the page's sample capability), so the scripted talk is tested and live talk is marked untested.

Written by the cloud lane, 18 Nov 2026. The game's code is not changed; the only additions in
the page are a seeded Math.random (so a run repeats) and reads through LEDGER.
"""
import argparse
import datetime
import functools
import http.server
import json
import math
import os
import subprocess
import sys
import re
import tempfile
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PROTO = os.path.dirname(HERE)
sys.path.insert(0, PROTO)
sys.path.insert(0, HERE)
import build  # noqa: E402
import wording  # noqa: E402

GL = ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
VIEW = {"width": 1280, "height": 720}

# Estimates for booking play time (a newcomer's pace; stated in the report, not measured on players)
WALK_MPS = 2.2        # walking with some jogging, metres a second
DRIVE_MPS = 8.0       # town driving, metres a second, over the straight-line distance times ROAD_FACTOR
ROAD_FACTOR = 1.35
READ_WPS = 3.3        # reading speed, words a second (about 200 a minute)
LINE_MIN_S = 2.0      # the shortest time a line stays read
RUN_MPS = 4.5         # a newcomer running from the constable (round 2)
CHOOSE_S = 3.0        # picking a reply or a choice
WAIT_STEP_S = 15.0    # one wait with nothing to do

SEEDED = """
(() => { let s = %d >>> 0; Math.random = function () { s = (s + 0x6D2B79F5) >>> 0; let t = s;
  t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; })();
"""

# What the page gives back about everyone, in one call (named people and the crowd)
PEOPLE_JS = r"""
() => {
  const G = LEDGER.G, cap = (s) => s ? s[0].toUpperCase() + s.slice(1) : s;
  const all = G.named.concat(G.crowd);
  return all.map((P) => {
    const named = !P.anon, rec = named ? LEDGER.person(P.id) : null;
    const known = named ? !!(rec && rec.nameKnownToTom) : false;
    const shown = P.anon ? cap(P.def.desc) : known ? P.def.name : cap(P.def.desc);
    return { id: P.id, anon: !!P.anon, name: P.def.name || null, desc: P.def.desc || null, sex: P.def.sex || null,
      age: P.def.age == null ? null : P.def.age, role: P.def.role || null, known, shown,
      x: P.x, z: P.z, ang: P.ang || 0, space: P.space, gone: !!P.gone, dead: !!P.dead, down: !!P.down,
      inCar: !!P.inCar, keeper: !!P.keeper, walker: !!P.walker, lad: !!P.lad, pax: !!P.pax };
  });
}
"""

# Put Tom 1.2 m in front of one person, facing them, and read what is on offer
FACE_JS = r"""
([id, dist, side]) => {
  const G = LEDGER.G, P = G.people[id] || G.crowd.find((q) => q.id === id) || G.named.find((q) => q.id === id);
  if (!P) return null;
  const t = G.tom;
  if (t.inCar) t.inCar = false;
  if (P.space !== t.space) { if (P.space !== 'street') LEDGER.enterRoom(P.space, true); else LEDGER.leaveRoom(); }
  const a = (P.ang || 0) + side;
  t.x = P.x + Math.sin(a) * dist; t.z = P.z + Math.cos(a) * dist;
  t.ang = Math.atan2(P.x - t.x, P.z - t.z); t.v = 0;
  const cap = (s) => s ? s[0].toUpperCase() + s.slice(1) : s;
  const near = G.named.concat(G.crowd).filter((Q) => Q !== P && Q.space === t.space && !Q.gone && Q.space !== 'home')
    .map((Q) => ({ id: Q.id, d: Math.hypot(Q.x - t.x, Q.z - t.z),
      off: Math.abs(Math.atan2(Math.sin(Math.atan2(Q.x - t.x, Q.z - t.z) - t.ang), Math.cos(Math.atan2(Q.x - t.x, Q.z - t.z) - t.ang))) }))
    .filter((q) => q.d < 4.5).sort((a, b) => a.d - b.d);
  return { prompts: LEDGER.prompts(), near, tom: { x: t.x, z: t.z, space: t.space } };
}
"""

# Rectangles of the words on screen, to catch overlaps and text off the edge
LAYOUT_JS = r"""
() => {
  const ids = ['prompt', 'subs', 'obj', 'ask', 'news', 'dialog', 'talk', 'fare', 'docket', 'called', 'noted', 'plate', 'zone', 'waitbar'];
  const out = [], els = [];
  const vis = (el) => { const s = getComputedStyle(el); return s.display !== 'none' && s.visibility !== 'hidden' && +s.opacity > 0.05 && !el.classList.contains('hidden'); };
  for (const id of ids) {
    const el = document.getElementById(id);
    if (!el || !vis(el) || !el.textContent.trim()) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;
    if (els.some((o) => o.contains(el) || el.contains(o))) continue;
    els.push(el);
    out.push({ id, x: r.x, y: r.y, w: r.width, h: r.height, text: el.textContent.trim().slice(0, 80),
      overflow: el.scrollWidth > el.clientWidth + 2 && getComputedStyle(el).overflowX === 'visible' });
  }
  const bub = document.getElementById('bubbles');
  if (bub) for (const el of bub.children) {
    if (!vis(el) || !el.textContent.trim()) continue;
    const r = el.getBoundingClientRect();
    out.push({ id: 'bubble', x: r.x, y: r.y, w: r.width, h: r.height, text: el.textContent.trim().slice(0, 80), overflow: false });
  }
  return { boxes: out, vw: innerWidth, vh: innerHeight };
}
"""


def layout_faults(snap, where):
    faults = []
    vw, vh = snap["vw"], snap["vh"]
    b = snap["boxes"]
    for r in b:
        if r["x"] < -2 or r["y"] < -2 or r["x"] + r["w"] > vw + 2 or r["y"] + r["h"] > vh + 2:
            faults.append({"kind": "off screen", "where": where, "what": r["id"], "text": r["text"]})
        if r.get("overflow"):
            faults.append({"kind": "text spills out of its box", "where": where, "what": r["id"], "text": r["text"]})
    for i in range(len(b)):
        for j in range(i + 1, len(b)):
            p, q = b[i], b[j]
            ox = min(p["x"] + p["w"], q["x"] + q["w"]) - max(p["x"], q["x"])
            oy = min(p["y"] + p["h"], q["y"] + q["h"]) - max(p["y"], q["y"])
            if ox > 4 and oy > 4:
                inside = (p["x"] >= q["x"] and p["y"] >= q["y"] and p["x"] + p["w"] <= q["x"] + q["w"] and p["y"] + p["h"] <= q["y"] + q["h"]) or \
                         (q["x"] >= p["x"] and q["y"] >= p["y"] and q["x"] + q["w"] <= p["x"] + p["w"] and q["y"] + q["h"] <= p["y"] + p["h"])
                faults.append({"kind": "words overlap", "where": where, "what": "%s over %s" % (p["id"], q["id"]),
                               "text": "%s | %s" % (p["text"][:40], q["text"][:40]), "contained": inside})
    return faults


class Game:
    def __init__(self, assets, seed, shots_dir, take_shots=True, allow_changed=False):
        from playwright.sync_api import sync_playwright
        self.tmp = tempfile.TemporaryDirectory()
        build.build(assets_dir=assets, dist=self.tmp.name, allow_changed=allow_changed, log=lambda *a: None)

        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *a):
                pass
        self.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=self.tmp.name))
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.pw = sync_playwright().start()
        self.b = self.pw.chromium.launch(args=GL)
        self.ctx = self.b.new_context(viewport=VIEW)
        self.ctx.add_init_script(SEEDED % seed)
        # Google Fonts cannot be reached from the cloud; refuse at once so the page does not wait
        self.ctx.route("**/fonts.googleapis.com/**", lambda r: r.abort())
        self.ctx.route("**/fonts.gstatic.com/**", lambda r: r.abort())
        self.pg = self.ctx.new_page()
        self.errors = []
        self.pg.on("pageerror", lambda e: self.errors.append(str(e)))
        self.pg.goto("http://127.0.0.1:%d/index.html" % self.srv.server_address[1])
        self.pg.wait_for_function("window.LEDGER && window.LEDGER.G", timeout=120000)
        self.pg.evaluate("LEDGER.startNew()")
        self.pg.wait_for_function("LEDGER.G.story.phase === 'play'", timeout=60000)
        self.pg.evaluate("window.LEDGER_MANUAL = true; window.LEDGER_NORENDER = true")
        self.shots_dir = shots_dir
        self.take_shots = take_shots
        self.shots = []
        os.makedirs(shots_dir, exist_ok=True)

    def js(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def step(self, secs):
        # the game's own logic, in 0.05 s slices, in pieces so one call never runs long
        left = secs
        while left > 0:
            n = min(left, 20.0)
            self.js("(s) => LEDGER.step(s)", n)
            left -= n

    def shot(self, name, note=""):
        """A screenshot with the picture drawn, plus the words on screen checked for overlaps."""
        if not self.take_shots:
            return None, []
        self.js("window.LEDGER_NORENDER = false")
        self.pg.wait_for_timeout(700)
        snap = self.js(LAYOUT_JS)
        path = os.path.join(self.shots_dir, "%02d-%s.png" % (len(self.shots) + 1, name))
        try:
            self.pg.screenshot(path=path, timeout=120000)
        except Exception as e:  # a slow software frame: keep going, say so
            path = None
            note = (note + " (screenshot failed: %s)" % str(e)[:80]).strip()
        self.js("window.LEDGER_NORENDER = true")
        self.shots.append({"file": os.path.basename(path) if path else None, "note": note, "clock": self.clock()})
        return path, snap

    def clock(self):
        return self.js("(() => { const r = LEDGER.read(); return r.day + ' ' + r.clock; })()")

    def close(self):
        try:
            self.b.close()
            self.pw.stop()
        finally:
            self.srv.shutdown()
            self.srv.server_close()
            self.tmp.cleanup()


# ---------------------------------------------------------------- the boxes (scenes and talks)

def read_box(g):
    return g.js("""(() => { const r = LEDGER.read(); return { box: r.boxOpen, paused: r.paused, why: r.pausedBecause,
      w: LEDGER.written.read(), t: LEDGER.talk.state(), toDo: r.toDo }; })()""")


def talk_log(g):
    return g.js("Array.from(document.querySelectorAll('#tlog p')).map(p => ({ who: p.className, text: p.textContent }))")


def clear_boxes(g, book, novelty, transcript, choice=0, answer="yes", limit=120, tense=None):
    """Answer whatever box is up until the game runs again; book the reading time as talking."""
    for _ in range(limit):
        r = read_box(g)
        if r["box"] == "dialog" and r["w"].get("open"):
            w = r["w"]
            key = "scene:" + (w.get("speaker") or "narration") + ":" + (w.get("text") or "")[:30]
            novelty.see("scene", (w.get("speaker") or "narration"), first_line=w.get("text"))
            transcript.append("%s: %s%s" % (w.get("speaker") or "(narration)", w.get("text"),
                                             (" [" + " | ".join(w["choices"]) + "]") if w.get("choices") else ""))
            book.add("talking", max(LINE_MIN_S, len((w.get("text") or "").split()) / READ_WPS) + (CHOOSE_S if w.get("choices") else 0))
            if w.get("choices"):
                if tense is not None and PRESSURE.search((w.get("text") or "") + " " + " ".join(w["choices"])):
                    tense.add("choice under pressure", "%s: %s" % (w.get("speaker") or "narration", (w.get("text") or "")[:50]))
                g.js("(n) => LEDGER.written.choose(n)", min(choice, len(w["choices"]) - 1))
            else:
                g.js("LEDGER.written.next()")
        elif r["box"] == "talk":
            t = r["t"]
            if t.get("waitingForTheReply"):
                g.js("LEDGER.talk.idle()")
                continue
            if t.get("deciding"):
                if tense is not None and str(t["deciding"]).startswith(PRESSURE_DECISIONS):
                    tense.add("choice under pressure", "talk decision: %s" % t["deciding"])
                a = g.js("(w) => LEDGER.talk.answer(w)", answer)
                transcript.append("(decided %s: %s)" % (t["deciding"], " / ".join(a.get("said") or [])))
                book.add("talking", CHOOSE_S + 4)
                if not a.get("answered"):
                    g.js("LEDGER.talk.leave()")
            else:
                for ln in talk_log(g)[-4:]:
                    transcript.append("  [%s] %s" % (ln["who"], ln["text"]))
                x = g.js("LEDGER.talk.say('leave')")
                if not x:
                    g.js("LEDGER.talk.leave()")
                book.add("talking", CHOOSE_S)
        elif r["box"] == "ledger":
            g.js("LEDGER.ledger.close()")
        elif r["box"]:
            g.js("(k) => LEDGER.press(k)", "Escape")
            g.step(0.2)
            if read_box(g)["box"] == r["box"]:
                return r["box"]
        elif r["paused"]:
            g.step(0.5)
            book.add("waiting", 0.5, note="paused: %s" % r.get("why"))
        else:
            return None
        g.step(0.1)
    return "stuck"


# ---------------------------------------------------------------- (a) the sweep

def sweep(g, stock, times=("Tue 09:30", "Tue 13:00", "Tue 18:00", "Tue 22:00")):
    """Every person at four times of day: prompt wording, who it names, talk on offer."""
    out = {"prompt_faults": [], "people": {}, "times": [], "layout": []}
    dummy = Book()
    nov = Novelty()
    for when in times:
        # move the clock on to the wanted time (the game's own logic, people walking their routines)
        target_min = parse_when(when)
        now = g.js("LEDGER.read().gameMinute")
        guard = 0
        while now < target_min and guard < 400:
            clear_boxes(g, dummy, nov, [])
            g.step(min(30.0, (target_min - now) * 45 / 60 + 0.5))
            now = g.js("LEDGER.read().gameMinute")
            guard += 1
        clear_boxes(g, dummy, nov, [])
        out["times"].append(g.clock())
        people = g.js(PEOPLE_JS)
        byid = {p["id"]: p for p in people}
        for p in people:
            if p["gone"] or p["dead"] or p["down"] or p["inCar"] or p["space"] in ("home", "off"):
                continue
            rec = out["people"].setdefault(p["id"], {"id": p["id"], "name": p["name"], "desc": p["desc"], "sex": p["sex"],
                                                     "age": p["age"], "anon": p["anon"], "seen": 0, "prompts": []})
            rec["seen"] += 1
            for dist, side in APPROACHES:
                check_person(g, p, byid, dist, side, rec, out)
        # one picture of the street at this hour, words checked
        path, snap = g.shot("sweep-" + when.replace(" ", "-").replace(":", ""), "sweep at " + when)
        if snap:
            out["layout"] += layout_faults(snap, "sweep " + when)
        # talk with everyone on the street now who has not been talked to yet
        done = {t["id"] for t in out.setdefault("talks", []) if t["talk"] != "not on the street now"}
        out["talks"] = [t for t in out["talks"] if t["id"] in done] + talk_round(g, stock, skip=done, when=g.clock())
    # one row per person: keep the talked row, else the last "not on the street" row
    rows = {}
    for t in out["talks"]:
        if t["id"] not in rows or rows[t["id"]]["talk"] == "not on the street now":
            rows[t["id"]] = t
    out["talks"] = list(rows.values())
    return out


APPROACHES = ((1.2, 0.0), (2.0, 0.6), (2.0, -0.6))  # metres in front, and radians round to one side


def check_person(g, p, byid, dist, side, rec, out):
    f = g.js(FACE_JS, [p["id"], dist, side])
    if not f:
        return
    talkp = [x for x in f["prompts"] if x["key"] == "E" and x["text"].startswith(("Talk to", "Speak to"))]
    other_e = [x for x in f["prompts"] if x["key"] == "E" and not x["text"].startswith(("Talk to", "Speak to"))]
    approach = "%.1f m, %+.0f deg" % (dist, math.degrees(side))
    here = "%s, %s (%s), approached at %s" % (g.clock(), p["shown"], p["id"], approach)
    if not talkp:
        rec["prompts"].append({"when": g.clock(), "approach": approach, "text": None,
                               "blocked_by": other_e[0]["text"] if other_e else None})
        if not other_e and dist <= 1.5:
            out["prompt_faults"].append({"kind": "no talk prompt in front of a person", "where": here,
                                         "detail": "prompts on offer: %s" % [x["text"] for x in f["prompts"]]})
        return
    text = talkp[0]["text"]
    label = wording.label_of(text)
    rec["prompts"].append({"when": g.clock(), "approach": approach, "text": text})
    expect = ("Speak to " if p["anon"] else "Talk to ") + low_article(p["shown"])
    if text != expect:
        cand = [q for q in f["near"] if (("Speak to " if byid.get(q["id"], {}).get("anon") else "Talk to ") +
                                         low_article(byid.get(q["id"], {}).get("shown") or "")) == text]
        who = byid.get(cand[0]["id"]) if cand else None
        out["prompt_faults"].append({
            "kind": "prompt names someone else",
            "where": here,
            "detail": "facing Tom at %.1f m: %s (%s, %s, age %s); prompt says %r%s" % (
                dist, p["shown"], p["id"], p["sex"], p["age"], text,
                (" = %s (%s, %s) at %.1f m, %.0f deg off Tom's facing" % (who["shown"], who["id"], who["sex"],
                                                                         cand[0]["d"], math.degrees(cand[0]["off"]))) if who else ""),
            "sex_mismatch": bool(who and who["sex"] != p["sex"]),
            "in_front": p["id"], "named": who["id"] if who else None,
        })
        return
    for fl in wording.wording_faults(label, p["sex"], p["age"], p["name"] if not p["anon"] else None,
                                     p["known"] if not p["anon"] else None):
        out["prompt_faults"].append({"kind": "prompt wording against record", "where": here, "detail": fl})


def talk_round(g, stock, turns=6, skip=(), when=""):
    res = []
    people = g.js(PEOPLE_JS)
    dummy, nov = Book(), Novelty()
    for p in people:
        if p["id"] in skip:
            continue
        if p["gone"] or p["dead"] or p["space"] in ("home", "off") or p["inCar"]:
            res.append({"id": p["id"], "shown": p["shown"], "anon": p["anon"], "talk": "not on the street now",
                        "where": p["space"]})
            continue
        clear_boxes(g, dummy, nov, [])
        if p["anon"]:
            # a stranger: E gives a one-line bark in a speech bubble, no talk
            g.js(FACE_JS, [p["id"], 1.2, 0.0])
            g.js("(k) => LEDGER.press(k)", "E")
            bub = g.js("(id) => (LEDGER.ui.bubs.find(b => b.P.id === id) || {}).text || null", p["id"])
            box = g.js("LEDGER.read().boxOpen")
            res.append({"id": p["id"], "shown": p["shown"], "anon": True, "when": when, "talk": "talk box" if box == "talk" else "bark only",
                        "turns": 0, "lines": [bub] if bub else [], "classes": [wording.classify_reply(bub, p["id"], stock)] if bub else []})
            clear_boxes(g, dummy, nov, [])
            continue
        st = g.js("(id) => LEDGER.talk.open(id, { free: true })", p["id"])
        if not st.get("open"):
            res.append({"id": p["id"], "shown": p["shown"], "anon": False, "talk": "no talk opened", "turns": 0,
                        "lines": [], "classes": [], "written": st.get("written")})
            clear_boxes(g, dummy, nov, [])
            continue
        said, held, jobs_used, offered = [], 0, [], []
        for _ in range(turns):
            s = g.js("LEDGER.talk.idle()")
            if not s.get("open"):
                break
            if s.get("deciding"):
                g.js("(w) => LEDGER.talk.answer(w)", "no")
                held += 1
                continue
            lines = g.js("LEDGER.talk.lines()")
            offered.append([l["job"] + ": " + l["text"] for l in lines])
            pick = next((l for l in lines if l["job"] not in ("leave", "yes", "no", "prop", "keep") and l["text"] not in said), None)
            if not pick:
                break
            r = g.js("(n) => LEDGER.talk.say(n)", pick["line"])
            if not r:
                break
            said.append(pick["text"])
            jobs_used.append(pick["job"])
            held += 1
        log = talk_log(g)
        npc = [ln["text"] for ln in log if ln["who"] == "npc"]
        classes = [wording.classify_reply(t, p["id"], stock) for t in npc]
        repeats = sum(1 for i, t in enumerate(npc) if t in npc[:i])
        res.append({"id": p["id"], "shown": p["shown"], "anon": False, "when": when, "talk": "talk", "turns": held, "jobs": jobs_used,
                    "lines": npc, "classes": classes, "repeats": repeats, "log": log, "offered": offered})
        g.js("LEDGER.talk.leave()")
        clear_boxes(g, dummy, nov, [])
    return res


def low_article(s):
    if s.startswith("A "):
        return "a " + s[2:]
    if s.startswith("The "):
        return "the " + s[4:]
    return s


def parse_when(when):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    d, hm = when.split()
    h, m = hm.split(":")
    return days.index(d) * 1440 + int(h) * 60 + int(m)


# ---------------------------------------------------------------- (b) the newcomer run

class Book:
    """Play time booked by activity, with a timeline."""
    def __init__(self):
        self.t = 0.0
        self.by = {}
        self.timeline = []

    def add(self, kind, secs, note=""):
        if secs <= 0:
            return
        self.by[kind] = self.by.get(kind, 0.0) + secs
        if self.timeline and self.timeline[-1][1] == kind and self.timeline[-1][3] == note:
            s = self.timeline[-1]
            self.timeline[-1] = (s[0], kind, s[2] + secs, note)
        else:
            self.timeline.append((self.t, kind, secs, note))
        self.t += secs


class Novelty:
    """Something new: a place, a person met, a kind of action, a scene."""
    def __init__(self):
        self.seen = set()
        self.events = []
        self.book = None

    def see(self, kind, what, first_line=None):
        key = (kind, what if kind != "scene" else (what, (first_line or "")[:40]))
        if key in self.seen:
            return False
        self.seen.add(key)
        self.events.append({"t": self.book.t if self.book else 0.0, "kind": kind, "what": what if kind != "scene" else "%s: %s" % (what, (first_line or "")[:50])})
        return True


FIGHT_JS = """() => { const F = LEDGER.F, G = LEDGER.G, out = { secs: 0, foes: F.foes.length };
  F.tele = []; let k = 0; const subs = [];
  const said = () => { for (const b of LEDGER.ui.bubs || []) if (!subs.some((s) => s[1] === b.text)) subs.push([b.P.def.name, b.text]); };
  for (let i = 0; i < 1200 && F.on; i++) {
    const live = F.foes.filter((f) => f.st !== 'down' && f.st !== 'flee');
    const coming = live.some((f) => f.st === 'windup' && f.t < 0.3);
    if (coming && F.st === 'idle') LEDGER.fight.block(true);
    else if (!coming && F.st === 'block') LEDGER.fight.block(false);
    else if (F.st === 'idle' && F.stam > 0.3) LEDGER.fight.input(k++ % 3 === 2 ? 'heavy' : 'light');
    LEDGER.tick(0.05); out.secs += 0.05; if (i % 10 === 0) said();
  }
  const T = F.tele || [];
  out.landed = T.filter((e) => e.ev === 'hit_contact' && e.actor === 'player').length;
  out.took = T.filter((e) => e.ev === 'hit_contact' && e.target === 'player').length;
  out.blocked = T.filter((e) => e.ev === 'block' && e.target === 'player').length;
  out.walls = T.filter((e) => e.ev === 'fall_hazard').length;
  out.downs = T.filter((e) => e.ev === 'knockdown').length;
  out.watchers = (F.watch || []).length;
  out.outcome = G.tom.hurt >= 1 ? 'Tom beaten' : out.downs ? 'a man put down' : F.on ? 'still going' : 'they gave way or ran';
  out.said = subs; F.tele = null; return out; }"""
# "fronting up" and "fighting" are play, not talk: the round 3 fight sample in the newcomer hour
PRESSURE = re.compile(r"\b(police|polis|job|carry|carrying|parcel|bag|deliver|owe[sd]?|debt|threat|warn|knife|cosh|fight|run|drop|tin|refuse|errand|garbutt|iveson)\b", re.I)
PRESSURE_DECISIONS = ("debt", "wash", "job", "ask", "errand", "wares")


class Tense:
    """Tense moments (lane task 4l, 18 Nov): a risk of being seen, a pursuit, a fight, an escape, a choice under pressure.
    Counted from what the game itself records: a job step taken in the open; an act of Tom's the town actually saw
    (a new event with witnesses, of a kind with a crime level or a menacing reading in LEDGER.rules.kinds); a fight begun; a police chase or an escape (none exist in the prototype yet, so
    they stay 0 until a round adds them); a decision on a debt, a job, the tin or the like, or a written choice whose
    words name such stakes (a word list, PRESSURE: an estimate, not a judgement)."""
    KINDS = ("risk of being seen", "seen doing it", "pursuit", "fight", "escape", "choice under pressure")

    def __init__(self):
        self.events = []
        self.book = None
        self.last_ev = None

    def add(self, kind, what):
        self.events.append({"t": self.book.t if self.book else 0.0, "kind": kind, "what": what})

    def poll(self, g):
        """New acts of Tom's that somebody saw, since the last poll."""
        evs = g.js("(LEDGER.G.events || []).map((e) => { const k = (LEDGER.rules.kinds || {})[e.kind] || {};"
                   " return {t: e.t, kind: e.kind, wit: (e.wit || []).length, crime: k.crimeLevel || 0,"
                   " menace: (k.readsMinusOneMenaceToOneDecent || 0) < 0}; })") or []
        if self.last_ev is None:
            self.last_ev = len(evs)
            return
        seen = set()
        for e in evs[self.last_ev:]:
            # only an act that could cost him (a crime, or something that reads as menace) seen by somebody;
            # one moment per kind and game minute, however many sighting records the town keeps of it
            key = (e["kind"], int(e.get("t") or 0))
            if e["wit"] and (e["crime"] > 0 or e["menace"]) and key not in seen:
                seen.add(key)
                self.add("seen doing it", "%s, %d witness%s" % (e["kind"], e["wit"], "" if e["wit"] == 1 else "es"))
        self.last_ev = len(evs)


def tense_stats(events, total_s):
    per30 = len(events) * 1800.0 / total_s if total_s else 0.0
    by = {k: sum(1 for e in events if e["kind"] == k) for k in Tense.KINDS}
    return {"count": len(events), "per_30_min": round(per30, 1), "by_kind": by}


def newcomer(g, stock, minutes=60.0):
    book, nov = Book(), Novelty()
    nov.book = book
    tense = Tense()
    tense.book = book
    transcript = []
    talked = {}
    stuck = {}
    places = g.js("LEDGER.places")
    shot_every = 300.0
    next_shot = 0.0
    layout = []
    log = []
    budget = minutes * 60.0
    last_cab = [-1e9]

    def note(s):
        log.append("%6.0fs %s | %s" % (book.t, g.clock(), s))
        print("  " + log[-1], flush=True)

    def where_now():
        r = g.js("LEDGER.read().tom")
        return r

    def walk_to(x, z, label, kind="walking", carrying=False):
        t = where_now()
        if t.get("indoorsRoomId"):
            # out through the door first (rooms sit apart from the street in the game's map)
            g.js("LEDGER.goOutside()")
            book.add(kind, 3.0, note="out of " + str(t.get("place")))
            t = where_now()
        d = math.hypot(x - t["xMetres"], z - t["zMetres"])
        if d > 400:
            note("walk of %.0f m to %s refused as a fault of the script (more than the whole street)" % (d, label))
            return False
        secs = d / WALK_MPS
        n = max(1, int(secs))
        for i in range(1, n + 1):
            fx = t["xMetres"] + (x - t["xMetres"]) * i / n
            fz = t["zMetres"] + (z - t["zMetres"]) * i / n
            g.js("([x, z]) => { const T = LEDGER.G.tom; T.ang = Math.atan2(x - T.x, z - T.z); LEDGER.goTo({ xMetres: x, zMetres: z }); }", [fx, fz])
            g.step(secs / n)
            book.add(kind, secs / n, note=label)
            if read_box(g)["box"]:
                clear_boxes(g, book, nov, transcript, tense=tense)
        place = g.js("LEDGER.read().tom.place")
        nov.see("place", place)

    def person_spot(pid):
        p = g.js("(id) => LEDGER.person(id)", pid)
        if not p or p["place"] in ("at home", "away"):
            return None
        door = places.get(p["place"] + " (street door)")
        return p, door

    def chat(pid, label):
        sp = person_spot(pid)
        if not sp:
            return False
        p, door = sp
        if door:
            walk_to(door["xMetres"], door["zMetres"], "to " + p["place"])
        else:
            walk_to(p["xMetres"], p["zMetres"], "to " + (p["shownAs"] or pid))
        st = g.js("(id) => LEDGER.talk.open(id)", pid)
        nov.see("person", pid)
        if st.get("written", {}).get("open"):
            note("scene with %s" % (p["shownAs"]))
            clear_boxes(g, book, nov, transcript, tense=tense)
            st = g.js("(id) => LEDGER.talk.open(id, { free: true })", pid)
        if not st.get("open"):
            return True
        nov.see("action", "talk")
        talked[pid] = talked.get(pid, 0) + 1
        n0 = len(talk_log(g))
        transcript.append("--- talk with %s (%s), %s" % (p["shownAs"], pid, g.clock()))
        used = set()
        for _ in range(5):
            s = g.js("LEDGER.talk.idle()")
            if not s.get("open"):
                break
            if s.get("deciding"):
                a = g.js("(w) => LEDGER.talk.answer(w)", "yes")
                transcript.append("(decided %s: %s)" % (s["deciding"], " / ".join(a.get("said") or [])))
                book.add("talking", CHOOSE_S + 4, note="talk " + pid)
                continue
            lines = g.js("LEDGER.talk.lines()")
            pick = next((l for l in lines if l["job"] not in ("leave",) and l["text"] not in used), None)
            if not pick:
                break
            used.add(pick["text"])
            g.js("(n) => LEDGER.talk.say(n)", pick["line"])
            new = talk_log(g)
            words = sum(len(x["text"].split()) for x in new[n0:])
            n0 = len(new)
            book.add("talking", CHOOSE_S + max(LINE_MIN_S, words / READ_WPS), note="talk " + pid)
        offered = False
        for ln in talk_log(g):
            transcript.append("  [%s] %s" % (ln["who"], ln["text"]))
            offered = offered or "front up to them on the street" in ln["text"]
        g.js("LEDGER.talk.say('leave')")
        g.js("LEDGER.talk.leave()")
        clear_boxes(g, book, nov, transcript, tense=tense)
        if offered and pid not in fronted:
            front_up(pid)
        return True

    def front_up(pid):
        """Round 3 (18 Nov): the game offers to front up a debtor who will not pay ([Q]); a newcomer takes it,
        climbs the ladder to a shove while the man stands, and if it comes to blows fights as a first-time
        player would: jabs, a heavy blow every third, the guard up only once a wind-up is plainly coming."""
        fronted.add(pid)
        tense.add("choice under pressure", "front up to %s over the debt" % pid)
        g.js("(id) => { const P = LEDGER.G.people[id], t = LEDGER.G.tom; if (!P) return;"
             " t.ang = Math.atan2(P.x - t.x, P.z - t.z); LEDGER.fight.frontUp(P); }", pid)
        nov.see("action", "front up")
        transcript.append("--- fronts up to %s, %s" % (pid, g.clock()))
        book.add("fronting up", 3, note="front up " + pid)
        for _ in range(4):
            f = g.js("({on: LEDGER.F.on, rung: LEDGER.F.rung, y: !!LEDGER.F.yielded})")
            if not f["on"] or f["rung"] >= 5 or f["y"]:
                break
            g.js("LEDGER.fight.climb()")
            g.step(0.7)
            book.add("fronting up", 2, note="front up " + pid)
        f = g.js("({on: LEDGER.F.on, rung: LEDGER.F.rung, y: !!LEDGER.F.yielded})")
        transcript.append("  (ladder: rung %d, %s)" % (f["rung"], "he gave way" if f["y"] else "he stood"))
        if f["on"] and f["rung"] >= 5:
            out = g.js(FIGHT_JS)
            nov.see("action", "fight")
            tense.add("fight", "a fight with %s and %d more" % (pid, max(0, out["foes"] - 1)))
            book.add("fighting", out["secs"], note="fight " + pid)
            fights.append(dict(out, who=pid, at=round(book.t / 60.0, 1)))
            transcript.append("  (fight: %.0f s, Tom landed %d, took %d, blocked %d, walls %d, watchers %d, outcome %s)" % (
                out["secs"], out["landed"], out["took"], out["blocked"], out["walls"], out["watchers"], out["outcome"]))
            for ln in out.get("said", []):
                transcript.append("  [%s] %s" % (ln[0], ln[1]))
        if g.js("LEDGER.F.on"):
            g.js("LEDGER.fight.end()")
        clear_boxes(g, book, nov, transcript, tense=tense)

    fronted, fights = set(), []

    def do_fare():
        f = g.js("LEDGER.read().story.fare")
        if not f:
            return False
        cab = g.js("LEDGER.cab.read()")
        if not cab["tomHasTheKeys"]:
            return False
        if not g.js("LEDGER.read().tom.inTheCab"):
            walk_to(cab["xMetres"] + 1.6, cab["zMetres"], "to the cab")
            if not g.js("LEDGER.cab.getIn()"):
                return False
        nov.see("action", "drive the cab")
        if f["state"] == "offered on the radio":
            g.js("LEDGER.fare.accept()")
            nov.see("action", "take a fare")
            book.add("driving", CHOOSE_S, note="fare offered")
        f = g.js("LEDGER.fare.read()")
        if not f:
            return True
        here = g.js("LEDGER.cab.read()")
        if f["state"] == "to pick up":
            d = math.hypot(f["pickUp"]["xMetres"] - here["xMetres"], f["pickUp"]["zMetres"] - here["zMetres"]) * ROAD_FACTOR
            g.step(d / DRIVE_MPS)
            book.add("driving", d / DRIVE_MPS, note="to the fare")
            g.js("LEDGER.fare.pickUp()")
            clear_boxes(g, book, nov, transcript, tense=tense)
            f = g.js("LEDGER.fare.read()")
        if f and f["state"] == "carrying":
            d = math.hypot(f["dropOff"]["xMetres"] - f["pickUp"]["xMetres"], f["dropOff"]["zMetres"] - f["pickUp"]["zMetres"]) * ROAD_FACTOR
            g.step(d / DRIVE_MPS)
            book.add("driving", d / DRIVE_MPS, note="fare to " + f["toPlace"])
            nov.see("place", f["toPlace"])
            r = g.js("LEDGER.fare.dropOff()")
            note("fare dropped at %s, paid %sp" % (f["toPlace"], r.get("paidPence")))
            clear_boxes(g, book, nov, transcript, tense=tense)
        g.js("LEDGER.cab.getOut()")
        return True

    def do_job():
        j = g.js("LEDGER.job.read()")
        if not j or j["state"] not in ("to pick up", "carrying"):
            return False  # done, missed or taken: nothing more to do for it (looped forever before round 2)
        h = g.js("LEDGER.read().hour")
        if j.get("doorsOpenFromHour") is not None and h < j["doorsOpenFromHour"] and h > 6:
            return False
        nov.see("action", "night job")
        if j["state"] == "to pick up":
            walk_to(j["pickUp"]["xMetres"], j["pickUp"]["zMetres"], "job pick-up", kind="job actions")
            press_job_key()
        j = g.js("LEDGER.job.read()")
        if j and j["state"] == "carrying":
            if carry_under_watch(j):
                press_job_key()
        clear_boxes(g, book, nov, transcript, tense=tense)
        return True

    def carry_under_watch(j):
        """Round 2 (18 Nov): the carry with a constable on his beat. Walks to the drop a second at a time;
        called out to, a newcomer runs (away from him, at a run of RUN_MPS, through the script's straight
        lines, which ignore walls: an estimate) until he gives up or catches him. True if still carrying."""
        warned = False
        for _ in range(400):
            j = g.js("LEDGER.job.read()")
            if not j or j["state"] != "carrying":
                return False
            w = j.get("watch") or {}
            st = w.get("state")
            if st == "beat" and not warned and (w.get("metresAway") or 999) < 30:
                warned = True
                tense.add("risk of being seen", "constable on his beat %.0f m away, carrying" % w["metresAway"])
                nov.see("action", "carry past a constable")
            if st in ("challenge", "chase"):
                tense.add("choice under pressure", "called out to with the bag: run")
                nov.see("action", "run from the constable")
                tense.add("pursuit", "the constable after him with the bag")
                for _ in range(90):
                    j = g.js("LEDGER.job.read()")
                    w = (j or {}).get("watch") or {}
                    if not j or w.get("state") not in ("challenge", "chase"):
                        break
                    t = where_now()
                    c = w["constable"]
                    dx, dz = t["xMetres"] - c["xMetres"], t["zMetres"] - c["zMetres"]
                    n = math.hypot(dx, dz) or 1.0
                    g.js("([x, z]) => { const T = LEDGER.G.tom; T.run = true; T.ang = Math.atan2(x - T.x, z - T.z); LEDGER.goTo({ xMetres: x, zMetres: z }); }",
                         [t["xMetres"] + dx / n * RUN_MPS, t["zMetres"] + dz / n * RUN_MPS])
                    g.step(1.0)
                    book.add("running", 1.0, note="from the constable")
                    if read_box(g)["box"]:
                        clear_boxes(g, book, nov, transcript, tense=tense)
                g.js("() => { LEDGER.G.tom.run = false; }")
                j = g.js("LEDGER.job.read()")
                w = (j or {}).get("watch") or {}
                how = w.get("how")
                note("job: chase ended: %s" % how)
                if how == "lost him":
                    tense.add("escape", "lost the constable, still carrying")
                    nov.see("action", "escape with the bag")
                continue
            t = where_now()
            dx, dz = j["drop"]["xMetres"] - t["xMetres"], j["drop"]["zMetres"] - t["zMetres"]
            d = math.hypot(dx, dz)
            if d < 1.5:
                return True
            stepm = min(d, WALK_MPS)
            g.js("([x, z]) => { const T = LEDGER.G.tom; T.ang = Math.atan2(x - T.x, z - T.z); LEDGER.goTo({ xMetres: x, zMetres: z }); }",
                 [t["xMetres"] + dx / d * stepm, t["zMetres"] + dz / d * stepm])
            g.step(stepm / WALK_MPS)
            book.add("job actions", stepm / WALK_MPS, note="carrying to the drop")
            if read_box(g)["box"]:
                clear_boxes(g, book, nov, transcript, tense=tense)
        return False

    def press_job_key():
        ps = g.js("LEDGER.prompts()")
        for p in ps:
            if not p["text"].startswith(("Talk to", "Speak to", "Go into", "Coat", "Front up", "Get in", "Pick up a")):
                g.js("(k) => LEDGER.press(k)", p["key"])
                book.add("job actions", 3.0, note=p["text"])
                tense.add("risk of being seen", "job: " + p["text"])
                note("job: pressed %s (%s)" % (p["key"], p["text"]))
                return True
        note("job: no job prompt at the spot; prompts %s" % [p["text"] for p in ps])
        return False

    def objective_target(obj):
        if not obj:
            return None
        people = g.js(PEOPLE_JS)
        import re as _re
        low = obj.lower()
        titles = {"father", "ds", "pc", "mrs", "mr", "miss", "dr"}
        for p in people:
            if p["anon"] or not p["name"]:
                continue
            parts = [w for w in p["name"].split() if w.lower().strip(".") not in titles]
            if any(_re.search(r"\b%s\b" % _re.escape(w.lower()), low) for w in parts if len(w) > 2):
                return ("person", p["id"])
        # a place: the one whose first word comes earliest in the words asked ("Find Mickey's. ... Quay
        # Street" goes to Mickey's), a door before a spot on the street
        best = None
        for name, pl in places.items():
            base = name.split(" (")[0].lower()
            first = [w for w in _re.findall(r"[a-z']+", base) if w not in ("the", "a")][:1]
            if not first or len(first[0]) < 4:
                continue
            m = _re.search(r"\b%s\b" % _re.escape(first[0]), low)
            if not m:
                continue
            score = (m.start(), 0 if pl.get("kind") == "door" else 1, len(name))
            if best is None or score < best[0]:
                best = (score, name)
        return ("place", best[1]) if best else None

    clear_boxes(g, book, nov, transcript, tense=tense)
    nov.see("place", g.js("LEDGER.read().tom.place"))
    while book.t < budget:
        print("  t=%.0fs %s toDo=%r" % (book.t, g.clock(), (g.js("LEDGER.read().toDo") or "")[:50]), flush=True)
        if book.t >= next_shot:
            path, snap = g.shot("newcomer-%03dmin" % int(book.t / 60), "newcomer at %.0f min" % (book.t / 60))
            if snap:
                layout.extend(layout_faults(snap, "newcomer %.0f min" % (book.t / 60)))
            next_shot += shot_every
        if g.js("LEDGER.read().weekEnded"):
            note("the week ended")
            break
        box = clear_boxes(g, book, nov, transcript, tense=tense)
        if box == "stuck":
            note("a box would not close")
            g.step(1)
            book.add("waiting", 1, note="stuck box")
            continue
        tense.poll(g)
        if g.js("!!(LEDGER.F && LEDGER.F.on)"):
            if nov.see("action", "fight") or not (tense.events and tense.events[-1]["kind"] == "fight"):
                tense.add("fight", "a fight")
            g.step(2)
            book.add("fighting", 2)
            continue
        if do_fare():
            continue
        r = g.js("LEDGER.read()")
        obj = r.get("toDo")
        tgt = objective_target(obj)
        key = (obj, tgt)
        if tgt and stuck.get(key, 0) < 2:
            stuck[key] = stuck.get(key, 0) + 1
            if tgt[0] == "person":
                if chat(tgt[1], obj):
                    continue
                note("objective names %s, who is not on the street now: %r" % (tgt[1], obj))
            else:
                pl = places[tgt[1]]
                walk_to(pl["xMetres"], pl["zMetres"], "objective: " + tgt[1])
                ps = g.js("LEDGER.prompts()")
                door = next((p for p in ps if p["key"] == "E" and p["text"].startswith("Go into")), None)
                if door:
                    g.js("LEDGER.press('E')")
                    nov.see("place", door["text"][8:])
                    book.add("walking", 2.0, note=door["text"])
                    clear_boxes(g, book, nov, transcript, tense=tense)
                continue
        elif obj and tgt is None and stuck.get((obj, None), 0) == 0:
            stuck[(obj, None)] = 1
            note("objective not followable by name: %r" % obj)
        if do_job():
            continue
        # a newcomer with the cab keys tries the radio once in a while
        if book.t - last_cab[0] > 600 and g.js("LEDGER.cab.read().tomHasTheKeys"):
            last_cab[0] = book.t
            cab = g.js("LEDGER.cab.read()")
            if walk_to(cab["xMetres"] + 1.6, cab["zMetres"], "to the cab") is not False and g.js("LEDGER.cab.getIn()"):
                nov.see("action", "sit in the cab")
                for _ in range(8):
                    g.step(WAIT_STEP_S)
                    book.add("waiting", WAIT_STEP_S, note="in the cab for the radio")
                    if g.js("LEDGER.read().story.fare"):
                        break
                if g.js("LEDGER.read().story.fare"):
                    note("fare offered on the radio")
                    do_fare()
                else:
                    note("two minutes in the cab, no fare offered")
                    g.js("LEDGER.cab.getOut()")
                continue
        # curiosity: the nearest named person not yet spoken to, then the nearest stranger, then wait
        people = [p for p in g.js(PEOPLE_JS) if not (p["gone"] or p["dead"] or p["space"] in ("home", "off") or p["inCar"])]
        tom = where_now()
        fresh = sorted((p for p in people if not p["anon"] and talked.get(p["id"], 0) == 0),
                       key=lambda p: math.hypot(p["x"] - tom["xMetres"], p["z"] - tom["zMetres"]))
        if fresh and math.hypot(fresh[0]["x"] - tom["xMetres"], fresh[0]["z"] - tom["zMetres"]) < 80:
            if chat(fresh[0]["id"], "curiosity"):
                continue
            talked[fresh[0]["id"]] = -1
        unvisited = [k for k, v in places.items() if v.get("kind") in ("street", "door") and ("place", k.split(" (")[0]) not in nov.seen and k not in stuck]
        if unvisited:
            k = unvisited[0]
            stuck[k] = 1
            walk_to(places[k]["xMetres"], places[k]["zMetres"], "looking about: " + k)
            continue
        g.step(WAIT_STEP_S)
        book.add("waiting", WAIT_STEP_S, note="nothing to do")
    tense.poll(g)
    return {"book": book.by, "timeline": book.timeline, "novelty": nov.events, "log": log, "transcript": transcript,
            "layout": layout, "played_s": book.t, "tense": tense.events, "fights": fights}


def novelty_stats(events, total_s, window_s=1800.0):
    ts = sorted(e["t"] for e in events)
    windows = []
    w = 0.0
    while w < total_s:
        windows.append({"from_min": w / 60, "to_min": min(total_s, w + window_s) / 60,
                        "new_things": sum(1 for t in ts if w <= t < w + window_s)})
        w += window_s
    gaps = []
    last = 0.0
    for t in ts + [total_s]:
        gaps.append((t - last, last))
        last = t
    longest = max(gaps) if gaps else (0, 0)
    return {"windows": windows, "longest_gap_min": longest[0] / 60, "longest_gap_from_min": longest[1] / 60}


# ---------------------------------------------------------------- writing it down

def write_reports(out, res):
    with open(os.path.join(out, "report.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1, default=str)
    sw = res.get("sweep")
    if sw:
        L = ["# Sweep, %s" % res["started"], "", "Times swept: " + ", ".join(sw["times"]), ""]
        kinds = {}
        for fl in sw["prompt_faults"]:
            kinds.setdefault(fl["kind"], []).append(fl)
        L.append("## Prompt faults (%d)" % len(sw["prompt_faults"]))
        for k, v in kinds.items():
            L.append("")
            L.append("### %s (%d)" % (k, len(v)))
            for fl in v[:40]:
                L.append("- %s: %s" % (fl["where"], fl["detail"]))
        L += ["", "## Talk with each person", "", "| person | when | talk | turns | own | stock | other | repeats | first reply |", "|---|---|---|---|---|---|---|---|---|"]
        for t in sw["talks"]:
            c = t.get("classes") or []
            L.append("| %s (%s) | %s | %s | %s | %d | %d | %d | %s | %s |" % (t["shown"], t["id"], t.get("when", ""), t["talk"], t.get("turns", ""),
                     c.count("own"), c.count("stock"), c.count("other"), t.get("repeats", ""), ((t.get("lines") or [""])[0] or "")[:60].replace("|", "/")))
        L += ["", "## Words on screen (%d)" % len(sw["layout"])]
        for fl in sw["layout"]:
            L.append("- %s: %s, %s (%s)" % (fl["where"], fl["kind"], fl["what"], fl["text"]))
        open(os.path.join(out, "sweep.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    nc = res.get("newcomer")
    if nc:
        tot = nc["played_s"] or 1
        L = ["# Newcomer run, %s" % res["started"], "", "Played (booked): %.1f min. Estimates: walking %.1f m/s, driving %.1f m/s x %.2f road, reading %.1f words/s, %.0f s a choice." % (
            tot / 60, WALK_MPS, DRIVE_MPS, ROAD_FACTOR, READ_WPS, CHOOSE_S), "", "## Share of play time", "", "| activity | minutes | share |", "|---|---|---|"]
        for k, v in sorted(nc["book"].items(), key=lambda kv: -kv[1]):
            L.append("| %s | %.1f | %.0f%% |" % (k, v / 60, 100 * v / tot))
        ns = nc["novelty_stats"]
        L += ["", "## Something new", ""]
        for w in ns["windows"]:
            L.append("- minutes %.0f to %.0f: %d new things" % (w["from_min"], w["to_min"], w["new_things"]))
        L.append("- longest stretch with nothing new: %.1f min, from minute %.1f" % (ns["longest_gap_min"], ns["longest_gap_from_min"]))
        ts = nc.get("tense_stats") or tense_stats(nc.get("tense") or [], tot)
        L += ["", "## Tense moments", "", "- %d in %.1f min, %.1f per 30 minutes" % (ts["count"], tot / 60, ts["per_30_min"])]
        for k, v in ts["by_kind"].items():
            L.append("- %s: %d" % (k, v))
        for e in nc.get("tense") or []:
            L.append("    - %.1f min: %s, %s" % (e["t"] / 60, e["kind"], e["what"]))
        L += ["", "## Fights (round 3)", ""]
        for fo in nc.get("fights") or []:
            L.append("- %.1f min, with %s and %d more: %.0f s; Tom landed %d, took %d, blocked %d; walls %d; men down %d; watchers %d; %s" % (
                fo["at"], fo["who"], max(0, fo["foes"] - 1), fo["secs"], fo["landed"], fo["took"], fo["blocked"], fo["walls"], fo["downs"], fo["watchers"], fo["outcome"]))
        if not nc.get("fights"):
            L.append("- none")
        L += ["", "## New things in order", ""]
        for e in nc["novelty"]:
            L.append("- %.1f min: %s, %s" % (e["t"] / 60, e["kind"], e["what"]))
        L += ["", "## Log", ""] + ["    " + x for x in nc["log"]]
        L += ["", "## Words on screen (%d)" % len(nc["layout"])]
        for fl in nc["layout"]:
            L.append("- %s: %s, %s (%s)" % (fl["where"], fl["kind"], fl["what"], fl["text"]))
        open(os.path.join(out, "newcomer.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
        open(os.path.join(out, "transcripts.md"), "w", encoding="utf-8").write("# Transcripts\n\n" + "\n".join(nc["transcript"]) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--assets", default=os.environ.get("LEDGER_PROTO_ASSETS"), help="the pictures folder (as build.py)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--minutes", type=float, default=60.0)
    ap.add_argument("--seed", type=int, default=19901120)
    ap.add_argument("--no-shots", action="store_true")
    ap.add_argument("--only", choices=["sweep", "newcomer"], default=None)
    ap.add_argument("--allow-changed", action="store_true")
    a = ap.parse_args(argv)
    if not a.assets or not os.path.isdir(a.assets):
        ap.error("--assets DIR (or LEDGER_PROTO_ASSETS) must name the folder of pictures fetched from the page")
    stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    out = a.out or os.path.join(os.path.expanduser("~"), ".cache", "ledger-playtest", stamp)
    os.makedirs(out, exist_ok=True)
    stock = json.loads(subprocess.check_output(["node", os.path.join(HERE, "stock_lines.mjs"), os.path.join(PROTO, "project", "src")]))
    res = {"started": stamp, "seed": a.seed, "live_talk": "untested (runs only inside claude.ai)", "errors": []}
    t0 = time.time()
    if a.only in (None, "sweep"):
        g = Game(a.assets, a.seed, os.path.join(out, "shots"), not a.no_shots, a.allow_changed)
        try:
            res["sweep"] = sweep(g, stock)
            res["errors"] += g.errors
            res["shots_sweep"] = g.shots
        finally:
            g.close()
    if a.only in (None, "newcomer"):
        g = Game(a.assets, a.seed, os.path.join(out, "shots"), not a.no_shots, a.allow_changed)
        try:
            nc = newcomer(g, stock, a.minutes)
            nc["novelty_stats"] = novelty_stats(nc["novelty"], nc["played_s"])
            nc["tense_stats"] = tense_stats(nc.get("tense") or [], nc["played_s"])
            res["newcomer"] = nc
            res["errors"] += g.errors
            res["shots_newcomer"] = g.shots
        finally:
            g.close()
    res["wall_seconds"] = round(time.time() - t0)
    write_reports(out, res)
    print("playtest written to", out)
    sw = res.get("sweep")
    if sw:
        print("sweep: %d prompt faults, %d words-on-screen faults; talks: %d people" % (len(sw["prompt_faults"]), len(sw["layout"]), len(sw["talks"])))
    nc = res.get("newcomer")
    if nc:
        print("newcomer: %.1f min booked; %s; longest with nothing new %.1f min" % (
            nc["played_s"] / 60, {k: round(v / 60, 1) for k, v in nc["book"].items()}, nc["novelty_stats"]["longest_gap_min"]))
        print("tense moments: %(count)d, %(per_30_min).1f per 30 minutes, %(by_kind)s" % nc["tense_stats"])
    if res["errors"]:
        print("page errors:", res["errors"][:5])
    return 0


if __name__ == "__main__":
    sys.exit(main())
