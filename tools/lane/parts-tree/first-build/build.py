import csv, json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import tree_a, tree_b, tree_c, tree_d, tree_e  # noqa
from tree_a import PARTS
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "production", "lane", "parts-tree", "work") + "/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "production", "lane", "parts-tree", "PARTS-TREE.json")

def key(i): return [int(x) for x in i.split(".")]
parts = {p["id"]: p for p in PARTS}
assert len(parts) == len(PARTS), "duplicate ids"

RN = json.load(open(os.path.join(os.path.dirname(__file__), "research.json")))

proto = {r["part_id"]: r for r in csv.DictReader(open(W + "status-prototype.csv"))}
unreal = {r["part_id"]: r for r in csv.DictReader(open(W + "status-unreal.csv"))}
NEWMAP = {"Collision and physics": "8.10", "Crowd movement and avoidance": "2.1.5", "Animals and birds": "4.11",
          "Coat, pockets and storage": "1.6.9", "Platform account, cloud and achievements": "10.7", "Photo mode": "6.8"}
checks, ruled = {}, []
feat = {}
for line in open("/home/claude/ledger/production/research/feature-coverage/MASTER-CHECKLIST.md"):
    m = re.match(r"\| ([A-Z]\d+(?:\.\d+)?) \| (.+?) \|", line)
    if m: feat[m.group(1)] = m.group(2)
for r in csv.DictReader(open(W + "map-checklist.csv")):
    pid = r["part_id"]
    if r["verdict"] == "NEW":
        nm = r["note"].split("name=")[1].strip()
        pid = NEWMAP[nm]
    if r["verdict"] == "RULED_OUT":
        ruled.append({"item": r["item_id"], "feature": feat.get(r["item_id"], ""), "ruled_out_by": r["note"]}); continue
    checks.setdefault(pid, []).append(r["item_id"])
themes = {}
for line in open(W + "map-players.md"):
    c = [x.strip() for x in line.split("|")]
    if len(c) > 5 and re.match(r"^[A-Z]{1,2}\d+$", c[1]) and c[3] in ("MAP", "GAP"):
        for pid in re.findall(r"\d+(?:\.\d+)*", c[4]):
            themes.setdefault(pid, []).append(c[1] + " " + c[2])
# gap-fixes that answer player GAP themes
themes.setdefault("6.8", []).append("A9 photo mode (players asked for)")
themes.setdefault("10.2", []).append("P7/X2 price, length and value")
themes.setdefault("2.4.4", []).append("S4 gossip timeliness in the first 30 real minutes")
themes.setdefault("10.6", []).append("A10 mods position")

OVR = {
 ("1.1.1", "unreal"): ("built", "walk passed his eye 26 Oct for its look (RULINGS People's moves), but ER-INPUT-01 is not measured in Unreal and feel numbers are a research item; open faults: treads on the spot at Mickey's front, foot slide unmeasured since 22 Oct (FINDINGS.md)"),
 ("5.2.1", "unreal"): ("built", "third motion-matching try is the default (RULINGS, his eye 26 Oct); foot slide is an open fault (FINDINGS.md, phase1-exit EXIT-B 9 Nov) and its test never ran"),
 ("2.14", "prototype"): ("built", "src/rules.js gives each named person nerve, talk, discretion, fear and liking; test 6.08 checks only that values sit in the table; nothing tests that the same deed goes differently by person; the standard waits on his answer to QUESTIONS 3"),
 ("7.9", "prototype"): ("built", "beaten Tom wakes at Rinaldi's and custody ends (test/town.mjs), but no failure route is timed against ER-CORE-04's 2 minutes; NOT_DONE: ER-CORE-02 to 04 checked only for a crash, a run-down and a wedged cab"),
 ("1.2.3", "prototype"): ("built", "F in and out works and a blocked door never strands him (gate6.mjs), but gate6 accepts up to 5 s at a blocked door against ER-DRIVE-07's 2 s, and both sides are not timed"),
 ("6.1.1", "prototype"): ("built", "gate6.mjs checks the prompt's target and hold, but 'everything usable has a prompt' is unchecked (NOT_DONE: prompts not searched one by one; GATE-REVIEW-2026-11-19: no help prompt after a run-down)"),
 ("2.3.1", "prototype"): ("built", "memory kept per person and a scripted week compares part for part after save and load (same_week.mjs, town.mjs), but the reload-at-random-moments test did not run"),
 ("7.13", "prototype"): ("passes", "rules.js realSecondsPerGameHour 45; the prototype's live test 6.01 (round 6 build) shows one game hour is 45 real s; his clock decision C11 is still open"),
 ("9.4", "prototype"): ("missing", "ONE-SHOT-PORTING.md does not exist yet (advisor 254 asks for it)"),
 ("9.4", "unreal"): ("missing", "ONE-SHOT-PORTING.md does not exist yet; no system has been ported from the prototype under shared tests"),
 ("5.4.3", "unreal"): ("missing", "no design in detail and no build evidence (D28 owed)"),
 ("9.3", "prototype"): ("built shallow", "the real town rules compiled for the browser match 102,949 golden rows and six weeks (ONE-SIM-METHOD-2026-11-19, tools/lane/one-sim, run 3 breaker 191 of 191), but not yet swapped into the prototype (DIFFERENCES.md: seven decisions for the swap)"),
 ("9.6", "prototype"): ("built", "src/rules.js holds 1,313 numbers and npm run numbers fails on a new one, but 1,053 small numbers were never examined (NOT_DONE 3), so the one-home standard is not yet met"),
}
STAT = {"missing", "designed", "built shallow", "built", "passes", "unknown"}
def norm(s):
    s = (s or "").strip().lower()
    return s if s in STAT else "unknown"

out = []
for pid in sorted(parts, key=key):
    p = parts[pid]
    par = ".".join(pid.split(".")[:-1]) if "." in pid else ("0" if pid != "0" else None)
    tr = p.get("tr", "both")
    hp, hu, hb = (p.get("h") or "|||").split("|")[:3] if p.get("h") else ("", "", "not estimated")
    rl, rw = (p.get("rk") or "low|").split("|", 1)
    st = {}
    notes = []
    if tr in ("both", "prototype"):
        r = proto.get(pid)
        s = norm(r["proto_status"]) if r else "unknown"
        ev = r["evidence"] if r else "no evidence gathered (part added after the status sweep)"
        if s == "passes" and p.get("rn"):
            s = "built"; notes.append("prototype check passes its rule, but the feel standard is a research item, so not 'passes'")
        if not r and "not designed" not in str(p.get("des", "not designed")):
            s, ev = "designed", "design exists (%s); build not checked by the status sweep" % p.get("des")
        st["prototype"] = {"status": s, "evidence": ev}
    if tr in ("both", "unreal"):
        r = unreal.get(pid)
        s = norm(r["unreal_status"]) if r else "unknown"
        ev = r["evidence"] if r else "no evidence gathered (part added after the status sweep)"
        if not r and "not designed" not in str(p.get("des", "not designed")):
            s, ev = "designed", "design exists (%s); build not checked by the status sweep" % p.get("des")
        st["unreal"] = {"status": s, "evidence": ev}
    if tr == "unreal" and pid in proto and norm(proto[pid]["proto_status"]) not in ("unknown", "missing", "designed"):
        notes.append("prototype has a stand-in: " + proto[pid]["evidence"][:160])
    for (oid, tk), (os_, oev) in OVR.items():
        if oid == pid and tk in st:
            notes.append("status set by the parts-tree session over the sweep's '%s': %s" % (st[tk]["status"], oev))
            st[tk] = {"status": os_, "evidence": oev}
    rev = proto.get(pid, {}).get("review_themes", "") if pid in proto else ""
    std = p.get("std", "none")
    rec = {
        "id": pid, "level": 0 if pid == "0" else len(pid.split(".")), "parent": par, "name": p["name"], "what": p["what"],
        "felt": bool(p.get("f", 0)), "standard": std, "standard_source": p.get("ss", "none"),
        "research_items": p.get("rn", []), "designed_in": p.get("des", "not designed"), "track": tr, "status": st,
        "needs": p.get("n", []), "blocks": [], "hours": {"prototype": hp, "unreal": hu, "basis": hb},
        "risk": {"level": rl.strip(), "why": rw.strip()}, "test": p.get("t", "none"), "owner": p.get("o", "builder"),
        "checklist_items": checks.get(pid, []), "review_themes": ([rev] if rev else []) + themes.get(pid, []),
        "notes": notes, "children": []}
    out.append(rec)
by = {r["id"]: r for r in out}
for r in out:
    if r["parent"]: by[r["parent"]]["children"].append(r["id"])
    for n in r["needs"]:
        if n in by: by[n]["blocks"].append(r["id"])
        else: print("MISSING NEED", r["id"], n)
for r in out:
    r["leaf"] = not r["children"]
ORDER = ["missing", "designed", "built shallow", "built", "passes", "unknown"]
def leaves_under(r):
    if r["leaf"]: return [r]
    return [x for c in r["children"] for x in leaves_under(by[c])]
for r in out:
    if r["leaf"]: continue
    lv = leaves_under(r)
    for t in list(r["status"].keys()):
        cnt = {}
        for x in lv:
            if t in x["status"]: cnt[x["status"][t]["status"]] = cnt.get(x["status"][t]["status"], 0) + 1
        if not cnt:
            del r["status"][t]; continue
        mode = max(cnt, key=lambda k: (cnt[k], -ORDER.index(k)))
        r["status"][t] = {"status": mode, "evidence": "rollup of %d leaves: %s" % (sum(cnt.values()), ", ".join("%s %d" % (k, cnt[k]) for k in ORDER if k in cnt))}
    ks = set(r["status"])
    r["track"] = "both" if ks == {"prototype", "unreal"} else next(iter(ks))
doc = {"title": "LEDGER parts tree", "version": "2026-11-20", "built_by": "parts-tree cloud session, Opus 5.5",
       "statuses": sorted(STAT), "parts": out, "ruled_out_checks": ruled, "research_items": RN}
json.dump(doc, open(OUT, "w"), indent=1, ensure_ascii=False)
print(len(out), "parts;", sum(r["leaf"] for r in out), "leaves;", sum(len(v) for v in checks.values()), "checks mapped;", len(ruled), "ruled out")
