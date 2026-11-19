#!/usr/bin/env python3
"""Recompute every heading's status in PARTS-TREE.json from its leaves (the mode, ties to the lower status), in place."""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
F = os.path.join(ROOT, "production", "lane", "parts-tree", "PARTS-TREE.json")
ORDER = ["missing", "designed", "built shallow", "built", "passes", "unknown"]
doc = json.load(open(F, encoding="utf-8"))
by = {p["id"]: p for p in doc["parts"]}
def leaves(p):
    return [p] if p["leaf"] else [x for c in p["children"] for x in leaves(by[c])]
for p in doc["parts"]:
    if p["leaf"]:
        continue
    st = {}
    for t in ("prototype", "unreal"):
        cnt = {}
        for x in leaves(p):
            if t in x["status"]:
                k = x["status"][t]["status"]; cnt[k] = cnt.get(k, 0) + 1
        if cnt:
            mode = max(cnt, key=lambda k: (cnt[k], -ORDER.index(k)))
            st[t] = {"status": mode, "evidence": "rollup of %d leaves: %s" % (sum(cnt.values()), ", ".join("%s %d" % (k, cnt[k]) for k in ORDER if k in cnt))}
    p["status"] = st
    p["track"] = "both" if len(st) == 2 else next(iter(st))
json.dump(doc, open(F, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rollups recomputed")
