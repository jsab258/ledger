"""Code Steam reviews twice: the players study's theme list, and one mechanic list.

Advisor 273 (20 Nov 2026): for each walkthrough game, the general themes (the frozen
coder, tools/steam_review_coder.py, logic unchanged) and what reviewers say about the
mechanic the game is studied for: driving, fists, on foot, being seen, chases.

Set-aside words are widened for games outside GTA V and RDR2 (their launchers, online
services and DRM: Games for Windows Live, Ubisoft Connect, always-online): the frozen
coder's ONLINE and OFFTOPIC patterns are extended at run time, nothing else changes.

Mechanic method (setting-free): split as the frozen coder does; a clause names the
mechanic when it matches the mechanic's words; a sub-point when it also matches the
sub-point's words; praise or complaint from the same word lists and flip. A mention
with no side takes the review's thumb (no quote). Short quotes (6 to 30 words) are kept, ten a side.

Tuned once on 80 hand-read GTA V reviews (tune-mech-gtav), frozen 20 Nov 2026 18:25.

Usage: python tools/steam_review_mech.py <reviews.jsonl> <out.json> --mech driving,chases
       python tools/steam_review_mech.py sample <game> <reviews.jsonl> <set> <n> <seed> --mech m1,m2
       python tools/steam_review_mech.py score <set> [<set> ...] --mech m1,m2
Prints general counts (as the frozen coder) and per mechanic: reviews mentioning it,
praise and complaint shares of kept reviews, sub-points.
"""
import json, random, re, sys
from collections import Counter
import os
sys.path.insert(0, os.path.dirname(__file__))
import steam_review_coder as C

P = C.P
C.ONLINE = P(C.ONLINE.pattern[:-3] + r"|games for windows( live)?|gfwl|ubisoft connect|uplay|ubi ?connect|always[- ]online|denuvo|xbox (app|live)|microsoft store|elusive targets?|servers?)\b")
C.OFFTOPIC = P(C.OFFTOPIC.pattern[:-3] + r"|ubisoft|ubi|microsoft|io ?interactive|ioi|2k|square enix|delist\w*|price hike|bundle|dlc pass|re-?buy)\b")

MECH = {
    "driving": (P(r"\b(driving|drives? like|cars? ?: ?\d+|handling|handles? (well|badly|like|great|poorly|nicely)|steering|drift\w*|car physics|vehicle physics|driving physics|cars? (feel|handle|drive|controls?)|races?|racing)\b"), {
        "handling": P(r"\b(handling|handles?|steering|grip|drift\w*|controls?|turn(ing)?|brak\w*|feel)\b"),
        "weight": P(r"\b(weight\w*|heavy|floaty|boat\w*|sway\w*|body roll|suspension|physics|momentum|slid\w*|ice)\b"),
        "crashes": P(r"\b(crash(es|ing)? into|collisions?|damage|wreck\w*|deform\w*|smash\w*|traffic)\b"),
        "camera": P(r"\b(camera|view|cockpit|first[- ]person)\b"),
        "cars": P(r"\b(car list|selection|variety|classic cars?|old cars?|period cars?|sound of|engine sounds?)\b"),
    }),
    "fists": (P(r"\b(combat|melee|fist\w*|fights?|fighting|punch\w*|brawl\w*|kung ?fu|martial arts?|counters?|combos?|hand[- ]to[- ]hand)\b"), {
        "counters": P(r"\b(counters?|countering|parry|block\w*|timing)\b"),
        "combos": P(r"\b(combos?|moves?|grapple\w*|throws?|takedowns?)\b"),
        "environment": P(r"\b(environment\w*|environmental|objects?|surroundings)\b"),
        "impact": P(r"\b(impact|weight\w*|brutal\w*|satisfying|crunch\w*|visceral|animations?)\b"),
        "difficulty": P(r"\b(easy|hard|difficult\w*|challeng\w*|button[- ]mash\w*|mash\w*|repetitive)\b"),
    }),
    "onfoot": (P(r"\b(on foot|walking around|walking speed|movement|parkour|climb\w*|free ?running|sprint\w*|character controls?|walks? like|runs? like)\b"), {
        "weight": P(r"\b(weight\w*|heavy|sluggish|clunky|floaty|momentum|realistic|euphoria|ragdoll|physics)\b"),
        "responsive": P(r"\b(responsive|smooth|fluid|controls?|precise|tight|snappy|stiff)\b"),
        "parkour": P(r"\b(parkour|climb\w*|vault\w*|free ?running|jump\w*)\b"),
        "camera": P(r"\b(camera|view)\b"),
    }),
    "seen": (P(r"\b(stealth|sneak\w*|disguises?|detect\w*|spotted|seen|suspicio\w*|blend\w*|noticed|witness\w*|guards?|ai|npcs?|social stealth)\b"), {
        "disguise": P(r"\b(disguises?|outfits?|costumes?|enforcers?|blend\w*)\b"),
        "detection": P(r"\b(detect\w*|spotted|seen|noticed|suspicio\w*|witness\w*|alert\w*|line of sight)\b"),
        "ai": P(r"\b(ai|guards?|npcs?|routines?|patterns?)\b"),
        "fair": P(r"\b(fair|unfair|cheap|psychic|omniscient|clear|readable|instinct)\b"),
        "freedom": P(r"\b(sandbox|creative|freedom|options?|approach\w*|ways? to)\b"),
    }),
    "chases": (P(r"\b(chases?|chasing|pursuits?|police|cops|wanted (level|system)|getaways?|escap\w*|flee\w*|tail(ing)?|follow missions?)\b"), {
        "foot": P(r"\b(foot chases?|on foot|running|tackl\w*|parkour)\b"),
        "car": P(r"\b(car chases?|driving|cars?|vehicles?|ram\w*)\b"),
        "police": P(r"\b(police|cops|wanted|stars?|heat)\b"),
        "scripted": P(r"\b(scripted|rubber[- ]?band\w*|on rails|cutscene|fail\w*|instant fail|lose them|lost them)\b"),
    }),
}


def mech_code(review, mechs):
    sents = C.sentences(re.sub(r"\bstory[- ]?mode\b", "campaign", review.get("review", ""), flags=re.I))
    out = {}
    for m in mechs:
        rx, subs = MECH[m]
        # A clause about the online side, not the game, is dropped (as the frozen coder does).
        hit = [s for s in sents if rx.search(s) and not (C.ONLINE.search(s) and not C.GAME_WORDS.search(s))]
        if not hit:
            continue
        d = {"praise": set(), "punish": set(), "mention": True, "q": []}
        # As the frozen coder does for some themes: a side-less mention takes the thumb,
        # judged per clause (an online clause is already dropped); such clauses give no quote.
        use_vote = True
        for s in hit:
            sd = C.side(s)
            if sd is None and use_vote and review.get("voted_up") is not None:
                d["praise" if review.get("voted_up") else "punish"].update(
                    [k for k, srx in subs.items() if srx.search(s)] or ["general"])
                continue
            sp = [k for k, srx in subs.items() if srx.search(s)] or ["general"]
            if sd:
                d[sd].update(sp)
                w = len(s.split())
                if 6 <= w <= 30:
                    d["q"].append((sd, s.strip()))
        out[m] = {"praise": sorted(d["praise"]), "punish": sorted(d["punish"]), "q": d["q"][:2]}
    return out


def main():
    a = sys.argv[1:]
    src, dst = a[0], a[1]
    mechs = a[a.index("--mech") + 1].split(",") if "--mech" in a else list(MECH)
    rows = [json.loads(l) for l in open(src, encoding="utf-8")]
    res, pc, nc = {}, Counter(), Counter()
    mm, mp, mn, sp, sn = Counter(), Counter(), Counter(), Counter(), Counter()
    quotes = {m: {"praise": [], "punish": []} for m in mechs}
    aside = mixed = 0
    for r in rows:
        c = C.code(r)
        c["mech"] = {} if c["set_aside"] else mech_code(r, mechs)
        res[r["recommendationid"]] = {k: v for k, v in c.items()}
        aside += c["set_aside"]; mixed += c["mixed"]
        if c["set_aside"]:
            continue
        pc.update(c["praise"]); nc.update(c["punish"])
        for m, d in c["mech"].items():
            mm[m] += 1
            if d["praise"]: mp[m] += 1
            if d["punish"]: mn[m] += 1
            sp.update(f"{m}:{k}" for k in d["praise"]); sn.update(f"{m}:{k}" for k in d["punish"])
            for sd, q in d["q"]:
                quotes[m][sd].append((r["recommendationid"], q))
    kept = len(rows) - aside
    rng = random.Random(273)
    for m in quotes:
        for sd in quotes[m]:
            rng.shuffle(quotes[m][sd]); quotes[m][sd] = quotes[m][sd][:10]
    json.dump({"source": src, "reviews": len(rows), "set_aside": aside, "mixed": mixed, "kept": kept,
               "praise": dict(pc), "punish": dict(nc),
               "mech": {m: {"mention": mm[m], "praise": mp[m], "punish": mn[m]} for m in mechs},
               "mech_sub_praise": dict(sp), "mech_sub_punish": dict(sn), "quotes": quotes, "tags": res},
              open(dst, "w", encoding="utf-8"))
    pct = lambda n: f"{100*n/max(kept,1):5.1f}%"
    print(f"reviews {len(rows)}, set aside {aside}, mixed {mixed}, kept {kept}")
    for name, c in (("PRAISE", pc), ("PUNISH", nc)):
        print(name)
        for th, n in c.most_common():
            print(f"  {th:12s} {n:6d}  {pct(n)}")
    for m in mechs:
        print(f"MECH {m}: mention {mm[m]} {pct(mm[m])}, praise {mp[m]} {pct(mp[m])}, punish {mn[m]} {pct(mn[m])}")
        for k in MECH[m][1].keys() | {"general"}:
            print(f"    {k:12s} praise {sp[m+':'+k]:5d}  punish {sn[m+':'+k]:5d}")


def score(sets, mechs):
    """Compare with the hand reading <set>-hand.json in F:/LedgerTools/steam-reviews/hand:
    general themes as steam_review_check.py does (with the widened set-aside), and per
    mechanic whether the review praises it and whether it punishes it."""
    H = "F:/LedgerTools/steam-reviews/hand"
    tp = sp = hp = agree = total = 0
    mt = {m: Counter() for m in mechs}
    for s in sets:
        hand = json.load(open(f"{H}/{s}-hand.json", encoding="utf-8"))
        for l in open(f"{H}/{s}.jsonl", encoding="utf-8"):
            r = json.loads(l)
            h = hand.get(r["id"])
            if h is None:
                continue
            rv = {"review": r["text"], "voted_up": r["voted_up"]}
            c = C.code(rv)
            mc = {} if c["set_aside"] else mech_code(rv, mechs)
            total += 1
            agree += bool(c["set_aside"]) == bool(h.get("set_aside"))
            for side in ("praise", "punish"):
                st = set(c[side]) if not c["set_aside"] else set()
                ht = set(h.get(side, [])) if not h.get("set_aside") else set()
                tp += len(st & ht); sp += len(st); hp += len(ht)
                for m in mechs:
                    a = bool(mc.get(m, {}).get(side))
                    b = bool((h.get("mech") or {}).get(m, {}).get(side)) and not h.get("set_aside")
                    mt[m]["tp"] += a and b; mt[m]["script"] += a; mt[m]["hand"] += b
    print(f"sets {','.join(sets)}: {total} reviews")
    print(f"  general: precision {100*tp/max(sp,1):.0f}, recall {100*tp/max(hp,1):.0f}, set-aside agreement {agree} of {total}")
    for m in mechs:
        t = mt[m]
        print(f"  {m}: script {t['script']}, hand {t['hand']}, both {t['tp']}: precision "
              f"{100*t['tp']/max(t['script'],1):.0f}, recall {100*t['tp']/max(t['hand'],1):.0f}")


# A broad net, wider than the coder's words, so a check sample holds enough mechanic talk.
NET = {
    "driving": P(r"\b(driv\w*|cars?|vehicles?|handling|steering|bikes?|racing|races?)\b"),
    "fists": P(r"\b(combat|melee|fist\w*|fight\w*|punch\w*|brawl\w*|kung ?fu|martial|counters?|combos?)\b"),
    "onfoot": P(r"\b(walk\w*|run(ning)?|sprint\w*|movement|parkour|climb\w*|jump\w*|on foot|animations?)\b"),
    "seen": P(r"\b(stealth|sneak\w*|disguis\w*|detect\w*|spotted|seen|suspic\w*|blend\w*|notic\w*|guards?|ai|npcs?)\b"),
    "chases": P(r"\b(chas\w*|pursu\w*|police|cops|wanted|escap\w*|flee\w*|tail\w*|follow\w*)\b"),
}


def sample(game, src, name, n, seed, mechs):
    """Half random reviews of 8+ words, half from those the broad net finds for the mechanics.
    Precision is read on the whole set; recall only against what the net lets in."""
    H = "F:/LedgerTools/steam-reviews/hand"
    rows = [json.loads(l) for l in open(src, encoding="utf-8")]
    rows = [r for r in rows if len(r.get("review", "").split()) >= 8]
    rng = random.Random(seed)
    rng.shuffle(rows)
    net = [r for r in rows if any(NET[m].search(r["review"]) for m in mechs)]
    pick, seen = [], set()
    for r in net[: n // 2] + rows:
        if len(pick) >= n:
            break
        if r["recommendationid"] not in seen:
            seen.add(r["recommendationid"]); pick.append(r)
    with open(f"{H}/{name}.jsonl", "w", encoding="utf-8") as f:
        for r in pick:
            f.write(json.dumps({"id": r["recommendationid"], "game": game, "voted_up": r["voted_up"],
                                "text": r["review"][:4000]}, ensure_ascii=False) + "\n")
    print(f"{name}: {len(pick)} reviews ({min(n // 2, len(net))} from the net)")


if __name__ == "__main__":
    if sys.argv[1] == "sample":
        a = sys.argv[2:]
        sample(a[0], a[1], a[2], int(a[3]), int(a[4]), a[a.index("--mech") + 1].split(","))
    elif sys.argv[1] == "score":
        a = sys.argv[2:]
        mechs = a[a.index("--mech") + 1].split(",")
        score([x for x in a[:a.index("--mech")]], mechs)
    else:
        main()
