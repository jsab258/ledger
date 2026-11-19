#!/usr/bin/env python3
"""Validate the LEDGER parts tree and print totals for the progress page.

Checks: every field present; ids unique; parent and children agree; needs and
blocks name real parts and mirror each other; no loops in needs; every felt
part has a standard or a research item; every research item named exists;
every experience rule id in DESIGN.md (and the addendum) lands in some part.

Usage: python tools/lane/parts-tree/check.py [--json]   (exit 1 on any fault)
"""
import json, os, re, sys
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
TREE = os.path.join(ROOT, "production", "lane", "parts-tree", "PARTS-TREE.json")
DESIGNS = [os.path.join(ROOT, "production", "lane", "synthesis", f) for f in ("DESIGN.md", "DESIGN-ADDENDUM-2026-11-20.md")]
FIELDS = ["id", "level", "parent", "name", "what", "felt", "standard", "standard_source", "research_items", "designed_in",
          "track", "status", "needs", "blocks", "hours", "risk", "test", "owner", "checklist_items", "review_themes",
          "notes", "children", "leaf"]
STATUSES = {"missing", "designed", "built shallow", "built", "passes", "unknown"}
TRACKS = {"prototype": ["prototype"], "unreal": ["unreal"], "both": ["prototype", "unreal"]}
OWNERS = {"builder", "town", "clothing", "lane"}


def has_standard(p):
    s = (p.get("standard") or "").strip().lower()
    return bool(s) and not s.startswith("none")


def main():
    doc = json.load(open(TREE, encoding="utf-8"))
    parts = doc["parts"]
    rn = doc.get("research_items", {})
    faults = []
    ids = [p.get("id") for p in parts]
    dup = [i for i, c in Counter(ids).items() if c > 1]
    if dup:
        faults.append("duplicate ids: %s" % dup)
    by = {p["id"]: p for p in parts}
    for p in parts:
        pid = p.get("id")
        for f in FIELDS:
            if f not in p:
                faults.append("%s: missing field %s" % (pid, f))
        if p.get("track") not in TRACKS:
            faults.append("%s: bad track %r" % (pid, p.get("track")))
        else:
            for t in TRACKS[p["track"]]:
                s = p.get("status", {}).get(t, {})
                if s.get("status") not in STATUSES:
                    faults.append("%s: bad or missing %s status" % (pid, t))
                if not s.get("evidence"):
                    faults.append("%s: %s status without evidence" % (pid, t))
        if p.get("owner") not in OWNERS:
            faults.append("%s: bad owner %r" % (pid, p.get("owner")))
        if p.get("risk", {}).get("level") not in ("low", "medium", "high"):
            faults.append("%s: bad risk level" % pid)
        if not p.get("hours", {}).get("basis"):
            faults.append("%s: hours without basis" % pid)
        par = p.get("parent")
        if pid != "0":
            if par not in by:
                faults.append("%s: parent %r missing" % (pid, par))
            elif pid not in by[par].get("children", []):
                faults.append("%s: not listed under its parent" % pid)
        for k in ("needs", "blocks", "children"):
            for q in p.get(k, []):
                if q not in by:
                    faults.append("%s: %s names missing part %s" % (pid, k, q))
        for q in p.get("needs", []):
            if q in by and pid not in by[q].get("blocks", []):
                faults.append("%s needs %s but %s does not list it in blocks" % (pid, q, q))
        for q in p.get("blocks", []):
            if q in by and pid not in by[q].get("needs", []):
                faults.append("%s blocks %s but %s does not need it" % (pid, q, q))
        if p.get("leaf") != (not p.get("children")):
            faults.append("%s: leaf flag wrong" % pid)
        for r in p.get("research_items", []):
            if r not in rn:
                faults.append("%s: research item %s not defined" % (pid, r))
        if p.get("felt") and not has_standard(p) and not p.get("research_items"):
            faults.append("%s: felt part with no standard and no research item" % pid)
    # headings: their status must be the rollup of their leaves
    def leaves_under(p):
        return [p] if p.get("leaf") else [x for c in p.get("children", []) for x in leaves_under(by[c])]
    for p in parts:
        if p.get("leaf") or p.get("id") not in by:
            continue
        for t, s in p.get("status", {}).items():
            cnt = Counter(x["status"][t]["status"] for x in leaves_under(p) if t in x.get("status", {}))
            want = "rollup of %d leaves: " % sum(cnt.values())
            if not s.get("evidence", "").startswith(want) or any("%s %d" % (k, v) not in s["evidence"] for k, v in cnt.items()):
                faults.append("%s: %s rollup out of date (re-run the rollup)" % (p["id"], t))
    # loops in needs
    WHITE, GREY, BLACK = 0, 1, 2
    colour = defaultdict(int)

    def visit(n, stack):
        colour[n] = GREY
        for m in by.get(n, {}).get("needs", []):
            if colour[m] == GREY:
                faults.append("loop in needs: %s" % " > ".join(stack + [n, m]))
            elif colour[m] == WHITE and m in by:
                visit(m, stack + [n])
        colour[n] = BLACK
    sys.setrecursionlimit(10000)
    for i in by:
        if colour[i] == WHITE:
            visit(i, [])
    # every experience rule lands in a part
    text = json.dumps(parts)
    rules = set()
    for d in DESIGNS:
        if os.path.exists(d):
            rules |= set(re.findall(r"ER-[A-Z]+-\d+", open(d, encoding="utf-8").read()))
    unplaced = sorted(r for r in rules if r not in text and not re.search(r"%s to \d+" % re.escape(r[:-2]), text))
    # rule ranges like "ER-FIRST-01 to 04" count for the ids inside them
    def in_range(r):
        pre, num = r.rsplit("-", 1)
        for m in re.finditer(re.escape(pre) + r"-(\d+) to (\d+)", text):
            if int(m.group(1)) <= int(num) <= int(m.group(2)):
                return True
        return False
    unplaced = [r for r in sorted(rules) if r not in text and not in_range(r)]
    for r in unplaced:
        faults.append("experience rule %s lands in no part" % r)

    # totals
    leaves = [p for p in parts if p.get("leaf")]
    group = lambda p: p["id"].split(".")[0]
    tot = {"parts": len(parts), "leaves": len(leaves), "by_group": {}, "by_status": {}, "felt_leaves": 0,
           "felt_without_standard": 0, "research_items": len(rn), "checklist_items_mapped": sum(len(p.get("checklist_items", [])) for p in parts),
           "checklist_items_ruled_out": len(doc.get("ruled_out_checks", [])), "experience_rules": len(rules), "faults": len(faults)}
    for p in leaves:
        g = group(p)
        e = tot["by_group"].setdefault(g, {"name": by[g]["name"], "leaves": 0, "prototype": Counter(), "unreal": Counter()})
        e["leaves"] += 1
        for t, s in p["status"].items():
            e[t][s["status"]] += 1
            tot["by_status"].setdefault(t, Counter())[s["status"]] += 1
        if p.get("felt"):
            tot["felt_leaves"] += 1
            if not has_standard(p):
                tot["felt_without_standard"] += 1
    if "--json" in sys.argv:
        print(json.dumps({**tot, "fault_list": faults}, indent=1, default=dict))
    else:
        print("Parts: %d (%d buildable leaves). Felt leaves: %d, of which %d rest on a research item instead of a standard." % (
            tot["parts"], tot["leaves"], tot["felt_leaves"], tot["felt_without_standard"]))
        print("Checklist items: %d hung on parts, %d ruled out. Experience rules: %d, all placed unless listed below." % (
            tot["checklist_items_mapped"], tot["checklist_items_ruled_out"], tot["experience_rules"]))
        order = ["missing", "designed", "built shallow", "built", "passes", "unknown"]
        for g in sorted(tot["by_group"], key=int):
            e = tot["by_group"][g]
            line = "  %-2s %-38s %3d" % (g, e["name"][:38], e["leaves"])
            for t in ("prototype", "unreal"):
                if e[t]:
                    line += " | %s: %s" % (t, ", ".join("%s %d" % (s, e[t][s]) for s in order if e[t][s]))
            print(line)
        for t, c in tot["by_status"].items():
            print("  all %s: %s" % (t, ", ".join("%s %d" % (s, c[s]) for s in order if c[s])))
        print("Faults: %d" % len(faults))
        for f in faults:
            print("  FAULT " + f)
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main())
