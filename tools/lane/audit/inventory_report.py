"""Write INVENTORY.md (plain words, by area) from inventory.json and pc-inventory.json.
Usage: python3 tools/lane/audit/inventory_report.py production/audits/full-2026-11
"""
import collections
import json
import pathlib
import sys

AREA_WORDS = {
    "production": "the studio's records, plans, research, audits and art work",
    "ledger": "the town simulation in C# (the Town session's code and tests)",
    "tools": "the checks and scripts that run the studio and the game's gates",
    "legacy": "the old versions' records (reference only)",
    "ledger-v2": "the second version's research (reference)",
    "ue-probe": "the Unreal project (the builder's)",
    "content": "game content in text form",
    "game-design": "the game's design documents",
    "voice-candidates": "voice samples kept from voice casting",
    "research": "older shared research",
    "ledger-imagegen": "the image generation tools",
    ".claude": "the sessions' skills, agents and settings",
    ".github": "the build workflows on his PC",
    ".githooks": "the shared commit checks",
}


def mb(b):
    return f"{b / 1e6:.1f}"


def esc(t):
    return str(t or "").replace("|", "/").replace("\n", " ")[:120]


def render(inv, pc):
    f = inv["folders"]
    out = ["# Inventory of the repository (full audit, November 2026)", "",
           f"Every folder in the repository (branch wip merged into lane-2026-11), {len(f)} folders, read on {inv['made'][:10]}; "
           f"newest commit {inv['newest_commit']}; full history (shallow: {inv['shallow']}). Made by tools/lane/audit/inventory.py; "
           "the full record per folder is in inventory.json.", "",
           "How to read the status: live (changed lately or referred to and in use), reference (kept to look things up: old versions, research, archives), "
           "stale (referred to but unchanged for over 30 days), dead (nothing refers to it and unchanged for over 21 days), duplicate (same files as another folder). "
           "The status is a first guess by rule, for the stage 2 reviewers to test. It is weakest for code folders: code is rarely named by its path, "
           "so code folders under ledger/ can show as dead while the build still uses them.", ""]
    c = collections.Counter(x["status"] for x in f)
    out += ["## Counts", "", "| Status | Folders |", "|---|---|"] + [f"| {k} | {v} |" for k, v in c.most_common()] + [""]
    top = [x for x in f if x["depth"] == 1]
    out += ["## The areas (top-level folders)", "", "| Folder | What it is | Owner | Last change | Size MB | Files | Folders inside by status |", "|---|---|---|---|---|---|---|"]
    for t in sorted(top, key=lambda x: -x["size_bytes"]):
        inner = collections.Counter(x["status"] for x in f if x["path"].startswith(t["path"] + "/"))
        words = AREA_WORDS.get(t["path"], esc(t["purpose"]))
        out.append(f"| {t['path']} | {words} | {t['owner']} | {t['last_commit']} | {mb(t['size_bytes'])} | {t['file_count_total']} | "
                   + ", ".join(f"{k} {v}" for k, v in inner.most_common()) + " |")
    out.append("")
    for t in sorted(top, key=lambda x: x["path"]):
        subs = [x for x in f if x["depth"] == 2 and x["path"].startswith(t["path"] + "/")]
        if not subs:
            continue
        out += [f"## {t['path']}/", "", "| Folder | Purpose | Owner | Last change | MB | Files | Referred to by | Status (why) |", "|---|---|---|---|---|---|---|---|"]
        for s in sorted(subs, key=lambda x: x["path"]):
            out.append(f"| {s['path']} | {esc(s['purpose'])} | {s['owner']} | {s['last_commit']} | {mb(s['size_bytes'])} | {s['file_count_total']} | "
                       f"{s['referenced_by_incl_descendants']} | {s['status']} ({esc(s['status_reason'])}) |")
        out.append("")
    dead = [x for x in f if x["status"] == "dead" and x["depth"] <= 3]
    out += [f"## Dead at depth 3 or less ({len(dead)})", "", "Nothing in the repository names these and they have not changed in three weeks. Candidates for deletion or archiving, each to be checked by a reviewer first.", ""]
    out += [f"- {x['path']} (last change {x['last_commit']}, {x['file_count_total']} files, {mb(x['size_bytes'])} MB)" for x in sorted(dead, key=lambda x: x["path"])]
    out.append("")
    dup = [x for x in f if x.get("duplicates")]
    out += [f"## Duplicates ({len(dup)})", ""] + ([f"- {x['path']} = {', '.join(x['duplicates'])}" for x in dup] or ["None found by content."]) + [""]
    big = sorted(f, key=lambda x: -x["size_bytes"])
    big = [x for x in big if x["depth"] >= 2][:15]
    out += ["## Largest folders", ""] + [f"- {x['path']}: {mb(x['size_bytes'])} MB, {x['file_count_total']} files ({x['status']})" for x in big] + [""]
    if pc:
        pf = pc["folders"]
        unref = [x for x in pf if not x.get("referenced_by")]
        out += ["## The PC side (from the builder's read-only inventory)", "",
                f"{len(pf)} folders on his PC read on {str(pc.get('made'))[:16]} (folder sizes and dates only, never contents). "
                f"{len(unref)} of them are named by no repository file, tool, retention.json or CATALOGUE.md.", "",
                "| Folder | GB | Files | Last change | Named by |", "|---|---|---|---|---|"]
        for x in sorted(pf, key=lambda x: -(x.get("size_gb") or 0))[:40]:
            out.append(f"| {esc(x['path'])} | {x.get('size_gb')} | {x.get('file_count')} | {x.get('last_modified')} | {len(x.get('referenced_by') or [])} |")
        out += ["", "Named by nothing (the 40 largest):", ""]
        out += [f"- {esc(x['path'])} ({x.get('size_gb')} GB, last change {x.get('last_modified')})" for x in sorted(unref, key=lambda x: -(x.get("size_gb") or 0))[:40]]
        out.append("")
    else:
        out += ["## The PC side", "", "Not yet read: PC areas are seen from the repository only.", ""]
    return "\n".join(out) + "\n"


def main(base):
    b = pathlib.Path(base)
    inv = json.loads((b / "inventory.json").read_text(encoding="utf-8"))
    pcp = b / "pc-inventory.json"
    pc = json.loads(pcp.read_text(encoding="utf-8")) if pcp.exists() else None
    (b / "INVENTORY.md").write_text(render(inv, pc), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1])
