"""Tables for the walkthrough games' Steam study (advisor 273, 20 Nov 2026).

Usage: python tools/steam_walkthrough_tables.py <coded-dir>
Reads <coded-dir>/<game>-mech.json written by tools/steam_review_mech.py and
F:/LedgerTools/steam-reviews/<appid>/totals.json, prints markdown: one section per game
(sample, set aside, top themes, its mechanics with sub-points and short quotes), then one
table per mechanic across its games (share of kept reviews praising and punishing it).
"""
import json, os, sys

GAMES = [  # key, appid, title, mechanics studied
    ("sleepingdogs", 307690, "Sleeping Dogs: Definitive Edition", ["driving", "fists", "onfoot", "chases"]),
    ("gtaiv", 12210, "GTA IV", ["driving", "fists", "onfoot", "chases"]),
    ("lanoire", 110800, "L.A. Noire", ["chases", "driving"]),
    ("hitmanwoa", 1659040, "Hitman: World of Assassination", ["seen"]),
    ("wdlegion", 2239550, "Watch Dogs: Legion", ["driving", "chases"]),
    ("fh4", 1293830, "Forza Horizon 4", ["driving"]),
]
MNAME = {"driving": "Driving", "fists": "Fists", "onfoot": "Moving on foot", "seen": "Being seen", "chases": "Chases"}


def pct(n, k):
    return f"{100*n/max(k,1):.1f}%"


def main():
    d = sys.argv[1]
    have = {}
    for key, app, title, mechs in GAMES:
        f = f"{d}/{key}-mech.json"
        if not os.path.exists(f):
            print(f"## {title}\n\nNot coded yet.\n")
            continue
        j = json.load(open(f, encoding="utf-8"))
        have[key] = (title, mechs, j)
        tot = json.load(open(f"F:/LedgerTools/steam-reviews/{app}/totals.json"))
        e = (tot.get("english") or {})
        k = j["kept"]
        print(f"## {title}\n")
        print(f"Steam app {app}; Steam's English count {e.get('total_reviews','?')} "
              f"({e.get('total_positive','?')} up), read {tot.get('read','?')}. Pulled {j['reviews']}, "
              f"set aside {j['set_aside']}, kept {k} (mixed {j['mixed']}).\n")
        for side in ("praise", "punish"):
            top = sorted(j[side].items(), key=lambda x: -x[1])[:8]
            print(f"Top {side}: " + "; ".join(f"{t} {pct(n, k)}" for t, n in top) + ".\n")
        for m in mechs:
            mm = j["mech"][m]
            print(f"### {MNAME[m]}\n")
            print(f"Mentioned in {pct(mm['mention'], k)} of kept reviews; praised in {pct(mm['praise'], k)}, "
                  f"punished in {pct(mm['punish'], k)}.\n")
            subs = sorted({x.split(':')[1] for x in list(j['mech_sub_praise']) + list(j['mech_sub_punish'])
                           if x.startswith(m + ':')})
            print("| Sub-point | Praise | Punish |\n|---|---|---|")
            for s in subs:
                print(f"| {s} | {j['mech_sub_praise'].get(m+':'+s, 0)} | {j['mech_sub_punish'].get(m+':'+s, 0)} |")
            print()
            for side in ("praise", "punish"):
                for rid, q in j["quotes"][m][side][:3]:
                    print(f"- {side}: \"{q}\" (review {rid})")
            print()
    for m in MNAME:
        rows = [(t, j) for key, (t, ms, j) in have.items() if m in ms]
        if not rows:
            continue
        print(f"## {MNAME[m]} across its games\n\n| Game | Kept | Mention | Praise | Punish | Top praised sub-point | Top punished sub-point |\n|---|---|---|---|---|---|---|")
        for t, j in rows:
            mm, k = j["mech"][m], j["kept"]
            sp = sorted(((x.split(':')[1], n) for x, n in j["mech_sub_praise"].items() if x.startswith(m + ':') and not x.endswith(':general')), key=lambda x: -x[1])
            sn = sorted(((x.split(':')[1], n) for x, n in j["mech_sub_punish"].items() if x.startswith(m + ':') and not x.endswith(':general')), key=lambda x: -x[1])
            print(f"| {t} | {k} | {pct(mm['mention'], k)} | {pct(mm['praise'], k)} | {pct(mm['punish'], k)} | "
                  f"{sp[0][0] if sp else '-'} | {sn[0][0] if sn else '-'} |")
        print()


if __name__ == "__main__":
    main()
