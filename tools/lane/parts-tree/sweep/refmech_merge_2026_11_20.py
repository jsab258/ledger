"""Merge the reference-mechanics map (work/refmech-map/map-A/B/C.json) into PARTS-TREE.json.
Lane, 20 Nov 2026 (task 1c). Adds the new parts, notes each mapped part with its mechanic ids,
writes MECHANICS-MAP-2026-11-20.md and the addendum sections A32 to A40. Run once; it refuses to run twice."""
import json, os, collections
D = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "production", "lane", "parts-tree")
D = os.path.abspath(D)
SYN = os.path.join(D, "..", "synthesis", "DESIGN-ADDENDUM-2026-11-20.md")
tree = json.load(open(os.path.join(D, "PARTS-TREE.json"), encoding="utf-8"))
P = {p["id"]: p for p in tree["parts"]}
if any("Reference mechanics (20 Nov)" in n for p in tree["parts"] for n in p["notes"]):
    raise SystemExit("already merged")
mech = {m["id"]: m for m in json.load(open(os.path.join(D, "work/refmech-map/mechanics.json"), encoding="utf-8"))}
rows = []
for L in "ABC":
    rows += json.load(open(os.path.join(D, "work/refmech-map/map-%s.json" % L), encoding="utf-8"))
ORDER = ["horn", "torch", "pocket-lift", "damage-by-hand", "police-aftermath", "street-on-edge", "discovery", "calling-on", "crew-pay"]
PARENT = {"horn": "1.2", "torch": "1.6", "pocket-lift": "1.6", "damage-by-hand": "1.6", "police-aftermath": "2.6",
          "street-on-edge": "2.5", "discovery": "2.5", "calling-on": "3.2", "crew-pay": "2.11"}
HOURS = {"horn": ("0.5", "4"), "torch": ("1", "8"), "pocket-lift": ("1.5", "12"), "damage-by-hand": ("1", "10"),
         "police-aftermath": ("2", "16"), "street-on-edge": ("1", "6"), "discovery": ("1.5", "10"), "calling-on": ("2", "16"), "crew-pay": ("1", "6")}
specs, members = {}, collections.defaultdict(list)
for r in rows:
    if r["decision"] == "new":
        members[r["new_key"]].append(r["id"])
        if "new" in r:
            specs[r["new_key"]] = r["new"]
assert set(specs) == set(ORDER), (set(specs), ORDER)
newid, addendum = {}, []
for n, key in enumerate(ORDER):
    s, par = specs[key], P[PARENT[key]]
    nums = [int(c.split(".")[-1]) for c in par["children"]]
    pid = "%s.%d" % (par["id"], max(nums) + 1)
    sec = "A%d" % (32 + n)
    newid[key] = pid
    part = {
        "id": pid, "level": par["level"] + 1, "parent": par["id"], "name": s["name"], "what": s["what"],
        "felt": bool(s["felt"]),
        "standard": "rule: " + s["test"],
        "standard_source": "DESIGN-ADDENDUM-2026-11-20 %s (from REFERENCE-MECHANICS-2026-11-20 %s)" % (sec, ", ".join(members[key])),
        "research_items": [], "designed_in": "DESIGN-ADDENDUM-2026-11-20 %s" % sec, "track": s["track"],
        "status": {t: {"status": "designed", "evidence": "DESIGN-ADDENDUM-2026-11-20 %s, 20 Nov; nothing built" % sec}
                   for t in ("prototype", "unreal")},
        "needs": [], "blocks": [],
        "hours": {"prototype": HOURS[key][0], "unreal": HOURS[key][1], "basis": "guess"},
        "risk": {"level": "low", "why": "rule-driven, on parts that exist"},
        "test": s["test"], "owner": "lane", "checklist_items": [], "review_themes": [],
        "notes": ["Added 20 Nov by the lane from the reference-mechanics map (1c): %s" % ", ".join(members[key])],
        "children": [], "leaf": True,
    }
    if s["track"] == "both" or s["track"] == "prototype":
        pass
    tree["parts"].insert(tree["parts"].index(P[par["children"][-1]]) + 1, part)
    par["children"].append(pid)
    P[pid] = part
    q = [r.get("question") for r in rows if r.get("new_key") == key and r.get("question")]
    addendum += ["", "## %s. %s (%s)" % (sec, s["name"], pid), "",
                 "Found by mapping the reference mechanics onto the parts tree (%s, 20 Nov). Decided within canon, the pillars and his rulings." % ", ".join(members[key]),
                 *["- " + x.strip() for x in s["design"].replace(". ", ".\n").split("\n") if x.strip()],
                 "", "Check: " + s["test"]]
    if q:
        addendum += ["", "Built to the recommended answer; recorded in DECISIONS-PENDING.md (the three questions for him are already used)."]
# notes on mapped parts
bypart = collections.defaultdict(list)
for r in rows:
    if r["decision"] == "part":
        bypart[r["part"]].append(r["id"])
for pid, ms in bypart.items():
    P[pid]["notes"].append("Reference mechanics (20 Nov): " + ", ".join(sorted(ms, key=lambda x: [int(v) for v in x[1:].split(".")])))
json.dump(tree, open(os.path.join(D, "PARTS-TREE.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
with open(SYN, "a", encoding="utf-8") as f:
    f.write("\n".join(addendum) + "\n")
# the map
L = ["# Reference mechanics on the parts tree", "",
     "Dated 20 Nov 2026 (lane, task 1c). Every mechanic in production/research/lane/REFERENCE-MECHANICS-2026-11-20.md that its marks do not already rule out (289 of 483) now lands on a part, became a new part, or is marked not for LEDGER here with its reason. The 194 lines already marked not for LEDGER keep their reason in that file. Mapped by three Opus helpers at high effort (brief: work/refmech-map/BRIEF.md; raw: work/refmech-map/map-A, B, C.json); merged by tools/lane/parts-tree/sweep/refmech_merge_2026_11_20.py, which also writes each mechanic id into its part's notes.", ""]
c = collections.Counter(r["decision"] for r in rows)
L += ["Counts: on an existing part %d; new parts %d (from %d mechanics); not for LEDGER %d." % (c["part"], len(ORDER), c["new"], c["out"]), "",
      "## New parts", ""]
for key in ORDER:
    L.append("- %s %s: %s (%s; DESIGN-ADDENDUM %s)" % (newid[key], specs[key]["name"], specs[key]["what"], ", ".join(members[key]), "A%d" % (32 + ORDER.index(key))))
L += ["", "## Not for LEDGER, with the reason", ""]
for r in rows:
    if r["decision"] == "out":
        L.append("- %s %s: %s" % (r["id"], mech[r["id"]]["text"].split(":")[0], r["reason"]))
L += ["", "## On existing parts", ""]
for r in sorted([r for r in rows if r["decision"] == "part"], key=lambda r: [int(v) for v in r["id"][1:].split(".")]):
    L.append("- %s %s: %s %s" % (r["id"], mech[r["id"]]["text"].split(":")[0], r["part"], P[r["part"]]["name"]))
open(os.path.join(D, "MECHANICS-MAP-2026-11-20.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print(c, newid)
