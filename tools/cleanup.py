#!/usr/bin/env python3
"""The one-time cleanup of drive C:, as a page for Jafar to approve first.

    python tools/cleanup.py page      # measures every group and writes production/approvals/<date>-cleanup/
    python tools/cleanup.py check     # every path in the plan is inside the fixed list and not protected
    python tools/cleanup.py --selftest

WHY, 25 September (night). Jafar: "The C: drive is full again two days after
we freed a lot of it, because nothing cleans up after itself. I want the cause
fixed ... and it must be impossible for anything of mine to be deleted."
First, with nothing deleted, one page like the approval pages: what would go,
folder by folder, with sizes and why, and the free space it leaves. He
approves; only then does anything go, and only a group he said yes to.

THE FIXED LIST (CLAUDE.md, Disk) is ALLOWED below. A path outside it is
refused, and so is a PROTECTED one inside it: what he approved, what the game
or a build uses, what the backup covers.

THE DELETING STEP, 26 September, after his approval on the page:
    python tools/cleanup.py delete-group ID    # a group he said yes to (verdicts.json beside the page)
    python tools/cleanup.py rename-old         # the old copies renamed, not deleted
    python tools/cleanup.py restore-old        # their names put back
    python tools/cleanup.py delete-renamed     # only once proofs.json says all three proofs passed
    python tools/cleanup.py sweep-record       # my own recorded rejects on F:
Deletion walks the tree by hand: a link or junction is removed as a link,
never entered, so what it points to is never touched (the self-test proves it
on a throwaway tree).
"""
import json
import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = "2026-09-25"
HOME = os.path.expanduser("~")
LOCAL = os.environ.get("LOCALAPPDATA", os.path.join(HOME, "AppData", "Local"))
RUNNER = r"C:\actions-runner-ledger\_work"

ALLOWED = [
    os.path.join(HOME, "wc26-picks"),
    os.path.join(HOME, "ledger-migrate"),
    os.path.join(REPO, "ue-probe", "Intermediate"), os.path.join(REPO, "ue-probe", "Saved"),
    os.path.join(REPO, "ue-probe", "Packaged"), os.path.join(REPO, "ue-probe", "DerivedDataCache"),
    os.path.join(REPO, "production", "playtest"),
    r"C:\LedgerTools",
    RUNNER,
    os.path.join(LOCAL, "UnrealEngine", "Common"),
]

PROTECTED = [
    r"C:\LedgerTools\mh-assemble",                  # the build machine's cast comes from here
    r"C:\LedgerTools\mh-assemble-before-dressing-2026-09-24",   # the backup covers its MH_Test
    r"C:\LedgerTools\chatterbox-nano",              # the game's live voice runs from here
    r"C:\LedgerTools\blender",                      # the garment and prop scripts run in it
    r"C:\LedgerTools\python312",
    # LINKS, NOT COPIES (25 September): these two point to the only copies on
    # F:. Measured through the link they looked like 7.8 GB of duplicates;
    # deleted "as duplicates", the real files could have gone with them.
    r"C:\LedgerTools\parler-tts", r"C:\LedgerTools\slr83",
    os.path.join(REPO, "ue-probe", "Binaries"),     # the game runs from it
    os.path.join(HOME, "wc26-picks", "tools", "voice-live", "env-export"),   # the live voice loads from here: moved out first
    os.path.join(HOME, "ledger-migrate", "ue-probe", "Packaged"),            # the played copy: moved out first
]


def norm(p):
    return os.path.normcase(os.path.realpath(p))


def inside(path, root):
    try:
        return os.path.commonpath([norm(path), norm(root)]) == norm(root)
    except ValueError:
        return False


def allowed(path):
    """(ok, why): inside the fixed list and not protected."""
    if not any(inside(path, a) for a in ALLOWED):
        return False, "outside the fixed list"
    for p in PROTECTED:
        if inside(path, p) or inside(p, path) and not path_is_parent_ok(path, p):
            return False, "protected: " + p
    return True, "ok"


def path_is_parent_ok(parent, protected):
    """A group may contain a protected path only if the plan moves it out first."""
    return any(inside(protected, m["from"]) for g in PLAN for m in g.get("moveOut", []) if inside(m["from"], parent))


def is_link(path):
    """A symbolic link or a junction: measured as nothing, never walked through."""
    import stat
    try:
        st = os.lstat(path)
    except OSError:
        return False
    return os.path.islink(path) or bool(getattr(st, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def size_gb(path):
    total = 0
    if is_link(path):
        return 0.0
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not is_link(os.path.join(root, d))]
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total / 1e9 if os.path.isdir(path) else (os.path.getsize(path) / 1e9 if os.path.exists(path) else 0.0)


# ---- DELETING, 26 September: only what he approved on the page ------------
#
# His safeguards for the old copies: rename first, delete last (the renamed
# copies go only after the live voice makes a line, a build succeeds and his
# play shortcut opens the game); repoint, never link; secrets never into the
# public repository; settings files never deleted silently (copied to the
# Dropbox backup first); no stashes. And in F:\LedgerTools, only what the
# large-file record names as my own rejected or superseded files.
RENAMED = "to-delete-2026-09-26"
OLD_COPIES = [os.path.join(HOME, "wc26-picks"), os.path.join(HOME, "ledger-migrate")]
ALLOWED += [p + "." + RENAMED for p in OLD_COPIES]
APPROVALS = os.path.join(REPO, "production", "approvals", DATE + "-cleanup")
F_TOOLS = r"F:\LedgerTools"


def record_rejects():
    """The F:\\LedgerTools paths the large-file record names as mine, rejected or superseded."""
    rec = json.load(open(os.path.join(REPO, "production", "large-files.json"), encoding="utf-8"))
    out = []
    for e in rec["entries"]:
        p = os.path.normpath(e["path"])
        if e.get("status") in ("rejected", "superseded") and inside(p, F_TOOLS) and norm(p) != norm(F_TOOLS):
            out.append(p)
    return out


def may_delete(path):
    """(ok, why) for one path to be deleted."""
    if any(norm(path) == norm(x) for x in record_rejects()):
        return True, "my own recorded reject on F:"
    if inside(path, F_TOOLS):
        return False, "F:\\LedgerTools: only my own recorded rejects"
    return allowed(path)


def _long(p):
    p = os.path.abspath(p)
    return p if p.startswith("\\\\?\\") else "\\\\?\\" + p


def remove_tree(path, done):
    """Deletes path and what is inside it. A link or junction is removed as a
    link: never entered, and what it points to is never touched."""
    import stat
    lp = _long(path)
    if is_link(lp):
        try:
            os.rmdir(lp)            # a junction or a directory link: removes the link only
        except OSError:
            os.unlink(lp)           # a file link
        done["links"] += 1
        return
    if os.path.isdir(lp):
        with os.scandir(lp) as it:
            entries = [e.path for e in it]
        for e in entries:
            remove_tree(e, done)
        os.rmdir(lp)
        return
    try:
        size = os.lstat(lp).st_size
        os.chmod(lp, stat.S_IWRITE)
        os.remove(lp)
        done["files"] += 1
        done["bytes"] += size
    except OSError as e:
        done["failed"].append("%s (%s)" % (path, e.strerror))


def delete(path):
    ok, why = may_delete(path)
    if not ok:
        return {"path": path, "refused": why}
    done = {"files": 0, "links": 0, "bytes": 0, "failed": []}
    if os.path.exists(_long(path)) or is_link(_long(path)):
        try:
            remove_tree(path, done)
        except OSError as e:
            done["failed"].append("%s (%s)" % (path, e.strerror))
    return {"path": path, "files": done["files"], "links": done["links"], "gb": round(done["bytes"] / 1e9, 2),
            "failed": done["failed"][:5], "failedCount": len(done["failed"]), "gone": not os.path.exists(_long(path))}


def approved_groups():
    v = json.load(open(os.path.join(APPROVALS, "verdicts.json"), encoding="utf-8"))
    return {k.replace("cleanup-", ""): d.get("pick") for k, d in v.items()}


def delete_group(gid):
    if approved_groups().get(gid) != "yes":
        return [{"group": gid, "refused": "not approved on the page"}]
    g = next(x for x in PLAN if x["id"] == gid)
    if g.get("moveOut"):
        return [{"group": gid, "refused": "an old copy: rename first, prove, then delete-renamed"}]
    return [delete(p) for p in g["paths"]]


def rename_old(back=False):
    out = []
    for p in OLD_COPIES:
        a, b = (p + "." + RENAMED, p) if back else (p, p + "." + RENAMED)
        if os.path.exists(a) and not os.path.exists(b):
            os.rename(a, b)             # same drive: a rename moves nothing
            out.append("%s -> %s" % (a, b))
        else:
            out.append("left: %s (exists %s, target exists %s)" % (a, os.path.exists(a), os.path.exists(b)))
    return out


def delete_renamed():
    proofs = json.load(open(os.path.join(APPROVALS, "proofs.json"), encoding="utf-8"))
    need = ("voiceMakesALine", "buildSucceeds", "shortcutOpensGame", "movedOutVerified", "noStashes", "settingsBackedUp", "leftoversSaved")
    missing = [k for k in need if proofs.get(k) is not True]
    if missing:
        return [{"refused": "proofs not all passed: " + ", ".join(missing)}]
    for gid in ("old-copy-wc26-picks", "old-copy-ledger-migrate"):
        if approved_groups().get(gid) != "yes":
            return [{"refused": gid + " not approved"}]
    return [delete(p + "." + RENAMED) for p in OLD_COPIES]


W = os.path.join(RUNNER, "ledger", "ledger", "ue-probe")
PLAN = [
    {"id": "runner-leftovers", "title": "The build machine's leftovers from its last build",
     "paths": [os.path.join(W, d) for d in ("Packaged", "Saved", "Intermediate", "Binaries")],
     "why": "The last build's packaged game, cooked files, logs and compile scratch. Every build deletes these four itself at its start and makes them again, and its game has already been copied out to the played copy, so nothing reads them between builds.",
     "after": "Nothing changes until the next build, which makes them again as it always does. From now on the build also clears them at its end (a step added to the workflow), so they stop sitting on C: between builds.",
     "recommend": True},
    {"id": "runner-old-workspace", "title": "The build machine's old workspace for wc26-picks",
     "paths": [os.path.join(RUNNER, "wc26-picks")],
     "why": "Left from when this machine built the wc26-picks project. The machine now builds only this project, so nothing uses it.",
     "after": "Nothing changes.", "recommend": True},
    {"id": "old-copy-wc26-picks", "title": "The old copy of the project: wc26-picks",
     "paths": [os.path.join(HOME, "wc26-picks")],
     "moveOut": [
         {"from": os.path.join(HOME, "wc26-picks", "tools", "voice-live", "env-export"), "to": r"F:\LedgerTools\voice-env-export",
          "why": "the game's live voice still loads a library folder from here (its pointer file is changed to the new place)"},
         {"from": os.path.join(HOME, "wc26-picks", "tools", "voice-live", "game-out"), "to": r"F:\LedgerTools\voice-graphs\game-out",
          "why": "the voice model converted for the old Unity player; hours to make again, so kept on F:"},
         {"from": os.path.join(HOME, "wc26-picks", "tools", "voice-live", "export-out"), "to": r"F:\LedgerTools\voice-graphs\export-out",
          "why": "the same, an earlier conversion"}],
     "saveIntoProject": "140 small files found nowhere on GitHub (7 MB): 37 prop models made by the old recipes, the old supervisor's log, two reply receipts, the migration log and bench-spoke.wav; into production/archive/old-copies/wc26-picks/.",
     "why": "Its history is on GitHub: every commit is pushed. Everything else in it is Python environments that can be made again, an old packaged game the played copy replaced, and build output.",
     "after": "The live voice runs from F: (checked by making a line before anything is deleted); the old files are in the project's archive.",
     "recommend": True},
    {"id": "old-copy-ledger-migrate", "title": "The older copy of the project: ledger-migrate",
     "paths": [os.path.join(HOME, "ledger-migrate")],
     "moveOut": [
         {"from": os.path.join(HOME, "ledger-migrate", "ue-probe", "Packaged"), "to": r"F:\LedgerTools\played-game",
          "why": "the played copy of the game, which your 'play the street' shortcut opens and every build refreshes; a link is left at the old place, so the shortcut and the build find it without anything of yours being changed"}],
     "saveIntoProject": "7 small files found nowhere on GitHub (15 MB): the retired studio's supervisor logs and the 11 September answer file; into production/archive/old-copies/ledger-migrate/.",
     "why": "Its history is on GitHub: every commit and branch is pushed. Apart from the played copy, nothing in it is used.",
     "after": "The shortcut opens the same game, now kept on F:.",
     "recommend": True},
    {"id": "project-intermediate", "title": "This project's local compile scratch",
     "paths": [os.path.join(REPO, "ue-probe", "Intermediate")],
     "why": "Compile and cook scratch for the game on this PC.",
     "after": "The next build here makes it again, a few minutes slower, and it grows back to the same size at once, so it frees nothing for long.",
     "recommend": False},
    {"id": "unreal-cache", "title": "Unreal's shared cache",
     "paths": [os.path.join(LOCAL, "UnrealEngine", "Common", "DerivedDataCache"), os.path.join(LOCAL, "UnrealEngine", "Common", "Zen")],
     "why": "Compiled shaders and cooked data that every editor start and every build reuses. All of it was written in the last three days, so all of it is in use.",
     "after": "Every editor start and build would compile for a long time, and it would grow straight back.",
     "recommend": False},
]

NOT_IN_LIST = [
    ("Dropbox", os.path.join(HOME, "Dropbox"), "yours; the backup adds to it and never deletes"),
    ("Windows' hibernation file", r"C:\hiberfil.sys", "a Windows setting you can switch off yourself"),
    ("Windows' swap file", r"C:\pagefile.sys", "Windows'"),
    ("Hugging Face's download cache", os.path.join(HOME, ".cache", "huggingface"), "two speech datasets from August and the voice model; not on your list, so untouched; add it and it can go"),
    ("C:\\LedgerTools\\parler-tts and slr83", r"C:\LedgerTools\slr83",
     "links to the only copies on F:, taking no room on C:; left alone (measured through the link they looked like 7.8 GB of duplicates)"),
    ("F:\\LedgerTools, my own rejected and superseded files", r"F:\LedgerTools", "not on your list; the large-file record lists 13.7 GB of my own there that are rejected or superseded; add it and the end-of-sitting sweep can clear them"),
]


def measure():
    free_c = shutil.disk_usage("C:\\").free / 1e9
    groups = []
    for g in PLAN:
        g = dict(g)
        g["sizes"] = [(p, round(size_gb(p), 2)) for p in g["paths"]]
        g["gb"] = round(sum(s for _, s in g["sizes"]), 1)
        g["movedGb"] = round(sum(size_gb(m["from"]) for m in g.get("moveOut", [])), 1)
        groups.append(g)
    others = []
    for name, p, why in NOT_IN_LIST:
        if p.upper().startswith("F:"):
            # only my own rejected and superseded entries in the large-file record, not the whole folder
            rec = json.load(open(os.path.join(REPO, "production", "large-files.json"), encoding="utf-8"))
            gb = sum(e["mb"] for e in rec["entries"] if e["status"] in ("rejected", "superseded")) / 1000
        else:
            gb = (os.path.getsize(p) / 1e9 if os.path.isfile(p) else size_gb(p)) if os.path.exists(p) else 0.0
        others.append({"name": name, "path": p, "gb": round(gb, 1), "why": why})
    return {"freeC": round(free_c, 1), "freeF": round(shutil.disk_usage("F:\\").free / 1e9, 1) if os.path.exists("F:\\") else None,
            "groups": groups, "others": others}


def check():
    bad = []
    for g in PLAN:
        for p in g["paths"]:
            if is_link(p):
                bad.append((g["id"], p, "a link: removing it could reach what it points to"))
            if not any(inside(p, a) for a in ALLOWED):
                bad.append((g["id"], p, "outside the fixed list"))
            for q in PROTECTED:
                if inside(p, q):
                    bad.append((g["id"], p, "protected: " + q))
                elif inside(q, p) and not any(inside(q, m["from"]) for m in g.get("moveOut", [])):
                    bad.append((g["id"], p, "holds a protected path not moved out first: " + q))
        for m in g.get("moveOut", []):
            if not any(inside(m["from"], a) for a in ALLOWED):
                bad.append((g["id"], m["from"], "moves from outside the fixed list"))
    return bad


PAGE = r"""<title>Drive C Cleanup</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=Courier+Prime:wght@400;700&display=swap">
<style>
:root{
  --ground:#e9ecea; --surface:#f6f7f6; --ink:#1b2224; --muted:#56636a; --rule:#c9d0d0;
  --accent:#9a3e2b; --ok:#2e6a48; --chip:#dde2e1;
  --display:"Archivo Narrow","Arial Narrow",Arial,sans-serif;
  --body:"Source Serif 4",Georgia,"Times New Roman",serif;
  --type:"Courier Prime","Courier New",Courier,monospace;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ground:#121617; --surface:#1a2022; --ink:#e3e8e7; --muted:#98a4a7; --rule:#2d3639;
    --accent:#d27352; --ok:#63b384; --chip:#242c2e; color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --ground:#121617; --surface:#1a2022; --ink:#e3e8e7; --muted:#98a4a7; --rule:#2d3639;
  --accent:#d27352; --ok:#63b384; --chip:#242c2e; color-scheme:dark;
}
*{box-sizing:border-box}
body{background:var(--ground);color:var(--ink);font:16px/1.5 var(--body);padding-inline:16px;padding-block:28px 64px}
.wrap{max-width:1000px;margin:0 auto;display:grid;gap:28px}
header{display:grid;gap:10px;border-bottom:2px solid var(--ink);padding-bottom:18px}
.kicker{font:700 12px/1 var(--type);letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
h1{font:700 clamp(30px,5vw,46px)/1.02 var(--display);margin:0;text-wrap:balance}
h2{font:700 clamp(22px,3.4vw,28px)/1.05 var(--display);margin:0;text-wrap:balance}
h3{font:600 15px/1 var(--display);letter-spacing:.06em;text-transform:uppercase;margin:0}
.how{margin:0;max-width:70ch;color:var(--muted)}
.meter{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.meter div{background:var(--surface);border:1px solid var(--rule);padding:12px}
.meter b{display:block;font:700 30px/1 var(--display);font-variant-numeric:tabular-nums}
.meter span{font:400 13px var(--type);color:var(--muted)}
section.group{display:grid;gap:12px;background:var(--surface);border:1px solid var(--rule);padding:20px}
section.group.rec{box-shadow:inset 4px 0 0 var(--ok)}
.gb{font:700 22px/1 var(--display);font-variant-numeric:tabular-nums}
table{border-collapse:collapse;width:100%;font:400 14px/1.4 var(--type)}
td{border-top:1px solid var(--rule);padding:6px 4px;vertical-align:top;word-break:break-all}
td.n{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums;word-break:normal}
.tbl{overflow-x:auto}
p{margin:0;max-width:72ch}
.lbl{font:700 12px/1 var(--type);letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}
.row{display:flex;flex-wrap:wrap;gap:14px;align-items:center}
label.pick{display:flex;align-items:center;gap:6px;font:400 14px var(--type)}
textarea{width:100%;min-height:50px;font:15px/1.4 var(--body);color:var(--ink);background:var(--ground);border:1px solid var(--rule);padding:8px}
.saved,.tally{font:400 13px var(--type);color:var(--muted)}
footer{font:400 13px/1.5 var(--type);color:var(--muted);border-top:1px solid var(--rule);padding-top:14px}
</style>
<div class="wrap">
  <header>
    <div class="kicker">LEDGER · cleanup page · 25 September, night</div>
    <h1>What would go from drive C, and why</h1>
    <p class="how">Nothing has been deleted. Each group below is a folder or a few, with its size, why it can go, and what happens after. Say yes or no to each; only the groups you say yes to go, and only inside the list you gave (now in CLAUDE.md). Anything that must survive is moved to F: first and checked there. Groups I would not delete are shown too, marked, so you see everything I looked at.</p>
    <div class="meter" id="meter"></div>
    <div class="tally" id="tally"></div>
  </header>
  <main class="wrap" id="groups"></main>
  <section class="group"><h2>Not on your list, so not touched</h2><div class="tbl"><table id="others"></table></div></section>
  <section class="group"><h2>What stops it filling again</h2>
    <p>1. The build machine clears its build leftovers at the end of each build, not only at the start. 2. Every large file I make is recorded (production/large-files.json), and at the end of each sitting only my own rejected or superseded ones go, only inside your list. 3. My scratch and downloads go to drive F. 4. The backup never lets drive C fall below 1.8 GB free. 5. Each summary shows free space on C: before and after; under 60 GB, this page comes first next time.</p>
  </section>
  <footer>Sizes measured __WHEN__ by tools/cleanup.py, which refuses any path outside the list or protected (what you approved, what the game or a build uses, what the backup covers).</footer>
</div>
<script>
const DATA = __DATA__;
const state = {};
let db = null;
function el(tag, attrs, ...kids){ const n = document.createElement(tag); for (const [k,v] of Object.entries(attrs||{})) { if (k === "class") n.className = v; else if (k === "text") n.textContent = v; else n.setAttribute(k, v); } for (const k of kids) if (k) n.append(k); return n; }
function save(key, patch){ state[key] = Object.assign({}, state[key] || {}, patch, {at: new Date().toISOString()}); render(); if (db) db.doc("verdicts/" + key).set(Object.assign({}, state[key])).catch(() => {}); }
function gb(x){ return (Math.round(x * 10) / 10).toFixed(1) + " GB"; }
function render(){
  let yes = 0, judged = 0;
  const root = document.getElementById("groups"); root.replaceChildren();
  for (const g of DATA.groups) {
    const k = "cleanup-" + g.id, st = state[k] || {};
    if (st.pick) judged++;
    if (st.pick === "yes") yes += g.gb;
    const sec = el("section", {class:"group" + (g.recommend ? " rec" : "")});
    sec.append(el("div", {class:"row"}, el("h2", {text:g.title}), el("span", {class:"gb", text:gb(g.gb)})));
    sec.append(el("div", {class:"lbl", text: g.recommend ? "I recommend: yes" : "I recommend: keep"}));
    const t = el("table"); for (const [p, s] of g.sizes) t.append(el("tr", {}, el("td", {text:p}), el("td", {class:"n", text:gb(s)})));
    sec.append(el("div", {class:"tbl"}, t));
    sec.append(el("p", {}, el("b", {text:"Why it can go. "}), document.createTextNode(g.why)));
    if (g.moveOut && g.moveOut.length) { const m = el("table"); for (const x of g.moveOut) m.append(el("tr", {}, el("td", {text:"moved first: " + x.from + " → " + x.to + " (" + x.why + ")"}))); sec.append(el("div", {class:"tbl"}, m)); }
    if (g.saveIntoProject) sec.append(el("p", {}, el("b", {text:"Saved into the project first. "}), document.createTextNode(g.saveIntoProject)));
    sec.append(el("p", {}, el("b", {text:"After. "}), document.createTextNode(g.after)));
    const picks = el("div", {class:"row"});
    for (const [v, txt] of [["yes", "Yes, it can go"], ["no", "No, keep it"]]) { const id = "p-" + g.id + "-" + v; const r = el("input", {type:"radio", name:"p-" + g.id, id, value:v}); if (st.pick === v) r.checked = true; r.addEventListener("change", () => save(k, {pick:v})); picks.append(el("label", {class:"pick", for:id}, r, document.createTextNode(txt))); }
    const note = el("textarea", {placeholder:"A word, if any (optional)"}); note.value = st.note || ""; note.addEventListener("change", () => save(k, {note:note.value}));
    sec.append(picks, note, el("span", {class:"saved", text: st.at ? "Saved " + new Date(st.at).toLocaleString() : ""}));
    root.append(sec);
  }
  const rec = DATA.groups.filter(g => g.recommend).reduce((a, g) => a + g.gb, 0);
  document.getElementById("meter").replaceChildren(
    el("div", {}, el("b", {text:gb(DATA.freeC)}), el("span", {text:"free on C: now"})),
    el("div", {}, el("b", {text:gb(DATA.freeC + rec)}), el("span", {text:"free after the groups I recommend"})),
    el("div", {}, el("b", {text:gb(DATA.freeC + yes)}), el("span", {text:"free after the groups you said yes to"})),
    el("div", {}, el("b", {text:gb(DATA.freeF - DATA.groups.filter(g => g.recommend).reduce((a, g) => a + (g.movedGb || 0), 0))}), el("span", {text:"free on F: after the moves"})));
  document.getElementById("tally").textContent = judged + " of " + DATA.groups.length + " groups answered" + (db ? "" : " · answers are not being stored on this view");
  const o = document.getElementById("others"); o.replaceChildren();
  for (const x of DATA.others) o.append(el("tr", {}, el("td", {text:x.name}), el("td", {class:"n", text:gb(x.gb)}), el("td", {text:x.why})));
}
render();
(async () => { try { db = window.claude && window.claude.use ? await window.claude.use("db") : null; } catch (e) { db = null; }
  if (!db) { render(); return; }
  for (const g of DATA.groups) { try { const s = await db.doc("verdicts/cleanup-" + g.id).get(); if (s.exists) state["cleanup-" + g.id] = Object.assign({}, s.data()); } catch (e) {} }
  render(); })();
</script>
"""


def page():
    import datetime
    data = measure()
    out = os.path.join(REPO, "production", "approvals", DATE + "-cleanup")
    os.makedirs(out, exist_ok=True)
    json.dump(data, open(os.path.join(out, "plan.json"), "w", encoding="utf-8"), indent=1)
    html = PAGE.replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<" + chr(92) + "/")).replace(
        "__WHEN__", datetime.datetime.now().strftime("%d %B %Y, %H:%M"))
    open(os.path.join(out, "index.html"), "w", encoding="utf-8", newline="\n").write(html)
    rec = sum(g["gb"] for g in data["groups"] if g["recommend"])
    print("cleanup page: free C %.1f GB now, %.1f GB after the recommended groups (%.1f GB); groups=%d" % (
        data["freeC"], data["freeC"] + rec, rec, len(data["groups"])))


def selftest():
    ok = bad = 0

    def check_(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("cleanup selftest FAIL " + name)
    check_("the plan is inside the fixed list and spares what is protected", check() == [])
    check_("his Documents are refused", not allowed(os.path.join(HOME, "Documents", "x"))[0])
    check_("his Desktop is refused", not allowed(os.path.join(HOME, "Desktop"))[0])
    check_("his Downloads are refused", not allowed(os.path.join(HOME, "Downloads", "a.zip"))[0])
    check_("his Dropbox is refused", not allowed(os.path.join(HOME, "Dropbox", "LEDGER backup"))[0])
    check_("the build machine's cast source is refused", not allowed(r"C:\LedgerTools\mh-assemble\Content")[0])
    check_("the game's live voice is refused", not allowed(r"C:\LedgerTools\chatterbox-nano\env-dml")[0])
    check_("a place on the list is allowed", allowed(os.path.join(HOME, "wc26-picks", "ue-probe"))[0])
    check_("a link to F: is refused", not allowed(r"C:\LedgerTools\slr83")[0])
    src = open(os.path.abspath(__file__), encoding="utf-8").read().split("def selftest")[0]
    check_("no rmtree or move anywhere: deletion walks by hand, links as links", all(w not in src for w in ("shutil.rmtree", "shutil.move(")))
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        target = os.path.join(t, "target")
        os.makedirs(target)
        open(os.path.join(target, "keep.txt"), "w").write("keep")
        tree = os.path.join(t, "tree", "deep")
        os.makedirs(tree)
        open(os.path.join(tree, "a.txt"), "w").write("a")
        subprocess.run(["cmd", "/c", "mklink", "/J", os.path.join(tree, "link"), target], capture_output=True)
        check_("the test junction was made", is_link(os.path.join(tree, "link")))
        done = {"files": 0, "links": 0, "bytes": 0, "failed": []}
        remove_tree(os.path.join(t, "tree"), done)
        check_("a tree with a junction inside is deleted", not os.path.exists(os.path.join(t, "tree")))
        check_("and what the junction pointed to is untouched", open(os.path.join(target, "keep.txt")).read() == "keep")
        check_("the junction was removed as a link", done["links"] == 1 and done["files"] == 1)
    check_("F:\\LedgerTools itself is refused", not may_delete(F_TOOLS)[0])
    check_("a file on F: not in the record is refused", not may_delete(os.path.join(F_TOOLS, "played-game"))[0])
    check_("his Documents are refused for deletion", "refused" in delete(os.path.join(HOME, "Documents", "nothing-here")))
    print("cleanup selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "page":
        page()
    elif cmd == "delete-group":
        print(json.dumps(delete_group(sys.argv[2]), indent=1))
    elif cmd == "rename-old":
        print("\n".join(rename_old()))
    elif cmd == "restore-old":
        print("\n".join(rename_old(back=True)))
    elif cmd == "delete-renamed":
        print(json.dumps(delete_renamed(), indent=1))
    elif cmd == "sweep-record":
        print(json.dumps([delete(p) for p in record_rejects()], indent=1))
    else:
        problems = check()
        for p in problems:
            print("REFUSED", *p)
        print("cleanup check: %s" % ("ok" if not problems else "%d problem(s)" % len(problems)))
        sys.exit(1 if problems else 0)
