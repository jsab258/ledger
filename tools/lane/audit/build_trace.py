"""Join the decisions with their status pass and write DECISIONS-TRACE.md and decisions-trace.json.
Usage: python3 tools/lane/audit/build_trace.py production/audits/full-2026-11
"""
import collections
import json
import pathlib
import sys

ORDER = ["lost", "contradicted", "open", "unclear", "in-force", "enforced", "superseded", "done"]
TITLES = {
    "lost": "Lost: in force nowhere, never withdrawn",
    "contradicted": "Contradicted: his word stands, a current text or practice says otherwise",
    "open": "Open: unanswered, or still waiting to be carried out",
    "unclear": "Unclear: not enough evidence",
    "in-force": "In force, but nothing checks it",
    "enforced": "In force and enforced by a check",
    "superseded": "Superseded by a later decision of his",
    "done": "Done: one-off, carried out",
}
GROUPS = {"A": "DECISIONS.md (first half)", "B": "DECISIONS.md (second half)", "C": "RULINGS.md and canon.md",
          "D": "the weekly orders", "E": "the advisor rows", "F": "his page's picks", "G": "the old version's records"}


def join(base):
    work = pathlib.Path(base) / "work"
    rows = {r["id"]: r for r in json.loads((work / "decisions-merged.json").read_text(encoding="utf-8"))}
    for f in sorted(work.glob("status-*.json")):
        for s in json.loads(f.read_text(encoding="utf-8")):
            r = rows.get(s.get("id"))
            if r is None:
                continue
            st = s.get("status", "unclear")
            r["status"] = st if st in ORDER else "unclear"
            for k in ("enforcer", "by", "evidence"):
                r[k] = s.get(k, "")
    for r in rows.values():
        r.setdefault("status", "unclassified")
    return list(rows.values())


def esc(t):
    return str(t or "").replace("|", "/").replace("\n", " ").strip()


def render(rows):
    c = collections.Counter(r["status"] for r in rows)
    srcs = collections.Counter(r["group"] for r in rows)
    out = ["# Decisions trace (full audit, November 2026)", "",
           "Every decision Jafar made that the audit could find, and where it stands on 19 Nov 2026. "
           "Made by the cloud lane (item 4q, stage 1b): seven helpers extracted his decisions from seven sources, "
           "eight more checked each against today's texts and checks. Lost and contradicted come first. "
           "The same decision found in several sources may appear more than once (each row names its source). "
           "Status is a first reading for the stage 2 reviewers to test, not a verdict.", "",
           "## Counts", ""]
    out.append("| Status | Count |\n|---|---|")
    for s in ORDER + ["unclassified"]:
        if c.get(s):
            out.append(f"| {s} | {c[s]} |")
    out.append(f"| total | {len(rows)} |")
    out += ["", "Sources: " + "; ".join(f"{GROUPS.get(g, g)} {n}" for g, n in sorted(srcs.items())) + ".", ""]
    for s in ORDER + ["unclassified"]:
        items = sorted([r for r in rows if r["status"] == s], key=lambda r: (r["area"], r["date"]))
        if not items:
            continue
        out += [f"## {TITLES.get(s, s)} ({len(items)})", ""]
        detailed = s in ("lost", "contradicted", "open", "unclear")
        if detailed:
            for r in items:
                out.append(f"- **{esc(r['topic'])}** ({r['date'] or 'no date'}, {r['area']}, {r['id']}): {esc(r['decision'])}"
                           + (f" His words: \"{esc(r['words'])}\"." if r.get("words") else ""))
                if r.get("by"):
                    out.append(f"  - Against / by: {esc(r['by'])}")
                out.append(f"  - Evidence: {esc(r.get('evidence'))} Source: {esc(r['src'])}")
            out.append("")
        else:
            out.append("| Id | Date | Area | Topic | Decision | " + ("Enforcer" if s == "enforced" else "By / evidence") + " |")
            out.append("|---|---|---|---|---|---|")
            for r in items:
                last = r.get("enforcer") if s == "enforced" else (r.get("by") or r.get("evidence"))
                out.append(f"| {r['id']} | {r['date']} | {r['area']} | {esc(r['topic'])} | {esc(r['decision'])} | {esc(last)} |")
            out.append("")
    return "\n".join(out) + "\n"


def main(base):
    rows = join(base)
    b = pathlib.Path(base)
    (b / "decisions-trace.json").write_text(json.dumps({"made": "2026-11-19", "rows": rows}, indent=1, ensure_ascii=False), encoding="utf-8")
    (b / "DECISIONS-TRACE.md").write_text(render(rows), encoding="utf-8")
    print(collections.Counter(r["status"] for r in rows))


if __name__ == "__main__":
    main(sys.argv[1])
