#!/usr/bin/env python3
"""Score the panel's reviews with PLAYERS.md's forty themes, beside KCD2's and Mafia's shares.

PLAYERS.md's own scoring script is not in the repository, so its word lists are rebuilt here from the
theme names and descriptions (18 Nov 2026, the lane): a sentence carries a theme when it matches the
theme's words; it praises or punishes it by a short list of negative words (with a flip for "not",
"never", "no"); a sentence with neither takes the side of the review's thumb. Rough, like the original
(its frozen check matched a hand reading 53 to 65 times in 100); use the order, not the sizes.

Usage: python themes.py reviews.json   (a list of {"reviewer", "thumb": "up"|"down", "text", ...})
"""
import json
import re
import sys

# rank, name, KCD2 share %, Mafia share % (PLAYERS.md tables), words
PRAISE = [
    (1, "A story and characters worth caring about", 32.2, 47.5, r"story|stories|character|plot|writing|written|narrative"),
    (2, "How it looks", 17.8, 28.7, r"looks?|graphic|visual|beautiful|light(ing)?|pretty|art style"),
    (3, "A living, believable world", 24.5, 14.7, r"world|alive|living|believable|lived[- ]in|town|routine|react|watch(ing|es)?|remember|gossip"),
    (4, "Skill-based melee", 17.7, 5.0, r"melee|fist|punch|brawl|combat|fight"),
    (5, "Side quests that are whole stories", 13.7, 2.5, r"side quest|side stor|errand|quest"),
    (6, "It ran well", 7.8, 8.3, r"ran well|runs well|smooth|performance|frame ?rate|fps"),
    (7, "A fair price and length", 7.1, 8.7, r"price|worth|length|hours of"),
    (8, "Historical accuracy and period detail", 10.0, 5.7, r"period|1990|accura|authentic|histor|anachron|eighties|nineties|british"),
    (9, "Music and sound design", 4.7, 5.8, r"music|sound|audio|soundtrack"),
    (10, "Voice acting and performances", 3.8, 6.6, r"voice|acting|performance|accent|dialogue|lines"),
    (11, "Crafting, skills and perks", 8.9, 0.8, r"skill|perk|craft|level(ling|ing)? up|progress(ion)?"),
    (12, "Choices that change what happens", 7.1, 2.2, r"choice|choose|consequence|decision|matter"),
    (13, "The slow burn", 3.4, 5.5, r"slow burn|slow-burn|cinematic|atmosph|tension|tense|mood"),
    (14, "Stealth that works", 3.4, 4.5, r"stealth|sneak|unseen|lockpick|break[- ]in|witness"),
    (15, "Humour and a mix of tones", 4.7, 2.2, r"humou?r|funny|laugh|wit"),
    (16, "Gunfights that feel weighty", 0.4, 6.5, r"gun|shoot|pistol"),
    (17, "Driving that feels good", 0.6, 6.0, r"driv|car\b|cab|taxi|handling"),
    (18, "Polish", 4.5, 2.1, r"polish|bug[- ]free|clean launch|no bugs"),
    (19, "Challenge as a reward", 4.1, 1.6, r"challeng|hard but fair|difficult"),
    (20, "Knife duels", 0.8, 4.5, r"knife"),
]
PUNISH = [
    (1, "A thin or clichéd story", 8.3, 21.6, r"story|plot|clich|predictable|rushed|thin|writing"),
    (2, "Too short or not worth the price", 8.1, 19.6, r"short|price|expensive|worth|refund"),
    (3, "Clunky or unfair combat", 20.7, 6.4, r"combat|fight|clunky|melee|punch|brawl"),
    (4, "Slow opening, too much talk", 10.7, 14.0, r"talk|dialogue|cutscene|slow (start|opening)|opening|chat|conversation|yap|reading|text"),
    (5, "Boring, nothing to do for minutes", 10.9, 11.6, r"boring|bored|dull|flat|nothing (to do|happen)|waiting|wait(ed)?\b|empty minutes|idle|tedious"),
    (6, "Bugs that break the illusion", 15.6, 6.9, r"bug|glitch|broken|break(s)? the|repeat(s|ed|ing)? (the same|itself)|same line|stock line|word for word"),
    (7, "Stutter, crashes, loads", 4.6, 14.7, r"stutter|crash|load(ing)?|freeze|lag"),
    (8, "Linear, an interactive movie", 2.0, 17.2, r"linear|on rails|interactive movie|walking sim|corridor|empty map"),
    (9, "The same loop over and over", 6.8, 7.7, r"same (loop|thing)|repetit|over and over|grind"),
    (10, "A forced or abrupt ending", 1.7, 10.2, r"ending|abrupt"),
    (11, "Stealth that is thin", 3.5, 7.4, r"stealth|sneak"),
    (12, "Difficulty badly set", 5.9, 3.0, r"too hard|too easy|difficulty"),
    (13, "Boss fights that repeat", 0.5, 8.3, r"boss"),
    (14, "Quests that waste time or give no direction", 7.2, 1.5, r"no direction|where to go|lost|aimless|objective|errand|fetch|what to do"),
    (15, "A hollow world, rules on a whim", 4.0, 4.6, r"hollow|lifeless|fake|wooden|cardboard|npcs? (just|only)|same (few )?lines"),
    (16, "Weak gunplay", 0.5, 8.0, r"gun|shoot"),
    (17, "Menus, controls, camera, interface", 5.6, 2.6, r"menu|control|camera|interface|ui\b|prompt|keys?\b"),
    (18, "Racing and handling", 0.9, 6.1, r"racing|race|handling"),
    (19, "A save system that costs time", 5.7, 0.8, r"save system|saving"),
    (20, "Systems nobody explains", 5.0, 1.5, r"unexplained|not explained|no explanation|confus|no idea|tutorial|explain"),
]
NEG = re.compile(r"\b(bad|boring|dull|flat|clunky|broken|bug|glitch|repeat|repetitive|same|annoy|hate|worst|weak|thin|empty|nothing|tedious|slow|lost|confus|fake|wooden|lifeless|hollow|frustrat|awful|terrible|poor|lack|missing|never|no\b|not\b|isn't|doesn't|didn't|wasn't|can't|cannot|too (much|long|many|slow))", re.I)
POS = re.compile(r"\b(great|good|love|loved|best|excellent|amazing|brilliant|enjoy|fun|beautiful|solid|nice|impress|liked|tense|gripping|clever|sharp|real|alive|works)", re.I)
FLIP = re.compile(r"\b(not|never|no|isn't|doesn't|didn't|wasn't|hardly)\b", re.I)


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+|\n+", text or "") if s.strip()]


def score_review(r):
    """{'praise': set(ranks), 'punish': set(ranks)} for one review."""
    out = {"praise": set(), "punish": set()}
    thumb = (r.get("thumb") or "").lower()
    for s in sentences(r.get("text", "") + " " + r.get("top_praise", "") + ". " + r.get("top_complaint", "")):
        neg, pos = bool(NEG.search(s)), bool(POS.search(s))
        if pos and FLIP.search(s) and not re.search(r"\b(not|never|no)\b[^.]*\b(bad|boring|dull|broken|bug)", s, re.I):
            pos, neg = False, True  # "not good", "never fun": the flip wins
        side = "punish" if neg and not pos else "praise" if pos and not neg else ("punish" if thumb == "down" else "praise")
        table = PUNISH if side == "punish" else PRAISE
        for rank, _name, _k, _m, words in table:
            if re.search(r"\b(%s)" % words, s, re.I):
                out[side].add(rank)
    return out


def panel_shares(reviews):
    n = len(reviews) or 1
    tags = [score_review(r) for r in reviews]
    rows = {"praise": [], "punish": []}
    for side, table in (("praise", PRAISE), ("punish", PUNISH)):
        for rank, name, k, m, _w in table:
            c = sum(1 for t in tags if rank in t[side])
            rows[side].append({"rank": rank, "theme": name, "panel_pct": round(100.0 * c / n, 1), "kcd2_pct": k, "mafia_pct": m})
    return rows


def table_md(rows, side, top=8):
    L = ["| theme | panel | KCD2 | Mafia |", "|---|---|---|---|"]
    for r in sorted(rows[side], key=lambda r: (-r["panel_pct"], r["rank"]))[:top]:
        L.append("| %s %d. %s | %.0f%% | %.1f%% | %.1f%% |" % ("P" if side == "praise" else "X", r["rank"], r["theme"], r["panel_pct"], r["kcd2_pct"], r["mafia_pct"]))
    return "\n".join(L)


if __name__ == "__main__":
    revs = json.load(open(sys.argv[1], encoding="utf-8"))
    rows = panel_shares(revs)
    print("Praised\n" + table_md(rows, "praise") + "\n\nPunished\n" + table_md(rows, "punish"))
