"""Testing the testers (4t piece 8): plant known faults in a copy of the game and count which testers catch them.

His plan of 19 Nov (advisor's 8th point): each week plant faults on purpose and record how many the testers
catch. Method: mutation testing with faults drawn from our own past finds (see
production/research/lane/TESTING-THE-TESTERS-2026-11-20.md). Never touches the game's own folder: the source is
copied outside the repository, one fault applied, built there, and each named tester run on that build.

A fault counts as caught by a tester when its run on the planted build fails something the same narrow run on the
clean build did not (a rule with more failures, a feel number newly outside its band, a new fault line, or a check
that broke). The clean runs are made first with the same arguments, so a fault the build already had never counts.

The machine testers run here with no model. The AI testers (player types, breakers, the panel) are tested in a
loop: each planted build stays in its own folder (OUT/<fault>/dist) so a loop can serve one to them; their catches
are added with --ai FILE (a JSON list of {"fault", "tester", "caught", "evidence"}).

    python plant.py [--only id1,id2] [--out DIR] [--report FILE] [--ai FILE]
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.dirname(HERE)
LANE_TOOLS = os.path.dirname(GATE)
REPO = os.path.abspath(os.path.join(LANE_TOOLS, "..", ".."))
sys.path.insert(0, os.path.join(LANE_TOOLS, "prototype"))
import build as proto_build  # noqa: E402

WORK = os.path.join(os.path.expanduser("~"), ".cache", "ledger-plant-work")
TESTERS = {
    "machine": ("machine_checks.py", "machine.json"),
    "consequences": ("consequences.py", "consequences.json"),
    "clumsy": ("clumsy.py", "report.json"),
    "feel": ("feel_numbers.py", "feel.json"),
}


def swiss_now():
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo("Europe/Zurich")).isoformat(timespec="minutes")
    except Exception:
        return datetime.datetime.now().isoformat(timespec="minutes")


def load_faults(path=os.path.join(HERE, "faults.json")):
    return json.load(open(path, encoding="utf-8"))["faults"]


def apply_fault(src_dir, fault):
    """Apply one fault to a source folder. Returns None, or why it could not be planted."""
    p = os.path.join(src_dir, fault["file"])
    if not os.path.exists(p):
        return "no file " + fault["file"]
    text = open(p, encoding="utf-8").read()
    n = text.count(fault["old"])
    if n != 1:
        return "the text to change occurs %d times in %s (must be once): the game moved on, renew the fault" % (n, fault["file"])
    open(p, "w", encoding="utf-8").write(text.replace(fault["old"], fault["new"]))
    return None


def build_variant(fault, dist, log=print):
    """Copy the game's source to the work folder, plant the fault (or none), build into dist. Returns (problem, src)."""
    work = proto_build.prepare_work(WORK, log=log)
    src = os.path.join(work, "src")
    os.makedirs(os.path.join(work, "assets"), exist_ok=True)  # built without the art, as the lane's tests are
    if fault:
        why = apply_fault(src, fault)
        if why:
            return why, src
    b = subprocess.run(["node", "tools/build.mjs"], cwd=work, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if b.returncode:
        first = (b.stderr.strip().splitlines() or ["(no message)"])[0]
        return "the planted source does not build: " + first[:200], src
    if os.path.exists(dist):
        shutil.rmtree(dist)
    shutil.copytree(os.path.join(work, "dist"), dist)
    # keep the planted source beside the build, so the content scan reads what was built
    shutil.copytree(src, os.path.join(dist, "_src"))
    return None, os.path.join(dist, "_src")


def run_tester(name, args, dist, src, out):
    script, result = TESTERS[name]
    cmd = [sys.executable, os.path.join(GATE, script), "--dist", dist, "--out", out] + list(args)
    if name == "machine":
        cmd += ["--src", src, "--baseline", os.path.join(out, "no-baseline.json")]
    os.makedirs(out, exist_ok=True)
    try:
        p = subprocess.run(cmd, cwd=GATE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=1800)
    except subprocess.TimeoutExpired:
        return {"broke": "the tester ran past 30 minutes"}
    open(os.path.join(out, "run.log"), "w").write(p.stdout)
    path = os.path.join(out, result)
    if not os.path.exists(path):
        return {"broke": "no %s written (exit %d): %s" % (result, p.returncode, p.stdout[-300:])}
    return json.load(open(path, encoding="utf-8"))


def records(name, rep):
    """Every failure a run reported, as (key, line, unreached): key is the rule (or the feel number's id), line
    tells failures of one rule apart, unreached marks a check that could not be made."""
    out = []
    if name == "feel":
        for r in rep.get("numbers", []):
            if r.get("verdict") in ("outside", "not measured"):
                out.append((r["id"], "%s: %s" % (r["id"], r["verdict"]), r["verdict"] == "not measured"))
        for f in rep.get("faults", []):
            t = f if isinstance(f, str) else json.dumps(f, sort_keys=True)
            out.append(("fault", "fault: " + t[:160], "not reached" in t))
        return out
    for r in rep.get("results", []):
        if r.get("ok") is False or r.get("ok") is None:
            text = " ".join(str(r.get(k, "")) for k in ("steps", "note", "where"))
            out.append((r["rule"], r["rule"] + " | " + str(r.get("where") or r.get("steps") or "")[:120],
                        r.get("ok") is None or "not reached" in text))
    return out


def watched(key, watch):
    return any(w == key or w in key for w in watch)


def caught(name, cleans, planted, watch):
    """Did the tester catch the planted fault? (True, False or None for not tested; the lines that show it.)

    Only the checks the fault aims at (watch) count. A line that differs between the two clean runs is noise and
    never counts. Caught: a new failure there, or more failures of a watched rule than any clean run had.
    Not tested: the tester broke, or a watched check could not be made, or (feel) the number already failed."""
    if isinstance(cleans, dict):
        cleans = [cleans]
    if "broke" in planted or any("broke" in c for c in cleans):
        return None, ["not tested: the tester broke: " + str(planted.get("broke") or "on the clean build")[:200]]
    cl = [[x for x in records(name, c) if watched(x[0], watch)] for c in cleans]
    pl = [x for x in records(name, planted) if watched(x[0], watch)]
    clean_lines = [set(l for _, l, u in c if not u) for c in cl]
    noise = set.union(*clean_lines) - set.intersection(*clean_lines) if clean_lines else set()
    known = set.union(*clean_lines) if clean_lines else set()
    new = sorted(l for _, l, u in pl if not u and l not in known and l not in noise)
    more = []
    noisy_rules = {l.split(" | ")[0] for l in noise}
    for key in sorted({k for k, _, u in pl if not u}):
        n = sum(1 for k, _, u in pl if k == key and not u)
        most = max(sum(1 for k, _, u in c if k == key and not u) for c in cl) if cl else 0
        if n > most and key not in noisy_rules and name != "feel":
            more.append("%s: %d failed, clean at most %d" % (key, n, most))
    if new or more:
        return True, (more + new)[:8]
    gaps = sorted({k for k, _, u in pl if u} | {k for c in cl for k, _, u in c if u})
    if gaps:
        return None, ["not tested: could not make " + ", ".join(gaps)[:200]]
    if name == "feel" and known:
        return None, ["not tested: already outside on the clean build: " + ", ".join(sorted(known))[:200]]
    return False, []


def table(rows, ai_rows):
    by = {}
    for r in rows + ai_rows:
        if r.get("caught") is None:
            continue
        t = by.setdefault(r["tester"], [0, 0])
        t[0] += 1 if r["caught"] else 0
        t[1] += 1
    return by


def write_report(path, faults, rows, ai_rows, when):
    by = table(rows, ai_rows)
    caught_any = {r["fault"] for r in rows + ai_rows if r.get("caught")}
    planted = sorted({r["fault"] for r in rows + ai_rows if r.get("planted") is not False and r.get("caught") is not None})
    lines = ["# Testers' catch record, %s" % when[:10], "",
             "Faults planted on purpose in a copy of the game (4t piece 8, his plan of 19 Nov), each taken from a fault "
             "our testing met before; the game's own folder is never changed. Made by tools/lane/gate/plant/plant.py, "
             "run at %s, no model." % when, "",
             "Caught by at least one tester: %d of %d faults planted and tested." % (len(caught_any), len(planted)), "",
             "## Per tester", "", "| Tester | Caught | Planted for it |", "|---|---|---|"]
    for t, (c, n) in sorted(by.items()):
        lines.append("| %s | %d | %d |" % (t, c, n))
    lines += ["", "## Per fault", "", "| Fault | What it does | Tester | Caught | What showed it |", "|---|---|---|---|---|"]
    for r in rows + ai_rows:
        f = next((x for x in faults if x["id"] == r["fault"]), {"plain": ""})
        state = "not planted" if r.get("planted") is False else ("yes" if r.get("caught") else "NO" if r.get("caught") is False else "not run")
        lines.append("| %s | %s | %s | %s | %s |" % (r["fault"], f.get("plain", ""), r["tester"], state,
                                                    "; ".join([r["evidence"]] if isinstance(r.get("evidence"), str) else r.get("evidence", []))[:300].replace("|", "/")))
    missed = [r for r in rows + ai_rows if r.get("caught") is False]
    lines += ["", "## Missed, for the next loop's list", ""]
    lines += ["- %s by %s" % (r["fault"], r["tester"]) for r in missed] or ["- none"]
    if not ai_rows:
        lines += ["", "The AI testers (player types, breakers, the panel) were not run on planted builds this time; "
                  "they are tested in a loop: each planted build stays in its own folder under the run's output for a loop to serve them."]
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")


def main(argv=None):
    with proto_build.work_lock(WORK):  # never two plant runs (or a plant run and a build) in one work folder
        return _main(argv)


def _main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", default="")
    ap.add_argument("--out", default=os.path.join(os.path.expanduser("~"), ".cache", "ledger-plant",
                                                   datetime.datetime.now().strftime("%Y%m%d-%H%M")))
    ap.add_argument("--report", default=None)
    ap.add_argument("--ai", default=None)
    ap.add_argument("--faults", default=os.path.join(HERE, "faults.json"))
    a = ap.parse_args(argv)
    for d in [a.out] + ([a.report] if a.report else []):
        if proto_build._inside_repo(d):
            raise SystemExit("write the run outside the repository (copy the report into production/lane/ by hand): " + d)
    when = swiss_now()
    faults = load_faults(a.faults)
    only = [x for x in a.only.split(",") if x]
    if only:
        faults = [f for f in faults if f["id"] in only]
    os.makedirs(a.out, exist_ok=True)
    clean_dist = os.path.join(a.out, "clean", "dist")
    why, clean_src = build_variant(None, clean_dist)
    if why:
        raise SystemExit("the clean build failed: " + why)
    clean = {}
    rows = []
    for f in faults:
        dist = os.path.join(a.out, f["id"], "dist")
        why, src = build_variant(f, dist)
        if why:
            rows.append({"fault": f["id"], "tester": "-", "planted": False, "caught": None, "evidence": [why]})
            print("not planted", f["id"], why, flush=True)
            continue
        for t, args in f["testers"].items():
            key = (t, tuple(args))
            if key not in clean:  # two clean runs, so run-to-run noise is seen and never counted
                tag = t + "-" + "-".join(args).replace("-", "").replace(",", "+")[:30]
                clean[key] = [run_tester(t, args, clean_dist, clean_src, os.path.join(a.out, "clean", tag + "-%d" % i))
                              for i in (1, 2)]
            rep = run_tester(t, args, dist, src, os.path.join(a.out, f["id"], t))
            ok, ev = caught(t, clean[key], rep, f.get("watch") or [])
            rows.append({"fault": f["id"], "tester": t, "caught": ok, "evidence": ev})
            print("%-28s %-13s %s" % (f["id"], t, {True: "caught", False: "MISSED", None: "not tested"}[ok]), flush=True)
    ai_rows = json.load(open(a.ai, encoding="utf-8")) if a.ai else []
    json.dump({"when": when, "rows": rows, "ai": ai_rows}, open(os.path.join(a.out, "catch.json"), "w"), indent=1)
    report = a.report or os.path.join(a.out, "TESTER-CATCH.md")
    write_report(report, load_faults(a.faults), rows, ai_rows, when)
    print("report:", report)
    return 0 if all(r.get("caught") for r in rows if r.get("planted") is not False and r["tester"] != "-") else 1


if __name__ == "__main__":
    sys.exit(main())
