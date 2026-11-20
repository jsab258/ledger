"""Replay a breaker's (or a player type's) claimed faults by machine (lane task 4t, piece 3).

    python replay.py --dist DIR --hidden DIR --report breaker.json --out DIR [--seed 7]

Reads the session's actions.jsonl (in --hidden, written by play.py serve) and the tester's JSON report, replays the
same actions in a fresh game with the same seed up to each claimed fault's action number n, and checks the claim
by its class:

  crash                a new page error (not a missing picture) while action n itself ran
  stuck                Tom walked off W, S, A, D in turn (the clumsy newcomer's escape test)
  camera               the line from Tom to the camera at action n (the clumsy newcomer's camera test)
  content              the content word list of machine_checks against the words on screen at action n
  money                only the money rules of machine_checks.rule_faults at action n (whole pence, a real
                       number, the pocket never below nothing); "paid twice" or "money from nothing" cannot be
                       seen at one moment, so when these hold the claim NEEDS A LOOK, never a final no
  people               people inside a solid for 1.5 s or under 18 (machine_checks' held scan); when that holds,
                       NEEDS A LOOK (a person killed or left on the ground has no machine test yet)
  cab, soft lock, talk, period, other   no machine test: NEEDS A LOOK

First the replay must reach the same game: day, clock (within 2 game minutes), money and Tom's place (within 2 m)
at action n equal to the logged ones. If not, the claim is NOT REPRODUCED (the replay went another way; the reason
is given). If it did and the class's machine test fails, REPRODUCED. If it did and the test holds, NOT REPRODUCED
only for the classes whose test sees the whole claim (crash, stuck, camera, content); NEEDS A LOOK for the rest.
For NEEDS A LOOK the replayed screenshot is saved beside the original for the panel.
Writes replay.json in --out. Test tools only: the game's code is never changed. Exit code 0 always (a report, not a
gate); the loop counts REPRODUCED.
"""
import argparse
import json
import math
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PLAYERS = os.path.join(os.path.dirname(HERE), "players")
GATE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "gate"))
sys.path.insert(0, PLAYERS)
sys.path.insert(0, GATE)

FINAL = {"crash", "stuck", "camera", "content"}      # the test sees the whole claim: holding means a real no
PARTIAL = {"money", "people"}                         # the test sees part: holding means a look, never a no
MACHINE = FINAL | PARTIAL
LOOK_ONLY = {"cab", "soft lock", "talk", "period", "other"}


def load_actions(hidden):
    """Returns (seed, actions). play.py writes the seed as row n 0; the action numbers must climb strictly, or the
    folder holds more than one session and cannot be replayed."""
    rows, seed = [], None
    with open(os.path.join(hidden, "actions.jsonl")) as f:
        for line in f:
            line = line.strip()
            if line:
                r = json.loads(line)
                if r.get("n") == 0 and "seed" in r:
                    seed = r["seed"]
                else:
                    rows.append(r)
    ns = [r.get("n") for r in rows]
    if any(b <= a for a, b in zip(ns, ns[1:])):
        raise SystemExit("the action log's numbers do not climb: more than one session in one --hidden folder")
    return seed, rows


def parse_action(text):
    """play.py logs each action as 'cmd arg arg'; a typed line keeps its spaces."""
    parts = text.split(" ", 1)
    cmd = parts[0]
    if cmd == "type":
        return cmd, [parts[1] if len(parts) > 1 else ""]
    return cmd, (parts[1].split(" ") if len(parts) > 1 else [])


def same_game(a, b):
    """Pure: the differences between two LEDGER.read() states that matter for a replay, or [] when the same."""
    if not a or not b:
        return ["no state to compare"]
    d = []
    for k in ("dayIndex",):
        if a.get(k) != b.get(k):
            d.append("%s %r became %r" % (k, a.get(k), b.get(k)))
    if abs((a.get("gameMinute") or 0) - (b.get("gameMinute") or 0)) > 2:
        d.append("clock %s became %s" % (a.get("clock"), b.get("clock")))
    if json.dumps(a.get("money"), sort_keys=True) != json.dumps(b.get("money"), sort_keys=True):
        d.append("money %s became %s" % (a.get("money"), b.get("money")))
    ta, tb = a.get("tom") or {}, b.get("tom") or {}
    try:
        if math.hypot(ta["xMetres"] - tb["xMetres"], ta["zMetres"] - tb["zMetres"]) > 2:
            d.append("Tom's place moved %.1f m" % math.hypot(ta["xMetres"] - tb["xMetres"], ta["zMetres"] - tb["zMetres"]))
    except (KeyError, TypeError):
        d.append("Tom's place missing")
    return d


def verdict(cls, reached_diffs, machine_failed):
    """Pure: the claim's result from whether the replay reached the same game and the class's machine test."""
    if reached_diffs:
        return "NOT REPRODUCED", "the replay went another way: " + "; ".join(reached_diffs[:3])
    if cls in MACHINE and machine_failed:
        return "REPRODUCED", "the machine test fails at this action"
    if cls in FINAL:
        return "NOT REPRODUCED", "the same game was reached and the machine test holds"
    if cls in PARTIAL:
        return "NEEDS A LOOK", "the machine test holds, but it cannot see every form of this claim; screenshots saved side by side"
    return "NEEDS A LOOK", "no machine test for this class; screenshots saved side by side"


def classify(c):
    c = (c or "other").strip().lower()
    return c if c in MACHINE | LOOK_ONLY else "other"


def real_errors(errors):
    return [e for e in errors if "404" not in e]  # missing pictures in a build without the art are not crashes


def machine_test(g, cls, out, n, errors_before):
    """Run the class's test on the live replayed game at action n. Returns (failed, detail)."""
    import machine_checks as mc
    import invariants as inv
    if cls == "crash":
        errs = real_errors(g.errors[errors_before:])  # only errors raised while action n ran
        return bool(errs), errs[:5]
    if cls == "money":
        f = [x for x in mc.rule_faults(g.state(), None, []) if x.startswith(("money", "pocket"))]
        return bool(f), f[:10]
    if cls == "people":
        held = mc.Checks.people_held(g)
        return bool(held), held[:10]
    if cls == "content":
        s = mc.content_scan(json.dumps(list(g.words().values())).replace("\\n", " "))
        return bool(s["fails"]), s["fails"][:10] if isinstance(s["fails"], list) else s["fails"]
    from clumsy import Gate
    gate = Gate(g, out)
    if cls == "stuck":
        v = inv.moved_again(gate.escape_track(["KeyW", "KeyS", "KeyA", "KeyD"], secs_each=1.5))
        return not v["ok"], v
    if cls == "camera":
        r = gate.check_camera("replay to action %d" % n, "replay")
        return not r["ok"], {k: r.get(k) for k in ("hit", "dist", "what")}
    return False, None


def replay_one(dist, seed, actions, claim, out):
    try:
        return _replay_one(dist, seed, actions, claim, out)
    except Exception as e:  # noqa: BLE001 - one broken replay never loses the others
        return {"claim": claim, "class": classify(claim.get("class")), "result": "NEEDS A LOOK",
                "why": "the replay itself broke: %s" % str(e)[:300]}


def _replay_one(dist, seed, actions, claim, out):
    import play
    try:
        n = int(claim.get("n") or 0)
    except (TypeError, ValueError):
        n = 0
    cls = classify(claim.get("class"))
    res = {"claim": claim, "class": cls}
    logged = next((a for a in actions if a.get("n") == n), None)
    if not n or logged is None:
        res.update(result="NOT REPRODUCED", why="no action number, or it is not in the log: cannot be replayed")
        return res
    work = tempfile.mkdtemp(prefix="work-%04d-" % n, dir=out)  # inside --out, removed after
    sess = play.Session(dist, work, seed, os.path.join(work, "hidden"), minutes=10 ** 6)
    try:
        sess.g.clear(tries=0)
        rec, errors_before = None, 0
        for a in actions:
            if a["n"] > n:
                break
            if a["n"] == n:
                errors_before = len(sess.g.errors)
            cmd, args = parse_action(a["action"])
            rec = sess.act(cmd, args)
        state = sess.g.state()
        diffs = same_game(logged.get("hidden", {}).get("state"), state)
        failed, detail = (False, None) if diffs else machine_test(sess.g, cls, out, n, errors_before)
        result, why = verdict(cls, diffs, failed)
        res.update(result=result, why=why, detail=detail)
        os.makedirs(os.path.join(out, "shots"), exist_ok=True)
        if rec and rec.get("shot"):
            res["replay_shot"] = shutil.copy(rec["shot"], os.path.join(out, "shots", "replay-%04d.png" % n))
        res["original_shot"] = logged.get("shot")
    finally:
        try:
            sess.g.close()
        except Exception:  # noqa: BLE001
            pass
        shutil.rmtree(work, ignore_errors=True)
    return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", required=True)
    ap.add_argument("--hidden", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, help="only for an old log without its seed row; else the log's own seed")
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    report = json.load(open(a.report))
    seed, actions = load_actions(a.hidden)
    seed = seed if seed is not None else (a.seed if a.seed is not None else 7)
    results = [replay_one(a.dist, seed, actions, c, a.out) for c in report.get("faults", [])]
    counts = {}
    for r in results:
        counts[r["result"]] = counts.get(r["result"], 0) + 1
    json.dump({"tester": report.get("type"), "counts": counts, "results": results},
              open(os.path.join(a.out, "replay.json"), "w"), indent=1, default=str)
    print(json.dumps(counts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
