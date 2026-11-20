"""Code Steam reviews by theme, praise or punish, the way PLAYERS.md (12 Oct 2026) did.

Method (setting-free): split each review into sentences, then clauses (at but,
however, although, though, while, whereas, semicolons); a clause takes a theme when
its words match the theme's pattern; praise or complaint comes from word lists with
a flip for not/never/no; a clause that names a theme with no clear side takes the
review's thumb, for themes where that is usually right, only in reviews with no
online talk. Clauses about the online side (and not the game) are dropped.
Set aside whole, on two grounds: (a) no clause left that names a theme or the game;
(b) no theme found and an online or off-topic word anywhere (company, mods, keys...).

Theme names follow the players study (production/research/lane/PLAYERS-KCD2-GTAV-
RDR2-2026-11-20.md on lane-2026-11): the twenty of each that rank, plus 'freedom'.
Frozen 20 Nov 2026 17:30 (logic hash 758ebc14 before this description was edited).

Usage: python tools/steam_review_coder.py <reviews.jsonl> <out.json> [--game gtav|rdr2]
Writes per-review tags (out.json) and prints counts per theme.
"""
import json, re, sys
from collections import Counter

P = lambda s: re.compile(s, re.I)

PRAISE = {
    "story": P(r"\b(story|stories|storyline|plot|narrative|writing|written|characters?|protagonists?|arthur|dutch|john marston|michael|franklin|trevor|cast of characters|character development|emotional)\b"),
    "looks": P(r"\b(graphics|visuals?|beautiful|gorgeous|stunning|looks? (amazing|great|incredible|good)|scenery|landscapes?|lighting|sunsets?|breathtaking|art ?style|eye candy|photo ?realistic|detailed)\b"),
    "world": P(r"\b(open world|world|immersi\w+|alive|living|atmosphere|believable|lived[- ]in|npcs?|city|los santos|towns?|wildlife|animals|details?|attention to detail)\b"),
    "side": P(r"\b(side (quests?|missions?|content|activities|stories)|strangers?|random encounters?|encounters|activities)\b"),
    "music": P(r"\b(music|soundtrack|score|radio|sound design|audio|songs?)\b"),
    "ranwell": P(r"\b(runs? (well|great|smooth\w*|fine|perfectly)|optimi[sz]\w*|good port|great port|performance|60 ?fps|smooth)\b"),
    "price": P(r"\b(worth (it|every|the (money|price))|value|price|on sale|bang for|hours of (content|gameplay|fun)|for the money|cheap)\b"),
    "voice": P(r"\b(voice acting|voice actors?|performances?|acting|voiced)\b"),
    "humour": P(r"\b(funny|humou?r|hilarious|satire|satirical|jokes?|laugh\w*|comedy)\b"),
    "polish": P(r"\b(polish\w*|no bugs|bug[- ]free|few bugs|stable)\b"),
    "choices": P(r"\b(choices?|honou?r system|consequences?|roleplay\w*|role[- ]play\w*|decisions?)\b"),
    "skills": P(r"\b(crafting|upgrades?|skills?|perks?|level(l)?ing up|progression)\b"),
    "driving": P(r"\b(driving|cars?|horses?|riding|vehicles?|handling|flying|planes?)\b"),
    "slowburn": P(r"\b(slow[- ]?(burn|paced?|pacing)|cinematic|cutscenes?|takes? its time)\b"),
    "gunfights": P(r"\b(gun ?fights?|gunplay|shoot(ing|outs?)|combat)\b"),
    "reacts": P(r"\b(react\w*|remember\w*|notice\w*|witness\w*|reputation|wanted system|bounty)\b"),
    "ending": P(r"\b(ending|endings|epilogue|finale|the end)\b"),
    "freedom": P(r"\b(freedom|sandbox|do whatever|whatever you want|so much to do|lots to do|heists?|switch(ing)? between|three (protagonists|characters|leads)|mess(ing)? around|chaos|crimes?|things to do|endless|do anything|explor\w*|everything is here)\b"),
}
PUNISH = {
    "controls": P(r"\b(controls?|menus?|camera|clunky|animations?|slow (walk\w*|animation\w*|loot\w*)|looting|skinning|interface|ui|keybind\w*|input lag|sluggish|unresponsive)\b"),
    "boring": P(r"\b(boring|bored|dull|tedious|nothing to do|slow travel|travel(l)?ing|riding for|empty)\b"),
    "story": P(r"\b(story|plot|writing|characters?|protagonists?|predictable|clich\w*|rushed|unlikable|unlikeable)\b"),
    "bugs": P(r"\b(bugs?|buggy|glitch\w*|broken|soft[- ]?lock\w*)\b"),
    "cutscenes": P(r"\b(cutscenes?|slow (start|opening|beginning)|prologue|too much talk\w*|dialogue heavy|chapter (1|one|2|two)|first (few|\d+) hours)\b"),
    "loop": P(r"\b(repetiti\w*|same thing|over and over|copy[- ]paste|grind\w*|formulaic|rinse and repeat)\b"),
    "price": P(r"\b(overpriced|too expensive|not worth|full price|price|refund\w*|too short|short)\b"),
    "port": P(r"\b(crash\w*|stutter\w*|fps|frame ?rate|lag\w*|performance|unoptimi[sz]ed|optimi[sz]ation|port|loading|long loads?|load times?|storage|\d+ ?gbs?|freez\w*|hardware|gpu|vram)\b"),
    "missions": P(r"\b(missions?|mission design|fail(ed|s)? (the )?mission|on rails|restrictive|forced to|hand[- ]holding|follow the (yellow|marker))\b"),
    "survival": P(r"\b(eat(ing)?|hunger|sleep\w*|wash\w*|bath\w*|horse care|feeding|cores?|weight|survival)\b"),
    "hollow": P(r"\b(hollow|shallow|dead world|lifeless|rules|bounty (system)?|wanted (level|system)|witness\w*)\b"),
    "difficulty": P(r"\b(difficult\w*|too hard|too easy|unfair|frustrat\w*)\b"),
    "linear": P(r"\b(linear|interactive movie|walking simulator|empty map|on rails)\b"),
    "gunplay": P(r"\b(gunplay|auto[- ]?aim|aim assist|aiming|shooting|dead ?eye)\b"),
    "saves": P(r"\b(save system|saves?|saving|checkpoints?|autosave)\b"),
    "unexplained": P(r"\b(tutorial|not explained|never explained|no explanation|confusing|unclear)\b"),
    "paid": P(r"\b(microtransactions?|shark cards?|dlc|story (dlc|expansion)|single[- ]player (dlc|content|expansion)|abandon\w*|cash grab)\b"),
    "dated": P(r"\b(dated|outdated|old graphics|looks? (bad|old|dated|ugly)|ugly|blurry|taa)\b"),
    "stealth": P(r"\b(stealth)\b"),
}
# Themes where a side-less mention takes the review's vote (as on 12 Oct).
VOTE_SIDE = {"story", "looks", "world", "music", "voice", "ending", "freedom", "controls",
             "boring", "bugs", "port", "loop", "missions"}

POS = P(r"\b(banger|classic|holds? up|addictive|goated|good|great|amazing|awesome|best|love\w*|beautiful|fantastic|excellent|incredible|masterpiece|perfect\w*|brilliant|enjoy\w*|fun|well|solid|wonderful|outstanding|gorgeous|stunning|impressive|recommend\w*|favou?rite|nice|immersive|alive|worth|smooth|memorable|top notch|peak|goat|10/10)\b")
NEG = P(r"\b(bad|worst|terrible|awful|hate\w*|boring|annoying|poor|clunky|broken|buggy|slow|tedious|frustrat\w*|horrible|garbage|trash|mediocre|disappoint\w*|crash\w*|stutter\w*|sucks?|problem\w*|issues?|lag\w*|waste|overpriced|unplayable|meh|dull|repetitive|janky|ruin\w*|annoy\w*|forced|awkward|too (long|much|short|slow))\b")
FLIP = P(r"\b(not|never|no|n't|isn't|wasn't|doesn't|didn't|aren't|hardly|without)\b")

ONLINE = P(r"\b(gta ?online|red dead online|rdo|online mode|multiplayer|modders?|hackers?|cheaters?|anti[- ]?cheat|battleye|launcher|social club|rockstar games launcher|account|ban(ned)?|shark cards?|griefers?|lobby|lobbies|review ?bomb\w*|epic games|online)\b")
OFFTOPIC = P(r"\b(rockstar|take[- ]?two|mods?|modding|modders?|community|greed\w*|support|g2a|linux|steam deck|email|drm|key|refund)\b")
GAME_WORDS = P(r"\b(story|single[- ]?player|campaign|offline|missions?|characters?|world|graphics)\b")


def sentences(t):
    """Sentences, then clauses at but/however/although/while/whereas and ; so a
    sentence like 'the story is great but online is a joke' keeps its first half."""
    out = []
    for s in re.split(r"(?<=[.!?\n])\s+|\n+", t):
        out += [c for c in re.split(r"\b(?:but|however|although|though|while|whereas)\b|;", s, flags=re.I)
                if c and c.strip()]
    return out


def any_theme(s):
    return any(rx.search(s) for rx in PRAISE.values()) or any(rx.search(s) for rx in PUNISH.values())


def side(s):
    pos, neg = len(POS.findall(s)), len(NEG.findall(s))
    if FLIP.search(s):
        pos, neg = neg, pos
    return "praise" if pos > neg else "punish" if neg > pos else None


def code(review):
    text, up = review.get("review", ""), review.get("voted_up")
    # 'story mode' names a mode, not the story: match it as the campaign.
    text = re.sub(r"\bstory[- ]?mode\b", "campaign", text, flags=re.I)
    sents = sentences(text)
    # A clause naming the online side is dropped unless it also names the story game.
    on = [s for s in sents if ONLINE.search(s) and not GAME_WORDS.search(s)]
    kept = [s for s in sents if s not in on]
    set_aside = len(on) > 0 and not any(any_theme(s) or GAME_WORDS.search(s) for s in kept)
    tags = {"praise": set(), "punish": set()}
    if set_aside:
        return {"set_aside": True, "mixed": False, "praise": [], "punish": []}
    # The thumb decides a side-less mention only in reviews wholly about the game.
    use_vote = not on
    for s in kept:
        sd = side(s)
        for th, rx in PRAISE.items():
            if rx.search(s) and (sd == "praise" or (sd is None and use_vote and up and th in VOTE_SIDE)):
                tags["praise"].add(th)
        for th, rx in PUNISH.items():
            if rx.search(s) and (sd == "punish" or (sd is None and use_vote and not up and th in VOTE_SIDE)):
                tags["punish"].add(th)
    if not tags["praise"] and not tags["punish"] and (on or OFFTOPIC.search(text)):
        return {"set_aside": True, "mixed": False, "praise": [], "punish": []}
    return {"set_aside": False, "mixed": bool(on), "praise": sorted(tags["praise"]),
            "punish": sorted(tags["punish"])}


def main():
    src, out = sys.argv[1], sys.argv[2]
    rows = [json.loads(l) for l in open(src, encoding="utf-8")]
    res, pc, nc = {}, Counter(), Counter()
    aside = mixed = 0
    for r in rows:
        c = code(r)
        res[r["recommendationid"]] = c
        aside += c["set_aside"]; mixed += c["mixed"]
        if not c["set_aside"]:
            pc.update(c["praise"]); nc.update(c["punish"])
    kept = len(rows) - aside
    json.dump({"source": src, "reviews": len(rows), "set_aside": aside, "mixed": mixed,
               "kept": kept, "praise": dict(pc), "punish": dict(nc), "tags": res},
              open(out, "w", encoding="utf-8"))
    print(f"reviews {len(rows)}, set aside {aside}, mixed {mixed}, kept {kept}")
    for name, c in (("PRAISE", pc), ("PUNISH", nc)):
        print(name)
        for th, n in c.most_common():
            print(f"  {th:12s} {n:6d}  {100*n/max(kept,1):5.1f}%")


if __name__ == "__main__":
    main()
