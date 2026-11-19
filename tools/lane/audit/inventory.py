#!/usr/bin/env python3
"""Folder inventory for the full-2026-11 audit.

Read-only on the repository. Writes inventory.json and work/inventory-table.md
into --out.

    python3 tools/lane/audit/inventory.py --repo . --out production/audits/full-2026-11

Notes on method (heuristics, all recorded in the output):
  * last_commit: one `git log --name-only --format=@@%cs` pass, dates propagated
    to every ancestor folder.
  * referenced_by: one ripgrep run over text files (<= 2 MB, binaries skipped,
    .gitignore respected).  Patterns are the folder paths (forward slash,
    backslash, JSON-escaped double backslash), longest first.  Unlike a bare -F
    substring search each hit must sit on a path boundary (not preceded by a
    word char, '/', '\\' or '-'; not followed by a word char, '.', '-' unless the
    '.' ends a sentence), and a top-level folder name only counts when followed
    by a slash, otherwise words like "tools" or "content" would match everywhere.
    A reference is credited to the longest folder path it names.
  * Files that are inside the folder never count as referencing it.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from collections import defaultdict

# ---------------------------------------------------------------- owner table
# Tier 1 wins over everything; tier 2 is the clothing name rule; tier 3 the rest.
# Longest matching prefix wins inside a tier.  A prefix matches the folder itself
# and everything below it.
OWNER_TIER1 = {
    "tools/lane": "lane",
    "production/lane": "lane",
    "production/research/lane": "lane",
    "production/audits/full-2026-11": "lane",
    "ledger-v2": "reference (old version)",
    "ledger": "town (simulation)",
    "legacy": "none (archive)",
    "production/archive": "none (archive)",
    "production/research": "shared research",
    "research": "shared research",
}
CLOTHING_PREFIXES = {"production/clothing": "clothing"}
CLOTHING_WORDS = ("clothing", "garment")
OWNER_TIER3 = {
    "ue-probe": "builder",
    "content": "builder",
    "ledger-imagegen": "builder",
    "voice-candidates": "builder",
    "production/art": "builder",
    "production/cast": "builder",
    "production/casting": "builder",
    "game-design": "design",
    "tools": "builder",
}
# Folders strictly below these (not the folder itself) fall back to this owner.
OWNER_UNDER = {"production": "builder"}
OWNER_DEFAULT = "shared"

README_NAMES = ("README.md", "README.txt", "INDEX.md")
REFERENCE_PREFIXES = ("legacy", "ledger-v2", "production/archive", "research",
                      "production/research")
REFERENCE_NAMES = {"archive", "archives", "reference", "references"}
DEAD_DAYS = 21
STALE_DAYS = 30
MAX_RG_FILESIZE = "2M"


def _under(path, prefix):
    return path == prefix or path.startswith(prefix + "/")


def _best(path, table):
    hits = [p for p in table if _under(path, p)]
    return table[max(hits, key=len)] if hits else None


def owner_of(path):
    o = _best(path, OWNER_TIER1)
    if o:
        return o
    low = path.lower()
    if _best(path, CLOTHING_PREFIXES) or any(w in low for w in CLOTHING_WORDS):
        return "clothing"
    o = _best(path, OWNER_TIER3)
    if o:
        return o
    for p, o in OWNER_UNDER.items():
        if path.startswith(p + "/"):
            return o
    return OWNER_DEFAULT


# ------------------------------------------------------------------- helpers
def run(cmd, cwd, check=True):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, check=check)


def parse_date(s):
    return dt.date.fromisoformat(s) if s else None


def clean_line(line):
    line = line.strip()
    line = re.sub(r"^(#+\s*|>\s*|[-*+]\s+|\d+\.\s+)", "", line)
    line = re.sub(r"[*_`]{1,3}", "", line)
    line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
    return re.sub(r"\s+", " ", line).strip()


def purpose_of(abs_dir):
    try:
        names = {n.lower(): n for n in os.listdir(abs_dir)}
    except OSError:
        return ""
    for want in README_NAMES:
        real = names.get(want.lower())
        if not real:
            continue
        try:
            with open(os.path.join(abs_dir, real), "r", encoding="utf-8",
                      errors="replace") as fh:
                text = fh.read(16384)
        except OSError:
            continue
        lines = text.splitlines()
        i = 0
        if lines and lines[0].strip() == "---":  # front matter
            for j in range(1, len(lines)):
                if lines[j].strip() == "---":
                    i = j + 1
                    break
        first_heading = ""
        in_fence = False
        in_comment = False
        for raw in lines[i:]:
            s = raw.strip()
            if s.startswith("```") or s.startswith("~~~"):
                in_fence = not in_fence
                continue
            if in_fence or not s:
                continue
            if in_comment:
                if "-->" in s:
                    in_comment = False
                continue
            if s.startswith("<!--"):
                if "-->" not in s:
                    in_comment = True
                continue
            if re.fullmatch(r"[-=*_~\s|:]{3,}", s) or s.startswith("![") or \
                    s.startswith("[!["):
                continue
            if s.startswith("#"):
                if not first_heading:
                    first_heading = clean_line(s)
                continue
            c = clean_line(s)
            if c:
                return c[:160]
        return first_heading[:160]
    return ""


def sha1_file(path):
    h = hashlib.sha1()
    try:
        if os.path.islink(path):
            h.update(b"link:" + os.readlink(path).encode("utf-8", "replace"))
        else:
            with open(path, "rb") as fh:
                while True:
                    b = fh.read(1 << 20)
                    if not b:
                        break
                    h.update(b)
    except OSError:
        h.update(b"unreadable")
    return h.hexdigest()


# --------------------------------------------------------------- tree walking
def walk_tree(repo):
    """Return (folders, files). folders: {rel: {'direct': n}}, files: {rel: size}."""
    folders = {}
    files = {}
    for root, dirs, fnames in os.walk(repo, followlinks=False):
        dirs[:] = [d for d in dirs if d != ".git" and d != "node_modules"]
        rel = os.path.relpath(root, repo).replace(os.sep, "/")
        if rel == ".":
            rel = ""
        if rel:
            folders[rel] = {"direct": 0}
        # symlinks to directories are listed in dirs but never descended into
        # by os.walk(followlinks=False); count them as files instead.
        for d in list(dirs):
            if os.path.islink(os.path.join(root, d)):
                dirs.remove(d)
                fnames.append(d)
        for f in fnames:
            try:
                size = os.lstat(os.path.join(root, f)).st_size
            except OSError:
                size = 0
            frel = (rel + "/" + f) if rel else f
            files[frel] = size
            if rel:
                folders[rel]["direct"] += 1
    return folders, files


def ancestors(path):
    """'a/b/c' -> ['a/b', 'a'] (excluding itself)."""
    parts = path.split("/")
    return ["/".join(parts[:i]) for i in range(len(parts) - 1, 0, -1)]


def git_dates(repo):
    """One git log pass. Returns ({folder: 'YYYY-MM-DD'}, newest)."""
    out = run(["git", "-c", "core.quotepath=off", "log", "--name-only",
               "--format=@@%cs"], repo, check=False).stdout.decode("utf-8", "replace")
    dates = {}
    newest = ""
    cur = ""
    for line in out.splitlines():
        if line.startswith("@@"):
            cur = line[2:].strip()
            if cur > newest:
                newest = cur
            continue
        if not line or not cur:
            continue
        for a in ancestors(line):
            if dates.get(a, "") < cur:
                dates[a] = cur
    return dates, newest


# ------------------------------------------------------------------ rg refs
def _rx_escape(s):
    return re.sub(r"([\\.+*?()|\[\]{}^$])", r"\\\1", s)


def build_patterns(folder_paths):
    pats = []
    lead = r"(?:^|[^\w/\\-])"
    trail_any = r"(?:$|[^\w.\-]|\.(?:\s|$))"
    trail_slash = r"[/\\]"
    for p in folder_paths:
        trail = trail_slash if "/" not in p else trail_any
        variants = {p}
        if "/" in p:
            variants.add(p.replace("/", "\\"))
            variants.add(p.replace("/", "\\\\"))
        for v in variants:
            pats.append((len(v), lead + _rx_escape(v) + trail))
    pats.sort(key=lambda t: -t[0])
    return [p for _, p in pats]


def find_references(repo, folder_paths, exclude_files=()):
    """Return {folder: set(files)} of files that mention the folder path."""
    refs = defaultdict(set)
    if not folder_paths:
        return refs
    known = set(folder_paths)
    with tempfile.NamedTemporaryFile("w", suffix=".pat", delete=False,
                                     encoding="utf-8") as tf:
        tf.write("\n".join(build_patterns(sorted(known))) + "\n")
        patfile = tf.name
    try:
        cmd = ["rg", "--hidden", "-o", "--null", "--no-line-number",
               "--with-filename", "--no-heading", "--max-filesize", MAX_RG_FILESIZE,
               "--no-config", "--regex-size-limit", "2G", "--dfa-size-limit", "2G",
               "-g", "!.git", "-g", "!node_modules"]
        for ex in exclude_files:
            cmd += ["-g", "!" + ex]
        cmd += ["-f", patfile, "."]
        proc = subprocess.Popen(cmd, cwd=repo, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        buf = b""
        while True:
            chunk = proc.stdout.read(1 << 20)
            if not chunk:
                break
            buf += chunk
            lines = buf.split(b"\n")
            buf = lines.pop()
            for ln in lines:
                _consume(ln, known, refs)
        if buf:
            _consume(buf, known, refs)
        err = proc.stderr.read().decode("utf-8", "replace")
        proc.wait()
        if proc.returncode == 2 and ("regex" in err or "error" in err.lower()) \
                and not refs:
            raise RuntimeError("ripgrep failed: " + err[:500])
    finally:
        os.unlink(patfile)
    return refs


def _consume(line, known, refs):
    if b"\0" not in line:
        return
    fname, match = line.split(b"\0", 1)
    fname = fname.decode("utf-8", "replace")
    if fname.startswith("./"):
        fname = fname[2:]
    fname = fname.replace("\\", "/")
    m = match.decode("utf-8", "replace").replace("\\\\", "/").replace("\\", "/")
    for lead in (0, 1):
        for trail in (0, 1, 2):
            core = m[lead:len(m) - trail]
            if core not in known:
                core = core.rstrip("/")
            if core in known:
                if not (fname == core or fname.startswith(core + "/")):
                    refs[core].add(fname)
                return


# ------------------------------------------------------------------- core
def classify(rec, newest, refs_incl_desc):
    path = rec["path"]
    if rec.get("duplicates"):
        return "duplicate", "same content as " + ", ".join(rec["duplicates"][:3])
    low = path.lower()
    is_ref = any(_under(low, p) for p in REFERENCE_PREFIXES) or \
        any(part in REFERENCE_NAMES for part in low.split("/"))
    if is_ref:
        return "reference", "archive / old version / research location"
    nd = parse_date(newest)
    lc = parse_date(rec["last_commit"])
    n = rec["referenced_by"]["count"]
    if lc and nd:
        age = (nd - lc).days
        if refs_incl_desc == 0 and age > DEAD_DAYS and rec["depth"] > 1:
            return "dead", ("no references to it or below it; last commit %d days "
                            "before newest" % age)
        if age > STALE_DAYS and n > 0:
            return "stale", ("last commit %d days before newest; still referenced "
                             "by %d files" % (age, n))
        return "live", "touched %d days before newest commit; %d refs" % (age, n)
    return "live", "no commit date (untracked/new); %d refs" % n


def build_inventory(repo, out_dir=None):
    repo = os.path.abspath(repo)
    shallow = run(["git", "rev-parse", "--is-shallow-repository"], repo,
                  check=False).stdout.decode().strip() == "true"
    folders, files = walk_tree(repo)
    dates, newest = git_dates(repo)

    total_files = defaultdict(int)
    total_size = defaultdict(int)
    folder_files = defaultdict(list)  # recursive file list (for content hash)
    for f, size in files.items():
        for a in ancestors(f):
            total_files[a] += 1
            total_size[a] += size
            folder_files[a].append(f)

    needed = set()
    for fl in folder_files.values():
        if len(fl) >= 2:
            needed.update(fl)
    fhash = {f: sha1_file(os.path.join(repo, f)) for f in sorted(needed)}

    chash = {}
    for a, fl in folder_files.items():
        if len(fl) < 2:
            continue
        h = hashlib.sha1()
        prefix = len(a) + 1
        for f in sorted(fl, key=lambda x: x[prefix:]):
            h.update(f[prefix:].encode("utf-8", "replace") + b"\0" +
                     fhash[f].encode() + b"\n")
        chash[a] = h.hexdigest()
    by_hash = defaultdict(list)
    for a, h in chash.items():
        by_hash[h].append(a)

    exclude = []
    if out_dir:
        ap = os.path.abspath(out_dir)
        if ap.startswith(repo + os.sep):
            r = os.path.relpath(ap, repo).replace(os.sep, "/")
            exclude = [r + "/inventory.json", r + "/work/inventory-table.md"]
    refs = find_references(repo, list(folders), exclude)

    texts = {}
    for name in ("storage-map.json", "retention.json"):
        try:
            with open(os.path.join(repo, "production", name), "r", encoding="utf-8",
                      errors="replace") as fh:
                texts[name] = fh.read().replace("\\\\", "/").replace("\\", "/")
        except OSError:
            texts[name] = ""

    recs = {}
    for path in sorted(folders):
        r = sorted(refs.get(path, ()))
        recs[path] = {
            "path": path,
            "depth": path.count("/") + 1,
            "file_count_direct": folders[path]["direct"],
            "file_count_total": total_files.get(path, 0),
            "size_bytes": total_size.get(path, 0),
            "purpose": purpose_of(os.path.join(repo, path)),
            "last_commit": dates.get(path, ""),
            "referenced_by": {"count": len(r), "examples": r[:8]},
            "owner": owner_of(path),
            "in_storage_map": path in texts["storage-map.json"],
            "in_retention": path in texts["retention.json"],
            "content_hash": chash.get(path, ""),
            "duplicates": [],
        }

    for group in by_hash.values():
        if len(group) < 2:
            continue
        for a in group:
            recs[a]["duplicates"] = sorted(
                b for b in group if b != a and not _under(b, a) and not _under(a, b))

    sub_total = defaultdict(int)
    for p, rec in recs.items():
        n = rec["referenced_by"]["count"]
        sub_total[p] += n
        for a in ancestors(p):
            sub_total[a] += n
    for p, rec in recs.items():
        rec["referenced_by_incl_descendants"] = sub_total[p]
        rec["status"], rec["status_reason"] = classify(rec, newest, sub_total[p])
        rec["status_basis"] = "heuristic"

    return {
        "made": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "shallow": shallow,
        "newest_commit": newest,
        "folders": [recs[p] for p in sorted(recs)],
    }


def esc_cell(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def write_outputs(inv, out_dir):
    os.makedirs(os.path.join(out_dir, "work"), exist_ok=True)
    with open(os.path.join(out_dir, "inventory.json"), "w", encoding="utf-8") as fh:
        json.dump(inv, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    lines = ["# Folder inventory (depth <= 3)", "",
             "Made %s; newest commit %s; shallow repo: %s. Status is a heuristic." % (
                 inv["made"], inv["newest_commit"], inv["shallow"]), "",
             "| path | owner | last_commit | size MB | files | refs | status | reason | purpose |",
             "|---|---|---|---|---|---|---|---|---|"]
    for f in inv["folders"]:
        if f["depth"] > 3:
            continue
        lines.append("| %s | %s | %s | %.2f | %d | %d | %s | %s | %s |" % (
            esc_cell(f["path"]), esc_cell(f["owner"]), f["last_commit"] or "-",
            f["size_bytes"] / 1048576.0, f["file_count_total"],
            f["referenced_by"]["count"], f["status"], esc_cell(f["status_reason"]),
            esc_cell(f["purpose"])))
    with open(os.path.join(out_dir, "work", "inventory-table.md"), "w",
              encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Folder inventory for the audit")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    t0 = time.time()
    inv = build_inventory(a.repo, a.out)
    write_outputs(inv, a.out)
    counts = defaultdict(int)
    for f in inv["folders"]:
        counts[f["status"]] += 1
    print("folders=%d shallow=%s newest=%s runtime=%.1fs %s" % (
        len(inv["folders"]), inv["shallow"], inv["newest_commit"], time.time() - t0,
        dict(sorted(counts.items()))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
