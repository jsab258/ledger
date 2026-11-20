"""After the merge: rewrite each part's 'Reference mechanics (20 Nov)' note and MECHANICS-MAP-2026-11-20.md
from the raw maps (work/refmech-map/map-A/B/C.json), so fixes to the maps reach the tree. Safe to run again."""
import json, os, collections
D = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "production", "lane", "parts-tree"))
tree = json.load(open(os.path.join(D, "PARTS-TREE.json"), encoding="utf-8"))
P = {p["id"]: p for p in tree["parts"]}
mech = {m["id"]: m for m in json.load(open(os.path.join(D, "work/refmech-map/mechanics.json"), encoding="utf-8"))}
rows = []
for L in "ABC":
    rows += json.load(open(os.path.join(D, "work/refmech-map/map-%s.json" % L), encoding="utf-8"))
key = lambda i: [int(v) for v in i[1:].split(".")]
NEW = {p["id"]: p for p in tree["parts"] if any(n.startswith("Added 20 Nov by the lane from the reference-mechanics map") for n in p["notes"])}
newof = {}
for pid, p in NEW.items():
    for n in p["notes"]:
        if n.startswith("Added 20 Nov by the lane"):
            for m in n.split(": ", 1)[1].split(", "):
                newof[m] = pid
bypart = collections.defaultdict(list)
for r in rows:
    if r["decision"] == "part":
        bypart[r["part"]].append(r["id"])
for p in tree["parts"]:
    p["notes"] = [n for n in p["notes"] if not n.startswith("Reference mechanics (20 Nov): ")]
    if p["id"] in bypart:
        p["notes"].append("Reference mechanics (20 Nov): " + ", ".join(sorted(bypart[p["id"]], key=key)))
json.dump(tree, open(os.path.join(D, "PARTS-TREE.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
c = collections.Counter(r["decision"] for r in rows)
name = lambda i: mech[i]["text"].split(":")[0]
L = ["# Reference mechanics on the parts tree", "",
     "Dated 20 Nov 2026 (lane, task 1c). Every mechanic in production/research/lane/REFERENCE-MECHANICS-2026-11-20.md that its marks do not already rule out (289 of 483) now lands on a part, became a new part, or is marked not for LEDGER here with its reason. The 194 lines already marked not for LEDGER keep their reason in that file. Mapped by three Opus helpers at high effort (brief: work/refmech-map/BRIEF.md; raw: work/refmech-map/map-A, B, C.json); merged by tools/lane/parts-tree/sweep/refmech_merge_2026_11_20.py and kept current by refmech_refresh_2026_11_20.py, which writes each mechanic id into its part's notes. Fixed once after a fresh review (production/lane/REVIEW-1C-MERGE-2026-11-20.md).",
     "", "A line on an existing part says how LEDGER does it where that differs from the reference game ('LEDGER form'); 'LEDGER form only' means the reference game's version is not in LEDGER, only the narrower form named.", "",
     "Counts: on an existing part %d; new parts %d (from %d mechanics); not for LEDGER %d." % (c["part"], len(NEW), c["new"], c["out"]), "", "## New parts", ""]
for pid in sorted(NEW, key=lambda i: [int(v) for v in i.split(".")]):
    p = NEW[pid]
    L.append("- %s %s: %s (%s)" % (pid, p["name"], p["what"], p["designed_in"]))
L += ["", "## Not for LEDGER, with the reason", ""]
for r in sorted([r for r in rows if r["decision"] == "out"], key=lambda r: key(r["id"])):
    L.append("- %s %s: %s" % (r["id"], name(r["id"]), r["reason"]))
L += ["", "## On existing parts", ""]
for r in sorted([r for r in rows if r["decision"] == "part"], key=lambda r: key(r["id"])):
    L.append("- %s %s: %s %s%s" % (r["id"], name(r["id"]), r["part"], P[r["part"]]["name"], (". " + r["reason"]) if r.get("reason") else ""))
open(os.path.join(D, "MECHANICS-MAP-2026-11-20.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print(c)
