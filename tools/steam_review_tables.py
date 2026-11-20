"""Tables for the players study from coded Steam reviews (tools/steam_review_coder.py).

Usage: python tools/steam_review_tables.py <gtav-coded.json> <rdr2-coded.json> <gtav dir> <rdr2 dir>
Prints markdown: the sample by pull kind, reviews by year, median hours, set-aside
counts, and the praise and punish tables ranked by the mean of the three games'
shares (KCD2's counts kept from PLAYERS.md, 12 Oct 2026: 5,701 Steam reviews).
"""
import json, statistics, sys, datetime as dt
from collections import Counter
import os
sys.path.insert(0, os.path.dirname(__file__))
from steam_review_coder import PRAISE as CODER_PRAISE, PUNISH as CODER_PUNISH

KCD2_N = 5701
# code: (row name in the players study, KCD2 count from the 12 Oct Steam script)
PRAISE = {
    "story": ("A story and characters worth caring about", 1836),
    "looks": ("How it looks", 1015),
    "world": ("A living, believable world that feels lived in", 1398),
    "side": ("Side content that are whole stories, not errands", 781),
    "music": ("Music and sound (and the radio)", 270),
    "ranwell": ("It ran well, a good PC version", 444),
    "price": ("A fair price and plenty of game for it", 403),
    "melee": ("Skill-based melee that rewards learning it", 1009),
    "voice": ("Voice acting and performances", 219),
    "period": ("Period accuracy and detail", 568),
    "humour": ("Humour, satire and a mix of tones", 269),
    "polish": ("Polish: few bugs", 258),
    "choices": ("Choices and roleplay that change what happens", 403),
    "skills": ("Crafting, skills, getting better at things", 508),
    "driving": ("Driving and riding that feel good", 37),
    "slowburn": ("The slow burn and long cinematic scenes (liked)", 195),
    "gunfights": ("Gunfights that feel weighty", 22),
    "reacts": ("The world reacts to you", 168),
    "challenge": ("Challenge as a reward", 235),
    "ending": ("An ending that landed", 71),
}
PUNISH = {
    "controls": ("Menus, controls, camera and slow animations", 318),
    "boring": ("Boring: nothing to do for minutes", 623),
    "combat": ("Combat that felt clunky or unfair", 1182),
    "story": ("A story that felt predictable, cliched, rushed or thin", 476),
    "bugs": ("Bugs that stop progress or break the illusion", 888),
    "cutscenes": ("Too many or too long cutscenes, a slow opening, too much talk", 612),
    "loop": ("The same loop over and over", 385),
    "price": ("Too short, too expensive, not worth the price", 464),
    "port": ("Stutter, crashes, heavy hardware demands, a bad port", 260),
    "missions": ("Missions that waste time, give no direction or fail you for doing it your way", 409),
    "survival": ("Survival chores as friction", 217),
    "hollow": ("A world that is hollow, or whose rules change on a whim", 227),
    "difficulty": ("Difficulty that is wrong", 338),
    "linear": ("Linear, an empty map, an interactive movie", 115),
    "gunplay": ("Gunplay that feels weak, or auto-aim", 28),
    "saves": ("A save system that costs time", 327),
    "unexplained": ("Systems nobody explains", 286),
    "paid": ("Paid extras, microtransactions, no story add-ons", 123),
    "dated": ("Looks poor or dated", 89),
    "stealth": ("Stealth that is thin or stupid", 197),
}


def load(path):
    return json.load(open(path, encoding="utf-8"))


def sample_rows(d):
    rows = [json.loads(l) for l in open(f"{d}/reviews.jsonl", encoding="utf-8")]
    return rows


def table(name, spec, g, r):
    out = []
    for code, (row, k) in spec.items():
        kg = k / KCD2_N
        ng, nr = g[name].get(code, 0), r[name].get(code, 0)
        sg, sr = ng / g["kept"], nr / r["kept"]
        out.append(((kg + sg + sr) / 3, row, k, kg, ng, sg, nr, sr, code))
    out.sort(reverse=True)
    print(f"| Rank | Theme | KCD2 (Steam, {KCD2_N:,}) | GTA V (Steam, {g['kept']:,} kept) | RDR2 (Steam, {r['kept']:,} kept) | Mean share |")
    print("|---|---|---|---|---|---|")
    for i, (m, row, k, kg, ng, sg, nr, sr, code_) in enumerate(out, 1):
        coded = code_ in (CODER_PRAISE if name == "praise" else CODER_PUNISH)
        cg = f"{ng:,} ({100*sg:.1f}%)" if coded else "not coded (0)"
        cr = f"{nr:,} ({100*sr:.1f}%)" if coded else "not coded (0)"
        print(f"| {i} | {row} | {k:,} ({100*kg:.1f}%) | {cg} | {cr} | {100*m:.1f}% |")
    print()


def describe(label, coded, d):
    rows = sample_rows(d)
    tot = json.load(open(f"{d}/totals.json"))
    pulls = json.load(open(f"{d}/pulls.json"))
    pos = [r for r in rows if r["voted_up"]]
    neg = [r for r in rows if not r["voted_up"]]
    e = tot["english"]
    print(f"**{label}.** Steam English totals read {tot['read']}: {e['total_positive']:,} positive, "
          f"{e['total_negative']:,} negative, {e['total_reviews']:,} in all, '{e['review_score_desc']}'; "
          f"positive share {100*e['total_positive']/e['total_reviews']:.1f}%.")
    first = dt.datetime.utcfromtimestamp(min(r["timestamp_created"] for r in rows)).date()
    last = dt.datetime.utcfromtimestamp(max(r["timestamp_created"] for r in rows)).date()
    print(f"Fetched: {len(rows):,} different English reviews, {len(pos):,} positive and {len(neg):,} negative, written {first} to {last}.")
    print(f"Set aside whole (only about the online mode, anti-cheat, launcher, accounts, the company or mods, with no word on the game): {coded['set_aside']:,}; "
          f"coded on their game sentences only (mixed): {coded['mixed']:,}; kept: {coded['kept']:,}.")
    hrs = lambda rs: statistics.median(r["author"].get("playtime_at_review", 0) / 60 for r in rs)
    print(f"Median hours at review: positive {hrs(pos):.0f}, negative {hrs(neg):.0f}.")
    kinds = Counter()
    for k, n in pulls.items():
        base = "monthly" if k.startswith("month_") else "weekly" if k.startswith("week") else k.rsplit("_", 1)[0]
        kinds[(base, k.rsplit("_", 1)[1])] += n
    print("Pulls: " + "; ".join(f"{b} {v} {n}" for (b, v), n in sorted(kinds.items())) + ".")
    years = Counter(dt.datetime.utcfromtimestamp(r["timestamp_created"]).year for r in rows)
    print("By year of writing: " + ", ".join(f"{y} {n}" for y, n in sorted(years.items())) + ".")
    print()


def main():
    g, r = load(sys.argv[1]), load(sys.argv[2])
    describe("GTA V (app 271590)", g, sys.argv[3])
    describe("RDR2 (app 1174180)", r, sys.argv[4])
    print("### Praise\n"); table("praise", PRAISE, g, r)
    print("### Punish\n"); table("punish", PUNISH, g, r)
    fg, fr = g["praise"].get("freedom", 0), r["praise"].get("freedom", 0)
    print(f"NEW, not ranked (KCD2 not coded for it): freedom to play, lots to do: GTA V {fg:,} ({100*fg/g['kept']:.1f}%), RDR2 {fr:,} ({100*fr/r['kept']:.1f}%).")


if __name__ == "__main__":
    main()
