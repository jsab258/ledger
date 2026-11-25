#!/usr/bin/env python3
"""LEDGER combat and stealth simulator, revision 1 (seeded, repeatable).

Runs the general rules of COMBAT-SYSTEM.md on thousands of fights, takedowns,
shots and threats, and prints the headline numbers.

    python3 combat_sim.py              # seed 1990, n 2000, writes results.json
    python3 combat_sim.py --seed 7 --n 2000

Revision 1 (his pick A, 25 Nov, advisor 382): readable rules decide outcomes.
  * A blow lands, is blocked or is slipped by what the struck man is doing at
    that moment (guard up and facing, or mid-swing, or looking away); there is
    no hidden defence roll at landing. Where a man reacts (raises his guard on
    seeing a wind-up, chooses to press or run) that is his choice, drawn from
    his skill and temper, and it shows before the blow lands.
  * Blows land where they were aimed (the attacker's line); a guarded blow lands
    on the arms; a low kick on the legs. No zone dice table.
  * Knock-downs and knock-outs follow force and the man's visible state
    (wobbling from head blows, gasping) by thresholds, not by chance.
  * Stealth: a takedown works when the man is reached unseen; he turns only for
    a cause the player could notice (his routine glance, a footstep within his
    hearing, other eyes). A choke breaks only on a big, fresh man against a
    winded or hurt Frank; a disarm follows the grip and the moment.
  * Chance remains only at the violent end (a knife wound's depth, a fall of a
    spent man at a kerb, a critical wound's outcome, a gunshot, a held choke,
    boots on a head), and every such chance is fixed to the save: drawn from a
    hash of the save seed and the act, so a reload never rerolls it.

Every tuning value lives in TUNE, named as in COMBAT-SYSTEM.md.
"""
import argparse, hashlib, json, random, statistics
from collections import Counter, defaultdict

# ---------------------------------------------------------------- tuning
TUNE = {
    # CS-02 actions: wind-up s, recovery s, wind cost, force, line (the zone it is aimed at)
    "act": {
        "jab":    dict(wu=0.32, rec=0.25, wind=0.12, force=1.0, kind="blunt"),
        "heavy":  dict(wu=0.74, rec=0.50, wind=0.20, force=2.6, kind="blunt"),
        "kick":   dict(wu=0.55, rec=0.45, wind=0.10, force=1.7, kind="blunt"),
        "stamp":  dict(wu=0.60, rec=0.40, wind=0.09, force=1.3, kind="blunt"),   # boot on a downed man
        "grab":   dict(wu=0.45, rec=0.35, wind=0.08, force=0.0, kind="grab"),
        "shove_surface": dict(wu=0.50, rec=0.40, wind=0.10, force=2.0, kind="blunt"),
        "thrust": dict(wu=0.60, rec=0.35, wind=0.09, force=0.0, kind="edge"),
        "slash":  dict(wu=0.35, rec=0.35, wind=0.09, force=0.0, kind="edge"),
    },
    # CS-06 weapons as data
    "weapon": {
        "fists":  dict(mult=1.0, wu=0.0, kind="blunt", menace=0.0, breaks=None),
        "knuckleduster": dict(mult=1.35, wu=0.0, kind="blunt", menace=0.35, breaks=None),
        "cosh":   dict(mult=1.9, wu=0.10, kind="blunt", menace=0.45, breaks=None),
        "bat":    dict(mult=2.3, wu=0.25, kind="blunt", menace=0.55, breaks=None),
        "brick":  dict(mult=2.0, wu=0.15, kind="blunt", menace=0.40, breaks=3),
        "chair":  dict(mult=1.7, wu=0.30, kind="blunt", menace=0.30, breaks=2),
        "knife":  dict(mult=1.0, wu=0.0, kind="edge", menace=0.75, breaks=None),
        "revolver": dict(mult=1.0, wu=0.0, kind="gun", menace=1.0, breaks=None),
        "sawn_off": dict(mult=1.0, wu=0.0, kind="gun", menace=1.0, breaks=None),
    },
    # CS-05 the body
    "blunt_threshold": {"hurt": 3.0, "serious": 9.5, "critical": 15.0},
    "limb_serious": 6.0,             # blunt harm on one arm or leg that breaks it (a bat to the forearm, a boot to the knee)
    "fists_cap": "serious",          # his ruling of 30 Oct: fists never kill on their own
    "boots_can_kill": True,          # D2 yes (25 Nov)
    # edge wounds: (act, zone) -> (minor, serious, critical): the depth is the knife's one chance, fixed to the save
    "edge_wound": {
        ("thrust", "torso"): (0.40, 0.44, 0.16),
        ("thrust", "head"):  (0.30, 0.45, 0.25),   # face
        ("thrust", "neck"):  (0.10, 0.40, 0.50),
        ("thrust", "arms"):  (0.70, 0.27, 0.03),
        ("thrust", "legs"):  (0.62, 0.32, 0.06),   # 6%: the femoral artery
        ("slash", "torso"):  (0.72, 0.25, 0.03),
        ("slash", "head"):   (0.70, 0.28, 0.02),   # face: a slash leaves a scar
        ("slash", "neck"):   (0.35, 0.40, 0.25),
        ("slash", "arms"):   (0.85, 0.14, 0.01),
        ("slash", "legs"):   (0.80, 0.18, 0.02),
    },
    # guns (CS-23): by zone, (minor, serious, critical); the sawn-off by range band
    "gun_wound": {
        "revolver": {"arms": (0.15, 0.80, 0.05), "legs": (0.10, 0.80, 0.10), "torso": (0.0, 0.50, 0.50),
                      "head": (0.0, 0.15, 0.85), "neck": (0.0, 0.10, 0.90)},
        "sawn_off_close": {"arms": (0.0, 0.65, 0.35), "legs": (0.0, 0.60, 0.40), "torso": (0.0, 0.10, 0.90),
                            "head": (0.0, 0.0, 1.0), "neck": (0.0, 0.0, 1.0)},          # under 5 m: one mass
        "sawn_off_mid":   {"arms": (0.20, 0.70, 0.10), "legs": (0.20, 0.70, 0.10), "torso": (0.05, 0.60, 0.35),
                            "head": (0.0, 0.40, 0.60), "neck": (0.0, 0.40, 0.60)},      # 5 to 15 m: pellets spread
        "sawn_off_far":   {"arms": (0.80, 0.20, 0.0), "legs": (0.80, 0.20, 0.0), "torso": (0.70, 0.28, 0.02),
                            "head": (0.45, 0.45, 0.10), "neck": (0.45, 0.45, 0.10)},    # beyond 15 m: scattered pellets
    },
    "critical_death_untreated": 0.55, "critical_death_helped": 0.20,
    "gun_critical_death_untreated": 0.75, "gun_critical_death_helped": 0.35,
    # CS-04 wind and states
    "wind_regen": 0.12, "low_wind": 0.18, "pause": (0.3, 1.4), "npc_pause": (0.2, 0.9), "counter_window": 0.45, "counter_mult": 1.5,
    "capacity": {"frank": 12.0, "boxer": 15.0, "brawler": 14.0, "big": 21.0, "knife": 12.0, "wiry": 12.0, "constable": 14.0},
    # knock-down and knock-out by threshold (readable: a man wobbling from head blows, or gasping, goes down sooner)
    "kd_head_force": 3.4, "kd_torso_force": 5.0, "kd_head_soak": 6.0, "kd_low_wind_mult": 1.5,
    "ko_head_dmg": 8.0,
    "ko_seconds_fist": (10, 60), "ko_seconds_weapon": (30, 300),
    # CS-07 surfaces and the fall: a spent man knocked down at an edge (the violent end; fixed to the save)
    "fall_crit_spent": 1/50, "fall_serious_spent": 0.12, "unaware_mult": 1.5,
    # CS-09 temper in a fight
    "flee_will": 0.08, "yield_will": 0.20,
    # CS-14 public: step-in and police
    "stepin_per_5s": 0.025, "stepin_per_bystander": 1.10, "police_per_s_after_20": 1/150,
    # CS-08 disarm: the grip gives when the man is winded or hurt, his weapon arm is hurt, or he is caught mid-swing
    "disarm_wind": 0.40, "disarm_hurt": 0.40,
    # CS-13 choke
    "choke_s": {"small": 6.5, "middling": 7.5, "big": 10.0},
}

TYPES = {  # CS-11 fighter kinds: defence (how often he reads a wind-up and gets his guard up), aggression, nerve range
    "boxer":   dict(defence=0.55, aggr=0.55, nerve=(0.5, 0.8), weapon="fists", size="middling"),
    "brawler": dict(defence=0.28, aggr=0.85, nerve=(0.5, 0.85), weapon="fists", size="middling"),
    "big":     dict(defence=0.30, aggr=0.60, nerve=(0.55, 0.9), weapon="fists", size="big"),
    "knife":   dict(defence=0.40, aggr=0.45, nerve=(0.35, 0.7), weapon="knife", size="middling"),
    "wiry":    dict(defence=0.50, aggr=0.45, nerve=(0.2, 0.5), weapon="fists", size="small"),
}

FRANK_STYLES = {  # player styles the bots play; aim_high: share of blows aimed at the head
    "patient": dict(defence=0.68, heavy_share=0.30, surface=0.25, threat_first=False, run_at=None, aim_high=0.6, aim_arm=0.5),
    "masher":  dict(defence=0.22, heavy_share=0.60, surface=0.0, threat_first=False, run_at=None, aim_high=0.5),
    "street":  dict(defence=0.62, heavy_share=0.30, surface=0.70, threat_first=False, run_at=None, aim_high=0.6),
    "menace":  dict(defence=0.65, heavy_share=0.30, surface=0.30, threat_first=True, run_at=None, aim_high=0.6),
    "runner":  dict(defence=0.60, heavy_share=0.25, surface=0.10, threat_first=False, run_at=0.45, aim_high=0.6),
}

LEVELS = ["none", "bruise", "hurt", "serious", "critical", "dead"]


def fixed(save, *key):
    """A chance fixed to the save: the same save and the same act give the same number, so a reload never rerolls it."""
    h = hashlib.sha256(("|".join(str(k) for k in (save,) + key)).encode()).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64


class Man:
    def __init__(self, rng, name, side, kind, weapon="fists", defence=0.5, aggr=0.6, nerve=0.6,
                 style=None, is_frank=False, size="middling"):
        self.rng, self.name, self.side, self.kind, self.size = rng, name, side, kind, size
        self.weapon = weapon
        self.weapon_uses = 0
        self.defence, self.aggr, self.nerve = defence, aggr, nerve
        self.style = style or {}
        self.is_frank = is_frank
        self.wind = 1.0
        self.dmg = defaultdict(float)
        self.wounds = []
        self.condition = 0.0
        self.capacity = TUNE["capacity"]["frank" if is_frank else kind]
        self.heavies_taken = 0
        self.weapon_hits_taken = 0
        self.state = "fresh"
        self.busy_until = 0.0
        self.down_until = 0.0
        self.pending = None
        self.worst = "none"
        self.manner = set()
        self.counter_until = -1.0
        self.guard_until = -1.0
        self.open_until = -1.0      # mid-swing recovery: cannot guard
        self.focus = None           # the man he is facing
        self.was_out = False
        self.arm_out = False        # weapon arm hurt: drops what it holds, no heavy blow with it
        self.leg_out = False        # leg hurt: cannot run; can crawl
        self.face_mark = False      # a scar or mark witnesses remember
        self.acts = 0
        self.gun_wound = False

    def active(self):
        return self.state in ("fresh", "hurt")

    def standing(self):
        return self.state in ("fresh", "hurt", "beaten")

    def hurt_frac(self):
        return min(1.0, self.condition / self.capacity)

    def bump(self, level):
        if LEVELS.index(level) > LEVELS.index(self.worst):
            self.worst = level


def blunt_level(d, zone):
    t = TUNE["blunt_threshold"]
    if zone in ("arms", "legs"):
        return "serious" if d >= TUNE["limb_serious"] else ("hurt" if d >= t["hurt"] else ("bruise" if d > 0 else "none"))
    if d >= t["critical"] * (1.0 if zone in ("head", "neck") else 1.5):
        return "critical"
    if d >= t["serious"]:
        return "serious"
    if d >= t["hurt"]:
        return "hurt"
    return "bruise" if d > 0 else "none"


def wound_from(probs, u):
    return "minor" if u < probs[0] else ("serious" if u < probs[0] + probs[1] else "critical")


class Fight:
    def __init__(self, rng, frank_side, other_side, place, save=1990, fid="f", bystanders=6, public=True):
        self.rng, self.save, self.fid = rng, save, fid
        self.men = frank_side + other_side
        self.place = place
        self.t = 0.0
        self.first_blow = None
        self.log = Counter()
        self.bystanders, self.public = bystanders, public
        self.ended_by = None
        self.menace = 0.3

    def chance(self, m, what):
        m.acts += 1
        return fixed(self.save, self.fid, m.name, what, m.acts)

    def foes(self, m):
        return [o for o in self.men if o.side != m.side and o.standing() and o.state != "fled"]

    def downed_foes(self, m):
        return [o for o in self.men if o.side != m.side and o.state in ("down", "out")]

    # ---- CS-09 temper
    def will(self, m):
        allies = sum(1 for o in self.men if o.side == m.side and o is not m and o.active())
        foes = [o for o in self.men if o.side != m.side and o.active()]
        fear = max([TUNE["weapon"][f.weapon]["menace"] for f in foes] + [0.0])
        outnumber = max(0, len(foes) - allies - 1) * 0.12
        return (m.nerve * 0.9 + 0.12 * allies - 0.30 * fear - 0.45 * m.hurt_frac()
                - outnumber - (0.08 * self.menace if m.side != "F" else 0.0) - (0.1 if m.wounds else 0.0)
                - (0.1 if m.arm_out else 0.0))

    def decide(self, m):
        rng = self.rng
        if m.is_frank:
            st = m.style
            if st.get("run_at") and m.hurt_frac() >= st["run_at"] and rng.random() < 0.5 and not m.leg_out:
                return ("flee", None)
        if m.state == "beaten":
            if m.is_frank:
                return ("spent", None)
            if m.leg_out:
                return ("yield", None)      # a man who cannot run gives up or crawls
            return ("yield", None) if m.hurt_frac() >= 0.85 or rng.random() < 0.5 else ("flee", None)
        if not m.is_frank:
            w = self.will(m)
            if w < TUNE["flee_will"]:
                return ("flee", None) if (m.hurt_frac() < 0.85 and not m.leg_out) else ("yield", None)
            if w < TUNE["yield_will"] and m.hurt_frac() > 0.45:
                return ("yield", None)
            if m.state == "hurt" and m.weapon == "fists" and not m.arm_out and rng.random() < 0.02:
                return ("pickup", None)
        foes = self.foes(m)
        if not foes:
            if any(o.side != m.side and o.state == "down" for o in self.men):
                return ("guard", None)
            return ("done", self.downed_foes(m))
        target = min(foes, key=lambda o: (o.hurt_frac() if m.is_frank else 0) + rng.random() * 0.5)
        m.focus = target
        if not m.is_frank:
            swinging = sum(1 for o in self.men if o.pending and o.pending[2] is target and o is not m)
            if swinging >= 2:
                return ("circle", None)
            blade = TUNE["weapon"][target.weapon]["menace"] >= 0.45
            if blade and m.weapon == "fists" and rng.random() < 0.05:
                return ("pickup", None)
            if blade and rng.random() < 0.12 and m.wind > 0.3:
                return ("grab", target)
            if rng.random() > min(0.95, m.aggr * (0.45 if blade else 1.0)):
                return ("guard", None)
        if m.wind < TUNE["low_wind"]:
            return ("gasp", None)
        st = m.style if m.is_frank else {}
        surface_use = st.get("surface", 0) * 0.4 if m.is_frank else (0.10 if m.kind in ("brawler", "big") else 0.03)
        if self.place["surface"] and rng.random() < surface_use:
            return ("grab", target)
        if m.weapon == "knife":
            return ("thrust" if rng.random() < 0.5 else "slash", target)
        heavy_share = st.get("heavy_share", 0.35) if m.is_frank else (0.5 if m.kind in ("brawler", "big") else 0.3)
        if m.arm_out:
            heavy_share = 0.0
        if rng.random() < 0.10:
            return ("kick", target)    # a low kick (CS-02): to the legs
        if m.is_frank and m.style is FRANK_STYLES["patient"] and target.pending:
            return ("guard", None)
        return ("heavy" if rng.random() < heavy_share else "jab", target)

    def aim_line(self, att, act):
        """The attacker's line: his choice, shown in his shoulders. High is the head, low the body; a knife thrust goes to the body, a slash high."""
        rng = self.rng
        if act == "kick":
            return "legs"
        if act == "thrust":
            r = rng.random()
            return "torso" if r < 0.75 else ("neck" if r < 0.85 else "legs")
        if act == "slash":
            return "head" if rng.random() < 0.5 else ("arms" if rng.random() < 0.5 else "torso")
        if att.is_frank and att.focus is not None and att.focus.weapon != "fists" and att.weapon != "fists" and rng.random() < att.style.get("aim_arm", 0.0):
            return "arms"              # aimed at the weapon arm (CS-02: the stick held to his weapon side)
        high = att.style.get("aim_high", 0.55) if att.is_frank else 0.55
        return "head" if rng.random() < high else "torso"

    def react(self, tgt, att):
        """CS-03: a wind-up is readable 0.45 to 0.80 s ahead. A man facing it and not mid-swing may get his guard up; that is his choice, seen before the blow lands."""
        if tgt.state not in ("fresh", "hurt") or self.t < tgt.open_until or tgt.pending:
            return
        facing = tgt.focus is att or tgt.focus is None or len(self.foes(tgt)) == 1
        if not facing:
            return
        if tgt.wind < 0.2:
            return                          # emptied: his hands are down
        wu = TUNE["act"][att.pending[1]]["wu"] + TUNE["weapon"][att.weapon]["wu"] if att.pending else 0.0
        rt = 0.85 - 0.55 * tgt.defence + (0.15 if tgt.hurt_frac() > 0.4 else 0.0)   # his reaction time, fixed per man
        if rt <= wu:
            tgt.guard_until = max(tgt.guard_until, self.t + wu + 0.2)

    # ---- resolving a landed blow: by what the struck man is doing at that moment
    def land(self, att, act, tgt, unaware=False, counter=False, aim=None, finishing=False):
        T = TUNE
        if not tgt.standing() and act != "stamp" and not finishing:
            return
        w = T["weapon"][att.weapon]
        z = aim or self.aim_line(att, act)
        guarded = (not unaware and act != "stamp" and tgt.standing() and self.t < tgt.guard_until
                   and self.t >= tgt.open_until and not counter)
        if act in ("thrust", "slash"):
            if guarded:
                self.log["blocked"] += 1
                tgt.counter_until = self.t + T["counter_window"]
                if act == "slash":
                    self.edge_wound(tgt, "slash", "arms", att)   # a slash on the guarding forearm
                elif att.wind < 0.4 or self.t < att.open_until:
                    pass   # a tired thrust is turned aside
                else:
                    self.edge_wound(tgt, "thrust", "arms", att)  # a thrust into the guard goes through the forearm
                return
            self.edge_wound(tgt, act, z, att)
            tgt.manner.add("weapon")
            if unaware:
                tgt.manner.add("behind")
            att.wind -= 0.06
            return
        a = T["act"][act]
        force = a["force"] * w["mult"] * (0.5 + 0.5 * max(att.wind, 0)) * (T["unaware_mult"] if unaware else 1.0) * (T["counter_mult"] if counter else 1.0)
        if att.arm_out:
            force *= 0.6
        if act == "stamp":
            z = aim or "head"
            tgt.manner.add("downed")
            if tgt.state == "yielded":
                tgt.manner.add("yielded")
        if finishing:
            tgt.manner.add("downed")
        if guarded:
            self.log["blocked"] += 1
            tgt.counter_until = self.t + T["counter_window"]
            att.open_until = self.t + 0.3
            att.busy_until += 0.3
            tgt.wind -= 0.05 * force
            if not (act == "heavy" and att.weapon != "fists"):
                return
            z = "arms"; force *= 0.6       # a swung weapon breaks through onto the arm
        if act == "shove_surface":
            force = a["force"] * (0.5 + 0.5 * max(att.wind, 0))     # the wall is the weapon, not what is in his hand
        steady = 1.0 + tgt.dmg["head"] / T["kd_head_soak"]          # how steady he was before this blow
        if tgt.wind < 0.25:
            steady *= T["kd_low_wind_mult"]
        armed = att.weapon != "fists" and act != "shove_surface"
        if w["breaks"]:
            att.weapon_uses += 1
            if att.weapon_uses >= w["breaks"]:
                att.weapon = "fists"; self.log["thing_broke"] += 1
        if armed:
            tgt.weapon_hits_taken += 1
            tgt.manner.add("weapon")
        if act == "heavy":
            tgt.heavies_taken += 1
        tgt.dmg[z] += force * (1.25 if z == "head" else 1.0)
        tgt.condition += force * (1.1 if z == "head" else (0.5 if z in ("arms", "legs") else 0.9))
        tgt.wind -= 0.04 * force
        prev = tgt.worst
        lvl = blunt_level(tgt.dmg[z], z)
        if finishing and LEVELS.index(lvl) > LEVELS.index(prev) + 1:
            lvl = LEVELS[LEVELS.index(prev) + 1]   # one blow on a downed man raises the harm one level at most: each step shows
            tgt.dmg[z] = min(tgt.dmg[z], {"hurt": 9.4, "serious": 14.9}.get(lvl, tgt.dmg[z]))
        if (not armed) and act in ("jab", "heavy", "kick", "shove_surface"):
            if LEVELS.index(lvl) > LEVELS.index(T["fists_cap"]):
                lvl = T["fists_cap"]
        if act == "stamp" and not T["boots_can_kill"] and lvl == "critical":
            lvl = "serious"
        tgt.bump(lvl)
        if z in ("arms", "legs") and lvl == "serious":
            self.limb(tgt, z)
        if lvl == "critical":
            self.critical(tgt, cause="blunt_" + act)
            return
        self.log["landed_" + act] += 1
        # knock-down by threshold: the blow's force against how steady he is (head harm and wind show in his legs)
        eff = force * steady
        downs = (z == "head" and eff >= T["kd_head_force"]) or (z == "torso" and eff >= T["kd_torso_force"])
        if tgt.standing() and downs:
            self.knockdown(tgt, z, att, unaware)
        elif tgt.condition >= tgt.capacity and tgt.state != "beaten":
            tgt.state = "beaten"; self.log["beaten"] += 1
        elif tgt.condition >= tgt.capacity * 0.4 and tgt.state == "fresh":
            tgt.state = "hurt"

    def limb(self, tgt, z):
        if z == "arms" and not tgt.arm_out:
            tgt.arm_out = True; self.log["arm_out"] += 1
            if tgt.weapon != "fists":
                tgt.weapon = "fists"; self.log["dropped_weapon"] += 1
        if z == "legs" and not tgt.leg_out:
            tgt.leg_out = True; self.log["leg_out"] += 1

    def edge_wound(self, tgt, act, z, att):
        probs = TUNE["edge_wound"][(act, z)]
        lvl = wound_from(probs, self.chance(tgt, "edge"))
        tgt.wounds.append((z, lvl))
        tgt.condition += {"minor": 1.0, "serious": 3.5, "critical": 9.0}[lvl]
        self.log["stab_" + lvl] += 1
        if z == "head" and act == "slash":
            tgt.face_mark = True; self.log["face_mark"] += 1
        tgt.bump({"minor": "hurt", "serious": "serious", "critical": "critical"}[lvl])
        if lvl in ("serious", "critical"):
            if z in ("arms", "legs"):
                self.limb(tgt, z)
            if z == "head":
                tgt.face_mark = True
        if lvl == "critical":
            self.critical(tgt, cause="edge_" + act)
        elif lvl == "serious" and z in ("torso", "neck"):
            if tgt.state in ("fresh", "hurt"):
                tgt.state = "down"; tgt.down_until = self.t + 4.0; self.log["dropped_by_stab"] += 1
        elif tgt.condition >= tgt.capacity:
            tgt.state = "beaten"
        elif tgt.state == "fresh":
            tgt.state = "hurt"

    def critical(self, tgt, cause):
        self.log["critical_" + cause] += 1
        if tgt.is_frank:
            tgt.state = "out"; self.log["frank_hospital"] += 1
            return
        tgt.state = "dying"

    def knockdown(self, tgt, z, att, unaware=False):
        T = TUNE
        self.log["knockdown"] += 1
        tgt.state = "down"
        tgt.down_until = self.t + 2.0 + 3.0 * tgt.hurt_frac()
        spent = tgt.heavies_taken >= 3 or tgt.weapon_hits_taken >= 1   # RT2-12: the visible "spent" man
        if spent and self.chance(tgt, "edge_pos") < self.place["near_edge"]:   # where he falls (no geometry here: fixed to the save)
            u = self.chance(tgt, "fall")
            if u < T["fall_crit_spent"]:
                tgt.bump("critical"); self.log["fall_critical"] += 1
                if tgt.is_frank:
                    tgt.state = "out"; self.log["frank_hospital"] += 1; return
                tgt.state = "dying"; return
            if u < T["fall_serious_spent"]:
                tgt.dmg["head"] += 4; tgt.bump("serious"); self.log["fall_serious"] += 1
        weapon_blow = att.weapon not in ("fists", "knuckleduster")
        if z == "head" and (tgt.dmg["head"] >= T["ko_head_dmg"] or (unaware and att.weapon != "fists")):
            tgt.state = "out"; tgt.was_out = True; self.log["knockout"] += 1
            lo, hi = T["ko_seconds_weapon"] if weapon_blow else T["ko_seconds_fist"]
            tgt.down_until = self.t + lo + (hi - lo) * min(1.0, tgt.dmg["head"] / 15.0)

    def try_grab(self, m, tgt):
        """CS-08: a grab works unless he is guarding and facing (he slips it). The weapon arm comes free by the grip and the moment."""
        if not tgt.standing():
            return
        if self.t < tgt.guard_until and self.t >= tgt.open_until and tgt.focus is m:
            self.log["grab_slipped"] += 1
            return
        self.log["grab"] += 1
        if tgt.weapon != "fists":
            loose = (tgt.wind < TUNE["disarm_wind"] or tgt.hurt_frac() >= TUNE["disarm_hurt"]
                     or tgt.arm_out or self.t < tgt.open_until)
            if loose:
                self.log["disarmed" + ("_frank" if tgt.is_frank else "")] += 1
                tgt.weapon = "fists"; m.busy_until = self.t + 0.6
            else:
                self.log["disarm_held"] += 1     # a firm grip: a struggle for the arm, then a shove
                tgt.wind -= 0.15; m.wind -= 0.10
            return
        if self.place["surface"]:
            self.log["surface_used"] += 1
            m.pending = (self.t + 0.5, "shove_surface", tgt, False); m.busy_until = self.t + 0.9

    # ---- main loop
    def run(self, max_t=150.0, dt=0.1, frank_finishes=False):
        rng = self.rng
        while self.t < max_t:
            self.t += dt
            for m in self.men:
                if m.state in ("dead", "dying", "fled", "yielded"):
                    continue
                if m.state == "down" and self.t >= m.down_until:
                    m.state = "beaten" if m.condition >= m.capacity else "hurt"
                if m.state == "out":
                    continue
                if m.pending and self.t >= m.pending[0]:
                    _, act, tgt, ctr = m.pending
                    m.pending = None
                    m.open_until = self.t + 0.3       # just swung: open for about 0.3 s
                    if act == "grab":
                        self.try_grab(m, tgt)
                        continue
                    if self.first_blow is None:
                        self.first_blow = self.t
                    self.land(m, act, tgt, counter=ctr)
                if not m.pending and (self.t >= m.busy_until or self.t < m.guard_until):
                    m.wind = min(1.0 - 0.4 * m.hurt_frac(), m.wind + TUNE["wind_regen"] * dt * (2.0 if self.t < m.guard_until else 1.0))
                if self.t < m.busy_until or m.state == "down":
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
                a = TUNE["act"][choice]
                wu = a["wu"] + TUNE["weapon"][m.weapon]["wu"]
                if m.wind < TUNE["low_wind"]:
                    wu *= 1.3
                m.wind -= a["wind"]
                ctr = self.t <= m.counter_until and rng.random() < m.defence   # he takes the opening if he saw it
                if ctr:
                    wu *= 0.6; self.log["counter" + ("_frank" if m.is_frank else "")] += 1
                m.pending = (self.t + wu, choice, tgt, ctr)
                if not ctr and tgt is not None:
                    self.react(tgt, m)
                pause = 0 if ctr else rng.uniform(*(TUNE["pause"] if m.is_frank else TUNE["npc_pause"])) * (0.4 if (m.is_frank and m.style.get("heavy_share", 0) > 0.5) else 1.0)
                m.busy_until = self.t + wu + a["rec"] + pause
                if pause and (m.defence > 0.5 or rng.random() < m.defence):
                    m.guard_until = m.busy_until
            if self.public and self.first_blow is not None:
                if int(round(self.t * 10)) % 50 == 0:
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
        frank = next((m for m in self.men if m.is_frank), None)
        if frank_finishes and frank and frank.standing():
            for d in downed:
                for _ in range(3):           # the quiet decision: up to three blows on the downed man (CS-14)
                    if frank_finishes == "heed" and d.worst in ("serious", "critical"):
                        self.log["stopped_at_cue"] += 1
                        break                # the cue: he stops moving his arms; "He's not moving. Again?" and the player stops
                    self.land(frank, "stamp" if frank.weapon == "fists" else "heavy", d, aim="head", finishing=True)
                    if d.state in ("dying", "dead"):
                        break
        for m in self.men:
            if m.state == "dying":
                helped = self.public and self.chance(m, "helped") < 0.55
                gun = m.gun_wound
                p = (TUNE["gun_critical_death_helped"] if helped else TUNE["gun_critical_death_untreated"]) if gun else \
                    (TUNE["critical_death_helped"] if helped else TUNE["critical_death_untreated"])
                if self.chance(m, "dying") < p:
                    m.state = "dead"; m.bump("dead"); self.log["death"] += 1
                else:
                    m.state = "out"; self.log["survived_critical"] += 1
        if not self.ended_by:
            self.ended_by = "decided"
        return self


# ---------------------------------------------------------------- consequences (CS-16 to CS-19)
CHARGE = {"none": None, "bruise": "common assault", "hurt": "ABH (s.47)", "serious": "GBH or wounding (s.20)",
          "critical": "GBH with intent (s.18)", "dead": "manslaughter"}


def consequences(rng, fight):
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
        sev = LEVELS.index(m.worst) / 5
        factor = 1.0
        for k, f in (("behind", 1.3), ("downed", 1.5), ("yielded", 1.6), ("weapon", 1.4)):
            if k in m.manner:
                factor *= f
        reading = min(1.0, sev * factor)
        out["reading_band:" + ("grave" if reading >= 0.8 else "bad" if reading >= 0.45 else "talked of")] += 1
        if m.face_mark:
            out["face_marked"] += 1
        if m.state == "dead":
            out["body"] += 1
            continue
        grudge, law = rng.random(), rng.random()
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
               aggr=t["aggr"], nerve=rng.uniform(*t["nerve"]), size=t["size"])


PLACES = {
    "open_street": dict(near_edge=0.15, surface=True),
    "kerbside":    dict(near_edge=0.45, surface=True),
    "yard_night":  dict(near_edge=0.25, surface=True),
}


def threat_first(rng, frank, foes, menace):
    """CS-10: a threat folds a man whose nerve plus pride is under its weight. The rng stands for each man's hidden nerve, which the player reads in his face."""
    threat = 0.5 + 0.4 * TUNE["weapon"][frank.weapon]["menace"]
    folded = 0
    for f in foes:
        eff = f.nerve + 0.15 * (len(foes) - 1) + rng.uniform(0.0, 0.25)
        if eff < threat * (0.8 + 0.4 * menace):
            folded += 1
    return folded == len(foes)


def run_fights(rng, n, save, scen, style, weapon, n_foes, kinds, place, menace=0.3, allies=0, frank_finishes=False,
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
        f = Fight(rng, fside, foes, PLACES[place], save=save, fid=f"{scen}#{i}", public=public, bystanders=rng.randint(0, 12))
        f.menace = menace
        f.run(frank_finishes=frank_finishes)
        res.update(f.log)
        for x in foes:
            res["foe_arm_out"] += x.arm_out; res["foe_leg_out"] += x.leg_out; res["foe_face_mark"] += x.face_mark
        res["frank_arm_out"] += frank.arm_out; res["frank_face_mark"] += frank.face_mark
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
            res["no_result"] += 1
        if f.first_blow is not None:
            durations.append(f.t - f.first_blow)
        cons.update(consequences(rng, f))
        for x in foes:
            res["foe_worst:" + x.worst] += 1
        res["frank_worst:" + frank.worst] += 1
    return res, durations, cons


# ---------------------------------------------------------------- stealth (CS-12, CS-13), revision 1: readable causes only
SURFACE_NOISE = {"dry_flags": 1.0, "wet_cobbles": 1.25, "gravel": 1.7, "metal_deck": 2.1}
LIGHTS = {"doorway_dark": 0.12, "unlit_street": 0.25, "lamp": 0.7, "day": 1.0}


TD_REACH = 1.5


def sight_reach(light, crouch, moving):
    """Metres within which a watcher looking this way picks the figure out (spotted), and twice that a shape (uneasy)."""
    r = (2.0 + 22.0 * light) * (1.0 if moving else 0.5)
    if crouch and light < 0.5:
        r *= 0.6
    return r


def hear_reach(surface, crouch, slow, rain):
    return 3.6 * SURFACE_NOISE[surface] * (0.5 if crouch else 1.0) * (0.6 if slow else 1.0) * (0.5 if rain else 1.0)


def approach(scene, play, method="choke", frank_wind=1.0, frank_hurt=False, save=1990, key="a"):
    """Approach from scene['start'] metres behind an unaware man and take him. Deterministic for a scene and a play.
    scene: light, surface, rain, glance_every (s, his routine), glance_len, glance_phase, watcher_at (m from the man, or None),
           kind (his build), shadow (whether there is dark to freeze in)
    play: 'careful' (crouches; slow on loud ground; freezes while he glances; before closing in waits for a glance to end
          and goes only if he can reach him before the next; holds back if he cannot), 'crouch' (crouches, ignores his
          glances), 'walk' (walks straight in). Takedown reach: 1.5 m (a step and the grab, 0.45 s)."""
    light, surface, rain = scene["light"], scene["surface"], scene["rain"]
    crouch = play in ("careful", "crouch")
    slow = play == "careful" and hear_reach(surface, True, False, rain) > TD_REACH
    speed = (1.2 if crouch else 1.6) * (0.5 if slow else 1.0)
    dist, t, dt = scene["start"], 0.0, 0.05
    uneasy_at = None
    committed = play != "careful"
    waited = 0.0
    while dist > TD_REACH:
        t += dt
        phase = (t + scene["glance_phase"]) % scene["glance_every"]
        glancing = phase < scene["glance_len"]
        moving = True
        if play == "careful":
            if glancing:
                moving = False
            elif not committed:
                danger = max(sight_reach(light, True, True), hear_reach(surface, True, slow, rain)) + 1.0
                if dist - speed * dt <= danger:
                    left = scene["glance_every"] - phase          # seconds until his next glance
                    need = (dist - TD_REACH) / speed + 0.45
                    if need < left:
                        committed = True
                    else:
                        moving = False; waited += dt
                        if waited > 3 * scene["glance_every"]:
                            return "held_back", t                 # he can see it cannot be done from here
        if moving:
            dist -= speed * dt
        if glancing or (uneasy_at is not None and t >= uneasy_at):
            reach = sight_reach(light, crouch, moving)
            if play == "careful" and not moving and not scene["shadow"] and light >= 0.5:
                reach = sight_reach(light, crouch, True) * 0.7
            if dist <= reach:
                return ("spotted" if glancing else "heard_turned"), t   # turned to a sound he heard, then saw him
        if moving and uneasy_at is None and dist <= hear_reach(surface, crouch, slow, rain):
            uneasy_at = t + 0.8
        if scene["watcher_at"] is not None and scene["watcher_at"] <= sight_reach(light, crouch, moving) * 0.8:
            return "seen_by_other", t
    # reached: the man turns only if a heard step gave him time
    if uneasy_at is not None and t + 0.45 >= uneasy_at:
        return "heard_turned", t
    if method == "choke":
        size = scene["kind"]
        if size == "big" and (frank_wind < 0.6 or frank_hurt):
            return "broke_free", t       # a big, fresh man against a winded or hurt Frank: readable before he tries
        return "out", t + TUNE["choke_s"][size]
    frank = Man(random.Random(0), "Frank", "F", "frank", weapon={"cosh": "cosh", "fist": "fists", "knife": "knife"}[method],
                defence=0.6, is_frank=True)
    kind = {"small": "wiry", "middling": "boxer", "big": "big"}[scene["kind"]]
    tgt = make_foe(random.Random(0), kind, 0)
    tgt.name = key
    f = Fight(random.Random(0), [frank], [tgt], dict(near_edge=0.0, surface=True), save=save, fid=key, public=False)
    if method == "knife":
        f.land(frank, "thrust", tgt, unaware=True, aim="torso")
    elif method == "fist":
        f.land(frank, "heavy", tgt, unaware=True, aim="head")
    else:
        f.land(frank, "heavy", tgt, unaware=True, aim="head")
    if tgt.state == "dying":
        dead = fixed(save, key, "dying") < TUNE["critical_death_untreated"]
        return ("dead" if dead else "critical_survived"), t
    if tgt.state == "out":
        return ("out_serious" if tgt.worst == "serious" else "out"), t
    if tgt.state == "down":
        return ("dropped_serious" if tgt.worst == "serious" else "knocked_down"), t
    return ("wounded" if method == "knife" else "staggered"), t


def random_scene(rng, light=None, surface=None):
    return dict(light=LIGHTS[light] if light else rng.choice(list(LIGHTS.values())),
                surface=surface or rng.choice(list(SURFACE_NOISE)), rain=rng.random() < 0.3,
                glance_every=rng.uniform(6, 20), glance_len=rng.uniform(1.0, 2.0), glance_phase=rng.uniform(0, 20),
                watcher_at=None if rng.random() < 0.8 else rng.uniform(5, 25),
                kind=rng.choice(["small", "middling", "middling", "big"]), shadow=rng.random() < 0.7, start=12.0)


def choke_death(extra_s):
    """D1: chance of death when a choke is held on extra_s seconds past the knock-out; the body goes still at 20 s."""
    return max(0.0, min(0.95, (extra_s - 40) / 100.0))


def run_stealth(rng, n, save):
    rows = {}
    for lname in LIGHTS:
        for play in ("walk", "crouch", "careful"):
            for surface in ("dry_flags", "wet_cobbles", "gravel", "metal_deck"):
                c = Counter()
                for i in range(n):
                    sc = random_scene(rng, lname, surface)
                    sc["watcher_at"] = None
                    o, _ = approach(sc, play, save=save, key=f"st{lname}{play}{surface}{i}")
                    c[o] += 1
                rows[f"{lname}|{play}|{surface}"] = {k: round(v / n, 3) for k, v in c.items()}
    methods = {}
    for meth in ("choke", "cosh", "fist", "knife"):
        for play in ("careful", "crouch"):
            c = Counter()
            for i in range(n):
                sc = random_scene(rng, "unlit_street", "wet_cobbles")
                o, _ = approach(sc, play, method=meth, save=save, key=f"td{meth}{play}{i}")
                c[o] += 1
            methods[f"{meth}|{play}"] = {k: round(v / n, 3) for k, v in c.items()}
    # the choke on a big man: Frank fresh against Frank winded
    for fw, lab in ((1.0, "fresh"), (0.5, "winded")):
        sc = random_scene(random.Random(1), "doorway_dark", "dry_flags"); sc.update(kind="big", watcher_at=None, glance_every=30, glance_phase=10)
        methods[f"choke on a big man, Frank {lab}"] = approach(sc, "careful", frank_wind=fw)[0]
    methods["choke_held_past_knockout_death_chance"] = {f"{x} s": round(choke_death(x), 2) for x in (5, 15, 30, 60, 90, 120, 135)}
    for x in (30, 60, 90):
        d = sum(fixed(save, "held_choke", x, i) < choke_death(x) for i in range(n))
        methods[f"choke held {x} s past the knock-out, drawn from the save"] = {"dead": round(d / n, 3)}
    # a correct play must never fail: careful, in shadow, quiet ground, no watcher, reached before any glance
    fails = Counter()
    for i in range(n):
        sc = random_scene(rng); sc.update(shadow=True, watcher_at=None)
        if sc["light"] >= 0.5:
            continue
        o, _ = approach(sc, "careful", save=save, key=f"cp{i}")
        fails[o] += 1
    tot = sum(fails.values())
    methods["careful_in_the_dark_any_surface"] = {k: round(v / tot, 3) for k, v in fails.items()}
    return rows, methods


# ---------------------------------------------------------------- guns (CS-23), revision 1
def gun_hit(rng, gun, rng_m, aimed, moving, steady):
    """Where the shot goes: the aimed zone if the aim holds; else the next zone in, else a miss. Aim holds by range,
    the zone's size, Frank moving and his wind (sway shows on screen). A player's aim, simulated as a bot's error."""
    size = {"torso": 1.0, "head": 0.45, "neck": 0.25, "arms": 0.35, "legs": 0.5}[aimed]
    spread = (0.04 + 0.025 * rng_m) * (1.8 if moving else 1.0) * (1.4 if not steady else 1.0)
    if gun == "sawn_off":
        spread *= 0.5   # the pattern covers for aim
    err = abs(rng.gauss(0, spread))
    if err < 0.3 * size:
        return aimed
    if err < 0.4:
        return "torso" if aimed != "torso" else ("arms" if rng.random() < 0.5 else "legs")
    return None


def gun_table(rng, n, save):
    out = {}
    for gun, ranges in (("revolver", (3, 8, 15)), ("sawn_off", (3, 10, 20))):
        for r in ranges:
            for aimed in ("arms", "legs", "torso", "head"):
                c = Counter()
                for i in range(n):
                    z = gun_hit(rng, gun, r, aimed, moving=False, steady=True)
                    if z is None:
                        c["miss"] += 1; continue
                    key = gun if gun == "revolver" else ("sawn_off_close" if r < 5 else "sawn_off_mid" if r <= 15 else "sawn_off_far")
                    lvl = wound_from(TUNE["gun_wound"][key][z], fixed(save, gun, r, aimed, i, "wound"))
                    c["hit_" + z] += 1
                    if z == "arms" and lvl != "minor":
                        c["dropped_weapon"] += 1
                    if z == "legs" and lvl != "minor":
                        c["cannot_run"] += 1
                    if lvl in ("serious", "critical") and z in ("torso", "head", "neck"):
                        c["went_down"] += 1
                    if lvl == "critical":
                        helped = rng.random() < 0.55
                        p = TUNE["gun_critical_death_helped"] if helped else TUNE["gun_critical_death_untreated"]
                        c["dead" if fixed(save, gun, r, aimed, i, "dying") < p else "critical_survived"] += 1
                    elif lvl == "serious":
                        c["serious"] += 1
                    else:
                        c["minor"] += 1
                out[f"{gun} {r} m aimed {aimed}"] = {k: round(v / n, 3) for k, v in sorted(c.items())}
    return out


def knife_zone_table(save, n=4000):
    out = {}
    for (act, z), probs in TUNE["edge_wound"].items():
        c = Counter(wound_from(probs, fixed(save, "kz", act, z, i)) for i in range(n))
        out[f"{act} {z}"] = {k: round(v / n, 3) for k, v in sorted(c.items())}
    return out


def threat_table(rng, n=4000):
    out = {}
    for menace in (0.3, 0.5, 0.8):
        for weapon in ("fists", "cosh", "knife", "revolver"):
            for nf in (1, 2):
                ok = 0
                for _ in range(n):
                    fr = make_frank(rng, "menace", weapon)
                    foes = [make_foe(rng, rng.choice(["boxer", "brawler", "big", "wiry"]), j) for j in range(nf)]
                    ok += threat_first(rng, fr, foes, menace)
                out[f"menace {menace} | {weapon} | {nf} man"] = round(ok / n, 3)
    return out


def reload_check(save):
    """A reload never rerolls: the same act on the same man from the same save gives the same wound, fall and outcome,
    even when everything else in the session (the random stream) differs."""
    outs = []
    for stream in (11, 999):
        rows = []
        for i in range(200):
            rng = random.Random(stream * 1000 + i)
            fr = make_frank(rng, "patient", "knife"); foe = make_foe(rng, "boxer", 0); foe.name = f"r{i}"
            f = Fight(rng, [fr], [foe], dict(near_edge=1.0, surface=True), save=save, fid=f"reload{i}", public=True)
            f.land(fr, "thrust", foe, aim="torso", unaware=True)
            f.finish([], False)
            rows.append((foe.wounds[-1][1] if foe.wounds else None, foe.state))
        outs.append(rows)
    other = []
    for i in range(200):
        rng = random.Random(i)
        fr = make_frank(rng, "patient", "knife"); foe = make_foe(rng, "boxer", 0); foe.name = f"r{i}"
        f = Fight(rng, [fr], [foe], dict(near_edge=1.0, surface=True), save=save + 1, fid=f"reload{i}", public=True)
        f.land(fr, "thrust", foe, aim="torso", unaware=True); f.finish([], False)
        other.append((foe.wounds[-1][1] if foe.wounds else None, foe.state))
    return {"same_save_different_streams_identical": outs[0] == outs[1],
            "a_different_save_differs": other != outs[0], "acts": 200}


def pct(a, b):
    return round(100.0 * a / b, 1) if b else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=1990)
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    n, save = args.n, args.seed
    results = {"seed": args.seed, "n_per_scenario": n, "revision": 1, "scenarios": {}}
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
        ("1v1 Frank bat vs knife man patient", dict(style="patient", weapon="bat", n_foes=1, kinds=["knife"], place="open_street")),
        ("1v1 Frank bat masher", dict(style="masher", weapon="bat", n_foes=1, kinds=kinds_all, place="open_street")),
        ("2v1 Frank knife patient", dict(style="patient", weapon="knife", n_foes=2, kinds=kinds_all, place="open_street")),
        ("1v1 menace with knife shown", dict(style="menace", weapon="knife", n_foes=1, kinds=kinds_all, place="open_street", menace=0.5)),
        ("1v1 fists, Frank finishes", dict(style="patient", weapon="fists", n_foes=1, kinds=kinds_all, place="kerbside", frank_finishes=True)),
        ("1v1 cosh, Frank finishes", dict(style="patient", weapon="cosh", n_foes=1, kinds=kinds_all, place="open_street", frank_finishes=True)),
        ("1v1 fists, Frank finishes but heeds the cue", dict(style="patient", weapon="fists", n_foes=1, kinds=kinds_all, place="kerbside", frank_finishes="heed")),
        ("1v1 cosh, Frank finishes but heeds the cue", dict(style="patient", weapon="cosh", n_foes=1, kinds=kinds_all, place="open_street", frank_finishes="heed")),
        ("1v1 yard at night, nobody about", dict(style="patient", weapon="fists", n_foes=1, kinds=kinds_all, place="yard_night", public=False)),
    ]
    for name, kw in scen:
        res, dur, cons = run_fights(rng, n, save, name, **kw)
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
            "knockdowns_per_fight": round(res["knockdown"] / n, 2),
            "foe_yielded_per_fight": round(res["yielded"] / n, 2),
            "foe_begged_per_fight": round(res["begged"] / n, 2),
            "foe_fled_per_fight": round(res["fled"] / n, 2),
            "disarms_per_fight": round((res["disarmed"] + res["disarmed_frank"]) / n, 3),
            "disarm_held_per_fight": round(res["disarm_held"] / n, 3),
            "foe_arm_out_pct": pct(res["foe_arm_out"], n),
            "foe_leg_out_pct": pct(res["foe_leg_out"], n),
            "foe_face_marked_pct": pct(res["foe_face_mark"], n),
            "frank_arm_out_pct": pct(res["frank_arm_out"], n),
            "frank_face_marked_pct": pct(res["frank_face_mark"], n),
            "dropped_weapon_per_fight": round(res["dropped_weapon"] / n, 3),
            "frank_hospital_pct": pct(res["frank_hospital"], n),
            "foe_worst": {k.split(":")[1]: v for k, v in res.items() if k.startswith("foe_worst:")},
            "consequences": dict(cons),
        }
    rows, methods = run_stealth(rng, n, save)
    results["stealth_approach"] = rows
    results["takedowns"] = methods
    results["guns"] = gun_table(rng, n, save)
    results["knife_by_zone"] = knife_zone_table(save)
    results["threats"] = threat_table(rng)
    results["reload_check"] = reload_check(save)
    out = args.out or "results.json"
    with open(out, "w") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    for name, r in results["scenarios"].items():
        print(f"{name:34s} win {r['frank_win_pct']:5.1f}% (of decided {r['frank_win_of_decided_pct']:5.1f}%)  lost {r['frank_lost_pct']:5.1f}%  ran {r['frank_escaped_pct']:4.1f}%  stopped {r['stepped_in_pct'] + r['police_arrived_pct']:4.1f}%  "
              f"med {r['duration_median_s']}s p90 {r['duration_p90_s']}s  deaths/1000 {r['deaths_per_1000']}")
    for k in ("doorway_dark|careful|wet_cobbles", "doorway_dark|crouch|wet_cobbles", "unlit_street|walk|wet_cobbles",
              "unlit_street|crouch|wet_cobbles", "unlit_street|careful|wet_cobbles", "lamp|careful|dry_flags",
              "lamp|crouch|dry_flags", "day|walk|dry_flags", "day|careful|dry_flags", "unlit_street|careful|metal_deck"):
        print(k, rows[k])
    for m, r in methods.items():
        print("takedown", m, r)
    for k in ("revolver 3 m aimed arms", "revolver 8 m aimed legs", "revolver 8 m aimed torso", "sawn_off 3 m aimed torso",
              "sawn_off 10 m aimed torso", "sawn_off 20 m aimed torso"):
        print("gun", k, results["guns"][k])
    print("reload", results["reload_check"])


if __name__ == "__main__":
    main()
