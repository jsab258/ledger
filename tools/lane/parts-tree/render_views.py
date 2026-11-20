#!/usr/bin/env python3
"""Write ONESHOT-CHECKLIST.md, PLAN-VIEW.md and RESEARCH-NEEDED.md from PARTS-TREE.json.

The tiers below place each gameplay part in the prototype's stages (BUILD-ORDER's A to D) and each part in a proposed
Unreal phase. They are a view, not a decision: Monday's order and the loops pick what is built.
"""
import json, os
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
D = os.path.join(ROOT, "production", "lane", "parts-tree")
doc = json.load(open(os.path.join(D, "PARTS-TREE.json"), encoding="utf-8"))
P = doc["parts"]
by = {p["id"]: p for p in P}
leaves = [p for p in P if p["leaf"]]

def under(pid, prefixes):
    return any(pid == x or pid.startswith(x + ".") for x in prefixes)

# Prototype stage of each gameplay part (BUILD-ORDER stages: A one evening, B a week, C the rise, D the end)
STAGE_B = ["1.1.6", "1.1.8", "1.2.6", "1.2.8", "1.2.9", "1.2.10", "1.3.11", "1.4.8", "1.5.2", "1.6.1", "1.6.2", "1.6.3", "1.6.10", "1.6.11",
           "2.1.6", "2.4.5", "2.6.5", "2.6.7", "2.7.5", "2.7.6", "2.7.8", "2.9.2", "2.10.2", "2.14", "2.16", "2.19", "3.1.1", "3.1.6", "3.2.5",
           "3.3", "3.5.3", "3.5.4", "3.7", "4.11.1", "7.3", "7.10", "7.16", "6.10",
           "1.6.12", "1.6.13", "1.6.14", "2.5.4", "3.2.7"]  # last line: added 20 Nov from the reference-mechanics map
STAGE_C = ["1.3.10", "1.7", "2.6.6", "2.6.8", "2.6.9", "2.10.1", "2.10.3", "2.10.4", "2.11", "2.12.2", "2.12.3", "2.12.5", "2.13", "2.15.1",
           "2.15.2", "2.15.3", "2.17", "3.1.2", "3.5.5", "7.4", "7.5", "7.7",
           "1.6.15"]  # last line: hold-ups, his yes of 20 Nov 07:39 (addendum A41)
STAGE_D = ["3.1.3", "3.1.4", "3.1.5", "6.2.5", "7.15"]
GAMEPLAY_EXTRA = ["4.1.4", "4.2.4", "4.11.1", "4.5.1", "8.4.1", "9.6"]

def stage(pid):
    if under(pid, STAGE_D): return "D"
    if under(pid, STAGE_C): return "C"
    if under(pid, STAGE_B): return "B"
    return "A"

def is_gameplay(p):
    g = p["id"].split(".")[0]
    return p["track"] in ("both", "prototype") and (g in ("1", "2", "3", "6", "7") or p["id"] in GAMEPLAY_EXTRA)

# Unreal phase proposal
UPH = {"U2": "Quay Street (now)", "U3": "Thirty minutes hold", "U4": "Friends' candidate", "U5": "First town: the Hook and its people",
       "U6": "Crime and the rise ported from the prototype", "U7": "Story: acts and endings", "U8": "The docks", "U9": "Ship"}
def uphase(p):
    i = p["id"]
    if under(i, ["4.2"]): return "U8"
    if under(i, ["10"]) or under(i, ["8.2.1", "8.3.1", "8.1.3", "8.6.1", "8.5"]): return "U9"
    if under(i, ["4.1.1", "4.4", "4.3.1", "5.3", "5.4", "5.10", "4.7", "4.8", "4.9", "4.10"]): return "U2"
    if under(i, ["9"]): return "U2"
    if under(i, ["4", "5", "8"]): return "U5"
    s = stage(i)
    if s == "A":
        return "U3"
    return {"B": "U5", "C": "U6", "D": "U7"}[s]

def status(p, t):
    return p["status"].get(t, {}).get("status", "-")

def hours(p, t):
    try:
        return float(p["hours"].get(t) or 0)
    except ValueError:
        return 0.0

# transitive dependents (what blocks the most) and longest path by hours
def dependents(pid, seen=None):
    seen = set() if seen is None else seen
    for q in by[pid]["blocks"]:
        if q not in seen:
            seen.add(q); dependents(q, seen)
    return seen
memo = {}
def longest(pid, t):
    k = (pid, t)
    if k in memo: return memo[k]
    best = (0.0, [])
    for n in by[pid]["needs"]:
        h, path = longest(n, t)
        if h > best[0]: best = (h, path)
    memo[k] = (best[0] + hours(by[pid], t), best[1] + [pid])
    return memo[k]

# ---------------- ONESHOT-CHECKLIST.md ----------------
G = [p for p in leaves if is_gameplay(p)]
L = ["# The one-shot's checklist", "",
     "Every gameplay part the one-shot (Friday 20 Nov, 22:10) builds into the browser prototype, in BUILD-ORDER's stages, each with its test and where its design is. The one-shot reports against this list, part by part: done (its test passes), shallow (built, test not yet passing), or not reached, with the reason. Generated from PARTS-TREE.json by tools/lane/parts-tree/render_views.py.", "",
     "Rules for the one-shot: never change tools/lane/one-sim/; the town simulation stays the real one where the switch has landed; no polish (art, animation detail, voices, clothes and faces are never the browser's work); the content rule; a play build reaches him only through the publish gate. 'Now' is the prototype's status before the one-shot, from evidence (round 5 published, round 6 built and not published).", "",
     "Parts: %d. Already passing their standard: %d (keep them passing)." % (len(G), sum(1 for p in G if status(p, "prototype") == "passes")), ""]
NAMES = {"A": "Stage A: one evening that holds", "B": "Stage B: a week that holds", "C": "Stage C: the rise", "D": "Stage D: the end"}
for s in "ABCD":
    rows = [p for p in G if stage(p["id"]) == s]
    L += ["## " + NAMES[s] + " (%d parts)" % len(rows), ""]
    for p in sorted(rows, key=lambda x: [int(n) for n in x["id"].split(".")]):
        L.append("- [ ] %s %s. Now: %s. Design: %s. Test: %s." % (p["id"], p["name"], status(p, "prototype"), p["designed_in"], p["test"]))
    L.append("")
L += ["## Not for the one-shot", "", "Every part whose track is Unreal only (art, faces, clothes, Kiln, performance, shipping) and the machinery outside the prototype. See PLAN-VIEW.md for their order.", ""]
open(os.path.join(D, "ONESHOT-CHECKLIST.md"), "w", encoding="utf-8").write("\n".join(L))

# ---------------- PLAN-VIEW.md ----------------
L = ["# Plan view: the order of the parts", "",
     "From the parts' needs and blocks (PARTS-TREE.json), generated by tools/lane/parts-tree/render_views.py. A view, never a plan by itself: Monday's order and the loops pick what is built (his decision of 19 Nov; RULINGS 29 Sep: no new system before its place in PLAN.md). Hours are first estimates, mostly marked guesses (each part's basis is in the JSON).", ""]
for t, title in (("prototype", "The prototype"), ("unreal", "The Unreal game")):
    tl = [p for p in leaves if t in p["status"]]
    tot = sum(hours(p, t) for p in tl)
    left = sum(hours(p, t) for p in tl if status(p, t) not in ("passes", "built"))
    L += ["## " + title, "", "Leaves on this track: %d; estimated hours in all %.0f, of which %.0f on parts not yet built (guesses mostly; see each part's basis)." % (len(tl), tot, left), ""]
    end = max(tl, key=lambda p: longest(p["id"], t)[0])
    h, path = longest(end["id"], t)
    L += ["Critical path by hours (the longest chain of needs): %.0f h: %s." % (h, " > ".join("%s %s" % (x, by[x]["name"]) for x in path)), ""]
    L += ["What blocks the most (parts that the most other parts need, directly or through others):", ""]
    ranked = sorted(tl, key=lambda p: -len(dependents(p["id"])))[:15]
    for p in ranked:
        L.append("- %s %s: %d parts wait on it; status %s." % (p["id"], p["name"], len(dependents(p["id"])), status(p, t)))
    L.append("")
L += ["## The prototype's order", "", "BUILD-ORDER's stages, each in an order that respects needs (a part after what it needs):", ""]
order = []
seen = set()
def topo(pid):
    if pid in seen: return
    seen.add(pid)
    for n in by[pid]["needs"]:
        if by[n]["leaf"] and is_gameplay(by[n]): topo(n)
    order.append(pid)
for s in "ABCD":
    for p in sorted([p for p in G if stage(p["id"]) == s], key=lambda x: [int(n) for n in x["id"].split(".")]):
        topo(p["id"])
for s in "ABCD":
    ids = [i for i in order if stage(i) == s]
    L.append("- %s: %s" % (NAMES[s], ", ".join(ids)))
L += ["", "## The Unreal phases (a proposal for the order of 23 November's re-plan)", "",
      "Phases U2 to U4 are PLAN.md's phases 2 to 4; U5 is its phase 5; U6 to U9 are the re-plan his ruling of 19 Nov asked for (crime, empire, story and the docks, costed at measured rates). Each part is placed by where it is needed first.", ""]
ph = defaultdict(list)
for p in leaves:
    if "unreal" in p["status"]:
        ph[uphase(p)].append(p)
for k in sorted(UPH):
    rows = ph.get(k, [])
    hh = sum(hours(p, "unreal") for p in rows)
    open_ = [p for p in rows if status(p, "unreal") not in ("built", "passes")]
    L.append("- %s %s: %d parts, about %.0f h (guesses mostly), %d not yet built: %s" % (k, UPH[k], len(rows), hh, len(open_), ", ".join(p["id"] for p in rows)))
L.append("")
open(os.path.join(D, "PLAN-VIEW.md"), "w", encoding="utf-8").write("\n".join(L))

# ---------------- RESEARCH-NEEDED.md ----------------
RN = doc["research_items"]
L = ["# Research needed: felt parts whose standard is still to be measured", "",
     "Rule (his decision of 19 Nov, advisor 257): every part a player feels has a standard, a reference game measured or a rule; a part without one, or whose numbers rest on judgement, is a research item here. Every item names what to measure, in which reference games and how. Measuring is outside only (RULINGS 17 Nov): clips played in Chrome, never downloaded, nothing decompiled or extracted. Generated from PARTS-TREE.json.", "",
     "Items: %d. Felt leaves with no standard at all, resting only on an item: %d." % (len(RN), sum(1 for p in leaves if p["felt"] and p["standard"].lower().startswith("none"))), ""]
for k in sorted(RN, key=lambda x: int(x.split("-")[1])):
    r = RN[k]
    L += ["## %s %s" % (k, r["title"]), "",
          "- Parts: " + ", ".join("%s %s" % (x, by[x]["name"]) for x in r["parts"] if x in by),
          "- Measure: " + r["measure"], "- Reference games: " + r["games"], "- How: " + r["how"], "- Status: " + r["status"], ""]
open(os.path.join(D, "RESEARCH-NEEDED.md"), "w", encoding="utf-8").write("\n".join(L))
print("written: ONESHOT-CHECKLIST.md (%d parts), PLAN-VIEW.md, RESEARCH-NEEDED.md (%d items)" % (len(G), len(RN)))
