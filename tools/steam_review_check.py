"""Hand check for tools/steam_review_coder.py, as PLAYERS.md (12 Oct 2026) did it.

sample <game> <reviews.jsonl> <set> <n> <seed> [--exclude set1,set2]
    writes F:/LedgerTools/steam-reviews/hand/<set>.jsonl: n random reviews of 8+ words,
    none from the excluded sets (so a test set is fresh).
score <set> [<set> ...]
    compares the coder's tags with <set>-hand.json: of every 100 script tags how many
    the hand reading has (precision), of every 100 hand tags how many the script found
    (recall), set-aside agreement, and Spearman rank correlation of theme order.
"""
import json, os, random, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from steam_review_coder import code

HAND = "F:/LedgerTools/steam-reviews/hand"


def sample(game, src, name, n, seed, exclude):
    os.makedirs(HAND, exist_ok=True)
    used = set()
    for e in exclude:
        for l in open(f"{HAND}/{e}.jsonl", encoding="utf-8"):
            used.add(json.loads(l)["id"])
    rows = [json.loads(l) for l in open(src, encoding="utf-8")]
    rows = [r for r in rows if len(r.get("review", "").split()) >= 8 and r["recommendationid"] not in used]
    random.Random(seed).shuffle(rows)
    with open(f"{HAND}/{name}.jsonl", "w", encoding="utf-8") as f:
        for r in rows[:n]:
            f.write(json.dumps({"id": r["recommendationid"], "game": game, "voted_up": r["voted_up"],
                                "text": r["review"]}, ensure_ascii=False) + "\n")
    print(f"{name}: {min(n, len(rows))} reviews")


def spearman(a, b):
    keys = sorted(set(a) | set(b))
    if len(keys) < 3:
        return float("nan")
    def ranks(c):
        order = sorted(keys, key=lambda k: -c.get(k, 0))
        r, i = {}, 0
        while i < len(order):  # average ranks for ties
            j = i
            while j + 1 < len(order) and c.get(order[j + 1], 0) == c.get(order[i], 0):
                j += 1
            for k in order[i:j + 1]:
                r[k] = (i + j) / 2
            i = j + 1
        return r
    ra, rb = ranks(a), ranks(b)
    n = len(keys)
    ma, mb = sum(ra.values()) / n, sum(rb.values()) / n
    cov = sum((ra[k] - ma) * (rb[k] - mb) for k in keys)
    va = sum((ra[k] - ma) ** 2 for k in keys) ** 0.5
    vb = sum((rb[k] - mb) ** 2 for k in keys) ** 0.5
    return cov / (va * vb) if va and vb else float("nan")


def score(sets):
    tp = sp = hp = agree = total = 0
    cs = {"praise": Counter(), "punish": Counter()}
    ch = {"praise": Counter(), "punish": Counter()}
    for s in sets:
        hand = json.load(open(f"{HAND}/{s}-hand.json", encoding="utf-8"))
        for l in open(f"{HAND}/{s}.jsonl", encoding="utf-8"):
            r = json.loads(l)
            h = hand.get(r["id"])
            if h is None:
                continue
            c = code({"review": r["text"], "voted_up": r["voted_up"]})
            total += 1
            agree += bool(c["set_aside"]) == bool(h.get("set_aside"))
            for side in ("praise", "punish"):
                st = set(c[side]) if not c["set_aside"] else set()
                ht = set(h.get(side, [])) if not h.get("set_aside") else set()
                tp += len(st & ht); sp += len(st); hp += len(ht)
                cs[side].update(st); ch[side].update(ht)
    print(f"sets {','.join(sets)}: {total} reviews")
    print(f"  of 100 script tags, {100*tp/max(sp,1):.0f} match the hand reading (precision)")
    print(f"  of 100 hand tags, the script found {100*tp/max(hp,1):.0f} (recall)")
    print(f"  set-aside agreement {agree} of {total}")
    for side in ("praise", "punish"):
        print(f"  rank correlation {side}: {spearman(cs[side], ch[side]):.2f}"
              f" over {len(set(cs[side]) | set(ch[side]))} themes")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "sample":
        ex = a[a.index("--exclude") + 1].split(",") if "--exclude" in a else []
        sample(a[1], a[2], a[3], int(a[4]), int(a[5]), ex)
    else:
        score(a[1:])
