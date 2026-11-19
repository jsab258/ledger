"""The publish gate's experience rules as pure checks on recorded numbers (no browser).

Each function takes rows the clumsy player recorded and returns a verdict dict with "ok" and the numbers.
Until DESIGN.md is published these are the interim rules from the lane's order (4o): never stuck, every input
device usable, every state change shown or said, no failure without warning, camera never inside geometry,
no page errors, no stretch where nothing responds.
"""
import math
import os
import re

STUCK_LIMIT_S = 5.0      # able to move again within this many seconds of any stop
MOVED_M = 0.5            # counts as moving again
SILENT_LIMIT_S = 1.5     # a state change must show words within this time
UNRESPONSIVE_S = 3.0     # longest stretch of held input with nothing moving


def moved_again(track, limit_s=STUCK_LIMIT_S, moved_m=MOVED_M):
    """track: list of (seconds, x, z) after a stop, while the player tries to get away.
    Returns ok and the first time the player was moved_m away from the start."""
    if not track:
        return {"ok": False, "free_after_s": None, "reason": "no samples"}
    t0, x0, z0 = track[0]
    for t, x, z in track:
        if math.hypot(x - x0, z - z0) >= moved_m:
            free = round(t - t0, 2)
            return {"ok": free <= limit_s, "free_after_s": free}
    return {"ok": False, "free_after_s": None, "reason": "never moved %.1f m in %.1f s" % (moved_m, track[-1][0] - t0)}


def longest_unresponsive(rows, eps_m=0.05):
    """rows: list of (seconds, pressing(bool), x, z). The longest run of pressing with no movement."""
    best, start, last = 0.0, None, None
    for t, pressing, x, z in rows:
        if pressing and last is not None and math.hypot(x - last[0], z - last[1]) < eps_m:
            if start is None:
                start = t
            best = max(best, t - start)
        else:
            start = None
        last = (x, z)
    return {"ok": best <= UNRESPONSIVE_S, "longest_s": round(best, 2)}


# ---------------------------------------------------------------- the game's own words, read from its source
# The "told on screen" checks match on the game's own event kinds and on the lines its source writes for them
# (kinds.js: what the Ledger's Noted line says; talk_lines.js: what people who saw it say), never on guessed
# English words. test_invariants.py builds these from the source, so the test breaks if the wording drifts.
SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prototype", "project", "src")
SCREEN_PLACES = ("subs", "noted", "news", "bubbles")  # places a player can read; "queued" notes are not yet shown


def _template_rx(t):
    """A source string or template literal as a regex: ${...} and {t} stand for any words."""
    parts = re.split(r"\$\{[^}]*\}|\{[a-z]+\}", t)
    return r".+?".join(re.escape(p) for p in parts)


def _literals(text):
    return [m.group(2) for m in re.finditer(r"([`'\"])((?:\\.|(?!\1).)*)\1", text)]


def source_phrases(kind, src=SRC):
    """Regexes for every line the game's source writes about an event of this kind (kinds.js, talk_lines.js)."""
    out = []
    kinds = open(os.path.join(src, "kinds.js"), encoding="utf-8").read()
    m = re.search(r"\n  %s: K\(\s*'%s',\s*\(e\) => (`[^`]*`|'[^']*'),\s*\(e\) => (`[^`]*`|'[^']*')" % (kind, kind), kinds)
    if m:
        truth, mine = m.group(1)[1:-1], m.group(2)[1:-1]
        out.append(_template_rx(truth))
        # the Noted line (ledger_screen.js believedLine): "Noted in the Ledger: WHO knows|may have seen ... that you MINE."
        out.append(r"Noted in the Ledger: .+? that you " + _template_rx(mine[:1].lower() + mine[1:]))
    talk = open(os.path.join(src, "talk_lines.js"), encoding="utf-8").read()
    for blk in re.finditer(r"\n  %s: (\{.*?\}|'(?:\\.|[^'])*'|\"(?:\\.|[^\"])*\"),?\n" % kind, talk, re.S):
        for lit in _literals(blk.group(1)):
            if len(lit) > 8:
                out.append(_template_rx(lit.replace("\\'", "'")))
    return [re.compile(p, re.I) for p in out]


def count_line_rx(src=SRC):
    """The merged Noted line ("Noted in the Ledger: 11 things", ui.js): it names no event."""
    ui = open(os.path.join(src, "ui.js"), encoding="utf-8").read()
    m = re.search(r"`(Noted in the Ledger: )\$\{n\}( things)`", ui)
    return re.compile(re.escape(m.group(1)) + r"\d+" + re.escape(m.group(2))) if m else None


def told(before, frames, patterns, limit_s=SILENT_LIMIT_S, count_rx=None):
    """before: the game's message lists just before the event (dict place -> list of texts or a text).
    frames: list of (seconds after the event frame, lists). ok when a place a player can read shows a new text
    matching one of the game's own lines for the event within limit_s. Also says when the line was only queued
    (the Noted queue, not yet on screen), only a count line showed, or the line came late."""
    def texts(d, k):
        v = d.get(k) or []
        return [v] if isinstance(v, str) else list(v)
    seen = {k: set(texts(before, k)) for k in SCREEN_PLACES + ("queued",)}
    res = {"ok": False, "after_s": None, "queued_at_s": None, "count_line_at_s": None, "late_at_s": None}
    for t, d in frames:
        for k in SCREEN_PLACES + ("queued",):
            for v in texts(d, k):
                v = (v or "").strip()
                if not v or v in seen[k]:
                    continue
                if any(p.search(v) for p in patterns):
                    if k == "queued":
                        if res["queued_at_s"] is None:
                            res["queued_at_s"] = round(t, 2)
                        continue
                    if t <= limit_s + 1e-9:
                        res.update(ok=True, after_s=round(t, 2), where=k, words=v[:160])
                        return res
                    if res["late_at_s"] is None:
                        res.update(late_at_s=round(t, 2), late_words=v[:160])
                elif count_rx and k == "noted" and count_rx.search(v) and res["count_line_at_s"] is None:
                    res["count_line_at_s"] = round(t, 2)
    return res


# ---------------------------------------------------------------- steering
STEER_MIN_RISE_S = 0.1     # the 10%-to-90% move of the turn rate takes at least this long (about: 0.09 accepted)
STEER_MAX_STEP = 0.2       # no single frame moves the turn rate by more than this share of the whole change


def steer_change(rates, dt, start=None, end=None):
    """rates: the turn rate each frame, from the last frame before the key changed. start/end: the rates before
    and after (default: the first and the last of the series). Returns the 10%-to-90% time and the biggest one-frame
    step as a share of the change; ok when the move is eased (rise >= about 0.1 s, every step <= STEER_MAX_STEP)."""
    if len(rates) < 2:
        return {"ok": False, "reason": "no samples"}
    r0 = rates[0] if start is None else start
    r1 = rates[-1] if end is None else end
    swing = r1 - r0
    if abs(swing) < 1e-6:
        return {"ok": False, "reason": "the turn rate did not change", "from": round(r0, 3), "to": round(r1, 3)}
    share = [(r - r0) / swing for r in rates]
    i10 = next((i for i, s in enumerate(share) if s >= 0.1), None)
    i90 = next((i for i, s in enumerate(share) if s >= 0.9), None)
    if i10 is None or i90 is None:
        return {"ok": False, "reason": "never reached 90% of the change", "from": round(r0, 3), "to": round(r1, 3)}
    rise = (i90 - i10) * dt
    step = max(abs(share[i] - share[i - 1]) for i in range(1, len(share)))
    return {"ok": rise >= STEER_MIN_RISE_S - 0.011 and step <= STEER_MAX_STEP + 1e-9, "rise_10_90_s": round(rise, 3),
            "biggest_frame_step_share": round(step, 3), "from": round(r0, 3), "to": round(r1, 3)}


def camera_clear(hit_m, cam_dist_m, near_ignore_m, slack_m=0.3):
    """hit_m: distance from the look point to the first solid thing on the line to the camera (None when clear).
    The camera is blocked when a solid lies between the look point and the camera, past near_ignore_m."""
    if hit_m is None or hit_m < near_ignore_m:
        return {"ok": True}
    blocked = hit_m < cam_dist_m - slack_m
    return {"ok": not blocked, "solid_at_m": round(hit_m, 2), "camera_at_m": round(cam_dist_m, 2)}


def summarise(results):
    """results: list of {"rule", "ok", ...}. Counts by rule, failures listed with their steps."""
    out = {}
    for r in results:
        s = out.setdefault(r["rule"], {"checked": 0, "failed": 0, "failures": []})
        s["checked"] += 1
        if not r["ok"]:
            s["failed"] += 1
            s["failures"].append(r)
    return out


# ---------------------------------------------------------------- what the game draws, read from its source
# The street furniture the game draws (render/town.js draws map.js's LAMPS and PROPS; render/sync.js places the
# parked cars). The game's own data code is run in node, as written, so the gate aims at what is drawn and not
# only at what the collision map knows.
NOT_SOLID_BY_DESIGN = {"shelter"}  # the ferry shelter is a roof to stand under


def drawn_props(src=SRC):
    import json
    import subprocess
    mp = open(os.path.join(src, "map.js"), encoding="utf-8").read()
    sy = open(os.path.join(src, "render", "sync.js"), encoding="utf-8").read()
    props = mp[mp.index("export const PROPS = []"):mp.index("// Sodium street lamps")]
    lamps = mp[mp.index("export const LAMPS = []"):mp.index("export const GLOWS")]
    a = sy.index("// a few parked cars for life")
    parked = sy[sy.index("for (const [k, c, x, z, a] of", a) + len("for (const [k, c, x, z, a] of"):sy.index("]) {", a) + 1]
    js = ("const hyp = Math.hypot;\n" + (props + lamps).replace("export const", "const")
          + "\nconst PARKED = " + parked + ";\nconsole.log(JSON.stringify({PROPS, LAMPS, PARKED}));")
    p = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=60)
    if p.returncode:
        raise RuntimeError("could not read the drawn props from the source: " + p.stderr[:300])
    d = json.loads(p.stdout)
    out = []
    for q in d["PROPS"]:
        if q["t"] not in NOT_SOLID_BY_DESIGN:
            out.append({"type": q["t"], "x": q["x"], "z": q["z"], "r": max(q.get("r") or 0, 0.1), "w": q.get("w")})
    for l in d["LAMPS"]:
        if l["k"] == 1:  # a column lamp stands on the ground; k 2 and 3 hang on walls
            out.append({"type": "lamp post", "x": l["x"], "z": l["z"], "r": 0.11})
    for k, c, x, z, a in d["PARKED"]:
        out.append({"type": "parked car", "kind": k, "x": x, "z": z, "r": 1.5, "ang": a})
    return out
