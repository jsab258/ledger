"""Melee feel drills: definitions, telemetry format, scorer and pass/fail.

Written 18 Nov 2026 for production/research/lane/FEEL-TARGETS-MELEE-2026-11-18.md.
Pure Python (standard library only). The same drills run unchanged against the
browser feel study now and the Unreal game later: each game plays the scripted
drill, writes the telemetry log below, and this tool turns the log into the
sheet's numbers (C1 to C15) and a pass or fail for each.

Behaviour carries over, never raw settings: nothing here reads a game's tuning
values, only the timed events a game reports.

Telemetry format (one JSON object per line, "JSON lines"):
    {"t": 1.234, "ev": "hit_contact", "actor": "player", "target": "dummy", ...}
  t      seconds of real (wall-clock) time since the drill started
  ev     one of EVENTS below
  actor  who did it ("player", "dummy", "a1", "a2", "camera", "audio")
  other fields as listed per event in EVENTS.

Times are real time. Hit-stop freezes the game but not the clock, so the
scorer subtracts hit-stop from recovery (recovery means time the attacker is
busy after contact, not counting the freeze).
"""

import json
import math

# --------------------------------------------------------------------------
# Events
# --------------------------------------------------------------------------

EVENTS = {
    "input": "a button press; fields: action (jab, hook, heavy, swing, block, dodge, shove), stick_deg optional",
    "hit_start": "the attack's animation starts moving; fields: action, weapon",
    "active_start": "the blow can now connect",
    "active_end": "the blow can no longer connect",
    "hit_contact": "the blow lands; fields: target, action, weapon",
    "miss": "the blow ended without landing",
    "hitstop_start": "hit-stop (the brief freeze on contact) begins",
    "hitstop_end": "hit-stop ends",
    "recovery_end": "the attacker can act again",
    "stagger_start": "a hit reaction starts; fields: severity (light, heavy)",
    "stagger_end": "the hit reaction ends and the man can act",
    "telegraph_start": "an attacker's wind-up becomes readable; fields: action",
    "attack_start": "an enemy commits to an attack (holds an attack token)",
    "attack_end": "that enemy attack is over (token returned)",
    "guard_up": "the guard is fully raised",
    "block": "a blow was stopped by the guard; fields: target",
    "dodge_start": "the dodge moves the body",
    "invuln_start": "blows can no longer land on the dodger",
    "invuln_end": "blows can land again",
    "dodge_end": "the dodger can act again",
    "knockdown": "a man is on the ground but conscious",
    "ko": "a man is knocked out; fields: cause (fists, weapon)",
    "getup_start": "a man starts getting up",
    "getup": "a man is on his feet and can act",
    "fall_hazard": "a fall against a kerb, wall or step after a blow; fields: surface",
    "death": "a man dies; fields: cause",
    "stamina": "stamina reading 0 to 1; fields: value",
    "stamina_empty": "stamina reached zero",
    "weapon_break": "an improvised weapon broke; fields: weapon",
    "warp_start": "the attacker starts closing the gap to his target; fields: dist (m)",
    "warp_end": "closing ends; fields: dist (m)",
    "target_pick": "a target was chosen; fields: picked, expected",
    "camera": "camera sample; fields: dist, height, shake_deg, both_visible, feet_visible, occluded",
    "close_in_start": "the brief camera close-in on contact starts",
    "close_in_end": "the camera is back at the fight distance",
    "sound": "a sound starts; fields: kind (whoosh, impact, pain, shout)",
}

STRIKES = ("jab", "hook", "heavy", "swing")

# --------------------------------------------------------------------------
# Targets: (low, high, source). None means shown but not failing.
# Sources: see the sheet's section (c). "est." marks an estimate.
# --------------------------------------------------------------------------

TARGETS = {
    # C1 input to motion
    "jab_input_to_motion_s": (0.0, 0.10, "latency surveys; est."),
    "hook_input_to_motion_s": (0.0, 0.10, "latency surveys; est."),
    "heavy_input_to_motion_s": (0.0, 0.10, "latency surveys; est."),
    "swing_input_to_motion_s": (0.0, 0.10, "latency surveys; est."),
    # C2 startup (motion to contact), active, recovery after contact, after a miss
    "jab_startup_s": (0.25, 0.40, "real jab 0.36 s whole; Mafia window from 0.27 s; est."),
    "jab_active_s": (0.03, 0.10, "est."),
    "jab_recovery_s": (0.20, 0.40, "est."),
    "hook_startup_s": (0.45, 0.75, "real hook 0.48 s whole; KCD2 hooks 0.70 s"),
    "hook_active_s": (0.05, 0.15, "est."),
    "hook_recovery_s": (0.35, 0.50, "KCD2 about 0.4 s"),
    "heavy_startup_s": (0.63, 0.85, "KCD2 0.63 to 0.80, LEDGER B01 0.73"),
    "heavy_active_s": (0.05, 0.17, "KCD2 swing live 0.17 s before contact"),
    "heavy_recovery_s": (0.35, 0.50, "KCD2 0.4; Study 14 item 2"),
    "heavy_miss_recovery_s": (0.70, 0.90, "Study 14 item 2, judgement"),
    "swing_startup_s": (0.80, 1.05, "KCD2 blunt 0.93 s"),
    "swing_active_s": (0.08, 0.20, "est."),
    "swing_recovery_s": (0.50, 0.80, "est."),
    # C3 hit-stop
    "jab_hitstop_s": (0.025, 0.05, "est.; LEDGER now 2 frames"),
    "hook_hitstop_s": (0.04, 0.08, "est."),
    "heavy_hitstop_s": (0.06, 0.12, "est."),
    "swing_hitstop_s": (0.07, 0.13, "est."),
    # C4 hit reactions on the man struck
    "light_stagger_s": (0.50, 0.70, "KCD2 weak class 0.6; LEDGER D03"),
    "heavy_stagger_s": (0.90, 1.30, "Mafia 1.06, KCD2 unarmed 1.18; LEDGER D04"),
    # C5 block
    "telegraph_lead_s": (0.45, 0.80, "above choice reaction time plus lag; est."),
    "guard_raise_s": (0.0, 0.15, "est."),
    "blocked": (1, 1, "drill must succeed"),
    # C6 dodge
    "dodge_input_to_motion_s": (0.0, 0.10, "est."),
    "dodge_invuln_s": (0.20, 0.35, "est."),
    "dodge_total_s": (0.50, 0.80, "est."),
    "evaded": (1, 1, "drill must succeed"),
    # C7 knockdown, knock-out, getting up
    "down_time_s": (1.5, 3.0, "est."),
    "getup_s": (1.0, 2.0, "est."),
    "ko_time_s": (10.0, 30.0, "KCD2 quest knock-out 10 s; est. upper"),
    "fist_rule_violations": (0, 0, "his ruling of 30 Oct: fists never kill on their own"),
    # C8 attackers at once
    "max_simultaneous_attackers": (1, 2, "design: two against one is deadly; est."),
    "min_attack_start_gap_s": (0.40, None, "LEDGER half-gap offset; est."),
    "max_attacker_idle_s": (None, 2.5, "KCD2 at most 2 s between a man's blows, widened"),
    # C9 closing in and target choice (no lock-on)
    "warp_time_s": (0.40, 0.55, "Mafia 0.42 to 0.52 s"),
    "warp_end_dist_m": (0.9, 1.1, "Mafia 1 m off"),
    "warp_start_max_dist_m": (None, 2.0, "Mafia at most 2 m"),
    "target_pick_correct_pct": (100.0, 100.0, "scripted cases must all pick right"),
    # C10 camera
    "cam_dist_m": (3.5, 5.0, "his 28 Oct wider fight camera; est."),
    "both_visible_pct": (95.0, 100.0, "est."),
    "feet_visible_pct": (90.0, 100.0, "his 28 Oct pick: the other man's feet seen"),
    "occluded_frames": (0, 0, "no camera inside a wall"),
    "close_in_hold_s": (0.6, 1.0, "Mafia melee camera 0.8 s"),
    "shake_peak_deg": (0.3, 1.5, "est.; obeys Reduce motion"),
    "shake_settle_s": (0.0, 0.30, "est."),
    # C11 stamina
    "jabs_to_empty": (6, 10, "est.; mashing tires you out"),
    "heavies_to_empty": (3, 4, "LEDGER 0.34 a swing gives 3; KCD2 about 4"),
    "regen_full_s": (4.0, 8.0, "KCD2 about 4.5 s; LEDGER now 11 s; est."),
    # C12 improvised weapons
    "chair_hits_to_break": (1, 3, "est."),
    "brick_hits_to_break": (2, 5, "est."),
    "pipe_hits_to_break": (20, None, "a pipe does not break in a fight; est."),
    # C13 sound
    "whoosh_offset_s": (-0.05, 0.10, "est."),
    "impact_sync_s": (0.0, 0.034, "within one frame at 30 fps; est."),
    "pain_delay_s": (0.05, 0.30, "est."),
    "shout_lead_s": (0.40, None, "KCD2 combat shouts as telegraphs; est."),
    # C14 combo
    "combo_hits_landed": (3, 3, "all three buffered inputs land"),
    "combo_total_s": (1.5, 2.4, "est.; recovery cancelled into the next blow"),
    # C15 blows to put a man down
    "blows_to_knockdown": (3, 6, "LEDGER Combat.cs 4; est. band"),
}

# --------------------------------------------------------------------------
# Drills
# --------------------------------------------------------------------------

DRILLS = {
    "M1_jab": {
        "setup": "Player and a standing dummy 1.0 m apart, face to face, open street.",
        "script": "At t=1.0 s press jab once. Wait 3 s.",
        "gives": ["jab_*", "light_stagger_s", "impact_sync_s", "whoosh_offset_s", "pain_delay_s"],
    },
    "M1_hook": {
        "setup": "As M1_jab.",
        "script": "At t=1.0 s press hook once. Wait 3 s.",
        "gives": ["hook_*"],
    },
    "M1_heavy": {
        "setup": "As M1_jab; then repeated with the dummy 3 m away so the blow misses.",
        "script": "At t=1.0 s press heavy once. Wait 3 s.",
        "gives": ["heavy_*", "heavy_stagger_s", "heavy_miss_recovery_s (miss run)"],
    },
    "M2_combo": {
        "setup": "As M1_jab.",
        "script": "Press jab at 1.00 s, jab at 1.30 s, hook at 1.60 s (inputs arrive early on purpose to test buffering).",
        "gives": ["combo_hits_landed", "combo_total_s"],
    },
    "M3_block": {
        "setup": "Player faces one attacker 1.5 m away who throws one heavy at t=1.0 s.",
        "script": "Press block 0.30 s after telegraph_start (a fast human's choice reaction).",
        "gives": ["telegraph_lead_s", "guard_raise_s", "blocked", "shout_lead_s"],
    },
    "M4_dodge": {
        "setup": "As M3_block.",
        "script": "Press dodge 0.30 s after telegraph_start, stick away from the attacker.",
        "gives": ["dodge_input_to_motion_s", "dodge_invuln_s", "dodge_total_s", "evaded"],
    },
    "M5_knockdown": {
        "setup": "A fresh opponent who does not block, 1.0 m away, open ground, no kerb within 3 m.",
        "script": "Press heavy each time the player can act, until a knockdown or knock-out; then wait 40 s.",
        "gives": ["blows_to_knockdown", "down_time_s", "getup_s", "ko_time_s", "fist_rule_violations"],
    },
    "M5k_kerb": {
        "setup": "As M5 but with the opponent's back to a kerb 0.5 m behind him; fists only; run 200 times with seeds 1 to 200.",
        "script": "As M5.",
        "gives": ["fist_rule_violations (a death only through fall_hazard)"],
    },
    "M6_two_attackers": {
        "setup": "Player stands still, guard down; two attackers a1 and a2 start 3 m away on either side.",
        "script": "No input for 20 s.",
        "gives": ["max_simultaneous_attackers", "min_attack_start_gap_s", "max_attacker_idle_s"],
    },
    "M7_breakage": {
        "setup": "Player holds the improvised weapon (chair, brick or pipe) 1.0 m from a standing dummy that never falls.",
        "script": "Press swing each time the player can act, until weapon_break or 25 hits.",
        "gives": ["swing_*", "<weapon>_hits_to_break"],
    },
    "M8_camera_narrow": {
        "setup": "A street 2.5 m wide between walls; player and one opponent trade blows along it for 10 s; then across it.",
        "script": "Alternate jab and hook each time the player can act; the opponent does the same.",
        "gives": ["cam_dist_m", "both_visible_pct", "feet_visible_pct", "occluded_frames",
                  "close_in_hold_s", "shake_peak_deg", "shake_settle_s"],
    },
    "M9_stamina": {
        "setup": "Player 1.0 m from a dummy, full stamina.",
        "script": "Press jab each time the player can act until stamina_empty; idle until stamina is full; repeat with heavy.",
        "gives": ["jabs_to_empty", "heavies_to_empty", "regen_full_s"],
    },
    "M10_targets": {
        "setup": "Two dummies 1.8 m away at 30 degrees left and 30 degrees right.",
        "script": "Six cases: stick at -40, -20, -5, 5, 20, 40 degrees, then heavy. The expected target is the dummy nearer the stick.",
        "gives": ["target_pick_correct_pct", "warp_time_s", "warp_end_dist_m", "warp_start_max_dist_m"],
    },
}

# --------------------------------------------------------------------------
# Reading and writing logs
# --------------------------------------------------------------------------


def write_log(path, events):
    with open(path, "w", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e, sort_keys=True) + "\n")


def read_log(path):
    out = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            check_event(e, n)
            out.append(e)
    return sorted(out, key=lambda e: e["t"])


def check_event(e, n=0):
    if "t" not in e or "ev" not in e:
        raise ValueError(f"line {n}: every event needs t and ev")
    if e["ev"] not in EVENTS:
        raise ValueError(f"line {n}: unknown event {e['ev']!r}")
    if not isinstance(e["t"], (int, float)) or e["t"] < 0:
        raise ValueError(f"line {n}: t must be a number of seconds, 0 or more")


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------


def _first(events, ev, after=-1.0, actor=None, **match):
    for e in events:
        if e["t"] < after or e["ev"] != ev:
            continue
        if actor is not None and e.get("actor") != actor:
            continue
        if all(e.get(k) == v for k, v in match.items()):
            return e
    return None


def _all(events, ev, actor=None, **match):
    return [e for e in events if e["ev"] == ev
            and (actor is None or e.get("actor") == actor)
            and all(e.get(k) == v for k, v in match.items())]


def _r(v):
    return None if v is None else round(v, 4)


# --------------------------------------------------------------------------
# Scorers: each takes a sorted event list and returns {metric: value}
# --------------------------------------------------------------------------


def score_strike(events, actor="player"):
    """First strike by actor: input lag, startup, active, recovery, hit-stop, the
    victim's stagger, sound sync. Works for jab, hook, heavy and swing."""
    inp = next((e for e in events if e["ev"] == "input" and e.get("actor") == actor
                and e.get("action") in STRIKES), None)
    if inp is None:
        return {}
    a = inp["action"]
    out = {}
    hs = _first(events, "hit_start", inp["t"], actor)
    if hs is None:
        return out
    out[f"{a}_input_to_motion_s"] = hs["t"] - inp["t"]
    contact = _first(events, "hit_contact", hs["t"], actor)
    miss = _first(events, "miss", hs["t"], actor)
    a0 = _first(events, "active_start", hs["t"], actor)
    a1 = _first(events, "active_end", hs["t"], actor)
    if a0 and a1:
        out[f"{a}_active_s"] = a1["t"] - a0["t"]
    rec = _first(events, "recovery_end", hs["t"], actor)
    if contact and (miss is None or contact["t"] < miss["t"]):
        out[f"{a}_startup_s"] = contact["t"] - hs["t"]
        h0 = _first(events, "hitstop_start", contact["t"] - 1e-9)
        h1 = _first(events, "hitstop_end", contact["t"] - 1e-9)
        stop = (h1["t"] - h0["t"]) if (h0 and h1) else 0.0
        if h0 and h1:
            out[f"{a}_hitstop_s"] = stop
        if rec:
            out[f"{a}_recovery_s"] = rec["t"] - contact["t"] - stop
        s0 = _first(events, "stagger_start", contact["t"] - 1e-9, contact.get("target"))
        if s0:
            s1 = _first(events, "stagger_end", s0["t"], s0.get("actor"))
            if s1:
                out[f"{s0.get('severity', 'light')}_stagger_s"] = s1["t"] - s0["t"]
        imp = _first(events, "sound", contact["t"] - 0.2, "audio", kind="impact")
        if imp:
            out["impact_sync_s"] = abs(imp["t"] - contact["t"])
        pain = _first(events, "sound", contact["t"], "audio", kind="pain")
        if pain:
            out["pain_delay_s"] = pain["t"] - contact["t"]
    elif miss and rec:
        out[f"{a}_miss_recovery_s"] = rec["t"] - miss["t"]
    wh = _first(events, "sound", hs["t"] - 0.2, "audio", kind="whoosh")
    if wh:
        out["whoosh_offset_s"] = wh["t"] - hs["t"]
    return out


def score_combo(events, actor="player"):
    inputs = [e for e in events if e["ev"] == "input" and e.get("actor") == actor
              and e.get("action") in STRIKES]
    if not inputs:
        return {}
    hits = [e for e in _all(events, "hit_contact", actor) if e["t"] >= inputs[0]["t"]]
    recs = _all(events, "recovery_end", actor)
    out = {"combo_hits_landed": len(hits)}
    if recs:
        out["combo_total_s"] = recs[-1]["t"] - inputs[0]["t"]
    return out


def score_block(events, player="player"):
    tel = _first(events, "telegraph_start")
    if tel is None:
        return {}
    attacker = tel.get("actor")
    out = {}
    land = _first(events, "block", tel["t"], attacker) or _first(events, "hit_contact", tel["t"], attacker)
    if land:
        out["telegraph_lead_s"] = land["t"] - tel["t"]
    inp = _first(events, "input", tel["t"], player, action="block")
    gu = _first(events, "guard_up", tel["t"], player)
    if inp and gu:
        out["guard_raise_s"] = gu["t"] - inp["t"]
    out["blocked"] = 1 if _first(events, "block", tel["t"], attacker) else 0
    shout = _first(events, "sound", tel["t"] - 1.0, "audio", kind="shout")
    if shout and land:
        out["shout_lead_s"] = land["t"] - shout["t"]
    return out


def score_dodge(events, player="player"):
    tel = _first(events, "telegraph_start")
    inp = _first(events, "input", 0, player, action="dodge")
    if inp is None:
        return {}
    out = {}
    ds = _first(events, "dodge_start", inp["t"], player)
    de = _first(events, "dodge_end", inp["t"], player)
    i0 = _first(events, "invuln_start", inp["t"], player)
    i1 = _first(events, "invuln_end", inp["t"], player)
    if ds:
        out["dodge_input_to_motion_s"] = ds["t"] - inp["t"]
    if i0 and i1:
        out["dodge_invuln_s"] = i1["t"] - i0["t"]
    if ds and de:
        out["dodge_total_s"] = de["t"] - ds["t"]
    if tel:
        hit_on_player = [e for e in _all(events, "hit_contact", tel.get("actor"))
                         if e.get("target") == player and e["t"] >= tel["t"]]
        out["evaded"] = 0 if hit_on_player else 1
    return out


def score_knockdown(events, victim=None):
    out = {}
    down = next((e for e in events if e["ev"] in ("knockdown", "ko")
                 and (victim is None or e.get("actor") == victim)), None)
    if down is None:
        out["fist_rule_violations"] = fist_rule_violations(events)
        return out
    v = down.get("actor")
    out["blows_to_knockdown"] = len([e for e in events if e["ev"] == "hit_contact"
                                     and e.get("target") == v and e["t"] <= down["t"]])
    gs = _first(events, "getup_start", down["t"], v)
    g = _first(events, "getup", down["t"], v)
    if gs:
        key = "ko_time_s" if down["ev"] == "ko" else "down_time_s"
        out[key] = gs["t"] - down["t"]
    if gs and g:
        out["getup_s"] = g["t"] - gs["t"]
    out["fist_rule_violations"] = fist_rule_violations(events)
    return out


def fist_rule_violations(events, protagonist="player", hazard_window_s=3.0):
    """His ruling of 30 Oct: fists knock a man out and never kill on their own; a
    fall against a kerb, wall or step after a blow can kill. And Tom cannot die.
    Counts deaths that break this: any death of the player; any death in a fight
    where only fists were used, unless the victim had a fall_hazard within
    hazard_window_s after a blow landed on him and before he died."""
    bad = 0
    weapons = {e.get("weapon", "fists") for e in events
               if e["ev"] in ("hit_contact", "hit_start")}
    fists_only = weapons <= {"fists", None}
    for d in _all(events, "death"):
        v = d.get("actor")
        if v == protagonist:
            bad += 1
            continue
        if not fists_only:
            continue
        hits = [e for e in events if e["ev"] == "hit_contact" and e.get("target") == v
                and e["t"] <= d["t"]]
        falls = [e for e in _all(events, "fall_hazard", v) if e["t"] <= d["t"]]
        ok = any(0 <= f["t"] - h["t"] <= hazard_window_s for f in falls for h in hits)
        if not ok or d.get("cause") not in ("fall", None):
            bad += 1
    return bad


def score_attackers(events, player="player"):
    starts = sorted((e for e in _all(events, "attack_start") if e.get("actor") != player),
                    key=lambda e: e["t"])
    if not starts:
        return {}
    ends = _all(events, "attack_end")
    spans = []
    for s in starts:
        e = _first(ends, "attack_end", s["t"], s.get("actor"))
        spans.append((s["t"], e["t"] if e else math.inf, s.get("actor")))
    edges = sorted([(a, 1) for a, _, _ in spans] + [(b, -1) for _, b, _ in spans if b != math.inf],
                   key=lambda x: (x[0], x[1]))
    cur = peak = 0
    for _, d in edges:
        cur += d
        peak = max(peak, cur)
    out = {"max_simultaneous_attackers": peak}
    gaps = [b["t"] - a["t"] for a, b in zip(starts, starts[1:]) if a.get("actor") != b.get("actor")]
    if gaps:
        out["min_attack_start_gap_s"] = min(gaps)
    idle = []
    for who in {s.get("actor") for s in starts}:
        mine = [sp for sp in spans if sp[2] == who]
        for (a0, b0, _), (a1, _, _) in zip(mine, mine[1:]):
            idle.append(a1 - b0)
    if idle:
        out["max_attacker_idle_s"] = max(idle)
    return out


def score_breakage(events, actor="player"):
    out = score_strike(events, actor)
    br = _first(events, "weapon_break", 0, actor)
    swings = [e for e in _all(events, "hit_contact", actor) if e.get("weapon") not in (None, "fists")]
    weapon = (br or (swings[0] if swings else {})).get("weapon")
    if weapon:
        cut = br["t"] if br else math.inf
        out[f"{weapon}_hits_to_break"] = len([e for e in swings if e["t"] <= cut])
    return out


def score_camera(events):
    cams = _all(events, "camera")
    if not cams:
        return {}
    dists = sorted(c["dist"] for c in cams if "dist" in c)
    out = {
        "both_visible_pct": 100.0 * sum(1 for c in cams if c.get("both_visible")) / len(cams),
        "feet_visible_pct": 100.0 * sum(1 for c in cams if c.get("feet_visible")) / len(cams),
        "occluded_frames": sum(1 for c in cams if c.get("occluded")),
        "shake_peak_deg": max(c.get("shake_deg", 0.0) for c in cams),
    }
    if dists:
        out["cam_dist_m"] = dists[len(dists) // 2]
    holds = []
    for c0 in _all(events, "close_in_start"):
        c1 = _first(events, "close_in_end", c0["t"])
        if c1:
            holds.append(c1["t"] - c0["t"])
    if holds:
        out["close_in_hold_s"] = max(holds)
    settles = []
    for h in _all(events, "hit_contact"):
        later = [c for c in cams if c["t"] >= h["t"]]
        peak_seen = False
        for c in later:
            if c.get("shake_deg", 0) > 0.05:
                peak_seen = True
            elif peak_seen:
                settles.append(c["t"] - h["t"])
                break
    if settles:
        out["shake_settle_s"] = max(settles)
    return out


def score_stamina(events, actor="player"):
    out = {}
    empties = _all(events, "stamina_empty", actor)
    t0 = 0.0
    for emp in empties:
        starts = [e for e in _all(events, "hit_start", actor) if t0 <= e["t"] <= emp["t"]]
        if starts:
            kind = starts[0].get("action")
            if kind in ("jab", "heavy"):
                out[("jabs" if kind == "jab" else "heavies") + "_to_empty"] = len(starts)
        full = next((e for e in _all(events, "stamina", actor)
                     if e["t"] > emp["t"] and e.get("value", 0) >= 0.99), None)
        if full:
            out["regen_full_s"] = max(out.get("regen_full_s", 0.0), full["t"] - emp["t"])
            t0 = full["t"]
    return out


def score_targets(events, actor="player"):
    picks = _all(events, "target_pick", actor)
    out = {}
    if picks:
        out["target_pick_correct_pct"] = 100.0 * sum(
            1 for p in picks if p.get("picked") == p.get("expected")) / len(picks)
    times, ends, starts = [], [], []
    for w0 in _all(events, "warp_start", actor):
        w1 = _first(events, "warp_end", w0["t"], actor)
        if w1:
            times.append(w1["t"] - w0["t"])
            ends.append(w1.get("dist"))
            starts.append(w0.get("dist"))
    if times:
        out["warp_time_s"] = max(times)
        out["warp_end_dist_m"] = max(ends)
        out["warp_start_max_dist_m"] = max(starts)
    return out


SCORERS = {
    "M1_jab": score_strike, "M1_hook": score_strike, "M1_heavy": score_strike,
    "M2_combo": score_combo, "M3_block": score_block, "M4_dodge": score_dodge,
    "M5_knockdown": score_knockdown, "M5k_kerb": score_knockdown,
    "M6_two_attackers": score_attackers, "M7_breakage": score_breakage,
    "M8_camera_narrow": score_camera, "M9_stamina": score_stamina,
    "M10_targets": score_targets,
}


def score_drill(drill, events):
    events = sorted(events, key=lambda e: e["t"])
    for n, e in enumerate(events, 1):
        check_event(e, n)
    return {k: _r(v) for k, v in SCORERS[drill](events).items()}


def score_runs(runs):
    """runs: {drill_name: [events]} or {drill_name: [[events], [events]]} for
    repeated runs (e.g. M5k_kerb seeds, M1_heavy hit and miss). Repeated runs
    are merged: counts of rule breaks are summed, other numbers take the worst
    (furthest from the band middle is not known here, so the last run wins
    except for counts)."""
    result = {}
    for drill, logs in runs.items():
        if logs and isinstance(logs[0], dict):
            logs = [logs]
        for log in logs:
            for k, v in score_drill(drill, log).items():
                if k in ("fist_rule_violations", "occluded_frames") and k in result:
                    result[k] += v
                else:
                    result[k] = v
    return result


# --------------------------------------------------------------------------
# Pass and fail
# --------------------------------------------------------------------------


def compare_targets(result, targets=None):
    """Each number against its band, edges included. Returns rows of
    (metric, value, low, high, verdict) with verdict PASS, FAIL or NO BAND.
    A band the run did not produce is MISSING (a fail)."""
    targets = TARGETS if targets is None else targets
    rows = []
    for k in sorted(set(result) | set(targets)):
        v = result.get(k)
        if k not in targets:
            rows.append((k, v, None, None, "NO BAND"))
            continue
        lo, hi, _src = targets[k]
        if v is None:
            rows.append((k, None, lo, hi, "MISSING"))
            continue
        ok = (lo is None or v >= lo - 1e-9) and (hi is None or v <= hi + 1e-9)
        rows.append((k, v, lo, hi, "PASS" if ok else "FAIL"))
    return rows


def failures(rows, only_measured=True):
    return [r for r in rows if r[4] == "FAIL" or (r[4] == "MISSING" and not only_measured)]


ABS_TOL = {"_s": 0.034, "_m": 0.1, "_deg": 0.2, "_pct": 2.0}


def compare_results(result, reference, rel=0.05):
    """Unreal against the browser: within 5% or a fixed allowance by unit,
    whichever is larger (one frame at 30 fps for times). Counts must match
    exactly. A number one side gives and the other does not is a fail."""
    rows = []
    for k in sorted(set(result) | set(reference)):
        a, b = result.get(k), reference.get(k)
        if a is None or b is None:
            rows.append((k, a, b, "FAIL"))
            continue
        tol = next((t for suf, t in ABS_TOL.items() if k.endswith(suf)), 0.0)
        tol = max(tol, abs(b) * rel) if tol else 0.0
        rows.append((k, a, b, "PASS" if abs(a - b) <= tol + 1e-9 else "FAIL"))
    return rows


# --------------------------------------------------------------------------
# A reference fighter, only to test the tool. It writes logs the way a game
# would, from a timing profile. It proves the measuring, not how LEDGER's
# fighting should be built.
# --------------------------------------------------------------------------

REFERENCE_PROFILE = {
    "lag": 0.05,
    "jab": (0.32, 0.06, 0.30, 0.035),     # startup, active, recovery, hit-stop
    "hook": (0.60, 0.10, 0.42, 0.06),
    "heavy": (0.73, 0.12, 0.40, 0.09),
    "swing": (0.93, 0.14, 0.65, 0.10),
    "miss_recovery": 0.80,
    "stagger": {"jab": ("light", 0.60), "hook": ("light", 0.62),
                "heavy": ("heavy", 1.10), "swing": ("heavy", 1.20)},
    "telegraph_lead": 0.60, "guard_raise": 0.10,
    "dodge": (0.05, 0.28, 0.65),            # lag, invulnerable, total
    "blows_to_down": 4, "down_time": 2.2, "getup": 1.4, "ko_time": 12.0,
    "attack_len": 1.2, "attack_gap": 0.6, "idle": 1.6,
    "warp": (1.8, 1.0, 0.48),               # start dist, end dist, time
    "cam": (4.2, 0.8, 0.8),                 # dist, shake peak, close-in hold
    "stamina_cost": {"jab": 0.125, "heavy": 0.30}, "regen_s": 6.0,
    "breaks": {"chair": 2, "brick": 3, "pipe": None},
}


def _strike_events(t, action, p, target="dummy", weapon="fists", land=True, actor="player"):
    su, act, rec, stop = p[action]
    ev = [{"t": t, "ev": "input", "actor": actor, "action": action}]
    hs = t + p["lag"]
    ev.append({"t": hs, "ev": "hit_start", "actor": actor, "action": action, "weapon": weapon})
    ev.append({"t": hs - 0.0, "ev": "sound", "actor": "audio", "kind": "whoosh"})
    c = hs + su
    ev.append({"t": c - act / 2, "ev": "active_start", "actor": actor})
    ev.append({"t": c + act / 2, "ev": "active_end", "actor": actor})
    if land:
        ev.append({"t": c, "ev": "hit_contact", "actor": actor, "target": target,
                   "action": action, "weapon": weapon})
        ev.append({"t": c, "ev": "hitstop_start", "actor": actor})
        ev.append({"t": c + stop, "ev": "hitstop_end", "actor": actor})
        ev.append({"t": c + 0.01, "ev": "sound", "actor": "audio", "kind": "impact"})
        ev.append({"t": c + 0.12, "ev": "sound", "actor": "audio", "kind": "pain"})
        sev, dur = p["stagger"][action]
        ev.append({"t": c, "ev": "stagger_start", "actor": target, "severity": sev})
        ev.append({"t": c + dur, "ev": "stagger_end", "actor": target})
        end = c + stop + rec
    else:
        ev.append({"t": c + act / 2, "ev": "miss", "actor": actor})
        end = c + act / 2 + p["miss_recovery"]
    ev.append({"t": end, "ev": "recovery_end", "actor": actor})
    return ev, end


def simulate(drill, profile=None, **kw):
    p = dict(REFERENCE_PROFILE)
    p.update(profile or {})
    ev = []
    if drill in ("M1_jab", "M1_hook", "M1_heavy"):
        action = drill.split("_")[1]
        e, _ = _strike_events(1.0, action, p, land=kw.get("land", True))
        ev += e
    elif drill == "M2_combo":
        t = 1.0
        for i, a in enumerate(("jab", "jab", "hook")):
            e, end = _strike_events(t, a, p)
            ev += e
            if i < 2:
                # buffered and cancelled: the next blow starts 0.10 s after
                # the hit-stop ends, cutting this blow's recovery short
                su, _act, rec, stop = p[a]
                end = end - rec + 0.10
                ev[-1]["t"] = end
            t = end
    elif drill in ("M3_block", "M4_dodge"):
        tel = 1.0
        land = tel + p["telegraph_lead"]
        ev.append({"t": tel - 0.1, "ev": "sound", "actor": "audio", "kind": "shout"})
        ev.append({"t": tel, "ev": "telegraph_start", "actor": "a1", "action": "heavy"})
        ev.append({"t": tel, "ev": "attack_start", "actor": "a1"})
        r = tel + 0.30
        if drill == "M3_block":
            ev.append({"t": r, "ev": "input", "actor": "player", "action": "block"})
            ev.append({"t": r + p["guard_raise"], "ev": "guard_up", "actor": "player"})
            ev.append({"t": land, "ev": "block", "actor": "a1", "target": "player"})
        else:
            lag, inv, tot = p["dodge"]
            ev.append({"t": r, "ev": "input", "actor": "player", "action": "dodge"})
            ev.append({"t": r + lag, "ev": "dodge_start", "actor": "player"})
            ev.append({"t": r + lag + 0.02, "ev": "invuln_start", "actor": "player"})
            ev.append({"t": r + lag + 0.02 + inv, "ev": "invuln_end", "actor": "player"})
            ev.append({"t": r + lag + tot, "ev": "dodge_end", "actor": "player"})
            ev.append({"t": land, "ev": "miss", "actor": "a1"})
        ev.append({"t": land + 0.5, "ev": "attack_end", "actor": "a1"})
    elif drill in ("M5_knockdown", "M5k_kerb"):
        t = 1.0
        for i in range(p["blows_to_down"]):
            e, t = _strike_events(t, "heavy", p, target="opp")
            ev += e
        kind = "ko" if kw.get("ko", True) else "knockdown"
        down = t - 0.3
        ev.append({"t": down, "ev": kind, "actor": "opp", "cause": "fists"})
        wait = p["ko_time"] if kind == "ko" else p["down_time"]
        if kw.get("death"):
            if kw.get("hazard", True):
                ev.append({"t": down + 0.2, "ev": "fall_hazard", "actor": "opp", "surface": "kerb"})
            ev.append({"t": down + 0.4, "ev": "death", "actor": "opp", "cause": "fall"})
        else:
            ev.append({"t": down + wait, "ev": "getup_start", "actor": "opp"})
            ev.append({"t": down + wait + p["getup"], "ev": "getup", "actor": "opp"})
    elif drill == "M6_two_attackers":
        t, who = 1.0, ["a1", "a2"]
        n = 0
        while t < 20.0:
            a = who[n % 2]
            ev.append({"t": t, "ev": "attack_start", "actor": a})
            ev.append({"t": t + p["attack_len"], "ev": "attack_end", "actor": a})
            t += p["attack_gap"] if n % 2 == 0 else (p["attack_len"] + p["idle"] - p["attack_gap"])
            n += 1
    elif drill == "M7_breakage":
        w = kw.get("weapon", "chair")
        limit = p["breaks"][w]
        t = 1.0
        for i in range(25):
            e, t = _strike_events(t, "swing", p, weapon=w)
            ev += e
            if limit is not None and i + 1 == limit:
                ev.append({"t": t - 0.4, "ev": "weapon_break", "actor": "player", "weapon": w})
                break
    elif drill == "M8_camera_narrow":
        dist, shake, hold = p["cam"]
        contacts = [1.5, 4.0, 6.5]
        for c in contacts:
            ev.append({"t": c, "ev": "hit_contact", "actor": "player", "target": "opp"})
            ev.append({"t": c, "ev": "close_in_start", "actor": "camera"})
            ev.append({"t": c + hold, "ev": "close_in_end", "actor": "camera"})
        for i in range(300):
            t = i / 30.0
            s = 0.0
            for c in contacts:
                if 0 <= t - c < 0.2:
                    s = shake * (1 - (t - c) / 0.2)
            ev.append({"t": round(t, 4), "ev": "camera", "actor": "camera", "dist": dist,
                       "height": 1.7, "shake_deg": s, "both_visible": True,
                       "feet_visible": True, "occluded": False})
    elif drill == "M9_stamina":
        t = 1.0
        for action in ("jab", "heavy"):
            st = 1.0
            while st > 1e-9:
                e, t = _strike_events(t, action, p)
                ev += e
                st = max(0.0, st - p["stamina_cost"][action])
                ev.append({"t": t, "ev": "stamina", "actor": "player", "value": round(st, 4)})
            ev.append({"t": t, "ev": "stamina_empty", "actor": "player"})
            t += p["regen_s"]
            ev.append({"t": t, "ev": "stamina", "actor": "player", "value": 1.0})
            t += 0.5
    elif drill == "M10_targets":
        sd, ed, wt = p["warp"]
        t = 1.0
        for stick in (-40, -20, -5, 5, 20, 40):
            want = "left" if stick < 0 else "right"
            picked = kw.get("wrong_pick") if kw.get("wrong_pick") and stick == 5 else want
            ev.append({"t": t, "ev": "input", "actor": "player", "action": "heavy", "stick_deg": stick})
            ev.append({"t": t + 0.01, "ev": "target_pick", "actor": "player",
                       "picked": picked, "expected": want})
            ev.append({"t": t + 0.02, "ev": "warp_start", "actor": "player", "dist": sd})
            ev.append({"t": t + 0.02 + wt, "ev": "warp_end", "actor": "player", "dist": ed})
            t += 3.0
    else:
        raise KeyError(drill)
    return sorted(ev, key=lambda e: e["t"])


def simulate_all(profile=None):
    return {
        "M1_jab": simulate("M1_jab", profile),
        "M1_hook": simulate("M1_hook", profile),
        "M1_heavy": [simulate("M1_heavy", profile), simulate("M1_heavy", profile, land=False)],
        "M2_combo": simulate("M2_combo", profile),
        "M3_block": simulate("M3_block", profile),
        "M4_dodge": simulate("M4_dodge", profile),
        "M5_knockdown": [simulate("M5_knockdown", profile, ko=False),
                         simulate("M5_knockdown", profile, ko=True)],
        "M5k_kerb": [simulate("M5k_kerb", profile, death=True)],
        "M6_two_attackers": simulate("M6_two_attackers", profile),
        "M7_breakage": [simulate("M7_breakage", profile, weapon=w) for w in ("chair", "brick", "pipe")],
        "M8_camera_narrow": simulate("M8_camera_narrow", profile),
        "M9_stamina": simulate("M9_stamina", profile),
        "M10_targets": simulate("M10_targets", profile),
    }


def report(rows):
    lines = []
    for k, v, lo, hi, verdict in rows:
        band = "" if lo is None and hi is None else f"[{lo if lo is not None else '-'} .. {hi if hi is not None else '-'}]"
        lines.append(f"{verdict:8} {k:28} {v!s:10} {band}")
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        res = score_drill(sys.argv[1], read_log(sys.argv[2]))
        print(report(compare_targets(res, {k: TARGETS[k] for k in res if k in TARGETS})))
    else:
        print(report(compare_targets(score_runs(simulate_all()))))
