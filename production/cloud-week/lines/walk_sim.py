#!/usr/bin/env python3
"""A small simulation of a walk through the rules (unit 12, cloud week 42). Standard library only, light (about a second).

Used by check_lines.py. It plays thirty minutes along Quay Street with a fixed seed: Tom walks the street and pauses, twenty
passers-by cross his path, four of the street's own people stay where they are (Ron at the rank, a shopkeeper at her door, a
pensioner on her step, the pawn's keeper at hers, as quay-cast.json's routines have them), rain falls from minute 12 to minute 20, and one crime
happens at minute 15. Every line a person would say goes through the rules in rules.json, the way the PC session's picker would
apply them, and the result reports repeats, gaps and the busiest minute.

What it models: the hearing radius by weather, who is out in rain, chances to speak, standing, conditions, accents and
never-police, the bag and the ledger (only what he HEARD counts), the cooldowns, one voice at a time with priority and shelf
life, the 45 s neighbours' clock shared with the street's existing ambient exchanges, the hush after a deed, a witness's
sureness by distance. What it does not: faces, animation, the stance ladder (everyone here stands at Notices or below), the
real route, real voices. The street's existing ambient exchanges are stood in for by a share of the neighbour slots
(EXISTING_AMBIENT_SHARE): an assumption of this sim, not a measurement.
"""
import heapq
import math
import random
from collections import defaultdict

EXISTING_AMBIENT_SHARE = {"dry": 0.60, "drizzle": 0.50, "rain": 0.40}
TALK_SPEED = 3.0           # words a second (Sheila's voice-key lines run 3.1)
LEAD_S = 0.3
KIND_WEIGHT = {"shopkeeper": 3, "dock_worker": 3, "pensioner": 2, "office_worker": 3, "driver": 2, "laundry_worker": 2,
               "tradesman": 2, "night_shift": 0.4, "casual_worker": 2}
NAMED = {"darren": ("sam", 1.0), "father_walsh": ("emil", 0.6), "june": ("june", 0.4)}
STANDING_DRAW = [("stranger", 0.55), ("owner", 0.30), ("nowak", 0.12), ("tom", 0.03)]
NAMED_STANDING = {"rocco": "nowak", "sam": "nowak", "emil": "owner", "june": "owner"}
LOCALS = [("rocco", "ron", 8.3, "nowak"), ("marla", "shopkeeper", 12.0, "owner"), ("ada", "pensioner", 6.5, "owner"), ("rita", "shopkeeper", 18.0, "owner")]
BANKS = {"bumped": "bumped", "rain_starts": "rain/starts", "in_rain": "rain/in", "crime_noise": "crime/noise",
         "crime_shape": "crime/shape", "crime_face": "crime/face", "after_deed": "deed/after", "asked_way": "way/ask", "farewell": "farewell"}
KNOWS_PLACE = {"street": 0.95, "town": 0.75, "atlas_near": 0.70, "atlas_far": 0.30}


def family_of(sit):
    if sit.startswith("greeting"):
        return "greet"
    return {"bumped": "bump", "rain_starts": "rain_starts", "in_rain": "in_rain", "crime_noise": "crime", "crime_shape": "crime",
            "crime_face": "crime", "after_deed": "after_deed", "asked_way": "way", "farewell": "farewell"}[sit]


def bank_of(sit):
    return "greeting/" + sit.split(".")[1] if sit.startswith("greeting") else BANKS[sit]


def weather_at(t, rain):
    """Dry; drizzle for the first minute of the rain, rain, drizzle for the minute after it ends; then dry."""
    a, b = rain[0] * 60.0, rain[1] * 60.0
    if t < a or t >= b + 60.0:
        return "dry"
    if t < a + 60.0 or t >= b:
        return "drizzle"
    return "rain"


def band_of(hour_f, bands):
    h = int(hour_f) % 24
    for name, (lo, hi) in bands.items():
        if (lo < hi and lo <= h < hi) or (lo > hi and (h >= lo or h < hi)):
            return name
    return "morning"


class Sim:
    def __init__(self, doc, rules, seed=1990, passers=20, minutes=30, start_hour=10.0, rain=(12, 20), crime_minute=15,
                 label="main", enforce=True, force_collision=True):
        self.doc, self.R = doc, rules
        self.rng = random.Random(seed)
        self.seed, self.n_pass, self.minutes, self.start_hour = seed, passers, minutes, start_hour
        self.rain, self.crime_t, self.label, self.enforce = rain, crime_minute * 60.0, label, enforce
        self.force_collision = force_collision
        self.end = minutes * 60.0
        self.bands = doc["time"]
        self.groups = defaultdict(list)
        for l in doc["lines"]:
            self.groups[l["group"]].append(l)
        self.members = {k: v["members"] for k, v in doc["speakers"].items()}
        self.kind_rungs = {k: v["greeting_rungs"] for k, v in doc["speakers"].items()}
        self.places = {p["id"]: p for p in doc["places"]}
        sp = rules["speaker_overrides"]
        self.never_police = set(sp["never_police"]["speakers"])
        self.not_local = set(sp["not_local_voice"]["speakers"])
        self.prio = rules["priority"]["order"]
        self.shelf = {k: v["value"] for k, v in rules["priority"]["shelf_life_s"].items()}
        self.fam = rules["cooldowns"]["per_family"]
        self.log, self.drops, self.cut, self.asked = [], [], [], []
        self.t_deed = None
        self.heap, self.seq = [], 0
        # the ledger and the cooldown clocks
        self.heard_order = defaultdict(dict)    # group -> {line id: order heard}: what HE heard
        self.used = defaultdict(set)
        self.recent = defaultdict(list)
        self.counter = 0
        self.spk_line_last = defaultdict(dict)
        self.spk_last, self.spk_family_last = {}, {}
        self.spk_times = defaultdict(list)
        self.line_last_any, self.family_last, self.group_last = {}, {}, {}
        self.neigh_last = -1e9
        self.channels = []                      # every line started: the voice's timeline
        self.waiting = None                     # one line may wait for the voice

    # ------------------------------------------------------------------ the street
    def hear_radius(self, w, hushed=False):
        r = self.R["rain"]["hear_radius_m"][w]["value"]
        return min(r, self.R["after_deed"]["hear_radius_m"]["value"]) if hushed else r

    def build_tom(self):
        """Tom's position each second: walks to a point at 1.2 m/s, pauses ten to ninety seconds, again."""
        x, path = 3.0, []
        while len(path) < self.end + 5:
            tx = self.rng.uniform(3.0, 16.0) if self.rng.random() < 0.6 else self.rng.uniform(4.0, 46.0)   # he lives and works at the quay end
            n = max(1, int(abs(tx - x) / 1.2))
            for i in range(1, n + 1):
                path.append(x + (tx - x) * i / n)
            x = tx
            path.extend([x] * self.rng.randint(10, 90))
        self.tom = path

    def tom_x(self, t):
        return self.tom[min(max(int(t), 0), len(self.tom) - 1)]

    def presence(self, kind, t):
        vals = self.R["rain"]["presence"]["values"].get(kind, [1, 1, 1])
        return vals[{"dry": 0, "drizzle": 1, "rain": 2}[weather_at(t, self.rain)]]

    def make_people(self):
        rng, night = self.rng, band_of(self.start_hour, self.bands) == "night"
        weights = dict(KIND_WEIGHT)
        if night:
            weights.update({"night_shift": 3.0, "pensioner": 0.2, "shopkeeper": 0.4, "laundry_worker": 0.2})
        pool = list(weights.items()) + [(k, w) for k, (sid, w) in NAMED.items()]
        used_named, used_ids = set(), {p[0] for p in LOCALS}
        arrivals, guard = [], 0
        while len(arrivals) < self.n_pass and guard < 100000:
            guard += 1
            t = rng.uniform(15.0, self.end - 15.0)
            kind = self._draw(pool, used_named)
            if rng.random() <= self.presence(kind, t):
                arrivals.append((t, kind))
            elif kind in NAMED:
                used_named.discard(kind)
        arrivals.sort()
        if self.force_collision and self.crime_t and arrivals:
            j = min(range(len(arrivals)), key=lambda i: abs(arrivals[i][0] - (self.crime_t + 2.0)))
            arrivals[j] = (self.crime_t + 2.0, arrivals[j][1])
            arrivals.sort()
        people = []
        for t, kind in arrivals:
            if kind in NAMED:
                sid = NAMED[kind][0]
                standing = NAMED_STANDING[sid]
            else:
                mem = [m for m in self.members[kind] if m not in used_ids] or self.members[kind]
                sid = rng.choice(mem)
                used_ids.add(sid)
                standing = self._draw_standing()
                if sid == "lena":
                    standing = "owner"          # Sheila holds at the first rung until she trusts him, and is never a stranger
                if sid in ("zlata", "ferko", "dusan") and standing == "stranger":
                    standing = "owner"          # the dispatcher and the drivers know who he is from the first day
            people.append({"id": sid, "kind": kind, "standing": standing, "t_c": t, "d_c": rng.uniform(1.0, 6.0),
                           "dir": rng.choice([-1, 1]), "speed": rng.uniform(1.2, 1.5), "stops": rng.random() < 0.30,
                           "bumps": rng.random() < 0.10, "passer": True})
        for sid, kind, x, standing in LOCALS:
            if kind in ("shopkeeper", "pensioner") and night:
                continue
            people.append({"id": sid, "kind": kind, "standing": standing, "x": x, "d_c": 2.0 if sid != "ada" else 5.0, "passer": False, "stops": True, "bumps": False})
        for p in people:
            p["windows"] = self._windows(p)
        self.people = people
        passers = [p for p in people if p["passer"]]
        self.asks = []
        for minute in (6, 22):
            if passers:
                p = min(passers, key=lambda q: abs(q["t_c"] - minute * 60.0))
                if p not in [a for a in self.asks]:
                    self.asks.append(p)

    def _draw(self, pool, used_named):
        total = sum(w for k, w in pool if k not in used_named)
        r = self.rng.uniform(0, total)
        for k, w in pool:
            if k in used_named:
                continue
            r -= w
            if r <= 0:
                if k in NAMED:
                    used_named.add(k)
                return k
        return pool[0][0]

    def _draw_standing(self):
        r = self.rng.random()
        for s, w in STANDING_DRAW:
            r -= w
            if r <= 0:
                return s
        return "stranger"

    def pos(self, p, t):
        if not p["passer"]:
            return p["x"]
        return self.tom_x(p["t_c"]) + p["dir"] * p["speed"] * (t - p["t_c"])

    def dist_tom(self, p, t):
        if p["passer"]:
            return math.hypot(p["d_c"], 2.0 * (t - p["t_c"]))       # closing at about 2 m a second
        return math.hypot(abs(self.tom_x(t) - p["x"]), p["d_c"])

    def _windows(self, p):
        """The spells in which he is within the dry hearing radius of this person: (from, to, closest)."""
        R0, wins, cur = self.hear_radius("dry"), [], None
        lo = max(0.0, p["t_c"] - 40.0) if p["passer"] else 0.0
        hi = min(self.end, p["t_c"] + 40.0) if p["passer"] else self.end
        t = lo
        while t <= hi:
            d = self.dist_tom(p, t)
            if d <= R0:
                cur = [t, t, d] if cur is None else [cur[0], t, min(cur[2], d)]
            elif cur is not None:
                wins.append(tuple(cur))
                cur = None
            t += 1.0
        if cur is not None:
            wins.append(tuple(cur))
        return wins

    def in_earshot(self, p, t, hushed=False):
        return self.dist_tom(p, t) <= self.hear_radius(weather_at(t, self.rain), hushed)

    # ------------------------------------------------------------------ the picker
    def cond_ok(self, l, ctx):
        c = l["conditions"]
        if "standing" in c and ctx["standing"] not in c["standing"]:
            return False
        if "weather" in c and ctx["weather"] not in c["weather"]:
            return False
        if "time" in c and ctx["time"] not in c["time"]:
            return False
        if "sure" in c and ctx.get("sure") != c["sure"]:
            return False
        if "destination" in c and ctx.get("destination") != c["destination"]:
            return False
        if "since_deed_s" in c:
            s = ctx.get("since_deed")
            if s is None or not (c["since_deed_s"][0] <= s <= c["since_deed_s"][1]):
                return False
        if "rain_began_within_s" in c:
            s = ctx.get("rain_began_within_s")
            if s is None or s > c["rain_began_within_s"]:
                return False
        return True

    def eligible(self, group, ctx, speaker):
        out = []
        for l in self.groups.get(group, []):
            if not self.cond_ok(l, ctx):
                continue
            if speaker in self.not_local and l["dialect"] == "local":
                continue
            if speaker in self.never_police and l.get("calls_police"):
                continue
            out.append(l)
        return out

    def pick(self, group, ctx, speaker, t, must_answer=False):
        """Returns (line, refill, reason). Pure: nothing is committed here."""
        el = self.eligible(group, ctx, speaker)
        if not el:
            return None, False, "no eligible line"
        per_line = self.R["cooldowns"]["per_line"]
        s_floor = per_line["same_speaker_same_line_s"]["value"] if self.enforce else 0
        a_floor = per_line["any_speaker_same_line_s"]["value"] if self.enforce else 0

        def clear(l):
            return (t - self.spk_line_last[speaker].get(l["id"], -1e9) >= s_floor
                    and t - self.line_last_any.get(l["id"], -1e9) >= a_floor)
        used = self.used[group]
        cands = [l for l in el if l["id"] not in used and clear(l)] if self.enforce else list(el)
        refill = False
        if not cands:
            refill = True
            half = len(self.groups[group]) // 2
            hold = set(self.recent[group][-half:]) if half else set()
            cands = [l for l in el if clear(l) and l["id"] not in hold]
            if not cands:
                cands = [l for l in el if clear(l)]
        if not cands:
            if must_answer:
                el = sorted(el, key=lambda l: self.heard_order[group].get(l["id"], -1))
                return el[0], True, "oldest heard: a question is answered"
            return None, False, "every eligible line is inside a floor: silence rather than a repeat"
        l = self.rng.choices(cands, weights=[max(1, x["weight"]) for x in cands], k=1)[0]
        return l, refill, ""

    def commit(self, rec):
        l, speaker, t, heard = rec["line"], rec["speaker"], rec["t"], rec["heard"]
        g = l["group"]
        if heard:
            if rec["refill"]:
                self.used[g] = set()
            self.counter += 1
            self.heard_order[g][l["id"]] = self.counter
            self.used[g].add(l["id"])
            self.recent[g].append(l["id"])
            if len(self.recent[g]) > len(self.groups[g]):
                self.recent[g].pop(0)
        fam = family_of(l["situation"])
        self.spk_line_last[speaker][l["id"]] = t
        self.spk_last[speaker] = t
        self.spk_family_last[(speaker, fam)] = t
        self.spk_times[speaker].append(t)
        self.line_last_any[l["id"]] = t
        self.family_last[fam] = t
        self.group_last[g] = t
        if self.fam[fam]["class"] == "neighbour":
            self.neigh_last = t

    # ------------------------------------------------------------------ the rules around a pick
    def silent_because(self, sit, speaker, t, p, hush, answer):
        if not self.enforce:
            return None
        cd, fam = self.R["cooldowns"], family_of(sit)
        f = self.fam[fam]
        if t - self.family_last.get(fam, -1e9) < f["gap_s"]["value"]:
            return "family gap (%s)" % fam
        if not answer and t - self.spk_family_last.get((speaker, fam), -1e9) < f["speaker_s"]["value"]:
            return "speaker's family cooldown (%s)" % fam
        if not answer:
            if t - self.spk_last.get(speaker, -1e9) < cd["per_speaker_any_line_s"]["value"]:
                return "speaker spoke inside 15 s"
            if len([x for x in self.spk_times[speaker] if t - x < 600]) >= cd["per_speaker_lines_per_10min"]["value"]:
                return "speaker has had four in ten minutes"
        if fam != "crime":
            mc = cd["lines_per_minute_cap"]
            if len([r for r in self.log if r["heard"] and r["family"] != "crime" and t - r["t"] < mc["window_s"]["value"]]) >= mc["lines"]["value"]:
                return "minute cap"
        if fam == "crime":
            cap = cd["crime_chorus_cap"]
            if len([r for r in self.log if r["family"] == "crime" and t - r["t"] < cap["window_s"]["value"]]) >= cap["lines"]["value"]:
                return "crime chorus cap"
        if f["class"] == "neighbour":
            gap = cd["neighbours_talk_min_gap_s"]["value"]
            if weather_at(t, self.rain) != "dry":
                gap *= cd["neighbours_rain_multiplier"]["value"]
            if hush:
                gap *= self.R["after_deed"]["gap_multiplier"]["value"]
            if t - self.neigh_last < gap:
                return "neighbours' gap"
        return None

    def attempt(self, sit, p, t, ctx_extra=None, chance=1.0, hush=False, answer=False, must_answer=False):
        self.voice_advance(t)
        kind, speaker = p["kind"], p["id"]
        ctx = {"weather": weather_at(t, self.rain), "time": band_of(self.start_hour + t / 3600.0, self.bands), "standing": p["standing"]}
        if self.t_deed is not None and 0 <= t - self.t_deed <= self.R["after_deed"]["hour_s"]["value"]:
            ctx["since_deed"] = t - self.t_deed
        if ctx_extra:
            ctx.update(ctx_extra)
        if sit == "greeting":
            sit = "greeting." + p["standing"]
            if p["standing"] not in self.kind_rungs.get(kind, []):
                return self._drop(t, sit, speaker, "%s has no %s greeting: silent" % (kind, p["standing"]))
        if chance < 1.0 and self.rng.random() > chance:
            return self._drop(t, sit, speaker, "the chance roll failed")
        in_hour = self.t_deed is not None and p.get("hushed") and 0 <= t - self.t_deed <= self.R["after_deed"]["hour_s"]["value"]
        if self.enforce and in_hour and sit in self.R["after_deed"]["silent_for_witnesses"]:
            return self._drop(t, sit, speaker, "a witness within the hour says nothing of this kind")
        why = self.silent_because(sit, speaker, t, p, hush or bool(in_hour), answer)
        if why:
            return self._drop(t, sit, speaker, why)
        if sit == "asked_way" and ctx.get("knows"):
            group = "way/to/%s@anyone" % ctx["destination"]
        else:
            group = "%s@%s" % (bank_of(sit), kind)
        fam = family_of(sit)
        if self.enforce and fam not in self.R["cooldowns"]["per_group"]["except"] and t - self.group_last.get(group, -1e9) < self.R["cooldowns"]["per_group"]["min_gap_s"]["value"]:
            return self._drop(t, sit, speaker, "the group spoke inside a minute")
        l, refill, reason = self.pick(group, ctx, speaker, t, must_answer)
        if not l:
            return self._drop(t, sit, speaker, reason)
        self.place(l, p, t, refill, bool(in_hour) or hush, ctx.get("sure"))
        return True

    def _drop(self, t, sit, speaker, why):
        self.drops.append({"t": round(t, 1), "situation": sit, "speaker": speaker, "why": why, "id": None})
        return False

    # ------------------------------------------------------------------ the voice: one at a time, priority, shelf life
    def voice_advance(self, t):
        """A waiting line starts when the voice is free; if something else has begun meanwhile it waits again, or its shelf life ends."""
        while self.waiting and self.waiting["t"] <= t:
            w = self.waiting
            gap = self.R["cooldowns"]["start_gap_s"]["value"]
            sounding = [c for c in self.channels if c["t"] + c["dur"] > w["t"]]
            cap = self.R["priority"]["voices"]["crime" if w["prio"] >= 90 else "ordinary"]["value"]
            if len(sounding) >= cap:
                ends = sorted(c["t"] + c["dur"] for c in sounding)
                w["t"] = ends[len(sounding) - cap] + gap
                shelf_key = {"greet": "greet", "bump": "bumped", "way": "asked_way", "crime": "crime"}.get(family_of(w["line"]["situation"]), family_of(w["line"]["situation"]))
                if w["t"] - w["ready"] > self.shelf.get(shelf_key, 5):
                    self.drops.append({"t": round(w["ready"], 1), "situation": w["line"]["situation"], "speaker": w["speaker"], "id": w["line"]["id"],
                                       "why": "shelf life: the voice was taken while it waited"})
                    self.waiting = None
                continue
            self.waiting = None
            self._start(w)

    def place(self, l, p, t, refill, hush, sure):
        sit = l["situation"]
        pr, fam, gap = self.prio.get(sit, 10), family_of(sit), self.R["cooldowns"]["start_gap_s"]["value"]
        shelf_key = {"greet": "greet", "bump": "bumped", "way": "asked_way", "crime": "crime"}.get(fam, fam)
        shelf = self.shelf.get(shelf_key, 5)
        dur = LEAD_S + len(l["text"].split()) / TALK_SPEED
        rec = {"line": l, "speaker": p["id"], "p": p, "t": t, "dur": dur, "refill": refill, "sure": sure, "ready": t, "prio": pr,
               "hushed": hush or l["delivery"] == "hushed"}
        voices = self.R["priority"]["voices"]
        cap = voices["crime"]["value"] if pr >= 90 else voices["ordinary"]["value"]
        playing = [c for c in self.channels if c["t"] + c["dur"] > t]
        last_end = max([c["t"] + c["dur"] for c in self.channels] or [-1e9])
        if pr >= 90:
            # a crime line fades the neighbours' talk that is playing (they stop for it)
            for c in playing:
                if self.fam[family_of(c["line"]["situation"])]["class"] == "neighbour":
                    self.cut.append({"t": round(t, 1), "cut": c["line"]["id"], "by": l["id"]})
                    c["dur"] = (t - c["t"]) + 0.4
            playing = [c for c in self.channels if c["t"] + c["dur"] > t]
            last_end = max([c["t"] + c["dur"] for c in self.channels] or [-1e9])
        if len(playing) < cap and (cap > 1 or t >= last_end + gap):
            return self._start(rec)
        ends = sorted(c["t"] + c["dur"] for c in playing)
        free_at = (ends[len(playing) - cap] if len(playing) >= cap else last_end) + gap
        wait = free_at - t
        if wait > shelf:
            self.drops.append({"t": round(t, 1), "situation": sit, "speaker": p["id"], "id": l["id"],
                               "why": "shelf life: would wait %.1f s for the voice" % wait})
            return False
        rec["t"] = free_at
        if self.waiting:
            if pr > self.waiting["prio"]:
                old = self.waiting["line"]
                self.drops.append({"t": round(t, 1), "situation": old["situation"], "speaker": self.waiting["speaker"], "id": old["id"],
                                   "why": "replaced while waiting by a higher priority (%s)" % l["id"]})
                self.waiting = rec
                return True
            self.drops.append({"t": round(t, 1), "situation": sit, "speaker": p["id"], "id": l["id"],
                               "why": "a waiting line of equal or higher priority"})
            return False
        self.waiting = rec
        return True

    def _start(self, rec):
        l, p = rec["line"], rec["p"]
        t = rec["t"]
        radius = self.hear_radius(weather_at(t, self.rain), rec["hushed"])
        d = self.dist_tom(p, t)
        heard = d <= radius
        rec["heard"] = heard
        fam = family_of(l["situation"])
        self.channels.append({"t": t, "dur": rec["dur"], "line": l})
        self.log.append({"t": round(t, 1), "id": l["id"], "text": l["text"], "kind": l["kind"], "speaker": rec["speaker"],
                         "situation": l["situation"], "family": fam, "group": l["group"], "prio": rec["prio"], "heard": heard,
                         "dist": round(d, 1), "delivery": l["delivery"], "weather": weather_at(t, self.rain), "sure": rec["sure"],
                         "waited": round(t - rec["ready"], 1), "class": self.fam[fam]["class"]})
        self.commit(rec)
        return True

    # ------------------------------------------------------------------ the walk
    def push(self, t, order, kind, p=None, data=None):
        self.seq += 1
        heapq.heappush(self.heap, (t, order, self.seq, kind, p, data))

    def run(self):
        self.build_tom()
        self.make_people()
        c = self.R["chance"]
        for p in self.people:
            for (a, b, dmin) in p["windows"]:
                if p["passer"]:
                    self.push(p["t_c"] - 1.5 if dmin > 3.0 else a + 0.5, 1, "greet", p)
                    if p["bumps"] and dmin < 4.0:
                        self.push(p["t_c"] - 0.6, 0, "bump", p)
                    if p["stops"]:
                        self.push(b, 2, "farewell", p)
                elif b - a >= 8:
                    self.push(a + 1.0, 1, "greet", p)
                    self.push(b, 2, "farewell", p)
        for p in self.asks:
            self.push(p["t_c"], 0, "ask", p)
        self.push(self.rain[0] * 60.0, 0, "rain_begins")
        if self.crime_t:
            self.push(self.crime_t, -1, "crime")
        t = 5.0
        while t < self.end:
            self.push(t, 3, "neighbours")
            t += 5.0
        while self.heap:
            t, _, _, kind_e, p, data = heapq.heappop(self.heap)
            if t > self.end + 60:
                break
            self.voice_advance(t)
            if kind_e == "greet":
                if self.in_earshot(p, t):
                    g = c["greet"]
                    ch = min(g["capped_at"], g[p["standing"]]["value"] * g["kind_multiplier"].get(p["kind"], 1.0) * g["weather_multiplier"][weather_at(t, self.rain)])
                    self.attempt("greeting", p, t, chance=ch)
            elif kind_e == "bump":
                self.attempt("bumped", p, t, chance=c["bump"]["value"])
            elif kind_e == "farewell":
                if self.in_earshot(p, t - 0.5):
                    self.attempt("farewell", p, t, chance=c["farewell"]["value"])
            elif kind_e == "ask":
                self.do_ask(p, t)
            elif kind_e == "rain_begins":
                self.do_rain_begins(t)
            elif kind_e == "rain_line":
                self.attempt("rain_starts", p, t, ctx_extra={"rain_began_within_s": t - data}, chance=c["rain_starts"]["value"])
            elif kind_e == "crime":
                self.do_crime(t)
            elif kind_e == "crime_line":
                self.attempt("crime_" + data, p, t, ctx_extra={"sure": data}, chance=c["crime"][data]["value"])
            elif kind_e == "neighbours":
                self.do_neighbours(t)
        self.voice_advance(1e9)
        return self.report()

    def do_ask(self, p, t0):
        t = t0 + 0.5
        dest = self.rng.choice(sorted(self.places))
        pl = self.places[dest]
        cls = "street" if pl["class"] == "street" else "town" if pl["src"].startswith("hook-cast") else "atlas_far" if pl["far"] else "atlas_near"
        knows = self.rng.random() < KNOWS_PLACE[cls]
        self.asked.append({"t": round(t, 1), "who": p["id"], "dest": dest, "knows": knows})
        self.attempt("asked_way", p, t, ctx_extra={"destination": dest, "knows": knows}, answer=True, must_answer=True)

    def do_rain_begins(self, t):
        for p in self.people:
            if p["passer"] and not any(a - 6 <= t <= b + 6 for a, b, _ in p["windows"]):
                continue
            if self.in_earshot(p, t + 3):
                self.push(t + self.rng.uniform(1.0, 8.0), 1, "rain_line", p, t)

    def do_crime(self, t):
        self.t_deed = t
        x_c = min(46.0, max(3.0, self.tom_x(t) + self.rng.uniform(-25.0, 25.0)))   # it happens within sight of where he is
        near_m = self.R["after_deed"]["near_m"]["value"]
        face_m = 8.0 if band_of(self.start_hour + t / 3600.0, self.bands) != "night" else 5.0
        for p in self.people:
            if p["passer"] and abs(t - p["t_c"]) >= 25.0:
                continue
            px = self.pos(p, t)
            d = math.hypot(px - x_c, 5.0)
            looking = self.rng.random() < 0.60       # facing the right way, with an open line of sight (the ladder's detect needs both)
            sure = ("face" if d <= face_m else "shape" if d <= 40.0 else "noise" if d <= 80.0 else None) if looking else ("noise" if d <= 80.0 else None)
            if d <= near_m or sure in ("face", "shape"):
                p["hushed"] = True
            if sure:
                self.push(t + {"noise": 1.5, "shape": 2.0, "face": 1.0}[sure] + self.rng.uniform(0.0, 1.2), 0, "crime_line", p, sure)

    def do_neighbours(self, t):
        w = weather_at(t, self.rain)
        near = [p for p in self.people if self.in_earshot(p, t)]
        if len(near) < 2:
            return
        in_hour = self.t_deed is not None and 0 <= t - self.t_deed <= self.R["after_deed"]["hour_s"]["value"]
        hushed = [p for p in near if p.get("hushed")] if in_hour else []
        sit = "after_deed" if hushed else "in_rain" if w != "dry" else None
        if sit is None:
            return
        if self.rng.random() < EXISTING_AMBIENT_SHARE[w]:
            # the street's own exchange takes this slot; it stands on the same clock
            if t - self.neigh_last >= self.R["cooldowns"]["neighbours_talk_min_gap_s"]["value"]:
                self.neigh_last = t
            return
        p = self.rng.choice(hushed or near)
        self.attempt(sit, p, t, chance=self.R["chance"][sit]["value"], hush=bool(hushed))

    # ------------------------------------------------------------------ the report
    @staticmethod
    def _count(xs):
        out = defaultdict(int)
        for x in xs:
            out[x] += 1
        return dict(sorted(out.items(), key=lambda kv: -kv[1]))

    def report(self):
        heard = [r for r in self.log if r["heard"]]
        R = self.R
        minutes = defaultdict(int)
        for r in heard:
            minutes[int(r["t"] // 60)] += 1

        def busiest_of(rows):
            ts = sorted(r["t"] for r in rows)
            best, at, j = 0, 0.0, 0
            for i, t0 in enumerate(ts):
                while ts[j] < t0 - 60.0 + 1e-9:
                    j += 1
                if i - j + 1 > best:
                    best, at = i - j + 1, t0
            return best, at
        busiest, at = busiest_of(heard)
        busiest_nc, _ = busiest_of([r for r in heard if r["family"] != "crime"])
        times = sorted(r["t"] for r in heard)
        gaps, prev = [], 0.0
        for t in times:
            gaps.append((t - prev, prev, t))
            prev = t
        gaps.append((self.end - prev, prev, self.end))
        longest = max(gaps)
        quiet = sum(1 for m in range(self.minutes) if minutes.get(m, 0) == 0)
        same_spk, any_spk = [], []
        by_spk, by_line, by_text = defaultdict(dict), {}, defaultdict(list)
        for r in sorted(heard, key=lambda r: r["t"]):
            if r["id"] in by_spk[r["speaker"]]:
                dt = r["t"] - by_spk[r["speaker"]][r["id"]]
                if dt < R["cooldowns"]["per_line"]["same_speaker_same_line_s"]["value"]:
                    same_spk.append([r["id"], r["speaker"], round(dt, 1)])
            by_spk[r["speaker"]][r["id"]] = r["t"]
            if r["id"] in by_line and by_line[r["id"]][1] != r["speaker"]:
                dt = r["t"] - by_line[r["id"]][0]
                if dt < R["cooldowns"]["per_line"]["any_speaker_same_line_s"]["value"]:
                    any_spk.append([r["id"], by_line[r["id"]][1], r["speaker"], round(dt, 1)])
            by_line[r["id"]] = (r["t"], r["speaker"])
            by_text[r["text"]].append(r["t"])
        same_words = [[t, len(v)] for t, v in by_text.items() if len(v) > 1]
        neigh = sorted(r["t"] for r in self.log if r["class"] == "neighbour")
        neigh_gaps = [b - a for a, b in zip(neigh, neigh[1:])]
        gg = defaultdict(list)
        for r in sorted(self.log, key=lambda r: r["t"]):
            if r["family"] not in R["cooldowns"]["per_group"]["except"]:
                gg[r["group"]].append(r["t"])
        group_gaps = [min(b - a for a, b in zip(v, v[1:])) for v in gg.values() if len(v) > 1]
        crime_lines = [r for r in self.log if r["family"] == "crime"]
        coll = None
        if self.crime_t:
            over2 = []
            for r in self.log:
                if r["family"] != "greet":
                    continue
                r_end = r["t"] + LEAD_S + len(r["text"].split()) / TALK_SPEED
                for c in crime_lines:
                    c_end = c["t"] + LEAD_S + len(c["text"].split()) / TALK_SPEED
                    if r["t"] < c_end and c["t"] < r_end:
                        over2.append([r["id"], c["id"]])
            window = [r for r in self.log if r["family"] == "greet" and self.crime_t <= r["t"] <= self.crime_t + 20.0]
            gd = [d for d in self.drops if str(d["situation"]).startswith("greeting") and self.crime_t <= d["t"] <= self.crime_t + 20.0]
            coll = {"greetings_played_in_the_20_s_after_the_crime": [{"t": r["t"], "id": r["id"], "waited": r["waited"]} for r in window],
                    "greetings_overlapping_a_crime_line": over2,
                    "greeting_attempts_not_played_in_those_20_s": [{"t": d["t"], "why": d["why"]} for d in gd],
                    "crime_lines": [{"t": r["t"], "id": r["id"], "sure": r["sure"], "heard": r["heard"], "speaker": r["speaker"], "waited": r["waited"]} for r in crime_lines]}
        by_sit, by_kind = defaultdict(int), defaultdict(int)
        for r in heard:
            by_sit[r["situation"]] += 1
            by_kind[r["kind"]] += 1
        ra, rb = self.rain[0] * 60.0, self.rain[1] * 60.0
        passers = [p for p in self.people if p["passer"]]
        in_rain = sum(1 for p in passers if ra <= p["t_c"] < rb)
        return {
            "label": self.label, "seed": self.seed, "minutes": self.minutes, "passers": self.n_pass, "start_hour": self.start_hour,
            "rain_minutes": list(self.rain), "crime_minute": self.crime_t / 60.0,
            "people_who_came_within_earshot": len([p for p in self.people if p["windows"]]),
            "lines_played": len(self.log), "lines_heard": len(heard),
            "heard_by_situation": dict(sorted(by_sit.items())), "heard_by_kind": dict(sorted(by_kind.items())),
            "busiest_minute_heard": busiest, "busiest_minute_at_s": round(at, 1), "busiest_minute_without_crime_lines": busiest_nc,
            "longest_gap_s": round(longest[0], 1), "longest_gap_from_s": round(longest[1], 1), "longest_gap_to_s": round(longest[2], 1),
            "minutes_with_no_line": quiet, "quiet_share": round(quiet / self.minutes, 2),
            "repeats_same_speaker_same_line_within_floor": same_spk,
            "repeats_same_line_two_speakers_within_floor": any_spk,
            "same_words_heard_twice": same_words,
            "neighbour_lines": len(neigh), "neighbour_min_gap_s": round(min(neigh_gaps), 1) if neigh_gaps else None,
            "group_min_gap_s": round(min(group_gaps), 1) if group_gaps else None,
            "attempts_not_played": len(self.drops), "not_played_by_reason": self._count([d["why"].split(":")[0].split("(")[0].strip() for d in self.drops]),
            "voice_drops": [d for d in self.drops if d.get("id")], "cut_while_playing": self.cut,
            "crime": coll, "after_deed_lines_heard": len([r for r in heard if r["situation"] == "after_deed"]),
            "asked": self.asked,
            "passers_arriving_in_the_rain_minutes": in_rain, "passers_arriving_otherwise": len(passers) - in_rain,
            "rain_minutes_length": self.rain[1] - self.rain[0], "other_minutes_length": self.minutes - (self.rain[1] - self.rain[0]),
            "log": [{k: v for k, v in r.items() if k in ("t", "id", "text", "kind", "speaker", "situation", "weather", "heard", "dist", "delivery", "waited", "sure")} for r in self.log],
        }


def simulate(doc, rules, **kw):
    return Sim(doc, rules, **kw).run()


# ---------------------------------------------------------------------------------------------------- the rules, one at a time

def rule_tests(doc, rules):
    """Small deterministic scenarios, one rule each. Returns [(id, what, passed, detail)]."""
    out = []

    def fresh(rain=(100, 101), weather_always=None):
        s = Sim(doc, rules, seed=7, rain=rain)
        s.tom = [8.0] * 6000
        return s

    def person(pid, kind, standing="stranger", hushed=False):
        return {"id": pid, "kind": kind, "standing": standing, "passer": False, "x": 8.0, "d_c": 2.0, "windows": [], "hushed": hushed}

    def line_of(s, group, idx=0):
        return s.groups[group][idx]

    # 1. a crime line fades the neighbours' talk that is playing and starts at once
    s = fresh(rain=(0, 60))
    n = line_of(s, "rain/in@shopkeeper")
    p1, p2 = person("a", "shopkeeper"), person("b", "dock_worker")
    s.place(n, p1, 10.0, False, False, None)
    c = line_of(s, "crime/noise@dock_worker")
    s.place(c, p2, 11.0, False, False, "noise")
    s.voice_advance(60.0)
    cut = [x for x in s.cut if x["cut"] == n["id"]]
    second = s.log[1] if len(s.log) > 1 else {"t": -1.0}
    ok = bool(cut) and abs(second["t"] - 11.0) < 1e-6 and (s.channels[0]["t"] + s.channels[0]["dur"]) <= 11.0 + 0.4 + 1e-6
    out.append(("rule.crime_fades_neighbour_talk", "a crime line starts at once and fades a neighbour line that is playing within 0.4 s", ok, "cut=%s start=%.1f" % (bool(cut), second["t"])))

    # 2. a crime line outranks a greeting that is waiting for the voice
    s = fresh()
    way = line_of(s, "way/ask@shopkeeper", 0)
    g = line_of(s, "greeting/stranger@driver", 0)
    cr = line_of(s, "crime/shape@laundry_worker", 0)
    s.place(way, person("a", "shopkeeper"), 0.0, False, False, None)
    s.place(g, person("b", "driver"), 0.5, False, False, None)
    s.place(cr, person("c", "laundry_worker"), 0.8, False, False, "shape")
    s.voice_advance(30.0)
    crime_rec = [r for r in s.log if r["situation"] == "crime_shape"]
    greet_rec = [r for r in s.log if r["situation"].startswith("greeting")]
    crime_first = bool(crime_rec) and crime_rec[0]["t"] == 0.8
    greet_after = (not greet_rec) or greet_rec[0]["t"] >= crime_rec[0]["t"] + crime_rec[0].get("dur", 0)
    # the greeting must not sound while the crime line does
    c_end = 0.8 + LEAD_S + len(cr["text"].split()) / TALK_SPEED
    no_overlap = (not greet_rec) or greet_rec[0]["t"] >= c_end
    out.append(("rule.crime_outranks_greeting", "a crime line and a greeting wanting the voice together: the crime line sounds first and the greeting never sounds over it (it waits or is dropped)",
                crime_first and no_overlap, "crime at %s; greeting %s; drops %s" % ([r["t"] for r in crime_rec], [r["t"] for r in greet_rec], [d["why"][:40] for d in s.drops])))

    # 3. a higher priority replaces a waiting line
    s = fresh()
    short = dict(s.groups["way/ask@shopkeeper"][0], id="test.short", text="Over there, love.")      # a short line, so the next one can wait within its shelf life
    s.place(short, person("a", "shopkeeper"), 0.0, False, False, None)
    s.place(line_of(s, "farewell@driver", 0), person("b", "driver"), 0.4, False, False, None)               # waits behind it
    s.place(line_of(s, "way/ask@pensioner", 0), person("c", "pensioner"), 0.6, False, False, None)          # an answer (75) replaces a goodbye (45)
    replaced = [d for d in s.drops if "replaced while waiting" in d["why"]]
    out.append(("rule.higher_priority_replaces_waiting", "one line may wait; a higher priority replaces it (an answer to a question replaces a goodbye)", len(replaced) == 1, str([d["why"][:50] for d in s.drops])))

    # 4. neighbours' talk at most every 45 s (67.5 in rain)
    s = fresh(rain=(0, 3000))
    a, b = person("a", "shopkeeper"), person("b", "pensioner")
    s.rain = (0, 3000)
    t0 = 200.0
    first = s.attempt("in_rain", a, t0)
    early = s.silent_because("in_rain", "b", t0 + 60.0, b, False, False)
    late = s.silent_because("in_rain", "b", t0 + 70.0, b, False, False)
    out.append(("rule.neighbours_gap_in_rain", "neighbours' talk in rain: 60 s after the last is silent (45 x 1.5 = 67.5 s), 70 s after is allowed", first and early == "neighbours' gap" and late is None, "%s / %s" % (early, late)))
    s = fresh(rain=(1000, 1001))
    first = s.attempt("in_rain", a, 50.0) if False else None
    s.neigh_last = 50.0
    d1 = s.silent_because("in_rain", "b", 50.0 + 44.0, b, False, False)
    d2 = s.silent_because("in_rain", "b", 50.0 + 46.0, b, False, False)
    out.append(("rule.neighbours_gap_dry", "neighbours' talk in the dry: 44 s after the last is silent, 46 s after is allowed (RULINGS: at most every 45 s)", d1 == "neighbours' gap" and d2 is None, "%s / %s" % (d1, d2)))

    # 5. the hush: after a deed a witness's neighbour talk comes at most every 90 s, and no greetings, rain or farewells
    s = fresh(rain=(1000, 1001))
    s.t_deed = 0.0
    w1 = person("w", "shopkeeper", hushed=True)
    s.neigh_last = 100.0
    h1 = s.silent_because("after_deed", "w", 100.0 + 80.0, w1, True, False)
    h2 = s.silent_because("after_deed", "w", 100.0 + 95.0, w1, True, False)
    out.append(("rule.hush_doubles_the_gap", "in the hour after a deed a witness's neighbour talk is at most every 90 s: 80 s silent, 95 s allowed", h1 == "neighbours' gap" and h2 is None, "%s / %s" % (h1, h2)))
    before = len(s.log)
    played = s.attempt("greeting", w1, 300.0)
    out.append(("rule.witness_says_no_hello", "a witness within the hour after a deed says no greeting", (not played) and len(s.log) == before, str(s.drops[-1]["why"]) if s.drops else ""))

    # 6. the bag: a speaker's greetings, ten minutes apart, never repeat a line until the pool is used
    s = fresh()
    g = person("g", "shopkeeper", "owner")
    pool_n = len(s.eligible("greeting/owner@shopkeeper", {"weather": "dry", "time": "morning", "standing": "owner"}, "g"))
    said = []
    t = 0.0
    for i in range(pool_n):
        t += 700.0
        s.t_deed = None
        s.attempt("greeting", g, t)
    said = [r["id"] for r in s.log if r["speaker"] == "g"]
    out.append(("rule.bag_uses_every_line_once", "ten minutes apart, one speaker's %d greetings are %d different lines before any repeats" % (pool_n, pool_n), len(said) == pool_n and len(set(said)) == pool_n, "said %d, distinct %d" % (len(said), len(set(said)))))

    # 7. never-police: Rita, Ron, Sheila, Hal, Wayne, Susan and Dennis are never given a line that rings the police
    bad = []
    for sid, kind in (("rita", "shopkeeper"), ("hal", "shopkeeper"), ("victor", "shopkeeper"), ("lena", "office_worker"), ("tibor", "office_worker"), ("drago", "dock_worker"), ("rocco", "ron")):
        s = fresh()
        for k in range(60):
            ctx = {"weather": "dry", "time": "morning", "standing": "stranger", "sure": "noise"}
            l, _, _ = s.pick("crime/noise@%s" % kind, ctx, sid, 5000.0 * (k + 1))
            if l and l.get("calls_police"):
                bad.append((sid, l["id"]))
            if l:
                s.spk_line_last[sid][l["id"]] = 5000.0 * (k + 1)
    out.append(("rule.never_police_never_rings", "the seven who never go to the police are never picked a line that rings them (420 picks)", not bad, str(bad[:3])))

    # 8. a speaker whose voice is not local never gets a dialect line
    bad = []
    for sid, kind in (("vesna", "pensioner"), ("takeaway_m", "shopkeeper"), ("takeaway_f", "shopkeeper")):
        for sit, bank in (("greeting.stranger", "greeting/stranger"), ("greeting.owner", "greeting/owner"), ("bumped", "bumped"), ("in_rain", "rain/in"), ("farewell", "farewell"), ("after_deed", "deed/after")):
            s = fresh()
            for k in range(40):
                ctx = {"weather": "rain", "time": "evening", "standing": sit.split(".")[1] if "." in sit else "stranger", "since_deed": 100.0}
                l, _, _ = s.pick("%s@%s" % (bank, kind), ctx, sid, 5000.0 * (k + 1))
                if l and l["dialect"] == "local":
                    bad.append((sid, l["id"]))
                if l:
                    s.spk_line_last[sid][l["id"]] = 5000.0 * (k + 1)
    out.append(("rule.not_local_voice_no_dialect", "Nora and the Tangs are never picked a line in local dialect (720 picks)", not bad, str(bad[:3])))

    # 9. a question is always answered, even from a spent pool
    s = fresh()
    pa = person("q", "shopkeeper")
    got = 0
    for k in range(30):
        ctx = {"weather": "dry", "time": "morning", "standing": "stranger"}
        l, _, _ = s.pick("way/ask@shopkeeper", ctx, "q", 10.0 + k, must_answer=True)
        if l:
            got += 1
            s.spk_line_last["q"][l["id"]] = 10.0 + k
            s.line_last_any[l["id"]] = 10.0 + k
            s.used["way/ask@shopkeeper"].add(l["id"])
    out.append(("rule.question_always_answered", "thirty questions in thirty seconds from one shopkeeper are all answered (the oldest-heard line when the pool is spent)", got == 30, "answered %d of 30" % got))
    return out
