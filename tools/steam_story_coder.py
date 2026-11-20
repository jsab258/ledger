"""Code what Steam reviewers say about a game's STORY, by sub-theme (advisor 276, 20 Nov 2026).

Method (setting-free), as the players study's coder: split each review into clauses; drop
clauses about the online side; a review speaks about the story when a clause matches the
story net; each story clause takes the sub-themes whose words it matches; praise or
complaint from the shared word lists with the flip, a side-less clause taking the thumb.
Complaint sub-themes that carry their own side (predictable, rushed ending, padded, plot
holes...) count as complaints whatever the side words say. Names: capitalised words in
praised character clauses, counted, common words removed.

Usage: python tools/steam_story_coder.py <reviews.jsonl> <out.json> [--names Arthur,Dutch]
       python tools/steam_story_coder.py sample <game> <reviews.jsonl> <set> <n> <seed>   # story-tagged only
       python tools/steam_story_coder.py score <set> [<set> ...]
"""
import json, os, random, re, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
import steam_review_mech  # widens the frozen coder's set-aside words, as for the walkthrough games
C = steam_review_mech.C
P = C.P

NET = P(r"\b(story|stories|storyline|plot|narrative|writing|written|characters?(?! (creat\w*|customi[sz]\w*|models?|editor|slots?))|protagonists?|villains?|antagonists?|ending|endings|dialogue|twists?)\b")
# Tuned once on 50 hand-read GTA V story-net reviews (tune-story-gtav, 20 Nov 20:40): missions,
# quests, campaign, cutscenes and character customisation left the net (15 of 50 spoke of the story).

PRAISE = {
    "characters": P(r"\b(characters?(?! (creat\w*|customi[sz]\w*|models?|editor|slots?))|cast|protagonists?|companions?|lovable|likeable|likable|memorable characters?|character development)\b"),
    "lead_changes": P(r"\b(character (arc|development|growth)|arc|redemption|grows?|growth|changes? (as|over)|transformation)\b"),
    "villain": P(r"\b(villains?|antagonists?|bad guys?|big bad)\b"),
    "moments": P(r"\b(cried|tears?|emotional|heart ?break\w*|gut[- ]?punch\w*|chills|goosebumps|hit (me )?hard|moving|touching|powerful|unforgettable|memorable (moments?|scenes?))\b"),
    "writing": P(r"\b(writing|written|dialogue|script|lines|conversations?|voice acting|banter)\b"),
    "humour": P(r"\b(funny|humou?r|hilarious|satire|satirical|jokes?|witty|comedy)\b"),
    "twist": P(r"\b(twists?|surpris\w*|unexpected|didn'?t see (it|that) coming|plot twist)\b"),
    "ending": P(r"\b(ending|endings|finale|conclusion|epilogue)\b"),
    "side_stories": P(r"\b(side (quests?|missions?|stories|content)|strangers?|side characters?)\b"),
    "missions_tell": P(r"\b(missions?|quests?|set pieces?|heists?|cases?|investigat\w*|interrogat\w*)\b.{0,60}\b(story|plot|narrative|tells?|told)\b|\b(story|plot|narrative)\b.{0,60}\b(missions?|quests?|heists?|cases?)\b"),
}
PUNISH = {
    "predictable": P(r"\b(predictable|clich[eé]\w*|generic|tropes?|seen it before|formulaic|by the numbers)\b"),
    "rushed_ending": P(r"\b(rushed|abrupt|unsatisfying|weak|bad|terrible|disappointing|stupid|lame) (ending|endings|finale|conclusion)\b|\bending (was|is|felt) (rushed|abrupt|weak|bad|terrible|disappointing|unsatisfying)\b"),
    "padded_middle": P(r"\b(padd?(ed|ing)|drags?|dragged|slow (start|beginning|middle|paced?|pacing)|pacing|filler|boring (story|middle|missions?)|takes forever)\b"),
    "thin_villain": P(r"\b(villains?|antagonists?|bad guys?)\b"),
    "flat_lead": P(r"\b(protagonist|main character|lead|hero)\b"),
    "on_rails": P(r"\b(on rails|linear|railroad\w*|scripted|follow (the|a) (car|line|marker)|instant fail|mission fail\w*|fail(ed)? the mission|restrictive missions?|my way)\b"),
    "too_much_talk": P(r"\b(too (many|much|long) (cutscenes?|talking|dialogue|walking)|cutscenes? (are|were) (too )?long|unskippable|walk and talk|interactive movie|movie)\b"),
    "plot_holes": P(r"\b(plot holes?|makes? no sense|nonsens\w*|contrived|inconsisten\w*|ludonarrative)\b"),
    "tone_clash": P(r"\b(tone|tonal|ludonarrative dissonance|mood whiplash|takes itself too seriously|edgy)\b"),
    "side_better": P(r"\b(side (quests?|missions?|stories|content) (are|were|is) better|better than the main (story|quest|plot))\b"),
    "too_short": P(r"\b(too short|short (story|campaign|game)|only (\d+|a few) hours|over too (soon|quickly))\b"),
    "thin_story": P(r"\b(story|plot|narrative|writing)\b"),
}
OWN_SIDE = {"predictable", "rushed_ending", "padded_middle", "on_rails", "too_much_talk", "plot_holes", "side_better", "too_short"}
STOP = set("The I It This That He She They We You A An And But So If In On Of To As At By For Or Not My His Her Their Its Game Story GTA RDR Red Dead Rockstar Steam PC Online Kingdom Come Deliverance Hitman Watch Dogs Sleeping Noire Grand Theft Auto Definitive Edition Complete World Assassination Legion Los Angeles Hong Kong Liberty City Santos Bohemia Henry".split())


def clauses(text):
    text = re.sub(r"\bstory[- ]?mode\b", "campaign", text, flags=re.I)
    return [s for s in C.sentences(text) if not (C.ONLINE.search(s) and not C.GAME_WORDS.search(s))]


def code(review):
    cl = clauses(review.get("review", ""))
    hit = [s for s in cl if NET.search(s)]
    if not hit:
        return None
    up = review.get("voted_up")
    pr, pu, q, names = set(), set(), [], Counter()
    for s in hit:
        sd = C.side(s)
        own = [k for k in OWN_SIDE if PUNISH[k].search(s)]
        pu.update(own)
        if sd is None and up is not None:
            sd = "praise" if up else "punish"
        if sd == "praise":
            ks = [k for k, rx in PRAISE.items() if rx.search(s)] or ["story_general"]
            pr.update(ks)
            if "characters" in ks:
                names.update(w for w in re.findall(r"(?<=[a-z,] )[A-Z][a-z]{2,}\b", s) if w not in STOP)
        elif sd == "punish":
            ks = [k for k, rx in PUNISH.items() if rx.search(s) and k not in OWN_SIDE] or ([] if own else ["story_general"])
            pu.update(ks)
        if sd and 6 <= len(s.split()) <= 30:
            q.append((sd, s.strip()))
    return {"praise": sorted(pr), "punish": sorted(pu), "q": q[:2], "names": dict(names)}


def main(a):
    src, dst = a[0], a[1]
    rows = [json.loads(l) for l in open(src, encoding="utf-8")]
    res, pc, nc, names = {}, Counter(), Counter(), Counter()
    quotes = {}
    aside = speak = 0
    for r in rows:
        g = C.code(r)
        if g["set_aside"]:
            aside += 1; continue
        c = code(r)
        if c is None:
            continue
        speak += 1
        res[r["recommendationid"]] = {k: c[k] for k in ("praise", "punish")}
        pc.update(c["praise"]); nc.update(c["punish"]); names.update(c["names"])
        for sd, s in c["q"]:
            for k in (c["praise"] if sd == "praise" else c["punish"]):
                quotes.setdefault(f"{sd}:{k}", []).append((r["recommendationid"], s))
    rng = random.Random(276)
    for k in quotes:
        rng.shuffle(quotes[k]); quotes[k] = quotes[k][:6]
    kept = len(rows) - aside
    json.dump({"source": src, "reviews": len(rows), "set_aside": aside, "kept": kept, "speak": speak,
               "praise": dict(pc), "punish": dict(nc), "names": dict(names.most_common(15)),
               "quotes": quotes, "tags": res}, open(dst, "w", encoding="utf-8"))
    print(f"reviews {len(rows)}, set aside {aside}, kept {kept}, speak about the story {speak} ({100*speak/max(kept,1):.1f}%)")
    for nm, c in (("PRAISE", pc), ("PUNISH", nc)):
        print(nm)
        for k, n in c.most_common():
            print(f"  {k:15s} {n:6d}  {100*n/max(speak,1):5.1f}%")
    print("NAMES", ", ".join(f"{k} {n}" for k, n in names.most_common(10)))


def sample(game, src, name, n, seed):
    H = "F:/LedgerTools/steam-reviews/hand"
    rows = [json.loads(l) for l in open(src, encoding="utf-8")]
    rows = [r for r in rows if len(r.get("review", "").split()) >= 8 and not C.code(r)["set_aside"] and code(r)]
    random.Random(seed).shuffle(rows)
    with open(f"{H}/{name}.jsonl", "w", encoding="utf-8") as f:
        for r in rows[:n]:
            f.write(json.dumps({"id": r["recommendationid"], "game": game, "voted_up": r["voted_up"],
                                "text": r["review"][:4000]}, ensure_ascii=False) + "\n")
    print(f"{name}: {min(n, len(rows))} story-tagged reviews")


def score(sets):
    H = "F:/LedgerTools/steam-reviews/hand"
    tp = sp = hp = 0
    per = Counter()
    for s in sets:
        hand = json.load(open(f"{H}/{s}-hand.json", encoding="utf-8"))
        for l in open(f"{H}/{s}.jsonl", encoding="utf-8"):
            r = json.loads(l)
            h = hand.get(r["id"])
            if h is None:
                continue
            c = code({"review": r["text"], "voted_up": r["voted_up"]}) or {"praise": [], "punish": []}
            for side in ("praise", "punish"):
                st, ht = set(c[side]) - {"story_general"}, set(h.get(side, []))
                tp += len(st & ht); sp += len(st); hp += len(ht)
                for k in st | ht:
                    per[f"{side}:{k}:script"] += k in st; per[f"{side}:{k}:hand"] += k in ht; per[f"{side}:{k}:both"] += k in st and k in ht
    print(f"sets {','.join(sets)}: precision {100*tp/max(sp,1):.0f}, recall {100*tp/max(hp,1):.0f}")
    for key in sorted({k.rsplit(':', 1)[0] for k in per}):
        print(f"  {key:28s} script {per[key+':script']:3d} hand {per[key+':hand']:3d} both {per[key+':both']:3d}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "sample":
        sample(a[1], a[2], a[3], int(a[4]), int(a[5]))
    elif a[0] == "score":
        score(a[1:])
    else:
        main(a)
