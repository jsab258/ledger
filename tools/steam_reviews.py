"""Pull English Steam reviews for one game through Steam's public review interface.

Method copied from production/research/aaa-reference/PLAYERS.md (12 Oct 2026):
one request at a time, 3 to 8 s pause, five kinds of pull, overlaps removed by
recommendation id. Raw text goes outside the repository (default
F:/LedgerTools/steam-reviews/<app>/), never into git.

Usage: python tools/steam_reviews.py <appid> <release YYYY-MM-DD> [--out DIR] [--monthly N]
Writes reviews.jsonl (one review per line, with the pulls that found it),
totals.json (Steam's own counts) and pulls.json (rows per pull kind).
"""
import json, os, random, sys, time, datetime as dt, urllib.parse, urllib.request

# The old store.steampowered.com/appreviews address was retired on 22 Oct 2026
# (it now redirects to the store front). Valve's replacement, read in full
# 20 Nov 2026: https://partner.steamgames.com/doc/webapi/IUserReviewsService
# Same filters as enums in input_json; no key needed; HTTP 429 when rate-limited.
BASE = "https://api.steampowered.com/IUserReviewsService/GetAppReviews/v1/?"
UA = "research script; reads public review counts"
FILTER = {"all": 0, "recent": 1, "updated": 2}
VOTE = {"all": 0, "positive": 1, "negative": 2}


def get(app, params, tries=4):
    q = {"appid": int(app), "languages": ["english"], "purchase_type": 1, "num_per_page": 100}
    for k, v in params.items():
        if k == "filter":
            q["filter"] = FILTER[v]
        elif k == "review_type":
            q["review_type"] = VOTE[v]
        elif k == "language":
            q["languages"] = [v]
        elif k == "cursor":
            q["cursor"] = v
        else:
            q[k] = int(v)
    url = BASE + urllib.parse.urlencode({"input_json": json.dumps(q)})
    for k in range(tries):
        time.sleep(random.uniform(3, 8))
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8")).get("response", {})
        except Exception as e:  # network or 429: wait longer, try again
            print(f"  retry {k+1} after {e}", flush=True)
            time.sleep(20 * (k + 1))
    return {"reviews": []}


def pull(app, kind, want, params, store):
    """Page through one list with cursors until `want` reviews or the list ends."""
    cursor, got, seen_cursors = "*", 0, set()
    while got < want:
        p = dict(params, cursor=cursor)
        d = get(app, p)
        revs = d.get("reviews") or []
        if not revs:
            break
        for r in revs:
            rid = r["recommendationid"]
            if rid not in store:
                store[rid] = dict(r, pulls=[])
            if kind not in store[rid]["pulls"]:
                store[rid]["pulls"].append(kind)
            got += 1
            if got >= want:
                break
        cursor = d.get("cursor")
        if not cursor or cursor in seen_cursors:
            break
        seen_cursors.add(cursor)
    print(f"{kind}: {got}  (pool {len(store)})", flush=True)
    return got


def ts(d):
    return int(dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc).timestamp())


def main():
    a = sys.argv[1:]
    app = a[0]
    rel = dt.date.fromisoformat(a[1])
    out = a[a.index("--out") + 1] if "--out" in a else f"F:/LedgerTools/steam-reviews/{app}"
    monthly = int(a[a.index("--monthly") + 1]) if "--monthly" in a else 100
    os.makedirs(out, exist_ok=True)
    store, rows = {}, {}
    if "--weeks-only" in a:
        # Add the five early weeks to an existing pull (the Steam release can come
        # after the first PC release, as RDR2's did: 5 Dec 2019, not 5 Nov).
        for l in open(f"{out}/reviews.jsonl", encoding="utf-8"):
            r = json.loads(l); store[r["recommendationid"]] = r
        rows = json.load(open(f"{out}/pulls.json"))
        for vote in ("positive", "negative"):
            for w in range(5):
                s = rel + dt.timedelta(days=7 * w)
                e = s + dt.timedelta(days=7)
                rows[f"week{w+1}_{vote}"] = pull(app, f"week{w+1}_{vote}", 100,
                    {"filter": "all", "review_type": vote, "day_range": 0,
                     "date_range_start": ts(s), "date_range_end": ts(e) - 1}, store)
        json.dump(rows, open(f"{out}/pulls.json", "w"), indent=1)
        with open(f"{out}/reviews.jsonl", "w", encoding="utf-8") as f:
            for r in store.values():
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        pos = sum(1 for r in store.values() if r.get("voted_up"))
        print(f"DONE weeks app {app}: {len(store)} different reviews, {pos} positive, {len(store)-pos} negative", flush=True)
        return

    t = get(app, {"filter": "all", "review_type": "all", "num_per_page": "0"})
    tall = get(app, {"filter": "all", "review_type": "all", "num_per_page": "0", "language": "all"})
    json.dump({"english": t.get("query_summary"), "all_languages": tall.get("query_summary"),
               "read": dt.datetime.now().isoformat(timespec="minutes")},
              open(f"{out}/totals.json", "w"), indent=1)

    for vote in ("positive", "negative"):
        rows[f"default_helpful_{vote}"] = pull(app, f"default_helpful_{vote}", 600,
                                               {"filter": "all", "review_type": vote, "day_range": 0}, store)
        rows[f"recent_{vote}"] = pull(app, f"recent_{vote}", 500,
                                      {"filter": "recent", "review_type": vote}, store)
        rows[f"helpful_365_{vote}"] = pull(app, f"helpful_365_{vote}", 300,
                                           {"filter": "all", "review_type": vote, "day_range": "365"}, store)
        for w in range(5):
            s = rel + dt.timedelta(days=7 * w)
            e = s + dt.timedelta(days=7)
            rows[f"week{w+1}_{vote}"] = pull(app, f"week{w+1}_{vote}", 100,
                {"filter": "all", "review_type": vote, "day_range": 0,
                 "date_range_start": ts(s), "date_range_end": ts(e) - 1}, store)
        m = dt.date(rel.year, rel.month, 1)
        m = dt.date(m.year + (m.month // 12), m.month % 12 + 1, 1)  # month after launch
        today = dt.date.today()
        while m < today:
            n = dt.date(m.year + (m.month // 12), m.month % 12 + 1, 1)
            k = f"month_{m:%Y-%m}_{vote}"
            rows[k] = pull(app, k, monthly,
                {"filter": "all", "review_type": vote, "day_range": 0,
                 "date_range_start": ts(m), "date_range_end": ts(n) - 1}, store)
            m = n
        json.dump(rows, open(f"{out}/pulls.json", "w"), indent=1)
        with open(f"{out}/reviews.jsonl", "w", encoding="utf-8") as f:
            for r in store.values():
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    pos = sum(1 for r in store.values() if r.get("voted_up"))
    print(f"DONE app {app}: {len(store)} different reviews, {pos} positive, {len(store)-pos} negative", flush=True)


if __name__ == "__main__":
    main()
