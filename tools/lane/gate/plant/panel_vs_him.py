"""The panel's verdicts beside his own words (4t piece 8, second half).

His plan of 19 Nov: "record the panel's verdicts beside his own words when he plays, and fix the panel when they
keep disagreeing." Each time he plays a build the panel has judged, one entry goes into
production/lane/PANEL-VS-JAFAR.json (written by the loop, from his words on his page or in the advisor's message;
never asked of him):

  {"date": "2026-11-23", "build": "loop 2", "his_words": "...", "his_verdict": "yes" | "no" | "unsure",
   "his_problems": ["the cab camera", ...], "panel_verdict": "yes" | "no", "panel_problems": [...]}

his_verdict is whether he would keep playing (yes or no), taken from his words; "unsure" when they do not say.
The report shows, per entry, whether the verdicts agree and how many of his problems the panel named; and states
"fix the panel" when two of the last three entries with a verdict disagree, or when the panel named fewer than
half of his problems in two of the last three. Agreement beyond chance (Cohen's kappa, Judge's Verdict 2025's
measure) is shown once there are ten entries with a verdict; before that it would mean nothing.

    python panel_vs_him.py [--file F] [--out MD]
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
FILE = os.path.join(REPO, "production", "lane", "PANEL-VS-JAFAR.json")


def norm(s):
    return " ".join(str(s).lower().split())


COMMON = set("""a an the and or but of in on at to for with by from is are was were be been it its this that
these those too very so not no his her he she they them there here as than then into out up down over under
cab car tom game feels feel felt looks look bit much more less""".split())


def words(s):
    return {w.strip(".,;:!?'\"()") for w in norm(s).split()} - COMMON - {""}


def named_share(his, panel):
    """Share of his problems the panel also named: every telling word of his line (common words and the game's
    everywhere-words like cab and Tom left out) must be in one panel line, or at least two of them when his line
    has three or more. A loop still reads the lines by eye; this only screens."""
    if not his:
        return None
    got = 0
    for h in his:
        hw = words(h)
        need = len(hw) if len(hw) < 3 else max(2, (len(hw) + 1) // 2)
        if hw and any(len(hw & words(p)) >= need for p in panel):
            got += 1
    return got / len(his)


def kappa(pairs):
    n = len(pairs)
    if n == 0:
        return None
    po = sum(1 for a, b in pairs if a == b) / n
    labels = {x for p in pairs for x in p}
    pe = sum((sum(1 for a, _ in pairs if a == l) / n) * (sum(1 for _, b in pairs if b == l) / n) for l in labels)
    return None if pe == 1 else (po - pe) / (1 - pe)


def judge(entries):
    rows, flags = [], []
    for e in entries:
        hv, pv = e.get("his_verdict"), e.get("panel_verdict")
        agree = None if hv not in ("yes", "no") or pv not in ("yes", "no") else hv == pv
        share = named_share(e.get("his_problems", []), e.get("panel_problems", []))
        rows.append(dict(e, agree=agree, named=share))
    with_v = [r for r in rows if r["agree"] is not None][-3:]
    if len(with_v) >= 2 and sum(1 for r in with_v if r["agree"] is False) >= 2:
        flags.append("fix the panel: its verdict disagreed with his in %d of the last %d plays"
                     % (sum(1 for r in with_v if r["agree"] is False), len(with_v)))
    with_p = [r for r in rows if r["named"] is not None][-3:]
    if len(with_p) >= 2 and sum(1 for r in with_p if r["named"] < 0.5) >= 2:
        flags.append("fix the panel: it named fewer than half of his problems in %d of the last %d plays"
                     % (sum(1 for r in with_p if r["named"] < 0.5), len(with_p)))
    pairs = [(r["his_verdict"], r["panel_verdict"]) for r in rows if r["agree"] is not None]
    k = kappa(pairs) if len(pairs) >= 10 else None  # None too when he gave the same verdict every time
    return rows, flags, k, len(pairs)


def report(rows, flags, k, n):
    out = ["# The panel beside his own words", "",
           "Made by tools/lane/gate/plant/panel_vs_him.py from production/lane/PANEL-VS-JAFAR.json.", ""]
    if not rows:
        out += ["No entries yet: he has not played a build the panel judged (the first loop comes after the one-shot)."]
        return "\n".join(out) + "\n"
    out += ["| Date | Build | His verdict | Panel | Agree | His problems the panel named |", "|---|---|---|---|---|---|"]
    for r in rows:
        out.append("| %s | %s | %s | %s | %s | %s |" % (
            r.get("date", ""), r.get("build", ""), r.get("his_verdict", ""), r.get("panel_verdict", ""),
            {True: "yes", False: "NO", None: "-"}[r["agree"]],
            "-" if r["named"] is None else "%d%%" % round(100 * r["named"])))
    out += ["", "Agreement beyond chance (Cohen's kappa): " +
            ("%.2f over %d plays" % (k, n) if k is not None else "not shown until ten plays with a verdict (%d so far)" % n), ""]
    out += ["## What to do", "",
            "A flag is a prompt to read his words and the panel's side by side and look for why, not proof that the "
            "panel is wrong: with few plays even a good panel trips it now and then.", ""]
    out += ["- " + f for f in flags] or ["- nothing: the panel and he agree well enough so far"]
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", default=FILE)
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    entries = json.load(open(a.file, encoding="utf-8")) if os.path.exists(a.file) else []
    rows, flags, k, n = judge(entries)
    md = report(rows, flags, k, n)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(md)
    print(md)
    return 1 if flags else 0


if __name__ == "__main__":
    sys.exit(main())
