#!/usr/bin/env python3
"""LEDGER combat and stealth simulator (seeded, repeatable).

Runs the general rules of COMBAT-SYSTEM.md (CS-03 to CS-19) on thousands of
fights and takedowns across player styles, weapons, opponents, numbers, places
and light, and prints the headline numbers against the target bands.

    python3 combat_sim.py              # default seed 1990, writes results.json
    python3 combat_sim.py --seed 7 --n 2000

Every tuning value lives in TUNE below, named as in COMBAT-SYSTEM.md, so the
loops can retune in minutes. Nothing here is a listed case: deaths, knock-outs
and yields come only from force, zone, the man's state and his temper.
"""
import argparse, json, math, random, statistics, sys
from collections import Counter, defaultdict

# ---------------------------------------------------------------- tuning
TUNE = {
    # CS-02 actions: wind-up s, recovery s, wind cost, force, kind
    "act": {
        "jab":    dict(wu=0.32, rec=0.25, wind=0.12, force=1.0, kind="blunt"),
        "heavy":  dict(wu=0.74, rec=0.50, wind=0.20, force=2.6, kind="blunt"),
        "kick":   dict(wu=0.55, rec=0.45, wind=0.10, force=1.7, kind="blunt"),
        "stamp":  dict(wu=0.60, rec=0.40, wind=0.09, force=1.6, kind="blunt"),   # boot on a downed man
        "grab":   dict(wu=0.45, rec=0.35, wind=0.08, force=0.0, kind="grab"),
        "shove_surface": dict(wu=0.50, rec=0.40, wind=0.10, force=2.0, kind="blunt"),
    },
    # CS-06 weapons as data: force multiplier on the strike, wind-up, kind, menace when shown
    "weapon": {
        "fists":  dict(mult=1.0, wu=0.0, kind="blunt", menace=0.0, breaks=None),
        "knuckleduster": dict(mult=1.35, wu=0.0, kind="blunt", menace=0.35, breaks=None),
        "cosh":   dict(mult=1.9, wu=0.10, kind="blunt", menace=0.45, breaks=None),
        "bat":    dict(mult=2.3, wu=0.25, kind="blunt", menace=0.55, breaks=None),
        "brick":  dict(mult=2.0, wu=0.15, kind="blunt", menace=0.40, breaks=3),
        "chair":  dict(mult=1.7, wu=0.30, kind="blunt", menace=0.30, breaks=2),
        "knife":  dict(mult=1.0, wu=0.0, kind="edge", menace=0.75, breaks=None),
    },
    # CS-05 the body: zone weights for blunt damage and severity thresholds
    "zone_aim": {"head": 0.45, "torso": 0.40, "arms": 0.10, "legs": 0.05},
    "blunt_threshold": {"hurt": 3.0, "serious": 9.5, "critical": 15.0},
    "fists_cap_head": "serious",     # his ruling of 30 Oct: fists never kill on their own
    "boots_can_kill": True,          # his decision D2 (recommended yes): a stamp on a downed head follows the body rule
    # knife wounds: thrust or slash, by zone -> (minor, serious, critical) probabilities
    "edge_wound": {
        ("thrust", "torso"): (0.40, 0.44, 0.16),
        ("thrust", "head"):  (0.25, 0.40, 0.35),   # neck and face
        ("thrust", "arms"):  (0.70, 0.27, 0.03),
        ("thrust", "legs"):  (0.62, 0.32, 0.06),
        ("slash", "torso"):  (0.72, 0.25, 0.03),
        ("slash", "head"):   (0.65, 0.30, 0.05),
        ("slash", "arms"):   (0.85, 0.14, 0.01),
        ("slash", "legs"):   (0.80, 0.18, 0.02),
    },
    "critical_death_untreated": 0.55,   # a critical wound left alone (minutes)
    "critical_death_helped": 0.20,      # help inside the window (a passer-by, the ambulance)
    # CS-04 wind and states
    "wind_regen": 0.12, "low_wind": 0.18, "pause": (0.3, 1.4), "npc_pause": (0.2, 0.9), "counter_window": 0.45, "counter_mult": 1.5,
    "capacity": {"frank": 12.0, "boxer": 15.0, "brawler": 14.0, "big": 21.0, "knife": 12.0, "wiry": 12.0, "constable": 14.0},
    # knock-down and knock-out
    "kd_head": 0.016, "kd_torso": 0.006, "ko_base": 0.22, "ko_per_head": 0.05,
    "ko_seconds_fist": (10, 60), "ko_seconds_weapon": (30, 300),
    # CS-07 surfaces and the fall
    "fall_crit_spent": 1/50,    # RT2-12's lower bound: 1 in 50 per knock-down at an edge when spent
    "fall_serious": 0.12, "unaware_mult": 1.5,
    # CS-09 temper in a fight
    "flee_will": 0.08, "yield_will": 0.20,
    # CS-14 public: step-in and police
    "stepin_per_5s": 0.025, "stepin_per_bystander": 1.10, "police_per_s_after_20": 1/150,
}

TYPES = {  # CS-11 fighter kinds: defence skill, aggression, nerve range, preferred weapon
    "boxer":   dict(defence=0.55, aggr=0.55, nerve=(0.5, 0.8), weapon="fists"),
    "brawler": dict(defence=0.28, aggr=0.85, nerve=(0.5, 0.85), weapon="fists"),
    "big":     dict(defence=0.30, aggr=0.60, nerve=(0.55, 0.9), weapon="fists"),
    "knife":   dict(defence=0.40, aggr=0.45, nerve=(0.35, 0.7), weapon="knife"),
    "wiry":    dict(defence=0.50, aggr=0.45, nerve=(0.2, 0.5), weapon="fists"),
}

FRANK_STYLES = {  # player styles the bots play
    "patient": dict(defence=0.68, heavy_share=0.30, surface=0.25, threat_first=False, run_at=None),
    "masher":  dict(defence=0.22, heavy_share=0.60, surface=0.0, threat_first=False, run_at=None),
    "street":  dict(defence=0.62, heavy_share=0.30, surface=0.70, threat_first=False, run_at=None),
    "menace":  dict(defence=0.65, heavy_share=0.30, surface=0.30, threat_first=True, run_at=None),
    "runner":  dict(defence=0.60, heavy_share=0.25, surface=0.10, threat_first=False, run_at=0.45),
}

LEVELS = ["none", "bruise", "hurt", "serious", "critical", "dead"]


class Man:
    def __init__(self, rng, name, side, kind, weapon="fists", defence=0.5, aggr=0.6, nerve=0.6,
                 style=None, is_frank=False):
        self.rng, self.name, self.side, self.kind = rng, name, side, kind
        self.weapon = weapon
        self.weapon_uses = 0
        self.defence, self.aggr, self.nerve = defence, aggr, nerve
        self.style = style or {}
        self.is_frank = is_frank
        self.wind = 1.0
        self.dmg = defaultdict(float)     # blunt damage by zone
        self.wounds = []                  # (zone, level) for edge wounds
        self.condition = 0.0              # accumulated hurt, towards capacity
        self.capacity = TUNE["capacity"]["frank" if is_frank else kind]
        self.heavies_taken = 0
        self.weapon_hits_taken = 0
        self.state = "fresh"              # fresh, hurt, beaten, down, out, dying, dead, fled, yielded
        self.busy_until = 0.0
        self.down_until = 0.0
        self.pending = None               # (t_land, action, target)
        self.guarding = False
        self.worst = "none"
        self.manner = set()               # how it was done to him: behind, downed, yielded, weapon
        self.stamped_downed = 0
        self.counter_until = -1.0
        self.guard_until = -1.0
        self.was_out = False

    # ---- helpers
    def active(self):
        return self.state in ("fresh", "hurt")

    def standing(self):
        return self.state in ("fresh", "hurt", "beaten")

    def hurt_frac(self):
        return min(1.0, self.condition / self.capacity)

    def bump(self, level):
        if LEVELS.index(level) > LEVELS.index(self.worst):
            self.worst = level


def zone(rng, aimed=None):
    if aimed:
        return aimed
    r, acc = rng.random(), 0.0
    for z, w in TUNE["zone_aim"].items():
        acc += w
        if r <= acc:
            return z
    return "torso"


def blunt_level(d, head=False):
    t = TUNE["blunt_threshold"]
    if d >= t["critical"] * (1.0 if head else 1.5):
        return "critical"
    if d >= t["serious"]:
        return "serious"
    if d >= t["hurt"]:
        return "hurt"
    return "bruise" if d > 0 else "none"


class Fight:
    def __init__(self, rng, frank_side, other_side, place, light=0.7, bystanders=6, public=True,
                 frank_unaware_first=False):
        self.rng = rng
        self.men = frank_side + other_side
        self.place = place  # dict: near_edge prob, surface availability
        self.t = 0.0
        self.first_blow = None
        self.log = Counter()
        self.bystanders, self.public = bystanders, public
        self.ended_by = None
        self.menace = 0.3

    def foes(self, m):
        return [o for o in self.men if o.side != m.side and o.standing() and o.state != "fled"]

    def downed_foes(self, m):
        return [o for o in self.men if o.side != m.side and o.state in ("down", "out")]

    # ---- CS-09 temper
    def will(self, m):
        allies = sum(1 for o in self.men if o.side == m.side and o is not m and o.active())
        foes = [o for o in self.men if o.side != m.side and o.active()]
        fear = 0.0
        for f in foes:
            fear = max(fear, TUNE["weapon"][f.weapon]["menace"])
        outnumber = max(0, len(foes) - allies - 1) * 0.12
        w = (m.nerve * 0.9 + 0.12 * allies - 0.30 * fear - 0.45 * m.hurt_frac()
             - outnumber - (0.08 * self.menace if m.side != "F" else 0.0) - (0.1 if m.wounds else 0.0))
        return w

    def decide(self, m):
        rng = self.rng
        if m.is_frank:
            st = m.style
            if st.get("run_at") and m.hurt_frac() >= st["run_at"] and rng.random() < 0.5:
                return ("flee", None)
        if m.state == "beaten":
            if m.is_frank:
                return ("spent", None)        # Frank beaten: he can no longer fight; the fight is lost
            return ("yield", None) if m.hurt_frac() >= 0.85 or self.rng.random() < 0.5 else ("flee", None)
        if not m.is_frank:
            w = self.will(m)
            if w < TUNE["flee_will"]:
                return ("flee", None) if m.hurt_frac() < 0.85 else ("yield", None)
            if w < TUNE["yield_will"] and m.hurt_frac() > 0.45:
                return ("yield", None)
            if m.state == "hurt" and m.weapon == "fists" and rng.random() < 0.02:
                return ("pickup", None)    # CS-06: a man losing looks for something to hand
        foes = self.foes(m)
        if not foes:
            if any(o.side != m.side and o.state == "down" for o in self.men):
                return ("guard", None)        # he waits for the downed man to get up or stay down
            downed = self.downed_foes(m)
            return ("done", downed)
        # at most two swing at Frank at once (token, ER-FIGHT-02)
        target = min(foes, key=lambda o: (o.hurt_frac() if m.is_frank else 0) + rng.random() * 0.5)
        if not m.is_frank:
            swinging = sum(1 for o in self.men if o.pending and o.pending[2] is target and o is not m)
            if swinging >= 2:
                return ("circle", None)
            blade = target.weapon == "knife" or TUNE["weapon"][target.weapon]["menace"] >= 0.45
            if blade and m.weapon == "fists" and rng.random() < 0.05:
                return ("pickup", None)
            if blade and rng.random() < 0.12 and m.wind > 0.3:
                return ("grab", target)     # go for the weapon arm (CS-08 disarm)
            if rng.random() > min(0.95, m.aggr * (0.45 if blade else 1.0)):
                return ("guard", None)
        if m.wind < TUNE["low_wind"]:
            return ("gasp", None)      # emptied: hands drop while he gets his wind (1.3.2: 4 to 8 s)
        st = m.style if m.is_frank else {}
        surface_use = st.get("surface", 0) * 0.4 if m.is_frank else (0.10 if m.kind in ("brawler", "big") else 0.03)
        if self.place["surface"] and rng.random() < surface_use:
            return ("grab", target)       # anyone may put a man into a wall (CS-07)
        if m.weapon == "knife":
            return ("thrust" if rng.random() < 0.5 else "slash", target)
        heavy_share = st.get("heavy_share", 0.35) if m.is_frank else (0.5 if m.kind in ("brawler", "big") else 0.3)
        if m.is_frank and m.style is FRANK_STYLES["patient"] and target.pending:
            return ("guard", None)    # the patient player reads the wind-up and waits to counter
        return ("heavy" if rng.random() < heavy_share else "jab", target)

    # ---- resolving a landed blow
    def land(self, att, act, tgt, unaware=False, counter=False, aim=None, finishing=False):
        rng, T = self.rng, TUNE
        if not tgt.standing() and act not in ("stamp",) and not finishing:
            return
        w = T["weapon"][att.weapon]
        if act in ("thrust", "slash"):
            base_wu = 0.6 if act == "thrust" else 0.35
            p_def = 0 if unaware else tgt.defence * (0.8 if (self.t < tgt.guard_until) else 0.5) * (0.6 if tgt.wind < 0.2 else 1)
            if rng.random() < p_def * (0.7 if act == "thrust" else 1.0):
                self.log["blocked"] += 1
                tgt.counter_until = self.t + T["counter_window"]
                if rng.random() < 0.25:   # a slash on the guarding arm
                    self.edge_wound(tgt, "slash", "arms")
                return
            z = zone(rng) if not unaware else rng.choice(["torso", "torso", "head"])
            self.edge_wound(tgt, act, z)
            tgt.manner.add("weapon")
            if unaware:
                tgt.manner.add("behind")
            att.wind -= 0.06
            return
        a = T["act"][act]
        force = a["force"] * w["mult"] * (0.5 + 0.5 * max(att.wind, 0)) * (T["unaware_mult"] if unaware else 1.0) * (T["counter_mult"] if counter else 1.0)
        z = "head" if act == "stamp" and rng.random() < 0.6 else zone(rng, aim)
        if finishing:
            tgt.manner.add("downed")
        if act == "stamp":
            z = z if z == "head" else "torso"
            tgt.manner.add("downed")
            if tgt.state == "yielded":
                tgt.manner.add("yielded")
        if not unaware and act != "stamp" and tgt.standing():
            p_def = tgt.defence * (1.0 if (self.t < tgt.guard_until) else 0.55) * (0.5 if tgt.wind < 0.2 else 1.0)
            if act == "heavy" or w["mult"] > 1.5:
                p_def *= 1.1 if (self.t < tgt.guard_until) else 0.75   # the committed blow is readable: a watching man slips it
            if counter:
                p_def *= 0.3    # a blow thrown straight after a block or slip
            if att.weapon == "knife" or any(o.weapon == "knife" for o in [att]):
                pass
            if rng.random() < p_def:
                self.log["blocked"] += 1
                tgt.counter_until = self.t + T["counter_window"]
                att.busy_until += 0.3
                tgt.wind -= 0.05 * force
                if act == "heavy" and att.weapon != "fists":
                    z = "arms"; force *= 0.6   # a swung weapon breaks through to the arm
                else:
                    if att.is_frank or tgt.is_frank:
                        pass
                    return
        if w["breaks"]:
            att.weapon_uses += 1
            if att.weapon_uses >= w["breaks"]:
                att.weapon = "fists"; self.log["thing_broke"] += 1
        if att.weapon != "fists":
            tgt.weapon_hits_taken += 1
            tgt.manner.add("weapon")
        if act == "heavy":
            tgt.heavies_taken += 1
        tgt.dmg[z] += force * (1.25 if z == "head" else 1.0)
        tgt.condition += force * (1.1 if z == "head" else 0.9)
        tgt.wind -= 0.04 * force
        lvl = blunt_level(tgt.dmg[z], head=(z == "head"))
        if att.weapon in ("fists",) and act in ("jab", "heavy", "kick", "shove_surface"):
            if LEVELS.index(lvl) > LEVELS.index(T["fists_cap_head"]):
                lvl = T["fists_cap_head"]
        if act == "stamp" and not T["boots_can_kill"] and lvl == "critical":
            lvl = "serious"
        tgt.bump(lvl)
        if lvl == "critical":
            self.critical(tgt, cause="blunt_" + act)
            return
        self.log["landed_" + act] += 1
        # knock-down and knock-out
        p_kd = (T["kd_head"] if z == "head" else T["kd_torso"]) * force ** 1.6 * (1 + tgt.dmg["head"] / 6.0)
        if tgt.wind < 0.25:
            p_kd *= 1.5
        if tgt.standing() and rng.random() < min(0.9, p_kd):
            self.knockdown(tgt, z, att)
        elif tgt.condition >= tgt.capacity and tgt.state != "beaten":
            tgt.state = "beaten"; self.log["beaten"] += 1
        elif tgt.condition >= tgt.capacity * 0.4 and tgt.state == "fresh":
            tgt.state = "hurt"

    def edge_wound(self, tgt, act, z):
        probs = TUNE["edge_wound"][(act, z)]
        r = self.rng.random()
        lvl = "minor" if r < probs[0] else ("serious" if r < probs[0] + probs[1] else "critical")
        tgt.wounds.append((z, lvl))
        tgt.condition += {"minor": 1.0, "serious": 3.5, "critical": 9.0}[lvl]
        self.log["stab_" + lvl] += 1
        tgt.bump({"minor": "hurt", "serious": "serious", "critical": "critical"}[lvl])
        if lvl == "critical":
            self.critical(tgt, cause="edge_" + act)
        elif tgt.condition >= tgt.capacity:
            tgt.state = "beaten"
        elif tgt.state == "fresh":
            tgt.state = "hurt"

    def critical(self, tgt, cause):
        self.log["critical_" + cause] += 1
        if tgt.is_frank:
            tgt.state = "out"; self.log["frank_hospital"] += 1     # Frank never dies (12 Oct)
            return
        tgt.state = "dying"

    def knockdown(self, tgt, z, att):
        rng, T = self.rng, TUNE
        self.log["knockdown"] += 1
        tgt.state = "down"
        tgt.down_until = self.t + rng.uniform(2.0, 5.0)
        # the fall at an edge (CS-07)
        if rng.random() < self.place["near_edge"]:
            spent = tgt.heavies_taken >= 3 or tgt.weapon_hits_taken >= 1   # RT2-12
            r = rng.random()
            if spent and r < T["fall_crit_spent"]:
                tgt.bump("critical"); self.log["fall_critical"] += 1
                if tgt.is_frank:
                    tgt.state = "out"; self.log["frank_hospital"] += 1; return   # CS-15: Frank is out, never dying
                tgt.state = "dying"; return
            if r < T["fall_serious"]:
                tgt.dmg["head"] += 4; tgt.bump("serious"); self.log["fall_serious"] += 1
        if z == "head" and rng.random() < T["ko_base"] + T["ko_per_head"] * tgt.dmg["head"]:
            tgt.state = "out"; tgt.was_out = True; self.log["knockout"] += 1
            lo, hi = T["ko_seconds_weapon"] if att.weapon not in ("fists", "knuckleduster") else T["ko_seconds_fist"]
            tgt.down_until = self.t + rng.uniform(lo, hi)

    # ---- main loop
    def run(self, max_t=150.0, dt=0.1, frank_finishes=False):
        rng = self.rng
        while self.t < max_t:
            self.t += dt
            for m in self.men:
                if m.state in ("dead", "dying", "fled", "yielded"):
                    continue
                if m.state in ("down",) and self.t >= m.down_until:
                    m.state = "beaten" if m.condition >= m.capacity else "hurt"
                if m.state == "out":
                    continue
                if m.pending and self.t >= m.pending[0]:
                    _, act, tgt = m.pending[:3]
                    ctr = len(m.pending) > 3 and m.pending[3]
                    m.pending = None
                    if act == "grab":
                        if tgt.standing() and rng.random() > tgt.defence * 0.6:
                            self.log["grab"] += 1
                            if tgt.weapon != "fists" and rng.random() < 0.40:
                                self.log["disarmed" + ("_frank" if tgt.is_frank else "")] += 1
                                tgt.weapon = "fists"; m.busy_until = self.t + 0.6; continue
                            if self.place["surface"]:
                                self.log["surface_used"] += 1
                                m.pending = (self.t + 0.5, "shove_surface", tgt); m.busy_until = self.t + 0.9
                                continue
                    else:
                        if self.first_blow is None:
                            self.first_blow = self.t
                        self.land(m, act, tgt, counter=ctr)
                if not m.pending and (self.t >= m.busy_until or self.t < m.guard_until):
                    m.wind = min(1.0 - 0.4 * m.hurt_frac(), m.wind + TUNE["wind_regen"] * dt * (2.0 if self.t < m.guard_until else 1.0))
                if self.t < m.busy_until:
                    continue
                choice, tgt = self.decide(m)
                if choice == "flee":
                    m.state = "fled"; self.log[("frank_" if m.is_frank else "") + "fled"] += 1; continue
                if choice == "yield":
                    m.state = "yielded"; self.log["yielded"] += 1
                    if m.hurt_frac() > 0.6:
                        self.log["begged"] += 1
                    continue
                if choice == "pickup":
                    m.weapon = rng.choice(["brick", "chair"]); self.log["picked_up"] += 1
                    m.busy_until = self.t + 1.0; continue
                if choice == "spent":
                    m.busy_until = self.t + 1.0; continue
                if choice == "done":
                    return self.finish(tgt, frank_finishes)
                if choice == "gasp":
                    m.busy_until = self.t + 1.5; self.log["gasp" + ("_frank" if m.is_frank else "")] += 1; continue
                if choice in ("guard", "circle"):
                    m.guard_until = self.t + 0.4; m.busy_until = self.t + 0.4; continue
                a = TUNE["act"].get(choice) or dict(wu=0.6 if choice == "thrust" else 0.35, rec=0.35, wind=0.09)
                wu = a["wu"] + TUNE["weapon"][m.weapon]["wu"]
                if m.wind < TUNE["low_wind"]:
                    wu *= 1.3
                m.wind -= a["wind"]
                skilled_counter = rng.random() < m.defence      # the same rule for everyone (CS-01)
                ctr = self.t <= m.counter_until and skilled_counter
                if ctr:
                    wu *= 0.6; self.log["counter" + ("_frank" if m.is_frank else "")] += 1
                m.pending = (self.t + wu, choice, tgt, ctr)
                pause = 0 if ctr else rng.uniform(*(TUNE["pause"] if m.is_frank else TUNE["npc_pause"])) * (0.4 if (m.is_frank and m.style.get("heavy_share",0) > 0.5) else 1.0)
                m.busy_until = self.t + wu + a["rec"] + pause
                if pause and (m.defence > 0.5 or rng.random() < m.defence):
                    m.guard_until = m.busy_until    # a careful fighter keeps his hands up between blows
            # public: someone steps in, or the police arrive
            if self.public and self.first_blow is not None:
                if int(self.t * 10) % 50 == 0:
                    p = TUNE["stepin_per_5s"] * TUNE["stepin_per_bystander"] ** min(self.bystanders, 20)
                    if rng.random() < p:
                        self.ended_by = "stepped_in"; return self.finish([], False)
                if self.t - self.first_blow > 20 and rng.random() < TUNE["police_per_s_after_20"] * dt:
                    self.ended_by = "police"; return self.finish([], False)
            in_fight = lambda x: x.state in ("fresh", "hurt", "down")
            if len({m.side for m in self.men if in_fight(m)}) < 2:
                downed = [m for m in self.men if m.side != "F" and m.state in ("down", "out")]
                return self.finish(downed, frank_finishes)
        self.ended_by = "timeout"
        return self.finish([], False)

    def finish(self, downed, frank_finishes):
        rng = self.rng
        frank = next((m for m in self.men if m.is_frank), None)
        if frank_finishes and frank and frank.standing():
            for d in downed:
                for _ in range(3):           # the quiet decision: blows on the downed man (CS-14)
                    self.land(frank, "stamp" if frank.weapon == "fists" else "heavy", d, aim="head", finishing=True)
                    if d.state in ("dying", "dead"):
                        break
        # dying men: death or survival by help (CS-05)
        for m in self.men:
            if m.state == "dying":
                helped = self.public and rng.random() < 0.55
                p = TUNE["critical_death_helped"] if helped else TUNE["critical_death_untreated"]
                if rng.random() < p:
                    m.state = "dead"; m.bump("dead"); self.log["death"] += 1
                else:
                    m.state = "out"; self.log["survived_critical"] += 1
        if not self.ended_by:
            self.ended_by = "decided"
        return self


# ---------------------------------------------------------------- consequences (CS-16 to CS-19)
CHARGE = {"none": None, "bruise": "common assault", "hurt": "ABH (s.47)", "serious": "GBH or wounding (s.20)",
          "critical": "GBH with intent (s.18)", "dead": "manslaughter"}


def consequences(rng, fight, victim_sex_age="man"):
    out = Counter()
    for m in fight.men:
        if m.is_frank or m.side == "F" or m.worst == "none":
            continue
        if m.was_out and LEVELS.index(m.worst) < LEVELS.index("hurt"):
            m.worst = "hurt"
        charge = CHARGE[m.worst]
        intent = bool(m.manner & {"weapon", "downed", "yielded"})
        if m.worst == "serious" and intent:
            charge = "GBH with intent (s.18)"
        if m.worst == "dead" and ("weapon" in m.manner or "downed" in m.manner):
            charge = "murder"
        out["charge:" + charge] += 1
        # the street's reading of the deed (CS-17)
        sev = LEVELS.index(m.worst) / 5
        factor = 1.0
        for k, f in (("behind", 1.3), ("downed", 1.5), ("yielded", 1.6), ("weapon", 1.4)):
            if k in m.manner:
                factor *= f
        if victim_sex_age in ("woman", "over sixty"):
            factor *= 1.5
        reading = min(1.0, sev * factor)
        out["reading_band:" + ("grave" if reading >= 0.8 else "bad" if reading >= 0.45 else "talked of")] += 1
        if m.state == "dead":
            out["body"] += 1
            continue
        grudge = rng.random()
        law = rng.random()
        if law > 0.55 and m.worst in ("serious", "critical"):
            out["victim_reports"] += 1
        if grudge * sev > 0.25:
            out["revenge_" + ("with_friends" if m.nerve < 0.6 else "alone")] += 1
        if m.worst in ("serious", "critical"):
            out["hospital_days"] += rng.randint(3, 14)
        if m.state == "yielded":
            out["yielded_spared"] += 1
    return out


# ---------------------------------------------------------------- scenarios
def make_frank(rng, style, weapon="fists"):
    st = FRANK_STYLES[style]
    return Man(rng, "Frank", "F", "frank", weapon=weapon, defence=st["defence"], aggr=0.8, nerve=1.0,
               style=st, is_frank=True)


def make_foe(rng, kind, i, weapon=None):
    t = TYPES[kind]
    return Man(rng, f"{kind}{i}", "E", kind, weapon=weapon or t["weapon"], defence=t["defence"],
               aggr=t["aggr"], nerve=rng.uniform(*t["nerve"]))


PLACES = {
    "open_street": dict(near_edge=0.15, surface=True),
    "kerbside":    dict(near_edge=0.45, surface=True),
    "yard_night":  dict(near_edge=0.25, surface=True),
    "indoors":     dict(near_edge=0.30, surface=True),
    "quay":        dict(near_edge=0.35, surface=True),
}


def threat_first(rng, frank, foes, menace):
    """CS-10: a threat said before a blow. Word 0.5, shown weapon 0.8 (temper model)."""
    threat = 0.5 + 0.4 * TUNE["weapon"][frank.weapon]["menace"]   # a word 0.5; a knife shown 0.8; a gun 0.9
    folded = 0
    for f in foes:
        # pride: a man in front of his own stands longer; some call a bluff whatever their nerve
        eff = f.nerve + 0.15 * (len(foes) - 1) + rng.uniform(0.0, 0.25)
        if eff < threat * (0.8 + 0.4 * menace):
            folded += 1
    return folded == len(foes)


def run_fights(rng, n, style, weapon, n_foes, kinds, place, menace=0.3, allies=0, frank_finishes=False,
               public=True):
    res = Counter(); durations = []; cons = Counter()
    for i in range(n):
        frank = make_frank(rng, style, weapon)
        fside = [frank] + [make_foe(rng, "boxer", 100 + a) for a in range(allies)]
        for a in fside[1:]:
            a.side = "F"; a.nerve = max(a.nerve, 0.6)
        foes = [make_foe(rng, rng.choice(kinds), k) for k in range(n_foes)]
        if FRANK_STYLES[style]["threat_first"] and threat_first(rng, frank, foes, menace):
            res["ended_by_threat"] += 1; res["frank_win"] += 1; durations.append(0.0)
            continue
        f = Fight(rng, fside, foes, PLACES[place], public=public, bystanders=rng.randint(0, 12))
        f.menace = menace
        f.run(frank_finishes=frank_finishes)
        res.update(f.log)
        res["ended_by_" + f.ended_by] += 1
        frank_up = frank.state in ("fresh", "hurt", "down")
        foes_left = [x for x in foes if x.state in ("fresh", "hurt", "down")]
        if frank_up and not foes_left:
            res["frank_win"] += 1
        elif frank.state == "fled":
            res["frank_escaped"] += 1
        elif not frank_up:
            res["frank_lost"] += 1
        else:
            res["no_result"] += 1      # stopped by a bystander, the police or the clock with both still in it
        if f.first_blow is not None:
            durations.append(f.t - f.first_blow)
        cons.update(consequences(rng, f))
        for x in foes:
            res["foe_worst:" + x.worst] += 1
        res["frank_worst:" + frank.worst] += 1
    return res, durations, cons


# ---------------------------------------------------------------- stealth (CS-12, CS-13)
SURFACE_NOISE = {"dry_flags": 1.0, "wet_cobbles": 1.25, "gravel": 1.7, "metal_deck": 2.1, "glass_grit": 2.4}


def sight_p(light, dist, crouch, moving):
    """Chance per second that a watcher looking this way picks the figure out (perception ladder)."""
    if dist <= 0:
        return 1.0
    base = light ** 1.5 * (1.0 if moving else 0.55) * (0.5 if crouch and dist > 4 and light < 0.5 else 1.0)
    reach = 4 + 26 * light       # metres at which a moving figure is near-certain in this light
    return max(0.0, min(1.0, base * (reach / max(dist, 0.5)) ** 1.4 * 0.35))


def choke_death(extra_s):
    """Chance of death when a choke is held on extra_s seconds past the knock-out (D1)."""
    return max(0.0, min(0.95, (extra_s - 20) / 100.0))


def threat_table(rng, n=4000):
    out = {}
    for menace in (0.3, 0.5, 0.8):
        for weapon in ("fists", "cosh", "knife"):
            for nf in (1, 2):
                ok = 0
                for _ in range(n):
                    fr = make_frank(rng, "menace", weapon)
                    foes = [make_foe(rng, rng.choice(["boxer", "brawler", "big", "wiry"]), j) for j in range(nf)]
                    ok += threat_first(rng, fr, foes, menace)
                out[f"menace {menace} | {weapon} | {nf} man"] = round(ok / n, 3)
    return out


def approach(rng, light, surface, crouch, rain=False, alert=0.0, watchers=0, method="choke", hold_on=False):
    """Approach from 12 m behind an unaware man and try a takedown. Returns an outcome dict."""
    out = Counter()
    dist, t = 12.0, 0.0
    speed = 1.2 if crouch else 1.6
    reach = 3.6 * SURFACE_NOISE[surface] * (0.5 if crouch else 1.0) * (0.5 if rain else 1.0)
    uneasy = alert
    facing_away = True
    while dist > 1.0:
        dt = 0.25; t += dt; dist -= speed * dt
        # the man turns his head now and then; more when uneasy
        if rng.random() < (0.07 + 0.10 * light + 0.40 * uneasy) * dt:
            facing_away = False
        elif rng.random() < 0.5 * dt:
            facing_away = True
        if dist <= reach and rng.random() < 0.45 * dt:
            uneasy = min(1.0, uneasy + 0.5); out["heard"] += 1
        if not facing_away and rng.random() < sight_p(light, dist, crouch, True) * dt * 4:
            out["seen_on_approach"] += 1
            return "spotted", out
        for _ in range(watchers):     # other watchers in the street
            if rng.random() < sight_p(light, rng.uniform(6, 20), crouch, True) * dt * 0.6:
                out["witnessed"] += 1
                break
    # the last metre: a last-moment turn
    p_turn = 0.05 * SURFACE_NOISE[surface] * (1.0 if crouch else 1.5) * (1 + uneasy)
    if rng.random() < p_turn:
        return "turned", out
    if method == "choke":
        cap = TUNE["capacity"][rng.choice(["boxer", "brawler", "big", "wiry"])]
        frank_wind = 1.0
        t_ko = max(4.0, rng.gauss(7.5, 1.8))
        held = 0.0
        while held < t_ko:
            held += 1.0
            # he may break the hold: more for a big man, less as Frank keeps his wind (CS-13)
            if rng.random() < 0.035 * (cap / 14.0) * (1.6 - 0.6 * frank_wind):
                return "broke_free", out
            frank_wind = max(0.0, frank_wind - 0.06)
            if watchers and rng.random() < 0.02:
                out["struggle_seen"] += 1
        if hold_on:  # held past the knock-out on purpose (his decision D1)
            return ("dead" if rng.random() < choke_death(hold_on) else "out_held"), out
        return "out", out
    # every other takedown is the body rule on an unaware man (CS-05, CS-13)
    frank = Man(rng, "Frank", "F", "frank", weapon={"cosh": "cosh", "fist": "fists", "knife": "knife"}[method],
                defence=0.6, is_frank=True)
    frank.wind = 1.0
    tgt = make_foe(rng, rng.choice(["boxer", "brawler", "big", "wiry"]), 0)
    f = Fight(rng, [frank], [tgt], dict(near_edge=0.2, surface=True), public=False)
    if method == "knife":
        f.land(frank, "thrust", tgt, unaware=True)
    else:
        f.land(frank, "heavy", tgt, unaware=True, aim="head")
    if tgt.state == "dying":
        return ("dead" if rng.random() < TUNE["critical_death_untreated"] else "critical_survived"), out
    if tgt.state == "out":
        return ("out_serious" if tgt.worst == "serious" else "out"), out
    if tgt.state == "down":
        return "knocked_down", out
    if method == "knife":
        return ("serious" if tgt.worst == "serious" else "wounded"), out
    return "staggered", out
    return "none", out


def run_stealth(rng, n):
    rows = {}
    for light_name, light in (("doorway_dark", 0.12), ("unlit_street", 0.25), ("lamp", 0.7), ("day", 1.0)):
        for crouch in (False, True):
            for surface in ("dry_flags", "wet_cobbles", "gravel", "metal_deck"):
                c = Counter()
                for _ in range(n):
                    o, _x = approach(rng, light, surface, crouch)
                    c[o] += 1
                key = f"{light_name}|{'crouch' if crouch else 'walk'}|{surface}"
                rows[key] = {k: round(v / n, 3) for k, v in c.items()}
    methods = {}
    for m in ("choke", "cosh", "fist", "knife"):
        c = Counter()
        for _ in range(n * 2):
            o, _x = approach(rng, 0.25, "wet_cobbles", True, method=m)
            c[o] += 1
        methods[m] = {k: round(v / (n * 2), 3) for k, v in c.items()}
    methods["choke_held_past_knockout_death_chance"] = {f"{x} s": round(choke_death(x), 2) for x in (5, 15, 30, 60, 90, 120)}
    return rows, methods


# ---------------------------------------------------------------- the report
def pct(a, b):
    return round(100.0 * a / b, 1) if b else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=1990)
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    n = args.n
    results = {"seed": args.seed, "n_per_scenario": n, "scenarios": {}}
    scen = []
    kinds_all = ["boxer", "brawler", "big", "wiry"]
    for style in ("patient", "masher", "street", "menace", "runner"):
        scen.append((f"1v1 fists {style}", dict(style=style, weapon="fists", n_foes=1, kinds=kinds_all, place="open_street")))
        scen.append((f"2v1 fists {style}", dict(style=style, weapon="fists", n_foes=2, kinds=kinds_all, place="open_street")))
    scen += [
        ("3v1 fists patient", dict(style="patient", weapon="fists", n_foes=3, kinds=kinds_all, place="open_street")),
        ("2v2 with Ron patient", dict(style="patient", weapon="fists", n_foes=2, kinds=kinds_all, place="open_street", allies=1)),
        ("1v1 kerbside patient", dict(style="patient", weapon="fists", n_foes=1, kinds=kinds_all, place="kerbside")),
        ("1v1 vs knife man patient", dict(style="patient", weapon="fists", n_foes=1, kinds=["knife"], place="open_street")),
        ("1v1 Frank knife patient", dict(style="patient", weapon="knife", n_foes=1, kinds=kinds_all, place="open_street")),
        ("1v1 Frank cosh patient", dict(style="patient", weapon="cosh", n_foes=1, kinds=kinds_all, place="open_street")),
        ("1v1 Frank bat masher", dict(style="masher", weapon="bat", n_foes=1, kinds=kinds_all, place="open_street")),
        ("2v1 Frank knife patient", dict(style="patient", weapon="knife", n_foes=2, kinds=kinds_all, place="open_street")),
        ("1v1 menace with knife shown", dict(style="menace", weapon="knife", n_foes=1, kinds=kinds_all, place="open_street", menace=0.5)),
        ("1v1 fists, Frank finishes", dict(style="patient", weapon="fists", n_foes=1, kinds=kinds_all, place="kerbside", frank_finishes=True)),
        ("1v1 cosh, Frank finishes", dict(style="patient", weapon="cosh", n_foes=1, kinds=kinds_all, place="open_street", frank_finishes=True)),
        ("1v1 yard at night, nobody about", dict(style="patient", weapon="fists", n_foes=1, kinds=kinds_all, place="yard_night", public=False)),
    ]
    for name, kw in scen:
        res, dur, cons = run_fights(rng, n, **kw)
        d = sorted(dur)
        results["scenarios"][name] = {
            "frank_win_pct": pct(res["frank_win"], n),
            "frank_win_of_decided_pct": pct(res["frank_win"], res["frank_win"] + res["frank_lost"] + res["frank_escaped"]),
            "no_result_pct": pct(res["no_result"], n),
            "ended_by_timeout_pct": pct(res["ended_by_timeout"], n),
            "frank_lost_pct": pct(res["frank_lost"], n),
            "frank_escaped_pct": pct(res["frank_escaped"], n),
            "ended_by_threat_pct": pct(res["ended_by_threat"], n),
            "stepped_in_pct": pct(res["ended_by_stepped_in"], n),
            "police_arrived_pct": pct(res["ended_by_police"], n),
            "duration_median_s": round(statistics.median(d), 1) if d else None,
            "duration_p90_s": round(d[int(0.9 * (len(d) - 1))], 1) if d else None,
            "deaths_per_1000": round(1000.0 * res["death"] / n, 1),
            "fall_critical_per_1000": round(1000.0 * res["fall_critical"] / n, 1),
            "knockouts_per_fight": round(res["knockout"] / n, 2),
            "foe_yielded_per_fight": round(res["yielded"] / n, 2),
            "foe_begged_per_fight": round(res["begged"] / n, 2),
            "foe_fled_per_fight": round(res["fled"] / n, 2),
            "picked_up_per_fight": round(res["picked_up"] / n, 2),
            "surface_used_per_fight": round(res["surface_used"] / n, 2),
            "frank_hospital_pct": pct(res["frank_hospital"], n),
            "foe_worst": {k.split(":")[1]: v for k, v in res.items() if k.startswith("foe_worst:")},
            "consequences": dict(cons),
        }
    rows, methods = run_stealth(rng, n)
    results["stealth_approach"] = rows
    results["takedowns"] = methods
    results["threats"] = threat_table(rng)
    out = args.out or "results.json"
    with open(out, "w") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    # short print
    for name, r in results["scenarios"].items():
        print(f"{name:34s} win {r['frank_win_pct']:5.1f}% (of decided {r['frank_win_of_decided_pct']:5.1f}%)  lost {r['frank_lost_pct']:5.1f}%  ran {r['frank_escaped_pct']:4.1f}%  stopped {r['stepped_in_pct'] + r['police_arrived_pct']:4.1f}%  "
              f"med {r['duration_median_s']}s p90 {r['duration_p90_s']}s  deaths/1000 {r['deaths_per_1000']}")
    for k in ("doorway_dark|crouch|wet_cobbles", "unlit_street|walk|wet_cobbles", "unlit_street|crouch|wet_cobbles",
              "lamp|crouch|dry_flags", "day|walk|dry_flags", "unlit_street|crouch|gravel", "unlit_street|crouch|metal_deck"):
        print(k, rows[k])
    for m, r in methods.items():
        print("takedown", m, r)


if __name__ == "__main__":
    main()
