#!/usr/bin/env python3
"""HIS PAGE ANSWERS, KEPT IN THE REPOSITORY: THE INDEX, AND A CHECK THAT FAILS WHEN ONE IS MISSING.

Jafar, 5 October 2026 (the plan's edits 9 and 10): phase 0 sweeps "the approval pages' stored
answers", and "the approval pages' answers are read back into the repository automatically each
night". The answers live in each page's own database on claude.ai, where no script here can
reach them; a session reads them with its ArtifactData tool into
production/approvals/answers/<page id>/<collection>/<answer>.json (their home in the repository),
and production/approvals/answers/pages.json lists every page and where it keeps them.

  python tools/page_answers.py              # check: every page with a database read, every file sound
  python tools/page_answers.py --index      # rewrite production/approvals/answers/INDEX.md
  python tools/page_answers.py --selftest
"""
import argparse
import io
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.join(REPO, "production", "approvals", "answers")


def load(home=HOME):
    with io.open(os.path.join(home, "pages.json"), encoding="utf-8") as f:
        return json.load(f)["pages"]


def answers(home, page):
    out = []
    for col in page.get("collections", []):
        d = os.path.join(home, page["id"], col)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if name.endswith(".json"):
                with io.open(os.path.join(d, name), encoding="utf-8") as f:
                    out.append((col, name[:-5], json.load(f)))
    return out


def check(home=HOME, out=sys.stdout):
    pages = load(home)
    bad = []
    ids = {p["id"] for p in pages}
    if len(ids) != len(pages):
        bad.append("a page is listed twice")
    for p in pages:
        if p["storage"] == "db" and not p.get("collections"):
            bad.append("%s keeps a database but names no collection" % p["title"])
        try:
            answers(home, p)
        except ValueError as e:
            bad.append("%s: an answer file is not JSON (%s)" % (p["title"], e))
    for entry in os.listdir(home):
        full = os.path.join(home, entry)
        if os.path.isdir(full) and entry not in ids:
            bad.append("answers for a page nobody listed: %s" % entry)
    n = sum(len(answers(home, p)) for p in pages)
    for b in bad:
        print("page-answers FAIL " + b, file=out)
    print("page-answers pages=%d answers=%d outcome=%s" % (len(pages), n, "FAIL" if bad else "PASS"), file=out)
    return 1 if bad else 0


def index(home=HOME):
    pages = load(home)
    lines = ["# His page answers", "",
             "Copied from each page's own database into this folder (pages.json lists the pages). Written by tools/page_answers.py --index; never edited by hand.", "",
             "| Page | Updated | Answers | Each answer: pick or verdict, date |", "|---|---|---|---|"]
    total = 0
    for p in pages:
        a = answers(home, p)
        total += len(a)
        cells = []
        for col, key, d in a:
            v = d.get("pick") or d.get("verdict") or d.get("choice") or d.get("speaker") or "?"
            at = (d.get("at") or "")[:10]
            note = (" (" + d["note"].strip().replace("|", "/").replace("\n", " ")[:80] + ")") if d.get("note") else ""
            cells.append("%s: %s, %s%s" % (key, v, at, note))
        what = "; ".join(cells) if cells else (p.get("note") or p["storage"])
        lines.append("| [%s](https://claude.ai/artifact/%s) | %s | %d | %s |" % (p["title"], p["id"], p["updated"], len(a), what))
    lines += ["", "%d pages, %d answers." % (len(pages), total)]
    with io.open(os.path.join(home, "INDEX.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    return total


def selftest():
    import tempfile
    ok = True

    def t(cond, what):
        nonlocal ok
        print(("  ok   " if cond else "  FAIL ") + what)
        ok = ok and cond

    d = tempfile.mkdtemp()
    with io.open(os.path.join(d, "pages.json"), "w", encoding="utf-8") as f:
        json.dump({"pages": [{"id": "P1", "title": "One", "updated": "2026-10-05", "storage": "db", "collections": ["verdicts"]}]}, f)
    os.makedirs(os.path.join(d, "P1", "verdicts"))
    with io.open(os.path.join(d, "P1", "verdicts", "a.json"), "w", encoding="utf-8") as f:
        json.dump({"pick": "yes", "at": "2026-10-05T08:00:00Z"}, f)
    sink = io.StringIO()
    t(check(d, sink) == 0, "a listed page with its answers passes")
    t(index(d) == 1 and "a: yes, 2026-10-05" in io.open(os.path.join(d, "INDEX.md"), encoding="utf-8").read(), "the index shows each answer and its date")
    os.makedirs(os.path.join(d, "P2", "verdicts"))
    t(check(d, sink) == 1, "answers from a page nobody listed fail the check")
    print("page_answers selftest: " + ("passed" if ok else "FAILED"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.index:
        print("INDEX.md: %d answers" % index())
    return check()


if __name__ == "__main__":
    sys.exit(main())
