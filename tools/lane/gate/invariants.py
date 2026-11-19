"""The publish gate's experience rules as pure checks on recorded numbers (no browser).

Each function takes rows the clumsy player recorded and returns a verdict dict with "ok" and the numbers.
Until DESIGN.md is published these are the interim rules from the lane's order (4o): never stuck, every input
device usable, every state change shown or said, no failure without warning, camera never inside geometry,
no page errors, no stretch where nothing responds.
"""
import math

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


DAMAGE_WORDS = ["damage", "dent", "crash", "bumper", "wing", "smash", "scrape", "knock", "wreck", "broke", "headlamp", "radiator"]
HIT_WORDS = ["knock", "hit", "down", "hurt", "ambulance", "run over", "ran over", "cab hit", "bleed"]
MESSAGE_PLACES = ["subs", "news", "noted", "called", "bubbles", "obj", "dialog"]


def said(before, after_frames, limit_s=SILENT_LIMIT_S, about=None, where=None):
    """before: the words on screen (dict of element -> text) just before a state change.
    after_frames: list of (seconds_after, words dict). ok when any element shows new words within limit_s."""
    for t, words in after_frames:
        if t > limit_s:
            break
        for k, v in words.items():
            if where and k not in where:
                continue
            v = (v or "").strip()
            if about and not any(w in v.lower() for w in about):
                continue
            if v and v != (before.get(k) or "").strip():
                return {"ok": True, "after_s": round(t, 2), "where": k, "words": v[:120]}
    return {"ok": False, "after_s": None}


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
