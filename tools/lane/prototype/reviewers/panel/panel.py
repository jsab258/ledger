"""The panel judges recordings of real play sessions (lane task 4t, piece 6).

Turns one played session (play.py's screenshots and its hidden action log) into a recording packet a judge can look
at: frame strips (one frame every 15 to 20 game seconds across the whole session), short clips (six frames in a row
around chosen moments) and the plain log of what the player pressed and what was on screen. The judge never gets a
written summary, the player's own review, the game's hidden state or any design file: only what a person watching
over the player's shoulder would have seen, in order, with the minute.

    python panel.py strip --shots DIR --hidden DIR --out DIR [--answer player.json] [--label "loop 1, the rusher"]
    python panel.py pair  --a DIR --b DIR --out DIR --key KEYDIR/<pair>.key.json [--seed N]
    python panel.py score --answers DIR [--pairs DIR] --out FILE.md

strip: --shots is play.py's --out folder (holding shots/), --hidden its --hidden folder (actions.jsonl), --answer the
player type's JSON answer (only its minutes are used, to choose the clips; its words never reach the judge). Writes
OUT/sheets/*.jpg, OUT/LOG.md and OUT/PACKET.md (the list of what to look at), and OUT/../<name>.moments.json beside
it (why each clip was chosen, for scoring; never given to the judge).
pair: puts two packets side by side as A and B (for before and after a loop), in two orders, OUT/order1 and OUT/order2,
A and B swapped between them; each copy's label becomes "version A" or "version B", so nothing names the loop. The key
goes to --key (name it <pair>.key.json), outside --out. Each judge sees both orders, in separate fresh sessions, never told.
score: reads the judges' JSON answers and writes the panel's verdict: recommends out of judges, each axis's middle
value and spread, dead stretches named by two or more judges, faults to check by machine (never counted as found),
and for pairs the winner per axis counted in both orders (a winner that changes with the order counts as a tie).

Test tools only: reads a session's files, never the game's code. No model runs here; the judges are helpers given
PANEL-PROMPT.md and ANCHORS.md with one packet.
"""
import argparse
import glob
import json
import os
import random
import shutil
import statistics
import sys

from PIL import Image, ImageDraw, ImageFont

AXES = ["hands_busy", "town_alive", "people_and_talk", "tension", "controls_and_camera", "period_and_place",
        "knowing_what_to_do", "looks_finished"]
TILE = (480, 270)
STRIP_COLS, STRIP_ROWS = 3, 4      # 12 frames a strip sheet
CLIP_LEN = 6                       # frames in a clip, in a row
MAX_STRIP_FRAMES = 48              # at most 4 strip sheets a session
MIN_STRIP_GAP_S = 15
MAX_CLIPS = 6
WORDS_KEYS = ["subs", "dialog", "talk", "prompt", "obj", "fare", "news", "noted", "called", "bubbles", "panel"]


def font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def load_rows(hidden):
    rows = []
    with open(os.path.join(hidden, "actions.jsonl")) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r.get("n", 0) >= 1 and "minute" in r:
                rows.append(r)
    return rows


def shot_path(row, shots_dir):
    """The row's screenshot, found under the --shots folder by its file name (the session may have moved)."""
    p = row.get("shot")
    if not p:
        return None
    for cand in [p, os.path.join(shots_dir, "shots", os.path.basename(p)), os.path.join(shots_dir, os.path.basename(p))]:
        if os.path.exists(cand):
            return cand
    return None


def words_line(row, limit=150):
    w = row.get("words") or {}
    parts = [str(w[k]).replace("\n", " / ") for k in WORDS_KEYS if w.get(k)]
    parts += [str(v).replace("\n", " / ") for k, v in w.items() if k not in WORDS_KEYS and v]
    s = " | ".join(parts)
    return s if len(s) <= limit else s[: limit - 3] + "..."


def pick_strip(rows, shots_dir):
    """One frame every gap seconds of played time across the session, the gap at least 15 s and wide enough that
    the whole session fits in 48 frames. Rows with no screenshot are skipped."""
    rows = [r for r in rows if shot_path(r, shots_dir)]
    if not rows:
        return []
    total_s = rows[-1]["minute"] * 60
    gap = max(MIN_STRIP_GAP_S, total_s / (MAX_STRIP_FRAMES - 1))
    out, next_t = [], 0.0
    for r in rows:
        t = r["minute"] * 60
        if t + 1e-6 >= next_t:
            out.append(r)
            next_t = t + gap
    out = out[:MAX_STRIP_FRAMES]
    if out[-1] is not rows[-1]:
        if len(out) == MAX_STRIP_FRAMES:
            out[-1] = rows[-1]
        else:
            out.append(rows[-1])      # the last thing seen always shows
    return out


def moments_from(rows, answer):
    """Minutes worth a closer look, and why (kept away from the judge): the player's best and worst moments, its
    faults and its quit, then the biggest bursts of new words on screen (talk and scenes), then the session's end."""
    m = []
    if answer:
        for key in ["best_moment", "worst_moment"]:
            v = answer.get(key) or {}
            if isinstance(v, dict) and isinstance(v.get("minute"), (int, float)):
                m.append((float(v["minute"]), key))
        for fz in answer.get("faults") or []:
            if isinstance(fz, dict) and isinstance(fz.get("minute"), (int, float)):
                m.append((float(fz["minute"]), "fault"))
        if answer.get("quit") and isinstance(answer.get("quit_minute"), (int, float)):
            m.append((float(answer["quit_minute"]), "quit"))
    seen, bursts = set(), []
    for r in rows:
        new = 0
        for line in words_line(r, 10_000).split(" | "):
            if line and line not in seen:
                if any(old.startswith(line) for old in seen):   # half-typed talk, already counted whole
                    continue
                before = max((len(old.split()) for old in seen if line.startswith(old)), default=0)
                seen.add(line)
                new += max(0, len(line.split()) - before)
        if new:
            bursts.append((new, r["minute"]))
    for _, minute in sorted(bursts, reverse=True)[:3]:
        m.append((float(minute), "words"))
    if rows:
        m.append((float(rows[-1]["minute"]), "end"))
    # drop moments within half a minute of one already kept, in priority order
    kept = []
    for minute, why in m:
        if all(abs(minute - k[0]) >= 0.5 for k in kept):
            kept.append((minute, why))
    return kept[:MAX_CLIPS]


def clip_rows(rows, minute, shots_dir):
    rows = [r for r in rows if shot_path(r, shots_dir)]
    if not rows:
        return []
    i = min(range(len(rows)), key=lambda k: abs(rows[k]["minute"] - minute))
    lo = max(0, min(i - CLIP_LEN // 2, len(rows) - CLIP_LEN))
    return rows[lo: lo + CLIP_LEN]


def sheet(rows, shots_dir, path, cols, title):
    n_rows = max(1, -(-len(rows) // cols))
    cap_h = 44
    W, H = TILE[0] * cols, 34 + n_rows * (TILE[1] + cap_h)
    img = Image.new("RGB", (W, H), (16, 16, 16))
    d = ImageDraw.Draw(img)
    f_t, f_c = font(20), font(14)
    d.text((8, 6), title, fill=(240, 240, 240), font=f_t)
    for k, r in enumerate(rows):
        x, y = (k % cols) * TILE[0], 34 + (k // cols) * (TILE[1] + cap_h)
        try:
            im = Image.open(shot_path(r, shots_dir)).convert("RGB")
            im.thumbnail(TILE)
            img.paste(im, (x + (TILE[0] - im.width) // 2, y))
        except Exception:  # noqa: BLE001 - an unreadable frame is drawn as a grey box and named
            d.rectangle([x, y, x + TILE[0] - 1, y + TILE[1] - 1], fill=(70, 70, 70))
            d.text((x + 8, y + 8), "frame could not be read", fill=(255, 255, 255), font=f_c)
        cap1 = "min %.1f   %s" % (r["minute"], (r.get("action") or "")[:40])
        cap2 = words_line(r, 64)
        d.text((x + 6, y + TILE[1] + 4), cap1, fill=(255, 220, 120), font=f_c)
        d.text((x + 6, y + TILE[1] + 22), cap2, fill=(200, 200, 200), font=f_c)
    img.save(path, "JPEG", quality=82)
    return path


def fresh_dir(out, marker):
    """Empty out for a new packet, but only a folder this tool made (holding its marker file) or an empty one."""
    if os.path.exists(out):
        if os.listdir(out) and not os.path.exists(os.path.join(out, marker)):
            raise SystemExit("%s is not empty and is not an earlier %s folder: refusing to clear it" % (out, marker))
        shutil.rmtree(out)
    os.makedirs(out)


def strip(a):
    rows = load_rows(a.hidden)
    if not rows:
        raise SystemExit("no actions in %s/actions.jsonl: nothing to judge" % a.hidden)
    answer = json.load(open(a.answer)) if a.answer else None
    out = a.out
    fresh_dir(out, "PACKET.md")
    os.makedirs(os.path.join(out, "sheets"))
    label = a.label or "a play session"
    files = []
    strip_rows = pick_strip(rows, a.shots)
    per = STRIP_COLS * STRIP_ROWS
    for s in range(0, len(strip_rows), per):
        part = strip_rows[s: s + per]
        p = os.path.join(out, "sheets", "strip-%02d.jpg" % (s // per + 1))
        sheet(part, a.shots, p, STRIP_COLS, "Whole session, minutes %.1f to %.1f (left to right, top to bottom)"
              % (part[0]["minute"], part[-1]["minute"]))
        files.append(("strip", os.path.basename(p), part[0]["minute"], part[-1]["minute"]))
    moments = moments_from(rows, answer)
    secret = []
    for k, (minute, why) in enumerate(sorted(moments), 1):
        cr = clip_rows(rows, minute, a.shots)
        if not cr:
            continue
        p = os.path.join(out, "sheets", "clip-%02d.jpg" % k)
        sheet(cr, a.shots, p, 3, "Clip %d: six frames in a row, minutes %.1f to %.1f" % (k, cr[0]["minute"], cr[-1]["minute"]))
        files.append(("clip", os.path.basename(p), cr[0]["minute"], cr[-1]["minute"]))
        secret.append({"clip": k, "minute": minute, "why": why})
    with open(os.path.join(out, "LOG.md"), "w") as f:
        f.write("# What the player pressed and what was on screen\n\n%s. Minute played (reading counts), the action, "
                "the words on screen after it.\n\n" % label)
        last = None
        for r in rows:
            wl = words_line(r, 600)
            f.write("- %.2f  %s  %s\n" % (r["minute"], r.get("action", ""), wl if wl != last else "(same words)"))
            last = wl
    with open(os.path.join(out, "PACKET.md"), "w") as f:
        f.write("# Recording packet: %s\n\nLength: %.1f minutes played, %d actions.\n\nLook at every sheet, in this "
                "order, then read LOG.md.\n\n" % (label, rows[-1]["minute"], len(rows)))
        for kind, name, m0, m1 in files:
            f.write("- sheets/%s (%s, minutes %.1f to %.1f)\n" % (name, kind, m0, m1))
    side = os.path.join(os.path.dirname(os.path.abspath(out)), os.path.basename(os.path.abspath(out)) + ".moments.json")
    json.dump({"label": label, "clips": secret, "minutes": rows[-1]["minute"]}, open(side, "w"), indent=1)
    print(json.dumps({"packet": out, "sheets": len(files), "clips": len(secret), "minutes": rows[-1]["minute"]}))
    return 0


def packet_label(folder):
    try:
        first = open(os.path.join(folder, "PACKET.md")).readline()
    except OSError:
        return None
    return first.split(":", 1)[1].strip() if first.startswith("# Recording packet:") and ":" in first else None


def blind_copy(src, dst, letter):
    """Copy a packet as version A or B, with its label (which may name the loop) replaced everywhere."""
    shutil.copytree(src, dst)
    label = packet_label(src)
    for name in ("PACKET.md", "LOG.md"):
        p = os.path.join(dst, name)
        if os.path.exists(p):
            t = open(p).read()
            if label:
                t = t.replace(label, "version %s" % letter)
            open(p, "w").write(t)


def pair(a):
    """Two orders of the same pair, order1/ and order2/, A and B swapped between them. The judge is never told which
    order it has; the key (kept outside --out) says which letter is the version after the loop in each."""
    rnd = random.Random(a.seed)
    if os.path.abspath(a.key).startswith(os.path.abspath(a.out) + os.sep):
        raise SystemExit("--key must not be inside --out (the judge may open files under --out)")
    fresh_dir(a.out, "PAIRS.txt")
    open(os.path.join(a.out, "PAIRS.txt"), "w").write("made by panel.py pair\n")
    name = a.name or os.path.splitext(os.path.basename(a.key))[0].replace(".key", "")
    after_first = rnd.random() < 0.5
    key = {"pair": name, "before": os.path.abspath(a.a), "after": os.path.abspath(a.b), "orders": {}}
    for order, after_is_a in (("order1", after_first), ("order2", not after_first)):
        d = os.path.join(a.out, order)
        os.makedirs(d)
        blind_copy(a.b if after_is_a else a.a, os.path.join(d, "A"), "A")
        blind_copy(a.a if after_is_a else a.b, os.path.join(d, "B"), "B")
        with open(os.path.join(d, "PAIR.md"), "w") as f:
            f.write("# Two recordings of the same game, A and B\n\nPair: %s/%s (copy this into your answer's \"pair\").\n\n"
                    "The same kind of player played two versions of one game. Look at A's sheets, then B's, then both "
                    "logs.\n" % (name, order))
        key["orders"][order] = "A" if after_is_a else "B"
    json.dump(key, open(a.key, "w"), indent=1)
    print(json.dumps({"pair": a.out, "key": a.key, "name": name}))
    return 0


def _num(v):
    if isinstance(v, dict):
        v = v.get("score")
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    return float(v) if 1 <= v <= 5 else None


def merge_dead(dead):
    """Dead stretches (from, to, judge): overlapping ones merged into one span; kept when two or more judges share it."""
    spans = []
    for f0, t0, who in sorted(dead):
        if spans and f0 < spans[-1][1]:
            spans[-1][1] = max(spans[-1][1], t0)
            spans[-1][2].add(who)
        else:
            spans.append([f0, t0, {who}])
    return [(f, t, len(w)) for f, t, w in spans if len(w) >= 2]


def score_single(answers):
    """Judges' answers on single sessions, one table per session: recommends, each axis's middle value and spread,
    dead stretches named by two or more judges, and faults to check by machine."""
    sessions = {}
    for name, ans in answers:
        if "better" in ans:
            continue
        sessions.setdefault(str(ans.get("session", "unnamed")), []).append((name, ans))
    lines, summary = [], {}
    for sess, group in sorted(sessions.items()):
        rec, per_axis, dead, faults = 0, {k: [] for k in AXES}, [], []
        for name, ans in group:
            rec += 1 if ans.get("would_recommend") is True else 0
            for k in AXES:
                v = _num((ans.get("scores") or {}).get(k))
                if v is not None:
                    per_axis[k].append(v)
            for dz in ans.get("dead_stretches") or []:
                if isinstance(dz, dict) and all(isinstance(dz.get(x), (int, float)) and not isinstance(dz.get(x), bool)
                                                for x in ("from", "to")):
                    dead.append((float(dz["from"]), float(dz["to"]), str(ans.get("judge", name))))
            for fz in ans.get("faults_seen") or []:
                if isinstance(fz, dict):
                    faults.append((fz.get("minute"), str(fz.get("what", ""))[:160], str(ans.get("judge", name))))
        n = len(group)
        lines += ["### %s" % sess, "", "Recommends: %d of %d judges." % (rec, n), "",
                  "| Axis | Middle | Spread (low to high) | Judges |", "|---|---|---|---|"]
        summary[sess] = {"recommend": rec, "judges": n, "axes": {}}
        for k in AXES:
            v = per_axis[k]
            if v:
                summary[sess]["axes"][k] = statistics.median(v)
                lines.append("| %s | %.1f | %.0f to %.0f | %d |" % (k.replace("_", " "), statistics.median(v), min(v), max(v), len(v)))
            else:
                lines.append("| %s | not judged | | 0 |" % k.replace("_", " "))
        shared = merge_dead(dead)
        if shared:
            lines += ["", "Dead stretches named by two or more judges (minutes): " +
                      ", ".join("%.0f to %.0f (%d judges)" % s for s in shared)]
        if faults:
            lines += ["", "Faults the judges think they saw (to replay by machine; a judge's eye alone is never a found fault):"]
            lines += ["- minute %s: %s (judge %s)" % f for f in faults[:20]]
        lines.append("")
    return lines, summary


def score_pairs(answers, key_dir):
    """Pairs, each judged in order1 and order2 (A and B swapped, the judge not told). A winner, overall and per axis,
    that holds in both orders counts; one that changes with the order is a tie (Shi and others, 2025)."""
    seen = {}
    for name, ans in answers:
        if "better" not in ans:
            continue
        pid, _, order = str(ans.get("pair", "")).partition("/")
        seen.setdefault((pid, str(ans.get("judge", name))), {})[order] = ans
    lines, tally = [], {"after": 0, "before": 0, "tie": 0}
    axes_tally = {k: {"after": 0, "before": 0, "tie": 0} for k in AXES}
    for (pid, judge), orders in sorted(seen.items()):
        keyf = os.path.join(key_dir or "", "%s.key.json" % pid)
        if not key_dir or not os.path.exists(keyf):
            lines.append("- pair %s, judge %s: no key found, not scored" % (pid, judge))
            continue
        if set(orders) != {"order1", "order2"}:
            lines.append("- pair %s, judge %s: judged in one order only, not scored" % (pid, judge))
            continue
        key = json.load(open(keyf))

        def real(letter, order):
            if letter not in ("A", "B"):
                return "tie"
            return "after" if letter == key["orders"][order] else "before"

        w1, w2 = real(orders["order1"].get("better"), "order1"), real(orders["order2"].get("better"), "order2")
        res = w1 if w1 == w2 else "tie"
        tally[res] += 1
        for k in AXES:
            a1 = real((orders["order1"].get("axes") or {}).get(k), "order1")
            a2 = real((orders["order2"].get("axes") or {}).get(k), "order2")
            axes_tally[k][a1 if a1 == a2 else "tie"] += 1
        lines.append("- pair %s, judge %s: %s (first order %s, second order %s)" % (pid, judge, res, w1, w2))
    if any(tally.values()):
        lines = ["After the loop better: %d; before better: %d; tie or order-dependent: %d."
                 % (tally["after"], tally["before"], tally["tie"]), "",
                 "| Axis | After better | Before better | Tie or order-dependent |", "|---|---|---|---|"] + \
                ["| %s | %d | %d | %d |" % (k.replace("_", " "), v["after"], v["before"], v["tie"]) for k, v in axes_tally.items()] + \
                [""] + lines
    return lines, tally


def score(a):
    answers = []
    for p in sorted(glob.glob(os.path.join(a.answers, "*.json"))):
        try:
            answers.append((os.path.basename(p)[:-5], json.load(open(p))))
        except Exception as e:  # noqa: BLE001 - a broken answer is named, never silently dropped
            print("could not read %s: %s" % (p, e), file=sys.stderr)
    s_lines, summary = score_single(answers)
    p_lines, tally = score_pairs(answers, a.pairs)
    with open(a.out, "w") as f:
        f.write("# The panel's verdict on recordings\n\n")
        if s_lines:
            f.write("## Single sessions\n\n" + "\n".join(s_lines) + "\n\n")
        if p_lines:
            f.write("## Before and after, judged in both orders\n\n" + "\n".join(p_lines) + "\n")
        if not s_lines and not p_lines:
            f.write("No judge answers found.\n")
    print(json.dumps({"summary": summary, "pairs": tally}))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("strip")
    s.add_argument("--shots", required=True)
    s.add_argument("--hidden", required=True)
    s.add_argument("--out", required=True)
    s.add_argument("--answer")
    s.add_argument("--label")
    p = sub.add_parser("pair")
    p.add_argument("--a", required=True, help="the packet before the loop")
    p.add_argument("--b", required=True, help="the packet after the loop")
    p.add_argument("--out", required=True)
    p.add_argument("--key", required=True)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--name", help="the pair's name (default: the key file's name)")
    c = sub.add_parser("score")
    c.add_argument("--answers", required=True)
    c.add_argument("--pairs", help="the folder holding <pair>.key.json files")
    c.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    return {"strip": strip, "pair": pair, "score": score}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
